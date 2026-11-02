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

## QA S02 fix (2 Nov ~13:40 UTC)
- Found the cause: my smoke-puff clearing (`_clear_smoke`) matched every empty whose name starts with "puff", and
  that includes the shrimp (`puff_root`). So it hid the shrimp in **S02 and in S04** (the shrimp in Kai's cupped
  hands). S16 has no shrimp object. Fixed: only top-level smoke puffs are cleared now.
- S02 is being reframed so the shrimp sits clearly at the puddle edge above the caption band. The drop starts sooner
  (the wings snap shut at f7, and the drop curve is less delayed). The bird and its shadow converge on the shrimp.
- S02 is now 44 render frames ("The bird struck first.", timing e6a1dbb). Plan: re-render S02 (44 f) and then **S04 (66 f)** too, with the shrimp visible in his hands. Both get a new
  mp4 + sheet. S19 f001-062 keeps running; it will use the crf 10 yuv420p spec, as the coordinator asked.

## S19 f001-062 done (2 Nov 14:12 UTC)
- out/monsters/diorama_ep02/parts/S19_f001-062.mp4 has 62 frames, 720x1280 at 24 fps. It's libx264 crf 10 yuv420p
  with the CLEAN flags, and `-start_number 1`, so part frame 1 is render frame 1. Raw: no 2D pass.
  Tags 0, no black edges.
- Rendered with helper9.py from after 9c14cb8, at about 60-130 s per frame (it shared the CPU with the S02 re-render).
- Helper 9: frames ~20-24 of the crane pass through a tree canopy, so the frame goes almost all green leaf blur
  for about 5 frames. If that's not intended, tell me here and I'll re-render.

## S02 re-rendered (2 Nov ~14:40 UTC): QA fix done
- out/monsters/diorama_ep02/shots/S02.mp4 has 44 frames ("The bird struck first.", timing e6a1dbb), plus
  S02_sheet.jpg. Tags 0, no black edges.
- The shrimp is visible in every frame, drinking at the puddle edge at about 57% down the frame (above the caption
  band). The bird's growing shadow spreads over it, and the bird dives in from the top right onto it. The wings snap
  shut at f7 and the drop starts sooner.
- I also fixed post_helper1, which could leave a stale frame from a longer earlier cut.
- S04 is re-rendering now (66 f) so the shrimp shows in Kai's cupped hands. The old S04 had it hidden by the same bug.

## S04 re-rendered (2 Nov ~15:50 UTC)
- out/monsters/diorama_ep02/shots/S04.mp4 has 66 frames, plus S04_sheet.jpg. Tags 0, no black edges.
- The shrimp now shows in Kai's cupped hands in every frame. It was hidden by the same smoke-clearing bug as S02.
  He curls round it after the rake. Everything else is unchanged: the rake, the claw slash, three thin marks, no
  blood, the bird swooping away.
- All my Ep 2 jobs are done: S02, S04, S16, and S19 f001-062. I'm idle and checking git for QA notes.

## S20bot v2 f101-120 (2 Nov 20:25 UTC): ready, waiting for GO
- The coordinator's heads-up arrived. The render + encode script is ready: it pulls first, renders S20bot f101-120
  with helper 4's builder, then encodes parts/S20bot_v2_f101-120.mp4 (crf 6 yuv444p, bitexact, `-start_number 101`).
- **Not started.** It waits for "GO S20bot v2".
- 20:40 UTC: GO received. Pulled 3b479cf, and S20bot v2 f101-120 is rendering. It encodes to
  parts/S20bot_v2_f101-120.mp4 when the render finishes.
- (QA note from helper4.md: S04 was re-rendered at 0241a90, with the shrimp in Kai's cupped hands in every frame.)
