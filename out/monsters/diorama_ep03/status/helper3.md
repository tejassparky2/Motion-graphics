# Helper 3 status (Ep 3)

Updated 07 Nov 2026 13:20 UTC.

| Shot | State | Notes |
|---|---|---|
| S02 | **Your 3 fixes in, OK stills re-pushed** (okstills/S02_h3_sheet.jpg: f12, f30, f44, f62). **Full render running** (79 frames), then the 2D pass + encode. Your late-afternoon grade is in the 2D pass (greens -25% saturation, level -10%, peach highlights; okstills sheet updated). | 1) Evening sky: the 3D sky (one flat haze colour) is keyed out in the 2D pass and an evening sky painted behind: peach/orange low to deeper blue up top by real elevation, wispy warm-lit clouds fixed in the sky, the crack the darkest thing in it; a light warm cast over the frame. 2) The crack shot: treetops along the bottom, a tilt up into it. 3) The shrimp on the outer edge of Kai's left shoulder, beside his face, looking up with him. Note: to keep the shrimp off Wren's face in A, A's camera is wider of his shoulder, so his blurred forearm/mark is no longer in A's foreground (its coral light still is). |
| S19top | **S19top framing FINAL @ 61f6f756** (helper 8's ask: rows 0-800, border 0.375-1.0; camera 1.5 lower and shift_y -0.249, so the lighthouse lamp sits at rows ~120-145 instead of ~40; probe: okstills/S19top_h3_reframe_probe.jpg, f1 and f176, lines at rows 60/110/705/800). I render **f001-088** right after S02 (queued, starts ~13:45). **f089-176: bGqrs** — the part started 12:28 at bf89da0 has the OLD framing and won't match; bGqrs has been asked to stop it and re-render `-- diorama_ep03 S19top OUT --frames 89-176` from **61f6f756 or later**, RAW part `parts/S19top_f089-176.mp4` (crf 6, yuv444p, bitexact, `-start_number 89`, no tags). | Night on the lake: Kai rows (facing the stern, the shrimp on his left shoulder), Wren in the stern (worried, then stern, a nod on 'go'), his mark a coral pool on the water, the lighthouse glow ahead. Camera behind the stern quarter, tracking, slow push. Water: navy toon. |

## Coordinator

## From helper 8 (assembly), 7 Nov ~11:45 UTC  (**done** @ 61f6f756, see the S19top row)
- **S19top needs rows 0-800, not 0-690 (from helper 8, the assembler).**
  - In the split the top plate shifts up 60 px and tilts, so the top band shows plate rows from 60 down to about 782 at the left edge.
  - Tested on your OK stills: a render that stops at row 690 leaves a black sliver at the left edge just above the divider, screen y ~633-653, in frames 8-163. That fails the edge scan.
  - Please render rows 0-800 (border about 0.375-1.0).
  - Rows 0-60 are hidden by that shift, and the lighthouse's lamp sits at about row 40 in the stills, so it gets cut off at the top of the frame. Please frame it so the lamp is below row ~110.
  - The test frame is `status/helper8_s19_split.jpg`.
