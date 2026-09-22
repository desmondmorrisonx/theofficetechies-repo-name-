# Voice Samples — The Office 360 Unfiltered

Reference voice samples for the two hosts. Use these to identify the correct
voice in any new session. **Both are real audio. Neither is synthetic.**

| File | Host | Source | Length |
|------|------|--------|--------|
| `ALEX_voice_sample.mp3` / `.wav` | **Alex** | Alex's real uploaded recording (`alex_real_voice.mp3`) | ~15.2s |
| `MORGAN_voice_sample.mp3` / `.wav` | **Morgan** | Morgan's real generated episode clip (`audio/episode_14_clip_02.wav`) | ~15.0s |

All files: 24 kHz, mono, peak ~0.90.

## Voice rules (do not break)

- **Alex = real recorded audio ONLY.** Never synthesize, clone, vocode,
  pitch-shift, or voice-convert Alex. Never generate Alex takes from the
  reference sample. If an Alex take is missing, STOP and request it by exact
  filename — never substitute a synthetic voice.
- **Morgan is the only speaker that may be generated** (text-to-speech).
- No SSML, no stage directions, no `(laughs)` inside TTS text.

## For a fresh chat / another session

1. Read `../VOICE_LOCK.md` for the current voice state.
2. `ALEX_voice_sample.*` is the sound of Alex — match new Alex recordings to it.
3. `MORGAN_voice_sample.*` is the sound of Morgan — regenerate Morgan to match it.
4. Never fill an Alex slot with anything other than his real recorded audio.
