import json
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://titus9123.github.io/free-utility-lab/"
GOAL3_PAGES = [
    "tools/index.html",
    "printable-templates/index.html",
    "finance-tools/index.html",
    "meal-planning-tools/index.html",
    "moving-tools/index.html",
    "ai-tools/index.html",
]
GA4_MEASUREMENT_ID = "G-54GQ1ZT341"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def page_url(path: str) -> str:
    return BASE_URL + path.removesuffix("index.html")


def test_goal3_marketplace_pages_exist_and_use_shared_modules():
    for page in GOAL3_PAGES:
        html_path = ROOT / page
        assert html_path.exists(), f"missing {page}"
        html = html_path.read_text(encoding="utf-8")
        assert "shared/styles/marketplace.css" in html
        assert "shared/styles/print.css" in html
        assert "shared/scripts/utility-actions.js" in html
        assert "FreeUtilityLabComponents" in html
        assert "data-page-type=\"marketplace-hub\"" in html
        assert "ful-tool-card" in html
        assert "No signup" in html
        assert "BreadcrumbList" in html
        assert "ItemList" in html


def test_goal3_marketplace_hubs_load_the_shared_measurement_stack():
    """Generated hubs must not become invisible in GA4."""
    for page in GOAL3_PAGES:
        html = read(page)
        assert f"googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}" in html, page
        assert f"gtag('config', '{GA4_MEASUREMENT_ID}')" in html, page
        assert "../free-utility-lab-tracking.js" in html, page
        assert "../free-utility-lab-measurement-bridge.js" in html, page
        assert html.index("free-utility-lab-tracking.js") < html.index("free-utility-lab-measurement-bridge.js"), page


def test_marketplace_renderer_owns_hub_measurement_markup():
    renderer = read("scripts/render_marketplace_pages.py")
    assert "googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}" in renderer
    assert "../free-utility-lab-tracking.js" in renderer
    assert "../free-utility-lab-measurement-bridge.js" in renderer


def test_all_tools_hub_lists_every_live_tool_and_category_hub():
    html = read("tools/index.html")
    for slug in ["budgetreset/", "mealplansheet/", "movebudget/", "aistackcost/"]:
        assert f'href="/free-utility-lab/{slug}"' in html
    for hub in ["finance-tools/", "meal-planning-tools/", "moving-tools/", "ai-tools/", "printable-templates/"]:
        assert f'href="/free-utility-lab/{hub}"' in html
    assert "data-filter-control" in html
    assert "related_tool_click" in html


def test_category_hubs_only_include_relevant_live_tool_cards():
    expectations = {
        "finance-tools/index.html": ["budgetreset"],
        "meal-planning-tools/index.html": ["mealplansheet"],
        "moving-tools/index.html": ["movebudget"],
        "ai-tools/index.html": ["aistackcost"],
    }
    excluded = {"budgetreset", "mealplansheet", "movebudget", "aistackcost"}
    for page, included_ids in expectations.items():
        html = read(page)
        for asset_id in included_ids:
            assert f'data-asset-id="{asset_id}"' in html
        for asset_id in excluded - set(included_ids):
            assert f'data-asset-id="{asset_id}"' not in html


def test_printable_templates_hub_includes_printable_assets_only():
    html = read("printable-templates/index.html")
    for asset_id in ["budgetreset", "mealplansheet", "movebudget"]:
        assert f'data-asset-id="{asset_id}"' in html
    assert 'data-asset-id="aistackcost"' not in html
    assert "Printable templates" in html
    assert "Print" in html


def test_goal3_pages_have_canonicals_titles_meta_and_schema_json():
    for page in GOAL3_PAGES:
        html = read(page)
        canonical = page_url(page)
        assert f'<link rel="canonical" href="{canonical}">' in html
        assert "<title>" in html and "Free Utility Lab" in html
        assert '<meta name="description"' in html
        schema_blocks = []
        marker = '<script type="application/ld+json">'
        remaining = html
        while marker in remaining:
            before, after = remaining.split(marker, 1)
            raw, remaining = after.split("</script>", 1)
            schema_blocks.append(json.loads(raw.strip()))
        schema_types = {block.get("@type") for block in schema_blocks}
        assert "BreadcrumbList" in schema_types
        assert "ItemList" in schema_types


def test_goal3_pages_are_in_sitemap():
    sitemap = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {loc.text for loc in sitemap.findall(".//sm:loc", ns)}
    for page in GOAL3_PAGES:
        assert page_url(page) in locs


def test_marketplace_catalog_marks_goal3_hubs_live():
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    by_id = {asset["id"]: asset for asset in catalog["assets"]}
    assert by_id["all-tools-hub"]["status"] == "live"
    assert by_id["printable-templates-hub"]["status"] == "live"
    for local_path in ["tools/index.html", "printable-templates/index.html"]:
        assert (ROOT / local_path).exists()

    categories = json.loads((ROOT / "data" / "categories.json").read_text(encoding="utf-8"))
    live_hubs = {category["slug"] for category in categories["categories"] if category["status"] == "live"}
    assert {"tools", "printable-templates", "finance-tools", "meal-planning-tools", "moving-tools", "ai-tools"} <= live_hubs
