# Style: Material Design 3 (including Expressive)

## Principles
Colour roles instead of colours, a single type scale, shape and motion as theme parts. M3 defines 26 standard colour roles in six groups (primary, secondary, tertiary, error, surface, outline) built on accessible pairings; roles map to tokens, so a custom component must map to the same roles [C, M3 Color roles]. Dynamic colour derives a scheme from a seed colour or wallpaper. Reference, system and component token levels are the structure [C, Material Web docs].

## Typical tokens
| Area | Value |
|---|---|
| Type | one scale with 15 baseline and 15 emphasized styles, Display, Headline, Title, Body and Label in Large, Medium and Small [C, M3 Type scale]; emphasized styles for selection, primary actions and editorial moments |
| Colour | roles such as primary / on-primary / primary-container, surface and surface-container levels, outline; error always its own group |
| Spacing | 4 dp grid, 8 dp rhythm, 16 dp margins on compact [F] |
| Radius | shape scale from none to full; larger and more varied shapes in Expressive [F] |
| Elevation | tonal surface colour plus light shadow; avoid heavy shadows |
| Motion | the physics system (springs) replaces easing and duration; two schemes, expressive (some overshoot) and standard (minimal bounce, for utilitarian products) [C, M3 Motion, May 2025 update] |
| Targets | 48 dp (practitioner and platform default; page values were not re-read this pass) |

## Do
- Pick colour by role: containers for emphasis, on-colours for text on them.
- Use the standard motion scheme for utilitarian or dense products, expressive for hero moments.
- Adapt layout by window size class (compact below 600, medium 600 to 839, expanded 840 and up).

## Avoid
- Mixing iOS idioms (back-swipe-only navigation, iOS segmented style) into Android screens.
- Hand-picking hex values that sidestep the role system, which breaks dark and dynamic colour.
- Applying expressive overshoot to forms, tables or error feedback.

## Accessibility risks
Dynamic colour from a user wallpaper can produce low-contrast custom pairings if you leave roles; always use on-colour roles. Bouncy springs should shrink to fades under reduce-motion settings. Tonal buttons with low surface contrast can fail 3:1 for boundaries; check.

## Fits / does not fit
Fits: Android, Google ecosystem, web products wanting a complete token system with theming. Does not fit: products with a strong own identity that would be diluted by its look, or iOS-first products.

## Sources
m3.material.io Color roles, Type scale and tokens, Motion (BIBLIOGRAPHY 34 to 36): read this pass through a browser. M3 shape, elevation and 48 dp values were not re-read this pass; treat as practitioner [F].
