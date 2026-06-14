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

Use `docs/ASSET_FACTORY_GOAL12.md`, `data/asset_factory_checklist.json`, and `templates/new_asset_manifest.template.json` before publishing a new tool, template, checklist or calculator.

CI uses `.github/workflows/validate-free-utility-lab.yml` to run the same credential-free quality gates on pushes to `main` and pull requests: Python tests, the validation bundle, HTML page count reporting, Docker Compose config validation, and Docker image build.
