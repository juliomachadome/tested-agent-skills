# HTTP caching, CDN and service workers

## HTTP cache headers

| Resource | Header |
|---|---|
| File with a content hash in its name (JS, CSS, fonts, imported images) | `Cache-Control: public, max-age=31536000, immutable` |
| HTML and any unversioned URL | `no-cache` plus `ETag` (revalidate every time, answer 304) |
| Response with personal or paid data | `private, no-store` (or a short `private, max-age` only if safe) |
| Public API identical for everyone | short `max-age` plus `s-maxage` and `stale-while-revalidate` at the CDN |

Source: https://web.dev/articles/http-cache (fetched 2026-11-15). The page recommends one-year max-age for versioned URLs and `no-cache` plus ETag for unversioned ones; it calls `immutable` an optional extra that some browsers ignore, so never rely on it alone; it mentions `stale-while-revalidate` only briefly. The `stale-while-revalidate` and `stale-if-error` semantics are in RFC 5861 (not re-verified).

Rules:
- `public` lets shared caches (CDN) store; `private` is browser only. Getting this wrong on a user-specific response leaks one user's data to another.
- `no-cache` does not mean "do not store"; it means "revalidate before use". `no-store` means do not keep.
- Do not append changing query strings to cacheable assets: each variant is a separate cache entry and misses the CDN.
- Keep critical resources on the same origin as the HTML when possible (no extra connection setup).
- Pages that must stay bfcache-eligible should avoid `no-store` on the HTML unless required.
- On managed platforms, static and ISR cache headers are often owned by the framework; you control revalidation time. Bytes served from a public folder or a function usually count as billed transfer.

## Signed URLs and cacheability

A signed (presigned) URL with a new signature on every request is a different URL every time: the browser and the CDN never reuse the cached object, and the same media downloads again. Options, simplest first (inference, confirm in the browser Network panel; each needs a security review):
1. The client reuses the URL until it expires.
2. The server signs with the time rounded to a window so the URL repeats inside the window.
3. A worker or edge function in front of the bucket exposes a stable URL, checks a token, and returns `Cache-Control: private, max-age=N`.

For one object store (Cloudflare R2), presigned URLs last from 1 second to 7 days and work only on the S3 API domain, not on a custom domain; for custom domains the docs point to HMAC validation in the WAF or a worker with a bucket binding. Source: https://developers.cloudflare.com/r2/api/s3/presigned-urls/ (input file, read 2026-11-12; not re-fetched).

## Application caches (Redis and similar)

- Cache is the last tool, after index, query shape and HTTP cache. Each cache is another place for stale data.
- Cache-aside with a TTL always; the key contains everything that changes the response (locale, version, plan); per-user data only with the user id in the key.
- If the cache is down, the page still answers, only slower. A cache is never the source of truth.
- A remote cache in another region adds tens of ms per call; do not put it on every request without measuring. On per-command billing, every cache read and every rate-limit check costs money: count 1 to 2 commands per request in the cost per user.

## Service workers

Source: https://developer.chrome.com/docs/workbox/caching-strategies-overview (input, read 2026-11-12).

| Strategy | Use for |
|---|---|
| Cache first | hashed immutable files, fonts |
| Network first | HTML and data that must be fresh, with offline fallback |
| Stale-while-revalidate | content that tolerates a little staleness (avatars, public catalog) |
| Network only | payments, auth, anything that must not be replayed |
| Cache only | only what was precached at install |

- Cache Storage ignores `Cache-Control`: entries stay until you delete them. Version cache names and delete old ones on `activate`.
- Never store authenticated HTML, per-user API responses or signed URLs: the cache is per origin, not per user, so on a shared device it leaks.
- Enable navigation preload when the worker intercepts navigations so worker boot does not delay the HTML (web.dev navigation-preload, not re-verified).
- A badly built worker makes things slower (stale cache stuck, boot on every navigation). Minimum safe scope: offline page plus push; grow only for a measured use case.
- `skipWaiting` plus `clients.claim` switch versions immediately; test "installed app after a deploy" for real.
- iOS Safari storage is best effort: quota per origin up to about 60 percent of disk in the browser, eviction under pressure or after long non-use, persistence granted by heuristics (for example installed to the home screen). Source: https://webkit.org/blog/14403/updates-to-storage-policy/ (input, read 2026-11-12).
- Full offline for paid per-user content is expensive and risky; only with proven demand.

## Sources

- https://web.dev/articles/http-cache (fetched 2026-11-15)
- https://developer.chrome.com/docs/workbox/caching-strategies-overview, https://webkit.org/blog/14403/updates-to-storage-policy/, https://developers.cloudflare.com/r2/api/s3/presigned-urls/ (input file, read 2026-11-12, not re-fetched)
- RFC 5861 (not re-verified)
