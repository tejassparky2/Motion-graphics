# Voice and sound for horror Shorts: open-source CPU TTS, horror SFX libraries, dread techniques, loudness (notes, 25 Oct 2026)

Scope: what can voice an emotional horror narrator plus several characters offline on a 4-core CPU (this machine: `nproc` = 4), with a licence that allows a monetized YouTube channel and without cloning a real person; free horror sound libraries and their exact licences; evidence-based dread techniques that survive phone speakers; loudness targets.

Local context used below (not web sources): `tools/clone_tts.py` loads `ChatterboxTurboTTS.from_pretrained(device="cpu")` in plain PyTorch, with `EXAGGERATION, CFG = 0.6, 0.6` passed to the original-Chatterbox path; `out/turbo_tags_research.md` (14-15 Oct 2026 tests) found Turbo's tokenizer has 19 tags, sound tags work only on some takes, and mood tags ([fear], [whispering], [dramatic]...) are "undocumented and weak" (no real whisper). CLAUDE.md: never clone a real person, never strip other parties' provenance watermarks.

RTF warning: sources use "RTF" both ways. Some mean wall-time divided by audio length (lower = faster, below 1 = faster than real time); others mean "x real time" (higher = faster). Each figure below says which one.

---

## 1. Which open-source TTS models can voice an emotional horror narrator and several characters on a 4-core CPU? (licence, size, speed, emotion/pace control, watermark, quality)

### Takeaway
As of October 2026, no open model with a licence that allows a monetized channel has all four things at once: strong emotion control, stable voices for several characters, a fast 4-core CPU path and top-tier quality. The Chatterbox family (MIT) is still the best balance. Turbo (350M) gives paralinguistic tags and has an official ONNX export and a ggml/C++ port. Nano (110M) is built for CPU (~3x real time on 8 cores). The models with the strongest emotion controls either need a GPU (IndexTTS2/2.5, Maya1, Orpheus, Zonos, Dia) or carry a non-commercial or contact-us licence (IndexTTS, Fish S2, Higgs v3, Breeze TTS 2, F5, XTTS-v2, OpenAudio S1-mini). The fast CPU models (Pocket TTS, Kokoro, Soprano, Supertonic 3) have little or no emotion control. The one CPU model with a built-in "fearful" emotion, NeuTTS-2E, has an unclear licence and is an early alpha.

### Cited Findings

**Leaderboard signal (Artificial Analysis Speech Arena, snapshot fetched 25 Oct 2026)**
- The top open-weights entries are Fish Audio Drama 3 Preview (Elo 1248, #9), Breeze TTS 2 (1230, #11), Ming-3.0-tts (1191, #19), Fish Audio S2 Pro (1110, #38), Step Audio EditX (1100, #41) and Voxtral TTS (1091, #46). Further down: Kokoro 82M v1.0 1066 (#57), Maya1 1048 (#68), Higgs Audio V3 1045 (#69), OpenAudio S1 Mini 1045 (#70), Chatterbox 1025 (#78), Zonos-v0.1 1000 (#81), VibeVoice 1.5B 956, XTTS v2 915, StyleTTS 2 890. Proprietary Eleven v4 Turbo leads at 1336. Chatterbox Turbo, Orpheus, Dia, CSM, F5, IndexTTS and Kyutai are not listed. — [Artificial Analysis TTS leaderboard](https://artificialanalysis.ai/text-to-speech/leaderboard)
- Kokoro (82M) ranks above the original Chatterbox (1066 vs 1025) on that arena. — [Artificial Analysis](https://artificialanalysis.ai/text-to-speech/leaderboard)
- The TTS Arena V2 Space (TTS-AGI) did not render its leaderboard when fetched. — [TTS Arena V2](https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2)
- EmergentTTS-Eval (2025, model-as-judge on prosody and expressiveness) reportedly found Orpheus-TTS best among the open-source models it tested, with Qwen 2.5 Omni close behind. This comes from a search summary; the paper's table was not read directly. — [arXiv 2505.23009](https://arxiv.org/pdf/2505.23009)

**Chatterbox family (Resemble AI): MIT**
- Licence MIT. Sizes: Chatterbox 500M (English); Multilingual V3 500M (23+ languages); Turbo 350M (English); Nano 110M (English); single-language packs 500M each. — [GitHub resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)
- Turbo distils the speech-token-to-mel decoder from 10 steps to 1, "less compute and VRAM". The model card documents only `[cough]`, `[laugh]`, `[chuckle]` "and more". — [HF ResembleAI/chatterbox-turbo](https://huggingface.co/ResembleAI/chatterbox-turbo)
- Exaggeration and cfg_weight are documented for the original Chatterbox: defaults 0.5/0.5; for dramatic speech try cfg_weight ~0.3 and exaggeration ~0.7 or higher. "Higher exaggeration tends to speed speech up"; lowering cfg_weight slows it down. The Turbo example calls `generate()` with only the text and an optional reference clip, and the card does not say Turbo honours these knobs. — [GitHub](https://github.com/resemble-ai/chatterbox); [HF Turbo card](https://huggingface.co/ResembleAI/chatterbox-turbo)
- Nano (110M) is "designed for on-device and CPU inference", reportedly 3x real time on 8 CPU cores, and supports paralinguistic tags. — [GitHub](https://github.com/resemble-ai/chatterbox)
- Watermark: every file from the Python package carries Resemble's PerTh watermark (imperceptible, survives MP3), which can be checked with `perth.PerthImplicitWatermarker().get_watermark()`. — [HF Turbo card](https://huggingface.co/ResembleAI/chatterbox-turbo)
- Third-party opinion: a roundup calls Chatterbox "the most interesting release" and cites a vendor-run study in which 65.3% preferred it over ElevenLabs (vendor study, not independent). — [LocalAIMaster](https://localaimaster.com/blog/best-local-tts-models)
- Local test: Turbo's 19 tokenizer tags split into sound tags ([laugh] [chuckle] [sigh] [gasp] [sniff] [groan] [cough] [clear throat] [shush]) and mood tags ([angry] [fear] [surprised] [whispering] [dramatic] [narration] [crying] [happy] [sarcastic] [advertisement]). Sound tags fired on only some takes. Mood tags were weak: [whispering] did not make a real whisper. With Kokoro-reference character voices, "[chuckle]" was sometimes spoken as a word. — local file `out/turbo_tags_research.md`

**Kokoro-82M (hexgrad): Apache 2.0**
- 82M parameters, StyleTTS2-based decoder only. Apache-licensed weights trained on permissive or non-copyrighted audio. v1.0 (27 Jan 2025) has 54 voices in 8 languages. — [HF hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- It has a `speed` argument (`pipeline(text, voice='af_heart', speed=1, ...)`). The README documents no emotion control. — [GitHub hexgrad/kokoro](https://github.com/hexgrad/kokoro)
- Reported speed: about 5x real time on CPU (hardware not stated) vs 210x on an RTX 4090. — [ocdevel blog](https://dev.ocdevel.com/blog/20250720-tts). Also 13.8x real time on an M4 GPU. — [Yaps, 10 Oct 2026](https://www.yaps.ai/blog/best-local-tts-models)

**Kyutai Pocket TTS: code MIT; weights reported CC BY 4.0**
- About 100M parameters (also 18.2M / 6.9M / 1.9M English variants). About 6x real time on a MacBook Air M4 CPU using only 2 cores, ~200 ms to first chunk. On a cloud x86 VM with 4 vCPUs, the CPU figure is "about 2.3–2.5" (x real time; 6.28 on a T4 GPU). Small English models reach up to 25x real time on one thread (hardware not stated). — [GitHub kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts)
- No emotion or pace control: adding silence for pauses is unsupported. Prohibited uses include "voice impersonation or cloning without explicit and lawful consent". — [GitHub](https://github.com/kyutai-labs/pocket-tts); weights licence given as CC BY 4.0 (attribution) in [Yaps](https://www.yaps.ai/blog/best-local-tts-models)

**Kyutai TTS 1.6B (en/fr): weights CC-BY 4.0**
- Actually 1.8B parameters (1B backbone + 600M depth transformer). Voice cloning is deliberately limited to pre-computed voice embeddings from the tts-voices repo. No CFG control (CFG-distilled). Kyutai deliberately adds **no watermark**. Throughput is "75x generated audio per compute unit of time". The only inference hardware mentioned is CUDA (plus MLX on Apple). — [HF kyutai/tts-1.6b-en_fr](https://huggingface.co/kyutai/tts-1.6b-en_fr); [GitHub delayed-streams-modeling](https://github.com/kyutai-labs/delayed-streams-modeling)

**Orpheus TTS (Canopy Labs): Apache 2.0 (Llama 3.2 base)**
- Llama-3B backbone trained on 100k+ hours of English. Tags: `<laugh> <chuckle> <sigh> <cough> <sniffle> <groan> <yawn> <gasp>`. Eight English voices (tara, leah, jess, leo, dan, mia, zac, zoe). Needs `repetition_penalty>=1.1`; raising repetition_penalty and temperature makes speech faster. There is a no-GPU llama.cpp path. — [GitHub canopyai/Orpheus-TTS](https://github.com/canopyai/Orpheus-TTS)
- The card says Apache 2.0, but the model is built on Llama 3.2, so Meta's terms also apply, and access is gated. Needs a GPU in practice. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models)
- Real-time playback needs about 83 tokens/s (Baseten talk, GPU context). GGUF sizes are Q4_K_S 2.40 GB, Q4_K_M 2.49 GB and Q8_0 4.03 GB. No measured CPU RTF was found. — search summary of [AI Engineer talk](https://ai.engineer/talks/optimizing-inference-for-voice-models-in-production) and [Codersera macOS guide](https://codersera.com/blog/install-and-run-orpheus-3b-tts-on-macos-a-complete-guide/amp/) (UNVERIFIED: not opened)
- A roundup calls it "the best permissively-licensed option if you need expressive, emotional speech". — [LocalAIMaster](https://localaimaster.com/blog/best-local-tts-models)

**Dia (Nari Labs): Apache 2.0**
- 1.6B parameters. Dia2 (1B/2B) was released 19 Nov. Two speakers, `[S1]`/`[S2]`. Nonverbal tags: (laughs) (clears throat) (sighs) (gasps) (coughs) (singing) (mumbles) (groans) (sniffs) (screams) (inhales) (exhales) (humming) and others; unlisted tags cause artifacts. The voice changes every run unless you fix the seed or give an audio prompt. RTX 4090: x2.1 real time (bf16, compiled), ~4.4 GB VRAM. "CPU support is to be added soon." Prohibits producing "audio resembling real individuals without permission". — [GitHub nari-labs/dia](https://github.com/nari-labs/dia)

**Sesame CSM-1B: Apache 2.0**
- Llama backbone plus an audio decoder that makes Mimi codes. It is not tuned to any voice: without context it picks a random speaker, and it works best with context. Needs a CUDA GPU. Prohibits impersonation without consent. Released 13 Mar 2025. — [GitHub SesameAILabs/csm](https://github.com/SesameAILabs/csm)

**Zonos v0.1 (Zyphra): Apache 2.0**
- Emotion conditioning for happiness, fear, sadness and anger, plus speaking rate, pitch and pitch variation. Needs 6 GB+ VRAM. It can run on CPU "much slower… likely won't be sufficient for interactive use". About 2x real time on an RTX 4090. — [GitHub Zyphra/Zonos](https://github.com/Zyphra/Zonos)

**IndexTTS2 / IndexTTS-2.5 (bilibili): bilibili Model Use License; commercial use means contacting indexspeech@bilibili.com**
- Emotion is separate from the speaker. Controls: an 8-value emotion vector (happy, angry, sad, afraid, disgusted, melancholic, surprised, calm), an emotion reference clip with `emo_alpha` 0–1, or emotion from a text description. IndexTTS-2.5 (0.8B, released 10 Aug 2026) adds `duration_factor` 0.5–2.0x. Benchmarked on an RTX 4090; no CPU guidance. — [GitHub index-tts/index-tts](https://github.com/index-tts/index-tts)
- IndexTTS-2 runs at 0.1x real time on an M4 (i.e. 10x slower than real time). — [Yaps](https://www.yaps.ai/blog/best-local-tts-models)

**Maya1 (Maya Research): Apache 2.0**
- 3B Llama-style model that predicts SNAC codec tokens at 24 kHz. Inline tags include `<laugh> <sigh> <whisper> <angry> <giggle> <gasp> <cry>`, "more than 20 emotions". Voices are designed from natural-language descriptions (age, gender, accent, tone), so no reference clip is needed. Runs on a single GPU. — [MarkTechPost](https://www.marktechpost.com/2025/11/11/maya1-a-new-open-source-3b-voice-model-for-expressive-text-to-speech-on-a-single-gpu/); [HF maya-research/maya1](https://huggingface.co/maya-research/maya1)

**Qwen3-TTS (Alibaba): Apache 2.0**
- 0.6B and 1.7B. The VoiceDesign model creates a voice from a text description. CustomVoice/VoiceDesign take instructions for tone, speaking rate and emotion. 9 preset speakers. Released 22 Jan 2026. Examples assume CUDA, and no CPU support is stated. — [GitHub QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
- 0.2x real time on an M4 (Yaps). The arena entry "Qwen3 TTS" scores 930 but is not marked open-weights. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models); [Artificial Analysis](https://artificialanalysis.ai/text-to-speech/leaderboard)

**NeuTTS (Neuphonic)**
- NeuTTS Air: Apache 2.0, GGML/GGUF builds for on-device use, PerTh watermark on every output. — [PyPI neutts](https://pypi.org/project/neutts/)
- NeuTTS-2E: ~125M active / ~236M total parameters, English. Emotions angry, disgusted, **fearful**, happy, sad, surprised and neutral, chosen by `emotion="..."`. Four fixed speakers (emily, paul, sophie, steven) and no cloning. Q8/Q4 GGUF. Claims "real-time or better-than-real-time generation on laptop-class CPUs" (no benchmark given). PerTh watermark. "Early alpha". Licence tagged "other" and gated. — [HF neuphonic/neutts-2e](https://huggingface.co/neuphonic/neutts-2e)

**Soprano (ekwek1): Apache 2.0**
- 80M parameters, 32 kHz. Claims up to 20x real time and under 250 ms latency on CPU (hardware not named). English only, no voice cloning, no explicit emotion controls. Mispronounces numbers and rare words. Released 22 Dec 2025, v1.1 on 14 Jan 2026. — [GitHub ekwek1/soprano](https://github.com/ekwek1/soprano)

**Supertonic 3 (Supertone): OpenRAIL-M weights**
- ~99M parameters, CPU via ONNX Runtime, 31 languages, 44.1 kHz. Sources conflict on whether expression tags work in the free local version. — [Better Stack guide](https://betterstack.com/community/guides/ai/supertonic-3/)
- 4.2x real time on an M4 CPU, "10 inline expression tags", preset voices only, repo archived Sept 2026. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models)

**Non-commercial or restricted (not usable for a monetized channel without a separate licence)**
- F5-TTS: code MIT, weights CC-BY-NC-4.0 (trained on Emilia). — [HF SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS)
- XTTS-v2: Coqui Public Model License (non-commercial); Coqui has shut down. — [HF coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2); [Yaps](https://www.yaps.ai/blog/best-local-tts-models); [LocalAIMaster](https://localaimaster.com/blog/best-local-tts-models)
- Higgs Audio v3 (4B): "Research and Non-Commercial License"; production or revenue use needs a separate commercial licence. — [GitHub boson-ai/higgs-audio](https://github.com/boson-ai/higgs-audio)
- Fish Audio: code and weights under the Fish Audio Community License; S2-Pro (4B) weights under the Fish Audio Research License. Drama 3 is 35B total / 3B active. Tags: S2-Pro `[pause] [excited] [whisper]`; Drama 3 `[whisper] [angry] [laughing]`. S2-Pro RTF 0.195 on one H200 (wall/audio). — [GitHub fishaudio/fish-speech](https://github.com/fishaudio/fish-speech). S2 Pro is described as research-only, with a separate licence for commercial use. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models). OpenAudio S1-mini (0.5B) is CC-BY-NC-SA-4.0. — [LocalAIMaster](https://localaimaster.com/blog/best-local-tts-models)
- Breeze TTS 2 (BreezeBlue, released 25 Aug 2026): top open-weights model on the arena, but weights, derivatives and self-hosted outputs are research/non-commercial. — [OrcaRouter blog](https://www.orcarouter.ai/blog/breeze-tts-2-tops-open-weights-speech-arena) (secondary; licence text not read)
- StyleTTS2: code MIT, but users of the pretrained models must tell listeners the speech is synthesized unless they have permission to use the voice. — [PyPI styletts2](https://pypi.org/project/styletts2)
- VibeVoice: MIT, but Microsoft removed the long-form TTS code (Sept 2025); research models only. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models)
- Bark: MIT, can make laughter and non-verbal sounds, but last updated May 2023, slow, and weak for predictable narration. — [Yaps](https://www.yaps.ai/blog/best-local-tts-models); [LocalAIMaster](https://localaimaster.com/blog/best-local-tts-models)

### Inferences
- Summary of horror-relevant control, from the findings above:

| Model | Commercial OK? | 4-core CPU realistic? | Fear / whisper / breath control | Multi-character |
|---|---|---|---|---|
| Chatterbox Turbo | Yes (MIT) | Yes, slow in PyTorch; faster via ONNX / chatterbox.cpp (section 2) | Sound tags ([gasp] [sigh] [sniff]); no real whisper (local test) | Reference clips (synthetic Kokoro refs) |
| Chatterbox Nano | Yes (MIT repo) | Built for CPU, 3x RT on 8 cores | Paralinguistic tags (exact list unknown) | Not documented |
| Kokoro-82M | Yes | Yes | None (speed only) | 54 preset voices |
| Pocket TTS | Yes, with attribution (CC BY 4.0 weights) | Yes, ~2.3-2.5x RT on 4 vCPU | None, no pauses | Voices plus consented cloning |
| NeuTTS-2E | Unclear ("other", gated) | Claimed real time on laptop CPU | `fearful`, `sad`, `surprised` | 4 fixed speakers |
| Zonos v0.1 | Yes | Possible, "much slower" | fear slider, rate, pitch | Cloning / presets |
| Maya1, Orpheus, Dia | Yes (Orpheus also under Meta Llama terms) | Unlikely (1.6-3B, GPU-oriented) | Best tag sets (`<whisper>` Maya1; (inhales)/(screams) Dia; `<gasp>`/`<groan>` Orpheus) | Voice design / presets / [S1][S2] |
| IndexTTS2/2.5 | Contact bilibili | Unlikely (0.1x RT on M4) | 8-emotion vector incl. afraid, melancholic; duration control | Speaker separate from emotion |
| Qwen3-TTS | Yes | Unlikely (0.2x RT on M4) | Plain-language instructions for emotion and rate | VoiceDesign plus 9 presets |

- For this pipeline the realistic shortlist is: (a) keep Chatterbox Turbo but switch its runtime to ONNX or chatterbox.cpp for speed (section 2); (b) trial Chatterbox Nano on CPU for the narrator if its tags hold up; (c) trial NeuTTS-2E's "fearful" emotion for a horror narrator, but only after reading its licence; (d) Pocket TTS or Kokoro as fast fallbacks for plain lines.
- Whisper is the signature horror-narration texture. None of the CPU-friendly commercial models has a working whisper control: Turbo's [whispering] failed in local tests. Whisper-capable models are Maya1 (`<whisper>`, GPU), Fish (`[whisper]`, non-commercial) and Dia (no whisper tag listed). A practical workaround is DSP: a breathy/noise-excited layer under the narrator, or a separate pre-made whisper SFX.
- Voice design from a text description (Qwen3-TTS VoiceDesign, Maya1) and Kyutai's embeddings-only cloning create voices with no real-person reference, which fits CLAUDE.md's no-cloning rule. The current approach (synthetic Kokoro clips as Turbo references) fits it too.
- Watermark rule: the official Turbo ONNX example defaults to `apply_watermark = False` (section 2). To stay consistent with CLAUDE.md ("never strip other parties' provenance watermarks"), a move to ONNX or chatterbox.cpp should apply the `perth` watermark itself after generation.
- Pace variation: on the original Chatterbox, higher exaggeration speeds speech up and lower cfg_weight slows it. `tools/clone_tts.py` uses 0.6/0.6, which may add speed variance on that path. Models with explicit pace control are Kokoro `speed`, Zonos speaking rate, IndexTTS-2.5 `duration_factor` and Qwen3 instructions. Otherwise, time-stretching takes toward a target syllable rate (as the ElevenLabs path already does) stays the most deterministic fix.

### Gaps
- No Reddit (r/LocalLLaMA, r/TextToSpeech) threads came back in search, so community opinion here rests on blog roundups (Yaps, LocalAIMaster, ocdevel), not Reddit.
- No measured CPU speed for Chatterbox Turbo in Python/PyTorch, Nano on a 4-core x86 CPU, Orpheus GGUF on CPU, Maya1 GGUF, or NeuTTS-2E. These need a local benchmark.
- TTS Arena V2 leaderboard did not load. Chatterbox Turbo itself is not on the Artificial Analysis arena (only "Chatterbox" open and Resemble's hosted "Chatterbox HD").
- Full Chatterbox Nano tag list and Nano weights licence (separately from the repo's MIT) not confirmed. NeuTTS-2E licence text not read. Breeze TTS 2 and Fish Community License texts not read directly.
- Pocket TTS weights licence is from Yaps, not the repo page (the repo links per-voice licences).
- Unknown models in the arena snapshot (Ming-3.0-tts, Step Audio EditX, Voxtral TTS, Magpie-Multilingual 357M): licence, size and CPU viability were not researched.

---

## 2. How to speed up CPU inference for the leading candidates (ONNX, quantization, llama.cpp/ggml ports, batching)

### Takeaway
The biggest gain for the current setup (Turbo in PyTorch fp32 on CPU, ~40-60 s per sentence) is to change the runtime, not the model. Resemble ships an official Turbo ONNX export with fp32/fp16/q8/q4/q4f16 variants. The community ggml port chatterbox.cpp reports Turbo at Q4_0 running faster than real time on a desktop CPU (RTF 0.82 on a Ryzen 9 9950X), about 1.2x faster than ONNX Runtime on that CPU. Small CPU-native models (Nano, Pocket TTS, Kokoro ONNX, NeuTTS GGUF) are the other route.

### Cited Findings
- Official Chatterbox Turbo ONNX: dtype options fp32, fp16, q8, q4, q4f16. The example runs on ONNX Runtime, clones from a 24 kHz reference clip, and has an `apply_watermark` flag set to False in the sample code. — [HF ResembleAI/chatterbox-turbo-ONNX](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX)
- Community ONNX Turbo (q4f16): four graphs (reference speech encoder, embeddings, autoregressive LM, conditional decoder). The LM's q4f16 weights are ~222 MB. — search summary of [KitsuMate/chatterbox-turbo-onnx](https://huggingface.co/KitsuMate/chatterbox-turbo-onnx) and [Dvirile/chatterbox-turbo-lora](https://huggingface.co/Dvirile/chatterbox-turbo-lora)
- chatterbox.cpp (C++/ggml, MIT, 2026, "early-stage": 6 stars, no releases) runs Turbo and Multilingual on CPU, Metal, CUDA and Vulkan with no Python at runtime. Reported (RTF = wall/audio):
  - Turbo Q4_0 on Ryzen 9 9950X: 5,397 ms wall, RTF 0.82, ~1.2x faster than ONNX Runtime on that CPU.
  - Turbo Q4_0 on M3 Ultra: RTF 1.05, ~2.3x faster than ONNX Runtime.
  - Multilingual Q4_0 on Apple M4 with 4 threads: RTF 4.32 (F16: 6.70), ~3x faster than ONNX Runtime.
  - Q4_0 can give a different sample than F16 from the same seed; subjective quality is similar.
  - Supports cloning from a >5 s reference (10-15 s recommended) with cached voice profiles (`--save-voice`). Exaggeration is supported only for Multilingual.
  - The README mentions neither paralinguistic tags nor the watermark.
  - — [GitHub gianni-cor/chatterbox.cpp](https://github.com/gianni-cor/chatterbox.cpp)
- Chatterbox Nano is the official CPU-targeted variant (3x real time on 8 cores). — [GitHub resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)
- Kokoro ONNX (kokoro-onnx, MIT): ~300 MB, ~80 MB quantized, "near real-time on macOS M1". — [GitHub thewh1teagle/kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx). The HF card lists 107 quantized variants. — [HF Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- Orpheus has a documented no-GPU path via llama.cpp (orpheus-cpp with CPU-optimized llama-cpp-python). — [GitHub canopyai/Orpheus-TTS](https://github.com/canopyai/Orpheus-TTS)
- NeuTTS Air/2E ship GGML/GGUF (Q4/Q8). Q4_0 benchmarks cover Galaxy A25, Ryzen 9 HX 370, iMac M4 and RTX 4090. — [PyPI neutts](https://pypi.org/project/neutts/); [HF neutts-2e](https://huggingface.co/neuphonic/neutts-2e)
- Pocket TTS uses only 2 CPU cores at ~6x real time on an M4 MacBook Air, and ~2.3-2.5x real time on a 4-vCPU x86 VM. — [GitHub kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts)
- Kyutai TTS is "easy to batch" and can use fewer audio tokens per frame at inference for speed. MLX offers `--quantize 8/4` (Apple only). — [HF kyutai/tts-1.6b-en_fr](https://huggingface.co/kyutai/tts-1.6b-en_fr); [GitHub delayed-streams-modeling](https://github.com/kyutai-labs/delayed-streams-modeling)
- UNVERIFIED / likely unreliable: a 2026 guide claims Turbo batch synthesis is "~40% faster" and voice preloading "~5x faster", but the API names it uses (`synthesize_batch`, `preload_voices`, `emotion_intensity`) do not appear in the official repo. Do not rely on it. — [Codersera Turbo guide](https://codersera.com/blog/chatterbox-turbo-run-and-install-locally-free-elevenlabs-alternative-2026/amp/)

### Inferences
- The current ~40-60 s per sentence (~3 s of audio) is roughly RTF 13-20 (wall/audio). chatterbox.cpp's Turbo Q4_0 figure (0.82 on a 16-core desktop) suggests an order-of-magnitude gain is plausible. A 4-core machine will be slower than a 9950X, so expect several times faster than now, not real time. This must be measured locally.
- Any runtime switch must re-run the existing checks: Whisper medium on every line, and the tag-fired check (`voice._sound_ok`). Quantization (Q4) changes samples per seed and may change how reliably tags fire. Also re-apply the PerTh watermark (see section 1).
- One cheap optimization needs no new model: reuse conditionals and voice profiles across sentences (load the model and reference once per video, not per sentence). chatterbox.cpp's `--save-voice` exists for exactly this. Whether `tools/clone_tts.py` already does this was not checked in depth.
- On a 4-core box, two 2-core Pocket TTS or Kokoro workers could run in parallel for plain lines while Turbo handles tagged emotional lines.

### Gaps
- No PyTorch-CPU tuning numbers (threads, bf16 on CPU, int8 dynamic quantization, OpenVINO) for Chatterbox were found.
- No independent CPU benchmark of the official Turbo ONNX at q8/q4 on x86.

---

## 3. Royalty-free / CC0 horror sound libraries for a monetized YouTube channel: licences and attribution

### Takeaway
Safe without attribution: Sonniss #GameAudioGDC (licence v2.0 from 27 Aug 2026: commercial and video use, no attribution, no AI training, no reselling as SFX), Freesound CC0, Pixabay (no attribution; no standalone redistribution) and YouTube Audio Library "Attribution not required" items. Freesound CC BY needs a credit. Freesound CC BY-NC and Sampling+ are off-limits for a monetized channel. BBC Sound Effects (RemArc) is personal/educational/research only, so a monetized channel needs a paid licence.

### Cited Findings
- **Sonniss #GameAudioGDC licence v2.0** (effective 27 Aug 2026; applies to files downloaded on or after that date; older downloads follow the version in force on the download day, archived on a previous-versions page):
  - You "may use and modify the licensed sound effects for personal and commercial projects… without attribution to the original creator".
  - Synchronization covers "Games, films, videos, podcasts, apps and interactive projects".
  - You may not "distribute, publish, sub-license or otherwise supply the sound effects as sound effects" (raw or modified, including in packs).
  - Using them for AI training is "expressly prohibited".
  - — [Sonniss GDC bundle licence](https://sonniss.com/gdc-bundle-license/)
- **Freesound licences:**
  - CC0: anything, including selling; you can't claim authorship; no attribution.
  - CC BY: commercial use allowed with credit.
  - CC BY-NC: credit required, and "you can't earn money" from the work.
  - Sampling+ (legacy): roughly BY-NC, and not allowed in commercial advertising.
  - The search filter "Free Cultural Works" returns only CC0 or CC BY.
  - Credit format: sound name, uploader, sound URL and licence. A link to a full credits page is allowed when space is short. Downloaded sounds are listed at freesound.org/home/attribution/.
  - — [Freesound FAQ](https://freesound.org/help/faq/)
- **Pixabay Content License (summary):**
  - Free, no attribution required, can be modified.
  - You may not sell or distribute content "on a Standalone basis".
  - Not in trademarks or for misleading or illegal use.
  - You must check third-party rights yourself.
  - The summary is non-binding (the full licence governs) and says nothing about YouTube Content ID.
  - — [Pixabay licence summary](https://pixabay.com/service/license-summary/)
- **YouTube Audio Library:**
  - YouTube Partner Program members can monetize videos that use Audio Library music and SFX.
  - Downloaded Audio Library tracks won't be claimed through Content ID.
  - Creative Commons tracks need an artist credit in the description; the filter "Attribution not required" finds standard-licence tracks.
  - — [YouTube Help: Use music and sound effects from the Audio Library](https://support.google.com/youtube/answer/3376882?hl=en)
- **BBC Sound Effects (RemArc licence):**
  - Free for personal, educational or research use; commercial use needs a licence, and individual sounds can be bought.
  - "Research" excludes AI training and data mining.
  - One news piece suggests a short film "on your personal YouTube channel" is probably fine, which conflicts with treating a monetized channel as commercial.
  - — [DIY Photography](https://www.diyphotography.net/the-bbc-sound-effects-archive-is-now-free-to-download-with-over-33000-files/); [MusicRadar](https://www.musicradar.com/news/the-bbc-is-letting-you-download-more-than-16000-free-sound-effect-samples-from-its-archive). The official licensing page (sound-effects.bbcrewind.co.uk/licensing) could not be fetched.

### Inferences
- For this channel: use Sonniss GDC bundles first. They are pro-recorded, include large horror-useful categories (ambiences, foley, impacts) and need no credit. Then Freesound filtered to CC0 (or CC BY with a description credit line), then YouTube Audio Library SFX. Treat BBC RemArc as not usable for a monetized channel unless sounds are bought.
- Keep a per-video SFX log (file, source, licence, URL). Freesound CC BY needs it for credits, and Sonniss's licence version depends on the download date.
- Synthesizing SFX in numpy (current practice) avoids licensing entirely. Section 4's roughness and nonlinearity findings are easy to synthesize.

### Gaps
- The official BBC RemArc licence text and Pixabay's full terms (and any Pixabay Content ID or music-claim policy) were not read.
- Which Sonniss bundle years contain the most horror material was not researched.

---

## 4. Evidence-based horror sound design (silence, nonlinear/rough sounds, low rumble and infrasound, risers, heartbeat, binaural) and what survives phone speakers

### Takeaway
The strongest evidence supports "rough" and noisy nonlinear sounds as fear signals: noise and noisy screams in horror scores; amplitude modulation at 30-150 Hz ("roughness") driving amygdala response. Also supported: sudden, fast-onset loud sounds for startle, made bigger by prior anxiety, and fast heartbeat sounds raising anxiety. Two caveats matter for Shorts. First, with video on screen, added nonlinearities still darkened the mood but no longer raised arousal. Second, infrasound and deep sub-bass are physically absent on phone speakers (microspeaker resonance ~500-1000 Hz, rolling off ~12 dB/octave below). Low dread must therefore come from harmonics, roughness and mid-range texture, not from sub frequencies.

### Cited Findings
**Nonlinear / noisy sounds**
- Blumstein, Davitian and Kaye (2010, *Biology Letters* 6:751-754) analysed 102 films (24 horror), with a 30-s iconic clip per film. Horror soundtracks had fewer abrupt frequency shifts and musical sidebands, more non-musical sidebands, and more noisy female screams (p = 0.002). The authors link this to animal alarm and fear screams ("commonly produced when animals are under duress"; meerkat alarm calls "get noisier as the urgency… increases"). They argue harsh, unpredictable sounds capture attention and resist habituation. Conclusion: "noise in horror films" is used to elicit fear. — [PMC3001365](https://pmc.ncbi.nlm.nih.gov/articles/PMC3001365)
- Blumstein, Bryant and Kaye (2012, *Biology Letters* 8:744-747) used 12 neutral 10-s pieces, with noise or abrupt pitch shifts added at 5 s.
  - Music only (n = 42): noise raised arousal (p < 0.0001), upward shifts raised arousal (p = 0.029), and noise and downward shifts lowered valence (p = 0.005, p < 0.0001).
  - With a benign video (n = 42): no arousal effect (p = 0.755), but noise and downward shifts still lowered valence (p = 0.014, p = 0.010).
  - Quote: "the presence of a video image suppressed the ability of simulated nonlinearities to modify arousal."
  - — [PMC3440987](https://pmc.ncbi.nlm.nih.gov/articles/PMC3440987)
- Arnal et al. (2015, *Current Biology* 25:2051-2056): screams carry "roughness", fast amplitude/frequency modulation at 30-150 Hz, a range normal speech (4-5 Hz modulation) does not use. Screams and artificial alarms both raised amygdala activity (fMRI, n = 16), and the roughest sounds were rated most frightening. — [ScienceDaily](https://www.sciencedaily.com/releases/2015/07/150716123834.htm); [Max Planck press release](https://www.aesthetics.mpg.de/en/newsroom/news/news-article/article/scream-if-you-have-to.html); paper record at [UNIGE archive](https://archive-ouverte.unige.ch/unige:75898)

**Startle, and silence before a scare**
- Psychophysiologist Christian Grillon (via Inverse): sound is the most effective startle trigger, and startle depends on intensity and how abruptly the sound arrives. A slow build (a plane taking off) does not startle like a door slam. Being anxious first potentiates startle; the quoted "100 to 300 percent" increase is secondhand (UNVERIFIED). — [Inverse](https://www.inverse.com/article/7531-the-unexpected-physiology-of-jump-scares)
- In the lab, threat-of-shock (NPU task, Grillon and colleagues) separates phasic fear from sustained anxiety. Startle is potentiated during threat, especially unpredictable threat. — [JoVE protocol](https://jove.com/51905)
- No peer-reviewed study was found that isolates "silence before the scare" as a variable (see Gaps).

**Infrasound and low rumble: myth vs evidence**
- Tandy and Lawrence (1998, *J. Society for Psychical Research*) traced a "ghost" in a Coventry lab to a fan emitting ~19 Hz and proposed infrasound effects such as fear and shivering. — [Wikipedia: Vic Tandy](https://en.wikipedia.org/wiki/Vic_Tandy)
- Wiseman's 2003 London concerts laced some pieces with 17 Hz infrasound and reported more unusual experiences although listeners could not consciously detect it (percentages not retrieved). — search summary of [Wikipedia: Vic Tandy](https://en.wikipedia.org/wiki/Vic_Tandy) and [Smithsonian](https://www.smithsonianmag.com/smart-news/five-scientific-explanations-spooky-sensations-180973436) (UNVERIFIED: pages not fully read)
- Schmaltz et al. (*Frontiers in Behavioral Neuroscience*, published Apr/May 2026, MacEwan University) studied n = 36 (27 women) listening to calm or unsettling music, with hidden subwoofers playing 18 Hz to half of them. The infrasound group had higher salivary cortisol, more irritability and rated the music sadder. Participants could not tell whether infrasound was on. Caveats: small sample, one frequency. Schmaltz: it does not make people see ghosts but may give "unexplainable discomfort". — [Popular Science](https://www.popsci.com/science/haunted-sounds-feelings/); [ScienceAlert](https://www.sciencealert.com/hidden-phenomenon-could-explain-why-old-buildings-feel-haunted-study-finds); [404 Media](https://www.404media.co/scientists-investigated-a-frequency-linked-to-paranormal-encounters-the-results-were-unsettling/)

**Phone speakers: frequency limits**
- Smartphone microspeakers resonate at roughly 500-1000 Hz. A Knowles 11x15 mm phone speaker datasheet gives 800 Hz ±10% (1 cm³ back cavity; 450 Hz on a baffle without a back cavity). Output falls ~12 dB/octave below resonance, and low end drops faster below ~300 Hz in small phones. These figures come from search summaries; the pages were not opened in full. — [audioXpress: microspeakers anatomy](https://www.audioxpress.com/article/microspeakers-anatomy-how-to-design-audio-systems-with-very-small-drivers); Knowles datasheets via [eicom 440124](https://cdn.eicom.ru/media/PDF/440124.pdf) / [eicom 3468456](https://cdn.eicom.ru/media/PDF/3468456.pdf)
- Notebookcheck phone reviews measure bass in the 100-315 Hz band and often find weak or "nearly no bass": Moto G37 ~28% below median; Asus ZenFone 3 Max 37.7% below; Lenovo C2 34.3% below. — [Notebookcheck review](https://www.notebookcheck.net/Apple-wouldn-t-sell-something-like-this-This-smartphone-s-sound-test-shocks-us.1356637.0.html); [Notebookcheck (CN) ZenFone 3 Max](https://www.notebookcheck-cn.com/ZenFone-3-Max-ZC520TL.192030.0.html); [Notebookcheck (CN) Lenovo C2](https://www.notebookcheck-cn.com/C2.197976.0.html)
- Missing-fundamental effect: when only the harmonics of a bass tone are played, listeners still perceive the fundamental. Psychoacoustic bass enhancers (MaxxBass, SRS TruBass) exploit this for small speakers. — [Aalto thesis: missing fundamental](https://aaltodoc.aalto.fi/items/28f25581-3beb-49e4-8418-506dcb5b3446); [US patent 8,625,813](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8625813)

**Heartbeat**
- False fast heart-rate feedback raised self-reported fear and lowered perceived stability at height (Hill, Johnson and Ellmers 2024, *Biological Psychology*, n = 60; effect sizes 0.79-1.78). Slow feedback had no significant effect. — [Coventry pure portal](https://pureportal.coventry.ac.uk/en/publications/the-influence-of-false-interoceptive-feedback-on-emotional-state-/)
- Fast heartbeat sound and/or vibration raised anxiety and heart rate in both calm and stressed states (Glasgow, 2023). — [Glasgow eprints](https://eprints.gla.ac.uk/305397)
- In a conference poster, heartbeat false feedback amplified emotional responses to pictures: fast rates raised arousal, slow rates calmed (Tajadura et al., 2006, preliminary). — [IMRF 2006 abstract](https://imrf.mcmaster.ca/2006/viewabstract.php%3Fid=161.html)

**Risers / Shepard tone**
- The Shepard tone layers octave-spaced tones that fade in at the bottom and out at the top, giving an endlessly rising pitch. Nolan used it in *Dunkirk*'s score ("a continuing ascension of tone"). This is craft evidence, not experimental. — [Inverse](https://www.inverse.com/article/34765-shepard-tone-dunkirk-christopher-nolan-soundtrack); [Mental Floss](https://www.mentalfloss.com/entertainment/movies/inside-auditory-illusion-makes-hans-zimmers-movie-scores-so-anxiety-producing)
- Upward abrupt pitch shifts raised arousal in music-only listening (p = 0.029). — [PMC3440987](https://pmc.ncbi.nlm.nih.gov/articles/PMC3440987)

**Binaural / close-mic**
- The evidence is small and mixed:
  - Aalborg VR horror master's thesis (2015): no questionnaire difference between stereo and 3D audio, but electrodermal responses differed. — [AAU project page](https://projekter.aau.dk/projekter/files/213012770/151031_Rapport.pdf)
  - Interactive binaural audio story (Stephen King text, 2019): a trend toward higher immersion and fear. — [AAU VBN](https://vbn.aau.dk/da/publications/creating-an-audio-story-with-interactive-binaural-rendering-in-vi)
  - Indonesian horror-film study (2025, n = 60 film students): the binaural group reported higher immersion and stronger physiological responses. — [Garuda / Journal of Dialogos](https://garuda.kemdiktisaintek.go.id/documents/detail/5975501)

### Inferences
- Roughness is the most phone-proof fear cue in the evidence. Amplitude-modulating a mid/high-frequency carrier (noise, a drone, a voice) at 30-150 Hz makes it "rough", and the carrier sits where phone speakers work. This is trivial in the existing numpy SFX code.
- Because video suppressed arousal effects in Blumstein 2012, nonlinear "texture" in a Short will mostly shift mood darker (valence). For arousal spikes, rely on startle mechanics: an abrupt onset after a quiet stretch, fast attack, broadband content. Pair them with a visual threat rather than a benign image.
- "Silence before the scare" has no direct study, but the mechanism holds. Startle needs abrupt onset; anticipation and anxiety potentiate startle. Under YouTube's -14 LUFS normalization (section 5), a quiet stretch also makes the hit loud by contrast. Shorts can't afford long dead air (channel rule), so the practical form is a short drop-out (~0.3-0.8 s; assumption, not sourced) of music and ambience under the line before the hit. The pipeline's `TWIST` music drop already does this.
- Infrasound and sub-bass rumble cannot reach a viewer on a phone speaker. It may reach headphone listeners, but the 18-19 Hz evidence is a small lab study with subwoofers. For "low dread" on phones, synthesize the rumble's harmonics (e.g. 80-300 Hz partials plus distortion or saturation so the missing fundamental is implied) and add roughness. A heartbeat's audible part on phones is its attack/click and low-mid "thump" harmonics, not its ~40-60 Hz body.
- Binaural and close-mic breathing only work on headphones. On a phone speaker the spatial cue collapses. Close-mic breaths still read as intimate (dry, mid-range, high presence). Use them as a texture that works on both, not as a binaural effect.
- A heartbeat that speeds up through the setup is supported by evidence (fast false feedback raised fear and anxiety; slow did not), and it doubles as a rhythmic tension bed under narration.

### Gaps
- No peer-reviewed study isolating pre-scare silence length, and none on horror sound specifically on phone speakers or in vertical short-form video.
- Wiseman 2003 effect sizes and the Schmaltz 2026 paper were not read in full (press coverage only).
- No source found on the share of Shorts viewers using headphones vs phone speakers (needed to weigh binaural effort).

---

## 5. Loudness targets for YouTube and mixing voice vs ambience for mobile

### Takeaway
YouTube turns playback down toward about -14 LUFS integrated loudness (since 2019) and does not turn quiet uploads up. So master Shorts at about -14 LUFS with true peak ≤ -1 dBTP (common advice), keeping dynamic contrast inside the track rather than mastering quiet. For voice vs bed, research shows highly individual preferences and that older or hearing-impaired viewers want more speech-to-background separation. Keep narration clearly on top (it already has captions) and duck ambience and music under speech.

### Cited Findings
- YouTube changed its playback reference to -14 LUFS (Ian Shepherd, 18 Sep 2019). YouTube and TIDAL "don't turn quieter songs up". Before the change, YouTube's displayed values could differ from LUFS by up to 3 dB. — [MeterPlugs blog](https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html)
- -14 LUFS is the reference for the main YouTube video platform (louder material is turned down). YouTube Music only reduces music louder than -7 LUFS. — [Production Advice, Oct 2023](https://productionadvice.co.uk/youtube-music/)
- "Stats for nerds" → content loudness: a positive value (e.g. 6 dB) means the video is that much louder than the reference and is turned down. A negative value means it's quieter, and no normalization is applied. — search summary of [Youlean](https://youlean.co/?p=30813) (UNVERIFIED: page not opened)
- No official YouTube Help page stating -14 LUFS was found. The figure rests on mastering-engineer and meter-vendor sources (above).
- AES TD1008 (audio-only streaming), as reported: speech/"assorted" content -18 LUFS; music ≤ -16 LUFS; mixed content -17 LUFS. True peak max -1 dBTP is common in the older TD1004. — [Production Advice TD1008](https://productionadvice.co.uk/td1008/); [Production Expert](https://www.production-expert.com/production-expert-1/aes-update-loudness-recommendations-for-audio-only-streaming)
- Speech vs background preferences:
  - Torcoli et al. (2017, normal-hearing listeners, median age ~25): preferred speech-to-background loudness differences ranged 0-13 LU, and personalising the mix significantly raised satisfaction.
  - BBC 1991 study (~336 viewers, mean age just over 60, background at -6/0/+6 dB): no definite preference, but the preferred speech-to-background SNR related to the degree of hearing loss.
  - Two 2010 surveys: 60% of 20,000 viewers had difficulty following TV speech.
  - Listeners over 65 preferred larger differences than the original mixes.
  - — [Straninger 2020 thesis (Fraunhofer IIS / Ansbach), arXiv 2006.14282](https://arxiv.org/pdf/2006.14282)
- Audio experts prefer louder backgrounds than non-experts, and individual preferences vary widely (ducking study with Torcoli, Shirley and others, 22 listeners). — search summary, [Salford repository](https://salford-repository.worktribe.com/output/1360952) (UNVERIFIED: not opened)

### Inferences
- Target: integrated ≈ -14 LUFS for the final Short, true peak ≤ -1 dBTP. Mastering much quieter just plays quieter on YouTube (no boost). Mastering louder only gets turned down and loses scare dynamics to limiting.
- Mix the scare hit and the quiet passages around a narration that sits consistently on top. Measure short-term loudness of the narration bus vs the bed. Older viewers prefer larger speech-to-background differences and preferences vary, so err toward clear speech: the existing sidechain duck (20 ms / 300 ms) under narration, with beds well below speech. The exact LU gap is a judgement call; the evidence gives a 0-13 LU preference range, not a single number.
- Check mixes on a phone speaker (or a high-pass around 300-500 Hz simulating one, from section 4) as well as headphones. Anything that only lives below ~200 Hz disappears on phones.
- Whisper-medium checks stay the clarity gate for narration. Re-run them on the final mixed track (narration plus bed), not only on the dry takes, because the bed can mask consonants.

### Gaps
- No official YouTube documentation of the -14 LUFS target or of Shorts-specific normalization was found.
- No peer-reviewed speech-to-background target specifically for phone-speaker listening or short-form video.
- The EBU R128 / -3 dBTP lossy-codec recommendation appeared only in a search snippet (UNVERIFIED) and was left out of the targets above.
