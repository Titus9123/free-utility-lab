from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.validate_domain_migration import validate_domain_migration_readiness

ROOT = Path(__file__).resolve().parents[1]


def test_goal11_domain_migration_config_and_docs_are_ready_without_cutover():
    config = ROOT / "data" / "domain_migration.json"
    doc = ROOT / "docs" / "DOMAIN_MIGRATION_GOAL11.md"
    cname = ROOT / "CNAME"

    assert config.exists()
    assert doc.exists()
    assert not cname.exists(), "Goal 11 readiness must not switch GitHub Pages domain yet"

    text = doc.read_text(encoding="utf-8")
    required_phrases = [
        "Goal 11 domain migration readiness",
        "selected_custom_domain",
        "current_canonical_base",
        "target_canonical_base",
        "canonical rewrite plan",
        "sitemap URL rewrite plan",
        "redirect strategy",
        "GSC new property checklist",
        "GA4 continuity check",
        "post-migration crawl validation",
        "Do not create CNAME",
    ]
    for phrase in required_phrases:
        assert phrase in text

    forbidden = ["client" + "_secret", "access" + "_token", "password", "secrets."]
    assert not any(item in text.lower() for item in forbidden)


def test_goal11_validator_inventory_matches_current_site_and_target_domain():
    result = validate_domain_migration_readiness(ROOT)

    assert result.ok, result.errors
    assert result.html_count >= 90
    assert result.sitemap_url_count == result.html_count
    assert result.current_base == "https://titus9123.github.io/free-utility-lab/"
    assert result.target_base == "https://freeutilitylab.com/"
    assert result.selected_custom_domain == "freeutilitylab.com"
    assert result.base_path == "/free-utility-lab/"


def test_goal11_does_not_migrate_urls_before_final_cutover():
    sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "https://freeutilitylab.com/" not in sitemap_text
    assert "https://titus9123.github.io/free-utility-lab/" in sitemap_text

    urls = [
        loc.text.strip()
        for loc in ET.parse(ROOT / "sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc.text
    ]
    assert urls
    assert all(url.startswith("https://titus9123.github.io/free-utility-lab/") for url in urls)

    html_files = [path for path in ROOT.rglob("*.html") if ".git" not in path.parts]
    assert html_files
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        assert "https://freeutilitylab.com/" not in text
