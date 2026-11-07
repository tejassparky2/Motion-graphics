# Helper 3 status (Ep 3)

Updated 07 Nov 2026 15:20 UTC.

| Shot | State | Notes |
|---|---|---|
| S02 | **FINAL, pushed:** `shots/S02.mp4` (79 frames, 720x1280 like the other Ep 3 shots, crf 10, bitexact, 0 Lavf/Lavc/x264 tags) + `shots/S02_sheet.jpg`. The evening sky and the late-afternoon grade are in. | A: Wren close, bell up, shocked to stern, looks up on 'sky'; B: tilt up into the zigzag crack in the evening sky; C: Kai looks up, raising his marked forearm beside the crack (the echo outline from mark to crack), the shrimp on his shoulder. |
| S19top | **FINAL, pushed:** `shots/S19top.mp4` (176 frames, 720x1280, crf 10, bitexact, 0 tags) + `shots/S19top_sheet.jpg`. Framing FINAL @ 61f6f756: plate rows 0-800 painted (black below, as a top panel), lighthouse lamp at rows ~120-145. f001-088 rendered by me, f089-176 by bGqrs (parts/S19top_f089-176.mp4), both from 61f6f756; the seam at f88/89 is clean (frame-to-frame change 1.6 / 1.0 like every other step on 2s). | Night on the lake: Kai rows facing the stern, the shrimp on his left shoulder, Wren in the stern (worried, then stern, a nod on 'go'), his mark a coral pool on the water, the lighthouse glow ahead; camera behind the stern quarter, tracking, slow push. |

## Coordinator

## From helper 8 (assembly), 7 Nov ~11:45 UTC  (**done** @ 61f6f756, see the S19top row)
- **S19top needs rows 0-800, not 0-690 (from helper 8, the assembler).**
  - In the split the top plate shifts up 60 px and tilts, so the top band shows plate rows from 60 down to about 782 at the left edge.
  - Tested on your OK stills: a render that stops at row 690 leaves a black sliver at the left edge just above the divider, screen y ~633-653, in frames 8-163. That fails the edge scan.
  - Please render rows 0-800 (border about 0.375-1.0).
  - Rows 0-60 are hidden by that shift, and the lighthouse's lamp sits at about row 40 in the stills, so it gets cut off at the top of the frame. Please frame it so the lamp is below row ~110.
  - The test frame is `status/helper8_s19_split.jpg`.


## Next
S02 and S19top are both final (15:20 UTC). **S18 f028-054 for helper 9: DONE, pushed** (16:22 UTC, `parts/S18_f028-054.mp4`, 27 frames, from feacea3, 0 tags). **Now: S15 f017-024** (coordinator, 16:41: the pop at f31/32): renders as soon as helper 5's "S15 redo from <commit>" line is up, then the raw part `parts/S15_f017-024.mp4` (crf 10, yuv420p, CLEAN, `-start_number 17`).
