#!/usr/bin/env python3
"""Assemble Episode 7 of The Office 360 Unfiltered (4:00 minimum)."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
NUM = 7
TITLE = "The Contact Form Graveyard & The 3-Click Lead Machine"

CLIPS = [
    ("ep7_clip01_alex.mp3", "Alex", "cold"),
    ("ep7_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep7_clip03_alex.mp3", "Alex", "speech"),
    ("ep7_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep7_clip05_alex.mp3", "Alex", "speech"),
    ("ep7_clip06_morgan.mp3", "Morgan", "ad"),
    ("ep7_clip07_alex.mp3", "Alex", "ad"),
    ("ep7_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep7_clip09_alex.mp3", "Alex", "speech"),
    ("ep7_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep7_clip01_alex.mp3": (
        "Wooo we are live and I have a graveyard to show you. Welcome back to The Office 360 Unfiltered. "
        "I am Alex. Last week we talked about keys. Who owns the repo. Today is about the leads you already "
        "paid to get, and how they die in a contact form that emails nobody. Come on. If your site is pretty "
        "and your inbox is empty, this one is going to sting in a useful way."
    ),
    "ep7_clip02_morgan.mp3": (
        "Ha, I have the autopsy. I'm Morgan. Picture a gorgeous homepage. Video background. Forty-seven plugins. "
        "And the only door for a human being is a form that says send, and then it mails an intern who left in "
        "twenty twenty-three. No CRM. No follow up. No owner. Authors, schools, churches, you ran ads into that hole. "
        "That is not a marketing problem. That is architecture with a missing pipe."
    ),
    "ep7_clip03_alex.mp3": (
        "Exactly. At The Office 360 we obsess over three-click discoverability, and then we obsess over what happens "
        "after click three. Book. Event. Donate. The form cannot be a trap door. It has to land in a system with a name "
        "on it. A CRM. A sequence. A human who actually answers. Four seniors, Lisbon to New York. We do not ship a "
        "pretty funnel that dumps water on the floor."
    ),
    "ep7_clip04_morgan.mp3": (
        "And the funny-sad part is agencies love to sell you more traffic. More ads. More SEO retainers. Meanwhile the "
        "bucket has a hole. We audited a publisher who spent real money on a campaign and every lead sat in a spam folder "
        "named info at. No tags. No book title. No, hey, you asked about the hardcover. Just a graveyard. When we rebuild "
        "it, the form is short, the thank you is honest, and the lead is in the CRM before they close the tab."
    ),
    "ep7_clip05_alex.mp3": (
        "That is the whole product. Fixed scope. You own the code. You own the list. Automated so it does not depend on "
        "one intern's Gmail. If a visitor cannot hit the thing in three clicks, we failed. If they hit it and nobody answers, "
        "we also failed. Same standard as last week. If you cannot leave with your data, you do not own it. Don't rent your "
        "leads to a contact form."
    ),
    "ep7_clip06_morgan.mp3": (
        "And this is why this episode is sponsored by Klear. Klear with a K. Same joke. Don't swallow the heavy version "
        "that sits there and does nothing. Traditional protein is chalk and bloating. Klear is clear whey isolate. You can "
        "see it. Twenty grams of protein, zero sugar, zero lactose, about ninety calories. We earn a commission if you use "
        "our code. That keeps this live show on the air, and I would rather say that out loud."
    ),
    "ep7_clip07_alex.mp3": (
        "Two cities, long days, I am not dumping a milkshake into a form that goes nowhere. Strawberry watermelon. Wild blue "
        "raspberry. One scoop, twelve ounces of water, shake, let it settle a minute, drink it like a sports drink. Exclusive "
        "twenty percent off. Code MARKETPL. klearprotein.com/discount/MARKETPL. Use that link. Same rule as the CRM. Use the "
        "pipe that actually delivers."
    ),
    "ep7_clip08_morgan.mp3": (
        "Homework. Open your own site on your phone. Fill the form. See who gets the email. See if your name, your book, "
        "your event even shows up. If it dies, call us. theoffice360.com. Code STUDIO50. Fifty percent off the studio tiers. "
        "Email theofficetechies@gmail.com. Four people. You own the work. You own the list."
    ),
    "ep7_clip09_alex.mp3": (
        "Authors, schools, publishers, churches. Traffic is vanity if the door is a graveyard. We build the three-click path "
        "and we wire the follow through. No junior maze. No retainer to babysit a form. When the invoice is paid, the house "
        "is yours, and the leads are yours. Clean sites. Clean fuel. That is the whole vibe of this show."
    ),
    "ep7_clip10_morgan.mp3": (
        "If your protein still tastes like chalk, Klear, klearprotein.com, code MARKETPL, twenty percent off. If your contact "
        "form emails a ghost, you know where we live. I'm Morgan, he's Alex, this was The Office 360 Unfiltered, sponsored "
        "in part by Klear. We love you. Bye!"
    ),
}


def main() -> None:
    e3.RNG = np.random.default_rng(36007)
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
        raise SystemExit(f"under 4:00 ({total:.1f}s) — do not ship")
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
    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md = [
        f"# The Office 360 Unfiltered — Episode {NUM} Transcript",
        "",
        f"**Title:** {TITLE}",
        f"**Duration:** {dur_mm:02d}:{dur_ss:02d}",
        "**Hosts:** Alex & Morgan",
        "**Sponsor:** Klear Juicy Protein — we earn a commission when you use our code.",
        "",
        "## Description / Show Notes",
        "",
        "Pretty sites. Empty inboxes. Alex and Morgan autopsy the contact form that emails nobody, then rebuild "
        "the three-click path into a CRM you actually own. Sponsored by Klear.",
        "",
        "### Sponsor (exclusive listener discount)",
        "",
        "- **20% OFF** any Klear product with code **MARKETPL**",
        "- https://klearprotein.com/discount/MARKETPL",
        "- https://klearprotein.com",
        "- Flavors: Strawberry Watermelon · Wild Blue Raspberry",
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

    notes = f"""# Episode {NUM} — Show Notes & Description

**The Office 360 Unfiltered — Ep {NUM:02d}**
{TITLE}
Sponsored by Klear Juicy Protein
Duration: {dur_mm}:{dur_ss:02d}  (4:00 minimum)

## Paste-ready podcast description

Pretty homepage. Empty inbox. Alex and Morgan go live on the contact form graveyard — the send button that emails an intern who left in 2023, the ads you ran into a hole, the publisher leads sitting in a spam folder named info@. The Office 360 fix: three-click discoverability, then a CRM and follow-through you actually own. Four seniors. Lisbon to New York. Fixed scope. You own the list.

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
    (ROOT / f"EPISODE_{NUM}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <language>en-us</language>
    <item>
      <title>Episode {NUM}: {TITLE.replace('&', '&amp;')} (sponsored by Klear)</title>
      <description>The contact form graveyard vs a 3-click lead machine you own. Sponsored by Klear. 20% off code MARKETPL at https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code. Studio: STUDIO50 at https://the-office360.com</description>
      <guid isPermaLink="false">office360-unfiltered-ep{NUM}</guid>
      <itunes:duration>{dur_mm}:{dur_ss:02d}</itunes:duration>
      <link>https://klearprotein.com/discount/MARKETPL</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / f"EPISODE_{NUM}_RSS.xml").write_text(rss, encoding="utf-8")
    print("Wrote masters + transcripts")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")
    print("TOTAL", f"{dur_mm}:{dur_ss:02d}")


if __name__ == "__main__":
    main()
