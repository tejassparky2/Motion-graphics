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

## Owner, 18 Oct 2026: one AI per video, funny like references 5 and 6
"I always don't want both claude and codex together in videos" and "Funny like this". Clarified the same day: "I don't
want always only claude or always only codex, both can mix, both can be different, we do everything possible".
**Rule: vary the cast.** Some episodes Dev + Claude, some Dev + Codex, some all three; don't fall into one fixed
format. Episode 1 (code review) and the ep02 draft
used both, so the channel's first reel is a new one-AI episode 1 (scripts/ep01_absolutely_right.md).
5. **Usage meter** (51 s, comedy): Dev and Claude only, night city window. Running visual gag: a "Usage %" card
   ticks up on every line while Dev watches it "like a taxi meter"; tiny deadpan lines ("Seventeen." "Thinking.");
   twist: usage resets to 0% and Dev instantly says "Claude. Fix every button!"
6. **Mushroom** (57 s, dark comedy): a kid and one chatbot robot in a bright low-poly forest. The bot says "Great
   question!", confidently calls the mushroom safe, the kid turns green and becomes a ghost, then "You're absolutely
   right! I apologize for the confusion." and a cheerful "5 mushrooms you should never eat" list as the punchline.
What makes them funny: one recognisable AI habit pushed further on every line, a running visual gag (a meter, a
card), very short deadpan replies with real pauses, and a last line that shows nothing was learned.
7. **Train / "I'm switching to Codex"** (53 s, comedy; owner, 18 Oct: "1 more reference please adapt"): Dev and
   Claude on a night train; Codex appears **only as a chat panel** ("Hey! 👋 Want me to take this one?"), never as a
   character. Navy-blue night with warm key light and blurred city lights behind; realistic coding-agent tool-log
   panels (Read / Edit / Write / Bash rows with +/- counts, "✓ 12 passed", an orange "Running tests…" line); small
   white captions above the characters. Adapted from episode 1 (new): `MOOD = "night"` (navy room, city window
   behind Dev), the lived-in desk (`DETAILS`), tool-log cards and small white captions in the upper middle.

## Length (owner, 18 Oct 2026): "we can go duration upto 60 seconds only for this channel"
Low-poly episodes may run **up to 60 s** (Interestingly Strange keeps its 40-50 s rule). Never over 60 s.
