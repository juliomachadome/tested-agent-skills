# Sizing and willingness to pay

Tags: **[C]** consensus, **[M]** serious but single or old, **[F]** practitioner. Compute with python3 and show inputs.

## Bottom-up sizing
Top-down figures ("the market is 10 billion, we need 1 percent") are not estimates: nothing in them says how you reach one buyer **[C]**. Build from units.

1. **Universe** (TAM people): count of people or firms with the problem. Source and year: IBGE for people and households, firms by size or sector (IBGE, Receita Federal open data), Sebrae studies for small businesses, platform reports. Say "assumed" when you estimate.
2. **Fit filter** (SAM): share served by your format, language, price and channel.
3. **Reachable**: how many you can put the offer in front of in 12 months with your audience and budget.
4. **Conversion**: from reached to buyer (from your tests, not hope).
5. **Price and frequency**: price per purchase, purchases per customer per year (a course is often 1; a subscription 12; a consumable several).
6. **Net**: less refunds, platform fees and taxes.

SOM = reached x conversion x price x frequency x (1 - refunds) x (1 - fees). TAM and SAM in money = people x price x frequency, shown as the ceiling, never the forecast.

**Worked example** (assumed inputs, not data): niche course for bookkeepers who serve restaurants; universe 210,000 bookkeepers; fit 15 percent gives SAM = 31,500 people, SAM in money = 31,500 x R$ 297 = R$ 9,355,500 (one purchase each). SOM base: reach 20,000, conversion 1.5 percent = 300 buyers; gross 300 x 297 = R$ 89,100; refunds 5 percent and platform fees 10 percent (assumed) leave R$ 76,181. Low case (reach 10,000, conversion 0.8 percent): 80 buyers, R$ 20,315 net. High (30,000, 2.5 percent): 750 buyers, R$ 190,451 net. The result moves most with conversion and reach, so test those first; SAM only matters as a ceiling check (300 buyers is 0.95 percent of SAM).

Cross-check with traction: if the top three competitors show a few hundred reviews and steady ads, a SOM of several hundred buyers a year is plausible; if SOM exceeds the leader's visible traction, doubt the input.

## Willingness to pay methods
Strength order **[C]**: paid pre-sale > deposit > behavioural proxy (click on a price, reached checkout) > stated (Van Westendorp, Gabor-Granger, conjoint) > opinion. Stated methods bracket a range; they do not predict sales.

**Van Westendorp price sensitivity meter** **[M]** (1976). Four questions per respondent: too cheap (doubt quality), cheap or a bargain, getting expensive, too expensive. Plot cumulative curves; the crossings define a range of acceptable prices: the point of marginal cheapness and point of marginal expensiveness bracket the range; the optimal price point and indifference point mark the centre. Needs 100 or more respondents from the real segment; the method gives a range, not a demand curve or revenue; and it ignores competitors and cost. Check respondents' answers are ordered (too cheap below bargain below expensive below too expensive) and drop inconsistent rows, reporting how many.

**Gabor-Granger** **[M]**. Present price steps sequentially; share saying yes at each step gives a demand curve; multiply price by share for a revenue index and by margin for profit. Worked (assumed): prices 47, 67, 97, 147 with yes shares 52, 38, 24, 9 percent give revenue per 100 asked of 24.4, 25.5, 23.3, 13.2, so 67 maximises revenue index, 47 is within noise, and 147 collapses. Caveats: stated yes overstates (apply a haircut, test with a real pre-sale), order effects (randomise the start), anchoring.

**Conjoint** **[M]**. Respondents choose among product profiles that vary features and price; analysis estimates how much each feature is worth. Needs a designed set, several hundred responses and software; for a first test it is usually overkill. Use simple "which of two versions" choice questions instead, or a pre-sale with two versions.

**Behavioural tests (strongest)**: price page A/B at the same promise (volume allows only large differences), pre-sale at two prices to separate cold audiences, a deposit. See `playbooks.md` section 5. Price structure (anchors, tiers, guarantee): `offers`.

## Small samples and intervals
A rate from few trials is wide. Use the Wilson interval: with 5 buyers of 100 visitors the plausible rate is about 2.2 to 11.2 percent; with 15 of 300 (same 5 percent) about 3.1 to 8.1 percent. Do not compare two tests with 20 visitors each. Decision rules should be written as thresholds with the sample size they need.

## Sources
Trends: relative, sampled, 0-100, normalised by time and place (Google Trends help); good for shape and comparison, not volume. Population and firm counts: IBGE, Sebrae (Brazil); statistical offices elsewhere. Marketplaces: ranking is not revenue. Always record source, date and whether the page could be read.
