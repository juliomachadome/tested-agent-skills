---
name: engineering-playbook
description: Backend and full-stack code (TypeScript/Node/NestJS, React/Next.js, C#/.NET, SQL/Postgres) - invoke this skill FIRST, before answering, for any production code question, even a short one. Examples - "this endpoint takes 2s, it queries the customer for each order" (N+1), "the domain folder keeps importing from infrastructure" (Clean/Hexagonal boundaries, lint rules), "safe migration or index on a 30M-row table without blocking writes", duplicate charges after a webhook retry, validation errors as problem+json (RFC 9457), pagination, idempotency, retries, queues and outbox, money, time and Unicode, multi-tenant data, tests, observability, diagnosing a production code problem, routines (test-first change, new endpoint or job, hotfix, upgrade), "best practice way", "most performant". Not for narrow jobs a specialist owns (software-security, web-performance, code-review-criteria for a PR verdict, llm-engineering, cloud-deploy-ops, software-architecture for system design and ADRs).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Engineering Playbook

A decision guide, not a textbook. Read this file fully; open a reference **only when the task touches that area** (section 4). Siblings own: `web-performance`, `ux-design`/`ui-design`, `llm-engineering`, `software-security`.

Evidence tags: **[C]** consensus or spec, **[M]** measured or from a study, **[F]** practitioner starting point (replace with your own numbers), **[X]** myth.

## 0. Project first

Before any advice, read the current project's CLAUDE.md or AGENTS.md, lint and type configs, ADRs, folder layering and test setup. **The project's existing patterns win**: find how this codebase already does the same kind of thing (naming, errors, validation, data access, tests) and follow it; never add a second way. If the existing pattern is a bug or security issue, keep the structure, flag it, and propose the change separately.

## 1. Priority order (when goals conflict)

1. **Correctness**, including edge cases (empty, null, huge, concurrent, duplicate, timezone, rounding).
2. **Security and data safety**: no new injection, authz gap, secret leak, PII exposure or data-loss path.
3. **Clarity and maintainability**: the next reader understands it without you.
4. **Performance** at the level real data and traffic justify, *measured* where it matters.
5. **Cleverness**, last. Never trade 1-3 for it.

- Find the **lower bound** before optimizing (touch every item: O(n) is the floor). **I/O dominates CPU** in web backends: fix N+1, chatty calls and missing indexes first. Name the cost of every optimization.

## 2. Pre-flight checklist (run mentally before writing code)

- [ ] `n` in production (rows, requests/s, payload)? Hot or cold path? Growth 10x, 100x?
- [ ] I/O inside a loop (DB, HTTP, file, cache)? Batch it. Lookup inside a loop (`.find`, `.includes`, `IndexOf`)? Build a `Map`/`Dictionary`/`Set` once.
- [ ] Untrusted input reaching SQL, shell, HTML, paths, URLs, deserializers, regex? Parameterize, encode, validate, allow-list.
- [ ] Who may do this, checked **on the server, per resource and tenant**?
- [ ] Retry, double submit, concurrent run? Idempotency, transactions, optimistic concurrency.
- [ ] Timeout or partial failure of a dependency? Timeouts, bounded retries with backoff and jitter, compensation.
- [ ] Money in `decimal`/minor units with explicit rounding; time in UTC.
- [ ] Observable (structured log with correlation id, metric, span), no secrets or PII, and tested?

## 3. Red flags to always fix or call out

| Smell | Cost | Fix |
|---|---|---|
| Lookup in loop (`list.Find` in `foreach`) | O(n*m) | pre-index into a map/set: O(n+m) |
| DB/HTTP call in loop (N+1) | n round trips | join/`Include`, `WHERE id IN (...)`, batch endpoint, bounded `Task.WhenAll` |
| `.Result`, `.Wait()`, `async void` | deadlocks, crashes | `await` all the way; `async Task` |
| `double`/`float` money | wrong totals | `decimal`, integer minor units or a decimal lib |
| `DateTime.Now` in server logic | DST/timezone bugs | `DateTimeOffset.UtcNow` / injected `TimeProvider` |
| String-built SQL | injection | parameters / ORM |
| Unbounded query (`ToList()` no limit) | memory, latency | filter, project, keyset paginate |
| Catch-and-ignore | silent data loss | handle specifically, or log and rethrow |
| Secrets committed | breach | secret manager / env |
| Authorization only in the UI | IDOR | server check per resource and tenant |
| Retries without backoff/limit, or on non-idempotent ops | storms, duplicates | bounded backoff + jitter, idempotency keys |
| No timeout on outbound calls | thread/connection starvation | explicit timeouts, cancellation |
| Heavy sync work on the Node event loop | server stalls | stream, chunk, worker thread, queue |

## 4. Which reference to open

| The task is... | Open |
|---|---|
| Something is broken or slow in production: slow endpoint, intermittent 500s, duplicates, wrong totals, leak, flaky test, locked table, wrong-tenant data, stuck job, hydration or stale cache, inconsistent LLM output | `references/diagnosis-playbook.md` |
| A routine: change test-first, big-table migration, new endpoint or job, hotfix, dependency upgrade, definition of done | `references/playbooks.md` |
| Loops, collections, data structures, complexity | `references/algorithms-complexity.md` |
| Latency, memory, caching, profiling, .NET/Node runtime | `references/performance.md` |
| SQL, indexes, ORM, transactions, Postgres migrations, keyset paging, Prisma and pooler, RLS | `references/databases.md` |
| async/await, threads, locks, races, background workers | `references/concurrency.md` |
| Queues, retries, idempotency, outbox, sagas, breakers, SSE, rate limits | `references/distributed-systems.md` |
| Auth, input handling, secrets, crypto, headers, OWASP, PII | `references/security.md` |
| Boundaries, Clean/Hexagonal, NestJS ports, Next.js BFF, DDD, CQRS, ADRs, C4 | `references/architecture-design.md` |
| Endpoints, status codes, RFC 9457 errors, validation, versioning, webhooks | `references/api-design.md` |
| Money, rounding, ledgers, dates and time zones, Unicode, i18n | `references/money-time-text.md` |
| Multi-tenant SaaS, tenant isolation, per-tenant LLM quota, billing | `references/saas-multitenancy.md` |
| Tests, mocking, flaky tests, load tests | `references/testing.md` |
| Logging, tracing, SLOs, health, deploys, small-product reliability | `references/reliability-ops.md` |
| React/Next/React Native/Expo, web vitals, accessibility, forms | `references/frontend.md` |
| LLM features: prompts, RAG, evals, cost, prompt injection | `references/ai-llm.md` (and `llm-engineering`) |
| GDPR, DORA, MiFID II, PSD2, EU Accessibility Act | `references/compliance-eu.md` |
| Tail latency, load tests, syncing external feeds, repo hygiene | `references/latency-sync-hygiene.md` |
| Which book, spec or paper backs a rule (check the V/P/S/U status) | `references/BIBLIOGRAPHY.md` |
| Explicit request for a full-project audit | `references/audit-mode.md` |
| i18n: ICU messages, plurals, Intl, RTL, translation workflow | `references/i18n-l10n.md` |

## 5. How to work

1. **Understand before changing:** read the surrounding code and helpers; reuse before writing.
2. **Reproduce before fixing**; for a production problem start at Step 0 of the diagnosis playbook (what changed, what signals exist).
3. **State the complexity** (time, extra space) and the I/O count (queries and HTTP calls per request) of non-trivial code.
4. **Measure when claiming a speedup** (n/2n/4n benchmark or a query plan); otherwise say it is expected, not proven.
5. **Prefer the boring framework solution** over custom code.
6. **Keep changes scoped;** list unrelated refactors as follow-ups; flag, do not silently fix, risky pre-existing issues.
7. **Do not optimize** when `n` is small, the code is rare, or the bottleneck is elsewhere; find the critical 3% (Knuth) by measuring.
8. **Audit mode** (`/engineering-playbook audit`, explicit request only): `references/audit-mode.md`.

## 6. Output contract for reviews and optimizations

```
[severity: critical|high|medium|low] <file>:<line> - <problem in one line>
Why: <concrete failure scenario or cost, with numbers if possible>
Fix: <the change> (complexity/IO before -> after; trade-off)
```

Order by severity; separate **must-fix** (correctness, security, data loss) from **should-fix** (performance at real scale) from **nice-to-have**. Say when something is fine and what you could not verify.

## AI tells to avoid (check while answering, not after)

- Generic best-practice lists (validate input, add logging) that ignore the user's stack and files: name the file:line or query they apply to.
- Boilerplate and over-engineering: extra layers, ports, patterns or abstractions with no present need; write the smallest change that works.
- Invented APIs, flags, versions or limits: check the installed version or say "not verified".
- "It depends" without the deciding factor: name it (n, traffic, consistency need) and pick.
- "Fixed" or "faster" with no test, query plan or benchmark: show it or say "expected, not measured".
- Say what you chose and why in one line; a choice without a reason is removed.

## Gaps

- Version-bound facts (frameworks, EU regulation, limits, pricing) age; re-check vendor docs.
- Some reference rules are marked "not re-verified": they come from earlier study notes. The bibliography shows what was re-checked.

