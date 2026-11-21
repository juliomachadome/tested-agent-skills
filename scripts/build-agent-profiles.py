#!/usr/bin/env python3
"""Generate portable role profiles from Claude Code agent definitions.

The generated documents retain the source role and explicitly label every
Claude-specific setting. They are prompts/checklists, not fake native agents.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    return match.group(1)


def scalar(header: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.+)$", header, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {">", ">-", ">+"}:
        block = re.match(r"\n((?:[ \t]+[^\n]+\n?)+)", header[match.end():])
        return " ".join(line.strip() for line in block[1].splitlines()) if block else None
    return value


def list_block(header: str, key: str) -> list[str]:
    match = re.search(rf"^{re.escape(key)}:\s*\n((?:[ \t]+-\s+.+\n?)*)", header, re.MULTILINE)
    if not match:
        return []
    return [line.strip()[2:].strip() for line in match.group(1).splitlines() if line.strip().startswith("-")]


def read_agents(agents_dir: Path) -> list[dict]:
    agents = []
    for path in sorted(agents_dir.glob("*.md")):
        header = frontmatter(path)
        name = scalar(header, "name")
        description = scalar(header, "description")
        if not name or not description:
            raise ValueError(f"agent needs name and description: {path}")
        tools = [item.strip() for item in (scalar(header, "tools") or "").split(",") if item.strip()]
        agents.append({
            "name": name,
            "description": description,
            "tools": tools,
            "skills": list_block(header, "skills"),
            "model": scalar(header, "model"),
            "memory": scalar(header, "memory"),
            "mcp_servers": list_block(header, "mcpServers"),
        })
    return agents


def capabilities(agent: dict) -> tuple[list[str], list[str]]:
    tools = set(agent["tools"])
    required = [
        "Read the current project's instructions, relevant scope and supplied evidence before acting.",
        "Read the listed skills and only the references needed for the task.",
        "Return a verifiable deliverable, assumptions, limits and the next handoff when appropriate.",
    ]
    optional = []
    mappings = [
        ("Write" in tools or "Edit" in tools, "Modify workspace files only when the requesting workflow authorizes it."),
        ("Bash" in tools, "Run proportionate, non-destructive local commands when the host grants shell access."),
        (bool({"WebSearch", "WebFetch"} & tools), "Research current external facts only when web access is available and appropriate."),
        (any(tool.startswith("mcp__") for tool in tools), "Use equivalent isolated browser or tool integrations only when explicitly available."),
    ]
    optional.extend(text for enabled, text in mappings if enabled)
    return required, optional


def render_profile(agent: dict) -> str:
    required, optional = capabilities(agent)
    skills = ", ".join(f"`{skill}`" for skill in agent["skills"]) or "No preloaded skill declared."
    source_tools = ", ".join(f"`{tool}`" for tool in agent["tools"]) or "None declared."
    source_servers = ", ".join(f"`{server}`" for server in agent["mcp_servers"]) or "None declared."
    required_md = "\n".join(f"- {item}" for item in required)
    optional_md = "\n".join(f"- {item}" for item in optional) or "- No optional host capability is required by the frontmatter."
    return f"""# {agent['name']}

## Role

{agent['description']}

## Scope and inputs

- Apply the current project instructions before this role profile.
- Use the task brief, explicitly supplied files and project context as the source of truth.
- Core knowledge: {skills}
- State a missing input or assumption instead of inventing it.

## Output contract

Deliver the requested specialist output in the language of the brief. Identify relevant evidence, assumptions, what could not be verified, and the next responsible owner or role when a handoff is needed. Do not claim that a tool was used unless the host actually provided it.

## Required capabilities

{required_md}

## Optional capabilities

{optional_md}

## Claude Code mapping

This profile was generated from `agents/{agent['name']}.md`. The following values are **Claude Code configuration**, not portable instructions or permissions:

- model: `{agent['model'] or 'not declared'}`
- memory: `{agent['memory'] or 'not declared'}`
- Claude tools: {source_tools}
- Claude MCP servers: {source_servers}

When another harness uses this profile, map only the capabilities it actually offers. If an equivalent is unavailable, disclose the limitation, adapt the work, or hand it off. Do not assume access to Claude tools, MCP servers, model selection, project memory, agent delegation or network access.
"""


def build(agents_dir: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for agent in read_agents(agents_dir):
        path = output_dir / f"{agent['name']}.md"
        path.write_text(render_profile(agent), encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate portable profiles for Claude Code agents.")
    parser.add_argument("--agents", type=Path, default=ROOT / "agents")
    parser.add_argument("--output", type=Path, default=ROOT / "agent-profiles")
    args = parser.parse_args(argv)
    paths = build(args.agents, args.output)
    print(f"generated={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
