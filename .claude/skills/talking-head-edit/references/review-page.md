# The review page and the graphics board

The creator gives notes per line and per graphic. These two local pages are how they do it. Build them once into the toolkit and regenerate them on every render.

## The local server

A small Python server (`vid.py serve`) on `127.0.0.1`, port 8765 (try the next port if it's busy), serving the project's `_edit/` folder.

It must:
- **Support HTTP Range requests** (reply `206 Partial Content` with `Content-Range`). Python's built-in `http.server` doesn't, and without it videos won't seek, so ▶ on a line plays from the wrong spot or not at all.
- Accept `POST /feedback` and `POST /board` and write the JSON body to `_edit/feedback.json` / `_edit/board_feedback.json` with a `saved_at` time.
- Send `Cache-Control: no-store` for `.html`, and add `?v=<file modified time>` to every video URL in the page, so a re-render shows up on refresh instead of the old cached file.

Run it in the background. Open the page in the browser pane if you have one; otherwise give the creator the URL.

## The review page (`_edit/review.html`)

**Tabs along the top:** one per version, labeled with its name and length ("Recommended · 1:24"). Archived versions sit in a smaller Archive row.

**A cut version's tab:**
- The rendered cut in a player (vertical, phone-sized).
- The version's one-line blurb.
- Every line in order: line id, section label when one starts ("Hook", "Story"), the text, its length. Lines you flagged as optional are highlighted with your reason.
- Per line: **▶** (plays just that line in the cut), **Cut**, **Speed up**, and a notes field.
- Below the kept lines, the lines that aren't in this version, each with **▶** (plays it from a low-res proxy of the source clip) and **Add back**.
- A live length at the top that updates as they mark Cut / Speed up / Add back, so they see "1:24 → 1:09" before you re-render.
- A general notes box at the bottom.

**A styled version's tab:**
- The styled render in the player.
- Every style element as a row in time order (hook title, each graphic, each punch-in with the words it covers, each B-roll clip): **▶** jumps to it, plus Keep / Change and notes.
- If you remastered the voice: a before/after pair of short clips.

**Saving:** every change saves as they type (debounced), to `localStorage` and by `POST /feedback`. Structure the JSON by version, then by line id or element: `{ "rec": { "lines": { "2.05": { "mark": "speed", "note": "drags" } }, "general": "..." } }`. Expose `window.reviewState()` returning the same object, so you can read it from the browser if the server was down.

**Reading it:** `vid.py feedback` prints, per version, each marked line with its mark and note, notes-only lines, and the general box. Don't make them tell you they're done; check `feedback.json` when they say they've reviewed.

## The graphics board (`_edit/board.html`)

Before the full styled render, whenever a graphic type or image is new to this creator:
- One card per proposed graphic: a still of the overlay at that moment composited over a real frame from the cut, labeled with the line it sits on ("2.05 'I quit my job'"), and **▶** that plays that moment of the cut with the still on top.
- Where you have alternatives (two title wordings, two fonts, two photo choices), a "Pick one" row of options side by side.
- Per card: **Keep / Change / Cut** and notes.
- Saves by `POST /board` the same way.

## Design

Plain and fast: system fonts, light background, the video big enough to judge on a laptop. Buttons large enough to tap. It's a work tool, not a showcase.
