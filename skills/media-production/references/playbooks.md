# Playbooks: selector, brief, routines, QA, cost and time

Tags as in `SKILL.md`. Costs and times are planning numbers with stated assumptions; replace them with your own log after three pieces.

## 1. Selector by goal, deadline, budget and rights
Answer five questions, then read the row.
1. Goal and where it runs (paid ad, organic, product page, series, launch).
2. Deadline (hours, days, weeks).
3. Budget (cash and your hours).
4. Rights (do you own faces, voices, music, brand assets; is paid promotion involved).
5. Must anything be exact (real product, UI, a real person)?
| Situation | Pick | Why |
|---|---|---|
| Ad or launch, real product visible, deadline under 48 h | Live footage or screen recording + stock B-roll + captions | Exact product, no consistency risk |
| Mood, concept, background, B-roll nobody inspects, small budget | AI images, light animation | Cheapest per scene |
| Recurring character, 20+ pieces, exact repeat | 3D (Blender) or a trained reference workflow | Near-zero marginal cost after setup |
| Same template, many variants (names, prices, locales) | Video by code (Remotion/ffmpeg + JSON) | Rerender from data |
| Site or repo to launch video | Code-made video with real screen captures | True to the product |
| No faces, voice or brand rights available | Stock with a clean licence or AI with commercial terms and no real likeness | Rights first |
| Real person endorsement | Real shoot with a release, never AI likeness | Consent and law |
| Explainer with voice | Script, TTS or recorded voice, screen and diagrams, captions | Cheap, clear |
Rule: pick the cheapest route that keeps the exact parts exact; mix routes in one piece (real product shot + AI background + code captions).

## 2. Production brief (fill before generating)
Goal and metric; platform and ratio; length; one-sentence promise; audience; must-show real elements; claims and their proof; style block; characters (sheet reference); voice (who, consent); music (licence); captions language; legal labels; deadline; budget; approver; where files go.

## 3. Routine: AI image series piece
Script and shot list, continuity table, character sheet (once), one test frame per location, batch, QA and pick, upscale hero frames, light animation, captions as layers, assemble, loudness, QA checklist, label, export, log tools and cost.

## 4. Routine: Blender episode
Spec JSON per scene (pose, expression, camera preset, background), dry-run one frame, measure render seconds, batch render, review contact sheet, assemble, finish as above. Change the spec, never the rig mid-season.

## 5. Routine: launch video from a site or repo
Read project and site; list 3 true proof points; capture real screens; storyboard 15-30 s; JSON of beats; render 9:16 and 16:9; music licensed; QA; share copy (short caption, link, label if needed); hooks and copy to `viral-content` and `copywriting`.

## 6. Cost and time per piece (worked, assumptions stated)
Assumed hourly value of your time: 30 per hour. Replace.
| Route | Cash | Time | Total at 30/h |
|---|---|---|---|
| AI images: 18 scenes x 3 attempts x $0.04 + 5 clips x $0.60 | 2.16 + 3.00 = $5.16 | 3 h | $95.16 |
| Blender episode after setup: render 18 frames x 40 s = 12 min | about $0 | 1.5 h | $45 |
| Blender setup (once) | $0-50 assets | 30 h | $900-950 |
| Code-made launch video from a site | $0 + licence if required | 4 h first, 1 h per variant | $120 first |
| Live shoot, 1 person, 1 product | gear/location variable | 6 h (plan, shoot, cut) | $180+ |
Break-even Blender vs AI: setup 900 / (95.16 - 45 = 50.16 saved per piece) = 18 pieces. Time per piece depends on your attempts per kept image; log it.

## 7. QA checklist before publishing
- Spec: ratio, resolution, length, codec, file size, safe area, captions inside it.
- Picture: hands, faces, drift against sheet, text artifacts, brand marks, background logic, continuity.
- Facts: every claim, number, price and product detail is true and on screen as real text.
- Audio: voice clear, music ducked, no clipping, loudness at target, plays on phone speaker, silent-start check (reads on mute).
- Captions: names and numbers correct, timed, not in platform UI zone.
- Rights: stock licence kept, music plan covers use, releases signed, voice consent filed, no real likeness without consent, no trademarks.
- Labels: platform AI field set, on-screen line if realistic, C2PA data kept.
- Accessibility: contrast, caption language, flashing content.
- Final: watch it once on a phone at full length; first 3 s and last 3 s; file name, version, log.

## 8. Review agenda (after 3 pieces)
Attempts per kept image, minutes per piece, cash per piece, defects found in QA, rework reasons, which route had the cheapest exact result, next change to the style block or the template.
