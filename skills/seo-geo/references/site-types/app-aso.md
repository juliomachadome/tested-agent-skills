# Mobile apps and App Store / Google Play optimisation (ASO)

## What matters most
Store search is its own engine. Apple lists text relevance (title, subtitle, keywords, category) plus behaviour (downloads, ratings, reviews) as inputs [#44]; Google Play documentation warns against repetitive or irrelevant keywords in name and descriptions [#45, #47]; its ranking inputs were not read. The web side links the two: a website that explains the app, deep links and a landing page for web search.
- Name, subtitle or short description, and keywords carry relevance; the icon, first screenshots and rating carry conversion.
- Localise the whole listing per market in natural language, not machine output.
- Product page testing: Apple product page optimisation and custom product pages [#43]; Play listing experiments exist in the console but were not read this pass.

## Page templates
- Store listing (Apple): name, subtitle (up to 30 characters per Apple's docs read), promotional text, description, keyword field (hidden), up to 10 screenshots with the first 1-3 visible in search, app preview, category, in-app events, custom product pages with their own keywords [#43, #44].
- Store listing (Play): title, short description, full description, graphics and video, category and tags [#45-47]. Check current limits in the console before writing.
- Web: an app landing page per app with the same name, a clear description, screenshots, store badges, links with `apple-itunes-app` and Android app links; help and privacy pages; a blog or guides for web search intent.

## Structured data (candidates)
Web page for the app: `SoftwareApplication`/`MobileApplication` with `operatingSystem`, `applicationCategory`, offers; rating only from real store data shown on the page [#10]. Store pages need no schema; follow the store's metadata fields.

## Pitfalls
- Keyword stuffing, competitor names or irrelevant terms in the title or description (suspension risk [#47]).
- Repeating words across title, subtitle and keyword field (wasted space, per store guidance).
- Rating prompts gated by sentiment or incentivised reviews.
- Screenshots that do not show what the app does; misleading claims.
- Translating keywords literally instead of researching local search terms.
- Not syncing web and store: different names, claims or prices.
- Ignoring crash rate and ratings, which feed ranking and conversion.
- Deep links that fail on the web fallback.

## Metrics
Impressions, product page views, conversion rate (views to installs), installs by keyword and source, retention at day 1 and 7, ratings and review rate, crash-free sessions, custom product page conversion, web-to-store clicks.

## Checklist
- [ ] Research local keywords per market; use the title, subtitle (or short description) for the top terms.
- [ ] First 3 screenshots show the core value; localised.
- [ ] Rating prompt after a success moment, no gating.
- [ ] Custom product pages or experiments for 1-2 audiences with a stated hypothesis.
- [ ] Web landing page, store badges, smart banner and deep links tested.
- [ ] Review and crash monitoring weekly; replies to reviews.
- [ ] Metadata updated with versions on a schedule; changes logged with dates.
- [ ] Verify limits in the consoles before submitting (not hard-coded here).

## Sources
#43 Apple product page, #44 Apple search, #45-47 Play Console help, #10 software app data; `../beyond-google.md` ASO section. Not read: store-specific character limits other than Apple's subtitle and screenshot counts.
