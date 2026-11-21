# Typography

Read when choosing or auditing type. Facts marked with a source and "read 2026-11-14" were checked on that date; "(not re-verified)" ones come from a prior knowledge base that cited a source.

## Contents
1. Scale and roles
2. Line length and line height
3. Weights and families
4. Apple text styles and Dynamic Type
5. Material 3 type scale
6. Web specifics (zoom, rem, form fields, stacks)
7. Audit checklist

## 1. Scale and roles
- Define type as roles (display, title, body, label, caption), each a composite token: family, size, line height, weight, tracking. Screens pick a role, never a raw size.
- Hand-picked scale beats a mathematical ratio for UI because small sizes need integer steps. A workable web scale: 12, 14, 16, 18, 20, 24, 30, 36, 48 px. Avoid nested `em`, which compounds unpredictably; use `rem`.
- Neighboring sizes should differ visibly (about 12 to 25 percent). If two sizes look the same, delete one.
- Hierarchy comes first from weight and color tone, then from size. Two or three text tones (primary, secondary, tertiary) and two weights solve most screens.
- Label vs value: when a label is needed, make it the secondary item and the value the primary.

## 2. Line length and line height
- Body measure of 45 to 75 characters per line (cap the container with `max-width` in `ch`, for example 65ch). Narrower for small columns, never full viewport width.
- Line height inversely proportional to size: about 1.5 for body, 1.2 to 1.3 for subheads, 1.0 to 1.15 for large display text. Long lines and long text need looser line height.
- WCAG 1.4.12 requires content to tolerate user-set line height 1.5, paragraph spacing 2x, letter spacing 0.12 em, word spacing 0.16 em with no loss of content: do not give text containers fixed pixel heights. (w3.org/TR/WCAG22, read 2026-11-14)
- Tight leading is acceptable only for one or two lines.

## 3. Weights and families
- Prefer Regular, Medium, Semibold, Bold. Avoid Ultralight, Thin and Light for body; a thin custom face needs larger sizes. (Apple HIG Typography, not re-verified on this date; Apple Accessibility page confirms "aim for larger than the recommended sizes" for thin weights, read 2026-11-14)
- One family, or two clearly different ones. Numbers in tables and prices: tabular figures (`font-variant-numeric: tabular-nums`) so columns align.
- Do not use all caps for long labels (hurts word-shape reading); small caps-style labels need added tracking.
- Negative tracking on large headings is a brand choice, not a platform rule: Apple's own tracking table is slightly positive at small sizes and only mildly negative around 15 to 22 pt.

## 4. Apple text styles and Dynamic Type
Defaults and minimums (Apple HIG Accessibility page, read 2026-11-14, https://developer.apple.com/design/human-interface-guidelines/accessibility):

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |
| tvOS | 29 pt | 23 pt |

iOS text styles at the default Large size, size/line height in pt, verified against the official HIG Typography data on 2026-11-15 (https://developer.apple.com/design/human-interface-guidelines/typography). Apple also says to avoid Ultralight, Thin and Light with system fonts, and that three or more lines should not use tight leading even where height is limited:

| Style | Weight | Size/Leading |
|---|---|---|
| Large Title | Regular | 34/41 |
| Title 1 | Regular | 28/34 |
| Title 2 | Regular | 22/28 |
| Title 3 | Regular | 20/25 |
| Headline | Semibold | 17/22 |
| Body | Regular | 17/22 |
| Callout | Regular | 16/21 |
| Subhead | Regular | 15/20 |
| Footnote | Regular | 13/18 |
| Caption 1 | Regular | 12/16 |
| Caption 2 | Regular | 11/13 |

- Dynamic Type has seven normal sizes plus five accessibility sizes. Headings scale less than body (Large Title 34 to 60 pt across the range, Body 17 to 53 pt), so at the largest sizes hierarchy must survive by weight, color and position rather than size. (not re-verified for the full grid)
- Apple asks that text be enlargeable by at least 200 percent (140 percent in watchOS). (Accessibility page, read 2026-11-14)
- When text grows, prioritize content over chrome: tab labels can grow less than reading text; stack side-by-side items; let text wrap instead of truncating.
- On macOS the scale is denser than iOS (Body 13, Title 1 22). Do not raise all sizes on desktop; desktop is denser, not larger.
- In the iPhone viewport 1 pt equals 1 CSS px, so the table above transfers directly to CSS (use `rem` for the user zoom).

## 5. Material 3 type scale
Display 57/64, 45/52, 36/44; Headline 32/40, 28/36, 24/32; Title 22/28, 16/24, 14/20; Body 16/24, 14/20, 12/16; Label 14/20, 12/16, 11/16 (sp). Fifteen styles, five roles times three sizes. (m3.material.io type scale; the site renders by script and could not be fetched on 2026-11-14: not re-verified)

## 6. Web specifics
- Sizes in `rem`, heights flexible; test at 200 percent browser zoom (WCAG 1.4.4) and 320 CSS px width (1.4.10). (w3.org/TR/WCAG22, read 2026-11-14)
- `input`, `select`, `textarea` below 16 px make iOS Safari zoom on focus: keep fields at 16 px or more. (known browser behavior, not re-verified)
- iOS Dynamic Type reaches web content only for system font keywords in Safari; custom web fonts rely on browser zoom. (not re-verified)
- System-native stack without embedding Apple fonts: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`. Apple's system font license allows use in apps for Apple platforms only; on web, use a metrically close open font.
- Set `lang` correctly; hyphenation and quotes depend on it.
- Font loading: `font-display: swap` plus a size-matched fallback to limit layout shift (see `web-performance`).

## 7. Audit checklist
- [ ] Only scale roles used; count distinct sizes on a screen (aim at 4 to 6)
- [ ] Body at least 16 px web; nothing below 11 pt equivalent on mobile
- [ ] Measure 45 to 75 characters; line height by size
- [ ] No fixed-height text boxes; wraps at 200 percent zoom
- [ ] Weights from the allowed set; contrast checked on gray text
- [ ] Tabular numbers in data columns

## Sources
- W3C WCAG 2.2, https://www.w3.org/TR/WCAG22/ (1.4.4, 1.4.10, 1.4.12), read 2026-11-14
- Apple HIG Accessibility, https://developer.apple.com/design/human-interface-guidelines/accessibility (via the official JSON feed), read 2026-11-14
- Apple HIG Typography (official JSON feed), https://developer.apple.com/design/human-interface-guidelines/typography, read 2026-11-15 (Large-size table, default and minimum sizes, weights, leading)
- Material Design 3 typography, https://m3.material.io/styles/typography/overview (not re-verified)
- Wathan and Schoger, Refactoring UI (2018), book, scale and hierarchy advice (not re-verified)
