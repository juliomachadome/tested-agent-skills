# Style: Fluent 2 (Microsoft)

## Principles
Productivity first: clear hierarchy, native feel on each platform, calm surfaces, and materials such as Acrylic and Mica used to place layers. Fluent keeps the system font of each platform and uses Segoe UI as the web default [C, Fluent 2 Typography]. Content and tasks lead; chrome is quiet. Fluent says to write in sentence case and to avoid all caps for attention, as it is harder to read [C].

## Typical tokens
| Area | Value |
|---|---|
| Type (web ramp) | Caption 2 10/14, Caption 1 12/16, Body 1 14/20, Subtitle 2 16/22, Subtitle 1 20/26, Title 3 24/32, Title 2 28/36, Title 1 32/40, Large Title 40/52, Display 68/92 (size / line height px); regular, semibold, bold variants [C] |
| Colour | neutral foreground and background ramps plus a brand ramp; semantic status colours; light, dark and high-contrast themes |
| Spacing | 4 px base: 2, 4, 6, 8, 12, 16, 20, 24 [F] |
| Radius | small and consistent: about 2 to 8 px, circular for avatars [F] |
| Elevation | shadow tiers plus layering; acrylic for transient surfaces [F] |
| Motion | functional, short, with reduced motion respected [F] |
| Targets | follow the platform; web minimum 24 px (WCAG), prefer 32 to 44 |

## Do
- Use the type ramp roles and sentence case; body 14 px is dense: confirm it suits the audience.
- Keep one brand ramp and let neutrals do most of the work; support high contrast themes.
- Use the platform's native type and controls on each OS.

## Avoid
- Brand colour for large text areas without checking contrast.
- Decorative acrylic over busy content under text.
- Tiny 10 px captions as the only place to find important information.

## Accessibility risks
14 px base text needs the 200% zoom and text-spacing checks; acrylic and mica transparency reduces contrast; dense toolbars crowd 24 px targets.

## Fits / does not fit
Fits: enterprise and productivity software, Windows and Microsoft 365 add-ins, dashboards with forms. Does not fit: expressive consumer brands, editorial sites.

## Sources
Fluent 2 Typography page read this pass (BIBLIOGRAPHY 37). Fluent shapes, material and colour pages loaded without readable body text in the browser pass, so radius, elevation and motion values here are practitioner defaults [F], not Fluent's published numbers. NN/g glassmorphism article (15) confirms Acrylic as Fluent's translucent material.

## Quick recipe
Start from neutral surfaces and a 14/20 body. Use Subtitle 2 (16/22) for card titles and Title 3 (24/32) for page headings. Keep a single filled brand button per view, outline or subtle buttons for the rest, and a visible 2 px focus ring in a contrast colour. Test both light and dark, plus a high-contrast theme. If the project already ships Fluent UI components, use them as they are and change tokens, not component CSS.
