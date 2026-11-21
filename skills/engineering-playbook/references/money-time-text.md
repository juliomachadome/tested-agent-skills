# Money, Time & Text — Correctness Traps

## 1. Money

### Representation
- **Never `double`/`float`** — binary floating point can't represent 0.1 exactly (`0.1 + 0.2 = 0.30000000000000004`).
- **C#:** `decimal` (base-10, 28–29 significant digits). **SQL:** `decimal(19,4)` / `numeric(19,4)` (or more scale for FX rates/unit prices). **JS/TS:** integer minor units (`bigint` or safe integers) or a decimal library (`decimal.js`, `big.js`, `dinero.js`); JSON transport as string.
- Always carry the **currency** with the amount (Money value object: `record Money(decimal Amount, string Currency)`); never add different currencies.
- **ISO 4217** minor units differ: EUR/USD 2, JPY 0, BHD/KWD/TND 3. Don't hardcode 2 decimals.

### Rounding
- Decide **when** (per line vs on total — they give different results; follow the business/tax rule), **how** (mode), and **to what precision**.
- .NET `Math.Round(x)` and `decimal.Round` default to **banker's rounding** (`MidpointRounding.ToEven`: 2.5 → 2, 3.5 → 4). Commercial "round half up" needs `MidpointRounding.AwayFromZero`. Always pass the mode explicitly.
- JS `Math.round` rounds half toward +∞ (−2.5 → −2) and `toFixed` uses binary values (`(1.005).toFixed(2) = "1.00"`) — don't use them for money.
- Keep full precision during intermediate calculations (interest, FX, fees); round once at the defined boundary.

### Allocation (splitting)
- Splitting 100.00 into 3 → 33.33 × 3 = 99.99 loses a cent. Allocate remainders deterministically:

```csharp
static decimal[] Allocate(decimal total, int parts, int decimals = 2)
{
    var unit = 1m / (decimal)Math.Pow(10, decimals); // 0.01 for 2 decimals, exact
    var baseShare = Math.Floor(total / parts / unit) * unit;
    var result = Enumerable.Repeat(baseShare, parts).ToArray();
    var remainder = total - baseShare * parts;
    for (int i = 0; remainder > 0; i++, remainder -= unit) result[i] += unit;
    return result; // sums exactly to total
}
```

  For proportional splits (by ratios), allocate by ratio and distribute remainder (largest remainder method).

### Ledgers
- **Double-entry bookkeeping:** every transaction has ≥ 2 entries (debits = credits); balances are derived from immutable entries, not overwritten.
- Entries are **append-only**; corrections are reversing entries, never updates/deletes.
- Store both business time (`effective_at`) and record time (`created_at`).
- Idempotency keys on postings; unique constraints on external references.
- Balance checks under concurrency: atomic conditional updates or serialized per-account processing; or compute available balance from entries inside a transaction with appropriate locking.
- **Reconciliation:** periodically compare internal ledger with bank/PSP statements; flag mismatches; never "fix" by editing history.
- FX: store rate, source, timestamp and both amounts.
- Taxes (VAT/sales tax): rules on rounding per line vs per invoice and on invoicing software are legal requirements in many countries — confirm with accounting.

## 2. Time

### Concepts
- **Instant** (a point on the timeline) vs **local date/time** (wall clock in a place) vs **calendar date** (birthday, due date) vs **duration**.
- Time zones (`Europe/Lisbon`, `America/Sao_Paulo`) have rules that change (DST, government decisions) — store **IANA zone id**, not a fixed offset, for future local events.

### Rules
- Store instants in **UTC** (`datetimeoffset`/`timestamptz`); convert to local only for display.
- **.NET:** `DateTimeOffset` over `DateTime` for instants; `DateOnly`/`TimeOnly` (.NET 6+) for dates/times without zone; inject **`TimeProvider`** (.NET 8+) instead of calling `DateTime.UtcNow` directly (testability). Consider **NodaTime** for serious calendar/timezone logic.
- `DateTime.Now` on servers depends on the host's zone — avoid. `DateTimeKind.Unspecified` is a frequent bug source.
- **JS:** `Date` is an instant in ms with local-zone formatting; month is 0-based; parsing non-ISO strings is implementation-dependent. Use ISO 8601 (`2026-10-17T09:30:00Z`); `Intl.DateTimeFormat` for display; `date-fns`/`date-fns-tz` or Luxon; Temporal API where available.
- **Scheduling future events** (a class at 07:00 Lisbon time next March): store local time + zone, compute instant at execution — offset may change with DST.
- **DST traps:** some local times don't exist (spring forward) or occur twice (fall back); "add 1 day" ≠ "add 24 hours"; daily jobs at 01:00–03:00 local may skip/duplicate.
- Date ranges: use half-open intervals `[start, end)`; "today" depends on the user's zone — compute day boundaries in that zone.
- Durations for timeouts/elapsed time: monotonic clock (`Stopwatch`, `performance.now()`), not wall clock.
- Don't compare timestamps from different machines for strict ordering (clock skew).
- Leap years (Feb 29 birthdays/anniversaries), month-end arithmetic (Jan 31 + 1 month), week numbering (ISO weeks start Monday; locale differences).

## 3. Text & Unicode

- Strings in .NET and JS are **UTF-16 code units**; `length` ≠ number of user-visible characters. Emojis and many scripts use surrogate pairs/combining marks.
  - .NET: `StringInfo`/`EnumerateRunes()`; JS: `[...str]` for code points, `Intl.Segmenter` for grapheme clusters.
- Truncating by length can split a character → truncate by grapheme or text elements.
- **Normalization:** "é" can be one code point (NFC) or two (NFD). Normalize (`string.Normalize()`, `str.normalize('NFC')`) before comparing/storing identifiers.
- **Comparison:**
  - Identifiers, keys, protocols, file paths → **ordinal** (`StringComparison.Ordinal`/`OrdinalIgnoreCase`).
  - User-facing sorting/search → culture-aware (`StringComparer.Create(culture, …)`, `Intl.Collator('de-DE')`).
  - The **Turkish i problem:** `ToUpper()` with tr-TR culture changes "i" → "İ". Use `ToUpperInvariant` / ordinal ignore case for non-linguistic comparisons.
  - Accent-insensitive search: collation (`Latin1_General_CI_AI` in SQL Server), or normalize + strip diacritics into a search column.
- **Encoding:** UTF-8 everywhere (files, HTTP `charset=utf-8`, DB `nvarchar` in SQL Server or UTF-8 collations). Mojibake ("Ã©") = UTF-8 read as Latin-1.
- **Parsing/formatting numbers & dates:** culture matters ("1.234,56" in de-DE vs "1,234.56" en-US). Use `CultureInfo.InvariantCulture` for machine formats (JSON, CSV, logs), user culture for display. Set `<InvariantGlobalization>` consciously (it disables culture data).
- CSV: quote fields, escape quotes, specify delimiter (Excel in many European locales expects `;`), UTF-8 BOM if Excel must open it correctly; beware **CSV injection** (cells starting with `= + - @`).
- Email addresses, names, addresses, phone numbers: don't over-validate (see "Falsehoods programmers believe about names/addresses"); E.164 for phones (libphonenumber).

## 4. i18n / l10n

- Externalize strings (resx, i18next); no string concatenation for sentences (word order differs) — use ICU MessageFormat placeholders and plural rules.
- Plurals vary by language (`Intl.PluralRules`).
- Format currency with `Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' })` / `ToString("C", culture)`.
- Text expansion (German, French and others run longer than English) and RTL support in UI.
- Store user locale and time zone preferences.

## 5. Numbers in general

- Integer overflow: C# `checked` context for critical arithmetic; JS numbers lose integer precision beyond 2^53 − 1 (`Number.MAX_SAFE_INTEGER`) → `bigint` or strings for large ids.
- Division by zero, NaN propagation in JS, `-0`.
- Floating point equality: compare with tolerance for scientific/physical values (not money).
- Percentages: store as decimal fraction or basis points explicitly; document units (seconds vs ms, kg vs lb, kcal) in names (`timeoutMs`, `weightKg`).
