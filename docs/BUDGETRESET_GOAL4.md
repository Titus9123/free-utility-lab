# Marketplace Foundation — Goal 4 BudgetReset Upgrade

Goal 4 upgrades the live BudgetReset tool as the first deeper organic mini-product in Free Utility Lab.

## Scope completed

- Kept the current GitHub Pages canonical/base URL unchanged.
- Did not migrate domain or alter existing support-page canonicals.
- Added shared marketplace/print CSS to the main BudgetReset page.
- Added shared `utility-actions.js` wiring for copy/download/print actions.
- Improved above-the-fold clarity with a 3-step workflow:
  1. Add income.
  2. Review bills + debt.
  3. Copy, CSV or print.
- Added a printable/copyable result area with `data-print-section="budgetreset-result"`.
- Added actions:
  - Copy plan summary.
  - Download CSV for Excel.
  - Print worksheet.
  - Existing PDF/print action preserved.
- Added generated plain-text summary output for users who want a quick offline result.
- Added marketplace hub links:
  - `/tools/`
  - `/finance-tools/`
  - `/printable-templates/`
- Added internal links to priority BudgetReset support pages for bill calendars, paycheck budgeting, debt payoff and zero-based budgeting.
- Added structured data:
  - `BreadcrumbList`
  - `HowTo`
- Updated marketplace catalog metadata for BudgetReset to include `HowTo` and the Goal 4 upgrade marker.

## Measurement notes

The BudgetReset page now records non-private interaction events for:

- `tool_start`
- `tool_complete`
- `copy_click`
- `download_click`
- `print_click`
- internal support/hub clicks via existing `data-event` attributes

The implementation does not intentionally send raw income, debts, names, text notes, emails or other private user inputs in tracking events.

## Verification

Covered by `tests/test_budgetreset_goal4.py` plus the full repo validation suite.
