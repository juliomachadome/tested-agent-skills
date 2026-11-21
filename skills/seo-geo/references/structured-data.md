# Structured data (JSON-LD), status late 2026

Sources: Google "AI features and your website", "Optimizing for generative AI features", Article and Course structured-data docs, Search Gallery, Video SEO, documentation changelog. Read 12/11/2026. Before proposing a type, open the gallery: it changes.

- **[C] No special schema for AI:** "there's no special schema.org markup you need to add". Use schema for semantics and for rich results that still exist; data must match visible text.
- **[C] `Article`:** no required properties; recommended `headline`, `image` (16×9, 4×3 and 1×1, at least 50k pixels), `datePublished`, `dateModified` (ISO 8601 with time zone), `author` with `name` and `url` or `sameAs`. `author.name` is only the name; `Person` for people, `Organization` for organisations; all visible authors also in markup.
- **[C] `BreadcrumbList`** remains in the gallery: keep it.
- **[C] FAQ rich results are gone for everyone:** restricted to government/health since Aug 2023, stopped showing 07/05/2026, docs removed 15/06/2026. `FAQPage` stays valid schema.org and does no harm, but produces nothing visible in Google. Do not create FAQs just for schema.
- **[C] Course:** "Course info" was discontinued (12/06/2025). "Course list" remains: needs **at least 3 courses** marked up, `name`, `description` (shows 60 chars) and `provider`, available **only in English**. Course titles without price or promotion. In other languages, `Course` is semantics only.
- **[C] `HowTo`, `DefinedTerm`, `DefinedTermSet` are not in the gallery.** Using them in a glossary is optional semantics. [F] No study shows they help AI citation.
- **[C] `Organization`** (logo, name, `sameAs`) still supported: one brand entity with the same `@id`, name and description site-wide; `sameAs` only to real profiles.
- **[C] `VideoObject`:** unique `name`, `description`, `thumbnailUrl` per video; `embedUrl` or `contentUrl`; accepts `creator` since 24/09/2026. Video features only on a dedicated watch page.
- **[C] Gallery today (25 types):** Article, Breadcrumb, Carousel, Course list, Dataset, Discussion forum, Education Q&A, Employer aggregate rating, Event, Image metadata, Job posting, Local business, Math solver, Movie, Organization, Product, Profile page, Q&A, Recipe, Review snippet, Software app, Speakable, Subscription and paywalled content, Vacation rental, Video. Removed: FAQ, HowTo, Course info, Practice problems (Jan 2026), Sitelinks search box, Fact check, Learning video, Special announcement, Vehicle listing, Book actions, Estimated salary.
- **[C] Reviews:** `AggregateRating` and `Review` only with real reviews visible on the page; fake or undisclosed incentivised reviews violate the review-snippet guideline (Jul 2026).
- **[C] Validate** in the Rich Results Test (what Google uses) and the schema.org validator (syntax). An automated test comparing JSON-LD with visible text (price, questions, author, dates) prevents silent divergence.
