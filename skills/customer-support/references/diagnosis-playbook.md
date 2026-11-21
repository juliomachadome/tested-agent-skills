# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: a wrong denominator or a broken export makes every branch meaningless. Thresholds are **[F]** (practitioner starting points) unless tagged; the team's own last 8-12 weeks replace them. Evidence tags: **[C]** consensus or law, **[M]** serious but single or correlational, **[F]** practitioner or vendor, **[X]** myth. Nothing is copied from a source; ideas are applied. Typical fields: ticket id, created, first reply, solved, status, channel, tags (area, cause), requester id, agent, reopened flag, CSAT, article linked, bot-handled flag.

## Step 0: is the data trustworthy?
| Check | How | If it fails |
|---|---|---|
| Same period, timezone, business-hours calendar in all reports | compare 3 tickets by hand against the export | fix the calendar before comparing SLAs |
| Definitions | "solved" vs "closed"; is a bot reply a "first response"? does auto-merge hide duplicates? are spam and internal tickets removed? | write the definition next to every metric |
| Denominator | CSAT = good ÷ responses (also report responses ÷ solved tickets); reopen rate = reopened ÷ solved in the cohort | recompute and label |
| Volume per cohort | CSAT with under about 30 responses in a cell moves 10+ points on noise (95% range at n=30, 80% good: roughly ±14 points) | report "not enough responses"; read verbatims instead |
| Tagging coverage | share of tickets with a cause tag | under 70%: sample 50 tickets by hand first |
| Change calendar | releases, pricing or billing changes, campaigns, outages, staff changes, policy changes in the window | line them up on the timeline before any cause is named |

## Core arithmetic
- **Staffing**: agents needed = (tickets per day × average handle time in minutes) ÷ (productive minutes per agent per day), then divide by target occupancy. Worked example: 240 tickets/day (email-like, async), 11 minutes handle time incl. wrap-up = 2,640 min. An agent with 7.5 paid hours has about 5.5 productive hours after breaks, meetings, training, coaching and leave (share varies; 70-75% productive is a common planning figure **[F]**) = 330 min. 2,640 ÷ 330 = 8.0 agents at 100% occupancy; at 85% target occupancy 8.0 ÷ 0.85 = 9.4, so 10 heads, plus about 12-15% for holidays and sickness **[F]** = 11. Check it against the real backlog and reply times.
- **Erlang caution**: Erlang C and its relatives assume random arrivals and a queue where callers wait (live phone, chat). Email and async messaging have deadlines of hours, so a simple workload calculation above is fine; for live chat or phone with seconds-level targets use Erlang-style tools or a vendor calculator, and note that small teams (under about 5 agents) have high variance: a single long call breaks the model. Also chat concurrency (one agent on 2-3 chats) lowers handle time per chat but raises error rates **[F]**. Treat results as planning, not truth; verify with weekly actuals.
- **Backlog dynamics**: backlog change per week = created − solved. If created exceeds solved by 40 tickets/week, a backlog of 200 doubles in 5 weeks. Time to clear a backlog B with spare capacity s per week = B ÷ s.
- **Contact rate** = tickets ÷ active customers (or orders) in the same period; the right measure for "did the product get noisier", because volume alone rises with growth.
- **Repeat contact rate** = customers with 2+ tickets on the same issue in 7 days (or 30) ÷ customers with at least one ticket; **contacts per resolved issue** = tickets ÷ distinct issues.
- **Cost per ticket** = (agent cost + tools + management) ÷ tickets; use it only to compare options, not to push handle time down (see burnout and CSAT branches).

## Tree A: CSAT falling
| Check first | Likely cause | How to check | Fix |
|---|---|---|---|
| Response volume or mix changed | survey sent only after some channels or only to solved tickets; response rate fell | responses ÷ solved by week and channel | keep the survey rule fixed; compare same-channel cohorts |
| First response slower | staffing gap, backlog, holiday | median and 90th percentile first reply, by hour of day | Tree B |
| More contacts per issue | bug or unclear instruction; policy change | repeat contact rate; top tags with CSAT split | Tree D; fix the cause, article, policy |
| One cause tag dominates the bad scores | a release or a policy ("no refund after 30 days") | CSAT by tag and by policy-decision ticket; read 20 verbatims | change policy or message; write the reason into the reply |
| One agent or one macro | tone or accuracy problem | CSAT by agent with n; macro used in bad tickets | coaching with tickets, macro rewrite; never rank on small n |
| The score reflects the product, not the support | "I hate the new pricing" verbatims | tag the reason in verbatims: product, policy, agent, speed | send to product via the VoC report (`playbooks.md`); do not coach agents for it |
Remember CSAT measures one interaction and carries response bias towards extremes **[M]**; read the reasons, not the average.

## Tree B: backlog growing / first response SLA missed
Compute created, solved, backlog, median and p90 first response and resolution time per week; split by hour of day and day of week.
| Pattern | Likely cause | Check | Fix |
|---|---|---|---|
| Created > solved steadily | understaffing or growth without cost-of-contact work | staffing arithmetic above vs actual agents on shift | hire or reduce contacts (Trees D, E, H); cut work that is not support (refund approvals in the queue, internal requests) |
| Spikes at fixed hours | shifts do not match arrival curve (Monday morning, after e-mail campaign) | tickets created by hour vs agents on shift | move shifts; schedule campaigns with support |
| p50 fine, p90 bad | long-tail tickets waiting on another team or on the customer | age of tickets by status; "pending" vs "on hold" | status discipline, clock paused only for the customer, owner for every hold |
| Many tickets touched, few solved | cherry-picking, bad triage, tickets bounced | touches per ticket; reassignments | one owner per ticket, triage rules (`playbooks.md`), limit work in progress |
| Sudden jump | release or outage (Tree E) | change calendar | incident macro and one engineering issue |
Promise real SLAs; a miss triggers a note to the customer. The first-response metric is gameable (an empty acknowledgement): if the median is fast but resolution slow, count only a reply that moves the case.

## Tree C: high reopen rate
| Likely cause | Check | Fix |
|---|---|---|
| Closed without verifying the fix | reopen reasons on 30 tickets: "still broken" vs "new question" | ask the customer to confirm, auto-close after a stated wait only when a fix was confirmed |
| Fix is a workaround, cause remains | same tag reopened within 7 days | engineering issue linked; tell customers a fix is coming |
| Agent answered the wrong question | compare first customer message with the closing reply | reread-before-send habit; ask a clarifying question first |
| Auto-close rules too aggressive | reopens right after auto-close timer | lengthen the timer, send a reminder |
| Reopen counted when a customer says "thanks" | share of reopens with a thank-you only | change the system so thanks does not reopen |

## Tree D: repeat contacts on the same issue
Find the issue: group by customer, then by tag or text similarity within 7-30 days.
| Cause | Check | Fix |
|---|---|---|
| Bug not fixed or fix not rolled out | same version or plan, rising count | escalation (`escalation-template.md`), customer notice at ship |
| Unclear message in the product, email or billing page | the same first question in many tickets | fix the copy at the source (with the copywriting skill) |
| Reply gave steps but no result | customer returns saying "I did it, nothing" | add expected result and the check ("you should see X") to the article and macro |
| Channel bounce (bot then e-mail then chat) | customers with 3+ channels per issue | one case id across channels, history visible to the agent |
| Promise missed (update promised and not sent) | tickets "any update?" | set the next update date in the ticket; alert on due dates |
Customers punished effort (repeating themselves, switching channels) more than they rewarded surprise **[M]** (vendor-led study). Fix the largest repeat cluster first.

## Tree E: ticket volume spike after a release
1. Time of the first spike vs deploy times (ticket created timestamps vs release log, same timezone).
2. Tag or text clusters in the spike window; compare with the same weekday earlier.
3. Is it one bug (similar steps and errors), a UX change (how-to questions), a pricing or billing change, or an outage?
4. Contact rate vs prior release, to separate growth from regression.
Actions: one engineering issue, with all tickets linked; an incident or known-issue macro; a banner or status note if it affects many; ask product for rollback or feature flag if the cost per hour of tickets is high; after the fix, a customer notice and an article. Add support to the release checklist: what changed, expected questions, a draft macro, a rollback path **[F]**. Review the expected-vs-actual contact bump per release in the weekly review.

## Tree F: deflection up but CSAT down (customers are giving up)
A "deflection" counted when a customer saw an article or bot and did not open a ticket is not a resolution **[M/F]**.
| Check | What it shows | Fix |
|---|---|---|
| Resolved-without-recontact | share of bot or article sessions with no ticket, chat, or call from that customer in 7 days | judge success on this, not on tickets avoided |
| Bot abandon points | where conversations end without a human or a resolution; "agent" or "human" typed | clear human path, show when it is a bot |
| Escape via other channels | rise in social posts, phone calls, chargebacks after the bot launched | weight these as failure of deflection |
| Article helpfulness | thumbs-down and search with no click; query phrases customers use | rewrite in their words; KCS improve loop |
| Topic scope | bot answering payments, cancellation, complaints | remove those from the bot |
| CSAT sample bias | survey sent only after human contact, so the unhappy who gave up never answer | survey bot sessions too |
Correct course by routing sensitive categories to humans first, fixing top 10 articles, and reporting deflection net of recontact.

## Tree G: angry escalations and social complaints
| Cause | Check | Fix |
|---|---|---|
| Slow or no reply | time to first reply of the posted-about ticket | public acknowledgement within the hour, private resolution thread, link back later |
| Policy felt unfair | tag: refund, cancel, ban; read the thread | review the policy with the owner; fix the message even if policy stays |
| Repeat failure | customer had 3+ contacts | single owner, named; apologise once with specifics |
| Real defect or outage | many posts, same topic | incident comms template (`playbooks.md`) |
| Pattern of one abusive account | threats, repeated abuse | abusive-customer recipe |
Never argue in public; do not delete honest criticism; do not disclose private details on a public channel. Track social complaints as a leading indicator in the weekly review.

## Tree H: chargebacks and refund rate up
Refund rate = refunds ÷ orders (same cohort, same window); chargeback ratio = disputes ÷ transactions (card-network thresholds unverified, see `refunds-consumer-law.md`).
| Cause | Check | Fix |
|---|---|---|
| Customers cannot find how to cancel or contact you | "cancel" searches, "charged after cancel" tickets | clear cancel and contact path; descriptor recognisable on the statement |
| Unrecognised charge (descriptor, family use) | disputes with "fraud" reason, tickets "what is this charge" | billing descriptor, receipts, renewal reminders |
| Product not as described | refund reasons, reviews | change the page copy (copywriting skill), onboarding |
| A bug or outage with no credit | refunds clustered after an incident | proactive credit and notice |
| Real fraud | same card, velocity, new country | payment provider tools; escalate to the owner |
| Support too slow to refund | refund request age before dispute | fast-path refunds; a refund costs less than a dispute |
Do not set agent targets to "avoid refunds"; set a rule for what to grant.

## Tree I: help articles not used
| Check | Cause | Fix |
|---|---|---|
| Search with no results or no click | wrong words (internal jargon) | titles as the customer's problem phrase; synonyms |
| Article linked rate in tickets under 30% **[F]** | agents do not search or links are not in the macro | search-first habit, link in the macro, review monthly |
| High views, low "solved" | article incomplete or outdated | owner, review date, test the steps |
| Not visible | no entry points in product or email | link from the screen where the problem occurs |
| Sprawl | duplicates and stale content | merge or retire; measure reuse, not count |
KCS says to capture in the workflow and improve on reuse, and its content-health and self-service measures are the metrics to open next **[M]** (practices guide listing read; the metric definitions were not).

## Tree J: agent burnout and turnover
| Signal | Check | Fix |
|---|---|---|
| Occupancy above about 85-90% for weeks **[F]** | schedule adherence, no recovery time | add capacity; protect time off the queue |
| Many tickets with abuse or emotional load | share of tickets tagged angry or abusive; contact-by-agent skew | rotate; escalation path; abusive-customer recipe; a rule that agents may end abuse |
| Metrics pressure (handle time, CSAT as pay) | complaints; gaming signs | remove single-score pay; use quality review of tickets |
| No growth or no power to fix | exit interviews | allow agents to edit articles and flag product issues; a visible loop from VoC |
| Repetitive tickets | top 5 tags = half of volume | remove causes (Trees D, I) |
| Tools friction | tool time per ticket | fix the tooling |
Turnover also resets knowledge: track time to proficiency of new agents, and keep articles current so training is lighter.

## Tree K: NPS and churn disagree
| Check | Cause | Fix |
|---|---|---|
| Who answers | NPS sent to active power users; churners never answer | survey churned and downgraded customers; compare the response base to the customer base |
| Timing | NPS right after onboarding vs at month 9 | align the survey to the lifecycle stage |
| Churn driver is price, budget or business closure, not satisfaction | cancellation reasons | split voluntary and involuntary churn (failed payments) |
| Segment mix | enterprise vs SMB | compute by segment |
| Score vs behaviour | in independent research (21 firms, 15,500+ interviews), the claimed clear superiority of NPS in predicting growth was not replicated **[P]** (Keiningham et al. 2007, abstract read 15/11/2026; it does not show NPS to be worse) | use NPS as one input beside usage, retention and cancellation reasons |
Read the free-text reason on every detractor and on every cancellation.

## Tree L: bot complaints
| Complaint | Check | Fix |
|---|---|---|
| "It does not understand me" | intents failed; fallback rate | add intents from real tickets; hand-off earlier |
| "I cannot reach a human" | path to human; time to hand-off | visible option at every step; two failed turns trigger a hand-off |
| "It gave a wrong answer" | answer vs policy; stale knowledge | single source of truth; review top answers weekly |
| "It pretended to be human" | disclosure | say it is a bot **[C]** (verify local rules) |
| Customer repeats everything after hand-off | context passing | pass the transcript to the agent |
Escalate bot errors that touched money or privacy like incidents.

## What to output
Name the branch, the data used, the check result, the fix list ordered by effect over effort with owner and date, the single metric that will confirm it, and what could not be verified (field missing, n too small, definitions unknown).
