**Superseded (owner, 31 Oct 2026: "Make episode 1 with 2.5 d so i can compare correctly"): see DIORAMA_EP01.md. D15 is now S15 and D16 is now S16 in the diorama registry.**

# Diorama 2.5D style test (owner, 31 Oct 2026)

The owner watched Episode 1 (3D) and said "Go for 2.5d". Asked which 2.5D, they chose **"Diorama 2.5D (game look)"**:
a tilted top-down toy world with tilt-shift blur, like their forest reference Short. They also chose **"Style test
first"**: one Episode 1 moment, 5-8 s, to compare side by side with the 3D version before deciding anything.

**The moment:** the snap, S15 + S16. Episode frames 802-980 (179 frames, 7.46 s at 24 fps). It uses the same audio as
the finished episode (out/monsters/ep01v2/mix.wav, 33.424-40.893 s), so the comparison is exact.

## The look: `channels/monsters/mk/diorama.py` (coordinator)
- `diorama.setup()`: render settings, warm low sun, lit grass, haze (mist pass) and bloom in the compositor.
- `diorama.camera(name, target, dist, tilt, yaw, lens, blur, frame)` builds the tilted toy camera.
  - Its f-stop is solved for tilt-shift blur, so don't set it by hand. Call `diorama.fstop_for()` again if you
    animate the distance.
  - Its haze starts just past the target.
- `diorama.island(seed=31)` builds the forest ring, the clearing and the pond at (0.1, -2.6). Every shot uses
  **seed 31**, so the sets match.
  - `diorama.blast_spots(isl["spots"], origin)` gives the trees in the snap's fan (toward +Y).
  - `diorama.stumps(spots, origin)` gives their hot-cut stumps.
- Look-dev still: `out/monsters/diorama/lookdev_v3_half.png` (tilt 62, dist 190, lens 100, blur 12).
  - Run it with `blender -b -y -P channels/monsters/diorama_look.py -- OUT.png --scale 0.5`.
  - It takes ~4 min, most of that building the 78 trees.

**Rules:**
- No HUD and no outlines on the set. Kai and the shrimp keep their toon look.
- Characters animate on 2s.
- Every camera move renders on 1s (`ones=(A, B)` in the builder's return, as S24top).
- Keep the action above y 960 and left of x 560 (the Shorts UI). Kai must read: at least ~110 px tall in the wides,
  bigger in the close beats.
- Pokémon-level clarity: one idea per beat, staging readable at phone size.

## Beats and owners (frames are 1-based within the test, 179 total)

| Beat | Frames | What happens | Camera | Who |
|---|---|---|---|---|
| D1 | 1-41 | Wide diorama of the clearing. Kai kneels at the pond reaching toward the shrimp. The shrimp blinks and looks up (~f13), then its claw rises out of the pond, dripping (f22-41, silence). | tilt ~60, dist ~200, slow push-in | helper 10 |
| D2 | 42-49 | The strike: the claw snaps shut (42-43). The 2 white flash frames (44-45) and the impact frames (46-49) go in the 2D composite (helper10.composite). | locked | helper 10 |
| D3 | 50-79 | The money shot. The blast fires a fan toward +Y (up the screen). A white shock ring races out, and the trees in the fan pop into dust (mk/erase.py) in order of distance, leaving glowing stumps and a scorched swath. | pulls up and back (dist ~200→300) to reveal the swath; shake on 2s | helper 10 |
| D4 | 80-93 | Kai is blown backward (toward -Y, down the screen), tumbles and lands on his back near the pond. | follows; still diorama | helper 10 |
| D5 | 94-115 | Kai on his back, dazed. The knocked-out stars come from the composite. His eyes close at 111-113. | closer, tilt ~70, dist ~110 | helper 10 |
| D6 | 116-179 | S16, "When I opened my eyes, it was on my chest." Near top-down over Kai on his back. The stumps glow and the dust settles. The shrimp sits on his chest and Kai's eyes open (blink). | tilt ~78, dist ~70-90, slow push-in | bGqrs |

- **D6's set** is the "after" state: `island(seed=31)` with the fan's trees removed and stumps placed.
- **Origin:** use the same blast origin as helper 10 (the shrimp's claw tip, read it from helper 10's builder once
  pushed), so the swath matches.

**Builders:**
- Code goes in `channels/monsters/diorama/helper10.py` and `bgqrs.py`, using `render_shot.py`'s builder interface:
  return `dict(frames, step, ones, subject)`. Register them so `render_shot.py -- diorama D15 OUT` and
  `-- diorama D16 OUT` work.
- Post OK stills to `out/monsters/diorama/okstills/` (0.5 scale) and message the coordinator **before** the full
  render.
- After the OK, the coordinator splits the frames across helpers (chunk rule in HELPERS.md).

**Coordinator after the render:**
- composite and join;
- mux the audio window;
- build a side-by-side comparison with the 3D frames 802-980;
- send both to the owner.
