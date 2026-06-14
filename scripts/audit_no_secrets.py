#!/usr/bin/env python3
"""Small no-secrets scanner for Free Utility Lab modular data/config files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

SECRET_PATTERNS = [
    re.compile(r"\bclient_secret\b", re.IGNORECASE),
    re.compile(r"\baccess_token\b", re.IGNORECASE),
    re.compile(r"\brefresh_token\b", re.IGNORECASE),
    re.compile(r"\bapi[_-]?key\b", re.IGNORECASE),
    re.compile(r"\bpassword\s*[:=]", re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b[A-Za-z0-9_\-]{24,}\.[A-Za-z0-9_\-]{6,}\.[A-Za-z0-9_\-]{20,}\b"),
]

ALLOWLIST_PATTERNS = [
    re.compile(r"do not enter passwords", re.IGNORECASE),
    re.compile(r"secrets or passwords", re.IGNORECASE),
    re.compile(r"no secrets", re.IGNORECASE),
    re.compile(r"secret-looking", re.IGNORECASE),
    # Guardrail blocked-key lists are allowed because they assert that
    # secret-like inputs are stripped; they are not credentials.
    re.compile(r"BLOCKED_TRACKING_KEYS", re.IGNORECASE),
]


class AuditResult:
    def __init__(self, findings: list[str]) -> None:
        self.findings = findings

    @property
    def ok(self) -> bool:
        return not self.findings


def _is_allowlisted(line: str) -> bool:
    return any(pattern.search(line) for pattern in ALLOWLIST_PATTERNS)


def audit_paths(paths: Iterable[Path | str]) -> AuditResult:
    findings: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            candidates = [p for p in path.rglob("*") if p.is_file()]
        else:
            candidates = [path]
        for candidate in candidates:
            if not candidate.exists() or candidate.name.startswith("."):
                continue
            if candidate.name == "audit_no_secrets.py":
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                if _is_allowlisted(line):
                    continue
                for pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        findings.append(f"{candidate}:{line_number}: secret-like pattern `{pattern.pattern}`")
                        break
    return AuditResult(findings=findings)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit files for secret-like values.")
    parser.add_argument("paths", nargs="*", default=["data", "scripts"], help="Files/directories to scan")
    args = parser.parse_args()
    result = audit_paths([Path(p) for p in args.paths])
    if not result.ok:
        for finding in result.findings:
            print(finding)
        return 1
    print("No secret-like values found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
