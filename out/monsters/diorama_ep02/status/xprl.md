# XprL status (Ep2: Wren, S17, S18, S20 top)

**2 Nov 2026, 12:45 UTC: all three of my shots are complete.**

| Shot | File | Render frames | Commit |
|---|---|---|---|
| S17 | out/monsters/diorama_ep02/shots/S17.mp4 (+ S17_sheet.jpg) | 75 | d4116f0 |
| S18 | out/monsters/diorama_ep02/shots/S18.mp4 (+ S18_sheet.jpg) | 86 | 76ece0a |
| S20top | out/monsters/diorama_ep02/shots/S20top.mp4 (+ S20top_sheet.jpg) | 156 (all) | this commit |

- **Encoding:** all three are joined with join_parts.py --ep02 at crf 10, with 0 x264/Lavf/Lavc tags. Raw parts are in out/monsters/diorama_ep02/parts.
- **S20top:** a full frame from the west, with the same staging as the approved stills. Kai lowers the shrimp into Wren's net (hands over it around f42, released around f43, in the net from about f50). Faces, hands, the shrimp and the net rim stay above plate y ~510, per helper 8's split layout (6fa9cc4). It's ready for helper 8 to drop into the split.
- **Rendering:** nothing more is rendering on my side.

**2 Nov 2026, 12:55 UTC: S15 (helper 9's builder) is rendering here at the coordinator's request.**
- **Split (coordinator, 13:08 UTC):** I render frames 1-20 only and push one RAW part, out/monsters/diorama_ep02/parts/S15_f001-020.mp4. Helpers 2, 3 and 6 take f021-040, f041-060 and f061-080. Helper 9 has been told, because it had offered to take 41-80.
- Builder: helper9.py at 9c14cb8 or later. Encode: libx264 crf 10, yuv420p, 24 fps, the CLEAN flags, no 2D pass.
- At about 350 s per frame (3 of 20 done at 13:08), the part should be pushed around 14:50 UTC.
- **14:47 UTC: S15 f001-020 is pushed** as out/monsters/diorama_ep02/parts/S15_f001-020.mp4: 20 frames, 720x1280, yuv420p, 24 fps, 0 tags, raw with no 2D pass. My S15 render has stopped, and nothing else is rendering here.
