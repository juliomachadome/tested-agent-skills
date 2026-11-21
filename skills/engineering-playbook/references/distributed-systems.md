# Distributed Systems & Resilience

Assume: the network is unreliable, latency is not zero, bandwidth is finite, the topology changes, clocks drift, and any call can fail **after** having succeeded on the other side (Fallacies of Distributed Computing).

## 1. Consistency models

- **CAP:** during a network partition you choose Consistency or Availability. **PACELC:** else (no partition) you trade Latency vs Consistency.
- Models: strong/linearizable → sequential → causal → read-your-writes → monotonic reads → eventual.
- **Do:** decide per use case. Balances, payments, inventory reservations → strong (single DB transaction or consensus). Feeds, counters, search indexes, analytics → eventual is fine.
- After writing, if the UI reads from a replica/cache, guarantee **read-your-writes** (read from primary for that user briefly, or return the written data).

## 2. Idempotency (the most important property)

- **What:** performing an operation multiple times has the same effect as once.
- **Why:** retries, at-least-once delivery, double-clicks and timeouts guarantee duplicates.
- **Do:**
  - Client sends an `Idempotency-Key` (UUID) for unsafe operations (payments, orders). Server stores key + request hash + response; repeats return the stored response; same key with different payload → 422/409.
  - Store the key in the **same transaction** as the effect; unique constraint on it.
  - Message consumers keep a processed-message table (inbox) keyed by message id, or make the effect naturally idempotent (upsert, `SET status='paid' WHERE status='pending'`).
  - PUT/DELETE should be idempotent by design; POST is not unless you make it so.

## 3. Delivery semantics

- At-most-once (may lose), at-least-once (may duplicate — the practical default), exactly-once (only within a closed system; in practice = at-least-once + idempotent processing).

## 4. Transactional Outbox / Inbox

- **Problem (dual write):** saving to DB and publishing a message are two systems; one can fail → lost or phantom events.
- **Outbox:** in the same DB transaction, write the business change **and** an `OutboxMessages` row. A relay (background worker, CDC) publishes and marks sent. Consumers must be idempotent (relay can publish twice).
- **Inbox:** consumer records message ids processed in the same transaction as its effect.
- Libraries: MassTransit, NServiceBus, Wolverine, CAP (.NET) implement outbox/inbox.

## 5. Sagas (long-running business transactions)

- No distributed ACID across services → sequence of local transactions with **compensating actions** (refund, release reservation).
- **Choreography** (services react to events) — simple, but flow is implicit. **Orchestration** (a coordinator, e.g. Durable Functions, MassTransit state machine) — explicit, easier to monitor.
- Design compensations to be idempotent and to handle "already compensated".
- Avoid two-phase commit (2PC) across services: blocking and fragile.

## 6. Retries, timeouts, circuit breakers

- **Timeouts on every outbound call** (HTTP, DB, queue). Total budget per request; pass deadlines downstream.
- **Retry only transient failures** (timeouts, 408, 429, 502/503/504, connection reset, deadlocks) and only **idempotent** operations (or with idempotency keys).
- **Exponential backoff + jitter + max attempts:** e.g. 200 ms, 400 ms, 800 ms ± random; respect `Retry-After`.
- **Circuit breaker:** after N failures, fail fast for a cooldown, then probe — protects the dependency and your threads.
- **Bulkhead:** isolate resource pools per dependency so one slow dependency can't consume all threads/connections.
- **Fallback / graceful degradation:** cached/stale data, default values, feature off.
- **Hedging:** send a second request after p95 latency to cut tail latency (only for idempotent reads).
- .NET: `Microsoft.Extensions.Http.Resilience` (`AddStandardResilienceHandler()`, built on Polly v8): retry, circuit breaker, timeouts, rate limiter. EF Core: `EnableRetryOnFailure`.
- Avoid **retry amplification**: retries at every layer multiply load (3 layers × 3 retries = 27 calls). Retry at one layer.

## 7. Rate limiting & backpressure

- Algorithms: **token bucket** (bursts allowed), leaky bucket (smooth), fixed window (simple, edge bursts), sliding window (accurate), concurrency limiter.
- Limit per user/API key/tenant/IP; return **429** with `Retry-After`.
- ASP.NET Core: `builder.Services.AddRateLimiter(...)` + `app.UseRateLimiter()`; distributed limits need Redis or the API gateway (Azure API Management).
- **Backpressure:** bounded queues/channels; reject or slow producers instead of buffering unboundedly (OOM).
- **Load shedding:** under overload, drop low-priority work early with a fast 503 rather than timing out everything.

## 8. Messaging

| | Queue (point-to-point) | Topic / pub-sub | Stream/log |
|---|---|---|---|
| Examples | Service Bus queue, Storage Queue, SQS | Service Bus topics, SNS, Event Grid | Kafka, Event Hubs |
| Consumers | one per message | each subscription gets a copy | consumer groups with offsets, replay |
| Use | commands, jobs | events to many services | high-volume events, analytics, event sourcing |

- Handle: **poison messages** (dead-letter queue after N attempts, alert on DLQ), ordering (sessions/partition keys — ordering only per key), duplicates (idempotency), message size limits (claim-check pattern: store payload in blob, send reference), visibility timeout/lock renewal for long work.
- Message contracts are APIs: version them, add fields compatibly, never reuse meanings.
- Commands (do X, one handler) vs events (X happened, many subscribers, past tense).

## 9. Time & ordering

- Wall clocks drift and can jump; don't use timestamps from different machines to order events strictly.
- Use DB sequence/`rowversion`, Lamport clocks/vector clocks, or a single writer/partition for ordering.
- Leases/locks need expiry and **fencing tokens** (monotonic number checked by the resource) to avoid two holders after a pause.

## 10. Consensus & coordination

- Leader election and replicated state need consensus (Raft, Paxos) — use existing systems (etcd, ZooKeeper, Consul, cloud-managed locks, database) instead of writing your own.
- Quorum: R + W > N for read/write overlap in replicated stores.

## 11. Distributed caching & sessions

- Stateless app servers; session/state in Redis/DB/tokens.
- Cache invalidation via events or short TTL; beware cache/DB inconsistency on concurrent writes (delete cache after DB commit; consider versioned keys).

## 12. Service boundaries

- Start with a **modular monolith**; split into services only for independent scaling/deployment/team ownership needs. Microservices trade code complexity for operational complexity.
- Each service owns its data; no shared database writes across services.
- Synchronous call chains multiply failure probability and latency (availability of a chain = product of availabilities: 0.999⁵ ≈ 0.995). Prefer async events for non-critical paths.

## 13. Event sourcing & CQRS (when justified)

- Event sourcing: store events as the source of truth; rebuild state by replay. Great audit trail and temporal queries; costs: schema evolution of events, projections, eventual consistency, complexity. Use for ledger-like domains, not by default.
- CQRS: separate write model (commands, invariants) from read models (projections optimized for queries). Can be done in one DB without event sourcing.

## 14. A job queue inside Postgres (pg-boss, SKIP LOCKED)

- For small and medium volume, the queue can be a table in the primary database: claim with `SELECT ... FOR UPDATE SKIP LOCKED`, a unique key to avoid duplicates, a lease/expiry to recover orphaned jobs, final states `done`/`failed`. The docs: `SKIP LOCKED` skips rows that cannot be locked immediately; it gives an inconsistent view of the data, so it is not for general-purpose reads, but it suits multiple consumers of a queue-like table. Source: https://www.postgresql.org/docs/current/sql-select.html (read 2026-11-15).
- **Benefit:** a job can be created in the same transaction as the business change (no phantom job when the commit fails, no effect without a job). This is the outbox without a relay.
- **Know the library defaults** (pg-boss, from its docs, not re-verified): a job that exceeds its expiry returns to retry and **may run again while the first attempt is still executing**; default retry delay is 0 (immediate); queue policies (`short`, `singleton`, `stately`, `exclusive`, ordered-by-key) change duplicate and blocking behavior, and an ordered-by-key policy can leave a key blocked after a permanent failure. Choosing the wrong policy fails silently as a duplicate or a stuck queue. Sources: https://pgboss.io/api/jobs, https://pgboss.io/api/queues.
- `complete()`/`fail()` with the job object apply only to that attempt (zero affected if another worker took over): this protects against a stale worker finishing after expiry.
- **Dead-letter queue needs an owner:** a daily summary by job type and a simple manual reprocess. A DLQ nobody reads equals lost jobs.
- **Per-job deadline and per-cycle budget:** no job runs without a time limit; compute the ceiling (jobs per cycle x cycles per hour) and compare with the largest planned burst before it happens.
- Enqueue in batches (one `INSERT` with N rows), carry the tenant id in the payload explicitly, and open the tenant context inside the job.
- **Move to a managed queue** when the API process can no longer host the worker, volume exceeds the computed ceiling with margin, or you need per-message delay and retry the table cannot give. Before that it is one more moving part.
- Graceful shutdown: on `SIGTERM` stop fetching, finish or release the current job, exit; leases recover whatever was cut.

## 15. Idempotency in the handler

- **Idempotency key:** the client generates a random key (UUID v4 or equivalent entropy, no personal data) and sends `Idempotency-Key`. The server stores key + request fingerprint + response **in the same transaction as the effect**, with a unique constraint on the key. Same key, same payload: return the stored response. Same key, different payload: error. Same key while the first request is still running: conflict.
- The IETF HTTPAPI draft (`draft-ietf-httpapi-idempotency-key-header`, still an Internet-Draft, version 08 dated 2026-10-22 when read) specifies a String header value; 409 Conflict for a concurrent duplicate, 422 for a payload mismatch, 400 when a required key is missing. It is a draft: treat as convention. Source: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (read 2026-11-15).
- Do not consume the key when validation fails before execution starts; expire keys after a retention window (24 h is common; Stripe's documented practice, https://docs.stripe.com/api/idempotent_requests, not re-verified).
- **Message consumers:** at-least-once delivery means duplicates. Keep a processed-message table keyed by message id (inbox) written in the same transaction as the effect, or make the effect naturally idempotent: an upsert with a unique key, or `UPDATE ... SET status='paid' WHERE status='pending'` with an affected-row check.
- **Unique constraints are the real defense** under concurrency; application-level "check then insert" is a race.
- "Exactly once" in practice = at-least-once delivery + idempotent processing.

## 16. Transactional outbox: rules

- Write the state change and the outbox row in one transaction; a separate process reads and delivers; delivery may duplicate, so consumers are idempotent; never notify for a transaction that rolled back; preserve per-key order. Source: AWS Prescriptive Guidance, https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html (not re-verified).
- When the queue lives in the same database, inserting the job in the business transaction replaces the relay.

## 17. External calls: timeouts, retries, breaker, no I/O in a transaction

- **Every outbound call has a timeout chosen from the latency percentile you can tolerate, and a cap on attempts.** In Node use `AbortSignal.timeout(ms)` and combine with the caller's cancellation via `AbortSignal.any([...])` (Node 20.3+). A framework timeout middleware that only returns an error late does not cancel the underlying work: pass the signal to the call. Source: https://nodejs.org/api/globals.html (not re-verified).
- **Retry budget:** exponential backoff with a ceiling and **full or equal jitter** so retries do not synchronize into waves; a cap per request and per server; retry only transient, idempotent failures (timeout, 408, 429, 502/503/504, reset, deadlock); never permanent client errors; respect `Retry-After`; one retry layer only (3 layers x 3 tries = 27 calls, five layers of three = 243x load). Propagate one absolute deadline downstream instead of inventing a new timeout at each hop. Sources: AWS Builders' Library, "Timeouts, retries and backoff with jitter", https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/; Google SRE book, "Addressing Cascading Failures", https://sre.google/sre-book/addressing-cascading-failures/ (not re-verified).
- **Circuit breaker:** three states (closed, open, half-open), failure counter per window, one breaker per independent resource. Skip it for local resources, as a substitute for business error handling, or where failures already route to a dead-letter queue. For a low request rate, a short timeout plus graceful degradation is often enough and one less part to maintain. Add a breaker where a storm has been observed. Source: Microsoft Learn, "Circuit Breaker pattern", https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker (not re-verified).
- **Degradation must be simple, reversible, exercised on purpose and announce itself;** a fallback that never runs is the one that is broken.
- **Time budget per request:** sum the timeouts of a route's outbound calls; the sum must fit within the caller's patience (provider webhook deadline, function max duration, the user). A call without a timeout has no budget.
- **No external I/O inside a database transaction.** An HTTP, LLM, email or object-storage call inside `BEGIN ... COMMIT` stretches lock time, exhausts the pool and, on retry, repeats the effect. Pattern: reserve inside a short transaction, call outside, settle in a second short transaction (this is also how to enforce a spending cap without overshooting). Side effects that must follow a commit go through the outbox/job.
- **A failure inside a transaction after an external effect cannot be rolled back:** "database writes roll back; emails do not."
- In-memory locks need an expiry: an `if (running) return` guard with no per-job timeout stops the queue forever when one `await` never returns.

## 18. Server-Sent Events for progress

- SSE is one-way (server to client) over plain HTTP with automatic reconnect: the right tool for progress and token streaming; use WebSockets only when the client must push messages too.
- In NestJS, `@Sse()` returns `Observable<MessageEvent>`; client disconnect cancels the subscription (clean up in `finalize`). If the client leaves during asynchronous preparation, the observable is never subscribed and cleanup does not run: also watch an abort signal and make cleanup idempotent. A slow client with a huge pending buffer gets disconnected. Source: https://docs.nestjs.com/techniques/server-sent-events (not re-verified).
- **After the response headers are sent, the status cannot change:** errors become protocol events (`event: error` with fixed, non-leaking text); an exception filter can no longer rewrite the response.
- Send a periodic comment/heartbeat so proxies do not close idle streams; support resume with `Last-Event-ID` for long jobs; give long work a job id and a status endpoint as the fallback when the stream drops.
- Behind a reverse proxy, disable response buffering for the stream route.

## Sources

- PostgreSQL docs, SELECT (SKIP LOCKED): https://www.postgresql.org/docs/current/sql-select.html (read 2026-11-15)
- IETF draft, Idempotency-Key HTTP header: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (read 2026-11-15)
- pg-boss docs: https://pgboss.io/ (not re-verified)
- AWS Builders' Library; Google SRE book; Microsoft Learn Circuit Breaker; AWS Prescriptive Guidance outbox (URLs above, not re-verified)
- Stripe, Idempotent requests (design reference only, not re-verified)
- Nygard, *Release It!* 2nd ed. (timeouts, steady state; not re-verified)
