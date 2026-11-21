# Playbooks: data analysis

Templates and checklists. Copy, fill, delete what does not apply. Numbers in brackets point to `BIBLIOGRAPHY.md`. Evidence: **[C]** consensus or official docs, **[M]** serious but single or older, **[F]** practitioner rule.

## 1. Request intake
Ask these before touching data; a vague request produces a polished answer to the wrong question. Interviews with enterprise analysts describe discovery of data, wrangling and profiling as a large share of the work, so budget time for them [28] **[M]**.
```
Question:            (one sentence, answerable with a number or a comparison)
Decision it feeds:   (who decides, what changes if the answer is A or B)
Deadline and depth:  (quick estimate today, or rerunnable analysis in two weeks)
Population:          (which customers, orders, period; what is excluded)
Metric definition:   (numerator, denominator, gross or net, time zone, status filters)
Comparison:          (against what: last period, target, other group)
Data sources:        (tables, exports, owners, last refresh; source of truth to reconcile to)
Known issues:        (tracking gaps, migrations, test accounts, currency)
Format:              (number in chat, table, dashboard, memo; audience)
Privacy:             (personal data involved; allowed columns and aggregation level)
What would change the conclusion? (say it now; it frames the checks)
```
If the requester cannot name a decision, offer one and confirm it. If two definitions are in use, show both numbers and ask which governs.

## 2. Analysis plan template
Write it before the first query, in a notebook header or ticket.
1. **Question and hypothesis** (what you expect and why).
2. **Metric and unit of analysis** (grain statement: one row is one ___).
3. **Data** (sources, extraction time, row counts, join keys and expected cardinality).
4. **Step 0 checks** to run: reconcile total to source, profile nulls and duplicates, time zone, freshness [29].
5. **Method**: look at variation and covariation first [1, 15]; descriptive cuts, comparison, interval method (Wilson for rates, t interval for means), forecast baselines first.
6. **Planned comparisons** (list them now; extra cuts are labelled exploratory) [22].
7. **Stopping point**: what result means "done", what means "need more data".
8. **Deliverable and reviewer**.
Keep the plan with the result; a changed plan is noted, not erased.

## 3. Data quality checklist
Run on every new source and on every load that feeds a report. Express each rule as a test that fails loudly: not null, unique, accepted values, referential integrity, row-count and freshness bounds [53, 54].
| Dimension | Question | Example test |
|---|---|---|
| Completeness | Are expected rows and fields present? | row count within 10% of the same weekday last week; null rate of `email` under 2% |
| Uniqueness | Is the key unique? | `group by id having count(*) > 1` returns 0 rows |
| Validity | Do values fit type, range, format, set? | `amount >= 0`; `status in (...)`; dates between 2020-01-01 and today |
| Consistency | Do tables and systems agree? | order total equals sum of line items; orders per day equal the production count |
| Timeliness | Is it fresh enough for the decision? | latest `loaded_at` under 6 hours old; matview refresh time shown [46] |
| Accuracy | Does it match the real world? | sample 30 rows against the source documents; reconcile revenue to the payments provider |
| Referential integrity | Do foreign keys resolve? | `orders left join customers where customers.id is null` returns 0 |
Dimensions follow the data-quality literature and the DAMA vocabulary [38; 18 for vocabulary]; a given list is a convention, not a standard to cite for compliance (ISO/IEC 25012 defines a data quality model but was not read here [55]).
Handling issues:
- Log each rule hit with counts and the decision (fix at source, exclude, impute, flag). Never drop or fill silently; show the result with and without the treatment [29].
- Prefer fixing at the source; transformations in the analysis layer are documented and tested.
- Tidy shape for analysis: each variable a column, each observation a row, each observational unit a table [20]. Interactive wrangling tools that record each transformation as a script keep cleaning reproducible [27].
- Keep a "known issues" list with owner and date; check it when a number moves.

## 4. Notebook and pipeline reproducibility checklist
- [ ] Inputs: raw data stored read-only with extraction time and query; no manual edits; versioned or hashed.
- [ ] One command runs everything top to bottom; restart the kernel and run all before sharing.
- [ ] Random seeds set where sampling or bootstrap is used; library versions recorded.
- [ ] Assertions after loading and after each merge: row counts, key uniqueness, no unexpected nulls; in pandas `merge(..., validate="one_to_one" | "one_to_many" | "many_to_one")` [51] and explicit dtypes (IDs as strings, dates parsed with a format and zone) [2, 52].
- [ ] Missing data handled on purpose: pandas treats `NaN`, `NaT` and `None` in specific ways in groupby, merge and aggregation; test with a toy frame [52].
- [ ] Parameters (dates, thresholds, zone) at the top, not buried in cells.
- [ ] SQL kept in files with the grain comment; no `select *` in production queries.
- [ ] Outputs include the as-of time, filters, n, and a link or path to the code.
- [ ] A reviewer can reproduce the headline number from raw data in under an hour.
- [ ] Sensitive data not committed; outputs aggregated before sharing.
- [ ] Spreadsheets: raw data sheet, calculation sheet, checks block; no hidden rows in ranges; formulas over tables or whole columns [34, 35].
Pipeline and platform engineering beyond this checklist is data engineering, out of scope here [13]. Exploratory notebooks are allowed to be messy; anything that feeds a decision or a recurring report is converted to the checklist above.

## 5. Dashboard spec template
Fill this before building. A dashboard answers a small set of recurring decisions; if nobody can name the decision, do not build the tile [6, 4].
```
Dashboard name and owner:
Audience and decision:       (who looks, how often, what do they do with it)
Questions, one per chart:    (1) ... (2) ...
KPI definitions:             for each KPI: name, formula (numerator, denominator),
                             grain, filters, gross or net, time zone, owner of the definition,
                             source table or view, target or threshold and who set it
Refresh and freshness:       (schedule, as-of timestamp shown, who fixes failures)
Data quality checks:         (reconcile to source weekly; tests that block the refresh)
Dimensions and filters:      (default period, default segment; avoid more than needed)
Chart choices:               (comparison type -> form: ranking -> sorted bars; change over time -> line;
                              part of whole -> few categories only; distribution -> histogram or box)
Axes and scales:             (bars start at zero; no dual axes that invent a correlation;
                              same scale across small multiples) [7, 39, 19]
Annotations:                 (launches, price changes, outages, definition changes)
Access and privacy:          (who may see it; aggregation threshold, e.g. no cell under 10 people [F];
                              no personal data in tooltips or exports)
Performance budget:          (loads in under N seconds; source is a view or materialized view) [45, 46]
Retirement:                  (review date; delete if unused for 90 days [F])
```
Design details (tokens, table layouts, density, accessibility) are in `skills/ui-design/references/data-tables-dashboards.md` and the dataviz guidance; this skill decides what to show, ui-design decides how it looks. Form follows the comparison asked, and position and length are read more accurately than angle, area or colour [40, 19]. Think of a chart as data mapped to marks and scales, one message per chart [26]. The size of a visual effect should match the size of the data effect (Tufte's graphical integrity) [5]. Single-number tiles need a comparison (versus target or prior period) or they invite a shrug [6]. One governed definition per KPI, stored once, avoids two dashboards telling two stories (dimensional models and a shared metric layer) [3].

## 6. Insight memo template
Answer first. A reader gives you two minutes [4].
```
Title: the finding in a sentence, with the number
(e.g. "Net revenue for October was 1,620, not 1,820; two definitions differ by 200")

Answer (2-3 lines): number, range or interval, direction, confidence in words.
So what / recommendation: action, owner, date. What it costs not to act.
Evidence: 1-3 charts or a small table; each titled with its message; n and period in the caption.
Method in four lines: data source and as-of time, definition, filters, comparison.
Assumptions and data issues: what was excluded or imputed and how many rows; reconciliation result.
Uncertainty: interval or sensitivity (what if the other definition is used); what would change the conclusion.
Not verified: items you could not check, with the cheapest check.
Next step: the question that remains and the data needed.
Appendix: code or query path, tables, definitions.
```
Rules: one message per memo; separate the finding from the interpretation; do not bury a null result; avoid decimals the data cannot support; keep causal language for causal designs; say "associated with" otherwise [12, 10]. State the claim at the strength the evidence allows (descriptive, associational, causal).

## 7. Peer review of an analysis
Reviewer reproduces the headline number first, then reads in this order. Give findings with severity: blocker, should fix, nit.
1. **Question**: does the analysis answer the stated question and decision?
2. **Definitions**: metric and population written down; same as the project definition?
3. **Data trust**: Step 0 done; reconcile to source; freshness; time zone.
4. **Grain and joins**: row counts before and after each join; any fan-out or dropped rows; NULL keys.
5. **Cleaning**: exclusions and imputations logged with counts; sensitivity shown.
6. **Statistics**: n shown; intervals not only p-values; multiple comparisons counted; small-n caution; mix shift checked.
7. **Comparisons**: like periods; baseline for forecasts; leakage.
8. **Charts**: zero baseline for bars, honest axes, labelled units, one message per chart [7, 39].
9. **Claims**: causal language only with a causal design; limits stated.
10. **Reproducibility**: reruns from raw data; seeds; versions.
11. **Privacy**: minimum columns, small-cell suppression, no personal data in the deliverable.
12. **Communication**: answer first; assumptions visible; next action named.
Close with: "Blockers: ..., Should fix: ..., Could not verify: ...". Authors answer each point in the document, not in chat.
