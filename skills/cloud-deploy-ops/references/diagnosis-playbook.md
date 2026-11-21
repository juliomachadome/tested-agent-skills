# Diagnosis playbook: symptom, likely causes, check, fix

Use top-down. Step 0 first: most "mystery" incidents are a wrong assumption about what is running. Evidence tags: **[C]** consensus or vendor documentation read on 15/11/2026, **[M]** serious but single or inferred from docs, **[F]** practitioner or lived failure mode, **[X]** myth. `[n]` points to `BIBLIOGRAPHY.md`. Money in USD; rates are examples, replace them with the provider's price on the day. Nothing is copied from a source.

## Step 0: what is actually live, and where?
Ask for the evidence before any theory. Do not touch production to collect it unless the owner agreed.

| Question | How to get it | If unknown |
|---|---|---|
| Which commit SHA is serving traffic? | the service's own `/health` or `/version` (value baked at build), response header, or the deployment record; not "the last merged PR" | add `commit` to the health payload now; until then treat the SHA as unknown |
| Which environment and which service/project? | URL host, project id, region; an old "staging" service can hold the custom domain | list every service and domain mapped to the host |
| Which variables at build vs runtime? | names only, per environment: public build-time ones (`NEXT_PUBLIC_*`) were frozen at the last build `[23]`; server ones are read at start | compare the build log date with the date of the variable change |
| What changed in the last 24-72 h? | deploys, variable edits, DNS, plan changes, provider incidents, cron or schedule edits, dependency bumps | build the timeline before naming a cause `[2]` |
| What is the symptom as a user sees it? | a request with headers (`curl -sI`), a screenshot, a log line with request id | reproduce with and without cache (private window, `Cache-Control: no-cache`) |
| Is anything still running that I started? | GPU workers, preview deployments, extra replicas, local containers | list them before and after (section 5 arithmetic) |

Write the answer in one line: "live: SHA ?, env ?, built at ?, variables as of ?". If SHA is unknown, the first fix is observability, not code.

## 1. Production shows the old version after a deploy (dashboard says Active)
Order the checks from the platform outward to the user.

| Likely cause | How to check | Fix |
|---|---|---|
| Wrong service or environment got the deploy | compare the SHA in `/health` of the production URL with the one deployed; check which service holds the domain | deploy to the right target; remove stale domain mappings |
| Deploy without a SHA rebuilt an old source (API-triggered redeploy) **[F]** | deployment record shows an older commit; redeploy/rollback reuse the selected deployment's code `[15]` | redeploy by explicit SHA; require SHA in the script |
| Healthcheck passed on the old container, new one never became Active, or traffic not switched | state machine to the end: Building, Deploying, Active; "Active" is only container start when no healthcheck exists `[15]` `[14]` | add a deep enough healthcheck; read the deploy log for the failure |
| Deploy not promoted (Vercel: a previous rollback switched off auto-assignment of production domains, so pushes do not go live) `[26]` | project shows a rolled-back state; latest deployment is "Ready" but not the production deployment | `vercel promote <deployment>` to re-enable auto-assignment |
| Build cache reused stale inputs (monorepo cache that ignores variables) `[23]` | build log says cache hit; the bundle contains the old public value | list the variables in the cache key (`globalEnv`), clear cache, rebuild |
| Public variable changed but not rebuilt `[23]` | grep the shipped JS for the old and new value | redeploy after the change, then re-grep |
| CDN or browser cache serving the old asset or HTML | `curl -sI` for `age`, `cache-control`, `etag`; compare with an origin URL; hard reload | purge or lower TTL for the HTML shell; hashed asset names for the rest |
| Service worker serves the old app shell **[F]** | DevTools Application, Service Workers; "update on reload"; old SW still controls the tab | version the SW, skip waiting only when safe, ship a kill-switch SW once, tell the user to reload |
| Two regions or instances still draining | both SHAs appear in repeated `/health` calls | wait the overlap window, or check the draining setting `[15]` |

Done when: the SHA at the public URL equals the requested SHA, from two networks, with cache bypassed.

## 2. Deploy succeeds but the app crashes or fails its check
1. **Env var missing at build or at start.** Names diff between environments (never values): a variable that exists in staging and not in production is the usual case. A public variable missing at build is `undefined` in the bundle `[23]`. Fix: add it, rebuild; add a startup check that fails fast listing missing names.
2. **Port or host binding.** The platform injects `PORT`; the app must listen on it and on `0.0.0.0`, not `localhost` or a fixed port `[14]`. Symptom: "service unavailable" on the check although the process runs.
3. **Healthcheck path or host.** Path returns non-2xx (auth middleware, redirect to login), takes longer than the timeout (300 s default on Railway `[14]`), or a host allow-list rejects the probe host (`healthcheck.railway.app`). Fix: a fixed, unauthenticated, fast `/health`.
4. **Migration order.** New code needs a column the migration has not added yet (or the reverse: a destructive migration ran before old instances drained). Check the pre-deploy command log and the migrations table `[33]`. Fix: expand first, deploy, contract later (`playbooks.md` section 4).
5. **Memory or cold-start limits.** Exit code 137, "killed", build OOM; bundle over 250 MB on a function `[24]`. Fix: trim dependencies, raise memory, split.
6. **Image or lockfile drift.** `latest` tag moved, lockfile ignored. Fix: digest pin `[47]`.

## 3. Healthcheck flapping, or green deploy then errors an hour later
- The platform check is deploy-time only `[14]`: a pass proves the start, not the next hour. Add an external monitor on a deep check (database ping, queue age).
- Flapping with load: the check shares the saturated worker (event loop blocked, pool exhausted). Check CPU and connection use at the same minute; make `/health` independent of the pool, keep the deep check separate.
- Flapping at deploy only: slow boot (migrations, model load) beyond the timeout. Raise the timeout or move the work out of boot.
- Restart loop: read the exit code and last log lines first; a crash loop with growing bill is also a cost incident (section 5).

## 4. Cold starts and a slow first request
| Cause | Check | Fix |
|---|---|---|
| Scale-to-zero wake (Railway sleeping: first request may be slow or return 502; sleeps after about 5-10 min of no outbound traffic) `[18]` | latency of the first request after 15 min idle vs the next | decide: accept it, or keep one always-on replica and price it (section 5); callers retry idempotent reads only |
| Serverless GPU model load (cold start is billed and slow) `[43]` | job record: delay time vs execution time | smaller image, cached model on a volume, FlashBoot, accept and show progress; never raise idle timeout without the arithmetic |
| Function region far from the database (default `iad1`) `[25]` | trace: time per query; compare with region of the database | move the function region next to the database; add about 100 ms per query as the cost of a cross-ocean hop **[F]** |
| Connection setup on every request (no pooling, TLS each time) | trace shows connect time | module-level client, pooler |

Never "ping to keep warm" without pricing it: a ping every 4 minutes keeps the service awake and billing all month.

## 5. The bill doubled
Find the line that moved, not the total. Export usage by service and day; compare the same number of days.

| Suspect | Check | Worked number (assumptions stated) |
|---|---|---|
| **Idle or oversized GPU** | active workers above 0, idle timeout raised, endpoint stuck in a retry loop | assumed rate USD 0.00055/s (about 1.98/h). One active worker 24/7: 720 h x 1.98 = about USD 1,425/month with zero jobs. Serverless job: cold 20 s + exec 10 s + idle 5 s = 35 s x 0.00055 = USD 0.01925; 7,270 jobs = USD 140. Raise idle to 30 s and jobs rise 20%: 60 s x 0.00055 = 0.033; 8,724 jobs = USD 288. Doubling came from 1.71x per-job time times 1.2x volume, not from "more traffic" |
| **Egress** | provider's network line; large media served from the app host | Railway egress USD 0.05/GB `[16]`: 800 GB/month = USD 40; the same files from R2 have free egress `[37]` and about 100 GB x 0.015 = USD 1.50 storage |
| **Logs** | log volume per day, verbose level left on, a loop logging an error | cap level in production, sample, shorter retention; check the drain's own bill |
| **Always-on replicas / over-provisioned memory** | replica count, memory per service | upper bound at flat usage: 3 replicas x (1 vCPU x 20 + 2 GB x 10) = USD 120/month; actual bills follow use `[16]` |
| **Preview deployments** | list of previews with databases or workers attached | 5 previews x (0.5 vCPU x 20 + 1 GB x 10) = USD 100/month upper bound; delete on merge |
| **Redis or queue commands** | commands per day by key pattern | pay-as-you-go USD 0.20 per 100K `[42]`: a poll every second = 86,400 x 30 = 2.59 M commands = about USD 5.18/month per poller (1 command per poll assumed) |
| **A retry storm on paid calls** | duplicate job ids, submit timeouts | `/run` has no idempotency key `[45]`; each duplicate is billed; track by job id |

Fix order: stop the bleeding (scale to zero, pause), prove spend per hour is zero, then set a budget and an alert (`playbooks.md` section 7).

## 6. A secret leaked
Revoke first when the secret is abused or public; rotate in the no-downtime order when it is only exposed to a small circle. Both orders are in `playbooks.md` section 3. Triage questions: where did it appear (log, chat, public repo, bundle), which services hold it, what can it do, is there activity in the provider's usage panel during the window `[12]`. If it reached a browser bundle it was public from the first deploy: rotate immediately and move the call server-side. A restart does not revoke a stolen credential.

## 7. Database connections exhausted
Symptom: "too many connections", "remaining connection slots", timeouts under load, pooler errors.

Arithmetic: connections = instances x pool size per instance (+ workers + migrations + admin tools). Example: 40 warm serverless instances x 10 (a common driver default `[30]`) = 400 connections against a Micro compute with 60 direct and 200 pooler clients `[32]`: exhausted. With the transaction pooler and `max: 1`: 40 clients, inside 200. The pooler's pool to Postgres should stay under 80% of max connections (40% if the REST API is heavy): 0.8 x 60 = 48 `[31]`.

| Check | Fix |
|---|---|
| Which role holds the connections (`pg_stat_activity` by user and state) | one role per service; kill idle-in-transaction holders |
| Serverless fan-out: instances x pool | pooler transaction mode (6543), `max: 1`, disable prepared statements `[30]` |
| Session features in transaction mode (SET, LISTEN, temp tables, advisory session locks) | move that code to a direct or session connection; use `SET LOCAL` `[30]` |
| Long transactions or missing timeouts | statement timeout per role `[35]`, client timeout for slow calls |
| Migrations or backups through the pooler | use the direct connection |

## 8. Backups exist but the restore fails
A backup is proven only by a restore `[10]`. Check in this order: (1) the backup is the one you think (plan retention: 7/14/30 days; PITR replaces daily backups `[29]`); (2) restore went into a new project, not over production; (3) what the backup does not hold: Storage objects (metadata only) and custom role passwords `[29]`; (4) extensions, roles, grants and function privileges after restore; (5) subscriptions and replication slots dropped first and recreated; (6) row counts and a known recent record; (7) the application connects with the restored credentials. Record the timed result in the drill log (`playbooks.md` section 5). If the dump is yours (`pg_dump`), restore it into an empty database with the same major version and the same extensions.

RPO and RTO in numbers: RPO is the data you can lose, RTO the time to be working again. With one daily backup at 03:00 and an incident at 17:20, the worst loss is 14 h 20 min = 860 min. With PITR the stated worst case is 2 minutes `[29]`. RTO is measured, not promised: example drill on 18 GB: restore 38 min + verification 12 min + repoint 10 min = 60 min. Contingency-planning guidance gives the vocabulary `[13]`; the numbers are yours.

## 9. Cron or queue jobs duplicated or missed
- **Duplicated:** at-least-once delivery plus a slow wake (a 502 triggers a retry) `[40]`; two instances each running an in-process scheduler; a deploy overlap running the old and the new scheduler. Fix: idempotency key per job, one scheduler owner, lock or lease; respond 489 for permanent failures so they stop `[40]`.
- **Missed:** workflow schedules on the default branch only, delayed or dropped under load `[54]`; the receiver was asleep and returned 502 past the retries; the signature check rejects because the signing key was rotated `[41]`; database cron job exceeded 10 minutes or the 8-concurrent limit `[36]`. Fix: monitor "last success" age, not "job exists"; alert when a heartbeat is late.
- **Retries on paid work:** see section 5, retry storm. Backoff with jitter and a retry budget `[9]`.

## 10. Region latency or data-residency mismatch
Latency: compute and database in different regions add the round trip to every query; measure per-query time in a trace before moving anything `[25]`. Residency: where personal data lives (database region, object bucket jurisdiction, GPU provider, log drain, email provider) is a legal decision with the data-protection owner: the privacy law of the data subject's country (official regulator pages). Check the actual region of each store, not the dashboard default; note that some providers have no region in a given continent (Railway has no South America `[19]`) and that some choices are fixed at creation (R2 jurisdiction `[51]`).

## 11. Rollback restored the code but not the data
Symptoms after a rollback: errors about missing columns, enum values or rows the old code does not understand; double processing of jobs; the old build with new-format data. Cause: code rolls back in seconds, the database does not `[26]`. Check which migrations ran after the target SHA; whether the old code tolerates the new schema (expand step) or not (contract step ran). Fix: roll forward with a hotfix when the migration was destructive; restore a verified backup into a new project only when data is corrupt; keep the old environment variables and public values in mind, because Vercel rollbacks keep the built values `[26]`. Prevention: expand-contract, one irreversible step per release, the rollback plan written before deploying (`playbooks.md` section 4).

## Output of a diagnosis
Live state from Step 0 (SHA, environment, evidence); the tree branch followed with the command and its output; most likely and second cause; the smallest reversible fix, its rollback and who approves it; money or data at risk; what could not be verified and what you need from the owner.
