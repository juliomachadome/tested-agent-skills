# Metrics and testing for offers

## Definitions
| Metric | Formula | Note |
|---|---|---|
| Conversion (CVR) | orders ÷ unique visitors of the step | always per step and per source |
| Average order value (AOV) | gross revenue ÷ orders | includes bump and upsell of the same buyer |
| **Net revenue per visitor (RPV)** | (revenue − tax − fees − refunds) ÷ visitors | **decision metric** |
| Bump take rate | orders with bump ÷ orders | compare with a no-bump control |
| Upsell take rate | accepts ÷ those who **saw** it | split by payment method |
| Extra revenue per buyer | bump + upsell revenue ÷ buyers | post-purchase metric |
| Refund rate | refunded orders ÷ orders of the same cohort | by purchase cohort, count and value |
| Dispute rate | disputes ÷ card transactions | card-scheme programs penalise around 1%; payment processors warn earlier (one major processor treats ~0.75% as a warning). Check current rules. |
| Contribution margin | price − tax − fee − expected refund − variable cost | per order |
| Break-even ROAS | 1 ÷ contribution margin % | below it, ads lose money |

## Rules
- **[C] Decide on the whole funnel.** A bump that raises AOV and lowers conversion can lose; a low-take expensive upsell can win. Only RPV joins everything.
- **[C] Read refunds by cohort and cause.** A spike near the end of the guarantee window is expected; a spike on day one is a broken promise or broken access; refunds concentrated in one traffic source mean an ad that over-promises. No reliable public benchmark exists for info-product refunds: compare with your own history. [F] for any market number.
- **[C] Small volume does not support fine tests.** Compute sample size first; do not stop at the first good result; with little traffic test only large changes (price, offer, whole page) in alternating periods. Surprising results are usually measurement errors (Twyman's law). (Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments*, 2020)
- Rough sample guide: detecting +30% conversion with 80% power at 95% confidence needs roughly 450 purchases in total, whatever the base rate. With 500 visits per arm at 3% base, only about a doubling is visible.
- **One test per step at a time.** Register hypothesis, metric, start date and stop rule before starting.
- **Honest price tests:** alternating periods with the same price for everyone, or different markets. Simultaneous per-profile prices require disclosure in the EU.
- **Every price recommendation carries the arithmetic:** current vs proposed and the conversion needed to break even. Example: moving from 37 to 49, revenue is equal if conversion keeps 37/49 ≈ 76% of its current value; net of fixed fees the threshold is slightly lower.
- **No numeric targets published before a baseline exists.** Pre-launch, every market number needs a source; do not run Van Westendorp on invented data.

## Market, currency and payment method
- Price in local currency, final, tax included, in local format; converting another market's price by exchange rate ignores purchasing power and habit.
- Calibrate against local pockets: median net wage, prices of substitutes, typical online ticket of the dominant payment method, from official statistics with a date.
- **[C] Missing the preferred payment method kills purchases.** A large US survey lists ~9% abandoning for too few payment methods; local surveys in markets with a dominant local method usually show much more.
- Each payment method changes the funnel: stores credentials or not (one-click), has disputes or not, refund timing, minimum amount, activation requirements. Read the processor's page per method before designing.
- Seasonality: check with local data (search trends, school calendar, gift dates) before planning promotions.

## Weekly decision checklist
- [ ] RPV current and projected, with the break-even conversion.
- [ ] Refunds by cohort and by source; disputes below the warning threshold.
- [ ] Hypothesis, metric and stop rule registered before each test.

## Experiment rules from the literature (Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments*, 2020) [M]
1. **Fix one primary metric (OEC) and guardrails before the test** (refund rate, disputes, support load); a win on conversion with a worse refund rate is a loss.
2. **Check sample-ratio mismatch** first: if the split is not what you configured, discard the result and look for a bug.
3. **Twyman's law:** a surprisingly big win is more likely a bug than a discovery; replicate before shipping. No peeking at p-values to stop early.

## Related
Weekly routine and price-test design: `playbooks.md` 2 and 6. Symptom trees and worked arithmetic (break-even conversion, refund-adjusted RPV, CAC payback): `diagnosis-playbook.md`. Sample-size and stopping rules in general: the `growth-analytics` skill.
