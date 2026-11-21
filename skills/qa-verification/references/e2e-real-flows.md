# Stable E2E and real flows in a deployed environment

Format: **rule** · why · source id (ids in `BIBLIOGRAPHY.md`) · example.

## 1. Stable Playwright tests

1. **Test what the user sees and does,** not internals (CSS classes, function names). · Q13
2. **Locator priority:** `getByRole` (with accessible name), `getByText`, `getByLabel`, `getByPlaceholder`, `getByAltText`, `getByTitle`, then `getByTestId`. If an element cannot be found by role, a screen reader cannot find it either: report it as an accessibility issue. · Q13, Q2
3. **Locators are strict; `.first()`, `.nth()` and "item N of the list" hide ambiguity** and may click something you did not intend after the page changes. Use `locator.filter({ hasText })` or a relative locator. · Q13
4. **Actions auto-wait for actionability** (visible, stable for two frames, receives events, enabled, not inert). `force: true` disables checks: use it only to prove something should not block. A click that "does not receive events" usually means a real overlay (sheet, toast): that is a finding. · Q13
5. **Web-first assertions, always awaited:** `await expect(locator).toBeVisible()/toHaveText()/toHaveURL()` retry until timeout (5 s default). `expect(await locator.isVisible()).toBe(true)` does not retry. For changing values use `expect.poll(fn)`; for a block, `expect(...).toPass()` (its default timeout is 0: set one). · Q13
6. **No `waitForTimeout` as a readiness signal.** Wait for the element, URL or response. Timeouts only on the step that needs them; `test.slow()` triples one test's timeout; the default test timeout is 30 s and includes fixtures and hooks. · Q13
7. **Isolation:** each test creates its own state and does not depend on order; a new browser context per test (default); login once in a setup project and reuse saved storage state. `describe.serial` is a declared exception: when one step fails the rest are skipped, and skipped steps are NOT VERIFIED. · Q14
8. **Control time and randomness:** fixed timezone and locale in config; `page.clock` (`setFixedTime`, `install` + `fastForward`) instead of the machine clock; unique ids per test. · Q14
9. **Lint `@typescript-eslint/no-floating-promises`** catches the forgotten `await` that makes an `expect` always pass; scripts outside the typecheck (loose `.mjs` files) are not protected. · Q13
10. **Web server:** `reuseExistingServer: false` for real runs (with `true` Playwright reuses whatever listens on the port, including an old build); readiness by `url`. Run against a production build, not the dev server. · Q14
11. **Mock only what you do not control** (third-party payment UI, maps, analytics, external email) with `page.route`; the integration with that third party has its own separate test. · Q13, Q14
12. **CI failure: open the trace, do not guess from a screenshot.** `trace: 'retain-on-failure'` or `'on-first-retry'`; `on` for every test is heavy. Traces include network headers and bodies: store them outside the repo and delete them when they contain cookies or tokens. · Q14

## 2. Proving a real flow in a deployed environment

1. **Touch the cloud with the cloud.** If a route mock answers in place of the API, the result counts as "screen", not "environment". Label every step REAL or SIMULATED in the report. · Q14
2. **To vary one aspect of a real response,** use `route.fetch()` then `route.fulfill()` with the modified body, or a recorded HAR edited by hand; useful to force a 5xx in one step without breaking the environment. Clean HAR files of tokens and cookies before committing. · Q14
3. **Protected preview deployments:** use the provider's automation bypass (e.g. Vercel's `x-vercel-protection-bypass` header, with `x-vercel-set-bypass-cookie` for browsers) set through context headers, never in the URL, never printed in a report. Do not turn protection off to test. · Q25
4. **Timings and intermediate states are the data.** Per step record start, first response, done, and the states seen from the API (queued, processing, done), with timestamps and request ids. Many real defects (a job stuck in "queued" while a worker sleeps) only appear with real time and real waiting. Poll the API status with `expect.poll` and an explicit ceiling per step; do not poll faster than the rate limit allows. · Q13
5. **Probe repetition, order and windows:** double click, back, reload mid-flow, out-of-order steps, session refresh, cold start of a sleeping service; pause/resume/cancel when the engine changed. `--repeat-each N` on one suspect test. · Q9
6. **Login by email link in a real environment** needs a test inbox the tester can read, and provider sending limits apply; without it the login step is NOT VERIFIED and the rest starts from a provided storage state. Never add a code bypass. · Q14
7. **Storage state contains cookies that impersonate you:** keep it in a git-ignored temp folder, one file per role, refresh it when the app rotates cookies, delete when expired. · Q14
8. **Downloads via the API:** check status, size, hash and extracted text (`pdftotext`) with an authenticated request; in the browser only check that the click triggers it (a native "Save" dialog on someone's screen is not a test).
9. **Evidence without secrets or real personal data.** Screenshots, traces, HARs and dumps can hold names, emails, tokens, signed URLs: store the path and hash in the report and delete what holds secrets. · Q14 (auth warning), Q25
10. **Undo what you created.** List the test records you created in the environment; confirm paid resources (GPU, workers) are back to zero cost and idle before saying "off".
