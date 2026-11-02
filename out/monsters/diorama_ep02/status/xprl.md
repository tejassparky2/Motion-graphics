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
- Frames 1-80, one Blender. The result will be a single raw part at out/monsters/diorama_ep02/parts/S15_f001-080.mp4 (crf 6, yuv444p, no tags).
- Helper 9 was rendering S15 too, in parallel with S14/S19. I've asked it to drop S15 so its other two run faster; it does the 2D pass on S15 from my part.
- I'll update this note when the part is pushed.
