# Hooks, retention, looping and subscriber conversion for short-form comedy skits (YouTube Shorts first)

Scope note: the earlier report at `reports/Shorts retention for animated explainers.md` (G1–G34) already covers the official metric definitions (viewed-vs-swiped, engaged views, Instagram skip rate), the 2023 Galloway/Gileta 5,400-Short VVSA benchmarks, the TikTok auction-ads "63% in the first 3 s" figure, Facebook IQ's 1.7 s, Guo et al. on speaking rate, Cutting on shot length, Szarkowska on subtitles, Kang on curiosity, and tool defaults for dead air. These notes do not repeat that material except where a new source adds a number or contradicts it. New here: the MrBeast document read from a primary text copy, VidMob×TikTok hook data (1,678 ads), the OpusClip 2026 clip dataset, quso.ai's 108k-Short length dataset (2026), Dash Social's 2025 H2 benchmark, the Dashlet swipe-timing study, Berger & Milkman's regression figures and amusement experiment, Teixeira et al. on surprise vs joy, Galloway's subscriber-conversion numbers, and an audit of the subscriber/series/loop/comment claims that circulate (most are untraceable).

Evidence labels: **[Data]** = dataset or controlled study with a stated method; **[Official]** = platform or platform staff; **[Opinion]** = creator/analyst/vendor advice without disclosed data; **[Unverified]** = a number that circulates with no traceable primary source.

## Key question 1: What data exists on the first 1–3 seconds (swipe-away rates, hook types)?

### Takeaway
Measured evidence says the swipe decision is made at the very start and that the first seconds carry a disproportionate share of all drop-off, but no public dataset compares organic hook *types* (in-medias-res vs question vs text vs pattern-interrupt) on Shorts. The best quantified hook findings come from TikTok paid-ad research (VidMob×TikTok, 1,678 ads) and favour a person talking straight to camera, "everyday" people over celebrities, no logo, and stating the point in the first 3 s; the widely repeated "90% of underperforming TikToks fail in the first 3 s" and "19% more retention with a 2-second hook" have no traceable method.

### Cited Findings
- **[Data]** Swipe timing is bimodal: in a user study with 133 Mechanical Turk workers and 15,344 swipes (plus a college-campus cohort), "users are most likely to swipe either soon after the video playback begins or at the tail end of the video"; 29% of swipes fell in the first 20% of a video and 42% in the last 20%, and only 6% of College-Campus swipes fell in the 60–80% region. Per-video swipe distributions were stable across the two user groups (KL divergence 0.2 median), i.e. the video, not the viewer pool, mostly determines where people swipe — [Dashlet, arXiv 2204.12954 (2022)](https://arxiv.org/pdf/2204.12954)
- **[Data, ads]** VidMob×TikTok analysis of 1,678 ads / 7.3 billion impressions (1 Jan–15 Oct 2023): a direct-to-camera talking head gave a 14% lift in 2-second view-through rate and "+50% hooking power"; everyday people were 1.7× more likely to hook than celebrities, celebrities showed a 13% lower 6-s VTR; a logo on screen cut 6-s VTR by 14%; outdoor locations cut 6-s view time by 26%; ads that "hook viewers in the first 6 seconds" showed 2× engagement and +43% purchase intent — [VidMob, TikTok hook analysis](https://vidmob.com/resource/tiktok-hook-analysis). Caveats: paid ads, no control groups or significance reported, co-branded vendor piece.
- **[Data, ads]** TikTok's "How to Hook" study (2023, Metrixlab, US/UK/GCC) is only available second-hand through the VidMob page above; no sample size is published — [VidMob](https://vidmob.com/resource/tiktok-hook-analysis)
- **[Data, ads]** "Over 63% of all videos with the highest click-through rate highlight their key message or product within the first 3 seconds"; text overlays appear in 40% and fourth-wall breaks in 33% of top view-through ads — [TikTok for Business auction-ads PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf) (already in the earlier report; included because every other "63%" citation traces back here)
- **[Data, vendor, selection-biased]** OpusClip's hook taxonomy run over 34,635 clips processed through its own engine (Jan–Mar 2026): the top hook type ("product/outcome showcase") averaged 6,037 views per clip, "roughly 2× the lowest-ranked hook type" — [OpusClip, TikTok hooks that go viral 2026](https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026). The same company's posts assert "90% of underperforming TikToks fail in the first 3 seconds" and that the algorithm decides in "about 1.5 seconds" with no methodology — [OpusClip, first 3 seconds 2026](https://www.opus.pro/blog/viral-tiktoks-first-3-seconds-2026). **[Unverified]**
- **[Vendor, source unstated]** "50–60% of drop-offs" on Shorts occur in the first 3 seconds, attributed to "data from thousands of Shorts" with no dataset named; the author recommends >70% retention past 3 s as "healthy" — [OpusClip, ideal Shorts length & format (Nov 2025)](https://opus.pro/blog/ideal-youtube-shorts-length-format-retention)
- **[Data, 2023, correlational]** Galloway & Gileta (5,400 Shorts, 33 channels): best performers had 70–90% viewed-vs-swiped, under 60% "typically did not perform well"; advice: "work on hooks if VVSA is 60% or lower" and "treat your video like a thumbnail" — [BAM summary of the Galloway thread](https://nowbam.com/decoding-the-youtube-shorts-algorithm/)
- **[Official]** YouTube's Shorts product lead Todd Sherman (Creator Insider, Aug 2023): Shorts viewers are "swiping through a feed and discovering content as they go", a view is counted on intent to watch ("deliberately watching it"), not every swipe is a view; the system first finds a "seed audience" ("find a set of people that may enjoy your video") and the video grows or tapers from there — [MediaPost, 25 Aug 2023](https://www.mediapost.com/publications/article/388588/)
- **[Data, lab]** Teixeira, Wedel & Pieters (JMR 2012; 58 adults, 28 thirty-second ads, facial-expression coding + eye tracking + zapping): the *level* of surprise drives attention concentration, the *velocity* (rate of increase) of joy drives retention (less zapping); Teixeira's summary: "advertisers should use a quick element of surprise at the beginning of an ad, followed by a longer period of joy" — [HBS Working Knowledge](https://hbswk.hbs.edu/item/6807.html) (page returned 403 on fetch; quote taken from search-result excerpt); paper listing — [Tilburg University](https://research.tilburguniversity.edu/en/publications/emotion-induced-engagement-in-internet-video-ads/)
- **[Unverified]** "Shorts with an immediate hook in the first 2 seconds retain 19% more viewers" (attributed to Zebracat 2025, relayed by a creator blog, no data located) — [virvid.ai](https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026)
- **[Opinion]** "High-retention Shorts hold at least 80% of viewers through the first 3 seconds" — vendor guide citing other blogs — [GoFaceless](https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes)

### Inferences
- The Dashlet data is the only independent measurement of *when* people swipe. For a skit, it means the two places to engineer are the first 1–2 seconds (the early swipe mode) and the last seconds (the tail mode, where a swipe is normal and harmless if the joke already landed, but costly if the punchline is still coming).
- The ad findings translate into a skit rule set: open on a person already talking to someone (or to camera), not a title card, logo, or establishing shot; put the premise in words (voice and on-screen text) inside 3 s; "everyday" characters over glossy ones.
- Teixeira's surprise-then-joy pattern maps directly onto a skit: a surprising first line/image (the contradiction) to grab, then a rising line of jokes (joy *velocity*, i.e. each beat funnier than the last) to hold. A skit whose funniest line is first should lose more viewers in the middle than one that escalates.
- No source distinguishes hook types for organic Shorts, so the channel's own viewed-vs-swiped comparison (already done in CLAUDE.md: scene-with-something-wrong 75–78% vs "Meet X"/bare question 36–52%) is as good as any public dataset for this channel and should keep being the arbiter.

### Gaps
- No public A/B or large-sample study compares hook types (question vs in-medias-res vs text hook vs pattern interrupt) on organic Shorts; everything available is paid-ad research or vendor taxonomies with selection bias.
- TikTok's primary "How to Hook" report (Metrixlab 2023) could not be located; only VidMob's retelling exists.
- No peer-reviewed 2024–2026 paper measuring swipe decisions in the first seconds on YouTube Shorts was found (the MDPI 2025 TikTok study is about post-exposure cognition, not swipe timing).

## Key question 2: Paddy Galloway's Shorts analyses and the MrBeast production document; what transfers to 60 s skits

### Takeaway
Galloway's only disclosed dataset (5,400 Shorts, 2023) gives benchmarks for viewed-vs-swiped, length and subscriber conversion; no newer Galloway Shorts dataset or skit-specific analysis was found. The MrBeast document (read from a text copy) is explicit about minute-by-minute structure for ~13-minute videos; its transferable principles for a 60 s skit are front-loading, "hype to execution" (stop telling, start showing), a planned re-engagement before boredom sets in, stair-stepping stakes, never signalling the ending, and an abrupt ending right after the payoff.

### Cited Findings
- **[Data, 2023]** Galloway & Gileta, 5,400 Shorts from 33 channels: most creators post 20–40 s Shorts; 50–60 s Shorts got the most views on average; Shorts with AVD over 50 s averaged 4.1M views and those with AVD 40–50 s averaged 1.8M — [BAM summary](https://nowbam.com/decoding-the-youtube-shorts-algorithm/). The Publish Press reports the same study as "Shorts of 50–60 seconds performed best, averaging 1.7 million views" (a length bucket, versus BAM's AVD bucket; both numbers are from charts in the thread) — [The Publish Press, 17 Apr 2023](https://news.thepublishpress.com/p/are-shorts-worth-it)
- **[Data, 2023]** Same study: long-form converted 22.7 subscribers per 10,000 views vs 16.9 for Shorts; for channels over 1M subscribers the pattern reversed; Galloway's theory: big channels make better Shorts and use stronger calls to action — [The Publish Press](https://news.thepublishpress.com/p/are-shorts-worth-it)
- **[Data, 2023]** Same study: average Shorts RPM about 6 cents per 1,000 views, with length (10–60 s) making little difference — [The Publish Press](https://news.thepublishpress.com/p/are-shorts-worth-it)
- **[Opinion, Galloway]** "Treat your video like a thumbnail" (the first second must do the thumbnail's job) — [BAM summary](https://nowbam.com/decoding-the-youtube-shorts-algorithm/)
- **[Primary text, authenticity reported by Passionfruit via two former producers]** The MrBeast document ("How to Succeed at MrBeast Production", 36 pp., posted by Rosanna Pansino 13 Aug 2024): "the metrics you care about in regards to virality are CTR, AVD, and AVP" — [text copy of the PDF](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf); context and authenticity: [Tubefilter](https://www.tubefilter.com/2024/09/17/mrbeast-internal-production-guide-leaked-key-points/), [Passionfruit](https://passionfru.it/?p=81390)
- **[Primary text]** On the opening: "As with almost every video on Youtube, the first minute has the most loss (go look). This is why we freak out so much about the first minute"; on a 60M-click video "we lost 21 million viewers in the first minute … (which surprisingly compared to other channels is above average)"; causes listed: poor lighting, not matching "the expectations of the clickbait", not pre-planning what to say, and not "front load[ing] some interesting stuff" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Primary text]** Minutes 1–3: "transition from hype to execution … Stop telling people what they will be watching and start showing them"; "crazy progression" (cover multiple days in the first 3 minutes so the viewer is "super invested"); the "3 minute re-engagement" is "content that is highly interest[ing] that fits the story and makes people genuinely impressed … a segment that 'only MrBeast can do this'", inserted "because they could get bored of the story and click off" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Primary text]** Minutes 3–6: "all the most exciting and interesting content that is also very simple … lots of quick scene changes and highly stimulating simple content"; "If we can get them to watch the first half of the video there's a very high chance they'll watch to the end"; a second re-engagement at ~6 min; back half: once invested viewers are in a "lull"; "Don't ever signal the end of the video unless it's to build hype for the prize or payoff" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Primary text]** Summary rule: "Hook people at the start of the video, transition them to an amazing story that they are invested in, have no dull moments, and then have a satisfying payoff at the end of the video with an abrupt ending"; "The video endings must always be abrupt to protect retention"; formats that hold: "last to leave" (winner withheld until the end) and "stair stepping" ($1 → $10 → $50 → $375 → $1,000 → $10,000 → $40,000 → $100,000 → world record: "as you get deeper in the video the stakes get higher") — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Primary text]** "Wow factor": the one thing no other creator can do (the house lowered by crane 30 s into "100 days in the circle"), "arguably from a data standpoint illogical" but "does make them watch more videos and engage more with the brand" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf). (Opinion inside a primary document.)
- **[Primary text]** Two videos of equal length: the one watched "a minute and 38 seconds longer" on average got 120M views vs 45M ("first day data") — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Context]** Independent summaries confirm the same structure (first minute, re-engagements near minute 3 and 6, crane example) — [OMR (German)](https://omr.com/de/daily/mrbeast-doc-pdf-leak), [GIGAZINE](https://gigazine.net/gsc_news/en/20240917-mrbeast-youtube-production)

### Inferences
- Scaling the MrBeast template to a 60 s skit (proportionally: first minute ≈ first 5 s; "1–3 min" ≈ 5–15 s; "3–6 min" ≈ 15–30 s; back half ≈ 30–60 s): (a) first 5 s must match the on-screen "title" promise and show, not announce; (b) by ~15 s the premise must already be in motion with the first laugh; (c) plan one deliberate re-engagement (a new rule, a reversal, a new character) around the 40–50% mark where a one-joke premise goes stale; (d) escalate ("stair step") rather than repeat the same gag at the same level; (e) hold the resolution to the final seconds, never signal the ending, and cut on the last word.
- Galloway's 50–60 s "most views" finding and quso.ai's 11–20 s median peak (Q5) are not contradictory once the metrics are read: mean views from 33 large channels in 2023 vs median views across 1,900+ mostly small creators in 2025–26. For a story that needs 40–50 s, the 2023 big-channel data is the closer analogue.

### Gaps
- No Galloway publication specific to comedy skits or to Shorts after the 2024 three-minute change was found; his X threads could not be fetched directly.
- The MrBeast text copy is 8 pages of extracted text (the original is 36 pages with charts); the retention-chart numbers referenced in it are not in the text.

## Key question 3: Pacing (cut frequency, line length, dead air) and captions/sound-off viewing

### Takeaway
No new measured data on cut frequency or dead air for Shorts was found beyond what the earlier report covers; the circulating "cut every 2–4 s" and "captions +15–25% retention" figures are unsourced. The only controlled caption number is a YouTube (long-form) +7.32% views lift, and the "85% watch without sound" figure traces back to 2016 Facebook feed data.

### Cited Findings
- **[Vendor, unsourced]** "Cuts every 2–4 seconds" for high-performing Shorts ("data suggests"), "burned-in captions raise retention by 15–25%", "new beat every 5–7 s" for storytelling Shorts, comedy/entertainment sweet spot 18–28 s — [OpusClip, Nov 2025](https://opus.pro/blog/ideal-youtube-shorts-length-format-retention)
- **[Data, long-form YouTube]** DDN/3Play Media study: captioned videos saw a 7.32% overall increase in views — [3Play Media](https://www.3playmedia.com/blog/studies-find-captions-improve-engagement)
- **[Audit of a stat]** The common "85% of video is watched without sound" traces back to 2016 Facebook feed data from publisher self-reporting; the "69%/25%" sound-off preference figures come from a Verizon Media/Publicis Media survey relayed in a 2024 PLoS One eye-tracking paper — [VoxBooster roundup](https://voxbooster.com/blog/captions-subtitles-statistics-2026) **[Unverified beyond the roundup]**
- **[Unverified]** Meta "captioned video ads increased view time by an average of 12%" could not be confirmed against Meta's own materials — [3Play Media](https://www.3playmedia.com/blog/studies-find-captions-improve-engagement)
- **[Primary text, MrBeast]** Mid-video section is "lots of quick scene changes and highly stimulating simple content that reflects the story"; "have no dull moments" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Official]** Sherman: creators should "focus on content quality and on how much time their story actually needs" — [MediaPost](https://www.mediapost.com/publications/article/388588/)
- **[Survey of creators, not performance]** Adobe Express survey of 507 creators with ≥1,000 subscribers: under 30 s was named the ideal length for views/shares/click-throughs/saves by an average of 46% of creators; entertainment and comedy creators leaned toward under-30-second Shorts — [Adobe Express](https://www.adobe.com/express/learn/blog/youtube-shorts-length-study)

### Inferences
- For a dialogue skit the unit of pacing is the *line exchange*, not the cut: every line should change something (a new piece of information, a reversal, a reaction shot). The MrBeast "quick scene changes" and the earlier report's one-visual-change-per-second rule both support cutting on every speaker change and inserting a reaction beat rather than holding a two-shot.
- Captions: keep burning them in (comprehension insurance), but do not expect a measurable retention lift from caption *style*; no sound-off retention data for Shorts exists.

### Gaps
- No measured data on dead air or inter-line gaps for Shorts (unchanged from the earlier report).
- No study measures the effect of caption style (karaoke vs static) on Shorts retention; vendor claims only.

## Key question 4: Open loops / curiosity gap, seamless loop endings, rewatch and whether loops help or inflate metrics

### Takeaway
Official definitions show that loops do not count toward *engaged* views but do count toward the public view number since 31 Mar 2025, so a seamless loop inflates views and average-percentage-viewed without proving satisfaction; there is no official statement that replays are a ranking input, and all "10% replay rate boosts distribution" claims are unsourced. Withholding the payoff to the end is the one loop-related tactic with a primary-source rationale (MrBeast's "last to leave"/stair-stepping) and a measured analogue (Dashlet: swipes cluster at the tail, so the payoff must land before the natural tail-swipe point).

### Cited Findings
- **[Official]** Engaged views count viewers who "stayed to watch past the initial seconds, not including any loops"; average percentage viewed is "the average percentage of a video watched among those who stayed to watch" — [YouTube Help](https://support.google.com/youtube/answer/12220281)
- **[Official, reported]** From 31 Mar 2025 a public Shorts view counts every start or replay with no minimum watch time; engaged views still govern monetisation — [TechCrunch, 26 Mar 2025](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted); replays can therefore inflate raw view counts — [Shortimize](https://www.shortimize.com/blog/how-to-analyze-youtube-shorts-performance)
- **[Data, brands]** Dash Social 2025 H2 YouTube benchmark: "retention at 99% for Shorts and 65% for On-Demand" (brand accounts; Dash's percentage-viewed figures for Shorts sit near 100%, consistent with looped playback counting toward percentage viewed) — [Dash Social 2025 H2 YouTube benchmark PDF](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/youtube.pdf)
- **[Official]** Sherman's Creator Insider interview covered views, seed audiences and length; the MediaPost write-up does not quote him on loops or replays; the reporter's statement that watch time, re-watches, likes, shares and comments are "likely" considered is explicitly the reporter's inference — [MediaPost](https://www.mediapost.com/publications/article/388588/)
- **[Opinion/anecdote]** A creator account of a Short that "always hit completion but never grew" until a callback "button" was added at the end to make the loop feel intentional, after which rewatches and distribution rose — single anecdote, no numbers — [Deeside, Jan 2026](https://www.deeside.com/the-shorts-recommendation-loop-a-practical-map-of-signals-you-can-actually-influence/)
- **[Vendor, unsourced]** "A 10% replay rate can significantly boost distribution" — [OpusClip](https://opus.pro/blog/ideal-youtube-shorts-length-format-retention); "Shorts with natural loop structure can achieve retention above 100%" — [virvid.ai](https://virvid.ai/blog/looping-structure-shorts-retention-2026)
- **[Primary text, MrBeast]** "Strong payoffs at the end of videos boost retention"; "last to leave" works because "the winner isn't revealed until the end"; "Don't ever signal the end of the video" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Data]** Swipes cluster in the last 20% of a video (42% of MTurk swipes), including auto-advance at completion — [Dashlet](https://arxiv.org/pdf/2204.12954)
- **[Opinion]** The Shorts feed "test-batch" model (strong early retention earns a bigger batch) and "retention should be treated as evidence of viewer satisfaction rather than a target for misleading hooks or forced loops" — [GoFaceless](https://www.gofaceless.ai/tr/blog/youtube-shorts-retention-strategy)

### Inferences
- A seamless loop is a cheap, low-risk polish (it cannot hurt APV and raises the public view count), but it should not be mistaken for a retention strategy; the channel's own stayed-to-watch % and viewed-vs-swiped are the honest numbers and are unaffected by loops.
- For a skit, "open loop" = the first line sets up a question a character must answer ("but the teacher just smiles"); "payoff" = the last line. Because tail swipes are normal, the punchline must be the final spoken line and the video must end within ~0.5 s of it; any tag after the punchline is watched by almost no one and drags APV.
- A deliberate callback in the last line to the first image makes the loop rewatchable *and* serves as the closing joke; this is the one loop technique that also improves the comedy.

### Gaps
- No official or large-sample evidence that replays/loops are a ranking signal on Shorts; everything is practitioner belief.
- No data on open-loop vs closed-premise openings for skits specifically (the curiosity-gap literature in the earlier report is about information, not jokes).

## Key question 5: Ideal length; completion vs length; 60–180 s Shorts since Oct 2024

### Takeaway
The two largest datasets disagree in a way that is explained by sample and metric: quso.ai (108,138 Shorts, median views, mostly small creators, 2025–26) peaks at 11–20 s and falls steadily after 30 s, while Galloway (5,400 Shorts, 33 large channels, mean views, 2023) peaks at 50–60 s. YouTube says recommendation is "independent of duration". No primary data on 60–180 s Shorts performance exists; vendor completion-rate brackets by length are unsourced.

### Cited Findings
- **[Data, 2026]** quso.ai: 108,138 YouTube Shorts (live ≥14 days) from a 508k-post dataset of 1,900+ creators in 80+ countries; median views by length: 0–10 s 514; 11–20 s 901 (peak); 21–30 s 542; 31–45 s 347; 46–60 s 188; 61–90 s 186; 90 s+ 51. No retention data by length; the page's claim that "retention erodes faster than extra runtime pays back" is not supported by its own numbers — [quso.ai, 29 Jun 2026](https://quso.ai/research/youtube-shorts-length)
- **[Data, 2023]** Galloway & Gileta: 50–60 s Shorts most views on average; higher AVD buckets averaged more views (AVD >50 s: 4.1M; 40–50 s: 1.8M) — [BAM](https://nowbam.com/decoding-the-youtube-shorts-algorithm/); 50–60 s "averaging 1.7 million views" — [The Publish Press](https://news.thepublishpress.com/p/are-shorts-worth-it)
- **[Official]** Sherman: "What we try to do in recommendations is independent of duration, to figure out if someone really enjoyed the video"; "there's not a certain length that benefits creators"; a user's own watch history may favour shorter or longer videos — [RouteNote summary of Creator Insider, 2023](https://routenote.com/blog/youtube-shorts-algorithm/); [MediaPost](https://www.mediapost.com/publications/article/388588/)
- **[Official, reported]** Shorts up to 3 minutes from 15 Oct 2024 — [Social Media Today](https://www.socialmediatoday.com/news/youtube-expands-3-minute-shorts-to-all-users/736967/)
- **[Data, brands]** Dash Social 2025 H2: Shorts averaged 36K views per post at 3.6% engagement vs 200.5K views at 2.9% for On-Demand video; Shorts views per post down 20% vs six months earlier; "On-Demand videos generate nearly six times more views than Shorts. While Shorts see fewer views but significantly more likes, comments, and shares" — [Dash Social PDF](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/youtube.pdf)
- **[Unverified]** Vidooly "over 2 million Shorts" finding that 40–60 s had the highest average views; "watch time on Shorts grew 50% year-over-year" after the 3-minute change — both relayed by a vendor blog with no primary link — [argil.ai](https://www.argil.ai/blog/how-long-can-youtube-shorts-be)
- **[Unverified]** Completion brackets "under 30 s: 70–85%; 60–120 s: 30–45%" — no study cited — [AdCreate](https://adcreate.com/blog/youtube-shorts-length-guide-2026); "50–60 s Shorts show the highest average completion rate at 76%" — no primary source — [AWISEE](https://awisee.com/blog/youtube-shorts-statistics/)
- **[Opinion]** 60–180 s Shorts "show promise in niches such as tutorials, vlogs, and explainers but … are still under-tested" — [Toptal](https://www.toptal.com/creator/post/youtube-shorts-length)
- **[Vendor]** The most common length in OpusClip's dataset is 30–60 s, which "describes what people produce, not what performs best" — [Bytecap](https://www.bytecap.io/research/best-youtube-shorts-length)

### Inferences
- Median-views-by-length is confounded: small creators who pad to 60 s are over-represented in the longer buckets, and completion mechanically falls with length. The owner's 40–50 s target is inside the band where the large-channel data (Galloway) peaks and the small-creator data (quso) is already declining; the channel's own first-24-hour views and stayed-to-watch % by length are the only decisive evidence.
- For a comedy skit there is a specific reason to stay under ~50 s: both the Adobe creator survey (comedy creators prefer <30 s) and the OpusClip vendor sweet spot (18–28 s) point shorter for comedy than for explainers, and jokes do not tolerate padding. 60–180 s should be tried only for a multi-beat story with an escalation ladder, and judged against the channel's own numbers.

### Gaps
- No primary YouTube data or analyst dataset on 60–180 s Shorts performance after Oct 2024; no completion-vs-length dataset with a stated method was found.

## Key question 6: Subscriber conversion from Shorts (series, recurring characters, CTAs, pinned comments)

### Takeaway
The only measured conversion figures are Galloway's 2023 numbers (Shorts 16.9 vs long-form 22.7 subscribers per 10,000 views, reversing for 1M+ channels). The series/recurring-character claims that circulate ("67% higher", "2–3× higher") have no traceable dataset. The best-attested lever in a primary document is MrBeast's "wow factor"/signature idea making people "watch more videos", which is opinion.

### Cited Findings
- **[Data, 2023]** Long-form 22.7 vs Shorts 16.9 new subscribers per 10,000 views; reversed for channels over 1M subscribers; Galloway attributes the reversal to better Shorts and stronger calls to action; "Shorts are not a major growth driver compared to longform" — [The Publish Press](https://news.thepublishpress.com/p/are-shorts-worth-it)
- **[Data, brands]** Dash Social: average monthly follower growth 1.4% across YouTube brand accounts (2.2% for 0–20K, 1.2% for 20–150K, 1.0% for 150K+) — [Dash Social PDF](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/youtube.pdf)
- **[Unverified]** "Series-format Shorts get 67% higher subscriber conversion than standalone videos" — repeated across vendor blogs with no dataset — [virvid.ai](https://virvid.ai/blog/turning-shorts-views-into-subscribers-2026); "structured multi-episode series see conversion two to three times higher" citing unnamed "creator analytics platforms"; "comedic character series can suffer format fatigue faster than explainer series" — [Influencers Time](https://www.influencers-time.com/youtube-shorts-series-how-to-turn-viewers-into-subscribers/)
- **[Opinion/heuristic]** Shorts subscriber conversion of 0.1–0.5% is "good", above 0.5% "exceptional" — [Subscribr](https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-growth)
- **[Opinion, vendor]** Shortimize's conversion guide contains no numbers; it recommends hooks, consistency and explicit subscribe CTAs as unquantified advice — [Shortimize](https://shortimize.com/blog/converting-shorts-into-subscribers-analyzing-youtube-shorts-for-channel-growth)
- **[Primary text, MrBeast; opinion]** Doing "something that no other creator can do … makes our videos more special to them … it does make them watch more videos and engage more with the brand" — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- **[Case, no numbers]** Alan Chikin Chow (described by Buffer as the most-watched Shorts creator, ~30M subscribers, slapstick skits) posts a new Short every day and "is constantly trying new video techniques and approaches to see what hooks viewers"; strategy built with Underscore Talent after early Shorts underperformed — [Tubefilter, 2021](https://tubefilter.com/2021/05/26/creators-on-the-rise-alan-chikin-chow/); [Buffer](https://buffer.com/resources//youtube-shorts-creators/)
- **[Official, context]** Sherman: aside from breaking news, "what creators post matters more than when they post" — [MediaPost](https://www.mediapost.com/publications/article/388588/)

### Inferences
- With ~1.7 subs per 1,000 Shorts views as the only external benchmark, a channel can set its own target and test series vs one-offs internally; the public "series converts 67% better" number should not be quoted.
- Recurring characters/premises are still the defensible bet for comedy, for a reason that does not need the fake statistic: a subscription is a bet on the *next* video, and a named format (The Last Bencher, the genie rule-breaker) tells the viewer what the next one will be. The Influencers Time warning about faster fatigue for comedic character series argues for rotating characters inside a stable premise, which matches the owner's "never two of the same character in a row".
- Galloway's observed reversal for big channels (stronger CTAs) plus MrBeast's "never signal the end" suggest the CTA belongs in the pinned comment and description, not spoken before the punchline; a spoken ask after the punchline is in the tail-swipe zone and reaches few viewers.

### Gaps
- No measured evidence that pinned comments, end-screen CTAs or recurring characters change Shorts subscriber conversion; no data on what *hurts* conversion beyond opinion.

## Key question 7: Emotion and sharing (Berger & Milkman 2012; surprise/joy) and application to skits

### Takeaway
Berger & Milkman's NYT dataset shows sharing rises with high-arousal emotion (awe +30%, anger +34%, anxiety +21% odds per SD) and falls with sadness (−16%), and their lab study shows amusement increases sharing through arousal; Teixeira et al. show surprise captures attention while rising joy retains viewers. For a skit: surprise first, escalate the laughs, keep energy high, avoid low-arousal endings.

### Cited Findings
- **[Data]** Berger & Milkman, JMR 2012: ~7,000 New York Times articles over three months (most-emailed list as the outcome); a one-SD increase in awe raised the odds of making the list by 30%, anger by 34%, anxiety by 21%, practical value by 30%, interest by 25%, emotionality by 18%, surprise by 14%; sadness lowered them by 16%; positive content was more viral than negative; effects hold controlling for surprise, interest, usefulness and placement — [Berger & Milkman PDF](https://cssh.northeastern.edu/pandemic-teaching-initiative/wp-content/uploads/sites/43/2020/09/What-Makes-Online-Content-Viral.pdf)
- **[Data, lab]** Study 2a (N = 49): a high-amusement version of an ad story evoked more arousal (M = 3.73 vs 2.92) and was more likely to be shared, with arousal mediating the effect (Sobel z = 2.02, p < .05); Study 2b (N = 45, anger) and Study 3 (N = 47, sadness reduced arousal and sharing) completed the pattern — [Berger & Milkman PDF](https://cssh.northeastern.edu/pandemic-teaching-initiative/wp-content/uploads/sites/43/2020/09/What-Makes-Online-Content-Viral.pdf)
- **[Data, lab]** Teixeira, Wedel & Pieters 2012: level of surprise → attention; velocity of joy → retention; joy effect asymmetric (gains from increases exceed losses from decreases); recommended design "a quick element of surprise at the beginning … followed by a longer period of joy" — [HBS Working Knowledge](https://hbswk.hbs.edu/item/6807.html) (quote via search excerpt; page returned 403), [Tilburg listing](https://research.tilburguniversity.edu/en/publications/emotion-induced-engagement-in-internet-video-ads/)
- **[Opinion]** Rage-bait pieces claim "20% higher spreadability" for outrage posts with no source — [minnano-rakuraku](https://minnano-rakuraku.com/contents/en/ragebaiting-en-23430/) **[Unverified]**
- **[Official, Instagram]** Mosseri's ranking signals for Reels reach: watch time, likes per reach and sends per reach, with sends "slightly more important" for non-followers (from the earlier report) — [Social Media Today](https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/)

### Inferences
- Humour is a high-arousal positive emotion, so the Berger & Milkman mechanism applies directly: the share-worthy skit is the one that produces a laugh-out-loud *spike*, not gentle amusement. Warmth alone (low arousal) predicts fewer shares; warmth plus surprise (the "aww then ha" turn) is the better ending.
- Teixeira's joy-*velocity* finding argues for escalation: three jokes of rising size beat three equal jokes. The asymmetry (drops in joy cost less than rises gain) means a quiet set-up beat mid-skit is affordable if the next beat climbs.
- Anger/anxiety also drive sharing, which is why debate endings work; the owner's "always meaningful, never rage-bait" rule is consistent with using a two-sided question (mild arousal, defensible) rather than outrage.

### Gaps
- No study measures humour type (absurdist vs relatable vs cringe) against Shorts shares or retention; Berger & Milkman is text news, Teixeira is 30-second TV-style ads.

## Key question 8: What drives comments, and do comments matter for Shorts distribution?

### Takeaway
No official YouTube statement or dataset shows comments as a Shorts ranking input; the MediaPost write-up explicitly labels that idea the reporter's inference. Dash Social's brand data shows Shorts earn more comments per view than long-form, and engagement-bait tactics (deliberate errors, "which one are you") are documented only as practitioner tactics, with no measured effect size.

### Cited Findings
- **[Official]** Sherman's interview covers intent-to-view and seed audiences; the claim that likes, comments and shares are weighed is "the reporter's inference, and YouTube does not publish its calculations" — [MediaPost](https://www.mediapost.com/publications/article/388588/)
- **[Data, brands]** "While Shorts see fewer views … significantly more likes, comments, and shares" than On-Demand video; brand accounts average 29 comments per post across all YouTube formats (4 for 0–20K-follower brands, 71 for 150K+) — [Dash Social PDF](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/youtube.pdf)
- **[Opinion]** Engagement-bait glossary lists "saying something slightly wrong so experts must correct it" as a subtle form, notes audiences often call out the tactic and that the call-outs themselves generate comments — [Socialync](https://www.socialync.io/glossary/engagement-bait)
- **[Opinion]** "Right-baiting": a creator places an inconsistency to draw corrective comments and typically does not reply — [Substack essay](https://fjday.substack.com/p/algorithmic-outrage-from-rage-bait)
- **[Opinion]** Corrections are rewarded because ranking moved from chronological to engagement-based — [Pettauer](https://pettauer.net/en/rage-bait-in-the-digital-attention-economy/)
- **[Opinion]** GoFaceless: retention is the main feed signal; treat it as satisfaction evidence rather than a target for bait — [GoFaceless](https://www.gofaceless.ai/tr/blog/youtube-shorts-retention-strategy)

### Inferences
- Since comments are not a documented Shorts ranking input but are a documented strength of the format (Dash Social), the practical value of a debate ending is (a) the comment thread as a second content surface the owner already uses for debate replies, and (b) the arousal/share effect (Q7), not a presumed algorithm boost.
- Deliberate mistakes as bait are documented only as a tactic people detect and resent; they conflict with the owner's "always meaningful" rule and with the correction-shaped comments they produce. A genuinely two-sided question ("Did the teacher win, or dodge?") gets the comment without the credibility cost.

### Gaps
- No study of what question types ("which one are you", either/or, deliberate error) produce the most comments on Shorts.
- No official confirmation that comments, likes or shares influence Shorts distribution; Instagram (Mosseri) is the only platform with named engagement signals, and it names sends, not comments.
- Meta's 2017 engagement-bait demotion policy is relevant precedent but was not fetched in this session, so no URL is given.

## Key question 9: Concrete rules for a 30–75 s comedy skit Short (synthesis of the above)

### Takeaway
The measured evidence supports a small number of rules; everything else is opinion and should be tested against the channel's own viewed-vs-swiped and stayed-to-watch numbers.

### Cited Findings
- First 1–3 s: a person already mid-conversation or to camera, no logo/title/establishing shot, premise spoken and on screen inside 3 s, a surprise or contradiction in the first image — grounded in [VidMob×TikTok](https://vidmob.com/resource/tiktok-hook-analysis), [TikTok auction ads](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf), [Teixeira (surprise → attention)](https://hbswk.hbs.edu/item/6807.html), [Dashlet (early swipe mode)](https://arxiv.org/pdf/2204.12954), [MrBeast ("match the expectations", "front load")](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf)
- Middle: "hype to execution" by ~5 s (show, don't announce), escalate ("stair step") rather than repeat, one planned re-engagement (new rule/reversal/character) near the midpoint, no dull moments, cut on every line — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf), [Teixeira (joy velocity → retention)](https://research.tilburguniversity.edu/en/publications/emotion-induced-engagement-in-internet-video-ads/)
- Ending: punchline is the last spoken line, no signalled ending, abrupt cut within ~0.5 s, optional callback to frame 1 for a seamless loop, CTA in pinned comment/description not in the audio — [MrBeast doc](https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf), [YouTube Help (loops excluded from engaged views)](https://support.google.com/youtube/answer/12220281), [Dashlet (tail swipe mode)](https://arxiv.org/pdf/2204.12954)
- Length: 30–50 s for a dialogue skit; longer only with a multi-step escalation ladder; judge by channel's own stayed-to-watch, since public length data conflicts ([quso.ai](https://quso.ai/research/youtube-shorts-length) vs [Galloway](https://nowbam.com/decoding-the-youtube-shorts-algorithm/)) and YouTube says ranking is "independent of duration" ([RouteNote/Creator Insider](https://routenote.com/blog/youtube-shorts-algorithm/))
- Emotion: aim for a laugh *spike* plus surprise; avoid low-arousal (sad, merely sweet) endings; two-sided debate question for comments — [Berger & Milkman](https://cssh.northeastern.edu/pandemic-teaching-initiative/wp-content/uploads/sites/43/2020/09/What-Makes-Online-Content-Viral.pdf)
- Subscribers: a named recurring premise with rotating characters; benchmark against ~1.7 subs per 1,000 Shorts views ([The Publish Press](https://news.thepublishpress.com/p/are-shorts-worth-it)); ignore the "67% series lift" figure

### Inferences
- The owner's existing rules (scene-first hook, loop opened in 5 s and closed at the end, two-sided closing question, 40–50 s, vary characters, no spoken subscribe) are consistent with every measured finding above; the main additions from this research are (1) escalation inside the middle (joy velocity / stair-stepping) with one deliberate midpoint re-engagement, (2) "show, don't announce" by second 5, and (3) treating the seamless loop as polish, not strategy.

### Gaps
- There is no public measured evidence specific to scripted comedy skits on Shorts; all skit-specific rules are inferences from ad research, long-form production practice and general short-video swipe behaviour.
