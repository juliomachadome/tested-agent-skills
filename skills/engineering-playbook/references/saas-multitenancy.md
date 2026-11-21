# SaaS & Multi-Tenancy

## 1. Tenant isolation models

| Model | Isolation | Cost/ops | Use when |
|---|---|---|---|
| Shared DB, shared schema, `TenantId` column | logical (app-enforced) | cheapest, simplest ops | default for SMB SaaS, many small tenants |
| Shared DB + Row-Level Security | logical, DB-enforced | low | same as above with defense in depth |
| Schema per tenant | medium | migrations × N | moderate number of tenants needing separation |
| Database per tenant (elastic pools) | strong | higher, migrations × N, connection management | enterprise/regulated tenants, data residency, noisy tenants |
| Hybrid | per tier | | free/pro shared, enterprise dedicated |

## 2. Enforcing tenant isolation (shared schema)

- **Resolve tenant from the authenticated identity** (token claim, membership lookup) — never from a header/body the client controls without verification. Subdomain/route tenant must be checked against the user's memberships.
- Store it in a scoped `ITenantContext`.
- **EF Core global query filter:** `modelBuilder.Entity<Order>().HasQueryFilter(o => o.TenantId == _tenant.Id)` — and set `TenantId` automatically on insert (SaveChanges interceptor). `IgnoreQueryFilters()` only in audited admin code.
- **Database RLS** (SQL Server security policies with `SESSION_CONTEXT`, Postgres `CREATE POLICY ... USING (tenant_id = current_setting('app.tenant_id')::uuid)`) as a second layer.
- **Every** index that serves tenant queries starts with `TenantId`; unique constraints are usually `(TenantId, X)`.
- Caches, blob paths, search indexes, queues, logs and metrics must include tenant id in keys/partitions.
- Background jobs carry tenant id explicitly (no ambient HTTP context).
- **Tests:** automated cross-tenant tests for every endpoint category (user of tenant A requesting B's ids → 404).

## 3. Noisy neighbor

- Per-tenant rate limits and quotas (API calls, storage, AI tokens, jobs).
- Fair queuing (per-tenant partitions/sessions) so one tenant's bulk import doesn't delay everyone.
- Monitor per-tenant resource usage; move heavy tenants to dedicated resources.

## 4. Plans, entitlements & feature flags

- Separate **plan** (commercial) from **entitlements** (what features/limits a tenant has) — check entitlements in code, never plan names (`if (plan == "Pro")` breaks on every pricing change).
- Central entitlement service/table: features (bool), limits (numbers), usage counters.
- Enforce limits server-side and atomically (usage counter with conditional increment).
- Feature flags (LaunchDarkly, Unleash, Azure App Configuration, Microsoft.FeatureManagement) for rollout, separate from entitlements.

## 5. Billing (Stripe or similar)

- The payment provider is the source of truth for subscription/payment state; sync via **webhooks** (verified, idempotent, out-of-order safe — re-fetch the object from the API when in doubt).
- Model: customer ↔ tenant, subscription, price, invoice, payment status; store provider ids.
- Handle: trials, upgrades/downgrades with **proration**, cancellations at period end, failed payments (**dunning**: retries, emails, grace period, then restrict), refunds, taxes (Stripe Tax / VAT rules in the EU: B2B reverse charge, VAT id validation via VIES), currency.
- Usage-based billing: record usage events idempotently, aggregate, report to provider; reconcile.
- Never trust client-side "payment succeeded" redirects — confirm via webhook/API.
- PCI DSS: use hosted checkout/elements so card data never touches your servers (SAQ A).

## 6. Onboarding & lifecycle

- Tenant provisioning as an idempotent, resumable workflow (create tenant, seed data, default roles, billing customer, welcome email).
- Invitations with expiring single-use tokens; roles per tenant membership (a user can belong to several tenants).
- Offboarding: export data, retention period, hard delete (GDPR erasure), revoke access and API keys.

## 7. Operations

- Migrations across all tenants (DB-per-tenant): orchestrated, resumable, versioned per tenant.
- Per-tenant configuration and branding stored as data, cached.
- Audit log per tenant (who did what, when) — often a sales requirement for B2B.
- Data residency: region per tenant if required by customers.
- Backups and point-in-time restore per tenant (hard in shared schema — design export/restore tooling).

## 8. SaaS metrics (for product decisions)

- **MRR/ARR**, **churn** (logo and revenue), **NRR** (net revenue retention), **ARPA**, **CAC**, **LTV** (and LTV:CAC ≥ 3 as a common benchmark), **payback period**, activation rate, DAU/MAU, trial-to-paid conversion.
- Instrument product events (signup, activation milestones, feature usage) with tenant and plan dimensions.

## 9. Defense in depth: explicit filter plus RLS

- **Every repository method filters by tenant id explicitly, even when RLS is active.** RLS is a safety net with known holes (owner bypass without `FORCE`, superuser and `BYPASSRLS` roles, unique/foreign-key checks that ignore it, policies that read other tables racing under Read Committed). An explicit filter also makes the query plan and the tests honest, and a forgotten filter then shows up as an empty result in tests instead of a leak in production.
- **One door to tenant data:** a single wrapper (for example `withTenant(id, fn)`) opens a transaction, sets the tenant with `SET LOCAL`/`set_config(..., true)` and runs the work. All reads and writes go through it; the ORM client is importable only inside the persistence adapters (lint-enforced). Details of the SQL: databases.md section 18.
- **Jobs and consumers carry the tenant id in the payload** and open the same wrapper; there is no ambient request context in a worker.
- **Cross-tenant tests are mandatory:** for each endpoint category, tenant A asking for tenant B's ids gets 404, and a repository called without a tenant context returns nothing. Run them against a role that is subject to RLS.
- Logs carry tenant id and request id, never message content, emails or names.

## 10. Per-tenant LLM cost and quota

- Meter every LLM call per tenant: token counters per category (input, cached input, output; categories differ by provider) times the price of each category, stored as integer micro-units or `numeric`, with the price table and exchange rate versioned and recorded on each usage row.
- Enforce the quota with **reserve, call, settle:** an atomic reservation of the worst case in a short transaction, the model call outside any transaction, then a settlement that writes the real usage; failed calls also consume. Without the reservation, two concurrent generations overshoot the cap.
- Extra credit or overage is a **ledger entry** (who granted it, amount, reason, date), never an edit of the limit.
- Close billing periods in the tenant's own time zone.
- For routing, caching, batching and budget design see the `llm-engineering` skill (cost and latency optimization); this file only covers tenancy mechanics.

## Sources

- PostgreSQL docs, Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html (not re-verified)
- PostgreSQL docs, SET: https://www.postgresql.org/docs/current/sql-set.html (read 2026-11-15)
- Provider pricing and usage-field docs (categories of tokens change by vendor; check the vendor's current pricing page before encoding prices)
