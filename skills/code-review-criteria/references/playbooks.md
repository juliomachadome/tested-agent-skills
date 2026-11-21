# Playbooks: routines for reviewers, authors and teams

Numbers in brackets point to `BIBLIOGRAPHY.md`. Diagnosis of process problems is in `diagnosis-playbook.md`; what to look for line by line is in `what-to-look-for.md`; stack specifics in `stack-checks.md`; wording and the false-positive filter in `writing-findings.md`. Deeper security, QA and engineering topics live in the sibling skills `software-security`, `qa-verification`, `engineering-playbook`; link, do not copy. Evidence tags as in the diagnosis playbook.

## 1. Review checklist by risk order
Run Step 0 first (diagnosis playbook, Part 1). Then, in order; stop reading detail when a blocker already makes the rest moot, and send design objections early [20].
1. **Intent and design**: does the change belong here; does it fit the agreed design [2].
2. **Correctness**: edges (empty, one, limit, duplicate, null), state origin, two calls in parallel, failure between two writes.
3. **Security and tenancy**: guard on each new route; object checked against the caller or tenant; hostile input; secrets and personal data in logs (depth in `software-security`).
4. **Data**: transaction around multi-table writes, migration safety (section 4), deletion and retention.
5. **Performance**: only with a concrete consequence (N+1 in a loop, no limit, no timeout); precise numbers belong to `web-performance`.
6. **Design and complexity**: layering, duplication, speculative abstraction [33].
7. **Tests**: fail without the change; real assertions; dependent tests updated.
8. **Naming, comments, style, docs**: `nit:` only; a formatter owns the rest.
Every blocker needs the finding anatomy (file:line, scenario, label, fix, reproducing test; `writing-findings.md`).

## 2. Large PR (over about 400 human-written lines or 15 files)
1. **Do not start by reading line by line.** Read the description and decide whether the change should exist [20].
2. **Sort the diff**: `git diff --stat`, `git diff -M --color-moved`; list mechanical (renames, moves, generated, formatting), tests, interfaces (types, API shapes, schema), behaviour.
3. **Read order**: tests, then interfaces and schema, then behaviour files, then mechanical files by sampling and by running the tests [20].
4. **Cap each sitting** near 60 minutes and 200-400 lines [30] (vendor figures, **[F]**); note where you stopped.
5. **Ask for a split** when intent is mixed. Strategies: (a) refactor first, behaviour second; (b) one vertical slice per PR behind a flag; (c) stacked PRs, each independently green; (d) schema and migration separate from the code that uses it; (e) move first, edit in a later PR so the move shows as a pure move [6][18].
6. **If a split is refused**, declare coverage in the first line: "Read: files A, B, C fully; D-K sampled; not read: generated lockfile" and do not approve what you did not read.
7. The author helps by sending a map (section 7).

## 3. Reviewing AI-written code
Treat as a competent stranger's draft that cannot be asked why. **[F]**; no controlled study was read for these patterns.
- Read the tests first; invert a condition: does any test fail? Tests that assert the mock or restate the code cannot fail.
- Verify every API and import exists in the installed version; check invented helper names and changed signatures.
- Look for plausible-but-wrong: off-by-one in boundaries, time zones, rounding, silent `catch`, `any` casts, default branches that hide a missing case, copied code with the wrong variable.
- Look for scope drift: files touched that the task did not need; deleted tests; loosened assertions.
- Check the unhappy path: timeouts, retries, null from the database, empty list.
- Run it. A diff that compiles and has green mocks proves little; run the test, hit the endpoint, read the output.
- For auth, tenant, money, data: a human who did not prompt it reads those lines, plus a second tool pass with a clean context if needed (Tree I).
- Ask the author: "which parts did you read and run yourself?"

## 4. Migrations and data changes (review view; build detail in `engineering-playbook`)
- **Compatibility**: old code against new schema, new code against old schema (deploy order). Add before use; remove only after nothing reads it.
- **Locks and size**: does the statement rewrite or lock a big table? Estimate row count; concurrent index creation where the engine supports it; batches for backfills.
- **Reversibility**: is there a rollback or forward fix path; is data destroyed (drop, truncate, type narrowing)?
- **Backfill**: idempotent, resumable, batched, with a count of rows touched before and after.
- **Defaults and nullability**: new NOT NULL columns on live tables; default values computed at write time or by the migration.
- **Tenancy and access**: new table has the tenant column, indexes with it, and the access policy.
- **Evidence**: migration dry-run output on a copy, row counts, query plan for new indexes. No evidence for a data change: "not verified" on the verdict.
- Two reviewers (section 8).

## 5. Triage of an AI reviewer's comments (or any 20+ comment automated pass)
Build a table: id, file:line, claim, class, verified how, action.
| Class | Test | Action |
|---|---|---|
| Real, verified | You reproduced or traced it | Convert to the finding format with label |
| Already guarded | Caller, middleware or type prevents the path | Drop; note why once |
| Tool-owned | Formatter, linter or type checker should catch it | Drop; propose the rule |
| Pre-existing | Not made worse by this diff | `FYI:` or ticket |
| Preference | No written rule | `nit:` at most, usually drop |
| Generic worry | No scenario | Drop |
| Wrong | The claim misreads the code | Drop; if a pattern, tune the tool |
Then report counts ("25 comments: 4 real, 3 tool-owned, 2 pre-existing, 9 generic, 7 wrong"), keep at most 8 findings, and verify the 4 real ones. Count again after the fix commit; do not let "resolve all" stand in for answering.

## 6. Comment templates and labels
Labels: **blocking**, **follow-up**, **nit:**, **optional:** or **consider:**, **FYI:** (aligned with the written Google practice for nit, optional and FYI [3]; Conventional Comments offers a wider vocabulary such as issue, suggestion, question, praise with blocking or non-blocking decorations [37]). Unlabelled comments read as required.
```
blocking · path/file.ts:57
When <condition>, <what happens>, so <consequence for a user or the data>.
Fix: <one line>. Test: <the test that fails now and passes after>.

follow-up · path/file.ts:120
Not worse in this diff, but <debt>. Ticket: <id>, owner <name>, done when <acceptance>.

nit: path/file.ts:12  <small improvement, why it reads better>.
optional: <idea>, take it or leave it.
FYI: <information for later, no action here>.
question: <genuine question; if the answer reveals a problem, relabel>.
praise: <specific thing done well, one line>.
```
Rules: comment on the code, not the person; explain why; give a suggestion without rewriting the change [3].

## 7. Author's pre-review checklist and PR template
Before requesting review:
1. Reread your own diff as a reviewer; remove debug lines, unrelated edits and commented code.
2. One idea per PR; refactor separate from behaviour; under about 400 lines when you can [6].
3. Tests added or changed, and one of them fails without the change; CI green with nothing skipped.
4. Run it yourself; attach a screenshot or recording for UI, output for a migration.
5. Self-label risk class (money, auth, data, concurrency) and say what you did not check.
6. Description: first line a short imperative summary; body says why, approach, trade-offs, links, how to test, and what not to review [21].
```
## What and why
## Risk class: none | money | auth | data | concurrency
## How I tested (commands, results, screenshots)
## Review map: read first <tests/interface files>; mechanical: <files>
## Not covered / follow-ups
```
8. When replying: answer every comment; change code instead of explaining when the reviewer was confused; if you disagree, give facts and ask for the scenario [5].

## 8. Team review norms (starting points **[F]**; replace with your own data)
- **Turnaround**: first response within one business day [4]; ask for help when blocked, not silence.
- **Size**: soft limit about 400 human-written lines, hard ask to split above about 800 or 1000 lines [6].
- **Two reviewers** for money, auth and permissions, data migrations and deletion, concurrency primitives, and anything the author flags unverified. A second reader adds independent coverage, and review also spreads knowledge of the code [7][28] (no study was read that proves two readers beat one in risky areas, so this is a team rule **[F]**). Use `CODEOWNERS` plus required review from owners to route and enforce [38][39].
- **Author cannot self-approve**; the same author-model review for sensitive lines does not count (Tree I).
- **Rotate reviewers**; track load per reviewer monthly.
- **Hotfix lane**: allowed, post-merge review within one day, with a reason recorded.
- **Review time is work time**: schedule a daily slot.
- **Inspection origin**: formal inspections (Fagan) used roles, checklists and meetings and reported defect reductions [29]; modern review is lighter, so keep the cheap parts that matter: small units, checklist by risk, and a recorded verdict.

## 9. Approval rules
- **APPROVE** when the change improves code health or at least does not worsen it, even if not perfect [1]. **REQUEST CHANGES** if at least one blocker stands. No "approve but" third state: if a thing truly does not block, it is a labelled non-blocking comment.
- **LGTM with comments** is fine when remaining comments are non-blocking or trivial and you trust the author to address them [4].
- **Re-approval** after new commits that change reviewed code (dismiss stale approvals where the platform supports it [38]).
- **Blocking list**: reproducible bug, cross-tenant or cross-user exposure, broken project rule, test that cannot fail or deleted or skipped test, data written to several tables without a transaction, measured regression on a hot path.
- **Never approve** what you did not read; state coverage instead.
- **Emergency**: urgency lowers the bar for polish, not for correctness; review afterwards.

## 10. Concurrency and async review
Questions to ask, in order, each with a concrete interleaving:
1. What is shared (module state, cache, singleton, connection, file, row)? Who else touches it?
2. Check-then-act on the same row or key: is the guard in the same atomic statement (`UPDATE ... WHERE status = <origin>`; check affected rows) or under a lock? [Postgres isolation notes: 11]
3. Two requests, same job twice (retries, at-least-once queues): is the handler idempotent? is there a unique key?
4. Awaits inside loops that share state; fire-and-forget promises with no error handling; missing `await`; unbounded `Promise.all` fan-out.
5. Timeouts, cancellation and retry with backoff and a cap; retrying a non-idempotent call.
6. Transactions: external I/O inside one holds locks; work after commit that can fail needs an outbox or a retry.
7. Module-scope or per-request state in a runtime where instances serve concurrent requests [19]; singleton provider holding request data [17]; session settings leaking across pooled connections [10].
8. Ordering: events or messages assumed in order; clocks used as ordering.
Ask for a test that forces the interleaving (two parallel calls against the real database), not a comment that says "should be safe".
