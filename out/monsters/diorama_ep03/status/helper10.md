# Helper 10: S12 and S14 (Ep 3)

## Status
- **Next: S18 f055-081 for helper 9** (coordinator 15:12: 4-way split, was f037-072). Ready now; I start from the
  "S18 parts from <commit>" line in status/helper9.md (or the coordinator's release from 207f050), claim there first.
  Output `parts/S18_f055-081.mp4`, `-start_number 55`.
- **15:05 UTC: S01 f046-062 DONE, pushed** `parts/S01_f046-062.mp4` (from exactly `bb5be5d`; 17/17 frames, 0 tags). Output: `parts/S01_f046-062.mp4` (raw, crf 6 yuv444p, start_number 46).
- **12:45 UTC: S14 FINAL.** `shots/S14.mp4` + `S14_sheet.jpg`: 84/84 frames, crf 10 yuv420p, 0 tags. Joined from
  the four parts (1+2 helper 10, 3 helper 4, 4 helper 2 in two chunks), all rendered from helper 9's FINAL night
  `09d120fd`. Seams checked: the frame differences across f21/22, f42/43, f63/64 and f74/75 match the on-2s rhythm
  around them. The 2D pass is on (the coral column, roll arcs, stall ticks, dust puffs at every landing). **Both my
  shots, S12 and S14, are done.** I'm free for another job.
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

- 11:05 UTC: **S14: working on the coordinator's three notes (10:36).** Parts stay on hold until the new stills are OK'd.
  1. Night: switched to helper 9's shared `N9.night(n)` and `N9.mark(k)` (not marked FINAL yet; I'll re-check
     when it is).
  2. The light below: N9.mark's 6000 W key, a 3200 W coral under-glow above the wrist that lights the swarm from
     below, and a visible soft coral cone rising from the palm-up wrist through the grass, plus a glowing disc at
     its foot.
  3. The flip at phone size: four hero moths (the plops at f32, f38 and f44, plus f48) drift low over the foreground,
     roll over big near the lens (2D curved roll arcs), wobble in the stall (2D shock ticks) and drop onto their
     backs in front of the wrist. The camera moves from S13's last frame (bGqrs's `camera_at(45)`) down and in to a
     low, close view of that spot by f30, so we see them land legs-up. The other 24 land small in the ring.
  - It also uses bGqrs's new `swarm_layout()`/`swarm_at()` (28 moths), so S14 continues S13's circles exactly.

- 11:45 UTC: **S12 done and pushed: `shots/S12.mp4` + `S12_sheet.jpg`**, 79/79 frames, crf 10, no tags. The 2D pass
  (the glow line, the bloom, the dotted ring, the hill) is from `post_helper10.py`.
- S14: new stills rendering with the fixes (no decimation on the close heroes, which caused the speckles; the
  visible uplight is now a 2D coral column, because the 3D cone blew out in the grade; the heroes land clear of his face and
  above the caption band).

## OK stills
- **S12:** `okstills/S12_f010.png` (the moth on one side of the ring, seen from behind: its back tilted to the light,
  the glow line landing on it) and `okstills/S12_f030.png` (the other side, its face toward us, still banked with its
  back to the light). These are half-res renders scaled up, with the 2D pass. The moth is 1.9x on S11's stage; about
  1.7 laps.
- **S14 (new, 12:25 UTC, after the coordinator's three notes):** `okstills/S14_f001.png` (the held beat: S13's last
  frame, night, the coral column rising from his palm-up wrist, the swarm lit from below), `S14_f024.png` (the camera
  coming down; the hero moths rolled upside down near the lens, the roll and stall ticks), `S14_f040.png` (a hero
  plop with its dust ring, others tumbling), `S14_f060.png` (low and close: the heroes on their backs, legs up, in
  front of him; Kai's face and the glow behind; the ring of others small round him). The plops are at f32, f38 and
  f44 (heroes), plus f48. The night is helper 9's N9.night + N9.mark, with a 3200 W coral under-glow; the visible
  column is 2D. In the full render the wings no longer cast moon shadows (the dark smudges on the grass in these
  stills are gone). Half-res renders scaled up, with the 2D pass.

## S14 render parts (84 frames, every frame rendered: the camera moves on 1s)
**GO: helper 9's night is FINAL at `09d120fd` (11:29 UTC). Pull that commit or later before you render.** Parts 1+2
(helper 10) started 11:35 UTC, **both pushed 12:40 UTC** (night `09d120fd`). Waiting on parts 3 (helper 4) and 4 (helper 2); I join as soon as they land.
**S14 OK'd by the coordinator (11:20 UTC).** Start your part only **after helper 9's FINAL night commit** (marked
FINAL in status/helper9.md, ~11:40 UTC): pull that commit (or later) so every part has the same night. I'll note
the commit hash here when it lands. Write your name next to a range here and push before you start.

| Part | Frames | Who |
|---|---|---|
| 1 | f001-021 | helper 10: **DONE** 12:01 UTC, parts/S14_f001-021.mp4 (21/21, tags 0) |
| 2 | f022-042 | helper 10: **DONE** 12:36 UTC, parts/S14_f022-042.mp4 (21/21, tags 0) |
| 3 | f043-063 | helper 4: **DONE, pushed** `parts/S14_f043-063.mp4` (from 09d120f; 21 frames, crf 6 yuv444p, start_number 43, 0 tags; about 140 s/frame) |
| 4 | f064-084 | helper 2: **DONE** (S14_f064-074 + S14_f075-084) |

- Render: `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S14 OUT --frames A-B` (pull first).
- Encode a RAW part (crf 6 yuv444p, bitexact, no tags, `-start_number A`) to `out/monsters/diorama_ep03/parts/S14_fAAA-BBB.mp4` and push.
  I'll join the parts, run the 2D pass and encode shots/S14.mp4.

## Coordinator
