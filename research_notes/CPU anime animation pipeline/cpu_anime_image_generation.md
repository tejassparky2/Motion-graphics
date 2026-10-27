# CPU-only AI image generation of anime-style stills (characters and backgrounds): speed, quality, character consistency, licences

Scope: whether, and how, a CPU-only Linux box (4 cores, ~15 GB RAM, ~8 GB free disk, no GPU) can make anime stills for a 60+ shot animation pipeline that ends up in monetized YouTube videos. Research date 2026-10-27.

**Local machine facts (checked on this machine on 2026-10-27 with `lscpu`, `/proc/cpuinfo`, `free -g`, `df -h`; no URL, these are first-hand):**
- CPU: "Intel(R) Xeon(R) Processor @ 2.10GHz", family 6 model 207 (5th-gen Xeon / Emerald Rapids class), KVM guest, 4 vCPUs shown as 4 cores, 1 thread per core, 8 MiB L2, 260 MiB L3.
- SIMD flags present: `avx2 avx512f avx512_vnni avx512_bf16 amx_bf16 avx_vnni f16c fma`. **AMX-BF16 is present**, which is what makes bf16 inference fast on Intel CPUs (see the runtime section).
- RAM: 15 GB total, but only ~7 GB "available" at check time (8 GB in use by other processes). No swap.
- Disk: 8.2 GB free on `/`.
- Python packages: `torch`, `diffusers`, `openvino` are **not installed**; `onnxruntime 1.29.0` is installed. Nothing was benchmarked locally in this research (that is task #15).

---

## 1. Which anime checkpoints (SD 1.5 vs SDXL), how big, and which licences are safe for monetized YouTube?

### Takeaway
On this box only SD 1.5-class anime checkpoints (~2.1 GB fp16) fit comfortably; SDXL anime models (6.9-7.1 GB single file) nearly fill the 8.2 GB free disk and need ~7 GB RAM in bf16, so they are a stretch. Licence-wise the safe picks are **Animagine XL 4.0 / 3.1 (CreativeML Open RAIL++-M, commercial use explicitly permitted)** on SDXL and **Counterfeit-V3.0, MeinaMix, AnyLoRA, Anything V3/V5 (CreativeML OpenRAIL-M + Civitai "sell generated images" allowed)** on SD 1.5; **avoid NoobAI-XL (explicit ban on monetizing "model-generated products"), Cetus-Mix / AbyssOrangeMix3 / ToonYou (selling images not allowed on Civitai), DMD2-based anything (CC BY-NC-SA)**. Most SD 1.5 anime merges carry presumed NovelAI-leak lineage, which is an unresolved provenance risk, not a licence term.

### Cited Findings

**Base licences and what they say about outputs**
- CreativeML OpenRAIL-M (SD 1.x and most SD 1.5 anime merges): "The Output You Generate. Except as set forth herein, Licensor claims no rights in the Output You generate using the Model. You are accountable for the Output you generate and its subsequent uses. No use of the output can contravene any provision as stated in the License." — [CompVis LICENSE](https://github.com/CompVis/stable-diffusion/blob/main/LICENSE)
- Fair AI Public License 1.0-SD (FAIPL; used by Illustrious v0.1, NoobAI, Pony base): "The output of this software is not covered by this license, and no contributor claims any rights to it." It has no commercial-use clause; restrictions come from a Prohibited Uses list (illegal use, harming minors, harassment, medical advice, etc.) and a copyleft duty: modified models (fine-tunes, merges) must be released under the same licence and source offered to network users. — [FAIPL 1.0-SD text](https://freedevproject.org/faipl-1.0-sd/)
- Civitai permission toggles: "Sell generated images" = "Allow users to sell the outputs of this model"; "Use on Civitai generation service"; "Use on other generation services"; "Sell this model"; "Sell merges". For SD 1.5 / SDXL 1.0 base models Civitai generates an addendum to the Open RAIL licence from these choices; for other base models the toggles are only "a clear statement of what you want" and the base licence still applies. — [Civitai licensing guide](https://education.civitai.com/guide-to-licensing-options-on-civitai/)
- In the Civitai API, these appear as `allowCommercialUse` values; "Image" corresponds to selling generated images, "RentCivit" to Civitai's generator, "Rent" to other services, "Sell"/"SellMerge" to selling the model or merges (mapping inferred from the guide's toggle list and the API values; Civitai's own API reference page has moved and could not be fetched) — [Civitai licensing guide](https://education.civitai.com/guide-to-licensing-options-on-civitai/); [old API wiki, now moved](https://github.com/civitai/civitai/wiki/REST-API-Reference)

**SDXL anime models**
- **Animagine XL 4.0** (cagliostrolab): SDXL 1.0 base retrained on 8.4M anime images, knowledge cut-off 7 Jan 2025; 3B params; licence CreativeML Open RAIL++-M "without any modifications or additional restrictions", with commercial use, modification, distribution, private use listed as permitted. Recommended 1024x1024 (also 832x1216 / 1216x832), 25-28 steps, CFG 4-7 (5 recommended), Euler a; tag-only prompts (`1girl/1boy`, character, series, rating, then quality tags `masterpiece, high score, great score, absurdres`). A 4.0 "Opt" version (2025-02-13) improves stability, anatomy, noise and colour saturation. Card notes multi-character scenes "may need careful prompt engineering" and training focused on identity more than style. — [HF model card](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- Animagine XL 4.0 files: `animagine-xl-4.0.safetensors` and `animagine-xl-4.0-opt.safetensors`, 6.94 GB each (HF API sizes). — [HF files](https://huggingface.co/cagliostrolab/animagine-xl-4.0/tree/main)
- Animagine XL 4.0 on Civitai allows all commercial toggles (Image, RentCivit, Rent, Sell, SellMerge) and no-credit use. — [Civitai API, model 1188071](https://civitai.com/api/v1/models/1188071)
- **Animagine XL 3.1**: card now says CreativeML Open RAIL++-M, commercial use permitted, and "This license supersedes any previous community license tags (e.g., FAIPL) applied to earlier versions of this repository". File 6.94 GB. Civitai: Image, RentCivit, Rent allowed. — [HF card](https://huggingface.co/cagliostrolab/animagine-xl-3.1); [Civitai API 260267](https://civitai.com/api/v1/models/260267)
- **Illustrious-XL v0.1**: FAIPL-1.0-SD; fine-tuned from KBlueLeaf/kohaku-xl-beta5; authors "don't restrict uploading or sharing results"; derivatives must be open-sourced; monetizing closed-source fine-tunes/merges prohibited; 20-28 steps, CFG 5-7.5, Euler a. — [HF card v0](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0). Later HF repos are tagged differently: v1.0 "sdxl-license" (links the SDXL Open RAIL++ licence) and v2.0 "creativeml-openrail-m" (6.94 GB). — [HF v1.0](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.0); [HF v2.0](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0). **Conflict:** on Civitai the Illustrious-XL page does *not* tick "sell generated images" (only RentCivit, Rent). — [Civitai API 795765](https://civitai.com/api/v1/models/795765)
- **NoobAI-XL (v1.1 and V-pred 1.0)**: FAIPL-1.0-SD plus added terms: "II. Commercial Prohibition — We prohibit any form of commercialization, including but not limited to monetization or commercial use of the model, derivative models, or model-generated products." File 7.11 GB. Civitai flags: RentCivit only. — [HF card v1.1](https://huggingface.co/Laxhar/noobai-XL-1.1); [HF card V-pred](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0); [Civitai API 833294](https://civitai.com/api/v1/models/833294)
- **Pony Diffusion V6 XL**: "modified Fair AI Public License 1.0-SD": "You are not permitted to run inference of this model on websites or applications allowing any form of monetization (paid inference, faster tiers, etc.). This applies to any derivative models or model merges." Civitai flags: Image (sell images) and RentCivit allowed. File 6.78 GB. — [Civitai API 257749 (description + flags)](https://civitai.com/api/v1/models/257749) (the Civitai web page returned HTTP 403 to the fetcher; the API was used)
- WAI-Illustrious-SDXL (Illustrious-based merge): Civitai flags Image, RentCivit. Nova Anime XL (Illustrious-based): Image, RentCivit, Rent. — [Civitai API 827184](https://civitai.com/api/v1/models/827184); [Civitai API 376130](https://civitai.com/api/v1/models/376130)
- **Anima** (CircleStone Labs + Comfy Org, 2026): 2B-parameter anime model built on NVIDIA Cosmos-Predict2-2B, "several million anime images and about 800k non-anime artistic images", anime knowledge cut-off Sept 2025; variants Base / Aesthetic / **Turbo ("Use at CFG 1 and 8-12 steps")**. Licence: CircleStone Labs Non-Commercial License for the model, **but** "the non-commercial restriction applies only to the Model, and not to Outputs (the generated images). You may use generated images commercially", with "generating images to use as concept art or assets for a paid product" listed as allowed. Files: 4.18 GB diffusion model + 1.19 GB Qwen3-0.6B text encoder + 0.25 GB Qwen-Image VAE. — [HF card](https://huggingface.co/circlestone-labs/Anima). stable-diffusion.cpp supports it (safetensors and GGUF). — [sd.cpp docs/anima.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/anima.md)

**SD 1.5 anime models (HF licence tag, Civitai flags, file size)**
- Anything V3: Civitai flags all commercial toggles (Image, RentCivit, Rent, Sell, SellMerge), no credit needed; `anythingV3_fp16.safetensors` 2.08 GB. The original HF repo (Linaqruf/anything-v3.0) is now gated/restricted. — [Civitai API 66](https://civitai.com/api/v1/models/66); [HF repo](https://huggingface.co/Linaqruf/anything-v3.0)
- Anything V5 (HF mirror `stablediffusionapi/anything-v5`): creativeml-openrail-m, diffusers format (UNet 3.44 GB fp32). The Civitai page id 9409 is now titled "万象熔炉 | Anything XL" with all commercial toggles. — [HF](https://huggingface.co/stablediffusionapi/anything-v5); [Civitai API 9409](https://civitai.com/api/v1/models/9409)
- Counterfeit-V3.0: creativeml-openrail-m; HF files include `Counterfeit-V3.0_fix_fp16.safetensors` 2.13 GB; Civitai flags Image, RentCivit. — [HF](https://huggingface.co/gsdf/Counterfeit-V3.0); [Civitai API 4468](https://civitai.com/api/v1/models/4468)
- MeinaMix: creativeml-openrail-m; `meinamix_v12Final.safetensors` 2.08 GB (+ `kl-f8-anime2` VAE 0.4 GB); Civitai flags Image, RentCivit. — [HF V11](https://huggingface.co/Meina/MeinaMix_V11); [Civitai API 7240](https://civitai.com/api/v1/models/7240)
- AnyLoRA: creativeml-openrail-m; `AnyLoRA_noVae_fp16-pruned.safetensors` 2.13 GB; Civitai flags Image, RentCivit, Rent. Its Civitai description says "Training on this model is much more effective compared to NAI ... (I suspect that's because NAI is now much diluted in newer models)" — i.e., NovelAI weights are in the lineage of the anime-merge family. — [HF](https://huggingface.co/Lykon/AnyLoRA); [Civitai API 23900](https://civitai.com/api/v1/models/23900)
- Cetus-Mix: Civitai commercial flags **none**; description: "LET ME KNOW before you put this model on commercial usage". — [Civitai API 6755](https://civitai.com/api/v1/models/6755)
- AbyssOrangeMix3 (AOM3): commercial flags none. ToonYou: RentCivit only (no selling images). — [Civitai API 9942](https://civitai.com/api/v1/models/9942); [Civitai API 30240](https://civitai.com/api/v1/models/30240)
- DreamShaper 8 (general SD 1.5, the base used in LCM demos): Image, RentCivit, Rent allowed; 2.08 GB. — [Civitai API 4384](https://civitai.com/api/v1/models/4384)

**Provenance risk (NovelAI leak)**
- NovelAI's diffusion model and code leaked and were shared via torrent in October 2022. — [Scrapbox digest, Oct 2022 (second-hand via search snippet)](https://scrapbox.io/nishio-en/Image_Generation_AI_Study_Group_(Digest_October_2022))
- ASCII.jp presumes most anime SD checkpoints derive from the leaked NovelAI model and that Anything V3 was further trained on top of it; this is the author's inference, not documented fact. — [ASCII.jp (second-hand via search snippet)](https://ascii.jp/elem/000/004/124/4124486/2/)
- NovelAI's model licence is proprietary. — [Wikipedia: NovelAI](https://en.wikipedia.org/wiki/NovelAI)

### Inferences
- **Safest SDXL choice for monetized videos: Animagine XL 4.0 (Opt).** Unmodified Open RAIL++-M with commercial use stated on the card, all Civitai commercial toggles on, trained from SDXL base (not a NovelAI-lineage merge per its card). Animagine XL 3.1 is the same story. Illustrious v1.0/v2.0 look OK by HF tag, but the Civitai page's missing "sell images" toggle conflicts, so treat it as second choice.
- **Do not use NoobAI-XL or its merges/LoRAs** for a monetized channel: the added "model-generated products" ban covers YouTube videos.
- **Pony V6**: outputs can be sold (Civitai "Image" ticked; the extra restriction is about running paid inference services), so a YouTube video is probably fine, but derivatives inherit FAIPL copyleft. Lower priority than Animagine.
- **Anima** is the newest anime-specialist model and explicitly allows commercial use of outputs, but it is a 2B DiT with a Qwen-Image VAE (~5.6 GB of files), so CPU speed is unknown and probably minutes per image (see section 3).
- **SD 1.5 route** (the one that fits this machine): Counterfeit-V3.0, MeinaMix, AnyLoRA, Anything V3/V5 all have OpenRAIL-M + "sell images" ticked. Their NovelAI-leak ancestry is a residual, unlitigated risk (no takedowns or cases found); if the owner wants zero provenance doubt, the clean options are SDXL Animagine (too heavy here) or a non-anime clean SD 1.5 base + style LoRA.
- Images stay subject to each licence's use restrictions (OpenRAIL Attachment A / FAIPL Prohibited Uses) — e.g., no harassment/defamation, no medical advice. That matters for the doctor channel if the same models are reused there (FAIPL bans "Provide medical advice").

### Gaps
- No side-by-side, measured quality comparison of SD 1.5 anime merges vs Animagine 4.0 vs Anima was found; quality claims above are from model cards only.
- Civitai's current API reference page (developer.civitai.com) returned 404, so the exact enum-to-label mapping is inferred.
- Whether Civitai's generated "addendum" for SD 1.5 models is legally binding on downstream users is not stated by Civitai.
- No court case, DMCA takedown, or NovelAI statement about downstream users of Anything-family merges was found.

---

## 2. Few-step acceleration usable on CPU (LCM-LoRA, Hyper-SD, TCD, SD/SDXL-Turbo, DMD2, SDXS): what works, quality trade-offs, licences

### Takeaway
For an SD 1.5 anime checkpoint on CPU, **LCM-LoRA (OpenRAIL++, 4 steps, guidance 0-2)**, **Hyper-SD15 N-step LoRAs (ByteDance OpenRAIL-style; the 8-step CFG LoRA keeps negative prompts)** and **TCD-SD15-LoRA (MIT)** all plug into any SD 1.5 derivative and are licence-safe; SDXL equivalents exist (LCM-LoRA SDXL, Hyper-SDXL). **DMD2 is CC BY-NC-SA (not usable)**; SD-Turbo/SDXL-Turbo are now under the Stability Community License (commercial OK under US$1M revenue with registration) but are not anime models and SD-Turbo is SD 2.1-based, so SD 1.5 anime LoRAs do not apply.

### Cited Findings
- **LCM-LoRA SD1.5**: cuts inference to "only between 2 - 8 steps"; 67.5M params; "The adapter can be loaded with SDv1-5 or deviratives"; switch to `LCMScheduler`; "either disable `guidance_scale` or use values between 1.0 and 2.0"; also works for image-to-image. Licence tag openrail++. File 0.13 GB. — [HF card](https://huggingface.co/latent-consistency/lcm-lora-sdv1-5)
- **LCM-LoRA SDXL**: 197M params, openrail++, file 0.39 GB. — [HF card](https://huggingface.co/latent-consistency/lcm-lora-sdxl); [params table on SD1.5 card](https://huggingface.co/latent-consistency/lcm-lora-sdv1-5)
- **Hyper-SD**: `Hyper-SD15-Nstep-lora.safetensors` "for SD1.5-related models"; SD15 LoRAs for 1, 2, 4, 8 steps plus 8-step and 12-step **CFG-preserved** LoRAs that "support 5~8 guidance scales" (authors: "we strongly recommend making the 8-step CFGLora a standard configuration for all SDXL and SD15 models"); 1-step unified LoRA used with `TCDScheduler`, "Lower eta results in more detail for multi-steps inference". SD15 LoRA files 0.27 GB each; SDXL 12-step CFG LoRA 0.79 GB. — [HF card](https://huggingface.co/ByteDance/Hyper-SD)
- **Hyper-SD licence**: the repo LICENSE.md has three parts — FLUX.1-dev Non-Commercial for FLUX LoRAs, Stability Community License for SD3 LoRAs, and for "other SD-related models" a ByteDance OpenRAIL-style licence (dated 11 April 2024) with "Licensor claims no rights in the Output You generate using the Model." — [Hyper-SD LICENSE.md](https://huggingface.co/ByteDance/Hyper-SD/blob/main/LICENSE.md)
- **TCD-SD15-LoRA**: MIT licence, 0.13 GB. — [HF](https://huggingface.co/h1t/TCD-SD15-LoRA)
- **DMD2**: "released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0" (HF tag cc-by-nc-4.0). — [HF card](https://huggingface.co/tianweiy/DMD2)
- **SD-Turbo**: SD 2.1 distilled with Adversarial Diffusion Distillation, 1-4 steps, "does not make use of guidance_scale or negative_prompt", prefers 512x512; card: "For commercial use, please refer to https://stability.ai/license". — [HF card](https://huggingface.co/stabilityai/sd-turbo). Its LICENSE.md is the **Stability AI Community License (updated 5 July 2024)**: free commercial use for individuals/orgs under US$1,000,000 annual revenue, must register at stability.ai/community-license, "You own any outputs generated from the Models", and outputs may not be used to train foundational models. — [SD-Turbo LICENSE.md](https://huggingface.co/stabilityai/sd-turbo/blob/main/LICENSE.md)
- **SDXL-Turbo**: LICENSE.md is also the Stability AI Community License (5 July 2024) — [LICENSE.md](https://huggingface.co/stabilityai/sdxl-turbo/blob/main/LICENSE.md); **conflict**: the HF metadata tag still says `sai-nc-community` — [HF card](https://huggingface.co/stabilityai/sdxl-turbo) — and FastSD CPU labels SD Turbo and SDXL Turbo "research-only" — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu). SDXL-Turbo files: fp16 single file 6.94 GB, fp32 13.88 GB. — [HF files](https://huggingface.co/stabilityai/sdxl-turbo/tree/main)
- **SDXS-512-0.9**: openrail++; 1-step, needs `--cfg-scale 1 --steps 1`, uses a tiny autoencoder; called "incredibly fast" by sd.cpp docs. — [HF](https://huggingface.co/IDKiro/sdxs-512-0.9); [sd.cpp distilled_sd.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/distilled_sd.md)
- **Anima-Turbo**: distilled, "CFG 1 and 8-12 steps", "only slightly worse than Anima-Aesthetic" but "reduces diversity" with "a strong default style". — [HF card](https://huggingface.co/circlestone-labs/Anima)
- sd.cpp LCM usage: "set `--cfg-scale` to `1.0` ... For `--steps`, a range of `2-8` steps is recommended. For `--sampling-method`, `lcm`/`euler_a` is recommended", LoRA loaded inline with `<lora:lcm-lora-sdv1-5:1>`. — [sd.cpp docs/lcm.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/lcm.md)
- FastSD CPU supports LCM, LCM-LoRA (`lcm-lora-sdv1-5`, `lcm-lora-sdxl`), SD/SDXL-Turbo, SDXS, SDXL-Lightning, Hyper-SD (SDXL and SD 1.5 1-step), and lets you add Civitai single-file SD 1.5/SDXL checkpoints by path; "A guidance scale above 1 increases RAM use and slows inference". — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)

### Inferences
- Guidance (CFG) matters double on CPU: CFG > 1 runs the UNet twice per step (or a batch of 2), so LCM/Hyper/TCD at CFG 1 is ~2x cheaper per step than a normal 20-30 step CFG-7 run, on top of using 4-8x fewer steps. That combined ~10x is what makes CPU viable.
- Practical default for this pipeline: SD 1.5 anime checkpoint + LCM-LoRA (or Hyper-SD15 4-step / TCD) at 4-6 steps, CFG 1-1.5; switch to the Hyper-SD15 8-step CFG LoRA (CFG 5-8) when negative prompts are needed (e.g., to suppress extra fingers/text).
- Anime-specific trade-off (not measured, from general behaviour of distillation LoRAs): few-step LoRAs tend to flatten fine detail and shift the checkpoint's colour/contrast toward the LoRA's training base; lowering the LoRA weight (e.g., 0.7-0.8) and adding 1-2 steps is the usual mitigation. Must be verified on actual frames.
- Avoid DMD2 for anything monetized; treat SD/SDXL-Turbo as commercially usable only after registering for the Stability Community License (and they're not anime-tuned anyway).

### Gaps
- No published side-by-side of LCM-LoRA vs Hyper-SD vs TCD **on anime checkpoints** was found.
- No found statement on whether merging LCM/Hyper LoRAs into an OpenRAIL-M anime checkpoint creates any additional licence obligations (both are OpenRAIL-family, so likely none).

---

## 3. CPU runtimes (PyTorch, OpenVINO/optimum-intel, ONNX Runtime, stable-diffusion.cpp, FastSD CPU): real seconds per image, RAM, quantization

### Takeaway
All published CPU numbers come from bigger CPUs (12-128 cores); none from a 4-core box. They show (a) few-step SD-class models run in ~1-14 s per 512-768 px image on 12-16 core desktop/laptop CPUs, (b) OpenVINO and bf16-on-AMX each give 2-12x over naive PyTorch fp32, (c) full SDXL at 1024 px, 40 steps, is ~30 s even on 128 server cores. Scaling down to this 4-core AMX Xeon, a realistic **estimate** is ~10-30 s per 512x768 SD 1.5 + LCM frame and ~1.5-4 min per few-step SDXL 832x1216 frame (5-11 min at 28 normal steps). SD 1.5 needs ~2-3 GB RAM in sd.cpp; SDXL needs ~7 GB RAM in bf16 and its 6.9 GB checkpoint barely fits the free disk.

### Cited Findings

**FastSD CPU (rupeshs/fastsdcpu, MIT) — all on Intel Core i7-12700 (12 cores, 8P+4E, 20 threads)**
- SDXS-512-0.9, 1 step, 512x512: PyTorch 4.8 s; OpenVINO 3.8 s; OpenVINO + TAESD **0.82 s**. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- SD Turbo, 1 step, 512x512: PyTorch 7.8 s; OpenVINO 5 s; OpenVINO + TAESD 1.7 s. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- SDXL Turbo, 1 step, 512x512: PyTorch 10 s; OpenVINO 5.6 s; OpenVINO + TAESDXL 2.5 s. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- Hyper-SD SDXL, 1 step, 768x768: PyTorch 19 s; OpenVINO 13 s; OpenVINO + TAESDXL 6.3 s. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- SDXL-Lightning, 2 steps, 768x768: PyTorch 18 s; OpenVINO 12 s; OpenVINO + TAESDXL 10 s. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- FLUX.1-schnell int4, 3 steps, 512x512, OpenVINO: 4 min 30 s, ~30 GB RAM; Iris 3B Turbo int8, 4 steps, 1024x1024: ~90 s, peak ~8.4 GB RAM; FLUX.3 Image Klein int4, 4 steps, 512x512: ~36 s (edit with one reference ~72 s), 8-9 GB RAM. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- Minimum RAM: LCM 2 GB; LCM-LoRA 4 GB; OpenVINO (standard) 11 GB, ~9 GB with TAESD (TAESD saves ~2 GB). — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu); RAM figures and i7-12700 core count also tabulated (as citations, "They are not our measurements") in [LocalAIMaster, 27 Sep 2026](https://localaimaster.com/blog/image-generation-without-gpu)
- ControlNet v1.1 in FastSD works in LCM-LoRA mode only; annotators Canny, Depth, LineArt, MLSD, NormalBAE, Pose, SoftEdge, Shuffle; LoRA and multi-LoRA supported; OpenVINO img2img supported; upscalers EDSR 2x, Aura SR 4x, tiled SD upscale (no timings). — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- Independent user test (Core Ultra 7 155H laptop, 32 GB, 5 Aug 2024): SDXS-512 OpenVINO + tiny AE 1.36 s/image (~1.2-1.3 s typical); **LCM-dreamshaper-v7-openvino, 512x768, 4 steps: 13.53 s**. — [note.com (chibisuke)](https://note.com/_chibisuke/n/n23afada8420f)

**PyTorch / IPEX / OpenVINO on Intel Xeon (Hugging Face blog)**
- Sapphire Rapids r7iz.metal-16xl (64 vCPU), Stable Diffusion, 20 steps: baseline diffusers fp32 32.3 s (previous-gen Ice Lake ~45 s); jemalloc + Intel OpenMP + numactl on 32 cores 11.8 s; IPEX + **bf16 autocast (AMX) 5.4 s**; + DPMSolverMultistep 5.05 s; OpenVINO dynamic shapes 16.7 s; **OpenVINO static shape 512x512 bf16 4.7 s** (~6.5x over baseline). Software: PyTorch 1.13.1, IPEX 1.13.1, diffusers 0.14, OpenVINO 2023.0 dev. — [HF blog: Accelerating Stable Diffusion Inference on Intel CPUs](https://huggingface.co/blog/stable-diffusion-inference-intel)

**OpenVINO LCM + NNCF int8**
- Intel Core i9-10980XE (18 cores, AVX-512, no AMX), 128 GB RAM, LCM pipeline, 4 steps: average 6.54 s per image = text encoder 0.05 s + UNet (4 iterations) 4.27 s + VAE decode 2.21 s; UNet > 60% of time; PyTorch → OpenVINO+NNCF int8 speedup 1.38x; quantizing text encoder/VAE "gives little speedup and can substantially degrade accuracy"; resolution not stated. — [OpenVINO blog (Nov 2023)](https://blog.openvino.ai/blog-posts/optimizing-latent-consistency-model-for-image-generation-with-openvino-tm-and-nncf)

**SDXL on Xeon with OpenVINO**
- 2x Xeon Platinum 8592+ (2 x 64 cores, AMX), SDXL 1.0, 1024x1024, 40 steps: native HF ~6 min/image vs **OpenVINO ~30 s/image (12x)**, average of 30 images. Published 30 Jul 2025. — [Lenovo Press LP2261](https://lenovopress.lenovo.com/lp2261-accelerating-text-to-image-diffusion-models-openvino-intel-amx)

**stable-diffusion.cpp (leejet, MIT; GGML/GGUF)**
- Supports SD1.x/2.x/SDXL/Turbo/distilled SD, SD3, FLUX, Anima and more; LoRA "same as stable-diffusion-webui", LCM/LCM-LoRA, ControlNet with SD 1.5, IP-Adapter (SD 1.5 and SDXL incl. Plus), PhotoMaker, ADetailer, TAESD, ESRGAN upscaling, VAE tiling, flash attention. No CPU timings published in README or performance guide. — [sd.cpp README](https://github.com/leejet/stable-diffusion.cpp); [performance.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/performance.md)
- SD 1.x memory at 512x512 txt2img: f32 ~2.8 GB, f16 ~2.3 GB, q8_0 ~2.1 GB, q4_0 ~2.0 GB; **with flash attention** f32 ~2.4 GB, f16 ~1.9 GB, q8_0 ~1.6 GB, q4_0 ~1.5 GB. Quant types: f32, f16, q8_0, q5_0/q5_1, q4_0/q4_1; convert ahead with `sd-cli -M convert ... --type q8_0`. — [sd.cpp quantization_and_gguf.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/quantization_and_gguf.md). The 2023 README also listed disk sizes for SD 1.x: f32 2.7 GB, f16 2.0 GB, q8_0 1.7 GB, q4_0 1.5 GB. — [sd.cpp README, Oct 2023 revision](https://github.com/leejet/stable-diffusion.cpp/blob/afec5051cfba088c41c12bc006bbc32c9dc5f049/README.md)
- Flash attention memory saving examples: "SD2 768x768 ~1400mb". Threads default to the number of physical cores. — [performance.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/performance.md); [sd.cpp README (via search snippet)](https://github.com/leejet/stable-diffusion.cpp)
- Only CPU data point found for sd.cpp: FLUX.1-schnell q8_0, 512x512, 20 steps on Ryzen 9 3900X (12 threads, WSL2): ~75.6 s/it, ~1,440 s per image, ~24 GB RAM (Aug 2024). — [Zenn (syoyo)](https://zenn.dev/syoyo/articles/a2779def150fbb)

**Model weights (disk) relevant to RAM/disk budgets**
- SDXL single-file fp16 checkpoints ≈ 6.78-7.11 GB (Animagine 4.0 6.94, NoobAI 7.11, Pony 6.78); SDXL UNet fp16 5.14 GB + text encoders 0.25 + 1.39 GB + VAE 0.17 GB. — [Animagine 4.0 files](https://huggingface.co/cagliostrolab/animagine-xl-4.0/tree/main); [NoobAI files](https://huggingface.co/Laxhar/noobai-XL-1.1/tree/main)
- SDXL fp32 single file 13.88 GB (SDXL-Turbo). — [SDXL-Turbo files](https://huggingface.co/stabilityai/sdxl-turbo/tree/main)
- SD 1.5 anime fp16 pruned checkpoints ≈ 2.08-2.13 GB. — [Civitai API 66](https://civitai.com/api/v1/models/66); [AnyLoRA files](https://huggingface.co/Lykon/AnyLoRA/tree/main)

**TAESD (tiny VAE)**
- Encoder/decoder ~1.2M params each vs 34M/49M for the SD VAE; "can decode Stable Diffusion's latents into full-size images at (nearly) zero cost"; but "tends to fudge fine details" and "trades a (modest) loss in quality for a (substantial) gain in speed"; MIT. — [TAESD README](https://github.com/madebyollin/taesd)

### Inferences (estimates for THIS 4-core AMX Xeon; none measured)
- **Scaling logic:** HF blog: ~5 s for 20 CFG steps on 32 SPR cores with bf16/AMX ≈ 0.25 s per (CFG) step; linear scaling to 4 cores ×8 → ~2 s per CFG step at 512x512, ~1 s per no-CFG (LCM) step. The i9-10980XE LCM figure (1.07 s/UNet step on 18 non-AMX cores) scaled ×4.5 and corrected ~2x for bf16 AMX gives a similar ~1-2.5 s/step. Real scaling is usually sub-linear (fewer cores get more memory bandwidth each), so these are pessimistic-to-middle values.
- **VAE decode is a big fixed cost on CPU:** 2.21 s on 18 cores (OpenVINO LCM blog) and ~3.3 s on the i7-12700 (SD Turbo OpenVINO 5 s vs 1.7 s with TAESD) → roughly 5-10 s on 4 cores at 512 px. TAESD removes most of it but softens detail: use TAESD for drafts/previews and the full VAE (or an anime VAE) for final frames.
- **Estimated per-frame times on this box:**

  | Setup | Resolution | Estimate per image | Basis |
  |---|---|---|---|
  | SD 1.5 anime + LCM-LoRA, 4 steps, CFG 1, OpenVINO or PyTorch bf16, TAESD | 512x512 | ~5-10 s | HF blog + OpenVINO LCM blog scaled |
  | same, full VAE | 512x768 | ~13-30 s | note.com 155H measured 13.5 s; 4 cores ≈ 1-2x slower |
  | SD 1.5 anime, 25 steps, CFG 7 (no acceleration) | 512x768 | ~1.5-3 min | ~2-3 s per CFG step x 25 + VAE |
  | SDXL anime (Animagine) + LCM/Hyper LoRA, 8 steps, CFG 1 | 832x1216 | ~1.5-4 min | Lenovo 0.75 s/step on 128 cores, scaled |
  | SDXL anime, 28 steps, CFG 5 (card defaults) | 832x1216 | ~5-11 min | Lenovo scaled ×32 (sub-linear → lower end) |
  | Anima-Turbo 2B DiT, 8-12 steps | ~1 MP | unknown, likely minutes | no CPU data anywhere |

- For 60 shots with ~3 candidates each (180 images): SD 1.5 + LCM ≈ 40-90 min; few-step SDXL ≈ 5-12 h; full-step SDXL ≈ 15-33 h. **SD 1.5 + LCM is the only route that allows real iteration on this box.** A 512x768 still can then be upscaled (section 6) for a 1080x1920 Short.
- **Memory/disk fit:** SD 1.5 (≈2-3 GB RAM in sd.cpp, ~4 GB in FastSD LCM-LoRA mode) fits easily. SDXL in bf16 needs ~7 GB for weights alone, which matches the ~7 GB currently "available" → OOM risk with no swap; fp32 SDXL (~14 GB) does not fit. On disk, one 6.94 GB SDXL checkpoint leaves ~1.3 GB of the 8.2 GB free, so OpenVINO IR conversion (a second full copy) or GGUF conversion (needs the source file plus the output) **does not fit** unless disk is freed or a pre-quantized GGUF is downloaded directly.
- **Runtime choice:** (1) PyTorch CPU + diffusers with `torch.autocast("cpu", dtype=torch.bfloat16)` uses AMX directly and gives full access to LoRA/IP-Adapter/ControlNet/inpainting APIs — most flexible. (2) OpenVINO via optimum-intel (`OVStableDiffusionPipeline`, static reshape to the target size) was the fastest in every Intel comparison (HF blog, Lenovo), but every model/LoRA combination must be exported first (disk cost). (3) stable-diffusion.cpp is the leanest on RAM/disk (q8_0 SD 1.5 ~1.7 GB on disk, ~1.6-2.1 GB RAM) and bundles LoRA, LCM, ControlNet, IP-Adapter, TAESD and ESRGAN in one binary, but publishes no CPU speeds and its bf16/AMX use is not documented. (4) FastSD CPU is a convenient wrapper (OpenVINO + LCM + ControlNet) but its fast paths are tied to specific pre-converted models; any Civitai SD 1.5 checkpoint can still be used in LCM-LoRA mode. (5) ONNX Runtime (already installed) had no current CPU SD benchmarks in this search.
- int8 (NNCF) on the UNet bought only 1.38x in Intel's own LCM test; on an AMX CPU bf16 is probably the better first step (no calibration, no quality risk).

### Gaps
- **No published benchmark on any 4-core CPU** for SD 1.5/SDXL; all scaling above is estimated. A 5-minute local test (diffusers bf16 vs OpenVINO vs sd.cpp, SD 1.5 + LCM-LoRA, 512x768, 4 steps) would replace these estimates.
- No CPU timings found for stable-diffusion.cpp on SD 1.5/SDXL, for ONNX Runtime SD pipelines in 2025-2026, or for Anima on CPU.
- Whether sd.cpp's CPU backend uses AMX-BF16 was not documented.
- IPEX (used in the HF blog) status in 2026 was not checked; its bf16 path is reportedly upstreamed into PyTorch, but this was not verified here.

---

## 4. Character consistency on CPU across 60+ shots (seed + img2img, ControlNet, IP-Adapter, reference-only, CPU LoRA training, inpainting)

### Takeaway
The CPU-affordable stack is: **fixed character "model sheet" made once → per-shot generation with IP-Adapter Plus / Plus-Face (SD 1.5 adapter ~0.1 GB, but a 2.5 GB ViT-H image encoder; embeddings can be precomputed once) + LCM-LoRA at 4 steps, optionally + ControlNet (lineart_anime or openpose) for pose**, then inpaint only the face/mouth region for expressions. ControlNet adds roughly +50-60% compute per step. Training a character LoRA on CPU has no published timings; by estimate it is a multi-hour job and the common trainers assume CUDA.

### Cited Findings
- IP-Adapter freezes the base model and adds image cross-attention layers; checkpoints "are typically ~100MB"; `set_ip_adapter_scale`: "1.0 applies the adapter at full strength; 0.5 usually balances text and image prompts"; "Load Plus when detail from the reference image matters most"; IP-Adapter Face "to generate consistent faces and characters" combined with IP-Adapter Plus for style; works with img2img and inpainting pipelines; "Precompute them [image embeddings] once instead of loading and encoding the same images every time", then load with `image_encoder_folder=None`. — [diffusers IP-Adapter guide](https://huggingface.co/docs/diffusers/main/en/using-diffusers/ip_adapter)
- Same guide's "Instant generation" recipe: SD 1.5 model + `ip-adapter_sd15.bin` + `lcm-lora-sdv1-5` + `LCMScheduler`, `set_ip_adapter_scale(0.4)`, `num_inference_steps=4`, `guidance_scale=1`. Also IP-Adapter + ControlNet (depth) and IP-Adapter masking for two characters in one frame (`ip-adapter-plus-face` with per-character masks). — [diffusers IP-Adapter guide](https://huggingface.co/docs/diffusers/main/en/using-diffusers/ip_adapter)
- File sizes: `ip-adapter-plus_sd15.safetensors` 0.1 GB, `ip-adapter-plus-face_sd15.safetensors` 0.1 GB; SD 1.5 image encoder (`models/image_encoder/model.safetensors`, ViT-H) **2.53 GB**; SDXL plus/plus-face adapters 0.85 GB each, SDXL encoder 3.69 GB; licence apache-2.0. — [h94/IP-Adapter files](https://huggingface.co/h94/IP-Adapter/tree/main)
- FaceID variants use InsightFace face embeddings instead of CLIP. — [diffusers IP-Adapter guide](https://huggingface.co/docs/diffusers/main/en/using-diffusers/ip_adapter)
- stable-diffusion.cpp supports IP-Adapter (SD 1.5 / SDXL, incl. Plus) via `--clip_vision clip_vision_h.safetensors --ip-adapter ... --ip-adapter-image ... --ip-adapter-strength 0.8`, and documents combining it with ControlNet (OpenPose) for "a character, side view". — [sd.cpp docs/ip_adapter.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/ip_adapter.md)
- ControlNet anime lineart model for SD 1.5: `control_v11p_sd15s2_lineart_anime`, fp16 0.72 GB (fp32 1.45 GB), licence openrail. — [HF](https://huggingface.co/lllyasviel/control_v11p_sd15s2_lineart_anime)
- FastSD CPU: ControlNet v1.1 only in LCM-LoRA mode; annotators include LineArt and Pose; example ControlNet model ~723 MB. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- ControlNet cost: "each ControlNet increases the computational load of the inference process by about half" — [RepControlNet paper (via search snippet)](https://arxiv.org/html/2408.09240v1); one ControlNet raised serving latency 1.6x (2.9 s → 4.5 s), and multiple ControlNets run sequentially per step so overhead accumulates — [SwiftDiffusion slides (via search snippet)](https://cse.hkust.edu.hk/event/RTF2025/slides/07-weiwa-Katz_RTF.pdf); [SwiftDiffusion paper](https://arxiv.org/pdf/2407.02031)
- LCM-LoRA also works for image-to-image (same 2-8 steps). — [LCM-LoRA card](https://huggingface.co/latent-consistency/lcm-lora-sdv1-5)
- Animagine 4.0 learns named characters from tags but "recent characters may have lower accuracy"; style consistency "may require specific style tags". — [Animagine XL 4.0 card](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- CPU LoRA training: secondary guides call it "technically possible but extremely slow" / "in practice, no"; SD 1.5 LoRA guides cite 10-50 training images at 512x512 and 6 GB VRAM GPUs as the practical minimum; kohya_ss install guides assume CUDA, and a kohya sd-scripts issue shows CUDA/CPU device-mismatch errors. — [Tech Tactician guide (via search snippet)](https://techtactician.com/how-to-train-stable-diffusion-lora-models/); [LocalAIMaster LoRA guide (via search snippet)](https://localaimaster.com/blog/image-lora-training-local-guide); [kohya sd-scripts #2150 (via search snippet)](https://github.com/kohya-ss/sd-scripts/issues/2150)

### Inferences
- **Recommended consistency recipe on this box (SD 1.5):**
  1. Design each character once (owner-approved model sheet: front/3-quarter/side, fixed outfit and colour palette), generated or drawn at 512x768.
  2. Fix a character "token" prompt (hair colour/length, eye colour, outfit, accessories) and the same seed family; keep the negative prompt constant.
  3. Per shot: IP-Adapter Plus-Face (scale ~0.5-0.7) fed from the model-sheet face crop, plus LCM-LoRA 4-6 steps; precompute and cache the IP-Adapter embeddings per character so the 2.5 GB ViT-H encoder only runs once (it can then be deleted from RAM/disk if disk is tight).
  4. Add ControlNet openpose or lineart_anime only for shots needing a specific pose/composition (+~50% time).
  5. For expressions/mouth shapes: inpaint just the face/mouth region at low denoise (0.3-0.5) from the approved base frame instead of regenerating the frame — that is the cheapest and most stable way to get blink/mouth variants for 2D animation.
  6. For two-character shots: IP-Adapter masks per character (diffusers supports it) or composite characters generated separately over the background (more reliable).
- **Seed + img2img at low denoise** (0.3-0.45) from the model sheet is the cheapest method of all and keeps outfit/colours, but locks the pose close to the reference; useful for small pose changes and alternates.
- **Failure modes to plan for (general knowledge, not measured here):** outfit details (buttons, logos, asymmetric accessories) drift first; hair colour shifts under strong scene lighting prompts; IP-Adapter at high scale copies the reference pose/background ("stickiness"); few-step LoRAs reduce prompt adherence for small details. Because the pipeline animates stills (2D motion on finished frames) rather than generating video, frame-to-frame flicker is not an issue; shot-to-shot drift is.
- **CPU LoRA training (estimate only):** a training step ≈ forward + backward ≈ ~3x a forward pass; with ~1-2 s per 512 px UNet forward on 4 AMX cores, that is ~3-6 s/step at batch 1, so a ~1,000-step character LoRA would be roughly 1-2 hours (assumed step count, not sourced). RAM is likely workable for SD 1.5 LoRA in bf16 with gradient checkpointing. Untested; trainers (kohya) are CUDA-oriented, so diffusers' LoRA training script on CPU via accelerate would be the more likely path. Worth trying only after IP-Adapter consistency proves insufficient.

### Gaps
- No measured CPU timings for IP-Adapter, ControlNet or inpainting were found; overhead figures are GPU/serving numbers.
- No source found with CPU LoRA training times (s/step or hours) for SD 1.5.
- "Reference-only" (ControlNet extension preprocessor in A1111/diffusers community pipeline) was not researched in depth; no CPU numbers found.
- No anime-specific evaluation of IP-Adapter Plus-Face vs FaceID on drawn faces was found (FaceID relies on InsightFace, which is trained on real faces and may fail on anime faces — unverified).

---

## 5. Anime-style backgrounds (classroom, underground concrete chamber, city crossing at dusk, hospital room): models/LoRAs

### Takeaway
Backgrounds are the easier half: they don't need identity consistency, and any of the licence-safe anime checkpoints can make them with tag prompts. Civitai has background-specific LoRAs for SD 1.5 with all commercial toggles on ("Anime Background Mix", "Anime Game Backgrounds"); several popular background LoRAs are **not** licence-safe (Pony/NoobAI/Anima-based ones with no "sell images" flag).

### Cited Findings
- Civitai background LoRAs (flags via API, sorted by downloads at query time):
  - "Anime Background Mix" — SD 1.5; Image, RentCivit, Rent, Sell, SellMerge; ~3.3k downloads. — [Civitai API 105382](https://civitai.com/api/v1/models/105382)
  - "Anime Game Backgrounds" — SD 1.5; all commercial toggles; ~3.7k downloads. — [Civitai API 16151](https://civitai.com/api/v1/models/16151)
  - "Anime Background - Style for Pony" — Pony base; all toggles; ~0.4k downloads. — [Civitai API 1176140](https://civitai.com/api/v1/models/1176140)
  - "anime bedroom background illu" — Illustrious base; all toggles. — [Civitai API 2696911](https://civitai.com/api/v1/models/2696911)
  - "Anime Style Backgrounds for Pony Diffusion" — RentCivit only (no selling images); ~8.7k downloads. — [Civitai API 337060](https://civitai.com/api/v1/models/337060)
  - "夏日晴空/日系动画场景/Anime background art style" — Anima base; commercial flags none; ~6.6k downloads. — [Civitai API 134989](https://civitai.com/api/v1/models/134989)
  - "Anime background enhancer" (Illustrious) — RentCivit only. NoobAI-based "Anime Sky/Night (Background)" — RentCivit, Rent (and NoobAI base bans monetized outputs). — [Civitai API 2281690](https://civitai.com/api/v1/models/2281690); [Civitai API 2725722](https://civitai.com/api/v1/models/2725722)
- Animagine 4.0 is tag-prompted ("Use tags only. Natural language may not work well"). — [Animagine XL 4.0 card](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- Anima covers "a wide variety of other non-photorealistic content" beyond characters, trained with ~800k non-anime artistic images; outputs commercially usable. — [Anima card](https://huggingface.co/circlestone-labs/Anima)

### Inferences
- Use the same SD 1.5 anime checkpoint as the characters (keeps line weight and palette matched) with Danbooru-style tags such as `scenery, no humans, classroom, desks, window, afternoon sunlight` / `hospital room, bed, curtains` / `city, crosswalk, dusk, street lights` / `underground, concrete, dim lighting`, optionally with a background LoRA that ticks "sell images" (Anime Background Mix / Anime Game Backgrounds), after visually checking it.
- Generate backgrounds wider/taller than the frame (e.g., 768x1152 or two 512x768 tiles + outpaint) so the 2D pipeline can pan/parallax; since backgrounds have no faces, TAESD drafts + one full-VAE final + upscale is enough.
- Backgrounds are reusable across many shots (one classroom plate for a whole episode), so they cost far less CPU time than characters per video.
- Avoid style LoRAs named after living artists or studios (e.g., "Shinkai style"): a style-mimicry/reputation risk rather than a licence term (not researched further).

### Gaps
- No quality comparison of these background LoRAs was found; download counts are only a popularity signal.
- No source tested specific scenes (concrete chamber, hospital) across anime checkpoints.

---

## 6. Upscaling stills on CPU (Real-ESRGAN anime models)

### Takeaway
Real-ESRGAN (BSD-3-Clause) has two anime-specific models — `RealESRGAN_x4plus_anime_6B` (images, ~5.9M params vs 16.7M for the general x4plus) and `realesr-animevideov3` ("XS size", for video) — and both run on CPU (PyTorch, ncnn, OpenVINO conversions, sd.cpp's built-in ESRGAN). **No published CPU seconds-per-image figure was found**; this must be measured locally.

### Cited Findings
- Real-ESRGAN licence: BSD 3-Clause. `RealESRGAN_x4plus_anime_6B.pth` is "optimized for anime images with much smaller model size"; `realesr-animevideov3` is an "Anime video model with XS size"; inference script supports `--tile` and defaults to fp16 (`--fp32` flag for full precision, needed on CPU). The portable ncnn-vulkan executables target Intel/AMD/Nvidia GPUs; tiling "may introduce block inconsistency". — [Real-ESRGAN README](https://github.com/xinntao/Real-ESRGAN); [anime_video_model.md](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_video_model.md)
- An OpenVINO IR conversion lists anime_6B at 5.9M params vs 16.7M for x4plus and claims "up to 13x faster than PyTorch", but its benchmark table had no filled-in rows. — [ibrhr/Real-ESRGAN-OpenVINO (via search snippet)](https://huggingface.co/ibrhr/Real-ESRGAN-OpenVINO)
- stable-diffusion.cpp can upscale with `--upscale-model RealESRGAN_x4plus_anime_6B.pth` directly after generation. — [sd.cpp docs/esrgan.md](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/esrgan.md)
- FastSD CPU offers EDSR 2x, Aura SR 4x (GigaGAN-based) and experimental tiled SD upscale, no timings. — [FastSD CPU README](https://github.com/rupeshs/fastsdcpu)
- Hosted Real-ESRGAN runs on an Nvidia T4 GPU (not CPU) typically finish within ~19 s. — [Replicate (via search snippet)](https://replicate.com/xinntao/realesrgan)

### Inferences
- For a 1080x1920 Short from 512x768 frames, x4 gives 2048x3072 (then downscale) — wasteful; `realesr-animevideov3` with `-s 2`/`3` (it is the smallest model) or anime_6B followed by a downscale are the two options to time. anime_6B at 512x768 input on 4 cores is probably tens of seconds per frame (estimate from model size, unmeasured); animevideov3 should be several times faster.
- Because frames are stills reused across a shot, upscaling cost is per unique frame (~60-200 per video), so even ~30 s/frame is ~0.5-1.5 h per video; batch it overnight or upscale only final picks.
- ONNX Runtime is already installed, so an ONNX export of anime_6B or animevideov3 is the zero-install way to benchmark here.

### Gaps
- No CPU timing for any Real-ESRGAN anime model was found in READMEs, issues or blogs; needs a local measurement.
- Exact `.pth` file sizes for anime_6B / animevideov3 were not verified in this session.
