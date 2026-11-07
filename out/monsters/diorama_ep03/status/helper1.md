# Helper 1: Ep 3 (villagers at night, S03, S09)

## Status
- 7 Nov 09:15 UTC: started, at dce8b49. First the shared piece, villagers at night, in
  `channels/monsters/diorama_ep03/village.py`:
  - a lane of huts at character scale on the track into helper 9's Ep 2 village, north of its square. Each hut has
    a hinged door, a window with two hinged shutters, a porch, and a porch bell;
  - `slam_door`, `bang_shutters`, `ring_bell`;
  - the Ep 2 villagers with nets and bells, plus `back_off` (stepping backwards, net held out like a ward) and
    `scratcher` (one villager scratching a red blotch on the forearm, comic).
  - No lanterns. Until helper 9's night grade lands I use a temporary night look in my builder. I'll switch to
    helper 9's when it's in.
- Next: push a still of it, then S03 and S09 (S09 waits for helper 6's swarm).

- 7 Nov ~09:55 UTC: **villagers at night: pushed, still for OK** in
  `out/monsters/diorama_ep03/okstills/helper1_villagers_night_f30.jpg`. Left is the lane, wide; right is the
  scratcher's porch, close. Both are f30 of a test build `VN` (in helper1.py, not a shot).
  - **What's in the still:** the lane of six huts (the same cream walls and rust/brown roofs as helper 9's village)
    on the track into the square, with the bell tower and lake at the end. Each hut has a hinged door, a window
    with two shutters, a porch, and a porch bell. Here, porch bells are swinging and a door is mid-slam. One
    villager on a porch scratches a red blotch on a bare forearm (eyes squeezed shut, the hand rubbing on 2s).
    Others ring hand bells on porches, and one backs off with the net held out. Kai stands in the lane with the
    shrimp on his left shoulder. No lanterns.
  - **The night here is a stand-in:** a compositor multiply to dark blue, lifted in a soft circle round the mark.
    Helper 9's night grade and mark light replace it when they land.
  - **How to use it** (for S07 helper 5, S08 XprL, S17 XprL):
    - `from channels.monsters.diorama_ep03 import village as V`.
    - `V.lane()` builds the huts and is idempotent. Each hut dict has door, shutters, bell, porch, doorstep and
      window, and the module docstring lists the calls.
    - Then `V.slam_door(hut, f)`, `V.bang_shutters(hut, f)`, `V.ring_bell(hut, f0, f1)`, `V.villager(i, seed,
      net, bell)`, `V.back_off(...)`, `V.scratcher(v, f0, f1)` and `V.slip_inside(v, hut, f)`.
    - `V.LANE_AT` is Kai's spot in the lane.
- Next: S03 stills (the village backs away, doors slam, shutters bang, Kai alone). It's day, since dusk starts at S04.

- 7 Nov ~11:20 UTC: **S03 stills for OK**: `okstills/helper1_S03_f1_f30_f50.jpg` (f1, f30, f50 at half scale, with the
  2D pass). The shot is 67 render frames (timing.json).
  - **Light:** late-afternoon daylight. Dusk only starts at S04.
  - **Camera:** high 3/4 from up the lane, with the square, the bell tower and the lake behind Kai, on a slow crane
    up and back.
  - **f1:** the villagers are round Kai with their nets up, the shrimp on his shoulder and the mark on his raised
    wrist.
  - **The retreat:** they back off to the far huts (faces toward the camera) and slip in, and the doors slam and
    the shutters bang one after another (the near huts slam from inside). The last villager turns and runs off
    down the lane. By ~f32 every door is shut and by ~f47 the shutters.
  - **f40-55:** Kai alone in the empty lane, his arm dropping and his head down.
  - **2D pass** (`diorama_ep03/post_helper1.py`): helper 9's zigzag mark on his inner left forearm and Ep 2's three
    thin scratches beside it.
- S09 builder drafted (night, the bells ringing, the swarm streaming past the porch bell-ringers to Kai's wrist,
  using helper 6's `fluffmoth.swarm`, 40 moths). Test stills are rendering.

- 7 Nov 11:47 UTC: **S09 stills for OK**: `okstills/helper1_S09_f20_f40_f66.jpg` (half scale, with the 2D pass). The
  shot is 87 render frames. It uses **helper 9's `night()` + `mark()`** (the VN test now does too).
  - **Camera:** low, up the lane behind the nearest porch bell-ringer (foreground right, facing us 3/4, ringing
    hard), looking down the lane at Kai, with two more ringers on porches further down. A slow push-in.
  - **f1-25:** every bell rings: porch bells swinging on all six huts and the ringers' hand bells, with 2D ring arcs
    on 2s. Kai stands in his coral pool with the shrimp on his shoulder and his wrist up.
  - **From ~f25** ("The moths" lands at f36): the swarm (helper 6's `fluffmoth.swarm`, 40 moths, on 2s) comes in
    from behind and above the camera. It goes over the ringers and right past them without a flinch, then down the
    lane to his wrist. The first ones start circling it with their backs tilting to the light, as S10 continues.
    At f44 Kai's face goes wide and the shrimp ducks.
  - **Render plan:** about 3 min per frame with the swarm. 87 frames are about 4.5 h, in parts:
    `parts/S09_f001-030`, `_f031-060`, `_f061-087`, each under 2 h.
- **S03 full render starting now** (67 frames, about 1 h). I'll re-render if the coordinator wants changes.

- 7 Nov 12:05 UTC: **the coordinator's notes are done** (pushed):
  - **The scratcher:** the blotch is now a soft, rounded pink-red rash patch with a few small bumps (not a solid
    red block). The face is annoyed and scrunched: squeezed slanted eyes, brows pinched down in a V and a tight
    crooked mouth. The 2D pass adds comic itch squiggles. Still: `okstills/helper1_scratcher_v2_f30.jpg` (on
    helper 9's final night).
    - **For S07 (helper 5):** `sc = V.scratcher(v, f0, f1)` returns `sc["blotch"]`. Write its screen position as an
      anchor, then use `post_helper1.itch(anchors, "blotch")` from `channels/monsters/diorama_ep03/post_helper1.py`
      in your 2D pass.
  - **Night:** S09 and the VN test now use helper 9's FINAL `night()` / `mark()` (09d120f), and my stand-in is no
    longer used.
  - **S03:** OK'd. Full render running (55 frames + 12 tail = 67). Its 2D pass now puts the whole frame through
    helper 3's S02 grade (`post_helper3.late_afternoon`: greens -25% saturation, level -10%, peach highlights).
  - **For XprL (S08/S17), new in village.py:**
    - `V.porch(i) -> (loc, yaw, floor_z)`. Wren goes on hut 2, the nearest porch to Kai.
    - `V.bang_shutters(hut, f, crack=0.06)` leaves a crack, and `V.peek(hut, f0, f1, blinks)` puts glowing eyes in it.
- Next: S03 2D pass and push, then the S09 full render on helper 9's final night (in three parts).

- 7 Nov ~13:05 UTC: **S03 done and pushed**: `shots/S03.mp4` (67 frames: 55 + the 12-frame tail) + `S03_sheet.jpg`.
  720x1280, crf 10, tags 0, no black edges. Late-afternoon grade (helper 3's S02 grade), the mark, and Ep 2's
  scratches. About 50 s per frame.
- **S09 full render running now**, on helper 9's FINAL night (09d120f), as three render chunks (1-30, 31-60, 61-87)
  into one frame folder, then the 2D pass. About 4-5 h.

## Coordinator
(answers here)
