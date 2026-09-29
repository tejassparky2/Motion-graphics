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

The narration is generated offline with [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) text-to-speech (Apache-2.0),
using the voice `am_michael` at speed 1.2. The voice was picked by measuring the candidates against the reference Short's narrator.
At about 225 wpm it transcribed 100% correctly, and its pitch variation (3.7 semitones SD, 8.8 range) is close to the reference's
(3.1 SD, 8.0 range). The previous Piper voice swung much wider (4.6 SD, 11.6 range). Other voices are compared in
`out/voice_samples.m4a`: `am_michael`, then `af_heart`, then `bm_george`. Hook, twist and payoff lines are read slightly
slower (`pace=` in `SCRIPT`) for emphasis. "Lakh" is given its Indian-English pronunciation ("laakh") with a phoneme
override in `motion/voice.py`.
Word timestamps come from [faster-whisper](https://github.com/SYSTRAN/faster-whisper) run over the synthesized speech.
**The whole video's timing follows the voice.** Each line is synthesized and trimmed, and its internal pauses are capped
at 0.22 s. The lines are then laid end to end with 0.15–0.3 s gaps, and every animation beat is keyed to *the moment a word is spoken*.

### Changing the script

The script is the `SCRIPT` list at the top of `motion/scenes.py`. `[spoken words|shown]` says one thing and shows another
in the captions, e.g. `[a hundred rupees|₹100]`. Scenes find their timing with `tl.at("v3", "₹12,000")`, which returns the
moment that number is spoken. If you edit a line, everything keyed to it moves with it. Lines are cached in `build/tts/`.

- Different voice: `NARRATOR_VOICE=af_heart python render.py` (any [Kokoro voice](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md); British voices start with `b`)
- Faster or slower speech: `NARRATOR_SPEED=1.3 python render.py` (the default is 1.2; higher is faster)
- The old Piper voice: `NARRATOR_ENGINE=piper python render.py`

## Episodes

Each video is one file in `videos/`. It holds the script (`SCRIPT`), the scenes (`draw`), an optional narrator
override (`NARRATOR`), and the upload sheet (`METADATA`: title, alternative titles, description, hashtags, tags,
pinned comment). Every render writes three files to `out/`:

- `<name>.mp4`: full quality
- `<name>_preview.mp4`: a small copy for phones
- `<name>_metadata.md`: the upload sheet, ready to paste into YouTube Studio

| Episode | File | Length |
|---|---|---|
| 1. The Pumpkin Trick | `videos/pumpkin_trick.py` | 51 s |
| 2. The $5 Lucky Charm | `videos/lucky_charm.py` | 35 s |

```bash
python render.py --video lucky_charm
```

Shared shot tools (camera moves, headlines, stamps, flying props, sepia flashbacks, confetti, whip transitions)
live in `motion/kit.py`.

**Channel narrator:** Kokoro `am_fenrir` at speed 0.95. It is a stock voice picked to match the delivery of a reference
narrator the channel chose (speaker similarity 0.72, the best of 12 voices; similar pitch and expressiveness). It is
a style match, not a clone of anyone's voice.

## Rendering

```bash
pip install -r requirements.txt   # the first render also downloads the Piper voice and a Whisper model
python render.py --video lucky_charm   # full video -> out/lucky_charm.mp4 (+ preview + upload sheet)
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

## Brand: Interestingly Strange (`out/brand/`)

The mascot is a curious one-eyed creature. Its curled antenna and round body together form a **question mark**, and one
raised eyebrow gives it an "hm, that's odd" look. It's drawn with the same hand-drawn helpers as the videos
(`motion/brand.py`), so it can be animated in intros and appear in episodes. The palette is purple on sunflower yellow,
with ink outlines.

| File | Use |
|---|---|
| `avatar.png` / `avatar.svg` | Profile picture, 800×800. It is designed for the circle crop and still reads at 40 px |
| `mark.png` | Mascot alone on transparent, for thumbnails and watermarking your own videos |
| `lockup_light.png` / `lockup_light.svg` | Mascot + wordmark for light backgrounds |
| `lockup_dark.png` | The same for dark backgrounds |
| `preview.png` | How it looks at real YouTube sizes on light and dark themes |

Regenerate with `python make_logo.py`.
