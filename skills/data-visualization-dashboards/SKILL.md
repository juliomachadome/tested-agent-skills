---
name: data-visualization-dashboards
description: Charts and dashboards people must read and decide from - invoke this skill FIRST, before answering, for any chart choice, dashboard review or data presentation, even a short one. Examples - "which chart for signups by channel over 12 months", "make this dashboard better, it has 22 tiles and nobody opens it", "design a KPI dashboard", "this chart is confusing", "present these numbers to the board", "pick colours that work for colour-blind readers and pass contrast", "Metabase or Looker Studio", pie vs bar, truncated or dual axis, takeaway titles, metric definitions and refresh. Owns the decision (which form, what to cut, honest scales, KPI hierarchy, board pack, BI tool); plotting-library code alone can use a general chart or dataviz skill. Not for the numbers, SQL or significance (data-analysis), which metrics or experiments (growth-analytics), story arc (storytelling), visual system and tokens (ui-design), or pipelines (data-engineering).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Data visualization and dashboards

A chart is an argument made with shapes: one question answered in seconds, and trusted. Evidence tags: **[C]** consensus or standard, **[M]** serious but single, old or lab-based, **[F]** practitioner rule of thumb, **[X]** myth. Sources: `references/BIBLIOGRAPHY.md`.

## 1. Start: project first, then purpose
Read the project's docs first (brand and chart tokens, BI tool, metric definitions, data dictionary, past dashboards); project rules override this skill. Then fix: **who** reads it (one named role, not "everyone"); the **decision or action** it should trigger; the **question** each visual answers; **where** it is read (live talk, wall screen, e-mail, phone, self-serve) and how much control you have over how it is read **[M]**; **how fresh** the data must be. No decision, no visual. Ask for: data sample (units, period), definitions, audience, tool, targets.

## 2. Explore or explain
Exploratory views let an analyst hunt; explanatory views carry one message **[M]**. A dashboard is monitoring (glanceable) or self-serve exploration; decide before drawing.

## 3. Pick the form by the question
| Question | Default | Avoid |
|---|---|---|
| One or two numbers | The number, large, with a comparison and a few words | A chart of two bars |
| Look up exact values, mixed units, many readers with different rows | Table, light rules, aligned numbers, sparklines or conditional colour as aid | Chart with 40 labels |
| Compare categories | Horizontal bars sorted by value, zero baseline | Pie or donut with many slices, 3D |
| Trend over time | Line (bars for few periods or counts) with even time steps | Dual axis, uneven intervals |
| Part-to-whole | Stacked bar for two or three parts, a single 100% bar, or a table; pie only for 2-3 slices with the point stated | Many-series stacked areas |
| Distribution | Histogram, box or strip plot, ECDF | Mean only |
| Relationship | Scatter (labelled outliers, trend only if justified) | Dual-axis lines to imply correlation |
| Change between two points | Slope chart or dumbbell | Two pies |
| Target or progress | Bullet chart or bar with target marker | Gauges |
| Same chart, many groups | Small multiples with shared scales | One chart, 12 colours |
| Geography | Map only if place is the question; else sorted bars | Area-sized regions that mislead |
Readers judge position on a common scale best, then length, angle, area, colour saturation **[C]** (Cleveland and McGill, 1984): put the key comparison there.

## 4. Remove clutter, then guide the eye
Drop borders, heavy gridlines, redundant legends, rotated labels, extra decimals; label lines and bars directly. Group with alignment, proximity and white space **[M]**. Then direct attention with one strong attribute (colour, weight, size) on what matters and grey for context **[M]**. If everything is highlighted, nothing is.

## 5. Colour
- **Categorical**: up to about 5-7 hues; beyond that group, label directly or use small multiples. Never use hue for order.
- **Sequential**: one hue, light to dark for low to high. **Diverging**: two hues around a meaningful midpoint (zero, target), neutral centre.
- **Meaning**: red and green only as a redundant signal.
- **Colour-blind safe**: about 8% of men have a colour-vision deficiency **[M]**; use tested palettes (ColorBrewer "colorblind safe" filter, the Okabe-Ito set), vary lightness, add labels, shapes or patterns **[C]**.
- **Contrast (WCAG 2.2)**: text 4.5:1 (large 3:1), graphics and UI states 3:1, colour never the only signal **[C]**. #9CA3AF on white is 2.54:1 (fails), #767676 4.54:1 (passes); check dark mode. Replace failing colours with values you computed (by hand if no code tool, ratio shown), never "check with a tool".

## 6. Axes, baselines and honest scales
Bars encode length, so they start at zero **[C]**. Lines encode position and slope, so a non-zero baseline is allowed when stated, if the range does not manufacture drama. Keep time steps even; same scale across small multiples unless flagged; label log scales; no dual axes (two aligned panels or index to 100) **[M]**; no cherry-picked windows; no area where a length would do; show denominators, sample size and an interval when the data is a sample; flag partial periods. A rate shown without its base is the classic trap. Misleading-chart patterns and fixes: `references/diagnosis-playbook.md`.

## 7. Annotate and write the takeaway title
Title states the finding, not the topic ("Conversion rose 0.3 points after the checkout change", not "Conversion by quarter"). Subtitle: metric, unit, period; label axes; call out the 1-3 points that matter; source and date in a footnote. Put the "so what" and the action beside the evidence **[M]**. If the data cannot support the headline, soften the headline, not the axis.

## 8. Story with data
Context first (who, what they must do, how delivered), then setup, change, resolution, call to action. One idea per chart; read the titles in order as a sentence **[M]**.

## 9. Dashboard design
- **One purpose, one audience**; two audiences, two dashboards or tabs.
- **KPI hierarchy**: 3-6 top numbers (with comparison: vs previous period, vs target, a sparkline), then the breakdowns that explain movement, then the detail. Most important top-left, above the fold **[F]**.
- **Every number needs**: a definition, a time window, a comparison, a target or "good" range, an owner. Metric definition card and refresh policy: `references/playbooks.md`.
- **Filters**: few, global first, sensible defaults, applied filters visible; none that silently change a definition.
- **Drill-down** summary to cause to record, with a way back.
- **Small multiples and sparklines** over many full charts; about 6-12 tiles per screen **[F]**.
- **Freshness**: show "data as of"; refresh no faster than the decision cycle; mark partial periods.
- **Performance**: fewer rows and visuals, pre-aggregate upstream, cache, limit high-cardinality filters **[F]**.
Brief and checklist: `references/playbooks.md` sections 1 and 6.

## AI tells to avoid (check while creating, not after)
- Default tool palettes and rainbow colours; fix: one highlight colour on grey, with a reason.
- 3D and gradient charts, shadows; flat marks, zero baseline for bars.
- Chart junk and decorative icons; every mark must carry data.
- Every tile the same size; size and position follow importance.
- Titles that name the topic ("Revenue by month"); write the finding.
- 20+ tiles "just in case"; give each tile a reason (decision, owner) or cut it.
- Dark neon dashboard look with no reason (wall screen, brand, audience).
- One message per chart; a chart that makes two points becomes two.
Say what you chose and why in one line; a choice without a reason is removed.

## 10. Accessibility
Colour never alone; contrast per section 5; short alt plus long description or the data table for complex charts (WAI) **[C]**; keyboard and screen-reader access; readable type on a phone; no essential value only on hover; respect reduced motion.

## 11. Tools, as examples
Looker Studio (Google ecosystem), Metabase (SQL or no-code, embedding, open source), Superset (open source, needs admin), Power BI (Microsoft estate), Tableau (rich exploration, licence cost), Vega-Lite, Plotly, Recharts (code, embedded in products). Choose by who builds, data location, governance, embedding, cost, skills; check current docs. Decision table: `references/chart-and-colour-guide.md` section 6.

## 12. Diagnose, fix, deliver
For a bad chart or dashboard run `references/diagnosis-playbook.md`: Step 0 (are the data, definitions and aggregation right) then symptom trees: confusing chart, misleading chart, unused dashboard, slow dashboard, numbers that do not match, wrong audience, inaccessible. Deliver, decision first: the answer and the ask (decision, owner, date) on top; then form and why, redraw spec, metric definitions, what was cut, unverified items.

## 13. Links
Numbers and significance: `data-analysis`. Which metrics and experiments: `growth-analytics`. Narrative: `storytelling`. Visual system: `ui-design`. Pipelines: `data-engineering`.

## 14. Which reference to open
`references/diagnosis-playbook.md` (broken chart or dashboard, honesty and performance trees) · `references/playbooks.md` (dashboard brief, KPI and metric card, chart redraw routine, board pack, refresh policy, review checklist) · `references/chart-and-colour-guide.md` (forms by question, colour recipes, tool notes) · `references/BIBLIOGRAPHY.md`.
