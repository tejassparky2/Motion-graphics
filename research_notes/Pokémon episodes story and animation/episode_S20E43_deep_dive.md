# S20E43 = SM043 "When Regions Collide!": story and animation deep dive (30 Oct 2026)

Study notes for our own original series. We copy technique only: no plot, characters, designs, names, or footage.
The video, frames, and transcript stay in the private scratchpad, and nothing from them is in the repo.

**How this was measured**
- Source: the owner's English-dub file (1280x720, 23.976 fps, 30,700 frames, 21:20.6).
- Timestamps are file time (mm:ss.s).
- Dialogue comes from the automatic Whisper-small transcript.
  - Lines that matter were re-transcribed with Whisper medium.en on short clips: 0:00-1:10, 9:50-10:16, 12:05-13:10, 13:20-14:33, 14:35-15:57, 16:40-17:46, 18:20-18:26, 19:20-20:40.
  - Whisper medium's segment times are rounded at clip starts, so treat dialogue times as ±1 s.
  - Names that Whisper misheard ("Turtinator", "Kiowai", "Gio-Doo", "zee move") are corrected only where the picture proves them.
- Pictures come from the 18 automatic contact sheets plus my own frame runs, every frame or every 2nd/3rd frame:
  - Flamethrower 8:44.0-8:50.6
  - Dig 9:35.0-9:39.5
  - Mega Steelix 10:08-10:26
  - Kiawe's Z-Move 11:04.8-11:26
  - Stone Edge 11:48.5-12:07
  - Gyarados send-out 14:12-14:18
  - Mega Gyarados 15:53-16:13
  - Iron Tail 16:53.3-16:57.4
  - Hurricane climb 17:43-18:03
  - Gigavolt Havoc 18:10-18:43
  - The ending 20:22-21:19
- Other measurements:
  - **Camera shake**: per-frame phase correlation.
  - **Holds**: frame-difference run lengths.
  - **Loudness**: RMS in 0.25 s steps, in dB relative to the episode median. Music, effects and voice are mixed, so I can't separate the music.

---

## 1. Identity, cast, settings

**Identity confirmed**
- **Title card at 1:39.9-1:48.9 (9.0 s):** "WHEN REGIONS COLLIDE!" in a white box on a patterned Alola-style frame, with a Z-Ring drawn on the right.
- The cold-open narrator names the place at 0:06: "Today, Pokémon battles at the Cerulean Gym!"
- The episode ends with the Kanto field trip ending (narrator, 20:17-20:30) and "To Be Continued" (20:42.8-20:49.5).
- These match SM043, the season 20 finale.

**Credits caveat**
- This dub file does **not** show the per-episode credits (screenplay, storyboard, director, animation director).
- Its English ED (20:50-21:20) is the series-wide roll:
  - "Written by" lists Aya Matsui, Atsuhiro Tomioka, Akemi Omode, Shoji Yonemura, Junichi Fujisaku and Ayumi Sekine (frame 20:53.2).
  - The storyboard list includes Masakatsu Iijima (20:55.0).
- So the credits "Tomioka / Iijima / Nakano" are consistent with the file but rest on the sourced research note, not on this video.

**Main cast (all seen on screen)**
| Side | Characters (Pokémon used here) | First clear frame |
|---|---|---|
| Hero | Ash (Pikachu; Lycanroc, Rowlet and Litten only watch) | 0:06.8, Pikachu on his shoulder |
| Classmates | Kiawe (Turtonator; Alolan Marowak), Sophocles (Togedemaru), Lillie (Alolan Vulpix), Lana (Popplio), Mallow (Steenee) | 0:03.8 group at the bus |
| Teacher | Professor Kukui; Rotom Dex (commentator / encyclopedia) | 0:06.8; 3:22.2 |
| Gym leaders | Misty (Psyduck; Gyarados → Mega Gyarados); Brock (Geodude; Steelix → Mega Steelix) | 0:28.1; 0:36.3 |
| Cameos | Professor Oak and an older man in an Alolan shirt at the airport, probably Samson Oak (not named in dialogue); Jigglypuff; Team Rocket (Jessie, James, Meowth, Wobbuffet) carried by Bewear | 19:57.4; 20:31.2; 20:36.7 |

**Settings**
- Cerulean Gym exterior with the bus (0:00).
- Pink gym doors (0:11.6).
- **One arena for every battle**:
  - A rock field with rocky arches (overhead 0:16.7; wide 7:30.3), a star-shaped emblem above the stands (10:08.0) and stands for the class.
  - Brock's battles are in this same Cerulean arena, with Misty refereeing at 7:34.2. This settles a gap in the earlier research note.
  - The floor sinks and floods into a pool with rock islands for Misty's battle (13:10-13:24).
- Airport: exterior at 19:22.6, concourse at 19:28-20:21, a sunset take-off at 20:22.0, the plane in a night sky at 20:27.5.
- The open sea for the Team Rocket tag (20:33.0).

---

## 2. Beat sheet

Structure markers, at a glance:
- Cold open 0:00-1:09.9
- **Opening song** 1:09.9-1:39.9 (30 s, credits on screen)
- **Title card** 1:39.9-1:48.9, then 0.5 s black
- **Eyecatch / act break**: "Who's That Pokémon?", Psyduck silhouette 10:28.4 (6.0 s) and answer 10:34.4 (6.0 s)
- A 0.5 s black at 19:07.4 may be a second broadcast break point (uncertain)
- Tag gags 20:29-20:49
- **ED** 20:50-21:20
- There is **no post-credits scene in this file**: the Jigglypuff gag the research note calls post-credits plays *before* the ED here, at 20:29-20:32.

| Time | Scene / place | Who | Wants | Obstacle | Turn | Emotional / comic beat |
|---|---|---|---|---|---|---|
| 0:00-0:10 | **Cold open**: gym exterior, bus | Narrator over the group | Set the premise | n/a | n/a | Promise of the day: "Pokémon battles at the Cerulean Gym!" |
| 0:11.6-0:32.6 | Gym door → dark corridor → rock field | Class, Psyduck, Misty | See the gym | Field is empty except a lone Psyduck ("Something's over there!", 0:19; "it's Psyduck!", 0:25) | Misty appears beside it and thanks it "for minding the store" (0:28), then welcomes them to "my gym" (0:33) | Visual question (why is a dopey duck alone on a battlefield?) answered with a joke (the duck was left in charge), then the owner's pride |
| 0:42.7-1:09.9 | Field | Ash, Kiawe, Kukui, Misty, Brock | Ash wants to battle now (0:42-0:48) | Nobody knows the rules yet | Kukui's formal intro of both leaders (0:49-1:03) → "These are the two you'll be battling" (1:04) | **Hook ends** on Kukui's glasses gleam (1:06.7) and an ECU (1:07.0, 2.8 s): "feel the heat" |
| 1:09.9-1:48.9 | OP, title card | n/a | n/a | n/a | n/a | n/a |
| 1:49.4-2:37 | Field, overhead 10.7 s | Kukui, leaders, class | Teach gyms, badges, the League | Class has never heard of them | Misty and Brock thrust badges at the lens (2:00.1, 2:03.0) | Tease: Misty and Brock in a split frame recall giving a badge "out of pity" (2:17.9-2:23), Ash protests |
| 2:37-3:27 | Field / stands | Everyone | Pick opponents | Too many volunteers, Lillie unsure (2:58) | Kiawe picks Brock (2:53); Ash wants both (2:55.9); Lana and Mallow go first vs Misty | Ash: Misty "may not look it, but she's tough" → Misty annoyed (3:08-3:19). Rotom will "record all the action" (3:22) |
| 3:27-5:01 | **Battle 1** (double): Lana + Mallow vs Misty's Psyduck | | Beat Psyduck | Psyduck is unpredictable ("kind of a flake", 4:23) | Water Gun turned into a balloon trap (3:47-4:08); Magical Leaf pops it and Psyduck lands on its head (4:30.9-4:33.9) → headache → eyes glow (4:42.9) → Confusion lifts both opponents (4:47.9-4:50) | Misty calls it off herself ("And that's that", 4:57, Whisper-small wording), praises their "battle instincts" (5:06), hugs Psyduck (5:26.0, 9.4 s) |
| 5:35-6:32 | **Battle 2**: Lillie + Sophocles vs Brock's Geodude | | Win with Zing Zap | Electric has no effect | Brock: the Kanto Geodude is Rock/Ground, not the Alolan one (5:57-6:06) | Sophocles' comic despair on a red burst BG (6:06.1, 5.0 s); Geodude spins Gyro Ball as a *defence* (6:20.8-6:27) |
| 6:32-7:52 | Field (talk) | Brock, Kukui, Sophocles, Kiawe, Ash | Draw the lessons; set the main battles | n/a | Brock: a challenger once taught him to "think outside" the box (6:41-6:48); Kukui: endless possibilities (6:48); Sophocles: know your opponent (7:02) | Kiawe and Ash declare their opponents (7:09-7:17). Brock: how trainer and Pokémon combine strengths matters more than winning (7:46-7:52) |
| 7:52-10:28 | **Battle 3, act 1**: Kiawe/Turtonator vs Brock/Steelix, Misty referees | | Kiawe: prove his strength (7:42) | Steelix's size (8:06.2) and versatility | Phases listed in §3c; Z-Move decision (9:50-9:58) → Brock answers with Mega Evolution (10:08-10:25) | Brock rips his shirt off before evolving (10:06.9-10:08.6); Kiawe and Ash shocked in a split (10:11.9) |
| 10:28.4-10:40.4 | **Eyecatch** "Who's That Pokémon?" (Psyduck) | n/a | n/a | n/a | n/a | Cliffhanger: the break falls on the Mega reveal, not on a result |
| 10:40-12:12 | **Battle 3, act 2** | | Kiawe: land the Z-Move | Mega Steelix survives it (11:24.5-11:31.2) | Stone Edge beats Dragon Tail (11:48-12:02); Turtonator faints (12:06.3); Misty: "Steelix wins!" (12:08-12:11) | Class: "Kiawe lost!" … "Gym leaders are strong!" (12:13-12:17); Rotom over-excited (12:19) |
| 12:22-13:10 | Field aftermath | Brock, Kiawe, Marowak, Kukui, class | Kiawe tends Turtonator | Kiawe's frustration | Marowak bonks Kiawe with its bone (12:40.6-12:42) → line: "praise them for their work" (12:47) | Kukui: "What did you think? Talk to me!" (12:53) → "I was on the edge of my seat!" (12:56) |
| 13:04-14:33 | Field changes to water | Ash, Misty, Sophocles, Kiawe, Rotom | Ash: his turn | Water field = disadvantage, nowhere for Pikachu to stand (13:35-13:38) | Ash: "I got this covered" (13:41); Pikachu stands on a rock islet (13:44-13:50) | Ash's rapid comic fist pumps (13:24.6-13:26.1); Rotom's flying screen gag (13:54.6-13:59.3); Gyarados reveal and the Dex legend of a burned town (14:12-14:32) |
| 14:33-18:44 | **Battle 4** (climax): Ash/Pikachu vs Misty/Gyarados, Brock referees | | Ash: win | Water, size, Rain Dance + Hurricane, Mega Evolution | Phases listed in §3c; turning point "Climb up the hurricane!" (17:43.6); finisher Gigavolt Havoc (18:10-18:34) | "Gyarados is unable to battle… Pikachu is the winner!" (18:40-18:43); cheek-to-cheek hug (18:46.8) |
| 18:50-19:24 | Field | Misty, Ash, class, Kukui | Close the battle | n/a | Misty and Ash trade compliments and a tease about the "little kid inside" one of them (18:52-19:05; who says which line is unclear) | Kukui: "Treasure this experience" (19:16-19:24) |
| 19:22-20:16 | Airport | All | Say goodbye | Leaving | Replica badges handed out (19:28.5; "They're replicas, but they'll remind you of today", 19:30); Kiawe vows a real win next time (19:43.6), Brock: "You're welcome to try" | Kukui: make the League an Alola tradition (19:53.6); an elder approves (19:57.8; Oak or the older man, speaker uncertain); Brock and Misty: "your turn to come visit" (20:09) |
| 20:13.5-20:30 | Overhead airport → sunset plane | Narrator | **Pull to next season** | n/a | "Can Professor Kukui's dream of creating an Alolan Pokémon League become a reality?" (20:22) | Open question, not a promise |
| 20:29-20:32.5 | Plane wing, night sky | Jigglypuff | n/a | n/a | n/a | Callback gag: Jigglypuff asleep on the wing |
| 20:33-20:49.5 | Open sea | Team Rocket, Bewear | Get home | Bewear has been swimming for days | n/a | "To Be Continued" over the gag (20:42.8) |
| 20:50-21:20 | **ED** | n/a | n/a | n/a | n/a | Ash hugs Pikachu on a white BG (21:15-21:19) |

Battle lengths escalate:
- Battle 1 is ~94 s and Battle 2 is ~54 s; both are comic and small.
- Battle 3 is ~4:08 of battle (7:52-12:12, minus the 12 s eyecatch); it is the big loss.
- Battle 4 is ~4:10 (14:33-18:44); it is the hero's win.

---

## 3. Storytelling analysis

### 3a. Hook and central question
- **The premise in one line, over the place:**
  - The narrator states it over a wide of the gym (0:00-0:10).
  - The first image *inside* is a contradiction: a vacant-looking Psyduck alone on a battlefield (0:20.6-0:28.1).
- **The question is posed by a character, not the narrator:**
  - Kukui introduces both leaders, then delivers the stakes: "These are the two you'll be battling" (1:04).
  - The camera goes to a glasses gleam (1:06.7) and an ECU (1:07.0) right before the OP.
  - The Japanese title is "Gym Battle! Z-Move vs. Mega Evolution!!" (research note), and the title card carries a Z-Ring (1:39.9). So the real question is whether Alola's Z-power can beat Kanto's Mega Evolution.
- **The answer is split, 1-1** (my inference from the outcomes):
  - Mega beats Z in Kiawe's battle (12:06-12:11).
  - Z beats Mega in Ash's (18:34-18:43).
  - Neither region "loses", which fits the title's collision and the closing lesson ("treasure this experience", 19:16).
- **Small questions keep the viewer leaning in**:
  - Will Psyduck do anything? (answered at 4:42.9)
  - Why didn't Zing Zap work? (answered at 6:01)
  - Where will Pikachu stand? (answered at 13:41-13:50)
  - Can anyone break the Hurricane? (17:30 → 18:02)

### 3b. Set-ups and payoffs
| Set-up | Payoff |
|---|---|
| Psyduck alone on the field, dazed (0:20.6-0:28.1); Misty: Psyduck is at its best when the chips are down (4:07); spectators: Psyduck is "kind of a flake" (4:21-4:23) | It falls on its head (4:31.9), its eyes glow (4:42.9), and Confusion lifts both opponents (4:47.9-4:50). Psyduck is also the Who's That Pokémon (10:28.4) |
| Geodude uses Gyro Ball as a defensive spin; spectators note that an attack move can be used this way "depending on how you train" (6:20.8-6:29) | Steelix uses Gyro Ball to scatter Flamethrower (8:53.2), and a spectator says "more thinking out of the box" (8:53) |
| Brock: a past challenger taught him to think outside the box (6:41-6:48), an unnamed nod to Ash | Ash climbs the hurricane; Brock smiles knowingly (17:48.0) and says "That's Ash for you" (18:04-18:05) |
| Sophocles mistakes the Kanto Geodude for the Alolan type (5:49-6:06); lesson: know your opponent (7:02) | Before Battle 3 he does the type maths carefully: fire beats steel, ground beats fire, "evenly matched" (8:22-8:36) |
| Brock: trainer and Pokémon combining strengths matters more than winning (7:46-7:52) | Mega Evolution defined as trainer and Pokémon "hearts" joining (10:53-10:59); after the loss, "praise them for their work" (12:47) |
| Kiawe: "I'm confident about my strength" (7:42) | "I can't win this with a prolonged battle" (9:50) → loses (12:06) → vows a *real* win next time (19:43.6) |
| Badges explained (1:50-2:05) | Replica badges given at the airport (19:28.5-19:41) |
| League explained (2:27-2:36) | Kukui's dream of an Alola League (19:53.6), restated as the narrator's open question (20:22) |
| Ash: "I want to battle both of them!" (2:55.9) | "Misty, don't forget, I'm next!" (13:04) |
| Ash teases Misty's toughness (3:08-3:19) | She proves it in Battle 4; the tease returns as the "little kid inside you" exchange (18:58-19:05) |
| Brock's Key Stone and Mega Evolution (10:13-10:25) | Misty reveals her own Key Stone in her hair tie, "Looks great on me, don't you think?" (15:48-15:50); Ash: "You got one too!" (15:52) |
| Rain Dance (14:59.9-15:07) + Hurricane cancels Electro Ball (15:18-15:33); Kukui names the combo (15:33-15:40, again 17:14) | The Hurricane becomes a prison (17:13-17:29) and then the hero's ladder (17:43-18:02) |
| OP shows Ash's Z-pose and Pikachu's bolt (1:28.4-1:31.2); title card shows the Z-Ring (1:39.9) | Gigavolt Havoc finisher (18:10-18:34) |
| Team Rocket absent all episode; Jigglypuff never mentioned | Both get the last gags (20:29-20:49) |

### 3c. How each battle is structured
**Battle 3: Kiawe vs Brock (the loss)**
1. **Send-outs and size**:
   - Kiawe's throw has smear frames (7:54.9-7:55.7).
   - Brock throws from a framed "trainer card" pose on a star BG (8:01.3).
   - Steelix: ECU with sparkles (8:03.5), roar (8:04.3), then towering over Kiawe (8:06.2), and Kiawe sweats (8:08.1).
2. **Information**: a Rotom Dex entry over a lava illustration (8:11.9-8:21), then Sophocles' type maths ending "evenly matched" (8:22-8:36).
3. **Opening exchange**: Misty signals the start (referee pose, 8:42.2-8:44.2), then Flamethrower (8:44.2-8:50.5).
4. **Opponent's strength revealed**:
   - Steelix's Gyro Ball spins the fire away (8:53.2-8:55.6) and Steelix grins through the flames (8:55.6).
   - Then Gyro Ball attacks (9:02.7-9:04.9) and Steelix wraps Turtonator (9:07.0-9:10.5).
5. **Counter and respect**:
   - Shell Trap explodes out of the bind (9:11.8-9:15.5).
   - Mutual respect: "Hey, not bad." "Not so bad yourself." (9:23-9:25)
6. **Hero in trouble**:
   - Steelix dodges Dragon Tail by Digging (9:28-9:35), shakes Kiawe (9:36-9:37.6) and bursts up under Turtonator (9:39.2).
   - Kiawe: he "can't win this with a prolonged battle", so he goes for a Z-Move (9:50-9:58).
7. **Opponent escalates instead of the hero**:
   - Brock: Z-Moves use all your power, so "we'll counter with all our power" (9:59-10:05).
   - Then the shirt rip and Mega Evolution (10:06.9-10:25).
   - **Act break** (10:28).
8. **Strategy**:
   - After the break, explanation and a dare: Mega Evolution is hearts joining (10:53); Brock asks to be shown a Z-Move (11:02).
   - Then Inferno Overdrive (11:04.8-11:25).
9. **Twist**: smoke holds 4.8 s (11:26.4-11:31.2), then Mega Steelix is scratched but grinning (11:31.2). The commentary says the Z-Move "definitely affected" Steelix but Turtonator couldn't take "one last step" (11:39-11:48).
10. **Finisher**: "Use Stone Edge!" (11:48) vs "Dragon Tail!" (11:54), then the crystal wave and explosion (11:52-12:02.1).
11. **Reaction**:
    - Kiawe (12:01.5), Ash and Pikachu (12:02.9), smoke (12:03.9).
    - Turtonator's swirl eyes (12:06.3), Misty's ruling (12:08.3), then the class (12:13-12:17).

**Battle 4: Ash vs Misty (the win)**
1. **Field disadvantage first**: the field floods (13:10-13:24), followed by "Does Ash realize…" (13:35) and "where is this Pokémon supposed to stand?" (13:38).
2. **Opponent revealed**:
   - The Gyarados reveal: ball in a void, then eye, face, roar (14:12-14:19).
   - Dex legend of a town burned in one night (14:22-14:32), and the class's Pokémon cower (14:32.4).
3. **Opening exchange**:
   - Brock signals the start (14:33.5-14:36).
   - Thunderbolt charge (14:36.5-14:40), answered by Misty's Hydro Pump, which meets it in a water burst (14:41-14:44).
   - "Water-type moves can stop electric types", and Rotom can't compute it (14:45-14:48).
4. **Small hero gains**: Quick Attack lands on Gyarados' forehead, a tiny Pikachu on a huge face (14:49.9-14:56).
5. **Opponent's control**:
   - Rain Dance turns the arena dark: "How can it rain in here?" (14:59.9-15:12).
   - Hurricane eats Electro Ball (15:14-15:27).
   - Misty taunts that there's nowhere for Ash to run (15:31-15:33), and Kukui explains the plan (15:34-15:42).
6. **Escalation**: the Key Stone reveal (15:48-15:50), Ash's shock (15:52-15:53.9), then Mega Gyarados (15:54-16:12).
7. **Hero in trouble**:
   - Water attacks wash Pikachu into the pool (16:25-16:30); Pikachu swims, tiny in frame (16:29.9 and 16:34.8).
   - Gyarados bites at it on the rocks (16:39-16:45).
8. **Partial recovery**: Ash says Iron Tail "won't work from that posture", jump on Gyarados first (over his shouting shots 16:41.6-16:48.4; Whisper timing approximate here). Iron Tail hits the face (16:50-16:57.1).
9. **Trap closes**:
   - Hurricane prison (17:13-17:29), and Thunderbolt is swallowed (17:22-17:29).
   - Misty: no challenger in her gym has ever broken through it (17:30).
10. **Turning point**:
    - Ash reframes it: thanks for telling me, breaking through makes battling awesome (17:35-17:38).
    - Across the wind: "Hey, Pikachu, can you hear me?" (17:41), then "Climb up the hurricane!" (17:43.6).
    - Confusion beat: Misty (17:46.2), a five-way split (17:47.2), Brock's knowing smile (17:48.0), Rotom (17:49.2).
    - Pikachu runs up the spiral (17:54.4-18:01), Kukui reacts ("Electric platforms!", then covers his face and laughs, 17:57-17:59.6), and the class cheers (18:01.8).
11. **Finisher**: "time for a Z-Move" (≈18:08), the Gigavolt Havoc kit (18:10-18:28.7), the spear (18:28.7-18:31.6) and impact (18:34.1).
12. **Reaction**:
    - Water shockwave (18:36-18:38), Gyarados back to normal with swirl eyes (18:39.5-18:41.7).
    - Ruling (18:40-18:43), Ash's victory pose (18:44.1), hug (18:46.8).
    - Misty recalls Gyarados (18:49.3), then a 10.6 s two-shot of Misty, Ash and Pikachu (18:56.8).

**Shared skeleton** (both big battles):
- Send-out and reveal, then a Dex card.
- Opening exchange that the opponent shrugs off.
- The opponent's signature control: Bind/Dig, or Rain/Hurricane.
- The hero's partial success.
- The opponent's Mega escalation.
- The hero's all-in move.
- Result hidden by smoke or mist, then the KO face, the referee's line, and spectator reactions.

**Small battles are one-joke structures:**
- Battle 1: set-up "Psyduck is a flake" → slapstick → hidden power → leader calls it.
- Battle 2: confident attack → no effect → explanation → comic despair.

### 3d. Making Kiawe's loss meaningful
- **The value is planted before the battle**:
  - Brock says what a leader looks for: trainer and Pokémon combining strengths, over winning (7:46-7:52).
  - Kiawe boasts about strength (7:42), and the loss tests exactly that.
- **He loses to something bigger, not to a mistake**:
  - Brock answers Kiawe's all-in with his own all-in (9:59-10:05).
  - The Z-Move is shown to work. It visibly damaged Mega Steelix: a scratched ECU (11:31.2), steam (11:41.7), and the commentary at 11:39-11:46.
  - Only stamina decides it, shown on Turtonator's tired ECU (11:43.8).
- **The loss gets silence**: the loudness drops to -9 to -11 dB on Turtonator's swirl eyes (12:05.5-12:06.5), then the ruling.
- **Care before comfort**: Brock thanks Steelix (12:31), Kiawe kneels by Turtonator (12:36.6-12:40.5, 3.8 s near-still).
- **Reframed through his own Pokémon**: Marowak bonks Kiawe with its bone (12:40.6-12:42.0), and the lesson line plays over Brock (12:45.5): "you should praise them for their work" (12:47).
- **Turned into a shared high**:
  - Kukui asks how they felt (12:53).
  - The class answers with "edge of my seat" and "heart's still racing" (12:56-12:58).
- **Pays off as a future goal**: "I'll win a real battle the next time we meet" … "You're welcome to try." (19:43.6-19:46)

### 3e. How mentors and rivals talk
- **Brock** is calm, generous and explanatory:
  - He corrects the kids' type error without mockery (5:57-6:06).
  - He shares his philosophy (7:46).
  - He brags only with a joke: "I'm not called Brock the Rock for nothing" (10:05).
  - He tests the hero ("I've heard about Z-Moves… show me one", 11:02) and credits the rival ("That's Ash for you", 18:04).
- **Misty** is proud, teasing and competitive:
  - "my gym" (0:32); "Looks great on me, don't you think?" about her Key Stone (15:48).
  - She is open about her trap: no challenger has ever broken through (17:30).
  - She praises opponents afterwards: "battle instincts" (5:06).
  - After the climax she thanks her own Gyarados for "an amazing battle" (18:52) and tells Ash he has grown (18:55, Whisper-small wording, cut off).
- **Kukui** is the enthusiastic teacher who frames each lesson:
  - "endless possibilities" (6:48).
  - He analyses mid-battle (15:33-15:40) and asks for feelings, not facts (12:53).
  - He sums up with a value ("Treasure this experience", 19:16-19:24).
- **Old-friend banter** carries the history without flashbacks:
  - The badge "out of pity" (2:18-2:23) and "it felt like old times" (20:07).
  - Brock's unnamed "challenger" (6:41).
- **Rival respect inside the fight**: "Hey, not bad." "Not so bad yourself." (9:23-9:25)

### 3f. Pokémon personality without words
| Pokémon | Acting | Time |
|---|---|---|
| Psyduck | Blank stare, clutches its head, comic gritted face; power comes from pain | 0:22.2; 4:38.9-4:39.6; 5:13.4; 4:42.9 |
| Steelix | Grins through fire (confidence); Mega form scratched but grinning; exhales steam (pride and fatigue) | 8:55.6; 11:31.2; 11:41.7 |
| Turtonator | Tired ECU with sweat before the end; swirl eyes on KO | 11:43.8; 12:06.3 |
| Alolan Marowak | Anger mark, bone bonk, steam puffs from its nose, lecturing gestures | 12:40.6-12:45.3 |
| Gyarados | Eye-first reveal, roar held ~2 s; Mega form spreads its fins in the storm | 14:15.2-14:19; 17:17.8 |
| Pikachu | Worried on a lonely rock; cheek sparks; shadowed determined close-up during the Z-dance; cheek-to-cheek hug after | 13:48.3; 14:38.9; 18:16.5-18:17.3; 18:46.8 |
| Class Pokémon | Litten, Lycanroc and Rowlet cower at the Gyarados legend | 14:32.4 |

### 3g. Bonds shown *during* battle
- **Mega Evolution draws the bond as a picture**: two energy streams, from the trainer's Key Stone and the Pokémon's Mega Stone, twist and join.
  - Steelix: 10:19.6-10:21.2. Gyarados: 16:03.3-16:04.6.
  - Brock then *says* what it shows: hearts joining as one (10:53-10:59).
- **The Z-Move is a shared dance**: the trainer's poses send power into the Pokémon.
  - Kiawe's poses (11:07.3-11:12.2) cut to close-ups of Turtonator's shell (11:09.3-11:10.9).
  - Ash's pose cuts to a shadowed Pikachu (18:16.5-18:17.3), then both glow in one frame (18:19.1-18:20.0).
- **Accelerating cross-cut**: Ash and Pikachu alternate in shots of 3 (Ash), 6, 5, 5, 4, 3, 2, 2, 2 frames (18:26.60-18:28.06), then a matched forward push.
- **Voice across the obstacle**: "Hey, Pikachu, can you hear me?" through the hurricane (17:41); "Pikachu! Are you okay?" "Pika!" (15:44-15:46).
- **Before and after the result**:
  - Before: Misty hugs Psyduck (5:26).
  - After: Brock thanks Steelix (12:31), Kiawe kneels by Turtonator (12:36.6), Ash and Pikachu hug cheek to cheek (18:46.8).

### 3h. Comedy patterns
- **Cut to the bystander after a tense beat**:
  - Rotom: "This data will never ever be deleted!" (12:19) right after the KO.
  - Marowak's bonk (12:40.6) right after Kiawe's quiet moment.
- **Escalate to absurd during a power-up**: Brock rips off his shirt, which lands on the gym emblem (10:06.9-10:08.0), before Mega Evolution.
- **Comic shapes and backgrounds**:
  - Sophocles' hands-on-cheeks on a red burst BG (6:06.1).
  - Chibi shock on Ash (15:53.0-15:53.9).
  - Bug eyes on Kiawe and Turtonator (12:41.0).
  - Swirl eyes on KO (12:06.3, 18:39.5).
- **Repetition-by-editing**: Ash's two fist-pump poses alternate every 2-6 frames for 1.5 s, ending on a sparkle (13:24.6-13:26.1). Rotom zips around in 0.2 s cuts (13:54.6-13:59.3).
- **Character running jokes**:
  - Psyduck is a flake who turns into a power (4:21-4:50).
  - Misty's vanity (15:48) and her irritation at "tough" (3:16).
  - Rotom's "does not compute" (14:46, 17:49).
- **Callback gags for fans at the end**: Jigglypuff asleep on the wing (20:29-20:32.5); Team Rocket towed across the sea by Bewear (20:34-20:49).

### 3i. Dialogue during action
- **Callouts are 1-4 words**, and the Pokémon moves within about a second:
  - "Use Stone Edge!" (11:48); "Dragon Tail!" (9:28, 11:54); "Quick Attack!" (14:49.9).
  - "Follow it with Electro Ball!" (14:56.9); "Climb up the hurricane!" (17:43.6).
- **Coaching beats** are longer but still one idea: Iron Tail "won't work from that posture" → jump on Gyarados first → now Iron Tail (16:41.6-16:48.4, timing approximate).
- **The chorus explains, so the fighters don't have to**:
  - Sophocles' type maths (8:22-8:36).
  - Kukui's analysis (15:33-15:40; 17:14).
  - Rotom's Dex entries (8:11.9; 14:22-14:32).
  - Spectators' "Look at that! A direct hit!" around the Iron Tail hit (≈16:57; Whisper timing unreliable in this clip).
- **The rival tells the hero the rule they will break**: "Not a single challenger… has ever broken through it" (17:30).
- **Transformation chants and named finishers**:
  - "Time for… Mega Evolution!" (10:14-10:16).
  - "here we go, with full power, now!" then "Gigavolt Havoc!" (18:20-18:26).
- **Silence during the biggest visuals**:
  - The Whisper transcript has no dialogue from 10:16 to 10:38 (Mega Steelix) or from 11:05 to 11:39 (Kiawe's Z-Move), apart from shouts.
  - These pieces are carried by picture and sound only.

### 3j. How the finale closes and pulls forward
1. **Debrief and value**: "Treasure this experience, and when you're back in Alola, keep it with you." (19:20)
2. **Tokens**: replica badges (19:28.5-19:41).
3. **Unfinished business** stated as a promise: Kiawe's rematch (19:43.6).
4. **Bigger goal**: Kukui wants a League as an Alola tradition (19:53.6), with an elder's approval (19:57.8).
5. **Reversal of the journey**: "now it's your turn to come visit me in Alola" (20:09).
6. **Narrator's open question** over a high overhead and a sunset take-off (20:16.9-20:30).
7. **Time passing through colour**: day concourse → orange sunset (20:22.0) → deep-blue night (20:27.5) → bright daytime sea (20:33.0), joined by dissolves (20:25.7, 20:29.3).
8. **Two gags**, then "To Be Continued" (20:42.8).

---

## 4. Animation and staging analysis

### 4a. The true cutting rate (shot detector vs. eyes)
- **The detector's numbers**:
  - It found 707 shots (median 1.13 s).
  - The same detector found 415 and 435 shots (median about 2.5 s) in the two sibling episodes (scratchpad `.ev`).
- **I checked 140 detected boundaries by eye** (the frame before, the frame after, and +6 frames):

| Stretch | Detected shots | False cuts | Real shots | Median detected → real | Mean real |
|---|---|---|---|---|---|
| Kiawe battle 8:37-9:35 | 40 | 11 (28%) | 29 | 1.21 s → **1.88 s** | 2.01 s |
| Ash climax 17:33-18:33 | 60 | 18 (30%) | 42 | 0.54 s → **1.06 s** | 1.43 s |
| Talk 2:00-3:09 | 20 | 2 (10%) | 18 | 2.86 s → **3.11 s** | 3.96 s |

- **The false cuts** are:
  - 1-2 frame white or colour flashes (8:48.71; 9:13.51; 9:04.92).
  - Inverted black/white impact frames (9:08.55; 9:39.13; 18:21.59; 18:32.72-18:33.56).
  - Effects that fill the frame inside one shot: a fireball becoming a beam (8:48.36), dust filling the screen (9:17.18; 9:35.20), Pikachu's glow (18:22.27-18:22.85).
  - Smear and pose snaps on a held background (8:46.36; 9:05.59; 2:56.97).
- **Conclusion**:
  - The 1.13 s median *is* inflated by effects. The real rate in battle is about **one cut every 1-2 s**:
    - Ordinary exchanges run about 1.9 s per shot.
    - The finisher build-ups run about 1.0-1.4 s.
    - Single cross-cuts drop to 2-6 frames (18:26.6-18:28.1).
  - Talk cuts about every **3-4 s**, with single holds up to 8.9 s (Brock, 9:58.0) and 14.6 s (2:23.4).
  - Even after the correction, this episode cuts noticeably faster than its siblings. That is an inference: it is battle-heavy.
- **Per section (detector, uncorrected)**:

| Section | Shots | Median | Share of held frames |
|---|---|---|---|
| Cold open | 22 | 3.0 s | 0.54 |
| Gym talk 1:49-3:27 | 27 | 3.1 s | 0.56 |
| Battle 1 | 55 | 1.25 s | 0.56 |
| Pre-Kiawe talk 6:32-7:52 | 15 | 5.6 s | 0.73 |
| Battle 3, act 1 | 113 | 0.96 s | 0.40 |
| Battle 3, act 2 | 67 | 0.92 s | 0.33 |
| Battle 4 | 219 | 0.75 s | 0.28 |
| Resolution 18:44-20:35 | 27 | 3.6 s | 0.72 |

  - The episode breathes: every battle is followed by a long talk section with a 3-6 s median. The wind-down after the climax is the slowest part (median 3.6 s, 12 shots over 4 s).

### 4b. Holds, on 2s and 3s
- **Measured by frame-difference run lengths** (256 px grey, threshold 0.6). The table gives the share of frames by how long each drawing is held:

| Stretch | 1 frame | 2 frames | 3 frames | 6+ frames |
|---|---|---|---|---|
| Talk 2:00-3:09 | 26% | 6% | **31%** | **35%** |
| Resolution 18:50-19:50 | 23% | 5% | 18% | **52%** |
| Kiawe battle 8:37-9:35 | **55%** | 15% | 6% | 22% |
| Ash climax 17:33-18:33 | **62%** | 6% | 12% | 19% |
| Gyarados fight 16:20-17:20 | **72%** | 11% | 9% | 8% |

- **Talk** is character acting on 3s plus long holds with mouth flaps (Brock's 8.9 s hold at 9:58.0).
- **Battle** changes most frames, but much of that is:
  - Camera moves: the push-in on Turtonator (8:46.75-8:47.9), the tilt-down to Brock (10:08.0-10:08.6), the slow drift in the Gigavolt Havoc hit shot (18:34.1-18:35.3, +1 to +3 px per frame).
  - Effects animated on 1s: the fire column (8:48.8-8:50.5).
  - The rain overlay from 15:00, which changes every frame.
- **Characters in action are mostly on 2s**: Pikachu's run along Gyarados' back alternates every 2 frames (16:53.30-16:54.30).
- **Camera shake is also on 2s** (see 4d).

### 4c. Frame-by-frame: key attacks
**A. Turtonator's Flamethrower (8:44.2-8:50.5): a clean anticipation → beam → impact → hold.**
- **Command shot**:
  - Kiawe on an orange diagonal speed-line BG holds one drawing for ~1.7 s with mouth flaps (8:44.21-8:45.84).
  - A pose snap on a held BG gives a mouth-wide shout (8:45.88).
  - The arm sweeps with a 2-frame smear (8:46.38-8:46.42), then the hand thrusts at the lens, held 6 frames (8:46.50-8:46.71).
- **Anticipation**:
  - The cut goes to Turtonator in a wide shot and the camera pushes in for ~1.2 s (8:46.75-8:47.92).
  - Fire swells in its mouth for about 20 frames (8:47.50-8:48.34).
  - Inside the charge sits a **3-frame eye ECU in hot yellow-orange** (8:47.96-8:48.05).
  - Then a profile: a fireball grows in concentric orange rings and the BG darkens to near black (8:48.09-8:48.34, ~6 frames).
- **Beam**: it extends as a tapering orange cone with a yellow core across 8 frames (8:48.38-8:48.67). It is the same layout as the fireball, so it isn't a cut.
- **Impact**: **2 frames of full-screen orange/yellow flash** (8:48.71-8:48.75).
- **Hold on the result**: a pillar of fire engulfs Steelix for 1.75 s, the flames animated on 1s (8:48.80-8:50.51).
- **Cut to the opponent trainer**, not the attacker: Brock grins (8:50.55). A confident opponent tells you the attack didn't work.

**B. Steelix's Dig and the eruption (9:32.5-9:41.4): shake the reaction, then inverted impact frames.**
- **Eye glint** on Steelix (9:32.45, 4 frames). It dives, and the ground passes the lens (9:32.6-9:35.2).
- **Dust fills the frame** for ~10 frames (9:35.29-9:35.71). A red flash of Turtonator's shell (9:35.79-9:35.83), then an ECU of Kiawe's shouting mouth (9:35.88-9:36.04).
- **Camera shake on Kiawe's reaction**:
  - First burst: amplitude about 93 px (at 320 px wide) on the first frame, then 12, 11, 15, 7, 4, 3 px. The offset changes **every 2 frames** and decays to zero over ~0.6 s (9:36.04-9:36.58).
  - Second burst: 53, 60, 83, 20, 39, 12, 5, 3 px (9:36.88-9:37.54).
- **The ground erupts in a wide shot** (9:37.96-9:38.92).
- **Impact frames**: 3 frames of brown speed-streak smear (9:38.96-9:39.09), **2 frames of black with white crack lines** (9:39.13-9:39.17), and **1 white frame** (9:39.21).
- **Reveal**: Steelix bursts up under-lit with glowing red eyes and flying rocks (9:39.25). Turtonator is thrown (9:39.2 shot, 2.0 s), a dark sky with debris (9:41.2), and it lands in dust (9:41.4).
- Spectators react: Ash and Rotom (9:43.1), the girls (9:45.9).

**C. Mega Steelix's Stone Edge vs Dragon Tail (11:48.5-12:08): the finisher.**
- **Command**: Brock close (11:48.5), turns his back (11:49.25), then thrusts his arm (11:49.50-11:50.0).
- **Power-up inserts**: a flurry of Mega Steelix ECUs, whipping past crystal edges and ending on an eye ECU (11:50.13-11:51.88, ~1.75 s).
- **Execution**:
  - Wide: Steelix slams the ground and dust rises (11:52.0-11:52.63).
  - Blue crystals erupt from the dust (11:52.88-11:53.38), then a full-frame crystal close-up (11:53.38-11:53.50).
- **Trainer reaction under shake**:
  - Kiawe grits his teeth and shouts the counter (11:53.6-11:56.4).
  - Shake on 2s in bursts: about 30 px decaying to 2-3 px (11:53.68-11:54.31); about 37 px decaying again (11:54.64-11:55.31).
- **Clash**:
  - Dragon Tail's glow (11:56.5-11:57.4). Crystals swallow Turtonator (11:57.5-11:58.26).
  - **1 black/white line frame** (11:58.38), a crystal smear (11:58.51-11:58.64), then a crystal wave hits a white star burst (11:58.76-11:59.51).
- **Impact**:
  - A black frame with a tiny orange spark (11:59.64), orange blobs on black (11:59.76-12:00.01).
  - **1 white frame with black cracks** (12:00.14).
  - A cream and orange explosion holds ~1.9 s (12:00.26-12:02.14).
- **Reactions and result**:
  - Kiawe lurches forward (12:02.26) and Ash and Pikachu are shocked (12:02.89-12:03.89).
  - Grey smoke for ~1.1 s (12:04.02-12:05.14), clearing to Turtonator lying down (12:05.14-12:06.27).
  - An **ECU of swirl eyes** (12:06.39-12:07.14).
  - The loudness drops to near-silence on that reveal (12:05.5-12:06.5).

**D. Pikachu's Iron Tail on Mega Gyarados (16:53.3-16:57.4): anticipation hold + eye insert + hit reaction.**
- Pikachu runs up Gyarados' back on 2s (16:53.30-16:54.30). It jumps; the new angle has stadium lights behind (16:54.34-16:54.47).
- **Anticipation**: Pikachu hangs in the air while only the white glow on its tail animates, about 12 frames (16:54.51-16:54.97).
- **Eye insert**: 2 frames of Pikachu's eye in ECU (16:55.01-16:55.05), then 1 white frame (16:55.09).
- **Smear**: a white diamond-shaped tail smear fills the frame for 3 frames (16:55.14-16:55.22), then a somersault with a glowing trail, ~17 frames (16:55.26-16:55.93).
- **The target waits**: Gyarados' face holds ~6 frames before the hit (16:55.97-16:56.18).
- **Hit**: the tail enters on speed lines (16:56.22). Then a white blade arc (16:56.26-16:56.43) and **multiple white crescent slashes** across the face (16:56.47-16:56.59, 4 frames).
- **Hit reaction**:
  - Gyarados' head jolts back, mouth wide, for about 12 frames while Pikachu bounces off with sparks (16:56.64-16:57.10).
  - Then a hard **cut to a spectator** (Mallow) smiling (16:57.14).

**E. Gigavolt Havoc's final strike (18:28.6-18:43): see 4f for the Z-pose part.**
- Pre-launch: a 1-2 frame radial yellow flash, then a grey-shaded "negative" Pikachu (18:28.64-18:28.72).
- The spear is a huge yellow-white bolt with branching lightning on a blue speed BG, held and cycled ~2.8 s (18:28.80-18:31.56).
- An inverted frame: a white field with a black Pikachu silhouette (18:31.64).
- Travel: a dark arena with a glow approaching from far away (18:31.89-18:32.64).
- **Impact frames**: white with drifting black blobs, ~20 frames (18:32.72-18:33.56).
- The hit shot is held ~1.1 s with a slow +1 to +3 px drift, no shake (18:34.14-18:35.23). Then a whiteout of ~0.5 s (18:35.23-18:35.73).
- Aftermath:
  - Top-down crater and shock rings in the water (18:35.64-18:37.73). Fog (18:37.81-18:38.40).
  - Gyarados reverts with a pinkish flash (18:39.48-18:40.56). Swirl eyes (18:40.65-18:41.65).
  - A dark smoke dissolve (18:41.73-18:43.23).

**Impact-frame grammar across all five attacks**
- **Anticipation**: a pose held 0.5-1.2 s, often with a 2-3 frame eye ECU inside it.
- **Contact**: 1-3 abstract frames (white, solid colour, or inverted black/white line art).
- **Result**: held 1-2 s.
- **Reaction**: the trainer's face, often shaken on 2s, then spectators.
- **Abstract or speed-line backgrounds** replace the real background for commands, power-ups and the moment of a strike:
  - Kiawe's orange diagonals (8:44.2), Brock's teal lines (8:52.4), Ash's horizontal lines (14:49.5), Misty's diagonals (16:21.7-16:22.7).
  - Blue radial for both Z-Moves (11:06-11:18; 18:11.9-18:28.6), the purple "curtain" for Ash's idea (17:51.5).
  - Real backgrounds return whenever the *world* or the *result* is the subject.

### 4d. Camera
- **Shake is reserved for reactions and eruptions**:
  - Shaken: Kiawe's close-ups at 9:36.0-9:37.6 and 11:53.6-11:56.4, on 2s with decaying amplitude.
  - Locked off: the Mega Steelix reveal (10:24.0-10:25.3, zero measured camera motion; only the sparkles animate).
  - The Gigavolt Havoc hit uses a slow drift, not shake (18:34.1-18:35.3).
- **Moves with a job**:
  - Tilt from the gym emblem (with Brock's thrown shirt on it) down to Brock (10:08.0-10:08.6).
  - Push-in on Turtonator before it fires (8:46.75-8:47.9).
  - Pull-back from Gyarados' roar to full body (14:16.0-14:17.0).
  - Whip-pan close-ups across Brock's chest to the Key Stone (10:13.6-10:14.9).
- **High overhead wides re-establish geography** after every break:
  - After the title (1:49.4, 10.7 s), after the eyecatch (10:40.4).
  - At the farewell (20:13.5, 8.3 s, under the narrator).
- **Split screens with a jagged white "lightning" divider** are the episode's face-off device, used about 15 times:
  - 2:17.9, 3:50.2, 6:23.3, 7:32.9, 8:40.9 (three-way), 9:27.0, 10:11.9, 13:52.3, 14:05.0 (three-way).
  - 14:56.1, 15:46.1, 17:04.9, 17:47.2 (five-way), 18:06.2 (4.1 s).
- **Framed "trainer card" poses** for gym leaders' send-outs: Brock in an octagon frame on a star BG (8:01.3), Misty in a star frame (14:12.1).

### 4e. Shot sizes, lighting, colour, expressions
- **Shot grammar in battle**: ECU eyes before every decision or transformation.
  - Lana 4:00.4, Brock 10:13.0, Kiawe 11:04.8, Misty 15:54.0, Gyarados 14:15.2, Pikachu 18:16.2.
  - Then medium command shots on abstract BGs, wide execution shots, and close reactions.
  - Spectator cutaways come about every 10-45 s, clustered after big hits: Kiawe battle at 8:59.0, 9:43.1, 9:45.9, 10:43.4-10:58.4, 11:35.0, 11:36.9, 12:02.9.
- **Scale shots**:
  - Steelix over Kiawe (8:06.2).
  - A tiny Pikachu on Gyarados' forehead (14:53.0).
  - Pikachu as a speck in the pool (16:29.9, 2.2 s; 16:34.8).
  - Mega Gyarados filling the frame (16:32.0).
- **Lighting tells who controls the fight**:
  - Kiawe's battle and the first half of Ash's are bright and saturated.
  - Misty's Rain Dance turns the arena dark green-grey with a rain overlay (15:00.3, 6.8 s, dark sky with radial lines), and it stays dark through the Hurricane.
  - After the KO the water is bright turquoise again (18:49.3).
- **Transformation palettes collapse to one hue**:
  - Mega Steelix: white and cyan (10:17.3-10:22.7).
  - Mega Gyarados: flat orange "graphic" frames (16:01.3-16:03.1).
  - Gigavolt Havoc: over-exposed cream-yellow on everything, including Ash's face (18:17.5-18:23.8).
- **Expression shorthand**:
  - Sweat drops (Kiawe 8:08.1, 9:50.6), glasses gleam (Kukui 1:06.7), anger mark (Marowak 12:42).
  - Swirl eyes for KO (12:06.3, 18:39.5), bug eyes and chibi for comedy (12:41.0, 15:53.0).
  - Shadowed brim over the eyes before the all-in (Ash 18:10.33-18:10.58).

### 4f. Transformation and power-up sequences
| Sequence | Start → reveal | Length | Kit (in order) |
|---|---|---|---|
| Mega Steelix | Brock's shirt rip 10:06.9 → Mega reveal 10:23.9; core from Key Stone ECU 10:13.0 | 17 s overall, 10.9 s core | Shirt gag → tilt-down to the trainer → gleam on the trainer (10:10.8-10:11.2, 1 white frame) → split-screen shock (10:11.9) → black/white swoosh (10:12.75-10:12.92) → ECU closed eyes (10:13.0) → whip to the Key Stone (10:13.6-10:14.9) → stone to the face, then thrust (10:15.0-10:16.9) → white (10:16.9-10:17.1) → Mega Stone globe (10:17.3) → cyan energy pulsing with white frames every 2-4 frames (10:18.0-10:19.5) → **two streams join** (10:19.6-10:21.2) → white silhouette breaks out (10:21.2-10:22.0) → **0.7 s pure white** (10:22.07-10:22.74) → red silhouettes (10:22.8) → **2 inverted frames, black with yellow eyes** (10:23.16-10:23.24) → glowing face → coloured face (10:23.9) → wide with rainbow Mega symbol, held 1.3 s (10:24.0-10:25.3) → shocked rival (10:25.4) |
| Mega Gyarados | Misty's eyes close 15:54.0 → reveal with symbol 16:10.1 | 16 s | Shocked hero in chibi (15:53.0) → trainer ECU, eyes closed then open (15:54.0-15:55.3) → turn and smear → **1 white frame with circle lines** (15:56.13) → light rings trace the Key Stone (15:56.3-15:57.6) → winking pose (15:57.6-15:58.9) → full-body pose (15:58.9-15:59.4) → yellow electric aura (15:59.9-16:00.3) → ECU of the Mega Stone on the forehead (16:00.4-16:01.1) → flat orange radial graphic (16:01.3-16:03.1) → **two streams join** (16:03.3-16:04.6) → white (16:05.1) → **inverted spiral frame** (16:05.26) → white cocoon → silhouette (16:05.4-16:07.8) → **red-eye ECU on white** (16:07.9-16:08.4) → gold glow in the water → burst → dark Mega form rises from a splash (16:08.6-16:10.0) → rainbow symbol (16:10.1-16:11.1) → spectators shocked (16:11.3) |
| Kiawe's Z-Move (Inferno Overdrive) | Kiawe ECU 11:04.8 → impact on Steelix ~11:23.2 | 18.4 s; ~20 s to the "still standing" reveal | Trainer ECU (11:04.8) → crossed arms, the crystal glows (11:05.8) → **type symbol on a blue radial BG**, 0.75 s (11:06.05-11:06.80) → dance poses with a light streak trailing the hand (11:07.3-11:08.4) → white (11:08.55) → power radiates (11:08.7-11:09.2) → the Pokémon's shell in close-ups (11:09.3-11:10.9) → more dance, then the trainer engulfed in flame (11:11-11:13.4) → fire streaks, magenta orbs, white (11:13.5-11:15.6) → symbol again, the Pokémon powered (11:15.7-11:16.6) → trainer profile on pink speed lines (11:16.7-11:18.4) → fireball rises, tendrils fill the sky (11:18.6-11:21.1) → **giant fireball held ~1.9 s** (11:21.2-11:23.1) → orange flash → tiny distant target → explosion and debris → Mega Steelix silhouetted in the blast, low angle (11:24.5-11:25.8) |
| Ash's Z-Move (Gigavolt Havoc) | Shadowed brim 18:10.3 → impact 18:34.1 → KO 18:40.6 | 23.8 s to impact, 30.3 s to KO | Shadowed brim → grin and arms up (18:10.3-18:11.1) → crossed arms with the crystal (18:11.1-18:11.6) → **inverted bolt symbol, 1 frame** (18:11.83) → bolt symbol on blue radial (18:11.95-18:12.45) → rainbow flash, white, fist (18:12.6-18:12.8) → dance poses on blue radial (18:12.95-18:15.2) → whole body outlined in light (18:15.3-18:16.1) → **Pikachu's gold eye, then a dark determined Pikachu** (18:16.2-18:17.3) → cream-yellow Ash ECU shouting (18:17.5-18:18.2) → trainer and Pokémon glowing together (18:18.3-18:20.0) → white → **lightning pattern behind Pikachu** (18:20.2-18:21.0) → **2 inverted line-art frames** (18:21.59, 18:21.84) → Pikachu wrapped in a sphere of lightning, ~1.5 s (18:22.3-18:23.8) → **accelerating cross-cut** (18:24-18:28.1) → launch (18:28.6) |

What repeats, and why it works:
- **Both Mega Evolutions run the same shot order**:
  - Trainer ECU, token glow, two streams joining, white cocoon, silhouette, inverted or eye flash.
  - Then the colour reveal with a rainbow symbol, then someone shocked.
- **Both Z-Moves run the same order**: crossed arms, the type symbol on a blue radial, the dance, power into the Pokémon, the trainer and Pokémon glowing, the attack.
  - The OP even previews Ash's Z-pose (1:28.4-1:31.2), so the viewer knows the ritual before the climax.
- **The reveal is a still frame**: the camera is locked and the drawing held while only the sparkles move (10:24.0-10:25.3).
- **The music and sound build long, not loud-quiet-loud** (loudness relative to the median):
  - Kiawe's Z-Move climbs from about -8 dB (11:03-11:06) to +10 dB (11:21-11:25) in one continuous crescendo.
  - Gigavolt Havoc rises from about 0 dB to +5…+7 dB as the cross-cut starts (18:24-18:32).
  - Mega Steelix has a deliberate dip on the trainer's gleam (-9 dB, 10:11.0-10:11.5) before rising (+7 dB, 10:19 and 10:25).
  - After each reveal there is a sharp drop: -11 dB at 10:26.75, just before the eyecatch; -11 to -15 dB at 18:44.0, just before Ash's victory pose.
  - I can't separate music from effects, so "music" claims are limited to these loudness shapes.

---

## 5. Lessons for our 60-90 s vertical Shorts anime

Premise reminder: a powerless reincarnated Earth student survives cute-but-deadly creatures with real animal knowledge and by bonding with them. Every episode ends on an A/B choice the viewers vote on. All lessons are about craft; none borrows plot, designs or names.

**Hook and question**
1. **Line 1 = place + the "wrong" thing; the character already in it.**
   - From: the narrator states the premise over the place in 10 s (0:00-0:10), and the first interior image is a lone dopey duck on a battlefield (0:20.6-0:28.1).
   - Ours: frame 0 shows the cute creature where it should not be, with the student already there.
2. **Pose the episode's question through a character, then punch it with an ECU.**
   - From: "These are the two you'll be battling" (1:04), then a glasses gleam (1:06.7) and an ECU (1:07.0).
   - Ours: the student's own line states the danger in the first 3 s, ending on an ECU of the creature's eye.
3. **Keep two or three "almost answerable" mini-questions open**, each closed by a picture.
   - From: will Psyduck do anything (0:22 → 4:42.9); where can Pikachu stand (13:38 → 13:44-13:50); can anyone break the Hurricane (17:30 → 18:02).
   - Ours: one mini-question per 20-30 s.

**Structure**
4. **Escalate inside one episode**: a small comic exchange first, then the real fight.
   - From: the comic Battles 1-2 (~94 s, ~54 s) before the 4-minute battles 3-4.
   - Ours (90 s): a 10-15 s "small test" of the creature (a sniff, a nip) before the real danger.
5. **Teach the rule cheaply, use it expensively.**
   - From: a defensive Gyro Ball on a small Pokémon (6:20.8-6:29) becomes the counter in the big fight (8:53.2). The Kanto/Alola type error (5:49-6:06) becomes careful type maths (8:22-8:36).
   - Ours: the real animal fact the student wins with is *seen* earlier in the same episode (a tic, a smell, a sound), not just said at the end.
6. **The win comes from reframing the obstacle, not from power.**
   - From: the rival says no one has broken her Hurricane (17:30); the hero thanks her, calls that the fun part (17:35-17:38), and turns the trap into a ladder (17:43.6-18:02).
   - Ours: the creature's deadliest trait becomes the student's way out, using a real behaviour.
7. **Put a 1-2 s "does not compute" beat between the idea and its success.**
   - From: Misty puzzled (17:46.2), a five-way split (17:47.2), Rotom glitching (17:49.2), and only then the climb (17:54.4).
   - Ours: the creature tilts its head and a bystander frowns, then it works.
8. **The opponent escalates before the hero's all-in, and the act break lands on the escalation's reveal.**
   - From: Mega Steelix revealed (10:24.1), the rival shocked (10:25.4), sound drops (-11 dB, 10:26.75), eyecatch (10:28.4).
   - Ours: our A/B vote should sit on the reveal of the problem, not after the solution. Open the next episode with a high wide re-establishing shot, as at 10:40.4.
9. **The hero's biggest move fails once, and the result hides behind smoke.**
   - From: smoke holds 4.8 s, then the opponent stands scratched but grinning (11:26.4-11:31.2).
   - Ours: one "it didn't work" twist per episode, revealed after a 1-1.5 s smoke/dust hold.
10. **Make a loss land through the partner, then turn it into a goal.**
    - From: the value is planted first (7:46-7:52). After the KO there is silence (12:05.5-12:06.5) and a still beat with the fallen partner (12:36.6-12:40.5). The partner's slapstick reframes it (12:40.6-12:47), and the loss becomes a vow (19:43.6).
    - Ours: when the student fails, the creature does something in character that changes what the failure means.

**Characters and dialogue**
11. **Creatures act without words.**
    - From: anger marks, steam puffs and a bone bonk (12:40.6-12:45.3); a scratched-but-grinning face (11:31.2); a tired sweating ECU (11:43.8).
    - Ours: each creature gets two signature silent tells (one "danger", one "trust"), repeated every episode.
12. **Show the bond as a picture.**
    - From: two streams joining (10:19.6-10:21.2; 16:03.3-16:04.6), a shared glow (18:19.1-18:20.0), a cheek-to-cheek hug (18:46.8).
    - Ours: one recurring "bond image" (e.g. matching breaths, or the student mirroring the creature's posture) that the series reuses at each trust moment.
13. **Accelerating cross-cut before the finisher.**
    - From: Ash and Pikachu alternate in shots of 6→5→5→4→3→2→2→2 frames, then a matched pose (18:26.6-18:28.1).
    - Ours: student face / creature face, shortening each cut, landing on one shared frame. It's cheap to animate (held drawings) and reads well vertically.
14. **Callouts are 1-4 words; one coaching line may carry the logic.**
    - From: "Use Stone Edge!" (11:48), "Quick Attack!" (14:49.9); the posture → jump → Iron Tail coaching line (16:41.6-16:48.4).
    - Ours: one sentence per step, each followed by the picture within a second.
15. **A chorus or encyclopedia explains so the hero stays in action.**
    - From: the Dex card with an illustrated legend (14:22-14:32, 6.5 s on the illustration), type maths (8:22-8:36), the teacher's analysis (15:33-15:40).
    - Ours: a "field-notes" card with *one* sourced animal fact, drawn as an inset over the scene, 2-3 s.
16. **The rival is generous; the tease is a running bit.**
    - From: Brock corrects without mockery (5:57-6:06), dares the hero (11:02), then credits him (18:04). The Misty "tough" tease returns at the end (3:16 → 18:58-19:05).
    - Ours: whoever explains a creature's danger should respect the student, and their tease should recur across episodes.

**Animation and staging**
17. **Anticipation → contact → result → reaction, in fixed counts.**
    - From: a 0.5-1.2 s anticipation hold with a 2-3 frame eye insert (8:47.50-8:48.34 with the eye at 8:47.96-8:48.05; 16:54.51-16:55.05). Contact is 1-3 abstract frames (8:48.71-8:48.75; 9:39.13-9:39.21; 12:00.14), the result holds 1-2 s (8:48.80-8:50.51; 12:00.26-12:02.14), then the trainer's face.
    - Ours: a template we can code: hold 12-24 frames, eye flash 2-3 frames, impact 1-2 frames, hold 24-48 frames.
18. **Inverted black/white line-art frames are the cheapest "power" frame.**
    - From: the impact frames at 9:39.13-9:39.17, 11:58.38, 12:00.14, 18:21.59, 18:21.84 and 18:31.64.
    - Ours: generate them by inverting the current frame's line layer. Use 1-2 per big moment, and never in calm scenes.
19. **Shake the observer, not the attacker, on 2s with decay.**
    - From: Kiawe's reaction shots, about 93 px down to 3 px at 320 px wide, offset every 2 frames (9:36.04-9:36.58; 11:53.68-11:55.31). Reveals stay locked (10:24.0-10:25.3).
    - Ours: shake the student's close-up when the creature strikes; freeze the camera on creature reveals.
20. **Swap to abstract speed-line backgrounds for will and commands; return to the real BG for results.**
    - From: 8:44.2, 8:52.4, 14:49.5, 17:51.5; blue radial for powers (11:06-11:18; 18:11.9-18:28.6).
    - Ours: a "decision BG" (radial lines in the creature's colour) whenever the student commits to a plan.
21. **Reveal creatures part before whole, and give the scale in the same frame.**
    - From: a tiny ball in a dark void (14:12.7-14:13.6) → eye ECU (14:15.2) → face → full roar from a low angle (14:16-14:19). Steelix over a human (8:06.2), a tiny Pikachu on a huge face (14:53.0).
    - Ours: the vertical frame is ideal: eye fills the width, then tilt to the full body with the student tiny at the bottom.
22. **Split screens are our native vertical shot.**
    - From: the lightning-divided split is used about 15 times for face-offs and group shock (2:17.9 … 18:06.2; five-way at 17:47.2).
    - Ours: stack it top/bottom with a jagged divider: creature above, student below, for every stand-off and for the A/B question card.
23. **Build power-ups from a fixed kit and reuse it exactly.**
    - From: both Mega Evolutions and both Z-Moves follow the same shot order (4f), and the OP pre-teaches it (1:28.4-1:31.2).
    - Ours: a 3-4 s "bond moment" kit (ECU eyes → token glow → symbol card → shared glow → reveal held still) that recurs every episode. Repetition builds anticipation, so it isn't lazy.
24. **Use colour and weather to show who controls the scene.**
    - From: rain and dark when the opponent takes over (15:00.3 onward), bright water after the win (18:49.3), sunset → night → bright day for the ending (20:22.0 → 20:27.5 → 20:33.0).
    - Ours: the forest darkens when the creature turns deadly and brightens when trust is earned.
25. **Cut rhythm: battle ~1-2 s per real shot, talk 3-4 s, explanations 6-9 s holds.**
    - From: measured corrected medians of 1.88 s and 1.06 s in battle and 3.1 s in talk; Brock's 8.9 s explanation hold (9:58.0).
    - Ours: for 60-90 s, keep danger at 1-1.5 s per shot and the one explanation line at 3-4 s.
    - Never hold over ~4 s in a Short. This one is an inference from our channel's retention rules, not from the episode.
26. **Characters act on 3s in talk and 2s in action; let effects and camera run on 1s.**
    - From: the hold measurements in 4b (talk 31% on 3s; Pikachu's run on 2s at 16:53.3-16:54.3; the fire column on 1s at 8:48.8-8:50.5).
    - Ours: this matches `anim.on_twos(objs, 3)` for acting and 2 for action, with VFX on 1s.

**Comedy and endings**
27. **Release tension with a bystander or creature gag right after a heavy beat.**
    - From: Rotom's "never ever be deleted" right after the KO (12:19); Marowak's bonk after the quiet grief beat (12:40.6); the shirt rip inside the most serious build-up (10:06.9).
    - Ours: one 1-2 s creature gag right after each scare, before the next rise.
28. **Repetition-by-editing for comic energy.**
    - From: two poses alternating every 2-6 frames for 1.5 s, ending on a sparkle (13:24.6-13:26.1).
    - Ours: a cheap reaction loop for the student's panic or joy.
29. **End on an open question in a calm wide, then one callback gag.**
    - From: the narrator asks whether Kukui's dream will come true over a high wide and a sunset plane (20:16.9-20:30), then Jigglypuff and Team Rocket gags (20:29-20:49), then "To Be Continued".
    - Ours: the A/B question is the narrator's open question, spoken over a still split card of A and B, cut within about 0.5 s (channel rule).
    - A single callback gag may come *before* the question, never after it.
30. **Use silence as a cue.**
    - From: near-silence on the KO face (12:05.5-12:06.5) and before the victory pose (18:44.0); the crescendo over the whole Z-Move (11:03-11:25).
    - Ours: drop the music bed to near-zero for 0.5 s before the A/B line and before any twist.

---

### Uncertainties and gaps
- **Dialogue I could not verify**:
  - Whisper small and medium disagree or garble a few lines: Misty's Gyarados intro (14:08), the line at 0:36-0:41, the Mega chant at 15:51, Battle 1's ending words (4:57-5:03), and Battle 2's result.
  - Battles 1-2 were not re-transcribed with Whisper medium.
  - No clean KO is shown for Battles 1-2 in the frames I checked.
  - I paraphrased these lines and did not quote them.
- **Speaker of the Z-Move commentary line (11:39-11:48)**: the frame at 11:38.9 is Brock. Whether he or Kukui speaks it is not certain.
- **The older man at the airport (19:57.4)** is probably Samson Oak, but no dialogue names him.
- **Per-episode staff credits** are not in this file (§1).
- **False-cut rates** come from 140 boundaries in three stretches, not all 707. Other stretches (the Rotom gag 13:54-13:59, the ED) may differ.
- **The 0.5 s black at 19:07.4** may be a removed broadcast break or just a scene transition.
