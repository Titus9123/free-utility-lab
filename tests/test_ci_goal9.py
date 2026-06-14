from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-free-utility-lab.yml"
README = ROOT / "README.md"


def test_goal9_ci_workflow_runs_quality_gates_without_credentials():
    assert WORKFLOW.exists(), "Goal 9 must add a GitHub Actions validation workflow"

    workflow_text = WORKFLOW.read_text(encoding="utf-8")

    assert "Validate Free Utility Lab" in workflow_text
    assert "pull_request:" in workflow_text
    assert "push:" in workflow_text
    assert "python3 -m pytest -q" in workflow_text
    assert "python3 scripts/run_all_validations.py" in workflow_text
    assert "python3 scripts/validate_schema_smoke.py" in workflow_text
    assert "docker compose config" in workflow_text
    assert "docker compose build" in workflow_text
    assert "find . -name 'index.html'" in workflow_text
    assert "HTML page count" in workflow_text
    assert "permissions:" in workflow_text
    assert "contents: read" in workflow_text

    for forbidden in (
        "secrets.",
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "/root/.hermes",
        "/root/.codex",
        "/root/.claude",
        "auth.json",
        "client" + "_secret",
        "access" + "_token",
    ):
        assert forbidden not in workflow_text


def test_goal9_local_and_ci_commands_are_documented():
    readme_text = README.read_text(encoding="utf-8")

    assert "Quality gates" in readme_text
    assert "python3 scripts/run_all_validations.py" in readme_text
    assert "docker compose config" in readme_text
    assert "docker compose build" in readme_text
    assert ".github/workflows/validate-free-utility-lab.yml" in readme_text
