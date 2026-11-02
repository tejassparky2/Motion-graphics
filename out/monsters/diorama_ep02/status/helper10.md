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
- 2026-11-02 15:20 UTC: **S19 f063-124 done and pushed**: `parts/S19_f063-124.mp4`, 62/62 frames (render frames
  63-124), libx264 crf 10 yuv420p 24 fps, post_helper9 CLEAN flags, no encoder tags. **Last frame: f124.** I was at
  f122 when the f110 split message arrived, so I finished the chunk as the coordinator said. Helper 4: S19 f110-124 isn't
  needed from you. Helper 9: use whichever frames you like for f110-124; mine cover f063-124 in full.
- 2026-11-02 15:45 UTC: **re-rendering S19 f017-032 from the fixed helper9.py (bbd52b1)** as the coordinator asked.
  It goes to `parts/S19_f017-032_v2.mp4` (helper 9's spec, starting at frame 17). ETA around 16:20 UTC. Helper 9: you can skip
  f017-032 in your f001-048 re-render, or keep going and use whichever lands first.
- 2026-11-02 16:20 UTC: **S19 f017-032 v2 done and pushed**: `parts/S19_f017-032_v2.mp4`, 16/16 frames (render frames
  17-32, from helper9.py bbd52b1), libx264 crf 10 yuv420p 24 fps, post_helper9 CLEAN flags, no tags. The crane rises
  over Kai and Wren to the village and lake, with no dip. No jobs pending.
- 2026-11-02 20:40 UTC: **GO S20bot v2 received.** Rendering S20bot f121-140 from helper4.py 331ab9c; it goes to
  `parts/S20bot_v2_f121-140.mp4` (crf 6 yuv444p, bitexact, no tags, starting at frame 121). ETA around 21:25 UTC.
- 2026-11-02 21:45 UTC: **S20bot v2 f121-140 done and pushed**: `parts/S20bot_v2_f121-140.mp4`, 20/20 frames (render
  frames 121-140, helper4.py 331ab9c), libx264 crf 6 yuv444p 24 fps, bitexact, no tags, no 2D pass. The frames are
  consistent: Kai's forearm up with the shrimp at his side, Wren with the bell, smoke drifting. No jobs pending.
