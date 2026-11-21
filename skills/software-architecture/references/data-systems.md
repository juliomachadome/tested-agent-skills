# Data systems: replication, partitioning, transactions, streams

Checks to run when a design involves more than one node or more than one store. Use with decision-checklists.md.

## Replication
- Name the guarantee users need: read-your-writes, monotonic reads, consistent prefix. Cheap ways to give it: read from the leader right after a write, sticky routing, or a version token the client sends back.
- Single leader is the default. Multi-leader or leaderless buys write availability across regions at the price of conflict handling (last-write-wins silently loses data; merge types or app-level resolution are the alternatives). Quorum settings (W + R > N) reduce but do not eliminate stale reads.
- Failover can lose acknowledged writes and cause two leaders; require an epoch or fencing token so a stale leader or lock holder is rejected by the storage layer.

## Partitioning
- Hash keys spread load but lose range scans; range keys keep scans but create hot spots on sequential keys (timestamps). Compound keys (entity, time) are the usual compromise.
- A single hot key (celebrity user, one big tenant) needs explicit handling: salting, a dedicated partition, or caching in front.
- Use many more fixed partitions than nodes (or consistent hashing) so adding a node moves few rows; never `hash mod N` with a changing N.
- Cross-partition queries and secondary indexes are the cost centre: keep data that is changed together in one partition, and decide per secondary index whether it is local (scatter-gather reads) or global (slower, async writes).
- Move data with dual-write, backfill, verify, then cut over; keep the old path until the new one is proven.

## Transactions and isolation
- Know which anomaly your isolation level still allows (lost update, write skew, phantom). Read-modify-write on a counter or a "check then insert" rule needs a lock, an atomic statement, a unique constraint or serializable isolation; "read committed" alone does not protect it.
- Prefer a constraint in the database (unique, check, foreign key) over a check in application code.
- Atomicity across services does not exist for free: use a single-store transaction where possible, otherwise a saga with compensations, and say what the user sees while it is half done.
- Distributed locks need a lease plus a fencing token, never a lease alone.

## Streams and derived data
- Treat the log of changes as the source of truth when several views (search index, cache, analytics) must stay consistent; derive each view from it and be able to rebuild it from scratch.
- Capture changes from the database log (change data capture) instead of dual writes from the application; dual writes diverge on partial failure.
- Exactly-once is idempotent consumers plus transactional or deduplicated sinks, not a broker feature you switch on. Keep order per key, not globally.
- Windows must say which clock they use (event time or processing time) and how late data is handled.
- Keep schema evolution rules explicit: new readers accept old data and old readers tolerate new fields (add optional fields, never reuse a field id or meaning); use a schema registry or contract tests for shared topics.

## Failure review
For every store or queue, write down: what happens on timeout, network partition, replica lag, restart mid-write and duplicate delivery, and which invariant is checked afterwards. Test at least the duplicate-delivery and mid-write-crash cases.
