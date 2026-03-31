# Notes Tutorials Replacement Design

## Goal

Replace the site's existing tutorial content with the Markdown notes from `/Users/krystal/Documents/notes/_tutorials` while preserving the current Jekyll theme, routing, and deployment workflow.

## Scope

- Replace the entire `_tutorials` directory in the site repository.
- Keep layouts, includes, assets, Pages workflow, and configuration unchanged.
- Validate the result with a fresh Jekyll build before publishing.

## Approach Options

### Option 1: Full `_tutorials` replacement

- Remove the current site `_tutorials` content.
- Copy in `/Users/krystal/Documents/notes/_tutorials` as the new `_tutorials` directory.
- Rebuild the site locally and publish if the build succeeds.

Trade-offs:
- Produces a clean content reset with no stale tutorials left behind.
- Assumes the notes directory is already formatted for this site structure.

### Option 2: Incremental merge

- Copy only matching or new files from the notes directory.

Trade-offs:
- Lower immediate churn.
- Risks leaving old tutorials mixed with the new content set.

### Option 3: Broader notes import

- Import more than `_tutorials` from the notes workspace.

Trade-offs:
- Could support a larger content migration later.
- Unnecessarily risky for this request because the current site expects `_tutorials` specifically.

## Recommendation

Use Option 1. The note files already match the site's tutorial Markdown/front matter pattern, and a full directory replacement is the safest way to ensure the published content reflects the new source exactly.

## Validation

- Run `bundle exec jekyll build` in the site repo.
- Check that `_site/tutorials/` is generated.
- Push to `main` and verify GitHub Pages responds successfully.
