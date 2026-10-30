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

**Verdicts:** PASS (ready for the cut), FIX (a concrete change, sent to the builder), or NOTE (weak but acceptable).
Most serious first within each shot. Updated as shots land.

## Summary

| Shot | Builder | Verdict | Frames (got / want) | Mean sat. | Notes |
|---|---|---|---|---|---|
| S03b | helper 1 | PASS (v2, 20:38) | 51 / 51 | 0.28 | v1 FIX resolved; 1 NOTE (saturation) |
| S09 | helper 3 | PASS (v2, 6d95527) | 66 / 66 | 0.47 | v1 FIX resolved: eyes open on "woke up", crack held through "cracked sky" |
| S06 | helper 9 | PASS | 48 / 41 | 0.37 | double flash on the line, lights cut out on 2s |
| S10a | helper 4 | PASS (v8 re-render) | 56 / 56 | 0.38 | outline and lit side back; 1 NOTE (outline slivers) |
| S10b | helper 6 | PASS (v2, 7dcec9b) | 35 / 35 | 0.46 | outline back; reframed, so the wings stay in frame |
| S11a | helper 4 | delivered (v8 rework), awaiting the coordinator's re-read | 39 / 39 | 0.51 | holes big at y 510-790, smoke dark |
| S11b | helper 6 | PASS (v2, 285c3f1) | 38 / 38 | 0.49 | outline back; brighter eye-spot glow |
| S21 | bGqrs (coordinator render) | PASS | 64 / 64 | 0.45 | finger stays on the claw; 1 NOTE |
| S22 | helper 5 | PASS | 57 / 57 | 0.44 | 1 NOTE (the shells read as beans) |
| S23 | helper 5 | PASS | 82 / 82 | 0.63 | 1 NOTE (saturation just over the band) |

Waiting for: S01, S02, S03a, S04, S05a, S05b, S07, S08, S12-S20, S24.

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
the frame, and the smoke was faint grey on green. Reworked (commit 840944e) and **re-rendered from 0c0ceeb**: 39 frames, saturation 0.51, on 1s. Waiting for the
coordinator's re-read:
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
