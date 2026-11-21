# Guided tours and in-context hints

Use only after you checked that the interface cannot teach itself (clear labels, good empty states, one obvious first action). A tour is a patch, not a design.

- Prefer doing to reading: highlight the real control and let the person click it; advance on the real action, not on "Next".
- Keep a linear tour to three or four steps. Introduce further hints later, when the person first reaches the relevant screen (progressive, contextual), not all on day one.
- Always allow skipping at every step, remember the dismissal, and offer a way to replay from a help or "getting started" entry. Never block the product behind a tour.
- Step text: a short action-oriented title and one or two sentences about the outcome; show progress ("2 of 4").
- Behaviour: scroll the target into view before showing the step; recompute position on resize and rotation; flip the popover when it would leave the viewport; if the target does not exist (feature flag, permission, empty data), skip the step instead of showing a floating box.
- Accessibility: the hint is a dialog that moves focus in and returns it to the trigger on close; Escape closes; arrow keys or Enter step through; the highlighted region must not hide content from assistive technology; respect reduced motion for the spotlight transition.
- Measure it: completion of the real task after the tour versus without it; if the tour does not move that number, remove it.
