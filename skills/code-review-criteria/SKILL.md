---
name: code-review-criteria
description: "Pull request or diff in front of you, invoke this skill FIRST, before reading files or answering, whenever someone wants a verdict on code they did not write or are about to merge, even for one line. Examples \"can you review my PR, it's the diff in feature/bulk-archive vs main\", \"LGTM?\" with a pasted diff of a helper, \"my reviewer says this useEffect is wrong, who's right\", \"should I split this PR\", \"copilot left 30 comments, which are real\", \"approve or block\", \"reviews take days\", \"blocker or nit\". Gives the approval standard, per-diff Step 0 (what changed, risk class, evidence), risk order, concurrency and tenant checks, React pitfalls, test quality, finding format (file:line, scenario, severity, fix), labels, large-PR and AI-code routines, review-process diagnosis. Not for proving a change works end to end (qa-verification), attacker audits (software-security), refactoring or writing the feature (engineering-playbook) or profiling (web-performance)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Code review criteria

Review keeps the codebase healthy while letting changes flow. A reviewer who demands perfection stalls the author; one who approves anything lets the code rot one diff at a time. This skill gives the approval standard, the order to look in, what blocks, and the anatomy of a finding that gets fixed instead of debated. Evidence tags: **[C]** written standard or consensus, **[M]** serious single or correlational study, **[F]** practitioner or vendor rule of thumb, **[X]** myth. Numbers in brackets are entries in `references/BIBLIOGRAPHY.md`.

Boundaries: running a review (fetch PR, post comments) goes to `code-review` skills and `superpowers:requesting-code-review`; answering review as the author goes to `superpowers:receiving-code-review`. Depth in `software-security` (attacks, RLS), `qa-verification` (does it work end to end, false greens), `engineering-playbook` (migrations, idempotency, tenancy design), `web-performance`. Link to them; do not repeat them.

## Project first
Before judging, read the current project's CLAUDE.md or AGENTS.md, lint and style config, ADRs, glossary, review guide, CODEOWNERS and PR template. **Project rules win over this skill**, and a broken written project rule is a blocking finding. If the project has none, use this skill and say so.

## Step 0 for every diff
What changed (size in human-written lines, files, generated or moved code); intended behaviour (ticket, description); **risk class** (money, auth and tenancy, data, concurrency, or none); **evidence** (which CI jobs ran, tests changed, screenshots, migration dry run); who wrote it (human, AI-assisted, AI). Put it in the first lines of the verdict. Details and the tree for process problems (slow reviews, rubber stamps, nit storms, escaped bugs, flaky tests, AI noise): `references/diagnosis-playbook.md`.

## Principles
1. **Approve when the change improves overall code health, even if not perfect.** Block what makes health worse, except in a real emergency; personal preference never blocks. **[C]** [1]
2. **Facts and data beat opinion; the written style guide beats preference.** Equal options: accept the author's. No rule: consistency with existing code. **[C]** [1]
3. **Risk order, by cost to fix later:** correctness > security > data integrity and tenancy > performance > design > tests > style. Raise design objections early. **[C]** [2][20]
4. **Read every human-written line and its surroundings** (callers, readers of the table). If an area is outside your competence, say so and name the specialist. [2]
5. **Verify before you flag.** Read the caller, run the test, reproduce; unverified findings say "(not verified)". False findings spend the trust the next real one needs.
6. **Review finds more maintainability issues than defects.** Two independent classifications found about 75 percent evolvability and 25 percent functional findings; much of the value is shared understanding **[M]** [7][25][26]. So leave what machines can catch (types, lint, tests) to machines, and add tests and monitoring for the bugs review will not catch.
7. **Size shapes quality.** About 100 lines is reasonable and about 1000 usually too large [6]; reading rates near 200-400 lines per sitting and under 500 lines per hour are common guidance **[F]** [30], with an individual-review study favouring about 200 lines per hour or less **[M]** [27]. If you cannot read it all, say what you read and ask to split.
8. **Coverage and participation matter:** components with little review and few reviewers had more post-release defects in three open-source systems (correlational) **[M]** [23]. Do not rubber-stamp.
9. **The reviewer points, the author fixes.** "Fix later" rarely happens: ask for it now or a ticket with an owner. [3][5]
10. **A finding seen twice becomes a lint rule, type or test.**

## Method
1. Step 0, then context: intent, design, acceptance.
2. Tests first (they state what the author believes), then interfaces, then behaviour [20].
3. Size and shape: one idea? refactor mixed with behaviour? Over about 400 lines: `references/playbooks.md` section 2.
4. Walk the risk order with `references/what-to-look-for.md`; apply `references/stack-checks.md` (TypeScript, React, server frameworks, SQL, API errors).
5. Verify each candidate; run the false-positive filter in `references/writing-findings.md`.
6. Write findings and the verdict; mention one specific good thing.

## What blocks, what suggests
| Label | Use for | Blocks? |
|---|---|---|
| **blocking** | Bug with a concrete failure scenario; cross-user or cross-tenant exposure; broken project rule; a test that cannot fail or a deleted or skipped test; measured regression on a hot path; multi-table write without a transaction | Yes |
| **follow-up** | Real debt not worse in this diff; ticket with owner | No |
| **nit:** | Polish that will not hurt | No |
| **optional:** | Might be a good idea | No |
| **FYI:** | Information, not for this change | No |
Labels follow written practice [3]; wider vocabulary in [37]. Severity of the problem: critical (data loss, breach, wrong money), high (core behaviour broken on a reachable path), medium (regression risk, race, slow under real load), low (maintainability). Verified critical or high security or data findings are never filtered out as "low confidence". Verdict: **APPROVE** (with follow-ups or nits) or **REQUEST CHANGES** (at least one blocker). No third "approve but" state; non-blocking items are labelled comments. Comment templates, approval rules and team norms: `references/playbooks.md` 6, 8, 9.

## Finding anatomy
**file:line**, a **concrete failure scenario** (when X, Y happens, consequence Z), **label**, **one-line fix**, **reproducing test**. Without a scenario it is a preference. Comment on code, not the person; explain why.
```
blocking · src/orders/approve.ts:57
Two concurrent approvals both read status=PENDING and both insert an invoice, so the customer is billed twice.
Fix: UPDATE orders SET status='APPROVED' WHERE id=$1 AND status='PENDING'; continue only if rowCount=1.
Test: two parallel approve() calls on the real DB; expect one invoice.
```
Report shape: first line verdict plus Step 0 and what you read and did not read; up to about 8 findings by severity (more means the diff is too big); what you ran (command and result) and what you only read; then "needs <specialist>: ...".

## Which reference to open
| Situation | Open |
|---|---|
| Reviews slow, rubber-stamped, noisy, bugs escaping, flaky CI, AI-reviewer flood, pushback loops, same-model review of sensitive code | `references/diagnosis-playbook.md` |
| Large PR, AI-written code, migrations, concurrency and async, AI-comment triage, templates and labels, author checklist, team norms, approval rules | `references/playbooks.md` |
| Line-by-line checklist in risk order | `references/what-to-look-for.md` |
| TypeScript, React, NestJS-style servers, SQL, API error shape | `references/stack-checks.md` |
| Wording findings, false-positive filter, report format | `references/writing-findings.md` |
| Sources, status of each, what was not read | `references/BIBLIOGRAPHY.md` |

## AI tells to avoid (check while answering, not after)

- Style nits (naming taste, formatting, quote style) raised instead of real defects: each finding needs a failure scenario with file:line.
- Generic checklists ("add tests", "consider error handling") not tied to this diff.
- Invented APIs, flags, versions or limits stated as fact: verify against the code and installed version.
- Over-engineering demanded as a fix (extra layers, abstractions with no current need): ask for the smallest change that works.
- "It depends" or "looks good" with no deciding factor or evidence; a verdict needs the reason.
- "Fixed" or "safe" claimed without a test or command output.
- Say what you chose and why in one line; a choice without a reason is removed.

## Gaps
The ~8-findings cap is a convention. Language checks cover TypeScript, React and SQL only. No figure for AI-reviewer false-positive rates was read. Published review studies are mostly open-source or large-company; small-team numbers here are **[F]**. Paper full texts were not read (see bibliography totals); no figure from them beyond the abstracts is quoted.
