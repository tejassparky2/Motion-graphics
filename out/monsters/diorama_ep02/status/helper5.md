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

## S20bot f053-078 (render job for helper 4; range cut from f104 by the coordinator, helper 3 takes f079-104)
**Rendering** since 2026-11-02 12:50 UTC: helper4.py builder, `--frames 53-78` (S20bot has ones=(1, n), so every
frame renders on 1s and f53 is a clean chunk start). Raw part goes to `parts/S20bot_f053-078.mp4` (crf 6 yuv444p,
bitexact, no tags). Restarted on the smaller range before any frame was saved, so nothing past f78 exists. ETA about 1-1.5 h.
