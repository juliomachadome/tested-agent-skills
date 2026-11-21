# UX of AI features

## Contents
1. Principles
2. Sources and citations
3. Confidence and abstention
4. The model proposes, the person decides
5. Latency and streaming
6. Wrong answers and recovery
7. Tone and anthropomorphism
8. Microsoft HAX 18 guidelines (checklist)
9. Checklist
10. Sources

## 1. Principles
People over-trust fluent output and rarely verify. The interface must make checking cheap, make uncertainty visible and keep the person in charge. These are design hypotheses backed by NN/g and academic studies; test them on your users.

## 2. Sources and citations
- Put the citation next to the claim it supports, in a distinct style, with a descriptive label (title and section, not "Source") and a deep link to the exact passage. NN/g's proximity advice is the author's reasoning, not a controlled test; deep links and descriptive labels lower the cost of checking.
- Visible citations raise trust even when wrong; NN/g observed hallucinated or unrelated citations and few people opening them. So the UI must not signal more certainty than the system's own validation gave. Remove or flag claims whose citation was not verified by code, not by the model.
- Show the cited passage inline or in a preview card with the literal text, date and validity status (in force or not) so one step verifies it. Never cite superseded or invalid material.
- Do not display the model's step-by-step "reasoning" as proof: it can be unfaithful and gives false transparency. Prefer sources and stated limits.

## 3. Confidence and abstention
- Show confidence only when it helps the person decide and will not mislead (Google PAIR). Format (category, alternatives, number, visual) follows the action; numbers assume statistical literacy, so prefer categories for general audiences and test.
- Abstention ("I could not find a source for this") is a designed state with an explanation, what was searched and a next action (rephrase, broaden, ask a human). It is not an error screen and not a fabricated answer.
- Mark what the system did not confirm (for example amber with an icon and text); never omit the abstention to look helpful.
- Uncertain or unsourced content looks different from sourced content by shape and label, not only color.

## 4. The model proposes, the person decides
- Every model suggestion has Apply and Dismiss, shows a before and after, and can be undone. The recommended option is highlighted, never applied automatically.
- Nothing is written into a final document without a person's action. A draft carries a persistent label stating who is responsible for the final text, in the header, not only a footer.
- Drafts are editable in place; edits are kept when the model regenerates; the person can regenerate a part, not only the whole.
- Break long output into reviewable parts and say what to check first. Replace "continue" with an invitation to examine ("how sure is this?").
- Cognitive forcing (Buçinca et al. 2021, arXiv 2102.09692; 199 participants) reduced over-reliance on wrong suggestions more than explanations alone, but people rated it least favorable. Apply forced review only where a wrong decision is costly; add no friction elsewhere. State facts ("57 of 57 doubts resolved") and remind to verify before confirming.
- Keep the sensitive decision outside the model: if rules decide risk, the interface shows the rule engine result, not a model verdict.

## 5. Latency and streaming
- Follow the response-time limits: first sign of life well under 1 s (typing indicator, skeleton, or the first stage "Searching the sources"), then named stages for long runs, percent or step count over 10 s, and cancel.
- Streaming text helps perceived speed but lets people read unverified text. Withhold citations and actions until validation completes, or label streamed text as provisional; avoid layout shifts while streaming and keep the scroll position stable.
- Show stages that mean something to the person (searching, reading, drafting, checking sources), not fake percentages.
- Allow leaving and coming back; the result stays available and a notification is optional.

## 6. Wrong answers and recovery
From Google PAIR "Errors + Graceful Failure" (read 2026-11-15):
- Define errors from the person's view; distinguish user errors, system errors and context errors (wrong assumptions about what the person wants).
- Weigh stakes: errors hurt most for novices, multitaskers and low-confidence outputs, and in health, safety and money.
- Find errors people do not notice: quality assurance and stress tests, not only complaints.
- Give a way forward: feedback channel, alternatives, control returned with context. Error messages may need to say the system made a mistake.
Add: one-tap "this is wrong" with a reason, correction the system applies to the current draft, and a path to a human. Keep an audit trail of what was shown (sources, versions) so a wrong answer can be traced.

## 7. Tone and anthropomorphism
- Prefer neutral source-based wording ("This answer is based on these provisions") over first person ("I think") and over personality or emotion.
- Do not give the system a name, face or feelings that imply understanding or accountability. Avoid claims like "I understand" or "I checked".
- Tell people in plain language, near the input and tied to an action, what the system can and cannot do (HAX guidelines 1 and 2).

## 8. Microsoft HAX 18 guidelines
Titles as published by Microsoft Research (read 2026-11-15):
- **Initially:** 1 Make clear what the system can do. 2 Make clear how well the system can do what it can do.
- **During interaction:** 3 Time services based on context. 4 Show contextually relevant information. 5 Match relevant social norms. 6 Mitigate social biases.
- **When wrong:** 7 Support efficient invocation. 8 Support efficient dismissal. 9 Support efficient correction. 10 Scope services when in doubt. 11 Make clear why the system did what it did.
- **Over time:** 12 Remember recent interactions. 13 Learn from user behavior. 14 Update and adapt cautiously. 15 Encourage granular feedback. 16 Convey the consequences of user actions. 17 Provide global controls. 18 Notify users about changes.
Use them as a review list: mark each as met, not met or not applicable.

## 9. Checklist
- [ ] Capabilities and limits stated before first use, near the input.
- [ ] Each claim has a verifiable source one step away; unverified claims are visibly different or removed.
- [ ] Abstention state exists and offers a next action.
- [ ] Model output is a proposal: Apply, Dismiss, edit, undo; nothing final without the person.
- [ ] Responsibility label persistent on drafts.
- [ ] Stages and cancel for long runs; no fake progress.
- [ ] Wrong-answer reporting and correction path; audit trail kept.
- [ ] Neutral tone; no pretended understanding.
- [ ] Sensitive judgments come from rules or a person, not from model prose.

## 10. Sources
- https://www.nngroup.com/articles/explainable-ai/ and https://www.nngroup.com/articles/ai-chatbots-discourage-error-checking/ (study notes 2026-11-13, not re-fetched)
- https://arxiv.org/abs/2102.09692 (Buçinca, Malaya, Gajos 2021; study notes, not re-fetched)
- https://pair.withgoogle.com/chapter/errors-failing/ and https://pair.withgoogle.com/chapter/explainability-trust/ (read 2026-11-15); guidebook home https://pair.withgoogle.com/guidebook/
- https://www.microsoft.com/en-us/research/articles/guidelines-for-human-ai-interaction-eighteen-best-practices-for-human-centered-ai-design/ and https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ (read 2026-11-15)
