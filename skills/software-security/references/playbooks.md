# Playbooks: routines for a small team

Eight routines. Each one is short on purpose; depth sits in the topic references named inside it (`threat-modeling-incident.md`, `checklists.md`, `sessions-auth-browser.md`, `supply-chain-secrets-logging.md`, `hardening-extras.md`). Evidence tags: **[C]** standard or vendor doc, **[M]** serious but single or dated, **[F]** practitioner judgment. B# are `BIBLIOGRAPHY.md` entries. Ideas are restated, nothing is copied.

## 1. Threat-model a feature (STRIDE-lite, 30 minutes)
Do it when a feature adds a trust boundary: a new provider, upload, webhook, role, AI step, mobile client. The template and the LINDDUN add-on for personal data are in `threat-modeling-incident.md` 1; this is the meeting.
1. **Draw the data flow** on one page: who calls (browser, app, partner), which processes, which stores, and a dashed line at each trust boundary (browser to server, server to provider, tenant to tenant, user content to model instructions). If you cannot draw a flow, nobody understands it yet. [C] B23, B2
2. **STRIDE-lite per flow crossing a boundary:** Spoofing (who says they are who?), Tampering (can it be changed in transit or at rest?), Repudiation (could we prove who did it?), Information disclosure, Denial of service (including cost), Elevation of privilege. Spend two minutes per letter, not an hour on one. [C] B23
3. **Write 5 abuse cases** next to the use cases, in the form "as <attacker> I do <thing> to get <gain>": a user changes an id; a free user repeats a paid action; two requests race; a replayed callback; a poisoned document. Rank by gain times ease. [C] B10, [F]
4. **Pick a response per top threat:** remove the feature or data, mitigate with a control, transfer (use the provider's control), or accept in writing with a review trigger. Every mitigation becomes a test or a checklist line. Output: one page in the repo beside the design doc. [C] B23

## 2. Secure code review checklist, by risk
Review in this order and stop to write a finding when proof exists. File:line, exploit, fix, test (`SKILL.md` format).
1. **Access control (highest yield):** guard on every route, server action and job; object and tenant filter in the query; role from the verified identity; admin routes separate. Tests for the denied case. [C] B7, B24, B18, B48
2. **Money and state:** price and entitlement on the server; atomic check-and-change; idempotency; state transitions from a known origin; refund and dispute paths.
3. **Authentication and session:** see routine 3; cookie flags verified in a real response; no token in a URL.
4. **Injection and unsafe sinks:** parameterized SQL only; no shell strings; HTML escaped by context; paths built from server data and confirmed after resolution; redirects only to an allowlist (open redirect) [B28]; no native deserialization of untrusted data (use JSON and a schema) [B26]; XML parsers with DTDs and external entities off [B27]; no user input in template source (server-side template injection) or in `eval`/`new Function`.
5. **Outbound requests:** SSRF controls (diagnosis Tree D); timeouts; no redirect following.
6. **Cryptography and tokens:** passwords hashed with Argon2id (at least 19 MiB memory, 2 iterations, 1 lane as OWASP's floor), else scrypt, bcrypt only for legacy, PBKDF2 only if FIPS is required, each with a unique salt [B25]; randomness from the platform CSPRNG, never `Math.random` for tokens; JWT: pin the allowed algorithm, verify signature, `exp`, `iss`, `aud`, reject `none`; TLS everywhere with HSTS; keys never in code. [C] B25, B30, B51
7. **Files and media:** allowlist, server names, private storage, short signed URLs (`input-files-apis.md`).
8. **Errors and logs:** generic errors outside; no secrets or personal data in logs; security events logged; fail closed on money, access and personal data.
9. **Dependencies and config:** new packages justified; lockfile changed on purpose; CI permissions minimal; no secret in public env prefixes.
10. **Tests:** every fix has a test that fails without it.
Anti-patterns that waste review time: style comments, scanner output pasted without proof, "add a WAF" as a fix.

## 3. Authentication and authorization design checklist
**Sessions or tokens**
- [ ] Browser app with your own backend: server-side session in an `HttpOnly; Secure; SameSite=Lax` cookie (prefer `__Host-`); the session id is rotated on login and privilege change; server-side expiry (idle and absolute) and revocation. [C] B13, B45
- [ ] Stateless JWTs only when you need them (multiple services, mobile); short access tokens, rotating refresh tokens, a revocation story; never in `localStorage`; token in the cookie or a backend-for-frontend, not in a URL. [C] B13, B50
- [ ] Mobile: tokens in Keychain or Keystore-backed storage (`mobile-security.md` 3).
**OAuth 2.0 and OIDC basics**
- [ ] Authorization code flow with PKCE; no implicit flow; exact redirect-URI match; `state` or PKCE against login CSRF; refresh tokens rotated or sender-constrained. [C] B50
- [ ] Validate the ID token: signature, issuer, audience equals your client id, expiry, nonce when used. Use a maintained library, do not parse by hand. [C] B51
- [ ] Do not use the ID token as an API access token; check scopes server-side.
**Passkeys and MFA**
- [ ] Offer passkeys (WebAuthn): credentials are bound to the origin, so a look-alike site cannot use them. Admins use phishing-resistant MFA. SMS and email codes are the weaker fallback; rate-limit them. [C] B52, B33
- [ ] Recovery is the weak link: the recovery path must not be easier than the login path; notify on factor or email change; recovery events are logged.
**Passwords (NIST SP 800-63B-4)**
- [ ] Single-factor password at least 15 characters; at least 8 when it is only one factor among several; accept at least 64; no composition rules; no forced periodic change (only on evidence of compromise); blocklist of common and breached values; paste and managers allowed; no security questions or hints; salted hash with a modern algorithm. [C] B33, B11, B25
- [ ] Per-account throttling that does not let an attacker lock the owner out; generic responses and similar timing for known and unknown accounts. [C] B11, B22
**Authorization**
- [ ] Deny by default; one central check; tests for denial; object, property and function levels (BOLA, BOPLA, BFLA). [C] B24, B9
- [ ] Multi-tenant: tenant from the verified identity; filter in code and RLS in the database; tests with presence and absence (`access-control-tenancy.md`).
- [ ] Service-to-service and AI agents act with the end user's permission, not a global key.

## 4. Secrets: routine and rotation
Inventory (private table): name, purpose, where used, owner, created, last rotated, rotation steps, what breaks. Environments never share a value; one secret per service. [C] B17
- **Prevent:** pre-commit hook plus CI scan plus the platform's secret scanning with push protection where available (B49); nothing secret in `NEXT_PUBLIC_*`, `EXPO_PUBLIC_*` or any bundle; short-lived OIDC credentials in CI instead of long-lived cloud keys.
- **Scheduled rotation (machine secrets):** every 90 days or on staff change **[F]**; with overlap: create the new, deploy it, verify the consumer uses it, revoke the old. Rehearse once on a quiet day (`hardening-extras.md` 6). Webhook secrets overlap by design (Stripe keeps the old one valid for a limited window).
- **Leak:** revoke, replace, redeploy, verify, remove from the place it leaked, audit the exposure window, record it (`supply-chain-secrets-logging.md` 4; diagnosis Tree E).
- **Never** print or paste values in chats, tickets or reports; work with names.

## 5. Security headers and CSP rollout
Start with the cheap, safe headers on every response, then CSP in stages. [C] B30, B43, B20
1. **Baseline (an afternoon):** `Strict-Transport-Security` (start with a short max-age, then long, add `includeSubDomains` only when every subdomain is HTTPS), `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` disabling unused features, `Cross-Origin-Opener-Policy` where compatible, `frame-ancestors` (via CSP) instead of `X-Frame-Options` (send both if old browsers matter) [B29]. Do not send `X-XSS-Protection`.
2. **CSP report-only first:** send `Content-Security-Policy-Report-Only` with a strict policy (nonce-based `script-src`, `object-src 'none'`, `base-uri 'none'`), collect reports via `Reporting-Endpoints` and `report-to` for one to two weeks, fix legitimate violations (inline scripts, third-party tags), drop noise from browser extensions. Report-only cannot be set with a meta tag. [C] B43, B20
3. **Enforce:** switch the header to `Content-Security-Policy`, keep a report-only copy for the next tightening; roll out per route or per percentage if the platform allows. Payment pages: allow only the provider's hosts. Nonces need per-response templating; static pages use hashes.
4. **Own the exceptions:** each third-party script has an owner and a reason; remove what is unused. A strict CSP is defence in depth, not a replacement for output encoding. [C] B19
5. **Check:** a header scan in CI against a preview URL; test that a harmless inline script marker is blocked on the enforced pages.

## 6. Dependencies and supply chain
- **Every build:** install from the lockfile (`npm ci`, frozen lockfile), generate an SBOM from it, run SCA, run secret scan. Block merge on new critical findings that are reachable. [C] B37, B21, B34
- **Weekly (30 minutes):** triage new alerts with the tree in diagnosis H (KEV first, then EPSS and reachability), merge safe update PRs in small batches, delete unused packages. [C] B39, B40
- **New package gate:** maintenance, maintainers, install scripts, name similarity (typosquatting), size of its tree; a ten-line helper is often cheaper to own.
- **CI hygiene:** third-party actions pinned to a commit SHA; token read-only by default; no untrusted input interpolated into scripts; OIDC trust limited to one repository and ref (`supply-chain-secrets-logging.md` 3, `hardening-extras.md` 3).
- **Provenance:** build in CI, produce provenance and sign artifacts; the deploy step verifies it. SLSA gives the vocabulary (Build and Source tracks); do not chase a level for its own sake. [C] B36, B34
- **VEX:** when you suppress a finding, record "not affected" with a reason and a review date (`hardening-extras.md` 4). [C] B38

## 7. Incident response for a suspected breach
Fuller steps and the one-person preparation list are in `threat-modeling-incident.md` 2; this is the run sheet.
1. **Declare and assign** one lead and one scribe (can be the same person); open a timeline note with UTC times.
2. **Contain:** revoke the suspicious credential or session, switch off the route or feature by configuration, block the account; do not delete anything. [C] B35
3. **Preserve evidence** before retention or restarts erase it: export logs, database audit rows, access logs of provider dashboards; snapshot volatile state if a host is involved; hash the copies and note who collected what (`hardening-extras.md` 7).
4. **Scope:** which data, which people, which period, which credentials could the attacker use next. Search for the same pattern elsewhere.
5. **Eradicate and rotate:** fix the cause with a reproducing test; rotate every secret the intruder could have read; invalidate sessions; patch.
6. **Notify:** if personal data was affected the legal clocks may already be running (GDPR: 72 hours to the authority after becoming aware, where notification is required; Brazil: see the ANPD rule) so open the privacy law of the data subject's country (official regulator pages) the same hour; tell the payment provider if charges are involved; tell affected users when the risk is high. Write down the decision to notify or not and why.
7. **Recover and watch:** restore from known-good, monitor for re-entry for two weeks.
8. **Learn:** blameless record within a week: timeline, cause, impact, what worked, one new control or test, owner and date. [C] B35

## 8. Pre-release security gate
Fail means block or a time-boxed exception with an owner and an expiry date (an exception without an expiry is a permanent suppression). [C] B34, B41
- [ ] Threat model exists for any new trust boundary (routine 1) and the top three risks have tests.
- [ ] Review done by risk (routine 2); no open Critical or High.
- [ ] Access control: denied-case tests for each new route and policy; advisors or catalog checks clean.
- [ ] Auth: nothing weaker than routine 3; admin has MFA.
- [ ] Secrets: scan clean on the diff and the built artifact; none in public prefixes.
- [ ] Dependencies: lockfile used in CI; no reachable known-exploited vulnerability; SBOM produced.
- [ ] Headers and CSP in at least report-only; CORS is an allowlist.
- [ ] Logging: auth, authorization failures and admin actions are logged without secrets; an alert reaches a phone.
- [ ] Payments and webhooks: signature on raw body, replay and duplicate tests green.
- [ ] Mobile build: the gate in `mobile-security.md` 11.
- [ ] Automated or AI-agent test run on the isolated preview (two tenants, one account per role): only confirmed findings count; unconfirmed candidates listed under "not verified" (`ai-assisted-testing.md`).
- [ ] Incident contacts and the rotation steps are current; a rollback exists.
- [ ] Privacy review for new personal data.
Output: one line verdict (ship, ship with caveats, do not ship), the list of exceptions with owner and date, and "not verified".
