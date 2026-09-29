"""Voice-over narration with Piper (offline neural text-to-speech).

The voice model (~120 MB) is downloaded on first use into build/voices/, and every
line is cached in build/tts/ so re-renders only synthesize lines that changed.
"""
import hashlib
import os
import subprocess
import sys
import urllib.request
import wave

import numpy as np

from .engine import ROOT

VOICE = os.environ.get("NARRATOR_VOICE", "en_US-ryan-high")
LENGTH_SCALE = float(os.environ.get("NARRATOR_PACE", "1.0"))  # >1 = slower speech
VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"
SR = 44100


def _voice_path():
    d = os.path.join(ROOT, "build", "voices")
    os.makedirs(d, exist_ok=True)
    model = os.path.join(d, f"{VOICE}.onnx")
    lang, name, quality = VOICE.split("-")
    url = f"{VOICE_BASE}/{lang.split('_')[0]}/{lang}/{name}/{quality}/{VOICE}.onnx"
    for path, src in ((model, url), (model + ".json", url + ".json")):
        if not os.path.exists(path):
            print(f"downloading {os.path.basename(path)}", file=sys.stderr)
            urllib.request.urlretrieve(src, path + ".part")
            os.replace(path + ".part", path)
    return model


def _read_wav(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32767
        if w.getnchannels() == 2:
            a = a[::2]
    if sr != SR:
        a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    return a


def synth(text):
    """Speech for one line as float samples at 44.1 kHz (cached)."""
    model = _voice_path()
    key = hashlib.sha1(f"{VOICE}|{LENGTH_SCALE}|{text}".encode()).hexdigest()[:16]
    out = os.path.join(ROOT, "build", "tts", f"{key}.wav")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", out, "--length-scale", str(LENGTH_SCALE)],
                       input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    return _read_wav(out)


def narration_track(schedule, total):
    """Mix all lines into one track. Returns (track, speaking) where speaking is a 0..1 envelope for ducking."""
    track = np.zeros(int(total * SR))
    busy_until = 0.0
    for at, text in sorted(schedule):
        clip = synth(text)
        if at < busy_until:
            print(f"warning: line at {at:.2f}s overlaps the previous one (ends {busy_until:.2f}s): {text!r}",
                  file=sys.stderr)
        busy_until = at + len(clip) / SR
        if busy_until > total:
            print(f"warning: line at {at:.2f}s runs past the end of the video: {text!r}", file=sys.stderr)
        i = int(at * SR)
        clip = clip[: max(0, len(track) - i)]
        track[i:i + len(clip)] += clip
    # speaking envelope: rectified voice, smoothed, with a slow release so music doesn't pump between words
    env = (np.abs(track) > 0.01).astype(np.float64)
    k = int(0.35 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    return track, np.clip(env * 4, 0, 1)
