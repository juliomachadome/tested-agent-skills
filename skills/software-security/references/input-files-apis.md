# Input, files, SSRF, signed URLs, rate limits and API protocols

Format: **rule** · why · source id (see `sources.md`) · example.

## 1. Injection sinks

1. **Every sink has its own encoding; validate early, encode at the sink.** SQL: parameterized queries only (no string-built raw queries). HTML: framework escaping; raw HTML insertion only after a sanitizer with an allowlist. Shell: no shell; pass an argv array, put `--` before user values, allowlist hosts and formats. Path: build from server data; reject `..`, absolute paths, and resolve then confirm the prefix. Log: strip CR/LF, log structured JSON. · W1 A05, W10, W3 V5 (5.3.2)
2. **Model output is untrusted input.** Validate it with a schema before it reaches a function, a query, a URL or HTML. Prompt-injection defenses belong to `llm-engineering`. · W1 A05 (by class)
3. **Third-party API responses are untrusted too** (payment, email, validation APIs): check type and size, set a timeout, do not follow redirects blindly. · W2 API10
4. **Validation lives on the server; client validation is UX.** · W3 V2 (2.2.2)

## 2. SSRF (API7:2023; mapped to A01 in the Top 10:2025)

1. **Do not accept a full URL from the user for a server-side fetch.** Accept an identifier and build scheme, host and path yourself from an allowlist. · W8
2. **Disable redirect following in the HTTP client used for those calls.** · W8
3. **If the destination must be arbitrary (avoid it):** only `http`/`https`; resolve DNS; check every A/AAAA record against private and metadata ranges (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16 including 169.254.169.254, ::1, fc00::/7, fe80::/10); connect to the validated IP with no second resolution. A blocklist is the last resort. · W8
4. **Media import by link (video/audio downloaders):** exact host allowlist, normalized URL, restricted extractors, `--` before the URL, egress filtering in production. · W8, W3 V5

## 3. File upload

1. **Allowlist extensions; do not trust the client `Content-Type`; check the file signature too (alone it is not enough); generate the stored name server-side; limit size including decompressed size; store on another host (bucket) with authorization for read and write.** Avoid accepting archives. · W9, W3 V5 (5.2.1 to 5.2.3)
2. **Re-encode user images to an allowed format and strip metadata** (EXIF location is personal data). · W9, W3 V14 (14.2.8)
3. **Fix `Content-Disposition` and ignore or sanitize the original filename.** · W3 V5 (5.4.1)
4. **Uploaded files are never executable on the server; parsers run isolated; extracted text is hostile data.** · W3 V5 (5.3.1)
5. **Per-user quota on uploads and on expensive processing** (transcoding, OCR, transcription): cost is an attack surface. · W3 V5 (5.2.4), V2 (2.4.1)
6. **Proportion:** a product where only the admin uploads does not need antivirus or content disarm; it needs strong admin auth and server-generated keys. Untrusted-public uploads of PDF/Office need sandboxed parsing and, where justified, antivirus/CDR. · W9

## 4. Signed URLs and paid media

1. **A signed URL is a bearer token:** whoever has it gets the object until it expires. Do not log it whole; do not put it in process argv. · W42
2. **Short life:** S3-style presigned URLs can last 1 second to 7 days; for paid content use minutes. Already-issued URLs cannot be revoked; short life is what limits damage. Changing object, method or expiry breaks the signature (403). · W42
3. **Sign the `Content-Type` for direct uploads** so a different type fails. Configure bucket CORS with exact origins if the browser fetches the URL. · W42
4. **Order of checks before signing:** authenticate (401) → validate id format (400) → entitlement: purchase and release date (403/409) → quota, failing closed (429) → read the object key from the database, never from the request → sign short, log the issuance, return only the URL. · W2 API1, API3, API4, API6
5. **Per-user quota (per day and per burst) and an issuance log** are the control against mass copying with a paid account. Per-buyer watermarks deter and trace leaks but do not prevent copying, and a watermarked copy contains personal data (retention and deletion apply). · W2 API6
6. **Public pages cannot be protected by signed URLs:** use rate limits, bot traps and monitoring, and accept that public HTML is copyable. · W2 API6

## 5. Rate limits and resource consumption

1. **Limit per IP and per account on costly or sensitive routes:** login, email send, checkout, media issuance, search, export, AI calls. · W2 API4
2. **Know your limiter's failure mode.** E.g. the Upstash rate limiter lets the request pass when its timeout (default 5 s) expires; failing closed is your code. Decide per route what happens when the store is down: closed for paid-content issuance and email sending; open or in-memory for cheap reads. · W43, W1 A10
3. **Algorithm trade-off:** fixed window is cheapest and lets a burst through at the boundary; sliding window fixes that at a higher cost; token bucket allows an initial burst. · W43
4. **In-memory limits are per process:** with N replicas the effective limit is N times higher. · W46 (processes)
5. **Client IP comes from the header your edge proxy guarantees,** not from a raw `X-Forwarded-For` sent by the client. · W6
6. **Limit the business flow, not only the endpoint** (many pending orders, many codes requested, card testing). · W2 API6

## 6. GraphQL and WebSocket resource limits

1. **GraphQL: limit query depth and amount, paginate, set application-level timeouts per query and resolver, and consider query cost analysis with a maximum cost.** Depth and amount are unlimited by default. · W14
2. **GraphQL batching enables brute force in one request** (many login mutations in one array or alias set): rate-limit by operation count, not by HTTP request. Disable introspection, verbose errors and the IDE in production unless deliberately public. · W14
3. **WebSocket: validate every message with a schema, cap message size (64 KB or less is a common starting point), rate-limit messages per connection and per user, cap connections per user.** HTTP access logs only see the upgrade request: log connection, auth events, validation failures and limit triggers yourself. · W13
