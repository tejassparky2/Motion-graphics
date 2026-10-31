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
| S10a, S10b, S11a, S12, S22 | (v2 copies) | PASS (v2 QA) | exact | the same picture and length as v2; S10a/S11a/S10b/S11b/S12 re-render under the GO |
| S11b | (v2 copy) | PASS (v2 QA) | 38 / 37 | the assembler trims 1 frame |
| S13 | (v2 copy) | PASS (v2 QA) | 62 / 63 | the assembler holds 1 frame |
| S14 | (v2 copy) | PASS (v2 QA) | 80 / 82 | the assembler holds 2 frames |
| S23 | (v2 copy) | PASS (v2 QA); **NOTE** | 82 / 74 | 8 frames shorter in v3 (62 in the cut, was 70); see below |
| S08b | helper 4 | PASS (self-review; the coordinator approved the stills) | 63 / 63 | the spark runs through the water, the electrocution jolt and x-ray on "died.", the fall, black from 31; clean |

Waiting for: S01, S06, S07, S08, S08a, S09, S15a, S15, S15b, S16-S21, S23b, S23c, S24top, S24bot.

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
