# Goal 15 priority QA — mini-tool verification

Date: 2026-06-15

Source: optimization audit recovery goals. Purpose: verify that priority organic/support pages behave like useful mini-tools, not thin SEO pages.

## QA standard

A page passes Goal 15 when it has:

- A visible, practical artifact/worksheet/table above or near the main content.
- Copy, print and CSV/download action markers where the page promises a template/tool.
- Tracking-safe action wiring through shared utility actions or explicit page handlers.
- FAQPage/BreadcrumbList/HowTo schema where appropriate.
- Internal links to the parent tool and relevant marketplace hub.
- Differentiated intent for near-duplicate long-tail pages.
- No credential/account/private-data requirement.

## Pages checked

### BudgetReset P0/P1

- `budgetreset/free-printable-monthly-bill-calendar-pdf/` — PASS
  - Added printable/copyable/exportable bill-calendar worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.
  - Differentiated as PDF-style month-view worksheet.

- `budgetreset/monthly-bill-calendar-template-free-pdf/` — PASS
  - Added printable/copyable/exportable bill-calendar worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.
  - Differentiated as template-first due-date/autopay worksheet.

- `budgetreset/monthly-bill-calendar-free-printable/` — PASS
  - Added printable/copyable/exportable bill-calendar worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.
  - Differentiated as family/refrigerator-friendly printable checklist.

- `budgetreset/monthly-bill-calendar-printable-free/` — PASS
  - Added printable/copyable/exportable bill-calendar worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.
  - Differentiated as due-date/paycheck timing worksheet.

- `budgetreset/biweekly-paycheck-budget-template-google-sheets-free/` — PASS
  - Added printable/copyable/exportable paycheck split worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.

- `budgetreset/paycheck-budget-template/` — PASS
  - Added printable/copyable/exportable paycheck budget worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.

- `budgetreset/debt-payoff-tracker/` — PASS
  - Added printable/copyable/exportable debt payoff worksheet.
  - Added FAQPage + BreadcrumbList schema.
  - Added parent BudgetReset + Finance tools links.

- `budgetreset/zero-based-budget-template/` — PASS
  - Added printable/copyable/exportable zero-based budget worksheet.
  - Added BreadcrumbList schema; existing FAQPage remains valid.
  - Added parent BudgetReset + Finance tools links.

### AIStackCost P0/P1

- `aistackcost/ai-tools-for-freelancers/` — PASS
- `aistackcost/best-free-ai-tools-for-freelancers/` — PASS
- `aistackcost/top-10-ai-tools-for-freelancers/` — PASS
- `aistackcost/best-ai-tools-for-small-business/` — PASS
- `aistackcost/chatgpt-claude-gemini-comparison/` — PASS

Evidence: static QA confirms stack preset/comparison table/methodology, copy/print/CSV actions, FAQPage, BreadcrumbList, HowTo schema, and links to `ai-tools` + parent AIStackCost.

### MealPlanSheet spot checks

- `mealplansheet/weekly-meal-planner-printable/` — PASS
  - Existing copy/print/export artifact confirmed.
  - Added FAQPage schema.

- `mealplansheet/grocery-list-template-free-editable/` — PASS
  - Existing copy/print/export artifact confirmed.
  - Added FAQPage schema.

### MoveBudget spot checks

- `movebudget/moving-cost-calculator-no-email/` — PASS
  - Existing copy/print/export artifact confirmed.
  - Added BreadcrumbList schema.

- `movebudget/free-printable-first-apartment-budget-worksheet/` — PASS
  - Existing copy/print/export artifact confirmed.
  - Added BreadcrumbList schema.

## Validator added

- `scripts/goal15_static_qa.py`
  - Checks priority mini-tool markers.
  - Checks schema markers for priority pages.
  - Checks important internal links.
  - Checks BudgetReset bill-calendar page differentiation with a text-similarity threshold.
  - Added to `scripts/run_all_validations.py` so the gate stays durable.

## Functional wiring fix

- `shared/scripts/utility-actions.js`
  - Added delegated click handling for `data-copy-target`, `data-csv-target`, and button-level `data-print-section` actions.
  - Improved print target resolution so pages using an element id plus a print button both work.

## Verification

- `python3 scripts/goal15_static_qa.py` — PASS.
- `python3 scripts/run_all_validations.py` — PASS: 91 pytest tests, 91 HTML files, 91 sitemap URLs, 168 JSON-LD blocks, no secrets.
- `docker compose config` — PASS.
- `docker compose build` — PASS.
- `docker compose run --rm validate` — PASS.

## Remaining external risks

- This goal validates repo-level and static mini-tool readiness. It does not prove Google indexation, GA4 live event ingestion, Search Console impressions, or real user engagement.
- Next priority remains `/goal 16`: update operator handoff so the project no longer references stale 49-URL assumptions.
