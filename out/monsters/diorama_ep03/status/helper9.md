# Helper 9: Episode 3 (night grade, mark light, lighthouse; S04, S05, S18)

**S18 parts: NOT YET from 207f050** (15:15 UTC). One more fix: at 207f050's framing Kai's body still hides Wren's kneel, so the camera has to move. Two framings are rendering; the commit line comes here in ~25 min (by ~15:40 UTC).

**night()/mark(): FINAL @ 09d120fd** (the coordinator's one change: ground, grass and foliage ~30 % darker and bluer; the mark's
coral pool and falloff unchanged). Check still (half res): `okstills/h9_night_village_final_half.png`. Use `N9.night(n)`
+ `N9.mark(k)` as in the API below; no more calibration rounds.

**S18 f082-107: CLAIMED by helper 2 (15:15 UTC)** (coordinator's 4-way split; replaces my old f073-107). Starts after my S17 part (~15:50 UTC), from your "S18 parts from <commit>" line if it's up by then, else from the coordinator's release 207f050 (or later with no S18 code change). Raw part `parts/S18_f082-107.mp4`, `-start_number 82`.

## Coordinator
(answers here)


## THE NIGHT API (pushed: channels/monsters/mk/night.py + diorama_ep03/helper9.py)
```python
from channels.monsters.diorama_ep03 import helper9 as N9
X._world(n)                 # or diorama.setup() + your set, as usual
N9.night(n)                 # night: navy sky, dark blue masses, the sun -> a cool moon (cel light/shadow kept, so faces
                            # read), dark-blue haze, and the grade. Call it any time after diorama.setup(): characters
                            # built later still get the mark's light (materials are re-tagged when the render starts).
lt = N9.mark(k)             # Kai's wrist mark = the coral KEY light: a point light on the inside of his LEFT forearm,
                            # parented to the forearm bone (follows every pose, no per-frame keys), no shadows,
                            # 6000 W. key=[(frame, watts), ...] for a flare or a dim. It gives the coral pool on the
                            # ground and warms his face, the shrimp and anyone close.
N9.dusk(n)                  # the dusk look instead (orange horizon, low warm sun, cooler tint)
lh = N9.lighthouse()        # the ruined lighthouse on its rocky point across the lake (default (120,-720)); lh["top"]
                            # is the lamp room's world position (aim cameras / pointing at it)
```
- **Use N9.mark(k) instead of your own coral light**: the grade only warms what a CORAL light reaches, and 6000 W with no
  shadows is calibrated for the coral pool. A stand-in coral light (e.g. 220 W) works but is far dimmer.
- Lights other than the mark: keep them cool or off at night (anything warm is read as mark light by the grade).
- Unlit (flat) materials just take the night tint; for a glow that must stay bright (eyes in the window cracks), give it
  a high emission strength (the bloom catches it).
- Interim still (half res, the night look + the lighthouse): `okstills/h9_night_interim.png`. Full-res night / dusk /
  lighthouse / wide stills are rendering, next push.

## Log
- 2026-11-07 15:00 UTC (**helper 6**): per the coordinator (14:56), **helper 6 takes S18 f001-036** (helper 1 didn't need S09
  help), so you're free for S04 and the join. I start as soon as the split line here names the commit; raw part
  `parts/S18_f001-036.mp4`, crf 6 yuv444p, clean, `-start_number 1`, unless you write another spec.
- 2026-11-07 14:55 UTC: re your split note: **S05 is already delivered** (`shots/S05.mp4`, pushed at c065ff2c), so
  nothing for bGqrs. **S18 split** (f001-036 me, f037-072 helper 10, f073-107 helper 2) goes here with the exact commit
  as soon as the kneel/rise/aim fix passes its check stills (rendering now, ~20 min). S04 full render: running.
- 2026-11-07 15:05 UTC: **S05 DELIVERED**: `shots/S05.mp4` (79 frames, 720x1280, 24 fps, no encoder strings) +
  `shots/S05_sheet.jpg`. The z-fight streaks are gone (f1-24 re-rendered with the clip fix; the rest is the approved
  look). **S18:** working on your note: Wren already starts in XprL's exact S17-end kneel (same spot, same bones: right
  knee on the grass, hips 2.35; checked against S17 f60), but Kai's body hid her legs, so she read as standing. Now:
  the camera shows the kneel, she whispers from it, rises up off the knee as she points, and the point is aimed (in
  screen space) at the tiny lighthouse behind her. New stills, then the full render.
- 2026-11-07 14:40 UTC: **S18 OK stills** in `okstills/`: `h9_S18_f026.png` (Wren leans in and whispers, hand cupped;
  Kai in the foreground over his shoulder, the shrimp on it, the mark glowing on his wrist), `h9_S18_f050.png` (on
  "left" she points across the dark lake; the ruined lighthouse's small coral glow sits on the far shore in the same
  direction) and `h9_S18_f080.png` (after the cut on "at": the lighthouse on its rocks, the coral lamp room, its
  reflection running to us, a small moon up-left; the glow swells on "lighthouse"). Camera A is now from the NNW over
  Kai's shoulder (from the ENE, Wren had her back to us and the point was hidden; NNE put a porch post in frame).
  **S18 full render starts when you OK this.** Render parts for helpers who are free: S18 f001-053 (the two-shot) /
  f054-107 (the lighthouse); tell me in "Coordinator" who takes which.
  **S05:** the first full render had flickering green streaks on the lake in f1-22 (the lake z-fighting the ground
  under it with the camera 470 m away). Fixed (camera clip start 0.05 -> 20; the S18 lighthouse camera got the same
  fix); f1-24 re-rendered (f9-12 match the old frames exactly). `shots/S05.mp4` goes up within the hour.
  **S04:** full render running (16/44).
- 2026-11-07 13:45 UTC: **OK stills for S04 and S05** are in `okstills/`: `h9_S04_f006.png` (day: S03's end, Kai alone in the lane facing
  us), `h9_S04_f022.png` (dusk on "down"), `h9_S04_f040.png` (night, the mark lights the lane coral), and `h9_S05_f060.png`
  (the dark island, the one coral dot with its bloom). The S04 sun disc is being moved into frame (it sat just off the
  right edge); a re-check is rendering. **S18:** the north-east two-shot camera was inside a lane hut (a flat grey
  frame); it's fixed (closer, wider lens) and re-rendering, along with the moon placed up-left of the lamp. S18 OK stills next.
- 2026-11-07 13:10 UTC: per the coordinator's notes: the lighthouse's lamp room has a hot near-white core, a stronger coral
  halo and the warm light on the broken stones; in S18 the moon is smaller and up-left of the lamp. S05 is darker
  (shot tint), and the 2D pass (`diorama_ep03/post_helper9.py`) adds the coral bloom on the village dot (S05) and on the
  lamp (S18, swelling on "lighthouse"). S04 is restaged: from up the lane looking south, Kai facing us, the sun
  sinking behind the far hills across the lake. S18's two-shot is now from the north-east so both faces read (3/4).
  **Full-res OK stills are rendering** (S04 f6/f22/f40, S05 f60, S18 f26/f50/f80).
- 2026-11-07 12:30 UTC: my shots are written in `diorama_ep03/helper9.py` (S04, S05, S18); test stills are rendering, then OK stills.
  - S04 (44 frames): Kai alone in the lane, side-on from the east (S03's spot and slump). The sun disc sinks behind the
    western treeline as the scene goes day -> dusk (on "down") -> night (`night.transition`). On "down" he lifts his
    wrist and the mark brightens (400 -> 6000 W). The shrimp turns to the glow.
  - S05 (79 frames): high and wide from the north, darker than the shared night; one coral dot (his mark) in the lane;
    a slow push-in toward it. No lighthouse in this shot (the wrist is "the only light for miles").
  - S18 (107 frames): XprL's S17 staging (Kai sitting, Wren kneeling at his village side). A two-shot from the east:
    she leans in to whisper (XprL's `wren.whisper`), on "left" turns and points across the lake (`wren.point` toward
    the lighthouse). On "at" (f53) a cut to the lighthouse across the dark water, its reflection running to camera and
    the moon beside it; the glow swells on "lighthouse".
- 2026-11-07 12:00 UTC: stills `okstills/h9_dusk_village.png` (dusk: a pink-orange horizon, a low warm sun, the mark's pool
  weaker) and `okstills/h9_night_wide.png` (high wide at night: the navy lake with ripples, the lighthouse's glow on the far
  shore, one coral dot at Kai). **The shared piece is done**, unless the coordinator wants changes. Next: my shots S04,
  S05, S18 (OK stills first).
- 2026-11-07 11:40 UTC: **The lighthouse is pushed** (per the coordinator's notes): `okstills/h9_lighthouse_night.png`. Rough stone
  blocks (a brick pattern with painted noise), a crumbled uneven top (broken wall stubs, gaps, fallen stones on the floor
  and down on the rocks), a small dark door and one slit window, moss at the foot, and in the lamp room a cracked coral
  lens, a coral light that warms the broken stone and a soft halo: the only warm thing in the frame. **The night lake**:
  navy-black with thin moonlit ripples, swapped in automatically by `night()` (helper 9's Ep 2 lake, also when it's
  built after `night()`). New in `mk/night.py`:
  - `night.reflection(src, toward)`: the lamp's long coral reflection on the water, broken dashes from below `src`
    toward `toward` (your camera's position).
  - `night.moon(az, el)`: a pale moon disc with a halo, at azimuth `az` (0 = north, 90 = east) and elevation `el`,
    the moonlight turned to come from it (call after `night()`).
  - `lh = night.lighthouse()` (or `N9.lighthouse()`): `lh["top"]` is the lamp room, `lh["halo"]` the glow ball.
- 2026-11-07 10:50 UTC: **night() + mark() updated and pushed: switch now.** Still: `okstills/h9_night_village.png` (full res).
  Per the coordinator's notes: the pool is the mark's coral (#ff8466), with a steeper falloff (bright at his wrist,
  dark a few units out); the night masses are a little darker; the mark now has a small hot coral core that blooms.
  Next: the lighthouse (stone blocks, crumbled top and fallen stones, door, slit window, moss, the glow + halo), the
  night lake (navy-black, moonlit ripples, the lamp's coral reflection) and a moon. Then S04/S05/S18.
- 2026-11-07 09:50 UTC: started. **Shared piece in progress: `channels/monsters/mk/night.py`** (WIP, pushed; the API may still
  change a little until the stills are approved):
  - `night.apply("night" | "dusk" | "day")` after your scene is built: the sun becomes a cool moon (same cel bands, so
    faces keep their light and shadow), the sky/fill/haze go to night or dusk, and a compositor grade tints the frame.
  - `night.mark_light(k)`: Kai's wrist mark as a coral point light, parented to his left forearm bone (it follows
    every pose), no shadows. Its light comes back warm through the grade: every cel material writes its light to an
    AOV, and the coral part of it (the moon and the fill are blue, so they drop out) lights the frame.
  - `night.transition(f0, f1, "day", "dusk", "night", f2)`: a keyed sunset (S04).
  - `night.lighthouse()`: the ruined lighthouse on a rocky point across the lake, at (120, -720) by default, with a broken
    top ring of posts, a coral lens and a coral light warming the broken stone.
  - Full-res stills of night / dusk / lighthouse / high wide are rendering now; they go to okstills/ next.
- Timing is in: S04 44 render frames, S05 79, S18 107.
