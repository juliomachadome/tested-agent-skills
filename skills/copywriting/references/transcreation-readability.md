# Transcreation, readability and AI-text tells

## Writing in another language
- **[C] Never translate word for word.** Recreate the message with the target language's logic: word order, idioms, politeness, what sounds too salesy. A calque is the first scam signal for a native reader.
- Decide the form of address (informal/formal) once per brand and keep it everywhere, including automated e-mails and errors. Legal text may use its own register.
- **[C] Plurals and cases are not "singular + s".** Many languages have 3-4 plural forms and inflect nouns after numbers and prepositions. Text with variable numbers uses Unicode CLDR plural categories (`one`, `few`, `many`, `other`) via ICU MessageFormat; never concatenate number + word.
- **[C] Numbers, currency and dates follow the locale:** decimal separator, currency position and spacing, date order, month capitalisation (CLDR).
- **[C] Text grows in translation.** Labels up to 10 characters in English can double or triple; long sentences grow 30% or more. Write buttons that fit and check on narrow screens. (W3C Internationalization)
- Grammatical gender: where verbs or adjectives mark gender, prefer neutral constructions (present tense, imperative, nouns) to guessing the reader's gender.
- Legal words have exact translations: "free", "sale", "guarantee", "withdrawal" carry legal weight per country. Use the local legal term, not the cognate.
- When the approver does not read the language: deliver each passage with a **faithful** translation beside it (not an improved version), plus a note where the literal translation loses the tone. Validate terms by research in the language (how competitors and customers write), not only from memory.

## Readability: measure without fooling yourself
- **Flesch Reading Ease (English only):** 206.835 − 1.015 × (words/sentence) − 84.6 × (syllables/word). 60-70 = plain English; general-audience sales text should stay above 60. (Flesch 1948)
- **[C] A formula for one language does not fit another.** Each language has its own because word length differs: Portuguese uses an adapted Flesch (constant 248.835); Spanish uses Fernández Huerta or Szigriszt-Pazos/INFLESZ; other languages have their own tools (for example Jasnopis and FOG-PL for Polish). Never run English Flesch on another language.
- **[C] Formulas measure surface, not comprehension.** Short confusing text passes; you can "win" by chopping sentences. Use as an alarm; confirm by reading aloud and, ideally, with a person from the audience.
- Practical targets: average 12-18 words per sentence, none above 25; one idea per sentence; verbs instead of abstract nouns ("pay", not "effect payment"); active voice; reading age about 12-14 for a general audience. Government content guides go further (sentences up to 25 words, reading age 9).
- **[F] "Grade 5-7 copy converts more"** comes from one vendor's correlational benchmark of landing pages (2024). Direction plausible, causation unproven. [1-SRC]
- Legal text is simplified by sentence, not by cutting content, and isolated on its own line, away from persuasive body copy.

## Copy that does not sound machine-written
Source of the tells list: Wikipedia "Signs of AI writing" (WikiProject AI Cleanup), also the basis of the `humanizer` skill.
- Always cut: openings that "set the scene in today's landscape"; "it's not just X, it's Y"; reflexive triads of adjectives or items; conclusions restating what was just said; "it's worth noting"; inflated vocabulary (crucial, robust, comprehensive, journey, dive into, elevate, unlock, empower); rhetorical questions answered immediately; chains of long dashes; Title Case headings where the language does not use them; emoji as bullets.
- **The cure is the specific:** a machine sentence fits any product; a good one fits only this one.
- **Rhythm:** vary sentence length; read aloud and rewrite where you stumble.
- **Tells differ by language.** What signals AI in English (long dashes, title case) can be normal punctuation elsewhere, and each language has its own clichés: list them for the project's language before reviewing.

See the "AI tells to avoid" block in SKILL.md; check it while writing.
