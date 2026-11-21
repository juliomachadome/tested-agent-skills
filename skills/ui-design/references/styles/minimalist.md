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

## Accessibility risks
Low-contrast subtle greys; placeholder-only labels; tiny touch targets in sparse layouts (space is cheap, so enlarge them); invisible focus because "it looks cleaner".

## Fits / does not fit
Fits: focused utilities, finance and health, onboarding, settings, marketing for premium products. Does not fit: expert tools needing density, playful brands, products whose users must discover many options at once.

## Sources
NN/g Flat Design (BIBLIOGRAPHY 14), NN/g Visual Hierarchy (11), NN/g Principles of Visual Design (12), Refactoring UI (8, site read; book text not read). Contrast figure computed with the WCAG formula.

## Quick recipe
Draw the screen in grayscale with one focal element. Give the page one heading size, one body size and one small size. Use 24 px between groups and 8 px inside them. Add the action colour to the primary button only. Then run the three checks that minimal screens usually fail: grey text contrast, tap-target size, and whether every clickable thing still looks clickable. Add a border or tint back wherever a boundary is needed to find a control.
