"""Re-voice one line until it is clear: N IndicF5 takes, each heard by Whisper large-v3-turbo (CPU, in the IndicF5
venv), the take with the lowest character error becomes the line's take (6 Nov 2026: the Hindi hook "एक आँख..."
came out mumbled in all three takes; Whisper medium is too weak to judge Kannada).
Usage: python -I -X utf8 channels/mythology/fix_line.py <video> <lang> <line id> [--takes 4]"""
import importlib.util, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from channel import NARRATORS, ROOT  # noqa: E402

F5_PY = os.path.join(ROOT, "tools", ".venv-f5", "Scripts", "python.exe")
SCORER = r'''
import json, sys, torch, soundfile as sf, librosa
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device="cpu",
               torch_dtype=torch.float32)
job = json.load(open(sys.argv[1], encoding="utf-8"))
def letters(s):
    return [c for c in s if "ऀ" <= c <= "ॿ" or "ಀ" <= c <= "೿"]
def cer(r, h):
    d = list(range(len(h) + 1))
    for i, x in enumerate(r, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(h, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1] / max(1, len(r))
out = []
for path in job["files"]:
    a, sr = sf.read(path, dtype="float32")
    a = a.mean(1) if a.ndim > 1 else a
    a = librosa.resample(a, orig_sr=sr, target_sr=16000) if sr != 16000 else a
    heard = asr({"raw": a, "sampling_rate": 16000},
                generate_kwargs={"language": job["lang"], "task": "transcribe"})["text"].strip()
    out.append([cer(letters(job["text"]), letters(heard)), heard])
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
'''


def main():
    name, lang, bid = sys.argv[1:4]
    n = int(sys.argv[sys.argv.index("--takes") + 1]) if "--takes" in sys.argv else 4
    spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    text = next(l["text"] for l in mod.SCRIPTS[lang] if l["id"] == bid)
    cfg = NARRATORS[lang]
    variant = lambda k: {**cfg, "take": k} if k else cfg
    takes = list(range(10, 10 + n))                        # fresh take numbers, never reused before
    jobs = [(text, narrate._raw_path(text, variant(k))) for k in takes
            if not os.path.exists(narrate._raw_path(text, variant(k)))]
    if jobs:
        narrate.BATCH[cfg["engine"]](jobs, cfg)
    files = [narrate._raw_path(text, variant(k)) for k in takes]
    base = narrate._raw_path(text, cfg)
    if os.path.exists(base):
        files.append(base)
        takes.append(0)
    tmp = os.path.join(narrate.CACHE, f"fix_{name}_{lang}_{bid}")
    json.dump({"files": files, "text": text, "lang": {"hi": "hindi", "kn": "kannada"}[lang]},
              open(tmp + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    open(tmp + "_scorer.py", "w", encoding="utf-8").write(SCORER)
    subprocess.run([F5_PY, "-I", "-X", "utf8", tmp + "_scorer.py", tmp + ".json", tmp + "_out.json"], check=True,
                   capture_output=True)
    scores = json.load(open(tmp + "_out.json", encoding="utf-8"))
    for k, (c, heard) in zip(takes, scores):
        print(f"{bid} take {k}: CER {c:4.0%}  {heard}", flush=True)
    best = min(range(len(takes)), key=lambda i: scores[i][0])
    if takes[best] != 0:
        shutil.copyfile(files[best], base)
        h = narrate._hash(text, cfg)
        for ext in (".wav", ".json"):
            p = os.path.join(narrate.CACHE, h + ext)
            if os.path.exists(p):
                os.remove(p)
    print(f"-> {bid}: take {takes[best]}, CER {scores[best][0]:.0%}", flush=True)


main()
