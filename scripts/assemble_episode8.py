#!/usr/bin/env python3
"""Assemble Episode 8 — Founding 20 listener appreciation."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
NUM = 8
TITLE = "20 Downloads Worldwide: The Founding Circle, Story Time & Your Shout-Out (Sponsored by Klear)"
SHORT = "Thank you, founding twenty. Listen, download, subscribe — then email us a story, an event, or an ad."

CLIPS = [
    ("ep8_clip01_alex.mp3", "Alex", "cold"),
    ("ep8_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep8_clip03_alex.mp3", "Alex", "speech"),
    ("ep8_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep8_clip05_alex.mp3", "Alex", "speech"),
    ("ep8_clip06_morgan.mp3", "Morgan", "speech"),
    ("ep8_clip07_alex.mp3", "Alex", "ad"),
    ("ep8_clip08_morgan.mp3", "Morgan", "ad"),
    ("ep8_clip09_alex.mp3", "Alex", "speech"),
    ("ep8_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep8_clip01_alex.mp3": (
        "Wooo we are live, and I am not going to pretend we just sold out Madison Square Garden. "
        "Welcome back to The Office 360 Unfiltered. I am Alex. We hit twenty downloads. Twenty. All over "
        "the world. And on this show we tell the truth, so here it is. Twenty humans actually pressed play. "
        "That is not nothing. That is a founding circle. Today the episode is for you, and I am grinning like "
        "it is a world tour in twenty living rooms."
    ),
    "ep8_clip02_morgan.mp3": (
        "Ha, he is treating twenty like a stadium and I am here for it. I'm Morgan. Twenty downloads means "
        "twenty rooms. Maybe Lisbon. Maybe New York. Maybe Lagos. Maybe a church office with the calendar still "
        "broken. Maybe an author who is done with the retainer. You found us. You stayed. That is how a four "
        "person studio builds an audience. Not with a fake million. With you. Thank you. We see you."
    ),
    "ep8_clip03_alex.mp3": (
        "If you want this thing to live, here is the unsexy ask, and I will say it with joy. Listen. Download. "
        "Subscribe. Follow wherever you get the show. The algorithm is a snob. It does not care that we are funny. "
        "It cares that you hit download, that you subscribe so the next episode is waiting, that you do not stream "
        "us once and vanish. Be one of the twenty who brought a friend. That is the whole growth plan. No billboard. You."
    ),
    "ep8_clip04_morgan.mp3": (
        "New segment, and this is the fun one. Story Time with The Office. You email us a story. The bad invoice. "
        "The site that buried Sunday service under four menus. The contact form that emailed a ghost. The win, even. "
        "The rebuild that finally worked. We will read it, we will talk it, we will put it on the next segment. Keep "
        "your name if you want credit. Strip it if you want cover. Send it to theofficetechies@gmail.com. Subject line: "
        "Story Time. We got you."
    ),
    "ep8_clip05_alex.mp3": (
        "And shout-outs. You have an event? Book launch. School open house. Church conference. Publisher fair. Product "
        "drop. A Friday night thing in your city. You email us, we say it on the air. We got you covered. This is a live "
        "show with twenty citizens of the world and we can still make a room feel big. Hit theofficetechies@gmail.com. "
        "Subject: Shout Out. Tell us the what, the when, the where, and who should show up. We will say it like we mean it."
    ),
    "ep8_clip06_morgan.mp3": (
        "If you want to advertise on this show, that door is open too. We are not going to pretend we have a Super Bowl "
        "slot. We have a founding audience that actually listens, and we talk like humans. Brands, studios, schools, authors, "
        "if you want a promotion on The Office 360 Unfiltered, email theofficetechies@gmail.com. Subject: Advertise. We will "
        "talk like people, not like a media kit that lies about numbers. Hit us up. Let's make something that does not sound "
        "like a hostage ad."
    ),
    "ep8_clip07_alex.mp3": (
        "This episode is still sponsored by Klear, Klear with a K, because the founding twenty deserve the truth in the "
        "shaker too. Clear whey, drinks like juice. Twenty grams of protein, zero sugar, zero lactose. We earn a commission "
        "if you use our code. That is how a twenty-download show stays on the air without selling you a hallway. Strawberry "
        "watermelon. Wild blue raspberry. One scoop, twelve ounces of water, shake, settle, go."
    ),
    "ep8_clip08_morgan.mp3": (
        "Code MARKETPL. Twenty percent off. klearprotein.com/discount/MARKETPL. Use that link. And if you need a site, "
        "theoffice360.com, code STUDIO50. But hear me. Today is not a pitch first. Today is thank you first. Listen. "
        "Download. Subscribe. Email us a story, an event, an ad. theofficetechies@gmail.com. We actually read it."
    ),
    "ep8_clip09_alex.mp3": (
        "I mean it. Twenty downloads all over the world is a small number with a loud heart. We are four people between "
        "Lisbon and New York. You found the unfiltered version. Subscribe so we can do Story Time next week with your name "
        "in the room. Download so the next person gets handed this show. Tell one human. That is how twenty becomes forty "
        "becomes a crowd that still feels like a room. We will not fake a million. We will earn the twenty-first."
    ),
    "ep8_clip10_morgan.mp3": (
        "Thank you, founding twenty. Email us. Story Time. Shout Out. Advertise. theofficetechies@gmail.com. Listen, "
        "download, subscribe, wherever this found you. I'm Morgan, he's Alex, this was The Office 360 Unfiltered, "
        "sponsored in part by Klear. We love you. We got you covered. Bye!"
    ),
}

KEYWORDS = (
    "The Office 360 Unfiltered, 20 downloads worldwide, listener appreciation podcast, subscribe download listen, "
    "Story Time with The Office, podcast shout out, podcast advertising, advertise on The Office 360 Unfiltered, "
    "theofficetechies@gmail.com, Lisbon New York podcast, 4-person web studio, founding circle, "
    "Klear protein, Klear juicy protein, MARKETPL, klearprotein.com, STUDIO50, the-office360.com, "
    "clear whey protein isolate, strawberry watermelon protein, event shout out podcast, book launch shout out"
)


def main() -> None:
    e3.RNG = np.random.default_rng(36008)
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
**Type:** Listener appreciation / community episode (unique)

## Listener CTAs
- **Listen, download, subscribe** wherever you get the show
- **Story Time with The Office** — email a story for the next segment  
  Subject: `Story Time` → theofficetechies@gmail.com
- **Event shout-outs** — book launches, school nights, church conferences, fairs  
  Subject: `Shout Out` → theofficetechies@gmail.com  
  Include: what / when / where / who should show up
- **Advertise on the show** — brands, studios, schools, authors  
  Subject: `Advertise` → theofficetechies@gmail.com

## Sponsor
**Klear Juicy Protein** (Klear with a K) — this episode is sponsored by Klear.
- 20g clear whey protein isolate · 0 sugar · 0 lactose · ~90 calories
- Flavors: Strawberry Watermelon · Wild Blue Raspberry
- Exclusive listener discount: **20% OFF** code **MARKETPL**
- Link: https://klearprotein.com/discount/MARKETPL
- Store: https://klearprotein.com
- FTC: We earn a commission when you use our code. If you buy, you support the show.

## Studio CTA
- https://the-office360.com
- Code **STUDIO50** — 50% off Turnkey Build / IA Roadmap / HTTPS Security
- theofficetechies@gmail.com

## Paste-ready podcast description
{TITLE}

We hit 20 downloads — all over the world. Not a fake million. A founding circle. Alex and Morgan say thank you, then open the doors: listen, download, subscribe; email Story Time for the next segment; send your event for a shout-out (we got you covered); hit us up to advertise like humans, not a media kit.

Email: theofficetechies@gmail.com
Subjects: Story Time · Shout Out · Advertise

Sponsored by Klear Juicy Protein. Exclusive 20% off with code MARKETPL: https://klearprotein.com/discount/MARKETPL
We earn a commission when you use our code.

Studio: https://the-office360.com · STUDIO50

## Episode keywords (SEO / RSS / YouTube / Apple tags)
{KEYWORDS}

## Hashtags
#Office360 #TheOffice360Unfiltered #Founding20 #PodcastSubscribe #StoryTime #ShoutOut #PodcastAdvertising #KlearProtein #MARKETPL #STUDIO50
"""
    (ROOT / f"EPISODE_{NUM}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <language>en-us</language>
    <itunes:keywords>{KEYWORDS}</itunes:keywords>
    <item>
      <title>{TITLE.replace('&', '&amp;')}</title>
      <description>{SHORT.replace('&', '&amp;')} Email theofficetechies@gmail.com with subject Story Time, Shout Out, or Advertise. Sponsored by Klear. Code MARKETPL at https://klearprotein.com/discount/MARKETPL — we earn a commission when you use our code.</description>
      <guid isPermaLink="false">office360-unfiltered-ep{NUM}</guid>
      <itunes:duration>{duration}</itunes:duration>
      <itunes:keywords>{KEYWORDS}</itunes:keywords>
      <link>https://the-office360.com</link>
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
