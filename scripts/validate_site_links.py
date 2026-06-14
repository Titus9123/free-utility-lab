#!/usr/bin/env python3
"""Validate local internal links in the static Free Utility Lab HTML site."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

HREF_RE = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)
SRC_RE = re.compile(r"\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
DEFAULT_BASE_PATH = "/free-utility-lab/"


class LinkValidationResult:
    def __init__(self, errors: list[str], files_checked: int) -> None:
        self.errors = errors
        self.files_checked = files_checked

    @property
    def ok(self) -> bool:
        return not self.errors


def _html_files(site_root: Path) -> list[Path]:
    ignored_parts = {".git", ".pytest_cache", "tests", "scripts", "docs", "data", "__pycache__"}
    files = []
    for path in site_root.rglob("*.html"):
        relative = path.relative_to(site_root)
        if any(part in ignored_parts for part in relative.parts):
            continue
        files.append(path)
    return sorted(files)


def _is_ignored_url(url: str) -> bool:
    stripped = url.strip()
    if not stripped or stripped.startswith("#"):
        return True
    if "${" in stripped or "{{" in stripped:
        # Runtime/template-generated URL; static validator cannot resolve it safely.
        return True
    parsed = urlparse(stripped)
    return parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}


def _target_for_url(url: str, page: Path, site_root: Path, base_path: str) -> Path | None:
    parsed = urlparse(url.strip())
    path = parsed.path
    if not path:
        return None
    if path.startswith(base_path):
        relative = path[len(base_path) :]
        relative = relative.lstrip("/")
        if not relative:
            relative = "index.html"
        elif relative.endswith("/"):
            relative = f"{relative}index.html"
        return site_root / relative
    if path.startswith("/"):
        # Root-absolute URL for another site/base path; ignore in this static preview check.
        return None
    relative_target = page.parent / path
    if path.endswith("/"):
        relative_target = relative_target / "index.html"
    return relative_target


def validate_site_links(site_root: Path | str = Path("."), base_path: str = DEFAULT_BASE_PATH) -> LinkValidationResult:
    site_root = Path(site_root)
    errors: list[str] = []
    files = _html_files(site_root)

    for page in files:
        text = page.read_text(encoding="utf-8", errors="ignore")
        urls = [match.group(1) for match in HREF_RE.finditer(text)]
        urls.extend(match.group(1) for match in SRC_RE.finditer(text))
        for url in urls:
            if _is_ignored_url(url):
                continue
            target = _target_for_url(url, page, site_root, base_path)
            if target is None:
                continue
            target_without_fragment = Path(str(target).split("#", 1)[0])
            if not target_without_fragment.exists():
                rel_page = page.relative_to(site_root)
                rel_target = target_without_fragment.relative_to(site_root) if target_without_fragment.is_relative_to(site_root) else target_without_fragment
                errors.append(f"{rel_page}: missing internal link target `{url}` -> `{rel_target}`")

    return LinkValidationResult(errors=errors, files_checked=len(files))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local internal links in HTML files.")
    parser.add_argument("site_root", nargs="?", default=".")
    parser.add_argument("--base-path", default=DEFAULT_BASE_PATH)
    args = parser.parse_args()
    result = validate_site_links(args.site_root, base_path=args.base_path)
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"Site links OK: {result.files_checked} HTML files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
