# Diagnosis playbook

Use when something is "slow" and you must find why. Step 0 decides whether the evidence can be trusted; then pick the tree. Thresholds: `core-web-vitals.md`. Routines and templates: `playbooks.md`. Sources: `BIBLIOGRAPHY.md`.

## Step 0: is the evidence trustworthy

1. **Field or lab?** Field = real users (CrUX, own RUM). Lab = Lighthouse, DevTools, WebPageTest. Field sets priority, lab reproduces. Tag every number "field" or "lab".
2. **Field at p75, by device and page type.** Read p75 (not the mean) for LCP, INP, CLS, per phone vs desktop and per template (home, list, product, checkout). A site-wide origin number hides the one bad template. CrUX needs enough traffic and covers only some browsers; no CrUX does not mean fast, it means unmeasured (`core-web-vitals.md`).
3. **Which page, which metric, since when.** Ask: URL or template, metric, the date it moved, and recent changes (release, new tag, new image, CDN or region change, traffic mix such as a campaign bringing slower phones). CrUX is a 28-day window, so a fix shows up slowly; use RUM for same-day proof.
4. **Network and device profile.** What the audience really has. State the throttle used in the lab (for example CPU 4x slowdown, about 1.6 Mbit/s down, 150 ms RTT). A lab run on a fast laptop proves nothing.
5. **Sample size.** One run is noise: take the median of at least 3 (5 if possible) on an idle machine; field needs hundreds of samples per segment.
6. **Production build, same cache state.** Dev servers and warm caches mislead. Cold and warm are separate experiments.

If field is already good and only the lab score is low, say so: the lab score is not the goal.

## Worked numbers (re-do them with your own data)

- **p75 vs average.** Ten LCP samples (s): 1.2, 1.3, 1.4, 1.5, 1.8, 2.0, 2.2, 3.9, 4.6, 5.1. Mean = 2.5 s ("passes"); p75 (nearest rank, 8th value) = 3.9 s ("needs improvement"). Vitals judge p75, so the mean lies.
- **LCP budget.** Target 2.5 s. Guideline split (web.dev): first byte about 40% = 1.0 s, load delay under 10% = 0.25 s, load duration about 40% = 1.0 s, render delay under 10% = 0.25 s. A page at 4.8 s with TTFB 1.9, delay 0.8, duration 1.5, render 0.6 has its largest slice in TTFB (40%) and a load delay 3x over guideline; fix those before touching image size.
- **Bytes to milliseconds on slow 4G** (1.6 Mbit/s, 150 ms RTT): transfer time = bytes x 8 / rate. 1 MB hero = 8 Mbit / 1.6 = 5.0 s. The same image as 150 KB AVIF or WebP = 0.75 s. 300 KB of compressed JS = 2.4 Mbit / 1.6 = 1.5 s of download before parse and run (CPU 4x slower than a laptop). A new HTTPS connection costs about 2-3 RTT = 300-450 ms before the first byte: reuse connections, preconnect only to origins that matter.
- **Cache hit ratio.** Edge hit 40 ms, origin miss 400 ms. Mean latency = h x 40 + (1 - h) x 400: h=50% gives 220 ms, h=90% gives 76 ms, h=99% gives 43.6 ms. But p95 is the miss latency until h exceeds 95%: at h=90% p95 is about 400 ms. Raise the hit ratio (normalize query strings, drop cookies from cacheable routes, vary only on what changes the body) before tuning origin speed.
- **N+1.** 50 items, one 4 ms query each = 200 ms of queries plus 50 round trips; one batched query = about 6 ms. Count queries per request in the log.
- **OFFSET.** `OFFSET 5000 LIMIT 50` reads and discards 5,000 rows on every call, so page 100 costs about 100x page 1; keyset costs the same on every page.
- **Fan-out tail.** 30 parallel calls, each slow 1% of the time: 1 - 0.99^30 = 26% of requests see a slow call (`backend-latency.md`).

## Trees

Each tree: symptom, split, likely cause, how to check, fix. Change one thing, re-measure.

### LCP slow (field p75 above 2.5 s)
Split into TTFB, load delay, load duration, render delay (`core-web-vitals.md`). Find the LCP element first (DevTools, or the `web-vitals` attribution build).
- **TTFB large:** go to "Slow TTFB" below.
- **Image not prioritised (large load delay):** LCP image lazy-loaded, set by CSS background, injected by JS, or discovered late. Check the HTML source and the waterfall start time. Fix: real `<img>` in the initial HTML, no `loading="lazy"`, `fetchpriority="high"` on that one image, `preload` only when discovery is late.
- **Large load duration:** oversize image or wrong format. Check bytes against the displayed size at 2x. Fix: AVIF/WebP, `srcset` and `sizes`, CDN resizing (`playbooks.md` image pipeline).
- **Render-blocking:** big CSS or synchronous scripts before the LCP element. Check "render blocking requests" in the trace. Fix: inline critical CSS, `defer` scripts, remove unused CSS.
- **Client-side render:** the LCP element exists only after JS fetches data. Check "view source" for an empty root. Fix: render it on the server or statically; stream the shell.
- **Font:** LCP is text waiting for a web font. Fix: `font-display: swap` or `optional`, preload the one critical font, self-host, subset.

### INP poor (p75 above 200 ms)
Split the slow interaction into input delay, processing, presentation delay (`core-web-vitals.md`). Record the interaction in the Performance panel or use the attribution build to name the element and script.
- **Long tasks on the main thread (input delay):** something else is running when the user taps. Fix: split work, yield (`scheduler.yield()` where available, else `setTimeout`), move to a worker, defer non-essential work.
- **Hydration:** page is visible but the first taps wait for hydration. Fix: less client JS, server components, smaller islands, defer below-the-fold hydration.
- **Heavy event handlers (processing):** one keystroke re-renders thousands of nodes, or runs sync layout. Fix: update less (state next to where it is used), memoize rows, debounce or `useDeferredValue`, virtualize the list, batch DOM reads then writes.
- **Third-party scripts:** tag managers, chat, A/B tools running on input. Check "bottom-up by domain" in the trace. Fix: remove, load after interaction, facade (`playbooks.md` third-party governance).
- **Presentation delay:** huge DOM or layout thrash. Fix: smaller DOM, `content-visibility: auto`.

### CLS poor (p75 above 0.1)
Use the layout-shift regions in the trace to see which element moved.
- **Images or video without dimensions:** set `width` and `height` or `aspect-ratio`.
- **Late ads or embeds:** reserve a slot with a min-height from the most common size.
- **Font swap:** fallback and web font have different metrics. Fix: `size-adjust` fallback, `next/font`, or `optional`.
- **Injected banners (cookie, promo):** overlay (position fixed) or reserve space; never push content down after paint.
- **Animations:** animate transform and opacity only.

### Slow TTFB
- **Server work:** per-stage timing (`Server-Timing`, traces). Fix: remove blocking calls from render, parallelise independent fetches, cache computed fragments.
- **Cache miss:** check CDN hit ratio and `Age`/cache-status headers. Cookies, `Vary` and unique query strings make everything a miss.
- **Cold starts:** first request after idle is slow, the rest fast. Fix: keep warm, smaller bundle, region near data, or static.
- **Region:** server far from the database or the user. Check RTT between app and database; co-locate them. Never put a function in one region and its database in another.

### JS bundle too big
Run the analyzer on a production build, per route. Look for: a whole library for one function (date, charts, icons, lodash), duplicate versions, polyfills, server-only code shipped to the client, code for routes the user is not on. Fix: replace or import narrowly, dynamic import below the fold or on interaction, server components, remove dead code. Gate with a per-route ceiling in CI.

### Slow list or table rendering
Count DOM nodes and renders per interaction. 2,000 rows x 8 cells = 16,000 nodes. Fix in order: paginate or filter on the server, virtualize (render the visible 30 rows), stable keys and memoized rows, move derived state out of the list's parent, `content-visibility: auto`.

### Slow database-backed page
Count queries per request (N+1), then `EXPLAIN (ANALYZE, BUFFERS)` on realistic volume (`postgres-performance.md`). Typical: sequential scan on a large table (missing index on the filter + order columns), OFFSET pagination, `SELECT *` on wide rows, per-item queries in a loop. Query design, schema and migrations: `engineering-playbook`.

### API slow at p95/p99 while the average is fine
Per-stage p95/p99 (`backend-latency.md`): queue wait, pool wait, database, downstream calls. Look for utilization above 70-80%, a slow outlier dependency under fan-out, lock waits, GC or event-loop stalls, retries amplifying load. Fix the stage with the largest tail, not the largest mean.

### Mobile much slower than desktop
Expected gap: CPU and network. Check the split: if load duration dominates, bytes; if main-thread work dominates (long tasks, hydration), JS. Test with CPU 4x and slow 4G. Fix: ship less JS, smaller images, fewer third parties, avoid layout-heavy DOM. Compare p75 per device in CrUX before concluding.

### Regression after a release
Bisect: confirm in field (RUM by release tag) that the change is real and not traffic mix. Diff the bundle report and the waterfall between two builds, then the dependency lockfile and tag changes. Revert or flag-off the candidate and re-measure. Add a budget so it cannot happen silently.

### Third-party tag bloat
List every third-party request: bytes, main-thread time, blocking or async, owner, purpose. Remove what has no owner; load the rest after interaction or idle; self-host or proxy only if the licence allows; set a per-page budget (`playbooks.md`).

## When to stop
Field passes at p75 on the audience's profile, or the remaining slice costs more than its measured value. Write the trigger ("revisit when p75 LCP on product pages exceeds 2.5 s") instead of adding code.
