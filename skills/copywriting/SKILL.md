---
name: copywriting
description: "Use whenever the task is words a customer reads to decide, buy or stay - landing and sales pages, homepage, headlines, value propositions, CTAs and button labels, app store descriptions (\"improve this app store description so more people install\"), checkout and form microcopy, error and empty states, onboarding and welcome e-mails (\"this email feels flat, make it compelling without hype\"), paywall text, tone of voice choices, and translating or adapting marketing text into another language (\"not word for word\"). Also diagnoses a page that gets traffic but no clicks or sales. Triggers include \"write copy for\", \"this copy is weak\", \"make it convert\", \"headline help\", \"what tone should we use\". Claims must be provable; EU consumer-law limits built in. Not for ad video scripts or hooks (ad-creatives), price, bonus or guarantee structure (offers), keyword briefs (seo-geo) or support replies (customer-support)."
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Copywriting

Copy is assembled, not written: the desire exists in the market; the piece channels it to the product. Start from research and diagnosis, write for people who scan, prove every claim, and keep the same name for the same thing from the ad to the receipt.

Evidence tags: **[C]** consensus, law or official docs · **[M]** serious but single or correlational · **[F]** practitioner rule, one test · **[X]** myth. **[1-SRC]** = single source. **[EU]** = EU consumer-law constraint. Not legal advice; sources in `references/BIBLIOGRAPHY.md`.

## 0. Project first
Read the current project's brand voice or style guide, glossary, design tokens, CLAUDE.md or AGENTS.md, legal terms and past approved copy before any rule here. Project rules win over this skill, including tone: a defined brand voice outranks `references/tones/`. Facts, prices and numbers come from the project, not memory.

## 1. Before writing: the 4-line diagnosis

1. Who reads, and what they would do without the product.
2. Awareness level and market sophistication (table below).
3. The one action this piece asks for.
4. The objection that blocks that action.

Missing data: ask the minimum or state the assumption. Know what the reader saw just before and reuse its words.

**Mine the voice of the customer first [M]:** reviews (yours and competitors'), support questions, ad comments, forums in the audience's language, quiz and post-purchase survey answers. Paste literal phrases into three columns: pain, desire, objection. Repeated phrases become headlines, bullets and FAQ.

**Awareness decides the opening [C]** (Schwartz, *Breakthrough Advertising*, 1966):

| Level | Reader knows | Open with | Avoid |
|---|---|---|---|
| Unaware | nothing of the problem | story, identity, curious fact | offer, price |
| Problem-aware | it hurts, not that a fix exists | the pain in their words | product name in headline |
| Solution-aware | a kind of fix exists | the mechanism and proof it works | re-explaining the problem |
| Product-aware | you exist, undecided | difference, proof, objections, guarantee | corporate text |
| Most aware | wants it, waits for terms | offer, price, real deadline, button | a long page |

**Sophistication [C]:** in a market that has heard every promise, a bigger promise breeds disbelief; show how it works (mechanism) and concrete quantities.

## 2. Core principles

1. **Clarity before cleverness.** Five-second test: shown the first screen for 5 s, can a person say what it is, who it is for and what to do? If not, rewrite before testing button colours. [C]
2. **Specific sells, generic slides off.** Replace adjectives with verifiable numbers, names, durations, units ("5 minutes a day", the real count). [C]
3. **One reader, one idea, one promise, one action per piece.** A second good idea becomes another piece. [M]
4. **Claim + evidence.** Every headline asserts something concrete; proof sits right under it. Promise only what you can prove: in the EU an unproven claim is a misleading practice. [C][EU]
5. **Feature → advantage → benefit.** Each bullet survives "so what?" and ends in a gain the reader recognises. [C]
6. **Answer each objection where it is born** (guarantee by the price). [M]
7. **Length follows awareness and objections, not dogma.** Boredom and repetition are the problem, not length. [M]
8. **People scan** (about 20% of words read, NN/g 2008): inverted pyramid, informative first words in headings and links, 1-3 line paragraphs on mobile. [C]
9. **Plain language serves everyone, experts included**; promotional "marketese" lowers usability. [C]
10. **Same name for the same thing everywhere** (ad, page, checkout, e-mail, receipt): renaming mid-journey breaks the information scent. [C]
11. **Persuasion in its honest form only:** one lever per claim, backed by true proof; dark patterns (fake urgency, confirm-shaming, hidden costs, fake reviews) are out (`references/persuasion.md`).
12. **The specific cures AI-sounding text.** If a competitor's name fits the sentence, rewrite it with a fact only this product has; run `humanizer` on long copy.
13. **Claims ladder:** can say (proven), not yet (built, not measured), never (outcome promises, invented numbers, fake reviews). Competitor facts only with source and date.

## AI tells to avoid (check while writing, not after)
- Em dashes as a tic: one per page at most.
- Stock verbs and adjectives: unlock, elevate, seamless, game-changer, supercharge, "transform your".
- Lists of three by reflex; use the real count.
- Empty taglines and openers like "In today's fast-paced world".
- Hedging and filler ("may help to", "really", "in order to").
- Fake enthusiasm and exclamation marks.
- Symmetrical "not X, but Y" lines.
- Generic benefits with no number, name or scene from the user's case.

Say what you chose and why in one line (audience, offer, platform, data); a choice without a reason is removed.

## 3. Page structure that rarely fails

Promise (specific) → proof it is real → mechanism → what is inside → verifiable social proof → offer and price → guarantee and what happens after paying → FAQ with real objections → button. [M] A value proposition: headline, 1-2 line subhead (for whom, how), three fact-backed bullets, real product image in use.

AIDA, PAS and relatives are scaffolding; none is proven better [F]. Order by awareness: `references/playbooks.md` 3.

## 4. Which reference to open
| Task | Read |
|---|---|
| A page or funnel underperforms (no clicks, no purchase, high bounce, e-mail not clicked, installs, checkout drop, generic text, weak translation, claim complaint) | `references/diagnosis-playbook.md` |
| Templates and routines: copy brief, headline generation, page order by awareness, proof inventory, e-mail sequences, microcopy, editing pass, safe A/B test | `references/playbooks.md` |
| Choosing or applying a tone of voice (plain, friendly, bold, expert, warm, playful, luxury, urgent) | `references/tones/README.md`, then one tone file |
| Buttons, forms, checkout, errors, empty states, e-mail deliverability, app-store listing | `references/ux-writing-checkout-email.md` |
| Copy shown to EU consumers (urgency, "free", reviews, discounts, pay button, AI personas) | `references/eu-consumer-law.md` |
| Persuasion levers, dark-pattern limits, engagement ethics, rhetoric and story | `references/persuasion.md` |
| Psychology claims, Cialdini with replication caveats, myths | `references/decision-psychology.md` |
| Classic copy principles (Ogilvy, Schwartz, Hopkins, Caples, Sugarman, Halbert) | `references/classics.md` |
| Another language, readability formulas, AI-text tells | `references/transcreation-readability.md` |
| Sources, ISBNs, status, date checked | `references/BIBLIOGRAPHY.md` |

Neighbours: `offers`, `growth-analytics` (sample size, test reading), `seo-geo`, `humanizer`, `customer-support`.

## 5. Workflow
1. Project first (0), diagnosis (1) and voice-of-customer phrases; pick the tone (`references/tones/README.md`).
2. Draft headline, subhead and CTA first; they must sell alone. Body by section 3; cut half, then again.
3. Final pass: truth of every claim, cut, AI tells, read aloud, legal check (`references/playbooks.md` 7).
4. Deliver the requested copy. Include variants when the user requests alternatives or is planning a copy test. For a failing page, run `references/diagnosis-playbook.md` before rewriting.

## 6. Output format

For a request for one piece, deliver one ready-to-use draft with one primary action. Keep the diagnosis and checklist as working steps. Add a short note only when requested or when missing evidence changes what can safely be published. For a review or test brief, use the relevant parts of this format:

```
Diagnosis (4 lines) + tone chosen (and why)
Copy by section: headline · subhead · CTA (+ support line) · sections
Why: one line per key choice, with the principle used
Variants (when requested or testing): 2-3 headlines or CTAs, each with the hypothesis it tests
Claims log: each number or promise -> source, or "needs proof"
Legal flags [EU] and open questions; what was not verified
(Other language: each passage with a faithful translation beside it)
```

## 7. Pre-delivery checklist

- [ ] Project voice and facts used; 4-line diagnosis done; assumptions stated.
- [ ] Passes the 5-second test; headline specific, proof right below; right awareness level.
- [ ] Top objection answered where it is born; guarantee next to price; one primary button.
- [ ] Testimonials real, attributable, with consent; zero unproven superlatives or outcome promises.
- [ ] Total price visible before the final button; final button states the payment obligation; no pre-ticked boxes; declining as easy as accepting [EU].
- [ ] Sentences mostly 12-18 words, none over 25; readability measured or "not measured".
- [ ] AI-tells block applied; read aloud.
