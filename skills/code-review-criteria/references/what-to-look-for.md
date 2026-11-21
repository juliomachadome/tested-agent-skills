# What to look for, in risk order

## Quick pass (use first, then the detailed sections)

- **Correctness:** does inverting the main condition break a test? Edges: empty, one, limit, duplicate, null, unicode, timezone. State origin checked? Two calls in parallel? Failure between two writes? Errors swallowed?
- **Security in the diff:** guard on every new route; object checked against the caller/tenant; hostile input not reaching SQL, HTML, shell, paths, prompts unencoded; no secrets or personal data in logs or error bodies.
- **Data:** queries filtered by owner/tenant; transaction around multi-table writes; no external I/O inside a DB transaction; migrations forward-only and safe on existing data.
- **Performance:** queries in loops, lists without limit or stable pagination, large objects loaded when a header would do, external calls without timeout, retries without cap or on non-idempotent operations. Block only with a concrete consequence; do not claim milliseconds you did not measure.
- **Design:** inner layer importing outer layer; one use case doing several jobs; type-switching where an interface fits; abstraction for a single case; vocabulary outside the domain glossary.
- **Frontend:** logic or data fetching inside views; effects that mirror derivable state; hooks out of order; render impurity; UI strings hard-coded where the project uses a catalog; design values outside tokens.
- **Tests:** fail without the change? real assertions? doubles only at boundaries? dependent tests updated (grep)?
- **Size:** one idea? refactor separated?

Format: **rule** · why · bibliography number (see `BIBLIOGRAPHY.md`) · example.

## 1. Correctness

1. **Does the code do what the author intended, and is the intent good for users (including future developers)?** Think about edge cases and bugs visible only by reading. · [2]
2. **Concurrency and deadlocks rarely show up when running the code; reason about them.** Two requests in parallel, a retried job running twice, a timer firing during a write. · [2] · e.g. two approvals of the same order both succeed.
3. **State transitions are validated on the server from a known origin and are idempotent:** `UPDATE ... WHERE status = <origin>` and check the affected row count; never trust the state the client reports. · [2], [11] · e.g. a "publish" endpoint that does not check the item is still a draft re-publishes an archived item.
4. **Multi-table writes run in one transaction.** A failure between two writes leaves half a record (an invoice without lines). · [11]
5. **Never swallow errors.** Empty `catch {}`, `catch (e) { return null }`, a `.catch(() => {})` on a background promise: the failure disappears. Unknown errors must not become client messages either: a central error handler maps them to a generic 500 and logs the cause. Some frameworks' default handlers do not log expected HTTP errors; without your own filter they vanish. · [17], [9] · e.g. `throw new HttpError(500, e.message)` leaks a provider message (possibly containing a prompt or a SQL fragment) to the client.
6. **HTTP errors follow a stable format** (RFC 9457 problem details): `status` equals the response code; `detail` helps the client fix the request, not debug the server; no stack, table names or internal ids. · [9]
7. **Request data never lives in a shared instance.** DI frameworks and serverless runtimes often reuse one instance across concurrent requests (singleton scope by default; module scope shared under concurrency). A field holding the current user or tenant leaks between requests; use request context (e.g. `AsyncLocalStorage`) or pass values explicitly. Request-scoped providers propagate up the injection chain and cost an instantiation per request. · [17], [19]
8. **Session-level database settings leak.** `SET` persists after commit; `SET LOCAL` outside a transaction does nothing (only a warning). A tenant or role set at session level in a pooled connection reaches the next request. · [10]
9. **In-memory state assumes one instance.** A new in-process registry, cache, lock or scheduler changes behavior when a second replica starts; the diff should say so or move the state out. · [19]

## 2. Security in the diff (point it out; deep analysis goes to `software-security`)

1. **Deny by default, check every request, centrally.** A new route without the standard guard is blocking; an allowlist of unguarded routes that grows without a reason is a finding. · [8]
2. **IDOR: every object read or written by id is checked against its owner/tenant.** Access to one object of a type does not imply access to the others; hard-to-guess ids are not a defense. With row-level security, the explicit filter is still required (RLS is the second wall, and "empty result" in a test does not prove isolation). · [8]
3. **Trace source → sanitizer → sink** for each external input (body, params, upload, ingested document, model output) to where it acts: SQL, HTML, shell/argv, file path, prompt, log, URL fetch. The finding is the unsanitized path. · [8] (by sink); engineering practice
4. **Secrets and personal data in logs are blocking** because the damage is irreversible: watch for logging whole request objects, `JSON.stringify(req)`, or raw provider error messages. · [9] (no implementation detail exposed)

## 3. Data and migrations

1. **Repository queries filter by owner/tenant explicitly;** no external I/O (model call, HTTP fetch, object storage) inside a database transaction, which holds a pooled connection and can blow the transaction timeout; batch inserts instead of `for … await insert`. · [10], [11] (transactions); engineering practice
2. **Migrations are forward-only; never edit one that has been applied;** a new `NOT NULL` or `CHECK` on existing data needs proof on a copy with production-like shape; deploy order (code vs schema) must keep the running version working. · engineering practice
3. **Uniqueness and "exactly once" invariants live in the database** (unique constraint, conditional update), not in an application-level "check then insert". · [11]

## 4. Performance (read in review, measure elsewhere)

1. **Look for:** queries inside loops (N+1), `SELECT *` on wide tables, lists without a limit and without stable keyset pagination, large payloads loaded where a header is enough, whole files read into memory, CPU-heavy loops on the event loop. · engineering practice
2. **Every external call has a timeout, a propagated abort signal, a typed retryable error and a retry cap;** retrying a non-idempotent paid call is a bug. · engineering practice
3. **Block only with a concrete consequence** (list grows without bound, hot path, paid resource); otherwise follow-up. Do not claim latency numbers you did not measure. · [1]

## 5. Design and complexity

1. **The design of the whole is the most important part:** do the pieces interact sensibly, does this belong here or in a library, does it integrate with the rest, is now the time? · [2]
2. **Complex = a reader cannot understand it quickly, or a maintainer is likely to break it.** Watch for over-engineering: solve today's problem, not a hypothetical one. Ask for a split only when the diff makes it worse. · [2]
3. **Use refactoring names as precise vocabulary:** Extract Function, Decompose Conditional, Replace Nested Conditional with Guard Clauses, Replace Conditional with Polymorphism, Remove Flag Argument, Replace Primitive with Object, Introduce Parameter Object, Remove Dead Code, Replace Magic Literal, Separate Query from Modifier. · [18]
4. **Comments explain why;** if code needs a "what" comment, simplify the code (exceptions: regexes, non-obvious algorithms). Stale comments and TODOs the diff invalidated are nits. · [2]
5. **Documentation changes when how to build, test, use or release changes.** · [2]

## 6. Tests

1. **Ask: does the test fail when the code breaks? Would it false-positive if the code changed harmlessly? Is the assertion simple and useful?** Tests are maintained code; complexity in tests is not acceptable. · [2]
2. **A diff that adds or changes logic brings its tests in the same diff.** A pure refactor must already be covered (if not, tests come first). A diff that changes a status code, a port/interface or a fake without updating dependent tests (grep) is blocking. · [6]
3. **A bug fix comes with a test that fails without the fix.** · [2]
4. **Real tests only:** no `skip`/`only`, `expect(true)`, assertion-free tests, swallowed failures; doubles only at system boundaries, and fakes obey the same rules as the real thing (including tenant filters). Tests that read source files as text with regexes are fragile. · [2]
5. **Mental mutation:** invert the main condition in your head; if no test would break, coverage is missing. · [2]
