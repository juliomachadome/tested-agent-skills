---
name: process-improvement
description: Use when a company project or operation must be justified to a manager, director or committee - a business case for automating, fixing or speeding up a process (approvals, invoices, orders, hiring, stock, support, reports), an A3, a DMAIC or lean six sigma project or charter (scope, out of scope, assumptions, risks, constraints), a value stream map, AS IS and TO BE, lead time and waiting time, rework, or hours saved turned into money per month, payback and break-even month, cost reduction vs revenue growth vs innovation. Brings the method and the honest money model (hard vs soft savings, ramp-up, cumulative cash curve, the threshold where the case flips). Not for a new product or the business model of a venture (business-model-finance, product-creation), unit economics of a sale (business-model-finance), chart styling (data-visualization-dashboards), a data analysis (data-analysis) or code design (software-architecture).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Process improvement and the business case

The goal is one page a decision-maker can approve or reject in five minutes: the problem in numbers, the process as it is and as it will be, what it costs, what it saves in money per month, and the month it pays for itself, with a worse case beside it. Evidence tags: **[C]** definition or accounting identity, **[M]** serious practitioner or single study, **[F]** rule of thumb or vendor claim, **[X]** myth. Details, templates and worked numbers are in the references.

## 1. Start: project first, then the five numbers
Read the current project's docs first (process descriptions, reports, cost rates, system exports, glossary, company templates); company rules and its own A3 or charter template override this skill. Then get, or state as assumptions: volume per month; time per step and waiting time between steps; cost per hour by role (loaded, as the company's finance defines it); error, rework and scrap rates; the one-off cost of the project and its running cost. A number nobody measured is an assumption: mark it and run the low case.

## 2. Is a project the right tool?
[C] If the fix is obvious, cheap and reversible, just do it (kaizen, one owner, one week) and measure. A project (charter, DMAIC) fits when the cause is unknown, the process crosses teams, or the money is large enough to need approval. If the problem is a new product or revenue line, hand the model to business-model-finance and product-creation; this skill then costs the change, it does not design the business.

## 3. DMAIC, with a gate per phase [C]
- **Define**: problem, goal with a number and a date, scope and out of scope, WBS (EAP), assumptions, risks, constraints, stakeholders. Gate: the sponsor signs the charter.
- **Measure**: baseline from real data, not memory; value stream map of the current state; data quality checked first. Gate: the baseline is trusted by the process owner.
- **Analyze**: root causes proven with data (Pareto, 5 Whys, cause-effect diagram, stratification), not guessed. Gate: each cause has evidence.
- **Improve**: countermeasures chosen against criteria, tried small, TO BE map, benefit recalculated with pilot data. Gate: the pilot beat the baseline.
- **Control**: standard work, owner, dashboard, control chart or simple run chart, trigger for action. Gate: the gain holds for the agreed period. A project without Control is a one-time clean-up.

## 4. A3: the one sheet [C]
A3 is a way of thinking and a 297 x 420 mm sheet (11 x 17 in as the nearest US size); the template is not the A3. The left half is the problem (background, current condition, goal, root cause), the right half is the answer (countermeasures, plan with who and when, follow-up and result). One owner signs it. It must read without the author in the room. Charts have to fit its grid: one chart per box, labelled, readable at arm's length. Layout and a filled example: `references/playbooks.md` 1.

## 5. VSM and AS IS to TO BE
Draw the current state first, with the real steps and the waiting between them, then the future state. Per step: process time, queue or waiting time, first-pass yield. Lead time is the sum of both; **value-added share = process time / lead time**, often a few percent [M]. The idle time is the "stopped value": that is where most of the saving is. Rolled throughput yield is the product of the step yields, so four steps at 95, 80, 90 and 98 percent give 67 percent, not 90. Present AS IS and TO BE side by side with the same measures, and show what changed in each step.

## 6. The money model (the part most business cases get wrong)
1. **Pick the benefit type** and say it: cost reduction (an operation that already runs costs less), revenue growth (new or larger revenue), innovation (capability or learning without a payback yet; say so, do not dress it as ROI). Revenue growth and a changed business model go to business-model-finance.
2. **Gain per month** in money: volume x unit effect. Every hour saved is **soft** until it becomes cash: overtime avoided, a contractor not hired, a hire not made, capacity sold. Hours saved that nobody redeploys are capacity, not a saving [M]. State hard and soft separately and count only hard in the break-even.
3. **Cost per month** of what the change consumes (licences, infra, hours of operation, upkeep) and the **one-off cost** (equipment, build, training, project hours at the role cost).
4. **Ramp-up**: the first months have the cost and little gain. Month 1 is negative.
5. **Curve and break-even**: plot cumulative net cash by month (gain minus cost, starting at minus the one-off cost). Break-even is the first month the line crosses zero. Do not stop at simple payback (one-off cost / steady monthly net): it ignores ramp-up and early running cost and is too optimistic; a worked case gives 7.95 months against a real crossing in month 11. Add a discounted version when the horizon is long or the company asks for NPV.
6. **Low case and one lever**: gain at 70 percent and the volume or adoption that kills the case. A single scenario is a guess.
7. **Do not invent inputs.** A ramp, a percentage or a share the user did not give is a labelled assumption, never a headline. Deliver the framing that was asked for first (the one-slide break-even, the A3), mark where it is optimistic, then compute the **threshold at which the case flips** (for example the share of saved hours that must become cash to cover the running cost) instead of arbitrary scenarios. If a cost line can be read two ways (avoided or incurred, such as storage while waiting), state your reading in one line and show the result of the other.
8. Numbers are computed with a script or sheet, inputs and formulas shown. Hand the check to business-model-finance when the project is large or tax and financing matter.

## 7. Who does what
This skill owns the method, the documents and the logic of the case. business-model-finance owns cash, taxes, scenarios and a changed business model (Business Model Canvas); data-visualization-dashboards owns chart craft; data-analysis owns messy data. Say who you handed what to.

## 8. AI tells to avoid (use while writing, not only in review)
Text: "unlock", "streamline", "leverage", "holistic", "robust"; benefits with no number; em-dash and rule-of-three rhythm; "significant savings" instead of the figure. Content: hours multiplied by a rate and called savings; one scenario; a break-even with no ramp-up; a VSM of the ideal process instead of the real one; a 5 Whys that stops at "human error" [C: a stop point, not a cause]; a root cause with no data; a "most change projects fail" percentage quoted as fact [X: Hughes 2011 asks whether any such figure has a basis]; sigma levels with the 1.5 shift stated as a law of nature [F]. Charts: default palette, 3D, a break-even line with no month marked, no low case.

## 9. Say what you chose and why
The output is for the customer: never name this skill, its references or a "playbook" in it.
Per choice, one line from the real case: why A3 and not a full DMAIC, why this benefit type, why this baseline period, why these steps are in scope, why hard savings only. Never "it is the usual way".

## 10. Which reference to open
- `references/diagnosis-playbook.md`: Step 0 on the data, then symptom trees ("the case is rejected", "savings never showed up", "the VSM looks perfect", "hours saved but no cash", "the gain faded after three months") and worked numbers.
- `references/playbooks.md`: A3 layout, project charter, DMAIC checklists, VSM measures, AS IS / TO BE table, business-case sheet with the full worked example, review agenda for the approval meeting.
- `references/BIBLIOGRAPHY.md`: books and pages with what was verified.

## 11. Core topics routed
Root cause tools, control charts and capability (Analyze, Control, diagnosis playbook); change adoption and standard work (Control); constraint thinking (Goldratt, diagnosis playbook); project scope and WBS (Define); NPV and payback (money model); portfolio choice between projects, and incentives, go to product-management.
