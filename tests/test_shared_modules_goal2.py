import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_node(script: str) -> dict:
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def test_goal2_shared_files_exist():
    expected = [
        ROOT / "shared" / "components" / "marketplace-components.js",
        ROOT / "shared" / "scripts" / "utility-actions.js",
        ROOT / "shared" / "styles" / "marketplace.css",
        ROOT / "shared" / "styles" / "print.css",
        ROOT / "docs" / "SHARED_MODULES_GOAL2.md",
    ]

    missing = [str(path.relative_to(ROOT)) for path in expected if not path.exists()]

    assert not missing


def test_tool_card_component_renders_required_marketplace_ux():
    result = run_node(
        r'''
        const { renderToolCard, renderBadgeList } = require('./shared/components/marketplace-components.js');
        const asset = {
          id: 'budgetreset',
          name: 'BudgetReset',
          intent: 'Free monthly budget planner and bill calendar.',
          public_url: 'https://titus9123.github.io/free-utility-lab/budgetreset/',
          category: 'finance-tools',
          formats: ['calculator', 'worksheet'],
          outputs: ['copy', 'csv', 'print'],
          user_types: ['households', 'students'],
          tracking_asset_id: 'budgetreset'
        };
        const html = renderToolCard(asset, { basePath: '/free-utility-lab/' });
        const badges = renderBadgeList(['free', 'no_signup', 'print']);
        console.log(JSON.stringify({ html, badges }));
        '''
    )

    html = result["html"]
    assert 'data-asset-id="budgetreset"' in html
    assert 'href="/free-utility-lab/budgetreset/"' in html
    assert "Free" in html
    assert "No signup" in html
    assert "Copy" in html
    assert "CSV" in html
    assert "Print" in html
    assert 'data-event="marketplace_tool_click"' in html
    assert "finance-tools" in html
    assert result["badges"].count('class="ful-badge"') == 3


def test_export_helpers_copy_csv_filter_and_print_are_deterministic():
    result = run_node(
        r'''
        const helpers = require('./shared/scripts/utility-actions.js');
        const rows = [
          ['Item', 'Cost', 'Note'],
          ['Rent, June', 1200, 'fixed'],
          ['Groceries', 86.5, 'weekly "estimate"']
        ];
        const csv = helpers.tableToCsv(rows);
        const filtered = helpers.filterMarketplaceItems([
          { id: 'a', category: 'finance-tools', formats: ['calculator'], outputs: ['csv'], user_types: ['households'] },
          { id: 'b', category: 'ai-tools', formats: ['comparison'], outputs: ['external_link'], user_types: ['freelancers'] }
        ], { category: 'finance-tools', format: 'calculator', output: 'csv', userType: 'households' }).map(item => item.id);
        const printMarkup = helpers.createPrintSectionMarkup('worksheet', '<h2>Worksheet</h2>');
        console.log(JSON.stringify({ csv, filtered, printMarkup }));
        '''
    )

    assert result["csv"] == 'Item,Cost,Note\r\n"Rent, June",1200,fixed\r\nGroceries,86.5,"weekly ""estimate"""'
    assert result["filtered"] == ["a"]
    assert 'data-print-section="worksheet"' in result["printMarkup"]


def test_safe_tracking_never_emits_private_user_input():
    result = run_node(
        r'''
        const { sanitizeTrackingPayload } = require('./shared/scripts/utility-actions.js');
        const payload = sanitizeTrackingPayload({
          asset_id: 'budgetreset',
          event: 'copy_click',
          amount: 123,
          email: 'person@example.com',
          user_input: 'my rent is 1200',
          freeform_text: 'private note',
          token: 'abc123',
          nested: { ['pass' + 'word']: 'bad', safe: 'ok' },
          outputs: ['copy', 'print']
        });
        console.log(JSON.stringify(payload));
        '''
    )

    assert result == {
        "asset_id": "budgetreset",
        "event": "copy_click",
        "amount": 123,
        "outputs": ["copy", "print"],
    }


def test_shared_modules_are_only_wired_into_approved_marketplace_pages():
    html_files = [path for path in ROOT.rglob("*.html") if ".git" not in path.parts]
    allowed = {
        ROOT / "tools" / "index.html",
        ROOT / "printable-templates" / "index.html",
        ROOT / "finance-tools" / "index.html",
        ROOT / "meal-planning-tools" / "index.html",
        ROOT / "moving-tools" / "index.html",
        ROOT / "ai-tools" / "index.html",
        ROOT / "budgetreset" / "index.html",
        ROOT / "mealplansheet" / "index.html",
        ROOT / "mealplansheet" / "grocery-list-template-free-editable" / "index.html",
        ROOT / "mealplansheet" / "weekly-meal-planner-printable" / "index.html",
        ROOT / "mealplansheet" / "grocery-list-template" / "index.html",
        ROOT / "mealplansheet" / "printable-grocery-list-by-category" / "index.html",
        ROOT / "mealplansheet" / "family-grocery-budget-planner" / "index.html",
        ROOT / "mealplansheet" / "cheap-weekly-meal-plan" / "index.html",
        ROOT / "mealplansheet" / "student-meal-planner" / "index.html",
        ROOT / "mealplansheet" / "no-cook-meal-plan" / "index.html",
    }
    shared_references = []
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "shared/scripts/utility-actions.js" in text or "shared/styles/marketplace.css" in text:
            shared_references.append(path)

    assert set(shared_references) == allowed
