# Style: modular monolith

One deployable unit, internally split into modules with enforced boundaries. Source numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Team up to roughly 5-40 engineers, one product, unclear or still moving domain boundaries, need for strong consistency (transactions across features), small ops capacity, early to mid scale. It is the default start **[F]** [18][19].

## When it does not
Parts need different runtimes, hard isolation or compliance zones, very different scaling profiles, or several teams whose releases truly collide even after trunk-based flow and flags. Also when nobody enforces boundaries: then it is a big ball of mud with one deploy.

## Core principles
Modules are cohesive around a business capability; each exposes a small public interface (functions, commands, events) and hides internals; each owns its tables; dependencies form a DAG; shared kernel is tiny and boring. Boundaries are designed as if modules could become services **[M]** [9][10].

## Structure
`src/modules/<capability>/{api (public), domain, application, infrastructure}`; `src/shared` (logging, types, no business logic); one composition root; one pipeline, one database with a schema or table prefix per module. Deploy unit: one container or process, scaled horizontally; background workers may run the same image with another entry point.

## Data ownership and consistency
Each module is the only writer and reader of its tables; others use its interface or subscribe to in-process events. Cross-module work inside one transaction is allowed but kept to a few well-known places (a use case that orchestrates); if two modules need a joint transaction often, merge them. Use an outbox if events must reach outside systems.

## Operations and failure modes
Cheap: one thing to deploy, trace, debug. Failure modes: one bad module (memory leak, hot loop) takes down all; one slow migration blocks everyone; boundary erosion over time ("just this one import"); a shared database lets modules cheat. Mitigate with per-module metrics, resource limits for background jobs, expand/contract migrations, and the fitness functions below.

## Migration in and out
In: from a tangled monolith, carve modules by change-coupling analysis (`diagnosis-playbook.md` 1), one at a time, with interfaces first. Out: extract a module to a service using branch by abstraction or strangler fig (`playbooks.md` 4) when a measurable reason exists; the module's own tables make this feasible.

## Checklist
Do: write a module map and glossary; one owner per module; forbid imports of module internals; keep events in-process until a consumer outside needs them; track change coupling per quarter.
Avoid: a "common" module that grows; cross-module joins in SQL; shared mutable entities; premature extraction "for scale"; splitting by technical layer only.

## Fitness functions
Dependency rules with ArchUnit, dependency-cruiser or import-linter (module A may import only B's `api`); cycle detection; test that SQL touches only the module's schema; PR touching 3+ modules metric; build time budget.

## Sources
Fowler, MonolithFirst and MicroservicePremium [18][19]; Newman [9][10]; Richards and Ford [6][7]; Ford et al. for fitness functions [8]; Azure Architecture Center styles [26].
