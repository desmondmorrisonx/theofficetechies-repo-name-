#!/usr/bin/env python3
"""Assemble Episodes 9 and 10 — no sponsor; shout-outs, ads, donations."""
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
MIN_DUR = 240.0

EPISODES = [
    {
        "num": 9,
        "title": "Pass the Mic: Listen, Subscribe, Donate, and Grow This Show",
        "short": "No sponsor in the chair. Listen, download, subscribe — then shout-out, advertise, or donate.",
        "seed": 36009,
        "clips": [
            ("ep9_clip01_alex.mp3", "Alex", "cold"),
            ("ep9_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep9_clip03_alex.mp3", "Alex", "speech"),
            ("ep9_clip04_morgan.mp3", "Morgan", "speech"),
            ("ep9_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep9_clip01_alex.mp3": (
                "Wooo we are live, and look at the rundown. No sponsor in the chair today. This hour is ours. "
                "Welcome back to The Office 360 Unfiltered. I am Alex. We told you we hit twenty downloads all over "
                "the world. We meant it. We did not inflate it. Today is not another roast of a WordPress retainer. "
                "Today is the growth episode. How you help this show live. Listen. Download. Subscribe. Send a shout-out. "
                "Book an ad. And if you have a few dollars and you believe four seniors in Lisbon and New York should keep "
                "telling the truth on a microphone, there is a donation door too. I am grinning because this is the "
                "unfiltered version of asking. No fake million. No crying violin. Just a room that wants a twenty-first "
                "listener, and a show that wants to stay on the air without selling you a hallway."
            ),
            "ep9_clip02_morgan.mp3": (
                "Ha, and I will not do the sad podcast voice. I'm Morgan. Here is how you boost us for real. Press play "
                "all the way through. Download the file, do not just stream and bounce. Subscribe on Apple, Spotify, YouTube, "
                "wherever this found you, so the next episode is waiting in the morning. Tell one human. One. Forward it to "
                "the church admin with the broken calendar. Forward it to the author who is still on a retainer. The algorithm "
                "is a snob. It counts downloads and subscribers, not how clever we were about Jamstack. If you already love "
                "this show, that is the whole job. Be loud in a small way. That is how twenty becomes a crowd that still feels "
                "like a room. We see you. We are asking you to bring a chair for somebody else."
            ),
            "ep9_clip03_alex.mp3": (
                "Donations. I am going to say the word like a grown-up. If this show has saved you from a bad invoice, or "
                "made you laugh, or handed you a sentence you forwarded, you can chip in so we can keep recording between "
                "Lisbon and New York. We are four people. Time is the real bill. Hosting is a bill. This is not a guilt jar. "
                "This is a keep-the-lights-on jar. Email theofficetechies@gmail.com. Subject line: Donate. Tell us you want "
                "to help the podcast grow. We will write you back like humans. No fake foundation. No mystery thermometer. "
                "You are funding unfiltered hours, not a fifty person hallway."
            ),
            "ep9_clip04_morgan.mp3": (
                "And the other doors stay open, because a show is a room. Shout-outs. You have an event, a book launch, a "
                "school night, a church conference, a Friday thing in your city? Email theofficetechies@gmail.com. Subject: "
                "Shout Out. What, when, where, who should show up. We got you covered. We will say it on the air like we mean "
                "it. Advertise. Brands, studios, authors, schools, if you want to talk to this founding circle without sounding "
                "like a hostage ad, subject line: Advertise. Same inbox. We will not lie about our numbers. Twenty downloads "
                "worldwide was the truth. The next truth is we are building, and there is a chair for a partner who talks like a person."
            ),
            "ep9_clip05_alex.mp3": (
                "So here is the whole card, one more time, with joy. Listen. Download. Subscribe. Tell one human. If you want "
                "to fund the next hour, subject Donate. If you want a shout-out, subject Shout Out. If you want to advertise, "
                "subject Advertise. All of it to theofficetechies@gmail.com. Studio is still theoffice360.com, code STUDIO50, "
                "if you need a site. But this episode is not a pitch first. This episode is a pass-the-mic. I'm Alex, she's Morgan, "
                "this was The Office 360 Unfiltered. No sponsor in the chair. Just us, and you. We love you. We got you covered. Bye!"
            ),
        },
        "keywords": (
            "The Office 360 Unfiltered, grow the podcast, listen download subscribe, podcast donations, "
            "donate to The Office 360 Unfiltered, podcast shout out, advertise on The Office 360 Unfiltered, "
            "theofficetechies@gmail.com, Lisbon New York podcast, 4-person web studio, STUDIO50, "
            "the-office360.com, founding listeners, Apple Podcasts subscribe, Spotify subscribe"
        ),
        "hashtags": "#Office360 #TheOffice360Unfiltered #PassTheMic #PodcastSubscribe #PodcastDonation #ShoutOut #PodcastAds #STUDIO50",
    },
    {
        "num": 10,
        "title": "Story Time Mailbag: Your Shout-Out, Your Event, Your Ad",
        "short": "The mailbox episode. Story Time, event shout-outs, advertise, donate — one inbox.",
        "seed": 36010,
        "clips": [
            ("ep10_clip01_alex.mp3", "Alex", "cold"),
            ("ep10_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep10_clip03_alex.mp3", "Alex", "speech"),
            ("ep10_clip04_morgan.mp3", "Morgan", "speech"),
            ("ep10_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep10_clip01_alex.mp3": (
                "We are live, and today the mailbox is the star. Welcome back to The Office 360 Unfiltered. I am Alex. "
                "No sponsor again. This one is Story Time, shout-outs, and the honest advertisement door. If you have been "
                "waiting for permission to write us, this is the permission. theofficetechies@gmail.com. We actually read it. "
                "We will talk your story on the next segment. We will shout your event. We will talk ads like humans. And if "
                "you want this mailbag to keep existing, listen, download, subscribe, and if you can, donate. I am fired up "
                "because a twenty-download show with a real mailbox is more interesting than a million-download show with a fake laugh track."
            ),
            "ep10_clip02_morgan.mp3": (
                "Ha, Story Time with The Office, let's make it easy. I'm Morgan. You email a story. The bad invoice. The site "
                "that buried Sunday service under four menus. The contact form that emailed a ghost. The win. The rebuild. Keep "
                "your name if you want credit. Strip it if you want cover. Subject line: Story Time. That is the whole form. We "
                "will not turn you into a case study deck. We will talk it on the air, like two people at a table. If you are shy, "
                "say shy in the first line. If you want a shout-out mixed in, say that too. We got you. This is the segment that "
                "makes the founding circle feel like a room and not a metric."
            ),
            "ep10_clip03_alex.mp3": (
                "Events. I want your messy real calendar. Book launch. School open house. Church conference. Publisher fair. "
                "Product drop. A reading in a library that holds twelve people. Email theofficetechies@gmail.com, subject Shout Out. "
                "Give me the what, the when, the where, and who should walk in the door. We will say it on this show. We got you "
                "covered. We are not a billboard company. We are a live mic in two cities that will read your event like it matters, "
                "because to you it does. That is the whole product. A shout-out that does not sound like it was generated by an intern "
                "who left in 2023."
            ),
            "ep10_clip04_morgan.mp3": (
                "Advertise, and donate, because I will not hide either door. If you want to run a promotion on The Office 360 "
                "Unfiltered, subject Advertise, same inbox. We will not sell you a vanity number. We will sell you a room of people "
                "who actually finish episodes. Authors, schools, studios, tools, if your thing is real, let's talk. And if you are "
                "a listener who just wants the show to survive, subject Donate. Chip in. You are not buying a gold plaque. You are "
                "buying another unfiltered hour. theofficetechies@gmail.com. Listen. Download. Subscribe. Then, if you can, fund it. "
                "That is how a small show stays honest."
            ),
            "ep10_clip05_alex.mp3": (
                "Write us tonight. Story Time. Shout Out. Advertise. Donate. Four subject lines, one inbox, "
                "theofficetechies@gmail.com. Subscribe so you do not miss the episode where we read your name. Download so the "
                "algorithm stops being a snob. Tell one human. I'm Alex, she's Morgan, this was The Office 360 Unfiltered. "
                "No sponsor. Our mailbox, our shout-outs, our hat in our hands. We love you. We got you covered. Bye!"
            ),
        },
        "keywords": (
            "The Office 360 Unfiltered, Story Time with The Office, podcast mailbag, event shout out, "
            "book launch shout out, church conference shout out, podcast advertising, donate to podcast, "
            "theofficetechies@gmail.com, listen download subscribe, Lisbon New York podcast, STUDIO50, "
            "the-office360.com, founding circle mailbag"
        ),
        "hashtags": "#Office360 #StoryTime #ShoutOut #PodcastAds #PodcastDonation #Mailbag #STUDIO50",
    },
]


def assemble(ep: dict) -> None:
    e3.RNG = np.random.default_rng(ep["seed"])
    clips = []
    for fname, speaker, kind in ep["clips"]:
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
        t = end if i == len(clips) - 1 else end + e3.PAUSE
    outro = e3.OUTRO_PAD
    total = t + outro
    if total < MIN_DUR:
        outro += MIN_DUR - total
        total = t + outro
        print(f"EP{ep['num']} extended outro to {outro:.1f}s to hit 4:00")
    n = int(total * SR)
    print(f"EP{ep['num']} Building {total:.2f}s ({int(total//60)}:{int(total%60):02d})")

    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], axis=0)
    music = music[:n]

    duck_speech = e3.db(-24)
    regions = [(0, int(e3.INTRO_PAD * SR), e3.db(-6.5))]
    for ev in events:
        regions.append((int(ev["start"] * SR), int(ev["end"] * SR), duck_speech))
    regions.append((int(events[-1]["end"] * SR), n, e3.db(-7.0)))
    g = e3.smooth_gain_curve(n, regions, duck_speech)
    music = music * g[:, None]
    music *= e3.fade(n, int(0.25 * SR), int(min(3.8 * SR, n // 8)))[:, None]

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
    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{num}.wav"), mix, SR, subtype="PCM_16")
    sf.write(str(ROOT / f"The_Office_360_Unfiltered_Episode_{num}.mp3"), mix, SR, format="MP3")

    dur_mm, dur_ss = int(total // 60), int(total % 60)
    duration = f"{dur_mm}:{dur_ss:02d}"

    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md = [
        f"# The Office 360 Unfiltered — Episode {num} Transcript",
        "",
        f"**Title:** {ep['title']}",
        f"**Duration:** {dur_mm:02d}:{dur_ss:02d}",
        "**Hosts:** Alex & Morgan",
        "**Sponsor:** None — listener-supported / shout-outs / house ads",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        text = ep["texts"][ev["file"]]
        vtt.append(f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}")
        vtt.append(f"<v {ev['speaker']}>{text}")
        vtt.append("")
        srt_blocks.append(f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n")
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]

    (ROOT / f"TRANSCRIPT_EPISODE_{num}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{num}.srt").write_text("\n".join(srt_blocks), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{num}.md").write_text("\n".join(md), encoding="utf-8")

    notes = f"""# EPISODE NOTES — Ep {num:02d}

**Show:** The Office 360 Unfiltered
**Episode:** {num:02d}
**Title:** {ep['title']}
**Short title:** {ep['short']}
**Duration:** {duration} (4:00 minimum)
**Hosts:** Alex (lead) & Morgan (co-host)
**Sponsor:** None
**Artwork:** episode_{num}_artwork.png

## Listener CTAs (house only)
Email **theofficetechies@gmail.com**

| Door | Subject line |
|---|---|
| Chip in so the show grows | `Donate` |
| Event / launch shout-out (we got you covered) | `Shout Out` |
| Advertise on the show | `Advertise` |
| Story for the next segment | `Story Time` |

Boost: **listen · download · subscribe · tell one human**

## Studio
- https://the-office360.com
- Code **STUDIO50** — 50% off studio tiers
- theofficetechies@gmail.com

## Paste-ready podcast description
{ep['title']}

{ep['short']}

No outside sponsor this week. Alex and Morgan pass the mic: listen, download, subscribe, then email theofficetechies@gmail.com with subject Donate, Shout Out, Advertise, or Story Time.

Studio: https://the-office360.com · STUDIO50

## Episode keywords (SEO / RSS / YouTube / Apple tags)
{ep['keywords']}

## Hashtags
{ep['hashtags']}
"""
    (ROOT / f"EPISODE_{num}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <language>en-us</language>
    <itunes:keywords>{ep['keywords']}</itunes:keywords>
    <item>
      <title>{ep['title'].replace('&', '&amp;')}</title>
      <description>{ep['short'].replace('&', '&amp;')} Email theofficetechies@gmail.com with subject Donate, Shout Out, Advertise, or Story Time. No outside sponsor.</description>
      <guid isPermaLink="false">office360-unfiltered-ep{num}</guid>
      <itunes:duration>{duration}</itunes:duration>
      <itunes:keywords>{ep['keywords']}</itunes:keywords>
      <link>https://the-office360.com</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / f"EPISODE_{num}_RSS.xml").write_text(rss, encoding="utf-8")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")
    print("TOTAL", duration)


if __name__ == "__main__":
    for ep in EPISODES:
        assemble(ep)
    print("done")
