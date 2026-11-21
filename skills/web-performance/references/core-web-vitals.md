# Core Web Vitals

Facts here age. Re-check the thresholds on web.dev before quoting them in a report.

## Thresholds (p75 of page loads, mobile and desktop reported separately)

| Metric | Good | Needs improvement | Poor | Measures |
|---|---|---|---|---|
| LCP | <= 2.5 s | 2.5 to 4.0 s | > 4.0 s | when the largest visible element renders |
| INP | <= 200 ms | 200 to 500 ms | > 500 ms | latency of click, tap and keypress across the whole visit, until the next frame is painted; the worst interaction is reported, with one outlier ignored per 50 interactions |
| CLS | <= 0.1 | 0.1 to 0.25 | > 0.25 | largest burst of unexpected layout shifts (session window: gaps under 1 s, at most 5 s long) |

A page passes only when all three are good at p75. Averages and medians hide the slow tail.
Sources: https://web.dev/articles/vitals (updated 2024-10-31), /lcp (2025-09-04), /inp (2025-09-02), /cls; read 2026-11-15.

LCP candidates: img, image inside svg, video (poster or first frame), elements with a CSS url() background (not gradients), block elements containing text. A text LCP is usually blocked by fonts and CSS.

## Field vs lab

- Field (real users) decides priority. Lab (Lighthouse, DevTools) reproduces, tests a fix before deploy, and simulates weak devices. If field is good and lab suggests a gain, the gain is optional.
- Lighthouse does not measure INP (no interaction). Use Total Blocking Time as a lab proxy and interact for real in DevTools, including during load, when the main thread is busiest.
- Why they differ: warm cache and bfcache make field faster; the LCP element changes with viewport, login and experiments; field CLS covers the whole page life while lab covers load only; a mobile page without a viewport meta has a touch delay that TBT does not show. Check these before declaring a tool wrong.
- A single Lighthouse run is noise. Take the median of several runs, one at a time on an idle machine; report "lab, n=3" when five is not feasible. Source: Lighthouse docs variability.md (not re-verified in this round).
- The Lighthouse score (0-100) is a lab aggregate and varies between runs; use it for trend, never as the goal.

## CrUX and RUM

CrUX is public field data from opted-in Chrome users: a 28-day rolling window, split by phone, tablet and desktop. It excludes Chrome on iOS, WebViews and other browsers, and it only covers public pages with enough traffic (threshold not published). Small sites, pages behind login and iPhone-heavy audiences therefore need their own RUM. Source: developer.chrome.com/docs/crux/methodology (not re-verified in this round; the knowledge input cites it as read 2026-11-12).

RUM: the `web-vitals` library, attribution build, reports which element or interaction and which phase caused the value. Send the data to the analytics you already have and sample it if the vendor charges per event. Source: github.com/GoogleChrome/web-vitals (not re-verified).

"No CrUX data" does not mean "no problem".

## LCP: four parts

Compare proportions, not absolute values: time to first byte about 40 percent, resource load delay under 10 percent, resource load duration about 40 percent, element render delay under 10 percent (optimize-lcp guide).

| Slice too big | Look at |
|---|---|
| TTFB | server, redirects, CDN miss, region, cold start |
| Load delay | resource not in HTML, no priority, wrongly lazy |
| Load duration | bytes, format, origin, CDN |
| Render delay | blocking JS or CSS, hydration, fonts |

Rules: resource in initial HTML (preload if it cannot be); `fetchpriority="high"` on one or two images; never lazy-load the LCP image; render on the server; no synchronous script in head; fewer redirects; no changing query strings on cacheable assets. Source: https://web.dev/articles/optimize-lcp (read by the input on 2026-11-12; not re-fetched).

## INP: three phases

Input delay (main thread busy), processing time (your handlers), presentation delay (render and paint). First find which interaction and which phase; CrUX gives only the number, RUM attribution gives the element and phase.

- In handlers, update the UI first and defer the rest (yield to the main thread, transitions in React).
- Tasks over 50 ms are long tasks; script parse and execution at load creates them, so less initial JS helps INP, not only LCP.
- Avoid layout thrashing (write style then read layout in the same task).
- Large DOMs make every update costly: flatten, render on demand, `content-visibility: auto` below the fold. Lighthouse warns at about 800 nodes and flags excess at about 1,400 (web.dev dom-size-and-interactivity, per input).
- Heavy hydration is the typical React culprit.

## CLS

Width and height or aspect-ratio on every image and video; reserve space for late content (banners, embeds, consent bars); animate transform and opacity only; font fallback with adjusted metrics or `font-display: optional`; keep pages bfcache-eligible (no unload handlers, careful with no-store on HTML). Lab CLS covers load only: scroll and interact before saying it is zero.

## Sources

- https://web.dev/articles/vitals, /lcp, /inp, /cls (fetched 2026-11-15)
- https://web.dev/articles/optimize-lcp, /optimize-inp, /optimize-cls, /lab-and-field-data-differences (input file, read 2026-11-12, not re-fetched)
- https://developer.chrome.com/docs/crux/methodology (not re-verified)
- https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md (not re-verified)
