# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 16:22 UTC.

On render parts (short ranges, ~15-20 frames; this container is 4 cores: S14 ran ~80 s/frame, S10 ~95 s/frame).


**Free for the next range** (all my claims are done and pushed).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S18 f082-107** (raw, for helper 9, 26 f) | **DONE, pushed.** Rendered from **feacea3** (helper 9's "S18 parts from", a worktree pinned to it; no H9_S18_* env), ~40 s/frame. 26 frames, crf 6 yuv444p, bitexact, `-start_number 82`, 0 tags, no 2D pass. Sheet + full-size f082/f107 checked: the slow push-in on the lighthouse, coral lamp room and halo, the moon up-left, the lamp's reflection rippling, no artefacts. | parts/S18_f082-107.mp4 |
| **S17 f036-070** (raw, for XprL, 35 f) | **DONE, pushed.** Rendered at 65e475a (XprL confirmed the same S17 code as theirs): `S17_f036-050.mp4` (15 f), `S17_f051-065.mp4` (15 f), `S17_f066-070.mp4` (5 f). crf 6 yuv444p, bitexact, 0 tags, no 2D pass. Sheet + full-size f040/f060 checked: Wren kneeling at Kai's side, the glance back at the huts and the turn back to him, no artefacts. | parts/S17_f036-050.mp4, S17_f051-065.mp4, S17_f066-070.mp4 |
| **S15 f071-106** (raw, for helper 5, 36 f) | **DONE, both chunks pushed**, both rendered at 00f1b1e: `S15_f071-088.mp4` (18 f) + `S15_f089-106.mp4` (18 f) = all of f071-106. crf 10 yuv420p, CLEAN, 0 tags, no 2D pass. Sheets checked: Kai sitting up in the coral pool among the upside-down moths, his turn to the lens, the shrimp's look round, the f088/f089 seam continuous. (My local build/ S15_heroes.json is not pushed; helper 5's builder writes its own.) | parts/S15_f071-088.mp4, parts/S15_f089-106.mp4 |
| **S10 f041-079** (raw, for helper 6, 39 f) | **DONE, both chunks pushed.** `S10_f041-059.mp4` (19 f, at ee9a7c3) + `S10_f060-079.mp4` (20 f, at 63846f3; no S10/night/fluffmoth code change between them) = all of f041-079, builder 117211c + night 09d120f. Still f040 matched okstills/S10_final_f40.jpg. crf 6 yuv444p, bitexact, 0 tags. Sheets checked: the ring turns round the glowing wrist, slow push-in, the f059/f060 seam continuous. | parts/S10_f041-059.mp4, parts/S10_f060-079.mp4 |
| **S14 f064-084** (part 4, raw, for helper 10) | **DONE, both chunks pushed.** `S14_f064-074.mp4` (11 f, rendered at 1a5d568) + `S14_f075-084.mp4` (10 f, at 93840df; no S14/night code change between the two) = all 21 frames of part 4. Night FINAL 09d120f in both. crf 6 yuv444p, bitexact, 0 tags. Checked on sheets: night look, coral mark light, legs waving, the f074/f075 seam continuous. | parts/S14_f064-074.mp4, parts/S14_f075-084.mp4 |

## Coordinator
