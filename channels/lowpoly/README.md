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
