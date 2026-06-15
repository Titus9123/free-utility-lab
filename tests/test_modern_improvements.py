"""Tests for the modern UX/SEO/interactivity improvements across all 4 assets."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ── BudgetReset improvements ──────────────────────────────────────────────────

BUDGETRESET = ROOT / "budgetreset" / "index.html"


def test_budgetreset_has_budget_semaphore():
    html = read(BUDGETRESET)
    assert 'id="budgetSemaphore"' in html
    assert "br-semaphore" in html
    assert "updateSemaphore" in html


def test_budgetreset_has_5030_analysis():
    html = read(BUDGETRESET)
    assert 'id="analysis5030"' in html
    assert "50 / 30 / 20" in html
    assert "update5030" in html
    assert "lbl-needs" in html
    assert "lbl-savings" in html


def test_budgetreset_uses_br_localStorage_namespace():
    html = read(BUDGETRESET)
    assert "br_budget_v1" in html
    assert "lsSave" in html
    assert "lsRestore" in html


def test_budgetreset_loads_shared_budget_calc():
    html = read(BUDGETRESET)
    assert "/free-utility-lab/shared/scripts/budget-calc.js" in html


# ── Shared budget-calc.js ─────────────────────────────────────────────────────

BUDGET_CALC = ROOT / "shared" / "scripts" / "budget-calc.js"


def test_budget_calc_exists_and_exports():
    assert BUDGET_CALC.exists(), "shared/scripts/budget-calc.js must exist"
    js = BUDGET_CALC.read_text(encoding="utf-8")
    assert "analyze5030" in js
    assert "budgetHealth" in js
    assert "payoffMonths" in js
    assert "lsGet" in js
    assert "lsSet" in js
    assert "csvEscape" in js
    assert "BudgetCalc" in js


def test_budget_calc_has_umd_wrapper():
    js = BUDGET_CALC.read_text(encoding="utf-8")
    assert "module.exports" in js
    assert "factory" in js


# ── MealPlanSheet improvements ────────────────────────────────────────────────

MEALPLANSHEET = ROOT / "mealplansheet" / "index.html"


def test_mealplansheet_has_scroll_snap_mobile():
    html = read(MEALPLANSHEET)
    assert "scroll-snap-type" in html
    assert "scroll-snap-align" in html


def test_mealplansheet_has_grocery_checkboxes():
    html = read(MEALPLANSHEET)
    assert "mp-check-item" in html
    assert "mp_grocery_checks_v1" in html


def test_mealplansheet_has_weekly_cost_estimate():
    html = read(MEALPLANSHEET)
    assert "mp-cost-bar" in html
    assert "Estimated weekly grocery cost" in html
    assert "Rough planning range only" in html


def test_mealplansheet_has_quick_swap():
    html = read(MEALPLANSHEET)
    assert "mp-swap-btn" in html
    assert "swap" in html.lower()


def test_mealplansheet_uses_mp_localStorage_namespace():
    html = read(MEALPLANSHEET)
    assert "mp_grocery_checks_v1" in html
    assert "mp_plan_v1" in html


# ── MoveBudget improvements ───────────────────────────────────────────────────

MOVEBUDGET = ROOT / "movebudget" / "index.html"


def test_movebudget_has_diy_vs_movers_comparator():
    html = read(MOVEBUDGET)
    assert "diy-movers-title" in html or "DIY vs professional movers" in html
    assert "diyCalcBtn" in html
    assert "diyResult" in html or "diy-movers" in html


def test_movebudget_has_day1_cash_metric():
    html = read(MOVEBUDGET)
    assert "day1Cash" in html
    assert "Day-1 cash" in html or "day1-title" in html


def test_movebudget_uses_mb_localStorage_namespace():
    html = read(MOVEBUDGET)
    assert "mb_budget_v1" in html
    assert "lsSave" in html or "lsRestore" in html


def test_movebudget_diy_verdict_logic_present():
    html = read(MOVEBUDGET)
    assert "DIY is cheaper" in html or "cheaper" in html
    assert "professional movers" in html.lower()


# ── AIStackCost improvements ──────────────────────────────────────────────────

AISTACKCOST = ROOT / "aistackcost" / "index.html"


def test_aistackcost_has_asset_lab_modern_css():
    html = read(AISTACKCOST)
    assert "/free-utility-lab/asset-lab-modern.css" in html


def test_aistackcost_has_interactive_stack_builder():
    html = read(AISTACKCOST)
    assert "aiToolGrid" in html
    assert "ai-tool-check" in html
    assert "aiStackTotal" in html
    assert "aiStackCount" in html


def test_aistackcost_has_overlap_alert():
    html = read(AISTACKCOST)
    assert "aiOverlapAlert" in html
    assert "Overlap detected" in html


def test_aistackcost_has_roi_calculator():
    html = read(AISTACKCOST)
    assert "roi-title" in html or "ROI calculator" in html
    assert "roiCalcBtn" in html
    assert "roiResult" in html
    assert "roiValue" in html
    assert "roiNet" in html


def test_aistackcost_has_budget_max_planner():
    html = read(AISTACKCOST)
    assert "aiMaxBudget" in html
    assert "aiBudgetBar" in html
    assert "budget planner" in html.lower()


def test_aistackcost_uses_ai_localStorage_namespace():
    html = read(AISTACKCOST)
    assert "ai_stack_v1" in html


def test_aistackcost_tool_data_has_official_urls():
    html = read(AISTACKCOST)
    assert "openai.com/pricing" in html
    assert "anthropic.com/pricing" in html
    assert "ai.google.dev/pricing" in html


def test_aistackcost_no_exact_prices_without_disclaimer():
    html = read(AISTACKCOST)
    # No "$20/month" or "$30/month" hard claims — only ranges like "$0–$20+"
    assert "$20/month" not in html
    assert "$30/month" not in html
    # Disclaimer must exist
    assert "Prices and features change" in html
    assert "official pricing" in html.lower()


def test_aistackcost_stack_builder_has_preset_categories():
    html = read(AISTACKCOST)
    # Freelancer preset still present
    assert "Freelancer stack preset" in html
    # Small business preset
    assert "Small business stack preset" in html
