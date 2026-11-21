# Portable agent profiles

These profiles turn the repository's 26 Claude Code roles into portable prompts and capability checklists. They do not create native agents in another tool.

## Use in any harness

1. Read the matching profile and its listed skill folders.
2. Apply the project's own rules first.
3. Map only the required and optional capabilities your harness actually provides.
4. Keep the output contract and state limitations rather than pretending a missing browser, shell, memory or delegation feature exists.

For Codex, install the listed skills through the normal skill folder, then render the profile as a compact role brief:

```bash
scripts/install.sh --target codex --skill code-review-criteria
python3 scripts/role-to-prompt.py code-reviewer
```

Paste that brief before the task and use only the tools enabled for that task. `--with-skills` appends the core `SKILL.md` for a standalone prompt; it is usually unnecessary when Codex already has the skill installed. For a raw API, send the profile and the needed skill content as context. For any other harness, follow its own discovery and tool-policy documentation. See [the Codex guide](../docs/codex.md) for the full workflow.

## Relationship to `agents/`

The source files in [`agents/`](../agents/) remain the authoritative Claude Code definitions. The generated profiles intentionally preserve the source's tool, model, memory and MCP configuration under a clearly labelled **Claude Code mapping** section. Those values are not universal permissions or feature claims.

Regenerate after changing an agent definition:

```bash
python3 scripts/build-agent-profiles.py
```
