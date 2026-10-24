# Recipes

Tested commands for each step. `W×H` is the output size (1080×1920 vertical, 1920×1080 wide), `FPS` is 30 unless the creator wants otherwise. `ACODEC` is `aac_at` on a Mac (Apple's encoder, cleaner peaks) and `aac` elsewhere. `PY` is the toolkit's Python from `setup.md`. Other UPPERCASE names and `(expressions)` are values your script computes and fills in. Use forward slashes in paths (they work on Windows too) and quote every path, since clip and folder names often have spaces. Wrap these in the toolkit scripts rather than typing them each time.

## Probe a clip

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,color_transfer:stream_side_data=rotation \
  -show_entries format=duration -of json clip.mov
```

- Phones store vertical video as a wide stream plus a rotation (e.g. 3840×2160 with rotation -90). ffmpeg rotates automatically, so treat that clip as vertical.
- No audio stream, or almost no words after transcription → B-roll, not a take. Don't judge by length alone: a 6-second clip of one spoken line is a take.

## HDR check

If `color_transfer` is `arib-std-b67` (HLG) or `smpte2084` (PQ), the clip is HDR (most iPhones record this by default). A plain conversion can look washed out or oddly saturated. If `ffmpeg -filters | grep zscale` finds zscale, tone-map to SDR first:

```
zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p
```

If zscale isn't available, render one test frame each way and show the creator. For future shoots, they can turn HDR off (iPhone: Settings → Camera → Record Video → HDR Video).

## Audio for transcription

```bash
ffmpeg -i clip.mov -vn -ac 1 -ar 16000 -c:a pcm_s16le _edit/audio/clip.wav
```

## Transcribe with word timing

**whisper.cpp (Mac, fastest):**
```bash
whisper-cli -m ~/whisper-models/ggml-large-v3-turbo-q5_0.bin -f _edit/audio/clip.wav -l en \
  -ojf -of _edit/transcripts/clip -t 8 -nfa --dtw large.v3.turbo \
  --prompt "Um, uh, like, you know. So, I mean, okay."
```
- `-ojf` writes full JSON with per-token timing. Word start = token `t_dtw / 100` seconds. Tokens whose text starts with a space begin a new word; others attach to the previous word. Skip tokens starting with `[_` or with `t_dtw < 0`.
- `-nfa` is required: flash attention silently disables DTW word timing.
- The prompt keeps "um"s and "like"s in the transcript, so you can see and cut them.
- On long clips with many retakes, whisper can get stuck repeating one line for minutes. If 6+ identical segments appear in a row, rerun with `-mc 0` added.
- Set `-l` to the creator's language.

**faster-whisper (Windows / Linux, or if whisper.cpp won't install):**
```python
from faster_whisper import WhisperModel
m = WhisperModel("large-v3-turbo", compute_type="int8")
segs, _ = m.transcribe("clip.wav", word_timestamps=True, initial_prompt="Um, uh, like, you know. So, I mean, okay.")
words = [{"w": w.word.strip(), "t": w.start, "end": w.end} for s in segs for w in s.words]
```

Cache transcripts: never re-transcribe a clip that already has one.

## Silences

```bash
ffmpeg -hide_banner -i _edit/audio/clip.wav -af silencedetect=noise=-38dB:d=0.22 -f null - 2>&1 | grep silence_
```

Run it at `d=0.35` to split lines, and at `d=0.22` to find pauses to tighten. Use silences to correct word times: a word can't start inside a silence.

## Lines and the transcript

- Split each clip's words into lines at silences ≥ 0.35s. Number them `take.line` (`2.07`).
- A line's in/out = first word start to last word end (use silence edges, not the next word's start, for the out point).
- `_edit/transcript.md` gets one row per line: `2.07  IMG_1234  01:23.40-01:26.10  "and that's when it clicked"`.

## Contact sheets

```bash
ffmpeg -i clip.mov -vf "fps=1/2,scale=240:-2,tile=8x5" -q:v 3 _edit/frames/clip_%02d.jpg
```
One tile per 2 seconds, 40 tiles per sheet. Use `fps=2` and a smaller tile for scrubbing a short range.

## Cutting a version

Render each segment as its own piece, then join. For a segment from `S` to `E` of a clip at speed `SP`, output duration `D = (E - S) / SP`, frame count `N = round(D * FPS)`:

```bash
ffmpeg -ss S -i clip.mov -t (E-S) \
  -vf "scale=W:H:force_original_aspect_ratio=increase:flags=lanczos,crop=W:H,setpts=(PTS-STARTPTS)/SP,fps=FPS,format=yuv420p,tpad=stop_mode=clone:stop_duration=1,trim=end_frame=N" \
  -af "atempo=SP,afade=t=in:d=0.02,afade=t=out:st=(D-0.03):d=0.03,aresample=48000,apad,atrim=end_sample=round(D*48000)" \
  -c:v libx264 -crf 16 -preset fast -c:a pcm_s16le _edit/pieces/v_rec_007.mov
```

- `-ss` before `-i` is frame-accurate when re-encoding.
- **Keep pieces' audio as PCM** and encode AAC once over the joined file. AAC on every piece adds tiny gaps that drift out of sync over a long cut.
- **Don't use `-frames:v` to set a piece's length**: ffmpeg stops muxing and drops the end of the audio. The `tpad` + `trim` pair above locks video length; `apad` + `atrim` locks audio length.
- The 20-30ms fades stop clicks at every cut.
- Leave `atempo` out at speed 1.0. Add the grade (below) to the `-vf` chain for styled renders; review cuts can skip it.
- Render pieces 3-4 at a time in parallel. Cache them by their in/out/speed so re-cuts only render what changed.

Join:
```bash
printf "file '%s'\n" v_rec_*.mov > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c:v copy -c:a ACODEC -b:a 256k -movflags +faststart _edit/renders/v_rec.mp4
```

## Tightening pauses

Inside a kept line, for every silence ≥ `max_pause` (0.22s): end the segment `pad_out` (0.07s) after the last word before the silence, and start the next segment `pad_in` (0.05s) before the next word. Between lines, the same pads give a ~0.12s gap. This turns one line into several segments, which is fine.

## Grade

```
colortemperature=temperature=5400:mix=0.7,eq=contrast=1.07:brightness=-0.02:saturation=1.14:gamma=0.97
```
Put it after `fps=` in the piece's `-vf`. Grade B-roll with the same chain.

## Punch-ins and slow pushes

Smooth zooms anchored on a point `(CX, CY)` (the face, e.g. 540, 640 on 1080×1920), using `perspective` so movement is sub-pixel. `Z` is an expression of time `T = (in/FPS)` that equals 1 outside zooms:

```
perspective=x0='CX-CX/(Z)':y0='CY-CY/(Z)':x1='CX+(W-CX)/(Z)':y1='CY-CY/(Z)':x2='CX-CX/(Z)':y2='CY+(H-CY)/(Z)':x3='CX+(W-CX)/(Z)':y3='CY+(H-CY)/(Z)':interpolation=cubic:eval=frame
```

- Static punch-in from `a` to `b`: `Z = if(between(T,a,b),1.2,1)`.
- Slow push from `a` to `b`: `Z = if(between(T,a,b),1+0.18*(T-a)/(b-a),1)`.
- Nest `if()`s for several zooms. Apply to the graded base cut, before B-roll and overlay.
- Avoid `zoompan` for pushes: it rounds to whole pixels and judders.

## B-roll inserts

```bash
ffmpeg -ss SRC_IN -i broll.mov -t DUR -an \
  -vf "scale=W:H:force_original_aspect_ratio=increase:flags=lanczos,crop=W:H,fps=FPS,GRADE,format=yuv420p" \
  -c:v libx264 -crf 16 _edit/styled/broll_0.mp4
```
Overlay on the base at `t0`:
```
[2:v]setpts=PTS-STARTPTS+t0/TB[b0];[base][b0]overlay=eof_action=pass:enable='between(t,t0,t1)'[v1]
```
Time B-roll to words: start on the word it illustrates, end on a word boundary.

## Overlay layer (captions, titles, graphics)

Many ffmpeg builds have no `drawtext` or `subtitles` filter, and HTML gives far nicer type anyway. Build the overlay as an HTML page and render it frame by frame with Playwright (installed into `PY` by `setup.md`):

1. `_style/tools/overlay.html`: a W×H transparent page that loads a plan (captions with times, title lines, graphics with start/end and positions) and exposes `window.render(t)`, which sets **every** element's state from `t` alone. No running CSS transitions or timers. If you use CSS `@keyframes`, pause them and set `anim.currentTime` for each frame via `document.getAnimations()`.
2. Load fonts from `_style/fonts/` with `@font-face`, and wait for `document.fonts.ready` and every image's `decode()` before the first frame.
3. Render loop:
```python
from playwright.sync_api import sync_playwright
import subprocess
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-c:v", "png", "-framerate", str(FPS),
                       "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", "_edit/styled/overlay.mov"], stdin=subprocess.PIPE)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--font-render-hinting=none", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    pg.goto("file://" + overlay_html_path)
    pg.evaluate("plan => window.load(plan)", plan)
    pg.evaluate("document.fonts.ready.then(() => true)")
    for f in range(round(duration * FPS)):
        pg.evaluate("t => window.render(t)", f / FPS)
        ff.stdin.write(pg.screenshot(type="png", omit_background=True))
    b.close()
ff.stdin.close(); ff.wait()
```
4. **Stills for mockups:** call `render(t)` at a few times and save PNGs. Composite each over a real frame of the cut for the graphics board.

About 1-2 minutes of rendering per minute of video.

## Composite + loudness

```bash
ffmpeg -i base_zoomed.mov -i overlay.mov [-i broll_0.mp4 ...] -filter_complex \
 "[...B-roll overlays...][vN][1:v]overlay=format=auto,format=yuv420p[v];[0:a]acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-10.5:TP=-1.0:LRA=5,aresample=48000[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -c:a ACODEC -b:a 256k -movflags +faststart final.mp4
```
- Keep `aresample=48000` after `loudnorm`: loudnorm outputs 192kHz audio, which the AAC encoder refuses.
- Loudness target: `I=-10.5` short-form, `I=-14` YouTube, `I=-16` podcast.
- ffmpeg's own `aac` can overshoot peaks slightly; when `ACODEC` is `aac`, set `TP=-1.5`.
- Check the result: `ffmpeg -i final.mp4 -af ebur128 -f null - 2>&1 | tail -12`.

## Voice remaster (boxy phone audio)

Before the compressor/loudnorm, for voices that sound like they're in a small room:
```
highpass=f=85,equalizer=f=450:t=q:w=1.0:g=-6,equalizer=f=3000:t=q:w=0.8:g=2.5,equalizer=f=7000:t=q:w=1.5:g=-4,highshelf=f=11000:g=2,agate=threshold=0.005:ratio=2:range=0.25:attack=3:release=90:knee=4,acompressor=threshold=0.063:ratio=2.2:attack=6:release=90:knee=4
```
The 450Hz cut removes the "box", 3kHz adds clarity, 7kHz tames harsh "s" sounds, the gentle gate shortens room ring after phrases. Measure first (a spectrum of a few seconds of speech) and adjust the 450Hz cut to where their hump actually is. Always put before/after clips on the review page.

## Sound effects

- Use real sounds from `_style/assets/sfx/` (a keyboard-typing loop, a soft click) that the creator gave you: free library sounds or their own recordings. If there are none, ask, or skip sound effects. Synthesized typing sounds fake.
- Mix them in with `adelay` per hit and `amix`, about 12dB under the voice, after loudness on the voice:
```
[1:a]adelay=1200|1200,volume=0.25[s0];[voice][s0]amix=inputs=2:normalize=0:duration=first[a]
```
- Deliver one version with SFX baked in and one without.

## Checks

- **Contact sheet of the render:** grab frames at 6-8 moments (title, each graphic, B-roll, last line) and `hstack` them, then look at it.
- **Caption sync:** transcribe the finished render with word timing, match each caption word in order to the next heard copy of it within 1s, and report the median offset. Within ±0.08s is right; a consistent offset means a timing bug in the plan.
- **Loudness:** `ebur128` as above.

## Cover frames

1. Pull frames at 2fps from every talking clip into contact sheets with each tile's time noted.
2. Look at the sheets and pick real smiles (closed-lip with eye contact first, then laughs). Mid-word frames sneak in; skip them.
3. Scrub ±0.3s around each pick at 10fps and take the peak of the smile.
4. Grade the still the same as the video, then lay out the cover as an HTML page (W×H) with the still, the hook title in the video's fonts and 1-3 photo cards, and screenshot it with Playwright.
5. Render a "guides" copy with a dashed box from y 240 to 1680 (the profile-grid crop) to check everything important sits inside.

## Long-form and big files

- 20 minutes of 4K is hundreds of pieces: render in the background, 4 at a time, and tell the creator the wait.
- On a Mac, `-hwaccel videotoolbox` before `-i` speeds up decoding 4K.
- Check free disk space before copying anything big (`df -h`). Prefer symlinks to copies.
