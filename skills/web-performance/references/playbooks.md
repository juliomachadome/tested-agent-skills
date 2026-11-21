# Playbooks

Practical routines. Diagnosis comes first (`diagnosis-playbook.md`); this file is what you do once you know what to change. Deep facts live in the topic references named in each section. Sources: `BIBLIOGRAPHY.md`. Framework APIs change: check the installed version's docs.

## 1. Measurement routine

1. **Field first.** PageSpeed Insights shows CrUX p75 for the URL and origin (if eligible) above the Lighthouse run. For history and per-device data use the CrUX API (histograms and p75 for LCP, INP, CLS).
2. **Own RUM.** Add the `web-vitals` library, report `onLCP`, `onINP`, `onCLS` with the attribution build, and send route, device class, connection type and release tag with `navigator.sendBeacon`. Aggregate at p75 per route and release.
3. **Lab repro.** Lighthouse (DevTools or CLI) on a production build with CPU and network throttling; median of 3-5 runs. WebPageTest for real-device, real-network runs and filmstrips when the Lighthouse waterfall is not enough.
4. **CI.** Lighthouse CI with assertions per route (LCP, CLS, total JS bytes) on a controlled environment; a failing assertion blocks the merge. Lab thresholds are tighter than field because lab has no cache and no variance.
5. **Record** the six fields: route, tool, device and network profile, cache state, n, commit. Report format in section 9.

## 2. Performance budget and CI gate

- Choose few budgets that map to metrics: LCP, INP and CLS at p75 (field alert), JS per route in KB compressed, image bytes per page, third-party count and time, API p95, query count per request.
- Set the first ceiling from the current measurement, slightly better (not from a blog number), and lower it at each cut.
- Enforce: bundle-size test on the production build, Lighthouse CI assertions, a load test with a p95 assertion on seed data, a query-count assertion in an integration test.
- A ceiling is raised only with a written reason and an owner. Alert on field regressions per release, not on single days.

## 3. Image pipeline

- **Format:** AVIF or WebP for photos with a JPEG fallback when needed; SVG for logos and icons; no GIF for animation (use video).
- **Size:** export at the largest displayed size x device pixel ratio (2x), not the source size. A 1 MB hero costs about 5 s on 1.6 Mbit/s; the same at 150 KB costs 0.75 s.
- **Responsive:** `srcset` with width descriptors and an honest `sizes`; the browser picks. A CDN or framework image component generates variants on demand.
- **Priority:** the one LCP image gets `fetchpriority="high"` and is never lazy; if discovered late (CSS background, JS) make it an `<img>` or add a preload with matching `imagesrcset`.
- **Lazy loading:** `loading="lazy"` for images below the fold only; always with `width` and `height` or `aspect-ratio` so nothing shifts.
- **Delivery:** long `immutable` cache on hashed or versioned URLs; a signed URL that changes per request never hits a cache (`caching-cdn-sw.md`).
- **Next.js:** `next/image` handles sizing, formats and lazy loading; remote hosts need an allow-list; use its priority or preload option for the LCP image as documented for the installed version. Details: `assets-js-images-fonts.md`.

## 4. Font loading

- Self-host WOFF2, subset to the scripts you use, limit to 1-2 families and few weights; variable fonts when you need many.
- Preload only the one font used above the fold (with `crossorigin`).
- `font-display: swap` (or `optional` when layout stability matters more than the exact font); tune the fallback with `size-adjust`, `ascent-override` so the swap does not shift layout.
- Next.js: `next/font` self-hosts and sets the fallback metrics automatically. Details: `assets-js-images-fonts.md`.

## 5. Code splitting, Server Components and streaming (Next.js)

- Default to Server Components: their code is not sent to the browser and is split per route automatically. Add `"use client"` only at the leaves that need state, effects or events; every client boundary adds JS and hydration.
- Lazy-load Client Components that are below the fold or behind an interaction (`next/dynamic` or `React.lazy` with Suspense): charts, editors, modals, maps.
- Stream: wrap slow data in `Suspense` so the shell and fast parts paint first; do not block the whole page on the slowest query. Fetch independent data in parallel, not in a waterfall of awaits.
- Keep heavy libraries on the server; pass the client only serialized, minimal props (props are shipped in the page payload).
- Verify with the framework's bundle analyzer on a production build, per route. Cache and rendering options differ by version (a newer cache model exists than the one in older guides): read the docs for the installed version.

## 6. Caching strategy

| Layer | Rule |
|---|---|
| Hashed static assets | `Cache-Control: public, max-age=31536000, immutable` |
| HTML and unversioned URLs | `no-cache` plus `ETag` (revalidate, answer 304) |
| Public API, same for everyone | short `max-age`, `s-maxage` and `stale-while-revalidate` at the CDN |
| Per-user or authenticated | `private` or `no-store`; never in a shared cache or a service worker's shared store |

- **stale-while-revalidate / stale-if-error** (RFC 5861): serve stale while refreshing in the background, or when the origin fails. Good for catalogs and avatars, wrong for prices at checkout.
- **CDN:** raise the hit ratio first (normalize query strings, strip cookies from cacheable routes, small `Vary`). Purge by tag or URL on change instead of short TTLs everywhere.
- **Service worker:** cache-first for the hashed shell, stale-while-revalidate for tolerant content, network-first for fresh data; version the cache and delete old ones. Do not add one just for speed on a normal site. See `caching-cdn-sw.md`.
- Every new cache needs a TTL, a complete key (user, locale, variant) and a behaviour when it is down.

## 7. Third-party governance

1. Inventory: every third-party origin, its bytes and main-thread time, blocking or async, owner, purpose, date added.
2. Remove anything without an owner or a measured value.
3. Load the rest `async`/`defer`, after interaction or idle; use a facade for embeds (video, chat, maps) that loads the real widget on click.
4. Budget: max count and max main-thread ms per page; a new tag needs a measurement before and after, and the tag manager is audited the same way.
5. Re-audit every quarter; a tag that nobody uses still costs bytes.

## 8. Database query performance pass

1. Find the costly statements: `pg_stat_statements` ordered by `total_exec_time` and by `calls`.
2. For the candidate: `EXPLAIN (ANALYZE, BUFFERS)` on realistic volume (run writes inside a transaction you roll back). Read per-node actual time x loops, rows removed by filter, sequential scans on large tables, sorts spilling to disk, estimate vs actual row gaps (stale statistics: `ANALYZE`).
3. Index to the plan: equality columns first, then the sort column; a partial or covering index only when the plan justifies it. Check write cost and the index actually gets used.
4. Pagination: keyset on a unique ordering (for example `(created_at, id)`) instead of `OFFSET`; always `LIMIT`.
5. Kill N+1: one query with a join or `= ANY($1)`; count queries per request and assert the count in a test.
6. Select only needed columns; keep external calls out of transactions; mind pool size vs concurrency (`postgres-performance.md`, `backend-latency.md`).
7. Re-run EXPLAIN and the endpoint's p95 on the same data; keep the query test with its LIMIT. Schema design and migrations on large tables: `engineering-playbook`.

## 8b. Transport and text delivery (checklist, not verified this pass)

Compress text responses (Brotli, else gzip) at the CDN; serve over HTTP/2 or HTTP/3 and avoid domain sharding; `preconnect` only to the one or two origins needed early; consider 103 Early Hints or speculation rules for likely next pages only after the basics pass. Protocol detail: Grigorik (`BIBLIOGRAPHY.md` 1). Treat these as weak evidence until measured on your profile.

## 9. Before / after report template

```
Scope: <route or endpoint> | profile (device, CPU, network) | field or lab | cache state | n, median | date, commit
Symptom: <metric and number, who is affected>
Split: <LCP phase / INP phase / stage / plan node> -> <where the time is>
Change: <one change, file:line>
Before: <number> (n=)   After: <number> (n=)   Delta: <number, percent>
Guard: <budget or test that fails if it regresses>
Cost: <bytes, requests, CPU, spend effect>
Not measured: <what is expected only>
```
