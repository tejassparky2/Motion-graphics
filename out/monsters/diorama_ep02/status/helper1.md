# Helper 1 status: Ep 2 (2 Nov 2026)

Done: S02, S04 and S16 are on this branch (commit 3d28621), in out/monsters/diorama_ep02/shots/, each with a _sheet.jpg.
- S02 has 45 frames, S04 has 66 and S16 has 47. All are 720x1280 at 24 fps, crf 10.
- Encoder tags: 0. No black edges.
- Render time per frame: S02 ~51 s, S04 ~56 s, S16 ~86 s.
- Full notes and the OK stills: out/monsters/diorama_ep02/okstills/helper1_REPORT.md.

Known weak points (I'll fix them if QA wants):
- S02: the bird stays in the upper right and only drops near the end, and the shrimp is small.
- S04: the three scratch marks are small at phone size, and Kai's face is hidden under his cap once he curls.
- S16: blurred foreground stumps and Kai's cap fill the bottom half, and the hill reads flat.

Status: idle. I'm checking git for QA notes.

## S19 f001-062 (coordinator job, 2 Nov 12:50 UTC)
- Rendering S19 frames 1-62 with helper9.py, into out/monsters/diorama_ep02/parts/S19_f001-062.mp4 (raw: crf 6,
  yuv444p, bitexact, no tags). Started ~12:50 UTC; estimate ~1 h at ~50-90 s/frame.
- Helper 9: your status says you're also rendering S19 1-62. If you'd rather keep yours, say so here and I'll stop.
  Otherwise you can drop yours and start 63-124 now.
