---
name: qa-verification
description: "ALWAYS use this skill, even for a short question, before saying a change is done and whenever someone asks to test it or decide if it ships, for example \"verify the fix works before I merge\", \"our e2e test for checkout is flaky on CI\", \"which tests should I run for this diff\", \"write test cases for this business rule\", \"CI is green but the bug is in production\", \"is the new onboarding flow ready to ship, I need a go/no-go with evidence\", \"run the tests\". Picks tests by risk and diff, writes stable Playwright E2E without sleeps, proves real flows in a deployed environment, checks accessibility, payments, webhooks, hunts false greens (zero tests ran, skipped, stale build, lying mocks). Reports PASSED, FAILED or NOT VERIFIED. Not for a plain unit test file for one utility, code quality review (code-review-criteria), authorization checks (software-security), slowness (web-performance), screen design (ux-design) or mobile store releases and app builds (mobile-app-engineering)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# QA and verification

"Done" is a claim someone will act on: merge, deploy, tell a customer. This skill makes it survive scrutiny. It chooses what to check by risk, runs the cheapest check that can catch each defect, distrusts green results, and reports in three states so that what was not verified never passes by omission.

Evidence tags used here and in the references: **[C]** consensus or standard (ISTQB, WCAG, vendor docs for their own tool), **[M]** serious single source or study, **[F]** practitioner or vendor claim, **[X]** myth. Source ids (Q1, Q2...) are entries in `references/BIBLIOGRAPHY.md`. 

## Step 1: project first

Before any command, read the current project's CLAUDE.md or AGENTS.md, `package.json` scripts, test and CI configuration, ADRs and glossary. Find out how this project verifies: which commands, what runs in CI versus locally, the critical path (purchase, access, first use, login), the screen widths and languages it must check. Project rules win over this skill. 

Boundaries:
- Writing tests and test doubles in code, TDD loop: `engineering-playbook` testing reference.
- The minimal "run the command before claiming success" gate: `superpowers:verification-before-completion`; this skill is the full method behind it.
- Security testing depth: `software-security`. Performance numbers: `web-performance`. UX judgment: `ux-design`. Mobile builds and stores: `mobile-app-engineering`. Code quality review: `code-review-criteria`.

## Principles

1. **Evidence at the level of the claim.** "Passed", "works", "done" come only from a command run in this session, output and exit code read, against the right commit and target. Unit green does not prove the screen works; mocked E2E does not prove production works. [C] Q1, Q2
2. **Testing is more than checking:** learning about the product, not only a repeatable check. Report both. [M] Q1
3. **Start from risk.** 5 to 10 lines: what can go wrong, for whom, cost. High, medium, low with one sentence of why; no invented scores. [C] Q4, Q3
4. **Push each check to the cheapest level that still catches the defect.** Rule in a pure function: unit. Route plus database plus permission: integration on a real database. Only what needs a browser (navigation, focus, cookies, layout, redirects): E2E. [C] Q5, Q6, Q28
5. **Test what changed, found by the diff:** touched files, importers, one critical neighbour; full suite once at the gate. Global files: smoke one screen per area. [F] Q7, Q8, Q9
6. **A flaky test is a defect with an owner and a deadline, not a pass.** Retries hide it. At 2% chance per test, a 50-test suite is red by chance 64% of runs. [C] Q10, Q28, Q34
7. **Never loosen a rule, delete a test, skip or raise a timeout to get green.** If the test is wrong, say so and propose the fix separately. [F] Q11
8. **A new test must be seen failing for the right reason** (change removed or fix reverted). A test born green proves nothing. [F] Q11
9. **Declare coverage:** verified, how, left out and why.
10. **Respect the machine:** one heavy process at a time, no watch mode, browser closed at the end.
11. **Coverage and metrics are flashlights, not targets.** Line coverage says a line ran; a mutation score says a change was noticed. Escaped defects and time to restore say more than test counts. [M] Q19, Q20, Q26, Q36
12. **Myth [X]:** "all green means safe". Green means the tests that ran passed; whether the right ones ran is Step 0.

## Method

1. **Read the request and the diff** (`git status`, `git diff --stat <base>...HEAD`). Without a diff or criteria, ask what must be verified.
2. **Step 0, is the evidence trustworthy?** What changed, risk class, which environment and build, which tests ran and their real counts. See `references/diagnosis-playbook.md`.
3. **List risks:** money, others' data, personal data, lost work, first use, irreversible actions, production-only things.
4. **Write acceptance criteria as repeatable observations:** state, action, expected result, including denied and error cases.
5. **Design cases with named techniques:** equivalence classes, boundaries, decision tables, state transitions, error guessing, a short exploratory charter. `references/playbooks.md` 2 and 6. [C] Q12
6. **Pick the minimal battery** and the exact command per criterion (`vitest related <files> --run`, `turbo run test --filter=...[origin/main]`, `playwright test -g "<title>" --project <name>`).
7. **Run one command at a time, cheapest first:** lint and types, related tests, focused E2E. Record command, counts (passed, failed, skipped, flaky), exit code, commit, target.
8. **Run the false-green table** (`references/false-green.md`) on anything new or critical.
9. **Look at what machines miss:** screenshots at the project widths, a keyboard pass on one critical flow, axe on new screens.
10. **For deployed flows** label each step REAL or SIMULATED, keep timings, no secrets or real personal data in evidence.
11. **Report in three states** and list what is unproven. You verify; you do not fix.

## Which reference to open

| Situation | Open |
|---|---|
| Tests green but the bug is in production, flaky E2E, slow suite, bug escaped review, cannot reproduce, release blocked with unclear evidence; worked numbers on flake rate, pyramid and mutation score | `references/diagnosis-playbook.md` |
| Routines: choose tests for a diff, cases from a business rule, stable Playwright, contract tests, payments and webhooks, exploratory charter, release gate checklist, bug report | `references/playbooks.md` |
| Risk lists, diff selection, ISTQB techniques in depth, suite shape, contract and property-based tests | `references/risk-and-selection.md` |
| Stable Playwright rules, auth state, real flows in a deployed environment, evidence hygiene | `references/e2e-real-flows.md` |
| How green lies, mutation testing, flaky tests, CI gotchas | `references/false-green.md` |
| Accessibility (automated and manual), screenshots, viewport checks | `references/a11y-visual.md` |
| Payment test paths, webhook duplicates, release gate detail, quality metrics | `references/payments-release.md` |
| Authors, years, ISBN or DOI, status | `references/BIBLIOGRAPHY.md` |

## Report format

First line: **READY**, **NOT READY** (what blocks) or **NOT VERIFIED** (what is missing to verify). Then:

| Criterion | How I verified | Evidence | State |
|---|---|---|---|
| Declined card shows an error and allows retry | e2e `checkout.spec` "declined", 1 passed, commit abc123 | command output | PASSED |
| Duplicate webhook grants access once | not run | payment CLI not available in this session | NOT VERIFIED |

Then: commit and target; what was left out and why; failures with file:line and steps, most severe first; residual risks. Banned without evidence: "should work", "probably passes", "tests pass" (which, how many, which commit?). Bug report template: `playbooks.md` 8.

## Core topics and where they live

Strategy and risk: principles 3, 4. Design techniques: `playbooks.md` 2. Levels and pyramid: `risk-and-selection.md` 4. E2E automation: `playbooks.md` 3. Flaky tests: diagnosis tree B. Regression selection: `playbooks.md` 1. Exploratory: `playbooks.md` 6. Accessibility: `a11y-visual.md`; security: `software-security`; performance: `web-performance`. Contract tests: `playbooks.md` 4. Defects and metrics: `playbooks.md` 8, `payments-release.md` 3. Release gate: `playbooks.md` 7. Mobile: `mobile-app-engineering`.

## AI tells to avoid (check while answering, not after)

- Generic test checklists not tied to the diff, the risk or the project's real commands: read them first and cite file:line.
- Boilerplate and over-engineering: a full battery or new test layers for a small change; run the smallest set that covers the risk.
- Invented commands, flags, versions or results: run it and quote the output, or say "not verified".
- "It depends" about what to test with no deciding risk: name the risk and pick.
- "Done", "works" or "passed" without a command run in this session; no output means NOT VERIFIED.
- Say what you chose and why in one line; a choice without a reason is removed.

## Gaps (still to research)

Playwright sharding, `waitForResponse` and `toPass` intervals; `networkidle` not reconfirmed; WCAG 2.2 normative text; vendor cold-start figures (measure instead); mutation tools beyond Stryker; the flaky-test paper and the mutation survey checked at landing-page level only.

