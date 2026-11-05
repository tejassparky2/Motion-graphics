"""Liveliness retakes (copied from channels/hinglish/lively_retake.py, now per language). On the Hinglish channel the
lines heard as robotic measured flat (pitch SD 3.7-4.1 semitones) against 5.1-5.3 for the lines heard as better.
Every line under MIN_SD gets EXTRA more takes; the take kept is the liveliest (highest pitch SD) among those that stay
clear (WER no worse than the line's current take + 10 points) and stay the same voice (similarity >= MIN_SIM).
The Kannada threshold is a starting guess until the owner has heard the Kannada narrator in a real video.

Usage: python -I -X utf8 channels/mythology/lively_retake.py <video> <hi|kn> [--also b14 ...]
(--also: only these lines, re-taken even if not flat, e.g. a line the owner heard as robotic)"""
import importlib.util, json, os, shutil, sys
import numpy as np, librosa
from resemblyzer import VoiceEncoder, preprocess_wav

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from asr import whisper  # noqa: E402
from channel import NARRATORS, WHISPER_LANG  # noqa: E402
from render_myth import wer, words  # noqa: E402

MIN_SD, MIN_SIM, EXTRA = {"hi": 4.5, "kn": 4.5}, 0.85, [3, 4, 5]


def main():
    name, lang = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cfg = getattr(mod, "NARRATORS", NARRATORS)[lang]
    model = whisper()
    enc = VoiceEncoder(verbose=False)
    ref_emb = enc.embed_utterance(preprocess_wav(cfg["ref_audio"]))

    def score(path, text):
        y, _ = librosa.load(path, sr=16000)
        y, _ = librosa.effects.trim(y, top_db=35)
        f0, v, _ = librosa.pyin(y, fmin=65, fmax=450, sr=16000)
        f0 = f0[v]
        sd = float((12 * np.log2(f0 / np.median(f0))).std())
        heard = " ".join(s.text for s in model.transcribe(y, language=WHISPER_LANG[lang], beam_size=5)[0])
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), ref_emb))
        return sd, wer(words(text), words(heard)), sim

    also = set(sys.argv[sys.argv.index("--also") + 1:]) if "--also" in sys.argv else set()
    flat = []
    for l in mod.SCRIPTS[lang]:
        if also and l["id"] not in also:
            continue
        sd, w, s = score(narrate._raw_path(l["text"], cfg), l["text"])
        if sd < MIN_SD[lang] or l["id"] in also:
            flat.append((l, sd, w, s))
            print(f"{l['id']:>4} flat: SD {sd:.1f} st, WER {w:.0%}", flush=True)
    variant = lambda k: {**cfg, "take": k}
    jobs = [(l["text"], narrate._raw_path(l["text"], variant(k))) for l, *_ in flat for k in EXTRA
            if not os.path.exists(narrate._raw_path(l["text"], variant(k)))]
    if jobs:
        narrate.BATCH[cfg["engine"]](jobs, cfg)          # IndicF5: each run samples a fresh reading
    log = {}
    for l, sd0, w0, s0 in flat:
        cands = [(sd0, w0, s0, None)]
        for k in EXTRA:
            sd, w, s = score(narrate._raw_path(l["text"], variant(k)), l["text"])
            print(f"{l['id']:>4} take {k}: SD {sd:.1f} st, WER {w:.0%}, sim {s:.2f}", flush=True)
            if s >= MIN_SIM and w <= w0 + 0.10:
                cands.append((sd, w, s, k))
        sd, w, s, k = max(cands, key=lambda c: c[0])
        if k is not None:
            shutil.copyfile(narrate._raw_path(l["text"], variant(k)), narrate._raw_path(l["text"], cfg))
            h = narrate._hash(l["text"], cfg)
            for ext in (".wav", ".json"):
                p = os.path.join(narrate.CACHE, h + ext)
                if os.path.exists(p):
                    os.remove(p)
        log[l["id"]] = dict(take=k, sd=sd, was_sd=sd0, wer=w, was_wer=w0, sim=s)
        print(f"  -> {l['id']}: pitch SD {sd0:.1f} -> {sd:.1f} st, WER {w0:.0%} -> {w:.0%}", flush=True)
    out = os.path.join(narrate.ROOT, "build", "mythology", f"{name}_{lang}_lively.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    old = json.load(open(out)) if os.path.exists(out) else {}
    json.dump({**old, **log}, open(out, "w"), indent=1)


main()
