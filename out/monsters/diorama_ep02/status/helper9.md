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
