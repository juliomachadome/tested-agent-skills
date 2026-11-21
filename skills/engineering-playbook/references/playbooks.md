# Playbooks: routines for everyday engineering changes

Checklists to run, not theory. Project conventions win: read the repo's own docs, lint rules and ADRs first and follow the pattern already in use. Evidence tags: **[C]** consensus or spec, **[F]** practitioner starting point. Rule details sit in the linked references; this file sequences them.

## 1. Implement a change test-first, smallest safe diff
1. Restate the item in one sentence and the observable behavior that proves it. If unclear, state your assumption.
2. Find the seam: the existing module, test file and helper that already do something similar. Reuse; do not add a second way.
3. No tests around the area? Write characterization tests that pin current behavior first (`testing.md`).
4. Red: write the failing test (a bug reproduces; a feature covers happy path, one edge, one error). Run it and read why it fails; a test that fails for the wrong reason proves nothing.
5. Green: the least code that passes, at the root cause, not a guard at the symptom. No hardcoded cases, no weakened assertions.
6. Refactor with tests green; delete dead code you created. Unrelated cleanup goes in a note, not in the diff.
7. Run the touched module's tests, the typecheck and the linter; read the output. Check the diff is reviewable (a few files, one idea).
8. Commit message states why. One item per commit, so any commit can be reverted alone.

## 2. Safe migration on a big table (Postgres)
Example target: add a required `region` column plus an index on a table of tens of millions of rows. Details and sources: `databases.md` sections 7, 12, 17.
1. **Plan the compatibility window.** The code running now must work with the old and the new schema. Order: expand (additive migration), deploy code that writes both, backfill, deploy code that reads the new column, enforce, contract later.
2. **Migration session settings.** `SET lock_timeout = '3s'; SET statement_timeout = '60s';` at the top, scoped to the session or transaction. If the lock is not granted, the migration fails fast and is retried; it must not queue behind a long transaction and block all traffic. Use a direct database connection, not the transaction-mode pooler.
3. **Expand.** `ALTER TABLE t ADD COLUMN region text;` (nullable, no default, metadata-only). A constant default is also metadata-only on current Postgres; a volatile default rewrites the table (verify on your major version).
4. **Dual write.** Deploy the application so every new and updated row sets the column.
5. **Backfill in batches, outside one transaction.** By primary-key range, 1k to 10k rows per batch, commit per batch, short pause, resumable (`WHERE region IS NULL`), progress logged. Arithmetic: 50M rows at 5,000 per batch is 10,000 batches; at 0.5 s per batch including the pause that is about 83 minutes, acceptable off-peak. Watch replication lag, dead tuples and CPU; pause when lag passes your limit **[F]**.
6. **Index.** `CREATE INDEX CONCURRENTLY ...` in its own migration, outside a transaction block. Afterwards check `indisvalid`; drop and retry on an `INVALID` index. Build before or after the backfill, but not in the same step.
7. **Enforce NOT NULL without a long lock.** `ALTER TABLE t ADD CONSTRAINT t_region_nn CHECK (region IS NOT NULL) NOT VALID;` then `VALIDATE CONSTRAINT` (scans without blocking writes), then `SET NOT NULL` (skips the scan because the valid check proves it), then drop the redundant check **[C]**.
8. **Switch reads, then contract** in a later release (drop old columns, remove dual write).
9. **Rollback story.** Each step is reversible by redeploying the previous code; the schema stays additive until the final contract step, which is a separate approved change.
10. Rehearse on a production-sized copy and record timings. The ORM's generated migration is a draft; review the SQL it emits.

## 3. Add an endpoint: checklist
- **Contract**: method and status codes correct (`201` plus `Location` for create, `204` for no body), resource-oriented path, documented in the schema or OpenAPI (`api-design.md`).
- **Validation**: schema at the boundary for body, query, params and headers; reject unknown fields where it matters; never trust price, role, owner or tenant from the client.
- **Authentication and authorization**: server-side, per resource and per tenant; a test for the denied case and for another tenant's id (`security.md`, `saas-multitenancy.md`).
- **Errors**: one mapping to `application/problem+json` (RFC 9457) with stable `type`, `status`, `detail` free of internals; validation errors list the field paths.
- **Pagination and limits**: lists have a cap and keyset or cursor paging; maximum body size; bounded filters (`databases.md` section 13).
- **Idempotency**: unsafe POSTs that create money or side effects accept an `Idempotency-Key`; PUT and DELETE idempotent by design (`distributed-systems.md` section 2).
- **Rate limit** per client or tenant on costly or abuse-prone routes, with `429` and `Retry-After`.
- **Performance**: query count per request known and bounded (no N+1), indexes for the filters used, explain plan checked on production-shaped data.
- **Observability**: structured log with request id and actor id, no personal data or secrets; a latency and error metric by route; span around outbound calls.
- **Tests**: happy path, validation failure, unauthorized, forbidden, not found, duplicate or conflict; one integration test through the real database.
- **Compatibility**: additive change to existing responses; a breaking change gets a new version or a deprecation path.

## 4. Add a queue or job
1. Decide if it must be a job: slow, retryable, or not needed for the response. Keep the request path short.
2. **Enqueue atomically** with the data change: transactional outbox (write the event row in the same transaction; a relay publishes) or the queue living in the same database (`distributed-systems.md` sections 14, 16). Publishing after commit without an outbox can lose events on a crash.
3. **Idempotent handler**: dedupe key (event or job id with a unique constraint written in the same transaction as the effect), or a naturally idempotent write (upsert, conditional status update). Assume at-least-once delivery.
4. **Retries**: bounded attempts, exponential backoff with jitter (for example 1 s, 2 s, 4 s, each plus random up to its size), retry only transient errors; permanent errors go straight to the dead letter.
5. **Dead-letter queue** with an alert on depth and an owner; a tool to inspect and replay.
6. **Timeouts and lease**: handler timeout shorter than the visibility lease; heartbeat for long work.
7. **Concurrency and ordering**: set a concurrency matched to the downstream limit; if order matters, partition by key; do not assume global order.
8. **Observability**: log job id, attempt, duration and outcome; metrics for queue depth, age of oldest job, failure rate.
9. **Tests**: handler run twice gives one effect; failing job lands in the dead letter after N attempts; crash between steps leaves a consistent state.

## 5. Incident hotfix routine
1. **Stop the bleeding first**: feature flag off, rollback to the previous release, rate limit, or disable the job. A rollback is a deploy of the last good commit, not an edit in production.
2. Capture evidence before it rotates: logs, request ids, the failing input, error-tracker links, timeline of deploys.
3. Reproduce with a failing test; fix at the root cause with the smallest diff; no refactor, no cleanup.
4. Review and run the checks proportional to the risk; for auth, money or data changes, get a second reviewer even under time pressure.
5. Deploy in the usual way and watch the same metric that showed the problem (error rate, queue depth) until it recovers; keep the flag path ready.
6. Repair the data: list affected records, correct with a reviewed, idempotent script, keep an audit trail; refund or notify as the law and policy require (`compliance-eu.md`).
7. Write the short post-incident note: timeline, cause, impact, why it was not caught, one or two follow-ups with owners (a test, an alert, a constraint). Blame-free; fix the system (`reliability-ops.md` section 6).

## 6. Dependency upgrade routine
1. Read the changelog and migration guide for every major jump; check the supported runtime versions and security advisories. A version newer than you know: read its bundled docs before touching routing, caching or build configuration.
2. One dependency (or one tightly coupled family) per change; lockfile committed; no mixing with feature work.
3. Run the tests, typecheck and lint; add a characterization test where the library behavior matters (serialization, dates, money rounding, validation).
4. Search the code for the deprecated or removed APIs named in the guide; use the vendor codemod if one exists and review its diff.
5. Check bundle size or image size and cold-start time when the library ships to the client or serverless.
6. Deploy to staging, watch errors; roll out gradually when possible; keep the previous lockfile as the rollback.
7. Record in the commit why the upgrade was needed (security fix, end of support, needed feature).

## 7. Code-level definition of done
- A test failed before the change and passes now; edge and error paths covered; no skipped or weakened tests.
- Denied-access test for anything that touches authorization; inputs validated at the boundary.
- No secret in code, logs or client bundles; no personal data in logs.
- External calls have timeouts; retries only on idempotent operations; webhooks and jobs idempotent.
- Migration additive and compatible with the running code; rollback is a redeploy of the previous commit.
- No N+1 or unbounded query introduced; query count and plan checked where data is large.
- Touched modules' tests, typecheck and lint ran, and the output was read.
- Changed screens checked for keyboard use, focus, contrast and text errors (`frontend.md` section 5).
- Observability added or kept: log, metric or span for the new path.
- Docs updated where behavior changed (README, OpenAPI, ADR for a decision with trade-offs).
- Risky areas (login, payments, entitlements, uploads, admin, personal data) flagged for security review before push.
- The summary says what was not verified.
