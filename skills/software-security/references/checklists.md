# Review checklists by change type

Use after the four questions in SKILL.md. Each line points to the reference that explains it.

**New route, handler or server action** (`access-control-tenancy.md`)
- [ ] Guard on the route itself (a page or proxy check does not cover a server action or a direct POST).
- [ ] Object filtered by owner/tenant from the verified token; a foreign id returns 404 like a missing one; test for the denied case.
- [ ] Response is a minimal DTO: no internal fields, no file paths, no other users' data.
- [ ] Per-IP and per-account limit on costly or sensitive routes; written fail-open/fail-closed decision (`input-files-apis.md` §5).
- [ ] Debug, QA and old-version routes are off in production by configuration checked at boot.

**Migration, policy or SQL function** (`access-control-tenancy.md` §3, §4)
- [ ] RLS enabled (and forced if the app connects as owner); default grants revoked from API roles; only needed grants back.
- [ ] One policy per command with explicit `TO`, `WITH CHECK` on writes, index on the policy column; unique keys scoped by tenant.
- [ ] `SECURITY DEFINER` only outside exposed schemas, `search_path` pinned, `REVOKE EXECUTE FROM PUBLIC` in the same transaction, caller checked inside.
- [ ] Views `security_invoker`; platform security advisors show no new error.
- [ ] Column with personal data has a purpose, retention and is covered by account deletion.

**Login, session, cookies** (`sessions-auth-browser.md`)
- [ ] Same response for existing and unknown email; one-time, short-lived tokens; token never stays in the URL.
- [ ] Passwords (if any): at least 15 characters when single-factor, no composition rules, no forced periodic change, blocklist check, paste allowed.
- [ ] Cookie `HttpOnly; Secure; SameSite=Lax|Strict`, no `Domain`; verified in a real `Set-Cookie`.
- [ ] Server trusts a verified token (signature checked), never an unverified cookie read; responses with `Set-Cookie` are not cacheable.
- [ ] Admin: MFA (phishing-resistant where possible), re-authentication for sensitive actions.

**Payment or entitlement** (`business-logic-payments.md`)
- [ ] Price computed server-side; access granted only by the verified event or an API lookup, never by the success redirect.
- [ ] Event id deduplicated, order not assumed, 2xx fast and work queued; idempotency key without personal data.
- [ ] Refund, dispute opened/won and failed refund handled; proof of delivery stored.

**Business flow with value** (`business-logic-payments.md` §1)
- [ ] Two parallel requests cannot both pass the check (atomic conditional update, unique constraint or lock).
- [ ] Steps cannot be skipped or replayed; state transitions checked from a known origin.
- [ ] The flow is limited per account when automation would hurt (trials, referrals, codes, paid jobs).

**Upload or paid media** (`input-files-apis.md` §3, §4)
- [ ] Type by allowlist plus content check, server-generated name, size (and decompressed size) limit, private bucket.
- [ ] Signed URL lives minutes, issued after identity + entitlement + quota; object key comes from the database, never from the request.

**Dependency or CI change** (`supply-chain-secrets-logging.md`)
- [ ] Lockfile committed and honored in CI; new package checked for maintenance, install scripts and typosquatting.
- [ ] Workflow token read-only by default; third-party actions pinned to a full commit SHA; no untrusted PR input interpolated into scripts.

**Secrets** (`supply-chain-secrets-logging.md` §4)
- [ ] Nothing secret in public env prefixes (`NEXT_PUBLIC_*` and similar), code, logs, tests or images; one secret per environment and per service.

**AI feature** (pointer)
- [ ] Model output validated before it reaches a query, a URL, HTML or a tool; retrieval filtered by tenant; per-account token and cost cap. Depth in `llm-engineering` and the OWASP Top 10 for LLM Applications 2025 (W47).

**Automated or AI-agent security test** (`ai-assisted-testing.md`)
- [ ] Written authorisation and target allowlist; isolated staging with fake data, test-only keys and accounts for two tenants; rate, time and spend caps; a named person who can stop it.
- [ ] Each reported finding reproduced by someone else with a minimal proof, a code location and a severity; rejections logged.

**Mobile app build** (`mobile-security.md` 11)
- [ ] No secret in the built bundle; tokens in secure storage; release build not debuggable; deep links verified; purchases validated on the server.

Routines and the pre-release gate: `playbooks.md`. Symptom-first diagnosis: `diagnosis-playbook.md`.
