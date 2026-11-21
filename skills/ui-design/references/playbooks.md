# Playbooks: routines for ui-design

Evidence tags: **[C]** standard or platform guideline, **[M]** single serious source, **[F]** practitioner default. Project tokens and DESIGN.md override every default below.

## 1. Build or extend a token set
1. Inventory what exists: grep for raw hex, px values, font stacks. Reuse names already in use.
2. Three layers: primitive (`blue.600`), semantic (`color.action.primary`), component (`button.primary.bg`). Components read semantics only. Name by role, not by look (`text.muted`, not `grey-600`) [F]. Format: DTCG JSON with `$value` and `$type`, aliases in curly braces [C, DTCG 2025.10].
3. Roles to cover:
| Group | Minimum set |
|---|---|
| Colour | neutral ramp (about 10 steps), surface 0/1/2, text primary/secondary/disabled, border subtle/strong, action (default, hover, pressed, on-action), focus ring, status success/warning/danger/info with an on-colour each |
| Type | 6 to 8 roles (caption, body, body-strong, subtitle, title, headline, display) with size, line height, weight, tracking |
| Space | 4, 8, 12, 16, 24, 32, 48, 64 |
| Radius | 2 or 3 values plus full (pill) |
| Elevation | 3 levels: flat, raised, overlay (shadow or surface tint, or a border in styles that ban shadows) |
| Motion | duration fast 100 to 150, base 200 to 250, slow 300 to 400 ms; easing out, in-out; a reduced-motion variant |
4. Dark theme: a second mapping of semantics, not an inversion. Status colours keep one meaning in every theme and a brand theme must not override them.
5. Check every text and boundary pair per theme with a computed matrix (ratio, pass or fail). Fail the build on raw hex in components.
6. Report what was assumed and what stayed unchanged.

## 2. Screen design routine
1. Content first: list the real content, longest strings, the one job of the screen and its primary action.
2. Hierarchy in grayscale: place one focal element, rank the rest; use size, weight, tone, space.
3. Layout grid: 4-based spacing, 4 columns on compact, 8 on medium, 12 on expanded; cap reading width at about 65ch; respect safe areas.
4. Components from the system; a new one only if no existing one covers the role.
5. Add colour last: action colour on the primary only, status colour for status only.
6. States: empty (say what and how to start), loading (skeleton or progress that matches the final shape, with a "where later" cue for long waits), error (what happened, what to do, keep the user's input), success (confirm and the next step), plus offline, disabled, hover, focus, pressed.
7. Test with real data: longest name, zero items, 1,000 items, other language.

## 3. Visual QA checklist (3 widths, project themes)
Run at 390, 820 and 1440 CSS px in each theme the project has (dark only if the project has it or the request says); if unclear, ask, never assume. Then once at 320 and at 200% zoom.
- Nothing clipped, overlapped or under a system bar; no horizontal scroll at 320 [C].
- Computed font sizes, heights and gaps are on the token scales (collect by script, list the exceptions).
- One primary action visible without scroll where the task needs it.
- Contrast pairs recomputed in every theme checked, including disabled and placeholder text (disabled text is exempt, but must stay legible enough to read) and text over images.
- Icons aligned to the text baseline and to one stroke weight; images do not pop white in dark mode.
- Hover, focus, pressed, disabled states exist; focus visible on every control.
- Tables and long text: wrapping, truncation with access to the full value, numerals aligned.
- Report: findings ordered by user impact, measured vs expected, and an explicit not-verified list.

## 4. Accessibility pass (WCAG 2.2 AA, visual layer)
| Check | Criterion | Test |
|---|---|---|
| Text contrast 4.5:1, large 3:1 | 1.4.3 | compute per pair |
| Boundaries and meaningful icons 3:1 | 1.4.11 | inputs, checkboxes, chart marks |
| Colour not the only signal | 1.4.1 | greyscale screenshot |
| Resize to 200% without loss | 1.4.4 | zoom, long strings |
| Reflow at 320 px | 1.4.10 | narrow viewport |
| Text spacing override survives | 1.4.12 | apply 1.5 / 2x / 0.12em / 0.16em |
| Focus visible; not hidden by sticky bars | 2.4.7, 2.4.11 | tab through; check headers and cookie bars |
| Target size at least 24 x 24 CSS px, or spacing | 2.5.8 | `getBoundingClientRect`; default design 44 or 48 |
| Reduced motion honoured | 2.3.3 (AAA), platform setting | `prefers-reduced-motion` emulation |
Automated tools catch only part of this [M]; say so, and do a manual keyboard pass. Semantics and ARIA belong to `ux-design`.

## 5. Design review agenda (30 minutes)
1. 3 min: goal, platform, theme, source of truth, what is provisional.
2. 5 min: squint test and focal order; one primary action.
3. 7 min: tokens: type, space, colour, radius used from scales; list exceptions.
4. 5 min: contrast and target table.
5. 5 min: states and edge data (empty, longest string, error).
6. 3 min: style fit: does it match the project's system (`styles/README.md`)?
7. 2 min: decisions, owners, fix order: blockers, then fix-before-code, then polish. Taste goes in a separate list from defects.

## 6. Handing off to code
- Export tokens as CSS custom properties on `:root`, dark overrides under `[data-theme="dark"]` and `@media (prefers-color-scheme: dark)`; or as a theme file (JSON, TS object, Tailwind theme, native resources) generated from the one DTCG source so values do not fork.
- Sample:
```
:root{--color-text:#1a1a1a;--color-surface:#fff;--space-4:16px;--radius-m:8px;--dur-base:200ms}
@media (prefers-reduced-motion:reduce){:root{--dur-base:0.01ms}}
```
- Give the developer: token file, a state matrix per component, spacing in tokens not px, min and max widths, the longest string used, and the contrast table. Say which values are provisional.
- Acceptance: computed styles match the tokens; screenshots at 390, 820, 1440 in both themes attached; lint blocks raw hex.
