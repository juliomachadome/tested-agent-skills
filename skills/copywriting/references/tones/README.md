# Tones of voice: how to pick and apply one

Voice is who the brand is and changes little; tone is how that voice is set for this reader in this moment (Mailchimp Content Style Guide, voice and tone section). Tone is the way the organisation shows how it feels about its message (NN/g). One brand can use several tones across a journey: playful on the home page, plain and calm on a payment error.

## How to choose (in this order)
1. **The project's own voice wins.** Read brand docs, style guide, glossary, past approved copy, CLAUDE.md or AGENTS.md. If they define voice, stay inside it and use the tone files below only to fine-tune.
2. **The request.** If the brief names a tone ("friendly but serious"), place it on the matrix and open the closest file.
3. **The reader's state, not the brand's mood.** Anxious, angry, in a hurry, spending money, in pain: move toward plain and warm whatever the brand voice is. Jokes in an error or a refusal read as contempt.
4. **The stakes.** Money, health, legal, safety and children push toward plain-trustworthy and expert-technical. Entertainment and low-stakes consumer apps allow more play.
5. **The market.** Check how local competitors and customers write in that language; register differs by country. Tone does not translate word for word (`../transcreation-readability.md`).
6. When unsure, pick the plainer option and add one human line; test variants (`../playbooks.md` 8).

## Tone matrix (after NN/g's four dimensions)
Place the piece on each spectrum; most pieces sit near the middle on at least two.
| Dimension | One end | Other end | Rule of thumb |
|---|---|---|---|
| Formal - casual | Formal: full sentences, titles, no contractions | Casual: contractions, first names, short | Match the reader's own register; formal for law and money, casual for peer-to-peer apps |
| Serious - playful | Serious: direct treatment of the subject | Playful: attempts at humour | Humour only where nothing is at stake for the reader; NN/g counted attempts at humour, not whether they landed |
| Respectful - irreverent | Respectful: deference to subject and reader | Irreverent: cheeky about the subject or category | Irreverence aims at the category or status quo, never at the reader |
| Matter-of-fact - enthusiastic | Dry facts | Excitement about the product | Enthusiasm needs proof next to it; high excitement with no facts reads as hype |

| File | Typical position | Fits |
|---|---|---|
| `plain-trustworthy.md` | formal-to-neutral, serious, respectful, matter-of-fact | finance, health, legal, public service |
| `friendly-casual.md` | casual, light, respectful, warm | consumer apps, onboarding |
| `bold-provocative.md` | casual, serious-to-playful, irreverent, enthusiastic | challenger brands |
| `expert-technical.md` | neutral, serious, respectful, matter-of-fact | B2B, developers |
| `warm-empathetic.md` | casual-neutral, serious, respectful, gentle | support, care, education |
| `playful-witty.md` | casual, playful, irreverent, enthusiastic | entertainment, games |
| `luxury-minimal.md` | formal, serious, respectful, restrained | premium goods and services |
| `urgent-direct-response.md` | casual, serious, irreverent, enthusiastic | info-products and launches |

## Rules for every tone
- Tone never changes facts, legal wording or the price shown. Pay buttons, withdrawal wording and mandatory notices stay as the law or platform requires.
- The same message must stay true if the style is stripped away.
- Accessibility: plain structure and clear labels in every tone; humour and wordplay must not be the only carrier of meaning (screen readers, cognitive load, non-native readers).
- Translation: jokes, idioms and irreverence rarely survive; write a local version, do not translate.
- Record the chosen tone, three words to use and three to avoid in the brief (`../playbooks.md` 1).

Sources: NN/g, The Four Dimensions of Tone of Voice (Kate Moran, 2016, reviewed 2023); Mailchimp Content Style Guide, Voice and Tone; GOV.UK content design guidance on writing for users. Details in `../BIBLIOGRAPHY.md`.

## Rules that always apply
1. **The project's voice guide wins.** When a brand voice guide exists, follow it and say so in the answer ("following the brand guide, not a generic tone"); the files here only fill gaps.
2. **Facts do not change with tone.** Price, date, renewal, how to cancel and what the user keeps stay identical in every version; style never hides or softens them.
3. **Count with a tool.** Character and word limits are checked by running a count (for example `len()` in Python or the editor's counter), not by hand; report the counted numbers.
4. **Playful or cheeky versions carry two checks:** accessibility (screen readers read emoji names; jokes and slang can confuse) and translation (wordplay rarely survives; keep a plain fallback).
