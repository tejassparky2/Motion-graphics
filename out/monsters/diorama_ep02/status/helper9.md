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
