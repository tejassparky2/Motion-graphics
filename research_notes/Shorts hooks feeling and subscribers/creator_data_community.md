# Creator/analyst data and community findings on Shorts hooks, retention, loops and comments (2023-2026)

Scope note: this file adds what is new relative to `research_notes/Shorts retention for animated explainers/hooks_metrics_length.md`.
That file already covers YouTube's metric definitions (viewed vs swiped, engaged views, the March 31, 2025 view-count change,
APV over 100% from loops), the Meta/Nielsen and TikTok ads first-3-seconds studies, the Adobe Express 507-creator length survey,
and OpusClip's unsourced claims. They are not repeated here.

Labels: **[Data]** = disclosed sample and a measurement. **[Data, weak]** = sample given but method unclear, vendor or secondary.
**[Anecdotal]** = creator or vendor opinion, or numbers with no dataset.

Access limits in this session: reddit.com is blocked for both search and fetch, and the GitHub search API is blocked (the session is
bound to its own repos). So there are **no Reddit analytics threads and no GitHub repo survey in these notes**. See the Gaps sections.

## 1. Disclosed datasets: what they report on hooks, length, % viewed, viewed-vs-swiped, loops, captions, posting

### Takeaway
Only a few datasets disclose their samples:
- **Paddy Galloway, Apr 2023:** 5,400 Shorts, 33 channels, 3.3B views.
- **Socialinsider, 2026:** 69M short videos across platforms.
- **Metricool:** 5.7M short videos in 2025; 800k YouTube videos in 2026.
- **Snapchat SnapUGC, ECCV 2024:** 90k videos.

The most actionable findings:
- **Viewed vs swiped:** Shorts under 60% rarely do well; the winners sit at 70-90%.
- **Watch time, not length:** holding viewers for longer seconds tracks with views; length alone does not.
- **Engagement:** likes, comments and shares showed no strong link to performance in Galloway's data.
- **First 5 seconds:** in the Snapchat data, "still watching at 5 s" correlates 0.926 with normalised watch percentage, so the opening largely decides the whole curve.

No disclosed dataset was found from Retention Rabbit (on Shorts), vidIQ, TubeBuddy, Dash Hudson, Tubular, ClipFlip or Hootsuite on these questions.

### Cited Findings
**Paddy Galloway / Chris Gileta, "We studied 3.3 billion views to decode the YouTube Shorts algorithm" (X thread, Apr 14, 2023)**
- [Data] Sample: 33 channels across niches, 5,400 Shorts, 3.3B views. Medians were checked against averages. Galloway calls it "early research".
  — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html); [X](https://x.com/PaddyG96/status/1646898359808974851)
- [Data] **Length:** most Shorts in the sample were 20-40 s, and very short ones were rare. "Longer shorts in the study performed much better on average" (no exact figures; he notes other factors). — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Data] **Watch time:** "Shorts where the AVD was higher than 50 seconds averaged 4.1 million views. Just making a long short isn't the goal, making a short that holds people for as long as possible is." Outliers existed at every length. — [X](https://twitter.com/PaddyG96/status/1646898363466481664)
- [Data] **Viewed vs swiped away (VVSA):** the best performers typically fell between 70% and 90%. Under 60% means "probably in trouble". A high VVSA does not guarantee success. — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Data] **Engagement:** likes, shares and comments showed no strong relationship with performance. Galloway suspects YouTube may still use them for satisfaction scoring. — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Data] **Subscriber conversion:** on average, long-form converts more subscribers per 10k views than Shorts. For channels over 1M subscribers, Shorts converted better, which he theorises comes from better Shorts and stronger CTAs. — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Data] **RPM:** about $0.06 per 1,000 Shorts views, and Shorts length doesn't meaningfully change RPM (2023 numbers). — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Anecdotal] Hook advice in the same thread is not measured: make the first second "punchy and engaging" and "treat your intro like a thumbnail". The promised white paper was not found. — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- Attribution conflict: Piktochart credits a "5,400 Shorts" study to "Inflow Network" (50-60 s Shorts got ~22x the views of <10 s ones). The sample size matches Galloway's study, so this is most likely the same dataset misattributed. Treat the "22x" figure as unverified. — [Digital Information World](https://www.digitalinformationworld.com/2023/04/paddy-galloway-decoded-youtube-shorts.html); see the prior notes for the Piktochart snippet.

**Socialinsider, "TikTok vs. Reels vs. Shorts" (2026 edition)**
- [Data] 69M Shorts, Reels and TikTok videos posted Jan 2025 to Jul 2026. Engagement rate = (likes + comments) / followers x 100. — [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)
- [Data] Shorts average engagement rate was 0.27% (2025) and 0.30% (2026), the only platform up year on year (Reels 0.45%, TikTok 2.60%). — [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)
- [Data] Average views per Short by account size: under 5K followers 15,160; 5-10K 22,000; 10-50K 23,200; 50-100K 28,400; 100K-1M 58,400. Shorts had the highest average views of the three platforms in every bracket. — [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)
- [Data] Comments: about **10 per Short** on average, vs 20 for Reels and 50 for TikTok. Socialinsider frames Shorts as "a discovery feeder into long-form" rather than a discussion space. — [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)
- Caveat: the sample is brand/business accounts tracked by a social-media tool, not story/entertainment creators.

**Metricool**
- [Data] 2025 State of Short Video report: 5,696,685 short videos from 582,456 accounts. It reports Shorts engagement fell 36%. — [Marketing Tech News summary](https://www.marketingtechnews.net/news/what-the-data-tells-us-about-short-form-video-insights-from-metricools-2025-state-of-short-form-video-report/)
- [Data] 2026 YouTube study: 799,718 videos from 71,177 accounts. Short-form views rose 127% from 2025 to 2026. Comments rose from 0.50 to 0.69 per video, but the page doesn't say whether that covers Shorts. — [Metricool](https://metricool.com/youtube-statistics/)
- [Data, weak] A search summary attributes to the same 2026 study an average Shorts watch time of about 16 s and Shorts engagement of 4.94% (2025) vs 1.85% (2026). I couldn't confirm these on the fetched page. — [Metricool](https://metricool.com/youtube-statistics/)

**Snapchat SnapUGC (Li et al., ECCV 2024) and VQualA 2025 challenge (ICCV 2025 workshop)**
- [Data] 90,000 Snapchat Spotlight user videos, 10-60 s, each with more than 2,000 views. Two metrics:
  - **ECR** = share of viewers who watch past 5 s;
  - **NAWP** = average watch time normalised by duration.
  — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)
- [Data] **NAWP and ECR correlate at 0.926**: whether people get past second 5 almost determines how much of the video they watch. — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)
- [Data] Factors in the prediction model:
  - average watch percentage falls as duration rises;
  - classic "video quality" scores correlate only weakly with engagement (r ≈ 0.07-0.31);
  - background-sound features, titles and on-screen captions/visual-semantic features each added predictive power;
  - speech transcripts did not, because viewers decide before much speech has happened;
  - "visual emotion" features slightly hurt prediction.
  — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)
- [Data] VQualA 2025 challenge on the same data: 97 participants, 15 valid submissions. The winning large-multimodal-model ensemble found that adding audio clearly improved prediction ("the important role of audio"). — [ICCV 2025W](https://openaccess.thecvf.com/content/ICCV2025W/VQualA/html/Li_VQualA_2025_Challenge_on_Engagement_Prediction_for_Short_Videos_Methods_ICCVW_2025_paper.html); [arXiv 2508.02516](https://arxiv.org/html/2508.02516v2)

**Vendors with no usable Shorts data**
- [Data, weak / not Shorts] "Retention Rabbit 2025 report, 10,000+ videos: average YouTube retention 23.7%, educational up to 42%" is quoted only second-hand and is not Shorts-specific. — [virvid.ai](https://virvid.ai/blog/average-view-duration-vs-retention-youtube-2026)
- [Anecdotal] Benchmark blogs cite Shorts "average retention" of 40-55%, 70-85% or 73%, with no attribution. They contradict each other, so ignore them. — [humbleandbrag](https://humbleandbrag.com/blog/youtube-shorts-benchmarks); [retensis](https://retensis.com/blog/audience-retention-benchmarks-2026)
- [Anecdotal] "Shorts with an immediate hook in the first 2 seconds retain 19% more viewers" is credited to Zebracat 2025 stats. I couldn't find the underlying data. — [virvid.ai](https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026)
- [Anecdotal] Bytecap's "Shorts retention benchmarks" page (Jul 2026) says it is an "evidence synthesis—not a Bytecap customer-performance study". It gives **no** numeric benchmarks and stresses that YouTube compares a Short against your own "recent videos of similar length". — [Bytecap](https://www.bytecap.io/research/youtube-shorts-retention-benchmarks)

### Inferences
- The channel's best video (92% average viewed, 70.7% stayed to watch) sits at the bottom of Galloway's 70-90% "winner" band for viewed-vs-swiped. Hold is strong, so the cheapest gain is in the first second (stopping the swipe), not in the middle.
- SnapUGC's 0.926 correlation supports spending most creative effort on seconds 0-5. It also shows that narration alone doesn't decide early retention: the sound bed, on-screen text and visuals matter more than the words in the opening seconds.
- With engagement weakly tied to reach (Galloway) and Shorts drawing few comments overall (Socialinsider: ~10 per Short), the debate endings should be justified by satisfaction and identity, not by expected algorithmic lift.

### Gaps
- No disclosed Shorts datasets from vidIQ, TubeBuddy, Dash Hudson, Tubular Labs, ClipFlip or Hootsuite on hooks, length, viewed-vs-swiped or loops turned up in searches.
- No later Galloway Shorts study (2024-2026) was found; the 2023 thread predates the 3-minute Shorts limit and the 2025 view-count change.
- No dataset measures loop or rewatch rate directly.

## 2. MrBeast's leaked production handbook: what it says and what transfers to Shorts

### Takeaway
"How to succeed in MrBeast production":
- **What it is:** a 36-page internal handbook, leaked via Rosanna Pansino in Aug/Sep 2024. Two former producers confirmed it to Passionfruit; MrBeast's team did not comment.
- **What it's about:** long-form only.
- **What transfers to 40-50 s Shorts:** the first stretch has the most loss; match the promise immediately; stakes rise as the video goes on; no dull moments; a strong payoff and an abrupt ending; never signal the end.

### Cited Findings
- [Data, single-video anecdote] "The first minute of each video is the most important minute… As with almost every video on Youtube, the first minute has the most loss (go look)." Example: "On this particular video we lost 21 million viewers in the first minute." — [Alexander Jarvis transcription](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/)
- [Anecdotal, internal doctrine] The three metrics are CTR, AVD and AVP: "For your videos to do well you must get their AVD and AVP as high as possible… The longer people watch, the better a video will do." — [Jarvis](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/)
- [Anecdotal] Structure:
  - "Hook people at the start of the video, transition them to an amazing story that they are invested in, have no dull moments, and then have a satisfying payoff at the end of the video with an abrupt ending."
  - "As you get deeper in the video the stakes get higher."
  - "Strong payoffs at the end of videos boost retention."
  - "Don't ever signal the end of the video unless it's to build hype for the prize or payoff."
  — [Jarvis](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/)
- [Anecdotal] Expectation matching: viewers "feel like you were lied to and click off because the video did not meet the expectations of the title/thumbnail." On minutes 1-3: "Stop telling people what they will be watching and start showing them." — [Jarvis](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/)
- [Anecdotal] "Re-engagement" at fixed points (around 3 and 6 min in long-form) with a segment "only MrBeast can do", and "it's important we never lose our wow." — [Jarvis](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/)
- Provenance: Pansino posted it after a former employee sent it. Passionfruit says two former producers confirmed its legitimacy; a MrBeast spokesperson declined to comment. — [Passionfruit](https://passionfru.it/mrbeast-leaked-document-81151/); [Net Influencer](https://www.netinfluencer.com/mrbeast-productions-leaked-internal-document-rosanna-pansino/); [Gigazine](https://gigazine.net/gsc_news/en/20240917-mrbeast-youtube-production)

### Inferences
- Mapping long-form to a 45 s Short (my mapping, not in the document): "first minute" ≈ first 1-3 s; "minutes 1-3: show, don't tell" ≈ by second 5 the story is happening, not being announced; "re-engagement at 3/6 min" ≈ one twist or escalation around 40-60% of runtime (e.g. the authority freezing in a genie story); "abrupt ending after the payoff" matches Jenny Hoyos's last-second data (Q3).
- "Never signal the end" argues against outro lines ("Comment below…", "Follow for more") said *after* the payoff. If a debate question is used, it should be the payoff line itself, and the video should cut right on it.

### Gaps
- I didn't see the original PDF; quotes come from a full-text transcription (Jarvis). The handbook has no Shorts-specific guidance.

## 3. Hook types, loop endings, end payoffs and on-screen-text hooks: any A/B evidence?

### Takeaway
No public controlled A/B test comparing hook *types* (question vs bold claim vs mid-action vs POV vs contradiction vs numbered) on organic Shorts was found.

The best quantified practitioner evidence is Jenny Hoyos's own analytics (Creator Science, Oct 2023):
- a ~25-point retention cliff in a Short's final second; trimming 1 s raised overall retention from 83% to 88%;
- she treats 90%+ retention as the "bare minimum" for a breakout;
- she aims for ~34 s on YouTube;
- she scripts at a 5th-grade reading level or below.

Loop endings are described as a common practice (e.g. Zack D. Films) with no measured lift.

### Cited Findings
**Jenny Hoyos, Creator Science ep. 167 (Oct 10, 2023)**
- [Data, single creator] Retention: her average is 95% and her scroll-through (viewed) rate is 85%; she cites ~70% as an average scroll-through rate. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)
- [Data, single creator] **Ending cliff:** one Short held 70% at second 31 and 45% one second later. Overall retention went from 83% to 88% after cutting that last second. Her rule of thumb: losing 1 s of a 32 s Short costs ~3 points, 2 s ~6 points. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/); [Short "Jenny Hoyos method"](https://www.youtube.com/shorts/95JNCi489gA)
- [Anecdotal, from her data] 90%+ retention is "the bare minimum" for a Short to blow up. A Short under 30 s needs ~100%+ (i.e. replays) to take off. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)
- [Data, single creator] Her top videos average **34 s**. TikTok favoured 10-20 s for her, while YouTube favoured ~34 s. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)
- [Data, single creator] Readability: she targets a **5th-grade reading level or below**, from scraping transcripts of "thousands of shorts". She says MrBeast's Shorts read at about 1st-grade level, and one word ("business") can push a script from 5th to 8th grade. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)
- [Anecdotal] Structure:
  - Hook → Foreshadow (≤3 s) → Narrative ("but/therefore") → twist ending;
  - she writes the hook and foreshadow as two lines and always knows the last line before filming.
  — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/); [Gillian Perkins ep. 202](https://www.gillianperkins.com/blog/ep-202); [summary](https://youtubesummary.com/summary/As7abwNhG7Y)
- [Data, single creator] One Short held only 70% over its first 100k views and still reached ~10M, largely from returning viewers. Another had shares ≈ 20% of views. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)

**Loops and payoff**
- [Anecdotal] Zack D. Films (per a vendor blog with no cited sources): content "starts immediately and ends abruptly, often encouraging a re-watch", and the narrative "often leads back to the beginning, creating a seamless loop". The hook "is always visual" (e.g. a needle piercing skin at microscopic scale). — [iVideoNow](https://ivideonow.com/blog/why-zack-d-films-dominates-youtube-shorts-with-unsettling-3d-animation-content-en)
- [Anecdotal] Hook-type lists (vidIQ "18 viral hooks", Metricool "25 viral hooks", Creatify "24 hooks") are taxonomies without test data. — [vidIQ](https://vidiq.com/blog/post/viral-video-hooks-youtube-shorts/); [Metricool](https://metricool.com/viral-video-hooks/); [Creatify](https://creatify.ai/blog/24-red-hot-scroll-stopping-hooks-to-increase-video-retention-on-tiktok)
- [Data, adjacent] SnapUGC: on-screen caption/visual-semantic features predicted early retention better than speech transcripts. That indirectly supports text-on-screen hooks over spoken-only hooks in the first seconds. — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)

### Inferences
- For this channel, the Hoyos ending data is the most transferable number: end on the payoff or debate line and cut within a few frames. A trailing "Either way…" callback should be checked in YouTube Studio's retention curve for a final-second cliff.
- A 5th-grade reading level matters more when a TTS voice reads to a multilingual audience (India/Philippines: English is often a second language). Short words, one idea per sentence (already a channel rule).
- A genie-story ending can loop naturally: if the closing either/or line echoes the opening on-screen hook text, a replay reads as intended. This is untested; measure APV over 100% and the rewatch bump on the retention graph.

### Gaps
- No A/B data on hook type, POV hooks, numbered hooks or contradiction hooks on organic Shorts.
- No measured loop-ending lift on YouTube Shorts.
- Hoyos's numbers are from 2023 (pre-3-minute Shorts and pre-March-2025 view counting) and from a single live-action creator.

## 4. Reddit / community analytics threads and GitHub/open datasets

### Takeaway
Reddit (r/NewTubers, r/PartneredYoutube, r/youtubers, r/YouTubeShorts) is blocked in this environment for both search and fetch, so no first-hand creator analytics threads were collected. The GitHub search API is also blocked here.

The best open dataset found is Snapchat's SnapUGC (90k short videos, public GitHub: dasongli1/SnapUGC_Engagement). There is no public YouTube Shorts retention dataset.

### Cited Findings
- [Data] SnapUGC repo is linked from the paper (github.com/dasongli1/SnapUGC_Engagement). It contains 90k Snapchat Spotlight videos with ECR and NAWP labels. — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)
- [Anecdotal] Blogs summarising community practice agree on two points:
  - YouTube publishes **no official benchmark** for viewed-vs-swiped or retention;
  - Studio compares each Short against the channel's own recent median, which is the useful yardstick.
  — [retensis](https://retensis.com/blog/youtube-shorts-viewed-vs-swiped-away); [Bytecap](https://www.bytecap.io/research/youtube-shorts-retention-benchmarks); [creatoressentials](https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/)
- [Anecdotal] A 2026 blog by one growth analyst says it tracked 40 data-video accounts for six months, finding higher average view duration on Shorts and a higher per-video ceiling on TikTok. Method not verifiable. — [data-reel-maker blog](https://data-reel-maker.lovable.app/blog/youtube-shorts-vs-tiktok-for-data-creators)

### Inferences
- The channel's own Studio data (Sep 29-Oct 11 analysis already in CLAUDE.md) is a stronger evidence base than anything public for this niche. Keep logging viewed-vs-swiped and APV per hook type.

### Gaps
- Reddit threads with real swipe rates, APV and subscriber-per-view numbers: **not collected (access blocked)**. A future session with Reddit access, or the owner pasting threads, could fill this.
- GitHub repo survey: **not done (API blocked)**.

## 5. Case studies: animated / story Shorts channels

### Takeaway
**Zack D. Films** is the biggest animated-Shorts case:
- 3D, US, founded Jun 2021, all-CGI from 2023;
- about 26-29M+ subscribers and 65-72B views by mid-2026;
- visual-first hooks on curiosity, medical, "what if" and disturbing-truth topics, under 60 s;
- abrupt endings, frequent loop-backs, 4-5 uploads a day, produced by a freelancer pipeline.

Indian animated storytelling is dominated by kids' moral-story channels and animated horror. No reliable, sourced breakdown of specific Hinglish story-Shorts channels (Abhay Create style) or Filipino animated story Shorts was found.

### Cited Findings
- [Data, third-party tracker] Zack D. Films stats: 27.6M subscribers, 20.0M average views, 71.8B total views (undated tracker). A mid-2026 blog says 26M+ subscribers and 65B views; a fandom wiki lists 29M. The figures are from different dates. — [OutlierKit](https://outlierkit.com/resources/faceless-youtube-channels/); [iVideoNow](https://ivideonow.com/blog/why-zack-d-films-dominates-youtube-shorts-with-unsettling-3d-animation-content-en); [Fandom](https://zackdfilms.fandom.com/wiki/Zack_D._Films)
- [Anecdotal] Format: about 1-minute fact Shorts on world history, "deep meanings", disturbing truths, "what if" scenarios and medical topics. Formula: "identify a common but misunderstood process, visualize it with precise CGI, and deliver the explanation with high-velocity narration". The logo is built into the 3D scene. Output: 4-5 videos a day (~150 a month). "How Stitches Work" passed 250M views. — [iVideoNow](https://ivideonow.com/blog/why-zack-d-films-dominates-youtube-shorts-with-unsettling-3d-animation-content-en); [YouTube fandom](https://youtube.fandom.com/wiki/Zack_D._Films)
- [Anecdotal, first-hand freelancer] One freelancer says they made "over 100" shorts for the channel using Blender, Cascadeur, BlenderKit, After Effects and EmberGen, with very short turnaround per video. — [Chris Reilly portfolio](https://supersets.chrisreillyportfolio.com/zackdfilms.php)
- [Data, third-party trackers] Indian animated storytelling:
  - Infobells-Hindi: ~70.3M subscribers (kids' rhymes and moral stories) — [Famekeeda](https://www.famekeeda.com/blogs/top-youtube-channels-by-subscribers/);
  - Scary Pumpkin (animated Hindi horror): ~3.72M subscribers and 913M+ views, Aug 2026 — [Parikshit Khanna](https://www.parikshitkhanna.com/post/top-10-hindi-horror-storytellers-on-youtube-in-2025);
  - "Hindi Moral Stories": ~2.85M subscribers but only 12 videos and tiny current daily views (Nov 2025), showing how stale subscriber counts mislead — [vidIQ stats](https://vidiq.com/youtube-stats/channel/UC5oMqcCaOTTT-5l8s5uYt4A/).
- [Data, single creator, live-action] Jenny Hoyos (budget-cooking story Shorts) averages ~10M views per Short with a story structure (hook, foreshadow, but/therefore, twist) at ~34 s. This is the best-documented *story* Shorts case. — [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)

### Inferences
- What Zack D. Films and Hoyos share with this channel: one premise per video, visual proof in frame 0, no outro, an abrupt cut after the payoff, and huge volume (Zack D.) or a strict cut-down of ideas (Hoyos: ~1,000 ideas → ~10 made).
- Where this channel differs: its stories are argument and dialogue driven, not spectacle driven. So the frame-0 equivalent of Zack D.'s needle-through-skin is a character mid-conflict plus the contradiction in big text (already the channel rule).

### Gaps
- No interview with Zack D. Films (Zachary Dziadul) on strategy or analytics.
- No Social Blade growth curves were retrieved, and Social Blade wasn't fetched.
- No sourced analysis of Abhay Create-style Hinglish animated Shorts, Filipino storytelling Shorts, riddle/paradox animation channels or "what if" channels (e.g. retention, length, growth).

## 6. 2D vs 3D animation in Shorts

### Takeaway
No data comparing 2D vs 3D (or realistic vs cartoon) performance on Shorts was found. The available material is studio marketing on both sides. The one large dataset that tested visual "quality" (SnapUGC) found technical quality scores only weakly correlated with engagement (r ≈ 0.07-0.31).

### Cited Findings
- [Anecdotal] 3D studios claim higher engagement for 3D without numbers; 2D studios argue cost and speed suit Shorts. — [Whizzy Studios](https://www.whizzystudios.com/post/creating-viral-youtube-shorts-with-3d-animation-what-works-in-2025); [AniJam](https://www.anijam.ai/blog/2d-vs-3d-animation/); [Educational Voice](https://educationalvoice.co.uk/youtube-animation-content/)
- [Anecdotal] "Younger viewers often prefer 3D's dynamic look" is unsourced. — [Educational Voice](https://educationalvoice.co.uk/2d-vs-3d-animation/)
- [Data, adjacent] Visual-quality (MOS) scores correlate weakly with engagement; semantic content (what is shown, captions, sound) predicts better. — [arXiv 2410.00289](https://arxiv.org/html/2410.00289v1)

### Inferences
- The biggest animated-Shorts success (Zack D. Films) is 3D, but its edge plausibly comes from its *subject* (visceral close-ups of bodies and processes) and volume, not from the 3D itself. That can't be separated from the evidence. A controlled test on this channel (same script, 2D vs 3D, e.g. the robot-butler 3D sample) would be the only real evidence.

### Gaps
- No public A/B test or cross-channel analysis by animation style.

## 7. Comment-bait vs genuine debate endings; pinned comments; replying to comments

### Takeaway
- **Replying to comments:** the strongest data is Buffer's 2025 fixed-effects study of ~2M posts on 6 platforms, with lifts of +5% to +42%. YouTube and TikTok were *not* included.
- **Question endings and pinned comments on Shorts:** no measured evidence; it's advice only.
- **Engagement bait:** Meta officially demotes it (2017). No equivalent YouTube Shorts statement was found.
- **Algorithmic value of comments:** Galloway found engagement (comments included) not strongly linked to Shorts performance.

### Cited Findings
- [Data] Buffer, "Replying to comments boosts engagement" (Nov 12, 2025):
  - sample: nearly 2M posts from 220k+ accounts;
  - method: fixed-effects regression comparing each account to itself (controls for size, location, niche), plus a z-score check;
  - results: Threads +42% (128k posts), LinkedIn +30% (72k), Instagram +21% (700k+ posts, ~68k accounts; holds after controlling for whether a post got comments), Facebook +9% reactions, X +8% (p≈0.097, marginal), Bluesky +5%;
  - caveats: authors call it "directional", and causality isn't established; no YouTube data.
  — [Buffer](https://buffer.com/resources/replying-to-comments-boosts-engagement/)
- [Official, Meta] Facebook (Dec 2017) demotes posts that use "engagement bait" (e.g. "LIKE this if you're an Aries!"), with stricter demotion for Pages that do it repeatedly. Posts asking for help, advice or recommendations are not affected. — [Meta Newsroom](https://about.fb.com/news/2017/12/news-feed-fyi-fighting-engagement-bait-on-facebook/)
- [Official, Meta] Mosseri on Threads: "We've seen an increase in engagement-bait on Threads and we're working to get it under control." — [MediaPost](https://www.mediapost.com/publications/article/400061/threads-has-an-engagement-bait-problem.html)
- [Data] Shorts average ~10 comments per video vs 20 for Reels and 50 for TikTok (Socialinsider, 69M videos, brand accounts). — [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)
- [Data] Galloway 2023: likes, shares and comments showed no strong relationship with Shorts views. — [Thread Reader](https://threadreaderapp.com/thread/1646898356419981315.html)
- [Anecdotal] A coach claims that a question ending, a pinned comment and fast replies "typically lift engagement rate by 30-40%" across client channels. This has no dataset. — [ytshark](https://ytshark.com/?p=740)
- [Official feature] YouTube lets creators reply to comments with a Short, which notifies the commenter, and added a filter for replied comments. No published lift data. — [DesignRush](https://news.designrush.com/youtube-shorts-engagement-features-content-creators)

### Inferences
- Meta's line between demoted "bait" and allowed "asking for help/advice/recommendations" lines up with the owner's rule: a meaningful two-sided question is fine; "comment YES or NO" is the pattern platforms penalise.
- Since comments barely predict Shorts reach (Galloway) but replies raise engagement on other platforms (Buffer), the debate format's value is likely community and return viewing (Hoyos's ~10M-view Short grew "largely from returning viewers"). Replying to comments with a Short is the one officially supported tool that both reaches commenters and creates new content.
- Per MrBeast's "never signal the end": put the debate question in the story's last line (spoken by the narrator or a character) and cut on it, rather than adding a separate "comment below" outro.

### Gaps
- No YouTube-specific data on reply effects, pinned comments or question endings.
- No YouTube policy statement on engagement bait in Shorts was found in this session.
