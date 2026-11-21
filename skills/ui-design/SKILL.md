---
name: ui-design
description: "Use for the visual side of screens and design systems, including quick numeric questions such as \"compute the contrast ratio of #767676 on white, does it pass AA\", \"4px or 8px spacing scale\", \"type scale with body size, line height and line length for dense data tables\", dark mode and status colors (is inverting ok, red/green), grids, visual hierarchy (\"my settings screen looks amateur, too many things fight for attention\"), choosing or applying a visual style (Apple HIG, Material 3, Fluent, neo-brutalism, Swiss, editorial, minimalist, glass, Liquid Glass, retro, data-dense, playful), design tokens (DTCG), motion, touch targets, dashboards, brand colors that fail contrast, matching a mockup by computed CSS values. Not for flows, forms, heuristics or ARIA semantics (ux-design), load speed (web-performance) or bold free-form aesthetic direction (frontend-design)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# UI design

Make a screen look deliberate, readable and consistent, and prove it with numbers, not taste. "Amateur" screens usually fail on few measurable things: competing emphasis, spacing by eye, too many type sizes, low contrast, color used for decoration and meaning at once. Fix them with a system, not decoration.

Evidence tags: **[C]** standard or platform guideline (WCAG, HIG, M3), **[M]** serious single source, **[F]** practitioner default, **[X]** myth. Project values replace every [F].

Boundaries:
- Flows, heuristics, forms, state logic, ARIA and accessibility beyond the visual layer: `ux-design`.
- Speed, Core Web Vitals, bundle weight: `web-performance`.
- Free aesthetic direction and a distinctive look: `frontend-design`; this skill supplies the measurable craft under it.
- How motion and interface sound are built (tool choice, scroll and landing animation, explainers, feedback in motion, three.js, Lottie): `web-motion`; durations and easing stay in `references/motion.md`.

## Step 0: the project first
Before any advice, read the current project: DESIGN.md, token files, the component library, ADRs, CLAUDE.md or AGENTS.md, and shipped screens. **Project rules win.** If a design system exists, work inside it and propose changes as a delta for the owner. Then fix platform, brand, devices, accessibility level (default WCAG 2.2 AA) and evidence (screenshots at 390, 820, 1440, light and dark).

## Match the visual structure to the task [F]

Use the task and states identified by `ux-design` to decide what needs emphasis and what can stay quiet. Preserve helpful structure, labels, locale and density in a targeted fix. Use an existing pattern when it already serves the task.

Choose the starting layout from the primary use case. Start narrow when quick phone actions matter most; start wide when the main job is dense comparison or simultaneous panes. For responsive web, check where the content stops fitting across phone, tablet, split view and desktop; adapt density or pane count there. A tablet can be narrow in split view and may use touch, a pointer or a keyboard. For native apps, use the target platform's components, safe areas and text scaling. If the product ships on both, carry over priorities and states while adapting the controls and layouts to each platform.

| What people need to do | Visual default |
|---|---|
| Scan repeated items | Compact rows with alignment and light separators. Keep the name, state and next useful action in predictable places. |
| Compare several values across items | Table with consistent columns and aligned numbers. On narrow screens keep essential values comparable, using fewer columns plus details, a compact list, or a labelled scroll area for a genuinely wide table. |
| Browse independent items or visual choices | Cards can help when each item needs a distinct preview, summary or action. Group shared controls once. |
| Complete a form or recover from an error | Group related fields by task. Place actionable error text by its field and keep the focus state distinct. Add a summary when it helps users find multiple errors. |

Remove boilerplate subtitles, repeated badges, nested panels and decoration whose absence would not change a decision or action. Start with alignment, type and spacing; add borders, fills or elevation only where they clarify grouping or interaction.

## Principles
1. **System before screen.** Scales for type, space, color, radius, elevation and motion are decided once as tokens; screens only pick from them.
2. **Hierarchy comes from few levers.** Size, weight, tone, position, space. Two or three text tones, two or three weights. To emphasize one thing, quiet its competitors.
3. **Semantic color is information; brand color is decoration.** Status colors keep one meaning in every theme and style; color is never the only signal (WCAG 1.4.1).
4. **Measure, do not eyeball.** Compute contrast, read computed styles, compare with the source by value.
5. **The primary style belongs to the action that advances the task.** Cancel, discard and delete are secondary and confirm with the consequence stated.
6. **Respect the platform.** Do not mix Apple and Material idioms on one screen.
7. **Text must survive.** 200% zoom, 320 px, the longest real string, reduced motion.
8. **Do not invent when a source exists.** A screen built without one is labeled provisional.
9. **One dataset.** Names, counts and dates on different screens come from the same source.

## Choose the style
1. A project design system or existing UI exists: its look is the style. Stop; do not override it.
2. Otherwise the platform: iOS gets `hig-apple`, Android `material-3`, Microsoft or enterprise productivity `fluent-2`.
3. Otherwise the request or the product's feeling and audience, using the table in `references/styles/README.md`.
4. One base style, at most one accent style in one place; say the choice in one line and mark tokens provisional. The accessibility floor is the same for every style; a style is taste, not a defect fix.

## Which reference to open
| Task | Open |
|---|---|
| Something looks wrong, cause unknown (cluttered, generic, hard to read, buttons missed, dark mode, breakpoints, dashboard, brand contrast, motion) | `references/diagnosis-playbook.md` |
| Routines: tokens, screen design, visual QA (3 widths, its themes), accessibility, review, handoff | `references/playbooks.md` |
| Which style, mixing styles, never override a system | `references/styles/README.md`, then the style file |
| A named style | `styles/<name>.md`: hig-apple, material-3, fluent-2, brutalism-neo-brutalism, swiss-international, editorial, minimalist, glass-translucent, retro-y2k, data-dense, playful |
| Type scale, line length, leading, Dynamic Type, font stacks | `references/typography.md` |
| Contrast math, 1.4.3 / 1.4.11, APCA status, semantic vs brand, dark mode | `references/color-contrast.md` |
| 4/8 space, grids, window classes, hierarchy, density | `references/layout-spacing-grid.md` |
| Token layers, DTCG JSON, naming, theming, states | `references/tokens-theming.md` |
| Apple HIG vs Material 3, target sizes, safe areas, PWA | `references/platforms-hig-material.md` |
| Durations, easing, microinteractions, reduced motion | `references/motion.md` |
| Computed-value fidelity check, per-screen checklist | `references/visual-review.md` |
| Generic look, critique and polish passes (squint test, rank by impact) | `references/anti-patterns-polish.md` |
| Anti-patterns from real reviews | `references/review-lessons.md` |
| Dense tables, filters, KPI cards | `references/data-tables-dashboards.md` |
| Sources, status V/P | `references/BIBLIOGRAPHY.md` |

## Workflow
1. **Find the source of truth.** Most faithful first: exported CSS or canvas values, design file via API, exported image, written spec. Image-only gives layout, not values; say so.
2. **Gather constraints.** Platforms, themes (light, dark, high contrast), languages and longest strings, density, brand color, inputs.
3. **Set or reuse tokens.** If none, create the minimum: neutral ramp, one action color, four status colors, 4-based spacing, 6 to 8 type roles, 2 to 3 radii, 3 shadows, 3 durations (`playbooks.md` 1).
4. **Build in grayscale first**; add color last.
4b. **Before building, scan `references/anti-patterns-polish.md` 1-1b. No brand given**: light neutral theme, one saturated action colour; dark or stylised on request. The primary action is the strongest element (filled, white label 4.5:1+, never a pale tint). No demo toggles in the delivered screen **[F]**.
5. **Specify states, do not defer them.** For every component you change, write the values: default, hover, focus-visible (2 px ring), pressed, disabled (Save disabled until the form changes), loading, error; and a non-colour cue for any status colour (icon on a banner). Screens: empty, loading, error, offline, success.
6. **Verify with numbers.** Contrast for every text and boundary pair in every theme; computed styles against the source; 320, 390, 820, 1440 px, 200% zoom, reduced motion.
7. **Report** in the output format below.

## Quick rules [C unless marked]
- Body at least 16 px on web (Apple default 17 pt, minimum 11 pt); form fields at least 16 px so mobile Safari does not zoom [F].
- Line length 45 to 75 characters; line height about 1.5 body, 1.1 to 1.2 large headings [F].
- Contrast: 4.5:1 normal text; 3:1 large text (18 pt, or 14 pt bold), component boundaries and meaningful icons. Compute, never round up.
- Targets: 44 pt (Apple) or 48 dp (Material) by default; WCAG 2.2 AA floor 24 CSS px with exceptions.
- Space on a 4 px base; spacing inside a group smaller than between groups [F].
- One prominent button per view; verbs in labels; icons without labels only when universal.
- Animate transform and opacity, briefly, in response to an action; honor reduced motion.
- Dark mode is a separate mapping, not an inversion; recheck contrast.
- Translucent surfaces (glass, Liquid Glass) hold text only on opaque or heavily blurred areas; Apple keeps Liquid Glass in the navigation layer, not in content.

## Checklist before finishing
- [ ] Project system and tokens read first; nothing overrides them
- [ ] Every value is a token; no raw hex or off-scale pixel in component code
- [ ] Contrast computed for text and non-text pairs in each theme
- [ ] Type uses only scale roles; measure and leading in range
- [ ] One clear primary action; dangerous actions are not primary
- [ ] Spacing from the scale; grouping unambiguous
- [ ] Repeated data still scans and compares at narrow widths; any larger surface earns the space it uses
- [ ] Targets met; focus visible and not obscured
- [ ] States designed, including waits with progress
- [ ] 320 px, 200% zoom, longest string, reduced motion tested
- [ ] Safe areas respected; facts consistent
- [ ] Chosen style named, and its accessibility risks checked

When modifying an existing screen, compare before and after at the same viewport and state. Record whether the intended priority is easier to see and whether fewer useful rows or controls fit. Report functional pass/fail and visual quality separately.
For responsive work, check narrow, intermediate and wide layouts and one width either side of any changed breakpoint. Include tablet portrait, landscape or split view when relevant, and test larger text or browser zoom.

## Output format for a review or restyle
```
Screen/component: <name>   Platforms/themes: <list>   Source of truth: <what was used>   Style: <chosen and why>
Verdict: <ship | fix first | rework>
Findings (blockers, then fix-before-code, then polish):
 1. <what> | evidence (measured vs expected) | rule or source tag | fix
Measured: contrast table (pair, ratio, pass/fail), spacing and type vs source
Not verified: <only what needs the live app or real data, and why; a state you can specify is specified, not listed>
```
Mark source-less screens provisional.

## Gaps
- M3 shape, elevation and 48 dp values, and Fluent 2 shapes, material and color pages were not read in the latest pass; style files mark them [F].
- APCA: only the WCAG 3 draft status was verified; no APCA thresholds are given, deliberately.
- Books are identity-verified only; ideas paraphrased, not re-read.
- Trend styles (neo-brutalism, glass, Y2K) change quickly; native SwiftUI and Compose specifics and RTL are not covered in depth.
