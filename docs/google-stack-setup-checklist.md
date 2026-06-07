# Google stack setup checklist for Free Utility Lab

Use this checklist when connecting the neutral Free Utility Lab property to Google measurement.

## Properties

Recommended production URL:

- Current GitHub Pages URL: `https://titus9123.github.io/free-utility-lab/`
- Preferred later: a neutral custom domain, then redirect GitHub Pages URLs if possible.

## GA4

1. Create or choose a GA4 property named `Free Utility Lab`.
2. Create a Web data stream for the production URL.
3. Copy the Measurement ID, e.g. `G-XXXXXXXXXX`.
4. Install it via the shared tracking loader/template, not manual page-by-page edits.
5. Verify Realtime shows:
   - page_view
   - asset_view
   - cta_click
   - link_click
   - tool-specific export/copy/print events when available

## GTM alternative

If using GTM instead of direct GA4:

1. Create a container for Free Utility Lab.
2. Copy the public container ID, e.g. `GTM-XXXXXXX`.
3. Add GA4 config tag inside GTM.
4. Publish the GTM container.
5. Verify with Tag Assistant and GA4 Realtime.

## Search Console

1. Add URL-prefix property:
   - `https://titus9123.github.io/free-utility-lab/`
2. If using a custom domain, also add a Domain property for the domain.
3. Submit sitemap:
   - `https://titus9123.github.io/free-utility-lab/sitemap.xml`
4. Request indexing for priority URLs:
   - `/free-utility-lab/`
   - `/free-utility-lab/mealplansheet/`
   - `/free-utility-lab/budgetreset/`
   - `/free-utility-lab/movebudget/`
   - `/free-utility-lab/aistackcost/`
5. Monitor Page indexing:
   - Indexed
   - Discovered, currently not indexed
   - Crawled, currently not indexed
   - Duplicate without user-selected canonical

## Weekly pull

After connections work, export/report weekly:

- GSC clicks/impressions/CTR by page and query
- GA4 sessions/views/users/events by asset path
- tool events: print, copy, export/download, calculate, support-page click
- indexed page count

## Security

Do not commit OAuth tokens, service account keys, client secrets, refresh tokens, API keys, or private keys.
