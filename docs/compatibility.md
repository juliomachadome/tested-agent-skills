# Compatibility

## Read this as a capability matrix, not a marketing promise

The skills are ordinary Markdown folders with a `SKILL.md`. That makes their knowledge portable, but discovery, tool permissions, agent delegation and evaluation behavior belong to the harness. “Works with” means the precise capability in the table, not identical results across all models.

| Environment | Skill discovery | Agent definitions | Measured here | Notes |
| --- | --- | --- | --- | --- |
| Claude Code | Supported by `scripts/install.sh` | Native Claude subagents in `agents/` | Historical skill evaluations used Claude models | This repository publishes [aggregate evidence](evaluation-summary.md). The historical runner and holdouts remain private. |
| Codex | Supported by `scripts/install.sh --target codex`; focused `--skill` and profiles are supported | Render a portable role brief with `scripts/role-to-prompt.py`; not a native Claude subagent | One isolated local smoke test is supported; no scored benchmark yet | The adapter prevents normal user configuration from loading. See [Codex guide](codex.md). |
| Shared Agent Skills folder | Supported by `scripts/install.sh --target agents` | Harness-dependent | Not scored as a group | A reader must implement the folder-discovery behavior. |
| Cursor and other Agent Skills readers | Format-compatible | Harness-dependent | No integration claim | Check that product's documented discovery folder. |
| Raw model API or chat | Manual prompt export | Manual role prompt | No automatic discovery or evaluation claim | Use `scripts/skill-to-prompt.py`. |

The Markdown files can be installed in Codex. Applying the workflows in [`redigir`](../skills/redigir/SKILL.md) and [`agent-orchestration`](../skills/agent-orchestration/SKILL.md) requires adapting the Claude Code command and delegation conventions respectively.

## Portable skills

A skill can be copied into a compatible discovery folder or converted to a system/context prompt:

```bash
scripts/install.sh --dry-run --target codex
scripts/skill-to-prompt.py engineering-playbook
```

The first command is a no-change preview. The second emits the selected `SKILL.md`; `--refs` includes reference files and can be substantially larger.

## Loading, cost and safety boundaries

In Claude Code, these skills are optimized for progressive disclosure: the concise description is used for discovery; Claude Code loads the matching `SKILL.md` when it decides the topic applies; the skill points to reference files only when deeper material is needed. That design avoids putting every playbook and bibliography into every conversation, but it is a context-efficiency design, not a guarantee about a particular response or bill.

Install only the material a person or project needs when appropriate:

```bash
scripts/install.sh --skill copywriting
scripts/install.sh --profile marketing
scripts/install.sh --profile marketing --skill process-improvement
```

On Codex, Cursor and other readers, the same files are portable but the harness owns discovery and loading behavior. A raw model API needs an explicit prompt export, so there is no automatic activation. In every environment, a skill is an instruction file, not an authorization layer: tool permissions, file access, network access, spending limits, rate limits and any agent-concurrency limit must be configured in the harness or surrounding application.

## Portable agent roles

The `agents/*.md` files are Claude Code-specific because their frontmatter names Claude tools, models and skills. A portable consumer should use the matching document in [`agent-profiles/`](../agent-profiles/) as a role prompt and capability checklist. It must map the required capabilities to its own tools, keep project rules above the role, and decline or adapt work when a capability is unavailable.

That is useful portability, not a claim of native subagent support.

## Reporting a new result

For a result to be comparable, publish or retain:

1. Harness and exact version.
2. Model identifier and relevant settings.
3. Skill revision/commit.
4. Fixture identifier and whether it is synthetic or private.
5. Isolation settings and available tools.
6. Evaluation rule, judge procedure, result and date.

Do not put customer data, raw prompts containing private content, credentials, connector configuration or full private model responses in a public report.
