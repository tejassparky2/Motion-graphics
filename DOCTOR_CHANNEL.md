# Doctor channel ("Body Facts"): handoff

This branch (`ccr-56282fe5-evehq4-doctor`) is the owner's **second channel**: 2D hand-drawn medical Shorts where
organs are characters and a doctor explains the real fact. The first channel (Interestingly Strange: paradoxes,
weird history, The Last Bencher) lives on `ccr-56282fe5-evehq4` and has its own chat. Keep the two apart: doctor
videos are made, committed and pushed here only.

## The format
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

## Channel name and brand
Suggested name **Organ ER** (tagline "Your organs argue. The doctor explains."). Brand kit: `python make_doc_brand.py`
(`--name "..."` to change it) writes `out/doc_brand/` (avatar, banner, lockup, watermark, preview) and
`out/doc_brand/channel_about.md` (About text, keywords, settings, upload order).

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
- **Doctor: the owner's own cloned voice** (Chatterbox, prompt `assets/voice/owner_prompt_fast.wav`, settings in
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
