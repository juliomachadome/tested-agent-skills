# Cost and multi-region design

Design-time view only. Running the platform, deploys, rotation, bills and rightsizing: `skills/cloud-deploy-ops`. Prices are illustrative assumptions, not quotes; check the provider price page. Tags as in SKILL.md; `[n]` = `BIBLIOGRAPHY.md`. Security: `security-architecture.md`.

## 1. Cost architecture

### C1 Cost as a design input
Treat cost like latency: a characteristic with a target. Express it per unit that earns money: cost per request, per tenant, per active user, per report. Measure business output against spend, and attribute spend to owners `[45]` **[M]**. Put "cost per request" as a fitness function and a line in every ADR (`adr-template.md`). A design that cannot be priced per tenant cannot be priced to customers.

### C2 Worked cost model (assumptions, then the arithmetic)
Assumed monthly workload: 30 M requests, 400 tenants, 2,000 GB stored, 1,500 GB internet egress, 500 GB cross-zone or cross-region transfer.
| Line | Assumption | USD/month |
|---|---|---|
| Compute | 3 small containers x $0.05/h x 730 h | 109.5 |
| Database | managed, HA, one size up | 450 |
| Cache | managed small | 60 |
| Storage | 2,000 GB x $0.023 | 46 |
| Egress | 1,500 GB x $0.09 | 135 |
| Observability | logs, metrics, traces | 120 |
| Transfer | 500 GB x $0.02 | 10 |
| **Total** | | **930.5** |
Per 1,000 requests: 930.5 / 30,000 = $0.031. Per tenant: 930.5 / 400 = $2.33; at a $25 plan that is 9.3% of revenue before staff and payment fees (margin on infrastructure 90.7%). Sensitivity: if egress doubles the total is $1,065.5 (+14.5%); if tenants halve but costs stay, per-tenant cost doubles to $4.65, so check fixed vs variable lines. Reproduce with python3 when numbers change.

### C3 Managed vs self-hosted break-even
Self-hosting is cheaper only when the saved fee exceeds the staff time: break-even hours per month = (managed price - self-hosted infra) / loaded hourly rate. Example: ($450 - $180) / $80 = 3.4 h/month. Backups, patching, failover tests, upgrades and on-call usually exceed that, so default to managed unless scale, a feature gap or a lock-in or residency constraint says otherwise **[F]**. Count the hours honestly, including the incident that happens once a year.

### C4 Serverless vs containers vs VMs
- Pay-per-use (functions): cost grows linearly with requests, near zero when idle, with cold-start and duration limits. Assumed price: $0.20 per million invocations plus $0.0000166667 per GB-second, 0.25 GB, 120 ms: 3 M requests = $2.1, 30 M = $21, 100 M = $70, 300 M = $210.
- Always-on containers: fixed floor (the three above = $109.5) plus headroom, flat until you add nodes. Crossing point in this example: about 156 M requests/month; below it functions win, above it containers win, ignoring ops time, cold starts and gateway fees (which move the line, so recompute with real prices).
- VMs: cheapest per unit at steady high utilisation with reserved or committed pricing; you pay for idle and for patching.
Rule: spiky or low volume, serverless; steady and high, containers or committed VMs; measure utilisation before committing. Commitment discounts are a bet on stable load; commit to the floor, not the peak `[F]`.

### C5 Egress, transfer and storage tiers
Data leaving a provider, a region or sometimes a zone is billed; the cheapest byte is the one not moved. Keep chatty services in one zone or region, serve media through a CDN, compress, do not replicate everything cross-region. Storage tiers: hot, infrequent access, archive; with lifecycle rules. Example: 2,000 GB all hot = $46; 600 GB hot plus 1,400 GB at $0.004 = $19.4 (-58%), minus retrieval fees and minimum durations, which can erase the gain for data read often.
Multi-region cost: a warm standby adds roughly the standby compute plus replication transfer and storage; an active-active setup can approach double the infrastructure (here about $1,720 vs $930). Compare against the cost of downtime (R1 below).

### C6 FinOps loop
Inform (visibility and allocation), Optimize, Operate: a repeating loop with engineering, finance and business together; data must be accessible, timely and accurate, and each team owns its usage `[44]` **[M]**. Capabilities: allocation, unit economics, budgeting `[44]`. Minimum viable set: mandatory tags or accounts for owner, environment and product (tag keys the provider reports on; untagged spend is reported weekly); budgets with alerts at 50/80/100% and a named owner; a unit-cost dashboard (cost per request, per tenant, per active user) next to revenue; a monthly review that closes at least one saving or accepts one cost with a reason. Dev and test resources that run only working hours save about 75% (40 of 168 h) `[45]`. Operations, rightsizing and purchases: `skills/cloud-deploy-ops`.

## 2. Multi-region and resilience

### R1 When one region is enough
Most products: yes. Multi-AZ inside one region already covers most disasters (fire, power, one zone failing); multi-region protects against a whole-region event or is needed by latency, residency or contract `[43]`. Check first: what is the downtime cost per hour, what does the SLA promise, and is the weak point actually the region (more often it is a bad deploy, a database or a dependency). 99.9% allows 43.2 min/month of downtime; 99.99% allows 4.32 min. A strategy more stringent than needed adds cost for nothing `[43]`.

### R2 RTO and RPO, and the four strategies
RTO = how long you may be down; RPO = how much data you may lose. Set both per workload from business impact `[43]`. Strategies, in rising cost and complexity, falling RTO and RPO `[43]`:
| Strategy | RPO | RTO | What runs in the second region |
|---|---|---|---|
| Backup and restore | hours (minutes with point-in-time) | up to a day | backups only |
| Pilot light | minutes | tens of minutes | data replicated, compute off |
| Warm standby | seconds | minutes | scaled-down working copy |
| Active-active | near zero | near zero | full copy serving traffic |
The figures are the source's orders of magnitude, not guarantees. Replication does not protect against corruption or deletion: keep versioned or point-in-time backups, also in the recovery region `[43]`.

### R3 Active-passive vs active-active
Active-passive: one write region, standby promoted on failure; simple, one source of truth, failover loses the replication lag (your actual RPO) and needs a failback plan (re-sync old primary as replica) `[43]`. Active-active: every region serves and writes; lowest latency and downtime, but concurrent writes to one record need prevention or merge: partition by tenant or user so each record has one home region, or use conflict-free types, last-writer-wins (loses data silently), or application merge **[M]** (Kleppmann `[1]`, `data-systems.md`). Choose it only when requirements force it; it is the most operationally complex option `[43]`.

### R4 Data residency
Country-neutral rule: for each class of personal or regulated data, check the rules of the data subject's country (and the sector regulator and customer contracts) on where data may be stored, processed, accessed from and backed up; get a qualified opinion before launch. Design implications: region per tenant recorded at signup, data and backups kept in the allowed region, logs and analytics included, support access controlled, no cross-region replication of restricted data. If a country has one provider region, multi-AZ is the resilience option, not multi-region `[43]`. See the privacy law of the data subject's country (official regulator pages).

### R5 Failover routing
DNS-based or global load balancing routes to healthy regions (`scaling-load-balancing.md` 9). DNS answers are cached, so failover time includes TTL and resolver behaviour. Automatic failover on health checks can fail over on a false alarm, which costs availability and data, so many teams automate the steps but keep a human trigger `[43]`. During recovery use data-plane operations that stay up, not control-plane calls that may be down `[43]`. Pre-provision or reserve capacity in the standby; scaling up a cold region during a regional outage competes with everyone else.

### R6 Cell-based architecture
Split the system into independent cells, each a full copy serving a fixed subset of tenants, with a thin router above. A failure, bad deploy or noisy tenant hits one cell: blast radius = 1/N of users, and deploys roll cell by cell **[F]** (practitioner pattern; no source opened). Costs: more capacity headroom, a routing layer that must be simpler than the cells, cross-cell queries and migrations between cells. Fits tenant-partitioned products; relates to bulkheads (SKILL.md 8) and silo/bridge isolation (1.4).

### R7 DR tests and game days
An untested plan is a hope. Keep failover and failback steps in a playbook everyone can reach and review it regularly; use common recovery patterns so tooling is shared `[43]`. Test restores from backup (time it against RTO, check data against RPO), run region-evacuation drills in a non-production copy first, then in production in a low-risk window with a rollback. Some teams rotate primary and standby on a schedule so the standby is always proven `[43]`. Record: time to detect, decide, recover; gaps become tickets.
