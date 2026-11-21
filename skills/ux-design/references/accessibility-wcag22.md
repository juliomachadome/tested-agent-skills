# Accessibility: WCAG 2.2 AA for product UI, ARIA, keyboard patterns

## Contents
1. Scope and how to test
2. Criteria by theme
3. New in WCAG 2.2
4. First rule of ARIA and native-first
5. ARIA APG patterns: keyboard behavior
6. Status messages
7. Keyboard shortcuts
8. Sources

## 1. Scope and how to test
Target level AA. Automated tools find only part of the failures; always add a keyboard-only pass and a screen-reader pass on a sample of key flows (W3C WAI evaluation guidance). Test at 200 percent zoom and 320 CSS px width. Legal applicability varies by country and organization size: confirm with a legal source, then use AA as the working bar anyway.

## 2. Criteria by theme
Levels and wording checked at w3.org/TR/WCAG22 on 2026-11-15 unless marked.

**Color and contrast**
- 1.4.1 Use of Color (A): color is not the only way to convey information. Pair with icon, shape or text. (not re-fetched)
- 1.4.3 Contrast Minimum (AA): text 4.5:1, large text 3:1. Large text is at least 18 pt, or 14 pt bold (about 24 px or 18.66 px bold) (not re-fetched numerics).
- 1.4.11 Non-text Contrast (AA): visual information needed to identify UI components and states, and graphical objects, at least 3:1 against adjacent colors. A field with no border depends on its fill contrasting with the surface. Decorative dividers are out of scope.
- 1.4.13 Content on Hover or Focus (AA): extra content shown on hover or focus (tooltip, popover) must be dismissible (for example Esc) without moving the pointer or focus, hoverable (the pointer can move onto it), and persistent until dismissed or the trigger is removed. Never put instructions or errors only in a tooltip.

**Reflow and text**
- 1.4.4 Resize Text (AA) at 200 percent; 1.4.10 Reflow (AA): no two-dimensional scrolling at 320 CSS px width (vertical content), exceptions for content needing 2D layout such as data tables and maps; 1.4.12 Text Spacing (AA): content survives user-adjusted spacing. (1.4.10 verified; others not re-fetched)

**Keyboard and focus**
- 2.1.1 Keyboard (A): all functionality available from the keyboard (not re-fetched).
- 2.1.4 Character Key Shortcuts (A): a single-printable-character shortcut must be turn-off-able, remappable with a non-printable modifier, or active only while the component has focus. Key sequences count.
- 2.4.3 Focus Order (A): order preserves meaning and operability. Modals trap focus and return it to the trigger on close.
- 2.4.7 Focus Visible (AA): there is a mode of operation where the keyboard focus indicator is visible. Do not remove outlines without a replacement; use `:focus-visible` so mouse clicks do not show rings.
- 2.4.11 Focus Not Obscured (Minimum) (AA, new in 2.2): a focused component is not entirely hidden by author-created content such as sticky headers, banners, toasts or bottom bars. Fix with `scroll-padding` equal to the fixed bars.
- 2.4.13 Focus Appearance (AAA, new in 2.2): a cheap design goal: indicator at least 2 px thick around the component with 3:1 change in contrast. (not re-fetched)

**Pointer**
- 2.5.7 Dragging Movements (AA, new): any function that uses dragging can be done with a single pointer without dragging, unless dragging is essential or determined by the user agent. Example: sortable list gets "move up / move down" buttons.
- 2.5.8 Target Size (Minimum) (AA, new): the pointer target is at least 24 by 24 CSS px. Smaller targets pass only if: (1) spacing: a 24 px circle centered on each undersized target does not intersect another target or circle; (2) an equivalent control on the same page meets the size; (3) inline in a sentence or limited by surrounding line height; (4) size set by the user agent; (5) essential or legally required presentation. 24 px is the floor; 44 px is the common touch design target (2.5.5 Target Size Enhanced is AAA).
- 2.5.3 Label in Name (A): the accessible name contains the visible label text (not re-fetched).

**Input and errors**
- 1.3.5 Identify Input Purpose (AA): fields collecting personal data expose their purpose (use correct `autocomplete`).
- 3.3.1 Error Identification (A) and 3.3.3 Error Suggestion (AA): errors identified in text, with a correction suggestion where known (not re-fetched).
- 3.3.4 Error Prevention, Legal, Financial, Data (AA): submissions that create legal or financial commitments or change or delete user data must be reversible, checked, or confirmed. This does not require a confirm on every save. (wording not re-fetched; consistent with the Understanding page cited in the study notes)
- 4.1.2 Name, Role, Value (A): icon buttons have an accessible name (not re-fetched).
- 4.1.3 Status Messages (AA): see section 6.
- 4.1.1 Parsing was removed in WCAG 2.2 (confirmed).

## 3. New in WCAG 2.2 (A and AA)
| Criterion | Level | One-line rule | Typical failure |
|---|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused item not entirely hidden by author content | Sticky footer covers the focused field |
| 2.5.7 Dragging Movements | AA | Single-pointer alternative to dragging | Reorder only by drag |
| 2.5.8 Target Size (Minimum) | AA | 24x24 CSS px or an exception | Tiny close icons packed together |
| 3.2.6 Consistent Help | A | Help mechanisms (contact, self-help, chat) appear in the same relative order across pages of a set, unless the user changes it | Help link moves between pages |
| 3.3.7 Redundant Entry | A | Information already entered in the same process is auto-populated or selectable, unless essential, security-related or no longer valid | Asking for email again at step 3 |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive function test (remember a password, solve a puzzle) in any authentication step unless there is an alternative, a helping mechanism (password manager, paste), object recognition, or personal content | Blocking paste in password or code field; transcription CAPTCHA |

3.3.9 Accessible Authentication (Enhanced) is AAA and not required for AA.

**Status of WCAG 3.** The WCAG 3.0 draft on w3.org is a Working Draft dated 2026-09-10 (read 2026-11-15). It is not a Recommendation, does not replace WCAG 2, and states that its contrast algorithm is yet to be determined (no APCA or other method is adopted). Keep using the WCAG 2.2 ratios (4.5:1, 3:1) for conformance; APCA can be a extra readability check but is not a standard.

## 4. First rule of ARIA and native-first
The W3C "Using ARIA" note states the first rule: if a native HTML feature already has the semantics and behavior you need, use it instead of repurposing another tag and adding ARIA. The APG's read-me-first guidance says "No ARIA is better than bad ARIA" and "a role is a promise": adding a role means you must also supply the keyboard behavior that role implies, because ARIA roles do not give browsers keyboard behavior or styling. Practical order: native tag, then native tag plus a few attributes, then a custom widget following the APG pattern exactly.

## 5. ARIA APG patterns: keyboard behavior
Summary of the APG pattern pages (read for the study notes on 2026-11-13; pattern names and URLs below; details not re-fetched this session).

| Pattern | Key behavior |
|---|---|
| Modal dialog | `role="dialog"`, `aria-modal="true"`, labelled by its visible title; focus moves inside on open (first focusable, or the least destructive action when the action is hard to undo); Tab and Shift+Tab cycle inside; Esc closes; focus returns to the opener |
| Menu button | Trigger is a button with `aria-haspopup` and `aria-expanded`; Enter or Space opens and focuses the first item; Esc closes and returns focus; Arrow keys move among items |
| Combobox | `role="combobox"`, `aria-expanded`, `aria-controls` to the popup, `aria-autocomplete`; DOM focus stays in the input, the active option via `aria-activedescendant`; Down Arrow enters the popup, Esc closes, Enter accepts |
| Listbox | `role="listbox"` with `option`; arrows move, Home/End on long lists, type-ahead, `aria-multiselectable` for multi-select; keyboard focus and selected state are different things |
| Toolbar | `role="toolbar"` with a label; one tab stop, arrows move between controls (roving tabindex); group only 3+ controls |
| Tabs, accordion, disclosure | Follow their APG pages; prefer native `details` for simple disclosure |

A long document list with per-item focus (for example reviewing thousands of rows) is a document with managed focus, not a listbox.

## 6. Status messages
4.1.3: status messages are presented by assistive technology without receiving focus. Use `role="status"` (polite) for results and progress ("Saved", "3 items deleted"); `role="alert"` only for urgent errors; an alert on non-urgent content is a failure. Keep one polite live region per screen instead of one per row, and avoid assertive announcements for counters that change every second. The region must exist in the DOM before the text changes.

## 7. Keyboard shortcuts
- Show shortcuts in tooltips and in a shortcuts panel; scoped shortcuts work only in their context, and a focused text field's own shortcuts win.
- Do not redefine platform standards (copy, paste, undo, find, save). Use Cmd on Apple platforms and Ctrl elsewhere, and show the one the person has.
- Hover does not exist on touch or keyboard: any hover-only reveal needs a focus or tap path.
- Single-key shortcuts must satisfy 2.1.4 (off, remap, or focus-scoped).

## Sources
- https://www.w3.org/TR/WCAG22/ (levels and wording of 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 2.4.7, 1.4.3, 1.4.11, 1.4.13, 2.1.4, 1.3.5, 1.4.10, removal of 4.1.1; read 2026-11-15)
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html (2.5.8 and five exceptions; read 2026-11-15)
- https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html, .../consistent-help.html, .../redundant-entry.html, .../accessible-authentication-minimum.html (read 2026-11-15)
- https://www.w3.org/TR/wcag-3.0/ (status and contrast algorithm note; read 2026-11-15)
- https://www.w3.org/TR/using-aria/ (first rule of ARIA, read 2026-11-15)
- https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/ (read 2026-11-15)
- https://www.w3.org/WAI/ARIA/apg/patterns/ (dialog-modal, menu-button, combobox, listbox, toolbar; read 2026-11-13 via study notes, not re-verified)
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html, .../focus-not-obscured-minimum.html, .../character-key-shortcuts.html, .../content-on-hover-or-focus.html (read 2026-11-13 via study notes, not re-verified)
