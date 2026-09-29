# Sparky3dcraft – "Mini Me" motion-graphics ad

A 33-second vertical (9:16, 1080×1920, 30 fps) video ad for Sparky3dcraft's multi-colour 3D printed Mini Me miniatures, printed on the Snapmaker U1.

**▶ Ready-to-upload video:** [`video/sparky3dcraft-minime-9x16.mp4`](video/sparky3dcraft-minime-9x16.mp4)
**Why it's built this way (research and sources):** [`RESEARCH.md`](RESEARCH.md)

| Time | Scene | On screen |
|---|---|---|
| 0–3 s | Hook | "Wait… is that YOU?" and a Mini Me pops in and waves |
| 3–7 s | Feeling | "Your best moments… are stuck in your camera roll." |
| 7–11 s | How it works | ① Send us one photo → ② We sculpt your Mini Me |
| 11–19 s | Proof | Multi-colour printing: 4 toolheads (T1–T4) swapping, layer by layer |
| 19–24 s | Reveal | "Made from YOUR photo": your hairstyle / outfit / smile |
| (+3 s) | Real prints | Shown only if you add real photos (see below) |
| 24–28 s | Gift | "A gift that says 'I see you.'" plus occasions |
| 28–33 s | Call to action | Sparky3dcraft: "Send us your photo ➜" |

## Change the text, colours or photos

Edit **one file**: [`src/config.ts`](src/config.ts). It holds every word, your handle/website, the 4 filament colours and the real-photo list.

- Add your Instagram handle or website: `brand.handle = '@yourhandle'`
- Add real proof photos: copy them into `public/photos/`, then set
  `realPhotos = ['photos/one.jpg', 'photos/two.jpg', 'photos/three.jpg']`
- Only if you show customers a 3D preview before printing: `showPreviewApproval: true`

Then re-render (below).

## Render the video yourself

Needs Node 18+ and Python 3 with numpy.

```bash
npm install
npm run audio      # regenerates public/music.wav (re-run after changing photos/timings)
npm run render     # -> out/sparky3dcraft-minime-9x16.mp4
npm run studio     # live preview & scrubbing in the browser
```

Files: scenes are in `src/scenes/`, the figure/printer drawings are in `src/components/`, and scene timings are in `src/timeline.json`.

Built with [Remotion](https://www.remotion.dev/). Remotion is free for individuals and companies with up to 3 employees; check their licence if you grow beyond that. The fonts (Fredoka, Nunito) are open source (SIL OFL). The music is original and synthesised by `scripts/make_music.py`, so it is royalty-free.
