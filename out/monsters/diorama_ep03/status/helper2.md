# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 12:15 UTC.

On render parts (short ranges, ~15-20 frames: this container is 4 cores and slower).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S10 f041-079** (raw, for helper 6, 39 f) | **Claimed** 10:35 UTC (assigned in status/helper6.md). **GO from helper 6 (11:40), builder 117211c.** Queued right after my S14 part 4 (coordinator's order: S14 first; both at once on my 4 cores would only slow each): starts ~12:10 UTC, at a pull containing 117211c. First a still of f040 to match okstills/S10_final_f40.jpg, then the range. **Helper 6: you render ~2x faster than me; if you're free before I reach S10's end, take f060-079 back (write it in your file and I'll stop at f059).** Then: pull, render a still and match it against helper 6's S10 still, then the range. Goes BEFORE S14 part 4 (the coordinator is holding S14). | parts/S10_f041-079.mp4 (pending) |
| **S14 f064-084** (part 4, raw, for helper 10) | **DONE, both chunks pushed.** `S14_f064-074.mp4` (11 f, rendered at 1a5d568) + `S14_f075-084.mp4` (10 f, at 93840df; no S14/night code change between the two) = all 21 frames of part 4. Night FINAL 09d120f in both. crf 6 yuv444p, bitexact, 0 tags. Checked on sheets: night look, coral mark light, legs waving, the f074/f075 seam continuous. | parts/S14_f064-074.mp4, parts/S14_f075-084.mp4 |
| S17 f036-070 (XprL offered, 12:13) | **Declined for now** (busy with S10); told XprL to keep S17 whole. I'll claim in status/xprl.md first if I take any later. | - |

## Coordinator
