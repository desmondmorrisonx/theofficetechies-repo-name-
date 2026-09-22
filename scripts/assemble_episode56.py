#!/usr/bin/env python3
"""Assemble Episodes 5 and 6 of The Office 360 Unfiltered."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR

EPISODES = [
    {
        "num": 5,
        "title": "From Lisbon to New York: The Anatomy of a 4-Person Senior Studio",
        "clips": [
            ("ep5_clip01_alex.mp3", "Alex", "cold"),
            ("ep5_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep5_clip03_alex.mp3", "Alex", "ad"),
            ("ep5_clip04_morgan.mp3", "Morgan", "ad"),
            ("ep5_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep5_clip01_alex.mp3": (
                "Wooo! Live from the gap between Lisbon and New York. Welcome back to The Office 360 Unfiltered. "
                "I am Alex. Last week churches, schools, publishers. This week we crack open the studio itself. "
                "Four senior people. Two cities. And how we out-build a fifty person agency that needs a meeting "
                "to schedule a meeting. Come on!"
            ),
            "ep5_clip02_morgan.mp3": (
                "Ha, he packed the whole manifesto into the open. I'm Morgan. Here is the anatomy. Traditional shop: "
                "account manager, then a project manager, then a junior who actually touches the files, then a senior "
                "who reviews it on Friday. You paid for a building. You got a hallway. The Office 360 is four seniors. "
                "You talk to the people who write the code. No intern maze. Lisbon to New York, same Slack, same repo, "
                "same standard."
            ),
            "ep5_clip03_alex.mp3": (
                "And that only works because the process is boring in the best way. Fixed scope. Fixed price. Automated QA. "
                "We do not babysit a stack that wants to break. Same philosophy I have with my own fuel, and yes this episode "
                "is sponsored by Klear, Klear with a K. Two cities, long days, I am not slamming a chalky milkshake between "
                "calls. Clear whey, drinks like juice, twenty grams of protein. We earn a commission if you use our code. "
                "It keeps this live show on the air."
            ),
            "ep5_clip04_morgan.mp3": (
                "Strawberry watermelon or wild blue raspberry. Zero sugar, zero lactose, about ninety calories. One scoop, "
                "twelve ounces of water, shake, let it settle a minute. No bloating. Exclusive twenty percent off, code MARKETPL. "
                "klearprotein.com/discount/MARKETPL. Use that link. Then if you want the studio, theoffice360.com, code STUDIO50. "
                "Four people. You own the work."
            ),
            "ep5_clip05_alex.mp3": (
                "That is the whole anatomy. Small on purpose. Senior on purpose. Two cities on purpose. If a fifty person deck "
                "impressed you and the site still loads like 2012, you already know. I'm Alex, she's Morgan, this was "
                "The Office 360 Unfiltered, sponsored in part by Klear. We love you. Bye!"
            ),
        },
        "blurb": (
            "Alex and Morgan crack open The Office 360: four seniors, Lisbon to New York, no intern maze, "
            "fixed scope, automated QA. Sponsored by Klear. Exclusive 20% off with code MARKETPL at "
            "https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code."
        ),
        "seed": 36005,
    },
    {
        "num": 6,
        "title": "You Own Every Line: Why Agencies Keep the Keys",
        "clips": [
            ("ep6_clip01_alex.mp3", "Alex", "cold"),
            ("ep6_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep6_clip03_alex.mp3", "Alex", "ad"),
            ("ep6_clip04_morgan.mp3", "Morgan", "ad"),
            ("ep6_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep6_clip01_alex.mp3": (
                "We are live and I brought a pet peeve. Welcome back to The Office 360 Unfiltered. I am Alex. "
                "Today is about keys. Who holds them. Agencies love to build your site and then keep the repo, "
                "the fonts, the logins, the whole house. You paid for a home. You got a lease. Come on!"
            ),
            "ep6_clip02_morgan.mp3": (
                "Ha, I have seen the email. Sorry, we cannot export that, it is in our proprietary theme. Sorry, "
                "the designer owns the Figma. Sorry, hosting is in our account and the password is a secret. "
                "That is not partnership. That is a hostage note with a status meeting. At The Office 360 you own "
                "every line of code. Every asset. Period."
            ),
            "ep6_clip03_alex.mp3": (
                "Four seniors, Lisbon to New York, we hand you the keys because we do not make money trapping you. "
                "Fixed scope, you know the number, and when we are done it is yours. Same energy as not drinking "
                "mystery sludge. This episode is sponsored by Klear. Clear protein, you can literally see it. "
                "Twenty grams, zero sugar, zero lactose. We earn a commission on code MARKETPL. That supports the show."
            ),
            "ep6_clip04_morgan.mp3": (
                "If you are done with chalk and done with lock-in, here is your homework. Ask your current shop for "
                "the repo, the design files, and the domain logins. If they stall, call us. theoffice360.com, STUDIO50. "
                "And for the shaker, klearprotein.com/discount/MARKETPL. Twenty percent off. Strawberry watermelon. "
                "I'm just saying."
            ),
            "ep6_clip05_alex.mp3": (
                "Own the site. Own the fuel. Don't rent your own stack. I'm Alex, she's Morgan, The Office 360 Unfiltered, "
                "sponsored in part by Klear. Code MARKETPL. We love you. Bye!"
            ),
        },
        "blurb": (
            "Alex and Morgan go after agency lock-in: proprietary themes, hidden repos, passwords you don't get. "
            "The Office 360 hands you every line of code. Sponsored by Klear. 20% off code MARKETPL: "
            "https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code."
        ),
        "seed": 36006,
    },
]


def assemble(ep: dict) -> None:
    e3.RNG = np.random.default_rng(ep["seed"])
    clips = []
    for fname, speaker, kind in ep["clips"]:
        path = AUDIO / fname
        if not path.exists():
            raise SystemExit(f"missing {path}")
        mono = e3.load_mono(path)
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
    n = int(total * SR)
    print(f"EP{ep['num']} Building {total:.2f}s")

    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], axis=0)
    music = music[:n]

    duck_speech = e3.db(-24)
    duck_ad = e3.db(-13)
    regions = [(0, int(e3.INTRO_PAD * SR), e3.db(-6.5))]
    for ev in events:
        s = int(ev["start"] * SR)
        e = int(ev["end"] * SR)
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

    num = ep["num"]
    wav_path = ROOT / f"The_Office_360_Unfiltered_Episode_{num}.wav"
    mp3_path = ROOT / f"The_Office_360_Unfiltered_Episode_{num}.mp3"
    sf.write(str(wav_path), mix, SR, subtype="PCM_16")
    sf.write(str(mp3_path), mix, SR, format="MP3")

    dur_mm, dur_ss = int(total // 60), int(total % 60)
    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md = [
        f"# The Office 360 Unfiltered — Episode {num} Transcript",
        "",
        f"**Title:** {ep['title']}",
        f"**Duration:** {dur_mm:02d}:{dur_ss:02d}",
        "**Hosts:** Alex & Morgan",
        "**Sponsor:** Klear Juicy Protein — we earn a commission when you use our code.",
        "",
        "## Description / Show Notes",
        "",
        ep["blurb"],
        "",
        "### Sponsor (exclusive listener discount)",
        "",
        "- **20% OFF** any Klear product with code **MARKETPL**",
        "- https://klearprotein.com/discount/MARKETPL",
        "- https://klearprotein.com",
        "- Flavors: Strawberry Watermelon · Wild Blue Raspberry",
        "- 20g protein · 0 sugar · 0 lactose · ~90 calories · just add water",
        "- We earn a commission when you use our code. If you buy, you support the show.",
        "",
        "### Studio",
        "",
        "- https://the-office360.com",
        "- Code **STUDIO50** — 50% off studio tiers",
        "- theofficetechies@gmail.com",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        text = ep["texts"][ev["file"]]
        vtt.append(f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}")
        vtt.append(f"<v {ev['speaker']}>{text}")
        vtt.append("")
        srt_blocks.append(
            f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n"
        )
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]

    (ROOT / f"TRANSCRIPT_EPISODE_{num}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{num}.srt").write_text("\n".join(srt_blocks), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{num}.md").write_text("\n".join(md), encoding="utf-8")

    notes = f"""# Episode {num} — Show Notes & Description

**The Office 360 Unfiltered — Ep {num:02d}**
{ep['title']}
Sponsored by Klear Juicy Protein
Duration: {dur_mm}:{dur_ss:02d}

## Paste-ready podcast description

{ep['blurb']}

THIS EPISODE IS SPONSORED BY KLEAR (Klear with a K).
Clear whey protein isolate that drinks like juice, not a chalky shake.
20g protein · 0 sugar · 0 lactose · ~90 calories
Flavors: Strawberry Watermelon and Wild Blue Raspberry
Just add water: 1 scoop + 12 oz, shake, settle 1 minute.

EXCLUSIVE LISTENER DISCOUNT — 20% OFF any Klear product
Code: MARKETPL
Link: https://klearprotein.com/discount/MARKETPL
Store: https://klearprotein.com

We earn a commission when you use our code. If you buy, you support the show.

Studio: https://the-office360.com
Code STUDIO50 — 50% off studio tiers
theofficetechies@gmail.com
"""
    (ROOT / f"EPISODE_{num}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <language>en-us</language>
    <item>
      <title>Episode {num}: {ep['title'].replace('&', '&amp;')} (sponsored by Klear)</title>
      <description>{ep['blurb'].replace('&', '&amp;')}</description>
      <guid isPermaLink="false">office360-unfiltered-ep{num}</guid>
      <itunes:duration>{dur_mm}:{dur_ss:02d}</itunes:duration>
      <link>https://klearprotein.com/discount/MARKETPL</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / f"EPISODE_{num}_RSS.xml").write_text(rss, encoding="utf-8")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")


if __name__ == "__main__":
    for ep in EPISODES:
        assemble(ep)
    print("done")
