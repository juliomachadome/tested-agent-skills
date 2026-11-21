# Quality, contracts, orchestration, platform choice

## Test layers **[C]** unless tagged
1. Source: freshness (`loaded_at_field`, `warn_after`, `error_after`), volume vs same weekday history, not null on keys.
2. Staging: unique and not null on the key, accepted values, types cast.
3. Marts: grain unique, relationships (every fact key finds a dimension), reconciliation to the source total within a stated tolerance, one business-rule singular test.
4. Unit tests for tricky SQL logic with small fixtures, run in development.
Severity: `error` blocks downstream, `warn` for monitoring; set thresholds (`warn_if`, `error_if`) so a few bad rows do not stop everything unless they must. Store failing rows to inspect them.
Rule **[F]**: every test has an owner and an action; a test nobody reads is noise. Start with ten tests on the tables the dashboards use, not three hundred.

## Contracts
A contract fixes the interface of a model: columns, types, constraints. In dbt, `contract: enforced` fails the build on mismatch; enforcement of constraints differs by platform, so a declared primary key may not be enforced **[C]**. Version a model when a breaking change is unavoidable and give consumers a deprecation date. Between teams, agree contract and owner in writing; the producer notifies before changing.

## Observability **[F]**
Five signals: freshness, volume, schema, distribution (null rate, value ranges), lineage. Add them in that order of value. Alert by owner, with a runbook link.

## Orchestration
| Option | Pick when |
|---|---|
| cron or the warehouse's scheduled queries | one or two jobs, no dependencies; add logging and alerts yourself |
| managed or self-hosted Airflow | many jobs, task dependencies, retries, a data interval concept, backfill by period **[C]**; needs operations effort |
| Dagster | you think in assets and partitions, want lineage and a local dev loop **[C]** |
| dbt Cloud jobs or CI scheduler | transform-only, small team |
One scheduler for the team. Keep the logic in dbt and scripts, the scheduler only calls them. Set retries with backoff, timeouts, and alert on missed runs. Use the data interval or run date as a parameter for backfills.

## Warehouse and engine choice
| Option | Good for | Limits |
|---|---|---|
| Postgres | up to tens of GB or low hundreds of GB of analytics data, OLTP and BI on a replica, simple ops **[F]** | row store, heavy scans slow, contention with the app if not a replica |
| DuckDB | single-node analytics on files, local development, small data **[F]** | one writer, not a multi-user server by itself; check current docs |
| BigQuery | serverless, large scans, pay by bytes scanned or reserved slots | cost surprises without partitioning and caps **[C]** |
| Snowflake | separated compute and storage, many concurrent teams, credit billing | credit spend from idle or oversized warehouses; clustering only for very large tables **[C]** |
Thresholds are **[F]** and move with hardware; measure your slowest query on the current platform before migrating. Pick by team skill and exit cost, not by feature lists. Move when a measured limit is hit (query time, concurrency, storage), not before.

## Data products and ownership **[M]**
For larger organisations, treat key datasets as products with an owner, contract, SLA and documentation (Dehghani's data mesh). Small teams: one owner per table in a YAML file is enough.
