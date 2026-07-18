#!/usr/bin/env python3
"""Render Goal 3 marketplace foundation hub pages.

This is intentionally small and deterministic: it reads the Goal 1 catalog,
uses the Goal 2 shared CSS/JS module paths, and writes only the six approved
hub pages for Goal 3. It does not rewrite existing asset pages.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://titus9123.github.io/free-utility-lab/"
GA4_MEASUREMENT_ID = "G-54GQ1ZT341"
BASE_PATH = "/free-utility-lab/"

CATEGORY_META = {
    "tools": {
        "title": "Free Online Tools, Calculators and Printable Templates",
        "h1": "Free online tools, calculators and printable templates",
        "description": "Browse every Free Utility Lab tool: budget planners, grocery templates, moving calculators, AI stack cost planners and printable worksheets. Free, fast and no signup.",
        "intro": "Start with a practical tool, calculator, worksheet or checklist. Every asset is designed to be usable immediately, without registration or an email gate.",
        "category": None,
        "printable_only": False,
    },
    "printable-templates": {
        "title": "Free Printable Templates and Worksheets",
        "h1": "Free printable templates and worksheets",
        "description": "Print free worksheets, planners, calendars, grocery lists and moving checklists from Free Utility Lab. No signup required.",
        "intro": "Use these print-friendly tools when you want a worksheet, planner, calendar or checklist you can complete offline.",
        "category": None,
        "printable_only": True,
    },
    "finance-tools": {
        "title": "Free Budget and Finance Tools",
        "h1": "Free budget and finance tools",
        "description": "Free budget planners, bill calendars, paycheck budget templates and debt payoff worksheets. Copy, export or print without signup.",
        "intro": "Plan bills, paychecks and debt payoff with practical money tools that work as calculators and printable worksheets.",
        "category": "finance-tools",
        "printable_only": False,
    },
    "meal-planning-tools": {
        "title": "Free Meal Planning and Grocery Tools",
        "h1": "Free meal planning and grocery tools",
        "description": "Free weekly meal planners, grocery list templates and budget grocery worksheets. Print, copy or export with no signup.",
        "intro": "Turn meal planning into a simple weekly workflow: choose a planner, build a grocery list, then print or copy your plan.",
        "category": "meal-planning-tools",
        "printable_only": False,
    },
    "moving-tools": {
        "title": "Free Moving Budget and Checklist Tools",
        "h1": "Free moving budget and checklist tools",
        "description": "Free moving cost calculators, apartment budget worksheets, moving checklists and box calculators. No email required.",
        "intro": "Estimate moving costs, plan boxes and keep the first-apartment budget visible before moving day.",
        "category": "moving-tools",
        "printable_only": False,
    },
    "ai-tools": {
        "title": "Free AI Tool Cost and Stack Planners",
        "h1": "Free AI tool cost and stack planners",
        "description": "Free AI subscription cost planners and tool-stack comparisons for freelancers, creators, agencies and small businesses.",
        "intro": "Compare AI tool stacks and estimate recurring subscription costs before adding another paid plan.",
        "category": "ai-tools",
        "printable_only": False,
    },
}

HUB_LINKS = [
    ("All tools", "/free-utility-lab/tools/"),
    ("Printable templates", "/free-utility-lab/printable-templates/"),
    ("Finance tools", "/free-utility-lab/finance-tools/"),
    ("Meal planning tools", "/free-utility-lab/meal-planning-tools/"),
    ("Moving tools", "/free-utility-lab/moving-tools/"),
    ("AI tools", "/free-utility-lab/ai-tools/"),
]

FINANCE_JOB_ASSETS = [
    ("Monthly Bill Calendar", "monthly-bill-calendar", "Monthly bills", "Place due dates, planned amounts and payment status on one printable calendar.", "calendar", "print"),
    ("Biweekly Budget Planner", "biweekly-budget-planner", "Paycheck planning", "Assign bills and savings to each paycheck before the money is spent.", "planner", "csv"),
    ("Debt Snowball Calculator", "debt-snowball-calculator", "Debt payoff", "Order balances and model a focused smallest-balance-first payoff plan.", "calculator", "copy"),
    ("Emergency Fund Tracker", "emergency-fund-tracker", "Emergency savings", "Set a savings target and track progress without connecting a bank account.", "tracker", "print"),
    ("50/30/20 Budget Calculator", "50-30-20-budget-calculator", "Budget split", "Compare needs, wants and savings against the 50/30/20 guideline.", "calculator", "copy"),
]


def load_assets() -> list[dict[str, Any]]:
    catalog = json.loads((ROOT / "data" / "marketplace.json").read_text(encoding="utf-8"))
    return [asset for asset in catalog["assets"] if asset.get("status") == "live" and asset.get("page_type") != "hub"]


def path_from_public_url(public_url: str) -> str:
    if public_url.startswith(BASE_URL):
        return BASE_PATH + public_url.removeprefix(BASE_URL)
    return public_url


def label(value: str) -> str:
    labels = {"csv": "CSV", "external_link": "External link", "no_signup": "No signup"}
    return labels.get(value, value.replace("_", " ").title())


def badge_list(items: list[str]) -> str:
    return "".join(f'<span class="ful-badge">{escape(label(item))}</span>' for item in items if item)


def tool_card(asset: dict[str, Any]) -> str:
    badges = ["free", "no_signup", *asset.get("outputs", [])]
    href = path_from_public_url(asset["public_url"])
    return f"""<article class="ful-tool-card" data-asset-id="{escape(asset['id'])}" data-category="{escape(asset['category'])}">
  <div class="ful-card-topline">{escape(asset['category'])}</div>
  <h3>{escape(asset['name'])}</h3>
  <p>{escape(asset.get('intent', ''))}</p>
  <div class="ful-badges" aria-label="Tool outputs">{badge_list(badges)}</div>
  <p class="ful-card-meta">Formats: {escape(', '.join(asset.get('formats', [])))}</p>
  <p class="ful-card-meta">Useful for: {escape(', '.join(asset.get('user_types', [])))}</p>
  <a class="ful-primary-cta" href="{escape(href)}" data-event="related_tool_click" data-asset-id="{escape(asset.get('tracking_asset_id', asset['id']))}">Open free tool</a>
</article>"""


def item_list_schema(slug: str, assets: list[dict[str, Any]]) -> dict[str, Any]:
    items = [
        {"@type": "ListItem", "position": index + 1, "name": asset["name"], "url": asset["public_url"]}
        for index, asset in enumerate(assets)
    ]
    if slug == "finance-tools":
        for name, path, _job, _description, _format, _output in FINANCE_JOB_ASSETS:
            items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "url": BASE_URL + "budgetreset/" + path + "/"})
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": CATEGORY_META[slug]["h1"],
        "url": BASE_URL + slug + "/",
        "itemListElement": items,
    }


def breadcrumb_schema(slug: str) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Free Utility Lab", "item": BASE_URL},
            {"@type": "ListItem", "position": 2, "name": CATEGORY_META[slug]["h1"], "item": BASE_URL + slug + "/"},
        ],
    }


def select_assets(slug: str, assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    meta = CATEGORY_META[slug]
    selected = assets
    if meta["category"]:
        selected = [asset for asset in selected if asset.get("category") == meta["category"]]
    if meta["printable_only"]:
        selected = [asset for asset in selected if "print" in asset.get("outputs", []) and "external_link" not in asset.get("outputs", [])]
    return sorted(selected, key=lambda item: item.get("priority", 999))


def hub_nav(active_slug: str) -> str:
    links = []
    active_href = f"/free-utility-lab/{active_slug}/"
    for name, href in HUB_LINKS:
        current = ' aria-current="page"' if href == active_href else ""
        links.append(f'<a href="{href}"{current}>{escape(name)}</a>')
    return "\n".join(links)


def render_page(slug: str, assets: list[dict[str, Any]]) -> str:
    meta = CATEGORY_META[slug]
    selected = select_assets(slug, assets)
    cards = "\n".join(tool_card(asset) for asset in selected)
    finance_intro = ""
    finance_faq = ""
    schema_three = ""
    result_heading = f"{len(selected)} free tools in this hub"
    if slug == "finance-tools":
        result_heading = f"{len(selected) + len(FINANCE_JOB_ASSETS)} free finance tools by budgeting job"
        finance_intro = """<section class="ful-related-hubs" aria-labelledby="finance-job-heading">
      <h2 id="finance-job-heading">Choose by the job you need to finish</h2>
      <p>Start with the complete planner or open a focused calculator, tracker or printable. Every option is free and requires no signup. No bank connection is used.</p>
      <p><strong>Important:</strong> Educational planning tools, not financial advice. Check figures and decisions against your own circumstances.</p>
    </section>"""
        finance_cards = []
        for name, path, job, description, format_name, output in FINANCE_JOB_ASSETS:
            finance_cards.append(f"""<article class="ful-tool-card" data-asset-id="budgetreset-{escape(path)}" data-category="finance-tools">
  <div class="ful-card-topline">{escape(job)}</div><h3>{escape(name)}</h3><p>{escape(description)}</p>
  <div class="ful-badges" aria-label="Tool outputs">{badge_list(['free', 'no_signup', output])}</div>
  <p class="ful-card-meta">Format: {escape(format_name)}</p>
  <a class="ful-primary-cta" href="/free-utility-lab/budgetreset/{escape(path)}/" data-event="support_page_click" data-asset-id="budgetreset-{escape(path)}">Open {escape(job.lower())} tool</a>
</article>""")
        cards += "\n" + "\n".join(finance_cards)
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "Are these budgeting tools free?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. They can be used without signup or a bank connection."}},
            {"@type": "Question", "name": "Are these tools financial advice?", "acceptedAnswer": {"@type": "Answer", "text": "No. They are educational planning tools; verify figures and decisions for your circumstances."}},
        ]}
        schema_three = f'<script type="application/ld+json">\n{json.dumps(faq, ensure_ascii=False, indent=2)}\n  </script>'
        finance_faq = """<section class="ful-related-hubs" aria-labelledby="finance-faq-heading"><h2 id="finance-faq-heading">Budget tool FAQ</h2><h3>Are these tools free?</h3><p>Yes. Use, copy or print them without signup.</p><h3>Do they connect to a bank?</h3><p>No. Enter only the planning figures you choose; never enter credentials or account numbers.</p></section>"""
    related_hubs = "\n".join(
        f'<a class="ful-hub-pill" href="{href}">{escape(name)}</a>'
        for name, href in HUB_LINKS
        if href != f"/free-utility-lab/{slug}/"
    )
    filter_options = "\n".join(
        f'<option value="{escape(category)}">{escape(label(category))}</option>'
        for category in sorted({asset["category"] for asset in assets})
    )
    schema_one = json.dumps(breadcrumb_schema(slug), ensure_ascii=False, indent=2)
    schema_two = json.dumps(item_list_schema(slug, selected), ensure_ascii=False, indent=2)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}');
  </script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(meta['title'])} | Free Utility Lab</title>
  <meta name="description" content="{escape(meta['description'])}">
  <link rel="canonical" href="{BASE_URL}{slug}/">
  <link rel="stylesheet" href="../shared/styles/marketplace.css">
  <link rel="stylesheet" href="../shared/styles/print.css" media="print">
  <script type="application/ld+json">
{schema_one}
  </script>
  <script type="application/ld+json">
{schema_two}
  </script>
  {schema_three}
</head>
<body data-page-type="marketplace-hub" data-hub-slug="{escape(slug)}">
  <header class="ful-marketplace-hero">
    <nav class="ful-breadcrumb" aria-label="Breadcrumb"><a href="/free-utility-lab/">Free Utility Lab</a><span class="ful-breadcrumb-separator">/</span><span aria-current="page">{escape(meta['h1'])}</span></nav>
    <p class="ful-eyebrow">Free Utility Lab marketplace</p>
    <h1>{escape(meta['h1'])}</h1>
    <p class="ful-hero-copy">{escape(meta['intro'])}</p>
    <div class="ful-badges" aria-label="Marketplace promises">{badge_list(['free', 'no_signup', 'copy', 'csv', 'print'])}</div>
  </header>

  <main class="ful-marketplace-shell">
    {finance_intro}
    <aside class="ful-hub-sidebar" aria-label="Marketplace hubs">
      <h2>Browse by job</h2>
      <nav class="ful-hub-nav">
{hub_nav(slug)}
      </nav>
      <section class="ful-filter-panel" aria-label="Filter tools">
        <h2>Filter tools</h2>
        <label>Category
          <select data-filter-control="category">
            <option value="">All categories</option>
{filter_options}
          </select>
        </label>
        <label>Output
          <select data-filter-control="output">
            <option value="">Any output</option>
            <option value="copy">Copy</option>
            <option value="csv">CSV</option>
            <option value="print">Print</option>
            <option value="external_link">External link</option>
          </select>
        </label>
      </section>
    </aside>

    <section class="ful-tool-results" aria-label="Free tools">
      <div class="ful-section-heading">
        <h2>{result_heading}</h2>
        <p>Open a tool, then copy, export or print the result. No account required.</p>
      </div>
      <div class="ful-tool-grid" data-marketplace-results>
{cards}
      </div>
    </section>

    {finance_faq}

    <section class="ful-related-hubs" aria-label="Related hubs">
      <h2>Related hubs</h2>
      <div class="ful-hub-pill-list">
{related_hubs}
      </div>
    </section>
  </main>

  <script src="../shared/components/marketplace-components.js"></script>
  <script src="../shared/scripts/utility-actions.js"></script>
  <script src="../free-utility-lab-tracking.js"></script>
  <script src="../free-utility-lab-measurement-bridge.js"></script>
  <script>
    window.FreeUtilityLabComponents = window.FreeUtilityLabComponents || {{}};
    window.FreeUtilityLabActions = window.FreeUtilityLabActions || {{}};
    document.querySelectorAll('[data-event="related_tool_click"], [data-event="support_page_click"]').forEach(function (link) {{
      link.addEventListener('click', function () {{
        if (window.FreeUtilityLabActions.trackSafeEvent) {{
          window.FreeUtilityLabActions.trackSafeEvent(link.dataset.event || 'related_tool_click', {{ asset_id: link.dataset.assetId, hub: '{escape(slug)}' }});
        }}
      }});
    }});
  </script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def main() -> int:
    assets = load_assets()
    for slug in CATEGORY_META:
        output = ROOT / slug / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_page(slug, assets), encoding="utf-8")
        print(f"rendered {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
