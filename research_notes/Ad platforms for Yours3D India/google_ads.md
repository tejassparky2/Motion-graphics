# Google Ads as a paid channel for Yours3D India (custom 3D-printed figurines, WhatsApp-first ordering)

Research date: 21 Oct 2026. Context: singles from ₹3,599, couples ₹5,999–₹7,999, ships India-wide, orders via WhatsApp, site yours3dindia.com used mainly to push people to WhatsApp, no on-site checkout.

Method note: Reddit (r/PPC, r/googleads etc.) could not be reached. The search tool refused reddit.com ("domain not accessible to our user agent"), and general searches returned no Reddit threads, so practitioner views below come from Shopify Community threads, Substack/agency blogs and Google's own staff, not Reddit. Google Trends was also blocked (HTTP 429 on the Trends API), so no first-hand seasonality curve could be pulled. WordStream pages returned HTTP 403, so WordStream/LocaliQ figures come via search-result summaries of those pages plus the LocaliQ page listing.

## 1. Which campaign types fit, and can Google Ads send people straight to WhatsApp?

### Takeaway
Yes, with conditions. Google's "message assets" (WhatsApp extension) put a WhatsApp chat button on Search ads and work with Search and Performance Max. India was one of the two launch markets (with Brazil). The feature is still labelled beta, needs advertiser verification, and limits impressions for new advertisers at first. The headline click still goes to the website, so yours3dindia.com has to be a real, crawlable landing page. Search plus a message asset is the best fit. Shopping/Merchant Center is a weak fit without a product page and checkout. Demand Gen and YouTube are budget-hungry by Google's own guidance.

### Cited Findings
- **What message assets do:** they add a button or asset to responsive search ads. Tapping it opens a conversation with the business on the chosen messaging platform. Google's help page says message assets "are currently in beta" and may not be available to every account. — [Google Ads Help: About message assets](https://support.google.com/google-ads/answer/14888522?hl=en)
- **Campaign types:** Search and Performance Max. — [Google Ads Help: About message assets](https://support.google.com/google-ads/answer/14888522?hl=en)
- **Setup requirements:** select the country of the WhatsApp/SMS number, enter an active WhatsApp Business (or SMS) number, and write a "starter message" that complies with Google Ads policies. Don't mention the messaging platform in the headline. — [Google Ads Help: About message assets](https://support.google.com/google-ads/answer/14888522?hl=en)
- **Bidding:** choose "Conversions" as the bid goal at creation. For conversion bidding use Max conversions or tCPA; for value bidding use tROAS or Max conversion value. — [Google Ads Help: About message assets](https://support.google.com/google-ads/answer/14888522?hl=en)
- **Eligibility:** a good policy-compliance history, an eligible vertical (sensitive ones such as elections are excluded) and completed Advertiser verification. "New advertisers may see temporarily limited message asset impressions until they build up positive user interactions." — [Google Ads Help: About message assets](https://support.google.com/google-ads/answer/14888522?hl=en). The live page lists no countries and no update date, only "©2026 Google".
- **India availability timeline:** first spotted in March 2024. It launched in Brazil and India, then expanded on 21 Aug 2024 to 13 countries (Argentina, Brazil, Chile, China, Colombia, Hong Kong, India, Indonesia, Malaysia, Mexico, Peru, Singapore, Thailand). Still beta at that point. — [PPC News Feed, 21 Aug 2024](https://ppcnewsfeed.com/ppc-news/2024-08/whatsapp-asset-rolls-out-to-11-more-countries/)
- **Conversion tracking for WhatsApp:** Search Engine Land reported a new "conversation started" conversion action for WhatsApp engagements from message assets. It said these are compatible with Search and PMax in select markets including India, Brazil, Argentina and Singapore, still in beta and not available to all advertisers. Seen as a search snippet only: the page returned 403, so its date is unconfirmed. — [Search Engine Land](https://searchengineland.com/google-whatsapp-conversation-started-conversion-action-448608)
- **wa.me as the ad's final URL:** no Google documentation found that allows or bans a wa.me link as the final URL. Google's policy only says destinations must meet its Destination requirements, with disapprovals such as "Destination not working", "Destination mismatch" and "Destination not crawlable". — [Google Advertising Policies Help](https://support.google.com/adspolicy/answer/9338593?hl=en)
- **Demand Gen budget floor (Google staff):** Google PM Alejandro Osio called a "hundred dollars daily budget" (about ₹8,300+/day) the "bare minimum best practice" for a Demand Gen campaign (Ads Decoded episode, 1 Oct 2026). Since 1 Apr 2026 the Google Ads API enforces a $5/day technical minimum for Demand Gen. — [PPC Land, Oct 2026](https://ppc.land/google-pm-calls-100-a-day-the-floor-for-a-demand-gen-campaign/)
- **Demand Gen prerequisites (same source):** Google tag gateway, CRM linked via Data Manager, enhanced conversions, a first-party customer seed list, and horizontal, vertical and square images and video with "Excellent" ad strength. — [PPC Land, Oct 2026](https://ppc.land/google-pm-calls-100-a-day-the-floor-for-a-demand-gen-campaign/)
- **Demand Gen budget rules:** Google's help centre recommends a budget of at least 20× the average target CPA for conversion bidding. The Google Ads API docs and Search Ads 360 help say ≥15× target CPA. Google suggests tests of at least 4–6 weeks. — [Google Ads Help: Demand Gen low budget](https://support.google.com/google-ads/answer/14718973); [Google Ads Help: Demand Gen budget fluctuations](https://support.google.com/google-ads/answer/14715995); [Google Ads API: Create a Demand Gen campaign](https://developers.google.com/google-ads/api/docs/demand-gen/create-campaign); [SA360 Help](https://support.google.com/sa360/answer/14338021)
- **Shopping/Merchant Center checkout (free listings):** to get checkout on free listings you must supply a checkout or cart URL that lands on your own site's cart with the item loaded. It can't require sign-in and must be on the same domain. — [Merchant Center Help: checkout_link_template](https://support.google.com/merchants/answer/13580733)
- **Custom products in Merchant Center:** Google's `identifier_exists` attribute is for products without GTIN/MPN/brand. Google's own example is a customised dress with `identifier_exists = no`. Google warns against setting "no" when identifiers do exist. — [Merchant Center Help: identifier_exists](https://support.google.com/merchants/answer/6324478?hl=en-AU)
- **Merchants' reports on custom products:** Shopify Community merchants report "limited performance due to missing identifiers" warnings even when products are marked custom. One reports an account suspension for "customizable goods" without a clear trigger. These are anecdotes, not policy. — [Shopify Community thread](https://community.shopify.com/t/what-causes-google-merchant-center-to-label-goods-as-customizable/248031)
- **PMax caution (Shopify Community AMA):** "PMax can result in higher costs if not closely monitored". Standard Shopping with search-term control is suggested as the safer start for small stores. — [Shopify Community AMA recap, Apr 2025](https://community.shopify.com/t/ama-recap-april-google-shopping-and-google-ads-with-emmanuel-flossie/412585); [Shopify Community: small budget tips](https://community.shopify.com/t/tips-for-newly-started-company-with-a-small-budget/411000)

### Inferences
- **Best fit:** a Search campaign on high-intent keywords, with a WhatsApp message asset plus a call asset, pointing at a dedicated yours3dindia.com landing page. That page needs a gallery, prices, delivery time and a big WhatsApp button. The headline click must reach a crawlable page; WhatsApp is the secondary path.
- **Direct wa.me final URLs:** my inference is that "destination not crawlable" or mismatch disapprovals are likely, but this is unconfirmed. Practitioners usually route through a landing page.
- **Shopping/PMax with a feed:** a weak fit today. There is no on-site product page with checkout, and custom items lack GTINs. Shopping ads need product pages with price and the ability to buy (from my general knowledge; the official landing-page policy text was not retrieved, see Gaps). PMax without a feed is possible but opaque on a small budget.
- **Demand Gen and YouTube Shorts:** at Google's own $100/day "bare minimum" (₹8,000+/day), Demand Gen is above a ₹500–₹2,000/day budget. Also, figurines are a visual, impulse-type product better served by Instagram/Meta Reels for discovery. Treat YouTube/Shorts as a later test.
- **Local/Maps (Google Business Profile, location assets):** the buyers are India-wide, so this matters only if there is a physical studio. A free Business Profile still helps reviews and credibility. No source was retrieved on this.

### Gaps
- Official current country list for message assets: the live help page names none, so India's eligibility in 2026 is inferred from 2024 reports and the setup flow.
- Whether WhatsApp message assets work in Performance Max for India accounts today: the help page says Search and PMax, but there is no India-specific confirmation.
- Google's official Merchant Center landing-page/checkout policy for paid Shopping ads, and any explicit "personalised/made-to-order" policy: not retrieved.
- Lead form assets in India for this vertical: not researched within the tool budget.
- YouTube Shorts-specific minimum budgets: no source found.

## 2. Typical Indian CPCs and search volumes for the target keywords

### Takeaway
No public source gives India CPCs or volumes for "custom 3D figurine", "couple miniature", "caricature gift", "3D printed photo gift", "anniversary gift for husband" or "personalised gifts". The only India numbers are broad e-commerce ranges (roughly ₹3–₹40 per click, from vendors, 2025–2026). The owner must pull exact figures from Keyword Planner (free, location India, currency INR).

### Cited Findings
- **India e-commerce/retail CPC, ₹3–₹20 (Nico Digital, 11 Jun 2026):** from Keyword Planner and DataForSEO bid estimates for broad commercial terms (furniture, apparel, footwear), converted at about ₹83.5/$. Called "indicative ranges". Gifting is not broken out. — [Nico Digital, Jun 2026](https://www.nicodigital.com/performance-marketing/google-ads-cost-in-india-cpc-benchmarks/)
- **Three sources disagree on e-commerce CPC.** Catlist Media (Mar 2026) gives ₹10–₹40 (practitioner estimate, no sample), with Shopping at ₹10–₹40 and display at ₹5–₹15. OwlClaw (2025 data) gives about ₹10 (₹5–₹20, agency client averages). Nico Digital gives ₹3–₹20. The compiler advises against averaging them because they measure different things (planner bids vs account averages). — [Rahul D Sarker: three sources, three answers](https://rahuldsarker.co/insights/google-ads-cpc-india-by-industry)
- **OwlClaw (vendor, 2026 page):** average India CPC ₹8–₹25, Google Shopping e-commerce CPC ₹5–₹15, search CTR 4.5–7%. Claims Indian CPCs are 70–85% below US. The dataset is not named, so treat as unverified. — [OwlClaw PPC Benchmarks India 2026](https://owlclaw.com/benchmarks/ppc-benchmarks-india)
- **Overall India range:** about ₹10 for long-tail terms up to about ₹3,000 for high-intent insurance terms (agency guide, 2026). — [upGrowth: Google Ads Pricing India 2026](https://upgrowth.in/google-ads-pricing-india-2026/)
- **Fashion e-commerce:** an average CPC of about ₹3 is cited (2026 guide). — [Thinkster: Google Ads CPC in India 2026](https://thinkster.in/google-ads-cpc-in-india)
- **"Personalised gifts" volume:** found only as a global (not India) figure. Keysearch lists about 165,000/month; another list shows 135,000, undated (about 2024). — [Keysearch: top gift keywords](https://www.keysearch.co/top-keywords/gift-keywords); [Seopital: best gift SEO keywords](https://www.seopital.co/blog/the-best-gift-seo-keywords)
- **Competition:** large incumbents already rank and advertise on "personalized gifts" in India. IGP has a dedicated "Personalized Gifts India 2026" category page. — [IGP personalized gifts](https://www.igp.com/personalized-gifts)

### Inferences
- **Example spend (estimate, not data):** at ₹10–₹25 per click, ₹1,000/day buys about 40–100 clicks. Generic terms like "personalised gifts" and "anniversary gift for husband" will be contested by IGP, FNP and Amazon-type players and likely cost more. Niche terms like "custom 3D figurine", "3D miniature of couple" and "mini me figurine" likely have low volume but higher intent.
- **Long tail is likely tiny.** Keyword Planner may show "custom 3D figurine India" volumes in the tens to low hundreds per month. This is unverified and must be checked. Low volume caps how much a Search campaign can spend, which suits a small budget but limits scale.

### Gaps
- No public India Keyword Planner, SEMrush or Ahrefs data found for any of the six named keywords: CPC, volume and competition are all unavailable.
- Bid ranges are not public; they need the owner's own Keyword Planner export (Tools → Keyword Planner → India, INR).

## 3. Benchmarks for India and for gifting (CPC, CTR, CVR)

### Takeaway
The only gifting-specific benchmark is WordStream/LocaliQ's "Shopping, Collectibles & Gifts" category, and it is US data. 2025 report: CTR 8.92%, search CVR 3.83%, CPC up 33.72% YoY. 2026 report: CTR 8.28%, CPC $4.14, CVR 4.01%, CPL $49.40. No credible India-specific gifting CVR exists. Indian vendor figures (CTR 4.5–7%) are unverified.

### Cited Findings
- **WordStream/LocaliQ 2025** (data Apr 2024–Mar 2025, 16,446 US search campaigns), Shopping, Collectibles & Gifts: average search CTR 8.92%, average CPC up 33.72% YoY, average CVR 3.83%. Overall headline average CPC widely cited as $5.26. These are search-result summaries of the WordStream page; the page itself returned 403. — [WordStream 2025 Google Ads benchmarks](https://www.wordstream.com/blog/2025-google-ads-benchmarks)
- **LocaliQ 2026 update** (data Apr 2025–Mar 2026), Shopping, Collectibles & Gifts: CTR 8.28%, CPC $4.14, CVR 4.01%, CPL $49.40 (third-party summary; the LocaliQ page shows $4.14 CPC). — [LocaliQ Search Advertising Benchmarks 2026](https://localiq.com/blog/search-advertising-benchmarks/)
- **Overall CPC trend:** across industries, average CPC rose to $5.42 with 87% of industries rising, and average CVR climbed to 8.18%. These reports are labelled 2025 or 2026 inconsistently. — [Shopifreaks summary](https://www.shopifreaks.com/google-ads-cpcs-rose-to-5-42-in-2025-with-87-of-industries-seeing-increases-but-conversion-rates-climbed-to-8-18-as-automation-improves/)
- **Global e-commerce averages (other sources):** e-commerce CTR about 1.55% and CPC about $5.03 (Digital Gravity 2025); e-commerce search CVR about 2.81% (Usermaven). Methodologies differ and they conflict with WordStream. — [Digital Gravity 2025](https://www.digitalgravity.ae/blog/?p=5305); [Usermaven](https://usermaven.com/blog/google-ads-benchmarks)
- **Landing-page CVR planning figures (India agency, Jun 2026):** homepage about 1%, a decent page 2–3%, a strong dedicated page 4–5%. Formula: CPL = CPC ÷ CVR. — [Nico Digital](https://www.nicodigital.com/performance-marketing/google-ads-cost-in-india-cpc-benchmarks/)
- **India search CTR of 4.5–7%** comes from OwlClaw only (vendor, unverified). — [OwlClaw](https://owlclaw.com/benchmarks/ppc-benchmarks-india)

### Inferences
- **Cost per chat (estimate):** ₹15 CPC ÷ 3% landing-page-to-WhatsApp rate ≈ ₹500 per WhatsApp lead. If 20–30% of chats become orders (an assumption, not sourced), cost per order is about ₹1,700–₹2,500. That would be 30–70% of a ₹3,599 single's price before production cost. Couples (₹5,999–₹7,999) have more headroom. Treat all of this as a planning estimate to be replaced by real data after 2–4 weeks.

### Gaps
- No India-specific gifting CTR/CVR benchmark from Google or a credible Indian agency report.
- No published WhatsApp chat-to-order conversion rates for Indian D2C gifting.

## 4. Is India search demand big enough, and how seasonal is it?

### Takeaway
Gifting demand in India is large and growing, and Google's own India research shows festive shoppers research heavily on Search and images. But there is no public Google Trends data for "3D figurine"-type queries, and the niche long tail is probably small. Peaks likely line up with Valentine's (Feb), Raksha Bandhan (Aug), Diwali (Oct/Nov) and Christmas/New Year, but this could not be verified with a Trends pull.

### Cited Findings
- **Market size (one 2026 vendor estimate):** India's personalised gifting market is put at ₹20,000–30,000 crore in 2026, growing to ₹45,000–55,000 crore by 2030. The source admits reports define the market differently. — [Lovely Design blog, 2026](https://www.lovelydesign.in/blog/personalized-gifting-market-india-2026-data-insights)
- **Think with Google India (Year in Search, 2018-era data):** gifting is becoming more personalised, with interest in customised, handmade and surprise gifts. Gifting-related "near me" searches grew 111% YoY around Diwali, Rakhi and Christmas. This data is dated. — [Think with Google: Year in Search India, insights for brands (PDF)](https://www.thinkwithgoogle.com/_qs/documents/7650/Year_in_Search__India_Insights_for_brands_jeEKocQ.pdf)
- **Google/Ipsos festive study:** 9 in 10 Indian festive shoppers research before buying, and 7 in 10 also buy on impulse. — [Tripura Star News reporting Google study](https://www.tripurastarnews.com/9-in-10-shoppers-research-extensively-yet-70-buy-on-impulse-google-unpacks-indias-two-speed-festive-consumer/); [Zee Biz](https://www.zeebiz.com/technology/news-how-ai-youtube-and-google-search-are-influencing-india-s-festive-purchases-403709)
- **Image-led journeys (Think with Google APAC):** 8 in 10 Diwali/Navratri shopping journeys involve ideas from image search or social images. — [Think with Google APAC: festive advertising in AI Search, India](https://business.google.com/in/think/consumer-insights/festive-advertising-strategy-ai-search-india/)
- **Raksha Bandhan:** Google Trends showed a sharp surge for "same day delivery rakhi" the day before Raksha Bandhan, pointing to last-minute, speed-led buying. — search-summary claim only. It appeared among results that included [Think with Google APAC festive piece](https://business.google.com/in/think/consumer-insights/festive-advertising-strategy-ai-search-india/) and [Zee Biz](https://www.zeebiz.com/technology/news-how-ai-youtube-and-google-search-are-influencing-india-s-festive-purchases-403709), but I did not confirm which page carries it. Treat as unverified.
- **Diwali gifting** is described as an "INR 20,000 cr" category (Substack commentary, not primary data). — [ReadOn Substack](https://readon.substack.com/p/diwali-gifting-an-inr-20000-cr-grand)

### Inferences
- **Lead times:** a made-to-order figurine needs production and shipping time. The company's own ad pushes must start 2–4 weeks before each festival, with cut-off dates in ad copy. Last-minute Rakhi searchers wanting same-day delivery are a poor fit.
- **Steady demand:** anniversaries and birthdays are year-round, giving a steady base. Festival spikes will raise CPCs as big gifting players bid.

### Gaps
- No Google Trends series could be retrieved (API returned 429). The owner should check trends.google.com for India, past 5 years, comparing "personalised gifts", "3d figurine", "miniature", "caricature" and "anniversary gift".
- No India search-volume data for the niche terms (see section 2).

## 5. PMax, Demand Gen and YouTube: minimum budgets, data needs, learning periods and small-budget pitfalls

### Takeaway
Google's own guidance puts automated campaigns out of reach of a ₹500–₹2,000/day budget. PMax should run at least 6 weeks without big changes, Demand Gen's "bare minimum" is $100/day, and Demand Gen budgets should be 15–20× target CPA. Smart Bidding learning takes 1–2 weeks (up to 6). Practitioners say target-based bidding needs roughly 15–30+ conversions a month, and agency guides say small accounts suffer from thin data.

### Cited Findings
- **PMax run time:** Google says to run new PMax campaigns for at least 6 weeks so the algorithm can ramp up, and to avoid frequent budget, bid-strategy or status changes, which can reset learning. — [Google Ads Help: PMax optimisation tips](https://support.google.com/google-ads/answer/11385582?hl=en)
- **Learning phase:** automated bidding learning is "typically 1–2 weeks, but sometimes up to 6 weeks". — [Google Ads Help: Create a PMax campaign](https://support.google.com/google-ads/answer/10724896?hl=en)
- **Smart Bidding:** about 2 weeks to learn and fully optimise; make smaller target changes and wait. — [Google Ads Help: performance fluctuations](https://support.google.com/google-ads/answer/12076885?hl=en). Think with Google says about one week, depending on conversion volume and delay. — [Think with Google: Smart Bidding](https://business.google.com/in/think/marketing-strategies/smart-bidding-strategy/)
- **PMax "3× target CPA daily budget" rule:** circulates on third-party sites, but I could not find it on Google's pages. Another guide says 10–15×. Sources disagree. — see search results summarised from [Google Ads Help: PMax tips](https://support.google.com/google-ads/answer/11385582?hl=en) (no 3× rule found there)
- **Conversion thresholds:** third-party sources say Target CPA needs about 15–30 conversions in a 7–30-day window, or about 30/month, before stabilising. These are not official Google figures. — [Stackmatix: learning phase on small budgets](https://www.stackmatix.com/blog/ad-learning-phase-small-budgets); [Relevant Audience: Smart Bidding glossary](https://www.relevantaudience.com/glossary/smart-bidding/). An Indian agency also says automated bidding needs about 30+ conversions per month per campaign. — [Nico Digital, Jun 2026](https://www.nicodigital.com/performance-marketing/google-ads-cost-in-india-cpc-benchmarks/)
- **Micro-conversions:** one small-budget guide suggests optimising for an event that can reach 10–50 conversions/week (e.g. a micro-conversion such as a WhatsApp click), and consolidating into fewer campaigns. — [Stackmatix](https://www.stackmatix.com/blog/ad-learning-phase-small-budgets)
- **Demand Gen:** $100/day "bare minimum best practice" (Google PM, 1 Oct 2026); API floor $5/day since 1 Apr 2026; budget ≥15–20× target CPA; ad groups with 50+ conversions perform better; tests of 4–6 weeks. Conversions can take 30+ days to arrive. — [PPC Land](https://ppc.land/google-pm-calls-100-a-day-the-floor-for-a-demand-gen-campaign/); [Google Ads Help: Demand Gen low budget](https://support.google.com/google-ads/answer/14718973)
- **Small-account difficulty:** accounts under $3,000/month are "typically more difficult" because thin data forces decisions on incomplete information. Use negative keywords aggressively. — [Practical Ecommerce](https://www.practicalecommerce.com/articles/1341-Pay-per-click-Advertising-Seven-Pointers-for-Smaller-Campaigns)
- **Budget vs structure:** "a budget misaligned with the structure it's asked to support will always be wasted spend". Fix location targets, match types and structure before raising budget. — [SlideShare agency deck: end of under- and over-spending (SMX)](https://www.slideshare.net/slideshow/end-of-under-and-over-spending-smxpptx/253459387)

### Inferences
- **Budget vs data needs:** at ₹1,000/day with an estimated ₹500 per WhatsApp lead, the account gets about 2 leads/day (about 60/month) on a WhatsApp-click micro-conversion. That is barely enough for Max Conversions, but only about 10–20 real orders/month, too few for tCPA/tROAS on purchases.
- **Recommended path:** start with Manual CPC or Max Clicks with a bid cap, or Max Conversions on the WhatsApp-click micro-conversion. Move to tCPA only after about 30 conversions/month.
- **Common small-budget leaks** (general practitioner knowledge; Reddit could not be checked): broad match, Search Partners and Display expansion (on by default in new Search campaigns) and PMax's opaque placements. For this account: exact and phrase match only, Search Partners and Display Network unticked, a negative list (free, DIY, "how to make", job, course, printer, STL, Amazon, Flipkart), and presence-only location targeting set to India.

### Gaps
- Reddit r/PPC, r/googleads and r/IndiaBusiness first-hand reports could not be retrieved (domain blocked to the tool). The report writer should not quote Reddit sentiment from these notes.
- No official Google statement of a minimum conversion count for tCPA/tROAS was retrieved in 2026 docs.
- YouTube Shorts / video-action-specific minimums for India: not found.

## 6. Concrete starter setup for ₹500–₹2,000/day in India

### Takeaway
Indian agency guides put typical starting budgets at ₹20,000–₹50,000/month for small advertisers, and ₹40,000–₹1,00,000/month for e-commerce. ₹500–₹2,000/day (₹15,000–₹60,000/month) is at or below the low end, which supports one tightly controlled Search campaign, not PMax or Demand Gen.

### Cited Findings
- **Small advertisers:** a workable starting budget is ₹20,000–₹50,000/month. The guide's title also notes GST is added on ad spend. — [upGrowth: Google Ads Pricing India 2026](https://upgrowth.in/google-ads-pricing-india-2026/)
- **E-commerce:** many start at ₹40,000–₹1,00,000/month and scale on returns. Local single-city services: ₹30,000–₹75,000/month. — [Nico Digital, Jun 2026](https://www.nicodigital.com/performance-marketing/google-ads-cost-in-india-cpc-benchmarks/)
- **Use your own data:** a Keyword Planner export for exact terms and cities is the best input (free). Don't average conflicting benchmark sources. — [Rahul D Sarker](https://rahuldsarker.co/insights/google-ads-cpc-india-by-industry)
- **Beginner advice:** avoid general/broad keywords and add negatives (Indian slide deck). Don't mix broad and exact ad groups in one campaign with a campaign-level bid. If no conversions arrive for days, check event configuration first. When scaling, raise budget before bids. — [SlideShare: Google Ad strategies for e-commerce](https://www.slideshare.net/ujjwalakharkar1/google-ad-strategies-for-e-commerce); [Digitanomy Substack](https://digitanomy.substack.com/p/search-engine-marketing-30-pieces)
- **Message-asset requirements:** advertiser verification, "Conversions" bid goal and a compliant starter message. — [Google Ads Help: message assets](https://support.google.com/google-ads/answer/14888522?hl=en)

### Inferences (proposed starter plan; synthesis, not a sourced recipe)
1. **Before spending:**
   - Complete advertiser verification.
   - Build one fast mobile landing page on yours3dindia.com: photo-to-figurine before/after, price ladder (₹3,599 / ₹5,999–₹7,999), delivery time, reviews, and a sticky "Chat on WhatsApp" button (wa.me link with a pre-filled message carrying a campaign tag, e.g. "Hi, I saw your Google ad — couple figurine").
   - Install the Google tag. Track the WhatsApp button click as the primary conversion, plus a "conversation started" conversion where the beta is available.
   - Upload offline order conversions weekly (GCLID or enhanced conversions for leads, captured from the WhatsApp chat) so Google learns from real orders.
2. **Campaign:**
   - One Search campaign, ₹700–₹1,500/day.
   - Exact and phrase match on high-intent themes in tight ad groups: "custom figurine from photo", "3D miniature couple", "personalised couple figurine", "mini me statue", "3D printed photo gift", "anniversary gift for husband unique".
   - Search Partners and Display off; location India, presence only.
   - Ad schedule weighted to evenings if data supports it.
3. **Assets:** WhatsApp message asset, call asset, sitelinks (Couples, Pets, Family, Price, Reviews), image assets showing real figurines, and price assets.
4. **Bidding:** Manual CPC or Max Clicks with a ₹20–₹30 cap for the first 2–3 weeks. Then Max Conversions on WhatsApp clicks. tCPA only after about 30 conversions/month.
5. **Review cadence:** check search terms twice a week and add negatives. Make no structural changes for 2 weeks at a time (learning resets).
6. **Later tests, only if Search is profitable:**
   - Brand-protection campaign at about ₹100/day.
   - PMax without a feed, or a YouTube Shorts / Demand Gen test, at Google's own recommended budgets (≥$100/day, about ₹8,300/day for Demand Gen) before festival windows.
   - Shopping only after building product pages with prices and a buyable checkout.

### Gaps
- No Indian practitioner case study found for a WhatsApp-first personalised-gift business on Google Ads.
- No sourced chat-to-order conversion rates; the cost-per-order maths above is an estimate.
- GST rate on Google Ads in India is not confirmed from a source here. It is commonly 18%; verify against Google India's billing page.
