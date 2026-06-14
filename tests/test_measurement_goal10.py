import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_EVENTS = [
    "asset_view",
    "tool_start",
    "tool_complete",
    "copy_click",
    "print_click",
    "download_click",
    "support_page_click",
    "related_tool_click",
    "directory_filter_use",
]
LEGACY_EVENT_NAMES = [
    "calculator_start",
    "calculator_complete",
    "generator_start",
    "generator_complete",
    "result_copy",
    "marketplace_tool_click",
]


def run_node(script: str) -> str:
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def test_goal10_standard_measurement_registry_and_safe_payload_contract():
    output = run_node(
        r'''
        global.window = { dataLayer: [], freeUtilityTrack: function (eventName, payload) { this.dataLayer.push({ eventName, payload }); } };
        const helpers = require('./shared/scripts/utility-actions.js');
        const result = {
          events: helpers.STANDARD_MEASUREMENT_EVENTS,
          normalizedStart: helpers.normalizeMeasurementEvent('calculator_start'),
          normalizedComplete: helpers.normalizeMeasurementEvent('generator_complete'),
          normalizedCopy: helpers.normalizeMeasurementEvent('result_copy'),
          normalizedMarketplace: helpers.normalizeMeasurementEvent('marketplace_tool_click'),
          tracked: helpers.trackSafe('calculator_start', {
            asset_id: 'budgetreset',
            hub: 'tools',
            category: 'finance-tools',
            email: 'person@example.com',
            user_input: 'private budget notes',
            query: 'private search text',
            output: 'calculator'
          }),
          pushed: global.window.dataLayer[0]
        };
        console.log(JSON.stringify(result));
        '''
    )

    import json

    result = json.loads(output)
    assert result["events"] == REQUIRED_EVENTS
    assert result["normalizedStart"] == "tool_start"
    assert result["normalizedComplete"] == "tool_complete"
    assert result["normalizedCopy"] == "copy_click"
    assert result["normalizedMarketplace"] == "related_tool_click"
    assert result["tracked"] == {
        "asset_id": "budgetreset",
        "category": "finance-tools",
        "event": "tool_start",
        "hub": "tools",
        "output": "calculator",
    }
    assert result["pushed"]["eventName"] == "tool_start"
    assert result["pushed"]["payload"]["event"] == "tool_start"
    assert "email" not in result["tracked"]
    assert "user_input" not in result["tracked"]
    assert "query" not in result["tracked"]


def test_measurement_bridge_allows_goal10_events_without_legacy_names():
    bridge = (ROOT / "free-utility-lab-measurement-bridge.js").read_text(encoding="utf-8")
    for event_name in REQUIRED_EVENTS:
        assert event_name in bridge
    for legacy_name in LEGACY_EVENT_NAMES:
        assert legacy_name not in bridge
    assert "allowedEvents" in bridge
    assert "allowedParams" in bridge
    assert "email" not in bridge
    assert "user_input" not in bridge


def test_goal10_sources_emit_standard_events_for_hubs_tools_and_outputs():
    source_files = [
        ROOT / "free-utility-lab-tracking.js",
        ROOT / "shared" / "scripts" / "utility-actions.js",
        ROOT / "scripts" / "render_marketplace_pages.py",
        ROOT / "scripts" / "render_aistackcost_goal7.py",
        ROOT / "budgetreset" / "index.html",
        ROOT / "mealplansheet" / "index.html",
        ROOT / "movebudget" / "index.html",
        ROOT / "aistackcost" / "index.html",
        ROOT / "tools" / "index.html",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    for event_name in REQUIRED_EVENTS:
        assert event_name in combined
    for legacy_name in LEGACY_EVENT_NAMES:
        assert legacy_name not in combined
    assert "data-filter-control" in (ROOT / "tools" / "index.html").read_text(encoding="utf-8")


def test_goal10_gsc_ga4_review_workflow_is_documented_without_credentials():
    doc = ROOT / "docs" / "MEASUREMENT_GOAL10.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for phrase in [
        "Goal 10 measurement and learning loop",
        "asset_view",
        "tool_start",
        "tool_complete",
        "copy_click",
        "print_click",
        "download_click",
        "support_page_click",
        "related_tool_click",
        "directory_filter_use",
        "indexed or not indexed",
        "impressions",
        "average position",
        "CTR",
        "observed data, not guesses",
        "No credentials are required",
    ]:
        assert phrase in text
    forbidden = ["secrets.", "client" + "_secret", "access" + "_token", "password"]
    assert not any(item in text.lower() for item in forbidden)
