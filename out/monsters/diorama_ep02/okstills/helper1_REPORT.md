# Helper 1, ep02: S02 / S04 / S16 OK stills (for the coordinator)

Sheet: `helper1_S02_S04_S16_ok.jpg` (PNGs beside it). Code: `channels/monsters/diorama_ep02/helper1.py` + `post_helper1.py`.

- **S02** "The bird dived first." (f30)
  - Side-on from the south-east, the pond on the left.
  - It uses bGqrs's shared dive line from the thorn perch, from 0.74 (where S01 ends) to 0.95.
  - The bird is in the dark form with the rage light. Its wings flare, then snap shut at f10; it holds its height a moment, then drops steeply onto the drinking shrimp.
  - 2D speed lines stream behind it, and its giant shadow spreads over the shrimp, whose eyes pin.
- **S04** "Its talons got my arm instead." (f14, f40)
  - Kai starts in bGqrs's exact S03 end pose and glances up and back.
  - The talons rake his left forearm at f13: a 2D three-streak slash and a ">_<" wince.
  - Then three thin pink scratch marks and a frayed wristband nick, no blood.
  - Kai has **short sleeves**, so "the sleeve tears" became the wristband plus marks on the bare forearm.
  - He curls round the shrimp, trembling, with a sweat drop, while the bird climbs away out of frame top-right.
- **S16** "Then came the bells." (f30)
  - Over Kai's right shoulder, down the south path.
  - Seven small stylised villagers in cloaks and wide hats, with long nets, come up over a grassy rise; three ring hand bells with 2D ring arcs.
  - The rise is `helper1.hill()`. I asked XprL to call it in S17/S18.

The full renders are running now (~45 s/frame, 158 frames). I'll re-render on any change.

## Final renders (2 Nov, commit 3d28621)
- out/monsters/diorama_ep02/shots/S02.mp4 (45 f), S04.mp4 (66 f), S16.mp4 (47 f), each with a _sheet.jpg.
- 720x1280, 24 fps, crf 10; Lavf/Lavc/x264/encoder tags 0; cropdetect full frame (no black edges).
- Render time per frame: S02 ~51 s, S04 ~56 s, S16 ~86 s (S16 ran in parallel with S02/S04).
- Still weak: S02 the bird stays in the upper right and only drops near the end, and the shrimp is small;
  S04 the three scratch marks are small at phone size and Kai's face is hidden under his cap once he curls;
  S16 blurred foreground stumps and Kai's cap fill the bottom half, and the hill reads as a flat rise.
