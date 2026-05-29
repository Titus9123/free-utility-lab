# Free Utility Lab handoff

Repo: `/root/work/free-utility-lab`
Remote: `git@github.com:Titus9123/free-utility-lab.git`
Branch: `main`
GitHub Pages: `https://titus9123.github.io/free-utility-lab/`

## Current state

Free Utility Lab is now separated from Clarvix in the public repo and published to GitHub Pages under the neutral `Free Utility Lab` brand.

Latest completed work:
- Removed inherited GTM / `googletagmanager` snippets from all copied tool and support pages.
- Rewrote public root copy and privacy policy for neutral free-tool positioning.
- Rebuilt sitemap with 29 real URLs.
- Fixed broken migrated SVG markers (`/free-utility-lab/>`) in `asset-lab/index.html` and `accessibility-widget.js`.
- Removed public Clarvix markers from CSS/JS and switched accessibility widget localStorage key to `free_utility_lab_a11y`.
- Removed internal monetization language from public root and asset-lab pages.
- Fixed migration-corrupted JS regexes in BudgetReset, AIStackCost, MealPlanSheet and MoveBudget CSV/name escaping.

## Verification snapshot

Local verification currently passes:
- HTML files: 29
- HTML parse errors: 0
- Inline script `node --check` errors: 0
- Sitemap URLs: 29 unique
- Sitemap local missing: 0
- Bad root-relative links outside `/free-utility-lab/`: 0
- Public forbidden markers outside this handoff: 0 for:
  - `Clarvix`, `clarvix.net`, `contact@clarvix.net`
  - `GTM-KQ8MQBNQ`, `googletagmanager`
  - `adsbygoogle`, `googlesyndication`
  - `client_secret`, `access_token`, `PRIVATE KEY`
  - `/free-utility-lab/>`
  - `RPM`, `RPV`, `CPV`, `ad revenue`, `make ad money`, `passive income`
  - migration-corrupted regex marker `free-utility-lab/g`

Live verification from previous push passed with cache-bust for:
- `/`
- `/asset-lab/`
- `/sitemap.xml`
- sample BudgetReset / MealPlanSheet / MoveBudget support pages

## Workflow constraint

Use small, deterministic patches. Avoid broad destructive repo-wide replacements unless the exact script is narrowly scoped and verified.

## Next recommended step

Commit and push the latest JS-regex fixes + updated handoff, then verify live with cache-busted URLs and page-specific markers.

Suggested live checks after push:
- `https://titus9123.github.io/free-utility-lab/budgetreset/?v=<commit>` includes `replace(/"/g,'&quot;')` and no `free-utility-lab/g`.
- `https://titus9123.github.io/free-utility-lab/aistackcost/?v=<commit>` includes `aistackcost-recommendation.csv` and no `free-utility-lab/g`.
- `https://titus9123.github.io/free-utility-lab/mealplansheet/?v=<commit>` includes `mealplansheet-weekly-plan.csv` and no `free-utility-lab/g`.
- `https://titus9123.github.io/free-utility-lab/movebudget/?v=<commit>` includes `movebudget-result.csv` and no `free-utility-lab/g`.
