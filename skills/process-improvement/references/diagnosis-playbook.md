# Diagnosis playbook: process improvement and business case

Evidence tags: **[C]** definition or identity, **[M]** serious practitioner or single study, **[F]** rule of thumb, **[X]** myth. Currency is generic (units of money); country, tax and accounting rules are the company's.

> **Illustrative examples only.** The worked cases in this file are fictional, de-identified teaching scenarios with synthetic figures. They do not describe L'Oréal, a customer, or any named company; replace every input with the organization's own evidence before using it in a decision.

## Step 0: is the evidence trustworthy?
Before any analysis or promise, check:
1. **Where does the baseline come from?** A system export, a time study, or a person's memory. Memory is an assumption: mark it, sample 20 to 30 real cases, and compare. [M] Averages hide the tail: ask for the median and the 90th percentile of lead time.
2. **Same definitions?** "Lead time" from order or from approval, "defect" as a rejected item or a reworked one, "hour" loaded or direct. Two reports that disagree usually use two definitions.
3. **A normal period?** Not a month with a launch, a holiday or a system outage. Use at least 3 months or a full cycle (month-end, season).
4. **Who owns the process and agrees with the baseline?** If the process owner disputes the number, the project dies in the meeting. Walk the process (gemba) before drawing it.
5. **Rate per hour**: ask finance for the loaded cost per role (salary, charges, overhead as the company counts it). Never invent one.
Any answer of "not known" turns the number into an assumption and adds a low case.

## Symptom trees

### A. "The business case was rejected or sent back"
| Likely cause | How to check | Fix |
|---|---|---|
| Savings are hours x rate, no cash | Ask: which cost line in the budget falls? | Split hard (overtime, contractor, avoided hire, sold capacity) from soft; count only hard in the break-even |
| Break-even uses simple payback | Does the model have a ramp-up and month-1 running cost? | Build the cumulative cash curve (worked example below) |
| One scenario | Is there a low case? | Add gain at 70 percent and the adoption level that makes it fail |
| Gain assumed from day one | Ask when the first benefit lands | Add a ramp (for example 0, 50, 100 percent) |
| Cost left out (support, licences, retraining, maintenance) | Ask who runs it in year 2 | Add running cost per month and an upkeep line |
| The sponsor owns a different goal | Read the charter goal against their targets | Reframe: the same project in their metric (cost, revenue, risk, service) |
| No owner after approval | Who signs the A3? | Name one owner with a date |

### B. "The savings never showed up"
1. Compare the planned cost line with the actual line, month by month; same definitions as in Step 0.
2. Hours were saved but the team was not reduced or redeployed: the gain is capacity, not money [M]. Decide: sell the capacity, avoid a hire, or accept it as a service gain and say so.
3. Adoption: how many cases use the new process? Gain = (cases on the new process) x (unit effect). A low adoption explains most gaps.
4. A side effect moved the cost elsewhere (rework downstream, support calls). Check the next step in the value stream.
5. Measurement changed (new definition after go-live). Re-baseline with the old definition.

### C. "The VSM looks perfect"
It is the designed process, not the real one. Walk the flow with the people who do it, time real cases, and add the hidden loops: rework, "waiting for information", approvals sent back. Typical result: process time is a small share of lead time [M]. If value-added share is above 50 percent in an office process, suspect the map.

### D. "We saved hours, where is the cash?"
Worked case (AI-drafted support replies): 9,000 tickets a month, 2 minutes saved per ticket, loaded cost 22 per hour. Hours saved 300 a month; "value" 6,600. Running cost: licence 2,500 plus 40 hours of quality checks at 22 = 880, so 3,380 a month. If every saved hour became cash: net 3,220 a month. If only 25 percent of the hours avoid overtime or a contractor (75 hours, 1,650): net minus 1,730 a month, so the project loses money unless the capacity is sold or a hire avoided. The decision is about what happens to the 300 hours, not the tool. Do not invent the 25 percent: compute the threshold. Running cost 3,380 covers only if 3,380 / 22 = 154 hours (51 percent of the 300) become cash; to pay back the 18,000 setup in 12 months the net must be 1,500 a month, so (3,380 + 1,500) / 22 = 222 hours (74 percent). Deliver the requested headline first (all hours as cash: net 3,220 a month, payback 18,000 / 3,220 = 5.6 months before any ramp), say it is the upper bound, then give these two thresholds and ask who will confirm that share.

### E. "The gain faded after three months" (Control failed)
Check: standard work written and trained; an owner; a metric on a visible chart with a trigger; new hires trained on the new way; the old system or shortcut closed. A run chart with the baseline and the target line shows the drift. Without a response plan a chart is decoration.

### F. "The root cause is 'human error' or 'lack of training'"
[C] That is where the analysis stopped, not a cause. Ask why the system allowed it: unclear step, missing check, overload, bad input, a tool that makes the wrong thing easy. Fix the process (error-proofing, poka-yoke) before retraining.

### G. "The team wants a fix, the data say another"
Stratify before arguing (by product, shift, site, channel, customer type). A Pareto of causes usually shows two or three that explain most of the loss [F: the 80/20 shape is common, not a law]. Work the biggest bar first.

### H. "Everything is a bottleneck"
Find the constraint: the step with the longest queue and the fewest spare capacity. An hour saved at a non-constraint does not raise output (Goldratt, The Goal [M]). Improve the constraint, then look again.

## Worked number: near-expiry stock (the cumulative curve)
Setting: 4,000 units a month approach the sell-by limit and are scrapped. Unit cost 12. Project: sell 70 percent of them to a discount buyer at 40 percent of cost (4.80). Scrapping cost 0.80 a unit; storage while waiting 1.50 a unit; extra selling cost (handling 0.60 plus transport 0.50) 1.10 a unit.
- Units sold 2,800. Revenue 13,440. Avoided scrapping 2,240. Avoided storage 4,200. Less extra selling cost 3,080. **Gain 16,800 a month.**
- Running cost 8,000 a month (160 hours at 25 plus tools 4,000). Net 8,800 a month at steady state.
- One-off 70,000 (system, labelling equipment, onboarding).
- Simple payback: 70,000 / 8,800 = **7.95 months** (too optimistic).
- Ramp: month 1 zero gain (setup), month 2 half, month 3 on full.
- Cumulative cash: month 1 minus 78,000 (70,000 plus 8,000), month 2 minus 77,600, month 3 minus 68,800, then plus 8,800 each month; month 10 minus 7,200; **month 11 plus 1,600: break-even in month 11.** Discounted at 10 percent a year: month 12.
- Low case (gain 70 percent, 11,760; net 3,760): break-even in month 24. The decision: approve if the sponsor accepts a two-year worst case; first confirm the buyer and the 70 percent sell-through with a pilot lot.
- Note the shape the owner described: a big negative first month, then recovery; what changes the month is the ramp and the running cost.

## Value stream numbers (worked)
Invoice approval: receive 0.1 day of work and then 1.0 waiting; coding 0.3 and 2.0; approval 0.2 and 6.0; payment run 0.1 and 3.0. Process time 0.7 day, waiting 12 days, **lead time 12.7 days** (work plus waiting), value-added share 0.7/12.7 = **5.5 percent**. Yields 95, 80, 90 and 98 percent: rolled throughput yield 0.67. The approval wait holds 6 of the 12.7 days (47 percent): the TO BE starts there (delegated limits, parallel approval), not at the 0.2 days of work. Sanity check: 1,500 invoices x 0.7 day of work is 1,050 work-days a month, about 50 full-time people; if the real team is much smaller, the times are elapsed time or batch time, not hands-on work, and the baseline must be re-measured before costing anything.

## Statistical tools and when
- **Run chart or control chart** [C]: tells common-cause from special-cause variation; do not react to every point (Wheeler, Understanding Variation). Use after the change and in Control.
- **Process capability**: only on a stable process; otherwise the index is meaningless.
- **Sigma levels and DPMO**: the 3.4 per million figure assumes a 1.5-sigma long-term shift convention [F]; do not present it as a law. Use first-pass yield and defects per million opportunities as plain measures.
- **Sample size**: for a before-after claim, use enough cases; a difference of two weeks of data is noise unless the process is stable.
- **Pilot first**: the improvement is proven on a small scope with the same measures, then scaled.

## What must be stated as unverified
Baseline from memory, the rate per hour not given by finance, adoption assumed, the buyer or vendor price not confirmed, any benefit still soft. Say so in the case, not in a footnote.
