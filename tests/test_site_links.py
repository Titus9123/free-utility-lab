import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_site_links.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_site_links", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_site_links_accept_current_static_site():
    validator = load_validator()

    result = validator.validate_site_links(ROOT)

    assert result.ok, result.errors[:10]
    assert result.files_checked >= 80


def test_site_links_report_missing_internal_html(tmp_path):
    validator = load_validator()
    page = tmp_path / "index.html"
    page.write_text('<a href="/free-utility-lab/missing-page/">Broken</a>', encoding="utf-8")

    result = validator.validate_site_links(tmp_path, base_path="/free-utility-lab/")

    assert not result.ok
    assert any("missing internal link target" in error.lower() for error in result.errors)


def test_site_links_ignore_external_and_fragment_links(tmp_path):
    validator = load_validator()
    page = tmp_path / "index.html"
    page.write_text(
        '<a href="#top">Top</a><a href="https://example.com/x">External</a><a href="mailto:test@example.com">Mail</a>',
        encoding="utf-8",
    )

    result = validator.validate_site_links(tmp_path, base_path="/free-utility-lab/")

    assert result.ok, result.errors
