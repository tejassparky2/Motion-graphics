# XprL status: Episode 3 (Wren's new poses, S08, S16, S17)

## Coordinator
(Your answers go here.)

## Done
**7 Nov, 09:22 UTC: Wren's Episode 3 poses and faces are pushed in `channels/monsters/mk/wren.py`.**
- **OK stills:** `okstills/xprl_wren_poses.png` and `okstills/xprl_wren_faces.png`. The test that makes them is
  `channels/monsters/test_wren_ep03.py`.
- **How to use the poses:** every pose takes a reset `ep01v2.xprl.Pose` (`P`) in her armature space (she faces -Y,
  her left is +X). Stack poses, then `P.key(f)`. Fingers and the cape drape are keyed on the rig.

| Shot | Call | Notes |
|---|---|---|
| S07 | `wren.shield(P, t)` + `wren.cape_up(w, f)` | Her left forearm comes across her face and the cape edge drapes over it. Her head ducks and turns to her right. `cape_up(w, f, False)` hides the drape again. |
| S08 | `wren.ring_hard(P, shake=-1/0/1, lift)` | Both hands on the bell at her right shoulder, face clear. Alternate `shake` on 2s. Pair with `wren.ring(w, f0, f1, swing=40, beat=4)` and face "shout". Also key `wren.grip(w, f)` and `wren.grip(w, f, side="L")`. |
| S16 | `wren.lower_bell(P, t)` | t 0 = bell held up, t 1 = bell at her side. Eased, with the shoulders and head dropping. |
| S17 | `wren.kneel(P, front="L", depth)` | Down on one knee with the left foot ahead and the right knee on the grass. The bell hand hangs by her knee, the left hand rests on her front knee. `depth` 0..1 blends from standing. |
| S18 | `wren.kneel(P)` then `wren.whisper(P, t, toward=dir)`, then `wren.point(P, direction, t)` + `wren.point_fingers(w, f)` | Whisper leans in with her left hand cupped at her mouth. Point uses her left arm with the index finger out. |
| S19 top | `wren.sit(P, seat=0.42, feet_y=-0.36)` | Sitting on a thwart `seat` high, feet forward, the bell in her lap, the left hand on her knee. |

- **Faces** (`wren.face(w, name, f)`): `stern`, `shout`, `shocked`, `softening` (the stern face cracks, eyes wide),
  `worried`, `whisper`, plus `stern_open`, `softer` and the hero faces. Use `wren.talk_words` for lip sync from
  timing.json words.
- **Brows:** her bangs hide the brow keys, so the faces work through the eyes and mouth. They read in close and medium
  shots.

**7 Nov, 12:20 UTC: OK stills for S08, S16 and S17 are pushed** (half scale, on helper 9's final night grade and mark
light, 09d120f). Builder: `channels/monsters/diorama_ep03/xprl.py`.
- `okstills/xprl_S08_f030.png`: Wren on the porch of helper 1's hut 2, ringing hard with both hands and shouting.
  The other porch bells join in one by one. Kai's mark is off-screen down the lane as the coral key light. A low 3/4
  camera with a slow push-in.
- `okstills/xprl_S16_f028.png`: close on Wren as the bell comes down. Her stern face cracks on "bell" (`softening`).
  The upside-down moths are at her feet and the shut huts behind her.
- `okstills/xprl_S17_f016.png` and `xprl_S17_f044.png`: she steps in and kneels at Kai's front-right on the village
  side. Kai sits up where helper 5's S15 leaves him (hips (9.0, -140), facing east, mark up, the shrimp on his left
  shoulder at 0.6). On "village" she glances back over her shoulder at the shuttered huts (helper 1's `peek` eyes in
  the cracks), then turns back to him, worried. Shot over Kai's left shoulder from the north.
- **Full renders start now:** S08 1-80, S16 1-55, S17 1-70 (render_frames from the final timing), one Blender here,
  as 15-frame raw parts in `parts/`.
- **Speed:** about 100 s a frame at full size, so around 6 h for all 205 frames. **Helper 2, or anyone free:** take S17
  f036-070, and write it here before you start. Same spec: crf 6, yuv444p, clean.

## Next
- Join each shot from its parts (`join_parts.py`), push `shots/<SHOT>.mp4` with its sheet, and note it here.
