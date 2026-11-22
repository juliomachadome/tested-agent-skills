# Web motion and code craft pilots

These are public development cases. The originating trials used one exploratory pair per task in Codex Desktop with matched prompts. The exact model ID was unavailable and the agent sessions were reused. The code-craft agent confirmed reading the skill. The web-motion assignment was recorded and its final read report was unavailable. See the [original pilot record](https://github.com/juliomachadome/tested-agent-skills/issues/7#issuecomment-7072476182).

| Case | Observed result |
| --- | --- |
| [Lume 02](../../evals/public/lume-02-motion.json) | Both explainers passed forward, back and restart, provided the steps without JavaScript, and worked with reduced motion. The skill-assigned result added a caption and an accessible description of the changed part that tracked the current step. The longest observed transition was 280 ms in that output and 775 ms in the control. No animations remained active after settling. The measured signals are transition duration and browser behavior. Comprehension and frame rate require their own measurements. |
| [Legacy shipping](../../evals/public/legacy-shipping-change.json) | Both versions passed 767 checks after adding pickup and 1,144 checks after adding a region. The region-first version assigned code-craft changed two locations for the new region. The speed-first control changed three. The region-first version also reused the rate table for validation. The change cost is descriptive and specific to that direction. |

## Reproduction

Give each condition only the fixture prompt. For shipping, save the first deliverable before revealing a follow-up. Start the region and scheduled-service branches independently from the same saved deliverable. The service check below starts both conditions from the same saved region-first module. Verify previous outputs and validation, local pickup rules, boundary values, and the new rules. Then compare how many places carry each rule and whether either extension requires a new abstraction.

For motion, check the settled state of each step using both standard and reduced motion. Use the same mobile width and initial state in each run. Check keyboard navigation and the written fallback without JavaScript. Record what the visual, step text, and caption each contribute. Review timing in context. The historical observations are not fixed performance targets.

## Revision check

For the scheduled-service follow-up, two fresh Codex Desktop agents used the same region-first module, prompt and inherited settings. One read the previous skill and one read the revision. The model ID was unavailable. Both output modules passed the same 1,019 checks: 504 legacy calculations, 252 pickup calculations, 11 validation errors, and 252 scheduled calculations. Both changed four lines. The previous-skill result edited a separate list of valid speeds. The revised-skill result derived validation from the surcharge table, with a string guard to preserve the original input contract. This removes one list to keep in sync on a future change. The observed diff size tied.

For the Lume follow-up, two fresh agents generated standalone explainers from the original prompt. They were assigned the previous and revised web-motion guidance respectively, with the same inherited host settings. Chromium 157 checked the three settled shapes and navigation at a 390 px reduced-motion viewport and a 1440 px standard-motion viewport. Both retained three instructions without JavaScript and showed no horizontal overflow, script errors or external requests. The revised result added a separate caption at each step, describing the ring opening, the support being exposed, and the new shade being seated. The older result conveyed the steps in the instruction text. The observed maximum desktop transition was 270 ms with the previous skill and 260 ms with the revision.

Each revision check is one pair. The evidence supports these scoped outcomes. A general preference or robustness claim requires further runs and independent review.
