# Episode 1 v3, 2.5D diorama, max quality (owner, 31 Oct 2026)

**What the owner said:**
- The v3 script is approved ("OK go ahead"): out/monsters/story_v3_diorama.md.
- "Go for 2.5d just try to improve it more ... improve overall animation quality and clear explanation."
- "you said 2.5 has large room to improve go improve it to max as it can you can use any free to use or opensouce
  things".

**What v3 must do (the owner's notes on v2):**
1. Kai's death is told step by step: the panicked shrimp's snap cracks the tank, the water pours into the power
   cables, he's standing in it, "That's how I died." Then "Then I woke up. In another world."
2. The shrimp tries to kill Kai: it looks right at him and aims, the blast fires straight down his line, "It missed me
   by an inch.", "It tried to finish me anyway."
3. The shrimp is in danger at the end: the bird is looking at it, and it has no idea.
4. The A/B vote: "Option A: save ... Option B: run ... Comment A or B." A big A and B pop on the split screen.

**Same as v2:** the voice (Turbo am_liam), the diorama look and world (mk/diorama.py, the seed-31 island, the
dollhouse lab), the characters, the hook text, the captions, and every story beat on its line.

## Files
- **Script and timing:** `channels/monsters/ep01v3/episode.py` and `channels/monsters/ep01v3/timing.json` /
  `TIMING.md`. Every shot's frames and render_frames (= frames + 12) come from there. Never use v2's counts for a
  v3 shot.
- **Builders:** `channels/monsters/diorama_v3/<you>.py`, registered in `channels/monsters/diorama_v3/shots.py`.
  Reuse your diorama/ builder and change only what v3 needs: the frame count, staging, acting.
- **Render:**
  `blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08a OUT [--frames A-B] [--still N --scale 0.5]`.
- **Outputs:** `out/monsters/diorama_v3/shots/<SHOT>.mp4` + `<SHOT>_sheet.jpg` (crf 10, the bitexact flags, then a
  stream-copy remux; no Lavf/Lavc/x264 strings). OK stills go to `out/monsters/diorama_v3/okstills/`; message the
  coordinator before the full render.
- **Splits:** parts go to `out/monsters/diorama_v3/parts/<SHOT>_fAAA-BBB.mp4`, and the coordinator joins them with
  `channels/monsters/diorama/join_parts.py`. The chunk rule (HELPERS.md) applies.
- **Shots whose v3 frame count equals v2 and whose picture doesn't change** are copied from out/monsters/diorama/shots
  by the coordinator.

## Quality bar ("max")
- **Acting:**
  - Every move has a clear key pose, anticipation before it and overshoot after it, on 2s.
  - Kai blinks every 2-4 s and his eyes move.
  - The face matches the line: VRM expressions (surprised, fear, angry, joy, neutral) plus the 2D comic marks.
  - No stiff poses. Lying Kai always reads as lying: a bent knee, an arm flung over his head, grass round him.
- **Readability at phone size:** the subject of the line is the biggest thing in frame, above y 960 and left of x 560
  (the Shorts UI), and clear of the caption band (845-930) unless the caption is moved.
- **Camera:** a slow move on 1s in every shot (a push-in or a drift). Emotional beats use closer, lower diorama
  cameras (tilt 40-55, dist 25-45); geography beats use the toy-world wide.
- **Light and colour:** the shared diorama.setup(), plus the per-scene grade (cool night lab, warm day island). The
  lighting pass (Q3) upgrades setup() for everyone.
- **Effects:** impact frames, speed lines, sparks, electric arcs and glows done properly in 2D (fx2d / comp), timed
  to the sound.
- **Free/open-source only:**
  - CC0 assets (Poly Haven, ambientCG, OpenGameArt CC0) or our own procedural ones. Credit anything that asks for it.
  - Open-source tools (Blender, ffmpeg, Real-ESRGAN, etc.).
  - No pirated or paid assets, and nothing that imitates a known franchise.

## Shots: what changes and who does it
| Shot | Line | v3 picture | Who |
|---|---|---|---|
| S06 | Then the storm hit. | + in the tank, the shrimp jolts awake at the flash | helper 9 |
| S07 | The shrimp panicked. Its snap cracked the tank. | Close in the tank: the startled shrimp jumps, snaps (flash), a crack zigzags across the glass, a jet of water spits out | helper 2 |
| S08 | Water poured off the desk, straight into the power cables. | Follow the water (camera on 1s): a waterfall off the desk edge, spreading over the tiles to the power strip under the desk; the plugs fizz with sparks | helper 9 |
| S08a | And I was standing in it. | Close on Kai's sneakers as the puddle slides under them; he looks down, his face drops (fear) | helper 1 |
| S08b | That's how I died. | A blue spark runs from the strip through the water and up into him: electric arcs, an x-ray skeleton flash (2D), the lights die, black (the flatline is in the sound) | helper 4 (+ the 2D FX library, Q5) |
| S09 | Then I woke up. In another world. | Black; a crack of light opens in a sky; a glowing spark (his soul) falls through it into the pink-flower meadow; Kai's eyes snap open, he stares at his hands; tilt up to the cracked sky | helper 3 |
| S15a | Then it looked right at me. | Close, low: the shrimp lifts its head, its eyes narrow (brow), and the dripping claw rises and swings to aim at his face (claw big in the foreground, Kai behind) | helper 10 |
| S15 | (the snap) | It fires straight at Kai: flash, impact frames; he's thrown back, and the fan of trees right behind where he knelt pops into dust, glowing stumps | helper 10 (renders split) |
| S15b | It missed me by an inch. | Kai on his back, dazed (stars), a smoking stump an inch from his head | bGqrs |
| S16-S19 | (same lines) | The new lying pose plus acting (blinks, terror, the drop), re-rendered | bGqrs (S16-S18), helper 5 (S19) |
| S20 | It tried to finish me anyway. | The claw winds up at his nose, snaps: only a puff; the shrimp startles and stares at its dry claw; Kai's deadpan dot eyes | helper 5 |
| S21 | Then it stomped back to the puddle. | A smug strut back to the puddle, then the claw dips in | helper 5 |
| S23b | And it was looking at the shrimp. | Close on the bird's eye and a head tilt; cut to its view: the tiny shrimp at the puddle, its back turned | XprL |
| S23c | The shrimp had no idea. | The bird's shadow slides over the shrimp, which keeps drinking | helper 6 |
| S24 | Option A: save... Option B: run... Comment A or B. | Split screen: top A, Kai reaching for the shrimp under the shadow; bottom B, Kai running, the bird diving. The big A/B letters are added by the assembler | XprL (top), helper 1 (bottom) |
| S01 | Don't move... | the new lying pose, re-rendered (the hook frame) | bGqrs |

## The quality passes (run alongside the shots, then everyone adopts them)
| Pass | Who | Deliverable |
|---|---|---|
| Q1 Acting library | bGqrs | `mk/acting.py`: blink(), look_at() with eye darts, expression(rig, name, f0, f1), overshoot/anticipation easing, Kai's LYING_V3 pose. The shrimp gets glare(), hop() and strut(); the bird gets tilt() and lock_on(). Push it first, ~45 min, and message everyone. |
| Q2 Set dressing | helper 6, then S23c | A richer island and lab: mushrooms, clover patches, pebble paths, flower clusters, small props, all CC0 or procedural, in the same MAP. A before/after still. |
| Q3 Light and grade | helper 9 (after S06/S08) | diorama.setup() v2: AgX look, AO/contact shadows, soft warm key and cool fill, a rim light on characters, and the per-scene grade. Show three before/after stills, then push. |
| Q4 Upscale test | helper 4 (after S08b) | Real-ESRGAN anime (open source, weights from Hugging Face) 720x1280 to 1080x1920, against our lanczos: crispness and time per frame on 3 shots. Adopt it at delivery only if it is clearly better. |
| Q5 2D FX library | helper 10 + helper 7 | fx2d: electric arcs, the x-ray skeleton flash, a soul spark with a trail, better impact frames, speed lines, and A/B letter cards with a pop. |
| Sound v3 | helper 7 | ep01v3 mix: the old cues retimed, plus the tank crack, water pour, plug fizz, zap, flatline beep, soul chime, the bird's lock-on sting, the shadow whoosh and A/B stingers. loudnorm -14 LUFS, then Whisper. |
| Assembly v3 | helper 8 | assemble_ep01v2.py `--version diorama_v3` with the ep01v3 timing; the new shot names; the A/B letters (A pops on "Option A", B on "Option B", both on "Comment A or B"); captions placed per shot. |
| QA | helper 4 | Every shot against this brief and story_v3_diorama.md. |
