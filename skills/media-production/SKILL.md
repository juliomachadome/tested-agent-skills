---
name: media-production
description: Use to make or choose how to make images, video, 3D, voice and music for any use (ads, organic posts, product pages, launch videos, series), and to check rights before publishing. Triggers "make a video for", "generate images for my ad", "keep the character consistent", "render this in Blender", "turn my site into a launch video", "which stock site", "AI voiceover", "can I use this music", "does this need an AI label", "cost per video". Picks the route by goal, deadline, budget and rights (AI, stock, live footage, 3D, video by code), then covers prompts, consistency, Blender JSON renders, Remotion and ffmpeg, captions, formats, loudness, QA and licences. Not for hooks and scripts (viral-content, ad-creatives), story structure (storytelling), page or ad copy (copywriting) or screen design (ui-design).
license: CC-BY-SA-4.0
metadata:
  author: Júlio Machado
  source: https://github.com/juliomachadome/tested-agent-skills
---

# Media production

Goal: the cheapest route that keeps the exact parts exact, made once, checked, and cleared to publish. Everything here serves four limits: **deadline, budget, rights, truth** (a real product, price or person must look real). Evidence tags: **[C]** consensus or law, **[M]** serious but single source, **[F]** vendor, platform or practitioner statement, **[X]** myth. Tool names are examples; prices and rules change, so the dated facts in the references were read on 18/11/2026 and must be re-read before a budget or a launch.

## 1. Start: project, then brief
Read the current project's docs first (brand, tokens, voice, claims rules, licences on file, past assets, platform and ratio, approvers); project rules win. Then get the minimum: goal and where it runs (paid ad, organic, product page, series, launch); deadline; budget in cash and hours; rights you hold (faces, voices, music, brand assets); anything that must be exact (the real product, a UI, a person); language; the platform. State assumptions where data is missing. The brief form is in `references/playbooks.md` section 2.

## 2. Pick the route (selector)
| Situation | Route | Open |
|---|---|---|
| Real product or UI, tight deadline | Live footage or screen recording, stock B-roll, captions | `playbooks.md` 1, `rights-and-labels.md` 5 |
| Mood, concept, backgrounds, B-roll, low budget | AI images, light motion | `generators-and-consistency.md` |
| Recurring character, 20+ pieces, exact repeat | 3D in Blender (headless, JSON spec) or a reference workflow | `blender-pipeline.md` |
| Same template, many variants, site or repo to launch video | Video by code (Remotion, ffmpeg) with real captures | `code-video-and-assembly.md` |
| Stock, music, voice, likeness, labels | Licences and consent first | `rights-and-labels.md` |
| Real person endorsing | Real shoot with a signed release, never AI likeness | `rights-and-labels.md` 3 |
Mix routes in one piece (real product shot, AI background, captions by code).

## 3. AI images and video **[F]**
Good at mood, backgrounds, concept frames, variants and 3-10 s of light motion. Bad at hands, small text and logos, exact products, long takes, many shots with one face. The generator invents, so anything exact is a real photo, a capture or a text layer. Method:
1. **Style block** written once, pasted unchanged, versioned (palette, light, lens, render, negatives; never "in the style of" a living artist or brand).
2. **Character sheet** first (front, side, back, expressions, outfits) plus a fixed written description; reuse the same reference file in every shot.
3. **Prompt per shot**: style block, shot, subject, one action, setting, mood, continuity, framing, negatives. One idea per image.
4. **Iteration cost**: cost per kept image = attempts x price per attempt. Worked example (assumed 3 attempts, $0.04 listed price): 18 scenes = 54 images = $2.16. Log attempts for three pieces.
5. Use video clips only for the hook and payoff; free motion (push-in, parallax) covers the rest. Details, tool families and limits: `references/generators-and-consistency.md`.

## AI tells to avoid (check while creating, not after)
- Plastic skin and waxy faces; over-saturated colour and HDR glow.
- Uncanny hands, garbled text and logos.
- Symmetrical, stock-like composition with no point of view.
- The same AI voice on every video; music picked by mood preset.
- Generic stock footage that does not show the real product.
- Fix: real product shots and people, one visual direction with a reason, consistent characters, labels where required.
- Say what you chose and why in one line (goal, audience, platform, budget, rights); a choice without a reason is removed.

## 4. 3D with Blender, headless
Use when the same character or product must look identical from any angle at near-zero marginal cost. One JSON file lists scenes (pose, expression, camera preset, background, props); a Python script reads it and renders a PNG: `Blender -b -P render_scene.py -- scene.json 01 out.png`. Tested on Blender 5.3.0 (about 5 s per 1080x1920 frame). Break-even against AI images = setup hours / (AI cost per piece minus 3D cost per piece); in the worked example about 18 pieces. Script, rig rules, asset licences: `references/blender-pipeline.md`.

## 5. Video by code, assembly and finish
- **Code**: ffmpeg for cuts, joins, resize, captions and loudness; Remotion (React videos, command-line render) for data-driven templates and launch videos; read its licence before commercial use. **Site or repo to launch video** (the brag-slim pattern): read the project, pick 3 true proof points, capture real screens, build 15-30 s from a JSON of beats, render 9:16 and 16:9.
- **Formats**: 9:16 1080x1920 (Reels, TikTok, Shorts), 1:1, 4:5, 16:9; subject and captions inside the safe area; render per ratio, no letterbox.
- **Edit**: cut on action, change shot size between cuts, readable on mute in 1-2 s, motion every 2-4 s on stills.
- **Captions**: burned in, 1-2 lines, correct names and numbers.
- **Loudness**: normalise to one target with a true-peak ceiling (ffmpeg loudnorm, two passes), duck music under voice, check on a phone speaker.
Commands: `references/code-video-and-assembly.md`.

## 6. Stock, music, voice, footage
- **Stock**: read the licence page and the file badge; commercial vs editorial; attribution depends on the licence (CC BY needs credit, CC BY-NC is never for ads); recognisable people, trademarks and property need releases. Keep URL, date, author and a copy of the licence.
- **Music**: ask who owns the recording and the composition, what use (organic, paid, TV), where, how long, and whether the plan covers it. Business accounts are often limited to the platform's commercial library.
- **TTS and cloning**: your own voice or a voice with written, specific consent; never clone a found clip; keep the consent file.
- **Live footage**: sound first, soft window light, headroom for captions, inserts, releases on set. All in `references/rights-and-labels.md`.

## 7. Cost and time per piece
Cash per piece plus hours x hourly value, from a log. Worked example: `playbooks.md` 6. Replace assumptions after three pieces.

## 8. QA before publishing
Spec (ratio, length, codec, safe area), picture (hands, faces, drift, text, brands), facts (claims real, numbers as text layers), audio (loudness, ducking, mute test), captions, rights (licences, releases, voice consent, no trademarks), labels, accessibility, one full watch on a phone. Checklist: `playbooks.md` 7.

## 9. Rights, likeness and AI labels
Not legal advice. **Check the rules of the country and platform where you publish**; Brazil, the EU, the UK and the US are examples only. A real person's face or voice needs written consent for the use; no AI likeness of real people for endorsements; no fake testimonials. Realistic AI or altered content needs a label: YouTube asks creators to disclose it in the upload flow; Meta and TikTok publish their own rules (not readable here, unverified); EU AI Act art. 50 applies from 2 Aug 2026 (marking by providers, deep fake disclosure by deployers, lighter duty for evidently creative work). Keep C2PA data. Label when in doubt. Details: `rights-and-labels.md` 6.

## 10. Diagnose
Bad output, slow render, wrong audio, rejected ad, copyright claim: `references/diagnosis-playbook.md` (Step 0, then trees A to F). Results problems (views, retention, CTR) go to viral-content, ad-creatives or paid-traffic.

## 11. Output
Match the request: route recommendation with cost and time, a filled brief, style block and character sheet prompt, shot list and continuity table, JSON scene spec and render command, ffmpeg or Remotion plan, QA report, rights table (asset, licence, use, proof). Always end with: the single next action, the cost and time estimate with assumptions, evidence level, what you could not verify.

## Which reference to open
- Choose route, brief, routines, QA, cost: `references/playbooks.md`.
- Generators, consistency, prompts, iteration cost: `references/generators-and-consistency.md`.
- Blender and the JSON spec: `references/blender-pipeline.md`.
- Remotion, ffmpeg, formats, captions, loudness: `references/code-video-and-assembly.md`.
- Stock, music, voice, likeness, labels: `references/rights-and-labels.md`.
- Something broke: `references/diagnosis-playbook.md`. Sources: `references/BIBLIOGRAPHY.md`.
Related: viral-content, ad-creatives, storytelling, copywriting, ui-design, brag-slim.
