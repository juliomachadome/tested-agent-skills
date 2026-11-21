# Style: glass and translucent (including Apple's Liquid Glass)

## Principles
Translucent layers create depth: an element shows blurred content behind it so the person keeps a sense of place. Two levers define it, opacity and background blur; strokes and gradients add edge definition (NN/g). Design systems call this a "material" (Fluent calls its version Acrylic) [C, NN/g Glassmorphism].

**Liquid Glass (Apple).** Documented in the HIG Materials page: a dynamic material that unifies Apple platforms and forms a functional layer for controls and navigation (tab bars, sidebars) floating above content, letting content scroll and peek through while keeping controls legible. Apple's rules [C]: do not use Liquid Glass in the content layer (use standard materials for backgrounds); the only exception is transient interactive elements like sliders and toggles; use it sparingly on custom controls; limit it to the most important functional elements; use the clear variant only over visually rich backgrounds, and the regular variant otherwise; appearance changes with the system's accessibility settings that reduce transparency or increase contrast.

## Typical tokens
| Area | Value |
|---|---|
| Fill | white or dark at 55 to 85 percent opacity [F]; more opaque for text-bearing panels |
| Blur | 20 to 40 px backdrop blur [F]; NN/g: more blur is better over complex backgrounds |
| Edge | 1 px inner stroke at 20 to 40 percent white, subtle gradient highlight |
| Shadow | soft and large, low opacity |
| Type | system sans, medium weight or heavier on glass; no thin weights |
| Radius | generous: 16 to 28 px, capsule for bars |
| Motion | fluid, interruptible, short; reduce-motion fallback |

## Do
- Put text on the most opaque or most blurred surfaces; sample the worst background pixel and compute the ratio.
- Offer a solid fallback when transparency is off (`prefers-reduced-transparency` where supported, platform Reduce Transparency, or a user toggle) [C, NN/g: let users adjust].
- Keep glass for navigation, overlays, menus and floating controls; keep the content layer plain.
- Control what sits behind a panel where you can (simple or single-colour backgrounds).

## Avoid
- Glass everywhere, glass on glass, glass as decoration under body text.
- Low blur over video, photos or animation, which makes text unreadable.
- Gradient-blob backgrounds used only to make glass visible.

## Accessibility risks (legibility)
Text over translucency spans many background colours, so contrast varies across one string and automated checks mislead; WCAG 1.4.3 and 1.4.11 apply to the worst case. Busy backgrounds reduce text and icon legibility, and focus rings on glass can vanish. Provide Increase Contrast and Reduce Transparency paths, test over light, dark and colourful content, and re-check in dark mode.

## Fits / does not fit
Fits: iOS and iPadOS system-style navigation, media overlays, floating toolbars, widgets and music or photo apps. Does not fit: forms, tables, long reading, compliance-heavy flows, low-end devices where backdrop blur costs frame rate (blur is also a performance cost: check with `web-performance`).

## Sources
Apple HIG Materials (BIBLIOGRAPHY 26, read this pass), HIG Accessibility (27), NN/g Glassmorphism (15, read this pass), WCAG Understanding 1.4.3 and 1.4.11 (17, 18).
