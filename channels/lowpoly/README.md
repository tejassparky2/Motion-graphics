# Low-poly 3D style test (separate channel, not Interestingly Strange)

Owner, 17 Oct 2026: "make the style test not for this channel its for different channel" (inspired by the
Agent Poly Studios low-poly look; we don't buy or copy their kit or characters).

Original cast: **Kip** (kid, yellow beanie, orange jacket, backpack) and **Orbi** (round floating robot with a dark
visor and glowing eyes). Set: a floating island at dusk with bokeh lights.

- `scene.html`: three.js scene; `window.renderAt(t)` draws an exact frame (emotions: smile, happy, curious,
  surprised, laugh; blink; wave, jump, fist pump; camera push-in).
- `render.mjs`: headless Chromium (headless_shell + SwiftShader) records frames. One-time setup:
  `cd build/lowpoly && npm init -y && npm install three@0.169.0 playwright-core@1.48.2`.
- `make_video.py`: frames + music bed -> `out/lowpoly/style_test.mp4` (8 s renders in about a minute).

## Reference skits the owner sent (17 Oct 2026; @agentpoly, studied for format only, nothing copied)
1. **Codex secret** (55 s, comedy): Claude hits its usage limit mid-fix; Dev secretly asks Codex; "19 files changed,
   38,412 lines added" and it still fails; Claude: "add a semicolon"; it works; Claude finds out ("You've been
   talking to another AI?"). Screen UI cut-ins, "5 HOURS LATER" card, twist ending.
2. **CAPTCHA** (83 s, comedy): Dev keeps failing "select all traffic lights / crosswalks / bicycles / a human";
   the robot passes in 2 s ("Maybe... you're the robot?" "Am I?"). The UI itself is the set.
3. **Am I good enough?** (60 s, emotional): job hunt, "242 applications, 0 replies", Claude reassures him
   ("And I'll always answer you"). Floating platform in space, purple neon edges, holographic panels, slow pauses,
   camera pulls back into space at the end.

What carries all three: one relatable dev pain point, short lines with real pauses, close-ups for reactions,
UI panels as story beats, captions coloured by speaker (Claude orange), a twist or a warm last line.

## Look, sound and camera (owner, 17 Oct 2026: "I want mood and music as reference video camera angles too")
- **Mood:** near-black low-key room, one warm key from the side, the big monitor glowing behind Claude and Codex,
  shallow depth of field (BokehPass), vignette and light grain.
- **Music:** `bed="pad"` in motion/audio.py: slow pad chords and a mellow electric piano with room reverb, quiet,
  key and progression set per episode; `hush` cues drop it out for punchlines (the comedy reference uses silence).
- **Camera:** eye level for the desk characters, 3/4 medium shot of Dev from the front-left, over-the-shoulder shot
  past Dev's head, close-ups for punchlines, high wide shot from behind Dev. Presets in scene_skit.html `SHOTS`.
4. **Campfire confession** (67 s, warm comedy): the kid admits using ChatGPT ("You said delve twice yesterday"),
   phone insert "11 chats", ends "Paste the code." Firelight key + moonlight fill, floating embers, very shallow
   focus, shot-reverse-shot close-ups, wide shots only to open/close; small clean white captions; quiet sustained
   chords (5-6 s each) over a constant fire-crackle ambience, music drops out once for a beat.

Applied to our look: small clean speaker-coloured captions (all four references use them), warm dust motes in the
light, slower pad chords, and a room tone that keeps going when the music drops out.
