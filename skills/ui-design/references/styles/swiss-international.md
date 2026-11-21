# Style: Swiss / International Typographic

## Principles
Objectivity, order and a visible grid. Hierarchy comes from size, weight and position on a modular grid, not from ornament. Flush-left, ragged-right text, a limited palette, generous whitespace, photography or data in place of illustration. Müller-Brockmann's work on grid systems argues that a grid gives consistent, clear, and flexible layout; this skill uses the idea, not his page formats [M, book not re-read in detail this pass].

## Typical tokens
| Area | Value |
|---|---|
| Type | neo-grotesque sans (Helvetica-like, or a modern equivalent); 2 to 3 sizes per layout with a strong ratio (1.333 to 1.5); weights regular and bold; tight tracking on large headlines |
| Colour | white or very light grey, near-black text, one strong accent (often red) used on one element; photography supplies the rest |
| Grid | 12 columns on desktop, 4 on compact, 16 to 24 px gutters, a baseline of 4 or 8 px; all elements snap |
| Spacing | 8 base with large steps (48, 64, 96) between sections |
| Radius | 0 to 2 px |
| Shadow | none; separation by space and thin rules (1 px) |
| Motion | minimal: fades and slides 150 to 250 ms on the grid axes |

## Do
- Align everything to the grid and the baseline; let whitespace do grouping.
- Make one size jump dramatic: a big headline against small body text creates the hierarchy.
- Use rules and alignment instead of boxes and shadows.
- Keep lines at 45 to 75 characters by assigning body text to 5 to 7 columns.

## Avoid
- Decorative gradients, drop shadows, rounded pills.
- Centred long text, many type families, many colours.
- A grid that collapses at 320 px with no compact variant.

## Accessibility risks
Small light-grey captions on white fail 4.5:1; extreme headline size jumps can overflow at 200% zoom; a single red accent used for both brand and error loses meaning (keep status separate); rules as only separators between table rows can fall under 3:1.

## Fits / does not fit
Fits: corporate and institutional sites, portfolios, documentation, cultural sites, dashboards that value order, products where trust and neutrality matter. Does not fit: playful consumer products, products that need warmth, or an existing system with rounded, tinted components.

## Sources
Müller-Brockmann, Grid Systems in Graphic Design (BIBLIOGRAPHY 2, V); Lupton, Thinking with Type for type and grid practice (1, V); Butterick line length and spacing (9, 10); Bringhurst for measure and rhythm (3, V). Token numbers are practitioner defaults [F].
