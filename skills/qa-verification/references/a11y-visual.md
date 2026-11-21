# Accessibility and visual checks

Format: **rule** · why · source id (ids in `BIBLIOGRAPHY.md`).

## 1. Automated accessibility (axe-core)

1. **Pick tags explicitly and include both levels:** `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. `best-practice` tags are not WCAG criteria. · Q16
2. **WCAG 2.2 rules such as target size are disabled by default** until enabled explicitly. · Q16
3. **Read `incomplete` as "needs human review", never as green.** Results come as violations, passes, inapplicable, incomplete. · Q16
4. **Where to run:** component tests (jsdom) for names, roles and structure; a real browser for contrast and anything layout-dependent. · Q16
5. **Automation finds a lot of what is frequent, not most of what matters.** Deque's own data says about 57% of issues by volume (contrast alone is a large share); older "20 to 30%" figures count criteria, not issues. It is vendor data. · Q17

## 2. Manual checks (zero axe violations is not conformance)

On one critical flow per delivery, not the whole site:
- Keyboard: everything reachable with Tab in a logical order, no trap, Esc closes dialogs (WCAG 2.1.1, 2.4.3).
- Focus visible and not hidden by sticky headers or banners (2.4.7, 2.4.11).
- Accessible name makes sense and contains the visible label (4.1.2, 2.5.3).
- Alt text actually describes (1.1.1).
- 320 CSS px wide without horizontal scroll; 200% zoom (1.4.10, 1.4.4).
- Form errors in text, next to the field (3.3.1, 3.3.3).
- Status messages announced (4.1.3); page and passage language set (3.1.1, 3.1.2).
- Motion respects `prefers-reduced-motion`; nothing auto-plays sound.

New A/AA criteria in WCAG 2.2 that catch most: 2.4.11 focus not obscured (AA), 2.5.7 dragging alternative (AA), 2.5.8 target size at least 24×24 CSS px (AA), 3.2.6 consistent help (A), 3.3.7 redundant entry (A), 3.3.8 accessible authentication without cognitive tests, allow paste and password managers (AA); 4.1.1 Parsing was removed. · Q18

A level A or AA failure on purchase, login or the product's main task blocks the delivery.

## 3. Visual checks

1. **Functional green does not prove the screen is right:** missing CSS, overlap, clipped text and wrong font pass any text assertion. A UI change needs eyes: screenshots at the project's widths (phone, tablet, desktop). · Q15
2. **Pixel comparison only in the same environment:** snapshot names include browser and platform because rendering differs by OS, fonts and headless mode; a baseline made on macOS is not valid on Linux CI. · Q15
3. **Stabilize before capture:** animations off, fonts loaded, fixed data, mask or hide what varies (dates, video, counters, via `stylePath`); small explicit tolerances (`threshold`, default 0.2; `maxDiffPixels`). · Q15
4. **`--update-snapshots` only after reviewing the diff.** Auto-updating baselines is the most common visual false green. · Q15
5. **Few baselines,** for screens that sell or break often; a large unattended visual suite becomes noise. A reviewed screenshot beats an unmaintained pixel diff. · Q15
6. **Horizontal overflow at the smallest width is a component defect;** catch it with a width test rather than by inspection.
7. **A screenshot is evidence:** record path, viewport and commit in the report.
