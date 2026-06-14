#!/usr/bin/env python3
"""Validate the Goal 12 repeatable new-asset factory contract."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
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

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST_PATH = Path("data/asset_factory_checklist.json")
DOC_PATH = Path("docs/ASSET_FACTORY_GOAL12.md")
TEMPLATE_PATH = Path("templates/new_asset_manifest.template.json")

REQUIRED_CHECK_IDS = {
    "catalog_entry",
    "main_product_page",
    "category_hub_inclusion",
    "usable_asset",
    "outputs",
    "schema",
    "tracking",
    "internal_links",
    "validation_pass",
    "no_secrets",
    "no_thin_support_pages",
}

REQUIRED_DOC_PHRASES = [
    "Goal 12 ongoing asset factory",
    "repeatable workflow",
    "do not clone existing pages manually",
    "catalog entry",
    "main product page",
    "category hub inclusion",
    "real tool/template/checklist/calculator",
    "copy/print/export outputs",
    "schema",
    "tracking",
    "internal links",
    "validation pass",
    "no secrets",
    "no thin support pages",
    "python3 scripts/validate_new_asset.py",
]


@dataclass(frozen=True)
class AssetFactoryValidationResult:
    errors: list[str]
    check_ids: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def check_count(self) -> int:
        return len(self.check_ids)


def _load_json(path: Path) -> tuple[Any | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [f"missing file: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON in {path}: {exc}"]


def _validate_manifest(manifest_path: Path, required_fields: set[str]) -> list[str]:
    data, errors = _load_json(manifest_path)
    if errors:
        return [f"new_asset: {error}" for error in errors]
    if not isinstance(data, dict):
        return ["new_asset: manifest root must be an object"]

    manifest_errors: list[str] = []
    missing = sorted(required_fields - set(data))
    for field in missing:
        manifest_errors.append(f"new_asset: missing required field `{field}`")
    if missing:
        return manifest_errors

    for field in ["formats", "outputs", "schema_types", "related_tools", "validation_commands"]:
        value = data.get(field)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            manifest_errors.append(f"new_asset: `{field}` must be a non-empty list of strings")

    supporting_pages = data.get("supporting_pages")
    if not isinstance(supporting_pages, list):
        manifest_errors.append("new_asset: `supporting_pages` must be a list")
    else:
        for index, page in enumerate(supporting_pages):
            if not isinstance(page, dict) or not page.get("path") or not page.get("purpose"):
                manifest_errors.append(f"new_asset: supporting_pages[{index}] needs path and purpose")

    if not ({"copy", "print", "csv", "download", "pdf", "checklist"} & set(data.get("outputs", []))):
        manifest_errors.append("new_asset: outputs must include copy, print, csv, download, pdf or checklist")
    if "BreadcrumbList" not in set(data.get("schema_types", [])):
        manifest_errors.append("new_asset: schema_types must include BreadcrumbList")
    if str(data.get("tracking_asset_id", "")) != str(data.get("id", "")):
        manifest_errors.append("new_asset: tracking_asset_id should match id for a new primary asset")

    secret_result = audit_paths([manifest_path])
    for finding in secret_result.findings:
        manifest_errors.append(f"new_asset: secret-like value: {finding}")

    return manifest_errors


def validate_asset_factory(site_root: Path | str = ROOT, manifest_path: Path | str | None = None) -> AssetFactoryValidationResult:
    site_root = Path(site_root)
    errors: list[str] = []

    checklist_file = site_root / CHECKLIST_PATH
    checklist, load_errors = _load_json(checklist_file)
    errors.extend(load_errors)
    check_ids: tuple[str, ...] = ()
    required_manifest_fields: set[str] = set()

    if isinstance(checklist, dict):
        checks = checklist.get("checks")
        if not isinstance(checks, list) or not checks:
            errors.append("asset_factory: checks must be a non-empty list")
        else:
            ids: list[str] = []
            for index, check in enumerate(checks):
                if not isinstance(check, dict):
                    errors.append(f"asset_factory: checks[{index}] must be an object")
                    continue
                check_id = check.get("id")
                if not isinstance(check_id, str) or not check_id:
                    errors.append(f"asset_factory: checks[{index}] needs id")
                    continue
                ids.append(check_id)
                for field in ["label", "description"]:
                    if not isinstance(check.get(field), str) or not check[field].strip():
                        errors.append(f"asset_factory: check `{check_id}` needs {field}")
            check_ids = tuple(ids)
            missing_ids = sorted(REQUIRED_CHECK_IDS - set(ids))
            for check_id in missing_ids:
                errors.append(f"asset_factory: missing required check `{check_id}`")

        raw_required_fields = checklist.get("required_manifest_fields", [])
        if not isinstance(raw_required_fields, list) or not raw_required_fields:
            errors.append("asset_factory: required_manifest_fields must be a non-empty list")
        else:
            required_manifest_fields = {str(field) for field in raw_required_fields if isinstance(field, str) and field}

        for field in ["workflow_doc", "manifest_template", "validator"]:
            value = checklist.get(field)
            if not isinstance(value, str) or not value:
                errors.append(f"asset_factory: missing `{field}` path")
            elif not (site_root / value).exists():
                errors.append(f"asset_factory: referenced `{field}` does not exist: {value}")
    elif checklist is not None:
        errors.append("asset_factory: checklist root must be an object")

    doc_file = site_root / DOC_PATH
    try:
        doc_text = doc_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {doc_file}")
        doc_text = ""
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase not in doc_text:
            errors.append(f"asset_factory: doc missing phrase `{phrase}`")

    template_file = site_root / TEMPLATE_PATH
    template_errors = _validate_manifest(template_file, required_manifest_fields or set())
    errors.extend(error.replace("new_asset:", "template:", 1) for error in template_errors)

    if manifest_path is not None:
        errors.extend(_validate_manifest(Path(manifest_path), required_manifest_fields))

    secret_result = audit_paths([checklist_file, doc_file, template_file])
    for finding in secret_result.findings:
        errors.append(f"asset_factory: secret-like value: {finding}")

    return AssetFactoryValidationResult(errors=errors, check_ids=check_ids)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goal 12 asset factory readiness.")
    parser.add_argument("--site-root", default=".")
    parser.add_argument("--manifest", help="Optional proposed new-asset manifest to validate")
    args = parser.parse_args()

    result = validate_asset_factory(Path(args.site_root), manifest_path=Path(args.manifest) if args.manifest else None)
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"Asset factory OK: {result.check_count} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
