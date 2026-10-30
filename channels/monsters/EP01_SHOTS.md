# Episode 1 shot list: "I Died Because of a Shrimp"

Lengths come from the voiced takes (Kai = Turbo `am_liam`, `assets/voice_cache/monsters_ep01_takes.tar`); with the
standard pauses the episode runs ~42.6 s. A shot's length is its line plus the pause after it, at 24 fps. Cut every
1.5-3 s (ANIME_STUDY.md): long lines are split into two shots. Frame 0 of S01 already shows the hook text.

| Shot | Line (s) | Narration | Picture | Camera | 2D overlay (fx2d) | Asset owner |
|---|---|---|---|---|---|---|
| S01 | 1 (2.11) | This cute little thing just erased a forest. | Puff-shrimp in the smoking crater, claw raised, eyes half-shut, smoke drifting | low, medium close, slow push-in | `hook_text` "IT ERASED / A FOREST", `creature_tag` WILD ??? threat 5 | coordinator (crater, puff-shrimp) |
| S02 | 2 (1.66) | Ten minutes ago, I was on Earth. | S01 frames run backwards with a glitch | none | glitch/rewind, chip "EARTH" | coordinator |
| S03 | 3 (2.62) | Wildlife biology student. Night shift at the lab. | Kai at the desk between glowing tanks, rain on the window, cool blue | medium, locked | none | lab: helper 1 · Kai: Kai helper |
| S04a | 4a | My favourite animal was this little guy. | The tank: Kai's finger taps the glass, the shrimp turns | medium close, locked | none | pistol shrimp: helper 2 |
| S04b | 4b (4 = 3.03) | The pistol shrimp. | Shrimp close-up, one huge claw, bubbles | close, locked | `rule_chip`-style name tag "PISTOL SHRIMP" | helper 2 |
| S05a | 5a | Its claw snaps so fast, | Slow-motion claw: open, shut | extreme close, locked | speed lines (radial, bg=False) | helper 2 |
| S05b | 5b (5 = 4.35) | it makes a bubble almost as hot as the surface of the sun. | The cavitation bubble glows white-hot, then collapses | close, slow push | `fact_card` "BUBBLE: ~4,700 °C", `bokeh` | helper 2 |
| S06 | 6 (2.33) | But only underwater. Remember that. | The bubble fades in the water; the shrimp blinks | close, locked | `fact_card` line "ONLY IN WATER" (yellow) | helper 2 |
| S07 | 7 (1.36) | That night, there was a storm. | Lightning outside the lab window, the lights flicker | wide of the window, locked | none | storm: helper 9 · lab: helper 1 |
| S08 | 8 (0.38) | Snap. | The shrimp snaps; a crack runs up the tank glass | close, 2-frame shake | `impact_frame` frames=2 (subject pass) | helper 2 |
| S09 | 9 (1.53) | The water reached the cables. | Water trickles across the floor to the power strip | low, floor level, short pan | none | helper 1 |
| S10 | 10 (1.90) | The lights went out. And so did I. | A spark, then black ("And so did I." on black), then pure white | locked | none | helpers 1 and 9 |
| S11 | 11 (0.92) | Then I heard birds. | White opens into a pastel sky; falling through soft clouds | falling, on 1s | none | world: helper 3 |
| S12 | 12 (2.14) | I woke up in grass that smelled like candy. | The camera floats down over the world: giant mushrooms, round hills, a pond | slow descent | ambient `sparkles` | helper 3 |
| S13 | 13 (2.73) | And there was a menu. Floating in front of my eyes. | Kai's view of the meadow; the menu boots | POV, locked | `hud_boot`, then `status_bar` KAI · LV 1 | helper 3 (bg) |
| S14a-c | 14 (2.35) | Everything here was small. And adorable. | Three ~0.9 s shots: jelly-snail, tuftwing, fluffmoth, each in a cute held pose | close, locked | `creature_tag` WILD ??? (red) on each | helpers 4, 5, 6 |
| S15 | 15 (1.14) | I reached out to pet one. | POV: Kai's hand reaches toward the puff-shrimp drinking at a puddle | POV, locked | none | coordinator · hand: Kai helper |
| S16 | 16 (0.38) | Snap. | Claw snaps; white shockwave ring | close, shake | `impact_frame` frames=2 (subject pass), `shockwave` | coordinator |
| S17 | 17 (1.54) | The forest behind it was gone. | The trees behind it dissolve into dust; Kai is thrown back; HP drops to red | wide, then shake | `status_bar` hit to red | erase: helper 10 · coordinator |
| S18 | 18 (1.33) | And now it's looking at me. | S01's crater framing: the creature turns its huge eyes to camera | low, locked, then a 6-frame push | `creature_tag` threat 5 blinking | coordinator |
| S19 | 19 (1.15) | Run, or stay still? | Choice menu over the frozen creature | locked | `choice_menu` RUN / STAY STILL, no pick | coordinator |

Rules for every shot:
- Characters act on 3s (step=2 for fast action); camera and VFX on 1s.
- Big moments (S08, S16): the character freezes while the effect moves.
- Shots S08 and S16 also render a **subject pass** (the character alone on a transparent film) so the impact frame
  and speed-line backgrounds keep the creature as a clean silhouette (see HELPERS.md v3.2).
- Captions sit at 845-930 px; nothing important under 845 or in the Shorts right rail (x > 620, y 640-1180).
- The last spoken line ends the video within 0.5 s (no outro).
