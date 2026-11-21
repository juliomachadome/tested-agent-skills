# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a wrong denominator, a missing refund or a contaminated test makes every branch below meaningless. Thresholds are **[F]** (practitioner starting points) unless tagged; your own last 8-12 weeks replace them. Tags: **[C]** consensus or law, **[M]** serious but single or lab study, **[F]** practitioner or vendor, **[X]** myth, **[EU]** EU consumer-law constraint. Nothing is copied from a source; ideas are applied. Not legal or tax advice: **[LAWYER]** and **[ACCOUNTANT]** questions are flagged, not answered. Typical fields: order id, timestamp, buyer country, currency, gross, tax, fee, payment method, offer variant, bump/upsell flags, source/campaign, refund date and amount, dispute flag, subscription status.

## Step 0: is the data trustworthy?
| Check | How | If it fails |
|---|---|---|
| Orders are attributed to the offer variant that was shown | take 10 orders, replay the session or check the variant id on the order record; check the variant is stored at purchase time, not inferred from the current page | stop; fix tracking before reading any rate |
| Revenue is net and refunds are counted | does "revenue" include tax? fees? refunds, partial refunds, chargebacks and their fee? | recompute RPV net; label every number gross or net |
| Currency and VAT | one currency in the export? price shown with VAT in each country? reduced or zero VAT cases? fixed fees are in the fee currency | convert at the order-date rate, state it; split by country |
| Refund window | the last cohort has not finished its guarantee (30-day guarantee: orders newer than 30 days are incomplete) | exclude open cohorts or mark "provisional"; never compare a closed cohort with an open one |
| Test contamination | split ratio as configured (sample-ratio mismatch), overlap with a campaign, a coupon leak, a bot spike, a channel mix change, two tests on the same step | discard the arm or period; see `metrics-and-testing.md` |
| Denominator | CR = orders ÷ unique visitors of that step; take rate = accepts ÷ those who **saw** the offer; refund rate = refunds ÷ orders of the **same cohort** | recompute and label |
| Volume | under about 30 events in a cell, rates move on noise (a 2% conversion measured on 1,000 visits is 20 orders: 95% range about 1.3% to 3.1%) | write "not enough volume"; test only large changes |
| Change calendar | price changes, promos, ad creative or audience changes, checkout or payment-method changes, outages, tax changes in the window | line them up before any cause is named |

## Core arithmetic (all numbers illustrative; replace with your own)
Assumptions for the worked numbers: VAT 20% included in the shown price, payment fee 0.25 EUR + 2.9% of gross, no delivery cost. Contribution per order = price ÷ 1.20 − 0.25 − 0.029 × price.
- **Revenue per visitor** RPV = CR × AOV. 2.0% × 37 = 0.74 EUR per visitor. Net RPV uses contribution instead of price.
- **Refund-adjusted RPV** = RPV × (1 − refund rate) when refunds return the full price and the fee is lost. At 10% refunds: 0.74 → 0.666. If the processor keeps the fee on refunds, subtract it too. [C]
- **Break-even conversion for a price change**: new CR needed = old CR × old margin ÷ new margin (margin = contribution per order). Moving 37 → 49: contribution 29.51 → 39.16, ratio 0.7535. From 3.0% conversion, 2.26% is break-even (the naive ratio 37/49 = 0.755 is close; fixed fees make the true threshold slightly lower). With a per-order delivery cost the margin ratio moves; always compute it.
- **Bump contribution**: a 9 EUR bump adds 9 ÷ 1.2 − 0.029 × 9 = 7.24 EUR (no second fixed fee if it is in the same payment). Front 29 EUR contributes 23.08. If the bump lowers checkout conversion from 13.0% to 12.0%, break-even take rate t solves (12/13) × (1 + t × 7.24/23.08) = 1, so t = (13/12 − 1) × 23.08 ÷ 7.24 = 26.6%. A 35% take clears it (net +2.4% on front-plus-bump contribution, inside noise at 4,000 views per arm). The take rate alone never proves it.
- **Payback on CAC**: contribution per buyer in the payback window, after refunds, vs the cost to acquire a buyer. Front 23.08 + bump 0.35 × 7.24 + upsell (15% of the 75% who can see it) 0.1125 × 63.29 = 32.73 per buyer; at 8% refunds 30.11. Against CAC 32 EUR payback is 0.94: not paid back in the window; front alone is 0.66.
- **Contribution margin and ROAS floor**: break-even ROAS = price ÷ contribution; 29 ÷ 23.08 = 1.26 on the front alone (`paid-traffic` owns the buying rules).
- **Sample size**: detecting 3.0% → 3.6% (+20% relative) at 80% power, 95% confidence needs about 14,000 visitors per arm (about 420 orders per arm). With 3,000 per arm only a relative difference of about 45% or more is reliably visible. Use `growth-analytics` for the calculator and stopping rules.

## Tree A: revenue per visitor falling
| Check first | Likely cause | How to check | Fix |
|---|---|---|---|
| Traffic mix | a cheaper or colder source took share | RPV by source and by device, same week-over-week | judge by source; do not change the offer for a mix effect |
| Conversion or AOV, which moved? | RPV = CR × AOV: one factor fell | decompose the change (CR ratio × AOV ratio) | go to Tree B (AOV) or the conversion branch below |
| Refunds up | cohort not closed, or a broken promise | refund rate by cohort and cause | Tree F |
| Price or offer changed | a test, a bundle removal, a bump removed | change calendar (Step 0) | revert in an alternating period and compare |
| Tracking | variant id lost, a payment method not tracked | Step 0 replay | fix first |

## Tree B: conversion fine but AOV low
Cause list: no bump or a weak one; upsell not shown to a payment method; front price below the buyer's value; only one plan. Check: take rates among those who saw the offer, by payment method; AOV split by source. Fix: one test at a time: bump relevance (the add-on solves a problem the front creates), upsell with the same promise (`bump-upsell-downsell.md`), then a price test. Do not stack a second bump to lift AOV; it adds decisions. [F]

## Tree C: bump take rate low
| Likely cause | Check | Fix |
|---|---|---|
| Not recognisable as a useful add-on | read it as a stranger: what is it, price, why now | one line, exact price, tied to the item bought |
| Price too high for an impulse decision | take rate by price tested | cheaper bump or lower-effort item |
| Buyer is not yet convinced of the front | take rate low in cold traffic, high in warm | leave the bump off until the front is validated [1-SRC] |
| Weak item (would nobody pay alone?) | the "pay for it alone" test | drop it; do not pad |
| Placement or mobile layout hides it | session replay on mobile | move above the pay button, test |
Remember: a low take rate is not a problem if RPV of the arm with the bump beats the control. [C]

## Tree D: upsell take rate high but refunds or chargebacks up
| Likely cause | Check | Fix |
|---|---|---|
| Upsell disguised or confusing (looks like part of the order) | read the page as a buyer; does it show price, say "offer", have a pay button and a visible decline? [EU] | rewrite as an offer; the page is also a legal exposure |
| Too much pressure or a false timer | countdown, "last chance", confirmshaming | remove; real deadlines only |
| Promise differs from the front | refund reasons text for upsell buyers | align the promise, or drop the upsell |
| Buyers did not notice a second charge | disputes with reason "unrecognised", small descriptor | clear descriptor, receipt email listing each charge |
| Refunds concentrate on the upsell buyers | refund rate upsell buyers vs rest (e.g. 16.7% vs 6.1%) | judge the upsell on net contribution after refunds; if negative, remove |
Dispute rate near 1% of card transactions risks scheme programs; processors warn earlier (check the current figure). [C]

## Tree E: price test "won" but revenue down
| Likely cause | Check | Fix |
|---|---|---|
| Conversion won on a cheaper price but RPV fell | RPV net, not conversion | choose by net RPV; compute the break-even |
| Refund window still open for the winning arm | cohort ages | wait the full window before reading |
| Time confounded (alternating periods hit a campaign, payday, holiday) | calendar; reverse the order and repeat | repeat in swapped order; only large effects count |
| Sample-ratio mismatch or contamination | Step 0 | discard |
| Backend effect: cheaper front attracts buyers who skip the upsell or churn | RPV over 30-60 days incl. backend | measure the whole funnel |
| Peeking and early stop | was the stop rule written first? | decide by the rule; replicate a surprising win (Twyman's law) [M] |

## Tree F: refund rate rising
Split first: by day since purchase, by source, by payment method, by country, by stated reason.
- Spike on day 0-1: access broken, delivery email in spam, wrong product expectations. Fix delivery and the first screen after payment.
- Spike near the end of the window: value not felt or "refund shopping". Fix the first-week experience; consider a nudge to the first result, not a barrier to refund.
- One source or creative: the ad over-promises (`ad-creatives`, `paid-traffic`); fix the claim.
- After a price rise or a promo: buyers who bought cheaply to test, or who saw a better price a week later; apply the promo's rule for earlier buyers (`playbooks.md`).
- Refund requests made via chargeback: the refund path is hard to find; make it simple. An easy refund costs less than a dispute. [C]

## Tree G: guarantee abused
Define abuse from data, not impressions: repeat refunders per email/card/device, refunds after full consumption (course finished, files downloaded), refund within hours of delivery. Fix: write the anti-abuse rule before purchase ("one refund per person", clear scope), keep the guarantee simple, consider access revocation on refund, tighten scope rather than shortening the window (longer windows tend to reduce returns; wider scope raises them). [M] Do not remove the legal withdrawal right: your guarantee is on top of it. [EU]

## Tree H: checkout abandonment
Measure the funnel: checkout view → payment started → paid, by device, country, payment method. Likely causes: cost revealed late (drip pricing [EU]), missing local payment method, forced account creation, errors, price shown in the wrong currency, trust gaps at the pay step. Fix in that order; check the processor's decline codes before blaming the page. A survey of checkout abandonment reasons by a research institute is an order of magnitude only (`metrics-and-testing.md`). Page words belong to `copywriting`, flow to `ux-design`.

## Tree I: anchor or compare-at price challenged (EU)
Symptoms: a consumer-authority letter, a competitor complaint, a payment processor query, a user who saw a lower price last month.
1. List the price history per product per country: every price applied in the last 90 days with dates (from the order system, not memory).
2. Compute the **prior price** for each announcement: the lowest price applied in the 30 days before the reduction, including promo prices of earlier campaigns. The % and "you save" must be computed on it (Directive 98/6/EC art. 6a, inserted by Directive 2019/2161; Commission guidance 2021/C 526/02; CJEU C-330/23). [C][EU]
3. Classify the product: art. 6a applies to goods; digital content and services answer to the UCPD misleading-advantage rule, and member states may extend the 30-day rule: **check national law for the buyer's country**. Safe default: show the 30-day lowest price whenever you show a reduction. [LAWYER] for the country-level reading.
4. Fix: remove "was" prices nobody paid; replace with the dated cost of the customer's alternative, a unit price, or a future price with a final date; keep the proof file.

## Tree J: low-ticket front end not paying back CAC
Compute payback (Core arithmetic). Then: (1) conversion of the front by source; (2) bump and upsell contribution after refunds; (3) share of buyers who see the upsell by payment method; (4) 30-60 day backend (email, next product) measured, not assumed. Fix in order of cost: raise the front price test, fix the upsell path for non-card buyers, improve the refund cause, lower CAC (`paid-traffic`). If payback is measured to need more than the cash you can carry, the funnel is not ready to scale. A front that must break even alone has no backend assumption in its math. [F]

## Tree K: subscription churn after trial
Split churn by month 0, 1, 2+; trial type (card up front or not); acquisition source. Month-0/1 churn after a trial is usually a value-not-reached problem or a surprise-charge problem. Check: reminder before the first charge (many jurisdictions and card schemes require notice), clear price and renewal terms at signup, cancellation no harder than signup [EU]. Token-price trials with hard cancellation are an enforcement target. Fix: activation in the first session (`onboarding`), pricing tiers (`pricing`, `paywalls`), annual vs monthly mix, a pause option. Recurring-billing legal detail: [LAWYER].

## Discount addiction (sales only convert on promo)
Check: share of revenue in promo weeks; conversion at full price over the last 8 weeks; who buys on promo (new or lapsed full-price buyers). Likely causes: promo too frequent, price anchor eroded, no reason to buy at full price, launch price never actually ended. Fix: fewer, real, dated promotions; a full-price-only period; a bonus instead of a cut; a firm future price. Every cut resets the 30-day reference price. [EU] Test by holding the full price in alternating weeks; do not infer from one campaign. Buyers at full price yesterday: give them a defined answer.

## Output of a diagnosis
Symptom and metric with the Step 0 outcome; ranked causes with the check and its result; the fix per cause with the arithmetic; the test that would confirm it (control, metric, stop rule); what remains unverified.
