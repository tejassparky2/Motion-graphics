# bGqrs status (Ep 3)

Updated 7 Nov 2026, 10:40 UTC.

| Shot | State | File |
|---|---|---|
| S13 "So I put the light below them." | **Building, OK stills next** (`diorama_ep03/bgqrs.py`, `s13`; 2D pass `post_bgqrs.py`). Stills at f1, f27 and f45 are rendering; they go to okstills/ with the 2D pass. | shots/S13.mp4 (pending) |

### S13 staging (57 render frames; "below" at f26)
- **Where:** the grass on the village's north edge, east of the track: his feet at **(12, -140)** at frame 1.
- **The drop (on 2s):** standing with the left wrist raised to the swarm (as S10 leaves him) -> a dip (f3) -> sits
  back (f8) -> flat on his back (f13, a small bounce) -> settled (f16). He lies **east-west, head to the west**, hips at
  (9, -140), LYING_V3's legs. The left arm goes out onto the grass f17-25 and ends **palm up** (the forearm rolled -90
  degrees, so the mark faces the sky); the hand rests at about (5.9, -136.6). Cap pushed back 32 degrees; his head rolled
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
- **Night:** a stand-in grade (compositor lift/gamma/gain to a dark moonlit blue) until helper 9's lands. `_night()`
  picks up `diorama_ep03/helper9.py`'s night()/night_grade() automatically.
- **Render cost here:** about 4.5 min to build and 2-2.5 min a frame at half size, so roughly 5 min a frame at full
  size. 57 frames on 1s is about 5 h on one container, so I'll split S13 into parts below.

### For helper 10 (S14 starts on S13's end): call these instead of copying numbers
`from channels.monsters.diorama_ep03 import bgqrs as B`
- `n13, beats = B.s13_beats()` (S13's cut is f45 = timing frames; its render frames run to 57).
- `B.swarm_layout()` gives each moth's dict(r, h, a0, w, s). `B.swarm_at(m, f, light)` is moth m's position at S13
  frame f round the light point (use f = 45 + your frame to continue the circles), and `B.swarm_heading(m, f)` its
  heading. The orbit is flattened (`SWARM_SQUASH`) and offset by `SWARM_SHIFT`. **I changed these from my first
  version** (radius 1.4-4.4, height 3.8-10, 28 moths): your `_swarm_layout` copy no longer matches.
- `B.camera_poses(n13, beats)` with `B.camera_at(45, poses)` gives (position, aim, lens, shift_y) at S13's cut. **The
  camera changed too** (now north of him, raised, shift_y -0.055); the old `c_dir`/`_cam_from` maths no longer matches.
- Light levels: `B.S13_LIGHT` (now 120) and `B.S13_UNDER` (900). The mark is at `H9._forearm(k, H9.MARK_U)` on the final pose.

After S13: render parts of the long shots (S14/S06/S10/S15/S18) from their owners' status files.

## Coordinator
