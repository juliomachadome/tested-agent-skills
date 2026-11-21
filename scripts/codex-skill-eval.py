#!/usr/bin/env python3
"""Run a synthetic Codex skill smoke test without loading user configuration.

Live execution is opt-in because it can call a model provider. Saved reports contain
metadata only; the model's response and raw JSONL are never written by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_fixture(path: Path) -> dict:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    missing = [key for key in ("id", "skill", "prompt") if not isinstance(fixture.get(key), str) or not fixture[key].strip()]
    if missing:
        raise ValueError(f"fixture missing non-empty fields: {', '.join(missing)}")
    return fixture


def prepare_workspace(project: Path, fixture_path: Path, skills_root: Path) -> dict:
    """Copy exactly one skill, excluding evals, into an otherwise fresh project."""
    fixture = load_fixture(fixture_path)
    source = skills_root / fixture["skill"]
    skill_file = source / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError(f"skill not found: {fixture['skill']}")
    destination = project / ".agents" / "skills" / fixture["skill"]
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("evals", "__pycache__", "*.pyc"))
    # Codex recognizes the shared Agent Skills layout. AGENTS.md makes the
    # smoke-test intent explicit without copying fixture data or answer keys.
    (project / "AGENTS.md").write_text(
        f"For this synthetic smoke test, read the `{fixture['skill']}` skill from `.agents/skills/` before answering. "
        "Do not use network tools, connectors, credentials, or files outside this temporary project.\n",
        encoding="utf-8",
    )
    return fixture


def build_command(project: Path, prompt: str) -> list[str]:
    return [
        "codex", "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--sandbox", "read-only",
        "--json",
        "-C", str(project),
        prompt,
    ]


def parse_jsonl(output: str) -> dict:
    """Return only redacted execution metadata from Codex JSONL output."""
    events = 0
    thread_started = False
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        events += 1
        if event.get("type") == "thread.started":
            thread_started = True
    return {"events": events, "thread_started": thread_started}


def report(fixture: dict, fixture_path: Path, completed: subprocess.CompletedProcess[str] | None = None) -> dict:
    result = {
        "fixture_id": fixture["id"],
        "fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        "skill": fixture["skill"],
        "date": str(date.today()),
        "harness": "codex-cli",
        "isolation": ["--ephemeral", "--ignore-user-config", "--sandbox read-only"],
    }
    if completed is None:
        result["mode"] = "dry-run"
        result["live_execution"] = False
    else:
        result.update(parse_jsonl(completed.stdout))
        result["mode"] = "live"
        result["live_execution"] = True
        result["exit_code"] = completed.returncode
        result["passed"] = completed.returncode == 0
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an isolated synthetic Codex skill smoke test.")
    parser.add_argument("--fixture", type=Path, required=True, help="Synthetic public fixture JSON")
    parser.add_argument("--skills-root", type=Path, default=ROOT / "skills")
    parser.add_argument("--output", type=Path, help="Optional redacted metadata JSON output")
    parser.add_argument("--live", action="store_true", help="Actually call Codex (may incur provider charges)")
    args = parser.parse_args(argv)

    with tempfile.TemporaryDirectory(prefix="codex-skill-eval-") as temporary:
        project = Path(temporary) / "project"
        fixture = prepare_workspace(project, args.fixture, args.skills_root)
        command = build_command(project, fixture["prompt"])
        if args.live:
            completed = subprocess.run(command, text=True, capture_output=True, timeout=300, check=False)
            result = report(fixture, args.fixture, completed)
        else:
            result = report(fixture, args.fixture)
            result["command"] = [
                "codex", "exec", "--ephemeral", "--ignore-user-config", "--sandbox", "read-only", "--json",
                "-C", "<temporary isolated project>", "<synthetic prompt>",
            ]
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if not args.live or result["passed"] else result["exit_code"] or 1


if __name__ == "__main__":
    raise SystemExit(main())
