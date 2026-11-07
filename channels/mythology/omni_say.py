"""Voice text with OmniVoice (k2-fsa, Apache-2.0, 2026; owner, 7 Nov 2026: "And try omni voice because it is latest")
from a consented reference clip. Runs in tools/.venv-omni; JSON job on stdin:
  {"ref_audio": wav, "ref_text": its words, "num_step": 32, "speed": 1.0, "jobs": [{"text": ..., "out": wav}, ...]}
The model loads once per batch. Output is 24 kHz float WAV."""
import inspect, json, os, sys

import soundfile as sf
import torch
from omnivoice import OmniVoice

spec = json.loads(sys.stdin.read())
dev = "cuda:0" if torch.cuda.is_available() else "cpu"
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map=dev,
                                  dtype=torch.float16 if dev != "cpu" else torch.float32)
if spec.get("show_signature"):
    print("generate", inspect.signature(model.generate), flush=True)
for job in spec["jobs"]:
    kw = dict(text=job["text"], ref_audio=spec["ref_audio"], ref_text=spec["ref_text"],
              num_step=spec.get("num_step", 32), speed=spec.get("speed", 1.0))
    if spec.get("language"):
        kw["language"] = spec["language"]
    audio = model.generate(**kw)
    sf.write(job["out"], audio[0], 24000)
    print("voiced", os.path.basename(job["out"]), f"{len(audio[0]) / 24000:.1f} s", flush=True)
