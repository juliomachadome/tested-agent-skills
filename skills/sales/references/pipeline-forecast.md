# Pipeline and forecast

Evidence **[F]** except where tagged. The rule: a stage is a statement about what the buyer has done, not about how the seller feels.

## 1. Stage definitions with exit criteria (B2B, adapt to your cycle)
| # | Stage | Exit criteria (all true, evidence in CRM) | Usual risk if skipped |
|---|---|---|---|
| 1 | Lead / prospect | fits ICP; a contact; a reason (trigger) | wasted effort |
| 2 | Qualified | buyer-confirmed pain and owner; a person with a plausible budget path; discovery call booked | pitching before the problem is known |
| 3 | Discovery done / opportunity | gap quantified in the buyer's numbers; decision process, criteria and timeline noted; second stakeholder identified | proposals with no business case |
| 4 | Solution / proposal | solution reviewed live with the buyer; proposal sent after review; EB identified and aware; dated next step | proposal ghosting |
| 5 | Negotiation / mutual plan | EB engaged; written mutual plan with dates for security, legal, procurement; pricing discussed | late surprises |
| 6 | Commit | buyer states decision intent and the date; no open blocker except paperwork | forecast inflation |
| 7 | Closed-won / lost | signature (or PO); loss reason from a fixed list incl. "no decision" and "no response" | learning lost |
Required fields per open deal: buyer name and role, EB, pain in their words, amount basis (how computed), next step with date, close date, loss/win reason when closed, source.

## 2. Hygiene rules (weekly)
- No next step with date → deal is stale; fix or move down.
- No buyer activity for 14+ days (30 for long cycles) → flag; one break-up attempt, then close.
- Close date pushed twice → probability halves; pushed three times → close or re-stage.
- Single contact after stage 3 → not in commit.
- Deal older than 2x the median cycle of won deals → review for close or a real reason.
- Amount without a basis (list × quantity or a signed scope) → set to zero in forecast.
- Duplicates, deals with no owner, deals in the past → clean at the review.
- Record every stage change with the date; conversion stats need it.

## 3. Forecast methods
| Method | How | Good for | Weak because |
|---|---|---|---|
| **Weighted pipeline** | Σ amount × stage probability | volume planning on 100+ deals | probabilities arbitrary unless from your own history; one huge deal distorts |
| **Historical stage conversion** | Σ amount × (observed win rate from this stage, last 4-8 quarters, same segment) | the best default **[F]** | needs 30+ closed deals per stage and consistent stage rules |
| **Commit / best case / upside** | rep and manager call each deal by evidence, three buckets | short horizon (quarter, month) | judgement bias; pair with the evidence checklist |
| **Cycle-based** | open deals expected to close = deals older than X days at stage Y where history shows closing | early warning | ignores deal specifics |
Report three numbers: **commit** (deals with buyer-confirmed decision date and EB engaged, scored 3 on EB and process in `playbooks.md`), **likely** (historical conversion applied to the rest), **upside** (the rest at low weight). Show the previous forecast and what changed. Compare forecast vs actual each quarter; the error is the lesson.
Coverage: pipeline value ÷ target. A 3x coverage rule is a common rule of thumb **[F]**; the right figure is 1 ÷ your stage-1-to-won ratio.
Worked example: target 300,000; historical stage 3→won 25%; stage-3+ pipeline needed = 300,000 ÷ 0.25 = 1,200,000 (4x), not 3x.

## 4. Weekly pipeline review template (30 min; one table)
1. **Numbers**: closed-won, closed-lost, new opportunities, pipeline created, coverage, forecast change (commit, likely, upside).
2. **Movements**: deals that advanced, stalled, or were lost this week, with reason.
3. **Deal table** (only deals above stage 3 or above the amount cutoff):
| Deal | Stage | Amount | Close date | Last buyer activity | Next step and date | EB met? | Threads | Risk | Action and owner |
4. **Questions per deal**: What did the buyer do this week? What do they need to decide? Who else decides? What will stop this? If we do nothing, what happens?
5. **Hygiene list**: items from section 2, assigned.
6. **Decisions**: deals to drop, deals needing help (exec sponsor, a pilot, a price decision).
Monthly: win/loss reasons, cycle time by segment, stage conversion trend, forecast accuracy, discount depth.

## 5. Self-serve pipeline
Treat accounts like deals once a PQL fires; funnel metrics in `founder-and-self-serve.md`; attribution and cohort analysis in `growth-analytics`.
