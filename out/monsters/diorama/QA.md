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
| S03a | helper 1 + coordinator | PASS (re-rendered, 9e3862e) | 53 / 53 | 0.45 | the new rain streaks read at 360 px and fall on 1s; clean file |
| S03b | helper 1 | PASS (remuxed, 175fa92) | 51 / 51 | 0.39 | the smile lands at ~f22; file now clean |
| S05b | helper 1 | PASS | 51 / 51 | 0.40 | the flash fades on 1s, the finger rises and taps on 30/34; clean file; 1 NOTE |
| S10a | helper 4 | PASS (self-review; the coordinator approved the stills) | 56 / 56 | 0.51 | the cute hold, blink on 23, on 2s; flowers round it; clean file |
| S15 | helper 10 + helper 7 + coordinator | **FIX** | 127 / 127 | 0.48 | the claw's wind-up (22-41) is unreadable: the shrimp is ~40 px and behind Kai; file tags |
| S11a | helper 4 | PASS (self-review; the coordinator approved the stills) | 39 / 39 | 0.58 | the trail of ember holes leads up to the snail; pale smoke on 1s; clean file |
| S10b | helper 6 | PASS (remuxed clean, 8672c25) | 35 / 35 | 0.54 | top-down, the moth big and cute; 1 NOTE |
| S11b | helper 6 | PASS (remuxed clean, 8672c25) | 38 / 38 | 0.54 | all four eye-spots open and stare up at the lens |
| S12 | helper 9 | PASS | 47 / 47 | 0.42 | the crawl to the pond, panting, glint on 2s; clean file |
| S17 | bGqrs | PASS | 47 / 47 | 0.38 | the drop falls from the claw tip by Kai's face; clean file; 1 NOTE |
| S24bot | XprL | PASS | 97 / 97 | 0.49 | the bird's shadow sweeps over Kai, then it drops on the shrimp and mantles; clean |
| S06 | helper 9 | PASS for the picture; **FIX** no rain in the window | 41 / 41 | 0.47 | the bolt on "storm" (14), Kai looks up, the lights stutter; clean |
| S07 | helper 2 | PASS (remuxed clean, 7c99972) | 36 / 36 | 0.42 | the eye, the strike, the ring, the crack up the tank glass |
| S09 | helper 3 | PASS (remuxed clean, e2b1af1) | 66 / 66 | 0.35 | the white-out blooms onto Kai in the flowers, then the cracked sky; 1 NOTE |
| S22 | XprL | PASS | 57 / 57 | 0.53 | the thorn tree on "thorn tree", pulling back to Kai by the pond; clean |
| S23 | XprL | PASS | 82 / 82 | 0.45 | the butcher bird lands on the tree, turns to its danger colours; clean |
| S04 | helper 2 | PASS (remuxed clean, fb8d031) | 73 / 73 | 0.23 | eye f1-4, claw open, shut on 19, the white-hot bubble swells to "boils"; 1 NOTE (low saturation) |
| S14 | helper 3's builder (+ 2D push-in, 8a3257d) | PASS | 80 / 80 | 0.37 | Kai on all fours looks up: wide eyes, then narrowed and a head tilt (SG2); 1 NOTE |
| S20 | helper 5's builder | PASS | 103 / 103 | 0.40 | the tiny "pff", the shrimp stares at its claw, cut on 44 to Kai's deadpan held 60 frames |
| S24top | XprL | PASS | 97 / 97 | 0.47 | Kai walks down from the thorn tree to the shrimp at the pond, push-in on 1s (57-85); reads in the top half |
| S08 | helper 9 (joined by the coordinator, 1b30467) | PASS | 85 / 85 | 0.29 | water pours off the tank and runs to the power strip, a spark on 55-57, the lights die, black from 58; rain in the window |
| S01 | bGqrs | re-render pending (helper 4, after bGqrs's three-quarter shrimp fix) | 69 | - | v1 (45ef696) superseded |
| S21 | helper 5 (rendered by helper 4) | PASS | 64 / 64 | 0.43 | the shrimp stomps off Kai's chest to the pond, the claw dips in with a ripple ring; clean |

## S03a: night shift at the marine lab (helper 1)
**v2 (9e3862e): PASS.** 53 frames, saturation 0.45, a clean file. The bright diagonal streaks fill all four panes and
fall on 1s, with drips; they read at 360 px. The shot is alive the whole way through (LC10).

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

Waiting for: S02, S05a, S13, S16, S18, S19; the S03a re-render and the S15 fix.

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

## S17: "Then I saw the drops." (bGqrs, rendered 0319933)
**PASS**, with one NOTE.
- **Length and level:** 47 frames, saturation 0.38, a clean file.
- **Picture:** from above, Kai lies on his back below the pond with the shrimp on his chest. A drop swells on the
  claw tip by his face and falls (the clue's second showing, CH3), with the 2D glint pass on it.
- **NOTE:** the drop is small and lands by his face rather than on the jacket, as the 3D insert did. It reads at
  360 px as a blue blip against the claw. A brighter splat would help.

## S24bot: RUN (XprL, f423ff4)
**PASS.**
- **Length and level:** 97 frames, saturation 0.49, a clean file, on 2s.
- **Picture:** from above, the butcher bird's giant shadow sweeps across Kai (frames 1-35). The bird then drops onto
  the shrimp at the pond and mantles over it, with Kai beside it.
- **Split:** it shows in place in the lower half (S24_FOCUS y 960). Kai is about 240 px tall, clear of the right rail.

## S07: the strike in the tank (helper 2)
**PASS** (remuxed clean, 7c99972).
- **Length and level:** 36 frames, saturation 0.42.
- **Picture:** the shrimp's eye close-up, the strike and the ring, then the crack runs up the tank glass over the
  shrimp, seen from above. Each beat reads at 360 px and keeps the 3D frame numbers.
- **FIX (file hygiene), done:** the mp4 carried 2 encoder tags; helper 2's CLEAN remux (7c99972) cleared them
  (0 tags, 36 frames).

## S09: waking in the meadow, the cracked sky (helper 3)
**PASS** (remuxed clean, e2b1af1), with one NOTE.
- **Length and level:** 66 frames, saturation 0.35 (low in the band, from the white-out at the start).
- **Picture:** white frames bloom onto Kai lying in the pink flowers, a blur tilt up, then the crack in the sky
  between two clouds, held from about frame 33, so it is on screen for "cracked sky" (frames 31-44).
- **FIX (file hygiene), done:** the 2 encoder tags are gone after helper 3's CLEAN remux (e2b1af1).
- **NOTE:** the sky crack is a thin line; at 360 px it reads, but only just. A thicker or brighter crack (or a glow
  along it) would sell the beat.

## S22: "That's when I saw the thorn tree." (XprL)
**PASS.**
- **Length and level:** 57 frames, saturation 0.53, a clean file.
- **Picture:** close on the thorn tree with its skewered bugs, then a pull back to a wide from above: Kai on his back
  by the pond, the shrimp beside him, the tree small at the top. The tree is the subject while "thorn tree" is spoken
  (frames 27-32).
- **Readability:** in the wide Kai is about 170 px tall, inside x < 560 and y < 960.

## S23: "A butcher bird hangs its food on thorns." (XprL)
**PASS.**
- **Length and level:** 82 frames, saturation 0.45, a clean file.
- **Picture:** the butcher bird lands on top of the thorn tree ("bird", frame 17), switches to its brown danger rig
  with dark eyes, then its giant shadow and the sparkle on an empty thorn ("on thorns", frames 39-45): the threat is
  set up for S24.

## S06: "Then the storm hit." (helper 9, 8158785)
**PASS for the picture**, with one FIX.
- **Length and level:** 41 frames, saturation 0.47, a clean file.
- **Picture:** the same dollhouse lab from above as S03a. The bolt forks across the window on "storm" (frame 14) with
  2-frame flashes (14, 16), Kai turns his head up to the window on 16, and the lamp and room lights stutter on and off
  from frame 20 to 35. Every beat reads at 360 px.
- **FIX (continuity):** the window has no rain. It was rendered before the S03a rain fix (mk/diorama_lab.py 38c9239 /
  3f04152), so S03a's heavy rain stops dead at the cut, just as "the storm hit". A re-render with the current
  diorama_lab picks the rain up; nothing else changes.

## S21: "Then it stomped back to the puddle." (helper 5's builder, rendered by helper 4)
**PASS.**
- **Length and level:** 64 frames, saturation 0.43, a clean file (0 encoder tags), crf 10.
- **Picture:** from above, Kai lies on his back by the pond. The shrimp climbs off his chest on "stomped" (frame 14),
  stomps on 2s round his head to the pond edge ("back to the puddle", frames 25-36), and dips its claw in from
  about frame 42, with a ripple ring on the water by frame 49. Kai is about 450 px tall, the action inside x < 560
  and y < 960.

## S04: "Its claw snaps so fast, the water boils." (helper 2, 7e437df; remuxed clean, fb8d031)
**PASS**, with one NOTE.
- **Length and level:** 73 frames, a clean file.
- **Picture:** the same cut points as the 3D shot: the eye close-up on frames 1-4, then the extreme close on the
  claw in the toy aquarium. The claw is held open (frames 5-18), shuts on 19, the shock line and the white-hot bubble
  burst on 22 and swell through "boils" (frame 45) to the end, on 1s. IM13 scale reads.
- **NOTE:** saturation 0.23, under the 0.34-0.61 band and below the 3D shot's 0.31: the water and gravel are a grey
  green, so the red shrimp is the only colour. A cooler, cleaner cyan tint on the tank water (as in 3D) would lift it.
  Not blocking: the beat reads.

## S14: "A shrimp. On land. Impossible." (helper 3's builder, rendered 736826b; 2D push-in 8a3257d)
**PASS**, with one NOTE.
- **Length and level:** 80 frames, saturation 0.37, a clean file.
- **Picture:** from above, Kai on all fours at the pond looks up at the lens (at the shrimp). The two-step change
  (SG2) reads: wide eyes on "A shrimp" (frames 1-11), narrowed by "On land" (about 30), then the sceptical head tilt
  on "Impossible" (about 50), held. The 20% 2D push-in toward his face runs on 1s.
- **NOTE:** even with the push-in his face is about 110 px wide at full size (about 55 px at 360 px). The change
  reads, but only just; the eyes carry it.

## S20: "It tried anyway." (helper 5's builder, 558f03b)
**PASS.**
- **Length and level:** 103 frames, saturation 0.40, a clean file, on 2s.
- **Picture:** from above, the shrimp on Kai's chest lifts its claw, snaps on "tried" and gets only a tiny "pff" puff
  (about frame 26), stares at the claw and tilts its head (CH14, frames 34-40). Cut on 44 to Kai's deadpan face,
  close, with the claw in the foreground, held 60 frames (SU11).

## S24top: SAVE (XprL, efb1871)
**PASS.**
- **Length and level:** 97 frames, saturation 0.47, a clean file; step 2 with the push-in on 1s (frames 57-85).
- **Picture:** from above, Kai walks down from the thorn tree to the shrimp at the pond's edge; the push-in ends on
  him standing over it, his face readable. Everything sits in the top half (S24_FOCUS y 320), clear of the split line.

## S08: "Water. Cables. Me." (helper 9's builder, joined by the coordinator, 1b30467)
**PASS.**
- **Length and level:** 85 frames, a clean file. Saturation 0.29 is under the band only because frames 58-85 are the
  black (the row asks for 0.8 s of black); the lit part sits near 0.4.
- **Picture:** the same dollhouse lab from above, now with S03a's rain in the window (continuity holds). On "Water"
  the tank spills over the desk edge, and the sparkling stream runs down to the power strip by "Cables" (frame 28).
  After "Me" (48) a white spark flares on the strip (55-57) with a ring of light, the room lights die, then black
  from 58. Nothing graphic. The spark and the stream read at 360 px.
