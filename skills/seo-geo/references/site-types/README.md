# Site types: selector

Pick the profile from the current project's signals first; the request second. Project signals win over what the person says, and mixes are normal (a SaaS with a blog and an app; a shop with a local store). Open every profile that matches and take the stricter rule where they differ. Source numbers (#n) point to `../BIBLIOGRAPHY.md`.

| Signal in the repository or site | Profile |
|---|---|
| `/locations/`, `/stores/`, opening hours, a street address, phone as primary CTA, Maps embed, `LocalBusiness` data, service-area text | `local-business.md` |
| `/product/`, `/products/`, `/cart`, `/checkout`, SKU, price, stock, variants, Stripe or shop SDK, category pages with filters | `ecommerce.md` |
| `/pricing`, `/docs`, `/integrations`, `/changelog`, `/signup`, `/login`, `/app`, "book a demo", free trial | `saas-b2b.md` |
| `/blog`, `/articles`, `/news`, bylines, categories, tags, archives, ad slots, newsletter, `Article` data | `publisher-content.md` |
| user-generated listings, `/listing/`, `/profile/`, `/search?`, many entity pages from a database, reviews from users, two-sided accounts | `marketplace-directory.md` |
| store links (App Store, Google Play), `apple-itunes-app` meta, `assetlinks.json`, `apple-app-site-association`, bundle id, deep links, app screenshots | `app-aso.md` |
| `/en/`, `/de/`, `[locale]` routes, i18n config, `hreflang`, several country domains or currencies | `multilingual-international.md` |

Rules for choosing
1. Read routes, sitemap, templates, metadata code and the analytics events before asking questions; state the profile and the signals that led to it.
2. No signal in the repository: use the request, then ask one question (what is sold, to whom, where, in which languages).
3. Count templates, not pages: the types of page that carry the traffic decide the profile order. List 3-5 templates and give each its profile.
4. Mixes: an app with a marketing site is `app-aso` plus `saas-b2b` (web) plus `multilingual-international` if localised; a restaurant with online ordering is `local-business` plus `ecommerce`.
5. Multilingual is a layer on top of any other profile, not an alternative to it.
6. Each file has: what matters most, page templates, structured data, pitfalls, metrics, checklist, sources. Structured data types are candidates: confirm in the gallery [#28] before implementing, rich results change.
7. Cross-cutting rules (people-first content, spam policies, crawling, canonicals, AI crawler policy) stay in `../../SKILL.md`, `../technical-seo.md` and `../playbooks.md`.
