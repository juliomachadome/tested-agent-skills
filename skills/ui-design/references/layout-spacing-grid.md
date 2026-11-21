# Layout, spacing, grid, hierarchy, density

## Contents
1. Space scale
2. Grouping and rhythm
3. Grids, breakpoints, width classes
4. Visual hierarchy
5. Navigation placement by size
6. Data tables and dashboards
7. "Looks amateur / cluttered" diagnosis

## 1. Space scale
- Base 4 px with steps: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96. Neighboring steps differ by roughly 25 percent or more so a change is visible. Material works on an 8 dp grid with 4 dp for fine adjustment of icons and text (m3.material.io, not re-verified). Apple publishes no grid, but its values (16 margins, 44 targets, 12 and 24 padding) fit a 4 base.
- Padding around controls: about 12 pt around controls with a bezel and about 24 pt around bezel-less controls (Apple HIG Accessibility, read 2026-11-14).
- Start with generous space and remove; tightening is easier than airing out.
- Do not invent off-scale values (13, 15, 22). A lint or review rule that rejects them pays for itself.

## 2. Grouping and rhythm
- Space inside a group is smaller than space between groups, with no ambiguity (proximity). Group with space, a background surface or a divider, in that order of preference; fewer borders.
- Keep one vertical rhythm per screen type (for example 24 between sections, 8 between label and field) and repeat it.
- Align to a few vertical edges: icons and text of a list on the same x per container. Misalignment of 4 to 12 px is invisible by eye and obvious to a measurement.
- Cap content width: a form designed for 600 px does not become 1200 px on desktop; cap reading measure (see typography.md).

## 3. Grids, breakpoints, width classes
- Window size classes by width in dp: compact below 600, medium 600 to 839, expanded 840 to 1199, large 1200 to 1599, extra-large 1600 and above. Compact, medium and expanded are the Material 3 classes; large and extra-large were added for desktop displays. Classes describe the window, not the device, and change at runtime (rotation, split screen, resizing), so never branch on "is tablet". If a compact layout exists, optimize expanded first, then decide whether medium needs its own layout. (Android developers, window size classes, read 2026-11-15)
- Adapt by width class, never by fixed device or aspect ratio. Common web test widths: 320 (reflow floor, WCAG 1.4.10), 390 (phone), 820 (tablet portrait), 1180 to 1280 (tablet landscape or small laptop), 1440 (desktop). (WCAG, read 2026-11-14)
- Typical columns: 4 on compact, 8 on medium, 12 on expanded, with margins 16 on phones growing with width. Gutters 16 to 24.
- Prefer content-driven breakpoints (where the layout breaks) over device lists; use container queries for components that live in several widths.
- Layouts adapt to rotation, window width, text size and language; scale artwork proportionally rather than changing its ratio (Apple HIG Layout, prior reading).

## 4. Visual hierarchy
- Levers: size, weight, tone, position, space, contrast. Use few. NN/g suggests at most three sizes and no more than two large items on a page, about four colors in the palette, bright warm colors reserved for warnings or errors, containers used sparingly, and a squint or blur test to reveal accidental emphasis (NN/g, Visual Hierarchy, 2021, read 2026-11-15).
- Importance order: most important at top and at the leading edge; scanning follows alignment.
- To emphasize, de-emphasize the competition. One prominent button per view, two at most; secondary as outline or low-contrast; tertiary as link. (Apple HIG Buttons, prior reading; Refactoring UI)
- Button hierarchy follows task importance, not semantics: a destructive action that is not primary does not need to be big and red; a destructive action is never the primary style because people tap the primary without reading.
- Progressive disclosure: show the essentials, put the rest one tap away.
- Limit simultaneous emphasis levels per card to three. Remove labels that the value makes redundant ("12 in stock" instead of "Stock: 12").
- Reduce decoration: each border, shadow and icon must carry information.

## 5. Navigation placement by size
Bottom tab bar (3 to 5 destinations) on compact phones; navigation rail on medium; permanent sidebar on expanded. Tabs navigate sections, never trigger actions; every tab has an icon and a one-word label. See platforms-hig-material.md for the comparison.

## 6. Data tables and dashboards
- Density is a user setting, not an accident: offer compact and comfortable row heights (for example 32 / 40 / 48 px) with the same type roles.
- Table anatomy: left-align text, right-align numbers (tabular figures), header row visually distinct, sticky header on long tables, zebra or hairline rows (not both), one primary column that identifies the row.
- Sorting and filtering state visible; empty, loading (skeleton rows) and error states; pagination or virtualization with a cap, never an unbounded list (see `web-performance`).
- On narrow screens do not shrink a table: reflow rows to cards or provide a horizontally scrollable region with a frozen identifying column, and keep it keyboard reachable.
- Dashboards: lead with the question the person came with (one to three key figures), group related metrics, give every number a unit, a time range and a comparison; avoid decorative gauges. Chart color rules in color-contrast.md; direct labels over legends when possible.
- Row actions: visible on hover and on keyboard focus, never hover-only; on touch, expose them in a menu or swipe with an on-screen alternative.

## 7. "Looks amateur / cluttered" diagnosis
Run in this order; each step is measurable.
1. Count distinct font sizes, colors and radii on the screen. More than about 6 sizes, 3 grays of text, or 3 radii is a smell.
2. Count prominent items. More than two filled buttons, or more than one saturated accent region, flattens hierarchy.
3. Measure spacing values; anything off the 4 scale, or equal spacing inside and between groups, is the cause of "messy".
4. Check alignment edges; list x positions.
5. Check contrast of secondary text; muddy gray is the usual cause of "cheap".
6. Count borders and shadows; replace most with space or a surface tint.
7. Check content width and line length.
8. Check states: an empty table or blank panel looks unfinished.
Fix in that order, re-measure, stop when the checklist passes; do not add decoration to compensate.

## Sources
- Android developers, Use window size classes, https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes, read 2026-11-15
- NN/g, Visual Hierarchy, https://www.nngroup.com/articles/visual-hierarchy-ux-definition/, read 2026-11-15
- NN/g, Principles of Visual Design, https://www.nngroup.com/articles/principles-visual-design/, read 2026-11-15
- Baymard, checkout form fields, https://baymard.com/blog/checkout-flow-average-form-fields, read 2026-11-15 (average 11.3 fields, about 8 needed; field count affects usability more than step count)
- Apple HIG Accessibility (control padding), https://developer.apple.com/design/human-interface-guidelines/accessibility, read 2026-11-14
- Apple HIG Layout and Buttons, https://developer.apple.com/design/human-interface-guidelines/layout (prior reading 2026-11-12, not re-fetched)
- W3C WCAG 2.2 Reflow 1.4.10, https://www.w3.org/TR/WCAG22/, read 2026-11-14
- Material Design 3 foundations, https://m3.material.io/foundations/layout/understanding-layout/overview (not re-verified)
- Wathan and Schoger, Refactoring UI (2018), book (not re-verified)
