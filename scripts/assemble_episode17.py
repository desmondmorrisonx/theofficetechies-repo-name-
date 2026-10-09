#!/usr/bin/env python3
"""Ep17 mix: 24 kHz, 380 ms gaps, duck −24 under speech, peak 0.94. No empty pad."""
from pathlib import Path
import numpy as np
from pydub import AudioSegment

SR = 24000
GAP_MS = 380
PEAK = 0.94
DUCK_DB = -24
BED_UNDER = -18  # bed level vs full scale before duck
INTRO_MS = 1200
OUTRO_MS = 4000

ROOT = Path("/home/user")
CLIPS = [
    ROOT / "audio/ep17_clip01_alex.mp3",
    ROOT / "audio/ep17_clip02_morgan.mp3",
    ROOT / "audio/ep17_clip03_alex.mp3",
    ROOT / "audio/ep17_clip04_morgan.mp3",
    ROOT / "audio/ep17_clip05_alex.mp3",
    ROOT / "audio/ep17_clip06_morgan.mp3",
    ROOT / "audio/ep17_clip07_alex.mp3",
    ROOT / "audio/ep17_clip08_morgan.mp3",
    ROOT / "audio/ep17_clip09_alex.mp3",
    ROOT / "audio/ep17_clip10_morgan.mp3",
]
OUT = ROOT / "The_Office_360_Unfiltered_Episode_17.mp3"
HOSTS = ["Alex", "Morgan"] * 5


def load(path: Path) -> AudioSegment:
    a = AudioSegment.from_file(path)
    a = a.set_frame_rate(SR).set_channels(1).set_sample_width(2)
    return a


def np_to_seg(x: np.ndarray) -> AudioSegment:
    x = np.clip(x, -1.0, 1.0)
    pcm = (x * 32767.0).astype(np.int16).tobytes()
    return AudioSegment(data=pcm, sample_width=2, frame_rate=SR, channels=1)


def make_bed(ms: int) -> AudioSegment:
    n = int(SR * ms / 1000.0)
    t = np.arange(n) / float(SR)
    # dusty two-chord lo-fi, do not fight the voices
    bpm = 76.0
    beat = 60.0 / bpm
    kick = np.zeros(n)
    for i, k in enumerate(np.arange(0, t[-1], beat)):
        env_i = int(k * SR)
        leng = int(0.08 * SR)
        if env_i + leng >= n:
            break
        te = np.arange(leng) / SR
        if i % 4 != 3:
            kick[env_i : env_i + leng] += np.sin(2 * np.pi * 48 * te) * np.exp(-te * 28)
    bass = 0.12 * np.sin(2 * np.pi * 55 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 8))
    chord = (
        0.04 * np.sin(2 * np.pi * 164.81 * t)
        + 0.03 * np.sin(2 * np.pi * 196.00 * t)
        + 0.025 * np.sin(2 * np.pi * 246.94 * t)
    ) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 11))
    hiss = 0.008 * np.random.default_rng(16).standard_normal(n)
    x = kick * 0.22 + bass + chord + hiss
    # fade ends
    fade = int(0.04 * SR)
    x[:fade] *= np.linspace(0, 1, fade)
    x[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(x)) or 1.0
    x = x / peak * 0.35
    return np_to_seg(x) + BED_UNDER


def main():
    parts = [load(p) for p in CLIPS]
    silence = AudioSegment.silent(duration=GAP_MS, frame_rate=SR).set_channels(1).set_sample_width(2)
    intro = AudioSegment.silent(duration=INTRO_MS, frame_rate=SR).set_channels(1).set_sample_width(2)
    outro = AudioSegment.silent(duration=OUTRO_MS, frame_rate=SR).set_channels(1).set_sample_width(2)

    speech = intro
    t = INTRO_MS
    marks = []
    for i, p in enumerate(parts):
        marks.append((t, t + len(p), HOSTS[i], len(p)))
        speech += p
        t += len(p)
        if i < len(parts) - 1:
            speech += silence
            t += GAP_MS
    speech += outro
    total_ms = len(speech)

    bed = make_bed(total_ms)
    # duck bed under every speech region
    ducked = bed
    for start, end, host, dur in marks:
        # extra 40ms pad on duck
        s = max(0, start - 40)
        e = min(total_ms, end + 80)
        piece = ducked[s:e] + DUCK_DB
        ducked = ducked[:s] + piece + ducked[e:]

    mix = ducked.overlay(speech)
    # peak 0.94
    samples = np.array(mix.get_array_of_samples()).astype(np.float32)
    peak = np.max(np.abs(samples)) or 1.0
    samples = samples / peak * (PEAK * 32767.0)
    mix = mix._spawn(samples.astype(np.int16).tobytes())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    mix.export(OUT, format="mp3", bitrate="192k", parameters=["-ar", str(SR)])
    sec = len(mix) / 1000.0
    mm = int(sec // 60)
    ss = int(round(sec % 60))
    print(f"TOTAL {mm:02d}:{ss:02d}  ({sec:.2f}s)")
    for start, end, host, dur in marks:
        print(f"  {start/1000:7.2f}-{end/1000:7.2f}  {host:6s}  {dur/1000:6.2f}s")
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
