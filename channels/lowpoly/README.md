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
