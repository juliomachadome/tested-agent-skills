# Unit economics and lifecycle

Evidence tags: **[C]** consensus, **[M]** serious but single or practitioner, **[F]** rule of thumb or vendor. Ranges are starting points, not laws; the company's own cohorts replace them. Worked diagnosis (LTV:CAC fine but cash short, CAC rising) is in `diagnosis-playbook.md` trees 7 and 8. Pricing decisions: `skills/pricing`; media decisions: `skills/paid-traffic`.

## Definitions (write them next to every number)
- **CAC** = acquisition spend / new paying customers in the same period. Say which spend: media only, or loaded (media + sales + onboarding + tools + agency). Report both; decisions use loaded. Lag: spend of month M closes customers in M and M+1 for longer cycles; use cohort-matched CAC for those.
- **Gross margin** = (revenue - cost of serving: hosting, payments, support, third-party fees) / revenue. **Contribution margin per customer per month** = ARPA x gross margin - variable cost per customer not already in margin.
- **Monthly churn** c = customers lost in month / customers at start of month (logo churn); revenue churn and net revenue retention (NRR) also include expansion and contraction. Annual plans: use the renewal rate at renewal date, not monthly.
- **LTV** (subscription, constant churn) = ARPA x gross margin / c. It is a model; with few months of data it is an extrapolation. Cap the horizon (for example 3 to 5 years) and do not discount away real uncertainty; the honest alternative is **cumulative contribution per acquired customer at month 12, 24** from the cohort table **[M]**.
- **Payback (months)** simple = CAC / (ARPA x gross margin). Churn-adjusted: the month in which cumulative contribution per acquired customer, 40 x (1 - (1-c)^t) / c for a 40 contribution, reaches CAC. Example: CAC 600, contribution 40, churn 3%: simple 15, churn-adjusted 20 months, LTV ceiling 1,333, LTV:CAC 2.2.
- **Cohort economics**: the table of acquired customers per month x months since acquisition x cumulative contribution; compare with the CAC of the same month. Cut by channel and plan: a blended number hides the channel that loses money **[C]**.

## Sanity ranges (rules of thumb)
LTV:CAC near 3:1 or higher and payback inside about 12 months are common subscription targets **[F]**; low-ticket self-serve needs shorter payback, enterprise tolerates longer. The ratio ignores time: a 5:1 ratio with 30-month payback can still starve cash. Read ratio and payback together, and cumulative cash for the planned acquisition pace.

## Cash view
Cash needed for growth = acquisition spend of the month minus contribution of all active cohorts that month. Model 12 months ahead at the planned pace: for 100 customers a month, loaded CAC 1,950, contribution 105, churn 4.0%, the 12-month cumulative cash is about -1.63M; compare with cash in the bank and the plan to raise or slow down. Annual prepay changes cash timing, not unit economics.

## Cohort reading for LTV
Stable cohorts: monthly churn falls with age (early churn is higher); do not use month-1 churn for lifetime, nor the late-life churn of survivors for new customers. If curves flatten, use the plateau for survivors and the early drop for new signups, with both stated.

## Lifecycle triggers (behaviour, not calendar)
- Trigger the next message on the product milestone reached or missed, not on "day 3 for everyone"; stop the sequence when the milestone is hit.
- Define the lifecycle states once (new, activated, engaged, at risk, dormant, churned) from events with thresholds; count users per state weekly; track transitions, not just totals.
- At-risk signal: a drop of the core action below the user's own recent baseline, or no core action for a number of days set from the cohort data (for example the day by which 90% of retained users have returned **[F]**).
- Win-back and reactivation: measure on a holdout (do not message a random 10%); an uplift is the difference, not the clicks.
- A signup increase that lowers retention is a loss; keep churn, refunds and support load as guardrails. Message copy and design: `skills/copywriting`; onboarding flows: `skills/product-management`.

## Test integrity (short)
Fix sample size and duration beforehand, check SRM before reading results; see `playbooks.md` 3 and `experimentation-notes.md`.
