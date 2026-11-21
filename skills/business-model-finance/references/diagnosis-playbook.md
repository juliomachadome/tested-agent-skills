# Diagnosis playbook: business model and finance

Step 0, always: is the data trustworthy? Match three sources before reading anything: platform sales report, payout/bank statement, and ad platform spend. If gross sales minus fees, refunds and chargebacks does not match the payouts within 1 to 2%, fix the reconciliation first (timing, currency, partial refunds, instalments, affiliate commissions). A conclusion built on dashboards that do not match the bank is a guess.

Numbers below use the example in `playbooks.md` (R$97 course, 300 sales).

## Tree 1: "I sell but there is no money left"
1. Compute contribution per sale (playbooks 1). Is it close to the price? 75% before ads means 25% is gone before you pay for traffic.
2. Is contribution after ads above the fixed cost per sale? 32.98 x 300 = 9,894 vs fixed 2,500: yes here. If no: price, volume or CAC problem; run the sensitivity (playbooks 4) and fix the biggest lever.
3. Did owner pay, taxes or tools leave the same account? Separate accounts; recompute with a pro-labore line.
4. Are payouts delayed (card 15 days, instalments)? Cash is behind the result by one cycle; see tree 2.
5. Check recurring costs not in the sheet: tools, support hours, platform plan, subscriptions of subscriptions.
Fix: raise contribution (price, bump via offers, fee plan), lower CAC, cut fixed cost; only then scale.

## Tree 2: "Revenue up, cash down"
Likely causes: ad spend paid now, revenue received later; payout lag; refund window not yet expired; annual tool or tax bill; stock or production paid ahead; owner withdrawals; instalment sales paid monthly.
Check: cash forecast per month for 3 months with real dates; list receivables by payout date. Test: opening cash + receipts - payments = closing cash each month; the gap is the lag.
Fix: smaller ad budget steps, shorter payout (platform early-payout option, check its fee), reserve for refunds, annual plans or presales to bring cash forward.

## Tree 3: "Ads are profitable on the platform but not in the bank"
Platform ROAS counts gross sales at purchase date and often ignores refunds, chargebacks, fees, tax and attribution overlap.
Check: ROAS needed to break even = price / contribution before ads per sale = 97 / 72.98 = 1.33. Platform ROAS of 2.4 (97 / 40) is true profit only if refunds and chargebacks are as assumed and every attributed sale is real. Compare ad-platform purchases with platform sales for the same days; the difference is attribution inflation or double counting.
Fix: judge channels on bank-reconciled sales per R$ of spend (blended CAC), hold back a refund reserve, report cash after 30 days.

## Tree 4: "Refunds and chargebacks are eating margin"
Quantify: each 1 point of refund rate on 300 sales at R$97 is 3 sales x R$97 = R$291 lost revenue per month, plus non-returned fees; 7% to 10% cost R$821 per month in the example. Chargebacks cost the sale, often a fee and risk the processor account.
Check by cohort: refunds by traffic source, offer, week after purchase, device, payment method, reason. A spike in one source points to a promise mismatch (copywriting) or poor traffic; a spike in a week points to delivery or expectations (customer-support).
Fix: align promise and product, clearer descriptor, faster support, fraud rules; do not hide refund buttons (consumer-law risk, see offers). Model the target rate in the sheet, not zero.

## Tree 5: "Subscription churn hides growth"
MRR rising can come from new sales while the base leaks. Check: new MRR, expansion, contraction, churned MRR per month. Example: 120 customers, 5% churn loses 6 per month; 10 new covers it and growth slows towards 200 customers at 10 new per month. Monthly 5% is 46% a year.
Check cohorts: churn in month 1 to 3 is an onboarding or promise problem; later churn is value or price. Separate voluntary from failed-payment (involuntary) churn; the latter is often the cheapest fix (retry, card-update emails).
Fix: lengthen life before buying more volume; each point of churn removed moves LTV more than a CAC cut at small base. Deeper LTV and retention: growth-analytics.

## Tree 6: "Taxes surprised me"
Likely causes: revenue passed a regime limit (MEI, Simples bracket, sublimit); tax is due on invoiced revenue, not on what you kept; income of the month is revenue before platform fees; VAT abroad not collected; annual declaration; income tax on distribution or pro-labore.
Check: monthly revenue on the tax basis to date versus the limit, and the date taxes fall due; ask the accountant which invoices are required and which base the regime uses.
Fix: reserve a tax percentage on each payout into a separate account; track revenue against the limit monthly (`platform-fees-taxes-br.md`); get an accountant before crossing the limit, not after. General information, not tax advice.

## Tree 7: "Does this business make money?" (new idea)
1. Contribution per sale with fees, refunds, tax and an honest CAC. 2. Break-even units against fixed costs. 3. Is break-even reachable with the traffic you can afford (units / conversion)? 4. Low case result and runway. 5. If it only works in the high case, rewrite the model (price, channel, cost) before building.
