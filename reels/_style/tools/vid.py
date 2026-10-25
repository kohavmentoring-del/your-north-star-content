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
END_PAD = 0.35  # breathing room after a piece's last word so sentences don't cut off mid-word
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


CAPTION_FONT = "Montserrat ExtraBold"
CAPTION_FONT_FILE = str(ROOT / "_style" / "fonts" / "Montserrat-ExtraBold.ttf")
CAPTION_COLOR = "&H002A1A6B"  # ASS &HAABBGGRR: burgundy #6B1A2A, no alpha
CAPTION_SIZE = 68
CAPTION_Y = 1350  # lower third: this footage is framed too tight for the usual above-head wall space
WORDS_PER_CAPTION = 3


def words_to_captions(cue_words):
    """Group (text, start, end) word tuples into 2-4 word caption cues."""
    cues = []
    for i in range(0, len(cue_words), WORDS_PER_CAPTION):
        group = cue_words[i:i + WORDS_PER_CAPTION]
        text = " ".join(w[0] for w in group).lower()
        start = group[0][1]
        end = group[-1][2]
        cues.append((text, start, end))
    return cues


def write_ass(cues, path, video_w=W, video_h=H):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {video_w}
PlayResY: {video_h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{CAPTION_FONT},{CAPTION_SIZE},{CAPTION_COLOR},&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,1.2,8,140,140,{CAPTION_Y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        return f"{h:d}:{m:02d}:{s:05.2f}"

    lines = [header]
    for text, start, end in cues:
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Caption,,0,0,0,,{text}\n")
    Path(path).write_text("".join(lines))


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
        cue_words = []  # (text, final_start, final_end) for captions
        cursor = 0.0
        for i, p in enumerate(v["pieces"]):
            segs = sub_segments(words, p["in"], p["out"])
            n = len(segs)
            seg_paths = []
            for j, (s, e) in enumerate(segs):
                # extend only the piece's final segment so sentences get breathing
                # room at the end instead of cutting off on the last word
                render_e = e + END_PAD if j == n - 1 else e
                out_path = pieces_dir / f"{vname}_{i:02d}_{j:02d}.mov"
                if not out_path.exists():
                    render_piece(source_clip, s, render_e, out_path)
                seg_paths.append(out_path)
                joined_list.append(out_path)
                seg_cursor = cursor + sum(
                    (segs[k][1] - segs[k][0] + (END_PAD if k == n - 1 else 0)) for k in range(j)
                )
                for w in words:
                    if s - 0.005 <= w["t"] < e:
                        cue_words.append((w["w"], seg_cursor + (w["t"] - s), seg_cursor + (min(w["end"], e) - s)))
            piece_dur = sum(e - s for s, e in segs) + END_PAD
            piece_log.append({"line": p["line"], "start": round(cursor, 3), "end": round(cursor + piece_dur, 3)})
            cursor += piece_dur

        concat_txt = pieces_dir / f"{vname}_concat.txt"
        concat_txt.write_text("".join(f"file '{p.resolve()}'\n" for p in joined_list))
        joined = renders_dir / f"{vname}_joined.mov"
        sh(f'ffmpeg -y -v error -f concat -safe 0 -i "{concat_txt}" -c copy "{joined}"')

        final = renders_dir / f"{vname}.mp4"
        sh(
            f'ffmpeg -y -v error -i "{joined}" '
            f'-af "acompressor=threshold=0.178:ratio=2:attack=20:release=200,loudnorm=I=-10.5:TP=-1.0:LRA=7" '
            f'-c:v libx264 -crf 17 -preset medium -c:a aac -b:a 256k -movflags +faststart "{final}"'
        )
        duration = get_duration(final)
        (renders_dir / f"{vname}_pieces.json").write_text(json.dumps(piece_log, indent=1))
        (renders_dir / f"{vname}_cues.json").write_text(json.dumps(cue_words, indent=1))
        print(f"  -> {final} ({duration:.1f}s)")

        burn_captions(vname, final, cue_words, renders_dir)

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
        base_cues = json.loads((renders_dir / f"{v['from']}_cues.json").read_text())
        scaled_cues = [(w, round(s/sp, 3), round(e/sp, 3)) for w, s, e in base_cues]
        (renders_dir / f"{vname}_cues.json").write_text(json.dumps(scaled_cues, indent=1))
        duration = get_duration(final)
        print(f"  -> {final} ({duration:.1f}s)")

        burn_captions(vname, final, scaled_cues, renders_dir)


def burn_captions(vname, final_path, cue_words, renders_dir):
    cues = words_to_captions(cue_words)
    ass_path = renders_dir / f"{vname}_captions.ass"
    write_ass(cues, ass_path)
    captioned = renders_dir / f"{vname}_captioned.mp4"
    fonts_dir = str(Path(CAPTION_FONT_FILE).parent)
    sh(
        f'ffmpeg -y -v error -i "{final_path}" '
        f'-vf "ass=\'{ass_path}\':fontsdir=\'{fonts_dir}\'" '
        f'-c:v libx264 -crf 17 -preset medium -c:a copy -movflags +faststart "{captioned}"'
    )
    print(f"  -> {captioned} (captions burned in)")


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
