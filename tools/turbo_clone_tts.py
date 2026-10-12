"""Speak lines in the owner's cloned voice with Chatterbox Turbo (one of the engines Voicebox uses).
Runs in the clone virtualenv. Chatterbox's Perth watermark is left in place.

  ~/.venv-clone/bin/python tools/turbo_clone_tts.py jobs.json [--prompt assets/voice/owner_prompt.wav]
  jobs.json: [["text", "out.wav"], ...]
"""
import argparse
import json
import os
import time

import soundfile as sf
from chatterbox.tts_turbo import ChatterboxTurboTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("jobs")
ap.add_argument("--prompt", default=os.path.join(ROOT, "assets", "voice", "owner_prompt.wav"))
a = ap.parse_args()
model = ChatterboxTurboTTS.from_pretrained(device="cpu")
model.prepare_conditionals(a.prompt)
for text, out in json.load(open(a.jobs)):
    if os.path.exists(out):
        continue
    t = time.time()
    w = model.generate(text)[0].numpy()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sf.write(out, w, model.sr)
    print(f"{time.time() - t:5.1f}s  {text}", flush=True)
