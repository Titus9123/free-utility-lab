import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOVEBUDGET = ROOT / "movebudget" / "index.html"
PRIORITY_SLUGS = [
    "moving-cost-calculator-no-email",
    "free-printable-first-apartment-budget-worksheet",
    "moving-cost-checklist",
    "moving-box-calculator",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def schema_blocks(html: str):
    marker = '<script type="application/ld+json">'
    remaining = html
    blocks = []
    while marker in remaining:
        _, after = remaining.split(marker, 1)
        raw, remaining = after.split("</script>", 1)
        blocks.append(json.loads(raw.strip()))
    return blocks


def test_movebudget_goal6_main_page_has_calculators_and_exports_above_fold():
    html = read(MOVEBUDGET)
    assert "/free-utility-lab/shared/styles/marketplace.css" in html
    assert "/free-utility-lab/shared/styles/print.css" in html
    assert "/free-utility-lab/shared/scripts/utility-actions.js" in html
    assert "FreeUtilityLabActions" in html
    assert 'data-goal="movebudget-upgrade"' in html
    assert 'data-print-section="movebudget-result"' in html
    for label in [
        "Moving cost calculator",
        "First apartment budget worksheet",
        "Moving cost checklist",
        "Box calculator",
        "Starter apartment example",
        "Family move example",
        "Copy moving budget summary",
        "Download moving budget CSV",
        "Print moving budget",
    ]:
        assert label in html


def test_movebudget_goal6_priority_pages_have_direct_artifacts_and_actions():
    for slug in PRIORITY_SLUGS:
        html = read(ROOT / "movebudget" / slug / "index.html")
        assert 'data-goal="movebudget-upgrade"' in html, slug
        assert 'data-print-section="movebudget-template"' in html, slug
        assert "Copy template" in html, slug
        assert "Print template" in html, slug
        assert "Download CSV" in html, slug
        assert "Realistic moving example" in html, slug
        assert "Practical FAQ" in html, slug
        assert "/free-utility-lab/moving-tools/" in html, slug
        assert "/free-utility-lab/tools/" in html, slug
        assert "/free-utility-lab/printable-templates/" in html, slug


def test_movebudget_goal6_schema_has_breadcrumb_howto_and_faq():
    blocks = schema_blocks(read(MOVEBUDGET))
    types = {block.get("@type") for block in blocks}
    assert "BreadcrumbList" in types
    assert "HowTo" in types
    assert "FAQPage" in types
    howto = next(block for block in blocks if block.get("@type") == "HowTo")
    assert "moving budget" in howto["name"].lower()
    assert len(howto.get("step", [])) >= 3
    assert all("text" in step for step in howto["step"])


def test_movebudget_goal6_links_to_marketplace_hubs_and_priority_support_pages():
    html = read(MOVEBUDGET)
    for href in [
        "/free-utility-lab/tools/",
        "/free-utility-lab/moving-tools/",
        "/free-utility-lab/printable-templates/",
        "/free-utility-lab/movebudget/moving-cost-calculator-no-email/",
        "/free-utility-lab/movebudget/free-printable-first-apartment-budget-worksheet/",
        "/free-utility-lab/movebudget/moving-cost-checklist/",
        "/free-utility-lab/movebudget/moving-box-calculator/",
    ]:
        assert f'href="{href}"' in html


def test_movebudget_catalog_records_goal6_upgrade_metadata():
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    movebudget = next(asset for asset in catalog["assets"] if asset["id"] == "movebudget")
    assert movebudget["status"] == "live"
    assert "copy" in movebudget["outputs"]
    assert "csv" in movebudget["outputs"]
    assert "print" in movebudget["outputs"]
    assert "HowTo" in movebudget["schema_types"]
    assert movebudget.get("goal6_upgrade") == "movebudget-calculators-checklists-export-print-copy-internal-links"
