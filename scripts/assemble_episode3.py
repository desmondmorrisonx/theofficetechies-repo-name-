#!/usr/bin/env python3
"""Assemble The Office 360 Unfiltered — Episode 3 broadcast master."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import lfilter

SR = 24_000
PAUSE = 0.380
AD_TAIL_PAUSE = 1.050
INTRO_PAD = 1.85
OUTRO_PAD = 4.40
PEAK = 0.94
RNG = np.random.default_rng(36003)

ROOT = Path("/home/user")
AUDIO = ROOT / "audio"

CLIPS = [
    ("ep3_clip01_alex.mp3", "Alex", "cold"),
    ("ep3_clip02_morgan.mp3", "Morgan", "speech"),
    ("ep3_clip03_alex.mp3", "Alex", "speech"),
    ("ep3_clip04_morgan.mp3", "Morgan", "speech"),
    ("ep3_clip05_alex.mp3", "Alex", "speech"),
    ("ep3_clip06_morgan.mp3", "Morgan", "speech"),
    ("ep3_clip07_alex.mp3", "Alex", "ad"),
    ("ep3_clip08_morgan.mp3", "Morgan", "speech"),
    ("ep3_clip09_alex.mp3", "Alex", "speech"),
    ("ep3_clip10_morgan.mp3", "Morgan", "outro"),
]

TEXTS = {
    "ep3_clip01_alex.mp3": (
        "Wooo! We are live, we are loud, and I am grinning like I just found money in an old jacket. "
        "Welcome back to The Office 360 Unfiltered. I am Alex. Folks, today's story is so ridiculous "
        "I laughed on the way to the mic. Agencies. Charging. Ten thousand dollars a year. Just to click "
        "update plugins. Come on. Come on!"
    ),
    "ep3_clip02_morgan.mp3": (
        "Ha! He has not stopped bouncing since breakfast. I'm Morgan, and yes, that invoice is real. "
        "Fifteen hundred a month. For pressing a button. For clearing a cache. For telling you your site "
        "is still up. That is not engineering. That is a very expensive goldfish sitter. And if you have "
        "been writing that check, this one is for you."
    ),
    "ep3_clip03_alex.mp3": (
        "A goldfish sitter! I love that. Okay, picture this. You built a cute WordPress site back in "
        "twenty eighteen. Fine. Then the agency leans in, all serious, and says the internet is dangerous, "
        "you need a retainer. Security updates. Plugin updates. Theme updates. And boom, you are on the "
        "hook for ten grand a year. Meanwhile the site still loads like it is running on a flip phone in a tunnel."
    ),
    "ep3_clip04_morgan.mp3": (
        "And the funny sad part, the part that gets me, is what you are actually buying. You are buying fear. "
        "Oh no, if we don't update it, hackers. Oh no, if we don't patch it, Google. So you keep paying. "
        "They keep clicking. Nothing gets faster. Nothing gets prettier. And your leads still vanish into a "
        "contact form that emails somebody's intern at two in the morning. That is the product. Anxiety with a login screen."
    ),
    "ep3_clip05_alex.mp3": (
        "Exactly. At The Office 360 we looked at this circus and said, why are we babysitting a stack that "
        "wants to break every Tuesday? We don't do that. Four senior people. Lisbon to New York. No junior "
        "freelancers hiding in the spreadsheet. You own every line of code. We build it modern. Jamstack. "
        "Headless where it should be headless. Static where it should be static. It ships fast, it stays fast, "
        "and you are not paying tribute to the plugin gods every month."
    ),
    "ep3_clip06_morgan.mp3": (
        "Let me translate that for the humans in the back row. Jamstack means your pages are pre-built. They fly. "
        "HTTPS is handled. No dusty admin panel sitting there like an unlocked candy store. No please update "
        "twenty-seven plugins before lunch. And if you need a form, a CRM, a little automation? We wire that in "
        "once, clean, and it just works. You are not renting peace of mind. You bought the peace. That is the "
        "whole joke of the retainer. They sell you a leak, then they sell you the bucket."
    ),
    "ep3_clip07_alex.mp3": (
        "Alright, live show rule, we keep it honest and we keep it short. If you are done lighting money on fire "
        "for retainers, go to theoffice360.com. Use code STUDIO50. That is studio fifty. Fifty percent off. "
        "Turnkey Build, normally eighteen hundred. IA Roadmap, nine hundred. HTTPS Security, six hundred. "
        "Half off, all of it. Email theofficetechies@gmail.com if you just want to talk like humans. We will be "
        "right back. Don't you go anywhere."
    ),
    "ep3_clip08_morgan.mp3": (
        "And we are back, and I still cannot get over the math. Ten thousand a year, times three years. That is "
        "a brand new site. That is a whole lead machine. That is you, not the agency, owning the thing. "
        "The Office 360 does fixed scope, fixed price. No surprise invoices. No, oh we had to update WooCommerce "
        "again so here is another bill. You know the number before we write a line."
    ),
    "ep3_clip09_alex.mp3": (
        "I would frame that old retainer invoice and hang it in a museum of bad decisions. Authors, schools, "
        "publishers, churches, if your site needs a priest and a developer every Sunday, it is the architecture, "
        "not your people. We do three-click discoverability. Visitor finds the book, the event, the donate button, "
        "boom. And because it is modern, you are not calling us to babysit plugins. You call us when you want to grow. "
        "That is a much better phone call. I actually like those."
    ),
    "ep3_clip10_morgan.mp3": (
        "Ha, me too. So here is your live-show homework. Open last year's web invoices. If you paid a fortune for "
        "someone to click update, you already know the punchline. Come see us. theoffice360.com. Code STUDIO50. "
        "We are four people who actually build the thing, and we are having way too much fun doing it. I'm Morgan, "
        "he's Alex, this was The Office 360 Unfiltered. Go be free of the plugin gods. We love you. Bye!"
    ),
}


def db(x: float) -> float:
    return 10 ** (x / 20.0)


def fade(n: int, fade_in: int, fade_out: int) -> np.ndarray:
    env = np.ones(n, dtype=np.float64)
    if fade_in > 0:
        env[:fade_in] *= np.linspace(0, 1, fade_in)
    if fade_out > 0:
        env[-fade_out:] *= np.linspace(1, 0, fade_out)
    return env


def one_pole_lowpass(x: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    rc = 1.0 / (2 * math.pi * cutoff)
    a = 1.0 / (rc * sr + 1.0)
    y = np.empty_like(x)
    acc = 0.0
    for i, s in enumerate(x):
        acc += a * (s - acc)
        y[i] = acc
    return y


def one_pole_highpass(x: np.ndarray, cutoff: float, sr: int = SR) -> np.ndarray:
    return x - one_pole_lowpass(x, cutoff, sr)


def exp_decay(n: int, t60: float, sr: int = SR) -> np.ndarray:
    # amplitude envelope approximating t60 decay
    tau = t60 / math.log(1000)
    t = np.arange(n) / sr
    return np.exp(-t / max(tau, 1e-4))


def midi_to_hz(m: float) -> float:
    return 440.0 * (2 ** ((m - 69) / 12.0))


def kick(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    freq = 118 * np.exp(-t * 18) + 38
    phase = 2 * np.pi * np.cumsum(freq) / SR
    body = np.sin(phase) * exp_decay(n, 0.28)
    click = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.22
    return (body + click) * fade(n, 4, 80)


def snare(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    noise = RNG.standard_normal(n)
    # cheap highpass via first difference + decay
    noise = np.concatenate([[0], np.diff(noise)])
    noise *= exp_decay(n, 0.18)
    tone = np.sin(2 * np.pi * 190 * t) * exp_decay(n, 0.16) * 0.35
    return (0.72 * noise + tone) * fade(n, 3, 60) * 0.55


def hat(n: int, open_hat: bool = False) -> np.ndarray:
    noise = RNG.standard_normal(n)
    noise = np.concatenate([[0], np.diff(noise)])
    t60 = 0.12 if open_hat else 0.045
    return noise * exp_decay(n, t60) * fade(n, 1, 20) * (0.22 if open_hat else 0.14)


def rhodes_note(freq: float, n: int, vel: float = 0.4) -> np.ndarray:
    t = np.arange(n) / SR
    det = 1.003
    a = np.sin(2 * np.pi * freq * t)
    b = np.sin(2 * np.pi * freq * det * t)
    c = 0.28 * np.sin(2 * np.pi * freq * 2 * t)
    d = 0.08 * np.sin(2 * np.pi * freq * 3 * t + 0.3)
    trem = 0.85 + 0.15 * np.sin(2 * np.pi * 5.4 * t)
    env = np.exp(-t * 1.15) * (1 - np.exp(-t * 90))
    env = np.maximum(env, 0.08 * np.exp(-t * 0.35))  # sustain pad
    sig = (a + b + c + d) * 0.33 * trem * env * vel
    return sig * fade(n, 12, 400)


def bass_note(freq: float, n: int) -> np.ndarray:
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(2 * np.pi * freq * 2 * t)
    env = (1 - np.exp(-t * 70)) * np.exp(-t * 3.2)
    env = np.maximum(env, 0.35 * np.exp(-t * 0.8))
    return sig * env * 0.42 * fade(n, 8, 200)


def vinyl(n: int) -> np.ndarray:
    hiss = RNG.standard_normal(n) * 0.012
    # slow rumble
    t = np.arange(n) / SR
    rumble = 0.006 * np.sin(2 * np.pi * 0.33 * t + 0.4)
    pops = np.zeros(n)
    for _ in range(int(n / SR * 2.2)):
        i = int(RNG.integers(0, n - 40))
        pops[i : i + 18] += RNG.normal(0, 0.08) * np.linspace(1, 0, 18)
    return hiss + rumble + pops


def make_music(seconds: float) -> np.ndarray:
    """Lo-fi dusty Rhodes bed, 78 BPM, stereo."""
    n = int(seconds * SR) + SR
    bpm = 78.0
    beat = 60.0 / bpm
    samples_beat = int(beat * SR)

    # chord voicings as MIDI (lo-fi jazz loop)
    # Fmaj7 | Am7 | Dm7 | Cmaj7
    chords = [
        [53, 57, 60, 64],  # F A C E
        [57, 60, 64, 67],  # A C E G
        [50, 53, 57, 60],  # D F A C
        [48, 52, 55, 59],  # C E G B
    ]
    bass_roots = [41, 45, 38, 36]  # F2 A2 D2 C2

    left = np.zeros(n)
    right = np.zeros(n)

    # drums + keys looped
    total_beats = int(math.ceil(seconds / beat)) + 8
    for bi in range(total_beats):
        start = bi * samples_beat
        if start >= n:
            break
        bar_pos = bi % 16  # 4 bars * 4 beats
        beat_in_bar = bi % 4
        bar = (bi // 4) % 4

        # kick on 1 and 3, extra ghost on last bar
        if beat_in_bar in (0, 2):
            k = kick(int(0.42 * SR))
            end = min(start + len(k), n)
            left[start:end] += k[: end - start] * 0.95
            right[start:end] += k[: end - start] * 0.95
        if bar == 3 and beat_in_bar == 3:
            k = kick(int(0.22 * SR)) * 0.35
            ghost_at = start + samples_beat // 2
            end = min(ghost_at + len(k), n)
            if ghost_at < n:
                left[ghost_at:end] += k[: end - ghost_at]
                right[ghost_at:end] += k[: end - ghost_at]

        # snare on 2 and 4
        if beat_in_bar in (1, 3):
            s = snare(int(0.32 * SR))
            end = min(start + len(s), n)
            left[start:end] += s[: end - start] * 0.92
            right[start:end] += s[: end - start] * 1.0

        # hats 8th notes
        for sub in (0, 1):
            hs = start + sub * samples_beat // 2
            open_hat = beat_in_bar == 3 and sub == 1
            h = hat(int((0.18 if open_hat else 0.09) * SR), open_hat=open_hat)
            end = min(hs + len(h), n)
            if hs < n:
                pan = 0.85 if sub == 0 else 1.15
                left[hs:end] += h[: end - hs] * (2 - pan)
                right[hs:end] += h[: end - hs] * pan

        # keys on downbeat of each bar, held ~ 3.6 beats
        if beat_in_bar == 0:
            hold = int(3.55 * samples_beat)
            hold = min(hold, n - start)
            if hold > 100:
                chord = chords[bar]
                acc = np.zeros(hold)
                for i, m in enumerate(chord):
                    vel = 0.33 if i == 0 else 0.26
                    acc += rhodes_note(midi_to_hz(m), hold, vel=vel)
                acc *= fade(hold, 30, min(1800, hold // 4))
                # stereo spread
                end = start + hold
                left[start:end] += acc * 0.85
                right[start:end] += np.roll(acc, 28) * 0.9

                b = bass_note(midi_to_hz(bass_roots[bar]), hold)
                left[start:end] += b * 0.95
                right[start:end] += b * 0.95

        # extra bass octave walk on beat 3
        if beat_in_bar == 2:
            hold = int(1.6 * samples_beat)
            hold = min(hold, n - start)
            if hold > 80:
                b = bass_note(midi_to_hz(bass_roots[bar] + 12), hold) * 0.35
                end = start + hold
                left[start:end] += b
                right[start:end] += b

    crack = vinyl(n)
    left += crack
    right += crack * 0.92

    # gentle saturation
    music = np.stack([left, right], axis=1)
    music = np.tanh(music * 1.35) * 0.85
    # high shelf cut for dusty lo-fi
    # simple one-pole on each channel
    for ch in range(2):
        music[:, ch] = one_pole_lowpass(music[:, ch], 6200)
    peak = np.max(np.abs(music)) + 1e-9
    music = music / peak * 0.55
    return music[: int(seconds * SR)]


def load_mono(path: Path) -> np.ndarray:
    data, sr = sf.read(str(path), always_2d=False)
    if data.ndim > 1:
        data = data.mean(axis=1)
    if sr != SR:
        # linear resample
        x_old = np.linspace(0, 1, len(data))
        x_new = np.linspace(0, 1, int(len(data) * SR / sr))
        data = np.interp(x_new, x_old, data)
    # trim trailing near-silence
    absd = np.abs(data)
    thresh = 0.008
    idx = np.where(absd > thresh)[0]
    if len(idx):
        end = min(len(data), idx[-1] + int(0.08 * SR))
        start = max(0, idx[0] - int(0.02 * SR))
        data = data[start:end]
    # light presence + de-ess-ish high cut, gentle compression for human live punch
    data = data - one_pole_lowpass(data, 80) * 0.15  # little low rumble out
    # vectorized-ish compressor via smoothed envelope
    env = np.abs(data)
    env = one_pole_lowpass(env, 18)
    thresh = 0.28
    ratio = 2.4
    over = np.maximum(env / thresh, 1.0)
    gain = over ** ((1 - ratio) / ratio)
    data = data * gain
    # live-show makeup + slight warmth
    data = np.tanh(data * 1.18) * 1.05
    peak = np.max(np.abs(data)) + 1e-9
    data = data / peak * 0.89
    return data.astype(np.float64)


def stereo_voice(mono: np.ndarray) -> np.ndarray:
    # tiny Haas for not-dead-center without chorus AI artifacts
    left = mono
    right = np.concatenate([np.zeros(6), mono[:-6]]) if len(mono) > 6 else mono
    return np.stack([left * 0.98, right * 1.0], axis=1)


def smooth_gain_curve(n: int, regions: list[tuple[int, int, float]], default: float) -> np.ndarray:
    g = np.full(n, default, dtype=np.float64)
    for s, e, val in regions:
        s = max(0, min(n, s))
        e = max(0, min(n, e))
        g[s:e] = val
    # 90ms ramps
    ramp = int(0.09 * SR)
    kernel = np.ones(ramp) / ramp
    # pad to keep length
    pad = ramp // 2
    gp = np.pad(g, (pad, ramp - pad), mode="edge")
    return np.convolve(gp, kernel, mode="valid")[:n]


def ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def ts_vtt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def main() -> None:
    clips = []
    for fname, speaker, kind in CLIPS:
        mono = load_mono(AUDIO / fname)
        clips.append(
            {
                "file": fname,
                "speaker": speaker,
                "kind": kind,
                "audio": stereo_voice(mono),
                "dur": len(mono) / SR,
            }
        )

    # timeline
    t = INTRO_PAD
    events = []
    for i, c in enumerate(clips):
        start = t
        end = t + c["dur"]
        events.append({**c, "start": start, "end": end})
        if i == len(clips) - 1:
            t = end
        elif c["kind"] == "ad":
            t = end + AD_TAIL_PAUSE
        else:
            t = end + PAUSE
    total = t + OUTRO_PAD
    n = int(total * SR)

    print(f"Building {total:.2f}s master @ {SR} Hz")
    music = make_music(total + 0.5)
    if len(music) < n:
        pad = np.zeros((n - len(music), 2))
        music = np.concatenate([music, pad], axis=0)
    music = music[:n]

    # ducking regions
    duck_speech = db(-24)
    duck_ad = db(-13)
    duck_intro = db(-6.5)
    duck_outro = db(-7.5)
    default = duck_speech
    regions = [(0, int(INTRO_PAD * SR), duck_intro)]
    for ev in events:
        s = int(ev["start"] * SR)
        e = int(ev["end"] * SR)
        val = duck_ad if ev["kind"] == "ad" else duck_speech
        # lift music 120ms before downbeat of ad and outro
        regions.append((s, e, val))
    regions.append((int(events[-1]["end"] * SR), n, duck_outro))
    g = smooth_gain_curve(n, regions, default)
    music = music * g[:, None]

    # fade music in/out
    music *= fade(n, int(0.25 * SR), int(3.2 * SR))[:, None]

    mix = music.copy()
    for ev in events:
        s = int(ev["start"] * SR)
        a = ev["audio"]
        e = min(n, s + len(a))
        mix[s:e] += a[: e - s]

    peak = np.max(np.abs(mix)) + 1e-12
    mix = mix / peak * PEAK
    # true peak-ish limiter
    mix = np.tanh(mix * 1.02) / math.tanh(1.02) * PEAK

    wav_path = ROOT / "The_Office_360_Unfiltered_Episode_3.wav"
    mp3_path = ROOT / "The_Office_360_Unfiltered_Episode_3.mp3"
    sf.write(str(wav_path), mix, SR, subtype="PCM_16")
    sf.write(str(mp3_path), mix, SR, format="MP3")
    print("Wrote", wav_path, mp3_path, "dur", len(mix) / SR)

    # transcripts
    vtt = ["WEBVTT", ""]
    srt_blocks = []
    md_lines = [
        "# The Office 360 Unfiltered — Episode 3 Transcript",
        "",
        "**Title:** The $10k WordPress Retainer Scam & The Modern Jamstack",
        f"**Duration:** {int(total // 60):02d}:{int(total % 60):02d}",
        "**Hosts:** Alex & Morgan",
        "**Promo:** `STUDIO50` — 50% off at https://the-office360.com",
        "",
        "## Show Notes",
        "",
        "Live-show energy this week: Alex and Morgan tear apart the classic WordPress retainer — the $1,500/month (about $10k a year) habit of paying an agency to click **Update Plugins** — and contrast it with The Office 360's senior-only Jamstack / headless / static builds.",
        "",
        "- Why retainers sell fear, not engineering",
        "- What Jamstack actually means in human language",
        "- Fixed scope, fixed price, 100% code ownership",
        "- Who this is for: authors, schools, publishers, faith orgs",
        "- Promo code **STUDIO50** (50% off Turnkey Build $1,800 / IA Roadmap $900 / HTTPS Security $600)",
        "- Inquiries: theofficetechies@gmail.com",
        "",
        "## High-intent SEO keywords",
        "",
        "`WordPress retainer scam`, `Jamstack agency`, `headless CMS for authors`, `fixed price web studio`, "
        "`plugin update retainer`, `The Office 360`, `STUDIO50`, `static site for churches`, "
        "`school website rebuild`, `Lisbon New York web studio`",
        "",
        "## Transcript",
        "",
    ]
    for i, ev in enumerate(events, start=1):
        start, end = ev["start"], ev["end"]
        speaker = ev["speaker"]
        text = TEXTS[ev["file"]]
        vtt.append(f"{ts_vtt(start)} --> {ts_vtt(end)}")
        vtt.append(f"<v {speaker}>{text}")
        vtt.append("")
        srt_blocks.append(
            f"{i}\n{ts(start)} --> {ts(end)}\n{speaker}: {text}\n"
        )
        mm, ss = divmod(int(start), 60)
        md_lines.append(f"**[{mm:02d}:{ss:02d}] {speaker}**")
        md_lines.append("")
        md_lines.append(text)
        md_lines.append("")

    (ROOT / "TRANSCRIPT_EPISODE_3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (ROOT / "TRANSCRIPT_EPISODE_3.srt").write_text("\n".join(srt_blocks), encoding="utf-8")
    (ROOT / "TRANSCRIPT_EPISODE_3.md").write_text("\n".join(md_lines), encoding="utf-8")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>The Office 360 Unfiltered</title>
    <link>https://the-office360.com</link>
    <description>The no-BS podcast on bespoke web architecture, 3-click discoverability, CRM automation, and senior studio engineering.</description>
    <language>en-us</language>
    <itunes:author>The Office 360</itunes:author>
    <itunes:summary>Live, unfiltered conversations from a 4-person senior studio between Lisbon and New York.</itunes:summary>
    <item>
      <title>Episode 3: The $10k WordPress Retainer Scam &amp; The Modern Jamstack</title>
      <description>Alex and Morgan go live on the classic agency retainer: $10k a year to click Update Plugins. They unpack the fear product, then show the Office 360 Jamstack alternative — fixed scope, full ownership, zero plugin babysitting. Promo code STUDIO50.</description>
      <guid isPermaLink="false">office360-unfiltered-ep3</guid>
      <itunes:duration>{int(total // 60)}:{int(total % 60):02d}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
      <link>https://the-office360.com</link>
    </item>
  </channel>
</rss>
"""
    (ROOT / "EPISODE_3_RSS.xml").write_text(rss, encoding="utf-8")
    print("Transcripts + RSS written")
    print("EVENTS:")
    for ev in events:
        print(f"  {ev['start']:7.2f}-{ev['end']:7.2f}  {ev['speaker']:7s} {ev['kind']:6s} {ev['dur']:.2f}s")


if __name__ == "__main__":
    main()
