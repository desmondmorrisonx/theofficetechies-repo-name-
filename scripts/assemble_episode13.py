#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

import assemble_episode3 as e3
import numpy as np
import soundfile as sf

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"
SR = e3.SR
NUM = 13
MIN_DUR = 600.0  # 10:00
TITLE = "The Fanfic That Ate the Bestseller List: Snowqueen Icedragon, Fifty Shades, and the Hidden Buy Button"

CLIPS = [
    ("ep13_clip01_alex.mp3", "Alex", "cold"),
    ("ep13_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep13_clip03_alex.mp3", "Alex", "speech"),
    ("ep13_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep13_clip05_alex.mp3", "Alex", "speech"),
    ("ep13_clip06_morgan.mp3", "Morgan", "speech"),
    ("ep13_clip07_alex.mp3", "Alex", "speech"),
    ("ep13_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep13_clip09_alex.mp3", "Alex", "speech"),
    ("ep13_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep13_clip01_alex.mp3": (
        "Wooo we are live and I am grinning like I found a bestseller hiding under a fake name! Welcome back to "
        "The Office 360 Unfiltered. I am Alex. Folks, tonight we are going into author world. A popular story so big "
        "it ate the bestseller list, ate the movies, ate your aunt's book club, and it started as Twilight fan fiction "
        "under a username that sounds like a frozen dessert. Snowqueen Icedragon. Come on! Stay with me. This is "
        "Episode Thirteen and we are going to talk."
    ),
    "ep13_clip02_morgan.mp3": (
        "Ha I cannot stop laughing and I have the research in front of me. I'm Morgan. E.L. James, Erika Mitchell, "
        "a television executive in London, watches Twilight, reads Twilight, rereads Twilight. She writes Master of "
        "the Universe as fan fiction under Snowqueen Icedragon on FanFiction.net. Then she rewrites it, files off the "
        "serial numbers, and the world meets Christian and Ana in Fifty Shades of Grey. The biggest publishing rocket "
        "of that decade was hiding in a fanfic neighborhood like a mansion with no doorbell."
    ),
    "ep13_clip03_alex.mp3": (
        "Come on, I love the details. She told the Chicago Tribune she watched the movie, read the books, reread them, "
        "had unpublished novels in a drawer, then found fan fiction. NPR later put it simply: Christian Grey began his "
        "fictional career as a vampire. There are no vampires in the rewrite and people still say wait, that was Twilight? "
        "Somebody loved a book so much they wrote in the margins of the culture until the margins became the mall."
    ),
    "ep13_clip04_morgan.mp3": (
        "And then the receipts started vanishing. Galleycat and the Los Angeles Times reported Wayback Machine snapshots "
        "of the old site gone. The agent said yes it started as Twilight fan fiction, then she took it down and rewrote it. "
        "The American publisher told the AP that Master of the Universe and Fifty Shades were two distinctly separate works. "
        "If grandma cannot find the hardcover in three clicks, you are doing a Snowqueen without the movie deal."
    ),
    "ep13_clip05_alex.mp3": (
        "This is where our studio lives. Authors come to The Office 360 with a book that could change a life and a homepage "
        "that treats the book like a secret. Three-click discoverability. Book. Store. Done. Fifty Shades found readers "
        "because people passed it like a hot dish, not because the original fanfic site was a cathedral of user experience. "
        "Word of mouth is a miracle. Your website should not require a miracle."
    ),
    "ep13_clip06_morgan.mp3": (
        "Ha, and I have audited this. Publisher site, author site, Amazon tab, Instagram bio that says link in bio pointing "
        "to a link in bio. Funny because a frozen-dessert username built a global franchise. Heavy because a lot of you have "
        "the talent and none of the doorbell. Email theofficetechies@gmail.com, subject Story Time. Launch or reading: "
        "subject Shout Out. We got you covered."
    ),
    "ep13_clip07_alex.mp3": (
        "Wooo I am still on the fanfic because the lesson is delicious. You do not control FanFiction.net. You do not control "
        "the Wayback Machine. You do not control an agency theme that owns your repo. Ownership. Keys. Four seniors, Lisbon "
        "to New York. Fixed scope. When the invoice is paid, the house is yours. Subscribe. Download. Tell one human. "
        "Preferably an aunt who already knows the plot."
    ),
    "ep13_clip08_morgan.mp3": (
        "Mailbox, slow, for the back row. Story Time. Shout Out. Advertise. Donate. All of it theofficetechies@gmail.com. "
        "Listen all the way through. This one is long on purpose. Try to buy your own book on your phone with one thumb. "
        "If you get lost, you already know the punchline. theoffice360.com. Code STUDIO50. Fifty percent off the studio tiers."
    ),
    "ep13_clip09_alex.mp3": (
        "Let me land it with joy. A TV executive falls in love with a vampire romance, writes in the margins, the margins "
        "become a planet, the receipts try to vanish, and somewhere a debut novelist has a gorgeous site where the cart is "
        "three clicks past a poem about fog. Authors, schools, churches, publishers. If your pretty page is FanFiction.net "
        "with a retainer, come see us. We build the doorbell. You own the house."
    ),
    "ep13_clip10_morgan.mp3": (
        "Thank you for sitting in the long hour. I'm Morgan, he's Alex, this was The Office 360 Unfiltered, Episode Thirteen, "
        "the fanfic that ate the bestseller list. Email us. Story Time. Shout Out. Advertise. Donate. theofficetechies@gmail.com. "
        "Listen. Download. Subscribe. Tell an aunt. theoffice360.com. We love you. We got you covered. Go check your own link. Bye!"
    ),
}

KEYWORDS = (
    "The Office 360 Unfiltered, Episode 13, Fifty Shades of Grey origin, E.L. James, Snowqueen Icedragon, "
    "Master of the Universe fanfiction, Twilight fan fiction, author website buy button, 3-click discoverability, "
    "author platform, book marketing website, Lisbon New York web studio, STUDIO50, Story Time, Shout Out, "
    "theofficetechies@gmail.com, listen download subscribe, author site UX, FanFiction.net, Wayback Machine"
)


def main() -> None:
    e3.RNG = np.random.default_rng(36013)
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
        start, end = t, t + c["dur"]
        events.append({**c, "start": start, "end": end})
        t = end if i == len(clips) - 1 else end + e3.PAUSE
    outro = 12.0
    total = t + outro
    if total < MIN_DUR:
        outro += MIN_DUR - total + 8.0
        total = t + outro
        print(f"extended outro to {outro:.1f}s")
    n = int(total * SR)
    print(f"Building {total:.2f}s ({int(total//60)}:{int(total%60):02d})")
    music = e3.make_music(total + 0.5)
    if len(music) < n:
        music = np.concatenate([music, np.zeros((n - len(music), 2))], axis=0)
    music = music[:n]
    duck = e3.db(-24)
    regions = [(0, int(e3.INTRO_PAD * SR), e3.db(-6.5))]
    for ev in events:
        regions.append((int(ev["start"] * SR), int(ev["end"] * SR), duck))
    regions.append((int(events[-1]["end"] * SR), n, e3.db(-7.0)))
    g = e3.smooth_gain_curve(n, regions, duck)
    music = music * g[:, None] * e3.fade(n, int(0.25 * SR), int(min(4.0 * SR, n // 10)))[:, None]
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
    vtt, srt, md = ["WEBVTT", ""], [], [
        f"# The Office 360 Unfiltered — Episode {NUM} Transcript",
        "",
        f"**Title:** {TITLE}",
        f"**Duration:** {duration}",
        "**Hosts:** Alex & Morgan",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        text = TEXTS[ev["file"]]
        vtt += [f"{e3.ts_vtt(ev['start'])} --> {e3.ts_vtt(ev['end'])}", f"<v {ev['speaker']}>{text}", ""]
        srt.append(f"{i}\n{e3.ts(ev['start'])} --> {e3.ts(ev['end'])}\n{ev['speaker']}: {text}\n")
        mm, ss = divmod(int(ev["start"]), 60)
        md += [f"**[{mm:02d}:{ss:02d}] {ev['speaker']}**", "", text, ""]
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / f"TRANSCRIPT_EPISODE_{NUM}.md").write_text("\n".join(md), encoding="utf-8")
    notes = f"""# EPISODE NOTES — Ep {NUM:02d}

**Show:** The Office 360 Unfiltered
**Episode:** {NUM:02d}
**Title:** {TITLE}
**Duration:** {duration} (10:00+ minimum)
**Hosts:** Alex (lead) & Morgan (co-host)
**Artwork:** episode_13_artwork.png

## Story
Popular author-world yarn: E.L. James / Fifty Shades of Grey began as Twilight fan fiction (Master of the Universe, pen name Snowqueen Icedragon). Origins later vanished from web archives. Mixed funny/true landing for authors whose buy button is still hiding.

Sources discussed on air: NPR; Los Angeles Times / Galleycat; Chicago Tribune; Associated Press via reporting.

## Listener CTAs
theofficetechies@gmail.com — subjects: Story Time · Shout Out · Advertise · Donate
Listen · download · subscribe · tell an aunt
https://the-office360.com · STUDIO50

## Paste-ready description
{TITLE}

Alex and Morgan go long on the author-world story hiding in plain sight: a TV executive, a frozen-dessert username, a fanfic that walked out of Twilight's house and ate the bestseller list — then the receipts tried to disappear. The Office 360 moral: three clicks to the book, keys you own, no doorbell in somebody else's coat.

Email theofficetechies@gmail.com (Story Time / Shout Out / Advertise / Donate). Studio: https://the-office360.com · STUDIO50

## Episode keywords
{KEYWORDS}

## Hashtags
#Office360 #TheOffice360Unfiltered #FiftyShades #AuthorWebsite #FanFiction #BuyButton #STUDIO50 #StoryTime
"""
    (ROOT / f"EPISODE_{NUM}_SHOW_NOTES.md").write_text(notes, encoding="utf-8")
    print("TOTAL", duration)
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['dur']:.2f}s")


if __name__ == "__main__":
    main()
