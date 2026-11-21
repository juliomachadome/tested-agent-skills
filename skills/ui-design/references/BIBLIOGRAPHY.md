# Bibliography: ui-design

Checked 18/11/2026. Status: **V** = identity (title, year, publisher; authors via the OpenLibrary authors endpoint) matched to the ISBN at `https://openlibrary.org/isbn/<isbn>.json` this pass; **P** = official page opened and the relevant text read this pass (JavaScript pages through a browser pass or the platform's JSON feed); **S** = exists, text not read; **U** = unverified. Nothing is quoted; ideas are restated. Older reference files (typography, color-contrast, layout, tokens, platforms, motion, visual-review) cite earlier readings listed in their own source lines; they are not re-counted here.

## Books
1. Lupton, E. *Thinking with Type*, 2nd revised ed. Princeton Architectural Press, 2010. ISBN 978-1568989693. **V** (catalogue title "Thinking with type", author Ellen Lupton). Backs: type, grid and hierarchy practice in `styles/swiss-international.md`, `styles/editorial.md`.
2. Müller-Brockmann, J. *Grid Systems in Graphic Design*. Niggli, 1996 (catalogue edition). ISBN 978-3721201451. **V** (author Josef Müller-Brockmann). Backs: the grid as the basis of consistent layout (`styles/swiss-international.md`).
3. Bringhurst, R. *The Elements of Typographic Style*, 3.0 ed. Hartley & Marks, 2005 (catalogue). ISBN 978-0881792065. **V** (author Robert Bringhurst). Backs: measure, leading, scale (`styles/editorial.md`).
4. Tufte, E. R. *The Visual Display of Quantitative Information*. Graphics Press, 1983 (first ed.). ISBN 978-0961392147. **V** (author Edward R. Tufte). Backs: data-ink thinking for `styles/data-dense.md`.
5. Albers, J. *Interaction of Color*, 50th anniversary ed. Yale University Press, 2013. ISBN 978-0300179354. **V** (catalogue author "Joseph Albers"). Backs: colour is judged by its neighbours (`styles/playful.md`; used lightly).
6. Yablonski, J. *Laws of UX*. O'Reilly, 2020 (first ed., catalogue). ISBN 978-1492055310. **V**. Backs: proximity, hierarchy-related laws cited in reviews.
7. Tidwell, J., Brewer, C., Valencia, A. *Designing Interfaces*, 3rd ed. O'Reilly, 2020. ISBN 978-1492051961. **V**. Backs: named interface patterns (visual hierarchy, lists, tables).
8. Wathan, A., Schoger, S. *Refactoring UI*. Self-published, 2018. https://www.refactoringui.com/ . **P** (book's official site opened 18/11/2026 and its description read; the book's text itself not read, no ISBN checked). Backs: hierarchy by weight and tone, constrained scales, gray-first design (`styles/minimalist.md`).

## Typography articles
9. Butterick, M. *Practical Typography: Line length*. https://practicaltypography.com/line-length.html . **P** 18/11/2026: 45 to 90 characters, or two to three alphabets.
10. Butterick, M. *Practical Typography: Line spacing*. https://practicaltypography.com/line-spacing.html . **P** 18/11/2026: 120 to 145 percent of the point size.

## NN/g
11. NN/g. *Visual Hierarchy in UX: Definition*. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ . **P** 18/11/2026.
12. NN/g. *5 Principles of Visual Design in UX*. https://www.nngroup.com/articles/principles-visual-design/ . **P** 18/11/2026.
13. NN/g. *Neobrutalism: Definition and Best Practices*. https://www.nngroup.com/articles/neobrutalism/ . **P** 18/11/2026: characteristics (high contrast, thick borders, stark shadows) and best practices (palette of 2 to 3 colours, contrast, readable body type, whitespace, interaction feedback).
14. NN/g. *Flat Design: Its Origins, Its Problems, and Why Flat 2.0 Is Better for Users*. https://www.nngroup.com/articles/flat-design/ . **P** 18/11/2026: lack of signifiers on clickable elements; history of pseudo-3D.
15. NN/g. *Glassmorphism: Definition and Best Practices*. https://www.nngroup.com/articles/glassmorphism/ . **P** 18/11/2026: opacity and blur, contrast, more blur over busy backgrounds, user control of transparency.

## WCAG and tokens (w3.org)
16. W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*, Recommendation. https://www.w3.org/TR/WCAG22/ . **P** 18/11/2026 (document opened, success criteria list read).
17. W3C. *Understanding SC 1.4.3 Contrast (Minimum)*. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html . **P** 18/11/2026.
18. W3C. *Understanding SC 1.4.11 Non-text Contrast*. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html . **P** 18/11/2026.
19. W3C. *Understanding SC 2.5.8 Target Size (Minimum)*. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html . **P** 18/11/2026.
20. W3C. *Understanding SC 2.4.11 Focus Not Obscured (Minimum)*. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html . **P** 18/11/2026.
21. W3C. *Understanding SC 2.4.7 Focus Visible*. https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html . **P** 18/11/2026.
22. W3C. *Understanding SC 1.4.4 Resize Text*. https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html . **P** 18/11/2026.
23. W3C. *Understanding SC 1.4.12 Text Spacing*. https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html . **P** 18/11/2026.
24. W3C. *Understanding SC 2.3.3 Animation from Interactions*. https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html . **P** 18/11/2026.
25. W3C DTCG. *Design Tokens Format Module 2025.10*. https://www.designtokens.org/tr/2025.10/format/ . **P** 18/11/2026 (page opened; `$value` and `$type` format).

## Apple HIG (developer.apple.com/design/human-interface-guidelines)
26. Apple. *Materials*. https://developer.apple.com/design/human-interface-guidelines/materials . **P** 18/11/2026 (browser pass): Liquid Glass and standard materials, content-layer rule, regular and clear variants.
27. Apple. *Accessibility*. https://developer.apple.com/design/human-interface-guidelines/accessibility . **P** 18/11/2026 (browser pass): 44x44 pt iOS default, 28x28 minimum, contrast table, Reduce Motion.
28. Apple. *Color*. https://developer.apple.com/design/human-interface-guidelines/color . **P** 18/11/2026 (platform JSON feed text): semantic system colours, light, dark and increased contrast.
29. Apple. *Dark Mode*. https://developer.apple.com/design/human-interface-guidelines/dark-mode . **P** 18/11/2026 (JSON feed text): follow the system appearance, avoid an app-specific switch.
30. Apple. *Motion*. https://developer.apple.com/design/human-interface-guidelines/motion . **P** 18/11/2026 (JSON feed text): make motion optional, do not rely on it alone.
31. Apple. *Layout*. https://developer.apple.com/design/human-interface-guidelines/layout . **P** 18/11/2026 (JSON feed text): safe areas, margins and guides.
32. Apple. *Typography*. https://developer.apple.com/design/human-interface-guidelines/typography . **P** 18/11/2026 (JSON feed text): default and minimum sizes per platform (iOS 17 and 11 pt), Dynamic Type.
33. Apple. *Buttons*. https://developer.apple.com/design/human-interface-guidelines/buttons . **P** 18/11/2026 (JSON feed text): 44x44 pt hit region, prominent style for the most likely action, press state.

## Material Design 3 (m3.material.io) and Fluent 2
34. Google. *Material Design 3: Color roles*. https://m3.material.io/styles/color/roles . **P** 18/11/2026 (browser pass): 26 roles in six groups, accessible pairings, tokenized roles.
35. Google. *Material Design 3: Typography, type scale and tokens*. https://m3.material.io/styles/typography/type-scale-tokens . **P** 18/11/2026 (browser pass): 15 baseline and 15 emphasized styles; the token value tables are collapsed on the page and were not read.
36. Google. *Material Design 3: Motion, how it works*. https://m3.material.io/styles/motion/overview/how-it-works . **P** 18/11/2026 (browser pass): physics (spring) system, expressive and standard schemes.
37. Microsoft. *Fluent 2: Typography*. https://fluent2.microsoft.design/typography . **P** 18/11/2026 (browser pass): web type ramp sizes and line heights, sentence case, avoid all caps.

Totals: 37 entries. Verified identity or text read (V or P): 37 = 100%. S: 0. U: 0. Limits: Fluent 2 shapes, material and colour pages and the M3 shape, elevation and 48 dp pages were not read, so claims about them in `styles/` are marked practitioner [F]. Books 1 to 7 are identity-verified only; the specific ideas attributed to them are general and were not re-read. Apple's JSON feed is the data source behind the HIG pages, read as text.
