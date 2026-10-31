# Episode 1 v3 in diorama 2.5D: QA review (helper 4)

Every v3 shot is checked against two documents: the brief, `channels/monsters/DIORAMA_EP01_V3.md` (the "max" quality
bar), and the script, `out/monsters/story_v3_diorama.md`. The checks are the same as the v2 QA
(`out/monsters/diorama/QA.md`):

- **Length:** the frame count equals the `render_frames` in `ep01v3/timing.json`.
- **Beats:** every beat lands on its word in the v3 timing.
- **Readability:** the subject of the line is the biggest thing in frame, above y 960 and left of x 560, and clear
  of the caption band (845-930).
- **Camera:** a slow move on 1s.
- **Acting:** a clear key pose with anticipation and overshoot, on 2s. Blinks every 2-4 s. The face fits the line.
  Lying Kai reads as lying.
- **File:** no encoder strings.

## Summary
| Shot | Owner | Verdict | Frames (got / want) | Notes |
|---|---|---|---|---|
| S03a, S03b, S04, S05a, S05b | v2 copies, 2D grade-matched to Q3 (c7b638e) | PASS (interim) | exact | clean files; the lab grade now matches the Q3 renders; superseded when the owners' full v3 renders land |
| S10a | helper 4 (v3 re-render) | PASS (self-review) | 56 / 56 | the cute hold and the blink as v2, now with the 8% push-in on 1s; clean |
| S11a | helper 4 (v3 re-render) | PASS (self-review) | 39 / 39 | the trail of smoking ember holes up to the snail, now with the push-in; clean |
| S10b, S12 | (v2 copies) | PASS (v2 QA) | exact | the same picture and length as v2; S10a/S11a/S10b/S11b/S12 re-render under the GO |
| S01 | bGqrs (68fb99c) | PASS; 1 NOTE | 69 / 69 | hook frame: the new lying pose (arm over his head), terror eyes + sweat, claw by his face, a cut stump smoking by his head; NOTE no blink in 2.9 s |
| S06 | helper 9 (bb29d71) | PASS | 41 / 41 | the strong flash on "storm" (14), and in the tank the shrimp jolts awake with comic surprise lines (16-22) |
| S07 | helper 2 (ee287b1) | PASS | 87 / 87 | the startled shrimp jumps, snaps on "snap" (42) with the flash and ring, the crack zigzags across the glass, the water jet spits out |
| S08 | helper 9 (4cc6b26) | PASS; 1 NOTE | 98 / 98 | the camera follows the waterfall off the desk across the tiles to the strip, the plugs fizz; NOTE Kai stays seated, then stands in S08a |
| S08a | helper 1 (e4bbe29) | PASS | 60 / 60 | close on the sneakers as the spill slides under, tilt up to his fear face + sweat; ends on FEAR_STAND (S08b's f1) |
| S09 | helper 3 (2a2d3e3) | PASS | 72 / 72 | black, the soul spark falls; Kai in the pink flowers, eyes open on "woke up", stares at his raised hand; the cracked sky on "another world" (now bold, fixes v2's thin crack) |
| S15a | helper 10 (f7a947e) | PASS | 48 / 48 | close low on the shrimp, its eyes narrow; cut to the dripping claw raised in the foreground, aimed at Kai |
| S17 | bGqrs (5a5a9c8) | PASS | 46 / 46 | the drop swells and falls from the claw tip by his face on "drops" |
| S18 | bGqrs (5b73d83) | PASS; 1 NOTE | 60 / 60 | eyes narrow, cut on 31 to the realisation background; NOTE his eyes sit half under the cap brim, small at 360 px |
| S21 | helper 5 / coordinator (430eb95) | PASS | 64 / 64 | the shrimp struts off his chest to the puddle and dips its claw (ripple ring); Kai lying, smoking stumps |
| S22 | XprL (dbbfe8c) | PASS | 57 / 57 | the thorn tree on "thorn tree", pull back to Kai and the shrimp among the smoking stumps |
| S23 | XprL (b428667) | PASS | 74 / 74 | re-rendered to the v3 length: lands on the tree, the danger rig, then the giant shadow; closes my v2-copy NOTE |
| S23b | XprL (1bdad22) | PASS | 56 / 56 | close on the bird's eyes and a head tilt; cut on ~31 to its view: the tiny shrimp at the puddle |
| S23c | helper 6 (b8330ac) | PASS | 60 / 60 | the bird's shadow slides over the shrimp, which keeps drinking, eyes shut and content; the bird on the tree top |
| S15b | bGqrs + helper 2 (c192795) | PASS | 62 / 62 | Kai on his back, dazed, KO stars circling his cap, a smoking stump with a glowing cut by his head ("an inch"); no seam at the f31/32 join (max frame change 0.011) |
| S24top (A) | XprL + coordinator + helper 2 (c0d0d40) | PASS; 1 NOTE | 180 / 180 | Kai walks down to the shrimp at the pond and stands over it as the bird's shadow sweeps in over both (f90+); he blinks; seams invisible (max change 0.014); the shrimp sits just above the split line at y 640; NOTE: he stands over it rather than reaching for it (the brief's "reaching") |
| S16 | bGqrs; parts helper 6 + coordinator (0dd4fbf) | PASS | 77 / 77 | close on Kai's shut eyes, they open by "eyes" (24) and jump to the 2D terror eyes + sweat; the reveal pulls back on "chest" (45-47) to the shrimp on his chest (S01's framing); seams at 39/40 and 57/58 invisible |
| S11b | (v2 copy) | PASS (v2 QA) | 38 / 37 | the assembler trims 1 frame |
| S13 | (v2 copy) | PASS (v2 QA) | 62 / 63 | the assembler holds 1 frame |
| S14 | (v2 copy) | PASS (v2 QA) | 80 / 82 | the assembler holds 2 frames |
| S08b | helper 4 | PASS (self-review; the coordinator approved the stills) | 63 / 63 | the spark runs through the water, the electrocution jolt and x-ray on "died.", the fall, black from 31; clean |

Waiting for: S03a/S03b/S04/S05a/S05b re-renders, S10b, S11b, S12, S13, S14, S15, S15b, S16, S19, S20, S24top, S24bot.

## S23: the v2 copy in a shorter v3 slot
The words land on the same frames as in v2 ("bird" 17, "thorns." 45, the line out by 58), so every spoken beat
survives. The v3 cut is 62 frames, against v2's 70, so the cut ends 8 frames earlier, inside the bird's
danger-colour hold. It is more than the README's 1-2-frame trim.

This is not blocking: the bird shot hands over to the new S23b ("And it was looking at the shrimp."), which carries
the threat.

## The lab grade-match (c7b638e, interim)
The five reused lab shots (S03a, S03b, S04, S05a, S05b) were passed through `tools/grade_match.py`: lift, gamma, gain
and saturation plus a soft vignette, fitted to the Q3 lab before/after. The result is
`okstills/lab_grade_match_before_after.jpg`.

**Verdict: PASS as the interim.**
- The change is subtle but moves the cool night lab onto the Q3 look, with no clipping and no colour shifts on
  Kai's face.
- Frame counts are exact (53/51/73/75/51) and the files are clean.

They stay interim until the GO re-renders land: helper 1 (S03a, S03b), helper 2 (S04, S05a) and helper 7 (S05b,
from helper 1's builder).

## S08b: "That's how I died." (helper 4)
**PASS** (self-review; the coordinator approved the OK stills). 63 frames, clean file (0 encoder strings).
- **f1-10:** helper 1's FEAR_STAND (S08a's last pose), trembling on 2s, the shared water round his sneakers.
- **f4-10:** the spark at the strip; the current runs through the water to his feet (fx2d.electric_arcs with travel).
- **f11-23:** the overshoot into the electrocution pose (bent elbows, clawed hands by his head, arched back, head back,
  one knee buckling), shaking on 1s, arcs crawling over his joints.
- **x-ray:** the strobe on 14-15, 18-19 (on "died.") and 22-23, with the skeleton on his exported joints.
- **f24-30:** limp at 24; the lights die at 27 and he falls back with a short camera follow; he lands at 29.
- **f31:** black to the end. One fix after the first encode: the 2D arcs faded past their end onto frame 31, and
  now stop at the black.

## Finals round 1 (19:15 UTC): 14 shots, all PASS
Every file has the exact v3 render_frames and 0 encoder strings. The rows above carry the beats; checked on the
sheets plus crops of the tank (S06) and of Kai's face (S18). Three NOTES, none blocking:
- **S01:** the hook's terror eyes hold for the whole 2.9 s with no blink; the brief asks for one every 2-4 s.
- **S08 to S08a:** Kai sits at the desk through S08 (the camera leaves him at about f45) and is standing in the
  spill in S08a. The cut reads as a jump, since we never see him get up. It is covered by S08a opening close on
  his feet.
- **S18:** the narrowing eyes sit half under the cap brim. Tilting the cap back, as in S08b and S08a, would help.
