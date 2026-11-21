# Deal diagnosis: symptom, likely causes, check, fix

Use it top-down. Thresholds and ratios are **[F]** (practitioner starting points) unless tagged; the company's own last-4-quarters data replaces them. Evidence tags: **[C]** consensus or law, **[M]** serious but single or correlational, **[F]** practitioner, **[X]** myth. Nothing here is copied from a book; the ideas are applied.

## Step 0: is the data trustworthy? (before blaming the rep, the buyer or the product)
| Check | Metric | If it fails |
|---|---|---|
| Stage is set by a buyer action, not by seller feeling | sample 10 open deals: can you name the buyer's last action and its date? | rewrite stage exit criteria (`pipeline-forecast.md`) before reading any conversion number |
| Cohorts are comparable | same segment, same deal-size band, same lead source, same period | split by segment first; a blended win rate hides one good and one bad market |
| Denominator is right | win rate = won / (won + lost), **closed** deals of one cohort. "Won / created" is conversion, not win rate. "No decision" counted as lost? | recompute both and label them |
| Enough volume | under about 30 closed deals in a cohort the win rate has a 95% range of roughly ±17 points (at 50%) | write "not enough volume to conclude"; qualitative review of every lost deal instead |
| Sales cycle measured on closed deals only | open old deals are not "average cycle" | report median of closed-won, and age of open deals separately |

## The five metrics every diagnosis names
1. **Stage conversion** = deals that reached stage N+1 ÷ deals that reached stage N (same cohort, same window).
2. **Cycle time** = days from stage 1 entry to close (median, won and lost separately) and days in current stage.
3. **Win rate** = won ÷ (won + lost), by segment and source. "No decision" is the biggest competitor in many markets **[F]**: track it as its own loss reason.
4. **ACV** (annual contract value, or deal value if one-off) and its spread; discount given as share of list.
5. **Next-step coverage** = open deals with a dated, buyer-confirmed next step ÷ open deals. Target 100%.

## Symptom table (one row = one deal-level problem)
For each: what to ask the buyer (or yourself), the metric that shows it at pipeline level, and the fix.

| Symptom | Likely causes | Question to ask | Metric that shows it | Fix |
|---|---|---|---|---|
| **No next step** after a call or demo | recap not sent; buyer polite not interested; rep afraid to ask; no agenda so no outcome | "To decide well, what needs to happen between now and a decision, and can we put the next one on the calendar now?" | next-step coverage under 90%; deals idle 14+ days; call-to-next-meeting rate | end every call by booking the next dated step (in the invite); same-day recap with 3 bullets and the proposed step; if the buyer will not commit to a date twice, mark as "no decision risk" and drop probability |
| **Great calls, nothing moves** (compliments, "keep in touch", "very impressive") | the call ended in a continuation, not an advance; no explicit need stated; objective was information or rapport; polite exit | "What would you want to see or do next, and who needs to be involved? Can we book it now?" | share of calls that end with a buyer action; calls to advance ratio; stage with the oldest idle deals | write the intended buyer action before each call (trial, technical review, intro to the economic buyer); log calls as advance or continuation; in discovery pursue explicit needs, not only problems (`playbooks.md` 7.3-7.4) |
| **Single-threaded** (one champion, nobody else seen) | champion leaves, is not senior, or is a "friendly" with no power | "Who else will be affected or has to say yes? Could we include them in the next conversation?" | share of deals past stage 3 with 1 contact; win rate single vs multi-thread | give the champion a one-page case to forward; ask for an intro to the economic buyer and a user; propose a 30-minute session with finance or IT; a deal with one contact after stage 3 is not forecast in commit **[F]** |
| **No budget / no authority** | pain too small to fund; budget cycle closed; person is an evaluator, not a buyer; spend sits in another department | "How do similar projects get funded here? Who owns that line? When is the next planning window? What would this displace?" | stage 2→3 conversion low, deals die at proposal; discount requests rise late | quantify the gap in the buyer's money (`playbooks.md` discovery); find the owner of the budget; for fixed cycles, agree a date to be in the next plan; pilot sized under the person's own signing limit only if the pilot leads to a decision path, not as a trap |
| **"Too expensive"** | value unproven; no comparison point; wrong buyer (cost owner, not value owner); price compared to a different scope; real budget ceiling | "Expensive compared with what: another offer, the budget you have, or the cost of the problem? If I got the price to X, what else would still stop this?" | discount depth above 15-20% of list; late-stage losses citing price; ACV falling with volume flat | `objections` map in `playbooks.md`; compute the gap-vs-price ratio (worked example below); trade scope, term or payment date for price, never free discount |
| **Ghosting after the proposal** | proposal surprised them (discovery was thin); sent to the wrong person; champion has no internal answer; competitor chosen quietly; priorities changed | "Was anything in the proposal different from what you expected?" plus a break-up note: "I will close this file on [date] unless something changed; either answer helps" | proposal-to-decision rate; share of "no decision"; days since last reply | send proposals only after a call walks through them; follow-up cadence in `playbooks.md`; after 3 value touches and the break-up note, close the deal and log reason "no response"; reopen on a trigger event |
| **Long procurement** (security review, legal, vendor onboarding, tender) | late involvement of procurement and security; unknown steps; paper requirements | "What are all the steps after you say yes: security, legal, vendor form, signatures? Who does each, how long did the last one take?" | days in stage 4-5; stage 4→close conversion; slippage of close date | map the approval path in discovery and write it as a mutual plan with dates; send security pack, DPA, insurance and references early; open legal in parallel; for public buyers see `b2g-procurement.md` |
| **Competitor or incumbent** | status quo is "free" (switching cost); incumbent has relationships; you lack a differentiator for this buyer's criteria | "What do you value most in the current solution? What is missing? What would have to be true for you to move?" | win rate vs named competitor; "lost to incumbent / no decision" share | gap analysis, not attack; a side-by-side pilot on one measurable job; address switching cost explicitly (migration plan, parallel run); if criteria favour the competitor, disqualify early |
| **Scope creep** (pre-sale or post-sale) | requirements grow to please everyone; no written scope; free "just one more" asks | "Which of these is needed for the first measurable result and which can come in phase 2?" | proposal revisions per deal (over 3); delivery overrun | write in/out of scope, assumptions and change control; every addition is priced or traded; phased plan |
| **Low win rate** | poor qualification (too many weak deals), wrong ICP, no differentiator, discovery too shallow, late pricing conversation | review 10 lost + 10 won: where did the won deals differ (champion, EB access, quantified pain, pilot)? | win rate by source and segment; win rate when EB met vs not | tighten qualification (scorecard below), stop working the segments with under half the average win rate, coach on discovery recordings |
| **Pipeline not converting by stage** | one stage leaks; stage definition vague; wrong lead mix | which transition is lowest vs the company's own baseline? (table next) | stage conversion by transition | fix the leakiest transition first (table) |

## Stage-leak table (find the leaking transition, then the cause)
| Transition | Healthy-looking range **[F]**, B2B mid-ticket | If low, check | Typical fix |
|---|---|---|---|
| Lead → qualified opportunity | 10-30% (inbound), 1-5% (cold outbound) | lead source quality, ICP fit, speed to first contact (hours, not days) | tighten ICP and the bar for "qualified"; respond fast; stop a source with near-zero conversion |
| Qualified → discovery done (pain quantified) | 50-70% | no-shows, call set up as demo instead of discovery, wrong contact | confirm the agenda and attendee beforehand; discovery before demo |
| Discovery → proposal/solution | 40-60% | pain too small, no budget path, EB unknown | disqualify earlier and explicitly; get EB in the room |
| Proposal → negotiation/decision | 40-60% | proposal not walked through, price shock, no mutual plan | live proposal review; options (3 packages); mutual plan |
| Negotiation → closed-won | 60-80% | procurement, legal, late stakeholders, discount fight | map the path early; trade concessions; legal in parallel |

These ranges are broad rules of thumb from practitioner material, not measured benchmarks; do not report them as industry data. Use the company's own history.

## Worked example: the "too expensive" arithmetic
Situation: your price 60,000 per year; competitor quote claimed at 30% less (42,000); buyer's discovery numbers: 6 people lose 4 h/week each to the manual task, loaded cost 40 per hour.
- Cost of the problem per year = 6 × 4 × 52 × 40 = **49,920**.
- If your product removes 70% of that time: benefit = 34,944 per year. Net first-year value at 60,000 price = **-25,056** (not viable as stated). At the buyer's own numbers the price must be below the benefit, or the benefit larger (error cost, delay, risk not yet counted). This is why discovery must find the other costs, or you must say honestly that the case does not clear.
- If the quantified benefit were 150,000 per year, price 60,000 gives payback of 4.8 months and the 18,000 gap to the competitor is 12% of the benefit; the question becomes "what do we lose in the next 12 months if we pick the cheaper offer and it removes less?".
- Discount cost: a 30% discount on 60,000 gives away 18,000. At a 70% gross margin the deal's gross profit falls from 42,000 to 24,000, i.e. 43% less (use your own margin). Never match a number you have not seen: ask for the quote or the scope list. A claimed rival price with no scope is not information.
Thin case: if the confirmed annual benefit is under about 2x the price (as in the first branch of the example above), say so plainly; look for costs not yet counted (errors, delay, risk, compliance), change scope or price structure, or disqualify. Do not oversell a case the buyer's own numbers do not support.
Rules: use only numbers the buyer gave or confirmed; label the rest as assumptions; never invent the competitor's offer or a "final price" deadline.

## Next-step language (use verbatim as a pattern)
- Calendar-first: "Let's put 30 minutes with [name] on [date]; I'll send the 1-page summary today so you can forward it."
- Mutual plan line: "If we both stay on this path: security review by [date], legal by [date], decision by [date]. What might break it?"
- Break-up note: "Not hearing back usually means priorities moved. I will close this out on [date]. If it is still a priority, one line is enough to reopen."

## Reporting a diagnosis
Output: (1) data used and its quality, (2) the stage or deal where it leaks, with the metric, (3) the most likely cause and the second most likely, (4) the next action per deal with the question to ask and the owner, (5) what could not be verified (missing CRM fields, small sample, no call recordings).
