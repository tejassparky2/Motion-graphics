# 2D animation playbook: everything we built, learned and tried (5 Nov 2026)

Written for the Indian mythology chat (owner, 5 Nov 2026: "give all best 2d animations things we did learned explored
skills installed all so far so it know which to use"). Source: the Interestingly Strange chat, branch
`ccr-56282fe5-evehq4` (115+ Shorts since 29 Sep 2026). File paths below are on that branch:
`git fetch origin ccr-56282fe5-evehq4`, then `git show origin/ccr-56282fe5-evehq4:<path>` to read a file, or
`git checkout origin/ccr-56282fe5-evehq4 -- <path>` to copy it into your worktree.

---

## 1. Pick the right route first (the biggest lesson)

The look comes from the drawings and the motion source, not the render engine. We tested this side by side.

| Route | What it gives | Use it for | Cost | Where |
|---|---|---|---|---|
| **A. Code-drawn characters (pycairo)** | Full control and a consistent cast. Any expression, any pose, lip sync, free and unlimited | Talking characters, story beats, debates, explainers. This was the channel's main route | Free; ~70 fps to draw | `motion/toons.py`, `motion/vex2d.py` |
| **B. Polished vector look** | Gradients, soft blurred shadows, glows, bokeh, depth of field, light rays, particles | Divine glow, auras, halos, night skies, magic | Free | `motion/polish.py` |
| **C. Still images brought to life** | Film grade, push-in or drift, grain, flash, glow over still paintings | Painted establishing shots, battle tableaus, temples (stills made by the owner in Gemini/ChatGPT) | Free per frame once the stills exist | `motion/thriller.py` (`shot`, `finish`, `grain`, `flash`, `glow`) |
| **D. One AI character image as a sprite** | Squash, jelly wobble with planted feet, blinks drawn over the eyes, breathing | A mascot made in ChatGPT/Gemini, when you only need small moves | Free | `experiments/mascot_test/vex_test.py`, `vex_ground.py` |
| **E. AI image-to-video (Veo 3.1 / Seedance)** | Smooth full-body moves, real hands, real floor or camera footage | The only way to match "reference" realism (Grim-style mascot reels). Code can't get there | Flow Veo 3.1 Fast ~20 credits per 8 s clip, ~300 credits per 40 s episode; Higgsfield Seedance ~$26 per episode | `research_notes/gary_recipe_higgsfield_2026-11-05.md`, `out/vex3d/LAPTOP_TASK.md` |

**What we measured:**
- The owner compared code-drawn Vex with AI-video mascot reels and said: "Why so small and not looking real and actions
  also don't look real".
- Three agents studied those reels frame by frame. The reels are AI image-to-video over real floor footage. A code
  puppet can't match that motion, however well it is drawn.
- **Use code (A-D)** for stylised 2D storytelling: a consistent cast, exact timing to the voice, no cost.
- **Use AI video (E)** only where realism is the point, and budget for it.

**Remotion + GSAP (tested 29 Oct 2026, `experiments/remotion_gsap/README.md`):**
- Not worth switching. The same scene looked almost identical and rendered about 10x slower (31 s against 2.7 s for
  198 frames). It would also mean rewriting every character in React/SVG.
- Keep Remotion only for one-off browser jobs: Lottie files, heavy text effects, interactive preview.
- Remotion's licence is free only for individuals and companies of up to 3 people. GSAP is free, including commercial
  use.
- **Ideas worth porting into Python:**
  - Elastic and back eases, and wiggle.
  - Letter-by-letter pops.
  - Squash and stretch.
  - Follow-through: hair, cloth and tails lag behind the body.
  - Pupils that react.
  - **Motion blur**: draw each frame at 4-6 in-between times and average them. This was a visible gain on fast moves.

---

## 2. The engine: one Python file per video, everything keyed to spoken words

**Render:**
- `python render.py --video NAME` makes `out/NAME.mp4`, a phone preview and the upload sheet.
- `--sheet N --out x.png` makes a contact sheet. `--still T --out x.png` renders the single frame at T seconds.
- Canvas 720x1280 at 30 fps.
- Output is clean: `-map_metadata -1`, bitexact, no encoder tags. Never strip provenance watermarks such as SynthID.

**A video module (`videos/NAME.py`) defines:**
- `SCRIPT`: a list of beats `dict(id=, scene=, text=, speaker=, tone=, speaker_from=)`.
- `NARRATOR`, `MUSIC` (`"plucks"`, `"pad"`, `"thriller"` or `"none"`), `TAIL` (seconds after the last word),
  `TWIST` (beat id), `SERIES`, `END_TAG`, `METADATA` (upload sheet).
- `draw(cr, t, tl)`, called for every frame.

**Timeline (`motion/timeline.py`): the key to good timing.**
- Every beat is voiced, trimmed and laid end to end. Each sentence is its own take, with a real pause after it:
  - `STOP_PAUSE` 0.24 s after a full stop.
  - `QUESTION_PAUSE` 0.30 s after a question.
  - `BEAT_GAP` 0.24 s between lines.
  - These lengths come from the owner's reference narrators.
- `tl.at("b3", "word")` returns the time that word is spoken. `tl.at("b3", end=True)` returns the end of the beat.
- `tl.scene_at(t)`, `tl.by_id[...]`, and `beat.start`, `.end`, `.audio`, `.speaker` are also available.
- **Every visual change is keyed to a spoken word**, never to hand-typed seconds. Rewording a line then moves the
  animation with it automatically.
- `[spoken|shown]` markup: the voice says the first part and the caption shows the second, e.g. `[ten|10]`. Use it
  for numbers, and for names the voice needs spelled differently.

**Shared kits (pick by need):**
- `motion/engine.py`:
  - Easing: `seg`, `lerp`, `ease_out`, `ease_in`, `back_out`, `pop`, `smooth`, `blink`, `wobble`.
  - Hand-drawn "boiling" lines: `boil`, `shape`, `blob`, `line`.
  - Handwritten text: `write`, `write_t`.
  - `cue(name, t, start)` registers a sound effect at an exact time from inside `draw`.
- `motion/kit.py`:
  - Camera: `camera`, `set_camera`, `enter_world`.
  - **`whip(cr, t, start)`**: a quick push-in on every scene change. Research: every scene needs a slow push-in.
  - Handwritten headline `hl`, `stamp`, `fly` (a prop flying along an arc), `sepia`, `confetti`.
- `motion/polish.py`:
  - Shading: `shade`, `soft_disc`, `soft_rrect`, `ground_shadow`, `vignette`.
  - Atmosphere: `bokeh`, **`light_rays`**, `particles`. Good for divine light.
  - Text and signs: `bold_text`, `sign`, `counter` (ticking numbers), `stamp`, `appear`.
  - Captions and `series_tag`.
  - `sprite(key, w, h, draw)` caches a drawn element (huge speed-up for detailed drawings).
- `motion/pkit.py`: logic cards, `bubble`, `buttons`, red X, `check`, `sparkles`, `shake`, `calendar`, `knot`.
- `motion/rulekit.py`:
  - A big quoted rule `note` (for "one rule" stories: a genie, a curse, a boon).
  - `stone` turns a character to stone.
  - `either_way` draws two branch cards.
- `videos/bq_kit.py`:
  - **`hook2`**: two-tier hook text, small dark setup words plus ONE big red key word, marked as it's spoken.
  - `ring` (a hand-drawn circle mark) and `plain` (plain backdrop).
  - **`talker`**: the speaker's mouth moves only on their own lines.
  - `door`, `two_doors`, `scroll`, `night_sky`, `moon`, `heart_shape`.
- `motion/sets.py`: living room (couch in two layers so people sit IN it), street, kiosk.
- `motion/story.py`: close camera, title cards, quote scrolls, answer buttons.
- `motion/captions.py`: word-by-word kinetic captions, 1-3 words, the spoken word highlighted.

---

## 3. Characters

**`motion/toons.py`: the chibi human cast (big head, small body)**
- `person(cr, t, x, y, s, who=, facing=, eyes=, mouth=, look=, brows=, arms=, walk=...)`, with feet at (x, y).
- `CAST` holds 30+ looks built from skin, hair (spiky, bun, bald, topknot, tonsure, curly, twain), beard, moustache,
  shirt, suit, tunic and toga, in kid or adult build.
- For mythology:
  - Add new entries rather than new code: dhoti, crown, jewellery, skin tones, sacred marks.
  - `tunic=True` and `toga=` already give draped clothes.
- `head`, `portrait` (a circle close-up for reactions).
- Animals: `tortoise`, `crocodile`, `fish`, `jellyfish`, `alien`, `baby_basket`.
- `motion/critters.py`: ant, emu.
- `motion/bees.py`: insects.

**`motion/vex2d.py`: our most advanced puppet (copy its design for a hero character)**
- Signature: `vex(cr, t, x, y, s, turn, lean, squash, tilt, look, eyes, brows, mouth, talk, arms, hold, point, legs,
  walk, cape, blink, blush, tears, lift, rot, pivot, flip, held, idle)`.
- **2.5D head turn**: `turn` slides the features over and tucks the far ear and eye in. One drawing reads as several
  angles.
- **9 eye states**: open, happy, closed, angry, sad, shocked, dizzy, cry, sparkle. Plus brows.
- **10 mouths**: smirk, closed, open, wide, grin, frown, o, wobble, bite, chomp.
- **Lip sync from loudness**: RMS of the character's own audio over 30 ms windows, mapped to 0..1. See `talk()` in
  `videos/vex2d_demo.py`. This is cheap and good enough at Shorts size.
- **Arms by inverse kinematics** to named targets: rest, up, point, out, hips, chin, front, cheek, eyes, wave, down,
  reach. You can also pass any (x, y) target, so hands land exactly on a prop.
- `held(cr)` draws a prop between the face and the hands.
- **Legs**: stand, walk, sit, jump. `lift` gives hops, `rot` with `pivot` gives spins.
- **Cape**: billows and flares (`cape=0..1`). Reuse it for dupattas, angavastrams and banners.
- **Cel shading with a rim light.**
- `idle=0` gives dead-still holds. Idle wobble on every frame reads as "cheap animation".

**Grounding a cartoon on a photo or real background** (`videos/vex_kit.py`):
- `world_layer()` draws everything on the floor into one layer.
- `composite(cr, layer, rim=3.5, shadow=...)` gives the whole layer a thick dark outer rim and ONE soft drop shadow
  falling down-right, with a warm tint.
- This is what makes a 2D figure sit on a real photo instead of floating.
- Feet on one line. A contact shadow under each foot.

**Expression and action vocabulary that sells a beat:**
- `impact` (burst stars), `dizzy` (circling stars), tears, blush, sparkle eyes.
- Shake on hits, squash on landings.
- A spin and land sitting for "knocked back".

---

## 4. Motion craft rules (from measuring the owner's reference videos frame by frame)

- **Frame 0 = one subject, large, on a plain background, already moving.** No busy establishing shot, no fade-in, no
  wide dark opening. Add the set after the hook.
- **A visible change every 1-1.5 s, densest in seconds 3-15**: a new element, a mark, a pose, a card.
  - The hits ran 10-12 changes per 10 s.
  - The number-card reels ran 3-4 and flopped.
- **Slow push-in on every scene** (`kit.whip` or a 1.00 → 1.04 scale over the scene).
- Smooth moves, then **dead-still holds**. The character faces the camera when talking and turns to the other
  character when acting.
- **Props arrive by a dash off-screen and back**, with a whoosh.
- **Anticipation, squash and stretch, follow-through.** Back and elastic eases on pops: `back_out`, `pop`.
- **Hook text in two tiers, fully on screen by ~2 s and timed to the spoken word**:
  - A few small dark setup words.
  - ONE big red key word that carries the contradiction.
  - The key word is marked as it's spoken (strike-through, tick or ring).
  - Never a bare topic word or a number as the headline.
- **Every logic step shown on screen as it's spoken**: a card, chart or counter, kept above the caption band and
  fully in frame.
- **Captions**: 58-64 px at ~71% of the height, so they don't cover faces.
  - Word-by-word style: `motion/captions.py`.
  - Reference "comic" style: Comic Neue ~62 px, white with a black outline, one phrase at a time, hard cut on and
    off (`vex_kit.ref_captions`).
  - Never a caption and a character's speech label on screen at the same time.

---

## 5. Voice (what worked, what the owner rejected)

**English narrator: Chatterbox Turbo, stock female voice, with emotion tags.**
- Settings: `NARRATOR_ENGINE=clone CLONE_MODEL=turbo`.
- Tags: [laugh] [chuckle] [sigh] [gasp] [sniff] [groan] [whispering] [dramatic]. How to use them:
  `out/turbo_tags_research.md`.
- Use one sound tag per line at most, 4-6 per video, placed where a storyteller would make the sound, and none on
  logic lines.
- The owner judged this better than plain voices ("This is better").

**Characters:**
- Each character gets its own voice in `voice.SPEAKERS[name]`. Options:
  - `turbo_ref`: a different Turbo voice.
  - `post_pitch`: semitones up or down with the formants moved, so the voice doesn't sound chipmunked.
  - `babble=True`: cute gibberish for creatures. The meaning goes in the subtitle.
  - Kokoro `voice`, `speed`, `pitch`, `formant`.
- A line that switches from narrator to a character uses `speaker_from`, so there's a pause at the hand-over.

**Hindi (earlier, in this chat):**
- ElevenLabs "Liam" was the owner's pick on 14 Oct.
- Kokoro Hindi and Chatterbox Hindi were rejected ("voice not good").
- Your chat already uses the IndicF5 "Aman" voice, which is newer; keep that.

**Never:**
- Never the owner's cloned voice (owner, 15 Oct 2026). `tools/clone_tts.py` refuses it unless `ALLOW_OWNER_CLONE=1`.
- Never swap the narrator's voice without asking. The owner caught it at once: "Why changed the narrator voice".
- Never use plain untagged takes for emotional lines. The owner's complaint: "voice robotic use tags".

**After every render:** Whisper **medium** on every line (`python tools/audit.py NAME`; it skips babble lines).
- Any line where words merge or get misheard gets reworded and re-rendered.
- Real cases: "No. Your age" was heard as "Know your age", and "Attack Greece" was misheard.
- Name spellings for the voice go in a pronounce map (`PRONOUNCE`, `CLONE_SAY`, e.g. "Pyrrhus" → "Peer-us").
  Sanskrit names will need the same.

---

## 6. Sound (all synthesised in numpy, no samples, no licence issues)

**`motion/audio.py`:**
- Beds:
  - `plucks`: plucks plus sub-bass plus shaker, with a sidechain duck under the voice (20 ms attack, 300 ms release).
  - `pad`.
  - `thriller` (drone).
  - `none` with room tone at -30 dB under the voice. Use this for the "real footage" look.
- `TWIST = "<beat id>"` drops the music under the twist line, with a tick just before it.
- Sound effects, triggered from `draw` with `cue("name", t, start)`:
  - pop, whoosh, hit, thud, slam, fall, step, knock.
  - ding, kaching, tick, ring, buzz, sting, riser, hush.
  - scribble, typing, creak, lock, police, engine.
  - laugh, sniff, gasp_in, whisper_air, heartbeat.
  - musicbox, crunch, poof.
- Rules: **a sound effect on every action**, sound from the first frame, and no dead air.
- For mythology you will probably want new synthesised sounds: a conch, temple bells, a damaru, a tanpura drone and a
  whoosh-glow for divine appearances. Add them in `sfx()` the same way.

---

## 7. Story and hook rules that came from our own analytics (59 Shorts)

**Line 1 is a character asking the impossible question:**
- Stayed-to-watch by opening:
  - A character asking from the first words: ~72%.
  - The narrator setting a scene first: ~62%.
  - Talking to the viewer, a topic statement, "Meet X", "Did you know" or a numbered list: ~47%.
- Line 1 contains the contradiction itself. The narrator's setup comes second, in one short line.
- Open a loop in the first 5 s that only the ending closes.

**Ending:**
- A punchline or a two-sided question as the literal last spoken line, then a hard cut within ~0.2-0.5 s.
- No outro, and no spoken "comment below" or "subscribe".

**Big questions:**
- Hard-to-answer questions held best (the God-rock video: 92% viewed, 70.7% stayed).
- The pattern: the question in a character's mouth, why both answers break, a real thinker's sourced answer, then a
  two-sided closing question.
- **Respectful on religion: argue ideas, never mock believers.**

**Variety:**
- Rotate outcomes and characters. YouTube's inauthentic-content rule bans "the same situation with the same outcome"
  over and over.
- Mix episode types: funny, cute, task/challenge, and sometimes a fact. Never two of the same type in a row.

**Length:** 40-50 s for these Shorts. Clarity first, one step per sentence. Your 2-minute Hinglish format has its own
rules; keep those where they differ.

**Post every Short as an Instagram Reel too.** The reference creator's identical files did 100-10,000x better there.

**Full evidence:**
- `reports/Shorts hooks feeling and subscribers.md` (a 47-rule checklist).
- `reports/Shorts retention for animated explainers.md`.
- `research_notes/meanwhilemayank_deep_dive_2026-10-29.md`.

---

## 8. Mistakes we made (don't repeat them)

- **Matching a reference with the wrong tool.** We spent many rounds polishing a code puppet toward AI-video realism.
  The owner: "very worst don't even matching 1%". Decide route A-E in section 1 first.
- **A glossy "3D vinyl toy" prompt** for a character meant to sit in a flat 2D world. Close-ups showed the reference
  was flat 2D: flat colours, light shading, a clean outline, simple eyes. Match the reference's rendering style in
  the image prompt.
- **Characters floating on photos.** They need a contact shadow per foot, a rim, one directional shadow and a camera
  angle that matches the background ("seen slightly from above" for floor shots).
- **Small, hard-to-read characters.** For phone viewing, the hero should be large. Toy scale (~226 px) only works
  when the shot is built around it.
- **One-sided explanation.** The owner wanted a conversation: "communicating ... not one side explanation". Facts
  come out as answers to a character's question or mistake.
- **Endings that didn't match the reference.** The reference ends on a punchline and a hard cut, not a question card.
- **Captions merging across lines or stranding single words.** Split at sentence ends, merge only within a line, and
  balance two-line captions.
- **Technical traps:**
  - Zero-size props crash cairo (an invalid matrix). Guard with `if s <= 0.01: return`.
  - Blink overlays on wobbling sprites leave seams. Use pixel-aligned slices.
  - Kokoro's phonemiser crashes on nonsense words. Pass explicit phoneme markup.
- **Unsure facts presented as certain.** Quote real, sourced words. For mythology, say "according to the Valmiki
  Ramayana" and similar, and say "often credited to" when the source is unknown.

---

## 9. Tools and skills installed

**Skills in the repo (`.claude/skills/`, they load in any chat working in this repo):**
- **yt-\*** (YouTube): yt-script (hooks from 21 formulas, full script), yt-package (title and thumbnail lint),
  yt-retention (reads a retention export), yt-seo, yt-shorts, yt-viral (what's beating its channel average),
  yt-audit, yt-plan, yt-comment, yt-chapters, yt-edit. Treat their generic advice as a starting point; our own data
  (section 7) wins where they differ.
- **gsap-\*** (8: core, timeline, plugins, react, utils, performance, scrolltrigger, frameworks) and **remotion-\***
  (12: best-practices router, markup, create, render, captions, studio, docs, interactivity, maps, multimedia, saas,
  upgrade). Needed only if you use the browser route (section 1).
- **skill-finder**: searches claude-plugins.dev for a skill when a new domain comes up.

**Tools (`tools/`):**
- `audit.py NAME`: Whisper medium, line by line.
- `verify.py`: quick check with the small model.
- `make_pack.py out/packs FIRST LAST`: an upload pack with the videos plus upload sheets.
- `make_order_pack.py`.
- `el_redo.py VIDEO "sentence"`: throws away one ElevenLabs take.
- `redo_takes.py`.
- `shots.py`: local still images for route C.
- `render_check.sh`.

**Fonts:** `assets/fonts/` (Comic Neue, OFL licence). Check the licence of any new font, including Devanagari and
Kannada fonts (Noto is OFL).

---

## 10. Suggested picks for Indian mythology 2D reels (a recommendation, the owner decides)

1. **Cast**: code-drawn characters (route A) using vex2d's techniques: a 2.5D head turn, IK arms, a mouth from voice
   loudness, a cape used as a dupatta or angavastram.
   - Build each deity or hero once as a function with iconography parameters: skin colour, crown, weapon in `held`,
     extra arms as more IK targets.
   - Then every episode is cheap and on-model.
   - Design original looks. Don't copy a specific comic or TV serial's character art.
2. **Divine moments** with the polish kit (route B): `light_rays` and `soft_disc` glow behind a deity, `particles`
   for sparks or petals, `bokeh` for heaven or night.
3. **Painted establishing stills** (route C), only after the hook: Kurukshetra, Lanka, Kailash. Use a slow push-in
   and grain. Frame 0 stays a single character on a plain background.
4. **Opening**: a character asks the impossible question in line 1, with the contradiction in it. For example: "Why
   did Karna fight for the side he knew would lose?" or "Can Brahma create something he can't lift?"
5. **Hook text** with `hook2`: small setup words, then one red Devanagari or Kannada key word, marked as it's spoken.
6. **Every action gets a sound effect**: synthesise a conch, bells and a damaru in `audio.sfx()`.
7. **AI video (route E)** only for a few hero shots, if the owner wants realism and spends credits on it. The laptop
   chat already has the Flow/Veo steps (`out/vex3d/LAPTOP_TASK.md`).
8. **Respect**: argue ideas, quote the text a version comes from (versions differ between texts and regions; say
   which one), and never mock a deity or a believer.
