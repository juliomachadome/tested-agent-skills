# Diagnosis playbook: symptom, likely cause, safe check, fix, proving test

Use it top-down. Step 0 first: a wrong picture of what is exposed makes every branch meaningless. Evidence tags: **[C]** standard or vendor doc, **[M]** serious but single or dated, **[F]** practitioner judgment, **[X]** myth. Numbers in brackets (B#) are `BIBLIOGRAPHY.md` entries. Rules of engagement for every "how to confirm": use your own test accounts and a local or staging copy; read-only against production, only with the owner's explicit order; never use real users' data as the proof; stop at the first proof of access, do not download more. Nothing here is copied from a source; ideas are restated.

## Step 0: what is exposed and can we trust the picture?
| Question | How to get it | If unknown |
|---|---|---|
| What is reachable from the internet | route list from the framework, hosting config, DNS records, storage buckets, preview URLs, admin and debug paths, server actions, webhooks, cron endpoints | list from code and from the platform dashboard; assume anything undocumented is reachable |
| Data classes | personal data, health or financial data, credentials, paid content, tenant data, secrets; one line each with where stored | treat as personal data until shown otherwise |
| Auth model | cookie session, JWT, API key, magic link, OAuth; who issues, who verifies, where verified (edge, route, database) | read the code path of one real request, do not trust the diagram |
| Tenancy | one tenant per row, per schema, per database; where the tenant id comes from | follow `tenant_id` from login to the SQL |
| Recent changes | last releases, migrations, new dependencies, new integrations, new env vars, people who left | diff the last 30 days; most incidents follow a change |
| Logs and retention | what is logged (auth, authorization failures, admin actions), where, how long, who can read them | if there are none, say "cannot prove or rule out past abuse" and add logging first |
| Environment | is the symptom in production, staging or local; same config? | reproduce in staging, or on a copy |
Severity after Step 0: Critical (other users' or tenants' data, paid content free, exposed live secret, auth bypass), High (exploitable with effort or a paid account, abuse that costs money), Medium (missing defence a likely change turns High), Low (hardening). [C] B7, B9

## Tree A: a user can see another user's data (IDOR/BOLA, missing RLS or tenant check)
| Likely cause | Safe check | Fix | Test that proves it |
|---|---|---|---|
| Lookup by id with no owner filter (`findUnique({ id })`) | two test users A and B; as B request A's object id; compare status and body | filter by the verified identity inside the query; foreign id returns the same 404 as a missing one | integration test: B asks for A's id, expect 404 and no body fields |
| Tenant or user id taken from the request body, query or `user_metadata` | send a modified `tenant_id`; inspect the JWT claims you can edit | derive tenant from the verified token or the database; ignore the body value | test posting another tenant id: the row is written to the caller's tenant |
| RLS off, no `TO`, permissive extra policy, `USING (true)`, view without `security_invoker`, `SECURITY DEFINER` function callable by `anon` | as `anon` and as user B run a select through the real API with the publishable key; check grants and policies with a catalog query | enable RLS, revoke default grants, one policy per command with `TO` and `WITH CHECK`, `security_invoker` on views, `REVOKE EXECUTE FROM PUBLIC` | pgTAP or script: A sees A's row and not B's, B cannot update or insert into A; both presence and absence asserted |
| Service-role key used on a user request, so RLS is skipped | grep which client each route builds; check whether the user token is attached | use the user-scoped client for user requests; service key only in jobs, with an explicit filter | test with a user token for a foreign id through that route |
| Endpoint returns the whole row (BOPLA/mass assignment) | compare the response fields with what the screen needs; try writing `role` or `is_admin` | return a DTO; allowlist writable fields | test: PATCH with `role` is ignored or 400 |
| Cache or search index keyed without tenant | request the same cached URL as two users | include the tenant in the key; do not cache authenticated responses publicly | test: A's cached response is never served to B |
Worked check: Next.js route `GET /api/orders/[id]` doing `supabase.from('orders').select('*').eq('id', id).single()` with the service client returns any order. Fix: user-scoped client plus `.eq('user_id', session.user.id)` and RLS as the second wall; a page or proxy check does not protect the route (B48). [C] B7, B9, B18, B24, B46

## Tree B: account takeover (fixation, weak reset, credential stuffing, no MFA or rate limit)
| Symptom or cause | Safe check | Fix | Test |
|---|---|---|---|
| Session id unchanged after login | log in on a test account and compare `Set-Cookie` before and after | regenerate the session id on login and privilege change; invalidate the old one | test: pre-login cookie is rejected after login |
| Reset token guessable, reusable, long-lived, in the URL logged by third parties, or accepted for any account | request a reset for a test account; read the token format, try reuse and an expired one | random token, single use, short life, stored hashed, bound to the user; reset page sends `Referrer-Policy: no-referrer`; no auto-login; revoke sessions after reset | tests: reuse fails, expired fails, token of user A cannot reset B |
| Reset or login answers differ for known and unknown emails | compare status, text and response time for a known and a random address | same response and path; send mail asynchronously | test compares both responses |
| Credential stuffing (many logins from many IPs, low success rate each) | login log: failures per account and per IP per hour, share of unknown emails, user-agent clusters | per-account throttling with backoff (not lockout that lets anyone deny the owner), breached-password check, MFA on risk, bot challenge after signals | test: N+1 wrong passwords for one account slows the next attempt, and the real owner can still log in |
| No MFA on admins or sensitive accounts | list admin accounts and their factors | phishing-resistant MFA (passkeys, WebAuthn) for admins; offer MFA to users | test: admin route requires the second factor |
| Email or phone change without re-authentication | change email on a test account with only a session | require recent authentication, notify the old address | test: change without recent auth is refused |
Arithmetic for stuffing: 10 million attempts at 0.5% success is 50,000 accounts; a per-IP limit of 5 per minute is defeated by 2,000 rented addresses at 10,000 attempts per minute, so limit per account and add breached-password screening. [M] B22, B33 (NIST: 15-character single-factor passwords, no forced rotation, blocklist), B11, B12, B13, B52

## Tree C: XSS found
| Likely cause | Safe check | Fix | Test |
|---|---|---|---|
| Unescaped user content in HTML, `dangerouslySetInnerHTML`, `innerHTML`, markdown or rich text without a sanitizer | in a test account inject a harmless marker (`<b>probe</b>`, not a payload that sends data anywhere) and see if it renders as markup | encode at the output for its context; use framework escaping; sanitize allowed HTML with a maintained allowlist sanitizer; avoid unsafe sinks | unit test with the marker: output is escaped; E2E check that no markup appears |
| DOM sink fed by `location`, `postMessage` or storage | review sinks (`innerHTML`, `document.write`, `eval`, `href` with `javascript:`) | safe sinks (`textContent`), validate URL schemes | test with a `javascript:` URL: it is rejected |
| Stored XSS via uploaded SVG or HTML served from your origin | upload a harmless SVG with a marker and open the stored URL | serve uploads from another domain with `Content-Disposition` and `nosniff`; re-encode images | test: uploaded file is served with download disposition |
| Session theft possible | check that the session cookie is `HttpOnly`; check where tokens are stored | `HttpOnly` cookie, no tokens in `localStorage`; CSP as defence in depth (report-only first) | test reads `document.cookie` and finds no session |
XSS defeats CSRF defences and token stores, so close it before tuning anything else. [C] B19, B20, B13, B14, B43

## Tree D: SSRF from a URL fetcher, webhook sender or image proxy
| Likely cause | Safe check | Fix | Test |
|---|---|---|---|
| Server fetches any user-supplied URL | in staging point it at a local listener you control and at `http://127.0.0.1` and the cloud metadata address; never probe real internal systems | accept an identifier, build the URL from an allowlist; if a free URL is unavoidable: resolve DNS, block private, loopback and link-local ranges (also IPv6 and IPv4-mapped forms), connect to the validated IP, no redirects, short timeout and size limit, egress firewall; require IMDSv2 | tests: private, loopback, metadata, redirect-to-private, DNS name that resolves to private are all refused |
| Redirect or DNS rebinding bypasses the check | a host you control that redirects or flips its DNS answer, in staging | disable redirects; validate and connect with the same resolved address | test with a rebinding stub |
| Webhook URL registered by customers | register your own listener URL; check retries, headers, body leakage | same controls; sign outgoing events; do not echo responses back | test: private target refused at registration and at delivery |
[C] B15, B9 (API7), B7 (SSRF is mapped under A01 in the 2025 list)

## Tree E: a secret leaked (repo, logs, client bundle)
Order is fixed: revoke, replace, redeploy, verify, remove, audit. A restart or deleting the commit revokes nothing. [C] B17, B49
| Where | Safe check | Fix | Test |
|---|---|---|---|
| Repo or git history | secret scanner on history and on the current tree; note the first commit and who had access | rotate at the provider first; then scrub if worth the cost; read the provider's usage log for the exposure window | scanner passes in CI; the old key returns 401 |
| Logs, error pages, support tickets | search logs for key prefixes and `Bearer`, `postgres://`, `sk_` patterns | redact at the logger; rotate; shorten retention | test that a logged request header is masked |
| Client bundle (`NEXT_PUBLIC_*`, `EXPO_PUBLIC_*`, source maps) | search the built output, not the source | move the call server-side; restrict what must remain public; delete public source maps | build-time check that fails on secret patterns in output |
| Unknown exposure | assume used; list what the key could reach | least-privilege replacement, one key per service and environment | the new key cannot do what the old one could |
If personal data was reachable, start the legal clock (`playbooks.md` 7).

## Tree F: webhook spoofing (no signature, no timestamp check, replay)
| Cause | Safe check | Fix | Test |
|---|---|---|---|
| Handler parses JSON and trusts it | post a fake event with a wrong signature to staging; if it is processed, it is exploitable | verify the signature over the raw body with the provider library before parsing; refuse when no secret is configured (5xx) | test: wrong or missing signature returns 400 and no side effect |
| No replay protection | resend a valid captured event after the tolerance window and again within it | keep the timestamp tolerance (5 minutes by default at Stripe, never 0), dedupe by event id in a table with a unique key, make handlers idempotent | tests: stale timestamp rejected; same event id twice changes state once |
| Access granted from the success redirect or from the event body alone | complete a payment, then request access without the webhook | grant from verified event or API lookup of the object; handle refund and dispute events | test: no entitlement before the verified event |
| Slow handler causes retries | measure response time | return 2xx fast, queue the work | load test with duplicates |
[C] B47, B9 (API10 for third-party data), B2

## Tree G: file upload abuse
| Cause | Safe check | Fix | Test |
|---|---|---|---|
| Trusts `Content-Type` or extension | upload a harmless text file named `.png` and a `.html` | allowlist extensions, check content signature, re-encode images, strip metadata | test: wrong type rejected |
| Original filename used in a path (traversal) | upload a file named `../../probe.txt` in staging | generate the stored name server-side, resolve then confirm the final path prefix | test: traversal name stored under a random name |
| Public bucket or guessable URLs | list the bucket anonymously, fetch an object without a token | private bucket; signed URL issued after identity, entitlement and quota; keys from the database | test: anonymous fetch of any object returns 403 |
| Archive or image bombs, huge files, costly processing | upload a file at the limit, a high-ratio archive in staging | size limit including decompressed size, per-user quota, isolated parser | test: oversized and bomb files rejected |
| Stored active content (SVG, HTML) | see Tree C | serve from a separate origin with download disposition | test: `Content-Type`, `nosniff` and `Content-Disposition` headers |
[C] B16, B9 (API4)

## Tree H: dependency vulnerability alert
Decide reachable or not, and by how much to hurry. [C] B21, B39, B40
1. Is it in a production dependency or only a build or test tool? Direct or transitive? Is the vulnerable function on a request path?
2. Priority: on the CISA KEV list (exploited in the wild) first; then EPSS (probability of exploitation in 30 days) combined with CVSS and reachability; worked example: CVSS 9.8 with EPSS 0.02% in an unused code path is lower than CVSS 7.5 with EPSS 40% on your login path.
3. Fix: upgrade to the fixed version (check lockfile and CI use it); if none, remove the dependency, isolate the feature, or apply a narrowly scoped mitigation, and track the real fix.
4. If not reachable, record a VEX-style statement: product, vulnerability, status "not affected", justification, review date; do not just mute the alert (B38). Keep an SBOM from the lockfile (B37).
Test: the scanner passes on the fixed lockfile; a unit test that fails on the old version when the fix is a code-level mitigation.

## Tree I: prompt injection reaching tools or data
Symptom: a document, web page, email or user message makes the model call a tool, leak data or change behaviour. Cause: untrusted text and instructions share one channel, and the model has permissions. Confirm in staging with a harmless instruction in a test document ("append the word PROBE to the reply") and see if the model obeys, then whether it can call a tool. Fix by limiting what the model can do: least privilege for tools, the user's identity and tenant filter on retrieval, human approval for risky actions, output validated before it reaches a query, URL or HTML, per-account cost cap. There is no filter that removes the risk. Test: a poisoned document cannot cause a tool call outside the user's permission, and a foreign-tenant document is never retrieved. Depth: `llm-engineering`. [C] B32, B7 (A01, A05)

## Tree J: CORS or CSRF misconfiguration
| Cause | Safe check | Fix | Test |
|---|---|---|---|
| `Access-Control-Allow-Origin` reflects any `Origin`, or `*` with credentials | send requests with a foreign `Origin` header and read the response headers | exact allowlist, `Vary: Origin`, never `null`; remember CORS is not access control | test: foreign origin gets no allow header |
| Cookie-authenticated state change with no CSRF defence | from a local page on another origin, try a form post to staging with a test cookie | framework protection first; otherwise synchronizer token or signed double submit, check `Origin` and `Sec-Fetch-Site`; `SameSite=Lax` or `Strict` as a layer; no state change on GET | test: cross-site post is refused |
| Sibling subdomain takeover or wildcard CORS | review DNS for dangling records | remove dangling DNS; no wildcard origins | DNS audit script |
[C] B14, B44, B45

## Tree K: rate-limit bypass and bots
| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Limit works in one test, not in production | per-process memory limit with several replicas, or the IP read from a spoofable header | count effective limit = limit x replicas; check which header the edge sets | shared store; client IP from the edge's trusted header |
| Bypass by rotating IPs or accounts | limit only per IP | log by account and by flow | per-account and per-flow limits, quotas, challenge after signals |
| Limiter outage opens the route | fail-open default | stop the store in staging and call the route | fail closed for money, email and paid-media routes; open for cheap reads |
| Abuse of a sensitive flow (trials, codes, referrals, paid AI) | no flow-level limit | count creations per device signal and per payment fingerprint | per-account quota, delay, verification step |
Test: N+1 requests in a window get 429 on request N+1; stopping the limiter store yields the documented behaviour. [C] B9 (API4, API6)

## Tree L: admin panel exposed
Check from outside: is the path public, indexed, guessable; does it require login; does the login have MFA and rate limiting; can a normal user's token call admin API routes (function-level authorization, API5); are staging or preview deployments protected. Fix: authorize every admin route and server action on the server (a hidden link is not a control); phishing-resistant MFA; short sessions and re-authentication for refunds, exports and role changes; network or identity-provider restriction where affordable; log every admin action. Test: a normal user token gets 403 on every admin route (iterate the route list), and an admin action without recent authentication is refused. [C] B9 (API5), B24, B33
