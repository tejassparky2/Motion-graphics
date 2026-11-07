# Helper 10: S12 and S14 (Ep 3)

## Status
- 2026-11-07 11:20 UTC: **both builders are in** `channels/monsters/diorama_ep03/helper10.py` (S12 79 frames,
  S14 84 frames, from timing.json) and the 2D pass is in `post_helper10.py`. Test stills are rendering; I'll push
  the OK stills to okstills/ when they look right. No full render before the coordinator's OK.
- **S12 (the orbit)** continues helper 4's S11 explainer on the same stage: the dark night ground, the coral glow, one
  big fluffmoth, the same 2D style. Now the light is **above**: the moth flies round and round under it, side-on (the
  ring is an ellipse), banked about 42 degrees so its back always faces the glow (helper 6's `back_to`). 2D: S11's
  glow line from the light to its back all the way round, the light's bloom, a dotted trail tracing the ring, and
  the hill silhouette. About 1.7 laps; a slow push-in on 1s.
- **S14 (the flip)** picks up bGqrs's S13 end on action (I import bGqrs's staging: the spot, the lying pose with the
  palm-up arm, the light levels and the camera):
  - f1-12, the held beat: Kai on his back, the wrist glowing up through the grass, the swarm still circling above
    (S13's 26 moths, member by member, continuing their circles).
  - f12-40: a wave of rolls: each moth turns upside down to keep its back to the light below, stalls (the circling
    dies, wings frantic) and tumbles (a flip) into the grass round him.
  - The landings: **plop f32, plop f38, plop f44**, then the rest f46-66, each on its back with legs waving
    (helper 6's `upside_down`). 2D dust puffs on 2s at each landing.
  - Kai: determined, eyes on the swarm, then following them down; a grin starts on the second plop.
  - The camera starts on S13's last framing and eases down to the grass.
- **Hand-offs:**
  - helper 7 (sound): the plops are at S14 f32, f38, f44, then a patter f46-66. Every landing frame is in
    `build/monsters/diorama_ep03/S14_landings.json`.
  - helper 5 (S15): the same file has every moth's landing spot (world x, y) and size, so S15 can start from them.
  - helper 6: `upside_down` rests the body at `BACK_REST` unscaled (0.86). A 0.42 moth floats about 0.5 above the
    grass. I re-key the root at `BACK_REST * scale` after calling it; you may want to scale it inside.

## Progress
- 10:35 UTC: **S12 OK'd (coordinator 10:22). The full render is running** (79 frames, two chunks). Then the 2D pass,
  then `shots/S12.mp4` + sheet.

## OK stills
- **S12:** `okstills/S12_f010.png` (the moth on one side of the ring, seen from behind: its back tilted to the light,
  the glow line landing on it) and `okstills/S12_f030.png` (the other side, its face toward us, still banked with its
  back to the light). These are half-res renders scaled up, with the 2D pass. The moth is 1.9x on S11's stage; about
  1.7 laps.
- **S14:** `okstills/S14_f001.png` (the held beat: S13's end framing, Kai on his back, the wrist glowing up, the
  swarm circling above), `S14_f040.png` (moths rolled upside down and tumbling, the first ones landed with a dust
  ring), `S14_f066.png` (everyone down on their backs round him, legs up, clear of the caption band). The plops are
  at f32, f38 and f44. A mid-roll still (f24) is rendering and will be added. Half-res renders scaled up, with the 2D
  dust puffs. The night lighting is still bGqrs's stand-in until helper 9's night grade lands.

## S14 render parts (84 frames, every frame rendered: the camera moves on 1s)
**Wait for the coordinator's OK on the S14 stills (noted below) before starting.** Then write your name next to a
range here and push before you start.

| Part | Frames | Who |
|---|---|---|
| 1 | f001-021 | helper 10 |
| 2 | f022-042 | (free) |
| 3 | f043-063 | (free) |
| 4 | f064-084 | helper 2 (claimed 10:15 UTC, starts on the coordinator's OK) |

- Render: `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S14 OUT --frames A-B` (pull first).
- Encode a RAW part (crf 6 yuv444p, bitexact, no tags, `-start_number A`) to `out/monsters/diorama_ep03/parts/S14_fAAA-BBB.mp4` and push.
  I'll join the parts, run the 2D pass and encode shots/S14.mp4.

## Coordinator
