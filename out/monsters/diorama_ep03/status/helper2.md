# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 10:15 UTC.

On render parts (short ranges, ~15-20 frames: this container is 4 cores and slower).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S14 f064-084** (part 4, raw, for helper 10) | **Claimed** 10:15 UTC (also marked in status/helper10.md). Starts as soon as the coordinator OKs the S14 stills (helper 10's rule). Pulled 8274b7a timing (S14 = 84 render frames). Raw spec: crf 6 yuv444p, bitexact, `-start_number 64`, no tags. | parts/S14_f064-084.mp4 (pending) |

## Coordinator
