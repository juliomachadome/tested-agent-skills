---
name: software-security
description: "ALWAYS use this skill, even for a short \"is this ok?\" question, when code touches auth, user data, uploads, money or a mobile app's secrets and storage. Triggers \"can user B read user A's orders through GET /api/orders/:id\", \"is the JWT in localStorage bad\", \"our Stripe webhook parses JSON before checking the signature, ok for launch?\", \"review my supabase migration or RLS policy for multi-tenant\", \"I save the original upload filename in /public/uploads\", \"we leaked a key\", \"is my Expo app safe to ship\". Think like an attacker on web, API and mobile app security, covering login, sessions, IDOR, tenant isolation, Postgres RLS, payments, webhooks, uploads, secrets, CORS/CSRF/CSP, SSRF, rate limits, deep links, certificate pinning and incident response. Returns findings by severity with file:line, exploit, fix and test. Not for legal basis or consent, PR review (code-review-criteria), prompt injection in LLM features (llm-engineering) or deploy mechanics (cloud-deploy-ops)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Web, API and mobile app security

Read every change as the cheapest attacker would: another logged-in user, a stranger with a URL, a bot with a paid account, a forged webhook, a rooted phone. What must never leak is other people's data, money and paid content; the architecture is always discoverable. Evidence tags: **[C]** standard or vendor doc, **[M]** single or dated source, **[F]** practitioner judgment, **[X]** myth. OWASP Top 10:2025 is current (SSRF sits in A01).

**Project first.** Read the current project's CLAUDE.md or AGENTS.md, ADRs, access model, known open issues, migrations and CI files; project rules and accepted risks win over this skill. Then Step 0 of `references/diagnosis-playbook.md` (what is exposed, data classes, auth model, tenancy, recent changes, logs).

Boundaries: prompt injection to `llm-engineering`; "may we process this data?" to counsel and the official regulator of the data subject's country; coding defaults to `engineering-playbook`; store, build and OTA mechanics to `mobile-app-engineering`.

**Proportion.** Assume a small team. Prefer platform-shipped controls (RLS, provider auth limits, framework CSRF) over homemade ones; one tested control beats three unmaintained. No WAF, SIEM, DRM, vault or recurring pentest without an incident or number to justify it. Secure by default: MFA available, no default passwords (W48).

## Principles (sources in `references/`)

1. **Authorize on the server, per object, on every request, deny by default.** Broken access control is the top web and API risk; `GET /orders/:id` filters by the caller, not just "has a session". [W1, W2, W12] **[C]**
2. **The database policy is the second wall.** Owners and `BYPASSRLS` roles skip RLS; FK and unique checks ignore it; views bypass it unless `security_invoker`. Keep the tenant filter in code. [W25, W29] **[C]**
3. **Tenant context only inside a transaction** (`SET LOCAL`); behind a pooler a session `SET` leaks to the next request; missing setting = deny. [W26, W32]
4. **The server computes everything that has value:** price, discount, role, tenant, quota, entitlement. A mobile or browser client is attacker-controlled. [W15, W16]
5. **Abuse the flow, not only the endpoint:** races, replay, steps out of order, automation. Validators never catch these. [W2a, W16, W28]
6. **Fail closed where money, access or personal data is at stake;** list what may fail open. [W1 A10, W43]
7. **Authentication follows NIST SP 800-63B-4:** single-factor passwords of 15+ characters, no composition rules or forced rotation, blocklist, paste allowed; one-time codes used once; phishing-resistant MFA for admins. [W49, W5] **[C]**
8. **A leaked secret is dead:** revoke, replace, remove, audit the exposure window; a restart revokes nothing. Anything in an app bundle is leaked. [W11] **[C]**
9. **Generic errors outside, detail in logs, no secrets or personal data in logs.** [W10, W44]
10. **Eliminate the class, not the instance** (default `REVOKE`, allowlists, parameterized queries, a central guard), and **prove before you claim**: file:line, exploit, a test that fails today; unproven means "not verified". [W48]

## Method

1. **Scope:** routes, server actions, migrations, policies, functions, views, cookies, env vars, dependencies, CI files, third-party scripts; for apps the bundle, deep links, local storage and build config.
2. **Four questions per item:** who can call it, with which identity, on which row, and what happens if it is called a thousand times or twice at once. An answer in neither code nor test is a finding.
3. **Walk as an attacker:** anonymous, unpaid login, another user's id, another tenant, refunded or disputed account, lower admin, bot with a paid account, forged callback, modified mobile client.
4. **Trace source to sink** for each external input (body, header, upload, document, model output, webhook, deep link) reaching SQL, shell, path, HTML, URL fetch, prompt, log or signed URL.
5. **New trust boundary:** a 30-minute threat model (`references/playbooks.md` 1).
6. **Verify each finding** as the real role with your own test accounts; production only read-only and on the owner's order. Isolation is proven when the row is present for the right tenant and absent for the other.
7. **Close with the checklist** for the change type (`references/checklists.md`); before release, the gate in `playbooks.md` 8.

## Which reference to open

| The task or symptom | Open |
|---|---|
| Something is broken or exposed: other user's data, account takeover, XSS, SSRF, leaked secret, webhook spoofing, upload abuse, dependency alert, prompt injection, CORS/CSRF, bots, admin exposed | `references/diagnosis-playbook.md` (Step 0, then the tree) |
| Routines: threat model, review checklist, auth design, secrets rotation, headers and CSP, supply chain, breach response, release gate | `references/playbooks.md` |
| Authorization levels, multi-tenant, Postgres RLS, grants, SECURITY DEFINER, pooler, Supabase keys and advisors | `references/access-control-tenancy.md` |
| Passwords and MFA, sessions, cookies, magic link/OTP, CSRF, CORS, CSP, WebSocket auth | `references/sessions-auth-browser.md` |
| SSRF, uploads, signed URLs, injection sinks, rate limits, GraphQL/WebSocket limits | `references/input-files-apis.md` |
| Abuse cases, races, replay, state machines, payments, webhooks, idempotency, disputes | `references/business-logic-payments.md` |
| Dependencies, SBOM, KEV/EPSS, CI hardening, secrets, security logging | `references/supply-chain-secrets-logging.md` |
| Threat model template, privacy threats, incident response preparation | `references/threat-modeling-incident.md` |
| Prototype pollution, request smuggling, OIDC trust, VEX, provenance, rotation rehearsal, evidence order, access hygiene | `references/hardening-extras.md` |
| iOS, Android, Expo, React Native: secrets in the bundle, secure storage, pinning, deep links, WebViews, receipts, modified clients | `references/mobile-security.md` |
| AI agents testing your own app: scope, proof, CI | `references/ai-assisted-testing.md` |
| Checklist per change type | `references/checklists.md` |
| Sources | `references/BIBLIOGRAPHY.md` (numbered), `references/sources.md` (W ids) |

## AI tells to avoid (check while answering, not after)
- A generic OWASP list not tied to this code; name the route, query or policy.
- A finding with no file:line and no test that reproduces it.
- Severity inflation: rate by who can exploit it and what leaks, not by the category name.
- Invented CVEs, versions or advisory ids; cite only what you read.
- "Add a WAF, MFA or rotation" with no link to the threat at hand.
Fix: use the user's case and data, sources actually read, one recommendation with its reason and how to verify it. Say what you chose and why in one line; a choice without a reason is removed.

## Severity and report

Critical: other users' or tenants' data, access without paying, exposed secret, auth bypass. High: exploitable with effort or a paid account, or abuse that costs money. Medium: missing defense in depth. Low: hardening. Cite the category (API1:2023, A01:2025).

```
[High] BOLA on GET /orders/:id  (API1:2023)
Where: src/routes/orders.ts:42
Exploit: user B changes the id and reads A's order (email, amount).
Proof: "foreign id returns 404" in orders.test.ts fails today (200).
Fix: filter by the token's user id in the repository; 404. Effort: 1 h.
```

Report: verdict (ship, caveats, do not ship); table (severity, category, file:line, exploit, fix, effort, status); "checked and fine" per area; "not verified"; "owner decisions" (dashboards, keys, vendors).

**Myths [X]:** the publishable/anon key is public by design; RLS on with no policy is closed; CORS only stops browsers reading; `SameSite=Lax` covers unsafe methods only and sibling subdomains are same-site; only a signed event or API lookup proves payment; a signed URL works until it expires; obfuscation and root detection protect no secret.

## Gaps (still to research)

ASVS 5.0 chapters V1, V3, V4, V9, V11 to V13, V15 and MASVS control texts not read in full; Apple receipt pages need a browser pass; PCI DSS SAQ A for embedded payment forms after 2025 unclear (vendor summaries disagree); vendor facts (Supabase, Stripe, Upstash, Cloudflare, Expo) re-check every 3 to 6 months.
