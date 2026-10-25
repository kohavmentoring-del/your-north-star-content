import json

shots = json.load(open("_edit/shots.json"))
beats = json.load(open("_edit/beats.json"))
captions = json.load(open("_edit/captions.json"))

TOTAL_DUR = round(shots[-1]["final_start"] + shots[-1]["dur"] + 0.3, 2)

DEVICE = {
    "A": {"scale": 1.0, "x": 0, "y": 0},
    "B": {"scale": 1.22, "x": 0, "y": -20},
    "C": {"scale": 1.12, "x": 60, "y": 0},
}

CARDS = [
    {"line": "1", "type": "note", "text": "60 DAYS LEFT", "image": "line1-calendar-pad.png",
     "side": "right", "beat_index": 0, "offset": 0.15, "dur": 2.4},
    {"line": "2", "type": "search", "text": "how do you learn to fail?", "image": "line2-walking.png",
     "side": "left", "beat_index": 0, "offset": 0.15, "dur": 2.6},
    {"line": "3", "type": "quote", "text": "failing = succeeding?", "image": "line3-matcha.png",
     "side": "right", "beat_index": 0, "offset": 0.15, "dur": 2.4},
    {"line": "3", "type": "photo", "text": "", "image": "line3-running.png",
     "side": "left", "beat_index": 2, "offset": 0.15, "dur": 2.3},
    {"line": "5", "type": "note", "text": "NEW YORK CITY.\\nstarting from scratch.", "image": "line5-nyc-street.png",
     "side": "right", "beat_index": 0, "offset": 0.15, "dur": 2.6},
    {"line": "6", "type": "search", "text": "is it normal to start over at 26?", "image": "line6-toronto-generic.png",
     "side": "left", "beat_index": 0, "offset": 0.15, "dur": 2.8},
    {"line": "7", "type": "quote", "text": "it's okay to fail.", "image": "line7-berries.png",
     "side": "right", "beat_index": 0, "offset": 0.15, "dur": 2.6},
]

FULLSCREEN = [
    {"line": "4", "beat_index": 1, "image": "line4-diamond.png", "kicker": "", "title": "a second before\\nthe diamonds"},
    {"line": "8-9", "beat_index": 0, "image": None, "kicker": "EPISODE 1", "title": "Attempting\\nto Suck"},
]

line_beats = {}
for b in beats:
    line_beats.setdefault(b["line"], []).append(b)
for ln in line_beats:
    line_beats[ln].sort(key=lambda b: b["final_start"])

line_shot = {s["line"]: s for s in shots}

SIDE_X = {"left": 40, "right": 700}
CARD_W, CARD_H = 340, 420
TILT = {"left": -5, "right": 5}

# ----------------- compute full-screen absolute windows (for hiding captions/video) -----------------
fullscreen_windows = []
for fs in FULLSCREEN:
    b = line_beats[fs["line"]][fs["beat_index"]]
    fullscreen_windows.append((b["final_start"], b["final_start"] + b["dur"]))


def overlaps_fullscreen(t0, t1):
    for ws, we in fullscreen_windows:
        if t0 < we and t1 > ws:
            return True
    return False


# ===================== index.html =====================
index_html = f'''<html>
  <body>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{TOTAL_DUR}"
      data-width="1080"
      data-height="1920"
    >
      <div
        id="talkinghead"
        data-composition-id="talkinghead"
        data-composition-src="compositions/talkinghead.html"
        data-start="0"
        data-duration="{TOTAL_DUR}"
        data-track-index="1"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
      <div
        id="cards"
        data-composition-id="cards"
        data-composition-src="compositions/cards.html"
        data-start="0"
        data-duration="{TOTAL_DUR}"
        data-track-index="2"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
      <div
        id="captions"
        data-composition-id="captions"
        data-composition-src="compositions/captions.html"
        data-start="0"
        data-duration="{TOTAL_DUR}"
        data-track-index="3"
        data-track-kind="captions"
        data-width="1080"
        data-height="1920"
      ></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open("hf-project/index.html", "w").write(index_html)
print("wrote index.html")

# ===================== compositions/talkinghead.html =====================
video_divs = []
zoom_tweens = []
for sh in shots:
    name = sh["_name"]
    start = sh["final_start"]
    dur = sh["dur"]
    line = sh["line"]

    video_divs.append(f'''
    <div id="wrap-{name}" class="shot-wrap" style="position:absolute;inset:0;overflow:hidden">
      <video id="{name}" class="clip" data-start="{start}" data-duration="{dur}" data-track-index="1"
        src="assets/{name}.mp4" playsinline data-has-audio="true"
        style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover"></video>
    </div>''')

    shot_beats = [b for b in line_beats[line] if start - 0.01 <= b["final_start"] < start + dur - 0.01]
    for b in shot_beats:
        local_t = round(b["final_start"] - start, 3)
        dev = DEVICE[b["device"]]
        zoom_tweens.append(
            f'tl.set("#wrap-{name}", {{ scale: {dev["scale"]}, x: {dev["x"]}, y: {dev["y"]} }}, {start + local_t});'
        )

talkinghead_html = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; background: #000; overflow: hidden; }}
    .shot-wrap {{ transform-origin: center center; }}
  </style>
  <div id="root" data-composition-id="talkinghead" data-width="1080" data-height="1920">
    {''.join(video_divs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + t for t in zoom_tweens)}
    window.__timelines["talkinghead"] = tl;
  </script>
</template>
'''
open("hf-project/compositions/talkinghead.html", "w").write(talkinghead_html)
print("wrote talkinghead.html with", len(shots), "shots,", len(zoom_tweens), "zoom beats")

# ===================== compositions/cards.html =====================
card_divs = []
card_tweens = []

for i, c in enumerate(CARDS):
    b = line_beats[c["line"]][c["beat_index"]]
    start = round(b["final_start"] + c["offset"], 3)
    dur = c["dur"]
    cid = f"card-{i}"
    side = c["side"]
    x = SIDE_X[side]
    tilt = TILT[side]
    # vertical slot: alternate upper/lower mid-band to avoid stacking identical spots
    y = 360 if i % 2 == 0 else 760

    label_font = "Montserrat" if c["type"] in ("search", "label") else "Playfair Display"
    label_style = "font-style:italic;font-weight:600;" if label_font == "Playfair Display" else "font-weight:800;"
    text_html = ""
    if c["text"]:
        lines_html = "<br>".join(c["text"].split("\\n"))
        if c["type"] == "search":
            text_html = f'''
        <div class="search-bar">
          <span class="search-icon">&#128269;</span>
          <span class="search-text">{lines_html}</span>
        </div>'''
        else:
            text_html = f'<div class="card-text">{lines_html}</div>'

    card_divs.append(f'''
    <div id="{cid}" class="clip wall-card side-{side}" data-start="{start}" data-duration="{dur}" data-track-index="1"
      style="position:absolute; left:{x}px; top:{y}px; width:{CARD_W}px;">
      <div id="{cid}-inner" class="card-anim" style="opacity:0;">
        <div class="card-inner" style="transform:rotate({tilt}deg);">
          <img src="assets/images/{c['image']}" class="card-photo" />
          {text_html}
        </div>
      </div>
    </div>''')

    card_tweens.append(f'''
    tl.fromTo("#{cid}-inner", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {start});
    tl.to("#{cid}-inner", {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, {start + dur - 0.35});
    tl.set("#{cid}-inner", {{ opacity: 0 }}, {start + dur});''')

# full-screen moments
full_divs = []
full_tweens = []
for i, fs in enumerate(FULLSCREEN):
    b = line_beats[fs["line"]][fs["beat_index"]]
    start = b["final_start"]
    dur = b["dur"]
    fid = f"full-{i}"
    img_html = f'<img src="assets/images/{fs["image"]}" class="full-photo" />' if fs["image"] else '<div class="full-bg"></div>'
    kicker_html = f'<div class="full-kicker">{fs["kicker"]}</div>' if fs["kicker"] else ""
    title_lines = "<br>".join(fs["title"].split("\\n"))
    full_divs.append(f'''
    <div id="{fid}" class="clip full-screen" data-start="{start}" data-duration="{dur}" data-track-index="2"
      style="position:absolute;inset:0;">
      <div id="{fid}-inner" class="full-anim" style="position:absolute;inset:0;opacity:0;">
        {img_html}
        <div class="full-scrim"></div>
        <div class="full-text-wrap">
          {kicker_html}
          <div class="full-title">{title_lines}</div>
        </div>
      </div>
    </div>''')
    full_tweens.append(f'''
    tl.fromTo("#{fid}-inner", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {start});
    tl.to("#{fid}-inner", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {start + dur - 0.3});
    tl.set("#{fid}-inner", {{ opacity: 0 }}, {start + dur});
    tl.fromTo("#{fid}-inner .full-photo", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {dur}, ease: "none" }}, {start});''')

cards_html = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: visible; }}
    @font-face {{ font-family: "Montserrat ExtraBold"; src: local("Montserrat"); }}
    .wall-card {{ filter: drop-shadow(0 8px 20px rgba(0,0,0,0.45)); }}
    .card-inner {{ background: #F6ECDD; border: 6px solid #fff; border-radius: 4px; padding: 14px; box-sizing: border-box; }}
    .card-photo {{ width: 100%; height: 220px; object-fit: cover; border-radius: 2px; display: block; }}
    .card-text {{ font-family: "Playfair Display"; font-style: italic; font-weight: 600; font-size: 34px;
      color: #6B1A2A; margin-top: 10px; line-height: 1.2; text-align: center; }}
    .search-bar {{ margin-top: 10px; background: #fff; border: 2px solid #C9A07A; border-radius: 24px;
      padding: 10px 16px; display: flex; align-items: center; gap: 8px; }}
    .search-icon {{ font-size: 20px; }}
    .search-text {{ font-family: "Montserrat"; font-weight: 700; font-size: 22px; color: #24160F; }}
    .full-screen {{ background: #000; }}
    .full-photo {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transform-origin: center center; }}
    .full-bg {{ position: absolute; inset: 0; background: linear-gradient(160deg, #6B1A2A, #24160F); }}
    .full-scrim {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,.15) 0%, rgba(0,0,0,.55) 100%); }}
    .full-text-wrap {{ position: absolute; left: 0; right: 0; top: 760px; text-align: center; padding: 0 80px; }}
    .full-kicker {{ font-family: "Montserrat"; font-weight: 800; letter-spacing: 6px; font-size: 28px; color: #F6B511; margin-bottom: 18px; }}
    .full-title {{ font-family: "Playfair Display"; font-style: italic; font-weight: 600; font-size: 74px; color: #F6ECDD; line-height: 1.15; }}
  </style>
  <div id="root" data-composition-id="cards" data-width="1080" data-height="1920">
    {''.join(card_divs)}
    {''.join(full_divs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + t for t in card_tweens)}
    {chr(10).join('    ' + t for t in full_tweens)}
    window.__timelines["cards"] = tl;
  </script>
</template>
'''
open("hf-project/compositions/cards.html", "w").write(cards_html)
print("wrote cards.html with", len(CARDS), "cards,", len(FULLSCREEN), "fullscreen moments")

# ===================== compositions/captions.html =====================
cap_divs = []
cap_tweens = []
kept = 0
for i, c in enumerate(captions):
    start, end = c["start"], c["end"]
    if overlaps_fullscreen(start, end):
        continue
    start = max(start, 0.08) if start < 0.08 else start  # never start at exactly 0
    dur = max(0.35, end - start)
    cid = f"cap-{i}"
    cap_divs.append(f'''
    <div id="{cid}" class="clip caption-group" data-start="{start}" data-duration="{dur}" data-track-index="1"
      style="position:absolute; left:0; right:0; top:1280px;">
      <div id="{cid}-inner" class="caption-anim" style="opacity:0;">
        <div class="caption-text">{c["text"]}</div>
      </div>
    </div>''')
    cap_tweens.append(f'''
    tl.fromTo("#{cid}-inner", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "power1.out" }}, {start});
    tl.to("#{cid}-inner", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {start + dur - 0.12});
    tl.set("#{cid}-inner", {{ opacity: 0, visibility: "hidden" }}, {start + dur});''')
    kept += 1

captions_html = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: visible; }}
    .caption-text {{ font-family: "Montserrat"; font-weight: 800; font-size: 64px; color: #6B1A2A;
      text-align: center; line-height: 1.15; letter-spacing: -0.5px;
      text-shadow: 0 2px 10px rgba(246,236,221,0.35); padding: 0 90px; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-track-kind="captions">
    {''.join(cap_divs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + t for t in cap_tweens)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open("hf-project/compositions/captions.html", "w").write(captions_html)
print("wrote captions.html with", kept, "of", len(captions), "groups (skipped during full-screen moments)")
