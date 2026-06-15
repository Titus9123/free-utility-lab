# Goal 17 GSC/GA4 learning loop

Date: 2026-06-15

Purpose: convert Free Utility Lab's repo-level readiness into organic-market evidence using Search Console and GA4 without committing credentials, private exports, or user-level data.

## Status

Goal 17 is **operator-ready / externally blocked**.

The repository now contains the external checklist, weekly evidence template, decision rules, and privacy guardrails needed to run the learning loop. Actual Search Console and GA4 confirmation still require Google account access and live property inspection outside this repo.

## Properties to use

Current production property:

- Public base: `https://titus9123.github.io/free-utility-lab/`
- Sitemap: `https://titus9123.github.io/free-utility-lab/sitemap.xml`

Prepared but not active:

- Custom domain: `freeutilitylab.com`
- Do not add a `CNAME`, rewrite canonicals, or move GSC/GA4 reporting to the custom domain until domain cutover is explicitly approved and complete.

## One-time external setup checklist

### Search Console

1. Open Google Search Console using the operator Google account.
2. Add or confirm URL-prefix property:
   - `https://titus9123.github.io/free-utility-lab/`
3. Verify ownership using an approved method for GitHub Pages.
4. Submit sitemap:
   - `https://titus9123.github.io/free-utility-lab/sitemap.xml`
5. Confirm sitemap status:
   - Last read is recent.
   - Discovered URL count is close to 91.
   - No global fetch errors.
6. Inspect priority URLs and request indexing where appropriate.
7. Record findings in the weekly evidence template below.

### GA4

1. Open the Free Utility Lab GA4 property or create it if missing.
2. Confirm the active web stream matches the current public base URL.
3. Open Realtime / DebugView while visiting priority pages.
4. Confirm these safe events appear when actions are performed:
   - `asset_view`
   - `tool_start`
   - `tool_complete`
   - `copy_click`
   - `print_click`
   - `download_click`
   - `support_page_click`
   - `related_tool_click`
   - `directory_filter_use`
5. Confirm event parameters are safe bounded labels only:
   - allowed examples: `asset_id`, `page_path`, `page_title`, `page_type`, `category`, `hub`, `output`, `format`, `type`, `step`, `count`.
   - blocked/private examples: email, name, address, phone, token, password, free-form note, free-form search query, private export rows.
6. Do not commit Measurement Protocol secrets, API keys, OAuth tokens, service-account keys, or private GA4 exports.

## Priority URL inspection list

Inspect these first because they represent hubs, main tools, and Goal 15 P0/P1 mini-tool pages.

### Marketplace hubs

- `https://titus9123.github.io/free-utility-lab/`
- `https://titus9123.github.io/free-utility-lab/tools/`
- `https://titus9123.github.io/free-utility-lab/printable-templates/`
- `https://titus9123.github.io/free-utility-lab/finance-tools/`
- `https://titus9123.github.io/free-utility-lab/meal-planning-tools/`
- `https://titus9123.github.io/free-utility-lab/moving-tools/`
- `https://titus9123.github.io/free-utility-lab/ai-tools/`

### Parent tools

- `https://titus9123.github.io/free-utility-lab/mealplansheet/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/`
- `https://titus9123.github.io/free-utility-lab/movebudget/`
- `https://titus9123.github.io/free-utility-lab/aistackcost/`

### BudgetReset P0/P1

- `https://titus9123.github.io/free-utility-lab/budgetreset/free-printable-monthly-bill-calendar-pdf/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/monthly-bill-calendar-template-free-pdf/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/monthly-bill-calendar-free-printable/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/monthly-bill-calendar-printable-free/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/biweekly-paycheck-budget-template-google-sheets-free/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/paycheck-budget-template/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/debt-payoff-tracker/`
- `https://titus9123.github.io/free-utility-lab/budgetreset/zero-based-budget-template/`

### AIStackCost P0/P1

- `https://titus9123.github.io/free-utility-lab/aistackcost/ai-tools-for-freelancers/`
- `https://titus9123.github.io/free-utility-lab/aistackcost/best-free-ai-tools-for-freelancers/`
- `https://titus9123.github.io/free-utility-lab/aistackcost/top-10-ai-tools-for-freelancers/`
- `https://titus9123.github.io/free-utility-lab/aistackcost/best-ai-tools-for-small-business/`
- `https://titus9123.github.io/free-utility-lab/aistackcost/chatgpt-claude-gemini-comparison/`

### Spot-check pages

- `https://titus9123.github.io/free-utility-lab/mealplansheet/weekly-meal-planner-printable/`
- `https://titus9123.github.io/free-utility-lab/mealplansheet/grocery-list-template-free-editable/`
- `https://titus9123.github.io/free-utility-lab/movebudget/moving-cost-calculator-no-email/`
- `https://titus9123.github.io/free-utility-lab/movebudget/free-printable-first-apartment-budget-worksheet/`

## Weekly evidence template

Create a dated copy outside private exports, for example:

- `docs/organic-evidence/weekly-summary-YYYY-MM-DD.md`

Do not paste raw private Google exports. Record only non-sensitive aggregate evidence.

```markdown
# Free Utility Lab weekly organic evidence — YYYY-MM-DD

## GSC property

- Property checked: https://titus9123.github.io/free-utility-lab/
- Sitemap submitted: yes/no
- Sitemap last read: YYYY-MM-DD or not available
- Submitted URL count seen in GSC: number or not available
- Indexed priority URLs: number / checked number
- Not indexed priority URLs: number / checked number

## Page evidence

### URL: <public URL>

- Index status: indexed / discovered not indexed / crawled not indexed / duplicate / unknown
- Clicks: aggregate number
- Impressions: aggregate number
- CTR: aggregate percent
- Average position: aggregate number
- Query themes: 3-5 non-sensitive phrase themes, not raw private exports
- GA4 `asset_view`: aggregate number
- GA4 tool-action events: aggregate counts for copy/print/download/start/complete
- Decision: keep / refresh title-meta / improve above-fold utility / request indexing / merge-canonicalize / no action
- Owner note: short non-sensitive note

## Cluster summary

- MealPlanSheet:
- BudgetReset:
- MoveBudget:
- AIStackCost:
- Marketplace hubs:

## Actions approved this week

- Action 1:
- Action 2:

## Actions explicitly not approved

- Custom-domain cutover: no unless explicitly approved
- Live ads: no unless organic and engagement evidence supports it
- New thin page expansion: no
```

## Decision rules

Use observed data, not assumptions:

- **Not indexed**: improve unique utility and internal links, then request indexing.
- **Discovered/crawled but not indexed**: strengthen above-the-fold artifact, reduce overlap, add examples, and request indexing again.
- **Impressions but low CTR**: rewrite title/meta for query intent; do not change the tool unless GA4 also shows weak engagement.
- **Clicks but low tool events**: improve above-the-fold instructions, visible artifact, and copy/print/download affordances.
- **High copy/print/download rate**: create more printable/exportable variants only if Goal 18 expansion criteria are met.
- **Similar pages both get impressions for the same theme**: monitor cannibalization; merge/canonicalize only after evidence, not before.
- **No impressions after indexation**: deprioritize expansion in that cluster and look for lower-competition long-tail demand.

## Repo validation before and after any measurement changes

Run:

```bash
python3 scripts/goal15_static_qa.py
python3 scripts/validate_final_launch_readiness.py
python3 scripts/run_all_validations.py
docker compose config
docker compose build
docker compose run --rm validate
git diff --check
git status --short --branch
```

## Completion criteria

Goal 17 repo work is complete when:

- This checklist exists.
- A non-sensitive weekly evidence template exists.
- Priority URLs are listed for GSC inspection and GA4 event confirmation.
- Decision rules tie changes to indexation, impressions, CTR, and safe event counts.
- Credentials/private exports remain out of the repo.

External completion remains blocked until the operator confirms GSC and GA4 in the Google accounts.
