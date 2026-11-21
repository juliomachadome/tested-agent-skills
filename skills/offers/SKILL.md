---
name: offers
description: Build, review or fix the offer behind a digital product, course, info-product, coaching or service, or a low-ticket funnel - what is sold, positioning and the claims you can prove, offer and mechanism naming, the promise, price and anchor, comparison ("was/now") price, guarantee and refunds, order bump, upsell/OTO and downsell, bonuses, promotions and urgency, gift codes, quiz funnels - and read the numbers (revenue per visitor, take rate, refunds, disputes). Use it whenever someone asks "what should I charge", "should I add a bonus/bump/upsell", "is this discount legal", "write a guarantee", "build a quiz funnel", "my offer converts badly", or plans a sale, Black Friday or launch price, even if they never say "offer". Brings the arithmetic, diagnosis trees and the EU consumer-law limits. For SaaS tiers and plans use pricing; for the words on the page use copywriting.
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Offers

An offer is five things, not one number: **what the buyer gets + what it solves + what it costs + what happens if it does not work for them + why act now (only if there is a real reason)**. A weak offer is not rescued by a discount. This skill builds the offer, chooses the number with arithmetic, keeps every tactic inside consumer law and decides with funnel-level metrics.

Evidence tags: **[C]** consensus, law or official docs · **[M]** serious but single/old/lab study · **[F]** practitioner rule, vendor data, one case: a hypothesis to test · **[X]** myth. **[1-SRC]** rests on one source. **[EU]** an EU consumer-law constraint. Nothing here is legal or tax advice: flag **[LAWYER]** / **[ACCOUNTANT]** questions instead of answering them. Sources and their check status: `references/BIBLIOGRAPHY.md`.

## Start: project first, then the 6-line diagnosis

0. **Project first**: read the current project's CLAUDE.md or AGENTS.md, pricing and legal docs, glossary, past tests and closed decisions. They override this skill on project matters; never import prices, markets or numbers from another project.
1. Who buys and what they would do without the product (nothing, free content, a competitor) and what that costs in money and time.
2. The single promise, as what the buyer does and receives, not an outcome you cannot prove.
3. Current price, taxes, payment fees, refund rate, delivery/support cost (the floor).
4. Market and payment methods (decides one-click upsells, disputes, tax).
5. Funnel stage being changed (front offer, bump, upsell, promotion).
6. Traffic and volume per week (decides what can be tested at all).
Missing data: ask once, or state the assumption and call the result a hypothesis.

## Core principles

1. **Offer before price, value before cost.** Three rulers in order: value to the customer (ceiling), alternatives (reference), cost and margin (floor). [C]
2. **Few strong components beat many weak ones.** A weak bonus lowers the perceived value of the whole. [M] Ask of each item: would anyone pay for this alone?
3. **The customer's alternative is the anchor that needs no trick**: its cost, with source and date.
4. **Honest anchors only**, safest first: the alternative's cost (sourced, dated) → price per unit/day from the real price → a dated future price that will apply → a previous price really charged (30-day rule). Never a "was" price nobody paid, a summed "value" with no proof, or a non-equivalent comparison. [C][EU]
5. **Decide by net revenue per visitor (RPV)** = (revenue − tax − fees − refunds) ÷ visitors, never by conversion or AOV alone. [C]
6. **Every recommendation ships with arithmetic**: current, proposed, break-even condition (at 49, keeping 76% of the conversion at 37 earns the same).
7. **Easy refunds cost less than disputes.** A simple generous guarantee tends to raise purchases more than returns; longer windows tend to lower returns, wide scope raises them. [M]
8. **Urgency only when real, definitive and equal for everyone.** A dated launch price is the cleanest. Extending a deadline makes it false. [C][EU]
9. **Bump and upsell are measured against a control**; a take rate does not prove extra revenue. [C]
10. **Low ticket is an acquisition model.** Without a measured backend, the front must break even alone. [F][1-SRC]
11. **Whoever paid full price yesterday must not feel punished.** Decide the answer before any promotion; never raise a price silently.
12. **Positioning is a claims ladder**: *can say* (proven), *not yet* (built, unmeasured), *never* (outcome promises, invented numbers, fake reviews). Competitor facts need source and date.
13. **One name for offer and mechanism, from ad to receipt**; test by purchases, not clicks.
14. **App-store sales follow the store's rules** (price tiers, no pointing to cheaper paths): check current guidelines with a date. In-app upgrade screens belong to `paywalls`.

## AI tells to avoid (check while answering, not after)
- Generic advice that would fit any business, instead of the user's own numbers.
- Benchmarks or market sizes stated as fact, with no source.
- Round-number assumptions with no source or range.
- Frameworks named (SWOT, Canvas, Van Westendorp) but not applied to the case.
- "It depends" without saying on what and what to do.
- Long option lists with no recommendation.
- Confident tone on unverified fees, laws or rates.
Fix: use the user's data, show the arithmetic, give a range and the assumption, then one recommendation with its reason and the next check. Say what you chose and why in one line; a choice without a reason is removed.

## Which reference to open

| Task or symptom | Open |
|---|---|
| Something is wrong: RPV down, AOV low, bump or upsell off, price test confusing, refunds or chargebacks up, abandonment, churn, CAC not paid back, a price claim challenged | `references/diagnosis-playbook.md` (Step 0 data check, trees, worked math) |
| Doing a routine: build an offer stack, design a price test, launch a promotion, sequence bump/upsell, write a guarantee, weekly review | `references/playbooks.md` |
| Any discount, "was/now", %, launch price, Black Friday, codes, guarantee wording, withdrawal right, pre-ticked boxes, VAT | `references/eu-consumer-law.md` |
| Bump, upsell/OTO, downsell, one-click, recovery, gift codes | `references/bump-upsell-downsell.md` |
| Quiz funnel, mechanism/name tests, low-ticket validation | `references/quiz-and-low-ticket-funnels.md` |
| Charm prices, anchoring, decoys, price as quality signal, WTP surveys, myths; value-proposition and revenue-stream checklists; reciprocity and scarcity limits | `references/price-psychology-evidence.md` |
| Metric definitions, sample size, refunds by cohort, dispute thresholds | `references/metrics-and-testing.md` |
| What a book or study supports and whether it was checked | `references/BIBLIOGRAPHY.md` |

Neighbours: words on the page `copywriting`; ad hooks and claims `ad-creatives`; budgets and cut rules `paid-traffic`; sample size, tracking, test reading `growth-analytics`; SaaS tiers `pricing`; in-app upgrade screens `paywalls`; refund replies `customer-support`.

## Workflow

1. Diagnosis (above); if the task is a problem, run Step 0 of the diagnosis playbook first.
2. List the customer's alternative and its cost (sourced, dated).
3. Build the offer: one promise, one main offer, each component passes the "pay for it alone" test, a guarantee you can keep, what happens after payment (`playbooks.md` 1, 5).
4. Compute floor and break-even: price − consumption tax − payment fee (fixed + %) − expected refunds − delivery/support. Fixed fees weigh heavily below about 5 EUR; compute per payment method. [C]
5. Pick an honest anchor and store its proof.
6. Law check for the target market (`eu-consumer-law.md`; national law can go further).
7. Define measurement: RPV per arm, a control, refunds by cohort and source, stop rule written first (`playbooks.md` 2).
8. Hand off: copy to `copywriting`, flow to `ux-design`, budget to `paid-traffic`.

## Output format

```
Recommendation (2-3 lines) + the number that supports it
Arithmetic: current vs proposed, break-even conversion
Offer: promise · components (each with its job) · price · anchor (+ proof) · guarantee · after-payment
Legal check: items touched [EU] and what was verified; [LAWYER]/[ACCOUNTANT] questions
Test plan: hypothesis, metric (RPV), control, sample/stop rule
Risks, what is unverified, and what would reopen the decision
```

## Quick checks before sending

- Final price with tax, local currency, identical on every screen; total before the order. [EU]
- Any reduction signal (strike-through, %, "sale", "instead of", "launch price") uses the 30-day lowest prior price; dates final. [EU]
- Bump unticked with exact price; upsell presented as an offer with price, pay button and its own waiver; neutral decline. [EU]
- Guarantee is a keepable promise beyond the law; the legal right is not sold as a feature.
- Nothing in the price is called "free"; no invented "value"; no seat counts on digital items.
- Price tests: same price for everyone in a period; refund window closed before reading.

## What this skill will not do

- Invent "value" totals, fake deadlines, reviews or expert personas.
- Promise outcomes ("fluent in 30 days", "lose 5 kg"): it describes what the buyer does and gets.
- Give a legal or tax opinion: it flags the question and the rule to check.
