# Postgres performance

Version note: the docs below are the "current" manual (PostgreSQL 18 at the time of reading). Syntax is stable across recent majors; check the manual for yours.

## Find the slow query first

`pg_stat_statements` records planning and execution statistics per normalized statement (literals replaced by parameters). Enable: add it to `shared_preload_libraries` (restart required), keep `compute_query_id` on or auto, then `CREATE EXTENSION pg_stat_statements;` in each database. Key columns: `queryid`, `calls`, `total_exec_time`, `mean_exec_time`, `rows`, `shared_blks_read`. Sort by `total_exec_time` to find what costs the most overall, and by `mean_exec_time` for individually slow ones; a cheap query called a million times often beats a slow one called twice. `queryid` is stable within a major version, not across. Source: https://www.postgresql.org/docs/current/pgstatstatements.html (fetched 2026-11-15). Managed platforms often ship an advisor on top of this view.

## Reading EXPLAIN (ANALYZE, BUFFERS)

Source: https://www.postgresql.org/docs/current/using-explain.html (fetched 2026-11-15).
- `EXPLAIN ANALYZE` executes the statement and shows true row counts and times next to the estimates; BUFFERS (implied by ANALYZE in recent versions) shows buffer hits, reads, dirtied and written for each node and its children. Many reads on a node means disk I/O; many hits means cache.
- `cost` is planner units, not time. Judge by `actual time`.
- Estimated rows far from actual rows explains bad plans: run `ANALYZE` on the table and check statistics.
- Per-node times and row counts are averages per loop: multiply by `loops` for the total. A node inside a nested loop with `loops=10000` is the database-side N+1.
- `Rows Removed by Filter` high means the scan reads many rows it throws away; an index that eliminates them is the likely fix.
- Because the statement really runs, wrap writes: `BEGIN; EXPLAIN ANALYZE UPDATE ...; ROLLBACK;`.
- A tiny test table is misleading: the planner picks a sequential scan on one page whether or not an index exists. Test with volume similar to production.
- Compare plans before and after an index; if the plan did not change or got no faster, drop the index (indexes slow writes and cost space).

## Index types

Source: https://www.postgresql.org/docs/current/indexes-types.html (fetched 2026-11-15).

| Type | Use |
|---|---|
| B-tree (default) | equality and ranges on sortable data (`<, <=, =, >=, >`, BETWEEN, IN, IS NULL, anchored LIKE); also gives ORDER BY for free |
| Hash | equality only |
| GiST | framework for geometry, ranges, nearest-neighbor ordering |
| SP-GiST | non-balanced structures (quadtrees, k-d trees, tries) |
| GIN | inverted index for multi-valued data: arrays, jsonb, full-text |
| BRIN | tiny min/max summaries per block range; only for columns correlated with physical row order, such as append-only timestamps |

Shapes (from the indexing chapters, general knowledge, not re-fetched this round):
- Composite: put equality columns first, then the range or sort column; the index serves queries using a left prefix of its columns.
- Partial: `CREATE INDEX ... WHERE status = 'pending'` indexes only the subset you query; smaller and faster to maintain.
- Covering: `INCLUDE (col)` adds payload columns so an index-only scan avoids the table, provided the visibility map is current (vacuum).
- Index every column used by WHERE, JOIN and ORDER BY on hot paths, especially with LIMIT. Foreign keys are not indexed automatically.
- Vector similarity (approximate nearest neighbor) has its own index kinds provided by extensions; evaluate them with recall and latency together.

## N+1

One query per item of a list. Symptom: N near-identical statements with different parameters inside one request (visible in logs or as high `calls` in pg_stat_statements); in EXPLAIN, a node with a large `loops`. Fixes: a join, `WHERE id = ANY($1)` or `IN (...)` with a batch, or the ORM's eager loading option. Count queries per request in tests and fail above a ceiling.

## Pagination

- Every list query has a LIMIT. An unbounded result is a failure waiting for the data to grow.
- Keyset (seek) pagination for lists that grow: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT n`, with an index in the same order and a unique tiebreaker. `OFFSET` reads and discards skipped rows, so cost grows with depth, and rows repeat or vanish when data is inserted between pages. Trade-off: no jump to page N. Source: https://use-the-index-luke.com/no-offset (fetched 2026-11-15: OFFSET must still read and discard skipped rows, pages drift when rows are inserted, the seek method filters on the last key seen; drawback: no jump to arbitrary pages).
- Cap page size on the server; the client must not be able to raise it.

## Vacuum and autovacuum

Source: https://www.postgresql.org/docs/current/routine-vacuuming.html (fetched 2026-11-15).
- Vacuum is needed to reclaim space from dead row versions left by UPDATE and DELETE, update planner statistics (ANALYZE), update the visibility map (which enables index-only scans) and prevent transaction ID wraparound.
- Autovacuum runs these automatically. A table is vacuumed when dead tuples exceed `vacuum base threshold + scale factor x rows` (defaults: threshold 50 and scale factor 0.2, from the configuration chapter, not on this page). On a very large table 20 percent is a lot of bloat: lower the scale factor per table for hot, large tables.
- Symptoms of trouble: growing table or index size without growing data, slow scans of a table with many dead tuples, stale statistics causing bad plans, long-running transactions or idle-in-transaction sessions that stop vacuum from removing rows.
- Wraparound: the server warns when fewer than about 40 million transactions remain and stops accepting new transaction IDs below about 3 million. Never disable autovacuum.
- Update-heavy tables: keep rows narrow, avoid indexing frequently updated columns so cheaper in-page updates are possible (general knowledge).

## Connections and pooling

Serverless and edge functions open many short connections: use a pooler in transaction mode, a small pool per function instance, and no session-level state (`SET` leaks across requests; use `SET LOCAL` inside a transaction) and be careful with prepared statements in that mode. A persistent server can use direct connections or a session-mode pooler. Source: Supabase docs "Connecting to Postgres" (input, read 2026-11-12; not re-fetched; other vendors differ).

## Row-level security cost

Policies run for every row. Wrap function calls in a subquery so they evaluate once per statement, for example `(select auth.uid())` rather than `auth.uid()`, and index the column used by the policy. Source: Supabase RLS docs (not re-verified). Filter by the tenant column explicitly as well, so the planner can use an index even when RLS is active.

## Placement

Keep the database and the application in the same region. Each cross-region round trip lands in TTFB, and N+1 multiplies it.

## Extra database checks

- `Sort Method: external merge Disk` in a plan means a sort spilled to disk: raise `work_mem` for that role or query, not globally. Memory is per sort or hash node per query, so multiply by expected concurrency before changing it.
- `shared_buffers` (page cache, often a quarter to a third of RAM on a dedicated host) and `effective_cache_size` (a planner hint about OS cache, allocates nothing) are different knobs; managed services usually preset both.
- Tables with heavy updates or deletes can need their own autovacuum thresholds (per-table storage parameters) instead of a lower global value; watch dead-tuple ratio and long-running transactions that block cleanup.
- A `jsonb` column queried by containment (`@>`) or key existence needs a GIN index; queries on one extracted key are often better served by a B-tree expression index.
- A high `Loops` count on the inner side of a nested loop is the signature of a missing index on the join key (or a bad row estimate; run `ANALYZE` first).
- Connection pools in transaction mode forbid session state (session-level `SET`, advisory locks, plain prepared statements on older setups): use transaction-local settings.

## Sources

- https://www.postgresql.org/docs/current/using-explain.html, /indexes-types.html, /routine-vacuuming.html, /pgstatstatements.html (all fetched 2026-11-15)
- https://use-the-index-luke.com/no-offset (fetched 2026-11-15); Supabase docs (connecting-to-postgres, query-optimization, RLS) (input file, read 2026-11-12, not re-fetched)
