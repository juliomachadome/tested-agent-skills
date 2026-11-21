# The "understand it without reading" test

## Contents
1. What it proves and why
2. Procedure
3. Browser script (Playwright or DevTools)
4. Judging the screenshot
5. Pass/fail criteria
6. Limits and pitfalls
7. Walk through a flow in an unfamiliar language
8. Sources

## 1. What it proves and why
Layout, shape, weight, position and color should carry the structure of a screen before a single word is read. Pre-attentive cues (size, contrast, grouping) and Gestalt grouping (proximity, common region, similarity) are processed before reading, and people scan more than they read. If a screen only makes sense through its words, it also fails people who do not read the language well, read fast, read under stress, use translation, or rely on grayscale or low vision. The test is a heuristic: it finds weak hierarchy and state-by-color-only. It does not replace tests with real people and cannot judge the quality of the words.

## 2. Procedure
1. Pick the screen and one state (for example a list with mixed item states). Test each important state separately.
2. Load it in a browser at the real viewport (phone width and desktop width, separately).
3. Run the script below: every visible text string becomes gibberish of the same length; icons, shapes, colors and layout stay.
4. Take a screenshot (full page and viewport).
5. Judge from that screenshot alone, without looking at the original, ideally by someone who has not seen the screen. Answer in writing, within a few seconds each:
   1. **Where is the single focus?** The one place the eye lands first and the thing it is supposed to be.
   2. **What state is each item in?** For every row, card or control: done, pending, error, selected, disabled, new. Name the cue that tells you: shape, icon, color, position, weight.
   3. **What is the next action?** The control you would press, and whether anything dangerous looks like the safe choice.
6. Compare with the intended answers. Record mismatches as findings (cite hierarchy, Von Restorff, Gestalt, WCAG 1.4.1).
7. Optionally repeat in grayscale (`filter: grayscale(1)` on `html`) to expose color-only state.

## 3. Browser script
Replaces letters and digits (any script) with random letters, keeps whitespace and punctuation, skips scripts, styles and icon fonts, and also scrambles placeholders, input values, `title` and `alt` text so nothing leaks. A MutationObserver rescrambles content added later (toasts, lazy rows).

```js
(() => {
  const SKIP = /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/;
  const rnd = () => 'abcdefghijklmnopqrstuvwxyz'[Math.floor(Math.random() * 26)];
  const garble = (s) => s.replace(/\p{L}|\p{N}/gu, (c) => {
    const g = rnd();
    return c === c.toUpperCase() && c !== c.toLowerCase() ? g.toUpperCase() : g;
  });
  const isIconFont = (el) => /icon|symbol|glyph|awesome|material/i.test(getComputedStyle(el).fontFamily);
  const done = new WeakSet();
  function scrub(root) {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (w.nextNode()) nodes.push(w.currentNode);
    for (const n of nodes) {
      const p = n.parentNode;
      if (!p || SKIP.test(p.tagName) || done.has(n) || !n.nodeValue.trim()) continue;
      if (isIconFont(p)) continue;               // ligature icons stay intact
      n.nodeValue = garble(n.nodeValue);
      done.add(n);
    }
    root.querySelectorAll?.('[placeholder],[title],[alt],input,textarea').forEach((el) => {
      for (const a of ['placeholder', 'title', 'alt']) if (el.hasAttribute(a)) el.setAttribute(a, garble(el.getAttribute(a)));
      if (/^(text|search|email|url|tel)?$/.test(el.type || '') && el.value) el.value = garble(el.value);
    });
  }
  scrub(document.body);
  new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => {
    if (n.nodeType === 1) scrub(n); else if (n.nodeType === 3 && n.parentNode) scrub(n.parentNode);
  }))).observe(document.body, { childList: true, subtree: true, characterData: false });
})();
```

Playwright usage (Node): save the script as `garble.js`, then

```js
await page.setViewportSize({ width: 390, height: 844 });
await page.goto(url);
await page.addScriptTag({ path: 'garble.js' });
await page.screenshot({ path: 'garbled-mobile.png', fullPage: true });
```
Run it after driving the page to the state under test (login, click, wait for data); the observer handles content that arrives later. In DevTools, paste the IIFE into the console. Grayscale variant: `document.querySelector('html').style.filter = 'grayscale(1)'` before the screenshot.

## 4. Judging the screenshot
- **Focus:** squint. The largest, darkest, most saturated or most isolated region is the focus. If two regions compete, the screen has no single focus. If the focus is a decorative image or a banner rather than the task, it fails.
- **State:** for each item list the cue. Pass cues: different shape (check, cross, ring), different icon, position (grouped under a section), weight; color alone is a fail. A row whose state is identical in grayscale to its neighbor but differs only in hue fails.
- **Next action:** one control reads as primary (fill, size, position). Destructive controls must look distinct and must not look like the primary. If you hesitate between two actions, it fails.
- Also note: reading order implied by layout, groups visible by spacing, tap targets that look tappable, empty areas that look like missing content.

## 5. Pass/fail criteria
- **Pass:** a reviewer who has not seen the screen answers all three questions correctly within about 5 seconds each, and at least two independent cues (for example shape and color) distinguish each state.
- **Conditional pass:** focus and next action right, but one state group relies on a single cue; log a severity 2 finding.
- **Fail:** the reviewer cannot name a single focus; or any state is distinguishable only by color or only by text; or the safe and dangerous actions look alike; or the primary action is not identifiable. Log severity 3 for a fail on a core task screen.
- Run it for each state that matters (loading, empty, error, success), not just the happy view. An unreadable empty or error state is common.

## 6. Limits and pitfalls
- Does not judge copy, clarity of labels, or correctness. Pair with a normal read-through.
- Icon-only controls pass this test but fail "icons need labels unless universal": check separately.
- Canvas, images of text, pseudo-node `content` (CSS) and text inside closed shadow DOM or cross-origin iframes are not scrambled by the script; scrub these by hand or note them.
- Scrambling changes text length only within a word's glyph widths; proportional fonts make widths differ slightly. Layout differences from line wrapping are expected and acceptable.
- Numeric badges and counts carry information; the script scrambles digits too. If a count is part of the state, check separately that a visible badge shape exists.
- Do not use real personal data on a screen you screenshot and share; the script also helps redact it.

### Companion check with the real words

Use intact copy in a separate check for a public landing page or important task state. Ask a reviewer unfamiliar with the screen what it offers, what happens next and where they would click or tap. For an error state, ask them to identify the correction and complete it without re-entering unaffected fields. Compare at the same viewport and starting state. Note redundant explanations separately from wording that communicates a price, condition, choice or way out. A short inspection is a diagnostic proxy; claims about how users actually complete the task need observation with users.

## 7. Walk through a flow in an unfamiliar language

Use an actual localized preview in a language the participant does not understand. Keep the labels in place, use synthetic data and pick a reversible task the person has never seen. Give the goal in a language they understand without naming controls or pointing at the screen. For example, ask them to add an item to a saved list, find it again and remove it. Run this at the viewport and input method you are reviewing.

Before the session, identify the intended entry point, action feedback, completion cue and safe recovery step. Observe the first meaningful action, wrong turns, requests for help and whether the person recognizes when they are done. Include a recoverable mistake where relevant. A useful signal is that someone navigates to the right place, understands a change occurred and can recover without being shown the path. Record where the flow needed a guess. Use people unfamiliar with the screen before claiming that users can do this. Keep the scrambled screenshot above as a faster hierarchy check. Its script mutates page content and input values, so use the localized preview for interaction.

Check names, warnings, amounts, permissions and consequences in the person's own language. Use the unfamiliar-language walkthrough for navigation and feedback. Evaluate any consequential action up to its confirmation screen in a safe preview, then verify informed confirmation separately. Preserve visible labels and accessible names.

## 8. Sources
- Gestalt grouping principles and Von Restorff effect: https://lawsofux.com/ (read 2026-11-15)
- WCAG 1.4.1 Use of Color: https://www.w3.org/TR/WCAG22/ (referenced; level A)
- NN/g on scanning behavior: https://www.nngroup.com/articles/how-users-read-on-the-web/ (not re-verified)
- The procedure itself is a review heuristic of this skill, not a standard.
