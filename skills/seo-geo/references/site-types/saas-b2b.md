# SaaS and B2B software

## What matters most
Buyers search by problem, by comparison and by category before they know a product; the site must own the pages where evaluation happens: use cases, integrations, alternatives, pricing and docs. Content has to prove product knowledge with real screens and data, not generic definitions. [C #1]
- Map queries to the funnel: problem (know), category and comparison (compare), pricing and integration (decide), docs (retain).
- Be a citable source for AI answers: clear definitions of the product, who it is for, what it costs, how it differs; numbers with sources; consistent facts across site, docs, review sites and directories. [#13, #33]
- The marketing site must be server-rendered; the logged-in app is out of scope and belongs behind noindex or auth.

## Page templates
- Home: one-sentence what it is and for whom, proof, link to use cases and pricing.
- Product and feature pages; use-case and industry pages with real examples (not swapped templates).
- Integration pages: what syncs, setup steps, limits, one page per real integration.
- Comparison and alternative pages: honest, current, dated, with sources; no false claims about competitors.
- Pricing page in text (plans, limits, billing terms), not only an image or widget.
- Docs and changelog: indexable, versioned, canonical to the current version.
- Glossary and guides tied to product capabilities; case studies with named results.

## Structured data (candidates)
`Organization` (home), `SoftwareApplication` or `WebApplication` where eligible and truthful (rating data only if real and shown) [#10]; `Article`/`BlogPosting` for posts [#9]; `BreadcrumbList`; `VideoObject` for hosted demos with watch pages [#29]. No `FAQPage` for rich results (not shown since 07/05/2026) and no `Review` markup for your own product on your own page.

## Pitfalls
- Programmatic pages (one per integration, city or keyword) with a swapped word: scaled content abuse [#2].
- Gated everything: nothing indexable between the home page and signup.
- JavaScript-rendered docs or pricing [#12].
- Staging, app and preview subdomains indexed; duplicate docs versions.
- Comparison pages with invented claims or stale prices.
- Blog traffic with no path to the product; metrics read as pageviews.
- Cannibalising: several posts for one query.
- llms.txt or "AI schema" as strategy [#33].

## Metrics
Signups, demo requests and activated trials by landing page and by source (organic, AI referral where visible); non-brand clicks to money pages; share of impressions on category and comparison queries; assisted conversions; citation rate on a fixed prompt set with a confidence interval; sales-cycle feedback on "how did you hear".

## Checklist
- [ ] 10 core queries mapped to owner URLs; no two URLs share an intent.
- [ ] Pricing, integrations and docs indexable, rendered in HTML, current.
- [ ] Each comparison page dated, sourced and reviewed by someone accountable.
- [ ] App, staging and preview environments are noindex or behind auth, and out of the sitemap.
- [ ] Organization facts identical across site, docs, directories and review profiles.
- [ ] AI crawler policy decided and documented (`../playbooks.md` 7).
- [ ] Each post has an asset (screen, data) and one relevant CTA.
- [ ] Measurement: organic conversion events tested end to end.

## Sources
#1, #2, #9, #10, #13, #29, #33 plus `../geo-ai-search.md`; diagnosis tree 10 (AI citation) in `../diagnosis-playbook.md`.
