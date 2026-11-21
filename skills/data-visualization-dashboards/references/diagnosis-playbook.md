# Diagnosis playbook: broken chart or dashboard, symptom, cause, check, fix

Run top-down. Step 0 first: a chart cannot be better than its numbers. Evidence tags: **[C]** consensus or standard, **[M]** serious but single or lab-based, **[F]** practitioner rule, **[X]** myth. Thresholds are starting points; the project's own rules and the audience's tolerance replace them. Nothing here is copied from a source; ideas are applied.

## Step 0: are the data and definitions trustworthy?
| Check | How | If it fails |
|---|---|---|
| Same number, same definition | Recompute the headline number from the source query or table by hand; compare with the tile | Fix the definition or the query before touching the chart; fold the fix into a metric card (`playbooks.md` 2) |
| Aggregation level and joins | Sum of parts equals total? Row count before and after joins; one row per entity? | A join that fans out inflates sums; hand it to `data-analysis` |
| Period and timezone | Same window, same calendar, partial current period flagged | Cut the partial period or mark it dashed |
| Denominators | Rate = numerator over a stated base; average of averages? | Recompute from sums; show the base |
| Sample size | Small cells (under about 30) swing a lot **[F]** | Merge categories, show the count, add an interval or "not enough data" |
| Freshness | "Data as of" visible; refresh job succeeded | Show the stamp; alert on failed refresh |
| Who reads it and what they decide | One sentence | If you cannot write it, the dashboard has no purpose: stop and run `playbooks.md` 1 |

## Tree A: "this chart is confusing"
| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Reader asks "what am I looking at" | Topic title, no unit or period | Read only the title and axes: is the finding stated? | Takeaway title, subtitle with metric, unit, period |
| Reader cannot find the point | Everything has the same weight; many series; rainbow colours | Squint test: does one thing stand out? | Grey the context, one accent colour, direct labels, small multiples |
| Reader keeps looking back at a legend | Legend far from marks; many categories | Count colours | Label directly; group to 5-7; sort |
| Slices or areas are hard to compare | Pie, donut, 3D, bubbles, stacked areas | Ask which comparison matters | Sorted horizontal bars or a table |
| Lines tangle | Too many series | Count lines | Highlight one or two, grey the rest, or small multiples with shared axis |
| Labels overlap or rotate | Long category names on a vertical axis | Look at phone width | Horizontal bars; shorten names |
| Table is unreadable | Heavy borders, mixed alignment, no emphasis | Check alignment and units | Light rules, right-align numbers, same decimals, conditional colour or sparklines |
| It works on screen, not on a phone | Fixed layout, small type, hover only | Test at 360 px | Stack tiles, larger type, tap targets, tooltips not required |

## Tree B: "this chart is misleading" (patterns, detection, fix)
| Pattern | How to detect | Fix |
|---|---|---|
| Truncated bar axis | Bars do not start at zero; bar ratio does not match value ratio | Bars from zero; or use a dot or line chart with a labelled non-zero baseline |
| Dual axis | Two y scales; crossings imply a relationship that depends on the scale choice | Two aligned panels, or index both to 100 |
| Uneven time steps | Decades then years on one axis; gaps | Even steps; or a broken-axis note |
| Cherry-picked window | Starts at a peak or trough | Show a longer window; mark the event |
| Area or radius encodes a value | Circle area vs radius; 3D | Encode by length or position |
| Cumulative as a trend | A cumulative line always rises | Plot the period values |
| Rate without base | Percent with no n; "up 50%" from 2 to 3 | Show counts and n |
| Correlation drawn as cause | Two trends overlaid | Say what the data cannot show; hand testing to `growth-analytics` |
| Averages hide spread | A mean for a skewed group | Show distribution or median plus range |
| Map by area | Large sparse regions dominate | Normalise per capita; or a sorted bar or cartogram with a note |
| Colour scale hides the pattern | Rainbow, uneven steps, outlier stretches the scale | Sequential palette, clipped range with a note |
| Ignoring uncertainty | A sample estimate shown as a point | Add an interval or a "n=" note |
Worked example (conversion). Q1 384 orders from 12,400 visits = 3.10%; Q2 405 from 11,900 = 3.40%. Relative gain 9.9%. A bar chart with the axis from 3.0% to 3.5% draws bar heights 0.1 and 0.4, which looks like 4 times. On a zero baseline the bars are 3.10 and 3.40 (ratio 1.10). Two-proportion check: z = 1.35, p = 0.18, 95% interval for the difference -0.14 to +0.75 points: the gain is not clearly separate from noise, so the title must not say "conversion jumped". Numbers and tests: `data-analysis`.

## Tree C: "nobody uses the dashboard"
| Cause | Check | Fix |
|---|---|---|
| No decision attached | Ask three users which decision it feeds | Retire it or rebuild around one decision |
| Too many tiles | Count visuals above the fold (over about 12 is a warning **[F]**) | Cut to the KPI row plus the breakdown that explains it |
| Numbers disagree with other reports | Compare against finance or the source system | One metric definition, one owner, shown on the tile |
| Stale or unclear freshness | Last refresh, failed jobs | Stamp, alerts, refresh cadence matched to the decision |
| Slow | Load time over about 5 s feels broken **[F]**; see Tree D | Fix performance first |
| No target or comparison | Does any tile say good or bad? | Add targets, previous period, thresholds |
| Wrong audience | Detail for executives, summary for analysts | Two views, or tabs |
| Not where people work | Usage by channel | Push key numbers to chat or e-mail on a schedule; link to the dashboard |

## Tree D: "the dashboard is slow"
Measure first: time per tile, query time versus render time, rows returned, concurrent users. Then:
| Cause | Fix |
|---|---|
| Raw tables queried at full grain | Pre-aggregate in the warehouse or a semantic or reporting layer |
| Too many visuals each running a query | Reduce tiles; share one dataset across tiles where the tool allows |
| High-cardinality filters or unbounded date ranges | Default to a recent window; limit options; lazy-load |
| Heavy calculated fields per row | Move the logic upstream |
| Cache cold at peak | Warm or schedule extracts and caches; set cache time to the refresh cadence |
| Large extracts in the browser | Return the top N plus "other"; drill for the rest |
Re-measure after each change and keep the before and after. Tool-specific limits are in the vendors' performance docs; check current versions.

## Tree E: numbers do not match another report
Same definition? Same filters? Same time zone and calendar? Same join keys and deduplication? Same refresh time? Currency and tax treatment? Compare totals at the source, then by one dimension at a time until the gap isolates. Document the reconciliation on the metric card. Data work: `data-analysis`; pipeline causes: `data-engineering`.

## Tree F: accessibility failures
| Symptom | Check | Fix |
|---|---|---|
| Colour-blind users cannot separate series | Simulate deficiency; look at lightness only | Tested palette, vary lightness, direct labels, shapes or patterns |
| Low-contrast text | Contrast ratio under 4.5:1 (3:1 large) | Darken grey; #9CA3AF on white is 2.54:1, #767676 is 4.54:1 |
| Marks or UI states hard to see | Under 3:1 against background | Thicker marks, outlines, darker fill |
| Screen reader gets nothing | Chart is an image with no alt | Short alt plus long description or a data table |
| Hover-only values | Keyboard and touch test | Visible labels for key values; focusable controls |
| Motion distracts | Auto-animations | Respect reduced-motion settings |

## Output of a diagnosis
Data and definitions used and their quality; the most likely cause and the second; the redraw or fix spec; what changes for the reader; what you could not verify.
