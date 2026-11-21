# Playbooks: routines for growth analytics

Evidence tags: **[C]** consensus or law, **[M]** serious but single or correlational, **[F]** practitioner or vendor, **[X]** myth. Ideas are applied, never copied. Diagnosis (something looks wrong) lives in `diagnosis-playbook.md`; unit economics in `unit-economics-lifecycle.md`. Media buying is `skills/paid-traffic`; discovery and roadmap are `skills/product-management`; legal depth is the privacy law of the data subject's country (official regulator pages).

## 1. North Star and input metrics tree
1. Write the customer value in one sentence ("a team finishes a report without help"). The North Star counts that value delivered per period (for example weekly teams that finished a report), not visits or signups **[F]**.
2. Test it: reflects value not activity; the team can move it; it leads revenue (check the lag with cohorts); it is hard to game; one definition with a query.
3. Split into 3-5 inputs, usually breadth (how many users reach it), depth (how much each does), frequency, efficiency (time or cost to get there). Each input has an owner, a definition, a weekly number and a lever.
4. Attach a guardrail to each (refund rate, support contacts per 100 users, latency, churn) so a gain cannot be bought by harm.
5. Keep to one page; review at stage change (Lean Analytics suggests one metric that matters per stage **[M]**).
6. Find activation from data: compare early actions of retained vs churned users, pick the action with the largest separation, then confirm with interviews. Correlation is a hypothesis; test it with an experiment before building the product around it **[M]**.
Output: tree table (metric, definition, period, owner, lever, guardrail, decision it serves).

## 2. Tracking plan
Fields per event: name, trigger (exact user or system action), properties (name, type, allowed values, example), where fired (client or server), PII flag, consent category, owner, decision served, status, version.
- **Naming**: object_action, snake_case, past tense (`invoice_paid`); no UI wording (`button_click` carries no meaning); the same property name means the same thing in every event; booleans as `is_` or `has_`; enums over free text; few events, rich properties **[F]**.
- **Properties**: typed, with allowed values; currency as code plus amount in minor units; no free text; no emails, names or precise location; ids that are opaque.
- **Identity**: anonymous id at first visit; user id on login; alias once; never reuse ids; define behaviour on logout and shared devices; define the unit of analysis (user, account, workspace); write merge rules and the cookie lifetime; keep an account id on every B2B event.
- **Server vs client**: money, subscription state, signup commit, and anything the business must reconcile: server-side from the database transaction (immune to ad blockers and double fire). UI interactions and exposure to experiments: client, with the consent rule. A server event still needs a lawful basis; server-side is not a way around consent **[C]**.
- **Consent mode**: in Google's model each storage type (analytics, ad storage, ad user data, ad personalisation) has a default and an update state set by the banner; the tag adapts what it sends, and the tool does not remember choices for you **[M]**. Decide, per tool, what happens when denied (no cookies, cookieless pings, modelled data) and tag it in the plan.
- **Event limits**: check the tool's limits for events, parameters and batch size before designing (GA4 documents batching and size limits **[M]**).
- **QA**: (1) schema validation in CI that fails on unknown or mistyped properties; (2) a staging run through each flow with a debug view; (3) a reconcile: analytics purchases vs database orders for 7 days (target within 2-5%, with consent effect explained); (4) volume alert when an event falls below a floor or changes more than a set share day over day; (5) dated changelog and a deprecation window; (6) a test account excluded from data.
Template: `tracking-plan.md`.

## 3. Experiment design doc and pre-registration
Write before launch, freeze, store with the result:
1. **Problem and hypothesis**: "Because X (evidence), changing Y for segment Z will move metric M by at least delta."
2. **Unit and population**: randomisation unit (user, account; session only for session metrics), eligibility, exclusions, exposure point (assign at the moment of exposure to avoid diluted populations).
3. **Metrics**: one primary (a business or leading metric the change targets); guardrails with thresholds; diagnostic metrics labelled exploratory.
4. **MDE and sample size**: smallest effect worth shipping; compute n per arm (formula in `diagnosis-playbook.md`), traffic per day, duration rounded to whole weeks (min 1 full week, often 2 to cover weekly cycles) **[C]**.
5. **Stopping rule**: fixed horizon (read once at the planned n); or a sequential design with a valid boundary if looking early is needed. Peeking at a fixed-horizon test without correction inflates false positives **[C]**. Early stops allowed only for guardrail harm.
6. **Variance reduction (option)**: CUPED adjusts the metric with pre-experiment data and can cut variance by a factor of about (1 - rho^2) for pre/post correlation rho (rho 0.5 cuts it 25%, rho 0.7 cuts 51%) **[M]**; needs a pre-period per user; useless for new users without history.
7. **Sequential testing (option)**: always-valid or group-sequential methods; accept less power for the right to look **[M]**.
8. **Multiple comparisons**: more variants or metrics raise false positives (5 independent metrics at 5% give a 23% chance of at least one false alarm); name the primary, correct or label the rest.
9. **Decision rule**: ship if the primary improves with the interval above zero (or above the break-even), no guardrail breached, no segment-only effect; iterate if neutral with a learning; revert otherwise. Write the rule before.
10. **Analysis checklist**: SRM first; A/A or pre-period balance; exposure logging; bot and internal filter; whole weeks; effect as a difference with its interval and relative lift; guardrails; novelty by days since exposure; segment cuts as hypotheses; outliers (winsorise by rule, set in advance); interactions with other live tests.
11. **Twyman's law**: a result that looks too good (a 40% lift on a mature page) is more likely a bug than a discovery; investigate before celebrating **[M]**.
12. **Record**: store the doc, the data cut, the readout and the decision, including nulls.
Low traffic: larger changes, pre/post with a matched control, qualitative tests, or decide on a reversible bet and say it is one.

## 4. Weekly metrics review (30 minutes)
1. Data health first (5 min): event volumes, reconcile vs database, any tracking or consent change, any holiday or outage.
2. North Star and inputs (10 min): this week vs last 4 weeks and vs same week last year, with the definition printed; cohort row for the newest completed week.
3. Funnel and channel (5 min): the step with the largest absolute loss; CAC and payback by channel.
4. Experiments (5 min): running (days, planned n, SRM), finished (decision), next.
5. Decisions (5 min): at most 3 actions, each with owner, metric, date.
Rules: no reading of partial weeks; no reasons given for a move inside noise (use the interval or the historical range); every chart has period and definition; keep a log of changes.

## 5. Cohort and funnel recipe (SQL sketches)
Cohort retention (weekly), warehouse with `users(user_id, signup_at)` and `events(user_id, event_name, ts)`:
```sql
WITH c AS (
  SELECT user_id, date_trunc('week', signup_at) AS cohort_week FROM users),
r AS (
  SELECT c.cohort_week,
         floor(extract(epoch FROM (date_trunc('week', e.ts) - c.cohort_week)) / 604800) AS week_n,
         count(DISTINCT e.user_id) AS active
  FROM c JOIN events e ON e.user_id = c.user_id AND e.event_name = 'core_action_done' AND e.ts >= c.cohort_week
  GROUP BY 1, 2)
SELECT r.cohort_week, r.week_n, r.active, s.size, r.active::numeric / s.size AS retention
FROM r JOIN (SELECT cohort_week, count(*) AS size FROM c GROUP BY 1) s USING (cohort_week)
ORDER BY 1, 2;
```
Funnel with a window (step B within 7 days after step A): take the first A per user, left join the first B after A inside the window, count per step; report step rate, cumulative rate, median time between steps. Always: define the denominator (users who reached the previous step), one timezone, exclude test and internal users, keep the cohort in the output so the table can be re-cut by channel and plan. Hide cells with fewer than about 30 users or show the interval.

## 6. Reading attribution
| Lens | What it tells | Limits |
|---|---|---|
| Platform report (ad networks) | what that platform claims within its click and view windows | self-attribution; overlap between platforms; modelled conversions; changes of defaults |
| Web analytics last-click or data-driven | which touch preceded the visit | loses consent-denied and blocked traffic; direct bucket grows when UTM is lost |
| Self-reported ("how did you hear") | the memory of the buyer, good for dark social and word of mouth | biased, coarse; still useful beside the others |
| Incrementality / holdout test | causal lift: withhold ads (user holdout, or geo experiment with matched regions) and compare outcomes | needs spend and volume; one channel at a time; wide intervals; design with pre-registration as in section 3 |
| Media-mix model (MMM) | channel contribution and saturation from aggregate time series, no user ids | needs 2+ years of weekly data with spend variation; priors drive results; check against experiments; open-source tools exist (Google Meridian, Meta Robyn) **[M]** |
Method: compute the overlap ratio (sum of platform claims / database orders); sort channels by marginal not average return; calibrate platform claims with at least one holdout per major channel per year if spend allows; report a range and the method. Never claim causation from a before/after on a mixed-change week. Spend actions: `skills/paid-traffic`.

## 7. Consent and privacy checks for analytics
Not legal advice; pass doubts to the owner or counsel. Law depth: the privacy law of the data subject's country (official regulator pages).
1. **Inventory**: every tool, cookie, SDK, pixel and server-side forwarder; what each stores or reads on the device, what personal data it receives, the processor, the transfer destination.
2. **Rule for devices (EU)**: storing or reading information on the user's device needs prior information and an opportunity to refuse, except where strictly necessary for a service the user asked for (ePrivacy Directive art. 5(3)) **[C]**. Analytics is not automatically "strictly necessary"; some regulators exempt strictly limited audience measurement under conditions (for example the French regulator: statistics only for the publisher, anonymous output, no cross-site tracking, limited lifetime and retention). Check the local authority's current text **[C]**.
3. **Consent quality**: affirmative act, not pre-ticked, not bundled, not obtained by scrolling, and withdrawal as easy as giving it (GDPR recitals 32, 42, 43 and the EDPB consent guidelines **[C]**). A banner that makes "reject" harder than "accept" is a risk and also distorts the data.
4. **Personal data**: online identifiers can be personal data: GDPR names them, and LGPD art. 5 I covers information about an identified or identifiable person, so an identifier that singles someone out can qualify; each purpose needs a basis (LGPD art. 7: ten bases, consent among them; art. 8: consent in writing or another provable way, specific purposes, burden of proof on the controller, revocable at any time, free and easy; art. 10: legitimate interest only for strictly necessary data, with transparency) **[C]**; minimise; no personal data in event properties; retention limit; IP truncation; access and deletion requests reach the analytics store.
5. **Server-side is not a bypass**: moving the tag changes where it runs, not whether consent applies **[C]**.
6. **Consent state in the data**: log the consent state per event (or per session) so analysis can compare bases; test that nothing fires before the choice; QA after every banner or tag-manager release.
7. **Report the effect**: when the acceptance rate changes, show it next to the metrics it affects (Step 0 in `diagnosis-playbook.md`).
8. **Other regimes**: UK GDPR and PECR, California (CCPA/CPRA opt-out of sale or sharing), LGPD (ANPD guidance): note which apply to the audience; ANPD guidance not read; the LGPD text was read (see `BIBLIOGRAPHY.md`).
