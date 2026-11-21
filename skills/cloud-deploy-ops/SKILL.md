---
name: cloud-deploy-ops
description: "Railway, Vercel, Supabase, Cloudflare R2, Upstash, RunPod, Docker, GitHub Actions - invoke this skill FIRST, before running commands or answering, for any deploy or cloud-operations question, however short. Examples - \"prod still shows the old version after I deployed on railway\", \"set up staging and production for next.js on vercel + api on railway + supabase, keep secrets separate\", \"we leaked the resend api key in a log, rotate it across railway and vercel without downtime\", \"our runpod serverless bill doubled, make it cost 0 when idle\". Also env vars, healthchecks, rollbacks, regions, backups and restores, cost caps. Rules - deploy by commit SHA, healthcheck closes the deploy, idle spend checked at zero, backup proven by restore. Not for app code (engineering-playbook), slow pages (web-performance), RLS flaws (software-security), local docker-compose or GDPR region law, mobile store releases and app builds (mobile-app-engineering)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Cloud deploy and operations

Most incidents in small products are operational: the wrong commit went live, a variable changed in one environment only, a delete removed more than intended, a GPU billed overnight, an untested backup did not restore. Say it plainly: "Active" is not working, "deployed" without the SHA is not deployed, a backup without a restore is not a backup, "off" without zero workers and zero spend is not off. Evidence tags: **[C]** vendor documentation read or consensus, **[M]** serious but single or inferred, **[F]** practitioner or lived failure mode, **[X]** myth. Vendor numbers were checked 15/11/2026; `[n]` points to `references/BIBLIOGRAPHY.md`.

## 1. Start: project first, then the live state
Read the current project's CLAUDE.md or AGENTS.md, deploy notes, runbooks, ADRs and the glossary first; project rules override this skill, and a command you ran beats a document you read. Then fix **Step 0** in one line: which commit SHA is live, which environment and service, which variables at build versus runtime, what changed in the last 72 h. Ask for: the URL, the deploy or build log, `/health` output, the variable names per environment (never values), the plan, last month's usage by line. Without a SHA you cannot say what is running. Details: `references/diagnosis-playbook.md` Step 0.

## 2. Principles
1. **A release is an immutable build of one commit plus the config of one environment** **[C]** `[1]` `[4]`. Deploy by explicit SHA; call it live only when the running service reports that SHA. A redeploy without a SHA can ship an old source **[F]** `[15]`.
2. **The healthcheck closes the deploy;** Active alone means the container started `[15]`. Railway checks only at deploy time, so add an external monitor `[14]`.
3. **Config lives in the environment,** per environment and per service; the test is "could this repository be public now?" `[1]`.
4. **Variable changes apply to new deployments only,** and public build-time variables are baked into the bundle: change, redeploy, verify in the shipped bundle `[23]`.
5. **A leaked secret is revoked or rotated in a defined order,** then proven, cleaned and audited; agents handle names, never values `[12]`. Runbook: `playbooks.md` 3.
6. **Destructive actions only from an approved list;** prefer pause or scale-to-zero; read what a delete removes; write the rollback first **[F]**.
7. **Every variable cost has a cap and an earlier alert; idle spend is checked at zero after each test.** A hard cap can be an outage `[17]` `[43]`.
8. **Paid calls are not retried blindly:** submit endpoints may lack idempotency and each duplicate is billed `[45]`; retry only idempotent calls, with backoff and jitter `[9]`.
9. **A backup exists only after a timed restore into a new project;** know what it omits (Storage objects, custom role passwords) `[29]`. RPO is data you can lose, RTO is time to recover; measure both.
10. **Migrations are expand, migrate, contract;** rollback redeploys the previous SHA, the database stays `[26]`. Irreversible steps only after a verified restore.
11. **Environments are separate with a written list of differences;** preview never holds production keys or data.
12. **Region is latency and law.** Compute next to the database `[25]`; residency is the data-protection owner's decision.
13. **Scale-to-zero has rules:** pooled connections, telemetry and pings keep a service awake; the first request can be slow or 502 `[18]`.
14. **Shut down gracefully:** handle `SIGTERM`, drain, exit; some platforms give 0 s before `SIGKILL` by default `[15]`.
15. **Connections = instances x pool size.** Serverless uses the transaction pooler and a pool of 1 `[30]`.

## 3. Diagnose first
Run `references/diagnosis-playbook.md` top-down. After Step 0 pick the tree: old version live after deploy; deploy ok but crash; healthcheck flapping; cold starts; bill doubled; secret leaked; connections exhausted; backup restores fail; duplicated or missed jobs; region latency or residency; rollback without data. Each branch gives cause, check and fix, with worked numbers (idle GPU per month, egress, connections, RPO and RTO). Output: live state with evidence, branch followed with command and output, most likely and second cause, smallest reversible fix with its rollback, money or data at risk, what was not verified.

## 3b. Numbers to keep in your head
Idle GPU: workers x hours x rate, so one always-on worker at about USD 2/h costs about USD 1,400 a month with zero jobs; a serverless job bills cold start + execution + idle timeout, so raising the idle timeout from 5 s to 30 s can nearly double per-job cost `[43]`. Egress: GB x price (Railway USD 0.05/GB `[16]`; R2 egress free `[37]`). Connections: instances x pool per instance against the compute ceiling (Micro: 60 direct, 200 pooler clients `[32]`). Data loss window: time since the last backup (daily) or about 2 min with PITR `[29]`. Recompute with the provider's price on the day.

## 4. Routines
`references/playbooks.md`: deploy runbook by SHA with a health gate; environment matrix and secret separation; secret rotation without downtime; rollback and expand-contract; quarterly timed restore drill; cost guardrails and table; incident checklist for a solo operator; postmortem template; new-service checklist.

## 5. Which reference to open
| Need | Open |
|---|---|
| Something is broken or expensive | `references/diagnosis-playbook.md` |
| A routine to run or copy | `references/playbooks.md` |
| Railway (healthcheck, sleep, limits, regions, SMTP, config as code deprecated) | `references/railway.md` |
| Vercel (variables, protection, rollback, function limits, regions) | `references/vercel.md` |
| Supabase (pooler, connection limits, backups, PITR, migrations) | `references/supabase.md` |
| R2, QStash, Upstash Redis (presigned URLs, retries, prices) | `references/storage-queues.md` |
| Serverless GPU (billing, idempotency, spend limit) | `references/gpu-serverless.md` |
| Images, GitHub Actions hardening, observability | `references/images-ci-secrets-cost.md` |
| Outage, severity, roles, rollback-first, postmortem | `references/incident-response.md` |
| Sources, dates, verification status | `references/BIBLIOGRAPHY.md` |

## 6. Output of a task
`done: command · output (exit code) · SHA live · before/after · how to roll back · what is still on · spend checked · not verified`. Production, paid resources and destructive actions need the owner's explicit OK; account, plan and key creation are the owner's steps ("OWNER: ..."). Always list what you could not verify (provider panel not accessible, price read from a page that may have changed, restore not rehearsed).

## AI tells to avoid (check while answering, not after)

- Generic deploy and ops checklists not tied to this project's platform, config files and environments: read them first and cite file:line.
- Boilerplate and over-engineering: Kubernetes, extra environments, IaC layers or pipelines with no current need; use the smallest setup that works.
- Invented CLI flags, settings, regions, versions, prices or limits: check the installed CLI or the vendor page and date it, or say "not verified".
- "It depends" or a list of options with no recommendation, cost or number: pick one and give the reason.
- "Deployed", "fixed" or "restored" without a healthcheck, commit SHA or log line as evidence.
- Say what you chose and why in one line; a choice without a reason is removed.

## 7. Limits and honesty
Provider facts age: re-check before money or data decisions and every 3 months. Known gaps: whether a PaaS redeploy rebuilds or reuses the image; Railway's replacement for legacy config files (deprecated, works until 2026-12-01 `[22]`); RunPod serverless per-second rates and a low-balance alert; Upstash Redis eviction and persistence per plan; R2 versioning and object lock; Vercel plan limits beyond Functions; Supabase region change after creation; NIST text on RPO and RTO not read `[13]`.

## 8. Boundaries
CLI and API steps: `railway:use-railway`, `vercel:deployments-cicd`, `vercel:env-vars`, `supabase:supabase`. Observability design and SLOs: `engineering-playbook` (reliability-ops). Code security and RLS: `software-security`. Slow pages: `web-performance`. Release test gate: `qa-verification`. Personal-data transfers and region law: the privacy law of the data subject's country (official regulator pages). Not duplicated here.
