# Deep study: the "candy button" Grim reference, measured frame by frame (5 Nov 2026)

Reference: another creator's Short about their mascot "Grim" (chibi grim reaper) and a big red button: "Hit that
button and one candy will appear, but one random person dies." 31.43 s (943 frames), 720x1280, 30 fps, H.264 High
940 kb/s, AAC HE stereo 54 kb/s. The file stays out of the repo (public). **We copy technique, pacing, layout, audio
and structure only, never Grim's design, name or look.**

Method: every 2 s contact sheet, then 30 fps crops of every key moment (all of 0-4 s and 28.4-31.43 s, every
mascot action, the walk, the counter changes); per-frame difference maps; phase correlation of background patches
for camera motion; colour and edge measurements on full-resolution frames; white/red/purple text masks to get
caption on/off frames; RMS envelope, spectral-flux onsets, spectrograms and an autocorrelation pitch track for audio.
All pixel numbers are at 720x1280 unless noted. Times are video time in seconds.

---

## 1. Shot and camera

**The background is real moving video, not a still photo.**
- Background patches (sofa band, empty floor right of the button) change by 0.2-1.0 grey levels (mean abs diff)
  between consecutive new frames, against 0.03-0.2 on duplicated frames, and the image drifts: phase correlation
  of the sofa band against frame 0 gives dx -10..+4 px, dy -8..+16 px over 0-17.5 s (e.g. dy -8 at 1.0 s, +16 at
  4.5 s, +4 at 11 s, +16 at 17.5 s). It's a slow, smooth float (max ~8 px/s, frame-to-frame <= 0.6 px, no
  high-frequency shake): a phone held very steady or a generated "static" camera.
- No zoom and no push-in: the button's red area stays 6,000-6,300 px (+-3%) for 17.6 s.
- No cuts at all in 0-17.6 s (shift track is continuous through every pose change). The walk (17.6-26.6 s) has no
  detectable hard cut; if there is a splice it's hidden in the whip pan at 24.0-24.5 s (motion blur, 20-40 level
  frame differences). 26.6-31.43 s is locked off (drift <= 4 px).
- Frame cadence: the walk is clean 24 fps footage with 3:2-style pulldown (every 5th frame repeated: 529, 534,
  539...). The floor section has 21-25 new frames per second with irregular repeats and holds of up to 8 frames
  (0.27 s at 5.03-5.30 s), the look of a 24 fps clip retimed to fit the dialogue. Captions, counter and red text
  change on the 30 fps grid, so they were added afterwards in an editor.
- Background, mascot, button and candy all repeat on the **same** duplicated frames (e.g. the falling candy is
  identical in frames 2.833/2.867 and 2.967/3.000), so the cartoon is baked into the same 24 fps picture, not
  overlaid at 30 fps like the text.

**Framing of the floor shot (0-17.6 s and 26.6-31.4 s)**
- Low, high-angle phone shot: camera roughly knee-to-waist height, tilted down ~20-35 deg (the button's cap top reads
  as an ellipse 105x40 px, ratio 0.38). The sofa base cuts the top 11-13% of the frame, the rest (~87%) is floor.
  Horizon above the frame. The characters stand ~1-1.5 m from the lens.
- Brightness: mean luma 148/255 (58%), std 41. Warm, low-saturation: mean RGB (154,146,141), floor mid
  (180,175,173), far floor (161,151,142); mean saturation 0.12. Light comes from the right/front-right (shadows fall
  left, see 2).
- Soft and clean: 720p at 940 kb/s, temporal noise std 0.2-0.6 levels (no visible grain), floor high-pass std 2.0
  (marble veins only). Mild compression smoothing, no blocking that reads on a phone.

**The POV walk to the front door (17.6-26.6 s), exactly how it's cut in and out**
- In (17.60 s, on "anymore, Grim"): no cut. The same take starts to move: an ease-in pan that turns the camera left
  and tilts up while walking forward (content shift 2 px at 17.60, 18 px at 17.80, 50 px at 18.00, then too fast to
  correlate). The counter is removed on that exact frame (17.600); the caption stays. Grim, the button and the
  candies stay glued to the floor and are carried down-right out of frame in 1.1 s (Grim gone at 18.70), Grim
  turning his head to keep looking at the camera.
- 18.9-19.2: hallway, front door fills the frame. 19.6: the filmer's real right forearm enters bottom-left;
  20.2 grabs the knob; 20.2-20.9 unlatches; 20.9-21.6 the door swings open onto a sunny street (exposure jumps:
  luma 139 inside to 126 outside, saturation 0.10 to 0.26).
- 21.6-24.0 held view through the open door, porch columns framing it: a cyclist ("Mark") rides left to right;
  22.33-22.67 a pink-white starburst flash (~120 px) on him, he vanishes, glitter dots linger to ~23.5, the bike
  rolls on riderless and topples 23.0-23.6.
- Out: whip pan back at 24.0-24.5 s (heavy motion blur); auto-exposure visibly pumps (mean luma 125 -> 84 at
  24.5 s, back to 124-140 by 25.2-26.5), a strong sign of a real phone camera. 24.5-25.3 wall with a framed
  picture and a light switch, 25.3 the living room and sofa; the button slides in from the left edge at 25.37 and
  Grim at 25.53-25.60, **already mid-crime** (lying on the button). The camera settles by 26.6 s. "GRIM!" starts at
  25.52, the instant his skull enters the frame.

**Likely production route (inference, not certain):** the floor scenes look like AI image-to-video clips (character
placed on a frame of the real floor, then animated): the cartoon turns in 3D, its robe deforms, the hood design
drifts between moments (thin hood outline at 0 s, a full puffy black hood at 5.2 s), it casts room-consistent soft
shadows, the real pointing hand occludes the button's base (0.6-1.2 s), and everything shares one 24 fps picture.
The pointing hand at 0 s is smooth and pale, unlike the hairy tanned forearm at the door. The walk looks like real
phone footage (auto-exposure lag, real forearm). Whatever the tool, what the viewer sees is: real moving footage, a
character that is lit, shadowed and pinned to the floor, and continuous full animation.

## 2. Mascot rendering

| Measure | Value |
|---|---|
| Height, upright | 195-219 px = 15.2-17.1% of 1280 (0.0 s: 196 px; 4.0 s: 219 with raised hands; 28.5 s: 195) |
| Width, upright | 124-160 px = 17-22% of 720 |
| Leaning/lying on button | bbox up to 285x252 px (2.0 s, 9-12 s, 26.5 s) |
| Button | 155x137 px (21.5% of width, 10.7% of height); cap top ellipse 105x40 |
| Group (mascot + button) | x 219-498, centred on the frame (centre x 358); feet y 695-707 (54-55%), button bottom 733-743 (57-58%) |
| Final segment | mascot x 169-293, y 436-630 (feet 49%), button x 348-501, y 610-747 |

- Position over time: 0-13 s near the button (head top y 480-500); 6.0-8.5 s shuffles 16 px right toward the
  button; 9-12 s draped over it; **14.0-17.5 s slowly backs away up-left** (bbox moves 48 px left, 66 px up, height
  215 -> 194 px, i.e. perspective-correct shrinking as he retreats) while the keeper says "DO NOT hit that button".
- Outline: black, ~4-6 px on the silhouette (edge 10-90% transition 2 px; overlay text is 1 px, so the cartoon is
  very slightly softer than the overlays, matching the footage). Inner lines thinner (~2-3 px).
- Colours: skull off-white (246,242,244), robe near-black (15,7,10) with soft grey fold highlights (luma up to 84),
  hood lining red-orange (172,45,24), eyes yellow (242,228,117) with two white catch-lights, pink blush ellipses
  (224,200,205). Button cap red (192,21,8) with highlight to (245,69,70), base purple-black (36,20,28) with purple
  glyphs (97,35,118) and a white skull emblem.
- Shading style: flat cel colours plus soft gradients on the robe and cap (plush/vinyl-toy look), glossy specular
  streak on the button.
- **Grounding:** a soft cast shadow on the floor to the left/back of each object (light from the right): floor luma
  falls from ~150-157 at 100 px away to 109-117 right beside the robe (-25 to -30%), fading over 80-100 px; the gap
  between Grim and the button is darkened to 108-135 vs 165-175 open floor. A subtle contact shadow under the feet:
  -10% (150-155 vs 165) within ~20 px. Nothing on the lit right side of the button (174-180 = open floor).
- Viewing angle: the character is drawn face-on (front/3-4 views at eye level), the button is drawn from the
  camera's high angle (cap top visible). Candies are drawn flat-on but scaled with distance.
- Not a sticker: no white border, no drop shadow, no paper edge. It reads as a small toy standing in the room.

## 3. Mascot animation

It is full animation, not a cut-out puppet: the mascot region changes on every new source frame whenever he moves
(mean abs diff up to 62 levels), head and hood turn in 3D, the robe stretches. He is **never still for more than
0.63 s** (longest idle 3.70-4.33 s, during "sory"); even the idles carry a 1-3 level sway/breath.

Action list (each is a new pose or action; continuous motion in between):

| Time | What Grim does |
|---|---|
| 0.00-0.43 | Front view, hands clasped low, looking into the lens, gentle sway |
| 0.47-0.67 | Turns head and body to a 3/4 view (0.2 s) to look at the pointing finger; black hood exterior revealed |
| 0.70-1.53 | Watches the finger, small bobs; purple "+" sparkles float round the button (~0.8-1.6) |
| 1.57-2.00 | Leans and crawls onto the button, robe stretching |
| 2.00-2.60 | **Press:** lies across the cap, hand on top, eyes closed ^^ (happy) |
| 2.60-3.20 | Lifts head, watches the candy fall and land |
| 3.20-3.43 | Fast spin to front view in 3 frames with one blurred smear frame (3.40) |
| 3.47-4.33 | Guilty: hands at mouth, eyes up, tiny jaw tremble ("sory") |
| 4.57-5.07 | Re-settles, hands at chin, hood puffs out |
| 5.60-6.10 | Turns to 3/4, eyes on the button |
| 6.33-8.13 | Fidgets, slides toward the button |
| 8.20-8.83 | Hand creeps onto the button's side |
| 9.0-11.0 | Leans on the button, peeks at the camera (sneaky), blink at ~10.5 |
| 11.33-11.63 | **Press #2** with the hand; three candies drop |
| 12.00-12.10 | Spin to front view (2-3 frames) |
| 12.87-14.27 | Hands clasped at chest, jaw opens and closes ("sory again") |
| 14.30-17.60 | Front, hands hidden, slowly backs away (see 2) |
| 17.6-18.7 | Pinned to the floor as the camera leaves; turns head to follow the lens |
| 25.6-27.2 | Caught lying on the button, mashing it with one hand, looking at the camera |
| 27.20-27.40 | Spin upright to front view |
| 27.4-28.8 | Worried "puppy" eyes (eyebrow-shaped upper lids), slight sway |
| 28.83-29.00 | Blink: eyes close over 2 frames, closed ~3 frames, open over 2 |
| 29.60-29.90 | **Rubber-hose arm** stretches ~150 px sideways to the button and presses it |
| 30.0-31.43 | Stands still, worried, as the avalanche buries the floor |

- About 10 distinct key poses (front idle, 3/4 turn, lean/crawl, lying press, hands-at-mouth guilt, hands at chest,
  sneaky lean, back-away walk, worried front, stretched-arm press), 24 listed actions in 31 s.
- Pose changes are smooth (moves of 0.2-0.5 s) except the "caught" snaps back to front view, which take 2-3 frames
  with a smear frame (3.40, 12.05, 27.3).
- Blinks with in-betweens; eye shapes carry the acting (round sparkly, ^^ closed, droopy worried). Mouth: no lip
  sync; the skull jaw only trembles or parts slightly while he squeaks.
- Pressing is always shown with the body (draping over the cap, a hand pushing, the stretched arm), never by the
  button moving down; the candy is the visible "click".
- Effects: purple sparkle particles round the button 0.8-1.6 s (~0.8 s); starburst + glitter on Mark 22.33-23.5 s
  (~1.2 s).

## 4. Button, counter and candy

**Counter ("1x")**
- Font: heavy rounded display sans (Fredoka-One-like), white fill (252,251,251), black outline 4-7 px (median 4,
  p90 6.4). Digit height 50-51 px (fill) = 4.0% of 1280; with outline 64 px tall.
- Position: screen-fixed (it does not follow the 13-16 px floor drift), centred at x ~422 (59%), fill top y 493
  (counter box y 486-550), i.e. ~50 px above the button cap, over its right half. Final segment: x 362-488,
  y 511-574.
- Values and times (all hard swaps, no pop, no scale, no fade, no count-up animation except the final run):

| Time | Value | Trigger |
|---|---|---|
| 0.000 | 1x | on from frame 0 |
| 4.500 | 3x | 1.5 s after the first candy lands; with a chime |
| 14.067 | 9x | after "sory again"; same chime |
| 17.600 | (removed) | camera starts moving |
| 26.400 | 18x | reappears as Grim mashes the button |
| 26.567 | 27x | |
| 26.667 | 33x | |
| 26.767 | 39x | |
| 26.900 | 54x | |
| 27.033 | 59x | |
| 27.167 | 67x | holds (the "6-7" meme number) |
| 29.733 | (removed) | the final press |

  The run 18x -> 67x is 7 values in 0.77 s, one every 3-5 frames, synced to clicks. The number isn't literal
  (~9 candies are on screen at 67x).

**Button press:** shown by the mascot's body and the candy, with no button travel. The first multiplier jumps (1x->3x,
3x->9x) are not presses: they are "the price went up" reveals the keeper reads out.

**Candy**
- Wrapped bonbon, sky blue (129,183,223) with white diagonal stripes (234,246,253), navy outline (29,36,51)
  ~3 px, two specular dots, wrapper ends with 2-3 crease ticks. ~100x55 px on the floor at y ~820 (14% of width),
  ~70 px when farther away (perspective-scaled); drawn flat-on.
- Drop #1 (one candy): appears at the very top of frame at 2.70 s (x ~400, y 25-100, ~117 px wide, spinning),
  falls 715 px in 0.33 s (centroid y 96, 197, 294, 380, 570, 672, 759, 811 per 30 fps frame: ~2,200-3,000 px/s),
  shrinking to ~100 px as it falls, lands at 3.03 in front of Grim, bounces 18 px, settles by 3.27.
- Drop #2 (three candies): enter at the top edge at 11.60, land 11.77-11.93, scatter and settle by 12.07.
- Rain (26.4-27.4): candies fall one after another in a stream from the top edge onto the button, one every
  ~0.1-0.15 s, scattering round it.
- Avalanche (frame by frame in 7): a dense column ~150-200 px wide pours from the top edge onto the button from
  30.00 s, splashes out, spreads to the bottom edge by 30.4, the pour ends ~30.9, settled by ~31.2. Final frame:
  candy covers y 576-1280 (bottom 55% of the frame, blue coverage 24% of all pixels), roughly 100+ visible candies,
  only the red cap and Grim showing above it.
- Floor counts: 1 candy 3.0-11.6 s; 4 candies 12.0-17.6 s; ~9 visible 27.4-29.9 s; 100+ at the end.

## 5. Text on screen

Font for captions and replies: Comic Sans MS Bold or a close twin (Comic Neue Bold matches): single-storey "a",
rounded strokes. Size: x-height 29-30 px, ascender line 45-46 px, cap height 42 px ("DO NOT", "GRIM!!"), so about
56 px font size (4.4% of 1280). Black outline 5 px (p90 5, max 6), **no drop shadow** (the floor next to the outline
is equally dark on every side). Line pitch 64 px (baseline to baseline). Centred horizontally. All overlays appear
and disappear on a single frame: no pop, slide, typewriter or fade (bbox and pixel count identical from the first
frame of each caption).

**(a) Keeper's captions:** white (252,251,251) fill, 5 px black outline, lowercase txt-speak, digits for numbers
("1 candy", "3x", "9x"), no full stops; CAPS only for shouting ("DO NOT", "GRIM!!"). Position: two-line block
y 890-1014 (line 1 x-height band 905-934, line 2 970-998); one-line captions sit at y 922-968, so the block is
centred around y 945-955 (74-75% of the height), about 190 px below the mascot's feet. Width up to 580 px (80%), at
most ~19-20 characters per line, line 1 usually the longer one.

| # | On - off (s) | Dur | Text exactly as shown | Lines |
|---|---|---|---|---|
| 1 | 0.000-1.733 | 1.73 | hit that button and / 1 candy will appear | 2 |
| 2 | 1.733-3.333 | 1.60 | but 1 random person / dies | 2 |
| 3 | 5.167-5.533 | 0.37 | woah | 1 |
| 4 | 5.533-6.767 | 1.23 | the number went up / to 3x | 2 |
| 5 | 7.000-9.700 | 2.70 | 3 candies but / 3 random people die | 2 |
| 6 | 9.967-11.200 | 1.23 | grim... | 1 |
| 7 | 11.200-11.800 | 0.60 | no! | 1 |
| 8 | 14.567-15.800 | 1.23 | omg now its 9x | 1 |
| 9 | 16.067-16.867 | 0.80 | DO NOT | 1 |
| 10 | 16.867-18.133 | 1.27 | hit that button / anymore | 2 |
| 11 | 18.133-18.967 | 0.83 | grim im serious | 1 |
| 12 | 19.200-20.100 | 0.90 | im gonna check / to make sure | 2 |
| 13 | 20.100-21.600 | 1.50 | nobody we know / is dead | 2 |
| 14 | 25.767-26.400 | 0.63 | GRIM!! | 1 |

Mean 1.19 s (median 1.23, range 0.37-2.70), 3.9 words per caption (1-8), 7 two-line and 7 one-line. Captions come
on within about +-0.1 s of the spoken phrase (a few 0.2-0.4 s late: "omg" 0.39 s, "GRIM!!" 0.23 s) and go off
0.05-0.35 s after it. Chunks follow the breath groups ("DO NOT" / "hit that button anymore", "Grim" moved into the
next chunk "grim im serious"). Quiet asides are not captioned ("Oh" at 4.2, "Oh God" at 12.4, the final "Oh my God").

**(b) Mascot replies and other speakers:** same font, size and 5 px black outline.

| On - off (s) | Dur | Text | Colour | Position |
|---|---|---|---|---|
| 3.467-4.333 | 0.87 | sory | red (242,66,73) | x 222-337, y 412-457: centred on his head (x ~280), baseline ~35-45 px above the hood top |
| 12.833-14.000 | 1.17 | sory again | red | x 138-420 (centre 279), y 400-457 |
| 21.967-22.667 | 0.70 | oh hi mark! | purple (188,127,240) | x 246-555, y 370-417, floating ~100 px above the cyclist (it's the keeper's line, labelled at the person it's said to) |
| 28.767-29.900 | 1.13 | i like candy | red | x 86-399 (centre 242, Grim at 231), y 360-419 |

Replies are 1-3 words, lowercase baby spelling ("sory"), shown while the keeper's caption is off (never two
captions at once). Text-free stretches: 4.33-5.17, 11.80-12.83, 22.67-25.77 (3.1 s, the walk back), 26.40-28.77
(2.4 s, the candy rain and counter), 29.90-31.43 (1.5 s, the avalanche). Total ~10.9 s with no text at all (35%
of the runtime), always during action: the picture carries those moments.

## 6. Audio

- **No music** anywhere: quiet gaps fall to -40..-51 dBFS (RMS, 30 ms windows), e.g. 27.4-28.7 s median -47 dB.
  Everything is voice plus spot sound effects.
- Levels: overall RMS -17.8 dBFS, peak -0.7 dBFS. Keeper speech -15..-16 dBFS RMS (peaks -3), Grim -18.5 dBFS
  (2-3 dB under the keeper), candy clicks -24 dBFS, avalanche -16 dBFS.

**Keeper (off-screen owner):** adult male. Pitch medians per line: 103 Hz ("I'm serious", flat and stern), 137 Hz
("I'm gonna check..."), 152 Hz ("Do not hit that button anymore"), rising to 255-289 Hz on shouts ("Grim!", "No!",
"oh hi Mark"). Pace: 68 words in 31.4 s (2.2 words/s overall); 3.3-5.8 words/s inside phrases (fast "I'm gonna
check to make sure nobody we know is dead" 5.8 w/s; slow, dragged "Griiim..." 1.15 s on one word; split "Do. Not.").
Sound: casual, reactive, recorded live on a phone-class mic: energy is 30 dB lower at 3-6 kHz than at 0.3-1 kHz and
~50 dB lower above 6 kHz; a short room tail (-10 to -35 dB in ~0.25 s after "No!"). Not studio-clean, not echoey.

**Grim:** high squeaky voice, f0 375-445 Hz (median ~400 Hz, about 18 semitones above the keeper), a rise-fall
inside each syllable, slight vibrato. One burst per syllable of the shown text, each 0.12-0.45 s with 0.04-0.10 s
gaps: "sory" = 2 bursts 3.52-3.96 (text leads by 0.05 s, lingers 0.37 s), "sory again" = 3 bursts 12.90-13.74
(text leads 0.07, lingers 0.26), "i like candy" = 4 bursts 28.68-29.88 (text 0.09 s after the voice, ends with it).
Whisper transcribed none of it, so it's unintelligible cute sound, not speech.

**Sound effects (from RMS peaks, spectral-flux onsets and spectrograms, matched to the picture):**

| Time (s) | Sound | Picture |
|---|---|---|
| 2.68-2.79 | soft pop | candy appears at the top edge (2.70) |
| 3.03-3.37 | bright ding/pop (centroid 1.9 kHz, 26% energy above 4 kHz) | candy lands (3.03) |
| 4.50-6.07 | chime, D-major stack: 291, 371, 441, 587, 738, 883, 1,179 Hz (D4-F#4-A4-D5-F#5-A5-D6), ~1.5 s, under the voice | counter 1x -> 3x |
| 9.04-9.81 | three short "sneak" blips (690->850, 621, 621-649 Hz, 0.1-0.2 s each) | Grim's hand creeps onto the button |
| 11.49, 11.88 | clicks | press #2, candies land |
| 14.01-15.5 | the identical chime (same partials) | counter 3x -> 9x |
| 20.47, 20.82 | latch clicks | door handle |
| 21.1-21.9 | near silence (-40 dB) | door swings open, street revealed |
| 22.6-23.3 | broadband poof + clatter (centroid 2.7-3.6 kHz) | Mark vanishes, bike falls |
| 23.4-25.4 | footsteps / handling (~-25 dB, onsets every 0.1-0.2 s) | walk back |
| 26.09-27.42 | rapid clicks every 0.09-0.16 s (26.09, .23, .36, .45, .60, .74, .82, .92, 27.02, .18) | button mashing, candy rain, counter 18x -> 67x |
| 29.95-31.2 | candy avalanche rattle, -14 dB, decaying to -47 dB by 31.2 | avalanche |

Silences: no voice 23.3-25.5 (2.2 s, footsteps only) and 26.1-28.7 (2.6 s, clicks then a 1.3 s near-silent hold
27.4-28.7); the last ~0.25 s before the cut is near silent (-47 to -50 dB).

## 7. Script and structure

| Time (s) | Who | Exact words (heard) | On screen |
|---|---|---|---|
| 0.00-1.68 | Keeper | "Hit that button and one candy will appear," | caption 1; real hand points at the button; Grim turns to look (0.47) |
| 1.82-3.2 | Keeper | "but one random person dies." | caption 2; hand leaves (1.8); Grim lies on the button (2.0); candy falls 2.70, lands 3.03 |
| 3.52-3.96 | Grim | (2 squeaks) | red "sory"; guilty front pose |
| 4.20 / 4.50 | Keeper / SFX | "Oh," / chime | counter 1x -> 3x |
| 5.10-6.72 | Keeper | "whoa, the number went up to three X." | "woah", "the number went up / to 3x" |
| 6.90-9.36 | Keeper | "Three candies, but three random people now die." | caption 5; Grim edges to the button; sneak blips |
| 9.90-11.05 | Keeper | "Griiim..." (warning) | "grim..." ; Grim leans on it, peeks |
| 11.20-11.60 | Keeper | "No!" | "no!"; press #2 (11.4), three candies (11.60-11.93) |
| 12.42-12.58 | Keeper | "Oh God." (aside) | no caption; Grim snaps to front |
| 12.90-13.74 | Grim | (3 squeaks) | red "sory again" |
| 14.07 | SFX | chime | counter 9x |
| 14.18-15.86 | Keeper | "Oh my God, now it's nine times." | "omg now its 9x"; Grim starts backing away |
| 16.14-18.22 | Keeper | "Do not hit that button anymore, Grim." | "DO NOT", "hit that button / anymore"; camera starts to leave (17.6), counter removed |
| 18.30-18.76 | Keeper | "I'm serious." | "grim im serious"; Grim carried out of frame (18.7) |
| 19.18-21.08 | Keeper | "I'm gonna check to make sure nobody we know is dead." | two captions; walk to the door, real forearm opens it |
| 21.84-22.66 | Keeper | "Oh, hi Mark." | purple "oh hi mark!" over the cyclist; flash, he vanishes, bike falls |
| 23.3-25.5 | - | (footsteps) | whip pan back, wall, living room |
| 25.52-26.10 | Keeper | "GRIM!" | "GRIM!!"; Grim caught mashing the button |
| 26.4-27.4 | SFX | clicks | candy rain, counter 18x -> 67x |
| 27.4-28.7 | - | (silence) | Grim snaps upright, worried eyes, 67x |
| 28.68-29.88 | Grim | (4 squeaks) | red "i like candy"; blink; stretched arm presses (29.6-29.9) |
| 30.0-30.94 | Keeper + SFX | "Oh my God." (uncaptioned, under the rattle) | candy avalanche buries everything |
| 31.43 | - | - | cut |

- **Hook, frame 0 exactly:** everything is already there: a real hand pointing up-right at the button (fingertip
  ~y 870), Grim front-on looking into the lens, the red button, "1x", and the full rule as a two-line caption; the
  voice starts at 0.00 ("Hit"). No fade-in, no title card. First motion 0.47 s (Grim turns to the finger); the
  rule's stakes ("one random person dies") are fully stated by 3.2 s, but **Grim presses at 2.0 s, before the
  sentence ends**, and the candy lands at 3.03 s.
- **Escalation:** press 1 -> 1 candy -> "sory" -> price jumps to 3x (keeper reads it out: "3 candies but 3 random
  people die") -> press 2 -> 3 candies -> "sory again" -> 9x -> the stern warning, twice ("DO NOT...", "I'm
  serious").
- **Cut-away gag (17.6-26.6 s, 56-85% of the runtime):** the keeper leaves to "check nobody we know is dead"; the
  stakes, unseen so far, finally pay off in the real world: the neighbour he greets ("oh hi Mark!", a meme line)
  vanishes in a sparkle mid-ride. Then the return reveals Grim never stopped.
- **Ending:** caught (GRIM!!) -> counter runs to 67x -> Grim's only "explanation" "i like candy" -> one more press
  with a stretched arm -> avalanche. Last 3 s at 30 fps:
  - 28.43-28.73: Grim front, worried, 67x, ~9 candies on the floor, no text.
  - 28.77: "i like candy" appears; 28.83-29.00 blink.
  - 29.00-29.57: worried hold, small sway.
  - 29.60-29.70: arm starts to extend right; 29.73 counter disappears; ~29.83 the hand reaches the cap.
  - 29.87-29.97: press; the red text goes off at 29.90.
  - 30.00: a dense candy column enters at the top edge; 30.07-30.17 it hits the button (button hidden); 30.2-30.4
    splash and spread; 30.4-30.67 thinner column, pile reaches the bottom edge; 30.67-30.90 the last candies fall.
  - 30.90-31.20: settling, the red cap re-emerges; 31.20-31.43 still settling slightly (frame diffs 0.7-2.6, so no
    frozen hold), Grim standing worried at the edge of the pile.
  - Final line: the keeper's "Oh my God" (30.0-30.94), uncaptioned under the rattle; the sound decays to -47 dB by
    31.2. **Hard cut at 31.43 s, ~0.5 s after the pour ends**: no outro, no end card, no question, no fade.

## 8. Pacing

Visible changes (new pose/action, text on/off, counter change, candy event, camera event, effect):

| Window | Changes | Notes |
|---|---|---|
| 0-10 s | 24 | head turn 0.47, sparkles 0.8, hand out 1.2-1.8, lean 1.57, caption 1.73, press 2.0, candy 2.70 & 3.03, caption off 3.33, spin 3.40, "sory" 3.47/4.33, counter 4.50, re-settle 4.6, "woah" 5.17, caption 5.53, turn 5.6, captions 6.77/7.00, slide 7.4, hand 8.2, lean 9.0, captions 9.70/9.97 |
| 10-20 s | 23 | peek/blink, "no!", press, 3 candies, landing, spin, "sory again" on/off, 9x, back-away, captions, camera leaves 17.6, Grim exits 18.7, door 19.0, hand 19.6 |
| 20-31.4 s | 29 (25 per 10 s) | knob, door opens, street, "oh hi mark!", flash, bike falls, whip pan, wall, room, button/Grim re-enter (25.37/25.55), "GRIM!!", 7 counter values, spin, "i like candy", blink, arm, counter off, text off, avalanche, spread, settle |

- Average: one visible change every ~0.41 s (2.4 per second). On top of that the mascot is in continuous motion
  (never still > 0.63 s) and the background always drifts.
- Longest stretch with no new event: 27.4-28.77 s (1.37 s: 67x hold, worried face, idle sway only); next 14.57-15.80
  (1.23 s, but Grim is visibly backing away) and 12.83-14.00 (1.17 s, "sory again" with jaw movement).
- Captions: keeper mean 1.19 s, replies mean 1.06 s. Some text on screen 20.5 s (65% of the runtime; keeper
  captions 16.6 s, replies 3.9 s); ~10.9 s text-free, always during action.

## 9. Real-world elements

- **Real footage** for the whole background: the creator's own tiled living room (0-17.6, 26.6-31.4 s), hallway,
  front door, porch and street (17.6-26.6 s). Same house throughout, no stock, no stills.
- **Real hands:** (1) 0.00-1.80 s a hand from the bottom-left corner points at the button; the fingertip touches
  and covers the front of the button base (0.6-1.2 s), so the hand is in front of the cartoon; it leaves frame by
  1.8 s. (2) 19.6-21.5 s the filmer's right forearm reaches in from the bottom-left, grabs the knob, opens the door.
- **A real person as the payoff:** the cyclist on the street; the only VFX on real footage are the starburst
  (~120 px, 0.35 s) and glitter (~1 s), then the riderless bike falls.
- **Cartoon in moving footage:** pinned to the floor plane: the button moved with the background drift
  (+13 px down while the floor moved +12..+16); during the pans Grim slides with the floor, keeps his perspective
  size and turns to face the lens; when he walks away he shrinks with distance (-10%). Overlays (captions, counter)
  are screen-fixed, and the counter is hidden whenever the camera moves.

---

## Rules to copy, most important first

1. **Shoot a real video clip of the floor, not a photo.** Phone held steady at knee-to-waist height, tilted down
   20-35 deg, sofa/wall in the top 10-15%, floor ~85%. One continuous take per scene: slow float only (+-8 px x,
   +-16 px y over ~10 s, <= 8 px/s), no zoom, no push-in, no cuts. If we must use a still, fake this drift and move
   Vex with it.
2. **Pin Vex to the floor:** every floor-plane drift applies to Vex and his props by the same amount; props are
   drawn from the camera's angle (top face visible, ellipse ratio ~0.4); size scales with distance when he walks
   toward or away from the lens.
3. **Ground him like a toy in the room:** soft cast shadow on the side away from the room's light, -25..-30% floor
   brightness at the body fading to nothing over 80-100 px, plus a contact shadow -10% within 20 px under the feet,
   matching the footage's real shadows. Black silhouette outline 4-6 px, no white sticker border, edges softened
   ~1 px more than the text overlays.
4. **Vex is never still for more than 0.6 s:** constant idle sway/breath (1-3 level change), and a new action or
   pose every 1-1.5 s in seconds 0-15. Build at least 10 key poses (front, 3/4 left/right, lean/crawl onto the prop,
   lying across it, guilty hands-at-mouth, hands at chest, sneaky peek, walk-away, worried, stretched-arm reach)
   with 0.2-0.5 s moves between them, and 2-3 frame "caught" snaps with one smear frame.
5. **Frame 0 = the whole setup at once:** a real hand pointing at the prop, Vex facing the lens, the prop, the
   counter at its first value and the rule as a two-line caption; voice from 0.00 s. First motion by 0.5 s, first
   mischief by 2.0 s (before the rule sentence ends), first visible payoff by 3 s.
6. **Keeper captions:** Comic Neue Bold ~56 px (cap height 42 px, x-height 29-30 px), white fill, 5 px black
   outline, no shadow, centred, block centre at y ~945-955 (74-75%), line pitch 64 px, max 19-20 characters per
   line, 1-8 words (mean ~4), lowercase txt-speak with digits ("1 candy", "omg", "im"), CAPS only for shouts. Phrase
   chunks on within +-0.1 s of the voice, off 0.05-0.35 s after, mean ~1.2 s on screen; hard cut on and off, no pop
   or fade. Leave quiet asides uncaptioned.
7. **Vex's replies:** same font and size, red (242,66,73) with 5 px black outline, centred on his head with the
   baseline 30-45 px above it, 1-3 words of baby spelling ("sory"), on screen 0.9-1.2 s, never at the same time as
   a keeper caption. Text leads his voice by <= 0.1 s and stays 0.25-0.4 s after it. A third speaker or person gets a
   third colour (purple (188,127,240)) placed above that person in the shot.
8. **Vex's voice:** one squeaky burst per syllable of the red text (2-4 bursts, 0.12-0.45 s each, 0.04-0.10 s
   gaps), f0 ~375-445 Hz with a rise-fall per syllable and slight vibrato, unintelligible, 2-3 dB quieter than the
   keeper.
9. **Keeper's voice:** a real, casual adult voice recorded on a phone in the room (energy mostly under 3 kHz, short
   room tail), reacting rather than narrating: drawn-out warnings ("Griiim..."), single-word outbursts ("No!"), a
   stern split ("Do. Not."), fast asides; ~2.2 words/s overall, 3.3-5.8 inside phrases; about 65-70 words per 31 s.
10. **No music.** Spot sound effects on every event: pop when an object appears, bright ding when it lands, a
    ~1.5 s major-chord chime whenever the counter rises (the same chime each time), tiny "sneak" blips while he
    creeps, a click per press, a poof for the magic, a rattle for the payoff. Speech RMS around -15 dBFS, peaks
    around -1 to -3 dBFS, true silence (-45 dB) in the pauses.
11. **Escalating counter:** heavy rounded font, white with 6 px black outline, digits ~51 px tall (4% of height),
    screen-fixed ~50 px above the prop's right half (centre ~59% x, 40% y). Hard swaps only. Climb x3 per step
    (1 -> 3 -> 9) with the chime and the keeper reading the new stakes aloud, then an absurd run (7 values in
    ~0.8 s, every 3-5 frames, synced to clicks) ending on a meme-able number. Remove it on the frame the camera moves.
12. **Physical, falling payoffs:** objects enter from the top edge, fall ~700 px in ~0.33 s while spinning,
    shrink slightly with distance, land with a small bounce (~18 px) and stay on the floor as a growing count
    (1 -> 4 -> ~9 -> 100+), drawn in Vex's style (same outline language, flat colours, two highlights).
13. **The story shape:** keeper's rule with a cost (line 1) -> Vex breaks it immediately -> tiny guilty reply ->
    stakes rise (keeper reads them out) -> breaks it again -> "sorry again" -> stern warning twice -> keeper leaves ->
    the cost shows up in the real world -> return: Vex caught mid-mischief -> one-line excuse -> one last press ->
    huge physical payoff -> cut.
14. **Mid-video real-world cut-away at ~55-85% of the runtime:** no hard cut; the camera turns away with an ease-in
    pan while the caption continues, Vex rides out of frame on the floor in ~1 s, a real walk with real hands
    (open a door, pick something up), one real-world gag, a whip pan back, and Vex re-enters frame already
    misbehaving; the keeper shouts his name the moment he's back in frame (within 0.1 s).
15. **Ending:** the final mischief lands within ~1 s of the last reply, the payoff covers >= 50% of the frame in
    < 1 s, and the video hard-cuts ~0.5 s after the motion peaks, while things are still settling. Last line is the
    keeper's uncaptioned "oh my god" under the sound effect. No outro, no question card, no fade.
16. **Pacing:** >= 23 visible changes per 10 s (one every ~0.4 s); no stretch over ~1.4 s without a new event;
    text-free stretches of 1.5-3 s are fine when action carries them (walk back, rain, avalanche).
17. **Real hands twice:** once in frame 0 pointing at the prop (covering part of it, so it reads as in front), once
    in the cut-away doing a real action. Use the owner's own hands and house.
18. **Acting through the eyes:** blinks with 2-frame in-betweens, ^^ closed eyes for joy while misbehaving, round
    sparkly eyes at the lens, droopy "puppy" lids when caught; the mouth barely moves (jaw tremble only while
    squeaking).
19. **Mascot scale and place:** upright height 195-220 px of 1280 (15-17%), prop ~155x137 px; mascot plus prop
    centred horizontally, feet at 50-55% of the height, captions 190 px below the feet, replies just above the head.
20. **Shot continuity:** keep one location and one camera angle for the floor scenes; the only change of place is
    the real cut-away. Brightness ~58% mean luma, warm, low saturation (~0.12), clean (no added grain or filters).
21. **Overlays are screen-fixed, everything else is in the world:** captions, counter and replies don't move with
    the drift; Vex, props, shadows and fallen objects do.
22. **Running time ~31 s** for this format (the channel's own 40-50 s rule may still apply to Interestingly Strange
    uploads; this reference shows how much story fits in 31 s).
23. **Motion cadence (low priority):** the reference picture moves at 24 fps (frames repeated to reach 30) while the
    overlays change on the 30 fps grid; holds of up to ~0.3 s are used to fit the dialogue.
