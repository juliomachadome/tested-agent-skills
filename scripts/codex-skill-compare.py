#!/usr/bin/env python3
"""Compare synthetic Codex fixtures. Dry-run by default; never save raw traces."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FLAGS = (
    "--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox", "read-only",
    "--skip-git-repo-check", "--disable", "plugins", "--enable", "skip_host_skill_discovery",
    "-c", 'web_search="disabled"', "--json",
)
COMMON = "Use only the synthetic data supplied. Do not access the network, connectors, credentials or files outside the temporary project."


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture(path: Path) -> dict:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be a JSON object")
    for key in ("id", "skill"):
        if not isinstance(fixture.get(key), str) or not FIXTURE_NAME.fullmatch(fixture[key]):
            raise ValueError(f"fixture {key} must be a lowercase slug")
    if not isinstance(fixture.get("prompt"), str) or not fixture["prompt"].strip():
        raise ValueError("fixture prompt is required")
    expected = fixture.get("expected_fields", {})
    if not isinstance(expected, dict):
        raise ValueError("expected_fields must be a JSON object")
    return fixture


def prepare(project: Path, source: Path, fixture: dict, condition: str, discovery: str) -> tuple[str, Path | None]:
    task = COMMON + "\n\n" + fixture["prompt"].strip()
    if condition == "without":
        return task, None
    if discovery == "explicit":
        content = (source / "SKILL.md").read_text(encoding="utf-8")
        return f"<reference_skill>\n{content}\n</reference_skill>\n\n{task}", None
    target = project / ".agents" / "skills" / fixture["skill"]
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("evals", "__pycache__", "*.pyc"))
    skill_file = target / "SKILL.md"
    if discovery == "forced":
        (project / "AGENTS.md").write_text(
            f"Read .agents/skills/{fixture['skill']}/SKILL.md before answering.\n", encoding="utf-8"
        )
    return task, skill_file


def parse_output(stdout: str, target: Path | None) -> tuple[str, dict]:
    answer, usage, tool_calls = "", None, 0
    completed = read_observed = False
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "turn.completed":
            completed = True
            fields = event.get("usage") or {}
            usage = {
                k: fields[k] for k in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
                if type(fields.get(k)) is int
            }
        if event.get("type") != "item.completed":
            continue
        item = event.get("item") or {}
        kind = item.get("type")
        if kind == "agent_message":
            answer = item.get("text") or ""
        elif kind in {"command_execution", "mcp_tool_call", "web_search", "file_change", "collab_tool_call"}:
            tool_calls += 1
        if target is not None and kind == "command_execution" and item.get("exit_code") == 0:
            relative = f".agents/skills/{target.parent.name}/{target.name}"
            command = item.get("command") or ""
            excerpt = item.get("aggregated_output") or ""
            paths = "|".join(re.escape(path) for path in (str(target), relative, "./" + relative))
            if re.search(r"(?:^|[\s\"'])(" + paths + r")(?=$|[\s\"';])", command) and re.search(
                r"(?m)^name:\s*" + re.escape(target.parent.name) + r"\s*$", excerpt
            ):
                read_observed = True
    return answer, {
        "turn_completed": completed,
        "usage": usage,
        "tool_calls_observed": tool_calls,
        "project_file_read": ("observed" if read_observed else "not_observed") if target is not None else None,
    }


def evaluate(answer: str, expected: dict) -> dict[str, bool] | None:
    if not expected:
        return None
    try:
        value = json.loads(answer)
    except json.JSONDecodeError:
        return dict.fromkeys(expected, False)
    if not isinstance(value, dict):
        return dict.fromkeys(expected, False)
    return {
        key: key in value and json.dumps(value[key], sort_keys=True) == json.dumps(expected_value, sort_keys=True)
        for key, expected_value in expected.items()
    }


def private_batch(parent: Path) -> Path:
    path = parent.resolve()
    if any((candidate / ".git").exists() for candidate in (path, *path.parents)):
        raise ValueError("answer directory must be outside Git checkouts")
    if not path.is_dir():
        raise ValueError("answer directory must already exist and be private")
    return Path(tempfile.mkdtemp(prefix="blind-answers-", dir=path))


def write_answer(path: Path, answer: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(answer + "\n")


def invoke(fixture: dict, source: Path, condition: str, args: argparse.Namespace) -> tuple[str, dict]:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="codex-skill-compare-") as folder:
        project = Path(folder)
        task, target = prepare(project, source, fixture, condition, args.discovery)
        command = ["codex", "exec", *FLAGS, "-m", args.model, "-C", folder, "-"]
        try:
            run = subprocess.run(command, input=task, text=True, capture_output=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            return "", {"status": "timeout", "elapsed_seconds": round(time.monotonic() - started, 2)}
    answer, evidence = parse_output(run.stdout, target)
    valid = run.returncode == 0 and evidence["turn_completed"] and bool(answer.strip())
    return answer if valid else "", {
        **evidence, "exit_code": run.returncode, "elapsed_seconds": round(time.monotonic() - started, 2),
        "status": "completed" if valid else "failed",
        "checks": evaluate(answer, fixture.get("expected_fields", {})) if valid else None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--condition", choices=("paired", "with", "without"), default="paired")
    parser.add_argument("--discovery", choices=("explicit", "natural", "forced"), default="explicit")
    parser.add_argument("--seed", type=int, default=173)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--answers-dir", type=Path, help="Opt in to storing final answers in a private directory outside Git")
    parser.add_argument("--live", action="store_true", help="Call the model; may incur charges")
    args = parser.parse_args(argv)
    try:
        fixture = load_fixture(args.fixture)
        source = ROOT / "skills" / fixture["skill"]
        if not (source / "SKILL.md").is_file():
            raise ValueError("skill does not exist in this checkout")
        if args.timeout <= 0:
            raise ValueError("timeout must be positive")
        order = ["with", "without"] if args.condition == "paired" else [args.condition]
        random.Random(args.seed).shuffle(order)
        batch = private_batch(args.answers_dir) if args.live and args.answers_dir else None
        report = {
            "date": str(date.today()), "fixture_id": fixture["id"], "fixture_sha256": digest(args.fixture),
            "skill": fixture["skill"], "skill_sha256": digest(source / "SKILL.md"),
            "model": args.model, "discovery": args.discovery, "seed": args.seed,
            "mode": "live" if args.live else "dry-run", "condition_order": order,
            "isolation_flags": FLAGS,
        }
        failed = False
        if args.live:
            version = subprocess.run(["codex", "--version"], text=True, capture_output=True, check=True, timeout=10)
            report["harness_version"] = version.stdout.strip()
            report["runs"] = []
            for index, condition in enumerate(order):
                label = "AB"[index]
                answer, evidence = invoke(fixture, source, condition, args)
                failed |= evidence["status"] != "completed"
                if batch is not None and answer:
                    write_answer(batch / f"{label}.txt", answer)
                report["runs"].append({"label": label, "condition": condition, **evidence})
            if batch is not None:
                print(f"Private answers: {batch}", file=sys.stderr)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if failed else 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
