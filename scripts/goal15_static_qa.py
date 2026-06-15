#!/usr/bin/env python3
"""Goal 15 static QA for priority mini-tool pages.

This script does not replace browser QA. It verifies the static markers that are
reliable for launch-readiness: artifact sections, copy/print/export actions,
FAQ/schema, internal links, tracking readiness, and differentiation among
near-duplicate BudgetReset bill-calendar pages.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUDGETRESET_TOP = [
    "free-printable-monthly-bill-calendar-pdf",
    "monthly-bill-calendar-template-free-pdf",
    "monthly-bill-calendar-free-printable",
    "monthly-bill-calendar-printable-free",
    "biweekly-paycheck-budget-template-google-sheets-free",
    "paycheck-budget-template",
    "debt-payoff-tracker",
    "zero-based-budget-template",
]

AISTACK_TOP = [
    "ai-tools-for-freelancers",
    "best-free-ai-tools-for-freelancers",
    "top-10-ai-tools-for-freelancers",
    "best-ai-tools-for-small-business",
    "chatgpt-claude-gemini-comparison",
]

MEAL_SPOT = [
    "weekly-meal-planner-printable",
    "grocery-list-template-free-editable",
]

MOVE_SPOT = [
    "moving-cost-calculator-no-email",
    "free-printable-first-apartment-budget-worksheet",
]


@dataclass(frozen=True)
class PageCheck:
    cluster: str
    slug: str
    required: tuple[str, ...]
    any_of: tuple[tuple[str, ...], ...] = ()

    @property
    def path(self) -> Path:
        return ROOT / self.cluster / self.slug / "index.html"

    @property
    def label(self) -> str:
        return f"{self.cluster}/{self.slug}"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def schema_types(html: str) -> set[str]:
    types: set[str] = set()
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            block = json.loads(raw.strip())
        except json.JSONDecodeError:
            continue
        if isinstance(block, dict):
            typ = block.get("@type")
            if isinstance(typ, str):
                types.add(typ)
    return types


def visible_text(html: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def check_page(page: PageCheck) -> list[str]:
    failures: list[str] = []
    if not page.path.exists():
        return [f"missing file: {page.path.relative_to(ROOT)}"]
    html = read(page.path)
    lower = html.lower()
    types = schema_types(html)

    for marker in page.required:
        if marker == "FAQ_SCHEMA":
            if "FAQPage" not in types:
                failures.append("missing FAQPage schema")
        elif marker == "BREADCRUMB_SCHEMA":
            if "BreadcrumbList" not in types:
                failures.append("missing BreadcrumbList schema")
        elif marker == "HOWTO_SCHEMA":
            if "HowTo" not in types:
                failures.append("missing HowTo schema")
        elif marker.lower() not in lower:
            failures.append(f"missing marker: {marker}")

    for group in page.any_of:
        if not any(marker.lower() in lower for marker in group):
            failures.append("missing one of: " + " | ".join(group))
    return failures


def build_checks() -> list[PageCheck]:
    checks: list[PageCheck] = []
    for slug in BUDGETRESET_TOP:
        checks.append(PageCheck(
            cluster="budgetreset",
            slug=slug,
            required=(
                "data-goal=\"budgetreset-support-upgrade\"",
                "data-print-section=\"budgetreset-template\"",
                "Copy template",
                "Print template",
                "Download CSV",
                "Practical example",
                "FAQ_SCHEMA",
                "BREADCRUMB_SCHEMA",
                "/free-utility-lab/budgetreset/",
                "/free-utility-lab/finance-tools/",
                "support_page_click",
            ),
            any_of=(("bill calendar", "paycheck", "debt", "zero-based"),),
        ))
    for slug in AISTACK_TOP:
        checks.append(PageCheck(
            cluster="aistackcost",
            slug=slug,
            required=(
                "data-goal=\"aistackcost-upgrade\"",
                "data-print-section=\"aistackcost-template\"",
                "Copy template",
                "Print template",
                "Download CSV",
                "Stack preset",
                "Comparison table",
                "Methodology",
                "Prices and features change",
                "FAQ_SCHEMA",
                "BREADCRUMB_SCHEMA",
                "HOWTO_SCHEMA",
                "/free-utility-lab/ai-tools/",
                "/free-utility-lab/aistackcost/",
            ),
        ))
    for slug in MEAL_SPOT:
        checks.append(PageCheck(
            cluster="mealplansheet",
            slug=slug,
            required=(
                "data-print-section",
                "Copy",
                "Print",
                "FAQ_SCHEMA",
                "/free-utility-lab/mealplansheet/",
            ),
            any_of=(("Download", "CSV"),),
        ))
    for slug in MOVE_SPOT:
        checks.append(PageCheck(
            cluster="movebudget",
            slug=slug,
            required=(
                "data-goal=\"movebudget-upgrade\"",
                "data-print-section=\"movebudget-template\"",
                "Copy template",
                "Print template",
                "FAQ_SCHEMA",
                "BREADCRUMB_SCHEMA",
                "/free-utility-lab/movebudget/",
            ),
        ))
    return checks


def check_budgetreset_differentiation() -> list[str]:
    failures: list[str] = []
    texts: dict[str, str] = {}
    for slug in BUDGETRESET_TOP[:4]:
        html = read(ROOT / "budgetreset" / slug / "index.html")
        texts[slug] = visible_text(html)
    slugs = list(texts)
    for i, left in enumerate(slugs):
        left_words = set(texts[left].split())
        for right in slugs[i + 1:]:
            right_words = set(texts[right].split())
            union = left_words | right_words
            similarity = len(left_words & right_words) / max(1, len(union))
            if similarity > 0.72:
                failures.append(f"bill-calendar pages too similar: {left} vs {right} ({similarity:.2f})")
    return failures


def main() -> int:
    all_failures: list[str] = []
    for page in build_checks():
        failures = check_page(page)
        if failures:
            all_failures.extend(f"{page.label}: {failure}" for failure in failures)

    for failure in check_budgetreset_differentiation():
        all_failures.append("budgetreset differentiation: " + failure)

    if all_failures:
        print("Goal 15 static QA failed:")
        for failure in all_failures:
            print("- " + failure)
        return 1

    print("Goal 15 static QA OK: priority pages have mini-tool markers and bill-calendar pages are differentiated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
