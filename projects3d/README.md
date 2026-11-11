# yours3dindia: owner's 3D figurine videos

Owner's standing preferences for every video made here (keep them unless the owner says otherwise):

- **Voice:** the owner's own cloned voice (`NARRATOR_ENGINE=clone`, `tools/voiceover.py`), default pace 0.85. Only ever
  clone the owner's voice; leave Chatterbox's watermark in place.
- **Customer voice dubs (owner, 25 Oct 2026):** Sowmya (the customer in reels 05-06) can't speak Hindi and agreed to
  her voice being cloned to dub her testimonials into Hinglish for the Hindi page. Clone only from her own takes, only
  for her own testimonials, keep her meaning (captions show her real English words), leave Chatterbox's watermark in.
  She is the owner's business partner. Owner (27 Oct 2026): no partnership, AI or dub tags in any reel or caption. Her voice reference and the dubs stay out
  of git. Nobody else is cloned without the same clear consent.
- **Reel voice style (owner, 12 Oct 2026: "use the speed and pause from the Your Cute Mini reference"):** one line per
  paragraph in the script, each line one flowing take, ~5.3 syllables/s, ~0.9 s pause after each line, polished:
  `tools/voiceover.py SCRIPT NAME --engine turbo --flow --gap 0.9 --polish` (owner picked Chatterbox Turbo at its
  natural speed, 12 Oct 2026: "the speed is good in ab_T"; sample `out/voiceover/ab_T3.mp3`). Whisper-checked retakes.
  No `--even` for Turbo (the owner preferred its own speed); `--even` stays available for the older Chatterbox voice.
  **Faster read (owner, 2 Nov 2026: "make voice faster so it won't feel boring"):** `--gap 0.35 --tempo 1.12` (every
  take sped up 12%, pitch kept; reel 07). Use this for new reels unless the owner says otherwise; re-check with Whisper.
- **Workflow:** look at the uploads, send the plan + script, wait for approval, then make it. Keep the owner's words;
  flag words the clone may mishear (write websites and numbers the way they should be spoken, e.g.
  "yours 3D India dot com", "zero point two"; captions show the written form).
- **Platform:** Instagram Reels, 1080x1920, captions and graphics clear of the Reels UI (bottom ~380 px).
- **Brand / call to action:** @yours3dindia · "Comment below to get a DM" (no keyword) · free preview on WhatsApp
  +91 91647 48401. WhatsApp replaces the website as the place to send people (owner, 12 Oct 2026): don't put
  yours3dindia.com in new videos unless the owner asks.
- **Learning reels (owner, 30 Oct 2026: "in first second people should see we getting something to learn"):** the
  very first frame already reads as a tutorial, with no fade-in: a "HOW TO" tag, the topic as a big title, the
  numbered steps on screen and a "SAVE IT" bookmark; every step then gets a "STEP n OF N" bar and the tool's name.
  Learning reels can run up to 1:10 when the information needs it (owner, 27 Oct 2026).
- **Look:** motion graphics between shots (see `reel01/build_v3.py`: tracker, scan, counters, wipes, word-by-word
  captions), light grade + vignette on phone clips.
- **Background:** keep the real background. No background replacement (owner, 11 Oct 2026); lighting and colour
  fixes, a blur or a tighter crop are fine. `tools/bgswap.py` exists but is not used by default.
- **Product facts (owner):** printed in full colour by the printer (not hand-painted); hand-finished = supports
  removed and sanded by hand. Sizes/prices and "free delivery across India", "free previews in 1-2 minutes" come
  from the owner's WhatsApp bot (12 Oct 2026). **Pricing rule (owner, 12 Oct 2026): products start from ₹3,599
  (single figurine); always lead with "from ₹3,599", never ₹5,999.** ₹5,999 / ₹6,999 / ₹7,999 (13 / 15 / 18 cm) are
  the couple prices: label them "couple" wherever they appear.
  **Keychains (owner, 11 Nov 2026):** ₹999 for one, ₹599 each for 10 or more (bulk, e.g. return gifts).
  Delivery takes up to 7 days (owner, 20 Oct 2026: "within 7 days" is true).
  Sowmya says "7 to 10 days" in her reel 08/09 takes: owner (11 Nov 2026) "keep"; those sheets say 7–10 days.
- Don't write "Pixar" in videos (trademark). **Style (owner, 2 Nov 2026): the figurines are semi-realistic, not
  cartoon**; say "semi-realistic 3D design", and "mini you" for a figurine of the viewer.
- Customer photos/names only with the customer's consent.
- **Kannada page (owner, 11 Nov 2026):** a separate page for Sowmya's Kannada takes. Never mix languages in one reel;
  open each reel with its best hook; Kannada reels have **no captions**, just a clean edit (titles and labels stay
  English).
- **Talking takes (owner, 11 Nov 2026):** keep every complete sentence she says (don't drop takes or lines), but
  cut where she stops, stumbles or says it wrong, half-finished endings, stray words and long pauses (jump cut).
- **Front-camera takes are mirrored:** check names on bases/keychains and flip (`testimonial.FLIP`).
- Finished videos and the owner's raw footage stay out of git (`out/3d/` is ignored).
