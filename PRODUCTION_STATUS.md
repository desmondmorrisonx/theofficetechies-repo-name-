# Production Status — The Office 360 Unfiltered

_Last audited: 2026-09-22_

## Summary

| Episode | Script | Artwork | Morgan clips | Alex takes | Mix | Transcripts | Show notes | RSS | State |
|---|---|---|---|---|---|---|---|---|---|
| 13 | done | done | done | done (3/3) | done 4:03 | done | done | done | **SHIPPED** |
| 14 | done | done | done (5/5) | **0 of 5** | blocked | blocked | draft | draft | **BLOCKED — needs Alex** |
| 15 | done | done | done (6/6) | **0 of 6** | blocked | blocked | draft | draft | **BLOCKED — needs Alex** |

Everything that can be built without Alex's voice has been built. Both
episodes are one command away from final once the recordings land.

---

## The blocker

`VOICE_LOCK.md` sets `ALEX_VOICE_MODE=real_recorded_audio`,
`ALEX_VOICE_ID=NONE_BY_DESIGN`, `ALEX_SYNTHESIS=disabled`.

Alex is a real human on real recordings. He is not a TTS voice and there is
no saved Alex voice model in this repository — by design, not by accident.
The only Alex audio in the repo is his three Episode 13 takes
(`alex_13_01/03/05.wav`), which are the Episode 13 words and cannot be
repurposed for Episodes 14 or 15. The reference file named in VOICE_LOCK.md,
`alex_real_voice.mp3`, was never committed and is not in git history.

Cloning or synthesizing Alex to unblock these episodes is explicitly
forbidden by the show's standing rules and has not been done.

---

## Missing recordings — 11 takes

Record each line as its own take. Exact words are already written in
`ALEX_RECORDING_SCRIPT_EPISODE_14.md` and `ALEX_RECORDING_SCRIPT_EPISODE_15.md`.

### Episode 14 — 5 takes (tone: very funny, high comedic energy, big grin)

```
audio/alex_14_01.wav
audio/alex_14_03.wav
audio/alex_14_05.wav
audio/alex_14_07.wav
audio/alex_14_09.wav
```

### Episode 15 — 6 takes (tone: warm, informative, proud of the case study)

```
audio/alex_15_01.wav
audio/alex_15_03.wav
audio/alex_15_05.wav
audio/alex_15_07.wav
audio/alex_15_09.wav
audio/alex_15_11.wav
```

### Recording notes

- WAV preferred; MP3 is fine and will be converted to 24 kHz mono.
- Any sample rate works — the mixer resamples.
- Aim ~25-30 seconds per take (Episode 13 averaged 26.6s).
- Keep breaths, natural laughter, and human timing. Do not over-clean.
- Open every clip with energy per the house style.
- Drop the files into `audio/` using exactly these filenames.

---

## Finishing command

Once the takes are in `audio/`, per episode:

```bash
python3 tools/mix_episode_generic.py 14
python3 tools/build_transcripts_generic.py 14
```

That produces the 24 kHz stereo master, the final WAV and MP3, the timing
map, and all three transcript formats. Then fill the `PENDING` duration and
pubDate fields in the show notes and RSS.

Projected runtimes, using Episode 13's average Alex pace against the real
Morgan clip durations already on disk:

- **Episode 14** — 10 clips, approx **4:40**
- **Episode 15** — 12 clips, approx **5:59**

Both clear the 4:00 minimum without padding. Verified by a full dry run of
the pipeline (run in a temp directory with silent placeholders, then
deleted — no placeholder audio was ever written into this repository).

---

## Tooling added this pass

- `tools/mix_episode_generic.py` — episode-agnostic mixer holding the exact
  Episode 13 house spec: 24 kHz stereo, ~380 ms gaps, 1.85 s intro, 4.4 s
  outro, bed ducked 24 dB under speech, peak 0.94. Adds light edge-silence
  trim and conservative level matching (gain clamped 0.5x-2.0x so human
  dynamics survive). **Refuses to build and names every missing take rather
  than substituting synthesized audio.**
- `tools/build_transcripts_generic.py` — parses the episode script for text
  and the mixer's timing map for timestamps, so transcripts cannot drift
  from either the script or the audio. Emits SRT, VTT, and Markdown.

The Episode 13 originals (`mix_episode.py`, `build_transcripts.py`) are
untouched for reference.

## Other fixes this pass

- `episode_14_artwork.png` — the hallway tally sticky note showed 7 marks;
  the script and Morgan's line both say **four**. Redrawn with four marks.
  Everything else in the artwork is unchanged.
