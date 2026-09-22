"""
Build a listenable SEGMENT REEL for an episode from the clips that exist.

This is NOT the finished episode. It lays the recorded segments end to end
over the house lo-fi bed so they can be reviewed as audio. Alex's slots are
simply absent — never synthesized, never padded with filler music.

House spec is preserved: 24 kHz stereo, ~380 ms gaps, bed ducked ~24 dB
under speech, peak ~0.94.

Usage:
    python3 tools/build_segments.py 14
"""
import os
import sys

import numpy as np
import soundfile as sf

SR = 24000
GAP = 0.38
LEAD = 1.85
TAIL = 4.4
DUCK_DB = -24.0
TARGET_PEAK = 0.94

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(REPO, "audio")

SEGMENTS = {
    "14": [f"episode_14_clip_{c}.wav" for c in ["02", "04", "06", "08", "10"]],
    "15": [f"episode_15_clip_{c}.wav" for c in ["02", "04", "06", "08", "10", "12"]],
}


def load_mono_24k(path):
    data, sr = sf.read(path, always_2d=True)
    data = data.mean(axis=1)
    if sr != SR:
        dur = len(data) / sr
        n = int(round(dur * SR))
        data = np.interp(
            np.linspace(0, dur, n, endpoint=False),
            np.linspace(0, dur, len(data), endpoint=False),
            data)
    return data.astype(np.float64)


def trim_edges(sig, thresh=0.006, pad=0.12):
    idx = np.where(np.abs(sig) > thresh)[0]
    if len(idx) == 0:
        return sig
    p = int(pad * SR)
    return sig[max(0, idx[0] - p): min(len(sig), idx[-1] + p)]


def fade(sig, fin=0.015, fout=0.02):
    out = sig.copy()
    a, b = int(fin * SR), int(fout * SR)
    if 0 < a < len(out):
        out[:a] *= np.linspace(0, 1, a)
    if 0 < b < len(out):
        out[-b:] *= np.linspace(1, 0, b)
    return out


def level_match(sig, target_rms=0.11):
    rms = np.sqrt((sig ** 2).mean()) + 1e-9
    return sig * float(np.clip(target_rms / rms, 0.5, 2.0))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SEGMENTS:
        print("Usage: python3 tools/build_segments.py [14|15]")
        sys.exit(2)
    ep = sys.argv[1]

    files = SEGMENTS[ep]
    missing = [f for f in files if not os.path.exists(os.path.join(AUDIO, f))]
    if missing:
        print("Missing segment clips: " + ", ".join(missing))
        sys.exit(1)

    clips = [fade(level_match(trim_edges(load_mono_24k(os.path.join(AUDIO, f))))) for f in files]

    gap = int(GAP * SR)
    total = int(LEAD * SR)
    pos = []
    for i, c in enumerate(clips):
        pos.append((total, total + len(c)))
        total += len(c)
        if i < len(clips) - 1:
            total += gap
    total += int(TAIL * SR)

    speech = np.zeros(total)
    for c, (s, e) in zip(clips, pos):
        speech[s:e] += c

    bed, bsr = sf.read(os.path.join(AUDIO, "music_bed.wav"), always_2d=True)
    bed = bed.mean(axis=1)
    if bsr != SR:
        dur = len(bed) / bsr
        n = int(round(dur * SR))
        bed = np.interp(np.linspace(0, dur, n, endpoint=False),
                        np.linspace(0, dur, len(bed), endpoint=False), bed)
    if len(bed) < total:
        bed = np.tile(bed, int(np.ceil(total / len(bed))))
    bed = bed[:total]

    duck = 10 ** (DUCK_DB / 20.0)
    env = np.ones(total)
    ramp = int(0.25 * SR)
    for s, e in pos:
        rs, re_ = max(0, s - ramp), min(total, e + ramp)
        if s > rs:
            env[rs:s] = np.linspace(1.0, duck, s - rs)
        env[s:e] = duck
        if re_ > e:
            env[e:re_] = np.linspace(duck, 1.0, re_ - e)

    mix = speech + bed * env * 0.9
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * TARGET_PEAK
    stereo = np.stack([mix, mix], axis=1).astype(np.float32)

    wav = os.path.join(AUDIO, f"episode_{ep}_segments.wav")
    mp3 = os.path.join(REPO, f"Episode_{ep}_Segments_Morgan.mp3")
    sf.write(wav, stereo, SR, subtype="PCM_16")
    sf.write(mp3, stereo, SR)

    secs = total / SR
    print(f"Episode {ep} segment reel — {len(clips)} recorded segments")
    print(f"  runtime : {int(secs)//60}:{int(secs)%60:02d}  ({secs:.1f}s)")
    print(f"  peak    : {np.max(np.abs(mix)):.3f}   rate: {SR} Hz stereo")
    print(f"  mp3     : {mp3}")
    for f, (s, e) in zip(files, pos):
        print(f"    {s/SR:6.1f}s - {e/SR:6.1f}s  {f}")


if __name__ == "__main__":
    main()
