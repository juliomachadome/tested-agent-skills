# Diagnosis playbook: symptom, likely causes, check, fix

Use it top-down. Step 0 first: copy gets blamed for problems that are targeting, speed, price or tracking. Thresholds are **[F]** (practitioner starting points) unless tagged; the project's own last 4-8 weeks replace them. Tags as in SKILL.md. Measurement design (sample size, peeking, SRM) lives in the `growth-analytics` skill; price and offer structure in `offers`.

## Step 0: what do we know before touching a word?
| Question | Why it matters | If unknown |
|---|---|---|
| Who reads, and where did they come from (ad, query, e-mail, store search)? | The page must continue the promise they just saw | Get the ad or query text; open the page as that visitor, on a phone |
| Awareness level of that traffic (SKILL.md section 1) | Cold traffic needs problem and mechanism; hot traffic needs terms | State the assumption in the diagnosis |
| The one action wanted | Several equal buttons split attention | Name it; demote the rest |
| Proof available today (numbers, demos, reviews with consent, guarantee) | Copy cannot create proof; it can only show it | Build the proof inventory (`playbooks.md` 4) before rewriting |
| Page analytics: unique visits by source, scroll depth, CTA clicks, conversion by source and device, page speed | A rate without a denominator or a source split misleads | Report "not measured"; use a 5-second test with 5 people meanwhile |
| Traffic quality and load time | A mismatched or slow page loses people before the copy is read | Split by source; check mobile load before blaming words |
| Change calendar (ad changes, price, release, season) | Most "copy drops" are timing | Line changes up on a timeline |

Small samples: under about 30 conversions per cell, a rate moves by several points on noise alone. Read sessions and verbatims, do not declare a winner.

## Core arithmetic
- Conversion rate = conversions / visitors (state the denominator: sessions, unique visitors, or ad clicks).
- CTR = clicks / impressions (or CTA clicks / page visitors for on-page buttons).
- Worked funnel: 4,200 mobile visits, 336 CTA clicks, 63 purchases. Click rate 336/4,200 = 8.0%; click-to-purchase 63/336 = 18.8%; visit-to-purchase 63/4,200 = 1.5%. Moving click rate to 10% at the same 18.8% gives 79 purchases (+25%); moving click-to-purchase to 22% at the same 8% gives 74 (+17%). Fix the stage with the bigger relative gap first, but only after Step 0.
- **Sample before calling a headline test** (two-sided 5%, power 80%, pooled formula): baseline 3.0% to 3.6% (+20% relative) needs about 13,900 visitors per arm, 27,800 in all; at 400 visits a day that is about 70 days. Baseline 3.0% to 4.5% (+50%) needs about 2,500 per arm (about 13 days). Baseline 2.0% to 2.5% needs about 13,800 per arm. Small traffic: test bold changes (offer, structure, first screen), not synonyms; fix sample size and duration in advance, run whole weeks, never stop on a lucky day. See `growth-analytics` (`playbooks.md`, `experimentation-notes.md`). **[C]**

## Tree 1: the page gets traffic but few clicks on the CTA
| Likely cause | Check | Fix |
|---|---|---|
| Headline does not say what it is or for whom | 5-second test with 5 people from the target: what is it, who is it for, what do you do next? | Rewrite headline and subhead: result or object, reader, how (`playbooks.md` 2) |
| CTA below the fold or low contrast, or label says "Submit" | Scroll-depth and click map; mobile screenshot | One primary button in the first screen; label states the gain or next step |
| Promise bigger than anyone believes (sophisticated market) | Compare claim with what competitors say | Show mechanism and a concrete quantity; cut the superlative |
| No proof near the button | Count proofs in the first two screens | Move the best proof under the headline |
| Wrong traffic | Click rate by source | Fix targeting or the ad promise; copy cannot rescue it |

## Tree 2: clicks, but no purchase
Split by where they leave (checkout started? form started? price seen?).
| Cause | Check | Fix |
|---|---|---|
| **Message-offer mismatch**: the ad promised X, the page sells Y, or the price or format surprises | Read ad, page and checkout back to back; same names? | Align the words; same name for the same thing from ad to receipt |
| **Trust**: no real person or company, no terms, no contact, stock-photo proof | Ask 5 target users what they doubt; list trust signals present | Real product images, named policy, contact, verifiable testimonials with consent, payment-provider marks |
| **Friction**: long form, forced account, no guest option, many steps, slow mobile | Funnel by step; session recording sample; field count | Cut fields, one step per screen, show total before the last click |
| Objection unanswered | Support and chat questions before purchase | Answer it next to the price or button |
| Price shock (price first seen at checkout) | Drop at the price step | Show price where the offer is made; offer questions go to `offers` |

## Tree 3: high bounce within 5 seconds
Cause is usually mismatch between the first screen and the ad or query. Check the ad or search result next to the first screen: same promise, same words, same image? Check speed on a mid-range phone (LCP over 2.5 s hurts). Fix: echo the ad's wording in the headline, show the thing being sold, remove the cookie wall from covering the first screen, and test again with the same traffic source. **[M]**

## Tree 4: long page nobody scrolls
Scroll depth shows a cliff at a given block. Likely: a hero that reads as the whole story (false floor), a block that looks like a footer, or a dense wall of text. Fix: let the next section peek above the fold, descriptive subheads that carry the argument alone, shorter paragraphs, a mid-page button. If most people convert before the cliff, the page is fine; do not shorten for its own sake. **[M]**

## Tree 5: e-mail opened, no click
Opens are unreliable (mail-privacy features inflate them), so judge on clicks and replies. Checks: one purpose, first line carries the point, one primary link in plain words, the link text says what happens, the page it opens continues the e-mail's promise, mobile rendering, send time less important than relevance. Fix: single action, shorter, link text as a verb plus object, subject line honest to the content. **[M]**

## Tree 6: app store page views but few installs
Checks: first screenshots and the first lines of the description (what shows before "more"), ratings count and score, price or "in-app purchases" surprise, search term the visitor used versus the first screen. Fix: first screenshot states the main benefit in the user's words, first lines say what the app does and for whom, real numbers, no unprovable superlatives ("best", "number one"). Use store-supplied product page tests where available. See `ux-writing-checkout-email.md`. **[M]**

## Tree 7: checkout abandonment tied to microcopy
Look for: unclear price (tax, shipping, fees shown late), vague button, unclear trial or renewal terms, error messages that blame ("invalid input"), no reassurance on security or refund path, a field label that does not say why it is needed. Fix: total with taxes before the final click, button states the obligation, errors say what is wrong and how to fix it next to the field, one line on what happens after paying. Legal labels are not rewritten for style (`eu-consumer-law.md`). **[C][EU]**

## Tree 8: the copy sounds AI-generated or generic
Test: swap a competitor's name into the sentence; if it stays true, it is generic. Signs: stock phrases and inflated adjectives, three-item lists everywhere, "not just X, but Y" patterns, vague attributions, same sentence length throughout. Fix: replace with a fact only this product has (count, date, example, customer phrase), vary rhythm, run the anti-AI pass (`transcreation-readability.md`, `humanizer` skill). **[M]**

## Tree 9: the translated page converts worse than the original
Check first that traffic, offer and price are equal. Then: literal translation (calques), wrong form of address, text overflow on buttons, currency and date format, legal terms not localised, local competitors' vocabulary. Fix: transcreate with a native reader, test in market, keep a glossary. See `transcreation-readability.md`. **[M]**

## Tree 10: a complaint, regulator or platform flag about a claim
Do not defend; verify. List every claim in the piece, find the evidence file and date for each, remove or qualify what lacks it (comparative price, "free", urgency, testimonials, health or income outcomes). Check the rule for the country: EU `eur-lex` rules in `eu-consumer-law.md`; Brazil CDC and the CONAR code; US FTC endorsement guides. Keep a claims log from now on. Not legal advice; involve counsel for formal proceedings. **[C]**
