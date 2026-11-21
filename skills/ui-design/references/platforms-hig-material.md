# Platforms: Apple HIG, Material 3, web and PWA

## Contents
1. Target sizes (three rulers)
2. HIG vs Material 3 table
3. Safe areas and viewport
4. Navigation and sheets
5. Buttons and icons
6. Installed PWA surfaces
7. Choosing a base

## 1. Target sizes
| Ruler | Default | Minimum | Source |
|---|---|---|---|
| Apple iOS, iPadOS | 44 x 44 pt | 28 x 28 pt | HIG Accessibility, read 2026-11-14 |
| Apple macOS | 28 x 28 pt | 20 x 20 pt | same |
| Apple visionOS | 60 x 60 pt | 28 x 28 pt | same |
| Apple watchOS | 44 x 44 pt | 28 x 28 pt | same |
| Apple tvOS | 66 x 66 pt | 56 x 56 pt | same |
| Material (Android) | 48 x 48 dp, about 8 dp between targets | | m3.material.io (not re-verified) |
| WCAG 2.2 AA 2.5.8 | | 24 x 24 CSS px, with exceptions | w3.org, read 2026-11-14 |
| WCAG 2.2 AAA 2.5.5 | 44 x 44 CSS px | | w3.org Understanding 2.5.5, read 2026-11-15 (exceptions: equivalent, inline, user-agent control, essential) |

WCAG 2.5.8 exceptions: spacing (a 24 px circle centered on each undersized target overlaps no other target), equivalent control on the same page, inline target within a sentence or limited by surrounding line height, user-agent-sized control, and essential presentation. (read 2026-11-14)

Practical web rule: 44 px as the design default, 48 px for Android-heavy or older audiences, never below 24 px; the hit area may exceed the drawn icon via padding. Add about 12 pt padding around bezeled controls and about 24 pt around bezel-less ones (HIG, read 2026-11-14).

## 2. HIG vs Material 3
| Topic | Apple HIG | Material 3 |
|---|---|---|
| Touch target | 44 x 44 pt | 48 x 48 dp |
| Body text | Body 17/22 pt | Body Large 16/24, Medium 14/20 sp |
| Type scale | 11 named text styles (Large Title to Caption 2) | 15 styles: Display, Headline, Title, Body, Label by Large, Medium, Small |
| Top-level navigation | Tab bar at bottom (3 to 5 items); sidebar on iPad and Mac | Navigation bar (3 to 5) on compact; rail on medium; drawer on large |
| Back | Back button at top leading plus edge swipe | System back gesture or button; app bar arrow |
| Primary action | Prominent button in a bar or after content | Floating action button for the screen's main action |
| Depth | Thin separators, translucent materials, little shadow | Tonal color elevation plus shadow |
| Color | One accent plus system semantic colors | Role-based palette (primary, secondary, tertiary, surface, on-*) generated from a seed; dynamic color |
| Shape | Continuous corners, moderate radius | Shape scale; expressive variants use more varied shapes |
| Sheets | Detents (medium, large) with a grabber | Standard and modal bottom sheets |
| Button text | Sentence case, verb | Sentence case (M2 used all caps) |
Source: Apple HIG pages above; M3 values from m3.material.io (not re-verified: site renders by script). Material comparison row on type scale also in typography.md.

Takeaways: do not mix idioms on one screen; pick a base and borrow the larger target where both audiences matter. Material research on its expressive update reports faster finding of enlarged key items but is manufacturer research without a peer-reviewed publication: use the direction (primary action large, text labels kept) not the multiplier.

## 3. Safe areas and viewport
- Never place controls or text under the notch, status bar, dynamic island or home indicator. Backgrounds and images may bleed; controls may not. (Apple HIG Layout, prior reading)
- Web: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` plus `env(safe-area-inset-*)`. `env()` is not a margin: combine with `max()`, for example `padding-bottom: max(12px, env(safe-area-inset-bottom))`. (WebKit blog on designing for iPhone X; MDN env, prior reading 2026-11-13, not re-fetched)
- Landscape iPad and phones can have nonzero side insets: gutters use `max()` too.
- Use `dvh` or `svh` instead of `100vh` for full-height layouts so the browser bar does not clip footers. (not re-verified)
- Virtual keyboard: it shrinks the visual viewport, not the layout viewport; read `window.visualViewport` to keep the focused field and primary action visible; test on a device, emulators do not show it. (MDN VisualViewport, prior reading)
- Fixed bars must not hide the focused item: use `scroll-padding` equal to bar heights (WCAG 2.4.11).

## 4. Navigation and sheets
- Tab bar is for sections not actions; 3 to 5 items; always visible except under modals; icon plus one-word label; do not disable an empty tab, explain the emptiness inside it. Badges only for critical information. (HIG Tab bars, prior reading)
- Modal only for a focused, short task; always an obvious exit (button and drag-down), confirm if closing loses data; one sheet at a time; Cancel at leading, Done at trailing; long multi-step work belongs in a full page, not a sheet. (HIG Modality, Sheets, prior reading)
- Since iOS 26 navigation controls float on a translucent layer over content; translate to web as a translucent bar over scrolling content with brand color only on the primary action. Do not copy Apple assets or the Apple UI kit; patterns are fine, assets are not. (HIG Layout and Color, prior reading)

## 5. Buttons and icons
- One or two prominent buttons per view; distinguish the preferred option by style not size; labels start with a verb; destructive never primary; full width on phones eases tapping. (HIG Buttons, prior reading)
- Icons: one library per product with fixed stroke and sizes (for example 24 px navigation, 20 px in lists); open libraries include Lucide, Phosphor, Heroicons, Material Symbols, Tabler. System symbol sets from a platform vendor are licensed for that vendor's platforms only and cannot be used in logos or app icons.
- Icon without label only when universal (search, close, send, home, print); heart and star change meaning across products. Labels always visible, never hover-only. In a usability test reported by NN/g, no participant clicked a clock icon that opened history; NN/g also says labels should be always visible, not revealed on hover, and that few icons (home, print, search magnifier) are widely recognized. (NN/g Icon Usability, 2014, read 2026-11-15)
- Five-second test: if you need more than five seconds to find an icon for the concept, use text.

## 6. Installed PWA surfaces
- Manifest: `name`, `short_name` (about 12 characters), `start_url`, `id`, `display: standalone`, `theme_color`, `background_color`, 192 and 512 px icons plus a maskable icon. (web.dev, prior reading)
- `beforeinstallprompt` exists only in Chromium; save the event and offer install after a completed task, never in the first second; `prompt()` works once per event. On iOS install is Share, Add to Home Screen; show an illustrated instruction. Offer install only in a browser tab: `@media (display-mode: browser)`.
- In standalone there is no browser back button or address bar: every screen needs its own back control; external links open outside the app.
- Orientation locks in the manifest affect tablets: a portrait lock keeps the installed app portrait even on a landscape iPad.
- Offline: a designed offline screen with retry, never the browser error page. Updates: define how a new service worker replaces the old (prompt or next launch).
- App-like polish: no accidental zoom (16 px fields), controlled `overscroll-behavior`, pressed states everywhere.

## 7. Choosing a base
Match the dominant platform of the audience; for responsive web used on both, use a platform-neutral system with the larger touch target (48 px on touch), sentence-case verb labels, bottom navigation on compact, and avoid imitating a platform's chrome so closely that it feels wrong on the other.

## Sources
- WCAG 2.2 Understanding Target Size (Enhanced), https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html, read 2026-11-15
- Android developers, window size classes (Material 3 classes), read 2026-11-15
- Material Web theming docs, https://github.com/material-components/material-web/blob/main/docs/theming/README.md, read 2026-11-15 (three token levels: reference, system, component)
- Apple HIG Accessibility, https://developer.apple.com/design/human-interface-guidelines/accessibility, read 2026-11-14
- Apple HIG Layout, Buttons, Tab bars, Sheets, Modality, SF Symbols, https://developer.apple.com/design/human-interface-guidelines/ (prior reading 2026-11-12, not re-fetched)
- W3C WCAG 2.2 Target Size (Minimum), https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html, read 2026-11-14
- Material Design 3, https://m3.material.io (not re-verified; site could not be fetched on 2026-11-14)
- WebKit, Designing Websites for iPhone X, https://webkit.org/blog/7929/designing-websites-for-iphone-x/ (prior reading)
- MDN env(), VisualViewport (prior reading)
- NN/g, Icon Usability (2014), https://www.nngroup.com/articles/icon-usability/ (prior reading, not re-fetched)
- web.dev Learn PWA installation prompt, https://web.dev/learn/pwa/installation-prompt (prior reading)
