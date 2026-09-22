#!/usr/bin/env python3
"""Assemble The Office 360 Unfiltered — Episode 4 broadcast master."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import soundfile as sf
import numpy as np

e3.RNG = np.random.default_rng(36004)  # same bed character, fresh seed

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR

CLIPS = [
    ("ep4_clip01_alex.mp3", "Alex", "cold"),
    ("ep4_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep4_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep4_clip05_alex.mp3", "Alex", "ad"),
    ("ep4_clip06_morgan.mp3", "Morgan", "ad"),
    ("ep4_clip07_alex.mp3", "Alex", "speech"),
    ("ep4_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep4_clip09_alex.mp3", "Alex", "speech"),
    ("ep4_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep4_clip01_alex.mp3": (
        "Wooo we are live again! If you were here last week we dragged that ten thousand dollar "
        "WordPress retainer into the street and I am still laughing. Welcome back to The Office 360 "
        "Unfiltered. I am Alex. Today we are talking about the sites that actually matter to real people. "
        "Churches. Schools. Publishers. And why accessibility is not a nice-to-have. It is the front door. Come on!"
    ),
    "ep4_clip02_morgan.mp3": (
        "Ha, he is already standing. I'm Morgan. Picture a church homepage where Sunday service is four "
        "menus deep. A school portal that takes eight taps to find the calendar. A publisher site where "
        "the book is hiding under a popup. Grandma cannot find the donate button. The kid cannot find the "
        "event. That is not a design choice. That is a locked door with a pretty logo on it."
    ),
    "ep4_clip04_morgan.mp3": (
        "And we have audited this for real. Broken event calendars. Forms that die on a phone. Play buttons "
        "that do not play for anyone using a screen reader. Faith orgs and schools are not asking for neon "
        "startup vibes. They are asking, can my people actually use this. When we rebuild it clean, engagement "
        "comes back because the community can finally find the thing."
    ),
    "ep4_clip05_alex.mp3": (
        "Alright I gotta tell you something because it is the same joke in a shaker bottle. Last week we "
        "roasted stacks that get heavy and bloated and then bill you to babysit the bloat. I was doing that "
        "to my own body. Chalky shakes, milk, that thick gym sludge between calls. This episode is sponsored "
        "by Klear. That is Klear with a K. Clear whey protein isolate. Light. Looks like juice. And yes, we "
        "earn a commission if you use our code. It helps keep this live show on the air."
    ),
    "ep4_clip06_morgan.mp3": (
        "Ha, and it is not a vanilla brick. Strawberry watermelon. Wild blue raspberry. Twenty grams of protein, "
        "zero sugar, zero lactose, about ninety calories. You mix one scoop with twelve ounces of water, shake it, "
        "let it settle a minute, and you drink it like a sports drink, not a milkshake. No bloating. Built for people "
        "who actually move. Listeners, this is the best exclusive cut they are giving. Twenty percent off. Code MARKETPL. "
        "Go to klearprotein.com/discount/MARKETPL. Link is in the description. Use that link, not a random one."
    ),
    "ep4_clip07_alex.mp3": (
        "That is the whole philosophy. Don't swallow the heavy version just because that is what the industry sold you. "
        "Same with your website. Authors, schools, publishers, churches, if your site needs a tour guide, it is the "
        "architecture. We build it so a parent on a bus can find pickup time. So a member can give in two taps. "
        "Fixed scope. Fixed price. You own it."
    ),
    "ep4_clip08_morgan.mp3": (
        "And if you have been paying a fortune for a pretty homepage nobody can use, you already know the punchline. "
        "Come see us. theoffice360.com. Code STUDIO50. Fifty percent off the studio tiers. Email "
        "theofficetechies@gmail.com. Four people who actually build the thing. No junior freelancer maze."
    ),
    "ep4_clip09_alex.mp3": (
        "I love this show. Clean sites. Clean fuel. If you try Klear, start with strawberry watermelon, I'm just saying. "
        "If you need a site that respects your people, start with a conversation. We are not here to scare you into a "
        "retainer. We are here to hand you the keys. Go be light. Go be fast. That is the whole vibe."
    ),
    "ep4_clip10_morgan.mp3": (
        "Homework. Open your church or school site on your phone, with one thumb. If you get lost, call us. And if your "
        "protein still tastes like chalk, you know what to do. Klear. klearprotein.com. Code MARKETPL. Twenty percent off. "
        "I'm Morgan, he's Alex, this was The Office 360 Unfiltered, sponsored in part by Klear. We love you. Bye!"
    ),
}


def main() -> None:
    clips = []
    for fname, speaker, kind in CLIPS:
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
            t = end + 0.55
        else:
            t = end + e3.PAUSE
    total = t + e3.OUTRO_PAD
    n = int(total * SR)

    print(f"Building {total:.2f}s master @ {SR} Hz")
    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], axis=0)
    music = music[:n]

    duck_speech = e3.db(-24)
    duck_ad = e3.db(-13)
    duck_intro = e3.db(-6.5)
    duck_outro = e3.db(-7.5)
    regions = [(0, int(e3.INTRO_PAD * SR), duck_intro)]
    for ev in events:
        s = int(ev["start"] * SR)
        e = int(ev["end"] * SR)
        val = duck_ad if ev["kind"] == "ad" else duck_speech
        regions.append((s, e, val))
    regions.append((int(events[-1]["end"] * SR), n, duck_outro))
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

    wav_path = ROOT / "The_Office_360_Unfiltered_Episode_4.wav"
    mp3_path = ROOT / "The_Office_360_Unfiltered_Episode_4.mp3"
    sf.write(str(wav_path), mix, SR, subtype="PCM_16")
    sf.write(str(mp3_path), mix, SR, format="MP3")
    print("Wrote", wav_path, mp3_path, "dur", len(mix) / SR)

    dur_mm = int(total // 60)
    dur_ss = int(total % 60)

    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md_lines = [
        "# The Office 360 Unfiltered — Episode 4 Transcript",
        "",
        "**Title:** Faith, Schools & Publishing: Accessibility Done Right (sponsored by Klear)",
        f"**Duration:** {dur_mm:02d}:{dur_ss:02d}",
        "**Hosts:** Alex & Morgan",
        "**Sponsor:** Klear Juicy Protein — we earn a commission when you use our code.",
        "",
        "## Description / Show Notes",
        "",
        "Live show this week: Alex and Morgan tear into church, school, and publisher sites that look pretty and work like locked doors. Three-click discoverability, real mobile, real accessibility — the Office 360 way.",
        "",
        "This episode is sponsored by **Klear** (that's Klear with a K) — clear whey protein isolate that drinks like juice, not a chalky milkshake. 20g protein, 0 sugar, 0 lactose, ~90 calories. Mix 1 scoop with 12 oz water, shake, settle 1 minute.",
        "",
        "### Sponsor links & discount (use these — code is exclusive)",
        "",
        "- **20% OFF any Klear product** with code **MARKETPL**",
        "- Checkout link (code applied): https://klearprotein.com/discount/MARKETPL",
        "- Store: https://klearprotein.com",
        "- Flavors: Strawberry Watermelon · Wild Blue Raspberry",
        "- We earn a commission when you use our code. If you buy, you support the show.",
        "",
        "### Studio",
        "",
        "- https://the-office360.com",
        "- Promo **STUDIO50** — 50% off Turnkey Build / IA Roadmap / HTTPS Security",
        "- Inquiries: theofficetechies@gmail.com",
        "",
        "## High-intent SEO keywords",
        "",
        "`accessible church website`, `school portal UX`, `publisher website IA`, `3-click discoverability`, "
        "`The Office 360 Unfiltered`, `Klear protein`, `clear whey protein isolate`, `MARKETPL`, "
        "`lactose free protein`, `strawberry watermelon protein`",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        start, end = ev["start"], ev["end"]
        speaker = ev["speaker"]
        text = TEXTS[ev["file"]]
        vtt.append(f"{e3.ts_vtt(start)} --> {e3.ts_vtt(end)}")
        vtt.append(f"<v {speaker}>{text}")
        vtt.append("")
        srt_blocks.append(f"{i}\n{e3.ts(start)} --> {e3.ts(end)}\n{speaker}: {text}\n")
        mm, ss = divmod(int(start), 60)
        md_lines.append(f"**[{mm:02d}:{ss:02d}] {speaker}**")
        md_lines.append("")
        md_lines.append(text)
        md_lines.append("")

    (ROOT / "TRANSCRIPT_EPISODE_4.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / "TRANSCRIPT_EPISODE_4.srt").write_text("\n".join(srt_blocks), encoding="utf-8")
    (ROOT / "TRANSCRIPT_EPISODE_4.md").write_text("\n".join(md_lines), encoding="utf-8")

    show_notes = f"""# Episode 4 — Show Notes & Description

**The Office 360 Unfiltered — Ep 04**
Faith, Schools & Publishing: Accessibility Done Right
Sponsored by Klear Juicy Protein
Duration: {dur_mm}:{dur_ss:02d}

## Paste-ready podcast description

This week on The Office 360 Unfiltered, Alex and Morgan go live on the sites that actually serve people: churches, schools, and publishers. If Sunday service is four menus deep, the calendar takes eight taps, or grandma cannot find the donate button, that is not a design choice — it is a locked door with a pretty logo.

The Office 360's answer is three-click discoverability, real mobile, real contrast, and architecture you own. Four senior people. Lisbon to New York. Fixed scope. Fixed price.

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
    (ROOT / "EPISODE_4_SHOW_NOTES.md").write_text(show_notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <description>The no-BS podcast on bespoke web architecture, 3-click discoverability, CRM automation, and senior studio engineering.</description>
    <language>en-us</language>
    <itunes:author>The Office 360</itunes:author>
    <item>
      <title>Episode 4: Faith, Schools &amp; Publishing: Accessibility Done Right (sponsored by Klear)</title>
      <description>Alex and Morgan go live on church, school, and publisher sites that look pretty and work like locked doors. Sponsored by Klear — clear whey protein isolate. Exclusive 20% off with code MARKETPL at https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code. Studio: STUDIO50 at https://the-office360.com</description>
      <guid isPermaLink="false">office360-unfiltered-ep4</guid>
      <itunes:duration>{dur_mm}:{dur_ss:02d}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <link>https://klearprotein.com/discount/MARKETPL</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / "EPISODE_4_RSS.xml").write_text(rss, encoding="utf-8")
    print("Transcripts + RSS + show notes written")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")


if __name__ == "__main__":
    main()
