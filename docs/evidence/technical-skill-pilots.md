# Web motion and code craft pilots

These are public development cases. The originating trials used one exploratory pair per task in Codex Desktop with matched prompts. The exact model ID was unavailable and the agent sessions were reused. The code-craft agent confirmed reading the skill. The web-motion assignment was recorded and its final read report was unavailable. See the [original pilot record](https://github.com/juliomachadome/tested-agent-skills/issues/7#issuecomment-7072476182).

| Case | Observed result |
| --- | --- |
| [Lume 02](../../evals/public/lume-02-motion.json) | Both explainers passed forward, back and restart, provided the steps without JavaScript, and worked with reduced motion. The skill-assigned result added a caption and an accessible description of the changed part that tracked the current step. The longest observed transition was 280 ms in that output and 775 ms in the control. No animations remained active after settling. This measures behavior, not comprehension or frame rate. |
| [Legacy shipping](../../evals/public/legacy-shipping-change.json) | Both versions passed 767 checks after adding pickup and 1,144 checks after adding a region. The region-first version assigned code-craft changed two locations for the new region. The speed-first control changed three. The region-first version also reused the rate table for validation. The change cost is descriptive and specific to that direction. |

## Reproduction

Give each condition only the fixture prompt. For shipping, save the first deliverable before revealing a follow-up. Start the region and scheduled-service branches independently from the same saved deliverable. The service case is a new proposed check, not part of the reported comparison. Verify previous outputs and validation, local pickup rules, boundary values, and the new rules. Then compare how many places carry each rule and whether either extension requires a new abstraction.

For motion, check the settled state of each step using both standard and reduced motion. Use the same mobile width and initial state in each run. Check keyboard navigation and the written fallback without JavaScript. Record what the visual, step text, and caption each contribute. Review timing in context. The historical observations are not fixed performance targets.
