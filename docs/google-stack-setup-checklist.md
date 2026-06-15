# Google stack setup checklist for Free Utility Lab

Use this checklist when connecting the neutral Free Utility Lab property to Google measurement.

Goal 17 source of truth:

- `docs/GOAL17_GSC_GA4_LEARNING_LOOP_2026-06-15.md`
- `docs/organic-evidence/WEEKLY_ORGANIC_EVIDENCE_TEMPLATE.md`

## Properties

Current production URL:

- Current GitHub Pages URL: `https://titus9123.github.io/free-utility-lab/`
- Sitemap: `https://titus9123.github.io/free-utility-lab/sitemap.xml`

Prepared later, not active yet:

- Custom domain: `freeutilitylab.com`
- Do not add a custom-domain property as the active reporting source, rewrite canonicals, or cut over until the domain migration is explicitly approved.

## GA4

1. Create or choose a GA4 property named `Free Utility Lab`.
2. Create or confirm a Web data stream for the current GitHub Pages production URL.
3. Confirm the public Measurement ID is installed only through approved shared tracking patterns.
4. Do not commit Measurement Protocol secrets, API keys, OAuth tokens, service-account keys, refresh tokens, or private exports.
5. Verify Realtime / DebugView shows safe standard events:
   - `asset_view`
   - `tool_start`
   - `tool_complete`
   - `copy_click`
   - `print_click`
   - `download_click`
   - `support_page_click`
   - `related_tool_click`
   - `directory_filter_use`
6. Confirm event parameters are bounded non-sensitive labels only, such as `asset_id`, `page_path`, `page_title`, `page_type`, `category`, `hub`, `output`, `format`, `type`, `step`, and `count`.

## GTM alternative

If using GTM instead of direct GA4:

1. Create a container for Free Utility Lab.
2. Copy only the public container ID, e.g. `GTM-XXXXXXX`.
3. Add the GA4 config tag inside GTM.
4. Publish the GTM container.
5. Verify with Tag Assistant and GA4 Realtime.
6. Do not store GTM account credentials or private preview/debug exports in the repository.

## Search Console

1. Add or confirm URL-prefix property:
   - `https://titus9123.github.io/free-utility-lab/`
2. Submit sitemap:
   - `https://titus9123.github.io/free-utility-lab/sitemap.xml`
3. Confirm sitemap status:
   - last read is recent;
   - discovered count is close to 91 URLs;
   - no global fetch error.
4. Request indexing for priority URLs listed in `docs/GOAL17_GSC_GA4_LEARNING_LOOP_2026-06-15.md`.
5. Monitor Page indexing:
   - Indexed
   - Discovered, currently not indexed
   - Crawled, currently not indexed
   - Duplicate without user-selected canonical

## Weekly pull

After connections work, record weekly aggregate evidence using:

- `docs/organic-evidence/WEEKLY_ORGANIC_EVIDENCE_TEMPLATE.md`

Track only non-sensitive aggregate evidence:

- GSC clicks/impressions/CTR/average position by page and query theme.
- GA4 sessions/views/users/events by asset path.
- Tool events: start, complete, print, copy, export/download, support-page click, related-tool click.
- Indexed priority URL count.
- Decisions: keep, refresh title/meta, improve above-fold utility, request indexing, merge/canonicalize, or defer.

## Security

Do not commit OAuth tokens, service-account keys, client secrets, refresh tokens, API keys, private keys, private Google exports, private query dumps, user-level analytics, or screenshots containing account identifiers.
