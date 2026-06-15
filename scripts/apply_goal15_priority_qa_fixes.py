#!/usr/bin/env python3
"""Apply Goal 15 priority QA fixes to organic support pages.

The fixes turn thin priority support pages into verifiable mini-tools by adding
printable/copyable/exportable artifacts, schema, stronger internal links, and
tracking-compatible action markers.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://titus9123.github.io/free-utility-lab"

BUDGETRESET_TOP = {
    "free-printable-monthly-bill-calendar-pdf": {
        "name": "Free printable monthly bill calendar PDF",
        "angle": "PDF-style month view for renters or households that want one page to print before payday.",
        "rows": [
            ("Rent / mortgage", "1st", "$1,400", "Autopay", "Confirm balance 3 days before"),
            ("Electric", "8th", "$120", "Manual", "Check usage spike"),
            ("Internet", "12th", "$65", "Autopay", "Save confirmation"),
            ("Credit card", "18th", "$250", "Manual", "Pay above minimum"),
        ],
    },
    "monthly-bill-calendar-template-free-pdf": {
        "name": "Monthly bill calendar template free PDF",
        "angle": "Template-first layout for people comparing due dates, autopay status and paycheck timing.",
        "rows": [
            ("Phone", "3rd", "$55", "Autopay", "Match card date"),
            ("Car insurance", "9th", "$145", "Manual", "Set reminder"),
            ("Streaming", "14th", "$22", "Autopay", "Cancel if unused"),
            ("Loan", "24th", "$310", "Manual", "Schedule after paycheck"),
        ],
    },
    "monthly-bill-calendar-free-printable": {
        "name": "Monthly bill calendar free printable",
        "angle": "Printable checklist version for families who want a refrigerator-friendly monthly bill tracker.",
        "rows": [
            ("Water", "5th", "$48", "Manual", "Add meter photo"),
            ("Childcare", "10th", "$600", "Manual", "Split across paychecks"),
            ("Gas", "16th", "$80", "Autopay", "Review average"),
            ("Savings transfer", "28th", "$150", "Autopay", "Treat as a bill"),
        ],
    },
    "monthly-bill-calendar-printable-free": {
        "name": "Monthly bill calendar printable free",
        "angle": "Due-date focused printable for catching bills that land before the next paycheck clears.",
        "rows": [
            ("Rent", "1st", "$1,250", "Manual", "Move cash before month starts"),
            ("Minimum card payment", "7th", "$90", "Autopay", "Verify autopay cap"),
            ("Internet", "15th", "$70", "Manual", "Negotiate annually"),
            ("Gym", "27th", "$35", "Autopay", "Cancel if unused"),
        ],
    },
    "biweekly-paycheck-budget-template-google-sheets-free": {
        "name": "Biweekly paycheck budget template Google Sheets free",
        "angle": "Paycheck split worksheet for assigning bills to first check, second check and buffer.",
        "rows": [
            ("Check 1", "Rent reserve", "$700", "Manual", "Hold before spending"),
            ("Check 1", "Utilities", "$180", "Autopay", "Leave in checking"),
            ("Check 2", "Debt payoff", "$220", "Manual", "Pay after deposit"),
            ("Check 2", "Groceries", "$360", "Manual", "Weekly cap"),
        ],
    },
    "paycheck-budget-template": {
        "name": "Paycheck budget template",
        "angle": "Simple paycheck-by-paycheck template for covering bills before flexible spending.",
        "rows": [
            ("Income", "Paycheck", "$1,850", "Deposit", "Use net pay"),
            ("Bills", "Fixed due before next check", "$1,120", "Reserve", "List due dates"),
            ("Spending", "Food and transport", "$420", "Cash cap", "Split by week"),
            ("Buffer", "Leftover", "$310", "Save", "Protect from surprises"),
        ],
    },
    "debt-payoff-tracker": {
        "name": "Debt payoff tracker",
        "angle": "Debt tracker for choosing next payment priority without connecting accounts or entering private logins.",
        "rows": [
            ("Card A", "18th", "$3,400", "Manual", "Highest APR first"),
            ("Student loan", "22nd", "$8,200", "Autopay", "Keep minimum current"),
            ("Medical bill", "30th", "$620", "Manual", "Ask for plan"),
            ("Card B", "12th", "$980", "Manual", "Snowball candidate"),
        ],
    },
    "zero-based-budget-template": {
        "name": "Zero based budget template",
        "angle": "Zero-based worksheet for assigning every dollar to bills, spending, saving or debt before the month begins.",
        "rows": [
            ("Income", "Monthly net income", "$4,200", "Plan", "Start with take-home pay"),
            ("Needs", "Rent, utilities, food", "$2,650", "Reserve", "Cover first"),
            ("Goals", "Debt and savings", "$900", "Schedule", "Automate if safe"),
            ("Wants", "Flexible spending", "$650", "Cap", "Stop at zero"),
        ],
    },
}

MEAL_FAQS = {
    "weekly-meal-planner-printable": ("Can I print this weekly meal planner?", "Yes. Use the print action on the planner section and keep the page as a no-login weekly meal plan worksheet."),
    "grocery-list-template-free-editable": ("Can I edit the grocery list template?", "Yes. Copy the template text or export the CSV, then adjust categories in your notes app or spreadsheet."),
}

MOVE_BREADCRUMBS = {
    "moving-cost-calculator-no-email": "Moving cost calculator no email",
    "free-printable-first-apartment-budget-worksheet": "Free printable first apartment budget worksheet",
}


def script_block(obj: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + '</script>'


def add_schema_before_head(html: str, marker: str, block: str) -> str:
    if marker in html:
        return html
    return html.replace("</head>", block + "</head>", 1)


def budget_table_html(slug: str, data: dict) -> str:
    rows = "".join(
        f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>"
        for a, b, c, d, e in data["rows"]
    )
    title = data["name"]
    return f'''
<section class="card" id="budgetreset-template" data-print-section="budgetreset-template" aria-labelledby="budgetreset-template-title">
  <span class="kicker">Mini-tool worksheet</span>
  <h2 id="budgetreset-template-title">Copy, export or print this {title.lower()} worksheet</h2>
  <p>{data["angle"]} No signup, no bank connection and no private account numbers required.</p>
  <div class="table-wrap"><table><thead><tr><th>Bill or bucket</th><th>Due date / timing</th><th>Planned amount</th><th>Payment mode</th><th>Action note</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="ful-action-row">
    <button type="button" data-copy-target="#budgetreset-template">Copy template</button>
    <button type="button" data-csv-target="#budgetreset-template table" data-filename="{slug}.csv">Download CSV</button>
    <button type="button" data-print-section="budgetreset-template">Print template</button>
  </div>
  <h3>Practical example</h3>
  <p>Start by filling only public labels, due dates and planned amounts. Then mark autopay or manual payment and review the next bill before the paycheck that must cover it.</p>
  <p><a class="cta" href="/free-utility-lab/budgetreset/" data-event="support_page_click">Open the full BudgetReset tool</a> <a class="chip" href="/free-utility-lab/finance-tools/" data-event="support_page_click">Browse finance tools</a></p>
</section>
'''


def apply_budgetreset() -> None:
    for slug, data in BUDGETRESET_TOP.items():
        path = ROOT / "budgetreset" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        if 'data-goal="budgetreset-support-upgrade"' not in html:
            if '<body data-asset-id="' in html:
                html = html.replace('<body data-asset-id="', '<body data-goal="budgetreset-support-upgrade" data-asset-id="', 1)
            elif '<body' in html:
                html = html.replace('<body', '<body data-goal="budgetreset-support-upgrade"', 1)
        if '/free-utility-lab/finance-tools/' not in html:
            html = html.replace('</nav></header>', '<a class="chip" href="/free-utility-lab/finance-tools/">Finance tools</a></nav></header>', 1)
        if 'id="budgetreset-template"' not in html:
            html = html.replace('</main>', budget_table_html(slug, data) + '</main>', 1)
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f"Is this {data['name'].lower()} really free?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. The worksheet can be copied, exported as CSV or printed without signup."}},
                {"@type": "Question", "name": "Do I need to enter private financial data?", "acceptedAnswer": {"@type": "Answer", "text": "No. Use labels, due dates and planned amounts only; do not enter account numbers or credentials."}},
            ],
        }
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Free Utility Lab", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Finance tools", "item": f"{BASE}/finance-tools/"},
                {"@type": "ListItem", "position": 3, "name": "BudgetReset", "item": f"{BASE}/budgetreset/"},
                {"@type": "ListItem", "position": 4, "name": data["name"], "item": f"{BASE}/budgetreset/{slug}/"},
            ],
        }
        html = add_schema_before_head(html, '"@type":"FAQPage"', script_block(faq))
        html = add_schema_before_head(html, '"@type":"BreadcrumbList"', script_block(breadcrumb))
        if 'shared/scripts/utility-actions.js' not in html:
            html = html.replace('<script src="/free-utility-lab/free-utility-lab-tracking.js" defer></script>', '<script src="/free-utility-lab/shared/scripts/utility-actions.js" defer></script>\n<script src="/free-utility-lab/free-utility-lab-tracking.js" defer></script>', 1)
        path.write_text(html, encoding="utf-8")


def apply_meal() -> None:
    for slug, (q, a) in MEAL_FAQS.items():
        path = ROOT / "mealplansheet" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}]}
        html = add_schema_before_head(html, '"@type":"FAQPage"', script_block(faq))
        path.write_text(html, encoding="utf-8")


def apply_move() -> None:
    for slug, name in MOVE_BREADCRUMBS.items():
        path = ROOT / "movebudget" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Free Utility Lab", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Moving tools", "item": f"{BASE}/moving-tools/"},
                {"@type": "ListItem", "position": 3, "name": "MoveBudget", "item": f"{BASE}/movebudget/"},
                {"@type": "ListItem", "position": 4, "name": name, "item": f"{BASE}/movebudget/{slug}/"},
            ],
        }
        html = add_schema_before_head(html, '"@type":"BreadcrumbList"', script_block(breadcrumb))
        path.write_text(html, encoding="utf-8")


def main() -> int:
    apply_budgetreset()
    apply_meal()
    apply_move()
    print("Goal 15 priority QA fixes applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
