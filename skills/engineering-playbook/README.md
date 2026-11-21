# engineering-playbook: how to use it in Claude Code

## What it is

A Claude Code **skill**: a folder with a `SKILL.md` (the router: priorities, pre-flight checklist, red flags, routing table, output format) and one file per area in `references/`. The content is in English because models follow technical instructions most precisely in English.

```
engineering-playbook/
├── SKILL.md                      <- read whenever the skill activates
├── references/                   <- read only when the task touches the topic
│   ├── algorithms-complexity.md
│   ├── performance.md
│   ├── databases.md              (indexes, plans, migrations, keyset, temporal versions, Prisma + pooler, RLS)
│   ├── concurrency.md
│   ├── distributed-systems.md    (queues in Postgres, idempotency, outbox, retries, SSE)
│   ├── security.md
│   ├── architecture-design.md    (ports and adapters, BFF, MVVM, ADR, C4, proportion)
│   ├── api-design.md             (status codes, RFC 9457 problem details)
│   ├── money-time-text.md
│   ├── saas-multitenancy.md      (explicit tenant filter + RLS, per-tenant LLM quota)
│   ├── testing.md
│   ├── reliability-ops.md
│   ├── frontend.md
│   ├── ai-llm.md
│   ├── compliance-eu.md
│   ├── latency-sync-hygiene.md
│   ├── diagnosis-playbook.md     (Step 0 and trees for production problems, with worked numbers)
│   ├── playbooks.md              (test-first change, big-table migration, endpoint, job, hotfix, upgrade, done)
│   ├── audit-mode.md
│   └── BIBLIOGRAPHY.md           (numbered, V/P/S/U status per source)
└── evals/                        <- evals.json and trigger_eval.json
```

## Why a skill and not one huge CLAUDE.md

`CLAUDE.md` is loaded in full in every session; a 3,000-line file there spends context on everything and dilutes the project's own instructions. With a skill, only the `description` is visible at first; `SKILL.md` loads when the task matches, and each reference only when its topic appears.

## Install

Copy the folder to `~/.claude/skills/engineering-playbook/` (personal) or `.claude/skills/engineering-playbook/` inside a repository (shared with the team). A personal skill wins over a project skill of the same name.

## Triggering

- **Automatic:** requests such as "optimize this endpoint", "review this PR", "design the payments table", "why is this slow".
- **Manual:** start the message with `/engineering-playbook`. Add `audit` for the full-project audit mode.

Add three lines to each repository's `CLAUDE.md` so triggering is more reliable, and keep project-specific conventions (stack, build commands, patterns) there, not in the skill.

## Prompts that work well

- `/engineering-playbook audit src/Payments for performance and security. Report in the output contract format, ordered by severity, without changing code yet.`
- `Implement the transfer endpoint. Before coding, run the pre-flight checklist and tell me the risks.`
- `This handler takes 2 s with 50k rows. Find the bottleneck (I/O first), propose the fix with Big O before/after and write a benchmark.`
- `Design the tenant isolation model following saas-multitenancy.md and record it as an ADR.`

## Maintenance

- When the model repeats a mistake, add a line to the "Red flags" table in `SKILL.md`: it is the highest-leverage place.
- Keep `SKILL.md` short; new content goes to `references/` with one routing line.
- Review once a year. Version-bound facts (framework versions, EU regulation, platform limits) age; fundamentals (Big O, indexes, idempotency) do not. Each reference ends with a Sources list with read dates.

## Limits

- It raises the odds that the model considers indexes, N+1, idempotency, authorization and money, but a human still reviews.
- "Most performant" without measurement is a guess; demand a benchmark or a query plan on critical paths.
- `compliance-eu.md` flags impact; it does not replace legal advice.
