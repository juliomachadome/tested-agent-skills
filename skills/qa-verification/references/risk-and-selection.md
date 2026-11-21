# Risk, test selection and test design

Format: **rule** · why · source id (ids in `BIBLIOGRAPHY.md`) · example.

## 1. Risk first

1. **Risk = chance that a problem that matters to someone exists.** Work in two directions: from the diff outward ("what does this break, and in whom does it call?") and from a risk catalog inward ("does this apply here?"). · Q3
2. **Risk level = likelihood × impact, stated as high/medium/low with one sentence.** · Q4 (ISTQB risk level), Q3
3. **Risk catalog for most web products:** money (wrong charge, double charge, paid and not delivered) · access (sees what is not theirs, loses what is theirs) · personal data · loss of user progress or content · first use (signup, login, email) · irreversible actions (delete, send, publish) · production-only parts (keys, domain, webhooks, cron) · cost (paid API or GPU left running). · Q3
4. **Order of effort follows the list;** the last items get a smoke or nothing, and the report says so. · Q3

## 2. Selecting tests from a diff

1. **Three rings:** (1) tests of touched files; (2) tests of files that import them; (3) one neighboring critical path if the diff touched something shared (layout, auth, i18n, API client). · Q7, Q8
2. **Tools:** `vitest related <files> --run` (static imports only: dynamic imports and DI containers are invisible, so a "0 tests found" does not mean nothing covers it); `vitest --changed <ref>`; `turbo run test --filter=...[<ref>]` (the `...` prefix adds dependents; `--dry` shows the set without running); `turbo run test --affected` in CI needs full git history (`fetch-depth: 0`) or every package counts as changed. · Q7, Q8
3. **Playwright selection:** `--only-changed <ref>` runs changed **test files** only (does not follow code dependencies); `--grep @tag` and `--project` narrow; `--last-failed` repeats failures; `--list` collects without running. For "I changed component X", keep a small map from source paths to test tags. · Q9
4. **Do not rerun what already passed** if nothing it depends on changed (code, dependency, config, data, environment). Note "passed at commit X" and rerun only what changed after. After a fix, rerun what failed and the neighbors of the fix. · Q7
5. **Global changes** (build config, tsconfig, lockfile, root layout, middleware, message catalog, CI files) have no related test: typecheck all affected packages and smoke one screen per area; CI runs everything. · Q8

## 3. Test design techniques (ISTQB CTFL v4.0.1, chapter 4)

1. **Equivalence partitioning:** split inputs into classes the system treats the same way, valid and invalid; one test per class. · Q12 · e.g. quantity: <1 invalid, 1 to 10 valid, >10 invalid.
2. **Boundary value analysis:** test at the edges of ordered partitions. 2-value BVA covers each boundary and its closest neighbor; 3-value BVA adds the value on the other side. Most off-by-one bugs live here. · Q12 · e.g. limit 10: test 10 and 11 (2-value) or 9, 10, 11 (3-value).
3. **Decision tables:** list conditions and actions; each column is a rule combination; collapse impossible ones. Use when several flags interact. · Q12 · e.g. discount = member × coupon × first order.
4. **State transition testing:** model states and events; cover valid transitions, and try invalid ones (they must be rejected). Use for workflows: draft → submitted → approved → final. · Q12
5. **Branch coverage** shows code paths never executed; use it to find gaps, not as a goal. · Q12, Q20
6. **Experience-based:** error guessing (null, empty, duplicate, very long, unicode, timezone, concurrent), short time-boxed exploratory sessions with a charter, checklists from past defects. · Q12
7. **Acceptance criteria written with the requester** (collaborative user stories, ATDD) are the cheapest way to agree on "done" before code. · Q4

## 4. Suite shape

1. **Pyramid, trophy or any shape: what matters is fast, reliable tests that fail for a useful reason.** Disagreements are mostly vocabulary (solitary vs sociable unit tests). Avoid the "ice-cream cone" (many E2E, few low-level). Google's often-quoted 70/20/10 (unit/integration/E2E) was offered as "a good first guess", and the same post warns not to pay too much attention to the exact numbers: E2E simulates the user better but loses on speed, reliability and failure isolation. · Q28, Q5, Q6
2. **"The more your tests resemble the way your software is used, the more confidence they give."** Query by role and label, not by CSS class. · Q2
3. **E2E only for a few high-value paths** (purchase, access, login, the product's main task); screen logic belongs in view-model or component tests with a fake backend. · Q5
4. **Types and lint are the cheapest layer,** but a green typecheck proves no behavior.
5. **Size tests by what they may touch, not by name** (Google's test sizes): small = no network, database, filesystem, threads or sleeps, ~60 s limit; medium = localhost network, database, filesystem allowed, external systems discouraged, ~300 s; large = anything, 900 s+. Keep most tests small; give medium/large their own CI lane. · Q28

## 5. Contract tests

1. **A contract is what the consumer actually uses** (fields, types, error codes); test each side against it without running both together. · Q22, Q5
2. **One team and one repository: a shared schema/type used by both sides plus a test that validates the real API response against it** is enough; a broker such as Pact is overkill. · Q22
3. **The risk it covers is the stale mock:** E2E passes against a fake API while the real one changed. Signs: hand-written mocks with no shared type, fields nobody's tests know about. · Q5
4. **Third parties:** pin the API version, validate at the edge, keep recorded real payloads (webhooks, responses) as fixtures instead of invented ones. · Q22
5. **Contract changes are additive:** add the field, keep the old one until clients stop using it. · Q5

## 6. Property-based tests

1. **Declare a property that always holds and let the tool generate hundreds of inputs;** it shrinks a failure to a minimal counterexample and prints the seed. A complement to example tests, not a replacement. · Q21
2. **Where it pays:** money (parts sum to the total, a discount never makes a negative price), dates and time zones (round-trip), parsers and normalizers, ordering and pagination (no item duplicated or lost), state machines. · Q21
3. **Easy properties:** round-trip (`decode(encode(x)) == x`), invariants (size, sum, order), idempotence (`f(f(x)) == f(x)`), comparison with a slow obvious implementation, "never throws on valid input". · Q21
4. **When it finds a bug, copy the shrunk counterexample into a fixed example test.** · Q21
