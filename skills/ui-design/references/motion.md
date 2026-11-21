# Motion

## Contents
1. Purpose
2. Durations and easing
3. What to animate
4. Reduced motion
5. Feedback and loading
6. Checklist

## 1. Purpose
Motion explains change (where did this go), gives feedback (my action registered) or guides attention. Decorative loops compete with content and distract; they also fail WCAG 2.2.2 if they move over 5 seconds without a pause control.

Microinteractions (Saffer, 2013) break a small interaction into four parts: a trigger (user or system initiated), rules (what happens), feedback (what the person perceives) and loops and modes (what changes over time or in special states). Use the parts as a checklist for any toggle, like, save or pull-to-refresh: is the trigger discoverable, are the rules simple, is the feedback proportional, and does repetition become annoying? (book; not fetched on 2026-11-15)

## 2. Durations and easing
- Micro-feedback (press, toggle, hover): 100 to 150 ms. Small transitions (menu, tooltip, chip): 150 to 250 ms. Larger transitions (sheet, page, dialog): 250 to 350 ms. Keep transitions between screens under about 300 ms to feel immediate. (practitioner ranges; not from a normative source)
- Entering items decelerate (ease-out), leaving items accelerate (ease-in), moving on screen uses ease-in-out. Avoid linear except for continuous progress. Limit the system to two or three curves defined as `cubicBezier` tokens.
- Exits are shorter than entrances.

## 3. What to animate
- Animate `transform` and `opacity` only; they avoid layout work. Animating width, height, top or left causes layout and jank (see `web-performance`).
- Do not animate in response to scroll continuously without need; avoid parallax.
- Keep animations interruptible; a new input cancels the old one.
- No flashing more than three times per second (WCAG 2.3.1).

## 4. Reduced motion
- WCAG 2.3.3 (AAA): motion animation triggered by interaction can be disabled unless essential. (w3.org/TR/WCAG22, read 2026-11-14)
- Apple, when Reduce Motion is on (HIG Accessibility, read 2026-11-14): reduce automatic and repetitive animation, including zooming, scaling and peripheral motion; tighten springs to reduce bounce; track animation to gestures; avoid animating depth changes; replace x, y, z transitions with fades; avoid animating into and out of blurs.
- Web: `@media (prefers-reduced-motion: reduce)`: remove scale, slide, parallax, autoplay and looping; keep short fades; static alternatives for animated illustrations; pause or stop autoplay video and carousels. Never convey information only by motion.
- Pattern: write the animated version inside `@media (prefers-reduced-motion: no-preference)` so the default is calm.

## 5. Feedback and loading
- Every custom button has a pressed state. An action over about 1 second shows an in-place activity indicator and, when it fits, a changed label ("Saving...").
- Use skeletons for content that arrives in place and spinners for short blocking waits; keep the final layout stable to avoid layout shift.
- Success and error appear near the action, with text, not only color or motion; announce with a live region for assistive tech (see `ux-design`).
- Haptics on touch devices pair with a visual cue, never replace it.

## 6. Checklist
- [ ] Every animation has a purpose (feedback, continuity or attention)
- [ ] Only transform and opacity; durations from tokens
- [ ] Reduced-motion path tested
- [ ] Nothing moves over 5 s without a pause control; nothing flashes
- [ ] Pressed and loading states present

## Sources
- Saffer, Microinteractions (O'Reilly, 2013), book (not fetched)
- W3C WCAG 2.2 (2.2.2, 2.3.1, 2.3.3), https://www.w3.org/TR/WCAG22/, read 2026-11-14
- Apple HIG Accessibility (Reduce Motion), https://developer.apple.com/design/human-interface-guidelines/accessibility, read 2026-11-14
- MDN prefers-reduced-motion, https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion (prior reading 2026-11-13, not re-fetched)
