# Tactical DDD

Tactical building blocks (Evans [10], Vernon [11][12]). Strategic design (bounded contexts, context maps, subdomain classification) and architecture styles are in `skills/software-architecture`; this file stays at code level. Use tactical DDD where the domain is complex and changing; for CRUD, a transaction script is cheaper. **[F]**

## Value object
Defined by its values, immutable, equal by value, validates on creation, has behavior. Candidates: Money, Email, DateRange, Quantity, Address, Percentage. [24]
```cs
public readonly record struct Money(decimal Amount, string Currency) {
  public static Money Zero(string c) => new(0m, c);
  public static Money operator +(Money a, Money b) =>
    a.Currency == b.Currency ? new(a.Amount + b.Amount, a.Currency)
                             : throw new DomainException("Currency mismatch");
}
```
```ts
class Percentage { private constructor(readonly value: number) {}
  static of(v: number) { if (v < 0 || v > 100) throw new RangeError("0..100"); return new Percentage(v); } }
```
Money rule of thumb: integer minor units or `decimal`, never binary floats; rounding policy explicit (see engineering-playbook for the money details). Value or entity? Ask: do two instances with the same data mean the same thing (value), or do they have a life and history (entity)? A shipping address copied onto an order is a value; a customer is an entity.

## Entity
Identity persists across change; equality by id. Keep identity type explicit (`OrderId`, not `string`). Behavior lives on the entity (`order.Cancel(reason)`), not in a service that flips fields.

## Aggregate
A cluster of entities and values with one **root** and a consistency boundary. Rules (Vernon's four): protect true invariants inside the boundary; design small aggregates; reference other aggregates by id only; use eventual consistency (events) across boundaries. **[F]**
- Invariant needed in one transaction means the same aggregate. "Customer's total credit never exceeds limit" across many orders may be a smell: ask if the business accepts a short inconsistency window.
- One aggregate per transaction; outside code goes through the root. Concurrency: optimistic versioning on the root.
- Too big: many writers contend, load is slow. Too small: invariants leak into services.

## Domain event
A fact that happened, past tense, immutable, small payload (`OrderPaid { OrderId, PaidAt, Total }`). Raised by the aggregate, dispatched after commit; handlers may be in the same process (a list of handlers) or published to a broker (outbox pattern for reliability; see engineering-playbook). Events are not commands: no reply expected.

## Domain service
A stateless operation that fits no entity and uses domain language (`TransferFunds(from, to, amount)`, `PricingPolicy`). Smell: a service with all the rules and entities as bags of properties (anemic model [23]). Fowler's criticism: it brings the cost of an object model without the benefit; but for simple domains, a script is honest.

## Application service (service layer)
Orchestrates a use case: load aggregate, call a method, save, publish. No rules inside. Handles transaction, authorization, mapping.

## Repository
One per aggregate root; interface in the domain, implementation in infrastructure; collection-like (`Get`, `Add`, no `Update` when a unit of work tracks). Queries for screens go to read models, not repositories. Do not leak `IQueryable` into the domain. **[F]**

## Factory
Use a factory or static `Create` when building an aggregate has rules (generate id, initial state, invariants). Rehydration from storage bypasses it.

## Anti-corruption layer
A translator between your model and a foreign one (legacy system, vendor API) so foreign concepts do not leak. Implement as adapter plus mapping tests. Decision of where to place contexts belongs to software-architecture.

## Anemic versus rich: how to decide
Count rules, not tables. Rules that branch on state, need invariants across fields, and change often belong in the model. Remodel steps: list rules scattered in services; move each next to the data it guards; make setters private; replace primitives with value objects; keep services for orchestration. Check: can an invalid state be constructed? If yes, not done.

## Pitfalls
Entities with public setters; value objects with identity; aggregates holding other aggregates as objects; domain events used as remote procedure calls; repositories per table; "DDD" applied to a CRUD admin screen.
