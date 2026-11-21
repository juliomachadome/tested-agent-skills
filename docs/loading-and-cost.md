# Loading, cost and safety boundaries

## What is optimized in Claude Code

The skills are designed for progressive disclosure:

1. A short description is available for discovery.
2. When Claude Code judges the task relevant, it loads the matching `SKILL.md`.
3. The skill directs it to a specific `references/` file only when depth is needed.

That structure avoids injecting every skill, playbook and bibliography into every conversation. It reduces unnecessary context and therefore can reduce token use. It does **not** guarantee that a particular task will use a specific number of tokens, call a model a certain number of times, or select a skill perfectly.

## Install only what is needed

The installer supports a focused installation as well as profiles:

```bash
# One person only writes copy.
scripts/install.sh --skill copywriting

# A marketing team uses the curated marketing group.
scripts/install.sh --profile marketing

# A marketing team also needs one business skill.
scripts/install.sh --profile marketing --skill process-improvement

# An optional Claude Code specialist is installed only by name.
scripts/install.sh --profile none --agent sales-rep
```

Use `--dry-run` first to see the planned links without changing the machine. A focused installation lowers the number of available descriptions and reduces accidental or irrelevant discovery. It is useful for clarity and potential context cost; it is not isolation.

## What the repository does not control

Skills are Markdown instructions. They cannot grant or remove permissions. The harness or surrounding application must enforce:

- file, shell, browser and network permissions;
- model/provider spend caps, rate limits and request quotas;
- which connectors hold data and which tools an agent may call;
- whether subagents are allowed and their concurrency limit;
- approval requirements for external or irreversible actions.

Claude Code has the progressive-loading path described above. Codex, Cursor and other compatible readers may use the same skill folders, but their discovery and loading behavior is their own. For a raw model API, use `scripts/skill-to-prompt.py`; selection is manual and there is no automatic activation.

## A practical default

Start with one skill or one profile, use the main session for normal work, and add an agent only when a separate context has a clear benefit (for example, independent review or browser-heavy evidence). Keep sensitive connectors out of any harness unless the task requires them, and configure its permissions independently of this repository.
