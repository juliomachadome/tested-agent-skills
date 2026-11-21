# Ethical persuasion inside copy

Principles are used in their honest form: they help a reader who would genuinely benefit decide faster. They never replace a true claim. Evidence tags as in SKILL.md. Never quote the books; use the idea. Source list: `BIBLIOGRAPHY.md`. Tone variants: `tones/README.md`.

## 1. Frameworks and what they give a copywriter

| Source | Core idea | Use in copy | Confidence / caveat |
|---|---|---|---|
| Cialdini, *Influence* (new ed. 2021) | Seven levers: reciprocity, commitment/consistency, social proof, authority, liking, scarcity, unity | Table in section 2 | [M] Field studies exist but effects vary by context; several lab effects replicate weakly |
| Cialdini, *Pre-Suasion* (2016) | What the reader attends to just before the ask shapes the response | Order the page: first screen frames the problem or the shared goal the offer answers; the ad's promise must match the landing headline | [M] Priming chapters lean on weak-replication research: treat as "relevance and sequence", not as a trick |
| Kahneman, *Thinking, Fast and Slow* (2011) | Fast intuitive mode vs slow checking mode; framing, anchoring, loss aversion | Headline, image, hierarchy pass the fast mode; price, proof, guarantee pass the slow mode. Frame honestly (gain or loss, both true) | [M] The priming chapter failed replication; the author acknowledged it. Prospect theory itself is solid |
| Fogg Behavior Model (2009 paper; *Tiny Habits*, 2019) | Behavior happens when motivation, ability and a prompt coincide (B=MAP); when it fails, make it easier before making it more exciting | Cut fields and steps, shrink the first ask, put the prompt (button) at the moment of motivation, write microcopy that removes doubt | [M] Practitioner model with wide use; little direct experimental validation of the exact equation |
| Eyal, *Hooked* (2014) | Trigger, action, variable reward, investment loop for habit-forming products | Onboarding that gets one real win fast; investment steps that make the product better for the user | [M] Ethics: see section 4 |
| Ariely, *Predictably Irrational* (2008) | Anchoring, decoy effect, zero-price effect, social vs market norms | Show a reference price that was really charged; plan comparison tables; be careful with "free" | [M] Several Ariely results are contested; one co-authored honesty study was retracted in 2021. Use as direction, test it, never cite as proof |

## 2. Mapping each lever to the page

| Lever | Headline | Proof | Offer | CTA and microcopy | Stop line |
|---|---|---|---|---|---|
| Reciprocity | "Free X you can use today" only if truly free | A real sample, template, calculator | Free first step with no card | "Get the checklist" (no hidden signup) | "Free" that needs a card or forces a trial |
| Commitment | Ask for a small, voluntary, relevant step | The user's own quiz answer reflected back | Start small, upgrade later | "Start with 1 lesson" | Using a past answer to shame ("you said you cared") |
| Social proof | Real count, with unit and date | Specific named reviews, peers like the reader, near the price | Most chosen plan only if it is true | "Join 4,210 learners" (current, sourced) | Invented or rounded-up numbers, fake "just bought" toasts, bought reviews |
| Authority | Credential in the subhead | Cited study, named expert, regulator or standard | Guarantee backed by a real policy | Link to method or credentials | Fictional expert or AI persona posing as human |
| Liking | Reader's own words (voice-of-customer) | Founder or team with a real face and story | Warm, plain terms | Friendly, first-person button text | Fake intimacy, guilt trips, mock human chat |
| Scarcity | Only a limit that exists ("cohort closes 12 Jan") | Visible count that is real | Genuine cap or deadline | Deadline next to the button | Resetting timers, fake stock of a digital product |
| Unity | "For night-shift nurses" | Stories from the same group | Group pricing that exists | "Join the group" | Manufactured us-vs-them |
| Anchoring and decoy (Kahneman, Ariely) | Show value in the real unit | Price per day or per lesson, true | Higher plan shown first only if it is sold | Highlight the plan that fits most | Fake "was" price never charged |
| Fogg ability | Name the effort ("2 minutes") | Demo of the actual first step | Shortest path to the first win | One field, one button, error text that tells the fix | Hiding steps to inflate conversion |
| Fogg prompt | Match the ad's promise | Context the reader just saw | Reminder tied to a real event | Prompt at the moment of motivation | Notifications that exist only to pull usage |

Rules of thumb:
1. One lever per claim; stack proof, not tricks.
2. Strongest lever near the decision (price, pay button), weakest in the hero.
3. Every lever is backed by a log entry in the claims log (source, date).
4. Test, do not assume: levers have context-dependent effects. Pair each with a hypothesis in the variants block.
5. Cost of being wrong is asymmetric: a deceptive element can make the whole page illegal; a missing lever only costs some conversion.

## 3. Hard limits: dark patterns

Treat these as constraints, not style choices. Legal references (verify current text before relying; this is not legal advice):

- **EU Unfair Commercial Practices Directive 2005/29/EC**: misleading actions and omissions, aggressive practices, and the blacklist (Annex I) with always-banned items such as false "limited time" claims and fake urgency. Guidance document by the European Commission (2021) lists examples.
- **EU Digital Services Act (Regulation 2022/2065), Art. 25**: online platforms may not design interfaces that deceive or manipulate or otherwise distort users' ability to make free and informed decisions (applies to platforms; the UCPD covers traders generally). It applies to online platforms and does not apply where Directive 2005/29/EC or the GDPR already covers the practice (art. 25(2)); for an ordinary shop or landing page, the UCPD blacklist is the main limit.
- **FTC staff report "Bringing Dark Patterns to Light" (Sept 2022; URL not reachable on 2026-11-16, not re-read)**: catalogues disguised ads, false urgency, hidden fees, obstructed cancellation, forced continuity and confirm-shaming as potential deception under the FTC Act (US).
- **Brazil Consumer Defense Code (CDC, Lei 8.078/1990)**: right to adequate, clear information on quantity, characteristics, quality, taxes and price, plus protection against misleading or abusive advertising (art. 6 III-IV); advertising must be identifiable as such, and the advertiser keeps the factual, technical and scientific data behind the message (art. 36); misleading advertising, including by omission of an essential fact, and abusive advertising are banned (art. 37, pars 1-3); the burden of proving the claim is on the sponsor (art. 38); a sufficiently precise ad binds the supplier and becomes part of the contract (art. 30); abusive practices include tying products, sending unrequested products or services, raising a price without cause and exploiting a person's weakness (art. 39 I, III, IV, X). Read on normas.leg.br 15/11/2026.

Patterns to refuse or rewrite:
1. **Fake urgency or scarcity**: countdown that resets, "3 left" with no stock.
2. **Confirm-shaming**: decline buttons that insult ("No, I like paying full price").
3. **Roach motel**: easy sign-up, hidden or multi-step cancellation. Cancel path must be as visible as buy.
4. **Hidden costs and drip pricing**: total shown late; pre-ticked add-ons; auto-renewal buried.
5. **Trick questions and misdirection**: double negatives, visual weight inverted to hide the real choice.
6. **Fake social proof**: invented reviews, fabricated live-activity pop-ups, undisclosed incentivized reviews.
7. **Nagging and forced action**: repeated prompts, forced account creation before value.
8. **Disguised ads and fake humans**: ads that look like content; AI personas claiming to be real people.

## 4. Engagement ethics (Eyal and the critique)

Eyal himself separates a "facilitator" (would use the product, believes it helps others) from a "dealer" and proposes a manipulation test: would I use it, will it materially improve users' lives. Critics (for example Schull, *Addiction by Design*, 2012, on machine gambling; and the design-ethics movement around "humane technology") argue that variable rewards and investment loops can exploit vulnerabilities regardless of intent.

Working rules:
1. Build habit loops only where the habit serves the user's stated goal (learning, health, finances), and measure that outcome, not just return visits.
2. Variable rewards: no reward schedules tied to spending money; no streak mechanics that punish a missed day with loss of paid value.
3. Notifications: user-controlled, specific, silenceable in one step; never guilt copy.
4. Vulnerable groups (minors, compulsive behavior, health): stricter, default to no loops.
5. If the honest version of the screen would make users leave, the product or offer has a problem; copy cannot fix it.

## 5. Quick review prompt

For each persuasive element ask: (1) true? (2) would the reader feel respected if they saw how and why it is there? (3) is leaving or declining as easy as accepting? (4) does a regulator's blacklist cover it? Any "no" means rewrite.

## 6. Rhetoric and story applied to pages (Aristotle, Heinrichs, Gallo, Sinek)
Principles restated; chapter cites point to the owner's copies. Heinrichs' file is a condensed chapter summary, so those points are weaker than the others (status in `BIBLIOGRAPHY.md`).

**Aristotle, *Rhetoric* (Spanish edition) [C as theory, M as evidence of effect]**
- **Three sources of proof (I.2):** the speaker's character, the listener's state of mind, the argument itself. A page needs all three: trust signals, the emotional state the reader arrives in, and a claim with proof.
- **Credibility has three parts (II.1):** sound judgement, integrity, goodwill toward the listener. A reader who doubts any one stops trusting. On a page: specifics that show you know the problem (judgement); real limits, full price and plain terms (integrity); the reader's benefit before yours, and a "not for you if..." line (goodwill).
- **Emotion changes the verdict (II.1, II.11):** the same facts are judged differently by someone anxious, friendly or angry, so write for the state the reader is in and move it only toward calm and confidence. Aristotle separates emulation (the wish to reach something peers already have and that is reachable) from envy; show reachable results of people like the reader, not status envy.
- **Enthymeme (I.2, II.22):** persuade with a short argument built on premises the audience already holds, leaving the obvious step out; long chains lose a general audience. Premises come from knowing the real facts of the case, so research the reader's beliefs and the true numbers first, then state the claim on a premise they already accept.
- **Audience by age and circumstance (II.12-17):** his sketches of the young, the old and the rich are dated and stereotyped; use them only as a prompt to ask what each segment fears, trusts and can reach.
- **Delivery matters because audiences are imperfect (III.1):** hierarchy, rhythm and format earn attention but come after substance.

**Heinrichs, *Thank You for Arguing* (chapter summary only) [M]**
- **Decorum (ch. 5):** match the register, vocabulary and dress the audience expects; copy the reader's own words, never fake slang.
- **Ethos kit (ch. 6-8):** shared values, practical wisdom (shows you know what to do, not only what to feel), and disinterest. A tactical admission of a flaw or of who should not buy reads as disinterested and raises trust; use it only when true.
- **Pathos (ch. 9):** a vivid, specific story moves mood better than announcing the emotion; restraint beats exaggeration, and naming the feeling you want in advance triggers resistance.
- **Tense of the argument (ch. 11, 26):** decisions are about the future and the advantage of the listener. Sell in the future tense of choice; blame (past) and praise (present) belong to other genres.
- **Fallacy check (ch. 14):** false comparison ("natural" means safe), a bad or lone example as proof, slippery slope. Run every claim in the claims log through it.
- **Timing (kairos, ch. 26):** a message lands when the reader is open to change: tie copy to trigger events (a new job, a failed attempt) rather than to the calendar.

**Gallo, *The Storyteller's Secret* (lessons at the end of chapters) [F]**
- **Hero, villain, conflict (ch. 9, 22):** the reader is the hero, the problem or the old way is the villain, the product is the tool. Name the villain in the first screen.
- **Struggle arc (ch. 5, 6, 28):** a believable story shows a real obstacle, the turn, and the result; skipping the difficulty makes it feel like an ad.
- **Concrete detail from your own problem (ch. 13):** an origin story that explains why you built it works when it is specific and true; never invent one.
- **First sentence and rule of three (ch. 18, 19):** one strong opening line that carries the whole idea; three beats are easy to follow and to remember.
- **Simplicity (ch. 22, 23):** plain words a child could follow; be able to tell the story in about 60 seconds.
- **Analogy and surprise (ch. 11, 12, 21):** an analogy explains an unfamiliar feature faster than statistics; a small, honest surprise earns a second look.
- **Caution:** the book leans on brain-chemistry claims (oxytocin, cortisol) as proof that stories work. That link is popular science with weak replication; do not cite it. Treat story as a format to A/B test, not as a guaranteed lever.

**Sinek, *Start with Why* [F practitioner, use with caution]**
- **Manipulation vs inspiration (ch. 2):** price cuts, promotions, fear, peer pressure, aspiration and novelty all work in the short term and train buyers to wait for the next discount (his carmaker-rebate case). Good warning for discount-led copy.
- **Golden circle (ch. 3):** a check for the hero and the about page: does the piece say why the company exists before listing features? Useful for brand copy and for readers who already know the category.
- **Limits:** the case studies (Apple, the Wright brothers) are after-the-fact stories picked from winners, the "limbic brain has no language" mapping in ch. 4 is an outdated simplification, and no test shows why-first beats a specific benefit for conversion. In direct-response copy, specificity and proof still lead.
