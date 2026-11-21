# E-commerce (catalogue, variants, filters, checkout)

## What matters most
Large catalogues win or lose on crawl control and uniqueness: which URLs may be indexed, one canonical per product, and category pages that help a buyer choose. Product data quality (price, availability, identifiers) feeds both rich results and shopping surfaces. [C #7, #16]
- Index the product page and a limited set of category and filter pages that match real searches; block the infinite combinations.
- Unique, useful product text and own photos; manufacturer text copied by every shop is the weakest page.
- Stock and price shown in text and in structured data agree.

## Page templates
- Category: short intro, product grid with real links, selected filters as crawlable landing pages (a few: "black running shoes women"), buying guide below the grid, breadcrumbs.
- Product: title with the distinctive features, price, availability, variants, images, specs table, delivery and returns, reviews (real), related items, FAQ answered in text.
- Variants: one canonical product URL with variants selectable, or variant URLs that each canonical to the main one unless a variant has its own demand (colour as a query).
- Out of stock: keep the page with alternatives if it returns; 301 to the closest replacement if permanent; 404/410 if nothing relevant [F].
- Guides and comparison pages for the purchase decision.

## Structured data (candidates)
`Product` with `offers` (price, currency, availability), identifiers (gtin, mpn), `brand`, `image`; merchant listing data and a product feed in Merchant Center for free listings; `AggregateRating` and `Review` only for real reviews of that product; `BreadcrumbList`; `Organization`; return policy data. Validate and keep in sync with the page; mismatched price is a policy issue [#7, #27].

## Pitfalls
- Faceted URLs (colour, size, sort, price, page) generating thousands of near-duplicates [#16]; sort and session parameters indexed.
- Canonical on every page pointing to the category or home.
- Pagination canonicalised to page 1 (hides products beyond page 1).
- JavaScript-only grids with no links in HTML [#12].
- Duplicate manufacturer descriptions; the same product under several URLs/categories.
- Reviews imported from other sites or fabricated.
- Redirecting every dead product to the home page (soft 404 behaviour).
- Slow category pages from heavy filters and images.

## Metrics
Revenue and orders by landing page type, category page clicks and position, index coverage by template (indexed vs submitted), crawl stats by section, product impressions in Merchant Center, conversion rate by device, share of non-brand revenue.

## Checklist
- [ ] Facet policy written: which filters are indexable, the rest blocked from crawling or noindexed consistently; parameters ordered, no session IDs.
- [ ] One canonical per product and variant rule documented.
- [ ] Sitemap lists canonical products and categories only, real `lastmod`.
- [ ] Product schema validates; price and stock match the page and feed.
- [ ] Category pages have intro, links and a buying guide; paginated pages are self-canonical and linked.
- [ ] Out-of-stock and discontinued rules applied.
- [ ] Images with descriptive filenames, alt, dimensions, modern formats; LCP image prioritised.
- [ ] Reviews are real and moderated.

## Sources
#7 Product data, #4 canonical, #16 faceted navigation, #17 crawl budget, #19 sitemaps, #12 JavaScript SEO, #27, #28 gallery. Worked example of duplicates in `../diagnosis-playbook.md` trees 2 and 5; hreflang for several markets in `multilingual-international.md`.
