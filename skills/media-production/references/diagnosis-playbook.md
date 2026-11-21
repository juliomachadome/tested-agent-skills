# Diagnosis playbook: symptom, likely cause, check, fix

Use top-down. Step 0 first. Tags as in `SKILL.md`; thresholds are **[F]** starting points to replace with your own log.

## Step 0: is the evidence trustworthy?
| Check | How | If it fails |
|---|---|---|
| Is the problem in the output or in the brief? | Compare the output with the brief line by line | Fix the brief before regenerating |
| Which file, tool, plan and version made it | Read the project log | Add a log; reproduce with the same inputs |
| Is the sample enough | Judge a defect on 10+ outputs, not one | State "too few to conclude" |
| Is it the viewer's device | Open on the target phone, not only the desktop | Re-check after export |
| Rules read today | Tool terms, licence page and platform policy dated this month | Re-read; do not trust memory |

## Tree A: image and video quality
| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Character changes face or outfit between shots | No reference, or a reference not re-attached; prompt drifts | Compare to the sheet side by side | Attach the sheet every time; paste the fixed description; keep insert shots faceless; if still drifting, LoRA or 3D |
| Hands, fingers, objects wrong | Model weakness | Zoom 200% | Reframe to hide hands, crop, inpaint or regenerate; use insert shots; photograph the real hand |
| Text or logo is garbled | Generated text | Read it | Remove from the prompt; add as a real text layer |
| Look differs scene to scene | Style block missing or edited | Diff the prompts | Paste the unchanged block; version it |
| Video clip warps, faces melt | Complex motion, long clip | Frame-by-frame | Shorter clip, one camera move, first-frame image, or a still with push-in |
| Cost per kept image too high | Too many attempts | Attempts per kept image over the last 3 pieces | Tighten the prompt template, test frame per location, lower resolution until final |
| Output looks generic | Vague prompt, default style | Read the prompt | Name palette, light, lens; add 2-3 concrete objects |

## Tree B: 3D and render
| Symptom | Cause | Check | Fix |
|---|---|---|---|
| Script fails headless | Wrong argument split or a UI-only operator | Read the console; arguments after `--` | Print `sys.argv`; use data API instead of UI operators |
| Render too slow | Cycles samples, resolution, denoise off | Time 3 frames | Lower samples, EEVEE, crop, use a GPU if present; estimate = frames x seconds |
| Black or white image | Light energy, world colour, camera clip | Render at low res and open | Raise light energy; check camera clipping and the active camera |
| Output file missing | Wrong relative path | Print the absolute path | Use an absolute path or `//` for blend-relative |
| Wrong engine enum | Version change | Error text | List enum items; set the supported name |

## Tree C: audio and loudness
| Symptom | Cause | Fix |
|---|---|---|
| Too quiet or too loud on a platform | Loudness target mismatch | Two-pass loudnorm to the target; check true peak |
| Music hides voice | No ducking | Lower music 10-15 dB under speech |
| Robotic voice | TTS settings, long sentences | Shorter lines, punctuation for pacing, a human re-record for the hook |
| Mouth and audio mismatch | Frame-rate or sync drift | Check audio delay; re-export at a constant frame rate |

## Tree D: format and delivery
| Symptom | Cause | Fix |
|---|---|---|
| Captions covered by platform buttons | Outside safe area | Move up, shrink the block |
| Blurry text after upload | Low bitrate or wrong scaling | Export higher bitrate, scale once, avoid double re-encode |
| Black bars | Wrong ratio | Render per ratio or crop with intent |
| Large file refused | Bitrate or length | Re-encode to the limit; check the platform spec |

## Tree E: rights and claims
| Symptom | Cause | Check | Fix |
|---|---|---|---|
| Copyright claim on a video | Music or footage with unclear licence | Which asset, which licence, which use | Dispute with the licence proof; replace the asset |
| Platform flags AI content | Missing or wrong label | The platform's current rule | Set the label; add on-screen line |
| Person objects to being in a video | No release, or consent too narrow | The consent file | Remove or replace; get a release next time |
| Ad rejected | Claim, brand mark, before/after, likeness | The rejection text | Fix the cause; do not rephrase to evade |
| Worry the voice sounds like a real person | Cloned or lookalike voice | Source of the voice | Use own or consented voice; change voice |

## Tree F: results do not come
Views, hooks and retention belong to `viral-content`; ad metrics to `ad-creatives` and `paid-traffic`; copy to `copywriting`. Production causes to check first: first frame unreadable on mute, captions late, audio quiet, slow first 3 s, claims not shown. Change one production variable per piece and compare medians over 8-10 pieces.

## Output
Data used and quality; leak; most likely and second cause; one fix with owner; the check that will show it worked; what could not be verified.
