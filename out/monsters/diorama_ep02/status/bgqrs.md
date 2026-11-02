# bGqrs status (Ep 2)

Updated 2 Nov 2026.

| Shot | State | File |
|---|---|---|
| S01 | **Final, pushed** (9f77411). 78/78 frames, 720x1280 at 24 fps, crf 10, 0 encoder tags. A long-lens race: Kai sprints with his hand out from frame 0; the dark bird dives head-on from the thorn tree, its shadow a streak on the grass, and ends beside his hand. The shrimp sits at the pond edge, above the caption band. | shots/S01.mp4 + S01_sheet.jpg |
| S20bot f105-156 | **Rendering** (for helper 4; started 12:50 UTC). Helper 4's builder, frames 104-156 (the chunk rule), about 180 s/frame here, so done around 15:35 UTC. Frame 105 matches the approved look. The raw part (crf 6, yuv444p, no tags) follows. | parts/S20bot_f105-156.mp4 (pending) |
| S03 | **Final, pushed** (01a7aba). 62/62 frames, crf 10, 0 encoder tags. A knee slide, a cupped-hand scoop with a splash, and a hunch over the shrimp. Only the bird's shadow appears, sweeping over him from about f44; the strike is helper 1's S04. | shots/S03.mp4 + S03_sheet.jpg |

- Builder: channels/monsters/diorama_ep02/bgqrs.py. Encoder: post_bgqrs.py.
- OK stills: okstills/bgqrs_S01_f1.jpg (the hook frame), bgqrs_S01_f40.jpg and bgqrs_S03_f24/f30/f56.jpg.
- Render time per frame on this container: S01 about 95-100 s, S03 about 110-120 s.
- Continuity: the shrimp in his hands is 0.6 scale (helper4.SHRIMP_IN_HAND). The bird's dive runs 0.28 to 0.74 of the perch-to-shrimp line in S01 (helper 1's S02 picks it up there). kai_s03_end() gives S04 the end pose of S03.

Known weak points (I'll fix them if QA wants):
- S01: Kai is about 35% of the frame height. A tighter shot on him would cut the shrimp or the bird out of the portrait frame.
- S01: the long lens flattens the dive, so the bird reads as coming at the lens more than falling.

Status: rendering S20bot f105-156. I'm checking git for QA notes.
