# Diagnosis playbook: data analysis

Use when a number looks wrong, two numbers disagree, a result seems too good, or a report is slow. Bracketed numbers like [20] point to `BIBLIOGRAPHY.md`. Evidence tags: **[C]** consensus or official docs, **[M]** serious but single or older, **[F]** practitioner rule. Arithmetic in the worked cases was computed with python3 or sqlite; snippets are generic ANSI/Postgres.

## Step 0: is the data trustworthy?
Do these in order, and write the result of each in one line before explaining any finding.

| Check | How | Red flag |
|---|---|---|
| Source and owner | Which system, table or export; who owns it; extraction time | Nobody can say; a screenshot is the only source |
| Grain | "One row is one ___." Write it for every table and for the final result | Two answers, or the answer changes after a join [3] |
| Row counts | `count(*)` and `count(distinct key)` at each step | Counts differ after a join, or distinct < rows on a "unique" key |
| Period and time zone | Min and max timestamp; stored type; reporting zone; local or UTC day | Last day partial; zone not named [49] |
| Freshness | Latest load time vs now; refresh schedule of any materialized view or extract | "As of" missing; matview not refreshed [46] |
| Filters | Test and internal accounts, cancelled or refunded rows, deleted flags, currency | Filters differ between the two reports |
| Definition | Numerator, denominator, gross or net, who counts as "active" | Same name, two formulas |
| Reconcile | Compare to a source of truth (payments provider, finance ledger, production count) for the same period | Gap above about 1-5% is unexplained |
| Profile | Nulls, duplicates, min/max, category spellings, impossible dates, units [15, 29] | Nulls or outliers concentrated in a day, a source, a release |

Rule: a gap between a report and its source is explained before the finding is. Data quality is fitness for use; completeness, validity, uniqueness, consistency, timeliness and accuracy are the usual dimensions to check [38, 18 vocabulary only].

## Tree 1: two reports disagree
1. Same definition? Write both formulas side by side. If different, the answer is "not a bug, two metrics"; rename one.
2. Same population filter? Compare test rows, refunds, cancelled, currency, deleted.
3. Same period boundary? Time zone, half-open ranges, "to date" vs full month.
4. Same grain and joins? Compare row counts at each join.
5. Same freshness? Compare load times; a matview or cached extract lags [46].
6. Bisect: take one day, one customer, one order; trace it through both reports.

Worked case (time zone). Report A counts orders by UTC day, report B by local day (UTC-3). On 5 Oct, 60 orders were placed between 00:00 and 03:00 UTC, so B books them on 4 Oct; and 20 orders placed 00:00-03:00 UTC on 6 Oct land in B's 5 Oct. A shows 2,000 for 5 Oct; B shows 2,000 - 60 + 20 = 1,960. The gap is 40 orders (2.0%), and the net shift is only visible after bucketing both ways. Fix: name the zone in the metric definition, convert once at the reporting layer with `ts AT TIME ZONE 'America/Sao_Paulo'` after storing `timestamptz` [49], and bucket with half-open ranges. Check the DST edge days; a local day can have 23 or 25 hours.

## Tree 2: a join inflated a sum (fan-out)
Symptom: revenue doubles or triples after adding a table; sums grow, counts of orders do not.
Cause: the join key is not unique on the second table, so each parent row repeats once per child row.
Check: `count(*)` vs `count(distinct order_id)` after the join; `group by key having count(*) > 1` on each side.

Worked case. Orders 1, 2, 3 have totals 100, 200, 300 (true sum 600) and 2, 1, 3 items.
```sql
select sum(o.amount) from orders o join items i on i.order_id = o.order_id;  -- 1300
```
1300 = 100x2 + 200x1 + 300x3. Fixes, in order of preference: (1) aggregate the child to the parent grain first (`select order_id, count(*) n from items group by order_id`) and join that; (2) sum from the table that owns the amount; (3) `EXISTS` when you only need to filter parents (gives 600 here). Do not "fix" with `sum(distinct amount)`: two orders of 100 collapse into one. Guard in pandas with `merge(..., validate="one_to_many")` or `"many_to_one"` so a violated assumption raises an error [51]. Add a test: the result row count equals the parent row count, and the total equals the parent total.

## Tree 3: rows vanish or appear after a join
- Inner join drops unmatched rows; left join keeps them with NULLs. Worked case with 5 orders: order 4 has `customer_id` NULL, order 5 has a customer not in the customers table. `orders JOIN customers` returns 3 rows, `orders LEFT JOIN customers` returns 5, and `where c.customer_id is null` finds the 2 orphans (4 and 5).
- NULL keys never match, because `NULL = NULL` is not true; use `IS NOT DISTINCT FROM` if NULL keys should match [47].
- `NOT IN` with a NULL in the subquery returns no rows. With customers 10, 11, 13 and orders by 10, 11, 12 and NULL: `customers where id not in (select customer_id from orders)` returns 0 rows; `NOT EXISTS` returns customer 13.
- A `WHERE` on the right table of a left join turns it into an inner join; move the condition into `ON`.
- Aggregates skip NULL: `avg(customer_id)` over 5 rows with 1 NULL divides by 4. `count(col)` and `count(*)` differ by the NULLs [47].
- Dedup rows with `ROW_NUMBER` and a deterministic tie-break, not `DISTINCT` on all columns (see `sql-patterns.md`).

## Tree 4: a metric jumped (or fell) overnight
Order of suspicion; cheapest checks first.
1. **Pipeline**: duplicate load, missing partition, late data, backfill. Check `count(*)` vs `count(distinct id)` by load date. Example: 1,200 rows/day normally, 2,400 on one day with 1,200 distinct ids means every row was loaded twice.
2. **Definition change**: a filter, a status mapping, a new event name, a currency or tax rule changed. Check the change log and compare old vs new formula on the same day.
3. **Calendar and time zone**: DST edge, month boundary, partial last day, holiday or promotion.
4. **Mix shift**: a new channel, country or plan with a different rate (Tree 5).
5. **Real change**: only after 1-4 are cleared; then segment by one dimension at a time and check the change calendar (release, price, campaign, outage).
Output: the earliest date the series breaks, which of 1-5 explains it, how many rows or euros, and the check that separates it from the second cause. Product-behaviour drops (conversion, activation) go to growth-analytics after Step 0 is clean.

## Tree 5: the average misleads
- **Skew**: 95 orders of 20 and 5 orders of 2,000: mean 119, median 20, standard deviation 431.5, and the top 5% of orders carry 10,000 of 11,900 revenue (84%). Report median and a percentile, plus the share from the top group; "the average" without saying which one is a classic way to mislead [8]. A tail dominated by a few records needs a business look, not a trim [29, 15].
- **Percentile definitions differ**: the 95th percentile of those 100 values is 20 by nearest rank, 119 by linear interpolation (`percentile_cont` interpolates; `percentile_disc` does not) [48]. Name the method.
- **Outliers**: for 12, 14, 15, 15, 16, 17, 18, 19, 21, 95 the quartiles (inclusive method) are 15 and 18.75, the IQR is 3.75, and the 1.5 x IQR fences are 9.4 and 24.4, so 95 is flagged. A flag is a question (typo? whale? test?), not a deletion [15].
- **Mix shift and Simpson's paradox**. Trial-to-paid, Old region: SMB 10/100 (10.0%), Enterprise 180/400 (45.0%), overall 190/500 = 38.0%. New region: SMB 33/300 (11.0%), Enterprise 46/100 (46.0%), overall 79/400 = 19.75%. New is higher in both segments and far lower overall, because 75% of its trials are SMB against 20% in Old. Re-weighted to Old's mix (100 SMB, 400 Enterprise) New would be (0.11x100 + 0.46x400)/500 = 39.0%. Compare within segment, or standardise to a common mix, and say which [21, 42]. The 1-point segment gaps are inside the noise (Tree 6).
- **Ratio of sums vs mean of ratios**: average of per-store rates is not the pooled rate; choose by the question and say which.

## Tree 6: "significant" from tiny n or many slices
- **Tiny n**: 3 of 10 vs 2 of 10 is 30% vs 20%, a 50% relative lift. The 95% Wilson intervals are 11% to 60% and 6% to 51%; they overlap almost entirely. The wide Wald interval for 3/10 (1.6% to 58.4%) is also unreliable at this n [31]. Say "too noisy to conclude" and give the n needed. Small samples also overstate effects that do reach significance [36, 24].
- **Needed n**: detecting a 1-point gap around a 45% rate needs about 2 x (1.96 + 0.84)^2 x 0.45 x 0.55 / 0.01^2 = 38,800 per group (80% power, 5% two-sided). A few hundred rows cannot settle it.
- **Many slices**: 20 independent looks at 5% give 1 - 0.95^20 = 64% chance of at least one false hit. Bonferroni uses 0.05/20 = 0.0025 per test. Benjamini-Hochberg on sorted p = 0.001, 0.008, 0.012, 0.04, 0.2, 0.5 (m = 6) rejects the first three, since 0.012 <= 0.05 x 3/6 = 0.025 and 0.04 > 0.0333 [32]. Count every cut you tried, including the ones not shown; analysis choices made after seeing the data are comparisons too [22]. Label unplanned cuts exploratory; one planned comparison is the confirmatory one [23].
- A p-value does not give the probability the hypothesis is true or the size of the effect; report the interval [23].
- Real controlled tests (random assignment, stopping rules, SRM): growth-analytics.

## Tree 7: a dashboard is slow
1. Measure: `EXPLAIN (ANALYZE, BUFFERS)` on a copy of the slow query; read estimated vs actual rows and the node with the largest time [45].
2. Wrong estimate (rows=10 expected, 2,000,000 actual): stale statistics (`ANALYZE`), skew, or a non-sargable filter.
3. `Seq Scan` on a big table with a selective filter: missing index on the filter or join column; a function on the column (`date(ts)`) blocks a plain index; use a range on the raw column [17].
4. Join fan-out or a many-to-many join before aggregating (Tree 2): aggregate first.
5. Scanning raw events for every viewer: pre-aggregate daily with a materialized view and `REFRESH MATERIALIZED VIEW`; add a unique index to refresh concurrently; show the as-of time because the data is only as fresh as the last refresh [46].
6. Hot subset (`where status = 'paid'`): a partial index [45].
7. Too many tiles or filters firing at once: fewer queries per page, cache by filter, set defaults.
Report before and after in milliseconds and rows. Deeper tuning: web-performance and engineering-playbook.

## Tree 8: the forecast is way off
1. Compute baselines on the same holdout: naive (last value), seasonal naive (same weekday last week), trailing mean. Example, two training weeks then a test week of 102, 121, 133, 124, 146, 198, 181: seasonal naive (repeat week 2) has MAE 4.0, naive 40.1, overall mean 26.8. The in-sample seasonal-naive error on training is 5.43, so MASE of seasonal naive is 4.0/5.43 = 0.74 and a model with MAE 2.71 scores 0.50. Below 1 beats the in-sample seasonal naive benchmark [11, 33].
2. Does the "model" beat seasonal naive on recent periods it did not see? If not, ship the baseline.
3. Structural breaks: price change, launch, outage, a new channel, a holiday that moved. A forecast cannot know them; add them as an adjustment with a label.
4. Leakage: features or normalisation using future data; the test period must be after the training period.
5. Compare like periods: YoY or WoW on the same weekday count; 5 weekends vs 4 weekends is not growth.
6. Report an interval and the error history, not only the point.
Compounding is not linear: 5% monthly growth is 79.6% a year, not 60%.

## Tree 9: survey or sample data may be biased
1. Who could answer? Define the frame and the response rate by group [16].
2. Non-response: if the quick responders differ from the silent ones, the mean is biased. Example: population is 50% young, 50% old; sample is 80% young, 20% old; satisfaction 70% young, 40% old. Raw mean 0.8x70 + 0.2x40 = 64%; re-weighted to the population 0.5x70 + 0.5x40 = 55%. Weighting fixes known imbalance on observed groups, not unknown ones [16, 14].
3. Selection and survivorship: you only see customers who stayed, planes that returned, patients who finished; ask what the missing group looked like. The classic aircraft-armour case is Wald's reasoning about where returning planes were not hit [41].
4. Self-selection and leading questions: separate opinion from behaviour; behaviour data beats stated intent.
5. Ecological fallacy: a group-level correlation does not hold for individuals [43].
6. Regression to the mean: units selected for an extreme first value tend to look less extreme next time with no intervention [37].
7. Small segments: apply Tree 6.
8. A classifier, alert or anomaly rule looks accurate: compute precision at the real prevalence (`statistics-for-analysts.md` 11); a low base rate makes most alerts false.
9. A "best performer" or long streak: count how many candidates and windows you searched before calling it skill (`statistics-for-analysts.md` 11).

## Tree 10: spreadsheet formulas silently broken
Check list when a total is "close but off":
- **Range too short**: 120 rows of 50 summed with `=SUM(A2:A100)` covers 99 rows: 4,950 instead of 6,000, missing 1,050. Use a table or whole-column reference, and a check cell (row count and total vs source).
- **Numbers stored as text**, left-aligned or with trailing spaces: `=SUM` skips them; convert and re-check the count.
- **Dates parsed by locale** (day-month vs month-day) or auto-converted values; gene names such as SEPT2 turned into dates in published supplementary files, about a fifth of the papers scanned [35].
- **Approximate-match lookup** (`VLOOKUP(..., TRUE)` or default) on an unsorted key returns a wrong row without an error; use exact match.
- **Hidden rows, filters, merged cells, manual overrides** inside a formula range.
- **Hard-coded constants** in formulas and copy-pasted values that stopped updating.
- **Averages of averages** across groups of different size.
- A published critique of a widely cited economics paper reported a spreadsheet formula that left out several countries, among other issues [34] (landing page only; details not re-read here).
Fix: keep raw data on its own sheet, formulas on another, a checks block that reconciles to the source, and an owner.

## Output
Findings in order: data used and its Step 0 result; the most likely cause and the second; the check that separates them, with the query; the corrected number with its arithmetic; what could not be verified; the next action and owner.
