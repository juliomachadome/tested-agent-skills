#!/usr/bin/env python3
"""Print stable IDs and SHA-256 fingerprints for public evaluation fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fingerprints(directory: Path) -> list[dict[str, str]]:
    rows = []
    for path in sorted(directory.glob("*.json")):
        raw = path.read_bytes()
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON fixture: {path.name}") from error
        fixture_id = value.get("id")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            raise ValueError(f"fixture needs a non-empty id: {path.name}")
        rows.append({
            "id": fixture_id,
            "path": path.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
        })
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Identify public evaluation fixtures by content hash.")
    parser.add_argument("directory", nargs="?", type=Path, default=ROOT / "evals" / "public")
    args = parser.parse_args(argv)
    print(json.dumps(fingerprints(args.directory), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
