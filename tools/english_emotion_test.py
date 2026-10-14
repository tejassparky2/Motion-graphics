"""English narration with emotion: Chatterbox's own stock voice (not a clone of anyone) at two emotion levels, plus
Chatterbox Turbo with sound tags, and the current Kokoro am_fenrir for comparison. Perth watermark left in place.

  /home/user/.venv-clone/bin/python tools/english_emotion_test.py OUT_DIR
"""
import sys

import numpy as np
import soundfile as sf
import torch

OUT = sys.argv[1]
LINES = ["A teacher finds a pack of cigarettes in the classroom trash can.",
         "The school's cameras have been broken for years.",
         "But the kids don't know that.",
         "So he makes a plan.",
         "Four minutes of silence. Then Tyler stands up.",
         "Everyone leans in. And it's... candy cigarettes!"]


def join(chunks, sr, gap=0.28):
    pad = np.zeros(int(gap * sr))
    return np.concatenate([np.concatenate([c, pad]) for c in chunks])


from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
for name, ex, cfg in (("en_stock_lively", 0.55, 0.5), ("en_stock_dramatic", 0.85, 0.35)):
    torch.manual_seed(5)
    chunks = [m.generate(t, exaggeration=ex, cfg_weight=cfg).squeeze(0).numpy() for t in LINES]
    sf.write(f"{OUT}/{name}.wav", join(chunks, m.sr), m.sr)
    print(name, flush=True)

from chatterbox.tts_turbo import ChatterboxTurboTTS
mt = ChatterboxTurboTTS.from_pretrained(device="cpu")
tagged = LINES[:-1] + ["Everyone leans in. And it's... [gasp] candy cigarettes! [laugh]"]
torch.manual_seed(5)
chunks = [mt.generate(t).squeeze(0).numpy() for t in tagged]
sf.write(f"{OUT}/en_turbo_tags.wav", join(chunks, mt.sr), mt.sr)
print("en_turbo_tags", flush=True)
