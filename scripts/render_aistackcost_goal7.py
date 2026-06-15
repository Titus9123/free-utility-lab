#!/usr/bin/env python3
"""Render Goal 7 AIStackCost selective modular upgrade pages."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://titus9123.github.io/free-utility-lab/"
BASE_PATH = "/free-utility-lab/"
DATA = json.loads((ROOT / "data" / "aistackcost_goal7.json").read_text(encoding="utf-8"))

PRIORITY_PAGES = {
    "ai-tools-for-freelancers": {
        "title": "AI Tools for Freelancers",
        "h1": "AI tools for freelancers: choose a lean paid stack",
        "intro": "Start with one assistant, one production tool, and one workflow helper. Add subscriptions only when they remove repeat work.",
        "preset": "Freelancer stack preset",
    },
    "best-free-ai-tools-for-freelancers": {
        "title": "Best Free AI Tools for Freelancers",
        "h1": "Best free AI tools for freelancers before paying for upgrades",
        "intro": "Use the free-option column first, then compare paid upgrades against real weekly client work.",
        "preset": "Freelancer stack preset",
    },
    "top-10-ai-tools-for-freelancers": {
        "title": "Top 10 AI Tools for Freelancers",
        "h1": "Top AI tools for freelancers, compared by job-to-be-done",
        "intro": "This is a decision workflow, not a hype list. Pick tools by role, overlap, and monthly budget impact.",
        "preset": "Freelancer stack preset",
    },
    "best-ai-tools-for-small-business": {
        "title": "Best AI Tools for Small Business",
        "h1": "Best AI tools for small business: practical stack planner",
        "intro": "Small teams should avoid duplicate subscriptions. Assign each tool to one recurring business workflow before paying.",
        "preset": "Small business stack preset",
    },
    "chatgpt-claude-gemini-comparison": {
        "title": "ChatGPT vs Claude vs Gemini Comparison",
        "h1": "ChatGPT vs Claude vs Gemini comparison for work stacks",
        "intro": "Compare the three general assistants by role fit, free option, official source, and whether your stack needs one or more.",
        "preset": "Freelancer stack preset",
    },
}


def source_links() -> str:
    return "".join(
        f'<li><a href="{escape(source["url"])}">{escape(source["label"])}</a></li>'
        for source in DATA["official_sources"]
    )


def comparison_rows(limit: int | None = None) -> str:
    tools = DATA["tools"][:limit] if limit else DATA["tools"]
    return "".join(
        "<tr>"
        f"<th scope=\"row\">{escape(tool['name'])}</th>"
        f"<td>{escape(tool['role'])}</td>"
        f"<td>{escape(tool['free_option'])}</td>"
        f"<td>{escape(tool['paid_plan_note'])}</td>"
        f"<td><a href=\"{escape(tool['official_url'])}\">Official source</a></td>"
        "</tr>"
        for tool in tools
    )


def presets_markup() -> str:
    cards = []
    for preset in DATA["presets"]:
        roles = "".join(f"<li>{escape(role)}</li>" for role in preset["recommended_roles"])
        cards.append(
            f"<article class=\"ful-tool-card\"><h3>{escape(preset['name'])}</h3>"
            f"<p><strong>Audience:</strong> {escape(preset['audience'])}</p>"
            f"<ul>{roles}</ul><p><strong>Buying rule:</strong> {escape(preset['buying_rule'])}</p></article>"
        )
    return "".join(cards)


def schema(kind: str, page_url: str, title: str) -> str:
    if kind == "breadcrumb":
        block = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Free Utility Lab", "item": BASE_URL},
                {"@type": "ListItem", "position": 2, "name": "AI tools", "item": BASE_URL + "ai-tools/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": page_url},
            ],
        }
    elif kind == "howto":
        block = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": "Build an AI stack without duplicate subscriptions",
            "step": [
                {"@type": "HowToStep", "text": "List the workflows that need AI help before picking tools."},
                {"@type": "HowToStep", "text": "Compare free options, paid plan notes, and official pricing sources."},
                {"@type": "HowToStep", "text": "Estimate approximate monthly cost and remove overlapping subscriptions."},
                {"@type": "HowToStep", "text": "Recheck official pricing pages before buying because prices and features change."},
            ],
        }
    else:
        block = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Are these AI prices guaranteed?",
                    "acceptedAnswer": {"@type": "Answer", "text": DATA["disclaimer"]},
                },
                {
                    "@type": "Question",
                    "name": "Should a freelancer pay for every major AI assistant?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Usually no. Start with one primary assistant and add another only for a specific workflow advantage."},
                },
            ],
        }
    return json.dumps(block, ensure_ascii=False, indent=2)


def head(title: str, description: str, canonical: str) -> str:
    return f"""<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)} | Free Utility Lab</title>
  <meta name=\"description\" content=\"{escape(description)}\">
  <link rel=\"canonical\" href=\"{escape(canonical)}\">
  <link rel=\"stylesheet\" href=\"/free-utility-lab/shared/styles/marketplace.css\">
  <link rel=\"stylesheet\" href=\"/free-utility-lab/shared/styles/print.css\" media=\"print\">
  <script type=\"application/ld+json\">\n{schema('breadcrumb', canonical, title)}\n  </script>
  <script type=\"application/ld+json\">\n{schema('howto', canonical, title)}\n  </script>
  <script type=\"application/ld+json\">\n{schema('faq', canonical, title)}\n  </script>
</head>"""


def nav() -> str:
    return """<nav class=\"ful-breadcrumb\" aria-label=\"Breadcrumb\"><a href=\"/free-utility-lab/\">Free Utility Lab</a><span class=\"ful-breadcrumb-separator\">/</span><a href=\"/free-utility-lab/ai-tools/\">AI tools</a><span class=\"ful-breadcrumb-separator\">/</span><span aria-current=\"page\">AIStackCost</span></nav>"""


def actions(print_section: str, copy_label: str, csv_label: str, print_label: str) -> str:
    return f"""<div class=\"ful-action-row\">
  <button type=\"button\" data-copy-target=\"#{print_section}\">{escape(copy_label)}</button>
  <button type=\"button\" data-csv-target=\"#{print_section} table\">{escape(csv_label)}</button>
  <button type=\"button\" data-print-section=\"{print_section}\">{escape(print_label)}</button>
</div>"""


def common_sections(print_section: str, compact: bool = False) -> str:
    rows = comparison_rows(3 if compact else None)
    return f"""
<section class=\"ful-panel\" aria-labelledby=\"comparison-title\">
  <h2 id=\"comparison-title\">Free vs paid AI stack comparison</h2>
  <p>Comparison table for common AI stack decisions. Use the notes as planning prompts, not final pricing claims.</p>
  <div class=\"ful-table-wrap\"><table><thead><tr><th>Tool</th><th>Best for</th><th>Free option</th><th>Paid plan note</th><th>Official source</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
<section class=\"ful-panel\" aria-labelledby=\"assistant-title\">
  <h2 id=\"assistant-title\">ChatGPT vs Claude vs Gemini comparison</h2>
  <p>ChatGPT vs Claude vs Gemini comparison: pick by workflow fit first, then check official pricing pages before buying.</p>
</section>
<section class=\"ful-panel\" aria-labelledby=\"preset-title\">
  <h2 id=\"preset-title\">Stack preset library</h2>
  <div class=\"ful-tool-grid\">{presets_markup()}</div>
</section>
<section class=\"ful-panel\" aria-labelledby=\"method-title\">
  <h2 id=\"method-title\">Methodology</h2>
  <p>Methodology: group tools by job-to-be-done, prefer free options until usage is proven, compare recurring cost, and remove overlapping subscriptions before upgrading.</p>
  <p><strong>Prices and features change.</strong> These are approximate planning notes only; check the official pricing pages before buying.</p>
  <p><strong>Last updated:</strong> {escape(DATA['last_updated'])}</p>
  <ul>{source_links()}</ul>
</section>
<section class=\"ful-related-hubs\" aria-label=\"Related hubs\"><a class=\"ful-hub-pill\" href=\"/free-utility-lab/ai-tools/\">AI tools</a><a class=\"ful-hub-pill\" href=\"/free-utility-lab/tools/\">All tools</a><a class=\"ful-hub-pill\" href=\"/free-utility-lab/aistackcost/\">AIStackCost</a></section>
"""


def scripts() -> str:
    return """<script src=\"/free-utility-lab/shared/scripts/utility-actions.js\"></script>
<script>
window.FreeUtilityLabActions = window.FreeUtilityLabActions || {};
document.querySelectorAll('[data-price-input]').forEach(function (input) {
  input.addEventListener('input', function () {
    var total = 0;
    document.querySelectorAll('[data-price-input]').forEach(function (field) { total += Number(field.value || 0); });
    var output = document.querySelector('[data-cost-output]');
    if (output) output.textContent = 'Approximate monthly total: ' + total.toLocaleString('en-US', {style: 'currency', currency: 'USD'});
  });
});
</script>
<script src=\"/free-utility-lab/accessibility-widget.js?v=8ec7e2e\" defer></script>
<script src=\"/free-utility-lab/free-utility-lab-tracking.js\" defer></script>
<script src=\"/free-utility-lab/free-utility-lab-measurement-bridge.js\" defer></script>"""


def render_main() -> str:
    canonical = BASE_URL + "aistackcost/"
    return f"""<!doctype html>
<html lang=\"en\">
{head('AIStackCost Free AI Stack Cost Planner', 'Compare free and paid AI tools, choose stack presets, and estimate approximate monthly subscription cost without unsupported pricing claims.', canonical)}
<body data-asset-id=\"aistackcost\" data-goal=\"aistackcost-upgrade\">
<header class=\"ful-marketplace-hero\">{nav()}<p class=\"ful-eyebrow\">AIStackCost modular planner</p><h1>Build an AI stack without wasting subscription budget</h1><p class=\"ful-hero-copy\">Compare assistants, presets, and recurring subscription risk before paying for another AI tool.</p><div class=\"ful-badges\"><span class=\"ful-badge\">Free</span><span class=\"ful-badge\">No signup</span><span class=\"ful-badge\">CSV</span><span class=\"ful-badge\">Print</span></div></header>
<main class=\"ful-marketplace-shell\">
<section class=\"ful-panel\" data-goal=\"aistackcost-upgrade\" id=\"aistackcost-result\" aria-labelledby=\"goal7-title\">
  <h2 id=\"goal7-title\">Approximate monthly cost calculator</h2>
  <p>Enter current planning estimates, then remove duplicates. The result is approximate because prices and features change.</p>
  <div class=\"ful-tool-grid\"><label>General AI assistant <input data-price-input type=\"number\" min=\"0\" value=\"0\"></label><label>Design/content tool <input data-price-input type=\"number\" min=\"0\" value=\"0\"></label><label>Automation/workflow tool <input data-price-input type=\"number\" min=\"0\" value=\"0\"></label></div>
  <p data-cost-output>Approximate monthly total: $0.00</p>
  <h3>Freelancer stack preset</h3><p>One general assistant + one design/content tool + one project workspace.</p>
  <h3>Small business stack preset</h3><p>One general assistant + one marketing/design tool + one automation or CRM helper.</p>
  {actions('aistackcost-result', 'Copy AI stack summary', 'Download AI stack CSV', 'Print AI stack plan')}
</section>
{common_sections('aistackcost-result')}
</main>
{scripts()}
</body>
</html>
"""


def render_priority(slug: str, meta: dict[str, str]) -> str:
    canonical = BASE_URL + "aistackcost/" + slug + "/"
    return f"""<!doctype html>
<html lang=\"en\">
{head(meta['title'], meta['intro'], canonical)}
<body data-asset-id=\"aistackcost_{slug.replace('-', '_')}\" data-goal=\"aistackcost-upgrade\">
<header class=\"ful-marketplace-hero\">{nav()}<p class=\"ful-eyebrow\">AIStackCost guide</p><h1>{escape(meta['h1'])}</h1><p class=\"ful-hero-copy\">{escape(meta['intro'])}</p></header>
<main class=\"ful-marketplace-shell\">
<section class=\"ful-panel\" id=\"aistackcost-template\" data-goal=\"aistackcost-upgrade\" aria-labelledby=\"template-title\">
  <h2 id=\"template-title\">Stack preset</h2>
  <p><strong>{escape(meta['preset'])}</strong>: use one primary assistant, one production tool, and one workflow helper before adding duplicate subscriptions.</p>
  <h2>Comparison table</h2>
  <div class=\"ful-table-wrap\"><table><thead><tr><th>Tool</th><th>Best for</th><th>Free option</th><th>Paid plan note</th><th>Official source</th></tr></thead><tbody>{comparison_rows(6)}</tbody></table></div>
  {actions('aistackcost-template', 'Copy template', 'Download CSV', 'Print template')}
</section>
{common_sections('aistackcost-template', compact=True)}
</main>
{scripts()}
</body>
</html>
"""


def main() -> int:
    (ROOT / "aistackcost" / "index.html").write_text(render_main(), encoding="utf-8")
    for slug, meta in PRIORITY_PAGES.items():
        output = ROOT / "aistackcost" / slug / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_priority(slug, meta), encoding="utf-8")
        print(f"rendered {output.relative_to(ROOT)}")
    print("rendered aistackcost/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
