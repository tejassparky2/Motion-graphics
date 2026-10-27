# Open-source anime-style voices, YouTube AI policy, and anime image-model licences (researched 2026-10-27)

Scope note: this is not legal advice. Licence files were downloaded directly from GitHub and Hugging Face on 2026-10-27, so the "current" terms below are as of that date. YouTube Help pages show no revision date, only "©2026 Google", so treat them as current on 2026-10-27. "Local" marks a measurement or file in this repo or container. "Secondary" marks a claim from a search summary or a third-party write-up rather than the primary page.

## A1. Licences and commercial-use terms of the open voice tools (code vs. weights)

### Takeaway
For a monetized channel, the clean choices are **Chatterbox (MIT code and weights)**, **Kokoro-82M (Apache-2.0 weights)**, **CosyVoice 2/3 (Apache-2.0)**, **Zonos (Apache-2.0)** and **GPT-SoVITS (MIT code and pretrained weights)**. IndexTTS-2/2.5 is royalty-free below very large thresholds, but its own README and disclaimer send mixed signals about commercial use.

Three tools are not clean:
- **F5-TTS weights** are non-commercial (CC-BY-NC).
- **Fish Audio S2-Pro** is non-commercial only. **Drama 3** and the Fish Speech code fall under a new revenue-capped community licence (under USD 500k), which also requires attribution.
- **Style-Bert-VITS2** is AGPL code. Its bundled voices carry their own terms: CC BY-SA, or Amitaro's rules with a mandatory credit.

### Cited Findings
**GPT-SoVITS**
- Code is MIT ("Copyright (c) 2024 RVC-Boss"). — [GPT-SoVITS LICENSE](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/LICENSE)
- The pretrained-weights repo on Hugging Face is tagged `license: mit`. — [lj1995/GPT-SoVITS](https://huggingface.co/lj1995/GPT-SoVITS)
- The README lists v2, v3, v4, v2Pro/v2ProPlus and now a **V5** set of pretrained models (`gsv-v5-pretrained`). — [GPT-SoVITS README](https://github.com/RVC-Boss/GPT-SoVITS)

**Style-Bert-VITS2 (SBV2)**
- Code is **AGPL-3.0**, "the same as the original Bert-VITS2 repository". The `text/user_dict/` module is LGPL-3.0, inherited from VOICEVOX. — [Style-Bert-VITS2 README](https://github.com/litagin02/Style-Bert-VITS2)
- The repo's "requests" document (お願い) says its usage requests are *not binding*, and that only the repo licence binds. It asks users not to use SBV2 for illegal, political, harmful or impersonation/deepfake purposes. — [SBV2 TERMS_OF_USE.md](https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md)
- **JVNV default models** (jvnv-F1/F2/M1/M2-jp) inherit the JVNV corpus licence, **CC BY-SA 4.0**. — [SBV2 TERMS_OF_USE.md](https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md); [litagin/style_bert_vits2_jvnv](https://huggingface.co/litagin/style_bert_vits2_jvnv)
- **Koharune Ami / Amitaro default models:**
  - Commercial and non-commercial use are both OK if you follow Amitaro's rules.
  - A credit is **required** wherever generated audio is published, e.g. "Style-BertVITS2モデル: あみたろ、あみたろの声素材工房 (https://amitaro.net/)".
  - Prohibited: age-restricted works; works deeply tied to new religions, politics or MLM; defamation of groups, people or nations; presenting the output as Amitaro's own voice or as anyone else's voice.
  - Merges that keep ≥25% of her voice stay under her rules.
  - — [SBV2 TERMS_OF_USE.md](https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md); [Amitaro voice rules](https://amitaro.net/voice/voice_rule/)

**Fish Speech / Fish Audio**
- The repo LICENSE is now the **"Fish Audio Community License Agreement, Version 1.0 — Last Updated: October 13, 2026"**. It covers the Fish Speech code and the **Drama 3** model. — [fish-speech LICENSE](https://github.com/fishaudio/fish-speech/blob/main/LICENSE)
- Commercial use is free only "while Your Annual Revenue is less than USD 500,000". Annual Revenue means total gross revenue from all sources. Above the threshold you must notify business@fish.audio within 30 days, and you get a 90-day transition. Hosted TTS services always need a separate licence. — [fish-speech LICENSE](https://github.com/fishaudio/fish-speech/blob/main/LICENSE)
- Attribution: "If You distribute or make available the Fish Audio Materials or a Derivative Work, or a product or service that uses any portion of them, You shall prominently display 'Built with Fish Audio'". Outputs are explicitly *not* Derivative Works, and "You own any outputs". — [fish-speech LICENSE](https://github.com/fishaudio/fish-speech/blob/main/LICENSE)
- Use restriction: you may not "generate speech that imitates the voice of an identifiable natural person without that person's prior consent". Breach of the use restrictions terminates the licence automatically. Outputs may not be used to train other speech models. — [fish-speech LICENSE](https://github.com/fishaudio/fish-speech/blob/main/LICENSE)
- **S2-Pro** weights are under the "Fish Audio Research License". The model card says "Research and non-commercial use is permitted free of charge. Commercial use requires a separate license", and the download gate makes you tick "I agree to use this model for non-commercial use ONLY". — [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro); [fish-speech README](https://github.com/fishaudio/fish-speech)
- **Licence conflict:** the Drama 3 model card's front-matter says `license_name: fish-audio-research-license`, but its body text says "licensed under the Fish Audio Community License". — [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3)

**CosyVoice**
- The repo LICENSE is Apache-2.0. — [CosyVoice repo](https://github.com/FunAudioLLM/CosyVoice)
- The model cards for Fun-CosyVoice3-0.5B-2512 and CosyVoice2-0.5B are both tagged `license: apache-2.0`. — [Fun-CosyVoice3-0.5B-2512](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512); [CosyVoice2-0.5B](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B)
- The README disclaimer reads: "The content provided above is for academic purposes only … Some examples are sourced from the internet." This refers to the demo content, not a licence restriction. — [CosyVoice README](https://github.com/FunAudioLLM/CosyVoice)

**F5-TTS**
- "Our code is released under MIT License. The pre-trained models are licensed under the CC-BY-NC license due to the training data Emilia". The Hugging Face card is tagged `license: cc-by-nc-4.0`. — [F5-TTS README](https://github.com/SWivid/F5-TTS); [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS)

**Chatterbox (Resemble AI)**
- Code is MIT ("Copyright (c) 2025 Resemble AI"). The Chatterbox and Chatterbox-Turbo model cards are tagged `license: mit`. — [chatterbox LICENSE](https://github.com/resemble-ai/chatterbox); [ResembleAI/chatterbox-turbo](https://huggingface.co/ResembleAI/chatterbox-turbo); [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox)
- "Every audio file generated by Chatterbox includes Resemble AI's Perth (Perceptual Threshold) Watermarker". The README provides an extraction script. — [chatterbox README](https://github.com/resemble-ai/chatterbox)
- The model-card disclaimer says only: "Don't use this model to do bad things." — [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox)

**Kokoro-82M**
- Weights are `license: apache-2.0`. The card says: "Kokoro has been deployed in numerous projects and commercial APIs. We welcome the deployment of the model in real use cases." — [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- The model card's "Creative Commons Attribution" section lists two CC BY datasets in the training set:
  - Koniwa `tnc` (CC BY 3.0)
  - SIWIS (CC BY 4.0)

  VOICES.md has a "CC BY" column that ties the Japanese voices jf_gongitsune, jf_nezumi, jf_tebukuro and jm_kumo to Koniwa texts. — [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M); [Kokoro VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

**Zonos**
- Both the repo LICENSE and the model card (`Zonos-v0.1-transformer`) are Apache-2.0. — [Zonos repo](https://github.com/Zyphra/Zonos); [Zyphra/Zonos-v0.1-transformer](https://huggingface.co/Zyphra/Zonos-v0.1-transformer)

**IndexTTS (bilibili)**
- Licence: "bilibili Model Use License Agreement", which grants a "worldwide, non-exclusive, non-transferable, royalty-free limited license to Use the Model or any Derivative Work". — [index-tts LICENSE](https://github.com/index-tts/index-tts/blob/main/LICENSE)
- **Separate-licence threshold:** a separate licence is needed only if you or your affiliates had more than 100 million monthly active users, or more than RMB 1 billion annual revenue.
- **Notices:** you must keep the copyright notices and a copy of the agreement.
- **Training restriction:** you may not use it to improve other AI models, except the model's own derivatives or non-commercial models.
  — [index-tts LICENSE](https://github.com/index-tts/index-tts/blob/main/LICENSE)
- The same README also says "For commercial usage and cooperation, please contact indexspeech@bilibili.com". — [index-tts README](https://github.com/index-tts/index-tts)
- The Chinese DISCLAIMER forbids synthesizing "political figures, public figures or any unauthorized individual's voice". It also forbids "未经授权将合成声音用于商业目的" (using synthesized voices commercially without authorization). — [index-tts DISCLAIMER](https://github.com/index-tts/index-tts/blob/main/DISCLAIMER)

### Inferences
- **Fully permissive for monetized output, no revenue cap:** Chatterbox, Kokoro, CosyVoice 2/3, Zonos and GPT-SoVITS. Chatterbox's PerTh watermark is a provenance mark; per the channel's CLAUDE.md rule, it must not be stripped.
- **Prohibit or limit commercial use:**
  - F5-TTS pretrained weights (CC-BY-NC).
  - Fish S2-Pro (non-commercial).
  - Fish Drama 3 and the Fish Speech code: commercial use only under USD 500k total revenue, plus "Built with Fish Audio" attribution. Whether a YouTube video counts as a "product or service that uses" the materials is unclear, so crediting in the description is the cautious reading. Drama 3 is a 35B-A3B MoE benchmarked on H200 GPUs, so it is impractical on CPU anyway.
- **Require attribution:**
  - The SBV2 Amitaro/Koharune Ami voices (credit mandatory).
  - JVNV voices (CC BY-SA 4.0: attribution plus share-alike; whether share-alike reaches a video soundtrack is uncertain).
  - Fish Audio materials ("Built with Fish Audio").
  - Kokoro's Koniwa-derived Japanese voices. Their CC BY 3.0 origin suggests crediting Koniwa, as a precaution.
- **AGPL:** SBV2's AGPL licence covers the software. Generating audio files for videos does not distribute or network-serve the software, so the AGPL is very likely not triggered by publishing videos. (Interpretation; not legal advice.)
- **IndexTTS:** the formal licence is permissive for a small channel, but the "contact us for commercial usage" line and the disclaimer's "unauthorized commercial use of synthesized voices" clause create ambiguity. Get written confirmation from indexspeech@bilibili.com before monetized use.

### Gaps
- Licence of older Fish Speech / OpenAudio S1-mini weights was not verified: the Hugging Face page returned 401 (gated). Earlier Fish Speech versions are commonly reported as CC-BY-NC-SA-4.0, but this is unverified here.
- I did not check whether IndexTTS-1.x was released under the same bilibili licence, or whether IndexTTS-2.5's model card has its own licence tag.
- The training-data provenance of the GPT-SoVITS pretrained base and of CosyVoice's base model is not stated in the files reviewed.

## A2. English and Japanese quality, emotion control, and pretrained voices that are not clones of real people

### Takeaway
Most modern open TTS models are **zero-shot cloners with no stock voices**: GPT-SoVITS, F5, Zonos, IndexTTS and Fish all need a reference clip. That makes reference-audio provenance the whole ethical question.

Ready-made voices that are not clones of a real person:
- **Kokoro's 54 preset voices.** Trained only on permissive data, and the card says no "custom voice clones". Weak Japanese, and no emotion control.
- **Chatterbox's built-in default conditioning (`conds.pt`).** Its source is undocumented.
- **SBV2's JVNV and Amitaro voices.** Recorded with the speakers' permission for corpora or free voice material. Japanese-first, with real emotion styles.

The best emotion control is in:
- IndexTTS-2/2.5 (emotion vectors and text).
- Chatterbox Turbo (`[laugh]`/`[chuckle]`/`[cough]` tags) and original Chatterbox (exaggeration slider).
- Zonos (emotion vector).
- CosyVoice (instruct).
- SBV2 (7 emotion styles).

### Cited Findings
**GPT-SoVITS**
- Zero-shot from a 5-second sample, or few-shot fine-tuning with 1 minute of data.
- Supported languages: English, Japanese, Korean, Cantonese, Chinese.
- The roadmap item "Enhanced TTS emotion control" is struck through ("Maybe use pretrained finetuned preset GPT models for better emotion").
- v3/v4 "lean more toward the reference audio".
- — [GPT-SoVITS README](https://github.com/RVC-Boss/GPT-SoVITS)

**Style-Bert-VITS2**
- JVNV models come with 7 styles (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral) and are tagged languages ja/zh/en. The JP-Extra versions are Japanese-focused. — [litagin/style_bert_vits2_jvnv](https://huggingface.co/litagin/style_bert_vits2_jvnv)
- SBV2 can make style vectors from audio and set emotion strength continuously. — [Style-Bert-VITS2 README](https://github.com/litagin02/Style-Bert-VITS2)

**Kokoro**
- v1.0 (2025-01-27) has 54 voices in 8 languages. — [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- Training data was "exclusively … permissive/non-copyrighted audio": public domain audio, Apache/MIT-licensed audio, and "Synthetic audio generated by closed TTS models from large providers". The card adds: "No synthetic audio from open TTS models or 'custom voice clones'". — [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- Japanese voices (4F/1M) grade only **C- to C+**. Top English voices: af_heart "A", af_bella "A-". — [Kokoro VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

**Chatterbox**
- Turbo (350M, English) has native paralinguistic tags (`[cough]`, `[laugh]`, `[chuckle]`), and "excels at narration and creative workflows". — [chatterbox README](https://github.com/resemble-ai/chatterbox)
- The original Chatterbox (500M) has "emotion exaggeration control". — [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox)
- Multilingual V3 (500M) covers 23+ languages, including Japanese. — [chatterbox README](https://github.com/resemble-ai/chatterbox); [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox)
- The README example calls `model.generate(text)` without a reference clip, so a built-in default voice exists. The cached Turbo snapshot here contains `conds.pt`. — [chatterbox-turbo card](https://huggingface.co/ResembleAI/chatterbox-turbo); Local: `~/.cache/huggingface/hub/models--ResembleAI--chatterbox-turbo/snapshots/*/conds.pt`
- Earlier local tests found Turbo's mood tags weak: `[whispering]` produced no real whisper. — Local: `reports/3D horror Shorts animation and hooks.md` (line 55), citing `out/turbo_tags_research.md`

**CosyVoice 3**
- Covers 9 languages, including English and Japanese.
- "Supports various instructions such as languages, dialects, emotions, speed, volume".
- CosyVoice-300M-SFT / -Instruct models are also offered.
- — [CosyVoice README](https://github.com/FunAudioLLM/CosyVoice)

**Zonos**
- Trained on >200k hours.
- Clones from "a reference clip spanning just a few seconds", or takes a speaker embedding.
- Controls: speaking rate, pitch, max frequency, audio quality, and emotions "such as happiness, anger, sadness, and fear".
- — [Zonos README](https://github.com/Zyphra/Zonos); [Zonos-v0.1-transformer](https://huggingface.co/Zyphra/Zonos-v0.1-transformer)

**IndexTTS**
- IndexTTS-2.5, released 2026-08-10, supports Chinese, English, Japanese, Spanish and Arabic.
- Emotion control: a separate emotional reference audio, `emo_alpha` intensity, an 8-float emotion vector, emotion inferred from the script text (`use_emo_text`), or an explicit emotion description (`emo_text`).
- Duration control: `duration_factor` 0.5x–2.0x.
- It clones "from a single reference audio clip".
- — [index-tts README](https://github.com/index-tts/index-tts)

**Fish Drama 3 / S2-Pro**
- Inline tags such as `[whisper]`, `[angry]`, `[laughing]`, with multi-speaker generation and cloning. — [fish-speech README](https://github.com/fishaudio/fish-speech)
- S2-Pro reports Seed-TTS English WER 0.99%. — [fish-speech README](https://github.com/fishaudio/fish-speech)

**Licensed Japanese "anime-style" voice sources**
- Amitaro allows commercial use with credit. — [Amitaro voice rules](https://amitaro.net/voice/voice_rule/)
- JVNV corpus voices are CC BY-SA 4.0. — [JVNV corpus](https://sites.google.com/site/shinnosuketakamichi/research-topics/jvnv_corpus)
- The Tsukuyomi-chan corpus is described as a free character-voice material that permits commercial use, including building TTS from it. Secondary source; the credit terms were not verified. — [Niconico Pedia: つくよみちゃん](https://dic.nicovideo.jp/a/%E3%81%A4%E3%81%8F%E3%82%88%E3%81%BF%E3%81%A1%E3%82%83%E3%82%93); official terms at https://tyc.rei-yumesaki.net/ (not fetched)

### Inferences
- **English anime-style character voices on a commercial-safe licence:**
  - Chatterbox Turbo/Nano (tags) or original Chatterbox (exaggeration slider for shouty or excited delivery), with references that are synthetic. Examples: a Kokoro preset voice, pitch-shifted Kokoro audio, or an Amitaro or JVNV clip used under its terms.
  - Kokoro presets, with pitch/speed tweaks for kid or teen timbres.
  - The current repo already uses "Kokoro timbre fed into Turbo as reference" (`motion/voice.py` docstring), which keeps the chain free of real-person clones.
- **Japanese:** SBV2 with the JVNV and Amitaro voices is the most "anime-like" licensed option, but it carries attribution (and share-alike for JVNV). Kokoro's Japanese is low-grade.
- **Kokoro provenance caveat:** Kokoro's training data includes synthetic audio from closed commercial TTS providers. Some providers' terms forbid using their outputs to train competing models. That is a risk for Kokoro's trainer, not clearly for downstream users, but the provenance is not fully clean. (Interpretation.)

### Gaps
- No source states who or what the Chatterbox Turbo default `conds.pt` voice is (a hired voice actor, synthetic, or something else).
- No primary source was found for subjective English quality comparisons across all nine tools on anime-style delivery. The TTS Arena or a listening test would be needed.
- The Tsukuyomi-chan corpus credit and terms were not verified against the official page.

## A3. CPU inference speed (real numbers)

### Takeaway
Published **CPU** numbers are scarce.

Measured CPU numbers:
- GPT-SoVITS v2ProPlus: **RTF 0.526 on an Apple M4 CPU** (faster than real time).
- Chatterbox-Nano: **~3x faster than real time on 8 CPU cores**.
- chatterbox.cpp: Turbo at Q4_0 **RTF 0.82 on a Ryzen 9 9950X**.
- This container: Chatterbox Turbo in PyTorch takes **~40-60 s per sentence**.

GPU-only figures:
- Zonos: ~2x real time on RTX 4090.
- IndexTTS-2.5: RTF ~0.2 on RTX 4090.
- F5-TTS: RTF 0.147 offline PyTorch on L20.

Expectations without numbers:
- F5-TTS, Zonos, IndexTTS and Fish should be slow on CPU. Zonos says so explicitly.
- Kokoro is generally reported as about real time on CPU.

### Cited Findings
**GPT-SoVITS**
- "RTF(inference speed) of GPT-SoVITS v2 ProPlus: 0.028 tested in 4060Ti, 0.014 tested in 4090 … 0.526 in M4 CPU". — [GPT-SoVITS README](https://github.com/RVC-Boss/GPT-SoVITS)
- A CPU install option exists (`--device CPU`). — [GPT-SoVITS README](https://github.com/RVC-Boss/GPT-SoVITS)

**Chatterbox**
- "Chatterbox-Nano … 110M … targets on-device and CPU inference — running 3x faster than realtime on 8 CPU cores". — [chatterbox README](https://github.com/resemble-ai/chatterbox)
- Turbo distils the speech-token-to-mel decoder "from 10 steps to just one". — [chatterbox README](https://github.com/resemble-ai/chatterbox)
- Local measurement: Turbo takes "about 40-60 s per sentence in PyTorch on this CPU". — Local: `reports/3D horror Shorts animation and hooks.md` line 55
- chatterbox.cpp reports Turbo at Q4_0 "RTF 0.82 … on a Ryzen 9 9950X, 1.2x faster than ONNX Runtime". — [chatterbox.cpp](https://github.com/gianni-cor/chatterbox.cpp) (as cited in the local report; early-stage port)
- Official ONNX export with q4/q8 variants. — [chatterbox-turbo-ONNX](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX)

**Zonos**
- "real-time factor of ~2x on an RTX 4090". — [Zonos README](https://github.com/Zyphra/Zonos)
- "Zonos can also run on CPU provided there is enough free RAM. However, this will be a lot slower … and likely won't be sufficient for interactive use." — [Zonos README](https://github.com/Zyphra/Zonos)

**IndexTTS**
- RTF on RTX 4090 (kv_cache): 2.0 fp16 overall 0.3257; 2.5 bf16 0.2065; 2.5 fp32 0.2060.
- No CPU figures are given.
- — [index-tts README](https://github.com/index-tts/index-tts)

**F5-TTS**
- On a single L20 GPU at 16 NFE: RTF 0.0394 (Triton client-server) and 0.1467 (offline PyTorch). — [F5-TTS README](https://github.com/SWivid/F5-TTS)
- No CPU benchmark was found. — Secondary: [search across F5-TTS issues](https://github.com/SWivid/F5-TTS/issues/224)

**Fish Drama 3**
- Measured on NVIDIA H200 GPUs; 35B parameters with 3B active per token. — [fishaudio/drama-3](https://huggingface.co/fishaudio/drama-3)

**Kokoro**
- Community-reported RTF ≈1.1 on a mid-range x86 laptop (WASM, q8, 1 thread). — Secondary: [voicechanger.live browser TTS benchmarks](https://voicechanger.live/text-to-speech/benchmarks)
- RTF 0.58 via ONNX Runtime on an Android emulator. — Secondary: [soniqo Android benchmarks](https://soniqo.audio/benchmarks/android)
- No standard desktop-CPU benchmark was found.

**Style-Bert-VITS2**
- CPU inference is supported; training is not. — [Style-Bert-VITS2 README](https://github.com/litagin02/Style-Bert-VITS2)
- A Zenn write-up estimates ~5 GB RAM on CPU (vs ~2 GB on GPU). — Secondary: [Zenn kun432 scrap](https://zenn.dev/kun432/scraps/68321ea844075b)
- No timing numbers were found.

**Local attempt on this container** (4 vCPU Intel Xeon @ 2.10 GHz)
- Kokoro-82M (PyTorch, af_heart) gave RTF 3.3–14 across runs.
- The load average rose from about 8 to 12.9 during the runs because other jobs were sharing the 4 cores.
- **These figures are contaminated and should not be used.**
- — Local: scratchpad `kbench.py` run on 2026-10-27

### Inferences
- **For a CPU-only pipeline:** Kokoro (82M), Chatterbox-Nano (110M) and GPT-SoVITS v2ProPlus are the realistic real-time-ish options. Chatterbox Turbo is usable offline only via ONNX or a cpp quantized runtime, unless a slow render budget is acceptable.
- **SBV2** (a VITS-family model) is plausibly fast on CPU, but no number was found.
- **Not practical on a 4-core CPU:** F5, Zonos, IndexTTS, CosyVoice-0.5B and Fish models are LLM/flow-matching models published with GPU numbers only. Expect much slower than real time on 4 cores. (Unmeasured.)

### Gaps
- No clean CPU RTF for Kokoro, SBV2, CosyVoice 2/3, F5-TTS, Zonos or IndexTTS on an x86 desktop CPU.
- Measure these on an idle machine. The local Kokoro run was ruined by CPU contention.

## A4. Ethics and law: reference-audio consent, and using anime voice-actor clips

### Takeaway
Every licence or disclaimer that addresses it forbids cloning an identifiable person without consent: Fish's licence, IndexTTS's disclaimer and SBV2's requests. YouTube treats a realistic AI simulation of an identifiable person's voice as a privacy violation it can remove. Japanese voice actors are publicly campaigning against unauthorized AI models of their voices. **Clips of anime voice actors (from shows, games or dubs) must not be used as reference audio.** Use synthetic preset voices or explicitly licensed voice material (Amitaro, JVNV, Tsukuyomi-chan) under its terms.

### Cited Findings
- **Fish licence:** you may not use outputs to "generate speech that imitates the voice of an identifiable natural person without that person's prior consent (or, for a minor, the consent of a parent or legal guardian, and for a deceased person, the consent of the holder of the relevant rights)". Breach terminates the licence automatically. — [fish-speech LICENSE](https://github.com/fishaudio/fish-speech/blob/main/LICENSE)
- **IndexTTS disclaimer:** bans synthesizing political figures', public figures' or any unauthorized individual's voice, and infringing IP, portrait or privacy rights. — [index-tts DISCLAIMER](https://github.com/index-tts/index-tts/blob/main/DISCLAIMER)
- **IndexTTS licence:** the user bears sole responsibility for infringement of "personality rights, data-protection rights". — [index-tts LICENSE](https://github.com/index-tts/index-tts/blob/main/LICENSE)
- **SBV2 requests:** asks users not to use it for "なりすまし・ディープフェイク作成目的" (impersonation or deepfakes). — [SBV2 TERMS_OF_USE.md](https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md)
- **Amitaro:** forbids presenting generated audio as her voice or anyone else's. — [SBV2 TERMS_OF_USE.md](https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md)
- **NOMORE無断生成AI campaign:**
  - Launched by 26 well-known Japanese voice actors on 15 Oct 2024; members include Koichi Yamadera and Yuki Kaji.
  - It opposes AI voice models trained and distributed without the permission of actors or rights holders.
  - Ryusei Nakao said his voice was sold without his knowledge.
  - Sources differ on the exact launch date (15/16/21 Oct).
  - — [Automaton](https://automaton-media.com/en/nongaming-news/japans-top-voice-actors-band-together-to-fight-against-their-voices-being-used-to-train-ai-without-permission)
- **YouTube privacy guidelines:** list "Simulating audio to make it sound like a person is saying something they have not said" as a privacy issue. A person can request removal of content that "looks or sounds like you" when it is "a realistic altered or synthetic version of your likeness". — [YouTube privacy guidelines](https://support.google.com/youtube/answer/7671399)
- **Chatterbox:** watermarks all outputs (PerTh), which supports later provenance checks. — [chatterbox README](https://github.com/resemble-ai/chatterbox)

### Inferences
- **Do not use anime voice-actor clips** as zero-shot references or fine-tuning data (GPT-SoVITS 1-minute fine-tune, SBV2 training). That is the exact practice the NOMORE campaign targets. It would breach Fish's licence terms, and arguably IndexTTS's disclaimer. Any recognizable actor could file a YouTube privacy complaint.
- **Copyright exposure:** episode or game audio is copyrighted, so ripping it adds a separate copyright problem regardless of the voice question.
- **Safe reference sources:**
  1. Preset or synthetic voices: Kokoro presets, Chatterbox default `conds.pt`.
  2. Licensed free voice material, used with credit: Amitaro, JVNV CC BY-SA, Tsukuyomi-chan.
  3. A paid voice actor with a written release that covers AI cloning.
  4. The owner's own voice. The owner has refused this for this channel, per CLAUDE.md.
- **Record provenance:** keep a provenance log of every reference clip, with source, licence and consent.

### Gaps
- No statute-level legal sources were gathered: Japan's publicity-rights case law, the Tennessee ELVIS Act, the US NO FAKES Act status, or the EU AI Act transparency duties. They are flagged here as relevant but unresearched.
- No source was found that ties YouTube enforcement specifically to anime-character voice clones of Japanese actors.

## B1. YouTube "altered or synthetic content" disclosure: what triggers it, and does anime-style fiction need it?

### Takeaway
Disclosure is required for **realistic** content: making a real person appear to say or do something, altering real footage, generating a realistic scene that never happened, or AI music as the main focus. **Clearly non-realistic and animated content does not require disclosure.** The help page's own example is "an AI-generated or altered animation of a missile in a fully animated video". Disclosure does not by itself hurt reach or monetization. YouTube may still auto-label content that carries C2PA metadata, was made with YouTube's GenAI tools, or that its systems detect. For animated or non-photorealistic content, the label appears in the expanded description.

### Cited Findings
All from [YouTube Help: Disclosing use of altered or synthetic content](https://support.google.com/youtube/answer/14328491) (no revision date shown; "©2026 Google"; fetched 2026-10-27).
- Disclosure is needed for content that "Makes a real person appear to say or do something they didn't do", "Alters footage of a real event or place", "Generates a realistic scene that didn't actually occur", or "Creates music that's the main focus of the video".
- Not required, unrealistic: "Someone riding a unicorn through a fantastical world"; "Using an AI-generated or altered animation of a missile in a fully animated video"; also "Creators don't need to disclose non-realistic content that's made with AI".
- Not required, minor or production use:
  - "Production assistance, like using generative AI tools to create or improve a video outline, script, thumbnail, title, or infographic"
  - "Caption creation"
  - "Idea generation"
  - "Video sharpening, upscaling or repair and voice or audio repair"
  - "Cloning one's own voice to create voice overs or dubs"
- No bullet names synthetic or cloned voices of fictional characters as requiring disclosure.
- **Label placement:** labels "may appear in the expanded description for non-music AI-generated audio or AI content that is non-photorealistic or animated". Player labels apply to AI music or photorealistic AI content.
- **Auto-labelling:** YouTube may auto-apply a label for content made with "YouTube's GenAI tools", content with C2PA metadata, or content its systems detect. Labels on content made with YouTube's AI tools, content with C2PA, or content labelled after manual review "can not be adjusted".
- **Penalties:** failing to disclose "may be subject to manual application of a label, or penalties from YouTube, including removal of content". Also: "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money."

### Inferences
- An anime-style animated story with fictional characters and synthetic voices is "non-realistic" and generally needs **no** disclosure.
- Disclosure *would* be needed if a video:
  1. depicts or voices a real person (e.g. a real historical figure presented realistically), or
  2. uses photorealistic AI scenes presented as real events.
- **Low-cost safeguard:** tick "Yes" anyway whenever borderline. YouTube says disclosure alone doesn't affect reach or monetization, and the label for animated content sits only in the expanded description.

### Gaps
- No official statement was found on whether a *realistic-sounding* AI voice of a *fictional* character inside an animation triggers disclosure. The page's logic (not realistic, not a real person) suggests no, but this is interpretation.
- No dated changelog for the help page was found.

## B2. YouTube Partner Program "inauthentic content" (July 2025) and how it treats AI-assisted narrative series

### Takeaway
On **15 July 2025** YouTube renamed "repetitious content" to **"inauthentic content"** and clarified that it covers "repetitive or mass-produced" content. YouTube called this a minor clarification. Using AI tools is explicitly fine. What is not allowed:
- templated or mass-produced videos;
- "characters put in the same situation over and over again with the same outcome";
- "AI-generated content made with generic or unoriginal templates giving the impression of mass production".

A series that follows the same characters is allowed if each episode has "a distinct storyline". Enforcement is channel-wide. In 2026, YouTube's CEO made cutting "AI slop" a stated priority, and AI channels were removed, including an AI Dragon Ball-themed channel.

### Cited Findings
- July 15, 2025 notice: "repetitious content" is renamed and the policy now "clarify[ies] this includes content that is repetitive or mass-produced". The same notice says "There is no change to our reused content policy." — [YouTube channel monetization policies](https://support.google.com/youtube/answer/1311392)
- Not allowed:
  - "Videos where characters are put in the same situation over and over again with the same outcome"
  - "Image slideshows, templated storylines, or scrolling text with minimal or no narrative"
  - "AI-generated content made with generic or unoriginal templates giving the impression of mass production"

  — [YouTube channel monetization policies](https://support.google.com/youtube/answer/1311392)
- Allowed: "Same intro and outro for your videos, but the bulk of your content is different" and "Similar content, like a series following a set of characters across episodes". Each video should have "a distinct storyline, focus, or concept". Templates and automation are OK if "the final product must still demonstrate your creative vision". — [YouTube channel monetization policies](https://support.google.com/youtube/answer/1311392)
- TeamYouTube (Community Manager Carlos) called it "a minor update to our longstanding guideline on repetitious content". Using AI to enhance storytelling "will not affect channel monetization eligibility". — [PPC Land, 15 Jul 2025](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)
- Examples cited in coverage: "channels uploading multiple narrated stories with only superficial differences between videos" and "multiple slideshow presentations with identical narration". — [PPC Land, 15 Jul 2025](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)
- Enforcement is channel-level: "monetization may be removed from your entire channel". — [PPC Land, 15 Jul 2025](https://ppc.land/youtube-clarifies-inauthentic-content-policy-changes/)
- **2026 context:**
  - In his 21 Jan 2026 annual letter, CEO Neal Mohan named reducing "AI slop" a 2026 priority, building on anti-spam systems: "AI will remain a tool for expression, not a replacement." — [Variety AU](https://au.variety.com/2026/digital/news/youtube-channels-using-ai-tools-reduce-slop-neal-mohan-letter-32190/)
  - Tubefilter reported bans of slop channels. One example is an AI channel described as making "low-quality Dragon Ball-themed videos", with over 1.2B views. A Kapwing study found 278 of 15,000 trending channels were pure AI slop. — Secondary (search summary): [Tubefilter, 29 Jan 2026](https://tubefilter.com/2026/01/29/youtube-ai-slop-channel-crackdown-bans/)

### Inferences
- **Risk profile:** an AI-assisted anime story series is compatible with the policy if each episode has a distinct plot and outcome, scenes and shots vary, and human authorship is visible (owner-written lines, opinions, original story). This matches the channel's existing CLAUDE.md "rotate outcomes" rule.
- **Specific danger for anime-style AI channels:** templated look-alike episodes with the same structure, the same voice and the same outcome. Also, using existing franchise characters (e.g. Dragon Ball) adds both copyright risk and "slop" pattern-matching.
- **Status of the 2026 slop crackdown:** it is enforcement emphasis, not a new written rule. No new policy text was found beyond the July 2025 wording.

### Gaps
- No YouTube primary blog post text was fetched for the January 2026 letter. The quotes come via Variety and search summaries.
- No official statement was found that addresses AI voice narration specifically under inauthentic content.
- Reddit (r/NewTubers, r/youtubers) creator reports were not consulted.

## B3. YouTube policies on AI voices and likeness

### Takeaway
YouTube has no ban on AI or TTS voices. Its rules attach to **realistic simulations of identifiable people**: privacy removals since mid-2024, and likeness detection rolled out from late 2025 and opened to all creators aged 18+ in May 2026. Reported coverage says likeness detection does not yet cover voice. AI *music* as the main focus requires disclosure.

### Cited Findings
- **Privacy guidelines:** cover "Someone uses AI or other tools to alter or generate your voice or image without your permission". Factors YouTube weighs:
  - whether the content is altered or synthetic, and whether viewers are told it is;
  - whether the person can be uniquely identified, and whether the content is realistic;
  - whether it has "parody, satire, or other public interest value";
  - whether it shows a public figure in sensitive behaviour, such as crime, violence, or endorsing a product or political candidate.

  The uploader may be given time to trim or blur. — [YouTube privacy guidelines](https://support.google.com/youtube/answer/7671399)
- The AI-likeness privacy route was added quietly in June 2024 and publicized on 1 July 2024. — [TechCrunch, 1 Jul 2024](https://techcrunch.com/2024/07/01/youtube-now-lets-you-request-removal-of-ai-generated-content-that-simulates-your-face-or-voice)
- **Likeness detection:**
  - Announced as expanding to creators in Sept 2025. — [Axios, 16 Sep 2025](https://www.axios.com/2025/09/16/youtube-ai-likeness-detection-deepfakes)
  - Rolled out to YPP creators from Oct 2025. — Secondary: [Business Today, 22 Oct 2025](https://www.businesstoday.in/amp/technology/news/story/youtube-rolls-out-ai-likeness-detection-for-creators-to-combat-deepfakes-499101-2025-10-22)
  - Opened to all creators 18+ in May 2026; requires ID and selfie verification. One source says voice is not yet covered. — [PetaPixel, 18 May 2026](https://petapixel.com/2026/05/18/youtube-will-help-you-find-videos-featuring-your-ai-clone/); Secondary: [PPC Land](https://ppc.land/youtubes-ai-face-shield-now-covers-every-creator-18-and-over)
- Cloning one's own voice for voice-overs is listed as "minor" (no disclosure needed). — [YouTube Help 14328491](https://support.google.com/youtube/answer/14328491)

### Inferences
- **What this means for the channel:** using synthetic preset voices or licensed character voices for fictional anime characters creates no YouTube-policy issue. Cloning a real voice actor or celebrity does: privacy takedowns, plus licence breaches.

### Gaps
- No primary YouTube page for likeness detection was fetched. The "voice not yet covered" claim is secondary.

## B4. Licences of common anime image models, and what each allows for monetized video output

### Takeaway
**Safe for monetized video output:**
- SD1.5 derivatives (CreativeML OpenRAIL-M) and SDXL derivatives (OpenRAIL++-M). Both say "Licensor claims no rights in the Output" and impose only use-based restrictions.
- **Animagine XL 4.0 and 3.1.** Both now OpenRAIL++-M, with commercial use explicitly permitted.
- **Illustrious XL v1.0/v2.0.** SDXL licence / OpenRAIL-M tags.
- **Illustrious v0.1.** FAIPL-1.0-SD. Outputs are not restricted; the "monetization prohibition" applies to closed-source fine-tunes and merges.

**Do not use for monetized video:**
- **NoobAI-XL**, which adds an explicit ban on monetizing "model-generated products".

**Unclear:**
- **Pony Diffusion V6** (modified FAIPL). Bans monetized inference sites and asks commercial users to email PurpleSmart. It doesn't address selling outputs.

**Stability AI Community License** (SD3.5, SDXL Turbo, etc.): free commercial use under USD 1M annual revenue, with registration.

**Civitai permission icons** are binding addenda only for SD1.5/SDXL OpenRAIL models. Otherwise they are a statement of the creator's wishes, and the base licence still governs.

### Cited Findings
**CreativeML OpenRAIL-M (SD1.5)**
- "Licensor claims no rights in the Output You generate using the Model. You are accountable for the Output you generate and its subsequent uses. No use of the output can contravene any provision as stated in the License." — [CompVis stable-diffusion LICENSE](https://github.com/CompVis/stable-diffusion/blob/main/LICENSE)
- Derivatives must carry the Attachment A use-based restrictions. — [CompVis stable-diffusion LICENSE](https://github.com/CompVis/stable-diffusion/blob/main/LICENSE)

**CreativeML OpenRAIL++-M (SDXL)**
- Same output clause ("Licensor claims no rights in the Output"). — [SDXL LICENSE.md](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md)
- Attachment A bans include: harming minors, "verifiably false information … with the purpose of harming others", harmful PII, discrimination, and exploiting vulnerabilities. Downstream derivatives "will always have to include … the same use-based restrictions". — [SDXL LICENSE.md](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md)

**Fair AI Public License 1.0-SD**
- "The output of this software is not covered by this license, and no contributor claims any rights to it." — [FAIPL-1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
- Derived models must be distributed with source/weights under the same licence, including network access to a modified model. — [FAIPL-1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
- Prohibited Uses mirror the SD list, plus "To provide medical advice and medical results interpretation". — [FAIPL-1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
- The licence calls itself "not a free software license". — [FAIPL-1.0-SD](https://freedevproject.org/faipl-1.0-sd/)

**Animagine XL**
- 4.0: `license: openrail++`; "adopts the original CreativeML Open RAIL++-M License … without any modifications"; "✅ Permitted: Commercial use, modifications, distributions, private use". — [cagliostrolab/animagine-xl-4.0](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- 3.1: OpenRAIL++-M, commercial use permitted. "This license supersedes any previous community license tags (e.g., FAIPL) applied to earlier versions of this repository". — [cagliostrolab/animagine-xl-3.1](https://huggingface.co/cagliostrolab/animagine-xl-3.1)

**Illustrious XL**
- Early release v0.1: FAIPL-1.0-SD. — [OnomaAIResearch/Illustrious-xl-early-release-v0](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0)
- v0.1 on outputs: "We do not restrict any upload or spread of the generation results, as we do not own any rights regard to generated materials". — [Illustrious-xl-early-release-v0](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0)
- v0.1 "Monetization Prohibition": "You are prohibited from monetizing any close-sourced fine-tuned / merged model". — [Illustrious-xl-early-release-v0](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0)
- v1.0: `license_name: sdxl-license`, linking to the SDXL LICENSE.md. — [Illustrious-XL-v1.0](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.0)
- v2.0: `license: creativeml-openrail-m` (front-matter tag only). — [Illustrious-XL-v2.0](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0)

**NoobAI-XL 1.1**
- Licence: FAIPL-1.0-SD plus added terms. "II. Commercial Prohibition: We prohibit any form of commercialization, including but not limited to monetization or commercial use of the model, derivative models, or model-generated products." — [Laxhar/noobai-XL-1.1](https://huggingface.co/Laxhar/noobai-XL-1.1)
- It also requires open-sourcing derivatives and sharing prompts and workflows. — [Laxhar/noobai-XL-1.1](https://huggingface.co/Laxhar/noobai-XL-1.1)

**Pony Diffusion V6 XL** (Hugging Face mirror, not the original Civitai page)
- "licensed under a modified Fair AI Public License 1.0-SD". — Secondary/mirror: [Pony_Diffusion_V6_XL mirror](https://huggingface.co/gnicartweet/Pony_Diffusion_V6_XL)
- "You are not permitted to run inference of this model on websites or applications allowing any form of monetization". The restriction covers derivatives and merges. — Secondary/mirror: [Pony_Diffusion_V6_XL mirror](https://huggingface.co/gnicartweet/Pony_Diffusion_V6_XL)
- For commercial use, "reach us at contact@purplesmart.ai". "Explicit permission for commercial inference has been granted to CivitAi and Hugging Face." — Secondary/mirror: [Pony_Diffusion_V6_XL mirror](https://huggingface.co/gnicartweet/Pony_Diffusion_V6_XL)
- Original page (not fetched): [civitai.com/models/257749](https://civitai.com/models/257749)

**Stability AI Community License** (Last Updated July 5, 2024)
- Free use for those "generating annual revenue of less than US $1,000,000". — [Stability AI Community License](https://stability.ai/community-license-agreement)
- "If You are using or distributing the Stability AI Materials for a Commercial Purpose, You must register with Stability AI". — [Stability AI Community License](https://stability.ai/community-license-agreement)
- Above USD 1M, an Enterprise licence is needed. — [Stability AI Community License](https://stability.ai/community-license-agreement)
- "You own any outputs generated from the Models". — [Stability AI Community License](https://stability.ai/community-license-agreement); [SDXL-Turbo LICENSE.md](https://huggingface.co/stabilityai/sdxl-turbo/blob/main/LICENSE.md)
- The licence page lists SD 3.5 Suite, SDXL Turbo, Stable Audio 3.0 and Stable Fast 3D under Community. — [stability.ai/license](https://stability.ai/license)

**SDXL-Turbo and SD-Turbo**
- **SDXL-Turbo naming mismatch:** the front-matter tag reads `sai-nc-community`, but the LICENSE.md text is the Community License with a commercial section. — [stabilityai/sdxl-turbo](https://huggingface.co/stabilityai/sdxl-turbo)
- SD-Turbo's card says only "For commercial use, please refer to https://stability.ai/license", and calls the model "a research artifact". — [stabilityai/sd-turbo](https://huggingface.co/stabilityai/sd-turbo)

**Civitai permissions** (education page published Mar 7 2024, updated Oct 26 2026)
- Commercial options: "Sell generated images", "Use on Civitai generation service", "Use on other generation services", "Sell this model", "Sell merges using this model". Also "Use without crediting me", "Share merges", and "Use different permissions on merges". — [Civitai licensing guide](https://education.civitai.com/guide-to-licensing-options-on-civitai/)
- For SD 1.5 and SDXL 1.0 models, Civitai generates an addendum to the Open RAIL licence from these choices. For other base models, the permissions "work as a clear statement of what you want" and "the base model's own license still applies". — [Civitai licensing guide](https://education.civitai.com/guide-to-licensing-options-on-civitai/)

### Inferences
- **Usable for monetized YouTube video output:** Animagine XL 4.0/3.1, Illustrious XL v0.1/v1.0/v2.0, SD1.5 and SDXL fine-tunes under OpenRAIL. Check each Civitai fine-tune's "Sell generated images" box, since for SDXL/SD1.5 bases it becomes a licence addendum. Stability Community models are also usable while under USD 1M revenue, after registering.
- **Avoid for monetized output:** NoobAI-XL and anything merged from it. Its added "commercial prohibition" on "model-generated products" conflicts with FAIPL's own "output … not covered" clause. Which clause wins is legally uncertain, so the conservative choice is to avoid it.
- **Pony V6:** treat output use as unclear and get written permission. Many popular anime checkpoints are NoobAI- or Pony-based merges, so check each merge's lineage.
- **All licences:** none of them clear *third-party IP in outputs*. Generating recognizable franchise characters (e.g. Danbooru-tagged characters) is a copyright and trademark risk, separate from the model licence. Use original characters only.

### Gaps
- The original Civitai Pony V6 page and the Pony V7 licence were not fetched.
- No court decision or authoritative guidance was found on how NoobAI's added terms interact with FAIPL's output clause.
- I didn't check whether SD-Turbo specifically is covered by the Community License or remains non-commercial. The model card points to stability.ai/license, whose snippet named only SDXL Turbo.
