# Style: brutalism and neo-brutalism

## Principles
Brutalism (web) is raw and utilitarian: plain HTML elements, system or monospaced type, rigid layouts, few colours. Neo-brutalism is its more colourful and orderly descendant, blending brutalist rawness with nostalgic 90s graphic design: high contrast, blocky layouts, bold colours, thick borders, stark single-colour drop shadows, and "unpolished" elements [C, NN/g Neobrutalism]. NN/g's caution: the look draws attention but can overwhelm or confuse if usability is not kept; balance it. It is a trend [F], so treat it as taste, not as a rule set.

## Typical tokens
| Area | Value |
|---|---|
| Type | chunky grotesque or slab for headlines (700 to 900), neutral sans or mono for body; NN/g suggests pairing bold headlines with clean body fonts such as Inter or Roboto; headline about 2x body size |
| Colour | 2 to 3 bold hues plus black and an off-white or paper background (NN/g: limit the palette) e.g. black #000, yellow #FFE600, pink or coral, mint #B8F2E6 |
| Spacing | 8-based, generous padding of 24 to 32 px around dense shapes (NN/g) |
| Radius | 0 to 4 px; or deliberately mixed |
| Borders | 2 to 4 px solid black |
| Shadow | hard, no blur: `4px 4px 0 #000` (NN/g example: a black shadow offset 4 px) |
| Motion | snappy: press moves the element into its shadow (translate 2 to 4 px, shadow shrinks), 100 to 150 ms, no easing flourish |

## Worked contrast (computed)
Black on #FFE600 = 16.57:1; black on #FF6B6B = 7.57:1; white on #FF6B6B = 2.78:1 (fails); #FFE600 on white = 1.27:1 (fails as text; fine as a fill under black text). Rule: bright colours are fills, black is the text.

## Do
- Keep real hierarchy: size contrast, one clear primary action, and consistent shadow direction.
- Show interaction: hover and focus change fill or shadow; NN/g recommends clear feedback such as underline or colour shift [C].
- Keep body text calm: 16 px or more, 45 to 75 characters, neutral face.
- Use whitespace to offset thick borders.

## Avoid
- Yellow on cyan or any pair that fails the checks (NN/g).
- Decorative condensed or novelty faces for paragraphs.
- Borders and shadows on every element: it removes hierarchy and increases clutter.
- Rotated or overlapping text that breaks reading order and zoom.

## Accessibility risks
Thick borders do not replace text contrast; bright fills with white text commonly fail 4.5:1; "ugly on purpose" layouts can break reflow at 320 px and 200% zoom; overlapping blocks can hide focus rings (WCAG 2.4.11). Make the focus ring a thick, high-contrast outline, which suits the style. Motion stays short and respects reduced motion.

## Fits / does not fit
Fits: creative tools, developer and indie products, portfolios, youth brands, campaigns, landing pages with a point of view. Does not fit: healthcare, banking, legal, long-form reading, dense enterprise data, an existing project design system you may not override.

## Sources
NN/g Neobrutalism: Definition and Best Practices (BIBLIOGRAPHY 13), read this pass; contrast numbers computed here with the WCAG formula; WCAG Understanding 1.4.3 (17) and 2.4.11 (20).
