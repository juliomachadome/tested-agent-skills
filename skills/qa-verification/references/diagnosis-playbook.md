# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a green or red result you cannot trace to a commit, an environment and a real test count says nothing. Evidence tags: **[C]** consensus or standard, **[M]** serious single source or correlational, **[F]** practitioner or vendor, **[X]** myth. Thresholds are **[F]** starting points; the team's own last weeks of runs replace them. Source ids (Q..) point to `BIBLIOGRAPHY.md`. Nothing is copied.

## Step 0: is the evidence trustworthy?
| Ask | How to check | If it fails |
|---|---|---|
| What changed? | `git diff --stat <base>...HEAD`, changed config, lockfile, env vars, migrations | no diff and no criteria: ask, do not run everything |
| What risk class? | money, access to others' data, personal data, lost work, first use, irreversible, production-only (keys, domains, webhooks, cron) | high class raises the bar of evidence, not the number of tests |
| Which environment and build? | commit SHA, build id, URL, port, branch, feature flags; is the server reused from an older run? | record them next to every result; unknown = NOT VERIFIED |
| Which tests ran, real counts? | `--list` before, "N passed, M failed, K skipped, F flaky" after, exit code | 0 ran, or count lower than expected: stop, it is a failure (Q7, Q9) |
| Was the log the full one? | `cmd \| tail` or `\|\| true` can hide the exit code | rerun with `set -o pipefail`, read `$?` |
| Is the claim at the right level? | unit green is not "screen works"; mocked E2E is not "production works" | downgrade the claim or add the missing level (Q1) |

## Tree A: tests green but the bug is in production (false green)
| Likely cause | Check | Fix |
|---|---|---|
| Zero tests ran (filter, wrong project, `--passWithNoTests`) | CI log count; `--list` | fail the gate on 0; remove the pass-with-no-tests flag (Q7, Q9) |
| Skipped or `.only` | grep `test.skip`, `.only`, `fixme`; `forbidOnly` set? | forbid `.only` in CI; list skips with reasons (Q10) |
| Stale build or reused server | build id and commit served vs commit tested | `reuseExistingServer: false` in CI; print the SHA from the running app (Q14) |
| Mocks that lie | mock fields vs real response; recorded real payloads | validate real responses against the shared schema; contract test (Q22) |
| Wrong environment | prod env vars, keys, domains, webhooks, cron, CDN cache, feature flags | smoke the real environment after deploy (Q27) |
| Assertion that cannot fail | no `await`, `toBeDefined`, value read once | break the code on purpose; the test must go red (Q11) |
| Retry hid a flake that was a real race | report lists "flaky"; trace of the first attempt | treat flaky-pass as a defect; `--fail-on-flaky-tests` (Q10) |
Then add the missing test at the lowest level that fails on the old code.

## Tree B: flaky E2E
Measure first. Run the single test `--repeat-each=30` with 1 worker, then with the CI worker count. Fails alone = timing or selector or app race; fails only in parallel = shared state; fails only after another test = order dependence. Fowler lists the same families: lack of isolation, asynchronous behaviour, remote services, time, resource leaks (Q34); the empirical study of flaky tests found async waits, concurrency and test-order dependence among the commonest root causes (Q35).
| Cause | How to recognise | Fix |
|---|---|---|
| Timing, fixed sleeps | `waitForTimeout`, `sleep`, passes slower machine | web-first assertion that waits for the state (Q13) |
| Shared state | same user, same row, same cart across tests or workers | one account or tenant per test or worker; seed through API; clean up |
| Selectors | CSS or XPath tied to layout, text that changes, several matches | role, label and test-id locators; strict mode errors are a signal (Q13) |
| Network | real third party, variable latency, rate limit | mock third parties at the network edge; wait for the specific response |
| Test order | passes alone, fails in suite, or the reverse | run `--shard`/random order; remove dependence; each test sets up its own state |
| Clock and data | date, time zone, "today", random ids | fixed clock (Q14), fixed seeds |
Check the trace of a failed run (Q14) before changing code: it shows the DOM and network at the failure.

## Tree C: slow suite
| Likely cause | Check | Fix |
|---|---|---|
| Not parallel | workers = 1 on CI, one giant file | split files, raise workers to what the runner has, shard across jobs |
| Pyramid shape upside down (ice-cream cone) | count tests per level and time per level | move rules to unit or integration; keep E2E for few paths (Q28, Q5) |
| Over-E2E | every validation message tested in the browser | one E2E per journey, the rest at component or API level |
| Over-mocking | thousands of unit tests, none touching a real DB | a few integration tests against a real database (Q6) |
| Login in every test | UI login repeated | saved auth state (Q14) |
| Whole suite for a small diff | no selection | `related`, `--filter=...[ref]`, `--only-changed` (Q7, Q8, Q9) |

## Tree D: bug escaped review and tests
Name the missing case type, then add that type to the checklist. Typical gaps (Q12, Q38):
| Type | Example case that was missing |
|---|---|
| Boundaries | exactly at the limit, one below, one above; empty and one item; first and last page |
| Permissions | other user's id in the URL, expired session, role downgraded, direct API call |
| Empty and error states | no data, slow response, 500, offline, timeout, partial failure |
| Time zones and dates | midnight UTC vs local, daylight-saving change, month end, leap day |
| Money | rounding, currency decimals, refunds, discount stacking, negative totals, tax |
| Concurrency | double click, two tabs, retry of the same request |
Fix: write the failing test first, fix, keep the test; add the case type to `playbooks.md` 2 checklist.

## Tree E: payment or webhook untested
Check: is there a test-mode run of the full path (pay, redirect, webhook, access released)? Does a duplicate and a replayed event grant once? Does an invalid signature get rejected? Does a failed or declined payment leave the user in a recoverable state? What does the provider dashboard show vs the database? Fix with `playbooks.md` 5. If the CLI or keys are missing, report NOT VERIFIED; never use a real card or production.

## Tree F: accessibility regression
Run axe on the touched screens with WCAG tags (Q16), read `incomplete` as human review. Then keyboard pass: Tab order, visible focus not hidden by sticky bars, Escape closes dialogs, focus returns. New 2.2 checks: target size 24 px, focus not obscured, accessible authentication (Q18). Automated tools find a large share of frequent issues but not conformance (Q17, vendor data). Fix by role and label first; add an axe check to the component or page test so it stays caught.

## Tree G: visual regression
Different pixels, which cause? Same commit, same OS and browser, same fonts, same fake data and clock: if a rerun differs, the test is flaky (animation, fonts, dates). Different environment baseline: regenerate in the CI image, not locally (Q15). Real change: review diff, update the snapshot deliberately, never in bulk. Missing CSS or font gets caught by a screenshot at the project's widths, not by text assertions.

## Tree H: cannot reproduce a user bug
Collect: exact time, account (anonymised), device and browser, build version, steps, expected vs actual, screenshot or replay, logs and trace id. Compare environments: data (a specific record), locale and time zone, feature flag, permissions, cache, extensions, slow network. Reproduce in a fresh profile, then with the user's data shape. Add logging or a trace id if still missing; say "not reproduced, N attempts, with these conditions" rather than closing.

## Tree I: release blocked with unclear evidence
List the claims the release makes; for each, the evidence and its level. Mark PASSED (evidence, commit), FAILED, NOT VERIFIED (why). Unclear evidence is NOT VERIFIED, not PASSED. Ask what is the cheapest check that turns each NOT VERIFIED into a state; run those, in risk order. Release only on a decision by the owner who has read the NOT VERIFIED list.

## Worked numbers
- **Flake rate.** Each test fails by chance 2% of runs. A 50-test suite goes red by chance in 1 - 0.98^50 = 63.6% of runs. At 0.5% per test: 22.2%. At 0.1% per test over 200 tests: 18.1%. One flaky test is enough to teach the team to ignore red. A retry once cuts a 2% flake to 0.02^2 = 0.04% per test, but only for pure chance flakes; a real race that fails 2% of the time in production still fails there. The Google figures (about 1.5% of runs flaky, about 16% of tests with some flakiness) are one company's numbers (Q28).
- **Test count by pyramid.** A 400-test suite at a 70/20/10 first guess (Q28): 280 unit, 80 integration, 40 E2E. Time with 0.05 s, 1 s and 30 s each: 14 s + 80 s + 1,200 s = 1,294 s (21.6 min); the 40 E2E are 93% of the time. On 4 workers the E2E take 300 s. Inverting to 40 unit and 280 E2E would take 2 s + 80 s + 8,400 s, and would fail far more often by the flake math above.
- **Mutation score.** 50 mutants generated, 35 killed, 5 timed out (counted as detected), 6 survived, 4 equivalent (cannot change behaviour). Score = (35 + 5) / (50 - 4) = 87.0%. A 100% line-coverage suite can score far lower, because coverage only says the line ran, while a survivor says no test noticed the change (Q19, Q20, Q36). Read surviving mutants by hand: each is either a missing assertion or an equivalent mutant. Use it on small critical modules (money, permissions).
