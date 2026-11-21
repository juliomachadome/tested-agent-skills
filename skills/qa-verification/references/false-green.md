# False green: how green lies and how to catch it

Format: **rule** · why · source id (ids in `BIBLIOGRAPHY.md`).

| How green lies | How to catch it | Source |
|---|---|---|
| **Zero tests ran** (filter matched nothing, wrong project) | Run `--list` first; read "N passed" and compare with the expected count; zero is a failure. Never use `--pass-with-no-tests` / `--passWithNoTests` in a gate | Q7, Q9 |
| **`test.only` left in** | `--forbid-only` / `forbidOnly: !!process.env.CI`; Vitest `allowOnly` false in CI | Q7, Q9 |
| **Flaky passed on retry** | `--fail-on-flaky-tests`; the report separates passed / flaky / failed; `--repeat-each` to hunt | Q9, Q10 |
| **Skipped by annotation** | `test.skip` and `test.fixme` do not run; `test.fail` runs and must fail. Count and list skips with reasons; a conditional skip per browser is legitimate, a skip to get green is not | Q10 |
| **Assertion that cannot fail** | No assertion; `expect` without `await`; value read once; assertion inside an `if`; `try/catch` that swallows; only `toBeDefined()` or `toHaveBeenCalled()` without arguments; snapshot of everything | Q13, Q11 |
| **`expect.soft` used for a precondition** | Soft fails at the end but lets the test continue on a broken state; use hard assertions for preconditions | Q13 |
| **Ran against the wrong thing** | Old build, reused server, wrong branch or environment: record commit, URL, port, build id with the result; `reuseExistingServer: false` | Q14 |
| **Mock stands in for the thing under test** | Label REAL/SIMULATED; validate real responses against the shared schema; recorded real payloads instead of invented ones | Q5, Q22 |
| **Exit code lost** | `cmd \| tail`, `\|\| true`, scripts that swallow errors: `set -o pipefail`, read `$?`, read the end of output, not the last nice line | general shell |
| **Skipped job reported as success** | A required check skipped by `paths` stays Pending and blocks merge; a job skipped by `if` reports Success. Use one aggregating gate job (`if: always()`) that fails on failure or cancel and accepts skips only by decision | Q24 |
| **Passes for the wrong reason** | Locator hits another element, asserts the loading state, a fixed wait got lucky: read the test, not just the result; a new test born green is suspect | Q13, Q11 |
| **Visual baseline updated without looking** | `--update-snapshots` only after reviewing the diff; baselines are per browser and OS | Q15 |
| **Wrong level of evidence** | Unit green used to claim "the screen works" or "production is fine": evidence must match the claim | Q1 |
| **Works locally, breaks in the environment** | Env vars, migrations, keys, domains: smoke in the environment after deploy | Q27 |
| **Offline or fake evaluation read as real** | Say "offline (fake)" or "real (model X, N cases)"; list excluded cases with exact numbers | general |
| **Nightly/scheduled run cited as proof** | Scheduled workflows run on the default branch only and can be delayed or dropped; check the run's head SHA before citing it | Q24 |

## Rules

1. **Break it on purpose.** For a new or critical test, revert the fix or invert the condition and watch it go red. It costs seconds and settles most doubts. · Q11
2. **Bug fixed = regression test kept.** Revert the fix: the test must fail again. · Q11
3. **Mutation testing** introduces small faults (flip a condition, change a boundary, remove a call) and checks that some test fails; surviving mutants show code executed but not verified. It is expensive: use it on small critical modules (money, permissions, parsers, rule engines), not the whole repo. · Q19
4. **Coverage is a flashlight, not a target.** It shows what was not exercised; as a goal it produces assertion-free tests. A floor only where business rules live. Signs of enough testing: bugs rarely escape and nobody fears changing the code. · Q20
5. **A flaky test teaches the team to ignore red.** At Google about 1.5% of all test runs reported a flaky result, almost 16% of tests had some flakiness, and about 84% of observed pass-to-fail transitions involved a flaky test. Fix it or remove it from the gate with an owner and a date; never enable retries in the gate without `--fail-on-flaky-tests`. · Q28, Q10
6. **CI hygiene:** cancel superseded runs of the same PR (`concurrency` with `cancel-in-progress`); never put secrets in caches (anyone with read access can open a PR and read the cache); do not cache test results that touch a database (a cache hit hides regressions). · Q24

## Extra checks: test-suite quality

7. **Report mutation results honestly.** State the tool, the scope, the denominator and the exclusions. Classify each mutant as killed by the expected assertion, survived, or errored or timed out (the last two are not kills). Mutants that behave identically to the original (equivalent) leave the denominator after a human check; a score alone never proves correctness.
8. **A failure must fail for the right reason.** When a mutant or a deliberate break turns a test red, read the message: a crash in setup is not a kill of the rule you meant to test.
9. **Trace tests to requirements.** Keep a short matrix from each acceptance criterion to its example test, boundary test and, for critical rules, a property or mutation check. A criterion with no row is a gap, and a test with no criterion is a candidate for deletion.
10. **Write rules testably.** Phrase each requirement as "when <trigger>, the system shall <response>" (or "while", "if ... then") so every clause becomes one assertion and the boundary values are visible.
11. **Metamorphic checks when there is no oracle.** If you cannot say what the right output is, assert a relation that must hold: the result is unchanged by re-ordering inputs, doubling the input scales the output, a filter never returns more rows than no filter.
12. **Controlled time in unit tests.** Use fake timers to test debounce, retries and expiry deterministically and restore real timers after each test; never sleep for real. Reset mocks and module state between tests so order does not matter.
13. **Fuzz where input is hostile or complex** (parsers, upload handlers, anything decoding untrusted bytes): assert that nothing crashes, hangs or leaks; keep each crashing input as a regression file.
