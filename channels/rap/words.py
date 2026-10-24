"""Whisper word timestamps for a song: python channels/rap/words.py SONG.wav WORDS.json LYRICS.txt

faster-whisper medium; the audio goes in as a 16 kHz numpy array (the installed PyAV rejects file paths).
LYRICS.txt is used as the initial prompt so sung words are heard as the real lyrics.
"""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.float32)
model = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, language="en", word_timestamps=True, initial_prompt=open(sys.argv[3]).read())
words = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3)) for s in segs for w in s.words]
json.dump(words, open(sys.argv[2], "w"), indent=0)
print(len(words), "words")
