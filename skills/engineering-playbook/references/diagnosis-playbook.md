# Diagnosis playbook: production code problem, likely cause, check, fix

Use it top-down. Step 0 first: a fix without a reproduction or a timeline is a guess. Evidence tags: **[C]** consensus or spec, **[M]** measured in a well-known study or by you, **[F]** practitioner starting point (replace with your own numbers), **[X]** myth. Nothing here is copied from a source; ideas are applied. Rule details live in the linked references; this file only routes and shows the arithmetic.

## Step 0: what do we actually know?

| Check | How | If it fails |
|---|---|---|
| What changed, and when | deploys, config and feature-flag changes, migrations, dependency bumps, traffic or data-volume jump, cert or key expiry, cloud incident. Put them on one timeline against the first bad request | the first bad timestamp is the best clue; find it before reading code |
| Which signals exist | logs with request id, traces, metrics (rate, errors, latency percentiles), DB slow-query log, error tracker | no signal: add the minimum (one structured log line with request id and duration, one timing around each outbound call) and wait for the next occurrence; do not guess-fix |
| Scope | one endpoint, one tenant, one region, one version, one browser? Everyone since a time, or only some inputs? | the narrowest true statement drives the tree below |
| Reproduce | locally or in staging with production-shaped data (row counts, skew, a big tenant). Write the failing test or script first | cannot reproduce: capture the failing input from logs, or a read-only look at the production query plan; say "not reproduced" in the report |
| Environment parity | versions, config, locale and time zone, connection pooler, pool and timeout settings, instance count | differences are suspects; list them |
| Blast radius and time pressure | money, data loss, security? | if yes, stop the bleeding first (flag off, rollback, rate limit) using `playbooks.md` section 5, then diagnose |

Method: change one thing at a time, read the actual error, bisect the search space (commit, input, layer) **[C]**. Measure before concluding; a plausible story is not a cause **[M]**.

## Core arithmetic

- **N+1 cost**: queries = 1 + n. 500 orders, one customer lookup each, 3.8 ms per round trip (network plus execution): 501 x 3.8 = 1,904 ms, about 1.9 s. Batched (`WHERE id IN (...)` or a join): 2 queries, about 8 ms. The cost grows linearly with n, so it passes tests with 5 rows and fails with 500.
- **Little's law**: concurrent requests in the system L = arrival rate x time in system. 80 req/s x 0.2 s holding a connection = 16 connections needed. A pool of 10 serves at most 10 / 0.2 = 50 req/s; at 80 req/s the queue grows by 30 req/s and every request starts waiting for a connection (timeouts follow). The fix is a shorter hold time (no I/O inside the transaction, fewer queries), not a bigger pool: more connections than the database has cores to serve usually lowers throughput **[F]**.
- **Average hides the tail**: 95% of calls at 80 ms and 5% at 1,500 ms give a mean of 0.95 x 80 + 0.05 x 1500 = 151 ms, which looks fine, while 1 in 20 users waits 1.5 s. A page that makes 20 such calls hits at least one slow call 1 - 0.95^20 = 64% of the time. Alert on p95 and p99 per route, never the mean.
- **Retry duplicates**: 200 charges a day, 1% time out on the client side = 2 retries a day. If the provider had already processed the first attempt, each retry without an idempotency key is a double charge: 2 a day, 60 a month.
- **Memory growth**: container limit 512 MB, 150 MB after warm-up, growth 3 MB per minute: (512 - 150) / 3 = about 121 minutes to out-of-memory. That period (about 2 hours) is itself a clue: look for what happens per request or per job and is never released.
- **Join fan-out**: an order of 100 with 3 items and 2 payments, joined to both, yields 3 x 2 = 6 rows; `SUM(order.total)` returns 600.

## Trees

### 1. Endpoint is slow
First split the time: where do the milliseconds go (trace spans, or timers around DB, outbound HTTP, serialization)? Then:

| Symptom | Likely cause | How to check | Fix |
|---|---|---|---|
| Time grows with result size; many near-identical queries | N+1 (lazy relation inside a loop or a serializer) | count queries per request (ORM query log, `pg_stat_statements` calls); 1 + n pattern | eager load or join, `IN` batch, dataloader; add a test that asserts the query count; `databases.md` section 3 |
| One query dominates; plan shows a sequential scan on a big table | missing or unusable index (function on the column, type mismatch, leading wildcard, wrong column order) | `EXPLAIN (ANALYZE, BUFFERS)` on the real query with real parameters; compare rows removed by filter to rows returned | add the index with `CREATE INDEX CONCURRENTLY` (`databases.md` sections 1, 2, 12); re-run the plan |
| Fast on small tenants, slow on big ones; returns thousands of rows | unbounded query or offset pagination deep in the table | row count in the response, `OFFSET` value | cap page size, keyset pagination (`databases.md` section 13), select only needed columns |
| Latency equals a downstream call | synchronous external call on the request path | span for the outbound call; vendor status | timeout, cache, move to a job and return 202, or fall back (`distributed-systems.md` section 6) |
| Fast alone, slow under load; waiting not working | lock contention or pool queueing | `pg_stat_activity` wait events, `pg_locks`, pool wait metric; long transactions | shorten transactions, no I/O inside them, consistent lock order, `SKIP LOCKED` for queues (`databases.md` section 5, `concurrency.md`) |
| CPU high, event loop lag (Node) | heavy sync work (JSON, regex, crypto, loops) | profile, event-loop delay metric | stream, chunk, worker thread, or queue (`performance.md` section 6) |

Always report before and after with the same data (`performance.md` section 1). When a change is expected but not measured, say so.

### 2. Intermittent 500s
1. Group the errors by message, route, instance and time. All at the same minute points to a deploy, a cron job or a dependency; evenly spread points to inputs.
2. Timeouts to a dependency: compare the timeout setting with the dependency's p99; check for a missing timeout (threads pile up).
3. Pool exhaustion: errors like "timeout acquiring connection"; pool wait metric near the max; usually a leak (connection not released on an error path) or a long transaction holding a connection while calling an API. See Little's law above.
4. Race: fails only under concurrency; unique-violation or deadlock errors; read-then-write without a lock or constraint. Fix with a unique constraint, atomic update (`UPDATE ... WHERE status = 'pending'`), or optimistic concurrency (`databases.md` section 15).
5. Retries without idempotency turn a transient 500 into duplicates; see tree 3.
6. Cold start, memory kill or restart loop: check restarts and OOM events in the platform logs.

### 3. Duplicate records or payments
| Cause | Check | Fix |
|---|---|---|
| Missing idempotency key on the outbound charge or create call | provider dashboard shows two charges with different request ids; your logs show a retry | send a stable key derived from the business operation (order id plus attempt purpose) on every charge |
| At-least-once delivery (queue or webhook retry) with a handler that is not idempotent | same event id handled twice in logs; the provider retried after a slow or non-2xx response | store the event id with a unique constraint in the same transaction as the effect; answer 2xx fast, do slow work in a job (`distributed-systems.md` sections 2, 15; `api-design.md` section 11) |
| Visibility timeout shorter than the job | job duration p99 greater than the lease | extend the lease or heartbeat; make the handler idempotent anyway |
| Double submit from the client | two requests milliseconds apart with the same body | disable the button on submit, send a client idempotency key, unique constraint on the natural key |
| Dual write (DB plus broker) | event missing or duplicated after crashes | transactional outbox (`distributed-systems.md` section 16) |

Then repair the data: list the duplicates by key, refund or merge with an audit trail, and add the constraint that would have made it impossible.

### 4. Wrong totals
| Cause | Check | Fix |
|---|---|---|
| Float money | `0.1 + 0.2` is `0.30000000000000004`; sums drift by cents | integer minor units or decimal type; round once, at a defined step (`money-time-text.md` section 1) |
| Rounding order | per-line rounding versus total rounding; `1.005 * 100` is `100.49999999999999` in JS and rounds to 100, not 101 | define the rule (per line or per invoice, half-up or half-even), implement in one function, test with edge values |
| Time zone or date boundary | "today" report differs by the server and user zone; DST day has 23 or 25 hours | store UTC instants, convert at the edge, group by the business time zone (`money-time-text.md` section 2) |
| Join fan-out | totals multiply with the number of child rows | aggregate each child table in a subquery or CTE before joining; compare `COUNT(*)` before and after the join |
| Stale cache or reading a replica | totals correct after a few seconds | read from the primary for read-your-writes, or invalidate on write |
| Currency or tax-inclusive mix | mixed units in one sum | one currency per aggregate; label gross versus net |

### 5. Memory growth or leak
1. Confirm it is a leak and not a cache warming up: memory after load stops (plateau) versus a sawtooth that never returns to baseline. Compute the time to the limit (about 2 hours in the example above) and compare with the restart pattern.
2. Heap snapshots at two points (Node: `--heapsnapshot-signal` or DevTools; .NET: `dotnet-gcdump` or `dotnet-dump`); diff and read the retained-size leaders.
3. Usual suspects: unbounded in-memory cache or map keyed by user or request, event listeners added per request and never removed, timers and intervals, closures holding large request objects, unbounded queues, per-request `new` of a client or `HttpClient` (sockets), large response buffering instead of streaming.
4. Fix at the owner of the lifetime (bounded LRU with a size, remove the listener, reuse the client). Verify with the same load test and a flat line (`performance.md`, `concurrency.md`).

### 6. Flaky tests
Classify first: **order dependence** (shared state, run alone passes), **time** (real clock, sleeps, time zones, midnight), **concurrency** (unawaited promises, races), **environment** (ports, files, network, random data), **async UI** (assert before render). Reproduce by running the single test 50 to 200 times and in random order. Fix the cause: inject a clock, await everything, isolate state per test (transaction rollback or fresh schema), wait for conditions instead of sleeping, seed randomness. Quarantine only with an owner and an expiry date; deleting the assertion is not a fix (`testing.md` section 5).

### 7. A migration locked a table
Symptoms: every query on the table hangs; connection count climbs; the migration is "running" or waiting.
1. Look at `pg_stat_activity` and `pg_locks`: who is blocking whom. A queued `ALTER TABLE` (waiting behind a long transaction) blocks every later query, even plain reads, because it sits in the lock queue.
2. Stop the damage: cancel the migration session (`pg_cancel_backend`), or terminate the long blocker if safe. Check that no `INVALID` index was left by a failed concurrent build.
3. Prevent: `SET lock_timeout` low (about 3 s) and retry, `statement_timeout`, concurrent index build, constraints `NOT VALID` then `VALIDATE`, nullable column plus batched backfill. Full routine in `playbooks.md` section 2 and `databases.md` section 12.

### 8. Data visible to the wrong tenant
Treat as a security incident: contain first (disable the endpoint or feature, rotate if keys were exposed), then find. Check: does the query carry the tenant filter, taken from the session and not from the client body? Is there a cache key without the tenant (shared cache returning another tenant's response)? A background job or admin path running without a tenant context? A join that drops the filter? A pooled connection that kept a tenant setting from a previous request (`SET` instead of `SET LOCAL`)? Write the cross-tenant test that fails, fix at the single door (`saas-multitenancy.md` sections 2, 9; `databases.md` section 18), then assess who saw what from the logs for any breach notification duty (`compliance-eu.md`, `software-security`).

### 9. Background job stuck or repeated
| Symptom | Cause | Check and fix |
|---|---|---|
| Stuck in "active" | worker crashed or lost its lease; handler awaits something with no timeout | job age versus lease; add handler timeout, heartbeat, expiry that returns the job to the queue |
| Repeated forever | exception after a partial effect and unbounded retries; or ack before commit | cap attempts, backoff with jitter, dead-letter queue and alert on its depth; make the handler idempotent (`playbooks.md` section 4) |
| Runs twice | lease shorter than the job; two scheduler instances | one scheduler via a lock or the queue's own schedule; idempotency key per run |
| Piles up | consumers slower than producers | arrival rate versus service rate (Little); scale consumers or batch; do not just raise concurrency if the database is the limit |
| Poison message blocks the queue | one bad payload retried at the head | move to dead letter after N attempts; do not block others |

### 10. Frontend hydration mismatch or stale cache
Hydration mismatch: the server HTML differs from the first client render. Causes: `Date.now()`, `Math.random()`, `window` or `localStorage` read during render, locale or time zone formatting that differs between server and browser, invalid HTML nesting, browser extensions. Fix: compute such values in an effect after mount, pass the server value down, format with an explicit locale and zone, or mark intentionally dynamic parts. Stale data: check which layer caches (CDN, framework data cache, router cache, client query cache, browser) with response headers and the framework's cache docs for the installed major version; per-user data must never sit in a shared cache; invalidate by tag or key on write (`frontend.md` sections 2, 3).

### 11. LLM feature gives inconsistent output
Step 0 for this tree: is there an eval set with saved inputs and expected properties? Without one you cannot tell "worse" from "different". Then: log the exact prompt, model version, parameters and retrieved context for the bad cases; lower the temperature only after you know the cause; check if the model alias moved to a new version; check if retrieval returns different chunks; constrain with a schema and validate the output; add the bad cases to the eval set before changing the prompt. Prompts, RAG, evals and injection: `ai-llm.md` and the `llm-engineering` skill.

## Report format
State: the timeline (what changed), the evidence that supports the cause (a number, a plan, a log line), the fix, the test that now fails without it, and what was not verified (for example "not reproduced with production data volume").
