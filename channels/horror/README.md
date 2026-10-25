# Interactive horror Shorts in 3D (separate channel)

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

## Status
- 25 Oct 2026: channel opened; waiting on the owner for the name, narrator voice, part-2 timing and premise pick.
