---
name: ad-creatives
description: Create, script, storyboard, review or analyse ad creatives for conversion - short vertical video for Reels, TikTok, Shorts and Stories, static images and carousels - covering the concept as the unit of testing, the first-3-seconds hook, structure by awareness level, formats and safe zones, sound and burned-in captions, test batches, reading hook/hold/CTR against purchases, fatigue and refresh, and ad policy plus EU law (fake urgency, testimonials, AI-generated faces and voices, stock and music licences). Use it whenever someone asks for ad ideas, hooks, a UGC-style script, "why is this ad not working", "make variations of this winner", a creative brief, or wants to render an ad by code, even without the word "creative". It produces the piece; budgets and kill rules live in paid-traffic, final words in copywriting, price/deadline claims in offers.
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Ad creatives

Not for organic reach without paid spend: use viral-content.

The ad buys the right click; the offer and the page make the sale. A creative that does not show the product and ask for an action is entertainment. Decide by purchases, cost per purchase and revenue per visitor; attention metrics explain *why*.

Evidence tags (untagged = a rule of this skill): **[C]** platform docs, law or replicated · **[M]** serious but single/old/modelled · **[F]** vendor data, practitioner rule · **[X]** myth · **[1-SRC]** single source · **[EU]** EU law. Re-check specs and policies officially if older than ~3 months.

## 1. The 5-line diagnosis (before any idea)

1. **Who** sees it (one person, one situation) and what they would do without the product.
2. **Awareness** in that channel and market **sophistication** (cold social traffic is usually unaware/problem-aware; retargeting is product-aware/most-aware).
3. **The single idea**, in one sentence that would fit on a poster.
4. **The proof** on screen (product in use, real count, demonstration).
5. **The one action and where the click lands**; the destination's first screen repeats the ad's image and phrase (information scent).

## 2. Core principles

1. **The concept is the unit of testing.** Hierarchy of impact: offer and audience → **concept** (angle × persona × awareness) → format → hook → body → CTA → cosmetics. Test the top first. [F, consistent with platform guidance]
2. **Write each concept in one line:** "for [persona] who [situation], show [proof] in [format], opening with [hook], asking for [action]". Two creatives with the same line are one creative.
3. **Cosmetic variation is not a new creative.** A new first line on the same body is iteration of a winner, not a starting batch. [C]
4. **Diverse batch, not big batch.** 3-5 genuinely different creatives per group (TikTok); on small budgets 3-6 concepts in 2 formats beat 25 hook swaps. [C]
5. **Proposition in the first 3 s, hook resolved by ~6 s** (TikTok); brand early (Google ABCD). Image, text and voice say the same at frame 0, which works as a still thumbnail. [C]
6. **The hook promises only what the body delivers.** Unpaid bait kills retention, attracts non-buyers and breaks "misleading tactics" policies. [C]
7. **Never assert a personal attribute of the viewer.** "You're bad at…" hits Meta's personal-attributes policy; "Do you understand but freeze when speaking?" asks about a situation. [C]
8. **Product early and in use;** ask for the action on screen and in voice; the end card button matches the ad's CTA. [C]
9. **Design for sound on and off;** burned-in captions (max 2 lines, high contrast, inside the safe zone). "85% watch without sound" is an outdated feed statistic. [C][X]
10. **Never generate by AI:** product screens, results, testimonials, a person presented as a customer or expert. Product and screens are always real. Synthetic voice is "narration", never a named person, disclosed where required. [C][EU]
11. **Ideas can be remade; others' files, music, faces and brands cannot.** Re-uploading a viral video with a new CTA infringes copyright. [C]
12. **One name and one phrase from ad to post-purchase;** the creative reuses the method name and core phrase; no price, guarantee or deadline sentence is born in the creative (it comes from offers/copy).

## 3. Which reference to open

| Task | Read |
|---|---|
| Angles, hook types, video structure by awareness, durations, rhythm, end card, formats, story and neuromarketing caveats | `references/concepts-hooks-structure.md` |
| Specs, aspect ratios, Meta 9:16 safe zone, export settings, sound mix, music | `references/specs-safe-zones-audio.md` |
| Test batches, metric definitions, reading results, fatigue and refresh, batch report | `references/testing-fatigue.md` |
| "Why is this ad not working": Step 0, symptom trees, metric formulas with worked numbers | `references/diagnosis-playbook.md` |
| Routines: brief, concept sprint, UGC brief and rights checklist, test batch, iteration ladder, weekly review, refresh calendar, AI disclosure checklist | `references/playbooks.md` |
| Ad policy and EU law: deceptive practices, price in ads, urgency, testimonials, creators, AI disclosure, stock licences | `references/policy-and-law.md` |
| Producing video by code without freezing the machine; adapting to a new country | `references/production-and-localisation.md` |
| Sources with verification status (V/P/S/U) | `references/BIBLIOGRAPHY.md` |

**Rule of thumb:** numbers or a "why": `diagnosis-playbook.md` (Step 0 first); make/plan/brief/refresh: `playbooks.md`; "may I say or show this": `policy-and-law.md`. Budget and kill rules: paid-traffic.

## 4. Workflow

0. **Project first.** Read the current project's CLAUDE.md or AGENTS.md, brand and glossary notes, persona and offer documents, existing creative library and credits file, and past batch reports. Project rules override this skill. With none, ask once: product, audience, country, language, offer owner, destination URL, real material, budget; state assumptions.
1. Diagnosis (section 1); collect what may be said about price, deadline and guarantee from the offer owner.
2. Concepts: one line each, different from each other; pick 3-6 for the batch.
3. Script and storyboard per concept as a table: `time | line in the audience's language | faithful translation | on screen`.
4. Stills first (one per scene, one mid-transition) to fix overflow and contrast; render one piece, check, then the rest.
5. Law and policy checklist; licences logged in a credits file.
6. Final file check (duration, resolution, loudness, captions in the safe zone, cover = first frame, no invented data, price/date equal to the page's).
7. After publishing: batch report with decision (scale / iterate / kill) and next hypothesis; read results via `diagnosis-playbook.md` Step 0. With under ~10 purchases per ad say "not enough volume to conclude".
8. Say what was not verified: specs older than ~3 months, AI-disclosure rules (EU AI Act art. 50 pending), sources marked S or U in `references/BIBLIOGRAPHY.md`.

## 5. Output format

```
Diagnosis (5 lines)
Concepts: one line each, with the hypothesis
Per creative: script table (time | line | translation | on screen), frame-0, CTA, destination URL + first-screen requirement, tracking ID = file name
Short (6-10 s) cut planned for the winner
Law/policy flags and licences used
```

## AI tells to avoid (check while writing, not after)
- Em dashes as a tic in captions and voice-over.
- Stock verbs and adjectives: unlock, elevate, seamless, game-changer, supercharge, "transform your".
- Lists of three by reflex; use the real count.
- Empty taglines and "In today's fast-paced world" openers; hedging and filler.
- Fake enthusiasm and exclamation marks.
- Symmetrical "not X, but Y" hooks.
- Generic benefits with no number, name or scene from the user's case.
- AI-looking visuals: plastic skin, over-saturation, uncanny hands, stock-like composition.
- The same hook formula in every variant.
- Captions that restate what the video already shows.

Say what you chose and why in one line (audience, offer, platform, data); a choice without a reason is removed.

## 6. Checklists

**Before the script**
- [ ] 5-line diagnosis, including the click destination.
- [ ] Concept line differs from the others in the batch.
- [ ] Price, deadline, guarantee wording and every number come from the offer owner or project documents.

**Script and storyboard**
- [ ] Frame 0: image, big text and voice say the same; works as a still.
- [ ] Proposition by 3 s; real product on screen early.
- [ ] One idea; each line leads to the next; hook paid by the body.
- [ ] CTA on screen and in voice, equal to the ad button and the destination's first screen.

**Law and policy**
- [ ] No outcome promises, absolute terms, before/after.
- [ ] Price and date identical to the page; no strike-through or %, or the 30-day line legible [EU].
- [ ] Only real deadlines; no countdown graphics.
- [ ] No person presented as customer or expert who is not; stock people only as background; releases stored.
- [ ] Nothing of the product AI-generated; AI disclosure switched on where required.
- [ ] Music and images licensed and logged; no personal attribute asserted.

**Final file**
- [ ] 9:16 1080×1920 (or the placement's ratio), 30 fps, H.264 + AAC, faststart.
- [ ] Text and captions within the safe zone; checked in the ads-manager preview.
- [ ] Burned-in captions plus `.vtt`; audio checked.
- [ ] Cover, caption, tracked link, expiry date in file name.
