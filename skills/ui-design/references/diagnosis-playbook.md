# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a fix built on the wrong tokens, platform or device assumptions is wasted. Thresholds are **[C]** consensus or standard (WCAG, platform guidelines), **[M]** serious but single source, **[F]** practitioner starting point, **[X]** myth. The project's own tokens and DESIGN.md replace every [F] value. Ideas are paraphrased from the sources in `BIBLIOGRAPHY.md`.

## Step 0: what do we actually have?
| Check | How | If it fails |
|---|---|---|
| Project tokens or DESIGN.md | search for `DESIGN.md`, `tokens.json`, `theme.*`, `globals.css`, a Figma variables export, a components folder | none found: say so, mark every value provisional, build the minimum set (`playbooks.md` 1) |
| Platform | iOS, Android, web, installed PWA, desktop; which guideline family applies | undecided: ask; do not mix Apple and Material idioms on one screen |
| Brand | logo colours, brand fonts, tone; which parts are fixed | no brand: neutral ramp plus one action colour; flag as a decision for the owner |
| Target devices and widths | real device list or analytics; smallest supported width | unknown: assume 320 (floor), 390, 820, 1440 |
| Accessibility level | WCAG 2.2 AA is the default floor [C]; contractual or legal level? AAA parts wanted? | unknown: AA |
| Evidence | screenshots at 390, 820 and 1440 in each theme the project has (dark only if the project has it or the request says), or the live URL; computed styles beat a screenshot | image only: layout is judged, values are not; say "values not verified" |
| Style | the project's existing look, else the request (`styles/README.md`) | a project design system exists: never override it |

## Worked numbers (reuse in every branch)
- **Contrast ratio** = (L1 + 0.05) / (L2 + 0.05), L1 the lighter. Relative luminance L = 0.2126 R + 0.7152 G + 0.0722 B, where each sRGB channel c (0..1) becomes c/12.92 if c <= 0.03928, else ((c + 0.055)/1.055)^2.4 [C, WCAG definition]. Example: #767676 gives L = 0.1812; white L = 1.0; ratio = 1.05 / 0.2312 = 4.54, passes 4.5:1 by a hair. #999999 gives L = 0.3185, ratio 1.05 / 0.3685 = 2.85, fails. Thresholds: 4.5:1 normal text, 3:1 large text (18 pt or 14 pt bold) and meaningful UI parts [C]. Never round up: 4.49 fails.
- **Type scale (modular)**: size_n = base x ratio^n. Base 16, ratio 1.25 (major third): 12.8, 16, 20, 25, 31.2, 39.1, 48.8. Ratio 1.333 grows too fast for dense UI (16, 21.3, 28.4, 37.9). Round to whole px or to the platform's named roles; 6 to 8 roles are enough [F].
- **Spacing scale**: base 4, steps 4, 8, 12, 16, 24, 32, 48, 64 [F]; 8-only is coarser and cannot make 12 or 4 gaps. Inside a group the gap is smaller than between groups (proximity). A mixed 13/15/22 set snaps to 12/16/24.
- **Line length** 45 to 75 characters including spaces is the common band; a long single column up to about 90 is tolerated [F, with Butterick's 45-90 as a looser range]. At 16 px a Latin body face averages about 0.5 em per character, so 66 characters is about 530 px: cap at roughly 33 to 38 em, in CSS `max-width: 65ch`. Check by measurement, since faces differ.
- **Line height**: body about 1.4 to 1.5, large headings 1.1 to 1.2; WCAG 1.4.12 requires that content survives line height 1.5, paragraph spacing 2x, letter spacing 0.12 em, word spacing 0.16 em with no loss [C].

## 1. The screen looks cluttered
| Likely cause | Check | Fix |
|---|---|---|
| Many things at the same weight, nothing leads | squint test (blur the screenshot); count items at full emphasis | one focal element per view; quiet the rest by tone and weight, not by removing |
| Too many sizes, weights, colours | list distinct font sizes and weights, text colours (DevTools or `getComputedStyle`) | max about 3 sizes and 2 weights per view, 2 or 3 text tones [F] |
| Spacing by eye | collect all padding and margin values; off-scale ones are the finding | snap to the scale; groups tighter inside than between |
| Borders on every row and card | count 1 px lines | replace with space or a surface tint; keep a border only where a boundary needs 3:1 |
| Competing buttons | count filled buttons per view | one primary, others secondary or text |
Verify: re-run the squint test and the value collection; report before and after counts.

## 2. It looks generic or "AI-made"
Likely cause: no decision made. Check for: system default fonts only, purple or blue gradient, identical rounded cards with soft shadow, gradient headline text, decorative glass or blobs, emoji or icon in every card heading. Fix: write one sentence of point of view (who, tone, one memorable element); pick one typeface pairing or one expressive weight; limit colour to one accent from the product's own content; boldness in one place and discipline elsewhere. If a project design system exists, restraint inside it is the answer, not a new style. Open `anti-patterns-polish.md` and `styles/README.md`.

## 3. Text is hard to read
| Likely cause | Check | Fix |
|---|---|---|
| Contrast | compute the ratio for every text and background pair, including text on images and tinted banners | darken text or lighten background until 4.5:1 (3:1 large); derive text colour from the surface hue |
| Size | body under 16 px on web, under 17 pt on iOS default, captions under 11 pt (Apple minimum) [C] | raise; check 200% zoom and Dynamic Type |
| Line length | characters per line (measure) | cap at 65ch; wider screens get margins or columns, not longer lines |
| Line height and weight | leading under 1.3 for body; thin weights on dark | 1.4 to 1.5; raise weight a step |
| Colour on colour or text over photo | sample the worst background pixel | solid scrim or surface behind text; see `styles/glass-translucent.md` |

## 4. Buttons are not noticed or are mis-tapped
Affordance: does it look pressable (fill, border or underline plus label)? NN/g notes flat design strips signifiers; add a fill, border, or at least an underline [M]. Size: Apple 44 x 44 pt default hit region, Material 48 dp, WCAG 2.2 AA floor 24 x 24 CSS px with spacing exceptions [C]. Spacing: two small targets closer than 8 px invite mis-taps [F]. Check by measuring `getBoundingClientRect` for the hit area, not the glyph. Fix: enlarge the hit area with padding (the visual can stay small), separate destructive from primary, give a pressed state, one primary per view.

## 5. Screens are inconsistent
Likely: no tokens, tokens exist but raw values used, components copied and edited. Check: grep for raw hex, off-scale px, `!important`; list the distinct button heights and radii across screens. Fix: introduce tokens in three layers (`tokens-theming.md`), replace raw values, one component per role, add a lint rule against raw hex. Contradicting data across screens (counts, dates) is a data bug, not a style bug (`review-lessons.md`).

## 6. Dark mode is broken
Likely: inversion instead of a second mapping; pure #000 with pure white text vibrating; shadows invisible; brand colours too saturated; images and logos with white boxes. Check: contrast matrix in both themes, elevation still readable, status colours still distinct and not colour-only. Fix: separate semantic mapping, slightly lighter surfaces for higher elevation, desaturate accents, off-white text (about 87 percent tone) [F], supply dark logo variants, honour the system setting; Apple advises against an app-specific appearance switch [C]. Open `color-contrast.md`.

## 7. The layout breaks on small or large screens
Check at 320, 390, 820, 1440, 200% zoom, longest real string. Small: fixed widths, no wrapping, horizontal scroll (WCAG 1.4.10 reflow at 320 CSS px [C]), text under bars. Large: stretched forms, lines of 150 characters, tiny content in a huge canvas. Fix: fluid widths with max-width, a content cap, breakpoints by window class (compact under 600, medium 600 to 839, expanded 840+), safe-area padding. Open `layout-spacing-grid.md`.

## 8. The dashboard or table is unreadable
See `data-tables-dashboards.md`. Quick causes: no hierarchy among KPIs, numbers not right-aligned or not tabular, ink spent on gridlines and decoration (Tufte's data-ink idea [M]), chart colours that fail 3:1 or rely on hue only, no units or time range. Fix: lead with the question, align numerals, remove chart junk, label directly, density chosen on purpose (`styles/data-dense.md`).

## 9. Brand colours fail contrast
Compute for each pairing, as text on white, white on colour, and colour as a boundary on its surface. Worked case: orange #FF6B35 on white is 2.84 (fails text and 3:1 UI is close); black on it is 7.41. Options in order: keep brand colour as a fill with dark text; darken a text and link variant (#C2410C on white is 5.18); use the brand colour only as decoration with a text-safe sibling token. Logos are exempt from 1.4.3 and 1.4.11, decoration is exempt, but a brand-coloured button label is not. Never ship an off-brand fix without saying which role changed.

## 10. Motion is annoying or inaccessible
Check: does anything move without an action, loop, parallax, or auto-play; durations over 400 ms on routine UI [F]; is `prefers-reduced-motion` honoured; does motion carry meaning alone? WCAG 2.3.3 (AAA) asks that interaction-triggered motion can be disabled, and Apple asks apps to respond to Reduce Motion [C]. Fix: animate transform and opacity, 150 to 300 ms with ease-out for entering [F], replace large movement with a fade under reduced motion, never loop decoratively, pair motion with a non-motion cue. Open `motion.md`.

## What cannot be checked from here
Real device rendering, user preference settings, and brand intent are not visible in a screenshot. State them as not verified in the report.
