#!/usr/bin/env python3
"""Validate Goal 11 custom-domain migration readiness without performing cutover."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

CURRENT_BASE = "https://titus9123.github.io/free-utility-lab/"
BASE_PATH = "/free-utility-lab/"
CONFIG_PATH = Path("data/domain_migration.json")
DOC_PATH = Path("docs/DOMAIN_MIGRATION_GOAL11.md")
SITEMAP_PATH = Path("sitemap.xml")
CANONICAL_RE = re.compile(r"<link\s+rel=[\"']canonical[\"']\s+href=[\"']([^\"']+)[\"']", re.IGNORECASE)
OG_URL_RE = re.compile(r"<meta\s+property=[\"']og:url[\"']\s+content=[\"']([^\"']+)[\"']", re.IGNORECASE)


@dataclass(frozen=True)
class DomainMigrationValidationResult:
    errors: list[str]
    html_count: int
    sitemap_url_count: int
    current_base: str
    target_base: str
    selected_custom_domain: str
    base_path: str

    @property
    def ok(self) -> bool:
        return not self.errors


def _site_html_files(site_root: Path) -> list[Path]:
    ignored_parts = {".git", ".pytest_cache", "tests", "scripts", "docs", "data", "__pycache__"}
    files: list[Path] = []
    for path in site_root.rglob("*.html"):
        relative = path.relative_to(site_root)
        if any(part in ignored_parts for part in relative.parts):
            continue
        files.append(path)
    return sorted(files)


def _urls_from_sitemap(sitemap_path: Path) -> list[str]:
    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [loc.text.strip() for loc in root.iter(f"{namespace}loc") if loc.text]
    if not urls:
        urls = [loc.text.strip() for loc in root.iter("loc") if loc.text]
    return urls


def _load_config(config_path: Path) -> tuple[dict[str, object], list[str]]:
    try:
        raw = config_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}, [f"missing domain migration config: {config_path}"]
    try:
        config = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {}, [f"invalid domain migration config JSON: {exc}"]
    if not isinstance(config, dict):
        return {}, ["domain migration config must be a JSON object"]
    return config, []


def _target_base_for_domain(domain: str) -> str:
    return f"https://{domain.strip().strip('/')}/"


def validate_domain_migration_readiness(site_root: Path | str = Path(".")) -> DomainMigrationValidationResult:
    site_root = Path(site_root)
    errors: list[str] = []
    config, config_errors = _load_config(site_root / CONFIG_PATH)
    errors.extend(config_errors)

    selected_domain = str(config.get("selected_custom_domain", "")) if config else ""
    current_base = str(config.get("current_canonical_base", "")) if config else ""
    target_base = str(config.get("target_canonical_base", "")) if config else ""
    base_path = str(config.get("base_path", "")) if config else ""

    expected_target = _target_base_for_domain(selected_domain) if selected_domain else ""
    if selected_domain != "freeutilitylab.com":
        errors.append("selected_custom_domain must be freeutilitylab.com")
    if current_base != CURRENT_BASE:
        errors.append(f"current_canonical_base must be {CURRENT_BASE}")
    if target_base != expected_target:
        errors.append("target_canonical_base must match selected_custom_domain")
    if base_path != BASE_PATH:
        errors.append(f"base_path must remain {BASE_PATH} until cutover")

    required_lists = [
        "canonical_rewrite_plan",
        "sitemap_url_rewrite_plan",
        "redirect_strategy",
        "gsc_new_property_checklist",
        "ga4_continuity_check",
        "post_migration_crawl_validation",
    ]
    for key in required_lists:
        value = config.get(key) if config else None
        if not isinstance(value, list) or not value:
            errors.append(f"{key} must be a non-empty list")

    if (site_root / "CNAME").exists():
        errors.append("CNAME exists; Goal 11 readiness must not perform domain cutover")

    doc_path = site_root / DOC_PATH
    if not doc_path.exists():
        errors.append(f"missing domain migration runbook: {doc_path}")

    html_files = _site_html_files(site_root)
    sitemap_urls: list[str] = []
    try:
        sitemap_urls = _urls_from_sitemap(site_root / SITEMAP_PATH)
    except FileNotFoundError:
        errors.append("missing sitemap.xml")
    except ET.ParseError as exc:
        errors.append(f"invalid sitemap XML: {exc}")

    if sitemap_urls and len(sitemap_urls) != len(html_files):
        errors.append(f"sitemap URL count ({len(sitemap_urls)}) does not match HTML inventory ({len(html_files)})")
    for url in sitemap_urls:
        if not url.startswith(CURRENT_BASE):
            errors.append(f"sitemap URL outside current canonical base: {url}")
        if target_base and url.startswith(target_base):
            errors.append(f"sitemap already uses target domain before final cutover: {url}")

    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8", errors="ignore")
        relative = html_file.relative_to(site_root)
        for url in CANONICAL_RE.findall(text) + OG_URL_RE.findall(text):
            if url.startswith(target_base) and target_base:
                errors.append(f"{relative}: target domain present before final cutover")
            if not url.startswith(CURRENT_BASE):
                parsed = urlparse(url)
                if parsed.scheme in {"http", "https"}:
                    errors.append(f"{relative}: canonical/social URL outside current base: {url}")

    return DomainMigrationValidationResult(
        errors=errors,
        html_count=len(html_files),
        sitemap_url_count=len(sitemap_urls),
        current_base=current_base,
        target_base=target_base,
        selected_custom_domain=selected_domain,
        base_path=base_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goal 11 domain migration readiness without cutover.")
    parser.add_argument("site_root", nargs="?", default=".")
    args = parser.parse_args()
    result = validate_domain_migration_readiness(args.site_root)
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(
        "Domain migration readiness OK: "
        f"{result.html_count} HTML files, {result.sitemap_url_count} sitemap URLs, "
        f"target {result.target_base}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
