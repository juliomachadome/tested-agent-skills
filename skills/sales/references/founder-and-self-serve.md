# Founder-led and self-serve sales

Evidence mostly **[F]** (practitioner); numbers are starting hypotheses to replace with your own data.

## 1. When to sell by hand, when to let the product sell
| Signal | Sell by hand (founder or sales) | Let self-serve carry it |
|---|---|---|
| Price per account | high enough that a 30-60 min human cost is repaid (rule of thumb: ACV above roughly 5-10x the cost of a sales hour set) | low ticket, card-ready |
| Time to first value | long, needs setup, data or integration | minutes, no setup |
| Buyer | many stakeholders, security or legal review, procurement | the user is the buyer |
| Product stage | fewer than ~20-50 customers; objections unknown | the pitch and onboarding are repeatable |
| Churn risk | needs adoption work | low-touch works |
Hybrid is common: self-serve entry, human help where value and need meet (product-qualified accounts).

## 2. Founder-led phase (first 20-50 deals)
- Do every sales call yourself, record with consent, tag each objection and the exact words used. After 10 similar closes you have a pitch; before that you have hypotheses. Do not hire a salesperson to find the pitch for you.
- Keep a one-page "why we win / why we lose" and update weekly. The loss reasons feed the roadmap and pricing.
- Use discovery that asks about past behaviour and spend (the Mom Test idea), not whether people like the idea.
- Outbound pattern (Ross, Predictable Revenue [F]): defined ICP, a short value-first message, a metric per step (sent, replied, meeting, opportunity); its examples are dated and email-heavy, so use the metrics logic, not the 2011 scripts. Prospecting discipline (Blount) is a volume-and-consistency argument [F]; combine with consent rules.
- Hire the first rep when: pitch repeatable, ICP clear, 10+ closes with similar buyer and sales cycle, a documented playbook, and demand exceeds your hours.
- Customer-development detail (what to test, what counts as an early customer, how to read test sales, the sales closer vs a sales VP): section 7.

## 3. Pricing page and trial hand-off
- A pricing page that hides price forces a call: acceptable for enterprise, a leak for low ticket. Show tiers, the metric price scales with, and who each is for; keep "talk to us" for the top tier. (Price design itself: use the `offers` skill and `pricing`.)
- Trial or freemium: define the **activation event** (the action that predicts retention, found from your data, not guessed) and the target time to reach it. Hand-off to a human only after a product signal, not on day 1.
- Do not put a call in front of a card form. Offer help at the moment of stuck (in-app, email triggered by failed step).

## 4. Product-qualified leads (PQL)
A PQL is an account whose usage pattern correlates with paying. Build it: take paid accounts of the last 6-12 months, list the first-14-day behaviours (invited teammates, reached activation event, used a key feature N times, hit a limit), compare with churned trials, choose 2-3 signals that separate them. Set the route: PQL → human outreach within one business day with a message about their use, not a generic "can I help?". Check the PQL monthly: share of PQLs that convert vs non-PQLs (should be clearly higher; if not, the signal is wrong).

## 5. Metrics for the funnel (define each before reporting)
| Metric | Definition | Starting hypothesis [F] |
|---|---|---|
| Visit → signup | signups ÷ unique visitors, by source | 2-5% for a clear B2B product page |
| Signup → activated | activated ÷ signups (activation event, within X days) | varies widely; improve the weakest step first |
| Activated → paid | paid ÷ activated | free-trial B2B often 10-25% of activated, card-upfront trials higher conversion but fewer starts |
| Demo request → held | held ÷ requested | 60-80%; below means slow response or weak confirmation |
| Demo held → paid | closed-won ÷ held | 15-30% in qualified mid-market, lower for unqualified inbound |
| Trial → paid by sales touch vs none | conversion with and without human help, same cohort | tells if the hand-off earns its cost |
| CAC payback | acquisition cost ÷ monthly gross margin per customer | under 12 months is a common target; see `growth-analytics` |
These are not industry benchmarks; compare each to your own previous quarter and to the same cohort. Min sample before concluding: 100 trials or 30 closes per cohort, else say so.

## 6. Diagnosis for self-serve (symptom → check)
- Many signups, few activated: check time to activation, first-run friction, wrong audience from a channel (segment by source).
- Activated, no pay: pricing page clarity, limits too generous or too tight, no trigger to upgrade, missing procurement route (invoice, PO).
- Pay then churn month 1-3: promise mismatch, activation not sustained; look at the first 30 days of usage.
- Sales touches don't lift conversion: PQL signal weak, human contact late, the product is simple enough not to need help.

## 7. Customer development for the first sales (Blank and Dorf) [F]
Source: The Startup Owner's Manual (ch. 4, 6, 7-9). Practitioner method from the authors' teaching and startups, widely used, no controlled trials; the numeric thresholds are rules of thumb, not data. Think of the first sales as a search for a repeatable business model, not as execution of a plan.
- **Test the problem before the product (ch. 4).** First meetings use a short problem page, not a product deck: the problems you assume, how the buyer solves them today, your idea in one line. Most of the meeting is the buyer talking; ask which problems rank highest, which are must-fix vs nice-to-fix, what the problem costs (money, time, customers), what they tried, who else has it, and who else you should talk to. Close by asking what hurts most in how they work and what you should have asked. Large companies: arrange one-on-one conversations with the decision-maker, the heavy user and the influencer before or after group meetings; people hold back when the boss is in the room.
- **Score what you hear (ch. 4).** One row per conversation: excited, urgent need, business impact, home-made workaround, likelihood to sign within a stated time (weight it if cash is short), whether you spoke with someone who can decide. Do not discard outliers. If most rows show "urgent" but few show a near-term order, suspect a weak value or price story, or the wrong level of contact.
- **Signals worth acting on (ch. 6):** customers rating the problem 8-10 of 10, a workaround already in use, referrals to colleagues, "when can I get it?". Lukewarm enthusiasm rarely makes a scalable business. For enterprise products the authors suggest three or four strong early customers plus a similar number in the pipeline, from more than one segment, as a start; consumer products need far more (tens), web or mobile apps on the order of a hundred activations, and network-effect products hundreds of engaged users; treat these as rough hypotheses.
- **Build a sales roadmap before building a sales team (ch. 7-8).** Written answers to: who influences, recommends, decides and holds the budget (and who may block it), how many calls per sale, how long a sale takes, what the buyer's key problems are, what an ideal early customer looks like, and where leads will come from. Hiring salespeople before that map exists burns cash and slows learning. Test one channel at a time.
- **The early customer (ch. 9).** Look for the buyer who has the problem, knows it, is already trying to fix it (even with a spreadsheet), has a budget and can sign; the authors call them earlyvangelists. A visionary without budget is a friend, not a customer. Expect a low hit rate (their rule of thumb: about 1 in 20 prospects engages and about 1 in 3 of those orders). Mainstream buyers who "will test when it ships" are future customers: keep them in the list.
- **Test-sell at close to full price (ch. 9).** Free or deeply discounted deals prove nothing about buying intent; frame early access as a programme (only say seats are limited if they really are). Beware two traps from early customers: requests for custom features (fine if several customers ask for the same thing, deadly if it turns you into a custom shop) and exclusivity or "best price forever" clauses (do not give up the right to sell to others). Every request needs the buyer's reason first (the Mom Test habit, `product-management` skill).
- **Make each call a test.** Write the pass/fail line in advance ("2 orders from 10 calls", "an average of 6 units within 3 months"), end every call-sheet with four fixed questions (is an order in hand or on its way, how many units or how much, what is needed to sign, when), and log why buyers said no and at which stage they dropped out; the authors rank understanding no above understanding yes. Build a probability-weighted forecast from those sheets only as a rough guide.
- **Founders lead; a closer helps (ch. 8-9).** Founders stay in front of customers through validation; if nobody on the team can negotiate with a buyer or a purchasing manager, add an experienced early-market closer (someone who likes new markets, listens well and does not need to build an organisation) rather than a sales VP who will scale before the model is proven. A closer does not replace founder conversations.
- **If no orders come:** go back to the hypotheses: wrong segment, no early customer found, weak value proposition, price or channel. Agree a number of orders that proves the model with the board in advance: the authors suggest three to five repeatable sales to the same segment for large enterprise deals, and a retailer's re-order for consumer goods; there is no single magic number.

