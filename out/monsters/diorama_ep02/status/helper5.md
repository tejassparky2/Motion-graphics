# Helper 5: Ep2 status

**2026-11-02: S07, S11, S12, S13 final** (coordinator confirmed receipt 12:40 UTC).

| Shot | Frames | File | 2D pass |
|---|---|---|---|
| S07 | 50 | shots/S07.mp4 + S07_sheet.jpg | sweat bead on temple from f5 |
| S11 | 113 | shots/S11.mp4 + S11_sheet.jpg | none (3D only) |
| S12 | 74 | shots/S12.mp4 + S12_sheet.jpg | sweat drop from f37 |
| S13 | 59 | shots/S13.mp4 + S13_sheet.jpg | nose "tink" f17, dot eyes f18 to end |

All 720x1280, 24 fps, crf 10, bitexact + stream-copy remux, 0 encoder tags.
OK stills: okstills/S07_f32, S11_f52, S11_f76, S12_f50, S13_f19.
Code: channels/monsters/diorama_ep02/helper5.py (3D), post_helper5.py (2D pass + encode).

Known caveat: in S12 the raised claw points up/outward rather than squarely at Kai's face.

## S20bot f053-078 (render job for helper 4) — **DONE, pushed**
`parts/S20bot_f053-078.mp4`: 26 frames (render f53-78), 720x1280, yuv444p crf 6, 24 fps, bitexact + remux, 0 tags.
helper4.py builder, `--frames 53-78` (ones=(1, n): every frame on 1s, so f53 is a clean start). About 170 s/frame.
Nothing past f78 was rendered (helper 3 has f079-104).

## S14 f041-075 (render job for helper 9)
**Rendering** since 13:58 UTC with helper9.py, `--frames 41-75` (helper 9 renders f001-040; ones=(1, 75)).
Raw part to helper 9's spec: `parts/S14_f041-075.mp4` (libx264 crf 10 yuv420p 24 fps, CLEAN flags,
`-start_number 41`, no 2D pass). ETA about 1.5-2 h.
