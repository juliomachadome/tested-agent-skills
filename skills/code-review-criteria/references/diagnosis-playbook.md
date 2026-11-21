# Diagnosis playbook: review-process problems, per-diff Step 0, how to check, how to fix

Two parts. **Part 1** is the per-diff Step 0 you run before reading code. **Part 2** is a tree of review-process symptoms (slow, rubber-stamped, noisy, escaping bugs). Evidence tags: **[C]** consensus or written standard, **[M]** serious but single or correlational study, **[F]** practitioner or vendor, **[X]** myth. Numbers tagged [F] are starting points; the team's own last 8-12 weeks replace them. Numbers in brackets like [25] point to `BIBLIOGRAPHY.md`. Nothing is copied from a source; ideas are restated.

## Part 1. Step 0 for every diff (before the first line of code)

| Question | How to answer it | If the answer is bad |
|---|---|---|
| What changed? | `git diff --stat <base>...<head>`; separate generated files, lockfiles, renames (`git diff -M --stat`), tests, production code. Count only human-written production lines | Under 5 minutes of reading to sort; if the author did not say, ask for a description [21] |
| What should it do? | Ticket, acceptance criteria, design note, PR description | No stated intent: ask first; you can only find syntax errors otherwise |
| Risk class | Tag the diff: **money** (price, tax, refunds, credits), **auth** (identity, permissions, sessions, tenant scope), **data** (migration, deletion, retention, personal data), **concurrency** (shared state, queues, retries, locks, caches), **none of these** | Any tag set: two-reviewer rule and specialist (`software-security`, `engineering-playbook` for migrations) in `playbooks.md` 8 |
| What evidence exists? | CI status (which jobs ran, not just green), new or changed tests, screenshots or recordings for UI, a benchmark for performance claims, a migration dry-run output | No evidence for a risky class: "not verified" goes on the verdict, or you request it. Green CI with skipped or retried jobs is not evidence |
| Who wrote it? | Human, AI-assisted, AI-generated, mixed | AI-generated or security-sensitive: `playbooks.md` 3 and Tree F/H below |
| Size | Human-written production lines changed, files touched | Over about 400 lines or over 15 files: Tree A before reading |

Write the Step 0 result as the first lines of your review ("risk: auth + data; evidence: unit tests only, no integration run; size: 640 lines, read 640") so the author can correct a wrong assumption early.

## Part 2. Core arithmetic

- **Review rate.** Studies and vendor material converge on slow, bounded reading: individual review rates at or below about 200 lines of code per hour caught more defects in a personal-process dataset (371 and 246 programs; correlational) [27]; a vendor write-up of a large peer-review programme recommends under 500 lines per hour, 200-400 lines per sitting and sessions near 60 minutes [30] (vendor, label **[F]**). The written Google guidance calls roughly 100 lines reasonable and 1000 usually too large, and also counts files [6].
- **Example 1, one PR.** 800 human-written lines at 300 lines per hour = 2.7 focused hours. With a 60-minute session cap that is 3 sittings, so it will not be done "between meetings"; expect it to sit for days, or to be skimmed. Split into 4 PRs of 200 lines: each is a single 40-minute read.
- **Example 2, reviewer capacity.** 8 developers, each opening about 250 reviewable lines a day = 2000 lines per day. 5 reviewers who give 1 hour per day at 300 lines per hour = 1500 lines per day. Backlog grows 500 lines per day; after 10 working days 5000 lines are waiting (about 17 hours of reading). The fix is smaller PRs, more reviewer hours or fewer authors per reviewer, not "review faster".
- **Cycle time** = first reviewer response time + rounds x (author turn + reviewer turn). Report median and 90th percentile separately: one stuck PR does not move the median but dominates the pain. Written target at Google is a response within one business day [4]; their log study of 9 million reviewed changes reports review latency in hours at the median and most changes small [22] (read the paper for the exact figures; not copied here).
- **What reviews find.** Two independent classifications (industrial and student code reviews [25]; over 1,400 changes in two open-source projects [26]) found about 75 percent of review findings were maintainability or readability ("evolvability") issues and about 25 percent functional defects **[M]**. Interviews and surveys at a large software company show the same gap between what people expect (defects) and what they get (knowledge transfer, shared understanding, alternative solutions) [7] **[M]**. Plan reviews as a maintainability and understanding gate that sometimes catches a bug, not as the bug filter.

## Part 2. Symptom trees

### Tree 0: is the review data trustworthy?
| Check | How | If it fails |
|---|---|---|
| Definitions | "time to first review" starts at "ready for review", not at first push; draft time excluded; bot comments excluded | Recompute; write the definition next to the number |
| Denominator | PRs merged without any human review are in or out? | Report both; a low median hides the unreviewed ones |
| Sample | 20-30 PRs read by hand per finding | Do not change process on 3 anecdotes |
| Mix | Weekly releases, reverts, hotfix lanes | Separate hotfixes from normal flow |

### Tree A: reviews take days
| Likely cause | How to check | Fix |
|---|---|---|
| PRs too large | median human-written lines per PR; share over 400; correlate size with time to first review | Size limit and split strategy (`playbooks.md` 2); stacked PRs; separate refactor from behaviour [6] |
| Reviewer load or one bottleneck | review requests per reviewer per week; share handled by top 2 reviewers | Round-robin or CODEOWNERS groups [39]; cap load; teach second reviewers |
| No agreed turnaround | histogram of first-response time; many above 1 business day | Team norm: first response within one business day [4]; time-box a daily review slot |
| Waiting on CI | PR open to green time | Fix CI first (Tree G); do not blame reviewers |
| Round trips | rounds per PR; comments that block versus nits | Label comments (`playbooks.md` 6); LGTM-with-comments for non-blocking [4] |
| Unclear PR description | reviewers' first comments are questions | PR template (`playbooks.md` 7) [21] |

### Tree B: rubber-stamp LGTM
| Likely cause | How to check | Fix |
|---|---|---|
| Diff too large to read | approvals on PRs over 800 lines with under 10 minutes between open and approve | Size limit; "I read X, not Y" in the verdict |
| Social or time pressure | approvals cluster at release time; same pair always approving each other | Rotate; protect review time; require non-author approval [38] |
| Reviewer lacks context or expertise | approvals with zero comments in areas of one owner | Code owners [39]; second reviewer for risky areas |
| Process counted, not read | metric is "approved", not "what was checked" | Require the Step 0 line and one specific observation in each review |
Link to outcomes: in three open-source systems, components with low review coverage and low participation had more post-release defects (estimates of up to about two and five more per component) after controlling for size and churn **[M]**, correlational [23]. The extension study repeated the question over more systems [24] (abstract not read this pass). Treat as a reason to keep coverage high, not a guarantee.

### Tree C: nitpick storms and bikeshedding
| Likely cause | How to check | Fix |
|---|---|---|
| Style is argued by humans | share of comments about formatting, naming, quotes | Formatter and linter in CI; a finding seen twice becomes a rule |
| Missing written guide | same preference debated across PRs | Write the rule or accept the author's choice; no rule applies means consistency with existing code, and personal preference never blocks [1] |
| Easy topics soak attention | long threads on names while a design flaw has zero comments | Review in risk order; raise design first [20] |
Fix the comment, not the person: label `nit:` and stop at three; if there are more, propose a rule.

### Tree D: AI-generated PR, or an AI reviewer with 30 comments
| Check | How | Fix |
|---|---|---|
| Triage the comments | classify each: real bug (verified), already guarded upstream, style a tool should own, pre-existing, generic worry, wrong | `playbooks.md` 5 triage table; drop false positives, never "resolve all" |
| Verify before acting | read the caller, run the test, reproduce | Unverified AI comment is a hypothesis, not a finding |
| Volume rule | more than about 10 comments on a 150-line diff | Ask the tool for severity-only, or cap the report; keep a human verdict |
| AI-written change | plausible but wrong API use, invented helpers, tests that assert the mock, broad `any`, silent catches, dead branches | `playbooks.md` 3; read the tests first; run it |
Honest limit: there is no published figure here for AI-reviewer false-positive rates that this skill read; measure your own by classifying 50 comments.

### Tree E: author pushback loops
| Likely cause | Fix |
|---|---|
| Comment is a preference, not a problem | Relabel `optional` or drop; style guide beats preference [1] |
| Reviewer was unclear | Add the scenario and a fix; explain why [3] |
| Real disagreement on design | One written exchange; then a call; escalate to a tech lead with the two options and evidence |
| "I will fix it later" | Cleanup now, or a ticket with an owner; later rarely happens [5] |
| Reviewer is right and the author is defensive | Facts and data first; keep the tone on the code [3] |

### Tree F: bugs escape review
| Question | Check | Fix |
|---|---|---|
| Was it reviewed at all? | merge records of the escaped bug's PR | Required review [38] |
| Reviewed but too big? | PR size, approval time | Size limit (Tree A, B) |
| Was it in the risk class that needs two readers? | tag the escaped bug against the Step 0 classes | Two-reviewer rule, specialist |
| Could a test have caught it? | write the failing test now | Add it; a repeated class becomes a lint rule or type |
| Realistic expectation | **[X]** "review will catch our bugs" is a myth: published classifications find mostly maintainability issues [25][26] | Add tests, types, static checks, canary and monitoring; use review for design and understanding |

### Tree G: flaky tests hide regressions
| Check | Fix |
|---|---|
| Rerun-to-green count per week; tests that fail then pass on retry | Quarantine with an owner and a date; do not merge on a retry you did not read |
| A real failure explained away as "flaky" | Require the failing test name and a rerun log in the PR |
| Skipped or `.only` tests | Block; see `qa-verification` for false greens |
Flaky tests make green CI meaningless as evidence in Step 0; say so in the verdict.

### Tree H: huge refactor mixed with behaviour change
Symptom: 2,000 lines, a rename plus a rule change. Check: `git diff -M --color-moved` to separate pure moves; ask which lines change behaviour. Fix: split into (1) mechanical move or rename, reviewed by diff tool and tests unchanged; (2) behaviour change, small; (3) cleanup. Fowler's catalogue names the moves, so the PR description can list them [18][32]. If a split is impossible, review order is tests, interfaces, behavioural files, then mechanical files by sampling, and say what you sampled.

### Tree I: security-sensitive diff reviewed by the author's own model
Risk: the same model family and context that wrote the code tends to share its blind spots; no independent check. Check: who or what reviewed auth, tenant, money, data. Fix: a different human reviewer for those lines, a different tool or model with a fresh context for a second pass if humans are scarce, and a specialist review (`software-security`); tag the verdict "not independently reviewed" when none exists. Evidence for same-model blind spots is **[F]**; no study was read.

### Tree J: tests that cannot fail
Check: invert the main condition or comment out the fix; does any test go red? Assertions like `toBeDefined`, only the mock is asserted, the test recomputes the code under test, snapshot updated blindly. Fix: block with the failing-test request; the fix must come with a test that fails without it.

## What this playbook does not cover
Attacker-style audit (`software-security`), end-to-end proof that a feature works (`qa-verification`), implementation and refactoring (`engineering-playbook`), profiling (`web-performance`).
