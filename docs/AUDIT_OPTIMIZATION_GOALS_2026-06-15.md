# Audit optimization recovery goals — 2026-06-15

Source: actionable audit comparing the original organic traffic plan, the later Claude/execution optimization plan, and the current repository state.

## /goal 14 — clean auditable repository state

**Priority source:** Priority #1 from the audit.

**Objective:** Leave the repo clean, intentional, reproducible, and ready for the remaining optimization goals.

**Scope:**
- Remove generated Python cache artifacts.
- Review current modified/untracked files.
- Keep only intentional product/test improvements.
- Run the full validator and Docker gates.
- End with either a clean committed state or a clearly documented intentional diff.

**Acceptance:**
- `python3 scripts/run_all_validations.py` passes.
- `docker compose config` passes.
- `docker compose build` passes.
- `docker compose run --rm validate` passes.
- `git status --short` has no accidental generated artifacts.
- Any remaining diff is committed or explicitly listed as blocked.

## /goal 15 — P0/P1 manual QA for priority pages

**Priority source:** Priority #2 from the audit.

**Objective:** Verify that the most important asset and support pages behave as real mini-tools, not just SEO pages.

**Scope:**
- BudgetReset top pages.
- AIStackCost top pages.
- MealPlanSheet and MoveBudget spot checks.
- Above-the-fold utility, copy/print/export, FAQ/schema, links, and page differentiation.

**Acceptance:**
- QA checklist exists and is completed page-by-page.
- Any missing copy/print/export or weak artifact is fixed or listed as a blocker.
- A validator covers the most important mini-tool markers where static checks are reliable.

## /goal 16 — update operator handoff

**Priority source:** Priority #3 from the audit.

**Objective:** Replace stale 49-URL handoff assumptions with the current 91-URL / Goal 13 operating state.

**Scope:**
- Update `HANDOFF_FREE_UTILITY_LAB.md`.
- Reference Goal 13 as the authoritative readiness state.
- Preserve current guardrails: no custom-domain cutover, no live ads, no thin pages.

**Acceptance:**
- Handoff reflects current counts and validation commands.
- No stale 49-URL launch instructions remain as the primary state.
- Next steps are aligned with GSC/GA4 and controlled publication.

## /goal 17 — activate external GSC/GA4 learning loop

**Priority source:** Priority #4 from the audit.

**Objective:** Convert technical readiness into market-readiness evidence through Search Console and GA4.

**Scope:**
- Prepare operator checklist for property verification, sitemap submission, URL inspection, and GA4 event confirmation.
- Define a weekly evidence log format.
- Keep credentials and private exports out of the repo.

**Acceptance:**
- External checklist is ready for the operator.
- A non-sensitive reporting template exists.
- Decisions are tied to indexation, impressions, CTR, and safe event counts.

## /goal 18 — freeze expansion until signal-driven improvements

**Priority source:** Priority #5 from the audit.

**Objective:** Prevent more thin expansion and make future assets depend on observed demand and proven utility.

**Scope:**
- Add a documented expansion freeze/approval gate.
- Tie future asset factory usage to GSC/GA4 evidence.
- Keep domain and monetization guardrails intact.

**Acceptance:**
- Expansion criteria are documented.
- Asset factory remains the only approved path for new assets.
- No new cluster/page expansion proceeds without evidence or explicit approval.
