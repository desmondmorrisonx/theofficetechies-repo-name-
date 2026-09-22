"""
Mix The Office 360 Unfiltered - Episode 13.
- 24kHz stereo WAV master
- lo-fi Rhodes bed ducked ~24dB under speech
- ~380ms gaps between speaker clips
- ~1.85s intro, ~4.4s outro
- peak normalized to ~0.94
"""
import numpy as np
import soundfile as sf
import sys

SR = 24000
GAP = 0.38
INTRO = 1.85
OUTRO = 4.4
DUCK_DB = -24.0
TARGET_PEAK = 0.94

CLIP_ORDER = [
    "/home/user/audio/alex_13_01.wav",
    "/home/user/audio/episode_13_clip_02.wav",
    "/home/user/audio/alex_13_03.wav",
    "/home/user/audio/episode_13_clip_04.wav",
    "/home/user/audio/episode_13_clip_05.wav",
    "/home/user/audio/alex_13_05.wav",
    "/home/user/audio/episode_13_clip_07.wav",
]


def load_mono_24k(path):
    data, sr = sf.read(path, always_2d=True)
    data = data.mean(axis=1)  # to mono
    if sr != SR:
        # simple resample via linear interpolation (good enough for speech here)
        duration = len(data) / sr
        n_new = int(round(duration * SR))
        x_old = np.linspace(0, duration, num=len(data), endpoint=False)
        x_new = np.linspace(0, duration, num=n_new, endpoint=False)
        data = np.interp(x_new, x_old, data)
    return data.astype(np.float64)


def fade(sig, sr, fade_in_s=0.015, fade_out_s=0.02):
    n_in = int(fade_in_s * sr)
    n_out = int(fade_out_s * sr)
    out = sig.copy()
    if n_in > 0 and n_in < len(out):
        out[:n_in] *= np.linspace(0, 1, n_in)
    if n_out > 0 and n_out < len(out):
        out[-n_out:] *= np.linspace(1, 0, n_out)
    return out


def build_timeline():
    clips = [fade(load_mono_24k(p), SR) for p in CLIP_ORDER]
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

    return speech, positions, total_len


def duck_envelope(total_len, positions, sr=SR):
    """1.0 = full music volume, duck_lin during speech (with short ramps)."""
    duck_lin = 10 ** (DUCK_DB / 20.0)
    env = np.ones(total_len)
    ramp_samps = int(0.25 * sr)
    for start, end in positions:
        r_start = max(0, start - ramp_samps)
        r_end = min(total_len, end + ramp_samps)
        # ramp down into duck
        if start > r_start:
            env[r_start:start] = np.linspace(1.0, duck_lin, start - r_start)
        env[start:end] = duck_lin
        # ramp back up
        if r_end > end:
            env[end:r_end] = np.linspace(duck_lin, 1.0, r_end - end)
    return env


def main():
    speech, positions, total_len = build_timeline()

    # load music bed, trim/loop to total_len
    bed_stereo, bed_sr = sf.read("/home/user/audio/music_bed.wav", always_2d=True)
    bed = bed_stereo.mean(axis=1)
    if bed_sr != SR:
        duration = len(bed) / bed_sr
        n_new = int(round(duration * SR))
        x_old = np.linspace(0, duration, num=len(bed), endpoint=False)
        x_new = np.linspace(0, duration, num=n_new, endpoint=False)
        bed = np.interp(x_new, x_old, bed)
    if len(bed) < total_len:
        reps = int(np.ceil(total_len / len(bed)))
        bed = np.tile(bed, reps)
    bed = bed[:total_len]

    env = duck_envelope(total_len, positions)
    bed_mixed = bed * env * 0.9  # bed base level before ducking scale

    # give intro/outro a brief full-volume music moment
    mix = speech * 1.0 + bed_mixed

    # normalize to target peak
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * TARGET_PEAK

    stereo = np.stack([mix, mix], axis=1)
    sf.write("/home/user/audio/episode_13_master.wav", stereo.astype(np.float32), SR, subtype="PCM_16")

    print("Total duration (s):", total_len / SR)
    print("Total duration (m:s):", f"{int(total_len/SR)//60}:{int(total_len/SR)%60:02d}")
    print("Peak after normalize:", np.max(np.abs(mix)))

    # write a timing map for transcript building
    with open("/home/user/audio/episode_13_timing.txt", "w") as f:
        f.write(f"intro_start=0.0\nintro_end={INTRO}\n")
        for (start, end), path in zip(positions, CLIP_ORDER):
            f.write(f"{path}\t{start/SR:.3f}\t{end/SR:.3f}\n")
        f.write(f"outro_start={(total_len-int(OUTRO*SR))/SR:.3f}\nouttro_end={total_len/SR:.3f}\n")


if __name__ == "__main__":
    main()
