# Motion-graphics

Code-driven 2D explainer animations: a flat cartoon look, "boiling" hand-drawn outlines,
and handwritten captions that write themselves on. Everything is drawn in Python with Cairo.
No After Effects or other animation software is needed.

## The Pumpkin Trick (`out/pumpkin_trick.mp4`)

A 49-second vertical Short (720×1280, 30 fps). It retells the classic speculator parable with original characters: a rich
man inflates the price of pumpkins, and his assistant sells the villagers' own pumpkins back to them before the price crashes.

It is built for retention, following the research in [`reports/Shorts retention for animated explainers.md`](reports/Shorts%20retention%20for%20animated%20explainers.md):

| | This video | Target from the research |
|---|---|---|
| Hook | Frame 0 shows a ₹1000 note beside a ₹70-tagged pumpkin, with the question *"Why would a rich man pay ₹1000 for a ₹70 pumpkin?"* | Conflict and a question in the first 1–2 s |
| Speech rate | ~239 wpm while speaking | 200–240 wpm |
| Dead air | Longest silence in the voice track: 0.22 s. Speech covers 94% of the runtime | Gaps ≤0.25 s, coverage ≥90% |
| Visual change | One every 0.97 s (measured with ffmpeg scene detection), never more than 2 s without one | ~1 s (the reference Short measured 0.92 s) |
| Numbers | Every price is handwritten on screen on the spoken word | On-word number pops |
| Captions | Word-by-word, 1–3 words, current word highlighted | Kinetic captions in the safe zone |
| Ending | Payoff, one line, then back to the hook frame: *"...ask yourself:"* flows into *"Why would a rich man..."* | Loop ending, no outro |
| Mix | −14 LUFS, −1 dBFS peak. 124 BPM music ~22 dB under the voice; heavy hits only on the plot turns | Same |

The narration is generated offline with [Piper](https://github.com/rhasspy/piper) text-to-speech (voice `en_US-ryan-high`).
Word timestamps come from [faster-whisper](https://github.com/SYSTRAN/faster-whisper) run over the synthesized speech.
**The whole video's timing follows the voice.** Each line is synthesized and trimmed, and its internal pauses are capped
at 0.22 s. The lines are then laid end to end with 0.15–0.3 s gaps, and every animation beat is keyed to *the moment a word is spoken*.

### Changing the script

The script is the `SCRIPT` list at the top of `motion/scenes.py`. `[spoken words|shown]` says one thing and shows another
in the captions, e.g. `[a hundred rupees|₹100]`. Scenes find their timing with `tl.at("v3", "₹12,000")`, which returns the
moment that number is spoken. If you edit a line, everything keyed to it moves with it. Lines are cached in `build/tts/`.

- Different voice: `NARRATOR_VOICE=en_US-lessac-high python render.py` (any [Piper voice](https://huggingface.co/rhasspy/piper-voices); it downloads on first use)
- Faster or slower speech: `NARRATOR_PACE=0.75 python render.py` (Piper length scale; below 1 is faster, and the default is 0.8)

## Rendering

```bash
pip install -r requirements.txt   # the first render also downloads the Piper voice and a Whisper model
python render.py                 # full video  -> out/pumpkin_trick.mp4
python render.py --still 12.5    # one frame   -> build/still_12.5.png
python render.py --sheet 1       # contact sheet, one thumbnail per second -> build/sheet.png
python render.py --no-voice      # music + sound effects only
python render.py --no-audio      # silent video
```

ffmpeg comes from the `imageio-ffmpeg` wheel, so you don't need a system install.

Every render also writes `out/pumpkin_trick_preview.mp4`, a smaller copy for phones. Both files are written with all
container metadata removed: no encoder or version tags and no x264 settings block. Nothing in this pipeline adds a
watermark in the first place. The frames are drawn by Cairo, the voice comes from Piper, and the music and sound effects
are generated with numpy.

## Layout

| File | What it does |
|---|---|
| `motion/engine.py` | Easing and timing, wobbly hand-drawn shapes, handwritten write-on text, sound cues |
| `motion/characters.py` | The cast (Seth, Ramu, Chotu) with poses and expressions, plus the stall, truck, crates, cash and speech bubbles |
| `motion/scenes.py` | The script (`SCRIPT`) and the scenes, keyed to spoken words; camera punch-ins |
| `motion/timeline.py` | Narration-driven timeline: synthesizes lines, lays them end to end, answers "when is this word spoken?" |
| `motion/captions.py` | Word-by-word kinetic captions |
| `motion/audio.py` | The synthesized music and sound effects, plus the final mix with ducking |
| `motion/voice.py` | Piper voice-over: synthesis, silence trimming and pause squeezing, Whisper word timestamps, the narration track |
| `render.py` | Renders frames and pipes them to ffmpeg |

To make a new video, write a new `SCRIPT` and scene functions keyed to it with `tl.at(...)`. Characters take `arms=`, `eyes=`,
`mouth=`, `walk=`, `item=` and similar arguments, so most acting is done by changing arguments over time.

Font: [Kalam](https://fonts.google.com/specimen/Kalam), licensed under the SIL Open Font License (`assets/fonts/OFL.txt`).
