# Goal 2 — Shared static modules

Status: implemented as a conservative `shared/` foundation.

Goal 2 creates reusable components and browser helpers without mass-editing the existing 84 static HTML pages. The modules are ready for Goal 3 marketplace pages and later asset-cluster upgrades.

## Files

- `shared/components/marketplace-components.js`
  - `renderToolCard(asset, options)`
  - `renderBadgeList(items)`
  - `renderRelatedTools(assets, relatedIds, options)`
  - `renderBreadcrumb(items)`
  - `renderFaq(items)`
- `shared/scripts/utility-actions.js`
  - `copyText(text)`
  - `tableToCsv(rows)`
  - `downloadText(filename, text, mimeType)`
  - `createPrintSectionMarkup(id, innerHtml)`
  - `printSection(id)`
  - `filterMarketplaceItems(items, filters)`
  - `sanitizeTrackingPayload(payload)`
  - `trackSafe(eventName, payload)`
- `shared/styles/marketplace.css`
  - marketplace cards, badges, filters, breadcrumbs and FAQ styles.
- `shared/styles/print.css`
  - print-safe worksheet behavior and non-print hiding utilities.

## Boundary

This goal intentionally does not wire these modules into existing pages yet. Goal 3 should use them for `/tools/`, `/printable-templates/` and category hub pages. Later asset goals can migrate individual tool/support pages gradually.

## Safety rules

- Do not send free-form user input to analytics.
- Use `trackSafe()` instead of direct analytics calls in new shared-module pages.
- Keep the current GitHub Pages base path until final domain migration.
- Keep existing tracking and accessibility scripts intact.
