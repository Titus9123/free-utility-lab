#!/usr/bin/env python3
"""Validate the Free Utility Lab marketplace catalog.

Goal 1 keeps the current static site behavior unchanged while adding a
central, machine-checkable catalog for assets, hubs, templates and future
marketplace pages.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from audit_no_secrets import audit_paths
except ModuleNotFoundError:  # pragma: no cover - import path fallback for tests
    import importlib.util

    _audit_path = Path(__file__).with_name("audit_no_secrets.py")
    _spec = importlib.util.spec_from_file_location("audit_no_secrets", _audit_path)
    assert _spec is not None and _spec.loader is not None
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    audit_paths = _module.audit_paths

REQUIRED_TOP_LEVEL = {"assets"}
REQUIRED_ASSET_FIELDS = {
    "id",
    "name",
    "slug",
    "category",
    "cluster",
    "public_url",
    "local_path",
    "page_type",
    "intent",
    "priority",
    "formats",
    "outputs",
    "user_types",
    "related_tools",
    "schema_types",
    "tracking_asset_id",
    "status",
}

ALLOWED_STATUSES = {"live", "planned"}
ALLOWED_PAGE_TYPES = {"tool", "calculator", "printable", "template", "checklist", "guide", "hub"}
ALLOWED_OUTPUTS = {"copy", "csv", "print", "pdf", "download", "checklist", "external_link"}
ALLOWED_FORMATS = {"calculator", "worksheet", "checklist", "template", "guide", "planner", "comparison"}


class ValidationResult:
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"missing catalog file: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, ["catalog root must be an object"]
    return data, []


def _local_path_exists(asset: dict[str, Any], site_root: Path) -> bool:
    local_path = str(asset.get("local_path", ""))
    candidate = site_root / local_path
    return candidate.exists() and candidate.is_file()


def _validate_asset(asset: Any, index: int, site_root: Path) -> list[str]:
    prefix = f"assets[{index}]"
    errors: list[str] = []
    if not isinstance(asset, dict):
        return [f"{prefix}: asset must be an object"]

    missing = sorted(REQUIRED_ASSET_FIELDS - set(asset))
    for field in missing:
        errors.append(f"{prefix}: missing required field `{field}`")
    if missing:
        return errors

    asset_id = str(asset["id"])
    if not asset_id or any(char.isspace() for char in asset_id):
        errors.append(f"{prefix}: id must be a compact slug")

    status = asset["status"]
    if status not in ALLOWED_STATUSES:
        errors.append(f"{prefix}: status must be one of {sorted(ALLOWED_STATUSES)}")

    page_type = asset["page_type"]
    if page_type not in ALLOWED_PAGE_TYPES:
        errors.append(f"{prefix}: page_type `{page_type}` is not allowed")

    priority = asset["priority"]
    if not isinstance(priority, int) or priority < 1:
        errors.append(f"{prefix}: priority must be a positive integer")

    for list_field in ["formats", "outputs", "user_types", "related_tools", "schema_types"]:
        value = asset[list_field]
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"{prefix}: {list_field} must be a non-empty list of strings")

    unknown_formats = set(asset.get("formats", [])) - ALLOWED_FORMATS
    if unknown_formats:
        errors.append(f"{prefix}: unknown formats {sorted(unknown_formats)}")

    unknown_outputs = set(asset.get("outputs", [])) - ALLOWED_OUTPUTS
    if unknown_outputs:
        errors.append(f"{prefix}: unknown outputs {sorted(unknown_outputs)}")

    public_url = str(asset["public_url"])
    if not public_url.startswith("https://titus9123.github.io/free-utility-lab/"):
        errors.append(f"{prefix}: public_url must stay on the current Free Utility Lab base until domain migration")
    if not public_url.endswith("/") and not public_url.endswith(".html"):
        errors.append(f"{prefix}: public_url should be canonical trailing-slash URL or HTML verification file")

    local_path = str(asset["local_path"])
    if local_path.startswith("/") or ".." in Path(local_path).parts:
        errors.append(f"{prefix}: local_path must be a safe relative path")
    if asset["status"] == "live" and not _local_path_exists(asset, site_root):
        errors.append(f"{prefix}: missing local_path `{local_path}` for live asset")

    if page_type == "printable" and "print" not in asset.get("outputs", []):
        errors.append(f"{prefix}: printable page must include print output")
    if page_type == "calculator" and "calculator" not in asset.get("formats", []):
        errors.append(f"{prefix}: calculator page_type must include calculator format")

    return errors


def validate_catalog(catalog_path: Path | str, site_root: Path | str = Path(".")) -> ValidationResult:
    catalog_path = Path(catalog_path)
    site_root = Path(site_root)
    errors: list[str] = []

    data, load_errors = _load_json(catalog_path)
    errors.extend(load_errors)
    if data is None:
        return ValidationResult(errors)

    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    for field in missing_top:
        errors.append(f"catalog: missing required field `{field}`")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("catalog: assets must be a non-empty list")
        return ValidationResult(errors)

    seen_ids: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    for index, asset in enumerate(assets):
        errors.extend(_validate_asset(asset, index, site_root))
        if isinstance(asset, dict):
            asset_id = str(asset.get("id", ""))
            public_url = str(asset.get("public_url", ""))
            if asset_id:
                if asset_id in seen_ids:
                    errors.append(f"assets[{index}]: duplicate id `{asset_id}` also used at assets[{seen_ids[asset_id]}]")
                seen_ids[asset_id] = index
            if public_url:
                if public_url in seen_urls:
                    errors.append(f"assets[{index}]: duplicate public_url `{public_url}` also used at assets[{seen_urls[public_url]}]")
                seen_urls[public_url] = index

    secret_result = audit_paths([catalog_path])
    for finding in secret_result.findings:
        errors.append(f"secret-like value in catalog: {finding}")

    return ValidationResult(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate data/marketplace.json")
    parser.add_argument("catalog", nargs="?", default="data/marketplace.json")
    parser.add_argument("--site-root", default=".")
    args = parser.parse_args()

    result = validate_catalog(Path(args.catalog), site_root=Path(args.site_root))
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"Catalog OK: {args.catalog}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
