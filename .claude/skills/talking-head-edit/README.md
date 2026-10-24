# Talking-head video editor for Claude

A Claude skill that edits your talking-head videos for you. You film, drop the clips in a folder, and Claude:

1. Transcribes every take, word by word
2. Cuts 2-3 versions at different lengths, keeping your best take of each line
3. Opens a review page where you press ▶ on any line and mark **Cut**, **Speed up** or **Add back**
4. Styles it: captions, punch-in zooms, on-screen graphics, B-roll, color, and clean loud audio
5. Exports the final video, a captions file and 2-3 cover options

It asks you about the title and the look of every video, and it remembers every note you give it ("captions bigger", "no sound effects"), so each edit gets closer to your style.

## What you need

- A **Mac** (Apple silicon is fastest) or a **Windows PC**
- A **Claude Pro or Max** plan
- **Claude Code**: the Code tab in the Claude desktop app, or Claude Code in a terminal
- About 3 GB free for the tools, plus 5-10 GB free per video while it's being edited

It won't work in a regular chat on claude.ai, because it needs to run editing tools on your own computer.

## Install

**The easy way:** open the Claude desktop app, go to the **Code** tab, choose the folder where you keep your videos, drag this zip into the chat and say:

> Install this skill for me as a personal skill.

**By hand:** unzip it and move the `talking-head-edit` folder into your skills folder:
- Mac: `~/.claude/skills/` (in Finder: Go → Go to Folder…, paste `~/.claude/skills`). If Finder says it doesn't exist, use the easy way above instead.
- Windows: `C:\Users\<your name>\.claude\skills\`

Start a new Claude Code session after installing.

## Your first video

1. Make one folder per video with your raw clips in it. Add a `B-ROLL` folder inside it for any extra shots you want used.
2. In the Code tab, open the folder that holds your video folders.
3. Type `/talking-head-edit` and say which folder, e.g. *"/talking-head-edit edit the clips in 'Morning routine reel'"*.

The first time, Claude checks your computer for the tools it needs and asks before installing anything (ffmpeg, a speech-to-text model, and a small browser for rendering text). Then it asks for 1-3 videos whose look you love, so it can learn your style.

**Your first video takes the longest.** Claude is building its editing tools and learning your look as it goes, and that uses a lot of your Claude usage. On the Pro plan you may hit your limit partway through; just pick up where you left off after it resets. From the second video on it reuses everything and goes much faster.

**Have these ready if you want them:** photos for on-screen graphics (your own, or ones you generated), and a couple of real sound effects (a keyboard typing sound, a soft click) from your editing app's free library. Claude will ask when it needs them, and skips them if you don't have any.

## Filming tips that make the edit better

- Film vertical for Reels/TikTok, horizontal for YouTube. It sorts them for you.
- Messed up a line? Pause for a second and say it again. Keep rolling. It finds the cleanest take.
- Long takes are fine. Several clips are fine.
- Face a window or a light. The edit can warm the color, but it can't fix a dark face.
- Phone audio sounds boxy in small rooms. Claude can clean that up, but a quiet room helps most.

## What it doesn't do

- It doesn't post anything for you, and it doesn't spend money.
- It doesn't add music: add trending audio in Instagram, TikTok or your editing app when you post.
- It only uses your own footage and images (or ones you generate or have licensed). No other people's photos.

## Files

- `SKILL.md`: the instructions Claude follows
- `references/`: the starter look, setup steps, tested editing commands and the review page spec

Your own look and notes are saved in a `_style` folder next to your video folders, not in this skill. Updating the skill later won't erase them.
