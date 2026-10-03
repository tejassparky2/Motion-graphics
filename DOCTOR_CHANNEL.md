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
  liver lobe `bm_george` +2, working nostril and big liver lobe `bm_daniel` +2, scalpel `bf_alice` +4, heart
  `af_jessica` +4, resting nostril `af_river` +4 (`formant` stays "shifted"). Every line is exact on Whisper
  medium. One-word takes ("Hey!", "Me?", "Whoa.", "Half?", "Ugh.") get misheard in these voices: fold them into a
  longer sentence ("Hey, who opened the roof?", "What, me?"). Avoid "Shh".
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
