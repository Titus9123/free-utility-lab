# Modular Asset Lab Architecture

Free Utility Lab is currently a static HTML site. Goal 1 introduces a modular data foundation without changing public behavior.

## Source of truth

- `data/marketplace.json` is the central catalog for live and planned assets.
- `data/categories.json` defines marketplace/category hubs.
- `data/outputs.json` defines reusable output badges such as copy, CSV, print, PDF and download.
- `data/page-types.json` defines page type vocabulary.

The current domain/base URL remains `https://titus9123.github.io/free-utility-lab/` until a later approved domain migration.

## Required catalog fields

Each catalog asset/page must include:

- `id`
- `name`
- `slug`
- `category`
- `cluster`
- `public_url`
- `local_path`
- `page_type`
- `intent`
- `priority`
- `formats`
- `outputs`
- `user_types`
- `related_tools`
- `schema_types`
- `tracking_asset_id`
- `status`

Use `status: "live"` only when `local_path` exists in the static site. Use `status: "planned"` for future marketplace hubs or pages.

## How to add a new catalog entry

1. Add the page/tool to `data/marketplace.json`.
2. Use a stable, lowercase, hyphenated `id`.
3. Keep `public_url` on the current GitHub Pages base until the final domain migration.
4. Point `local_path` to the local HTML file for live pages.
5. Mark future pages as `planned` until the local HTML exists.
6. Choose a valid `page_type` and matching `formats`/`outputs`:
   - printable pages need `print` output;
   - calculator pages need `calculator` format;
   - spreadsheet/table-like pages should include `copy` or `csv` output.
7. Run validators before committing.

## Validators

Run from the repo root:

```bash
python3 scripts/validate_marketplace_catalog.py
python3 scripts/validate_sitemap.py
python3 scripts/audit_no_secrets.py data scripts
python3 -m pytest tests/test_marketplace_catalog.py tests/test_sitemap_validation.py tests/test_no_secrets.py -q
```

## Goal 1 boundary

Goal 1 does not rewrite HTML, add Docker, change canonicals, or migrate the domain. It only creates the catalog, vocabularies, validators, and tests that make later marketplace work safer.
