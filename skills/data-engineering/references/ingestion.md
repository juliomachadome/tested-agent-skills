# Ingestion: batch, CDC, APIs, webhooks, files; ELT vs ETL

## ELT vs ETL **[C]**
ELT loads raw data into the warehouse, then transforms in SQL there; fits cloud warehouses where compute is separate and SQL is the shared skill. ETL transforms before loading; still right when data must be masked or reduced before it may enter the target, when the target is small, or when the transform is not SQL-friendly (parsing binary files). Default for small teams: load raw as is (plus load metadata), transform with dbt **[F]**.

## Patterns
| Source | Pattern | Watch for |
|---|---|---|
| Database table, small | full reload daily | cost and lock time; fine below millions of rows **[F]** |
| Database, large | incremental by `updated_at` or id | rows updated without touching the column, hard deletes, clock skew; use `>=` plus overlap |
| Database, need deletes and low latency | CDC from the log (in Postgres, logical decoding with a replication slot) | an unused slot retains WAL and can fill the disk **[C]**; monitor slot lag, drop slots you no longer use |
| REST API | paginate by cursor, store the raw JSON, respect rate limits | cursors expire, pages shift while reading, ids missing; save the request params and time with each page |
| Webhook | receive, verify the signature, store the raw body, acknowledge fast, process later | senders retry, so duplicates and out-of-order are normal **[C]**; dedupe on event id; keep a replay path |
| Files (CSV, parquet, exports) | land immutable by date, one manifest row per file | encodings, header changes, partial uploads (write to a temp name then rename), same file delivered twice (hash it) |
| Event stream | append-only log; process by event time | late data, watermark choice **[M]** |

## Delivery semantics
Networks retry, so assume **at-least-once** and make the consumer idempotent (dedupe key or upsert) rather than chasing exactly-once **[C]**. Keep both `event_time` (when it happened) and `loaded_at` (when you got it); the gap is your lateness distribution.

## Raw layer contract
Every raw table: source name, loaded_at, batch or file id, payload untouched. Never mutate raw. Schema drift is expected: land semi-structured fields as JSON and extract in staging.

## Managed loader or custom code
Use a managed connector when one exists for the source and the cost is below the engineer time; write custom code for odd sources, and keep it small, parameterised by window, with tests. Check the vendor's pricing model (often per row or per connection) before committing.
