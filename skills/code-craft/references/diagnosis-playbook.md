# Diagnosis playbook: smell -> cause -> check -> refactoring

Names follow Fowler's catalogue (Refactoring, 2nd ed). Tags: **[C]** consensus, **[M]** mixed evidence, **[F]** craft. A smell is a prompt to look, not a verdict (studies link some smells to change- and fault-proneness, but effects are modest and confounded with size **[M]**).

## Step 0: is the evidence trustworthy?
1. **Is this the code that runs?** Check the branch, generated files (do not refactor generated code, fix the generator), vendored code, dead code (search callers and the coverage report).
2. **Does it hurt?** Look at history: `git log --format=%h --follow -- file | wc -l` for churn and `git log -S"symbol"` for the bug trail. Code that is ugly but untouched for two years is the worst place to spend effort. Hot and ugly is the target. **[F]**
3. **Are the tests a safety net?** Run them; break a line on purpose; if nothing fails, they do not guard it. No net means characterization tests first (`playbooks.md` 2). **[C]**
4. **What must not change?** Public API, persisted data shape, error messages that clients parse, performance contract. Ask, do not assume.
5. **Measure before judging size.** A 120-line function that is a flat list of steps is less urgent than a 25-line function with five nested branches. Look at nesting depth and number of reasons to change, not lines. **[F]**

## Tree 1: the long function with nested ifs
Symptom: one function validates, loads, decides, saves, notifies; indentation 4+ levels.
- Cause: rules and I/O grew in place (shotgun risk when any rule changes).
- Check: list the decisions as a table (condition -> outcome). Mark which lines touch I/O. If the table has 6+ rows of the same shape, it is data, not code.
- Fix order: (1) guard clauses for invalid input (flatten); (2) extract pure decision into its own function (Extract Function); (3) replace branch ladders by a lookup table or polymorphism only when rows share a shape; (4) leave I/O in a thin shell.

Before (TypeScript):
```ts
function shipping(o: Order): number {
  if (o) {
    if (o.items.length > 0) {
      if (o.country === "BR") {
        if (o.total >= 200) return 0; else return 25;
      } else {
        if (o.total >= 500) return 0; else return 60;
      }
    } else { throw new Error("empty"); }
  } else { throw new Error("no order"); }
}
```
After:
```ts
const FREE_FROM = { BR: 200 } as const;
const FLAT = { BR: 25 } as const;
function shipping(o: Order): number {
  if (o.items.length === 0) throw new Error("empty order");
  const free = FREE_FROM[o.country as "BR"] ?? 500;
  const flat = FLAT[o.country as "BR"] ?? 60;
  return o.total >= free ? 0 : flat;
}
```
Guard clause plus data table; behavior pinned by a table test of 8 rows. If rules become many and differ in shape, use a Strategy per rule (`patterns.md`).

## Tree 2: "this class does too much" (large class, divergent change)
- Check: group methods by the fields they use (clusters = candidate classes); ask "who asks for changes here?" If two different actors do, split (single responsibility = one actor **[F]**).
- Fix: Extract Class along the cluster; keep the old class as a facade only while callers migrate. Do not split by technical layer alone (a `UserValidator`, `UserSaver`, `UserMapper` trio often spreads one idea over three files).

## Tree 3: feature envy
Symptom: a method reads many fields of another object.
```cs
// before
decimal Total(Order o) => o.Lines.Sum(l => l.Price * l.Qty) - o.Discount;
// after: the data owner computes it
public decimal Total() => Lines.Sum(l => l.Price * l.Qty) - Discount; // inside Order
```
Check: does the logic change when that object's data changes? Then move it (Move Function). Exception: Strategy/Visitor, where separation is deliberate.

## Tree 4: shotgun surgery
Symptom: one change touches 6 files. Check: `git log --name-only` shows the same files together (co-change). Cause: one rule duplicated or one concept spread out. Fix: Move Function and Inline to gather the concept in one module; introduce a single owner (a value object, a policy). **[F]**

## Tree 5: primitive obsession and data clumps
Symptom: `string email`, `decimal amount, string currency` travel together; validation repeated.
```ts
// after
class Email { private constructor(readonly value: string) {}
  static parse(s: string): Email { if (!/^[^@\s]+@[^@\s]+$/.test(s)) throw new Error("bad email"); return new Email(s.toLowerCase()); } }
```
Check: does the same validation or the same parameter group appear in 3+ places? Fix: Replace Primitive with Object, Introduce Parameter Object. Money, ranges, ids, and quantities are the usual wins (`ddd-tactical.md`). Do not wrap every string.

## Tree 6: switch/if on type, repeated
Check: the same `switch (kind)` in 2+ places. Fix: Replace Conditional with Polymorphism, or in TypeScript/C# a discriminated union plus exhaustive `switch` (compiler warns on a missing case). One switch in one place is fine. **[F]**

## Tree 7: long parameter list, flag arguments
`save(user, true, false)`. Fix: split into two named functions or pass an options object; booleans that select behavior mean two functions.

## Tree 8: speculative generality, over-abstraction
Symptom: interface with one implementation, abstract base never extended, config for options nobody sets. Check: search usages; if one real implementation and no test double, Inline Class/Collapse Hierarchy. Cost of keeping it: every reader pays. **[F]**

## Tree 9: comments that apologise
A comment explaining what a block does is a prompt to Extract Function with that name. Keep comments for why (a business rule, a workaround with a link, a non-obvious invariant). Delete commented-out code (history has it). **[C]**

## Tree 10: mutable shared state, temporal coupling
Symptom: methods must be called in order (`init()`, then `run()`). Fix: constructor injection, return a value instead of setting a field, make the object immutable. In C# prefer `record` and `init`; in TS `readonly` and `as const`. **[F]**

## Tree 11: tests that break on every refactor
Cause: tests assert on internal calls (mock verification of private collaborators). Fix: test through the public behavior; replace mocks with fakes; delete tests of implementation. See `tdd-and-tests.md`.

## Worked numbers: is it worth it?
A function changed 14 times in 6 months, each change touching 3 branches, bug fixes in 4 of them: roughly 14 x 40 min of extra reading = 9 hours spent. A 3-hour characterized refactor pays back in two changes. A function changed once in two years: leave it.
