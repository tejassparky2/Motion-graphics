"""Batch voicing with AI4Bharat IndicF5 (MIT), using the channel's OWN designed voice as the reference prompt (IndicF5
terms: clone only voices you have permission for; this reference is our synthetic voice, made from a text
description). Runs in tools/.venv-f5; narrate.py sends a JSON job on stdin:
  {"ref_audio": wav, "ref_text": its transcript, "jobs": [{"text": ..., "out": wav}, ...]}
The model loads once per batch. Output is 24 kHz float WAV."""
import json, os, sys
import numpy as np, soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narrate import _key  # noqa: E402

spec = json.loads(sys.stdin.read())
os.environ.setdefault("HF_TOKEN", _key("HF_TOKEN") or "")

import torch, torchaudio  # noqa: E402


def _load(path, *args, **kwargs):
    """torchaudio >= 2.9 reads files through torchcodec, which needs extra native FFmpeg libraries on Windows;
    the reference prompt is a plain WAV, so soundfile reads it directly (same tensor layout: channels x samples)."""
    data, sr = sf.read(path, dtype="float32", always_2d=True)
    return torch.from_numpy(data.T.copy()), sr


torchaudio.load = _load
from transformers import AutoModel  # noqa: E402

model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True, token=os.environ["HF_TOKEN"] or None)
try:
    import torch
    if torch.cuda.is_available():
        model = model.to("cuda")
except Exception:
    pass
for job in spec["jobs"]:
    audio = model(job["text"], ref_audio_path=spec["ref_audio"], ref_text=spec["ref_text"])
    audio = np.asarray(audio)
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    sf.write(job["out"], audio.astype(np.float32), samplerate=24000)
    print("voiced", os.path.basename(job["out"]), flush=True)
