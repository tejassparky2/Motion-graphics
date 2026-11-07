# Helper 6 status (Ep 3)

Updated 7 Nov 2026.

| Piece / shot | State | Files |
|---|---|---|
| Shared: moth legs, upside_down, swarm, back-to-light (mk/fluffmoth.py) | **API pushed** (still: tests/ep03_moths_still.jpg, left = a 40-moth swarm orbiting a light with backs tilted to it + a level moth + one on its back; right = close on the one on its back). Short test video rendering next. | mk/fluffmoth.py, channels/monsters/test_moth3.py |
| S06 (swarm down the hillside, eye-spots blink open) | Next, after the shared piece. | diorama_ep03/helper6.py |
| S10 (top view, the spiral round Kai's raised left wrist) | Next. | diorama_ep03/helper6.py |

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
