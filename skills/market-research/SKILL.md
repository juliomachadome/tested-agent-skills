---
name: market-research
description: Use before building or launching any product (ebook or PDF, course, kit, community, service, app, SaaS, physical product) to decide whether the opportunity is worth pursuing - "is there a market for", "is this idea worth it", "validate this product idea", "how big is the market", "who are my competitors", "will people pay for", "this video went viral, should I sell something", "research the market for". Frames who, problem and current alternative, reads demand signals honestly (search trends, communities, competitor traction, waitlists, pre-sales), sizes the market bottom-up, tears down competitors, tests willingness to pay, runs cheap ethical validation, and scores go, pivot or no-go. Brazil and global sources. Not for discovery interviews or PRDs (product-management), price structure or guarantees (offers), building the product, or running the ads (paid-traffic).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Market research and validation

Goal: decide, with the least money and time, whether to build, change or drop an idea, and say how sure you are. Tags: **[C]** consensus, **[M]** serious but single or correlational, **[F]** practitioner, **[X]** myth. Research that cannot change the decision is waste: write the decision and kill threshold first.

## 1. Start: project first, then the frame
Read the current project's docs first (audience, past launches, analytics, prices, legal notes). Then fix in five lines **[C]** (Osterwalder, Christensen):
1. **Who** exactly (a segment you can find, not "everyone").
2. **Problem and job** they are trying to get done, and the moment it hurts.
3. **Alternative today**, including doing nothing, a spreadsheet, a free video, a competitor, a hack.
4. **Switch trigger**: why would they pay now.
5. **Idea in one sentence** and how it would be delivered.

Missing data: ask for the minimum or mark the assumption as a hypothesis, never a finding.

Ask for: idea and target; raw evidence numbers; budget, deadline, kill threshold; own audience and channels; known competitors; country; any triggering viral post (links, views).

## 2. Step 0: is the evidence trustworthy
Classify each signal **[C]**: behaviour with a cost (paid, pre-ordered, booked a call, switched tool) beats stated intent (survey, "I would buy") beats attention (likes, views) beats praise (friends, family). Check denominators, the sample (your followers are not the market), the period (spike or trend) and who gains from the answer. Trees: `references/diagnosis-playbook.md`.

## 3. Demand signals and how to read them
| Signal | Strong when | Misleads when |
|---|---|---|
| Search interest (Google Trends, keyword tools) | Rising or stable over years, problem-worded queries | Trends is relative 0-100, not volume; short window, seasonality, news spike **[C]** |
| Communities, forums, groups, comments | Many detailed, repeated "how" asks and paid workarounds | One viral thread, your own audience, venting without spend |
| Competitor traction | Several sellers earning, steady reviews, ads running for months | Rank without sales data, paid reviews, legacy ranks |
| Waitlist | Opt-in with a cost (a qualifying question), later converted | Giveaway signups; waitlist-to-buyer is low, measure it |
| Pre-sale or deposit | Strangers paid, with refund promise | Friends paid, or heavy discount makes it a lottery ticket |
| "How did you do it" comments on viral content | Many comments ask for the method, tool or template (`viral-content`) | Curious commenters, not buyers; the wave decays in days |

Rule of thumb **[F]**: one behavioural signal from strangers outweighs ten weak ones.

## 4. Size the market bottom-up
Top-down ("1% of a 10 billion market") is a hope, not an estimate **[C]** (Aulet; Blank and Dorf). Use customers x price x frequency by segment, then TAM, SAM, SOM as filters **[C]**:
- **TAM**: everyone who has the problem and could buy this type of solution.
- **SAM**: those your format, language, price and channels can serve.
- **SOM**: what you can win in 12 months with your reach and conversion.

SOM = people you can reach x conversion x price x purchases per year, less refunds and fees. Show low, base and high cases and the input that moves the result most. Method and python check: `references/sizing-and-wtp.md`.

## 5. Competitor teardown
List 5-10 direct, indirect and "do nothing" alternatives. For each: offer, format, price and plans, promise, proof, audience, channels, review themes, traction, weakness. Mine reviews (1-3 stars for gaps, 5 stars for words customers use, "I wish" and "missing" for features) **[F]**. Competitor traction is evidence that demand exists; no competitor is not good news until you find why. Position on a gap customers pay to close. Template: `playbooks.md` section 2.

## 6. Willingness to pay (WTP)
Order of strength **[C]**: money paid (pre-sale) > deposit or card on file > behavioural proxy (price click, checkout reach) > stated WTP (Van Westendorp, Gabor-Granger) > "would you pay". Van Westendorp gives an acceptable range from four questions; Gabor-Granger gives a demand curve from price steps; conjoint trades off features and price (needs sample and design) **[M]**. Stated methods overstate; bracket a range, then test real prices (`sizing-and-wtp.md`, `playbooks.md` section 3). Price structure and guarantees: `offers`.

## 7. Cheap validation tests (ethical)
Pick the cheapest test that produces a behavioural signal:
1. **Landing page plus waitlist**: one honest promise, one qualifying question.
2. **Fake door** (a button for a feature that does not exist yet) only with disclosure on the next screen: it is not built yet, here is what happens, your data is used as stated. A hidden fake door that takes money is deceptive and illegal in many places.
3. **Concierge**: serve 3-10 paying customers by hand before software.
4. **Pre-sale** with a clear delivery date and refund promise (`playbooks.md` section 5).
5. **Smoke-test ads** to the page with a small fixed budget and a kill rule (`paid-traffic`).
6. **Mock-up shown to the segment**, asking for a commitment, not an opinion (interview craft: Mom Test in `product-management`).

The 48-hour sprint is in `playbooks.md` section 1. Write the threshold before you look at results (e.g. 30 waitlist signups from 500 visits, 5 pre-sales).

## 8. Decide: go, pivot, no-go
Score 0-5 each, weights in `playbooks.md` section 4 (default: demand 20, willingness to pay 20, reachability 15, competition and differentiation 10, effort and cost 10, window and timing 10, risk and compliance 5, founder fit 10). Any 0 on demand, willingness to pay or reachability is a no-go or pivot whatever the total. Below 55 no-go, 55-70 pivot or test more, above 70 go small. Output: decision, total, what moved it, next test, what is unverified. Under about 100 responses or 30 buyers, call it directional.

## 9. Timing windows
A viral wave loses most demand in days or weeks, so only fast formats fit (template, checklist, short guide, pre-sale, concierge) **[F]**. Judge the shape: spike (days), season (annual), growth (years), decline. A 2-week window means a pre-sale this week. See `viral-content`.

## 10. Brazil and global sources
Brazil: Google Trends BR (country, period, category), IBGE (population, firms, PNAD), Sebrae (small-business studies, MEI), marketplaces Hotmart, Kiwify, Mercado Livre (rank, price, reviews as demand evidence, rank is not sales), Reclame Aqui for pain, Receita Federal open data for firm counts. Global: Trends worldwide, statistical offices, app-store charts, community threads, trade bodies. Cite source and year for each figure.

## 11. Ethics and law
No deception: fake doors disclose, ads promise what exists, pre-sales state the delivery date and refund. Surveys and waitlists need a clear purpose, minimal data, consent where required and an exit; scraping personal data or messaging strangers needs a lawful basis. Consumer law on refunds applies to pre-sales (`offers`).

## AI tells to avoid (check while answering, not after)
- Generic advice that would fit any business, instead of the user's own numbers.
- Benchmarks or market sizes stated as fact, with no source.
- Round-number assumptions with no source or range.
- Frameworks named (SWOT, Canvas, Van Westendorp) but not applied to the case.
- "It depends" without saying on what and what to do.
- Long option lists with no recommendation.
- Confident tone on unverified fees, laws or rates.
Fix: use the user's data, show the arithmetic, give a range and the assumption, then one recommendation with its reason and the next check. Say what you chose and why in one line; a choice without a reason is removed.

## 12. Which reference to open
- Misleading signals, "nobody pays", waitlist not converting, "no search volume", competitor exists, interest fades: `references/diagnosis-playbook.md`
- 48-hour sprint, competitor template, WTP survey, scorecard, pre-sale plan: `references/playbooks.md`
- Bottom-up sizing, TAM/SAM/SOM, Van Westendorp, Gabor-Granger, conjoint, small samples: `references/sizing-and-wtp.md`
- Sources and status: `references/BIBLIOGRAPHY.md`

## 13. Boundaries
Interviews and PRDs: `product-management`. Price, bumps, guarantees and SaaS tiers: `offers`. Viral waves: `viral-content`. Ads and budgets: `paid-traffic`. Metrics and tests: `growth-analytics`. Page words: `copywriting`. Format and build mode: `product-creation` if present, else product-management and offers.
