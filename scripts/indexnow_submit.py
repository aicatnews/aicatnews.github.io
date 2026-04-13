#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


DEFAULT_ENDPOINT = "https://api.indexnow.org/IndexNow"
DEFAULT_CONFIG = Path("_config.yml")
DEFAULT_ENV = Path(".env")
SHARED_PATH_PREFIXES = (
    "_config",
    "_data/",
    "_includes/",
    "_layouts/",
    "_plugins/",
    "_sass/",
    "assets/",
)


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def read_host_from_config(path: Path) -> str:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("url:"):
            continue
        value = line.split(":", 1)[1].split(" #", 1)[0].strip()
        if not value:
            continue
        parsed = urllib.parse.urlparse(value)
        if parsed.netloc:
            return parsed.netloc.strip()
        return value.replace("https://", "").replace("http://", "").strip().strip("/")
    raise ValueError(f"Could not find 'url' in {path}")


def collect_sitemap_urls(source: str | Path) -> list[str]:
    if isinstance(source, Path) or not str(source).startswith(("http://", "https://")):
        xml_text = Path(source).read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(str(source)) as response:
            xml_text = response.read().decode("utf-8")
    root = ET.fromstring(xml_text)
    urls: list[str] = []
    for node in root.iter():
        if node.tag.endswith("loc") and node.text:
            url = node.text.strip()
            if url and url not in urls:
                urls.append(url)
    return urls


def map_changed_files_to_urls(changed_files: Iterable[str], host: str) -> list[str]:
    urls: list[str] = []
    base = f"https://{host}"
    include_home = False
    for changed_file in changed_files:
        path = changed_file.strip()
        if not path:
            continue
        if path == "_pages/tutorials.md":
            include_home = True
            continue
        if path == "_pages/404.md":
            continue
        if path.startswith("_tutorials/") and path.endswith(".md"):
            slug = Path(path).stem
            urls.append(f"{base}/tutorials/{slug}/")
            continue
        if path.startswith(SHARED_PATH_PREFIXES) or path == "run.sh":
            include_home = True
    if include_home:
        urls.insert(0, f"{base}/")
    return dedupe(urls)


def dedupe(urls: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        ordered.append(url)
    return ordered


def build_payload(host: str, key: str, urls: list[str]) -> dict[str, object]:
    return {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }


def get_changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..{head}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def filter_live_urls(urls: Iterable[str], timeout: float = 10.0) -> list[str]:
    live_urls: list[str] = []
    for url in urls:
        request = urllib.request.Request(url, headers={"User-Agent": "aicatnews-indexnow/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status == 200:
                    live_urls.append(url)
        except urllib.error.HTTPError as exc:
            if exc.code == 200:
                live_urls.append(url)
        except urllib.error.URLError:
            continue
    return live_urls


def submit_payload(payload: dict[str, object], endpoint: str = DEFAULT_ENDPOINT) -> tuple[int, bytes]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.read()


def resolve_key(explicit_key: str | None, env_path: Path) -> str:
    if explicit_key:
        return explicit_key
    if os.environ.get("INDEXNOW_KEY"):
        return os.environ["INDEXNOW_KEY"]
    env_values = parse_env_file(env_path)
    if env_values.get("INDEXNOW_KEY"):
        return env_values["INDEXNOW_KEY"]
    raise ValueError("INDEXNOW_KEY not found in environment or .env")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit site URLs to IndexNow.")
    parser.add_argument("--mode", choices=("sitemap", "diff"), default="diff")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to _config.yml")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV), help="Path to .env file")
    parser.add_argument("--key", help="Override IndexNow key")
    parser.add_argument("--host", help="Override site host")
    parser.add_argument("--sitemap", help="Local sitemap path or remote sitemap URL")
    parser.add_argument("--base", default="HEAD~1", help="Diff base ref for diff mode")
    parser.add_argument("--head", default="HEAD", help="Diff head ref for diff mode")
    parser.add_argument("--check-live", action="store_true", help="Only submit URLs returning HTTP 200")
    parser.add_argument("--dry-run", action="store_true", help="Print payload JSON instead of submitting")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="IndexNow endpoint")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    env_path = Path(args.env_file)
    host = args.host or read_host_from_config(config_path)
    key = resolve_key(args.key, env_path)

    if args.mode == "sitemap":
        sitemap_source = args.sitemap or f"https://{host}/sitemap.xml"
        urls = collect_sitemap_urls(sitemap_source)
    else:
        changed_files = get_changed_files(args.base, args.head)
        urls = map_changed_files_to_urls(changed_files, host)

    if args.check_live:
        urls = filter_live_urls(urls)

    if not urls:
        print("No URLs to submit.", file=sys.stderr)
        return 1

    payload = build_payload(host, key, urls)

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    status, body = submit_payload(payload, endpoint=args.endpoint)
    print(f"IndexNow status: {status}")
    if body:
        print(body.decode("utf-8", errors="replace"))
    print(f"Submitted URLs: {len(urls)}")
    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    raise SystemExit(main())
