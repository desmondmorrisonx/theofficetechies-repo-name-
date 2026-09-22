"""
Generic mixer for The Office 360 Unfiltered — works for any episode.
Same house spec as Episode 13:
  - 24 kHz stereo WAV master + MP3 delivery
  - lo-fi Rhodes bed ~78 BPM ducked ~24 dB under speech
  - ~380 ms gaps between speaker clips
  - ~1.85 s intro, ~4.4 s outro
  - peak normalized to ~0.94

REAL-ALEX RULE: this script only ever READS Alex WAV files supplied by the
user. It never synthesizes. If an Alex take is missing it refuses to build.

Usage:
    python3 tools/mix_episode_generic.py 14
    python3 tools/mix_episode_generic.py 15
"""
import os
import sys

import numpy as np
import soundfile as sf

SR = 24000
GAP = 0.38
INTRO = 1.85
OUTRO = 4.4
DUCK_DB = -24.0
TARGET_PEAK = 0.94

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(REPO, "audio")

# Clip running order per episode. Odd slots = Alex (real recordings),
# even slots = Morgan (session voice). Filenames are the contract with
# the ALEX_RECORDING_SCRIPT_EPISODE_N.md documents.
EPISODES = {
    "14": [
        ("Alex",   "alex_14_01.wav"),
        ("Morgan", "episode_14_clip_02.wav"),
        ("Alex",   "alex_14_03.wav"),
        ("Morgan", "episode_14_clip_04.wav"),
        ("Alex",   "alex_14_05.wav"),
        ("Morgan", "episode_14_clip_06.wav"),
        ("Alex",   "alex_14_07.wav"),
        ("Morgan", "episode_14_clip_08.wav"),
        ("Alex",   "alex_14_09.wav"),
        ("Morgan", "episode_14_clip_10.wav"),
    ],
    "15": [
        ("Alex",   "alex_15_01.wav"),
        ("Morgan", "episode_15_clip_02.wav"),
        ("Alex",   "alex_15_03.wav"),
        ("Morgan", "episode_15_clip_04.wav"),
        ("Alex",   "alex_15_05.wav"),
        ("Morgan", "episode_15_clip_06.wav"),
        ("Alex",   "alex_15_07.wav"),
        ("Morgan", "episode_15_clip_08.wav"),
        ("Alex",   "alex_15_09.wav"),
        ("Morgan", "episode_15_clip_10.wav"),
        ("Alex",   "alex_15_11.wav"),
        ("Morgan", "episode_15_clip_12.wav"),
    ],
}


def load_mono_24k(path):
    data, sr = sf.read(path, always_2d=True)
    data = data.mean(axis=1)
    if sr != SR:
        duration = len(data) / sr
        n_new = int(round(duration * SR))
        x_old = np.linspace(0, duration, num=len(data), endpoint=False)
        x_new = np.linspace(0, duration, num=n_new, endpoint=False)
        data = np.interp(x_new, x_old, data)
    return data.astype(np.float64)


def trim_edge_silence(sig, sr=SR, thresh=0.006, pad=0.12):
    """Light edge-silence trim only. Preserves interior breaths and timing."""
    idx = np.where(np.abs(sig) > thresh)[0]
    if len(idx) == 0:
        return sig
    p = int(pad * sr)
    return sig[max(0, idx[0] - p): min(len(sig), idx[-1] + p)]


def fade(sig, sr=SR, fade_in_s=0.015, fade_out_s=0.02):
    n_in = int(fade_in_s * sr)
    n_out = int(fade_out_s * sr)
    out = sig.copy()
    if 0 < n_in < len(out):
        out[:n_in] *= np.linspace(0, 1, n_in)
    if 0 < n_out < len(out):
        out[-n_out:] *= np.linspace(1, 0, n_out)
    return out


def level_match(sig, target_rms=0.11):
    """Gently match a clip toward the house speech RMS. Never hard-compresses."""
    rms = np.sqrt((sig ** 2).mean()) + 1e-9
    gain = target_rms / rms
    gain = float(np.clip(gain, 0.5, 2.0))  # conservative; keeps human dynamics
    return sig * gain


def duck_envelope(total_len, positions, sr=SR):
    duck_lin = 10 ** (DUCK_DB / 20.0)
    env = np.ones(total_len)
    ramp = int(0.25 * sr)
    for start, end in positions:
        r_start = max(0, start - ramp)
        r_end = min(total_len, end + ramp)
        if start > r_start:
            env[r_start:start] = np.linspace(1.0, duck_lin, start - r_start)
        env[start:end] = duck_lin
        if r_end > end:
            env[end:r_end] = np.linspace(duck_lin, 1.0, r_end - end)
    return env


def check_takes(ep):
    """Hard gate: every Alex take must be a real file on disk."""
    missing = []
    for speaker, fname in EPISODES[ep]:
        if not os.path.exists(os.path.join(AUDIO, fname)):
            missing.append((speaker, fname))
    return missing


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in EPISODES:
        print("Usage: python3 tools/mix_episode_generic.py [14|15]")
        sys.exit(2)
    ep = sys.argv[1]

    missing = check_takes(ep)
    if missing:
        print(f"REFUSING TO MIX EPISODE {ep} — missing source audio:\n")
        for speaker, fname in missing:
            tag = "REAL RECORDING REQUIRED" if speaker == "Alex" else "generated clip"
            print(f"  [{speaker:6s}] audio/{fname}   <- {tag}")
        print("\nAlex is real recorded audio by design (see VOICE_LOCK.md).")
        print("No synthesis substitute will be made. Supply the takes and re-run.")
        sys.exit(1)

    clips = []
    for speaker, fname in EPISODES[ep]:
        sig = load_mono_24k(os.path.join(AUDIO, fname))
        sig = trim_edge_silence(sig)
        sig = level_match(sig)
        clips.append(fade(sig))

    gap_samps = int(GAP * SR)
    intro_samps = int(INTRO * SR)
    outro_samps = int(OUTRO * SR)

    total_len = intro_samps
    positions = []
    for i, c in enumerate(clips):
        positions.append((total_len, total_len + len(c)))
        total_len += len(c)
        if i < len(clips) - 1:
            total_len += gap_samps
    total_len += outro_samps

    speech = np.zeros(total_len)
    for c, (start, end) in zip(clips, positions):
        speech[start:end] += c

    bed_stereo, bed_sr = sf.read(os.path.join(AUDIO, "music_bed.wav"), always_2d=True)
    bed = bed_stereo.mean(axis=1)
    if bed_sr != SR:
        duration = len(bed) / bed_sr
        n_new = int(round(duration * SR))
        x_old = np.linspace(0, duration, num=len(bed), endpoint=False)
        x_new = np.linspace(0, duration, num=n_new, endpoint=False)
        bed = np.interp(x_new, x_old, bed)
    if len(bed) < total_len:
        bed = np.tile(bed, int(np.ceil(total_len / len(bed))))
    bed = bed[:total_len]

    env = duck_envelope(total_len, positions)
    mix = speech + bed * env * 0.9

    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * TARGET_PEAK
    stereo = np.stack([mix, mix], axis=1).astype(np.float32)

    master = os.path.join(AUDIO, f"episode_{ep}_master.wav")
    sf.write(master, stereo, SR, subtype="PCM_16")

    final_wav = os.path.join(REPO, f"The_Office_360_Unfiltered_Episode_{ep}.wav")
    final_mp3 = os.path.join(REPO, f"The_Office_360_Unfiltered_Episode_{ep}.mp3")
    sf.write(final_wav, stereo, SR, subtype="PCM_16")
    sf.write(final_mp3, stereo, SR)

    secs = total_len / SR
    with open(os.path.join(AUDIO, f"episode_{ep}_timing.txt"), "w") as f:
        f.write(f"intro_start=0.0\nintro_end={INTRO}\n")
        for (start, end), (speaker, fname) in zip(positions, EPISODES[ep]):
            f.write(f"{fname}\t{start/SR:.3f}\t{end/SR:.3f}\t{speaker}\n")
        f.write(f"outro_start={(total_len-outro_samps)/SR:.3f}\nouttro_end={secs:.3f}\n")

    print(f"Episode {ep} mixed.")
    print(f"  runtime : {int(secs)//60}:{int(secs)%60:02d}  ({secs:.1f}s)")
    print(f"  peak    : {np.max(np.abs(mix)):.3f}")
    print(f"  rate    : {SR} Hz stereo")
    print(f"  master  : {master}")
    print(f"  wav     : {final_wav}")
    print(f"  mp3     : {final_mp3}")
    if secs < 240:
        print("  WARNING: under the 4:00 minimum — add real content, do not pad with music.")


if __name__ == "__main__":
    main()
