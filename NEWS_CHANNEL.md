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
- Narration in Kokoro `am_fenrir` (owner's cloned voice only on request), every line checked with Whisper medium:
  `tools/render_check.sh NAME`. Reword any misheard line (see the CLAUDE.md narration rules).
- One video = one file in `videos/`, with `SCRIPT`, scenes and `METADATA` (the upload sheet).
- The Interestingly Strange videos in `videos/` are examples to copy from (e.g. `machiavelli_feared.py`,
  `pyrrhic_victory.py`).

## First steps for this chat
1. Agree with the owner on the channel name and the mix (world news vs tech). Posting: 2 videos a day.
2. Build news-specific pieces in `motion/`: a simple world map with countries to highlight, flag shapes, a "date
   stamp" and a "source" tag, phone/laptop/chip drawings for tech stories.
3. Research and fact-check the first batch (two reliable sources per claim, dates on everything), then render,
   check, and deliver with upload sheets.
4. Keep a `out/news_calendar.md` for this channel.

## Script format (from the owner's reference clip, 4 Oct 2026; our own animation)
The owner shared a 63 s reference: a host chats with the country itself (a talking flag). Use only the *script shape*,
never its wording, look or footage. The owner asked (4 Oct 2026) not to copy his style: no talking flag (we use our
globe), and never his opening "Hey <country>, what's new with you?" or any greeting to the country.
- Line 1: the host states the surprising news to the viewer as a hook (e.g. "Want to live in Japan for good? It just got
  a lot more expensive."). Line 2: the Globe confirms it with the date.
- Then quick back-and-forth, one fact per line: the host asks the obvious viewer question ("How much was it before?"),
  the country answers with a sourced number. Convert money to dollars with the date's rate.
- Host reactions carry the emotion (surprise, a relatable comparison like "a nice dinner" vs "a new phone").
- Give the reason in the official source's words ("The government says ..."), plus one clarifying fact people get wrong.
- End on a question the viewer answers in the comments. About 45–60 s.
- Drawing: our `reporter` host (motion/characters.py) and `motion/news.globe(...)`: our talking desk globe, painted in the
  story country's flag colours (add a palette in `PALETTES`). Never a talking flag. Close shot
  on whoever speaks, pop-in panels for every number, `date_stamp` and `source_tag` on screen.
- Two voices (owner, 5 Oct 2026): the host is the channel narrator (Kokoro `am_fenrir`); the Globe has its own Kokoro
  voice (`GLOBE_VOICE`, per-line `voice=` in the script; default `bm_george`). A 0.36 s pause whenever the speaker changes.
- First video in this format: `videos/japan_residency_fee.py`.

## Owner's channel-wide decisions (5 Oct 2026)
1. **Voice: Kokoro, not the cloned voice.** The default narrator is Kokoro `am_fenrir` at speed 0.95 (`motion/voice.py`).
   Use the owner's cloned voice (`NARRATOR_ENGINE=clone`) only if the owner asks. On Interestingly Strange, more viewers
   swiped away on cloned-voice videos (about 35% stayed) and Whisper misheard it far more often. For a voice unique to
   this channel, Kokoro can blend voices (e.g. `NARRATOR_VOICE="am_fenrir,am_fenrir,am_michael"`): offer the owner
   2-3 short samples, checked with Whisper medium, before picking one.
2. **Posting: 2 videos a day, not 3.** Many similar videos a day is riskier under YouTube's "inauthentic /
   mass-produced content" rule.
3. **Script first.** For every new video, send the owner the script first (each line, what's on screen, title,
   sources) and render only after they approve or edit it. Keep their wording; if one of their lines would be
   misheard, say so and suggest a fix. Their ideas, opinions and edits make each video original, which protects
   monetization.

## Company stories and topic choice (owner, 5 Oct 2026)
- Company stories: the Globe wears the company's brand colours (`PALETTES` in `motion/news.py`, e.g. `"apple"`: silver
  and graphite) plus a white badge with the company's mark so viewers recognise it (owner's request). We draw the mark
  ourselves as a simple shape (`EMBLEMS`), never paste the official logo file, and never suggest the company made or
  endorses the video.
- Any topic is open, including wars and tariff/trade wars, as long as the accuracy and neutrality rules hold.
- What US viewers stay for (research, 5 Oct 2026): the money-in-your-pocket angle. In the Iran war, 7 in 10 Americans
  worry most about gas prices (Pew, Apr 2026); 64% say gas prices hurt their household (Reuters/Ipsos); tariffs are
  raising food prices (CAP). Economy/inflation, government and immigration top Gallup's "most important problem". So:
  lead with what a story means for the viewer (prices, jobs, their phone, their data), then explain the why.
  Shorts: most engagement happens in the first 10 seconds, so the hook line is the most important line. 20% of US
  adults (43% under 30) regularly get news on TikTok; YouTube is used by 84% (Pew 2025).
  Sources: https://www.pewresearch.org/global/2026/04/07/gas-prices-are-americans-top-concern-in-iran-war/ ;
  https://thehill.com/policy/international/5820379-rising-fuel-costs-concern/ ;
  https://news.gallup.com/poll/14338/most-important-problem.aspx ;
  https://www.niemanlab.org/2025/09/more-americans-than-ever-now-get-news-on-tiktok-pew-finds/ ;
  https://www.americanprogress.org/article/the-trump-administrations-tariffs-and-iran-war-will-cause-americans-to-face-higher-prices-this-summer/
