# WW2 Episode 1: shot list (helper 4, 31 Oct 2026)

This shot list covers `channels/ww2/ep01_script.md` (after the fact-check, 5bf6d0a) in the **animated 1940s poster** look of `channels/ww2/STYLE.md` and `style_reference.png`.
- **Size:** 133 narration entries (131 numbered lines plus 109b and 123b), broken into **165 shots**.
- **Shot IDs:** `C<chapter>-S<nn>`, where C0 is the cold open.

## Length
- **Estimated running time: 12:33 (754 s).**
  - This is computed per line as words / 150 wpm, plus 0.45 s per sentence pause, plus 0.15 s, with 2 s of held silence after the Holocaust candle.
  - The script is ~1,660 words, so it runs **longer than the 10 minutes in the brief**. At a brisker 165 wpm it is about 11:30.
  - Real timing comes from the voice takes. Re-time every shot from the final timing.json, as on the monsters channel.
- **Average shot:** 4.6 s.
  - The 1-2 s visual-change rule is met *inside* shots. Every shot over 2.5 s carries a beat at least every 2 s: an arrow growing, a stamp, a counter tick, a pose change, a label, a date flip or the push-in reframing. The beats are named in the composition column.

## Rules for every shot
- **Finish:** `push_in` on every shot, `date_stamp` in the corner (the DATE column) and `print_finish` last.
- **Background:** paper plus 3-4 inks.
- **Rays:**
  - ink, gold, blue or khaki only;
  - **never red rays from a red or white disc** (STYLE.md);
  - **no rays at all in the Holocaust chapter.**
- **Content limits:**
  - no Nazi or Imperial Japanese symbols;
  - no visible deaths;
  - the Holocaust chapter has no figures at all.
- **Sound:** cues are the effect layer only. Music beds and the narration come from the mix.
- **Transitions:**
  - hard cuts inside a chapter;
  - a poster wipe into each chapter card;
  - a slow fade in and out of chapter 5 only.

## Reusable set-pieces
Build each set-piece once, as a module with parameters, then reuse it across shots.

| Set-piece | What it is | Shots | Used in packages |
|---|---|---|---|
| **MAP eu** | Europe map (maps.py `Map("europe")`): regions 1936-45, arrows, fronts, secret line, stamps, city dots. Style frame map_1939 exists. | 32 | P2, P3, P4, P5, P6, P7 |
| **MAP pac** | Pacific / East Asia map (`Map("pacific")`): Manchukuo, occupied China, island-hop arrows, Midway pin, Burma arrow. | 8 | P2, P5, P7, P8 |
| **MAP world** | World map (`Map("world")`, Equal Earth): flood fills, globe spin to the Pacific, the Atlantic inset, Commonwealth outlines, the blue/red Cold War split. | 8 | P1, P2, P4, P5, P8 |
| **MAP africa** | The south edge of the Europe view, extended to Ethiopia (or a world crop). One shot. | 1 | P2 |
| **RAYS** | Poster card on rays (`rays`, `chapter_card`, `word_card`): 8 chapter cards, word cards, date posters, the title, the end cards. Style reference exists. | 19 | P1, P2, P3, P4, P5, P6, P7, P8 |
| **LEADER** | Leader portraits on rays (stick.py `Figure(leader=...)`): Hitler, Stalin, Churchill, Roosevelt, Mussolini, Hirohito, Chamberlain (+ Daladier, Chiang as one-shot extras). Poses: speech, point, handshake, shake head, wave paper, slam. | 14 | P1, P2, P3, P4, P5, P6, P8 |
| **COUNTER** | Big Anton number on plain or dark paper (`counter`): 60-85M, 2,403, 338,226, 6,000,000, 200,000, 27M, 15M. | 7 | P1, P4, P5, P8 |
| **SIGN** | Signing table / courtroom rig: Versailles, Munich, Reims, the Missouri deck, the UN round table, Nuremberg and Tokyo. | 7 | P1, P2, P7, P8 |
| **SKY** | Sky layer with aircraft (`props`: bomber, fighter, dive bomber), searchlights, flash and cloud silhouettes. | 7 | P4, P5, P7, P8 |
| **OCEAN** | Sea surface with ships (battleship, carrier, ship, periscope, submarine), flat smoke and bursts. | 7 | P4, P5, P6, P7, P8 |
| **CHANNEL** | The English Channel side view: the Dunkirk flotilla, the D-Day fleet. Shares its sea with OCEAN. | 3 | P3, P6 |
| **HOLO** | The Holocaust chapter: muted Europe map, black text cards, rail lines, the candle. No figures, no rays, no colour. | 6 | P6 |
| **DANZIG** | Night harbour: the battleship, the Westerplatte wall, Polish guards. Opens the film and returns at line 33. | 5 | P1, P2 |
| **STEPPE** | Eastern front landscape: mud, snow, columns, the Kursk tank plain. | 5 | P4, P6 |
| **CROWD** | Crowd silhouettes: humiliated 1919 crowd, the jobless queue, V-E Day cheering (London and Moscow). | 4 | P1, P7 |
| **PODIUM** | Rally podium + Reichstag silhouette + padlock. | 4 | P1 |
| **TRENCH** | Trench / soldier close-ups: 1918 German soldier, the yawning Phoney War soldiers. | 3 | P1, P3 |
| **BEACH** | Beach: Dunkirk lines, Omaha dash and sunset. | 3 | P3, P7 |
| **ROOM** | Interior: Station HYPO, Bletchley hut (Enigma, bombe), the Japanese family radio. | 3 | P5, P6, P8 |
| **CITYRUIN** | Ruined city: Stalingrad skyline and cross-section, the Berlin bunker door. | 3 | P5, P7 |
| **CITY** | Night city / Paris: London searchlights, Paris liberation crowd. | 2 | P4, P7 |
| **PLANE** | Chamberlain at the airliner door; the crumpled paper. | 2 | P2 |
| **CARRIAGE** | The Compiègne carriage in the forest, 1918 sepia and 1940. | 2 | P3 |
| **SNOW** | Stalingrad surrender: white flag, the line of prisoners. | 2 | P5 |
| **ISLAND** | Iwo Jima / Okinawa island silhouette and the generals' map table. | 2 | P7 |
| **CHART** | 1929 stock chart. | 1 | P1 |
| **PARADE** | Rearmament: multiplying ranks. | 1 | P2 |
| **FIELD** | Poland 1939 tank and dive bomber. | 1 | P2 |
| **FOREST** | Ardennes trees with the tank column. | 1 | P3 |
| **COAST** | Radar towers on the cliffs. | 1 | P4 |
| **DESERT** | El Alamein desert. | 1 | P5 |

## Shared assets (needed before the packages start)
These go into `channels/ww2/kit/` once and are used by every package:
1. **core.py:** the paper, `print_finish`, `rays`, `halftone`, `push_in`, `shake`, `date_stamp`, `chapter_card`, `word_card`, `counter`, `text`. This exists already.
2. **maps.py:** all three views, with:
   - region floods;
   - arrows, fronts and the secret line;
   - stamps and city dots;
   - camera keys.

   This exists. It still needs these regions:
   - Rhineland, Austria, Sudetenland, rest of Czechoslovakia;
   - Denmark, Norway, the Baltics;
   - Italy's south;
   - Normandy beaches, Berlin, Stalingrad zoom;
   - Midway, Burma, Manchuria arrows;
   - the Maginot line;
   - the Gustav line.
3. **stick.py, poster figures:**
   - all nations and their headgear;
   - the 7 leaders, plus Daladier, Chiang and a Turing-like civilian;
   - civilians and crowds;
   - poses: speech, point, handshake, shrug, shake head, wave paper, slam, shiver, yawn, run, march, crouch, salute, cheer.

   This needs the poster restyle from STYLE.md.
4. **props.py (to write):**
   - Weapons and vehicles: tank, fighter, bomber, dive bomber, battleship (and turret), carrier, destroyer, ferry, small boats, submarine and periscope, truck.
   - Structures and scenery: radar tower, searchlight, fort wall, railway carriage, airliner door, podium, parliament, padlock, ruined skyline and cross-section, bunker door, courtroom and signing table, skyline silhouettes, trees, island.
   - Small props: clock, calendar, telegram, newspaper, Enigma, bombe, radio, microphone, candle, white flag, parachute icons, chart, coins, die, pedestal.
5. **fx (to write):** flat star-burst explosions, halftone smoke puffs, the white flash, snow, mud, radar rings, fireworks, the mushroom-cloud *silhouette* (distant, not graphic).
6. **Sound:** a shared SFX folder for the cues below, plus three music beds (tension, march, elegy) and a single low tone for chapter 5.

**Order:**
1. Shared assets: core and maps first, then props, fx and figures, in parallel by 3 helpers.
2. The owner OKs one still per set-piece.
3. The 8 packages animate in parallel.

## Work packages (8, contiguous, ~90-100 s each)
Each package is a contiguous run of lines, so it renders as one clip that the assembler butts against the next. Package boundaries fall between lines.

| Pkg | Shots | Script lines | Screen time | Main set-pieces |
|---|---|---|---|---|
| **P1** | C0-S01 - C1-S13 (22) | 1-16 | 94 s (0:00-1:33) | DANZIG (4), RAYS (4), PODIUM (4), MAP world (2), SIGN (2) |
| **P2** | C1-S14 - C2-S04 (25) | 17-35 | 92 s (1:33-3:05) | MAP eu (8), LEADER (4), RAYS (3), MAP pac (2), PLANE (2) |
| **P3** | C2-S05 - C2-S23 (19) | 36-53 | 96 s (3:05-4:41) | MAP eu (9), TRENCH (2), CHANNEL (2), CARRIAGE (2), RAYS (1) |
| **P4** | C2-S24 - C3-S15 (21) | 54-69 | 92 s (4:41-6:14) | MAP eu (5), STEPPE (4), RAYS (3), SKY (2), OCEAN (2) |
| **P5** | C3-S16 - C4-S15 (20) | 70-86 | 99 s (6:14-7:52) | LEADER (5), MAP world (2), MAP pac (2), CITYRUIN (2), SNOW (2) |
| **P6** | C4-S16 - C6-S06 (17) | 87-101 | 91 s (7:52-9:24) | HOLO (6), MAP eu (4), OCEAN (2), STEPPE (1), ROOM (1) |
| **P7** | C6-S07 - C7-S09 (23) | 102-116 | 97 s (9:24-11:01) | MAP eu (5), SKY (3), MAP pac (3), RAYS (2), BEACH (2) |
| **P8** | C7-S10 - C8-S13 (18) | 117-131 | 93 s (11:01-12:33) | COUNTER (4), RAYS (4), SIGN (3), MAP world (2), MAP pac (1) |

Each package is self-contained, given the shared assets. One-off scenes stay inside their package, for example DANZIG in P1 (its line-33 callback in P2 reuses P1's module), DESERT in P5 and HOLO in P6. The heavy shared pieces are MAP eu, RAYS, LEADER and COUNTER.

## Shots
Times are estimates at 150 wpm. **Dur** is that shot's share of its line.

### Cold open (0:00, 44 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C0-S01 | 1 | 4.2 | P1 | DANZIG | Night harbour, low angle up at the old battleship's bow; a dock clock ticks to 4:45 | PROP battleship, clock; DATE 1 SEPT 1939 | slow push; open from black | clock ticks, harbour water |
| C0-S02 | 2 | 4.7 | P1 | DANZIG | Low heroic angle: the turret swings across frame toward the fort | PROP battleship turret | push in on turret | turret servo whine |
| C0-S03 | 2 | 4.7 | P1 | DANZIG | Across the water: tiny Polish guards on the Westerplatte wall look up (poster silhouettes) | FIG polish x3 idle->look; PROP fort wall | cut | gulls stop |
| C0-S04 | 3 | 1.4 | P1 | DANZIG | Full-frame muzzle star-burst; halftone smoke rolls | FX star burst, smoke | shake, smash to black | BOOM, then silence |
| C0-S05 | 4 | 7.0 | P1 | MAP world | World map; fire-coloured flood spreads out from Poland | MAP world flood (charcoal) | pull back | low rumble swell |
| C0-S06 | 5 | 4.6 | P1 | COUNTER | Huge Anton counter racing to '60-85 MILLION' over the darkening world | CTR 0->85,000,000 range card | push | ticking accelerates |
| C0-S07 | 6 | 8.6 | P1 | RAYS | Distant city skyline silhouette; one white flash wipes it to paper | PROP skyline; FX white flash | hold, flash | deep thud, ring |
| C0-S08 | 7 | 4.3 | P1 | RAYS | Title poster: WORLD WAR II 1939-1945, gold rays, slab type stamps in | CARD title | push | title sting |
| C0-S09 | 7 | 4.3 | P1 | RAYS | Subtitle strip '20 YEARS AFTER THE WAR TO END ALL WARS' slides in | CARD strip | hold | paper whoosh |

### Chapter 1: The broken peace (0:43, 134 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C1-S01 | 8 | 1.8 | P1 | RAYS | Chapter card CHAPTER 1 THE BROKEN PEACE; a calendar spins back to 1919 | CARD chapter; PROP calendar; DATE 1919 | spin, wipe | calendar riffle, sting |
| C1-S02 | 9 | 4.2 | P1 | TRENCH | Low angle: a tired German soldier (flared helmet, charcoal) lowers his rifle against grey rays | FIG german:tired->drop rifle | slow push | rifle clatter |
| C1-S03 | 10 | 5.5 | P1 | SIGN | Hall of Mirrors read as a long signing table, Allied leaders in silhouette, a German delegate alone | SIGN table; FIG civ x5 | push | pen scratch |
| C1-S04 | 10 | 5.5 | P1 | SIGN | Treaty page fills frame; four stamps thump in: RESPONSIBILITY / LAND / ARMY / MONEY | CARD 4 stamps | hold | 4 stamp thunks |
| C1-S05 | 11 | 2.2 | P1 | CROWD | Crowd silhouette, heads bowed, newspaper headline strip | CROWD civ heads-down | drift | murmur |
| C1-S06 | 12 | 3.5 | P1 | CHART | Poster stock chart line plunges off the bottom; 1929 tag | PROP chart; DATE 1929 | follow the line down | crash chord |
| C1-S07 | 12 | 3.5 | P1 | MAP world | Coins drain off the world map toward a hole | MAP world; PROP coins | pull back | coins pour |
| C1-S08 | 13 | 3.0 | P1 | CROWD | Endless jobless queue in profile, coats and flat caps; counter 6,000,000 | CROWD queue; CTR jobless | pan along queue | shuffling feet |
| C1-S09 | 14 | 5.3 | P1 | PODIUM | Low angle podium; an unnamed speaker's shadow grows huge on the wall | FIG hitler:speech (back); PROP podium | push | crowd roar swells |
| C1-S10 | 14 | 5.3 | P1 | PODIUM | Crowd seen over the speaker's shoulder, poster rays behind | CROWD rally silhouettes | cut | chant (wordless) |
| C1-S11 | 15 | 2.6 | P1 | LEADER | Hitler poster portrait 3/4, side-swept hair, moustache; name strip ADOLF HITLER | FIG leader hitler portrait | push | low brass hit |
| C1-S12 | 16 | 3.7 | P1 | PODIUM | Reichstag silhouette; JAN 1933 tag | PROP parliament; DATE JAN 1933 | push | clock |
| C1-S13 | 16 | 3.7 | P1 | PODIUM | A giant padlock snaps shut across the doors | PROP padlock | shake | padlock clunk |
| C1-S14 | 17 | 3.8 | P2 | MAP world | Pull back from Germany to the world | MAP world | zoom out | whoosh |
| C1-S15 | 18 | 3.7 | P2 | LEADER | Mussolini portrait (bald, square jaw) over a Roman-arch silhouette | FIG leader mussolini | push | fanfare stab |
| C1-S16 | 18 | 3.7 | P2 | MAP africa | Arrow from Italy to Ethiopia; 1935 tag | MAP eu-south/africa arrow | follow arrow | arrow swoosh |
| C1-S17 | 19 | 3.7 | P2 | MAP pac | East Asia: Japan floods Manchuria; 1931 stamp | MAP pac flood manchukuo; DATE 1931 | pan | stamp |
| C1-S18 | 19 | 3.7 | P2 | MAP pac | Arrows push into China; 1937 stamp; China gold holds a front | MAP pac arrows china_occ; DATE 1937 | push | drums |
| C1-S19 | 20 | 1.8 | P2 | MAP eu | Back to Europe, Germany 1937 borders lit | MAP eu | whip pan | whoosh |
| C1-S20 | 21 | 4.6 | P2 | PARADE | Rows of soldier silhouettes multiply toward the horizon; tanks & planes stamp in | FIG german:march x crowd; PROP tank, fighter | pull back | marching boots build |
| C1-S21 | 22 | 7.8 | P2 | MAP eu | Rhineland strip floods grey; 1936 tag | MAP eu region rhineland | push | boots + flood |
| C1-S22 | 23 | 2.6 | P2 | LEADER | British and French figures shrug side by side (flat dish & crested helmets) | FIG britain, france: shrug | hold | comic beat (soft) |
| C1-S23 | 24 | 3.0 | P2 | MAP eu | Austria floods grey; 1938 tag | MAP eu region austria | push | flood swell |
| C1-S24 | 25 | 3.0 | P2 | MAP eu | Sudetenland edge flashes and pulses | MAP eu region sudetenland | push | pulse ticks |
| C1-S25 | 26 | 3.5 | P2 | SIGN | Munich table, four leaders (Hitler, Mussolini, Chamberlain, Daladier); Czech chair empty | SIGN table; FIG leaders x4 | push | pen signs |
| C1-S26 | 26 | 3.5 | P2 | MAP eu | Sudetenland floods grey | MAP eu region sudetenland | cut | flood |
| C1-S27 | 27 | 6.2 | P2 | PLANE | Chamberlain at the plane door waving the paper; PEACE FOR OUR TIME strip | FIG leader chamberlain:wave paper; PROP airliner | push | crowd cheer |
| C1-S28 | 28 | 2.7 | P2 | MAP eu | Rest of Czechoslovakia floods grey; MARCH 1939 | MAP eu region czech | push | flood |
| C1-S29 | 28 | 2.7 | P2 | PLANE | Chamberlain's paper crumples in close-up | PROP paper | insert | paper crumple |
| C1-S30 | 29 | 3.8 | P2 | RAYS | Drum hit; AUGUST 1939 date card slams | DATE AUG 1939 | shake | drum hit |
| C1-S31 | 30 | 7.0 | P2 | LEADER | Hitler and Stalin poster portraits face off; handshake, crossed fingers behind backs | FIG leader hitler, stalin: handshake | push | suspense strings |
| C1-S32 | 31 | 3.4 | P2 | LEADER | NON-AGGRESSION PACT stamp across the handshake | CARD stamp | hold | stamp |
| C1-S33 | 32 | 5.8 | P2 | MAP eu | Secret dotted line splits Poland; SECRET stamp; Baltic states & Finland tinted red | MAP eu secret_line, regions baltics/finland | push (style frame map_1939) | pen scratch, stamp |
| C1-S34 | 33 | 4.2 | P2 | DANZIG | Callback: the battleship flash from the open | PROP battleship; FX star burst | smash cut | BOOM |

### Chapter 2: Lightning war, 1939-1940 (2:57, 128 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C2-S01 | 34 | 1.5 | P2 | RAYS | CHAPTER 2 LIGHTNING WAR card (style_reference) | CARD chapter | wipe | sting |
| C2-S02 | 34 | 1.5 | P2 | MAP eu | Grey arrows sweep across Poland from Germany and East Prussia | MAP eu arrows poland | push | tank rumble |
| C2-S03 | 34 | 1.5 | P2 | FIELD | Poster tank silhouette rolls through frame, dive bomber overhead | PROP tank, dive bomber | pan | engine roar |
| C2-S04 | 35 | 3.5 | P2 | RAYS | BLITZKRIEG word card over a newspaper masthead; LIGHTNING WAR underline | CARD word; PROP newspaper | push | press clatter |
| C2-S05 | 36 | 4.6 | P3 | RAYS | Two telegrams fly in: LONDON / PARIS 3 SEPT | PROP telegrams; DATE 3 SEPT 1939 | hold | telegraph clicks |
| C2-S06 | 37 | 5.0 | P3 | MAP eu | Red arrows from the east; 17 SEPT | MAP eu arrows soviet | push | brass + rumble |
| C2-S07 | 38 | 3.8 | P3 | MAP eu | Poland floods grey and red along the secret line | MAP eu flood | hold | flood |
| C2-S08 | 39 | 3.4 | P3 | TRENCH | Western front: soldiers in a trench yawning | FIG france, britain: idle yawn | drift | crickets |
| C2-S09 | 40 | 6.7 | P3 | TRENCH | A clock spins months; PHONEY WAR card | PROP clock; CARD word | hold | clock ticking |
| C2-S10 | 41 | 4.6 | P3 | MAP eu | Denmark and Norway flood grey; APRIL 1940 | MAP eu regions denmark/norway | pan north | flood |
| C2-S11 | 42 | 5.4 | P3 | MAP eu | Four arrows west into NL, BE, LUX, FR; 10 MAY 1940 | MAP eu arrows west | push | rumble |
| C2-S12 | 43 | 7.0 | P3 | MAP eu | Maginot Line glows as a fort chain along the border | MAP eu line maginot; PROP fort icons | track along line | concrete thud |
| C2-S13 | 44 | 4.5 | P3 | FOREST | Ardennes trees in poster layers; tank column threads through | PROP trees, tank x n | track | engines in woods |
| C2-S14 | 44 | 4.5 | P3 | MAP eu | Arrow curls around the Maginot Line through the Ardennes | MAP eu arrow ardennes | push | arrow swoosh |
| C2-S15 | 45 | 4.6 | P3 | MAP eu | Arrow hits the Channel coast; 10 DAYS counter | MAP eu arrow; CTR days | push | impact + count |
| C2-S16 | 46 | 6.6 | P3 | BEACH | Packed Dunkirk beach, lines of soldiers to the water, smoke in the sky | CROWD soldiers beach; PROP smoke | pan | distant guns, sea |
| C2-S17 | 47 | 6.2 | P3 | CHANNEL | Flotilla: destroyers, ferries, fishing boats, little yachts cross the Channel | PROP destroyer, ferry, small boats | track | engines, gulls |
| C2-S18 | 48 | 7.4 | P3 | CHANNEL | Boats return loaded; counter climbs to 338,226 | PROP boats; CTR 338,226 | hold | counter ticks |
| C2-S19 | 49 | 2.2 | P3 | MAP eu | France greys out | MAP eu region france | push | low drone |
| C2-S20 | 50 | 3.4 | P3 | CARRIAGE | Railway carriage in a Compiègne clearing; 22 JUNE 1940 | PROP railway carriage, trees; DATE | push | wind, birds |
| C2-S21 | 51 | 7.8 | P3 | CARRIAGE | 1918 flashback: same carriage in sepia halftone, then match-cut to 1940 | PROP carriage x2 | match cut | clock + echo |
| C2-S22 | 52 | 3.8 | P3 | MAP eu | Britain and the Commonwealth in blue against a grey continent; Commonwealth outlines light far off | MAP world inset commonwealth | pull back | wind |
| C2-S23 | 53 | 4.6 | P3 | LEADER | Churchill portrait (bowler, cigar) shakes his head; NO PEACE stamp | FIG leader churchill:shake head | push | brass motif |
| C2-S24 | 54 | 8.2 | P4 | SKY | Swarms of charcoal bombers cross the Channel at a low heroic angle | PROP bomber x n | push | drone of engines |
| C2-S25 | 55 | 3.0 | P4 | RAYS | THE BATTLE OF BRITAIN title poster, blue rays, fighter silhouettes | CARD title; PROP fighter | push | sting |
| C2-S26 | 56 | 3.1 | P4 | COAST | Radar towers on the cliffs; rings pulse out; blips appear | PROP radar tower; FX rings | push | radar pings |
| C2-S27 | 56 | 3.1 | P4 | SKY | Fighters scramble up into the bombers | PROP fighter x n, bomber | track | engines, guns (muffled) |
| C2-S28 | 57 | 3.3 | P4 | MAP eu | Invasion arrow across the Channel fades out; SEA LION CALLED OFF stamp | MAP eu arrow fade; CARD stamp | hold | stamp |
| C2-S29 | 57 | 3.3 | P4 | CITY | London rooftops at night, searchlights cross, flat bomb bursts | PROP skyline, searchlights | push | sirens |

### Chapter 3: The war goes global, 1941 (5:06, 93 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C3-S01 | 58 | 4.2 | P4 | RAYS | CHAPTER 3 THE WAR GOES GLOBAL card; a die rolls over the map | CARD chapter; PROP die | wipe | dice roll |
| C3-S02 | 59 | 6.6 | P4 | LEADER | The pact paper tears; the handshake snaps apart; 22 JUNE 1941 | FIG hitler, stalin; PROP pact | shake | paper rip |
| C3-S03 | 60 | 7.4 | P4 | MAP eu | Front from Baltic to Black Sea; three giant grey arrows | MAP eu arrows barbarossa | pull back | huge rumble |
| C3-S04 | 61 | 2.2 | P4 | RAYS | OPERATION BARBAROSSA word card, stencil | CARD word | hold | stamp |
| C3-S05 | 62 | 2.2 | P4 | MAP eu | Arrows race east | MAP eu arrows | push | momentum |
| C3-S06 | 63 | 3.7 | P4 | STEPPE | Columns of Soviet prisoners as distant silhouettes; counter MILLIONS | CROWD soviet prisoners | pan | wind |
| C3-S07 | 63 | 3.7 | P4 | MAP eu | Arrow tip stops at the Moscow dot; DEC 1941 | MAP eu city moscow | push | rumble stops |
| C3-S08 | 64 | 3.5 | P4 | STEPPE | Tanks stuck axle-deep in autumn mud; supply trucks stalled | PROP tank, truck; FX mud | track | engines straining |
| C3-S09 | 64 | 3.5 | P4 | STEPPE | Snow begins to fall over everything | FX snow | hold | wind rises |
| C3-S10 | 65 | 6.2 | P4 | STEPPE | Shivering German soldiers in thin coats; thermometer to -30 | FIG german:shiver x3; PROP thermometer | push | howling wind |
| C3-S11 | 66 | 5.8 | P4 | MAP eu | Red arrows push the grey line back from Moscow; 5 DEC | MAP eu front moves | push | brass rise |
| C3-S12 | 67 | 4.5 | P4 | MAP world | Globe spins to the Pacific | MAP world spin | whip pan | whoosh |
| C3-S13 | 67 | 4.5 | P4 | OCEAN | Pearl Harbor: battleship row, dive bombers diving in; 7 DEC 1941 | PROP battleships, dive bomber x n | push | plane dive whine |
| C3-S14 | 68 | 5.8 | P4 | OCEAN | Ships tilt and smoke (flat puffs) | PROP battleships; FX smoke | hold | explosions (muffled) |
| C3-S15 | 69 | 4.2 | P4 | COUNTER | Counter 2,403 on smoke-dark paper | CTR 2,403 | hold | single bell |
| C3-S16 | 70 | 4.6 | P5 | LEADER | Roosevelt (pince-nez) at a radio microphone; 8 DEC | FIG leader roosevelt:speech; PROP microphone | push | radio hiss |
| C3-S17 | 71 | 5.4 | P5 | LEADER | Hitler points across an Atlantic map; 11 DEC | FIG leader hitler:point; MAP world | push | drum |
| C3-S18 | 72 | 3.4 | P5 | MAP world | Pull back: both oceans flicker with fire | MAP world | pull back | swell |
| C3-S19 | 73 | 4.2 | P5 | LEADER | Three Axis portraits side by side in charcoal tones | FIG leaders hitler, mussolini, hirohito | slide in | low brass |
| C3-S20 | 74 | 7.0 | P5 | LEADER | Allied portraits line up: Churchill, Stalin, Roosevelt, Chiang + 'and many more' flags as colour chips | FIG leaders churchill, stalin, roosevelt, chiang | slide in | bright brass |

### Chapter 4: The turning points, 1942-1943 (6:38, 105 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C4-S01 | 75 | 1.7 | P5 | RAYS | CHAPTER 4 THE TURNING POINTS card | CARD chapter | wipe | sting |
| C4-S02 | 75 | 1.7 | P5 | MAP world | Grey fills half the map; EARLY 1942 | MAP world flood | pull back | drone |
| C4-S03 | 76 | 3.8 | P5 | MAP pac | Grey spreads across SE Asia and the Pacific | MAP pac flood | pan | flood |
| C4-S04 | 77 | 3.5 | P5 | ROOM | Codebreakers' basement: headphones, code paper, one figure circles a word | FIG usa civ x2; PROP headphones, papers | push | morse |
| C4-S05 | 77 | 3.5 | P5 | MAP pac | Map pin drops on MIDWAY | MAP pac city midway | push | pin thunk |
| C4-S06 | 78 | 4.9 | P5 | SKY | Dive bombers peel off high above; 4 JUNE 1942 | PROP dive bomber x3 | tilt down | dive whine |
| C4-S07 | 78 | 4.9 | P5 | OCEAN | Three carriers burst into flat flame | PROP carrier x3; FX star bursts | pull back | three booms |
| C4-S08 | 79 | 7.5 | P5 | COUNTER | Four carrier icons crossed out one by one | CARD icons x4 | hold | 4 stamps |
| C4-S09 | 80 | 8.2 | P5 | DESERT | Desert at El Alamein: Commonwealth tanks advance, Rommel's arrow pushed back west | PROP tank x n; MAP inset n.africa | track | tank guns |
| C4-S10 | 81 | 8.7 | P5 | CITYRUIN | City on the Volga; STALINGRAD zooms in as slab type | PROP ruined skyline; CARD word | push | wind, distant guns |
| C4-S11 | 82 | 6.6 | P5 | CITYRUIN | Building cross-section, a figure on each floor ducking | PROP building section; FIG german, soviet crouch | tilt up | gunfire (muffled) |
| C4-S12 | 83 | 4.6 | P5 | MAP eu | Red pincers close a ring around Stalingrad; NOV 1942 | MAP eu zoom stalingrad arrows | push | pincers clank |
| C4-S13 | 84 | 2.6 | P5 | LEADER | Hitler slams a table: NO RETREAT stamp | FIG leader hitler:slam | shake | slam |
| C4-S14 | 85 | 4.2 | P5 | SNOW | A white flag in the snow; 2 FEB 1943 | PROP white flag; FX snow | hold | wind, silence |
| C4-S15 | 86 | 7.8 | P5 | SNOW | A long line of prisoners walks into the snow; counter ~91,000 | CROWD german prisoners; CTR | track | footsteps in snow |
| C4-S16 | 87 | 4.6 | P6 | MAP eu | Grey arrows reverse westward | MAP eu arrows reverse | pull back | reverse whoosh |
| C4-S17 | 88 | 6.6 | P6 | STEPPE | Kursk plain: hundreds of tank silhouettes clash under star-burst flashes | PROP tank x many; FX bursts | pan | tank battle |
| C4-S18 | 89 | 6.6 | P6 | OCEAN | Periscope rises; Atlantic map with convoy ships sinking as icons | PROP periscope, submarine; MAP world atlantic | push | sonar ping |
| C4-S19 | 90 | 9.0 | P6 | ROOM | Bletchley hut: Turing at a bombe; a Polish cipher chip on the desk; Enigma letters scramble then click into words | FIG britain civ (turing); PROP enigma, bombe | push | rotor clicks |
| C4-S20 | 91 | 4.2 | P6 | OCEAN | U-boat counter falls; MID 1943 | CTR uboats | hold | falling tone |

### Chapter 5: The Holocaust (8:23, 43 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C5-S01 | 92 | 6.6 | P6 | HOLO | CHAPTER 5 THE HOLOCAUST on plain black (no rays); fade to a muted grey map of Europe | CARD chapter (black); MAP eu muted | slow fade | music drops to one low tone |
| C5-S02 | 93 | 8.7 | P6 | HOLO | Text on black, white serif | CARD text | hold | tone only |
| C5-S03 | 94 | 8.2 | P6 | HOLO | Ghetto dots appear in cities; rail lines draw slowly toward camp dots (Auschwitz named) | MAP eu muted; rail lines; city dots | very slow push | tone only |
| C5-S04 | 95 | 4.2 | P6 | HOLO | 6,000,000 appears and stays | CTR static | hold | silence |
| C5-S05 | 96 | 8.6 | P6 | HOLO | Lines of text naming the other victim groups, one by one | CARD text lines | hold | tone |
| C5-S06 | 97 | 6.6 | P6 | HOLO | A single candle flame, flat poster shape | PROP candle | hold 2 s extra | tone fades |

### Chapter 6: Closing in, 1943-1945 (9:06, 87 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C6-S01 | 98 | 1.9 | P6 | RAYS | CHAPTER 6 CLOSING IN card | CARD chapter | wipe | sting |
| C6-S02 | 98 | 1.9 | P6 | MAP eu | Arrows hit Sicily; JULY 1943 | MAP eu arrows sicily | push | landing craft |
| C6-S03 | 99 | 1.9 | P6 | LEADER | Mussolini portrait tipped off a pedestal | FIG leader mussolini; PROP pedestal | tilt | crash |
| C6-S04 | 99 | 1.9 | P6 | MAP eu | Italy flips to Allied blue in the south; SEPT 1943 | MAP eu region italy split | push | flip |
| C6-S05 | 100 | 5.4 | P6 | MAP eu | Grey defensive lines across Italy hold | MAP eu lines gustav | push | guns |
| C6-S06 | 101 | 4.6 | P6 | CHANNEL | Huge fleet fills the Channel horizon to horizon | PROP ship x many | pull back | massed engines |
| C6-S07 | 102 | 2.6 | P7 | RAYS | 6 JUNE 1944 D-DAY date poster | CARD date | push | sting |
| C6-S08 | 103 | 4.9 | P7 | MAP eu | Normandy: five beaches light up; parachute icons drop inland | MAP eu zoom normandy; PROP parachute icons | push | aircraft |
| C6-S09 | 103 | 4.9 | P7 | SKY | Paratroopers drifting down in silhouette at dawn | FIG usa/britain paratroopers | drift | wind |
| C6-S10 | 104 | 3.3 | P7 | BEACH | Omaha: figures dash across sand past obstacles, flat bursts | FIG usa:run x n; PROP obstacles | track | surf, gunfire |
| C6-S11 | 104 | 3.3 | P7 | BEACH | Sunset on a held beach, flags in the sand | PROP sunset | dissolve | calm surf |
| C6-S12 | 105 | 9.8 | P7 | MAP eu | Huge red arrow smashes the grey Army Group Centre block; 22 JUNE 1944 | MAP eu arrow bagration | push | massive rumble |
| C6-S13 | 106 | 2.6 | P7 | CITY | Paris map: crowds and confetti; AUG 1944 | MAP eu city paris; CROWD cheering | push | bells, cheering |
| C6-S14 | 107 | 9.4 | P7 | MAP eu | Grey bulge pushes into the blue line through the Ardennes; DEC 1944 | MAP eu front bulge | push | tanks in snow |
| C6-S15 | 108 | 1.4 | P7 | MAP eu | The bulge collapses | MAP eu front | pull back | deflate |
| C6-S16 | 109 | 6.6 | P7 | MAP pac | Blue arrows leap island to island toward Japan | MAP pac arrows hop | track | hops |
| C6-S17 | 109b | 5.3 | P7 | MAP pac | Camera swings west: China in gold holds a long front | MAP pac china front | pan | drums |
| C6-S18 | 109b | 5.3 | P7 | MAP pac | Blue arrow pushes out of India into Burma | MAP pac arrow burma | push | brass |
| C6-S19 | 110 | 4.9 | P7 | ISLAND | Volcanic island silhouette under flat bursts; bar chart of casualties grows | PROP island; CARD chart | push | guns |
| C6-S20 | 110 | 4.9 | P7 | ISLAND | Worried generals around a map table | FIG usa officers x3 | push | low strings |

### Chapter 7: The end (10:33, 58 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C7-S01 | 111 | 2.9 | P7 | RAYS | CHAPTER 7 THE END card | CARD chapter | wipe | sting |
| C7-S02 | 111 | 2.9 | P7 | MAP eu | Red ring closes around Berlin; LATE APRIL 1945 | MAP eu zoom berlin ring | push | rumble |
| C7-S03 | 112 | 4.2 | P7 | CITYRUIN | Bunker door slams shut; 30 APRIL | PROP bunker door | hold | slam, silence |
| C7-S04 | 113 | 2.6 | P7 | SIGN | Signing table at Reims; 7 MAY | SIGN table; FIG officers | push | pen |
| C7-S05 | 114 | 2.9 | P7 | CROWD | Cheering crowd, hats flying; V-E DAY 8 MAY | CROWD cheer | push | cheers, bells |
| C7-S06 | 114 | 2.9 | P7 | CROWD | Moscow crowd under fireworks; 9 MAY | CROWD cheer; FX fireworks | cut | fireworks |
| C7-S07 | 115 | 2.2 | P7 | OCEAN | Quiet Pacific: a single ship on calm water | PROP ship | hold | silence, wind |
| C7-S08 | 116 | 3.5 | P7 | SKY | A lone bomber high over clouds; 6 AUG 1945 | PROP bomber | track | single engine |
| C7-S09 | 116 | 3.5 | P7 | SKY | White flash; distant mushroom-cloud silhouette | FX flash; PROP cloud silhouette | hold | deep thud, ring |
| C7-S10 | 117 | 4.6 | P8 | MAP pac | Red arrows into Manchuria; 8 AUG | MAP pac arrows manchuria | push | brass |
| C7-S11 | 118 | 4.6 | P8 | SKY | Second flash over a distant skyline; 9 AUG | FX flash | hold | thud |
| C7-S12 | 119 | 7.8 | P8 | COUNTER | Number on black: AS MANY AS 200,000 | CTR static | hold | silence |
| C7-S13 | 120 | 6.6 | P8 | ROOM | Family around a radio, heads bowed; 15 AUG | FIG japan civ x4; PROP radio | push | crackling radio |
| C7-S14 | 121 | 6.6 | P8 | OCEAN | USS Missouri deck signing; 2 SEPT 1945 | PROP battleship deck; SIGN table | pull back | gulls, final chord |

### Chapter 8: After the war (11:31, 62 s)
| Shot | Line | Dur | Pkg | Set-piece | Composition | Assets | Camera / transition | Sound |
|---|---|---|---|---|---|---|---|---|
| C8-S01 | 122 | 2.3 | P8 | RAYS | CHAPTER 8 AFTER THE WAR card | CARD chapter | wipe | sting |
| C8-S02 | 122 | 2.3 | P8 | MAP world | Slow pull back over a grey world | MAP world muted | pull back | low strings |
| C8-S03 | 123 | 4.2 | P8 | COUNTER | Counter: SOVIET UNION ~27,000,000 | CTR | push | ticks |
| C8-S04 | 123b | 3.0 | P8 | COUNTER | Second counter beside it: CHINA 15,000,000+ | CTR | hold | ticks |
| C8-S05 | 124 | 6.7 | P8 | COUNTER | Cold-open counter returns and settles on 60-85 MILLION; MOST CIVILIANS | CTR range card | hold | settle |
| C8-S06 | 125 | 7.4 | P8 | SIGN | Generic round table, many flags as plain colour chips | SIGN round table; FIG civ x n | push | gavel |
| C8-S07 | 126 | 3.5 | P8 | SIGN | Courtroom: defendants in the dock (Nuremberg) | PROP courtroom; FIG defendants | push | gavel |
| C8-S08 | 126 | 3.5 | P8 | SIGN | Second courtroom tag: TOKYO | PROP courtroom | cut | gavel |
| C8-S09 | 127 | 8.2 | P8 | LEADER | US and Soviet figures stand back to back; the map splits blue and red | FIG usa, soviet; MAP world split | push | tension chord |
| C8-S10 | 128 | 3.8 | P8 | MAP world | Map zooms out to the whole war | MAP world | pull back | rise |
| C8-S11 | 129 | 3.4 | P8 | RAYS | Three poster cards slide in | CARD x3 | slide | card flips |
| C8-S12 | 130 | 9.5 | P8 | RAYS | Each card lights as named: BARBAROSSA / AMERICA JOINS / STALINGRAD | CARD x3 highlight | hold | 3 hits |
| C8-S13 | 131 | 4.6 | P8 | RAYS | Cards hold; COMMENT strip; cut within half a second | CARD | hard cut out | final hit |
