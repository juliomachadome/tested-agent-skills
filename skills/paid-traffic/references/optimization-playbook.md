# Optimization playbook: what to change, in which order

## 1. Order of levers (biggest first) [F]
1. **Offer and price** (what is sold, guarantee, bump): changes conversion most; belongs to the offers skill.
2. **Page and funnel** (first-screen match, speed, checkout, payment methods).
3. **Creative concept** (who/what/why; different concepts, not colour swaps).
4. **Audience controls** (mostly automated now: country, age floor, language, exclusions).
5. **Bid and budget mechanics** (highest volume first; cost cap or bid cap later).
Rule: do not touch level 4-5 to repair a level 1-2 problem. If cold traffic does not buy after several concepts and two entry points, go back up.

## 2. Break-even math (write it first)
- margin per order = AOV net of tax - fees - expected refunds - variable cost; **break-even CPA = margin per order**; break-even ROAS = gross AOV ÷ BE CPA.
- Example: price 27, bump 9 at 30% take, AOV 29.7 gross; 25% fees and VAT → net about 22.3; refunds 5% → margin ≈ 21.2 = BE CPA; BE ROAS ≈ 1.4; max cost per visit at 3% conversion = 0.64.
- Contribution margin test for scale: marginal CPA (Δspend ÷ Δpurchases) must stay below BE CPA to keep adding profit; average CPA below BE only says the total is profitable.
- Target CPA during validation = BE CPA; once stable, target = BE × (1 - desired margin).

## 3. Kill rules (written before spending)
| Rule | Value | Risk of killing a good item [MATH] |
|---|---|---|
| Ad with zero purchases | pause at 2.5 × target CPA spent | 8% (e^-2.5) |
| Same, if link CTR also under ad set median | pause at 1.5 × | 22% |
| Ad with 1-2 purchases at 3x CPA | pause | high-ish; log it |
| Ad set / campaign 7-day CPA | back one step if 3-day CPA > 1.3 × BE with 10+ purchases; back one phase if 7-day > 1.5 × BE | |
| Day with 3 × CPA spent and no sale | pause and check payment, page, pixel before blaming the ad | |
Never kill on CTR or hook rate alone: attention metrics triage, purchases decide.

## 4. Test design
- **One question per test**, one variable, others frozen; decide metric and stop rule first.
- **Creative:** reading cost per ad ≈ 2.5 × target CPA. Number of ads you can read in a period = period budget ÷ (2.5 × CPA). Weekly batch of 3-5 ads, at least one new concept.
- **Minimums:** candidate at 3-5 purchases within target; winner at 10+ within target or repeated in a second week. A/B on conversion: to detect +30% needs about 450 purchases in total at 80% power and 95% confidence [MATH, Kohavi]; with fewer, test only big changes (2x).
- **Platform tools:** Meta's creative test tool (2-5 ads, similar spend, 7 days default; size so the best ad nears 50 events) and A/B tests that separate audiences [C per platforms.md]. Google: experiments with 4-6 weeks [C per Google's guidance]. TikTok: Split test.
- **Lift tests** for channel-level truth: see `reading-data.md`.

## 5. Scale rules
| Phase | Daily budget | Gate to next |
|---|---|---|
| Validate | 2-4 × BE CPA | 20+ purchases and 7-day CPA ≤ 1.5 × BE |
| Stabilise | 4-8 × | 2 weeks CPA ≤ BE and 2+ winning creatives |
| Scale | steps | 7-day CPA ≤ target with 50+ purchases/week |
| Diversify | 15 × or more | main channel stable |
- **Budget step:** +20-30% every 3-4 days is a conservative habit [F], not a platform law; doubling only when CPA is 30%+ under target and the ad set has 50 purchases/week. Google guidance for Smart Bidding: avoid multiple target changes inside one conversion cycle; judge over 2 conversion cycles or 2 weeks [C].
- **Raise vs duplicate:** raise the budget of the winning ad set first; duplicate only for a structural reason (new country, new offer) or when a new concept must be read at equal spend. Duplicating a winner to scale makes copies compete [F].
- **Cost cap / bid cap:** use only with history. Set cost cap near target CPA × 1.1 once 7-day CPA is stable; if delivery collapses, the cap is below the market: raise 20-30% or return to highest volume. Bid caps need account history; do not mix with Meta's creative testing tool [C per platforms.md].
- **Horizontal scale, in order:** new concepts, another entry point, another platform (only when its math closes), another country, another product.
- **Step-down:** written rules in section 3.

## 6. Creative refresh cadence
Weekly batch (3-5 ads), monthly retire list (ads over 4 weeks old with falling CTR and rising cost per visit), concept review every 4-6 weeks. Small universes need more refresh. Keep the control (best winner) running until the challenger reads at 2.5 × CPA. Hand concepts to the ad-creatives skill.

## 7. Account consolidation
- One campaign per objective; fewest ad sets (weekly budget ÷ (50 × CPA)); merge ad sets with under ~30 conversions in 30 days (Google guidance: merge groups under ~30 conversions in 30 days [C]); pool conversion data; one primary conversion event (purchase).
- Remove duplicate remarketing until daily budget > ~15 × CPA.
- Keep naming = UTM convention; one link per ad.

## 8. Weekly review ritual (30 minutes, same day/time)
1. Step 0 checks (tracking, consent share, orders without source).
2. Backend table: spend, purchases, net revenue, CPA, net RPV by entry point and concept; platform ÷ backend ratio.
3. Funnel factor read: CPM, CTR, visits ÷ clicks, page conversion, checkout, refunds.
4. Apply kill/candidate/winner rules; list the decisions with the rule that triggered each.
5. Marginal CPA of the last budget step; decide hold/step/step-down.
6. Next batch (concept, owner, date) and the single experiment for the week.

**Report template**
```
Week of DD/MM  | Spend | Backend purchases | CPA | BE CPA | Net revenue | MER | Platform/backend ratio
Verdict (2 lines):
What moved (factor: CPM, CTR, visit rate, page conversion): 
Decisions: kill / keep / scale with rule + numbers
Not enough volume to conclude: 
Tracking gaps and consent share:
Next week: batch, test, budget step
Could not verify:
```
