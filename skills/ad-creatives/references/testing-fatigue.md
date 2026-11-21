# Testing creatives, reading results, fatigue

Budget, kill statistics and scaling are in the paid-traffic skill (`references/testing-and-scaling.md`). Symptom-by-symptom diagnosis (Step 0, trees, formulas with worked numbers) is in `diagnosis-playbook.md`; batch design, iteration ladder, weekly review and refresh calendar are in `playbooks.md`. The tables below are the short form.

## Metrics (define them identically in every report)
| Metric | Formula | Tells |
|---|---|---|
| Hook rate | 3-s plays ÷ impressions | do frame 0 and the first line stop the thumb? |
| Hold rate | ThruPlays (15 s or full video if shorter) ÷ 3-s plays | does the body keep those who stopped? |
| Outbound CTR | outbound clicks ÷ impressions | does it give a reason to leave the app? |
| Cost per visit | spend ÷ landing visits | traffic price |
| Page conversion | purchases (or leads) ÷ visits | do ad and page tell the same story? |
| CPA | spend ÷ purchases | cost of a customer |
| ROAS / revenue per visitor | whole-funnel revenue (front + bump + upsell) ÷ spend or ÷ visits | **decision** |
| Frequency | impressions ÷ people | fatigue signal |

"Hook rate" and "hold rate" are practitioner names built from official metrics (3-second plays, ThruPlay); write the formula in the report.

## Building the test
- **[C] Few, clearly different creatives per group** (3-5 on TikTok; "different enough" on Meta). New creatives join the existing group instead of opening a new one.
- **Budget sets batch size.** Each creative needs enough spend to show signal; practitioner kill rule: no purchase after ~1.5-2× target CPA (or the product price in low ticket) [F]. If the period's budget cannot cover that for N creatives, the batch has fewer than N.
- **One variable per round when the question is "why".** To find the angle, keep format and CTA; to find the format, keep the script. A first batch may mix concepts (the question is "which sells"); iterating a winner changes one thing.
- **[F] Attention is not sales.** In ~88k sales video ads on Meta (Jan-Jun 2026), mean hook rate 25.4% and mean ROAS 2.17; the category with the highest hook rate (28.8%) ranked 12th of 14 in ROAS. Vendor data without published method. [1-SRC]
- **Few purchases = noise.** 3 vs 5 purchases is no winner. Use top-funnel indicators for quick triage (kill what nobody stops for) and declare winners by purchases with volume, or by repeating in another week. Say "no volume to conclude" when true.
- **Vary before killing one that sold:** the same script in 2-3 formats (motion, hand with product, screen). Practitioner report: format changes results a lot for the same copy [F][1-SRC].

## Reading results
| Symptom | Likely cause | Change |
|---|---|---|
| Low hook rate | weak frame 0, small text, slow start | image and phrase of the first 2 s |
| High hook, low hold | bait the body does not pay; slow body | body; deliver the hook's promise earlier |
| High hold, low CTR | no reason to click; hidden CTA | CTA in voice and on screen; reason to go now |
| High CTR, low conversion | ad promises one thing, page shows another; wrong audience; exaggerated hook | align the page; lower the promise |
| All good, CPA rises with frequency | fatigue | below |
| Everything bad everywhere | offer, audience or page | not a creative problem |

**Minimum batch report:** concept line, spend, impressions, hook, hold, CTR, visits, purchases, CPA, revenue per visitor, decision (scale, iterate, kill) and the next round's hypothesis.

## Fatigue and refresh
- **[M] Repetition lowers response.** A platform analytics team's 2023 analysis is cited (second-hand) as ~45% lower conversion likelihood at the fourth exposure to the same creative; another reading says 60%. Direction only.
- **[C] Official signals:** Meta flags "creative limited"/"creative fatigue" when cost per result rises above history [search]; TikTok says refresh when delivery drops consistently or daily new users stay low, adding new creatives to the same group.
- **Practical signal:** frequency up, CTR down, cost per visit up, with page conversion stable. If page conversion also falls, the problem is elsewhere.
- **Refreshing is not remaking everything.** Cheapest first: new 3-s hook on the same body; same script in another format; same angle with other proof; new concept. Small audiences tire faster and need new concepts sooner.
- **[X] Magic thresholds** ("frequency above 2.5", "CTR down 20% in a week") come from vendor blogs. Watch your own history.
- **Creatives with an expiry** (price, deadline, holiday) carry the date in the file name and go offline that day. An ad with an expired deadline is false information.
- File naming and tracking: `{format}-{concept}-v{n}` (+ date if it expires); one ID per creative in the link's content parameter, equal to the file name.

## Myths
| Claim | Status |
|---|---|
| "Attention span is 8 seconds, less than a goldfish" | [X] no study behind it |
| "85% watch without sound" | [X] for Reels/TikTok; 2016 feed data |
| "Hook rate above 30% = good ad" | [X] attention is not sales |
| "UGC always beats produced ads" | [F] only vendor/agency blogs with inconsistent numbers |
| "Change the first line and you have 25 creatives" | [X] for the first batch; fine for iterating a winner |
| "More creatives is always better" | [F] depends on budget; volume without difference dilutes spend |
| "Following ABCD gives 30% more sales" | [M] 30% higher *predicted* short-term sales probability in a 2021 model, not measured sales |
| "Creative drives 49% of sales" | [M] consumer goods, 2017, repeated 2023 |
| "Video always beats image" | [F] images test cheaply and sometimes sell alone |
| "Urgency always converts" | [X] fake urgency is illegal in the EU and reads as a scam |
| "AI voice or person needs no disclosure" | [X] depends on platform and case; TikTok requires it for generated audio |
| "Free stock footage lets me show the person as a customer" | [X] a work licence is not an image release or endorsement |

## Experiment hygiene (Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments*, 2020) [M]
1. One primary metric and guardrails chosen before the batch; do not change the winner rule after seeing data.
2. Equal budgets and run windows within a test; same audience and placements; otherwise differences are noise or delivery bias.
3. A suspiciously large win gets a rerun before it is scaled (Twyman's law).
