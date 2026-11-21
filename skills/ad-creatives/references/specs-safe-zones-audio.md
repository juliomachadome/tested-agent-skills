# Specs, safe zones, sound and export

Read 13/11/2026 (Meta Ads Guide pages for Reels, Stories and feed; TikTok spec pages by search). Re-check before production.

| Placement | Ratio | Resolution | Notes |
|---|---|---|---|
| Reels (Instagram/Facebook) | 9:16 | Meta recommends 1440×2560; 1080×1920 accepted | H.264, fixed frame rate, AAC stereo ≥128 kbps, MP4/MOV, up to 4 GB |
| Stories | 9:16 | same | primary text up to 125 characters |
| Feed image | 4:5 (or 1:1) | 1440×1800 recommended (1080×1350 accepted) | primary text 125; headline 40 |
| TikTok | 9:16 | ≥540×960; produce 1080×1920, min 720p | MP4/MOV; no duration limit in auction |
| YouTube Shorts | 9:16 | 1080×1920 | Shorts ABCD guidance |
| YouTube / page | 16:9 | 1920×1080 or 1280×720 | |

- **[C] Meta 9:16 safe zone (Reels and Stories):** Meta's help page (read 15/11/2026) gives no percentages. It says to keep the top, bottom and side edges free of text and logos in 9:16 placements, and, if the Reels ad carries labels, to keep the **bottom 40%** free of text, logos and key elements; the platform may zoom or letterbox on taller screens. **[M] Practitioner estimate, not Meta's figures:** about top 14%, bottom 35%, 6% each side (1080×1920: free area y 269-1248, x 65-1015). Use the stricter of the two and confirm in the ads-manager preview. The bottom third holds account name, caption and button.
- **[C] TikTok publishes no fixed pixels:** the safe area depends on orientation and caption length; use the official downloadable template and check in preview. Longer caption, smaller area. [search]
- **One file for all 9:16 placements:** compose for the most restrictive zone (Meta's). Burned captions above y 1248 at 1080×1920. Background may bleed to the edge; text may not.
- **Always check in the ads-manager preview** with the interface on top; a frame extracted from the MP4 does not show the button or caption.
- **Cover:** a frame from the video with a legible hook that works as a still.
- **Export:** 30 fps, H.264 (`yuv420p`), AAC 128 kbps 48 kHz, `faststart`. 1080×1920 is the working standard; 1440×2560 only if the machine copes and the gain is visible.
- Meta primary text over 125 characters is truncated: the first line carries the meaning.

## Sound, captions, on-screen text
- **[C] Design for sound on and off at once.** Meta marks captions "optional, recommended" and sound "optional, highly recommended" for Reels; TikTok says use sound or music; Google says announce with audio and reinforce with text.
- **[X] "85% watch without sound"** is 2016 data from publisher videos in an auto-muted feed. Reels and TikTok are sound-on environments; the 70-85% sound-on figures circulating for Reels have no open official source.
- **[M] Burned-in captions:** older internal platform tests (2016) found ~12% more view time with captions. Burn them in because optional tracks do not always show. Max 2 lines, high contrast, spoken word highlighted, inside the safe zone.
- Voice, screen and image say the same thing ("avoid competing elements"). While the hook is written large, do not repeat it in the caption.
- **[F] Clean audio:** voice in front, music ~18-24 dB below with ducking, one entry and one CTA effect, final loudness around −16 LUFS with peaks to −1.5 dBTP. Mixing practice, not a platform rule.
- **[C] Music only original, synthesised or commercially licensed.** Hit songs in ads are not covered by ordinary libraries: TikTok ads use the Commercial Music Library; Meta's Sound Collection covers commercial use inside Meta products. [search; check current terms]

## Text-to-speech narration
One call per sentence; numbers spelled out in spoken text and digits in captions; short pause between sentences; foreign words with phonemes or a voice of that language; check by ear or automatic transcription before mixing. API keys come from environment variables, never from the script or repo.
