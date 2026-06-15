# Free Utility Lab

Free practical web tools, calculators, planners, checklists and generators.

Public site target: https://titus9123.github.io/free-utility-lab/

This repo is intentionally neutral and brand-independent.

## Quality gates

Local validation before publishing:

```bash
python3 scripts/run_all_validations.py
docker compose config >/tmp/free-utility-lab-compose-config.out
docker compose build
```

## New asset factory

Goal 12 adds a repeatable workflow for creating new assets without manual page cloning:

```bash
python3 scripts/validate_new_asset.py path/to/new_asset.json
python3 scripts/run_all_validations.py
```

Use `docs/ASSET_FACTORY_GOAL12.md`, `docs/GOAL18_EXPANSION_FREEZE_2026-06-15.md`, `data/asset_factory_checklist.json`, and `templates/new_asset_manifest.template.json` before publishing a new tool, template, checklist or calculator.

Goal 18 freezes new clusters and support-page variants until there is GSC/GA4 evidence, a documented QA coverage gap, or explicit operator approval. Even when approved, the Goal 12 asset factory remains the only implementation path.

## Final launch readiness

Goal 13 adds a final operator handoff and readiness guardrail:

```bash
python3 scripts/validate_final_launch_readiness.py
python3 scripts/run_all_validations.py
```

Use `docs/FINAL_LAUNCH_READINESS_GOAL13.md` and `data/final_launch_readiness.json` before future launches. The custom-domain cutover and live ads remain approval-gated.

CI uses `.github/workflows/validate-free-utility-lab.yml` to run the same credential-free quality gates on pushes to `main` and pull requests: Python tests, the validation bundle, HTML page count reporting, Docker Compose config validation, and Docker image build.
