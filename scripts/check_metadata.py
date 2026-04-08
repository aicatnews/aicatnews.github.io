#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from html import unescape
from pathlib import Path


TITLE_RE = re.compile(r"<title>\s*(.*?)\s*</title>", re.IGNORECASE | re.DOTALL)
DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="(.*?)"\s*/?>',
    re.IGNORECASE | re.DOTALL,
)


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def read_metadata(path: Path) -> tuple[str, str]:
    html = path.read_text(encoding="utf-8")
    title_match = TITLE_RE.search(html)
    desc_match = DESC_RE.search(html)
    title = collapse(title_match.group(1) if title_match else "")
    description = collapse(desc_match.group(1) if desc_match else "")
    return title, description


def collect_pages(site_dir: Path) -> list[Path]:
    pages = []
    for path in site_dir.rglob("*.html"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if "assets" in path.parts:
            continue
        if path.name.startswith("google"):
            continue
        pages.append(path)
    return sorted(pages)


def relpath(path: Path, site_dir: Path) -> str:
    return "/" + path.relative_to(site_dir).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check built HTML metadata against SEO title/description rules.")
    parser.add_argument("site_dir", nargs="?", default="_site", help="Built site directory")
    parser.add_argument("--brand", default="AICAT News", help="Brand suffix expected in page titles")
    parser.add_argument("--max-title", type=int, default=60, help="Maximum title length")
    parser.add_argument("--max-description", type=int, default=160, help="Maximum description length")
    parser.add_argument("--min-description", type=int, default=80, help="Minimum description length for normal pages")
    args = parser.parse_args()

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.exists():
        raise SystemExit(f"Site directory does not exist: {site_dir}")

    failures: list[str] = []
    title_to_pages: defaultdict[str, list[str]] = defaultdict(list)
    desc_to_pages: defaultdict[str, list[str]] = defaultdict(list)
    pages = collect_pages(site_dir)

    for path in pages:
        page = relpath(path, site_dir)
        title, description = read_metadata(path)
        if not title:
            failures.append(f"{page}: missing <title>")
        if not description:
            failures.append(f"{page}: missing meta description")
        if title and len(title) > args.max_title:
            failures.append(f"{page}: title too long ({len(title)} chars): {title}")
        if description and len(description) > args.max_description:
            failures.append(
                f"{page}: description too long ({len(description)} chars): {description}"
            )
        if page != "/404.html" and description and len(description) < args.min_description:
            failures.append(
                f"{page}: description too short ({len(description)} chars): {description}"
            )
        if page == "/index.html":
            if title.startswith(args.brand):
                failures.append(f"{page}: homepage title should lead with topic keywords, not the brand")
            if args.brand not in title:
                failures.append(f"{page}: homepage title must include the brand")
        else:
            if title and not title.endswith(f"| {args.brand}"):
                failures.append(f"{page}: page title should end with '| {args.brand}': {title}")
        if title and args.brand not in title:
            failures.append(f"{page}: title must include the brand")
        if title:
            title_to_pages[title].append(page)
        if description:
            desc_to_pages[description].append(page)

    for title, paths in sorted(title_to_pages.items()):
        if len(paths) > 1:
            failures.append(f"duplicate title across {', '.join(paths)}: {title}")

    for description, paths in sorted(desc_to_pages.items()):
        if len(paths) > 1:
            failures.append(f"duplicate description across {', '.join(paths)}: {description}")

    if failures:
        print("Metadata check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Metadata check passed for {len(pages)} HTML pages in {site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
