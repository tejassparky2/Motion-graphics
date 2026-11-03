# Mascot quality test (3 Nov 2026)

Owner: "Can we make it that quality as him?" (the "Grim" mascot references, research_notes/mascot_challenge_reference_2026-11-03.md).
- `zib.py`: an original chibi mascot (a tiny alien scientist, working name Zib) drawn in pycairo with soft 3-tone
  lighting, an occlusion shadow, a rim light, glossy eyes with two highlights, glowing antennae that wobble after a
  landing, squash and stretch, blink, five arm poses and moods (open, happy, shut, cry, angry).
- `scene.py`: a 4 s test clip and an expression sheet (`zib_expressions.png`). The test background was a frame of
  the reference creator's own footage, used only for the private side-by-side and not committed or published;
  real videos use the owner's own photos.
- Not approved yet: the owner picks the mascot first.

## Vex, the baby vampire (owner's pick, 3 Nov 2026)
- The owner made the character in ChatGPT (`assets/mascot/vex/vex_front.png`, transparent PNG, 1199x1312) and asked
  whether a Tripo or Blender 3D model would help.
- `vex_test.py` animates that single image as a 2D sprite: drop-in, squash on landing, a jelly wobble that leaves the
  boots planted (pixel-aligned slices at the image's own size, then scaled once, so no seams), breathing, blinks
  drawn over the eyes (EYES = eye centres in the image), a red reply line. A pose set from ChatGPT gives the rest.
- 3D (Tripo -> rig -> Blender) is not needed for this format: chibi proportions rig badly, the face needs its own
  expression controls, and Blender is not installed on this server. Worth it only for walking or turning shots.
