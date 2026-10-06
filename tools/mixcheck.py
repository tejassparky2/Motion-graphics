"""Whisper medium on the finished video's full mix (voice + music + effects), to prove the music never hides a word.
Usage: PYTHONPATH=. python tools/mixcheck.py NAME [NAME ...]"""
import difflib
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

import render

m = WhisperModel("medium.en", device="cpu", compute_type="int8")


def toks(s):
    return re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split()


for v in sys.argv[1:]:
    render._tl.clear()
    render.load(v)
    tl = render.timeline()
    pcm = subprocess.run([render.ffmpeg_bin(), "-loglevel", "error", "-i", f"out/{v}.mp4", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    heard = " ".join(s.text for s in m.transcribe(audio, language="en", beam_size=5)[0])
    said = toks(" ".join(b.spoken_text for b in tl.beats))
    got = toks(heard)
    sm = difflib.SequenceMatcher(None, said, got)
    print(f"{v}: Whisper medium on the full mix matches {100 * sm.ratio():.1f}% of the script")
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            print(f"   {' '.join(said[i1:i2])!r} -> {' '.join(got[j1:j2])!r}")
