"""Clarity retakes (copied from channels/hinglish/retake.py, now per language): every line whose take Whisper medium
hears with more than MAX_WER word error gets two more IndicF5 takes; the clearest take that still sounds like the
narrator (speaker similarity >= MIN_SIM to the voice prompt) becomes the line's take. Choices are logged in
build/mythology/<video>_<lang>_retakes_<voice>.json.

Whisper is much weaker in Kannada than in Hindi: for Kannada a high WER points at a line to listen to, and the
owner's ear decides.

Usage: python -I -X utf8 channels/mythology/retake.py <video> <hi|kn> [--all]
"""
import importlib.util, json, os, shutil, sys
import numpy as np, librosa
from resemblyzer import VoiceEncoder, preprocess_wav

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from asr import whisper  # noqa: E402
from channel import NARRATORS, WHISPER_LANG  # noqa: E402
from render_myth import wer, words  # noqa: E402

MAX_WER, MIN_SIM = 0.30, 0.85


def main():
    name, lang = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cfg = getattr(mod, "NARRATORS", NARRATORS)[lang]
    script = mod.SCRIPTS[lang]
    narrate.prefetch(script, cfg)                         # make sure every default take exists
    model = whisper()
    enc = VoiceEncoder(verbose=False)
    ref_emb = enc.embed_utterance(preprocess_wav(cfg["ref_audio"]))
    voice = narrate._hash("", {k: v for k, v in cfg.items()
                               if k not in ("studio", "pace_wps", "pitch_expand", "tempo", "take")})
    log_path = os.path.join(narrate.ROOT, "build", "mythology", f"{name}_{lang}_retakes_{voice}.json")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    log = json.load(open(log_path, encoding="utf-8")) if os.path.exists(log_path) else {}

    def score(path, text):
        a, _ = narrate._trim(narrate._decode(open(path, "rb").read()))
        y = librosa.resample(a.astype(np.float32), orig_sr=narrate.SR, target_sr=16000)
        heard = " ".join(s.text for s in model.transcribe(y, language=WHISPER_LANG[lang], beam_size=5)[0])
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), ref_emb))
        return wer(words(text), words(heard)), sim, heard.strip()

    key, extra = "take", [1, 2]                           # IndicF5 samples fresh noise each run: a take is a new run
    base = cfg.get(key, 0)
    variant = lambda v: {**cfg, key: v}
    todo = []
    for line in script:
        if line["id"] in log and log[line["id"]].get("text") == line["text"]:
            continue                                       # already decided for this exact text
        w, s, heard = score(narrate._raw_path(line["text"], cfg), line["text"])
        print(f"{line['id']:>4} take {base}: WER {w:4.0%} sim {s:.2f}  {heard[:70]}", flush=True)
        if w > MAX_WER or "--all" in sys.argv:
            todo.append((line, w, s))
        else:
            log[line["id"]] = dict(text=line["text"], take=base, wer=w, sim=s)
    for v in extra:
        batch = [(l["text"], narrate._raw_path(l["text"], variant(v))) for l, _, _ in todo
                 if not os.path.exists(narrate._raw_path(l["text"], variant(v)))]
        if batch:
            narrate.BATCH[cfg["engine"]](batch, variant(v))
    for line, w0, s0 in todo:
        cands = [(w0, -s0, base, s0)]
        for v in extra:
            w, s, heard = score(narrate._raw_path(line["text"], variant(v)), line["text"])
            print(f"{line['id']:>4} take {v}: WER {w:4.0%} sim {s:.2f}  {heard[:70]}", flush=True)
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
        print(f"  -> {line['id']}: take {sd}, WER {w0:.0%} -> {w:.0%}", flush=True)
    json.dump(log, open(log_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
