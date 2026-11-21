# Style: Apple Human Interface Guidelines

## Principles
Clarity, deference to content, depth. Use system components, system colours and text styles so the product adapts to light, dark, increased contrast, Dynamic Type and Reduce Motion for free [C]. Customise sparingly and on top of the system. Since the 2025 platform generation, navigation and controls sit on a Liquid Glass layer floating above content (see `glass-translucent.md`); content itself uses standard materials [C, HIG Materials].

## Typical tokens
| Area | Value |
|---|---|
| Type | system font (SF); iOS default body 17 pt, minimum 11 pt [C, HIG Typography]; use text styles (Large Title, Title 1 to 3, Headline, Body, Callout, Subheadline, Footnote, Caption 1 and 2); avoid light weights at small sizes |
| Colour | semantic system colours (label, secondaryLabel, systemBackground, separator, tint); one tint as accent; custom colours need light, dark and increased-contrast variants [C] |
| Spacing | 8 pt rhythm, 16 pt typical margins, respect safe areas and layout margins |
| Radius | continuous (squircle) corners; concentric radii: inner radius = outer minus padding [F] |
| Elevation | materials and grouped backgrounds rather than heavy shadows |
| Motion | springs, short, interruptible; respond to Reduce Motion [C] |
| Targets | 44 x 44 pt default on iOS, 28 x 28 pt minimum [C, HIG Accessibility] |

## Do
- One prominent button for the most likely action; role-based buttons (destructive, cancel) [C, HIG Buttons].
- Follow the system appearance; avoid an app-specific light and dark switch [C, HIG Dark Mode].
- Text colour contrast: at least 4.5:1 up to 17 pt, 3:1 at 18 pt or bold [C, HIG Accessibility].
- Build hierarchy with text styles and system backgrounds before adding custom decoration.

## Avoid
- Material-style FABs and bottom sheets on iOS; hamburger menus when a tab bar fits.
- Liquid Glass in the content layer or stacked on custom controls everywhere [C].
- Fixed point sizes that ignore Dynamic Type; text under the home indicator or Dynamic Island.

## Accessibility risks
Translucent bars over busy content lose text contrast; check Reduce Transparency and Increase Contrast variants. Custom fonts can break Dynamic Type scaling. Gesture-only actions need a visible alternative.

## Fits / does not fit
Fits: iOS, iPadOS, macOS apps, products whose users expect a native feel, consumer and prosumer utility. Does not fit: a cross-platform brand-led product that needs one look everywhere (use its own tokens, borrowing only target sizes and states), data-dense pro dashboards on web.

## Sources
Apple HIG: Materials, Accessibility, Typography, Color, Dark Mode, Buttons, Layout, Motion (BIBLIOGRAPHY 26 to 33). Text sizes, target sizes and the contrast table were read this pass; the 8 pt rhythm and concentric-radius advice are practitioner [F].
