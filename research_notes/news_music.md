# News channel background music: research and design (5 Oct 2026)

Owner's ask: new background music for the news story videos, designed for the highest possible retention, backed by
research, no guesses. Posting: 2 videos a day, at 9:30 PM IST and 4:30 AM IST.

## What the research says

| Finding | Source | What we do with it |
|---|---|---|
| A **simple beat** under spoken news made it more memorable and more enjoyable; **complex music hurt** both processing and enjoyment. | Dillman Carpentier (2010), *Innovating radio news: Effects of background music complexity on processing and enjoyment*, Journal of Radio & Audio Media 17, 63-81. https://www.tandfonline.com/doi/full/10.1080/19376521003719375 | A steady pulse (bass + soft kick + ticks) and slow low chords. No busy arpeggio, no lead melody. |
| Music **with lyrics** hurt verbal memory and reading comprehension (d ≈ -0.3); instrumental music did not credibly hurt or help. | Souza & Barbosa (2023), *Should we turn off the music? Music with lyrics interferes with cognitive tasks*, Journal of Cognition 6(1), 24. https://journalofcognition.org/articles/10.5334/joc.273 | No vocals or vocal-like sounds. |
| Music that **fits the story's emotion** raised memory, attitude change and the **perceived credibility** of non-fiction video; mismatched music did not. | Herget & Albrecht (2022), *Soundtrack for reality?*, Psychology of Music 50(2). https://journals.sagepub.com/doi/full/10.1177/0305735621999091 | Three moods, chosen per story: `urgent` (wars, health scares), `money` (prices, jobs, fees), `tech`. |
| **Tempo changes arousal**, **mode (major/minor) changes mood**; the two are independent. | Husain, Thompson & Schellenberg (2002), Music Perception 20(2), 151-171. https://www.semanticscholar.org/paper/0336b09b4d6bc8570c386b8728ac36eefc973b6d | All moods are brisk (108-128 BPM) to keep arousal up. `tech` is major (curious, upbeat); `urgent` and `money` are minor (serious). |
| Structural features such as **music onsets, sound effects and voice changes** trigger orienting responses: brief extra attention and better memory. But capacity is limited: too many features compete with the message. | Lang, Limited Capacity Model of Motivated Mediated Message Processing (LC4MP); Potter, Lang & Bolls (2008), *Identifying structural features of audio*: 8 of 9 audio features caused orienting and raised memory for what came right after. https://www.semanticscholar.org/paper/4caf5aae24fa5a42fea60f99e7337e517c517078 ; the orienting response **habituates** when the same feature repeats: *I've heard that before* https://www.researchgate.net/publication/276929868 | At each **scene cut**, the bed changes groove and plays a riser, a soft impact and a 2-note sting. **Inside a scene** it stays steady, so it doesn't compete with the words. Each scene gets a different groove so the cue doesn't wear out (habituation). |
| A **sudden change, including a drop in level**, is detected automatically and pulls attention (mismatch negativity). A sound after silence is detected within about 100 ms. | Rinne, Särkkä, Degerman, Schröger & Alho (2006), Brain Research 1077, 135-143 (sound decrements and increments both detected) https://www.sciencedirect.com/science/article/abs/pii/S000689930600093X ; *Involuntary motor responses are elicited both by rare sounds and rare pitch changes*, Scientific Reports 2024 https://pmc.ncbi.nlm.nih.gov/articles/PMC11364668/ | One **drop** per video: the music cuts to silence in the pause before the reveal line, then comes back with a hit on its first word. |
| **Expectation and resolution:** tension builds before an expected outcome; a resolved prediction feels good. Suspensions and delayed cadences are used to raise tension. | Huron (2006), *Sweet Anticipation: Music and the Psychology of Expectation*, MIT Press. | The last scene ends on the **dominant (V) chord**, which resolves into bar one when the Short **loops**. |
| Since 31 Mar 2025, a Shorts view counts on **every play and replay**; "engaged views" still drive revenue. | YouTube via Music Ally, 27 Mar 2025. https://musically.com/2025/03/27/youtube-is-changing-the-way-it-counts-views-on-shorts/ ; gHacks https://www.ghacks.net/2025/03/27/youtube-updates-shorts-view-count-methodology-to-align-with-industry-standards/ | A seamless loop (same tempo and key; V resolving to I at the start). |
| Most swipe-aways happen in the **first ~2 seconds**. | Creator analytics guides (not peer-reviewed): vidIQ https://vidiq.com/blog/post/youtube-shorts-algorithm/ ; prepublish https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts | The music starts at **full energy on frame 1** with an impact. No fade-in. |
| Mix speech at least **20 dB above** background sound. | W3C WCAG technique G56. https://www.w3.org/WAI/WCAG20/Techniques/general/G56 | The bed sits about 21.6 dB under the voice while words are spoken (measured), and rises to about 10 dB under in the pauses. |
| Background music becomes "barely audible" between about **-23 and -36 dB** below the speech. | *Towards a characterization of background music audibility in broadcasted TV*, PMC9819249. https://pmc.ncbi.nlm.nih.gov/articles/PMC9819249/ | At -21.6 dB the music is still **audible but under** the words. In the pauses it comes up, so viewers feel the pulse. |
| YouTube's spam policy gives "**the exact same background music**" across many videos as an example of mass-produced content. | YouTube Spam policy https://support.google.com/youtube/answer/2801973 ; Music Ally, 10 Jul 2025 https://musically.com/2025/07/10/youtube-updates-mass-produced-and-repetitious-content-policy/ | Key, tempo, chord progression, grooves, tone and sting interval are picked **per video** from its name. No two videos share a bed. |
| News themes signal urgency with fast pulses and **clock-like ticking**, e.g. the *60 Minutes* stopwatch. | University of Plymouth, *The power & impact of breaking news music* https://wrasse.plymouth.ac.uk/ac-news/the-power-and-impact-of-breaking-news-music-1764805017 ; Wikipedia, Ticking (sound) | Soft 16th-note ticks sit high (above 4 kHz), out of the voice's way. This is our own generic tick, not any network's theme. |

**Gaps, stated honestly.**
- Reddit could not be read from here (it returns 403), so discussion signals came via web search only.
- No public study tests background music on YouTube Shorts retention specifically. The design rests on lab and
  broadcast studies, plus YouTube's own policies.
- The real test is your YouTube analytics: watch "viewed vs swiped away" and average % viewed.

## Design (motion/newsmusic.py)

- **Layers.**
  - A bass pulse with harmonics: phone speakers can't play below ~150 Hz, so the harmonics carry it.
  - Soft kick.
  - High ticks.
  - Low sustained chords (under ~500 Hz).
  - The voice band (about 1-4 kHz) is cut by ~8 dB on the whole bed. Measured: under 1% of the bed's energy is in
    1-4 kHz, where about 18% of the voice's energy is.
- **Scene cuts:** a riser into the cut, an impact, a 2-note bell sting in the silent gap, and the next groove.
- **Last scene (the question to viewers):** no kick, and an iv-V or IV-V cadence that loops back into bar one.
- **Per video:** `MUSIC = dict(mood="urgent"|"money"|"tech", drops=[beat ids])`.
- **Remixing:** `python render.py --video NAME --remix` rebuilds only the soundtrack in ~25 s, without redrawing the
  frames.
- **Intelligibility check:** `tools/mixcheck.py NAME` runs Whisper medium on the finished mix, to prove the music
  never hides a word.

## Posting times (owner, 5 Oct 2026): 9:30 PM IST and 4:30 AM IST

| IST | US Eastern | US Pacific | UK |
|---|---|---|---|
| 9:30 PM | 12:00 PM (11:00 AM from 1 Nov) | 9:00 AM (8:00 AM from 1 Nov) | 5:00 PM (4:00 PM from 25 Oct) |
| 4:30 AM | 7:00 PM **the previous day** (6:00 PM from 1 Nov) | 4:00 PM (3:00 PM from 1 Nov) | midnight (11 PM from 25 Oct) |

- Both slots land just **before** the US peaks that data studies report for Shorts: lunchtime (12-3 PM) and evening
  (6-9 PM). Sources: Buffer (1.8M videos) https://buffer.com/resources/best-time-to-post-on-youtube/ and SocialPilot
  https://www.socialpilot.co/insights/best-time-to-post-on-youtube. These are industry data, not peer-reviewed.
  Several of them advise posting a little before the peak.
- **4:30 AM IST slot (US prime evening): US stories.** It catches the American after-work scroll.
- **9:30 PM IST slot (US lunch + UK/Europe evening + India night): world and tech stories.** It catches the global
  audience too.
- US clocks go back on **1 Nov 2026** and UK clocks on **25 Oct 2026**. The IST times stay the same, but the US times
  move one hour earlier.
- Note: a video posted at 4:30 AM IST on, say, Tuesday is seen on **Monday evening** in the US. Put "as of" dates in
  scripts accordingly.
