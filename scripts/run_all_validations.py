#!/usr/bin/env python3
"""Run the complete Free Utility Lab validation bundle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATION_COMMANDS = [
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "scripts/validate_marketplace_catalog.py"],
    [sys.executable, "scripts/validate_shared_modules.py"],
    [sys.executable, "scripts/validate_site_links.py", ".", "--base-path", "/free-utility-lab/"],
    [sys.executable, "scripts/validate_sitemap.py", "sitemap.xml", "--site-root", "."],
    [sys.executable, "scripts/validate_schema_smoke.py"],
    [sys.executable, "scripts/validate_domain_migration.py"],
    [
        sys.executable,
        "scripts/audit_no_secrets.py",
        "data",
        "scripts",
        "shared",
        "docs",
        "tests",
        "free-utility-lab-tracking.js",
        "free-utility-lab-measurement-bridge.js",
        "Dockerfile",
        "docker-compose.yml",
        ".github/workflows/validate-free-utility-lab.yml",
    ],
]


def run_all() -> int:
    for command in VALIDATION_COMMANDS:
        print(f"$ {' '.join(command)}", flush=True)
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def main() -> int:
    return run_all()


if __name__ == "__main__":
    raise SystemExit(main())
