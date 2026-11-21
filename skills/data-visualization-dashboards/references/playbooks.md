# Playbooks: dashboards and charts, routines and templates

Evidence tags as in `SKILL.md`. Ideas restated from the sources, never copied.

## 1. Dashboard brief (fill before building)
1. **Audience and role** (one): who opens it, how often, on what device.
2. **Decision or action** it supports, and what a "bad" reading triggers.
3. **Mode**: monitoring (glanceable) or self-serve exploration. Two audiences = two views.
4. **Questions** (3-7), each mapped to one visual or number.
5. **KPI hierarchy**: 3-6 top numbers; the 1-2 breakdowns that explain each; the detail behind a drill-down.
6. **Comparisons and targets**: previous period, same period last year, target, range for "normal".
7. **Metrics**: each with a card (section 2).
8. **Data**: source tables, grain, filters, refresh cadence, row-level access.
9. **Layout**: top-left most important; KPI row at the top; explanation in the middle; detail at the bottom or a drill-down; consistent colours; about 6-12 tiles **[F]**.
10. **Interactions**: global filters (default to the usual question), drill paths, links back.
11. **Success measure**: usage by the named audience and a decision that changed; review date; retire rule.

## 2. Metric card (one per number)
Name; plain-language definition; formula with numerator, denominator and unit; grain (user, order, day); inclusions and exclusions; time window and timezone; source table or query; owner; refresh cadence and "data as of"; known caveats; target and thresholds; version and date of last change. Changing a definition creates a new version noted on the dashboard. Which metrics to choose and how to read them: `growth-analytics`; the calculation itself: `data-analysis`.

## 3. Chart redraw routine (confusing or weak chart)
1. State the single message in one sentence for a named reader.
2. Pick the form by the question (`chart-and-colour-guide.md` 1).
3. Strip: borders, gridlines, legends, 3D, decoration.
4. Fix axes: zero baseline for bars; even time steps; labelled units; one scale.
5. Order: sort bars; order series by the point.
6. Colour: grey for context, one accent, tested palette, contrast per WCAG.
7. Label directly; takeaway title; subtitle; short annotations; source and date.
8. Test: five-second test with a colleague (what do they say the chart shows?); phone width; grayscale; screen-reader text.
9. Deliver the spec: form, data fields, title, axis settings, colours (hex), annotations, alt text.

## 4. Board or executive pack (data presentation)
- Open with the decision and the answer (one page), then the evidence.
- One message per page, title is a sentence; 5-8 evidence pages; appendix for tables **[M]**.
- Each page: number or chart, comparison, "so what", proposed action and owner.
- State assumptions, data quality, what is uncertain and the range; do not show a point estimate alone when the base is small.
- Pre-wire the numbers with the finance or data owner so figures match other reports.
- Live: slides support the talk (practise aloud); sent as a document: more text and detail, since you will not be there to explain **[M]**. Narrative craft: `storytelling`.

## 5. Refresh and operations policy
| Item | Rule |
|---|---|
| Cadence | Match the decision cycle (hourly only if someone acts hourly); finance numbers refresh after close |
| Stamp | "Data as of <time, timezone>" on every dashboard |
| Failures | Alert owner on a failed refresh; show the last good stamp; never silently show partial data |
| Late data | Define a lookback window and restate; mark the last periods provisional |
| Change control | Metric definition changes versioned; announce; keep old values reproducible |
| Access | Row-level rules tested with a restricted test user; exports allowed or not |
| Retire | Review quarterly: usage, decisions, owner; archive the unused |
| Cost and speed | Track load time and query cost per dashboard; budget per team |

## 6. Review checklist (dashboard or chart)
Purpose: one audience, one decision? Questions mapped to visuals? Numbers: every metric defined, windowed, compared, owned? Reconcile one headline number by hand. Form: right chart for each question; tables where lookup is the job? Honesty: zero baseline on bars, no dual axis, even time steps, denominators, n, intervals or caveats, no cherry-picked window? Clutter: borders, 3D, legends, decimals removed? Emphasis: one accent, rest grey? Text: takeaway titles, units, source, date, annotations? Colour: tested palette, contrast 4.5:1 text and 3:1 marks, colour never alone, dark mode? Layout: KPI first, tile count, consistent colours across tiles? Interaction: filters minimal, defaults sensible, drill-down with a way back? Performance: load time measured, queries pre-aggregated? Accessibility: alt text, table behind the chart, keyboard, phone width? Operations: refresh stamp, failure alert, owner, retire date? Output: pass or fix list, ordered by reader impact, with what could not be verified.

## 7. Choosing a tool, in ten minutes
List: who builds, who reads, data location, governance and row-level security, embedding need, budget, skills, export needs. Score two or three candidates 0-3 per line; run one real question end to end in each (connect, model, build one tile, share, refresh); record time spent and blockers. Keep metric logic in the warehouse or shared semantic layer so the tool can change.
