# Patterns catalogue: GoF and PoEAA

Format: intent, use when, avoid when, modern alternative, tiny example. Use a pattern to name a solution you already need; patterns are not goals. Origin: Gamma et al. (GoF), Fowler (PoEAA); Kerievsky shows how to arrive at patterns by refactoring instead of up-front design. **[F]** unless noted.

## Still matter (GoF)
**Strategy.** Intent: swap an algorithm behind one interface. Use when: 3+ variants chosen at runtime or by config (pricing, shipping, retry). Avoid: two variants, no growth. Modern: a function type or lookup map.
```ts
type Discount = (subtotalCents: number) => number;
const rules: Record<string, Discount> = { none: s => 0, vip: s => Math.round(s * 0.1) };
```
**Factory (method / simple factory).** Intent: centralize creation with validation or choice of concrete type. Use when: construction has rules or depends on input. Avoid: `new` of a plain class is enough. Modern: static `create`/`parse` returning a valid object; DI container for lifetimes.

**Adapter.** Intent: translate a foreign interface to the one you want. Use when: wrapping a third-party SDK, legacy API or payment provider; the place where you own the type you mock. Avoid: wrapping your own stable code. Modern: a small interface plus one class (also the anti-corruption layer at module scale).
```cs
public interface IPayments { Task<ChargeResult> ChargeAsync(Money amount, CardToken t); }
public sealed class StripePayments : IPayments { /* maps SDK types to ours */ }
```
**Decorator.** Intent: add behavior around an object with the same interface (logging, caching, retry, authorization). Use when: cross-cutting behavior must stack and be optional. Avoid: one fixed behavior; just call it. Modern: higher-order function or middleware pipeline (`withRetry(fn)`, ASP.NET middleware, `Scrutor` decoration).

**Observer.** Intent: notify subscribers of a change without coupling. Use when: UI state, in-process domain events. Avoid: control flow that must be ordered, transactional or traced (hidden coupling, leaks from forgotten unsubscribes). Modern: events, `EventEmitter`, RxJS, C# `event`; across processes use messaging (software-architecture).

**Command.** Intent: an operation as an object (queue, undo, audit, retry). Use when: you must store, schedule, replay or undo it. Avoid: a plain method call. Modern: a record with data plus a handler (`CreateOrder` and `CreateOrderHandler`); a closure for simple deferral.

**State.** Intent: behavior depends on state, each state its own type. Use when: a lifecycle with many transitions and rules (order: draft, paid, shipped). Avoid: two states and a boolean. Modern: union type plus exhaustive `switch`, or a state table; libraries for statecharts.
```ts
type Order = { s: "draft" } | { s: "paid"; paidAt: Date } | { s: "shipped"; trackingId: string };
```
**Template Method.** Intent: a fixed skeleton with overridable steps. Use when: a framework invites subclassing and the steps are stable. Avoid: when inheritance blocks reuse; Modern: pass the varying step as a function (composition).

**Composite.** Intent: treat a tree of parts and wholes uniformly. Use when: menus, file trees, nested price bundles, specification trees (and/or/not). Avoid: flat lists. Modern: recursive types; one interface with `Evaluate`.

**Builder.** Intent: construct a complex object stepwise. Use when: many optional parts, tests that need readable fixtures (test data builders). Avoid: few parameters. Modern: named arguments, object literals with defaults, C# `init` and `with`; keep builders for test data and fluent queries.

## Absorbed by language features
- Iterator: `for...of`, generators, `IEnumerable<T>`/LINQ. Singleton: use a DI lifetime or module; global mutable singletons hide dependencies and hurt tests. **[C]**
- Visitor: exhaustive `switch` on union types or C# pattern matching (use Visitor only for double dispatch over closed hierarchies across assemblies).
- Prototype: spread/`with` expressions. Memento: immutable values. Null Object: option types or default object; still useful when it removes null checks.
- Abstract Factory, Bridge, Flyweight, Mediator: seldom needed outside large frameworks; check that the simpler options failed first.

## When a pattern is overkill
Signs: more classes than rules; names ending `-Factory`, `-Provider`, `-Manager` with no logic; reading a flow needs 6 files; the second implementation never came after a year. Cost is cognition, onboarding time and slower debugging. Remedy: inline (Inline Class, Collapse Hierarchy), keep the test seam, move on.

## Enterprise patterns (Fowler, PoEAA)
| Pattern | Intent | Use when | Avoid when |
|---|---|---|---|
| Transaction script | One procedure per use case | Simple rules, mostly CRUD, small team | Rules branch and interact; duplication across scripts grows |
| Domain model | Objects with data and rules | Complex, changing rules | Plain CRUD (costly mapping) |
| Table module | One object per table, set-based logic | Reporting-style logic, .NET datasets | Rich object graphs |
| Repository | Collection-like access to aggregates | Domain model; you want to hide persistence and fake it in tests | A thin wrapper over an ORM adds nothing; query-heavy reads (use read models) |
| Unit of work | Track changes, commit once | Several changes in one transaction; `DbContext` and Prisma `$transaction` already do this | Re-wrapping what the ORM provides |
| Data mapper | Separate objects from schema | Domain model that must not know the DB (EF Core, TypeORM data-mapper mode) | Simple tables 1:1 |
| Active record | Object wraps a row and its CRUD | CRUD-heavy apps, fast delivery (Rails, some ORMs) | Rules large enough that persistence noise hides them |
| Service layer | Boundary of use cases; orchestration, transactions, authorization | Several clients (API, jobs, UI) share use cases | Moving rules out of the model into it (anemic) |
| Specification | A composable, testable rule object | Rules combined at runtime or reused for query and validation | A single `if` |

Repository sketch (C#): `IOrderRepository { Task<Order?> Get(OrderId id); void Add(Order o); }` per aggregate, with the unit of work committing in the service layer. Specification sketch (TypeScript): `type Spec<T> = (x: T) => boolean; const and = <T>(a: Spec<T>, b: Spec<T>): Spec<T> => x => a(x) && b(x);`.
Choice rule: start with transaction script; move to domain model when you see the same rule branch in several scripts. Layering and boundaries between modules belong to software-architecture.
