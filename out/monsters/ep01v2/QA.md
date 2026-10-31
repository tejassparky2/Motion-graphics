# Episode 1 v2: QA review (helper 4)

An independent read of every delivered shot in `out/monsters/ep01v2/shots/`. Each shot is judged against:
- its row in `channels/monsters/EP01V2_SHOTS.md` and its rule IDs, using the full rule text in
  `reports/Pokémon episodes story and animation.md`;
- the frame-by-frame targets in `channels/monsters/HELPERS.md`;
- the exact lengths in `channels/monsters/ep01v2/TIMING.md`.

The checks:
- **Measured on every frame:** frame count (render frames = cut + 12) and mean HSV saturation (target 0.34-0.61,
  LC9). Also black frames, and runs of identical frames, which show whether a shot really holds on 3s or 2s.
- **Looked at:** the contact sheet, plus at least 6 full frames (the first, the last, the voice in and out, the
  biggest changes), viewed at full size and at 360 px wide (TP16).

**v8 check (coordinator, 30 Oct):** until `mk/sdf.py` 3b0fc70, every SDF-built mesh faced inward, so SDF bodies
had no inverted-hull outline and inverted toon light. An SDF creature without its coloured line is a FIX.

**v8b check (coordinator, 30 Oct):** until `mk/puffshrimp.py` 1d22a94, the claw hinge and lid pivots sat at twice
their offset. In every puff-shrimp shot the snapping finger must stay attached to the claw and the lids must close
over the eyes. A shrimp shot rendered before 1d22a94 (or, for outlines, before 3b0fc70) is a FIX.

**Since tonight's fixes, the key checks (coordinator, 30 Oct):**
- SDF creatures have outlines and a lit side (from 0c0ceeb).
- The shrimp's snapping finger stays attached.
- The shrimp has its locked-on eyes in S01, S16, S19 and S20.

## Known minor issues (revisit after Episode 1)
- **Outline slivers (look.outline, shared).** Since the SDF normal fix, short dark slivers show inside SDF bodies
  at full size, where the inverted-hull shell pokes through creases. They are not shadow acne and not mesh noise.
  Barely visible at 360 px. The coordinator decided to leave look.outline alone for this episode (seen on the
  jelly-snail in S10a).

**Verdicts:** PASS (ready for the cut), FIX (a concrete change, sent to the builder), or NOTE (weak but acceptable).
Most serious first within each shot. Updated as shots land.

## Summary

| Shot | Builder | Verdict | Frames (got / want) | Mean sat. | Notes |
|---|---|---|---|---|---|
| S02 | assembler (helper 8), from S01 | PASS (picture.mp4 2a8c1f7) | 49 in the cut | - | the glitch rewind reads; captions clear; 1 NOTE (the white ends as bright as the strike) |
| S03b | helper 1 | PASS (v3, 93da447) | 51 / 51 | 0.24 | warm skin, cyan on the lit side; 1 NOTE (saturation, a hard split down the face) |
| S09 | helper 3 | PASS (v2, 6d95527) | 66 / 66 | 0.47 | v1 FIX resolved: eyes open on "woke up", crack held through "cracked sky" |
| S06 | helper 9 | PASS (v2, bb8f476) | 41 / 41 | 0.37 | the bolt on frame 14, the stutter on 2s, the black opaque |
| S10a | helper 4 | PASS (coordinator's second read of v2) | 56 / 56 | 0.38 | outline and lit side; known minor issue: outline slivers |
| S10b | helper 6 | PASS (v2, 7dcec9b) | 35 / 35 | 0.46 | outline back; reframed, so the wings stay in frame |
| S11a | helper 4 | PASS (v3, 4898f09; the coordinator's read) | 39 / 39 | 0.52 | pale smoke rises off the holes; the shell and eyes are clear |
| S11b | helper 6 | PASS (v2, 285c3f1) | 38 / 38 | 0.49 | outline back; brighter eye-spot glow |
| S01 | bGqrs | PASS (v2, c8a0958) | 69 / 69 | 0.46 | the terror-eye sliver is fixed; 1 NOTE (chin at the caption line) |
| S04 | helper 2 | PASS | 73 / 73 | 0.31 | claw held open, shuts, white-hot on "boils"; 1 NOTE |
| S18 | bGqrs (helper 5 render) | PASS (v2, b172892) | 60 / 60 | 0.38 | a 2D snap-zoom into the eyes on "wet" (resolves the NOTE) |
| S19 | bGqrs | PASS (v2, b0aa7eb) | 105 / 105 | 0.49 | the last drop dries by frame 90 and stays gone; 1 NOTE (shrimp's eyes not in frame) |
| S08 | helper 9 | PASS | 85 / 85 | 0.23* | water to the strip, spark on frame 55 after "Me.", then black; *black frames pull the mean down |
| S12 | helper 9 | PASS (v2, 055a865) | 47 / 47 | 0.55 | restaged close and low: a tired panting face, a glint at the puddle ahead |
| S15 | helper 10 | PASS (v3, 318b92d) | 127 / 127 | 0.50 | the full nine-step hit, every step inside the report's ranges |
| S05b | helper 1 (frames 40-51 by helper 6) | PASS | 51 / 51 | 0.32 | the flash fades on his face; he taps the glass (BD2) |
| S03a | helper 1 | PASS | 53 / 53 | 0.33 | the night lab, rain, the glowing tank; cuts with S03b |
| S13 | helper 9 | PASS | 62 / 62 | 0.52 | the claw dipped in the puddle (the clue, CH3) |
| S20 | bGqrs (coordinator render) | PASS | 103 / 103 | 0.45 | the pff, the stare, the head tilt, Kai's deadpan held 2 s |
| S14 | helper 9 (helper 5 render) | PASS (caption placement, picture.mp4 3ad5173) | 80 / 80 | 0.33 | "Impossible." sits above the cap; the mouth is clear |
| S16 | bGqrs | PASS | 76 / 76 | 0.40 | eyes open on "eyes", then S01's framing (SU9 rhyme) |
| S24bot | XprL (coordinator restage) | PASS (v2, 957f393) | 97 / 97 | 0.46 | Kai at x 90-345, clear of the rail; the bird drops on the shrimp and mantles |
| S07 | helper 2 | PASS (v2, d978975) | 36 / 36 | 0.29 | re-aimed: the shrimp mid-frame; the hit and the crack land |
| S05a | helper 2 | PASS | 75 / 75 | 0.30 | the bubble peaks, then collapses to micro-bubbles on "sun" |
| S17 | bGqrs | PASS | 47 / 47 | 0.51 | a drop falls on "drops." and splats on the jacket (CH3, second showing) |
| S24top | XprL | PASS (v1); v2 re-delivery pending (bGqrs's frames 67-97 fix, ~02:05) | 97 / 97 | 0.53 | the SAVE plate; split-ready |
| S21 | bGqrs (coordinator render) | PASS (v2, e9c0f7c) | 64 / 64 | 0.49 | the stomp seen from Kai's feet; the finger stays on |
| S22 | helper 5 | PASS | 57 / 57 | 0.44 | 1 NOTE (the shells read as beans) |
| S23 | helper 5 | PASS | 82 / 82 | 0.63 | 1 NOTE (saturation just over the band) |

Waiting for: S24top v2 (XprL, ~02:05).

## S03b: Kai's face lit cyan by the tank, a fond smile (helper 1)
**v2 (9ff69f6): PASS**, with one NOTE.
- **Fixed:** the tank light is now cyan from one side, so the left of the face falls into a hard, designed cool
  shadow tone. The shirt reads dark slate again (the earth outfit). The smile lands in two steps: the eyes soften
  around frame 19, then the closed-eye `happy` smile at about frame 22 (SG2).
- **NOTE:** mean saturation is 0.28. That is under the 0.34-0.61 band but inside E22's measured 0.26-0.69, and it
  suits a pale face in a dark lab. Not blocking. S03a and S05b come from the same rig, so check they cut with it.

**v1: FIX** (sent to helper 1, 30 Oct).
1. **Most serious: the tank light washes the frame out instead of lighting it cyan (row: "lit cyan by the tank";
   LC9, LC1).**
   - Mean saturation is 0.23, below the 0.34-0.61 band and below even E22's measured minimum of 0.26. S06, the same
     night lab, measures 0.37.
   - The skin reads near-white and flat, with no designed shadow tone, and the light on it is white, not cyan.
   - Fix: lower the tank light's energy and give it a saturated cyan (about #4fd8e8). Let one side of the face fall
     into the cool shadow tone.
2. **The shirt reads as the world outfit's teal top (continuity: Earth = "earth" outfit, EP01V2_SHOTS.md "The
   hero").**
   - The code loads `outfit="earth"`. The wear_earth texture is dark blue-grey, but the overexposure bleaches it to
     pale cyan with white trim, which at a glance is the new world's teal tunic.
   - Fix: the lighting fix above should bring back the charcoal. Check that the shirt reads dark grey next to S03a.
- **NOTE:** the "small fond smile" barely shows; the mouth is a faint line. The face change lands through the eyes
  (wide on frame 1, soft half-lidded from about frame 24: SG2 met). A touch of the `happy` mouth shape would make
  it read at 360 px.
- **Passes:** the length (51 frames, exactly what TIMING.md asks), the cap and K, the amber eyes, and the locked
  close framing above the captions (SG4). No text in the frame.

## S09: white bloom, cracked sky, tilt down to Kai (helper 3)
**v2 (6d95527): PASS.** The structure is reversed from the shot list, which suits the words better:
- The white blooms onto Kai's sleeping face (frames 4-16), and his eyes open on "woke up". He goes from closed
  eyes, to a shocked pinprick stare at about frame 20 (SG2), to a squint.
- A fast tilt up (frames 25-30) lands on the crack, which holds centred from about frame 31 to the end of the cut,
  so it is on screen for "cracked sky" (frames 31-44). There is no full-frame blur.
- 66 frames, saturation 0.47. Kai is on-model.
- The crack's continuity with S07 and S08 is to be checked when they land.

**v1: FIX** (sent to helper 3, 30 Oct). The shot was built to the old 2.3 s estimate. v7's TIMING.md gives it **54
frames in the cut** (66 to render), and the picture no longer lands on the words.
1. **Most serious: the crack is off screen on "cracked sky" (SG10, EP4 continuity; timing.json l9).**
   - The words: "cracked" at 1.26-1.40 s (frames 31-34) and "sky." at 1.40-1.82 s (frames 34-44).
   - The picture: the crack leaves the frame around frame 31. From frame 36 to 48 the camera is tilting through
     defocused pink grass, so nothing reads at all.
   - Fix: keep the crack in frame until about frame 40 (hold it through "cracked" and most of "sky"), then tilt.
2. **Kai's wake-up falls after the cut (TIMING.md v7).**
   - The cut ends at frame 54, but Kai is first sharp at about frame 50, and the blink beat (frames 48-67) sits
     mostly in the trimmed handle.
   - Fix: land the tilt on Kai by about frame 48, so frames 48-54 show his eyes opening (one face change, SG2). The
     rest of the blink can live in the handle.
3. **About 0.5 s of full-frame blur during the tilt (frames 36-48; TP16, readable at 360 px).**
   - The near pink grass sweeps right past the lens at f/0.15, so the frame turns to mush.
   - Fix: stop the aperture down while the camera moves (for example key the f-stop 0.15 → 1.5 → 0.15 around the
     tilt), or raise the camera's path so the nearest grass stays out of the frame.
- **Passes:**
  - Kai is on-model against `hero_v2_outfit.png`: white cap with a teal visor and the teal K, amber eyes, teal top
    with white trim and zip.
  - The crack reads at 360 px.
  - The bloom from white works (SG12: white bloom for the crossing).
  - Saturation is 0.44, and the white opening is low as expected.
  - Continuity: the crack comes from `pistolshrimp.crack_path()`, the tank crack's path. To be confirmed against
    S07 and S08 when they land.

## S06: the storm hits the lab window (helper 9)
**PASS.**
- **Length and level:** 48 frames (41 needed). Saturation 0.37. The lab is cold blue (LC1), and fear shows as
  darkness, not a hue shift (LC2).
- **Lightning:** a double flash on frames 8 and 10 that decays by frame 13. Frame 8 is exactly the voice-in, "Then
  the storm hit."
- **Lights:** the room cuts out in 2-frame pairs from frame 16 to 28 (action on 2s, IM2). Rain on the glass runs on
  1s throughout.
- **Picture:** no people, no text. Locked camera (SG4).

## S10b: the fluffmoth hovers, cute (helper 6)
**v2 (7dcec9b): PASS.** It now has its line on the body, collar and antennae, and a lit side. It is framed closer,
and the wings stay inside the frame on the down-flap (which resolves v1's NOTE). 35 frames, saturation 0.46.

**v1: FIX (v8)**, sent to helper 6.
- **The outline is missing:** rendered at 20:01, before 3b0fc70 (20:14). In the full frames, the fluffy body, the
  collar and the feathery antennae have no line; only the wings do. Re-render after pulling 3b0fc70.
- Everything below still stands for the re-render. It was a PASS with one NOTE.
- **Length and level:** 46 frames (35 needed, so the edit trims). Saturation 0.44. Locked camera, low against the
  sky, the background melts.
- **Timing:** the wings beat on 1s and the head-tilt pose lands on frame 16, inside the 23-frame cut (SG2). Its
  blink at frame 30 falls in the handle.
- **NOTE:** on the down-flap, the left forewing tip leaves the frame edge (frame 20). The moth sits in the top 55%
  of the frame with plain grass below, so it could be framed a little lower or wider. Not blocking.

## S11b: the eye-spots open (helper 6)
**v2 (285c3f1): PASS.** The outline is back on the body and antennae, the eye-spots glow brighter, and all four open
on "wrong", then hold still. 38 frames, saturation 0.49.

**v1: FIX (v8)**, sent to helper 6: as for S10b, the body, collar and antennae have no outline. Re-render after pulling
3b0fc70. Otherwise it was a PASS:
- **Length and level:** 38 frames (38 needed). Saturation 0.47.
- **Timing:** the wings stop dead, then all four eye-spots open on frames 9-17, landing on "wrong" (voice
  0.00-0.48 s). Their irises light up locally (LC4, TP11), and the shot then holds still (IM12: the reveal as a
  still).
- **Readability:** the spots read at 360 px. The face and all four spots are inside the frame and above the
  captions.

## S10a: jelly-snail, close, cute held pose (helper 4)
**Second read (coordinator): PASS.** **v8 re-render, delivered:**
- Built from 0c0ceeb (outline shells cast no shadow) with the body pivot fix: under puffshrimp's new `_empty`, the
  head-tilt had dropped the face about 0.25 m. 56 frames, saturation 0.38, holds on 3s.
- The body now has its coloured line and a lit side with a cool shadow side.
- **NOTE (shared look.outline):** at full size a few short dark slivers show inside the body, where the
  inverted-hull shell pokes through creases. They are not shadow acne (turning off self-shadow changes nothing) and
  not mesh noise (more smoothing changes nothing). Barely visible at 360 px. Reported to the coordinator.
- **Length and level:** 56 frames, 720x1280, 24 fps. Saturation 0.39, value 0.84 (bright day, LC). No black
  frames.
- **Timing:** characters on 3s. The frame runs are all 3 or longer; the longer runs are where the bob turns. The
  blink closes on frame 24-26 (SG2: one face change inside the hold). Motes drift on 1s (LC10).
- **Framing:** locked camera at eye level (SG4). The face sits at y 260-800, above the captions (845) and clear of
  the right rail. It reads at 360 px.
- **Look:** coloured lines, black eyes with the violet crescent and two highlights. One cool shadow tone, and the
  background melts at f/0.15.
- **No wrongness here.** The trail is saved for S11a, so EP4's "cute plus one wrong detail" lands across the
  S10a → S11a cut.

## S11a: the trail of smoking burnt holes (helper 4)
**Second read (coordinator): FIX.** In 1.12 s the wrong detail must read instantly (EP4), and it didn't: the holes
were small dark specks in the upper third at 360 px, a sharp red mushroom in the corner was the brightest thing in
the frame, and the smoke was faint grey on green. Reworked (commit 840944e) and **re-rendered from 0c0ceeb**: 39 frames, saturation 0.51, on 1s. **The coordinator's
re-read: PASS** ("the ember-rimmed, smoking holes now lead the eye up the trail to the snail in its 1.1 s"):
- **Camera:** low and close behind the trail. The nearest holes are big in the lower middle, at y 510-790 above
  the captions, and the trail leads the eye up to the snail.
- **Mushroom:** removed in this scene.
- **Embers:** brighter orange, with a soft local glow on the grass round each hole (LC4/TP11, no regrade).
- **Smoke:** darker and thicker.

The first version's notes, for the record:
- **Length and level:** 39 frames, saturation 0.52, value 0.81, no black frames.
- **Timing:** on 1s, because the smoke and the ember flicker are effects (IM2: the camera and effects stay on
  1s). The snail itself acts on 3s.
- **Framing:** a locked high three-quarter view down the trail. Six holes run from y 500 to 795 above the
  captions; the snail sits soft at the top left. The wrongness is lit locally (the ember edges breathe; LC4/TP11),
  with no regrade.
- **NOTE (weak):** the shell's glowing spiral is seen edge-on from behind, as a cyan band. It still reads as the
  marble's glow.
- **NOTE (weak):** where the background blur meets the smoke, the snail's tail looks slightly see-through.
- **NOTE (geography):** a small world mushroom fills the bottom-left corner, out of focus and below the caption
  line. It adds depth. The puddle shows at the right edge.

## S21: the shrimp stomps back to the puddle (bGqrs; rendered by the coordinator)
**PASS**, with one NOTE.
- **Length and level:** 64 frames (64 needed), saturation 0.45, action on 2s (IM2).
- **Picture:** a low angle with Kai lying in the foreground. He is on-model (teal jacket, gloves, joggers). The shrimp
  turns its back and stomps off toward the puddle (SU12: the gag undercuts the standoff).
- **Continuity:** the sliced, glowing, smoking stumps from S15 are behind it.
- **v8 checks:** the shrimp has its outline and lit side, and the snapping finger stays on the claw in every frame
  checked (frames 9, 19, 31; v8b).
- **NOTE:** on frames 7-8 the claw swings past the lens and fills the middle of the frame as an orange blur. It reads
  as a huffy turn. Fine at 2 frames.

## S22: the thorn tree (helper 5)
**PASS**, with one NOTE.
- **Length and level:** 57 frames (57 needed), saturation 0.44.
- **Picture:** it opens close on thorns with things skewered on them, then pulls back to the whole bare thorn tree
  beside the puddle, with the burned stumps behind (SU2: reveal by scale).
- **Timing:** the camera moves on 1s, then holds for 22 frames at the end.
- **NOTE:** the skewered shells are smooth blue and green ovals, which at 360 px read more like beans or beetles
  than shells. A ridge or spiral on them would sell "shells". Not blocking, since the line is about the tree and S23
  inserts the empty thorn.

## S23: the butcher bird lands (helper 5)
**PASS**, with one NOTE.
- **Length and level:** 82 frames (82 needed), the bird on 2s (landing is action).
- **Picture:** filmed from below (SU4), the small fluffy bird drops onto the top of the thorn tree and looks down at
  us. A beat later its light switches to a top shadow with glowing eyes: danger lit on the creature, with no regrade
  (LC4, TP11).
- **Insert:** an empty shrimp-sized thorn with a sparkle on its tip, and the bird's giant shadow sweeping over the
  grass (the tuftwing's tell).
- **NOTE:** mean saturation is 0.63 (frames peak at 0.70) because the deep blue sky fills the upper frames. That is
  just over the 0.34-0.61 band but inside E22's measured 0.26-0.69. Not blocking. A slightly paler sky gradient
  would bring it in.

## S07: Snap. The crack runs up the tank (helper 2)
**PASS**, with two NOTEs.
- **Length and level:** 36 frames (36 needed). Mean saturation 0.32; it dips on the white flash, and the lab
  frames measure about 0.40.
- **The hit (IM1, as far as a 24-frame cut allows):**
  - frames 1-2: the eye close-up;
  - frames 3-8: the claw cocked and held, with only the glint moving (IM2);
  - frames 8-9: the strike;
  - frame 10: a 1-frame white flash (IM3);
  - frames 11-12: two inverted radial impact frames with the shrimp in silhouette;
  - then the shock ring and bubble, and from frame 14 the crack running up the glass in 5 frames;
  - the result holds to the cut, and the camera drifts rather than shakes on the final hit (IM5).
- **Timing:** "Snap." (voice in 0.30 s, frame 8) lands on the strike.
- **Continuity:** the crack is `pistolshrimp.glass_crack()` on `crack_path()`, the same main zigzag S09 draws in
  the sky (code-checked). S07 adds the starburst and branches on the glass, which suits glass.
- **NOTE (IM1):** the wind-up is 5 frames, against IM1's 12-29. There is no target or observer reaction inside the
  shot; S08 follows on the floor. Both are forced by the 24-frame cut, and S04 already gave the snap its long
  wind-up.
- **NOTE (IM4/HELPERS):** each impact frame shows for 1 frame, where the target is 2-6 frames on 2s. Holding each
  inverted burst for 2 frames would hit harder, but the 1-frame pair reads as a strobe at 24 fps. Not blocking.

## S24top: the SAVE plate (XprL)
**PASS.**
- **Length and level:** 97 frames (97 needed), saturation 0.53. Kai acts on 3s.
- **Split-ready (AB13):** the action sits in the upper half (Kai from y 30 to 570). He walks in from the right and
  crouches toward the shrimp at the puddle, which raises its wet claw again.
- On-model: the cap, the K and the teal jacket. Graded lighter than the RUN plate (value 0.75 against 0.67; LC8).

## S24bot: the RUN plate (XprL)
**FIX** (sent to XprL, 30 Oct).
1. **Kai backs into the Shorts right rail and under the caption band (HELPERS v3.2 safe areas; TP16).**
   - The plate's action is in the lower half, as it should be for the split. But Kai backs to the right: his
     jacket is at x 435-550 on frame 1, x 531-642 on frame 60 and x 546-655 on frame 97, with his raised arm and
     shoulder beyond that.
   - From about frame 50 his shoulder, his outflung arm and his side are inside the right rail (x > 620,
     y 640-1180), where the like and comment buttons sit.
   - The caption band (y 845-930) crosses his torso, and this is the shot that carries the question line.
   - Fix: start him further left, or frame the camera about 150 px to the right, so he ends at x ≤ 580. Keep his
     face above about y 820.
- **Passes:** 97 frames; the bird drops from the top of the thorn tree into the lower half; it is graded darker
  (the riskier option, LC8); he is on-model; acting runs on 2s and 4s.

## S01: frame 0, the shrimp on Kai's chest (bGqrs)
**PASS**, with two NOTEs.
- **Length and level:** 69 frames (69 needed), saturation 0.46.
- **Frame 0 (ST1, EP2, TP16):**
  - At 360 px it reads at once: Kai on his back with 2D terror eyes and a sweat drop (TP7), the shrimp sitting on
    his chest glaring at him with its narrow, locked-on eyes, and its claw raised and open over his face.
  - The sliced, glowing, smoking stumps are at the top of the frame (EP4: what it just did).
  - Locked camera; the smoke runs on 1s.
- **Mouth:** Kai whispers the line. The mouth changes on frames 4, 10 and 13 ("Don't move."), then every 3 frames
  from 26 to 50 ("That claw can boil water.").
- **On-model** (cap, K, teal jacket). The finger stays on the claw.
- The claw is raised over his face rather than "2-3 cm from his nose". That is the coordinator's reviewed pose
  (bgqrs.py `s01` docstring), not a defect.
- **NOTE:** under the lower 2D terror eye, a sliver of the 3D eye shows (frame 12 at full size). A slightly bigger
  sprite, or hiding the 3D eye while the sprite is on, would clean it up.
- **NOTE:** Kai's chin reaches about y 870, the top of the caption band (845-930). The terror eyes, at y 730-790,
  stay clear.

## S04: the slow-motion snap (helper 2)
**PASS**, with one NOTE.
- **Length and level:** 73 frames (73 needed). On 1s: the effects and the slow motion.
- **Picture:** an extreme close-up of the big red snapping claw (IM13 scale). It is held open with only the glints
  moving on frames 8-16, shuts at about frame 22 (just after "snaps", frame 16), and the bubble swells in front of
  it to white-hot on "boils" (frame 45). The shock ring rises through the water.
- The pistol shrimp has its outline, and the snapping finger stays on the claw.
- **NOTE:** saturation is 0.31, just under the band but inside E22's 0.26, and fine for the cool tank.

## S18: "Its claw only works wet." (bGqrs; rendered by helper 5)
**PASS**, with one NOTE.
- **Length and level:** 60 frames (60 needed), saturation 0.42. Acting on 2s.
- **Picture:** Kai's eyes go from the pinprick shock to open, then narrow: by frames 40-60 the lids are visibly
  lower. On "wet." (frame 32) the background swaps from the grass to a blue speed-line realisation background (SU16,
  IM6).
- **NOTE:** it is framed as a face close-up (cap to chin) rather than an extreme close-up of the eyes, so the
  narrowing is subtle at 360 px. A tighter crop on the eyes would land "realisation" harder. Not blocking.

## S19: "So I didn't move. I let the sun dry it." (bGqrs)
**PASS**, with one NOTE.
- **Length and level:** 105 frames (105 needed), saturation 0.49.
- **Picture:**
  - One held, quiet shot (SG14) with the sun glare and sparkles on 1s, and a comic sweat bead on Kai (TP7).
  - The last drop on the claw tip shrinks and is gone by "dry it" (frames 49-55).
  - It then holds still for 43 frames, the ~1.4 s quiet hold that v7 asks for.
  - Kai blinks once. He is on-model, and the finger stays on the claw.
- **NOTE (the coordinator's key check):** the shrimp's face is out of frame (only its claw shows), so its
  locked-on eyes can't be seen here. If the eyes matter in S19, a slightly wider framing would include them.
  Otherwise S01, S16 and S20 carry them.

## S03a: night shift at the marine lab (helper 1)
**PASS.**
- **Length and level:** 53 frames (53 needed). Saturation 0.33, at the band's floor, which is right for the cold
  night lab (LC1, LC2).
- **Picture:** rain streaks the window on 1s. Kai, in the earth outfit (charcoal shirt; cap and K), sits at the
  desk in a back three-quarter view, with the hero tank glowing cyan beside him. The camera is locked (SG4).
- **Cut:** it cuts with S03b (same rig, same cyan tank light, same saturation band).
- **Note (minor):** Kai is static through the shot. The tank light, rain and screen carry the life (LC10), and the
  face change is S03b's job.

## S13: "Something else was already drinking." (helper 9)
**PASS.**
- **Length and level:** 62 frames (62 needed), saturation 0.52.
- **Picture:** the puff-shrimp at the puddle with its big claw dipped in the water, and ripples on the surface: the
  clue's first showing as an insert (SG10, CH3). It blinks once and looks up (SG2).
- Rendered from 0c0ceeb: outline and lit side present, and the finger is on the claw. The trees behind are the
  meadow's "before" state, which is right, since S13 comes before the snap in S15.

## S20: "It tried anyway." (bGqrs; rendered by the coordinator)
**PASS.**
- **Length and level:** 103 frames (103 needed), saturation 0.45.
- **Picture:** the shrimp on Kai's chest raises its claw and snaps on "anyway" (frame 16): just a tiny "pff" of
  dust. It stares at the claw and tilts its head (CH14: the "does not compute" beat).
- **Cut:** to Kai's deadpan face, held for about 2 s (SU11). It has dot eyes and a sweat drop (TP7), then the amber
  eyes return.
- **Key check (locked-on eyes):** the shrimp's narrow, determined eyes show before the snap, and go round and
  puzzled after it.

## S06 v2 (bb8f476) and S21 v2 (e9c0f7c): re-deliveries
- **S06 v2: PASS.** 41 frames, exactly what TIMING.md asks. The bolt now hits on frame 14 (0.52 brightness) with an
  afterflash, then the room lights stutter in 2-frame pairs from frame 20 to 35. The blackout frames are now opaque,
  so rain can't sort in front of them.
- **S21 v2: PASS.** 64 frames, saturation 0.49. It is now seen from Kai's feet: his boots are in the foreground, and
  the shrimp hops off him and stomps to the puddle in a huff (SU12). The finger stays on the claw, and the action
  runs on 2s.

## S14: "A shrimp. On land. Impossible." (helper 9; rendered by helper 5)
**Resolution (coordinator, 31 Oct):** no re-render. Helper 8 moves S14's caption above the cap (CAP_Y_SHOT), which
clears the mouth. PASS once that is checked in helper 8's next animatic.

**v1: FIX** (sent to helper 9, cc helper 5, 31 Oct).
1. **The face is framed too low: the mouth sits in the caption band (HELPERS v3.2 safe areas; TP16).**
   - The white cap fills the top 40% of the frame. Kai's eyes sit at about y 560-640, his mouth at about y 850-880
     and his chin at about y 1000.
   - The caption line ("Impossible.") will cover the mouth, and the mouth is half of this shot's two-step expression
     change (SG2).
   - Fix: tilt or raise the camera so the face sits at about y 300-800, with the cap cropped at the top.
2. **NOTE:** the two face changes (around frames 22 and 48, close to "On land" and "Impossible") are subtle at
   360 px: a slight squint and a head tilt. A stronger second step, such as brows down with a flat mouth or the
   `squint` and `brows_down` keys at 1.0, would sell "sceptical".
- **Passes:** 80 frames, saturation 0.33, holds of 21, 26 and 33 frames (acting held between pose snaps).
  On-model.

## S16: eyes open, then S01's framing (bGqrs)
**PASS.**
- **Length and level:** 76 frames (76 needed), saturation 0.40.
- **Picture:** an eye close-up with the eyes closed, opening on "eyes" (frame 24). Then a cut to S01's exact
  framing (SU9: the scary composition rhymes), with the terror-eye sprites and the shrimp on his chest. The shrimp's
  narrow, dark, locked-on eyes show (key check). Acting on 3s.
- **Note:** the S01 half shares S01's NOTE (the chin at the caption line).

## S01 v2 (c8a0958) and S18 v2 (b172892): re-deliveries
- **S01 v2: PASS.** The terror eyes are 8% bigger and centred on the rendered eyes, so the sliver of 3D eye is gone
  (frame 12 checked at full size).
- **S18 v2: PASS.** A 2D snap-zoom into the eyes on the realisation (1.0 to 1.18 over frames 30-32, held), so the
  narrowing now reads at 360 px.

## Round 8 (31 Oct, 00:45 UTC)
- **S14: PASS** (fixed by placement). In the animatic (picture.mp4 at 3ad5173), "Impossible." sits at y ≈ 150,
  above the cap, and the mouth is clear.
- **S24bot:** XprL's restage stills (okstills, 08b6456) put Kai in the centre-left of the RUN plate (about x
  240-500) with the bird dropping to his right, clear of the rail. PASS once the restaged mp4 lands.
- **S08: PASS** (helper 9). 85 frames.
  - Floor level, the lab after the strike: water pours from the hero tank to the floor and runs to the power strip.
    The spark lands on frame 55, right after "Me." (frame 48), then cut to black from frame 58 with no rain showing
    through. Nothing graphic (EP1).
  - The words line up: "Water." frame 8 (the pour), "Cables." frame 28 (the strip), "Me." frame 48.
  - **NOTE (continuity):** at this framing the tank's crack is too small to compare with S07 and S09. The water
    comes from the front of the tank, which is consistent. Code-wise it is the same lab tank.
- **S12: PASS** (helper 9). 47 frames, Kai on 3s.
  - A low side view: Kai crawls on hands and knees across the meadow toward flowers and the puddle (off frame
    right, where S13 picks up). On-model.
  - **NOTE:** Kai is small (about a quarter of the frame width, in the upper middle). Saturation 0.61 sits at the
    top of the band because of the deep sky. Thirst would read more at a tighter, lower angle. Not blocking.
- **S03b v3: PASS** (helper 1).
  - Warm skin, with the tank's cyan on the lit side only, a jaw rim light, and catchlights until the smile at
    frame 22.
  - **NOTE:** the cyan half reads teal-grey against the warm half, as a hard split down the middle of the face.
    Mean saturation fell to 0.24, below even E22's 0.26. It is a designed shadow tone, so not blocking, but it may
    look odd next to S03a.
- **S19 v2: PASS.** The last drop is full at frame 1, gone at frame 90, and stays gone.

## S11a v3: pale anime smoke (helper 4, from the coordinator's polish note, 31 Oct)
**The coordinator's read: accepted.** 39 frames, saturation 0.52, value 0.79, 13-24 s per frame.
- **Smoke:** pale lavender-grey (#cfc8d8) with a cel step to a darker underside (#9a93ab) and a soft see-through
  rim, peaking at about 60-70% opacity. Thin columns of three small puffs per hole lean up and to screen-left.
- **Clearances:** no puff crosses the shell or the eye stalks in any of the 7 sheet frames. The six burnt holes and
  their orange rims are fully readable.
- **Readability:** the smoke reads at 360 px without becoming a smear.

## Round 9 (31 Oct, 01:10 UTC)
- **S17: PASS** (bGqrs). 47 frames, saturation 0.51, the drop on 2s.
  - The second showing of the clue (CH3): an insert of the claw tip over Kai's jacket. A drop swells and falls on
    "drops." (frame 21; it lands on frame 23), leaves a dark wet splat on the jacket, and the next drop starts to
    swell.
  - The finger stays on the claw. The burning stumps are soft behind it.
- **S05a: PASS** (helper 2). 75 frames, on 1s (the effect).
  - The white-hot bubble glows at its peak in front of the snapped claw, then collapses with a flash on "sun."
    (frame 53) into rising micro-bubbles. The shot then holds.
  - NOTE: saturation 0.30, the cool tank (like S04). Fine.
- **S07 v2: PASS** (helper 2, rendered by helper 5).
  - The camera is re-aimed, so the shrimp sits mid-frame. The impact frames are composited from the subject pass.
  - The crack runs up the glass in 5 frames beside the shrimp (crack_path, as before).
  - NOTE: saturation 0.29, the tank. Round 4's notes still apply (short wind-up, impact frames on 1s).

## Round 10 (31 Oct, 01:35 UTC)
- **S15, THE SNAP (helper 10, v3 318b92d): PASS.** 127 frames (127 needed), saturation 0.50, no black frames. The
  nine-step hit (IM1), measured frame by frame:
  1. **Observation (frames 1-18):** POV, Kai's gloved hand reaches toward the shrimp drinking at the puddle; Kai on
     3s.
  2. **Eye close-up (frames 19-21, 3 frames; SG6):** the shrimp's eyes narrow.
  3. **Wind-up (frames 22-41, 20 frames; IM1 asks 12-29):** the claw rises out of the puddle and is held, dripping;
     only the drops move (IM2). Near-silence (SS2).
  4. **Strike (frames 42-43, 2 frames):** the claw snaps shut.
  5. **Flash (frames 44-45):** white, then a fade (IM3).
  6. **Impact frames (46-49):** inverted radial bursts with the shrimp in silhouette, on 2s (IM4), from the subject
     pass.
  7. **Result (frames 50-79, 30 frames; asks 24-48):** from behind Kai, small under the forest (SG8, SG9), the white
     ring and the forest wall erased into rising dust, the sliced stumps glowing. The camera is locked.
  8. **Reaction (frames 80-93, 14 frames; asks 12-20):** Kai blown backwards on 2s.
  9. **Observer shake (frames 94-110):** Kai on his back. The frame difference decays 41 → 49 → 45 → 39 → 30 → 23
     → 17 → 9 on 2s, so it settles in about 0.7 s (IM5). Knocked-out stars circle above the cap, his eyes close
     (into S16), and it holds to the end.
  - On-model; the shrimp has its outline and the finger stays on the claw. No text.
  - **Note:** the erased forest becomes big cream dust balls rather than fine dust; it reads as "gone" at 360 px.
- **S05b (helper 1; frames 40-51 by helper 6): PASS.** 51 frames, saturation 0.32 (the night lab). Kai in the earth
  outfit; the flash light fades off his face, and he lifts a gloved hand and taps the tank glass with one finger
  (around frame 24; BD2 seed). Acting on 3s, with a 1-frame tap. It cuts with S03a and S03b.
- **S12 v2 (helper 9, 055a865): PASS.** Restaged close and low: a three-quarter view of Kai crawling, panting,
  tired, with a glint at the puddle ahead, on 3s. This resolves round 8's NOTE (Kai small). Saturation 0.55.

## S02: "Ten minutes ago, I was alive." (built by the assembler from S01; reviewed in picture.mp4 2a8c1f7)
**PASS**, with one NOTE. Episode frames 57-105 (49 frames, timing.json), viewed at full size.
- **The rewind and glitch read:** every frame carries RGB split, sliced row offsets, colour bars (magenta, yellow,
  cyan) and chroma shift over S01's image. Frame 103 is one frame of full-screen static, and frames 104-105 are
  white, then the cut to S03a's dark lab.
- **Captions:** "Ten minutes ago," (frames ~64-80) and "I was alive." are readable in the band, and no glitch bar
  crosses the caption on any frame checked.
- **Flash safety (WCAG 2.3.1):**
  - The white end is one flash: frame 103 to 104 swings +0.51 in mean luminance, and 105 to 106 swings -0.55.
    That is one flash in the second, under the 3-per-second limit.
  - The S15 strike, measured in the same picture, peaks at a swing of 0.54. So S02's white is as bright as the
    strike but no harder.
  - The glitch jitter is small (±0.07 per frame) and a single frame of static is not a sequence.
- **NOTE:** to keep the strike in S15 the brightest moment of the episode, cap the S02 white at about 85% (or make
  it 1 frame).

## S24bot v2 (RUN; XprL, from the coordinator's restage; 957f393)
**PASS.** v1's FIX (Kai in the Shorts right rail) is resolved.
- **Length and level:** 97 frames, saturation 0.46, the action on 2s (with a 48-frame end hold).
- **Framing:** a higher camera about 22° down. Kai is close, stepping toward the lens with his hands up and his face
  to camera, at x 90-345. He stays clear of the right rail (x > 620, y 640-1180) on every frame checked (1, 30, 60,
  97).
- **Captions:** the face sits at y 790-880. For S24 the assembler sets the caption baseline at y 748 (CAP_Y_SHOT),
  so the question line sits above his face, not over it. The default 845-930 band does not apply to this shot.
- **Story:** the bird's giant shadow is over Kai on frames 1-35 (composited; LC8: the riskier option is darker).
  The butcher bird drops from the top of the thorn tree onto the shrimp at the puddle and mantles over it (wings
  arched, beak down), and the shrimp's pupils shrink. That is the visible cost of RUN (AB1).
- On-model. The seams at frames 25/26, 49/50 and 73/74 (stitched parts) match their neighbours.
