# Playbooks: routines for a verifier

Eight routines. Source ids (Q..) point to `BIBLIOGRAPHY.md`. Deeper rule lists: `risk-and-selection.md`, `e2e-real-flows.md`, `payments-release.md`, `false-green.md`, `a11y-visual.md`.

## 1. Choose tests by risk for a diff
1. `git diff --stat <base>...HEAD`; list touched files, their importers, one critical neighbour path.
2. Risk table (5 to 10 lines): what can break, for whom, cost, class high/medium/low with one sentence of why.
3. Map each risk to the cheapest level that catches it: pure rule = unit, route + database + permission = integration, browser-only (focus, cookies, redirects, layout) = E2E (Q5, Q6).
4. Commands, one at a time, cheapest first: lint and types of the package, `vitest related <files> --run`, `turbo run test --filter=...[origin/main]`, `playwright test -g "<title>" --project <name>` (Q7, Q8, Q9).
5. Global files (lockfile, build config, root layout, middleware, shared messages) have no related test: smoke one screen per area.
6. Record command, counts, exit code, commit, target. Full suite only at the release gate.

## 2. Test cases from a business rule (ISTQB techniques, Q12)
Steps: restate the rule as conditions and outcomes; find ambiguities and ask; apply the techniques; write each case as initial state, action, expected result; keep one case per class or boundary.
- **Equivalence classes:** split every input into valid and invalid classes; one case per class.
- **Boundary values:** for each ordered class, 2-value (edge and neighbour) or 3-value (below, at, above) cases.
- **Decision table:** all condition combinations as columns; mark impossible ones; one case per column.
- **State transitions:** states, events, allowed and forbidden moves; test each allowed move and try forbidden ones.
- **Error guessing and checklist:** empty, null, duplicate, very long, unicode, time zone, concurrent, double click, retry, other user's id.
Checklist of case types so none is missed: boundaries, permissions, empty and error states, time zones, money, concurrency.
Worked mini-example: "orders of 100 or more get 10% off, once per customer". Classes: <100, >=100, first or repeat customer. Boundaries: 99.99, 100.00, 100.01. Table: (under, first), (under, repeat), (over, first), (over, repeat). Money: rounding of 10% on 100.05. Ask: is the threshold before or after tax?

## 3. Stable Playwright E2E (Q13, Q14)
- Locators by role, label, then test id; no CSS chains or positions: `page.getByRole('button', { name: 'Pay' })`.
- Web-first assertions that retry: `await expect(page.getByRole('status')).toHaveText('Paid')`. No `waitForTimeout`, no `sleep`, no `networkidle` as the only signal.
- Wait for the specific thing: a response (`waitForResponse`), a URL, an element state.
- Isolation: each test creates its own data and user (through API or fixture), no order dependence, no shared account across workers; saved auth state instead of UI login each time.
- Control what you do not own: mock third parties at the network edge; fixed clock for date logic.
- Traces: `trace: 'on-first-retry'` in CI; open the trace of a failure before editing the test; screenshots and video only on failure.
- CI: `forbidOnly`, `reuseExistingServer: false`, retries 1 at most with flaky reported, workers set deliberately.
- A new test must be seen failing without the change (Q11).

## 4. Contract tests for APIs (Q22)
1. List what each consumer actually reads: fields, types, status codes, error shape.
2. One repo or one team: a shared schema or type, plus a test that validates the real response against it. Several teams: consumer-driven contracts (Pact) with a broker.
3. Provider side: run the contract against the real handler with a test database.
4. Third parties: pin API version, keep recorded real payloads as fixtures.
5. Changes are additive: add a field, keep the old until clients stop using it.
6. Failure shows which consumer breaks and which field.

## 5. Payments and webhooks (Q23, Q42)
Test mode only, test keys, test cards from the provider's docs; never a real card or production purchase.
- Paths: success, declined, insufficient funds, authentication required, cancelled at checkout, expired session.
- Webhook signature: valid signature accepted, tampered body or wrong secret rejected; use the raw body.
- Idempotency: the same event delivered twice, or out of order, grants access once; check by event id; the proof is exactly one row or one entitlement.
- Replay: resend an event from the CLI or dashboard; delayed delivery; handler failure then retry.
- Refunds, disputes, currency decimals, tax display.
- Check provider dashboard against database at the end. If keys or CLI are missing: NOT VERIFIED.

## 6. Exploratory session charter (Q32, Q12)
Template: **Explore** [area or feature] **with** [data, tool, persona, constraint] **to discover** [risk or question]. Timebox 45 to 90 minutes. Notes: what was tried, bugs (with steps), questions, areas not covered. Debrief in 5 minutes: what was learned, what to automate. Example: Explore the coupon box with expired, stacked and pasted codes to discover wrong totals. Testing is learning, not only checking (Q1).

## 7. Release gate checklist
| Item | State | Evidence |
|---|---|---|
| Right commit and build deployed to the target, SHA shown | PASSED / FAILED / NOT VERIFIED | |
| Lint, types, unit, integration green, counts and no skips | | |
| Focused E2E for critical path in the target environment | | |
| Payment path in test mode, access granted once | | |
| Webhooks signed, duplicates harmless | | |
| Accessibility: axe on new screens, keyboard pass on one flow | | |
| Screens at the project widths | | |
| Migrations, env vars, keys, cron exist in the target | | |
| Rollback path known | | |
| Known flaky tests listed, none hidden by retry | | |
Verdict: READY, NOT READY (blocking items), NOT VERIFIED (missing items). Anything not run is NOT VERIFIED, never blank.

## 8. Bug report template and mobile
Title (observable: "Checkout button stays disabled after a declined card"), environment and commit or build, steps, expected, actual, evidence path (screenshot, trace, log excerpt without secrets or personal data), severity by user impact, frequency (3 of 3, or 2 of 10), workaround, suspected area if known. Do not guess the cause.
**Mobile apps:** device matrix, store builds, permissions, push, offline and release testing sit in `mobile-app-engineering`; this skill supplies the risk list, cases, evidence and the three states.
