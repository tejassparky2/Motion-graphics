# Helper 2 status (Ep 3)

Updated 7 Nov 2026, 11:55 UTC.

On render parts (short ranges, ~15-20 frames: this container is 4 cores and slower).

| Job | State | File |
|---|---|---|
| Setup | **OK.** Pulled dce8b49, read DIORAMA_EP03.md. Check still Ep 2 S20bot f027 (current code, v2) matches helper 4's pushed `S20bot_v2_f021-040` frame 27: mean diff 0.43/255, no pixel over 16 (codec noise only). 82 s/frame at full size for that shot. No Ep 3 builders pushed yet. | - |
| **S10 f041-079** (raw, for helper 6, 39 f) | **Claimed** 10:35 UTC (assigned in status/helper6.md). **GO from helper 6 (11:40), builder 117211c.** Queued right after my S14 part 4 (coordinator's order: S14 first; both at once on my 4 cores would only slow each): starts ~12:10 UTC, at a pull containing 117211c. First a still of f040 to match okstills/S10_final_f40.jpg, then the range. **Helper 6: you render ~2x faster than me; if you're free before I reach S10's end, take f060-079 back (write it in your file and I'll stop at f059).** Then: pull, render a still and match it against helper 6's S10 still, then the range. Goes BEFORE S14 part 4 (the coordinator is holding S14). | parts/S10_f041-079.mp4 (pending) |
| **S14 f064-084** (part 4, raw, for helper 10) | **Claimed** 10:15 UTC (also marked in status/helper10.md). S14 OK'd (11:20), night FINAL at 09d120f. Rendered at 1a5d568 (contains 09d120f; no S14 code changes since). **Chunk 1 f064-074 PUSHED** (11 frames, 0 tags, checked on a sheet: night look, coral mark light, legs waving, no artefacts). The final builder runs ~80 s/frame here (not 528), so **chunk 2 f075-084 lands ~12:10 UTC**. Pulled 8274b7a timing (S14 = 84 render frames). Raw spec: crf 6 yuv444p, bitexact, `-start_number 64`, no tags. Test still f074 (builder as of 10:10 UTC) rendered clean: **528 s/frame here**, so the part is ~3 h. To lose little if my container is reclaimed I'll push it in two chunks, `S14_f064-074.mp4` (11 f) then `S14_f075-084.mp4` (10 f); together they are part 4 (post_helper10 joins numbered PNGs, so the split doesn't matter). | parts/S14_f064-074.mp4 (pushed), parts/S14_f075-084.mp4 (rendering) |

## Coordinator
