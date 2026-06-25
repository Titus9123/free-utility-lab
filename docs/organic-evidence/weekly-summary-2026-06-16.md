# Free Utility Lab weekly organic evidence — 2026-06-16

Status: initial post-Goal-18 measurement log. Keep this file non-sensitive: no raw Google exports, user-level data, credentials, tokens, private account IDs, or private query dumps.

## Operating recommendation

Do not expand yet. The correct next operating mode is: publish, index, measure, and only then decide.

- Goal 18 remains active: no new clusters, pages, variants, support pages, or assets without real signal or explicit operator approval.
- Allowed work this week: Search Console ownership/sitemap confirmation, GA4 realtime/event verification, QA on existing pages, evidence logging, and non-expansion fixes.
- Ads remain off until GSC/GA4 are readable and there is a baseline.
- Custom domain remains prepared but not cut over until measurement is stable.

## Deployment / public crawlability

- Repository status checked: `main` is synced with `origin/main`.
- Latest published commit checked: `b8757f0 ci: install pytest in validation workflow`.
- Validation workflow checked: latest `Validate Free Utility Lab` run is successful.
- GitHub Pages workflow checked: latest Pages build/deployment is successful.
- Home checked: `https://titus9123.github.io/free-utility-lab/` returns HTTP 200.
- Sitemap checked: `https://titus9123.github.io/free-utility-lab/sitemap.xml` returns HTTP 200.
- Sitemap URL count: 91.
- Sitemap unique URL count: 91.
- Robots checked: `https://titus9123.github.io/free-utility-lab/robots.txt` returns HTTP 200 and points to the live sitemap.
- Google site verification file checked: `google4164797b9ea878c8.html` returns HTTP 200 with the expected verification body.

## GSC property

- Property intended: `https://titus9123.github.io/free-utility-lab/`.
- Sitemap intended: `https://titus9123.github.io/free-utility-lab/sitemap.xml`.
- OAuth reauthorized on 2026-06-18: API credentials are usable again for `free-utility-lab-google-stack`; no tokens or secrets were written to this evidence log.
- GSC property visibility confirmed by API on 2026-06-18: `https://titus9123.github.io/free-utility-lab/` is visible with `siteOwner` permission.
- Sitemap submitted: already present in GSC before the latest API action.
- Sitemap last submitted according to GSC API: `2026-06-09T14:13:07.603Z`.
- Sitemap current GSC API state on 2026-06-18: `isPending=true`, `errors=0`, `warnings=0`.
- New submit attempt on 2026-06-18: blocked by Google with HTTP 403 because the current OAuth scope is readonly; this does not remove the already-present sitemap entry.
- Submitted URL count seen in GSC: not exposed by the sitemap list response in this run.
- Search Analytics snapshot for `2026-05-21..2026-06-17`: API query succeeded; 0 rows, 0 clicks, 0 impressions for the property.
- Follow-up Search Analytics recheck on 2026-06-18 for `2026-05-21..2026-06-17`: API query still succeeds; 0 rows, 0 clicks, 0 impressions.
- Priority URL index inspection: not performed in this run; current OAuth scope is readonly and suitable for measurement, not write/request-index actions.
- Indexed priority URLs: not checked.
- Not indexed priority URLs: not checked.
- Manual actions/security issues: not checked in this run.

## GA4 property

- Measurement ID detected on site: `G-54GQ1ZT341`.
- HTML measurement coverage from prior technical scan: 90 pages with GA4 installed.
- Measurement bridge from prior technical scan: present on 83 pages.
- GTM: not installed.
- Ads/scripts: 0 pages.
- Realtime tested: not tested in this run.
- GA4 Admin API visibility on 2026-06-18: property `Free Utility Lab` is visible as `properties/540515052` with web stream `Free Utility Lab Web`, measurement ID `G-54GQ1ZT341`, default URI `https://titus9123.github.io/free-utility-lab/`.
- GA4 Data API snapshot for `2026-05-21..2026-06-17`: query succeeded for the Free Utility Lab property; totals were 1 view, 1 session, 1 active user, and 5 events, all on `/free-utility-lab/`.
- Events confirmed by API in aggregate: 5 total events for the period.
- Event-name breakdown pulled on 2026-06-18 for `2026-05-21..2026-06-17`: `asset_view` 1, `first_visit` 1, `page_view` 1, `scroll` 1, `session_start` 1.
- Events confirmed by API by configured event name:
  - `asset_view`: 1.
  - `tool_start`: 0.
  - `tool_complete`: 0.
  - `copy_click`: 0.
  - `print_click`: 0.
  - `download_click`: 0.
  - `support_page_click`: 0.
  - `related_tool_click`: 0.
  - `directory_filter_use`: 0.
- Private payload check: no private payloads were added to this evidence log.
- OAuth blocker status: resolved for readonly measurement on 2026-06-18.

## Page evidence

Page-level organic search evidence is now API-readable but not yet actionable. Search Console query for `2026-05-21..2026-06-17` returned 0 rows / 0 clicks / 0 impressions. GA4 Data API returned a very small first signal: 1 view, 1 session, 1 active user, and 5 events on `/free-utility-lab/`. Event-name breakdown confirms only one configured asset engagement event (`asset_view` 1) and no tool/completion/copy/print/download/support/related/directory events yet. This is enough to confirm measurement plumbing, not enough to justify expansion.

## Cluster summary

### MealPlanSheet

- Indexed priority pages: not available.
- Pages with impressions: not available.
- Pages with clicks: not available.
- Best event signal: not available.
- Action: hold; no expansion.

### BudgetReset

- Indexed priority pages: not available.
- Pages with impressions: not available.
- Pages with clicks: not available.
- Best event signal: not available.
- Action: hold; no expansion.

### MoveBudget

- Indexed priority pages: not available.
- Pages with impressions: not available.
- Pages with clicks: not available.
- Best event signal: not available.
- Action: hold; no expansion.

### AIStackCost

- Indexed priority pages: not available.
- Pages with impressions: not available.
- Pages with clicks: not available.
- Best event signal: not available.
- Action: hold; no expansion.

### Marketplace hubs

- Indexed priority hubs: not available.
- Pages with impressions: not available.
- Pages with clicks: not available.
- Best event signal: not available.
- Action: hold; no expansion.

## Decisions from evidence

- Refresh title/meta: no decision yet; wait for GSC/GA4 signals.
- Improve above-fold utility: no decision yet; wait for event/engagement signal or QA gap.
- Request indexing: likely useful after confirming GSC property and sitemap, but not marked complete here.
- Merge/canonicalize candidate: no decision yet.
- Keep/no change: yes, default action for all existing assets this week.
- Candidate for future expansion after Goal 18 approval: none selected in this evidence log; no implementation approved here.

## Actions explicitly not approved this week

- Custom-domain cutover: no.
- Live ads: no.
- New thin page expansion: no.
- New clusters/support pages/variants: no.
- Private Google exports in repo: no.

## Next human/API step

Reauthorization and baseline API verification are now complete for readonly measurement. Next measurement steps:

1. Wait for GSC sitemap processing to leave pending state, then recheck sitemap errors/warnings and Search Analytics rows.
2. Keep collecting Search Console and GA4 snapshots before deciding on any expansion.
3. If GSC remains at 0 impressions after the next crawl window, prioritize non-expansion fixes only: existing-page title/meta review, internal links, sitemap/indexing diagnostics, and QA on current assets.

Current decision: measurement plumbing is restored, but signal is still too small for expansion. Keep Goal 18 freeze active.

## 3-day scheduled recheck

Recheck date: 2026-06-22. Evidence range requested for GSC and GA4: `2026-05-21..2026-06-21` (through the day before execution).

- GSC API: not revalidated in this cron run because no reusable Google OAuth token/credential file was present on the host. This is a credential availability issue, not a real zero-data result. Previous readonly API state from 2026-06-18 remains the last confirmed API baseline in this file.
- GSC sitemap API state: not available for this run for the same missing-OAuth reason; therefore pending/errors/warnings were not refreshed by API.
- GSC Search Analytics: not available for this run; do not interpret as 0 clicks or 0 impressions.
- GA4 API: not revalidated in this cron run because no reusable Google OAuth token/credential file was present on the host. This is a metric-unavailable state, not a real zero.
- GA4 property target: `Free Utility Lab`, measurement ID `G-54GQ1ZT341`; prior API-visible property remains `properties/540515052` from the 2026-06-18 baseline.
- Public sitemap technical check: HTTP 200, XML parsed successfully, 91 URLs, 91 unique URLs, home URL present, and all URLs remain under `https://titus9123.github.io/free-utility-lab/`.
- Public robots technical check: HTTP 200, allows crawl, does not disallow `/`, and points to `https://titus9123.github.io/free-utility-lab/sitemap.xml`.
- Validation status: Goal 18 expansion-freeze validator and full validation bundle were run after this section update; results are recorded in the local cron output, not as private exports in this repo.
- Secrets check: documentation update contains aggregate status only; no OAuth tokens, refresh tokens, bearer strings, client secrets, private URLs, raw exports, or user-level analytics were added.

Conclusion: keep Goal 18 expansion freeze active. Public crawlability remains technically healthy, but API measurement could not be refreshed without a local reusable OAuth credential. No new assets, pages, clusters, variants, ads, or custom-domain cutover are approved by this recheck.

## 7-day scheduled recheck

Recheck date: 2026-06-26. Evidence range requested for GSC and GA4: `2026-05-21..2026-06-25` (through the day before execution).

- Google OAuth / connector state: a vault entry for `free-utility-lab-google-stack` is present, but API credential refresh failed with `invalid_grant: Token has been expired or revoked.` This means Google API metrics are unavailable for this run; it is not evidence of zero traffic or zero engagement.
- GSC property target: `https://titus9123.github.io/free-utility-lab/`.
- GSC sitemap API state: not refreshed because the Google credential could not be refreshed; pending/errors/warnings are unavailable for this run.
- GSC Search Analytics: not refreshed because the Google credential could not be refreshed; do not infer clicks, impressions, CTR, or position from this run.
- GA4 property target: `Free Utility Lab`, measurement ID `G-54GQ1ZT341`, API property `properties/540515052` from the prior baseline.
- GA4 totals and event breakdown: not refreshed because the Google credential could not be refreshed. The requested events (`tool_start`, `tool_complete`, `copy_click`, `print_click`, `download_click`, `support_page_click`, `related_tool_click`, `directory_filter_use`) remain unavailable by API for this recheck; do not infer zero counts.
- Public sitemap technical check: HTTP 200, XML parsed successfully, 91 URLs, 91 unique URLs, home URL present, and all URLs remain under `https://titus9123.github.io/free-utility-lab/`.
- Public robots technical check: HTTP 200, `text/plain`, allows crawl, does not disallow `/`, and points to `https://titus9123.github.io/free-utility-lab/sitemap.xml`.
- 3-day recheck review: the previous scheduled recheck also recorded API metrics as unavailable due to local OAuth usability; the 7-day recheck confirms this is now a real reauthorization blocker rather than a public crawlability problem.
- Secrets check: this section records aggregate status only. No OAuth tokens, refresh tokens, bearer strings, client secrets, private URLs, raw exports, or user-level analytics were added.

Conclusion: keep Goal 18 expansion freeze active. Public crawlability remains technically healthy, but GSC and GA4 evidence is blocked until the Google connection is reauthorized. No new assets, pages, clusters, variants, ads, or custom-domain cutover are approved by this recheck. Next action should be reauthorizing the Free Utility Lab Google Stack connection, then rerunning the same GSC sitemap/Search Analytics and GA4 event breakdown against existing pages only. If signal remains weak after API access is restored, optimize only existing pages with concrete evidence.
