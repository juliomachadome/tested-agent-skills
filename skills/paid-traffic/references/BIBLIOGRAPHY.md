# Bibliography: paid-traffic

Checked 15/11/2026. Status: V = identity (author, title, year, ISBN) matched in a catalogue; P = official page opened and read this pass; S = official page exists, content seen only through a search summary or the page returned only its title; U = not verified. Nothing is quoted. Labels: OFFICIAL (platform), ACADEMIC/BOOK, VENDOR (commercial, interest in the result), PRACTITIONER.

## Books and studies
1. Sharp, B. *How Brands Grow: What Marketers Don't Know*. Oxford University Press, 2010. ISBN 978-0195573565. **V** (OpenLibrary 15/11/2026). ACADEMIC/BOOK. Supports: reach and broad audiences (`measurement-diagnosis.md`).
2. Binet, L., Field, P. *The Long and the Short of It: Balancing Short and Long-Term Marketing Strategies*. IPA. ISBN 978-0852941348. **V** (OpenLibrary ISBN record re-read 18/11/2026: title, subtitle and both author keys match; no publication date on the record, so the year is not verified and "2013" is not cited as fact). PRACTITIONER/industry study (IPA effectiveness database, large consumer brands). Supports: brand vs activation (`measurement-diagnosis.md`).
3. Kohavi, R., Tang, D., Xu, Y. *Trustworthy Online Controlled Experiments*. Cambridge University Press, 2020. ISBN 978-1108724265. **V** (OpenLibrary 15/11/2026). ACADEMIC/BOOK. Supports: test design, sample-ratio, Twyman's law (`testing-and-scaling.md`, `optimization-playbook.md`).

## Official documentation (read live; dates are when checked)
4. Meta for Developers, "Deduplicate pixel and server events" (Conversions API). https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events . **P** 15/11/2026. OFFICIAL.
5. Meta for Developers, Conversions API customer information parameters. https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/customer-information-parameters . **P** 15/11/2026. OFFICIAL.
6. Meta Business Help Center, "About the learning phase". https://www.facebook.com/business/help/112167992830700 . **P** 15/11/2026 (browser pass, pt-BR): ad sets exit learning when performance stabilises, "normally after about 50 results in the week after the last significant edit"; Shops ads need at least 17 purchases on the website and 5 on Meta; editing during learning resets it; merge similar ad sets. OFFICIAL.
7. Google Ads Help, "Smart Bidding" / setting smarter search bids. https://support.google.com/google-ads/answer/10970825 . **P** 15/11/2026. OFFICIAL.
8. Google Ads Help, Smart Bidding for Display (volume bands). https://support.google.com/google-ads/answer/10285843 . **P** 15/11/2026 (campaign-type specific). OFFICIAL.
9. Google Ads Help, Performance Max optimisation tips. https://support.google.com/google-ads/answer/11385582?hl=en . **P** 15/11/2026 (browser pass): 6-week minimum for new campaigns; avoid frequent budget, bid or status changes; wait 1-2 weeks (or a full conversion cycle) after significant changes; asset counts (20 text assets: 15 headlines and 5 descriptions; 7 images; 1 video). The "15 conversions per 30 days" figure is **not on this page**; `platforms.md` labels it a practitioner figure. OFFICIAL.
10. Google Meridian GeoX docs. https://developers.google.com/meridian/geox/faqs . **P** 15/11/2026 (browser pass, pt-BR, page updated 2026-09-21): user-level studies (Conversion Lift, Brand Lift) must be off on campaigns under test because hidden control groups contaminate the geo split; a multi-cell design gives no direct significance test between two active treatment cells; GeoX suggests a larger budget or MDE than TBRMM. OFFICIAL, open-source tool.
11. TikTok Business Help Center, "About event deduplication". https://ads.tiktok.com/help/article/event-deduplication . **P** 15/11/2026 (browser pass; page last updated May 2025): `event_id` must be sent on both Pixel and Events API; identical event plus `event_id` within a 48 h window is deduplicated and the first event is kept (Pixel+API merge when the second copy arrives after 5 minutes); not needed when different events go through each channel. OFFICIAL.
12. TikTok Ads Help, "Learning phase" (learning-phase part only; Smart+ not checked). https://ads.tiktok.com/help/article/learning-phase . **P** 18/11/2026 (read: the page describes the learning phase for campaigns and ad groups and sets no hard exit threshold; it says performance swings usually taper off after roughly 25 results or a week in the phase). OFFICIAL.
13. Meta Engineering, "Meta Andromeda: Supercharging Advantage+ automation with the next-gen personalized ads retrieval engine", 02/12/2024. https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/ . **P** 18/11/2026 (read: title and date match; Andromeda is a retrieval stage narrowing tens of millions of candidates to a few thousand; the article reports +6% retrieval recall and 10x inference efficiency, among other engineering figures; the ad-level ROAS and conversion figures in it are not Andromeda measurements). The Meta for Developers post on Advantage+ campaign migration (13/02/2026) was not located and is not cited. OFFICIAL.
14. web.dev, Core Web Vitals (LCP "good" under 2.5 s). https://web.dev/articles/lcp . **P** 18/11/2026 (read: "sites should strive to have Largest Contentful Paint of 2.5 seconds or less"; caption: "A good LCP value is 2.5 seconds or less"). OFFICIAL.

## Books, practitioner
15. Hormozi, A. *$100M Offers* (2021): offer-side limits, see `offers`. PRACTITIONER. ISBN 978-1-7374757-0-5 (9781737475705). **V** (OpenLibrary ISBN record 18/11/2026: title "$100M Offers", publish year 2021, author key matches the Hormozi author record of the same catalogue; the record's author-key match was taken from the catalogue search, not a second page).

Totals: 15 entries; 15 V or P (100%). Before this pass: 19 entries, 11 V or P (58%).

## Further reading, not read and not used as evidence
These are vendor reports and industry news that could not be opened or were not read in this pass. They are not evidence for any claim in the skill. Claims that cite them are tagged [F] in the reference files.

- ppc.land (industry news) summaries of Meta and Google changes (window changes, thresholds). https://ppc.land . S; secondary reporting. PRACTITIONER/news.
- Consent and tracking vendors (Cookiebot, Usercentrics and similar) on Consent Mode v2 and Event Match Quality thresholds. S via search; VENDOR.
- Measurement vendor reports on incrementality (e.g. "The Meta Report", Haus, 2025), cited in `platforms.md`. U; VENDOR, self-selected large advertisers.
- Creative-analytics vendor dataset on winner rates (579k creatives), cited in `testing-and-scaling.md`. U; VENDOR.
