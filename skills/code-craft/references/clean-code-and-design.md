# Clean Code, deep modules, SOLID

Numbers point to BIBLIOGRAPHY.md. Tags: **[C]** consensus, **[M]** mixed, **[F]** craft, **[X]** dogma.

## 1. What both camps agree on
Martin's Clean Code [1] and Ousterhout's A Philosophy of Software Design [2] agree that: names reveal intent; duplicated knowledge hurts; comments should carry what code cannot say; tests protect change; complexity is the enemy. **[C]** They differ on how to divide code.

## 2. Naming
Name for the reader at the call site. Nouns for things, verbs for actions, booleans as questions (`isExpired`). Same word for same concept everywhere (`fetch` or `get`, not both); use the domain's vocabulary (glossary). Length proportional to scope: `i` in a 3-line loop, `unpaidInvoicesOlderThan30Days` in a module. Avoid `data`, `info`, `Manager`, `Helper`, `Util`. If a good name is hard to find, the design is usually unclear. **[F]**
```ts
// before: if (d > 30 && s === 2) ...
// after:
const isOverdue = daysSinceDue > GRACE_DAYS && invoice.status === InvoiceStatus.Open;
```

## 3. Functions
Do one thing at one level of abstraction: the function reads as a short story whose steps are named. Few parameters (3 or fewer; group related ones). No flag arguments. Command-query separation: a function either changes state or returns an answer. Early returns flatten nesting. Size is a symptom: split when you can name a block, not when a line count is reached. **[F]**
Dogma to refuse **[X]**: "functions should be 4 lines" and "every comment is a failure". Tiny shallow functions that exist only to be called once can raise reading cost when you must jump to understand the flow, and extracted helpers with hidden shared state are worse than a clear 40-line sequence. Critics [26][27] show examples where following the book hurt clarity or performance; the Ousterhout-Martin discussion [28] shows the disagreement is about depth versus size, not about quality. **[M]**

## 4. Deep modules (Ousterhout [2])
Module depth = functionality hidden / interface size. Deep: `fs.readFile(path)`, a `Cache.get/put` that hides eviction and locking. Shallow: a class that mostly forwards, or a method whose body is one line of the same complexity as its signature. Practices: hide design decisions (information hiding), pull complexity downward into the module, define errors out of existence (a delete of a missing key is a no-op rather than an exception), design it twice (sketch two interfaces before coding), general-purpose interfaces with a somewhat special-purpose usage. Complexity = anything that makes the system hard to understand or modify; symptoms: change amplification, cognitive load, unknown unknowns. **[M]** (book is expert judgement, not experiment)
**Tactical vs strategic programming**: tactical = get it working, accept small hacks; the hacks compound. Strategic = working code is not enough; spend a small, constant share of every change improving design; leave the area a little better. Rule: when the quick fix needs a comment apologising, redesign the interface instead. **[F]**

## 5. Comments
Explain **why**: business rule, rejected alternative, link to ticket or spec, unit of a value, invariants not expressible in types. Interface comments (what the contract is) are valuable on public APIs (XML docs, TSDoc). Delete: restating code, journal entries, commented-out code, noise like `// increment i`. Write the comment before the code when you design the interface; if it is hard to write, the interface is unclear. **[F]**
```cs
// Stripe retries webhooks for 3 days, so the same event id can arrive twice: dedupe on event id.
```

## 6. Error handling
- Distinguish **expected** failures (invalid input, not found, conflict, payment declined) from **bugs** and **infrastructure** failures. Model expected ones in the return type (result/option, union); throw for bugs and unrecoverable infrastructure; do not use exceptions for control flow in hot paths. **[F]**
- Never swallow: log with context or rethrow with the cause attached. Catch at a boundary that can act. Fail fast on invalid state; validate at the edge, then trust types inside.
- Errors out of existence where the semantics allow (idempotent delete, empty list rather than null).
- C#: `Result<T>`/`OneOf` or `ErrorOr` libraries, or a small custom type; keep exceptions for exceptional cases. TypeScript: `type Result<T,E> = {ok:true;value:T}|{ok:false;error:E}`.
```ts
function parseQty(s: string): Result<number, "NaN" | "range"> {
  const n = Number(s);
  if (!Number.isInteger(n)) return { ok: false, error: "NaN" };
  return n >= 1 && n <= 99 ? { ok: true, value: n } : { ok: false, error: "range" };
}
```
Do not return `null` for both "none" and "error". Never mix result types and exceptions for the same failure in the same boundary.

## 7. Formatting
Let a formatter decide (Prettier, dotnet format, .editorconfig) and stop reviewing whitespace. Related code close; blank line between ideas; declare near use; one team style enforced by CI. **[C]**

## 8. SOLID with prices
| Principle | Helps when | Over-abstracts when |
|---|---|---|
| Single responsibility (one actor) | Two teams or reasons change one class | You split every method into a class |
| Open-closed | Variation is real and recurring (rules, providers) | You build plug-in points for changes nobody asked |
| Liskov | Always: subtype keeps contract, never narrows inputs or strengthens preconditions | Never over-applied; breach means redesign (a Square is not a Rectangle) |
| Interface segregation | Clients need small, role-shaped interfaces | One interface per method |
| Dependency inversion | Boundary you want to fake or swap (DB, clock, HTTP) | Interface for every class; DI container hiding the real flow |
Test: is there a second implementation or a fake in a test? If not, the interface is speculative. SOLID came from Martin's 2000s writing (see [15]); it is a set of heuristics, not laws. **[F]**
Composition over inheritance: inherit only for true is-a with a stable contract; otherwise hold a collaborator. **[C]**

## 9. Functional habits
Immutable values (`readonly`, C# `record`), pure functions for decisions (same input, same output, no I/O), effects at the edges ("functional core, imperative shell"), data transformation by `map/filter/reduce` or LINQ when it reads better than a loop (avoid chains of 8 stages). Domain modeling with unions: make illegal states unrepresentable [17].
```ts
type Payment = { kind: "card"; last4: string } | { kind: "pix"; key: string };  // no optional-field soup
```

## 10. Simplicity rules of thumb
YAGNI for features, not for tests or error handling; the cheapest design that passes tests and shows intent [25]; make the change easy, then make the easy change (Beck's tidyings [20]); prefer boring code your team can debug at 3 a.m.
