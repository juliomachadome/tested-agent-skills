# Feedback in motion: patterns and durations

How feedback moves. Which feedback to give is decided in `ux-design`; colours, shapes and the base duration and easing tokens live in `ui-design/references/motion.md`. When the project has motion tokens, they replace every number here. Ranges are practitioner defaults [F] unless a source is named.

## Contents
1. Response-time thresholds
2. Button and submit states
3. Loading: skeleton, spinner, progress
4. Enter, exit and reorder
5. Toggles, selection, add-to-cart
6. Reduced motion and no-sound versions
7. Code shapes

## 1. Response-time thresholds
- About 0.1 s: feels instant; the pressed state must show inside this window, on `pointerdown`, not after the network reply (Nielsen, response-time limits).
- About 1 s: flow is kept; beyond it show an in-place activity indicator.
- About 10 s: attention is lost; show progress with percent or named steps and a way to cancel.
- Do not show a spinner for waits under about 300 to 400 ms; delay it (show only if the request is still pending) to avoid a flash. Once shown, keep it at least about 500 ms so it does not flicker.

## 2. Button and submit states
| State | What moves | Typical time |
|---|---|---|
| Pressed | scale to 0.97 to 0.98 or darken; instant in, release on pointerup | in under 100 ms, out 100 to 150 ms |
| Loading | label crossfades to spinner or "Sending..." inside the same box; width locked | crossfade 150 ms; spinner rotation about 0.8 to 1 s per turn, linear |
| Success | spinner swaps to a check (stroke draw or fade-scale from 0.8), label "Sent" | 200 to 300 ms; hold 1.5 to 2 s or move to the next view |
| Error | button returns to idle; message appears near the field; optional single shake of 2 to 4 px | message fade 150 to 200 ms; shake under 300 ms, once, never on reduced motion |
Rules: lock the width (`min-width` or measured) so the label swap does not shift layout; set `aria-busy` and disable during loading to block double submit; move focus to the error summary or first invalid field; keep the input.

## 3. Loading: skeleton, spinner, progress
- Skeleton: same size and position as the arriving content (no shift when it lands); a soft shimmer at 1.2 to 2 s per cycle or a static block; stop the shimmer under reduced motion. Replace skeleton with content by a 150 to 200 ms fade, not a slide.
- Spinner: only for short, blocking waits where nothing can be shown in place.
- Determinate progress: when the size or the steps are known (upload, multi-step job). Animate `transform: scaleX()` on the bar, never `width`. Never let it reach 100% before the job ends; a stuck bar is worse than a spinner.
- Optimistic UI: show the result at once and reconcile; on failure, roll back with a visible message and a retry.

## 4. Enter, exit and reorder
- Enter: opacity 0 to 1 plus translate 8 to 16 px from the direction of origin, 200 to 300 ms, decelerating.
- Exit: about 30% faster than the enter, accelerating; then collapse the freed space (animate a wrapper with FLIP or a grid-rows trick, not `height` every frame).
- Lists: stagger 20 to 40 ms per item, at most the first 6 to 8 items; the rest appear together.
- Reorder and shared-element moves: FLIP (measure first and last, invert with transform, play) or the View Transitions API where supported.
- Toasts and snackbars: slide 8 to 16 px plus fade; stay at least 4 to 6 s, longer with an action; pause the timer on hover and focus.

## 5. Toggles, selection, add-to-cart
- Toggle thumb: translate 150 to 200 ms; the track colour changes with it; state also shown by position and label, never colour alone.
- Checkbox: check stroke draw 150 ms.
- Add-to-cart: button confirms in place ("Added" plus check) and the cart count updates with a small scale pulse (1 to 1.15 to 1) of 200 to 300 ms; avoid flying-product animations across the page.
- Like or save: one short scale pulse; no particle bursts by default.

## 6. Reduced motion and no-sound versions
Every pattern above has a plain version:
- Pressed: colour or shade change only.
- Loading: static "Sending..." text with `aria-busy`; spinner may stay (it is essential feedback) but slower or replaced by a static icon if the project prefers.
- Success and error: instant swap of icon and text; announce via `role="status"` (success) or `role="alert"` (error).
- Enter and exit: opacity only, or instant.
- No shake; no shimmer; no stagger.
- Sound is never the carrier: the visual and text state is complete without it.

## 7. Code shapes
```css
.btn { transition: transform 120ms ease-out, background-color 120ms ease-out; }
.btn:active { transform: scale(.98); }
@media (prefers-reduced-motion: no-preference) {
  .toast[data-state="in"] { animation: toast-in 240ms cubic-bezier(.2,.8,.2,1) both; }
}
@keyframes toast-in { from { opacity: 0; transform: translateY(12px); } }
```
```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
// Delayed spinner: show only if still pending after 400 ms, keep at least 500 ms.
async function submit(btn, work) {
  btn.disabled = true; btn.setAttribute('aria-busy', 'true');
  let shownAt = 0;
  const t = setTimeout(() => { btn.dataset.state = 'loading'; shownAt = performance.now(); }, 400);
  try { await work(); btn.dataset.state = 'success'; }
  catch { btn.dataset.state = 'error'; }
  finally {
    clearTimeout(t);
    if (shownAt) await new Promise(r => setTimeout(r, Math.max(0, 500 - (performance.now() - shownAt))));
    btn.disabled = false; btn.removeAttribute('aria-busy');
  }
}
```

## Sources
See `BIBLIOGRAPHY.md`: Nielsen response-time limits; WCAG 2.2 (2.2.2, 2.3.1, 2.3.3, 4.1.3); MDN prefers-reduced-motion and View Transitions; Saffer, *Microinteractions* (via `ui-design/references/motion.md`).
