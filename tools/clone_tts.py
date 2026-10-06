"""Speak sentences in the channel owner's own cloned voice (Chatterbox, MIT licence). Runs in the separate clone
virtualenv (torch); motion/voice.py calls it once per render with every sentence that isn't cached yet.

  /home/user/.venv-clone/bin/python tools/clone_tts.py jobs.json
  jobs.json: [["text", "out.wav"], ...]   ->   24 kHz mono wavs, start/end silence trimmed gently

Chatterbox's Perth watermark is left in place.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The owner's clip sped up x1.2: the clone copies the prompt's pace, and this lands it near Teacher Bluffed's
# 5.2 syllables/s instead of ~3.2 (tested: 4.9 median, clearer and more even than the plain prompt).
PROMPT = os.path.join(ROOT, "assets", "voice", "owner_prompt_fast.wav")
EXAGGERATION, CFG = 0.6, 0.6     # cfg 0.6 follows the text more closely: better pronunciation


def trim(w, sr):
    """Gentle trim: keeps soft first consonants ("Put" was clipped to "could" by a harder trim)."""
    env = np.convolve(np.abs(w), np.ones(int(sr * 0.01)) / (sr * 0.01), mode="same")
    loud = np.nonzero(env > 0.004)[0]
    if not len(loud):
        return w
    return w[max(0, loud[0] - int(0.09 * sr)): loud[-1] + int(0.06 * sr)]


def main():
    jobs = json.load(open(sys.argv[1]))
    model = ChatterboxTTS.from_pretrained(device="cpu")
    model.prepare_conditionals(PROMPT, exaggeration=EXAGGERATION)
    for k, (text, out) in enumerate(jobs, 1):
        w = model.generate(text, exaggeration=EXAGGERATION, cfg_weight=CFG)[0].numpy()
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sf.write(out + ".tmp.wav", trim(w, model.sr), model.sr)
        os.replace(out + ".tmp.wav", out)
        print(f"clone voice {k}/{len(jobs)}: {text}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
