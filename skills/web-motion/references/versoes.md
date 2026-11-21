# Versions, API changes and browser support

Read 20/11/2026 from official sources (URLs below and in `BIBLIOGRAPHY.md`). Only API and support changes are noted; no text copied. Re-check before relying on a number older than about three months: three.js ships roughly monthly and its WebGPU side still moves.

## three.js
Source: releases https://github.com/mrdoob/three.js/releases and Migration Guide https://github.com/mrdoob/three.js/wiki/Migration-Guide (read 20/11/2026; the guide has no page date; its last part was not read). Five points re-checked 20/11/2026 against the repository source through Context7 (library `/mrdoob/three.js`, files cited inline) and corrected below.
- Current release: **r187 (npm `three@0.187.0`), 30/10/2026**. r186 24/09/2026, r185 01/07/2026, r184 16/04/2026. The guide already lists r187 to r188 changes; r188 is not released yet.
- Pin the exact version in imports (`three@0.187.0`); examples written for older releases break silently.
- WebGPU and TSL (still changing; avoid for production unless you pin and test):
  - `PostProcessing` became `RenderPipeline` (r183).
  - `Clock` deprecated; `Timer` is in core (r179, r183).
  - Async methods (`renderAsync`, `computeAsync`, `clearAsync`, `initTextureAsync`, `hasFeatureAsync`) deprecated in r181; `renderAsync` now only awaits `init()` then calls `render()`. Initialisation happens by itself inside `renderer.setAnimationLoop()`; call `await renderer.init()` yourself only for on-demand rendering or feature detection. `waitForGPU()` removed (r181). (Context7 20/11/2026: Migration Guide 180→181 and https://github.com/mrdoob/three.js/blob/dev/src/renderers/common/Renderer.js)
  - `colorBufferType` renamed `outputBufferType` (r182).
  - TSL renames: `label()` to `setName()`, `PI2` to `TWO_PI`, `directionToColor` to `packNormalToRGB`. r187: implicit type coercion of math operands; storage structs always treated as arrays.
  - Post-processing: `AnamorphicNode` removed for `BloomNode` (r185); `DepthOfFieldNode` rewritten (r180); `GTAONode` changed in r181, r185, r188. `TiledLighting` removed for `ClusteredLighting` (r185). Premultiplied alpha changed on WebGPU (r185).
- Shadows: `PCFSoftShadowMap` is deprecated since r186 and removed in both renderers: WebGLShadowMap and WebGPU switch to `PCFShadowMap` (already soft) with a warning. Use `PCFShadowMap`. (Context7 20/11/2026: https://github.com/mrdoob/three.js/blob/dev/src/renderers/webgl/WebGLShadowMap.js and src/constants.js, dev branch; earlier note said only WebGPU removed it)
- Loaders: `HDRLoader` replaces `RGBELoader` (r180); `RGBELoader` still exists as a deprecated subclass that logs a warning, so old code runs but should move to `HDRLoader` (Context7 20/11/2026: https://github.com/mrdoob/three.js/blob/dev/examples/jsm/loaders/RGBELoader.js); `RGBMLoader` removed (r180); `USDZLoader` removed for `USDLoader` (r179); `VTKLoader` deprecated (r184); `LWOLoader`, `SVGLoader.createShapes()`, `DRACOLoader.setDecoderConfig()` deprecated (r185). `FileLoader.load()` and `ImageBitmapLoader.load()` return nothing since r184 (use `onLoad`). `FBXLoader` converts Z-up to Y-up (r184).
- Materials and light: `CubeUVReflectionMapping` removed (r187); `LightProbe` family deprecated in r188; ambient and hemisphere lights gain specular in r188. Colour management defaults unchanged since r152 (sRGB output, `ColorManagement` on).
- Other: `Source` renamed `TextureSource` (r186); `Object3D.dispose()` added (r186).
- WebGL1: WebGLRenderer is WebGL2-only since r163 (Migration Guide 162→163, confirmed 20/11/2026 through Context7; earlier note was from memory). Fallback for no WebGL2 is a static image, not WebGL1.

## CSS scroll-driven animations
Sources: MDN https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations (modified 05/10/2026), https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline (modified 16/09/2026); spec https://drafts.csswg.org/scroll-animations-1/ (Editor's Draft, 25/09/2026). Support from MDN browser-compat-data 8.1.10.
- `animation-timeline` is **Baseline 2026, newly available**. No flags: Chrome/Edge/Chrome Android 115, Safari and iOS Safari 26, Firefox 159. Same for `animation-range`.
- Values: `auto`, `none`, named timeline, `scroll()`, `view()`. Related: `scroll-timeline`, `view-timeline`, `timeline-scope`; newer trigger properties (`animation-trigger`, `timeline-trigger`) are not Baseline.
- Traps: the `animation` shorthand resets `animation-timeline`, so set the timeline after it. Feature-detect with `@supports (animation-timeline: view())`; older browsers get the final state, not a broken one.
- The spec is still a draft: keep effects simple and progressive.

## View Transitions
Source: MDN https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API (modified 28/09/2026); browser-compat-data 8.1.10.
- Same-document `document.startViewTransition()`: Chrome/Edge 111, Safari 18, Firefox 144.
- Cross-document `@view-transition`: Chrome/Edge 126, Safari 18.2, Firefox not shipped (preview only).
- Always guard (`if (document.startViewTransition)`) and skip under reduced motion.

## GSAP
Sources: npm registry; docs https://gsap.com/docs/v3/ ; license https://gsap.com/standard-license ; https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/ ; https://gsap.com/docs/v3/Plugins/ScrollTrigger/ (all read 20/11/2026).
- Current: **gsap 3.15.1, 04/11/2026**.
- License: free for commercial use under the Webflow standard license, formerly paid plugins (SplitText, MorphSVG and others) included. Not allowed in visual no-code animation builders competing with Webflow without consent; Webflow may change terms for future versions.
- Reduced motion: `gsap.matchMedia()` (since 3.11) with `(prefers-reduced-motion: no-preference)` and `reduce` branches, or the conditions object (`{ reduceMotion: "(prefers-reduced-motion: reduce)", ... }` read through `context.conditions`, e.g. `duration: reduceMotion ? 0 : 2`); animations and ScrollTriggers created inside are reverted automatically when no condition matches, and a returned function is only for extra cleanup (do not call `revert()` in it). `ScrollTrigger.matchMedia()` is deprecated since 3.11. (Confirmed 20/11/2026 through Context7, library `/websites/gsap`: https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/ and https://gsap.com/docs/v3/Plugins/ScrollTrigger/static.matchMedia()/)
- ScrollTrigger: `clamp()` in start/end (3.12+); `normalizeScroll()` moves scrolling to JS (use only to fix mobile address-bar jumps); refresh on resize is debounced 200 ms.
- No 3.12 to 3.15 changelog was found on the official site in this pass.
- Prefer native CSS scroll-driven animation where support fits; use ScrollTrigger for pinning, scrubbed timelines and older browsers.

## Lottie and Rive (package versions only; docs pages not read this pass)
From the npm registry, 20/11/2026:
- `@lottiefiles/dotlottie-web` 0.83.2 (12/11/2026); `@lottiefiles/dotlottie-react` 0.22.3 (18/11/2026). `lottie-web` 5.13.0 (21/05/2025) looks unmaintained compared with dotLottie; prefer dotLottie for new work.
- `@rive-app/canvas`, `@rive-app/webgl2`, `@rive-app/canvas-lite` 2.52.0 (19/11/2026); `@rive-app/react-canvas` 4.40.0. `canvas-lite` is the smaller runtime when you do not need text or advanced features.

## prefers-reduced-motion
MDN https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion (modified 10/06/2026): Baseline widely available since January 2020 (Chrome 74, Edge 79, Firefox 63, Safari 10.1, iOS 10.3).
