# Modelling: dimensional, wide tables, data vault, history

Tags as elsewhere. Ideas from Kimball and Ross, Inmon, Linstedt and Olschimke, applied not copied.

## Dimensional basics **[C]**
- **Business process first.** Pick one process (orders, sessions, tickets). Declare the **grain** in one sentence before any column: "one row per order line". Everything in the fact table must be true at that grain.
- **Fact** = measurements (amount, quantity, duration) plus foreign keys to dimensions. Additive (sum across all), semi-additive (balances: not across time), non-additive (ratios: store numerator and denominator).
- **Dimension** = descriptive context (customer, product, date). Keep a surrogate key and the natural key. Put a "unknown" row (key -1) so facts never drop on null.
- **Conformed dimensions** (same customer dimension in all marts) are what makes cross-process numbers agree. A bus matrix (processes as rows, dimensions as columns) is the planning tool.
- **Fact types**: transaction (one row per event), periodic snapshot (balance per day), accumulating snapshot (one row per lifecycle, updated as stages complete).
- Degenerate dimensions (order number) live in the fact; junk dimensions hold small flags.

## Slowly changing dimensions
| Type | Behaviour | Use when |
|---|---|---|
| 1 | overwrite | history of the attribute does not matter (typo fix) |
| 2 | new row with valid_from, valid_to, is_current | reports must show the value as it was then (plan, region, owner) |
| 3 | keep previous value in a column | one prior value is enough |
dbt snapshots implement type 2: `timestamp` strategy is preferred, `check` when no reliable update column exists, valid-from and valid-to columns are added, hard deletes handled by an option, and snapshots cannot be rebuilt so protect the schema **[C]**. Join facts to the version valid at the event time (`event_time >= valid_from and event_time < coalesce(valid_to, far_future)`). Test that versions of one key do not overlap.

## Choosing a style
| Style | Strength | Cost | Fit |
|---|---|---|---|
| Kimball star | easy for BI users, fast, clear grain | upfront modelling, conformance discipline | the default for most teams **[F]** |
| One wide table per use case ("OBT") | fastest to ship, simple for a single dashboard | duplicated logic, slow to change, fan-out risks, many definitions | one team, one dashboard, small data **[F]** |
| Data vault (hubs, links, satellites) | auditability, parallel loading, many sources, history by design **[M]** | more tables and joins, needs a presentation layer on top, specialist skill | large, regulated, many-source enterprises; rarely a small team |
| Inmon normalised core | single enterprise truth | heavy, slow to deliver | large organisations with a central data team |
Layering that works in dbt **[F]**: sources, staging (rename, cast, dedupe, one model per source table), intermediate (joins and business logic), marts (facts and dimensions or wide tables for consumers). A wide table can be a mart built on a star; do not skip the layer below.

## Rules that prevent wrong numbers
- Declare and test the grain (unique on the key) in every model.
- Aggregate to the target grain before joining many-to-one chains; never sum a column after a one-to-many join.
- One definition per metric, in one place (a model or a semantic layer), named in the data dictionary.
- Keep money as integer minor units or fixed decimal with currency; convert currency with a dated rate table.
- Keep raw data untouched; fix in staging so you can reprocess.
