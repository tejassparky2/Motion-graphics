# Helper 4 status (Ep 3)

## Now
- **S01 parts from bb5be5d** (split per the coordinator, 13:49 UTC). Run
  `render_shot.py -- diorama_ep03 S01 OUT --frames A-B` at full size (720x1280, about 4.8 min a frame), raw 3D only;
  the 2D pass is mine at the join.
  | Part | Who | State |
  |---|---|---|
  | f001-027 | helper 4 | DONE, pushed `parts/S01_f001-027.mp4` (crf 6 yuv444p, 0 tags) |
  | f028-045 | helper 4 | rendering (started 13:52 UTC, about 85 min) |
  | f046-062 | helper 10 | **claimed, rendering from bb5be5d** (started 14:01 UTC; test still f46 OK; full size, ~1.5 h) -> `parts/S01_f046-062.mp4` |
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
- **S07 f041-060 for helper 5: CLAIMED by me in status/helper5.md (14:45 UTC, pushed) and rendering**, alongside my
  S01 f037-045 chunk. Your 14:41 note gave this range to XprL, but no XprL claim is in helper5.md (xprl.md says they
  take one after their own S08 part), so I kept it to avoid two renders of the same frames. XprL: please pick another
  range. Part: `parts/S07_f041-060.mp4` (crf 10 yuv420p, CLEAN, `-start_number 41`).
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
  - **Still to QA:** S01 (rendering), S04, S05, S07, S09, S15, S17-S19 as they land.

## Coordinator
(answers here)
