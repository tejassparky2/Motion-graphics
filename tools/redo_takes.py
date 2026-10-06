"""Throw away the cloned-voice takes for some sentences so the next render makes them again.

  python tools/redo_takes.py "The last bencher is back." "Sir, just one."
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motion import voice  # noqa: E402

for text in sys.argv[1:]:
    gone = [voice._clone_raw(text)]
    for pace in (1.0, 0.9):
        k = voice._key(text, pace)
        gone += glob.glob(os.path.join(voice.ROOT, "build", "tts", k + "*"))
    for p in gone:
        if os.path.exists(p):
            os.remove(p)
    print(f"redo: {text}")
