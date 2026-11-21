# Object storage, queues and schedules (Cloudflare R2, Upstash)

Format: **rule** · why · source `[n]` (see `BIBLIOGRAPHY.md`) · example. Numbers checked 15/11/2026.

## Cloudflare R2 (S3-compatible)

1. **Presigned URLs are bearer tokens valid 1 second to 7 days (604,800 s);** methods GET, HEAD, PUT, DELETE (not POST); they work only on the account's S3 API domain, not a custom domain `[38]`. Changing object, method or expiry invalidates them. Use minutes for private content and never log them.
2. **Browser use needs bucket CORS with exact origins;** re-test after a domain change; sign the `Content-Type` on upload URLs `[38]`.
3. **Lifecycle rules** `[39]`: objects usually go within 24 h of the expiry time; up to 1,000 rules per bucket; incomplete multipart uploads are aborted after 7 days by default. Per-customer legal retention needs your own deletion job.
4. **Jurisdiction is fixed at bucket creation** (`eu`, `fedramp`, default) plus location hints `[51]` (not re-read this pass). Data-residency rules can force another provider behind your storage interface.
5. **Pricing** `[37]`: Standard USD 0.015/GB-month, Infrequent Access USD 0.01/GB-month; class A USD 4.50 per million (IA 9.00), class B USD 0.36 per million (IA 0.90); free tier each month 10 GB, 1 M class A, 10 M class B (Standard only); egress free via the Workers API, S3 API or r2.dev. Worked example in `diagnosis-playbook.md` section 5.
6. **Keys carry tenant or owner in the path** (`tenant/<id>/<uuid>`), never a client-provided path.

## Upstash QStash (HTTP push queue and schedules)

7. **Verify every call:** the `Upstash-Signature` JWT with the current and the next signing key; verify the raw body before parsing `[41]`. The page does not describe a rotation order; the pattern in `playbooks.md` section 3 (promote "next", then re-roll) is an inference to test.
8. **Retries** `[40]`: 3 by default; delay `min(86400, e^(2.5 n))` seconds (about 12 s first, 24 h from the fifth); override with `Upstash-Retries`, `Upstash-Retry-Delay` or a `Retry-After` response header; respond **489** with `Upstash-NonRetryable-Error: true` for permanent errors (message goes to the DLQ). Handlers must be idempotent because a 502 from a waking service also triggers a retry `[9]`.
9. **A schedule is a clean way to wake a scale-to-zero service** instead of an always-on timer inside it `[18]`.

## Upstash Redis

10. **The rate-limit SDK lets requests pass when its timeout expires** `[52]` (not re-read this pass); fail-closed is your code, decided per route.
11. **Pricing** `[42]`: pay-as-you-go USD 0.20 per 100K commands, storage USD 0.25/GB (first 1 GB free per database), bandwidth free to 200 GB then USD 0.03/GB; free tier 500K commands/month, 250 MB; fixed plans from USD 10 (250 MB). Rate limiting every page view spends commands: 3 commands per check and 1 M views is 3 M commands = USD 6.00 at pay-as-you-go (assumed 3 commands per check; measure yours).
12. **Cache keys include the tenant or user for private data;** cache changes speed, never correctness; private responses never reach a shared cache.
