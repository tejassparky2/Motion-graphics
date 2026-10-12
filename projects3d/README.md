# yours3dindia: owner's 3D figurine videos

Owner's standing preferences for every video made here (keep them unless the owner says otherwise):

- **Voice:** the owner's own cloned voice (`NARRATOR_ENGINE=clone`, `tools/voiceover.py`), default pace 0.85. Only ever
  clone the owner's voice; leave Chatterbox's watermark in place.
- **Reel voice style (owner, 12 Oct 2026: "use the speed and pause from the Your Cute Mini reference"):** one line per
  paragraph in the script, each line one flowing take, ~5.3 syllables/s, ~0.9 s pause after each line, polished:
  `tools/voiceover.py SCRIPT NAME --engine turbo --flow --gap 0.9 --polish` (owner picked Chatterbox Turbo at its
  natural speed, 12 Oct 2026: "the speed is good in ab_T"; sample `out/voiceover/ab_T3.mp3`). Whisper-checked retakes.
  No `--even` for Turbo (the owner preferred its own speed); `--even` stays available for the older Chatterbox voice.
- **Workflow:** look at the uploads, send the plan + script, wait for approval, then make it. Keep the owner's words;
  flag words the clone may mishear (write websites and numbers the way they should be spoken, e.g.
  "yours 3D India dot com", "zero point two"; captions show the written form).
- **Platform:** Instagram Reels, 1080x1920, captions and graphics clear of the Reels UI (bottom ~380 px).
- **Brand / call to action:** @yours3dindia · "Comment below to get a DM" (no keyword) · free preview on WhatsApp
  +91 91647 48401. WhatsApp replaces the website as the place to send people (owner, 12 Oct 2026): don't put
  yours3dindia.com in new videos unless the owner asks.
- **Look:** motion graphics between shots (see `reel01/build_v3.py`: tracker, scan, counters, wipes, word-by-word
  captions), light grade + vignette on phone clips.
- **Background:** keep the real background. No background replacement (owner, 11 Oct 2026); lighting and colour
  fixes, a blur or a tighter crop are fine. `tools/bgswap.py` exists but is not used by default.
- **Product facts (owner):** printed in full colour by the printer (not hand-painted); hand-finished = supports
  removed and sanded by hand. Sizes/prices and "free delivery across India", "free previews in 1-2 minutes" come
  from the owner's WhatsApp bot (12 Oct 2026). **Pricing rule (owner, 12 Oct 2026): products start from ₹3,599
  (single figurine); always lead with "from ₹3,599", never ₹5,999.** ₹5,999 / ₹6,999 / ₹7,999 (13 / 15 / 18 cm) are
  the couple prices: label them "couple" wherever they appear.
- Don't write "Pixar" in videos (trademark); say "3D cartoon render".
- Customer photos/names only with the customer's consent.
- Finished videos and the owner's raw footage stay out of git (`out/3d/` is ignored).
