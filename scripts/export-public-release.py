#!/usr/bin/env python3
"""Create a filtered source-tree export for a future public repository.

The destination is intentionally not a clone: it has no .git directory and omits
private evaluation material. Create/push a new Git repository only from this tree.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_NAMES = {".git", "__pycache__", ".DS_Store", "CATALOGO.md"}
EXCLUDED_PREFIXES = {
    Path("docs/superpowers"),
    Path("docs/token-diagnosis"),
}
EXCLUDED_FILES = {
    Path("catalog/descriptions.json"),
    Path("catalog/progress.json"),
    Path("catalog/status.json"),
    Path("catalog/template.html"),
    Path("scripts/agent-routing-evals.json"),
    Path("scripts/build-catalog.py"),
    Path("scripts/build-evaluation-summary.py"),
    Path("scripts/build-public-catalog.py"),
    Path("scripts/pilot-arms.py"),
    Path("scripts/pilot-critic.py"),
    Path("scripts/real-output-sweep.py"),
    Path("scripts/skill-eval.py"),
    Path("scripts/skill-vs-none.py"),
    Path("tests/test_build_evaluation_summary.py"),
    Path("tests/test_build_public_catalog.py"),
}


def excluded(relative: Path) -> bool:
    if relative in EXCLUDED_FILES:
        return True
    if any(part in EXCLUDED_NAMES for part in relative.parts):
        return True
    if any(relative == prefix or prefix in relative.parents for prefix in EXCLUDED_PREFIXES):
        return True
    # Historical comparisons contain full answers and task material. The
    # top-level evals/public directory is deliberately synthetic and ships.
    return "evals" in relative.parts and not (len(relative.parts) >= 2 and relative.parts[:2] == ("evals", "public"))


def export_tree(source: Path, destination: Path) -> int:
    source = source.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"destination must be empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    copied = 0
    for file in source.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(source)
        if excluded(relative):
            continue
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)
        copied += 1
    # README and public documentation use release-safe language at the source;
    # no export-time prose rewrite is needed or hidden from reviewers.
    (destination / "PUBLIC_RELEASE.md").write_text(
        "# Public release boundary\n\n"
        "This directory was created by `scripts/export-public-release.py` from a filtered source tree. "
        "It intentionally has no previous Git history and excludes raw evaluation answers, holdouts, internal planning notes and historical PT-BR catalog output. "
        "Before publishing, run `python3 scripts/check-public-safety.py .`, review the files, then initialize a new repository here.\n",
        encoding="utf-8",
    )
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an empty-history, filtered public release directory.")
    parser.add_argument("destination", type=Path, help="New or empty output directory")
    parser.add_argument("--source", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    copied = export_tree(args.source, args.destination)
    print(f"exported={copied} destination={args.destination}")
    print("Next: inspect the export, run the safety check there, then initialize a new Git repository if approved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
