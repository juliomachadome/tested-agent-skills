# Testing, kill rules, scaling and fatigue (money side)

Concepts, hooks, formats and attention metrics live in the ad-creatives skill.

## Creative testing
- **[F] Most creatives do not win; that is statistics, not incompetence.** In one vendor's reported ~579k creatives across ~6k accounts (Sep 2025 - Jan 2026), about 5% became "winners" by that study's definition (10× the account's median spend and at least 500 USD), taking ~55% of total spend (23% in small accounts, 64% in huge ones). It measures spend, not profit, and comes from a creative-analytics vendor. Plan volume over weeks, not one giant batch. [1-SRC]
- **[MATH] How many creatives at once:** period budget ÷ (2.5 × target CPA). With 14 days at 150/day and target CPA 50: 2,100 ÷ 125 ≈ 16 "readings", covering ~6 creatives across two entry points or 8-10 in one, already allowing for uneven allocation.
- **[MATH] Kill rule and its risk.** If a creative truly has the target CPA, the chance it shows zero purchases after spending k × CPA is e^(−k):

| Spend with zero purchases | Chance of killing a good creative |
|---|---|
| 1.0 × target CPA | 37% |
| 1.5 × | 22% |
| 2.0 × | 14% |
| 2.5 × | 8% |
| 3.0 × | 5% |

Practitioner rules ("1.5 tickets without a sale", "0-1 purchases at 3× CPA, cut") all fall in this range [F]. Recommended default: pause at **2.5 × target CPA with zero purchases**; pause already at 1.5 × if, besides zero purchases, link CTR is below the ad set's median.

- **[MATH] Few purchases do not make a winner.** 95% interval for the true CPA given observed purchases:

| Purchases | True CPA lies between |
|---|---|
| 5 | 43% and 310% of observed |
| 10 | 54% and 209% |
| 20 | 65% and 164% |
| 50 | 76% and 135% |
| 100 | 82% and 123% |

"Candidate" at 3-5 purchases within target; "winner" at 10+ within target, or repeating in another week. A 20% CPA gap between two ads with 8 purchases each does not exist.

- **An ad that got no spend was not tested.** Meta concentrates spend early. For an ad with under 5% of spend after 4 days: accept the system's choice, or give it a fair reading in the next batch (testing tool or its own fixed-budget ad set). Complaining about allocation and switching off what got spend is the worst option.
- **Weekly batch:** out goes whatever hit the cut, in come 3-4 new ads, at least one a new concept and the rest format variations of a candidate.
- **Attention metrics triage; purchases decide.** Hook rate, retention and CTR show where a piece breaks; no research links them to financial results, and a prominent critic argues much "testing" is delivery noise. [F]
- **[F] Practitioner starting batches** (5 bodies × 5 hooks; 6 creatives × 3 hooks) assume budgets of ~10 tickets/day per campaign. With less, shrink by the formula above. Hook-only variations count as the same concept for delivery. [1-SRC]

## Audience and page tests
- With automated delivery, an "audience test" is a concept test plus breakdown reading: the creative that speaks to 50-year-olds finds them. Read age/gender/platform breakdowns for hypotheses, remembering they show averages, not marginal cost.
- Split audiences into ad sets only for structural differences: another country, language, offer, or an age band needing a different page.
- **[C] Split page tests in the ad, not on the site, when the site can only randomise consented visitors.** Two copies of the same ad set (same creatives, audience, budget), one destination each; preferably via the platform's A/B tool, which separates audiences. Organic traffic stays out.
- **[MATH] Sample:** detecting +30% conversion at 80% power and 95% confidence needs ~450 purchases in total, whatever the base rate. With 500 visits per arm at 3%, only ~2× differences show; with 2,000 per arm, 50%+. With little traffic, test only big changes and write the stop rule first. (Kohavi, Tang & Xu 2020)
- One test per step at a time; page frozen during a page test; new creative batches enter both arms the same day.
- Decide by net RPV per arm, refunds deducted. Statistical significance is required when being wrong is expensive; for "which page do we keep", a pre-written rule like "the higher one at deadline" is acceptable.

## Scaling phases (gates in purchases and CPA, not days)

| Phase | Question | Daily budget | Passes when |
|---|---|---|---|
| Validate | does the funnel sell to cold traffic? which entry and concept? | 2-4 × break-even CPA | 20+ purchases and 7-day CPA ≤ 1.5 × break-even |
| Stabilise | can it break even consistently? | 4-8 × | 2 weeks with CPA ≤ break-even and 2+ winning creatives |
| Scale | how much fits before marginal cost passes break-even? | steps | 7-day CPA ≤ target with 50+ purchases/week |
| Diversify | where is the next audience? | 15 × or more | main channel stable; winners in the new channel's format |

- **Vertical scaling:** steps of 20-30% every 3-4 days while 7-day CPA stays on target [F]. One bigger jump (doubling) is acceptable when CPA is 30%+ under target and the ad set does 50 purchases/week. Large operators double daily [F]; in a small account that risks a week's profit in one bad day.
- **[M] Cost rises with budget:** the first people reached are the cheapest. Scale on marginal CPA.
- **Horizontal scaling, in order:** new creative concepts; another entry point; another platform; same language in another country; another product for the same base.
- **[F] Do not duplicate campaigns to scale:** identical campaigns compete in the same auction and split learning.
- **Step-down rule, written in advance:** 3-day CPA above 1.3 × break-even with ≥10 purchases → back one step; 7-day CPA above 1.5 × → back one phase and a new creative batch; a day with no sale at 3 × CPA spent → pause and check payment, page and pixel before blaming the ad.
- **[F] Seasonality:** auctions get pricier in Q4 with a Black Friday peak and usually cheaper in January. Confirm with your own CPM. "Fresh start" products (languages, health, finance) combine cheaper auctions and high intent in January.
- **[F] Hourly budget changes** are a big-operation technique; on small budgets, at most one change a day at a fixed time.
- **Second platform only when its math closes:** TikTok at 25 results in 7 days; Google video at 20 × CPA per day.

## Fatigue and saturation
- Composite signal: frequency rising, link CTR falling, cost per visit rising, with page conversion stable. If page conversion falls too, it is something else (season, page, offer).
- **[X] Magic frequency thresholds** ("above 2.5, replace everything") come from vendor blogs. Watch your own 4-week trend and the platform's labels.
- Small audiences saturate first (small country, single language, high minimum age): estimate the universe in planning and treat the weekly creative batch as a fixed cost.
- Account-level saturation: CPM rising with flat reach and marginal CPA above break-even even with new creatives → scale horizontally, not with more budget.

## Rules from *Trustworthy Online Controlled Experiments* (Kohavi, Tang and Xu, 2020) [M]
1. Define the primary metric and guardrails (refund rate, page conversion) before the test starts, and the stop date by sample size, not by looking.
2. Verify the split is as configured (sample-ratio check) on landing-page or audience tests you control; platform lift studies have their own checks.
3. A very large effect is suspicious (Twyman's law): re-run or hold out before scaling spend.
