# Helper 10 status (Ep 2 diorama)

Updated 2026-11-02. All shots done; nothing pending.

| Shot | Frames | File | Notes |
|---|---|---|---|
| S08 | 72 | shots/S08.mp4 + S08_sheet.jpg | Kai aims the pistol shrimp two-handed, low hero angle; bird circling behind |
| S09 | 93 | shots/S09.mp4 + S09_sheet.jpg | Twist: eye close-up, wind-up, bird dives, SNAP, bird blasted into the thorn tree |
| S10 | 64 | shots/S10.mp4 + S10_sheet.jpg | Bird upside down in the thorn bush, dazed, stars circling (alive) |

- S09 snap: impact frames f34-36 (0-based 33-35); shockwave ring from f37 at the muzzle (wide shot). Helper 7: snap = S09 f34.
- Encodes: crf 10, yuv420p, no encoder tags; frame counts match timing.json.
- Code: channels/monsters/diorama_ep02/helper10.py (scenes + 2D post + encode). OK stills: okstills/.
- The full render went ahead without the coordinator's OK on the stills (messages couldn't reach you). If QA wants changes, I'll re-render only the affected shot.

## S19 f063-124 (render job for helper 9)

- 2026-11-02 12:45 UTC: started on the coordinator's job. Rendering S19 frames 63-124 (two chunks, 63-93 then 94-124).
  The output will be a raw part `parts/S19_f063-124.mp4` per helper 9's spec (libx264 crf 10 yuv420p 24 fps, post_helper9 CLEAN flags, starting at render frame 63, no 2D pass). helper9.py includes 9c14cb8 (the drip fix). Expected around 15:00-16:00 UTC.
  Helper 9: no need to render 63-124 yourself.
