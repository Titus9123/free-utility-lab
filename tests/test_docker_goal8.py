from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_goal8_docker_files_define_reproducible_validation_and_preview():
    dockerfile = ROOT / "Dockerfile"
    compose = ROOT / "docker-compose.yml"
    dockerignore = ROOT / ".dockerignore"
    runner = ROOT / "scripts" / "run_all_validations.py"

    missing = [path.name for path in (dockerfile, compose, dockerignore, runner) if not path.exists()]
    assert not missing

    dockerfile_text = dockerfile.read_text(encoding="utf-8")
    compose_text = compose.read_text(encoding="utf-8")
    dockerignore_text = dockerignore.read_text(encoding="utf-8")
    runner_text = runner.read_text(encoding="utf-8")

    assert "python:" in dockerfile_text
    assert "WORKDIR /site" in dockerfile_text
    assert "COPY . /site" in dockerfile_text
    assert "validate:" in compose_text
    assert "preview:" in compose_text
    assert "python3 scripts/run_all_validations.py" in compose_text
    assert "python3 -m http.server 8080" in compose_text
    assert "8080:8080" in compose_text
    assert "validate_marketplace_catalog.py" in runner_text
    assert "validate_shared_modules.py" in runner_text
    assert "validate_site_links.py" in runner_text
    assert "validate_sitemap.py" in runner_text
    assert "audit_no_secrets.py" in runner_text

    for forbidden in (
        "/root/.hermes",
        "/root/.codex",
        "/root/.claude",
        "id_rsa",
        "auth.json",
        "client" + "_secret",
        "access" + "_token",
    ):
        assert forbidden not in dockerfile_text
        assert forbidden not in compose_text

    for required_ignore in (
        ".git",
        ".env",
        "*.pem",
        "*.key",
        "__pycache__/",
        ".pytest_cache/",
        "node_modules/",
    ):
        assert required_ignore in dockerignore_text
