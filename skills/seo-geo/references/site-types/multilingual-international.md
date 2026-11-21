# Multilingual and international sites

## What matters most
Each language or country version is a separate set of pages that must be linked correctly and be good in its own language. Machine-translated, templated duplicates are scaled content risk; unmarked alternates compete with each other. [C #5, #2]
- Choose a structure and keep it: country-code domains, subdirectories (`/de/`), or subdomains; subdirectories are simplest to maintain [F].
- Content is localised, not just translated: examples, currency, law, units, search terms.
- Every version is crawlable with real links; no automatic redirect by IP or Accept-Language alone.

## Page templates
- Language selector as links (not a script-only menu) to the equivalent page.
- Localised home, category and product or article pages; with their own titles, descriptions, slugs in the language.
- `hreflang` set on every version listing all alternates and itself, plus `x-default`, via HTML, header or sitemap (use one method consistently).
- Localised legal, delivery and payment content per market.

## Structured data
Same types as the profile (Product, Article, Organization), values in the page language: `inLanguage`, currency in `priceCurrency` per market, local `address`. Keep `@id`s and names consistent across versions [#5, #6].

## Pitfalls
- Missing return links; wrong codes (`en-UK`, `iw`); alternates that redirect, noindex or canonical elsewhere [#5].
- Same language for several countries with identical pages and no differentiation (choose one or localise).
- Machine translation published unreviewed.
- Canonical pointing every version to the English page.
- Redirecting by IP so Google only sees the US version.
- Mixed languages on a page; untranslated navigation.
- URL slugs and keywords translated literally rather than researched.
- Currency and price mismatch with structured data.
- Different engines per market (Yandex, Baidu, Naver, Seznam): verify market share and submit separately [#56-59, #71].

## Metrics
Clicks and impressions by country and language, wrong-language landing rate, index coverage per locale, hreflang errors found by crawl, conversion by market, share of locales with at least one top-10 page for non-brand queries, translation freshness (versions behind the source).

## Checklist
- [ ] Market list with language, country, currency and priority; structure chosen and documented.
- [ ] Query research per language by native speakers (`../playbooks.md` 1).
- [ ] hreflang validated by crawl: reciprocal, 200, self-canonical, x-default.
- [ ] Each locale in its sitemap section; no auto IP redirects; selector uses links.
- [ ] Native-level review of titles, headings, key pages.
- [ ] Locale-specific legal and trust content.
- [ ] Search Console property covers all versions; filter by country.
- [ ] Translation workflow keeps versions in sync and updates `lastmod` only when real.

## Sources
#5 localized versions, #4 canonical, #2 spam policies, #6 structured data, #56-59 regional engines (not read), #71 share by country; `../diagnosis-playbook.md` tree 6 for hreflang errors.
