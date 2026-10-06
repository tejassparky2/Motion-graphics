# Narration Pace, Pauses/Dead Air, and Sound Design for Short-Form Vertical Explainers (AI TTS)

Evidence tags: [Official] = platform/company research; [Academic] = peer-reviewed or conference paper; [Data study] = measured analysis by a third party; [Anecdotal/creator] = creator, vendor blog, or forum opinion. Vendor blogs that sell TTS or editing tools are tagged Anecdotal and flagged as self-interested.

## 1. How fast should a Shorts/Reels/TikTok voiceover be (WPM)?

### Takeaway
Normal speech is about 150 wpm. Voiceover-industry guides put explainers at about 160 wpm and commercials at about 180 wpm. The best measured evidence comes from a large MOOC dataset, not from Shorts: engagement was highest for the fastest speakers (185–254 wpm), and the mid-pace band (145–165 wpm) did worst. I found no measured WPM analysis of viral Shorts/TikTok narrators such as Zack D. Films. The "170–180 wpm for Shorts" figures online come from unsourced vendor blogs.

### Cited Findings
- **Baseline human rate.** "humans generally speak at a rate of 150 words per minute (Peelle & Davis, 2012)" [Academic, cited in Murphy et al. 2022]. — [Murphy et al. 2022, PDF](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2021/11/ACP-Lecture-Speed-Murphy-2021-in-press.pdf)
- **Guo, Kim & Rubin (2014), edX MOOC study.** 6.9M watching sessions across 862 videos. Speaking rate was computed from time-coded subtitles as total words ÷ in-video speaking time. "Speaking rates range from 48 to 254 words per minute (mean = 156 wpm, sd = 31 wpm)." Videos were split into speaking-rate quintiles: 48–130, 130–145, 145–165, 165–185 and 185–254 wpm. [Academic] — [Guo, Kim & Rubin, L@S 2014 PDF](https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf); [ACM DL](https://dl.acm.org/doi/10.1145/2556325.2566239)
- **Guo et al. result.** "Students generally engaged more with videos where instructors spoke faster… Within a particular length range, engagement usually increases (up to 2x) with speaking rate. And for 6–12 minute videos, engagement dips in the middle bucket (145–165 wpm)." [Academic] — [Guo et al. 2014](https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf)
- **Guo et al. on why fast speakers did better.** "fast-speaking instructors conveyed more energy and enthusiasm… We had no trouble understanding even the fastest-speaking videos (254 wpm), since the same information was also presented visually in PowerPoint slides. In contrast, instructors in the middle bucket (145–165 wpm) were the least energetic." The authors also warn that "speaking rate is merely a surface feature that correlates with enthusiasm." They ruled out confused re-watching as the cause: "no significant differences in the numbers of play and pause events among videos with different speaking rates." [Academic] — [Guo et al. 2014](https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf)
- **Guo et al. on the 160 wpm rule.** The common 160 wpm recommendation "(first made in 1967) was for live lectures, but students watching online can actually follow along with much faster speaking rates." [Academic] — [Guo et al. 2014](https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf)
- **MIT News summary of Guo et al.** "Fast talkers (professors seen as the most engaging spoke at 254 words per minute)"; "viewers generally tune out after six minutes." [Academic, press summary] — [MIT News 2014](https://news.mit.edu/2014/what-69-million-clicks-tell-us-about-how-fix-online-education)
- **Voiceover-industry norms.** Most conversational voiceover is about 150–160 wpm of finished audio. Explainer/corporate reads run about 160 wpm, commercials about 180 wpm ("copy is tight and the energy is up"), and audiobooks/long narration nearer 140 wpm. A :60 script is roughly 150–160 words, "a little less if you want room to breathe or music underneath." [Anecdotal/creator — VO industry guides] — [Debbie Grattan VO](https://www.debbiegrattan.com/blog/how-to-write-a-voice-over-script/); [Bread n Beyond](https://breadnbeyond.com/articles/how-many-words-does-a-60-seconds-explainer-video-needs/); [Lance Blair VO script timer](https://lanceblairvo.com/voiceover-script-timer/)
- **Short-form WPM claims (unsourced).** FlowShorts lists TikTok at "140–160 WPM", YouTube Shorts at "140–150 WPM", conversation at 130–150, audiobooks at 150–160 and podcasts at 150–170. It cites no sources. [Anecdotal/creator; vendor] — [FlowShorts](https://flowshorts.app/blog/words-per-minute-speaking). Other script-timer vendors say Shorts creators "often hit 170–180 WPM," also unsourced. — [ScriptTimer blog](https://blog.scripttimer.io/average-words-per-minute/). **These sources conflict with each other, and neither shows measurements.**
- **Zack D. Films.** Search results only describe the style qualitatively ("energetic… fast-paced and crisp") on AI voice-clone vendor pages. I found no WPM measurement. [Anecdotal] — [Komiko](https://komiko.app/voice/zack-d-films/ai-voiceover)

### Inferences
- For a 60 s short, a good working target is about 160–200 wpm (roughly 160–200 words per 60 s of narration). That sits at or above explainer/commercial norms and inside Guo et al.'s top two quintiles (165–185 and 185–254 wpm). It also stays well below the ~275 wpm audio-only comprehension cliff (see Section 2). Keep going above about 220 wpm for moments where on-screen visuals and captions carry the same information, which is the condition under which Guo et al. found 254 wpm easy to follow.
- The Guo result is really about *energy*, and speed is only a proxy for it. A fast but monotone TTS voice may not reproduce the effect. This is a caveat: I found no study isolating rate from enthusiasm.
- The Guo evidence is 6–12 minute lectures with adult learners. Carrying it over to 30–60 s entertainment shorts is an extrapolation.

### Gaps
- I found no published measured WPM analysis of top Shorts/TikTok/Reels narrators (Zack D. Films, finance explainer or story channels). A team could measure this themselves: transcribe with Whisper and divide word count by speech duration, the same method Guo et al. used.
- I found no platform-official (YouTube/TikTok/Meta) guidance on narration speed.

## 2. What does research say about speech rate vs comprehension and engagement?

### Takeaway
Comprehension of audio-only compressed speech stays largely intact up to about 250–275 wpm and falls quickly after that (Foulke & Sticht 1969). In lecture video with slides, Murphy et al. (2022) found no significant loss at 1.5x (210–234 wpm) or 2x (314–332 wpm). The only significant loss was at 2.5x (393–416 wpm), relative to 1x. Visuals raise the ceiling.

### Cited Findings
- **Foulke & Sticht (1969).** "When comprehension of compressed speech passages is measured, a rapid decline in comprehension is found above a speech rate of approximately 250 to 275 words per minute." Comprehension decreases slowly up to about 275 wpm and more rapidly beyond it. [Academic, review] — [Sticht, ERIC ED066080](https://files.eric.ed.gov/fulltext/ED066080.pdf); related: [Springer, speech-rate intelligibility threshold](https://link.springer.com/content/pdf/10.3758/BF03199702.pdf)
- **Murphy et al. on the 275 wpm threshold.** They restate: "speech comprehension begins to decline at around 275 words per minute if the information is encoded just audibly (see Foulke & Sticht, 1969). However, audiovisual materials… may be more comprehensible at increased presentation speeds due to benefits from the visually presented information." [Academic] — [Murphy, Hoover, Agadzhanyan, Kuehn & Castel 2022, Applied Cognitive Psychology](https://onlinelibrary.wiley.com/doi/abs/10.1002/acp.3899); [PDF](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2021/11/ACP-Lecture-Speed-Murphy-2021-in-press.pdf)
- **Murphy et al. 2022, Experiment 1 design.** n = 231 UCLA undergraduates (1x n=57, 1.5x n=58, 2x n=59, 2.5x n=57). Two lecture videos with slides and no captions: real estate appraisal (12:56, 2,031 words) and Roman Empire (14:27, 2,403 words). Table 1 speech rates:

  | Speed | Appraisal | Roman Empire |
  |---|---|---|
  | 1x | 157 wpm | 166 wpm |
  | 1.5x | 210 wpm | 234 wpm |
  | 2x | 314 wpm | 332 wpm |
  | 2.5x | 393 wpm | 416 wpm |

  [Academic] — [Murphy et al. PDF](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2021/11/ACP-Lecture-Speed-Murphy-2021-in-press.pdf)
- **Murphy et al. 2022, Experiment 1 results.** Immediate comprehension was .65 at 1x, .60 at 1.5x, .62 at 2x and .55 at 2.5x. One-week delayed comprehension was .59, .54, .53 and .50. The main effect of speed was F(3,202)=3.98, p=.009. "The 1x group performed better than the 2.5x group (pbonf = .004, d = .24) but there were no other pairwise differences." Abstract: "minimal costs incurred by increasing video speed from 1x to 1.5x, or 2x speed, but performance declined beyond 2x speed." [Academic] — [Murphy et al. PDF](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2021/11/ACP-Lecture-Speed-Murphy-2021-in-press.pdf)
- **Murphy et al. survey.** Of 123 undergraduates, 85% reported watching lecture videos faster than normal. In the control sample, 60% usually watch at 1.5x and 23% at 2x. [Academic] — [Murphy et al. PDF](https://castel.psych.ucla.edu/wp-content/uploads/sites/111/2021/11/ACP-Lecture-Speed-Murphy-2021-in-press.pdf)
- **Follow-up work.** Studies on playback speed, mind-wandering and age: [Murphy et al. 2023, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10330257/). A 2025 study on speed-watching and metacognition: [Computers in Human Behavior 2025](https://www.sciencedirect.com/science/article/abs/pii/S0747563225000032). Ahn 2025 on playback speed and preferences: [Applied Cognitive Psychology 2025](https://onlinelibrary.wiley.com/doi/10.1002/acp.70026). [Academic; I did not read the full texts, so their specific numbers are not reported here.]

### Inferences
- A 60 s short cannot be rewatched at leisure the way a lecture can, and viewers decide quickly whether to stay. The safe zone is therefore well below 2x: about 180–220 wpm, roughly 1.1–1.4x of a 155 wpm natural read. The Murphy 1.5x condition (210–234 wpm) showed no significant loss even without captions.
- Burned-in captions plus animated visuals that restate key numbers are the same "audiovisual redundancy" mechanism that let 254 wpm (Guo) and 314+ wpm (Murphy) remain comprehensible.

### Gaps
- I found no academic study on speech rate specifically in sub-60 s vertical entertainment video, or on swipe-away/retention outcomes as opposed to comprehension.
- I found no study separating the effect of speeding up TTS output from speeding up human speech.

## 3. Dead air, breaths, and gap length between sentences

### Takeaway
Creator and editor practice is to cut silences hard but keep about 100–200 ms of padding around speech. Auto-editor's default margin is 0.2 s, and a "YouTube hard-cut" setting is 100–150 ms. Zero padding sounds choppy. Some editors warn that deleting every breath pause entirely sounds unnatural and costs comprehension. Automated shorts pipelines insert about 0.3 s between TTS segments.

### Cited Findings
- **Auto-editor defaults.** The open-source tool's `--margin` defaults to 0.2 s of padding before and after each kept segment ("adds in some 'silent' sections to make the editing feel nicer"). The default audio threshold is `audio:threshold=0.04`. [Anecdotal/creator — tool default] — [auto-editor README](https://github.com/WyattBlue/auto-editor/blob/master/README.md)
- **VidPickr padding guidance (May 2026).** 0 ms = "hard cuts, will feel choppy"; 100 ms = "natural-feeling, slight pause before each thought"; 200 ms = "generous, good for podcasts"; 500 ms = "barely changes anything." It recommends "YouTube hard-cut style: 100–150ms. For podcasts: 200–300ms." Silence thresholds: about −40 dB for clean recordings, −30 dB as a moderate default, −20 dB is aggressive. The article is written for long talking-head content, not Shorts. [Anecdotal/creator; vendor] — [VidPickr](https://vidpickr.com/blog/remove-silence-from-youtube-videos-2026)
- **carykh's jumpcutter.** Built to "watch lectures ~1.5x faster by fast-forwarding long pauses between sentences." [Anecdotal/creator — tool] — [AlternativeTo listing](https://alternativeto.net/software/carykh-jumpcutter)
- **Counterpoint from Adobe community threads.** Some editors want to reduce the breath *sound* but keep the pause, "as removing the pause creates an unusual response… it's during the breaths that people assimilate what was in the previous sentence." [Anecdotal/creator] — [Adobe Community, Audition](https://community.adobe.com/t5/audition-discussions/how-do-i-remove-breaths-from-long-recordings-to-save-time/m-p/10982965)
- **Adobe feature request.** A Premiere Pro user asks for a fixed pause length after deleting pauses, because full removal "can make edits sound abrupt or unnatural, especially in… narration." [Anecdotal/creator] — [Adobe feature request](https://community.adobe.com/feature-requests-730/feature-request-allow-setting-fixed-pause-duration-after-deleting-pauses-in-text-based-editing-1328765)
- **RedditVideoMakerBot.** `silence_duration` = "Time in seconds between TTS comments", default **0.3**. [Anecdotal/creator — repo default] — [RedditVideoMakerBot .config.template.toml](https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/.config.template.toml)
- **short-video-maker (gyoridavid).** `paddingBack` = "how long the video should keep playing after the narration has finished (in milliseconds)", default **0**. [Anecdotal/creator — repo default] — [short-video-maker README](https://github.com/gyoridavid/short-video-maker)

### Inferences
- For TTS narration, the gap length is set in the pipeline, not in a recording session. A reasonable default is about 100–150 ms between clauses and sentences within a beat, and about 250–400 ms before a key reveal or number. RedditVideoMakerBot's 0.3 s sits at the top of that range.
- A "pause" in a short works best when something happens visually during it (a number counting up, a reveal). That way the audio gap is never visual dead air. This is an inference and has no direct source.

### Gaps
- I did not retrieve a Reddit thread (r/editors, r/NewTubers, r/VideoEditing, r/TikTokHelp) giving a specific inter-sentence gap number. Searches returned tool pages and Adobe forums instead. The "gaps under ~0.2 s" figure is consistent with the tool defaults above but I did not find it stated in a Reddit post.
- I found no data comparing retention for tight (0 ms) vs padded (150 ms) edits.

## 4. AI TTS narration: does it hurt retention? Speed-up factors and pipeline settings

### Takeaway
There is no independent data showing TTS itself hurts Shorts retention. The claims come from TTS vendors, who say *robotic/monotone* TTS loses viewers and expressive TTS doesn't. Open-source shorts pipelines mostly leave TTS speed at 1.0x by default and expose it as a knob. Background music defaults sit at 0.15–0.2 linear gain. Subtitle timing is derived from TTS word boundaries or proportionally from the text.

### Cited Findings
- **Vendor claims on TTS quality.** Shorts with expressive voices "showed up to a 15% higher audience retention rate compared to those with robotic, monotone text-to-speech." Supertone sells TTS, and no methodology is given. [Anecdotal/creator; vendor, self-interested] — [Supertone](https://www.supertone.ai/en/work/top-tts-voices-for-youtube-shorts)
- **Causes of robotic-sounding output.** Robotic sound comes from "flat prosody, no emotional cues, and poor script design," and "a script without punctuation will sound like a breathless, robotic wall of text." [Anecdotal/creator; vendor] — [Narration Box](https://narrationbox.com/blog/why-ai-voice-sounds-robotic-on-youtube)
- **BlackHatWorld forum.** Posters argue YouTube isn't directly suppressing AI voices; retention is the mechanism ("if the voice sounds too robotic people leave faster"). [Anecdotal/creator] — [BlackHatWorld thread](https://www.blackhatworld.com/seo/ai-voice-killing-youtube-shorts-reach.1837391/)
- **Other vendor claims.** Figures such as "5x more views" and "40–60% higher engagement" after upgrading TTS appeared in search summaries from TTS vendor pages (e.g., Vocallab, Murf, Recast). No methodology was visible, so treat them as marketing. — [Vocallab](https://www.vocallab.ai/blog/best-ai-voice-for-youtube-automation); [Recast](https://recast.studio/blog/creating-ai-voice-overs-for-youtube-shorts-a-step-by-step-guide)
- **MoneyPrinterTurbo (harry0703) config defaults.** `voice_rate = 1.0`, `voice_volume = 1.0`, `bgm_volume = 0.2`, `subtitle_display_mode = "sentence"` (or `"word_by_word"`), `subtitle_animation = "none"` (or `"pop_spring"`), `font_size = 60`. The MiMo TTS default style prompt asks for a natural, clear tone suited to short-video narration (Chinese: "请用自然、清晰、适合短视频旁白的语气朗读。"). [Anecdotal/creator — repo default] — [config.example.toml](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/config.example.toml)
- **MoneyPrinterTurbo rate conversion.** `convert_rate_to_percent()` turns `voice_rate` into edge-tts's signed percentage: `percent = round((rate - 1.0) * 100)`, so 1.2 becomes "+20%".
- **MoneyPrinterTurbo subtitle timing fallback.** When no word boundaries are available, subtitles are split by punctuation and sentence durations are allocated in proportion to character count. [Anecdotal/creator — repo code] — [app/services/voice.py](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/app/services/voice.py)
- **RedditVideoMakerBot.** Default TTS voice is `tiktok` with `random_voice = true`. Background audio volume defaults to **0.15** (range 0–1). `silence_duration` is 0.3 s. The config has no TTS speed setting. [Anecdotal/creator — repo default] — [RedditVideoMakerBot config template](https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/.config.template.toml)
- **short-video-maker (gyoridavid).** Uses Kokoro TTS (default voice `af_heart`) with Whisper for captions. Music volume options are "low", "medium", "high" and "muted", and the README default is **high**. [Anecdotal/creator — repo default] — [short-video-maker README](https://github.com/gyoridavid/short-video-maker)
- **ShortGPT (RayVentura).** Uses Microsoft EdgeTTS through an `edge_voice_module` (30+ languages) alongside ElevenLabs. I did not confirm a speed default in the repo files. [Anecdotal/creator — repo] — [ShortGPT GitHub](https://github.com/RayVentura/ShortGPT); [Issue #25](https://github.com/RayVentura/ShortGPT/issues/25); [edge-tts](https://github.com/rany2/edge-tts)

### Inferences
- None of the major open-source pipelines hard-codes a speed-up; the 1.1–1.3x habit is creator folklore. Given Murphy (no significant loss at 1.5x) and Guo (faster = more engaging), a 1.1–1.25x rate on a TTS voice whose natural rate is about 150–170 wpm lands at about 165–210 wpm. That fits the target band in Section 1.
- Time-stretching the whole audio file raises pitch perception less than it raises artifacts. Where the engine supports it, set rate at synthesis time (edge-tts `rate="+15%"`, ElevenLabs speed setting) rather than applying ffmpeg `atempo` afterward. This is an inference, not a sourced test.
- Word-level timestamps (edge-tts WordBoundary events, or Whisper alignment as in short-video-maker) give tighter caption sync than MoneyPrinterTurbo's proportional-by-character fallback.

### Gaps
- I found no independent A/B data (only vendor claims) on TTS vs human voice, or TTS speed, vs Shorts retention.
- I did not verify ShortGPT's or MoneyPrinter's (FujiwaraChoki) exact TTS speed defaults, or AutoShorts' silence-trim settings, in source files.

## 5. Sound design: music under voice, SFX, trending audio, sound-on data

### Takeaway
Mixing guides agree on these levels: voice around −14 LUFS integrated for YouTube/Spotify-style normalization, and music about 18–25 dB below the voice, ducking 15–25 dB with fast attack and slower release. Pipeline defaults of 0.15–0.2 linear gain are about −14 to −16.5 dB. On TikTok, sound is central to the experience per TikTok's own Kantar research (88% say sound is essential). Meta's widely quoted sound-off stats are old ad-feed figures, so captions remain insurance. Guidance on SFX is purely anecdotal: accent key beats and don't put a sound on every cut.

### Cited Findings
- **Music level under speech.** Background music should sit "between −20 dB and −30 dB while someone is speaking, rising to −12 dB to −18 dB in gaps." Aim for "music roughly 18 to 25 dB under speech, with the voice normalized near −14 LUFS." [Anecdotal/creator — audio guides] — [Pure Audio Insight](https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be); [Zella: music ducking](https://zellahq.com/blog/music-ducking-explained/)
- **Ducking parameters.** Duck depth about 15–25 dB, attack 10–30 ms, release 200–500 ms. "If you notice the music while the person talks, it's too loud… the gaps are where you should feel it." [Anecdotal/creator] — [OpenClip: audio ducking](https://openclip.app/learn/audio-ducking); [Zella](https://zellahq.com/blog/music-ducking-explained/)
- **Open-source precedent.** An openscreen PR titled "music beds start at −18 dB and duck under the voice." [Anecdotal/creator — code] — [openscreen PR #797](https://github.com/getopenscreen/openscreen/pull/797)
- **Loudness normalization.** Spotify, YouTube and Amazon use about −14 LUFS; Apple uses −16 LUFS for music and podcasts. [Anecdotal/creator — secondary summary of platform specs] — [Lance Blair VO: LUFS](https://lanceblairvo.com/lufs-voiceover-levels/)
- **Pipeline music defaults.** MoneyPrinterTurbo `bgm_volume = 0.2` and RedditVideoMakerBot background volume `0.15` (linear). [Anecdotal/creator — repo defaults] — [MoneyPrinterTurbo config](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/config.example.toml); [RedditVideoMakerBot config](https://github.com/elebumm/RedditVideoMakerBot/blob/master/utils/.config.template.toml)
- **TikTok/Kantar sound study.** 88% of TikTok users say sound is essential to the TikTok experience. 73% say they would "stop and look" at ads with audio. TikTok was the only platform where ads with audio generated significant lifts in both purchase intent and brand favorability. Sound is experienced as "fun" at a 66% higher rate than on other platforms. The study was commissioned by TikTok and conducted by Kantar (about 2021). [Official, platform-commissioned] — [Social Media Today](https://www.socialmediatoday.com/news/tiktok-shares-new-insights-into-the-importance-of-sound-for-marketing-promo/601569/); [TikTok for Business blog](https://ads.tiktok.com/business/en-US/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok)
- **Meta sound-off stats.** Meta research on mobile feed video ads found that 41% of videos were "basically meaningless without sound." 80% react negatively when feed ads play loudly unexpectedly, and captioned video ads increase view time by 12% on average. The often-repeated "85% of Facebook video watched sound-off" is from about 2016 feed video, not Reels. The "75% of Reels plays start muted" claim comes from a vendor blog with no primary source. [Official (older Meta ad research), plus unverified vendor claims] — [Meta for Business: updated features for video ads](https://www.facebook.com/business/news/updated-features-for-video-ads); [OpusClip (vendor)](https://www.opus.pro/blog/facebook-reels-caption-subtitle-best-practices)
- **SFX overuse.** "A video with a sound effect on every single cut starts to feel chaotic rather than polished." Reserve SFX for the "3–5 most important beats per video." Whooshes, pops, hits and risers are the standard short-form palette. [Anecdotal/creator; vendor blog] — [EseCut blog](https://esecut.com/blog/sound-effects-that-boost-engagement); [Krotos: balancing music and SFX](https://krotos.studio/blog/how-to-balance-music-and-sound-effects)

### Inferences
- **Practical mix for a TTS finance explainer:**
  - Voice normalized to about −14 LUFS integrated, peaks at or below −1 dBTP.
  - Music bed about −20 to −25 dB relative to voice while narration plays, swelling in gaps and on the payoff.
  - Sidechain ducking with about 20 ms attack and about 300 ms release.
  - SFX (whoosh on transitions, pop on number/text reveals, cash register on a money payoff) on key visual beats, about −6 to −12 dB under the voice. This SFX level is an inference from the ducking guidance, not sourced.
- **Trending audio.** For voiceover-led explainers, the voice *is* the audio. Trending-sound mechanics apply to music-led content. On TikTok, a low-volume trending track under the VO may help discovery via the sound page. I found no data confirming this for voiceover explainers.
- Keep burned-in captions, because Meta viewers may start muted and TikTok viewers mostly don't. This covers both cases.

### Gaps
- I found no official YouTube Shorts data on sound-on rates.
- I found no controlled data on whether SFX density or a trending sound under a voiceover changes retention for explainer shorts; all SFX guidance is creator opinion.
- I could not retrieve the full Kantar/TikTok methodology (sample size, markets) from the TikTok blog page, which rendered as navigation only.
