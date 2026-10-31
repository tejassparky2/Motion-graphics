# Q4: the upscale test, Real-ESRGAN anime vs lanczos (helper 4, 31 Oct 2026)

## The bottom line
**Real-ESRGAN is clearly crisper on everything in focus, and about 7.5 s per frame on this 4-core CPU. It also
re-sharpens the tilt-shift blur, which weakens the diorama look.** Recommendation: adopt it at delivery as a **65% ESRGAN / 35% lanczos blend** (option 2 below). The blend keeps most
of the crispness and the miniature softness; the coordinator decides after viewing `okstills/Q4_upscale_blend.jpg`.

## Setup
- **Model:** Real-ESRGAN `realesr-animevideov3`, an open-source project (BSD-3, xinntao/Real-ESRGAN).
  - Weights: `realesr-animevideov3.pth`, 2.5 MB, from the project's own v0.2.5.0 GitHub release. The Hugging Face
    mirror I tried returned 404.
  - Runner: `channels/monsters/tools/esrgan_upscale.py` re-types the network (SRVGGNetCompact), so only torch is
    needed; the realesrgan/basicsr pip packages break on current torchvision. The weights load with
    `strict=True`, so the network matches.
  - Method: 4x, then lanczos down to 1080x1920. This is what Real-ESRGAN's own `--outscale 1.5` does.
- **Baseline:** PIL lanczos, 720x1280 to 1080x1920.
- **Test frames:** from the delivered v2 diorama mp4s (crf 10): S01 f1 (the hook close), S12 f30 (Kai crawling,
  mid-distance) and S24bot f60 (a wide, Kai small).
- **Command:**
  `python channels/monsters/tools/esrgan_upscale.py realesr-animevideov3.pth IN.png ... --out DIR`

## Results
| Frame | Sharpness, lanczos | Sharpness, ESRGAN | ESRGAN s/frame (CPU, 4 threads) |
|---|---|---|---|
| S01 f1 | 23.8 | 112.4 | 10.9 (includes warm-up) |
| S12 f30 | 8.3 | 39.8 | 7.7 |
| S24bot f60 | 10.4 | 37.7 | 7.3 |

Sharpness is the variance of the Laplacian at 1080x1920; higher means crisper edges.

**Crops** (left lanczos, right ESRGAN):
- `okstills/Q4_upscale_crops_A.jpg`: S01 sky, S12 Kai, S24bot Kai.
- `okstills/Q4_upscale_crops_B.jpg`: S01 face, S01 shrimp, S12 blurred foreground.

## What it does to our picture
**Better:**
- The ink outlines are crisp, single-pixel lines instead of a soft ramp. This shows on Kai's face, the cap edge
  and stripes, and the shrimp's outline.
- The eyes and the 2D comic marks (terror eyes, sweat drop) look drawn rather than scaled.
- At phone size the whole frame reads as sharper, closer to a real anime master.

**Worse:**
- **It undoes part of the tilt-shift.** Out-of-focus flower dots, stones and the far grass come back as hard-edged
  flat discs (B, row 3; A, row 3). Kai's own soft blur in the S24bot wide is half-removed. The soft-band falloff
  is our main miniature cue.
- **Fine texture flattens.** The painted grass streaks in the sharp band smooth out into flatter green (A, row 2,
  background). This is the model's cel-anime prior.
- Fine detail on dark areas gets a slight posterised look; I saw no ringing or halos.

## Cost
- **Per frame:** about 7.5 s on 4 CPU threads.
- **Whole episode:** at about 60 s and 1,450 frames, roughly 3 hours on one 4-core machine. It splits across
  machines by frame range like a render.
- **Compared with rendering at 1080x1920 natively:** EEVEE would cost about 2.25x our current 60-75 s per frame,
  or roughly 100 s more per frame. ESRGAN is far cheaper and keeps the 720p renders.

## Options
In every option, upscale the picture before the captions and burn the captions at 1080, so the text stays sharp.

1. **Adopt as is** at delivery, on the final picture, and accept harder bokeh.
2. **Blend, my pick:** 65% ESRGAN + 35% lanczos, at no extra time (`Image.blend`, or ffmpeg `blend=all_opacity`).
   - Tested: `okstills/Q4_upscale_blend.jpg` (lanczos, blend, ESRGAN side by side).
   - Sharpness is 65.9 / 22.9 / 22.9 against lanczos 23.8 / 8.3 / 10.4: about 2.5x crisper.
   - The face lines and comic eyes stay clean, the bokeh dots keep a soft edge, and Kai's blur in the S24bot wide
     stays partly soft.
3. **Keep lanczos** if the coordinator judges the tilt-shift softness more important than line crispness.

My pick is option 2: the line crispness is a large, visible gain on every face, and the blend keeps the miniature
softness.
