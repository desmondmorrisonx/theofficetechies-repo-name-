#!/usr/bin/env python3
"""Assemble Episodes 11–12 — Wedding on Page 404 two-parter, no sponsor."""
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
        "num": 11,
        "title": "The Wedding on Page 404 — Part 1: Two Hundred Guests and a Copier",
        "short": "A mixed yarn, funny and heavy. A wedding, a 404 map, RSVPs trapped in a copier. Part 1 ends in the parking lot.",
        "seed": 36011,
        "clips": [
            ("ep11_clip01_alex.mp3", "Alex", "cold"),
            ("ep11_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep11_clip03_alex.mp3", "Alex", "speech"),
            ("ep11_clip04_morgan.mp3", "Morgan", "speech"),
            ("ep11_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep11_clip01_alex.mp3": (
                "Folks, pull up a chair. I have sat behind more microphones than I care to count, and I learned one thing "
                "the long way. The good shows do not shout. They tell you a story and let you see the room. Welcome back to "
                "The Office 360 Unfiltered. I am Alex. No sponsor in the chair tonight. Just a yarn. A true one. A wedding, "
                "a website, a 404 page, and two hundred people in their Sunday best staring at a parking lot. Stay with me. "
                "This is part one. If you subscribe, you get the ending next. That is how radio used to work, and that is how "
                "we are going to work, because I still believe a story should take its time. Download this. Sit with it. I am going to talk."
            ),
            "ep11_clip02_morgan.mp3": (
                "Ha, he is in full late-night mode and I am not stopping him. I'm Morgan. Picture a church. Good people. Real "
                "parking lot. They paid an agency for a pretty homepage. Video background. Forty-seven plugins. The couple fills "
                "out RSVP like adults. The form, folks, emails a fax-to-email address that rings in a copier room nobody has unlocked "
                "since last Advent. The agency is on retainer. They are clicking update plugins. They are not watching the wedding. "
                "Forty replies sit in a spam folder named info@. The calendar on the site says the wrong hall. The map link is a 404. "
                "I need you to hold that picture. Two hundred guests. Corsages. Aunts. A flower girl with a basket. And a webpage that shrugs."
            ),
            "ep11_clip03_alex.mp3": (
                "Now I have been on the air a long time, and I have heard every kind of disaster. Snowstorms. Lost records. A man "
                "who called in to propose and forgot the name. This one still gets me. Half the guests go to the old hall because "
                "Google cached a page the agency never redirected. Half go to the new hall because Uncle Ray got a text. The couple "
                "is in a vestibule doing math on a napkin. The pastor is a saint. The photographer is photographing a door. And somewhere "
                "a junior developer, who has never met this family, owns the password. Folks, that is not a cute tech oops. That is a "
                "wedding day with a lock on the door and a pretty logo on the lock. Stay with us. We do not leave you in the parking lot. "
                "That is next time. Subscribe so you are in the room."
            ),
            "ep11_clip04_morgan.mp3": (
                "If you are laughing, you are allowed. If you are wincing, you are also allowed. I'm Morgan. This is the mixed story. "
                "Funny because it is ridiculous. Heavy because it is somebody's actual Saturday. And this is why we built a mailbox. "
                "If you have a story like this, the invoice, the 404, the form that emailed a ghost, you send it. Subject: Story Time. "
                "theofficetechies@gmail.com. We will talk it on the air like this, with names stripped if you want cover. Shout-outs too. "
                "Your event, your book, your school night. Subject: Shout Out. We got you covered. No sponsor tonight. Just the station, "
                "and you. Listen. Download. Subscribe. Tell one aunt. Aunts move numbers."
            ),
            "ep11_clip05_alex.mp3": (
                "Part one ends in a parking lot, folks, because that is honest radio. I will not rush the ending to fit a banner. "
                "Next episode we walk into Monday morning, Lisbon and New York on the same Slack, and we talk about keys, three clicks, "
                "and how you do not let a wedding live on a retainer. If you want this kind of hour to keep existing, subject Donate, "
                "same inbox, theofficetechies@gmail.com. If you want to advertise like a human, subject Advertise. I'm Alex, she's Morgan, "
                "this was The Office 360 Unfiltered, part one of The Wedding on Page 404. Download it. Subscribe. Come back. We love you. "
                "We got you covered. Don't you go anywhere."
            ),
        },
        "keywords": (
            "The Office 360 Unfiltered, Wedding on Page 404, church website disaster, RSVP form failure, "
            "404 map wedding, radio storytelling podcast, listen download subscribe, Story Time, "
            "podcast shout out, donate to podcast, theofficetechies@gmail.com, Lisbon New York studio, "
            "agency retainer horror story, three-click discoverability, STUDIO50"
        ),
        "hashtags": "#Office360 #WeddingOnPage404 #Part1 #StoryTime #ChurchWebsite #PodcastSubscribe #ShoutOut",
    },
    {
        "num": 12,
        "title": "The Wedding on Page 404 — Part 2: Monday, the Keys, and the Aunts",
        "short": "Part 2. Monday morning. We get the keys. Three clicks. The couple still gets married. Then the mailbox.",
        "seed": 36012,
        "clips": [
            ("ep12_clip01_alex.mp3", "Alex", "cold"),
            ("ep12_clip02_morgan.mp3", "Morgan", "speech"),
            ("ep12_clip03_alex.mp3", "Alex", "speech"),
            ("ep12_clip04_morgan.mp3", "Morgan", "speech"),
            ("ep12_clip05_alex.mp3", "Alex", "outro"),
        ],
        "texts": {
            "ep12_clip01_alex.mp3": (
                "Folks, we left two hundred people in a parking lot, and I am not the kind of host who goes to commercial and forgets them. "
                "Welcome back to The Office 360 Unfiltered. I am Alex. This is part two. The Wedding on Page 404. No sponsor in the chair. "
                "Just the rest of the yarn, and then the mailbox. Monday morning. Lisbon is making coffee. New York is still in yesterday. "
                "The church admin writes us in language I have heard for decades. We have a problem. The site looks fine. The people are not "
                "fine. That is the call you want, if you do this work with a conscience. Sit down. I am going to talk you through the morning "
                "like I was on the board in sixty-five, except the board is Slack, and the record is a Git repo they did not own."
            ),
            "ep12_clip02_morgan.mp3": (
                "Ha, and I have the email. I'm Morgan. Subject line in all caps. The map is broken. The RSVP is a ghost. The date on the "
                "homepage is last year's Christmas pageant. We get on with the admin. No junior maze. No, please open a ticket. Four seniors. "
                "You talk to the people who write the code. First question Alex always asks, and I love him for it. Who has the keys. Domain. "
                "Host. Repo. They do not. The agency does. Of course they do. So we do the unglamorous radio work. We get the keys. We do not "
                "make a speech. We make a page a grandmother can find in three taps. Event. Time. Map that is a map. Form that lands in a human "
                "inbox with a name on it. Not a copier. A human."
            ),
            "ep12_clip03_alex.mp3": (
                "Here is the funny part, and I have waited a whole episode to give it to you. The couple still got married. The aunts still cried. "
                "Uncle Ray still gave a toast that ran long. The website did not get to keep the day. We rebuilt the thing so the next wedding is "
                "not a scavenger hunt. Fixed scope. They own every line. When the invoice is paid, the house is theirs. I have been telling versions "
                "of that story my whole career, folks. Different props. Same moral. Don't rent the door to your own party. If you are an author, a "
                "school, a church, a publisher, and your pretty page is a parking lot, you already know the ending. Call us before the corsages. "
                "theoffice360.com. Code STUDIO50 if you need the studio. But first, stay human. Subscribe. Download. Let this story travel."
            ),
            "ep12_clip04_morgan.mp3": (
                "Mailbox is open, and I will say it slow so the back row gets it. I'm Morgan. Story Time. Your yarn, your invoice, your win. "
                "Subject: Story Time. Shout Out. Your event, we got you covered. Subject: Shout Out. Advertise. If you want to sit in this room "
                "with our founding listeners without lying about a million downloads, subject: Advertise. Donate. If this two-parter made you laugh "
                "and then go quiet, chip in so the next hour exists. Subject: Donate. All of it, theofficetechies@gmail.com. Listen all the way through. "
                "Download the file. Subscribe so part three of your own life might end up on this mic. We are not a hallway. We are a show."
            ),
            "ep12_clip05_alex.mp3": (
                "That is the hour, folks. Two hundred guests, one 404, a copier full of RSVPs, and a Monday that put the keys back in the church's "
                "pocket. I have loved radio my whole life because it lets a story breathe. Thank you for letting this one breathe. I'm Alex, she's Morgan, "
                "this was The Office 360 Unfiltered, part two of The Wedding on Page 404. No sponsor. Our mailbox. Our hat in our hands. Email us. "
                "Subscribe. Tell one human, preferably an aunt. We love you. We got you covered. Good night."
            ),
        },
        "keywords": (
            "The Office 360 Unfiltered, Wedding on Page 404 part 2, church website rebuild, website code ownership, "
            "three-click event page, RSVP to CRM, Lisbon New York web studio, radio storytelling, "
            "podcast donations, advertise on The Office 360 Unfiltered, Story Time mailbag, event shout out, "
            "theofficetechies@gmail.com, STUDIO50, listen download subscribe"
        ),
        "hashtags": "#Office360 #WeddingOnPage404 #Part2 #StoryTime #Donate #ShoutOut #PodcastAds #STUDIO50",
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
        "**Sponsor:** None",
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
**Hosts:** Alex (lead, veteran radio) & Morgan (co-host)
**Sponsor:** None
**Artwork:** episode_{num}_artwork.png
**Type:** Two-part mixed story (funny / human)

## Listener CTAs
Email **theofficetechies@gmail.com**

| Door | Subject |
|---|---|
| Donate so the next hour exists | `Donate` |
| Event shout-out — we got you covered | `Shout Out` |
| Advertise like a human | `Advertise` |
| Your yarn on the air | `Story Time` |

Boost: listen · download · subscribe · tell one aunt

## Studio
- https://the-office360.com
- Code **STUDIO50**
- theofficetechies@gmail.com

## Paste-ready podcast description
{ep['title']}

{ep['short']}

No outside sponsor. Alex tells it like a late-night board op. Morgan keeps the picture honest. Then the mailbox: Donate, Shout Out, Advertise, Story Time — theofficetechies@gmail.com

Studio: https://the-office360.com · STUDIO50

## Episode keywords
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
      <description>{ep['short'].replace('&', '&amp;')} Email theofficetechies@gmail.com — Donate, Shout Out, Advertise, Story Time. No outside sponsor.</description>
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
