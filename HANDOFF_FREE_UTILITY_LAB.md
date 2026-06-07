# Free Utility Lab handoff

Repo: `/root/work/free-utility-lab`
Remote: `git@github.com:Titus9123/free-utility-lab.git`
Branch: `main`
GitHub Pages: `https://titus9123.github.io/free-utility-lab/`

## Current state

Free Utility Lab is separated from Clarvix in the public repo and published to GitHub Pages under the neutral `Free Utility Lab` brand.

Latest organic-growth work:

- Added 20 new long-tail SEO support pages across MealPlanSheet, BudgetReset, MoveBudget and AIStackCost.
- Rebuilt sitemap with 49 real URLs, trailing-slash root URL and `lastmod` values.
- Added OpenGraph and Twitter metadata to all HTML pages.
- Added a shared `free-utility-lab-tracking.js` event loader across all pages.
- Added internal links from hub/main pages into new organic-search guides.
- Added docs:
  - `docs/organic-traffic-growth-plan.md`
  - `docs/google-stack-setup-checklist.md`
  - `docs/distribution-kit.md`

## Verification snapshot

Local verification currently passes:

- HTML files: 49
- Sitemap URLs: 49 unique
- Local sitemap URL check: 49/49 returned HTTP 200
- Canonicals: present on all HTML pages
- OpenGraph metadata: present on all HTML pages
- Twitter metadata: present on all HTML pages
- Tracking loader: present on all HTML pages
- Body `data-asset-id`: present on all HTML pages
- Shared tracking JS: `node --check` passed
- Git diff whitespace check: passed

## Measurement status

- Current neutral Free Utility Lab pages now have local `dataLayer`/event instrumentation.
- GA4/GTM external collector is intentionally not hardcoded yet because a dedicated Free Utility Lab Measurement ID or GTM container ID is still needed.
- Search Console verification/submission still requires user Google account action.

## Next recommended step

Commit/push the organic-growth updates, wait for GitHub Pages deployment, then verify live with cache-busted URLs:

- `https://titus9123.github.io/free-utility-lab/sitemap.xml?v=<commit>` should include 49 URLs.
- `https://titus9123.github.io/free-utility-lab/mealplansheet/cheap-weekly-meal-plan/?v=<commit>` should return HTTP 200 and include `Open the free MealPlanSheet tool`.
- `https://titus9123.github.io/free-utility-lab/budgetreset/zero-based-budget-template/?v=<commit>` should return HTTP 200 and include `Open the free BudgetReset tool`.
- `https://titus9123.github.io/free-utility-lab/movebudget/moving-cost-checklist/?v=<commit>` should return HTTP 200 and include `Open the free MoveBudget tool`.
- `https://titus9123.github.io/free-utility-lab/aistackcost/best-ai-tools-for-small-business/?v=<commit>` should return HTTP 200 and include `Open the free AIStackCost tool`.
