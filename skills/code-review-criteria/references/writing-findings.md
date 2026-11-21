# Writing findings, filtering false positives, and review flow

Format: **rule** · why · bibliography number (see `BIBLIOGRAPHY.md`).

## 1. Comment style

1. **Comment on the code, never the person, and explain why.** "This concurrency model adds complexity without a measured gain" instead of "why did you use threads?". State the intent of the comment, the good practice, the effect on code health. · [3]
2. **Label severity so the author can prioritize:** `Nit:` (minor, technically should be done), `Optional`/`Consider:` (may be a good idea, not required), `FYI:` (not for this change). Unlabeled comments read as required. · [3]
3. **Balance explicit direction with letting the author solve it;** a short code suggestion is fine when it removes ambiguity. · [3]
4. **Recognize good things when specific:** one line naming what was done well teaches the pattern and records what you checked. No empty praise; never "LGTM" without reading. · [2]

## 2. False-positive filter (run before publishing any finding)

Drop or downgrade a candidate when:
1. It is **pre-existing** and the diff does not make it worse (mention as FYI at most).
2. It only **looks** like a bug: read the caller, the type, the test; if it is correct, drop it.
3. A **linter, type checker or formatter** would catch it: propose the tool instead of commenting each instance.
4. It is a **style preference** not backed by the project's written rules (nit at most, or nothing).
5. It is a **generic worry** ("might have security issues", "needs more tests") without a concrete scenario: rewrite as a scenario or drop.
6. A written rule names it but the code **explicitly and deliberately** opts out with a reason in place.

Confidence anchors for automated or AI-assisted reviews: 0 = false positive or pre-existing; 25 = maybe real, stylistic, no written rule; 50 = real but minor; 75 = verified and important or in a written rule; 100 = confirmed and frequent. Publish at high confidence only, **except verified critical/high security or data-loss findings, which are always reported.** For high-stakes diffs, a second independent reader (person or agent) validating each finding is a cheap way to cut false positives. · [7] (understanding is the bottleneck); engineering practice

## 3. Large diffs and partial reviews

1. **Small CLs are reviewed faster and more thoroughly, have fewer bugs and are easier to roll back.** ~100 lines reasonable, ~1000 usually too large; file count matters. · [6]
2. **Separate refactoring from behavior changes;** exceptions: deleting whole files, trusted automated refactors. · [6]
3. **If you cannot split and cannot review it fully,** comment on the design, declare on the first line what you read and what you did not, and request changes for the unreviewed part. Approving a whole you did not read is worse than no review. · [6], [4]
4. **For a commit range, review per commit but give one verdict;** order findings by commit to help the author. · engineering practice

## 4. Speed and disagreement

1. **Respond within one business day at most;** fast first response matters more than total cycle time. If busy, say when you will review. · [4]
2. **"LGTM with comments" is right when** the author is trusted to address them, or the comments are minor (import order, nearby typo, unused dependency). · [4]
3. **Do not let a diff stall on disagreement:** seek consensus with facts, record the outcome, escalate to whoever owns the decision (architecture lead, product owner). · [1]
4. **Pushback from the author is often right;** re-read with their argument. If you still hold the point, explain why it matters to code health, not that you prefer it. · [5]

## 5. From finding to rule

1. **Twice is a pattern:** propose a lint rule, type, test or CI check so the class leaves manual review. Examples of rules that commonly earn their place: `no-floating-promises` and `no-misused-promises`, `react-hooks/rules-of-hooks` and `exhaustive-deps`, `jsx-a11y`, no empty catch, banning unsafe raw-SQL APIs, a route-guard coverage test, a test that every UI message key exists. · [2] (tests and tools); engineering practice
2. **Keep the reviewer's notes short:** the repeated pattern, the commit, what was run and what was not; not a scoreboard.

## 6. Report template

```
REQUEST CHANGES  abc123..def456   (read: all of src/orders/*, tests; not read: generated client)

1. blocking · src/orders/approve.ts:57 · parallel approvals both pass the PENDING check -> double invoice · conditional UPDATE + rowCount=1 · parallel approve() test against real DB
2. blocking · src/orders/repo.ts:22 · findById without tenant filter -> tenant A reads B's order by id · add tenant_id to where · two-tenant presence/absence test
3. follow-up · src/orders/list.ts:10 · list without limit grows with history · keyset pagination, limit 50 · test with 51 rows
4. nit · src/orders/approve.ts:80 · magic number 86400 -> SECONDS_PER_DAY

Ran: pnpm vitest related src/orders/approve.ts --run -> 14 passed. Only read: migration 0042.
Good: the refund path is idempotent via the provider key and a unique constraint.
Needs security reviewer: new webhook route signature handling.
```
