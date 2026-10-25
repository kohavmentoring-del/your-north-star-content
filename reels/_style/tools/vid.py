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


GRADE = "colortemperature=temperature=5400:mix=0.7,eq=contrast=1.07:brightness=-0.02:saturation=1.14:gamma=0.97"
MAX_PAUSE_TIGHTEN = 0.22
PAD_OUT = 0.07
PAD_IN = 0.05
W, H, FPS = 1080, 1920, 30


def load_words(edit_dir, clip_stem):
    return json.loads((edit_dir / "transcripts" / f"{clip_stem}.json").read_text())


def sub_segments(words, in_t, out_t):
    """Split [in_t, out_t] into sub-segments, cutting internal pauses >= MAX_PAUSE_TIGHTEN."""
    piece_words = [w for w in words if in_t - 0.01 <= w["t"] < out_t + 0.01]
    if not piece_words:
        return [(in_t, out_t)]
    segs = []
    seg_start = max(in_t, piece_words[0]["t"] - PAD_IN)
    for prev, w in zip(piece_words, piece_words[1:]):
        gap = w["t"] - prev["end"]
        if gap >= MAX_PAUSE_TIGHTEN:
            seg_end = min(out_t, prev["end"] + PAD_OUT)
            segs.append((seg_start, seg_end))
            seg_start = max(in_t, w["t"] - PAD_IN)
    seg_end = min(out_t, piece_words[-1]["end"] + PAD_OUT)
    segs.append((seg_start, seg_end))
    return segs


def render_piece(clip_path, s, e, out_path):
    d = e - s
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={W}:{H},setpts=PTS-STARTPTS,fps={FPS},{GRADE},format=yuv420p")
    af = f"afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03,aresample=48000"
    sh(
        f'ffmpeg -y -v error -ss {s:.3f} -i "{clip_path}" -t {d:.3f} '
        f'-vf "{vf}" -af "{af}" '
        f'-c:v libx264 -crf 16 -preset fast -c:a pcm_s16le "{out_path}"'
    )


def cut(project):
    proj = ROOT / project
    edit = proj / "_edit"
    pieces_dir = edit / "pieces"
    renders_dir = edit / "renders"
    pieces_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads((edit / "edit.json").read_text())
    source_clip = proj / data["source_clip"]
    words = load_words(edit, source_clip.stem)

    for vname, v in data["versions"].items():
        if "from" in v:
            continue  # derived versions (e.g. global_speed) handled after base versions
        print(f"=== cutting version '{vname}' ===")
        joined_list = []
        piece_log = []  # (line id, start offset in final cut, end offset)
        cursor = 0.0
        for i, p in enumerate(v["pieces"]):
            segs = sub_segments(words, p["in"], p["out"])
            seg_paths = []
            for j, (s, e) in enumerate(segs):
                out_path = pieces_dir / f"{vname}_{i:02d}_{j:02d}.mov"
                if not out_path.exists():
                    render_piece(source_clip, s, e, out_path)
                seg_paths.append(out_path)
                joined_list.append(out_path)
            piece_dur = sum(e - s for s, e in segs)
            piece_log.append({"line": p["line"], "start": round(cursor, 3), "end": round(cursor + piece_dur, 3)})
            cursor += piece_dur

        concat_txt = pieces_dir / f"{vname}_concat.txt"
        concat_txt.write_text("".join(f"file '{p.resolve()}'\n" for p in joined_list))
        joined = renders_dir / f"{vname}_joined.mov"
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{concat_txt}" -c copy "{joined}"')

        final = renders_dir / f"{vname}.mp4"
        sh(
            f'ffmpeg -y -v error -i "{joined}" '
            f'-af "acompressor=threshold=0.1:ratio=2.5:attack=8:release=120,loudnorm=I=-10.5:TP=-1.0:LRA=7" '
            f'-c:v libx264 -crf 17 -preset medium -c:a aac -b:a 256k -movflags +faststart "{final}"'
        )
        duration = get_duration(final)
        (renders_dir / f"{vname}_pieces.json").write_text(json.dumps(piece_log, indent=1))
        print(f"  -> {final} ({duration:.1f}s)")

    for vname, v in data["versions"].items():
        if "global_speed" not in v:
            continue
        base = renders_dir / f"{v['from']}.mp4"
        sp = v["global_speed"]
        final = renders_dir / f"{vname}.mp4"
        print(f"=== deriving '{vname}' from '{v['from']}' at {sp}x ===")
        sh(
            f'ffmpeg -y -v error -i "{base}" '
            f'-vf "setpts=PTS/{sp}" -af "atempo={sp}" '
            f'-c:v libx264 -crf 17 -preset medium -c:a aac -b:a 256k -movflags +faststart "{final}"'
        )
        base_log = json.loads((renders_dir / f"{v['from']}_pieces.json").read_text())
        scaled = [{"line": p["line"], "start": round(p["start"]/sp, 3), "end": round(p["end"]/sp, 3)} for p in base_log]
        (renders_dir / f"{vname}_pieces.json").write_text(json.dumps(scaled, indent=1))
        duration = get_duration(final)
        print(f"  -> {final} ({duration:.1f}s)")


if __name__ == "__main__":
    cmd = sys.argv[1]
    project = sys.argv[2]
    if cmd == "intake":
        intake(project)
    elif cmd == "cut":
        cut(project)
    else:
        print(f"unknown subcommand: {cmd}")
        sys.exit(1)
