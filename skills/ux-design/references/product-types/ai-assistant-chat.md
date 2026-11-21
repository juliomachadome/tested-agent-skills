# AI assistant and chat

## Key jobs
A person gets a useful, checkable answer or completed action, understands how far to trust it, and can correct or stop it. Companion file: `../ai-features-ux.md` (citations, abstention, drafts, streaming).

## Critical flows
First use and what it can do; asking (free text, suggestions, prompt controls); answer with sources; follow-up and correction; handoff to a human; actions the agent takes (preview, permission, undo); history, memory and privacy; errors and refusals; feedback.

## Typical pitfalls
- Blank box with no examples; users do not know the scope (NN/g conversation types and prompt controls).
- Confident wrong answers; no sources, or numbered footnotes with no link to the passage; verification cost so high that people skip it (NN/g: chatbots discourage error checking).
- Tone that overpromises ("I understand you perfectly"); apologizing loops; vague refusals with no next step.
- Streaming text that moves the page or cannot be paused; long answers with no structure.
- An agent that acts without preview, permission or undo; memory that is invisible or cannot be deleted.
- Chat as the only interface for tasks better done with forms and buttons.
- Errors: timeouts and model failures that lose the draft (Google PAIR: errors and graceful failure; calibrate trust).
- Screen readers: live regions that read every streamed token.

## Metrics
Task success (not satisfaction alone), thumbs and edit rate, citation click rate, abstention rate and its correctness, escalation to human rate, retry and rephrase rate, time to useful answer, error rate by type, share of actions undone. Measure on a labeled sample: the data analysis for quality evals is outside this skill (`llm-engineering`).

## Checklist
- [ ] Opening state shows scope and 3 real examples; suggestions are editable.
- [ ] Each factual claim has a descriptive source one step away, with the passage; no source means labeled draft or abstain.
- [ ] Abstention is a designed state: why, what it can do instead, next action.
- [ ] Neutral, honest tone; no claims of feelings or certainty; responsibility label persistent where stakes are high.
- [ ] Output editable, copyable, dismissible; the person confirms before anything leaves the system.
- [ ] Actions: preview, scope of permission, one undo, log of what was done.
- [ ] Streaming: stable layout, stop button, polite and throttled announcements for assistive tech, reduced motion.
- [ ] Error states preserve the prompt and offer retry; a human route exists.
- [ ] Memory and history visible, editable, deletable; privacy explained.

## Sources
NN/g AI chatbots discourage error checking, prompt controls in GenAI chatbots, six types of conversations with generative AI; Google PAIR (errors and graceful failure, explainability and trust, mental models); WCAG 4.1.3; Norman (feedback, conceptual models); Microsoft guidelines for human-AI interaction appear in the older bibliography and are not re-verified.
