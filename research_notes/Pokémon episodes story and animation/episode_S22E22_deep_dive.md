# Deep dive: Pokémon Sun & Moon Ultra Legends, S22E22 "Beauty Is Only Crystal Deep!" (story and animation)

Study notes, 30 Oct 2026. The owner supplied the episode for study only. The video, frames and transcripts stay in the
private scratchpad and are not copied here. **We copy technique, never plot, characters, designs or names.**

## 0. Method and how far to trust the numbers

- Video: 21:19, 856x480, 23.976 fps, English dub.
- Transcript: the supplied Whisper-small file has big gaps (for example nothing from 16:03 to 18:29), and its timestamps
  after ~4:45 drift into round 1-2 s steps. I re-ran faster-whisper **medium.en** with VAD (scratchpad only) and used it
  to fill the gaps. Both passes mishear names ("Elton", "Marini", "Verze crystal", "Listen Pokémon"). A name is
  corrected below only when the picture or the context proves it. Medium's VAD sometimes merges a line into a long
  segment, so a few line times are marked "~".
- Shots: `shots.json` (435 cuts). The **episode body** used for all averages leaves out the opening song (2:26-2:56),
  the logo/beach/title stretch (2:56-3:05), the eyecatch (11:57-12:10) and the ending credits (20:48-21:19):
  **397 shots in 1,196 s**. The detector missed at least one cut: shot #72 (listed at 2:56.1, 9.0 s) actually holds
  a beach shot (~2:56-2:59) and then the title card (~3:00-3:04).
- My own measurements (scratchpad scripts):
  - frame-to-frame difference at 128x72, giving how often the picture changes, weighted by screen time;
  - camera translation per frame by phase correlation at 160x90. This finds pans and tilts but **not zooms or
    push-ins**, so those are taken from frames I looked at;
  - colour (brightness V, saturation S, blue-minus-red) every 0.5 s;
  - loudness (RMS dB) per second.
- I looked at about 1,500 frames: every contact sheet; 1 fps tiles of the whole body; 6-12 fps runs for the Hariyama
  clash, Quick Attack, Bewear's rage, the clash, the Beast Ball throw, the Z-Move power-up and Meowth's rejection.
- **Identity**: the coordinator's sourced note gives SM114, Japanese title "Beauty and Nyarth!", aired 24 Mar 2019,
  screenplay Akemi Omode, storyboard Hiromasa Amano. The title card in the video confirms the English title (below).
  The staff names are from that note and not from the video.

## 1. Identity

- **Title card text**: "BEAUTY IS ONLY CRYSTAL DEEP!", in white block letters inside a pink-and-white patterned frame,
  with Ash's Z-Ring (yellow Electrium Z) drawn in the lower right. Seen in frames at 3:00, 3:02 and 3:04. The series
  logo "Pokémon the Series: Sun & Moon Ultra Legends" is at 2:52-2:55. The title is a pun on "beauty is only skin
  deep": the beautiful creature's interest goes only as deep as the crystals.
- **Main cast in this episode** (seen and/or named):
  - **Ultra Guardians**: Ash with Pikachu and Rotom Pokédex; Lillie; Mallow; Lana; Kiawe; Sophocles.
    - Their battlers: Lycanroc (named 14:34), Turtonator (named 14:34), Tsareena, Alolan Vulpix, Popplio, Togedemaru
      (named 13:28).
    - Ride Pokémon (identified by design): Ash on Garchomp (1:54-1:57, 7:04), Kiawe on Charizard (1:29-1:31,
      2:02-2:08), Mallow on Flygon (1:25), Lana on Dragonair (7:00-7:01; probably also the rider leaving the seaside house at 1:27-1:28), Lillie on Altaria (1:20-1:21, 7:00),
      Sophocles on Metang (7:07).
  - **Adults**:
    - Professor Kukui (3:41-3:56).
    - Hala, the old kahuna in yellow, with Hariyama (0:30-2:23).
    - On the base monitor: Lusamine (centre), Professor Burnet (named "Burnett?" 4:45) and a purple-haired assistant
      (Wicke by design; never named in the audio).
    - Faba (named "whatever happened to Faba?" 19:18-19:25), the inventor of the glue trap.
    - Clefable, who works the base console (5:45-5:47).
    - A swarm of Meltan (6:09-6:31). The small transcript's "Elton" at 6:10 is probably "Meltan"; uncertain.
  - **Team Rocket**: Jessie, James, Meowth, Wobbuffet, Mimikyu ("use Shadow Ball" ~14:52-15:02), Mareanie (James
    says "All right, Mareanie?" 13:55, misheard as "Marini"), Bewear, Stufful (15:57).
  - **The Ultra Beast Pheromosa**. Named at 5:21-5:25. Bug/Fighting type per the Pokédex line (5:57-6:01), whose
    category word is misheard ("Listen"/"Vellesum"; probably "Lissome", unverified). It never speaks.
- **Setting**: Alola, from night to the next evening.
  - Night: an Ultra Wormhole over the jungle, Hala's house, Kukui's house.
  - Day: the Pokémon School classroom, the Ultra Guardians' underground base and launch tunnel, Team Rocket's forest
    hideout, a jungle meadow, a rocky clearing where the trap is set.
  - Faba's lab, seen only on the monitor.
  - Golden evening: the release site, then Bewear's den at dusk.

## 2. Beat sheet, scene by scene

Shot statistics per scene are in section 4.2.

### COLD OPEN (0:00-2:26, 146 s, 11% of the episode)
| Time | Location / who | Want | Obstacle | Turn | Beat |
|---|---|---|---|---|---|
| 0:00-0:32 | Night jungle sky; Pheromosa | (unknown) arrives | none | An Ultra Wormhole tears open (0:08-0:10); a white creature descends, looking **down** at the camera (0:12-0:18); full reveal in the trees (0:20-0:23); it's gone in a white blur (0:24-0:32) | Mystery and threat, no dialogue for 50 s |
| 0:30-1:01 | Hala's lit house; Hala, Hariyama | Hala works on a Z-crystal under a lamp (inserts 0:36-0:40) | "I have a visitor." (0:50.5); a dark empty path (0:52) | Poké Ball flash (0:55.5) brings out Hariyama (0:56); diagonal split-screen face-off of Hala and Pheromosa (0:58-1:00) | Suspense; **cut away before the fight** |
| 1:01-1:31 | Kukui's house, other homes; Ash, Kukui, Rotom, the other Guardians | sleep | Rotom's alarm: "Emergency dispatch request!" (1:11.6) | Ash falls off the sofa (1:08); Kukui with his coffee mug (1:06-1:10); Sophocles crying from sleepiness (1:22-1:24); a ride montage (1:20-1:31) | Comedy plus mobilisation, intercut with the threat |
| 1:31-1:36 | Hala's yard; Hariyama vs Pheromosa | Hariyama defends | Pheromosa's speed | Palm strikes miss, then Pheromosa's counter-kick throws Hariyama (1:35.9-1:36.2) | Action burst, 9 shots in 4.8 s |
| 1:36-1:54 | Hala's yard and desk | Pheromosa wants the crystal | Hala stands in the way | It towers over him (1:38-1:41), blurs past (1:42-1:44), takes the Z-crystal from the desk (1:45-1:46) and admires it in a 6.7 s close-up (1:47-1:51) | Menace plus strange beauty; Hala asks what it plans to do with that (~1:52) |
| 1:54-2:26 | Hala's yard; the Guardians arrive | catch it | too late | "It's gone already?" (~2:01-2:05). Hala: it saw his Z-crystal and stole it (2:06-2:22), told with a **sheepish grin** (2:19-2:23) | Button: group shock on a lightning comic background (2:24-2:25), then the opening song |

**OPENING SONG** 2:26-2:56 (series logo 2:52-2:55; beach shot ~2:56-2:59). **TITLE CARD** ~3:00-3:04.

### ACT A (3:05-11:57)
| Time | Location / who | Want | Obstacle | Turn | Beat |
|---|---|---|---|---|---|
| 3:05-3:53 | School; everyone | stay awake | they were up all night | Narrator bridges the time jump (3:05-3:15). A round of tired close-ups (3:13-3:39); "we didn't even end up finding the Ultra Beast" (3:37-3:41). Kukui (seen from behind) thanks them for coming out so late (3:45-3:48), then "Ultra Guardians, let's go." (3:53-3:56) | Comedy of exhaustion; the mission returns |
| 3:53-4:35 | Stock sequence | suit up | none | The chalkboard becomes a console (3:55); transformation (3:57-4:29); elevator down (4:31-4:33) | Ritual, stock footage |
| 4:35-6:09 | Base; monitor with Lusamine, Burnet, Wicke | understand the Beast | "so fast-moving... couldn't collect any data" (4:51-4:56) | **Clues in order**: a blurred image (4:59-5:03); every victim had a Z-crystal (5:13-5:19), with a washed-out flashback (5:09-5:11); an insert of Ash's own Z-Ring (5:25-5:27); the name Pheromosa (5:21-5:25); it "might be attracted to the energy" (5:25-5:30). Kiawe: no excuse for stealing (5:33-5:37). Rotom downloads the data (5:40-6:01) | Exposition delivered as a detective chain |
| 6:09-6:33 | Base; Meltan, Clefable | help | none | Meltan carry in a **crate of Beast Balls** (6:09-6:17; checked in a full-resolution crop at 6:10) | Cute side gag that plants the capture tool |
| 6:33-7:18 | Base to sky | launch | none | "Off you go" (~6:35); stock launch through a water tunnel (6:39-7:11); flight over the jungle (7:11-7:18) | Transit |
| 7:18-7:35 | Team Rocket's hideout | relax | none | James polishes Team Rocket's Z-crystals, with a **glint** (7:23-7:25); Jessie reads (7:26-7:29); Meowth and Wobbuffet eat a pile of fruit (7:30-7:34) | Calm before the intrusion |
| 7:35-8:01 | Same | (Pheromosa: crystals) | — | **Feet only** land (7:35-7:37); it stands right behind James and Jessie, unnoticed (7:38-7:42); Meowth sees it (7:43-7:45) | Love at first sight: heart eyes (7:46-7:48), blush and sparkle background (7:57-8:00) |
| 8:01-8:20 | Same | Team Rocket keeps its crystals | Pheromosa's speed | It snatches the crystals from James, flipping him upside down (8:06-8:13), and leaves (8:17). "Give those back" (~8:14-8:19). Meowth runs after it (8:18-8:20) | Theft played as slapstick |
| 8:20-8:37 | Same | Bewear brings fruit | too late | Wobbuffet and Mimikyu react (8:21-8:24); Bewear arrives with an armful of fruit (8:25-8:36) | Plants Bewear for the climax |
| 8:37-9:36 | Meadow; Meowth, Pheromosa | Meowth wants its love | it says nothing | His monologue ("never met such a beautiful Pokémon" 8:46-8:48); he names it "Beauty" (9:03-9:06); Pheromosa shows a crystal (9:11-9:16) and he gets it: "a Z-crystal collector" (9:17-9:20). He offers to get it a pile (9:23-9:35) with a sly face (9:23; 9:32-9:34) | **The turn: Meowth switches sides** |
| 9:36-10:28 | Meadow; the Guardians, Meowth | catch the Beast | Meowth is the bait | Meowth waves alone in a meadow (9:45-9:49) and goads them: only Z-Moves can stop him (10:06-10:18). Ash raises his Z-Ring ("OK, but you asked for it" 10:18-10:20). Meowth points at it: "Check out his wrist" (10:21-10:24). Pheromosa blurs past and Ash's crystal is gone (10:23-10:27) | The heroes are robbed by a trick they walked into |
| 10:28-10:42 | Same | get it back | speed | Pikachu's Quick Attack misses every pass (10:29-10:37); "How can it be faster than Pikachu's Quick Attack?" (10:37-10:40) | Brute force fails |
| 10:42-11:57 | Same; Team Rocket arrives | Team Rocket wants Meowth and its crystals back | Meowth has defected | Meowth stands on his toes like Pheromosa: "What's with the pose on the toes?" (10:51-10:57). He disowns Team Rocket (11:13-11:25) while Jessie fumes (11:25-11:28); James warns it may be an Ultra Beast (11:29-11:32). Meowth leaves with Pheromosa (11:34-11:53) | **Act-out**: the villain has gained a guide, and everyone is left stunned (11:50-11:56) |

**EYECATCH / ACT BREAK** 11:57-12:10: "Who's that Pokémon?" silhouette on a blue pattern (11:57-12:02), a black frame
(12:03), the reveal "PHEROMOSA" on yellow (12:04-12:09).

### ACT B (12:10-20:48)
| Time | Location / who | Want | Obstacle | Turn | Beat |
|---|---|---|---|---|---|
| 12:10-12:30 | Base | a plan | "speed makes it impossible to keep up" (12:16-12:19) | Over the monitor shot: "If we can't keep up... catch it when it comes to us." (12:22-12:26). "You mean lay a trap?" (12:26). Faba: "At your service!" (12:29) | Exhausted bodies on the floor (12:10-12:22); **the strategy line** |
| 12:30-13:10 | Faba's lab on the monitor | show off the Stuck-on-You Ultra Catcher | his own glue | Decoy crystal plus a glue puddle (12:39-12:50); "it'll get its feet stuck in the glue and..." (12:46-12:50), and his own boots stick (12:51-12:53). "And as you can see, it cannot escape." (12:57-13:00) | The claim, then instant visual contradiction; deadpan group (13:06-13:10) |
| 13:10-13:38 | Rocky clearing | set the trap | — | They put in their own crystals as bait (13:14-13:17); the glue spreads (13:18-13:21); "Make sure you don't get stuck!" (13:19-13:21); Togedemaru nearly steps in (13:25-13:29); they hide (13:29-13:37) | Second glue joke (near-miss) |
| 13:38-13:58 | Bushes; Team Rocket | steal all the crystals | — | Binocular view (13:38-13:41); scheme (13:46-13:52) | Adds a third party to the trap |
| 13:58-14:29 | Clearing | Meowth wants the crystals for Beauty | the glue | He runs ahead (14:05-14:10) and sticks (14:11-14:23). "Looks like we caught a Meowth instead." (14:24-14:26) | **Third glue joke: the trap catches the wrong creature** |
| 14:29-15:13 | Clearing | beat it head-on | speed | "I say let's face it head on!" (14:30-14:32). Three Z-Move power-ups (14:39-14:43), but Pheromosa **snatches the glowing crystals off their wrists** (14:49-14:53), spin-kicks three Pokémon (14:53-14:55), and the attackers end up in a heap (14:47-14:49). Team Rocket attacks from a rock: Shadow Ball, Spike Cannon (~14:52-15:04), Wobbuffet's counter glow (15:08-15:11). All fail (15:12-15:22) | Escalation: everything they have makes it worse |
| 15:13-15:45 | Clearing; Meowth | to be rescued by Beauty | it doesn't care | Meowth struggles and calls out (15:13-15:33). Pheromosa looks down at him, then **turns its back** (15:34-15:39). Meowth's tears (15:39.5-15:42); it leaves (15:43-15:44) | **Emotional low point.** "Pheromosa was using Meowth!" (~15:46); "That's awful" (15:48) |
| 15:45-16:03 | Clearing | a next move | none left | "What's our next move?" "This is bad on multiple fronts." (15:50-15:53). Stufful appears beside Team Rocket (15:55-15:58): "So if you're here, then that means..." (16:00-16:03) | The cavalry is set up by its smallest member |

**CLIMAX** (16:03-18:32). Neither Whisper pass found intelligible dialogue between ~16:12 and ~18:28; the stretch is
music, cries and reactions.

| Time | Location / who | Want | Obstacle | Turn | Beat |
|---|---|---|---|---|---|
| 16:03-16:29 | Clearing; Bewear | protect its friends | — | Tiny in a wide shot, walking (16:03-16:06), then a backlit close-up (16:07-16:09); Team Rocket terrified (16:10-16:11). It sees Meowth crying in the glue (16:18-16:20). Near-silent audio (-45 to -55 dB at 16:19-16:21) over its **blank face** (16:20.7-16:21.6), then a shadow falls, the eyes glow pink and an aura erupts (16:21.7-16:24.4) | Cute becomes terrifying |
| 16:29-17:40 | Clearing | stop Pheromosa | its speed | Charge (16:31-16:32); diagonal split (16:33.3-16:33.7); clashes with impact frames (16:33.8-16:39.8); Bewear is unhurt and blank-faced (16:40-16:41.8); its eyes flash (16:42.0-16:42.5); **Pheromosa's first shocked face** (16:42.7). Slammed into a rock (17:01-17:03). Pheromosa circles at speed while Bewear **stands still and tracks it** (17:12-17:20); Bewear steps in, grabs it (17:24-17:31), throws it up and slams it down (17:32-17:39); stolen crystals scatter (17:38-17:39) | The clever win is stillness against speed |
| 17:40-18:00 | Same | — | — | Rotom appears to hold up Bewear's paw like a boxing referee on a star-burst background (17:39.5-17:45). Bewear pulls Meowth out of the glue, leaving a **Meowth-shaped print** (17:49-17:53), grabs Team Rocket (17:54-17:55) and dashes over the horizon (17:56-17:59). The Guardians are stunned (18:00-18:05) | Comic release |
| 18:06-18:32 | Same; Ash | catch it | — | Pheromosa dizzy, swirl eyes (18:06-18:07). Beast Ball throw (18:08-18:12), capture (18:12-18:15), a 5 s wobble (18:16-18:20), Ash's grin (18:21-18:22), team pose (18:23-18:29). Someone says it wouldn't have worked without Bewear (~18:28); Ash cries comic tears (18:30-18:31) on a gloom background with Pikachu (18:32-18:35) | Victory undercut by a gag |

**RESOLUTION** (18:36-19:21): golden evening. An Ultra Wormhole opens (18:38-18:42) and Pheromosa is released (18:46-18:48). It **looks back over its shoulder** (18:49), then flies home (18:50-18:53). The kids watch and wave (18:54-19:07). A bag of the stolen crystals is held up (19:08-19:10): "Let's split up and deliver them!" (19:12-19:14).

**TAG** (19:21-19:41): Faba, still stuck in his glue, in an 11 s shot (19:26-19:37). Someone suggests taking off his uniform (19:33-19:36); he answers "Why didn't I think of that?" (19:39-19:41).

**CODA** (19:41-20:48): Bewear's den at dusk.
- Meowth sulks (19:42-19:50); Bewear brings fruit (19:49-19:53).
- Jessie: "Stop being so ungrateful" (20:00-20:03); "Bewear picked these berries for us, so just eat." (20:04-20:08).
- Meowth eats while crying (20:15-20:20), then says "This is where I belong!" (20:24-20:26).
- A wide shot of the glowing den (20:27-20:47). The narrator closes the episode: Pheromosa returned to its world, Meowth to Team Rocket, "happily ever after, as the journey continues" (20:35-20:46).
- **"To Be Continued"** caption at 20:44-20:47.

**ENDING CREDITS** 20:48-21:18 (illustrated stills, then black). **There is no next-episode preview in this file.**

## 3. Storytelling analysis

### 3.1 The hook (first 60 s) and the central question
- **The first 50 s have no dialogue.** The image does the hooking:
  - a slow tilt from treetops to stars (one 12.3 s shot, 0:00-0:12);
  - a rip in the sky (0:08);
  - a strange white creature that descends while **looking down at us** (0:12-0:18);
  - a full reveal (0:20-0:23), then it vanishes as a blur (0:24-0:32).
- Sound is there from ~0:01, quietly (about -35 dB against a body median of -29.7 dB). It gets quieter
  inside Hala's house (-36 to -46 dB, 0:29-0:49) and jumps at "I have a visitor" (0:50.5; -23 to -28 dB from 0:50).
- **The object of desire comes before the thief reaches it.** We watch Hala carve or polish the orange crystal in
  close inserts (0:36-0:40) 70 s before it is stolen (1:45-1:46). By the time the claw lifts it, we know the object.
- **The outcome is withheld.** The face-off (0:58-1:00) cuts straight to Ash asleep (1:02). The fight only resumes
  at 1:31, after 30 s of comedy and the ride montage. The viewer waits for "what happened to Hala?".
- **Central question 1 (plot)**: what is it, and why is it taking Z-crystals?
  - Posed visually by the creature admiring the crystal (1:47-1:51) and in words at 2:06-2:22.
  - Answered in steps: all victims had crystals (5:13-5:19), it's drawn to their energy (5:25-5:30), it's a
    collector (9:17-9:20).
- **Central question 2 (challenge)**: how do you catch something faster than anything you have?
  - Posed by Burnet (4:51-4:56), the failed Quick Attack (10:37-10:40) and "impossible to keep up" (12:16-12:19).
  - Answered by "catch it when it comes to us" (12:22-12:26) and finally by Bewear's stillness (17:12-17:31).
- **Central question 3 (heart)**: is "Beauty" worth Meowth's love? The title card poses it (3:00). Meowth's own
  naming makes it personal (9:03-9:06). The answer comes when it turns its back (15:34-15:39) and in "using Meowth"
  (~15:46).

### 3.2 Set-ups and payoffs
| # | Set-up | Payoff |
|---|---|---|
| 1 | Hala's crystal shown in inserts (0:36-0:40) | Taken from the desk (1:45-1:46) |
| 2 | James polishes Team Rocket's crystals, with a glint (7:23-7:25) | Pheromosa lands 10 s later (7:35) and takes them (8:06-8:13) |
| 3 | Insert of Ash's Z-Ring right after "every person attacked had a Z-crystal" (5:13-5:27) | Meowth: "Check out his wrist" (10:21-10:24); the crystal is gone (10:23-10:27) |
| 4 | Meltan carry a crate of Beast Balls (6:09-6:17) | Ash's Beast Ball throw and capture (18:08-18:15) |
| 5 | Speed: the blur (0:24-0:32, 1:42-1:44), "couldn't collect any data" (4:51-4:56), the blurred photo (4:59-5:03) | Quick Attack outrun (10:29-10:40); finally beaten by an opponent who doesn't chase (17:12-17:31) |
| 6 | Kiawe: no excuse for stealing (5:33-5:37); it is "attracted to the energy" (5:25-5:30) | Z-Move power-ups make the crystals glow, and it snatches them mid-pose (14:39-14:53) |
| 7 | Glue joke 1: Faba sticks (12:51-13:07) | Glue joke 2: Togedemaru near-miss (13:25-13:29) → 3: Meowth caught instead (14:11-14:26) → glue print when pulled out (17:49-17:53) → tag: Faba still stuck (19:22-19:41) |
| 8 | Pheromosa's tiptoe stance, shown as feet only (7:35-7:37) | Meowth copies the pose to impress it (10:51-11:07) |
| 9 | Meowth names it "Beauty" (9:03-9:06); the title card (3:00) | Beauty turns its back (15:34-15:39); "Pheromosa was using Meowth" (~15:46) |
| 10 | Bewear's fruit pile (7:30-7:34); Bewear arrives with fruit, too late (8:25-8:36) | The coda: Bewear feeds Meowth (19:49-20:20); "Bewear picked these berries for us" (20:04-20:08) |
| 11 | Stufful appears (15:55-15:58) | "...then that means..." (16:00-16:03), and Bewear walks in (16:03) |
| 12 | The wormhole opens over the jungle at night (0:08-0:18) | A wormhole opens at golden evening to send it home (18:38-18:53): a bookend |
| 13 | Tiredness: Ash falls off the sofa (1:08) | Sleepy class round (3:13-3:39) → bodies on the base floor (12:10-12:22) |
| 14 | Crystals stolen from everyone (5:13-5:19) | Scattered round the beaten Beast (17:38-17:39); bag returned (19:08-19:14) |

Every big payoff was planted at least once in the first act. The cavalry (Bewear) is planted twice: at 8:25 and
through Stufful at 15:57. That's why its rescue reads as earned rather than random.

### 3.3 How obstacles escalate
1. It is gone before the heroes arrive (~2:01-2:05).
2. It is too fast even to record (4:51-4:56).
3. It gains an inside man who understands people (Meowth's offer, 9:23-9:35).
4. It robs the heroes in front of their eyes (10:23-10:27), and their best fast move fails (10:29-10:40).
5. It leaves with a guide who can lead it to more crystals (11:34-11:53). This is the act-out.
6. The smart plan (the trap) catches the wrong animal (14:11-14:26).
7. The full-power attack backfires: powering up the Z-Moves **feeds** it crystals (14:39-14:53). Team Rocket's attack
   also fails (14:55-15:22).
8. The stakes turn emotional: the creature abandons Meowth (15:34-15:44).
9. "What's our next move?" Nobody has one (15:50-15:53).
10. An outside force solves it, planted earlier: Bewear (16:03).

The heroes' attempts get bigger (Pokémon move → trap → everyone's Z-Moves) and each failure costs more (Ash's crystal
→ the trap → more crystals → Meowth's heart).

### 3.4 Personality and menace with no words
**Pheromosa** (never speaks):
- Aloof elegance: half-lidded eyes in almost every close-up (7:54-7:56, 8:40-8:44, 15:35-15:38) and a tiptoe stance
  (7:35-7:37).
- It moves in two speeds only: slow, graceful head turns, or an instant blur (0:24-0:32, 1:42-1:44, 10:23).
- It dodges with tiny movements while others strain (Hariyama 1:31.5-1:33.1; Pikachu 10:32.5-10:36.3).
- It treats the crystal like jewellery, holding it up to its face (1:47-1:51, 8:12-8:13).
- It is filmed from below looking down (0:12-0:18; 15:34-15:39).
- Its face changes only when it loses: shock (16:42.7, 17:31), swirl eyes (18:06-18:07). Its single "human" moment
  is the look back before leaving (18:49).

**Bewear** (never speaks; it is a running-gag character):
- A fixed blank, cute face (16:20.7-16:21.6, 16:40-16:41.8).
- All its menace comes from **lighting and effects**, not a new drawing of the face: a shadow from the top, glowing
  eyes, aura, then a low-angle silhouette against the sky (16:21.7-16:24.4).
- It is shown immovable (16:36.7-16:38.7: Pheromosa kicks it from every side; it doesn't budge).
- Its protective motive is shown in one look at the crying Meowth (16:18-16:20).

**The others**:
- Hariyama: loyalty, stepping in front of its trainer (0:56).
- Pikachu: a crouched anticipation pose (10:29.5-10:30.7) and a determined extreme close-up (10:32.3); it looks
  with sympathy at sad Ash (18:33-18:35).
- Wobbuffet and Mimikyu: reaction shots only (8:21-8:24, 10:48-10:49).
- Togedemaru: the curious toddler near the glue (13:25-13:29).
- Meltan: the helpful swarm (6:09-6:31).
- Rotom: the referee gag (17:39.5-17:45).

### 3.5 How relationships change
- **Meowth and Pheromosa**:
  1. Infatuation (7:46-8:00).
  2. One-sided courtship to a silent partner (8:46-9:35).
  3. Meowth sides with it against his own team (11:13-11:28).
  4. It uses him as bait-finder and abandons him (15:34-15:44).
  5. The truth is said aloud by a bystander (~15:46).
- **Meowth and Team Rocket**:
  1. Betrayal ("these rapscallions" 11:15-11:20).
  2. Jessie's fury (11:25-11:28), James's warning (11:29-11:32) and Team Rocket's "how weird you're acting even for you" (11:54-11:57).
  3. Forgiven without speeches: Jessie scolds him into eating (20:00-20:08).
  4. Meowth's "This is where I belong!" (20:24-20:26).
- **Meowth and Bewear**: rescue (17:49-17:55) and food (19:49-20:20). Love is shown by feeding, not words.
- **Guardians and Pheromosa**: hunters at night (1:54-2:26) → it is sent home kindly at golden hour (18:46-19:07),
  with the kids waving. The "villain" is an animal following its nature, so the ending is release, not punishment.
- **Ash's ego**: his capture is credited to Bewear (~18:28), and he cries comic tears (18:30-18:35). A small
  deflation keeps the hero humble.

### 3.6 Suspense, threat and surprise, and how the night scenes build tension
- **Night palette**: the cold open averages V mostly 0.29-0.47 with a blue cast (blue minus red +0.17), and 37-43% of
  pixels are dark (V < 0.25).
  - The only warm light is Hala's lamp-lit window (0:30-0:46).
  - The visitor is first a **dark, empty path** (0:52), and the first bright thing is the Poké Ball's white flash
    (0:55.5).
- **Scale and partial reveals**:
  - Pheromosa first appears as feet only (7:35-7:37).
  - Then it is a huge foreground shape standing behind Team Rocket, who don't notice: dramatic irony (7:38-7:42).
  - Bewear first appears as a small Stufful (15:57), then tiny in a wide shot (16:03-16:06), then a backlit
    close-up (16:07-16:09).
- **Silence before the explosion**: the audio drops to near silence (16:19-16:21) on Bewear's blank face, then
  bursts (-20 to -24 dB at 16:22-16:24) as the eyes glow.
- **Surprises**, each one a reversal of expectation:
  - the trap catches Meowth (14:11);
  - the Z-Moves feed the thief (14:49-14:53);
  - Pheromosa's attacks do nothing to Bewear (16:40);
  - the cute bear wins by standing still (17:12-17:31).
- **Act-break placement**: Act A ends on the worst turn so far: the thief leaves with a guide (11:47-11:56). The
  "Who's that Pokémon?" silhouette (11:57-12:02) keeps the threat on screen during the break.

### 3.7 Comedy patterns: set-up, reaction shot, timing
- **Claim, then instant contradiction**: Faba explains the glue will stick the Beast's feet (12:46-12:50) and his
  own boots stick within a second (12:51). He keeps presenting while stuck ("as you can see, it cannot escape",
  12:57-13:00). The **reaction shot** is a frontal line-up of deadpan kids held about 4 s (13:06-13:10).
- **Rule of three plus a tag**: Faba (12:51) → Togedemaru near-miss (13:25) → Meowth caught (14:11) → Faba still
  stuck in the last 20 s (19:22-19:41), with the punchline in two short lines (19:33-19:41).
- **Comic background swaps** say the emotion instantly:
  - sparkle burst for love (8:00);
  - pink bubbles for Meowth's romance (11:33-11:35, 11:43-11:46);
  - anger marks (11:25-11:28);
  - a purple realisation background (14:06-14:09);
  - a dark-blue vertical-line "horror" background for Team Rocket's fear (16:25-16:28, 16:47-16:52, 17:04-17:05);
  - a star-burst for victory (17:40-17:45);
  - a gloom background for Ash (18:32-18:35);
  - group-shock lightning (2:24-2:25).
- **Character tics**: Meowth tacks Pheromosa's "-mosa" onto words ("Z-moves... Omosa? ... Sounds like gibberish"
  10:06-10:14; "trapposa" 14:05-14:12).
- **Mimicry**: Meowth's tiptoe pose (10:51-11:07).
- **Undercutting**: Hala's sheepish grin while reporting a theft (2:19-2:23); Ash's tears right after victory (18:30).
- **Timing**: the gag action is fast (1-3 s). The reaction holds are longer (2-4 s). Absurd tags are held very long
  (Faba 11 s, 19:26-19:37; Meowth's love speech, listed by the detector as one 16.3 s shot, 11:12.6-11:28.9, with
  Jessie fuming behind him in the same frame).

### 3.8 How the challenge is made clever
- **The problem is stated as one physical fact**: it is faster than anything they have (4:51-4:56, 10:37-10:40,
  12:16-12:19).
- **The strategy is stated as one line**: "If we can't keep up... catch it when it comes to us." (12:22-12:26).
  **Its desire becomes the bait**: they put their own crystals inside a glue ring (13:14-13:21).
- **The turning point uses the other characters' desires**:
  - Meowth's desire (to please Beauty) springs the trap on himself (14:05-14:15);
  - the heroes' desire to hit hard (Z-Move power-ups) makes the crystals glow, so they get stolen (14:39-14:53).
- **The final solution is the strategy done right, by a different body**. Bewear does not chase. It stands in the
  middle while Pheromosa circles, tracks it by turning its head (17:12-17:20), steps into its path and grabs
  (17:24-17:31). The environment helps: a rock wall to slam into (17:01-17:03).
- **The capture needs the target stunned first** (swirl eyes, 18:06-18:07). The suspense of the wobbling ball is
  held 5 s (18:16-18:20).

### 3.9 Dialogue style
- **Exposition as a chain of short facts**, each answered by a reaction:
  - "too fast... couldn't collect any data" (4:51-4:56);
  - "Do we have any other clues?" (5:04-5:07);
  - "every single person who was attacked was a trainer with a Z-crystal" (5:13-5:17);
  - "That's just like Hala." (5:19-5:21);
  - "attracted to the energy" (5:25-5:30).
- **Kids speak in reactions and short resolves**: "It's gone already?", "That's awful", "What's our next move?",
  "We'll never let you down".
- **The narrator** is used twice: to bridge the time jump (3:05-3:15) and to close the episode as a fairy tale
  (20:35-20:46).
- **Meowth carries the wordplay**: romance clichés ("write it in my heart" 8:50-8:52; "trip the light fantastic"
  11:34-11:38), puns and the "-mosa" tic.
- **Long stretches have no dialogue at all**: the opening 50 s, and the whole climax (no intelligible lines from
  ~16:12 to ~18:28). The big moments are told by picture and music.

### 3.10 The ending and its pull to the next episode
- The plot closes completely:
  - the Beast goes home (18:46-18:53);
  - the crystals go back to their owners (19:08-19:14);
  - Team Rocket is reunited (20:24-20:26).
- The pull is **soft**:
  - the narrator's "as the journey continues" (20:41-20:46);
  - a "To Be Continued" caption over a warm wide shot (20:44-20:47).
- No cliffhanger, no preview. Episodic TV relies on the series promise. **Our Shorts can't**: the episode's last
  question must be in the video itself (see lessons 22-24).

## 4. Animation and staging

### 4.1 Scene-type averages (computed from `shots.json`, the frame differences and the camera estimate)
Body only (397 shots, 1,196 s); each shot is assigned to the scene type of its midpoint.
- "Held frames" is the mean of the per-shot `still` values.
- "Picture changes every 1/2/3/4-8/>8 frames" is weighted by screen time. A 1-frame change includes camera pans,
  effects and noise above the threshold, so it does **not** mean characters animated on ones.
- "Static camera" comes from phase correlation, which cannot detect zooms or push-ins.

| Scene type | Shots | Time | Median shot | Mean | <1 s | <2 s | >5 s | Held frames | Mean motion | Cuts/min | Static camera | Picture changes every 1/2/3/4-8/>8 frames |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Action | 116 | 185 s | **1.13 s** | 1.61 | 45% | 67% | 3% | 0.30 | 10.8 | **37.7** | 63% (22% horizontal pans) | 0.57 / 0.13 / 0.14 / 0.01 / 0.15 |
| Threat | 30 | 105 s | 2.81 s | 3.48 | 10% | 27% | 23% | 0.38 | 4.9 | 17.2 | 70% | 0.56 / 0.09 / 0.14 / 0.03 / 0.18 |
| Dialogue | 69 | 261 s | 3.25 s | 3.85 | 1% | 22% | 20% | 0.63 | 3.1 | 15.9 | **90%** | 0.35 / 0.03 / 0.22 / 0.03 / **0.37** |
| Comedy | 98 | 394 s | 3.42 s | 3.96 | 5% | 14% | 15% | 0.55 | 3.3 | 14.9 | 83% | 0.32 / 0.11 / **0.31** / 0.02 / 0.25 |
| Emotion | 31 | 148 s | **3.96 s** | 4.79 | 3% | 10% | **32%** | 0.68 | 1.8 | 12.6 | 90% | 0.30 / 0.07 / 0.29 / 0.03 / 0.30 |
| Transit (rides) | 9 | 22 s | 2.50 s | 2.46 | 33% | 33% | 11% | 0.19 | 7.5 | 24.0 | 78% | 0.68 / 0.02 / 0.26 / 0.01 / 0.03 |
| Stock (suit-up, launch) | 44 | 81 s | 1.54 s | 1.83 | 32% | 61% | 2% | 0.19 | 8.5 | 32.6 | 52% | 0.83 / 0.06 / 0.07 / 0.02 / 0.03 |
| **Whole body** | 397 | 1,196 s | **2.71 s** | 3.01 | 20% | 37% | 13% | 0.44 | 6.2 | 19.9 | 74% | 0.42 / 0.08 / 0.23 / 0.02 / 0.24 |

- Picture changes in selected sequences (every 1/2/3/4-8/>8 frames):
  - Hariyama clash (1:31.5-1:36.3): 0.47 / **0.53** / 0 / 0 / 0. Fast action on 2s, the rest is camera and effects
    on 1s.
  - Meowth's monologue (8:56-9:35): 0.11 / 0.15 / **0.45** / 0.03 / 0.26. Talking acting on 3s.
  - Meowth eating and crying in the den (20:15-20:25): 0.19 / 0.04 / 0.46 / 0 / 0.31.
  - Bewear's rage and clash (16:20-16:46): 0.73 / 0.19 / 0 / 0.02 / 0.06. Effects and camera on 1s.
  - Suit-up stock sequence: 0.89 on 1s (camera moves throughout).
- For comparison, `channels/monsters/ANIME_STUDY.md` measured the sibling episode (S22E14) at a 1.65 s median with a
  different cut detector. This body measures 2.71 s overall but 1.13 s in action. Some of the gap is method; the
  shape (fast action, slow dialogue and emotion) is the same.

### 4.2 Per-scene numbers (shots / median shot / held frames / picture changes every 1, 2, 3, 4-8 and more than 8 frames)
| Scene | Type | Shots | Median | Held | Changes every 1/2/3/4+ frames |
|---|---|---|---|---|---|
| 0:00 Pheromosa arrives | threat | 4 | 7.15 | 0.55 | 0.87/0.05/0.05/0.03 |
| 0:30 Hala's visitor | threat | 9 | 3.00 | 0.37 | 0.85/0.05/0.08/0.02 |
| 1:01 Guardians woken | comedy | 5 | 2.96 | 0.51 | 0.89/0.05/0.02/0.03 |
| 1:31.5 Hariyama clash | action | 9 | **0.33** | 0.36 | 0.64/0.36/0/0 |
| 1:36 Crystal taken | threat | 5 | 2.84 | 0.60 | 0.61/0.06/0.29/0.04 |
| 1:54 Hala explains | dialogue | 11 | 2.38 | 0.53 | 0.63/0.08/0.27/0.02 |
| 3:05 Sleepy class | comedy | 11 | 3.50 | 0.29 | 0.93/0.02/0.05/0.01 |
| 4:35 Briefing | dialogue | 25 | 3.42 | 0.71 | 0.81/0.03/0.10/0.07 |
| 7:35 Meowth falls in love | comedy | 10 | 2.60 | 0.50 | 0.78/0.07/0.12/0.03 |
| 8:01 Team Rocket robbed | action | 12 | 1.92 | 0.31 | 0.77/0.07/0.12/0.03 |
| 8:37 Meowth woos | comedy | 11 | **4.96** | 0.70 | 0.30/0.18/**0.47**/0.06 |
| 9:45 Bait, Ash robbed | dialogue | 12 | 2.88 | 0.34 | 0.90/0.02/0.07/0.01 |
| 10:28 Quick Attack | action | 7 | 2.04 | 0.24 | 0.84/0.09/0.07/0 |
| 10:42 Meowth leaves | comedy | 18 | 3.34 | 0.58 | 0.52/0.10/0.35/0.03 |
| 12:30 Faba's demo | comedy | 8 | 4.36 | 0.65 | 0.66/0.10/0.20/0.04 |
| 13:58 Meowth trapped | comedy | 11 | 2.50 | 0.64 | 0.48/0.20/0.27/0.05 |
| 14:29 Team battle | action | 26 | 1.19 | 0.35 | 0.84/0.06/0.09/0.02 |
| 15:13 Meowth abandoned | emotion | 8 | 3.73 | 0.63 | 0.47/0.24/0.26/0.03 |
| 16:03 Bewear arrives | threat | 12 | 2.31 | 0.25 | 0.88/0.11/0/0.01 |
| 16:29 Bewear vs Pheromosa | action | 48 | **1.06** | 0.25 | 0.85/0.11/0.03/0.01 |
| 18:00 Capture | action | 14 | 1.73 | 0.35 | 0.82/0.04/0.11/0.02 |
| 18:32 Farewell | emotion | 9 | 4.38 | 0.71 | 0.74/0.04/0.18/0.04 |
| 19:21 Faba tag | comedy | 4 | 4.06 | 0.61 | 0.42/0.37/0.20/0.02 |
| 19:41 Den coda | emotion | 14 | 3.92 | 0.69 | 0.71/0.03/0.22/0.04 |

(In this table the change intervals are counted per interval, not weighted by time.)

### 4.3 Shot sizes and cutting rhythm by scene type
- **Dialogue** (briefing, 4:35-6:09):
  - A wide of the base re-establishes every 6-8 shots (4:41-4:47, 5:13-5:15, 6:33).
  - The monitor acts as a frame within the frame (4:37 onward).
  - Close-ups go on the speaker: Burnet (4:55-4:57), Lusamine (5:07), Kiawe (5:33-5:35).
  - Two- and three-shots give listeners' reactions (5:05, 5:17-5:19, 5:29-5:31).
  - Inserts show exactly what is being talked about: the blurred image (4:59-5:03), the Z-Ring (5:25-5:27), Rotom's
    screen (5:51-5:59).
  - The cameras are 90% static and 37% of screen time is in holds longer than 8 frames.
- **Comedy**:
  - Frontal medium shots held 3-5 s, with extreme close-ups for the face gag (heart eyes 7:46-7:48).
  - Cutaways to the straight man (Jessie's sweat drop 8:01-8:02).
  - A deadpan group line-up after each gag (13:06-13:10, 14:24-14:27).
  - Mouth and arm acting on 3s.
- **Action**:
  - Cuts are 0.2-1.0 s.
  - Shot types: extreme close-ups of limbs and faces, smears, full-figure profiles over speed lines.
  - About every 5-10 action shots, one reaction shot of the onlookers (17:21-17:23; 14:49-14:51; 18:00-18:05).
  - Example: Hariyama clash, 9 shots in 4.8 s with a 0.33 s median (1:31.5-1:36.3).
- **Emotion**:
  - Close-ups held 4-6 s (Pheromosa's turn-away, a 5.5 s tilt, 15:34-15:39; Meowth's tears 15:39.5-15:42).
  - Wides held for a long time (the den at 20:27-20:47 is two shots, 12.0 s and 8.9 s).
  - Almost no camera movement; 32% of shots are over 5 s.
- **Threat**:
  - Low angles and huge foreground shapes (0:12-0:18; 7:38-7:42).
  - An over-the-shoulder shot from behind the threat toward its target (16:13-16:14).
  - Wide-to-close reveals (16:03-16:09).
  - Long single shots in the night opening (median 7.15 s).

### 4.4 Camera moves
- 74% of body shots are static; 13% horizontal pans; 11% vertical pans or tilts.
- Moves cluster in action (22% horizontal) and the stock sequences (48% moving).
- Notable moves:
  - the 12.3 s tilt from treetops to the sky that opens the episode (0:00-0:12);
  - a tracking pan with Pikachu's Quick Attack over a blurred lawn (10:31.2-10:32.2);
  - a tilt holding on Pheromosa as it looks down at Meowth, then turns away (15:34-15:39);
  - a 10.7 s tilt up the evening trees to the wormhole (18:32-18:42).
- **Push-ins** (seen in frames, not measured): Bewear's face grows to an extreme close-up (16:40.0-16:41.8); Meowth's
  heart eyes go from close-up to extreme close-up (7:46-7:48).
- **Shakes**: only around impacts (14:35, 16:31.7, 16:35.5, 16:44.7). The camera mostly stays still and lets the
  drawing and effects move.

### 4.5 Holds and on-2s/3s timing
- **Dialogue and emotion live on holds**: 30-37% of their screen time is in holds longer than 8 frames.
  - The base wide at 4:40 is a 9 s shot with 96% held frames.
  - The monitor shot at 12:22.6 is 12.1 s with 88% held frames.
- **Talking and comic acting on 3s**:
  - Meowth's courtship (8:56-9:35) has 45% of its time in 3-frame steps;
  - Meowth's crying while eating (20:15-20:25) has 46%.
- **Fast action on 2s**: the Hariyama clash has 53% of its time in 2-frame steps. The camera, speed lines and effects
  run on 1s around it.
- **Long holds for absurdity**: Faba stuck (11 s, 19:26-19:37); Meowth's love speech (detector: one 16.3 s shot, 11:12.6-11:28.9).
- **Freeze the character, move the effect**:
  - Bewear stands still while the afterimage of Pheromosa circles it (17:12-17:20);
  - Bewear's face stays still while light and aura change it (16:20.7-16:24.4).

### 4.6 How a move is staged, step by step
- **Pikachu's Quick Attack** (10:28.5-10:37.3):
  1. Ash's angry close-up (10:28.5);
  2. the command pose, pointing (10:29.0);
  3. **anticipation**: Pikachu crouches low for ~1.2 s (10:29.5-10:30.7);
  4. launch with a lightning trail (10:30.8) and a white flash streak (10:31.0);
  5. a tracking streak across the grass (10:31.2-10:32.2);
  6. a 1-2 frame extreme close-up of Pikachu's determined face (10:32.3);
  7. the **effect**: repeated passes as a glowing blur while Pheromosa sidesteps each with minimal motion
     (10:32.5-10:36.3);
  8. **impact replaced by a miss**: Pikachu skids to a stop in dust (10:36.5-10:37.0);
  9. the **reaction shot**: Kiawe and Ash grit their teeth (10:37.2).
- **The Beast Ball throw** (18:07.8-18:22):
  1. Pheromosa's swirl eyes (18:06-18:07);
  2. an **insert** of the hand pressing the ball, which enlarges (18:08.0-18:09.3);
  3. a medium shot of the wind-up (18:09.5-18:11.0), with a smear frame of the ball (18:10.1);
  4. a full-body throw with the ball huge in the foreground (18:11.1-18:12.0);
  5. a frame-filling smear (18:12.1);
  6. the hit (18:12.3);
  7. a red-blue energy blob that shrinks into the ball (18:13.3-18:14.8);
  8. empty ground (18:15.0-18:15.6), then a 5 s wobble hold (18:16-18:20);
  9. the relief face (18:21) and the team pose (18:23).
- **Bewear's rage-up** (16:18-16:24.4):
  1. the motive (it sees Meowth crying, 16:18-16:20);
  2. near silence plus its blank extreme close-up (16:20.7-16:21.6);
  3. a shadow drops over the face (16:21.7-16:21.8);
  4. the eyes reshape into glowing pink ovals (16:21.9-16:22.5);
  5. lens flares on the eyes (16:22.6-16:22.9);
  6. a red, blue and black aura swirls over a dark body as the camera rises (16:23.0-16:23.9);
  7. a low-angle silhouette against the sky with glowing eyes (16:24.0-16:24.4);
  8. **the reaction**: Team Rocket's terrified grins on the horror background (16:25-16:28).
- **The Hariyama clash** (1:31.5-1:36.3):
  1. Pheromosa poised on a radial speed-line tunnel; Hariyama's palms smear in from the frame edges (1:31.7, 1:32.1,
     1:32.3, 1:32.6);
  2. close-ups of palm strikes and parries with yellow spark bursts (1:33.2-1:34.9);
  3. a profile two-shot on horizontal speed lines (1:35.0-1:35.9);
  4. the counter-kick lands with sparks and Hariyama is flung out of frame (1:36.0-1:36.2);
  5. the reaction cut to Hala, with Hariyama falling behind him (1:36.3-1:37).
- **The full-team attack** (14:33-14:55):
  1. Poké Ball throws (14:33-14:35);
  2. Pokémon appear (14:36-14:38);
  3. a three-trainer Z-power pose (14:39-14:43) with the three crystal symbols (14:43.3);
  4. a **three-panel vertical split** of three Pokémon (14:44-14:44.7);
  5. a second line-up (14:45-14:46), then an overhead charge (14:46-14:47);
  6. the attackers end up in a heap (14:47-14:49);
  7. the wind streak passes the kids (14:49-14:51), who look at their bare wrists (14:51.5);
  8. **the reveal**: Pheromosa holding their red and blue crystals (14:52-14:53).

### 4.7 Effects inventory (each one is cheap in 2D)
- **Speed-line backgrounds**: radial tunnel (1:31.5-1:33.1; 16:33.8-16:34.7), horizontal streaks (1:35-1:36;
  17:27-17:28).
- **Smears**: Hariyama's palms (1:31.7 etc.); the ball (18:10.1, 18:12.1).
- **Impact frames**: 1-2 frame grey blanks (16:34.8, 16:36.0); inverted olive-and-black flashes for about a second
  (16:38.8-16:39.8); a yellow X flash (16:42.2-16:42.5); spark bursts (1:33-1:36, 16:37-16:38).
- **White flashes**: the Poké Ball (0:55.5); Pikachu's launch (10:31.0).
- **Glows and auras**: eye glow and aura (16:22-16:24, 16:53-16:55); Z-crystal glow during the power-up
  (14:40-14:43); the wormhole burst with rainbow edges (0:08-0:10; 18:41-18:42, 18:52-18:53).
- **Afterimages**: Pheromosa circling Bewear (17:12-17:20).
- **Comic backgrounds** listed in 3.7, plus heart eyes (7:47-7:48), blush lines (7:57-8:00), a sweat drop (8:01),
  tear streams (15:40-15:42; 18:30-18:31), swirl eyes (18:06-18:07), sparkles in sly eyes (9:56-9:58).
- **Diagonal split screens** for face-offs: Hala vs Pheromosa (0:58-1:00), Pheromosa vs Meowth (8:56-9:00), Bewear
  vs Pheromosa (16:33.3-16:33.7). Also a three-panel vertical split (14:44).
- **Point-of-view masks**: binocular POV (13:38-13:41). **Screens**: the hologram-glow monitor frame (4:37 onward).
- **Flashback treatment**: washed-out white (5:09-5:11).
- **Dust and debris**: Pheromosa's kick (8:09); Bewear's exit (17:56-17:59); a glue print with strands (17:49-17:53).

### 4.8 Colour and lighting for mood
Measured every 0.5 s; values are means per scene.
- **Night**: cold open V mostly 0.29-0.47 (0.57 in the crystal close-ups, where the white creature fills the frame), saturation up to 0.68 (the deep night blues), blue minus red +0.17, 37-43% dark
  pixels. Warm, low-key lamplight only inside Hala's house (0:30-0:46).
- **Day comedy and dialogue**: V 0.62-0.78, saturation mostly 0.26-0.42 (pale interiors and lab).
- **Danger in daylight**: done by local lighting on the character, not by grading the whole frame. Bewear's face
  darkens from the top, its eyes glow and the aura is saturated red-blue (16:21.7-16:24.4); the scene's average stays
  V 0.67.
- **Resolution**: golden evening, blue minus red **-0.20**, saturation 0.48 (18:32-19:21).
- **Coda**: a dark frame with a glowing warm centre: V 0.40, saturation 0.69, blue minus red **-0.25**, 35% dark
  pixels (19:41-20:48). The final den shot frames a firelit hollow with near-black foliage around it (20:27-20:47).
- **The colour script runs cold night threat → bright day → warm dusk safety.**

### 4.9 Expressions and acting
- **Meowth carries the acting range**:
  - heart eyes with an open, drooling mouth (7:47-7:48);
  - blushing, starry-eyed offering (7:57-8:00);
  - sly half-lidded eyes with sparkles (9:56-9:58; 9:32-9:34);
  - a proud tiptoe pose with closed eyes (10:59-11:07);
  - pleading, then crying with tear streams and a wobbling mouth (15:30-15:42);
  - a sulking hunch (19:45-19:50);
  - crying while chewing (20:15-20:20).
- **Tired faces, a different "tired design" for each character**: dark eye bags (Mallow 3:27-3:29), forehead creases
  (Lana 3:31-3:33), drool and sleep (Sophocles 3:35), heavy-lidded slouch (Kiawe 3:37-3:39).
- **The others**:
  - Hala's sheepish closed-eye grin with a sweat drop (2:19-2:23);
  - Ash's gritted teeth (10:28) and comic waterfall tears (18:30);
  - Jessie's anger marks with clenched teeth (11:25-11:28).
- **The creatures act with eyelids and posture only**: Pheromosa's half-lids and tiptoes (7:54-7:56; 7:35-7:37);
  Bewear's unchanging face (16:40-16:41.8).

### 4.10 Transitions
- Almost all transitions are **hard cuts**, including the big tonal jump from the Hala face-off to Ash asleep
  (1:00 → 1:02).
- Time jumps are bridged by a narrator over an establishing exterior (3:05-3:15).
- Ritual stock sequences double as transitions between places (suit-up 3:53-4:35; launch 6:39-7:18).
- The act break is a bumper: silhouette → black frame (12:03) → reveal.
- Other devices: a white flash (0:55.5); a washed-out flashback (5:09-5:11); the "To Be Continued" caption over the
  final wide (20:44-20:47).
- I did not see any shape wipes in the frames I viewed (unlike the sibling episode noted in ANIME_STUDY.md). I didn't
  check every frame for this.

## 5. Transferable lessons for our original 60-90 s vertical series

Our series: a reincarnated Earth student survives in a cute-but-deadly creature world by real animal knowledge; every
episode ends on an A/B choice viewers vote on in the comments. Technique only; nothing from this episode's plot,
characters or designs.

1. **Open on the creature, not the hero, and make it look down at the viewer.** 0:08-0:18: a rip in the sky, then a
   strange body descending, eyes lowered at the camera. For Shorts, compress the 32 s night opening into 2-3 s: frame
   0 is the creature's eye or limb, already wrong.
2. **Show the coveted object in close inserts before anyone takes it.** 0:36-0:40 → 1:45-1:46. Show the student's
   food, tool or shelter in an insert one beat before the creature goes for it.
3. **Cut away at the peak of a face-off and come back later.** 0:58-1:00 → 1:02 → 1:31. In 60-90 s, a 2-3 s cutaway
   (the student's reaction, or a second creature) at the peak is enough to make the return land.
4. **Give every silent creature one signature pose and one signature eye shape.** Pheromosa's tiptoes and half-lids
   (7:35-7:37, 7:54-7:56); Bewear's blank face (16:20.7-16:21.6). Write these into each creature's model sheet.
5. **Turn cute into deadly with lighting, not a redraw.** 16:20.7-16:24.4: a shadow from the top, glowing eyes, aura,
   a low-angle silhouette. This is the core visual trick for "cute-but-deadly"; it reuses the same puppet.
6. **Put silence right before the explosion.** The audio drops to -45/-55 dB at 16:19-16:21, then bursts at
   16:22-16:24. Cut the music for about a second before a creature's reveal or attack.
7. **Reveal danger by scale in three steps**: small sign → tiny figure in a wide shot → close-up. Stufful (15:57) →
   Bewear far off (16:03-16:06) → backlit close-up (16:07-16:09). Footprints → silhouette on the ridge → face fills
   the frame.
8. **Partial reveal plus dramatic irony.** Feet only (7:35-7:37), then the creature standing behind characters who
   don't notice (7:38-7:42). Vertical frames suit this: the creature looms in the top half, the oblivious student in
   the bottom.
9. **State the problem as one physical fact, then the strategy as one line.** "Impossible to keep up" (12:16-12:19)
   → "catch it when it comes to us" (12:22-12:26). Our student's animal-knowledge line must work the same way: one
   true fact, one plan.
10. **Show brute force failing before the clever solution.** Quick Attack misses (10:29-10:40); the full-team charge
    collides (14:47-14:49). One failed obvious attempt (run, hit, hide) before the knowledge-based fix makes the fix
    feel smart.
11. **Make the obvious move backfire because of the creature's nature.** Powering up the crystals feeds the thief
    (14:39-14:53). Every creature's danger should come from a real behaviour that punishes the naive move.
12. **Win with stillness or timing against speed.** Bewear tracks, waits and steps in (17:12-17:31). Many real
    predator and prey tactics are about timing and position, not strength; build climaxes on that.
13. **Plant every payoff at least once in the first third.** Beast Balls (6:09-6:17 → 18:08); Ash's Z-Ring insert
    (5:25-5:27 → 10:23-10:27); Bewear twice (8:25; 15:57 → 16:03). In 60-90 s, plant the solving fact visually in the
    first 15-20 s.
14. **Run a gag three times and tag it in the last seconds.** Glue: Faba (12:51) → Togedemaru (13:25) → Meowth
    (14:11) → Faba again (19:22-19:41). Across episodes, give the series one recurring hazard gag and pay it off as
    a tag.
15. **Put a reaction shot after every beat, held 2-4 s.** 13:06-13:10, 14:24-14:27, 17:21-17:23, 18:00-18:05. The
    student's reaction (or a sidekick creature's) after each reveal is where viewers feel it.
16. **Cut fast for action, slow for dialogue and emotion.** Action has a 1.13 s median shot (45% under 1 s); dialogue
    3.25 s; emotion 3.96 s (32% over 5 s). For Shorts: action bursts of 0.3-1 s shots, then a 2-4 s reaction or
    feeling hold.
17. **Spend drawings where they show.** Fast action on 2s (Hariyama clash 53% on 2s), talking on 3s (Meowth 45% on
    3s), holds for listening (dialogue 37% of time held more than 8 frames), camera and effects on 1s. Our puppet
    rigs can step character poses on 2s/3s while effects run every frame.
18. **Stage every move in the same five steps**: command or decision → anticipation crouch → launch flash and streak
    → 1-2 frame extreme close-up of determination → result → reaction. Quick Attack (10:28.5-10:37.3) and the Beast
    Ball throw (18:07.8-18:22) follow this exactly.
19. **Impact frames are 1-2 drawings of nothing.** Grey blanks (16:34.8, 16:36.0) and inverted flashes
    (16:38.8-16:39.8) cost almost nothing and sell the hit.
20. **Use the diagonal split screen for face-offs.** 0:58-1:00, 8:56-9:00, 16:33.3-16:33.7; a three-panel split for a
    line-up (14:44). In 9:16, split top and bottom on a diagonal: student above, creature below.
21. **Use comic background swaps to tell the emotion in one frame.** Sparkles for love (8:00); purple for realisation
    (14:06-14:09); a dark vertical-line background for dread (16:25-16:28); a star-burst for victory (17:40-17:45);
    gloom (18:32-18:35). Build a small set of 4-6 emotion backgrounds once and reuse them.
22. **Plan a colour script: cold blue for danger, warm gold for safety.** Night V 0.29-0.47 with a blue cast; coda
    with a warm cast (blue minus red -0.25) in a dark frame. Grade the A/B question moment cold or warm depending on
    which choice we want to feel risky.
23. **Give each episode one small emotional beat beside the plot.** Meowth's love → rejection (15:34-15:42) → found
    family (20:24-20:26). One sidekick feeling per episode keeps the survival plot from being only mechanics.
24. **End on the decision, not a soft close.** This episode closes softly ("as the journey continues" 20:41-20:46;
    "To Be Continued" 20:44-20:47; no preview). That works for TV and fails for Shorts. Take the episode's real
    decision point, chase or ambush (10:28 vs 12:22-12:26), and make it our ending A/B. Both options must be backed by
    a real animal fact.
25. **Put a mystery card at the halfway point.** The silhouette card (11:57-12:02) → reveal (12:04-12:09). At ~45 s, a
    1-2 s silhouette of the next creature with our own design (no logo) holds viewers through the middle.
26. **Treat the dangerous creature as an animal, not a villain.** It is sent home at golden hour and looks back
    (18:46-18:53). The student respects animals; outcomes can be escape, release or truce, which also helps rotate
    outcomes between episodes.
27. **Undercut the win with one quick gag.** Ash's catch is credited to Bewear, followed by comic tears (~18:28-18:35).
    A 1-2 s humbling beat after the student wins keeps the hero likeable and gives a callback hook.
28. **Use no dialogue at the biggest moments.** 0:00-0:50 and ~16:12-18:28 have no lines. Let the climax play on
    picture, sound effects and one music sting, with captions only for the one key fact.

### What not to copy
- The Ultra Beast and its crystal-collector motive.
- The glue trap.
- The love-struck sidekick who defects.
- The bear rescuer.
- Any Pokémon designs, names, logos, the "Who's that Pokémon?" card or the stock sequences.

We take the **devices** (inserts before a theft, scale reveals, lighting-based menace, rule of three, split screens,
reaction holds, colour script) and build them on our own creatures and our own animal facts.
