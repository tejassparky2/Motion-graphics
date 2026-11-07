# Helper 6 status (Ep 3)

Updated 7 Nov 2026.

| Piece / shot | State | Files |
|---|---|---|
| Shared: moth legs, upside_down, swarm, back-to-light (mk/fluffmoth.py) | **Pushed**: API below, still tests/ep03_moths_still.jpg, short test tests/ep03_moths_test.mp4. Now with LOD: swarm copies share decimated body/collar/antenna meshes (near 0.2, far 0.07: ~46k / ~18k polys each, vs 185k for a full moth), since CPU EEVEE's cost goes with the polygon count. | mk/fluffmoth.py, channels/monsters/test_moth3.py |
| S06 (63 render frames) | **OK stills, please check**: okstills/S06_f22_f44.jpg. A (f1-33): low by Kai's spot looking up the rise (helper 1's Ep 2 hill), ~56 moths pour over the crest and down toward us. Cut on "down" (f34) to close on one moth, high in frame (clear of the caption band); its four eye-spots are shut at the cut and blink OPEN with a glow on "the hill" (f39-45), the swarm streaming behind. ~35 s/frame at 0.35 scale. | diorama_ep03/helper6.py |
| S10 (79 render frames) | **OK still, please check**: okstills/S10_f40.jpg. High over Kai's shoulder (tilt 68): his left wrist straight up over his head, the mark a glowing coral core; 42 moths in 4 rings round him (inner faster), each banked with its back leaning in to the light (S10_TILT 0.5); the shrimp on his shoulder squashes down (ducks) when a moth swings close. ~80 s/frame at 0.35 scale. | diorama_ep03/helper6.py |

Night look: a stand-in (navy world, cool moon, a navy multiply, the mark as a coral point light without shadows) until
helper 9's night grade + mark light land; the builder switches to helper9.night() / mark_light() automatically
when they exist.

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
