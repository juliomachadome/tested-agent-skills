---
name: web-performance
description: "Use when anything is slow or heavy, even a short question, for example \"this postgres query takes 3 seconds, how do I read EXPLAIN ANALYZE\", \"what Cache-Control for hashed JS bundles vs HTML\", \"should I add this charting library, worried about bundle size\", slow landing page or long list, Core Web Vitals (LCP, INP, CLS), JS budget per route, images, fonts, video, CDN and service worker caching, \"p99 spikes every few minutes, which stage is slow\" (tail latency, tracing), N+1, indexes, keyset pagination, cold start, cost per user. Always asks for a number before and after. Not for visual polish (ui-design), LLM token cost (llm-engineering), deploy mechanics (cloud-deploy-ops) or schema design (engineering-playbook)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Web performance

Performance work fails in one of two ways: people optimize something that was never the bottleneck, or they ship a change and claim a gain nobody measured. This skill is a method plus the facts that age slowly. Thresholds and platform details live in `references/` because they change.

## Project first

Before advice, read the current project's CLAUDE.md or AGENTS.md, ADRs, performance budgets, CI config (Lighthouse CI, bundle test), framework and version in `package.json`, and where RUM data lives. Project rules and budgets win over this skill. If the project already measures something, use that instead of building a second tool.

## Evidence tags

Tag claims: **[C]** consensus (vendor docs, textbook; see `references/BIBLIOGRAPHY.md`), **[W]** weak (practice, vendor blogs), **[M]** measured in this project (route, profile, n). Numbers without **[M]** are "expected, not measured". Thresholds quoted here are **[C]** at p75: LCP 2.5 s, INP 200 ms, CLS 0.1.

## Principles

1. **Measure, find the bottleneck, budget, change one thing, measure again.** Without a number before and after, the honest sentence is "expected, not measured". Say it that way.
2. **Field data sets priority, lab data debugs.** Real users decide what to fix first. Lighthouse and DevTools reproduce the problem, test the fix before deploy and simulate weak devices. If field is already good, a lab-only improvement is optional.
3. **Percentiles, never averages.** Vitals pass at p75. Backend budgets are p95/p99. An average of 400 ms can hide 1% of requests taking seconds.
4. **Split before you fix.** LCP into four parts, INP into three phases, a request into network, server and database. Fixing the wrong slice moves nothing.
5. **Cheap structural fixes first.** Send less (JS, bytes, rows), from closer (CDN), do less work (index, query shape); add caches last, since each can serve stale or someone else's data.
6. **A budget only works if it fails the build or a test.** A ceiling per route, measured on a production build, lowered at each cut and raised only with a written reason.
7. **Reference device and network come from the audience,** not the developer laptop.
8. **Cost is a performance dimension.** Bytes out, requests, transformations and CPU repeat every month a user is active.

## Which reference to open

| Situation | Open |
|---|---|
| "Slow" with no cause yet; field vs lab trust; symptom trees; worked numbers (p75, bytes to ms, cache hit) | `references/diagnosis-playbook.md` |
| Routines: measurement, budget and CI gate, image pipeline, fonts, code splitting and streaming, caching, third parties, query pass, report template | `references/playbooks.md` |
| LCP, INP or CLS thresholds, CrUX, RUM, Lighthouse variability | `references/core-web-vitals.md` |
| JS size per route, bundle analysis, images, fonts, audio/video, third parties | `references/assets-js-images-fonts.md` |
| Cache-Control, CDN, immutable hashes, signed URLs, service worker | `references/caching-cdn-sw.md` |
| Slow API or job: p95/p99 per stage, queues, tail latency, cold start, event loop | `references/backend-latency.md` |
| Slow query, N+1, index choice, vacuum, pooling | `references/postgres-performance.md` |
| Mobile or native clients: virtualization, startup, offline sync | `references/clients-mobile-offline.md` |
| How to run and report a measurement; sample size; cost per user | `references/measurement-protocol.md` |
| Front-end errors, RUM, release health, replay, trace IDs | `references/observability-frontend.md` |
| Sources and verification status | `references/BIBLIOGRAPHY.md` |

Open only what the task needs.

## Workflow

1. **Frame it.** "Slow for whom, where, doing what?" Convert to route + device + network + action. If the user cannot say, pick the highest-traffic route and say so.
2. **Look at field data first** (own RUM, CrUX if the site qualifies). No field data: state that everything below is lab.
3. **Reproduce on a production build** with throttling (CPU slowdown plus a network profile), one route at a time. Dev servers measure nothing useful.
4. **Divide the problem** with the splits in principle 4. For backends, get per-stage timings before touching code; for queries, run `EXPLAIN (ANALYZE, BUFFERS)`.
5. **One hypothesis, one change, one new measurement** with the same profile and the same number of runs.
6. **Lock the gain** with a failing budget: bundle test, weight ceiling, query with LIMIT, a p95 assertion in a load test.
7. **Report** with the template in `references/playbooks.md` (section 9) and the fields in `references/measurement-protocol.md`, always before and after.

## Quick rules that catch most problems

- The LCP resource is in the initial HTML, not lazy, with high fetch priority on one or two images at most.
- Every image and video has reserved dimensions; animate transform and opacity only.
- Ship less JS: server-rendered by default, client code only at the leaves that need state or events. Measure on every new dependency and every new client boundary.
- Fingerprinted files get a one-year immutable cache. HTML revalidates. Personal data never sits in a shared cache.
- Every list has a LIMIT, an index in the same order, and keyset pagination once it can grow.
- One query per item in a loop is a bug (N+1). Count queries per request in the log.
- No external I/O inside a database transaction; every outbound call has a timeout and a retry ceiling.
- Utilization above roughly 70-80 percent turns bursts into long queues; leave headroom.
- Parallel fan-out multiplies tail risk: a rare slow backend becomes the common case.

## Checklist before saying "done"

- [ ] Measured before and after on the same route, device profile, network profile and cache state, with n and median stated.
- [ ] Labelled field or lab; lab is not presented as user experience.
- [ ] The change was one thing (or each change measured separately).
- [ ] A budget or test now protects the gain.
- [ ] Any new cache has a TTL, a complete key and a fallback when it is down.
- [ ] Authenticated or per-user responses are `private` or `no-store`, and never in a service worker shared cache.
- [ ] New query: `EXPLAIN (ANALYZE, BUFFERS)` on realistic volume, LIMIT present, index justified by the plan.
- [ ] Unmeasured claims say "expected, not measured"; cost per active user estimated for 100, 1k, 10k.

## Measuring without ad-hoc tooling

One measurement at a time on an idle machine; close headless browsers afterwards. Prefer scripted, repeatable measurement (seeded perf test, Lighthouse CI per-route budget, build report) over hand-launched browsers. If the screen could not be measured, say so and deliver only what came from code and database.

## Output format for a performance review

```
Scope: <route or endpoint> | device/network profile | field or lab | cache state | n, median | date, commit
Severity: P1 breaks a budget on a main flow, P2 breaks one elsewhere, P3 risk without a measured breach
Finding: <one line, with the split that located it (LCP phase, INP phase, stage, plan node)>
Evidence: <before number> -> <after number> (or "expected, not measured")
Change: <one change>
Guard: <budget/test that keeps it>
Cost note: <effect on bytes, requests, CPU or spend, if any>
```

## Boundaries

- Algorithmic complexity, runtime behaviour, schema design and migrations: `engineering-playbook`.
- LLM latency, token cost, caching of model calls: use `llm-engineering`.
- Framework version details (cache APIs, image component options, config flags): check the installed version and the vendor skill or docs; this skill states only general patterns (server components cut client JS, streaming, static shell).

## AI tells to avoid (check while answering, not after)

- Generic speed tips (compress, lazy-load, cache) not tied to this route, bundle or query: read the code and cite file:line or the measurement.
- Boilerplate and over-engineering: new caches, CDNs, layers or libraries with no measured bottleneck; the smallest change that works.
- Invented thresholds, limits, versions or flags: check the installed version or vendor doc and date it, or say "not verified".
- "It depends" or a list of options with no recommendation, number or cost: pick one with the expected gain.
- "Faster" with no before and after number on the same profile: show it or say "expected, not measured".
- Say what you chose and why in one line; a choice without a reason is removed.

## Gaps

- Thresholds, budgets and platform numbers are dated 2026-11; re-check web.dev and vendor docs before quoting them.
- No real field data was used: replace the example device and network with the audience's.

