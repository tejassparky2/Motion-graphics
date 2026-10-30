# Open AI image, video and animation models for an original monster-taming isekai anime series, on a 4 GB RTX 3050 Laptop (16 GB RAM) and a 4-core CPU-only container (state as of 30 Oct 2026)

Scope note for the report writer. This extends `reports/CPU anime animation pipeline.md` (27 Oct 2026) and its notes in `research_notes/CPU anime animation pipeline/`. Numbers carried over from those are marked **(earlier report)** and were not re-checked here. Labels used: **[measured]** = a timing someone actually ran, with source and hardware; **[official]** = the model maker's own claim; **[secondary]** = a third-party blog or aggregator, lower reliability; **[estimate]** = my arithmetic or judgement; **[Reddit]** = one user's anecdote. New since the earlier report: the laptop's RAM is now known (16 GB), and it is the binding limit for most 2026 models, more than the 4 GB of VRAM.

Hardware reference: the RTX 3050 4 GB Laptop GPU is GA107 Ampere with 2,048 CUDA cores; the 2023 6 GB refresh has 2,560 cores and lower bandwidth ([Notebookcheck](https://www.notebookcheck.net/GeForce-RTX-3050-4GB-Laptop-GPU-vs-GeForce-RTX-3050-6GB-Laptop-GPU_10592_11576.247598.0.html)).

## Q1. Still images of original characters and creatures: which anime models, how fast on 4 GB VRAM + 16 GB RAM, and can the newer big image models run at all?

### Takeaway
An SDXL anime checkpoint (Animagine XL 4.0 first, Illustrious lineage second) in Forge or ComfyUI with an 8-step LCM/Hyper LoRA is still the best quality per minute on the laptop: about 30-60 s per ~1 MP image (estimate from measured same-card numbers). It also has the deepest anime tool ecosystem (ControlNet, IP-Adapter, LoRAs). The one new model worth a side-by-side test is **Z-Image Turbo** (Apache-2.0, 6B, 8 steps). It has a measured 2.17 s/it at 512x512 on an RTX 3050 Laptop and ~2 min per 1024x576 image on a 4 GB GTX 1050 Ti with 16 GB RAM, but its anime quality is unproven. FLUX.3 Klein, Qwen-Image(-Edit), LTX-class and MiniMax-class models want 18-32+ GB of system RAM, so on this laptop they are tests, not a production route. Qwen-Image-2.1 (Sept 2026) and FLUX.2 klein 9B are non-commercial and out.

### Cited Findings
**SDXL anime models on this exact GPU class (carried over, then new)**
- (earlier report) RTX 3050 Laptop median **2.63 it/s for SD 1.5 at 512x512** across 78 user records **[measured, vladmandic benchmark DB]** ([benchmark data](https://vladmandic.github.io/sd-data/pages/benchmark-data.json)). A ComfyUI SDXL workflow tuned for the 3050 Laptop 4 GB made a 1024x720 image in **55-60 s** (10 base + 5 refiner steps), and **85-115 s with a LoRA** **[measured by the workflow author, same GPU]** ([Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner)). The same page's comments report a **3050 Ti 4 GB** doing SDXL in Comfy at 896x1152 in **~30 s** **[Reddit-grade comment]**, and stock SDXL in under 3 minutes before tuning (same source, via search summary).
- (earlier report) Forge users report **Illustrious SDXL at 2-3 s/it on 4 GB** **[Reddit]** ([r/StableDiffusion 1two5jr](https://www.reddit.com/r/StableDiffusion/comments/1two5jr/)). A 16 GB-RAM 3050 owner saw Pony crash once LoRAs were added **[Reddit]** ([1hrgbnr](https://www.reddit.com/r/StableDiffusion/comments/1hrgbnr/)).
- Forge's README says "without any cmd flag, Forge can run SDXL with 4GB vram" **[official]** ([Forge README via search](https://huggingface.co/spaces/JusticeLee/stable-diffusion-webui-forge/blob/main/README.md)). A 2026 install guide says that with "always maximize offload" 4 GB cards can do SDXL but "3-5x longer" **[secondary]** ([offlinecreator Forge guide](https://offlinecreator.com/guide/stable-diffusion-webui-forge-installation-2026)).
- Step distillation: SDXL-Lightning ships 1-, 2-, 4- and 8-step checkpoints **[official]** ([ByteDance/SDXL-Lightning](https://Huggingface.co/ByteDance/SDXL-Lightning)). I found no measured 4 GB Lightning/Hyper timing. Licences (earlier report): LCM-LoRA is OpenRAIL++ ([HF](https://huggingface.co/latent-consistency/lcm-lora-sdv1-5)), Hyper-SD "claims no rights in the Output" ([licence](https://huggingface.co/ByteDance/Hyper-SD/blob/main/LICENSE.md)), **DMD2 is CC BY-NC-SA and must not be used** ([HF](https://huggingface.co/tianweiy/DMD2)).
- Licences of the anime checkpoints (earlier report): **Animagine XL 4.0** is CreativeML Open RAIL++-M with commercial use listed as permitted ([HF](https://huggingface.co/cagliostrolab/animagine-xl-4.0)). **Illustrious XL** has conflicting signals: HF says SDXL licence, but the Civitai page does not tick "sell generated images" ([HF](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.0); [Civitai API](https://civitai.com/api/v1/models/795765)). **NoobAI-XL** prohibits "any form of commercialization ... of ... model-generated products" ([HF](https://huggingface.co/Laxhar/noobai-XL-1.1)). Pony V6 should be avoided without written permission ([Civitai API](https://civitai.com/api/v1/models/257749)).
- Illustrious ecosystem size: Civitai lists "Illustrious XL Models & 202K+ LoRAs" ([Civitai ecosystem page](https://civitai.com/ecosystems/illustrious)). Reviewers rate Illustrious stronger than Anima for "tag control, character consistency, and batch work" ([lilting.ch WAI-Anima vs WAI-Illustrious](https://lilting.ch/en/articles/wai-anima-anima-ecosystem-evolution)).

**Anima (2B anime DiT on Cosmos-Predict2)**
- VRAM reports conflict: ~7 GB unquantized ([lilting.ch hands-on](https://lilting.ch/en/articles/anima-2b-anime-image-generation)), under 6 GB ([artokun guide](https://artokun.mintlify.app/blog/anima-comfyui)), 10-12 GB in Stability Matrix ([note.com/kemari](https://note.com/kemari_81ckqlbg/n/n25ef2d9ef43a?hl=en)). Speed: on an M1 Max, Anima preview3 took ~275 s per image against 217-337 s for WAI-Illustrious **[measured, Apple M1 Max]** ([lilting.ch](https://lilting.ch/en/articles/wai-anima-anima-ecosystem-evolution)). A Turbo LoRA reportedly cuts time to about a fifth "with some loss of detail" (via search summary of the same sources).
- Licence: CircleStone Labs Non-Commercial Licence on the model, but "You may use generated images commercially" ([HF card, earlier report](https://huggingface.co/circlestone-labs/Anima)).

**Z-Image Turbo (Tongyi-MAI, Alibaba)**
- **Apache-2.0**, 6B parameters, "only 8 NFEs", "fits comfortably within 16G VRAM consumer devices", "sub-second inference latency" on H800 **[official]**; paper published 27 Nov 2025. The card talks about photorealism and bilingual text; anime is not mentioned. The base Z-Image "supports a wide range of artistic styles"; a Z-Image-Edit variant exists **[official]** ([HF card](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)).
- **RTX 3050 Laptop GPU: 2.17 s/it at 512x512** in stable-diffusion.cpp **[measured, leejet (sd.cpp maintainer), 1 Dec 2025; quant and VRAM not stated]**. 4 GB AMD cards on Vulkan: RX 470 Q4_K "just fits" with the text encoder on CPU at **7 s/it (512x512) and 35 s/it (1024x1024)**; RX 580 4 GB Q3_K 7.3-20 s/it at 512x512 depending on driver settings. Qwen3 text conditioning on CPU took ~824 ms **[measured, unnamed CPU]** ([sd.cpp discussion #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026)).
- **GTX 1050 Ti 4 GB + i7-8750H + 16 GB RAM** (the closest match to the owner's laptop): "Z-Image Turbo AIO fp8" at 1024x576 took "a little over 2 minutes per image" (~2:06); a GGUF Q3 build was worse and slower **[Reddit, measured by OP, Dec 2025]** ([r/StableDiffusion 1pf7986 snapshot](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z)).
- Nunchaku added 4-bit Z-Image-Turbo on 2025-12-20 and a "20-30% performance boost for Z-Image" in v1.2.0 (2026-01-12) **[official]** ([Nunchaku README](https://github.com/nunchaku-ai/nunchaku)). Secondary guides put Q4_K_M at ~5-6 GB total at 768x768 and recommend 32 GB system RAM for offloaded GGUF **[secondary]** ([zimage.run memory guide](https://zimage.run/blog/zi-166-z-image-gpu-memory-optimization-en-20260728); [thundercompute](https://www.thundercompute.com/blog/z-image-turbo-comfyui)).

**FLUX family**
- **FLUX.1 [dev] and Kontext [dev]** use the "FLUX.1 [dev] Non-Commercial License v1.1.1". Section 2(d): "We claim no ownership rights in and to the Outputs ... You may use Output for any purpose (including for commercial purposes), except as expressly prohibited herein", plus a ban on using outputs "to train, fine-tune or distill a model that is competitive with the FLUX.1 [dev] Model" ([LICENSE.md](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md)). The licence's "Non-Commercial Purpose" definition excludes "revenue-generating activity", and users argue this conflicts with 2(d) ([HF discussion #136](https://huggingface.co/black-forest-labs/FLUX.1-dev/discussions/136)). A Kontext-dev thread reports a v1.1 revision that dropped and then restored the outputs line ([Kontext discussion #6](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/discussions/6)). Running the model on the owner's own laptop to make video frames is arguably "use" for a revenue-generating channel. **Flag: legally ambiguous; avoid unless BFL confirms in writing.**
- **FLUX.2 [klein] 4B is Apache-2.0**; the 9B variants are non-commercial. VRAM: "~13GB" on the HF card vs "~8GB" in the GitHub repo **[official, conflicting]**; GGUF from Q2_K 1.83 GB **[secondary]** ([HF card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B); [GitHub](https://github.com/black-forest-labs/flux2); [BFL blog](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence)). No 4 GB timing found.
- **FLUX.3 Image Klein** (5.6B, released 15 Oct 2026) uses the **FLUX Kommunity License**: commercial use of generated images is free for individuals and companies under **US$5M** gross revenue, with a requirement for content filtering or output review and AI disclosure where the law requires ([VentureBeat](https://venturebeat.com/technology/black-forest-labs-opens-flux-3-image-klein-weights-with-free-commercial-use-limited-to-smaller-businesses); [computingforgeeks](https://computingforgeeks.com/flux-3-klein-comfyui/)). On an **RTX 3060 Ti 8 GB**, int8 at 1024x1024, 16 steps: **11.1 s warm / 34.4 s cold** with the prompt upsampler off, **19.6 s warm** with it on; `--lowvram` 17.9 s warm; **ComfyUI process RAM 11.7-20.9 GiB (18.0 GiB default)**; the author recommends 32 GB RAM; 16 GB untested **[measured, rented 3060 Ti]** ([computingforgeeks](https://computingforgeeks.com/flux-3-klein-comfyui/)).

**Qwen-Image family**
- Nunchaku (Apache-2.0) supports Qwen-Image (2025-08-15), Qwen-Image-Edit (2025-09-09) and Edit-2509 (2025-09-24). v1.0.0 added asynchronous offloading that cuts transformer VRAM "to as little as 3 GiB with no performance loss"; FLUX with a 4-bit text encoder and per-layer offload needs "4 GiB" (v0.1.4, 2025-03-07) **[official]** ([Nunchaku README](https://github.com/nunchaku-ai/nunchaku)). Users report OOM even with offloading and a VRAM spike before `image.save()` ([issue #675](https://github.com/nunchux-ai/nunchaku/issues/675); [issue #796](https://github.com/nunchux-ai/nunchaku/issues/796)).
- **Qwen-Image-Edit-2511**: the official card claims "significantly improved" character consistency and better multi-person consistency (portraits and photos) ([via search summary of HF card / unsloth GGUF](https://huggingface.co/unsloth/Qwen-Image-Edit-2511-GGUF)). A spec article lists FP8 ~15 GB file / "6GB+" VRAM and GGUF Q4_K_M 13.1 GB "CPU runnable", recommends **32 GB RAM minimum on Windows**, and assumes "about 5 minutes" per 40-step edit; a Lightning LoRA gives 4 steps. None of it was measured by the author **[secondary]** ([lilting.ch 2511 specs](https://lilting.ch/en/articles/qwen-image-edit-2511-local-specs)). Q2_K GGUF is ~7.5 GB ([search summary](https://www.stablediffusiontutorials.com/2025/12/qwen-image-edit-2511.html)).
- **Qwen-Image-2.1 (released 20 Sept 2026; 7B, native transparency) is under the Qwen Research License: non-commercial only**, as are LoRAs built on it, such as the "2anime" LoRA. The earlier Qwen-Image models were Apache-2.0 ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence); [HF 2anime LoRA](https://huggingface.co/NicknickAI/QwenImage2.1-2anime); [HF Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1)). **Do not use.**

**Other**
- Wan2GP (Windows one-click, "free to use locally") now bundles image models including Flux 1/2/3 Klein, Qwen Image, Z-Image and HiDream, and claims it can "run select models with as little as 4 GB of VRAM" without naming them **[official]** ([Wan2GP README, read 30 Oct 2026](https://github.com/deepbeepmeep/Wan2GP)).

### Inferences
- **Laptop stills ranking (quality per minute, licence-clean)** **[estimate]**:
  1. **Animagine XL 4.0 (or a verified Illustrious lineage) + Hyper-SDXL 8-step CFG LoRA**, Forge or ComfyUI: ~30-60 s per 832x1216 image. This comes from the measured 55-60 s for 15 SDXL steps on the same GPU and 2-3 s/it in Forge. It is the only route with mature anime ControlNet, IP-Adapter and LoRA support, and it fits 16 GB RAM if LoRA stacking is kept light.
  2. **Z-Image Turbo** (Apache): ~20-25 s at 512x512 (8 x 2.17 s plus overhead) and roughly 1-2 min at ~1 MP on the 3050. That is similar to or faster than SDXL at 28 steps, and the license is cleaner. Anime styling and creature anatomy are untested, so test before adopting it.
  3. **FLUX.2 klein 4B GGUF** (Apache) and **Qwen-Image-Edit-2509/2511 via Nunchaku INT4 with offload** (Apache): these are for consistent *edits* of an approved character (new pose, outfit, expression), not bulk generation. Expect minutes per image and RAM pressure on 16 GB, and set a large Windows page file.
  4. **FLUX.3 Klein**: licence OK for a channel under US$5M, but ~18 GiB process RAM on a default run makes 16 GB marginal. Try `--lowvram` with the upsampler off.
- **Server (4-core CPU, 15 GB RAM)**: keep SD 1.5 anime + LCM (~10-14 s per 512x768 image, earlier report). For Z-Image Turbo on CPU via sd.cpp, the earlier server measurement was SDXL UNet 2.6B at 9.2 s per step (832x1216, bf16). A 6B DiT at ~1 MP should be roughly 2-4x that, which gives an estimated 2-5 min per 8-step image. That is acceptable for an overnight fallback only if the disk holds the ~4-7 GB of quantized files (the earlier report found 2.8-8.8 GB free).
- The 16 GB of system RAM, not the 4 GB of VRAM, is what rules out most 2026 models (FLUX.3 Klein 18 GiB RSS, Qwen-Image-Edit "32 GB minimum", LTX "at least 32GB"). A cheap RAM upgrade to 32 GB, if the laptop has a free slot, would unlock more of the list than anything else.

### Gaps
- No measured Hyper/Lightning/LCM SDXL timing on a 4 GB card was found; the 30-60 s figure is an estimate.
- Z-Image Turbo anime quality and creature anatomy: no review found. The card is photoreal-oriented.
- Whether Nunchaku's INT4 kernels run on Ampere sm_86 (RTX 30 series) and on Windows was not stated on the README page read. v1.2.0 added "INT4 support for 20-series GPUs", which suggests a pre-Blackwell INT4 path, but this is unverified.
- No 4 GB timings for FLUX.2 klein 4B, Qwen-Image-Edit-2511, Chroma, HiDream, SD 3.5 or Lumina/NetaYume. Their licences were not re-checked this round, except FLUX and Qwen as above.

## Q2. Keeping original characters and creatures consistent: reference tools, LoRA training on 4 GB, turnarounds and ControlNet posing

### Takeaway
No training-free tool reliably locks an *original* anime character, and especially not a non-human creature. IP-Adapter transfers "style and vibe". In-context editors (FLUX Kontext, Qwen-Image-Edit-2511, FLUX.2 klein) are the strongest training-free route, but one user's Kontext comic pipeline passed only ~84% of panels on a same-character check. The robust approach remains a per-character LoRA (or the earlier report's reuse-the-approved-art approach). On 4 GB, SD 1.5 LoRA training is feasible but SDXL LoRA training is marginal: an old OneTrainer build fit in 4.5-4.9 GB, and newer builds regressed to 12.2 GB.

### Cited Findings
- IP-Adapter "is doing style and vibe transfer, it was never really built to lock a specific character"; advice was a LoRA per character, a fixed token block, and separate passes because characters "bleed into each other" **[Reddit, earlier report]** ([r/comfyui 1v62676](https://www.reddit.com/r/comfyui/comments/1v62676/)). An academic paper describes IP-Adapter as a training-free way to inject identity features ([CharCom, arXiv 2510.10135](https://arxiv.org/html/2510.10135v2)).
- **FLUX Kontext reference pipeline**: one developer fed a reference portrait to Kontext instead of training LoRAs. A moderate reference strength worked best, and **about 84% of panels passed a manual same-character check** **[anecdote]** ([dev.to/qcrao](https://dev.to/qcrao/character-consistency-in-ai-comics-3-tricks-that-beat-lora-training-for-me-3ad7)). Kontext-dev carries the FLUX.1 [dev] licence ambiguity (Q1).
- **Illustrious** recognises well-known characters from tags, but "obscure or original ones usually need" a LoRA, and creature characters such as Pokémon need an extra species tag ([artificialguy Illustrious/NoobAI guide](https://artificialguy.com/blog/illustrious-noobai-anime-guide/)). An "Anima in-context character" LoRA is pitched as an IP-Adapter alternative ([HF darask0](https://huggingface.co/darask0/Anima-InContext-Character/discussions)).
- **Qwen-Image-Edit-2511** claims improved single- and multi-person identity consistency, shown on portraits and photos, not anime ([unsloth GGUF card](https://huggingface.co/unsloth/Qwen-Image-Edit-2511-GGUF)). Its licence family (pre-2.1 Qwen-Image) is Apache-2.0 ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence)).
- **Face-ID tools**: InsightFace's models are "for non-commercial research purposes only", per summaries of InsightFace's terms quoted in LivePortrait discussions ([HN thread on LivePortrait](https://news.ycombinator.com/item?id=40876840); [FacePoke LICENSE](https://huggingface.co/spaces/guardiancc/FacePoke/raw/8b13ef9d732b74256740077d2cd66b054fdbcdce/LICENSE)).
- **LoRA training VRAM**: a OneTrainer bug report says an SDXL LoRA once trained in **4.5-4.9 GB** (FP8 weights, FP32 fallback, batch 1, 1024 px, no sampling), but the then-current master used **12.2 GB** with the same settings. In the same thread, Kohya reached "under 6 gb" at FP8 batch 2 **[user report, ~mid-2025]** ([OneTrainer issue #934](https://github.com/Nerogar/OneTrainer/issues/934)). A 2026 guide says Kohya SDXL LoRA needs ~10 GB with fused backward + bf16 **[secondary]** ([sanj.dev](https://sanj.dev/post/lora-training-2025-ultimate-guide/)). An Illustrious character LoRA on a 6 GB card took about an hour, reached only 50% resemblance at first, and was "fine" after 60 epochs at LoRA weight 1.2-1.4 **[Reddit, earlier report]** ([1l04nqv](https://www.reddit.com/r/StableDiffusion/comments/1l04nqv/)). AdamW8bit "cuts VRAM meaningfully ... with negligible quality loss" **[secondary]** ([kohya_ss wiki](https://github.com/bmaltais/kohya_ss/wiki/LoRA-training-parameters)).
- **ControlNet for posing**: xinsir's openpose SDXL ControlNet is Apache-2.0 and shows anime examples ([HF card](https://HuggingFace.co/xinsir/controlnet-openpose-sdxl-1.0)). The union "ProMax" SDXL ControlNet covers OpenPose, Depth, Lineart and "Anime Lineart" among other control types ([RioShiina model list](https://huggingface.co/spaces/RioShiina/ImageGen/blob/main/yaml/controlnet_models.yaml)). The union model's own licence was not confirmed.

### Inferences
- Recommended consistency stack **[estimate]**:
  - The owner approves a turnaround sheet per character and creature: front, 3/4, side and back, plus expressions.
  - Train a small **SD 1.5 or SDXL LoRA per main character and per creature**. Use the laptop only if an older OneTrainer or Kohya FP8 recipe fits in 4 GB. Otherwise rent a cloud GPU for an hour per LoRA (cost not researched here).
  - Pose every shot with OpenPose (people) or depth/lineart (creatures, which OpenPose skeletons do not fit), then use Qwen-Image-Edit-2509/2511 or FLUX.2 klein 4B for small consistent fixes.
  - Keep the earlier report's principle: reuse approved art for most shots rather than regenerate.
- Creatures are harder than humans. Pose skeletons and face-ID tools are human-only, so creature consistency should rely on LoRAs, lineart/depth ControlNet from a simple 3D blockout or sketch, and a short fixed token block (species tag + colour + 2-3 distinctive features).

### Gaps
- No source tested OmniGen2, PuLID or InstantID on anime or creatures. Whether InstantID and PuLID depend on InsightFace weights (my understanding) was not re-verified.
- No measured SD 1.5 or SDXL LoRA training time on a 4 GB RTX 3050 or GTX 1650 was found.
- No evidence was found on turnaround-sheet generation quality (e.g., multi-view LoRAs) for anime creatures.

## Q3. Animating stills into 2-5 s anime character or creature clips: which video models run on 4 GB / 16 GB RAM, how long they take, and how good the motion is

### Takeaway
Only one open video model has a hardware match to the owner's laptop: **Wan 2.2 TI2V-5B with a 4-step Turbo** (Apache-2.0). A **GTX 1050 Ti 4 GB + 16 GB RAM** made a 1024x576, 97-frame (~4 s) clip in **29 min, 17 of them VAE decode**, and "only 1 out of 3 attempts is usable". The 3050 should be faster, but this remains an overnight hero-shot tool, not a production path. The anime-specialised **AniSora** (bilibili, Apache-2.0 on V2/V3, built on Wan) needs ~12 GB even in its slim build. **LTX-2.x, FramePack, HunyuanVideo 1.5 and MiniMax H3** need 6+ GB VRAM and/or 32-44+ GB RAM. Wan 2.5, 2.6, 2.7 and 3.0 have no verified open weights. **LivePortrait** (fast, MIT code) is officially for humans, cats and dogs; anime faces are untested.

### Cited Findings
**Wan 2.2 TI2V-5B (Apache-2.0)**
- Official: "5-second 720P video in under 9 minutes on a single consumer-grade GPU", but the single-GPU command needs "at least 24GB VRAM" (earlier report, [Wan2.2 README](https://github.com/Wan-Video/Wan2.2)). An RTX 4090 with the official CLI made 5 s of 720p in **667 s at a 24,079 MiB peak** **[measured]** ([computingforgeeks](https://computingforgeeks.com/run-wan-video-generation-locally/)).
- **Turbo GGUF** (from quanhaol/Wan2.2-TI2V-5B-Turbo via Kijai; Apache-2.0): "very much usable with an old 4GB GPU"; "4 steps is enough"; preferred 1280x704 or 704x1280; example 121-frame 1024x704 I2V at Q5_K_S. Sizes: Q2_K 1.86 GB, Q3_K_M 2.55 GB, **Q4_K_M 3.44 GB**, Q5_K_S 3.56 GB, Q6_K 4.22 GB, Q8_0 5.4 GB **[official card, no timings]** ([hum-ma GGUF](https://huggingface.co/hum-ma/Wan2.2-TI2V-5B-Turbo-GGUF)).
- **GTX 1050 Ti 4 GB / i7-8750H / 16 GB RAM**: Wan 2.2 5B fp16 with two Kijai LoRAs, 4 steps, **1024x576, 97 frames: 29 min per clip, of which decoding took 17 min**. Early clips had slow motion; the model "can surprise" but "only 1 out of 3 attempts is usable". A commenter with an RTX 4090 estimated "5-10 minutes per video" **[Reddit, measured by OP, Dec 2025]** ([1pf7986 snapshot](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z)). Earlier quotes from the same thread: the model "often misunderstands the prompts and doesn't have good motion", and "it's not perfectly consistent. I did it just through prompts" ([1pf7986](https://www.reddit.com/r/StableDiffusion/comments/1pf7986/), earlier report).
- (earlier report) Wan 2.2 **14B** GGUF on an **RTX 3050 4 GB + 64 GB RAM**: "about 30 minutes for 5s video" **[Reddit]** ([1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)). An **RTX 3050 Laptop + 32 GB RAM**: "6 hours 22 minutes for a single 15 second" clip; at fast settings "hands still render as indistinct blurry blobs" **[Reddit]** ([1w9zhbx](https://www.reddit.com/r/StableDiffusion/comments/1w9zhbx/)). A 3050 Laptop OOMed at Q6K with 49 frames and took 205-535 s at Q2K with 25 frames **[second-hand, Civitai page 403]** ([Civitai article 20036](https://civitai.com/articles/20036/3050-vs-3060-can-a-laptop-survive-wan22-gguf-video-generation)).
- Wan2GP (v18.00, 11 Oct 2026) sped up Wan 2.1 VAE decode at 1080p from "28 s / 10.5 GB to 11 s / 4.7 GB" (GPU not named) **[official]** ([Wan2GP README](https://github.com/deepbeepmeep/Wan2GP)). This matters because decode was 59% of the 1050 Ti clip time.
- **No newer open Wan**: the official Wan-AI HF org stops at Wan 2.2 (last: Wan2.2-Animate-14B, Nov 2025). Wan 2.6 is API-only, and Wan 3.0 open-weight claims trace to a single social post **[secondary, multiple]** ([runpod Wan 2.7 guide](https://www.runpod.io/articles/guides/wan-2-7-runpod); [digitalapplied Wan 3.0 reality check](https://www.digitalapplied.com/blog/wan-3-0-reality-check-rumor-vs-shipped)).

**Anime-specialised video models**
- **Index-AniSora (bilibili)**:
  - V1.0 is built on CogVideoX-5B; V2.0 on Wan2.1-14B, with weights "licensed under Apache 2.0" (2025-07-11).
  - V3 (2025-08-27, Apache 2.0): "can generate 5 sec 360p video shot within 8 sec" (hardware not stated), with arbitrary-frame inference, keyframe interpolation and "ultra-low-resolution super-resolution" from 90p to 720p/1080p.
  - V3.1 has a **"12GB VRAM version"** on ModelScope (2025-09-25). V3.2 is trained on Wan2.2 and runs in 8 steps. AnyMask (2025-10-31) adds spatial and temporal masks **[official]** ([GitHub](https://github.com/bilibili/index-anisora)).
  - A press summary warns that its published samples use clips and characters from Japanese anime ([GIGAZINE](https://gigazine.net/gsc_news/en/20250519-anisora/)). A third-party listing claims the 5B Diffusers variant runs in 6 GB **[secondary, unverified]** ([aibase](https://model.aibase.com/models/details/1924737758954524672)).
- **ToonComposer** (Tencent ARC, ICLR 2026) does inbetweening and colourisation from sparse sketch keyframes. Its base is Wan2.1-I2V-14B-480P, so it is heavy ([HF](https://huggingface.co/TencentARC/ToonComposer); [arXiv 2508.10881](https://arxiv.org/abs/2508.10881)). **AniDoc** colourises line-art sequences from a character reference ([awesomepapers](https://awesomepapers.io/generative-models/papers/2412.14173)). **ToonCrafter** (earlier report) needs ~10 GB after community optimisation and 8 GB at 512p in the kijai wrapper; "success rate is not guaranteed" ([ToonCrafter](https://github.com/Doubiiu/ToonCrafter)).

**LTX-Video / LTX-2.x (Lightricks)**
- The LTX-2 Community License covers "all LTX-2 versions since January 5, 2026". Entities at or above **US$10M annual revenue** need a paid licence; smaller ones may use it commercially; several third-party sites wrongly say Apache-2.0 ([HF LICENSE LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3/blob/main/LICENSE); [Magic Hour](https://magichour.ai/blog/ltx-2-3-vs-wan-2-2)).
- Low-VRAM reports: a user with **6 GB VRAM + 44 GB RAM** ran 1280x736 for 10 s "smoothly"; another: "very vram friendly but it's hungry with RAM, at least 32GB" **[Reddit-grade, HF discussion]** ([Kijai/LTXV2_comfy #32](https://huggingface.co/Kijai/LTXV2_comfy/discussions/32)). On an RTX 4090, LTX 2.3 GGUF Q4 took 4m18s (peak 9.1 GB) vs FP8 2m51s (13.7 GB) for 768x512x121, 40 steps **[secondary, unverified method]** ([ltxworkflow](https://ltxworkflow.com/blog/fp16-vs-fp8-vs-gguf-which-ltx-23-format-to-choose)).
- Older LTX-Video 2B 0.9.8 distilled has GGUFs (iq4_nl, q6_k, q8_0); "q2_k ... super fast but not usable" ([calcuis ltxv-gguf](https://huggingface.co/calcuis/ltxv-gguf/blob/ca4659f4a3eb2b4db2367b58539cd09b64942260/README.md?code=true)). An earlier quote: LTXV "is fast, but the quality is poor and everything morphs" **[Reddit, earlier report]** ([1pf7986](https://www.reddit.com/r/StableDiffusion/comments/1pf7986/)).

**FramePack, HunyuanVideo 1.5, MiniMax H3, others**
- **FramePack**: officially "At least 6GB" ([README](https://github.com/lllyasviel/FramePack), earlier report). Tom's Hardware: an RTX 3050 4 GB "is insufficient for full video generation" ([Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/framepack-can-generate-ai-videos-locally-with-just-6gb-of-vram)). On an RTX 4060 Laptop 8 GB, a 4.83 s clip took 56 min with **~43 GB peak RAM demand** **[measured, earlier report]** ([lilting.ch](https://lilting.ch/en/articles/local-long-video-fastwan-framepack-rocm)).
- **HunyuanVideo 1.5** (8.3B): a 480p I2V step-distilled checkpoint (Dec 2025) runs 8 or 12 steps with "about 75% speedup" on an RTX 4090 **[official]** ([GitHub](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)). The official minimum is ~14 GB with offloading; Wan2GP reportedly runs it in 6 GB **[secondary]** ([techiehub](https://techiehub.blog/best-local-ai-video-generator/); [localaimaster](https://localaimaster.com/blog/hunyuan-video-guide)). The Tencent Hunyuan Community License excludes the EU, UK and South Korea; India is not named as excluded **[secondary; 1.5 LICENSE text not retrieved]** ([ChatForest](https://chatforest.com/reviews/hunyuanvideo-tencent-open-source-video-generation/)). LightX2V's 4-step distills are listed as Apache-2.0 ([HF](https://huggingface.co/lightx2v/Hy1.5-Distill-Models)).
- **MiniMax H3 (Hailuo 3.0)**:
  - 33.1B dense; weights on HF on **3 Aug 2026** under the "MiniMax H3 Community License Agreement". It makes 768p locally (2K upscale API-only), 4-15 s at 24 fps, with native 32 kHz stereo audio ([RunPod](https://www.runpod.io/blog/minimax-h3-the-open-weight-omni-modal-video-model-and-what-it-takes-to-run-it)).
  - Licence "appears to not authorize use in the United States, European Union, United Kingdom, or South Korea", including use of outputs there (RunPod's reading). A MiniMax-branded FAQ adds a US$20M revenue cap and a requirement to display "MiniMax H3" in product UI (unverified domain) ([design.minimax.io](https://design.minimax.io/h3)).
  - It has a ~32B Qwen3-VL text encoder and 134 GB of bf16 weights ([search summary](https://huggingface.co/blog/ResterChed/minimax-h3-hailuo-3-0)).
  - Wan2GP claims "only 5-6GB of VRAM to gen 15 seconds of H3 video at 480p" (7 Oct 2026) ([Wan2GP](https://github.com/deepbeepmeep/Wan2GP)).
  - A creator found it "kept inventing extra people and objects that weren't in the source still" **[Reddit, earlier report]** ([1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)).
- (earlier report) **SVD** licence is non-commercial or registration-gated; CogVideoX ~13.8 GB of files; **AnimateDiff** on the server CPU measured ~42 s per step, and **Wan 2.1 1.3B ~134 s per step** **[measured on this server]**.

**LivePortrait**
- MIT-licensed code; the **Animals model** was released 2024-08-02 and updated 2025-01-01 "with more data". Animals mode needs X-Pose and is "ONLY tested on Linux and Windows with NVIDIA GPU". The README mentions only humans, cats and dogs, with no anime ([LivePortrait README](https://github.com/KwaiVGI/LivePortrait)). The default InsightFace detector is non-commercial, but ComfyUI-LivePortraitKJ uses MediaPipe (Apache-2.0) by default ([search summary of KJ wrapper/HN](https://news.ycombinator.com/item?id=40876840); earlier report: [LivePortraitKJ](https://github.com/kijai/ComfyUI-LivePortraitKJ)). The CPU path is "extremely slow and not recommended" ([FasterLivePortrait](https://github.com/warmshao/FasterLivePortrait), earlier report). A 2026 vendor blog lists LivePortrait as "strong on anime / illustrated inputs" **[secondary, vendor]** ([pixazo](https://www.pixazo.ai/blog/best-open-source-ai-lip-sync-models)).

### Inferences
- **Laptop video ranking** **[estimate]**:
  1. **Wan 2.2 TI2V-5B Turbo GGUF (Q4_K_M 3.44 GB) at 4 steps, run through Wan2GP or ComfyUI with a tiled or fast VAE.** For a 2-3 s anime clip at ~832x480 to 704x1280, scaling from the 1050 Ti's 29 min (97 frames at 1024x576, 17 min of decode) gives roughly **8-20 min per attempt on the 3050**. The 3050 has ~3x the 1050 Ti's FP16 throughput plus tensor cores, and 2026 VAE speed-ups cut decode. At 1 usable in 3 attempts, that is **~0.5-1 h per usable shot**: an overnight batch of 4-8 hero shots, never every shot.
  2. **LivePortrait (MediaPipe detector)**: worth a 30-minute test on a face crop of an Animagine character. If it tracks anime faces it gives head turns and expressions in seconds per clip on GPU, but it does nothing for bodies or creatures. Speed on the 3050 was not found.
  3. Everything else (AniSora 12 GB, ToonComposer 14B, ToonCrafter 8-10 GB, LTX-2.x 32 GB+ RAM, FramePack 6 GB / 43 GB RAM, HunyuanVideo 1.5, MiniMax H3) needs either a rented GPU or a RAM upgrade. **AniSora V3.x is the model to try first if a cloud GPU is ever rented**: Apache-2.0, anime-trained, with keyframe interpolation and masks. Use it only with original characters, since its samples use Japanese anime IP.
- **Server**: AI video stays ruled out (42-134 s per denoising step measured earlier; disk too small).
- **Quality limits** to plan around: one-in-three usable takes, slow or under-animated motion, morphing (LTXV), invented people and objects (H3), blurry hands at fast settings, and identity drift without a LoRA. Image-to-video from an owner-approved still with low motion (hair, cloth, breathing, camera push) is the safe zone. Fights and creature transformations are the riskiest.

### Gaps
- No measured Wan 2.2 5B time on an RTX 3050 Laptop 4 GB specifically; the 8-20 min figure is scaled from a GTX 1050 Ti.
- No independent test of AniSora's VRAM, speed or quality on consumer GPUs; the 12 GB build's speed is unknown.
- MiniMax H3 and HunyuanVideo 1.5 licence texts were read only through secondary summaries.
- No 4 GB report for LTX-2.x, HunyuanVideo 1.5 or AniSora.
- LivePortrait on anime faces, and its speed on the 3050, were not found.

## Q4. Frame interpolation and upscaling: CPU vs GPU speed, and suitability for anime

### Takeaway
Use RIFE (v4.7-4.10 are anime-tuned; MIT, ncnn-Vulkan build runs on CPU at ~2.2 s per 720p in-between, measured earlier) only on AI video clips, never across held 2s/3s drawings, and run a dedup pass first. GIMM-VFI is higher-quality but CUDA-only and ~8 GB at 2K. For upscaling, Real-ESRGAN anime models via OpenVINO bf16 are fast on the server (measured earlier). **4x-AnimeSharp is CC BY-NC-SA (non-commercial), and APISR's code is GPL-3.0 with unclear weight terms.**

### Cited Findings
- RIFE: v4.7-4.10 "optimized for anime scenes"; maintainers noted in 2024 that **4.22.lite** suits post-processing of diffusion-generated videos ([ECCV2022-RIFE](https://github.com/hzwer/ECCV2022-RIFE)). (earlier report) rife-ncnn-vulkan on the server CPU: **2.16 s per 720x1280 in-between**, 4.1-4.7 s at 1080x1920 **[measured on this server]** ([rife-ncnn-vulkan](https://github.com/nihui/rife-ncnn-vulkan)). Anime "use 1 image for 2~3 frames", which breaks naive interpolation ([Practical-RIFE PR #23](https://github.com/hzwer/Practical-RIFE/pull/23)).
- **MultiPassDedup** deduplicates anime frames before interpolation and supports GMFSS, RIFE and GIMM ([GitHub](https://github.com/routineLife1/MultiPassDedup)).
- **GIMM-VFI** (NeurIPS 2024): ~7.9 GB at 2K (DS_SCALE 0.5) and ~10.9 GB at 4K (0.25) for 8x interpolation on V100 **[official]** ([GitHub](https://github.com/GSeanCDAT/GIMM-VFI)). On extreme anime frames it "tends to give cottage cheese", while GMFSS is smoother **[anecdote]** ([wanx-troopers VFI notes](https://wanx-troopers.github.io/vfi.html)). The ComfyUI wrapper needs cupy with no non-CUDA fallback ([comfy.icu](https://comfy.icu/node/GIMMVFI_interpolate)).
- Upscalers: **4x-AnimeSharp is CC BY-NC-SA 4.0** per its creator Kim2091 ([OpenModelDB](https://openmodeldb.info/models/4x-AnimeSharp); [HF Kim2091](https://huggingface.co/Kim2091/AnimeSharp)). **APISR** code is GPL-3.0; the weights' licence is not stated ([APISR](https://github.com/Kiteretsu77/APISR)). Real-ESRGAN publishes "small models that are optimized for anime videos" ([anime_video_model doc](https://github.com/eortigoza5/Real-ESRGAN/blob/master/docs/anime_video_model.md)). (earlier report) On the server, `realesr-animevideov3` via OpenVINO bf16 upscaled 360x640 to 1440x2560 in **0.55-0.86 s**, and `RealESRGAN_x4plus_anime_6B` took 4.2-4.7 s **[measured on this server]**.

### Inferences
- **[estimate]** For AI video clips: generate at a low frame count (e.g., 16 fps), dedup, RIFE to 24 fps on the laptop GPU or the server CPU, and keep character layers on 2s/3s. Upscale stills once with anime_6B and video clips with animevideov3, both on the server.

### Gaps
- GIMM-VFI licence not found. No RIFE GPU timing on a 3050 Laptop. Real-ESRGAN weights' licence (BSD-3 in my understanding) not re-verified this round.

## Q5. Cut-out layers, layer decomposition, transparent generation and inpainting

### Takeaway
For commercial cut-outs, use **isnet-anime (Apache-2.0)**, **BiRefNet** or the open **BEN2** (both reported MIT). Avoid **RMBG-2.0 (CC BY-NC 4.0)**. LayerDiffuse transparent generation reportedly **fails on anime SDXL retrains such as Animagine 4.0**. **Qwen-Image-Layered** (Apache-2.0) decomposes an image into editable RGBA layers but peaked at 45 GB VRAM in one test, so it is a cloud-only tool. **Qwen-Image-2.1's native transparency is non-commercial.**

### Cited Findings
- RMBG-2.0: CC BY-NC 4.0; "commercial use is subject to a commercial agreement with BRIA"; built on BiRefNet ([HF card](https://huggingface.co/briaai/RMBG-2.0)). Exports inherit the licence ([yamura4 ONNX](https://huggingface.co/yamura4/RMBG-2.0-ONNX)).
- BiRefNet family and open BEN2 are listed as MIT **[secondary redistribution page]** ([zurg70 BiRefNet desktop models](https://huggingface.co/zurg70/birefnet-desktop-models)). A Q4 2026 survey lists the BEN2 ONNX export as MIT but "too heavy for first-load" in a browser ([nukebg issue #431](https://github.com/yocreoquesi/nukebg/issues/431)).
- (earlier report) skytnt anime-segmentation ships as rembg `isnet-anime`, 176 MB ONNX, Apache-2.0 ([anime-segmentation](https://github.com/SkyTNT/anime-segmentation)).
- **LayerDiffuse**: an issue reports it "produces solid-color backgrounds or fails" with retrained anime SDXL checkpoints (**NoobAI XL, Animagine XL 4.0, Kohaku**), while working with default SDXL models ([ComfyUI-layerdiffuse #124](https://github.com/huchenlei/ComfyUI-layerdiffuse/issues/124)). A repackaged SDXL attention-injection model is distributed under CreativeML Open RAIL-M ([Geeknasty HF](https://huggingface.co/Geeknasty/LayerDiffusion-SDXL-Attn-Diff)).
- **Qwen-Image-Layered**: Apache-2.0; decomposes into variable numbers of RGBA layers, recursively ([GitHub](https://github.com/QwenLM/Qwen-Image-Layered); [HF](https://huggingface.co/Qwen/Qwen-Image-Layered)). On an RTX Pro 6000 96 GB, peak memory reached **45 GB and 1024 px took 120 s** **[measured, ComfyUI wiki]** ([comfyui-wiki](https://comfyui-wiki.com/en/tutorial/advanced/image/qwen/qwen-image-layered)). Unsloth GGUFs exist ([HF](https://huggingface.co/unsloth/Qwen-Image-Layered-GGUF)).
- (earlier report) **See-through** splits one anime illustration into up to 23 layers; it needs 8-16 GB VRAM, and its free HF Space allows 1-2 extractions per day ([See-through](https://github.com/shitagaki-lab/see-through)).

### Inferences
- **[estimate]** Generate on a flat background, cut out with isnet-anime or BiRefNet on the server CPU (seconds per image; earlier report), and fix edges by inpainting with the same SDXL anime model on the laptop. Use Qwen-Image-Layered or See-through only for the main cast's one-time layer split, via a rented GPU or the free Space.

### Gaps
- No anime-specific accuracy comparison of BiRefNet, BEN2 and isnet-anime was found. SAM 2/SAM 3 licences were not re-checked this round. No Qwen-Image-Layered timing on 4-8 GB GPUs.

## Q6. Audio-driven lip sync for anime faces

### Takeaway
There is no open, commercially clean, independently tested audio-driven model for **anime** faces. MuseTalk, LatentSync, InfiniteTalk and Wan-S2V are built and judged on human faces. Anime claims come only from vendors. The reliable route for an anime look is **Rhubarb-style phoneme-to-mouth-shape timing** driving 3-5 drawn mouth sprites, which is also how TV anime works (earlier report: three mouth drawings).

### Cited Findings
- **MuseTalk** (Tencent Lyra, Apr 2024) inpaints a 256x256 face region in one latent step; a benchmark notes MuseTalk and VideoReTalking "frequently lose identity and visual quality" ([MuseTalk HF](https://huggingface.co/TMElyralab/MuseTalk); [arXiv 2410.10122](https://arxiv.org/html/2410.10122v3); [OmniSync arXiv 2505.21448](https://arxiv.org/html/2505.21448v1)).
- **LatentSync** (audio-conditioned latent diffusion, with TREPA against flicker) is heavier; one review says it wants an A10 or RTX 4090 ([LatentSync arXiv](https://arxiv.org/html/2412.09262v1); [sync.so](https://sync.so/blog/what-is-musetalk)). Hosted vendors claim it works for "stylized (e.g., anime) characters" **[vendor, unverified]** ([WaveSpeed](https://wavespeed.ai/models/wavespeed-ai/latentsync)).
- **InfiniteTalk** is built on Wan2.1 (480p/720p) ([HF Space README](https://huggingface.co/spaces/hlevring/infinitetalk2/blob/main/README.md)). A blog claims **Wan-S2V** needs "only 8.19 GB" **[secondary; this figure matches Wan2.1-1.3B's official requirement and is doubtful for the 14B S2V]** ([imagine.art](https://www.imagine.art/blogs/wan-s2v-overview)).
- **Rhubarb Lip Sync** is "a command-line tool that automatically creates 2D mouth animation from voice recordings" ([GitHub lip-sync topic](https://github.com/topics/lip-sync)). A Ren'Py "automatic anime lipsync" plugin exists ([itch.io](https://jaybe-games.itch.io/automatic-anime-lipsync-plugin-for-renpy)).
- (earlier report) LivePortrait and SadTalker rely on human-face priors; LivePortrait has no native audio driving (its README's only audio feature concatenates audio) ([LivePortrait](https://github.com/KwaiVGI/LivePortrait)).

### Inferences
- **[estimate]** Use Whisper word timings (already in the pipeline) or Rhubarb to drive 3-5 mouth sprites per character and creature, held on 2s/3s. If the owner wants AI lip sync for a close-up, test LatentSync on a rented GPU with an anime face first. It is not practical on 4 GB.

### Gaps
- Rhubarb's licence was not verified this round. No independent anime-face test of MuseTalk, LatentSync, InfiniteTalk or Wan-S2V was found.

## Q7. Real creators' measured results on low-VRAM GPUs (RTX 3050 4 GB, GTX 1650/1050 Ti 4 GB, RTX 3050 6 GB)

### Takeaway
Measured low-VRAM numbers exist only for a few combinations: SD 1.5 (~2.6 it/s), tuned SDXL (~1 min per image), Z-Image Turbo (2.17 s/it at 512 px on a 3050 Laptop; ~2 min per 1024x576 on a 1050 Ti), and Wan 2.2 5B (~29 min per ~4 s clip on a 1050 Ti with 16 GB RAM) / 14B (~30 min per 5 s with 64 GB RAM). Everything else is either a claim or a desktop or high-end number.

### Cited Findings
| Task | Hardware | Result | Source |
|---|---|---|---|
| SD 1.5, 512x512 | RTX 3050 Laptop 4 GB (78 records) | median 2.63 it/s | [vladmandic DB](https://vladmandic.github.io/sd-data/pages/benchmark-data.json) (earlier report) |
| SDXL 1024x720, 10+5 steps, ComfyUI | RTX 3050 Laptop 4 GB | 55-60 s; 85-115 s with LoRA | [Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner) |
| Illustrious SDXL, Forge | 4 GB cards | 2-3 s/it [Reddit] | [1two5jr](https://www.reddit.com/r/StableDiffusion/comments/1two5jr/) (earlier report) |
| Z-Image Turbo, 512x512, sd.cpp | RTX 3050 Laptop | 2.17 s/it | [sd.cpp #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026) |
| Z-Image Turbo Q4_K, Vulkan | RX 470 4 GB | 7 s/it (512), 35 s/it (1024) | [sd.cpp #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026) |
| Z-Image Turbo AIO fp8, 1024x576 | GTX 1050 Ti 4 GB, 16 GB RAM | ~2 min/image [Reddit] | [1pf7986 snapshot](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z) |
| Wan 2.2 5B, 1024x576x97, 4 steps | GTX 1050 Ti 4 GB, 16 GB RAM | 29 min/clip (17 min decode); 1 in 3 usable [Reddit] | same |
| Wan 2.2 14B GGUF, 5 s | RTX 3050 4 GB, 64 GB RAM | ~30 min [Reddit] | [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/) (earlier report) |
| Wan, 15 s at good settings | RTX 3050 Laptop, 32 GB RAM | 6 h 22 min [Reddit] | [1w9zhbx](https://www.reddit.com/r/StableDiffusion/comments/1w9zhbx/) (earlier report) |
| Wan 2.2 GGUF Q2K, 25 frames | RTX 3050 Laptop | 205-535 s; Q6K 49 frames OOM [second-hand] | [Civitai 20036](https://civitai.com/articles/20036/3050-vs-3060-can-a-laptop-survive-wan22-gguf-video-generation) |
| FLUX.3 Klein int8, 1 MP, 16 steps | RTX 3060 Ti 8 GB | 11-20 s warm; 18 GiB RAM | [computingforgeeks](https://computingforgeeks.com/flux-3-klein-comfyui/) |
| FramePack F1, 4.83 s | RTX 4060 Laptop 8 GB, 32 GB RAM | 56 min; ~43 GB RAM demand | [lilting.ch](https://lilting.ch/en/articles/local-long-video-fastwan-framepack-rocm) (earlier report) |

- A laptop owner believed hours of video inference "fried" his RTX 4050; commenters blamed cooling **[Reddit, earlier report]** ([1vlqwme](https://www.reddit.com/r/StableDiffusion/comments/1vlqwme/)).

### Inferences
- **[estimate]** The 3050 Laptop runs Z-Image ~3x faster per step than a 4 GB RX 470 at 512 px, so the 1050 Ti numbers are a pessimistic bound for the owner's laptop. Plan with a power cap and overnight batches.

### Gaps
- No RTX 3050 6 GB or GTX 1650 measurements were found for SDXL anime models, Z-Image at 1 MP, or Wan 5B. No YouTube benchmark video was found for the 3050 Laptop with these models.

## Q8. AI anime series on YouTube today, and what viewers say about AI-animation quality

### Takeaway
Hour-long AI anime-story channels mostly pan and zoom on stills, with a few image-to-video shots. Viewers and YouTube are both hostile to "AI slop": YouTube is testing a viewer pop-up asking whether a video "feels like AI slop", and its CEO made reducing slop a 2026 priority. No survey measures anime viewers' tolerance for AI flicker or morphing specifically.

### Cited Findings
- YouTube is testing a pop-up asking viewers if a video "feels like AI slop" (March 2026); YouTube hasn't said how responses are weighted ([Digital Trends](https://www.digitaltrends.com/movies/youtube-is-now-asking-viewers-if-videos-feel-like-ai-slop/)). The CEO's 2026 letter names reducing "AI Slop" as central ([Variety, earlier report](https://au.variety.com/2026/digital/news/youtube-channels-using-ai-tools-reduce-slop-neal-mohan-letter-32190/); [ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026)). Creators worry an August 2026 view-counting change favours AI volume, "especially in the animation space or artist space" ([Spokesman-Review](https://www.spokesman.com/stories/2026/aug/23/youtubers-worry-that-a-new-policy-will-lead-to-mor/)).
- "No representative survey of microdrama viewers has been published" on whether they mind machine-made video ([aidramareviews](https://aidramareviews.com/guides/ai-slop-do-viewers-care.html)). An AI microdrama series, *Fruit Love Island*, moved to YouTube after TikTok removals ([Wikipedia](https://en.wikipedia.org/wiki/Fruit_Love_Island)). Viewers mocked a glitching AI-narrated channel ([Futurism](https://futurism.com/artificial-intelligence/ai-slop-youtube-channel-glitches-bizarre)).
- (earlier report) Commenters say most hour-long AI anime-story videos "just pan/zoom on stills" with a few image-to-video shots; advice is to "only animate the 2-3 most important moments"; "the writing is the moat"; "if your character looks different every scene ... people immediately disconnect" **[Reddit]** ([r/aitubers 1wqgx16](https://www.reddit.com/r/aitubers/comments/1wqgx16/); [1ueqq68](https://www.reddit.com/r/aitubers/comments/1ueqq68/); [1v621co](https://www.reddit.com/r/aitubers/comments/1v621co/)). An auto-scrolling motion comic drew hostile replies ([r/manhwa 1t4yd80](https://www.reddit.com/r/manhwa/comments/1t4yd80/)).
- (earlier report) YouTube's inauthentic-content rule (from 15 July 2025) bans "AI-generated content made with generic or unoriginal templates" and "image slideshows ... with minimal or no narrative", but allows "a series following a set of characters across episodes" ([YouTube policy](https://support.google.com/youtube/answer/1311392)). Animated AI content needs no disclosure label ([YouTube Help](https://support.google.com/youtube/answer/14328491)).

### Inferences
- **[estimate]** The visible failure modes viewers punish (identity drift between shots, morphing limbs, flicker, invented objects) are exactly where AI video on 4 GB is weakest. AI belongs in the stills, with motion that cannot drift: layered rigs, held drawings, compositing. AI video should be reserved for a few checked hero shots.

### Gaps
- No anime-community survey or comment analysis quantifying complaints about flicker or morphing was found. No named, monetised AI anime *series* channel with public quality data was identified this round.

## Q9. Overall ranked map: best quality per minute on each machine (licence-clean for a monetised channel)

### Takeaway
On the **laptop**, rank stills first:
- SDXL anime (Animagine 4.0) + 8-step LoRA + ControlNet + per-character LoRA
- then Z-Image Turbo as a challenger
- then Qwen-Image-Edit / FLUX.2 klein 4B for consistent edits

Then use Wan 2.2 5B Turbo GGUF for a few overnight hero clips. On the **server**: SD 1.5 + LCM drafts, isnet-anime/BiRefNet cut-outs, Real-ESRGAN OpenVINO upscales, RIFE-ncnn on AI clips only, and all compositing and rig animation. Not usable for a monetised channel: NoobAI, Pony (unclear), DMD2, 4x-AnimeSharp, RMBG-2.0, Qwen-Image-2.1, FLUX.2 klein 9B, InsightFace-based tools. FLUX.1 dev/Kontext dev is ambiguous; MiniMax H3 has territory limits and is too big.

### Cited Findings
- See Q1-Q8 for every number and licence. Key licence anchors:
  - Animagine 4.0 commercial OK ([HF](https://huggingface.co/cagliostrolab/animagine-xl-4.0))
  - Z-Image Turbo Apache-2.0 ([HF](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo))
  - FLUX.2 klein 4B Apache-2.0 ([HF](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B))
  - FLUX.3 Klein free commercial use under US$5M ([VentureBeat](https://venturebeat.com/technology/black-forest-labs-opens-flux-3-image-klein-weights-with-free-commercial-use-limited-to-smaller-businesses))
  - Wan 2.2 5B Turbo GGUF Apache-2.0 ([HF](https://huggingface.co/hum-ma/Wan2.2-TI2V-5B-Turbo-GGUF))
  - AniSora V2/V3 Apache-2.0 ([GitHub](https://github.com/bilibili/index-anisora))
  - LTX-2.x free under US$10M ([HF LICENSE](https://huggingface.co/Lightricks/LTX-2.3/blob/main/LICENSE))
  - Qwen-Image-2.1 non-commercial ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence))
  - Nunchaku Apache-2.0 ([GitHub](https://github.com/nunchaku-ai/nunchaku))

### Inferences
| Rank | Job | Laptop (RTX 3050 4 GB, 16 GB RAM) | Time per unit | Server (4-core CPU, 15 GB) | Licence |
|---|---|---|---|---|---|
| 1 | Character/creature stills | Animagine XL 4.0 + Hyper-SDXL 8-step + xinsir OpenPose/lineart ControlNet, Forge/ComfyUI | ~30-60 s per 832x1216 [estimate from measured] | SD 1.5 anime + LCM ~10-14 s at 512x768 (earlier estimate) | OK |
| 2 | Challenger stills | Z-Image Turbo GGUF/fp8 (sd.cpp, ComfyUI or Wan2GP) | ~20-25 s at 512²; ~1-2 min at ~1 MP [estimate from measured 2.17 s/it] | ~2-5 min per 1 MP image [estimate], disk permitting | Apache-2.0 |
| 3 | Consistent edits (new pose/expression of an approved design) | Qwen-Image-Edit-2509/2511 Nunchaku INT4 + offload, or FLUX.2 klein 4B GGUF | minutes per edit [estimate]; RAM-limited | no | Apache-2.0 |
| 4 | Identity lock | Per-character/creature LoRA (SD 1.5 on laptop; SDXL marginal at 4 GB) | ~1 h+ per LoRA on 6 GB (Reddit); 4 GB unconfirmed | SD 1.5 LoRA ~1.5-2 h (earlier estimate) | depends on base |
| 5 | Hero motion clips (2-4 s) | Wan 2.2 TI2V-5B Turbo GGUF Q4, 4 steps, fast/tiled VAE | ~8-20 min per attempt, ~1 in 3 usable [estimate from 1050 Ti: 29 min] | no (134 s/step measured) | Apache-2.0 |
| 6 | Face expression clips | LivePortrait + MediaPipe detector (test on anime first) | unknown | too slow | MIT code; avoid InsightFace |
| 7 | Cut-outs | (either) | seconds | isnet-anime / BiRefNet / BEN2 | Apache / MIT |
| 8 | Lip sync | (either) | real-time-ish | Whisper/Rhubarb → mouth sprites | OK (Rhubarb licence unverified) |
| 9 | Interpolation | RIFE on AI clips only, after dedup | — | rife-ncnn 2.2 s per 720p in-between (measured) | MIT |
| 10 | Upscale | — | — | Real-ESRGAN anime via OpenVINO 0.6-4.7 s (measured) | OK; not AnimeSharp |
| — | Needs a rented GPU or 32-64 GB RAM | AniSora V3.x (anime I2V, 12 GB), ToonComposer, LTX-2.x, HunyuanVideo 1.5, FramePack, Qwen-Image-Layered, See-through, LatentSync | — | — | mostly OK except territory licences |

- **[estimate]** The biggest single upgrade for "a big step up in look and motion" is outside the model list. First, raise the laptop to 32 GB RAM. That unlocks FLUX.3 Klein, LTX-2.x low-VRAM workflows and Qwen-Image-Edit more comfortably. Second, rent a 12-24 GB cloud GPU for occasional batches of AniSora or Wan clips and LoRA training. Prices were not researched.

### Gaps
- No head-to-head anime-quality comparison was found among Animagine 4.0, Illustrious, Z-Image Turbo, FLUX.2/3 Klein and Qwen-Image for original characters and creatures. A one-evening side-by-side on the laptop (same character prompt, 8 seeds each) is the only way to settle it.
- No measured numbers for any model on the owner's exact laptop: the first task should be a 3-model timing test (Animagine + Hyper 8-step, Z-Image Turbo, Wan 2.2 5B Turbo Q4 at 832x480x49 frames).
