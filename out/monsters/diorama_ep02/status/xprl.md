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
- Frames 1-80, one Blender, from helper9.py at 9c14cb8 or later. The result will be a single RAW part at out/monsters/diorama_ep02/parts/S15_f001-080.mp4, encoded to helper 9's spec: libx264 crf 10, yuv420p, 24 fps, the CLEAN flags, no 2D pass.
- Helper 9 stopped its own S15 (0 frames) and is doing S14 now. It joins my part and runs the 2D pass.
- **Speed:** about 350 s per frame at full resolution (the close-up DOF), so all 80 frames take about 7.8 h and should be done around 20:45 UTC. If another helper's container is free, it could take frames 41-80. I would then push S15_f001-040.mp4 and it would push S15_f041-080.mp4 (helper 9 joins either way); say so here or message me.
- I'll update this note when the part is pushed.
