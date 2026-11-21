# Dense tables and dashboards

- Offer density as a setting or pick by use: compact for high-frequency scanning, default for most business lists, roomy for occasional reading. Keep touch targets at least 24 px (44 px for primary touch controls) even when rows are compact.
- Alignment carries meaning: text left, numbers and money right (header aligned the same way), single flags centred, row actions at the far end. Use tabular figures for every numeric column so digits do not jitter when values update.
- Header row visually distinct but quiet (small, medium weight, muted); thin dividers instead of heavy zebra stripes; a subtle hover step to guide the eye across wide rows.
- Wide tables: pin the identifier column and the action column, show a shadow or gradient edge where content is cut, and test that sticky really sticks (an overflow ancestor silently breaks it).
- Sorting: show the state on the header (none, ascending, descending) and, with several sort keys, their order. Filters: a search box first, faceted filters with counts, and the active filters always visible and clearable. Saved views (filters + sort + columns) save repeated work for power users.
- Selection: when rows are checked, swap the toolbar for a bar that shows the selected count and the batch actions; when paginated, offer "select all N matching the filter" explicitly, and confirm destructive batch actions with a count preview.
- Loading: a skeleton with the table's real structure, never one centred spinner; errors with a retry that keeps filters and page; empty states differ: "nothing yet" (explain and offer the first action) versus "no match for these filters" (offer to clear them).
- KPI card anatomy: label, one large number, a comparison with its baseline and direction (colour never the only cue), optional tiny trend line without axes; show the period and the data's "as of" time.
- In-cell bars and sparklines must still print the number next to the graphic; every chart gets a text alternative or an adjacent data table.
- Escape every user-supplied string rendered into HTML or SVG; a portable single-file report should work offline with no external scripts or fonts.
- Funnels count cumulatively: a stage counts everything that reached it or went beyond, so the numbers never rise down the funnel.
