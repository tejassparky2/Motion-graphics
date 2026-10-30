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

**Verdicts:** PASS (ready for the cut), FIX (a concrete change, sent to the builder), or NOTE (weak but acceptable).
Most serious first within each shot. Updated as shots land.

## Summary

| Shot | Builder | Verdict | Frames (got / want) | Mean sat. | Notes |
|---|---|---|---|---|---|
| S03b | helper 1 | **FIX** | 51 / 51 | **0.23** | face washed white, no cyan; shirt bleached toward the world teal |
| S09 | helper 3 | **FIX** | 67 / 66 | 0.44 | crack gone and frame blurred on "cracked sky"; Kai's wake-up mostly after the 54-frame cut |
| S06 | helper 9 | PASS | 48 / 41 | 0.37 | double flash on the line, lights cut out on 2s |
| S10a | helper 4 | PASS (reviewed by its own builder) | 56 / 56 | 0.39 | holds on 3s, one blink |
| S10b | helper 6 | PASS | 46 / 35 | 0.44 | 1 NOTE |
| S11a | helper 4 | PASS (reviewed by its own builder) | 39 / 39 | 0.52 | on 1s (smoke); 2 NOTEs |
| S11b | helper 6 | PASS | 38 / 38 | 0.47 | the spots open on "wrong" |

Waiting for: S01-S03a, S04-S05b, S07, S08, S12-S24.

## S03b: Kai's face lit cyan by the tank, a fond smile (helper 1)
**FIX** (sent to helper 1, 30 Oct).
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
**FIX** (sent to helper 3, 30 Oct). The shot was built to the old 2.3 s estimate. v7's TIMING.md gives it **54
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
**PASS**, with one NOTE.
- **Length and level:** 46 frames (35 needed, so the edit trims). Saturation 0.44. Locked camera, low against the
  sky, the background melts.
- **Timing:** the wings beat on 1s and the head-tilt pose lands on frame 16, inside the 23-frame cut (SG2). Its
  blink at frame 30 falls in the handle.
- **NOTE:** on the down-flap, the left forewing tip leaves the frame edge (frame 20). The moth sits in the top 55%
  of the frame with plain grass below, so it could be framed a little lower or wider. Not blocking.

## S11b: the eye-spots open (helper 6)
**PASS.**
- **Length and level:** 38 frames (38 needed). Saturation 0.47.
- **Timing:** the wings stop dead, then all four eye-spots open on frames 9-17, landing on "wrong" (voice
  0.00-0.48 s). Their irises light up locally (LC4, TP11), and the shot then holds still (IM12: the reveal as a
  still).
- **Readability:** the spots read at 360 px. The face and all four spots are inside the frame and above the
  captions.

## S10a: jelly-snail, close, cute held pose (helper 4)
**PASS** (self-review: a second reader should look too).
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
**PASS** (self-review), with two NOTEs.
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
