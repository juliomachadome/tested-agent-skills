# Diagnosis playbook: symptom, likely cause, check, fix

Use it top-down. Step 0 first: a broken tag, a consent change or a wrong denominator makes every branch below meaningless. Thresholds are **[F]** (practitioner starting points) unless tagged; the team's own last 8-12 weeks replace them. Evidence tags: **[C]** consensus or law, **[M]** serious but single or correlational, **[F]** practitioner or vendor, **[X]** myth. Nothing is copied from a source; ideas are applied. Typical inputs: event export with user id, timestamp (UTC), event name, properties, consent state, source/medium; the database of orders and signups as the second opinion; a release and campaign calendar.

## Step 0: is the data trustworthy?
| Failure | How to see it | Check | Fix |
|---|---|---|---|
| Tracking broke (tag removed, event renamed, SDK update) | one event or one platform falls to near zero overnight while the database does not | event volume per day per platform and app version; compare with database counts (signups, orders) | restore the event; mark the gap on the chart; never compare across the gap without a note; add a volume alert (`playbooks.md` 2) |
| Consent drop | sessions or users fall but orders in the database do not; the share of "unknown" source rises | consent acceptance rate per day; banner changes in the release log; consented vs not consented segments | report both bases; use database counts for money; do not bypass consent (`playbooks.md` 7) |
| Bot or internal traffic | spikes with 100% bounce, one data-centre ASN or one user agent; zero-second sessions | filter by known bot lists, internal IPs, user agent; look at sessions per user per day | exclude and document the filter; re-run the period |
| Timezone or calendar mismatch | daily totals differ by the same few percent between tools; "today" looks low | compare 3 orders by hand in both tools; check the tool's reporting timezone | one UTC rule for storage, one reporting zone, written next to every chart |
| Double counting | conversions higher than orders; page reload, retry or both client and server firing the same event | distinct order id vs event count; same event from two sources | dedupe on a stable id (order id, event id); one source of truth per event |
| UTM loss or overwrite | "direct" grows; paid sessions fall; redirects, payment return pages, app handoffs, link shorteners strip parameters | landing-page URLs with and without UTM; referral exclusions for payment domains; first-touch vs last-touch rows | persist first-touch at landing; add payment providers to referral exclusions; tag every campaign link by convention |
| Ad blockers and browser limits | client events lag the database by a stable percentage that differs by browser | compare by browser and device; client-side purchase vs server-side purchase | critical events server-side with the same consent rules; accept a stable gap for UI events |
| Sampling or thresholding | a report says "sampled" or hides small rows; totals differ from the unsampled export | check the sampling flag; export raw (warehouse) data | answer from the warehouse; shrink the date range or dimensions |
| Definition drift | same name, new meaning (active user, session, conversion) | glossary vs query; git history of the query | version definitions; restate history or break the series |

Rule: when the export and the database disagree by more than about 5%, stop and explain the gap before explaining the metric **[F]**.

## Core arithmetic

### Sample size per arm for a conversion rate
Two-sided alpha 0.05 (z = 1.96), power 80% (z = 0.84). With baseline p1, target p2, absolute lift delta = p2 - p1 and p-bar the mean of p1 and p2:

n = ( 1.96 * sqrt(2 * p-bar * (1 - p-bar)) + 0.84 * sqrt(p1(1-p1) + p2(1-p2)) )^2 / delta^2

Shortcut: n is about 15.7 * p(1-p) / delta^2, using the baseline for p; it slightly underestimates (it ignores that the variance at p2 differs).
- Example: baseline 4%, hoped 5% (delta 0.01). Full formula: 6,745 per arm. Shortcut: 15.7 * 0.0384 / 0.0001 = 6,029. Plan with the full formula: 13,490 users total.
- Small lifts cost a lot: 4% to 4.4% (10% relative) needs about 39,500 per arm; 4% to 4.5% about 25,550.
- Traffic check: at about 5,000 eligible users a day split 50/50, 4% to 4.5% takes about 10.4 days of traffic; round up to whole weeks, so 2 weeks. If the plan needs more than 6-8 weeks, test a bigger change or decide with other evidence **[F]**.

### Sample ratio mismatch (chi-square, 1 degree of freedom)
chi2 = sum over arms of (observed - expected)^2 / expected, expected from the design split.
- Example: design 50/50, 20,000 users; observed 10,300 vs 9,700, expected 10,000 each. chi2 = 300^2/10,000 + 300^2/10,000 = 18.0, p about 0.00002. Flag (threshold p < 0.001 **[C]**): the data is broken, do not read the conversion result.
- Borderline: 5,150 vs 4,850 of 10,000 gives chi2 = 9.0, p = 0.0027: above a 0.001 alarm, but a 3% split gap is not noise; look anyway.
- Fine: 5,060 vs 4,940 gives chi2 = 1.44, p = 0.23.

### Payback and LTV with churn
- Simple payback (months) = CAC / (ARPA per month x gross margin). Example: CAC 600, ARPA 50, margin 80%: contribution 40 per month, payback 15 months.
- With churn c, the contribution received by month t is 40 x (1 - (1-c)^t) / c. At 3% monthly churn it reaches 600 only in month 20 (not 15), and the lifetime ceiling is 40 / 0.03 = 1,333, so LTV:CAC = 2.2, not 3.
- Monthly churn from a retention number: c = 1 - R12^(1/12). A 61% twelve-month retention is about 4.0% a month.
- LTV on revenue instead of margin, or on the best cohort, is the most common inflated slide **[F]**.

### Cohort retention, read in four steps
Cohort = users who signed up in the same week; column = weeks since signup; cell = share of the cohort that did the core action that week.
| signup week | W0 | W1 | W2 | W3 | W4 |
|---|---|---|---|---|---|
| Jan wk1 | 100% | 42% | 31% | 27% | 26% |
| Mar wk1 | 100% | 38% | 25% | 20% | 17% |
Read: (1) shape: Jan flattens near 26% (a retained base), (2) compare the same column across rows: W4 26% vs 17%, a drop of 9 points, (3) check cohort size and mix (channel, plan, country) before blaming the product, (4) check whether the return event or the tracking changed between rows. The latest diagonal cells are incomplete weeks; never read them.

### Confidence interval of a proportion
p = x/n, standard error = sqrt(p(1-p)/n), 95% interval = p +/- 1.96 x SE (Wald; use Wilson when n is small or p near 0 or 1).
- 48 signups out of 1,200 visitors = 4.0%; SE = 0.57 points; Wald 2.9% to 5.1% (Wilson 3.0% to 5.3%).
- 5 of 100 = 5%: Wilson 2.2% to 11.2%. At n = 100 a 5% rate says almost nothing.
- Difference of two rates: the interval of the difference must be reported, not two separate intervals.

## Tree 1: conversion rate dropped
1. Step 0 table. Is the drop in the database too (orders, signups)? If only in analytics, it is measurement (consent, tag, bot filter); stay in Step 0 and Tree 11.
2. Which part moved: numerator (conversions) or denominator (traffic)? Traffic mix change (new paid channel, a viral post, a bot wave) lowers blended conversion with no product change. Split by source, device, country, new vs returning.
3. Timeline: line up releases, price changes, campaigns, outages, banner changes, holidays. A drop starting the same hour as a release points to the release; a slow slide points to mix or a competitor.
4. Segment test: if every segment fell, think site-wide (speed, outage, payment provider); if one fell, think that segment's change (browser bug, one landing page, one country's payment method).
5. Fix by cause: revert or hotfix; restore tracking; shift budget away from the low-intent traffic; do not "optimise the page" before the cause is known.

## Tree 2: signups up but activation down
- Likely causes: a new acquisition channel or promotion brought low-intent users (mix); signup friction was cut so more tentative users enter; onboarding broke for one platform; the activation event changed or broke; fake or bot signups.
- Check: activation rate (same window, for example 7 days from signup) by channel, device, cohort week. Number of activated users in absolute terms: if it rose, the rate fell because of dilution, which may be acceptable. Compare against bot-like signups (disposable emails, no events).
- Fix: if mix, judge channels by activated users per cost, not by signups; if friction, add a qualifying step or a better first-run path; if broken, fix; revisit the activation definition with data (`playbooks.md` 1). Link: onboarding work in `skills/product-management`.

## Tree 3: retention curve worse in newer cohorts
- Likely causes: mix (channel, plan, geography, age of audience); product regressions; seasonality of the signup week; promotion cohorts that join for a deal; tracking change on the return event; right-censoring (the newer cohort simply has fewer weeks).
- Check: same column across rows only; segment each cohort by source and plan; compare cohorts at equal age; confirm the return event fires in the same way in both periods; look at cohort size.
- Fix: if mix, report retention per channel and cut the weak one; if regression, trace to the release and the feature used by retained users; if seasonality, compare with the same weeks last year. Do not mix "unbounded" (returned any time after) and "bracket" (returned in that week) retention in one table.

## Tree 4: A/B "winner" did not hold after launch
Possible causes, in the order to check:
1. **Peeking or early stop**: stopped when p dipped below 0.05. Repeated looks raise false positives well above 5% (one well-known demonstration shows about 26% with continuous peeking at a nominal 5%, from Evan Miller's essay **[M]**).
2. **Winner's curse**: choosing the best of many variants or metrics overstates the effect; the observed lift of a selected winner is biased upward **[C]**. Shrink the estimate, replicate, or hold out.
3. **Novelty or primacy effect**: users click new things at first; the lift decays after weeks. Look at the lift by days since first exposure.
4. **SRM** or other broken randomisation (Tree 5).
5. **Different population at launch**: the test ran on a segment, a week or a country that differs from the full rollout; interaction with another test.
6. **Metric choice**: the primary metric was a proxy (clicks) and the business metric did not move.
7. **Underpowered test**: a lucky 2% lift on 1,800 users per arm is within noise (CI of the difference spanned negative to positive).
Fix: keep a holdout after launch (for example 5% for 4 weeks) to measure the real effect; pre-register the stopping rule (`playbooks.md` 3); record the result as "not confirmed".

## Tree 5: SRM detected
1. Compute chi2 against the designed split (see arithmetic). If p < 0.001, stop reading metrics.
2. Look for where users are lost, by stage: assignment (hash or bucketing bug), redirect or client-side flicker (treatment slower, users leave before exposure is logged), bot filtering that hits one arm, logging loss on one variant (heavier page, consent dependent), exposure logged only after an interaction, caching or CDN serving one variant, a data pipeline join that drops rows, returning users bucketed differently, a ramp-up that changed the split mid-test. The taxonomy in the KDD 2019 paper groups these by stage **[M]**.
3. Slice the mismatch by browser, country, new vs returning, day: the slice where the ratio breaks is the clue.
4. Fix the cause, discard the contaminated data, restart the test. Adjusting weights to "fix" the ratio hides a bias and is not a repair.

## Tree 6: attribution disagrees between platforms and analytics
- Expected: each ad platform claims conversions it touched (view-through and click windows differ, modelled conversions added), so the sum of platform claims exceeds the real total **[C]**. Analytics last-click credits the final touch and loses sessions without consent.
- Check: define the window and model of each number; compare each source with orders in the database for the same period; compute the overlap ratio = sum of platform conversions / database orders (a ratio of 1.4 means 40% overlapping or modelled claims); check UTM coverage (Step 0).
- Fix: treat the database as the total; use platform numbers for within-platform optimisation; for the question "what did the spend cause", use a holdout or geo test or a media-mix model (`playbooks.md` 6); report attribution as a range. Spending decisions belong to `skills/paid-traffic`.

## Tree 7: CAC rising
CAC = total acquisition spend / new customers in the same period (define the lag: customers closing this month came from spend of earlier months). Example: spend 40,000 and 100 customers gives 400; spend 52,000 and 104 customers gives 500 (+25%) while spend rose 30%.
- Causes: audience saturation on a channel, auction competition, creative fatigue, a conversion drop on the site or in the offer, a mix shift to costlier channels, a tracking loss (fewer attributed customers, not real), seasonality, a changed definition of "new customer".
- Check: CAC by channel and cohort; marginal CAC (the extra spend divided by the extra customers) vs average; funnel step conversion for the same period (Tree 1); database count of new customers vs attributed.
- Fix: cut the channel where marginal CAC exceeds payback limits; refresh creative; fix the conversion leak first; judge by payback, not by CAC alone (Tree 8). Media actions: `skills/paid-traffic`.

## Tree 8: LTV:CAC looks great but cash is short
- Likely causes: LTV built on revenue not margin; LTV from the best cohort or from a churn rate that excludes early churn; CAC excludes sales, onboarding or tools; long payback (the ratio hides time); growth spends cash on today's cohorts before earlier ones pay back; discounted annual prepay boosts the ratio but not recurring cash.
- Check: recompute LTV = ARPA x gross margin / monthly churn with the blended churn; loaded CAC; payback in months, simple and churn-adjusted (arithmetic above); cumulative cash by month for a steady acquisition pace (spend minus contribution of all cohorts).
- Worked slide: media CAC 1,500, ARPA 150, margin 70% (contribution 105), 12-month retention 61% (4.0% monthly churn). Slide LTV 150/0.015 = 10,000 gives 6.7:1; recomputed LTV is 105/0.0404 = 2,602, 1.7:1 on media-only CAC and 1.3:1 on loaded CAC 1,950; simple payback 14.3 months, churn-adjusted 21 months (34 loaded).
- Fix: show payback and cumulative cash next to the ratio; slow acquisition to what cash covers; shorten payback (annual prepay, onboarding that cuts early churn, price); see `skills/pricing`.

## Tree 9: North Star up but revenue flat
- Likely causes: the metric measures activity not value (clicks, messages) or is gameable; growth is in free or low-value segments; the metric rises but monetisation does not follow (pricing, packaging, paywall); revenue lags (annual plans recognised later); one big customer or promotion; definition changed.
- Check: split the North Star by plan and segment; correlate with revenue per cohort with a lag; test whether users with higher values of the North Star convert or renew more (correlational **[M]**).
- Fix: redefine so the metric includes the value that is paid for; add the revenue input and guardrails to the tree (`playbooks.md` 1); do not drop the North Star because one quarter disagrees, but test the link.

## Tree 10: funnel step with a sudden drop after a release
1. Check tracking first: did the event or its property change in the release? Compare the database (completed action) with the event count.
2. Segment the drop by platform, browser version, app version, locale: a single browser or a single app version is a bug.
3. Look at errors and logs for the same hour (client errors, failed requests, payment provider declines); time-to-step and abandonment before and after.
4. If tracking and errors are clean, treat it as a product change: session replays or tests with real users; an A/B holdback if a flag exists.
5. Fix: roll back or flag off first, analyse second. A funnel shows where, not why.

## Tree 11: dashboards disagree
- Causes: different definitions (unique vs total, UTC vs local, session vs user); different filters (bot, internal traffic); different data freshness; sampling; one source is client-side and the other server-side; currency or tax treatment in revenue.
- Check: pick one number and trace it: raw rows, filters, aggregation, timezone, join keys. Write both definitions side by side.
- Fix: one metric layer with named definitions and owners; each dashboard states the definition and the freshness; retire the duplicate.

## Tree 12: seasonality mistaken for an effect
- Signs: the "effect" starts at a holiday, a payday, a month end, a school term or a sale; it appears in untreated segments too.
- Check: compare with the same weeks last year; use a control group or a comparison series not exposed to the change; look at day-of-week; difference-in-differences on a matched control (before/after change in treated minus before/after change in control) **[M]**.
- Fix: run tests in whole weeks, both arms at the same time (an A/B test cancels seasonality; a before/after does not); state the seasonal baseline in the readout.

## Output of a diagnosis
Data used and its trust level (Step 0 result), the numbers with intervals, the most likely and second cause with the check that separates them, the next action with owner, what could not be verified.
