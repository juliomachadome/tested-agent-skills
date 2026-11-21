# Sessions, authentication and browser-side defenses

Format: **rule** · why · source id (see `sources.md`) · example.

## 0. Passwords and authenticators (NIST SP 800-63B-4, July 2025)

1. **Single-factor passwords: minimum 15 characters; passwords used only inside MFA: minimum 8; allow at least 64.** Length beats complexity. · W49 · e.g. reject "Summer2025!" by blocklist, accept a 4-word passphrase.
2. **No composition rules** (mixtures of character types) **and no forced periodic changes;** force a change only on evidence of compromise. · W49
3. **Check new and changed passwords against a blocklist** of common, expected and breached values, and tell the user why it was refused. · W49
4. **Allow paste and password managers;** no security questions (knowledge-based authentication) and no password hints. · W49, W5
5. **Rate-limit failed attempts per account** with techniques that do not let an attacker lock out the real user (backoff, CAPTCHA after signals, trusted-device allowance). · W49, W5
6. **One-time passcodes are used only once;** accept each authentication secret once, atomically, in state shared by all servers (replay protection). · W49, W15
7. **Telephone (SMS/voice) out-of-band codes are a restricted authenticator:** offer an alternative and inform users of the risk; prefer app-based or phishing-resistant authenticators (passkeys/WebAuthn). AAL2 applications must offer a phishing-resistant option; AAL3 requires one. Use phishing-resistant MFA for admins. · W49
8. **Make MFA available at no extra cost and on by default for administrators; no default or shared initial passwords** (random, instance-unique initial credentials if any). · W48

## 1. Session cookies and tokens

1. **Session cookie: `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict`, no `Domain`, `Path=/`.** HttpOnly stops session theft by XSS; no `Domain` pins the cookie to the origin. Prefer the `__Host-` prefix when you choose the name: it forces `Secure`, no `Domain`, `Path=/`, so a subdomain cannot overwrite it. · W4, W6
2. **Never keep access, refresh or ID tokens in `localStorage`/`sessionStorage`.** One XSS takes them all. Use an HttpOnly cookie or a backend-for-frontend that holds the token server-side. · W4, W3 V14 (14.3.3)
3. **Do not assume what a library sets.** Inspect the real `Set-Cookie` in a browser and in a test. · W36
4. **Token never in a URL** (query or fragment): it leaks through history, logs, `Referer` and third-party scripts reading `location.href`. · W4, W3 V14 (14.2.1) · e.g. a WebSocket token in `?token=` ends up in access logs.
5. **Rotate the session id after login and after any privilege change; invalidate the old one.** · W4, W3 V7 (7.2.4)
6. **Expiry is decided on the server.** Reference idle timeouts: 2 to 5 min for high-value apps, 15 to 30 min for low risk; an absolute timeout always exists; admin sessions use the short values. Document the choice. · W4, W3 V7 (7.1.1)
7. **Logout invalidates server-side every id of the logical session.** Deleting the cookie does not kill a stolen copy. Cheap extra: `Clear-Site-Data: "cache", "cookies", "storage"` on the logout response. Disabling an account ends all its sessions. · W4, W3 V7 (7.4.1, 7.4.2)
8. **Responses carrying session data: `Cache-Control: no-store`; a response with a session `Set-Cookie` must never be cached by a CDN or static regeneration** (another user would be logged in as the wrong person). · W4, W36
9. **Refresh in one place only** (server or proxy, not both). Single-use refresh tokens with a short reuse window revoke the whole session on reuse, which shows up as "random logouts" when two places refresh. · W36
10. **Log a salted hash of the session id, never the id.** · W4

## 2. Passwordless (magic link, OTP) and account recovery

1. **Identical response for known and unknown emails:** same text, status and similar timing (same code path or async send). · W5, W3 V6 (6.3.8)
2. **Tokens are cryptographically random, long, single-use, bound to the requesting user, short-lived** (ASVS caps out-of-band codes at 10 minutes); numeric PINs 6 to 12 digits; rate-limited. · W5, W3 V6 (6.5.1, 6.5.3, 6.5.5, 6.6.3)
3. **Prefer the server-side token-hash flow** over implicit flows that put tokens in the URL fragment. In Supabase: `{{ .TokenHash }}` in the template and `verifyOtp({ token_hash, type })` in a server route. Links expire in 1 hour by default and values above 24 h are discouraged; lower it to what support tolerates. · W34
4. **Do not auto-create users where accounts should exist only after purchase or invite** (e.g. `shouldCreateUser: false`). · W34
5. **Redirect URLs are a closed list with the production domain, no wildcards; build the link from configured origin, never from the request `Host` header.** · W34, W5
6. **The page that consumes the token uses `Referrer-Policy: no-referrer` and loads no third-party script before the token is consumed and removed.** · W5
7. **A confirmation button (POST) before exchanging the token** protects against email scanners that open links and against login CSRF. Strong practice; the scanner part is not stated in a vendor doc. · W6 ("Login CSRF")
8. **Provider rate limits are not your account limits.** Count failures per account in your API too (careful that lockout does not become a denial of service against the victim); CAPTCHA only after some failures. Built-in email senders of auth providers are heavily throttled: production needs your own SMTP. · W5, W35
9. **No undocumented authentication path** (a debug endpoint that returns the token, a test bypass left on). Local tests may return the link in the response; production never. · W3 V6 (6.1.3, 6.3.4)
10. **Notify the user after an email or factor change; re-authenticate before it.** · W3 V6 (6.3.7), V7 (7.5.1)

## 3. CSRF

1. **CSRF exists when the credential travels automatically (cookies).** An API that only accepts an `Authorization: Bearer` header set by your server is not the classic target; the front-end server that reads cookies is. · W6 (inference from the mechanism)
2. **Use the framework's protection first.** E.g. Next.js server actions accept only POST and compare `Origin` with `Host`/`X-Forwarded-Host`; behind a proxy with another domain configure an explicit allowed-origins list. Custom route handlers with cookies are your job. · W6, W45
3. **Own routes: synchronizer token or signed double-submit** (HMAC bound to the session, constant-time compare, read from header or field, never only from the cookie). Unsigned double-submit is insecure. · W6
4. **Fetch-only APIs: require a custom header** (forces a preflight) with a closed CORS list; a wildcard subdomain in CORS defeats this if any subdomain is taken over. · W6
5. **Fetch Metadata as an extra layer:** reject unsafe methods with `Sec-Fetch-Site: cross-site`, fall back to `Origin`/`Referer` when absent. Compare the full origin; a missing header or `Origin: null` proves nothing; never allowlist `null`. · W6
6. **`SameSite=Lax` blocks only unsafe cross-site methods**, so no GET may change state; sibling subdomains are "same site". Do not put cookies on the parent domain without need. · W6
7. **Third-party webhooks are exempt from CSRF and CORS; their authentication is the signature.** · W38

## 4. CORS, CSP and headers

1. **CORS: explicit origin list, never `*` on routes with data, never echo the received `Origin` without checking.** CORS only stops browsers from reading responses; it is not access control. · W7
2. **CSP for payment pages: allow only the provider's script, frame and API hosts** (for Stripe: `js.stripe.com` for script and frame, `hooks.stripe.com` frames for 3DS, `api.stripe.com` for connect, `checkout.stripe.com` for hosted checkout); Stripe.js does not work under cross-origin isolation (COOP/COEP). Load it from the vendor host, never self-hosted. · W40
3. **Fewer third-party scripts on login and payment pages:** including another site's JavaScript makes your security depend on theirs. · W40
4. **Signed media hosts must be allowed in `img-src`/`media-src`** (S3-style signed URLs work only on the storage API domain, not on a custom domain). · W42

## 5. WebSocket authentication

1. **Validate `Origin` on every handshake against an allowlist** (cross-site WebSocket hijacking). With Node `ws`, check in the HTTP server `upgrade` event before `handleUpgrade`. · W13
2. **Browser clients send the token in the first message over WSS, not in the URL;** accept only the auth message until it validates, close on failure or timeout, limit unauthenticated connections, and keep tokens out of message logs. Rotate tokens on long-lived connections. · W13
3. **Authorize each message type, not only the connection.** A connection opened by a viewer must not be able to send an editor's command. · W13, W12
