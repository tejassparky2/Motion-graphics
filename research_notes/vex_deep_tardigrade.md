# Deep study: "Grim, try and kill this tardigrade" (reference for the Vex series)

Frame-by-frame and sample-by-sample measurements of the owner's reference Short (another creator's mascot "Grim").
We copy technique, pacing, layout, audio and structure, never Grim's design. The video file is not in the repo (public).

- File: 41.82 s container, 720x1280, 30 fps, H.264 High at 834 kb/s, keyframe every 150 frames (5 s); audio HE-AAC 44.1 kHz.
- Last video frame: #1250 (41.67 s). Audio ends 41.73 s.
- Motion cadence: during any movement exactly 1 frame in 5 is a duplicate (patterns `#.###` / `##.##` over the whole
  video), so everything was **animated/edited at 24 fps** and delivered at 30 fps.
- Method: all 1,251 frames decoded to numpy. Per-region frame differences, background phase correlation, shadow fitting
  against a frame where Grim is off screen (16.6 s), text masks, 30 fps contact sheets of every action, RMS/spectral
  analysis of the audio, pitch tracking (f0.py), syllable peaks.
- All pixel values are at the full 720x1280 unless marked otherwise. "Luma" = 0.299R+0.587G+0.114B.

---

## 1. Shot and camera

**One locked-off shot for the whole 41.7 s.** There are no cuts, pans, zooms, push-ins or handheld wobble.
- Phase correlation of the background (sofa strip and floor) between any two frames from 2 s to 41.7 s: shift **0 px**
  (dx 0, dy 0).
- Frame-to-frame mean abs difference on clean background patches (360-wide copy): median **0.10-0.18** levels, which is
  compression noise. The only spikes are the keyframe refreshes every 5.00 s (frames 150, 300 and so on, ~1.6-2.1 levels)
  and two steps (below).
- **Two exposure steps, no geometry change:** at **15.03 s** the whole background gets ~3% darker (floor 177.9 to
  172.9), and at **30.07 s** another ~2.5% (172.1 to 168.4). These are joins between three takes of the same locked
  shot (0-15.03, 15.03-30.07 and 30.07-41.7). They aren't noticeable when watching.
- **Real footage where the hand appears:** during the two hand moments the untouched floor and sofa drift 1-2%
  in brightness (sofa 134.7 to 137.7 over 0.1-1.3 s, then 130.9 to 128.0 over 26.4-28.3 s): that's phone auto-exposure
  reacting to the hand. Everywhere else the plate is as still as a photo.
- **Conclusion for us:** a single still photo of the floor (or a tripod clip) is all it takes. The camera never moves.
  Note that our kit's `photo()` adds a 5% push-in over 6 s ("no shot is ever static"), and the reference has none.

**Framing.**
- Floor fills ~85% of the frame. The only furniture is the base of a light grey fabric sofa, a diagonal strip from
  y≈0-50 at the left edge to y≈0-220 at the right edge, with one round wooden leg at x≈150-210, y≈50-135. Above the
  characters there's nothing but floor (headroom y≈220-515).
- Light oak laminate planks run diagonally (bottom-left to top-right), giving strong leading lines toward the
  characters and the sofa.
- Camera height and angle (estimated from plank foreshortening and the hand scale): phone ~0.6-0.9 m above the floor,
  tilted ~45-50° down. It's a normal phone main lens: plank seams stay straight, with no wide-angle bulge.
- Scale: the owner's fingertip is ~40 px wide where it touches the tardigrade, so the characters are **toy-sized,
  about a finger long (~9-10 cm)**.

**Exposure and colour.**
- Bright, soft, mid-key, low contrast: mean luma of the whole frame **148/255 (58%)**, with p5 90 and p95 177.
- Floor luma 150-160 (mid/bottom) and ~129 (top); sofa ~141.
- White balance slightly warm. Floor mean RGB (171,147,126) at the bottom and (177,156,136) in the middle, a ratio
  R:G:B = 1.15:1:0.87. The near-neutral sofa reads 1.08:1:0.95.
- Soft daylight with no hard cast shadows in the room.

**Sharpness, noise and compression.**
- Soft phone image: the high-pass std of the floor is 3.6 levels, against 12-23 on the cartoon line work.
- No visible grain; static areas show only H.264 smoothing.
- The cartoons are noticeably crisper than the photo, and that contrast is part of the look.

---

## 2. Mascot rendering

**Size and position** (measured from the dark silhouette and from difference masks; Grim without props):

| item | value |
|---|---|
| Grim height | head top y≈516-524, feet y≈746-750, so **≈228 px = 17.8% of 1280** |
| Grim width | hood ≈170-195 px (24-27% of 720) |
| Grim centre x | 247-262 front view, 215-243 side view with a gun, **≈250 typical (35% of width)** |
| Head share | the hood/head is ≈150 of the 228 px (≈65%): big head, tiny body |
| Tardigrade (normal form) | x≈355-590 (w≈232), y≈595-760 (h≈165), centre x≈470 |
| Tardigrade (standing up) | y≈482-769 (h≈287) |
| Tun form | x≈380-575 (w≈195), y≈650-765 (h≈110-130) |
| Ground line | both characters' feet at y≈750-765 (58.6-59.8% of height) |
| Gap between them | 10-25 px: they stand almost touching, side by side |
| The pair | x≈120-590, y≈515-765, so the pair's centre is ≈(355, 640) = **the exact frame centre** |

- Grim's ground position never changes, apart from the two dash exits and entries and the final lunge (+60 px right at
  41.43 s).
- Props extend the silhouette to x≈25 (scythe on the left), x≈396 (gun muzzle) and y≈383 (scythe raised).

**Line and colour.**
- Outer silhouette: a dark rim 5-7 px thick (the hood edge scans as 6 px of luma <20). There's no white sticker border;
  floor goes to outline in a 2-3 px antialiased step (158 → 107 → 36).
- Inner feature lines (brows, mouth, eye rims, tardigrade folds) are 2-3 px. The tardigrade's lines are dark brown
  (68,41,11), not black.
- Palette:
  - Grim: cloak near-black with a slight blue/purple cast (13,9,22); face white (248,250,250) with light grey shading;
    hood lining red-orange ≈(204,60,12); eyes yellow with white highlights; pink hatched blush.
  - Tardigrade: beige fill ≈(212,190,161) with tan shading ≈(180,156,132) and dark brown lines.
  - Tun: darker brown ≈(156,120,95).
- Style: polished vector/cel look, flat fills plus one soft shade tone (the cloak has two near-black tones, the face a
  light grey shade). No gradients beyond that, no texture, no added blur or grain to match the footage.

**Grounding: one soft drop shadow per layer.** Fitted on frame 485 against frame 500 (Grim absent):
- The shadow is Grim's whole silhouette, scythe included, **offset down-right** (best fit: dy≈+160 px, dx≈+120 px for the
  whole layer). It's blurred with a **Gaussian σ≈50 px**, and its core darkens the floor by ≈18-26 luma on 160
  (**≈12-16%**).
- It's slightly warm: channel ratios in the core are 0.83/0.77/0.72 (R/G/B).
- The tardigrade has the same kind of soft shadow: a dark band below and right of its feet, x≈450-640, y≈750-820.
- No hard contact shadow and no ellipse under the feet.
- Effect: the characters look like figures standing on the floor, lit from the upper left.

**Viewing angle.** Drawn as if seen slightly from above (we see the top of the hood and the tardigrade's back), which
matches the camera tilt. Front and 3/4 views only; Grim is never shown in profile except while holding the guns.

---

## 3. Mascot animation

**Animation style.**
- Every move is fully in-betweened at 24 fps, with a new drawing on every 24 fps frame. Turns, twirls and morphs are
  smooth (they look like image-to-video clips or full frame-by-frame animation, not stepped cut-outs).
- Between actions the picture is **dead still**: pixel-identical frames, no idle bob, no breathing, no blinking, no mouth
  flaps.
- Grim is a skull and never lip-syncs. When he "talks", at most there's a small head tilt (38.0-38.2 s and 38.85-39.1 s),
  or nothing at all ("but y tho?" plays over a frozen pose).
- Motion is on screen in **66% of frames**. The longest fully still stretch, with nothing moving and no text change, is
  **1.03 s** (30.60-31.63); the next longest are 0.90, 0.83 and 0.77 s.

**Grim: every pose/drawing change (≈18 distinct drawings in 41.7 s, one per ~2.3 s).**

| time (s) | change | how |
|---|---|---|
| 0.00-0.83 | front view, big glossy eyes, paws clasped, red hood lining visible | still |
| 0.83-0.90 | turns to 3/4 right (toward the tardigrade/hand), worried brows | quick 2-3 frame turn, settles by 1.9 |
| 3.43-3.67 | turns front; scythe **twirls out** from low right to upright on his left; angry narrowed eyes | 7-frame twirl, whoosh |
| 3.70-5.90 | holds scythe upright ("ok fine") | still |
| 5.93-6.60 | lowers the scythe to the floor, turns 3/4, curious | smooth |
| 8.40-8.90, 10.65-11.10 | small leans / eye changes ("ew") | subtle |
| 11.40-11.53 | eyes go flat and unimpressed | subtle |
| 12.37-13.40 | slow turn to the camera with disgusted half-lidded eyes ("it so gross") | 1 s turn |
| 15.60-15.67 | **hard swap** to happy face plus thumbs-up ("ok!") | 2-frame cut |
| 16.37-16.47 | turns away, **dashes off left** with a motion smear | 3 frames |
| 16.50-16.77 | empty floor (Grim gone) | 0.3 s |
| 16.80-16.93 | **dashes in** from the left: side view holding a grey flamethrower | 4 frames, smear |
| 17.20-18.47 | fires the flame | effect |
| 18.80-19.17 | turns to front, flamethrower held down, big eyes ("its a tun", "of gross") | smooth |
| 20.70-20.80 | turns, dashes off | 3 frames |
| 20.83-21.00 | empty | 0.2 s |
| 21.03-21.13 | dashes in with a **ray gun** (green glowing muzzle, radiation badge) | 3-4 frames |
| 22.33-23.47 | fires the beam, squinting | effect |
| 24.77-24.83 | turns front, gun held forward | smooth |
| 25.00-26.17 | gun swings round until its muzzle points **at the camera/keeper** (foreshortened, big) | smooth, 2 clicks |
| 27.73-27.87 | gun lowered (removed) | quick |
| 28.27-28.60 | front, sad, paws together ("sorry") | smooth |
| 32.83-33.00 | turns 3/4 to watch the rain | quick |
| 37.73-37.80 | turns front, curious ("wat if... i kill it... in this form?") | 3 frames, plus 2 head tilts |
| 40.13-40.20 | turns 3/4, determined | quick |
| 40.63 | scythe appears in his paws (low) | pop |
| 40.67-41.30 | **wind-up**: raises the scythe overhead | 0.6 s |
| 41.33-41.40 | swing (blade arcs over the tardigrade) | 2 frames, smear |
| 41.43-41.53 | white 8-point **starburst flash** over the impact; Grim lunges right | 4 frames |
| 41.57-41.67 | result: tardigrade in two halves, scythe planted in the floor | 4 frames, then cut |

- Front vs 3/4: Grim faces the camera for 7 of his 9 replies (talking to the keeper) and turns 3/4 toward the
  tardigrade when acting or watching.
- Props always enter "off camera": a dash out and back in with a new prop, or a twirl that brings it into his paw.
  There are no slide-ins and no scale pops on props.
- Effects, all flat 2D in the same art style:
  - Flame 1.27 s: yellow core, orange body, red-orange edge and black outline; it flickers to a new shape every frame,
    grey smoke puffs rise behind it, and the floor under it gets a warm glow. It cuts in a single frame at 18.47, with a
    few embers and smoke left until 18.6.
  - Green beam 1.13 s: it shoots out to the frame edge in 3 frames, is translucent, has black zig-zag "zap" squiggles
    above and below, and puts a green glow on the floor. It retracts to a thin line at 23.47.
  - Slash: starburst 0.13 s, then white impact streaks for one frame.

## 4. The other creature (the tardigrade) and props

- Same art style and scale as Grim: chunky 4-legged body with 8 clawed stubby legs, small dot eyes and a round tube
  mouth. The beige body has folds drawn as 2 px brown lines. It never speaks.
- Its states:
  1. 0-2.77 s: side view facing Grim; still (the finger pokes it 0.6-1.0 s).
  2. 2.77-3.13 s: turns its face to the camera.
  3. 4.37-4.97 s: rears up on its hind legs with both arms raised (alarm), with a rising squeak. Held 5.0-5.9.
  4. 6.0-10.5 s: **slow 4.5 s morph**: crouches, hugs itself, shrinks and curls into the tun. Its colour darkens from
     beige to brown and its eyes become closed lines.
  5. 10.5-33.3 s: tun, completely still, unharmed by the flame and the beam.
  6. 33.3-35.0 s: rehydrates under the rain (swells back, colour lightens).
  7. 36.9-37.1 s: turns its face to the camera again ("good as new").
  8. 41.57 s: cut in two, with ham-pink cross-sections.
- Props:
  - Scythe: brown shaft, grey blade, black outline.
  - Flamethrower: grey/olive.
  - Ray gun: dark grey with a green radiation symbol and a glowing green muzzle.
  - Rain cloud: slate fill (129,142,159) ≈ #818E9F, black outline ≈4 px, about 340x150 px. It enters from the top-left
    corner at 31.70 and reaches its rest position (centre ≈(480,335)) by 32.53 (0.83 s, near-linear). It rains from 32.77
    (simple blue teardrops falling in a loop), leaves back to the top-left 35.50-36.13 (0.63 s), and doesn't rotate.

---

## 5. Text on screen

Two text types. **They are never on screen together**: strict turn-taking, keeper caption, then mascot reply, then
caption. Text is visible 85% of the time; the text-free gaps add up to 6.1 s, the longest being 0.74 s.

### (a) Keeper captions
- **Font:** Comic Sans MS Bold look. Single-storey a and g, wavy T. **Comic Neue Bold at ≈64 px em** reproduces it
  (Comic Neue x-height 0.487 em gives 31 px).
- **Size and colour:** white fill, **x-height 31 px, ascender/cap 46 px** (white part only), letter stroke ≈9-10 px
  thick.
- **Outline:** solid black, **4-5 px visible** outside the white (a centred stroke of ≈9-10 px). No drop shadow, no
  glow, no box.
- **Position:** centred at x=358-360.
  - One line: top 879, **baseline ≈925**.
  - Two lines: line 1 top 847 / baseline ≈894, line 2 top 911 / **baseline ≈958**, line pitch **64 px**.
  - Single and double lines share the same vertical centre, **y≈902 (70.5%)**, about 90-100 px below the characters'
    feet.
  - Widest line 630 px ("they become the most" = 20 characters, ~31 px per character), so lines are ≤~20-22
    characters. Never more than 2 lines. Line breaks are manual, at phrase boundaries ("no matter what / u do").
- **Writing style:** all lower case except "Tardigrade" in the first caption and the scream "OH MY GOD".
  - Txt-speak: "u", "ur", "thats", "its" (no apostrophes).
  - No commas or full stops; "!" sometimes; single quotes around the new term ('tun'); British spelling "shrivelled".
  - The scream is the only all-caps caption.
  - Repetition is shortened: 6 spoken "whoa"s become "woah woah woah".
  - A cut-off word is written out with a dash: "it would die-".
- **Unit:** one phrase/clause per caption; **4.6 words on average** (2-8).
- **Timing:** appears within ±0.05 s of the first spoken word (once +0.29 s) and disappears 0.1-0.5 s after the last
  word. The whole caption appears at once and is cut on/off with no pop, fade, scale or karaoke. **Average 1.26 s on
  screen** (0.63-2.37).
- The caption is fully visible from **frame 0**.

| on-off (s) | caption (exact) | lines |
|---|---|---|
| 0.00-1.67 | grim try and kill / this Tardigrade | 2 |
| 2.57-3.50 | just try | 1 |
| 5.07-6.00 | now watch this | 1 |
| 6.67-7.93 | when tardigrades / are stressed | 2 |
| 7.93-9.50 | they become the most / invincible animal | 2 |
| 9.50-10.63 | in the whole world | 1 |
| 11.63-13.17 | they can even / survive outer space! | 2 |
| 14.43-15.70 | now try killing it! | 1 |
| 17.10-19.03 | this shrivelled form / is called a 'tun' | 2 |
| 20.17-21.23 | ha good one | 1 |
| 21.23-22.63 | it can survive / immense heat | 2 |
| 22.63-23.63 | or radiation | 1 |
| 23.87-25.57 | thats enough to kill / a human u know | 2 |
| 26.13-27.20 | woah woah woah | 1 |
| 27.20-28.17 | watch where ur / pointing that | 2 |
| 29.70-30.57 | no matter what / u do | 2 |
| 30.57-32.93 | when its in 'tun' / form its invincible | 2 |
| 33.23-34.27 | give it a little water | 1 |
| 34.27-35.93 | and its right back / to normal form | 2 |
| 36.67-37.40 | good as new | 1 |
| 40.13-41.07 | well then i guess / it would die- | 2 |
| 41.07-end | OH MY GOD | 1 |

### (b) Mascot replies (red)
- **Font:** the **same comic font and the same size as the captions** (x-height ≈30 px, ascender ≈45 px). It is
  **not handwriting**.
- **Fill:** coral red **(242,66,73) = #F24249**. **Outline:** black, 4-5 px. No shadow.
- **Position (fixed):** centred at **x≈248** (over Grim's centre), **baseline ≈473** (ascender top 420-435), i.e.
  ≈45 px above the top of his hood. It stays at the same place every time.
- **Timing:** on 0-0.12 s before the squeak starts, off right after it ends. Instant on/off with no pop, bob or fade
  (the bounding box is identical from the first frame). **Average 0.72 s** (0.46-1.07). 1-3 words.
- **Writing style:** baby txt-speak: "y tho", "wat", "it so gross" (dropped verb), "of gross" (sic), "i kill it".

| on-off (s) | reply (exact) | squeak syllables / length |
|---|---|---|
| 1.67-2.57 | but y tho? | 3 / 0.94 s |
| 3.90-4.80 | ok fine | 3 / 0.90 s |
| 10.93-11.47 | ew | 1 / 0.22 s |
| 13.37-14.43 | it so gross | 3 / 0.90 s |
| 15.77-16.43 | ok! | 1-2 / 0.61 s |
| 19.17-19.63 | its a tun | 3 / 0.42 s |
| 19.63-20.20 | of gross | 2 / 0.60 s |
| 28.73-29.53 | sorry | 2 / 0.65 s |
| 38.03-38.60 | wat if | 2 / 0.42 s |
| 38.60-39.40 | i kill it | 3 / 0.73 s |
| 39.40-40.10 | in this form? | 2-3 / 0.69 s |

- There are no other overlays: no hook title, no counter, no series chip, no subscribe text, no emoji, no frame.

---

## 6. Audio

**Mix.**
- **No music at all.** Every pause sits on the same flat room tone, ≈-48.8 dBFS, low-frequency only (rumble plus faint
  59/118 Hz hum, nothing above 3 kHz).
- Integrated loudness ≈**-17 LUFS** (BS.1770 estimate); sample peak -0.2 dBFS.
- Only **5.1 s (12%)** of the video is silent (pauses ≥0.2 s). The longest pause is **0.84 s** (5.82-6.66), filled
  on screen by Grim lowering his scythe and the tardigrade starting to curl.

**Keeper (off-screen owner).**
- Adult, almost certainly male. Casual, amused, conversational, as if talking to a pet.
- Pitch: medians 115-230 Hz per line (calm explaining lines 138-162 Hz; excited lines 197-244 Hz; "whoa ×6" 244 Hz).
  The final "OH MY GOD" is a scream at **320 Hz**.
- 108 words in 16 lines. **≈4.2 words/s while speaking** (3.4 on fact lines, 5.4-6.3 on asides like "that's enough to
  kill a human, you know" and "watch where you're pointing that").
- Voice peaks capped at **-3.4 dBFS** (limited); line RMS -15.8 to -18.2 dBFS; the scream -12.
- Close mic in a dry room: lines decay to the floor in ~150-250 ms, with no audible echo. The room tone is left in
  (not gated): phone or lav quality.
- Keeper and mascot never overlap. The keeper answers 0-0.4 s after Grim's squeak ends (often on the same frame); Grim
  answers 0.2-0.95 s after the keeper.

**Mascot (Grim).**
- Cute gibberish, not English. The syllable count matches the red text exactly (but y tho = 3 peaks, ok fine = 3,
  ew = 1, it so gross = 3, its a tun = 3, of gross = 2, sorry = 2, wat if = 2, i kill it = 3).
- 3.2-4.4 syllables/s, a normal speaking rate (not sped-up chipmunk speech). Lines last 0.22-0.94 s.
- It reuses a tiny set of sounds: Whisper hears "Water." for "sorry" and "This water, this water, this water." for "wat
  if / i kill it / in this form?".
- Pitch **median 395-420 Hz** (all lines, range ≈340-460 Hz), almost monotone (within ±1-2 semitones), often with a
  small fall at the end (420 to 371 Hz in "but y tho?") and a rise on "ok!" (345 to 459 Hz).
- Bright, airy timbre: about 10 dB more energy above 6 kHz than the keeper.
- Level 1-2 dB below the keeper (RMS -18.4 to -20.9 dBFS).
- Whisper's transcript skips most of Grim's lines; the red text is the only "translation".

**Sound effects** (one per prop action; ~12 in total, all synced to the frame):

| time (s) | sound | level | on screen |
|---|---|---|---|
| 3.35-3.65 | soft whoosh | -26.5 dBFS RMS | scythe twirl |
| 3.88 | small click | peak -18 | scythe stops |
| 4.55-5.00 | rising squeak/whistle (glide ~250 to 700 Hz with harmonics) | -26.7, peak -4.5 | tardigrade rears up |
| 16.38-16.62 / 16.72-16.95 | whoosh out / softer whoosh in | -21 / -33 | Grim dashes off / back |
| 17.15-18.45 | flamethrower roar (broadband) | -12.6 (with speech), peak -0.3 | flame |
| 20.72-20.92 / 20.95-21.15 | whoosh out / in | -20 / -33 | dash off / back |
| 22.33-23.47 | beam buzz/roar with a falling tone | -12.4 beam alone, peak -0.2 | green beam |
| 25.05, 25.20 | two clicks (gun aim) | peak -6 | gun swings to the camera |
| 32.72-35.40 | light rain hiss bed | -36.7 | rain |
| 36.12-37.40 | sparkle/chime (bright partials 2.6-10 kHz, decaying) | -11, peak -1.5 | "good as new" |
| 40.9 | short noise burst (scythe swish or the cut-off "di-") | peak -9 | scythe pulled |
| 41.45-41.70 | slash "shing" under the scream | -11.5, peak -0.7 | starburst |

- Loud effects (flame, beam, sparkle, slash) are mixed **4-6 dB louder than the voices** and run under the keeper's
  fact line. Whooshes and clicks are quiet.
- The audio fades out in under 30 ms at the end: a hard cut while it's still loud.

---

## 7. Script and structure

| time (s) | speaker | words (spoken / shown) | on screen | fact |
|---|---|---|---|---|
| 0.00-1.46 | keeper | "Grim, try and kill this tardigrade." | both characters, caption from frame 0; **real finger from the top pokes the tardigrade** 0.10-1.43; Grim turns, worried | dare |
| 1.66-2.60 | Grim | squeak, *but y tho?* | worried hold | |
| 2.56-3.02 | keeper | "Just try." | tardigrade looks at the camera | |
| 3.43-4.80 | Grim | twirl, squeak, *ok fine* | scythe out, angry | attempt 1 |
| 4.4-5.9 | (tardigrade) | squeak | rears up, arms raised | |
| 4.78-5.86 | keeper | "Now watch this." | hold | promise |
| 6.68-10.52 | keeper | "When tardigrades are stressed, they become the most invincible animal in the whole world." | 4.5 s curl into a tun | stress → tun → toughest animal |
| 10.96-11.18 | Grim | *ew* | flat eyes | |
| 11.58-13.08 | keeper | "They can even survive outer space." | Grim slowly turns to the camera, disgusted | survives space |
| 13.38-14.28 | Grim | *it so gross* | | |
| 14.46-15.62 | keeper | "Now try killing it." | | **re-dare at 35%** |
| 15.88-16.50 | Grim | *ok!* | thumbs-up, dashes off and back with a flamethrower | attempt 2 |
| 17.02-18.70 | keeper | "This shriveled form is called a tun." | flame 1.27 s on the tun | the word "tun" |
| 19.21-20.25 | Grim | *its a tun / of gross* | turns to the camera | |
| 20.14-20.76 | keeper | "(ha) Good one." (laughs at the joke) | Grim dashes off, back with a ray gun | attempt 3 |
| 21.20-23.26 | keeper | "It can survive immense heat or radiation." | green beam 1.13 s | heat + radiation |
| 23.84-25.10 | keeper | "That's enough to kill a human, you know." | Grim turns the gun **toward the camera** | lethal dose for humans |
| 26.12-28.16 | keeper | "Whoa ×6. Watch where you're pointing that." | **real hand from the bottom** blocks (stop gesture) 26.37-28.5 | **gag/re-hook at 62%** |
| 28.81-29.45 | Grim | *sorry* | sad | |
| 29.62-32.56 | keeper | "No matter what you do, when it's in this tun form, it's invincible." | rain cloud slides in | invincible only as a tun |
| 33.24-35.86 | keeper | "Give it a little water, and it's right back to normal form." | rain, tun swells back | water revives it |
| 36.52-37.20 | keeper | "Good as new." | sparkle SFX, tardigrade looks at the camera | |
| 38.15-40.11 | Grim | *wat if / i kill it / in this form?* | curious head tilts | **the mascot's own idea (91%)** |
| 40.10-41.0 | keeper | "Well then I guess it would d-" | Grim turns, takes the scythe, winds up | |
| 41.02-41.70 | keeper | "OH MY GOD" (scream) | swing, starburst, tardigrade in halves | **payoff, cut** |

- **Hook (0-2 s):** the keeper's dare naming both characters is the first word at 0.00. The full caption is on screen
  from frame 0. Both characters are visible, large and centred, at frame 0. A real finger pokes the creature from
  0.10 s, and the mascot answers by 1.67 s. There's no title card and no "did you know".
- **Escalation:**
  1. Threat with a scythe (the creature curls up).
  2. Flamethrower (heat).
  3. Ray gun (radiation).
  4. The gun is aimed at the keeper himself, a meta gag with a real hand.
  5. Reversal: water undoes the tun.
  6. The mascot proposes killing it in the vulnerable form.
  7. He does it before the keeper finishes his sentence.

  Each attempt carries one fact, spoken by the keeper over the action. A new prop or attempt lands every ~4-6 s:
  3.4, 16.8, 21.0, 25.1, 31.7 and 40.6 s.
- **Re-hooks:** "now try killing it!" at 14.5 s (35%), the gun pointed at the camera plus the real hand at 26 s (62%),
  and the mascot's question at 38 s (91%).
- **The twist is a true fact used as the punchline:** tardigrades are only "invincible" while dried out as a tun.
  Rehydrated, they're ordinary tiny animals. The keeper's explanation sets the trap; the mascot springs it.
- **Ending, last 3 s at 30 fps:**
  - 38.70-39.40: "i kill it" shown, Grim front, head tilt.
  - 39.40-40.10: "in this form?".
  - 40.10-40.13: one frame with no text.
  - 40.13: caption "well then i guess / it would die-".
  - 40.13-40.20: Grim turns 3/4.
  - 40.63: scythe in his paws.
  - 40.67-41.30: wind-up; 41.07: caption becomes "OH MY GOD".
  - 41.33-41.40: swing (2 frames, smear).
  - 41.43, 41.47, 41.50, 41.53: white starburst flash.
  - 41.57: streaks, halves visible.
  - 41.60, 41.63, 41.67: hold on the result. **Hard cut after frame 41.67**: no freeze-frame, no black, no outro, no
    question, no call to action. The result is on screen only ~0.13 s before the cut.

---

## 8. Pacing

- **Visible changes per 10 s** (text appearing plus motion onsets): **0-10 s: 11, 10-20 s: 15, 20-30 s: 14,
  30-40 s: 11, 40-41.7 s: 3.** That's ≈1.1-1.5 per second; a new caption or reply appears every 1.26 s on average.
- Motion onsets alone: 3 / 7 / 6 / 4 / 1. The long motions are continuous (the 4.5 s curl, the 4.4 s cloud and rain).
- Longest fully still stretch: **1.03 s**. The characters move or effects run in 66% of frames.
- Caption duration: **1.26 s average** (keeper, 22 captions); reply **0.72 s average** (11 replies).
- Talk ratio: the keeper speaks ~26 s, Grim ~7 s, silence 5 s.

## 9. Real-world elements

- **Hand 1 (0.10-1.43 s):** the owner's arm enters from the **top** edge, the index finger points at and presses
  the tardigrade's back (0.6-1.0 s, the fingertip "pushing in" at its top contour), then withdraws upward.
  - The hand is layered **in front of** the cartoon (the finger covers the tardigrade), so it's rotoscoped/masked or the
    cartoon is masked around it.
  - Captions stay on top of the hand.
  - Lighting matches by construction: it's the same locked phone shot, with auto-exposure drifting 1-2% while the hand
    is in frame.
  - Slight motion blur on the fast moves.
- **Hand 2 (26.37-28.5 s):** an open hand rises from the **bottom** edge to a "stop" block in front of the gun and the
  tun (back of the hand to the camera, fingers up, filling the bottom ~55% of the frame up to y≈615), then sinks out.
  Again layered above the characters and below the caption.
- There are no other real elements: no face, no POV walk, no other footage.
- The real hand doubles as a **scale reference** (the characters are toy-sized) and as proof that "the keeper is
  really there".

---

## Rules to copy, most important first

1. **One locked-off shot, the whole video.** A single bright floor plate (still photo or tripod clip): no push-in, zoom,
   pan, cut or shake (the reference moves 0 px in 41.7 s). This clashes with the channel's "slow push-in on every
   scene" rule (CLAUDE.md research rules); the owner should decide for this series. Our `vex_kit.photo()` currently
   pushes in 5% over 6 s and switches photos.
2. **Framing:** camera ~0.6-0.9 m up, tilted ~45-50° down. Floor ≈85% of the frame; furniture only as a diagonal strip
   in the top 3-17% (y 0-220). Mean luma ≈148/255 (58%), floor 150-160, low contrast (p5 90 / p95 177), warm WB
   (floor R:G:B ≈ 1.15:1:0.87).
3. **Characters big, centred and still on one ground line.** Mascot ≈225-230 px tall (17.8% of 1280), head top
   y≈516-524, feet y≈750, centre x≈250. Co-star centre x≈470, feet on the same line. Gap ≤25 px; the pair's centre is
   ≈(360, 640). The mascot doesn't drift; he only leaves by dashing.
4. **Toy scale:** size characters so that a real fingertip (~40 px) is a quarter of the mascot's width (characters
   ≈9-10 cm "real").
5. **Grounding = one soft drop shadow per character/prop layer:** silhouette offset down-right (≈+60-160 px down,
   +40-120 px right), Gaussian σ≈50 px, core darkening 12-16% (≈-20 luma on 160), slightly warm. No hard contact
   shadow, no ellipse.
6. **Art:** flat cel fills plus one shade tone, dark outer rim 5-7 px, feature lines 2-3 px (brown lines on the
   light-coloured co-star), crisp 2-3 px antialiasing, no sticker border, no added blur or grain. Props, effects and the
   co-star are in the **same** style as the mascot.
7. **Animate, then freeze:** every action is a smooth in-betweened move at 24 fps with a new drawing on every frame
   (turns 0.1-1 s, prop twirl 0.25 s, dash 0.1 s, morph up to 4.5 s), then a **dead-still hold** while text/speech
   plays. No idle bob, breathing, blinks or mouth flaps; at most a small head tilt on a reply.
8. **≈18 distinct poses/expressions in 42 s** (one every ~2.3 s). Every attempt brings a new prop plus a new face. The
   mascot faces the camera when replying to the keeper and turns 3/4 toward the co-star when acting.
9. **Prop changes by dash:** dash off-screen left in 2-3 frames with a motion smear, 0.2-0.3 s of empty floor, dash back
   in 3-4 frames holding the new prop, with a whoosh out (-21 dBFS) and a softer whoosh in (-33 dBFS). Or a 7-frame
   twirl that brings the prop into the paw.
10. **Keeper captions:** Comic Neue Bold ≈64 px em (white x-height 31 px, ascender 46 px), white fill, black outline
    4-5 px visible (stroke ≈9-10 px), no shadow, centred x=360. One line: baseline ≈925. Two lines: baselines ≈894 and
    ≈958 (pitch 64). Block centre y≈902, about 90-100 px below the feet. Lines ≤20-22 characters (≤630 px), max 2,
    manual breaks at phrase boundaries. Our kit now uses 48 px with baseline 870.
11. **Caption writing:** all lower case, txt-speak (u, ur, thats, its), no commas or full stops, "!" allowed, 'quotes'
    on the new term, ALL CAPS only for the final scream. One phrase per caption (≈4.6 words), on within ±0.05 s of the
    first word, off 0.1-0.5 s after the last, hard cut on/off (no pop, fade or karaoke). Average 1.26 s. The first
    caption is visible from frame 0.
12. **Mascot replies = same comic font and size as the captions,** fill coral **#F24249**, black 4-5 px outline,
    centred over the mascot (x≈248), baseline ≈473 (≈45 px above his head), fixed position. 1-3 words of baby txt-speak
    ("but y tho?", "it so gross", "wat if"), on 0-0.1 s before the squeak, off right after it, hard on/off. Average
    0.72 s. Our kit uses Kalam handwriting, #EB1F26, a white outline, a pop-in and a bob: all four differ.
13. **Strict turn-taking:** a caption and a reply are never on screen together. Text is visible ≈85% of the time; gaps
    ≤0.75 s. The voices never overlap; the replies come 0.2-0.95 s after the keeper, the keeper 0-0.4 s after the reply.
14. **Mascot voice:** cute gibberish with exactly one syllable per syllable of the red line, at a normal rate (3.2-4.4
    syllables/s, 0.2-0.95 s per line). Pitch ≈395-420 Hz median (340-460), near-monotone with a slight fall at the end.
    Bright and airy; 1-2 dB under the keeper. Reuse a small syllable set (it sounds like "wa-ta / di-wa-ta").
15. **Keeper voice:** a real, casual voice talking to a pet. ≈4.2 words/s on lines, faster on asides. Laughs ("ha good
    one"), panics ("whoa" ×6), screams the payoff. Dry room, room tone left in (≈-49 dBFS), peaks limited ≈-3.4 dBFS,
    whole video ≈-17 LUFS.
16. **No music.** Sound is voices, room tone and ~12 synced SFX: quiet whooshes and clicks for moves; loud flame, beam,
    sparkle and slash 4-6 dB above the voices (peaks ≈0 dBFS) under the keeper's fact lines; a quiet rain hiss bed
    (-37 dBFS). Pauses ≤0.84 s and always filled by visible action; total silence ≈12%.
17. **Opening:** at 0.00 the keeper's dare naming the mascot and the co-star ("Grim, try and kill this tardigrade").
    Both characters and the full caption are visible at frame 0. A physical "proof" beat in the first second (real
    finger pokes the co-star 0.1-1.4 s). The mascot's first reply by ≈1.7 s.
18. **Body = attempts, each carrying one fact from the keeper:** 3 escalating attempts (here scythe 3.4 s, flame 16.8 s,
    ray gun 21 s), 7 fact beats in total, the keeper explaining while the effect plays. The co-star reacts visibly
    (rears up, curls, rehydrates) so every fact has a picture.
19. **Re-hooks:** a re-dare at ~35% ("now try killing it!"); a meta gag at ~60% where the mascot turns the weapon on the
    keeper/camera and a real hand blocks it ("woah woah woah", "sorry").
20. **Twist from a true fact, proposed by the mascot:** the reversal (water restores it, 80%), then the mascot's own
    question ("wat if i kill it in this form?", 91%), then the keeper's sentence is cut off by the act ("it would die-"),
    scream, **hard cut ≈0.13 s (4 frames) after the result appears**: no freeze, black, outro, question or call to action.
21. **Effects in the cartoon style:** flame 1.27 s (flickers every frame, smoke puffs, warm floor glow); beam 1.13 s
    (shoots out in 3 frames, translucent green, black zig-zag zaps, floor glow); weather/cloud prop slides in from a
    corner in ≈0.8 s and out in ≈0.6 s; the hit is a white 8-point starburst for 4 frames.
22. **Real hand twice** (≈1.3 s and ≈2.1 s), entering from a frame edge (top, bottom). It sits in front of the
    characters and behind the captions, shot on the same locked camera so the light matches.
23. **Pacing targets:** 11-15 visible changes per 10 s; motion on screen ≈2/3 of the time; no fully still stretch longer
    than ≈1.0 s; 40-45 s total.
24. **No other overlays:** no hook title, counters, chips, stamps, buttons, emojis or frames. The only graphics are the
    two text types and the in-world props and effects.
