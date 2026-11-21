# Interface sound and vibration

Only when the request includes sound. Read 20/11/2026 from official sources (URLs below, listed in `BIBLIOGRAPHY.md`); restated, not copied.

## Rules of use
- Sound only after a user action, never on load. Off by default unless the brief says otherwise; a visible mute switch (`role="switch"`, `aria-checked`) whose choice is stored.
- Short (UI sounds under about 300 ms), quiet (gain around 0.2 to 0.4 of full), no loops. One sound per meaning (tap, success, error), not per element.
- Never the only signal: every sound duplicates a visible text or icon state.
- Respect device silent mode: never try to work around it (for example with tricks that force the media audio route); if the device stays silent, the visible state still carries the meaning.

## Web Audio vs `<audio>`
Source: MDN Web Audio API https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API (modified 12/11/2026) and Best practices https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices (modified 27/08/2026).
- Short UI sounds: fetch once, `decodeAudioData`, play with a new `AudioBufferSourceNode` each time through one shared `GainNode`. Low latency, overlapping plays are fine.
- Long tracks (music, narration): `<audio>`, which streams.
- One `AudioContext` per page. Created inside a user gesture it starts `running`; created earlier it starts `suspended` and needs `ctx.resume()` from a gesture. Create or resume it on the first click, not at load.
- Use `AudioParam` scheduling (`setTargetAtTime`, `linearRampToValueAtTime`) for fades to avoid clicks.
- Synthesized tones (OscillatorNode plus a gain envelope of a few ms attack and 50 to 150 ms decay) avoid any file download for simple clicks and beeps.

## Formats
Source: MDN Web audio codec guide https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Audio_codecs (modified 13/10/2026; the page warns its own table may lag).
- Safe everywhere: **AAC in MP4 (.m4a)** or **MP3**. MP3 is supported in all current browsers.
- Opus is smaller at the same quality (Chrome, Edge, Firefox); Safari support is limited in that table, so ship AAC or MP3 as the fallback or test Opus-in-WebM on Safari first.
- Vorbis (Ogg): not in Safari.
- Encode UI sounds mono, 44.1 or 48 kHz, small bitrate; each file a few KB.

## Preloading
- `fetch` plus `decodeAudioData` works in all current browsers (compat data: Safari 6+, Chrome 14+, Firefox 25+). Fetch after first paint or when the user turns sound on, never in the critical path.
- Decoded buffers can be large in memory; keep the set small.

## Autoplay policy
Sources: MDN Autoplay guide https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay (modified 10/09/2026); Chrome https://developer.chrome.com/blog/autoplay (no page date); WebKit https://webkit.org/blog/6784/new-video-policies-for-ios/ (25/07/2016, video only).
- Audible playback without a user gesture is blocked by default. Allowed when muted, after the user interacted with the page, by site settings, or when the Permissions-Policy `autoplay` allows it (default `self`, so cross-origin iframes need `allow="autoplay"`).
- Chrome: audio/video policy since Chrome 66 (2018), Web Audio since Chrome 71. Engagement-based allowance (desktop) and installed PWAs may autoplay; do not rely on it.
- WebKit (iOS): muted or silent video may autoplay; it pauses off screen; `playsinline` needed on iPhone. No current official WebKit page on Web Audio autoplay was found in this pass.
- `navigator.getAutoplayPolicy()` exists only in Firefox (112+). Feature-detect; otherwise handle the rejected `play()` promise and check `AudioContext.state`.

## Vibration
Source: MDN Navigator.vibrate https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate (modified 30/11/2025).
- Limited availability: Chrome 32, Edge 79, Firefox 16 (Android). **Not supported in Safari or iOS**; there is no web haptics on iPhone through this API.
- Needs sticky user activation. Feature-detect (`'vibrate' in navigator`) and fail silently.
- Use only for confirmation (one pulse of about 10 to 30 ms) or error (two short pulses); never for decoration or every tap.

## Minimal shape
```js
let ctx, gain, buffers = {}, soundOn = localStorage.getItem('sound') === 'on';
async function enableSound() {           // call from the mute switch click
  ctx ??= new AudioContext(); await ctx.resume();
  if (!gain) { gain = ctx.createGain(); gain.gain.value = 0.3; gain.connect(ctx.destination); }
  for (const n of ['tap', 'ok', 'err']) buffers[n] ??= await fetch(`/s/${n}.m4a`)
    .then(r => r.arrayBuffer()).then(b => ctx.decodeAudioData(b));
}
function play(name) {
  if (!soundOn || !ctx || ctx.state !== 'running' || !buffers[name]) return;
  const s = ctx.createBufferSource(); s.buffer = buffers[name]; s.connect(gain); s.start();
}
```
