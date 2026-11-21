# Style: editorial

## Principles
The content is the interface. Typography carries voice and hierarchy, reading comfort leads, and layout varies pace (lede, pull quote, figure, caption) without breaking the reading column. Think magazine, newsletter, long-form journalism, a documentation or knowledge site with personality. Bringhurst and Lupton frame type as the structure of the page: measure, leading, scale and contrast between text and display [M, books].

## Typical tokens
| Area | Value |
|---|---|
| Type | serif or humanist body at 17 to 20 px, line height 1.5 to 1.6; display face with character for headlines (serif or grotesque); a small-caps or letterspaced label style used sparingly; scale ratio 1.25 to 1.333 |
| Measure | 45 to 75 characters (about 65ch); Butterick gives 45 to 90 characters as a wider range and 120 to 145 percent of point size for line spacing [C source, practitioner] |
| Colour | paper or white background, near-black text, one accent for links and highlights; dark mode as warm dark grey with off-white text |
| Space | 8 base, vertical rhythm on the baseline; large top margins around headings, 1.5x line height between paragraphs |
| Radius / shadow | none or 2 px / none; images with captions instead of cards |
| Motion | subtle reveal, no parallax over text |

## Do
- Set the reading column first and let figures break out wider.
- Distinguish levels with size and weight; use real italics, bold and small caps from the font, not synthesized ones.
- Make links recognizable (underline) with contrast of at least 4.5:1 on the surface.
- Provide dark mode and text-size controls or respect browser zoom.

## Avoid
- The templated "editorial" look: ALL-CAPS label above every heading, one word of the heading in colour or italic, dots between metadata, 01/02/03 numbering on non-sequences. It reads as a template mark [F].
- Justified text without hyphenation (rivers); lines over 90 characters.
- Display type over busy photos without a scrim.

## Accessibility risks
Thin display weights at small sizes; low-contrast grey metadata; pull quotes and drop caps that confuse screen reader order; text-over-image captions; fonts that do not scale under text-spacing overrides (WCAG 1.4.12).

## Fits / does not fit
Fits: news, blogs, essays, docs with a voice, brand storytelling, reports. Does not fit: transactional flows, dense tools, dashboards.

## Sources
Bringhurst (BIBLIOGRAPHY 3), Lupton (1), Butterick line length and line spacing (9, 10), WCAG Understanding 1.4.12 (23). Numbers are practitioner defaults [F] except where a source is named.
