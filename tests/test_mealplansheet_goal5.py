import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEALPLANSHEET = ROOT / "mealplansheet" / "index.html"
PRIORITY_SLUGS = [
    "grocery-list-template-free-editable",
    "weekly-meal-planner-printable",
    "grocery-list-template",
    "printable-grocery-list-by-category",
    "family-grocery-budget-planner",
    "cheap-weekly-meal-plan",
    "student-meal-planner",
    "no-cook-meal-plan",
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


def test_mealplansheet_goal5_main_page_has_real_exportable_templates_above_fold():
    html = read(MEALPLANSHEET)
    assert "/free-utility-lab/shared/styles/marketplace.css" in html
    assert "/free-utility-lab/shared/styles/print.css" in html
    assert "/free-utility-lab/shared/scripts/utility-actions.js" in html
    assert "FreeUtilityLabActions" in html
    assert 'data-goal="mealplansheet-upgrade"' in html
    assert 'data-print-section="mealplansheet-result"' in html
    for label in [
        "Editable grocery list by category",
        "Weekly meal planner printable",
        "Grocery budget worksheet",
        "Student preset",
        "Family preset",
        "Cheap week preset",
        "No-cook preset",
        "Copy meal plan summary",
        "Download grocery CSV",
        "Print weekly planner",
    ]:
        assert label in html


def test_mealplansheet_goal5_priority_pages_have_direct_artifacts_and_actions():
    for slug in PRIORITY_SLUGS:
        html = read(ROOT / "mealplansheet" / slug / "index.html")
        assert 'data-goal="mealplansheet-upgrade"' in html, slug
        assert 'data-print-section="mealplansheet-template"' in html, slug
        assert "Copy template" in html, slug
        assert "Print template" in html, slug
        assert "Download CSV" in html, slug
        assert "Example week" in html, slug
        assert "Practical FAQ" in html, slug
        assert "/free-utility-lab/meal-planning-tools/" in html, slug
        assert "/free-utility-lab/tools/" in html, slug
        assert "/free-utility-lab/printable-templates/" in html, slug


def test_mealplansheet_goal5_schema_has_breadcrumb_howto_and_faq():
    blocks = schema_blocks(read(MEALPLANSHEET))
    types = {block.get("@type") for block in blocks}
    assert "BreadcrumbList" in types
    assert "HowTo" in types
    assert "FAQPage" in types
    howto = next(block for block in blocks if block.get("@type") == "HowTo")
    assert "meal plan" in howto["name"].lower()
    assert len(howto.get("step", [])) >= 3
    assert all("text" in step for step in howto["step"])


def test_mealplansheet_goal5_links_to_marketplace_hubs_and_priority_support_pages():
    html = read(MEALPLANSHEET)
    for href in [
        "/free-utility-lab/tools/",
        "/free-utility-lab/meal-planning-tools/",
        "/free-utility-lab/printable-templates/",
        "/free-utility-lab/mealplansheet/grocery-list-template-free-editable/",
        "/free-utility-lab/mealplansheet/weekly-meal-planner-printable/",
        "/free-utility-lab/mealplansheet/grocery-list-template/",
        "/free-utility-lab/mealplansheet/printable-grocery-list-by-category/",
        "/free-utility-lab/mealplansheet/family-grocery-budget-planner/",
        "/free-utility-lab/mealplansheet/cheap-weekly-meal-plan/",
        "/free-utility-lab/mealplansheet/student-meal-planner/",
        "/free-utility-lab/mealplansheet/no-cook-meal-plan/",
    ]:
        assert f'href="{href}"' in html


def test_mealplansheet_catalog_records_goal5_upgrade_metadata():
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    mealplansheet = next(asset for asset in catalog["assets"] if asset["id"] == "mealplansheet")
    assert mealplansheet["status"] == "live"
    assert "copy" in mealplansheet["outputs"]
    assert "csv" in mealplansheet["outputs"]
    assert "print" in mealplansheet["outputs"]
    assert "HowTo" in mealplansheet["schema_types"]
    assert mealplansheet.get("goal5_upgrade") == "mealplansheet-templates-export-print-copy-internal-links"
