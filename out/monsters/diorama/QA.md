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
| S05b | helper 1 | PASS | 51 / 51 | 0.40 | the flash fades on 1s, the finger rises and taps on 30/34; clean file; 1 NOTE |
| S10a | helper 4 | PASS (self-review; the coordinator approved the stills) | 56 / 56 | 0.51 | the cute hold, blink on 23, on 2s; flowers round it; clean file |
| S15 | helper 10 + helper 7 + coordinator | **FIX** | 127 / 127 | 0.48 | the claw's wind-up (22-41) is unreadable: the shrimp is ~40 px and behind Kai; file tags |
| S11a | helper 4 | PASS (self-review; the coordinator approved the stills) | 39 / 39 | 0.58 | the trail of ember holes leads up to the snail; pale smoke on 1s; clean file |
| S10b | helper 6 | PASS (remuxed clean, 8672c25) | 35 / 35 | 0.54 | top-down, the moth big and cute; 1 NOTE |
| S11b | helper 6 | PASS (remuxed clean, 8672c25) | 38 / 38 | 0.54 | all four eye-spots open and stare up at the lens |
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

Waiting for: S01, S02, S04, S05a, S06-S09, S13, S14, S16-S24; the S03a re-render.

## S15: THE SNAP, diorama (helper 10 frames 1-42, helper 7 frames 43-84, coordinator frames 85-127; 1484987)
**FIX** (sent to helper 10, cc the coordinator).
1. **The wind-up does not read (IM1 step 3, the episode's biggest beat; DIORAMA_EP01.md: Pokémon-level clarity
   at phone size, one idea per beat).**
   - Frames 1-41 are one wide of the clearing with a slow push. The shrimp is about 40 px across and sits behind
     and under Kai's arm, so its claw rising, held and dripping (frames 22-41, the silence before the snap) is
     a small red blob at 360 px.
   - The 3D shot's eye close-up (frames 19-21, SG6) is also gone.
   - Fix (keep every frame number): cut at 19 to a closer, steeper camera on the shrimp (dist about 25-35, its face
     turned up to the lens; the eye beat on 19-21), and hold it through 22-41 with the claw rising past Kai's
     reaching hand. The wide can return at 50 for the blast, as now.
2. **File tags:** the mp4 carries `x264 - core 164`, `Lavc60.31.102 libx264` and `Lavf60.16.100`. A CLEAN remux
   clears them.
- **Passes:**
  - The strike, the flash, the inverted radial impact frames and the stars all keep the 3D frame numbers.
  - The money shot (frames 50-79) reads well from above: the white dust bursts where the trees stood, and the
    glowing stumps.
  - Kai is blown back (frames 80-93), then lies on his back below the pond with the stars and his eyes closing, on
    2s.
  - On-model. Saturation 0.48.
- **NOTE:** in the result wide, Kai is about 60 px tall, under the brief's ~110 px for wides. The blast swath is the
  subject there, so it is acceptable.

## S05b: "But only in water." (helper 1, d2d687f)
**PASS**, with one NOTE.
- **Length and level:** 51 frames, saturation 0.40, a clean file.
- **Picture:** the dollhouse desk from above. The flash fades on Kai's face on 1s (frames 1-20), his finger rises
  (18-24) and taps the tank glass on 30 and 34, as in 3D (BD2 seed). Earth outfit.
- **NOTE:** the tapping hand is small at 360 px (a dark glove against the dark tank lid). A brighter catch on the
  glass at the tap would sell it.

## S10a: "Everything here was tiny." (helper 4)
**PASS** (self-review; the coordinator approved the OK stills, with the meadow dressing added).
- **Length and level:** 56 frames, saturation 0.51, a clean file. The cute hold on 2s, one slow bob, the blink on
  23 (as in 3D), and pollen motes.
- **Diorama read:** a close toy view from the south, with the snail's face turned up to the lens. The pink and white
  flower dots melt in the tilt-shift above and below it.

## S11a: "And every one of..." (helper 4)
**PASS** (self-review; the coordinator approved the OK stills and asked for the two fixes, which are in).
- **Length and level:** 39 frames, saturation 0.58, a clean file, 24-42 s per frame.
- **Picture:** from above and behind, the trail of six burnt, ember-rimmed holes runs up the frame to the snail.
  The pale cel smoke rises off every hole on 1s, leaning up-left, clear of the shell. The slime ribbon is now a
  faint sheen, so the holes sit in the grass, with flower dots around.
