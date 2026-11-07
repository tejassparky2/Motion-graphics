# Helper 6 status (Ep 3)

Updated 7 Nov 2026.

| Piece / shot | State | Files |
|---|---|---|
| Shared: moth legs, upside_down, swarm, back-to-light (mk/fluffmoth.py) | **Pushed**: API below, still tests/ep03_moths_still.jpg, short test tests/ep03_moths_test.mp4. Now with LOD: swarm copies share decimated body/collar/antenna meshes (near 0.2, far 0.07: ~46k / ~18k polys each, vs 185k for a full moth), since CPU EEVEE's cost goes with the polygon count. | mk/fluffmoth.py, channels/monsters/test_moth3.py |
| S06 (63 render frames) | **Full render running** with helper 9's night (mk/night.py via helper9.night()) and a coral mark light at Kai's spot behind the camera (night.mark_light's settings). The close moth's eye-spot glow is brighter (x3.6). New stills: okstills/S06_f22_f44.jpg. Then the final encode (no 2D pass). | diorama_ep03/helper6.py |
| S10 (79 render frames) | **Split.** helper 9's night + helper 9's mark light on his forearm (9000 W: the wrist is high over his head) and a glowing core: a coral pool round him, the moths warm on the side facing the wrist. New still: okstills/S10_f40.jpg. I render **f001-040** after S06. **helper 2: please take f041-079** (steps below). I join and encode shots/S10.mp4 (no 2D pass). | diorama_ep03/helper6.py |

Night look: helper 9's shared night (helper9.night(), helper9.mark()); the stand-in _night() is only a fallback.

## S10 f041-079 for helper 2 (exact steps)
- Pull first (the builder is `channels/monsters/diorama_ep03/helper6.py`, `s10`; mk/fluffmoth.py at this commit or
  later). S10 returns `ones=(1, 79)`: every frame renders on 1s, so start exactly at f041.
- Render: `/home/user/tools/blender-4.5.15-linux-x64/blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S10 OUT --frames 41-79`
  (env vars S10_MOTHS unset: 42 moths).
- Encode a RAW part (near-lossless, no tags), 39 frames:
  ```
  ffmpeg -framerate 24 -start_number 41 -i OUT/%04d.png -frames:v 39 -c:v libx264 -crf 6 -pix_fmt yuv444p \
     -map_metadata -1 -fflags +bitexact -flags:v +bitexact -bsf:v filter_units=remove_types=6 /tmp/part.mp4
  ffmpeg -i /tmp/part.mp4 -c copy -map_metadata -1 -map_chapters -1 -fflags +bitexact -flags:v +bitexact \
     -metadata:s:v handler_name= out/monsters/diorama_ep03/parts/S10_f041-079.mp4
  ```
  `grep -a -c -E "Lavf|Lavc|x264"` on the part must print 0. Push it and note it in your status file.

## Moth API (mk/fluffmoth.py), for helpers 1, 4, 5, 10, bGqrs
- `build(loc, name)` now also returns `legs` (6 hip pivots, folded away by default: older shots look the same).
- `flight_mode(rig)`: the root becomes the body centre (hover 0), no ground shadow, legs folded. Animate
  `rig["root"].location`; rotation with:
  - `back_to(rig, f, light, heading, amount=1.0, prev=None)`: its BACK (body top, wings' upper side) toward the point
    `light` while it heads along `heading`; amount 0 = level, 1 = back square to the light (S10-S14). Returns the
    euler; pass it back as `prev` so angles stay continuous.
  - `face(rig, f, heading, bank=0.0, prev=None)`: level flight, optional bank.
- `flap(rig, phase=0, amp=1.0, fold=0.0)`: endless wing beats (one 4-frame beat + a CYCLES modifier: free for swarms).
- `show_legs(rig, f, on)`; `upside_down(rig, f0, f1, land_at=None)`: on its back from f0 (rolled over, resting on the
  ground at land_at, wings splayed, legs out and waving on 2s, eye-spots dazed/half shut, a wriggle now and then).
  The tumble from the air into this pose is the shot's job (S14): key the roll/drop before f0.
- `swarm(n, place, name, seed, far)`: ONE moth built, n-1 linked copies (shared meshes/materials), all in flight_mode
  with their own wing beat. `place(i, rnd) -> (location, scale)`; `far(i, loc, scale) -> True` drops small details on
  far moths. Returns a list of rigs (same dict keys). Cost on this CPU: 40 moths + 3 full moths at 0.4 scale ~2.7
  min/frame (memory ~2.2 GB); a single moth close ~50 s at 0.5 scale.
- Test scene: `blender -b -y -P channels/monsters/test_moth3.py -- OUT --still 12 --scale 0.4 [--noswarm --close]`.

## Coordinator
(answers here)
