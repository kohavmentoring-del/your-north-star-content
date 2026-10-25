#!/usr/bin/env python3
"""talking-head-edit toolkit. PY _style/tools/vid.py <subcommand> <project> [...]"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../reels
MAX_PAUSE_SPLIT = 0.35  # seconds: gap that starts a new line
MIN_WORDS_TALKING = 3   # fewer real words than this => treat clip as B-roll


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, check=True, **kw)


def ts(seconds):
    m = int(seconds // 60)
    s = seconds - m * 60
    return f"{m:02d}:{s:05.2f}"


def get_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def intake(project):
    proj = ROOT / project
    edit = proj / "_edit"
    (edit / "audio").mkdir(parents=True, exist_ok=True)
    (edit / "frames").mkdir(parents=True, exist_ok=True)
    (edit / "transcripts").mkdir(parents=True, exist_ok=True)

    clips = sorted(
        [p for p in proj.glob("*.MOV")] + [p for p in proj.glob("*.mov")],
        key=lambda p: p.stat().st_mtime,
    )
    if not clips:
        print(f"No .MOV clips found directly in {proj}")
        return

    from faster_whisper import WhisperModel
    print("Loading faster-whisper large-v3-turbo (int8)... this downloads the model on first run.")
    model = WhisperModel("large-v3-turbo", compute_type="int8")

    rows = []  # (take.line, clip_name, in_ts, out_ts, text)
    clip_meta = []  # for status reporting

    for take_idx, clip in enumerate(clips, start=1):
        name = clip.stem
        wav = edit / "audio" / f"{name}.wav"
        if not wav.exists():
            print(f"[{take_idx}/{len(clips)}] extracting audio: {clip.name}")
            sh(f'ffmpeg -y -v error -i "{clip}" -ar 16000 -ac 1 -vn "{wav}"')

        json_path = edit / "transcripts" / f"{name}.json"
        if json_path.exists():
            print(f"[{take_idx}/{len(clips)}] using cached transcript: {clip.name}")
            words = json.loads(json_path.read_text())
        else:
            print(f"[{take_idx}/{len(clips)}] transcribing: {clip.name}")
            segs, _ = model.transcribe(
                str(wav), word_timestamps=True, language="en",
                initial_prompt="Um, uh, like, you know. So, I mean, okay.",
            )
            words = [
                {"w": w.word.strip(), "t": round(w.start, 3), "end": round(w.end, 3)}
                for s in segs for w in s.words if w.word.strip()
            ]
            json_path.write_text(json.dumps(words, indent=1))

        duration = get_duration(clip)
        clip_meta.append((name, duration, len(words)))

        if len(words) < MIN_WORDS_TALKING:
            print(f"    -> {len(words)} words: treating as B-roll/no-speech, not splitting into lines")
            continue

        # split into lines at gaps >= MAX_PAUSE_SPLIT
        lines = []
        cur = [words[0]]
        for prev, w in zip(words, words[1:]):
            if w["t"] - prev["end"] >= MAX_PAUSE_SPLIT:
                lines.append(cur)
                cur = []
            cur.append(w)
        if cur:
            lines.append(cur)

        for line_idx, line_words in enumerate(lines, start=1):
            text = " ".join(w["w"] for w in line_words)
            in_t, out_t = line_words[0]["t"], line_words[-1]["end"]
            line_id = f"{take_idx}.{line_idx:02d}"
            rows.append((line_id, clip.name, ts(in_t), ts(out_t), text))

        # contact sheet(s): one tile per 2s, 8x5 grid = 40 tiles = 80s per sheet
        n_sheets = max(1, int(duration // 80) + 1)
        for page in range(n_sheets):
            start = page * 80
            out_img = edit / "frames" / f"{name}_p{page+1:02d}.jpg"
            if out_img.exists():
                continue
            sh(
                f'ffmpeg -y -v error -ss {start} -t 80 -i "{clip}" '
                f'-vf "fps=1/2,scale=240:-2,tile=8x5" -q:v 3 "{out_img}"'
            )

    # write transcript.md
    md = ["# Transcript — 001-how-to-suck", "", "| id | clip | in-out | text |", "|---|---|---|---|"]
    for line_id, clip_name, in_t, out_t, text in rows:
        md.append(f"| {line_id} | {clip_name} | {in_t}-{out_t} | {text} |")
    (edit / "transcript.md").write_text("\n".join(md) + "\n")

    print("\n=== intake done ===")
    for name, duration, nwords in clip_meta:
        kind = "talking" if nwords >= MIN_WORDS_TALKING else "B-roll/no-speech"
        print(f"  {name}: {duration:.1f}s, {nwords} words -> {kind}")
    print(f"\n{len(rows)} lines written to _edit/transcript.md")


if __name__ == "__main__":
    cmd = sys.argv[1]
    project = sys.argv[2]
    if cmd == "intake":
        intake(project)
    else:
        print(f"unknown subcommand: {cmd}")
        sys.exit(1)
