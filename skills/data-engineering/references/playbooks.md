# Playbooks: routines, templates, checklists

Tags as in `diagnosis-playbook.md`. Ideas applied, not copied.

## 1. New pipeline (design in 30 minutes)
Write one page before code.
1. Consumer and decision: who reads it, which question, how fresh must it be (minutes, hours, daily).
2. Source: system, how to read it (API, file drop, database replica, CDC, webhook), volume per day, rate limits, auth, owner, change policy.
3. Grain and key of the target table (one sentence: "one row per ...").
4. Load pattern: full reload, incremental by watermark, CDC, append-only event log.
5. Idempotency: rerun of the same window gives the same result (see 2).
6. Quality gates: freshness, volume, uniqueness, not null, accepted values, relationships (`quality.md`).
7. Failure plan: who is alerted, what retries, how to rerun one day.
8. Sensitive fields and retention (see 5).
9. Cost estimate: bytes per run times runs.
Small-team default **[F]**: operational Postgres replica or a managed loader into a warehouse, dbt for transforms, one scheduler.

## 2. Idempotent and backfillable job checklist
- Takes the window as parameters (start, end), never "now" inside the logic.
- Writes with replace-by-partition, merge on a unique key, or `INSERT ... ON CONFLICT DO UPDATE` **[C]**; a plain append is a bug on retry.
- Output unique on the declared key (test).
- Reads immutable inputs (files by date, snapshots) or accepts that history may change and records the read time.
- Staging then swap or one transaction, so a failed run leaves the old data.
- A backfill is the same job over many windows, throttled, run oldest first, with downstream rebuilt after.
- Log per run: window, rows in, rows out, duration, code version.
Postgres detail **[C]**: `DO UPDATE` needs a conflict target, and one command cannot hit the same row twice, so dedupe the batch first.

## 3. Backfill runbook
1. State the window and why. 2. Count rows expected per day from source. 3. Dry-run on one day in a copy schema; compare with production for a day that should be unchanged. 4. Freeze or pause the schedule for the affected tables. 5. Run oldest to newest with a concurrency cap. 6. Compare per-day counts and totals source vs target. 7. Rebuild downstream models and refresh extracts. 8. Resume schedule, write what changed in the run log.

## 4. Incremental dbt model review
- `unique_key` equals the grain and is tested unique and not null **[C]**.
- Filter uses `>=` on a watermark plus a lookback, not `>` **[C]** for the equal-timestamp case.
- `on_schema_change` set on purpose.
- Full refresh path works and its cost is known.
- Hard deletes in the source: decided (ignore, flag, remove).
- Partition or cluster config matches the filter column.
- Tests: unique, not_null, relationships, accepted_values, one business-rule test.

## 5. Sensitive data and retention
Route the law (lawful basis, subject rights, transfers, breach duties) to counsel and the official regulator pages of the data subject's country; this skill covers the engineering.
- Inventory columns that identify a person; classify (direct identifier, pseudonymous, sensitive).
- Collect only what a named use needs; drop or hash fields at the staging layer, not in dashboards.
- Hashing an email with a plain hash is pseudonymisation at best, not anonymisation **[C]**; keep the salt or key outside the warehouse.
- Column and row access by role; separate raw from marts; log who queries sensitive tables.
- Retention: a written period per dataset, a scheduled delete job that also covers backups, snapshots and copies, and a test that counts rows older than the period.
- Deletion requests: a keyed table of subject ids and a job that deletes or nulls across raw, marts and snapshots (snapshots cannot be rebuilt **[C]**, so plan for them).
- Never copy production personal data to a laptop or test database.

## 6. Time zones
Store instants in UTC (`timestamptz`) **[C]**; store the event's local zone or offset when local time matters (store hours, shifts). Choose one reporting zone per dashboard and write it on the page. Daily buckets use that zone, so DST days have 23 or 25 hours; test them. Never subtract local `timestamp` values across zones.

## 7. Cost control checklist
Partition on the date column used in filters; require a partition filter where the platform supports it; cluster only large tables with selective filters **[C]**; select named columns; stage heavy intermediate results; dry-run before big queries and cap bytes billed (BigQuery) or set a resource monitor and auto-suspend (Snowflake, check current feature names); schedule only what is read; review the top 10 queries monthly; tag jobs by team.

## 8. Observability and lineage
Per run: start, end, status, rows, bytes, code version. Per table: last loaded time, row count, test results. Alert on freshness and volume, not on every task failure; one owner and one channel per alert. Lineage: dbt's graph is enough for one project; the open specification OpenLineage records jobs, runs and datasets across tools if you have several.

## 9. Incident write-up (data)
What users saw, first bad timestamp, blast radius (tables, dashboards), cause, detection gap (why no alert), fix, backfill done, new test or check added, owner. Blameless, short, filed with the run log.

## 10. Choosing the tool (see SKILL.md 3 and 4)
Decision record: data volume now and in 12 months, concurrent users, latency need, team skills, budget ceiling, exit cost. Write the rejected options and the trigger that would reopen the decision.
