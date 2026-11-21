# Style: CQRS (command query responsibility segregation)

Separate the model that changes state (commands) from the model that reads it (queries). Numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Read shape very different from write shape (dashboards, search, lists with joins); read load far above write load; reads need denormalised or cached views; complex domain rules on the write side; in a bounded context where the extra moving part is justified **[M]** [16].

## When it does not
Simple CRUD; one model serves both well; the team cannot operate eventual consistency; an index, a view or a materialised view would solve it. Fowler warns it adds risk for most systems and should be limited to specific bounded contexts [16].

## Core principles
Commands express intent and may be rejected; queries never change state; the write model protects invariants; read models are disposable and rebuildable; levels of ambition: (1) same database, separate code paths and DTOs; (2) database views or read replicas; (3) separate read store updated by events; (4) with event sourcing (caution: `event-driven.md`). Most needs end at level 1 or 2.

## Structure
`commands/` (handlers, validation, aggregates) and `queries/` (handlers returning DTOs, may use plain SQL); projection workers for level 3; a mediator is optional, not required.

## Data ownership and consistency
Write side is the source of truth. Read model updates through events or change data capture; it lags. Give users read-your-writes where it matters: return the new state in the command response, route the next read to the write store, or pass a version token (`../data-systems.md`). Projections are idempotent and can be rebuilt from the source.

## Operations and failure modes
Projection lag and silent drift, a poisoned event stopping a projection, rebuild time, two schemas to migrate, duplicate logic between models, users seeing stale data after a write. Monitor lag, rebuild duration, reconciliation diffs.

## Migration in and out
In: begin with a read-only query module using SQL views; add a denormalised table fed by an outbox only when measurements demand. Out: drop the read store and point queries at the write database when scale no longer needs it.

## Checklist
Do: justify with a measured read/write mismatch; start at level 1; make projections rebuildable; show staleness in the UI where it matters.
Avoid: CQRS for the whole system; command handlers returning large query results; separate databases by default; mixing in event sourcing without need.

## Fitness functions
Query handlers cannot call write repositories (static rule); projection lag SLO alert; a rebuild-from-scratch test in CI on a small dataset compares to the live read model; test for read-your-writes on critical flows.

## Sources
Fowler, CQRS [16] and EventSourcing [17]; Kleppmann on derived data [1]; Evans for bounded contexts [4].
