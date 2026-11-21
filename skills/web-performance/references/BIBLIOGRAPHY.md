# Bibliography: web-performance

Checked 18/11/2026. Status: **V** = identity (title, publisher, year; authors where the catalogue record lists them) matched to the ISBN in OpenLibrary (`https://openlibrary.org/isbn/<isbn>.json`) this pass; **P** = official page opened and the relevant text read this pass (for a paper, the Crossref record: title, authors, venue, year; no full text); **S** = exists, text not read; **U** = unverified. Nothing is quoted; ideas are restated. Web pages change: thresholds and APIs must be re-checked before quoting them. The older per-file source lists inside the other references keep their own read dates.

## Books
1. Grigorik, I. *High Performance Browser Networking*. O'Reilly, 2013. ISBN 978-1449344764. **V**; **P** for the free online edition https://hpbn.co/ (author credit and table of contents read; chapters not read). Supports: latency vs bandwidth, TCP and TLS cost, mobile networks, HTTP/2; the bytes-to-milliseconds arithmetic in `diagnosis-playbook.md`.
2. Souders, S. *High Performance Web Sites*. O'Reilly, 2007. ISBN 978-0596529307. **V** (author per catalogue authors record). Supports: most end-user time is front-end time; fewer requests, caching, resource ordering. Dated on specifics (HTTP/1.1 era); the principle stands.
3. Wagner, J. *Web Performance in Action*. Manning, 2017 (catalogue year). ISBN 978-1617293771. **V** (author per catalogue authors record). Supports: image formats and delivery, font loading, JS delivery, caching in practice (`playbooks.md` image pipeline). Tool advice is dated.
4. Winand, M. *SQL Performance Explained*. Markus Winand, 2012. ISBN 978-3950307825. **V**. Supports: index column order, seek (keyset) pagination, why OFFSET is slow (`playbooks.md` database pass).
5. Gregg, B. *Systems Performance*, 2nd ed. Pearson, 2020. ISBN 978-0136820154. **V** for title, publisher, year (the catalogue record lists no author; author per the cover, not re-checked). Supports: USE method, saturation, methodology for finding a bottleneck.
6. Beyer, B., Jones, C., Petoff, J., Murphy, N. R. (eds). *Site Reliability Engineering*. O'Reilly, 2016. ISBN 978-1491929124. **V** (editors per the catalogue statement). Supports: percentiles, SLOs, golden signals.

## Papers
7. Dean, J., Barroso, L. A. The Tail at Scale. *Communications of the ACM* 56(2), 74-80, 2013. https://doi.org/10.1145/2408776.2408794 . **P** (Crossref record: title, authors, venue, year, pages; landing page only, full text not read). Supports: tail amplification under fan-out, hedged requests (`diagnosis-playbook.md` API p95/p99).
8. Little, J. D. C. A Proof for the Queuing Formula: L = lambda W. *Operations Research* 9(3), 383-387, 1961. https://doi.org/10.1287/opre.9.3.383 . **P** (Crossref record; landing page only). Supports: concurrency = arrival rate x latency, pool sizing.

## Core Web Vitals and measurement (web.dev, Chrome)
9. web.dev, *Web Vitals*. https://web.dev/articles/vitals . **P** 18/11/2026: p75 of page loads, split by mobile and desktop, as the pass rule; all three metrics must pass.
10. web.dev, *Largest Contentful Paint (LCP)*. https://web.dev/articles/lcp . **P** 18/11/2026: definition and thresholds.
11. web.dev, *Interaction to Next Paint (INP)*. https://web.dev/articles/inp . **P** 18/11/2026: good at or below 200 ms, poor above 500 ms, at p75.
12. web.dev, *Cumulative Layout Shift (CLS)*. https://web.dev/articles/cls . **P** 18/11/2026: definition and thresholds.
13. web.dev, *Optimize Largest Contentful Paint*. https://web.dev/articles/optimize-lcp . **P** 18/11/2026: four LCP subparts with guideline shares (about 40% first byte, under 10% load delay, about 40% load duration, under 10% render delay).
14. web.dev, *Optimize Interaction to Next Paint*. https://web.dev/articles/optimize-inp . **P** 18/11/2026: input delay, processing duration, presentation delay.
15. web.dev, *Optimize Cumulative Layout Shift*. https://web.dev/articles/optimize-cls . **P** 18/11/2026: causes (images without dimensions, late content, fonts, animations) and fixes.
16. web.dev, *Optimize long tasks*. https://web.dev/articles/optimize-long-tasks . **P** 18/11/2026: yielding to the main thread, splitting tasks.
17. web.dev, *Optimize resource loading with the Fetch Priority API*. https://web.dev/articles/fetch-priority . **P** 18/11/2026: `fetchpriority` high or low as a hint.
18. web.dev, *Prevent unnecessary network requests with the HTTP Cache*. https://web.dev/articles/http-cache . **P** 18/11/2026: versioned URLs with long max-age, revalidation for unversioned URLs, `immutable` as optional.
19. web.dev, *Best practices for fonts*. https://web.dev/articles/font-best-practices . **P** (page opened, title and fetch confirmed; claims in `playbooks.md` font section also rest on entry 24).
20. web.dev, *Why lab and field data can be different*. https://web.dev/articles/lab-and-field-data-differences . **P** (page opened; navigation and lead text read).
21. Chrome for Developers, *CrUX methodology*. https://developer.chrome.com/docs/crux/methodology . **P** 18/11/2026: eligibility needs a publicly discoverable, sufficiently popular page or origin; the exact threshold is not disclosed.
22. Chrome for Developers, *CrUX API*. https://developer.chrome.com/docs/crux/api . **P** 18/11/2026: histograms with three bins and p75 for LCP, CLS, INP; percentiles are synthetic values.
23. GoogleChrome, *web-vitals* library. https://github.com/GoogleChrome/web-vitals . **P** 18/11/2026: `onLCP`, `onINP`, `onCLS`, and the `web-vitals/attribution` build.
24. GoogleChrome, *Lighthouse CI*. https://github.com/GoogleChrome/lighthouse-ci . **P** 18/11/2026: running, saving and asserting Lighthouse results in CI.

## Platform references (MDN, Next.js, PostgreSQL, RFC)
25. MDN, *Performance APIs*. https://developer.mozilla.org/en-US/docs/Web/API/Performance_API . **P** 18/11/2026: PerformanceObserver, marks and measures, event timing entries.
26. MDN, *HTTP caching*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching . **P** (page opened and title confirmed; directive semantics used from entry 18 and 32).
27. MDN, *rel="preload"*. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload . **P** 18/11/2026: `as` is required, examples for style and script.
28. MDN, *HTMLImageElement.fetchPriority*. https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/fetchPriority . **P** 18/11/2026: values high, low, auto.
29. Next.js, *Image Optimization*. https://nextjs.org/docs/app/getting-started/images . **P** (page opened; remote patterns and dimensions read; option details such as the priority/preload prop live in the API reference, **not read**: check the installed version).
30. Next.js, *Font Optimization*. https://nextjs.org/docs/app/getting-started/fonts . **P** 18/11/2026: `next/font` self-hosts and avoids layout shift.
31. Next.js, *Caching and Revalidating (Previous Model)*. https://nextjs.org/docs/app/guides/caching . **P** (page is labelled the previous model, so a newer cache model exists; `fetch` cache option semantics read; use the docs of the installed version).
32. Next.js, *How to lazy load Client Components and libraries*. https://nextjs.org/docs/app/guides/lazy-loading . **P** 18/11/2026: Server Components are code split by default; `next/dynamic` and `React.lazy` with Suspense for Client Components.
33. PostgreSQL, *Using EXPLAIN*. https://www.postgresql.org/docs/current/using-explain.html . **P** 18/11/2026 (version 18 docs): ANALYZE implies BUFFERS, buffers counted per node including children.
34. PostgreSQL, *pg_stat_statements*. https://www.postgresql.org/docs/current/pgstatstatements.html . **P** 18/11/2026: `calls`, `total_exec_time`, per-statement counters.
35. Winand, M. *We need tool support for keyset pagination* (use-the-index-luke.com). https://use-the-index-luke.com/no-offset . **P** 18/11/2026.
36. Nottingham, M. RFC 5861, HTTP Cache-Control Extensions for Stale Content. https://www.rfc-editor.org/rfc/rfc5861 . **P** 18/11/2026: defines `stale-while-revalidate` and `stale-if-error`.

## Field statistics
37. HTTP Archive, *Web Almanac 2025, Performance*. https://almanac.httparchive.org/en/2025/performance . **P** 18/11/2026: share of sites with good Core Web Vitals rose to 48% on mobile and 56% on desktop in 2025 (44% and 55% in 2024). Use as orientation, not as a target.
38. Sentry docs, Release Health: https://docs.sentry.io/product/releases/health/ **P** (read 18/11/2026). Supports: crash-free sessions/users, adoption.
39. Sentry docs, JavaScript source maps: https://docs.sentry.io/platforms/javascript/sourcemaps/ **P** (read 18/11/2026); release matching and public-hosting security not covered by the page.
40. Sentry docs, Session Replay privacy: https://docs.sentry.io/platforms/javascript/session-replay/privacy/ **P** (read 18/11/2026).
41. OpenTelemetry docs, JavaScript browser getting started: https://opentelemetry.io/docs/languages/js/getting-started/browser/ **P** (read 18/11/2026); CORS not covered.
42. GoogleChrome/web-vitals README: https://github.com/GoogleChrome/web-vitals **P** (read 18/11/2026); p75 guidance not on the page.
43. Google SRE book, "Monitoring Distributed Systems": https://sre.google/sre-book/monitoring-distributed-systems/ **P** (read 18/11/2026). Supports: golden signals, alert design.

Totals: 43 entries. V or P: 43 = 100.0% (V: 6; P: 31). Seen but text unread (S): 0. Unverified (U): 0, but P entries 7, 8, 19, 20, 26, 29 and 31 are page-opened or landing-page level only, as noted. Not opened this pass: the full text of books 1-6 and of papers 7-8.
Added 18/11/2026 (6 entries): 0 S.
