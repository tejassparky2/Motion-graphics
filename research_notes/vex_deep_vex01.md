# Vex ep. 1 "Never Let a Vampire Bite a Pufferfish": frame-by-frame measurement (5 Nov 2026)

File measured: `out/vex01_pufferfish.mp4`: H.264 High 720x1280, 30 fps, 1158 frames (last frame n=1157 at 38.567 s),
5.6 Mb/s video; AAC 44.1 kHz stereo (dual mono, L/R correlation 0.9998), 130 kb/s; duration 38.60 s.
8 I-frames (n=0, 250, 290, 540, 579, 829, 868, ...), 294 P, 856 B.

How it was measured: real frames (6 fps contact sheets, full-res stills, all 1158 frames decoded at half-res for
change counts, the last 90 frames at full res); the source photo re-rendered with the scene's own push-in and
subtracted from the frames (overlay masks, grain, zoom fit); the scene's `draw()` run for all 1158 frames with Vex's
pose arguments logged and his body drawn alone (exact height, position, pose and lip-sync per frame); the audio
(`audio.wav`, the stereo AAC decoded again for loudness), RMS at 10/20/100 ms, the f0 tool, Welch spectra.
Beat times come from the render's cached timeline (`motion/timeline.py`). They match the Whisper word times to
within about 0.1 s. Times are in seconds; px are at 720x1280 unless noted.

---

## 1. Shot and camera

| Item | Measurement |
|---|---|
| Source | One still phone photo (`assets/mascot/photos/crops/close_living.png`, 720x1280). Template match: it is an 850x1511 px window (x0 331, y0 255) of the 1500x2000 resized original `floor_living.jpg` (NCC 0.80), i.e. 56.7% of the original's width and 75.6% of its height, downscaled 0.847x. |
| Video or still | Still. The background matches the still photo in every sampled frame (mean abs error 2.0-3.1 levels, which is grain plus compression). Nothing in the room moves. |
| Cuts | 0. The biggest frame-to-frame change is 9.1% of pixels (n=940, 31.33 s, Vex's pose pop), far below a cut. |
| Push-in | Linear digital zoom about the point (380, 700), from 1.000 to 1.0386 over 38.58 s (code: `push=0.04, dur=40`). Fitted from the frames: t=0 1.000, 5.0 1.004, 10.5 1.010, 19.0 1.018, 28.0 1.028, 33.3 1.034, 38.0 1.038. That is 0.1%/s with no easing. Edge content travels about 27 px (top), 22 px (bottom), 15 px (left) and 13 px (right) over the whole video. |
| Camera shake, pan, tilt, rotation | None. No handheld jitter: registration residual is flat over time. |
| What the zoom applies to | The photo only. Vex, the fish, the dish and the props are drawn in fixed screen coordinates, so the floor slides under them by up to 7 px at Vex's spot (x 190) and 4 px at the dish over the video. |
| Framing | Close high-angle view of a polished light-beige vitrified-tile floor. Top 0-100 px: white door frame (top left), a plant in a dark stand with a round base (top right, base at about (505, 150)), a dark doorway or furniture at the top right. The glossy floor mirrors the doorway (soft vertical bright streaks in the upper half). |
| Camera angle (estimate) | Tile seams on the left side at y 306, 598 and 1180 (tile rows 292 and 582 px deep). The cross-ratio puts the horizon about 575-690 px above the top edge. Assuming a 26 mm-equivalent phone lens and the crop above (f about 1280 px), the camera looks about 45 deg (plus or minus 5) below horizontal and sits about 1.5 tile-lengths above the floor (about 0.9 m for 60 cm tiles, 1.2 m for 80 cm). Roll about 3 deg: the seam at y 1180 on the left is at y 1148 on the right. The vertical seam runs from x 319 (y 300) to x 340 (y 1200). |
| Brightness | Background luma (Rec.709): mean 183, median 187, p5 138, p95 212 (0-255). Floor at y 300-560: 197; floor at y 800-1280: 183; top band at y 0-100: 139. Whole-frame mean is 170.5-178.2 across all 232 sampled frames (changes come from the overlays). No exposure change or flicker: the bottom band stays at 172.3-174.1. |
| Colour cast | Warm-neutral, low saturation. Background mean RGB (188, 182.5, 175.2): R-B is +13 levels on the floor and +17 in the top band. Mean saturation (max-min)/max is 0.071. No grade is applied in the video: it matches the crop to within about 2 levels (mean residual -1.8). |
| Sharpness | Photo: clean and soft-contrast. High-pass (3x3) std in flat floor is 0.84 levels on the clean photo. Tile seams are 1-2 px wide, 20-40 levels deep. Laplacian variance of the background is 90 on the clean photo and 159 after grain. Gradient p99 is 12. |
| Grain | `K.grain` adds Gaussian luma noise (sigma 2.2, the same value on R, G and B: residual channel correlation 0.90-0.93) to every frame before the text is drawn. In the delivered file: per-pixel temporal std over 71 frames of flat floor is 1.77 levels (median), and the mean frame-to-frame difference is 0.6-1.0 levels, with jumps to 2.2-2.3 at I-frames. 52% of pixels are identical between consecutive frames (P/B frames carry the noise forward), so the grain shimmers rather than dancing every frame. Residual against the clean photo: std 1.6-1.7 levels. |

## 2. Mascot rendering (Vex)

| Item | Measurement |
|---|---|
| Technique | Vector drawing in pycairo (`motion/vex2d.py`). Every part is a path, redrawn each frame at scale S = 0.33 (body units x 0.33 = px). |
| Height on screen | Standing, no jump or rotation (67% of frames): median 355 px = 27.7% of 1280 (range 327-363). The breathing bob alone moves it plus or minus 4 px. Sitting (18% of frames): median 354 px (legs stretch toward the camera). All frames: 272-392 px. |
| Width | Standing median 266 px = 36.9% of 720 (range 259-369; the cape flare widens it). Body area median 65,544 px = 7.1% of the frame. Frame 0: all overlays (Vex + fish + dish) cover 8.4%. |
| Proportions | Head 181 x 165 px, 47% of his height (about 2.1 heads tall). Eyes 54 x 61 px each, red iris, two white catchlights. |
| Position | Feet always on one line, y = 742 (58% of frame height); there is no depth movement and the scale never changes. Head top about y 388 (30%). Bounding-box centre: median x 212 (29% of width), range 184-392; median y 565 (44%). Feet x by time: x 205 for 6.1 s, x 190 for 14.8 s, x 355 for 5.8 s, x 250 for 7.3 s (the rest is in transit). He is always in the left half to centre; the fish dish sits at the right (centre x 480). |
| Outline | Dark ink (28, 15, 26), about 3.3 px on body shapes (10 units); measured edge profile at the hair top is 48/20/16/25 then the fill. Inner details: mouth 3 px, eye rim 4 px, eyelash 6 px, sleeves 3 px each side, sub-parts 2.3-3 px. No white sticker border. |
| Edges | Hard, about 1 px anti-aliased transitions at full contrast (luma 190 to 16 across 1-2 px). Laplacian variance on Vex is 2991, against 90 for the clean photo (33x); gradient p99 is 124 against 12. No blur or softening is applied to him. The scene grain does cover him (drawn before the grain pass). |
| Shading | Flat fills, plus one cel-shadow crescent per shape: a darker tone offset 4.3 px right and 3.6 px down, i.e. light assumed from the top left. Thin rim-light lines (1.65 px) on face and boots. Hair highlight swooshes. Radial gradient in the irises only. Three pink blush strokes per cheek. Colours: skin (226, 202, 247), cape red (237, 41, 46) with a dark red shade, black cloth, gold buttons. Pixel stats at frame 0: 57% of his pixels have luma < 50, mean saturation 0.38, 11% red, 21% lavender. |
| Grounding | Code-drawn soft shadow under the feet: two concentric radial-gradient ellipses (rx 109 x ry 17 px at alpha 0.22, and 71 x 11 px at 0.32), plus a 17 x 4 px contact shadow under each boot (alpha 0.5) when he stands with lift < 3. Measured at frame 0: centre luma ratio 0.57 (43% darker); 5% darkening reached at about plus or minus 80 px; overall darkened area 256 x 37 px (x 47-303, y 742-779). Mid-jump (37.5 s, lift 65 px): centre ratio 0.74, larger and fainter (`fade = 1/(1+lift/80)`, `grow = 1+lift/300`). Sitting: a 1.2x wider ellipse and no contact shadows. The shadow is centred straight under him with no direction, even though the photo's light comes from the far doorway. He has no reflection in the glossy floor. |
| Viewing angle | Drawn straight-on at eye level (front view). `turn` (up to 0.5) only slides the face features up to 19 px sideways and narrows the far ear. There are no 3/4, profile or flipped drawings and no top-down foreshortening, while the floor is seen from about 45 deg above. |
| Sticker look | Flat, thick-outlined cartoon on a photo, without matching blur, lighting, colour wash or perspective. It shares the photo's grain. |

## 3. Mascot animation

Rendering cadence: every value is recomputed every frame at 30 fps (no holds on twos). Continuous moves (hops, spins, walks,
squash and land wobbles) are eased (ease-out, sine arcs, damped cosine). **Pose and expression changes are stepped:
the arm targets, eye and mouth drawings swap in one frame with no in-betweens.**

Always-on idle: breathing bob (vertical scale plus or minus 1.2%, 0.49 Hz); cape-hem sway (plus or minus 3.3 px, 0.38 Hz; faster
sway while walking or airborne); auto-blinks.

### Every discrete pose/expression change (lip-sync excluded; 42 changes, 38 distinct states)

| t (s) | Change | Motion between |
|---|---|---|
| 0.00 | Frame 0: standing x 205, turned toward the fish (turn 0.5), leaning 3.4 deg forward, sparkle eyes, grin, hands at chest | - |
| 0.13-0.87 | Lip-sync on "Snack?" | mouth flaps |
| 1.37 | Eyes open, smirk, turn snaps to 0 | squash pulse 0.15 over 0.3 s |
| 2.67-2.97 | Glances right toward the fish (turn 0 to 0.4) | eased over 0.3 s |
| 3.53 | Angry eyes and brows, hands on hips, head tilt -2.9 deg, lip-sync | stepped |
| 4.13 | Arms out, cape flares to 1.0 (stays flared 4.0-11.07) | stepped |
| 4.83 | Arms up with claws. **The raised hands are hidden behind his head** (drawn before it). | stepped |
| 6.10-6.53 | Hop from x 205 to x 355, 70 px high, legs tucked, arms up | ease-out |
| 6.57 | Lands (squash 0.39 for 0.13 s); hands go onto the fish | stepped |
| 6.70-7.07 | Lifts the fish from the dish to his mouth | eased |
| 7.15 | CHOMP: eyes closed, clenched "chomp" mouth with long fangs, impact star, 0.25 s shake (fish 5 px, Vex 3 px) | - |
| 7.93 | Eyes shocked, brows up (fish puff > 0.25) | stepped |
| 8.30 | The puffed fish is drawn in front of him, filling his arms | stepped |
| 8.70 | Crying eyes (wobbling tear pools) | stepped |
| 9.44-9.94 | "OW!": backflip spin -360 deg about his centre, 130 px high, x 355 to 190; impact star; the fish falls back into the dish (0.35 s) | ease-out |
| 9.97 | Lands sitting: dizzy spiral eyes, tears, 3 stars circling his head (9.94-11.04), land wobble (squash 0.6, then 0.18, 0.03) | damped |
| 11.04-11.39 | Pops up standing, 60 px jump; chef hat scales in (0 to 1.25 in 0.3 s); left hand on hip, right arm up holding a frying pan, **the pan hidden behind his head** | ease-out, land squash 0.52 |
| 11.40 | Happy closed-arc eyes plus lip-sync | stepped |
| 12.83 | Sparkle eyes, smirk | stepped |
| 13.07 | Eyes open, flat brows (listening) | stepped |
| 14.30 | Shocked eyes, frown ("poison") | stepped |
| 16.67 | Drops the pan: it first appears, falls 0.3 s from (250, 560) to the floor at (150, 772); arms out, "o" mouth, squash 0.28 | pan eased fall |
| 17.60 | Hands on cheeks, shocked, lip-sync | stepped |
| 18.33 | Thinking: hand on chin, other on hip, turn 0.3, head tilt 4.6 deg | stepped |
| 20.30 | "o" mouth | stepped |
| 20.57-24.66 | Looks up at the thought bubble; chin hand plus resting hand; head nods plus or minus 2.9 deg at 0.95 Hz | continuous |
| 24.67-26.97 | Sparkle eyes, claws up (hidden behind head), walks x 190 to 355 (2.3 s, leg cycle 2.2 Hz, 26-unit leg lift), lip-sync | linear |
| 27.20 | Grabs the fish: angry eyes, wide biting mouth (118-unit gape) | stepped |
| 27.67-28.07 | Lifts the fish to his mouth | eased |
| 28.70 | Freezes: looks away to the left, flat brows, smirk | stepped |
| 30.01-30.46 | The fish puffs in his face: impact star, knocked sideways -83 deg, 80 px high, x 355 to 230 | ease-out |
| 30.46-31.31 | Lies rotated 83 deg with dizzy eyes, tears and stars, **floating**: his lowest point is 37 px above the floor line, his shadow on the floor below | - |
| 31.31 | **Hard pose pop** in one frame: rotated at x 230 becomes sitting upright at x 250, sad eyes and brows, holding a juice box at his mouth (sip bubbles). The single biggest frame-to-frame change in the video. | none (1 frame) |
| 33.16 | Juice box jumps to the floor; arms down, frown | stepped |
| 34.83 | Turns to look at the fish (turn 0.5), brows up | stepped |
| 35.63 | Shocked eyes, hands on cheeks, "o" mouth | stepped |
| 37.27-37.65 | "MY JUICE!": jumps 70 px, crying eyes with tears, sad brows, cape flare 0.6, arms up (hidden), lip-sync; lands at 37.67 (squash 0.5 plus wobble) | ease-out |
| 38.00 | Wobble mouth (crying) to the end | - |

Counts:
- 21 distinct body poses (arms, legs, claws, held prop, rotated) and 26 distinct face combinations (eyes, brows, mouth).
- Eye states used (9): sparkle, open, angry, closed, shocked, cry, dizzy, happy, sad.
- Mouth drawings (10): grin, smirk, closed, open, wide, bite, chomp, frown, o, wobble.
- Big body moves (5 airborne moments): hop 6.10, spin 9.44, hat pop 11.04, knock 30.01, jump 37.27. Plus 1 walk (24.67-26.97).
- Time split: body moving (x, lift, rot, squash, turn or tilt changing) 19.4% of frames (7.5 s); lip-sync 27.7% of frames; neither (only idle bob, sway or blink) 62.7%.

**Mouth flaps:** lip-sync is driven by the loudness of his own audio (30 ms RMS). Each frame picks one of 3 drawings:
closed (smile line with fangs), open (48 units), wide (86 units). 110 shape changes over 11.9 s of Vex speech (9.2 per s):
b1 8, b3 30, b5 3, b6 8, b8 29, b10 22, b14 10. **No lip-sync during b12** ("I'll have juice."): the mouth is a fixed "o"
while he holds the box. His mouth never moves during the keeper's lines.

**Blinks:** automatic every 2.9 s, 4 frames (0.13 s), peaking at 83% lid closure (never fully shut on frame samples).
13 scheduled; 2 suppressed by the scene (7.4, 27.7); of the 11 drawn, 8 are visible (1.63, 13.23, 16.13, 19.03,
21.93, 24.83, 33.53, 36.43). Not visible at 4.53 (angry eyes) or at 10.33 and 30.63 (dizzy spirals).

**Hands:** visible only in the rest, hips, out, chin, cheek, front (juice box), down and hands-on-fish poses. Hidden
behind the head whenever the arm is "up": 4.83-6.57, 9.47-9.97, the right hand and pan 11.07-16.67, 24.67-27.20,
30.03-31.31, and 37.27-end.

**Effects and durations:**
- Impact star (white 8-point burst with speed lines, up to 70 or 60 px radius, sine envelope over 0.3 s): 7.15, 9.44, 30.01.
- Dizzy stars (3 yellow stars, 13 px, on an 80 x 24 px elliptical orbit, 0.8 rev/s): 9.94-11.04 and 30.46-31.31.
- Tears (3 drops per eye cycling at 1.6 Hz plus a streak): 9.94-11.04, 30.46-31.31, 37.27-end.
- Sparkle eye stars: 0-1.37, 12.83-13.07, 24.67-27.20.
- Sip bubbles: 31.31-33.16.

## 4. The pufferfish, the dish and the props

| Object | Style and size | Animation and transformations |
|---|---|---|
| Pufferfish | Flat vector, about 2.5 px dark outline, yellow back #f2c94c, cream belly, orange fins, brown spots, pink lips; faces left toward Vex. Unpuffed body 94 x 45 px (whole fish about 105 px with tail, 39% of Vex's width). Fully puffed: body 137 x 132 px with 20 cream spikes, about 177 px across, half of Vex's height; angry brow and red cheek when puff > 0.5. | Idle: bob plus or minus 2.2 px (0.48 Hz), tail wag plus or minus 14 deg (1.43 Hz), side fin plus or minus 17 deg (1.1 Hz); stops while held. **Inflations:** 7.77-9.05, 3 stepped "gulps" (0.43 s each) while in Vex's hands; 30.01-30.26, one 0.25 s ease-out; 33.51-35.11, 3 gulps (0.53 s each) while turning yellow to tomato red (cream to pink), finished at 35.11 and kept to the end. **Deflations:** 13.05-14.25 (1.2 s); 31.66-33.16 (to 15%). **Moves:** lifted from the dish to Vex's mouth (6.70-7.07, 27.67-28.07); falls back (9.44-9.79, 30.26-30.61); shakes 5 px at 60 rad/s for 0.25-0.3 s (7.15, 9.44, 30.01); from 33.51, lips on the straw (3 px shift). |
| Water dish | Flat light-blue (#5a8fd0) oval pet dish with a light radial-gradient water surface and a 5 px outline: 156 x 53 px (blue pixels 150 x 44), centre (480, 736), with its own soft floor shadow. The front lip covers the fish's lower half. | Static the whole video. |
| Frying pan | Brown handle, dark grey pan, about 109 x 22 px on the floor with a soft shadow. | Held 11.07-16.67, but not visible (behind the head). Appears at 16.67 in mid-air, falls 0.3 s, thud SFX at 16.97, lies at about x 94-203, y 761-783 (plus its shadow) to the end. |
| Chef hat | White 3-puff toque with grey pleats: 113 x 93 px of white. | Scales in 0 to 1.25 over 0.3 s at 11.04; rides on his head 11.04-30.21; hidden while rotated (from 30.03). |
| Thought bubble | White cloud of 5 overlapping circles (about 380 x 250 px, centre (450, 470)), 4 px outline, plus 2 tail circles (r 18 and 12) down to the dish. | Scales in 0.3 s at 20.82 ("food"); bacteria (3 green ciliated blobs) at 21.75; pink worm, mini pufferfish and 2 red arrows at 23.21 (0.3 s scale-ins); shrinks out 24.86-25.11. Shows bacteria to worm to fish. |
| Juice box | Red carton with a white label, tomato icon and white straw: 52 x 74 px in his hands (31.31-33.16); on the floor at (382, 740) it is 44 x 64 px, with a 3-segment bendy straw into the fish's lips. | Appears with the 31.31 pose pop (no entrance); hard swap from hands to floor at 33.16; crumples to 85% width x 65% height over 33.51-35.11. |

## 5. Text

Two text systems, both drawn after the grain (so they are grain-free), both in **Comic Neue Bold** (`assets/fonts/ComicNeue-Bold.ttf`).

**Keeper captions** (`K.comic_captions`):
- Look: white fill (255, 255, 255) with a black (0, 0, 0) stroke of 8.6 px (about 4.3 px visible outside each glyph), no shadow, no box.
- Size: 54 px font, all lower case. Ascender (tallest letter) height 35 px = 2.7% of frame height; x-height 26 px; descenders to +10 px.
- Position: centred at x 360. Line 1 baseline y 880 (68.8%), line 2 baseline y 940 (73.4%); the block spans y 840-953 with outline. Example width: "vex no that's a" is 339 px fill.
- Layout: 1-2 lines of at most 21 characters; punctuation stripped except ' ? !.
- Timing: a whole phrase appears at once (no word-by-word karaoke), hard on 0.05 s before the first word, hard off or swap. 11 captions, 5.6 words each on average.

| On-Off (s) | Dur | Words | Text (exact) |
|---|---|---|---|
| 1.30-3.44 | 2.14 | 5 | vex no that's a / pufferfish |
| 6.03-8.17 | 2.14 | 7 | don't when it's / scared it blows up |
| 8.12-9.40 | 1.28 | 4 | into a spiky ball |
| 13.00-15.04 | 2.03 | 6 | cooking won't help / its poison doesn't |
| 14.99-16.67 | 1.69 | 7 | break down with heat / and there's no |
| 16.62-17.42 | 0.80 | 1 | antidote |
| 20.49-23.11 | 2.62 | 8 | from its food tiny / bacteria make it and |
| 23.06-24.52 | 1.46 | 6 | it builds up inside / the fish |
| 27.12-29.69 | 2.57 | 8 | farmed ones carry far / less not zero and |
| 29.64-30.90 | 1.26 | 4 | they still puff up |
| 34.16-36.72 | 2.56 | 6 | uh vex? it's drinking / your juice |

Mean caption duration 1.87 s (median 2.03, range 0.80-2.62).

**Vex's red replies** (`K.reply`), his meaning over his head:
- Look: red fill (233, 29, 39) with a white stroke of 8.5-9.9 px (about 4.3-4.9 px visible), no shadow.
- Size: 58 px font for short lines (ascender or cap height 38-40 px = 3.0-3.1%, x-height 28 px); 50 px for lines over 26 characters (ascender 35 px).
- Position: baseline y 376 (29.4% of frame height), 321 when it is clear of the chef hat, 412 for "i'll have juice". 2-line replies sit 52 px higher per extra line. Centred on Vex's x, so it travels with him (clamped to stay on screen). Lines wider than 650 px split near the middle.
- Motion: bobs plus or minus 3 px (0.8 Hz). Pops in with a 0.3 s back-out (overshoots to 115% at about 0.16 s); shrinks out over 0.25 s starting 0.7 s after his line ends.
- Case: mixed as written (lower case, and capitals for shouts).

| On (full at) / out | Visible | Size | Lines | Text (exact) |
|---|---|---|---|---|
| 0.12 (0.42) / 1.55-1.80 | 1.68 | 58 | 1 | snack? |
| 3.52 (3.82) / 6.54-6.79 | 3.28 | 50 | 2 | i'm a vampire. i / bite everything. |
| 9.44 (9.74) / 10.69-10.94 | 1.50 | 58 | 1 | OW! |
| 11.39 (11.69) / 13.51-13.76 | 2.38 | 58 | 1 | then i'll cook it first |
| 17.57 (17.87) / 21.00-21.25 | 3.67 | 50 | 2 | poison?? where does a / tiny fish get poison? |
| 24.66 (24.96) / 27.57-27.82 | 3.16 | 50 | 2 | so a fish with clean / food is safe to bite! |
| 31.66 (31.96) / 33.61-33.86 | 2.20 | 58 | 1 | i'll have juice. |
| 37.25 (37.55) / still on at the cut | 1.33 | 58 | 1 | MY JUICE! |

Mean reply visibility 2.44 s. Combined mean over all 19 text items: 2.11 s.

Coverage:
- Keeper caption on 20.3 s (53%); red reply on 19.2 s (50%); both at once 3.5 s; any text 36.0 s (93%).
- No-text stretches: 0-0.12, 10.94-11.39, 30.90-31.66, 33.86-34.16 and 36.72-37.25 (0.53 s); the rest are under 0.15 s each.
- No title, hook text, cards, arrows, labels, emoji, logo or end card anywhere.

## 6. Audio

**Overall:**
- Voices plus 5 synthesized SFX only. `MUSIC = "none"`: no music, no room tone, no ambience.
- Loudness: mixed to -14 LUFS mono, delivered as dual-mono stereo that measures -11.7 LUFS integrated (BS.1770). Short-term 3 s loudness p10 -13.0, p50 -11.9, p95 -9.9 LUFS (range about 3 LU).
- Sample peak 0.0 dBFS: 38 samples clip at 7.2 s (the hit), and samples at -0.4 dBFS at 17.0 and 36.7.
- **Between lines the track is digital zero** (-120 dBFS): 8.8 s of the 38.6 s (22.7%) is exact silence; 10.9 s is below -45 dBFS in gaps of at least 0.15 s.
- Silences of at least 0.5 s: 0.81-1.37, 9.97-11.41 (1.44 s, during the dizzy and hat pop), 31.03-31.69, 32.88-33.65 and 37.99-38.61 (end).
- Fades: 30 ms in, 120 ms out (in silence).

**Keeper (off-screen, never seen):**
- Voice: Chatterbox Turbo stock female TTS. f0 median 216 Hz (p10 175, p90 346; per line 213-253 Hz).
- Rate: 62 words over 17.9 s of first-to-last-word time is 3.46 words/s; per line 2.87, 3.70, 3.73, 3.86, 3.25 and 2.78. About 0.25-0.4 s pauses at full stops inside lines.
- Level: active-frame RMS median -18.8 dBFS (p90 -9.4).
- Sound: dry and close, no audible room (no reverb tail, black silence after each line). Spectrum: centroid 849 Hz, 99% of energy below 4.1 kHz, content present up to 16 kHz (-45 to -52 dB relative).
- Non-speech tags: [chuckle] 30.7-31.0 (peak -2.7 dBFS) and [laugh] 36.6-36.9 (peak -2.1 dBFS). These are among the loudest moments.
- Whisper renders the name as "**Bex**" both times ("Bex, no." 1.22; "Uh, Bex?" 34.76).

**Vex:**
- Voice: Turbo gibberish, pitch-shifted +6 semitones with the formants shifted. f0 median 383 Hz (p10 306, p90 477); per line: snack 359, b3 374, OW 350, b6 387, b8 401, b10 387, b12 361, MY JUICE 437 Hz.
- Level: active RMS median -16.4 dBFS, about 2.4 dB above the keeper.
- Spectrum: band-limited, steep roll-off above about 8 kHz (-49 dB at 8-10 kHz, -69 at 10-11, -85 at 12-16 relative to the 200-1000 Hz peak).
- Whisper hears none of his lines (as intended).

| Beat | Sound span | Gibberish sent (syllables) | Syl/s | Meaning shown |
|---|---|---|---|---|
| b1 | 0.15-0.80 (0.65 s) | "mi?" + [laugh] (1) | - | snack? |
| b3 | 3.56-5.81 (2.26 s) | "ni pa niponu. mi moku powaki." (10) | 4.4 | i'm a vampire. i bite everything. |
| b5 | 9.47-9.97 (0.50 s) | "owwie!" (2) | 4.0 | OW! |
| b6 | 11.42-12.80 (1.38 s) | "bu ka meh meh wi." (5) | 3.6 | then i'll cook it first |
| b8 | 17.60-20.25 (2.65 s) | "mibu? mowa bi pa mimo pya nyu mibu?" (12) | 4.5 | poison?? where does a tiny fish get poison? |
| b10 | 24.69-26.84 (2.15 s) | "pya pa pya mo mah po wi yani ni moku!" (13) | 6.0 | so a fish with clean food is safe to bite! |
| b12 | 31.69-32.86 (1.17 s) | "ka kubu panu." + [sigh] (5) | 4.3 | i'll have juice. |
| b14 | 37.28-37.97 (0.69 s) | "ka panu!" + [sniff] (3) | 4.3 | MY JUICE! |

Vex's sound always lasts shorter than his text stays on screen: speech 11.9 s in total, against 19.2 s of red text.

**Sound effects** (synthesized; cue times from the render, confirmed in the envelope):

| t (s) | SFX | Picture | Measured |
|---|---|---|---|
| 7.150 | "hit": 110 to 40 Hz boom plus noise burst, 0.45 s | CHOMP on "scared" | sub-140 Hz band -2 dBFS, 7.14-7.60; the loudest event (clips) |
| 16.972 | "thud": 160 to 60 Hz plus noise, 0.18 s | the pan lands | -7 dBFS full band, 16.96-17.12 |
| 33.658 | "pop": 900 to 300 Hz sweep, 0.12 s | fish gulp 1 (drinking) | -6.6 dBFS, alone in a silence (33.60-33.78) |
| 34.158 | "pop" | gulp 2 | under "Uh," |
| 34.658 | "pop" | gulp 3 | under "Vex?" |

No SFX on: the OW poke and spin (9.44), the knock-over (30.01), the hop, the landings, the hat pop, the walk, the bubble, the
text pops, or the juice box set-down. Gaps between speaker turns (beat end to next start): 0.24 s on 8 of the 13 turns;
0.30, 0.50, 0.60 s; 1.30 s (b12 to b13) and 1.40 s (b5 to b6). Voice is present for about 31.8 s of 38.6 (82%).

## 7. Script and structure

Order: Vex, keeper, Vex, keeper, Vex, Vex, keeper, Vex, keeper, Vex, keeper, Vex, keeper, Vex. 14 beats: 8 Vex
(gibberish plus red text), 6 keeper (spoken English plus captions). Beat times are start-end, including tags.

| # | Time | Speaker | Words (meaning) | On screen | Fact |
|---|---|---|---|---|---|
| b1 | 0.12-0.85 | Vex | Snack? [laugh] | grinning, sparkle eyes, leaning toward the fish in its dish | - |
| b2 | 1.35-3.28 | Keeper | Vex, no. That's a pufferfish. | eyes open, smirk, glance at the fish | names the animal |
| b3 | 3.52-5.85 | Vex | I'm a vampire. I bite everything. | angry, hands on hips, then arms out with cape flare, then claws up | - |
| b4 | 6.09-9.20 | Keeper | Don't. When it's scared, it blows up into a spiky ball. | hops over, grabs, CHOMP at 7.15 ("scared"); the fish gulp-inflates in his hands 7.77-9.05 | puffs into a spiky ball when scared |
| b5 | 9.44-9.99 | Vex | OW! | spin back 360 deg, lands sitting, dizzy, tears, stars | - |
| b6 | 11.39-12.81 | Vex | Then I'll cook it first. | pops up in a chef hat (pan hidden), happy eyes | - |
| b7 | 13.05-17.33 | Keeper | Cooking won't help. Its poison doesn't break down with heat. And there's no antidote. | the fish deflates; Vex shocked at "poison" (14.30); the pan falls at "antidote" (16.67), thud 16.97 | heat doesn't destroy it; no antidote |
| b8 | 17.57-20.30 | Vex | Poison? Where does a tiny fish get poison? (re-hook at 45.5% of runtime) | hands on cheeks, then hand on chin, thinking | - |
| b9 | 20.54-24.42 | Keeper | From its food. Tiny bacteria make it, and it builds up inside the fish. | thought bubble: bacteria (21.75), then worm, fish and arrows (23.21); Vex nods | bacteria make it; builds up via food |
| b10 | 24.66-26.87 | Vex | So a fish with clean food is safe to bite! | sparkle eyes, walks back to the dish | - |
| b11 | 27.17-31.06 | Keeper | Farmed ones carry far less. Not zero. And they still puff up. [chuckle] | grabs the fish (27.20), freezes at "Not" (28.67); puffs in his face at "puff" (30.01), knocked flying, dizzy | farmed: far less but not zero; still puff |
| b12 | 31.66-32.91 | Vex | I'll have juice. [sigh] | pose pop to sitting with a juice box (31.31), sad; the fish deflates | - |
| b13 | 34.21-37.01 | Keeper | Uh, Vex? It's drinking your juice. [laugh] | box on the floor (33.16); the fish drinks via the straw, gulp-puffs and turns red 33.51-35.11; Vex looks (34.83), shocked (35.63) | - |
| b14 | 37.25-37.98 | Vex | MY JUICE! [sniff] | jumps, crying, lands 37.67 | - |

4 fact beats, all in the keeper's mouth, each answering something Vex says or does.

**Escalation:**
1. Bite: the fish puffs, OW, spin and dizzy (9.44 = 24% of runtime).
2. Cook it: the keeper vetoes, pan drop (16.67 = 43%).
3. Question about poison: re-hook (17.57 = 46%).
4. "Clean food = safe": grabs again, puffed in the face and knocked flat (30.01 = 78%).
5. Gives up and takes juice: the fish steals the juice (33.5-35.1 = 87-91%), MY JUICE (37.25 = 97%).

Outcome: the animal wins (Vex loses 3 times).

**First 2 s (frame 0 exactly):**
- Frame 0 (n=0, t=0.000) contains Vex standing at x 205 (feet y 742), turned toward the fish, sparkle eyes, open grin with fangs, hands at chest, leaning 3.4 deg; the yellow unpuffed fish in its blue dish at right (480, 736). There is no text, the audio is digital silence (first voice at 0.15 s), and the push-in is at 1.000. Overlays cover 8.4% of the frame.
- Then: 0.12 red "snack?" pops in (full at 0.42); 0.13-0.87 lip-sync (8 mouth changes); 0.15-0.48 "mi?" (359 Hz) plus a laugh about 0.6-0.8; 0.81-1.37 silence; 1.30 caption "vex no that's a / pufferfish" hard on; 1.35 keeper "Vex, no."; 1.37 expression swap plus squash pulse; 1.55-1.80 "snack?" shrinks out; 1.63 blink.
- About 7 visible changes in the first 2 s.

**Ending, last 3 s at 30 fps (n=1068-1157, 35.60-38.57):**

| Frames | t (s) | What happens |
|---|---|---|
| 1068-1101 | 35.60-36.70 | Vex sits shocked, hands on cheeks (from n=1069, 35.63), "o" mouth. Caption "uh vex? it's drinking / your juice" on. The red fish gulps (until 35.11, then holds). Keeper "...your juice." ends 36.37; [laugh] 36.6-36.9. Frame-to-frame change 0.7-1.4 levels (idle only). |
| 1102 | 36.73 | Caption hard off (frame-luma +2.4). |
| 1102-1117 | 36.73-37.23 | No caption, no red text; idle only. |
| 1118 | 37.27 | Jump starts (biggest change of the ending, 11.6 levels mean abs diff); "MY JUICE!" begins its pop-in, full at 37.55. |
| 1118-1130 | 37.27-37.67 | Airborne 70 px, crying, tears, cape flare; "ka panu!" plus sniff 37.28-37.97. |
| 1130-1136 | 37.67-37.87 | Lands, squash 0.5 and wobble. |
| 1137-1157 | 37.90-38.57 | Holds: idle bob, tears, cape sway, fish fins, red text bob. Audio digital silence from 37.99 (0.59 s). Mean frame diff about 1.0. |

- Final spoken or shown line: Vex "MY JUICE!". The keeper's last line is "Uh, Vex? It's drinking your juice."
- No question, call to action, outro, end card or subscribe text.
- **Cut:** hard cut on frame 1157 (38.567 s). Picture luma steady at 173.6-173.8 to the last frame (no fade). "MY JUICE!" is still fully on screen; its shrink-out would only start at 38.68. TAIL = 0.6 s after the last beat.

## 8. Pacing

**Semantic visible-change events** (pose/expression swaps, moves, prop and fish changes, effects, text on/off, blinks): 89 in total, 23.1 per 10 s.

| Window | Events | Per 10 s | Excluding blinks | By type |
|---|---|---|---|---|
| 0-10 s | 30 | 30.0 | 29 | 12 Vex pose/expression, 9 text, 5 fish/prop, 2 impact, 1 lip-sync start, 1 blink |
| 10-20 s | 20 | 20.0 | 17 | 7 Vex, 8 text, 1 fish, 1 impact, 3 blinks |
| 20-30 s | 21 | 21.0 | 19 | 6 Vex, 8 text, 4 thought-bubble, 1 fish, 2 blinks |
| 30-38.6 s | 18 | 21.0 | 18.6 per 10 s | 6 Vex, 6 text, 3 fish/prop, 1 impact, 2 blinks |

**Pixel measure** (all 1158 frames at 360x640; "changed" means more than 20 levels):
- Median frame-to-frame changed area 0.36%, p90 3.9%, max 9.1% (31.33).
- Frames with at least 0.5% of pixels changing: 37.9% of all frames. Onsets of such activity per 10 s window: 17, 18, 15, 15.
- **Longest stretch with no significant change:** 1.60 s at the 0.5% threshold, from 15.10 s (Vex standing shocked with a static caption until it swaps at 16.62 and the pan drops at 16.67). It is 2.13 s at the 1% threshold, from 18.37 (Vex's thinking pose with only lip flaps and static red text). Using semantic events with text and blinks excluded, the gap is 14.30-16.67 (2.37 s).
- Longest gaps between any semantic events: 24.86-26.97 (2.11 s, but Vex is walking throughout), 31.66-33.16 (1.50 s), 11.40-12.83 (1.43 s).

**Averages:** keeper caption 1.87 s; red reply 2.44 s; both systems 2.11 s; speaker turn about 2.6 s average (14 beats in 38.6 s).

## 9. Real-world elements

- None besides the one still photo of the floor: no real hands, no real objects interacting, no live footage, no
  camera motion beyond the digital push-in.
- The keeper exists only as an off-screen TTS voice.
- The owner's hand photos (`hand_palm`, `hand_reach` in `assets/mascot/photos/`) are not used in this episode.
- Everything that moves is code-drawn vector: Vex, the fish, the dish, the pan, the hat, the box, the bubble, the stars and the impacts.
