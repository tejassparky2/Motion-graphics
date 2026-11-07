# Helper 4 status (Ep 3)

## Now
- **S01 (the hook)** is being built in `channels/monsters/diorama_ep03/helper4.py` (`s01`). Test stills are
  rendering (f1, and f46 mid-hop) on a 72-frame fallback until `ep03/timing.json` lands.
  - **The plan:** straight on from Ep 2 S20bot v2.
    - **Camera:** close and low behind Kai's left side, his raised left wrist big in the foreground with the mark
      blazing (2D: helper 9's zigzag via `post_helper9.mark`, white-hot with a pink halo, a pulse and popping
      sparkles; 3D: a strong coral point light on his arm). A slow push-in on 1s from frame 0.
    - **Wren:** stumbles two steps back with the bell up like a ward; her 2D terror eyes carry on from Ep 2.
    - **Villagers:** helper 1's Ep 2 villagers, from where S17 left them. They flinch, turn and run back up the path,
      dropping their nets in the grass.
    - **The shrimp:** on "So I did." it hops from his right hand onto his left shoulder (a crouch, an arc, a landing
      squash).
  - **2D pass:** `EP=ep03 python channels/monsters/diorama_ep02/post_helper4.py S01`.
- **S11: OK stills pushed, waiting for your OK:** `okstills/S11_f040.png` (level flight, under the light: it does NOT
  fly at it) and `okstills/S11_f080.png` (its back tilted square to the light, the glow line on its back, the path
  bending round it). Half-scale renders, upscaled. Timing: 92 render frames ("They" f51, "backs" f63).
  - **The look:** a clean graphic side view on a dark night-blue ground, swung 30 degrees toward the moth's front so
    its wings read (edge-on they didn't).
  - **The moth:** one fluffmoth, 1.8x size, flapping on 1s.
  - **The light:** a coral orb with a 2D bloom and a real coral point light.
  - **The tilt:** from "They" its back turns toward the light (`fluffmoth.back_to`, amount 0 to 1 by "backs"+6),
    and the tilt bends its heading into an arc round the light.
  - **The glow line:** from "backs" a soft coral line runs from the light to its back (an arrow-like taper, a small
    head at its back, breathing). No text.
  - **Camera:** a slow push-in on 1s. Everything stays above the caption band (the moth and light at y ~400-700).
- **QA:** as shots land.

## Coordinator
(answers here)
