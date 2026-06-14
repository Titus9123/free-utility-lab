from pathlib import Path

from scripts.validate_final_launch_readiness import validate_final_launch_readiness

ROOT = Path(__file__).resolve().parents[1]


def test_goal13_final_launch_readiness_docs_and_contract_exist_without_cutover():
    contract = ROOT / "data" / "final_launch_readiness.json"
    doc = ROOT / "docs" / "FINAL_LAUNCH_READINESS_GOAL13.md"

    assert contract.exists(), "Goal 13 must add a machine-checkable final readiness contract"
    assert doc.exists(), "Goal 13 must document the final operator handoff"
    assert not (ROOT / "CNAME").exists(), "Goal 13 must not perform custom-domain cutover"

    text = doc.read_text(encoding="utf-8")
    required_phrases = [
        "Goal 13 final launch readiness",
        "operator handoff",
        "no cutover was performed",
        "quality gates",
        "domain migration remains approval-gated",
        "asset factory remains the expansion path",
        "measurement loop",
        "CI gates",
        "Docker validation",
        "post-launch operating cadence",
        "do not activate live ads yet",
        "python3 scripts/validate_final_launch_readiness.py",
    ]
    for phrase in required_phrases:
        assert phrase in text

    forbidden = ["client" + "_secret", "access" + "_token", "password" + ":", "secrets."]
    assert not any(item in text.lower() for item in forbidden)


def test_goal13_validator_confirms_all_prior_readiness_gates_are_wired():
    result = validate_final_launch_readiness(ROOT)

    assert result.ok, result.errors
    assert result.completed_goal_count >= 13
    assert result.required_gate_count >= 9
    assert result.current_base == "https://titus9123.github.io/free-utility-lab/"
    assert result.target_domain == "freeutilitylab.com"
    assert "domain_migration_approval_required" in result.blockers
    assert "live_ads_not_activated" in result.blockers


def test_goal13_final_readiness_keeps_live_domain_and_expansion_guardrails_safe():
    result = validate_final_launch_readiness(ROOT)

    assert result.ok, result.errors
    assert result.cutover_performed is False
    assert result.live_ads_enabled is False
    assert "scripts/validate_domain_migration.py" in result.required_files
    assert "scripts/validate_asset_factory.py" in result.required_files
    assert "scripts/run_all_validations.py" in result.required_files