# Order bump, upsell (OTO), downsell, recovery

Definitions. **Order bump:** optional add-on inside checkout, before paying. **Upsell/OTO:** offer right after payment, ideally one click. **Downsell:** smaller offer for those who declined. **Take rate:** accepted ÷ saw the offer.

Legal limits for all of this: `eu-consumer-law.md` section 5.

## What public data is worth
- **[F] No independent study of bump take rates exists.** Figures in circulation (30-40% "average", ~30% for low-priced bumps) come from checkout vendors with undefined methods. Use as order of magnitude only. (vendor blogs, read 12/11/2026)
- **[F] Post-purchase upsell in e-commerce:** ~4.7% average and ~28% top decile in one vendor's base of ~40k stores (2023). One vendor, one sector.
- **[C] A take rate does not prove extra revenue.** The bump can lower checkout completion or cannibalise a later purchase. The only valid measure is a control without the bump, comparing net revenue per visitor of the checkout.
- **[M] Door-in-the-face (big ask, then smaller):** meta-analyses find a small effect (r ≈ 0.10-0.15), larger when the second ask comes immediately from the same requester. Supports **one** downsell, not a ladder of insistence. (Cialdini et al. 1975; O'Keefe & Hale 1998; Feeley, Anker & Aloe 2012)

## Practitioner rules, to test [F]
- One bump; cheap relative to the main item (impulse decision, not a second purchase).
- Remove the bump while validating a new offer: it can add an objection at checkout. Add it later behind a holdout. [1-SRC]
- Upsell keeps the **same promise and mechanism** as the front offer and adds one of: faster result, less effort, more access (expert, community), personalisation. [1-SRC]
- Upsell price 2-5x the entry price in low-ticket funnels, starting at 2-2.5x. [1-SRC]
- Upsell metric = contribution per buyer, not take rate (a 1% take on a big ticket can beat 100% on a tiny one).
- Video upsells reportedly beat text pages in that practitioner's tests. [1-SRC] Practitioners also "disguise" upsells as welcome lessons: **banned in the EU** (must present as an offer).
- Ascension points beyond the one-click: e-mail, in-product banner, a call-to-action at the end of each lesson linking that lesson's topic to the next product. Marketing messages (e-mail, SMS, messaging apps) need consent in the EU. [1-SRC for effect sizes]

## Recurring upsell recovery (practitioner sequence) [F][1-SRC]
Annual offer → reminder with benefits to non-buyers → after ~2 days a 20-30% discount → monthly plan → first month at a token price. Reported first-month churn on the monthly plan was 30-50%, falling with product quality; buyers of the monthly plan already declined the annual, so they are less qualified. EU caveats: discounts create a new 30-day lowest price; token-price trials with hard cancellation are an enforcement target; cancellation must take no more steps than signing up.

## Design rules
- The bump is unticked, has an exact price and one line saying what it is.
- Every extra purchase repeats price, what it is, pay button, withdrawal waiver where relevant.
- Decline is neutral and of equal weight; one refusal ends it for the session; at most one downsell.
- Access to the main purchase comes first and never waits on the upsell decision.
- Measure take rate per payment method, over those who **saw** the offer (credential-less methods do not see a true one-click).
- Run a control without bump/upsell at least once; decide by RPV of the whole funnel.

## Combinatorial ticket test [F][1-SRC]
2 front prices × 2 upsell prices = 4 funnels; the winner is the one that puts most money in the bank (front conversion × average order value, net of refunds), not the highest AOV. Needs volume (see `metrics-and-testing.md`).

## Related
Sequence design: `playbooks.md` 4. Bump take rate low, or upsell with refunds and disputes up: `diagnosis-playbook.md` Trees C and D (includes the break-even take-rate formula).
