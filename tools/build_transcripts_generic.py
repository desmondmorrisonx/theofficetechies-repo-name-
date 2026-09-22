"""
Build SRT / VTT / Markdown transcripts for any episode of
The Office 360 Unfiltered, from the timing map written by
tools/mix_episode_generic.py.

Transcript text is parsed straight out of EPISODE_N_SCRIPT.md, so the
transcript can never drift from the script. Timestamps come from the
real mixed timeline, so they can never drift from the audio.

Usage:
    python3 tools/build_transcripts_generic.py 14
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(REPO, "audio")

TITLES = {
    "14": "Behind the Mic — Part 2: We Got a Listener (And Regret Nothing)",
    "15": "What The Office 360 Actually Is (Featuring: The Book That Went From Invisible to Visible)",
}


def parse_script(ep):
    """Pull {filename: (speaker, [sentences])} out of EPISODE_N_SCRIPT.md."""
    path = os.path.join(REPO, f"EPISODE_{ep}_SCRIPT.md")
    text = open(path, encoding="utf-8").read()

    blocks = re.split(r"^### CLIP \d+", text, flags=re.M)[1:]
    headers = re.findall(r"^### CLIP \d+ — (\w+).*$", text, flags=re.M)
    files = re.findall(
        r"^### CLIP \d+ — \w+ \((?:real audio — record as |voice-00, file: )([a-z0-9_]+\.wav)\)",
        text, flags=re.M)

    if not (len(blocks) == len(headers) == len(files)):
        raise SystemExit(
            f"Script parse mismatch for episode {ep}: "
            f"{len(blocks)} blocks / {len(headers)} speakers / {len(files)} files")

    out = {}
    for speaker, fname, block in zip(headers, files, blocks):
        body = block.split(")", 1)[1] if ")" in block.split("\n")[0] else block
        body = body.split("\n", 1)[1] if "\n" in body else body
        body = body.split("---")[0].strip()
        body = re.sub(r"\s+", " ", body).strip()
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", body) if s.strip()]
        # group into readable 1-2 sentence cues
        cues, buf = [], ""
        for s in sents:
            cand = (buf + " " + s).strip()
            if len(cand) > 150 and buf:
                cues.append(buf)
                buf = s
            else:
                buf = cand
        if buf:
            cues.append(buf)
        out[fname] = (speaker.capitalize(), cues)
    return out


def read_timing(ep):
    path = os.path.join(AUDIO, f"episode_{ep}_timing.txt")
    if not os.path.exists(path):
        raise SystemExit(
            f"No timing map at {path}.\nRun: python3 tools/mix_episode_generic.py {ep}")
    segs = []
    for line in open(path).read().splitlines():
        if "\t" in line:
            parts = line.split("\t")
            fname = os.path.basename(parts[0])
            segs.append((fname, float(parts[1]), float(parts[2])))
    return segs


def fmt_srt(t):
    h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d},{int(round((t - int(t)) * 1000)):03d}"


def fmt_vtt(t):
    h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{int(round((t - int(t)) * 1000)):03d}"


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TITLES:
        print("Usage: python3 tools/build_transcripts_generic.py [14|15]")
        sys.exit(2)
    ep = sys.argv[1]

    content = parse_script(ep)
    segments = read_timing(ep)

    cues = []
    for fname, start, end in segments:
        if fname not in content:
            raise SystemExit(f"No script text for {fname}")
        speaker, sents = content[fname]
        dur = end - start
        counts = [len(s) for s in sents]
        total = sum(counts) or 1
        t = start
        for sent, cc in zip(sents, counts):
            seg = dur * (cc / total)
            cues.append((t, t + seg, speaker, sent))
            t += seg

    srt = []
    for i, (s, e, spk, txt) in enumerate(cues, 1):
        srt += [str(i), f"{fmt_srt(s)} --> {fmt_srt(e)}", f"{spk}: {txt}", ""]
    open(os.path.join(REPO, f"TRANSCRIPT_EPISODE_{ep}.srt"), "w", encoding="utf-8").write("\n".join(srt))

    vtt = ["WEBVTT", ""]
    for i, (s, e, spk, txt) in enumerate(cues, 1):
        vtt += [str(i), f"{fmt_vtt(s)} --> {fmt_vtt(e)}", f"{spk}: {txt}", ""]
    open(os.path.join(REPO, f"TRANSCRIPT_EPISODE_{ep}.vtt"), "w", encoding="utf-8").write("\n".join(vtt))

    runtime = segments[-1][2]
    md = [
        f"# The Office 360 Unfiltered — Episode {ep}",
        f'## "{TITLES[ep]}"',
        "",
        f"**Runtime:** approx {int(runtime)//60}:{int(runtime)%60:02d}",
        "",
        "---",
        "",
    ]
    for fname, start, end in segments:
        speaker, sents = content[fname]
        md += [f"**{speaker}** _[{start:0.1f}s–{end:0.1f}s]_", "", " ".join(sents), ""]
    open(os.path.join(REPO, f"TRANSCRIPT_EPISODE_{ep}.md"), "w", encoding="utf-8").write("\n".join(md))

    print(f"Episode {ep}: wrote SRT, VTT, MD. {len(cues)} cues, runtime {int(runtime)//60}:{int(runtime)%60:02d}.")


if __name__ == "__main__":
    main()
