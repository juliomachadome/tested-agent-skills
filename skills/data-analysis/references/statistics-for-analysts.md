# Statistics for analysts

What to use when, with the formula and one worked example each. Numbers computed with python3; t critical values come from a standard table. Numbers in brackets point to `BIBLIOGRAPHY.md`. Evidence: **[C]** consensus, **[M]** serious but single or older, **[F]** rule of thumb. This is working-analyst statistics, not a replacement for a textbook [9, 10, 14]. Controlled experiments (A/B tests, sample size, peeking, SRM) belong to growth-analytics.

## What to use when
| Question | Use | Watch for |
|---|---|---|
| What is typical? | median, mean, trimmed mean, with n | skew, outliers, mixed populations |
| How spread? | IQR, standard deviation, percentiles | method of percentile; heavy tails |
| What does the distribution look like? | histogram, ECDF, box plot | one summary number hides shape [25] |
| Rate or share with uncertainty? | Wilson interval | small n, p near 0 or 1 [31] |
| Mean with uncertainty? | t interval | skewed data, n < 30 |
| Difference between two groups? | interval of the difference, effect size | overlapping intervals, multiple looks |
| Are two variables related? | scatter, correlation, regression | outliers, nonlinearity, confounding [25, 14] |
| Did X cause Y? | a design (experiment, natural experiment) and causal reasoning | correlation alone [12] |
| Many cuts? | count comparisons; Bonferroni or Benjamini-Hochberg | forking paths [22, 32] |
| Seasonal series? | compare same period; seasonal naive baseline | calendar shifts [11] |

## 1. Describe first
Report n, number missing, minimum, median, mean, maximum, quartiles, and a histogram [15]. Mean and median differ when data is skewed: 95 orders of 20 and 5 of 2,000 have mean 119 and median 20, standard deviation 431.5; the top 5% of orders carry 84% of revenue. Say which statistic answers the question (typical customer: median; revenue planning: mean and total). Spread rules: IQR = Q3 - Q1; the 1.5 x IQR fences flag candidates for review, not deletions. Example: 12, 14, 15, 15, 16, 17, 18, 19, 21, 95 gives Q1 15, Q3 18.75, IQR 3.75, fences 9.4 and 24.4: 95 is flagged; check it against the source before deciding [15, 29].

Plot before you model. Anscombe's four data sets share mean of y (7.50), correlation (about 0.816) and the fitted line (slope 0.50) yet look completely different; set I and II were recomputed here: means 7.50 and 7.50, r 0.816 and 0.816, slope 0.50 and 0.50 [25].

## 2. Confidence interval of a mean
Formula: mean +/- t(0.975, n-1) x s / sqrt(n).
Example: n = 20, mean 52.0, s = 12.0. Standard error = 12 / sqrt(20) = 2.683; t(0.975, 19) = 2.093; half-width = 5.62; interval 46.4 to 57.6. With skewed data and small n, bootstrap the mean or report the median with a bootstrap interval; do not trust a normal interval on 8 customer orders with one whale. An interval says how precisely the sample estimates the population mean, not where individual values lie (individual values spread by about s: roughly 28 to 76 for 95% of them if they are near normal).

## 3. Confidence interval of a proportion
Do not use the plain Wald formula p +/- 1.96 x sqrt(p(1-p)/n) when n is small or p is near 0 or 1; its coverage is erratic [31]. Use the Wilson interval:
centre = (p + z^2/(2n)) / (1 + z^2/n); half-width = z x sqrt(p(1-p)/n + z^2/(4n^2)) / (1 + z^2/n), z = 1.96.
Example 1: 18 of 200 (p = 9.0%): Wilson 5.8% to 13.8% (Wald 5.0% to 13.0%).
Example 2: 3 of 10: Wilson 10.8% to 60.3% (Wald 1.6% to 58.4%); 2 of 10: 5.7% to 51.0%. The intervals overlap on most of their range, so 30% vs 20% is not evidence of a difference.
Sample size for a margin E at 95%: n = 1.96^2 x p(1-p) / E^2; worst case p = 0.5 and E = 5 points gives 384.2, so 385 responses (simple random sample) [16].

## 4. Difference between two groups
For two proportions: difference d = p1 - p2, standard error sqrt(p1(1-p1)/n1 + p2(1-p2)/n2), interval d +/- 1.96 x SE (adequate when counts are not tiny; otherwise use an exact or Wilson-type method).
Example: new region 9 of 60 (15.0%), old regions 120 of 1,000 (12.0%): d = +3.0 points, SE about 4.7 points, interval -6.3 to +12.3. The data is compatible with a worse, equal or better region; the honest sentence is "no detectable difference at this n". Report the interval and the n, not "up 25%" [23, 24].
Practical vs statistical: a tiny effect is "significant" with enough n; a big effect with n = 10 is not. Decide in advance the smallest difference that would change the decision.

## 5. Correlation and regression basics
Pearson r = cov(x, y) / (sd_x x sd_y); slope = cov(x, y) / var(x); intercept = mean(y) - slope x mean(x); R^2 = r^2 for one predictor.
Example: x = 1..8, y = 2, 3, 3, 5, 6, 8, 7, 10 gives r = 0.966, slope 1.095, intercept 0.571, R^2 = 0.933: each extra unit of x goes with about 1.1 more y, in this sample. Check residuals against x; extrapolating beyond 8 is a guess. A single high-leverage point can create or erase a correlation; refit without it and show both [14, 25].
Regression with several predictors answers "difference in y associated with x holding the others fixed, if the model is right"; it is a description unless the design supports a causal reading [14].

## 6. Correlation is not causation; confounding; Simpson
Name the three explanations before claiming cause: X causes Y, Y causes X, a third factor Z drives both (or selection into the data). To test cause you need a design: randomisation, or a credible natural experiment, or a causal model whose assumptions are stated [12, 42].
Simpson's reversal: an association in aggregate reverses within groups when group mix differs and group affects the outcome. Worked case in `diagnosis-playbook.md` Tree 5: New region beats Old in both segments (11% vs 10% and 46% vs 45%) yet is 19.75% vs 38.0% overall because 75% of its trials are SMB; the classic admissions study found a pooled bias against women that disappeared inside departments [21]. Rule: when a comparison matters, compare within segments or standardise to a common mix, and say which question each answers [42].
Ecological fallacy: group-level correlations need not hold for individuals [43].

## 7. Bias in who is in the data
- **Survivorship**: only survivors appear. Wald's analysis of returning aircraft asked where the missing planes were hit [41].
- **Selection and non-response**: the responders differ from the population; weights fix known imbalance only. Example: 80% young / 20% old sample, satisfaction 70% and 40%: raw 64%, population-weighted (50/50) 55% [16].
- **Regression to the mean**: groups chosen for an extreme first measurement drift back without any intervention; a "fix" applied to the worst stores will seem to work [37].
- **Look-ahead and leakage** in forecasts: never use information that was not available at the forecast date.

## 8. Many comparisons and forking paths
With m independent tests at level 0.05 the chance of at least one false positive is 1 - 0.95^m: 64.2% for m = 20. Flexible analysis choices (which subgroups, which exclusions, which outcome) create many implicit comparisons even when you ran "one test" [22].
- Bonferroni: use 0.05 / m (0.0025 for 20); conservative.
- Benjamini-Hochberg controls the false discovery rate: sort p-values p(1) <= ... <= p(m); reject all up to the largest k with p(k) <= 0.05 x k / m [32]. Example m = 6, p = 0.001, 0.008, 0.012, 0.04, 0.2, 0.5: thresholds 0.0083, 0.0167, 0.025, 0.0333, 0.0417, 0.05; k = 3 is the largest passing, so the first three are called discoveries.
- Under small samples, many tested relationships and flexible analysis, a large share of claimed findings can be false, and low power lowers the share of significant results that are true; significant small-n results also tend to overstate the effect [24, 36]. Treat exploratory cuts as hypotheses to confirm on new data.
- A p-value is not the probability that the hypothesis is true, nor an effect size; a large p-value is not proof of no effect [23].

## 9. Small n
Below roughly 30 observations per group, or fewer than about 10 events in the smaller cell, intervals are wide and normal approximations fail. Do this: show counts, not only percentages; give the Wilson or exact interval; state the n needed (for a 1-point gap around 45% about 38,800 per group at 80% power, 5% two-sided: 2 x (1.96 + 0.84)^2 x 0.45 x 0.55 / 0.01^2); say "cannot conclude"; decide what data to collect next; avoid ranking 12 regions by a rate that rests on 3 to 15 orders each [36].

## 10. Seasonality and comparisons over time
- Compare like with like: same weekday, same month last year (YoY), same weekday last week (WoW), aligned for holidays and the number of trading days. 100 to 118 is +18% YoY; a month with five Saturdays against one with four is not growth [11].
- Percent changes on small bases mislead: +300% from 2 to 8.
- Compounding: 5% a month is 79.6% a year (1.05^12 - 1), not 60%.
- Decomposition (trend, seasonal, remainder) is a way to look at a series; do it before modelling [11].
- A moving average smooths; it also lags and drops the ends.

## 11. Forecasting basics
Baselines first, on a holdout that comes after the training period [11]:
- Naive: next = last value. Seasonal naive: next = the value one season ago. Mean: average of history.
- Errors: MAE = mean(|e|); RMSE penalises big misses; MAPE fails near zero and is asymmetric; MASE scales MAE by the in-sample naive (or seasonal-naive) MAE and is scale-free [11, 33].
Example: two training weeks (100, 120, 130, 125, 140, 200, 180 and 104, 118, 135, 128, 150, 190, 176) then a test week 102, 121, 133, 124, 146, 198, 181. Seasonal naive (repeat the last week) MAE 4.0; naive 40.1; mean 26.8. Scale (in-sample seasonal naive MAE) 5.43, so MASE 0.74. A candidate model with MAE 2.71 has MASE 0.50 and earns its complexity; one with MAE 6 would not. Give a range from past errors (for example the 80th percentile of absolute holdout error) rather than a single number; say what would break it. Model building and tuning are out of scope.

## 12. Choosing between a quick answer and an experiment
Call growth-analytics when the question is causal and you can intervene (sample size, randomisation, stopping rules, guardrails, SRM), for funnels, activation, retention curves and attribution. Stay here when the question is descriptive (what happened, where, how big, how sure), when the data are already collected, or when a reconciliation or definition is in dispute. When in doubt, answer the descriptive part with its interval and name the experiment that would answer the causal part.

## 11. Randomness, base rates and fat tails (Mlodinow, Taleb)
Ideas restated from *The Drunkard's Walk* (prologue, ch. 6, 9) and *The Black Swan* (ch. 3, 6, 8, 14); status in `BIBLIOGRAPHY.md`.
- **Base rates and false positives (Mlodinow ch. 6) [C].** P(positive | no problem) is not P(no problem | positive). Worked case: 10,000 users, 1% will churn (100); a model catches 90% of them (90) and wrongly flags 5% of the 9,900 others (495). Precision is 90 / 585 = 15.4%, so 5 of 6 alerts are wrong although the model "is 95% specific". Report precision next to recall and the prevalence, and compare with a model that always predicts the base rate. The same slip is the prosecutor's fallacy: reading a p-value as the chance the null is true (section 8).
- **Streaks and "hot hands" (ch. 9) [C].** A long run looks improbable only if you name the person or campaign before looking. Over many candidates and many start dates it is likely: the book works a fund manager's 15-year winning streak, which is about 1 in 32,768 for one pre-named manager, but about 3% for any of 1,000 managers starting one given year and far higher over 40 years and thousands of funds (the book's figure for a 12-year streak is about 75%; assumptions are the author's). Before crowning a "best store, best ad, best week", count the field (m candidates x k windows) and simulate shuffled data: the longest run of heads in 100 fair flips is typically 6-7. Caveat [M, from memory, not re-fetched]: the 1985 basketball study that found no hot hand was later shown to use a biased test, and a small real effect is plausible; "streaks are pure luck" is a default to test, not a law.
- **Regression to the mean, worked case (prologue) [C].** Flight instructors saw praise followed by worse landings and shouting by better ones; both were just return to normal skill after an extreme attempt. Whenever you act on the worst (or best) units, keep a comparable untreated group of equally extreme units, or re-measure first (section 7).
- **Narrative fallacy (Taleb ch. 6) [M].** People supply reasons for any sequence, even for identical items they were asked to choose between, and the story raises confidence, not accuracy. In a write-up, label the explanation as a hypothesis, list one or two rival explanations including noise, and state what result would refute it. Do not put a cause in a dashboard headline unless a design supports it.
- **Silent evidence (ch. 8) [C].** The record shows survivors: the drowned worshippers do not hang portraits in the temple. Ask for the missing group in every cohort (churned users with no later events, failed campaigns not in the report, users who never logged in) before drawing a lesson from winners (section 7).
- **Fat tails (ch. 3, 14) [M].** Where one observation can dominate the total (revenue per customer, session length, claim size, citations, winner-take-all markets with cumulative advantage), the sample mean keeps jumping, standard deviation says little, and a normal interval is wrong. Checks: share of the total from the top 1% and 10%; mean versus median; the mean recomputed on growing samples (does it settle?); how the maximum grows with n. Report medians, top shares and bootstrap intervals, and never trim the large values away when they are the business.
- **Criticism of Taleb [M].** He is polemical and the book is mostly argument and anecdote, not a tested method. Many ordinary problems (means of moderately skewed data with large n) are fine under the central limit theorem; "black swan" is hard to define except after the fact; and his rule that tails cannot be estimated is itself hard to apply to everyday forecasts. Use the book as a prompt to check tail behaviour, not as proof that all statistics fail.
