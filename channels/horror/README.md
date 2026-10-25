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
- Next (owner, 25 Oct: "Yes do the Quaternius and vrm avatar model test after these"): a 15 s test with Quaternius CC0
  bodies + animations (build/assets3d/uaf: Universal Animation Library 1 and 2, standard, from opengameart.org; 89 clips
  incl. Driving, Idle_Torch, Sitting, Crouch, Hit_Head, Idle_TalkingPhone, ClimbUp, Zombie_Walk) and a VRM face
  (@pixiv/three-vrm; a CC0 or freely licensed VRM model still to find).
