---
name: software-architecture
description: Software architecture and system design - invoke this skill FIRST, before answering, for any system-level question, even a short one. Examples - "do we need a message queue for emails and PDFs or is a direct call fine", "write an ADR for row-level security versus schema-per-tenant", "draw the C4 context and container diagram from this repo structure", "should we split into microservices", "add a cache", "multi-tenant architecture", "noisy neighbour", "distributed monolith", "duplicate events", "this is getting hard to change", review this architecture, structure the modules. Picks a style from the project (modular monolith, microservices, event-driven, serverless, hexagonal/clean, CQRS, multi-tenant), trade-offs by characteristics, data and consistency, outbox and idempotency, stability patterns, 12-factor, fitness functions, strangler fig, ADRs. Prefers the simplest design that meets the stated needs. Not for code-level practices (engineering-playbook) or LLM features (llm-engineering).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Software architecture

Architecture is the set of decisions that are costly to change. Make few of them, make them late enough to have evidence, write each down with its reasons, and check them with automated tests. Everything is a trade-off; there is no best design, only the least bad one for stated needs (Richards and Ford) **[M]**.

Evidence tags: **[C]** consensus · **[M]** serious book or paper, one school · **[F]** practitioner opinion · **[X]** myth. Say which numbers you assumed and which facts you could not verify.

## 1. Start: read the project
Read the project's own docs first: CLAUDE.md, DESIGN and ADR files, glossary, repo layout, lint and dependency rules, deploy config, team size, load numbers, incident history. Project rules and past decisions override this skill; propose changes through a new ADR rather than silently diverging.

## 2. Choose the style
1. Name the style the project already uses, with evidence (folders, configs, ADRs). Mixed styles are normal; say which governs each area.
2. If there is none or the request is a new design, start from needs (step 3), then open the matching file through `references/styles/README.md` (selector table of signals and requests).
3. The existing style and its ADRs win. Change direction only with an ADR and a migration path.

## 3. Start from needs, not patterns
1. Name the 3-5 characteristics that matter most (availability, latency, correctness, tenancy isolation, cost, changeability, operability) with target numbers. You cannot optimise all **[M]**; a weighted scoring table is in `references/playbooks.md` 3.
2. List constraints: team size and skills, budget, law, existing systems, deadlines.
3. Write quality scenarios: "when X happens, the system does Y within Z".
4. Generate at least two options, including "do the least"; compare against the scenarios; pick one; record why (`references/adr-template.md`).

## 4. Default shape: modular monolith first
One deployable with strong internal modules is the right start for most teams **[F]** [Fowler: MonolithFirst, MicroservicePremium]. Modules own their data and expose a narrow interface; dependency direction is enforced by lint or tests; shared code is small and boring. Extract a service only for a measured reason: independent scaling, different runtime or team cadence, a hard isolation or compliance boundary, or a failure domain. Detail: `references/styles/modular-monolith.md`, `microservices.md`.

## 5. Domain boundaries (DDD)
Ubiquitous language shared by code and business (glossary in the repo); bounded contexts where terms change meaning; aggregates as small consistency boundaries referenced by id; domain events for facts others react to (Evans; Vernon) **[M]**. Strategic DDD pays off early; tactical DDD is wasted on plain CRUD. Ports and adapters: `styles/hexagonal-clean.md`. Code-level practice stays in `skills/engineering-playbook`.

## 6. Data and distributed systems
From Kleppmann **[M]**: choose the store by access pattern and consistency need; one relational database solves most problems longer than expected; know your isolation level's anomalies; replication lag, partial failure and clock skew are normal; exactly-once is at-least-once plus idempotency; outbox for "write and publish"; sagas for cross-service work; percentiles, not averages. Checks: `references/data-systems.md`.

## 7. When NOT to add a thing
| Thing | Add only when | Cheaper first |
|---|---|---|
| New service | independent scale, team or isolation reason proven | module with an interface |
| Queue or broker | work outlives a request, needs retry, smooths bursts; idempotent consumers | job table or the database's queue |
| Cache | measured slow path, staleness acceptable, invalidation defined | index, query fix, pagination |
| Event sourcing / CQRS | audit or temporal queries are core, cost accepted | audit table, read view (`styles/cqrs.md`) |
| Kubernetes or platform | many services and a platform team | managed platform, one process |
| Second database | access pattern the first cannot serve at cost | extension or index |
| Rewrite | cost of change exceeds rewrite risk, with strangler plan | incremental refactor behind tests |
Every added component needs an owner, failure story, monitoring and removal plan.

## 8. Stability and operations
Timeouts on every external call and deadlines passed down; retries with backoff, jitter, a cap or budget, only for idempotent or keyed requests; circuit breakers; bulkheads; backpressure and load shedding; honest health checks; graceful degradation; no unbounded queues, caches or result sets (Nygard; Google SRE) **[M]**. 12-factor as hygiene **[C]**. Observability: structured logs with correlation id, metrics, traces, SLOs and alerts on user-visible symptoms.

## 9. Multi-tenancy
Silo, pool or bridge by isolation need and cost; tenant identity from the verified session, enforced in one layer plus database policy; tenant in every cache key, queue message, log and metric; per-tenant limits; cross-tenant tests; per-tenant backup and deletion. Detail and cost per tenant: `styles/multi-tenant.md`.

## 10. Communicate and verify
C4 context and container diagrams for almost everyone, kept as text in the repo (recipe in `playbooks.md` 6) **[M]**. Fitness functions: automated checks for dependency rules, latency budgets, module-owned tables, cycles, cost per request (examples in `playbooks.md` 5) **[M]**. Review questions: what must stay changeable, what is the failure story, what cheaper option did we dismiss, what breaks at 10x, who gets paged.

## 11. Which reference to open
| Situation | Open |
|---|---|
| Something hurts (coupled changes, blocked deploys, slow, duplicates, cascades, noisy tenant, cost, onboarding, stale docs, "we need microservices") | `references/diagnosis-playbook.md` |
| Review, RFC, scoring characteristics, extracting a module, fitness functions, C4, ADR lifecycle | `references/playbooks.md` |
| Which style fits, or details of one | `references/styles/README.md` then the style file |
| Replication, partitioning, transactions, streams | `references/data-systems.md` |
| Scaling, load balancer, autoscaling, health checks, replicas, shedding | `references/scaling-load-balancing.md` |
| Threat model, authn/authz placement, secrets, tenant isolation, zero trust, audit log | `references/security-architecture.md` |
| Cost per request or tenant, build vs buy break-even, serverless vs containers, egress, FinOps, RTO/RPO, multi-region, residency, cells, DR tests | `references/cost-and-regions.md` |
| Quick yes/no gates (split, queue, cache, consistency) | `references/decision-checklists.md` |
| Writing the decision | `references/adr-template.md` |
| Citing a source or checking its status | `references/BIBLIOGRAPHY.md` |

## 12. Traps to name when you see them
Chained sync calls: five 99.9% hops give 99.5%, so cut hops before adding retries. Services that deploy together are one service. A shared database is coupling, not integration. "Exactly-once" without idempotency keys and an outbox means duplicate charges. A tenant id taken from the request body or missing from a cache key is a leak. A microservices request from a small team starts with the pain and its metric (`diagnosis-playbook.md` 12).

## AI tells to avoid (check while answering, not after)

- Generic best-practice lists (scalability, resilience) not tied to the project's code, load or team: read the repo first and cite file:line.
- Over-engineering: services, queues, caches, layers or patterns with no present need; the cheaper option comes first.
- Options laid out with no recommendation, no numbers and no cost: give one pick, the reason, and the estimate.
- Invented limits, prices, versions or SLAs: cite the source and date or say "not verified".
- "It depends" without the deciding factor: name the quality scenario that decides it.
- Say what you chose and why in one line; a choice without a reason is removed.

## 13. Output
Short design: context and needs, characteristics with numbers, options with trade-offs, recommendation, C4 context and container (Mermaid), risks, open questions, fitness functions, ADR. Review: findings by severity with evidence, the simplest fix, what to leave alone. Diagnosis: symptom, evidence checked, cause, fix, with the arithmetic shown. Mark assumed numbers and unverified facts. Do not implement unless asked.
