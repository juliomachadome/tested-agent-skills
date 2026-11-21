---
name: data-analysis
description: Use for any general data analyst task on a business or product dataset, even short ones - "analyse this CSV/spreadsheet", "write the SQL for", "why don't these numbers match", "the join doubled revenue", "dashboard disagrees with the database", "is this difference significant", "clean this data", "build a KPI dashboard", "what does this data say", "forecast next month", or a pasted table or query result. Covers framing the question, SQL (grain, joins, windows, NULLs, dedup, time zones), fact and dimension modelling, cleaning and data quality, exploratory statistics, simple forecasts, pandas and spreadsheets, KPI dashboards, memos and privacy in analysis. Checks data trust first, shows the arithmetic, states uncertainty. Not for experiments, funnels, cohorts of product use or attribution (growth-analytics), chart styling (ui-design), ML models or data platforms, or privacy law.
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Data analysis

An analysis answers one question for one decision. Most wrong numbers come from the data path (grain, join, filter, time zone, definition), not the arithmetic, so trust the data first. Evidence tags: **[C]** consensus or official docs, **[M]** serious but single or older, **[F]** practitioner rule of thumb, **[X]** myth. Sources and check status: `references/BIBLIOGRAPHY.md`.

## 1. Start: project first, then the question
Read the current project's docs first (metric definitions, glossary, schema or data dictionary, ADRs, dashboard specs, privacy notes); project rules override this skill. Then fix in five lines: the question, the decision it feeds and the deadline, the metric definition (numerator, denominator, period, time zone, filters), the data source and its owner, and what would change the conclusion. If a line is missing, ask or state the assumption. Intake template: `references/playbooks.md` section 1.

## 2. Step 0: can the data be trusted?
Before any chart, check: where each number comes from; the **grain** (one row is one what); row counts and distinct keys at each step; the date range, time zone and freshness; filters and test or internal rows; and a reconcile to a source of truth (finance, the production database) **[C]**. A gap above about 1-5% is explained before the finding is. Profile first: nulls, duplicates, ranges, category spellings, impossible dates **[C]** (Tukey, Hellerstein). Full table and worked cases: `references/diagnosis-playbook.md`.

## 3. SQL and modelling rules
- **State the grain** of every table and of the result. Joining a one-row-per-order table to a many-rows-per-order table and summing the order column multiplies it (fan-out). Aggregate to the join grain first, or count distinct keys **[C]** (Kimball).
- Check join cardinality: row count and `count(distinct key)` before and after; in pandas use `merge(..., validate="one_to_many")` **[C]**.
- Inner join drops unmatched rows; left join keeps them as NULL. `NULL = NULL` is not true; `NOT IN` against a subquery with a NULL returns nothing; use `NOT EXISTS` or `IS DISTINCT FROM` **[C]**.
- Window functions for dedup (`ROW_NUMBER`), running totals, previous-row logic, gaps and islands. Give a deterministic `ORDER BY` with a tie-break **[C]**.
- Time: store UTC `timestamptz`, report in one named business time zone, say whether a day is local or UTC, and use half-open ranges (`>= start AND < next_start`) **[C]**.
- Money and rates: numerators and denominators from the same population; safe division with `NULLIF`; say gross or net of refunds, tax and discounts.
- Model for analysis as facts (events, with a declared grain) and dimensions (descriptions); keep one governed definition per metric (semantic layer or a view) **[C]**. Patterns: `references/sql-patterns.md`.

## 4. Cleaning and data quality
Quality is fitness for use, in dimensions such as completeness, validity, uniqueness, consistency, timeliness and accuracy **[M]** (Wang and Strong; DAMA vocabulary **[F]**). Write rules as tests (not null, unique, accepted values, referential integrity, freshness) and run them on every load **[C]** (dbt, Great Expectations docs). Never silently drop or impute: log the count and the rule, and show the result with and without. Tidy shape: one variable per column, one observation per row **[C]**. Checklist: `references/playbooks.md` section 3.

## AI tells to avoid (check while answering, not after)
- Generic advice ("clean your data", "segment more") not tied to the user's table and numbers.
- Invented benchmarks or "typical" rates stated as fact.
- "Significant" or "real difference" with no test, n or interval; a bare p-value or a mean with no spread.
- Running every statistic or chart without saying which one answers the question.
- Slicing many ways with no hypothesis and no count of comparisons.
- Several possible SQL or analysis routes with no pick.
Fix: use the user's data, show the arithmetic or query, state the uncertainty, give one recommendation with its reason and the next check.
Say what you chose and why in one line; a choice without a reason is removed.

## 5. Statistics for analysts
Describe before you infer: n, missing, median and spread, not only the mean; skew and outliers move means **[C]**. Plot the data (Anscombe: identical summaries, different data) **[C]**. Report an effect with an interval and the n, not a bare p-value **[C]** (ASA statement). Small n: say "too noisy to conclude" and show the interval. Many slices or many tries inflate false positives (20 slices at 5% give a 64% chance of at least one hit); name the number of comparisons and control it or label the finding exploratory **[C]**. Aggregates can reverse inside groups (Simpson; mix shift): compare like with like **[C]**. Correlation is not cause; say what design would test it **[C]**. Survivorship, selection and non-response bias: ask who is missing **[M]**. Formulas and worked examples: `references/statistics-for-analysts.md` (incl. base rates, streaks, fat tails). Controlled experiments belong to growth-analytics.

## 6. Forecasting basics
Start with baselines: naive, seasonal naive and a trailing average. A model earns its place only by beating them on held-out recent periods, measured with an error that is scale-free (MASE) **[C]** (Hyndman). Compare same period last year or last week, never a short month with a long one. Give a range, not a point, and say what would break it (price change, launch, holiday shift). ML model building is out of scope.

## 7. Python and spreadsheets
Notebooks and scripts rerun top to bottom from raw data: pinned inputs, no hand edits, a seed, assertions on row counts and key uniqueness **[F]**. Watch silent traps: dtype coercion (IDs read as numbers, dates as text), `NaN` handling in groupby and merge, many-to-many merges **[C]** (pandas docs). In spreadsheets: one table per sheet, no merged cells, formulas over whole columns or tables not fixed ranges, no hard-coded numbers inside formulas, a checks row (totals reconcile to the source) **[M]**.

## 8. Dashboards and BI
Name the audience and the decision; one question per chart; define each KPI once (formula, owner, refresh, source, time zone) and show the as-of time. Bars start at zero; do not truncate or dual-scale to create a story **[C]** (Cairo, Pandey et al.). Choose the form by the comparison (ranking, change, part of whole, distribution, relationship) **[M]** (Cleveland and McGill; Wilke). Style: `skills/ui-design/references/data-tables-dashboards.md`. Spec template: `references/playbooks.md` section 5.

## 9. Communicate
Answer first (one sentence with the number and its range), then the so-what and the recommended action, then assumptions, data caveats, and what would change the conclusion. Show the arithmetic or query so a reviewer can rerun it. Report null results too. Memo and peer-review templates: `playbooks.md` sections 6-7 **[F]** (Knaflic).

## 10. Privacy in analysis
Use the minimum columns; aggregate; suppress small cells (for example groups under 10 people, a house rule **[F]**); pseudonymise keys; no raw personal data in notebooks, screenshots or shared sheets; keep exports out of chat. Law belongs to the privacy law of the data subject's country (official regulator pages).

## 11. Analytical queries on Postgres
Read the plan before adding indexes: `EXPLAIN (ANALYZE, BUFFERS)` on a copy, compare estimated and actual rows **[C]**. Typical wins: filter early, fewer columns, indexes on join and filter columns, a partial index for a hot subset, pre-aggregate with a materialized view refreshed on a schedule (its data is as old as the last refresh) **[C]**. See web-performance and engineering-playbook.

## 12. Boundaries
Product and growth metrics, A/B tests, funnels, activation and retention cohorts, attribution -> growth-analytics. Chart and screen design -> ui-design. Model training, MLOps and data platform engineering are out of scope (data engineering fundamentals: Reis and Housley). Legal advice -> the privacy law of the data subject's country (official regulator pages).

## 13. Output
Match the request: an answer with number, range and caveats; a reconciliation table; rerunnable SQL or code; a quality list; a dashboard spec; or a short memo. Always end with: the data used and its Step 0 result, the arithmetic, the assumptions, what could not be verified, and the single next action with its owner.

## References
`references/BIBLIOGRAPHY.md`. Related skills: growth-analytics, ui-design, web-performance, engineering-playbook.
