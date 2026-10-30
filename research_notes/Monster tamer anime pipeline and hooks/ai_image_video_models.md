# Open AI image, video and 3D models for consistent GAME-STYLE assets (monster-tamer series) on a 4 GB RTX 3050 Laptop (16 GB RAM) and a 4-core CPU-only container, state as of 30 Oct 2026

**Scope note for the report writer.**
- **Target style changed mid-research.** The coordinator relayed on 30 Oct 2026 that the owner wants the series to look "like a game", not anime: 2D is fine, for example a top-down monster-tamer game or the stylized top-down 3D diorama of the owner's reference Short. Sections Q1-Q5 cover game-style assets and come first. Q6-Q12 hold the general model findings from the first pass, with anime-face tools (LivePortrait, lip sync) now lower priority.
- **Later owner constraints, 30 Oct 2026:** 2D, 2.5D and 3D are all acceptable. The budget is **8-10 hours of machine time per 60-90 s episode**, on the laptop and/or the CPU box. The ranking must be by the **best quality reachable in that budget, not by speed**. **Q14 at the end holds that final ranked recommendation**; Q13 ranks the same tools by speed.
- This extends `reports/CPU anime animation pipeline.md` (27 Oct 2026) and `research_notes/CPU anime animation pipeline/`. Numbers carried over from those are marked **(earlier report)** and were not re-checked.

Labels:
- **[measured]**: someone ran it; source and hardware are given.
- **[official]**: the maker's own claim.
- **[secondary]**: a third-party blog or aggregator.
- **[estimate]**: my arithmetic or judgement.
- **[Reddit]**: one user's anecdote.

Hardware reference:
- The RTX 3050 4 GB Laptop is GA107 Ampere with 2,048 CUDA cores ([Notebookcheck](https://www.notebookcheck.net/GeForce-RTX-3050-4GB-Laptop-GPU-vs-GeForce-RTX-3050-6GB-Laptop-GPU_10592_11576.247598.0.html)).
- The laptop's 16 GB of system RAM, not its 4 GB of VRAM, is the binding limit for most 2026 models (see Q6, Q7).

## Q1. Pixel-art and 2D game-sprite generation: which models and LoRAs, how clean is the output, and how fast on 4 GB / CPU?

### Takeaway
Pixel art suits this hardware because sprites are small: 512x512 or less, then reduced to 32-128 px. Two licence-clean generator routes exist:
- **SDXL + nerijs `pixel-art-xl` LoRA** (CreativeML OpenRAIL-M tag). An independent test found Illustrious img2img with this LoRA "remains the best option" for turning a drawing into pixel art.
- **FLUX.2 klein 4B + Limbicnation pixel-sprite LoRA** (Apache-2.0 on both; claims CC0 training data; 512x512 RGBA with transparent background, 4 steps).

Z-Image Turbo makes pixel art from text but failed at image-to-pixel-art conversion. No diffusion model outputs a true pixel grid. Every sprite needs a deterministic cleanup pass to snap it to a real grid and a fixed palette. Four open tools do this (unfake, pixelart-cleaner, Pixel Snapper, perfectPixel), and all run on CPU.

### Cited Findings
- **nerijs/pixel-art-xl**: an SDXL LoRA whose HF licence field is `creativeml-openrail-m`, on base `stable-diffusion-xl-base-1.0` ([HF README](https://huggingface.co/nerijs/pixel-art-xl/blob/main/README.md)). An aggregator lists the licence as "None" with commercial use "Yes", which conflicts with the HF field ([Comflowy](https://www.comflowy.com/model/pixel-art-xl)).
- **Illustrious img2img + pixel-art-xl** at denoise 0.6, 25 steps took **1:30 and 6.5 GB on an M1 Max** and was rated "Works". **Z-Image Turbo** text-to-image (8 steps, 1024x1024) took **~75 s warm** (87 s cold) on the same Mac. A Z-Image pixel-art LoRA in txt2img "produces proper pixel art". Every Z-Image *img2img* route failed: at denoise 0.8 "no pixel art"; at 1.0 "the source image is essentially gone"; the base model gave "grid-like noise". Verdict: "Z-Image i2i pixel art conversion isn't practical right now". Z-Image-Edit was unreleased as of April 2026 **[measured, M1 Max 64 GB]** ([lilting.ch Z-Image pixel test](https://lilting.ch/en/articles/z-image-pixel-art-conversion)).
- **Limbicnation/pixel-art-lora for FLUX.2-klein-4B** **[official card]** ([HF](https://huggingface.co/Limbicnation/pixel-art-lora)):
  - Licence: Apache-2.0, with the base "also Apache 2.0".
  - Data: "CC0 training data — 100% public domain". The card lists 1,010 images in provenance but 500 in the training table, and says a provenance manifest is in the dataset repo (unverified).
  - Prompt template: "pixel art sprite, [description], game asset, transparent background"; modifiers "16-bit", "32-bit", "chibi".
  - Settings: 512x512, 4 steps, CFG 1.0, LoRA strength 0.85-1.4. Output: "512x512 RGBA output with transparent backgrounds".
  - Limits: needs a dev build of diffusers (≥0.37.0.dev0); 1 of 15 samples was blocked by the content filter; no sprite-sheet or multi-direction support; no VRAM or timing given.
- **artificialguybr Pixel Art Redmond for FLUX.2-klein-9B** is Apache-2.0 as a LoRA, but **FLUX.2 klein 9B itself is non-commercial**, so it is unusable ([HF README](https://huggingface.co/artificialguybr/PIXELART-REDMOND-FLUXKLEIN9B/blob/main/README.md); [BFL klein blog](https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence)). Z-Image Turbo community pixel LoRAs such as "ZIT - PixelSIN" exist on Civitai with per-upload licences ([search summary; HF LoRA mirror](https://huggingface.co/Alex995647/loras-z-image-turbo)).
- **Cleanup to a true pixel grid** (open source; licences not checked):
  - **unfake** (Rust, PyPI): scale detection, colour quantization, smart downscaling, grid snapping, jaggy cleanup and a fixed-palette option ([PyPI](https://pypi.org/project/unfake/)).
  - **pixelart-cleaner**: detects "virtual pixel boundaries from luma discontinuities" and reduces each block to one pixel ([GitHub](https://github.com/Danamir/pixelart-cleaner)).
  - **Sprite Fusion Pixel Snapper**: snaps to a grid, quantizes to a palette, accepts a custom palette, and has an online version ([GitHub](https://github.com/Hugo-Dz/spritefusion-pixel-snapper)).
  - **perfectPixel**: FFT-based grid detection plus quantization ([GitHub](https://github.com/theamusing/perfectPixel)).
- Speed anchors on the owner's GPU class, from Q6 and Q11:
  - SD 1.5 at 512x512: median **2.63 it/s** on the RTX 3050 Laptop **[measured, 78 records]** (earlier report) ([vladmandic DB](https://vladmandic.github.io/sd-data/pages/benchmark-data.json)).
  - Z-Image Turbo at 512x512: **2.17 s/it** on the RTX 3050 Laptop **[measured, sd.cpp]** ([discussion #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026)).
  - SDXL at 1024x720: **55-60 s** for 15 steps on the same GPU **[measured]** ([Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner)).
  - Server CPU (earlier report): SD 1.5 UNet bf16 **2.29 s per step at 512x768**, giving an estimated ~10-14 s per 4-step LCM image **[measured + estimate]**.

### Inferences
- **[estimate]** Sprite-generation times:
  - Laptop, SDXL + pixel-art-xl at 768-1024 px with an 8-step LCM/Hyper LoRA: ~20-45 s per candidate.
  - Laptop, FLUX.2 klein 4B + pixel LoRA at 512x512 and 4 steps: plausibly ~15-40 s, if the GGUF transformer and text encoder fit with offload (untested on 4 GB).
  - Server, an SD 1.5 pixel LoRA at 512x512 with LCM: ~10 s per candidate. Pixel art is the one style where the CPU server is a real production machine.
- **[estimate]** Recommended flow: generate 4-8 candidates, have the owner pick one, cut out (Q9), snap to the true grid and a **fixed per-creature palette** with unfake or Pixel Snapper, then upscale by nearest-neighbour (integer x4-x8) for 1080x1920. Never use an AI upscaler or frame interpolation on pixel art; both blur the grid.
- **[estimate]** Licence order for pixel generators:
  1. FLUX.2 klein 4B + Apache LoRA: cleanest on paper; the CC0 data claim is unverified.
  2. SDXL base + pixel-art-xl: OpenRAIL-M; outputs usable commercially with use restrictions.
  3. Illustrious-lineage merges: check each merge's Civitai "sell images" toggle (earlier report).
  - Avoid NoobAI- and Pony-based pixel merges (earlier report).

### Gaps
- No measured pixel-art generation timing on a 4 GB RTX 3050, and no 4 GB test of FLUX.2 klein 4B.
- The licences of unfake, pixelart-cleaner, Pixel Snapper and perfectPixel were not checked.
- No source compared SD 1.5 pixel LoRAs on licence and quality.
- No source measured how often generated sprites survive grid cleanup without hand fixes.

## Q2. Consistent ORIGINAL creature sprites in several poses, directions and evolution stages

### Takeaway
No open tool reliably keeps an original creature identical across poses, directions and evolutions. The evidence supports three principles:
- **Anchor everything to one owner-approved frame**, because frame-by-frame generation drifts.
- **Lock identity with a per-creature LoRA or an edit model**: Qwen-Image-Edit-2509/2511 or FLUX.2 klein 4B (both Apache), or FLUX Kontext (licence-ambiguous).
- **Lock colour deterministically** with a fixed palette in the pixel cleanup step.

Sprite-sheet-specific open models exist only as research code: Sprite Sheet Diffusion (MIT code, CC0 data, built on AnimateAnyone). Commercial tools (Retro Diffusion, Sloyd, AutoSprite) lock identity with sprite-sheet training or pose guides.

### Cited Findings
- A 2026 review says tools handle identity drift either by training on multi-frame sprite-sheet data (Retro Diffusion's `rd-animation`, not clearly open) or by pinning a reference image on a general model **[secondary]** ([sorceress.games](https://sorceress.games/blog/spin-up-an-ai-sprite-sheet-generator-browser-based)). OpenAI's sprite-pipeline skill generates the whole strip from one approved frame because frame-by-frame generation drifts ([mcpservers listing](https://mcpservers.org/agent-skills/openai/plugins/sprite-pipeline)). A Feb 2026 diffusers tutorial keeps sprites consistent with fixed seeds and an identical negative prompt, noting that dropping the negative prompt from even one generation introduces drift ([agentbus](https://agentbus.sh/posts/how-to-build-ai-sprite-sheet-generation-with-stable-diffusion/)). Sloyd locks identity by "pinning the opening pose", with "a hand-built pose guide" behind each animation ([Sloyd](https://www.sloyd.ai/spritesheet-generator)).
- **Sprite Sheet Diffusion (SSD)**: MIT code, "directly built on top of" Moore-AnimateAnyone, training data under CC0, fine-tuned weights on Google Drive; no VRAM, timing or pixel-art notes ([GitHub](https://github.com/chenganhsieh/Sprite-Sheet-Diffusion); paper arXiv 2412.03685). An open-source sprite-sheet app renders 2x2 grids per animation but calls fal.ai, a paid cloud API ([GitHub](https://github.com/blendi-remade/sprite-sheet-creator)).
- Reference-only tools are weak at identity:
  - IP-Adapter "is doing style and vibe transfer, it was never really built to lock a specific character" **[Reddit, earlier report]** ([r/comfyui 1v62676](https://www.reddit.com/r/comfyui/comments/1v62676/)).
  - A FLUX Kontext reference pipeline passed ~84% of comic panels on a same-character check **[anecdote]** ([dev.to](https://dev.to/qcrao/character-consistency-in-ai-comics-3-tricks-that-beat-lora-training-for-me-3ad7)).
  - Illustrious needs a LoRA for original characters, and creature characters need an explicit species tag ([artificialguy guide](https://artificialguy.com/blog/illustrious-noobai-anime-guide/)).
- **Edit models for new poses and evolutions:**
  - Qwen-Image-Edit-2511 claims "significantly improved" character consistency, demonstrated on people ([unsloth GGUF card](https://huggingface.co/unsloth/Qwen-Image-Edit-2511-GGUF)). The pre-2.1 Qwen-Image family is Apache-2.0 ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence)).
  - Nunchaku runs Qwen-Image-Edit/2509 in 4-bit with transformer VRAM "as little as 3 GiB" via async offload **[official]** ([Nunchaku](https://github.com/nunchaku-ai/nunchaku)).
  - A spec article recommends **32 GB RAM** for Qwen-Image-Edit-2511 on Windows **[secondary]** ([lilting.ch](https://lilting.ch/en/articles/qwen-image-edit-2511-local-specs)).
  - Qwen-Image-Edit-2511 also has a "Multi-Angle" LoRA covering 96 camera angles (4 elevations x 8 azimuths x 3 distances), trained on 3,000+ Gaussian-splat renders **[author's description, unverified]** (same lilting.ch article). This is relevant to 4- and 8-direction sprites.
- **LoRA training on 4 GB:** an SDXL LoRA once trained in 4.5-4.9 GB in OneTrainer (FP8, batch 1), but newer builds used 12.2 GB ([OneTrainer #934](https://github.com/Nerogar/OneTrainer/issues/934)). An Illustrious character LoRA on 6 GB took ~1 h and needed 60 epochs to look "fine" **[Reddit, earlier report]** ([1l04nqv](https://www.reddit.com/r/StableDiffusion/comments/1l04nqv/)).
- **IP risk:** no model licence clears third-party IP in outputs, and anime/SDXL models learn franchise characters from tags (earlier report: [Animagine card](https://huggingface.co/cagliostrolab/animagine-xl-4.0)). A monster-tamer series must never prompt with, or img2img from, existing franchise creatures.

### Inferences
- **[estimate]** Creature workflow:
  1. The owner approves a stage-1 design: one front 3/4 sprite plus a 6-12 colour palette.
  2. Generate other poses and directions with an edit model (Qwen-Image-Edit-2509 via Nunchaku, or FLUX.2 klein 4B), or with ControlNet lineart/depth from a rough sketch or a 3D blockout (Q5). OpenPose skeletons do not fit quadrupeds or blobs.
  3. Make evolutions by editing the approved stage-1 image ("same species, larger, adds armour plates, same palette"), then re-quantize to the stage palette plus 2-3 new colours. Palette locking does more for perceived consistency in pixel art than any model.
  4. Once a creature recurs across many episodes, train a small SD 1.5 or SDXL LoRA from its approved sheet, on the laptop if an FP8 recipe fits or on a rented GPU otherwise.
- **[estimate]** A cheaper consistency trick for game style: draw or generate each creature once as a **cut-out puppet** (body, head, limbs, tail) and animate it procedurally. This is the earlier report's rig approach, and in a game look it reads as intentional, like Flash-era and modern 2D games, rather than as a shortcut.

### Gaps
- No test of any edit model on non-human creatures or pixel art.
- No VRAM or speed figure for Sprite Sheet Diffusion, and no pixel-art result from it.
- The Qwen Multi-Angle LoRA's licence and quality on stylized creatures were not checked.

## Q3. Game-style tilesets, top-down maps and isometric/diorama backgrounds

### Takeaway
Tileable textures are a solved inference-time trick: circular padding in SD/SDXL, or the A1111 "Asymmetric Tiling" extension, which is "not 100%" seamless. Proper tile sets come from **content_aware_tiles** (Wang tiles via SD inpainting) and **Tiled Diffusion** (CVPR 2025, code public). For the reference diorama look, SDXL LoRAs exist: Isometric Tile Map (voxel), Low poly, Eldritch Diorama, Isometric Cutaway, Isometric Concept (Illustrious), plus an MIT "low-poly-count" slider. Most carry the CreativeML Open RAIL++-M addendum, so check each LoRA's Civitai toggles. There is no dedicated open top-down-RPG tileset model; build maps from generated tiles with autotile/Wang logic in code.

### Cited Findings
- Circular-padding approach: an SD 1.5 rank-4 LoRA on ~20 images, with UNet/VAE convs switched to circular padding at generation ([ankaragen](https://github.com/dammy0625/ankaragen)). Discussed for diffusers in [diffusers #556](https://github.com/huggingface/diffusers/issues/556). Asymmetric Tiling "won't guarantee seamless tiling 100% of the time, but it should manage it for most prompts" ([extension README](https://huggingface.co/datasets/artdwn/sd/blob/e9c227a3eee0e5dc5fd58ce979ea43310b80c80c/stable-diffusion-webui/extensions/asymmetric-tiling-sd-webui/README.md)).
- **content_aware_tiles** generates self-tiling images, stochastic self-tiling images and **Wang tile** textures using SD inpainting models ([GitHub](https://github.com/samsartor/content_aware_tiles)). **Tiled Diffusion** (CVPR 2025) covers self-tiling, tiling existing images and 360° synthesis ([paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Madar_Tiled_Diffusion_CVPR_2025_paper.pdf); [code](https://github.com/madaror/tiled-diffusion)). A FLUX seamless-texture LoRA exists, but it sits on FLUX.1-dev, which has the licence ambiguity in Q6 ([HF](https://huggingface.co/gokaygokay/Flux-Seamless-Texture-LoRA)).
- SDXL style LoRAs for game and diorama looks:
  - [Isometric Tile Map](https://civitai.com/models/360113/stylexl-isometric-tile-map) (voxel isometric, Open RAIL++-M addendum).
  - [Low poly](https://civitai.com/models/133120/low-poly) (Open RAIL++-M addendum).
  - [Eldritch Diorama](https://civitai.com/models/1567249/eldritch-diorama-for-sdxl) (Open RAIL++-M addendum).
  - [Isometric Cutaway SDXL](https://civitai.com/models/444099/isometric-cutaway-sdxl) (licence not shown).
  - [Isometric Concept IlluXL](https://civitai.com/models/1200408/isometric-concept-illuxl) (Illustrious-based; strength 0.5-0.7 with "diorama, miniature, isometric").
  - The ntc-ai low-poly-count slider (MIT) ([HF](https://huggingface.co/ntc-ai/SDXL-LoRA-slider.low-poly-count/blob/main/README.md)).
- Civitai turns its permission toggles into a licence addendum, so each LoRA's "sell generated images" box matters (earlier report; [Civitai licensing guide](https://education.civitai.com/guide-to-licensing-options-on-civitai/)).

### Inferences
- **[estimate]** Tiles are cheap to make: 512x512, or 256x256 for pixel tiles. SD 1.5 with circular padding runs on the **server CPU (~10 s per tile with LCM)** or on the laptop in seconds. A top-down map is then assembled in code (Wang/autotile rules, or the existing pycairo compositor) at any resolution, with a slow camera pan. Full-scene isometric diorama plates (one per location) are better made on the laptop with SDXL + a diorama LoRA (~30-60 s each), cut into depth layers for parallax.
- **[estimate]** For a true 3D diorama look, the plate can be a Blender render of simple low-poly blocks (earlier report: EEVEE headless on the server at ~8-15 s per frame), with AI only texturing or painting over it.

### Gaps
- No open model trained specifically on top-down RPG tilesets was found.
- No timing for content_aware_tiles or Tiled Diffusion on 4 GB or CPU.
- Licences of the Civitai LoRAs were read from listing summaries, not from each page's permission toggles.

## Q4. AI tools that animate sprites, or that make game-like motion

### Takeaway
The only open, pixel-specific animation model found is a **Wan 2.2 I2V-A14B LoRA trained on 226 pixel-art sprite animations** (idle, walk, attack, VFX). It is Apache-2.0 in its metadata, but it needs the 14B model, which is impractical with 16 GB RAM. Game sprites need very few frames (walk 4-8, idle 2-4, attack 4-6), so **cut-out/procedural animation or a handful of generated key poses**, held like game frames, gives game-like motion at near-zero cost and no drift. Wan 2.2 TI2V-5B Turbo (Q7) can make occasional 3-4 s "cutscene" clips on the laptop overnight.

### Cited Findings
- **styly-agents/Wan2-2-pixel-animate** **[official card]** ([HF](https://huggingface.co/styly-agents/Wan2-2-pixel-animate)):
  - Base: Wan2.2-I2V-A14B.
  - Data: 226 pixel-art sprite animation videos ("attack cycles, idles, and walking cycles", plus magic effects and VFX).
  - Training buckets 8-32 frames ("up to 2 seconds at 16fps"); recommended 45 frames at 600x370.
  - Settings: 4 steps with a 4-step distillation LoRA, DDIM, shift 5.0, CFG 1.1. LoRA rank 256, ~2.3 GB.
  - Licence metadata apache-2.0, with "refer to the Wan 2.2 model license". No VRAM, timing or sample outputs shown.
- Wan 2.2 14B GGUF on an **RTX 3050 4 GB with 64 GB RAM**: "about 30 minutes for 5s video" **[Reddit, earlier report]** ([1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)).
- Frame-count guidance from a hosted tool: "a walk cycle is normally 4 to 8 frames, an idle is 2 to 4 and an attack is 4 to 6"; another puts most attack frames on the wind-up **[secondary]** ([search summary; sprite-ai.art](https://www.sprite-ai.art/pixel-animation); [spritefusion animator](https://www.spritefusion.com/pixel-art-animator)).
- Local pipelines:
  - **Spriterrific**: a local Python pipeline for AI pixel spritesheets (idle, attack, hurt, death, walk, jump, crouch), with pixel-snapped or "richer mixed-pixel" output ([PyPI](https://pypi.org/project/spriterrific/)).
  - **sprite-animator**: produces a sheet, slices frames and builds a GIF, but needs a Google Gemini API key (cloud) ([PyPI](https://pypi.org/project/sprite-animator/)).
- Earlier report (measured on the server): a cut-out puppet frame costs ~25-60 ms (remap 2.1 ms, head rotation 0.8 ms, composite of 8 parts 23.5 ms at 1080x1920).

### Inferences
- **[estimate]** Ranked sprite-animation routes for this hardware:
  1. **Procedural cut-out animation** of approved creature and character parts (bob, squash/stretch, tail and ear springs, hit-flash, knockback, dissolve), stepped at 8-12 fps like real game sprites, with a smooth 24-30 fps camera. Milliseconds per frame on the server; zero drift.
  2. **Generated key poses** (2-6 per action) from the edit model in Q2, cleaned to the same palette and played as a sprite cycle. ~1-3 min of laptop time per pose.
  3. **Wan 2.2 TI2V-5B Turbo** on the laptop for a few non-pixel "cutscene" shots (~8-20 min per attempt, ~1 in 3 usable; see Q7).
  4. **Wan2-2-pixel-animate LoRA (14B)** only on a rented GPU. Its 600x370 output would still need grid cleanup.
- **[estimate]** Game look also comes from presentation rather than AI: UI boxes, HP bars, battle menus, "A wild ___ appeared"-style text drawn procedurally, screen shake and flash frames. The existing pycairo renderer already does these.

### Gaps
- No quality samples or VRAM/time for the Wan pixel-animate LoRA.
- No open sprite-animation model that runs on 4 GB was found.
- Spriterrific's underlying generator and licence were not checked.

## Q5. Open image/text-to-3D for low-poly creatures on 4 GB or CPU (TripoSR, Hunyuan3D-2mini, TRELLIS.2, TripoSG, SF3D, SPAR3D) and auto-rigging

### Takeaway
For the "stylized top-down 3D diorama" look:
- **Hunyuan3D-2mini (0.6B, mesh-only)** is the best fit for the 4 GB laptop: ~3 GB mesh-only per its Pinokio packager, 5 GB per ComfyUI docs, "1~5 sec" per mesh. Its licence excludes the EU/UK/South Korea (India is fine), and outputs may not be used to improve other AI models. Texture generation needs 12-16+ GB, so colour the mesh another way.
- **TripoSR** (MIT, code and weights) is the fallback: ~6 GB at default settings, claims to run without a GPU, so it is the only one plausible on the CPU server (~30 s per mesh, single unverified blog).
- TRELLIS.2 (MIT; official 24 GB, community GGUF 6-8 GB), TripoSG (MIT; >8 GB), SF3D (~7 GB; Stability Community Licence, free under US$1M revenue) and SPAR3D (10.5 GB, 7 GB low-VRAM) need more VRAM.
- None produces native low-poly topology. Decimate in Blender and flat-shade with vertex or palette colours.
- **UniRig** (MIT) auto-rigs meshes but is released progressively and untested on quadrupeds.

### Cited Findings
- **TripoSR** **[official]** ([GitHub](https://github.com/VAST-AI-Research/TripoSR)):
  - "released under the MIT license, which includes the source code, pretrained models".
  - "default options takes about 6GB VRAM for a single image input"; "less than 0.5 seconds on an NVIDIA A100".
  - Vertex colours by default, `--bake-texture` for a texture; a CPU build of torchmcubes is supported.
  - Stability's launch post says it is accessible "with or without GPUs" ([Stability AI](https://stability.ai/news-updates/triposr-3d-generation)).
  - CPU timing: "roughly 30 seconds per mesh" in one tutorial **[secondary, unverified]** ([qwe.edu.pl](https://www.qwe.edu.pl/ai-tools/text-to-3d-open-source-triposr-install/)); other sites say 15-60 s ([triposrai](https://www.triposrai.com/tools/triposr-vram-optimization-calculator/)).
- **Hunyuan3D-2 family** **[official]** ([GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)):
  - DiT-v2-mini (0.6B, 2025-03-18), mini-Fast (guidance-distilled, "could half the dit inference time") and mini-Turbo (step-distilled, 2025-03-19); Paint-v2-0 (1.3B, texture) and Paint-v2-0-Turbo.
  - "6 GB VRAM for shape generation and 16 GB for shape and texture"; `--low_vram_mode`; "supports Macos, Windows, Linux".
  - ComfyUI docs: 2mini "requires only 5GB VRAM", standard 6 GB, full shape+texture 12 GB ([ComfyUI docs](https://docs.comfy.org/tutorials/3d/hunyuan3D-2)).
  - Pinokio's packager: "for the mini model i've seen it only use like 3GB vram for mesh only generation" **[developer observation]** ([X/cocktailpeanut](https://x.com/cocktailpeanut/status/1902509430031446333)).
  - Timing: "mesh generation: just 1~5sec - Mesh + Texture Generation: 30~100sec, depending on the machine" **[developer post via search]** ([ComfyUI wiki news](https://comfyui-wiki.com/en/news/2025-03-19-tencent-hunyuan3d-2-release)).
  - Hunyuan3D-2.1 needs 10 GB shape / 21 GB texture ([2.1 repo](https://github.com/tencent-hunyuan/hunyuan3d-2.1)). The Hunyuan3D-2GP fork claims 6 GB for shape ([GitHub](https://github.com/deepbeepmeep/Hunyuan3D-2GP)).
- **Hunyuan3D 2.0 licence** ("TENCENT HUNYUAN 3D 2.0 COMMUNITY LICENSE AGREEMENT") ([LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE)):
  - Territory: "worldwide ... excluding the European Union, United Kingdom and South Korea".
  - Above "1 million monthly active users" a licence request is needed.
  - "Tencent claims no rights in Outputs You generate".
  - Outputs must not be used "to improve any other AI model".
- **TRELLIS.2**: code and weights MIT. Official: "NVIDIA GPU with at least 24GB" (tested on A100/H100) ([GitHub](https://github.com/microsoft/trellis.2)). Community GGUF builds report 6-8 GB at 512 resolution **[secondary]** ([dailytopai](https://dailytopai.com/article/how-to-run-trellis-2-3d-ai-locally-on-just-6gb-vram-with-gguf-44.html); [HF trellis2-gguf mirror](https://huggingface.co/fernandotonon/QtMeshEditor-trellis2-gguf)). The GGUF set's DINOv3 encoder is under Meta's DINOv3 licence (same mirror). One user's TRELLIS.2 output was 102.65 MB and became faceted, with distorted faces, after reduction to ~4 MB **[blog]** ([krrrl](http://krrrl.blogspot.com/2026/05/2d-to-3d-trellis-2-on-6-gb-of-vram.html)).
- **TripoSG**: 1.5B; "CUDA GPU with more than 8GB"; MIT code and weights ([HF](https://huggingface.co/VAST-AI/TripoSG); [card](https://huggingface.co/gen-lab/TripoSG/blob/main/README.md)).
- **SPAR3D**: "by default ... 10.5GB"; low-VRAM mode "roughly 7GB but ... slower" ([GitHub](https://github.com/Stability-AI/stable-point-aware-3d)).
- **Stable Fast 3D**: ~0.5 s on a GPU with 7 GB; UV-unwrapped, relatively low poly count. Stability Community Licence: free commercial use under US$1M revenue, gated download ([Stability AI](https://stability.ai/news-updates/introducing-stable-fast-3d); [HF](https://huggingface.co/stabilityai/stable-fast-3d)).
- **Low-poly topology**: there is no open native low-poly generator. Meshtron targets artist-like meshes (artist dataset median 10K faces) with unclear release ([arXiv 2412.09548](https://arxiv.org/pdf/2412.09548)). CraftsMan is AGPL-3.0 and remeshes with Instant Meshes ([search summary](https://www.meshy.ai/topics/ai-low-poly-generate-or-decimate)). A vendor guide puts game assets under 50K faces (PC/console) or 10K (mobile) **[vendor]** (same source).
- **UniRig** (SIGGRAPH 2025): MIT ([LICENSE](https://github.com/VAST-AI-Research/UniRig/blob/main/LICENSE)); "open-sourced progressively". At announcement the skinning model was "coming soon" ([ComfyUI wiki](https://comfyui-wiki.com/en/news/2025-04-12-unirig-one-model-to-rig-them-all)). The ComfyUI wrapper is GPL-3.0 and also supports Make-It-Animatable ([GitHub](https://github.com/PozzettiAndrea/ComfyUI-UniRig)). Quadruped results were not found.

### Inferences
- **[estimate]** Low-poly creature route:
  1. Approved 2D concept from Q1/Q2, front 3/4 on a plain background.
  2. Hunyuan3D-2mini-Turbo mesh on the laptop (seconds to a minute).
  3. Blender Decimate to ~1-5K faces, flat shading, palette colours by face or vertex (or project the concept image), simple hand rig or UniRig test.
  4. Render as a top-down diorama in Blender EEVEE on the server (~8-15 s per frame, earlier report) or on the laptop GPU.
  - TripoSR is the CPU fallback on the server (~30 s per mesh if the blog is right) and the cleanest licence (MIT). Its quality is lower, which matters little after heavy decimation into a low-poly style.
- **[estimate]** The Hunyuan3D licence ban on using outputs "to improve any other AI model" matters if creature meshes are later used to train LoRAs or other models. Keep Hunyuan-derived meshes out of any training set, or use TripoSR/TripoSG (MIT) for anything that feeds training.
- **[estimate]** Creature animation in 3D (walk, idle, attack) still needs a rig. With no reliable quadruped auto-rigger confirmed, simple hand-made bone chains in Blender, or procedural squash/bob of a single mesh, are the realistic options.

### Gaps
- No measured run of any image-to-3D model on a 4 GB RTX 3050, and no measured CPU timing for TripoSR. An earlier sandbox rule blocked running downloaded third-party code on the server.
- No test of these models on stylized, pixel-like or chibi creature inputs.
- UniRig's current skinning release status and quadruped quality were not confirmed.
- Hunyuan3D-2mini's exact licence file (2.0 vs 2.1 terms) was read for 2.0 only.

## Q6. General still-image base models on 4 GB VRAM + 16 GB RAM: speeds, quantized variants, licences

### Takeaway
- **SDXL** in Forge/ComfyUI with an 8-step LCM/Hyper LoRA (~30-60 s per ~1 MP image, estimated from measured same-card numbers) has the richest ControlNet/LoRA ecosystem, including the game-style LoRAs above.
- **Z-Image Turbo** (Apache-2.0, 6B, 8 steps) is measured at 2.17 s/it at 512² on a 3050 Laptop and ~2 min per 1024x576 on a 4 GB GTX 1050 Ti with 16 GB RAM.
- **FLUX.2 klein 4B** (Apache-2.0) is the cleanest new base for pixel sprites (Q1) but untested on 4 GB.
- FLUX.3 Klein (free under US$5M revenue) and Qwen-Image-Edit want ~18-32 GB of system RAM.
- Non-commercial, so out: Qwen-Image-2.1 (Sept 2026), FLUX.2 klein 9B, NoobAI, DMD2. FLUX.1-dev/Kontext-dev is ambiguous.

### Cited Findings
- SDXL on this GPU (earlier report):
  - **55-60 s** per 1024x720 (15 steps), 85-115 s with a LoRA, on an RTX 3050 Laptop 4 GB ([Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner)).
  - Illustrious in Forge at 2-3 s/it on 4 GB **[Reddit]** ([1two5jr](https://www.reddit.com/r/StableDiffusion/comments/1two5jr/)).
  - Forge: "without any cmd flag, Forge can run SDXL with 4GB vram" ([Forge README](https://huggingface.co/spaces/JusticeLee/stable-diffusion-webui-forge/blob/main/README.md)).
  - SDXL-Lightning ships 1/2/4/8-step checkpoints ([HF](https://Huggingface.co/ByteDance/SDXL-Lightning)).
  - Licences (earlier report): LCM-LoRA OpenRAIL++, Hyper-SD claims no rights in outputs, **DMD2 CC BY-NC-SA (avoid)**, Animagine 4.0 commercial OK, Illustrious conflicting, NoobAI no commercial outputs, Pony unclear ([DMD2](https://huggingface.co/tianweiy/DMD2); [Animagine](https://huggingface.co/cagliostrolab/animagine-xl-4.0); [NoobAI](https://huggingface.co/Laxhar/noobai-XL-1.1)).
- **Z-Image Turbo**: Apache-2.0, 6B, "only 8 NFEs", "fits comfortably within 16G VRAM consumer devices"; the card focuses on photorealism and text ([HF](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)).
  - RTX 3050 Laptop: 2.17 s/it at 512x512 (sd.cpp). RX 470 4 GB Q4_K: 7 s/it at 512, 35 s/it at 1024 ([sd.cpp #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026)).
  - GTX 1050 Ti 4 GB + i7-8750H + 16 GB RAM: AIO fp8 at 1024x576 in ~2:06 **[Reddit]** ([1pf7986 snapshot](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z)).
  - Nunchaku 4-bit Z-Image since 2025-12-20 ([Nunchaku](https://github.com/nunchaku-ai/nunchaku)).
- **FLUX licences**:
  - FLUX.1 [dev] licence v1.1.1 §2(d): "You may use Output for any purpose (including for commercial purposes), except as expressly prohibited herein". The "Non-Commercial Purpose" definition excludes "revenue-generating activity" ([LICENSE](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md); [discussion #136](https://huggingface.co/black-forest-labs/FLUX.1-dev/discussions/136)).
  - FLUX.2 klein 4B is Apache-2.0 (9B non-commercial); VRAM "~13GB" (HF) vs "~8GB" (GitHub); GGUF from 1.83 GB ([HF](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B); [GitHub](https://github.com/black-forest-labs/flux2)).
  - **FLUX.3 Klein** (5.6B, 15 Oct 2026), FLUX Kommunity Licence: free commercial use for individuals and companies under US$5M, with output review/filtering and legal AI disclosure ([VentureBeat](https://venturebeat.com/technology/black-forest-labs-opens-flux-3-image-klein-weights-with-free-commercial-use-limited-to-smaller-businesses)). On an RTX 3060 Ti 8 GB: int8 1 MP, 16 steps, **11.1 s warm with upsampler off, 19.6 s with it on; ComfyUI RAM 18.0 GiB by default** (11.7-20.9 GiB range); 32 GB RAM recommended **[measured]** ([computingforgeeks](https://computingforgeeks.com/flux-3-klein-comfyui/)).
- **Qwen**:
  - Nunchaku supports Qwen-Image/Edit/2509 with transformer VRAM "as little as 3 GiB"; users report OOMs ([Nunchaku](https://github.com/nunchaku-ai/nunchaku); [issue #675](https://github.com/nunchux-ai/nunchaku/issues/675)).
  - **Qwen-Image-2.1 (20 Sept 2026) is Qwen Research Licence: non-commercial**, including its LoRAs ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence); [HF](https://huggingface.co/Qwen/Qwen-Image-2.1)).
- **Anima** (anime 2B DiT): model non-commercial, outputs commercial OK; 6-12 GB VRAM by report; slower than SDXL ([lilting.ch](https://lilting.ch/en/articles/anima-2b-anime-image-generation); [HF](https://huggingface.co/circlestone-labs/Anima)). Now lower priority.
- **Wan2GP** (Windows one-click, free locally) bundles Flux 1/2/3 Klein, Qwen Image, Z-Image and HiDream, and claims "select models with as little as 4 GB of VRAM" ([README, 30 Oct 2026](https://github.com/deepbeepmeep/Wan2GP)).

### Inferences
- **[estimate]** For game-style stills on the laptop, the order is: SDXL (+ pixel or diorama LoRA) > FLUX.2 klein 4B (+ pixel LoRA; needs a test) > Z-Image Turbo (txt2img only for pixel art). On the server: SD 1.5 + LCM for sprites and tiles, and Z-Image Turbo via sd.cpp as a slow fallback (~2-5 min per 1 MP image, estimated from the measured 9.2 s SDXL step), disk permitting.
- **[estimate]** Upgrading the laptop to 32 GB RAM unlocks FLUX.3 Klein, Qwen-Image-Edit and LTX workflows more than any other change.

### Gaps
- No measured Hyper/Lightning timing on 4 GB, and no 4 GB test of FLUX.2 klein 4B or FLUX.3 Klein.
- Nunchaku's Ampere and Windows support was not stated on the page read.
- Chroma, HiDream, SD 3.5 and Lumina were not re-checked.

## Q7. Image-to-video models on 4 GB / 16 GB RAM (for occasional game-cutscene shots)

### Takeaway
Only **Wan 2.2 TI2V-5B Turbo GGUF** (Apache-2.0) has a matching-hardware report: a GTX 1050 Ti 4 GB with 16 GB RAM made 1024x576x97 frames in **29 min (17 min decode)**, and "only 1 out of 3 attempts is usable". Other models are out of reach on this laptop:
- **AniSora** (Apache-2.0 V2/V3, anime-specific, 12 GB build): less relevant now the style is not anime.
- **LTX-2.x** (free under US$10M; needs 32-44 GB RAM).
- **FramePack** (6 GB minimum; ~43 GB RAM).
- **HunyuanVideo 1.5** (~14 GB official).
- **MiniMax H3** (33B; territory-limited licence).
- Wan 2.5-3.0 have no verified open weights.

### Cited Findings
- **Wan 2.2 TI2V-5B**:
  - Official single-GPU path needs 24 GB. An RTX 4090 made 5 s of 720p in 667 s at a 24,079 MiB peak **[measured]** ([computingforgeeks](https://computingforgeeks.com/run-wan-video-generation-locally/)).
  - Turbo GGUF: "very much usable with an old 4GB GPU", "4 steps is enough", 1280x704/704x1280; Q4_K_M 3.44 GB, Q8_0 5.4 GB; Apache-2.0 ([hum-ma](https://huggingface.co/hum-ma/Wan2.2-TI2V-5B-Turbo-GGUF)).
  - GTX 1050 Ti 4 GB / 16 GB RAM: fp16 + two Kijai LoRAs, 4 steps, 1024x576x97, **29 min per clip, 17 min decode, 1 in 3 usable** **[Reddit]** ([1pf7986 snapshot](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z)).
  - Wan2GP cut Wan 2.1 1080p VAE decode "28 s / 10.5 GB to 11 s / 4.7 GB" (11 Oct 2026) ([Wan2GP](https://github.com/deepbeepmeep/Wan2GP)).
  - Earlier 3050 reports: 14B ~30 min per 5 s with 64 GB RAM; 6 h 22 min for 15 s with 32 GB RAM; blurry hands at fast settings **[Reddit, earlier report]**.
- No Wan 2.5/2.6/2.7/3.0 weights on the official HF org; the last open release is Wan2.2-Animate-14B (Nov 2025) **[secondary]** ([runpod](https://www.runpod.io/articles/guides/wan-2-7-runpod); [digitalapplied](https://www.digitalapplied.com/blog/wan-3-0-reality-check-rumor-vs-shipped)).
- **Index-AniSora**: V2 (Wan2.1-14B) and V3 weights Apache-2.0. V3 "5 sec 360p video shot within 8 sec" (hardware unstated). V3.1 "12GB VRAM version"; V3.2 on Wan2.2, 8 steps; AnyMask (2025-10-31) ([GitHub](https://github.com/bilibili/index-anisora)).
- **LTX-2 Community Licence**: covers versions since 5 Jan 2026; paid licence at ≥US$10M revenue ([HF LICENSE](https://huggingface.co/Lightricks/LTX-2.3/blob/main/LICENSE)). User reports: 6 GB VRAM + 44 GB RAM ran 720p for 10 s; "at least 32GB RAM" needed ([Kijai/LTXV2_comfy #32](https://huggingface.co/Kijai/LTXV2_comfy/discussions/32)).
- **FramePack**: "At least 6GB"; a 3050 4 GB "is insufficient" ([Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/framepack-can-generate-ai-videos-locally-with-just-6gb-of-vram)). Earlier report: 56 min per 4.83 s with ~43 GB RAM on a 4060 Laptop.
- **HunyuanVideo 1.5**: 480p step-distilled (8/12 steps, ~75% faster on a 4090) ([GitHub](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)). Its licence excludes EU/UK/South Korea **[secondary]** ([ChatForest](https://chatforest.com/reviews/hunyuanvideo-tencent-open-source-video-generation/)).
- **MiniMax H3**:
  - 33.1B; weights released 3 Aug 2026; 768p, 4-15 s, native audio.
  - Licence "appears to not authorize use in the United States, European Union, United Kingdom, or South Korea" ([RunPod](https://www.runpod.io/blog/minimax-h3-the-open-weight-omni-modal-video-model-and-what-it-takes-to-run-it)).
  - Wan2GP claims 5-6 GB VRAM for 15 s at 480p ([Wan2GP](https://github.com/deepbeepmeep/Wan2GP)).
  - It "kept inventing extra people and objects" **[Reddit, earlier report]** ([1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)).
- Server CPU (earlier report): AnimateDiff ~42 s per step and Wan 2.1 1.3B ~134 s per step **[measured]**. AI video is not viable there.

### Inferences
- **[estimate]** On the 3050, a 2-3 s Wan 5B Turbo clip at ~832x480 is ~8-20 min per attempt, or ~0.5-1 h per usable shot. Reserve it for 1-3 cutscene moments per episode (evolution reveal, legendary creature entrance), with low motion, from an approved still.

### Gaps
- No measured Wan 5B time on the RTX 3050 4 GB itself, and no 4 GB reports for LTX-2.x, HunyuanVideo 1.5 or AniSora.

## Q8. Frame interpolation and upscaling (and why pixel art should skip both)

### Takeaway
RIFE (MIT; v4.7-4.10 anime-tuned; ~2.2 s per 720p in-between on the server CPU, measured earlier) and GIMM-VFI (CUDA, ~8 GB at 2K) are only for smoothing AI video clips. Never use them on pixel or sprite animation, which should stay on held frames. Upscale pixel art by **integer nearest-neighbour**. Use Real-ESRGAN anime/illustration models (OpenVINO on the server, 0.55-4.7 s per image, measured earlier) only for painted 2D plates. **4x-AnimeSharp is CC BY-NC-SA**; APISR code is GPL-3.0 with unclear weights.

### Cited Findings
- RIFE v4.7-4.10 "optimized for anime scenes"; 4.22.lite suits diffusion-generated video ([ECCV2022-RIFE](https://github.com/hzwer/ECCV2022-RIFE)). Anime "use 1 image for 2~3 frames", which breaks naive interpolation ([Practical-RIFE PR #23](https://github.com/hzwer/Practical-RIFE/pull/23)). MultiPassDedup handles duplicate frames before interpolation ([GitHub](https://github.com/routineLife1/MultiPassDedup)).
- GIMM-VFI ~7.9 GB (2K) / ~10.9 GB (4K) on V100 ([GitHub](https://github.com/GSeanCDAT/GIMM-VFI)); "cottage cheese" on extreme frames **[anecdote]** ([wanx-troopers](https://wanx-troopers.github.io/vfi.html)).
- 4x-AnimeSharp is CC BY-NC-SA 4.0 ([OpenModelDB](https://openmodeldb.info/models/4x-AnimeSharp)). APISR is GPL-3.0 code ([GitHub](https://github.com/Kiteretsu77/APISR)). Real-ESRGAN anime video models ([doc](https://github.com/eortigoza5/Real-ESRGAN/blob/master/docs/anime_video_model.md)). Server timings are in the earlier report.

### Inferences
- **[estimate]** In a game-style pipeline, interpolation's only job is smoothing the rare Wan cutscene clip after dedup. Everything else stays stepped, which is part of the game look.

### Gaps
- GIMM-VFI licence not found. No RIFE GPU timing on a 3050.

## Q9. Cut-outs, layer decomposition and transparent generation

### Takeaway
For cut-outs, use BiRefNet or open BEN2 (reported MIT) or isnet-anime (Apache-2.0); avoid **RMBG-2.0 (CC BY-NC 4.0)**. The FLUX.2 klein pixel LoRA already outputs transparent 512x512 RGBA (Q1). LayerDiffuse reportedly fails on retrained anime SDXL checkpoints. Qwen-Image-Layered (Apache-2.0) does RGBA layer decomposition but peaked at 45 GB VRAM, so it needs a rented GPU. Qwen-Image-2.1's native transparency is non-commercial.

### Cited Findings
- RMBG-2.0 CC BY-NC 4.0 ([HF](https://huggingface.co/briaai/RMBG-2.0)). BiRefNet and BEN2 base listed as MIT **[secondary]** ([zurg70](https://huggingface.co/zurg70/birefnet-desktop-models); [nukebg survey](https://github.com/yocreoquesi/nukebg/issues/431)). isnet-anime Apache-2.0, 176 MB (earlier report; [anime-segmentation](https://github.com/SkyTNT/anime-segmentation)).
- LayerDiffuse fails with NoobAI XL, Animagine XL 4.0 and Kohaku ([issue #124](https://github.com/huchenlei/ComfyUI-layerdiffuse/issues/124)).
- Qwen-Image-Layered: Apache-2.0, variable and recursive RGBA layers ([GitHub](https://github.com/QwenLM/Qwen-Image-Layered)); 45 GB peak and 120 s per 1024 px on an RTX Pro 6000 **[measured]** ([comfyui-wiki](https://comfyui-wiki.com/en/tutorial/advanced/image/qwen/qwen-image-layered)).

### Inferences
- **[estimate]** For pixel sprites, generate on a flat key colour or with the RGBA LoRA, then hard-threshold alpha during grid cleanup. Soft matting is unnecessary at pixel scale.

### Gaps
- No anime- or pixel-specific accuracy comparison of cut-out models. SAM 2/3 licences not re-checked.

## Q10. Audio-driven lip sync and face animation (LOWER PRIORITY after the style change)

### Takeaway
Game-style characters talk through dialogue boxes, portraits with 2-3 mouth frames, or bobbing sprites, so AI lip sync is unnecessary. No open, commercially clean model is tested on stylized faces. **Rhubarb Lip Sync** (audio to 2D mouth shapes) or the existing Whisper word timings drive mouth sprites. LivePortrait (MIT code; humans, cats and dogs; InsightFace detector non-commercial, MediaPipe alternative) is now low priority.

### Cited Findings
- Rhubarb Lip Sync "automatically creates 2D mouth animation from voice recordings" ([GitHub topic](https://github.com/topics/lip-sync)).
- MuseTalk works on a 256x256 face region and "frequently lose[s] identity" ([HF](https://huggingface.co/TMElyralab/MuseTalk); [OmniSync](https://arxiv.org/html/2505.21448v1)). LatentSync wants an A10/4090-class GPU; anime support is vendor-claimed only ([arXiv](https://arxiv.org/html/2412.09262v1); [WaveSpeed](https://wavespeed.ai/models/wavespeed-ai/latentsync)).
- LivePortrait Animals model (2024-08-02), "ONLY tested on Linux and Windows with NVIDIA GPU"; no anime mention ([README](https://github.com/KwaiVGI/LivePortrait)). InsightFace models are "non-commercial research purposes only"; the KJ wrapper defaults to MediaPipe ([HN](https://news.ycombinator.com/item?id=40876840)).

### Inferences
- **[estimate]** Use game-style dialogue presentation: a portrait plus text box, with mouths flapping on the voice envelope. It costs nothing and fits the new look.

### Gaps
- Rhubarb's licence was not verified.

## Q11. Real creators' measured results on low-VRAM hardware

### Takeaway
Measured numbers on 4 GB-class GPUs exist only for SD 1.5, tuned SDXL, Z-Image Turbo and Wan 2.2 (5B and 14B). Nothing was found for pixel-sprite LoRAs or image-to-3D on 4 GB.

### Cited Findings
| Task | Hardware | Result | Source |
|---|---|---|---|
| SD 1.5, 512x512 | RTX 3050 Laptop 4 GB (78 records) | median 2.63 it/s | [vladmandic DB](https://vladmandic.github.io/sd-data/pages/benchmark-data.json) (earlier report) |
| SDXL 1024x720, 15 steps, ComfyUI | RTX 3050 Laptop 4 GB | 55-60 s; 85-115 s with LoRA | [Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner) |
| Illustrious SDXL, Forge | 4 GB | 2-3 s/it [Reddit] | [1two5jr](https://www.reddit.com/r/StableDiffusion/comments/1two5jr/) |
| Illustrious i2i + pixel-art-xl, 25 steps | M1 Max 64 GB | 1:30, 6.5 GB | [lilting.ch](https://lilting.ch/en/articles/z-image-pixel-art-conversion) |
| Z-Image Turbo txt2img 1024², 8 steps | M1 Max 64 GB | ~75 s warm | [lilting.ch](https://lilting.ch/en/articles/z-image-pixel-art-conversion) |
| Z-Image Turbo 512x512, sd.cpp | RTX 3050 Laptop | 2.17 s/it | [sd.cpp #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026) |
| Z-Image Turbo AIO fp8, 1024x576 | GTX 1050 Ti 4 GB, 16 GB RAM | ~2 min [Reddit] | [1pf7986](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z) |
| Wan 2.2 5B, 1024x576x97, 4 steps | GTX 1050 Ti 4 GB, 16 GB RAM | 29 min (17 decode); 1 in 3 usable [Reddit] | same |
| Wan 2.2 14B GGUF, 5 s | RTX 3050 4 GB, 64 GB RAM | ~30 min [Reddit] | [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/) |
| FLUX.3 Klein int8 1 MP | RTX 3060 Ti 8 GB | 11-20 s warm; 18 GiB RAM | [computingforgeeks](https://computingforgeeks.com/flux-3-klein-comfyui/) |
| Hunyuan3D-2mini mesh only | unspecified | ~3 GB VRAM; 1-5 s mesh [developer] | [X](https://x.com/cocktailpeanut/status/1902509430031446333); [ComfyUI wiki](https://comfyui-wiki.com/en/news/2025-03-19-tencent-hunyuan3d-2-release) |
| TripoSR | A100 / CPU | <0.5 s (official) / ~30 s (blog, unverified) | [GitHub](https://github.com/VAST-AI-Research/TripoSR); [qwe.edu.pl](https://www.qwe.edu.pl/ai-tools/text-to-3d-open-source-triposr-install/) |

### Inferences
- **[estimate]** The 3050 is faster per step than a 1050 Ti or RX 470, so the 1050 Ti numbers are a pessimistic bound for the owner's laptop. Cap the laptop's power for overnight runs; an earlier report found a "fried" GPU anecdote ([1vlqwme](https://www.reddit.com/r/StableDiffusion/comments/1vlqwme/)).

### Gaps
- No RTX 3050 6 GB or GTX 1650 numbers for pixel LoRAs, FLUX.2 klein or image-to-3D.

## Q12. What viewers and YouTube say about AI-made animation

### Takeaway
YouTube tests a viewer "feels like AI slop" pop-up and made reducing slop a 2026 priority. Its inauthentic-content rule bans templated or slideshow AI content but allows character series with distinct storylines. No survey measures tolerance for AI flicker or morphing. Viewers punish identity drift, which favours a deterministic game-style look over raw AI video.

### Cited Findings
- AI-slop pop-up test, March 2026 ([Digital Trends](https://www.digitaltrends.com/movies/youtube-is-now-asking-viewers-if-videos-feel-like-ai-slop/)). CEO's 2026 letter ([ScaleLab](https://scalelab.com/en/why-youtube-is-cracking-down-on-ai-generated-content-in-2026)). Creators worry about AI volume "especially in the animation space" ([Spokesman-Review](https://www.spokesman.com/stories/2026/aug/23/youtubers-worry-that-a-new-policy-will-lead-to-mor/)). "No representative survey" exists on viewer tolerance ([aidramareviews](https://aidramareviews.com/guides/ai-slop-do-viewers-care.html)).
- Earlier report:
  - "If your character looks different every scene ... people immediately disconnect" ([r/aitubers 1v621co](https://www.reddit.com/r/aitubers/comments/1v621co/)).
  - Most AI story videos "just pan/zoom on stills" ([1wqgx16](https://www.reddit.com/r/aitubers/comments/1wqgx16/)).
  - The policy allows "a series following a set of characters across episodes" ([YouTube](https://support.google.com/youtube/answer/1311392)).

### Inferences
- **[estimate]** A game look (stepped sprites, fixed palettes, UI chrome, procedural effects) reads as a deliberate style, and its consistency is enforced by construction. That is the opposite of the drift and morphing viewers call slop.

### Gaps
- No data on how viewers receive AI-made pixel or game-style series specifically.

## Q13. Overall ranked map for game-style assets: best quality per minute on each machine (licence-clean)

### Takeaway
On the **laptop** (unattended GPU jobs):
- SDXL or FLUX.2 klein 4B with pixel, isometric or diorama LoRAs for creatures, characters and plates.
- Qwen-Image-Edit-2509 (Nunchaku) or FLUX.2 klein 4B for consistent poses and evolutions.
- Hunyuan3D-2mini-Turbo mesh-only for low-poly 3D creatures.
- Rarely, Wan 2.2 5B Turbo for a cutscene.

On the **server** (CPU):
- SD 1.5 + LCM pixel sprites and tiles.
- Pixel-grid and palette cleanup, cut-outs.
- TripoSR (MIT) as a CPU 3D fallback.
- All procedural sprite animation, UI and compositing, plus Blender EEVEE diorama renders.

### Cited Findings
- Licence anchors:
  - FLUX.2 klein 4B and its pixel LoRA, Apache-2.0 ([HF](https://huggingface.co/Limbicnation/pixel-art-lora)).
  - pixel-art-xl, OpenRAIL-M ([HF](https://huggingface.co/nerijs/pixel-art-xl/blob/main/README.md)).
  - Z-Image Turbo, Apache-2.0 ([HF](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)).
  - TripoSR, MIT ([GitHub](https://github.com/VAST-AI-Research/TripoSR)).
  - TripoSG, MIT ([HF](https://huggingface.co/VAST-AI/TripoSG)).
  - TRELLIS.2, MIT ([GitHub](https://github.com/microsoft/trellis.2)).
  - Hunyuan3D 2.0: territory-limited, no training other models on outputs ([LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE)).
  - SF3D: under US$1M ([Stability](https://stability.ai/news-updates/introducing-stable-fast-3d)).
  - Wan 2.2: Apache-2.0 ([hum-ma](https://huggingface.co/hum-ma/Wan2.2-TI2V-5B-Turbo-GGUF)).
  - UniRig: MIT ([LICENSE](https://github.com/VAST-AI-Research/UniRig/blob/main/LICENSE)).
  - Qwen-Image-2.1: non-commercial ([latenode](https://latenode.com/ai-trends/qwen-image-2-1-commercial-licence)).

### Inferences
| Rank | Job | Laptop (RTX 3050 4 GB, 16 GB RAM) | Server (4-core CPU, 15 GB) | Time per unit [estimate unless noted] | Licence |
|---|---|---|---|---|---|
| 1 | Pixel creature/character sprites | SDXL + pixel-art-xl (+8-step LoRA); or FLUX.2 klein 4B + Apache pixel LoRA (512² RGBA, 4 steps; test first) | SD 1.5 pixel LoRA + LCM at 512² | laptop ~20-45 s; server ~10 s per candidate | OpenRAIL-M / Apache |
| 2 | True-pixel cleanup + fixed palette | — | unfake / Pixel Snapper / pixelart-cleaner | seconds | not verified |
| 3 | Poses, directions, evolutions | Qwen-Image-Edit-2509 (Nunchaku INT4 + offload) or FLUX.2 klein 4B edit; per-creature LoRA later | — | minutes per edit; RAM-limited | Apache |
| 4 | Tiles and top-down maps | (either) | SD 1.5 + circular padding / content_aware_tiles; map assembled in code | ~10 s per tile | OK (check LoRAs) |
| 5 | Isometric/diorama plates | SDXL + Isometric Tile Map / diorama LoRAs | Blender EEVEE low-poly plates (8-15 s per frame, measured earlier) | 30-60 s per plate | Open RAIL++-M addendum; check toggles |
| 6 | Low-poly 3D creatures | Hunyuan3D-2mini(-Turbo) mesh-only (~3-5 GB), then decimate + flat colour in Blender | TripoSR on CPU (~30 s claimed) | seconds to ~1 min per mesh | Hunyuan territory-limited; TripoSR MIT |
| 7 | Sprite animation | generated key poses (2-6 per action) | procedural cut-out rig at 8-12 fps steps (25-60 ms per frame, measured earlier) | ms per frame | own code |
| 8 | Cutscene clips | Wan 2.2 TI2V-5B Turbo Q4, 4 steps | — | ~8-20 min per attempt, 1 in 3 usable | Apache |
| 9 | Dialogue | portrait + text box + mouth flaps (Whisper/Rhubarb) | same | negligible | OK |
| — | Needs rented GPU or 32+ GB RAM | Wan2-2-pixel-animate (14B), TRELLIS.2, TripoSG, SPAR3D, SF3D, Hunyuan3D texture (12-16 GB), Qwen-Image-Layered, FLUX.3 Klein (comfortably), AniSora, LTX-2.x | — | — | mostly OK |
| ✗ | Do not use | Qwen-Image-2.1, FLUX.2 klein 9B (and its LoRAs), NoobAI/Pony merges, DMD2, 4x-AnimeSharp, RMBG-2.0, InsightFace-based tools; FLUX.1-dev family only with written BFL confirmation | | | non-commercial or unclear |

- **[estimate]** The first practical step is a one-evening laptop test on one original creature:
  1. Make the creature with (a) SDXL + pixel-art-xl and (b) FLUX.2 klein 4B + pixel LoRA, then snap to a 64x64 grid and a fixed palette.
  2. Make one evolution via an edit model.
  3. Make a Hunyuan3D-2mini mesh of it.
  4. Time each step and show the owner side by side with a 2D top-down mock-up and a 3D diorama mock-up.

### Gaps
- No head-to-head quality comparison of pixel LoRAs, edit models and image-to-3D models on original creatures. Only an owner-judged test on the actual laptop can settle the ranking.
- No measured numbers on the owner's exact machine.

## Q14. FINAL RANKED RECOMMENDATION: best visual and animation quality reachable in ~10 machine-hours per 60-90 s episode (2D, 2.5D or 3D), on the 4 GB laptop and the CPU box

### Takeaway
With 8-10 machine-hours per episode, speed stops being the constraint for stills, plates, upscaling and compositing. Every route below fits the budget for those steps. The constraints that remain are consistency, failure rate (AI video keeps ~1 in 3 attempts) and the 16 GB of laptop RAM.

| Rank | Route | Why |
|---|---|---|
| **1** | **2.5D "game diorama" hybrid** | High-step AI-painted top-down/isometric plates and creature/character art, animated as layered sprites/puppets on the server, plus **4-8 overnight Wan 2.2 5B image-to-video hero shots**, all upscaled and composited on the CPU box. Uses ~6-9 laptop-hours and ~1-3 server-hours. Gives the best picture quality per machine-hour with near-zero drift. |
| **2** | **Low-poly 3D diorama** | Hunyuan3D-2mini or TripoSR creature meshes, decimated, flat-coloured and procedurally animated, rendered in Blender EEVEE. Matches the owner's top-down 3D reference and gives the best *camera and motion* quality. A 60-90 s render fits in ~3-9 server-hours at measured EEVEE speeds. It ranks second only because every creature first needs a one-time mesh, rig and animation set-up (human time), and AI image-to-3D quality on stylized creatures is untested. Once the creature library exists, it can overtake route 1. |
| **3** | **2D pixel / top-down sprite game look** | Machine cost is the lowest (≈1-3 h per episode) and consistency is the strongest (fixed palettes, true grids, stepped frames). Its visual ceiling is lower and AI pixel art needs cleanup. Best as a fallback, or as the battle-screen layer inside route 1 or 2. |
| **4** | **i2v-heavy (most shots generated by Wan 2.2 5B on the laptop)** | Within 10 h it yields only an estimated **10-25 usable 2-3 s clips** at 8-20 min per attempt and 1 in 3 usable. That leaves no time for stills, and it adds morphing and identity-drift risk. Not recommended as the main route. |
| — | **Not reachable on this hardware within budget** | AniSora, the Wan pixel-animate 14B LoRA, LTX-2.x, HunyuanVideo 1.5, MiniMax H3, TRELLIS.2 textured, Hunyuan3D texture painting. These need a rented 12-24 GB GPU or 32+ GB RAM. |

### Cited Findings
Inputs to the budget arithmetic, all from Q1-Q13 and the earlier report:
- SDXL on the RTX 3050 Laptop 4 GB: 55-60 s for 15 steps at 1024x720, 85-115 s with a LoRA **[measured]** ([Civitai 117996](https://civitai.com/models/117996/sdxl-config-comfyui-fast-generation-4gb-vram-refiner)).
- Z-Image Turbo: 2.17 s/it at 512² on the 3050 Laptop **[measured]** ([sd.cpp #1026](https://github.com/leejet/stable-diffusion.cpp/discussions/1026)); ~2 min per 1024x576 on a GTX 1050 Ti with 16 GB RAM **[Reddit]** ([1pf7986](https://reddit.sentinel-team.org/posts/1pf7986/snapshots/2025-12-06T04%3A30%3A05.61931Z)).
- Wan 2.2 TI2V-5B Turbo, 4 steps: 29 min for 1024x576x97 frames on a 4 GB GTX 1050 Ti with 16 GB RAM, 17 min of it VAE decode, "only 1 out of 3 attempts is usable" **[Reddit]** (same source). Wan 2.2 TI2V outputs 720p at 24 fps (earlier report; [Wan2.2](https://github.com/Wan-Video/Wan2.2)). Wan2GP cut Wan VAE decode ~2.5x (28 s to 11 s at 1080p, GPU unnamed) ([Wan2GP](https://github.com/deepbeepmeep/Wan2GP)).
- Hunyuan3D-2mini mesh-only: ~3 GB VRAM, mesh "1~5sec" **[developer claims]** ([X](https://x.com/cocktailpeanut/status/1902509430031446333); [ComfyUI wiki](https://comfyui-wiki.com/en/news/2025-03-19-tencent-hunyuan3d-2-release)). Shape+texture needs 12-16 GB ([ComfyUI docs](https://docs.comfy.org/tutorials/3d/hunyuan3D-2); [Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)). TripoSR: MIT, ~6 GB default ([GitHub](https://github.com/VAST-AI-Research/TripoSR)). A decimated TRELLIS.2 mesh came out "faceted" with distorted faces ([krrrl](http://krrrl.blogspot.com/2026/05/2d-to-3d-trellis-2-on-6-gb-of-vram.html)).
- Server CPU, earlier report, measured with contention noted:
  - Blender EEVEE cel render: ~8 s per frame at 720x1280 (4 samples), ~15 s at 1080x1920, 37-55 s at 16 samples.
  - Puppet frame: 25-60 ms. Satsuei/effects stack: ~180-220 ms per frame.
  - realesr-animevideov3 via OpenVINO: 0.55-0.86 s (360x640 to 1440x2560) and 1.06-1.46 s (540x960 to 4K) per frame. RealESRGAN_x4plus_anime_6B: 4.2-4.7 s per still.
  - RIFE-ncnn: 2.16 s per 720x1280 in-between; 0.65-0.8 s per output frame in batch.
  - Chatterbox Turbo voice: ~40-60 s per sentence (earlier report, from an older repo report).
- Viewers punish identity drift ("people immediately disconnect") ([r/aitubers 1v621co](https://www.reddit.com/r/aitubers/comments/1v621co/)). YouTube's policy allows "a series following a set of characters across episodes" but not templated slideshows ([YouTube](https://support.google.com/youtube/answer/1311392)).

### Inferences
**Episode model [estimate]:** 60-90 s at 24 fps = 1,440-2,160 frames, about 15-25 shots. Assume the laptop runs unattended overnight (~8-10 h, power-capped) while the CPU box works in parallel. If the owner means 10 hours *combined*, halve the hero-clip count in route 1.

**Route 1: 2.5D game-diorama hybrid. Budget per episode [estimate]:**

| Step | Machine | Settings aimed at quality, not speed | Time |
|---|---|---|---|
| New plates (3-5 per episode; reused across episodes after that) | Laptop | SDXL + isometric/diorama LoRA + ControlNet depth/lineart from a blockout, 30-40 steps, plus a 1.5x hires/img2img pass; 6-8 candidates per plate (~4-6 min each) | **2-3.5 h** |
| New creature/character poses and evolutions (8-15 per episode) | Laptop | SDXL/FLUX.2 klein 4B at full steps, or a Qwen-Image-Edit-2509 edit of the approved design; 3-4 candidates (~2-5 min each) | **1-3 h** |
| Hero i2v shots (4-8 usable, low motion, from approved stills) | Laptop overnight | Wan 2.2 TI2V-5B Turbo Q4-Q5, 4 steps, ~704x1280 or 832x480, 49-73 frames; ~12-24 attempts at ~8-20 min | **2-5 h** (cap to fit) |
| Cut-out, layers, eye/mouth sprites | Server | isnet-anime/BiRefNet; procedural sprites | minutes |
| Upscale stills once | Server | anime_6B or animevideov3 OpenVINO | ~5-15 min |
| Upscale + dedup + RIFE on hero clips | Server | animevideov3 x2-x4 at ~1 s per frame, RIFE only where motion stutters | ~10-30 min |
| Voices (Turbo) + Whisper-medium check | Server | ~20-30 sentences at 40-60 s | ~15-30 min (+ checks) |
| Puppet animation, game UI, effects, satsuei, 1,440-2,160 frames | Server | stepped sprite timing, smooth camera, compositing at ~0.25-0.4 s per frame | **~6-15 min** |
| **Total** | | | **Laptop ~6-10 h; server ~1-2 h** |

- **Why it ranks first.** It puts the laptop's hours where AI is strongest: high-step, high-resolution painted stills that the owner picks from many candidates. Motion comes from code that cannot drift. The weakest component (i2v) is confined to a few reviewed shots. Each episode also adds plates and poses to a growing library, so later episodes need fewer laptop-hours for the same quality, and the hours can shift to more hero clips.

**Route 2: low-poly 3D diorama. Budget per episode [estimate]:**
- **One-time per creature (not per episode):** Hunyuan3D-2mini-Turbo mesh (seconds) from an approved concept, Blender decimation to ~1-5K faces, flat palette colours, simple bone chain or UniRig test, and procedural idle/hop/lunge/hit actions scripted in Blender. Expect human hours per creature; machine time is minutes.
- **Per episode:** EEVEE render of 1,440-2,160 frames on the server.
  - At 720x1280 (~8 s per frame) plus animevideov3 upscale to 1080x1920 (~1 s per frame): **≈3.6-5.4 h**.
  - At native 1080x1920 (~15 s per frame): **≈6-9 h**.
  - Rendering on the laptop GPU instead would likely be many times faster (not measured), leaving laptop hours for AI-painted skyboxes, textures and a few i2v shots.
- **Quality ceiling:** real parallax, camera orbits and consistent 3D creatures. Limits: flat or vertex colours (no texture painting on 4 GB), faceting after decimation, and simple procedural motion unless someone authors keyframes.
- **When it becomes #1:** once 6-10 recurring creatures and 3-4 diorama sets exist, each new episode costs mostly unattended render time. That makes it the best quality per *production*-hour long-term, and the closest match to the owner's reference Short.

**Route 3: 2D pixel / top-down game look [estimate]:**
- Sprites: SD 1.5/SDXL/FLUX.2 klein pixel LoRAs plus grid/palette cleanup, ~10-45 s per candidate.
- Tiles: circular padding, ~10 s each.
- Sprite animation: procedural or 2-6 generated key poses per action.
- Total: ≈1-3 machine-hours per episode.
- Spend spare budget on more candidates per sprite and more key poses per action, not on interpolation or AI upscaling, both of which damage pixel art.
- The visual ceiling is lower than routes 1-2, but consistency is the highest and production is the cheapest.

**Hybrid worth testing [estimate]:** 2D AI-painted sprites (routes 1 and 3) standing in 3D low-poly diorama sets rendered in Blender (route 2). Sets get the real parallax and camera moves of 3D, while the hardest assets (creatures, faces) avoid image-to-3D quality limits. This combines the strengths of routes 1-3 within the same budget.

**Quality per production-hour, counting human time [estimate]:**
1. Pixel 2D (fastest, fewest failures).
2. 2.5D hybrid.
3. 3D diorama (high up-front human cost, then cheapest per episode).
4. i2v-heavy (lowest: most review time per usable second).

**CPU box only (laptop unavailable) [estimate]:**
1. 3D diorama EEVEE render, if assets exist.
2. Pixel 2D with SD 1.5 + LCM sprites and tiles.
3. 2.5D with SD 1.5 stills (lower ceiling).
4. No AI video (42-134 s per denoising step measured).

**Do first [estimate]:** a one-evening laptop test on one original creature in one scene, rendered three ways: route 1 (painted diorama plate + puppet + one Wan clip), route 2 (Hunyuan3D-2mini mesh in a Blender diorama) and route 3 (pixel sprite on generated tiles). Log machine-hours for each and have the owner judge which looks best.

### Gaps
- No step of these routes has been timed on the owner's laptop. All per-episode budgets are estimates scaled from other 4 GB GPUs, an M1 Max and the server's contended measurements.
- No measured Blender EEVEE speed on an RTX 3050 Laptop, and no measured Hunyuan3D-2mini or TripoSR run on 4 GB or on this server.
- The quality gain of more SDXL steps or hires passes beyond ~30 steps was not quantified by any source found.
- Human hours per creature for 3D rigging and procedural animation were not researched here.
