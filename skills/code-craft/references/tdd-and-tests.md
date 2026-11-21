# TDD, test doubles and the evidence

Tags: **[C]** consensus, **[M]** mixed or single-source, **[F]** craft. Numbers in brackets point to BIBLIOGRAPHY.md.

## 1. The cycle (Beck [3])
1. Write a **test list** of behaviors and edge cases; do not write them all as code.
2. Pick one; write it so it fails for the right reason (red). Run it: a test never seen failing proves nothing.
3. Make it pass the quickest way: **fake it** (return the constant), **obvious implementation** when you are sure, or **triangulate** (second example forces the generalization).
4. Refactor with all tests green: remove duplication, improve names. Beck's four rules of simple design [25]: passes the tests, reveals intent, no duplication, fewest elements.
5. Cross off, add new cases you discovered, repeat. If you get stuck, take a smaller step. If a step takes more than ~10 minutes to green, revert and go smaller. **[F]**

## 2. Two schools
| | Detroit (classicist) | London (mockist) |
|---|---|---|
| Start | Inside-out, from the domain core | Outside-in from an acceptance test (Freeman and Pryce [4]) |
| Doubles | Real objects, fakes at the edges | Mocks of **roles** that the unit needs, to discover interfaces |
| Verifies | State and results | Interactions (messages sent) |
| Risk | Large setup; slow to discover collaborators | Tests coupled to structure; refactoring breaks tests |
Fowler's account [22] gives the contrast. Choose by uncertainty: clear domain rules, go Detroit; new feature across layers, an outside-in walking skeleton with a failing acceptance test, then unit-test with doubles for roles you own. Rules both schools share: do not mock what you do not own (wrap it in an adapter and test the adapter against the real thing once), and a mock is a design question: if it needs 6 expectations, the unit has too many collaborators. **[F]**

## 3. Test double vocabulary (Meszaros [5], summarized by Fowler [21])
- **Dummy**: passed but never used. **Stub**: returns canned answers. **Spy**: stub that records calls for later assertions. **Mock**: pre-programmed with expectations and verifies them. **Fake**: a working lightweight implementation (in-memory repository, SQLite).
- Prefer: real object, then fake, then stub; use a mock only when the interaction is the behavior (email sent once). Assert outcomes, not call order. Time and randomness: inject a clock or id generator. **[C]**
```ts
class InMemoryOrders implements Orders {
  private m = new Map<string, Order>();
  async get(id: string) { return this.m.get(id) ?? null; }
  async save(o: Order) { this.m.set(o.id, o); }
}
```
Contract test: run the same suite against the fake and the real repository, so the fake cannot drift.

## 4. Good tests (FIRST, one behavior, readable)
Fast, isolated, repeatable, self-validating, written with intent. Name by behavior (`rejects_expired_coupon`). Arrange, act, assert, no logic in tests. Test through the public API. One reason to fail. Property-based tests for rules with large input space (`fast-check`, FsCheck). Test pyramid is a heuristic: most tests cheap and local, few end-to-end; test strategy and release gates belong to qa-verification. **[F]**

## 5. When not to TDD (or not strictly)
- **Spikes** to learn an API or a shape: write, learn, discard, then test-drive the real code. **[F]**
- Pure layout or styling; thin glue over a framework; scripts you will run once.
- Rules still unknown: use examples and conversation first (or exploratory code), then pin them as tests.
- Test-last is acceptable when tests are written the same day, cover behavior and the code is testable; the problem is not order but absent tests. The dissection study [30] points the same way. **[M]**

## 6. The evidence, honestly
- **Rafique and Mišić 2013 [29]**: a meta-analysis of TDD studies. Reported a small positive effect on external quality overall and no reliable effect on productivity; results varied by context (academic vs industry, task size). **[M]** (summary from memory of the abstract; not re-read this pass)
- **Munir et al. 2014 [31]**: systematic review that weighs rigor and relevance; high-rigor studies show mixed or inconclusive effects on quality. **[M]**
- **Fucci et al. 2017 [30]**: a dissection of the process: the order (test-first vs test-last) was not the driver; **granularity** (short cycles), **uniformity** (steady rhythm) and **sequencing** mattered more. **[M]**
- **Nagappan et al. 2008 [32]**: four industrial teams; fewer pre-release defects (large reductions reported) with added development time; not randomized, so selection and context effects remain. **[M]**
- **Erdogmus et al. 2005 [33]**: student experiment; test-first led to more tests and higher productivity in that setting, with no consistent quality advantage. **[M]**
How to say it: "TDD is supported by craft experience and by some industrial case studies; controlled evidence on quality and productivity is mixed. Its most defensible benefits are a regression net and design feedback, and they come from small steps and tests, not ritual." Do not cite single percentages as a general law.

## 7. Legacy seams and characterization (Feathers [13])
A **seam** lets you change behavior without editing at that place. Kinds: object seam (subclass and override a method, pass a fake), parameter seam (add a parameter with default), module/link seam (swap import, DI registration). Techniques: **Extract and Override Call**, **Parameterize Constructor**, **Wrap Method**, **Sprout Method/Class** (new tested code called from old). Then **characterization tests**: assert what the code does today (golden master for large outputs; approval tests). A characterization test documents behavior, not correctness.

## 8. Smells in test code
Mystery guest (data hidden in a file), eager test (many behaviors), fragile fixture, mock overuse, assertion-free test, sleep-based waits, tests that share state, a clock or random seed read inside the unit. Fix by builders, narrower tests, injected time, per-test isolation. **[F]**
