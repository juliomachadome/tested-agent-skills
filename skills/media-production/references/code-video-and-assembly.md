# Video made by code, assembly, captions, formats, loudness

Tags as in `SKILL.md`. Commands were run on ffmpeg 8.1.2 (18/11/2026).

## 1. Choose the assembler
| Need | Tool |
|---|---|
| Cut, join, resize, add music, burn captions, normalise loudness, one-off | ffmpeg (free, scriptable) |
| Data-driven or repeatable video: same template, many variants (names, prices, screenshots), animated text, a launch video from a site or repo | Remotion: videos as React components, rendered from the command line (bib. 12). Its licence hub lists free-eligibility and company pricing; the terms were not read here, so read the licence before commercial use |
| Human editing, colour, complex audio | A desktop editor (any); export a preset per platform |
| Site or repo to launch video | The `brag-slim` skill pattern: read the project or URL, pick 3-5 real features, capture real screens, animate with code, add music and share copy |

## 2. Site or repo to launch video (pattern)
1. Read the README, landing page and changelog; write the one-sentence promise and 3 proof points that are true. 2. Capture real screens (browser screenshots or screen recording at 2x), never mock UI that the product does not have. 3. Storyboard 15-30 s: hook (problem or result), 3 beats (one feature each, 3-5 s), proof (number or quote you can source), call to action with the URL. 4. Build scenes as code (a Remotion composition per beat, fed from a JSON file: text, image path, duration). 5. Render at 1080x1920 and 1920x1080 from the same data. 6. Music from a licensed library (`rights-and-labels.md`), captions burned in, QA checklist in `playbooks.md`.

## 3. Aspect ratios and safe areas **[F]**
| Ratio | Pixels | Use |
|---|---|---|
| 9:16 | 1080x1920 | Reels, TikTok, Shorts, Stories |
| 1:1 | 1080x1080 | feed posts, carousels of video |
| 4:5 | 1080x1350 | feed |
| 16:9 | 1920x1080 | YouTube, web, landing pages |
Keep subject, eyes and captions inside the central area; platform buttons and captions cover the lower part and the right edge of 9:16. Exact current safe zones: `../../ad-creatives/references/specs-safe-zones-audio.md`. Make one master at the widest framing you can and crop with intent, or render each ratio from the same data; do not letterbox.
Resize with padding avoided: `ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:a copy out.mp4` (crops the centre; check the subject survives).

## 4. Cuts and pacing (editing craft)
Cut on action, hold a shot only as long as it gives new information, vary shot size between cuts (wide, medium, close, insert), use sound to bridge cuts (bib. 14 on what a cut should carry: emotion, story, rhythm; ideas only). First frame must read on mute within 1-2 s. A still image needs motion every 2-4 s (push-in, parallax) or a cut. Shot-planning ideas: bib. 16, 17. Cut to the beat of the music only when the music leads.

## 5. Captions
Burn captions for short vertical video (most viewing starts muted **[F]**); 1-2 lines, 3-7 words on screen, contrast with a box or outline, kept out of the platform UI zone. Source: your script (exact), or a speech-to-text draft that a person corrects; check names and numbers. Also upload a separate subtitle file (SRT) where the platform accepts it. Burn with ffmpeg: `ffmpeg -i in.mp4 -vf "subtitles=cap.srt:force_style='FontSize=18,Outline=2'" out.mp4`.

## 6. Loudness
Speech-first short video: normalise to one target and a true-peak ceiling. ffmpeg's `loudnorm` implements EBU R128 normalisation; its defaults are I=-24 LUFS, LRA=7, TP=-2 dBTP and it offers a two-pass mode for files (bib. 2). EBU R128 itself sets -23 LUFS for broadcast (bib. 13, identity only). Platforms apply their own normalisation and publish targets that change, so check the current help page; a common delivery for social is about -14 LUFS integrated with true peak at or below -1 dBTP **[F]**. Two-pass: first pass `-af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -`, then feed the measured values (`measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`, `offset`) into the second pass. Music under voice: duck 10-15 dB (`sidechaincompress` or a volume curve). Listen on a phone speaker and on earbuds. Audio craft: bib. 19, 21.

## 7. Export
H.264 video, AAC audio, `-pix_fmt yuv420p`, `-movflags +faststart`, 30 fps (match the source), bitrate high enough that text stays sharp; keep a lossless or high-bitrate master. Check: `ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -of csv out.mp4`. Re-encoding costs quality; cut from the master each time.

## 8. Frame sequences
A folder of PNGs (from Blender or a generator) becomes video with `ffmpeg -framerate 30 -i frame_%03d.png -c:v libx264 -pix_fmt yuv420p out.mp4`; stills held for N seconds use `-loop 1 -t N` per input and the `concat` filter, or a Remotion composition with one sequence per image.
