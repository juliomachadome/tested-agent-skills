# Query research, content-to-product, measurement, video, Bing

## Query research in any country and language
- **[C]** Check search-engine share by country and month (StatCounter). Where Bing exceeds ~5%, the low effort of Bing Webmaster + IndexNow pays; where a strong local engine exists (Yandex, Naver, Baidu, Seznam), it enters the plan.
- **[C]** Check whether and since when AI Overviews and AI Mode exist in that language and country (local Google blog). AI Mode reached 200+ countries and territories in Oct 2025. Studies from before local launch do not apply after it.
- **[M]** AI answers mostly simple definitional queries and rarely transactional ones. One EU-market study (Aug 2025): AI Overview on 24% of phrases; "know simple" 58%, "know" 31%, "do" 7%; by funnel, top 33%, middle 14%, bottom 5%. US panel (Mar 2025): 18% of searches. Numbers change by country and over time; the ordering (definition > comparison > purchase) is what guides the plan.
- **[M]** AI use varies a lot by age and country: use representative local surveys before assuming the audience asks ChatGPT; for older audiences classic search usually remains the largest source.
- **[C]** Autocomplete reflects real searches adjusted for language, location, trends and history; it is **not** a volume ranking. Use it to find real phrasing (with the market's `hl` and `gl`, private window). Volume only from Keyword Planner or Search Console.
- **[F]** "People also ask" boxes carry real questions useful as subheads; check the live SERP, do not copy from tools.
- **[C]** Write in the reader's natural language with the query as they type it, not a translated keyword from another language. Engines understand synonyms and inflections: the keyword goes where natural (title, first sentence, one subhead).
- **[M]** On commodity topics (definitions, rules, tables) reference sites dominate (Wikipedia, dictionaries, government, big portals). A small site only gets in with an angle they lack: own data, the audience's typical error, a tool, a product example.

## From content to product
- **[M] Business potential (0-3):** 3 when the product is almost the solution; 0 when it cannot be mentioned. Mark it in the brief; topics at 0-1 only as fact or brand pages.
- **[C] Prove with real assets** (images, audio, measurements, pros and cons, who it is for), as Google asks for reviews. A sample, never the whole paid material.
- **[M] Banner blindness:** users ignore what **looks like an ad** (coloured boxes, text in images, top and sidebar). In-text calls to action work better looking like content and continuing the paragraph.
- **[C]** One main call to action per page, tied to the topic, leading to the next funnel step, promising only what the destination delivers.
- **[M] Role by stage:** top (definitions) earns citations and brand, few clicks, light CTA; middle (method, comparison, how-to) has the best click-vs-AI balance, diagnostic CTA; bottom (product page, price) converts. Weight the plan to middle and bottom.

## Measurement
- **[C] Search Console:** Web performance per page and page group (clicks, impressions, CTR, position), which already includes AI features; and the dedicated **Search Generative AI** report (impressions of URLs in AI Overviews, AI Mode and Discover AI by page, country, device, date; no clicks, no queries). Google: "No third-party tool has access to our internal ranking or AI systems." (report for all sites since 31/08/2026)
- **[C] Bing Webmaster AI Performance** (public preview since Feb 2026): Copilot and Bing-summary citations by page and grounding query; no clicks; does not cover ChatGPT, Perplexity or Google. Grounding queries are also a hint for Google, which shows no queries in its AI report.
- **[M]** ChatGPT usually adds `utm_source=chatgpt.com` but not always (it briefly stopped in Oct 2026, visits falling into "direct"). Classify AI visits by UTM **and** referrer; accept some loss.
- **KPI:** product action from content pages (signup, test started, purchase) per topic group per month. Pageviews, impressions and position are diagnostics.
- **[C]** Brand-query filter in Search Console (since Mar 2026): separate brand from non-brand before concluding content grew; classification is automatic and errs.
- **[M] Reading window:** 4 and 8 weeks after publishing or changing, date noted. Actions (working thresholds, no source): position 8-20 with impressions → strengthen the direct answer, a subhead with the query, internal links; good position and low CTR → title and description, check for an AI Overview; traffic without product action → weak CTA; zero impressions in 8 weeks → revisit intent, merge or cut; two pages on one query → merge with 301.
- **[M] SEO tests are not user A/B tests:** change a group of similar pages, keep another as control, compare after 4-8 weeks; with few pages it is only an indication.
- **[F]** No official "time to rank". On new domains first impressions usually take weeks and useful traffic months. Never promise a date.

## Video and YouTube
- **[C]** In Google, a video enters video features only on a **watch page** (main purpose: that video). Articles or product pages with embedded video do not qualify; the page must be indexed and perform, the video not hidden or click-to-load, with a thumbnail at a stable URL.
- **[C]** A YouTube video embedded on the site may be indexed on both pages; **[F]** for small sites the YouTube page tends to appear, so the channel is the search asset and the embed serves the reader.
- **[C] Key moments:** labelled timestamps in the YouTube description; on your site `Clip` (all languages) or `SeekToAction` (limited languages).
- **[C] YouTube search** weighs relevance (title, tags, description, content vs query), engagement (watch time for that query) and quality (channel expertise and trust on the topic). Practice: real query in the title, answer and link in the description, chapters, reviewed captions in the audience's language.
- **[M]** YouTube is the most cited domain in AI Overviews in one vendor base: a second door to citation. Correlational.
- **[C]** YouTube AI disclosure: required for realistic altered or synthetic content; not for script, title, thumbnail, captions or clearly unreal animation. Mass same-template channels (auto voice over stills) lose monetisation under the "inauthentic content" policy (Jul 2025): same principle as scaled content abuse.
- **[C]** Search Console "platform properties" (Jul 2026) show how YouTube, Instagram, TikTok and X posts appear in Search, Discover and News.
- **[F]** Shorts: reach and brand; little search and almost no clicks to the site. A brand channel with its own metrics, not a ranking tactic.

## Bing and Copilot in one page
- **[C]** Verify the site in Bing Webmaster Tools (import from Search Console) and submit the sitemap.
- **[C] IndexNow:** notify new, changed or removed URLs; key file at the site root; GET for one URL or POST up to 10k; 200 only confirms receipt; 429 means too many. Send only real changes, after deploy. Participating engines share notifications; Google does not participate (for Google: sitemap and URL Inspection).
