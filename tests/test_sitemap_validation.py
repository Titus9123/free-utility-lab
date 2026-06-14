import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_sitemap.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_sitemap", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_current_sitemap_matches_local_html_inventory():
    validator = load_validator()

    result = validator.validate_sitemap(ROOT / "sitemap.xml", site_root=ROOT)

    assert result.ok, result.errors
    assert result.url_count >= 80
    assert result.local_html_count >= 80


def test_sitemap_reports_missing_local_pages(tmp_path):
    validator = load_validator()
    sitemap = tmp_path / "sitemap.xml"
    sitemap.write_text(
        """<?xml version='1.0' encoding='UTF-8'?>
<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
  <url><loc>https://titus9123.github.io/free-utility-lab/missing-page/</loc></url>
</urlset>
""",
        encoding="utf-8",
    )

    result = validator.validate_sitemap(sitemap, site_root=ROOT)

    assert not result.ok
    assert any("missing local html" in error.lower() for error in result.errors)
