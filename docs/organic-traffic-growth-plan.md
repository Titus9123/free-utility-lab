# Free Utility Lab organic traffic growth plan

Date: 2026-06-07

## Diagnosis

Free Utility Lab is live and crawlable, but it is not yet a traffic engine.

Confirmed current state:

- Public site: `https://titus9123.github.io/free-utility-lab/`
- Live sitemap: `https://titus9123.github.io/free-utility-lab/sitemap.xml`
- Published URLs: 29
- Live URL status: 29/29 returned HTTP 200 in the latest check
- Robots: allows crawling and points to the sitemap
- Canonicals: present on all HTML pages
- Structured data: present on tool and guide pages
- GA/GTM external measurement: not installed on the neutral Free Utility Lab property yet
- Local dataLayer events: present on most pages, but not connected to an analytics collector until GA4/GTM is installed
- Search Console for Clarvix Asset Lab: 0 clicks and 0 impressions in the checked windows
- GA4 Clarvix Asset Lab: 0 views/sessions/events in the latest 7-day window

Main bottleneck: discovery and measurement, not publication. The pages exist, but Google has no measurable search traction yet and the new neutral property is not fully connected to GA4/GSC.

## What must be fixed before scaling content

1. Measurement foundation
   - Install GA4 or GTM for the Free Utility Lab property.
   - Connect Search Console for `https://titus9123.github.io/free-utility-lab/` or, preferably, a custom domain.
   - Keep event tracking consistent across tool usage, export, print, copy and support-page clicks.

2. Search Console / indexing
   - Verify the neutral property in GSC.
   - Submit `/sitemap.xml`.
   - Inspect the 4 main tool URLs first, then the best support URLs.
   - Track indexed vs discovered-not-indexed vs crawled-not-indexed.

3. SEO technical polish
   - Add OpenGraph and Twitter metadata to every page.
   - Normalize the root sitemap URL with trailing slash.
   - Add `lastmod` to sitemap entries.
   - Add a shared tracking loader so future GA4/GTM wiring is one-file, not per-page chaos.

4. Content and topical authority
   - Do not keep launching isolated tools.
   - Expand the highest-demand clusters: MealPlanSheet, BudgetReset, MoveBudget, AIStackCost.
   - Add 20-40 new support pages only around clusters that have clear search demand and internal links.

5. Distribution / backlinks
   - Every cluster needs external discovery attempts: Reddit/community-safe posts, Pinterest-style images, directory submissions, owned profile links, and resource-page outreach.
   - Without links/distribution, Google may keep the pages at zero impressions for a long time.

## 30-day execution plan

### Phase 1 — Today: make the site measurable and index-ready

- Add shared event tracking loader across all pages.
- Add OG/Twitter social metadata across all pages.
- Improve sitemap freshness with trailing slash + `lastmod`.
- Verify 29 URLs locally and live.
- Prepare exact GSC/GA4 setup checklist for the user because OAuth/property verification requires account access.

### Phase 2 — Days 1-3: connect Google stack

Requires user/account action:

- Create or choose GA4 property for Free Utility Lab.
- Provide Measurement ID or GTM container ID for installation.
- Verify Search Console property.
- Submit sitemap.
- Request indexing for priority pages:
  1. `/free-utility-lab/`
  2. `/free-utility-lab/mealplansheet/`
  3. `/free-utility-lab/budgetreset/`
  4. `/free-utility-lab/movebudget/`
  5. `/free-utility-lab/aistackcost/`

### Phase 3 — Week 1: create demand surface

Add 20 long-tail pages:

MealPlanSheet:
- cheap weekly meal plan
- vegetarian meal planner
- family grocery budget planner
- meal plan calendar template
- healthy meal prep planner
- printable grocery list by category

BudgetReset:
- zero based budget template
- 50/30/20 budget calculator
- rent budget calculator
- grocery budget calculator
- emergency fund tracker
- bill organizer template

MoveBudget:
- moving box calculator
- moving supplies checklist
- moving cost checklist
- room by room packing checklist

AIStackCost:
- best AI tools for small business
- ChatGPT Claude Gemini comparison
- AI tools ROI calculator
- agency AI stack budget

### Phase 4 — Week 2: early optimization

- Pull GSC and GA4.
- If impressions > 0 and CTR weak: rewrite title/meta.
- If sessions > 0 and events weak: improve above-the-fold CTA/tool placement.
- Add stronger internal link blocks to pages receiving impressions.

### Phase 5 — Weeks 3-4: distribution and winner expansion

- Submit tools to free-tool and resource directories.
- Create Pinterest/share images for meal planner, grocery list, moving checklist, budget planner.
- Publish non-spam community posts where allowed.
- Pick 1-2 winning clusters by impressions + engagement.
- Add 10 more pages only around winners.

## Operating KPI dashboard

Weekly:

- GSC impressions by URL and query
- GSC clicks by URL and query
- CTR by page
- Indexed pages count
- GA4 sessions by asset
- GA4 events/session
- export/copy/print events
- support-page-to-tool clicks
- external links/referrals created

## Immediate implementation notes

I can implement technical improvements in the repo without passwords. I cannot complete GSC verification or create GA4 properties without the user's Google account/OAuth action. Once the Measurement ID or GTM ID is available, install it through the shared loader instead of editing every page manually.

## Execution update — 2026-06-09

Completed next organic sprint in the repo:

- Added 12 additional long-tail support pages across MealPlanSheet, BudgetReset, MoveBudget and AIStackCost.
- Regenerated sitemap from the actual HTML inventory.
- Kept GA4 event bridge, canonical tags, metadata, schema and no-live-ad safety rules on the new pages.
- Updated the distribution kit with the exact new URLs and 48-hour promotion actions.

Next operating action after deploy: submit/refresh the sitemap in Search Console and request indexing for the four main tools plus the 12 new support URLs.
