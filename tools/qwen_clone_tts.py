"""Speak lines in the owner's cloned voice with Qwen3-TTS (Base model, voice clone; one of the engines Voicebox uses).
Runs in its own virtualenv (~/.venv-qwen: torch CPU + qwen-tts).

  ~/.venv-qwen/bin/python tools/qwen_clone_tts.py jobs.json [--model Qwen/Qwen3-TTS-12Hz-0.6B-Base]
  jobs.json: [["text", "out.wav"], ...]

Only the owner's own voice is cloned (assets/voice/owner_prompt.wav and its transcript).
"""
import argparse
import json
import os
import time

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = os.path.join(ROOT, "assets", "voice", "owner_prompt.wav")
PROMPT_TEXT = ("Look, if your desk is a total mess right now, you need to watch this. I had pens, tools, literally "
               "everywhere, totally killing my focus. I needed an organizer, but standard pen stands are na")

ap = argparse.ArgumentParser()
ap.add_argument("jobs")
ap.add_argument("--model", default="Qwen/Qwen3-TTS-12Hz-0.6B-Base")
a = ap.parse_args()
torch.set_num_threads(os.cpu_count() or 4)
model = Qwen3TTSModel.from_pretrained(a.model, device_map="cpu", dtype=torch.float32)
prompt = model.create_voice_clone_prompt(ref_audio=PROMPT, ref_text=PROMPT_TEXT)
for text, out in json.load(open(a.jobs)):
    if os.path.exists(out):
        continue
    t = time.time()
    wavs, sr = model.generate_voice_clone(text=text, language="English", voice_clone_prompt=prompt)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sf.write(out, wavs[0], sr)
    print(f"{time.time() - t:5.1f}s  {text}", flush=True)
