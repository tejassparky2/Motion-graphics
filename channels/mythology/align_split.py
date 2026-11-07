"""Find where each line starts inside a take that reads several lines in one go (narrate.split_take uses it).

Whisper large-v3-turbo transcribes the take with word times; its letters are aligned to the script's letters
(edit-distance backtrace), and each line boundary is the midpoint between the time the last letter of one line was
heard and the first letter of the next. Runs in the IndicF5 venv (it has transformers). JSON on stdin:
  {"lang": "kannada", "groups": [{"wav": path, "texts": [line, ...]}, ...]}
prints JSON: [[boundary seconds, ...] or null, ...] (one list per group, len(texts) - 1 times each)."""
import json, sys

import librosa
import numpy as np
import torch
from transformers import pipeline


def letters(s):
    return [c for c in s if "ಀ" <= c <= "೿" or "ऀ" <= c <= "ॿ" or c.isdigit()]


def align(ref, hyp):
    """Map each ref index to a hyp index (or -1) by edit distance."""
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (ref[i - 1] != hyp[j - 1]))
    out, i, j = [-1] * n, n, m
    while i > 0 and j > 0:
        if d[i, j] == d[i - 1, j - 1] + (ref[i - 1] != hyp[j - 1]):
            out[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif d[i, j] == d[i - 1, j] + 1:
            i -= 1
        else:
            j -= 1
    return out


spec = json.loads(sys.stdin.read())
gpu = torch.cuda.is_available()
asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device="cuda" if gpu else "cpu",
               torch_dtype=torch.float16 if gpu else torch.float32)
result = []
for g in spec["groups"]:
    try:
        y, _ = librosa.load(g["wav"], sr=16000)
        dur = len(y) / 16000
        ref, owner = [], []
        for n, t in enumerate(g["texts"]):
            ls = letters(t)
            ref += ls
            owner += [n] * len(ls)

        def heard(**chunking):
            out = asr({"raw": y, "sampling_rate": 16000}, return_timestamps="word", **chunking,
                      generate_kwargs={"language": spec.get("lang", "kannada"), "task": "transcribe"})
            hyp, times = [], []
            for c in out["chunks"]:
                s, e = c["timestamp"]
                s = s if s is not None else (times[-1][1] if times else 0.0)
                e = e if e is not None else min(dur, s + 0.4)
                if s >= dur - 0.05:                 # words "heard" after the end are Whisper looping
                    continue
                ls = letters(c["text"])
                for k, ch in enumerate(ls):
                    hyp.append(ch)
                    times.append((s + (e - s) * k / len(ls), s + (e - s) * (k + 1) / len(ls)))
            return hyp, times

        # Whisper sometimes skips the opening sentence of a long take (7 Nov 2026: Jarasandha j13, 8 s dropped);
        # overlapping 10 s windows hear all of it, so retry that way when far fewer letters come back than expected
        hyp, times = heard()
        if len(hyp) < 0.8 * len(ref) or len(hyp) > 1.3 * len(ref):
            hyp, times = heard(chunk_length_s=10, stride_length_s=2)
        amap = align(ref, hyp)
        cuts = []
        for k in range(len(g["texts"]) - 1):
            last = max(i for i, o in enumerate(owner) if o == k)
            first = last + 1
            a = next((amap[i] for i in range(last, -1, -1) if amap[i] >= 0 and owner[i] == k), None)
            b = next((amap[i] for i in range(first, len(ref)) if amap[i] >= 0 and owner[i] == k + 1), None)
            if a is None or b is None or b <= a:
                cuts = None
                break
            cuts.append((times[a][1] + times[b][0]) / 2)
        result.append(cuts)
    except Exception as ex:                       # noqa: BLE001
        print(f"align failed for {g['wav']}: {ex}", file=sys.stderr)
        result.append(None)
print(json.dumps(result))
