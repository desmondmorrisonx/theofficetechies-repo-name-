#!/usr/bin/env python3
"""Assemble Episode 6 (4+ min recut) of The Office 360 Unfiltered."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
NUM = 6
TITLE = "You Own Every Line: Why Agencies Keep the Keys"

CLIPS = [
    ("ep6v2_clip01_alex.mp3", "Alex", "cold"),
    ("ep6v2_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep6v2_clip03_alex.mp3", "Alex", "speech"),
    ("ep6v2_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep6v2_clip05_alex.mp3", "Alex", "speech"),
    ("ep6v2_clip06_morgan.mp3", "Morgan", "ad"),
    ("ep6v2_clip07_alex.mp3", "Alex", "ad"),
    ("ep6v2_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep6v2_clip09_alex.mp3", "Alex", "speech"),
    ("ep6v2_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep6v2_clip01_alex.mp3": (
        "Wooo we are live and I brought a pet peeve that has been living in my chest since Lisbon. "
        "Welcome back to The Office 360 Unfiltered. I am Alex. Today is about keys. Who holds them. "
        "Agencies love to build your pretty site and then keep the repo, the fonts, the Figma, the domain "
        "logins, the whole house. You paid for a home. You got a lease with a smile on it. Come on. Come on!"
    ),
    "ep6v2_clip02_morgan.mp3": (
        "Ha, I have seen the email. I have the screenshots. Sorry, we cannot export that, it is in our "
        "proprietary theme. Sorry, the designer owns the Figma. Sorry, hosting is in our account and the "
        "password is a secret. We can make the change next sprint. That is not partnership. That is a hostage "
        "note with a status meeting attached. At The Office 360 you own every line of code. Every asset. Period. "
        "No cute exceptions."
    ),
    "ep6v2_clip03_alex.mp3": (
        "Let me translate that into boring, beautiful truth. Ownership means the Git repo is in your organization. "
        "The domain is in your registrar. The DNS is in your account. The design files are in your Drive. The CMS, "
        "the keys, the analytics. When we are done, you could fire us tomorrow and the site still belongs to you. "
        "That is the test. If you cannot leave, you do not own it. You are renting a smile."
    ),
    "ep6v2_clip04_morgan.mp3": (
        "And it gets funnier, in the sad way. A publisher we audited could not change a book cover without opening "
        "a ticket. A church could not update Sunday time because the special theme broke if anyone but the agency "
        "touched it. A school calendar was locked behind a plugin license that expired, and the agency wanted a "
        "retainer to renew it. You already paid to build the thing. Now you pay to knock on your own door."
    ),
    "ep6v2_clip05_alex.mp3": (
        "Four seniors. Lisbon to New York. We hand you the keys because we do not make money trapping you. "
        "Fixed scope. Fixed price. You know the number before we write a line. Automated QA so we are not babysitting. "
        "No junior maze. No proprietary lock. When the invoice is paid, the house is yours. That is not a slogan. "
        "That is the contract. And if a fifty person deck impressed you while they kept the passwords, you already "
        "know how this story ends."
    ),
    "ep6v2_clip06_morgan.mp3": (
        "And look, this is the same joke in a bottle, which is why this episode is sponsored by Klear. Klear with a K. "
        "Traditional protein is thick and secret and sits in your stomach like a proprietary theme. Klear is clear whey "
        "isolate. You can literally see it. Twenty grams of protein, zero sugar, zero lactose, about ninety calories. "
        "We earn a commission if you use our code. That keeps this live show on the air, and I would rather tell you "
        "that than hide it."
    ),
    "ep6v2_clip07_alex.mp3": (
        "Two cities, long days, I am not slamming gym sludge between calls. Strawberry watermelon is the one. Wild blue "
        "raspberry if you want the tang. One scoop, twelve ounces of water, shake it, let it settle a minute, drink it "
        "like a sports drink. Exclusive twenty percent off, code MARKETPL. klearprotein.com/discount/MARKETPL. Use that "
        "link, not a random one. Same rule as the repo. Use the keys that are actually yours."
    ),
    "ep6v2_clip08_morgan.mp3": (
        "Homework, and I want you to actually do it. Email your current shop today. Ask for the repo. Ask for the design "
        "files. Ask for the domain logins, the host, the analytics. If they stall, if they say it is complicated, if they "
        "say you need a retainer first, you already have your answer. Then call us. theoffice360.com. Code STUDIO50. "
        "Fifty percent off the studio tiers. Email theofficetechies@gmail.com. Four people. You own the work."
    ),
    "ep6v2_clip09_alex.mp3": (
        "I love this show because it is the same philosophy twice. Don't rent your stack. Don't rent your fuel. Don't "
        "swallow the heavy version just because the industry printed a brochure. Authors, schools, publishers, churches, "
        "if your site needs a priest and a project manager every Sunday, it is not your people. It is the lock on the door. "
        "We build so a parent on a bus can find pickup time. So a member can give in two taps. Then we hand you the keys "
        "and we get out of the hallway."
    ),
    "ep6v2_clip10_morgan.mp3": (
        "Own the site. Own the fuel. If your protein still tastes like chalk, Klear, klearprotein.com, code MARKETPL, "
        "twenty percent off. If your homepage is pretty and nobody can use it, you know where we live. I'm Morgan, "
        "he's Alex, this was The Office 360 Unfiltered, sponsored in part by Klear. We love you. Bye!"
    ),
}


def main() -> None:
    e3.RNG = np.random.default_rng(36006)
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
        extra = 240 - total + 0.5
        total += extra
        print("WARNING padded to 4:00 by", extra)
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
        "Alex and Morgan go after agency lock-in: proprietary themes, hidden repos, passwords you don't get. "
        "The Office 360 hands you every line of code. Sponsored by Klear.",
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

Alex and Morgan go live on agency lock-in. You paid for a home. You got a lease. Proprietary themes, hidden Git repos, Figma files you cannot export, domain logins that live in someone else's account. The Office 360 is four seniors, Lisbon to New York: when the invoice is paid, you own every line of code.

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
      <title>Episode {NUM}: {TITLE} (sponsored by Klear)</title>
      <description>Agency lock-in vs real ownership. Sponsored by Klear. 20% off code MARKETPL at https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code. Studio: STUDIO50 at https://the-office360.com</description>
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
