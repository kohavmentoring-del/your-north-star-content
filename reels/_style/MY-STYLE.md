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

**Confirmed with Kohav (2026-10-25): phrase captions, 3-4 words at a time.**

- **Phrase captions (default, confirmed):** 3-4 words at a time, broken at natural phrases. Easier to read than one word at a time.
- Lowercase as spoken, no punctuation. "I", "I'm", "I've", "I'll" keep their capital. Fix spellings with a caption fixes list (brand names, accents, numbers like "10k").
- **Fonts and color — overridden per kit.md (001-how-to-suck), treat as her house style going forward unless she says otherwise:** Montserrat ExtraBold. Burgundy on the light room shots, taxi yellow + burgundy outline over dark inserts/B-roll.
- Position: on the wall above her head by default (y ≈ 26% down the frame), not the bottom. Drop to the lower third only while a graphic sits up top.
- Size about 90-100px on a 1080-wide frame.
- Hidden while a hook title or full-screen card is up. Shown over B-roll.
- Never under the app's buttons (lower right) or top header.

## Hook title (ask every video)

Whether a video gets a title, what it says and how it looks is the creator's call. Offer 2-3 wordings from what they say. A pattern that works:
- 2-4 short lines, upper-middle of the frame, clear of the face.
- Typed on letter by letter over about **1.9s**, starting at **0.12s**, gone when the hook line ends.
- Mixed type for personality: a plain bold sans for most of it, an italic serif for the soft part, and one key word much bigger that pops in.
- Captions hidden while it's up.

## Graphics

**Fonts — per kit.md (her signature set, use for cards/titles going forward):** Playfair Display (regular + italic) for titles and cards, Montserrat (ExtraBold for captions/labels). Download both from Google Fonts into `_style/fonts/`.

**Colors — her palette** (confirmed against her saved "Your North Star" design system, 2026-10-25):
| Token | Hex | Use |
|---|---|---|
| Taxi yellow | `#F6B511` | Hooks/captions on dark or busy footage, always with a thin burgundy outline (2-3px). Highlighted word in captions. |
| Burgundy | `#6B1A2A` | Text on light footage and cream cards. The outline around yellow. Never on brown or dark footage — it disappears. |
| Brown | `#5A3A28` | Caption boxes on busy footage, carousel/Story backgrounds. |
| Espresso | `#24160F` | Body text on cream, dark quote cards. |
| Cream | `#F6ECDD` | Carousel/quote card backgrounds, card backgrounds. |
| Tan | `#C9A07A` | Dividers and small details only. |

One text rule: burgundy on light/soft footage, taxi yellow + burgundy outline when footage is too dark for burgundy to read. Nothing else — no white captions, no extra colors.

**A menu of elements** (all keep the creator on screen except the chapter card/full-screen card). Propose specific ones tied to specific lines; they pick.

| Element | Good for | How |
|---|---|---|
| Photo cards | the hook | 3-6 photos sliding in from the sides and top, kept off the face |
| Notes-style checklist | a list, credentials, steps | a phone-notes card in the lower middle; one item appears and ticks per line |
| Chapter card / full-screen card | the turn in a story, a title moment | full screen, paper texture (cream), heading typed on in Playfair, a live 1-3 word caption underneath |
| Text-message thread | dialogue, a letdown, a reaction | chat bubbles popping in with typing dots, in a lower card so captions keep running |
| Collage | the biggest line | realistic photo cutouts drifting or flying in |
| Sparkles | one word ("magic", "glow") | small four-point stars twinkling around the caption |
| Keyword pop | a key phrase | big stacked type on the empty side of the frame |
| Screen recording | a product, an app, a website | a real recording of the page, not a static screenshot |
| Tear-off calendar | a countdown/day-count moment | small cream calendar page in a top corner, Playfair number, Montserrat label, tears off and falls away |

**Rules:**
- Overlays on the footage, not full-screen white cards. Full screen only for chapter breaks / title cards.
- **Realistic photo cutouts** with a scrapbook-sticker feel (white die-cut border, soft shadow) beat clip-art and drawn shapes. Nothing cheesy: fake certificates, cartoon badges and novelty props tend to get cut.
- Each element lands on the spoken word, then rests. Start a graphic a beat before its punchline so it has room.
- Keep graphics clear of the top header, the lower-right buttons and the caption zone.
- **Imagery is original**: the creator's own photos, images she generates, or licensed stock. Never other people's photos.

**Images:** you can't take photos for them, so ask when a graphic needs one.
- Photo cards: picks from her camera roll, dropped in `_edit/assets/`, or images from an image generator she uses.
- Cutouts (a PNG with the background removed): on an iPhone she can long-press the subject of a photo and choose Copy or Share to get one; most design apps have a background remover too. Add the white die-cut border and shadow yourself in the overlay's CSS.
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
kit.md also calls for a "golden hour inside" warm lamp look on the signature-background set — the grade above should already read as warm; don't double it up with the lamp's own warmth.

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

- 2026-10-25: Caption style confirmed as phrase captions, 3-4 words at a time (the default). Inspo: she'll share links/files before the style brief — study before styling episode 1.
- 2026-10-25: "001-how-to-suck" kit.md defines the signature-background set used every episode (phone on tripod, warm lamp, same earrings) and a specific font/color system (Playfair Display + Montserrat, burgundy + taxi yellow + cream) — folded into the Captions/Graphics sections above as her house style, pending confirmation at the first style brief that this should carry forward to every episode, not just ep1.
- 2026-10-25: Inspo studied — Chloe Shih "30 Lessons by 30 / pillars" reel (saved: `_style/references/chloe-shih-pillars-inspo.mp4`, contact sheet in `_style/references/_study/`). Talking-head life-advice genre match. Takeaways, NOT yet confirmed as her look (ask at the style brief for ep1 before applying):
  - Cuts/new element roughly every 1-2s — denser than the 2-5s baseline above; energetic pacing.
  - Bold rounded sans captions in a bright yellow-green, mixing short phrase captions ("It's okay to not be okay.") with single punch-words ("LOOK", "Be gentle.").
  - Physical-prop visual metaphor carried through the whole video (a Jenga tower labeled CAREER/LOVE/HEALTH/FRIENDS for "pillars") — not directly applicable to ep1 (kit.md already specs its own inserts/cards), but worth offering as a device for a future "pillars"-style script.
  - Numbered lesson reveals ("1. New beginnings", "2. Ask for help!") with a small icon/prop per lesson.
  - Bright, warm, minimalist-interior grade; measured loudness -17.9 LUFS integrated (quieter than our -10.5 LUFS short-form target — don't copy that part).
  - Doesn't match Kohav's signature-background format (single story, fixed set) — treat as tone/energy/caption-style inspo only, not a structural template for ep1.
