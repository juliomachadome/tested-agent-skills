# Playbooks

Five routines. Each ends with a stop condition. Tags as in SKILL.md.

## 1. TDD cycle on a real example (TypeScript, Vitest/Jest style)
Rule to build: "10% off when the cart has 5 or more units; the discount never applies to items already on sale; total never below zero." Prices are integer cents.

**Test list first** (write on paper or as `it.todo`): empty cart = 0; one item = price x qty; 4 units no discount; 5 units 10% off; on-sale items excluded from the discount base; rounding of the discount; rounding direction stated by the owner (ask: half-up?).

**Cycle 1, red**
```ts
it("charges price times quantity for one line", () => {
  expect(total([{ cents: 1000, qty: 2, onSale: false }])).toBe(2000);
});
```
Run: fails because `total` does not exist (right reason: missing behavior, not a typo). **Green by faking it:** `export const total = (_: Line[]) => 2000;`. Triangulate with a second case (`qty: 3` -> 3000), then generalize:
```ts
export const total = (ls: Line[]) => ls.reduce((s, l) => s + l.cents * l.qty, 0);
```
**Cycle 2** `it("gives 10% off at 5 units")` with `[{cents:1000, qty:5}]` expects 4500. Red, then add the rule:
```ts
const units = ls.reduce((n, l) => n + l.qty, 0);
const base = ls.filter(l => !l.onSale).reduce((s, l) => s + l.cents * l.qty, 0);
const sale = ls.filter(l => l.onSale).reduce((s, l) => s + l.cents * l.qty, 0);
const off = units >= 5 ? Math.round(base * 0.1) : 0;
return Math.max(0, base - off + sale);
```
Edge: 4 units gives no discount (boundary test), the on-sale case, the rounding case (`base=1005` -> off 100.5 -> state the rule, test it). **Refactor** (green only): name `qualifiesForBulkDiscount(units)`, extract `subtotal(lines)`. Stop when the list is empty and the design shows the rule in one readable place. Commit on green.
Notes: write the smallest failing test; one behavior per test; never edit a test to pass; if the next test passes at once, it adds nothing (delete it or make it stronger). **[F]**

## 2. Refactoring safely with characterization tests
Goal: change structure, not behavior, of untested code.
1. Freeze scope: one function or class. Note callers (search the repo).
2. Find a seam (`tdd-and-tests.md` section on legacy): a parameter, constructor, or module boundary where you can substitute the clock, the DB or the HTTP client.
3. **Characterize**: call the code with realistic inputs (from logs or fixtures), write an assertion with a deliberately wrong expectation, run, copy the actual value into the expectation (golden master). Cover each branch you see; use a coverage report to find the ones you missed. Record weird outputs as they are; label suspected bugs `// current behavior, likely bug`, do not fix them now.
4. Check the net: mutate a line (flip `>=` to `>`), a test must fail. If not, add cases.
5. Refactor in steps of one named refactoring; run tests after each; commit after each green.
6. Only then change behavior, test-first, in a separate commit.
Stop condition: every extracted piece is covered, the old and new outputs match on the recorded corpus. **[C]**

## 3. Introducing a pattern step by step (Strategy, from an if ladder)
Trigger: the same `if (kind === ...)` ladder exists in two places, or a third variant is requested this month.
1. Characterize current behavior (routine 2).
2. Extract the ladder body into a function per variant (Extract Function), keep the ladder calling them.
3. Give the functions one signature: `type Pricing = (cart: Cart) => Money`.
4. Replace the ladder by a map `Record<Kind, Pricing>`; in C#, `IReadOnlyDictionary<Kind, IPricingRule>` or a `Func<>`.
5. Delete the ladder; make the unknown key fail loudly.
6. Only if variants carry state or need injected services, promote functions to classes behind an interface.
```cs
public interface IShippingRule { bool Applies(Order o); decimal Cost(Order o); }
public decimal Quote(Order o, IEnumerable<IShippingRule> rules) =>
    rules.First(r => r.Applies(o)).Cost(o);   // ordered, last rule is the default
```
Stop condition: adding a variant means adding one entry and one test, no edit to existing code. If you have two variants and no third in sight, keep the `if`. **[F]**

## 4. Modelling an aggregate (Order with lines)
1. List invariants in plain sentences: "an order has at least one line"; "a line quantity is 1..99"; "total = sum of lines, never negative"; "a paid order cannot gain lines".
2. Decide the boundary: which invariants need to be true within one transaction? Those objects live in one aggregate; everything else is referenced by id (`CustomerId`, not `Customer`).
3. One root, state private, behavior as methods that return or record events, no public setters.
```cs
public sealed class Order {
  private readonly List<Line> _lines = new();
  private readonly List<object> _events = new();
  public OrderId Id { get; }  public Status Status { get; private set; } = Status.Draft;
  public Order(OrderId id) => Id = id;
  public void AddLine(Sku sku, Quantity qty, Money unit) {
    if (Status != Status.Draft) throw new DomainException("Order is not editable");
    _lines.Add(new Line(sku, qty, unit));
  }
  public Money Total => _lines.Aggregate(Money.Zero, (s, l) => s + l.Subtotal);
  public void Pay() { if (_lines.Count == 0) throw new DomainException("Empty order");
    Status = Status.Paid; _events.Add(new OrderPaid(Id, Total)); }
}
```
4. Write the tests first from the invariants (build with a tiny test builder). 5. Repository per aggregate: load whole, save whole, optimistic concurrency with a version column. 6. Cross-aggregate effects go through domain events handled after commit (outbox if loss is not acceptable; see engineering-playbook). Stop condition: no code outside the root can break an invariant. Keep aggregates small; a large one causes lock contention. **[F]**

## 5. Review checklist (design level)
Not a PR verdict (see code-review-criteria); use before asking for review.
- Names say what, not how; one word per concept across the code base.
- Each function: one level of abstraction; early returns instead of nesting over 3.
- No flag arguments, no output parameters, no temporal coupling.
- Errors: expected failures typed (result/option) or specific exceptions; no swallowed catch; message says what to do.
- Comments: why only; no commented-out code; TODOs have an owner or ticket.
- Abstractions: each interface has a reason (swap, fake, boundary); no pass-through layers.
- Domain: primitives wrapped where rules live; invariants enforced in one place.
- Tests: behavior not implementation; fakes over mocks; no test depends on order or clock.
- Diff: refactor and behavior change in separate commits; dead code removed.
