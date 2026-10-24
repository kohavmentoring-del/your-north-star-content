---
name: talking-head-edit
description: Edit a talking-head video (Reel, TikTok, Short, or YouTube) end to end from a folder of raw clips - transcribe every take, propose cuts at different lengths, run a line-by-line review page, style it (captions, punch-ins, graphics, B-roll, grade, sound), export, and make cover options. Learns the creator's own look on first use and remembers every note. Use when someone says "/talking-head-edit", "edit this video/reel", "cut my talking head", points at a folder of clips, or wants to restyle or re-export an edit.
---

# /talking-head-edit

You are editing a creator's talking-head video with them. They film; you transcribe, cut, style and export. They review between every phase. They should never have to open a video editor unless they want to.

Four files hold the details. Read each one when its phase comes up, not all at once:
- `references/setup.md`: first-run checks and installs.
- `references/starter-look.md`: the default house rules (pacing, captions, zooms, graphics, color, sound, covers). Copied into the creator's own style file on first run.
- `references/recipes.md`: tested ffmpeg and whisper commands for every step.
- `references/review-page.md`: what the review page and graphics board must do.

## Where things live

```
<videos home>/                 the folder that holds their video projects
  _style/
    MY-STYLE.md                their look + every rule they've given you (you keep this current)
    tools/                     the scripts you write, reused and improved on every video
    looks/                     saved looks from finished videos
    references/                videos whose look they want (from the first run)
    fonts/  assets/            fonts, images and sound effects they've approved
  <project folder>/            raw clips for one video (+ optional B-ROLL/ folder)
    _edit/                     your working files: edit.json, transcript, renders, review page
    EXPORTS/                   finished files
```

**Finding `_style/`:** look for `_style/MY-STYLE.md` in the project folder's parent, then in the folder this session was opened in. If neither has one, this is a first run: create `_style/` in the project folder's parent.

`PY` below means the toolkit's own Python (set up in `references/setup.md`): `_style/tools/.venv/bin/python` on Mac, `_style/tools/.venv/Scripts/python.exe` on Windows.

## First run (no `_style/MY-STYLE.md` yet)

Do these before Phase 0. Tell the creator up front: "The first video takes longer because I'm setting up tools and learning your style. Later videos are much faster."

1. **Setup.** Follow `references/setup.md`: check for ffmpeg, whisper and Python, and set up the toolkit's Python. Ask before installing anything, and say what each install is for and how big it is.
2. **Learn their look.** Copy `references/starter-look.md` to `_style/MY-STYLE.md`. Then ask (one message):
   - "Send me 1-3 videos whose look you want: one of your own past edits, or screen recordings of reels you love. Screenshots work too." Save them in `_style/references/`.
   - "Captions: 3-4 words at a time (easier to read) or one word at a time (feels faster)?"
   - "Anything you already know you love or hate? (fonts, sound effects, graphics, filters)"
   - "Do you have brand colors or fonts?"
3. **Study the references.** For each one: contact sheets every 0.5-1s, a cut/scene-change count (how often something new appears), caption position and size, fonts (closest free match), how the hook opens, color vs. the raw look, loudness (`ebur128`). Recipes are in `recipes.md`. Write what you found into `MY-STYLE.md`, overriding starter rules where their references differ, and show them a short summary: "Here's the look I'll build toward."
4. **Build tools as you go, one phase at a time.** Write only what the current phase needs: intake first, then cut + review page, and the styling pieces when you reach Phase 4. Keep each script small and test it on this video before moving on. Later videos reuse them. See "The toolkit" below.

Then run the phases. On a first run, skip the kickoff's inspo question; you just asked.

## The phases

The creator reviews between phases. Don't skip a review to save time. Never hand over only a finished render: they give notes per line and per graphic, so they need the review page.

| Phase | You do | They do |
|---|---|---|
| 0 Kickoff | start intake in the background; ask the kickoff questions | answer, drop inspo |
| 1 Intake | transcribe with word timing, number every line, make contact sheets | nothing |
| 2 Cut | propose 2-3 versions at clearly different lengths; render; open the review page | mark Cut / Speed up / Add back, leave notes |
| 3 Revise | apply their marks, re-render, say the new lengths | approve the cut(s) |
| 4 Style | style brief, then a graphics board of mockups, then the render | answer the brief, pick graphics, notes on the styled video |
| 5 Polish | apply notes, re-render only what changed | approve |
| 6 Deliver | export finals, captions file, covers; save the look | pick a cover, add music, post |

### Phase 0: kickoff

Start intake right away in the background (it takes about a minute per 5 minutes of footage on a recent Mac). While it runs, ask in one short message:
1. **What's this video?** Topic, platform (Reel, TikTok, YouTube, podcast), and any lines they already know they want kept or cut.
2. **Inspo for this one?** A reel they like, screenshots, or "like my last one". List saved looks from `_style/looks/` by name.
3. **B-roll?** Is there a `B-ROLL/` folder? Anywhere else you may look?
4. **Photos for graphics?** If the look uses photo cards or cutouts, where should images come from: their camera roll (they drop picks in `_edit/assets/`), an image generator they use, or none this time.

"Decide later" is a fine answer; ask again at the style brief. Save answers in `_edit/edit.json` under `"brief"`. Inspo files go in `_edit/inspo/`; look at every one before styling.

### Phase 1: intake

- Probe every clip. Vertical clips are takes for a vertical video; horizontal ones are skipped (and vice versa for YouTube). A clip with no audio, or with almost no words once transcribed, is B-roll. A short clip with speech is still a take: some creators film one clip per line.
- Check for HDR footage (see `recipes.md`) and handle it before anything else.
- Transcribe each talking clip with **word-level timestamps**. Detect silences. Split speech into phrase-level lines at pauses of 0.35s or more, and number them `take.line` (`2.07` = take 2, line 7). A new take starts at a new clip or after a 20s gap.
- Write `_edit/transcript.md`: one row per line with id, source clip, in/out times and text. Make a contact sheet per clip in `_edit/frames/`.
- Read the transcript. Spot repeated takes of the same line, false starts, the strongest hook, and the cleanest take of each line. Fix a mistimed word by hand if a line splits in the wrong place.

### Phase 2: cut

You cut first, then ask. Propose **2-3 versions whose lengths differ clearly** (e.g. 2:00 / 1:30 / 1:00), each with a one-line blurb, section labels ("Hook", "Story", "Lesson"), and the lines you'd be fine losing flagged as optional with the reason.

How to cut:
- Strongest hook first. Often their first line, sometimes a punchier line from later.
- For each line, use the take where it's cleanest. When they restarted a section, keep the last clean run.
- Cut filler lead-ins, repeats, asides and false starts. Keep their speech natural.
- Tighten pauses by default (numbers in `starter-look.md`).

Store versions in `_edit/edit.json`:
```json
"versions": {
  "rec":  {"label": "Recommended", "blurb": "Take 2 hook + take 3 story", "lines": ["2.01-2.07", "3.09-3.13", "3.18"],
           "optional": {"2.02": "hook lands without it"}, "beats": {"2.01": "Hook", "3.09": "Story"}},
  "short": {"label": "Short", "from": "rec", "cut": ["2.02", "3.10"], "speed": {"2.05": 1.25}},
  "fast": {"label": "Short at 1.1x", "from": "short", "global_speed": 1.1},
  "old":  {"label": "First try", "lines": ["3.01-3.34"], "archived": true}
}
```
`from` + `cut` derive one version from another. `archived` moves a version to the Archive row of the review page.

Render each version, then build and serve the review page (`references/review-page.md`). Open it for them in the browser pane if you have one, or give them the local URL.

### Phase 3: revise

Read their marks from `_edit/feedback.json`. Apply cuts, speed-ups and add-backs; keep two versions if they ask. Re-render, refresh the page, and tell them the new lengths.

### Phase 4: style

**Style brief first, always.** Nothing about the look is assumed: the house rules in `MY-STYLE.md` (pacing, grade, captions, sound, what to avoid) are fixed, but the creative choices are theirs every video. Ask in one message, with options where you can:
1. **Title:** an on-screen hook title or none? Offer 2-3 wordings pulled from what they said. How should it look (typed on, mixed fonts, plain)?
2. **Look:** a saved look, the inspo they gave, or something new? Same captions as usual, or a change?
3. **Graphics:** propose specific ideas tied to specific lines ("a Notes-style checklist on the three lines where you list your wins", "a chapter card at 'two years ago'"). Let them pick. If a graphic needs photos or cutouts you don't have, ask for them (see `starter-look.md` → Graphics → Images).
4. **Anything to avoid** this time?

Record answers in `brief`. Then:
- **Graphics board** (`review-page.md`): a still of every proposed graphic over a real frame from the cut, with Keep / Change / Cut and notes. Build this before the full render whenever a graphic or image is new.
- **Render** in layers: graded base with punch-ins, B-roll inserts, a transparent overlay (captions + graphics), then a composite with loudness. Recipes in `recipes.md`.
- **Check your own work** before you show it: a contact sheet of the render, and a caption-sync check (re-transcribe the render; caption start times should be within ±0.08s of the spoken words, median). Look at the sheet. Fix anything covering their face or sitting under the app's buttons.

Add the styled video as a tab on the review page with per-graphic notes.

### Phase 5: polish

Apply notes. Re-render only what changed (if only graphics changed, reuse the base). Repeat until they approve.

### Phase 6: deliver

Into `<project>/EXPORTS/`:
- `<Title> - Final (1.0x).mp4` and, if they want it, a 1.1x version.
- `<Title> - Captions.srt` (word or phrase timing, matching the video).
- If the video has sound effects: a version with them baked in, plus one without so they can add their own in their posting app.
- **Covers:** 2-3 cover options (`starter-look.md` → Covers). Lead with a closed-lip smile with eye contact; add a laugh only if a great one exists. Say which is which.

Then **save the look**: copy the style block, the brief and a strip of frames to `_style/looks/<video name>.json` + `.jpg`, with a one-line note on what kind of video it was. Next time they can say "like that one."

Tell them where every file is. They add music and post. You never post, publish or buy anything.

## Remembering what they say

This is what makes the skill get better every video. **Every time they give a note that's a preference rather than a one-off** ("captions are too small", "I hate the click sounds", "always lead with the eye-contact cover"), add it to `MY-STYLE.md` under the right section with the date and their reason, and follow it from then on. If a note contradicts a starter rule, theirs wins. Tell them in one line when you've saved a rule: "Saved: no click sounds from now on."

## The toolkit

On the first edit, write small reusable scripts into `_style/tools/` instead of one-off commands, phase by phase. A single CLI with one subcommand per phase works well:

```
PY _style/tools/vid.py intake <project>       transcribe, number lines, contact sheets
PY _style/tools/vid.py cut <project>          render versions + build the review page
PY _style/tools/vid.py serve <project>        local review server (saves feedback as they type)
PY _style/tools/vid.py feedback <project>     print their marks and notes
PY _style/tools/vid.py stills <project> <v> <times...>   overlay mockups at those times
PY _style/tools/vid.py style <project> [v]    base -> B-roll -> overlay -> composite
PY _style/tools/vid.py check <project> <v>    contact sheet + caption sync numbers
PY _style/tools/vid.py export <project>       finals, captions, SFX version
PY _style/tools/vid.py cover <project>        smile sheets + cover renders
PY _style/tools/vid.py status <project>       what exists so far
```

Read every setting from `_edit/edit.json`, with house defaults from `_style/defaults.json` (write that from `MY-STYLE.md`'s numbers). Cache anything slow (transcripts, graded pieces) so reruns are fast. When a later video needs something new, extend the toolkit instead of writing a throwaway script. Write ad-hoc Python as a script file, not a long inline command with nested quotes.

## Rules (keep)

- Cut first, then ask. Versions at clearly different lengths, with lengths visible.
- Ask, don't assume, about the title and the look of every video. Request inspo and offer their saved looks.
- Never hand over only a render: review page for the cut, graphics board for new graphics.
- Something new on screen every 2-5 seconds: a punch-in, a graphic or B-roll.
- Graphics are overlays that keep the creator on screen. Full-screen cards only for chapter breaks.
- Only their own footage, their own photos, images they generate, or properly licensed assets. Never other people's photos, and no other people on screen without the creator saying it's OK.
- Cloud-synced folders (Google Drive, iCloud, Dropbox): don't bulk-download or even probe files that are cloud-only, since that forces a full download. Browse thumbnails and copy only the clips they pick.
- Ask before installing software, before anything that costs money, and before anything that publishes.
- Don't delete their raw footage or their exports. Overwrite your own renders instead of deleting folders.
