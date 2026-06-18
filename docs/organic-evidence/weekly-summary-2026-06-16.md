# Free Utility Lab weekly organic evidence — 2026-06-16

Status: initial post-Goal-18 measurement log. Keep this file non-sensitive: no raw Google exports, user-level data, credentials, tokens, private account IDs, or private query dumps.

## Operating recommendation

Do not expand yet. The correct next operating mode is: publish, index, measure, and only then decide.

- Goal 18 remains active: no new clusters, pages, variants, support pages, or assets without real signal or explicit operator approval.
- Allowed work this week: Search Console ownership/sitemap confirmation, GA4 realtime/event verification, QA on existing pages, evidence logging, and non-expansion fixes.
- Ads remain off until GSC/GA4 are readable and there is a baseline.
- Custom domain remains prepared but not cut over until measurement is stable.
- Candidate ideas such as Make My Drive Fun Israel remain backlog-only unless explicitly approved as a Goal 18 exception.

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
- Events confirmed by API in aggregate: 5 total events for the period; event-name breakdown not pulled in this run.
- Events confirmed by API by configured event name:
  - `asset_view`: not checked by event-name dimension in this run.
  - `tool_start`: not checked by event-name dimension in this run.
  - `tool_complete`: not checked by event-name dimension in this run.
  - `copy_click`: not checked by event-name dimension in this run.
  - `print_click`: not checked by event-name dimension in this run.
  - `download_click`: not checked by event-name dimension in this run.
  - `support_page_click`: not checked by event-name dimension in this run.
  - `related_tool_click`: not checked by event-name dimension in this run.
  - `directory_filter_use`: not checked by event-name dimension in this run.
- Private payload check: no private payloads were added to this evidence log.
- OAuth blocker status: resolved for readonly measurement on 2026-06-18.

## Page evidence

Page-level organic search evidence is now API-readable but not yet actionable. Search Console query for `2026-05-21..2026-06-17` returned 0 rows / 0 clicks / 0 impressions. GA4 Data API returned a very small first signal: 1 view, 1 session, 1 active user, and 5 events on `/free-utility-lab/`. This is enough to confirm measurement plumbing, not enough to justify expansion.

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
- Candidate for future expansion after Goal 18 approval: Make My Drive Fun Israel remains backlog-only; no implementation approved here.

## Actions explicitly not approved this week

- Custom-domain cutover: no.
- Live ads: no.
- New thin page expansion: no.
- New clusters/support pages/variants: no.
- Private Google exports in repo: no.

## Next human/API step

Reauthorization and baseline API verification are now complete for readonly measurement. Next measurement steps:

1. Wait for GSC sitemap processing to leave pending state, then recheck sitemap errors/warnings and Search Analytics rows.
2. Pull a GA4 event-name breakdown for the Free Utility Lab property to verify named engagement events, not only aggregate event count.
3. Keep collecting Search Console and GA4 snapshots before deciding on any expansion.
4. Treat Make My Drive Fun Israel as backlog-only unless explicitly approved as a Goal 18 exception.

Current decision: measurement plumbing is restored, but signal is still too small for expansion. Keep Goal 18 freeze active.
