---
name: reel-kit
description: Turn one of Kohav's voice memos (or a story from brand/voice.md) into a full Your North Star reel kit - scored hook, script in her words, on-screen cards, HyperFrames motion graphics, caption with CTA, cover, shot list, optional voiceover, and a scheduled slot. Use when she says "make a reel", "new episode", "reel kit", "here's a voice memo", or "schedule the next one".
---

# reel-kit

One reel in, one finished folder out: `reels/NNN-slug/`. Everything she needs to
film, edit, caption and post that reel lives in that folder.

Read `brand/voice.md` before anything else. It overrides every generic rule in
the ig-* skills when they disagree.

## What she has already told us (do not relearn these the hard way)

- **Her words only.** Build hooks and scripts by cutting and reordering her own
  sentences. Never write a new sentence in her name.
- **A hook must be something a person says out loud.** A cryptic fragment that
  scores well ("80 people.") is a fail even at 100. Every number needs the words
  around it that make it make sense to a stranger.
- **Hooks must score 90+ on `hookscore.py` and still pass the line above.** The
  usual fix for a weak natural line is one true concrete detail (her age, the
  year, New York) plus talking straight to the viewer ("You?").
- **Personal over general.** Lines about "people" or "startups" go before lines
  about her get cut.
- **Series episodes say so.** Name the series and the episode number out loud
  ("this is the first episode of my signature series, How To Suck").
- **Always one call to action**, from her, at the end. Never "follow for more".
- **Watch double meanings.** "Suck at sucking" was cut for reading as sexual.
- One story per reel. Never combine stories from voice.md.

## Steps

1. **Get the material.** A voice memo transcript, or a story number from
   `brand/voice.md`. If there is no specific true moment in it, ask one question
   for one before writing.
2. **Hooks.** Write 5-8 hook lines from her sentences. Score all of them:
   `python3 ~/.claude/skills/ig-reel/hookscore.py hooks.txt`. Iterate until one
   is 90+ and reads like speech. Show her the top 3 with scores.
3. **Script.** Cut and reorder her words around the winning hook:
   hook -> her question or thesis -> her own struggle -> series line -> CTA.
   Make the last line repeat a word from the hook so the replay loops.
4. **Check it.**
   - `python3 ~/.claude/skills/ig-reel/beats.py script.txt --target 35` - the
     hook must be 3s or less. Long lines are fine (she talks in long sentences)
     but each one needs a shot or card change inside it; note where.
   - `python3 ~/.claude/skills/ig-human/detect.py script.txt` - must PASS
     (70+). If burstiness fails, merge her sentences back the way she said them.
5. **Cards.** Write `cards.json`: on-screen text, six words or fewer each, with
   a start time from the beat sheet. Include a title card for the series.
6. **Motion graphics.** If the HyperFrames connector is available, compose the
   cards and the title card with `brand/look.md`, render the video, and save
   the link in `kit.md`. If it is not connected, leave `cards.json` ready and
   say so.
7. **Caption.** Run `/ig-caption` on the script. The caption carries the same
   single CTA as the video. Then `/ig-human` on the caption.
8. **Cover.** Make a 1080x1920 cover in Canva (connector) with the hook card
   text and `brand/look.md`. Save the Canva link in `kit.md`.
9. **Voiceover (optional).** Default is her own recording: a voice memo of her
   reading `script.txt`, laid under B-roll. Never use an AI voice clone of her
   unless she asks for it in that conversation.
10. **Shot list.** 3-4 setups (front, side, close-up, walking in NYC) mapped to
    script lines.
11. **Schedule.** Add a row to `schedule.md` with a planned date. If PostZen
    tools are available and her Instagram is connected, offer `/ig-publish` to
    schedule it, and only after she says yes to the exact caption, account and
    time. Otherwise mark it "post manually".
12. **Save.** Write everything to `reels/NNN-slug/`, commit, and push.

## kit.md template

```
# NNN - Title
status: draft | filmed | edited | scheduled | posted
planned: YYYY-MM-DD HH:MM (America/New_York)

## Hook (score)
## Script  -> script.txt
## On-screen cards  -> cards.json
## Shot list
## Voiceover
## Caption
## Cover  (Canva link)
## Motion graphics  (HyperFrames link)
```
