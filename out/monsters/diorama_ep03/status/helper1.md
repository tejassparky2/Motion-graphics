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

- 7 Nov ~11:00 UTC: **villagers at night: pushed, still for OK** in
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

- 7 Nov ~13:30 UTC: **S03 stills for OK**: `okstills/helper1_S03_f1_f30_f50.jpg` (f1, f30, f50 at half scale, with the
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

## Coordinator
(answers here)
