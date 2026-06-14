import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGETRESET = ROOT / "budgetreset" / "index.html"


def read_budgetreset() -> str:
    return BUDGETRESET.read_text(encoding="utf-8")


def schema_blocks(html: str):
    marker = '<script type="application/ld+json">'
    remaining = html
    blocks = []
    while marker in remaining:
        _, after = remaining.split(marker, 1)
        raw, remaining = after.split("</script>", 1)
        blocks.append(json.loads(raw.strip()))
    return blocks


def test_budgetreset_goal4_uses_shared_marketplace_modules_and_print_css():
    html = read_budgetreset()
    assert "/free-utility-lab/shared/styles/marketplace.css" in html
    assert "/free-utility-lab/shared/styles/print.css" in html
    assert "/free-utility-lab/shared/scripts/utility-actions.js" in html
    assert "FreeUtilityLabActions" in html
    assert 'data-goal="budgetreset-upgrade"' in html


def test_budgetreset_goal4_above_fold_explains_outputs_fast():
    html = read_budgetreset()
    assert "3-step budget worksheet" in html
    assert "1. Add income" in html
    assert "2. Review bills + debt" in html
    assert "3. Copy, CSV or print" in html
    assert "Copy plan summary" in html
    assert "Print worksheet" in html
    assert "Download CSV for Excel" in html


def test_budgetreset_goal4_has_printable_copyable_result_section():
    html = read_budgetreset()
    assert 'data-print-section="budgetreset-result"' in html
    assert 'id="copySummary"' in html
    assert 'id="printWorksheet"' in html
    assert 'id="summaryText"' in html
    assert "budgetreset-pro-summary.txt" in html
    assert "copy_click" in html
    assert "print_click" in html
    assert "calculator_start" in html
    assert "calculator_complete" in html


def test_budgetreset_goal4_schema_has_breadcrumb_and_howto():
    blocks = schema_blocks(read_budgetreset())
    types = {block.get("@type") for block in blocks}
    assert "BreadcrumbList" in types
    assert "HowTo" in types
    howto = next(block for block in blocks if block.get("@type") == "HowTo")
    assert "monthly budget" in howto["name"].lower()
    assert len(howto.get("step", [])) >= 3
    assert all("text" in step for step in howto["step"])


def test_budgetreset_goal4_links_to_marketplace_hubs_and_priority_support_pages():
    html = read_budgetreset()
    for href in [
        "/free-utility-lab/tools/",
        "/free-utility-lab/finance-tools/",
        "/free-utility-lab/printable-templates/",
        "/free-utility-lab/budgetreset/free-printable-monthly-bill-calendar-pdf/",
        "/free-utility-lab/budgetreset/monthly-bill-calendar-template-free-pdf/",
        "/free-utility-lab/budgetreset/monthly-bill-calendar-free-printable/",
        "/free-utility-lab/budgetreset/monthly-bill-calendar-printable-free/",
        "/free-utility-lab/budgetreset/biweekly-paycheck-budget-template-google-sheets-free/",
        "/free-utility-lab/budgetreset/paycheck-budget-template/",
        "/free-utility-lab/budgetreset/debt-payoff-tracker/",
        "/free-utility-lab/budgetreset/zero-based-budget-template/",
    ]:
        assert f'href="{href}"' in html


def test_budgetreset_catalog_records_goal4_upgrade_metadata():
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    budgetreset = next(asset for asset in catalog["assets"] if asset["id"] == "budgetreset")
    assert budgetreset["status"] == "live"
    assert "copy" in budgetreset["outputs"]
    assert "csv" in budgetreset["outputs"]
    assert "print" in budgetreset["outputs"]
    assert "HowTo" in budgetreset["schema_types"]
    assert budgetreset.get("goal4_upgrade") == "budgetreset-utility-export-print-copy-internal-links"
