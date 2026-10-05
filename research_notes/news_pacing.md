# Is our pacing right for Shorts? Research, measurements and changes (5 Oct 2026)

Owner's question: "Is our video speed good for audience retention and not swiping away?"

The earlier deep research for the first channel (29 Sep 2026) is in `research_notes/Shorts retention for animated
explainers/`. This note adds new sources and measures our six news videos against all of it.

Evidence labels:
- **[Academic]** peer-reviewed.
- **[Official]** YouTube.
- **[Creator]** creator or vendor claims, with no published method. Treat these as hints only.

## 1. What we measured (before the changes)

| Video | Length | Words/min while speaking | Pause at each full stop | Silence | Picture changes | Longest still shot |
|---|---|---|---|---|---|---|
| Plague | 62.7 s | 188 | 0.50 s | 12% | every 2.2 s | 4.9 s |
| Jobs | 55.6 s | 189 | 0.50 s | 13% | every 2.2 s | 4.8 s |
| Japan | 52.5 s | 192 | 0.50 s | 11% | every 2.1 s | 5.4 s |
| Diesel | 76.0 s | 199 | 0.50 s | 12% | every 2.0 s | 5.5 s |
| Apple | 46.1 s | 202 | 0.50 s | 12% | every 2.2 s | 5.8 s |
| Tesla | 55.3 s | 195 | 0.50 s | 13% | every 2.1 s | 4.8 s |

Other measurements:
- The first word is spoken at 0.12 s in every video.
- The first sentence takes 3.2-4.9 s.
- The ending is the question plus "Tell me in the comments", which takes 3.4-4.3 s, then 0.9 s of tail.
- The owner's reference Short ("How the Rich fools you", measured 29 Sep) runs at about 260 wpm with almost no pauses
  and one visual change every 0.9 s.

## 2. What the research says

### Talking speed (words per minute): ours is right, keep it
- **[Academic]** Guo, Kim & Rubin (2014), edX: 6.9M viewing sessions. Engagement rose with speaking rate, and the
  fastest group (185-254 wpm) was best. The 145-165 wpm middle group was worst, because those speakers sounded least
  energetic. https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- **[Academic]** Bragg et al. (CHI 2018): 453 people, synthetic speech. Mean intelligible listening rate was 309 wpm
  (297 for sighted listeners). **Native English speakers scored significantly higher.**
  https://danibragg.com/papers/listening_rates.pdf
- **[Academic]** Jones, Berry & Stevens (2007), Computer Speech & Language 21(4): a faster synthetic speech rate
  **lowered comprehension for both native and non-native listeners**, but did not change how persuasive the message
  was. https://www.sciencedirect.com/science/article/abs/pii/S0885230807000216
- **Verdict.** 188-203 wpm sits in Guo's best-engagement band and is still far below the comprehension limit.
  - We are a **global** channel, and many viewers are not native English speakers.
  - **Going faster would cost understanding**, and you asked for "clear explaining".
  - **Keep Kokoro at 0.95.**

### Pauses: ours were too long, so I shortened them (but they stay clear)
- **[Academic]** Tanaka, Sakamoto & Suzuki (2011), Acoustical Science & Technology 32(6):
  - Pauses between phrases (100-400 ms) made sentences more intelligible than no pauses.
  - The benefit showed with 300-400 ms pauses.
  - Natural pauses between phrases averaged about 200 ms.
  - https://www.jstage.jst.go.jp/article/ast/32/6/32_6_264/_article
- **[Academic]** The brain gives a strong "new start" response after pauses longer than ~200 ms (Hamilton, Edwards et
  al. 2018, as cited in *Continuous speech with pauses inserted between words*, PLOS ONE 2023). So a full stop needs a
  bit more than 200 ms to register as a stop.
  https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0289288
- **[Measured]** Human Shorts narrators in the owner's references pause about 0.09-0.19 s (`out/voice_rhythm.md`).
- **[Creator]** Editing guides cut "ums" and long pauses because it "keeps the energy high"
  (https://klap.app/blog/jump-cut-definition). No guide gives a measured number.
- **Verdict.** 0.5 s at every one of ~20 full stops a minute added 2-3 s of silence per video, and silence is where
  people swipe. Clarity is fully kept at about 0.32-0.40 s.
  - Each sentence is still voiced as its own take, so the voice still drops at every full stop.
  - The captions still show every full stop.
  - **Change:** full stop 0.50 → 0.32 s, question 0.55 → 0.40 s, between lines 0.50 → 0.34 s.
  - **Exception:** the one "reveal" line keeps 0.55 s, because that silence (with the music drop) is deliberate.

### Visual pace: medium, never frozen (we are news, not a meme channel)
- **[Academic]** Lang, Bolls, Potter & Kawahara (1999), J. Broadcasting & Electronic Media 43(4):
  - Faster cutting raises arousal.
  - For **calm** content, memory is best at a medium pace.
  - For **arousing** content (war, disease), fast pacing overloads viewers and memory drops.
  - https://www.tandfonline.com/doi/abs/10.1080/08838159909364504
- **[Academic]** Grabe, Lang & Zhao (2003), *News content and form*, Communication Research 30(4):
  - Tabloid "bells and whistles" helped memory for calm news, but overloaded viewers on arousing news.
  - Viewers rated tabloid-packaged news **less objective and less believable**.
  - https://journals.sagepub.com/doi/abs/10.1177/0093650203253368
- **[Academic]** Lang, Schwartz & Mayell (2015), J. Media Psychology 27(2): older viewers remember less as pacing gets
  faster, especially for arousing messages. https://econtent.hogrefe.com/doi/10.1027/1864-1105/a000130
- **[Academic]** Cutting et al. (2011): modern films average under 4 s per shot, with more motion inside each shot.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/
- **[Creator]** Common advice is "a new visual beat every 2-3 s"; it is unmeasured but consistent with the above.
- **Verdict.** Our one change every ~2.1 s is a medium pace. That is right for a news channel that has to be believed,
  and it suits the scary stories (plague, war). We should **not** copy the 0.9 s pace of the entertainment reference.
  The weak spots were **frozen shots of 4.8-5.8 s**.
  - **Change:** every held shot now has a slow camera push-in (+0.6% zoom a second, at most 3.6%), so nothing is ever
    frozen. It also moves from frame 1.
  - Three Diesel framings where a price sign or the grocery sign ran into the headline are fixed.

### Hook (first 1-2 seconds)
- **[Official]** Shorts metrics: "viewed vs swiped away" is the hook test. Average percentage viewed counts only people
  who stayed past the first seconds. https://support.google.com/youtube/answer/12220281
- **[Official]** Since June 2026, viewers can hold the screen to play a Short at 2x. Viewers who find a Short slow can
  speed it up rather than swipe, so the opening matters even more.
  https://routenote.com/blog/youtube-shorts-updates-playback-speed-clear-screen-and-more/
- **[Academic]** Curiosity is a felt gap in knowledge, and it peaks when the gap feels closable (Loewenstein 1994;
  Kang et al. 2009).
- **[Creator / YouTube blog]** Jenny Hoyos: "you have one second to hook someone". Phrase the hook as a question or an
  unexpected twist. https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/
- **Verdict.** Our hooks are true and clear, but some put the surprising word late. In Plague, "plague" comes at
  ~3.5 s; in Jobs, the shocking number comes in sentence 2. **Wording changes need your OK (script-first rule)**,
  so they are proposed below, not applied.

### Ending
- **[Creator]** Hoyos reports about a 25% drop in the last second when a Short winds down, and advises ending at the
  peak. This is creator data, not a study.
  https://www.youtube.com/shorts/95JNCi489gA
- **[Official]** Replays count as views since 31 Mar 2025. Engaged views exclude loops, but watch time from loops still
  counts toward average percentage viewed.
- **Change (production only):** the silent tail after the last word is 0.9 → 0.5 s. The YES/NO buttons still pop.
  The music ends on the chord that loops back into bar one.
- **Proposed (wording):** end on the spoken question and let the on-screen YES/NO buttons do the "comment" job. This
  saves about 1.2 s.

### Length
- **[Official]** YouTube allows up to 3 minutes, and its staff say there is no magic length: "as long as it needs to
  be". https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/
- Length studies conflict and are mostly vendor claims (see the 29 Sep notes).
- **Verdict.** 44-60 s is fine. Diesel is the long one (73 s after the changes); one repeated line could go (proposed
  below).

## 3. After the changes (measured)

| Video | Length (before → after) | Silence (before → after) |
|---|---|---|
| Plague | 62.7 → 60.3 s | 12 → 9% |
| Jobs | 55.6 → 53.3 s | 13 → 9% |
| Japan | 52.5 → 50.6 s | 11 → 8% |
| Diesel | 76.0 → 73.1 s | 12 → 9% |
| Apple | 46.1 → 44.3 s | 12 → 9% |
| Tesla | 55.3 → 53.1 s | 13 → 9% |

Talking speed is unchanged (188-203 wpm).

## 4. Proposed wording changes (need the owner's OK)

| Video | Now | Proposed | Why |
|---|---|---|---|
| Plague | "A laboratory worker in Siberia has died, and doctors suspect the plague." | "Doctors suspect the plague killed a lab worker in Siberia." | "plague" in the first second |
| Jobs | "Economists expected America to add about ninety thousand jobs in September." | "America added just twenty-nine thousand jobs in September, about a third of what economists expected." | the surprise first |
| Japan | "If you dream of moving to Japan for good, it just got a lot more expensive." | "Japan just made staying for good twenty times more expensive." | the number first |
| Tesla | "In Austin, Texas, you can now pay for a taxi ride with no driver." | "Tesla's taxi with no steering wheel just finished its first month." | the strange detail first |
| Diesel | (keep: "highest price ever" is already up front) | cut line 16, "So prices may drop soon, but they may not stay low for long." | repeats line 15, saves ~3 s |
| All | "… ? Tell me in the comments." | end on the question; YES/NO buttons on screen | end at the peak, ~1.2 s shorter |

The Jobs and Japan changes would need small re-orders of the lines after them, so the facts aren't said twice.

## 5. How to judge it on the channel

- **Viewed vs swiped away** tests the hook. **Average percentage viewed** tests the body.
- The retention graph shows exactly where people leave. If one line causes a dip in several videos, rewrite that
  kind of line.
- Change one thing at a time between uploads, so we know what worked.
