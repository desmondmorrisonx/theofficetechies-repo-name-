"""
Generate a lo-fi Rhodes-style music bed at ~78 BPM for The Office 360 Unfiltered.
Pure numpy synthesis: warm electric-piano-like tones (sine + slight FM + soft
attack/decay), a subtle laid-back kick/hat pulse, light vinyl-style noise
texture, gentle lowpass "lo-fi" filtering. Loops seamlessly.
"""
import numpy as np
import sys

SR = 44100
BPM = 78
BEAT = 60.0 / BPM  # seconds per beat

def rhodes_tone(freq, dur, sr=SR, amp=1.0):
    n = int(dur * sr)
    t = np.arange(n) / sr
    # Fundamental + a couple of slightly detuned harmonics for that "electric piano" bell/bark
    fm_mod = 1.0 + 0.0025 * np.sin(2 * np.pi * (freq * 2.01) * t)
    sig = np.sin(2 * np.pi * freq * t * fm_mod)
    sig += 0.35 * np.sin(2 * np.pi * (freq * 2.0) * t) * np.exp(-3.0 * t)
    sig += 0.15 * np.sin(2 * np.pi * (freq * 4.0) * t) * np.exp(-6.0 * t)
    # soft attack, exponential decay envelope (electric piano-like)
    attack = int(0.008 * sr)
    env = np.ones(n)
    if attack > 0 and attack < n:
        env[:attack] = np.linspace(0, 1, attack)
    decay = np.exp(-1.1 * t)
    env = env * decay
    return amp * sig * env

def chord(freqs, dur, amp=0.9):
    out = None
    for f in freqs:
        tone = rhodes_tone(f, dur, amp=amp / max(1, len(freqs)) ** 0.5)
        out = tone if out is None else out[: len(tone)] + tone[: len(out)] if len(tone) != len(out) else out + tone
    return out

def note_freq(name_octave):
    notes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6,
             "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    name = name_octave[:-1]
    octave = int(name_octave[-1])
    semitone = notes[name] + (octave - 4) * 12
    return 440.0 * (2 ** (semitone / 12.0))

def lowpass(sig, sr=SR, cutoff=3200.0):
    # simple one-pole lowpass for lo-fi warmth
    rc = 1.0 / (2 * np.pi * cutoff)
    dt = 1.0 / sr
    alpha = dt / (rc + dt)
    out = np.zeros_like(sig)
    prev = 0.0
    for i in range(len(sig)):
        prev = prev + alpha * (sig[i] - prev)
        out[i] = prev
    return out

def soft_pulse(n, sr=SR, kind="kick"):
    t = np.arange(n) / sr
    if kind == "kick":
        freq = 90 * np.exp(-18 * t)
        sig = np.sin(2 * np.pi * np.cumsum(freq) / sr)
        env = np.exp(-14 * t)
    else:  # soft hat / tick
        sig = np.random.default_rng(1).standard_normal(n)
        env = np.exp(-40 * t)
    return sig * env

def build_bed(total_dur, sr=SR):
    beats_per_bar = 4
    bar_dur = BEAT * beats_per_bar
    n_bars = int(np.ceil(total_dur / bar_dur)) + 1

    # gentle jazzy lo-fi progression: Cmaj7 - Am7 - Fmaj7 - G7 (one chord per bar)
    progression = [
        [note_freq("C3"), note_freq("E3"), note_freq("G3"), note_freq("B3")],
        [note_freq("A2"), note_freq("C3"), note_freq("E3"), note_freq("G3")],
        [note_freq("F2"), note_freq("A2"), note_freq("C3"), note_freq("E3")],
        [note_freq("G2"), note_freq("B2"), note_freq("D3"), note_freq("F3")],
    ]

    total_len = int(total_dur * sr) + sr  # small buffer
    bed = np.zeros(total_len)
    kick_hat = np.zeros(total_len)

    rng = np.random.default_rng(42)
    pos = 0
    bar_i = 0
    while pos < total_len:
        chord_freqs = progression[bar_i % len(progression)]
        # Rhodes plays a soft chord stab on beat 1 and a lighter one on beat 3
        stab1 = chord(chord_freqs, bar_dur * 0.95, amp=0.5)
        stab3 = chord([f * 1.0 for f in chord_freqs[:3]], bar_dur * 0.5, amp=0.32)

        end1 = min(pos + len(stab1), total_len)
        bed[pos:end1] += stab1[: end1 - pos]

        pos3 = pos + int(2 * BEAT * sr)
        end3 = min(pos3 + len(stab3), total_len)
        if pos3 < total_len:
            bed[pos3:end3] += stab3[: end3 - pos3]

        # laid-back lo-fi drum pulse: soft kick on 1 and 3, soft hat tick on 2 and 4
        for beat_idx, kind in [(0, "kick"), (1, "hat"), (2, "kick"), (3, "hat")]:
            hp = pos + int(beat_idx * BEAT * sr)
            n_pulse = int(0.12 * sr)
            end_p = min(hp + n_pulse, total_len)
            if hp < total_len:
                pulse = soft_pulse(end_p - hp, sr=sr, kind=kind)
                gain = 0.05 if kind == "kick" else 0.02
                kick_hat[hp:end_p] += pulse * gain

        pos += int(bar_dur * sr)
        bar_i += 1

    bed = bed[:total_len]
    kick_hat = kick_hat[:total_len]
    mix = bed + kick_hat

    # lo-fi warmth: lowpass filter (subsample for speed on long buffers using vectorized approx)
    # Vectorized one-pole lowpass via lfilter for speed
    from scipy.signal import lfilter
    cutoff = 3400.0
    rc = 1.0 / (2 * np.pi * cutoff)
    dt = 1.0 / sr
    alpha = dt / (rc + dt)
    mix = lfilter([alpha], [1, -(1 - alpha)], mix)

    # subtle vinyl-style noise bed for texture
    noise = rng.standard_normal(total_len) * 0.0025
    noise = lfilter([0.02], [1, -0.98], noise)  # soften noise spectrum
    mix = mix + noise

    # normalize bed to a modest level (it will be ducked under speech later)
    peak = np.max(np.abs(mix)) + 1e-9
    mix = mix / peak * 0.6

    return mix[: int(total_dur * sr)].astype(np.float32), sr


if __name__ == "__main__":
    total_dur = float(sys.argv[1]) if len(sys.argv) > 1 else 260.0
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/home/user/audio/music_bed.wav"
    bed, sr = build_bed(total_dur)
    stereo = np.stack([bed, bed], axis=1)
    import soundfile as sf
    sf.write(out_path, stereo, sr, subtype="PCM_16")
    print("wrote", out_path, "dur", len(bed) / sr)
