# Episode 1 (v2, APPROVED by the owner 30 Oct 2026): shot list and who builds what

Script: `out/monsters/story_v2.md`. Rules: `reports/Pokémon episodes story and animation.md`. Every shot obeys the
rules cited in its row. **Pure anime: no HUD, no text in the picture.** Captions and the frame-0 hook text are added by
the coordinator.

**Timing:** the seconds below are ESTIMATES until the voice is done (TP2). Render each shot with a 12-frame tail
handle; the coordinator sends exact frame counts once the takes are measured, and trims or holds in the edit.
24 fps, 720x1280.

## Look and timing rules for every shot (the report's numbers)
- **Cut lengths (SG1):** talk/feeling 1.5-2.5 s per shot, with a pose or face change inside each (SG2); action
  0.8-1.5 s; finishers 0.3-0.8 s; comedy is the gag 1-2 s, then a 1.5-3 s held reaction (SU11).
- **Camera (SG4/SG5):** mostly locked. Slow push-ins only for threat, decision or emotion, and ≤10% push-ins are done
  later as 2D zooms (TP13). Vertical moves (tilts, dives) suit 9:16.
- **Timing (IM2):** characters on 3s for acting, 2s for action. The camera and effects stay on 1s.
- **Render only changed frames:** a shot's builder returns `step` (3 or 2) when the camera is locked and no
  1s-effects run. render_shot.py then renders every Nth frame and copies it.
- **Every power uses the 9-step hit (IM1):**
  1. the observation;
  2. an eye close-up of 2-5 frames;
  3. a held wind-up of 12-29 frames, where only the effect grows;
  4. a strike of 2-4 frames;
  5. a flash of 1-3 frames;
  6. impact frames of 2-6 frames on 2s, inverted or abstract;
  7. the result held 24-48 frames;
  8. the target's reaction, 12-20 frames;
  9. the observer's reaction, shaken on 2s, decaying from ~30% to ~1% of the frame width over ~0.6 s (IM5).
- **Light (LC):**
  - Earth lab: cold blue. Fear is darkness, not a hue shift (LC2).
  - The new world: bright day.
  - Cute to deadly: local light on the creature (a top shadow, glowing eyes), never a regrade of the frame (LC4,
    TP11).
  - Power and bond moments: one series hue, coral-white.
  - Mean saturation 0.34-0.61 (LC9). Calm shots stay alive with ambient sparkles or motes (LC10).
- **Sound:** handled by the coordinator. For reference: silence ~1 s before the snap (SS2).
- **The hero:** `mk/hero.py`. On Earth he wears his "earth" outfit (grey shirt look); in the new world, the sage
  tunic. Faces are the VRM expression shape keys. For comic faces (sweat drop, dot eyes) use the pycairo kit (TP7),
  never a redrawn model.

## Shots

| Shot | Line | Est. s | Picture (and the rule it serves) | Builder |
|---|---|---|---|---|
| S01 | 1 Don't move. That claw can boil water. | 2.7 | FRAME 0. Close, from above at ~60°: Kai on his back in pink-tinted grass, eyes wide. The puff-shrimp sits on his chest, claw cocked 2-3 cm from his nose. At the top of the frame, sliced trees with glowing orange cuts, smoke (ST1, EP4). Kai's mouth whispers (aa/oh on 3s). Locked; step 3 except smoke. | bGqrs |
| S02 | 2 Ten minutes ago, I was alive. | 2.4 | S01 runs backwards under the glitch rewind (comp.glitch_rewind). | coordinator |
| S03a | 3 (first half) | 1.8 | Earth lab, night, rain on the window. Kai (earth outfit) at the desk beside the glowing hero tank, back three-quarter. Cold blue (LC1). | helper 1 |
| S03b | 3 (second half) | 2.0 | Close: Kai's face lit cyan by the tank, a small fond smile, looking at the shrimp (SG2: one face change). | helper 1 |
| S04 | 4 Its claw snaps so fast, the water boils. | 2.6 | Slow-motion snap, extreme close: claw open (held), shut, the white-hot bubble swelling (IM13 scale). | helper 2 |
| S05a | 5 (first half) | 2.0 | The bubble glowing at its peak, then collapsing to micro-bubbles. | helper 2 |
| S05b | 5 (second half: "But only in water.") | 2.0 | Kai's face, the flash light fading on it; he taps the glass with one finger (BD2 seed). | helper 1 |
| S06 | 6 Then the storm hit. | 1.5 | The window: lightning (2-frame flashes), the room lights stutter (storm.py with lab handles). | helper 9 |
| S07 | 7 Snap. | 1.0 | The shrimp snaps; a crack runs up the tank glass in 5 frames; impact frame 2f. | helper 2 |
| S08 | 8 Water. Cables. Me. | 2.2 | Floor level: water runs to the power strip (0.8 s), a spark (0.6 s), black (0.8 s). Nothing graphic. | helper 9 |
| S09 | 9 I woke up under a cracked sky. | 2.3 | White blooms to a pastel sky with a hairline crack (the SAME zigzag as the tank crack; copy the crack path from pistolshrimp.crack), then the camera tilts down (SG5) to Kai (world outfit) blinking in pink grass. | helper 3 |
| S10a | 10 (first half) | 1.3 | Jelly-snail, close, cute held pose, one bob. | helper 4 |
| S10b | 10 (second half) | 1.4 | Fluffmoth, close, hover. | helper 6 |
| S11a | 11 (first half) | 1.0 | The jelly-snail's trail: smoking burnt holes in the grass (the wrong detail, EP4). | helper 4 |
| S11b | 11 (second half) | 1.1 | The moth's wing eye-spots open and look at the camera. | helper 6 |
| S12 | 12 I was so thirsty. | 1.5 | Kai crawls on hands and knees toward a puddle, low side view. | helper 9 |
| S13 | 13 Something else was already drinking. | 2.5 | The puff-shrimp at the puddle, claw dipped in the water (insert of the clue, SG10, CH3). | helper 9 |
| S14 | 14 A shrimp. On land. Impossible. | 2.5 | Kai's sceptical face, two-step expression change (SG2). | helper 9 |
| S15 | (no words) | 4.0 | THE SNAP:<br>1. Kai's hand reaches into frame (observation);<br>2. eye close-up of the shrimp (3f);<br>3. the claw rises dripping, held while the drops fall (silence);<br>4-6. SNAP: a 2f flash, impact frames on 2s (comp.impact with the subject pass), a white ring;<br>7. the trees behind sliced and erased into dust (erase.py), held;<br>8. Kai blown backwards;<br>9. observer shake on 2s.<br>Meadow "before" set. | helper 10 |
| S16 | 16 When I opened my eyes, it was on my chest. | 2.8 | Kai's eyes open (eye close-up), then S01's framing (SU9 rhyme). | bGqrs |
| S17 | 17 Then I saw the drops. | 1.6 | Insert: a drop falls from the claw tip onto his tunic (CH3, second showing of the clue). | bGqrs |
| S18 | 18 Its claw only works wet. | 1.8 | Extreme close-up of Kai's eyes narrowing; realisation background (SU16, IM6). | bGqrs |
| S19 | 19 So I didn't move. I let the sun dry it. | 4.1 | One held, quiet shot (SG14): sun glare, a sweat bead (comic kit), the last drop on the claw tip shrinking away. A ≤10% 2D push. | bGqrs |
| S20 | 20 It tried anyway. | 3.5 | Snap: just a tiny "pff" of dust. The shrimp stares at its claw and tilts its head (CH14). Cut to Kai's deadpan face held 2 s (SU11). | bGqrs |
| S21 | 21 Then it stomped back to the puddle. | 2.2 | Low angle: Kai lying in the foreground, the shrimp hops off in a huff toward the puddle (SU12 gag). | bGqrs |
| S22 | 22 That's when I saw the thorn tree. | 2.2 | Reveal by scale (SU2): tiny shells skewered on thorns, then a tilt up the thorn bush beside the puddle. | helper 5 |
| S23 | 23 A butcher bird hangs its food on thorns. | 2.6 | A small fluffy bird lands on top, filmed from below looking down (SU4). Insert: one empty thorn, shrimp-sized. | helper 5 |
| S24 | 24 Save the shrimp that tried to kill me, or run while I can? | 3.5 | Split screen (AB13; divider by the coordinator). Render two plates: TOP Kai steps toward the shrimp at the puddle, its claw wet again; BOTTOM Kai backs toward the trees as the bird drops. Grade the riskier option darker (LC8). | XprL (after the voice) |

## Delivery (every builder)
- **Code:** `channels/monsters/ep01v2/<your_name>.py` with `SHOTS = {"S03a": fn, ...}`. Each fn builds its scene and
  returns `dict(frames=N, step=1|2|3, subject=[roots])`.
- **Render:** `blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S03a OUTDIR`. For Kai, see
  `channels/monsters/mk/hero.py`.
- **Composite your own 2D effects** with `comp.py`/`fx2d.py`/`fx2d_extra.py`: impact frames, speed lines, sweat drops.
  No text, no HUD.
- **Deliver:**
  - `out/monsters/ep01v2/shots/<SHOT>.mp4`, made with
    `ffmpeg -framerate 24 -i %04d.png -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p`;
  - `out/monsters/ep01v2/shots/<SHOT>_sheet.jpg`: a contact sheet of every 6th frame.
- **Before pushing, LOOK at every rendered frame** and compare it with the reference measurements in the report
  (TP3).
- **Report to the coordinator:** shot names, commit, sec/frame, anything weak.

## Who to message (send_message session IDs)
| Builder | Shots / job | Session |
|---|---|---|
| coordinator | S02, final cut, delivery | session_0153qDV4AufFgT2PhEBEfS8n |
| bGqrs | S01, S16-S21 | session_01PF511bGqrs1SFn3cpk5NqS |
| helper 1 | S03a, S03b, S05b | session_01PF511bDdsYwHy141n4jcnn |
| helper 2 | S04, S05a, S07 | session_01PF511Y13zuEX6TW3egNyxM |
| helper 3 | S09 | session_01PF511b6tpL8dByjU7Qp3Tu |
| helper 4 | S10a, S11a; QA reviewer (out/monsters/ep01v2/QA.md) | session_01PF511YEojWTNPFKxSeURms |
| helper 5 | S22, S23; butcher bird, thorn bush | session_01PF511ahSS4W8tEQ9ukoLwF |
| helper 6 | S10b, S11b | session_01PF511Y382fBtBJa7rzyVDQ |
| helper 7 | sound mix (ep01v2_sound.py) | session_01PF511bWPhLFvpRbgd3zffg |
| helper 8 | picture assembly (assemble_ep01v2.py), fx2d_anime | session_01PF511Yk7bwbspWweS95hGA |
| helper 9 | S06, S08, S12, S13, S14 | session_01PF511ZFaQeq2RigHZ22DrB |
| helper 10 | S15 | session_01PF511YTmbSi3KeLNnX6GyZ |
| XprL (render helper) | voice (done), S24 plates | session_01PF511XprLcpVNCdEQUsUFF |

Exact lengths: `channels/monsters/ep01v2/TIMING.md` (wins over the estimates above).
