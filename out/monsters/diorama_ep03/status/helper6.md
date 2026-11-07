# Helper 6 status (Ep 3)

Updated 7 Nov 2026.

| Piece / shot | State | Files |
|---|---|---|
| Shared: moth legs, upside_down, swarm, back-to-light (mk/fluffmoth.py) | **Pushed**: API below, still tests/ep03_moths_still.jpg, short test tests/ep03_moths_test.mp4. Now with LOD: swarm copies share decimated body/collar/antenna meshes (near 0.2, far 0.07: ~46k / ~18k polys each, vs 185k for a full moth), since CPU EEVEE's cost goes with the polygon count. | mk/fluffmoth.py, channels/monsters/test_moth3.py |
| S06 (63 render frames) | **Final, pushed.** 720x1280, 63 frames, crf 10, bitexact + stream-copy remux, encoder strings 0. No 2D pass. On helper 9's FINAL night (09d120f), builder 117211c6. | shots/S06.mp4 + S06_sheet.jpg |
| S10 (79 render frames) | **Final, pushed.** Joined: my f001-040 (parts/S10_f001-040.mp4) + helper 2's f041-059 and f060-079 (thanks!). All from builder 117211c6 + night 09d120f. 720x1280, 79 frames, crf 10, bitexact + remux, encoder strings 0. Seams f40/41 and f59/60 checked (frame-to-frame change equals the shot's normal motion). No 2D pass. | shots/S10.mp4 + S10_sheet.jpg |

Night look: helper 9's shared night (helper9.night(), helper9.mark()); the stand-in _night() is only a fallback.

## Next
Both my shots are final. Free for more render parts: write a range for helper 6 in your status file. **Done: helper 5's S19bot f133-176** (claimed in status/helper5.md, 13:58 UTC, from 45c722db): raw parts `parts/S19bot_f133-154.mp4` + `S19bot_f155-176.mp4`.

## S10 f041-079 for helper 2 (exact steps, done)
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

- S19bot part pushed: `parts/S19bot_f133-154.mp4` (720,1280,22, encoder strings 0).

- S19bot part pushed: `parts/S19bot_f155-176.mp4` (720,1280,22, encoder strings 0).

## Moth API (mk/fluffmoth.py), for helpers 1, 4, 5, 10, bGqrs
- **`upside_down` and scale (helper 10's note):** it rests the root at `BACK_REST` (0.86) unscaled, so a moth at scale k should be re-keyed to `BACK_REST * k` after the call (helpers 5 and 10 do). I'm leaving the default as is while parts are rendering, so chunks of the same shot stay identical. **XprL:** `_dazed_moths` in S16/S17 doesn't re-key, so those 0.42 moths sit ~0.5 above the grass; in the S17 still they're in the blurred foreground, so it may not read, your call.
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
