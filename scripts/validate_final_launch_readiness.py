#!/usr/bin/env python3
"""Validate Goal 13 final launch readiness and operator handoff."""

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
CONTRACT_PATH = Path("data/final_launch_readiness.json")
DOC_PATH = Path("docs/FINAL_LAUNCH_READINESS_GOAL13.md")
RUNNER_PATH = Path("scripts/run_all_validations.py")
CURRENT_BASE = "https://titus9123.github.io/free-utility-lab/"
TARGET_DOMAIN = "freeutilitylab.com"

REQUIRED_DOC_PHRASES = [
    "Goal 13 final launch readiness",
    "operator handoff",
    "no cutover was performed",
    "quality gates",
    "domain migration remains approval-gated",
    "asset factory remains the expansion path",
    "measurement loop",
    "CI gates",
    "Docker validation",
    "post-launch operating cadence",
    "do not activate live ads yet",
    "python3 scripts/validate_final_launch_readiness.py",
]

REQUIRED_FILES = {
    "README.md",
    "sitemap.xml",
    "docker-compose.yml",
    ".github/workflows/validate-free-utility-lab.yml",
    "data/marketplace.json",
    "data/domain_migration.json",
    "data/asset_factory_checklist.json",
    "docs/DOMAIN_MIGRATION_GOAL11.md",
    "docs/ASSET_FACTORY_GOAL12.md",
    "docs/FINAL_LAUNCH_READINESS_GOAL13.md",
    "templates/new_asset_manifest.template.json",
    "scripts/run_all_validations.py",
    "scripts/validate_domain_migration.py",
    "scripts/validate_asset_factory.py",
    "scripts/validate_final_launch_readiness.py",
}

REQUIRED_GATES = {
    "python3 -m pytest -q",
    "python3 scripts/validate_marketplace_catalog.py",
    "python3 scripts/validate_shared_modules.py",
    "python3 scripts/validate_site_links.py . --base-path /free-utility-lab/",
    "python3 scripts/validate_sitemap.py sitemap.xml --site-root .",
    "python3 scripts/validate_schema_smoke.py",
    "python3 scripts/validate_domain_migration.py",
    "python3 scripts/validate_asset_factory.py",
    "python3 scripts/validate_final_launch_readiness.py",
}

REQUIRED_BLOCKERS = {
    "domain_migration_approval_required",
    "live_ads_not_activated",
}


@dataclass(frozen=True)
class FinalLaunchReadinessResult:
    errors: list[str]
    completed_goal_count: int
    required_gate_count: int
    current_base: str
    target_domain: str
    cutover_performed: bool
    live_ads_enabled: bool
    blockers: tuple[str, ...]
    required_files: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_json(path: Path) -> tuple[dict[str, Any], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, [f"missing file: {path}"]
    except json.JSONDecodeError as exc:
        return {}, [f"invalid JSON in {path}: {exc}"]
    if not isinstance(data, dict):
        return {}, [f"{path} root must be an object"]
    return data, []


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def validate_final_launch_readiness(site_root: Path | str = ROOT) -> FinalLaunchReadinessResult:
    site_root = Path(site_root)
    errors: list[str] = []

    contract, load_errors = _load_json(site_root / CONTRACT_PATH)
    errors.extend(load_errors)

    completed_goals = _as_string_list(contract.get("completed_goals"))
    required_gates = _as_string_list(contract.get("required_gates"))
    required_files = _as_string_list(contract.get("required_files"))
    blockers = _as_string_list(contract.get("blockers"))
    current_base = str(contract.get("current_base", ""))
    target_domain = str(contract.get("target_domain", ""))
    cutover_performed = bool(contract.get("cutover_performed", False))
    live_ads_enabled = bool(contract.get("live_ads_enabled", False))

    if contract.get("goal") != "Goal 13 final launch readiness":
        errors.append("final_launch_readiness: goal must be `Goal 13 final launch readiness`")
    if contract.get("status") != "operator_handoff_ready":
        errors.append("final_launch_readiness: status must be `operator_handoff_ready`")
    if current_base != CURRENT_BASE:
        errors.append(f"final_launch_readiness: current_base must be {CURRENT_BASE}")
    if target_domain != TARGET_DOMAIN:
        errors.append(f"final_launch_readiness: target_domain must be {TARGET_DOMAIN}")
    if cutover_performed:
        errors.append("final_launch_readiness: cutover_performed must remain false")
    if live_ads_enabled:
        errors.append("final_launch_readiness: live_ads_enabled must remain false")
    if (site_root / "CNAME").exists():
        errors.append("final_launch_readiness: CNAME exists; custom-domain cutover was not approved")

    missing_goals = [f"goal_{index}" for index in range(13) if not any(goal.startswith(f"goal_{index}_") for goal in completed_goals)]
    for goal in missing_goals:
        errors.append(f"final_launch_readiness: missing completed goal marker `{goal}`")

    missing_gates = sorted(REQUIRED_GATES - set(required_gates))
    for gate in missing_gates:
        errors.append(f"final_launch_readiness: missing required gate `{gate}`")

    missing_file_entries = sorted(REQUIRED_FILES - set(required_files))
    for file_entry in missing_file_entries:
        errors.append(f"final_launch_readiness: missing required file entry `{file_entry}`")
    for file_entry in required_files:
        if not (site_root / file_entry).exists():
            errors.append(f"final_launch_readiness: required file missing on disk `{file_entry}`")

    missing_blockers = sorted(REQUIRED_BLOCKERS - set(blockers))
    for blocker in missing_blockers:
        errors.append(f"final_launch_readiness: missing blocker `{blocker}`")

    try:
        doc_text = (site_root / DOC_PATH).read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {site_root / DOC_PATH}")
        doc_text = ""
    for phrase in REQUIRED_DOC_PHRASES:
        if phrase not in doc_text:
            errors.append(f"final_launch_readiness: doc missing phrase `{phrase}`")

    try:
        runner_text = (site_root / RUNNER_PATH).read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {site_root / RUNNER_PATH}")
        runner_text = ""
    if "scripts/validate_final_launch_readiness.py" not in runner_text:
        errors.append("final_launch_readiness: run_all_validations.py must include the Goal 13 validator")

    secret_result = audit_paths([site_root / CONTRACT_PATH, site_root / DOC_PATH])
    for finding in secret_result.findings:
        errors.append(f"final_launch_readiness: secret-like value: {finding}")

    return FinalLaunchReadinessResult(
        errors=errors,
        completed_goal_count=len(completed_goals),
        required_gate_count=len(required_gates),
        current_base=current_base,
        target_domain=target_domain,
        cutover_performed=cutover_performed,
        live_ads_enabled=live_ads_enabled,
        blockers=tuple(blockers),
        required_files=tuple(required_files),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goal 13 final launch readiness and operator handoff.")
    parser.add_argument("site_root", nargs="?", default=".")
    args = parser.parse_args()

    result = validate_final_launch_readiness(Path(args.site_root))
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(
        "Final launch readiness OK: "
        f"{result.completed_goal_count} goal markers, {result.required_gate_count} gates, "
        f"current base {result.current_base}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
