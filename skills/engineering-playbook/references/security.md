# Security

Principles: **least privilege, defense in depth, secure defaults, fail closed, never trust input (including from your own frontend), minimize data kept.**

## 1. OWASP Top 10 — what each is and how to prevent it

Categories below follow OWASP Top 10:2021; the 2025 edition reorders them and adds explicit categories for **software supply chain failures** and **mishandling of exceptional conditions** (both covered here).

### Broken access control (most common)
- **What:** users act outside their permissions — IDOR (`GET /invoices/123` returns someone else's invoice), missing function-level checks, tenant crossover, privilege escalation, CORS misconfig.
- **Do:** deny by default; check authorization **server-side on every request, per resource** (`invoice.TenantId == currentTenant && user can read`); scope every query by tenant/owner; ASP.NET Core policy/resource-based authorization (`IAuthorizationService.AuthorizeAsync(user, resource, policy)`); test negative cases (user B accessing user A's id).
- **Avoid:** relying on hidden UI buttons, unguessable IDs, or client-sent roles/tenant ids.

### Cryptographic failures
- **What:** sensitive data unencrypted in transit/at rest, weak algorithms, hardcoded keys.
- **Do:** TLS 1.2+ everywhere (HSTS); encryption at rest (TDE, storage encryption); field-level encryption for highly sensitive data; keys in Key Vault/KMS with rotation; `RandomNumberGenerator` for tokens (never `Random`/`Math.random()`).
- **Avoid:** MD5/SHA-1 for security, ECB mode, rolling your own crypto, reusing IVs/nonces with AES-GCM.

### Injection (SQL, NoSQL, OS command, LDAP, XPath, template, log)
- **Do:** parameterized queries/ORM; never build SQL/shell with string concatenation; if dynamic identifiers (column names for sorting) are needed, **allow-list** them; avoid shell — call processes with argument arrays; contextual output encoding.
- **Avoid:** `FromSqlRaw($"...{input}")`, `exec`/`eval`, `Process.Start("cmd", "/c " + input)`.

### Insecure design
- Missing threat modeling, business-logic abuse (negative quantities, coupon reuse, race to double-spend). **Do:** threat model new features (STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege); validate business invariants server-side; rate limit abuse-prone flows.

### Security misconfiguration
- Default credentials, verbose errors/stack traces in prod, open storage buckets, debug endpoints, permissive CORS, missing headers.
- **Do:** environment-specific config; `UseExceptionHandler` + Problem Details without internals; disable directory listing; least-privilege cloud roles; IaC with reviewed defaults.

### Vulnerable & outdated components / supply chain
- **Do:** `dotnet list package --vulnerable`, `npm audit`, Dependabot/Renovate; pin versions and use lockfiles (`packages.lock.json`, `package-lock.json`); minimize dependencies; verify package names (typosquatting); CI with least-privilege tokens; SBOM; signed artifacts; review new dependencies' maintenance and install scripts.

### Identification & authentication failures
- Credential stuffing, weak passwords, session fixation, missing MFA.
- **Do:** use a proven identity provider (Entra ID/Azure AD B2C/Entra External ID, Auth0, Keycloak, ASP.NET Core Identity); MFA; rate limit & lockout/backoff on login; check passwords against breached lists; regenerate session on login; generic error messages ("invalid credentials").

### Software & data integrity failures
- Insecure deserialization, unsigned updates, CI/CD tampering.
- **Do:** never use `BinaryFormatter` (removed in .NET 9); with `Newtonsoft.Json` keep `TypeNameHandling.None`; validate webhooks by signature; protect pipelines and branch rules.

### Security logging & monitoring failures
- **Do:** log authentication events, authorization failures, admin actions, high-value transactions with user/tenant/correlation ids; alert on anomalies; keep audit logs tamper-evident and retained per policy. **Never log** passwords, tokens, full card numbers, secrets, or unnecessary PII.

### SSRF (server-side request forgery)
- **What:** server fetches a user-supplied URL → reaches internal services/cloud metadata (`169.254.169.254`).
- **Do:** allow-list hosts/schemes; resolve DNS and block private/link-local ranges (re-check after redirects; disable auto-redirect); separate egress network; don't return raw fetched responses.

### Mishandling exceptional conditions
- Fail **closed** (on authz error → deny); don't leak details in errors; handle partial failures without leaving inconsistent state; resource cleanup in `finally`/`using`.

## 2. Web-specific

- **XSS:** frameworks (React, Razor) encode by default — don't bypass (`dangerouslySetInnerHTML`, `Html.Raw`) with untrusted data; sanitize rich HTML with an allow-list sanitizer (DOMPurify, HtmlSanitizer); Content-Security-Policy (nonces, no `unsafe-inline`); sanitize Markdown output.
- **CSRF:** relevant for cookie-based auth. `SameSite=Lax/Strict` cookies + anti-forgery tokens for state-changing requests; never change state on GET.
- **CORS:** it's a browser relaxation, not a security control for your API. Allow explicit origins only; never reflect arbitrary `Origin` with `Allow-Credentials: true`.
- **Clickjacking:** `frame-ancestors 'none'` (CSP) / `X-Frame-Options: DENY`.
- **Headers:** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.
- **Cookies:** `HttpOnly`, `Secure`, `SameSite`, `__Host-` prefix for session cookies.
- **Open redirect:** validate `returnUrl` is local (`Url.IsLocalUrl`).
- **File uploads:** limit size; validate type by content (magic bytes), not extension; store outside web root/in blob storage with random names; serve with `Content-Disposition: attachment` and correct content type; scan for malware where relevant; never trust file paths (path traversal `../`).
- **Mass assignment / over-posting:** bind to DTOs with explicit fields, never directly to entities (`IsAdmin`, `TenantId` in body).
- **Prototype pollution (JS):** don't deep-merge untrusted objects into plain objects; use `Map`, schema validation (zod), `Object.create(null)`.
- **ReDoS:** regex timeouts / non-backtracking engine for untrusted input.
- **XXE:** disable DTD processing in XML parsers (default safe in modern .NET `XmlReader`).

## 3. Authentication & tokens

- **OAuth 2.0** = delegated authorization; **OIDC** = authentication layer on top (ID token).
- Flows: Authorization Code + **PKCE** for SPAs and mobile; Client Credentials for service-to-service. Avoid implicit and password (ROPC) flows.
- **SPA tokens:** prefer the **BFF pattern** (backend holds tokens, browser gets an HttpOnly session cookie) over storing tokens in `localStorage` (XSS-readable).
- **Mobile:** tokens in secure storage (Keychain/Keystore; `expo-secure-store`), never AsyncStorage.
- **JWT validation:** verify signature with expected algorithm (reject `alg: none`, prevent HS/RS confusion), `iss`, `aud`, `exp`/`nbf` with small clock skew; short-lived access tokens (5–15 min) + rotating refresh tokens with reuse detection; JWTs can't be revoked easily → short TTL or denylist; don't put sensitive data in JWT payload (it's only base64).
- **Passwords:** Argon2id (OWASP minimum: 19 MiB memory, 2 iterations, 1 parallelism) or bcrypt (cost ≥ 10) or PBKDF2-HMAC-SHA256 (≥ 600,000 iterations); unique salt per password (built into these); never encrypt passwords reversibly; ASP.NET Core Identity's `PasswordHasher` is acceptable.
- **Tokens for reset/verification:** cryptographically random, single-use, short expiry, stored hashed.
- **Constant-time comparison** for secrets/signatures: `CryptographicOperations.FixedTimeEquals`, `crypto.timingSafeEqual`.
- **API keys:** random ≥ 128 bits, store hashed, prefix for identification, scope and rotate.

## 4. Authorization models

- RBAC (roles), ABAC (attributes/policies), ReBAC (relationships, e.g. OpenFGA/Zanzibar-style) for sharing-heavy domains.
- Centralize policy logic; avoid scattered `if (user.Role == "Admin")`.
- Separate admin/back-office surfaces; require stronger auth for them.

## 5. Secrets management

- Never commit secrets; scan repos (gitleaks, GitHub secret scanning); rotate anything ever committed.
- Azure: **Managed Identity** to access Key Vault, SQL, Storage, Service Bus (no connection-string secrets); Key Vault references in App Service/Functions config.
- Local dev: `dotnet user-secrets`, `.env` in `.gitignore`.
- Frontend bundles and mobile apps are public — anything in them is not a secret (`NEXT_PUBLIC_*`, `EXPO_PUBLIC_*`).

## 6. Data protection & privacy

- Data minimization: collect and keep only what's needed; retention policies; deletion/erasure flows (GDPR).
- Classify data (public, internal, confidential, special category — health data is special category under GDPR).
- Mask/tokenize sensitive fields in logs and non-prod environments; don't copy production PII into dev/test without anonymization.
- Encrypt backups; restrict who can query production.
- ASP.NET Core Data Protection API for encrypting cookies/tokens — persist keys (Blob + Key Vault) when running multiple instances.

## 7. Multi-tenant security

- Tenant id from the authenticated principal, never from request body/query.
- Enforce at the data layer: EF Core global query filters, DB Row-Level Security; test cross-tenant access explicitly. See saas-multitenancy.md.

## 8. Infrastructure

- Private endpoints/VNet for databases and storage; no public DB endpoints with broad firewall rules.
- WAF/API gateway for public APIs; DDoS protection at the edge.
- Least-privilege RBAC for humans and workloads; just-in-time admin access.
- Container images: minimal base, non-root user, scanned.

## 9. Secure SDLC checklist for a change

- [ ] Input validated (type, length, range, format) at the boundary (FluentValidation, DataAnnotations, zod).
- [ ] Output encoded for its context.
- [ ] AuthN required; AuthZ checked per resource and tenant.
- [ ] No secrets/PII in code, logs, errors, URLs (query strings end up in logs).
- [ ] Dependencies added are maintained and needed.
- [ ] Rate limits on abuse-prone endpoints (login, OTP, password reset, signup, expensive search, AI calls).
- [ ] Tests for "user A cannot access user B's resource".
