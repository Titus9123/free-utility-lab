import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "audit_no_secrets.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("audit_no_secrets", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_secrets_audit_flags_secret_like_text(tmp_path):
    validator = load_validator()
    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{"client' + '_secret": "abc123"}', encoding="utf-8")

    result = validator.audit_paths([bad_file])

    assert not result.ok
    assert any("client" + "_secret" in finding for finding in result.findings)


def test_no_secrets_audit_accepts_safe_catalog_language(tmp_path):
    validator = load_validator()
    safe_file = tmp_path / "safe.json"
    safe_file.write_text('{"name": "BudgetReset", "status": "live"}', encoding="utf-8")

    result = validator.audit_paths([safe_file])

    assert result.ok, result.findings
