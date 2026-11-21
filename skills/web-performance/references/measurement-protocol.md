# Measurement protocol, reporting and cost

## The protocol

1. **Baseline.** Measure the current behavior before touching anything, with the exact profile you will reuse.
2. **Locate.** Split the problem (LCP parts, INP phases, request stages, query plan nodes). Compute the share of the stage (Amdahl) to know the maximum possible gain.
3. **Budget.** Write the target as a percentile and a profile ("p95 under 400 ms for this query at 1M rows"; "route JS under N KiB gzip").
4. **Change one thing.** If you change two, you cannot attribute the result. If you must, measure each separately.
5. **Measure after,** same profile, same n, same cache state, same data volume.
6. **Guard.** Add a test or budget that fails on regression.
7. **Report** before and after. If you could not measure, write "expected, not measured".

## Reporting fields (always all six)

route or endpoint | tool and mode (field or lab) | device and network (or throttling profile) | cache cold or warm | n of runs and median (and p95 where relevant) | date and commit.

## Rules for trustworthy numbers

- Production build only; dev servers distort bundle size and timing.
- Run one measurement at a time on an idle machine; close headless browsers afterwards. Two concurrent runs on one machine corrupt each other.
- Throttle: CPU slowdown (about 4x for mid-range mobile) and a network profile from your audience.
- Separate cold from warm, and success from error.
- Enough samples: at least 30 for p95, at least 100 for p99; otherwise report the max and say so.
- Same data volume as production for database work.
- Compare equal conditions only; a measurement before on a quiet machine and after on a busy one proves nothing.
- Load tests: use a fixed arrival rate for routes (open model), ramp up, and watch the saturation signals alongside latency.
- Do not call a change a win inside the noise: with Lighthouse, differences of a few score points between single runs are noise.

## Budgets worth writing down

Express each as percentile plus profile, and make a test fail when it breaks: API route p95 on seed data; retrieval or query p95; end-to-end flow p95 and cost per flow; LCP, INP, CLS at p75; JS per route; background job throughput relative to real time; memory flat across repeated runs; polling interval and stop condition. Budget per stage so stage numbers sum to the flow budget (see backend-latency.md). A new budget number is recorded with who accepted it.

## Cost per active user

monthly cost per active user = bytes delivered x egress price + requests x price + image or media transformations + compute + database + cache commands.

- Heavy media (video, audio, PDF, large images) belongs on storage without egress fees or behind a CDN; do not stream media bytes through application functions, you pay transfer and CPU for what a bucket would serve directly.
- Services billing per transformation (image optimization) or per event (RUM, analytics) or per command (Redis): cap variants, use long TTLs, sample events.
- Same-for-everyone pages are static or incrementally regenerated; compute only where there is per-user data.
- Before adopting a service, compute the cost at 100, 1,000 and 10,000 monthly active users with typical usage. Prices change: check the pricing page on the day.
- An optimization that saves cents a month and costs days of work does not enter; write the trigger instead ("when egress passes X GB per month, move to Y").
- Example price points seen in the input at 2026-11-12, to verify before use: object storage about 0.015 USD per GB-month with free egress; image transformation about 0.05 to 0.08 USD per thousand; Redis over a free tier about 0.20 USD per 100k commands. These are illustrations, not quotes.

## What can be claimed about speed and conversion

- Direction is consensus: slower converts worse, more on mobile and cold paid traffic. The size of the effect in your funnel is known only by measuring your funnel.
- Best public causal evidence: a retailer-side A/B test (web.dev case study, Vodafone, 2021) where a 31 percent better LCP went with 8 percent more sales. One company, one landing page, paid traffic; do not generalize the number.
- Observational studies (for example the "Milliseconds Make Millions" report, 2020) show association, not cause. Old "abandon after 3 seconds" statistics come from old network conditions and are repeated without context; do not quote them.
- Never promise "X percent more conversion" from someone else's study. Say: "studies point to a gain; here we measure before and after on our metric".
- Compare slow vs fast users only with caution: device, income and intent differ. Without an A/B test or a controlled before/after it is correlation.
- Perceived performance counts: visible response to input within about 100 ms, skeletons shaped like the content, nothing jumping.
- Prioritize where money and cold traffic are: ad landing pages, checkout, the first screen after purchase.

## Sources

- https://web.dev/case-studies/vodafone (input file, read 2026-11-12; not re-fetched)
- https://web.dev/articles/vitals (fetched 2026-11-15)
- Price points: vendor pricing pages as cited in the input (not re-verified)
- https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md (not re-verified)
