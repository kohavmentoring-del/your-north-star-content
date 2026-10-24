# Setup (first run)

Check what's already there before installing anything. **Ask the creator before every install**, and tell them in one line what it's for and roughly how big it is. Never use `sudo` without asking.

## What the skill needs

| Tool | For | Size |
|---|---|---|
| ffmpeg | every cut, render and export | ~100 MB |
| whisper + a speech model | transcripts with word timing | ~600 MB on Mac (whisper.cpp), ~1.5 GB on Windows (faster-whisper) |
| Python 3 | the toolkit scripts and review server | usually already there on a Mac |
| Playwright + Chromium | captions, titles and graphics (rendered from HTML) | ~700 MB |

Plus free disk space while editing: roughly 5-10 GB per short project, more for 4K long-form.

## Check

System Python is `python3` on a Mac and `python` (or `py`) on Windows.

```bash
ffmpeg -version | head -1
which whisper-cli
python3 --version
ffmpeg -hide_banner -filters | grep -E " (colortemperature|perspective|loudnorm|zscale) "
df -h .
```

`colortemperature`, `perspective` and `loudnorm` must be there. `zscale` is only needed for HDR footage.

## The toolkit's Python (`PY`)

Everything Python-side goes in a virtual environment inside `_style/tools/`, so nothing touches the system Python and every later session uses the same one. Create it once:

```bash
python3 -m venv _style/tools/.venv          # Windows: python -m venv _style/tools/.venv
```

From then on, `PY` means:
- Mac: `_style/tools/.venv/bin/python`
- Windows: `_style/tools/.venv/Scripts/python.exe`

Check it with `PY -c "import playwright; print('playwright ok')"`.

## Install: Mac

1. **Homebrew** (if `brew` is missing): the creator runs the one-line installer from brew.sh themselves, since it asks for their password.
2. `brew install ffmpeg whisper-cpp`
3. Whisper model:
   ```bash
   mkdir -p ~/whisper-models
   curl -L -o ~/whisper-models/ggml-large-v3-turbo-q5_0.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
   ```
4. Playwright:
   ```bash
   _style/tools/.venv/bin/pip install playwright pillow
   _style/tools/.venv/bin/python -m playwright install chromium
   ```

## Install: Windows

1. `winget install Gyan.FFmpeg` and, if Python is missing, `winget install Python.Python.3.12`. Then the creator closes and reopens Claude (or their terminal) so the new commands are found.
2. Create the venv (above), then:
   ```bash
   _style/tools/.venv/Scripts/pip install faster-whisper playwright pillow
   _style/tools/.venv/Scripts/python -m playwright install chromium
   ```
3. faster-whisper downloads its model on first use. On a slow PC, use the `small` model for speed and check words more carefully.

Use forward slashes and quote every path (clip names often have spaces). Forward slashes work in both bash and PowerShell.

## Fonts

Download the fonts the look needs into `_style/fonts/` from Google Fonts (Inter, Instrument Serif, Roboto Mono, or whatever MY-STYLE.md names). Inter is one variable font: its "Display" look is optical size 32 (`font-variation-settings: "opsz" 32`). If the creator has brand fonts, ask them to drop the files in that folder. Only use fonts they have the right to use.

## Speed expectations to tell them

On a recent Mac: transcription ~1 minute per 5 minutes of footage; a styled render ~3-10 minutes per minute of video. Older or Windows machines can be 2-4 times slower. Run long steps in the background and say how long to expect.
