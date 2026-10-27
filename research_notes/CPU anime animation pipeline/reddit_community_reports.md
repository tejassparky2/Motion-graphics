# Reddit community reports: anime-style AI video on low-end hardware, and AI anime channels on YouTube

Scope: first-hand Reddit reports (read through Reddit's API with the redditwarp tool, 27 Oct 2026) that confirm,
contradict or add to the planned pipeline: anime stills made on the owner's laptop (i7 11th gen, RTX 3050 Laptop
4 GB VRAM, system RAM unknown) and animated/composited on a CPU-only cloud server (4 cores, ~15 GB RAM), for 9:16
Shorts (~60 s) and 16:9 long videos (5-7 min).

How to read these notes:
- Every item gives post ID, subreddit, post date, score at the time of reading (27 Oct 2026) and the poster's
  hardware where stated. Text in quotation marks is copied exactly (typos kept). Scores of comments are given as "c+N".
- These are anecdotes. One person's timing is not a benchmark: drivers, OS, RAM, cooling and workflow all differ.
- "Inference" bullets are my reading of the quotes, not something a Reddit user said.
- Several model names below (MiniMax H3, Krea 2, Anima, Flux.2 Klein, LTX-2/2.3, Qwen-Image 2.1, Kandinsky 5 Lite)
  appear in 2025-2026 threads; I report what users said about them and did not verify them elsewhere.

## 1. Anime image models and workflows on 4 GB VRAM: speeds, settings, system RAM

### Takeaway
People do run SD1.5 and SDXL-based anime models (Illustrious, Pony) on 4 GB cards, but reports split sharply by
software: ComfyUI and Forge users report SDXL working (one comment says 2-3 s/it on 4 GB), while an A1111 user on an
RTX 3050 Ti 4 GB laptop reported "almost an hour" per SDXL image versus ~20 s for SD1.5. The difference users point to
is spill-over into system RAM ("sysmem fallback"), extra passes (ADetailer, upscaling) and the UI's memory handling;
system RAM (16 GB vs 32-64 GB) comes up again and again as the second bottleneck after VRAM.

### Cited Findings
**Directly comparable hardware (RTX 3050 / 3050 Ti / GTX 1650 4 GB laptops)**
- 1p9gjj7, r/StableDiffusion, 2025-11-29, 4 pts (cross-post 1p9gfw4, r/comfyui, 19 pts); hardware in title "RTX 3050
  (4GB VRAM + 64GB RAM)". Image step: "FLUX.2-dev q4_k_m with mistral_3_small_fp8 (works faster than gguf) yes on only
  4gb vram it's possible to run and generate 720p image with 14 steps in 5 minutes". On alternatives: "I have tried the
  qwen and z image turbo, but their prompt adherence is much worse and still take 1-2 minutes per generation." Anime
  style came from a second pass: "Styling: enrichment Illustrious + loras". Memory settings: "tiled VAE, model
  offloading, aggressive memory management", while "battling OOM errors every 5 minutes". —
  [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/) ; [1p9gfw4](https://www.reddit.com/r/comfyui/comments/1p9gfw4/)
- 1ovev7x, r/StableDiffusion, 2025-11-12, 0 pts, 16 comments; "RTX 3050 ti notebook version with 4gb", Automatic1111,
  Illustrious checkpoint (prefect_illustrious_v4), 832x1216, 20 steps, plus ADetailer and 4x-UltraSharp SD upscale:
  "when i generate an image with a 1.5 it takes about 20 seonds but when using a xl model it takes almost an hour".
  Replies: it is spilling into system RAM ("system-memory-fallback", c+14, u/Dezordan, who also suggests `--lowvram`);
  "Switch to dreamshaperXL turbo ... and use comfyUI because it has the optimizations" (c+2); "Most XL models start at
  6GB. If you only have 4GB, stick with SD." (c+2); "Just use SD1.5 and upscale it" (c+3); one reply says the Nvidia
  control panel can disable the fallback "that makes things extremely slow once you go beyond vram". —
  [1ovev7x](https://www.reddit.com/r/StableDiffusion/comments/1ovev7x/)
- 1hrgbnr, r/StableDiffusion, 2025-01-01, 0 pts; "RTX 3050 4Gb graphics on my laptop with Ram 16 Gb", SDXL/Pony "keep
  crashing". Reply (c+3, u/Venganza_Vz): "I have the same gpu with that amount of ram and use sdxl with no issues, use
  forge". OP (Forge, `--medvram`, bigger pagefile, full C: drive): "Somwtimes it worked using PONY but when I started
  using LORA alsong with it and embeddings, it crashed". Another reply: "You also would benefit from getting more ram". —
  [1hrgbnr](https://www.reddit.com/r/StableDiffusion/comments/1hrgbnr/)
- 1two5jr, r/StableDiffusion, 2026-06-04, 2 pts (OP has a GTX 750 Ti 4 GB, 16 GB RAM). Reply (u/KITTYCAT_5318008, own
  hardware not stated): "Forge/Forge Neo will happily run Illustrious (SDXL based, choose a finetune like WAI or Nova) or
  any sd1.5 checkpoint (MeinaMix is probably the best one here) on 4GB of VRAM (2~3 s/it for SDXL, 1~2 s/it for SD1.5).
  ... There's a new anime model called Anima, you might be able to fit a Q8_0 or Q6_K quant of it in VRAM." Another
  reply warns that the CUDA/PyTorch version an old card supports is "the hard limit on what you can use, not VRAM". —
  [1two5jr](https://www.reddit.com/r/StableDiffusion/comments/1two5jr/)
- 1p8lapx, r/StableDiffusion, 2025-11-28, 19 pts; "Acer Nitro 5 with 32GB of ram and 4GB GTX 1650", ComfyUI, Z-Image
  Turbo (quantized for low VRAM): "It's something like 37 seconds for a 512 x 512"; "I was sitting at about 22 GB of
  memory used"; the example workflow failed with out-of-VRAM until he removed its upscale stage; batches did not save
  time ("I think it's not a huge timesaver"). Reply (c+3, u/Obvious_Set5239): "You don't need to use gguf models. The
  .safetensor is faster and has better quality ... ggufs of diffusion models are needed only if you don't have enough
  RAM". — [1p8lapx](https://www.reddit.com/r/StableDiffusion/comments/1p8lapx/)
- 1pf7986, r/StableDiffusion, 2025-12-05, 2,880 pts (the most-upvoted low-VRAM post found); a comment quotes the OP's
  hardware as "4GB VRAM (NVIDIA Geforce GTX 1050 Ti) and 16 GB RAM (Intel Core i7-8750H)". Commenters identify the image
  model as quantized Z-Image Turbo. The OP's own text was not retrievable through the API (video post). The OP adds that
  on a desktop RTX 4080 the same workflow takes "4 seconds for generating image (1024 x 576 px)". —
  [1pf7986](https://www.reddit.com/r/StableDiffusion/comments/1pf7986/)
- 1ek6hsj, r/StableDiffusion, 2024-08-04 (older), 392 pts, title only: "Flux.1-dev on a laptop, RTX 3050 4 GB VRAM, 16 GB
  RAM, 10 minutes per generation but it works". — [1ek6hsj](https://www.reddit.com/r/StableDiffusion/comments/1ek6hsj/)

**Slightly larger cards (6 GB) with per-image times**
- 1tfs3ee, r/StableDiffusion, 2026-05-17, 18 pts; GTX 1060 6 GB (Pascal), ComfyUI on Windows; a self-made benchmark
  table: "SD 1.5 ... ~4GB ... ~30s"; "SDXL 1.0 ... ~5.7GB peak ... ~2-3 min"; "Illustrious XL | Mistoon Illustrious |
  ~4.9GB peak | ~2 min (24 steps, DPM++)"; "Z-Image Turbo FP16 ... ~3-4 min"; "batch generation is not practical on 6GB
  VRAM - sequential single image generation is dramatically faster." His explanation: the SDXL UNet (~4.5 GB) goes to
  VRAM while the text encoders run on CPU/RAM. On OS: "When VRAM fills up on Linux with NVIDIA, the result is a hard CUDA
  Out of Memory error - no graceful fallback, no RAM extension" (Windows WDDM "Shared GPU Memory" is what made his setup
  work). He also writes "Forge loads everything at once and crashes", although his own table marks Forge/A1111 "Not
  Tested", so that line is not first-hand. — [1tfs3ee](https://www.reddit.com/r/StableDiffusion/comments/1tfs3ee/)
- 1q588t7, r/StableDiffusion, 2026-01-06, 2 pts, title only: "11 cinematic backgrounds generated with PonyV7 Q4_0 on an RTX
  3050 6GB – pure environments, no characters". — [1q588t7](https://www.reddit.com/r/StableDiffusion/comments/1q588t7/)

**System RAM and laptop heat**
- 1lymf8b, r/StableDiffusion, 2025-07-13, 0 pts; OP: ASUS TUF F15, RTX 3050 Ti 4 GB, 16 GB RAM, asks about going to 48 GB.
  Reply (u/mmowg, c+3): "a RoG with 3050ti 4gb ram and 16gb, i upgraded it to 64gb and now i can also use FramePack, not
  so fast, but it works. So, from 16gb to 64 you will notice a BIG difference. Go for 64gb." Disagreeing reply
  (u/DelinquentTuna): "No, I'm sorry. You will not see the kinds of performance gains you are hoping for." A mobile-4090
  user (c+2) on heat: "It's getting so hot that I don't want to touch it anymore ... for training, which takes many hours,
  I prefer to rent GPUs in the cloud." — [1lymf8b](https://www.reddit.com/r/StableDiffusion/comments/1lymf8b/)
- CPU-only image generation (relevant only if the cloud server ever generates images): old titles from the FastSD CPU
  project claim "SDXL Turbo OpenVINO support (2.5 seconds on CPU)" (186t0mw, 2023-11-29) and "0.82 seconds/820
  milliseconds) with SDXS512-0.9 OpenVINO on CPU" (1bp3kvb, 2024-03-27); CPU model not stated in the titles and I did
  not read the threads. — [186t0mw](https://www.reddit.com/r/StableDiffusion/comments/186t0mw/) ;
  [1bp3kvb](https://www.reddit.com/r/StableDiffusion/comments/1bp3kvb/)

### Inferences
- The owner's GPU class can make Illustrious/SDXL anime stills, but the UI choice decides whether that means seconds-per-
  step or "almost an hour": the community advice is ComfyUI (or Forge/Forge Neo), no hires-fix/ADetailer/upscale in the
  same pass, single images rather than batches, and SD1.5 anime checkpoints as the fallback.
- The 6 GB GTX 1060 table (~2 min per Illustrious image, 24 steps) and the 2-3 s/it claim for 4 GB SDXL suggest a
  realistic range of roughly 1-2 minutes per 832x1216 Illustrious image at 20-25 steps on the 3050 Laptop, less with
  few-step LoRAs. That is my extrapolation; no thread gave a measured 3050 Laptop Illustrious time in ComfyUI.
- System RAM matters: 16 GB setups report crashes or "consumes RAM at record speed" (see section 2), while the success
  stories with bigger models have 32-64 GB. Knowing the owner's RAM is the first thing to check.
- If the laptop runs Linux rather than Windows, the GTX 1060 author's point means VRAM overflow becomes a hard OOM
  instead of a slowdown; Windows is the platform most of these 4 GB success stories used (one exception below used WSL2).

### Gaps
- No first-hand report found that gives seconds per image for LCM/Hyper-SD/DMD2/Lightning few-step anime models on a
  4 GB card; threads mention these LoRAs only for video.
- No measured tiled-VAE vs normal-VAE comparison on 4 GB.
- No thread compared Animagine directly with Illustrious on 4 GB.

## 2. AI video on 4 GB VRAM: Wan 2.1/2.2, FramePack, AnimateDiff, LTX, and newer models

### Takeaway
Image-to-video on a 4 GB card is possible but slow: the best documented numbers are ~30 min per 5 s clip (Wan 2.2 14B
GGUF, RTX 3050 4 GB + 64 GB RAM), "6 hours 22 minutes" for a 15 s MiniMax H3 clip at good settings on an RTX 3050 Laptop
4 GB + 32 GB RAM, and ~6 hours of total generation for a short film on 4 GB + 16 GB RAM. The smaller Wan 2.2 5B model with
a 4-step turbo LoRA is the one that produced the widely praised 4 GB result, but its own author says it "often
misunderstands the prompts and doesn't have good motion". Several commenters steer subtle "living still" motion away from
AI video toward parallax and particles in an editor, which is what the CPU-server plan does.

### Cited Findings
**Wan**
- 1p9gjj7 / 1p9gfw4 (RTX 3050 4 GB + 64 GB RAM, 2025-11-29): "Image-to-Video (Wan 2.2 14b gguf 5_K_M) for motion. Takes
  about 30 minutes for 5s video"; then "Restyling: I ran a pass with Illustrious again with low denoise to enforce the style
  (This is why the image flickers slightly and I'm not sure if it was necessary, might skip it next time)"; "Interpolation:
  RIFE"; plans "upscale via Wan 1.3B latent space" or FlashVSR, which "will be possible only on rented GPU". —
  [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)
- 1pf7986 (GTX 1050 Ti 4 GB + 16 GB RAM, 2025-12-05, 2,880 pts): video model per commenters is "Wan 2.2 5b with a 4-step
  Lora turbo" (c+18); the OP links Kijai's FastWan folder for the LoRAs. A commenter quotes the OP: "You don't want to wait
  30 minutes for a video to be generated" (c+48) - the exact 4 GB per-clip time was in the OP's text, which the API did
  not return. OP on his RTX 4080 desktop: "33 seconds for generating video (also 1024 x 576 px, 97 frames). ... the 5b model
  often misunderstands the prompts and doesn't have good motion" (c+37); on getting it to work: "There was always some
  flickering, and weird things kept appearing ... I tried different combinations of loras and adjusted their strength,
  and suddenly the results started to look nice" (c+8); "I also tried LTXV - it is fast, but the quality is poor and
  everything morphs." An RTX 3060 user with 16 GB RAM (in Portuguese, c+4): "demorou 12 minutos para gerar um video de 4
  segundos com resolução de 480px. A parte do Z-Imagem foi bem rapido, coisa de 20 segundos" (it took 12 minutes for a 4 s
  480p video; the Z-Image part took about 20 s) and "O problema principal é a VRAM que extrapola rápido, e consome a
  memoria ram em velocidade recorde. Se você tiver uma RTX 3060 com pouca ram (igual eu) não compensa." (VRAM overflows
  fast and eats RAM at record speed; with little RAM it isn't worth it). Disagreement: "Wan 2.2 5b has been nothing but
  hot garbage for me" (c+3). — [1pf7986](https://www.reddit.com/r/StableDiffusion/comments/1pf7986/)
- 1uey0kf, r/StableDiffusion, 2026-06-25, 56 pts; "I did this short film using 4GB VRAM and 16 GB RAM". OP on time: "6
  hours. It would be less if I just went with one generation. I just did 3 generations for both images and video, and took
  the best out of the 3, and it took me like 20 minutes to add them together with effects and transitions on CapCut". A
  commenter assumes Wan 5B FP16. Film length not stated in the readable text. —
  [1uey0kf](https://www.reddit.com/r/StableDiffusion/comments/1uey0kf/)
- 1j6cymq, r/StableDiffusion, 2025-03-08, 24 pts; RTX 4060 laptop (8 GB): "16fps 5sec video in wan2.1-i2v-14b-480p-Q4_K_M
  gguf ... It take around 100 minute to render and consume 6.2 gb of gpu memory." Replies: an RTX 3080 10 GB user did the
  same in "~12 minutes at 20 steps" with fp16; another: "Could be stuff doesn't even fit in there and instead overflow to
  the Windows page file (disk)." — [1j6cymq](https://www.reddit.com/r/StableDiffusion/comments/1j6cymq/)
- 1jztbh7, r/StableDiffusion, 2025-04-15, 287 pts; title: "WanGP 4 aka 'Revenge of the GPU Poor' : 20s motion controlled
  video generated with a RTX 2080Ti, max 4GB VRAM needed !" Top reply: "Impressive! Not good enough for prime time, but
  impressive nevertheless!" (c+48). — [1jztbh7](https://www.reddit.com/r/StableDiffusion/comments/1jztbh7/)
- 1o2wklr, r/StableDiffusion, 2025-10-10, 764 pts; "We can now run wan or any heavy models even on a 6GB NVIDIA laptop GPU |
  Thanks to upcoming GDS integration in comfy". Replies: "Be aware it's linux only atm" (c+35); a long reply explains GDS
  speeds loading from SSD but "does not prevent GPU memory overflow by itself". —
  [1o2wklr](https://www.reddit.com/r/StableDiffusion/comments/1o2wklr/)
- 1vg7qhj, r/StableDiffusion, 2026-08-05: a Wan 2.2 anime short drew "Get with the times, grandpa!" (c+35) - by Aug 2026
  the sub treats Wan as last year's model, with MiniMax H3 the new favourite. —
  [1vg7qhj](https://www.reddit.com/r/StableDiffusion/comments/1vg7qhj/)

**MiniMax H3, LTX-2, Kandinsky 5 Lite (2026 models) on 4-6 GB**
- 1w9zhbx, r/StableDiffusion, 2026-09-07, 6 pts; "RTX 3050 Laptop, WSL2, ComfyUI", "System RAM 32GB" (same GPU as the
  owner). Fast settings (turbo 4/8-step LoRA, 512x288): "hands still render as indistinct blurry blobs during actual gesture
  motion". Good settings (768x448, no distillation, 20 steps): "that config took 6 hours 22 minutes for a single 15 second,
  362 frame clip on this card. That's not a workflow, that's a single overnight bet." Replies: "rent a 5090 on runpod"
  (c+11); "There's no magic. Your card is woefully inadequate." (c+5); one suggests LTX-2.3 "is the better option for you". —
  [1w9zhbx](https://www.reddit.com/r/StableDiffusion/comments/1w9zhbx/)
- 1vlqwme, r/StableDiffusion, 2026-08-11, 0 pts, 72 comments; "RTX 4050 Laptop (6GB)", MiniMax H3 quantized + turbo LoRA:
  "managed to get 3 successful generations, albeit slowly (~300s+ for a 7s video)", then the GPU dropped out
  ("VIDEO_DXGKRNL_FATAL_ERROR") and the OP believes it is "fried". Commenters blame laptop cooling, not the software:
  "Buy a laptop fan cooler" (c+10); one capped power at 85% "this made it around 68-72 C ... instead of 75-81 C" (c+6); "I
  would never use a mobile GPU for inference. The cooling sucks" (c+6). Single anecdote; cause not established. —
  [1vlqwme](https://www.reddit.com/r/StableDiffusion/comments/1vlqwme/)
- 1rf8h97, r/comfyui, 2026-02-26, 10 pts; "Running LTX-2 on 4GB VRAM Using GGUF (Part 2)" (YouTube tutorial). Reply (c+4):
  "With enough of RAM it can be done, but it would be slow and bad quality. The latter in case of low quants. If you're able
  to use cpu (RAM) as the donor and you have enough of it (64GBs+) and run fp8 or even fp16, the quality will be no
  different then RTX 6000 Pro, it will just take a long time". Another user hit an error in the shared workflow. —
  [1rf8h97](https://www.reddit.com/r/comfyui/comments/1rf8h97/)
- 1v1lawz, r/StableDiffusion, 2026-07-20, ~125 pts; title: "Kandinsky5 Lite I2V – Low VRAM Workflow (4GB GPUs) – 5s video at
  675×900, 8–12 steps". No timing in the readable text. Replies: "gross slow motion" (c+4); one user's run "gets stuck
  forever at 80% while decoding the VAE"; another says the bundled LoRA "isn't doing anything". —
  [1v1lawz](https://www.reddit.com/r/StableDiffusion/comments/1v1lawz/)

**FramePack and AnimateDiff**
- FramePack on a 3050 Ti 4 GB laptop worked only after a RAM upgrade to 64 GB: "now i can also use FramePack, not so fast,
  but it works" (1lymf8b, 2025-07-13). A title from 1k2s4jr (2025-04-19): "Framepack: 16 RAM and 3090 rtx => 16 minutes to
  generate a 5 sec video". — [1lymf8b](https://www.reddit.com/r/StableDiffusion/comments/1lymf8b/) ;
  [1k2s4jr](https://www.reddit.com/r/StableDiffusion/comments/1k2s4jr/)
- 1i0pa5p, r/comfyui, 2025-01-13; 4 GB VRAM: AnimateDiff "can't get one batch to process due to memory allocation issues";
  the user solved the actual task in DaVinci Resolve instead. Older: 178lrr2 (2023-10-15) title "AnimateDiff runs very
  slowly (180s/it) with a GTX 1060 6Gb". — [1i0pa5p](https://www.reddit.com/r/comfyui/comments/1i0pa5p/) ;
  [178lrr2](https://www.reddit.com/r/animatediff/comments/178lrr2/)

**Subtle "living still" motion instead of AI video**
- 1j85gnw, r/StableDiffusion, 2025-03-10, 3 pts; RTX 3050 4 GB user wants "hair slightly moving or dust particles". Replies:
  "just download DaVinci Resolve, if it's mostly about particles" (c+2); "You can add dust particles and similar effects most
  easily in AE or DaVinci ... ComfyUI-Depthflow-Nodes ... animate a still image with slight movements and a small parallax
  effect" (c+1). The OP on hosted AI video: Kling "just makes a 5 second animation as the character moves and does whatever.
  it doesn't feel like live2d or animated wallpaper where the main focus of the image is in its place but the smaller
  elements float or moving slightly." — [1j85gnw](https://www.reddit.com/r/StableDiffusion/comments/1j85gnw/)

**A complete local "episode" pipeline and its reception (not 4 GB)**
- 1xfq81y, r/StableDiffusion, 2026-10-26, 0 pts, 40 comments; 10-minute episodes with Qwen-Image stills -> Wan 2.x I2V with
  4-step Lightning LoRA -> InfiniteTalk lip-sync -> TTS, rendered on an AMD MI300X datacenter GPU: "renders a 7 s shot in
  about 4 minutes on my GPU". On lip-sync: InfiniteTalk "animates every visible face, so listeners and even babies 'talk'
  along. I ended up giving the speaker their own close-up shot." On MiniMax H3: it "kept inventing extra people and objects
  that weren't in the source still". Reception in section 5. — [1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)

### Inferences
- For a 60 s Short (12 x 5 s clips) the 3050-class numbers imply roughly 6 hours of Wan 2.2 14B generation per Short, or
  overnight-per-clip for MiniMax H3 at good settings, before re-rolls (the 1uey0kf author made 3 tries per shot). A 5-7 min
  long video fully in AI video on this laptop is not realistic by these reports; using AI video only for 2-3 key shots per
  video and stills + parallax/particles for the rest matches what commenters advise.
- Video generation on the laptop also raises the hardware risk reported for mobile GPUs under hours of full load (one
  anecdote; power-limiting and a cooler were the suggested mitigations).
- None of these video models were reported running on a CPU-only server; the cloud server's role stays compositing.

### Gaps
- No first-hand Wan 2.1 1.3B timing on a 4 GB card was found (only a mention by a user who runs "Wan 1.3B T2V FP16").
- No LTX-Video (2024-25 versions) or AnimateDiff-Lightning/LCM timings on 4 GB were found.
- The OP text of 1pf7986 (exact 4 GB per-clip time and settings) could not be retrieved through the API.

## 3. Character consistency across many shots

### Takeaway
The low-VRAM creators kept characters consistent mainly with identical, word-for-word character and location
descriptions in every prompt, and both say it was imperfect. In general (not 4 GB-specific) threads, users agree that
IP-Adapter gives style/"vibe" rather than identity, ControlNet controls pose but not identity, and a LoRA per character
is the dependable route for a recurring cast. One user trained an Illustrious character LoRA on 6 GB in about an hour,
and the likeness went from ~50% to "fine" only with more epochs and LoRA weight 1.2-1.4. Newer reference/edit models
(Flux.2 Klein, Qwen-Image-Edit) are reported to replace LoRAs for many users, but they are large models.

### Cited Findings
- 1p9gjj7 (RTX 3050 4 GB + 64 GB RAM): "Consistency: In each prompt, I used identical descriptions of the location and
  character, word for word." The hardest part was "Keeping character consistency and scene geometry stable". —
  [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)
- 1pf7986 (GTX 1050 Ti 4 GB) OP: "Well, it's not perfectly consistent. I did it just through prompts, always describing the
  woman in detail - in my case, a blonde woman with slightly curly hair wearing a white dress, etc." (c+4). —
  [1pf7986](https://www.reddit.com/r/StableDiffusion/comments/1pf7986/)
- 1uey0kf (4 GB + 16 GB RAM) OP replying to a removed critique: "I would also love to know whenever you find a model to do
  consistent characters too"; a commenter: "Interestingly enough, the flower bouquet stayed pretty much the same." —
  [1uey0kf](https://www.reddit.com/r/StableDiffusion/comments/1uey0kf/)
- 1l04nqv, r/StableDiffusion, 2025-05-31, 4 pts; OneTrainer, 6 GB NVIDIA GPU, Illustrious-XL-v0.1 base, 24 images. Settings
  that fit: "1 hour of training, 20 epochs, LORA RANK (DIM) of 8, Alpha 1, 460x460" with EMA off and gradient checkpointing
  CPU-offloaded (advice from u/tom83_be). Results: "The character I trained got like 50% resemblance in lora weight 1.0";
  "My results with 40 epochs, same settings was better! I could say, 70% resemblance. ... But I need to use lora weight
  above 1.0 (like 1.2)"; "I tested with 60 epochs and IT WORKED! Its not 100% yet ... I still need to put LORA weight 1.2 up
  to 1.4"; "I tried to put RANK 16 but it gave me OOM error in 3%" while rank 12 worked; using the CPU's integrated graphics
  for the display cut the GPU's idle use "from 400mb to 150mb of VRAM"; "it's even better for clothing ... itens, and even
  concepts". — [1l04nqv](https://www.reddit.com/r/StableDiffusion/comments/1l04nqv/)
- 1gi2w2e, r/StableDiffusion, 2024-11-02 (older), 344 pts; OneTrainer author on RAM offloading: "VRAM usage is not reduced
  much when training unet models like SD1.5 or SDXL" (offloading helps Flux/SD3.5 more). —
  [1gi2w2e](https://www.reddit.com/r/StableDiffusion/comments/1gi2w2e/)
- 1i9jecq, r/StableDiffusion, 2025-01-25; "Can I train a SDXL LORA on a 3050 ti with 4GB VRAM?" - no success report; the
  only answer: "I gave in an got myself a game rig." — [1i9jecq](https://www.reddit.com/r/StableDiffusion/comments/1i9jecq/)
- 1wxey7r, r/StableDiffusion, 2026-10-04, ~205 pts; a free trainer advertised as covering "SDXL/Pony/Illustrious ... Anima
  ... from 4-8 GB VRAM"; the comments read contain a first-hand success on an RTX 3060, none on 4 GB. —
  [1wxey7r](https://www.reddit.com/r/StableDiffusion/comments/1wxey7r/)
- 1v62676, r/comfyui, 2026-07-25, 7 pts; Illustrious visual novel: "ControlNet works great, poses and framing come out
  exactly how I want, but I can't get the character's actual styling to stick using IPAdapter." Reply (u/AillexJ): "For a VN,
  LoRA per character is the better move and honestly it isn't close ... IPAdapter is doing style and vibe transfer, it was
  never really built to lock a specific character"; "check your ControlNet weight isn't cranked so high that it's fighting
  the LoRA"; multi-character scenes: "characters bleed into each other when they're close together", so lower each LoRA's
  weight and run "a per character detailer or inpaint pass masked to each face"; "lock a fixed token block per character
  (hair colour, eye colour, one distinctive clothing item, identical phrasing every time)". The VNCCS node pack is named for
  sprite sheets. — [1v62676](https://www.reddit.com/r/comfyui/comments/1v62676/)
- 1ryhz6s, r/comfyui, 2026-03-20, 43 pts; OP tried "IPAdapter → too much drift", "ControlNet → not for identity", "Pulid /
  FaceID → face only". Replies: "Flux 2 Klein 9B, or flux 2 Dev 32B. Qwen edit." (c+22); several references beat one: "If
  you give it 2 or three reference images, it has too guess much less" (c+2). (These are large models; the GTX 1060 guide in
  section 1 calls Klein 9B on 6 GB "slow or quality loss".) — [1ryhz6s](https://www.reddit.com/r/comfyui/comments/1ryhz6s/)
- 1u7a7tg, r/comfyui, 2026-06-16; manga panels: "I have 1 LoRA per character ... I create each character separately then i
  use an editing model to put them in the same image"; "The hard part is usually separating style consistency from
  character consistency. I would lock the character references first, then keep the panel style almost boring for a few
  tests before adding motion or dramatic angles." — [1u7a7tg](https://www.reddit.com/r/comfyui/comments/1u7a7tg/)
- 1xfq81y, 2026-10-26: style drift despite "the same style line in every prompt, some shots come out flatter and more 2D";
  the fix was "newer edit models (FireRed-Image-Edit 1.1 and Qwen-Image-Edit-2511) with reference images". Commenters' first
  complaint was the 2D/3D drift ("Why is it 3D and 2D like suddenly", c+9). —
  [1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)
- 1xgf9g6, r/StableDiffusion, 2026-10-27 (posted today, 16 pts); for a former animator: "controlnet is probably the thing
  that will feel closest to how you work. you feed in your own storyboard frame or character sheet as the guide"; "For a more
  budget combo maybe try anima with ltx they are faster, but quality is worse." —
  [1xgf9g6](https://www.reddit.com/r/StableDiffusion/comments/1xgf9g6/)
- 1p9gfw4 (r/comfyui) critic (u/chum_is-fum): "learn Blender and krita, in Blender you can animate an openpose rig to match
  the movement of your character and then plug that into wan 2.2 animate. In Kirta you can touch up any frames". —
  [1p9gfw4](https://www.reddit.com/r/comfyui/comments/1p9gfw4/)
- Viewer-side weight of consistency (1v621co, r/aitubers, 2026-07-25, 48 pts): "One weird hand movement? Most viewers won't
  even notice. But if your character looks different every scene ... people immediately disconnect." —
  [1v621co](https://www.reddit.com/r/aitubers/comments/1v621co/)

### Inferences
- With 4 GB, the realistic consistency stack per these reports is: one Illustrious (or SD1.5 anime) base model, a fixed
  token block per character copied word for word, ControlNet for pose, and a small per-character LoRA trained at low rank
  and low resolution (or trained on a rented GPU). Expect to over-weight the LoRA and cherry-pick.
- A puppet/cut-out approach (draw each character once, reuse the same layered art in every shot) sidesteps the
  generation-drift problem entirely; none of the AI threads above achieved full consistency by generation alone.

### Gaps
- No first-hand report of a successful SDXL/Illustrious LoRA trained on exactly 4 GB was found (6 GB is the lowest).
- No first-hand SD1.5 LoRA-on-4 GB timing was found in 2025-2026 threads.
- No report compared IP-Adapter results on SD1.5 vs SDXL at 4 GB.

## 4. Motion-comic, Live2D-style and 2.5D approaches for anime channels

### Takeaway
Commenters describe most long AI anime-story videos as stills with pan/zoom plus a few image-to-video shots, and advise
beginners to do exactly that ("only animate the 2-3 most important moments"). One faceless-channel operator reports that
light, stylised animation drew less "slop" criticism than cinematic AI video "and my retention didn't drop". But a bare
auto-scrolling/voice-over motion comic got a hostile reception, and no thread gave retention numbers for parallax,
Live2D or puppet-style channels. Live2D (free tier) is the community default over Inochi2D, which users describe as
buggy and slow-moving.

### Cited Findings
- 1wqgx16, r/aitubers, 2026-09-26, 17 comments; on the ~1-hour AI anime story videos: "Some channels animate a few seconds
  per shot with image-to-video, most just pan/zoom on stills. TTS does the narration. ... An hour-long video is several
  hundred shots produced in bulk batches" (u/Good-Caterpillar7890, c+3; a commenter's description, not the creators'). —
  [1wqgx16](https://www.reddit.com/r/aitubers/comments/1wqgx16/)
- 1ueqq68, r/aitubers, 2026-06-24, 8 pts; OP has character/scene images and dialogue audio for a 1-minute video; tried
  "Google Flow ... LivePortrait ... Hedra ... SadTalker" and every new clip changed the character, background, lighting.
  Reply (c+3): "you dont need to generate video clips at all. just sequence them with ken burns pan/zoom in ffmpeg and sync
  to your audio. only animate the 2-3 most important moments with image-to-video ... each generation starts fresh with no
  memory of the previous frame". OP's remaining problem: "In each shot there are dialogues so without video I do not know
  how to do the lip sync". — [1ueqq68](https://www.reddit.com/r/aitubers/comments/1ueqq68/)
- 1w0t2tb, r/FacelessVideos, 2026-08-28, 44 pts; operator of "more than 20 channels" (discloses he sells a tool, OpenVidi):
  "Simple visuals beat cinematic ones ... Complex realistic scenes always carry render bugs somewhere ... viewers zoom in on
  exactly those frames and call the whole video AI slop ... Light animation and stylized or cartoon elements that don't
  attempt realism get less hate and cost less, and my retention didn't drop. One of the beginners I onboarded did his history
  video in an anime style and it came out better than my early realism attempts." A commenter agrees: "stylised stuff gets
  way more slack. viewers already accept its not real so they stop hunting for the tell." —
  [1w0t2tb](https://www.reddit.com/r/FacelessVideos/comments/1w0t2tb/)
- 1t4yd80, r/manhwa, 2026-05-06, 0 pts; a solo "Motion Comics" channel asks for feedback. Replies: "Opened the regressed
  mercenary's machinations vid and it made me wanna barf. No wonder the channel isn't getting any traffic" (c+2); "I skimmed
  the text and thought he was making static panels animated. Not just auto-scrolling on webcomics and using AI voice
  generators to read out webcomics." — [1t4yd80](https://www.reddit.com/r/manhwa/comments/1t4yd80/)
- ultqvu, r/AfterEffects, 2022-05-09 (older), 701 pts; a pro making anime-style manga trailers "100% composited with AE":
  "I cut each part on photoshop and then I just assemble everything back on AE. I essentially use rotation and position key
  frames (old school)"; time: "I worked a full month on this project." —
  [ultqvu](https://www.reddit.com/r/AfterEffects/comments/ultqvu/)
- 1j85gnw (RTX 3050 4 GB, 2025-03-10): parallax via "ComfyUI-Depthflow-Nodes"; particles in DaVinci/AE; the OP wanted the
  "live2d or animated wallpaper" feel that hosted AI video did not give. —
  [1j85gnw](https://www.reddit.com/r/StableDiffusion/comments/1j85gnw/)
- 1olqpr5, r/vtubertech, 2025-11-01, 6 pts; Live2D free vs Inochi2D: "Live2D has a bigger user base and more support, the
  free version has enough unlocked features to start out" (c+3); "the project hasn't been developed consistently in the past
  2+ years ... it still has bugs that will corrupt your model file sometimes. I recommend staying away from it" (c+2, a
  party to a public dispute with the Inochi2D author, so not neutral); an Inochi2D user disagrees: "I use Inochi because
  Live2D burns my computer too much, and leaks my RAM ... it's an open source software". A Dec 2025 tool "INPFix, a tool for
  corrupted Inochi2D models" (1q0h9c4) supports the corruption report. —
  [1olqpr5](https://www.reddit.com/r/vtubertech/comments/1olqpr5/) ; [1q0h9c4](https://www.reddit.com/r/Inochi2D/comments/1q0h9c4/)
- 1wnirfr, r/aitubers, 2026-09-22; a self-built Python engine ("Characters that act out every line of narration, AI-painted
  backgrounds, TTS voice ... word-by-word captions"), 14 videos, 26 subs. Criticism (u/FlatBassets): "the videos and
  thumbnails look obviously AI generated ... lot of times your video simply doesn't sync with the narration, you mention
  boat? No Boats." Advice (u/Dependent-Bunch7505): "the title card at 0:20 is the first thing I'd remove ... TTS isn't
  automatically fatal, but flat pacing is." — [1wnirfr](https://www.reddit.com/r/aitubers/comments/1wnirfr/)
- 1xfq81y: for dialogue the creator gave "the speaker their own close-up shot" because the lip-sync model animated every
  face in frame. — [1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)

### Inferences
- The planned stills + parallax + lip flap + effects approach matches what the community says most AI anime-story
  channels do; the differentiator in the comments is that the motion must look intentional (the hostile replies target
  "auto-scrolling" panels with an AI voice, and visuals that do not match the narration).
- Lip-sync on dialogue is the step people get stuck on; the simplest community workaround is a close-up of the speaker,
  which suits a puppet rig with mouth shapes.

### Gaps
- No Reddit thread with retention or view data for parallax/2.5D, Live2D, Inochi2D, EasyVtuber or Talking-Head-Anime
  storytelling channels was found; searches for EasyVtuber/THA returned nothing relevant.
- No first-hand reports of Live2D or Inochi2D being run headless on a CPU server for batch rendering.

## 5. YouTube experiences of AI anime / AI story channels (2025-2026)

### Takeaway
AI story channels do get and keep monetization (one AI sci-fi series was reinstated after reapplying; commenters say
original, crafted stories pass), but 2026 threads describe waves of "inauthentic content" demonetizations that also hit
non-AI creators, with users pointing at repetitive titles, thumbnails and formats as triggers and recommending multiple
characters/voices and varied packaging. Viewer comments are often hostile ("AI slop", "click away instantly"); the
operators who report success say story, voice and consistency matter more than animation quality, and that stylised
visuals draw less hate than realistic ones.

### Cited Findings
**Monetization and "inauthentic content"**
- 1se9c36, r/aitubers, 2026-04-06, 118 pts, 159 comments; AI music-video channel (own lyrics, Suno, ComfyUI, Veo 3,
  Premiere), monetized ~8 months, then demonetized for "Inauthentic Content" without changes. Replies: "It's not just AI,
  non-AI creators are being swept up in this too ... thumbnails and titles that adhere to a very consistent formula every
  time. For example, if you have 20 videos and they all have 'parody music video' in the title, or if the thumbnails all
  mostly look the same except with a character swapped out." (c+41); "have multiple speaking characters with different
  voice-overs, doesn't matter if you use AI tools to make them. Make different types of content for the channel, and make
  sure titles, thumbnails and other stuff are not repetitive." (c+6); a niche channel "was terminated. YouTube could not
  provide me with any details" (c+5). — [1se9c36](https://www.reddit.com/r/aitubers/comments/1se9c36/)
- 1ulq33c, r/aitubers, 2026-07-02, 8 pts; AI sci-fi comedy/drama series with recurring characters (Midjourney, Nano
  Banana, Veo, some Sora), demonetized, appeal failed; deleted "two videos that weren't connected to the main storyline" and
  reapplied. Update: "After reviewing my channel for 2 days, I've been reintegrated ... in the Youtube Partnership Program."
  A commenter: "You also aren't pumping out multiple videos per day, which I know is a red flag." —
  [1ulq33c](https://www.reddit.com/r/aitubers/comments/1ulq33c/)
- 1wqgx16, r/aitubers, 2026-09-26; commenters (not official) on AI anime-story channels: "An original story with AI visuals
  and AI voice can pass review if it reads as a crafted work ... the most formulaic ones are exactly what the
  inauthentic-content enforcement sweeps for, so the genre lives in a gray zone - the channels with genuinely original
  writing survive, the template farms get demonetized in waves" and "the writing is the moat". —
  [1wqgx16](https://www.reddit.com/r/aitubers/comments/1wqgx16/)
- 1si1xbi, r/PartneredYoutube, 2026-04-10, 49 pts, 127 comments; poster's view: "it doesn't have to be all of your content.
  It just has to be a portion of your channel that is contributing significant traffic ... he'd been making AI shorts that
  had been going viral, and that's why he got dinged"; he judges the appeal form "won't work" and suggests TeamYouTube on X
  or partner support. Pushback in replies, including a creator with "300 million short-form views" who says genuine
  creators were hit and "YouTube does not retroactively fix earnings." —
  [1si1xbi](https://www.reddit.com/r/PartneredYoutube/comments/1si1xbi/)
- 1sn0ihk, r/PartneredYoutube, 2026-04-16, 50 pts; "once again, it's not AI. High-effort creators are getting slaughtered".
  Counterpoints: "almost every time a post like this on the sub it's 'transformative original content' and when you look
  inside its Minecraft parkour reddit stories or stolen content" (c+30); "Inauthentic used to be called Repetitious Content,
  so most channels getting demonetized for it are the ones posting 500 videos of basically the same content farm slop with
  minor tweaks and nearly identical titles" (c+10). — [1sn0ihk](https://www.reddit.com/r/PartneredYoutube/comments/1sn0ihk/)
- 1sy0hon, r/PartneredYoutube, 2026-04-28; a gaming creator flagged twice in a month, "appealed and was reinstated over the
  weekend", the second time restored within hours; others in the thread were still waiting or denied. —
  [1sy0hon](https://www.reddit.com/r/PartneredYoutube/comments/1sy0hon/)
- 1sti2eu, r/PartneredYoutube, 2026-04-23, title only: "AI slop second channel got removed from YPP for inauthentic content.
  What are the chances my main, non-AI channel is at-risk for a related channel claim?" —
  [1sti2eu](https://www.reddit.com/r/PartneredYoutube/comments/1sti2eu/)

**What viewers and other creators say**
- 1vxw9zb, r/NewTubers, 2026-08-25; asked about original stories with AI visuals and AI narration: "If someone sees something
  that looks and sounds like AI, why would they believe that the writing isn't?" (c+9); "When I see a video is made using ai
  I click away instantly and hit 'don't recommend'." (c+5). — [1vxw9zb](https://www.reddit.com/r/NewTubers/comments/1vxw9zb/)
- 1p9gfw4, r/comfyui (RTX 3050 4 GB anime short): "this looks pretty rough ... not sure if the wabble was intended but it is
  very distracting and the voice acting is too stilted. Your work is also riddled with hallmark AI artifacts galore" and "For
  voice over... Just speak into a microphone, maybe use a voice changer, it'll be better than the tts." Another commenter
  calls the same work "Brilliant". — [1p9gfw4](https://www.reddit.com/r/comfyui/comments/1p9gfw4/)
- 1xfq81y (2026-10-26): "AI slop literally. Who would even watch this? Why 2D and then 3D?" (c+4); "The voice-acting is
  atrocious" (c+2); "Most of these shots should've been dropped. Does anyone even edit?" (c+3). —
  [1xfq81y](https://www.reddit.com/r/StableDiffusion/comments/1xfq81y/)
- 1x62nx4, r/animation, 2026-10-14, 516 pts; a creator who "gave up on making AI videos to learn animation" is celebrated:
  "W Tier redemption" (c+69). Shows r/animation's stance on AI video. —
  [1x62nx4](https://www.reddit.com/r/animation/comments/1x62nx4/)

**What successful operators say made the difference**
- 1v621co, r/aitubers, 2026-07-25, 48 pts; claims "over 30M views across my AI storytelling channel" (monetization not
  answered in thread): "Don't start with Text to Video ... make the image first"; "Don't write stories that depend on acting.
  ... AI still sucks at acting ... Make stories that rely more on visual storytelling than acting"; "Character consistency.
  Location consistency. Visual style consistency. Those three things make AI stories believable."; "viewers forgive
  imperfect animation much more easily than a boring story." — [1v621co](https://www.reddit.com/r/aitubers/comments/1v621co/)
- 1w0t2tb, r/FacelessVideos, 2026-08-28 (tool seller): "Voice matters more than visuals ... a voice that sounds even slightly
  robotic kills retention in the first minute"; commenter: "i had decent visuals with a flat tts read and retention died
  around 20s. swapped to a narrator that actually breathes and paces and the same script held." Also: add "your own take"
  to the script so it "carries a point of view". — [1w0t2tb](https://www.reddit.com/r/FacelessVideos/comments/1w0t2tb/)

**Voice/TTS speed on modest hardware (side finding for the CPU server)**
- 1p9gjj7 (RTX 3050 4 GB laptop): "I can run IndexTTS2 only on CPU, and it takes 10–30 minutes, while ChatterBox on CPU takes
  just 2–3 minutes" (audio length not stated); voices were "ChatterBox + RVC". —
  [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)
- 1n4hkar, r/LocalLLaMA, 2025-08-31, 63 pts; Ryzen 7 laptop, 16 GB RAM, RTX 3060 laptop: "Kokoro - 0.4-0.5 x realtime .Fast
  and decent quality"; "Xtts v2 - 0.8-1x realtime"; "Chatterbox - if you have lower end gpu and cpu like me don't try ! It's
  slow (1.5-2x realtime but high quality , expressive"; "Zonos : 2-3x realtime"; "F5tts : around 1x realtime ... somewhere in
  the middle, it hallucinates". Reply (c+21): "Go straight to vibevoice ... If you need realtime, Kokoro." (I read "x
  realtime" as generation time divided by audio length.) — [1n4hkar](https://www.reddit.com/r/LocalLLaMA/comments/1n4hkar/)

### Inferences
- The owner's two-story, recurring-character format with distinct character voices and an owner-written script is the
  pattern commenters say survives review; the risk factors they name are high upload volume, near-identical titles and
  thumbnails across videos, and one voice/format repeated everywhere. These match the channel's existing CLAUDE.md rules.
- Voice quality is repeatedly named as the first retention killer, ahead of visuals.
- Reddit opinion on demonetization causes is speculative; nobody had official confirmation of what triggered a flag.

### Gaps
- No first-hand report found from an AI *anime thriller* channel specifically with monetization status and numbers.
- No thread gave Shorts retention (stayed-to-watch %) for AI anime content.

## 6. Anime look tips from animators and compositors

### Takeaway
Animators and AE users describe the anime "look" as mostly compositing and timing: a subtle gradient and noise/grain
layer, a blurred duplicate on Screen at low opacity for diffusion/glow, line work isolated by keying the black lines and
roughened or thickened, light that matches the background, and timing on twos via a 12 fps step (Posterize Time) while
exporting at 24 fps. In the most-upvoted critique thread, motion problems (uniform hair, mismatched wind, no ease in/out,
too fast) mattered more than the drawing.

### Cited Findings
- 1j8f6av, r/AfterEffects, 2025-03-11, 0 pts; reverse-engineering an anime compositing breakdown (u/craftuser, c+4):
  "Gradient and Noise is right there in the name, its just very subtle. Main Filter and Diffusion filter seem to be the same
  thing twice; duplicating the image, blurring it and setting it to low opacity, probably with Mode set to Screen. The line
  filter might be the most 'complicated' part of it. Color keep (reverse color key) the black outline then add a Roughen
  Edge filter. You may want to grow the line a bit before you roughen edge so you get thicker lines, use matte choker or
  Minimax". — [1j8f6av](https://www.reddit.com/r/AfterEffects/comments/1j8f6av/)
- 1p292vc, r/AfterEffects, 2025-11-20, 25 comments; varying line thickness: "You can blur it a few pixels, and add levels to
  'choke' the blur out ... the white and black points determine the thickness of the lines when you use blur and levels"
  (u/mcarterphoto, c+3); "Find Edges wouldn't work well, you'd have all the shadow edges as black lines as well"; others:
  simple choker + turbulent displace; "its literally just a default after effects tool called 'roughen edges'". —
  [1p292vc](https://www.reddit.com/r/AfterEffects/comments/1p292vc/)
- 1lhfy90, r/animation, 2025-06-22, 444 pts, 140 comments; "What is missing from this to make it look like a scene from a
  professional anime?" Top replies: "More generally consistent frame rate across elements. If the wind is blowing his hair
  ... Gusty wind should have a similar effect on his clothes and the snow as it has on his hair" (c+455); "The timing on the
  three main clumps of his bangs all move in unison. It gives it a stiff robotic feel. Offset each clump by a few frames"
  (c+63); "if the cut is going to be short then animate all your keys don't go for a loop, especially on a close up";
  "unless the depth of field has a purpose, I'd take it out and let the BG artist's effort be seen"; a top-down light falloff
  that also hits the background "makes it look like a cardboard behind the character"; "when the environment is dark, so
  should be the shadows" (c+43); "Try adding some ease ins and outs" (c+3); "it's a little fast" (c+159). —
  [1lhfy90](https://www.reddit.com/r/animation/comments/1lhfy90/)
- 1ac94e1, r/AfterEffects, 2024-01-27 (older), 24 pts; on twos: "if a project is rendered at 12fps, the motion blur ... is only
  using 12 frames worth of data ... It's rarely a good idea to render out a video at 12fps - many places you would upload a
  video reformat it to 23.97 or 24fps, which can lead to odd playback glitches" (c+73); "I animate 24fps on twos with some
  ones mixed in. I want to retain the look of twos with all digital effects, camera moves, etc. Posterizing time to 12fps on
  those layers achieves this" (c+2); a counterpoint: posterize "slow down the render time dramatically" versus setting the
  comp to the target rate (c+5). — [1ac94e1](https://www.reddit.com/r/AfterEffects/comments/1ac94e1/)
- ultqvu, r/AfterEffects, 2022-05-09 (older), 701 pts; manga-trailer compositing praised for "variety of textures ...
  especially the half tones"; parts cut in Photoshop and moved with rotation/position keys. —
  [ultqvu](https://www.reddit.com/r/AfterEffects/comments/ultqvu/)
- 1r3s6k9, r/animation, 2026-02-13, 10 pts, title: "Recreating 90s 'Bipack Glow/Underlighting' digitally: A look into the
  research and compositing workflow (via Animation Obsessive)" - the creator offers production detail in comments. —
  [1r3s6k9](https://www.reddit.com/r/animation/comments/1r3s6k9/)
- AI-specific look issue: the 4 GB anime-short creator's low-denoise Illustrious restyle pass on video frames made "the
  image flickers slightly" (1p9gjj7), and he used RIFE interpolation. —
  [1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/)

### Inferences
- All of the compositing steps named (gradient, grain, Screen-blended blur glow, keyed and roughened line art, posterized
  time) are per-frame image operations that a CPU compositor can do; they don't need a GPU.
- The r/animation critique implies that for limited/puppet animation the cheapest wins are timing ones: offset secondary
  motion (hair clumps, cloth), one consistent wind direction across hair, cloth and particles, ease in/out, and keeping
  rim/key light consistent with the background.
- Running AI frame-by-frame restyling or RIFE interpolation works against the "on twos" look; the AE threads keep a stepped
  12 fps feel inside a 24 fps export instead.

### Gaps
- No r/anime or r/Animators thread was found that discusses 24 fps on twos/threes for AI or puppet animation specifically;
  the "on twos" evidence comes from r/AfterEffects.
- No community thread was found that criticises RIFE-style interpolation on anime footage with specifics.
