# yours3dindia: owner's 3D figurine videos

Owner's standing preferences for every video made here (keep them unless the owner says otherwise):

- **Voice:** the owner's own cloned voice (`NARRATOR_ENGINE=clone`, `tools/voiceover.py`), default pace 0.85. Only ever
  clone the owner's voice; leave Chatterbox's watermark in place.
- **Workflow:** look at the uploads, send the plan + script, wait for approval, then make it. Keep the owner's words;
  flag words the clone may mishear (write websites and numbers the way they should be spoken, e.g.
  "yours 3D India dot com", "zero point two"; captions show the written form).
- **Platform:** Instagram Reels, 1080x1920, captions and graphics clear of the Reels UI (bottom ~380 px).
- **Brand / call to action:** @yours3dindia · "Comment below to get a DM" (no keyword) · free previews on WhatsApp
  +91 91647 48401 · website yours3dindia.com.
- **Look:** motion graphics between shots (see `reel01/build_v3.py`: tracker, scan, counters, wipes, word-by-word
  captions), light grade + vignette on phone clips.
- **Background:** keep the real background. No background replacement (owner, 11 Oct 2026); lighting and colour
  fixes, a blur or a tighter crop are fine. `tools/bgswap.py` exists but is not used by default.
- Don't write "Pixar" in videos (trademark); say "3D cartoon render".
- Customer photos/names only with the customer's consent.
- Finished videos and the owner's raw footage stay out of git (`out/3d/` is ignored).
