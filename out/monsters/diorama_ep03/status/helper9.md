# Helper 9: Episode 3 (night grade, mark light, lighthouse; S04, S05, S18)

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
