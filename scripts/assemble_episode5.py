#!/usr/bin/env python3
"""Assemble Episode 5 recut (4:00 minimum) of The Office 360 Unfiltered."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
NUM = 5
TITLE = "Lisbon to New York: The Anatomy of a 4-Person Senior Studio (Sponsored by Klear)"
SHORT = "From Lisbon to New York: How four seniors outbuild a 50-person hallway."

CLIPS = [
    ("ep5v2_clip01_alex.mp3", "Alex", "cold"),
    ("ep5v2_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep5v2_clip03_alex.mp3", "Alex", "speech"),
    ("ep5v2_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep5v2_clip05_alex.mp3", "Alex", "speech"),
    ("ep5v2_clip06_morgan.mp3", "Morgan", "ad"),
    ("ep5v2_clip07_alex.mp3", "Alex", "ad"),
    ("ep5v2_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep5v2_clip09_alex.mp3", "Alex", "speech"),
    ("ep5v2_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep5v2_clip01_alex.mp3": (
        "Wooo! Live from the gap between Lisbon and New York. Welcome back to The Office 360 Unfiltered. "
        "I am Alex. This episode is the anatomy of the studio itself, and it is sponsored by Klear. Four senior "
        "people. Two cities. And how we out-build a fifty person agency that needs a meeting to schedule a meeting. "
        "If you have ever paid for a building and got a hallway, come on. This one is for you."
    ),
    "ep5v2_clip02_morgan.mp3": (
        "Ha, he packed the manifesto into the open. I'm Morgan. Here is the traditional anatomy. Account manager. "
        "Then a project manager. Then a junior who actually touches the files. Then a senior who reviews it on Friday "
        "if nobody is on PTO. You paid for a studio. You got a hallway with name tags. The Office 360 is four seniors. "
        "You talk to the people who write the code. No intern maze. Lisbon to New York, same Slack, same repo, same standard."
    ),
    "ep5v2_clip03_alex.mp3": (
        "And that only works because the process is boring in the best way. Fixed scope. Fixed price. You know the number "
        "before we write a line. Automated QA, so we are not babysitting a stack that wants to break every Tuesday. "
        "No proprietary theme. No, wait for the junior to get unblocked. Authors, schools, publishers, churches, you do "
        "not need fifty people. You need four who have done this, and a contract that hands you the keys."
    ),
    "ep5v2_clip04_morgan.mp3": (
        "The client-truth version. When something breaks at nine at night in New York, you are not opening a ticket that "
        "lands in a queue in another time zone with a bot. You are talking to the person whose name is on the commit. "
        "That is the whole flex. Small on purpose. Senior on purpose. Two cities on purpose, because the work is async "
        "and the standard is not. If a fifty person deck impressed you and the site still loads like 2012, you already know."
    ),
    "ep5v2_clip05_alex.mp3": (
        "We do three-click discoverability. We do Jamstack when it should be Jamstack. We do not sell you a retainer to "
        "click update plugins. We do not hide juniors in the spreadsheet. When the invoice is paid, you own every line of "
        "code. That is not a slogan. That is how a four person senior studio beats a hallway. Clean architecture. Clean "
        "process. And yes, clean fuel, because this episode is sponsored by Klear, Klear with a K."
    ),
    "ep5v2_clip06_morgan.mp3": (
        "Two cities, long days, nobody on this team is slamming a chalky milkshake between calls. Traditional protein is "
        "thick, secret, and sits in your stomach like a proprietary theme. Klear is clear whey isolate. You can literally "
        "see it. Twenty grams of protein, zero sugar, zero lactose, about ninety calories. We earn a commission if you use "
        "our code. That keeps this live show on the air, and I would rather tell you that than hide it."
    ),
    "ep5v2_clip07_alex.mp3": (
        "Strawberry watermelon is the one. Wild blue raspberry if you want the tang. One scoop, twelve ounces of water, "
        "shake it, let it settle a minute, drink it like a sports drink, not a gym brick. Exclusive twenty percent off, "
        "the best cut they are giving. Code MARKETPL. klearprotein.com/discount/MARKETPL. Use that link, not a random one. "
        "Same rule as the repo. Use the keys that are actually yours."
    ),
    "ep5v2_clip08_morgan.mp3": (
        "Homework. If you are still in a hallway, ask who actually writes your code. If the answer is a junior you have "
        "never met, call us. theoffice360.com. Code STUDIO50. Fifty percent off the studio tiers. Turnkey Build, IA Roadmap, "
        "HTTPS Security. Email theofficetechies@gmail.com. Four people. Lisbon to New York. You own the work."
    ),
    "ep5v2_clip09_alex.mp3": (
        "I love this show because the studio and the shaker are the same philosophy. Don't rent a fifty person performance. "
        "Don't swallow the heavy version because a brochure said protein. Small on purpose. Clear on purpose. Authors, "
        "schools, publishers, churches, if your site needs a meeting to schedule a meeting, it is not your people. It is "
        "the hallway. We build, we hand you the keys, we get out of the way."
    ),
    "ep5v2_clip10_morgan.mp3": (
        "If your protein still tastes like chalk, Klear, klearprotein.com, code MARKETPL, twenty percent off. If your agency "
        "is a hallway, you know where we live. I'm Morgan, he's Alex, this was The Office 360 Unfiltered, from Lisbon to "
        "New York, sponsored by Klear. We love you. Bye!"
    ),
}

KEYWORDS = (
    "The Office 360 Unfiltered, Office 360 Lisbon New York, 4-person senior web studio, boutique web architecture, "
    "fixed scope web agency, no junior freelancers, Jamstack studio, three-click discoverability, "
    "authors schools publishers churches websites, STUDIO50, Klear protein, Klear juicy protein, "
    "clear whey protein isolate, lactose free protein, sugar free protein, strawberry watermelon protein, "
    "wild blue raspberry protein, MARKETPL, klearprotein.com, 20% off protein powder"
)


def main() -> None:
    e3.RNG = np.random.default_rng(36005)
    clips = []
    for fname, speaker, kind in CLIPS:
        mono = e3.load_mono(AUDIO / fname)
        clips.append(
            {
                "file": fname,
                "speaker": speaker,
                "kind": kind,
                "audio": e3.stereo_voice(mono),
                "dur": len(mono) / SR,
            }
        )

    t = e3.INTRO_PAD
    events = []
    for i, c in enumerate(clips):
        start = t
        end = t + c["dur"]
        events.append({**c, "start": start, "end": end})
        if i == len(clips) - 1:
            t = end
        elif c["kind"] == "ad":
            t = end + 0.50
        else:
            t = end + e3.PAUSE
    total = t + e3.OUTRO_PAD
    if total < 240:
        raise SystemExit(f"under 4:00 ({total:.1f}s)")
    n = int(total * SR)
    print(f"Building {total:.2f}s ({int(total//60)}:{int(total%60):02d})")

    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], axis=0)
    music = music[:n]

    duck_speech, duck_ad = e3.db(-24), e3.db(-13)
    regions = [(0, int(e3.INTRO_PAD * SR), e3.db(-6.5))]
    for ev in events:
        s, e = int(ev["start"] * SR), int(ev["end"] * SR)
        regions.append((s, e, duck_ad if ev["kind"] == "ad" else duck_speech))
    regions.append((int(events[-1]["end"] * SR), n, e3.db(-7.5)))
    g = e3.smooth_gain_curve(n, regions, duck_speech)
    music = music * g[:, None]
    music *= e3.fade(n, int(0.25 * SR), int(3.2 * SR))[:, None]

    mix = music.copy()
    for ev in events:
        s = int(ev["start"] * SR)
        a = ev["audio"]
        e = min(n, s + len(a))
        mix[s:e] += a[: e - s]

    peak = np.max(np.abs(mix)) + 1e-12
    mix = mix / peak * e3.PEAK
    mix = np.tanh(mix * 1.02) / math.tanh(1.02) * e3.PEAK

    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{NUM}.wav"), mix, SR, subtype="PCM_16")
    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{NUM}.mp3"), mix, SR, format="MP3")

    dur_mm, dur_ss = int(total // 60), int(total % 60)
    duration = f"{dur_mm}:{dur_ss:02d}"

    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md = [
        f"# The Office 360 Unfiltered — Episode {NUM} Transcript",
        "",
        f"**Title:** {TITLE}",
        f"**Duration:** {dur_mm:02d}:{dur_ss:02d}",
        "**Hosts:** Alex & Morgan",
        "**Sponsor:** Klear Juicy Protein",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        text = TEXTS[ev["file"]]
        vtt.append(f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}")
        vtt.append(f"<v {ev['speaker']}>{text}")
        vtt.append("")
        srt_blocks.append(f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n")
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]

    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.srt").write_text("\n".join(srt_blocks), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.md").write_text("\n".join(md), encoding="utf-8")

    notes = f"""# EPISODE NOTES — Ep {NUM:02d}

**Show:** The Office 360 Unfiltered
**Episode:** {NUM:02d}
**Title (with sponsor):** {TITLE}
**Short title:** {SHORT}
**Duration:** {duration} (4:00 minimum)
**Hosts:** Alex (lead) & Morgan (co-host)
**Studio:** The Office 360 — https://the-office360.com
**Artwork:** episode_{NUM}_artwork.png

## Sponsor
**Klear Juicy Protein** (Klear with a K) — this episode is sponsored by Klear.
- 20g clear whey protein isolate · 0 sugar · 0 lactose · ~90 calories
- Flavors: Strawberry Watermelon · Wild Blue Raspberry
- Mix: 1 scoop + 12 oz water, shake, settle 1 minute
- Exclusive listener discount: **20% OFF** code **MARKETPL**
- Link (use this): https://klearprotein.com/discount/MARKETPL
- Store: https://klearprotein.com
- FTC: We earn a commission when you use our code. If you buy, you support the show.

## Studio CTA
- https://the-office360.com
- Code **STUDIO50** — 50% off Turnkey Build / IA Roadmap / HTTPS Security
- theofficetechies@gmail.com

## Paste-ready podcast description
{TITLE}

{SHORT} Alex and Morgan crack open The Office 360: four seniors, Lisbon to New York, no intern maze, fixed scope, automated QA, you own every line of code. If you paid for a building and got a hallway, this one is for you.

Sponsored by Klear Juicy Protein — clear whey that drinks like juice, not a chalky shake. Exclusive 20% off with code MARKETPL: https://klearprotein.com/discount/MARKETPL
We earn a commission when you use our code.

Studio: https://the-office360.com · STUDIO50 · theofficetechies@gmail.com

## Episode keywords (SEO / RSS / YouTube / Apple tags)
{KEYWORDS}

## Hashtags
#Office360 #TheOffice360Unfiltered #Lisbon #NewYork #WebStudio #Jamstack #FixedScope #KlearProtein #MARKETPL #ClearWhey #STUDIO50
"""
    (ROOT / f"EPISODE_{NUM}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <language>en-us</language>
    <itunes:keywords>{KEYWORDS}</itunes:keywords>
    <item>
      <title>{TITLE.replace('&', '&amp;')}</title>
      <description>{SHORT.replace('&', '&amp;')} Sponsored by Klear. 20% off code MARKETPL at https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code. Studio: STUDIO50 at https://the-office360.com</description>
      <guid isPermaLink="false">office360-unfiltered-ep{NUM}</guid>
      <itunes:duration>{duration}</itunes:duration>
      <itunes:keywords>{KEYWORDS}</itunes:keywords>
      <link>https://klearprotein.com/discount/MARKETPL</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / f"EPISODE_{NUM}_RSS.xml").write_text(rss, encoding="utf-8")
    print("Wrote masters + notes")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")
    print("TOTAL", duration)


if __name__ == "__main__":
    main()
