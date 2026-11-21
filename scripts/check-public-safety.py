#!/usr/bin/env python3
"""Fail a release check when likely private data appears in a text file.

The checker deliberately reports only a rule name and a repository-relative path.
It never prints the matched text, which could itself be sensitive.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".py", ".sh",
    ".toml", ".txt", ".xml", ".yaml", ".yml",
}
PATTERNS = {
    "local-path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
    "personal-email": re.compile(
        r"\b[A-Z0-9._%+-]+@(?:gmail|googlemail|hotmail|outlook|live|icloud|me|protonmail)\.com\b",
        re.IGNORECASE,
    ),
    "credential-marker": re.compile(
        r"(?:"
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
        r"\bgh[opsu]_[A-Za-z0-9_]{20,}\b|"
        r"\bgithub_pat_[A-Za-z0-9_]{20,}\b|"
        r"\bAKIA[0-9A-Z]{16}\b|"
        r"\bsk-[A-Za-z0-9]{20,}\b|"
        r"\b(?:Authorization|Bearer)\s*[:=]?\s*Bearer\s+[A-Za-z0-9._-]{20,}\b"
        r")"
    ),
}


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str


def is_text_file(path: Path) -> bool:
    """Return whether a file is a reasonable text candidate without reading binaries."""
    if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"LICENSE", "Makefile"}:
        return True
    try:
        return b"\0" not in path.read_bytes()[:4096]
    except OSError:
        return False


def scan_tree(root: Path) -> list[Finding]:
    """Scan text files below *root*, returning redacted findings in stable order."""
    root = root.resolve()
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or not is_text_file(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative = path.relative_to(root).as_posix()
        for rule, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append(Finding(rule, relative))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a public release tree for likely private data.")
    parser.add_argument("path", nargs="?", default=".", help="Repository or export directory (default: current directory)")
    args = parser.parse_args(argv)
    root = Path(args.path)
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    findings = scan_tree(root)
    for finding in findings:
        print(f"FAIL [{finding.rule}] {finding.path}")
    if findings:
        print(f"{len(findings)} potential release-safety issue(s) found; matched content was not printed.")
        return 1
    print("PASS no configured private-data markers found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
