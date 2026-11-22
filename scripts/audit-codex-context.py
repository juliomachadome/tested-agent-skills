#!/usr/bin/env python3
"""Audit local Codex prompt assembly with a synthetic user-skill canary."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


CANARY = "synthetic-skill-isolation-canary"
TASK = "Synthetic context audit marker. Reply with OK."
TREATMENT = "<reference_skill>\nSynthetic treatment marker.\n</reference_skill>\n\n"
FLAGS = (
    "--disable", "plugins",
    "-c", 'web_search="disabled"',
)


def context(folder: Path, prompt: str, *, skip_host_skills: bool) -> str:
    flags = ("--enable", "skip_host_skill_discovery") if skip_host_skills else ()
    result = subprocess.run(
        ["codex", "debug", "prompt-input", *FLAGS, *flags, prompt],
        cwd=folder, text=True, capture_output=True, timeout=60, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Codex prompt inspection failed with exit {result.returncode}")
    return json.dumps(json.loads(result.stdout), ensure_ascii=False)


def main() -> None:
    if os.environ.get("RUNNER_ENVIRONMENT") != "github-hosted":
        raise RuntimeError("Run the synthetic discovery canary on a fresh GitHub-hosted runner")
    home = Path.home()
    skill = home / ".agents" / "skills" / CANARY
    skill.mkdir(parents=True)
    try:
        (skill / "SKILL.md").write_text(
            f"---\nname: {CANARY}\ndescription: Synthetic discovery marker for CI.\n---\n\nCanary only.\n",
            encoding="utf-8",
        )
        with tempfile.TemporaryDirectory(prefix="codex-context-audit-") as temp:
            project = Path(temp)
            assert not list(project.iterdir()), "The audit project must start empty"
            positive = context(project, TASK, skip_host_skills=False)
            control = context(project, TASK, skip_host_skills=True)
            treatment = context(project, TREATMENT + TASK, skip_host_skills=True)
    finally:
        (skill / "SKILL.md").unlink(missing_ok=True)
        skill.rmdir()

    assert CANARY in positive, "The discovery canary was not visible with default discovery"
    for kind, assembled in (("control", control), ("treatment", treatment)):
        assert TASK in assembled, f"{kind}: the user prompt marker was missing"
        assert CANARY not in assembled, f"{kind}: the user skill leaked into the visible prompt"
    assert "Synthetic treatment marker." not in control, "The treatment leaked into the control"
    assert "Synthetic treatment marker." in treatment, "The treatment marker was missing"

    print(json.dumps({
        "user_skill_discovery_detected_in_positive_control": True,
        "user_skill_discovery_detected_in_isolated_control": False,
        "user_skill_discovery_detected_in_isolated_treatment": False,
        "treatment_marker_present_only_in_treatment": True,
        "model_calls": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
