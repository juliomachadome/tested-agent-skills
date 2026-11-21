# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a wrong measurement makes every branch meaningless. Thresholds are **[F]** (practitioner starting points) unless tagged; the system's own last 8-12 weeks replace them. Tags: **[C]** consensus, **[M]** serious book or paper, **[F]** practitioner, **[X]** myth. Ideas are applied, never copied. Code-level fixes (N+1, indexes, idempotency keys) live in `skills/engineering-playbook`; this file decides which boundary or structure is wrong.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Percentiles, not averages | p50/p95/p99 per endpoint, same window | add histograms before concluding anything |
| Change calendar | releases, traffic campaigns, new tenants, incidents on one timeline | name no cause before aligning |
| Real dependency graph | traces or import graph, not the diagram from last year | generate it (see playbooks.md, C4) |
| Owner map | who owns each module/table/queue (CODEOWNERS, on-call) | assign before refactoring |
| Sample size | one incident is an anecdote; 3 similar ones are a pattern | write "one data point" in the report |

## Core arithmetic (use it in the answer)
- **Chained availability**: serial calls multiply. 0.999^5 = 99.50% (about 3.6 h/month down), 0.999^10 = 99.0%, 0.999^20 = 98.0%. Five 99.9% hops cannot meet a 99.9% promise; add timeouts, fallbacks or remove a hop **[M]**.
- **Fan-out tail**: if each call is slow 1% of the time, P(at least one slow among n) = 1 - 0.99^n: n=10 gives 9.6%, n=100 gives 63%. The user sees the slowest call, so p99 of a dependency becomes the median of the page **[M]**.
- **Little's law**: in-flight = arrival rate x time in system. 200 req/s x 0.25 s = 50 concurrent; if latency climbs to 2 s the same traffic needs 400 slots, so a 100-connection pool saturates and the queue grows without bound **[C]**.
- **Retry amplification**: 3 retries at each of 3 layers is up to 4^3 = 64 calls on the bottom service for one user action.
- **Cost per request**: monthly bill / successful requests, per tenant if possible. Illustrative serverless: 1M requests x 0.2 s x 0.5 GB = 100,000 GB-s; at an assumed 0.0000167 per GB-s that is about 1.7 plus a request fee; the same function at 50M requests is about 83. Egress: 2 TB x an assumed 0.09/GB = about 180. Check current prices; these are placeholders.

## 1. Every change touches many modules
| Likely cause | How to check | Fix |
|---|---|---|
| Wrong boundaries (split by layer or by entity, not by change reason) | change coupling: files that co-change in the same commits (`git log --name-only`, count pairs); a PR touching 5+ top-level folders is common | redraw modules around business capabilities; move the co-changing files together |
| Shared "utils"/"common" imported everywhere | fan-in of that folder in the import graph | split by owner; duplicate small code rather than share domain logic |
| Anemic domain, logic spread in controllers | same rule implemented in 3 places | one owner module per rule; ports in between (styles/hexagonal-clean.md) |
Check: share of the last 50 PRs touching 3+ modules; target falling over time **[F]**. Add a dependency-direction fitness function (playbooks.md).

## 2. Deploys block each other
Causes: one release train for unrelated work; shared database migrations; long-lived branches; flaky shared test suite. Check: deploy frequency per area, lead time, rollback count, queue time in CI. Fix: first trunk-based development, feature flags and per-module tests inside the monolith; extract only if two areas truly need independent cadence **[M]** (Fowler: MonolithFirst, MicroservicePremium).

## 3. "Distributed monolith"
Signals: services must deploy together or in order; one change needs coordinated PRs in 3 repos; synchronous call chains of 3+ hops; shared database or shared "models" library; integration tests need everything running. Check: count of releases that bundled 2+ services; trace depth; tables read by more than one service. Fix: merge back the chatty pair (a bigger service is fine), or cut the chain with a local copy of read data (event-carried state), or make one side async. Rule: if two services cannot be released alone, they are one service **[M]** (Newman).

## 4. Latency rises with fan-out
Check: trace shows N parallel or serial child calls; p99 child vs p50 parent. Fixes: batch or aggregate in one call, cap fan-out, timeout plus hedged request only for idempotent reads, cache or precompute a read model (styles/cqrs.md), return partial results with a degraded flag. Show the numbers: 100 children at 1% slow means 63% slow pages.

## 5. Database is the bottleneck / shared DB between services
| Cause | Check | Fix |
|---|---|---|
| Missing index, N+1, big scans | slow query log, rows examined vs returned | engineering-playbook first; it is usually not an architecture problem |
| Connection exhaustion | active vs max connections, pool wait time | pooler, fewer instances, shorter transactions |
| One hot table or hot key | per-table I/O, lock waits | partition, queue the writes, cache reads (data-systems.md) |
| Several services write the same tables | `pg_stat_statements` by user or role; grep for the table in other repos | one owner per table; others call its API or read a replica view; migrate with expand/contract |
| Reads and writes compete | replica lag vs read share | read replica or read model, with read-your-writes handling |

## 6. Inconsistent data after async flows
Causes: publish after commit can be lost (no outbox); at-least-once delivery without idempotent consumers gives duplicates; no per-key ordering; dual writes diverge; poison message blocks a partition. Check: reconcile counts between source and consumer (orders vs invoices), dead-letter size and age, duplicate ids in the consumer's dedup table, consumer lag. Fix: transactional outbox, idempotency key stored in the same transaction as the effect, dead-letter queue with an owner and alert, a reconciliation job, explicit version or timestamp in events (data-systems.md, styles/event-driven.md).

## 7. Cascading failures and retry storms
Signals: one slow dependency takes down callers; error rate jumps after a brief blip; load stays high after recovery. Check: retry rate vs request rate, thread/connection pool saturation, queue depth, timeouts longer than upstream deadlines. Fix: deadlines propagated and shorter downstream, retry budget (for example at most 10% extra calls) with jitter, circuit breaker, bulkheads, load shedding by criticality, concurrency limits, degrade to cached data **[M]** (Nygard; SRE chapters on cascading failures and overload).

## 8. Noisy neighbour in multi-tenant
Check: per-tenant breakdown of CPU, queries, queue share, p95; top 1 tenant share of load (above 30-40% on pooled resources is a risk **[F]**). Fix order: per-tenant rate limits and quotas, fair queueing or per-tenant concurrency, separate worker pool for heavy jobs, move the big tenant to its own cell or database (styles/multi-tenant.md). Add tenant id to logs, metrics and traces first or you cannot see it.

## 9. Cost exploding (serverless, egress, managed services)
Check: cost per request and per tenant, top 5 line items, idle vs busy share, cross-AZ and internet egress, retries counted as billed invocations, chatty functions calling functions. Fix: batch work, cache at the edge, keep data and compute in one region/zone, reserved or steady-state capacity for flat load (serverless pays off for spiky or low load; at constant high load a container is often cheaper), set budgets and alerts per environment (styles/serverless.md). Compute break-even: monthly serverless cost vs the fixed cost of the smallest instance that handles peak.

## 10. Onboarding a new developer takes weeks
Check: time to first merged PR, time to a running local environment, number of repos and services needed to run one feature, number of people consulted. Causes: too many deploy units for the team, no module map, tribal knowledge, no seeded data. Fix: one-command local run, module README and C4 container diagram, glossary, ADR index, a "first week" issue list; reduce deploy units if a team of N owns more than N/2 services **[F]**.

## 11. Architecture docs are out of date
Causes: diagrams in a drawing tool, no owner, no check. Fix: keep diagrams as text in the repo (Structurizr DSL, Mermaid, PlantUML), generate dependency views from code, review diagrams in the PR that changes a boundary, ADRs immutable and superseded not edited, a quarterly 30-minute "diagram vs reality" check; delete docs nobody owns.

## 12. "We need microservices" from a team of 5
Ask first, in this order: (1) what concrete pain (deploy blocking? scale on one axis? isolation?), with a metric; (2) does a modular monolith with enforced boundaries remove it; (3) who is on call for N services, and what is the pipeline, observability and data-consistency plan. Numbers: 5 people and 8 services is under one person per service, and each service adds a pipeline, alerts, a schema contract and failure modes. Typical outcome: modular monolith now, with one extraction candidate and a written trigger (for example "billing needs independent scaling at 20x load or a separate compliance zone"). Record in an ADR with a revisit trigger.
