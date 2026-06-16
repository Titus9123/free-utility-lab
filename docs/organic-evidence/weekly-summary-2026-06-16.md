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
- Sitemap submitted: not confirmed by API in this run.
- Sitemap last read: not available from API in this run.
- Submitted URL count seen in GSC: not available from API in this run.
- Priority URLs checked in GSC UI/API: not available from API in this run.
- Indexed priority URLs: not available from API in this run.
- Not indexed priority URLs: not available from API in this run.
- Manual actions/security issues: not available from API in this run.
- Blocker: Google OAuth token for `free-utility-lab-google-stack` is present in the vault but unusable: `invalid_grant: Token has been expired or revoked.`
- Remediation attempted: the Clarvix Connect state for `free-utility-lab-google-stack` was moved to `needs_reauth` and a fresh private reauthorization link was generated locally at `/root/clarvix-connect-links/free-utility-lab-google-stack.url` with token redacted from logs. Metrics remain unavailable until the operator completes Google consent again.

## GA4 property

- Measurement ID detected on site: `G-54GQ1ZT341`.
- HTML measurement coverage from prior technical scan: 90 pages with GA4 installed.
- Measurement bridge from prior technical scan: present on 83 pages.
- GTM: not installed.
- Ads/scripts: 0 pages.
- Realtime tested: not confirmed by API in this run.
- Events confirmed by API:
  - `asset_view`: not available.
  - `tool_start`: not available.
  - `tool_complete`: not available.
  - `copy_click`: not available.
  - `print_click`: not available.
  - `download_click`: not available.
  - `support_page_click`: not available.
  - `related_tool_click`: not available.
  - `directory_filter_use`: not available.
- Private payload check: no private payloads were added to this evidence log.
- Blocker: same OAuth error prevents live GA4 Admin/Data API verification: `invalid_grant: Token has been expired or revoked.`
- Remediation attempted: the private Google Stack reconnect flow is ready; API verification must be rerun after Google consent stores a new refresh token.

## Page evidence

No page-level organic decisions this week. API access is blocked, so this log intentionally does not infer clicks, impressions, CTR, average position, sessions, or event counts.

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

Reauthorize Google Stack OAuth for `free-utility-lab-google-stack` using the fresh private link stored at `/root/clarvix-connect-links/free-utility-lab-google-stack.url`, then verify in this order:

1. GSC property visibility for `https://titus9123.github.io/free-utility-lab/`.
2. Sitemap submitted/processed state for `https://titus9123.github.io/free-utility-lab/sitemap.xml`.
3. GA4 realtime/event reception for the public site.
4. First real page/query/event evidence snapshot.

Until those are done, treat external metrics as unavailable, not as zero.
