# Style: microservices

Independently deployable services, each owning one business capability and its data. Numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Many teams (rough rule: more than about 3 teams, or 30+ engineers **[F]**) that need independent release cadence; a domain with stable, well-understood bounded contexts; parts with very different scaling, runtime or compliance needs; an existing platform (CI/CD, observability, on-call) so each new service is cheap **[M]** [9][19][26].

## When it does not
Team of 5-10 with one product; boundaries still moving; need for cross-entity transactions; no automated deploy or tracing; the real pain is a slow query or a messy codebase. A "we need microservices" request without a metric is the signal to stop and diagnose (`../diagnosis-playbook.md` 12).

## Core principles
Single business capability per service (bounded context [4][5]); private data, no shared tables; communicate through versioned APIs or events; automate everything (deploy, test, observe); design for failure; team owns its services end to end (Team Topologies, stream-aligned teams [13][31]). Fewer, coarser services beat many nano-services.

## Structure
Repo per service or monorepo with per-service pipelines; each service: API, domain, own datastore, health checks, dashboards. Platform pieces: API gateway or ingress, service discovery or DNS, shared libraries kept thin, contract registry, central logs, metrics and traces.

## Data ownership and consistency
Database per service. No distributed transactions; use sagas with compensation [30], outbox for publish-after-commit, idempotent consumers, idempotency keys on commands. Reads across services: call the API, keep a local read copy fed by events, or compose in a gateway/BFF. Say what the user sees while a saga is half done.

## Operations and failure modes
Cost: N pipelines, N alerts, versioning, network failure, partial failure, higher latency, harder debugging, security between services. Failure modes: distributed monolith, chatty sync chains (availability 0.999^n), retry storms, version skew, shared-library coupling, ownership gaps, cost of idle services. Mitigate with timeouts, deadlines, retry budgets, circuit breakers, bulkheads [11][28][29], consumer-driven contract tests, SLOs per service.

## Migration in and out
In: strangler fig from a monolith, one capability at a time, data last-but-planned (`../playbooks.md` 4) [10][15]. Out: merge services that always deploy together or share data; fold back into a module (cheap if boundaries were clean).

## Checklist
Do: justify each service with a reason and a metric; one owner and one on-call; timeouts everywhere; contract tests; a service template (logging, tracing, health, CI); ADR per extraction.
Avoid: shared database; sync chains over 3 hops; one team per 10 services; sharing domain models by library; splitting before the monolith's modules exist; a service per entity.

## Fitness functions
Services deployable alone (pipeline test deploys one with others pinned to old versions); no cross-service DB access (network policy and credentials); max call depth in traces; contract tests green; p99 and error budget per service; cost per service report.

## Sources
Newman, Building Microservices and Monolith to Microservices [9][10]; Fowler, MicroservicePremium [19]; Nygard [11]; SRE book chapters on cascading failures and overload [28][29]; Azure microservices style [26]; Skelton and Pais [13].
