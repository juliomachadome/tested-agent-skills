# ShiftFern landing comparisons

[Original exploratory pair](shiftfern-landing.md) · [Public evaluation thread](https://github.com/juliomachadome/tested-agent-skills/issues/7)

## Short brief

> Cria uma landing em português pra ShiftFern. É um app de escalas semanais pra cafés independentes, com modelos reutilizáveis e exportação em PDF. Quero que dê pra experimentar os modelos na própria página. Entrega um HTML que eu consiga abrir direto.

[Fixture](../../evals/public/shiftfern-landing-ui-short.json) · [PNG without the skill](shiftfern-curta-sem-skill.png) · [PNG assigned the skill](shiftfern-curta-com-skill.png)

Both pages offered three templates and let the reviewer select one and edit a shift. The control put the working schedule in the first view and called the browser print action. The skill-assigned page showed a static example first, linked to the working schedule below, let the reviewer restore the original template, and downloaded a valid one-page PDF. Both rendered without horizontal page overflow at 320, 390, 768 and 1440 CSS px, page exceptions or external requests. Neither added a dedicated FAQ or a closing CTA. Those were outside the short brief.

The project owner flagged repetition in the skill-assisted design during review. The skill-assigned page shows the schedule twice: a static grid near the top and an editable grid below. The control uses the editable schedule as its main product visual. The direct PDF and reset controls are useful additions, while another large schedule preview adds a stop before the core interaction. That is a negative finding on economy and proximity to the task in this case. The review is qualitative and uses one pair.

## Detailed brief with full page requirements

[Fixture](../../evals/public/shiftfern-landing-ui-v2.json) · [PNG without the skill](shiftfern-completa-sem-skill.png) · [PNG with the skill](shiftfern-completa-com-skill.png)

Both pages provided a product introduction and schedule example, a workflow explanation, an interactive three-template demo, a PDF sample, a four-question FAQ, a closing call to action and a footer. The control shows saved templates beside the active schedule. The skill version gives saved templates a separate view. Both passed opening and closing the FAQ, returning to the demo from the closing CTA, and saving, finding and removing a template. Those checks ran at 390 px using keyboard activation and at 1440 px using pointer activation. Both downloaded readable one-page sample PDFs on desktop. Neither page overflowed horizontally at 320, 390, 768 and 1440 CSS px.

## Method and limitations

Each pair used the same user prompt in two independent Codex desktop agent sessions and retained the generated HTML without edits. Every screenshot used the same 1440 by 900 CSS-pixel browser viewport for the full page. The sessions inherited the same host settings. The tool did not expose the exact model ID. The without-skill arm was directed to use only the brief and common host guidance and was given no project skill. The skill arm was given the repository `ui-design` skill. In the detailed run, that agent confirmed reading the skill and the style index, minimalist and visual polish references. The short-run agents saved complete HTML before the session limit interrupted their final reports. Explicit assignment is the available exposure evidence for that pair.

The short and detailed briefs ask for different demo outcomes. Compare arms within each brief. The shared host guidance and general model capabilities can produce polished work in the control. These single development pairs support browser observations and visible differences, with no blinded preference, independent UI/UX attribution or automatic discovery result.
