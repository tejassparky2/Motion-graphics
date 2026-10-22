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
Low-poly episodes may run **up to 60 s** (Interestingly Strange keeps its 40-50 s rule).
**Updated the same day** (after episodes 3-6 came out at 30-34 s): "we can make videos upto 1 minutes or more like
more funny more relatable no 40sec limit for this as ItsInterestinglyStrange channel". So: **aim for about 60-75 s**
(Shorts allow up to 3 min), with more escalation beats, more jokes per idea and a stronger build to the last line.
No 40-50 s cap on this channel.
8. **"Forget everything about me"** (60 s, warm/emotional; owner, 18 Oct: "More reference just keep making better"):
   Dev on a beanbag at night, phone glow on his face, asks Claude to forget everything. A **Memory panel** ("4
   things about you": morning person, says please every time, calls Claude "buddy", first message Mar 2025) is the
   story device: items get struck through one by one; "Out of money. It's over. I start a real job Monday."; the last
   item is his first message, "I'm scared. But I want to try." / "I did try." / "You did." / "Keep this one?"; Claude
   quietly keeps "buddy" too. Smooth rounded 3D (not faceted), big glossy eyes, purple hoodie, navy dark with warm
   bokeh, slow pauses, Memory UI as full-screen cut-ins. Lesson: alternate comedy with a warm episode now and then;
   a real product UI (memory, context, usage) can carry the whole story; small true details (a date) sell it.

## Future idea (owner, 18 Oct 2026)
"maybe after few days we might make skit on our own conversation": a skit about this very chat, the owner and the AI
making these videos (references, "revert", "one AI only... no, mix them", "Approved, render it"). Not yet; ask first.

## Writing references (owner sends some for the skit, not the look)
9. **"Daily active users: one"** (54 s; owner, 18 Oct: "Skit reference not visual ref"). Dev and Claude get their first
   real user at 3 AM; it made one note, zero features used: a grocery list and a daily reminder "Did you eat?"; it's
   his mom, who spent 11 minutes on the About page ("Nobody reads the About page." "She did. Twice."); "What do I
   reply?" "The truth. This time." "Eating now." Last line: "Daily active users. One."
   What to learn for our scripts: lines of two to five words traded fast ("A real one?" / "Real email. Real
   human."); a small mystery that unfolds one clue per line; the turn from dev-joke to a human moment at the reveal;
   the last line repeats a dev/startup term with a new, warm meaning; the AI's lines are short and kind, not jokes.

## Posting schedule (owner, 18 Oct 2026)
First "2 videos a day same as ItsInterestinglyStrange", then the same day: "Will go for usa timing first".
**2 videos a day for US viewers: 12:00 PM and 7:00 PM US Eastern = 9:30 PM and 4:30 AM IST** (while the US is on
daylight time; from 2 Nov, when US clocks go back, the same US times are 10:30 PM and 5:30 AM IST). Lunch break and
the evening peak. Schedule the uploads in YouTube Studio so nobody has to be awake at 4:30 AM.
**2-week trial, 19 Oct to 1 Nov 2026**, then move to what this channel's YouTube Analytics shows.
Kept separate from the Interestingly Strange calendar.

## Standing rules from the research (18 Oct 2026; full report: reports/Shorts retention and AI dev humor.md)
Evidence grades in the report: [Data] measured, [Official] YouTube's own words, [Practitioner] sketch teaching or a
primary production text, [Inference]. The short version used on every episode from ep 7 on:
- **Hook:** frame 0 is a character mid-action with something already wrong; line 1 carries the contradiction; the
  on-screen hook text says what the skit then delivers; never a title card, logo, "Meet X" or a bare question.
- **Structure:** one game per episode, statable in one sentence; heighten by specifics, then emotion, then stakes;
  a re-engagement (new rule, reversal or third character) near the middle; one blowout; one-line blackout. Dev,
  the deadline and the bug are normal; only the assistants' one behaviour is strange ("everything but the game").
- **Dialogue:** one idea per sentence, reveal word last, every sentence its own take; a longer pre-gap and a slightly
  slower pace on the blow line; everyone plays it straight (the assistants' cheer stays flat over disasters).
- **Ending:** the punchline is the last spoken line and the video cuts about half a second after it; no outro, no
  spoken subscribe ask; the last line re-uses a word or image from line 1 (a loop point, treated as polish).
  End on a laugh spike or a warm-then-surprise turn, never flat or merely sweet.
- **Cast:** Dev is the straight man whose funny lines are reactions and who carries one quiet feeling line before
  the blow; Claude is the relentless agreer/over-doer; Codex is the blunt refuser/over-reacher. Personalities stay
  predictable, situations and which one is the fool rotate; never the same game twice in a row. Guests (Dad etc.)
  for one episode when the premise needs them.
- **Length:** default 35-50 s; 60-75 s only for a real escalation ladder; never pad. Judge by this channel's own
  stayed-to-watch and first-24-hour views by length (no public data covers 60-180 s Shorts).
- **Upload:** title names the archetype and the situation (<100 chars); "No, it's not made for kids" on every upload
  and dispute any auto-label (cartoon styles get it, and it strips most revenue and all comments); the pinned
  comment carries the two-sided question and the subscribe ask; hashtags optional; never re-upload a deleted Short;
  track engaged views and stayed-to-watch, not the public view count.
- **Policy:** recurring cast is allowed when each video has its own storyline and outcome; animated characters
  with premade synthetic voices need no AI label; never clone a real person. From 1 Feb 2027 Shorts revenue sharing
  needs 10M qualified Shorts views per 90 days, so plan income around subscribers and off-platform, not Shorts RPM.
- **Cadence:** every channel that grew posted daily or near daily with a fixed cheap cast; post the same file to
  TikTok and Reels (YouTube converts skit viewers slowest); read the comments as the writers' room.
- **Unverified claims we do not build on:** "90% fail in the first 3 s", "cuts every 2-4 s", "captions +15-25%",
  "series convert 67% better", "10% replay rate boosts distribution", "500-800 ms pause", "85% watch without sound".

## Catchphrase rationing (owner, 19 Oct 2026: "claude won't say you are absolutely right always")
"You're absolutely right!" at most once every four or five episodes (it was in eps 1, 8, 10 and 11). Claude has
other sides to play: the overconfident fixer ("Fixed!"), the over-doer, the gentle one with outsiders, and the honest
one in warm episodes. Every premise must come from a verified, relatable moment (owner: "I want reliable").

## Emotion tags in every episode (owner, 20 Oct 2026: "Use tags for emotions so it feels human")
- Write Chatterbox Turbo sound tags into the lines: [laugh] [chuckle] [sigh] [gasp] [sniff] [groan] (list and test
  results: out/turbo_tags_research.md). Put a reaction after the line it reacts to; put [gasp] or [sigh] before the
  line. One per line, 4-6 per episode, none on logic lines or the last punchline.
- The render retries a tagged take until Whisper medium hears the words and the sound is there. After the render,
  listen for tags read out as words ("chuckle") and swap any that fail for the breath effects (cue "sigh",
  "gasp_in", "sniff").

## Connection rules (owner, 21 Oct 2026: eps 14-15 "very bad not connecting ... i just want best connecting relatable
emotions feelable"; measured on the references + research_notes/Emotional AI dev skits that connect/)
These replace the old "default 35-50 s" length rule and the reaction-cut-before-every-line habit.
**Owner on batch 5 (eps 16-19, made with these rules), 22 Oct 2026: "This is better".** Keep this form as the default.
- **Pace like the references:** ~90 words a minute overall (refs 84-97; eps 14-15 ran 132-143), 0.6-1.2 s between
  lines, 1.5-2.5 s silent holds on the feeling beats. 60-100 s is fine; length comes from air and story, never padding.
- **Hold shots:** 3-7 s average (refs 3.6-7.5 s); no REACTION_CUTS on emotional episodes; hold on the listener's face.
- **Make me care:** in the first 10 s we learn what Dev wants or stands to lose (grandma's app, the model he talks to
  every night, the joy he lost). A story device on screen (notice, terminal, note, usage report) carries it.
- **Two plus two:** hold back one piece (what the note says) and pay it off; the reveal re-frames what came before.
- **Shape:** jokes first, then the jokes stop; one sincere act or line; the peak is closeness restored; a callback
  laugh last, cut ~0.5 s after.
- **Faces:** BIGEYES + ROUND + HEAD 1.12 (big glossy eyes, rounded heads, like reference 8); EMO entries can carry
  `wet` (glistening eyes) and `tear` (a tear rolls) for the peak; blinks on every new line; breathing in holds.
- **Music:** MUSIC = "score" with SCORE cues (light / tender / out / swell / end): the piano motif comes early, drops
  out before the key line, swells on the payoff (motion/audio.py `score`).
- **Grounded:** every premise comes from a real, sourced moment (developer_emotions.md); stories are fiction, and the
  description says what's real.
