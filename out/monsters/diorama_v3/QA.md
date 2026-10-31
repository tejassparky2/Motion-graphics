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
| S03a, S03b, S04, S05a, S05b, S10a, S10b, S11a, S12, S22 | (v2 copies) | PASS (v2 QA) | exact | the same picture and length as v2 |
| S11b | (v2 copy) | PASS (v2 QA) | 38 / 37 | the assembler trims 1 frame |
| S13 | (v2 copy) | PASS (v2 QA) | 62 / 63 | the assembler holds 1 frame |
| S14 | (v2 copy) | PASS (v2 QA) | 80 / 82 | the assembler holds 2 frames |
| S23 | (v2 copy) | PASS (v2 QA); **NOTE** | 82 / 74 | 8 frames shorter in v3 (62 in the cut, was 70); see below |
| S08b | helper 4 | rendering | - / 63 | OK stills in okstills/S08b_f*.jpg |

Waiting for: S01, S06, S07, S08, S08a, S09, S15a, S15, S15b, S16-S21, S23b, S23c, S24top, S24bot.

## S23: the v2 copy in a shorter v3 slot
The words land on the same frames as in v2 ("bird" 17, "thorns." 45, the line out by 58), so every spoken beat
survives. The v3 cut is 62 frames, against v2's 70, so the cut ends 8 frames earlier, inside the bird's
danger-colour hold. It is more than the README's 1-2-frame trim.

This is not blocking: the bird shot hands over to the new S23b ("And it was looking at the shrimp."), which carries
the threat.
