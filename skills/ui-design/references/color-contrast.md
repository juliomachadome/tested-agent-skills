# Color and contrast

## Contents
1. WCAG 2.2 thresholds
2. Computing contrast
3. APCA and WCAG 3 status
4. Semantic vs brand color
5. Palette construction
6. Dark mode
7. High contrast, forced colors, color blindness
8. Audit steps

## 1. WCAG 2.2 thresholds
(w3.org/TR/WCAG22, read 2026-11-14)
- 1.4.3 Contrast (Minimum), AA: text and images of text at least 4.5:1. Large-scale text at least 3:1, where large scale means at least 18 point, or 14 point and bold (roughly 24 px, or 18.66 px bold). Exceptions: inactive components, pure decoration, logotypes.
- 1.4.11 Non-text Contrast, AA: UI component boundaries needed to identify them, their states, and graphical objects required to understand content need at least 3:1 against adjacent colors. Decorative dividers are exempt.
- 1.4.1 Use of Color: color is never the only means of conveying information.
- Focus: visible keyboard focus (2.4.7); the focused item must not be entirely hidden by author content (2.4.11, AA, new in 2.2). The 2 px / 3:1 focus-appearance ring (2.4.13) is AAA but cheap to adopt.
- Apple states the same ratios for iOS (up to 17 pt: 4.5:1; 18 pt and bold: 3:1), asks to check light and dark appearances, and to offer a higher-contrast scheme when Increase Contrast is on. (HIG Accessibility, read 2026-11-14)

## 2. Computing contrast
Relative luminance (WCAG definition, read 2026-11-14):
1. For each channel c in 0..255, s = c / 255.
2. Linearize: if s <= 0.04045 then s / 12.92 else ((s + 0.055) / 1.055) ^ 2.4. (Older text used 0.03928; no practical difference.)
3. L = 0.2126 R + 0.7152 G + 0.0722 B.
4. Contrast = (L_lighter + 0.05) / (L_darker + 0.05), range 1 to 21.

Practical rules:
- Compute on the final blended color: translucent overlays, opacity, gradients and images must be flattened first; test the worst-case region of a gradient or photo.
- Do not round up: 4.49 fails 4.5.
- Check every pair in every theme and state (hover, disabled is exempt, selected, focus, placeholder when it carries meaning).
- Gray text on a colored surface looks washed out: derive the text color from the surface hue (lighter or darker tone of it) rather than lowering opacity of black.

A shell one-liner is enough; no tool is required:
```
python3 -c "
def L(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    f=lambda s: s/12.92 if s<=0.04045 else ((s+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
a,b=sorted([L('#767676'),L('#ffffff')])
print(round((b+0.05)/(a+0.05),2))"
```

## 3. APCA and WCAG 3 status
- WCAG 3.0 is a W3C Working Draft (dated 10 September 2026 when read 2026-11-14). The document says it should not be cited as other than work in progress, and states that the contrast algorithm to be used is "yet to be determined". (https://www.w3.org/TR/WCAG3/)
- APCA (Advanced Perceptual Contrast Algorithm) is a candidate perceptual model that accounts for polarity, font size and weight; it is not a conformance requirement of WCAG 2.2 and does not replace the 4.5:1 and 3:1 tests. APCA is not named on the visible portion of the WCAG 3 draft read on that date.
- Practical stance: pass WCAG 2.2 ratios for conformance and legal claims; optionally use APCA-style thinking (large light-on-dark text can look weaker than its ratio suggests, thin weights need more contrast) as an extra design heuristic, never as a substitute.

## 4. Semantic vs brand color
- Brand color is decoration and identity: logo, hero, primary action background, accents. A tenant or theme may change it.
- Semantic color is information: error, warning, success, info, risk or severity levels, selection, link. These keep a single meaning across screens and themes, and a brand theme must not override them.
- One color, one meaning. If the brand color marks clickable things, do not use it for non-clickable text or for a status.
- Never encode meaning by color alone: pair with an icon, shape, text or position. The critical confusable pairs are red/green and blue/orange. (Apple HIG Accessibility; WCAG 1.4.1)
- Name tokens by role (`text-secondary`, `status-danger`), not by appearance (`gray-500`, `red`).

## 5. Palette construction
- Define ramps up front, not with runtime lighten/darken: 8 to 10 neutral steps, 5 to 10 steps for the action color and each status color. (Refactoring UI, not re-verified)
- Tint neutrals slightly toward the brand hue for cohesion, keeping contrast pairs checked.
- Pick text/background pairings per role in the token file and test them once (a matrix: text-primary, text-secondary, text-on-action over each surface).
- Use color sparingly: a screen with one saturated accent reads clearer than several.
- Charts: do not rely on hue alone; vary lightness, add direct labels or patterns. Non-text items need 3:1 against the background (1.4.11).

## 6. Dark mode
- Treat dark as its own semantic mapping, not an inverted light theme. Use a very dark gray, not pure black, on large surfaces; raise surface lightness to show elevation instead of heavier shadows; reduce saturation of accent colors so they do not vibrate; re-test every ratio. (principle common to HIG and Material; not re-verified on this date)
- Status colors keep their meaning; adjust lightness for contrast, not hue.
- Apply through `prefers-color-scheme` and an explicit `data-theme` override; declare `color-scheme` so native controls, scrollbars and autofill follow the theme. `color-scheme` alone does not recolor the app (MDN, https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme, per prior reading 2026-11-13, not re-fetched).
- Photos and illustrations: reduce brightness or provide dark variants when they glare.

## 7. High contrast, forced colors, color blindness
- `prefers-contrast: more`: provide a token set with stronger text and visible borders on fields.
- `forced-colors: active` (for example Windows contrast themes) overrides author colors and removes `box-shadow`; use `outline` for focus rings and add real borders to pills, chips and filled fields so they do not vanish. (MDN forced-colors, prior reading, not re-fetched)
- Simulate protanopia, deuteranopia and tritanopia in browser devtools; confirm status is still distinguishable by icon or label.

Inclusive design framing: Microsoft's Inclusive Design principles are to recognize exclusion, learn from diversity, and solve for one and extend to many; contrast, large targets and clear labels designed for permanent needs also serve temporary and situational ones (glare, a hand full, a broken wrist). (https://inclusive.microsoft.design/, read 2026-11-15)

## 8. Audit steps
1. List text and non-text pairs per theme; compute ratios; record pass/fail.
2. Check disabled, placeholder, link-in-text (needs a non-color cue or 3:1 against surrounding text), and focus pairs.
3. Verify no meaning is color-only.
4. Verify semantic tokens are not overridable by brand themes.
5. Toggle dark, high contrast and forced colors; screenshot each.

## Sources
- Microsoft Inclusive Design, https://inclusive.microsoft.design/, read 2026-11-15
- WCAG 2.2 Understanding Non-text Contrast, https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html, read 2026-11-15 (inactive components and logos exempt; focus indicators and checkmarks count)
- W3C WCAG 2.2, https://www.w3.org/TR/WCAG22/ and Understanding pages, read 2026-11-14
- W3C WCAG 3.0 Working Draft, https://www.w3.org/TR/WCAG3/, read 2026-11-14
- Apple HIG Accessibility, https://developer.apple.com/design/human-interface-guidelines/accessibility, read 2026-11-14
- MDN color-scheme, prefers-contrast, forced-colors (prior reading 2026-11-13, not re-fetched)
- Wathan and Schoger, Refactoring UI (2018), book (not re-verified)

## Brand-palette check routine (always)
1. Build the full pair matrix: every text colour on every background it will sit on, plus both alternatives for each fill (white text and the darkest ink on it), plus non-text pairs (borders, focus rings, icons) against their background (WCAG 1.4.11, 3:1).
2. Compute every ratio with the relative-luminance formula (a script, not by eye) and report the number for each pair, passing or failing.
3. Fix without losing the brand: keep brand colours as fills and decoration; add separate text-safe tokens (a darker variant for text and for white-label buttons); prefer dark labels on light fills.
4. Say that the client or brand owner must approve the new text-safe variants, and list what was not checked (dark mode, hover/pressed/disabled states, text over images or gradients).
