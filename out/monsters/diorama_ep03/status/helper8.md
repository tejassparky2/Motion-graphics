# helper 8: Ep 3 assembly status

**Updated:** 7 Nov 2026, ~11:00 UTC (FINAL timing 8274b7a: 1298 frames, 54.09 s).

## Done and pushed
- **`assemble_ep01v2.py --version diorama_ep03`** is set up the way Episode 2's was (every setting is in the `*_VERSION` tables):
  - The inputs:
    - the shots from `out/monsters/diorama_ep03/shots/`, preferring the ESRGAN `shots_1080/`;
    - the timing from `channels/monsters/ep03/timing.json`;
    - the output at 1080x1920 to `out/monsters/diorama_ep03/picture.mp4`.
  - **Captions:** English, word-timed, 2-4 words each, on the 71% band (905) by default. They're placed per shot on the real frames as the shots land. S19 is at y 490, in the A half above the A card (at 520 the captions touched the card's top). S14, the flip, has no words.
  - **Frame-0 hook:** THE VILLAGE / RAN FROM / MY WRIST (MY WRIST in red), shown until line 1 ends. It starts high (y 170, size 96) and gets placed on S01's OK still or final.
  - **The A/B split on S19:** S19top.mp4 above, S19bot.mp4 below, with the jagged divider.
    - The cards are A · GO TONIGHT and B · LEAVE AT DAWN, at 85% size. A pops on "Option A", B on "Option B", and both pulse on "Comment".
    - LEAVE AT DAWN is 513 px wide from its centre at 85%, so B's centre has to stay at x ≤ 197.
    - **B card moved to (124, 880), placed on helper 5's S19bot OK still (f060/f124/f172).**
      - Kai's head, the shrimp and the look back fill the dawn panel's top, just under the divider. At y 715 the B card covered all three.
      - At 880 it sits over his waist, and his head, the shrimp and the look back stay clear. Its circle ends at y 951, above the Shorts UI line.
      - The two layouts side by side, 715 on the left and 880 on the right: `status/helper8_s19_cards.jpg`.
    - A stays at (124, 585), straddling the divider. It gets re-checked when helper 3's S19top still lands.
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

## The first animatic (pushed)
`out/monsters/diorama_ep03/picture.mp4` + `picture_sheet.jpg`, rebuilt on the FINAL timing (8274b7a):
- 1298 frames, 54.09 s, 1080x1920. All 19 shots are numbered slates showing each shot's line, and S19 is a split of two slates.
- **Frame 0 shows the hook.** In S19:
  - A pops on "Option A";
  - B pops on "Option B", with LEAVE AT DAWN fully in frame;
  - both pulse on "Comment".
- The edge scan is clean.
- Rebuild with `python channels/monsters/assemble_ep01v2.py --version diorama_ep03 --animatic --check`. Drop --animatic for the final.

## Next
- Then for each shot as it lands:
  - ESRGAN it to `shots_1080/`;
  - check its captions on the real frames, clear of faces;
  - rebuild the cut with placeholders;
  - push, and update this note.
- The hook gets placed on S01, the cards and captions on the S19 plates, and the cover frames get picked on the final renders.
