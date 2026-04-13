# IndexNow Submit Tool Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a reusable IndexNow submission tool that reads the key from `.env`, supports sitemap and git-diff URL collection, and avoids committing the secret key in tracked config files.

**Architecture:** Use a small Python CLI in `scripts/` so URL collection, payload generation, and submission logic live in one place with testable helpers. Keep the public root key file in the repo, but move the secret source of truth into `.env` and remove `.env` from git tracking so future edits do not get committed.

**Tech Stack:** Python 3 standard library, Git, existing Jekyll `_config.yml`, `.env`

---

### Task 1: Add failing tests for IndexNow helpers

**Files:**
- Create: `tests/test_indexnow_submit.py`

**Step 1: Write the failing test**

```python
def test_build_payload_uses_host_key_and_urls():
    payload = build_payload(...)
    assert payload["keyLocation"].endswith(".txt")
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_indexnow_submit -v`
Expected: FAIL because the module does not exist yet.

### Task 2: Implement the CLI and helpers

**Files:**
- Create: `scripts/indexnow_submit.py`
- Modify: `.env`
- Modify: `.gitignore`
- Delete: `2D30F8D3D76790FE2E2D4BA11F54CD7F.txt`
- Create: `9392961acc734a38b55a177477c1df13.txt`

**Step 1: Write minimal implementation**

Add a Python CLI that:
- loads `INDEXNOW_KEY` from `.env` or environment
- reads host from `_config.yml` unless overridden
- supports `--mode sitemap` and `--mode diff`
- optionally validates `200` pages
- POSTs JSON to `https://api.indexnow.org/IndexNow`

**Step 2: Run targeted tests**

Run: `python3 -m unittest tests.test_indexnow_submit -v`
Expected: PASS

### Task 3: Verify workflow end-to-end

**Files:**
- Modify: `scripts/indexnow_submit.py` if verification finds gaps

**Step 1: Verify no tracked secret remains**

Run: `git ls-files .env`
Expected: no output

**Step 2: Verify help output and payload preview**

Run: `python3 scripts/indexnow_submit.py --help`
Expected: exit 0 with CLI usage

**Step 3: Verify build still works**

Run: `bundle exec jekyll build`
Expected: exit 0
