# Chart, colour and tool guide

Tags: **[C]** consensus or standard, **[M]** serious but single or lab-based, **[F]** practitioner rule. Ideas restated, not copied (see `BIBLIOGRAPHY.md`).

## 1. Choosing by question
Start from the question and the number of values:
- **One or two numbers**: write them large with a comparison and a few words; a table or chart for two numbers dilutes them **[M]**.
- **Exact lookup, many small items, mixed units, a mixed audience**: a table. Rows sorted by something meaningful; numbers right-aligned with the same decimals; light rules or none; units in the header; highlight only the few cells that matter.
- **Compare categories**: bars. Horizontal when names are long; sort by value unless the order is natural (time, stages); zero baseline; gaps between bars; stacked only when the parts matter less than the total or you compare the first segment.
- **Time**: line for continuous series, columns for few periods; consistent steps; annotate events; compare with the same period last year when seasonal.
- **Part-to-whole**: few parts, one total; 100% bar or stacked bar; pie only with 2-3 slices and a single point.
- **Distribution**: histogram (try several bin widths), box or violin with raw points for small n, cumulative distribution for comparing groups.
- **Relationship**: scatter; transparency or binning for overplotting; label the outliers; a fitted line only if you state the method.
- **Ranking change or two-point change**: slope or dumbbell.
- **Progress to target**: bullet chart; avoid gauges, which waste space for one value **[M]**.
- **Many groups, same measure**: small multiples with shared axes; sparklines in a table for trends of many rows.
- **Flows and funnels**: funnel as sorted bars with conversion between steps; Sankey only for few nodes.
- **Maps**: when location is the story; normalise values; keep a sorted bar next to the map.

## 2. Colour recipes
| Need | Do |
|---|---|
| Emphasis | Neutral grey for context, one saturated accent for the point |
| Categories | 3-7 distinct hues of similar lightness weight; legend ordered as the data; same colour for the same entity in every tile |
| Low to high | Single-hue sequential ramp, light to dark; light = low on a light background |
| Above or below a midpoint | Diverging ramp with a neutral midpoint at the true centre (zero, target, average) |
| Status | Do not rely on red and green; add icons or text; use blue and orange or lightness differences |
| Colour-blind safe | Pick ramps flagged colour-blind safe in ColorBrewer; the Okabe-Ito set for categories; test in a simulator; vary lightness too |
| Print or grayscale | Check the chart in grayscale; use lightness steps and direct labels |
| Dark mode | Re-pick the palette; do not just invert; keep 3:1 against the background for marks |

## 3. Contrast arithmetic (WCAG 2.2)
Contrast ratio = (L1 + 0.05) / (L2 + 0.05), with L the relative luminance of the lighter and darker colour. Requirements: text 4.5:1 (large text 3:1), graphical objects and UI component states 3:1, colour not the only means to convey information. Computed examples on white: #9CA3AF 2.54:1 (fails text), #6B7280 4.83:1, #767676 4.54:1, #595959 7.00:1, #0072B2 5.19:1, #2E9E4F 3.43:1 (passes for marks, not for small text), #E69F00 2.25:1 (fails for small text and thin marks). Green #2E9E4F against red #D64545 is 1.28:1: the two differ almost only in hue, which is exactly what red-green colour-blind readers cannot use.

## 4. Pre-attentive attributes
Position, length, colour (hue and saturation), size, orientation, enclosure, and added marks are processed quickly **[M]**. Use one dominant attribute for the point; stack a second one only for hierarchy. Limit simultaneous emphases; every highlight takes attention away from the rest. Use size to order importance of text (title, key number, notes).

## 5. Text on charts
Takeaway title; subtitle with measure, unit and period; direct labels; short annotation on the 1-3 points that matter; source and date; no jargon the reader does not use. Numbers: thousands separators and decimals matching the reader's locale, consistent units, rounded to the precision the decision needs.

## 6. Tool choice (examples; check current docs and prices)
| Situation | Candidate | Why | Watch |
|---|---|---|---|
| Small team, Google data (Sheets, GA, ads), free, shareable | Looker Studio | Quick connectors and sharing | Limited modelling; blends and refresh limits; check data freshness settings |
| Product team with a SQL database, wants embedded or internal dashboards, self-serve questions | Metabase | SQL or no-code questions, dashboards, filters, embedding | Governance and semantic layer need care; scale by pre-aggregating |
| Engineering-led, many SQL sources, open source | Superset | Many chart types, SQL lab, semantic layer, no licence fee | Admin, security and upgrades are yours |
| Microsoft estate, finance and enterprise reporting | Power BI | Data modelling, Excel and Teams integration | Model design (star schema) drives speed; licensing tiers |
| Deep visual exploration by analysts | Tableau | Strong interactive exploration | Cost; keep dashboards to few views for clarity |
| Charts inside a product or a repeatable report | Vega-Lite, Plotly, Recharts | Version control, tests, tokens, accessibility control | You own accessibility, performance and data access |
Decide with: who builds and maintains; where the data lives; row-level security; embedding; budget; skills; export needs. Moving tools later is costly if the logic lives inside the BI tool: keep metric logic in the warehouse or a shared semantic layer.

## 7. Code notes
Vega-Lite: declarative JSON, marks plus encodings, good for repeatable specs and small multiples (facet or repeat). Plotly: interactive, strong in Python and JS notebooks and apps. Recharts: React components; compose axes, tooltips and legends; set accessible labels yourself. In all three: set explicit scales, zero baseline for bars, tokens for colours, text alternative, and test at phone width.
