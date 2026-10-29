"""Rank voice candidates against the channel brief ("youthful energy, strong command of language, friendly, upbeat,
clear"): Whisper-medium WER (clarity, weighted most), UTMOS naturalness, pitch SD in semitones (energy; lively
documentary narration ~5.5-8), median pitch (youthful male ~135-185 Hz) and pace (~190 wpm). Similarity to any real
voice is deliberately not a criterion. Lower penalty = better.
Usage: python -I -X utf8 channels/hinglish/rank_voices.py <dir_of_wavs> [out_json]"""
import glob, json, os, re, sys
import numpy as np, librosa
from faster_whisper import WhisperModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_voice_text import TEXT  # noqa: E402
from naturalness import mos  # noqa: E402

words = lambda s: re.findall(r"[\wऀ-ॿ]+", s.replace("़", ""))


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / len(ref)


def penalty(r):
    p = 3 * r["wer"] + max(0.0, 3.3 - r["mos"])
    p += 0.4 * max(0.0, 5.5 - r["sd"]) + 0.4 * max(0.0, r["sd"] - 8.0)
    p += 0 if 135 <= r["median"] <= 185 else 0.5
    p += abs(r["wpm"] - 190) / 100
    return p


def main():
    d = sys.argv[1]
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    rows = []
    for f in sorted(glob.glob(os.path.join(d, "*.wav"))):
        y, _ = librosa.load(f, sr=16000)
        y, _ = librosa.effects.trim(y, top_db=35)
        f0, v, _ = librosa.pyin(y, fmin=65, fmax=500, sr=16000)
        f0 = f0[v]
        st = 12 * np.log2(f0 / np.median(f0))
        heard = " ".join(s.text for s in model.transcribe(y, language="hi", beam_size=5)[0])
        r = dict(name=os.path.basename(f)[:-4], wer=wer(words(TEXT), words(heard)), mos=mos(f), median=float(np.median(f0)),
                 range=float(np.percentile(st, 95) - np.percentile(st, 5)), sd=float(st.std()),
                 wpm=60 * len(words(TEXT)) / (len(y) / 16000))
        r["penalty"] = penalty(r)
        rows.append(r)
        print(f"  {r['name']:24s} WER {r['wer']:4.0%}  MOS {r['mos']:.2f}  {r['median']:4.0f} Hz  range {r['range']:4.1f} st"
              f"  SD {r['sd']:3.1f}  {r['wpm']:3.0f} wpm  -> {r['penalty']:.2f}", flush=True)
    rows.sort(key=lambda r: r["penalty"])
    print("\nbest first:")
    for r in rows[:10]:
        print(f"  {r['penalty']:.2f}  {r['name']:24s} WER {r['wer']:4.0%}  MOS {r['mos']:.2f}  {r['median']:4.0f} Hz  SD {r['sd']:3.1f}  {r['wpm']:3.0f} wpm")
    if len(sys.argv) > 2:
        json.dump(rows, open(sys.argv[2], "w"), indent=1)


main()
