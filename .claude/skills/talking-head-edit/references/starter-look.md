# Starter look for talking-head videos

These are the defaults a new creator starts from. On first run, copy this file to `<videos home>/_style/MY-STYLE.md`, then change it to match their reference videos and every note they give you. Their rules always win over these.

Each number below came from real edits and real feedback. The "why" is there so you know when it's safe to bend a rule.

---

## Structure of a short (Reel / TikTok / Short)

| Beat | What happens | How long |
|---|---|---|
| Hook | Their first line. Optional hook title on screen, optional photo cards around them | first line, 3-6s |
| Set-up | Why they're worth listening to. Overlay graphics that keep them on screen, B-roll of their life | 10-15s |
| Story / lesson | Optional full-screen chapter card at the turn, then back to them | |
| Punchline | Punch-ins on the lines that matter; one bigger graphic moment on the biggest line | |
| Close | Ends on their last word. No outro card, no end hold | |

**Something new on screen every 2-5 seconds:** a cut, a punch-in, a graphic or B-roll. No dead stretches. But don't stack effects everywhere: viewers should be able to follow without effort. Easy to follow beats busy.

## Pacing

- Pauses longer than **0.22s** are cut down to about **0.12s** total: keep **0.07s** after the last word and **0.05s** before the next one. Line-to-line gaps about **0.12s**.
- Drop a click or breath shorter than 0.12s right before a line's first word.
- Speech speed stays natural. A single dragging line can go **1.25x**. A whole cut can run **1.1x** as an alternate version.
- **Hard cuts only.** No transitions, whips or spinning zooms.
- Long-form (YouTube/podcast) is looser: max pause 0.3s for a tight YouTube cut, 0.6s for a natural podcast cut.

## Framing and zooms

- Two framings: the base shot and a **static punch-in at 120%**, cut in on a punchline and held for the whole sentence.
- At most one **slow push** (100% → 118% across the line) for the single most emphatic line.
- Anchor zooms on the face (eyes about a third down the frame), so the face doesn't drift toward an edge.

## Captions

Pick one style with the creator. Both are proven:

- **Phrase captions (default):** 3-4 words at a time, broken at natural phrases. Bold geometric sans (Inter at weight 700 with optical size 32, which is its "Display" cut, or similar), white, tight letter spacing, a soft faint shadow, no outline, no highlight color. Easier to read than one word at a time.
- **One-word captions:** one word at a time, timed to when it's said. Feels faster.

For both:
- Lowercase as spoken, no punctuation. "I", "I'm", "I've", "I'll" keep their capital. Fix spellings with a caption fixes list (brand names, accents, numbers like "10k").
- **Position: on the wall above their head**, about 26% down the frame (y ≈ 500 of 1920), not at the bottom. Drop to the lower third (y ≈ 1330) only while a graphic sits up top.
- Size about 90-100px on a 1080-wide frame.
- Hidden while the hook title is up and during full-screen cards. Shown over B-roll.
- Never under the app's buttons (lower right) or top header.

## Hook title (ask every video)

Whether a video gets a title, what it says and how it looks is the creator's call. Offer 2-3 wordings from what they say. A pattern that works:
- 2-4 short lines, upper-middle of the frame, clear of the face.
- Typed on letter by letter over about **1.9s**, starting at **0.12s**, gone when the hook line ends.
- Mixed type for personality: a plain bold sans for most of it, an italic serif for the soft part, and one key word much bigger that pops in.
- Captions hidden while it's up.

## Graphics

**Fonts that are free to use:** Inter (captions, labels; set `font-variation-settings: "opsz" 32` for its Display look), Instrument Serif (titles, regular and italic), Roboto Mono (small uppercase labels). Download from Google Fonts into `_style/fonts/`. If the creator has brand fonts, use those.

**Colors:** take the creator's brand palette if they have one. Otherwise pick 3-4 colors from their reference videos and write the hex codes into MY-STYLE.md.

**A menu of elements** (all keep the creator on screen except the chapter card). Propose specific ones tied to specific lines; they pick.

| Element | Good for | How |
|---|---|---|
| Photo cards | the hook | 3-6 photos sliding in from the sides and top, kept off the face |
| Notes-style checklist | a list, credentials, steps | a phone-notes card in the lower middle; one item appears and ticks per line |
| Chapter card | the turn in a story, "step 1" | full screen, paper texture, heading typed on, a live 1-3 word caption underneath |
| Text-message thread | dialogue, a letdown, a reaction | chat bubbles popping in with typing dots, in a lower card so captions keep running |
| Collage | the biggest line | realistic photo cutouts drifting or flying in |
| Sparkles | one word ("magic", "glow") | small four-point stars twinkling around the caption |
| Keyword pop | a key phrase | big stacked type on the empty side of the frame |
| Screen recording | a product, an app, a website | a real recording of the page, not a static screenshot |

**Rules:**
- Overlays on the footage, not full-screen white cards. Full screen only for chapter breaks.
- **Realistic photo cutouts** with a scrapbook-sticker feel (white die-cut border, soft shadow) beat clip-art and drawn shapes. Nothing cheesy: fake certificates, cartoon badges and novelty props tend to get cut.
- Each element lands on the spoken word, then rests. Start a graphic a beat before its punchline so it has room.
- Keep graphics clear of the top header, the lower-right buttons and the caption zone.
- **Imagery is original**: the creator's own photos, images they generate, or licensed stock. Never other people's photos.

**Images:** you can't take photos for them, so ask when a graphic needs one.
- Photo cards: picks from their camera roll, dropped in `_edit/assets/`, or images from an image generator they use.
- Cutouts (a PNG with the background removed): on an iPhone they can long-press the subject of a photo and choose Copy or Share to get one; most design apps have a background remover too. Add the white die-cut border and shadow yourself in the overlay's CSS.
- Approved images go in `_style/assets/` so later videos can reuse them.
- No images? Use a graphic that doesn't need one (checklist, text thread, keyword pop) instead of drawing fake objects in CSS: drawn objects look fake next to real footage.

## B-roll

- From the creator's own life, matching the spoken line literally ("my desk" → their desk).
- **1.5-2.8s** per clip. Clips can chain back to back for a little sequence (pouring coffee → opening a laptop → typing).
- Graded like the main footage, filling the frame. Captions stay on top.
- The project's `B-ROLL/` folder first. Never show other people (friends, family, anyone on a video call) without the creator's OK.

## Color

A gentle warm grade that flatters skin, applied to the main footage and B-roll alike:

```
colortemperature=temperature=5400:mix=0.7,eq=contrast=1.07:brightness=-0.02:saturation=1.14:gamma=0.97
```

Pushing it further (5000K, contrast 1.10) turns skin orange. If their raw footage already looks right, skip the grade. No stylized filters (vintage, camcorder, heavy LUTs) unless they ask.

## Sound

- **Voice:** compressed, then loudness-normalized. Short-form: about **-10.5 LUFS** (loud and dense, like most Reels). YouTube: **-14 LUFS**. Podcast audio: **-16 LUFS**.
- **Phone recordings that sound boxy** (like they're in a small room): use the voice remaster chain in `recipes.md`, and put a before/after on the review page so they can hear it.
- **Sound effects: soft and sparse.** A keyboard-typing sound under a typed-on title and a soft click on a few key graphic moments work well, mixed about 12dB under the voice. A click on every single graphic gets overstimulating. Synthesized typing sounds fake: use real sounds. Ask the creator for them (a free sound from their editing app's library, or 10 seconds of their own keyboard recorded on their phone) and keep them in `_style/assets/sfx/`. No sounds yet? Skip sound effects rather than faking them.
- **No music in the edit.** They add it in their posting app, where trending audio lives.

## Covers

Every short gets a **1080×1920** cover:
- A graded still of them smiling, the hook title in the video's fonts, and 1-3 of the video's graphics or photos.
- Instagram and TikTok profile grids only show the **middle 3:4** (y 240 to 1680), so the face, the title and anything important sit inside that box.
- Offer 2-3 options. **Closed-lip smiles with eye contact** (even slight ones) usually win; add a laugh only if a great one exists.
- Title clear of their head, nothing on their face.

## Versions and platforms

- Finals at **1.0x** and, if they want, **1.1x**.
- Separate Instagram and TikTok versions only where the call to action differs ("comment GUIDE" vs. "link in bio"). Put the call to action in the bold caption font so it's easy to read.
- Long-form: a 16:9 thumbnail, and section starts double as YouTube chapters (the first chapter must be 0:00).

## Export settings

- 1080×1920 (or 1920×1080), 30fps, H.264, high quality (CRF 16-18), AAC 256k, `+faststart`.
- Keep the source frame rate if it's 24 or 25 and they prefer it.

---

## Changelog: what you told me

Add a dated line here every time the creator gives a lasting preference, with the reason. Example:
- 2026-01-05: captions bigger (110px), "can't read them on my phone".
