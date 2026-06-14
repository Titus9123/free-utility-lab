#!/usr/bin/env python3
"""Smoke-check JSON-LD schema blocks in Free Utility Lab HTML pages."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_MARKER = '<script type="application/ld+json">'
SCHEMA_END = "</script>"


@dataclass(frozen=True)
class SchemaSmokeResult:
    checked_pages: int
    checked_blocks: int
    findings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.findings


def iter_html_pages(site_root: Path) -> list[Path]:
    return sorted(
        path
        for path in site_root.rglob("*.html")
        if ".git" not in path.parts and path.is_file()
    )


def extract_schema_blocks(html: str) -> list[str]:
    blocks: list[str] = []
    start = 0
    while True:
        marker_index = html.find(SCHEMA_MARKER, start)
        if marker_index == -1:
            return blocks
        content_start = marker_index + len(SCHEMA_MARKER)
        content_end = html.find(SCHEMA_END, content_start)
        if content_end == -1:
            blocks.append(html[content_start:])
            return blocks
        blocks.append(html[content_start:content_end])
        start = content_end + len(SCHEMA_END)


def validate_schema_smoke(site_root: Path) -> SchemaSmokeResult:
    findings: list[str] = []
    checked_blocks = 0
    pages = iter_html_pages(site_root)

    for page in pages:
        html = page.read_text(encoding="utf-8")
        for block_index, raw_block in enumerate(extract_schema_blocks(html), start=1):
            checked_blocks += 1
            try:
                parsed = json.loads(raw_block.strip())
            except json.JSONDecodeError as exc:
                findings.append(f"{page}:{block_index}: invalid JSON-LD: {exc}")
                continue

            if not isinstance(parsed, dict):
                findings.append(f"{page}:{block_index}: JSON-LD block must be an object")
                continue
            if parsed.get("@context") != "https://schema.org":
                findings.append(f"{page}:{block_index}: missing schema.org @context")
            if not parsed.get("@type"):
                findings.append(f"{page}:{block_index}: missing @type")

    if not pages:
        findings.append(f"{site_root}: no HTML pages found")
    if checked_blocks == 0:
        findings.append(f"{site_root}: no JSON-LD schema blocks found")

    return SchemaSmokeResult(
        checked_pages=len(pages),
        checked_blocks=checked_blocks,
        findings=tuple(findings),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-check JSON-LD schema blocks.")
    parser.add_argument("site_root", nargs="?", default=".", help="Site root to scan")
    args = parser.parse_args()

    result = validate_schema_smoke((ROOT / args.site_root).resolve())
    if not result.ok:
        for finding in result.findings:
            print(finding)
        return 1
    print(f"Schema smoke OK: {result.checked_blocks} JSON-LD blocks across {result.checked_pages} HTML pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
