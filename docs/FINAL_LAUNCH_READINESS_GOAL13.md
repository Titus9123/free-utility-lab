# Goal 13 final launch readiness

Goal 13 is the final operator handoff for Free Utility Lab after the modular catalog, shared components, marketplace pages, priority cluster upgrades, Docker/CI gates, measurement loop, domain-migration readiness, and asset factory are in place.

This goal records the site as ready for controlled operation and future launches, but **no cutover was performed**.

## Final state

- Current public base: `https://titus9123.github.io/free-utility-lab/`
- Target custom domain: `freeutilitylab.com`
- Custom-domain cutover: not performed
- Live ads: not activated
- Expansion path: controlled by the Goal 12 asset factory
- Measurement path: controlled by the Goal 10 measurement loop

## Operator handoff

Use this handoff before publishing future changes:

1. Run the quality gates.
2. Confirm domain migration remains approval-gated.
3. Confirm the asset factory remains the expansion path.
4. Review the measurement loop before adding more pages or tools.
5. Keep CI gates and Docker validation green.
6. Review the diff for secrets, accidental domain cutover, live-ad activation, and thin-page expansion.
7. Publish only after validations pass and the operator approves the scope.

## Quality gates

Run:

```bash
python3 scripts/validate_final_launch_readiness.py
python3 scripts/run_all_validations.py
docker compose config
docker compose build
docker compose run --rm validate
```

The launch-readiness validator checks that the final handoff contract exists, required prior-goal artifacts are still present, no custom-domain `CNAME` exists, the current GitHub Pages base remains unchanged, live ads are not activated, and the final readiness validator is included in the full validation bundle.

## Guardrails that stay active

- Domain migration remains approval-gated.
- Do not create `CNAME` without explicit final approval.
- Do not rewrite canonicals, Open Graph URLs, or sitemap URLs to `freeutilitylab.com` until the cutover is approved.
- Do not activate live ads yet; wait for organic and engagement evidence.
- Do not add thin support pages.
- Do not clone existing pages manually; use the asset factory manifest and validators.
- Do not introduce secrets, credentials, tokens, private keys, passwords, or private analytics exports.

## Asset factory remains the expansion path

Every new asset should use:

```bash
python3 scripts/validate_new_asset.py path/to/new_asset.json
python3 scripts/run_all_validations.py
```

Before a new asset is accepted, it must have a catalog entry, main product page, category hub inclusion, real tool/template/checklist/calculator value, copy/print/export outputs, schema, tracking, internal links, validation pass, no secrets, and no thin support pages.

## Measurement loop

Use the existing measurement loop before making expansion decisions:

- Review GSC indexation and impressions.
- Identify pages in positions 8-30.
- Improve titles/metas only where impressions justify it.
- Improve UX where clicks exist but tool engagement is weak.
- Merge, canonicalize, or avoid expanding pages that show persistent cannibalization or no indexation.
- Expand only winning clusters.

## CI gates and Docker validation

CI gates should stay aligned with `scripts/run_all_validations.py`. Docker validation should remain a local parity check for the static site and validation service.

## post-launch operating cadence

Recommended cadence:

- Weekly: run the full validation bundle, review GSC/GA4 signals, and inspect top movement by cluster.
- Before each new asset: validate the new asset manifest and confirm internal links/category hub placement.
- Before any domain work: rerun `python3 scripts/validate_domain_migration.py` and request explicit cutover approval.
- Before monetization: confirm organic sessions, engagement, user value, policy fit, and page quality; do not activate live ads yet.

## Final acceptance

Goal 13 is complete when:

- `data/final_launch_readiness.json` records final handoff status.
- `scripts/validate_final_launch_readiness.py` verifies prior gates and guardrails.
- `scripts/run_all_validations.py` includes the Goal 13 validator.
- Local tests, validators, no-secret audit, Docker config/build, and Docker validate pass.
- The repo is clean after commit.
