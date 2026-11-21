# Style selector

Open the style file that matches the signals below; open several if the project mixes styles. The project's existing style, its ADRs and its DESIGN docs win over this table: extend what exists, and change direction only through a new ADR (`../playbooks.md` 7).

## Signals to file
| Signal in the project or request | Open |
|---|---|
| One deployable, `src/modules` or package-per-feature, "this is getting hard to change", small team, "should we split?" | `modular-monolith.md` (then `microservices.md` only to argue against or plan extraction) |
| Many repos or service folders, per-service pipelines, service mesh or gateway config, "distributed monolith", "we need microservices" | `microservices.md` and `../diagnosis-playbook.md` 3 and 12 |
| Broker or queue config (Kafka, SQS, RabbitMQ, outbox table, `events/` folder), duplicates, lost events, async workflows | `event-driven.md` |
| Event store, "replay", "audit trail as source of truth" | `event-driven.md` (event sourcing caution) and `cqrs.md` |
| Functions config (`serverless.yml`, edge or lambda handlers), cost per request, cold starts | `serverless.md` |
| `domain/`, `ports/`, `adapters/`, `usecases/`, "clean architecture", swap a provider, tests need the database | `hexagonal-clean.md` |
| Slow reads and complex writes, dashboards, read replicas, projections, "separate read model" | `cqrs.md` |
| `tenant_id` columns, RLS policies, plans and tiers, one customer slowing others, per-customer isolation or cost | `multi-tenant.md` |
| No signals, greenfield, user asks "design this" | `modular-monolith.md` as the default, then the matching file for the stated characteristics (`../playbooks.md` 3) |

## Rules
1. Read DESIGN/ADR docs, repo layout, deploy config and team size first; name the style you found and the evidence.
2. Existing style and ADRs win. Propose changes with an ADR, not by silent divergence.
3. Mixed styles are normal: for example a modular monolith whose modules are hexagonal, with an in-process event bus, one CQRS read model for a dashboard, and pooled multi-tenancy with one silo tenant. Say which style governs each area.
4. Choose by forces (characteristics, numbers, team, constraints), not by fashion; the simplest style that meets the stated needs wins.
5. Each file ends with fitness functions: add at least one to keep the chosen style honest.

Scaling out a chosen style (load balancing, autoscaling, replicas): `../scaling-load-balancing.md`.
