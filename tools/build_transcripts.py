import re

TIMING_FILE = "/home/user/audio/episode_13_timing.txt"

lines = open(TIMING_FILE).read().splitlines()
segments = []
for line in lines:
    if "\t" in line:
        path, start, end = line.split("\t")
        segments.append((path, float(start), float(end)))

# Map filenames to speaker + text (broken into readable chunks)
content = {
    "alex_13_01.wav": ("Alex", [
        "Woo! Live from the gap between Lisbon and New York.",
        "Welcome back to The Office 360 Unfiltered. I am Alex.",
        "This episode is the anatomy of the studio itself.",
        "Four senior people, two cities, and how we outbuild a fifty-person agency that needs a meeting to schedule a meeting.",
        "If you have ever paid for a building and got a hallway, come on. This one is for you.",
    ]),
    "episode_13_clip_02.wav": ("Morgan", [
        "Okay, \"the anatomy of the studio\" sounds very serious for what this actually is,",
        "which is four adults in two time zones arguing about a font choice over coffee.",
        "But that's the point, isn't it? No floor of account managers, no hallway you're secretly paying for,",
        "just the people who actually do the work, doing the work.",
        "That fifty-person-agency line got me though. The meeting to schedule the meeting.",
        "We have all sat in that meeting. We have all watched it go nowhere for forty-five minutes.",
    ]),
    "alex_13_03.wav": ("Alex", [
        "Woo! We are live, and look at the rundown, no sponsor in the chair today. This hour is ours.",
        "Welcome back to The Office 360 Unfiltered, I am Alex.",
        "We told you we hit twenty downloads all over the world. We meant it, we did not inflate it.",
        "Today is not another roast of a WordPress retainer.",
        "Today is the growth episode, how you helped this show live.",
        "Listen, download, subscribe, send a shout out, book an ad.",
    ]),
    "episode_13_clip_04.wav": ("Morgan", [
        "Twenty downloads, all over the world, no inflation, no fake dashboard confetti,",
        "just real people in real places pressing play.",
        "And listen, we know twenty sounds small if you're used to shows that claim numbers nobody can check.",
        "We would rather tell you the true twenty than a made-up twenty thousand.",
        "And no roast today, which, honestly, feels like a vacation. But don't get comfortable.",
        "Because Alex is about to ask you for something, and I want you to actually listen to how he does it.",
    ]),
    "episode_13_clip_05.wav": ("Morgan", [
        "Before Alex gets to the actual ask, let's talk about what \"growth episode\" has meant so far,",
        "because it is not us buying followers or running a giveaway for a ring light.",
        "It's been four people showing up every week, telling true stories about broken donation pages",
        "and wedding sites stuck on page 404, and slowly, actually slowly, people started forwarding the show to other people.",
        "That is the entire growth strategy. No funnel, no algorithm hack, just \"hey, you should hear this one.\"",
        "So when Alex asks you for something in a second, know that the twenty of you who are already here are the reason there's an ask to make at all.",
        "You built the room. He's just opening the door a little wider.",
    ]),
    "alex_13_05.wav": ("Alex", [
        "And if you have a few dollars, and you believe four seniors in Lisbon and New York should keep telling the truth on a microphone,",
        "there is a donation door too.",
        "I am grinning, because this is the unfiltered version of asking.",
        "No fake million, no crying violin, just a room that wants a twenty-first listener,",
        "and a show that wants to stay on the air without selling you a hallway.",
    ]),
    "episode_13_clip_07.wav": ("Morgan", [
        "I love that he will not even let the ask be dramatic. No violin, no fake milestone,",
        "just \"we exist, we're useful, help us keep existing.\" That's the whole pitch.",
        "So here is exactly how you do that. Story Time is open if you've got a tale for us,",
        "email the office techies at gmail dot com, subject line Story Time.",
        "Want a Shout Out? Same address, subject Shout Out, tell us what, when, where, and who should show up.",
        "Want to Advertise or Donate? Same inbox, subject Advertise or subject Donate, and we will get back to you.",
        "Listen, download, subscribe, and tell one person who needs to hear four seniors tell the truth on a microphone.",
        "That's it, that's the ask. We'll see you next time on The Office 360 Unfiltered.",
    ]),
}


def fmt_srt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_vtt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


# Build per-line sub-segments distributing time proportionally by character count
cues = []
for path, start, end in segments:
    fname = path.split("/")[-1]
    speaker, sents = content[fname]
    dur = end - start
    char_counts = [len(s) for s in sents]
    total_chars = sum(char_counts)
    t = start
    for sent, cc in zip(sents, char_counts):
        seg_dur = dur * (cc / total_chars)
        cues.append((t, t + seg_dur, speaker, sent))
        t += seg_dur

# SRT
srt_lines = []
for i, (start, end, speaker, text) in enumerate(cues, 1):
    srt_lines.append(str(i))
    srt_lines.append(f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}")
    srt_lines.append(f"{speaker}: {text}")
    srt_lines.append("")
open("/home/user/TRANSCRIPT_EPISODE_13.srt", "w").write("\n".join(srt_lines))

# VTT
vtt_lines = ["WEBVTT", ""]
for i, (start, end, speaker, text) in enumerate(cues, 1):
    vtt_lines.append(str(i))
    vtt_lines.append(f"{fmt_vtt_time(start)} --> {fmt_vtt_time(end)}")
    vtt_lines.append(f"{speaker}: {text}")
    vtt_lines.append("")
open("/home/user/TRANSCRIPT_EPISODE_13.vtt", "w").write("\n".join(vtt_lines))

# Markdown readable transcript
md_lines = [
    "# The Office 360 Unfiltered — Episode 13",
    "## \"Behind the Mic — The Anatomy of Unfiltered\"",
    "",
    f"**Runtime:** {fmt_srt_time(cues[-1][1]).split(',')[0]} (approx 4:03)",
    "",
    "---",
    "",
]
current_speaker = None
buffer = []
for path, start, end in segments:
    fname = path.split("/")[-1]
    speaker, sents = content[fname]
    md_lines.append(f"**{speaker}** _[{start:0.1f}s–{end:0.1f}s]_")
    md_lines.append("")
    md_lines.append(" ".join(sents))
    md_lines.append("")
open("/home/user/TRANSCRIPT_EPISODE_13.md", "w").write("\n".join(md_lines))

print("Wrote SRT, VTT, MD transcripts.")
print("Total cues:", len(cues))
