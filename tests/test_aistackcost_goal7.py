import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AISTACK = ROOT / "aistackcost" / "index.html"
PRIORITY_SLUGS = [
    "ai-tools-for-freelancers",
    "best-free-ai-tools-for-freelancers",
    "top-10-ai-tools-for-freelancers",
    "best-ai-tools-for-small-business",
    "chatgpt-claude-gemini-comparison",
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


def test_aistackcost_goal7_main_page_has_structured_comparison_and_cost_workflow():
    html = read(AISTACK)
    assert "/free-utility-lab/shared/styles/marketplace.css" in html
    assert "/free-utility-lab/shared/styles/print.css" in html
    assert "/free-utility-lab/shared/scripts/utility-actions.js" in html
    assert "FreeUtilityLabActions" in html
    assert 'data-goal="aistackcost-upgrade"' in html
    assert 'data-print-section="aistackcost-result"' in html
    for label in [
        "Free vs paid AI stack comparison",
        "Freelancer stack preset",
        "Small business stack preset",
        "ChatGPT vs Claude vs Gemini comparison",
        "Approximate monthly cost calculator",
        "Last updated",
        "Methodology",
        "Prices and features change",
        "Copy AI stack summary",
        "Download AI stack CSV",
        "Print AI stack plan",
    ]:
        assert label in html


def test_aistackcost_goal7_priority_pages_have_practical_artifacts_and_safe_disclaimers():
    for slug in PRIORITY_SLUGS:
        html = read(ROOT / "aistackcost" / slug / "index.html")
        assert 'data-goal="aistackcost-upgrade"' in html, slug
        assert 'data-print-section="aistackcost-template"' in html, slug
        assert "Copy template" in html, slug
        assert "Print template" in html, slug
        assert "Download CSV" in html, slug
        assert "Stack preset" in html, slug
        assert "Comparison table" in html, slug
        assert "Methodology" in html, slug
        assert "Prices and features change" in html, slug
        assert "OpenAI pricing" in html, slug
        assert "Anthropic pricing" in html, slug
        assert "Google Gemini pricing" in html, slug
        assert "/free-utility-lab/ai-tools/" in html, slug
        assert "/free-utility-lab/tools/" in html, slug
        assert "/free-utility-lab/aistackcost/" in html, slug


def test_aistackcost_goal7_schema_has_breadcrumb_howto_faq_and_no_unsupported_price_claims():
    html = read(AISTACK)
    blocks = schema_blocks(html)
    types = {block.get("@type") for block in blocks}
    assert "BreadcrumbList" in types
    assert "HowTo" in types
    assert "FAQPage" in types
    howto = next(block for block in blocks if block.get("@type") == "HowTo")
    assert "AI stack" in howto["name"]
    assert len(howto.get("step", [])) >= 3
    assert all("text" in step for step in howto["step"])
    assert "$20/month" not in html
    assert "$30/month" not in html
    assert "check the official pricing pages before buying" in html


def test_aistackcost_goal7_uses_maintainable_comparison_data_file():
    data_path = ROOT / "data" / "aistackcost_goal7.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    assert data["last_updated"]
    assert len(data["tools"]) >= 6
    assert len(data["presets"]) >= 3
    for tool in data["tools"]:
        assert {"name", "role", "free_option", "paid_plan_note", "official_url"} <= set(tool)
        assert tool["paid_plan_note"].startswith("Approximate") or "Check official" in tool["paid_plan_note"]
        assert tool["official_url"].startswith("https://")


def test_aistackcost_catalog_records_goal7_upgrade_metadata():
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    aistack = next(asset for asset in catalog["assets"] if asset["id"] == "aistackcost")
    assert aistack["status"] == "live"
    assert "csv" in aistack["outputs"]
    assert "print" in aistack["outputs"]
    assert "HowTo" in aistack["schema_types"]
    assert aistack.get("goal7_upgrade") == "aistackcost-comparison-presets-cost-calculator-methodology-sources"


def test_aistackcost_pages_load_ga4_before_relying_on_it():
    """free-utility-lab-tracking.js/measurement-bridge.js only forward events when
    window.gtag exists. Every aistackcost page must load gtag.js itself, matching
    the other Free Utility Lab assets, or custom events silently never reach GA4."""
    checked = 0
    for html_path in (ROOT / "aistackcost").rglob("index.html"):
        html = read(html_path)
        assert "googletagmanager.com/gtag/js?id=G-54GQ1ZT341" in html, html_path
        assert "gtag('config','G-54GQ1ZT341')" in html or "gtag('config', 'G-54GQ1ZT341')" in html, html_path
        checked += 1
    assert checked >= 6
