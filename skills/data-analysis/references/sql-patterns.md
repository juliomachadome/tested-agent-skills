# SQL patterns for analysis

Generic ANSI/Postgres SQL. The snippets with numbers were run (sqlite 3.53 for window functions, CTEs and filters; Postgres-only syntax is marked). Check dialect differences before production use. Numbers in brackets point to `BIBLIOGRAPHY.md`. Evidence: **[C]** official docs or consensus, **[F]** practitioner rule.

## 1. Grain first
Write the grain in a comment on every query: `-- grain: one row per order`. A join on a column that is not a key of one side repeats rows; keys are what make relational results predictable [30]. Before joining, know each side's grain; after joining, check that the row count and the distinct parent keys are what you expect [3].
```sql
-- grain: one row per order_id (check: both numbers must be equal)
select count(*) as rows_, count(distinct order_id) as orders from result;
```
Fan-out rule: join a parent to a child, then summing a parent column multiplies it by the child count. Aggregate the child to the parent grain in a CTE first [3, 48]:
```sql
with item_counts as (select order_id, count(*) as n_items from items group by order_id)
select o.order_id, o.amount, coalesce(ic.n_items, 0) as n_items
from orders o left join item_counts ic using (order_id);   -- still one row per order
```
Grain checklist for a metric: numerator grain = denominator grain; filters apply to both; the date used (created, paid, shipped) is named.

## 2. Deduplicate with ROW_NUMBER
Keep the latest row per key, with a tie-break so the result is deterministic [44]:
```sql
select id, user_id, plan from (
  select *, row_number() over (partition by user_id order by updated_at desc, id desc) as rn
  from user_events) t
where rn = 1;
```
Run on rows (1,u1,Jan,free), (2,u1,Feb,pro), (3,u2,Jan15,free), (4,u2,Jan15,free2): returns id 2 and id 4; without `id desc` the u2 pick would depend on physical order. Postgres shortcut: `select distinct on (user_id) ... order by user_id, updated_at desc, id desc` [48]; without the `ORDER BY` the row kept is unpredictable. Find the duplicates first: `group by key having count(*) > 1`. Deduplicating hides a pipeline bug; also fix the source.

## 3. Gaps and islands (streaks, continuous periods)
Subtract the row number from the date; consecutive days share a constant [44]:
```sql
select user_id, min(d) as start_d, max(d) as end_d, count(*) as days from (
  select user_id, d, d - (row_number() over (partition by user_id order by d))::int as grp  -- Postgres: date - int
  from (select distinct user_id, d from activity) a) x
group by user_id, grp;
```
Days 1, 2, 3 and 7, 8 of March give two islands: 1-3 (3 days) and 7-8 (2 days). `distinct` first, otherwise two events on one day break the arithmetic. A gap is the day after an island ends up to the day before the next starts.

## 4. Running totals, moving averages, period-over-period
```sql
select d, amt,
  sum(amt) over (order by d rows between unbounded preceding and current row) as running,
  avg(amt) over (order by d rows between 2 preceding and current row)        as ma3,
  lag(amt) over (order by d)                                                 as prev
from daily;
```
For 100, 50, 70, 0: running 100, 150, 220, 220; 3-row average 100, 75, 73.3, 40 (the first rows average fewer than 3 values, say so or drop them). Use `rows` or `range` deliberately: `range` with ties includes peers [44]. Percent change: `rev * 1.0 / nullif(lag(rev) over (order by month), 0) - 1`; for 100, 120, 90 it gives NULL, +20.0%, -25.0%. Mind integer division: `1/2 = 0` in many engines; multiply by `1.0`.

## 5. Conditional aggregation and FILTER
```sql
select g, count(*) filter (where v >= 9) as hi,                  -- Postgres, sqlite
       sum(case when v >= 9 then 1 else 0 end) as hi_portable    -- any engine
from s group by g;
```
Both give the same count; `FILTER` is clearer [48]. Use it for pivot-style columns and for "share of rows meeting a condition" without a self-join.

## 6. Cohorts and retention
Cohort = group of users by first-event period; compare each later period against the cohort size.
```sql
with c as (select user_id, date_trunc('month', first_seen) as cohort_m from users),
a as (select distinct user_id, date_trunc('month', ts) as active_m from events)
select c.cohort_m, a.active_m, count(*) as active_users
from c join a using (user_id) group by 1, 2 order by 1, 2;
```
Divide by the cohort's month-0 size, not by the number active in month 1. Cohort of 3 users in Jan: active 3, 2, 1 in Jan, Feb, Mar gives 100%, 67%, 33%. A cohort's latest period is incomplete: mark it. Product retention interpretation, activation definitions and funnels: growth-analytics.

## 7. Sessionisation
A new session starts on the first event or after a gap above a threshold (30 minutes is a convention [F], set it per product) [44]:
```sql
select user_id, ts, sum(new_s) over (partition by user_id order by ts) as session_id from (
  select user_id, ts,
    case when lag(ts) over (partition by user_id order by ts) is null
           or ts - lag(ts) over (partition by user_id order by ts) > interval '30 minutes'   -- Postgres interval
         then 1 else 0 end as new_s
  from hits) t;
```
Events at 10:00, 10:10, 11:00, 11:05 give sessions 1, 1, 2, 2. Bots, background pings and clock skew distort sessions; report the rule with the number.

## 8. Date spine (no missing days)
Left join facts onto a calendar so days with zero rows appear, otherwise averages and charts skip them [50]:
```sql
select d::date as day, coalesce(sum(r.amt), 0) as amt                                   -- Postgres
from generate_series('2026-03-01'::date, '2026-03-05'::date, interval '1 day') d
left join rev r on r.day = d::date group by 1 order by 1;
```
For daily 100, 50, 70, 0 and nothing on the 5th, the spine returns five rows (the fifth 0). In engines without `generate_series`, use a recursive CTE [48]. Weekly or monthly spines: use the same pattern with `date_trunc`; keep the spine in the reporting time zone.

## 9. Slowly changing dimensions (as-of joins)
A Type 2 dimension keeps one row per version with `valid_from` and `valid_to` (exclusive end); join facts on the key and the time [3]:
```sql
select f.order_id, c.plan from fact_orders f
join dim_customer c on c.customer_id = f.customer_id
 and f.ordered_at >= c.valid_from and f.ordered_at < c.valid_to;
```
A customer on `free` until 1 March and `pro` after: orders on 15 Feb, 1 Mar and 1 Apr map to free, pro, pro. Overlapping or gapped validity ranges multiply or drop rows: test that ranges per key do not overlap and cover the timeline. Decide whether a report wants the plan at the time of the order (as-of) or today (current row), and say which.

## 10. Time zones and calendars
- Store instants as `timestamptz` (UTC); a `timestamp` without zone has no instant [49].
- Convert to the business zone once: `ts AT TIME ZONE 'Europe/Warsaw'` turns a `timestamptz` into local wall-clock time [49]. When comparing a plain timestamp with a `timestamptz`, the plain one is read in the session `TimeZone` [49]; set it explicitly.
- Half-open ranges: `ts >= '2026-10-01' and ts < '2026-11-01'`. `BETWEEN` includes the end instant and drops or duplicates rows at midnight.
- Days on DST changes have 23 or 25 hours; "per hour" rates need care; weeks start on Monday (ISO) or Sunday: name it.
- Fiscal calendars, holidays and trading days live in a calendar table, not in code.

## 11. Percentiles and medians
`percentile_cont(0.5) within group (order by x)` interpolates between neighbours; `percentile_disc` returns an actual value [48]. For 95 values of 20 and 5 values of 2,000, the 95th percentile is 119 (`cont`) or 20 (`disc`, also nearest-rank). Name the method in the report. Medians per group: `select g, percentile_cont(0.5) within group (order by x) from t group by g` (Postgres). Top-N per group: `row_number() over (partition by g order by v desc, id) <= n`.

## 12. Safe division and rates
```sql
select numerator * 1.0 / nullif(denominator, 0) as rate from t;   -- NULL when denominator is 0
```
`NULLIF(a, b)` returns NULL if equal [47]. Decide whether a NULL rate means "not defined" (show a dash) or "0" (zero numerator); `coalesce(..., 0)` hides undefined cases, so use it knowingly. Pooled rate is `sum(num) / sum(den)`; mean of per-row rates is a different, often wrong, statistic.

## 13. NULL traps
| Trap | Behaviour | Safe pattern |
|---|---|---|
| `x = NULL` | never true | `x is null` |
| `x <> 'paid'` | NULL rows are excluded | `x is distinct from 'paid'` [47] |
| `NOT IN (subquery)` with a NULL in it | returns no rows | `NOT EXISTS` |
| `NULL = NULL` in a join | does not match | `is not distinct from` if intended [47] |
| `count(col)` vs `count(*)` | col skips NULLs | choose on purpose |
| `avg(col)` | skips NULLs | decide if NULL means 0 |
| `sum` of an all-NULL set | NULL, not 0 | `coalesce(sum(x), 0)` |
| `a + NULL` | NULL | `coalesce` each operand deliberately |
| `order by` with NULLs | position differs by engine | `nulls last` |
| `where right.col = 1` after a left join | acts as inner join | put the filter in `ON` |
Worked: orders (5 rows) with `customer_id` 10, 10, 11, NULL, 12 and `status` paid, paid, paid, paid, refunded. `status <> 'paid'` counts 1; `customer_id <> 10` counts 2 (the NULL row vanishes); `customer_id is distinct from 10` counts 3. `avg(customer_id)` is 10.75 (43 / 4), `count(customer_id)` 4, `count(*)` 5.

## 14. Reusable review checklist for a query
1. Comment states grain, period, zone, filters.
2. Row counts at each join step logged or tested.
3. Keys unique where assumed; deduplicated deterministically.
4. NULL behaviour of every filter and join reviewed.
5. Date boundaries half-open; zone named.
6. Result reconciled to a known total.
7. `EXPLAIN` read if it will run on a schedule or feed a dashboard [45].
