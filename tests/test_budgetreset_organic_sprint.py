from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINANCE_HUB = ROOT / "finance-tools" / "index.html"


def read_hub() -> str:
    return FINANCE_HUB.read_text(encoding="utf-8")


def test_finance_hub_exposes_distinct_budget_jobs_not_only_brand_tool():
    html = read_hub()
    required_paths = [
        "/free-utility-lab/budgetreset/",
        "/free-utility-lab/budgetreset/monthly-bill-calendar/",
        "/free-utility-lab/budgetreset/biweekly-budget-planner/",
        "/free-utility-lab/budgetreset/debt-snowball-calculator/",
        "/free-utility-lab/budgetreset/emergency-fund-tracker/",
        "/free-utility-lab/budgetreset/50-30-20-budget-calculator/",
    ]
    for path in required_paths:
        assert f'href="{path}"' in html
    assert "6 free finance tools by budgeting job" in html


def test_finance_hub_matches_format_intent_and_sets_user_expectations():
    html = read_hub()
    for phrase in [
        "Choose by the job you need to finish",
        "Monthly bills",
        "Paycheck planning",
        "Debt payoff",
        "Emergency savings",
        "Budget split",
        "Educational planning tools, not financial advice",
        "No bank connection",
    ]:
        assert phrase in html


def test_finance_hub_tracks_support_page_discovery():
    html = read_hub()
    assert html.count('data-event="support_page_click"') >= 5
    assert "support_page_click" in html
    assert "finance-tools" in html


def test_finance_hub_has_faq_and_richer_itemlist_schema():
    html = read_hub()
    assert '"@type": "FAQPage"' in html
    assert '"name": "Monthly Bill Calendar"' in html
    assert '"name": "Biweekly Budget Planner"' in html
    assert '"name": "Debt Snowball Calculator"' in html
