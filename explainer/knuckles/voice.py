"""Generate the narration with Kokoro TTS and save word timings for captions.

~/tts/bin/python explainer/knuckles/voice.py OUT_DIR
Writes OUT_DIR/voice.wav (24 kHz) and OUT_DIR/words.json [[word, start_s, end_s], ...].
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

# One entry per line; each is synthesised separately and joined with a pause.
LINES = [
    ("Ever wondered what that pop is when you crack your knuckles?", 0.30),
    ("Your joints are filled with fluid.", 0.20),
    ("Pull them apart, and the pressure drops so fast that a gas bubble suddenly forms.", 0.15),
    ("That's the pop!", 0.30),
    ("And it takes about twenty minutes before it can pop again.", 0.0),
]
VOICE = "af_heart"
SPEED = 1.1
SR = 24000

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
pipe = KPipeline(lang_code="a")
audio, words, t = [], [], 0.25
audio.append(np.zeros(int(0.25 * SR), np.float32))
for text, pause in LINES:
    for res in pipe(text, voice=VOICE, speed=SPEED):
        a = res.audio.numpy() if hasattr(res.audio, "numpy") else np.asarray(res.audio)
        toks = [tok for tok in res.tokens if tok.start_ts is not None]
        # Trim the silence Kokoro leaves around each phrase so the pacing stays tight.
        a0 = max(0.0, toks[0].start_ts - 0.04)
        a1 = min(len(a) / SR, toks[-1].end_ts + 0.10)
        a = a[int(a0 * SR):int(a1 * SR)]
        for tok in toks:
            if not any(c.isalnum() for c in tok.text):
                continue
            words.append([tok.text, round(t + tok.start_ts - a0, 3), round(t + tok.end_ts - a0, 3)])
        audio.append(a.astype(np.float32))
        t += len(a) / SR
    audio.append(np.zeros(int(pause * SR), np.float32))
    t += pause
wav = np.concatenate(audio)
sf.write(os.path.join(out, "voice.wav"), wav, SR)
json.dump(words, open(os.path.join(out, "words.json"), "w"), indent=0)
print(f"duration {len(wav) / SR:.2f}s, {len(words)} words")
for w in words:
    print(w)
