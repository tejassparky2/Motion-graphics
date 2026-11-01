# WW2 history channel (long videos)

This is a separate channel from Interestingly Strange (owner, 31 Oct 2026: "long video on world war 2 with detailed high quality animation even 2d stick man works, this is for different channel"). The work lives on branch `ccr-56282fe5-evehq4-ww2`.

**Owner's choices (31 Oct 2026):**
- About 10 minutes, the whole war from start to end.
- Stick figures plus animated maps.
- Made in the main chat, on its own branch.

**Rules:**
- **Script first.** The owner approves the script, then I make two voice samples and style frames, and only then render (as on the main channel).
- **Facts are sourced.** Every specific number or date is checked, and the sources are listed under the script. Where estimates differ, the narration gives a range or says "around".
- **No Nazi symbols.** Germany is shown by colour and label. No graphic violence: stick figures, flashes and maps only.
- **The Holocaust is handled with care.** No stick-figure victims, and the music drops. Argue ideas and report facts; never mock.
- **Landscape format.** 1920x1080, 24 fps, chapters with timestamps in the description, and a visual change every 1-2 seconds.
- **Narration as on the main channel.** Every sentence is its own take with a real pause, every line is checked with Whisper medium, and there is no cloned voice of any real person.
- **Clean files.** No metadata or encoder tags in the outputs.

**Files:**
- `ep01_script.md`: Episode 1 script, for approval.
- `sound.py`: the sound palette (original, synthesized in numpy, leaning to a 1940s newsreel score): score cues (tension, march, somber, low tone, triumph, drum-hit stinger, newsreel fanfare), a phonograph and old-radio texture, 20 effects, and `Mix` (narration duck, hard cuts, -14 LUFS / -1 dBTP master). `python channels/ww2/sound.py` writes `out/ww2/style/sound_demo.wav` and an effects reel; `test_sound.py` checks it.

**Episode 1 status (1 Nov 2026): delivered.**
- "World War 2 Explained: From the First Shot to the Last (Animated)", 12:14, 1920x1080, 24 fps. Helper 4 gave the final QA pass on e4d9bc3. The owner got the video, `out/ww2/ep01/thumbnail.png`, `upload_sheet.md`, `captions.srt` and `chapters.txt`.
- The final look is the animated 1940s posters (STYLE.md), not stick figures.
- The video isn't in git; rebuild it with `bash channels/ww2/ep01/deliver.sh`. That script concats the 32 chunks in `out/ww2/ep01/parts/` with `mix.flac`, encodes one generation (x264 crf 20 slow/animation, 4 Mbps cap, so ≤ 376 MiB) and strips tags. The send-file limit is 400 MiB; the stream-copy master is 653 MiB and too big to send.
- **QA lesson:** a camera framed below centre (cy > H/2 at zoom 1.0) exposes unpainted black canvas at the frame bottom. `core.paper()` now mirrors the page past its edges, and props must reach past the frame. QA runs an edge-band scan on every episode (every Nth frame: an edge strip with mean below 6 in a non-dark frame).
