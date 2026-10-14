# Milo thrillers: what keeps people watching (research, 14 Oct 2026)

Owner: "be sure to do deep research on visuals and storytelling to keep the suspense and keep users engaged; the
first hook should hold, they should not swipe away."

## 1. What we measured
- **The owner's reference ("That's Not My Dad", 2:08):** a new shot every **2.1 s** (median, 51 cuts), the camera is
  **never still** (constant drift and sweeps), picture fairly dark (mean brightness 71/255), captions **one to two words
  at a time**, centre screen. Story engine: one wrong detail in the first sentence, then a new clue every 5-10 s
  (wrong chair, black coffee, the dog afraid), a night confrontation with one chilling line, and an ending that calls
  back to the first clue.
- **Our own channel (Sep 29-Oct 11):** openings that drop the viewer into a scene where something is already wrong
  kept 75-78%; topic statements, "Meet X" and cold questions kept 36-52% (CLAUDE.md). Talky explainers stalled at
  ~60% viewed; stories hold.

## 2. What the craft says (sources below)
- **Hook = the strongest moment first**, no intro, no establishing shot; aim for 70%+ still watching at 3 s. The first
  line should leave the brain with something unresolved that takes longer than 3 s to settle (OpusClip, Aibrify).
- **Suspense beats surprise** (Hitchcock's bomb under the table): let the viewer know the danger before the character
  can escape it. Dramatic irony and a **ticking clock** are the fastest tools in a short (Writing Workshops,
  Screenwriter's Utopia).
- **Silence is a weapon:** sound punctuating silence, sudden silence right before the reveal, low-frequency drones and
  rumbles before the threat appears, the hit timed to the exact reveal frame (Indie Shorts Mag, IRPR, Morphic).
- **Jump scares fade, dread lasts:** short-form horror that holds people builds unease with pacing, visual cues and
  sound rather than relying on one scare.
- **End on the protagonist trapped with no way out**, and hand the decision to the viewer (comments).

## 3. How each video applies it
| Rule | In the videos |
|---|---|
| Frame 0 already scary, big hook text | Each opens mid-scene with the hook in big type from the first frame ("MOM NEVER CALLS ME **SWEETIE**") |
| Something wrong in sentence 1 | "Come down for dinner, sweetie. But my mom has never called me sweetie." / "Every night at 3 A.M. ... watching my house." / "Never open the basement door." |
| A new clue or shock every 5-8 s | humming → the text → humming stops → "I can hear you breathing" → footsteps → ringtone under the bed → doorknob |
| Cut about every 2 s, camera never still | 15-16 shots per video + punch-ins; every shot creeps in with a little handheld drift |
| Silence before the shock | a "hush" cue drops all sound for 0.3-1 s before each reveal, then a sting + white flash on the exact word |
| Rising dread | low drone that grows toward the end; heartbeat that speeds up from the midpoint |
| Ticking clock | "You have three seconds" + an on-screen 3-2-1 |
| Viewer decides | DOOR / WINDOW, OPEN IT / PRETEND, "why did he wait?" |
| Same hero every time | Milo, 15, red hoodie (series recognition, like the reference's red-haired kid) |
| Ad-friendly | psychological fear, no gore, nothing graphic |

## 4. Production notes
- Shots: tools/shots.py (DreamShaper 8 + LCM, free, local), sketch-guided with tools/milo_layouts.py so the scary
  detail is where the shot needs it; 2 takes per shot, the better one kept (assets/milo/shots/).
- Look: motion/thriller.py (grade, creep, shake, flicker, grain, vignette, phone/note/choice overlays, red-word
  captions in Anton). Sound: motion/audio.py thriller effects + drone.
- Voice: Chatterbox Turbo with tags; Milo from a younger Kokoro reference (am_puck +3 st).

Sources: [OpusClip hook formulas](https://www.opus.pro/blog/youtube-shorts-hook-formulas) ·
[Aibrify retention curve playbook](https://aibrify.com/blog/youtube-shorts-retention-curve-playbook) ·
[Writing Workshops: 19 ways to create suspense](https://writingworkshops.com/blogs/news/19-ways-to-create-suspense-in-your-plot) ·
[Screenwriter's Utopia: ticking clock](https://screenwritersutopia.com/article/52a249d6) ·
[Indie Shorts Mag: silence and sound in bite-sized horror](https://www.indieshortsmag.com/reviews/2022/03/doors-play-of-silence-and-sound-in-chilling-bite-sized-horror/) ·
[IRPR horror short sound design](https://sounddesign.irpr.agency/work/film-sound-design-horror-short/) ·
[Morphic: jump-scare timing](https://morphic.com/resources/how-to/how-to-make-a-jump-scare-ai-video)
(several are vendor blogs: their numbers are guides, not YouTube data).
