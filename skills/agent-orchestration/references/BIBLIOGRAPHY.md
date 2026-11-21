# Bibliography: agent-orchestration

Checked 15/11/2026. Status: **V** = identity (title, authors, year) matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`) this pass, authors from the authors endpoint; **P** = official page opened and the relevant text read this pass; **S** = exists, text not read; **U** = not verified. Nothing is quoted; ideas are restated. Labels: DOCS (vendor documentation, version-dependent), REPORT (published engineering report), BOOK, PAPER. Docs pages move: re-open before quoting a model name, price or flag.

## Anthropic engineering articles
1. Anthropic. "Building effective agents". https://www.anthropic.com/research/building-effective-agents (the older /research path serves it; page title "Building effective AI agents"). **P**. REPORT. Supports: start with the simplest pattern; chaining, routing, parallelisation, orchestrator-workers, evaluator-optimizer (`playbooks.md` 1, 4).
2. Anthropic Engineering. "How we built our multi-agent research system". https://www.anthropic.com/engineering/multi-agent-research-system (redirects to /research/). **P**. REPORT. Text read: agents use about 4x the tokens of chat and multi-agent about 15x; poor fit where agents share context or depend on each other, such as most coding. Supports: spawn test, cost figures (`SKILL.md` 2, `diagnosis-playbook.md` worked numbers).
3. Anthropic. "Effective context engineering for AI agents". https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. **P**. REPORT. Sub-agents with clean context windows return a condensed result. Supports: why a worker gets pointers, not pasted files (`playbooks.md` 2).
4. Anthropic. "Writing effective tools for agents". https://www.anthropic.com/engineering/writing-tools-for-agents. **P**. REPORT. Build a prototype, run evaluations, iterate with the agent. Supports: eval method for tools and agent descriptions (`playbooks.md` 7).

## Claude Code documentation (code.claude.com/docs/en/...)
5. "Create custom subagents" (`sub-agents`). **P**. DOCS. Text read: frontmatter fields (model, effort, maxTurns, isolation, background), nesting up to three layers by default and the depth variable, restricting spawnable agents with Agent(type) in tools, background versus foreground behaviour, worktree isolation. Supports: `SKILL.md` 4, `diagnosis-playbook.md` 5, 7.
6. "Extend Claude with skills" (`skills`). **P**. DOCS. SKILL.md frontmatter and description role. Supports: `SKILL.md` frontmatter, `playbooks.md` 7.
7. "Plugins overview" (`plugins`). **P**. DOCS. Plugin layout: manifest, skills/, agents/. Supports: loading all skills and agents together in a test plugin (`playbooks.md` 7).
8. "CLI reference" (`cli-reference`). **P**. DOCS. Read: `--max-turns` (print mode), `--max-budget-usd`. Supports: caps in headless runs.
9. "Run Claude Code programmatically" (`headless`). **P**. DOCS. Read: `claude -p` with `--allowedTools` to pre-approve tools. Supports: `diagnosis-playbook.md` 11, 14.
10. "Settings files and precedence" (`settings`). **P**. DOCS. Scopes and precedence. Supports: project rules and env settings (depth limit).
11. "Configure permissions" (`permissions`). **P**. DOCS. Read: deny, then ask, then allow order; deny cannot be overridden by a narrower allow. Supports: `diagnosis-playbook.md` 11.
12. "Manage costs effectively" (`costs`). **P**. DOCS. Read: agent-team token use scales with team size; Sonnet for teammates; `/usage` attribution by subagent, skill and plugin; the average-cost figures are enterprise averages, not a forecast. Supports: `diagnosis-playbook.md` 1, `playbooks.md` 8.
13. "Model configuration" (`model-config`). **P**. DOCS. Read 2026-11-15: aliases resolved to Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.2 on the Anthropic API; effort levels and which is default; effort of subagents; `claude-haiku-5-5` id. Supports: `playbooks.md` 3. Date-sensitive.

## Models and pricing
14. Anthropic. "Models overview", platform.claude.com/docs/en/models/overview (the older docs.claude.com path redirects). **P**. DOCS. Current model list and capability fields. Date-sensitive.
15. Anthropic. "Pricing", platform.claude.com/docs/en/about-claude/pricing. **P**. DOCS. Read per-million-token rows for Sonnet 5.5, Haiku 5.5 and Opus 5.5 (Opus cache columns not read; assumed 4x Sonnet in the worked numbers). Date-sensitive.

## Skills standard
16. Agent Skills. "Specification". https://agentskills.io/specification. **P**. DOCS. SKILL.md layout, required name and description fields. Supports: skill structure.
17. Agent Skills. "Evaluating skill output quality". https://agentskills.io/skill-creation/evaluating-skills. **P**. DOCS. Run each case with and without the skill, workspace per iteration, assertions, grading. Supports: `playbooks.md` 7.

## Books and paper
18. Brooks, F. P. *The Mythical Man-Month: Essays on Software Engineering, Anniversary Edition*. Addison-Wesley, 1995 (first edition 1975). ISBN 978-0201835953. **V** (catalogue shows 1995 and the publisher; author per authors endpoint). BOOK. Supports: communication paths grow as n(n-1)/2; adding workers adds coordination cost (`diagnosis-playbook.md` worked numbers).
19. Forsgren, N., Humble, J., Kim, G. *Accelerate: The Science of Lean Software and DevOps*. IT Revolution Press, 2018. ISBN 978-1942788331. **V**. BOOK + STUDY (survey data, from the book; not re-checked). Supports: small batches and fast feedback over large unverified changes.
20. Little, J. D. C. "A Proof for the Queuing Formula: L = λW". *Operations Research* 9(3), 383-387, June 1961. DOI 10.1287/opre.9.3.383. **S**: the publisher landing page is behind a bot check (needs browser pass); title, author, journal, volume, pages and year were matched through the Crossref record for the DOI. PAPER. Supports: work in progress equals throughput times time in system; extra agents above a bottleneck add queue, not output.

House rules marked [F] come from the owner's own operating experience and from running the evaluation scripts in this repository, not from published studies.

Totals: 20 entries. Verified identity or text read (V or P): 19 (items 1-17 are P, 18 and 19 are V). Seen but text unread (S): 1 (item 20). Unverified (U): 0, plus sub-claims not checked: Opus 5.5 cache prices, current Opus/Fable model details beyond the alias table, RAM and token ranges (estimates to measure locally), and the "owner experience" rules.
