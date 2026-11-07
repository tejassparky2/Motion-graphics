# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 11:35 UTC.

On render parts (short ranges, ~15-20 frames: this container is 4 cores and slower).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S10 f041-079** (raw, for helper 6, 39 f) | **Claimed** 10:35 UTC (assigned in status/helper6.md). **On hold** (helper 6, 10:39: until helper 9's night()/mark() are final; helper 6 says go in status/helper6.md). Then: pull, render a still and match it against helper 6's S10 still, then the range. Goes BEFORE S14 part 4 (the coordinator is holding S14). | parts/S10_f041-079.mp4 (pending) |
| **S14 f064-084** (part 4, raw, for helper 10) | **Claimed** 10:15 UTC (also marked in status/helper10.md). S14 OK'd (11:20), night FINAL at 09d120f. **Rendering since 11:33 UTC at 1a5d568** (contains 09d120f): chunk 1 f064-074 first (~1.7 h, lands ~13:15 UTC), then chunk 2 f075-084 (~1.5 h, ~14:50 UTC). Pulled 8274b7a timing (S14 = 84 render frames). Raw spec: crf 6 yuv444p, bitexact, `-start_number 64`, no tags. Test still f074 (builder as of 10:10 UTC) rendered clean: **528 s/frame here**, so the part is ~3 h. To lose little if my container is reclaimed I'll push it in two chunks, `S14_f064-074.mp4` (11 f) then `S14_f075-084.mp4` (10 f); together they are part 4 (post_helper10 joins numbered PNGs, so the split doesn't matter). | parts/S14_f064-074.mp4, parts/S14_f075-084.mp4 (pending) |

## Coordinator
