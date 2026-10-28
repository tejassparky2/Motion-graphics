# Interactive horror Shorts (separate channel)

Owner, 25 Oct 2026: "stories videos like this but with better animation, not for this channel" / "Yes open separate chat, 3D".
Branch `ccr-56282fe5-evehq4-horror`. Not Interestingly Strange: never put these in that calendar.

## Format
- Second person ("you"), 70-80 s, numbered series (Part 1 / Night 1 style).
- A ticking resource on a HUD (battery, fuel, light), one rule, a mostly unseen threat, a phone/radio message that
  makes it worse, and an impossible two-way choice as the last spoken line. The audience votes in the comments and the
  majority decides the next part.
- Better than the references: real 3D characters with faces that show fear, real lighting (flicker, torch beams, wet
  reflections, lightning), fear-building camera (push-ins, over-the-shoulder, cut to black), horror sound design
  (motion/audio.py thriller_sfx), one tiny hidden "wrong" detail per episode for rewatches.

## Rules
- Original stories only; never retell the reference videos ("The Copy", "Night 1") and never commit them.
- Suspense, not gore; nothing aimed at real people.
- Never the owner's cloned voice, never a clone of a real person.
- No metadata/encoder tags. Whisper medium check on every line after rendering.
- Script first (lines, on-screen note, title) and render only after the owner approves.

## Tools
- three.js engine: channels/is3d/ (scene_is3d.html, directions/*.js, make_is3d.py, render.mjs). Sample: out/robot_butler.mp4.
- Phone UI: motion/thriller.py phone(). Voices: Chatterbox Turbo (/home/user/.venv-clone).

## Build
    /home/user/.venv-main/bin/python channels/horror/make_horror.py floor13      # voices, 3D frames, HUD, sound -> out/horror/
    /home/user/.venv-main/bin/python channels/horror/check.py floor13            # Whisper medium on every line + tag check
    RANGE=a:b SCENE=... TIMING=... node channels/horror/render.mjs FRAMES 30     # re-render only frames a..b-1
Episodes: floor13.py, last_stop.py, tower9.py (scripts + HUD + sound cues); sets/lift.js, bus.js, tower.js (3D);
hud.py (meter, chips, phone chat, rule strip, blueprint cards, YOUR CALL); sound.py (synthesized horror effects).

2D (the look the owner chose, 25 Oct: "Not liking the animation" -> "Illustrated 2D, drawn in code" -> "Yeah 2d better"):
    /home/user/.venv-main/bin/python channels/horror/make_2d.py last_stop_2d                  # -> out/horror/last_stop_2d.mp4
    /home/user/.venv-main/bin/python channels/horror/make_2d.py last_stop_2d --stills 5,22.5  # check frames (build/horror/check2d)
    /home/user/.venv-main/bin/python channels/horror/check.py last_stop_2d                    # Whisper medium + tags
EPISODE_2d.py reuses EPISODE.py's SCRIPT, METADATA (hud2d.meta_2d: says "2D animation") and KEY, so the voice takes are
shared; only the drawing, shot list and cue timing are new. toon2d.py = the cast drawn in cairo (the lead "you",
Mrs. Gray, the old man, the driver's eyes, the pale passengers) with cel shading; hud2d.py = the overlays after the
owner's 2D reference (stats bar, rounded captions with red key words, RULE tag, stamps, speech bubbles, phone held in
both hands, background blur, A/B ending card). About 2-3 min per episode to render.

## Status
- 25 Oct 2026: channel opened. Owner: "All a b c make them now" -> Floor 13 (Part 1), Last Stop and Tower 9 (Night 1)
  made with the Turbo stock narrator (scripts: out/horror/scripts_part1.md). Name / narrator / part-2 timing still open.
- Ideas taken from the owner's references 3-7 (never their stories): inventory chips, full-screen phone chat, time cards,
  a line for each side before the vote, YOUR CALL card, big readable faces, two-colour lighting, blueprint cards,
  one hard number per rule, state carried into Part 2, the vote result shown at the start of Part 2.
- 25 Oct: all three delivered (out/horror/): floor13 (80 s, 23/24 lines exact), last_stop (72 s, 19/21), tower9
  (70 s, 20/21); the remaining flags are spelling only (2%, creak/creaks, 1040, one/won). Lessons: a sound effect on a
  word hides it (cue effects after the word or in a silence), rain/generator beds must sit low, Turbo says "riding" like
  "writing". Research report: reports/3D horror Shorts animation and hooks.md. Technique source worth reusing (MIT):
  github.com/lemomo-ai/lemo-opuscar (DIRECTOR.md, TECHNIQUE.md, styles/backrooms: VHS pass, handheld fear rig, OSD).
- 25 Oct: the owner didn't like the 3D look and picked illustrated 2D. Floor 13 2D (80 s, 22/24 exact, the rest digits)
  and Last Stop 2D (73 s, 20/21 exact, the other is "ten forty" heard as 1040) delivered. Lessons: the "creak/creaks"
  flag was the take itself (the dry take said "creak"; re-made it), so check the dry take before blaming the mix; a
  phone buzz under "out of service" made "out of Cervith" (notes can be silent); the breath on "breathes" made
  "bruised", so the breath now plays in a 1.3 s silence after the line.
- 25 Oct: Tower 9 2D (72 s, 20/21 exact; the other is "one" heard as its homophone "won") delivered; you wear an orange
  ranger jacket, and in the lightning one torch-holder below wears it too. Lessons: a noise right after a word ending
  reads as an "-s" ("crackled" -> "crackles"), so the rain starts after the hook line and static goes before the word
  or in a pause; a thunder roll needs ~1.8 s before a quiet line ("Please" -> "Wait"); lowpass 1800 on the hatch voice
  made "cold" into "cool" (now 2800). Whisper results move with the mix, so fix the cause, not single runs.
- Owner on the 2D Tower 9 (25 Oct): "Tower 9 is better now". Keep what it has: warm practical light (bulb, lantern,
  LCD) against the cold storm, objects that tell the story close up (radio, logbook writing itself, clock, fuel gauge,
  hatch), the outfit detail paid off in the lightning, and the mix fixes above.
- Channel name: "Midnight with <host>", the host's name still to pick (owner, 25 Oct 2026: rejected "Mae" as too
  common, then "Manya" as sounding Indian: "give me western name like this unique"). Offered, all free as
  @MidnightWith<Name> with no web hits: Elowen, Tamsin, Ottilie, Isolde, Sidonie, Odessa (Odessa reads as the city
  in the war news). The owner then asked "Midnight with Nancy?": @MidnightWithNancy free and the phrase unused on
  25 Oct; art and setup sheet made with it (brand.py Nancy). Owner: "Ok going with Midnight with Nancy make Nancy
  hair like Japanese" -> a hime cut (straight blue-black hair, blunt bangs at the brow line, jaw-length side locks,
  long straight hair, a shine ring), on the first drawing's face and outfit. Then: "Na switch to previous" -> back to the
  first drawing's long dark waves (the hime cut is in git history, commit ac7d124, if it's ever wanted). The host is a fictional storyteller (toon2d.host_bust), never presented as a real person; the
  description says the voices are synthetic. Her look: the FIRST drawing (owner: "previous was better" than a
  detailed redraw with lashes, earrings and a shawl), so keep that simpler style. Channel art:
  `python channels/horror/brand.py NAME` -> out/horror/channel/ (avatar.png, banner.png); setup steps, description
  and keywords: out/horror/channel/setup.md. The owner creates the Gmail and channel (phone verification); never ask
  for their password.
- Next (owner, 25 Oct: "Yes do the Quaternius and vrm avatar model test after these"): a 15 s test with Quaternius CC0
  bodies + animations (build/assets3d/uaf: Universal Animation Library 1 and 2, standard, from opengameart.org; 89 clips
  incl. Driving, Idle_Torch, Sitting, Crouch, Hit_Head, Idle_TalkingPhone, ClimbUp, Zombie_Walk) and a VRM face
  (@pixiv/three-vrm; a CC0 or freely licensed VRM model still to find).
- Vote: owner, 25 Oct 2026: "Most commented B" (taken as Tower 9: B = keep the hatch shut; owner to correct if it was
  another episode). Night 2 script sent for approval: out/horror/scripts_night2_tower9.md (a new choice, window or
  hatch, so it isn't the same situation with the same outcome; pays off Night 1's jacket detail). Don't render
  until the owner approves.
- 25 Oct: owner approved the Night 2 script ("Approved, make it"). Tower 9 Night 2 delivered (66 s,
  out/horror/tower9_n2_2d.mp4, channels/horror/tower9_n2_2d.py): Whisper medium 17/17 exact after one reword
  ("By your phone's light" was heard as "phone flight" -> "In the light of your phone"). New kit: toon2d "smile" face
  and finger_to_lips, sound glass_tap; check.py handles episodes without a 3D twin.
- Schedule (owner, 26 Oct 2026): Tower 9 goes out daily at 4:30, a second, different mystery/suspense story daily at
  7:30 (taken as PM IST, like the main channel). Second story: "Snowbound" (five friends snowed in at a cabin, ten
  seconds of dark, Maya gone, Leo and Ivy both lying); Part 1 script sent for approval:
  out/horror/scripts_snowbound_part1.md. Western names (the owner preferred a Western host name). Don't render until
  approved. Each daily part needs that day's vote; writing both branches ahead keeps the schedule.
- 26 Oct: owner asked for research on hooks (so viewers don't swipe), mid-video suspense and endings people can't help
  commenting on ("no hallucinations"). Report: reports/Horror Shorts hooks retention comments.md (9,100 words, 85
  sources, every claim labelled Measured / Official / Craft / Creator / Vendor; ends in a 70 s checklist H1-H8, M1-M12,
  T1-T5, V1-V8, A1-A6). Apply the checklist to every new script. Limits: first-hand Reddit was unreachable from this
  environment (search index excludes reddit.com, fetches refused; the owner's "workaround" permission was not usable
  because the proxy route is blocked as bot-check circumvention), so Reddit evidence is second-hand only; the
  "Zeigarnik effect" failed a 2025 meta-analysis, don't cite it. Snowbound Part 1 rewritten as v2 against the checklist
  (out/horror/scripts_snowbound_part1.md) and sent for approval.
- 27 Oct: owner "Make next story on bank heist. Continue" -> Time Lock, Part 1 (the 7:30 series; Snowbound v2 kept on
  file). Script for approval: out/horror/scripts_timelock_part1.md, written against the research checklist. Episode
  built (channels/horror/timelock_2d.py: masked Danny via ski_mask over you_bust, teller glass, vault door with time
  lock, 48-box wall, box 41 holder card, scarred hand and "D" key, alarm pedal with the inch measured, the photo);
  voices made; preview frames out/horror/timelock_part1_preview_frames.png. The final render waits for approval.
- 27 Oct: owner approved Time Lock Part 1 ("Approved"). Delivered out/horror/timelock_2d.mp4 (65 s), Whisper medium
  19/19 (check.py now knows 41 / 2:10 / key ring forms); thumbnail out/horror/thumbs/timelock.png. Note: hud2d.blurred()
  assumes a 720 x 1280 device, so thumbnails (drawn at 1.5x) dim the background instead of blurring it.
- 27 Oct: owner sent two reference Shorts from another new page (10-12k views each against our 1.5k): "study this".
  Findings in reports/Horror reference study 27 Oct.md. Pace, brightness, HUD and captions match ours. The gap is the
  premise (home, family, Halloween dated), rules that work as tells, a "which one is real" vote people can argue with
  clues, a test beat, a late flip at ~75%, a new shot every 2-4 s with a face in it, and Part 2 opening on the vote
  result with comment cards. Apply all of it to new scripts. Time Lock Part 1 v2 (thief, Lena; toon2d thief_bust /
  lena_bust; timelock_p1_2d.py) rewritten to ~60 s with two clocks and a late flip, sent for approval.
  timelock_p1_2d.py still holds the first v2 lines: update SCRIPT after approval.

- 27 Oct: owner "Ok go for Halloween we continue thief later auto approved Halloween use studies research reference make
  strong suspense tension video" -> The Seventh Kid, Part 1 (channels/horror/seventh_kid_2d.py, script
  out/horror/scripts_seventh_kid_part1.md). You (Riley) walk six kids trick-or-treating and count seven; two ghosts in
  the sheet you cut for your brother Sam; a note with three rules; the porch lights are the clock; the test "What's my
  name?"; the flip "Sam can't say R"; vote LEFT or RIGHT. New cast in toon2d (riley_bust/riley_back, sam_bust,
  ghost_kid, kid_full, kid_face, breath_fog); sounds crickets/porch_off/whoosh; hud2d.ab_card takes title/ask/letters;
  TAIL 2.0 (the card stays up 2 s, from the reference study).
  Delivered out/horror/seventh_kid_2d.mp4 (66.5 s incl. the 2 s card hold; 194 words, 212 wpm while speaking), Whisper
  medium 22/22, no encoder tags, peak -0.2 dB; thumbnail out/horror/thumbs/seventh_kid.png. Fixed on the way: "trust
  the note" was swallowed (heard "trust in it" / "the left") -> "trust the note on the door"; "cut his eye holes" was
  heard as "eyeballs" -> "cut the holes for his eyes"; the new porch-light snaps, whooshes and the sting peaked at
  0 dBFS -> porch_off 0.3, whoosh 0.25, sting 0.5 for this episode. Part 2 waits for the LEFT/RIGHT vote.

- 27 Oct: Tower 9 Night 2 vote: owner "All said hatch". Night 3 script for approval: out/horror/scripts_night3_tower9.md
  (you open the hatch and your own hand reaches up; the copy at the window vanishes at 4:44; test: page one of the
  logbook; flip: only one reflection; at five base calls; vote: answer the radio, or stay).
- 27 Oct: owner approved Night 3 ("Approved, make it"). Delivered out/horror/tower9_n3_2d.mp4 (63.3 s incl. the 2 s card
  hold; 174 words), Whisper medium 19/19, no encoder tags; thumbnail out/horror/thumbs/tower9_n3.png. Frame 0 adds a
  dark shape already climbing far down the ladder. Fixed on the way: the slam sat on "slam the bolt" (heard "spin") ->
  cued after "bolt."; a breath effect masked "Shut it! Before" -> removed; the bolt sound and the other-you's volume
  boost clipped -> lowered. No viewer comments were sent, so none are shown (never invent them). Night 4 waits for
  the vote: A answer the radio / B stay.
- 28 Oct: Tower 9 Night 3 vote: owner "For tower 9 all said to stay". Night 4 script for approval:
  out/horror/scripts_night4_tower9.md (you let the radio crackle; the other you's watch runs backwards; test: "Who's
  on the radio?" "Someone who answered."; flip: the radio reads page one in your voice; the logbook opens to a last page
  in your handwriting, dated tomorrow; vote: read the last page, or burn the logbook).
- 27 Oct: owner picked "Time Lock Part 1" as the next episode and approved the thief script ("Approved, make it").
  Delivered out/horror/timelock_p1_2d.mp4 (59.5 s incl. the 2 s card hold; 171 words), Whisper medium 20/20, no
  encoder tags; thumbnail out/horror/thumbs/timelock_p1.png. THIS is the Time Lock Part 1 to post; the earlier clerk
  version (timelock_2d.mp4, thumbs/timelock.png) is superseded and must not be posted. Lena's brows now lift with fear
  (they read as anger before). The clue shot (her eyes on the manager's office, a shape behind its frosted glass)
  gets ~1 s via the pause after "presses down."; the far siren stays low under the last lines. Part 2 waits for the
  vote: A mask off / B run.
- 27 Oct: owner "I said it Halloween week so its first": the 7:30 PM slot this week is The Seventh Kid (Part 1 28 Oct,
  then a part a day, finale on Halloween, Sat 31 Oct); Time Lock Part 1 (ready) waits and starts 1 Nov. Tower 9 stays
  at 4:30 PM.
- 27 Oct: The Seventh Kid Part 2 written in both versions for approval (out/horror/scripts_seventh_kid_part2.md): the
  truth is fixed (right ghost = Sam holding his breath, left = the thing, rule 2 was its lie). L: you pull off Sam's
  sheet, then count six kids into the van, the sixth in a sheet holding the little witch's hand (chase or stay). R:
  Sam calls "Wiley!" from the dark, its fingers won't let go, rule 4 on the note's back: never look under its sheet
  (pull it off or leave it on).
- 28 Oct: owner sent a reference Short (84 s: two bags with $20 million, a hidden phone texts "keep one, bring the other
  back", deadline midnight, vote return or keep): "I want story something like for clever psychological tension for
  Nancy story". New series for approval: out/horror/scripts_wrong_number_part1.md (a wrong-number text leads you to
  $50,000 under the bench you sit on every day; the texter says an angry man is coming; flip: the envelope's back says
  "Thank you for coming", so it was never a wrong number; vote: put it back, or keep it). Needs a posting slot.
- 28 Oct 2026: the owner's two stories (channels/stories/) rebuilt in an anime look on this CPU (report: reports/CPU
  anime animation pipeline.md): each character painted once with SD 1.5 Counterfeit-V3.0 (tools/anime_assets.py,
  casts in dma_cast.py / boy_cast.py), cut out, given face patches (expressions, three mouths, blinks where they came
  out clean) and animated as puppets on 24 fps held on 2s (anime2d.py); painted sets (portrait and 16:9); satsuei pass
  (motion/satsuei.py). Every part ends on a cliffhanger into the next (no A/B). Delivered: dma_s1, dma_s2, dma_long,
  boy_s1, boy_s2, boy_long (out/stories/, covers in out/stories/thumbs/), each checked line by line with Whisper medium.
- 28 Oct 2026 (later): owner on the anime look: "Worst animation", then "Make manga like video like showing manga page
  and explaining take manga pages from manga creation chat". DEAD MAN'S ALGORITHM is now made as voiced manga videos
  from the manga creation chat's pages (tejassparky2/Manga, branch ccr-454a96aa-vj1ino, video/chNN/ pages +
  manifest): channels/stories/manga.py zooms panel to panel in reading order (right to left), dims the other panels,
  turns pages; a storyteller narrator (Turbo bm_george) explains, every character speaks their bubble lines in their
  own voice. Episode 1 = Chapter 1 pages 1-7 (dma_manga01, 36/36 Whisper medium). The approved Parts 3-6 script
  (dma_arc_games_1_2.md) was sent to the manga chat to draw as the next chapter(s) (owner: "And update our continue
  story to manga chat"). The anime Parts 3-6 (dma_s3..s6, dma_kit, dma_shots) are shelved, not rendered.
  Episode 1 re-rendered without the horror hum (owner: "Why there is background beez sound"); the manga videos use
  the soft "pad" bed. Episode 2 = Chapter 1 pages 8-14 (dma_manga02, 67 s, 31/31 Whisper medium after two rewordings:
  "Fujimoto" was heard as "The Yumoto" and "Ren" as "Ben", so e3 and e17 drop the names), delivered with its cover.
