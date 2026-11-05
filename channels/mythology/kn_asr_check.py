"""Second opinion on Kannada clarity with Whisper large-v3-turbo (already in the Hugging Face cache), on the CPU so it
never competes with the GPU jobs. Whisper medium is weak in Kannada; turbo is noticeably better, so a line that turbo
also garbles is worth a retake or a reword. Prints the character error rate per line.
Runs in the IndicF5 venv (it has transformers):
  tools/.venv-f5/Scripts/python -I -X utf8 channels/mythology/kn_asr_check.py <timeline.json> [<timeline.json> ...]"""
import json, sys
import numpy as np, soundfile as sf
import torch
from transformers import pipeline


def kn(s):
    return [c for c in s if "ಀ" <= c <= "೿"]


def cer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / max(1, len(ref))


asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device="cpu",
               torch_dtype=torch.float32)
for path in sys.argv[1:]:
    tl = json.load(open(path, encoding="utf-8"))
    print(f"== {path}", flush=True)
    for b in tl["beats"]:
        a, sr = sf.read(b["wav"], dtype="float32")
        if a.ndim > 1:
            a = a.mean(1)
        if sr != 16000:
            import librosa
            a = librosa.resample(a, orig_sr=sr, target_sr=16000)
        heard = asr({"raw": a, "sampling_rate": 16000},
                    generate_kwargs={"language": "kannada", "task": "transcribe"})["text"].strip()
        c = cer(kn(b["text"]), kn(heard))
        print(f"{'!!' if c > 0.45 else 'ok'} {b['id']:>5} CER {c:4.0%}  {heard}", flush=True)
