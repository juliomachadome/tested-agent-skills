# Using the skills and roles with Codex

## Install the smallest useful set

For a person or project that needs one area, install only those skill folders:

```bash
# Review code in Codex.
scripts/install.sh --target codex --skill code-review-criteria

# Build a feature in Codex.
scripts/install.sh --target codex --skill engineering-playbook

# A curated engineering set, without installing unrelated marketing skills.
scripts/install.sh --target codex --profile engineering
```

Use `--dry-run` first to preview the links. Skill discovery and progressive loading are owned by Codex; installing a smaller set reduces available descriptions and potential irrelevant context, but it does not change Codex permissions or spending controls.

## Use specialist roles in Codex

The files in `agents/` are Claude Code subagent definitions. For Codex, use the corresponding portable profile in `agent-profiles/`. This command renders a compact role brief:

```bash
python3 scripts/role-to-prompt.py code-reviewer
python3 scripts/role-to-prompt.py qa-verifier
python3 scripts/role-to-prompt.py security-reviewer
python3 scripts/role-to-prompt.py fullstack-engineer
python3 scripts/role-to-prompt.py sales-rep
```

Paste the output at the beginning of a Codex task, followed by the actual request. The brief contains the role, output contract and its core skill name, while leaving out Claude-specific models, tool labels, memory and MCP settings. When the core skill is installed, let Codex load it normally. For a raw model or a one-off standalone prompt, add `--with-skills`; that appends only the role's core `SKILL.md`, not its potentially large reference tree.

| Need | Install | Portable role brief |
| --- | --- | --- |
| Read-only code review | `code-review-criteria` | `code-reviewer` |
| Test and release evidence | `qa-verification` | `qa-verifier` |
| Security review | `software-security` | `security-reviewer` |
| Implement a bounded change | `engineering-playbook` | `fullstack-engineer` |
| Sales proposal or deal work | `sales` | `sales-rep` |

List all 26 available roles with:

```bash
python3 scripts/role-to-prompt.py --list
```

## Safety and cost boundaries

A role brief changes task instructions only. Permissions, connectors, approvals and model budgets remain configured in Codex and the project.

## Run the synthetic smoke test

The adapter copies a skill from the checkout into a temporary project. The default run previews setup and command options.

```bash
python3 scripts/codex-skill-eval.py --fixture evals/public/codex-smoke.json
```

The `--live` option invokes Codex in an ephemeral, read-only session that ignores normal user configuration. It may incur provider charges. The report records session events and process exit. Verifying skill loading or scoring answer quality requires a separate test.

## Uninstall

Use the [README removal commands](../README.md#uninstall) with the target and destination you used when installing.

## What is and is not proven

The historical quality comparisons were run on Claude models. Codex support here covers skill installation, a portable role brief and an isolated synthetic smoke path. It does not establish equal role quality or native subagent behavior in Codex. Report a Codex result with the model, revision, harness version, fixture, tools and isolation settings; see [Compatibility](compatibility.md).
