# Hooks (first 1-3 s), platform retention metrics, length and looping for short-form vertical video (YouTube Shorts / Instagram Reels / TikTok)

Research date: 2026-09-29. Labels: **[Official]** = platform docs/staff statements; **[Data study]** = a dataset/survey with a stated method (sample size given where known); **[Anecdotal/creator]** = creator claims, vendor blogs, or unsourced numbers. Where a number circulates widely without a traceable origin, it is flagged **UNTRACEABLE**.

Context for the reader: none of the sources below are specific to 2D animated explainers or finance storytelling. The platform metrics apply to any Short; the hook research is mostly from **ads** (Meta, TikTok) and general creators. Applying it to animated explainers is inference and is marked as such.

---

## Q1. YouTube's "Viewed vs. swiped away" metric and average percentage viewed (APV) for Shorts

### Takeaway
"Viewed vs. swiped away" is an official YouTube Studio Shorts metric: of the times your Short was shown in the Shorts feed, the share of times viewers chose to view it instead of swiping away. YouTube publishes **no** target or threshold. The widely repeated "70%+" / "70–90%" benchmarks come from third-party blogs and one unverified Medium study, not from YouTube.

### Cited Findings
- [Official] YouTube Help ("Content tab analytics tips – Shorts"), under the card "How many chose to view": "This report highlights the percentage of times that viewers viewed your Shorts versus swiped away." — [YouTube Help 12942217](https://support.google.com/youtube/answer/12942217?hl=en-GB&co=YOUTUBE._YTVideoType%3Dshorts)
- [Official] Launch announcement (TeamYouTube community video "New YouTube Shorts Metric – Viewed vs Swiped Away"): "you can now understand how often a Short was shown in the Shorts feed + if viewers chose to view or swipe away in addition to the already existing number of views that resulted from this. These metrics will be available to all Shorts creators on Studio web and Studio mobile." (as quoted in search snippets; the page body would not render when fetched) — [YouTube Community](https://support.google.com/youtube/community-video/273390203/new-youtube-shorts-metric-viewed-vs-swiped-away?hl=en). A Medium post dated Nov 23, 2023 calls it a recent addition, so it probably launched in late 2023. — [Lacombled, Medium (via search snippet)](https://medium.com/@antoinelacombled/cracking-the-youtube-shorts-algorithm-a-study-of-3-3-billion-views-4711fdf7931b)
- [Official] Where it appears: YouTube Studio > Analytics > Content tab > Shorts (the "How many chose to view" card), and on the per-Short analytics page. — [YouTube Help 12942217](https://support.google.com/youtube/answer/12942217?hl=en-GB&co=YOUTUBE._YTVideoType%3Dshorts); navigation also described by [vidIQ (search snippet)](https://vidiq.com/blog/post/youtube-shorts-algorithm/)
- [Official] YouTube's definitions for Shorts in "Understand your YouTube content performance":
  - **Engaged views**: "How many times viewers stayed to watch past the initial seconds, not including any loops."
  - **Audience retention (Shorts)**: "The percentage of times viewers stayed to watch past the initial seconds of a Short."
  - **Average percentage viewed**: "Average percentage of a video watched among those who stayed to watch."
  — [YouTube Help 12220281](https://support.google.com/youtube/answer/12220281)
  - Implication: APV for Shorts is computed over *engaged* viewers only, i.e. after the swipe-away decision. So the hook shows up in "viewed vs. swiped away", and APV measures the body of the video.
- [Official] YouTube states it does not publish a universal viewed-vs-swiped threshold. This is reported by a third-party guide ("YouTube does not publish a universal viewed-versus-swiped threshold"), and no YouTube doc I found gives one. — [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts)
- [Anecdotal/creator] Benchmarks as they circulate:
  - "Top creators aim for roughly 75–80% view rate" — [ReelRise guide](https://reelrise.app/guide/viewed-vs-swiped-away-the-only-youtube-shorts-metric-that-matters/) (no data given)
  - "best-performing Shorts fell between 70% and 90% VVSA, while Shorts under 60% typically did not perform well" — attributed to a "study of 3.3 billion views" by Antoine Lacombled on Medium ([Medium](https://medium.com/@antoinelacombled/cracking-the-youtube-shorts-algorithm-a-study-of-3-3-billion-views-4711fdf7931b); returned HTTP 403, so I could not check the method or sample). A secondary summary of the same numbers is in [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts).
  - Prepublish's own "70–85% is strong, above 85% is exceptional" cites only its own guide, with no study, sample or date. — [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts)
  - **Verdict: the "70%+ viewed" target is anecdotal.** None of these figures come from YouTube.
- [Anecdotal/creator] The claim that it is "a key engagement metric the algorithm uses to determine reach" appears on many third-party pages. It is not stated in the YouTube Help text I retrieved. — [search summary incl. vidIQ, Metricool](https://vidiq.com/blog/post/youtube-shorts-algorithm/)
- [Official] Todd Beaupré (YouTube Sr. Director, Growth & Discovery) focuses on viewer satisfaction rather than single metrics: "We're trying to understand not just about the viewer's behavior and what they do, but how they feel about the time they're spending" (secondary quote; interview on Creator Insider, Sept 1, 2026). — [OutlierKit summary](https://outlierkit.com/resources/youtube-viewer-satisfaction-algorithm-2026/), [ppc.land](https://ppc.land/subscribers-skip-90-of-uploads-in-their-feed-youtube-director-says/). According to ppc.land, that interview contained **no** Beaupré statements about viewed-vs-swiped, loops or first-second engagement. His Shorts-specific quote was that viewers "sometimes feel overwhelmed with all the choices" and that a swipeable feed "eases the burden of decisionmaking". — [ppc.land](https://ppc.land/subscribers-skip-90-of-uploads-in-their-feed-youtube-director-says/)
- [Official] YouTube Creator Liaison Rene Ritchie: "The algorithm follows the audience, so please the audience. Check your Audience tab in Analytics… Make more videos like those…" (Aug 26, 2024 Shorts FAQ series). — [Tubefilter](https://www.tubefilter.com/2024/08/26/rene-ritchie-shorts-creator-faqs/)
- [Official] YouTube Liaison published a TikTok titled "How the algorithm surveys for satisfaction w/ Todd Beaupré" (2024), which confirms that satisfaction surveys feed ranking. — [TikTok @youtubeliaison](https://www.tiktok.com/@youtubeliaison/video/7397833528852892934)

### Inferences
- For an animated finance explainer, "viewed vs. swiped away" is effectively the scorecard for frame 1 plus the first spoken line. APV and the retention curve (over engaged viewers) score everything after it. Diagnose them separately: low viewed% points to the hook or first frame, while high viewed% with falling APV points to pacing or the middle.
- Because YouTube gives no threshold, the defensible benchmark is **your own channel median**, which is also Prepublish's recommendation.

### Gaps
- Could not open the original TeamYouTube launch post body or Creator Insider transcript, so the exact launch date is unconfirmed. Late 2023 is inferred from the Nov 2023 Medium date.
- Could not verify the Lacombled "3.3B views" study's method (403 error). Treat its 60%/70–90% figures as unverified.
- No official YouTube statement found on how heavily viewed-vs-swiped is weighted in ranking.
- No Reddit threads retrieved: reddit.com was blocked for both the search tool and fetch in this environment. Reddit anecdotes are therefore missing from these notes.

---

## Q2. How YouTube counts a Shorts view (March 31, 2025 change) and whether loops push APV above 100%

### Takeaway
Since March 31, 2025, a public Shorts "view" counts every start or replay with no minimum watch time. The old metric survives as "engaged views", which still governs YPP eligibility and revenue share and excludes loops. Loops do add watch time, which is why APV and the retention curve can exceed 100%.

### Cited Findings
- [Official] Announced by TeamYouTube (Meaghan) in the YouTube Help Community on March 26, 2025, effective **March 31, 2025**: Shorts views are counted when a Short starts to play or replay, with no minimum watch time. Previously a Short had to play for an undisclosed number of seconds. The old metric is renamed "engaged views" and remains in Analytics Advanced Mode. Rationale quoted: "We recognize that you want a deeper understanding of how your short-form videos are performing holistically, including when you're posting across multiple platforms." — [ppc.land summary](https://ppc.land/youtube-changes-how-shorts-views-are-counted-from-march-31/); original thread [YouTube Community](https://support.google.com/youtube/thread/333869549/a-change-to-how-we-count-views-on-shorts?hl=en)
- [Official] YPP eligibility and Shorts revenue sharing continue to use **engaged views**. The YPP threshold is unchanged at 1,000 subscribers plus 10M valid public Shorts views in 90 days. — [ppc.land](https://ppc.land/youtube-changes-how-shorts-views-are-counted-from-march-31/); [TubeBuddy](https://www.tubebuddy.com/blog/youtube-shorts-view-count-update-what-creators-need-to-know-about-the-new-metrics/)
- [Official] Engaged views = "How many times viewers stayed to watch past the initial seconds, **not including any loops**." — [YouTube Help 12220281](https://support.google.com/youtube/answer/12220281)
- [Anecdotal/creator, consistent with official definitions] "Average percentage viewed uses the watch time associated with Engaged Views and can exceed 100% when engaged viewers replay all or part of the Short. Although loops do not add another Engaged View, the additional watch time can still affect duration and percentage metrics." — [search summary of Creator Essentials / CoSchedule](https://www.creatoressentials.com/glossary/shorts-engaged-views/)
- [Anecdotal/creator] A creator in the YouTube Help Community reported APV of **103.9%** on a Short that still capped at ~10k views. This is real-world evidence that >100% APV occurs but does not guarantee reach. — [YouTube Community thread](https://support.google.com/youtube/thread/296504058/i-have-average-percentage-viewed-103-9-on-my-one-short-but-still-i-get-views-no-more-than-10k-and)
- [Anecdotal/creator] Loops show up as retention above 100% at second 1 of the retention graph, and 100%+ retention is claimed to be "common" under 30 s. — [Shortimize / Aibrify (search snippets)](https://www.shortimize.com/blog/youtube-shorts-retention-rate)
- [Data/analyst] Because public view counts after March 31, 2025 are broader, comparisons across that date are not apples-to-apples. — [TubeBuddy](https://www.tubebuddy.com/blog/youtube-shorts-view-count-update-what-creators-need-to-know-about-the-new-metrics/), [Sprout Social support](https://support.sproutsocial.com/hc/en-us/articles/35874991211533-YouTube-Shorts-View-Count-Update-March-2025)

### Inferences
- For benchmarking a new channel, **engaged views ÷ views** is a usable proxy for hook success alongside viewed-vs-swiped.
- A Short whose ending cuts cleanly back into its opening can lift APV above 100% without adding engaged views. APV > 100% signals rewatch but has not been shown to cause distribution (see the 103.9% / 10k case).

### Gaps
- YouTube has not published the "initial seconds" threshold that separates an engaged view from a view.
- No official YouTube statement found that explicitly says "APV can exceed 100% for Shorts". It follows from the definitions (watch time over engaged viewers, loops add time) and from creator reports.

---

## Q3. What hook formats are evidenced to work in the first 1-3 seconds

### Takeaway
The only rigorous, quantified evidence on the first seconds comes from **ads research** by Meta/Nielsen (2014–2016 data) and TikTok (auction-ads analysis, undated PDF). These studies show:
- a large share of value and attention is decided within 1.7–3 s;
- putting the key message in the first 3 s correlates with top CTR;
- sound, text overlays and direct address correlate with higher view-through.

Specific formats such as the "curiosity/negative framing", "mid-action start" or "question hook" are supported only by creator anecdote. No controlled study was found that compares them.

### Cited Findings
**Meta / Facebook (ads, older data)**
- [Data study, Official] Facebook with Nielsen: "up to 47% of the value in a video campaign was delivered in the first three seconds" and up to 74% in the first ten seconds. Also: 65% of people who watch the first 3 s watch ≥10 s, and 45% watch ≥30 s. The method is not described on the page. The data is from the 2015–2016 Facebook feed era (the companion IQ study below is dated April 2016). — [Meta for Business, "Capture Attention with Updated Features for Video Ads"](https://www.facebook.com/business/news/updated-features-for-video-ads)
- [Data study, Official] Facebook IQ, "Capturing Attention in Feed: The Science Behind Effective Video Creative" (April 20, 2016) found:
  - people spend **1.7 s** with a piece of content on mobile vs 2.5 s on desktop;
  - people can recall mobile feed content after a quarter-second of exposure.
  Method: analysis of 850+ video ads (late 2014–late 2015, US and Europe) matched to Nielsen Brand Effect studies. The model explained 82% of ad-recall variation.
  Recommendations: design for sound-off (captions, visual storytelling), show the brand/message early, and frame for mobile.
  — [Facebook IQ](https://www.facebook.com/business/news/insights/capturing-attention-feed-video-creative)
- [Data study] Meta's 2016 guidance recommended front-loading key visuals and "scenes with action or vivid backgrounds" to capture attention. — [Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads)
- Note: "1.7 seconds" is often misquoted as "people decide in 1.7 s whether to keep watching". The source measures **time spent per piece of feed content on mobile**, which is not a watch/skip decision threshold. It is also 2016 Facebook Feed data, not Reels.

**TikTok (ads, "9 Creative Tips to drive performance", auction ads; PDF undated)**
- [Data study, Official] "over 63% of all videos with the highest click-through rate (CTR) highlight their key message or product within the first 3 seconds." — [TikTok for Business PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf)
- [Data study, Official] The same PDF reports:
  - "fast-paced tracks above 120 BPM… often drive higher view-through rate";
  - vertical 9:16 videos have "an average 25% higher 6-second watch-through rate";
  - "33% auction ads with the highest VTR break the 4th wall" (direct address);
  - "40% of auction ads with the highest VTR" use text overlays;
  - "61% of the best-performing auction ads use half or more of these tips".
  No sample size or dates are given. — [TikTok for Business PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf)
- [Official] TikTok Creator Academy recommends an attention-grabbing element early, "ideally within the first 5 seconds" (search-snippet paraphrase; the page body would not render). — [TikTok Creator Academy](https://www.tiktok.com/creator-academy/en/article/elements-of-tiktok-video?lang=en)
- [Anecdotal/creator] "71% of users decide whether to keep watching or scroll past within the first 3 seconds" circulates on agency blogs with no primary source. **UNTRACEABLE**. — [Stackmatix (search snippet)](https://www.stackmatix.com/blog/tiktok-hook-first-3-seconds)

**Instagram**
- [Official] Instagram's Reels **Skip rate** (added to Insights around Aug 2025, announced via @creators on Threads) is defined as "the percentage of views from people who decided to skip your reel during those first 3 seconds." The new **Retention** graph shows "the moments in your Reel that keep or lose your viewers' interest… the flatter the line, the more engaged your audience is." — [Social Media Today, Aug 24, 2025](https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/)
- [Official, secondary-reported] Mosseri is quoted as saying "The first three seconds of a reel are super important" in an Instagram Reel about hooks. This quote is from a third-party summary; I did not see the Reel itself. — [search summary (Metricool/Babbleboxx)](https://metricool.com/instagram-reel-analytics/)
- [Anecdotal/creator] Skip-rate benchmarks of "under ~30–40% is healthy, over ~50% means the hook isn't working" come from industry trackers. The same sources note Instagram publishes no target. — [Babbleboxx](https://www.babbleboxx.com/post/instagram-adds-reels-retention-skip-rate-what-influencer-marketers-should-do-next)

**Creators**
- [Anecdotal/creator] Jenny Hoyos (Shorts creator): "I really do think you have one second to hook someone, especially on Shorts." She also said Shorts thumbnails matter little because "99.9% of the views are coming from the Shorts feed". — [YouTube Official Blog, Shorts deep dive with Todd Sherman & Jenny Hoyos](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/)
- [Anecdotal/creator] Hoyos is widely reported to have found a ~25% retention drop in a Short's last second (from an outro/wind-down), which led to her advice to "end at the peak and cut". The number is repeated in secondary blogs, and a Short titled "Why your Short's ending is destroying your retention – Jenny Hoyos method" exists. I could not find the primary interview. — [YouTube Short](https://www.youtube.com/shorts/95JNCi489gA); [Toptal/Shortimize (search snippets)](https://www.toptal.com/creator/post/youtube-shorts-length). A playbook blog attributes a "90%+ retention target" and a "3-second maximum hook" to her, also without a primary source. — [Marketing Examined](https://www.marketingexamined.com/blog/jenny-hoyos-short-form-video-playbook)
- [Anecdotal/creator] OpusClip's "50–60% of viewers who drop off do so within the first three seconds" and "burned-in captions see 15–25% higher retention" give no sample, dataset or date. Treat them as vendor marketing. — [OpusClip blog, Nov 11, 2025](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention)
- [Anecdotal/creator] Hook taxonomies such as "pattern interrupt / movement in frame 1", "direct address naming the viewer's situation", "curiosity gap" and "multi-sensory: voice + text + visual" come from agency blogs with no controlled data. — [Stackmatix](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)

### Inferences
Inferences for 2D animated finance explainers with voiceover:
- **Frame 1 must already be in motion and carry the topic visually.** Meta's recall findings and TikTok's "key message in first 3 s" point to no logo sting, no title card and no "Hey guys".
- **Voiceover line 1 should state the claim, number or question**, with the same words on screen as text. Meta's sound-off finding and TikTok's text-overlay/VTR finding both favour on-screen text. Also note Instagram says it demotes "majority text" reels (Q5), so the text should support visuals, not replace them.
- Direct address ("you") maps onto TikTok's "break the 4th wall" finding. In animation this can be a character looking at camera or a voiceover spoken in second person.
- The evidence base on first seconds is **ad-centric and 2014–2020 era**. Organic Shorts behaviour may differ, and no public study isolates animated content.

### Gaps
- No controlled or public data study compares hook *types* (question vs bold claim vs mid-action vs negative framing) on organic Shorts/Reels/TikTok.
- No Think with Google study on first-seconds attention for Shorts was retrieved.
- The TikTok 9-tips PDF is undated, and its sample size is not disclosed.
- No Reddit retention-graph case studies (Reddit is blocked in this environment).

---

## Q4. Shorts length: official guidance, whether shorter means higher APV, and seamless loop endings

### Takeaway
Since October 15, 2024, YouTube Shorts can be up to 3 minutes. YouTube's public stance is that there is no "magic length": make it as long as the story needs. Third-party data leans toward short (<30–60 s), but it conflicts, is mostly surveys or unsourced, and cannot separate length from content quality. Loop endings raise APV mechanically, but no official source confirms they are rewarded directly.

### Cited Findings
- [Official] YouTube Blog (Oct 3, 2024): starting Oct 15, 2024, Shorts can be up to 3 minutes (previously 60 s), for square or taller videos. YouTube said it would improve recommendations for longer Shorts in the coming months. — [YouTube Blog, "Tall updates coming to Shorts"](https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/)
- [Official] YouTube Help: square/vertical videos up to 3 min uploaded after Oct 15, 2024 are classified as Shorts. The help page gives music limits (most songs usable for up to 90 s in a Short up to 3 min; some tracks 60 or 30 s) and Content ID changes. It gives **no** performance guidance by length. — [YouTube Help 15424877](https://support.google.com/youtube/answer/15424877?hl=en)
- [Official] Todd Sherman (then Shorts product lead), on Creator Insider (Aug 2023), was quoted by secondary sources:
  - no "magic length": "The thing to really think about here is: 'What length do I need to tell my story?'";
  - "What we try to do in recommendations is independent of duration, to figure out if someone really enjoyed the video."
  Both are secondary quotes that I could not verify on a primary page. The YouTube Blog recap of Aug 24, 2023 confirms he answered "Just how short should a Short be?" but does not reproduce the answer. — [YouTube Blog, Rene's Top Five Aug 24 2023](https://blog.youtube/culture-and-trends/renes-top-five-august-24-2023-edition/); quotes via [Piktochart/Loomly (search snippets)](https://piktochart.com/blog/how-long-youtube-shorts/)
- [Official, dated] In a 2023 MediaPost interview, Sherman said "Shorts will remain focused on videos that are a minute or less." The Oct 2024 3-minute change superseded this. — [MediaPost](https://www.mediapost.com/publications/article/388588/youtube-shorts-product-lead-offers-insights-for-cr.html)
- [Official, secondary-reported] Rene Ritchie is quoted: "How long should a Short be? … as long as it needs to be, but no longer. As short as it can be, but no shorter. If it's padded… or cut to the point of being unsatisfying, people will lose interest or get frustrated and swipe out." The quote is from a third-party article and I did not locate the primary. — [Toptal (search snippet)](https://www.toptal.com/creator/post/youtube-shorts-length)
- [Data study, survey] Adobe Express (published June 24, 2026) surveyed 507 YouTube creators with ≥1,000 subscribers (March 2026). It is **self-reported**, not analytics data:
  - "under 30 seconds" was named the best length for views, shares, click-throughs and saves by an average of 46% of creators;
  - 53% named it for views specifically;
  - for subscriber growth the split was 34% (<30 s) vs 34% (30–60 s);
  - 49% said <30 s Shorts drive more click-throughs to long-form, vs 36% for >30 s.
  — [Adobe Express](https://www.adobe.com/express/learn/blog/youtube-shorts-length-study)
- [Data study, unverified] "A study of 5,400 Shorts by the Inflow Network found 50 to 60 second videos pulled nearly 22x more views than those under 10 seconds" (reported by Piktochart). The primary source was not reachable (403). This **conflicts in direction** with the "shorter is better" narrative. — [Piktochart (search snippet)](https://piktochart.com/blog/how-long-youtube-shorts/)
- [Anecdotal/creator] OpusClip claims 15–30 s Shorts "consistently achieve the highest retention rates, often exceeding 80%", that Shorts over 45 s "see dramatic drop-offs", and that "even a 10% replay rate can significantly boost" distribution. None of these are sourced. — [OpusClip](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention)
- [Anecdotal/creator] "Many viral YouTube Shorts fall between 25 and 35 seconds" and "7–8 seconds optimizes rewatch for loop content" come from vendor blogs with no dataset. — [Toptal (search snippet)](https://www.toptal.com/creator/post/youtube-shorts-length)
- [Official, TikTok, 2020] TikTok: "A strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end, would receive greater weight than a weak indicator." — [TikTok Newsroom, June 18, 2020](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)
- [Data study, older ads] Facebook IQ (2016) recommended short videos for engagement in feed ads (secondary summary cites 6–15 s). This is ads guidance, not organic. — [Facebook IQ](https://www.facebook.com/business/news/insights/capturing-attention-feed-video-creative)
- [Official, mechanism] Loops add watch time but not engaged views (see Q2). This is the only officially grounded mechanism by which seamless loops raise APV. — [YouTube Help 12220281](https://support.google.com/youtube/answer/12220281)

### Inferences
- APV is a percentage, so shorter Shorts will tend to post higher APV mechanically, and loops can take it past 100%. Total watch time per impression can still favour longer Shorts that hold viewers. None of the evidence found separates the two, which likely explains why the survey and Inflow data point in different directions.
- For finance explainers, a practical reading of the official stance is to cut every second that doesn't advance the story, rather than aim for a number. A single-concept explainer in roughly 20–45 s is consistent with the anecdotal consensus, but that range is **not** an evidenced optimum.
- A loop ending suits animation well: the last frame or voiceover line can lead straight back into frame 1, e.g. the final number or answer sets up the opening question. It raises APV by construction. Its effect on reach is **unproven**.

### Gaps
- There is no official YouTube data on how Shorts length relates to reach or APV.
- No controlled study was found on the effect of seamless loop endings on rewatch rate or distribution.
- I could not verify the primary sources for the Inflow Network study or the Sherman and Ritchie length quotes.

---

## Q5. TikTok and Instagram (Mosseri) official statements on ranking and creative best practice

### Takeaway
Instagram's head Adam Mosseri (January 2025) named **watch time, likes per reach and sends per reach** as the top three ranking signals. Likes matter slightly more for followers ("connected"), sends slightly more for non-followers ("unconnected"). Instagram's official 2023 ranking post lists the Reels predictions it makes: whether you will reshare, watch to the end, like, and visit the audio page. TikTok's official 2020 explainer says completing a longer video is a strong signal. TikTok's ads research favours an early key message, sound, text overlays, vertical format and direct address.

### Cited Findings
- [Official] Mosseri (reported Jan 22, 2025): "The top three signals that matter most for ranking are watch time, likes and sends." He told creators to look at "average watch time, likes per reach, and sends per reach", and added: "Likes are slightly more important for connected content, and sends are slightly more important for unconnected content." Comments were not mentioned. — [Social Media Today](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)
- [Official] "Instagram Ranking Explained" (May 31, 2023) says that for Reels Instagram predicts "how likely you are to reshare a reel, watch a reel all the way through, like it, and go to the audio page". The signal groups are:
  - your activity;
  - your history with the poster;
  - information about the reel (audio, visuals, popularity);
  - information about the poster.
  Instagram reduces distribution of "low-resolution or watermarked reels, reels that are muted or contain borders, reels that are majority text, or reels that have already been posted on Instagram." — [Instagram](https://about.instagram.com/blog/announcements/instagram-ranking-explained/)
- [Official] The Instagram Reels **Skip rate** (first 3 s) and **Retention** graph were added to Insights around Aug 2025. — [Social Media Today, Aug 24, 2025](https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/)
- [Anecdotal/creator] Claims that "sends carry roughly 3–5x the weight of likes for unconnected reach" and that "a 15-second Reel watched 3 times outranks a 60-second Reel watched once" appear on marketing blogs, attributed to Mosseri. **UNTRACEABLE**: Mosseri's quoted wording is only "slightly more important". — [Dataslayer / Socialync (search snippets)](https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers); contradicted by [Social Media Today's direct quote](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)
- [Official] TikTok (June 18, 2020): recommendations weigh user interactions (likes, shares, follows, comments, watch completion), video information ("captions, sounds, and hashtags") and device/account settings. "Neither follower count nor whether the account has had previous high-performing videos are direct factors." — [TikTok Newsroom](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)
- [Official/Data] The TikTok for Business "9 Creative Tips" (auction ads) cover:
  - leverage sound (>120 BPM linked to higher VTR);
  - key message in the first 3 s (63% of top-CTR ads);
  - let creators lead;
  - ride trends;
  - keep it real and entertaining ("almost half of the best performing" ads are emotionally appealing);
  - shoot 9:16 (+25% 6-s watch-through);
  - break the fourth wall (33% of top-VTR ads);
  - concise text overlays (40% of top-VTR ads);
  - a strong CTA.
  — [TikTok for Business PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf)

### Inferences
- On Instagram, "sends per reach" is the lever for reaching non-followers. Finance explainers with a single shareable takeaway ("send this to someone who…") fit that signal. The claim that sends are "3–5x" likes should not be repeated.
- Instagram explicitly demotes "majority text" reels and reels with borders. Animated explainers that lean on kinetic typography or letterboxed 16:9 inside 9:16 are therefore at risk on Instagram specifically.

### Gaps
- There is no official TikTok statement from 2025–2026 on hooks or length with numbers. The Creator Academy page did not render its body.
- The primary Mosseri Reel with the "first three seconds are super important" quote was not viewed directly.

---

## Q6. Common myths vs what has been stated or evidenced

### Takeaway
Most hard-number rules (a minimum viewed%, a mandatory length, hashtag reach) have no official basis. The officially grounded facts are:
- the metric definitions;
- that satisfaction and audience response drive distribution;
- that watch time, likes and sends matter on Instagram;
- that completion is a strong signal on TikTok.

### Cited Findings
- **Myth: "YouTube punishes/stops pushing Shorts below X% viewed (e.g. 70%)."** No YouTube doc gives a threshold. The numbers trace to third-party blogs and one unverifiable Medium study. — [YouTube Help 12942217](https://support.google.com/youtube/answer/12942217?hl=en-GB&co=YOUTUBE._YTVideoType%3Dshorts); [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts)
- **Myth: "APV above 100% guarantees virality."** A creator with 103.9% APV reported being stuck at ~10k views. — [YouTube Community](https://support.google.com/youtube/thread/296504058/i-have-average-percentage-viewed-103-9-on-my-one-short-but-still-i-get-views-no-more-than-10k-and)
- **Myth: "Shorts must be under 30 s / 60 s."** YouTube allows up to 3 min (since Oct 15, 2024). YouTube staff frame length as "what the story needs", and the 5,400-Short Inflow data (unverified) found 50–60 s outperformed <10 s. The survey showing <30 s preferred is self-reported. — [YouTube Blog](https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/); [Adobe](https://www.adobe.com/express/learn/blog/youtube-shorts-length-study); [Piktochart (snippet)](https://piktochart.com/blog/how-long-youtube-shorts/)
- **Myth: "Hashtags boost Reels reach."** Mosseri (Feb 2025, via secondary reports) said hashtags don't meaningfully increase reach and work more as labels. The reporting article paraphrases rather than quoting him verbatim. — [Digital Information World, Feb 4, 2025](https://www.digitalinformationworld.com/2025/02/adam-mosseri-declares-hashtags-useless.html). Caveat: TikTok's 2020 doc does list hashtags among the video-information signals, as low-weight metadata. — [TikTok Newsroom](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)
- **Myth: "People decide in 1.7 seconds whether to keep watching."** The original Facebook IQ figure (2016) is average time spent per piece of mobile feed content, not a watch/skip decision threshold. — [Facebook IQ](https://www.facebook.com/business/news/insights/capturing-attention-feed-video-creative)
- **Myth: "47% of a video's value is in the first 3 seconds" (applied to organic Shorts).** It is a Facebook+Nielsen **ad campaign** figure from around 2016 ("up to 47%"), not an organic Shorts/Reels metric. — [Meta for Business](https://www.facebook.com/business/news/updated-features-for-video-ads)
- **Myth: "Sends are weighted 3–5x likes on Instagram."** Mosseri's quoted wording is "slightly more important" for unconnected reach. — [Social Media Today](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)
- **Myth: "Follower count / past hits directly boost TikTok distribution."** TikTok says neither is a direct factor. — [TikTok Newsroom](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)
- **Myth: "Post-March-2025 Shorts view counts are comparable to earlier ones."** They are not: views now count on every start or replay. — [TubeBuddy](https://www.tubebuddy.com/blog/youtube-shorts-view-count-update-what-creators-need-to-know-about-the-new-metrics/)
- **Widely repeated with no traceable origin (UNTRACEABLE):**
  - "71% decide in the first 3 seconds" ([Stackmatix](https://www.stackmatix.com/blog/tiktok-hook-first-3-seconds));
  - "50–60% of drop-offs happen in the first 3 s" and "captions +15–25% retention" ([OpusClip](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention));
  - "75–80% view rate target" ([ReelRise](https://reelrise.app/guide/viewed-vs-swiped-away-the-only-youtube-shorts-metric-that-matters/)).

### Inferences
- The officially grounded optimisation loop for an animated explainer channel is:
  1. improve viewed-vs-swiped (hook, frame 1, first voiceover line) against the channel's own median;
  2. flatten the retention curve over engaged viewers;
  3. earn rewatches (loop ending) and sends/shares.
- Rules framed as hard thresholds should be treated as heuristics.

### Gaps
- There is no official statement from any platform that quantifies a "penalty" for low early retention, so both the myth and its refutation rest on absence of evidence.
- Reddit community evidence (r/NewTubers, r/PartneredYoutube, r/TikTokHelp, r/InstagramMarketing) could not be collected because reddit.com is blocked for both search and fetch in this environment.
