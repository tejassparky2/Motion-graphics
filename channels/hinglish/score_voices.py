"""Score voice samples of the voice-test passage against the channel's narrator targets.

For every .wav/.mp3 in <sample_dir>: median pitch (target ~145 Hz), pace in words a minute (target ~190), Whisper
medium (Hindi) word error rate, and, for information only, speaker similarity to the reference clips in <ref_dir>.
Ranked by distance from the targets plus a clarity penalty.
Usage: python -I -X utf8 channels/hinglish/score_voices.py <sample_dir> <ref_dir>
"""
import glob, os, re, sys
import numpy as np, librosa
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_voice_text import TEXT  # noqa: E402

PITCH_HZ, WPM = 145.0, 190.0


def words(s):
    return re.findall(r"[\wऀ-ॿ]+", s.replace("़", ""))


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / len(ref)


def main():
    sdir, rdir = sys.argv[1], sys.argv[2]
    files = sorted(f for e in ("wav", "mp3") for f in glob.glob(os.path.join(sdir, f"*.{e}")) if "_line" not in f)
    enc = VoiceEncoder(verbose=False)
    refs = [enc.embed_utterance(preprocess_wav(r)) for r in sorted(glob.glob(os.path.join(rdir, "ref_*.wav")))]
    centroid = np.mean(refs, axis=0)
    centroid /= np.linalg.norm(centroid)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    ref_words = words(TEXT)
    rows = []
    for f in files:
        y, _ = librosa.load(f, sr=16000)
        yt, _ = librosa.effects.trim(y, top_db=35)
        f0, voiced, _ = librosa.pyin(yt, fmin=60, fmax=400, sr=16000)
        pitch = float(np.nanmedian(f0[voiced])) if np.any(voiced) else float("nan")
        wpm = 60 * len(ref_words) / (len(yt) / 16000)
        heard = " ".join(s.text for s in model.transcribe(yt, language="hi", beam_size=5)[0])
        w = wer(ref_words, words(heard))
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(yt, source_sr=16000)), centroid))
        score = abs(pitch - PITCH_HZ) / 25 + abs(wpm - WPM) / 25 + 3 * w
        rows.append((score, os.path.basename(f), pitch, wpm, w, sim))
    print(f"targets: pitch {PITCH_HZ:.0f} Hz, {WPM:.0f} wpm, clear Hindi (lower score = closer)")
    for score, name, pitch, wpm, w, sim in sorted(rows):
        print(f"  {score:5.2f}  {name:38s} pitch {pitch:6.1f} Hz  {wpm:5.0f} wpm  WER {w:4.0%}  (sim {sim:.2f})")


main()
