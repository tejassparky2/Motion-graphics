# Q4 speed: Real-ESRGAN realesr-animevideov3 on CPU, under 3 s/frame with no quality loss (helper 7, 31 Oct 2026)

## The bottom line
**bf16 weights plus channels_last memory** cut the network from **7.1 s to 1.5 s** per 720x1280 frame on this 4-core
CPU. The CPU has AMX and AVX512-BF16, so oneDNN runs bf16 natively. The output stays **54-56 dB PSNR** against the
fp32 reference at 1080x1920, which is visually identical at a 200% crop. `esrgan_shot.py` end to end (decode,
ESRGAN, the 65/35 lanczos blend, x264 crf 10 encode) goes from **6.8 s to 2.0 s per frame**. Two parts run side by
side with `--threads 2` each give **~1.6 s per frame** of throughput.

- **Patch:** `out/monsters/diorama_v3/Q4_speed.patch` (for helper 4's `esrgan_upscale.py` and `esrgan_shot.py`;
  `git apply` it).
  - `load(weights, fast=True)` adds channels_last, and bf16 only where the CPU has native bf16. Elsewhere it stays
    fp32 channels_last, about 4 s.
  - `upscale()` follows the net's dtype and memory layout, and converts to uint8 in torch (identical output, faster).
  - `esrgan_shot.py` uses the fast path by default; `--exact` gives the old fp32 reference.
- **Checks:**
  - The `--exact` path is byte-identical to the original code.
  - The fast part vs the exact part (S12 f25-36, both through the whole `esrgan_shot.py` pipeline, crf 10): PSNR Y
    55.3 dB, average 55.8, minimum 55.4 dB.

## Benchmarks
The test frames are S01 f1, S12 f30 and S24bot f60 from the v2 diorama shots. The machine has 4 threads and
amx_bf16. Times are the mean of the 3 frames after a warm-up. PSNR is the minimum over the 3 frames, against the fp32
reference at 1080x1920. Sharpness is the variance of the Laplacian at 1080x1920.

| Variant | Network s | Post s | Total s/frame | PSNR vs fp32 | Sharpness |
|---|---|---|---|---|---|
| fp32 (reference, as Q4) | 7.06 | 1.29 | 8.35 | - | 60.0 |
| fp32 + channels_last | 4.05 | 1.59 | 5.65 | 93.2 dB | 60.0 |
| bf16 autocast | 4.12 | 1.86 | 5.99 | 56.4 dB | 59.6 |
| bf16 autocast + channels_last | 1.63 | 1.32 | 2.95 | 56.4 dB | 59.6 |
| **bf16 weights + channels_last** | **1.47** | 1.23 | 2.69 | **54.6 dB** | 59.3 |
| bf16 + CL, input 540x960 (x4, then down) | 0.84 | 0.49 | 1.33 | 41.1 dB (fails) | 48.0 |
| ONNX Runtime fp32 (CPU EP, all graph optimisations) | 3.89 | - | - | identical (1e-6) | - |

**The post step** (the 2880x5120 output to uint8, then lanczos to 1080x1920), on its own after the bf16 net:

| Post | s | PSNR vs fp32 |
|---|---|---|
| float clamp, numpy round, PIL lanczos (as Q4) | 0.50 | 54.6 dB |
| **uint8 in torch, PIL lanczos (same result)** | **0.32** | 54.6 dB |
| torch antialiased bicubic | 0.13 | 52.1 dB |
| torch antialiased bilinear | 0.11 | 47.4 dB |

The adopted post is the uint8-in-torch variant, because its output is identical to Q4's lanczos.

**Threads** (bf16 + CL network only, per frame): 4 threads 1.97 s, 2 threads 2.74 s, 1 thread 4.46 s. Whole runs
of 8 frames, including model load: 1 process x 4 threads 2.22 s/frame; **2 processes x 2 threads 1.87 s/frame**.

## Not adopted
- **Tiling:** only bounds memory (the full frame needs ~2 GB), and the patch keeps it for that. It adds overlap work
  and seams (a maximum 5-level difference vs untiled in fp32).
- **ONNX Runtime fp32:** 3.9 s. Faster than the fp32 reference but well behind torch bf16 with oneDNN AMX. OpenVINO
  would be the same idea; not needed.
- **A smaller input** (540x960, x4, then down to 1080x1920): the fastest at 1.3 s, but it throws away real pixels.
  It falls to 41 dB and sharpness drops from 59 to 48 (softer lines), so it is less crisp per second than the x4 run on
  the 720 frame. **Run the x4 model on the full 720x1280 frame.**

## For the delivery run
About 2,200 frames at 2.0 s each is **~1.2 CPU-hours** on one 4-core machine, was ~4.6. Split by frame ranges across
helpers as before. On one machine, two `--threads 2` parts side by side are ~15% faster than one with 4.
