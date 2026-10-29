# Remotion + GSAP test (29 Oct 2026)

Owner: "Intall both of it and see if this useful to upgrade our animation" (github.com/greensock/gsap,
github.com/remotion-dev/remotion).

## What was done
- Installed `gsap@3.15.0` and `remotion@4.0.539` (+ `@remotion/cli`, React 19) here, outside the Python pipeline.
- Remade the first 6.6 s of row 77 (toxo_rat) in Remotion + GSAP (`src/RatHook.tsx`): the same layout, voice, music
  and word times (`src/words.json`, exported from our timeline), so only the engine differs. It uses one paused GSAP
  timeline seeked to each frame (deterministic), with DrawSVG for the strike-through, CustomWiggle for the shiver,
  elastic/back eases, SVG gradients and blur filters, and real browser text for the hook and captions.
- Rendered with the pre-installed Chromium:
  `npx remotion render src/index.ts RatHook out/rat_hook.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell --concurrency=2`
  (first `npm install`; regenerate `public/rat_open.wav` from `out/toxo_rat.mp4`, first 6.6 s).
- `compare_rat.png`: top row pycairo (our render), bottom row Remotion + GSAP, at 0, 2.2, 3.65, 5.0 and 6.0 s.

## Results
| | pycairo (now) | Remotion + GSAP |
|---|---|---|
| Look | the same drawings | the same drawings (+ soft shadow, gloss) |
| Speed, 198 frames | 2.7 s to draw | ~31 s to render (+ ~10 s bundling), 2 Chromium tabs |
| Ready-made helpers | our kit (polish, pkit, toons, bq_kit) | GSAP eases, DrawSVG, MorphSVG, SplitText; Remotion Lottie, captions, Studio preview |
| Voice, music, Whisper checks | built in | stay in Python; Remotion would only receive words.json + audio |
| Our 100+ videos, characters (toons.py) | all here | would all need porting to React/SVG |
| Licence | ours | GSAP: free incl. commercial (standard no-charge licence). Remotion: free for individuals and companies of up to 3 employees; bigger companies need a paid company licence |

## Verdict
Not worth switching the pipeline. The two clips look almost the same because the look comes from the drawings, not
the engine; Remotion is ~10x slower here and would mean rewriting every character and helper. What is worth taking:
- GSAP's motion ideas, ported into our Python kit in a few lines each: elastic and wiggle eases, letter-by-letter
  pops, squash and stretch, follow-through (tails, hair, ears lagging behind), pupils that react.
- Remotion stays installed for one-off jobs where a browser wins: Lottie animations, heavy text effects or an
  interactive preview.
