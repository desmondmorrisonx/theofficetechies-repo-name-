#!/usr/bin/env python3
from __future__ import annotations
import math
from pathlib import Path
import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT, AUDIO, SR, NUM = Path("/home/user"), Path("/home/user/audio"), e3.SR, 15
MIN_DUR = 630.0
TITLE = "The Eight-Minute Website and the Ten-Books-a-Week Author: AI Slop, Zero Clicks, and office-360.com"

CLIPS = [
    ("ep15_clip01_alex.mp3", "Alex"),
    ("ep15_clip02_morgan.mp3", "Morgan"),
    ("ep15_clip03_alex.mp3", "Alex"),
    ("ep15_clip04_morgan.mp3", "Morgan"),
    ("ep15_clip05_alex.mp3", "Alex"),
    ("ep15_clip06_morgan.mp3", "Morgan"),
    ("ep15_clip07_alex.mp3", "Alex"),
    ("ep15_clip08_morgan.mp3", "Morgan"),
    ("ep15_clip09_alex.mp3", "Alex"),
    ("ep15_clip10_morgan.mp3", "Morgan"),
]
TEXTS = {
    "ep15_clip01_alex.mp3": "Wooo we are live. Authors publishing ten books a week with a chatbot. Grandma googles and never leaves Google. An eight-minute site that sells zero. This is Episode Fifteen. We walk you to office 360 dot com.",
    "ep15_clip02_morgan.mp3": "I'm Morgan. Amazon 2026 slop. Bill Johns, hundreds of titles, ten books a week at Amazon's cap. A vending machine in a cardigan. Real authors standing in a blizzard of paperbacks nobody asked for.",
    "ep15_clip03_alex.mp3": "Zero click. AI Overviews. The sidewalk answers and your site is a party with no guests. The eight-minute website: pretty lobby, buy button to nowhere. The fix is a doorbell.",
    "ep15_clip04_morgan.mp3": "The eight-minute site hallucinates calendars and example.com carts. If AI writes the sidewalk, your house must be findable when someone knocks. Book. Store. Done.",
    "ep15_clip05_alex.mp3": "The Office 360. Four seniors. Lisbon to New York. You own the code. Three-click discoverability. office 360 dot com. STUDIO50. Half off. A house with keys, not a vending machine.",
    "ep15_clip06_morgan.mp3": "You cannot out-slop the slop. Email theofficetechies@gmail.com: Story Time, Shout Out, Advertise, Donate. Then office 360 dot com.",
    "ep15_clip07_alex.mp3": "Ten books a week should be in a museum. Real IA, real HTTPS, real forms, real ownership. office 360 dot com. STUDIO50. A true book with a doorbell outlives a blizzard of slop.",
    "ep15_clip08_morgan.mp3": "Mailbox: Story Time, Shout Out, Advertise, Donate. Pretend you just left an AI overview. Three taps to the book. office 360 dot com.",
    "ep15_clip09_alex.mp3": "Landing. Blizzard of paperbacks, sidewalk answers, eight-minute lobby. office 360 dot com. STUDIO50. Subscribe. Download. Tell an aunt. The doorbell works.",
    "ep15_clip10_morgan.mp3": "Episode Fifteen. Ten books a week, zero clicks, eight-minute websites, doorbell at office 360 dot com. Email us. Listen. Download. Subscribe. Bye!",
}

def main():
    e3.RNG = np.random.default_rng(36015)
    clips = []
    for fname, speaker in CLIPS:
        mono = e3.load_mono(AUDIO / fname)
        clips.append({"file": fname, "speaker": speaker, "audio": e3.stereo_voice(mono), "dur": len(mono) / SR})
    t = e3.INTRO_PAD
    events = []
    for i, c in enumerate(clips):
        start, end = t, t + c["dur"]
        events.append({**c, "start": start, "end": end})
        t = end if i == len(clips) - 1 else end + e3.PAUSE
    outro = 15.0
    total = t + outro
    if total < MIN_DUR:
        outro += MIN_DUR - total
        total = t + outro
    n = int(total * SR)
    print(f"Building {total:.2f}s ({int(total//60)}:{int(total%60):02d})")
    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], 0)
    music = music[:n]
    duck = e3.db(-24)
    regions = [(0, int(e3.INTRO_PAD * SR), e3.db(-6.5))]
    for ev in events:
        regions.append((int(ev["start"] * SR), int(ev["end"] * SR), duck))
    regions.append((int(events[-1]["end"] * SR), n, e3.db(-7.0)))
    music = music * e3.smooth_gain_curve(n, regions, duck)[:, None]
    music *= e3.fade(n, int(0.25 * SR), int(min(6 * SR, n // 8)))[:, None]
    mix = music.copy()
    for ev in events:
        s = int(ev["start"] * SR)
        a = ev["audio"]
        e = min(n, s + len(a))
        mix[s:e] += a[: e - s]
    peak = np.max(np.abs(mix)) + 1e-12
    mix = np.tanh(mix / peak * e3.PEAK * 1.02) / math.tanh(1.02) * e3.PEAK
    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{NUM}.wav"), mix, SR, subtype="PCM_16")
    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{NUM}.mp3"), mix, SR, format="MP3")
    dur_mm, dur_ss = int(total // 60), int(total % 60)
    duration = f"{dur_mm}:{dur_ss:02d}"
    vtt, srt, md = ["WEBVTT", ""], [], [f"# Episode {NUM}", f"**{TITLE}**", f"**{duration}**", ""]
    for i, ev in enumerate(events, 1):
        text = TEXTS[ev["file"]]
        vtt += [f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}", f"<v {ev['speaker']}>{text}", ""]
        srt.append(f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n")
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.md").write_text("\n".join(md), encoding="utf-8")
    print("TOTAL", duration)
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['dur']:.2f}s")

if __name__ == "__main__":
    main()
