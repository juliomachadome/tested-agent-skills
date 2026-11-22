---
name: web-motion
description: "Use when a web page or web app needs movement or sound, even for a short question - an animated landing page or hero, animation on scroll (scroll-driven CSS, ScrollTrigger), an interactive explainer or step-through diagram, a micro-interaction (button press, toggle, add-to-cart), animated SVG, canvas, Lottie or Rive, a three.js or WebGL scene, page or view transitions, interface sounds (click, success or error sounds, a mute toggle) or vibration. Examples - \"make this hero feel alive without hurting load time\", \"animate the steps as the user scrolls\", \"should I use three.js or CSS for this\", \"add a subtle click sound with a mute toggle\". Picks the lightest tool, keeps motion purposeful, pausable and reduced-motion safe, and checks it in a browser. Not for colours, type and tokens (ui-design), flows and accessibility (ux-design). Not for native iOS/Android apps, Expo or React Native (mobile-app-engineering). Not for form and submit states (ui-design)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Web motion

Motion shows change; it is not decoration. The screen must work standing still; movement comes last, where it explains something or confirms an action. Durations, easing and micro-interaction timing belong to `ui-design/references/motion.md`: read it, do not restate it.

## Precedence
1. Project design system and motion tokens (DESIGN.md, tokens, components, CLAUDE.md/AGENTS.md).
2. `ux-design`: which feedback and states, flow, accessibility.
3. `ui-design`: how each state looks; durations and easing.
4. An explicit aesthetic direction in the brief.
5. This skill: how it moves and with which tool.
Add motion only after the static screen works: content, layout, states and focus correct with animation off.
Layout, spacing and visual finish belong to `ui-design`: this skill never decides button width, the gap between fields or card styling; it only moves what ui-design laid out.
Before writing code for an animation library (GSAP, three.js, Lottie, Rive, Motion), read its current docs (Context7 when connected, else the official site) instead of memory; pin the version you read.

## 1. Tool selector (lightest first; climb only on the signal)
1. **CSS** - transitions, `@keyframes`, scroll-driven animation (`animation-timeline`), View Transitions. Default for state changes, reveals, hovers. Climb for path drawing, morphing or many coordinated parts.
2. **Animated SVG** - stroke drawing, icon morphs, diagrams with independent parts (CSS or Web Animations API). Climb for hundreds of objects or per-pixel work.
3. **Canvas 2D** - particles, simulations, data redrawn every frame. Climb when a designer hands over a timeline you should not rebuild by hand.
4. **Lottie or Rive** - designer-authored vector animation; Rive when it reacts to input. Check file weight first.
5. **three.js** - only when depth is the content: an object the user rotates, spatial data, a scene that explains what 2D cannot.
**No 3D** for background effects, logo spins, "premium feel", text-heavy pages, or low-end phones and slow networks; a still image or short video usually wins. GSAP or Motion help with complex sequences at any step; a library is not a step. Versions and support: `references/versoes.md`.

## 2. Landing page
- One orchestrated moment at the top, done in about a second; the rest quiet: at most one short reveal per section, once, no loops.
- Nothing delays the top: hero text and image render without JS; heavy players load after first paint or on interaction, behind a same-size static poster (no layout shift).
- The CTA is visible and usable before and during the animation. No scroll-jacking, no parallax on body text.

## 3. Explanation
- Motion answers a user action (Next, slider, click on a part) and shows what changed; it never plays by itself.
- Draw the settled frame for each step before animating. Keep the changed part recognizable at the mobile viewport and show its new position, shape, or state. When geometry alone is ambiguous, use a local outline, pointer, or short label.
- For mechanical diagrams, mark the fixed parts, pivots, and contact points first. Plot the moving part's free end in each settled pose and check which side of the pivot and base it lands on. A brace or latch must meet the part it supports or locks. Draw the poses directly if a rotation or a chain of transforms makes the geometry hard to verify.
- Render one pose per step. If several SVG groups share a diagram, explicitly hide inactive groups with CSS or an SVG display attribute. Inspect the pixels after stepping to confirm the old pose disappeared. Keep callout text clear of the moving geometry and inside the frame at the narrowest width, or put it in the step caption.
- When a diagram teaches the step, give it an accessible name or description that identifies the part and its current state. Update it when the illustration changes. Add a visible caption if it clarifies details that are hard to see.
- Text and the settled frame must carry the meaning with animation off. If JavaScript drives the explainer, put the complete instructions in the initial HTML so they stay readable without it. Provide keyboard-reachable previous, next, and restart controls and announce step changes (`aria-live="polite"`). Never auto-advance faster than reading.

## 4. Feedback in motion
- Respond to a press within 100 ms (pressed state on pointer down, not on the server reply).
- Form states, loading and submit belong to `ui-design` and `ux-design`.

## 5. Sound and vibration (only when asked)
- Never on load or by itself; only after a user action.
- Short, quiet, with a visible mute control that is remembered; respect silent mode and autoplay policy.
- Never the only signal of anything.
- Vibration only on phones that support it, only for confirmation or error; feature-detect, fail silently.
- Formats, preloading, Web Audio, autoplay: `references/som.md`.

## 6. Fixed rules
- Animate only `transform` and `opacity`; never width, height, top, left or shadows in a loop.
- Pause off screen (IntersectionObserver) and on `visibilitychange`.
- `prefers-reduced-motion: reduce`: write motion inside `no-preference`; when reduced, instant change or short fade, no loops or autoplay. Check it in JS too for canvas, WebGL, Lottie, GSAP.
- No WebGL or context lost: show a static image or the 2D version, never a blank box.
- Budgets: 16 ms per frame, no long tasks during interaction; motion weight about 50 KB gzipped for CSS/SVG work, about 200 KB for a Lottie/Rive player plus file; three.js only with a measured reason. Measure with `web-performance`.
- Moving over 5 s needs pause (WCAG 2.2.2); nothing flashes over 3 times a second.

## 7. Default style
Sober and neutral: short distances (8 to 24 px), opacity plus small translate or scale (0.96 to 1), the project's easing. No bounce, glow, gradient sweeps, confetti, typing effects, cursor trails or floating blobs unless the brief asks.

## 8. Before delivering
Open it in a browser (headless is fine):
- [ ] Screenshots at first paint, mid-animation and settled: nothing overlaps, clips or jumps.
- [ ] No console errors.
- [ ] Reduced motion emulated: content complete, nothing loops.
- [ ] Explainers: at mobile width, cover the step title and identify the changed part in each settled frame. For mechanical diagrams, trace the pivot and contact points, and check that the moving piece stays inside the frame without passing through fixed parts. Verify that its accessible name or description matches the visible pose after each step. Disable JavaScript and read every instruction.
- [ ] Fallback shows without WebGL or JS.
- [ ] Console has no errors on the fallback path too (WebGL disabled).
- [ ] Canvas and 3D: if the reanimate skill is installed in the project, record our page with the virtual clock and GPU trace and check in numbers: draws while the scene is still (expected 0), draw calls per frame, and the animated values against the motion table. Pass the options directly in the command and fit curves only from the trigger.
- [ ] Sound off: every state still clear.
- [ ] 390 px wide; dark theme too only if the project has one or the brief asks (unsure: ask; never assume).
Report what was checked and what was not.

## References
- `references/versoes.md` - three.js, scroll-driven CSS, View Transitions, GSAP, Lottie, Rive: versions, API and support, dated.
- `references/feedback.md` - micro-interaction and state patterns with durations.
- `references/som.md` - Web Audio, formats, preloading, autoplay, vibration.
- `references/BIBLIOGRAPHY.md` - sources.
