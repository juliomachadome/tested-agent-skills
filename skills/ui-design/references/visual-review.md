# Visual review: fidelity checks, checklist, myths

## Contents
1. Source-of-truth precedence
2. Fidelity check by computed values
3. Per-screen visual checklist
4. Review workflow and report
5. Myths and weak evidence

## 1. Source-of-truth precedence
Most faithful first: exported CSS or canvas values; the design file read through its tool or API; an exported node; an exported image; a written spec; a loose reference page. A link to a hosted design that you cannot open is not a source: ask for the export. A screen with no source is built from the specification and marked provisional, never invented as if approved. Record any divergence between the design and the data contract or API as a note, not a silent choice.

## 2. Fidelity check by computed values
Eyes miss 4 to 12 px offsets, 1 to 2 px radius differences and near-identical grays. Compare numbers.
1. List the design values per item: x, y, width, height, padding, gap, radius, font size, weight, line height, color token, border, shadow, copy.
2. Read the rendered values: `getComputedStyle(el)` for font-size, line-height, font-weight, color, background-color, padding, margin, gap, border-radius, border; `el.getBoundingClientRect()` for x, y, width, height relative to the container.
3. Tabulate expected vs measured; flag any difference above 1 px or any color not equal to the token.
4. One column per container: icons and texts of a list share an x; vertical rhythm uses the same pair of values per screen type.
5. Verify the comparator itself before blaming the code: a scoping or offset bug in a comparison script produces false findings.
6. Pixel diff is an extra signal, not the test; thresholds hide small spacing errors.
Colors: assert tokens, not hex; grep component code for raw color literals when lint does not cover the folder.

Snippet pattern (browser console or an automation script):
```js
const m = (sel) => { const e = document.querySelector(sel); const s = getComputedStyle(e); const r = e.getBoundingClientRect();
  return { x: r.x, y: r.y, w: r.width, h: r.height, fs: s.fontSize, lh: s.lineHeight, fw: s.fontWeight, c: s.color, bg: s.backgroundColor, p: s.padding, br: s.borderRadius }; };
```
Capture at 390, 820, 1440 and in each theme; record a table of expected vs measured.

## 3. Per-screen visual checklist
- [ ] In 3 seconds: where am I, what is the main action
- [ ] One prominent action (two at most); rest quieter or collapsed
- [ ] Type only from scale; body at least 16 px; none under 11 pt equivalent on mobile
- [ ] Line length 45 to 75; line height by size
- [ ] Spacing only from the 4 scale; side margin consistent; groups unambiguous
- [ ] Alignment edges consistent
- [ ] Contrast 4.5:1 text, 3:1 large text and components, in every theme; color never alone
- [ ] Targets 44 px (48 where needed), never below 24; focus visible and unobscured
- [ ] Icons labeled except universal ones; one icon set, fixed stroke
- [ ] States: loading, empty, error, offline, success, pressed, disabled
- [ ] 320 px with no horizontal scroll; 200 percent zoom works; longest real string fits
- [ ] Safe areas respected; fixed bars do not cover content or focus
- [ ] Motion short, transform and opacity, reduced-motion path
- [ ] Dark and high-contrast variants checked
- [ ] Raw color literals and off-scale values absent from code
- [ ] One decorative item removed that did not serve the goal

## 4. Review workflow and report
1. Collect the source and the rendered screen at the three widths and themes.
2. Run the checklist; measure, do not guess.
3. Order findings by user impact (readability and function first, polish last).
4. Report with the format in SKILL.md; include a measured-vs-expected table and an explicit "not verified" list.
5. Fix in a batch by cause, re-measure only what changed.

## 5. Myths and weak evidence
| Claim | Status | Do instead |
|---|---|---|
| Lists and menus must have at most 7 items (Miller) | Myth | Group; the limit concerns memory, not what is on screen |
| Everything within 3 clicks | Myth | Count doubts, not clicks |
| The thumb zone forbids the top of the screen | Weak | Primary actions low, avoid corners, center is most precise |
| Hick's law says always cut options | Weak | Remove the unnecessary, organize the necessary |
| A button of color X converts better | Myth | Contrast with surroundings and a clear label |
| Users do not scroll | Myth | They scroll but attention drops below the fold; put essentials first |
| Icons are universal, labels unnecessary | Myth | Visible labels |
| A placeholder can serve as the label | Myth | Persistent label above the field |
| Very negative tracking on headings is the Apple standard | Myth | Apple's tracking table is mild; it is a brand choice |
| Desktop needs bigger text than mobile | Myth on Apple platforms | macOS is denser (Body 13, Title 1 22) |
| APCA replaces WCAG contrast | Myth | WCAG 3 is a draft with the algorithm undetermined; pass WCAG 2.2 ratios |
| Dark mode is inverted light mode | Myth | Separate mapping, contrast re-verified |
| Pixel diff proves fidelity | Weak | Compare computed values |

## Sources
- W3C WCAG 3.0 Working Draft, https://www.w3.org/TR/WCAG3/, read 2026-11-14
- W3C WCAG 2.2, https://www.w3.org/TR/WCAG22/, read 2026-11-14
- Apple HIG Typography and Accessibility, https://developer.apple.com/design/human-interface-guidelines/ (read 2026-11-14 for Accessibility; Typography prior reading)
- MDN getComputedStyle and getBoundingClientRect, https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle (not re-fetched)
- NN/g and Laws of UX, https://lawsofux.com/ (myth statuses from prior knowledge base, not re-verified)
