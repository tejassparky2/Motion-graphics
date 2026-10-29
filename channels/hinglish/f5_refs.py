"""Cut ~8 s reference prompts for IndicF5 from designed-voice candidates: the first two sentences of the voice-test
passage, ending exactly after the word "है" that closes sentence 2 (Whisper word timestamps), with their exact text.
Usage: python -I -X utf8 channels/hinglish/f5_refs.py <candidates_dir> <out_dir> name1 [name2 ...]"""
import json, os, sys
import numpy as np, soundfile as sf, librosa
from faster_whisper import WhisperModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_voice_text import TEXT  # noqa: E402

REF_TEXT = "।".join(TEXT.split("।")[:2]).strip() + "।"
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
model = WhisperModel("medium", device="cpu", compute_type="int8")
refs = {}
for name in sys.argv[3:]:
    y, sr = librosa.load(os.path.join(src, f"{name}.wav"), sr=24000)
    y16 = librosa.resample(y, orig_sr=24000, target_sr=16000)
    ws = [w for s in model.transcribe(y16, language="hi", word_timestamps=True)[0] for w in s.words]
    cut = None
    for i, w in enumerate(ws):                       # "...बिल्कुल सच है।" ends sentence 2
        if "सच" in w.word or "सज" in w.word:
            cut = (ws[i + 1].end if i + 1 < len(ws) else w.end) + 0.12
            break
    if cut is None:                                   # fall back to the first pause after 6 s
        gaps = [(b.start, a.end) for a, b in zip(ws, ws[1:]) if b.start - a.end > 0.2 and a.end > 6]
        cut = gaps[0][1] + 0.12 if gaps else 8.0
    clip = y[: int(cut * 24000)]
    path = os.path.join(out, f"{name}_ref.wav")
    sf.write(path, clip, 24000)
    refs[name] = {"audio": path, "text": REF_TEXT, "seconds": round(len(clip) / 24000, 2)}
    print(f"{name}: {len(clip) / 24000:.1f} s reference", flush=True)
json.dump(refs, open(os.path.join(out, "refs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
