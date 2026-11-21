# Red Flags and Audit Mode

Contents: 1 Red flags · 2 Audit mode

## 1. Red flags

| Smell | Cost | Fix |
|---|---|---|
| LLM doing arithmetic, totals, unit conversion, date math | wrong numbers | compute in code; give results to the LLM |
| Parsing free text with regex/`JSON.parse` and hoping | random failures | structured outputs / tool call + schema validation + bounded repair retry |
| Required schema fields with no `null`/"unknown" option | forced invention | nullable fields, explicit `unknown`, abstention examples |
| Whole knowledge base / full history pasted into every call | cost, latency, worse answers | retrieval, summaries, just-in-time loading, trimming |
| Dynamic data (date, user name, ids) at the start of the prompt | cache misses on every call | stable prefix first, variable parts last |
| Biggest model for every call | 5–30× cost | route by difficulty; small model for classify/extract; cascade |
| Long generation inside an HTTP request | timeouts, duplicate charges on retry | background job + status/polling/push + idempotency key |
| No per-user/tenant token quota | denial of wallet | quotas, rate limits, input size caps |
| Vector-only search for names, codes, article numbers | misses exact matches | hybrid (BM25 + vector) + metadata filters |
| Answers without citations in a knowledge domain | unverifiable hallucinations | cite source ids per claim; verify citations exist; abstain if none |
| Tool with side effects callable on model's word alone | prompt-injection damage | authorization in code, confirmation step, least-privilege tools |
| Model output rendered as HTML / executed as SQL/shell | XSS / injection | encode, allow-list, read-only scoped execution |
| Prompt edited in production with no eval or version | silent regressions | prompts in repo, versioned, eval gate in CI |
| Agent loop with no step/cost cap | infinite loops, bills | max steps, max tokens, timeouts, stop conditions |

## 2. Audit mode — `/llm-engineering audit`

Run this **only** when the user explicitly invokes `/llm-engineering audit` or explicitly asks for a full AI/LLM audit. Never start it during normal tasks. Do not change application code during the audit.

1. **Inventory every LLM/embedding call site.** For each: file:line, feature/purpose, provider and model, sync/async, prompt location and version, input composition (system, examples, retrieved context, history, user input), output format and validation, error/retry/fallback handling, caching, streaming, who triggers it and how often.
2. **Quantify.** From logs/usage data if present: calls/day, avg input/cached/output tokens, p95 latency, error and validation-failure rates. Otherwise estimate from code and mark `ESTIMATE`. Compute cost per call, per feature per month and per active user per month (use current prices from the provider's pricing page if accessible; otherwise leave price as a parameter).
3. **Assess quality.** Existing evals? Reference datasets? Known failure modes (hallucinated items, invalid JSON, wrong language, constraint violations)? If none, propose a starter eval set (20–50 real cases) per feature with graders.
4. **Go through every reference file** (except `BIBLIOGRAPHY.md`) and classify each relevant point per feature: `OK` (evidence file:line) / `GAP` (file:line, severity, fix) / `N/A` (reason) / `UNKNOWN` (what would confirm it). A valid alternative to this guide used consistently is `OK (convention)`, not `GAP`. For large codebases use one subagent per reference file and consolidate.
5. **Write `docs/llm-audit.md`:**
   - Call-site inventory table and cost table (current monthly cost, cost per user, with ESTIMATE flags).
   - **Optimization plan ranked by impact**: for each item — expected cost saving (% and $), expected quality effect, risk, effort (S/M/L), and how to verify with evals. Put zero-risk wins first (caching order, output caps, batch for offline work, removing redundant context, structured outputs).
   - Quality and security gaps (must-fix first), proposed eval sets and monitoring, date and commit hash.
6. **Propose an `## AI/LLM profile` block for `CLAUDE.md`** (≤ 30 lines): providers/models per feature, where prompts live, client wrapper, validation pattern, budgets per user, eval command, known gaps → `docs/llm-audit.md`. Show it and ask before editing.
7. Gaps are a backlog: fix only on request, one per change, each verified on evals.

## Sources

See BIBLIOGRAPHY.md (cost, evals and security sections back the fixes listed above).

See also: `diagnosis-playbook.md` for the evidence trees behind each flag and `playbooks.md` section 7 for incident response.
