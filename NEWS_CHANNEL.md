# Global News & Tech channel: handoff

The owner asked (4 Oct 2026) for a separate chat for a new **global news and tech** Shorts channel, inspired by
Omar Agamy (@omaragamyy). This branch (`ccr-56282fe5-evehq4-news`) starts from the Interestingly Strange code, so the
whole pipeline is already here.

## About the inspiration
Omar Agamy is an Egyptian-Canadian creator (about 3 million YouTube subscribers, 3,000+ Shorts) whose videos are
short, fast explainers about countries of the world, current affairs and some tech news: one fact or new
development per video, a punchy hook, simple explanation. Study the format (hook, length, pacing, how he explains);
don't copy his name, look, voice, catchphrases or clips.

## What's already built (see `AGENTS.md` for the full guide)
- `render.py` + `motion/`: the 2D hand-drawn renderer (720x1280, 30 fps), captions, characters, camera.
- `motion/story.py`: cards, scrolls, tags, answer buttons, helmets, talking mouths.
- Narration in the owner's cloned voice (Chatterbox, `tools/clone_tts.py`), every line checked with Whisper medium:
  `tools/render_check.sh NAME`. Reword any misheard line (see the CLAUDE.md narration rules).
- One video = one file in `videos/`, with `SCRIPT`, scenes and `METADATA` (the upload sheet).
- The Interestingly Strange videos in `videos/` are examples to copy from (e.g. `machiavelli_feared.py`,
  `pyrrhic_victory.py`).

## First steps for this chat
1. Agree with the owner on the channel name, the mix (world news vs tech), and how many videos a day.
2. Build news-specific pieces in `motion/`: a simple world map with countries to highlight, flag shapes, a "date
   stamp" and a "source" tag, phone/laptop/chip drawings for tech stories.
3. Research and fact-check the first batch (two reliable sources per claim, dates on everything), then render,
   check, and deliver with upload sheets.
4. Keep a `out/news_calendar.md` for this channel.

## Script format (from the owner's reference clip, 4 Oct 2026; our own animation)
The owner shared a 63 s reference: a host chats with the **country itself** (a talking flag). Use that *script shape*,
never its wording, look or footage:
- Line 1: the host greets the country / asks what changed. Line 2: the country states the news with the date.
- Then quick back-and-forth, one fact per line: the host asks the obvious viewer question ("How much was it before?"),
  the country answers with a sourced number. Convert money to dollars with the date's rate.
- Host reactions carry the emotion (surprise, a relatable comparison like "a nice dinner" vs "a new phone").
- Give the reason in the official source's words ("The government says ..."), plus one clarifying fact people get wrong.
- End on a question the viewer answers in the comments. About 45–60 s.
- Drawing: our `reporter` host (motion/characters.py) and `motion/news.country(...)` (talking flag on a pole), close shot
  on whoever speaks, pop-in panels for every number, `date_stamp` and `source_tag` on screen.
- Both parts are voiced in the owner's cloned voice; a 0.36 s pause whenever the speaker changes.
- First video in this format: `videos/japan_residency_fee.py`.
