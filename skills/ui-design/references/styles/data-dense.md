# Style: data-dense (pro tools and dashboards)

## Principles
Expert users want information per screen, speed, and keyboard access. Density is a choice: more rows and fewer decorations, with hierarchy kept by alignment, weight and a few tones. Tufte's argument is that ink should carry data: remove non-data ink and redundant decoration, and let comparison, small multiples and direct labels do the work [M, Tufte, book]. Visual hierarchy still needs a small number of emphasised items (NN/g: few sizes, few colours) [M].

## Typical tokens
| Area | Value |
|---|---|
| Type | 12 to 14 px body (Fluent's web body is 14/20; Apple's iOS minimum is 11 pt, which is a floor not a target); tabular-lining numerals (`font-variant-numeric: tabular-nums`), right-aligned numbers; mono for IDs |
| Row height | compact 28 to 32, default 36 to 40, comfortable 48 [F]; a density switch is common |
| Colour | neutral surfaces, one accent, semantic status; chart palettes tested for 3:1 against the background and for colour-blind separation; no colour-only encoding |
| Space | 4 base: 4, 8, 12, 16; gaps inside groups 4 to 8 |
| Radius / shadow | 2 to 4 px / none, hairline separators at 1 px |
| Motion | almost none: instant sorting and filtering; loading skeletons that match rows |

## Do
- Lead with the question: 1 to 3 key figures, each with unit, time range and comparison.
- Align numerals by decimal, sticky headers and first column, zebra or hover row highlight (not both heavy).
- Offer keyboard navigation, selection, resizing, saved views; keep targets at least 24 x 24 CSS px even in compact mode (WCAG 2.5.8).
- Show empty, loading, error and partial-data states for every table and tile.

## Avoid
- Gridlines on every cell, 3D charts, decorative gradients, dual-axis charts without need, truncated bar baselines.
- Rainbow palettes; legends far from the marks (label directly).
- Equal emphasis on all KPIs.

## Accessibility risks
Small text under 12 px; compact rows with tightly packed controls; colour-coded statuses with no icon or text; sortable headers without keyboard access; charts with no text alternative or table view; contrast of thin lines (1.4.11 needs 3:1 for graphical objects that carry meaning).

## Fits / does not fit
Fits: analytics, admin, trading, DevOps, CRM, logistics, anything operated for hours daily by trained users. Does not fit: first-time consumers, onboarding, marketing pages, touch-first phones (reflow to cards or keep a horizontal-scroll table with a sticky key column and say so).

## Sources
Tufte (BIBLIOGRAPHY 4, V), NN/g Visual Hierarchy (11), Fluent 2 Typography (37), WCAG Understanding 2.5.8 and 1.4.11 (19, 18), HIG Typography (32). Detailed table and KPI rules in `../data-tables-dashboards.md`. Row heights are practitioner defaults [F].
