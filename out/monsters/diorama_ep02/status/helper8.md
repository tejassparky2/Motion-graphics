# helper 8: Ep 2 assembly status

**Updated:** 2 Nov 2026, ~12:55 UTC. Branch head when written: see the commit that last touched this file.

## The picture
`out/monsters/diorama_ep02/picture.mp4` (+ `picture_sheet.jpg`, every 12th frame):
- 1376 frames, 57.33 s, 1080x1920, no encoder tags.
- Rebuild with `python channels/monsters/assemble_ep01v2.py --version diorama_ep02 --animatic --check`.

**Shots in (15):** S01-S04, S06-S13, S16-S18. They're 720 renders scaled to 1080 with lanczos; there are no ESRGAN versions yet (say if Ep 2 should get them, as Ep 1 v3 did).

**Placeholders (numbered cards):** S05, S14, S15, S19, S20top, S20bot.

## Checks on the real frames
- **The hook is on frame 0:** I SAVED / THE SHRIMP / THAT TRIED / TO KILL ME (the last line red), shown until line 1 ends (f63).
  - It sits in S01's middle band (y 480, size 80), over Kai's legs and the tree trunk.
  - Kai's face and the diving bird's face stay clear at the top, and the shrimp stays clear below.
- **Captions are clear of faces.** They're word-timed, 2-4 words each. Placements:
  - **S07 at 150:** in the sky above his cap; at the 71% band they crossed the claw he's turning.
  - **S10 at 600:** above the upside-down bird; at the band they sat on its masked face.
  - **S20 at 520:** in the A half under the net. The B half has Kai's face at caption height and the hide at chest level.
  - **Everything else stays at the 71% band (905).**
    - S01: over the grass, above the shrimp.
    - S02: grass under the diving bird.
    - S03/S04: under his hands, so the scratched forearm stays visible.
    - S06: under the profile shrimp on the plain ground.
    - S08/S12/S13: on his body.
    - S11: under the puffball.
    - S16: the blurred foreground.
    - S17/S18: below Wren's face.
  - S09 has no words, so no captions.
- **The edge scan passes.** No unpainted black in any frame's outer 3 px.
  - S09 frame 34 (the snap's ink impact frame: black ground, white speed lines) is black at the edges on purpose. It's listed as intended in `EDGE_OK_VERSION`.

## The S20 split (laid out on the OK stills; re-checked when the finals land)
- **Plates:** S20top is above, shifted up 60 px. S20bot is below, shifted down 80 px. Helper 4 now renders from row 486, so every visible row is rendered.
- **Cards (85% size), both straddling the divider:**
  - A · HAND OVER at (124, 585), over Kai's shins and the stump;
  - B · HIDE at (370, 715), in the sky between Kai's cap and Wren's hood.
  - Their timing: A on "Option A", B on "Option B", both pulse on "Comment".
- XprL and helper 4 have the zones to keep clear; their stills fit.

## Cover
`python channels/monsters/ep01v2_cover.py --ep02` makes the candidates plus a phone grid. The frames get picked once the shots are final:
- **hook (the pick):** I SAVED / MY KILLER, S01;
- **aim:** NATURE'S / PISTOL, S08;
- **tap:** IT TAPPED / MY NOSE, S13.

None of them repeats the title.

## Next
- Re-check each placeholder shot as it lands.
- The final cut (no --animatic) and the cover when all 20 shots are in.
