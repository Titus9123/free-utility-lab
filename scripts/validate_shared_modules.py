#!/usr/bin/env python3
"""Validate shared modules and approved marketplace wiring boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / "shared" / "components" / "marketplace-components.js",
    ROOT / "shared" / "scripts" / "utility-actions.js",
    ROOT / "shared" / "styles" / "marketplace.css",
    ROOT / "shared" / "styles" / "print.css",
    ROOT / "docs" / "SHARED_MODULES_GOAL2.md",
]
GOAL3_MARKETPLACE_PAGES = {
    ROOT / "tools" / "index.html",
    ROOT / "printable-templates" / "index.html",
    ROOT / "finance-tools" / "index.html",
    ROOT / "meal-planning-tools" / "index.html",
    ROOT / "moving-tools" / "index.html",
    ROOT / "ai-tools" / "index.html",
}
GOAL4_UPGRADED_TOOL_PAGES = {
    ROOT / "budgetreset" / "index.html",
}
GOAL5_UPGRADED_TOOL_PAGES = {
    ROOT / "mealplansheet" / "index.html",
    ROOT / "mealplansheet" / "grocery-list-template-free-editable" / "index.html",
    ROOT / "mealplansheet" / "weekly-meal-planner-printable" / "index.html",
    ROOT / "mealplansheet" / "grocery-list-template" / "index.html",
    ROOT / "mealplansheet" / "printable-grocery-list-by-category" / "index.html",
    ROOT / "mealplansheet" / "family-grocery-budget-planner" / "index.html",
    ROOT / "mealplansheet" / "cheap-weekly-meal-plan" / "index.html",
    ROOT / "mealplansheet" / "student-meal-planner" / "index.html",
    ROOT / "mealplansheet" / "no-cook-meal-plan" / "index.html",
}
APPROVED_SHARED_MODULE_PAGES = (
    GOAL3_MARKETPLACE_PAGES | GOAL4_UPGRADED_TOOL_PAGES | GOAL5_UPGRADED_TOOL_PAGES
)
SHARED_MARKERS = [
    "shared/scripts/utility-actions.js",
    "shared/styles/marketplace.css",
]


def validate_shared_modules(site_root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required shared module file: {path.relative_to(site_root)}")

    for html_path in site_root.rglob("*.html"):
        if any(part in {".git", ".pytest_cache"} for part in html_path.parts):
            continue
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        has_shared_marker = any(marker in text for marker in SHARED_MARKERS)
        if html_path in APPROVED_SHARED_MODULE_PAGES:
            if not has_shared_marker:
                errors.append(f"missing approved shared module wiring: {html_path.relative_to(site_root)}")
            continue
        if has_shared_marker:
            errors.append(f"unexpected shared module wiring outside approved pages: {html_path.relative_to(site_root)}")
    return errors


def main() -> int:
    errors = validate_shared_modules(ROOT)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Shared modules OK: Goal 2 files present and approved Goal 3/4 wiring is scoped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
