"""Throw away ElevenLabs takes so the next render makes them again (and Whisper-checks them):
  python tools/el_redo.py VIDEO "exact sentence" ["another sentence" ...]
Use it when the audit (tools/audit.py) flags a take that the take-by-take check let through."""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import render
from motion import voice
from motion.timeline import Timeline

mod = render.importlib.import_module(f"videos.{sys.argv[1]}")
voice.configure(**getattr(mod, "NARRATOR", {}))
for take in Timeline.voiced_takes(mod.SCRIPT):
    if take[0] not in sys.argv[2:]:
        continue
    key, raw, *_ = voice._el_spec(*take)
    gone = glob.glob(os.path.join(voice.ROOT, "build", "el_tts", f"{raw}*")) + \
        glob.glob(os.path.join(voice.ROOT, "build", "tts", f"{key}*"))
    for f in gone:
        os.remove(f)
    print(f"redo: {take[0]!r} ({len(gone)} files)")
