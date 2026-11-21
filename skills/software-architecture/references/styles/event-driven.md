# Style: event-driven

Components communicate through events (facts that happened) over a broker or log, instead of calling each other directly. Numbers [n] refer to `../BIBLIOGRAPHY.md`.

## When it fits
Work that must outlive a request (emails, exports, billing runs); fan-out of one fact to many independent consumers; bursts to smooth; integration of several systems; audit trail needs; real-time pipelines **[M]** [1][12][26].

## When it does not
Simple request/response with an immediate answer; strong consistency across the steps; a small team with no on-call for the broker; flows where debugging order matters and nobody can trace them. A database job table often does the job first (`../decision-checklists.md`).

## Core principles
Events are immutable facts named in the past tense ("OrderPaid"), carrying an id, a version, a timestamp and enough data to be useful; producers do not know consumers; consumers are idempotent; order is per key, not global; schemas evolve compatibly [1][12]. Distinguish event notification (small, consumer calls back), event-carried state transfer (full data), and commands (one addressee).

## Structure
Producers, broker or log (queue, topic, stream), consumers, dead-letter queue, schema registry or contract tests, an event catalog in the repo. Inside a modular monolith the bus can be in-process, then move out when a consumer needs it.

## Data ownership and consistency
Each service owns its data and publishes changes; consumers build their own copy. Eventual consistency is the price: define what the user sees meanwhile. Use the transactional outbox (write event and state in one transaction, relay to the broker) or change data capture, not dual writes. At-least-once plus idempotent consumers (dedup by event id stored in the same transaction as the effect) gives effectively-once. Sagas by choreography (events) or orchestration (a coordinator) for multi-step flows; prefer orchestration when more than 3-4 steps.

## Event sourcing: caution
Store events as the source of truth and derive state [17]. Worth it only when history, audit or temporal queries are the core product and the team accepts: schema evolution of old events, snapshots, replays, rebuild time, GDPR erasure (crypto-shredding or avoiding personal data in events), harder reporting and onboarding, and eventual-consistency read models (often with CQRS, see `cqrs.md`). Default alternative: current-state tables plus an append-only audit table or outbox. Apply it per bounded context, never system-wide **[M]**.

## Operations and failure modes
Lost events (no outbox), duplicates, reordering, poison messages blocking a partition, unbounded consumer lag, schema break, invisible flows (no correlation id), broker as single point of failure, retry storms on redelivery. Observe: consumer lag, dead-letter size and age, age of oldest message, end-to-end latency, duplicate rate, reconciliation counts.

## Migration in and out
In: introduce one outbox plus one consumer for a flow that is already asynchronous in practice; keep the sync path until proven. Out: replace a flow with a direct call or job table when traceability costs more than it gives; keep events as an integration contract if others consume them.

## Checklist
Do: name events as facts; version them; correlation id everywhere; idempotent consumers; dead-letter with owner; replay tool; reconcile periodically.
Avoid: events as remote procedure calls in disguise; one giant "everything changed" event; consumers writing back to the producer's tables; ordering assumptions; unbounded retention without a plan; event sourcing by default.

## Fitness functions
Contract tests per event schema (backward compatible); test that duplicate delivery and mid-handler crash leave state correct; alert on lag and dead-letter age; test that every published event comes from an outbox row; trace coverage of flows.

## Sources
Kleppmann [1][2]; Hohpe and Woolf [12]; Fowler, EventSourcing [17]; Azure event-driven style [26]; Sagas paper [30, identity via Crossref; full text not read]; SRE overload chapter for retries [29].
