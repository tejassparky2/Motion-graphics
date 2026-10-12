"""Even out the speaking speed inside a voice take, phrase by phrase.

A whole line voiced as one take keeps natural intonation, but the model sometimes rushes part of it (lists like
"from one photo, to a 3D design, to this"). This finds each phrase (split at , . ? !) with Whisper word timestamps
and time-stretches each phrase on its own (rubberband, formant-preserving) to the same target speed, then joins the
pieces with tiny crossfades. Speed is measured as syllables per second over the phrase's word span.

  even(path_in, text, path_out, target=5.6)   -> list of (phrase, rate before, rate after)
"""
import os
import re
import subprocess
import tempfile

import numpy as np
import soundfile

from motion import voice

TEMPO_LIMITS = (0.8, 1.25)
_model = None


def _words(path):
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    segs, _ = _model.transcribe(path, language="en", word_timestamps=True, beam_size=5)
    return [w for s in segs for w in s.words]


def _stretch(x, sr, tempo):
    if abs(tempo - 1) < 0.02:
        return x
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        soundfile.write(a, x, sr)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a, "-filter:a",
                        f"rubberband=tempo={tempo:.4f}:transients=crisp:detector=compound:phase=laminar:"
                        f"window=short:formant=preserved:pitchq=quality", b], check=True)
        y, _ = soundfile.read(b)
    return y


def phrases_of(text):
    return [p for p in re.split(r"(?<=[,.?!])\s+", " ".join(text.split())) if p.strip()]


def even(path_in, text, path_out, target=5.6):
    a, sr = soundfile.read(path_in)
    if a.ndim > 1:
        a = a.mean(axis=1)
    ph = phrases_of(text)
    ws = _words(path_in)
    counts = [len(p.split()) for p in ph]
    if len(ws) != sum(counts) or len(ph) < 2:
        soundfile.write(path_out, a, sr)        # can't map words to phrases reliably: leave the take as it is
        return []
    spans, i = [], 0
    for n in counts:
        spans.append((ws[i].start, ws[i + n - 1].end))
        i += n
    # cut points: middle of the gap between phrases
    cuts = [0] + [int((spans[k][1] + spans[k + 1][0]) / 2 * sr) for k in range(len(spans) - 1)] + [len(a)]
    fade = int(0.01 * sr)
    out, report = None, []
    for p, (s0, s1), c0, c1 in zip(ph, spans, cuts, cuts[1:]):
        rate = voice.syllables(p) / max(0.12, s1 - s0)
        tempo = float(np.clip(target / rate, *TEMPO_LIMITS))
        seg = _stretch(a[c0:c1], sr, tempo)
        report.append((p, rate, rate * tempo))
        if out is None:
            out = seg
        else:
            f = min(fade, len(seg), len(out))
            ramp = np.linspace(0, 1, f)
            out = np.concatenate([out[:-f], out[-f:] * (1 - ramp) + seg[:f] * ramp, seg[f:]])
    soundfile.write(path_out, out, sr)
    return report
