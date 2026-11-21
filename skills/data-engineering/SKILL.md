---
name: data-engineering
description: Use for building, fixing or reviewing data pipelines and the warehouse behind the numbers, even for short questions - "build a data pipeline", "model this in the warehouse", "dbt model", "incremental model misses rows", "our numbers differ between dashboard and database", "events arrive late or duplicated", "warehouse bill is too high", "backfill", ingestion from APIs, webhooks, files or CDC, ELT vs ETL, Postgres vs BigQuery vs Snowflake vs DuckDB, facts, dimensions, grain, slowly changing dimensions, Kimball vs wide tables vs data vault, Airflow or Dagster or cron, data tests, freshness, schema drift, time zones, PII and retention in pipelines, partitioning and clustering, lineage. Small-team defaults first. Not for analysis and SQL questions (data-analysis), dashboards and charts (data-visualization-dashboards), app schema and migrations (engineering-playbook), system design (software-architecture) or privacy law.
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Data engineering

A data pipeline is a promise: the same question gives the same, explainable number tomorrow. Everything below protects that promise cheaply. Evidence tags: **[C]** consensus or documented behaviour, **[M]** serious but single, old or vendor-tied, **[F]** practitioner starting point, **[X]** myth.

## 1. Start: project first, then five facts
Read the current project's docs first (existing dbt project, ADRs, naming rules, data dictionary, access policy, cost limits); project rules override this skill. Then fix in five lines: who reads the number and what decision it feeds; the sources, volume per day and how fast they change; how fresh it must be; the team (who runs it at 3 a.m.); the budget ceiling. If data is missing, ask for the minimum or state the assumption.
Ask for, by task: **numbers differ** - both queries, both results, the period and timezone, a sample row. **Slow or costly** - top queries with bytes or time, table sizes, refresh schedule. **New pipeline** - source description, sample payload, consumer. **Model** - business process, grain, list of questions. **Failure** - run log, last good run, recent changes.

## 2. Small-team default **[F]**
Start with one Postgres (a read replica or a separate analytics database), raw tables loaded as they are, dbt for staging and marts, one scheduler (cron or a managed one), ten tests on the tables dashboards read. Move up only when a measured limit hits: query time, concurrency, storage or cost. A bigger stack is a cost in people, not a sign of maturity **[C]**. Write the trigger that would reopen the choice. Details: `references/quality.md` (platform table), `references/playbooks.md` 10.

## 3. Pick the path
| Task | Go to |
|---|---|
| Numbers disagree, pipeline late or wrong, bill high, backfill broke | `references/diagnosis-playbook.md` (Step 0 then Trees A-G) |
| New pipeline, backfill, incremental model review, PII and retention, time zones, cost checklist, incident write-up | `references/playbooks.md` |
| Ingest from database, API, webhook, file, CDC; ELT vs ETL | `references/ingestion.md` |
| Facts, dimensions, grain, SCD, Kimball vs wide vs vault | `references/modelling.md` |
| Tests, freshness, contracts, orchestrator, warehouse choice | `references/quality.md` |
| Streaming, semantic layer, reverse ETL, dbt CI, catalog, ML features | `references/advanced-topics.md` |
| Sources behind a claim | `references/BIBLIOGRAPHY.md` |

## 4. Ingestion in brief
Land raw, untouched, with `loaded_at` and a batch or file id; fix in staging **[C]**. Choose the load by source: small tables reload fully; large ones load incrementally on `updated_at` with overlap (`>=`); deletes and low latency need log-based CDC; APIs by cursor with raw JSON saved; webhooks verified, stored, acknowledged fast and processed later; files landed immutable and hashed. Assume at-least-once delivery, so duplicates and reordering are normal **[C]**; make the consumer idempotent instead of chasing exactly-once. In Postgres CDC an unused replication slot keeps WAL and can fill the disk **[C]**; monitor lag. ELT (load, then SQL transform) is the default; ETL when data must be masked or reduced before it may land. See `ingestion.md`.

## 5. Modelling in brief
Pick one business process, state the **grain** in one sentence, build facts at that grain and dimensions around them **[C]**. Test the key is unique. Aggregate to the target grain before joining; summing after a one-to-many join is the commonest wrong number. Slowly changing history: type 1 overwrite, type 2 new row with valid-from and valid-to (dbt snapshots; they cannot be rebuilt, so protect them), type 3 prior value column. Styles: Kimball star is the default; one wide table per use case ships fastest but duplicates logic **[F]**; data vault suits many sources, audit and regulated scale and needs a presentation layer **[M]**. Layers: sources, staging, intermediate, marts. See `modelling.md`.

## 6. dbt rules **[C]**
`unique_key` equals the grain and is tested unique and not null. Incremental filters use `>=` plus a lookback sized from the measured lateness, because the default high-water filter misses late rows (the lookback is **[F]**). `on_schema_change` is set on purpose (default ignores new columns). Full refresh is rare and its cost known. Generic tests: unique, not_null, accepted_values, relationships; plus singular tests for business rules, severity set, failures stored. Source freshness with `warn_after` and `error_after`. Contracts on models other teams read; constraint enforcement differs by platform.

## 7. Idempotent, backfillable, late and duplicate-proof
A job takes its window as parameters, never "now"; writes replace the partition, merge on a key, or upsert (`INSERT ... ON CONFLICT DO UPDATE`, which needs a conflict target and a deduplicated batch) **[C]**; leaves old data intact on failure; logs window, rows in and out. A backfill is the same job over many windows, oldest first, throttled, then downstream rebuilt. Late events: measure `loaded_at - event_time`, set the lookback at or above p99, recompute those partitions. Duplicates: stable event id, dedupe in staging, unique test. Runbook: `playbooks.md` 2-3. Worked numbers: `diagnosis-playbook.md` Tree C.

## 8. Quality, orchestration, observability
Tests at four layers (source, staging, marts, unit) **[C]**; every test has an owner and an action. Watch five signals in order: freshness, volume, schema, distribution, lineage **[F]**. Scheduler success is not data success; add data checks and alert on freshness and volume, one owner per alert. Orchestrator: cron for one or two jobs, Airflow for many dependent jobs with a data interval and backfill, Dagster for asset and partition thinking **[C]**; one scheduler per team, logic in dbt and scripts. Lineage: dbt's graph for one project, OpenLineage across tools **[C]**.

## 9. Time, money, people data
Store instants as UTC (`timestamptz` in Postgres) and the local zone where local time matters; one reporting zone per dashboard, written on it; DST days have 23 or 25 hours **[C]**. Money as integer minor units with currency, rounded once at the end. Personal data: inventory columns, collect what a named use needs, drop or pseudonymise in staging, restrict by role, set retention with a delete job that also covers backups and snapshots, never copy production personal data to test. A plain hash of an email is not anonymisation **[C]**. The law (basis, rights, transfers, breach) goes to the privacy law of the data subject's country (official regulator pages).

## 10. Cost control
Find the top 10 queries before changing anything **[F]**. Partition on the date column filters use, filter on that raw column, select named columns, cluster only large tables with selective filters, stage heavy intermediate results, cap bytes billed or set auto-suspend, schedule only what is read **[C]**. `LIMIT` does not cut bytes on non-clustered BigQuery tables **[C]**. Always use the current price page; prices change and are not in this skill. Arithmetic in `diagnosis-playbook.md` Tree D.

## 11. Output standard
Deliver: data and definitions used, Step 0 result, the likely and the second cause with the check that separates them, the fix with the order to apply it, the test or alert that would have caught it, cost or runtime effect with numbers, and what you could not verify (state "unexplained residual" when numbers do not close). Sample SQL is portable and labelled by dialect. Never run destructive commands (drop, full refresh, delete) without naming the target and asking for the go-ahead.

## AI tells to avoid (check while answering, not after)
- Tool lists with no volume per day, team size or cost ceiling behind them.
- Invented warehouse prices or limits; use the current price page.
- A heavy stack (streaming, lakehouse) for data that fits one Postgres.
- A number that does not close, explained away.
Fix: use the user's case and data, sources actually read, one recommendation with its reason and how to verify it. Say what you chose and why in one line; a choice without a reason is removed.

## 12. Boundaries
Analysis, statistics and ad hoc SQL answers go to data-analysis; dashboards and chart design to data-visualization-dashboards; application schema, indexes and migrations to engineering-playbook; system and platform design with ADRs to software-architecture; privacy law to the privacy law of the data subject's country (official regulator pages); cloud deploy and secrets to cloud-deploy-ops; tracking plans and experiments to growth-analytics.
