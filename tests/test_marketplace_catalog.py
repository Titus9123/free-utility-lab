import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_marketplace_catalog.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_marketplace_catalog", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_catalog(tmp_path, assets):
    catalog_path = tmp_path / "marketplace.json"
    catalog_path.write_text(json.dumps({"assets": assets}, indent=2), encoding="utf-8")
    return catalog_path


def valid_asset(**overrides):
    asset = {
        "id": "budgetreset",
        "name": "BudgetReset",
        "slug": "budgetreset",
        "category": "finance-tools",
        "cluster": "budgetreset",
        "public_url": "https://titus9123.github.io/free-utility-lab/budgetreset/",
        "local_path": "budgetreset/index.html",
        "page_type": "tool",
        "intent": "monthly budget planner",
        "priority": 1,
        "formats": ["calculator", "worksheet"],
        "outputs": ["copy", "csv", "print"],
        "user_types": ["households", "students"],
        "related_tools": ["mealplansheet"],
        "schema_types": ["SoftwareApplication", "FAQPage"],
        "tracking_asset_id": "budgetreset",
        "status": "live",
    }
    asset.update(overrides)
    return asset


def test_valid_catalog_accepts_live_asset_with_required_fields(tmp_path):
    validator = load_validator()
    catalog_path = write_catalog(tmp_path, [valid_asset()])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert result.ok, result.errors


def test_catalog_rejects_missing_required_field(tmp_path):
    validator = load_validator()
    asset = valid_asset()
    asset.pop("tracking_asset_id")
    catalog_path = write_catalog(tmp_path, [asset])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert not result.ok
    assert any("tracking_asset_id" in error for error in result.errors)


def test_catalog_rejects_duplicate_ids_and_urls(tmp_path):
    validator = load_validator()
    catalog_path = write_catalog(tmp_path, [valid_asset(), valid_asset(name="BudgetReset Copy")])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert not result.ok
    assert any("duplicate id" in error.lower() for error in result.errors)
    assert any("duplicate public_url" in error.lower() for error in result.errors)


def test_live_catalog_entries_must_point_to_existing_local_html(tmp_path):
    validator = load_validator()
    catalog_path = write_catalog(tmp_path, [valid_asset(local_path="missing/index.html")])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert not result.ok
    assert any("missing local_path" in error.lower() for error in result.errors)


def test_planned_catalog_entries_may_point_to_future_pages(tmp_path):
    validator = load_validator()
    catalog_path = write_catalog(tmp_path, [valid_asset(status="planned", local_path="tools/index.html")])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert result.ok, result.errors


def test_page_type_output_consistency_rules(tmp_path):
    validator = load_validator()
    printable = valid_asset(
        id="bill-calendar",
        slug="budgetreset/free-printable-monthly-bill-calendar-pdf",
        public_url="https://titus9123.github.io/free-utility-lab/budgetreset/free-printable-monthly-bill-calendar-pdf/",
        local_path="budgetreset/free-printable-monthly-bill-calendar-pdf/index.html",
        page_type="printable",
        formats=["worksheet"],
        outputs=["copy"],
        tracking_asset_id="budgetreset_bill_calendar",
    )

    result = validator.validate_catalog(write_catalog(tmp_path, [printable]), site_root=ROOT)

    assert not result.ok
    assert any("printable" in error.lower() and "print" in error.lower() for error in result.errors)


def test_calculator_pages_require_calculator_format(tmp_path):
    validator = load_validator()
    calculator = valid_asset(
        id="moving-cost-calculator",
        slug="movebudget/moving-cost-calculator-no-email",
        public_url="https://titus9123.github.io/free-utility-lab/movebudget/moving-cost-calculator-no-email/",
        local_path="movebudget/moving-cost-calculator-no-email/index.html",
        page_type="calculator",
        formats=["worksheet"],
        outputs=["copy", "csv"],
        tracking_asset_id="movebudget_moving_cost_calculator",
    )

    result = validator.validate_catalog(write_catalog(tmp_path, [calculator]), site_root=ROOT)

    assert not result.ok
    assert any("calculator" in error.lower() and "format" in error.lower() for error in result.errors)


def test_catalog_rejects_secret_like_values(tmp_path):
    validator = load_validator()
    catalog_path = write_catalog(tmp_path, [valid_asset(intent="access" + "_token=abc123")])

    result = validator.validate_catalog(catalog_path, site_root=ROOT)

    assert not result.ok
    assert any("secret" in error.lower() for error in result.errors)
