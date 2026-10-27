# AI video generation, frame interpolation and upscaling for an anime pipeline on a CPU-only machine (plus the owner's RTX 3050 4 GB laptop)

Target machine: Linux, 4 vCPU Intel Xeon @ 2.10 GHz (Sapphire Rapids class: AVX-512, AVX512_BF16, AMX_BF16/AMX_TILE), ~15 GB RAM (5-10 GB actually free while other jobs run), 2.8-8 GB free disk (it moved between 5.0 and 8.8 GB while I worked), no GPU. The pipeline renders vector frames with pycairo at 30 fps.

**How the local measurements were taken (27 Oct 2026, this machine).** I downloaded the upstream release binaries and weights and timed them. Scripts are in `/tmp/claude-0/-home-user-Motion-graphics/ce9fa840-85fb-5cb2-9994-edff6b8c5245/scratchpad/bench/scripts/`: `runtime.py` (wall time + peak RSS), `esr_torch.py`, `ov_bench.py`, `vgen_step.py` and `cairo_bench.py`. I deleted the 1.3 GB venv and the unused RIFE models afterwards. Test frames are two consecutive frames of `out/backbencher.mp4` (720x1280, a 2D Short), resized with Lanczos to 360x640, 540x960 and 1080x1920.
- **Contention:** other agents were running Blender, a TTS job and Python jobs, so load average was 2-10 on 4 cores. Where a test was run twice I give both numbers: the lower one is the "quiet" figure, the higher one was taken under contention. Every local number below is labelled **[LOCAL]**. They come from the scripts above, not from a URL.
- **Video-diffusion step timings:** for AnimateDiff and Wan I built the real architectures from their official Hugging Face `config.json` files with **random weights**. No multi-GB checkpoints were downloaded. I timed one denoising forward pass in bf16, which uses all 4 threads and AMX. Compute cost does not depend on the weight values, so per-step time matches a real run. Total clip times are my **[ESTIMATE]**s built from those per-step times.

## 1. AI video generation on CPU (AnimateDiff / Lightning / AnimateLCM, Wan2.1 1.3B / Wan2.2 5B, LTX-Video, CogVideoX, HunyuanVideo, SVD, ToonCrafter, AnimateAnyone / MimicMotion / UniAnimate)

### Takeaway
No published source reports a usable CPU-only run of any of these models, and every official requirement is stated as GPU VRAM. My own step timings on this 4-core Xeon show the same thing:
- **AnimateDiff:** about 42 s per denoising step for 16 frames at 512x512, so a 4-step AnimateDiff-Lightning clip takes about 3.5-4 minutes for 0.5 s of 30 fps video.
- **Wan2.1 1.3B:** about 134 s per step for 33 frames at 832x480, so roughly 3.7 hours at standard settings.

Only AnimateDiff-class SD1.5 models fit the disk, and they can't hold a consistent character across a 40 s Short. Wan, LTX, CogVideoX, SVD, ToonCrafter and HunyuanVideo don't fit the 2.8-8 GB of free disk at all. **Treat AI video generation as not feasible on this machine.**

### Cited Findings
**Official hardware requirements (all GPU):**
- **Wan2.1 T2V-1.3B** "requires only 8.19 GB VRAM" and "can generate a 5-second 480P video on an RTX 4090 in about 4 minutes" without optimizations. The only CPU options are `--offload_model True` and `--t5_cpu`, which offload parts of the model from a GPU; there is no CPU-only mode. 1.3B is recommended at 480P, and 720P is "less stable" — [Wan2.1 README](https://github.com/Wan-Video/Wan2.1)
- **Wan2.1-T2V-1.3B checkpoint sizes:** official repo files are 5.68 GB DiT + 11.36 GB umt5-xxl text encoder (bf16) + 0.51 GB VAE (about 17.6 GB in total) — [HF API, Wan-AI/Wan2.1-T2V-1.3B](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B). ComfyUI repack: DiT fp16 2.84 GB, umt5_xxl fp8 6.74 GB or fp16 11.37 GB — [Comfy-Org/Wan_2.1_ComfyUI_repackaged](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged). GGUF text encoder: Q4_K_M 3.66 GB, Q8_0 6.04 GB, F16 11.37 GB — [city96/umt5-xxl-encoder-gguf](https://huggingface.co/city96/umt5-xxl-encoder-gguf)
- **Wan2.2 TI2V-5B:** "can generate a 5-second 720P video in under 9 minutes on a single consumer-grade GPU". The single-GPU command needs "at least 24GB VRAM (e.g, RTX 4090)" even with `--offload_model True --convert_model_dtype --t5_cpu`. Output is 720P at 24 fps (1280x704). The VAE compresses 16x16x4 — [Wan2.2 README](https://github.com/Wan-Video/Wan2.2). GGUF builds run from Q2_K 1.85 GB to Q8_0 5.40 GB (Q4_K_M 3.43 GB), and the Wan2.2 VAE is 1.41 GB — [QuantStack/Wan2.2-TI2V-5B-GGUF](https://huggingface.co/QuantStack/Wan2.2-TI2V-5B-GGUF)
- **stable-diffusion.cpp** (pure C/C++, CPU backend with AVX/AVX2/AVX512) supports Wan2.1/Wan2.2 since 2025-09-06 — [sd.cpp README](https://github.com/leejet/stable-diffusion.cpp). Its Wan doc gives no timings, uses `umt5_xxl` (fp16 or city96 GGUF), and warns "Wan models vae requires really much VRAM!" — [sd.cpp docs/wan.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/wan.md). I found no published CPU timing for Wan in sd.cpp. The closest sd.cpp CPU reports are for image models: about 5 s per step for SD after a `-O3` fix ([issue #248](https://github.com/leejet/stable-diffusion.cpp/issues/248)), and about 60 s per iteration for Qwen-Image on the CPU backend ([issue #1114](https://github.com/leejet/stable-diffusion.cpp/issues/1114)). Both are second-hand via search snippets.
- **LTX-Video:** the repo benchmarks speed only on H100, e.g. 13B distilled "generates HD videos in 10 seconds… (on H100)". The community LTX-VideoQ8 does 720x480x121 "in under a minute on RTX 4060 (8GB VRAM)", and the model "works best on resolutions under 720 x 1280 and number of frames below 257" — [LTX-Video README](https://github.com/Lightricks/LTX-Video). Checkpoint sizes: ltxv-2b-0.9.8-distilled 6.34 GB, fp8 4.46 GB, 13B fp8 15.69 GB. The text encoder in the repo is 4 shards totalling about 19 GB, and the VAE is 1.68 GB — [HF API, Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
- A blog says LTX CPU-only generation is "technically possible but extremely slow", on the order of hours per clip. It is a secondary blog, not a benchmark — [MindStudio](https://www.mindstudio.ai/blog/ltx-desktop-free-open-source-ai-video-editor) (via search snippet)
- **CogVideoX-2B** (720x480, 49 frames by default): about 90 s on A100 and 45 s on H100 for 50 steps. With diffusers optimisations it needs 4 GB minimum in FP16 or 3.6 GB in INT8, using `enable_sequential_cpu_offload()`, VAE slicing and tiling. Without optimisations, peak memory is "about 3 times the value in the table" — [CogVideo README](https://github.com/THUDM/CogVideo). Files: text encoder 9.52 GB + transformer 3.39 GB + VAE 0.86 GB — [HF API, zai-org/CogVideoX-2b](https://huggingface.co/zai-org/CogVideoX-2b)
- **HunyuanVideo:** "The minimum GPU memory required is 60GB for 720px1280px129f and 45G for 544px960px129f", and 80 GB is recommended. FP8 weights save "about 10GB" — [HunyuanVideo README](https://github.com/Tencent-Hunyuan/HunyuanVideo)
- **Stable Video Diffusion XT:** the single-file checkpoint is 9.56 GB. The diffusers fp16 parts are a 3.05 GB UNet, a 1.26 GB image encoder and a 0.20 GB VAE — [HF API, stabilityai/stable-video-diffusion-img2vid-xt](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt)
- **ToonCrafter (anime in-betweening):** "~24G & 24s (A100, ddim 50steps)". The original code "may consume about 24G~27G GPU memory", and "the community has lowered the consumption to ~10GB". It does "up to 16 frames with a resolution of 512x320", and the "success rate is not guaranteed". There is no CPU mention — [ToonCrafter README](https://github.com/Doubiiu/ToonCrafter). model.ckpt is 10.50 GB, plus a 1.46 GB sketch encoder — [HF API, Doubiiu/ToonCrafter](https://huggingface.co/Doubiiu/ToonCrafter)
- **AnimateDiff:** motion modules are mm_sd_v15_v2 1.82 GB and v3_sd15_mm 1.67 GB — [HF API, guoyww/animatediff](https://huggingface.co/guoyww/animatediff). AnimateDiff-Lightning checkpoints are 0.91 GB each (1, 2, 4 and 8 steps) — [HF API](https://huggingface.co/ByteDance/AnimateDiff-Lightning). It is "distilled from AnimateDiff SD1.5 v2", runs "more than ten times faster than the original AnimateDiff", and lists ToonYou, IMP, Mistoon Anime and similar anime/cartoon base models. The 1-step model is "only provided for research purposes" — [AnimateDiff-Lightning model card](https://huggingface.co/ByteDance/AnimateDiff-Lightning). AnimateLCM's fp16 motion model is 0.91 GB and its LoRA 0.13 GB — [HF API, wangfuyun/AnimateLCM](https://huggingface.co/wangfuyun/AnimateLCM)
- **AnimateDiff on CPU in practice:** the animatediff-cli README says it can "theoretically" run on CPU "but it's not recommended" — [neggles/animatediff-cli](https://github.com/neggles/animatediff-cli) (via search snippet). A Medium guide reportedly lists AnimateDiff on a Xeon CPU under WSL2 at about 141 s per frame. **Unverified:** the page returned HTTP 403 to me, and the settings are unknown — [Medium, aivisionslab](https://medium.com/@aivisionslab/running-local-ai-on-an-amd-rx-580-in-2026-the-complete-vulkan-guide-7c2592cdb020)
- **Pose-driven character models (all GPU-sized):**
  - MimicMotion: the 72-frame model "requires 16GB VRAM (4060ti) and finishes in 20 minutes on a 4090"; the 16-frame U-Net needs at least 8 GB, while "the VAE decoder demands 16GB" (it can be moved to CPU) — [MimicMotion README](https://github.com/Tencent/MimicMotion)
  - UniAnimate: "~12G" GPU memory for 32x768x512 after offloading CLIP and the VAE; "~21G" at 768x1216 — [UniAnimate README](https://github.com/ali-vilab/UniAnimate)
  - Moore-AnimateAnyone: local app needs ">= 16GB vram" — [Moore-AnimateAnyone README](https://github.com/MooreThreads/Moore-AnimateAnyone)

**[LOCAL] measured on this machine (bf16, 4 threads, real architectures with random weights):**
- **AnimateDiff** (SD1.5 UNet + motion adapter v1-5-2, 1,313M params), 16 frames at 512x512, one denoising forward pass: **41.2 s and 42.1 s**. SD VAE decode of the 16 frames: **46.1 s**. Peak RSS was **8.6 GB**, because the VAE decoded all 16 frames in one batch; decoding frame by frame would lower this. Load was 2.0-3.7, i.e. close to quiet.
- **Wan2.1-T2V-1.3B DiT** (1,419M params), 33 frames at 832x480 (latent 9x60x104, 14,040 tokens), one forward pass: **134.0 s**, peak RSS 3.8 GB. Another process was using about 1-2 cores at the start.

### Inferences
**Clip-time estimates from the measured step times** (these exclude model loading, the text encoder and file I/O):
- **AnimateDiff-Lightning 4-step** (no CFG): 4 x 42 s + 46 s VAE ≈ **3.5-4 min per 16-frame 512x512 clip**. That is 0.53 s of video at 30 fps, or 2 s at 8 fps. The 8-step model takes about 6-7 min.
- **AnimateLCM** at 4-6 steps uses the same architecture, so expect about 3-5 min.
- **Classic AnimateDiff** (about 25 steps with CFG, i.e. 2 passes per step): about 50 x 42 s ≈ **35 min per 16 frames**.
- **A full 40 s Short** at 8 fps (anime "on threes") is about 20 such clips: 1.2 h with Lightning and about 12 h with classic AnimateDiff. Then each clip must still be upscaled from 512 px, and the character will not stay on-model from clip to clip.
- **Wan2.1 1.3B, 33 frames:** with 50 steps and CFG (2 passes per step), 100 x 134 s ≈ **3.7 h for about 2 s of video**. With a 4-step distilled LoRA and no CFG it would be about 9 min plus VAE and T5. A 5 s / 81-frame clip has about 2.3x the tokens, and attention cost grows faster than linearly, so it would take well over 2.3x longer.
- **Disk:** a minimal Wan 1.3B set (2.84 GB DiT + 3.66 GB Q4 T5 + 0.25-0.5 GB VAE ≈ 6.8-7 GB) is larger than the free disk. Wan2.2 5B, LTX (encoder about 19 GB), CogVideoX (about 13.8 GB), SVD (9.5 GB), ToonCrafter (10.5 GB) and HunyuanVideo don't fit either.
- **RAM:** an AnimateDiff set (an SD1.5 anime checkpoint of about 2 GB fp16, which is my estimate, plus a 0.9 GB Lightning module) fits on disk. But peak RAM of about 8.6 GB at 512x512 x 16 frames is tight against the 5-10 GB that is actually free.
- **ToonCrafter on CPU:** it uses the same UNet-video class as AnimateDiff but with 50 DDIM steps plus CFG. From the AnimateDiff step time, I estimate **roughly an hour or more per 16-frame in-between** at 512x320. The 10.5 GB checkpoint doesn't fit the disk anyway.
- **Pose-driven models** (AnimateAnyone, MimicMotion, UniAnimate) are SD-UNet video models sized for 8-24 GB GPUs. On CPU they would be at least as slow as AnimateDiff per frame. Not feasible.
- **AMX helps but doesn't change the verdict.** OpenVINO/IPEX bf16 could plausibly speed up the UNet 2-5x; I measured that size of gain for the upscalers in section 3, but I did not test it on video diffusion. Even then, Lightning clips would take about 1-2 min each, at 512 px and with no character consistency.

### Gaps
- I found **no first-hand published CPU-only timing** for any listed video model. Searches of GitHub, diffusers and ComfyUI turned up only GPU numbers or "possible but slow". The only CPU figures are my own step timings and one unverifiable Medium claim of about 141 s per frame.
- I didn't time the text encoders (umt5-xxl, T5-XXL), the Wan/LTX VAEs on CPU, or a full end-to-end run with real weights, because the disk could not hold them.
- I didn't test OpenVINO or IPEX acceleration of a video diffusion model. Intel's OpenVINO notebooks for LTX-Video or Wan could not be confirmed by search.

## 2. Frame interpolation for anime on CPU (RIFE, rife-ncnn-vulkan, IFRNet, GMFSS, FILM)

### Takeaway
RIFE runs fine on this CPU, with no GPU and no Vulkan driver, through `rife-ncnn-vulkan -g -1`:
- about 2 s for one 720x1280 in-between and about 4-5 s at 1080x1920, both including model load;
- about 0.65-0.8 s per output frame in batch mode at 720x1280.

For a natively rendered vector animation, though, interpolation gives nothing. pycairo renders an extra frame in about 0.1 s at 1080x1920, exactly and with no artifacts; that's 10-40x cheaper than RIFE. Anime timing "on 2s/3s" is a style choice that interpolation destroys. Use frame holds instead of interpolation.

### Cited Findings
- **CPU mode is built in:** rife-ncnn-vulkan's CLI has `-g gpu-id … (-1=cpu, default=auto)`, and the README shows a run that "runs on CPU, Discrete GPU, and Integrated GPU all at the same time" — [rife-ncnn-vulkan README](https://github.com/nihui/rife-ncnn-vulkan). waifu2x-ncnn-vulkan, realcugan-ncnn-vulkan and realsr-ncnn-vulkan document the same `-1=cpu` option — [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan), [realcugan-ncnn-vulkan](https://github.com/nihui/realcugan-ncnn-vulkan), [realsr-ncnn-vulkan](https://github.com/nihui/realsr-ncnn-vulkan)
- **Published RIFE speeds are GPU-only:**
  - "30+FPS for 2X 720p interpolation on a 2080Ti GPU" (original project, via SVP search snippet) — [SVP RIFE wiki](https://svp-team.com/wiki/RIFE_AI_interpolation)
  - IFRNet paper: per-frame runtimes at 1280x720 on a Tesla V100 are RIFE 0.026 s and IFRNet 0.025 s — [IFRNet CVPR 2022 paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Kong_IFRNet_Intermediate_Feature_Refine_Network_for_Efficient_Frame_Interpolation_CVPR_2022_paper.pdf) (via search snippet)
  - RIFE v4.4 at 1920x1088 on an RTX 3090 runs at 53.6 fps (ORT-CUDA) and 71.3 fps (TensorRT). The page gives no CPU numbers, only that OV_CPU is "the recommended CPU backend; generally faster than ORT-CPU" — [vs-mlrt RIFE wiki](https://github.com/AmusementClub/vs-mlrt/wiki/RIFE)
- **SVP's GPU tiers:** real-time 1080p at 48 fps or 720p at 60-72 fps needs ">= RTX 3070" (generic) or ">= RTX 2060" (TensorRT) — [SVP RIFE wiki](https://www.svp-team.com/wiki/RIFE_AI_interpolation) (via search snippet)
- **Practical-RIFE:** "it is recommended to choose 4.25 by default for most scenes". On 4.25, "the anime scenes have been significantly improved". It recommends `--scale=0.5` for 4K. The README gives no CPU numbers — [Practical-RIFE README](https://github.com/hzwer/Practical-RIFE)
- **Anime held frames break naive interpolation:** "Normally anime use 1 image for 2~3 frames (8/12 FPS) in 24FPS video". The proposed fix finds "the next key frame (the frame is not same as previous frame)"; "Some scene change still cannot be detected" — [Practical-RIFE PR #23](https://github.com/hzwer/Practical-RIFE/pull/23)
- Community tools remove duplicate frames before interpolating to cope with this:
  - TheAnimeScripter `--smooth_dedup` — [TheAnimeScripter](https://github.com/NevermindNilas/TheAnimeScripter)
  - ddfi-rife — [ddfi-rife](https://github.com/Mr-Z-2697/ddfi-rife)
  - (via search snippets)
- An opinion source says shooting "on twos" is a deliberate style and interpolation removes it; it suggests interpolating to a lower target or not at all — [apatero blog](https://www.apatero.com/blog/rife-vs-film-video-frame-interpolation-comparison-2025) (low-reliability blog, via search snippet)
- A peer-reviewed case study of AI interpolation on a hand-made watercolor animated film reports "pulsing" artifacts — [ACM DL 10.1145/3749893.3749971](https://dl.acm.org/doi/10.1145/3749893.3749971) (via search snippet)
- **GMFSS_Fortuna** calls itself "Dedicated for Anime Video Frame Interpolation". It is built on PyTorch, CUDA and cupy, and gives no speed, VRAM or CPU information — [GMFSS_Fortuna README](https://github.com/98mxr/GMFSS_Fortuna)
- **FILM** has an official OpenVINO notebook that converts it to IR and offers a device dropdown, so it can run on CPU. No timing was in the snippet — [OpenVINO FILM notebook](https://docs.openvino.ai/2024/notebooks/film-slowmo-with-output.html)

**[LOCAL] rife-ncnn-vulkan 20221029, CPU mode `-g -1`** (wall time includes model load and PNG decode/encode):
- **RIFE v4.6, 720x1280, one pair → one in-between:** 2.16 s quiet, 3.04 s under heavy load. Peak RSS 0.77 GB.
- **RIFE v4.6, 1080x1920, one pair:** 4.14-4.66 s, or 6.23 s under heavy load. Peak RSS 1.5 GB.
- **RIFE v4.6, batch mode, 8 frames at 720x1280 → 16 frames:** 10.5 s (other agents using about 2.5 cores) and 12.4 s (Blender using 2 cores). That's about **0.65-0.8 s per output frame**.
- **The older "rife-anime" model** shipped in the same package: 17.0 s for one 720x1280 pair, 3.3 GB RSS (under load).
- **No GPU flag:** with no Vulkan GPU present, the default (auto) run also completed on CPU (7.5 s under load).

**[LOCAL] pycairo native rendering** (synthetic frame of 300 filled and stroked bezier shapes plus a gradient):
- 90 ms at 720x1280
- **100 ms at 1080x1920**
- 163 ms at 1440x2560
- 253 ms at 2160x3840

### Inferences
- **For this pipeline, interpolation is strictly worse than rendering more frames.** The animation is parametric, so sampling the curves at 60 fps costs about 0.1 s per extra 1080p frame and is exact. RIFE costs about 0.7-4 s per frame and adds warping artifacts, especially on thin line art and on overlapping limbs.
- **For the anime look, go the other way:** render on 2s/3s (12 or 8 drawings per second held over the 24/30 fps timeline). Smooth camera pans and push-ins can still be rendered at the full frame rate.
- **The only plausible use for RIFE here** is footage the pipeline does not render itself, such as a clip from an AI generator at 8-16 fps. Even then, de-duplicate first, as PR #23 and TheAnimeScripter do.
- **GMFSS on CPU:** it relies on CUDA/cupy kernels and heavier flow networks than RIFE. I estimate it would be several times slower than RIFE on CPU, if it runs at all without CUDA.

### Gaps
- I found no published CPU timing for RIFE (PyTorch), IFRNet, GMFSS or FILM. The only CPU numbers are my rife-ncnn ones.
- I did not test the OpenVINO FILM notebook, GMFSS on CPU, or rife v4.25/4.26 in ncnn form. The 2022 ncnn release tops out at v4.6.
- I didn't do a visual quality check of RIFE output on this channel's line art (timing only).

## 3. Video/frame upscaling on CPU (Real-ESRGAN animevideov3 / x4plus_anime_6B, Real-CUGAN, Anime4K, waifu2x-ncnn)

### Takeaway
Upscaling works on CPU, and with OpenVINO bf16 (AMX) it is fast:
- **realesr-animevideov3:** about 0.6-0.9 s per frame for 360x640 → 1440x2560 and about 1.1-1.5 s per frame for 540x960 → 2160x3840 (4K). That's 3-8x faster than PyTorch fp32.
- **ncnn on CPU:** Real-CUGAN is slow (about 10-12 s per frame, 540 → 1080), and the Real-ESRGAN ncnn binary does not run at all without a Vulkan device.

But pycairo renders a native 4K frame in about 0.25 s, so for vector frames, rendering at the target resolution is faster and exact. AI upscaling only pays off for raster or AI-generated sources.

### Cited Findings
- **Real-ESRGAN anime models:** realesr-animevideov3 is the anime video model (ncnn x2/x3/x4 variants ship in the release zip). The FAQ says CPU inference must use fp32, not half precision — [Real-ESRGAN anime video model doc](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_video_model.md), [Real-ESRGAN FAQ via mintlify](https://mintlify.com/xinntao/Real-ESRGAN/resources/faq) (via search snippet)
- **The Real-ESRGAN-ncnn-vulkan CLI documents no CPU option:** `-g gpu-id gpu device to use (default=auto)` — [Real-ESRGAN-ncnn-vulkan README](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan)
- **Third-party OpenVINO port on an Intel Xeon Platinum 8581C** (8 cores, 16 threads, AVX-512, AMX), FP32:
  - x4plus_anime_6B: 512x512 → 2048x2048 in 6.617 s (PyTorch) vs **0.583 s (OpenVINO)**, 11.3x faster; 1024 → 4096 in 26.37 s vs 2.34 s
  - x4plus: 512 → 2048 in 19.92 s vs 1.485 s
  - The page says it "leverages Intel OpenVINO with AVX-512 and AMX", but publishes no BF16 or INT8 runs
  - [ibrhr/Real-ESRGAN-OpenVINO](https://huggingface.co/ibrhr/Real-ESRGAN-OpenVINO)
- **AMX gains on Sapphire Rapids with OpenVINO** (non-SR models): about 2x for face detection and 2.6x for a weld-porosity model versus AVX-512 alone — [Phoronix AMX review](https://www.phoronix.com/review/intel-xeon-amx/4) (via search snippet)
- **Anime4KCPP ACNet single-image timings, 1080p → 4K:**

  | Hardware | Type | Time per image |
  |---|---|---|
  | Ryzen 2600 | CPU | 0.630 s |
  | Ryzen 2500U | CPU | 1.304 s |
  | GTX 1660 Super | GPU | 0.067 s |

  512p → 1024p takes 0.025 s on the Ryzen 2600 — [Anime4KCPP (Gitee mirror README)](https://gitee.com/tianzerl/Anime4KCPP). The current v3 is CNN-based, with CPU SIMD (AVX/AVX2/AVX512), OpenCL and CUDA backends — [Anime4KCPP GitHub](https://github.com/TianZerL/Anime4KCPP)
- **Anime4K (GLSL)** is a GPU shader set. Its pre-scaler is quoted at 1.5 ms for 1080p → 4K, 4 ms in total, on a Vega 64 GPU — [Anime4K](https://github.com/bloc97/Anime4K) (via search snippet)
- **ncnn Vulkan on a software renderer:** I found no benchmark of the ncnn tools on lavapipe or llvmpipe. Phoronix calls Lavapipe/LLVMpipe "painfully slow" in general — [Phoronix](https://www.phoronix.com/news/Zink-On-Lavapipe-Patch) (via search snippet). The nihui tools don't need it anyway, because they have a native ncnn CPU path (`-g -1`, see section 2). Lavapipe is not installed here, and apt had no candidate for `mesa-vulkan-drivers` without an index update.

**[LOCAL] upscaling timings** (per frame, after warm-up; ranges show quiet vs contended runs):

| Model / backend | Input → output | Time per frame | Peak RSS |
|---|---|---|---|
| realesr-animevideov3 x4, OpenVINO 2026.4 **bf16** | 360x640 → 1440x2560 | **0.55-0.86 s** | 0.6 GB |
| realesr-animevideov3 x4, OpenVINO bf16 | 540x960 → 2160x3840 | **1.06-1.46 s** | 0.9 GB |
| realesr-animevideov3 x4, OpenVINO bf16 | 720x1280 → 2880x5120 | ~2.0 s | 1.3 GB |
| realesr-animevideov3 x4, OpenVINO **f32** | 360x640 → 1440x2560 | 1.6-1.85 s (2.8-3.0 s under heavy load) | |
| realesr-animevideov3 x4, PyTorch 2.14 CPU fp32 | 360x640 → 1440x2560 | 4.0 s (5.8-7.0 s under load) | 0.45 GB |
| realesr-animevideov3 x4, PyTorch bf16 autocast | 360x640 → 1440x2560 | 4.1-5.7 s | |
| realesr-animevideov3 x4, PyTorch fp32 | 540x960 → 2160x3840 | 9.7-12.5 s | |
| RealESRGAN_x4plus_anime_6B, OpenVINO **bf16** | 360x640 → 1440x2560 | **4.2-4.7 s** | 1.7 GB |
| RealESRGAN_x4plus_anime_6B, OpenVINO f32 | 360x640 → 1440x2560 | 14.9-16.9 s | |
| RealESRGAN_x4plus_anime_6B, PyTorch fp32 | 360x640 → 1440x2560 | 35-37 s (62 s under load) | 3.2 GB |
| RealESRGAN_x4plus_anime_6B, PyTorch bf16 | 360x640 → 1440x2560 | 10-24 s | |
| Real-CUGAN se 2x, ncnn CPU `-g -1` | 540x960 → 1080x1920 | 39.4-48.2 s for 4 frames (≈10-12 s/frame) | 3.6 GB |
| Real-CUGAN se 2x, ncnn CPU `-g -1` | 720x1280 → 1440x2560 | 26.6-29.0 s (one frame, includes load) | 3.1 GB |
| realesrgan-ncnn-vulkan 20220424 (`-g -1` tried) | any | **fails**: "vkCreateInstance failed -9 … invalid gpu device" | |

- **OpenVINO setup cost:** converting a model takes about 5-6 s if you convert at a small input shape and then reshape. Tracing at full size took 33-48 s, and two full-size conversions were OOM-killed while other jobs held RAM.
- **bf16 quality:** OpenVINO bf16 output against PyTorch fp32 output scored **PSNR 55.4 dB**, which is visually identical.

### Inferences
- **Native rendering beats AI upscaling for vector frames.** pycairo renders native 2160x3840 in about 0.25 s/frame. Rendering at 540x960 (about 0.09 s) and upscaling with the fastest AI path takes about 1.1-1.5 s and is only an approximation of the true edges.
- **Upscaling is only worth it for raster or generated material:** painted backgrounds, AI-generated plates, or 512 px AnimateDiff clips. For that, use realesr-animevideov3 through OpenVINO bf16, at about 0.6-1.5 s per frame on this machine. A 40 s, 30 fps Short (1,200 frames) at 540 → 4K would take about 25-30 min. If only held anime drawings are upscaled (8-12 unique drawings per second), that drops to about 7-10 min.
- **anime_6B** gives higher quality but is about 6x slower (4-5 s/frame even with bf16). It is suitable for stills and backgrounds, not every frame.
- **Real-CUGAN via ncnn CPU** is too slow for video (about 10+ s/frame) unless ported to OpenVINO, which I didn't test.
- **Anime4KCPP** is the cheapest CPU option for a quick 2x (about 0.6 s per 1080p → 4K frame on a 6-core Ryzen, published). It is likely competitive with OpenVINO animevideov3 but untested here.
- **Lavapipe for the Real-ESRGAN ncnn binary:** installing it would be pointless, because the same model already runs well through OpenVINO or PyTorch.

### Gaps
- No published BF16/AMX benchmark exists specifically for Real-ESRGAN, RIFE or video diffusion on Xeon. The third-party OpenVINO page is FP32-only; my bf16 numbers are the only ones.
- I didn't test Anime4KCPP, waifu2x-ncnn `-g -1`, Real-CUGAN in OpenVINO or ONNX, or lavapipe with the ncnn tools.
- I only checked upscaled quality numerically (bf16 vs fp32). I didn't judge it visually against native renders of this channel's art style.

## 4. CPU-friendly AI that could add anime motion or detail to existing frames (img2img per keyframe, EbSynth-style propagation)

### Takeaway
The only CPU-practical AI options are:
- **(a) still-image models on keyframes.** SD1.5-class img2img or LCM/SDXS through OpenVINO (FastSD CPU) runs from under 1 s to about 20 s per 512-768 px image.
- **(b) non-neural example-based propagation.** The open-source EbSynth core is public domain and has a CPU backend; Ezsynth is a Python wrapper around it.

Both add per-frame flicker or drift risk. With a fully vector pipeline, AI is best kept to backgrounds, textures and still keyframes, not the moving characters.

### Cited Findings
- **FastSD CPU (OpenVINO):** SDXS-512 makes one 512x512 image in 0.82 s on a Core i7-12700. LCM at 768x768 with 2 steps takes 18 s in PyTorch and 12 s in OpenVINO on the same CPU. FLUX.1-schnell int4 at 512x512, 3 steps, takes about 4 min 30 s — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu) (via search snippet). A third-party user reports about 20 s for 4 steps with LCM-dreamshaper-v7-openvino — [DEV Community](https://dev.to/webdeveloperhyper/image-generative-ai-on-pc-without-gpu-free-and-fast-fastsd-cpu-1jio) (via search snippet)
- **jamriska/ebsynth (open-source core):** "The code is released into the public domain". It implements PatchMatch, which the README says "is patented by Adobe (U.S. Patent 8,861,869)". It has a `-backend [cpu|cuda]` option and CPU-only build scripts. It does "not rely on neural networks". The README shows no video or keyframe mode and no timings — [jamriska/ebsynth README](https://github.com/jamriska/ebsynth)
- **Ezsynth** builds the ebsynth library (Linux and Windows cpu+cuda build scripts). Its own GPU use is optional: `use_gpu` for histogram blending "Defaults to False", and there are optional Cupy paths — [Ezsynth README](https://github.com/Trentonom0r3/Ezsynth). ReEzSynth is described as a PyTorch rewrite with custom CUDA extensions, i.e. GPU-oriented — via a [nemovideo.com](https://www.nemovideo.com/es-ES/alternative/ebsynth) marketing page (low reliability, via search snippet)
- **AnimateDiff vid2vid** advice from its distiller: don't use overly long or high-resolution inputs (their tests were 576x1024, 8 s, 30 fps) — [AnimateDiff-Lightning model card](https://huggingface.co/ByteDance/AnimateDiff-Lightning)

### Inferences
**Practical CPU uses for this pipeline:**
- **(1) Backgrounds and texture plates:** generate them once with SD1.5/LCM on CPU, upscale them once (anime_6B through OpenVINO bf16), and pan them in pycairo. Cost is seconds to minutes per plate, not per frame.
- **(2) Paint-over style transfer:** render the vector frames, stylise one keyframe per shot by hand or with img2img, then propagate with EbSynth on CPU. I found no CPU timing for this. PatchMatch is non-neural and the README calls it "Fast", so tens of seconds per 720p frame seems plausible, but that is unverified.
- **Not practical on CPU:** per-frame img2img of a whole Short (1,200 frames x 1-20 s, plus flicker) and AnimateDiff vid2vid (see section 1).
- **Patent:** Adobe's PatchMatch patent notice is worth a legal check before commercial use. Its expiry date is unverified.

### Gaps
- I found no published CPU timings for ebsynth, Ezsynth or TemporalKit, and no anime-specific results for them.
- I didn't benchmark SD1.5 img2img or FastSD on this Xeon. From the AnimateDiff numbers (about 42 s for 16 frames, i.e. about 2.6 s per 512x512 frame per UNet pass in bf16), a 4-step LCM still would take about 10-15 s here with PyTorch bf16. That is an estimate.

## 5. Owner's laptop: Intel Core i7 (11th gen) + NVIDIA RTX 3050 Laptop GPU, 4 GB VRAM (scope added by coordinator)

### Takeaway
**What 4 GB of VRAM can do:**
- **Fits:** RIFE and Real-ESRGAN (ncnn-vulkan or PyTorch; small models) and SD1.5 still images.
- **Might fit, with offloading:** AnimateDiff-Lightning/LCM at reduced size, and Wan2.1 1.3B GGUF with T5 on the CPU. Community reports for the 3050 4 GB run from **minutes to hours** per few-second clip.
- **Doesn't fit:**
  - FramePack (official minimum 6 GB)
  - ToonCrafter (about 10 GB community minimum, 8 GB at 512p in the ComfyUI wrapper)
  - Wan2.2 5B (OOM reports on a 3050 laptop at Q6K)
  - LTX-Video 2B (no 4 GB reports; its smallest checkpoint is 4.46 GB)
  - HunyuanVideo, MimicMotion, UniAnimate and AnimateAnyone

### Cited Findings
- **RTX 3050 Laptop:** 4 GB VRAM, 2,048 shading units, 192 GB/s memory bandwidth — [versus.com](https://versus.com/en/nvidia-geforce-gtx-1650-vs-nvidia-geforce-rtx-3050-laptop) (via search snippet); TDP 60 W — [theframecoach](https://theframecoach.com/can-run/nvidia-rtx-3050-laptop-4gb/cyberpunk-2077) (via search snippet)
- **FramePack:** "At least 6GB GPU memory", "Laptop GPUs are okay", and "Nvidia GPU in RTX 30XX, 40XX, 50XX series that supports fp16 and bf16". Speed is 2.5 s/frame unoptimized or 1.5 s/frame with TeaCache on an RTX 4090, and laptops are "about 4x to 8x slower" — [FramePack README](https://github.com/lllyasviel/FramePack)
- **Independent FramePack F1 test on an RTX 4060 Laptop** (8 GB, 32 GB RAM): a 4.83 s, 145-frame, 608x640 clip took 3,363 s (56 min), or 23.2 s/frame. VRAM sat at 5.75 GB reserved, but peak RAM demand was about 43 GB because of the ~16 GB text encoder plus the ~26 GB transformer. The model download is about 40 GB, and the author concludes "the bottleneck is RAM" — [lilting.ch](https://lilting.ch/en/articles/local-long-video-fastwan-framepack-rocm)
- **Wan2.1 GGUF on the 3050 laptop:**
  - A ComfyUI workflow page names "RTX 3050 Laptop (4 GB VRAM)" as its target and lists Q5, Q3_K_M and Q2_K quants, but contains no timings — [The-frizzy1/Wan21-GGUF-4GB-Workflow](https://huggingface.co/The-frizzy1/Wan21-GGUF-4GB-Workflow)
  - Search snippets attribute to the related Civitai page an RTX 3050 Laptop (4 GB) report: 53 frames at 480x848, plus an upscaler to 1080p, at 25 steps, took **5.32 hours**. The model size is unclear. Other comments: a 3050 8 GB with 32 GB RAM took "approx. 25 min for a 3-second i2v clip with upscaling and interpolation", and someone waited "up to 5 hours for about 3 seconds" before adding TeaCache and torch.compile — [Civitai 1309674](https://civitai.com/models/1309674/wan21gguf-only-4gb-vram-comfyui-workflow) (**second-hand, not opened**)
- **Wan2.2 GGUF on the 3050 vs 3060 laptop:** search snippets say the 3050 laptop hit OOM errors every time at Q6K with 49 frames, and took 205-535 s at Q2K with 25 frames, depending on resolution. Whether this was 5B or 14B is unclear — [Civitai article 20036](https://civitai.com/articles/20036/3050-vs-3060-can-a-laptop-survive-wan22-gguf-video-generation) (**second-hand; the page returned 403**)
- **Wan2.1 1.3B officially needs 8.19 GB VRAM** without quantisation — [Wan2.1 README](https://github.com/Wan-Video/Wan2.1). A guide says GGUF Q4 at about 4-6 GB is the minimum viable setup, with T5 offloaded to CPU RAM — [willitrunai](https://willitrunai.com/blog/wan-2-2-vram-requirements) (low-reliability aggregator, via search snippet)
- **WanGP** ("Wan for the GPU poor") claims to "run select models with as little as 6 GB of VRAM". It gives no per-model 4 GB claims — [Wan2GP README](https://github.com/deepbeepmeep/Wan2GP)
- **ToonCrafter:** 24-27 GB originally, "~10GB" after community work — [ToonCrafter README](https://github.com/Doubiiu/ToonCrafter). The kijai ComfyUI wrapper listing says "interpolation at 512p can be done with 8GB" and fp16 at 1024x576 uses a bit under 10 GB — [comfy.icu, kijai DynamiCrafterWrapper](https://comfy.icu/extension/kijai__ComfyUI-DynamiCrafterWrapper) (via search snippet)
- **LTX-Video 2B:** the smallest checkpoint is the 4.46 GB fp8 2B distilled; the community Q8 build runs 720x480x121 in under a minute on an 8 GB RTX 4060 — [LTX-Video README](https://github.com/Lightricks/LTX-Video), [HF API](https://huggingface.co/Lightricks/LTX-Video). I found no 4 GB report.
- **AnimateDiff VRAM:**
  - SDXL high-resolution AnimateDiff "usually requires ~13GB VRAM" — [AnimateDiff README](https://github.com/guoyww/AnimateDiff)
  - AnimateDiff-Evolved supports fp8 motion models, which "decreases VRAM usage, but changes outputs" — [ComfyUI-AnimateDiff-Evolved README](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved)
  - I found no measured 4 GB AnimateDiff report. One guide says `--novram` "puts the entire model in CPU RAM; generation can take 10–30 minutes but works even on 4GB" (for still images) — [comfylab.dev](https://comfylab.dev/blog/guides-pro/reduce-vram-usage-comfyui/) (low reliability, via search snippet)
- **MimicMotion** needs 8 GB minimum for its 16-frame U-Net and 16 GB for its VAE decoder — [MimicMotion README](https://github.com/Tencent/MimicMotion). UniAnimate needs about 12 GB — [UniAnimate README](https://github.com/ali-vilab/UniAnimate)
- **RIFE/ESRGAN on this class of GPU:** I found no 3050-specific numbers. SVP lists ">= RTX 2060" with TensorRT for real-time 1080p at 48 fps — [SVP RIFE wiki](https://www.svp-team.com/wiki/RIFE_AI_interpolation) (via search snippet). Anime4KCPP ACNet does 1080p → 4K in 0.067 s/image on a GTX 1660 Super — [Anime4KCPP Gitee](https://gitee.com/tianzerl/Anime4KCPP)

### Inferences
- **RIFE v4.x and realesr-animevideov3** are small models (my CPU runs peaked at 0.8-1.5 GB RAM for RIFE at 720-1080p and under 1 GB for animevideov3 at 4K). They should fit 4 GB of VRAM and run several times faster than on the Xeon. I estimate roughly 5-20 fps for RIFE at 720p via ncnn-vulkan or TensorRT on a 60 W 3050 laptop; that is unverified.
- **Real-CUGAN and anime_6B** at large sizes may need tiling (`-t`) on 4 GB.
- **AnimateDiff-Lightning on 4 GB:** the SD1.5 UNet (about 1.7 GB fp16) plus the motion module (0.9 GB fp16) is about 2.6 GB of weights. 512x512 x 16 frames activations likely exceed the rest. It should run with ComfyUI `--lowvram`, smaller sizes (e.g. 384x640 or 512x288) or fewer frames, likely at **tens of seconds to a few minutes per 16-frame clip**. That still beats this Xeon's measured ~3.5-4 min. Unverified.
- **Wan2.1 1.3B on 4 GB** is possible with GGUF plus CPU T5 plus tiled VAE, but community reports are hours per clip. **Wan2.2 5B** OOMs except at Q2K and very short lengths.
- **Not realistic on the 3050 4 GB:** FramePack (6 GB minimum and about 40 GB of models plus a very large RAM need), ToonCrafter, LTX 2B, HunyuanVideo and the pose models.
- **The laptop CPU:** an 11th-gen mobile i7 (Tiger Lake) likely has AVX-512 but not AMX or AVX512_BF16. That is unverified for the owner's exact SKU; check with `lscpu` or CPU-Z. The OpenVINO bf16 speed-ups measured on this Xeon would therefore not carry over to the laptop CPU.

### Gaps
- I have no first-hand timing of RIFE, Real-ESRGAN, AnimateDiff or LTX on an RTX 3050 Laptop 4 GB. The Wan 3050 figures come from search snippets of Civitai pages I could not open (HTTP 403).
- The laptop's system RAM and free disk are unknown. Offloading-based video models (Wan GGUF, FramePack) depend on them heavily.
- I couldn't confirm a FramePack fork that works below 6 GB.
