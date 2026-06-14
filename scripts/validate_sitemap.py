#!/usr/bin/env python3
"""Validate that sitemap.xml maps to local static HTML pages."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

BASE_PATH = "/free-utility-lab/"


class SitemapValidationResult:
    def __init__(self, errors: list[str], url_count: int, local_html_count: int) -> None:
        self.errors = errors
        self.url_count = url_count
        self.local_html_count = local_html_count

    @property
    def ok(self) -> bool:
        return not self.errors


def _local_path_for_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    if not path.startswith(BASE_PATH):
        return ""
    relative = path[len(BASE_PATH) :]
    if not relative:
        return "index.html"
    if relative.endswith("/"):
        return f"{relative}index.html"
    return relative


def _local_html_files(site_root: Path) -> set[str]:
    ignored_parts = {".git", ".pytest_cache", "tests", "scripts", "docs", "data", "__pycache__"}
    files: set[str] = set()
    for path in site_root.rglob("*.html"):
        relative = path.relative_to(site_root)
        if any(part in ignored_parts for part in relative.parts):
            continue
        files.add(relative.as_posix())
    return files


def _sitemap_urls(sitemap_path: Path) -> list[str]:
    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = []
    for loc in root.iter(f"{namespace}loc"):
        if loc.text:
            urls.append(loc.text.strip())
    if not urls:
        for loc in root.iter("loc"):
            if loc.text:
                urls.append(loc.text.strip())
    return urls


def validate_sitemap(sitemap_path: Path | str, site_root: Path | str = Path(".")) -> SitemapValidationResult:
    sitemap_path = Path(sitemap_path)
    site_root = Path(site_root)
    errors: list[str] = []

    try:
        urls = _sitemap_urls(sitemap_path)
    except FileNotFoundError:
        return SitemapValidationResult([f"missing sitemap: {sitemap_path}"], 0, len(_local_html_files(site_root)))
    except ET.ParseError as exc:
        return SitemapValidationResult([f"invalid sitemap XML: {exc}"], 0, len(_local_html_files(site_root)))

    if len(urls) != len(set(urls)):
        errors.append("sitemap contains duplicate URLs")

    local_html = _local_html_files(site_root)
    sitemap_local_paths = {_local_path_for_url(url) for url in urls}
    sitemap_local_paths.discard("")

    for url in urls:
        local_path = _local_path_for_url(url)
        if not local_path:
            errors.append(f"URL outside current base path: {url}")
            continue
        if local_path not in local_html:
            errors.append(f"missing local html for sitemap URL: {url} -> {local_path}")

    missing_from_sitemap = sorted(local_html - sitemap_local_paths)
    if missing_from_sitemap:
        sample = ", ".join(missing_from_sitemap[:10])
        errors.append(f"local HTML missing from sitemap ({len(missing_from_sitemap)}): {sample}")

    return SitemapValidationResult(errors=errors, url_count=len(urls), local_html_count=len(local_html))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sitemap.xml against local HTML files.")
    parser.add_argument("sitemap", nargs="?", default="sitemap.xml")
    parser.add_argument("--site-root", default=".")
    args = parser.parse_args()
    result = validate_sitemap(args.sitemap, site_root=args.site_root)
    if not result.ok:
        for error in result.errors:
            print(error)
        return 1
    print(f"Sitemap OK: {result.url_count} URLs, {result.local_html_count} local HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
