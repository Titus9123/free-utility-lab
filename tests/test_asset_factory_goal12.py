from pathlib import Path

from scripts.validate_asset_factory import validate_asset_factory

ROOT = Path(__file__).resolve().parents[1]


def test_goal12_asset_factory_docs_define_repeatable_workflow_without_page_cloning():
    guide = ROOT / "docs" / "ASSET_FACTORY_GOAL12.md"
    spec = ROOT / "data" / "asset_factory_checklist.json"

    assert guide.exists(), "Goal 12 must document the repeatable new-asset workflow"
    assert spec.exists(), "Goal 12 must add a machine-checkable asset factory checklist"

    guide_text = guide.read_text(encoding="utf-8")
    required_phrases = [
        "Goal 12 ongoing asset factory",
        "repeatable workflow",
        "do not clone existing pages manually",
        "catalog entry",
        "main product page",
        "category hub inclusion",
        "real tool/template/checklist/calculator",
        "copy/print/export outputs",
        "schema",
        "tracking",
        "internal links",
        "validation pass",
        "no secrets",
        "no thin support pages",
        "python3 scripts/validate_new_asset.py",
    ]
    for phrase in required_phrases:
        assert phrase in guide_text

    forbidden = ["client" + "_secret", "access" + "_token", "password" + ":", "secrets."]
    assert not any(item in guide_text.lower() for item in forbidden)


def test_goal12_asset_factory_validator_enforces_new_asset_contract():
    result = validate_asset_factory(ROOT)

    assert result.ok, result.errors
    assert result.check_count >= 10
    assert "catalog_entry" in result.check_ids
    assert "main_product_page" in result.check_ids
    assert "category_hub_inclusion" in result.check_ids
    assert "usable_asset" in result.check_ids
    assert "outputs" in result.check_ids
    assert "schema" in result.check_ids
    assert "tracking" in result.check_ids
    assert "internal_links" in result.check_ids
    assert "validation_pass" in result.check_ids
    assert "no_secrets" in result.check_ids
    assert "no_thin_support_pages" in result.check_ids


def test_goal12_new_asset_validator_rejects_incomplete_manifest(tmp_path):
    manifest = tmp_path / "new_asset.json"
    manifest.write_text(
        '{"id":"thinasset","name":"Thin Asset","slug":"thinasset","category":"finance-tools"}',
        encoding="utf-8",
    )

    result = validate_asset_factory(ROOT, manifest_path=manifest)

    assert not result.ok
    assert any("new_asset" in error for error in result.errors)
    assert any("missing required field" in error for error in result.errors)
