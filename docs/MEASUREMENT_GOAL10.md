# Goal 10 measurement and learning loop

Free Utility Lab now uses one safe event vocabulary for marketplace hubs, asset pages, and output actions. The purpose is to decide future page and asset work from observed data, not guesses.

## Standard events

Use only these page-level or asset-level events:

- `asset_view` — page view for a marketplace hub, support page, or asset page.
- `tool_start` — a user starts interacting with a calculator, checklist, planner, or generator.
- `tool_complete` — a tool produces a result or completes a meaningful workflow step.
- `copy_click` — a copy-to-clipboard action is requested.
- `print_click` — a printable artifact or worksheet is requested.
- `download_click` — a CSV, text, or downloadable artifact is requested.
- `support_page_click` — a link from an asset page to a support/priority page is clicked.
- `related_tool_click` — a marketplace card, related tool, or cross-cluster recommendation is clicked.
- `directory_filter_use` — a marketplace hub filter is used.

Legacy names such as calculator/generator start/complete events and old marketplace click names are normalized by the shared helper before forwarding.

## Safe payload contract

Allowed analytics payload fields are limited to non-private operational metadata such as asset ID, category, hub, page type, output type, format, language, step, count, and similar bounded labels.

Do not send private user input to analytics. Free-form notes, emails, names, addresses, phone numbers, search queries, tokens, and secret-like values must be filtered before an event reaches GA4 or any data layer consumer.

No credentials are required to emit the standardized events. The site pushes safe browser events only; operators connect or inspect GA4/Search Console outside the repository.

## GSC / GA4 review workflow

Review priority pages on a recurring cadence, starting with the main marketplace hubs and upgraded asset clusters:

1. In Search Console, export page-level rows for the current site property.
2. For every priority page, record whether it is indexed or not indexed.
3. Capture impressions, query list, average position, CTR, clicks, and the page URL.
4. Separate pages with impressions but low CTR from pages indexed with no impressions.
5. Separate pages crawled or discovered but not indexed from pages that have not been discovered.
6. In GA4, compare safe event counts for `asset_view`, `tool_start`, `tool_complete`, `copy_click`, `print_click`, `download_click`, `support_page_click`, `related_tool_click`, and `directory_filter_use`.
7. Record content actions from observed data, not guesses.

## Decision rules

- Not indexed: improve page utility/content, then request indexing.
- Impressions but low CTR: rewrite title/meta and improve snippet alignment.
- Clicks but low usage: improve above-the-fold tool clarity and output actions.
- High print/download rate: create more printable or downloadable templates in that cluster.
- High hub filtering or related-click rate: expand marketplace navigation and related tool coverage.
- No impressions after indexing: shift to lower-competition long-tail pages or add topical depth.

## Local validation

Run the standard bundle before publishing measurement changes:

```bash
python3 -m pytest -q
python3 scripts/run_all_validations.py
# Run the repository no-secret audit against data, scripts, shared assets, docs, and measurement JavaScript.
```
