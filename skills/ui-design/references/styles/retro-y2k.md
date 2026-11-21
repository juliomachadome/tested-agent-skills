# Style: retro and Y2K

## Principles
Nostalgia as a deliberate identity: 90s desktop UI (bevels, system windows, pixel and bitmap type), early-2000s web 2.0 and Y2K futurism (chrome, glossy gel buttons, metallic gradients, bubbles, translucent plastics, techno shapes), or earlier print and arcade looks. The style is a costume over a normal interface: layout and states stay modern. NN/g recalls that early GUIs used heavy pseudo-3D effects as signifiers, which helped users see what was clickable but could be overdone and distracting [M, NN/g Flat Design]. Treat it as a trend [F].

## Typical tokens
| Area | Value |
|---|---|
| Type | bitmap or pixel display face for headings only; a legible system or humanist sans for body at 16 px or more; monospaced for accents |
| Colour | limited palette (teal, magenta, lime, silver, deep blue) or a web-safe style; black or deep navy backgrounds with neon accents; chrome gradients only on fills |
| Space | 4 or 8 base; tight and boxed, like windows |
| Radius | 0 for 90s windows; 8 to 999 for Y2K gel and bubbles |
| Borders | 2 px bevels: light top-left, dark bottom-right (computed from the surface colour) |
| Shadow | hard offset or inset bevel; glossy highlight gradient on buttons |
| Motion | stepped or blinking effects as accents, under 3 seconds, never on text |

## Do
- Keep it a skin: tokens swap, structure stays accessible and responsive.
- Make bevels and gloss communicate state: raised for buttons, inset for fields and pressed.
- Use pixel fonts only at large sizes with whole-pixel scaling.
- Offer a calmer variant or reduced-motion path for animation.

## Avoid
- Pixel or dingbat fonts for body text; Comic-like fonts for serious content.
- Auto-playing sound, marquee text, blinking over content.
- Chrome text gradients with poor contrast at small sizes.
- Fake OS windows that behave unlike real ones (draggable but not keyboard-operable).

## Accessibility risks
Neon on dark often passes, pastel chrome on silver often fails; gradients make contrast uneven; blink and flash can trigger photosensitivity (WCAG 2.3.1 limits flashes to three per second); bitmap fonts blur under zoom; decorative animation breaks reduced-motion expectations.

## Fits / does not fit
Fits: campaigns, fan or music sites, games, creative portfolios, nostalgic brands, events. Does not fit: banking, medicine, public services, long documents, any project with an established design system.

## Sources
NN/g Flat Design (BIBLIOGRAPHY 14, read this pass for the pseudo-3D history); WCAG 2.2 (16); WCAG Understanding 2.3.3 (24). Token values are practitioner choices [F]; no primary Y2K style guide exists to cite.
