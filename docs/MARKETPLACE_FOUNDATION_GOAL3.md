# Goal 3 — Marketplace foundation pages

Goal 3 turns the Goal 1 catalog and Goal 2 shared modules into visible marketplace-style hub pages without rewriting existing asset pages.

## Pages added

- `/tools/` — all live tools.
- `/printable-templates/` — print-focused tools/templates only.
- `/finance-tools/` — BudgetReset cluster entry.
- `/meal-planning-tools/` — MealPlanSheet cluster entry.
- `/moving-tools/` — MoveBudget cluster entry.
- `/ai-tools/` — AIStackCost cluster entry.

## Implementation rules

- Source of truth remains `data/marketplace.json`.
- Page renderer is `scripts/render_marketplace_pages.py`.
- Shared assets used by hub pages only:
  - `shared/styles/marketplace.css`
  - `shared/styles/print.css`
  - `shared/components/marketplace-components.js`
  - `shared/scripts/utility-actions.js`
- Existing asset pages are not mass-rewritten in this goal.
- Canonicals remain on the current GitHub Pages base until the final approved domain migration.
- No secrets, credentials, tracking IDs, or private user inputs are stored in the hub pages.

## SEO structure

Every Goal 3 hub includes:

- Unique title and meta description.
- Canonical URL.
- Breadcrumb UI and `BreadcrumbList` schema.
- Tool cards and `ItemList` schema.
- Links to related hubs.
- Filter controls for later client-side UX.
- `marketplace_tool_click` attributes for safe click tracking.

## Validation

Run:

```bash
python3 scripts/render_marketplace_pages.py
python3 -m pytest tests/test_marketplace_foundation_goal3.py -q
python3 scripts/validate_shared_modules.py
python3 scripts/validate_sitemap.py
python3 scripts/validate_site_links.py
```
