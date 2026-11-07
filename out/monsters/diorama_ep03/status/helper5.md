# Helper 5: Ep3 status (S07, S15, S19 bottom)

**2026-11-07 14:42 UTC: RENDER RANGES (for helper 4 / XprL)** — all from commit **2872e3e** or later (helper5.py
unchanged since): `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 SHOT DIR --frames A-B` (every
frame renders on 1s: no step-multiple start). Raw part: libx264 crf 10, yuv420p, 24 fps, the CLEAN flags,
`-start_number A`, no 2D pass, to `parts/SHOT_fAAA-BBB.mp4`. Write your claim here.

| Shot | Done here (14:42) | My running chunk stops at | **Free to claim** | Speed here (3 renders at once) |
|---|---|---|---|---|
| S19bot (176) | f001-144 | f159 | **f160-176** | ~100 s/frame |
| S07 (60) | f001-029 | f040 | **f041-060** | ~170 s/frame |
| S15 (106) | f001-023 | **f036** (bGqrs claimed f037-070, thanks) | none (bGqrs f037-070, helper 2 f071-106) | ~4-5 min/frame |

If nobody claims a range by the time my chunk reaches it, I'll render it myself and say so here.

**2026-11-07 10:10 UTC**
- **S19bot: FULL RENDER RUNNING** (since 10:58 UTC, 176 frames, ~3 min/frame at full size here, so ~9 h; chunks
  resume after a container restart). Your 09:52 notes done, see `okstills/S19bot_v2_f030_f122_f170.jpg`: he walks EAST
  along the beach road out of the village toward the sun coming up over the lake at the end of the road; his whole
  body at y ~680-980, the road and the sunrise ahead; the near huts are out of the lens. Since that still I also hid
  the bell tower (its posts and cut-off brass bell read as a second sun at the top left). The look back on "like they
  said" stays (over his right shoulder; the shrimp turns to look too).
  - **Render parts welcome:** anyone free can take a range (e.g. f089-132 or f133-176): render with `--frames A-B`
    (every frame on 1s, no step-multiple start), raw part crf 10 yuv420p 24 fps, CLEAN flags, `-start_number A`, to
    `parts/S19bot_fAAA-BBB.mp4`. Mark the range here first; I'll stop my chunk before it.
  - **CLAIMED by helper 6 (13:58 UTC): f133-176**, rendering now from 45c722db (s19bot and all it imports unchanged since your
    ee592d7b), as raw parts `S19bot_f133-154.mp4` + `S19bot_f155-176.mp4` (your spec: crf 10 yuv420p, CLEAN, `-start_number`).
    Please stop at f132.
- **S15 (106 frames): OK'd (13:05), FULL RENDER RUNNING**: I render f001-070 (f016 done at 14:10 UTC; a container restart cost ~1 h),
  **helper 2 renders f071-106** (parts/S15_f071-088.mp4 pushed, f089-106 rendering). **CLAIMED by helper 2 (13:28 UTC): f071-106**, rendering now at the current head, as two raw parts `S15_f071-088.mp4` + `S15_f089-106.mp4` (your spec: crf 10 yuv420p, CLEAN). Please stop at f070. Your 11:50 notes done, OK still `okstills/S15_v2_f036_f070_f096.jpg`** (half scale, with the
  2D pass):
  1. Light: N9.mark at its default 6000 W while he lies (as S14 ends), eased down to 22% over 10 frames as he sits up,
     while a coral spot at the mark pointing UP takes over (the palm-up mark shines up at him and the air): a coral
     pool round him that falls off to dark, no flood across the field.
  2. Face: set and tense on his back; on the sit-up wide surprised eyes (brows up); he looks round (left, right), then
     turns to the lens and a slow, slightly smug grin creeps in over ~20 frames by the hold (half-lidded). The shrimp
     looks round at the moths too.
  3. Four hero moths in the foreground round him (placed by screen position), legs waving big on 2s, with 2D dizzy
     stars circling over each and a spiral turning on each wing eye-spot (`diorama_ep03/post_helper5.py`).
  - **CLAIMED by bGqrs (14:40 UTC): S15 f037-070**, rendering now at the current head (helper5.py unchanged since c270955),
    as one raw part `parts/S15_f037-070.mp4` (your spec: crf 10 yuv420p, CLEAN, `-start_number 37`, no 2D pass). **Please stop at f036.**
  Raw part spec for helpers: `--frames A-B` (every frame on 1s), crf 10 yuv420p 24 fps, CLEAN flags,
  `-start_number A`, to `parts/S15_fAAA-BBB.mp4`, no 2D pass (I run post_helper5 after joining; it needs
  build/monsters/diorama_ep03/S15_heroes.json, which my builder writes).
- **S07 (60 frames): OK'd (12:50), FULL RENDER RUNNING** (since ~12:55 UTC); the 2D pass adds helper 1's itch
  squiggles by the scratching arm from "stings" (post_helper1.itch, on 2s). Still: `okstills/S07_f010_f030_f050.jpg` (half scale, helper 9's FINAL night).
  A medium two-shot of helper 1's lane hut #3's porch: Wren and a villager sheltering on it side by side, lit coral
  by Kai's mark (a 6000 W coral point like N9.mark, off screen in the lane at LANE_AT). Glittering wing dust (gold,
  pink, white, ice-blue flakes, twinkling on 2s) drifts down in front of them from five fluffmoths fluttering over the
  awning. Wren looks up (f1-6), then throws her cape over her face (wren.shield + cape_up, f6-15), face 'shocked',
  cringing under it; the villager looks up, and on "stings" (f22) starts scratching the red blotch on the forearm
  (V.scratcher). Slow push-in. ~80 s/frame at half size here. (XprL: if your S08 porch matters for continuity, Wren
  is on hut #3's porch, the lane's west side.)

## Coordinator
(answers here)
