# S22E14 "Evolving Research!": story and animation deep dive (30 Oct 2026)

Study of ONE episode the owner supplied, so that we can write and animate our own original series with the same
craft. We borrow technique only: no plot, characters, designs, names or frames go into our videos. The video,
frames and transcript stay in the private scratchpad; nothing from them is in this repo except these notes.

**Sources and how far to trust them**
- Video: English dub, 21:19, 23.976 fps, 858x480. All times below are file times (m:ss.s) in that file.
- Dialogue: the automatic Whisper-small transcript, plus my own Whisper **medium.en** pass over the stretches where
  the small model dropped most lines (e.g. 1:48-2:08, 3:10-4:10, 6:24-6:42, 11:25-13:10 and 19:10-20:25). The
  small model's timestamps also drift by up to ~70 s in places: it puts the 20:21 "treasure dive" line at 19:08.
  Both models mishear names. A name is corrected only where the picture or the dialogue proves it; otherwise it is
  marked uncertain. Medium also hallucinated over music (a run of "Ooh!" at 5:57-6:17, "I'll see you in the next
  video" at 10:52, "Thanks for watching!" at 18:50), and I ignored those.
- Shots: `shots.json` automatic cut detection (415 shots; "#N" below = its shot number, the same numbers as the
  contact sheets). I checked it by eye in four places:
  - It **misses cuts in dark or same-coloured scenes.** #357 (18:24.9, "27.6 s") is really about 5 shots plus a fade
    to black. #187 (10:34.7, "15.9 s") is about 4 shots. In the dialogue stretch 8:39.7-9:23.7 I count about 14-15
    shots by eye against 11 detected.
  - It is **about right in effect-heavy shots.** The cuts in the Charjabug evolution (13:39-13:50) are real cuts of
    0.25-0.9 s.
  - So dialogue medians below are probably ~0.5-0.8 s too long, and night and cave scenes too long by more.
  - The earlier study in `channels/monsters/ANIME_STUDY.md` used a different detector on this same episode (440
    shots, median 1.65 s); this one finds 377 shots in the body, median 2.59 s. The truth is likely between the two.
    The scene-by-scene *comparisons* below are more reliable than either absolute number.
- Lighting numbers: mean brightness (HSV value), saturation and warmth (mean red minus mean blue), sampled at 2 frames
  per second, averaged per scene.
- Identity facts I could not see on screen (production number, air date, staff) come from the coordinator's sourced
  research note and are marked so.

---

## 1. Identity

- **Title card:** the card reads **"EVOLVING RESEARCH!"** (frame checked at 2:42; card on screen 2:38.1-2:47.1,
  9.0 s, #54).
  - Layout: white panel, pink chevron frame, island-pattern border (flowers, leaves, suns).
  - In the lower right is a black wrist device with a yellow crystal: the series' Z-Ring. It previews the Z-move
    subplot (17:04).
  - Series logo just before it: "Pokémon the Series: Sun & Moon Ultra Legends" (2:34.6, #53).
- **From the coordinator's sourced note (not visible in this dub file):** production number SM106, Japanese air date
  27 Jan 2019. Staff: screenplay Akemi Omode, storyboard Hiromasa Amano, episode director Junya Koshiba, animation
  director Masaya Ōnishi.
- **Setting.**
  - Poni Island: the narrator says it at 0:01 (small model "Pony Island"; medium model "Poni Island" at 0:25).
  - Day 1:
    - A Pokémon-Center-style lobby: a nurse in pink at a counter, 0:57.
    - The sea-folk dock with a large grey whale-shaped boat (1:59-5:39).
    - "Vast Poni Canyon", near the altar of the sun (1:08-1:16). It is a red-rock canyon with a beach (5:49), a pitch-dark
      cave (10:27) and ruins with a rope bridge over a chasm and a stone altar (12:58-13:09).
    - Night: a feast outside a blue building (16:15).
  - Day 2: a dawn farewell at the dock (18:50-20:48).
- **Cast (with the evidence that identifies them)**

| Character | Role here | Evidence |
|---|---|---|
| Sophocles | A-plot lead: wants Charjabug to evolve | named 7:29 ("Sophocles still has a lot to learn"); plan stated 1:44-1:47 |
| Charjabug → Vikavolt | Sophocles' partner; evolves 13:39-13:49 | Rotom entry for Vikavolt 15:25; narrator 20:35 |
| Togedemaru | Sophocles' other partner, left behind | "Hey, Togedemaru! That was Charjabug's battle!" 7:22 (medium) |
| Lana | B-plot lead: wants to learn from Ida before she leaves | "Hi, Lana!" 2:06; "Thank you for training with me" 5:50 |
| Popplio → Brionne | Lana's partner; evolves 19:29-19:45 | narrator 20:38; Brionne reveal #392 19:45.1 |
| Ida (spelling uncertain: "Aida/Ida/Heida") | sea-folk performer and mentor; Primarina's trainer; leaves next morning | "Ida!" 2:02 (medium); "leaving tomorrow morning" 4:55 |
| Kanoa (spelling uncertain: "Kanoa/Canelo") | Ida's companion; a "treasure hunter" with goggles | "I'm a dedicated treasure hunter" 4:28 over #91 |
| Horacio ("Horatio" in both transcripts; "Horacio" in the coordinator's sourced plot) | rival, "the Red Comet", red race-styled Charjabug, two henchmen | self-intro 8:20; "the Charjabug race" 8:25 |
| Hapu | Poni local; purple bonnet | Ash: "Hapu doesn't seem to wanna battle me" 0:41 → bonnet girl: "Did I hear my name?" 0:43.6 (#10) |
| Ash + Pikachu, Kiawe + Turtonator/Marowak, Mallow, Lillie | ensemble | plans stated 0:08-0:41; Kiawe named 6:51 |
| Rotom Dex | encyclopaedia voice | entries at 3:32 (Primarina) and 15:25 (Vikavolt) |
| Narrator | frames the day | 0:01 and 20:35 |
| Off-screen mention: Gladion (small model "Gladion", medium "Vladion") | Lillie's brother | 0:21; never shown |

The coordinator guessed that the purple-bonnet girl is "Hapu in the classroom". The frames confirm she is Hapu
(0:41 → 0:43.6). The room is **not a classroom**: it is a lobby with a pink-clad nurse behind a counter (0:57) and
Pokémon eating radishes Hapu brought (0:58).

---

## 2. Beat sheet

**Overall shape (file times):**

| Part | Time | Length | Note |
|---|---|---|---|
| Cold open | 0:00-2:08 | 128 s | 10% of the file |
| Opening song (shortened dub OP) | 2:08-2:38 | 30 s | |
| Title card | 2:38-2:47 | 9 s | |
| Act 1 | 2:47-7:57 | 5 min 10 s | |
| Eyecatch / act break | 7:57-8:10 | 13 s | Silhouette quiz card 7:57; one black second at 8:03 where the ad break sat; answer card "PRIMARINA" 8:04 |
| Act 2 | 8:10-16:15 | 8 min 5 s | Contains the A-plot climax at 13:20-14:03 |
| Act 3 | 16:15-20:48 | 4 min 33 s | Contains the B-plot climax at 19:10-19:51 and the resolution |
| Ending credits | 20:48-21:18 | 30 s | Then black. **There is no next-episode preview in this file.** |

Two plots run in parallel. **A = Sophocles in the canyon** (warm colours) and **B = Lana at the sea** (cool colours).
Both are about evolution, and both reach their answer by something other than the obvious shortcut.

| # | Time | Place | Who | Want | Obstacle | Turn | Emotional / comic beat |
|---|---|---|---|---|---|---|---|
| **COLD OPEN** C1 | 0:00-0:06.7 | Aerial of the island | Narrator | Set up the day: everyone has a "research project" (0:01) | none | none | Calm establishing shot; seabirds (#1) |
| C2 | 0:06.7-0:45 | Lobby | Whole group | Each states today's plan in one or two lines: Mallow cooking (0:08), Kiawe training (0:12), Lillie observing (0:21), Ash wants a strong battle (0:36-0:41) | Hapu won't battle Ash (0:41) | Hapu answers her name (0:43.6) | Each plan gets a "comic background": Mallow sparkles (#4 0:09), Kiawe stars (#5 0:15.8), Lillie a pink burst (#6 0:21) |
| C2b | 0:45-1:07 | Lobby | Hapu, group | Hapu brings Poni radishes for the Pokémon (0:48-0:57) | none | Giant radish bundle on a cart (0:54-0:57) | Group shock poses (0:45-0:49); Pokémon carry radishes (0:58-1:00) |
| C2c | 1:07-1:48 | Lobby | Sophocles, Kiawe, Hapu | **A-plot question:** the canyon reportedly makes Charjabug evolve more easily (1:20), but Kiawe, with a sceptical eye-roll, wonders "if anyone really knows for sure" (1:31.3-1:34.6, his mouth moves in #20) | Nobody knows how it works (1:25-1:28) | An extreme close-up of Hapu's eye (1:34.85), then the local's verdict: "It is known that..." the canyon has a mysterious power (1:37) | Sophocles fist-pumps, "Let's get you to evolve" (1:43-1:47) |
| C3 | 1:48-2:08 | Window → outside → dock | Lana, Ida | Lana says she'd like to go too (1:51), then sees something: "They're here!" (1:55) | none | She runs out (1:57); boat arrives (1:59); a woman is shown only from behind and below (2:02-2:05) | **Hook into the OP:** the face is shown only at "Hi, Lana!" (2:06), then the cut to the song at 2:08 |
| **OP / TITLE** | 2:08-2:47 | | | | | | Title "EVOLVING RESEARCH!" |
| A1 | 2:47-3:35 | Dock | Lana, Ida, Kanoa; group arrives | Reunion | none | **Surprise:** Ida's Brionne has evolved into Primarina; "I kept it a secret because I wanted to surprise you" (3:10-3:22) | Rotom's Primarina entry (3:32-3:42): it makes balloons by singing inherited melodies |
| A2 | 3:35-3:58 | Dock | Primarina | Show off | none | Sky full of balloons (3:45-3:54) | Wonder; Lana: "please show me how!" (4:02) = **B-plot want** |
| A3 | 3:58-5:39 | Dock | Group, Ida, Kanoa, Hapu | Catch up | Kanoa and Ida are always away; **they leave tomorrow morning** (4:55) = B-plot clock | Ida: train until we leave? (5:07); it's "up to you" how much you learn (5:13) | Hapu plays aloof: "I ran into them, that's all!" (4:15). Kanoa's "gigantic treasure... in my mind" (4:36-4:40) → group pratfall (4:42-4:43). Lana's face falls (4:59-5:01) |
| A4 | 5:39-5:57 | Canyon walk → beach | All | Go to the canyon | none | Hapu joins: she's curious about the evolution too (5:43-5:47) | Travel shots; the group is small inside huge rock walls (#108) |
| A5 | 5:57-6:28 | Beach | Lana, Ida, Primarina, Popplio | Training, part one (5:55) | It looks like play: "They're supposed to be training, right?" (6:17) | none (the lesson comes later, 11:52) | Bubble-play montage (6:00-6:14); Mallow and Lillie puzzled (6:19-6:25); Lana puzzled (6:26) |
| A6 | 6:28-7:28 | Canyon | Ash, Kiawe, Sophocles, wild Pokémon | Ash and Kiawe battle wild Pokémon | Sophocles: "We came here so Charjabug could evolve, you know?" (6:55-7:01) | Charjabug's Discharge on a Golduck (7:06-7:11) is **stolen by Togedemaru** (7:13.7, inside the bolt) | "That was Charjabug's battle!" (7:22). Hapu's wise "still has a lot to learn" (7:29) is undercut by a rock bouncing off her forehead (7:32.2-7:32.9) |
| A7 | 7:28-7:57 | Canyon ruins | Sophocles, group | Find the spot | **"Something's wrong with the map!"** (7:39); the spot is a cave: "In a cave?" (7:45) | Silhouettes on a cliff (7:50): "Well, lookie what we have here." (7:50) | **Act-break cliffhanger:** Horacio's face (7:52.8), then the eyecatch (7:57) |
| **EYECATCH** | 7:57-8:10 | | | | | | Silhouette quiz → black (ad) → answer "PRIMARINA" |
| B1 | 8:10-10:27 | Canyon ruins | Horacio and 2 henchmen vs Sophocles | Horacio: evolve his Charjabug first (8:40). Sophocles: not lose (9:39) | Nobody remembers Horacio (8:13-8:21). Then his secret weapon, the "Bug Stone" (9:12) | **Race rules:** first Charjabug to evolve wins; **"getting help from your friends isn't allowed"** (9:49-9:51) | Gags: blank stares → pratfall (8:14-8:21); red-burst rage (8:21.5); Ash dot-eyes (8:24.5); flashback to the old race (8:28.5); henchman's doubt (8:53-8:59); Rotom "???" (9:07); slip "Pretend I didn't say that" (9:18-9:24). Sophocles leaves Togedemaru with friends; hug (9:59.7) |
| B2 | 10:27-11:31 | Inside the cave | Sophocles, Charjabug (Horacio passes) | Get through the cave | "Caves are pitch black inside" (10:32); "It's so dark, I'm scared!" (10:35); Horacio passes: "See you later!" (10:42); "Togedemaru always lights the way for us" (10:44) | **Charjabug lights up** (10:49.7-10:52): "You're filling in for Togedemaru" (10:49) | Bond beat ("Thanks so much", 10:56). Device: "There's a powerful magnetic field in here!" (11:05). Then "something scary might appear" (11:18) → black → eyes → Golbat swarm (11:23.5-11:28) → scream |
| B3 | 11:31-12:42 | Beach | Lana, Ida (Mallow, Lillie watch) | Learn | It still looks like play: "I'm afraid they're just playing", "here I thought it was something more" (~11:40-11:50) | **Ida's lesson:** the ocean is vast, fearsome and awesome; "the ocean will teach you the rest" (11:52-12:09). Lana: "It will?" (12:11). Ida: listen to the waves' beat; "don't forget that rhythm" (12:13-12:25) | Lana listens, eyes closed, light from the water on her face (12:10.4, 12 s hold). A camera dive from the waves to the dark sea floor (12:27-12:42) carries us back to the cave |
| B4 | 12:42-12:58 | Cave | Sophocles, Charjabug vs Golbats | Escape | Swarm | "String Shot! Go!" (12:45): Charjabug's eyes flash → web (12:49) → "Discharge! Back to back!" (12:50) → electric burst (12:52-12:55) | Sophocles fist up (12:50.6) |
| B5 | 12:58-13:31 | Ruins: tunnel exits, rope bridge, altar | Horacio, Sophocles | Reach the stone | Horacio arrives first (12:58.8); the green stone sits on an altar across the bridge (13:07.5) | Sophocles warns "That's dangerous!" (13:15); Horacio: a trick (13:18); **the bridge snaps** (13:20.6) | Horacio dangles over the chasm (13:26.6); Sophocles is dizzy with fear at the edge (13:29) |
| B6 **CLIMAX A** | 13:31-14:03 | Bridge edge | Sophocles, Charjabug, Horacio | Save Horacio ("Oh, what shall I do?", Horacio, 13:22) | The chasm | Sophocles: "Huh? Can it be?" (13:28); Charjabug surges with electricity (13:31.4-13:34.2); the device reads the field (13:35.5); **evolution** (13:37.6-13:49.8); "You evolved!" (13:50) | Vikavolt flies down and lifts Horacio to safety (13:53-14:01); Sophocles beams (14:03.6). A small comic slip: "That's amazing, Charjabug! I mean, Vikavolt!" (14:02-14:07) |
| B7 | 14:03-14:47 | Altar | Sophocles, Vikavolt, Horacio | (Horacio) still wants the stone | Sophocles has already won | **Sophocles has Vikavolt fetch the stone and gives it to Horacio** (14:14-14:31) | **Twist:** the stone does nothing, "It isn't evolving!" (14:37). Sophocles' guess: the magnetic field did it (14:41-14:50). Horacio's comic soul-sigh puff (14:53-14:54) |
| B8 | 14:47-16:15 | Cave mouth, canyon | Friends, Sophocles, Horacio | Friends worry and go in (14:54-15:01) | Golbats burst out over them (15:04.6-15:08) | Vikavolt emerges from the same dark (15:08.5-15:15) | Rotom's Vikavolt entry (15:25). Horacio's vow: a Vikavolt race next time (15:40-15:46). "Let's go!" → wrong way → face-plant by the stairs (15:46-15:58). Friends' deadpan (15:59). Sophocles likes the race idea (16:00-16:12); Hapu: "Sophocles is good, too" (16:12.5) |
| D1 | 16:15-16:59 | Village, night | All plus sea folk | Celebrate | none | Feast (16:30-16:56) | Mallow sparkle background (#315 16:40) |
| D2 | 16:59-18:08 | Feast, night sky | Ida, Primarina | Thank-you gift (16:59) | none | **Z-move** "Oceanic Operetta" (17:04-17:52): a giant balloon bursts into sparkle rain | Awe reactions (17:24-17:35; 17:56-18:08). Kanoa pats Hapu's head (17:33.5) |
| D3 | 18:08-18:49 | Night | Lana, Ida | Lana wants that move | **Popplio must evolve into Brionne, then Primarina, first** (18:16-18:21) | "You keep training hard, and you'll use it too" (18:21) → Lana decides alone: she wants to show Ida "right at this moment"; "It's time to train" (18:36-18:46) | Sparkles still falling on Lana's face (18:08-18:15); she walks off at night with Eevee (18:44.9); fade to black (18:48.9) |
| D4 | 18:50-19:10 | Dock, dawn | Friends, Ida, Kanoa | Say goodbye | Lana is missing: "Maybe it's hard to say goodbye." / "I'll look for her." (18:55-18:58) | They find her training at the dock: "this is the best we can possibly do right now" (19:01-19:09) | Soft dawn light, low saturation |
| D5 **CLIMAX B** | 19:10-19:55 | Dock | Lana, Popplio | A bigger balloon (the want from 4:02): "Now make it bigger!" (19:15) | none stated, except the boat waiting | Popplio's balloon swells huge (19:12-19:27) → **evolution** (19:29.6-19:45.1) | Friends cheer (19:20-19:22); Mallow and Ash stunned (19:28); "It evolved!... What a surprise!" (19:47-19:50); Lana's four-step face shot (19:46.7-19:50.7) |
| D6 **RESOLUTION** | 19:55-20:48 | Dock → sea | Lana, Ida, Kanoa | Farewell. Lana: "This is the very best we can do!" (19:59); Ida: "Thanks for showing me!" (20:03) | Lana's stated next goal: train more and "someday" use Oceanic Operetta (20:07-20:11) | **Ida gives Lana a "Primarium Z"** (20:13). Lana: "That's your Z crystal!" (20:17). Kanoa, thumb to his chest, says he found it on a treasure dive (20:21-20:26). Ida: "Can't wait for that Z-move" (20:26-20:29) | Lana holds it on a sparkle background (20:31.7); the boat leaves (20:35); the narrator wraps both plots (20:35-20:46); aerial bookend with "To Be Continued" (20:44) |

---

## 3. Storytelling analysis

### 3.1 The hook and the central questions
- **The first 60 s are a warm round-robin, not a shock.**
  - The narrator frames a premise in one line: everyone has a research project today (0:01).
  - Each character then gets one or two lines plus a signature background (0:08-0:35).
  - Tension comes from one unmet want: Ash wants a strong opponent and Hapu won't battle (0:36-0:41). The
    "speak of the devil" entrance follows at 0:43.6.
  - The first 60 s carry little suspense. For TV this is fine; a Short could not afford it (see lesson 1).
- **Question A is posed as a doubt between two characters.**
  - Sophocles reads that the canyon makes Charjabug evolve more easily (1:20). Nobody knows how (1:25-1:28), and
    Kiawe wonders "if anyone really knows for sure" (1:31.3-1:34.6).
  - An extreme close-up of Hapu's eye (1:34.85) gives her the floor. She answers with the authority of a local, "It
    is known that..." (1:37), but she gives no mechanism.
  - The *how* stays open until the map glitch (7:39), the device reading (11:05, "powerful magnetic field"), the
    evolution (13:37) and Sophocles' explanation (14:43-14:50).
- **Question B is posed as a want plus a clock.**
  - The want: Lana's "please show me how!" (4:02).
  - The clock: "we're leaving tomorrow morning" (4:55).
  - The answer: Popplio evolves at dawn just before the boat leaves (19:29-19:45), and Ida hands over the crystal
    (20:13).
- **The cold open ends mid-reveal.** Lana's "They're here!" (1:55) names nobody. The newcomer is first seen from behind
  and below, face hidden (2:02-2:05), and is revealed in close-up one second before the song (2:06-2:08).

### 3.2 Set-ups and payoffs

| Set-up | Time | Payoff | Time |
|---|---|---|---|
| The canyon's "mysterious power" | 1:37 | The power is a magnetic field: device reading, evolution, explanation | 11:05; 13:35.5; 14:41-14:50 |
| "Something's wrong with the map!" | 7:39 | The magnetic field is what affects Charjabug (and the map) | 11:05-11:11 |
| The "world-famous" Bug Stone, "top-secret information" | 9:12-9:22 | It does nothing: "It isn't evolving!" | 14:34-14:43 |
| Dad "paid a fortune" for the stone tip | 9:32-9:35 | The paid shortcut fails; the free natural cause works | 14:37-14:50 |
| Rule: "getting help from your friends isn't allowed" | 9:49-9:51 | Sophocles leaves Togedemaru → he has no light in the cave | 10:00; 10:44 |
| "Caves are pitch black inside" + "In a cave?" | 10:32; 7:45 | "It's so dark, I'm scared!" → Charjabug becomes the light | 10:35; 10:49.7 |
| Togedemaru steals Charjabug's Discharge ("That was Charjabug's battle!") | 7:13.7-7:22 | Alone, Charjabug's electricity lights the cave and beats the Golbats. *(My reading: the episode never says this link aloud.)* | 10:49.7; 12:52-12:55 |
| "I let you win that race back then"; henchman doubts it | 8:47-8:59 | Horacio loses again, and is rescued by the boy he "let win" | 13:58-14:01 |
| "That's dangerous!" → "I'm not falling for that lie." | 13:15-13:18 | The bridge snaps | 13:20.6 |
| Golbats come out of the dark at Sophocles | 11:24-11:28 | Same staging, inverted: Golbats burst over the friends, then Vikavolt emerges from the same dark | 15:04.6-15:15 |
| Hapu: "Ash is good, but you're pretty good, too" (to Kiawe); "Sophocles still has a lot to learn" | 6:51; 7:29 | Hapu, smiling in close-up: "Sophocles is good, too." | 16:12.5 (medium model; #308) |
| Kanoa ruffles Hapu's bonnet; she pulls away embarrassed: "I ran into them, that's all!" | 4:12-4:17 | He pats her head again during the Z-move, and this time she just closes her eyes (no words) | 17:33.5 |
| Ida, at the Z-move: the biggest balloon anyone has seen ("never seen a balloon that big", 17:26) | 17:22-17:29 | Lana: "Now make it bigger!" → Popplio's giant balloon | 19:15-19:27 |
| Lana, at night: she wants to show Ida "right at this moment"; "It's time to train" | 18:38-18:46 | Missing at the farewell (18:55), found training (19:01), shows Ida the evolution before the boat leaves | 19:05-19:45 |
| The old "Charjabug race" (flashback) | 8:28.5 | Horacio proposes a future "Vikavolt race"; Sophocles likes the idea | 15:46; 15:59 |
| Ida's Brionne evolved in secret "to surprise you" | 3:16-3:22 | Lana slips away to train and surprises everyone with an evolution | 18:44; 19:29 |
| Primarina makes balloons by singing inherited melodies | 3:36-3:42 | Popplio sings a giant balloon at dawn → evolves | 19:12-19:29 |
| "Please show me how!" (bigger balloons) | 4:02 | Popplio's biggest balloon | 19:16-19:27 |
| The training looks like play | 6:17-6:26; 11:40 | Ida's rhythm-of-the-waves lesson → it becomes Popplio's song | 11:52-12:09 → 19:22 |
| "Well, Lana, about that..." | 4:06 | The departure news, then the dawn goodbye | 4:55; 20:35 |
| Z-Ring icon on the title card | 2:38 | Ida's Z-Ring and Oceanic Operetta; "you'll use it too"; the crystal gift | 17:04; 18:21; 20:13 |
| Kanoa's "gigantic treasure... in my mind" | 4:36-4:40 | His treasure diving turns out to be real: he found the Z crystal that becomes Lana's gift ("found it when I was in the middle of a treasure dive") | 20:21-20:26 |
| Opening aerial of the island; narrator "research projects" | 0:00; 0:01 | Closing aerial with the boat leaving; narrator "research projects have been successful" | 20:39.7; 20:40 |

### 3.3 How the obstacles escalate (A-plot)
Each step takes away a support or adds a danger, and the last step changes what winning means.

1. **Uncertainty.** Nobody knows if the place works (1:25-1:30).
2. **Interference from his own team.** Togedemaru takes the battle (7:13-7:22).
3. **The tools fail.** The map breaks (7:39); the spot is a cave (7:45).
4. **A rival with a "shortcut," plus a rule that isolates the hero.** The stone (9:12); "no help from friends" (9:51).
5. **His light is gone.** Darkness and fear (10:35-10:44); the rival overtakes him (10:42).
6. **Lost.** The magnetic field scrambles direction: "Which way do we go?" (11:05-11:15).
7. **A swarm.** Golbats (11:24-11:28, resumed 12:42-12:58).
8. **The rival reaches the prize first.** 12:58-13:09.
9. **The rival is in mortal danger.** The bridge collapses (13:20-13:31). The race turns into "save him or grab the
   prize." Sophocles saves him, and the evolution comes *from* that choice (13:31-13:58). Then he gives the prize away
   (14:23).

The B-plot escalates gently, which suits it as the emotional counterweight:
1. A one-day clock (4:55).
2. Training that seems pointless (6:17).
3. A cryptic lesson (11:52).
4. The far goal is shown and Lana learns it costs two evolutions (17:35-18:21).
5. She trains alone at dawn (19:01).
6. The breakthrough (19:29).

### 3.4 Pokémon personality with no words
- **Charjabug.** Eyes blink from blank to a determined glare before acting (7:09.0-7:09.7). In the dark it sparks
  while Sophocles cries into it (10:49.7), then lights up the cave (10:50.6-10:52). Its eyes flash in 0.2 s inserts
  before String Shot (12:48.1-12:48.9). On the bridge edge it surges with electricity unprompted (13:31.4-13:34.2).
- **Vikavolt.** An extreme close-up eye glint (13:55.0, 0.2 s) before it dives to the rescue; it fetches and hands
  over the stone (14:17.7-14:21.2).
- **Togedemaru.** It sits inside the stolen bolt (7:13.7), then beams on a star-sparkle background (7:19.7-7:21) while
  Charjabug's trainer fumes: a greedy, happy, oblivious character in two shots.
- **Eevee.** It follows the Primarina's arcs from a rock (6:02-6:05), bounces on a bubble (6:09), laughs (6:12-6:14),
  and trails Lana alone at night (18:44).
- **Popplio and Brionne.** Popplio sings with eyes closed while the balloon grows (19:22-19:24). The new Brionne's
  first act is a wink (19:43.6), then a big arms-up pose (19:46).
- **Primarina.** Graceful, eyes-closed singing, hair rising (17:18.5-17:21.6). The balloon it makes dwarfs everyone
  (17:22).
- **Turtonator.** An extreme close-up glare (6:44.4-6:44.6) before the attack.
- **Golbat.** Just eyes opening in a black frame (11:24-11:24.5) = menace.
- **Horacio's red Charjabug.** It is styled as a race car with a grin and star sparkles (8:30.3): it shows the owner's
  vanity.
- **Rotom Dex.** Its face-screen turns into "???" (9:07-9:10): an interface used as a facial expression.

### 3.5 How bonds and relationships change
- **Sophocles and Charjabug** go from commander and tool to partners.
  - Start: "Use Discharge!" (7:09).
  - Middle: "You're filling in for Togedemaru... Thanks so much" (10:49-10:56).
  - End: Charjabug evolves to save the person Sophocles chose to save (13:37).
- **Sophocles and Togedemaru.** The separation is staged as a hug (9:59.7). The absence is felt as darkness (10:44).
- **Sophocles and Horacio** move from rivalry to friendly rivalry.
  - Rivalry: split-screen glares (8:41.7, 9:40.3, 13:16.6).
  - Then a warning (13:15), a rescue (13:58), and a gift (14:23).
  - Horacio's exit vow is "train hard" and race again (15:42-15:46). Sophocles answers that a Vikavolt race "sounds
    like a lot of fun" (15:59).
- **Lana and Ida** are student and mentor.
  - Lana's joy (2:02), then her face falls at the news (4:59-5:01).
  - The lesson (11:52-12:09), then the gift of a performance (16:59).
  - Lana's private decision to show Ida before she leaves (18:38). The student acts on her own and is not told to.
  - Then a crystal (20:13), and Lana's last close-up holds it to her chest on a sparkle background (20:31.7).
- **Hapu and the sea folk.** Someone tells Hapu he's glad she has friends now that she's "always been by yourself"
  (4:10). The speaker is inferred to be Kanoa, who crosses to her in the wide shot as the line plays (4:08-4:11).
  He ruffles her bonnet and she pulls away,
  fists clenched: "I ran into them, that's all!" (4:12-4:17). During the Z-move he pats her head again and she lets
  him, eyes closed (17:33.5). The relationship changes through **one repeated gesture**, with no dialogue the second
  time.
- **Hapu and Sophocles.** Hapu's verdict changes from "still has a lot to learn" (7:29) to "Sophocles is good, too"
  (16:12.5). The line echoes her earlier praise of Kiawe (6:51).
- **Ash and Hapu.** Ash's wish to battle Hapu (0:36-0:41) is **not resolved in this episode**; it is left open.

### 3.6 Where suspense and surprise sit
- **The act-break cliffhanger.** Figures appear as silhouettes against the sky on a cliff (7:50.0, #149). The leader's
  face is shown at 7:52.8, and the episode cuts to the eyecatch at 7:57. The viewer knows *who* only after the break
  (8:13-8:28).
- **The dark cave builds suspense in steps.**
  1. A long, dark wide shot where Sophocles is a speck (10:34.7-10:37.7).
  2. "Something scary might appear" over a slow push into an **empty** dark hollow (11:19-11:23).
  3. A full black frame (11:23.5).
  4. Two eyes (11:24), then many (11:24.5), then the swarm (11:25-11:28).
  5. Then the story **cuts away to the other plot for 71 s** (11:31.6-12:42.5) before resolving the danger.
- **Dramatic irony.** Sophocles' warning is dismissed 2 s before the bridge snaps (13:15-13:20).
- **Surprises.**
  - Ida's Primarina (3:10).
  - Togedemaru stealing the attack (7:13.7).
  - Horacio passing in the dark (10:42).
  - The stone failing (14:37).
  - Lana missing at the dawn farewell (18:55), then found training (19:01).
- **Each climax is "earned" by something set up earlier,** never by a new element: the field (11:05), the singing
  balloon (3:36).

### 3.7 Comedy patterns
| Pattern | Example | Timing |
|---|---|---|
| Speak-of-the-devil cut | "Hapu doesn't seem to wanna battle me" → hard cut to Hapu: "Did I hear my name?" | 0:41 → 0:43.8; then a 4.5 s group-shock shot (#11) |
| Proud pose held in a wide shot, deflating last word, group pratfall | Kanoa's fists-up "gigantic treasure" → "in my mind" → everyone topples | 4:36 → 4:40 → 4:42-4:43 |
| Blank stare → pratfall → rage background → dot-eyes | "Who's that guy?" / "Who are you again?" → henchmen and Horacio fall over → red jagged-burst background → Ash's blank dot-eyes | 8:14-8:16.8 (a 2.8 s blank hold, still 0.95) → 8:20-8:21 → 8:21.5-8:24 → 8:24.5-8:28 |
| Underling undercuts the boss | Henchman: "Are you sure about that?" → "You said something!" → "No sir, not a thing!" with a sweat drop | 8:53-8:59 |
| Boast → slip → take-back | Brags about the "top-secret" stone, then "Pretend I didn't say that" with hands up | 9:12-9:24 (pose at 9:23.7) |
| A teammate steals the moment | Togedemaru absorbs Charjabug's bolt | 7:13.7 → 7:19.7 grin → 7:22 complaint |
| Dignity undercut | Hapu's sage line, then a rock bonks her | 7:29 → 7:32.2 |
| Bravado → literal fall | "Let's go!" → runs the wrong way → face-plant next to the stairs → "Now you tell me." | 15:46 → 15:57 → 15:59 deadpan reaction |
| Soul-sigh puff | Horacio slumps; a white ghost-like puff floats out | 14:52-14:54 |

**Timing finding.** In this episode comedy is **not cut faster than dialogue**.
- Forgotten-name gag: median 2.9 s.
- Wrong-way gag: 4.4 s.
- Togedemaru gag: 1.9 s.
- Every gag places a held reaction shot right after the joke (2-4 s), and the joke line itself is short. The laugh
  lives in the pause (8:14-8:16.8).

### 3.8 How the challenge is made clever
- It is a **race with an environmental puzzle,** not a strength contest.
  - The rival's paid item is a red herring (9:12 → 14:37).
  - The real cause is a natural property of the place, a strong magnetic field (11:05).
  - It is detected by the hero's device. The same insert shot recurs: 1:13.9, 7:37.2, 11:07.1, 13:35.5.
- **The creature's natural traits solve the problems.**
  - Charjabug is a battery: it lights the cave (10:50).
  - Its thread (String Shot) and electricity scatter the Golbats (12:49-12:55).
- **The turning point is a moral choice,** not a tactic. Saving the rival triggers the evolution (13:31-13:58). Giving
  the stone away (14:23) proves the win wasn't about the prize.
- The short wild battle (6:28-7:22) shows the team's power (Pikachu dash 6:35.7, Turtonator 6:44-6:48). It then
  becomes a gag that sets up Sophocles' need to prove Charjabug on its own.

### 3.9 Dialogue style
- **Lines are short:** one idea, mostly 1-3 s (e.g. the medium-model timings at 8:33-8:59 run 1-2 s per line). Wants are
  stated out loud and early (0:38, 1:45, 4:02, 8:40).
- **Exposition is always given to a character who has a reason to say it:**
  - a braggart who can't keep a secret (Horacio, the stone, 9:12-9:35);
  - the local who "knows" (Hapu, 1:37);
  - an encyclopaedia (Rotom, 3:32, 15:25);
  - a mentor speaking in images (Ida, 11:52-12:09);
  - the narrator at the two ends (0:01, 20:35).
- **Each character has a recognisable voice:**
  - Horacio swaggers in folksy phrases ("Well, lookie what we have here", 7:50), gives himself a title ("the Red
    Comet", 8:20) and uses a show-off image ("like a bug type flying into a flame", 9:43; the speaker is probably
    Horacio, answering Sophocles' "I'm not gonna lose" at 9:39).
  - Hapu is formal and terse ("It is known that...", 1:37; "still has a lot to learn", 7:29).
  - Ida is warm and lyrical (11:52).
  - Kanoa jokes (4:36).
  - Ash is impulsive and battle-minded (0:38).
  - Sophocles is technical and anxious, then brave (11:05; 10:35; 13:15).
  - Lana is eager (5:18 "I'll do my best!").
- Characters often say a Pokémon's name as a one-word line, and the Pokémon "answer" with their own cries (e.g.
  0:19-0:20). That keeps the creatures in the conversation.

### 3.10 The ending and its pull
- Both climaxes land within 6 minutes of each other (13:37, 19:29).
- The narrator then names both results in plain words (20:35-20:45), and a **"To Be Continued"** caption sits over the
  bookend aerial (20:44-20:47).
- Forward hooks are spoken, not shown:
  - the future Vikavolt race (15:46; "sounds like a lot of fun", 16:00);
  - Lana's far goal: one more evolution and the Z-move. "Then someday we'll use Oceanic Operetta!" (20:07-20:11);
    Ida's "Can't wait for that Z-move" (20:26-20:29). The crystal in her hand (20:31.7) is the physical promise.
- This file has **no next-episode preview** after the credits (20:48-21:18, then black).
- The pull is soft and character-based: no cliffhanger.

---

## 4. Animation and staging

### 4.1 Shot length by scene type (from shots.json; see the detector caveats at the top)

| Scene type (segments) | Shots | Median | Mean | Shots under 1 s | Held frames | Motion |
|---|---|---|---|---|---|---|
| Dialogue (C2, A1, A3, B1, B7, D4) | 109 | 3.75 s | 4.14 s | 5% | 0.66 | 2.3 |
| Mood / emotion (B2 cave, B3 lesson, D3 night, D6 farewell) | 41 | 4.25 s | 5.66 s | 2% | 0.58 | 2.2 |
| Montage (A5 bubble play, D1 feast) | 16 | 3.88 s | 4.73 s | 0% | 0.48 | 3.4 |
| Action (A6 wild fight, B4 Golbats, B5 bridge) | 56 | 1.69 s | 1.94 s | 32% | 0.38 | 9.2 |
| Spectacle (A2 balloons, B6 evolution + rescue, D2 Z-move, D5 evolution) | 112 | 0.92 s | 1.50 s | 55% | 0.21 | 11.4 |
| Opening song | 25 | 1.08 s | 1.20 s | 44% | 0.19 | 12.9 |
| Whole body (no OP, cards or ED) | 377 | 2.59 s | 3.17 s | 24% | 0.45 | 6.3 |

Sub-sequences:

| Moment | Time | Shots | Median | Under 1 s |
|---|---|---|---|---|
| Turtonator attack | 6:42.1-6:48.5 | 7 | 0.33 s | 71% |
| Charjabug evolution glow | 13:37.6-13:51.4 | 18 | 0.67 s | 78% |
| Popplio evolution glow | 19:29.6-19:46.8 | 19 | 0.79 s | 68% |
| Z-move power-up | 17:03.9-17:24.6 | 21 | 0.71 s | 67% |
| Bridge collapse | 13:15-13:31 | 10 | 1.33 s | 40% |
| Togedemaru gag | 7:09-7:28.7 | 9 | 1.88 s | 11% |
| Forgotten-name gag | 8:10-8:33.7 | 8 | 2.88 s | 0% |
| Wrong-way gag | 15:42.6-16:03 | 4 | 4.44 s | 0% |
| Golbat reveal + scream | 11:23-11:31.6 | 3 | 1.63 s | 0% |

**Rhythm rules the numbers show:**
1. **Dialogue holds** about 3-4 s (probably ~3 s once the missed cuts are counted).
2. **Action** about 1.7 s.
3. **Transformations and finishers** go **under 1 s per cut,** for 10-17 s at a stretch.
4. **Comedy and emotion** hold *longer* than dialogue.

The longest real holds are all emotional or listening shots:
- the 12-s group master shot (1:19.2);
- the 12.5-s two-shot during Ida's ocean speech (11:50.9, still 0.98);
- Lana listening with eyes closed (12:10.4, 12 s).

**Shot sizes in use:**
- **Extreme wide and aerial:** the bookends 0:00 and 20:39.7; the dock from high above at the bad news (4:51-4:59,
  7.9 s, everyone tiny); Sophocles as a speck in the cave (10:34.7, 11:15.5).
- **Group master in which characters act one after another:** 1:19.2-1:31 (12 s, one frame).
- **Over-the-shoulder:** the henchman → Ash and Kiawe (8:53.7); Lana → Ida (18:15.5).
- **Medium close-up and close-up** for most lines.
- **Extreme close-up of eyes** for a decision or a threat: Turtonator 6:44.4; Charjabug 12:48.1; Vikavolt 13:55.0.
- **Inserts** of the device (1:13.9, 7:37.2, 11:07.1, 13:35.5) and the crystal (20:15).
- **Depth staging:** foreground shock, background reason. Horacio's terrified face in front, Sophocles small behind
  (13:22.2); Sophocles appearing small in the tunnel mouth behind Horacio (13:09.5).

### 4.2 Camera moves (each one has a job)
- **Tilt up from legs to face, low angle,** to present a rival (8:10-8:13).
- **Extreme close-up tilt from belly to glaring face (~5 frames), then a quick pull-back to show the stance** before
  an attack (6:44.40-6:44.61 → 6:44.65-6:44.99).
- **A long descent from the waves to a dark sea floor (~15 s),** used as a mood bridge between plots (12:27-12:42).
  The cut to the dark cave follows at 12:42.5. Brightness drops from 0.72 (beach) to 0.61 during the dive, then 0.40
  in the cave fight.
- **A slow push into empty darkness** before a scare (11:19-11:23).
- **A slow pan across the audience during a spectacle** (17:24.6-17:35.6, 11 s).
- **A tilt down from a sparkle-filled sky to the crowd** (17:48.5-17:52).
- **The balloon rising with a locked camera:** the object moves, not the frame (17:40-17:45).
- **Mostly static frames otherwise.** The earlier study measured 78% static shots; this pass agrees (e.g. the bookend
  aerial 20:39.7 has still 1.00).

### 4.3 Holds and timing on 2s / 3s (adds to ANIME_STUDY.md; not re-measured)
- **Wind-up:** the body is held and the effect moves. Turtonator's pose barely changes from 6:44.99 to 6:47.03,
  while the flame column grows and wind-swirl lines whip past (6:45.7-6:45.9).
- **Impact graphics alternate on 2s:** pairs of frames, A-B-B-C-C-D-D (6:47.37-6:47.62).
- **The evolution silhouette holds for several frames while the glow flickers on 1s** (13:39.45-13:39.78).
- **Dialogue: the mouth moves on a held drawing for long stretches.** Horacio and his henchmen: one framing for 8 s
  (9:10.3-9:18.3, 78% held frames). Pose changes mark the line beats: hand on head (8:47.7) → pointing (8:51.7);
  boasting with a finger up (9:15.5); hands up (9:23.7).
- **Action shots carry the most drawn motion:** mean motion 9-11 against 2.3 in dialogue.

### 4.4 How a move is staged, step by step

**(a) Turtonator's tail attack, 6:42.1-6:48.5, ~6.4 s.** The transcript gives the command as "drag it down", probably
"Dragon Tail", but that is not verified.

| Step | Time | Length | What happens |
|---|---|---|---|
| 1. Command | 6:42.1-6:44.36 | 2.2 s | Trainer's arm thrust, low angle |
| 2. Glare | 6:44.40-6:44.61 | 5 frames | Extreme close-up tilt up to the eyes |
| 3. Wind-up | 6:44.65-6:47.03 | 2.4 s | Pull-back to a medium wide; crouch; the flame tail grows; swirl lines |
| 4. Strike | 6:47.07-6:47.20 | 4 frames | The spin, with flame smears |
| 5. Flash | 6:47.24-6:47.32 | 3 frames | Full-frame orange-white wash |
| 6. Impact frames | 6:47.37-6:47.62 | 6 frames | Abstract yellow/black slash shapes |
| 7. Hit | 6:47.66-6:47.70 | 2 frames | The target fills the frame |
| 8. Knock-away | 6:47.74-6:48.49 | 0.8 s | The target sails into the sky, shrinking |
| 9. Reaction | 6:48.53- | 6.1 s hold | Group reaction |

**(b) Charjabug's Discharge, with a twist, 7:09-7:22:**
1. Eyes open (7:09.7).
2. Charge with radial light and speed lines (7:10.3-7:11.7).
3. The trainer's proud fist (7:12.3).
4. The bolt over a warm speed-line background (7:13.6-7:15.7). **Togedemaru is inside the bolt** (7:13.7).
5. Flash (7:16.3-7:17).
6. The target is unharmed and leaves (7:17.7-7:19).
7. Togedemaru's grin on sparkles (7:19.7).
8. Group reaction and complaint (7:21.7-7:28).

**(c) Charjabug vs the Golbats, 12:42.5-12:58.5:**
1. Swarm (12:42.5).
2. The trainer points (12:45).
3. Eye extreme close-ups, cut at 0.2 s (12:48.1-12:48.9).
4. String Shot threads net the bats (12:49-12:50.6).
5. The trainer's fist (12:50.6).
6. An electric burst with jagged lightning over the whole frame (12:52.3-12:55.1).
7. Dark aftermath (12:58.5).

**(d) Ida's Z-move, 16:59-18:08:**
1. She stands up at the table (17:03.5).
2. Close-up smile (17:04.1).
3. Arm up with the Z-Ring (17:04.75).
4. Crossed-arm pose against the moon (17:05.4).
5. A glowing sigil (17:06.0).
6. Lana's reaction (17:07.25).
7. Dance poses (17:08.5).
8. An aura flame against a darkened background (17:09.75-17:11).
9. The power goes to Primarina (17:11.6-17:12.9).
10. A calm pose in a curtain of light with bubbles (17:13.5-17:16).
11. A big smile (17:17.25).
12. Primarina sings, hair rising (17:18.5-17:21.6).
13. **A giant balloon makes both figures tiny** (17:22.25).
14. A slow audience pan (17:24.6-17:35.6).
15. The command (17:37.25).
16. The balloon rises (17:40-17:45).
17. A burst into an abstract concentric-swirl graphic (17:46-17:48).
18. Sparkle rain on the crowd (17:48.5-17:52).
19. The final pose (17:52.9).
20. Reactions (17:56.8-18:08).

The order is: power-up in short cuts, then a long, quiet scale shot, then the release.

**(e) An evolution (the same template both times):**

| Step | Charjabug | Popplio |
|---|---|---|
| 1. Trigger (emotional + environmental) | Rival falling, the field | Biggest balloon, the song |
| 2. Body goes white | 13:37.6 | 19:24.7 |
| 3. Radial light burst with speed lines | none seen | 19:29.3 |
| 4. Background replaced by a blue starfield / bubble pattern | 13:40.9 | 19:31.3 |
| 5. Silhouette morphs in 0.3-0.9 s cuts | 10.6 s in all | 15.5 s in all |
| 6. Reveal pose | 13:49.8 | 19:45.1 |
| 7. Trainer reaction | 13:51.4 | 19:46.7 |
| 8. The new creature's first act | Flies to the rescue, 13:53-14:01 | Arms-up pose, 19:46 |

Lana's reaction (19:46.7-19:50.7) is a four-step face change inside one shot: blank → wide-eyed → open-mouthed →
eyes-closed smile with fists.

### 4.5 Effects inventory
- **Emotion / comic backgrounds that replace the set:**
  - sparkle bubbles (Mallow 0:09, 16:40);
  - stars (Kiawe 0:15.8);
  - a pink radial burst (Lillie 0:21);
  - a red jagged burst for rage (Horacio 8:21.5);
  - star sparkle for glee (Togedemaru 7:19.7);
  - magenta-yellow sparkle for a vow (Lana 20:31.7).
- **Speed lines:**
  - radial blue streaks behind a charging Pokémon (#122 6:40.1);
  - a radial yellow burst while Charjabug charges (7:10.3);
  - warm streaks behind the bolt (7:13.6);
  - a radial burst at the start of the evolution (19:29.3).
- **Impact frames:** a flash plus two-colour slash graphics (6:47.24-6:47.62); a black frame with a yellow arc (13:31.0);
  eye extreme close-ups on dark (12:48.7-12:48.9).
- **Glows and auras:**
  - Charjabug as a light source, with radial rays and the cave lit around it (10:52.4);
  - Ida's cyan aura (17:09.75);
  - a light curtain plus bubbles (17:13.5);
  - evolution glows (13:39, 19:24).
- **Background replacement for transformations:** a starfield of circles (13:40.9-13:49.6); a bubble field
  (19:31.3-19:46).
- **Split screens** with a diagonal white "lightning" seam for rival eye-lines: 8:41.7, 8:45.7, 9:40.3, 13:16.6. There
  is also a diagonal three-panel "lesson starts" frame of mentor, Pokémon and student (5:58.8).
- **Comedy faces:**
  - Ash's blank dot-eyes (8:24.5);
  - tears as streams (10:44.7, 11:26.2);
  - white eyes with pin-prick pupils for terror (13:22.2);
  - dizzy swirl (13:29-13:30.6);
  - a soul-sigh puff (14:53).
- **Sweat drops:** the henchman (8:55.7), Ash and Kiawe (9:18.7).
- **Flashback treatment:** a white bloom vignette and soft focus (8:28.5-8:31).
- **Silhouettes:** rivals against the sky (7:50); Vikavolt in the cave mouth (15:08.5-15:10.5); the quiz card (7:57).
- **Atmosphere:**
  - sparkle rain carried on into the next emotional shot (18:08-18:15);
  - water caustics on Lana's face (12:10.4);
  - floating balloons and bubbles as ambient motion (3:45-3:54, 6:06-6:09).

### 4.6 Colour and lighting by scene (measured)

| Scene | Brightness | Saturation | Warmth (red − blue) |
|---|---|---|---|
| Lobby (day, interior) | 0.68 | 0.35 | +0.08 |
| Dock / beach scenes (B-plot) | 0.72-0.77 | 0.44-0.49 | **−0.08 to −0.16** |
| Primarina balloon show | 0.81 | 0.53 | −0.33 |
| Canyon scenes (A-plot) | 0.53-0.68 | 0.38-0.43 | **+0.11 to +0.21** |
| Dark cave alone | **0.25** | 0.55 | +0.10 |
| Golbat fight | 0.40 | 0.46 | +0.14 |
| Charjabug evolution glow | 0.81 | 0.53 | **−0.31** |
| Night feast / Z-move | 0.51-0.54 | 0.50-0.51 | −0.07 to −0.11 |
| Night lesson (Lana's resolve) | 0.43 | **0.58** | −0.10 |
| Dawn dock + farewell | 0.67-0.73 | **0.31** | −0.02 to −0.05 |
| Popplio evolution glow | **0.89** | 0.51 | **−0.43** |

What the numbers show:
- **The two plots are colour-coded:** warm canyon (A) against cool sea (B). The intercuts are readable at a glance.
- **Both evolutions break into the same bright cyan,** even the canyon one, so "evolution" has its own colour.
- **Fear is carried by darkness, not by colour.** The cave is the darkest stretch (0.25) and keeps its warm hue.
- **The goodbye at dawn is the least saturated scene** (0.31), a muted, wistful light. The resolve scene at night is the
  most saturated (0.58, deep blue).

### 4.7 Expressions and acting
- **Eyes:**
  - big round eyes under thick brows for alarm (Hapu 0:43.8);
  - half-lidded, narrowed eyes for scepticism or impatience (Ash 0:40.5);
  - smug narrow lids (Horacio 8:31.7);
  - white eyes with tiny pupils for terror (13:22.2);
  - closed arcs for joy (Ida 4:47; Sophocles 14:05) **and** for calm wisdom (Hapu 7:28.7; Lana listening 12:10.4);
  - tear streams for comic despair (10:44.7; 11:26.2).
- **Mouths:** huge open shapes for shouting (Sophocles 13:23.8; Horacio 8:21.5); a short flat line for doubt (Ash
  0:40.5); a grin with teeth for smugness (Horacio 13:17.8).
- **Hands:**
  - fist pumps for resolve (Sophocles 1:44, 12:50.6; Lana 19:14);
  - a raised index finger for teaching or boasting (Ida 5:14, 5:57; Horacio 9:15.5);
  - both hands up for "take it back" (9:23.7);
  - a hand behind the head for vanity (8:47.7);
  - crossed arms for impatience (Ash 0:35.6);
  - a hand on the chest holding the gift (20:32);
  - an arm thrust for a command (Kiawe 6:42.1).
- **Acting progressions inside one held shot:**
  - Lana's four-step reaction (19:46.7-19:50.7);
  - the group master shot where Sophocles turns, speaks and everyone reacts in turn (1:19.2-1:31);
  - Sophocles in the cave, from clutching his head to crying into Charjabug (10:38.7-10:49.7).

### 4.8 Transitions
- **Cut to the opening song on a face reveal** (2:06 → 2:08).
- **Eyecatch:** a question card, the ad gap, then the answer card (7:57-8:10).
- **A smash cut between plots on a scream:** dark cave scream (11:29.2) → bright splash of Popplio in a wave (11:31.6).
  It is a contrast cut: dark to bright, fear to play.
- **A camera dive as a mood bridge** from the bright sea to the dark cave (12:27-12:42.5).
- **A hard cut from canyon day to village night** (16:11.4 → 16:15.1).
- **A fade to black for the time skip from night to dawn** (18:48.9 → 18:50.9). A scan of brightness at 2 fps finds
  no other fade in the body. The only other black frames are the ad gap (8:03) and the deliberate black beat in the
  scare (11:23.5); the cave shots at 10:34-11:15 are near-black but are shots, not fades.
- **Flashback in and out on a white bloom** (8:28.5-8:31).
- **Bookend aerials** (0:00 and 20:39.7), with the "To Be Continued" caption at 20:44.

---

## 5. Lessons for our original 60-90 s vertical Shorts series

Our series: a reincarnated Earth student survives a cute-but-deadly creature world through real animal knowledge. Each
episode ends on an A/B choice that viewers vote on in the comments. Each lesson cites where it comes from.

1. **Compress the cold open into 3 seconds.**
   - What the episode does: it takes 60 s to get to a want (0:36-0:41) and 108 s to its first mystery hook (1:55).
   - For us: open on the student already in a scene with a want and a doubt in one line ("They say X. Nobody knows
     if it's true."), as Kiawe's doubt and Hapu's "It is known that..." do (1:31-1:37).
2. **End the opening beat on a hidden reveal.**
   - What the episode does: it shows the newcomer from behind and below and reveals the face only at the last
     moment (2:02-2:08).
   - For us: show the creature's tail or shadow first and its face later; cut on the reveal.
3. **Make the solution a real natural fact, found by observing.**
   - What the episode does: the canyon's power is a magnetic field (11:05). It is read on a device that the episode
     shows four times (1:13.9, 7:37.2, 11:07.1, 13:35.5) and explained by the hero (14:43-14:50).
   - For us: the student's animal fact is the "device insert". Show the clue on screen (a sketch card, a footprint,
     a smell cloud) at least twice before it pays off.
4. **Let the myth or shortcut fail on screen.**
   - What the episode does: the "world-famous", expensive stone does nothing (9:12 → 14:37).
   - For us: a local superstition or magic item fails, and the real animal behaviour works. This delivers "real
     animal knowledge" as a twist, not a lecture.
5. **Remove the hero's supports one by one before the climax.** The episode takes away friends (9:51), light (10:44),
   map (11:07) and the lead (10:42, 12:58). In 60-90 s we can afford two removals: pick the two that make the fact
   necessary.
6. **Turn the goal into a moral choice at the climax, and make that our A/B vote.**
   - What the episode does: "win the race" becomes "save the rival" (13:20-13:58), and the prize is given away
     (14:23).
   - For us: put the bridge moment at the end of the Short, stop before the choice, and ask "Save the rival, or
     grab the prize?". Both sides must be defensible, as the race was real (9:49).
7. **The hero's kind choice causes the next problem.** Leaving Togedemaru behind (10:00) is why the cave is dark
   (10:44). Our student's good deed should create the next danger. Viewers then argue whether it was worth it.
8. **Cut after every beat to a reaction shot, and hold it.** Examples: group (6:48.5, 6.1 s), Ash's dot-eyes
   (8:24.5-8:28), Lana's four-step face (19:46.7-19:50.7). In vertical, the reaction close-up is our cheapest,
   strongest shot.
9. **Pace by scene type, not one global rhythm.**
   - What the episode does: dialogue holds ~3-4 s; action ~1.7 s; transformations under 1 s per cut (median
     0.67-0.79 s). Comedy medians run 1.9-4.4 s, each with a held reaction; emotional and listening holds run up to
     12 s (4.1).
   - For a Short: dialogue 1.5-2.5 s, action 0.8-1.5 s, impact cuts 2-6 frames. Keep one 2-3 s held reaction after
     each joke.
10. **Use the attack template** (6:42.1-6:48.5):
    1. command;
    2. extreme close-up of the eyes (5 frames);
    3. wind-up hold while only the effect grows (~2 s);
    4. a 4-frame strike;
    5. a 3-frame flash;
    6. a two-colour impact graphic on 2s (6 frames);
    7. the target flies off (0.8 s);
    8. a reaction hold.
    About 4 s in all for a Short. The wind-up hold is where we can save drawing work.
11. **Replace the background for the big moment** (starfield 13:40.9; bubble field 19:31.3; light curtain 17:13.5).
    One painted pattern behind a glowing silhouette costs little and reads instantly on a phone.
12. **Introduce each character with a signature emotion background** in 4-6 s (Mallow 0:09, Kiawe 0:15.8, Lillie
    0:21). Give the student and each recurring creature their own pattern, and reuse it as a visual "name tag".
13. **Undercut every dignified moment with a small gag:** "gigantic treasure... in my mind" (4:36-4:43); Hapu's sage
    line plus the rock (7:29-7:32); Horacio's soul-sigh (14:53). Undercut the deadly creatures too ("cute-but-deadly"
    is the same contrast).
14. **Use the speak-of-the-devil cut:** a name is mentioned, then a hard cut to that person or creature already there
    (0:41 → 0:43.8). It is a free laugh and a free introduction in under 3 s.
15. **Stage scares in this order:** an empty dark shot, a push into nothing, black, then eyes opening (11:19-11:25).
    Then the swarm and a scream. In vertical, the black frame with two eye-dots is a perfect stopping-thumb frame.
16. **If a Short continues, cut away on the scream.** The episode leaves Sophocles screaming and jumps to the other
    plot for 71 s (11:29 → 11:31.6 → 12:42.5). For a two-part Short, end Part 1 on the threat. For a single Short,
    end on the threat plus the A/B question: "Run, or stand still?"
17. **Colour-code places and moods.** Canyon warm, sea cool (4.6). Darkness, not hue, for fear (cave 0.25). The
    transformation has its own bright cyan. A muted dawn (saturation 0.31) for goodbyes. Pick one palette per biome
    in our world, and one "power" colour.
18. **Rhyme the threat and the payoff.** Golbats come out of the dark at the hero (11:24); later the hero's evolved
    partner comes out of the same dark (15:08-15:15). Repeat a scary composition at the win so viewers feel the turn.
19. **Show rivalry as a split screen with a diagonal seam** (8:41.7, 9:40.3, 13:16.6). In 9:16 this becomes a natural
    top/bottom split: student's eyes above, rival or creature below.
20. **Give the mentor one image-sentence, and pay it off with action, not words.** "The ocean will teach you the
    rest... remember that rhythm" (11:52-12:09) pays off as Popplio's song (19:22). One line of wisdom per episode,
    paid off in the last 15 s.
21. **Give creatures personality through eyes plus one physical action, with no lines.** Charjabug sparks to comfort
    (10:49.7); Vikavolt's eye glint before acting (13:55.0); Brionne's first act is a wink (19:43.6). Each creature
    gets one signature gesture we reuse every time.
22. **Give exposition to a character who has a reason to say it:**
    - a braggart who can't keep a secret (9:12-9:24);
    - the local who "knows" (1:37);
    - an encyclopaedia card (Rotom 3:32, 15:25).
    Our student's Earth knowledge can be the "card". Keep each to one or two short lines; the episode's lines are
    1-3 s.
23. **Give each character a verbal signature:** Horacio's self-title and folksy openers (7:50, 8:20); Hapu's "It is
    known that..." (1:37). Viewers recognise a recurring character from one line, which Shorts need because viewers
    arrive mid-series.
24. **Use a rival who loses small and leaves with dignity.** He is forgotten (8:13-8:21), slips his secret (9:18-9:24)
    and falls the wrong way (15:46-15:58), but exits with a respectable vow (15:40-15:46). That keeps him likeable
    enough to come back. Rotate story outcomes as CLAUDE.md requires: he should sometimes win.
25. **Bookend with the same image and frame line** (aerial 0:00 / 20:39.7; narrator "research projects" 0:01 / 20:40).
    In a Short, the last frame can echo frame 0, and the A/B question is the last spoken line. That fits our rule:
    question last, cut within 0.5 s.
26. **Prefer vertical camera moves.** The best "tall" moves here are the tilt up a rival from feet to face (8:10-8:13),
    the dive from surface to sea floor (12:27-12:42), the tilt down from sparkles to the crowd (17:48-17:52) and the
    balloon rising out of frame (17:40-17:45). They map directly onto 9:16; wide pans don't.
27. **Shrink the hero against something huge for awe:** the giant balloon over tiny figures (17:22; 19:25-19:27); a
    speck in a dark cave (10:34.7, 11:15.5). Our "deadly but cute" creatures read as dangerous mainly through scale
    shots like these.
28. **Hold the long shot for listening and goodbyes, not for information.** The 12-12.5 s holds are Ida's speech and
    Lana listening (11:50.9, 12:10.4). In a Short, one 2-3 s quiet hold before the A/B question gives the choice
    weight.

### Proportions to borrow (episode body 2:47-20:48 = 1,081 s → a 75 s Short)

| Story point | In the episode | Fraction of the body | In a 75 s Short |
|---|---|---|---|
| Want and doubt stated | 1:08-1:37, in the cold open | before the body starts | first 3-5 s |
| Rules / stakes | 9:49 | 39% | ~29 s |
| Lowest point (alone, dark, swarm) | 10:35-11:28 | 43-48% | ~32-36 s |
| Climax / choice | 13:20-13:58 | 59-62% | ~44-47 s |
| Twist (myth fails, fact wins) | 14:37-14:50 | 66-67% | ~49-50 s |
| A/B question | no equivalent | none | last line, ~70-75 s |

The fractions are measured from the body start (2:47.1) over 1,081 s. The episode resolves its moral choice itself
(13:58). Our format leaves the choice to the viewer, so in our Shorts the "climax / choice" row moves to the very end.
The fact-based twist then comes *before* it (around 60-70%), so viewers vote knowing the real animal fact.
