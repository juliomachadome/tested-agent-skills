---
name: code-craft
description: Use for code-level design craft in any language (examples in TypeScript and C#) - "is this clean code", "refactor this", "code smells in this file", "this class does too much", "too many ifs", "which design pattern", "should I use a repository", "value object or entity", "write this test-first", "TDD this feature", mocks vs fakes, SOLID that over-abstracts, aggregates and invariants, anemic domain model, characterization tests for legacy code, result types vs exceptions. Gives a decision per case with the cost of the abstraction, the evidence strength and a small safe step. Not for system design and architecture styles (software-architecture), production incidents and API or database practices (engineering-playbook), PR verdicts (code-review-criteria), test strategy and release gates (qa-verification), or speed (web-performance).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Code craft

Code is read far more than written, so the goal is the smallest design that the next person can change safely. Every rule below is a trade-off with a price; name the price before you apply it. Evidence tags: **[C]** consensus or strong evidence, **[M]** serious but mixed, single-source or correlational, **[F]** practitioner craft, **[X]** myth or dogma. Never copy book text; apply the idea.

## 1. Start: project first, then facts
Read the current project's docs first (CLAUDE.md or AGENTS.md, lint and formatter config, ADRs, glossary, existing tests, how similar code is already written). Project rules and the existing style win over this skill. Then ask for the minimum: the code (not a description), the language and framework version, what must not change, how it is tested today, what hurts (bug, slow change, fear of touching it), and who maintains it. No tests means no safe refactoring: that is step 1.

## 2. The order of decisions
1. **Behavior safe?** No tests around the code means characterization tests first (`references/playbooks.md` 2). **[C]**
2. **What hurts?** Name the pain in one line (hard to change X, bug keeps returning, cannot test Y). No pain, no refactor. **[F]**
3. **Smell, then cause, then smallest move.** Use `references/diagnosis-playbook.md`; do one named refactoring per step, tests green between steps. **[C]**
4. **Rule of three for abstraction.** Duplicate once, abstract at the third real case, and only along a seam that varies. Wrong abstraction costs more than duplication. **[F]**
5. **Pattern last.** Use a pattern to name a solution you already need (`references/patterns.md`). A language feature (function, lambda, union, record) often replaces it. **[F]**
6. **Leave it better, in the same small diff.** Mixed commits (refactor plus behavior) are unreviewable; separate them. **[F]**

## 3. Clean Code versus deep modules
Both camps agree on intent-revealing names, no duplicated knowledge, why-comments and tests. They disagree on size. Tiny functions help against 120-line procedures, but as dogma they scatter one idea across shallow methods (Ousterhout's shallow module). Prefer **deep modules**: a small stable interface hiding real complexity (a `Cache` with get/put). A function does one thing at one level; it need not be 5 lines. No controlled study shows short functions cause fewer defects **[M]**. Criticism of Clean Code examples (mutable state, tiny stateful methods, hidden side effects) is fair **[M]**; keep its naming, boy-scout and test advice. A tactical fix that adds complexity is debt; invest ~10% of effort per change in design. **[F]**

## 4. SOLID, honestly
- **S** one reason to change (one actor), not "one method". **[F]** **O** extend by adding, not editing, but only where change really happens. **L** subtypes must keep the contract; this one is a hard rule. **[C]** **I** small client-shaped interfaces. **D** depend on abstractions at boundaries you must swap or fake (I/O, clock, network), not everywhere. **[F]**
- Over-abstraction smell: an interface with one implementation and no test double; factories for objects that never vary; "Manager", "Helper", "Service" classes holding no rule. **[F]**

## 5. TDD and tests
- Cycle: write a test list, pick one, red (fails for the right reason), green (fake it, then triangulate, or obvious implementation), refactor, repeat. Keep steps small enough that red-to-green takes minutes. **[F]**
- Detroit (classicist, state-based, real collaborators, design emerges) and London (mockist, outside-in, mocks of roles to discover interfaces) are both valid; choose by where uncertainty is. Mock roles you own and need to discover; never mock types you do not own, wrap them in an adapter. **[F]**
- Test double vocabulary (Meszaros): dummy, stub, spy, mock, fake. Prefer fakes and real objects; assert on outcomes, not call order, unless the call is the behavior. **[C]**
- Evidence is **mixed** **[M]**: a 2013 meta-analysis found a small quality benefit and no clear productivity effect; a 2017 dissection found small, uniform steps mattered more than test-first; industrial case studies are not randomized. Say so. Details and citations: `references/tdd-and-tests.md`.
- When not to TDD: exploratory spikes (throw the code away, then test-drive the real one), pure UI layout, thin glue over a framework, and code whose rules you do not yet know. Test after is fine if the tests exist, cover behavior and the code is shaped to be testable. **[M]**

## 6. Patterns and enterprise patterns
Still earn their place: Strategy, Factory, Adapter, Decorator, Observer, Command, State, Template Method, Composite, Builder. Absorbed by language features: Strategy and Command by functions, Iterator by `for-of`/`IEnumerable`, Singleton by DI lifetime, Visitor by pattern matching on unions. Catalogue with when/when-not: `references/patterns.md`. Fowler PoEAA: **transaction script** for simple logic, **domain model** when rules branch and interact, **table module** for set-based record logic; **repository** (a collection-like view of aggregates), **unit of work**, **data mapper** vs **active record** (active record fits CRUD-heavy code), **service layer** for use-case orchestration, **specification** for composable rules. Do not add a repository over an ORM that already is one unless it expresses aggregate boundaries or buys testability you need. **[F]**

## 7. Tactical DDD
Entity (identity), value object (equality by value, immutable, validates in the constructor), aggregate (a consistency boundary that guards invariants; reference other aggregates by id; one transaction per aggregate), domain event (a fact in past tense), domain service (a rule that fits no entity), repository (per aggregate), anti-corruption layer (translate foreign models at the border). The anemic model (data bags plus rule-filled services) is a smell when the rules are complex; it is fine for simple CRUD. **[F]** Strategic DDD (bounded contexts, context maps) and architecture styles: `skills/software-architecture`, not here. Details: `references/ddd-tactical.md`.

## 8. Smells and evidence
Fowler's catalogue (long function, feature envy, shotgun surgery, primitive obsession, divergent change, data clumps) names pain. Studies link some smells to higher change- and fault-proneness (Khomh et al. 2012), but effects are modest and smells co-vary with size. Use smells as prompts to look, not verdicts. **[M]**

## 9. Functional habits in mainstream code
Immutability by default (`readonly`, records), pure functions for rules, effects at the edges, result or option types for expected failures (invalid input, not found) and exceptions for bugs and exhausted infrastructure. One style per boundary; never mix both for the same failure. **[F]**

## 10. Legacy code
Feathers: legacy is code without tests. Find a **seam** (a place to change behavior without editing there: parameter, constructor, subclass, module substitution), write **characterization tests** that record current output, then refactor. Sprout or wrap new code instead of editing tangled code when you cannot test. **[C]**

## 11. Which reference to open
| Need | Open |
|---|---|
| Smell, long function, nested ifs, what to do | `references/diagnosis-playbook.md` |
| TDD walk-through, safe refactoring, adding a pattern, aggregate, review checklist | `references/playbooks.md` |
| GoF and PoEAA catalogue | `references/patterns.md` |
| TDD, doubles, schools, evidence | `references/tdd-and-tests.md` |
| Entities, value objects, aggregates, events | `references/ddd-tactical.md` |
| Naming, comments, errors, SOLID, deep modules | `references/clean-code-and-design.md` |
| Sources and verification status | `references/BIBLIOGRAPHY.md` |

## AI tells to avoid (check while answering, not after)

- Generic clean-code advice not tied to the user's code: cite the file:line and the pain it causes.
- Boilerplate and over-engineering: interfaces with one implementation, factories, layers or patterns with no current need; do the smallest refactoring that works.
- Invented APIs, library features or versions: check the installed one or say "not verified".
- "It depends" between options with no deciding factor, and no recommendation: pick one and give the reason.
- "Refactored, behavior unchanged" with no test that ran: run it or say it was not run.
- Say what you chose and why in one line; a choice without a reason is removed.

## 12. Deliver
Give the decision first, then the smallest step, the code, the test that guards it, the price of the change, and what you could not verify.
