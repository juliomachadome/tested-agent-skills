#!/usr/bin/env python3
"""Print a portable agent role as compact context for Codex or a raw model.

Usage: scripts/role-to-prompt.py <role>
       scripts/role-to-prompt.py <role> --with-skills
       scripts/role-to-prompt.py --list

Without --with-skills, install the role's skills in the target harness and let its
normal skill discovery load them. --with-skills appends only the core SKILL.md
files for a standalone prompt; it never appends reference trees.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "agent-profiles"
SKILLS = ROOT / "skills"


def role_names() -> list[str]:
    return sorted(path.stem for path in PROFILES.glob("*.md") if path.name != "README.md")


def profile_path(role: str) -> Path:
    path = PROFILES / f"{role}.md"
    if role not in role_names() or not path.is_file():
        raise ValueError(f"no role named {role} (try --list)")
    return path


def portable_profile(role: str) -> str:
    """Drop the host-specific mapping: it adds tokens and is not an instruction."""
    text = profile_path(role).read_text(encoding="utf-8").strip()
    return text.split("\n## Claude Code mapping\n", maxsplit=1)[0].strip()


def core_skills(profile: str) -> list[str]:
    match = re.search(r"^- Core knowledge:\s*(.+)$", profile, re.MULTILINE)
    if not match:
        return []
    names = re.findall(r"`([a-z0-9][a-z0-9-]*)`", match.group(1))
    for name in names:
        if not (SKILLS / name / "SKILL.md").is_file():
            raise ValueError(f"role names a missing skill: {name}")
    return names


def skill_body(name: str) -> str:
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n.*?\n---\n?", text, re.DOTALL)
    return text[match.end():].strip() if match else text.strip()


def render(role: str, include_skills: bool = False) -> str:
    profile = portable_profile(role)
    skills = core_skills(profile)
    out = [
        f"# Role brief: {role}",
        "",
        "Use this role for the current task. Project instructions and host permissions win over this brief. "
        "Use only tools actually granted by the host; state any missing capability instead of assuming it.",
        "",
        profile,
    ]
    if include_skills:
        for skill in skills:
            out += ["", "---", "", f"# Skill: {skill}", "", skill_body(skill)]
    elif skills:
        out += [
            "",
            "---",
            "",
            "Load the core skill(s) above through the host's normal skill discovery. "
            "For a standalone prompt with only each core `SKILL.md`, rerun with `--with-skills`.",
        ]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a portable role brief for Codex or a raw model.")
    parser.add_argument("role", nargs="?", help="Role name from agent-profiles/")
    parser.add_argument("--list", action="store_true", help="List available roles")
    parser.add_argument("--with-skills", action="store_true", help="Append each core SKILL.md, but not references")
    args = parser.parse_args(argv)
    if args.list:
        if args.role:
            parser.error("--list does not take a role")
        print("\n".join(role_names()))
        return 0
    if not args.role:
        parser.error("a role is required (or use --list)")
    try:
        print(render(args.role, include_skills=args.with_skills), end="")
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
