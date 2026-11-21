# Playbooks: process improvement and business case

Templates to adapt, not to copy blindly: the company's own template wins. Every choice on the sheet carries its reason from the real case.

> **Illustrative examples only.** The filled cases below are fictional, de-identified teaching scenarios with synthetic figures. They do not identify or report on a real company; validate all inputs with the organization that will make the decision.

## 1. A3 layout (one sheet, 297 x 420 mm)
Owner, sponsor and date in the top right corner. Title is the problem or the goal in a sentence with a number. Read left to right, top to bottom.

| Left half: the problem | Right half: the answer |
|---|---|
| 1. Background: why it matters now, in one or two lines | 5. Countermeasures: what will change, linked to a root cause |
| 2. Current condition: the VSM or a chart of the baseline, with the pain marked | 6. Plan: who, what, when (a short table or a timeline) |
| 3. Goal: measure, target, date | 7. Business case: the cumulative cash curve with the break-even month marked and the low case as a second line; one-off cost, monthly cost, monthly gain |
| 4. Root cause analysis: Pareto or cause tree with the data behind it | 8. Follow-up: how and when we check, the control metric and the trigger |

Rules: one chart per box and one message per chart; text in short phrases; the numbers a reader needs sit on the sheet, the detail in an annex. A sheet that needs the author to explain it is not done. Show a draft to the process owner before the meeting (the dialogue is part of the method).
Filled example (condensed, near-expiry stock): Title "Recover value from near-expiry stock: break-even in month 11". Background: 4,000 units a month scrapped, 48,000 of product plus 9,200 of scrapping and storage. Current: stock waits 6 weeks then is scrapped. Goal: sell 70 percent at 40 percent of cost by month 3. Root cause: no buyer channel and no rule for the discount window. Countermeasure: a discount channel plus a rule at 12 weeks to sell. Plan: pilot lot in month 1, full by month 3. Business case: one-off 70,000, running 8,000, gain 16,800, break-even month 11, low case month 24. Follow-up: sell-through rate weekly, trigger below 50 percent.

## 2. Project charter (Define)
1. Problem statement: what, where, how big, since when (with the baseline number and its source).
2. Goal and metric: measure, current value, target, date; one primary metric and at most two guardrails.
3. Benefit type: cost reduction, revenue growth or innovation; hard and soft benefit in money per month.
4. Scope: in, and explicitly out. Break the work into a WBS (EAP) down to packages one person can own.
5. Initial conditions: process owner, volume, current cost and time, systems, headcount, frozen constraints.
6. Assumptions (each with an owner to confirm), constraints (budget, time, systems, people, law), risks (cause, effect, probability, impact, response, owner).
7. Team and roles: sponsor, owner, finance partner, process experts.
8. Milestones with gates (see section 3) and the approval date.
9. Business case summary (section 6) and the review date.

## 3. DMAIC checklists
- **Define done when**: charter signed; goal has a number and a date; scope and out of scope agreed; stakeholders listed.
- **Measure done when**: data source and definition written; baseline for at least 3 months or a full cycle; current state VSM drawn from a walk of the real flow; data quality checked (missing, duplicated, test records).
- **Analyze done when**: causes ranked by data (Pareto, stratified); each cause tested (comparison, correlation with caution, or a trial); a cause tree to the level where a person can act; "human error" not accepted as a cause.
- **Improve done when**: options scored on criteria that came from the goal; pilot with the same measures; TO BE VSM; benefit recalculated with pilot numbers; risks updated; owner for rollout.
- **Control done when**: standard work written and trained; control metric on a visible chart with a trigger and a response plan; owner named; audit date set; the old way closed; lessons recorded.

## 4. VSM measures and notation
Per step: process time (PT), queue or waiting time (WT), first-pass yield (FPY), batch size, people, system. For the stream: lead time = sum of PT and WT, value-added share = PT / lead time, rolled throughput yield = product of FPY, takt time = available time / demand, work in progress between steps.
Draw: customer on the right, request on the left, steps as boxes, a triangle for waiting with its time, a timeline below with the two sums. Mark the "idle value" (money stopped in the queue, for example stock or invoices awaiting approval times their value times the cost of money) on the biggest triangle. Draw current state first from a walk; the future state follows the lean guidelines (flow where possible, pull where not, one pacemaker point, level the load).

## 5. AS IS and TO BE table
| Step | AS IS (PT, WT, FPY, who) | Problem | TO BE (PT, WT, FPY, who) | Change | Owner and date |
Totals row: lead time, value-added share, rolled yield, cost per case. The table and the two VSMs use the same measures so the reader compares like with like.

## 6. Business-case sheet
Inputs (each with source and a tag fact or assumption): volume per month; unit effect; share that becomes cash; one-off cost; running cost per month; ramp (month, percent of gain); loaded rates by role; discount rate if used.
Calculation rows by month: gain, running cost, net, cumulative (starting at minus one-off), discounted cumulative if used. Break-even month = first month cumulative is at or above zero. Low case: gain at 70 percent, plus the adoption level at which the case fails.
Checks: hard and soft shown separately; month 1 is negative; running cost is in the first month; the unit effect has a pilot or a reference; the sum of monthly gains cannot exceed the real cost line it comes from.
Report: one line "approve if the sponsor accepts break-even in month X (low case month Y)". Hand cash, taxes or financing questions to business-model-finance.

Benefit types and the canvas: cost reduction touches cost structure, key activities, key resources; revenue growth touches revenue streams, customer segments, value proposition; innovation touches key partners and value proposition. If the project changes the model itself, hand it to business-model-finance (it has the canvas).

## 7. The three charts (for the A3 and the deck)
1. Cumulative net cash by month: line, zero line, break-even month marked and labelled, low case as a second line in a muted colour.
2. Gain versus cost by month: two lines or bars; the crossing is the break-even. Say what each line includes.
3. Lead time by step (before and after): horizontal bars with waiting and work in two colours; or the VSM timeline.
Chart craft (axes, palette, accessible colour, labelling) goes to data-visualization-dashboards; the content decides which chart.

## 8. Approval meeting agenda (20 minutes)
1. The problem and the number (2 min). 2. Baseline and how it was measured (3). 3. Root cause (3). 4. AS IS and TO BE (3). 5. The case: cost, gain, break-even, low case (5). 6. The decision requested and the date (2). 7. Questions on the weakest assumption, which the author names first (2).
After: record the decision, the owner and the follow-up date within a day.

## 9. Kaizen (when the project is too big a tool)
Cheap and reversible fixes: write the change, the owner and the measure on a card, do it in a week, check the measure, keep or drop. A list of these can sit under a larger project.
