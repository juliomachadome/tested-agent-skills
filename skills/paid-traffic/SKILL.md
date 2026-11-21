---
name: paid-traffic
description: "Use to plan, diagnose, read and scale paid media on Meta, TikTok and Google/YouTube: break-even CPA and budget, account structure, test, kill and scale rules, and a symptom-to-cause diagnosis tree for CPA up, CTR down, CPM spike, fatigue, learning limited, delivery stopped, pixel vs backend gaps, CAPI dedup and Event Match Quality, attribution windows, UTMs, consent and Performance Max/Advantage+ effects; also reads pasted ads-manager CSVs and reconciles them with backend revenue (MER, incrementality). Triggers: \"why did CPA go up\", \"should I kill this ad\", \"how do I scale\", \"learning limited\", pasted ads numbers. Plans and reads; never operates an account. Not for what to charge or the offer itself (offers), ad concepts and scripts (ad-creatives), page copy (copywriting) or organic search (seo-geo)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Paid traffic

One inequality governs everything: **net revenue per visitor ≥ cost per visit.** CPM, CTR, hook rate and platform ROAS only explain why it holds or fails. Spend the minimum on what is bad and the maximum on what is good, with rules written **before** looking at the dashboard.

Evidence tags: **[C]** official docs, law or replicated · **[M]** serious but biased sample · **[F]** practitioner rule or vendor data, a hypothesis · **[X]** myth · **[1-SRC]** single source · **[EU]** EU law/consent · **[MATH]** computed here. Platform facts change fast: references carry read dates; reopen the source if older than ~3 months and the decision is expensive.

## Levers, biggest first

Offer and price → page and funnel → creative → account structure and bid. The buyer controls the last two; if cold traffic does not buy after several creatives and entry points, go back to offer and page. [F]

## Three numbers before the campaign exists [C][MATH]

| Number | Formula |
|---|---|
| Average order value (AOV) | entry price + bump price × measured take + upsell price × measured take |
| Margin per order | AOV net of tax − payment fee − expected refunds − variable cost |
| **Break-even CPA** | = margin per order |
| Target CPA | break-even × (1 − desired margin); during validation, target = break-even |
| Break-even ROAS | gross AOV ÷ break-even CPA |
| **Max cost per visit** | page conversion × margin per order |
| Minimum conversion | cost per visit ÷ margin per order |

Also write the **loss ceiling of the validation phase** ("spend up to 30× break-even CPA; stop if 7-day CPA is not within 1.5× break-even by then"). Without a proven backend, break even on the first order; "lose on the front" only after the upsell is measured with real buyers. VAT charged on ad invoices may be a cost for VAT-exempt sellers [ACCOUNTANT].

## Core principles

1. **Decide on backend net revenue, not platform ROAS.** The dashboard uses gross revenue, its own attribution window and only the purchases it sees. Hierarchy: backend orders (truth) > site analytics (consented only) > platform dashboard (modelled). [C]
2. **Budget comes from CPA, not taste.** To exit Meta's learning phase: ~50 optimisation events per week → daily budget ≈ 50 × CPA ÷ 7. To read one creative: 2-3× CPA per creative. If the budget pays for neither, shrink the test (fewer creatives, one entry point) instead of pretending it fits. [C][MATH]
3. **Few ad sets, broad audience, genuinely different ads.** Every ad set needs events to learn; splitting budget starves all of them. With Advantage-style automation, the creative does the targeting. [C]
4. **Judge where the budget is split.** Platforms allocate by marginal cost, so the ad or placement that got more spend can show a worse average CPA and still be right (the "breakdown effect"). [C]
5. **Few purchases do not make a winner.** Kill and win by the statistics tables in `references/testing-and-scaling.md`: default pause at **2.5× target CPA with zero purchases**; "candidate" at 3-5 purchases within target; "winner" at 10+ or repeated in another week. [MATH]
6. **Creatives enter in weekly batches** (adding an ad is a significant edit), at least one new concept per batch. [M]
7. **Scale by marginal CPA.** (new spend − old spend) ÷ (new purchases − old purchases). When marginal CPA passes break-even, that step does not pay, even if the average still looks fine. Steps of 20-30% every 3-4 days are a conservative habit, not a platform law. [M][F]
8. **Consent is not optional and server events are not a loophole.** In the EU, pixel and server-side events only with marketing consent; sending a refuser's purchase via the server is the same infringement by another path. [C][EU]
9. **Ad and page are one pair.** High CTR with low conversion almost always means the first screen does not repeat the ad's promise: fix with copy/UX, not more budget.
10. **The agent never operates the account.** It plans, reads and recommends; the owner creates, edits, pauses and pays.

## AI tells to avoid (check while answering, not after)
- Generic advice ("test more creatives", "optimise the audience") not tied to the user's spend, CPA and break-even.
- Invented benchmarks (CTR, CPM, CPA, ROAS "for the niche") stated as fact.
- Calling an ad a winner or loser with no purchase count, no interval and no threshold written beforehand.
- Listing every platform metric without applying the CPA decomposition.
- "Test everything": no hypothesis, budget or kill rule.
- Long option lists with no prioritised plan.
Fix: use the user's data, show the arithmetic, state the uncertainty, give one recommendation with its reason and the next check.
Say what you chose and why in one line; a choice without a reason is removed.

## Routing

| Task | Read |
|---|---|
| **Something is wrong** (CPA, CTR, CPM, fatigue, learning limited, delivery, tracking mismatch, policy) | `references/diagnosis-playbook.md` (Step 0, then the tree) |
| **What to change, in which order**; scale, kill, test design, refresh, weekly review and report template | `references/optimization-playbook.md` |
| **Pasted CSV or screenshot**, platform vs backend ROAS, MER, lift and geo tests | `references/reading-data.md` |
| Platform mechanics (Meta, TikTok, Google) and the verification ledger of what is official | `references/platforms.md` |
| Structure by budget, optimisation event, audiences, bids, naming | `references/account-structure.md` |
| Kill/winner statistics, page tests, scaling phases, fatigue | `references/testing-and-scaling.md` |
| Stage metrics, attribution, UTMs, consent, country research, myths | `references/measurement-diagnosis.md` |
| Sources, with status (verified / seen via search / unverified) | `references/BIBLIOGRAPHY.md` |

## Diagnosis protocol (when numbers are pasted or something broke)

1. **Ask for the data** if missing: period, timezone, attribution setting, level, spend, impressions, link clicks, landing page views, purchases and value, plus backend orders with source for the same days, break-even CPA, edit history, consent share.
2. Run Step 0 of the diagnosis playbook (is measurement right?), then decompose CPA = CPM / 1000 / (CTR x visit rate x page conversion) and walk the branch whose factor moved.
3. Give the **fix list with the math** (budget needed = 50 x CPA / 7; marginal CPA; kill threshold), ordered by the lever order, each with the metric and threshold that would confirm it.
4. End with **what could not be verified** (platform rule not confirmed, data missing, sample too small).

## Workflow

1. Write the three numbers, loss ceiling, kill/winner/scale/step-down rules.
2. Pre-flight: a test purchase shows in the backend with source, campaign and creative **without accepting cookies**; pixel + server events deduplicated under consent; landing and checkout tested inside the Instagram, Facebook and TikTok in-app browsers with the cookie banner on screen; account hardening (business verification, 2FA, a second trusted admin, spend limit, correct currency and time zone, beneficiary/payer fields decided [EU]).
3. Structure by the budget table (`account-structure.md`).
4. Daily 5-minute check at a fixed time; weekly batch and readout.
5. Scale through the phase gates; step down by the written rules.
6. Hand back to each specialist what is theirs (offer: CPA and RPV per entry point; creative: cuts and winners with counts; copy/UX: pairs with high CTR, low conversion).

## Output format

Verdict with its number; the three numbers with formulas; source (backend / analytics / dashboard) and period for every figure; decisions per item with the triggering rule; "no volume to conclude" where true; flags ([ACCOUNTANT], [LAWYER], consent and tracking gaps); **could not verify** line.

## Checklists

**Before launch:** workflow step 2 done; three numbers and loss ceiling written; events deduplicated (same name and `event_id`), test code removed; UTM convention, one link per ad; ads checked against policy and consumer law; kill, winner, scale-up, step-down rules written.

**Daily (5 min):** spend as planned, rejected ads, backend purchases per campaign; 3x CPA spent with no sale: check payment, page, pixel first; no edits outside batch day except rule-based cuts.

**Weekly:** use the review ritual and report template in `optimization-playbook.md`.

**Before raising budget:** 7-day CPA at or below target with volume; last step's marginal CPA at or below break-even; two winners live and a batch ready; support and refunds can absorb the volume.
