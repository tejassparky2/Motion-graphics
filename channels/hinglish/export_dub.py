"""Export a voice-only dub (videos/dub_*.py): one mono 48 kHz WAV per line, trimmed to ~50 ms of silence at each end,
plus lines.json (id, text, Whisper transcript, seconds, target, fit = seconds / target).

Usage: python -I -X utf8 channels/hinglish/export_dub.py dub_monsters_ep01 out/monsters_hi/ep01_takes
"""
import importlib.util, json, os, sys, wave
import numpy as np, librosa

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from asr import whisper  # noqa: E402

PAD, OUT_SR = 0.05, 48000


def trimmed(a, sr):
    """The take with ~50 ms of silence kept at each end (loud = within 40 dB of the peak)."""
    loud = np.flatnonzero(np.abs(a) > np.abs(a).max() * 0.01)
    i0, i1 = max(0, loud[0] - int(PAD * sr)), min(len(a), loud[-1] + int(PAD * sr))
    return a[i0:i1]


def main():
    name, out = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.makedirs(out, exist_ok=True)
    model, rows = whisper(), []
    for line in mod.SCRIPT:
        a, _, _ = narrate.take(line["text"], mod.NARRATOR)
        a = librosa.resample(trimmed(a, narrate.SR).astype(np.float32), orig_sr=narrate.SR, target_sr=OUT_SR,
                             res_type="soxr_hq")
        with wave.open(os.path.join(out, f"{line['id']}.wav"), "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(OUT_SR)
            f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
        y = librosa.resample(a, orig_sr=OUT_SR, target_sr=16000)
        heard = " ".join(s.text for s in model.transcribe(y, language="hi", beam_size=5)[0]).strip()
        sec, target = round(len(a) / OUT_SR, 2), getattr(mod, "TARGET", {}).get(line["id"])
        rows.append(dict(id=line["id"], text=line["text"], transcript=heard, seconds=sec, target=target,
                         fit=round(sec / target, 2) if target else None,
                         note=getattr(mod, "NOTES", {}).get(line["id"], "")))
        print(f"{line['id']}  {sec:5.2f}s / {target}  x{rows[-1]['fit']}  {heard}", flush=True)
    json.dump(rows, open(os.path.join(out, "lines.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
