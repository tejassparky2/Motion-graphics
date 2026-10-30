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
| S10a | helper 4 | PASS (reviewed by its own builder) | 56 / 56 | 0.39 | holds on 3s, one blink |
| S11a | helper 4 | PASS (reviewed by its own builder) | 39 / 39 | 0.52 | on 1s (smoke); 2 NOTEs |

Waiting for: S01-S09, S10b, S11b, S12-S24.

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
