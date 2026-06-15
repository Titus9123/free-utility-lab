#!/usr/bin/env python3
"""Validate Goal 18 expansion freeze and signal-driven growth guardrails."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

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
DOC_PATH = Path("docs/GOAL18_EXPANSION_FREEZE_2026-06-15.md")
HANDOFF_PATH = Path("HANDOFF_FREE_UTILITY_LAB.md")
RUNNER_PATH = Path("scripts/run_all_validations.py")
ASSET_FACTORY_DOC_PATH = Path("docs/ASSET_FACTORY_GOAL12.md")
GOAL17_DOC_PATH = Path("docs/GOAL17_GSC_GA4_LEARNING_LOOP_2026-06-15.md")
FINAL_READINESS_DOC_PATH = Path("docs/FINAL_LAUNCH_READINESS_GOAL13.md")

REQUIRED_DOC_PHRASES = [
    "Goal 18 expansion freeze and signal-driven improvement gate",
    "Do not add new clusters",
    "Do not add new support-page variants",
    "Do not clone existing pages manually",
    "Required evidence before expansion",
    "GSC demand signal",
    "GA4 utility signal",
    "Coverage gap discovered during QA",
    "Explicit operator approval",
    "Expansion approval checklist",
    "Improvement-first decision tree",
    "Asset factory remains the only approved path for new assets",
    "Custom-domain cutover remains approval-gated",
    "Live ads remain disabled",
    "Measurement and evidence must stay non-sensitive",
    "python3 scripts/validate_new_asset.py",
    "python3 scripts/validate_goal18_expansion_freeze.py",
]

REQUIRED_HANDOFF_PHRASES = [
    "/goal 18",
    "expansion freeze",
    "signal-driven",
    "Asset factory remains the only approved path",
    "Do not add new clusters",
    "GSC/GA4 evidence",
]

REQUIRED_CROSS_DOCS = {
    ASSET_FACTORY_DOC_PATH: [
        "Goal 12 ongoing asset factory",
        "do not clone existing pages manually",
        "python3 scripts/validate_new_asset.py",
    ],
    GOAL17_DOC_PATH: [
        "Goal 17 GSC/GA4 learning loop",
        "High copy/print/download rate",
        "Goal 18 expansion criteria",
    ],
    FINAL_READINESS_DOC_PATH: [
        "Do not add thin support pages",
        "Expand only winning clusters",
    ],
}


@dataclass(frozen=True)
class Goal18ValidationResult:
    errors: list[str]
    required_phrase_count: int

    @property
    def ok(self) -> bool:
        return not self.errors


def _read_text(site_root: Path, path: Path, errors: list[str]) -> str:
    try:
        return (site_root / path).read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {path}")
        return ""


def validate_goal18_expansion_freeze(site_root: Path | str = ROOT) -> Goal18ValidationResult:
    site_root = Path(site_root)
    errors: list[str] = []

    doc_text = _read_text(site_root, DOC_PATH, errors)
    handoff_text = _read_text(site_root, HANDOFF_PATH, errors)
    runner_text = _read_text(site_root, RUNNER_PATH, errors)

    for phrase in REQUIRED_DOC_PHRASES:
        if phrase not in doc_text:
            errors.append(f"goal18: freeze doc missing phrase `{phrase}`")

    for phrase in REQUIRED_HANDOFF_PHRASES:
        if phrase not in handoff_text:
            errors.append(f"goal18: handoff missing phrase `{phrase}`")

    if "scripts/validate_goal18_expansion_freeze.py" not in runner_text:
        errors.append("goal18: run_all_validations.py must include the Goal 18 validator")

    for path, phrases in REQUIRED_CROSS_DOCS.items():
        text = _read_text(site_root, path, errors)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"goal18: {path} missing phrase `{phrase}`")

    if (site_root / "CNAME").exists():
        errors.append("goal18: CNAME exists; custom-domain cutover remains approval-gated")

    secret_result = audit_paths(
        [
            site_root / DOC_PATH,
            site_root / HANDOFF_PATH,
            site_root / GOAL17_DOC_PATH,
            site_root / ASSET_FACTORY_DOC_PATH,
        ]
    )
    for finding in secret_result.findings:
        errors.append(f"goal18: secret-like value: {finding}")

    return Goal18ValidationResult(errors=errors, required_phrase_count=len(REQUIRED_DOC_PHRASES))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goal 18 expansion freeze guardrails.")
    parser.add_argument("site_root", nargs="?", default=".")
    args = parser.parse_args()

    result = validate_goal18_expansion_freeze(Path(args.site_root))
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"Goal 18 expansion freeze OK: {result.required_phrase_count} guardrail phrases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
