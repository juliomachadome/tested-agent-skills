# Playbooks: practical routines

Templates and checklists to copy into the project's own runbook. Project rules win over these. `[n]` = `BIBLIOGRAPHY.md`. Evidence: the vendor facts were read on 15/11/2026; the routines themselves are practice ([F]) shaped by release-engineering and incident-handling sources `[2]` `[3]` `[4]` `[10]`.

## 1. Deploy runbook by SHA, with a healthcheck gate
**Before**
1. CI is green on the exact SHA; write it down: `SHA=<40 chars>`.
2. Target environment named; the migration in this release is additive (section 4); required variable names exist in this environment (names only); public build-time variables will be rebuilt `[23]`.
3. Rollback written first: previous SHA, the command, and for data the forward fix or the verified backup.
4. Check freeze windows and who is reachable for the next hour.

**During**
5. Deploy by SHA (never "redeploy" without one). Watch build, deploy, healthy to the end `[15]`.
6. Migrations run once, from one place, with a lock, before or with the code that needs them.

**Gate (all must pass before the word "live")**
7. `/health` and `/ready` answer 2xx, and the reported commit equals `$SHA`.
8. One read-only smoke of the main path (entry page, login, one product action); workers prove themselves with a log line or a no-op job.
9. Error rate and latency show no new spike over 10 minutes; webhooks and schedules still delivering `[2]`.
10. Everything switched on for the deploy or test (GPU, extra replicas, debug flags, previews) is off, and the spend per hour was read.

Report line: `done: command · output (exit code) · SHA live · before/after · rollback command · what is still on · spend checked · not verified`.

## 2. Environment matrix and secret separation
| | dev (local) | preview | staging | prod |
|---|---|---|---|---|
| Data | seed or synthetic | synthetic, short-lived | scrubbed copy or synthetic | real |
| Database | local or throwaway | branch or shared test, never prod | own project | own project, backups tested |
| Secrets | `.env.local`, never committed | scoped to Preview `[23]` | own values | own values, write-only `[23]` |
| Third-party keys | test mode | test mode | test mode | live mode |
| Who can deploy | anyone | on push | on merge | owner or release job, by SHA |
| Alerts | none | none | to chat | to phone |
| Cost cap | n/a | delete on merge | small | budget and alert (section 7) |

Rules: preview never receives production keys or the production database; QA never holds real personal data; one secret per environment and per service, never copied between them `[12]`; the differences between environments are a written list, not memory `[1]`. Test: "could this repository be made public now without leaking anything?".

## 3. Secret rotation runbook
Inventory per secret: purpose, provider and environments that hold it, consumers, owner, last rotation, what breaks when it changes. Scheduled rotation for machine secrets (for example every 90 days **[F]**); human credentials on suspicion `[12]`.

**A. Exposed but not yet abused (no downtime).** Example: one email-API key used by a web app on Vercel and a worker on Railway.
1. Create a second key at the provider (two valid keys at once).
2. Set the new key in every consumer and environment (names only on screen); redeploy each by SHA, because variables apply only to new deployments `[23]`.
3. Prove each consumer: health, then one small real operation that uses the key (one test email), and the provider panel shows traffic on the new key.
4. Revoke the old key only after step 3 is green for every consumer (a revoked key cannot be restored). Watch errors for 15 minutes; a forgotten consumer fails loudly here.
5. Clean the place it leaked (log, chat, file); delete or rewrite the log if the platform allows `[48]`.
6. Review the provider's usage for the exposure window; record date, who, the names (never the value).

**B. Abused or public (stop the bleeding).** Revoke first, accept a short outage on the affected function, then steps 1-3, 5-6. For a public repository or a client bundle, assume copies exist.

Side effects to announce: rotating a session-signing secret logs everyone out; rotating a rate-limit token resets counters; a database password change breaks every service holding the old URL; for a signing key with a current and a next slot (QStash), promote the next key, update consumers, then roll a new next key `[41]` (the order is an inference, test it in staging).

## 4. Rollback runbook: code versus schema
Code rolls back by redeploying or promoting the previous deployment; the database does not roll back with it `[26]` `[15]`.

**Expand, migrate, contract**
1. **Expand** (release N): add the new column, table or enum value; nullable or with a default; old code keeps working. Safe to roll back N to N-1.
2. **Migrate** (release N or N+1): code writes to both, a backfill job fills old rows in batches, readers prefer the new column.
3. **Contract** (release N+2, later, after the rollback window): remove the old column and the dual-write. Irreversible: run it only after a verified restore `[33]`.

**Rollback decision**
- Bug in code, schema additive: roll back the code (previous SHA); check nothing else depends on the new column.
- Bug plus destructive migration already ran: roll forward with a hotfix; restore into a new project and copy back only if data is corrupt.
- After a Vercel rollback, auto-promotion of production is off until you promote a deployment `[26]`; public variables stay as built.
- Railway: confirm the target is inside the plan's retention window `[15]`.
Always: rollback command written before deploying; after rolling back run the gate in section 1 and open an incident note (section 8).

## 5. Backup and restore drill (quarterly, timed)
Pick a date each quarter; the owner approves the cost of a temporary project.
1. Record the target: RPO and RTO the business accepts (for example RPO 24 h, RTO 2 h) and what the plan gives: daily retention 7/14/30 days by plan, PITR worst-case RPO 2 min as an add-on `[29]`.
2. Start a stopwatch. Restore the latest backup, or a PITR point, into a **new** project, never over production `[29]`.
3. Check: row counts per main table against production; the last known record; extensions; roles and grants; function privileges; reset custom role passwords; storage objects (not in the backup, restore them from their own copy) `[29]`.
4. Connect a staging copy of the app to it and run the smoke path.
5. Stop the stopwatch. Compare with the RTO. Write the log: date, backup used, minutes for restore, verification, repoint; failures found; owner of each fix.
6. Delete the temporary project. A backup that was not restored this quarter is "unproven" in the inventory.
Worked example: 18 GB database, restore 38 min + checks 12 min + repoint 10 min = 60 min against an RTO of 120 min: pass with 60 min margin; worst-case loss with a 03:00 daily backup and an incident at 17:20 is 860 min of data, so the 24 h RPO holds but a payment-heavy product should consider PITR.

## 6. Incident checklist for a solo operator
1. **Declare and time-stamp** (one line: what users see, since when). Open a notes file; every action gets a time.
2. **Stop the bleeding** with the smallest reversible action: roll back the last deploy, pause the service, scale the GPU to zero, disable the feature flag, rotate the leaked key. No cleanup yet.
3. **Run Step 0** of `diagnosis-playbook.md`: SHA, environment, recent changes.
4. **Communicate:** a short status line to users or the owner now, an update every 30-60 min; say what you know, what you do not, the next update time.
5. **Fix forward only with a rollback ready;** one change at a time, each verified.
6. **Verify recovery** with the gate (section 1) and the user-visible symptom, not only the dashboard.
7. **Postmortem within 3 days** (section 8) if a trigger was met: user-visible degradation, data loss, any manual rollback `[2]`.
Rules for a tired person: no destructive command without reading what it removes; no production change from a phone unless it is a rollback; call someone when money, personal data or an irreversible step is involved.

## 7. Cost guardrails
**One row per variable cost; fill it in once, review monthly.**
| Item | Plan | Hard cap | Alert at | Idle cost | Check |
|---|---|---|---|---|---|
| App hosting / containers | | usage hard limit (min USD 10) `[17]` | 75% / 90% | sleeping? | after each deploy |
| Front-end platform | | spend management | | | monthly |
| Database | | | | | monthly |
| Object storage | | | | | monthly |
| Redis / queue | | | | | monthly |
| GPU | | prepaid balance; hourly limit (default USD 80/h) `[43]` | | must be 0 | after every test |
| Email | | | | | monthly |
| LLM / AI APIs | | per-key budget | | | weekly |

Guardrails: (1) an alert before the cap, a cap that you chose knowingly (a hard limit on the container platform takes all workloads offline `[17]`, so set it above the worst expected month and treat a hit as an outage); (2) idle spend checked at zero after every test: workers 0, spend per hour 0 `[43]`; (3) scale-to-zero checks: list what keeps a service awake (polling, pooled connections, telemetry, pings `[18]`); (4) previews deleted on merge; (5) a monthly 10-minute review of the top three lines against last month; (6) cost per unit, not only total: per visit, per customer, per active customer per day (the third surprises); infrastructure under 1-2% of revenue is not the problem, complexity is **[F]** `[11]`.

## 8. Blameless postmortem template
Trigger and date · impact (who, how long, what data or money) · timeline with timestamps · detection (how we found out; how long it took) · cause (systemic: why did the system allow it) · what went well · what went badly · action items each with owner, date and a test or alert that would catch a repeat `[2]` `[3]`. No names as causes. Store them in one place; review the open items monthly.

## 9. New-service checklist
Owner named · repository and SHA-based deploy path · environment variables listed by name per environment, none in the repo `[1]` · health and ready endpoints (shallow for the platform, deep for the monitor) `[14]` · graceful `SIGTERM` handling and a draining window `[15]` · region chosen next to its data, residency decided with the data-protection owner `[25]` · logs as JSON with request ids and no personal data `[1]` · external uptime monitor and one symptom alert that reaches a phone `[2]` · resource limits and a hard spend cap with an alert · idle-cost check (does it sleep, does it bill at zero) · timeouts and retry policy on every outbound call, retries only on idempotent operations `[9]` · backup and restore plan with the first drill date · secrets inventory row and rotation date · rollback command written · image pinned by digest, non-root `[47]` · runbook entry (where it lives, how to stop it, who to call).

## 10. Load balancer and autoscaling on managed platforms
Facts read 18/11/2026 on the pages cited; re-check before relying on a limit. Design theory: `software-architecture/references/scaling-load-balancing.md`.
- **Health check path and readiness**: one cheap endpoint that returns 2xx only when the app can serve (listening on the injected `PORT`, migrations done, critical dependency reachable for readiness). Keep liveness separate and local, so a database blip does not restart everything `[58]`. Railway polls the path on deploy and switches traffic only after a 2xx (default timeout 300 s); it does not monitor after the deploy is live, so add an external monitor `[14]`.
- **Draining on deploy**: on SIGTERM stop accepting new work, finish in-flight requests, then exit; Railway says removed replicas drain gracefully `[55]`, but its pages do not state the drain length (not verified), so measure your longest request and test a deploy under load. Services with an attached volume can see brief downtime on redeploy `[14]`.
- **Min instances vs cost**: Railway scales each service vertically up to the plan limit and adds replicas manually (staged change, no full redeploy); metrics are summed over replicas `[55]`. Always keep 2 replicas only where an outage costs more than the second instance; otherwise one instance plus a fast restart is the cheaper honest choice. Cold starts matter only when scaling to zero.
- **Sticky sessions**: Railway does not support them; traffic goes to the nearest region, then randomly among its replicas `[55]`. So keep sessions in a cookie or shared store. WebSockets need a pub/sub backplane or one replica until you have one.
- **Where the platform already balances**: Railway (replica random balancing, above) `[55]`. Vercel Functions scale automatically on demand, run several invocations per instance with Fluid compute, pre-warm production and fail over across availability zones (and regions on Enterprise) `[56][25]`; you do not run a balancer. Cloudflare Load Balancing is a product you configure: monitors from several data centers, steering by latency or region, failover away from unhealthy endpoints `[57]`; its session affinity settings were not read.
- **Connections multiply**: more replicas or function instances mean more database connections; use a pooler and cap the pool per instance (see `supabase.md`). Vercel shares 1,024 file descriptors across concurrent executions `[25]`.
- **Overload**: rate limit at the edge and shed early with 429/503; do not rely on autoscaling alone `[59]`.
