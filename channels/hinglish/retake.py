"""Retakes for the designed (Parler) voice: every line whose take Whisper medium hears with more than MAX_WER word
error gets extra takes with other seeds; the clearest take that still sounds like the channel voice (speaker
similarity >= MIN_SIM to the reference sample) becomes the line's take. Choices are logged in
build/hinglish/<video>_retakes.json.

Usage: python -I -X utf8 channels/hinglish/retake.py <video> [--all]
"""
import importlib.util, json, os, re, shutil, sys
import numpy as np, librosa
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402

MAX_WER, MIN_SIM = 0.30, 0.85
EXTRA_SEEDS = [101, 202, 303]
VOICE_REF = os.path.join(os.path.dirname(narrate.ROOT), "mayank", "voice", "designed", "Rohit_midhigh_calm_s3.wav")


def words(s):
    return re.findall(r"[\wऀ-ॿ]+", s.replace("़", ""))


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / max(1, len(ref))


def main():
    name = sys.argv[1]
    spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cfg = mod.NARRATOR
    narrate.prefetch(mod.SCRIPT, cfg)                     # make sure every default take exists
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    enc = VoiceEncoder(verbose=False)
    ref_emb = enc.embed_utterance(preprocess_wav(VOICE_REF))
    log_path = os.path.join(narrate.ROOT, "build", "hinglish", f"{name}_retakes.json")
    log = json.load(open(log_path, encoding="utf-8")) if os.path.exists(log_path) else {}

    def score(path, text):
        a, _ = narrate._trim(narrate._decode(open(path, "rb").read()))
        y = librosa.resample(a.astype(np.float32), orig_sr=narrate.SR, target_sr=16000)
        heard = " ".join(s.text for s in model.transcribe(y, language="hi", beam_size=5)[0])
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), ref_emb))
        return wer(words(text), words(heard)), sim, heard.strip()

    todo = []
    for line in mod.SCRIPT:
        if line["id"] in log and log[line["id"]].get("text") == line["text"]:
            continue                                       # already decided for this exact text
        w, s, heard = score(narrate._raw_path(line["text"], cfg), line["text"])
        print(f"{line['id']:>4} take s{cfg['seed']}: WER {w:4.0%} sim {s:.2f}", flush=True)
        if w > MAX_WER or "--all" in sys.argv:
            todo.append((line, w, s))
        else:
            log[line["id"]] = dict(text=line["text"], seed=cfg["seed"], wer=w, sim=s)
    jobs = [(l["text"], narrate._raw_path(l["text"], {**cfg, "seed": sd})) for l, _, _ in todo for sd in EXTRA_SEEDS
            if not os.path.exists(narrate._raw_path(l["text"], {**cfg, "seed": sd}))]
    for sd in EXTRA_SEEDS:                                 # one batch per seed: parler_say uses one seed per batch
        batch = [(t, p) for t, p in jobs if p.endswith(".wav") and p == narrate._raw_path(t, {**cfg, "seed": sd})]
        if batch:
            narrate._parler_batch(batch, {**cfg, "seed": sd})
    for line, w0, s0 in todo:
        cands = [(w0, -s0, cfg["seed"], s0)]
        for sd in EXTRA_SEEDS:
            w, s, heard = score(narrate._raw_path(line["text"], {**cfg, "seed": sd}), line["text"])
            print(f"{line['id']:>4} take s{sd}: WER {w:4.0%} sim {s:.2f}  {heard[:70]}", flush=True)
            if s >= MIN_SIM:
                cands.append((w, -s, sd, s))
        w, _, sd, s = min(cands)
        if sd != cfg["seed"]:                              # the chosen take becomes the line's take
            shutil.copyfile(narrate._raw_path(line["text"], {**cfg, "seed": sd}), narrate._raw_path(line["text"], cfg))
            h = narrate._hash(line["text"], cfg)
            for ext in (".wav", ".json"):
                p = os.path.join(narrate.CACHE, h + ext)
                if os.path.exists(p):
                    os.remove(p)                           # re-process from the new raw take
        log[line["id"]] = dict(text=line["text"], seed=sd, wer=w, sim=s, was_wer=w0)
        print(f"  -> {line['id']}: seed {sd}, WER {w0:.0%} -> {w:.0%}", flush=True)
    json.dump(log, open(log_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
