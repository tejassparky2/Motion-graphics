# Helper 4 status (Ep 3)

## VERDICT (16:45 UTC): picture.mp4 (5e7bff18) PASSES; ship it. One fix recommended: the S15 f32 pop (helper 5)
- **Checked:** `picture.mp4` at 5e7bff18 (md5 6ec83c71). It's the build with S18 in; the 16:32 file before it still
  had the grey S18 placeholder card.
- **File:** 1080x1920, 24 fps, 1298 frames = 54.08 s (= timing 8274b7a), 0 Lavf/Lavc/x264 strings.
- **Every cut (18) lands on the timing.json boundaries** (50 117 172 204 271 322 370 438 513 580 660 727 772 844 938
  981 1039 1134), checked frame-by-frame. The other frame jumps are all planned or motion:
  - S02's two internal cuts (f85, f96) and S18's cut to the lighthouse (f1091);
  - the flip's fast tumble (S14, f792-828);
  - S13's drop (f737-739), and a caption change in S05 (f304);
  - **plus one glitch: f876 = S15 local f32.**
- **Continuity across cuts:** fine. The coral mark and the shrimp on his shoulder hold from S03 on. The dusk in S04
  leads into the night in S05 and every night shot after it. Wren's look holds from S16 to S18.
  - Known look changes, not blockers: S02/S03 are brighter than S01's evening, and under the coral light Wren's
    hair reads mauve (noted in rounds 1 and 2).
- **Hook:** THE VILLAGE / RAN FROM / MY WRIST at the top over the sky on frame 0, clear of Kai's face and the
  blazing mark; MY WRIST is red.
- **Captions:** word-timed, yellow on the spoken word, never over a face. Checked on the S01 chest line, the S11
  "backs to it." beat, the S18 lines, and S19's line at y 430 in the A half above the cards.
- **A/B:** A · GO TONIGHT pops on "Option A" (f1148), B · LEAVE AT DAWN on "Option B" (f1205), and both are held
  through "Comment A or B" to the last frame. The panels slide in over f1134-1136 from an empty slate frame (the
  assembler's designed entrance, as in Ep 2).
- **Edge scan (every frame):** clean, except seven short "bottom" hits in S18's lighthouse half (f1093-1132, up to
  48 px). These are the painted night water (RGB ~0,0,24, deep navy with coral reflection streaks), not unpainted
  canvas. The source shots/S18.mp4 has the same pixels. Not a defect.
- **The one fix (helper 5, S15):** at local f31 to f32 (picture f876), three things change in one frame:
  1. the pile of upside-down moths round Kai's head and chest vanishes;
  2. the light snaps from the coral glow to a warm yellow pool;
  3. Kai jumps from lying flat to half sat up.
  - It reads as a pop in the laugh hold. Fix: ease the light change and the sit-up over ~6 frames, and keep the
    moths by his head until he sits up through them. Or, cheapest, hold f31 for 2 frames and let the sit-up start
    on f33 with the light easing.
  - If there's no time, it's watchable: it lands right where he sits up, so it can pass as a comic snap.


## Now
- **S01: FINAL, pushed** (`shots/S01.mp4` + `S01_sheet.jpg`). It joins my f001-045 and helper 10's f046-062 (thanks),
  with the 2D pass: the evening sky and grade, the blazing mark, the halo, the bloom and the sparkles.
  - **File:** 62 frames (= render_frames), 720x1280, crf 10, 0 Lavf/Lavc/x264 strings.
  - **Checks:** no black edges (every frame scanned) and no frame jumps; the f045/f046 seam is smooth.
  - **Frame 0:** Wren stumbling back past the lens with her bell up, Kai's wrist blazing, the villagers behind.
  - **By f30:** the shrimp has landed on his left shoulder, and his face stays clear to the end.
- **S01 parts from bb5be5d** (split per the coordinator, 13:49 UTC). Run
  `render_shot.py -- diorama_ep03 S01 OUT --frames A-B` at full size (720x1280, about 4.8 min a frame), raw 3D only;
  the 2D pass is mine at the join.
  | Part | Who | State |
  |---|---|---|
  | f001-027 | helper 4 | DONE, pushed `parts/S01_f001-027.mp4` (crf 6 yuv444p, 0 tags) |
  | f028-045 | helper 4 | DONE, pushed `parts/S01_f028-045.mp4` (18 frames, crf 6 yuv444p, 0 tags) |
  | f046-062 | helper 10 | **DONE, pushed** `parts/S01_f046-062.mp4` (from bb5be5d; 17/17 frames, crf 6 yuv444p, start_number 46, 0 tags; checked: smooth push-in, no jump at the f54/55 chunk seam) |
  When f046-062 lands, I join the parts, run the 2D pass (the mark, the evening grade, sparkles), encode and push
  `shots/S01.mp4`.
- **S01: your 11:44 tweaks are in** (frame 1 checked: the evening grade, brows down, eyes to Wren, the mark brightest):
  1. **Face:** a nervous-defiant face (brows down and together, angry 0.6, a small grit), eyes toward Wren.
  2. **Shrimp:** further out and lower on his shoulder, so his whole face stays clear.
  3. **Grade:** S02's evening sky and late-afternoon grade, through helper 3's own `post_helper3.evening()`, applied
     before the mark so the mark stays the brightest thing.
  I'll check frame 1 as soon as it lands. Earlier notes:
  (frame 0 of the episode) and `okstills/S01_f030.png` (the shrimp landed on his left shoulder). The old f036 is
  removed. Half-scale renders, upscaled, with the 2D pass.
  1. **Camera:** low, behind and to the left of Wren, looking up at Kai, 40 mm, a slow push-in on 1s. Found with an
     occlusion-checked probe so nothing hides his face, the mark or his shoulder. Her hood and braid are soft in the
     near right foreground; as she stumbles back she moves past the lens.
  2. **Kai faces camera:** his raised LEFT wrist above his face, the inner forearm to us.
     - **The mark blazes:** helper 9's `mark()` zigzag at 2.1x, a white-hot core, a coral line, a pink halo and a
       white bloom, sparkles every 0.6 s, plus a coral light that also lights his face. It's the brightest thing
       in frame.
     - **The 2D mark only draws where the camera really sees his forearm** (ray-cast per frame), so it can never
       land on Wren.
  3. **Behind him:** the villagers on the meadow flinch, turn and scatter sideways and away, dropping their nets.
  4. **The shrimp:** in his right hand at f1; it hops onto his LEFT shoulder beside his neck (helper 3's S02 perch
     and size, never the cap) by f30.
  5. **Light:** a warm low sun from Wren's side; the mark is brighter.
  - **Weak spot:** his face reads steady rather than clearly nervous/defiant at phone size. The face keys are pushed
    (brows down, a tight wide mouth); I can add a 2D sweat drop if you want more.
- **S11: FINAL, pushed** (`shots/S11.mp4` + `S11_sheet.jpg`).
  - **File:** 92 frames (= render_frames), 720x1280, crf 10, 0 Lavf/Lavc/x264 strings. The edge-band scan found no
    black edges; the background is dark navy, which is not unpainted canvas.
  - **Fixed after the first render:** the light is higher and the moth slower. On "Moths don't fly at a light"
    (f25-38) there is now a clear gap between the moth and the light; before, its antennae touched it and it read
    as flying AT it. At f92 its body ends at x ~540, clear of the right rail.
  - **Your notes, all in:** the frame shifted 70 px left and 90 px up; the glow line stops in the fur of its back;
    the flight trail; the moth big; the hill silhouette below the captions.
  - **Render time:** about 27 s/frame.
- **S14 part 3 (f043-063) for helper 10: DONE, pushed** as `parts/S14_f043-063.mp4` (from 09d120f, 21 frames, crf 6 yuv444p, 0 tags).
- **S07 for helper 5: split with XprL (their offer, 14:42).** I rendered f041-050: **DONE, pushed**
  `parts/S07_f041-050.mp4` (10 frames, crf 10 yuv420p, CLEAN, 0 tags); XprL takes f051-060 after their S17 part (about 15:30 UTC). Both are written in
  helper5.md's S07 row.
- **QA, round 1 (S02, S03, S06, S12, S13, S14 as landed; S11 is mine, already checked):**
  - **Files:** all 720x1280; frames S02 79, S03 67, S06 63, S12 79, S13 57, S14 84; 0 Lavf/Lavc/x264 strings each.
  - **Edge-band scan:** every 2nd frame of each shot; no unpainted black at any edge.
  - **Cut check:** no frame jumps, except S02's two planned cuts (f35 Wren to the sky, f46 to Kai).
  - **S02 PASS.** Wren is steady with her bell up, the zigzag sky crack, and Kai looks up with his raised wrist;
    the mark/crack match reads. Note: Wren's half is bright daytime green, while the sky half and S01 are evening.
  - **S03 PASS.** The villagers back away and the shutters close; Kai is left alone in the lane, the shrimp on his
    shoulder, the 2D mark on. Note: it is bright midday (blue sea, hard light) between S01/S02's evening and
    S04's sunset. If there's time, a late-afternoon grade (`post_helper3.late_afternoon`) would match.
  - **S06 PASS.** A night swarm pours down the hill path toward camera; in the close-up a wing eye-spot blinks open.
  - **S12 PASS, physics reads at phone size.** Side-on, the light glows and the line runs to the moth's back while
    the dotted trail goes round. Weak spot: the light is only ~60 px above the moth at 720 wide, so "above them"
    rests on the line's angle. Not a blocker.
  - **S13 PASS, physics reads.** Kai drops flat with his wrist on the ground; a coral glow cone points up into the
    swarm. Weak spot: his "determined face" is too small to read at phone size (his head is ~40 px). Not a
    blocker, since the action carries it.
  - **S14 PASS, the flip reads at phone size.** The held beat, then the swarm rolls belly-up (legs visible), stalls
    and drops with dust puffs, landing in a heap of moths with their legs up around him. The bottom third is empty
    grass, which is fine under the 71% captions.
- **QA, round 2 (S08, S10, S16):** frames S08 80, S10 79, S16 55 (= render_frames); 720x1280; 0 tags; no black
  edges (every 2nd frame); no frame jumps.
  - **S08 PASS.** Wren on the porch rings her bell with both hands, mouth flapping, with 2D ring lines at the bell.
    Note: only her bell shows ring lines; "every bell in the village rings" isn't on screen (no other bell in frame).
    If the sound carries the village bells, that's fine; otherwise a few far 2D ring lines in the upper left would
    sell it.
  - **S10 PASS, physics reads at phone size.** A top view of a full ring of moths circling Kai, the glow at his
    raised wrist in the centre; the circling motion is clear in playback.
  - **S16 PASS.** Wren lowers the bell; her stern face softens to wide eyes by the second half.
  - **Continuity watch (S08/S16 vs S02):** under the coral night light, Wren's hair reads mauve-brown and her eyes
    grey, against dark purple hair and gold eyes in S02's daylight. It's the light, not the model, so it's fine
    unless you want them closer.
- **QA, round 3 (S01, S05, S09, S19bot):** frames S01 62, S05 79, S09 87, S19bot 176 (= render_frames); 720x1280;
  0 tags; no frame jumps.
  - **Edges:** none on S01, S05 or S09. S19bot's black top band (to y ~485) is the planned empty half for helper 8's
    split, so it's expected; nothing else is black.
  - **S01 PASS** (mine; see above).
  - **S05 PASS.** A high wide shot at night: the dark island, the lake, one coral glow in the village; a very slow
    push-in (the plant). The upper ~40% is the dark lake: deep navy, not unpainted.
  - **S09 PASS.** 2D ring lines on several bells along the lane; the swarm comes over the roofs and pours past the
    bell posts straight to Kai, with no flinch.
  - **S19bot PASS.** Dawn: Kai walks away along the beach road toward the rising sun, the shrimp on his shoulder,
    and the look back is there. Within the band he's small (~170 px tall) but clear.
  - **S19top PASS.** 176 frames, 0 tags, no jumps. Night: Kai and Wren in the rowing boat, his mark lighting a
    coral pool on the water, the lighthouse with its coral glow on the far shore. The bottom half is black on
    purpose (for the split). The edge scan skipped it, since the frame is dark overall. Note: the boat and the two
    of them take up ~200 px, so it reads as a wide shot; fine for the A/B split.
- **QA, round 4 (S04, S07, S15, S17, S18):** frames S04 44, S07 60, S15 106, S17 70, S18 107 (= render_frames);
  720x1280; 0 tags; no black edges.
  - **S04 PASS.** A quick dusk: the sun sinks and the sky goes blue to rose to navy; the lane darkens and his
    mark's coral glow grows on the path. His face is under the cap brim, looking down.
  - **S07 PASS.** Glittering wing dust; Wren throws her cape over her face; the villager scratches with the 2D itch
    squiggles; moths above the awning. No jump at the f040/041 or f050/051 part seams.
  - **S15 FIX RECOMMENDED** (see the verdict): the f31/32 pop. Otherwise good: the field of belly-up moths with
    dizzy spirals and stars, Kai sitting up into a grin.
  - **S17 PASS.** Wren kneels by Kai and glances back at the village on "village", then turns back to him. Note:
    the eyes in the window cracks don't read at phone size; the huts behind are small and soft.
  - **S18 PASS.** She leans in, then points across the lake; the cut (local f52) goes to the lighthouse on the
    rocks with a coral glow at the top and reflections on the water.

## Coordinator
(answers here)
