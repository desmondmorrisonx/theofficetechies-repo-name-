#!/usr/bin/env python3
from __future__ import annotations
import math
from pathlib import Path
import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT, AUDIO, SR, NUM = Path("/home/user"), Path("/home/user/audio"), e3.SR, 14
MIN_DUR = 630.0
TITLE = "Martians in Grover's Mill: Orson Welles, Fake Panic, and the Disclaimer in the Footer"

CLIPS = [
    ("ep14_clip01_alex.mp3", "Alex", "cold"),
    ("ep14_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep14_clip03_alex.mp3", "Alex", "speech"),
    ("ep14_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep14_clip05_alex.mp3", "Alex", "speech"),
    ("ep14_clip06_morgan.mp3", "Morgan", "speech"),
    ("ep14_clip07_alex.mp3", "Alex", "speech"),
    ("ep14_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep14_clip09_alex.mp3", "Alex", "speech"),
    ("ep14_clip10_morgan.mp3", "Morgan", "outro"),
]
TEXTS = {
    "ep14_clip01_alex.mp3": "Wooo we are live and I am grinning so hard my face hurts! Welcome back to The Office 360 Unfiltered. I am Alex. Halloween, 1938. Orson Welles. Martians in New Jersey. The newspapers screamed louder than the Martians. If your doorbell rings later, that was no Martian.",
    "ep14_clip02_morgan.mp3": "Ha I am already laughing. I'm Morgan. October 30, 1938. Mercury Theatre on the Air, CBS. They start like a dance band, then we interrupt this program. Grover's Mill, New Jersey. People who tuned in late missed the drama label and got the cabbage-field invasion.",
    "ep14_clip03_alex.mp3": "They used the costume of news. Some packed cars. Papers, losing ads to radio, said look what this talking box has done. Modern research: the panic was smaller than the headlines. The Martians were fake. A lot of the stampede was extra sauce.",
    "ep14_clip04_morgan.mp3": "Ha the papers hyped the panic to dunk on radio. Welles signed off: if your doorbell rings and nobody's there, that was no Martian, it's Halloween. If your real thing is in an intro nobody hears, you are Grover's Mill with a shopping cart. Three clicks to what is actually happening.",
    "ep14_clip05_alex.mp3": "Picture Grover's Mill, a water tower with a plaque, a kid under a table, a young man at CBS making art in the costume of urgency. At The Office 360 we put the book, the event, the donate where a thumb can hit it. You own the keys. I love this story. Come on.",
    "ep14_clip06_morgan.mp3": "Ha subject line all caps: IS THIS REAL. Email theofficetechies@gmail.com, Story Time or Shout Out. We got you covered. This hour is long because radio should take its time, except we tell you it is us talking.",
    "ep14_clip07_alex.mp3": "We do not mock fear. We mock the buried label. Three clicks. Book. Store. Done. STUDIO50 at theoffice360.com, fifty percent off. Subscribe. Download. Tell an aunt. I am having too much fun.",
    "ep14_clip08_morgan.mp3": "Mailbox: Story Time, Shout Out, Advertise, Donate. theofficetechies@gmail.com. Pretend you tuned in late. Can you find the real thing in three taps. If the doorbell rings tonight, that was no Martian.",
    "ep14_clip09_alex.mp3": "Landing with joy. A cabbage field, a CBS mic, papers in a costume. Put the real thing where a late arrival can hear it. Mixed yarn. Funny then useful. I'm still grinning.",
    "ep14_clip10_morgan.mp3": "I'm Morgan, he's Alex, Episode Fourteen. Martians in Grover's Mill. Email us. Listen. Download. Subscribe. If the doorbell rings, it is Halloween, we love you, we got you covered. Good night. Bye!",
}

def main():
    e3.RNG = np.random.default_rng(36014)
    clips = []
    for fname, speaker, kind in CLIPS:
        mono = e3.load_mono(AUDIO / fname)
        clips.append({"file": fname, "speaker": speaker, "kind": kind, "audio": e3.stereo_voice(mono), "dur": len(mono) / SR})
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
    music *= e3.fade(n, int(0.25 * SR), int(min(5 * SR, n // 8)))[:, None]
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
    vtt, srt, md = ["WEBVTT", ""], [], [f"# Episode {NUM} Transcript", "", f"**{TITLE}**", f"**Duration:** {duration}", ""]
    for i, ev in enumerate(events, 1):
        text = TEXTS[ev["file"]]
        vtt += [f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}", f"<v {ev['speaker']}>{text}", ""]
        srt.append(f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n")
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / f"EPISODE_{NUM}_SHOW_NOTES.md").write_text(
        f"""# EPISODE NOTES — Ep {NUM:02d}

**Title:** {TITLE}
**Duration:** {duration} (10:00+)
**Hosts:** Alex & Morgan
**Artwork:** episode_14_artwork.png

## Story
Halloween 1938. Orson Welles, Mercury Theatre, CBS, War of the Worlds. Grover's Mill, N.J. Buried drama label. Newspapers amplified panic (radio rivalry). Modern research: panic overstated. Welles: if your doorbell rings, that was no Martian, it's Halloween.

Office 360 moral: late arrivals must still find the real thing in three clicks.

## CTAs
theofficetechies@gmail.com — Story Time · Shout Out · Advertise · Donate
https://the-office360.com · STUDIO50

## Keywords
The Office 360 Unfiltered, Episode 14, War of the Worlds 1938, Orson Welles, Grover's Mill, Mercury Theatre, radio panic myth, author website UX, 3-click discoverability, buried disclaimer, STUDIO50, Story Time, theofficetechies@gmail.com, listen download subscribe

## Hashtags
#Office360 #WarOfTheWorlds #OrsonWelles #GroverMill #Podcast #STUDIO50
""",
        encoding="utf-8",
    )
    print("TOTAL", duration)
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['dur']:.2f}s")

if __name__ == "__main__":
    main()
