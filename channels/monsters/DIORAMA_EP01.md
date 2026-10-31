# Episode 1 in diorama 2.5D (owner, 31 Oct 2026: "Make episode 1 with 2.5 d so i can compare correctly")

Background: the owner watched the 3D Episode 1 and said "Go for 2.5d". Asked which look, they chose **Diorama 2.5D
(game look)**: a tilted top-down toy world with tilt-shift blur, like their forest reference Short. They first asked
for a short test, then for **the whole of Episode 1 in that look** to compare the two versions. It replaces the 7 s
test in DIORAMA_TEST.md: the D15/D16 work there becomes S15/S16 here.

**What stays exactly the same as the 3D Episode 1:**
- the script and voice;
- the music and SFX (out/monsters/ep01v2/mix.wav);
- the timing (channels/monsters/ep01v2/timing.json and TIMING.md: same shots, same frame counts, same render frames =
  frames + 12);
- the captions and the hook text (the assembler adds them);
- every story beat on the same frame as in your 3D shot, because the SFX are synced to those frames (snaps, flashes,
  stomps, taps, landings).

**What changes:** only the look and the staging, to the diorama:
- cameras, sets, lighting, tilt-shift and haze;
- shot framing redesigned for a high camera.

## The look: `channels/monsters/mk/diorama.py` (coordinator; pull it often, the API stays stable)
- `diorama.setup()`: call it first in every builder. It sets the warm low sun, the haze/mist compositor and bloom,
  and keeps render_shot's --scale.
- `diorama.camera(name, target, dist, tilt, yaw, lens, blur, frame)` builds the tilted toy camera.
  - The tilt-shift f-stop is solved from `blur` (full-res px). Re-solve it with `diorama.fstop_for(dist, lens, blur)`
    if you animate the distance.
  - The haze starts just past the target.
  - **tilt 40-80** (never eye level). **lens 70-120.** For close beats, use dist ~45-90 with the face turned up
    toward the lens, so expressions read.
- `diorama.island(seed=31)` builds the ONE other-world set. Every meadow and clearing shot uses it with **seed 31**:
  - the forest ring around the clearing;
  - the pond at MAP["pond"];
  - the meadow, the path and the landmarks in `diorama.MAP`.
- `diorama.blast_spots(...)` and `diorama.stumps(...)` give the "after the snap" state (S15 on).
- Look-dev still: out/monsters/diorama/lookdev_v3_half.png (tilt 62, dist 190, lens 100, blur 12).
- **The lab (S03a-S08):** a dollhouse cutaway room: floor, two walls with the rain window, the desk and the tank,
  seen from above at an angle, with the same tilt-shift and haze. Helper 1 builds it as `channels/monsters/mk/
  diorama_lab.py` (`room()` returns the tank, desk and window anchors) and pushes it FIRST. Helpers 2 and 9 use it.

## Rules (all shots)
- **Look:** no HUD. No ink outlines on sets. Kai and the creatures keep their toon look.
- **Timing:** characters on 2s. Camera moves render on 1s: `ones=(A, B)` in the builder's return. Locked cameras
  can go on 2s/3s.
- **Readability (Pokémon-level clarity at phone size):**
  - the action stays above y 960 and left of x 560;
  - Kai at least ~110 px tall in wides, bigger in close beats;
  - one idea per beat.
- **Code:** `channels/monsters/diorama/<you>.py` with `SHOTS = {"S01": ...}`, the same shot names as ep01v2. Add your
  module name to the list in `channels/monsters/diorama/shots.py`. Render with:
  `blender -b -y -P channels/monsters/render_shot.py -- diorama S01 OUT_DIR [--frames A-B] [--still N --scale 0.5]`.
- **Outputs:** `out/monsters/diorama/shots/<SHOT>.mp4` plus `<SHOT>_sheet.jpg`, render_frames long, near-lossless
  (crf 12 or less), no encoder tags (stream-copy clean as before).
- **Review:** OK stills (0.5 scale) go to out/monsters/diorama/okstills/<SHOT>_fN.jpg. Message the coordinator and
  wait for the OK before the full render.
- **Splitting a render:** the chunk rule in HELPERS.md applies.

## Who builds what (you know these beats from your 3D shot)

| Who | Shots | Note |
|---|---|---|
| helper 1 | S03a, S03b, S05b, plus `mk/diorama_lab.py` (push it first, ~30 min) | the lab dollhouse |
| helper 2 | S04, S05a, S07 | tank beats: look down into the tank (a toy aquarium) |
| helper 9 | S06, S08, S12 | S06/S08 in the lab; S12 the crawl to the pond on the island |
| helper 3 | S09, S13, S14 | S09: the sky crack, then down to the island; S13/S14 at the pond |
| helper 4 | S10a, S11a, then QA of everything | the jelly-snail and its burnt-hole trail |
| helper 6 | S10b, S11b | the fluffmoth |
| helper 10 | S15 (was D15) | the snap and the erased forest |
| bGqrs | S01, S16, S17, S18 (was D16) | S01 is the hook frame: big hook text at the top, so keep the action mid-frame |
| helper 5 | S19, S20, S21 | from bGqrs's 3D builders (bgqrs.py) |
| XprL | S22, S23, S24top, S24bot | the thorn tree, the butcher bird, the SAVE/RUN split |
| helper 8 | the assembler for the diorama cut | `assemble_ep01v2.py --shots out/monsters/diorama/shots --out out/monsters/diorama/picture.mp4`; S02 from the diorama S01; re-check CAP_Y per shot |
| helper 7 | sound | the same mix; check sync on the diorama cut and make a diorama-only cue fix only if a beat moved; the cover for the diorama version |

The coordinator reviews stills and shots, splits renders, then runs deliver and sends both versions to the owner.
