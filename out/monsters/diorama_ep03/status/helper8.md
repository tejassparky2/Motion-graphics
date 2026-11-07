# helper 8: Ep 3 assembly status

**For the coordinator (7 Nov ~11:25 UTC): I can't take the S14 render part (part 2, f022-042).**
- This session has no Blender (`which blender` finds nothing).
- Installing or running Blender was blocked by this session's permissions back on Episode 1, and I'm not working around that.
- Part 2 is still free in `status/helper10.md`, with a note saying so. Please give it to a helper who has Blender.
- Everything on the assembly side keeps going: ESRGAN, captions and cut rebuilds as the shots land.


**Updated:** 7 Nov 2026, ~13:25 UTC (FINAL timing 8274b7a: 1298 frames, 54.09 s).

## Done and pushed
- **`assemble_ep01v2.py --version diorama_ep03`** is set up the way Episode 2's was (every setting is in the `*_VERSION` tables):
  - The inputs:
    - the shots from `out/monsters/diorama_ep03/shots/`, preferring the ESRGAN `shots_1080/`;
    - the timing from `channels/monsters/ep03/timing.json`;
    - the output at 1080x1920 to `out/monsters/diorama_ep03/picture.mp4`.
  - **Captions:** English, word-timed, 2-4 words each, on the 71% band (905) by default. They're placed per shot on the real frames as the shots land. S19 is at y 430, in the A half above the stacked cards. S14, the flip, has no words.
  - **Frame-0 hook:** THE VILLAGE / RAN FROM / MY WRIST (MY WRIST in red), shown until line 1 ends.
    - **Re-placed on the re-staged S01 (helper 4's OK stills f1, f30, a1925681):** at the top, centred at x 345, size 84, lines at y 120/206/292.
      - That's open sky above Kai's raised hand (fingertips at ~350), clear of his face and the blazing mark. It stays left of Wren's braid at the right edge.
      - **S01 captions move to y 760, on his chest.** At the 71% band, "You said show her" crossed the shrimp's face in his lower hand. At 760 they're clear of his face and the shrimp, both in his hand (f1) and on his shoulder (f30).
      - Test frames (f0, f20, f40): `status/helper8_s01_hook.jpg`.
  - **The A/B split on S19:** S19top.mp4 above, S19bot.mp4 below, with the jagged divider.
    - The cards are A · GO TONIGHT and B · LEAVE AT DAWN, at 85% size. A pops on "Option A", B on "Option B", and both pulse on "Comment".
    - LEAVE AT DAWN is 513 px wide from its centre at 85%, so B's centre has to stay at x ≤ 197.
    - **Re-placed on helper 5's S19bot v2 still (beach road into the sunrise; f030/f122/f170): A at (124, 515), B at (124, 655). The S19 captions move to y 430.**
      - Kai's whole body is at screen y ~716-1040, from the shrimp's tip to his feet.
      - The cards stack on the divider: A just above it, B in the dawn sky just under it. B clears his head, the shrimp and the look back, and only the end of its pill crosses the sun's edge.
      - The other layout I tried put B low, at 880, where it covered his waist and hands.
      - Both layouts side by side, 880 on the left and the pick on the right: `status/helper8_s19_cards.jpg`.
      - **Checked on helper 3's S19top OK stills (f40, f120) together with S19bot v2:** `status/helper8_s19_split.jpg`.
        - The A card sits on the water under the boat's glow, clear of Kai, Wren and the shrimp.
        - The captions at y 430 sit on the hull's glow under the characters. At y 160 they covered Kai's head.
        - Cards and captions stay where they are.
      - **Two things for helper 3's render (also noted in status/helper3.md):**
        1. S19top is rendered to row 690, but the split's top band needs rows 0-800. On the stills the short render leaves a black sliver at the left edge above the divider, which fails the edge scan.
        2. The lighthouse's lamp is at about plate row 40, inside the 60 px the split hides at the top. It should sit below row ~110.
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

## Shots in the cut (ESRGAN 1080 in `shots_1080/`, captions checked on the real frames)
| Shot | From | ESRGAN | Captions |
|---|---|---|---|
| S06 | helper 6 (63 f) | done | 905: under the close-up moth's face and the mushrooms; it only brushes a few small far moths in the pour |
| S11 | helper 4 (1532847e, 92 f) | done | 905: under the moth and the light, clear of its face and the glow line |
| S12 | helper 10 (7ac5713b, 79 f) | done | 905: under the orbit, clear of the moth and the light |
| S13 | bGqrs (9fdf70df, 57 f) | done (two halves) | 905: on the grass below Kai, clear of his face, the wrist glow and the swarm |
| S14 | helper 10 (ef0558dc, 84 f) | done | none (the flip has no words). It reads at phone size: the swarm rolls over above the uplight and tumbles into the grass |

The picture is rebuilt with every other shot slated: 1298 frames, edge scan clean.

## Next
- Then for each shot as it lands:
  - ESRGAN it to `shots_1080/`;
  - check its captions on the real frames, clear of faces;
  - rebuild the cut with placeholders;
  - push, and update this note.
- Re-check the hook and the S01 captions on the S01 final. The A card and captions get placed on helper 3's S19top still, and B on helper 5's reframed S19bot. The cover frames get picked on the final renders.
- **S15 captions move to y 300, from helper 5's OK still (f20/f50/f90).** That puts them in the dark sky over the trees, above Kai's cap (~480). At the 71% band they'd cross the upside-down moths' faces in the foreground, which is the laugh.
- The S10 OK still (f40) is checked: the 71% captions fall on moths, not on Kai, and the swarm cover frame works, with Kai below the cover words.
