# Visual Pacing and On-Screen Captions for Short-Form Vertical Explainers (2D Animated)

Evidence labels: [Official] = platform/company first-party; [Academic] = peer-reviewed; [Data study] = vendor/aggregator analysis of many videos (usually correlational, methodology often thin); [Anecdotal/creator] = rules of thumb, opinion. Research date: 2026-09-29.

## Q1. Measured shot/cut lengths and "visual change every N seconds"

### Takeaway
Hard academic data exists for film (Hollywood ASL fell from about 10 s in the 1930s-40s to under 4 s after 2000, with more motion inside shots), and TV-pacing research shows cuts trigger orienting responses but memory peaks at medium pacing and drops at high pacing, especially with arousing content. For Shorts/TikTok specifically, I found no peer-reviewed measurement of average shot length; the widely repeated "cut every 2-3 seconds" and "2.5 s clips = 35% higher completion" figures come from vendor blogs with no published methodology.

### Cited Findings
- [Academic] Cutting, DeLong & Nothelfer (2010, Psychological Science) analyzed 150 Hollywood films (1935-2005); shot lengths became more correlated with neighbors over time, with power spectra approaching 1/f, a pattern also seen in human attention/reaction-time fluctuations; authors suggest 1/f shot structure may help "harness observers' attention" to the narrative — [SAGE](https://journals.sagepub.com/doi/10.1177/0956797610361679); [PubMed](https://pubmed.ncbi.nlm.nih.gov/20424081/); [Cornell Chronicle](https://news.cornell.edu/stories/2010/03/study-pattern-movies-mimics-found-our-brain)
- [Academic] Cutting et al. (2011, i-Perception, "Quicker, Faster, Darker"), 160 films 1935-2010: ASLs "of about 10 s in the 1930s and 1940s falling to below 4 s after 2000" (r = -.75 with year). Visual Activity Index (motion) rose linearly (r = .583), e.g., Barry Lyndon (1975) VAI 0.008 vs Toy Story 3 (2010) VAI 0.122. In modern films, shorter shots carry proportionately more motion. Authors: faster films "demand a reorientation of visual attention"; short shots force eye movements "to quickly reevaluate each new visual depiction and increasing heart rate"; filmmakers have tuned these dimensions to "better control the eye movements and the attention of the viewer" — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/); [DOI](https://doi.org/10.1068/i0441aap)
- [Academic] Annie Lang's Limited Capacity Model: structural features (cuts, edits, effects) elicit involuntary orienting responses; camera cuts are the most studied structural feature and reliably produce orienting responses — [Lang 1990, Communication Research](https://journals.sagepub.com/doi/10.1177/009365090017003001); [Fox, Park & Lang 2007](https://journals.sagepub.com/doi/abs/10.1177/0093650207300429)
- [Academic] Lang, Bolls, Potter & Kawahara (1999, J. Broadcasting & Electronic Media 43(4)): fast pace and arousing content both raise self-reported arousal; the combination of fast pace + arousing content overloads processing, reducing recognition and cued recall; for non-arousing content, memory rose with pacing, peaking at medium and declining at high pacing — [Taylor & Francis](https://www.tandfonline.com/doi/abs/10.1080/08838159909364504); [Semantic Scholar](https://www.semanticscholar.org/paper/The-effects-of-production-pacing-and-arousing-on-of-Lang-Bolls/4eb8a8e71793bb2ad29fb3daa110f01061fad750)
- [Academic, secondary summary — not verified in primary] A search-summary claim that recognition dropped off sharply once cuts exceeded 10 in two minutes is attributed to this research line (OSU dissertation "The Role of Emotional State and Production Pacing") — [OhioLINK ETD](https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=osu1276636393&disposition=inline). I could not extract the exact passage from the PDF; treat as unverified.
- [Data study, no methodology] Vidpros: "Analysis of the top 100 Shorts in 2024 showed an average clip length of 2.5 seconds correlated with 35% higher completion rates than those with clips averaging 4+ seconds." The page gives no sample definition, method, or data source (links only to its own blog) — [Vidpros](https://vidpros.com/video-clip-length/)
- [Data study, correlational] ClipFlip (2026), 44,000 clips submitted to its platform across TikTok/Shorts/Reels/X: "Fast-paced clips outperform slow, polished ones by 2.4x on average"; recommends cutting every 2-3 seconds maximum; top-1% clips have "the first frame is already interesting"; claims a "0.8 seconds" decision window. How "fast-paced" was measured is not stated; sample is self-selected users of the tool — [ClipFlip](https://www.clipflip.io/resources/how-to-make-viral-clips)
- [Official] TikTok for Business: "faster scene changes typically draw viewers in early"; "90% of ad recall impact is captured within the first six seconds" (ads context, no cut-rate number given) — [TikTok Creative Codes blog](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads)
- [Anecdotal/creator] Taylor Gunn (editor/producer, claims 7B+ views, worked with MrBeast) has an essay titled "Retention Editing Isn't What You Think" pushing back on "cut faster, add more elements" doctrine; body is paywalled so specific claims could not be verified — [Substack](https://thetaylorgunn.substack.com/p/retention-editing-isnt-what-you-think)
- [Anecdotal/creator] Overediting critique: "retention editing" doctrine of cutting faster and adding elements risks "confusing fatigue for finesse" — [George Blackman, Retention Rabbit newsletter](https://georgeblackman.substack.com/p/rr11-were-all-trapped?open=false)

### Inferences
- The "change something every 2-3 s" rule is consistent in direction with film ASL trends (<4 s) and orienting-response research, but its specific number is a creator/vendor heuristic, not a measured Shorts norm.
- Lang's inverted-U (memory peaks at medium pacing, overload at high pacing, worse with arousing content) is directly relevant to finance explainers: numbers must be encoded, so a pure "cut every 1 s" style may hurt comprehension even if it holds the eye. A reasonable design target: a visual change (cut, zoom step, new element, number pop) every ~1.5-3 s, but keep a key number on screen long enough to read, and avoid stacking fast cuts on already emotionally loaded moments.
- Cutting's finding that shorter shots carry more motion suggests "change" can be motion within a shot (camera push, element entering) rather than only hard cuts — well suited to 2D animation where a single "scene" can evolve continuously.

### Gaps
- No peer-reviewed measurement of average shot length for viral TikToks/Shorts/Reels found.
- No controlled study (A/B with retention curves) of cut rate on Shorts retention found; vendor numbers are correlational and unaudited.
- "Pattern interrupt" as a term appears only in creator/marketing discourse; no academic study using that label found (closest academic construct: orienting response to structural features, Lang).

## Q2. Editing techniques that hold attention (punch-ins, scale bumps, whips, first-frame motion, synced text pops, color)

### Takeaway
Platform docs endorse fast early scene changes, a hook in the first seconds, readable text, and native/creator style; vendor data says the first frame must already be interesting. Specific techniques (punch-ins, whip pans, scale bumps) are supported by editor consensus, not by published controlled data.

### Cited Findings
- [Official] TikTok: "creative attributes that get people to read increase view time, drive recall, and make ads more likable"; product on screen drives "a 65% increase in brand affinity and 25% uplift in recall"; CTA cards "45% lift in recall and a 19% increase in likeability"; TikTok-first ads "drive 3.3x more action" — [TikTok Creative Codes](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads)
- [Official] YouTube/Google Ads: using sound (music, voiceover, or both) in Shorts ads "has been shown to increase conversions by over 20%"; keep Shorts ads under 60 s; only the first 60 s play in the Shorts feed — [Google Ads Help: Shorts ads asset specs](https://support.google.com/google-ads/answer/16041697?hl=en)
- [Official, 2016-era feed] Meta: "Since most video ads in mobile feed are viewed without sound, make sure to express your message visually" — [Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads)
- [Data study] ClipFlip: first frame "already interesting" is "the single biggest differentiator between clips that get 10K views and clips that get 10M views"; native-feeling clips get "3x more engagement" than ad-like clips — [ClipFlip](https://www.clipflip.io/resources/how-to-make-viral-clips)
- [Academic] Motion inside shots increased alongside shorter shots in modern film (VAI up, r = .583), i.e., camera/character movement is part of how modern editing holds gaze — [Cutting et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)
- [Anecdotal/creator] Rule-of-thumb that clips in edits should change every 1-2 seconds (search-summary of an Adobe community FAQ thread on where to cut) — [Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/faq-discussion-learning-to-edit-how-do-i-decide-where-to-cut/m-p/10642153/highlight/true)

### Inferences
- For a 2D finance short, "punch-in" equivalents are virtual camera scale steps (e.g., 100% -> 110-120%) on beat with narration emphasis, and number pops (scale overshoot + settle) synced to the spoken number; both create a structural-feature orienting cue without a hard cut.
- TikTok's "get people to read" finding supports making the handwritten numbers themselves the visual event (large, center-safe, timed to the word).

### Gaps
- No public data isolating punch-ins, whip transitions, scale bumps, or color/contrast changes as retention drivers; Reddit editing subreddit threads were not surfaced by search in usable form (no verifiable quotes collected).

## Q3. Captions/subtitles and watch time/retention

### Takeaway
The famous caption stats come from the sound-off Facebook feed era (2016-2019) and from surveys, not retention measurements on sound-on vertical feeds. TikTok and Reels are predominantly sound-on. Captions still help comprehension/accessibility and are near-universal among short-form creators, but I found no published controlled evidence that word-by-word "kinetic" captions beat static captions on retention.

### Cited Findings
- [Official, 2016, feed ads, sound-off context] Meta/Facebook: "Internal tests show that captioned video ads increase video view time by an average of 12%"; case example A&W Canada: "Adding captions increased watch time by 25%" (post undated on page; widely reported as 2016) — [Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads); [Social Media Today](https://www.socialmediatoday.com/social-business/facebook-adds-automated-captions-video-ads-offers-tips-improve-video-performance); [3Play Media](https://www.3playmedia.com/blog/captions-increase-viewership-for-facebook-video-ads/)
- [Data study — survey, 2019] Verizon Media + Publicis Media: online survey of 5,616 U.S. adults 18-54 (April 2019); 69% view video with sound off in public places; 80% more likely to watch an entire video when captions are available (commonly paraphrased as "more likely to finish"); 50% say captions important because they watch sound-off; 80% of caption users are not hearing-impaired. This is self-report, not measured retention — [Forbes](https://www.forbes.com/sites/tjmccue/2019/07/31/verizon-media-says-69-percent-of-consumers-watching-video-with-sound-off/); [3Play Media](https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/); [Streaming Media](https://www.streamingmedia.com/Articles/ReadArticle.aspx?ArticleID=131860)
- [Official] TikTok: "88% of TikTok users" say "sound is vital to the TikTok experience" (from TikTok's "Evolution of Sound" research series) — [TikTok Creative Codes](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads); [TikTok Evolution of Sound Vol. 1](https://ads.tiktok.com/business/en-US/blog/evolution-of-sound-volume-1?redirected=1)
- [Official via secondary — unverified] "80 percent of Reels are viewed with the sound on" is attributed to Meta's Reels ads page; I could not load Meta's page (login wall), only secondary restatements — [Metricool](https://metricool.com/facebook-reels-ads-guide/); [Meta page (login-walled)](https://www.facebook.com/business/ads/facebook-instagram-reels-ads)
- [Academic] Szarkowska et al. (2024, PLOS ONE), 161 participants (UK, Australian, Polish L2), 6-min Netflix clips with subtitles, sound on vs off: comprehension 81.30% vs 77.70% (small effect); recall 80.87% vs 78.14% (n.s.); effort 3.07 vs 4.84; frustration 2.01 vs 3.63; immersion 5.43 vs 4.73; enjoyment 5.52 vs 4.47 (1-7 scales); subtitle total reading time 996 ms vs 1253 ms; skipping 0.055 vs 0.023 — i.e., with sound on, viewers still read subtitles but skip more and spend less time on them — [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0306251)
- [Academic] Kruger & Steyn (2014, Reading Research Quarterly): significant positive correlation between subtitle reading and comprehension — [Wiley](https://ila.onlinelibrary.wiley.com/doi/10.1002/rrq.59); related: Kruger, Hefer & Matthew (2014) on attention distribution and cognitive load in subtitled lectures (L1 vs L2) — [researchgate overview](https://www.researchgate.net/publication/324174969_The_Development_of_Eye_Tracking_in_Empirical_Research_on_Subtitling_and_Captioning)
- [Data study, descriptive] OpusClip (Jan-Mar 2026, 13.5M clips on its platform, organic): 80.2% use captions; 78.6% of clips use animated captions vs ~1.6% static; 4.5% text overlays. This is adoption data only; no retention lift was quantified — [OpusClip research](https://www.opus.pro/research/best-caption-strategy-short-form)
- [Anecdotal/vendor] Submagic markets its "Animated" word-by-word highlight style as the strongest performer in its TikTok completion-rate test; no test data published — search-summary of [Submagic](https://www.submagic.co/ai-caption) and third-party comparisons ([Montaj](https://www.trymontaj.com/en/vs/submagic-vs-opus-clip))

### Inferences
- The 69% / 80% / +12% stats should be labeled as 2016-2019 feed-era, sound-off context. On TikTok/Reels (sound-on dominant), captions function more as a second attention channel and comprehension aid than as a sound replacement.
- Szarkowska 2024 implies viewers keep reading on-screen text even with audio; for Indian finance explainers (often Hinglish or English as L2 for many viewers), captions likely aid comprehension of numbers and terms. This is inference from general subtitle research, not Shorts-specific.
- Kinetic word-by-word captions are the de facto norm (OpusClip adoption data), so their benefit is best viewed as "table stakes"; the evidence for a retention lift over static captions is vendor anecdote only.

### Gaps
- No independent A/B study on word-by-word vs phrase captions for retention found.
- No eye-tracking study of kinetic/highlighted captions on vertical video found.
- Underlying survey year/sample for TikTok's "88% sound is vital" not visible in fetched pages.

## Q4. Caption best practices and safe zones

### Takeaway
Keep captions in the upper-middle/center of the 9:16 frame, clear of the bottom ~25-35% (captions, buttons, CTA) and the right edge (engagement buttons). Meta's Reels guide gives explicit percentages (14% top / 35% bottom / 6% sides). YouTube and TikTok official numeric safe zones were only available via secondary sources or template files.

### Cited Findings
- [Official via quotation] Meta Ads Guide (Instagram Reels): "Consider leaving roughly 14% of the top, 35% of the bottom, and 6% on each side of your asset free from text, logos, or other key creative elements" = ~269 px top, 672 px bottom, 65 px sides on 1080x1920. Reported that Meta unified the Stories/Reels 9:16 safe zone in March 2026 — [behaviour.digital](https://behaviour.digital/post/meta-reels-safe-zone-14-top-35-bottom-6-sides-the-2026-official-guide); [AdNabu](https://blog.adnabu.com/meta-ads/meta-safe-zones/)
- [Secondary summary of Google guidance] YouTube Shorts: avoid critical elements in the top 10%, bottom 25%, and right 10% where channel name, caption and engagement buttons sit; Google provides downloadable transparent PNG safe-zone templates for vertical video — [Strike Social](https://strikesocial.com/blog/maximize-ad-visibility-and-cut-through-the-noise-with-safe-zone-guides/); [Google Ads Help: vertical video](https://support.google.com/google-ads/answer/9128498?hl=en)
- [Secondary, conflicting] Google's vertical template safe area reported as 840x960 px starting 288 px from top and 48 px from left — [poster.ly](https://www.poster.ly/tools/youtube-shorts-safe-zone-checker); other sites give 900x1350 (180 top / 390 bottom / 60 sides) or ~888x1500 — [Hopper HQ](https://www.hopperhq.com/blog/youtube-shorts-dimensions/); [YouTube Toolkit](https://www.youtubetoolkit.com/blog/youtube-shorts-dimensions). Figures conflict; use Google's PNG template as ground truth.
- [Official, text length] Shorts ad description text overflowing 1 line on mobile is truncated — [Google Ads Help](https://support.google.com/google-ads/answer/16041697?hl=en)
- [Secondary, conflicting] TikTok: keep key text 108 px from top, 320 px from bottom, 60 px left, 120 px right; a 2026 guide says top 130 / bottom 484 / right 140 / left ~44 px. TikTok official phrasing: "Place your main creative elements in the central area to avoid UI obstruction" — [House of Marketers](https://houseofmarketers.com/guide-to-safe-zones-tiktok-facebook-instagram-stories-reels/); [Zeely](https://zeely.ai/blog/tiktok-safe-zones/); [TikTok TopView specs](https://ads.tiktok.com/help/article/tiktok-reservation-topview)
- [Official, sound on] Captions on Reels still recommended by Meta to catch the non-sound-on minority (per secondary restatement) — [Metricool](https://metricool.com/facebook-reels-ads-guide/)
- [Anecdotal/creator] Keep captions at least 120 px from top and 300 px above bottom on Shorts — [YouTube Toolkit](https://www.youtubetoolkit.com/blog/youtube-shorts-dimensions)

### Inferences
- A single cross-platform caption band that satisfies all three: vertical center to roughly 55-62% down the frame (below faces, above the 35% Meta bottom band which starts at y≈1248 px on 1920), horizontally inset ≥65 px left and ≥140 px right.
- Chunk size: GitHub tools default to 1 line and 2-3 words (see Q6); combined with Szarkowska's reading-time data (~1 s per subtitle with audio), short 1-3 word chunks lower reading load for fast narration.

### Gaps
- Official YouTube and TikTok pixel safe zones could not be read directly from first-party pages (template PNGs / login-gated ads docs); numbers above are secondary.
- No evidence-based font size or words-per-chunk standard for vertical video found; only tool defaults and creator habits.

## Q5. 2D animation specifics: constant motion, boil, secondary animation, limited animation

### Takeaway
I found no data linking animation technique (boil, secondary motion, limited animation) to Shorts retention. The academic film evidence (more motion per shot in modern film) and animation craft principles support "never fully static" frames, but that link is inference.

### Cited Findings
- [Academic] Modern films have more motion, and shorter shots carry proportionately more motion; the 2010 animated film Toy Story 3 had among the highest visual activity index cited (0.122) — [Cutting et al. 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)
- [Anecdotal/craft] Secondary animation is additional motion that emphasizes the main action and makes character motion feel natural — [School of Motion](https://schoolofmotion.com/blog/secondary-animation); [Wikipedia: Secondary animation](https://en.wikipedia.org/wiki/Secondary_animation)
- [Reference] Limited animation reuses frames/cels of character animation to reduce drawing load — [Wikipedia: Limited animation](https://en.wikipedia.org/wiki/Limited_animation); historical defense of limited styles as an aesthetic — [Animation Obsessive](https://animationobsessive.substack.com/p/dont-call-it-limited-animation?open=false)
- [Craft reference] Kurzgesagt teaches its motion-graphics approach publicly (Skillshare class series) — [Skillshare](https://www.skillshare.com/en/classes/motion-graphics-with-kurzgesagt-part-1/631970755)

### Inferences
- For simple-character finance shorts, cheap "alive" signals: idle loops (breathing, blinking), line boil on held drawings, slow camera drift/push during holds, and number write-on animations. These supply the within-shot motion that Cutting's data associates with modern short-ASL editing, without extra drawing cost.

### Gaps
- No Reddit/r/animation or r/AfterEffects thread with verifiable quotes on boil/limited animation vs retention was retrieved.
- No channel-level case study (e.g., Indian finance explainer channels) with retention graphs found.

## Q6. Automated shorts pipelines: subtitle timing on GitHub

### Takeaway
Open-source pipelines use Whisper/faster-whisper with word_timestamps to time captions; segmentation is either punctuation-driven (MoneyPrinterTurbo) or fixed small chunks with the current word highlighted (captacity, other caption repos, 1 line / 2-3 words).

### Cited Findings
- [Repo] MoneyPrinterTurbo `app/services/subtitle.py`: faster-whisper with `word_timestamps=True`, default `model_size` "large-v3", `compute_type` "int8", `beam_size` 5, VAD filter `min_silence_duration_ms=500`; lines split at punctuation (trailing punctuation removed), no explicit max-length constraint in that logic; a `word_level` option emits one subtitle per word — [GitHub](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/app/services/subtitle.py); subtitle provider configurable to "whisper" with model e.g. "large-v3-turbo" — [Riffkit guide](https://riffkit.ai/blog/how-to-use-moneyprinterturbo)
- [Repo] captacity (Whisper + MoviePy, for YouTube Shorts): params include `font_size` (example 130), `font_color` (yellow), `stroke_width` 3 black, `shadow_strength`/`shadow_blur`, `highlight_current_word` True, `word_highlight_color` (red), `line_count` 1, `padding` 50, `use_local_whisper` — [README](https://github.com/unconv/captacity/blob/master/README.md)
- [Repo] kaushal07wick/Captions: Whisper micro-captions of 2-3 words with dynamic highlight burn-in — [GitHub](https://github.com/kaushal07wick/Captions)
- [Repo] AutoCaption: faster-whisper + Silero VAD for word-level timestamps, short-form presets — [GitHub](https://github.com/Mightyiest/AutoCaption)
- [Repo] openai/whisper exposes `max_line_width`, `max_line_count`, and `max_words_per_line` for subtitle writers (require word timestamps) — [Discussion #1482](https://github.com/openai/whisper/discussions/1482); [faster-whisper issue #738](https://github.com/SYSTRAN/faster-whisper/issues/738)

### Inferences
- A practical pipeline default: word timestamps from (faster-)whisper/WhisperX, chunks of 1-3 words, one line, current-word highlight, and forced breaks at punctuation; hand-pin large numbers (₹ amounts, %) as separate animated graphics timed to the word timestamp rather than relying on caption text.

### Gaps
- ShortGPT and WhisperX-specific caption defaults were not verified in this session.
