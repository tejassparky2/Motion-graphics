# Helper 9: Episode 3 (night grade, mark light, lighthouse; S04, S05, S18)

## Coordinator
(answers here)

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
