# Playbooks: routines for offers

Short procedures to run, with the stop conditions. Evidence tags as in `SKILL.md`: **[C]** consensus or law, **[M]** serious single study, **[F]** practitioner hypothesis, **[X]** myth, **[EU]** EU consumer-law constraint. Law details live in `eu-consumer-law.md`; numbers and tests in `metrics-and-testing.md`; diagnosis trees in `diagnosis-playbook.md`. Not legal or tax advice.

## 1. Build an offer stack
1. **Core**: one promise phrased as what the buyer does and receives; one main product. Write the customer's alternative and its dated, sourced cost first.
2. **Bonuses with real value**: each passes "would anyone pay for this alone?", has a stand-alone price you have actually charged or can justify by the alternative's cost, and costs you little to deliver. Maximum two; a weak bonus lowers the perceived value of the bundle (presenter's paradox). [M]
3. **Value levers in order** (practitioner model from Hormozi, restated): outcome likelihood and size, shorter time to first result, less effort. Pull these before adding items. [F]
4. **Guarantee type** (see playbook 5): pick one, keep it simple, put it in writing before purchase.
5. **Payment options**: card and local methods the market uses; instalments only through a provider carrying consumer-credit duties (`eu-consumer-law.md` 7). One-click upsells exist only for methods that store credentials.
6. **After payment**: when and how access arrives, the first action, the support route.
Ethical limits (stop if you cannot say yes): no invented "total value", no outcome promises you cannot prove, no scarcity on digital items, no fake reviews or personas, no "free" for what is in the price, no "lifetime"/"unlimited" unless you can honour it as long as the buyer lives. [C][EU]
Output: a one-page stack (component, its job, its price if sold alone, cost to you) plus the floor price and its arithmetic.

## 2. Price test design
1. Write the hypothesis, the primary metric (net RPV), guardrails (refund rate, disputes, support load) and the stop rule **before** starting.
2. One variable: price only, or offer only, never both.
3. Sample size first, via `growth-analytics`: at 3.0% base, +20% relative needs about 14,000 visitors per arm; with 400 visitors a week that is not testable, so test only a large change (price x1.5, offer, page) and call the result weak. [C]
4. Honest method: alternating periods with the same price for everyone, or separate markets; per-profile simultaneous prices need disclosure in the EU (CRD art. 6(1)(ea)). [EU] Run each period at least one full weekly cycle; swap the order and repeat if the effect is small.
5. Check the sample ratio and contamination (Step 0 of the diagnosis playbook).
6. **Do not read the result until the refund window of the last cohort has closed**; provisional numbers must say so. Decide with net RPV after refunds, plus the backend if measured.
7. Record: arms, dates, visitors, orders, net RPV, refunds at closure, decision, what would reopen it.

## 3. Launch a promotion legally (EU)
1. Decide start and end dates, discount and what it applies to; they are final before the announcement. A deadline you extend is false for everyone who bought because of it (UCPD Annex I point 7). [C][EU]
2. Compute the **prior price** per product and country: the lowest price applied in the 30 days before the reduction, including earlier promo prices (Directive 98/6/EC art. 6a as inserted by Directive 2019/2161; Commission guidance 2021/C 526/02). Compute the % on it. The system computes it, not a human by hand. [EU]
3. Scope: art. 6a covers goods at EU level; digital content and services are still under the UCPD misleading-advantage rule and member states may go further. **Check the buyer country's law**; the safe default is to show the 30-day lowest price. [LAWYER]
4. No "was" price nobody paid; no "worth X" without proof; no seat counts or stock on digital items; no countdown that resets; no personal "just for you" code that everyone gets. [EU]
5. Answer for yesterday's full-price buyer before launch (credit, a bonus, or an honest note about the date); write it down.
6. After the promo: the promo price becomes the 30-day lowest price for the next month; plan the next reduction accordingly.
7. Gift and per-person rules written (limit per account, what if the recipient owns it).
8. Dated launch price: the cleanest urgency, but it can itself count as a reduction announcement against a future higher price. [EU]
Check list result: dates, prior price table, copy handed to `copywriting`, ad claims checked with `ad-creatives`.

## 4. Design the bump, upsell and downsell sequence
1. Order: front offer → one unticked bump in checkout → payment → one upsell as an explicit offer → at most one downsell on decline → access delivered. [EU]
2. Bump: cheap, one line, exact price, tied to the main item. Upsell: same promise, more speed, access or personalisation; price 2-5x the front is a practitioner start, not a rule. [F][1-SRC]
3. Every extra payment repeats the total price, what it is, the pay-obligation button and, for immediate digital content, its own withdrawal waiver steps. [EU]
4. Decline is neutral and equal in weight; no guilt wording; the main purchase never waits on the upsell.
5. Split take rate by payment method (methods without stored credentials do not get true one-click).
6. Run a control without the bump or upsell at least once; decide by net RPV after refunds, and watch the refund rate and disputes of the extra-purchase buyers. See `bump-upsell-downsell.md` for numbers and recovery sequences.

## 5. Write the guarantee policy
1. Pick the type: unconditional time-based (simplest; raises purchases more than returns [M]), conditional (effort-based; clear proof needed, easily seen as a trap), or outcome-based (only if you can measure the outcome honestly; a promise of results is a claim that needs proof [EU]).
2. Window: longer windows tend to lower returns; breadth of scope raises them. [M] Offer 30 days as a start; compare it with the legal withdrawal period.
3. Write as a commercial promise **beyond** the law; never sell the statutory right as a feature (UCPD Annex I point 10). Keep the digital-content waiver steps (express request, acknowledgement of losing the right, durable-medium confirmation) separate from the guarantee text (CRD arts. 16(m), 8(7)). [EU]
4. State how to claim (one email or form, no call) and when money arrives (same method, within 14 days in law).
5. Anti-abuse rule visible before purchase: one refund per person, scope, what happens to access.
6. Honour it: refund fast, do not argue, log the reason; reasons feed the diagnosis playbook.
7. Have it read once by a lawyer for the markets sold in. [LAWYER]

## 6. Weekly offer metrics review (30 minutes)
Run on closed cohorts only; mark provisional ones.
1. Step 0 data check (attribution, net, refunds counted, currency).
2. Net RPV this week vs 4-week mean, by source and by country; decompose into CR and AOV.
3. Bump and upsell take rates among those who saw them; control comparison if running.
4. Refund rate by cohort (day since purchase) and by source; disputes against the warning threshold.
5. Tests running: stop rule status, sample, contamination flags. One test per step.
6. Promotions: next dates, prior-price table, answer for earlier buyers.
7. Decision log: what was decided, the number it rests on, what would reopen it. Thresholds are your own history; vendor benchmarks are hypotheses. [F]
