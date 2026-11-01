# Episode 2, 2.5D diorama: "I Saved the Shrimp That Tried to Kill Me" (owner, 1 Nov 2026)

**What the owner said:**
- The viewers voted A on Episode 1: "Most said to save the shrimp".
- The Episode 2 script is approved: "OK go ahead". The script is `channels/monsters/ep02/episode.py`; the outline is
  2A "SAVE" in out/monsters/story_v2.md.

**The same as Episode 1 v3:**
- the 2.5D diorama look: mk/diorama.py, the seed-31 island, the pond and the thorn tree where Ep 1 ended;
- Kai (mk/kai.py), the shrimp (mk/puffshrimp.py) and the butcher bird (mk/butcherbird.py);
- the light and grade (mk/grade.py) and the acting library (mk/acting.py);
- the 2D FX (fx2d, comp);
- the quality bar in DIORAMA_EP01_V3.md ("max"): key poses with anticipation and overshoot, characters on 2s, blinks
  every 2-4 s, a slow camera move on 1s in every shot, the subject above y 960 and clear of the caption band
  (845-930), phone-size readability;
- English captions and the frame-0 hook text (added at assembly).

**Hard rules for this episode:**
- **No graphic violence.**
  - The talons rake Kai's sleeve: a torn sleeve and three thin marks, no blood.
  - The bird is never killed: blasted into the thorn bush, dazed, stars, then fluffed up and offended.
- **Creatures are never evil.** Danger comes from nature.
- **Original designs only** (HELPERS.md "Hard rules"). Free/open-source and CC0 only, credited where asked.

## Files
- **Script and timing (FINAL, 57.34 s = 1376 frames):** `channels/monsters/ep02/episode.py`, `ep02/timing.json` and `TIMING.md` (voiced: Kai is
  Turbo am_liam as in Ep 1; Wren is her own Turbo voice). Every shot's frames and render_frames (= frames + 12)
  come from timing.json.
- **Builders:** `channels/monsters/diorama_ep02/<you>.py`, with `SHOTS = {"S05": build_s05, ...}`. They're
  registered automatically by `channels/monsters/diorama_ep02/shots.py` (module names: bgqrs, xprl, helper1,
  helper4, helper5, helper9, helper10). Reuse your diorama_v3 code; change staging, acting and frame counts.
- **Render:**
  `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S05 OUT [--frames A-B] [--still N --scale 0.5]`.
- **Outputs:**
  - `out/monsters/diorama_ep02/shots/<SHOT>.mp4` + `<SHOT>_sheet.jpg` (crf 10, bitexact, then a stream-copy remux;
    no Lavf/Lavc/x264 strings).
  - OK stills go to `out/monsters/diorama_ep02/okstills/`. Message the coordinator with the stills BEFORE the full
    render.
  - Parts go to `out/monsters/diorama_ep02/parts/<SHOT>_fAAA-BBB.mp4` (the chunk rule in HELPERS.md).

## Shots and who does them
| Shot | Line | Picture | Who |
|---|---|---|---|
| S01 | You said save it. So I ran at the butcher bird. | **Frame 0, the hook:** a medium-close, low shot; Kai sprinting at camera-left, hand out; behind him the bird already diving at the shrimp by the pond, its shadow on the grass. Moving from frame 0. | bGqrs |
| S02 | The bird dived first. | The bird folds its wings and drops (speed lines), its shadow growing over the tiny shrimp at the puddle. | helper 1 |
| S03 | I got there half a second sooner. | Kai slides in on his knees and scoops the shrimp up in cupped hands; water splash. | bGqrs |
| S04 | Its talons got my arm instead. | The talons rake past his forearm: the sleeve tears, three thin marks, NO blood. Kai winces and curls round the shrimp; the bird swoops up and away. | helper 1 |
| S05 | Now I was holding a wet pistol shrimp. In my bare hands. | Close on his cupped hands: the dripping claw resting against his palm, one drop falls; cut up to Kai's terror eyes and sweat drop. | helper 4 |
| S06 | But a pistol shrimp only fires one way. Straight ahead. | The claw in clean profile (graphic, light background); a quick 2D flash shows the jet going straight forward only, an arrow-like streak (no text). | helper 4 |
| S07 | So I turned it around. | Kai turns the shrimp between his fingers to face outward, careful as a bomb tech; the shrimp lets him, confused. | helper 5 |
| S08 | They don't call it a pistol shrimp for nothing. | Kai aims it in both hands like a pistol, a heroic low angle; behind, the bird wheels round for a second dive. | helper 10 |
| S09 | (the snap, no words) | The measured pattern: the shrimp's eye close-up; a held wind-up (0.5-1 s); SNAP: 1-3 white impact frames, a shockwave ring; the bird is blasted backward. | helper 10 |
| S10 | The bird landed in the thorn bush. | The bird stuck upside down in the thorn bush, dazed, little stars circling. | helper 10 |
| S11 | Alive. Just very, very fluffed. | The bird shakes itself free into a round puffball, glares, and stomps off offended. Hold it ~2 s (the laugh). | helper 5 |
| S12 | Then the shrimp looked at me. | It turns in his palm and raises its claw at his face: the frame-0 threat again. A second of tension. | helper 5 |
| S13 | And tapped my nose. | A tiny tap on his nose; Kai's stunned dot eyes, a held beat. | helper 5 |
| S14 | Something on my wrist started to glow. | Close on his wrist: a thin coral zigzag mark lights up, soft glow and sparkles. | helper 9 |
| S15 | The same shape as the crack in the sky. | Match cut: the zigzag mark, then the zigzag crack in the sky in the same screen position. Tilt up. | helper 9 |
| S16 | Then came the bells. | Bells ring (2D ring lines). Villagers with nets come over the hill, small and stylised. | helper 1 |
| S17 | A girl with a bell marched right up to me. | Wren (new) marches up, bell in hand, stern, and stops in front of Kai. | XprL |
| S18 | (Wren) Step away from the snapper. It goes in the lake. | Close on Wren speaking (mouth flaps); a villager's net is held ready behind her. | XprL |
| S19 | The lake. Deep water. Where a pistol shrimp never runs dry. | Kai looks past the village to a huge deep-blue lake; cut to the shrimp's claw dripping in his hand. | helper 9 |
| S20 | Option A: hand it over. Option B: hide it in my shirt. Comment A or B. | Split screen with a jagged divider. **Top (A):** Kai lowers the shrimp into Wren's net. **Bottom (B):** Kai slips the shrimp into his shirt as Wren turns away. The A/B letters (A · HAND OVER, B · HIDE) are added by the assembler. | XprL (top + Wren in bottom), helper 4 (bottom) |

## New assets
- **Wren** (XprL; push her first so others can stage around her): `mk/wren.py`.
  - A village bell-keeper girl, about Kai's age. Original design, clearly different from Kai: a hooded short cape,
    a satchel, and a hand bell on a cord.
  - The same toon look and outline as Kai, built from the same base model, Seed-san (VRM Public License 1.0: changes
    allowed; it's credited in the description). Change the colours, hair and outfit enough that she reads as her own
    person at phone size.
  - She needs: walk, stop, a stern face, speaking mouth flaps, and the bell ring.
- **Villagers, nets and bells** (helper 1): small stylised figures (or silhouettes) with long-handled nets, and hand
  bells.
- **The lake and the village** (helper 9): a big deep-blue lake past a small village on the island's edge.
- **The wrist mark** (helper 9): the coral zigzag, the same shape as the sky crack from Ep 1 (S09 of v3). Reuse
  helper 3's crack shape.

## The other passes
| Pass | Who | Deliverable |
|---|---|---|
| Sound | helper 7 | ep02 mix (ep01v3_sound.py's way):<br>- bird dive whoosh, talon swipe and cloth tear;<br>- the wet drip, the wind-up hush and THE SNAP with the shockwave;<br>- the thorn-bush crash, dazed tweets and the fluff "poomf";<br>- the nose-tap "tink", the wrist glow chime, the bells, Wren's steps, the lake ambience;<br>- A/B stingers.<br>Music drops under the snap (TWIST = l9). -14 LUFS, then Whisper medium.en. |
| Assembly | helper 8 | assemble_ep01v2.py's way, for ep02:<br>- English captions per shot;<br>- the hook text on frame 0: I SAVED THE SHRIMP THAT TRIED TO KILL ME;<br>- the A/B letters (A pops on "Option A", B on "Option B", both on "Comment A or B");<br>- the cover. |
| QA | helper 4 | Every shot against this brief and the script, plus the edge-band scan (no unpainted black at any frame edge). |
