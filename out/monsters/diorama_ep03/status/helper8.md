# helper 8: Ep 3 assembly status

**Updated:** 7 Nov 2026, ~09:40 UTC (branch at dce8b49+).

## Done and pushed
- **`assemble_ep01v2.py --version diorama_ep03`** is set up the way Episode 2's was (every setting is in the `*_VERSION` tables):
  - The inputs:
    - the shots from `out/monsters/diorama_ep03/shots/`, preferring the ESRGAN `shots_1080/`;
    - the timing from `channels/monsters/ep03/timing.json`;
    - the output at 1080x1920 to `out/monsters/diorama_ep03/picture.mp4`.
  - **Captions:** English, word-timed, 2-4 words each, on the 71% band (905) by default. They're placed per shot on the real frames as the shots land. S19 starts at y 520, in the A half above the divider. S14, the flip, has no words.
  - **Frame-0 hook:** THE VILLAGE / RAN FROM / MY WRIST (MY WRIST in red), shown until line 1 ends. It starts high (y 170, size 96) and gets placed on S01's OK still or final.
  - **The A/B split on S19:** S19top.mp4 above, S19bot.mp4 below, with the jagged divider.
    - The cards are A · GO TONIGHT and B · LEAVE AT DAWN, at 85% size. A pops on "Option A", B on "Option B", and both pulse on "Comment".
    - LEAVE AT DAWN is 513 px wide from its centre at 85%, so B's centre has to stay at x ≤ 197.
    - Both cards start at x 124, straddling the divider (A at y 585, B at 715). They get re-placed on the S19 plates.
  - **Edge-band scan:** the same rule as Episode 2.
  - Regression check: Episode 2 still rebuilds byte-identical (sha 4926290880f2).
- **`deliver_ep01v2.py --version diorama_ep03`** writes the final files for Episode 3:
  - the inputs:
    - EPDIR is `ep03`, which supplies episode.py's METADATA and the timing;
    - the picture is `out/monsters/diorama_ep03/picture.mp4`;
    - the mix is `out/monsters/ep03/mix.wav`;
    - the cover is `out/monsters/diorama_ep03/cover.jpg`;
  - the outputs: `out/monsters/ep03_diorama.mp4`, the preview, the cover, the upload sheet headed "Episode 3", and the check (frames, tags, Whisper medium.en).
- **Cover:** `python channels/monsters/ep01v2_cover.py --ep03` makes the candidates, a phone grid and `cover.jpg`. The frames are placeholders until the shots land.
  - **swarm (the pick):** S10, THEY CIRCLED / MY WRIST. It's the top view of the spiral round his glowing wrist.
  - **flip:** S15, EVERY MOTH / FLIPPED. It's the field of upside-down moths.
  - **hook:** S01, THE VILLAGE / RAN.

  None of them repeats the title.

## Next
- When `ep03/timing.json` lands: build the first animatic with every shot as a numbered slate, and push it.
- Then for each shot as it lands:
  - ESRGAN it to `shots_1080/`;
  - check its captions on the real frames, clear of faces;
  - rebuild the cut with placeholders;
  - push, and update this note.
- The hook gets placed on S01, the cards and captions on the S19 plates, and the cover frames get picked on the final renders.
