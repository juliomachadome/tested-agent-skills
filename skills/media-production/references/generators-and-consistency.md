# AI image and video generators, consistency, prompts, cost

Tags: **[C]** consensus or law, **[M]** serious but single source, **[F]** platform, vendor or practitioner statement, **[X]** myth. Sources in `BIBLIOGRAPHY.md`. Tool names are examples; features and prices change monthly, so re-read the vendor page on the day you budget. Dated facts below were read on 18/11/2026.

## 1. What generators are good and bad at **[F]**
| Good at | Bad at (check every output) |
|---|---|
| Mood, atmosphere, backgrounds, concept frames, product-in-scene mockups, stylised characters, B-roll that nobody inspects | Hands and fingers, small text and logos, exact product details and packaging, counting objects, left/right and spatial logic, long takes (drift), real brand marks, legible UI screens |
| Fast variants: 10 looks in minutes | Identical character across 50 shots without a lock; exact repeatability |
| Image-to-video for 3-10 s of light motion (push-in, hair, smoke, water) | Fast complex motion, faces turning, hands handling objects, lip-sync to your voice unless the tool offers it |
Rule: the generator invents; anything that must be exact (price, label, UI, legal text, the real product) is a real photo, a screen capture or a text layer added in editing.

## 2. Style lock
Write a **style block** once; paste it unchanged at the top of every prompt (or store it as a preset). Parts: palette (3-5 named colours plus one accent), lighting (direction, softness, time of day), lens and angle (focal-length feel, camera height, depth of field), rendering (medium and finish), fixed negatives ("no text, no logos, no watermark"). Describe the look in your own words; never "in the style of <living artist, studio or brand>" (refusals, likeness and trademark disputes, derivative look). Version it (`style v1`) and change it between seasons only.

## 3. Character consistency
1. Generate a **character sheet**: front, side, back full body on plain background, a head row with 4-6 expressions, one row per outfit. Fix a written description (age, skin tone, hair, face marks, outfit, accessory) and paste it verbatim.
2. Reuse the same reference file and version for every scene. Re-attach it each time; do not rely on chat memory.
3. Mechanisms by family **[F]** (names are examples): reference-image or "omni reference" features in image tools; image-edit endpoints that take a reference and change the scene; character-reference features in other editors; a trained character LoRA or IP-Adapter on open weights (needs 15-30 sheet images, GPU time, and a check of the base-model licence); a fixed seed only repeats one shot, it is not a character lock.
4. Keep background-only and insert shots (hand, note, phone) free of faces: no face, no drift.
5. If the same face must appear in hundreds of shots from any angle, use 3D (`blender-pipeline.md`) or a real person with a release.
Dated fact: BFL lists FLUX.1 Kontext [pro] at $0.04 and [max] at $0.08 per image on its pricing page (bib. 5, read 18/11/2026).

## 4. Prompt structure per shot
```
[STYLE BLOCK v1]
SHOT: <extreme close-up | medium | wide | over-the-shoulder | insert>, <angle>
SUBJECT: <name + fixed description> (reference attached)
ACTION: <one verb, one moment>
SETTING: <place, time of day, 2-3 concrete objects>
MOOD/LIGHT: <one or two words>
CONTINUITY: <wardrobe, props, what changed since the previous shot>
FRAMING: <9:16 | 1:1 | 16:9>, subject in the safe area, empty space where captions go
NEGATIVE: no text, no logos, no extra fingers, no watermark
```
One idea per image. For video prompts add: camera move (one only), duration, what must not move, first frame image attached. Keep a **continuity table** per piece: shot id, location, time, wardrobe, props in hand, light direction, expression.

## 5. Iteration cost
Cost per kept image = attempts per kept image x price per attempt. Track attempts for the first three pieces; it is the number that moves the bill.
- Worked example (assumed attempt counts, list price from bib. 5): 18 scenes x 3 attempts = 54 images x $0.04 = $2.16. A new character sheet, about 10 attempts, adds $0.40.
- Subscription tools invert the math: monthly price / pieces per month; count queue and relax-mode limits.
- Image-to-video: assumed $0.30-1.00 per 5 s clip (replace with your invoice); use clips only for the hook and the payoff, 4-6 per piece, and check every clip frame by frame.
- Free motion (push-in, parallax, shake) in the editor or in code costs nothing and is often enough.
- Free tiers are for testing: one vendor read here gives 125 one-time credits on its free plan (bib. 10); do not plan a production on them.

## 6. Upscale, light animation, text
Upscale only the hero frames. Slow push-in held 2-4 s per scene reads as motion. Captions, counters, prices, UI and logos are real text layers, never generated pixels.

## 7. Picking a tool (decision order)
1. Rights: does the plan include commercial use, and does it exclude real-person likeness and brands? Read the terms page; keep the plan name, date and a copy. 2. Consistency need: single hero shot (any tool) or a recurring character (reference features, LoRA or 3D). 3. Control: API or batch for volume; chat UI for exploration. 4. Price per kept output, not per attempt. 5. Output ratio and resolution native to the platform. Run the same 3 test shots in two tools before committing.
