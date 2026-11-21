# Experimentation notes (quick reference)

Full routine: `playbooks.md` 3. Diagnosis of a failed or suspicious test: `diagnosis-playbook.md` trees 4 and 5. Evidence tags: **[C]** consensus, **[M]** serious but single or practitioner, **[F]** rule of thumb.

- **Sample size per arm** (conversion, two-sided alpha 0.05, power 0.8): n = (1.96 x sqrt(2 p-bar (1-p-bar)) + 0.84 x sqrt(p1(1-p1) + p2(1-p2)))^2 / delta^2. Example: 4% to 5% gives 6,745 per arm. Shortcut 15.7 x p(1-p) / delta^2 gives 6,029 and slightly underestimates. For a continuous metric: n about 15.7 x sigma^2 / delta^2.
- **Peeking**: repeated looks at a fixed-horizon test inflate false positives (an essay demonstrates about 26% at a nominal 5% under continuous peeking **[M]**). Use a fixed horizon, or a valid sequential method chosen in advance.
- **SRM**: chi-square of observed vs designed split; alarm at p < 0.001 **[C]**; if triggered, do not read the metrics; find the cause by stage and restart.
- **Duration**: whole weeks; at least one, usually two; watch novelty by days since exposure.
- **CUPED** (pre-experiment covariate adjustment) reduces variance by about 1 - rho^2; needs history per user **[M]**.
- **Multiple comparisons**: one primary metric; apply a correction or label the rest exploratory. With 5 independent metrics the chance of one false alarm at 5% each is 23%.
- **Low traffic**: bigger swings, qualitative tests, pre/post with a matched control and caveats, a Bayesian reading with explicit priors (state them).
- **Ship criteria**: primary improved (interval above the break-even) or neutral with a strategic reason; no guardrail harmed; not driven by one segment or outlier; a post-launch holdout confirms.
- **Winner's curse**: the observed lift of the best of many variants is biased upward; expect the real effect to be smaller **[C]**.
- **Vendor engines** differ (frequentist, Bayesian, sequential); read the method before trusting a "winner" badge **[F]**.
- **Twyman's law**: too good to be true usually is.
- **Interaction**: overlapping tests on one surface can interact; run them in separate layers or check.
- **Legal and consumer-protection texts** are not tested for conversion at the expense of clarity.
