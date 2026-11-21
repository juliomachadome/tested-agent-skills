# Style: minimalist

## Principles
Remove until the task is clear, then stop. One focal point per view, generous space, a restrained palette, few type sizes, few borders. Minimalism is a content decision as much as a visual one: everything that remains has a job. NN/g links flat design to minimalism and warns that stripping signifiers hurts usability (clickable things must still look clickable) [M, NN/g Flat Design]. Hierarchy tools are the same few levers: size, weight, tone, position, space (NN/g visual hierarchy: few sizes, few colours) [M].

## Typical tokens
| Area | Value |
|---|---|
| Type | one family, 3 sizes and 2 weights per view; body 16 to 18 px, line height 1.5; headings 1.1 to 1.2 |
| Colour | neutral ramp (white to near-black), one action colour, status colours only when needed; text in 2 or 3 tones |
| Space | 4-based, big steps: 16, 24, 32, 48, 64, 96; space replaces borders |
| Radius | 4 to 12 px, one value family |
| Shadow | none or one soft level for overlays |
| Motion | opacity and a few px of translate, 150 to 250 ms |

## Do
- Keep one primary action; demote the rest to text or outline.
- Use space and tone shifts to group instead of lines.
- Keep affordances: filled or outlined buttons, underlined links, visible input boundaries at 3:1.
- Include all states (empty, error, loading); minimal does not mean missing.

## Avoid
- Hiding navigation or actions behind unlabeled icons; ghost buttons with hairline borders under 3:1.
- Light-grey text on white for secondary information (#999 on white is 2.85:1, fails).
- Emptiness that hides a lack of decisions: a bare screen with no identity.

## First view and subtraction pass [F]

Use this pass when the brief calls for a minimalist or restrained direction. Start with the page's goal and its real content. Choose one recognizable cue from the project, such as its product photography, typography or existing brand palette. Use design references to name why a choice works; borrow the principle without duplicating a screen. Compare an editorial reference with a shipped flow when the task includes interaction.

Inspect the first view at the relevant phone, tablet and desktop widths before adding motion. The visitor should know where they are, what matters first and how to proceed. Remove an eyebrow, subtitle, badge or container if removing it leaves the same facts, choices and next action. Keep prices, material terms, control labels, visible focus and error recovery where users need them. In dense tools, keep useful rows and aligned values; use restraint in decoration to make room for information.

Review the entire page and list what each section adds. Treat a hero mockup and a working demo of the same interface as potential duplication. Prefer the working surface when it fits the first view and the user wants to try the product. If both surfaces earn their place, give them different jobs, such as editing a schedule and showing the final PDF. Apply the same check to benefit sections and captions. Repeat a primary action when it serves a new reading position, such as returning to a demo from the end of a long page. Keep sections and states required by the brief.

Compare before and after in the same state and viewport. Record the surplus removed, the useful information retained and one visible detail that carries the project's identity. Review comprehension separately from appearance.

## Accessibility risks
Low-contrast subtle greys; placeholder-only labels; tiny touch targets in sparse layouts (space is cheap, so enlarge them); invisible focus because "it looks cleaner".

## Fits / does not fit
Fits: focused utilities, finance and health, onboarding, settings, marketing for premium products. Does not fit: expert tools needing density, playful brands, products whose users must discover many options at once.

## Sources
NN/g Flat Design (BIBLIOGRAPHY 14), NN/g Visual Hierarchy (11), NN/g Principles of Visual Design (12), Refactoring UI (8, site read; book text not read). Contrast figure computed with the WCAG formula.

## Quick recipe
Draw the screen in grayscale with one focal element. Give the page one heading size, one body size and one small size. Use 24 px between groups and 8 px inside them. Add the action colour to the primary button only. Then run the three checks that minimal screens usually fail: grey text contrast, tap-target size, and whether every clickable thing still looks clickable. Add a border or tint back wherever a boundary is needed to find a control.
