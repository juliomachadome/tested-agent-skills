# Choosing a style

A style is a set of choices (type, colour, space, shape, depth, motion) made for a reason. This skill never imposes one; it picks one only when nothing exists.

## Order of decision
1. **The project's own system wins.** Read DESIGN.md, token files, theme files, a component library, the CSS variables and the screens already shipped. If a system exists, the style is "whatever it is"; work inside it. Never override it. A request that conflicts ("make it brutalist") on a project with a system is a proposal to put to the owner: show the delta and what it would cost, do not apply it silently.
2. **Platform conventions next.** A native iOS app starts from `hig-apple.md`, Android from `material-3.md`, a Windows or Office-adjacent product from `fluent-2.md`. A web product has no mandated platform style, but its users bring platform habits (controls, targets, focus).
3. **The request.** If the user names a style, open that file. If they name a feeling ("serious", "playful", "trustworthy", "dense"), map it with the table.
4. **Product and audience.** No request and no system: choose by what the product does. Finance, health, legal, enterprise: `minimalist.md` or `swiss-international.md`. Reading and media: `editorial.md`. Pro tools and analytics: `data-dense.md`. Kids, habit and consumer fun: `playful.md`. Developer or creative tools with a rebellious brand: `brutalism-neo-brutalism.md`. Nostalgic or campaign pages: `retro-y2k.md`.
4b. **Let the owner choose.** With no style and no brand given, offer 2-3 directions in one line each (name the style file, the feeling, one example choice) and ask; if you must proceed without asking, pick one, say why, and say how to switch. The owner can name any file in this folder at any time.
5. **Say what you chose and why**, in one line, and mark the tokens provisional until the owner approves.

| Feeling or need | Open |
|---|---|
| native iPhone, iPad, Mac feel | hig-apple.md |
| native Android, Google ecosystem, tonal colour roles | material-3.md |
| Windows, Microsoft 365, enterprise productivity | fluent-2.md |
| loud, raw, anti-polish, high contrast | brutalism-neo-brutalism.md |
| grid, order, neutral confidence | swiss-international.md |
| long reading, magazine, content-led | editorial.md |
| calm, spacious, focused | minimalist.md |
| layered, floating controls over content | glass-translucent.md |
| nostalgia, 90s and 2000s, campaigns | retro-y2k.md |
| power users, many rows, monitoring | data-dense.md |
| friendly, rounded, rewarding | playful.md |

## Mixing rules
- One **base** style per product, at most one **accent** style used in one place (a hero, an empty state, a campaign page). Two accents compete.
- Mix only along compatible axes: a Swiss grid with editorial type works; a glass layer on a minimalist base works if text sits on solid or heavily blurred surfaces; neo-brutalism with playful works (both use saturated colour and rounded or blocky shapes). Brutalism with glass, or data-dense with retro, usually fights itself.
- Tokens stay one set. A second style is a different mapping of the same roles, not a second palette in the code.
- Semantic colours (danger, success) keep their meaning across any style [C].
- Do not mix Apple and Material idioms on one screen (native components, navigation, sheet behaviour).
- Accessibility floor is identical for every style: WCAG 2.2 AA contrast, targets, focus visible, reduced motion. Style never buys an exemption.

## What a style file contains
Principles, typical tokens, do and avoid, accessibility risks, when it fits and when not, sources. Token numbers are typical starting values [F] unless a source is named; the project's own values replace them. Trends date quickly: treat anything marked trend as a taste decision, not a rule.
