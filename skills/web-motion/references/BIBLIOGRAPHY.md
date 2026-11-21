# Bibliography: web-motion

Read 20/11/2026. Status: **P** = official page opened and the relevant part read this pass; **D** = data from the official package registry or MDN browser-compat-data (the dataset behind MDN's tables), read this pass; **S** = exists, not read this pass. Nothing is quoted; ideas are restated.

## three.js
1. three.js releases. https://github.com/mrdoob/three.js/releases . **P** 20/11/2026: r187 on 30/10/2026.
2. three.js Migration Guide (wiki). https://github.com/mrdoob/three.js/wiki/Migration-Guide . **P** 20/11/2026: r178 to r188 entries read; final part of the page not read.

## CSS and browser APIs (MDN, W3C)
3. MDN. *CSS scroll-driven animations*. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations . **P** 20/11/2026 (page modified 05/10/2026).
4. MDN. *animation-timeline*. https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline . **P** 20/11/2026: Baseline 2026.
5. W3C CSSWG. *Scroll-driven Animations Module Level 1*, Editor's Draft 25/09/2026. https://drafts.csswg.org/scroll-animations-1/ . **P** 20/11/2026.
6. MDN. *View Transition API*. https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API . **P** 20/11/2026.
7. MDN. *prefers-reduced-motion*. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion . **P** 20/11/2026.
8. MDN browser-compat-data 8.1.10 (npm `@mdn/browser-compat-data`). https://github.com/mdn/browser-compat-data . **D** 20/11/2026: version numbers for animation-timeline, animation-range, View Transitions, getAutoplayPolicy, vibrate, decodeAudioData, AudioContext.
9. W3C. *WCAG 2.2* (2.2.2 Pause, Stop, Hide; 2.3.1 Three Flashes; 2.3.3 Animation from Interactions; 4.1.3 Status Messages). https://www.w3.org/TR/WCAG22/ . **S** (read 18/11/2026 for ui-design, not re-read).

## GSAP
10. GSAP docs v3. https://gsap.com/docs/v3/ . **P** 20/11/2026: v3.15.
11. GSAP standard license (Webflow). https://gsap.com/standard-license . **P** 20/11/2026.
12. GSAP. *gsap.matchMedia()*. https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/ . **P** 20/11/2026.
13. GSAP. *ScrollTrigger*. https://gsap.com/docs/v3/Plugins/ScrollTrigger/ . **P** 20/11/2026.
14. npm registry, `gsap`. https://www.npmjs.com/package/gsap . **D** 20/11/2026: 3.15.1 on 04/11/2026.

## Lottie and Rive
15. npm registry, `@lottiefiles/dotlottie-web`, `@lottiefiles/dotlottie-react`, `lottie-web`. https://www.npmjs.com/package/@lottiefiles/dotlottie-web . **D** 20/11/2026 (versions only; LottieFiles docs not read).
16. npm registry, `@rive-app/canvas`, `@rive-app/webgl2`, `@rive-app/canvas-lite`, `@rive-app/react-canvas`. https://www.npmjs.com/package/@rive-app/canvas . **D** 20/11/2026 (versions only; rive.app docs not read).

## Sound and vibration
17. MDN. *Web Audio API*. https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API . **P** 20/11/2026.
18. MDN. *Web Audio API best practices*. https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices . **P** 20/11/2026.
19. MDN. *Web audio codec guide*. https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Audio_codecs . **P** 20/11/2026.
20. MDN. *Autoplay guide for media and Web Audio APIs*. https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay . **P** 20/11/2026.
21. Chrome for Developers. *Autoplay policy in Chrome*. https://developer.chrome.com/blog/autoplay . **P** 20/11/2026.
22. WebKit. *New video policies for iOS* (2016). https://webkit.org/blog/6784/new-video-policies-for-ios/ . **P** 20/11/2026.
23. MDN. *Navigator: vibrate()*. https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate . **P** 20/11/2026.

## Feedback timing
24. Nielsen, J. *Response Times: The 3 Important Limits*. https://www.nngroup.com/articles/response-times-3-important-limits/ . **S** (classic thresholds 0.1 / 1 / 10 s; not re-read this pass).
25. Saffer, D. *Microinteractions*. O'Reilly, 2013. ISBN 978-1449342685. **S** (cited through `ui-design/references/motion.md`).

## Cross-check
26. Context7 documentation index (libraries `/mrdoob/three.js`, `/websites/gsap`). https://context7.com . **P** 20/11/2026: three.js Migration Guide and repository source (Renderer.js, WebGLShadowMap.js, RGBELoader.js) and GSAP matchMedia pages, used to correct five points in `versoes.md`.
