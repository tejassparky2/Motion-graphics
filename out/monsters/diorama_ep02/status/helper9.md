# Helper 9: S14, S15, S19 (Ep2)

- 2026-11-02 12:45 UTC: the coordinator approved the a0fceda stills. The full render has started: S14 1-75, S15 1-80
  and S19 1-62 in parallel, then S19 63-124. 279 frames in total, all on 1s (camera moves). The stills took about
  0.5-2 min per frame with three renders running at once. Next: the 2D pass (post_helper9), then
  shots/S14.mp4, S15.mp4, S19.mp4 and their sheets.

- 2026-11-02 12:50 UTC: **S19 handed off as the coordinator asked.** I stopped my S19 chunk with **0 frames rendered**,
  so helper 1 renders f001-062 and helper 10 f063-124. I'm rendering only S14 (1-75) and S15 (1-80).
  **S19 part spec for helpers 1 and 10:**
  - Use helper9.py at **9c14cb8 or later** (it has the drip fix). Builder: `blender -b -P channels/monsters/render_shot.py
    -- diorama_ep02 S19 DIR --frames A-B`. Every frame renders on 1s (ones=(1,124)), so there's no step-multiple start.
  - RAW only: no 2D pass, no post_helper9. Encode DIR's A..B PNGs as `parts/S19_fAAA-BBB.mp4`: libx264
    crf 10 yuv420p 24 fps, the same CLEAN flags as post_helper9.py.
  - Frame A of the part must be render frame A (ffmpeg `-start_number A`).
  - I build the S19 anchors JSON for the 2D pass myself (the builder is deterministic), then join the parts, run
    post_helper9 and do the final encode.
  - S19 renders at about 2 min per frame at full res on the close-up half (blur 10 depth of field). The aerial half is quicker.

- 2026-11-02 12:45 UTC: **S15 handed to XprL.** I stopped my S15 chunk with **0 frames rendered**. I'm rendering only
  **S14** (1-75). The S19 part spec above applies to S15 too (a raw part, libx264 crf 10 yuv420p 24 fps, CLEAN
  flags, no 2D pass). I have the S15 and S19 anchors here already, and I'll join the parts and run the 2D pass when they land.

- 2026-11-02 13:05 UTC: render times are about 120 s a frame here and about 350 s for XprL. **S15 is now split:** XprL does
  f001-040 (part), and I do f041-080 right after S14. Expected: S14 done around 15:20, S15 41-80 around 16:40, and
  XprL's S15_f001-040 part around 16:45. S19 is still with helpers 1 (f001-062) and 10 (f063-124).

- 2026-11-02 13:10 UTC: **New split, from the coordinator.** I render **S14 f001-040** (at f009 now, about 120 s a frame, done
  around 14:15) and stop there. **Helper 5: S14 f041-075.** S15: XprL f001-020, helper 2 f021-040, helper 3 f041-060,
  helper 6 f061-080. **I render no S15.** All parts use the spec above (raw, libx264 crf 10 yuv420p 24 fps, CLEAN,
  `-start_number A`, `parts/<SHOT>_fAAA-BBB.mp4`). Use helper9.py at 9c14cb8 or later; the full shot's frame number is the
  part's first frame. I'll join S14, S15 and S19, then run the 2D pass and the final encode.

- 2026-11-02 14:15 UTC: S15_f061-080 (20 frames) and S19_f001-062 (62 frames) are checked: the frame counts and size
  are right, they're 24 fps, and they match the builder. My S14 is at f037 and stops at f040. post_helper9.py now joins the
  parts by itself. Waiting on: S14 f041-075 (helper 5), S15 f001-020 (XprL), f021-030 (bGqrs), f031-040 (helper 4),
  f041-060 (helper 3), and S19 f063-124 (helper 10).

- 2026-11-02 14:22 UTC: **S14 f001-040 is rendered here** and checked; frame 30 with the 2D pass shows the mark drawing on.
  Helper 5 does **f041-075**. **My container is idle now** (about 120 s a frame here): give me any part that
  hasn't started (for example the end of S14 or S19 f063-124) and I'll render it straight into my build folder.

- 2026-11-02 15:30 UTC: **S19 joined** (helper 1 f001-062 + helper 10 f063-124) and the 2D pass is done. **f049-124 (the
  claw: drips, the glint on "dry") is good.** It's **not pushed yet**: the 124-frame sheet showed a flaw in my crane at
  f001-024. The mist was relative to a short focus, so the village and lake were washed out. The aim slid to the ground
  before the camera pulled back, so it dipped to grass level and passed a trunk, and Kai's cap filled the bottom.
  I've fixed the path: it rises over his left shoulder and never dips, and the haze is absolute so the village reads
  from f001. **I'm re-rendering S19 f001-048 myself** (the parts' f049-124 stay), then I'll push shots/S19.mp4.
  ETA around 16:30 UTC. Nobody else needs to render anything for this.

- 2026-11-02 15:55 UTC: **S15 DONE: shots/S15.mp4 + S15_sheet.jpg** (80 frames, 720x1280, 24 fps, crf 10, 0 encoder
  tags). It's joined from XprL f001-020, bGqrs f021-030, helper 4 f031-040, helper 3 f041-060 and helper 6 f061-080, then my 2D pass.
  Checked: the coral zigzag on bare skin, beats on "same"/"shape", the match cut at f031 (same shape, spot and size,
  one glow frame), then the rift in helper 3's look as the camera tilts up. In the 2D pass I mirrored the mark so it is
  exactly the crack's shape; before, it was the crack's mirror image and flattened to a line for a frame before the cut.
  S14 gets the same fix.
- S19: re-rendering f001-048 here (crane fix), ETA around 16:40. S14: waiting on helper 3 f058-066 and helper 6 f067-075
  (helper 5's f041-057 is in).

- 2026-11-02 15:45 UTC: **The fixed helper9.py (crane over his shoulder, absolute haze) is pushed: use bbd52b1 or later.**
  S19 re-render as the coordinator split it: **I do f001-016** (it stops itself after f016; my first frames are about to
  render). **Helper 10: f017-032, helper 4: f033-048**, as RAW parts to my spec (`parts/S19_f017-032.mp4`,
  `parts/S19_f033-048.mp4`). Frames 49-124 stay from the existing parts. **The existing S19_f001-062.mp4 is now stale for
  f001-048**: my join prefers the new frames, so please don't delete it. **S15.mp4 is already pushed.**

- 2026-11-02 16:10 UTC: **S14 DONE: shots/S14.mp4 + S14_sheet.jpg** (75 frames, 720x1280, 24 fps, crf 10, 0 encoder
  tags). It's joined from my f001-040, helper 5's f041-057, helper 3's f058-066 and helper 6's f067-075, then my 2D pass. The seams are
  invisible: the mean frame-to-frame change across them is 0.9-2.5, the same as neighbouring frames. Checked: the push-in
  over his shoulder; on "wrist" the coral zigzag draws on and flickers, on bare skin below the bracelet; on "glow"
  (f049) a burst and sparkles; then a steady glow with the shrimp leaning in. The lit mark is drawn bolder in S14 (it's
  small at this distance) so it reads at phone size.
- S19: waiting on my f001-016 (rendering) and the parts S19_f017-032 (helper 10) and S19_f033-048 (helper 4).

- 2026-11-02 16:22 UTC: **S19 f001-016 rendered here** (new crane, about 140 s a frame). Waiting on S19_f017-032 (helper 10)
  and S19_f033-048 (helper 4). Then the join (in a fresh folder; the short parts go first, so the old f001-062 part only
  supplies f049-062), the 2D pass, and shots/S19.mp4.

- 2026-11-02 16:40 UTC: **S19 DONE: shots/S19.mp4 + S19_sheet.jpg** (123 frames, which is S19's render_frames since the
  13:06 re-voice; 720x1280, 24 fps, crf 10, 0 encoder tags). It's joined from my f001-016, helper 10's S19_f017-032_v2,
  helper 4's S19_f033-048_v2, helper 1's f049-062 (from f001-062) and helper 10's f063-123 (from f063-124), then my 2D pass.
  Checked: the crane opens over Kai's shoulder on Wren, the lake beyond the trees; it rises over the path (no dip, no
  wash) to the high view of the village on the lake shore; at f049 it cuts to the claw draped over his fists; drops
  fall from the tip with glints, a sparkle on "dry", and the shrimp's eyes go big. The seams at f016/017 and f032/033
  are continuous; f048/049 is the cut. All my word cues still match the re-voiced timing (glow 49, crack cut 31,
  where cut 49, dry 90).
- **All three of my shots are delivered: S14.mp4, S15.mp4, S19.mp4.** Fixes this round: helper9.py's anchors now span the
  shot's own length, and post_helper9's join accepts _v2 part names.
