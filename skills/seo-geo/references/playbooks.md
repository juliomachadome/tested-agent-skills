# Playbooks: repeatable SEO and GEO routines

Each routine says when to run it, the steps, and what to record. Rules carry tags: **[C]** official docs, **[M]** study with a method, **[F]** practitioner, **[X]** myth. Source numbers (#n) point to `BIBLIOGRAPHY.md`. Site-type specifics are in `site-types/`.

## 1. Query research in the audience's language
When: before any new page or section. Output: a table of real phrasings, intent and an owner page.
1. Fix market and language: country, `hl`/`gl`, device. Work in a private window; note the date.
2. Collect phrasing, not translations: autocomplete (letters a-z after the stem), "People also ask", related searches, Search Console queries for the site, support tickets, sales calls, forum and review wording in that language. Local terms differ by country (same language, different word) [F].
3. Classify intent: know, compare, do, buy, local, navigate. Open the top 10 and note page types that win; a SERP of product pages means a guide will not rank [C #1].
4. Volume only from real sources (Keyword Planner, Search Console impressions, Bing Webmaster); autocomplete shows phrasing, not volume [X if used as volume].
5. Map each query cluster to one URL (one intent, one URL). A query with an existing owner page means update, not new page.
6. Score: business value 0-3, demand evidence, gap you can fill (own data or asset), difficulty from who ranks. Publish nothing below a total you set in advance.
Record: queries, date, SERP types, chosen owner URL, rejected queries and why.

## 2. Content brief (compact)
Full template: `writing-for-search.md` section 7. Before filling it, answer three gates; any "no" means do not write.
- Is there an asset or analysis the top 10 lacks (product screens, measurements, local data, a real case)?
- Is the intent not already owned by an existing URL on the site?
- Can an accountable person (or the organisation) sign it?
Then fill: query and intent, audience and language, owner URL, answer-first sentence, H2s as real sub-questions, sources with links, entities, internal links in/out, schema type that matches visible content, one CTA, read dates at 4 and 8 weeks. Texts in a language the approver does not read come with a faithful translation.

## 3. Pre-publish SEO/GEO gate
Return "approved" or the missing items, each with its rule. Check on the rendered page, not on the draft.
- Content: answers the query in the first sentence; each number has a named, linked source; facts checked by hand including title, description and alt; true authorship; not a twin of another page; no keyword stuffing.
- Technical: status 200, indexable, self-canonical absolute URL, in sitemap with real `lastmod`, text in initial HTML, one H1, unique title and description, 2-4 contextual internal links plus at least one inbound link from an older page, images with alt and dimensions.
- Structured data: type exists for a feature or helps machines, matches visible content, validates in the Rich Results Test or schema.org validator [#27].
- Experience: LCP, INP, CLS in "good" on mobile field or lab proxy; no intrusive overlay; CTA matches the topic.
- AI: search crawlers allowed by robots and CDN; no `nosnippet` on the answer; brand and entity names consistent.
- Publish: URL Inspection, IndexNow for Bing/Copilot (Google does not use it), note the date.

## 4. Site migration checklist
Run for domain change, URL restructure, HTTPS, CMS or framework change. [C #11]
Before: crawl the old site (URL, status, canonical, title, inbound links); export 16 months of Search Console and analytics; pick top pages by clicks and by links; write the 1:1 redirect map (old to closest equivalent; never mass-redirect to the home page); freeze content edits; lower DNS TTL; prepare staging with noindex or auth (never robots-only) and a crawl of it.
Launch: 301/308 redirects live, no chains; remove staging noindex and robots blocks (the most common failure); canonical, sitemap, hreflang, structured data and internal links use new URLs; robots.txt of the new host; verify the new property; Change of Address for domain moves; analytics and tag tested; update Business Profile, app links, ads, feeds, social bios, email templates.
After (day 1, 7, 28): status codes of the top 200 old URLs, redirect map hit rate, Search Console index coverage on the new property, crawl errors, clicks vs baseline (accept a dip, investigate a gap that persists past 4 weeks). Keep redirects at least 12 months. Do not change content, URLs and design in one go if you can avoid it [F].

## 5. Quarterly refresh and prune
1. Export pages with clicks, impressions, position, last substantive update, conversions for 16 months.
2. Bucket: winners (protect), decliners (clicks down 4+ weeks), stable, zero-value (no clicks, no links, no conversions).
3. Decliners: reopen the SERP; what do ranking pages add now? Update with real new material (data, steps, screens), then change the visible date and `lastmod`. A date bump alone is a search-first signal [C #1].
4. Zero-value: improve if the query has demand; merge into a stronger URL with 301; or 410. Never leave thin pages indexable in bulk [C #2].
5. Record each change and read it at 4 and 8 weeks; do not judge earlier than 4 weeks.

## 6. Internal linking pass
1. Crawl: inbound internal link count and click depth per indexable URL; list orphans and URLs deeper than 3 clicks that should rank.
2. Hubs: for each topic, a hub that links to every child and each child links back with a descriptive anchor; links are real `<a href>` [C #22].
3. For each new or updated page: 2-4 body links out, and at least one link in from an older, relevant, crawled page. For each money page: top 3 content pages that link in.
4. Fix anchors ("click here" and exact-match stuffing both fail); one link per target per paragraph is enough; no ideal count exists [X for any fixed number].
5. Remove or nofollow nothing for "sculpting"; fix navigation, breadcrumbs and related blocks at the template.
Record before/after depth and the pages that gained links; read impressions on those pages at 4 weeks.

## 7. AI crawler policy
Three separate decisions, owner decides, change robots.txt only with that decision. Document it in the repo.
| Goal | Token (verify in the docs, they change) | Note |
|---|---|---|
| Appear in ChatGPT search | `OAI-SearchBot` allow | Governs search appearance; `GPTBot` is the training decision [#60] |
| Opt out of OpenAI training | `GPTBot` disallow | Does not remove you from ChatGPT search if OAI-SearchBot is allowed |
| User-initiated ChatGPT fetches | `ChatGPT-User` | Fetches on a person's request; control may differ from search |
| Anthropic search, user fetches, training | `Claude-SearchBot`, `Claude-User`, `ClaudeBot` | Three separate robots [#61] |
| Perplexity search | `PerplexityBot`; user actions `Perplexity-User` | [#62] |
| Gemini training and grounding outside Search | `Google-Extended` | Not a crawler string; does not affect Search or AI Overviews [#14] |
Practice: robots.txt is a request; test with logs; a CDN or WAF can block bots that robots allows (check the bot-protection setting); blocking Googlebot or Bingbot removes you from their AI answers. `llms.txt` is a proposal by a third party [#63]; Google says it is not needed [#33]; keep it only if generated and identical to the pages. Review the table when a vendor changes its docs (quarterly).

## 8. Weekly Search Console and Bing review (30 minutes)
1. Step 0 from `diagnosis-playbook.md` (property, range, calendar).
2. Performance, last 7 vs previous 7 days and 28 vs 28: clicks, impressions, CTR, position, split brand/non-brand and device. Flag moves over about 20% on pages with real volume.
3. Top 10 pages and top 10 queries that gained or lost; open one SERP for each big loser.
4. Page indexing: new "not indexed" reasons, sitemap submitted vs indexed, spikes of 404 or 5xx; Crawl stats response time.
5. Core Web Vitals and Search Generative AI reports if present [#35]; Bing Webmaster performance, AI performance if available, IndexNow submissions.
6. Manual actions and security issues: empty is the goal.
7. Write 3 lines: what moved, why (or not verified), one action with an owner and a date.

## 9. SEO-safe A/B tests
[C #20] Google's guidance: do not cloak (show Googlebot what users see on the same URL logic), use `rel=canonical` on variant URLs pointing to the original (not noindex), use 302 for redirect tests and remove variants and redirects when finished, run tests only as long as needed.
- Prefer client or server variants on the same URL with consistent content for crawlers; rendered text must exist in the initial HTML for the control.
- Variant URLs: canonical to control; keep them out of the sitemap; no internal links to them.
- Do not test titles on a whole template without a holdout: split pages into matched groups (same template, similar clicks) and compare change vs control group, 2-4 weeks, with seasonality caveats [F].
- Read search metrics (clicks, CTR, position) and business metrics (conversions) separately; a conversion win with a clicks loss is still a loss to decide on.
- Never keep the winning variant by forgetting the loser live.

## Appendix A: myths and weak evidence
| Claim | Verdict |
|---|---|
| Ideal article length | [X] length is what the question needs |
| Meta keywords help | [X] ignored |
| Duplicate content gets a penalty | [X] inside a site it is inefficiency; copying others is a spam policy matter |
| E-E-A-T is a ranking factor | [X] literally; trust matters in quality systems |
| A person author with photo and bio is required | [X] organisations are accepted; invented personas are deception |
| AI content is punished for being AI | [X] scale without value is |
| FAQPage gives a rich result | [X] since 07/05/2026 |
| HowTo gives a rich result | [X] not in the gallery |
| Course schema gives rich results in any language | [X] list is English-only and needs 3 courses (at 12/11/2026) |
| llms.txt makes AI cite you | [X] for Google; [M] no measured effect overall |
| Chunk text for AI; special schema for AI | [X] per Google [#33] |
| SEO is dead, GEO replaces it | [X] still SEO |
| Blocking GPTBot removes you from ChatGPT search | [X] OAI-SearchBot decides |
| Google-Extended removes you from AI Overviews | [X] does not affect Search |
| AI crawlers read what JavaScript builds | [M] in Dec 2024 most did not [#64] |
| IndexNow speeds Google indexing | [X] Google does not participate |
| Changing the date keeps content fresh | [X] and a bad signal |
| Heading order or count affects ranking | [X] |
| Keywords in domain or URL rank | [X] almost no effect |
| Sitemap priority and changefreq help | [X] ignored |
| noindex on test variants is safest | [X] use canonical |
| Statistics, quotes, named sources raise AI visibility | [M] controlled study, 2023 [#65] |
| Brand mentions make AI cite you | [M] strong correlation, causation unproven [#67] |
| AI visitors convert far better | [F] partial method, no replication |
| Autocomplete shows the highest-volume queries | [X] |
| Green Core Web Vitals lift rankings | [M] recommended; weight unknown |
| A tool measures my AI visibility | [X] estimate; first-party data only in Search Console and Bing Webmaster |
| More internal links are always better | [X] |

## Appendix B: 2026 change log (read #37 and #31 before relying on dates)
| Date | Change |
|---|---|
| Jan 2026 | "Practice problems" structured data removed |
| Feb 2026 | Bing rewrote guidelines (names GEO, bans prompt injection and AI-engineered language); AI Performance report in preview (trade coverage) |
| Mar 2026 | Brand-query filter in Search Console for all |
| Apr 2026 | Back-button hijacking added to spam policies |
| 07/05/2026 | FAQ rich result no longer shown for any site |
| 15/05/2026 | Google's guide to optimising for generative AI features [#33] |
| Jun 2026 | Search Generative AI report [#35]; Google states llms.txt not needed |
| Jul 2026 | Search Console platform properties (YouTube, Instagram, TikTok, X) |
| 30/08/2026 | Site reputation manual action no longer applies for users in the EEA; policy continues elsewhere [#36] |
| Oct 2026 | Google's AI guide points to rater-guideline sections 4.6.5 and 4.6.6 [#39] |
Ranking updates reported by trade press in 2026 (not verified here): spam 24/03, core 27/03, core 21/05, spam 24/06.
