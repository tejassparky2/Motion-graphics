# Doctor channel ("Body Facts"): handoff

This branch (`ccr-56282fe5-evehq4-doctor`) is the owner's **second channel**: 2D hand-drawn medical Shorts where
organs are characters and a doctor explains the real fact. The first channel (Interestingly Strange: paradoxes,
weird history, The Last Bencher) lives on `ccr-56282fe5-evehq4` and has its own chat. Keep the two apart: doctor
videos are made, committed and pushed here only.

## NEW FORMAT FROM 24 OCT 2026: English explainers (owner's decision)
The owner sent 9 Hindi reference reels (instagram.com/meanwhilemayank) and asked for "same type of reels but in
English". Decisions (24 Oct): this **replaces** the talking-organs format; voice **Chatterbox Turbo stock female with
tags**; length **75-90 s**; art drawn by us in the vintage-paper style + public-domain Gray's Anatomy (1918) plates;
topics our choice. Voice since 25 Oct: Orpheus "leo" (male, human-sounding; `research_notes/voice_match.md`). Study of the references: `research_notes/explainer_study.md`. First three scripts (snakebite
antivenom, superbugs, malaria) with sources: `research_notes/explainer_1-3.md`; script approval before rendering.
How the explainers are built:
- Look: `motion/paper.py` (paper with creases, FIG header, two-line headline that fills in as it's said, flip
  counter, stamps, stopwatch, vial, microscope, polaroids, India/world maps from Natural Earth, India point-of-view
  boundary). A video lists `SHOTS = {scene: Shot(draw, label, fig, tone, small, big, big_at)}` and its draw() calls
  `P.frame()`. No subtitles (the headline is the only text tied to the voice, like the references). The channel
  logo sits small at the top-left above the header (`P.brand`).
- Voice from 27 Oct (owner: "Change to clear and best voice"): Chatterbox full model, stock voice,
  `NARRATOR = dict(chatterbox=True, tempo_min=1.0, tempo_max=1.0)`. Before that (25 Oct, "O"): Orpheus TTS stock voice "leo",
  `NARRATOR = dict(orpheus="leo", orpheus_quant="q8", tempo_min=1.0, tempo_max=1.0)` (no time-stretching): the Q8
  model (the default Q4 was muddy: "Malaria" heard as "Valeria") + `ORPHEUS_TONE` clarity EQ = "O+", approved
  ("Yeah this is clear"). Orpheus can change words, so it runs at temperature 0.45 with 6 Whisper-checked tries. Setup: `uv venv -p python3.12
  /home/user/.venv-orpheus` + `orpheus-cpp llama-cpp-python soundfile` (CPU wheels from
  https://abetlen.github.io/llama-cpp-python/whl/cpu); ~11x slower than real time on 4 cores. Turbo tags don't apply.
  Earlier tries: Turbo female, then Turbo with am_echo's timbre ("D") (calmer than the story videos' 5.5 syllables/s),
  `gap=0.42` between lines, `MUSIC = "pad"`. Words the voice gets wrong are respelled for speech only:
  `[kright|krait]`. Turbo needs `/home/user/.venv-clone` (chatterbox-tts 0.1.7 + `setuptools<70` for perth);
  the pipeline venv needs `av<16` for faster-whisper.
- Videos: `videos/snakebite.py` (+ `snakebite_shots.py`), `videos/superbugs.py`, `videos/malaria.py`.
- Check stills before rendering, then `tools/render_check.sh <video>` (render + Whisper small + Whisper medium).

Hook and retention rules (from the owner's "shorts" chat on the laptop, 29 Oct 2026; full notes in
`research_notes/from_shorts/` — hooks_from_shorts.md and from_shorts_chat.md, based on all 12 meanwhilemayank reels):
- Line 1 = a contradiction about the viewer, in second person, that is TRUE. Escalate 2-3 times within ~8 s. A reality
  anchor ("This isn't a movie. It's real."). Name the thing by ~12 s, with a short pause before the name.
- Never open on a number, a name, a date or a concept everyone knows (his flops; number/name in line 1 ranked lower).
- Frame 0: one subject, large, already moving; a small setup line + ONE big red word, grey ghost first, red by ~1.5 s.
- Health shape (his rabies reel, 4.6M): "the cure exists, so why do people still die?", re-hook at ~55%, myths struck
  through, a what-to-do list, then a YES/NO comment ending. Re-hook lines at ~40%, 55-60% and 90%. A bookend line.
- A new literal picture every ~3 s, something changing inside it every 0.5-1.5 s; one recurring metaphor (~3 uses).
- Music ~17 dB under the voice in pauses, above 300 Hz, dipping before reveals. Pauses 0.5 s, 0.6-0.8 s only before
  reveals.
- Instagram first (same files did 100-10,000x better there); covers: dark poster, one subject, <=3 words, one big
  coloured word, inside the 3:4 grid crop; caption line 1 = hook + one number (<125 chars); 3-5 hashtags; YT title
  <=60 chars.
- Hook scorers (hookscore etc.) don't predict views for this genre; use these rules instead.

Lessons (25 Oct 2026, owner: "Why you could not catch bug when running from hours"):
- Before a new voice engine goes into a video, read its audio path (how tokens become samples) and test it on 20+
  varied sentences, checking each one's FIRST word. orpheus-cpp's streaming decoder silently dropped the first
  ~0.17 s of every take; it cost hours of retries because the errors were blamed on the model "changing words".
- When Whisper flags the same kind of error in the same place again and again (first words, last words), treat it
  as a bug and investigate before re-rendering; retries can't fix a deterministic fault.

Everything below describes the old format (videos 1-26), kept for reference.

## The old format (videos 1-26)
- First half: organs (and tools) as cute characters arguing about something happening to the body.
- Second half: a hospital scene where the doctor explains what's actually true, with fact cards on screen.
- End on a joke and a question for the comments.
- Inspired by two reference Shorts the owner sent in the first chat (an organ-comedy video and a doctor explaining a
  dark neck patch, acanthosis nigricans). Story, characters and art are always our own.
- Medical facts: general and uncontroversial only, advertiser-safe, no personal medical advice beyond "see a doctor"
  and standard follow-up care. Leave out anything disputed.

## Video 1: done
"He Donated a Kidney... Then His Other Kidney Did THIS" (`videos/kidney_donor.py`).
- Output: `out/kidney_donor.mp4`, upload sheet `out/kidney_donor_metadata.md`. Sent to the owner; not scheduled or
  uploaded yet (ask before scheduling).
- Characters: Lefty and Righty (kidneys), the heart, the scalpel, the doctor, Mike (donor) and Danny (his brother).

## Videos 2-4: brain, nose, liver
Research, sources and the psychology behind the scripts: `research_notes/body_facts_2-4.md`.
- `videos/brain_awake.py`: "They Cut Into His Brain… While He Was AWAKE". The brain can't feel pain; the doctor
  explains awake surgery and where headaches really come from.
- `videos/nose_cycle.py`: "You're Breathing Through ONE Nostril Right Now". The two sides of the nose work in
  shifts (the nasal cycle). The viewer tests it and comments LEFT or RIGHT.
- `videos/liver_regrow.py`: "He Gave Away Half His Liver… Then It Grew Back". Sequel to the kidney video (Danny's
  "half a liver" joke); ends on the callback "Medically? Still yes."
- Shared organ cast (brain, nose tissue, liver lobes, head bandage, fact card, calendar): `motion/organs.py`.
  The heart, scalpel, faces and hospital set are imported from `videos/kidney_donor.py`, so every episode looks
  like the same world.

## Videos 5-6: little-known operations (owner: "not commonly known operations")
Format from the owner's reel (orthotopic neobladder): organs talk during the operation, a "they used WHAT?" twist,
then the doctor names the procedure and explains it. Notes and sources: `research_notes/body_facts_5-6.md`.
- `videos/tooth_eye.py`: tooth-in-eye surgery (osteo-odonto-keratoprosthesis).
- `videos/toe_thumb.py`: toe-to-thumb transfer.
- Scripted and voice-tested for later: high heels and the feet; not drinking water and constipation.
- More little-known operations to consider: hemispherectomy, uterus transplant.

## Videos 7-8: more weird operations
Notes and sources: `research_notes/body_facts_7-8.md`.
- `videos/rotationplasty.py`: the foot turned backwards so the ankle works as a knee (after a bone tumour).
- `videos/fecal_transplant.py`: fecal microbiota transplant (a donor's gut bacteria cure recurring C. diff).

## Videos 9-10: two more weird operations (first with the corner logo)
Notes and sources: `research_notes/body_facts_9-10.md`.
- `videos/half_brain.py`: hemispherectomy (half the brain removed to stop seizures; the other half takes over).
- `videos/forehead_nose.py`: paramedian forehead flap (forehead skin swung down to rebuild the nose, attached
  for about three weeks).

## Video 11: eggs vs multivitamin (fact-check, owner's request)
`videos/egg_vitamins.py`, notes `research_notes/body_facts_11.md`. A viral claim checked by the organs on a
nutrient scoreboard (what five eggs give each organ), then the doctor's answer. Don't name or mock the creator.

## Videos 12-14: hidden body processes (like the nose cycle), owner-approved scripts
Notes and sources: `research_notes/body_facts_12-14.md`. Doctor voice Kokoro `am_adam`.
- `videos/blind_spot.py`: the eye's blind spot, with an on-screen test (cross and dot).
- `videos/morning_height.py`: taller in the morning (spine discs lose and regain water); astronauts +3%.
- `videos/stomach_clean.py`: stomach growling and the migrating motor complex (the gut's cleaning wave).
- The ward scene setup is shared: `ward()` in `motion/clinic.py`.

## Videos 15-18: more hidden body facts, owner-approved scripts
Notes and sources: `research_notes/body_facts_15-18.md`.
- `videos/funny_bone.py` (the ulnar nerve), `videos/stomach_acid.py` (why acid doesn't digest the stomach),
  `videos/goosebumps.py` (the hair muscle), `videos/tickle.py` (why you can't tickle yourself).

## Videos 19-22 and the look to use from now on: REAL ANATOMY, like the owner's references
The owner rejected the polished style for this channel (13 Oct 2026: "doesn't even look like explaining inside the
human body, refer to the reference video"). The references (`/root/.claude/uploads/.../Video-*.mp4`, Dr
Healthcare Shorts) show the real anatomy as a flat, clean cut-away (a womb with placenta and cord, an esophagus with
its veins, an opened knee), googly eyes and a small mouth on the body part that talks, small white name labels, then
the masked doctor and the patient in bed. So:
- Draw the organ scene as an anatomically recognisable cut-away (head in profile with palate/tongue/brain, chest
  with ribs/lungs/heart/diaphragm/stomach/liver, leg with femur/tibia/sciatic nerve/artery, ear with canal/eardrum/
  ossicles/cochlea). Clean style (`STYLE = "clean"`), `motion.engine` shapes, `label()` tags, clean captions.
- Faces go ON the anatomy (`motion.explain.googly`).
- The doctor's part uses `motion.clinic.ward` (masked doctor, Mike and Danny in bed) with the explanation cards from
  `motion/explain.py`: `step_card` (Step 1/2/3), `tip_card` (Do this / See a doctor if), `stamp`, `sign`, placed
  over the bed sheet (y about 690), below the faces and above the captions.
- `motion/pbody.py` (the polished kit) stays in the repo but isn't used for this channel.
- Videos: `videos/brain_freeze.py`, `videos/hiccups.py`, `videos/foot_asleep.py`, `videos/earwax.py`
  (notes and sources: `research_notes/body_facts_19-22.md`).

## Videos 23-26: more hidden body processes (reference style, owner-approved scripts)
Sun sneeze (`videos/sun_sneeze.py`), wrinkly fingers (`videos/wrinkly_fingers.py`), the heart's own electricity
(`videos/heart_spark.py`), contagious yawns (`videos/yawn.py`). Same look as 19-22: anatomy cut-away (head in profile
from `videos/brain_freeze.head`, a fingertip, a four-chamber heart), googly faces on the parts, labels, then the ward
with Step 1/2/3 cards. Notes and sources: `research_notes/body_facts_23-26.md`; upload sheet `out/upload_sheet_batch4.md`.

## Channel name and brand (owner's choice)
The channel is **Doc and the Organs** (tagline "Your organs argue. The doctor explains."). The logo is the owner's
own: `assets/brand/doc_logo.png` (the doctor with his arms crossed among the organs, in a glowing blue circle). Use
it as supplied; don't redraw it. Name, logo helpers and the old heart mascot live in `motion/doc_brand.py`.
- **Every new video (from video 9 on) carries the channel logo** in the top-left corner (the owner's round logo + a
  navy "DOC AND THE ORGANS" tag), plus
  the name faint across the frame: call `watermark(cr)` from `motion/clinic.py` as the last thing in `frame()`.
  Videos 2-8 were made before the logo and stay as released (`watermark(cr, logo=False, name="Body Facts")`):
  the owner wants the logo on future videos only, so never re-render old videos just to add it.
- Brand kit: `python make_doc_brand.py` writes `out/doc_brand/` (avatar, banner, lockup, watermark, preview) and
  `out/doc_brand/channel_about.md` holds the About text, handles, keywords, settings and upload order.
- Upload sheets end with "🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on."

## House style (from the owner's references, videos 2-4)
The owner sent two more reference Shorts (an esophagus with bleeding veins treated by an endoscope; a baby that
stopped growing, taken out by a gloved hand to a NICU incubator) and asked to work "like that". What we took:
- **Clean look:** `STYLE = "clean"` in a video module turns off the hand-drawn wobble, thins outlines, and switches
  text to Anton (OFL, `assets/fonts/Anton-Regular.ttf`).
- **Captions:** one word at a time, uppercase, white with a dark outline, at y=950. The video's `EMPHASIS` set
  makes medical terms bigger.
- **Anatomy tags** instead of handwritten headlines: `motion.clinic.label("Nasal septum", x, y, px, py)`.
- **Doctor's room** (`motion/clinic.py`): plain olive wall, a masked doctor (`person(..., mask=...)`), and patients
  in blue shirts (`mike_b`, `danny_b`) sitting up in bed, in a medium shot with the sheet across the front.
- **Script:** the doctor names the medical term ("This is called an awake craniotomy.").
- **Voices (latest, owner: the pitched-up organ voices "not clear and understandable"):** natural stock voices at
  their own pitch, speed 0.95. Brain/small lobe `af_heart`, scalpel `af_bella`, grumpy organ `am_michael`, sleepy
  nostril `bf_emma`, heart `af_sarah`, Mike `am_fenrir`, Danny `am_puck`. Doctor: the owner's clone at 4.9 syl/s.
  No pitch shifting on dialogue voices. Lines are plain, natural sentences where characters call each other by name
  ("Relax, brain. It's just me, the scalpel."), like the references.
- A faint "Body Facts" watermark, like the references' channel mark.

## Surgery scenes (owner's rule)
The owner wants operations shown fully, like the reference Short (a knee cut open on blue drapes): the body part on
the table, the numbing shot, the cut, the open wound with red tissue and blood, the organ inside with a face, and
clamp characters holding it open. No hiding. Kit: `motion/surgery.py` (drapes, syringe, cut_line, wound, clamp,
forceps, stitches). Keep it in the channel's cartoon style.

## Voices (owner-approved)
- **Doctor (from 5 Oct 2026): Kokoro `am_adam`, the owner's decision ("don't use my voice"); see CLAUDE.md.**
  Videos 2-11 were first made with the doctor in the owner's own cloned voice (Chatterbox, prompt `assets/voice/owner_prompt_fast.wav`, settings in
  `motion/voice.py`: CLONE_RATE, CLONE_TONE, `clone_check`). Only ever clone the owner's own voice.
- **Organs and tools: cute but clear.** The owner first asked for cute voices, then for "clear but cute" after +8 to
  +10 semitones sounded too squeaky. Current settings (in the video's `NARRATOR` cast):
  - Lefty: `af_heart`, pitch +5 · Righty: `bf_emma`, +5 (a different accent so the kidneys sound different)
  - Heart: `af_bella`, +6 · Scalpel: `am_puck`, +7 · all at speed 1.0
  - Pitch shift is rubberband with `formant=shifted` (cartoon tone) and `pitchq=quality` (crisper words).
- Humans (Mike, Danny): `am_michael`, `am_adam`, no pitch change.
- **Videos 2-4 use a new style the owner asked for** (reference Short: a cracked kneecap and the tools fixing it).
  The organ things happen to gets a young male voice raised a little (+2); helpers get a brighter voice raised a
  bit more (+4). Stock voices picked by speaker similarity to the reference, not copies of it: brain and small
  liver lobe `bm_george` +2, working nostril and big liver lobe `bm_daniel` +2, scalpel `af_jessica` +4, heart
  `af_river` +4, resting nostril `af_river` +4 (`formant` stays "shifted"). Every line is exact on Whisper
  medium. One-word takes ("Hey!", "Me?", "Whoa.", "Half?", "Ugh.") get misheard in these voices: fold them into a
  longer sentence ("Hey, who opened the roof?", "What, me?"). Avoid "Shh". Don't use `bf_alice`: it ends every
  sentence with a breathy hiss that Whisper hears as an extra "s" ("Hello agains").
- Made-up words (e.g. "eeny, meeny") get garbled in a high voice: use real words ("And the lucky kidney is... this
  one!").

## Rules (see CLAUDE.md, they apply here too)
- Every sentence ends with a full stop and is voiced as its own take.
- After every render, check every line with Whisper medium: `tools/render_check.sh <video>`. Reword and re-render any
  misheard line.
- Each video ships with an upload sheet (title, alternative titles, description, hashtags, tags, pinned comment).
- No metadata or encoder tags in outputs.
- Layout: the world camera puts its focus at screen y=780 (`motion/kit.py` `ANCHOR`); captions sit at y=915. Keep
  faces above about y=860 on screen and fact cards fully in frame, under the headline.

## Setting up a fresh container
Cloud sessions do this automatically: `.claude/hooks/session-start.sh` (registered in `.claude/settings.json`)
runs the steps below at startup. Lint with `python -m pyflakes <file>`; smoke-test with `python render.py --video X --still 5`.
The voice clone runs in its own Python environment.
```bash
SETUPTOOLS_USE_DISTUTILS=stdlib pip install docopt   # docopt's old setup.py fails on this image without it
pip install -r requirements.txt
python -m venv /home/user/.venv-clone
/home/user/.venv-clone/bin/pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
SETUPTOOLS_USE_DISTUTILS=stdlib /home/user/.venv-clone/bin/pip install chatterbox-tts==0.1.7 faster-whisper soundfile
```
Kokoro, Chatterbox and Whisper models download on first use (about 5 GB). Rendering on this CPU-only cloud machine
takes about 15-30 minutes per video; the owner may later move rendering to a laptop with an NVIDIA GPU (the code
currently forces `device="cpu"` in `tools/clone_tts.py` and in the Whisper calls in `motion/voice.py`).

## Commands
```bash
NARRATOR_ENGINE=kokoro python render.py --video kidney_donor --sheet 1 --out build/sheet.png   # quick layout preview
python render.py --video kidney_donor --still 22.5 --out build/still.png                       # one frame
tools/render_check.sh kidney_donor          # final render + verify + Whisper-medium audit
python tools/redo_takes.py "Exact sentence." # throw away a cached voice take so it's made again
```

## Next
Backup topics already researched (see the notes): the stomach renewing its lining, being taller in the morning, the
funny bone being a nerve. The neck-patch reference suggests a skin or blood-sugar topic too.
