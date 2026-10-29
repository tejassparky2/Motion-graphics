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
    ref_emb = enc.embed_utterance(preprocess_wav(getattr(mod, "VOICE_REF", VOICE_REF)))   # the video's own voice
    voice = narrate._hash("", {k: v for k, v in cfg.items()
                               if k not in ("studio", "pace_wps", "pitch_expand", "tempo", "take")})
    log_path = os.path.join(narrate.ROOT, "build", "hinglish", f"{name}_retakes_{voice}.json")   # one log per voice
    log = json.load(open(log_path, encoding="utf-8")) if os.path.exists(log_path) else {}

    def score(path, text):
        a, _ = narrate._trim(narrate._decode(open(path, "rb").read()))
        y = librosa.resample(a.astype(np.float32), orig_sr=narrate.SR, target_sr=16000)
        heard = " ".join(s.text for s in model.transcribe(y, language="hi", beam_size=5)[0])
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), ref_emb))
        return wer(words(text), words(heard)), sim, heard.strip()

    # Parler varies a take by its seed; IndicF5 samples fresh noise each run, so a "take" number just names a new run
    key, extra = ("seed", EXTRA_SEEDS) if cfg["engine"] == "parler" else ("take", [1, 2])
    base = cfg.get(key, 0)
    variant = lambda v: {**cfg, key: v}
    todo = []
    for line in mod.SCRIPT:
        if line["id"] in log and log[line["id"]].get("text") == line["text"]:
            continue                                       # already decided for this exact text
        w, s, heard = score(narrate._raw_path(line["text"], cfg), line["text"])
        print(f"{line['id']:>4} take {key} {base}: WER {w:4.0%} sim {s:.2f}", flush=True)
        if w > MAX_WER or "--all" in sys.argv:
            todo.append((line, w, s))
        else:
            log[line["id"]] = dict(text=line["text"], take=base, wer=w, sim=s)
    for v in extra:                                        # one batch per variant (one seed per Parler batch)
        batch = [(l["text"], narrate._raw_path(l["text"], variant(v))) for l, _, _ in todo
                 if not os.path.exists(narrate._raw_path(l["text"], variant(v)))]
        if batch:
            narrate.BATCH[cfg["engine"]](batch, variant(v))
    for line, w0, s0 in todo:
        cands = [(w0, -s0, base, s0)]
        for v in extra:
            w, s, heard = score(narrate._raw_path(line["text"], variant(v)), line["text"])
            print(f"{line['id']:>4} take {key} {v}: WER {w:4.0%} sim {s:.2f}  {heard[:70]}", flush=True)
            if s >= MIN_SIM:
                cands.append((w, -s, v, s))
        w, _, sd, s = min(cands)
        if sd != base:                                     # the chosen take becomes the line's take
            shutil.copyfile(narrate._raw_path(line["text"], variant(sd)), narrate._raw_path(line["text"], cfg))
            h = narrate._hash(line["text"], cfg)
            for ext in (".wav", ".json"):
                p = os.path.join(narrate.CACHE, h + ext)
                if os.path.exists(p):
                    os.remove(p)                           # re-process from the new raw take
        log[line["id"]] = dict(text=line["text"], take=sd, wer=w, sim=s, was_wer=w0)
        print(f"  -> {line['id']}: {key} {sd}, WER {w0:.0%} -> {w:.0%}", flush=True)
    json.dump(log, open(log_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
