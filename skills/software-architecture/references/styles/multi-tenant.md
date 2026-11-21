# Style: multi-tenant SaaS (silo, pool, bridge)

One product serving many customers (tenants) with controlled isolation and cost. Numbers [n] refer to `../BIBLIOGRAPHY.md`. Data-level code detail: `skills/engineering-playbook` (saas-multitenancy).

## When it fits / does not
Fits: B2B or B2C SaaS with many tenants of mixed size. A single customer, or fewer than a handful of very large ones with strict contracts, is better served by single-tenant deployments (silo) and a repeatable deploy. Mixed is normal.

## Models
- **Pool** (shared everything, tenant id on every row, row-level security): lowest cost, simplest ops, weakest isolation, noisy neighbour risk.
- **Silo** (database or whole stack per tenant): strongest isolation, per-tenant restore and region, highest cost and operational load (N migrations, N upgrades).
- **Bridge** (pool for small tenants, silo or cell for large or regulated ones; or schema per tenant): the usual end state. Plan the tenant router and the "move tenant" tool from the start **[M]** [24][25][27].

## Core principles
Authentication is not isolation [25]: derive tenant context from the verified session, never from the request body, and enforce it in a layer that every access passes (query filter plus database policy, scoped credentials, per-tenant keys). Tenant id in every log, metric, trace, cache key, queue message and file path. Per-tenant limits and fairness. Tenant lifecycle: onboarding, backup, export, deletion, offboarding. Tiering (plans) mapped to isolation level.

## Structure
Request middleware sets tenant context; data access layer applies it; policy in the database (RLS) or per-tenant credentials; a control plane (tenant catalogue, routing, billing, provisioning) separate from the application plane; cells (a full copy of the stack serving a set of tenants) to cap blast radius.

## Data ownership and consistency
Pool: `tenant_id` in every key, composite unique constraints, RLS using transaction-scoped settings (never session-level on pooled connections). Silo: connection routing by tenant, migrations orchestrated with a version per tenant and a failure path. Cross-tenant analytics through a separate pipeline with explicit access.

## Operations and failure modes
Noisy neighbour (one tenant starves others: `../diagnosis-playbook.md` 8), cross-tenant leak (the worst failure), per-tenant migration drift, hot tenant on a shared partition, unbounded per-tenant cost, support access without audit, cache or queue key without tenant. Measure per-tenant CPU, queries, storage, requests and cost; top-1 tenant share; leakage test results.

## Per-tenant cost
Cost per tenant = attributable usage (compute share by requests or CPU-seconds, storage, egress, third-party calls) + allocated shared cost. Example: 200 tenants, total infra 6,000/month, shared fixed 2,000 spread evenly (10 each) and variable 4,000 by request share; a tenant with 8% of requests costs 10 + 320 = 330 against a plan price that must clear it. Use it to price tiers and to decide who moves to a silo.

## Migration in and out
In: add tenant id and RLS to a single-tenant schema (backfill, constraint, policy, tests) before a second customer lands. Out/up: promote a tenant to a silo with dual-write or snapshot plus replay, then flip the router; keep the tool and a rollback.

## Checklist
Do: deny by default; tests that attempt cross-tenant reads on every endpoint and job; rate limits and quotas per tenant; tenant-scoped caches and queues; per-tenant backup and delete; audit privileged access.
Avoid: trusting a tenant id from the client; global caches; session-level settings on pooled connections; one shared admin credential; a different code path per big customer.

## Fitness functions
Automated cross-tenant access test suite in CI; lint or query test that tables with `tenant_id` have RLS enabled; log scan for lines without tenant id; per-tenant resource ceiling tests; cost-per-tenant report with alert; migration drift check across silos.

## Sources
AWS SaaS Lens [24] and tenant isolation whitepaper (marked historical by AWS) [25]; Azure multitenant guidance [27]; Kleppmann on partitioning [1]; SRE overload chapter for per-customer quotas [29].
