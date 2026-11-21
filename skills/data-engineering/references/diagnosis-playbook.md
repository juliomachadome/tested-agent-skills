# Diagnosis playbook: symptom, likely causes, check, fix

Use top-down. Step 0 first: a wrong denominator, timezone or duplicate makes every branch meaningless. Tags: **[C]** consensus or documented behaviour, **[M]** serious but single or old, **[F]** practitioner starting point, **[X]** myth. Thresholds are **[F]** until replaced by the team's own history. Nothing is copied; ideas are applied.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Same question asked of both sides | write the metric as one sentence: entity, filter, period, timezone, currency, refunds in or out | agree the definition before comparing numbers |
| Same time window and timezone | compare 3 rows by hand across both systems (`timestamptz` is stored in UTC and displayed in the session zone, `timestamp` ignores zones **[C]**) | convert both to one zone and one cut-off |
| Row counts per layer | count at source, raw, staging, mart for one day | the first layer where counts diverge is the suspect |
| Grain | `select key, count(*) ... having count(*)>1` on the table's declared key | duplicates mean the grain is wrong or a join fans out |
| Run history | last successful run per model, any manual edits, full refreshes, backfills | compare with the change calendar (deploys, schema changes, vendor outages) |
| Who reads what | exact query behind the dashboard, copy it, run it | never debug from a screenshot |

## Tree A: "dashboard and database disagree"
Reconcile top-down: total, then split by day, then by key, until one bucket explains the gap.
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| Gap near the period edges, sign flips by day | timezone cut-off (UTC vs local) | group by date in both zones, compare edge hours | one reporting timezone, stored in config; keep UTC instants |
| Dashboard larger, gap grows with joins | fan-out: join to a many-side table before sum | count rows before and after the join; compare `sum` on the one-side table | aggregate to the target grain before joining; test uniqueness |
| Dashboard larger by whole rows | duplicates (webhook or batch retry) | duplicates on business key in raw | dedupe on a stable event id in staging; unique test |
| Dashboard smaller | late rows never merged, filter on `status`, inner join dropping unmatched | rows in source not in mart (anti-join) | lookback window; left join plus a relationships test |
| Same numbers on different days | cache or stale extract | last refresh time of the dashboard and of the model | freshness test; show "data as of" |
| Money differs by cents | rounding at different steps, float | store integer minor units or numeric | round once, at the end |
Worked example: DB October total 398,450.00; dashboard 407,010.00; gap 8,560.00 (2.15%). Timezone edge: 58 orders worth 7,780 near 31 Oct night, minus 41 orders worth 5,320 near 1 Oct = net 2,460. Duplicate webhook rows 6,100. 2,460 + 6,100 = 8,560, fully explained; always end with the residual and say if it is zero.

## Tree B: pipeline is late, failed or silently stale
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| Job failed, downstream ran on old data | dependencies by clock, not by data | scheduler graph: does the mart wait for the load? | dependencies by asset or sensor; freshness gate before the build |
| Succeeds but counts fall | upstream empty or partial file, API pagination stopped | volume test vs last 14 days of the same weekday | volume check with threshold; fail on zero rows |
| Slow growth in runtime | full scans, full refresh, small-file problem | query profile, bytes scanned per run | incremental with partition pruning; compaction |
| Random night failures | rate limits, lock contention, source maintenance | error text and times | retries with backoff, jitter, off-peak slot |
| Works locally, fails in prod | secrets, permissions, different data volume | run the same job id with prod config on a copy | environment parity; least-privilege test account |
Scheduler "success" proves the process ended, not that the data is right **[C]**. Add data checks.

## Tree C: late or duplicate events
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| Counts for yesterday keep changing for days | late arrival (offline devices, queues) | distribution of `loaded_at - event_time` | lookback window of at least the p99 lateness; recompute those partitions |
| Same event twice | at-least-once delivery, client retries, replay **[C]** | duplicates on event id | dedupe on id with `row_number() over (partition by id order by loaded_at desc)`; upsert on a unique key |
| No stable id | producer never set one | derive a hash of natural fields and say it is a proxy | ask producers for a UUID per event |
| Incremental model misses rows | high-water mark on event time, rows arrive older than the mark | rows in raw not in model | `>=` plus lookback; or rebuild affected partitions |
| Out of order updates | older version overwrites newer | compare source version or `updated_at` | merge only when incoming is newer |
Worked example: 2.4M events per day, 0.8% duplicates = 19,200 a day. A 3-day lookback reprocesses 7.2M rows; the 180-day table holds 432M, so the lookback touches 1.67% of it. Choose the lookback from the measured p99 (here 52 h, so 3 days covers it), not from habit.

## Tree D: "the warehouse bill is too high"
Get the per-query cost list first (BigQuery job metadata, Snowflake query history, Postgres `pg_stat_statements`); the top 10 queries usually carry most of the cost **[F]**.
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| One dashboard query tops the list | refresh every N minutes on an unpartitioned table | bytes per run times runs per month | partition on the date column, require a partition filter, raise refresh interval, pre-aggregate |
| Nightly full refresh | incremental models rebuilt with `--full-refresh` | scheduler command history | full refresh only on a schema change |
| `select *` on wide tables in a columnar store | reads every column | bytes billed vs needed | list columns; staging models that keep only used columns |
| Partition filter exists but bytes unchanged | filter on a derived expression, or wrong column | dry run bytes before and after **[C]** | filter on the raw partition column |
| `LIMIT` used to cut cost | on non-clustered tables it does not cut bytes **[C]** | dry run | filter or sample properly |
| Clustering added, no gain | table small, or filter columns differ | table size, filter columns | skip it under very large tables **[C]** |
Worked example (illustrative price of 6.25 per TiB, check the current price): a dashboard scans 0.18 TiB hourly, 720 runs a month = 129.6 TiB = 810 per month. Partition by day and read the last 7 of 180 days: 0.18 x 7/180 x 720 = 5.04 TiB = 31.50. Saving 778.50. A nightly full refresh of 4 models at 0.9 TiB: 4 x 0.9 x 30 = 108 TiB = 675. If the bill rose by 5,500 and these two explain 1,485, say that 4,015 is unexplained and go to the job list.

## Tree E: model or dashboard slow
Check the plan first (`EXPLAIN` in Postgres, query profile elsewhere). Row store: missing index or sequential scan on a filtered column. Columnar store: too many columns, no partition pruning, joins on skewed keys, repeated subqueries. Materialise the heavy step, not the whole chain.

## Tree F: schema drift and broken contracts
| Pattern | Cause | Check | Fix |
|---|---|---|---|
| Model fails on a missing column | producer renamed or dropped | compare source schema to last run | contract on the staging layer, alert on drift, versioned model for breaking change |
| New column ignored | `on_schema_change` default is ignore **[C]** | model config | `append_new_columns` or fail, by choice |
| Types silently widen | loose typing in raw | column types over time | cast in staging, enforce contract |

## Tree G: backfill went wrong
| Pattern | Cause | Fix |
|---|---|---|
| Double counted after rerun | append instead of replace | write by partition overwrite or delete-then-insert in one transaction, or merge on key |
| Results differ per run | uses `now()` or a mutable source inside the transform | pass the run date as a parameter; read snapshots, not live tables |
| Downstream not refreshed | backfill touched one layer | rebuild downstream of the changed range |
