# Motion-graphics

Code-driven 2D explainer animations: a flat cartoon look, "boiling" hand-drawn outlines,
and handwritten captions that write themselves on. Everything is drawn in Python with Cairo.
No After Effects or other animation software is needed.

## The Pumpkin Trick (`out/pumpkin_trick.mp4`)

A 71-second vertical short (720×1280, 30 fps) that retells the classic speculator parable:

1. A rich man offers ₹100 per pumpkin (market price is ₹70), and the farmer happily sells 120.
2. He raises the offer to ₹300, and the whole village sells him 500 more.
3. He offers ₹1000, but there are none left. He leaves for the city, and his assistant stays behind to buy.
4. The assistant quietly sells the villagers' own pumpkins back to them at ₹700 each.
5. Neither of them ever returns, and the price crashes to ₹50.
6. Their ledger shows they bought 620 for ₹1.62 L, sold 620 for ₹4.34 L, and made ₹2.72 L profit.

The soundtrack is synthesized too: a plucked-string loop with pops, scribbles, truck engines and a cash register "ka-ching".

## Rendering

```bash
pip install -r requirements.txt
python render.py                 # full video  -> out/pumpkin_trick.mp4 (~1 min)
python render.py --still 12.5    # one frame   -> build/still_12.5.png
python render.py --sheet 1       # contact sheet, one thumbnail per second -> build/sheet.png
python render.py --no-audio      # skip the soundtrack
```

ffmpeg comes from the `imageio-ffmpeg` wheel, so you don't need a system install.

## Layout

| File | What it does |
|---|---|
| `motion/engine.py` | Easing and timing, wobbly hand-drawn shapes, handwritten write-on text, sound cues |
| `motion/characters.py` | The cast (Seth, Ramu, Chotu) with poses and expressions, plus the stall, truck, crates, cash and speech bubbles |
| `motion/scenes.py` | The storyboard: one function per scene, plus the `SCENES` timeline |
| `motion/audio.py` | The synthesized music and sound effects |
| `render.py` | Renders frames and pipes them to ffmpeg |

To make a new video, write new scene functions and list them in `SCENES`. Characters take `arms=`, `eyes=`,
`mouth=`, `walk=`, `item=` and similar arguments, so most acting is done by changing arguments over time.

Font: [Kalam](https://fonts.google.com/specimen/Kalam), licensed under the SIL Open Font License (`assets/fonts/OFL.txt`).
