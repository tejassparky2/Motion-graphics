# helper 8: Ep 3 assembly status

**Updated:** 7 Nov 2026, ~11:40 UTC (FINAL timing 8274b7a: 1298 frames, 54.09 s).

## Done and pushed
- **`assemble_ep01v2.py --version diorama_ep03`** is set up the way Episode 2's was (every setting is in the `*_VERSION` tables):
  - The inputs:
    - the shots from `out/monsters/diorama_ep03/shots/`, preferring the ESRGAN `shots_1080/`;
    - the timing from `channels/monsters/ep03/timing.json`;
    - the output at 1080x1920 to `out/monsters/diorama_ep03/picture.mp4`.
  - **Captions:** English, word-timed, 2-4 words each, on the 71% band (905) by default. They're placed per shot on the real frames as the shots land. S19 is at y 430, in the A half above the stacked cards. S14, the flip, has no words.
  - **Frame-0 hook:** THE VILLAGE / RAN FROM / MY WRIST (MY WRIST in red), shown until line 1 ends.
    - **To redo: S01 is being re-staged (coordinator, 7 Nov ~10:52).** The new camera is low over Wren's shoulder, looking up at Kai's face and his raised wrist, with little sky. I'll re-place the hook on helper 4's next OK stills: still at the top, clear of his face and the mark. The placement below was for the old stills.
    - **Placed on helper 4's S01 OK stills (f1, f36):** in the open sky top left, centred at x 255, size 76, lines at y 200/278/355. That puts the text at about x 15-495, y 150-365.
    - Kai's head and the shrimp on his shoulder come in from the top right (x 530+), and his glowing arm crosses at y 560-650. The hook stays clear of all three, so the blazing wrist is the frame's focus.
    - Both stills with the hook: `status/helper8_s01_hook.jpg`. The assembler has a new per-version hook x for this.
  - **The A/B split on S19:** S19top.mp4 above, S19bot.mp4 below, with the jagged divider.
    - The cards are A · GO TONIGHT and B · LEAVE AT DAWN, at 85% size. A pops on "Option A", B on "Option B", and both pulse on "Comment".
    - LEAVE AT DAWN is 513 px wide from its centre at 85%, so B's centre has to stay at x ≤ 197.
    - **Re-placed on helper 5's S19bot v2 still (beach road into the sunrise; f030/f122/f170): A at (124, 515), B at (124, 655). The S19 captions move to y 430.**
      - Kai's whole body is at screen y ~716-1040, from the shrimp's tip to his feet.
      - The cards stack on the divider: A just above it, B in the dawn sky just under it. B clears his head, the shrimp and the look back, and only the end of its pill crosses the sun's edge.
      - The other layout I tried put B low, at 880, where it covered his waist and hands.
      - Both layouts side by side, 880 on the left and the pick on the right: `status/helper8_s19_cards.jpg`.
      - A at 515 sits on the bottom of the boat panel. It gets re-checked when helper 3's S19top still lands.
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
- Re-check the hook on the S01 final. The A card and captions get placed on helper 3's S19top still, and B on helper 5's reframed S19bot. The cover frames get picked on the final renders.
- The S10 OK still (f40) is checked: the 71% captions fall on moths, not on Kai, and the swarm cover frame works, with Kai below the cover words.
