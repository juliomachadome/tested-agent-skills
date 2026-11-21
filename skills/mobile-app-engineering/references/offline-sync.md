# Offline-first and sync design

Offline is a product decision first: what must work without network, for how long, and who else can edit the same thing. Tags: **[C]** established, **[M]** serious but single, **[F]** practitioner.

## 1. Classify each entity
| Class | Example | Strategy |
|---|---|---|
| Cache only | feed, catalogue | read from local DB, refresh in background, show age |
| Queued writes, single owner | notes, diary, workout log | outbox, last-write-wins per field |
| Shared edit | team list, document | version vectors or a CRDT, or server-side merge with user-visible conflicts |
| Must be online | payment, availability booking | block with a clear message; never fake success |

## 2. Local database
expo-sqlite (or WatermelonDB, Realm, op-sqlite) as the source of truth for screens; screens read via live queries; network only moves data into and out of the DB. Version the schema with migrations that copy data, tested from the oldest supported version. Encrypt sensitive data at rest where required (SQLCipher or file protection) **[C]**. Keep a `sync_state` table with cursor, last success time and last error.

## 3. Outbox pattern
- Every mutation writes the local row and an `outbox` row in one transaction: id (client uuid), entity, operation, payload, base version, created at, attempts, status.
- A sync worker drains oldest first per entity, sends with an idempotency key (the outbox id), marks done on a 2xx, retries with exponential backoff and jitter on network errors, parks on 4xx validation errors with a visible failed state.
- Triggers: connectivity regained, app to foreground, after a local write, periodic background task (best effort, not guaranteed **[C]**).
- Server: unique constraint on the client id so retries are harmless; return the canonical row and new version.

## 4. Pull and merge
- Incremental pull by cursor (updated-at plus id, or a change sequence), including tombstones for deletes; page the results.
- Apply remote changes only to rows without pending outbox operations; for rows with pending changes, keep local value and reconcile after the push returns.
- Order: push first, then pull, otherwise the pull overwrites unsent edits (the most common data-loss bug).
- Clocks: do not trust device time for ordering; use server-assigned versions. A device clock can be wrong by hours.

## 5. Conflict rules
1. Different fields changed: merge both.
2. Same field changed: last write by server order wins, and the loser is stored in a conflict log or shown ("kept your version" or "kept theirs, undo?") for data users care about.
3. Delete versus edit: prefer keeping the edit and restoring the row, unless the delete was a legal erasure.
4. Counters and sets: use operations (increment, add, remove), not values.
5. Co-editing text or lists in real time: CRDT libraries (Automerge, Yjs) fit; cost is size and complexity; the Ink & Switch essay lists the ideals and trade-offs **[M]**.

## 6. Optimistic updates
Apply locally at once; show a subtle pending state; on server rejection roll back or mark failed with a retry action; never leave a silent divergence. Money and irreversible actions are not optimistic.

## 7. Failure tests (run before release)
- Airplane mode during a write, then reconnect.
- Kill the app mid-sync; relaunch; no duplicates or loss.
- Double tap submit; one server row.
- Two devices edit the same row offline; defined result.
- Server returns 500 for 10 minutes; outbox grows, no battery drain loop.
- Upgrade from the oldest app version with a full outbox.
- Clock set one day ahead.
- Logout with pending operations: block or warn.
- Storage full: error is shown, nothing half-written.

## 8. Worked number
1,000 devices each doing 20 writes a day with a 3 percent network failure rate yields 600 retries per day; without idempotency keys, about 600 duplicate rows a day, which is why the key is mandatory **[F]**.
