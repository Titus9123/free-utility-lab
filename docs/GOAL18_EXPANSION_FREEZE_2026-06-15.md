# Goal 18 expansion freeze and signal-driven improvement gate

Date: 2026-06-15

Purpose: prevent low-signal page growth after the optimization push. Free Utility Lab should improve and expand only from observed user/search evidence or explicit operator approval.

## Status

Goal 18 is **repo-complete / externally signal-dependent**.

The repo now has a documented expansion freeze, approval criteria, weekly evidence inputs, and validation guardrails. This does not mean new pages are permanently banned; it means new pages, clusters, or variants must be justified by GSC/GA4 evidence or an explicit operator decision before the asset factory is used.

## Freeze decision

Effective now:

- Do not add new clusters.
- Do not add new support-page variants.
- Do not clone existing pages manually.
- Do not create near-duplicate long-tail pages to chase keywords.
- Do not activate live ads as a reason to expand inventory.
- Do not cut over the custom domain as a reason to expand inventory.

Allowed work during the freeze:

- Fix bugs, broken links, schema issues, accessibility issues, and validation failures.
- Improve existing pages based on GSC/GA4 evidence.
- Strengthen above-the-fold utility, examples, worksheets, copy/print/download/export actions, and internal links on existing pages.
- Refresh titles/metas only when impressions and CTR support the change.
- Merge, canonicalize, or de-prioritize overlapping pages when evidence shows cannibalization or non-indexation.
- Prepare a new asset manifest for review without publishing it.

## Required evidence before expansion

A new asset, page cluster, or support-page variant may proceed only if at least one approved trigger is present.

Approved triggers:

1. **GSC demand signal**
   - Existing related page has meaningful impressions.
   - The query theme is clearly distinct from existing pages.
   - The current page cannot satisfy the intent with a simple title/meta or UX refresh.

2. **GA4 utility signal**
   - Existing related page has real tool-action engagement, such as copy, print, download, start, or complete events.
   - The requested expansion is a stronger worksheet/template/export path, not a thin text variant.

3. **Coverage gap discovered during QA**
   - A hub or parent tool needs a missing practical asset to complete the user journey.
   - The gap is documented with a short owner note and expected user output.

4. **Explicit operator approval**
   - The operator approves a specific new asset or cluster despite limited signals.
   - The approval note must say why it is strategic and must still use the asset factory.

Not sufficient by itself:

- Keyword volume from a tool with no GSC/GA4 support.
- A competitor page existing.
- A desire to increase page count.
- A page title variation of an already-covered intent.
- Monetization/ad inventory goals.

## Expansion approval checklist

Before publishing any new asset or page cluster, create a short non-sensitive note in the weekly evidence log or in a reviewed PR/commit message with:

- Proposed asset/cluster:
- Existing related URL(s):
- Evidence source: GSC / GA4 / QA gap / explicit operator approval
- Evidence summary: aggregate, non-sensitive only
- Why existing pages cannot be refreshed instead:
- Intended user output: worksheet / calculator / checklist / comparison / export
- Internal links/hub path:
- Measurement events to confirm after publish:
- Decision: approved / rejected / hold

If approved, the only implementation path is the Goal 12 asset factory:

```bash
python3 scripts/validate_new_asset.py path/to/new_asset.json
python3 scripts/run_all_validations.py
```

## Improvement-first decision tree

Use this order before considering expansion:

1. **No indexation**: improve uniqueness, utility, internal links, and request indexing. Do not expand the cluster.
2. **Indexed but no impressions**: hold expansion; look for a better intent or improve the existing page.
3. **Impressions but weak CTR**: refresh title/meta first.
4. **Clicks but weak tool actions**: improve above-the-fold artifact and action buttons first.
5. **Strong tool actions**: consider deeper utility or export variants only if the query theme is distinct.
6. **Overlapping pages compete for same query theme**: monitor, then merge/canonicalize if evidence persists.
7. **Clear uncovered intent with evidence**: prepare an asset factory manifest for review.

## Active guardrails

These guardrails remain active while the freeze is in place:

- Asset factory remains the only approved path for new assets.
- Custom-domain cutover remains approval-gated.
- Live ads remain disabled until organic and engagement evidence supports monetization.
- New pages must be mini-tools or practical artifacts, not thin SEO text.
- Measurement and evidence must stay non-sensitive and aggregate-only.
- No credentials, tokens, private analytics exports, user-level data, or secret-like values may be committed.

## Weekly operating cadence

Each week after Goal 17 external setup is available:

1. Fill or update `docs/organic-evidence/weekly-summary-YYYY-MM-DD.md` using the template.
2. Identify pages with indexation issues, impressions, weak CTR, or weak tool actions.
3. Choose improvement-first actions.
4. Mark any candidate expansion as `hold`, `approved`, or `rejected` using the checklist above.
5. Run validators before and after repo-owned changes.

## Validation commands

Run before and after any future expansion or signal-driven improvement:

```bash
python3 scripts/validate_goal18_expansion_freeze.py
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

Goal 18 repo work is complete when:

- This expansion freeze document exists.
- The handoff points to the freeze as the current operating rule.
- The main validation runner includes `scripts/validate_goal18_expansion_freeze.py`.
- New expansion criteria are tied to GSC/GA4 evidence, QA gaps, or explicit operator approval.
- Asset factory remains the only approved implementation path.
- Domain and monetization guardrails remain intact.
- Full local and Docker validation gates pass.

External completion remains signal-dependent until the Goal 17 GSC/GA4 loop has real evidence.
