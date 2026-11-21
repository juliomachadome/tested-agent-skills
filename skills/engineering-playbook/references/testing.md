# Testing

## 1. Purpose

Tests buy **confidence to change code**. A good test: catches regressions, doesn't break on refactoring (tests behavior, not implementation), runs fast, is deterministic, and is easy to read (Khorikov's four pillars: protection against regressions, resistance to refactoring, fast feedback, maintainability).

## 2. Test types & where to put effort

| Type | Scope | Speed | Use for |
|---|---|---|---|
| Unit | pure logic, domain, algorithms | ms | business rules, calculations (money!), edge cases |
| Integration | your code + real DB/HTTP/queue | s | repositories/queries, EF mappings, endpoints, middleware, serialization |
| Contract | API between independently deployed services | s | consumer/provider compatibility (Pact) |
| End-to-end | full system via UI/API | slow, flaky | a few critical journeys (signup, checkout, login) |
| Load/stress/soak | system under traffic | long | capacity, latency, memory leaks |
| Security | SAST, DAST, dependency scan | CI | OWASP issues |

- Pyramid (many unit, fewer integration, few e2e) for logic-heavy code; **testing trophy** (most integration) for typical web apps where bugs live at boundaries. Choose per codebase.
- Don't mock what you don't own deeply (EF Core, HttpClient internals). Test DB code against a **real database** (Testcontainers for SQL Server/Postgres; EF InMemory provider behaves differently — avoid it for query tests; SQLite in-memory differs too).
- ASP.NET Core: `WebApplicationFactory<Program>` for in-memory HTTP integration tests.

## 3. Writing good tests

- **Arrange-Act-Assert**; one behavior per test; name describes behavior (`Transfer_fails_when_balance_is_insufficient`).
- Test through public APIs; avoid testing private methods or asserting internal calls (over-mocking = brittle tests).
- **Test doubles:** stub (canned answers), mock (verify interactions — use for outgoing commands to external systems only), fake (working lightweight implementation, e.g. in-memory repository, `FakeTimeProvider`), spy.
- Control non-determinism: inject `TimeProvider` (`FakeTimeProvider`), random seeds, GUID generators; no `Thread.Sleep` — await conditions with timeouts.
- Test data builders / object mothers for readable setup (Bogus/AutoFixture for fillers, but explicit values for what matters to the assertion).
- Cover edge cases: empty, one, many, max size, null, negative, zero, duplicates, unicode, timezone/DST boundaries, rounding midpoints, concurrency, permission denied, other tenant's data.
- Assertions: specific and readable (FluentAssertions/Shouldly or built-ins; Vitest/Jest `expect`).
- Snapshot/approval tests (Verify) for large outputs — review diffs carefully.

## 4. Advanced techniques

- **Property-based testing** (FsCheck/CsCheck, fast-check): generate many inputs to check invariants (allocation always sums to total; serialize→deserialize roundtrip; sort output is ordered permutation).
- **Mutation testing** (Stryker.NET, StrykerJS): measures if tests detect injected bugs — better than line coverage.
- **Coverage** is a smell detector, not a goal (Goodhart). Uncovered critical code is a problem; 100% coverage doesn't mean correct.
- **Characterization tests** for legacy code before refactoring.
- **Architecture tests** (NetArchTest) to enforce layering.
- **Fuzzing** for parsers and input handlers.

## 5. Flaky tests

- Causes: shared state between tests, order dependence, time, async waits, external services, parallel DB use, random data.
- Fix: isolate data (unique ids per test, transactions rolled back, Respawn to reset DB), deterministic clocks, await properly, quarantine and fix quickly — never ignore.

## 6. Frontend testing

- Testing Library (React/React Native): test what the user sees and does (roles, labels), not component internals.
- Mock network at the boundary with **MSW**.
- E2E with **Playwright** for critical flows; accessibility checks with axe.
- Visual regression for design systems (Chromatic/Playwright screenshots).

## 7. CI

- Run unit + integration on every PR; e2e on main/nightly or for critical paths; fail on warnings for analyzers; parallelize; cache dependencies.
- Keep the suite fast (< 10 min) or developers stop running it.

## 8. Testing LLM features

- See ai-llm.md: eval sets with expected properties, LLM-as-judge with rubric, regression evals on prompt/model changes; don't assert exact text.
