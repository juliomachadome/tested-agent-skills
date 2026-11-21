# Speech-to-Text (ASR) Pipelines

Contents: 1 Choosing and running a model · 1b Real audio and long-audio decoding · 2 Proper names · 3 Diarization · 4 Measuring with a gold set · 5 Cost and GPU · Sources

Use when an LLM feature starts from audio (meeting minutes, call summaries, voice notes). Rule of thumb: transcribe with a dedicated ASR model, then give **text** to the LLM; every ASR error becomes an LLM input, so measure the ASR stage on its own.

## 1. Choosing and running a model

- Open-weight Whisper (MIT license for code and weights) comes in sizes from tiny (39M parameters, about 1 GB VRAM) to large (1,550M, about 10 GB) and turbo (809M, about 6 GB); large and turbo are multilingual only, and quality varies widely by language (read 2026-11-15, github.com/openai/whisper). Pick the smallest size that meets your word error rate on **your** audio and language.
- Hosted ASR APIs have per-file size limits (25 MB at the time of reading), so compress or chunk long recordings. Split at natural pauses rather than mid-sentence, because cuts lose context and lower accuracy (read 2026-11-15, OpenAI speech-to-text guide).
- Model lines change fast (the guide marks older hosted models as deprecated with shutdown dates): wrap the ASR provider behind a port and re-run your gold set on every model change.

## 1b. Real audio and long-audio decoding

- Published word error rates for Whisper-class models come mostly from **read speech** benchmarks; spontaneous, multi-microphone, overlapping speech (meetings, hearings) is several times worse, so never promise a paper number. Measure on your own audio (section 4).
- Model cards warn of uneven quality by language and of text that was not spoken (hallucination) and repetition loops; beam search and temperature fallback reduce but do not eliminate them. A fabricated sentence in an official record is harm, not noise: flag long-silence regions, repeated phrases and non-speech segments for review. Hallucinations on non-speech sounds repeat across files, so a list of known hallucinated phrases is a cheap post-filter.
- Long audio is decoded in 30-second windows; a timing or text error in one window propagates to the next. Heuristics from the Whisper paper: beam 5, temperature fallback from 0 up to 1.0 when average log-probability is low or the compression ratio is high (above 2.4), previous text as context when temperature is low. Batched modes in some runtimes drop the fallback and previous-text context, trading a few quality features for roughly 3-4x less GPU time: verify on your gold set.
- Cutting at voice-activity pauses (with merge) before transcription improves quality and enables batching; forced alignment adds word timestamps. Words outside the aligner's vocabulary (rare names, numerals spelled out) may get no timestamps, which breaks "play this word" review tools.
- Quantization (int8, float16) can change decoding decisions slightly; set the compute type explicitly and keep it identical between experiments. Keep sampling and VAD settings fixed when comparing models.

## 2. Proper names, jargon and acronyms

- Prefer giving the recognizer the correct spellings: a `prompt` or keyword list where the API supports it. The older hosted Whisper accepts at most 224 prompt tokens and follows instructions loosely; keywords are hints, so include only terms likely to occur and check that they do not appear in the output when they were not spoken (read 2026-11-15).
- For long vocabularies use a **post-correction pass** with a text model that receives the transcript plus a list of known names and correct spellings; verify its edits against the audio or the original, because a corrector may "fix" what was really said. Treat the roster of known names as the source of truth for spelling, and require a human click for any rename.
- Pseudonymize speaker names before sending text to a third-party LLM; map back afterwards.

## 3. Diarization (who spoke)

- Hosted diarization models return segments with speaker label, start and end; some accept short reference clips (a few seconds each) to map labels to known speakers, but may not accept prompts, and are not always available in streaming modes (read 2026-11-15).
- Open pipelines (for example pyannote-style) separate diarization from transcription and merge by timestamps; overlap and short interjections are the main error source.
- Keep speaker labels as data (`SPEAKER_1`) until a person confirms the mapping; never let the LLM guess who a speaker is from content.

## 4. Measuring with a gold set

- **WER** = (substitutions + deletions + insertions) / words in the reference. Normalize text identically on both sides (case, punctuation, numerals, accents) or the number is meaningless. Report WER per condition (clean vs noisy, accent, domain terms) and a separate **proper-name error rate** because average WER hides name errors.
- **DER** (diarization error rate) = (missed speech + false alarm + speaker confusion) / total reference speech time; report it with the collar and overlap handling stated.
- Build a gold set of 1-2 hours of real, representative audio with human-verified transcripts and speaker turns; keep a sealed part (see evals-observability.md) and report intervals; WER over a few minutes of audio is noise.
- Compare vocabulary prompt on/off, model sizes and post-correction on the same audio (paired), and check that fixes do not raise errors elsewhere.
- **Normalize before WER and freeze the rule before seeing the number** (case, punctuation, numerals, abbreviations). Changing it later turns formatting differences into fake errors.
- **Bootstrap by blocks, not by utterance:** utterances from the same speaker or session are correlated, and the ordinary bootstrap gives intervals that are too narrow; resample blocks (sessions or speakers) and compare systems with paired differences (Bisani and Ney style, see sources).
- **Reference transcripts are not literal:** edited or summarized references give a WER floor; audit a sample (classify each disagreement as ASR error, reference edit or ambiguous) before quoting absolute values. For A-vs-B on the same references the floor cancels.
- **One metric per error class:** names (against a list), numbers and identifiers (against the agenda or source documents), hallucinated words (counted separately), speaker swaps, punctuation (punctuation error rate measured by sign). Average WER weights every word equally and hides the ones that matter.
- **Who said what:** cpWER counts a word correct only with the right speaker; DER with collar 0 vs 0.25 s differs, so state the collar and overlap handling; JER, purity and coverage show what DER hides (a dominant speaker masks errors on minor speakers).
- Procedure: change one lever at a time, run A and B on the same gold audio, report paired diff with block intervals, read 40 or more changed cases by hand, decide per class (no win on average that worsens names, voices or hallucinations), and write down what was not measured.
- Also measure what downstream cares about: names and numbers in the minutes, decisions attributed to the right speaker.

## 5. Cost and GPU operations

- Cost = audio hours x price per hour (hosted) or GPU seconds x rate (self-hosted). Real-time factor and batch size set GPU cost; keep GPUs at **zero minimum** (scale to zero) and verify after each test that no instance is left running and spend is flat.
- Serverless GPU billing is typically per second from worker start to stop, including cold start (model load) and idle timeout; image pulls and scaled-to-zero time are free. Cost per audio hour = GPU price per hour / real-time factor (for example a 12x faster-than-real-time model on a 0.75 USD/hour GPU is about 0.06 USD per audio hour, excluding cold start; own arithmetic, prices change). Re-check the price table before quoting costs.
- Batch (offline) transcription is much cheaper than live streaming; only stream when the user needs words as they are spoken.
- Make jobs idempotent and resumable (chunk-level checkpoints), with timeouts, bounded retries and a cap on audio length per request.
- Treat audio and transcripts as personal data: retention limits, access control, and an explicit policy on whether third-party processors may receive them.

## Sources (read 2026-11-15)

- Radford et al., Robust Speech Recognition via Large-Scale Weak Supervision (Whisper, 2022): https://arxiv.org/abs/2212.04356 (study notes 2026-11-13; not re-verified)
- Koenecke et al., Careless Whisper (hallucination in ASR, 2024) and ICASSP 2025 non-speech hallucination study: https://arxiv.org/abs/2501.11378 (study notes; not re-verified)
- Bain et al., WhisperX: https://arxiv.org/abs/2303.00747 (abstract, study notes; not re-verified)
- Bredin, pyannote.audio 2.1 speaker diarization (Interspeech 2023), pyannote.metrics documentation (DER, JER, purity, coverage): https://github.com/pyannote/pyannote-metrics (study notes; not re-verified)
- von Neumann et al., MeetEval (cpWER): https://arxiv.org/abs/2307.11394 (abstract, study notes; not re-verified)
- Block bootstrap for ASR significance: https://arxiv.org/abs/1912.09508 (abstract, study notes; not re-verified); Bisani and Ney 2004 (not opened)
- faster-whisper README (VAD defaults, batched mode benchmarks): https://github.com/SYSTRAN/faster-whisper (study notes; not re-verified)

- OpenAI Whisper repository (sizes, VRAM, license, language variance): https://github.com/openai/whisper
- OpenAI speech-to-text guide (prompt and keywords, 224-token limit, 25 MB limit, chunking, diarization options, deprecations): https://developers.openai.com/api/docs/guides/speech-to-text
- WER and DER definitions: standard evaluation definitions (own summary, not fetched; not re-verified)
