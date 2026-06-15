# Free Utility Lab handoff

Repo: `/root/work/free-utility-lab`
Remote: `git@github.com:Titus9123/free-utility-lab.git`
Branch: `main`
Public base: `https://titus9123.github.io/free-utility-lab/`
Target custom domain: `freeutilitylab.com` — prepared, **not cut over**

## Operating decision

Free Utility Lab is in **controlled launch-readiness state**.

The repository has strong static/product readiness, marketplace structure, mini-tool QA, Docker parity validation, no-secret checks, and domain-migration preparation. It is **not yet organic-market validated** because Search Console indexation, GA4 live event ingestion, impressions, CTR, and real user engagement still require external account verification.

Do not describe this as a fully proven organic launch until GSC/GA4 evidence exists.

## Current state

- Public site remains on GitHub Pages: `https://titus9123.github.io/free-utility-lab/`.
- Custom-domain cutover has not been performed.
- Live ads are not activated.
- Current inventory validated by the full project runner:
  - HTML files: 91
  - Sitemap URLs: 91
  - JSON-LD blocks: 168 after Goal 15
- Marketplace/category hubs exist for tools, printables, finance tools, meal-planning tools, moving tools, and AI tools.
- Priority pages have been checked against the mini-tool standard: useful artifact, copy/print/download or export actions, schema, internal links, and tracking-safe action wiring.

## Authoritative docs

Use these as the current source of truth:

- `docs/FINAL_LAUNCH_READINESS_GOAL13.md` — final controlled readiness state and launch guardrails.
- `docs/AUDIT_OPTIMIZATION_GOALS_2026-06-15.md` — audit recovery goals `/goal 14` through `/goal 18`.
- `docs/GOAL15_PRIORITY_QA_2026-06-15.md` — priority mini-tool QA evidence.
- `docs/DOMAIN_MIGRATION_GOAL11.md` — custom-domain migration runbook; preparation only, no cutover.
- `docs/MEASUREMENT_GOAL10.md` — GSC/GA4 measurement loop and privacy-safe event policy.
- `docs/organic-traffic-growth-plan.md` — original organic traffic plan.
- `docs/asset-organic-optimization-execution-plan.md` — later optimization/execution plan.
- `docs/asset-by-asset-organic-marketplace-action-plan.md` — asset-by-asset marketplace/action plan.

## Completed recovery goals

- `/goal 14` — repo cleanup and auditable state completed.
  - Generated Python/pytest caches ignored/cleaned.
  - Intentional diffs reviewed and committed.
  - Full local and Docker validation gates passed.

- `/goal 15` — priority mini-tool QA completed.
  - BudgetReset P0/P1 pages reinforced with worksheets, copy/print/CSV actions, schema, and links.
  - AIStackCost P0/P1 pages validated for artifact/action/schema/link coverage.
  - MealPlanSheet and MoveBudget spot checks passed after schema reinforcement where needed.
  - `scripts/goal15_static_qa.py` added and integrated into `scripts/run_all_validations.py`.
  - `shared/scripts/utility-actions.js` now delegates static HTML copy/print/download patterns reliably.

## Current quality gates

Run these before publishing or handing off new changes:

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

Expected current validation snapshot from Goal 15:

- `python3 scripts/goal15_static_qa.py` — PASS.
- `python3 scripts/run_all_validations.py` — PASS: 91 pytest tests, 91 HTML files, 91 sitemap URLs, 168 JSON-LD blocks, no secrets.
- `docker compose config` — PASS.
- `docker compose build` — PASS.
- `docker compose run --rm validate` — PASS.
- `git diff --check` — PASS.

## Guardrails that remain active

- Do not create a `CNAME` file or cut over `freeutilitylab.com` without explicit approval.
- Do not rewrite canonicals, Open Graph URLs, or sitemap URLs to `freeutilitylab.com` until custom-domain cutover is approved and executed.
- Do not activate live ads yet.
- Do not add thin support pages or clone pages manually.
- Use the asset factory path and validators for any future asset expansion.
- Do not commit secrets, tokens, private analytics exports, Search Console exports with sensitive account data, or private credentials.
- Do not claim market validation until external GSC/GA4 evidence exists.

## Measurement status

Repo-level measurement instrumentation is ready, but external account proof remains pending.

Implemented locally/static:

- Shared event loader and measurement bridge are present.
- Safe event patterns include `asset_view`, `tool_start`, `tool_complete`, `copy_click`, `print_click`, `download_click`, `support_page_click`, `related_tool_click`, and `directory_filter_use`.
- Payload sanitization is designed to avoid private fields such as emails, names, addresses, tokens, passwords, free-form queries, and secret-like values.

Still external/operator-owned:

- Verify or confirm the Search Console property for the current GitHub Pages URL.
- Submit/confirm sitemap: `https://titus9123.github.io/free-utility-lab/sitemap.xml`.
- Inspect priority URLs in GSC.
- Confirm GA4 receives safe live events from real page sessions.
- Start a weekly evidence log for indexation, impressions, CTR, positions 8-30, and tool-action engagement.

## Current publication check

After pushing/deploying a new commit to GitHub Pages, verify live with cache-busted URLs:

- `https://titus9123.github.io/free-utility-lab/sitemap.xml?v=<commit>` should include 91 URLs.
- `https://titus9123.github.io/free-utility-lab/tools/?v=<commit>` should load the tools marketplace hub.
- `https://titus9123.github.io/free-utility-lab/finance-tools/?v=<commit>` should load the finance tools hub.
- `https://titus9123.github.io/free-utility-lab/budgetreset/zero-based-budget-template/?v=<commit>` should expose a usable BudgetReset worksheet and actions.
- `https://titus9123.github.io/free-utility-lab/budgetreset/free-printable-monthly-bill-calendar-pdf/?v=<commit>` should expose a differentiated printable bill-calendar worksheet.
- `https://titus9123.github.io/free-utility-lab/mealplansheet/weekly-meal-planner-printable/?v=<commit>` should expose copy/print/export utility.
- `https://titus9123.github.io/free-utility-lab/movebudget/moving-cost-calculator-no-email/?v=<commit>` should expose calculator/worksheet utility.
- `https://titus9123.github.io/free-utility-lab/aistackcost/ai-tools-for-freelancers/?v=<commit>` should expose an AI stack preset/comparison artifact.

## Next recommended priority

Proceed to `/goal 17`: activate the external GSC/GA4 learning loop.

This should create or complete a non-sensitive operator checklist for:

- GSC property verification.
- Sitemap submission.
- Priority URL inspection.
- GA4 realtime event confirmation.
- Weekly evidence logging.
- Decision rules for refresh, merge/canonicalization, and expansion based on indexation, impressions, CTR, and engagement.

If Google account access is unavailable, document `/goal 17` as blocked by external account access rather than pretending it is complete.
