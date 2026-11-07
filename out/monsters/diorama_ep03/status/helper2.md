# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 12:50 UTC.

On render parts (short ranges, ~15-20 frames: this container is 4 cores and slower).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S10 f041-079** (raw, for helper 6, 39 f) | Rendering at ee9a7c3 (contains builder 117211c + night 09d120f). Still f040 matches okstills/S10_final_f40.jpg (mean diff 5/255 = jpg/scale noise), 95 s/frame. **Chunk 1 `S10_f041-059.mp4` PUSHED** (19 f, crf 6 yuv444p, bitexact, 0 tags; sheet checked: the ring turns round the glowing wrist, slow push-in, no artefacts). **Chunk 2 f060-079 rendering, lands ~13:25 UTC.** The two chunks = f041-079. | parts/S10_f041-059.mp4 (pushed), parts/S10_f060-079.mp4 (rendering) |
| **S14 f064-084** (part 4, raw, for helper 10) | **DONE, both chunks pushed.** `S14_f064-074.mp4` (11 f, rendered at 1a5d568) + `S14_f075-084.mp4` (10 f, at 93840df; no S14/night code change between the two) = all 21 frames of part 4. Night FINAL 09d120f in both. crf 6 yuv444p, bitexact, 0 tags. Checked on sheets: night look, coral mark light, legs waving, the f074/f075 seam continuous. | parts/S14_f064-074.mp4, parts/S14_f075-084.mp4 |
| S17 f036-070 (XprL offered, 12:13) | **Declined for now** (busy with S10); told XprL to keep S17 whole. I'll claim in status/xprl.md first if I take any later. | - |

## Coordinator
