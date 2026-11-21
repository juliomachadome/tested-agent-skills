# JS budget, images, fonts, audio and video

## Contents
1. JS budget and bundle analysis
2. Server components and client boundaries
3. Images
4. Fonts
5. Audio and video
6. Long lists and DOM size
7. Third parties

## 1. JS budget and bundle analysis

- What counts is JS compressed on the wire and, more, parse and execution time on a weak device. Both matter for LCP (render delay) and INP (long tasks).
- Pick the reference device from your audience: platform and vendor share in your country (StatCounter), real mobile speeds, and your own RUM. A country median speed is optimistic; people are indoors, on transit, in rural areas.
- One published reference (Alex Russell, "The Performance Inequality Gap, 2026", infrequently.org, 2025-11-24; read by the input on 2026-11-12): global p75 mid-range Android on 4G, about 9 Mbps down, 100 ms RTT. To be interactive in 3 s with two connections, the critical path is roughly 2 MiB total if JS is about 15 percent of it (about 300 KiB of JS), or about 1.2 MiB if half is JS. Real-world median is about 680 KiB of JS, p75 about 1.3 MiB. Treat as orientation, not law; any single magic number ("170 KB") without device, network and page weight context is weak evidence. Use as a no-regression ceiling.
- Lab test with 4x CPU slowdown and a slow-4G or p75 profile.
- Budget per route, measured on a production build, enforced by a test that sums the gzip size of the route's script tags against a ceiling. Lower it after every cut; raise only with a written reason.
- Evaluate a dependency before installing (bundle-size services such as Bundlephobia or bundlejs), then measure after. Use the framework's analyzer (for Next.js: the built-in analyzer in recent versions, or the webpack bundle analyzer plugin; confirm with current docs) to see the import chain of a heavy module.
- Defer what is used after an action (dynamic import for modals, editors, charts); for packages with many exports (icon sets) use tree-shaking-friendly imports or the framework's package optimization option.

## 2. Server components and client boundaries (general pattern)

Rendering on the server by default sends no component JS to the browser. Add client code only on leaves that need state or events. Work that turns data into UI (syntax highlighting, markdown, charts without interaction) belongs on the server if it needs no browser API. Streaming with Suspense lets a static shell paint while per-user parts load. Exact APIs, cache directives and config flags are version-specific: read the vendor docs for the installed version.

## 3. Images

- Format: AVIF first, WebP next, JPEG/PNG last; simple icons and illustrations as SVG. Source: web.dev/articles/optimize-lcp, web.dev/learn/images.
- `srcset` plus `sizes` with a few useful widths (1x and 2x of the displayed size). Without `sizes` the browser assumes 100vw and downloads the largest candidate. Every extra width, format or quality is another variant to generate, cache and, on a paid transformation service, pay for.
- Above the fold: eager, no lazy; one or two with `fetchpriority="high"`. Below the fold: `loading="lazy"`.
- Preloading a responsive image needs matching `imagesrcset` and `imagesizes`, or it downloads twice.
- Images with small text (diagrams, screenshots) suffer from aggressive compression; check legibility on a phone before lowering quality.
- Always set dimensions or aspect-ratio (CLS).
- A URL that changes on every request (fresh signature) never hits the browser or CDN cache. See `caching-cdn-sw.md`.
- If the host bills per transformation, cap formats, widths and qualities, set long TTLs, and skip optimization for assets already small.

## 4. Fonts

Source: https://web.dev/articles/font-best-practices (read by the input 2026-11-12).
- WOFF2 only; subset to the audience alphabet (check the license allows it).
- Fewer files: system fonts where acceptable; a variable font only when it replaces several weights.
- Declare `@font-face` early; preload only the critical font because preload takes bandwidth from other resources.
- `font-display`: `swap` shows text now and may shift; `optional` never shifts but may skip the font on first visit; `fallback` is between; `block` hides text.
- Self-host: no third-party request, and a metric-adjusted fallback reduces layout shift.
- Icons as SVG, not icon fonts.

## 5. Audio and video

Sources: web.dev/articles/video-and-source-tags, /fast-playback-with-preload (read by the input 2026-11-12).
- `preload`: `none` when playback is uncertain (with a poster), `metadata` as a sane mobile default, `auto` only when play is near certain. It is a hint: Chrome forces `metadata` on cellular and `none` with data saver.
- Always a `poster` with reserved dimensions. "Facade" pattern: show the cover, mount the player on click so video does not compete with LCP.
- `<source>` elements in order of preference, each with `type`.
- Autoplay only muted with `playsinline`; weigh the data cost.
- The server must honor HTTP Range (206, `Accept-Ranges: bytes`); without it there is no seeking and iOS Safari often refuses to play. MP4 needs the `moov` atom at the start (faststart) or the player downloads most of the file before starting (practical guidance, no standard cited).
- Progressive MP4 vs HLS: a short clip at one low bitrate is simpler as progressive MP4 with faststart (no player JS, no packaging). HLS or DASH pays off for long video, live, or audiences whose bandwidth varies enough to need quality switching. Choice is market practice, not a standard. For HLS, Apple's authoring spec suggests about 6 s segments and a variant up to 192 kbit/s for cellular (not re-verified).
- Size arithmetic: size = bitrate x duration. Two minutes at 350 kbit/s is about 5 MB; at 2.5 Mbit/s about 37 MB, where a smaller variant or HLS is worth it.
- Audio: `preload="none"`, fetch the URL on tap, show loading state; iOS plays audio only after a user gesture. MP3 and AAC play everywhere; Opus is smaller but check support.
- `rel=preload as=video` has no reliable support; do not use.

## 6. Long lists and DOM size

Rendering thousands of rows hurts INP and memory. Options in order: paginate or limit on the server; virtualize (render only the visible window; mind blank flashes on fast scroll and keep overscan small); `content-visibility: auto` for off-screen sections. Source: web.dev "Virtualize large lists with react-window", "How large DOM sizes affect interactivity" (via input, 2026-11-13).

## 7. Third parties

Pixels, chat widgets, analytics and session replay run on the same main thread and are the usual INP offenders. Load them after interaction or idle, behind consent where the law requires it, and count their bytes in the budget. Measure with and without.

## Extra browser JS checks

- Moving work to a Web Worker only pays if the data crosses cheaply: structured clone copies everything (thousands of objects can cost hundreds of ms and double the memory). Transfer binary buffers (zero copy; the sender loses access) or use shared memory (needs cross-origin isolation headers).
- Allocation rate on hot paths (objects created per event or per frame) causes unpredictable garbage-collection pauses: reuse objects, avoid per-item closures in tight loops, and check the allocation timeline, not only CPU.
- Layout thrashing: interleaving layout reads and style writes in a loop forces a reflow per iteration; batch all reads, then all writes, or insert nodes through a fragment.
- A micro-benchmark proves little: engines remove unused results and optimise differently across browsers. Consume the result, warm up, test on the real target engine, and confirm the win in a profile of the real page.
- Immutability and functional helpers are fine until they sit on a hot path with large data; measure, then loosen only that spot.

## Sources

- https://web.dev/articles/optimize-lcp, /font-best-practices, /video-and-source-tags, /fast-playback-with-preload, /learn/images (input file; not re-fetched 2026-11-15)
- https://infrequently.org/2025/11/performance-inequality-gap-2026/ (input file; not re-fetched)
