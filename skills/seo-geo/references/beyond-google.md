# Beyond Google: other engines, surfaces and stores

Principle: each surface has its own index, its own owner-verified console and its own spam rules. The shared base is the same: useful original content, clean crawlable HTML, consistent entity data (name, address, brand, product). Tags as in SKILL.md. "Vendor evidence" = a tool vendor's own data, not first-party.

## Bing, Copilot and IndexNow
- **[C]** Bing Webmaster Tools gives first-party data (clicks, impressions, crawl, index coverage; AI performance reports where available). Import the Search Console property to start.
- **[C] IndexNow:** an open protocol (Microsoft Bing, Yandex, Naver, Seznam and others participate; Google does not) where the site pings changed URLs with a key file hosted on the domain. Send on real create, update or delete only; one ping per change, batch where supported. It speeds discovery, it does not improve ranking. Keep a normal sitemap with true `lastmod`.
- **[C]** Bing Webmaster Guidelines mirror Google's on spam (cloaking, scaled low-value content, link schemes); Bing has said it penalizes text built to manipulate AI citation.
- Copilot answers draw on the Bing index: being indexed, snippet-eligible and clear in the first sentence matters more than any special tag.

## AI answer engines and GEO
- **[M] Aggarwal et al. (2023, KDD 2024)** tested "generative engine optimization" methods on a benchmark: adding citations to credible sources, quotations and statistics raised visibility in generated answers, keyword stuffing did not; results vary by domain and the test engine is not a production system. Treat as direction, retest on your own queries.
- **[C]** Google AI Overviews and AI Mode retrieve from the normal index; no extra markup is required. See `geo-ai-search.md` for crawler names and the controls.
- Practice: answer-first sentences, verifiable facts with named sources, entity-clear naming, up-to-date pages, brand mentions on reputable third-party sites. Track by sampling real prompts monthly and logging which pages and sources are cited; the sample is small and variable, so record the date, the prompt and the engine.

## Local
- **Google Business Profile [C]:** verified, accurate name (real-world name, no keyword stuffing), category, address or service area, hours, photos, products or services, reviews answered. Rules forbid fake locations, virtual offices posing as storefronts, incentivized reviews.
- **Apple Business Connect [C]:** claim the place card for Apple Maps and Siri; add hours, photos, showcases. Free.
- **Bing Places [F]:** create a listing or import it from Google Business Profile (now at bing.com/forbusiness); feeds Bing Maps and Copilot local answers. Import and instant verification described in third-party guides, not read on a Microsoft help page (16/11/2026).
- Consistency of name, address and phone across these and the site is the main local signal [M]. Local landing pages need unique value, not one swapped city name (doorway policy).

## App stores (ASO)
- **Apple App Store [C]:** title (30 chars), subtitle, keyword field (100 chars, hidden), screenshots and video, ratings, in-app events and custom product pages. Metadata is indexed; keyword stuffing is rejected in review.
- **Google Play [C]:** title, short description, full description (indexed text), graphics, ratings, installs and retention; the algorithm weighs engagement signals such as uninstall rate.
- Both: localize the whole listing per market in the native language, not machine output; ratings and review prompts must follow store rules (no gating by sentiment); measure with the store's own console. Reference: Apple product-page and search guidance, Google Play listing guidance (see BIBLIOGRAPHY).

## YouTube
- **[C]** Search and suggested rank on audience satisfaction (watch time, clicks, surveys) as described by YouTube; the title, thumbnail and first 30 seconds must promise and deliver the same thing.
- Use chapters, accurate captions or transcripts, a descriptive title and description, and the on-site embed. No misleading thumbnails (policy violation). Video structured data for pages that host videos: `structured-data.md`.

## Social search (TikTok, Instagram, Pinterest)
- **[M]** Younger audiences use these as search engines; each indexes captions, on-screen text, spoken words, hashtags and alt text, and ranks mainly on engagement. Vendor evidence only for most size claims.
- TikTok and Instagram: say the keyword phrase in the first seconds and in on-screen text and caption; Pinterest: keyword-rich pin titles and boards, evergreen vertical images, link to a page that matches the pin. Pinterest content lives longer than feeds.
- Treat as discovery, not as an owned asset; send the reader to a page you control.

## Marketplaces
- Amazon, Etsy, Mercado Livre, Allegro and others rank mostly on conversion and sales velocity, relevance of title and attributes, price, availability and reviews [M, vendor evidence]. Fill all attributes, answer questions, keep stock accurate, never buy reviews (platform bans and consumer-law exposure).

## Regional engines
| Engine | Console | Notes |
|---|---|---|
| Yandex (RU) | Yandex Webmaster | Supports IndexNow; strong in Russian-language sites; regional targeting and Turbo-era features have changed, verify in docs |
| Baidu (CN) | Baidu Search Resource Platform (Ziyuan) | [F] practitioner view: mainland hosting and ICP filing usually needed; mobile-first; submit via the platform (platform needs a login, not read) |
| Naver (KR) | Naver Search Advisor | [F] practitioner view: its own blog and cafe verticals weigh heavily; supports IndexNow (indexnow.org) |
| Seznam (CZ) | Seznam Webmaster | [F] SeznamBot is described as honouring robots.txt (help page moved, not read); supports IndexNow (indexnow.org) |
Markets move: check the engine's own docs before investing; use native-language reviewers.

## Image search
- **[C]** Google Images: descriptive file names, alt text in the page language, text near the image, `ImageObject` or standard markup, responsive formats (WebP or AVIF) with width and height, an image sitemap when the images are discovered by script. Do not hide the only copy of a fact inside an image.

## Controlling AI crawlers
Separate three decisions: appear in search answers, be used for training, allow user-initiated fetches. Example robots rules (verify each bot's current name in its docs):
```
User-agent: OAI-SearchBot      # ChatGPT search
Allow: /
User-agent: GPTBot             # OpenAI training
Disallow: /
User-agent: Google-Extended    # Google training/grounding outside Search
Disallow: /
User-agent: ClaudeBot          # Anthropic training
Disallow: /
```
robots.txt is a request, not enforcement; user-initiated agents may ignore it; a firewall rule can override it. Check server logs. Blocking Googlebot or Bingbot removes you from their AI answers too.

## llms.txt: contested
A proposed Markdown index for agents. Google has said it does not use it for Search; one large correlational study found no link to citation. Not a GEO tactic. Keep if auto-generated; never put content there that differs from the pages. See `geo-ai-search.md`.
