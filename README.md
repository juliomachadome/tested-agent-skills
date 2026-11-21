# Tested Agent Skills

**35 portable Agent Skills and 26 Claude Code subagents, measured on Claude models against a no-skill baseline.**

License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Commercial use is allowed; attribution is required; shared adaptations use the same license.

**Privacy and release policy:** public releases contain aggregate evidence and synthetic fixtures, not raw sessions, private holdouts or personal configuration. See [SECURITY.md](SECURITY.md) for boundaries, installation behavior and the release check.

Skills for marketing, sales, product, engineering, design and data. Historical claims are backed by aggregate evidence and synthetic fixtures; raw answers and holdouts stay out of public releases.

## Evidence at a glance

[![Aggregate historical Claude-based evaluation results](docs/assets/evaluation-summary.svg)](docs/evaluation-summary.md)

The chart reports historical Claude-based records only: **31 full-protocol wins**, **2 ties**, **1 limited comparison** and **1 not-applicable command** across 35 entries. It is aggregate evidence, not a score for every model or harness. Read the definitions and limits in [Evaluation evidence](docs/evaluation-summary.md).

- **Skill** = knowledge (rules, diagnosis trees, playbooks, sources) that Claude Code discovers by topic; the full skill and then its references are loaded progressively.
- **Agent** = a specialist that runs in a separate context and preloads one skill.
- **Project rules win.** Every skill and agent reads the current project's `AGENTS.md` or `CLAUDE.md` first.

## Works with

The skills are plain Markdown in the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md`. Nothing in them calls a vendor API.

| Where | How |
| --- | --- |
| Claude Code | Skills and native agents install with `scripts/install.sh`. See [the Claude Code guide](docs/claude-code.md). |
| Codex | Skills install with `scripts/install.sh --target codex` (or `--target agents`). `scripts/codex-skill-eval.py` provides an isolated smoke test; use a portable role brief for specialist work. See [the Codex guide](docs/codex.md). |
| Cursor and other Agent Skills readers | The skills use the open `SKILL.md` folder format. Check that tool's own docs for its discovery folder; this repository does not claim a tested integration for every tool. |
| Any other harness (OpenCode, Gemini CLI, Aider, your own) | Add the instructions shown below so it can find and read `SKILLS.md`; the harness must implement that behavior. |
| Any model with no harness (DeepSeek, GPT, Gemini, Llama, a raw API) | `scripts/skill-to-prompt.py <skill>` prints a prompt to paste or send as the system message; it is not automatic skill loading. |

What is tool-specific: the files in `agents/` use the Claude Code subagent format (frontmatter with `tools`, `model`, `skills`). In another tool, use an agent file as a role prompt.

What was measured: the evals ran on Claude models. The skills are model-neutral text, but they have **not** been scored on other models or in every harness.

For AI tools that support the emerging `llms.txt` convention, [llms.txt](llms.txt) provides a compact map to the right installation and harness guide. It improves discovery for compatible readers; it does not make a tool install or load skills automatically.

## What is inside

| Area | Skills |
| --- | --- |
| Marketing and sales | `copywriting`, `offers`, `ad-creatives`, `paid-traffic`, `seo-geo`, `viral-content`, `storytelling`, `lifecycle-messaging`, `media-production`, `sales`, `customer-support` |
| Product and business | `market-research`, `product-creation`, `product-management`, `business-model-finance`, `process-improvement`, `growth-analytics` |
| Engineering | `engineering-playbook`, `code-craft`, `code-review-criteria`, `software-architecture`, `software-security`, `qa-verification`, `web-performance`, `cloud-deploy-ops`, `mobile-app-engineering`, `llm-engineering`, `agent-orchestration` |
| Design | `ui-design`, `ux-design`, `web-motion` |
| Data | `data-analysis`, `data-engineering`, `data-visualization-dashboards` |
| Command | `redigir` (a guided copywriting brief; typed as `/redigir` in Claude Code) |

Each skill is a folder:

- `SKILL.md`: when it applies and the core rules, about 8 to 9 KB.
- `references/`: depth, loaded on demand (diagnosis playbook, playbooks, variants).
- `references/BIBLIOGRAPHY.md`: every source, marked as read, identity checked or unverified.
- `evals/public/`: synthetic fixtures for safe smoke tests. Historical full answers, task sets and holdouts stay outside the public release.

`SKILLS.md` lists every skill with its description and path. [CATALOG.md](CATALOG.md) and `catalog/index.html` are the English-first discovery catalog.

## How it was tested

- **With and without.** The same task is answered twice, once with the skill and once without, and a blind judge compares both orders. The aggregate historical record is 31 full-protocol wins, 2 ties, 1 limited comparison and 1 not-applicable command; `redigir` is a command with no standalone knowledge to compare.
- **Trigger.** Each skill is checked for firing on the questions it should and staying quiet on the ones it should not: `evals/trigger-results.json`.
- **Agents.** An agent costs about twice the skill alone, so only agents with a reason to run in a separate context are installed by default. Only `code-reviewer` has been compared with its inline skill so far; the other default agents are there because of how they are used, not because of a test.

Public releases exclude the full historical benchmark runner and holdout tasks. They include an isolated synthetic Codex smoke adapter in `scripts/codex-skill-eval.py`. See [Evaluation methodology](docs/evaluation-methodology.md) and [Compatibility](docs/compatibility.md) for the boundaries.

### Reproducing what is public

Anyone can verify the install plan without changing their machine:

```bash
scripts/install.sh --dry-run --target agents --profile engineering
```

They can inspect the [aggregate evaluation record](docs/evaluation-summary.md), review the available synthetic fixtures, and turn a skill into a standalone prompt with `scripts/skill-to-prompt.py <skill>`. The historical blind benchmark is not independently reproducible from this repository; public results are evidence from the original Claude-based runs, not a cross-model benchmark.

## Install

Requirements: git, bash and python3. Node with `npx` for the agents that open a browser. macOS and Linux; on Windows use WSL.

```bash
git clone https://github.com/juliomachadome/tested-agent-skills.git ~/tested-agent-skills
cd ~/tested-agent-skills
```

### Claude Code (skills and agents)

```bash
scripts/install.sh            # add --dry-run to preview
```

This links all 35 skills into `~/.claude/skills/` and 8 of the 26 agents into `~/.claude/agents/`: `code-reviewer`, `qa-verifier`, `real-user-tester`, `ui-ux-designer`, `web-performance-engineer`, `security-reviewer`, `fullstack-engineer` and `nextjs-architect`. Anything already there with the same name is moved to a dated backup folder first, never deleted.

See [Using the skills and agents with Claude Code](docs/claude-code.md) for focused installs, native agents, context controls, updates and safety boundaries.

The other 18 agents install by name:

```bash
scripts/install.sh --agent data-engineer,sales-rep
```

Open a new session afterwards. Update with `git pull`; the links follow the repo.

### Codex, Cursor and other Agent Skills readers

```bash
scripts/install.sh --target agents   # links skills into ~/.agents/skills (AGENTS_HOME overrides)
scripts/install.sh --target codex    # links skills into ~/.codex/skills  (CODEX_HOME overrides)
scripts/install.sh --target codex --skill code-review-criteria
```

For one project only, copy or link the folders you want into the project's `.agents/skills/`. If your tool reads another folder, check its docs and link `skills/<name>` there.

For a specialist workflow in Codex, render the corresponding portable role brief and paste it before the task:

```bash
python3 scripts/role-to-prompt.py code-reviewer
python3 scripts/role-to-prompt.py fullstack-engineer
```

See [Using the skills and roles with Codex](docs/codex.md) for the focused install, the most common role/skill pairs and safety boundaries.

### Any other harness

Add this to the tool's instructions file (`AGENTS.md`, `GEMINI.md`, a rules file):

```
General skills are listed in ~/tested-agent-skills/SKILLS.md.
Before working on a topic, find the matching skill there, read its SKILL.md,
then only the references/ files it points to.
Project rules in this repository win over the general skills.
```

### Any model, no harness

```bash
scripts/skill-to-prompt.py offers                     # SKILL.md as one prompt
scripts/skill-to-prompt.py offers --refs              # plus every reference file
scripts/skill-to-prompt.py offers --refs diagnosis    # plus the references whose name matches
```

Send the output as the system message, or paste it at the top of a chat. `--refs` can be large; pass a name to include only what the task needs.

### Only one area

```bash
scripts/install.sh --profile marketing            # or engineering, business, content
scripts/install.sh --profile marketing,business   # several together
scripts/install.sh --skill copywriting            # exactly one skill
scripts/install.sh --skill copywriting,seo-geo    # a small custom set
scripts/install.sh --profile marketing --skill process-improvement  # profile plus one extra
scripts/install.sh --agent sales-rep              # an extra Claude Code agent, only when wanted
```

Profiles are defined in `scripts/profiles.json`. Selecting fewer skills keeps the discovery list and potential context smaller. It is an installation and cost-control choice, **not** a permission boundary: the harness still decides which tools, files, network access and agent delegation are allowed. See [Loading, cost and safety boundaries](docs/loading-and-cost.md).

### Uninstall

```bash
find ~/.claude/skills ~/.claude/agents ~/.agents/skills -maxdepth 1 -type l -lname '*tested-agent-skills/*' -print -delete
```

## Skill or agent?

The knowledge lives in the skill. An agent is worth its cost only when a separate context buys something:

| Reason | Agents |
| --- | --- |
| Independent review: the reviewer has not seen the author's reasoning | `code-reviewer`, `qa-verifier`, `security-reviewer` |
| Heavy output (screenshots, traces) kept out of the conversation | `real-user-tester`, `ui-ux-designer`, `web-performance-engineer` |
| Parallel edits in a worktree | `fullstack-engineer` |
| Design on another model | `nextjs-architect` |

For everything else, work in the main session and let the skill load.

## License

Copyright (c) 2026 Júlio Machado.

Licensed under [Creative Commons Attribution-ShareAlike 4.0 International](LICENSE) (CC BY-SA 4.0). In short:

- **You may** use, copy and adapt this material, including commercially.
- **You must** give credit, link to this repository and to the license, and say what you changed.
- **You must** share adaptations under this same license.

For copy-paste attribution blocks for public projects, commercial products and agents, see [ATTRIBUTION.md](ATTRIBUTION.md). A public README is the preferred location when one exists.

The sources listed in each `BIBLIOGRAPHY.md` belong to their authors. They are cited as references; their text is not reproduced here.

### Scope and third-party materials

Unless a file says otherwise, the CC BY-SA 4.0 license covers the original skills, agents, documentation, catalog and scripts in this repository. Books, articles, websites, trademarks and other third-party materials mentioned in bibliographies or citations remain the property of their respective owners and are not licensed by this repository. The repository provides original synthesis and references, not copies of those materials.

## Contributing and community

External contributors propose changes through issues and pull requests; a proposal does not grant write, merge, release or settings access. See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SUPPORT.md](SUPPORT.md). Public-release maintainers can use the [branch and publication checklist](docs/maintainer-publication-checklist.md).
