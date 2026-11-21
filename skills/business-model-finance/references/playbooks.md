# Playbooks: business model and finance

Worked numbers computed with python3 on 18/11/2026. Inputs are examples, not market data. Fee levels are from `platform-fees-taxes-br.md` (dated); assumptions are marked (A). Tax rate 6% is an assumption, not your regime.

## 1. Unit-economics sheet (course, R$97, Kiwify-style fee)
Inputs: price R$97; 300 sales/month; fee 8.99% + R$2.49 per sale (Kiwify page, 18/11/2026); refunds 7% (A) with fees not returned (A, check terms); chargebacks 0.5% (A) at R$30 each (A); revenue tax 6% (A); ads R$12,000/month; fixed costs R$2,500/month (A).

| Line | Per sale (sold) | Month (300) |
|---|---|---|
| Gross sales | 97.00 | 29,100.00 |
| Platform fee (11.21 per sale, 11.6% of price) | -11.21 | -3,363.09 |
| Refunds (7%) | -6.79 | -2,037.00 |
| Chargebacks (0.5% of sales at 97 + 30 fee) | -0.64 | -190.50 |
| Tax on kept revenue (6%) | -5.38 | -1,615.05 |
| Contribution before ads | 72.98 | 21,894.36 |
| Ads (R$40 per sale) | -40.00 | -12,000.00 |
| Contribution after ads | 32.98 | 9,894.36 |
| Fixed costs | | -2,500.00 |
| Result | | 7,394.36 |

Read: only 75% of the price survives before ads; ads take more than half of that. Contribution after ads is R$32.98 per sale. The dashboard shows R$29,100; the bank shows about R$7.4 thousand of profit.

## 2. 12-month P&L and cash template
Columns per month: units, gross sales, fees, refunds, chargebacks, tax, ads, fixed, result, opening cash, payout lag adjustment, closing cash. Keep result (accrual) and cash separate; a payout lag of 15 days on cards shifts about half of a month's receipts to the next month (check payout rules on the platform page).
Example: opening cash R$15,000, ads R$40 per sale, fixed R$2,500, same rates as above, units ramp:

| Month | Units | Result | Closing cash |
|---|---|---|---|
| 1 | 80 | 138 | 15,138 |
| 2 | 120 | 1,458 | 16,596 |
| 3 | 200 | 4,096 | 20,692 |
| 4-6 | 300 | 7,394 | 28,087 / 35,481 / 42,876 |
| 7 | 320 | 8,054 | 50,930 |
| 9 | 360 | 9,373 | 69,016 |
| 12 | 400 | 10,692 | 100,434 |

The first months barely pay for themselves: launch costs (content, tools) are outside this table and must be added in section 5. Ignored here: income tax on distribution, payout lag, seasonality.

## 3. Break-even
Break-even units = fixed costs / contribution per unit. Pick the ads treatment:
- Ads as a variable cost (R$40 per sale): contribution 32.98; fixed 2,500 gives 2,500 / 32.98 = 75.8, so 76 sales = R$7,372 of gross sales.
- Ads as a fixed budget (R$12,000): contribution 72.98; (12,000 + 2,500) / 72.98 = 198.7, so 199 sales = R$19,303. Selling 150 units on that budget loses money.
Break-even revenue = units x price. Margin of safety = (planned units - break-even) / planned units: 300 vs 199 gives 34%.

## 4. Scenario and sensitivity table (same example)
| Scenario | Change | Monthly result |
|---|---|---|
| Low | 200 sales, ads R$12,000 fixed | 96 |
| Base | 300 sales | 7,394 |
| High | 400 sales | 14,692 |
| Ads +30% (15,600) | same 300 sales | 3,794 |

One lever at a time from the base 7,394 (price change holding units constant is optimistic; hand the real price test to offers):
| Lever | Change | Effect on result |
|---|---|---|
| Price +10% (106.70) | | +2,269 |
| Units -10% (270) | | -2,189 |
| Ads +10% | | -1,200 |
| Refunds 7% to 10% | | -821 |
The low case is break-even: a third less volume wipes the profit. That is the finding to report, with the lever (volume, CAC or price) that gives the cheapest protection.

## 5. Launch budget
List before the first sale, with date paid: production (content, video, design, tools), landing page and checkout setup, legal (terms, privacy), tax registration and accountant, test ads budget, support set-up, reserve for refunds (refund rate x expected gross for the first 30 days). Add a stop rule: the amount you accept to lose and the signal (CAC above X after Y sales) at which you stop or change. Example: tests R$3,000 + reserve (7% of R$29,100 = R$2,037) + set-up R$2,000 = R$7,037 needed in cash before month 1 revenue arrives.

## 6. Monthly close checklist (30 minutes)
1. Business account only; export the bank statement.
2. Export the platform statement; match payouts to sales, refunds and chargebacks; list differences.
3. Record platform fees, ad invoices, tools, taxes paid and due dates.
4. Compute contribution per sale and the break-even again; compare with plan.
5. Update cash forecast: next 3 months, with known dates (taxes, annual tools).
6. Pay yourself by the written rule; set aside taxes and refund reserve.
7. Send documents and invoices to the accountant; note questions.
8. One decision for next month (cut, keep, scale) and its trigger.

## 7. Subscription example (SaaS runway and payback)
Inputs (A): 120 customers, ARPA R$150, MRR R$18,000, gross margin 80%, monthly churn 5%, 10 new customers per month from R$6,000 ads, fixed costs R$21,000, cash R$90,000.
- CAC = 6,000 / 10 = R$600; monthly contribution per customer R$120; simple payback 5 months; churn-adjusted payback 6 months; LTV = 120 / 0.05 = R$2,400; LTV:CAC 4.0 (a model **[M]**).
- Month 1 net burn = 18,000 x 0.8 - 21,000 - 6,000 = -12,600; simple runway 90,000 / 12,600 = 7.1 months.
- Month-by-month simulation (churn 5%, 10 new): cash reaches zero in month 9, customers about 150, MRR about R$22,400. Growth stalls near 200 customers (new = churn at 10 / 0.05), so growth alone does not fix this: cut fixed costs or raise new-customer volume.
