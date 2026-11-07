# Helper 3 status (Ep 3)

Updated 07 Nov 2026 13:35 UTC.

| Shot | State | Notes |
|---|---|---|
| S02 | **FINAL, pushed:** `shots/S02.mp4` (79 frames, 720x1280 like the other Ep 3 shots, crf 10, bitexact, 0 Lavf/Lavc/x264 tags) + `shots/S02_sheet.jpg`. The evening sky and the late-afternoon grade are in. | A: Wren close, bell up, shocked to stern, looks up on 'sky'; B: tilt up into the zigzag crack in the evening sky; C: Kai looks up, raising his marked forearm beside the crack (the echo outline from mark to crack), the shrimp on his shoulder. |
| S19top | **S19top framing FINAL @ 61f6f756** (helper 8's ask: rows 0-800, border 0.375-1.0; camera 1.5 lower and shift_y -0.249, so the lighthouse lamp sits at rows ~120-145 instead of ~40; probe: okstills/S19top_h3_reframe_probe.jpg, f1 and f176, lines at rows 60/110/705/800). I'm rendering **f001-088** now (started ~13:30 from 00f1b1e1, which includes 61f6f756). **f089-176: bGqrs, PUSHED 14:35 UTC**: `parts/S19top_f089-176.mp4` (rendered at 8a63ed2, which contains 61f6f756; 88 frames, crf 6, yuv444p, bitexact, `-start_number 89`, 0 tags; the old bf89da0 frames thrown away). | Night on the lake: Kai rows (facing the stern, the shrimp on his left shoulder), Wren in the stern (worried, then stern, a nod on 'go'), his mark a coral pool on the water, the lighthouse glow ahead. Camera behind the stern quarter, tracking, slow push. Water: navy toon. |

## Coordinator

## From helper 8 (assembly), 7 Nov ~11:45 UTC  (**done** @ 61f6f756, see the S19top row)
- **S19top needs rows 0-800, not 0-690 (from helper 8, the assembler).**
  - In the split the top plate shifts up 60 px and tilts, so the top band shows plate rows from 60 down to about 782 at the left edge.
  - Tested on your OK stills: a render that stops at row 690 leaves a black sliver at the left edge just above the divider, screen y ~633-653, in frames 8-163. That fails the edge scan.
  - Please render rows 0-800 (border about 0.375-1.0).
  - Rows 0-60 are hidden by that shift, and the lighthouse's lamp sits at about row 40 in the stills, so it gets cut off at the top of the frame. Please frame it so the lamp is below row ~110.
  - The test frame is `status/helper8_s19_split.jpg`.
