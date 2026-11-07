# bGqrs status (Ep 3)

Updated 7 Nov 2026, 14:35 UTC (S15 part started 14:31).

| Shot | State | File |
|---|---|---|
| S19top f089-176 (for helper 3) | **Raw part, pushed.** 88 frames (f89-176), 720x1280 at 24 fps, libx264 crf 6, yuv444p, bitexact + stream-copy remux, `-start_number 89`, no 2D pass, 0 encoder tags. Rendered from helper 3's **framing FINAL @ 61f6f756** (HEAD 8a63ed2 contains it), 13:08-14:30 UTC, ~50 s/frame. The bf89da0 frames (old framing) were thrown away. The lighthouse lamp is near the top, the content is in rows 0-800 and black below, as in helper 3's probe. | parts/S19top_f089-176.mp4 |
| S13 "So I put the light below them." | **FINAL, pushed.** 57/57 frames, 720x1280 at 24 fps, crf 10, bitexact + stream-copy remux, 0 encoder tags. Rendered at 62572f2 on helper 9's FINAL night/mark (09d120f), ~55 s/frame. 2D pass: `post_bgqrs.py` (the zigzag, the coral #ff8466 cone and rays with a hot white core, grass blades, sparks). Beats: dip f3, flat f13, settled f16, arm out f17-25, the bloom on "below" f26. | shots/S13.mp4 + S13_sheet.jpg |

### S13 staging (57 render frames; "below" at f26)
- **Where:** the grass on the village's north edge, east of the track: his feet at **(12, -140)** at frame 1.
- **The drop (on 2s):** standing with the left wrist raised to the swarm (as S10 leaves him) -> a dip (f3) -> sits
  back (f8) -> flat on his back (f13, a small bounce) -> settled (f16). He lies **east-west, head to the west**, hips at
  (9, -140), LYING_V3's legs. The left arm goes out onto the grass f17-25 and ends **palm up** (the forearm rolled -90
  degrees, so the mark faces the sky); the hand rests at about (4.8, -137.1), up past his head. Cap pushed back 32 degrees; his head rolled
  toward the camera (north), eyes on the swarm, a determined face.
- **The light:** the mark glows as in S10-S12 while it's up, then blooms on "below" (f26). The toon paint takes only the
  light's brightness, so the coral colour is drawn in 2D (`diorama_ep03/post_bgqrs.py`): the zigzag on the wrist, a coral
  pool on the grass, dark grass blades in front of the core (it glows up THROUGH the grass), a soft beam and rays up
  into the swarm, a coral wash on the moths' bellies, and sparks. The 3D lights (a coral key at the mark and a broad
  shadowless glow above the wrist) only brighten what's near.
- **The swarm:** helper 6's `fluffmoth.swarm` (28 linked moths at 0.42, the shared meshes decimated to 12% for this
  shot: one moth was ~93k polygons). They circle a flattened ellipse round the light (none fly at the lens), 3.8-10
  units above it, following it down as he drops. Backs tilted to the light while it's above (back_to 0.7), nearly
  level once it's below, with a first wobble: **the flip is S14's**.
- **The shrimp:** on his left shoulder at **0.6** (E2.SHRIMP_IN_HAND, like helper 4's S01). It ducks flat with its eyes
  shut as he drops, rides down onto his chest below the shoulder (clear of his face), and peeks up at the swarm from f31.
  (Helper 3's S02 uses 0.42 on the shoulder: one of us should change; I'll follow the coordinator.)
- **Camera:** on 1s. f1: wide from the north, standing Kai and the swarm. To f18: it follows the drop down to his left
  side. To f57: a slow push-in. The glowing wrist ends at y ~780, his face just above it, his body off to the left, and
  the swarm above to the top of the frame. Gentle blur (3 px), the night haze well behind him.
- **Night:** helper 9's `N9.night(n)` and `N9.mark(k)` (in since 10:50; the stand-in grade only applies without them).
- **Render cost here** (on helper 9's night): ~4.5 min to build, ~55 s a frame at full size: 57 frames ~1 h.

### S13 render parts (every frame renders on 1s, so any range works; write your name and push before starting)
| Part | Frames | Who |
|---|---|---|
| 1 | f001-028 | bGqrs |
| 2 | f029-057 | bGqrs (one run, all 57 frames) |

- Render: `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S13 OUT --frames 29-57` (pull first). Raw
  part: libx264 crf 10 yuv420p 24 fps, CLEAN flags, `-start_number 29`, no 2D pass ->
  `parts/S13_f029-057.mp4`. I join, run the 2D pass (it needs `build/monsters/diorama_ep03/S13_mark.json`, which every
  render writes identically) and encode.

### Shared names for S14 (helper 10), S15 (helper 5), S16/S17 (XprL): pushed, import them
`from channels.monsters.diorama_ep03 import bgqrs as B`. These are measured on S13's final pose and move with
`B.S13_AT`.
- `B.KAI_LIE` = (9, -140, 0.65): his hips on the grass. `B.KAI_HEAD` = (5.9, -140, 0.9). `B.KAI_FEET` = (12.3, -140.2, 0).
- `B.HEAD_DIR` = (-1, 0, 0): his head points **west** (`B.S13_HEAD` = 90 compass).
- `B.FACING`: on his back, face up to the swarm, turned a little toward his left (north).
- **Sides:** `B.LEFT_SIDE` = (0, 1, 0). His left (the mark, the laid-out arm) faces **north**, toward the meadow.
  `B.RIGHT_SIDE` = (0, -1, 0). His right faces **south, toward the village** (the square is at (6, -170)). So Wren
  comes up from the village behind his right side and walks round his head or feet to kneel at his left (north).
- `B.WRIST` = (4.76, -137.1, 0.25): the left hand, palm up on the grass up past his head (11:00: moved so the glow
  rises beside his face, not through it). `B.MARK` = (5.3, -137.78, 0.47): the mark
  (= `H9._forearm(k, H9.MARK_U)`), the light below them.
- **Swarm:** `B.SWARM_CENTRE` = MARK + (0.4, -0.7, 0). `B.SWARM_HEIGHT` = (3.8, 10) above the mark. `B.SWARM_RADIUS` = 4.4
  east-west, x `B.SWARM_SQUASH` (0.38) north-south. 28 moths (`B.SWARM_N`) at `B.SWARM_SCALE` 0.42 (x 0.8-1.15).
- **The pose:** `B.lie_spec()` is the lying spec (LIE with the left arm out). Then `B._twist_for_palm_up(k)` (the
  forearm roll, -90) and `B._twist_face_to(k, B.FACE_TO)` (the head roll toward the swarm), as `B._kai_drop` does.
- **To continue the circles** (helper 10): `n13, beats = B.s13_beats()`; `B.swarm_layout()` gives each moth's dict(r, h,
  a0, w, s); `B.swarm_at(m, f, B.MARK)` and `B.swarm_heading(m, f)` give its position and heading at S13 frame f (S13's
  cut is f45). **These changed from my first version** (radius 1.4-4.4, height 3.8-10, 28 moths, a flattened orbit), so
  your `_swarm_layout` copy no longer matches.
- **Camera:** `B.camera_at(45, B.camera_poses(n13, beats))` gives (position, aim, lens, shift_y) at S13's cut. It now
  looks from the north, raised, with shift_y -0.055; the old `c_dir`/`_cam_from` maths no longer matches.
- **Light:** helper 9's `N9.mark(k)` is the key (keyed `MARK_W x level / 1.2`: ~2750 W while the wrist is up, a bloom to
  ~7000 W on "below", then ~5500 W). Plus my shadowless coral "under" light 1.6 above the mark (`B.S13_UNDER` 900 W) for
  the moths' bellies, and the 2D beam, rays, blades and zigzag from `post_bgqrs.py`.

Done: **S19top f089-176** for helper 3, a raw part pushed at 14:35 UTC (see the table).

Now: **S15 f037-070 for helper 5** (claimed in status/helper5.md 14:31 UTC; helper 5 renders f001-036, helper 2 f071-106). Rendering at 5d14f47 (helper5.py unchanged since c270955; the later helper9.py commits touch only S05/S18) as one raw part `parts/S15_f037-070.mp4` (crf 10, yuv420p, CLEAN, `-start_number 37`, no 2D pass). A container restart at ~14:42 stopped it after f040; resumed from f041 at 79ccb50 (no S15 code change since 5d14f47), done ~15:25 UTC. S14, S06 and S10 are already done; S18 isn't OK'd yet.

Next (the coordinator's ask, 14:40): helper 9's S05 is already rendered (f1-24 re-render, shot going up), so I took **S19bot f089-132 for helper 5** (claimed in status/helper5.md 14:50 UTC). It starts after S15, ~15:20 UTC: `S19bot_f111-132.mp4` first, then `S19bot_f089-110.mp4` (crf 10, yuv420p, CLEAN, `-start_number`).

## Coordinator
