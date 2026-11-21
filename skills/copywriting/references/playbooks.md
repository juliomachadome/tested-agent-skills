# Playbooks: templates and routines

Practical routines. Tags as in SKILL.md. Tone choice is in `tones/README.md`; classic principles in `classics.md`; button, form and e-mail details in `ux-writing-checkout-email.md`. Project rules and brand voice win over anything here.

## 1. Copy brief (fill before drafting)
```
Product: what it is, in one plain sentence
Reader: who, situation, what they do today without it (their words)
Awareness level / market sophistication:
Source of traffic and what they saw just before:
The one action:
Top objection (and the proof that answers it):
Proof available (number + source + date; demo; consented testimonial):
Offer and terms (price incl. tax, renewal, guarantee, deadline if real):
Tone: pick from tones/ or the project's voice guide; 3 words + 3 words to avoid:
Constraints: length, character limits, legal text that cannot change, languages:
Success measure and the test plan:
Open questions / assumptions:
```
Missing line = ask once, or write the assumption and mark it.

## 2. Headline: generate, select, test
1. Write 20+ options before judging; mix types: result, object plus reader, question, how, number, news. Do not edit while generating. **[F]**
2. Score each 0-2 on: specific (a number, a name, a duration)? true (proof on hand)? reader-centred? clear in 5 seconds with no context? matches the ad or query words? fits the tone? Drop any that fail "true".
3. Keep 3-5; read them aloud; pair each with a subhead that supplies the how and for whom.
4. Test the two most different ones (not two synonyms), after the sample check in `diagnosis-playbook.md`. Caples-era tests found headline differences of multiples; direction is useful, magnitudes are not portable. **[M]**
5. Log the hypothesis ("specific number beats the benefit statement for cold traffic") and the result, win or lose.

## 3. Landing page section order by awareness level
| Level | Order |
|---|---|
| Unaware | Story or identity hook, the problem named, why it persists, mechanism, product, proof, one soft action |
| Problem-aware | Pain in the reader's words, cost of leaving it, mechanism, product in use, proof, offer, FAQ, button |
| Solution-aware | Mechanism and difference first, proof it works, what is inside, comparison, offer, guarantee, button |
| Product-aware | Short headline, proof, objections answered, offer with total price, guarantee, button |
| Most aware | Offer, price, real deadline if any, button; a long page hurts |
Always: first screen says what it is, for whom, and what to do; button repeats after each major proof; the page after the click continues the promise.

## 4. Proof inventory
| Type | Rule | Where it sits |
|---|---|---|
| Testimonials | Written consent kept; real name or described role as agreed; specific outcome; no incentive hidden; verification rule published | Near the claim they support and near the price |
| Numbers | Source, date, method in the claims log; round honestly | Under the headline, in bullets |
| Demo or screenshot | The real product in use, current version | Hero and mechanism |
| Third-party mentions, ratings | Only real and current; link to the source | Near trust-sensitive moments |
| Guarantee and policy | Quote the real policy; short fact near the price, not a headline | Price and checkout |
Empty inventory means the first job is collecting proof (ask 10 users, run a small measured test), not writing around it. Material connection (gift, payment, affiliate) is disclosed next to the endorsement: EU `eu-consumer-law.md`, US FTC endorsement guides (16 CFR 255), Brazil CONAR code on testimonials (art. 27 section 9). **[C][EU]**

## 5. E-mail sequence templates (honest urgency only)
Each e-mail: one purpose, one primary link, plain sender, plain subject.
- **Welcome (day 0):** confirm what they signed up for, deliver the promised item first, one next step, how to reach a human, how to leave.
- **Onboarding (days 1, 3, 7):** one win per message tied to the product's activation event; e-mail 2 removes the most common blocker (from support data); e-mail 3 shows a real result of a similar user (consented). Stop the sequence when the action is done.
- **Win-back (after 30-60 days quiet):** say what changed or what they missed, one reason to return, an easy way to stop messages. A discount only if it exists as a real, priced offer.
- **Launch or deadline:** the real date and time with time zone in the first line; reminders only at true milestones; the deadline never extended without saying so; no resetting timers. A short close e-mail is fine: "closes tonight 23:59 CET". **[EU]**
Check: consent and unsubscribe, sender identity, subject matches the content, mobile preview, link text names the destination. Consent rules: the privacy law of the data subject's country (official regulator pages) skill.

## 6. Microcopy patterns
- **Buttons:** verb plus object plus gain ("Start my free week", "Save changes"); payment buttons carry the legal obligation wording of the market; support line beside it answers the fear of the moment ("Cancel anytime in settings").
- **Errors:** what happened, why if useful, what to do, next to the field; never blame, never code-only. "Enter a date like 24/03/2026."
- **Empty states:** what goes here, why it helps, one action. "No lessons yet. Pick your level to see the first three."
- **Success states:** confirm the result and the next step; keep the same name the user clicked.
- **Loading and waits:** say what is happening and roughly how long.
- **Consent and prices:** total with tax before the last click; no pre-ticked boxes; decline as visible as accept.

## 7. Editing pass (in this order)
1. **Clarity:** what, for whom, what next in 5 seconds; one idea per section.
2. **Specificity:** each adjective becomes a number, name or example, or goes.
3. **Claims check:** every number and promise against the claims log; unprovable superlatives out; comparison prices real.
4. **Readability:** sentences mostly 12-18 words, none over 25; measure with a tool for that language or write "not measured".
5. **Tone check:** matches the chosen tone file and the project voice; no tone shifts in errors and legal text.
6. **AI-tells removal:** stock phrases, uniform rhythm, empty intensifiers, rule-of-three habit, em-dash overuse; read aloud; run `humanizer` on long pieces.
7. **Legal pass:** urgency, "free", reviews, withdrawal wording, pay-button label, country rules.
Cut half first, then half again; keep a copy of the original.

## 8. A/B test of copy, safely
1. Hypothesis in one line: "Because X (evidence), changing Y will raise Z for audience A."
2. One primary metric (purchase or lead), guardrails (refund rate, complaints, unsubscribes, support tickets).
3. Sample and duration fixed before launch (`diagnosis-playbook.md` arithmetic); whole weeks; random split; check for ratio mismatch.
4. Both variants pass the claims and legal check; a variant must not use a claim you would not publish permanently.
5. Do not peek and stop; do not run many variants on low traffic.
6. Read by source and device; a win on one segment only is a hypothesis for the next test.
7. Record result, effect with interval, and what you will do. Under the traffic needed, use qualitative checks (5-second test, interviews) instead of a fake test.
8. SEO: avoid cloaking and use canonical correctly when testing indexed pages (`seo-geo`).
