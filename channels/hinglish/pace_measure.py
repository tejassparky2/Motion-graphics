"""Measure narration pace from word timestamps (faster-whisper medium, Hindi): articulation rate (words per second
of speaking, pauses excluded), and the pauses between words: how often they occur and how long they are, split
into short phrase pauses and longer sentence pauses. Used to match our narrator's timing to the reference.

Usage: python -I -X utf8 channels/hinglish/pace_measure.py <out_json> file1 [file2 ...]   (audio or video)
"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asr import whisper  # noqa: E402

SR = 16000
PAUSE = 0.12          # a gap shorter than this is just coarticulation, not a pause


def load(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32)


model = whisper()
results = {}
for path in sys.argv[2:]:
    segs, _ = model.transcribe(load(path), language="hi", beam_size=5, word_timestamps=True, vad_filter=False)
    words = [w for s in segs for w in s.words]
    gaps = np.array([b.start - a.end for a, b in zip(words, words[1:])])
    speak = sum(w.end - w.start for w in words)
    pauses = gaps[gaps >= PAUSE]
    sentence = pauses[pauses >= 0.35]
    phrase = pauses[pauses < 0.35]
    r = dict(words=len(words), articulation_wps=round(len(words) / speak, 2),
             overall_wpm=round(60 * len(words) / (words[-1].end - words[0].start), 1),
             pauses_per_10_words=round(10 * len(pauses) / len(words), 2),
             phrase_pause_median=round(float(np.median(phrase)), 3) if len(phrase) else None,
             sentence_pause_median=round(float(np.median(sentence)), 3) if len(sentence) else None,
             sentence_pause_p90=round(float(np.percentile(sentence, 90)), 3) if len(sentence) else None,
             longest_pause=round(float(gaps.max()), 3) if len(gaps) else None)
    results[path] = r
    print(path.split("\\")[-1], r, flush=True)
json.dump(results, open(sys.argv[1], "w"), indent=1)
