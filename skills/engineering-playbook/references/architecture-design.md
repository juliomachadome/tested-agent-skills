# Architecture & Code Design

## 1. What good design optimizes for

- **Change is cheap and local.** High cohesion (things that change together live together), low coupling (modules know little about each other).
- **Complexity is the enemy** (Ousterhout): symptoms are change amplification, cognitive load, unknown unknowns. Prefer **deep modules** (simple interface, rich functionality) over shallow ones (many tiny pass-through classes).
- **Essential vs accidental complexity** (Brooks, *No Silver Bullet*): only fight the accidental.

## 2. Architectural styles — when to use

| Style | Use when | Watch out |
|---|---|---|
| Layered (UI → App → Domain → Data) | simple CRUD apps | anemic domain, "pass-through" layers |
| **Clean / Hexagonal / Onion** (dependencies point inward to domain; infrastructure behind ports/interfaces) | business rules worth protecting, multiple adapters (HTTP, queue, CLI), long-lived systems | over-abstraction for trivial CRUD; interfaces with one implementation everywhere |
| **Vertical slice** (organize by feature: endpoint + handler + validation + data access together) | many independent features, CQRS handlers | duplication across slices (acceptable if intentional) |
| **Modular monolith** | default for most products/startups; clear module boundaries, one deployable | enforce boundaries (separate projects, internal visibility, architecture tests) |
| Microservices | independent teams/scaling/deploy cadence, proven boundaries | distributed transactions, ops overhead, network failures; don't start here |
| Event-driven | decoupled reactions, integrations, audit | eventual consistency, debugging flows, duplicates |
| Serverless (Functions) | spiky/event-triggered workloads, glue | cold starts, execution limits, local testing, vendor coupling |

## 3. CQRS & Mediator

- **CQRS:** commands change state (validate invariants, return minimal data); queries read (no side effects, can bypass the domain model and use projections/Dapper/`AsNoTracking`).
- **Mediator** (MediatR or source-generated alternatives like `Mediator`): decouples endpoints from handlers and enables pipeline behaviors (validation, logging, transactions, caching). Cost: indirection; navigation is harder. Don't add pipeline magic you can't see.
- Keep handlers small; one handler per use case; no handler calling another handler through the mediator (extract a domain/application service instead).

## 4. Domain-Driven Design (tactical & strategic)

- **Ubiquitous language:** code names match business terms (ask domain experts).
- **Bounded context:** a boundary where a model is consistent; the same word ("Account") can mean different things in different contexts. Integrate contexts via explicit contracts/anti-corruption layers.
- **Entity** (identity), **Value Object** (immutable, equality by value: `Money`, `Email`, `DateRange` — use `record`), **Aggregate** (consistency boundary with one root; modify one aggregate per transaction; reference others by id), **Domain Event** (something that happened), **Repository** (per aggregate root), **Domain Service** (logic not belonging to one entity).
- Keep aggregates **small**; invariants that span aggregates → eventual consistency via domain events or a process manager.
- **Make invalid states unrepresentable:** constructors/factories validate; private setters; no public parameterless constructors for domain types (EF can use private ones).
- **Primitive obsession:** wrap ids and values (`CustomerId`, `Money`) to prevent mixing them up (strongly typed ids).
- Don't use full DDD for CRUD/reporting areas — apply where the business logic is complex.

## 5. SOLID (pragmatically)

- **S**ingle Responsibility: one reason to change (one actor). Not "one method per class".
- **O**pen/Closed: extend via new code (strategies, handlers) rather than editing big `switch`es — when variation is real.
- **L**iskov Substitution: subtypes must honor the base contract (no throwing `NotSupportedException` in overrides).
- **I**nterface Segregation: small, client-specific interfaces.
- **D**ependency Inversion: high-level policy depends on abstractions; infrastructure implements them.
- Plus: **DRY** (knowledge, not text — duplicated code that changes for different reasons is fine), **KISS**, **YAGNI**, **Law of Demeter** (avoid `a.B.C.D.Do()`), **composition over inheritance**, **tell, don't ask**.

## 6. Error handling

- **Exceptions** for exceptional/unexpected failures (infrastructure down, bugs). **Result types** (`Result<T, Error>`, `OneOf`, discriminated unions) for expected business outcomes (validation failed, insufficient funds) — makes failure paths explicit and cheap.
- Pick one convention per codebase and stick to it.
- Never swallow exceptions; catch specific types; preserve stack (`throw;` not `throw ex;`); add context when wrapping.
- Validate at boundaries; inside the domain, trust validated types.
- Map errors to HTTP in one place (exception handler middleware / Problem Details) — see api-design.md.
- Guard clauses and early returns instead of deep nesting.

## 7. Design patterns (GoF) — when they earn their place

- **Creational:** Factory Method/Abstract Factory (choose implementation at runtime), Builder (complex construction, test data builders), Singleton (prefer DI singleton lifetime instead of static singletons), Prototype.
- **Structural:** Adapter (wrap external APIs to your port), Decorator (cross-cutting: caching/logging/retry around an interface — Scrutor in .NET), Facade (simplify subsystem), Proxy, Composite, Bridge, Flyweight.
- **Behavioral:** Strategy (swap algorithms: pricing, plan generation), Observer (events), Command (encapsulate requests — CQRS commands), Chain of Responsibility (middleware, pipeline behaviors), Template Method, State (state machines for order/payment status), Specification (composable query/business rules), Mediator, Iterator, Visitor, Memento.
- Enterprise (Fowler PoEAA): Repository, Unit of Work (EF `DbContext` already is one — don't wrap it in a generic repository without reason), Data Mapper, Money, Special Case/Null Object, Identity Map.
- **Anti-patterns:** God class, anemic domain where logic is complex, generic repository over EF that leaks `IQueryable` or hides useful features, service locator, deep inheritance trees, shotgun surgery, feature envy, boolean parameters controlling behavior, magic strings/numbers.

## 8. Code-level quality

- Names reveal intent; functions do one thing at one level of abstraction; small parameter lists (use parameter objects).
- Immutability by default (`record`, `readonly`, `init`, `const`, `readonly` arrays in TS).
- Nullable reference types enabled in C#; `strict: true` in TypeScript; treat warnings as errors in CI.
- Comments explain **why**, not what. Document non-obvious decisions, invariants and units.
- Cyclomatic complexity: split functions with many branches; replace conditionals with polymorphism/tables when it simplifies.
- Feature flags and configuration over code forks.
- Delete dead code (version control remembers).

## 9. Dependency management between modules

- Enforce boundaries with project references, `internal` visibility, and **architecture tests** (NetArchTest, ArchUnitNET; dependency-cruiser/eslint-plugin-boundaries in TS).
- Shared kernel minimal; avoid a "Common/Utils" dumping ground.
- Contracts between modules: interfaces or messages, not shared entities/DbContext.

## 10. Architecture decisions

- Record significant decisions in **ADRs** (context, decision, alternatives, consequences) in the repo (`docs/adr/0001-*.md`).
- Evaluate with quality attributes: performance, scalability, availability, security, maintainability, cost, time to market. Every choice is a trade-off — state what you give up.
- Reversible decisions → decide fast; irreversible (data model, public API, vendor lock-in) → think and document.

## 11. Laws worth remembering

- **Conway:** systems mirror the communication structure of the org.
- **Gall:** complex systems that work evolved from simple systems that worked.
- **Hyrum:** with enough users, every observable behavior becomes a contract.
- **Postel (contested):** be liberal in what you accept — today prefer strict validation with clear errors.
- **Brooks:** adding people to a late project makes it later.
- **Goodhart:** a metric that becomes a target stops being a good metric.
- **Kernighan:** debugging is twice as hard as writing the code; don't write code at the limit of your cleverness.
- **Amdahl / Little:** see performance.md.
- **Zawinski / Greenspun-style warnings:** avoid reinventing frameworks inside your app.

## 12. Legacy code & refactoring

- Characterization tests before changing untested code (Feathers).
- Small, behavior-preserving steps; separate refactor commits from behavior changes.
- **Strangler fig** for replacing a system incrementally behind a facade/router.
- Seams: introduce interfaces at boundaries to enable testing.

## 13. Proportion: designing for one developer or a small team

- **Start with the simplest design that meets a measured requirement:** one repository, one database, one API process, a queue as a table in that same database. Every extra piece (service, managed queue, distributed cache, replica) needs a number that justifies it: measured latency, a computed ceiling, a cost comparison. (Fowler "Yagni"; Ousterhout ch. 3; not re-verified.)
- **Write the trigger together with the deferral.** "Split the worker out when memory passes 80% or the queue lags more than 10 minutes" is a decision; "we will see later" is not. Put the trigger in the ADR.
- **Silent ceilings hurt small products more than cost does:** a 1000-row result cap, a serial queue, a call with no timeout, a job that stops without an error. Hunt for these before optimizing (Nygard, *Release It!*, "Unbounded Result Sets", "Blocked Threads"; not re-verified).
- **Latency is geography before it is code.** Keep front end, API, database and cache in the same region. An API an ocean away from its database turns every 2 ms query into 100 ms. Check each service's region before any other optimization.
- **Make optional things switchable.** A variant, provider or feature goes behind configuration, and the disabled path is tested. Removing code is a separate decision.
- **Ceremony budget:** formal aggregates, event sourcing, CQRS, a mediator and a generic repository are each a cost. Adopt one only when a concrete problem (invariants spanning tables, audit replay, two read shapes) shows up and a transaction plus plain functions no longer solves it.
- **Cheap design check:** if one piece were removed, what would actually break? If nothing, remove it.

## 14. Ports and adapters in NestJS

- **Layers and one dependency rule:** `domain` (pure rules, no I/O, injected time) <- `application` (use cases orchestrating ports) <- `infrastructure` (adapters: database, payments, email, storage, LLM) and `interface` (HTTP, queue consumers). The domain imports nothing from outside it (Cockburn, "Hexagonal Architecture"; Evans ch. 4; not re-verified).
- **A port is an interface owned by the caller and named in business vocabulary** (`PaymentGateway`, `MediaStorage`), not the vendor's. The adapter translates to the technology. Make a port for anything with an external effect or that needs a test double; not for pure functions and not one interface per class.
- **In Nest an interface is not an injection token** (it vanishes at compile time). Export a `Symbol` (or abstract class) from the same file as the interface and use `@Inject(TOKEN)`. Source: https://docs.nestjs.com/fundamentals/custom-providers (read 2026-11-14, from the input knowledge file; not re-verified).
- **Switching implementations (real vs fake, local vs cloud) is the composition module's job:** `useFactory` with `inject` for configuration, `useValue` for test doubles, `useExisting` for aliases. Never an `if (env)` inside a use case.
- **Providers are private to their module until exported.** Shared modules are singletons; `@Global()` is an exception, not a default. Registering one service in several modules creates separate instances (duplicated state). Source: https://docs.nestjs.com/modules.
- **Enforce the boundary with lint, not goodwill.** `eslint-plugin-boundaries`, `import/no-restricted-paths` or dependency-cruiser: `domain/` and `application/` may not import `infrastructure/` or `interface/`; the ORM client may be imported only inside the persistence adapter folder. A rule that is only written in a document will be broken within a quarter.
- **Thin controller:** validate, call one use case, map the error. One use case = one class = one responsibility. Business rules do not live in the handler.
- **Global exception filter** registered as an `APP_FILTER` provider (so it can receive injected dependencies; `useGlobalFilters()` in `main.ts` cannot). Unknown exceptions become a generic 500. Source: https://docs.nestjs.com/exception-filters.
- **Lifecycle:** shutdown hooks only run after `app.enableShutdownHooks()`; `app.close()` does not end the process while an interval or task is alive. Clean shutdown = stop accepting work, finish current work, exit. Source: https://docs.nestjs.com/fundamentals/lifecycle-events.

## 15. Next.js App Router: server/client boundary and BFF

Version-specific API details belong to the framework vendor's own skill and docs; these are the stable design rules.

- **Data access layer (DAL), server only:** a module (marked `import 'server-only'`) that checks the user, authorizes, and returns a minimal DTO. Only the DAL reads secrets from the environment.
- **A Server Action is reachable by a direct POST** even if no button calls it. Authenticate and authorize inside every action; a check in the page or in a proxy/middleware does not extend to it.
- **Props passed from a Server Component to a Client Component are public.** Pass only what the screen shows. Taint APIs are an extra layer, not the barrier.
- **BFF pattern:** the web server keeps the session in an HttpOnly cookie and calls the business API with a bearer token. The browser never sees the token or internal service URLs. A third party's webhook (payments) should point at the service that owns the queue and the database, not at a front-end function.
- **Large bodies skip the function:** upload and download go straight to object storage through signed URLs, because serverless platforms cap request and response size.
- **One screen, one call when the screen is hot:** an aggregation endpoint returns what the first view needs instead of N calls that each repeat authentication and access checks. Avoid request waterfalls.
- Source: the framework's data-security and backend-for-frontend guides in its documentation, https://nextjs.org/docs (from the input knowledge file, not re-verified); OWASP Session Management Cheat Sheet.

## 16. MVVM with hooks (web)

- **Layers:** `views/` render and own no logic; `viewmodels/` (custom hooks) hold state, derived data and event handlers; `services/` talk to the network and mutate nothing in the UI.
- **Rule: a view calls a viewmodel, never a service.** The view stays testable with a fake viewmodel, and the viewmodel with a fake service. Enforce it with a lint restriction on imports from `views/` into `services/`.
- A viewmodel exposes a small, explicit shape: `{ data, status, error, actions }`. It maps service errors to user-facing states; the view maps states to markup.
- Server data belongs to a data-fetching library or a Server Component, not to hand-written effects. Keep derived values derived (compute, do not copy into state).
- All user-visible strings come from the message catalog (i18n), never literals inside components.

## 17. Short ADR template

Format from Nygard, "Documenting Architecture Decisions" (https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions, read 2026-11-14 via input file; not re-verified). The whole document should be one or two pages, kept in the repository, numbered, never renumbered; a reversed decision stays and is marked superseded.

```markdown
# ADR-NNN: <noun phrase naming the decision>
Status: proposed | accepted | deprecated | superseded by ADR-MMM
## Context
The forces in tension, in neutral tone. Include the measured numbers.
## Decision
"We will ..."
## Alternatives
The simpler option that was rejected and why.
## Consequences
All of them, good and bad, including what we give up.
## Review trigger
The number or event that reopens this decision.
```

Alternatives and Review trigger are additions for small teams (judgment, not part of the original format). Write the ADR before the code; if the decision fits in five lines, five lines are enough. Only architecturally significant decisions qualify: structure, quality attributes, external dependencies, boundaries, how things are built.

## 18. C4 model (diagrams)

Source: https://c4model.com/ (read 2026-11-15). The C4 model describes software at four hierarchical levels and is notation independent, so any boxes-and-arrows tool works if labels are clear.

| Level | Diagram | Use it to show |
|---|---|---|
| 1 | System context | the system as one box, its users and the external systems it talks to |
| 2 | Container | the separately runnable/deployable pieces (web app, API, worker, database, queue) and how they communicate |
| 3 | Component | the major building blocks inside one container |
| 4 | Code | classes and functions; rarely worth drawing, generate it if needed |

Supplementary diagrams on the same site: system landscape, dynamic (a sequence of interactions for one scenario) and deployment.

- For most products, levels 1 and 2 are enough; add level 3 only for the one container that is hard to understand.
- Every box carries a name, a type and a one-line responsibility; every arrow carries a verb and, when relevant, the protocol. A diagram with unlabeled arrows is decoration.
- Keep the diagram next to the code (text-based tools such as Mermaid or Structurizr render from source) so it is reviewed in the same pull request as the change.

## Sources

- Cockburn, "Hexagonal Architecture", https://alistair.cockburn.us/hexagonal-architecture (not re-verified)
- NestJS docs: Custom providers, Modules, Exception filters, Lifecycle events, https://docs.nestjs.com (not re-verified)
- Nygard, "Documenting Architecture Decisions", https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (not re-verified)
- C4 model, https://c4model.com/ (read 2026-11-15)
- Fowler, "Yagni", https://martinfowler.com/bliki/Yagni.html; Ousterhout, *A Philosophy of Software Design* (not re-verified)
- Nygard, *Release It!* 2nd ed. (not re-verified)
- OWASP Session Management Cheat Sheet, https://cheatsheetseries.owasp.org (not re-verified)
