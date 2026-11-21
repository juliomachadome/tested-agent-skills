# Using the skills and agents with Claude Code

Claude Code reads this repository's skill folders and native agent definitions directly. Start with the smallest set that matches the work.

## Install skills

```bash
# Preview the default install without changing anything.
scripts/install.sh --dry-run

# Install every supported skill and the eight default Claude Code agents.
scripts/install.sh

# Install one skill only.
scripts/install.sh --skill copywriting

# Install a focused set.
scripts/install.sh --skill copywriting,seo-geo

# Install a curated area.
scripts/install.sh --profile marketing
scripts/install.sh --profile engineering
scripts/install.sh --profile business
scripts/install.sh --profile content
```

The installer links skills into `~/.claude/skills/` and native agent definitions into `~/.claude/agents/`. If a target already exists, it moves that target into a dated backup directory before creating the link. It does not run a skill, send data, or remove unrelated files. Start a new Claude Code session after installation.

Use `--prune` only when you want the installer to remove links that point to this repository but are outside the selected set. Run it with `--dry-run` first.

## Use native agents

Claude Code can use the definitions in `agents/` as native subagents. The default installation includes eight agents that have a clear reason to work in a separate context:

```text
code-reviewer
qa-verifier
real-user-tester
ui-ux-designer
web-performance-engineer
security-reviewer
fullstack-engineer
nextjs-architect
```

Install named roles without adding the default set:

```bash
scripts/install.sh --profile none --agent sales-rep
scripts/install.sh --profile none --agent data-engineer,finance-analyst
```

This installs only the agent definitions, not their skills. Install the relevant skills separately with `--skill`. Without `--profile none` or `--skill`, `--agent` adds the named agents to the default installation.

Each native agent declares its own skill, model and available Claude Code tools. The role descriptions define what the agent should do; Claude Code still enforces the permissions, approvals and tool availability of the current session.

## Keep context focused

Skills use progressive disclosure. Claude Code sees their short descriptions for discovery, then loads a relevant `SKILL.md` and only the references needed for the task. Installing fewer skills reduces the discovery surface and can reduce irrelevant context.

If the listing becomes crowded, the installer can set Claude Code's documented skill-listing budget only when that setting is absent:

```bash
scripts/install.sh --set-budget
```

This writes `skillListingBudgetFraction: 0.02` to Claude Code's settings and creates a dated backup of that settings file. It does not set a provider spending cap or grant permissions.

## Update or remove

The installation uses links, so updating the local clone updates what future Claude Code sessions load:

```bash
git pull
```

To preview removal of this repository's links, use:

```bash
scripts/install.sh --dry-run --prune --profile marketing
```

The command touches only links that point into this repository. It leaves standalone files and links to other locations alone.

## Safety and evidence

Skills are instructions, not permissions. Review tool access, connectors, data handling and model spend in Claude Code and the project itself. Do not put customer data, credentials or private prompts into public evaluation material.

The published historical comparisons were run with Claude models. They are evidence for those recorded runs, not a guarantee for every model configuration or task. See [Evaluation methodology](evaluation-methodology.md), [Security and privacy](../SECURITY.md), and [Loading, cost and safety boundaries](loading-and-cost.md).
