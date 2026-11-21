# Security architecture

Design-time view only. Code-level security and review: `skills/software-security`. Personal data law: the privacy law of the data subject's country (official regulator pages). Tags as in SKILL.md; `[n]` = `BIBLIOGRAPHY.md`.

### S1 Threat model at design time
Four questions: what are we building, what can go wrong, what do we do about it, did we do enough `[42]` **[C]**. Do it per feature or per change to a boundary, in 30-60 minutes, not once per year.
1. Draw a data-flow diagram: actors, processes, data stores, flows. Draw **trust boundaries** where the controlling party, network or privilege changes (browser/server, service/service, app/database, your system/third party, tenant/tenant). Boundaries are where checks must live.
2. For each element and each flow crossing a boundary, walk STRIDE `[41]` **[C]**: Spoofing (fake identity), Tampering (modified data), Repudiation (denied action, no proof), Information disclosure, Denial of service, Elevation of privilege.
3. For each threat choose: mitigate, accept, transfer or eliminate (remove the feature or the data) `[42]`. Eliminating data beats protecting it.
4. Write the result as ADR consequences or tickets; revisit after incidents and big changes `[42]`.
Output table: element or flow | STRIDE letter | threat | control | owner | test. The test column turns into a fitness function (`playbooks.md` 5).

### S2 Authn and authz placement
- Authentication once, at the edge or an identity provider; services receive a verified, signed identity (token with issuer, audience, expiry) and re-verify it. Never trust a user id from a header that any internal caller can set **[M]**.
- Authorization is two layers: coarse at the gateway (is this token allowed to call this API at all, rate limit, schema) and fine in the owning service or a central policy engine (can this subject do this action on this object). The gateway alone cannot know object ownership **[F]**.
- Central policy (policy as code, one decision point, many enforcement points) helps when many services share rules; it adds a latency and availability dependency, so cache decisions with short expiry and decide fail-closed vs fail-open per route, in writing.
- Service-to-service identity: workload identity or mutual TLS, not shared static keys.

### S3 Secrets and keys
No secrets in code, images, logs or client apps. Short-lived credentials from the platform identity over long-lived keys; a secret store with audit; rotation designed in (two valid versions during a switch). Encrypt at rest with keys held in a managed KMS or HSM, separate keys per tenant or data class when isolation or deletion needs it (crypto-shredding: destroy the key to delete data, including in backups). Keep people away from data: use tooling, not ad-hoc access `[F]`.

### S4 Tenant isolation (pool, bridge, silo)
Pool = shared everything, isolation by tenant id plus policy; bridge = mixed (shared compute, separate schema or database per tenant, or shared tier for small and silo for large); silo = separate stack or account per tenant `[25]` **[M]**. Choose by: contractual isolation demands, noisy-neighbour risk, per-tenant residency, blast radius, cost per tenant (`cost-and-regions.md` 1). Whatever the model, the isolation check must not depend on each developer remembering a filter: enforce it in one layer plus database policy, and test cross-tenant access. Pattern detail: `styles/multi-tenant.md`.

### S5 Zero-trust basics, blast radius, least privilege
Zero trust: no implicit trust from network location or ownership; verify user and device, then grant access to one resource, per request, with the least privilege that works `[46]` **[M]**. In practice: private subnets are not a control by themselves, each service authenticates callers, egress is allow-listed, admin access goes through an identity-aware path with MFA.
Blast radius: assume one credential, one service or one tenant will be compromised; design so that it reaches little. Separate accounts or projects for prod, staging and data; one role per service with only the actions and resources it uses; no wildcard policies; scoped, expiring tokens; per-tenant rate limits.

### S6 Audit logging
Log who did what to which object, when, from where, with outcome: authentication events, authorization denials, admin and privileged actions, data export, permission changes. Append-only, in a separate account or store that the audited system cannot edit, with retention set by law and risk, and no secrets or full personal data in the lines. Without it, repudiation cannot be answered and incidents cannot be scoped. Detail on personal data: the privacy law of the data subject's country (official regulator pages).
