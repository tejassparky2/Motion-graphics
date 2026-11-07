# Episode 3, 2.5D diorama: "They Rang Every Bell. The Moths Didn't Care" (owner, 7 Nov 2026)

**What the owner said:**
- The viewers voted B on Episode 2 ("Most said b continue with it"): Kai shows Wren the glowing mark.
- The Episode 3 script is approved ("Ok", 7 Nov). The script is `channels/monsters/ep03/episode.py`.

**Language: English only**, like Episode 2.

**The same as Episode 2** (DIORAMA_EP02.md):
- the 2.5D diorama look (mk/diorama.py, the seed-31 island, the village and the lake from Ep 2), the grade (mk/grade.py)
  and the acting library (mk/acting.py);
- Kai (mk/kai.py / hero), Wren (mk/wren.py), the shrimp (mk/puffshrimp.py), the villagers, nets and bells (helper 1's
  Ep 2 code), the wrist mark and the sky crack (helper 9's Ep 2 code: the mark is on the inside of Kai's LEFT
  forearm);
- the quality bar ("max" in DIORAMA_EP01_V3.md): key poses with anticipation and overshoot, characters on 2s, blinks
  every 2-4 s, a slow camera move on 1s in every shot, the subject above y 960 and clear of the caption band
  (845-930), phone-size readability;
- English captions, the frame-0 hook text and the A/B letters are added at assembly. No text in the picture.

**Continuity:**
- Ep 2 ended with Kai raising his left wrist, the coral zigzag mark flaring, and Wren stepping back with her bell up.
  S01 starts right there.
- **The shrimp rides on Kai's left shoulder** from S03 on (it climbs up in S01-S02). It's in every Kai shot.
- Kai's left sleeve is torn with three thin marks (Ep 2's talon scratch). No blood.
- From S04 it is dusk, from S05 on night: the island is dark blue, and **Kai's mark is the key light** (a coral point
  light at his wrist, brighter at night), plus a soft cool moon fill. Keep faces readable.

**Hard rules for this episode:**
- **No graphic violence.** The wing dust gives a small red itchy blotch (the villager scratches, comic, not gross).
- **Creatures are never evil.** The moths aren't attacking: they're pulled to the only light. Danger comes from
  nature. After the flip they're dazed, fine, waving their legs, and fly off later.
- **The physics is the payoff, so it has to read on screen:**
  - S10-S12: each moth flies with its BACK (top of the body, wings' upper side) tilted toward Kai's wrist. That tilt
    makes them orbit a light above them.
  - S13: Kai drops flat on his back and lays his left wrist on the ground, **mark facing the sky**, glowing up
    through the grass. The light is now BELOW the swarm.
  - S14: to keep their backs to the light, every moth rolls upside down, stalls and tumbles into the grass.
- **Original designs only** (HELPERS.md "Hard rules"). Free/open-source and CC0 only, credited where asked.

## Files
- **Script and timing:** `channels/monsters/ep03/episode.py`, `ep03/timing.json` and `TIMING.md`. Every shot's frames
  and render_frames (= frames + 12) come from timing.json. Voice in/out per shot is in TIMING.md.
- **Builders:** `channels/monsters/diorama_ep03/<you>.py` with `SHOTS = {"S05": build_s05, ...}`, registered
  automatically by `channels/monsters/diorama_ep03/shots.py` (module names: bgqrs, xprl, helper1, helper2, helper3,
  helper4, helper5, helper6, helper9, helper10). Reuse your diorama_ep02 code; change staging, acting and frame counts.
- **Render:**
  `blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S05 OUT [--frames A-B] [--still N --scale 0.5]`.
- **Outputs:**
  - `out/monsters/diorama_ep03/shots/<SHOT>.mp4` + `<SHOT>_sheet.jpg` (crf 10, bitexact, then a stream-copy remux; no
    Lavf/Lavc/x264 strings).
  - OK stills go to `out/monsters/diorama_ep03/okstills/`. Push them BEFORE the full render; the coordinator answers
    in your status file's "Coordinator" section (or by message).
  - Parts go to `out/monsters/diorama_ep03/parts/<SHOT>_fAAA-BBB.mp4` (the chunk rule in HELPERS.md).
- **Status:** every helper keeps `out/monsters/diorama_ep03/status/<you>.md` up to date (what's done, pushed, next, any
  blocker) and pushes it with each step. That's how the coordinator follows you: messages from helpers don't reach the
  coordinator session.

## Shared new pieces (push these first, others build on them)
| Piece | Who | What |
|---|---|---|
| Moth swarm + moth legs | helper 6 (fluffmoth author) | In `mk/fluffmoth.py` (yours): six short stubby legs (hidden in flight, shown upside down), an `upside_down` pose with legs waving on 2s, a cheap `swarm(n, ...)` (instanced/linked copies, wing beats offset, ~30-60 moths, small ones far away). Back-to-the-light flight: a helper that orients a moth so its back faces a given point. Push a still and a short test first. |
| Night grade + mark light + the lighthouse | helper 9 | Dusk and night versions of the island grade; Kai's wrist mark as a coral point light (brighter at night); a soft cool moon fill. The **old lighthouse**: a small ruined stone lighthouse on a rocky point across the lake, its top broken, a faint coral glow in the lamp room (the same coral as the mark). Push a still first. |
| Wren's new poses | XprL (Wren author) | Shield face with the cape (S07), ring hard with both hands (S08), lower the bell slowly (S16), kneel beside Kai (S17), lean in and whisper, then point across the lake (S18), sit in a rowing boat (S19 top). Faces: shocked, stern, softening, worried, whisper. |
| Villagers at night | helper 1 | Villagers backing off, doors and shutters closing, bells ringing on porches, one villager scratching a red blotch on the arm. Lantern-less (the mark is the only light). |

## Shots and who does them
| Shot | Line | Picture | Who |
|---|---|---|---|
| S01 | You said show her. So I did. | **Frame 0, the hook:** close, low: Kai's raised left wrist big in the foreground, the coral mark blazing (glow, sparkles); behind, Wren stumbling back with her bell up like a ward; villagers scattering, nets dropped. Moving from frame 0. The shrimp in his other hand, then hopping to his shoulder. | helper 4 (continues your S20bot v2) |
| S02 | (Wren) Marked. The sky cracked the night you fell. | Close on Wren speaking (mouth flaps), afraid but steady; she looks up. Cut/tilt up: the zigzag crack in the evening sky; then Kai looks up too: the same zigzag as his mark (a match of the two shapes). | helper 3 (+ Wren from mk/wren.py) |
| S03 | The whole village backed away from me. | Villagers retreat behind nets and doors, shutters bang shut; Kai left alone in the lane, the shrimp on his shoulder. | helper 1 |
| S04 | Then the sun went down. | A quick dusk: the sun sinks behind the hill, the sky goes orange to deep blue, the island darkens; his mark gets brighter. | helper 9 |
| S05 | And my wrist was the only light for miles. | High wide: the dark island and lake, one tiny coral dot in the village. Slow push-in. (The plant for the payoff.) | helper 9 |
| S06 | That's when the fluffmoths came down the hill. | A cloud of fluffmoths pours down the dark hillside toward camera; close on one: its wing eye-spots blink open. | helper 6 |
| S07 | Their wing dust stings like nettles. | Glittering wing dust drifts down; a villager scratches a red blotch on the arm (comic); Wren pulls her cape over her face. | helper 5 |
| S08 | (Wren) Ring the bells! Bells drive them off! | Wren on a porch rings her bell hard with both hands, shouting (mouth flaps); every bell in the village rings (2D ring lines). | XprL |
| S09 | The bells rang. The moths didn't even notice. | The bells ring; the swarm pours straight past the bell-ringers without a flinch, toward Kai. | helper 1 |
| S10 | They were circling my wrist. Round and round. | Top view: a spiral of moths circling Kai's raised left wrist, the light at the centre; the shrimp ducks. | helper 6 |
| S11 | Moths don't fly at a light. They keep their backs to it. | A clean, graphic side view on a dark background: ONE moth flying, its back tilting toward the glow (a soft 2D arrow-like glow line from the light to its back, no text). | helper 4 |
| S12 | So when the light is above them, they circle it. | The orbit, side-on: the light above, the moth's back tilted to it, so it curves round and round. | helper 10 |
| S13 | So I put the light below them. | Kai drops flat on his back in the grass and lays his left wrist on the ground, mark to the sky, glowing up through the grass; the swarm above him. Determined face. | bGqrs |
| S14 | (no words, the flip) | The swarm rolls upside down to keep their backs to the light, stalls, and tumbles into the grass: plop, plop, plop (little dust puffs, on 2s). A held beat of silence first. | helper 10 (render parts split) |
| S15 | Every single moth landed on its back. | Comic hold: a field of upside-down moths waving their little legs, eye-spots dizzy; Kai sits up among them. Hold ~2 s (the laugh). | helper 5 |
| S16 | Wren lowered her bell. | Wren slowly lowers her bell; her stern face cracks, eyes wide. | XprL |
| S17 | (Wren) The village wants you gone by sunrise. | Wren kneels by Kai, glancing back at the shuttered village (eyes in the window cracks). | XprL |
| S18 | (Wren) But the last marked one left something at the old lighthouse. | She leans in (a whisper), then points past him across the dark lake; cut to the ruined lighthouse on the rocky point, a faint coral glow at the top. | helper 9 (+ Wren poses from XprL) |
| S19 | Option A: go with Wren tonight. Option B: leave at sunrise, like they said. Comment A or B. | Split screen with a jagged divider. **Top (A):** Kai and Wren in a small rowing boat at night heading to the lighthouse, the mark lighting the water. **Bottom (B):** dawn, Kai walking away down the road out of the village, the shrimp on his shoulder, looking back. The letters (A · GO TONIGHT, B · LEAVE AT DAWN) come from the assembler. | helper 3 (top), helper 5 (bottom) |

**Render parts:** helper 2 and anyone who finishes early take render ranges of the long shots (S14, S06, S10, S15,
S18) from the shot owner, as on Ep 2. The owner splits the ranges in their status file; the coordinator joins them.

## The other passes
| Pass | Who | Deliverable |
|---|---|---|
| Sound | helper 7 | ep03 mix (`channels/monsters/ep03_sound.py`, ep02_sound.py's way):<br>- the mark flare and hum; Wren's stumble; villagers' steps, doors and shutters slamming;<br>- the dusk (birds settle, crickets), the night ambience;<br>- the swarm: a soft, fluffy wing flutter that grows; the wing dust glitter; a scratch;<br>- every bell in the village ringing, then still ringing as the moths pass;<br>- the orbit whoosh; Kai dropping into the grass;<br>- THE FLIP: a held hush, then plop, plop, plop (soft, comic), tiny dazed trills;<br>- Wren's bell lowered (a last small clink), her whisper (quieter and closer: Turbo has no real whisper), the lake lapping, the lighthouse glow chime;<br>- A/B stingers.<br>Music drops under the flip (TWIST = l14). -14 LUFS, then Whisper medium.en. |
| Assembly | helper 8 | assemble_ep01v2.py `--version diorama_ep03`:<br>- English captions per shot;<br>- the hook text on frame 0: THE VILLAGE RAN FROM MY WRIST;<br>- the A/B letters (A pops on "Option A", B on "Option B", both on "Comment A or B");<br>- the cover (Kai's glowing wrist and the swarm, or the upside-down moths). |
| QA | helper 4 | Every shot against this brief and the script, plus the edge-band scan (no unpainted black at any frame edge). The physics beats (S10-S14) must read at phone size. |
