"""Speak sentences with Orpheus TTS (Canopy Labs, Apache-2.0; stock voices trained on licensed speakers, nobody is
cloned). Runs in its own virtualenv (llama.cpp + SNAC); motion/voice.py calls it with every missing take.

  /home/user/.venv-orpheus/bin/python tools/orpheus_tts.py jobs.json      (ORPHEUS_VOICE=leo)
  jobs.json: [["text", "out.wav"], ...]  ->  24 kHz mono wavs, start/end silence trimmed gently
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

import llama_cpp

_Llama = llama_cpp.Llama


class _Llama8k(_Llama):          # orpheus-cpp asks for the model's full context (131k): far too much memory on CPU
    def __init__(self, *a, **k):
        k["n_ctx"] = 8192
        super().__init__(*a, **k)


llama_cpp.Llama = _Llama8k
from orpheus_cpp import OrpheusCpp  # noqa: E402

# Orpheus's defaults (temperature 0.8, no repetition penalty) let it improvise words ("Doctors take" -> "The doctor
# takes", 25 Oct 2026). Lower temperature + a repetition penalty (the Orpheus authors recommend >= 1.1) keep it on
# the script; Whisper medium still checks every take.
TEMPERATURE, TOP_P, REPEAT_PENALTY = 0.45, 0.9, 1.1


def _token_gen(self, text, options=None):
    options = options or {}
    prompt = f"<|audio|>{options.get('voice_id', 'leo')}: {text}<|eot_id|><custom_token_4>"
    for token in self._llm(prompt, max_tokens=2048, stream=True, temperature=TEMPERATURE, top_p=TOP_P, top_k=40,
                           min_p=0.05, repeat_penalty=REPEAT_PENALTY):
        yield token["choices"][0]["text"]


OrpheusCpp._token_gen = _token_gen


def _tts_whole(self, text, options=None):
    """All of a line's audio tokens decoded in one SNAC pass. orpheus-cpp's streaming decoder slides a 4-frame window
    and keeps only one frame of each, so a line's first two frames (~0.17 s) were never output: first words got
    clipped ("Experts estimate" heard as "Estimate", "Others lose" as "Blue's"; found 25 Oct 2026)."""
    tokens = []
    for tt in self._token_gen(text, options):
        tid = self._token_to_id(tt, len(tokens))
        if tid is not None and tid > 0:
            tokens.append(tid)
    frames = [tokens[i:i + 7] for i in range(0, len(tokens) // 7 * 7, 7)]
    frames = [f for f in frames if all(0 <= x <= 4096 for x in f)]
    c0 = np.array([[f[0] for f in frames]], dtype=np.int64)
    c1 = np.array([[x for f in frames for x in (f[1], f[4])]], dtype=np.int64)
    c2 = np.array([[x for f in frames for x in (f[2], f[3], f[5], f[6])]], dtype=np.int64)
    names = [x.name for x in self._snac_session.get_inputs()]
    audio = self._snac_session.run(None, dict(zip(names, [c0, c1, c2])))[0]
    return 24_000, audio.reshape(-1).astype(np.float32)


OrpheusCpp.tts = _tts_whole
# the default Q4_K_M model is muddy on some words ("Malaria" heard as "Valeria"); ORPHEUS_REPO picks another quant
OrpheusCpp.lang_to_model = dict(OrpheusCpp.lang_to_model, en=os.environ.get("ORPHEUS_REPO", OrpheusCpp.lang_to_model["en"]))


def trim(w, sr):
    env = np.convolve(np.abs(w), np.ones(int(sr * 0.01)) / (sr * 0.01), mode="same")
    loud = np.nonzero(env > 0.004)[0]
    if not len(loud):
        return w
    return w[max(0, loud[0] - int(0.09 * sr)): loud[-1] + int(0.08 * sr)]


def main():
    jobs = json.load(open(sys.argv[1]))
    voice = os.environ.get("ORPHEUS_VOICE", "leo")
    model = OrpheusCpp(verbose=False, lang="en", n_threads=os.cpu_count() or 4)
    for k, (text, out, *_) in enumerate(jobs, 1):
        sr, s = model.tts(text, options={"voice_id": voice})
        a = np.asarray(s).squeeze().astype(np.float32)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sf.write(out + ".tmp.wav", trim(a, sr), sr)
        os.replace(out + ".tmp.wav", out)
        print(f"orpheus voice {k}/{len(jobs)}: {text}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
