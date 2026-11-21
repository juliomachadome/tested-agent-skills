# Marketplaces and directories (user listings, entity databases, comparison sites)

## What matters most
These sites generate many pages from data, so the question is which pages deserve to exist. Each indexable page needs unique value beyond the shared template: a real listing with detail, a category with curation, an entity with facts, reviews, and freshness. [C #2, #1]
- Index a page only when it has enough unique data, a clear intent and a path to action.
- Supply quality is the SEO lever: listing completeness, photos, reviews, freshness.
- Handle expiry cleanly: sold, closed and deleted listings.

## Page templates
- Listing: title, key attributes in text, photos with alt, price, location, seller or provider, reviews, related listings, report link, one CTA.
- Category / location / attribute pages: a curated subset with a short unique intro, filters limited to useful combinations, counts that are real.
- Entity or provider profile: verified facts, reviews, services, links to listings.
- Search results pages: usually noindex; do not let internal search URLs into the index.
- Guides and "how to choose" content that links to categories.

## Structured data (candidates)
`Product` or `Offer` for listings with prices where eligible [#7], `LocalBusiness` for providers with real locations [#8], `ItemList` on category pages (no rich result promised), `BreadcrumbList`, `Review`/`AggregateRating` only for genuine reviews of that item that you collect and show; do not mark up reviews copied from elsewhere [#27].

## Pitfalls
- Thin listings (a title and a photo); empty category/location combinations; "0 results" pages indexable.
- Programmatic location x category pages for places with no supply (doorway pattern) [#2].
- Spam listings and user-generated links without `rel="ugc"` or `nofollow`.
- Duplicate listings from the same seller; syndicated feeds identical to competitors.
- Expired listings returning 200 with an "unavailable" message (soft 404).
- Indexing internal search and parameters [#16].
- Scraped content from other sites.

## Metrics
Indexed vs submitted pages per template; share of indexed pages with clicks in 90 days; listings per category and fill rate; listing-to-contact conversion; supplier acquisition from organic; crawl stats per section; time to index new listings; reviews per listing.

## Checklist
- [ ] Minimum-quality rule for indexing a listing and a category (fields, photos, text length is not a rule, uniqueness is).
- [ ] Empty or thin combinations noindexed or not generated; internal search noindex.
- [ ] Expiry flow: 301 to a close alternative or category, 410 for gone, keep sold with alternatives when useful.
- [ ] `ugc`/`nofollow` on user links; moderation and report flow.
- [ ] Sitemaps split by template, with real `lastmod`; sample audit of 20 pages per template each quarter.
- [ ] Unique intros for important categories, written by a person.
- [ ] Review markup only from genuine, shown reviews.
- [ ] Faceted URL policy documented.

## Sources
#1, #2, #4, #7, #8, #16, #17, #19, #27; diagnosis trees 2, 5 and 12 in `../diagnosis-playbook.md`.
