# Motion-graphics

Code-driven 2D explainer animations: a flat cartoon look, "boiling" hand-drawn outlines,
and handwritten captions that write themselves on. Everything is drawn in Python with Cairo.
No After Effects or other animation software is needed.

## The Pumpkin Trick (`out/pumpkin_trick.mp4`)

An 82-second vertical short (720×1280, 30 fps) with a voice-over narrator. It that retells the classic speculator parable:

1. A rich man offers ₹100 per pumpkin (market price is ₹70), and the farmer happily sells 120.
2. He raises the offer to ₹300, and the whole village sells him 500 more.
3. He offers ₹1000, but there are none left. He leaves for the city, and his assistant stays behind to buy.
4. The assistant quietly sells the villagers' own pumpkins back to them at ₹700 each.
5. Neither of them ever returns, and the price crashes to ₹50.
6. Their ledger shows they bought 620 for ₹1.62 L, sold 620 for ₹4.34 L, and made ₹2.72 L profit.

The narration is generated offline with [Piper](https://github.com/rhasspy/piper) text-to-speech (voice `en_US-ryan-high`).
The music and sound effects are synthesized too: a plucked-string loop, pops, scribbles, truck engines and a
cash-register "ka-ching". The music ducks automatically whenever the narrator speaks.

### Changing the narration

The script is the `NARRATION` list at the bottom of `motion/scenes.py`. Each entry says which scene a line belongs to,
when it starts (in seconds from the start of that scene) and what is said. The render prints a warning if two lines overlap or a
line runs past the end. Lines are cached in `build/tts/`, so only edited lines get re-synthesized.

- Different voice: `NARRATOR_VOICE=en_US-lessac-high python render.py` (any [Piper voice](https://huggingface.co/rhasspy/piper-voices) name works; it downloads on first use)
- Slower or faster speech: `NARRATOR_PACE=1.1 python render.py` (above 1 is slower)

## Rendering

```bash
pip install -r requirements.txt
python render.py                 # full video  -> out/pumpkin_trick.mp4 (~1 min)
python render.py --still 12.5    # one frame   -> build/still_12.5.png
python render.py --sheet 1       # contact sheet, one thumbnail per second -> build/sheet.png
python render.py --no-voice      # music + sound effects only
python render.py --no-audio      # silent video
```

ffmpeg comes from the `imageio-ffmpeg` wheel, so you don't need a system install.

## Layout

| File | What it does |
|---|---|
| `motion/engine.py` | Easing and timing, wobbly hand-drawn shapes, handwritten write-on text, sound cues |
| `motion/characters.py` | The cast (Seth, Ramu, Chotu) with poses and expressions, plus the stall, truck, crates, cash and speech bubbles |
| `motion/scenes.py` | The storyboard: one function per scene, plus the `SCENES` timeline |
| `motion/audio.py` | The synthesized music and sound effects, plus the final mix with ducking |
| `motion/voice.py` | The Piper voice-over: downloads the voice, synthesizes and caches each line, builds the narration track |
| `render.py` | Renders frames and pipes them to ffmpeg |

To make a new video, write new scene functions and list them in `SCENES`. Characters take `arms=`, `eyes=`,
`mouth=`, `walk=`, `item=` and similar arguments, so most acting is done by changing arguments over time.

Font: [Kalam](https://fonts.google.com/specimen/Kalam), licensed under the SIL Open Font License (`assets/fonts/OFL.txt`).
