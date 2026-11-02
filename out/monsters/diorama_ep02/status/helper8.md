# helper 8: Ep 2 assembly status

**Ending change (2 Nov ~19:40 UTC, the coordinator's note):** Option B is now "show her the glowing mark". S20 becomes 148 frames.
- The B label in the assembler is now **SHOW MARK**. At 85% that card is 422 px wide from its centre, so the B card has to move left from x 370 to x ≤ 286 to stay in frame. "SHOW IT" (320 px) would fit where B is now.
- I'll place it on helper 4's new S20bot: SHOW MARK if x ~286 is clear of Kai and Wren, else SHOW IT.
- The assembler reads S20's length and the word beats from timing.json, so no code changes are needed for 148 frames. I'll rebuild when the new timing and S20bot land.


**FINAL PUSHED (2 Nov ~16:55 UTC):** the final `picture.mp4` is in.
- Built with no --animatic, from all 21 pieces at ESRGAN 1080. S19 is helper 9's final (6fd32f1d).
- The timing is 0a7b842, which includes e6a1dbb.
- 1376 frames, 57.33 s, 52.7 MB.
- Tag check: no encoder or tool tags.
- The edge scan is clean; S09 f34 is allowed.
- The cover is `cover.jpg`: "fear", S05 f70, I SAVED / MY KILLER. It has no metadata.


**Updated:** 2 Nov 2026, ~16:20 UTC (on the re-voiced timing, 0a7b842). **Status: final. All 21 pieces are at 1080, nothing is slated.** Branch head when written: see the commit that last touched this file.

## The picture
- **Rebuilt on the re-voiced timing (0a7b842):** l2 "The bird struck first." is captioned on S02, and the 1-frame cut moves are in (S02 32, S03 51 from f98, S09 82 from f473, S12 63, S18 75, S20 145 from f1231). Every shot conforms inside its handle with no hold warnings, and the edge scan is clean.
`out/monsters/diorama_ep02/picture.mp4` (+ `picture_sheet.jpg`, every 12th frame):
- 1376 frames, 57.33 s, 1080x1920, 47.7 MB. Tag check: no encoder or tool tags. The only fields are the standard MP4 container ones: brand, handler, language.
- Edge scan: clean apart from S09 f34, which is allowed (see below).
- Rebuild with `python channels/monsters/assemble_ep01v2.py --version diorama_ep02 --check` (final, no --animatic).

**Shots in (all but S19):**
- S01-S18, plus S20top and S20bot.
- Every one is at ESRGAN 1080 in `shots_1080/`. None uses lanczos.
- The latest ESRGAN runs were on 2 Nov:
  - the re-rendered **S02** (44 f, helper 1) and **S04** (66 f, the shrimp in Kai's hands, fd9f12b), both with `--force`. Their old ESRGANs were stale.
  - **S14** (75 f, helper 9's final, 87a245a) and **S15** (80 f).

**S19 (helper 9's final, 123 f):** ESRGAN in two halves, then joined. Captions checked:
- "The lake." crosses Wren's chest under her face.
- The close-up lines sit on Kai's belt under the shrimp.
- No face is covered.

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
    - S03/S04: under his hands, so the scratched forearm stays visible. On the S04 re-render the band is on his knees, under the shrimp curled in his hands.
    - S05: under the dripping claw in the hands shot. In the terror-eyes close-up it crosses the back of the shrimp's fluff: no face is covered, and his face fills the top.
    - S06: under the profile shrimp on the plain ground.
    - S08/S12/S13: on his body.
    - S11: under the puffball.
    - S14: on his legs, below the glowing wrist mark and the shrimp.
    - S15: under the glowing scar in the close-up, then under the crack in the sky.
    - S16: the blurred foreground.
    - S17/S18: below Wren's face.
  - S09 has no words, so no captions.
- **The edge scan passes.** No unpainted black in any frame's outer 3 px.
  - S09 frame 34 (the snap's ink impact frame: black ground, white speed lines) is black at the edges on purpose. It's listed as intended in `EDGE_OK_VERSION`.

## The S20 split (laid out on the OK stills; S20top checked on its final)
- **Plates:** S20top is above, shifted up 60 px. S20bot is below, shifted down 80 px. Helper 4 now renders from row 486, so every visible row is rendered.
- **Cards (85% size), both straddling the divider:**
  - A · HAND OVER at (124, 585), over Kai's shins and the stump;
  - B · HIDE at (370, 715), in the sky between Kai's cap and Wren's hood.
  - Their timing: A on "Option A", B on "Option B", both pulse on "Comment".
- XprL and helper 4 have the zones to keep clear; their stills fit.
- **S20bot final (8a9a5d4):** checked in the split.
  - Kai holds the shrimp at his chest, then slips it into his shirt; Wren stays on the right.
  - The B card stays in the sky, clear of his cap, his raised hand and Wren.
  - There's no sliver above its render band.
- **S20top final (d584790):** checked in the split.
  - The captions sit under the net; the shrimp is above it, then at the rim.
  - Kai's and Wren's faces are clear.
  - The A card covers only Kai's shins and the stump.
  - Kai's cap sits near the top edge (the plate shifts up 60 px) but isn't cut.

## Cover
`out/monsters/diorama_ep02/cover.jpg` (1080x1920), made by `python channels/monsters/ep01v2_cover.py --ep02`. The candidates and the phone grid are in `covers/`.
- **Pick: "fear", S05 f70: I SAVED / MY KILLER.** It's the terror-eyes close-up. The words sit on his cap, his eyes are clear under them, and the shrimp is at his chest.
- At phone size it reads better than the old placeholder pick (S01 f30, where his head hid under the words and the shrimp was tiny).
- **Other candidates:**
  - **aim:** S08, NATURE'S / PISTOL;
  - **tap:** S13, IT TAPPED / MY NOSE;
  - **rake:** S04 f12;
  - **hook:** S01 f30.

None of them repeats the title.

## Next
- Nothing left on my side: the picture and the cover are final. The final mux and the Whisper check are the coordinator's.
