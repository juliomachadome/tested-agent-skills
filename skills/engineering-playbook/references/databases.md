# Databases (SQL Server / Azure SQL / PostgreSQL / EF Core)

## 1. Indexes

- **What:** a B-tree (usually) ordered by key columns → seek in O(log n) instead of full scan O(n).
- **Why:** the single highest-impact performance fix in most backends.
- **Do:**
  - Index columns used in `WHERE`, `JOIN`, `ORDER BY` of frequent queries. Foreign keys usually need an index (Postgres and SQL Server do **not** create them automatically).
  - **Composite index order:** equality columns first, then range/sort column. `(TenantId, Status, CreatedAt)` serves `WHERE TenantId=@t AND Status=@s ORDER BY CreatedAt`.
  - **Leftmost prefix rule:** index `(A,B,C)` helps `A`, `A,B`, `A,B,C` — not `B` alone.
  - **Covering index:** include selected columns (`INCLUDE` in SQL Server/Postgres 11+) to avoid key lookups.
  - **Filtered/partial index:** `WHERE IsDeleted = 0` / `WHERE status = 'active'` for skewed data.
  - Unique indexes enforce invariants (and are the real defense against duplicates under concurrency).
- **Avoid (non-sargable predicates that prevent index use):** functions on the column (`WHERE YEAR(CreatedAt)=2026` → use a range), leading wildcard `LIKE '%x'`, implicit type conversions (nvarchar vs varchar parameter), `OR` across different columns (consider `UNION`), arithmetic on the column.
- **Cost:** each index slows writes and uses storage. Remove unused indexes (`sys.dm_db_index_usage_stats`, `pg_stat_user_indexes`).

## 2. Read the query plan

- SQL Server: actual execution plan, `SET STATISTICS IO, TIME ON`, Query Store. Postgres: `EXPLAIN (ANALYZE, BUFFERS)`.
- Look for: scans on large tables, key lookups in loops, sorts/spills to tempdb, huge estimated vs actual row mismatches (stale statistics, parameter sniffing), implicit conversions.
- **Parameter sniffing** (SQL Server): plan compiled for a skewed parameter performs badly for others → `OPTION (RECOMPILE)` on specific queries, `OPTIMIZE FOR`, or rewrite; don't apply globally.

## 3. N+1 and loading strategy (EF Core)

```csharp
// N+1: one query for orders + one per order for customer (lazy loading) 
foreach (var o in db.Orders) Console.WriteLine(o.Customer.Name);

// One query, only needed columns
var rows = await db.Orders
    .Where(o => o.TenantId == tenantId && o.CreatedAt >= from)
    .Select(o => new OrderRow(o.Id, o.Total, o.Customer.Name))
    .ToListAsync(ct);
```

- **Projection with `Select`** beats `Include` when you need a few columns (no tracking, less data).
- `AsNoTracking()` for read-only queries (or `QueryTrackingBehavior.NoTracking` by default for read side in CQRS).
- `Include` of multiple collections → cartesian explosion → `AsSplitQuery()` (be aware: separate queries, consistency only within a transaction).
- Avoid lazy loading proxies in web apps (hidden N+1).
- Filter and paginate **before** `ToListAsync()`; never `ToList()` then `Where` on large sets.
- Bulk changes: `ExecuteUpdateAsync`/`ExecuteDeleteAsync` (EF Core 7+) instead of load-modify-save loops. Bulk inserts: `AddRange` + single `SaveChanges` (batched), or `SqlBulkCopy`/`COPY` for very large volumes.
- Hot queries: compiled queries (`EF.CompileAsyncQuery`), DbContext pooling (`AddDbContextPool`).
- Log generated SQL in development (`LogTo`, `EnableSensitiveDataLogging` only locally) and check it.
- `DbContext` is **not thread-safe** and is scoped per request; never share across parallel tasks.
- Raw SQL: `FromSql($"... {param}")` / `SqlQuery` are parameterized via interpolation; `FromSqlRaw` with string concatenation is an injection risk.

## 4. Pagination

| Method | How | Pros | Cons |
|---|---|---|---|
| Offset | `OFFSET 10000 FETCH 20` / `Skip/Take` | simple, jump to page | O(offset) cost, duplicates/skips when data changes |
| **Keyset (seek/cursor)** | `WHERE (CreatedAt, Id) < (@lastCreatedAt, @lastId) ORDER BY CreatedAt DESC, Id DESC` | constant cost, stable | no random page jumps |

- Always use a **deterministic order** (add a unique tiebreaker like `Id`).
- Cap page size server-side. Return an opaque cursor for keyset.

## 5. Transactions, isolation & concurrency

- **ACID:** atomicity, consistency, isolation, durability.
- Isolation levels & anomalies:

| Level | Dirty read | Non-repeatable read | Phantom | Notes |
|---|---|---|---|---|
| Read Uncommitted | yes | yes | yes | avoid (`NOLOCK` = this; can read rows twice or miss them) |
| Read Committed | no | yes | yes | default in SQL Server and Postgres |
| Repeatable Read | no | no | yes (SQL Server) / no (Postgres snapshot) | |
| Snapshot / RCSI | no | no | no | MVCC row versions; write-skew possible |
| Serializable | no | no | no | safest, more blocking/aborts; retry on serialization failure |

- Azure SQL Database has **Read Committed Snapshot (RCSI)** on by default: readers don't block writers.
- **Write skew / lost update:** two transactions read the same data then both write based on it (double booking, overdraft). Fixes:
  - **Optimistic concurrency:** row version column (`rowversion` in SQL Server, `xmin` in Postgres) → EF Core `[Timestamp]`/`IsRowVersion()`; handle `DbUpdateConcurrencyException`.
  - **Atomic conditional update:** `UPDATE Accounts SET Balance = Balance - @x WHERE Id=@id AND Balance >= @x` and check affected rows.
  - **Pessimistic lock:** `SELECT ... FOR UPDATE` (Postgres) / `WITH (UPDLOCK, ROWLOCK)` (SQL Server) inside a short transaction.
  - **Unique constraints** for "only one" rules.
- Keep transactions **short**; never hold one open across HTTP calls or user think time.
- Deadlocks: access tables in a consistent order, keep transactions short, index to reduce lock scope, and **retry** deadlock victims (EF Core `EnableRetryOnFailure` for transient errors in Azure SQL).

## 6. Schema design

- Normalize to 3NF by default (each fact once); denormalize deliberately for read performance with a plan to keep copies in sync.
- Correct types: `decimal(19,4)` or similar for money (never `float`), `datetimeoffset`/`timestamptz` for instants, `date` for calendar dates, appropriate string lengths, `uniqueidentifier`/`uuid`.
- **GUID primary keys:** random GUIDs fragment clustered indexes → use sequential GUIDs (`NEWSEQUENTIALID`, UUIDv7 — `Guid.CreateVersion7()` in .NET 9) or bigint identity + separate public id.
- Constraints in the DB (NOT NULL, FK, UNIQUE, CHECK) — the database is the last line of defense for invariants.
- Soft delete: global query filter + filtered unique indexes; consider legal retention/erasure requirements.
- Audit columns (`CreatedAt/By`, `UpdatedAt/By`); temporal tables (SQL Server) for history.
- Large blobs in object storage (Blob Storage/S3), not in the DB.

## 7. Migrations (zero-downtime)

- **Expand → migrate → contract:** add new column/table (nullable or with default) → deploy code writing both → backfill in batches → switch reads → remove old column in a later release.
- Never rename/drop a column used by the currently deployed version.
- Large table changes: batch updates (e.g. 5k rows per batch), online index operations (`ONLINE = ON`, `CREATE INDEX CONCURRENTLY`).
- Review generated EF migrations; generate idempotent SQL scripts for production.

## 8. Connections

- Use pooling (default in ADO.NET/Npgsql); open late, close early (`await using`).
- Pool exhaustion symptoms: timeouts acquiring connections → find leaks, long transactions, sync-over-async, too much parallelism.
- Serverless/Functions with many instances can exhaust DB connections → cap instances, use pooling proxies (PgBouncer), or a queue.

## 9. Scaling

- Order: indexes & queries → caching → read replicas (eventual consistency for reads) → vertical scale → partitioning (by date/tenant) → sharding (last resort; cross-shard queries and transactions get hard).
- **OLTP vs OLAP:** don't run heavy reports on the transactional DB at peak; use replicas, columnstore indexes, or a warehouse/lakehouse fed by CDC/ETL.
- Queue writes that don't need synchronous confirmation.

## 10. NoSQL choice

| Type | Examples | Good for | Watch |
|---|---|---|---|
| Key-value | Redis | cache, sessions, rate limits, locks | memory-bound, persistence settings |
| Document | Cosmos DB, MongoDB | aggregate-shaped data, flexible schema | design partition key for access pattern; cross-partition queries cost RU |
| Wide-column | Cassandra | huge write throughput, time series | query-driven modeling |
| Search | OpenSearch/Elasticsearch, Azure AI Search | full-text, facets | eventually consistent, not source of truth |
| Graph | Neo4j | relationship traversal | |

Default to a relational DB unless the access pattern clearly fits something else.

## 11. Full-text & fuzzy search

- `LIKE '%term%'` scans → use full-text indexes (SQL Server FTS, Postgres `tsvector` + GIN), trigram indexes (`pg_trgm`) for fuzzy, or a search engine for relevance ranking (BM25), facets and typo tolerance.
- Vector search (pgvector, Azure AI Search) for semantic similarity — see ai-llm.md.

## 12. PostgreSQL: safe migrations on a live table

Extends section 7. Goal: keep every lock short and make every long scan interruptible.

- **Additive first (expand/contract):** add the new thing, deploy code that tolerates both shapes, backfill, switch reads, drop the old thing in a later release. Make each migration re-runnable (`IF NOT EXISTS`) and forward-only; keep the applied version recorded in the database so every environment can say what it has.
- **Set timeouts at the top of every migration**, scoped to the transaction or session, never globally:

```sql
SET lock_timeout = '3s';        -- give up if the lock is not granted quickly
SET statement_timeout = '60s';  -- bound the work itself
```

  `lock_timeout` aborts a statement that waits too long for a lock (per lock attempt); it is the guard against a queued `ALTER TABLE` blocking every query behind it. If `statement_timeout` is non-zero and not larger than `lock_timeout`, the statement timeout fires first. The docs advise against putting either in `postgresql.conf` because it would affect all sessions. Retry the migration when it loses the lock race. Source: https://www.postgresql.org/docs/current/runtime-config-client.html (read 2026-11-15).
- **`CREATE INDEX CONCURRENTLY` on any table that takes writes.** A plain build blocks inserts, updates and deletes until it finishes; the concurrent build does two scans and waits for old transactions, so it takes longer but does not block writes. It cannot run inside a transaction block, and a failure (deadlock, uniqueness violation) leaves an `INVALID` index that is ignored by queries but still costs on every write: find it with `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`, then `DROP INDEX` and retry, or `REINDEX INDEX CONCURRENTLY`. Source: https://www.postgresql.org/docs/current/sql-createindex.html (read 2026-11-15).
- **`ADD COLUMN` with a non-volatile `DEFAULT` is metadata only;** a volatile default, a stored generated column or an identity column rewrites the table under an exclusive lock (read 2026-11-14 from the ALTER TABLE page via the input file; not re-verified).
- **New constraints on a big table in two steps:** `ADD CONSTRAINT ... NOT VALID` (no scan), then `VALIDATE CONSTRAINT` (weaker lock). `SET NOT NULL` skips the scan if a valid `CHECK (col IS NOT NULL)` already proves it. Foreign keys take a stronger lock on both tables. Source: https://www.postgresql.org/docs/current/sql-altertable.html (not re-verified).
- **Backfill in batches, outside the migration transaction:** 1k to 10k rows per batch keyed by primary key range, commit each batch, sleep briefly between batches, make the job resumable and idempotent (`WHERE new_col IS NULL`). One giant `UPDATE` holds locks, bloats the table and can stall replication.
- **Never rename or drop a column the deployed version still uses.** A rename is add + copy + switch + drop.
- Migrations and dumps use a **direct** connection, not the transaction-mode pooler (see section 17).

## 13. Keyset pagination in detail

- Order by a **unique, deterministic key**: `ORDER BY created_at DESC, id DESC`. Without a unique `ORDER BY`, `LIMIT` returns an unpredictable subset; large `OFFSET` still computes every skipped row. Source: https://www.postgresql.org/docs/current/queries-limit.html (not re-verified).
- Use a **row comparison** for the cursor: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT $3`. Row comparison is lexicographic and can use a composite btree index `(created_at DESC, id DESC)`. `NULL` in a deciding column makes the comparison unknown, so order columns must be `NOT NULL`. Source: https://www.postgresql.org/docs/current/functions-comparisons.html (not re-verified).
- Fetch `limit + 1` rows to know whether a next page exists; return an **opaque cursor** (base64 of the last key); enforce a server-side maximum limit; no `COUNT(*)` unless asked.
- Never `findMany`/`SELECT` without a limit on a table that grows, and do not load heavy columns (large JSON, text) in list queries.

## 14. Temporal versioning: insert a new version, close the previous

For data whose history matters (legal text, prices, contracts, permissions), never `UPDATE` in place.

- **Model:** `valid_during tstzrange` with half-open bounds `[)`, or `valid_from`/`valid_to` (`valid_to` null = current). Open upper bound means infinity.
- **Change = one transaction:** close the current row (`UPDATE ... SET valid_to = now() WHERE key = $1 AND valid_to IS NULL`), then `INSERT` the new row. Readers see "the version valid at time T" with a range predicate; "current" is `valid_to IS NULL` (partial unique index `ON (key) WHERE valid_to IS NULL`).
- **Let the database refuse overlaps:** `EXCLUDE USING gist (key WITH =, valid_during WITH &&)` (needs the `btree_gist` extension for scalar equality). Source: https://www.postgresql.org/docs/current/rangetypes.html (not re-verified).
- **Append-only protection:** a trigger that raises on `UPDATE`/`DELETE`, plus `REVOKE TRUNCATE` for the application role, because `TRUNCATE` is its own event and a `DELETE` trigger does not cover it. Source: https://www.postgresql.org/docs/current/sql-createtrigger.html (not re-verified).
- **Prefer derived state to a state column** when it can be computed from the log: a status column drifts from the log; the log is the truth, the state is a query.
- A foreign key should reference the stable key (not a version row) unless the consumer must pin one exact version, in which case reference the version id on purpose.

## 15. Atomic state transitions and upserts

- In Read Committed, `UPDATE ... WHERE state = 'pending'` waits for a concurrent writer and re-evaluates the `WHERE` on the new row version, so it is an atomic transition: check the affected-row count. Read-then-write without a lock or conditional update is a race. In Repeatable Read and Serializable, retry the **whole** transaction on SQLSTATE `40001` (and `40P01` for deadlocks). Source: https://www.postgresql.org/docs/current/transaction-iso.html (not re-verified).
- `INSERT ... ON CONFLICT (cols) DO UPDATE` is the atomic "insert or update" and the building block for idempotent creates and safe counters; `DO NOTHING` returns no row for the skipped one (empty `RETURNING` means it already existed); one statement may not touch the same row twice. Source: https://www.postgresql.org/docs/current/sql-insert.html (not re-verified).
- `FOR UPDATE` blocks other writers and lockers of the row, not readers. Prevent deadlocks by locking in a consistent order. Prefer transaction-scoped advisory locks (`pg_advisory_xact_lock`) over session-scoped ones, which stay on the pooled connection.

## 16. Money columns

`numeric(p,s)` or integer minor units, never `real`/`double precision`. `numeric` rounds ties away from zero when stored with a smaller scale; know it. For ledgers, record the unit and the exchange rate used on each row; never recompute the past with today's rate; make corrections new rows.

## 17. Prisma and a transaction-mode pooler

- **Connection URLs:** application traffic uses the pooled URL; migrations, `pg_dump` and long-lived processes use a direct URL (current Prisma docs put it in `prisma.config.ts`; older versions used `directUrl` in the schema). Prisma Migrate's schema engine needs a single direct connection; through the pooler it fails with `prepared statement "s0" already exists`.
- **Prepared statements:** Prisma uses named prepared statements, which external poolers often do not support. With PgBouncer in transaction mode set `max_prepared_statements` above zero; add `?pgbouncer=true` only for PgBouncer older than 1.21. Other poolers (including Supavisor, which behaves like PgBouncer) may need the flag or disabled prepared statements. Source: https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/pgbouncer (read 2026-11-15).
- **Transaction mode keeps no session state between transactions:** no session `SET`, no session advisory locks, no `LISTEN/NOTIFY`, no temp tables. A different physical connection may serve each transaction.
- **Pool is finite:** a long transaction with external I/O inside exhausts it and turns into timeouts for everyone. Errors `P2024` (pool) and `P2028` (transaction start) mean load, not a bug. Interactive transactions have default `maxWait` 2 s and `timeout` 5 s in v6: keep them short, with no network calls or slow queries inside (not re-verified).
- **Prisma does not retry write conflicts for you:** under Serializable/Repeatable Read or on deadlock, write the retry loop around the whole transaction (SQLSTATE `40001`, `40P01`). Side effects (email, job) go after commit.
- **Raw SQL:** tagged-template `$queryRaw` is parameterized; `$queryRawUnsafe` and `Prisma.raw` are the injection door. A variable replaces a value, never a table, column or keyword; use `Prisma.sql`/`Prisma.join` for `IN (...)`. Raw results are not type-checked: 64-bit integers arrive as `BigInt`, `numeric` as `Decimal`.

## 18. Row-level security with an application setting

Pattern for a shared schema where the database is the second line of defense (the first is the explicit filter, see saas-multitenancy.md):

```sql
ALTER TABLE doc ENABLE ROW LEVEL SECURITY;
ALTER TABLE doc FORCE ROW LEVEL SECURITY;           -- owner is subject too
CREATE POLICY tenant_isolation ON doc
  USING      (tenant_id = nullif(current_setting('app.tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = nullif(current_setting('app.tenant_id', true), '')::uuid);
```

```ts
await db.$transaction(async (tx) => {
  await tx.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`; // true = transaction-local
  return work(tx);
});
```

- **`SET LOCAL` lasts only until the end of the current transaction (commit or rollback); outside a transaction block it emits a warning and has no effect.** `set_config(name, value, true)` is the parameterizable equivalent. Never session-level `SET`: with a transaction-mode pooler the connection is reused by another client and the tenant leaks. Source: https://www.postgresql.org/docs/current/sql-set.html (read 2026-11-15).
- `current_setting('app.tenant_id', true)` (second argument `true`) returns NULL instead of raising when unset; the policy then matches nothing, so a forgotten transaction returns empty rows, never another tenant's.
- With no policy, RLS denies everything; the table owner bypasses RLS unless `FORCE ROW LEVEL SECURITY`; superusers and `BYPASSRLS` roles always bypass. The application role must be none of those. `USING` filters existing rows (they silently disappear); `WITH CHECK` validates new rows (loud error). `INSERT ... RETURNING` and `ON CONFLICT` need a matching SELECT policy.
- **Unique and foreign-key checks bypass RLS** and can reveal that a row exists in another tenant through the error: design keys as `(tenant_id, x)`.
- **Performance:** the policy expression runs per row; keep it a simple comparison on the row's own column, index that column as the **leading** column of a btree, and wrap function calls as `(select f())` so they are evaluated once per statement. Source: https://www.postgresql.org/docs/current/ddl-rowsecurity.html (not re-verified).
- Test with a role that is subject to RLS; tests run as the owner prove nothing.

## 19. Operating Postgres in production

- **Pick the connection by workload:** a Data API/PostgREST client needs no pool; a direct connection for persistent servers, migrations and backups; a session-mode pooler for persistent servers on IPv4-only networks; a transaction-mode pooler for serverless. In serverless create the client once per module scope with a pool of 1 per instance. (Supabase connection guide, not re-verified; the principle holds on any managed Postgres.)
- **Know your platform's default statement timeouts per role** and override per function for heavy work; the database timeout does not protect against a hung network, so the HTTP client also needs its own `AbortSignal` timeout and a single client per process.
- **Silent result caps:** a REST data layer can truncate a response at a configured row limit without error, so set-returning functions need pagination too. Aggregate in SQL, not in memory.
- **Every log or event table is born with a retention period and a batched cleanup job;** without it the system has no steady state (Nygard).
- **Migration source of truth:** versioned files applied by one tool; schema edits through a console create drift. The deploying service checks the expected version at boot.
- **In-database scheduling** (pg_cron or similar) suits cleanup and aggregation (bounded concurrency and duration), not logic that needs application code.
- **A backup counts only after a restore has been tested;** schedule the drill. Free tiers may pause and have no backup.

## Sources

- PostgreSQL docs, SET (https://www.postgresql.org/docs/current/sql-set.html), Client Connection Defaults (https://www.postgresql.org/docs/current/runtime-config-client.html), CREATE INDEX (https://www.postgresql.org/docs/current/sql-createindex.html): read 2026-11-15
- PostgreSQL docs: ALTER TABLE, Row Security Policies, CREATE POLICY, Range Types, CREATE TRIGGER, Transaction Isolation, INSERT, LIMIT and OFFSET, Row and Array Comparisons, Explicit Locking (https://www.postgresql.org/docs/current/): not re-verified
- Prisma docs, PgBouncer: https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/pgbouncer (read 2026-11-15); Connection pool and Transactions pages (not re-verified)
- Supabase, "Connect to your database", https://supabase.com/docs/guides/database/connecting-to-postgres (not re-verified)
- Fowler and Sadalage, "Evolutionary Database Design" (not re-verified)
