# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 13:25 UTC.

**Free for the next range** (S15 / S18 / anything). On render parts (short ranges, ~15-20 frames; this container is 4 cores: S14 ran ~80 s/frame, S10 ~95 s/frame).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S10 f041-079** (raw, for helper 6, 39 f) | **DONE, both chunks pushed.** `S10_f041-059.mp4` (19 f, at ee9a7c3) + `S10_f060-079.mp4` (20 f, at 63846f3; no S10/night/fluffmoth code change between them) = all of f041-079, builder 117211c + night 09d120f. Still f040 matched okstills/S10_final_f40.jpg. crf 6 yuv444p, bitexact, 0 tags. Sheets checked: the ring turns round the glowing wrist, slow push-in, the f059/f060 seam continuous. | parts/S10_f041-059.mp4, parts/S10_f060-079.mp4 |
| **S14 f064-084** (part 4, raw, for helper 10) | **DONE, both chunks pushed.** `S14_f064-074.mp4` (11 f, rendered at 1a5d568) + `S14_f075-084.mp4` (10 f, at 93840df; no S14/night code change between the two) = all 21 frames of part 4. Night FINAL 09d120f in both. crf 6 yuv444p, bitexact, 0 tags. Checked on sheets: night look, coral mark light, legs waving, the f074/f075 seam continuous. | parts/S14_f064-074.mp4, parts/S14_f075-084.mp4 |
| S17 f036-070 (XprL offered, 12:13) | **Declined for now** (busy with S10); told XprL to keep S17 whole. I'll claim in status/xprl.md first if I take any later. | - |

## Coordinator
