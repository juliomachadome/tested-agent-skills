---
name: business-model-finance
description: Use for the money side of a small digital business, product, course, app or SaaS run by a solo founder or small team, even for a quick question - "does this business make money", "how many sales to break even", "unit economics", "contribution margin after fees and refunds", "build a P&L", "cash flow forecast", "how much does Hotmart/Kiwify/Eduzz/Gumroad/Stripe/Paddle/App Store take", "MEI or Simples Nacional", "LTV CAC payback", "runway", "MRR and churn", "base/low/high scenarios", "launch budget", "should I reinvest or take profit", "selling but no money left", "ads profitable but not in the bank", EU VAT OSS basics, Business Model Canvas or Lean Canvas as thinking tools. Brings the arithmetic, dated fee tables and diagnosis trees. Not for price or offer design (offers), growth dashboards and experiments (growth-analytics), market sizing (market-research) or legal/tax advice for a specific case (accountant).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Business model and finance

The goal is one honest answer: after every fee, refund, tax and ad cost, does each sale leave money, how many sales cover the fixed costs, and how long does the cash last if things go worse than planned. Evidence tags: **[C]** accounting identity or consensus, **[M]** serious but single or practitioner, **[F]** rule of thumb or vendor claim, **[X]** myth. Fees and tax rules change: every number in the references is dated; re-check the official page before a decision. Tax content is general information, never advice for a specific case.

## 1. Start: project first, then five numbers
Read the current project's docs first (price, platform, costs, tax regime, ledger exports); project rules override this skill. Then get, or state as assumptions: price and units per month; platform and payment fee schedule; refund and chargeback rate; ad spend and other variable costs; fixed costs and cash on hand. Separate **cash** (money moved) from **result** (accrual). If any input is a guess, mark it and run the low case.

## 2. Business model as a thinking tool
- **Business Model Canvas** (nine blocks) and **Lean Canvas** (problem, solution, metrics, unfair advantage replace partners, activities, resources, relationships) are hypothesis maps, not deliverables **[M]**. Use them to find the riskiest assumption, then put a number on it (price, conversion, CAC, churn).
- Fill customer segment, value proposition, channel and revenue stream first; costs last. Two canvases of the same idea (before and after a test) show what the data changed.
- Output: top 3 assumptions, the metric that kills or confirms each, the cheapest test. Market evidence goes to market-research; price levels to offers.

## 3. Unit economics: contribution per sale
Contribution per sale = price - platform fee - payment fee - expected refunds - chargeback cost - taxes on revenue - variable delivery cost (support, hosting, AI/API) - ad cost per sale **[C]**.
1. Fee is usually percent plus fixed amount: fee = p x price + f. Low prices make the fixed part heavy (R$97 at 8.99% + R$2.49 is 11.6%).
2. Refunds: platform fees are often not returned on a refund; check the platform's terms **[M]**. Count refunded sales as revenue that never arrives but costs fees and ads.
3. Taxes: model the regime you are in (MEI fixed monthly payment, Simples percentage of revenue, VAT abroad).
4. Show contribution before ads (can the product pay for any traffic?) and after ads (does the channel pay?).
5. Worked sheet: `references/playbooks.md` (1).

## 4. P&L, cash flow, break-even, runway
- **Break-even units** = fixed costs / contribution per unit; revenue = units x price. If ads scale with sales, use contribution after ads; if ads are a fixed budget, treat them as fixed.
- **Monthly P&L and cash flow, 12 to 18 months**: one row per month with units, revenue, fees, refunds, taxes, ads, fixed costs, result, cash. Cash lags: card payouts take days, boletos and Pix less, and taxes and annual tools are paid on dates **[C]**. Template and numbers: `playbooks.md` (2).
- **Runway** = cash / net monthly burn; with growth or churn, simulate month by month rather than divide. Below 6 months of runway, decide before cutting ads blindly: cut the lowest-contribution channel or cost first.
- **Scenarios**: base, low (sales -33%, refunds up), high; then **sensitivity** one lever at a time (price, conversion, CAC, refund rate) to see which one moves the result most. `playbooks.md` (4).
- Price levels and tests: hand off to offers or pricing; this skill only reports how the margin changes.

## 5. CAC, payback, LTV
- **CAC** = acquisition spend / new paying customers in the same period; report media-only and loaded.
- **Payback** (months) = CAC / monthly contribution per customer; for subscriptions use the churn-adjusted version. **LTV** (constant churn) = ARPA x gross margin / churn **[M]**: a model, capped at 3 to 5 years. For one-time products LTV = contribution per customer including upsells, minus refunds.
- Cohort-matched CAC, channel cuts and the LTV caveats are in growth-analytics (`unit-economics-lifecycle.md`); do not duplicate them here. Benchmarks such as LTV:CAC of 3 are rules of thumb **[F]**; cash payback matters more for a small team.

## 6. Subscription metrics
MRR (new, expansion, contraction, churned), logo churn vs revenue churn, net revenue retention, cohort revenue curves **[C]**. Monthly churn of 5% loses 46% of a cohort in a year; a growing MRR can hide a leaking base: read new vs churned MRR separately (`diagnosis-playbook.md` tree 5). Annual plans bring cash early but defer revenue and refund exposure.

## 7. Reinvest or take profit
Order of use of cash **[M]**: (1) taxes and refunds reserve, (2) minimum cash buffer of 3 to 6 months of fixed costs, (3) reinvest only in channels with measured payback inside your cash horizon, (4) pay yourself a fixed pro-labore or distribution rule, (5) surplus. Reinvest while marginal contribution per extra real is above 1 and the cash buffer holds; take profit when the marginal channel pays back slower than the buffer. Write the rule down so one good month does not set the lifestyle.

## 8. Platforms, taxes, VAT (dated; open the reference)
- Platform fees (Kiwify, Hotmart, Eduzz, Gumroad, Stripe, Paddle, App Store, Google Play), merchant-of-record vs payment processor, payout times: `references/platform-fees-taxes-br.md`. A merchant of record handles sales tax and VAT on your behalf; a processor does not **[C]**.
- Brazil: MEI limits and allowed activities, Simples Nacional annexes, Fator R, invoices, when to hire an accountant: same file, labelled general information. Legal structure choices go to an accountant or lawyer.
- EU VAT on digital services: place of supply is where the consumer is; the One Stop Shop (OSS) lets one return cover EU states **[C]**; thresholds and non-EU rules in the reference.
- Bookkeeping hygiene: separate business account and card, every sale reconciled with a platform statement, monthly close (checklist in `playbooks.md` 6), receipts stored.

## AI tells to avoid (check while answering, not after)
- Generic advice that would fit any business, instead of the user's own numbers.
- Benchmarks or market sizes stated as fact, with no source.
- Round-number assumptions with no source or range.
- Frameworks named (SWOT, Canvas, Van Westendorp) but not applied to the case.
- "It depends" without saying on what and what to do.
- Long option lists with no recommendation.
- Confident tone on unverified fees, laws or rates.
Fix: use the user's data, show the arithmetic, give a range and the assumption, then one recommendation with its reason and the next check. Say what you chose and why in one line; a choice without a reason is removed.

## 9. Which reference to open
- Something is wrong ("selling but no money", "ads profitable on the platform but not in the bank", refunds, churn, tax surprise): `references/diagnosis-playbook.md`.
- Need a sheet, template, break-even, scenarios, launch budget, monthly close: `references/playbooks.md`.
- A fee, MEI/Simples or OSS number: `references/platform-fees-taxes-br.md`.
- Sources and verification status: `references/BIBLIOGRAPHY.md`.

## Common traps
- Quoting revenue as if it were profit: platform dashboards show gross sales; the bank shows what is left after fees, refunds and delay.
- Using the headline fee while ignoring the fixed part per sale, instant-payout fees, instalment (parcelamento) costs and currency conversion **[M]**.
- A break-even computed with a ROAS target but without refunds or taxes: ROAS 2 on R$97 is not profit when the sale leaves R$73.
- One scenario only. Always show the low case next to the base case.
- Mixing personal and business money, so no month can be closed.

## 10. Deliver
State inputs and assumptions, show the arithmetic line by line, give the answer (contribution, break-even, runway), the sensitivity that matters most, the decision with reasons, and what could not be verified (a fee page that needs a browser, a tax rule to confirm with an accountant). Computed numbers come from a script, not mental math.

Boundaries: price and offer design in offers and pricing; growth metrics, funnels and experiments in growth-analytics; market sizing in market-research; ad buying in paid-traffic; legal and tax for a specific case to an accountant or lawyer.
