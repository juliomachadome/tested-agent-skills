# Producing by code, and adapting to a new country

## Producing video by code without freezing the machine
- Standard tooling: an animated HTML page where every frame is a pure function of time, captured by a headless browser, plus ffmpeg for audio and encoding. If a code-rendered video skill is installed, it can produce story, visuals, synthesised soundtrack and render; treat its output as a draft and add what an ad needs: narration in the audience's language, captions burned inside the safe zone, end card with the ad's CTA, cover, `.vtt` file, tracked link, credits file.
- Machine-care rules:
  1. Script and storyboard approved **before** any render.
  2. Stills first: one per scene plus one mid-transition; fix overflow, collisions and contrast there.
  3. **One render at a time**, with `nice -n 10`, at most 2 capture processes; no parallel batches, no e2e tests or other browsers running alongside.
  4. 1080×1920 at 30 fps; higher resolution only with a reason.
  5. A batch is a queue: finish one, check, start the next; sample 1-2 pieces before producing the whole batch.
  6. When done: close browsers and servers, delete intermediate frames, keep only what the project versions.
- Final check on the exported file: duration, resolution, loudness, captions inside the safe zone, first frame equals cover, no language errors, no frame with invented data, price and date equal to the page that day.

## Adapting to a new market (method)
Answer with sources before the first script in a new market:
1. **Where the audience is** (daily use by platform and age) and which format it prefers: local measurement institute or the national advertising bureau.
2. **How it buys** (phone, dominant payment method, main fear) and what gives a shop credibility.
3. **Relationship with advertising and promotions** (distrust of discounts, buying dates, reaction to urgency).
4. **Register** of ad language (formal/informal, gender, accepted humour) and the language's readability tool; native review.
5. **Calendar** (commercial dates, holidays, back-to-school, new year).
6. **Law and regulator** (consumer authority, recent fines in the sector, price rule, review rule, ad labelling).
7. **What competitors run** in the country's public ad library: who has been live longest with most variations. Read the **concept** (angle, proof, format), never copy the file. If automated reading is blocked, ask the owner for ~10 screenshots.
8. **Cultural references** only locals recognise (expressions, press memes, beloved ads): gold when used lightly and validated by a native; the first place literal translation fails.

## Working with the neighbouring skills
| Neighbour | Gives the creative | Receives from the creative |
|---|---|---|
| offers | what may be said about price, deadline, guarantee, gift; what expires; decision metric | angles that call for offer changes; CPA and revenue per creative |
| copywriting | single phrase, method name, approved and banned terms, language review | script with timings, candidate hooks, audience comments |
| UI/UX design | brand, colours, type, the destination's first screen, contrast | key frames and cover for review; first-screen changes to match the ad |
| paid-traffic | budget per batch, kill and winner rules | concepts with IDs and destinations |

Order: offer defines what is true → copy defines the phrase → creative defines concept, script and storyboard → UI checks brand and legibility → production → final check. Disagreement is settled by a test, stating which hypothesis each version carries.
