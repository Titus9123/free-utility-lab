#!/usr/bin/env python3
"""Validate a proposed Free Utility Lab new-asset manifest."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from validate_asset_factory import validate_asset_factory
except ModuleNotFoundError:  # pragma: no cover - import path fallback for tests
    import importlib.util

    _validator_path = Path(__file__).with_name("validate_asset_factory.py")
    _spec = importlib.util.spec_from_file_location("validate_asset_factory", _validator_path)
    assert _spec is not None and _spec.loader is not None
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    validate_asset_factory = _module.validate_asset_factory


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a new Free Utility Lab asset manifest.")
    parser.add_argument("manifest", help="Path to a new-asset manifest JSON file")
    parser.add_argument("--site-root", default=".")
    args = parser.parse_args()

    result = validate_asset_factory(Path(args.site_root), manifest_path=Path(args.manifest))
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"New asset manifest OK: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
