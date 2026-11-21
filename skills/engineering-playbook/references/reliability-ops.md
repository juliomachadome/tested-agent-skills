# Reliability, Observability & Delivery

## 1. Observability — three signals

- **Logs:** discrete events. **Structured** (JSON, message templates: `logger.LogInformation("Order {OrderId} paid {Amount}", id, amount)` — not string interpolation), with correlation/trace id, tenant id, user id (pseudonymous). Levels used consistently; no secrets/PII; sample noisy debug logs.
- **Metrics:** aggregated numbers over time (counters, gauges, histograms). Cheap to store, used for dashboards and alerts.
  - **RED** for services: Rate, Errors, Duration (p50/p95/p99).
  - **USE** for resources: Utilization, Saturation, Errors (CPU, memory, connection pools, queues).
  - Business metrics: signups, payments, plans generated, failures per tenant.
  - Avoid high-cardinality labels (user id, request id) in metrics.
- **Traces:** a request's path across services (spans). Find where latency goes.
- **OpenTelemetry** is the standard: .NET `AddOpenTelemetry().WithTracing(...).WithMetrics(...)` exporting to Azure Monitor/Application Insights, Grafana, Datadog, etc. Propagate W3C `traceparent` across HTTP and messages.
- .NET: `[LoggerMessage]` source-generated logging; `ILogger` scopes for request context; `System.Diagnostics.Metrics` for custom metrics; `ActivitySource` for custom spans.

## 2. SLIs, SLOs, error budgets

- **SLI:** measured indicator (fraction of requests < 300 ms and non-5xx).
- **SLO:** target (99.9% over 28 days). **SLA:** contractual promise (lower than SLO).
- **Error budget:** 100% − SLO (99.9% ≈ 43 min/month). Budget left → ship faster; exhausted → prioritize reliability.
- **Alert on symptoms users feel** (SLO burn rate, error rate, latency), not every CPU spike. Every alert must be actionable with a runbook.

## 3. Health & lifecycle

- **Liveness** (process alive — keep trivial) vs **readiness** (can serve traffic — checks critical dependencies) vs startup probes. ASP.NET Core `AddHealthChecks()` with tags.
- Don't make liveness depend on the DB (DB outage → all instances restarted in a loop).
- **Graceful shutdown:** stop accepting new work, finish in-flight requests/messages, honor cancellation tokens, within the platform's grace period.
- Config validation at startup (`ValidateOnStart()` with options) — fail fast on misconfiguration.

## 4. Resilience in operations

- Timeouts, retries, circuit breakers (distributed-systems.md).
- Redundancy across availability zones for critical services; know the platform's SLA and the composite SLA of dependencies.
- **Backups ≠ disaster recovery** until restore is tested. Define **RPO** (data loss tolerated) and **RTO** (downtime tolerated); rehearse restores.
- Chaos/fault injection in staging (Azure Chaos Studio) for critical paths once basics are solid.

## 5. Delivery (CI/CD)

- Trunk-based development with short-lived branches and PR review; main always deployable.
- CI: build, test, lint/analyzers, security scans, artifact versioning; CD: same artifact promoted through environments.
- **Feature flags** decouple deploy from release; clean them up after rollout.
- Safe deploys: blue-green/deployment slots (App Service swap), canary/progressive rollout, automatic rollback on SLO regression.
- DB migrations backward compatible with the previous app version (databases.md, expand/contract).
- Infrastructure as Code (Bicep, Terraform) reviewed like code; no click-ops in production.
- **DORA metrics:** deployment frequency, lead time for changes, change failure rate, time to restore service (plus reliability). Small, frequent changes reduce risk.
- **12-Factor app:** config in environment, stateless processes, backing services as attached resources, logs as event streams, dev/prod parity, disposability.

## 6. Incidents

- Severity levels, an incident commander, a status page/comms for customers.
- Mitigate first (rollback, flag off, scale), diagnose after.
- **Blameless postmortem:** timeline, impact, root causes (contributing factors, not a person), action items with owners.

## 7. Azure specifics (common stack)

- **Identity:** Managed Identity for app → Key Vault/SQL/Storage/Service Bus; `DefaultAzureCredential` in code; RBAC least privilege.
- **Secrets/config:** Key Vault + App Configuration (with feature flags); Key Vault references in app settings.
- **Functions:** plan choice (Consumption/Flex Consumption/Premium/Dedicated) drives cold start, scale, VNet, timeouts; isolated worker model for .NET (in-process model is being retired — verify current status); keep functions small and idempotent; Durable Functions for orchestrations; reuse clients statically; bindings' retry semantics differ per trigger.
- **Messaging:** Service Bus (enterprise features: sessions/ordering, DLQ, duplicate detection, transactions, topics) vs Storage Queues (cheap, simple, large backlog) vs Event Grid (event routing, push) vs Event Hubs (high-throughput streaming).
- **Data:** Azure SQL (serverless auto-pause has resume latency; elastic pools for multi-tenant DB-per-tenant), Cosmos DB (partition key design, RU cost), Redis (Azure Cache for Redis / Azure Managed Redis).
- **Networking:** private endpoints, VNet integration, Front Door/App Gateway WAF, API Management for gateways/rate limits.
- **Monitoring:** Application Insights (OpenTelemetry distro), Log Analytics (KQL), alerts with action groups, Azure Monitor workbooks.
- **Cost (FinOps):** budgets and alerts, right-size SKUs, autoscale, reserved capacity/savings plans for steady load, delete idle resources, watch egress and log ingestion volume (Log Analytics can become a top cost).
- Well-Architected Framework pillars: reliability, security, cost optimization, operational excellence, performance efficiency.

## 8. Runbooks & docs

- For each service: what it does, owners, dependencies, dashboards, alerts and their runbooks, how to deploy/rollback, how to restore data.

## Small-product reliability (one team, few instances)

- **Time budget per request:** the sum of a route's outbound timeouts must fit the caller's deadline (provider webhook, function max duration, user patience). Keep an **exit table**: for each destination (database, payments, email, storage, cache, AI) its timeout, retry policy and behavior when down. Source: Nygard, *Release It!* ch. 4-5 (not re-verified).
- **Fail fast:** validate configuration at boot and crash if something critical is missing; validate input and permission before expensive work. 12-Factor III.
- **Steady state:** everything that grows (logs, finished queue rows, derived files, closed sessions) has automatic cleanup.
- **Shallow and deep health:** a fixed `/health` for the deploy platform; a protected `/health/deep` reporting what matters (age of the last queue cycle, overdue jobs, failures in 24 h, a `select 1`), called by an external monitor.
- **Graceful shutdown:** on `SIGTERM` stop accepting work, finish the current work, exit; leased queue jobs recover what was cut (12-Factor IX).
- **Alert on symptoms, few and actionable:** API down, queue stalled, webhook failing, paid-but-no-access, email bounce spike. For a solo owner a daily digest that only arrives when something is wrong beats a dashboard.
- **Measure before concluding the cause:** per-route p50/p95 and database round-trips per screen show where time goes; "cold start" and "dynamic render" are hypotheses until measured. Sentry-style tracing: capture an exception once, sample traces (a low percentage in high traffic is a rule of thumb, not an official number) and exclude health routes. Source: Agans, *Debugging* (not re-verified).
- **Cost per customer and per active customer** estimated before launch; no free tier where customer data lives.

## Sources

- The Twelve-Factor App, https://12factor.net (not re-verified)
- Google, *Site Reliability Engineering*, https://sre.google/sre-book/ (not re-verified)
- Nygard, *Release It!* 2nd ed. 2018 (not re-verified)
- OpenTelemetry docs, https://opentelemetry.io/docs/ (not re-verified)
