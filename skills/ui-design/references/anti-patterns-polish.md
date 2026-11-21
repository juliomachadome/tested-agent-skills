# Template look, critique and polish passes

Read when a screen feels generic or machine-made, when reviewing or polishing a built screen, or when choosing type and color variation. Ideas here are rules of craft, not a replacement for a brief: an explicit brief (pinned fonts, palette, era) always wins over any default below.

## Contents
1. Template-look defaults to refuse
2. Variation in type and color
3. Surfaces the browser draws for you
4. Depth and spacing details
5. Critique pass
6. Polish pass and triage order
7. Bounded verification

## 1. Template-look defaults to refuse
These recur in generated and templated UI. They are defaults, not crimes: use one only when the brief or the product's world earns it, and know why.
- Same-size cards of icon, heading and text as the page structure; nested cards (nearly always wrong).
- The most common AI-generated tells (real with/without test, 18/11/2026): dark theme with no brand reason, purple or indigo accent and purple-to-blue gradients, pale tinted primary buttons, emoji as icons, demo toggles left in the screen, every card the same rounded box with a soft shadow. With no brand given, start light and neutral with one saturated action colour.
- The hero-metric template: big number, small label, supporting stats, accent.
- A small eyebrow label above every heading; numbered section markers (01 / 02 / 03) when the sequence carries no information.
- Gradient text (use weight or size for emphasis); glass and blur as decoration rather than as a functional effect on a floating surface.
- A thick colored border on one side of cards, list items or alerts.
- Hard offset zero-blur shadows outside a style that deliberately chose them.
- Decorative sparklines, progress rings and rounded rectangles standing in for content.
- Emoji or loose glyphs as an icon system (draw icons from one library with one stroke weight); monospace as a costume for "technical" instead of for code and data.
- A modal for a task that needs neither interruption nor protected focus.
- Filler copy ("Welcome!", "Simplify your workflow"), and Title Case Everywhere.
- Test: if the screen could belong to any other product by swapping the logo, it is generic; bring in the real content, the real domain vocabulary and the owner's identity.


## 1b. Craft pass before delivering (what top-tier product shots do) [F]
For visual references, use Dribbble or editorial work to study composition, type and rhythm. Use Mobbin and shipped products to study task order and states. Inspect a working flow where possible when behavior matters. A shot can illustrate a visual choice. Verify keyboard, errors, real content and responsive behavior in your implementation. Write down the relevant choice and adapt it to the project's content, brand and users.

Apply these patterns where they fit the screen's job:
- A point of view: pick one base style from `styles/README.md` by product and audience and say which; a language app can lean `playful` (rounded, warm, one bright brand colour, a mascot or illustration moment) while money screens stay calm.
- Brand presence without decoration: a real logo mark or product image, a brand colour used for the primary action and one highlight only, warm or tinted neutrals instead of pure grey-on-white.
- Strong type scale: a clear display size for the screen goal and the price, tabular numbers for money, at most 3 weights; labels quieter than values.
- Space and grouping: 8-point rhythm, generous outer margins (16-24 px), related items grouped by space before borders; fewer boxes, not more.
- Subtle depth: one elevation level for the main card or sheet, hairline or no borders elsewhere; consistent radii (one small, one large).
- Real icons from one set (SF Symbols, Material Symbols, Lucide), never emoji; payment marks drawn correctly.
- Micro-states: selected plan with a clear check, pressed and loading states on the pay button, inline success for a promo.
- Fit: test at 320 and 390 px wide with no horizontal scroll; grid and flex children get `min-width: 0` and long prices or names wrap or truncate on purpose.
- Squint test at the end: the primary action and the price must be the first two things you see.

## 2. Variation in type and color
- Do not pick the family, accent hue or light/dark mode by category habit. Derive them from the use scene: who uses it, where, under what light, for how long. A dense tool used for hours in an office favors calm neutrals and one restrained accent; a campaign page can carry more expression.
- One or two families; if two, make them clearly different (for example a text face and a distinct display face), never two near-identical sans faces.
- Avoid the same hue and the same display treatment in every project: generate two or three palette candidates (different hue, temperature, chroma) and compare on the real screen with contrast computed, then commit to one.
- Keep expression in details (type character, one accent, spacing rhythm) while mechanics (contrast, targets, tokens) stay fixed.

## 3. Surfaces the browser draws for you
Defaults that belong to no design system are the cheapest signal that a page was assembled rather than built. Theme them from the palette:
- text selection color, caret color (`caret-color`), `accent-color` for native controls, custom scrollbars (`scrollbar-color`), focus rings, link underline offset and thickness, tabular numerals in data, form-control chrome via `color-scheme`.
- Keep them accessible: selection and focus still meet contrast.

## 4. Depth and spacing details
- Shadows have an offset and a soft blur and imitate a light source; a zero-offset colored halo is decoration. Use three elevation levels at most.
- Spacing: tight inside groups, generous between them, and more space above a heading than below it so the heading attaches to its content. Read computed values rather than judging by eye.
- Type details: balanced heading wrapping (`text-wrap: balance`), body measure 65 to 75 characters, a floor on negative tracking, display text capped to a sane maximum; run the real copy at every width and fix overflow.

## 5. Critique pass
A critique judges the built screen, not the intent.
1. State the screen's job and the primary action in one sentence.
2. Squint test: blur or shrink the screenshot; the primary action and the top two levels of hierarchy should still be identifiable.
3. Score the dimensions: hierarchy, consistency with the system, contrast and legibility, spacing rhythm, state coverage, responsive behavior, copy.
4. Each finding: what, where, evidence (measured value or screenshot region), consequence for the user, fix. Rank by user impact.
5. Separate defects (wrong) from taste (different). Report taste as an option, never as a defect.

## 6. Polish pass and triage order
Polish is refinement: preserve the incumbent look, content and behavior; if the concept itself is wrong, say so and recommend a redesign instead of smuggling one in.
Classify each drift, then fix the cause at the narrowest correct level:
- missing token (the system needs a reusable value), one-off hand-built code (replace with a shared component), conceptual mismatch (flow or hierarchy differs from comparable areas), local defect (incomplete or inconsistent).
Fix in this order:
1. broken or blocked tasks, data loss, misleading state, inaccessible paths;
2. missing loading, empty, error, success, disabled and permission states;
3. flow, hierarchy, responsive and design-system drift;
4. visual and motion inconsistencies;
5. code and asset cleanup.
Do not perfect one corner while the rest stays below the same bar.

## 7. Bounded verification
Build fully, inspect once with a batched round (all target widths and themes together), fix everything it shows in one batch, confirm with at most one more round, then stop. Open-ended self-checking burns time without raising quality. Checks that share one render (contrast, spacing values, overflow at each width, focus, states) run together.

## Sources
- Published craft guidance in the installed `impeccable` skill (version 4.5.1), craft-floor, critique and polish references, read 2026-11-15 as data; rules restated in own words.
- Apple HIG Color and Layout, https://developer.apple.com/design/human-interface-guidelines/ (prior reading, not re-fetched)
- W3C WCAG 2.2, https://www.w3.org/TR/WCAG22/ (contrast, focus), read 2026-11-14
