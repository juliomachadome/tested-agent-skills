---
name: sales
description: Use for any B2B, B2G (public tender) or founder-led/self-serve sales task, even short ones - diagnose a stalled or lost deal ("no next step", "ghosted after the proposal", "too expensive", "they use a competitor", "procurement is slow"), prepare a discovery call, qualify with MEDDICC, handle objections, negotiate, write a proposal or follow-up cadence, answer a public tender or edital (Lei 14.133, EU 2014/24, FAR), review a pipeline and forecast, or read a call transcript or CRM export. Ethical by default. Not for page or ad copy (copywriting, ad-creatives), price tiers, bundles or guarantees (offers), or support replies and refunds (customer-support).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Sales

Selling is helping a buyer decide well. You win when the problem is real, the buyer (not only you) has put a cost on it, and the next step is dated and agreed. Everything below serves those three things. Evidence tags: **[C]** consensus or law, **[M]** serious but single, old or correlational, **[F]** practitioner or vendor, **[X]** myth.

## 1. Start: context and data before tactics
Read the current project's docs first (ICP, pricing, product limits, terms, brand voice, sales notes); project rules override this skill. Then fix, in five lines, who buys and who pays; what happens if they do nothing; the buying process (steps, people, dates, budget cycle); the alternative (competitor or status quo); the next step wanted. If data is thin, ask for the minimum or state the assumption.

Ask for, by task: **deal** - stage, last buyer action and date, contacts and roles, amount basis, what the buyer said about budget, decision process and competitors, call notes or transcript. **Pipeline** - CRM export with stage dates, source, amount, close dates, win/loss reasons, last 4 quarters of closed deals. **Tender** - the full edital or notice, annexes, dates, the company's registrations and references. **Price pushback** - your price, the competitor's claimed price and scope, the buyer's numbers on the cost of the problem.

## 2. Pick the motion
| Motion | Rule |
|---|---|
| Self-serve | The product sells; people remove blockers (pricing page, trial hand-off at a product signal). No call before a card form. -> `references/founder-and-self-serve.md` (incl. customer development, section 7) |
| Founder-led | Do the first 20-50 deals yourself; log every objection; hire after a repeatable pitch and 10+ similar closes. Same file. |
| B2B sales-assisted | Several stakeholders: qualify hard, multi-thread early, keep a mutual plan. -> `playbooks.md`, `pipeline-forecast.md` |
| B2G (tender, public procurement) | Rules decide, not rapport. Eligibility, documents, deadlines, official channel only. -> `b2g-procurement.md` (not legal advice) |

## 3. Diagnose first (stalled or lost deal, weak pipeline)
Run `references/deal-diagnosis.md` top-down: Step 0 data quality (stage defined by buyer actions, cohorts, denominators, sample size), then the symptom table: no next step, single-threaded champion, no budget or authority, "too expensive", ghosting after proposal, long procurement, competitor or incumbent, scope creep, low win rate, stage leaks. Each row gives causes, the buyer question, the metric and the fix. Output: data used and its quality, where it leaks, most likely and second cause, next action per deal with the question and owner, what you could not verify. With under about 30 closed deals in a cohort, say the win rate is too noisy to conclude and review each loss by hand.

## 4. Discovery and qualification
Method families by need, not brand **[M]**: SPIN (Rackham) moves from facts to implications to the buyer stating the value; Gap Selling (Keenan) quantifies current state, future state and the gap in the buyer's money; Challenger (Dixon and Adamson) teaches an insight when the buyer does not know what they miss (weaker in small deals; use the teaching, skip pressure); the Mom Test (Fitzpatrick) asks about past behaviour for founders. Call shape: agenda and permission, situation (few), problem, implication, future state, decision process, dated next step; buyer talks most of the time; recap within a day. Script: `references/playbooks.md` section 1.
Qualify with a question list, not a score you trust blindly **[F]**. MEDDICC with a 0-3 scale is in `playbooks.md` section 2. Any 0 on Economic buyer, Pain or Decision process at proposal stage means go back a stage. Disqualify early and politely; a "no" in week 1 is cheaper than a "no decision" in month 5.

## 5. Objections, follow-up, proposal, negotiation
- **Objections** (price, timing, trust, status quo): listen, ask what the concern really is, answer with a fact, a comparison or a small test, check, agree the next step. Ethical patterns: `playbooks.md` section 3. "Too expensive" is first arithmetic (cost of problem vs price, worked example in `deal-diagnosis.md`), then scope options, never a first-move discount.
- **Follow-up cadence**: 5-8 touches in 3-4 weeks across two channels, each with new value, a dated break-up note; stop at "no"; respect consent law. Table in `playbooks.md` section 4.
- **Proposal**: problem in their words, outcome and measure, solution, scope in/out, plan, three price options, risks, terms with a real validity date, next step. Walk through it live before sending. Template: `playbooks.md` section 5.
- **Negotiation**: prepare BATNA, floor and variables; interests over positions and objective criteria (Fisher and Ury **[C]**); calibrated questions and labels (Voss **[M]**); trade, never give; anchor from documented value. Never invent a rival offer, deadline, approval limit or "last price". `playbooks.md` section 6.

## 6. Public buyers (B2G)
Read the whole notice; check eligibility and qualification documents; decide bid or no-bid in 24-48 hours; ask clarifications in writing through the official channel and use the challenge window for restrictive clauses; build a compliance matrix with evidence; price from cost with a floor you will not break in a live auction; submit early with proof. Conduct: no contact with evaluators outside the channel, no gifts, no coordination with competitors, no false documents. Open, documented market engagement before a notice exists is legitimate; private shaping of a live tender is not. Lei 14.133 (Brazil), EU Directive 2014/24 and US FAR specifics are in `b2g-procurement.md`; yearly-indexed amounts must come from the current decree. Always say "not legal advice" and point to the notice and the authority's channel.

## 7. Pipeline and forecast
Stages are buyer actions with exit criteria; every open deal has a named buyer, a dated next step, a close date and an amount basis. Weekly review: stale (14+ days), no next step, close date pushed twice, single-threaded, older than twice the median won cycle. Forecast from your own stage-to-won history; report commit, likely and upside separately, compare with actuals. Coverage target = 1 / (stage-to-won rate). Definitions, hygiene rules, methods and the weekly template: `references/pipeline-forecast.md`.

## 8. Ethics and law
No false scarcity, invented testimonials, hidden fees, fabricated competing offers or claims you cannot document **[C]**. Outreach needs a lawful basis and an opt-out (GDPR/ePrivacy, LGPD, CAN-SPAM; ask counsel for campaigns). In B2G, equal treatment and anti-bribery rules apply; never share information about other bidders. CRM personal data is kept for a purpose and deleted when it ends.

## AI tells to avoid (check while writing, not after)
- Reflex openers: "I hope this email finds you well", "just following up", "circling back", "quick question" subject lines.
- Flattery that would fit any prospect; praise with no fact behind it.
- Feature lists not tied to the problem this buyer stated.
- Fake urgency: invented deadlines, "last spots", "price rises Friday".
- Em dashes, rule-of-three lists, inflated words (unlock, seamless, elevate).
- One cadence and template for every account.
Fix: one specific observation about this buyer, their numbers, one clear ask. Say what you chose and why in one line; a choice without a reason is removed. If a humanizer skill is installed, run it as a final pass on the finished text, then re-check facts and numbers it may have touched.

## 9. Output
Match the request: diagnosis report, call plan (agenda, questions, risks), qualification verdict with the missing facts, proposal draft, two objection replies with the risk of each, follow-up sequence, tender compliance matrix and clarification list, or a pipeline review table (deal, stage, next step and date, risk, action). Always end with: the single next action and its owner; the question to ask the buyer; evidence level of any method cited; what you could not verify (missing data, unverified legal detail, small sample).

## References
`references/deal-diagnosis.md` (symptoms, metrics, worked arithmetic) · `references/playbooks.md` (discovery, MEDDICC, objections, cadence, proposal, negotiation; SPIN in depth, rapport signals and ethical competitive intelligence in 7-9) · `references/b2g-procurement.md` · `references/founder-and-self-serve.md` · `references/pipeline-forecast.md` · `references/methods.md` · `references/BIBLIOGRAPHY.md`. Style variants (SPIN, Challenger, MEDDICC, value, founder, self-serve, high-ticket, B2G, cultural): `references/styles/README.md` picker. Related skills: copywriting, offers, pricing, growth-analytics, customer-support.
