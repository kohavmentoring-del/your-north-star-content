import json, subprocess

shots = json.load(open("_edit/shots.json"))
src = "IMG_0341.MOV"
out_dir = "hf-project/assets"

# number shots sequentially within each line (handles line1's 2 shots)
counts = {}
for sh in shots:
    line = sh["line"]
    counts[line] = counts.get(line, 0) + 1
    idx = counts[line]
    name = f"shot-line{line}" + (f"-{idx}" if counts[line] > 1 or any(
        s["line"] == line for s in shots if s is not sh and shots.index(s) != shots.index(sh)
    ) else "")

# simpler: just index every shot sequentially, keep line id in filename
seen = {}
for sh in shots:
    line = sh["line"]
    seen[line] = seen.get(line, 0) + 1
    suffix = f"-{seen[line]}" if seen[line] > 1 else ""
    sh["_name"] = f"shot-line{line}{suffix}"

# second pass: if a line only ever had 1 shot, suffix stays empty; if >1, add suffix to ALL its shots
line_total = {}
for sh in shots:
    line_total[sh["line"]] = line_total.get(sh["line"], 0) + 1
seen = {}
for sh in shots:
    line = sh["line"]
    seen[line] = seen.get(line, 0) + 1
    if line_total[line] > 1:
        sh["_name"] = f"shot-line{line}-{seen[line]}"
    else:
        sh["_name"] = f"shot-line{line}"

for sh in shots:
    s, e, name = sh["src_start"], sh["src_end"], sh["_name"]
    dur = e - s
    out_path = f"{out_dir}/{name}.mp4"
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-ss", str(s), "-i", src, "-t", str(dur),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30",
        "-g", "10", "-c:v", "libx264", "-crf", "16", "-preset", "fast",
        "-c:a", "aac", "-b:a", "256k", out_path,
    ]
    print("extracting", name, dur)
    subprocess.run(cmd, check=True)

json.dump(shots, open("_edit/shots.json", "w"), indent=1)
print("done")
