# Notes Tutorials Replacement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the site's `_tutorials` collection with the content from `/Users/krystal/Documents/notes/_tutorials` and republish the site.

**Architecture:** Keep the current Jekyll site unchanged outside the tutorial collection. Perform a full content swap for `_tutorials`, then validate with a clean local Jekyll build and publish to GitHub Pages.

**Tech Stack:** Jekyll, GitHub Pages, GitHub Actions, Markdown collections

---

### Task 1: Document the approved content migration

**Files:**
- Modify: `docs/plans/2026-03-30-notes-tutorials-replacement-design.md`
- Modify: `docs/plans/2026-03-30-notes-tutorials-replacement.md`

**Step 1: Record the approved migration scope**

Document that the source of truth is `/Users/krystal/Documents/notes/_tutorials` and that the site theme/layouts remain unchanged.

**Step 2: Confirm validation strategy**

Document local Jekyll build plus post-push Pages verification.

### Task 2: Replace tutorial content

**Files:**
- Modify: `_tutorials/*`

**Step 1: Remove the current tutorial collection content**

Delete the existing files under `_tutorials` in the site repository.

**Step 2: Copy in the notes tutorial collection**

Copy every Markdown file from `/Users/krystal/Documents/notes/_tutorials` into the repo `_tutorials` directory.

**Step 3: Inspect the resulting git diff**

Confirm the change set contains only the planned content replacement plus plan docs.

### Task 3: Verify and publish

**Files:**
- Verify: `_tutorials/*`
- Verify: `.github/workflows/jekyll.yml`

**Step 1: Run a fresh build**

Run `bundle exec jekyll build` and confirm it succeeds.

**Step 2: Publish to `main`**

Commit the content replacement and push to `origin/main`.

**Step 3: Verify deployment**

Check the latest Actions run and confirm `https://aicatnews.github.io/` returns successfully.
