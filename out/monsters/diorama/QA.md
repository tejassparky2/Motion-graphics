# Episode 1 in diorama 2.5D: QA review (helper 4)

An independent read of every delivered shot in `out/monsters/diorama/shots/`, with the same checks as the 3D QA
(`out/monsters/ep01v2/QA.md`):
- **Picture rules:** the shot's row in `channels/monsters/EP01V2_SHOTS.md` and the rules in
  `reports/Pokémon episodes story and animation.md`.
- **Brief:** `channels/monsters/DIORAMA_EP01.md`.
- **Lengths:** the exact frame counts in `channels/monsters/ep01v2/TIMING.md`.
- **Readability:** readable at 360 px wide; the action above y 960 and left of x 560; Kai at least ~110 px tall in
  wides.
- **Timing:** characters on 2s; camera moves and effects on 1s.
- **Look:** no HUD or text, and no encoder or metadata tags in the file.

**One more check, the diorama read:**
- a tilt-shift sharp band on the subject;
- a toy-world feel from a high camera (tilt 40-80);
- nothing at eye level.

**Every beat stays on the same frame as in the 3D shot**, because the mix is shared.

## Summary

| Shot | Builder | Verdict | Frames (got / want) | Mean sat. | Notes |
|---|---|---|---|---|---|
| S03a | helper 1 | **FIX** (fix in 38c9239; re-render pending) | 53 / 53 | 0.45 | the rain was near-invisible and static; the new rain reads in the OK still |
| S03b | helper 1 | PASS (remuxed, 175fa92) | 51 / 51 | 0.39 | the smile lands at ~f22; file now clean |
| S10b | helper 6 | PASS | 35 / 35 | 0.54 | top-down, the moth big and cute; 1 NOTE |
| S11b | helper 6 | PASS | 38 / 38 | 0.54 | all four eye-spots open and stare up at the lens |
| S12 | helper 9 | PASS | 47 / 47 | 0.42 | the crawl to the pond, panting, glint on 2s; clean file |

## S03a: night shift at the marine lab (helper 1)
**Fix in progress:** mk/diorama_lab.py 38c9239 has bright 20° streaks (about 0.1 × 1.1 u) falling about 0.6 u per
frame, plus slow drips. The OK still (okstills/S03a_rain_f2.jpg) reads at 360 px. PASS once the re-rendered,
CLEAN-remuxed mp4 lands. Other lab shots that show the window pick up the new rain on their next render.

**v1: FIX** (sent to helper 1).
1. **The rain does not read and does not move (row: "rain on the window"; LC10: keep calm shots alive with
   ambient motion).**
   - In the window, the rain is a few faint specks, invisible at 360 px.
   - The whole shot changes only once, at frame 22 (frame runs of 21 and 32). In the 3D S03a the rain ran on 1s.
   - Fix: bigger, brighter diagonal streaks on the glass, animated on 1s (or 2s). A few drips running down would
     also help.
2. **File tag:** the file still carries `encoder=Lavc libx264`. Apply the same CLEAN remux as S03b.
- **Passes:**
  - The dollhouse cutaway lab from above, cold blue (LC1), saturation 0.45.
  - Kai at the desk in a back three-quarter view, in the earth outfit, with the hero tank glowing cyan beside him.
  - The power strip and its cable are planted on the floor for S08 (a nice setup).
  - 53 frames; a toy-world read.

## S03b: Kai's face lit by the tank, a fond smile (helper 1, ae19397; remuxed clean, 175fa92)
**PASS for the picture**, with one small FIX.
- **Length and level:** 51 frames, saturation 0.39 (inside the band, where the 3D version was 0.24).
- **Diorama read:** the dollhouse lab from above. Kai sits at the desk with his face turned up to the lens and lit
  cyan by the tank, the far wall soft.
- **Timing:** the face change lands as in 3D, with soft eyes then the closed-eye smile at about frame 22 (SG2). On
  2s. On-model, in the earth outfit.
- **FIX (file hygiene, DIORAMA_EP01.md "no encoder tags"):** the mp4 carries `encoder=Lavf60.16.100` and
  `Lavc60.31.102 libx264`. A stream-copy remux with deliver_ep01v2.CLEAN clears them; no re-render needed.
- **NOTE:** the face is about 60 px wide, small for a "close" beat. The smile still reads at 360 px.

## S10b: the fluffmoth hovers, cute (helper 6, e154824)
**PASS**, with one NOTE.
- **Length and level:** 35 frames, saturation 0.54.
- **Diorama read:** straight down onto the moth over flowers and clover. It is big and readable, its shadow falls
  long on the grass, and nothing is at eye level. The wings beat; the head tilt shows.
- **NOTE:** on the down-flap the left wing tip touches the frame edge (frames 1 and 25 on the sheet). The same note
  was made on the 3D version.

## S11b: the eye-spots open (helper 6, e154824)
**PASS.**
- **Length and level:** 38 frames, saturation 0.54.
- **Picture:** the wings stop. All four eye-spots open around frames 5-9 and stare straight up at the lens (from
  above, a strong read), then hold for 29 frames. The spots read at 360 px.

## S12: "I was so thirsty." (helper 9, 7a91179)
**PASS.**
- **Length and level:** 47 frames, saturation 0.42.
- **Diorama read:** high and behind. Kai crawls on hands and knees toward the pond, with the pond glint on 2s; the
  far path and trees melt in the tilt-shift.
- **Readability:** Kai is about 330 px tall, the action is inside x < 560 and y < 960, and he acts on 2s. The file
  is clean (no encoder tags).

Waiting for: S01, S02, S04-S09, S10a/S11a (mine, waiting for the coordinator's OK), S13-S24.
