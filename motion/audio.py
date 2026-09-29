"""Synthesized soundtrack: a light plucked-string loop plus cartoon sound effects.

No samples are used — everything is generated with numpy.
"""
import wave

import numpy as np

SR = 44100
_rng = np.random.default_rng(7)


def _env(n, attack=0.005, release=None):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / attack) if attack else np.ones(n)
    if release:
        e *= np.exp(-t / release)
    return e


def pluck(freq, dur, decay=0.996):
    """Karplus-Strong plucked string."""
    n = int(dur * SR)
    p = max(2, int(SR / freq))
    buf = _rng.uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out


def note(name):
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    semis = names[name[0]] + (int(name[-1]) - 4) * 12
    return 440.0 * 2 ** (semis / 12)


def music(total):
    bpm = 104
    beat = 60 / bpm
    chords = [["C3", "E4", "G4", "C5"], ["G2", "D4", "G4", "B4"], ["A2", "E4", "A4", "C5"], ["F2", "C4", "F4", "A4"]]
    out = np.zeros(int(total * SR) + SR)
    cache = {}
    t = 0.0
    bar = 0
    while t < total:
        ch = chords[bar % 4]
        pattern = [0, 2, 1, 3, 2, 1, 3, 2]  # arpeggio over 8 eighth notes
        for k, idx in enumerate(pattern):
            nt = ch[idx] if k else ch[0]
            if nt not in cache:
                cache[nt] = pluck(note(nt), 1.2)
            s = int((t + k * beat / 2) * SR)
            seg = cache[nt] * (0.9 if k == 0 else 0.5)
            out[s:s + len(seg)] += seg[: max(0, len(out) - s)]
        t += 4 * beat
        bar += 1
    return out[: int(total * SR)] * 0.16


def sfx(name, dur):
    if name == "pop":
        n = int(0.12 * SR)
        f = np.linspace(900, 300, n)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.04) * 0.5
    if name == "scribble":
        n = int(max(0.2, dur) * SR)
        noise = _rng.uniform(-1, 1, n)
        hp = np.diff(noise, prepend=0)  # crude high-pass -> pencil scratch
        strokes = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 7.5 * np.arange(n) / SR + _rng.uniform(0, 6)))
        return hp * strokes * _env(n, 0.02) * np.linspace(1, 0.6, n) * 0.07
    if name == "thud":
        n = int(0.18 * SR)
        f = np.linspace(160, 60, n)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
        return (tone + 0.3 * _rng.uniform(-1, 1, n)) * _env(n, 0.002, 0.05) * 0.45
    if name == "kaching":
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n)
        for delay, f in ((0.0, 1318), (0.08, 1760), (0.08, 2637)):
            s = int(delay * SR)
            tt = t[: n - s]
            out[s:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.25) * 0.25
        m = int(0.05 * SR)
        out[:m] += _rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / (0.01 * SR)) * 0.3
        return out
    if name == "engine":
        n = int(max(0.5, dur + 0.3) * SR)
        t = np.arange(n) / SR
        rumble = np.sin(2 * np.pi * 55 * t + 3 * np.sin(2 * np.pi * 11 * t))
        rumble += 0.4 * np.sign(np.sin(2 * np.pi * 27.5 * t))
        fade = np.minimum(1, np.minimum(t / 0.2, (t[-1] - t) / 0.4))
        return rumble * fade * 0.12
    if name == "whoosh":
        n = int(max(0.5, dur) * SR)
        noise = _rng.uniform(-1, 1, n)
        k = 40
        lp = np.convolve(noise, np.ones(k) / k, mode="same")
        return lp * np.sin(np.linspace(0, np.pi, n)) * 0.9
    if name == "fall":
        n = int(max(0.5, dur) * SR)
        f = np.linspace(1400, 180, n)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.linspace(0, np.pi, n)) * 0.22
    if name == "laugh":
        n = int(dur * SR)
        t = np.arange(n) / SR
        gate = (np.sin(2 * np.pi * 6 * t) > 0).astype(float)
        f = 260 + 40 * np.sin(2 * np.pi * 6 * t)
        voice = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR)
        k = 20
        voice = np.convolve(voice, np.ones(k) / k, mode="same")
        return voice * gate * np.linspace(1, 0.4, n) * 0.12
    return np.zeros(1)


def build_soundtrack(events, total, path):
    mix = music(total)
    seen = set()
    for at, name, dur in events:
        key = (round(at, 3), name)
        if key in seen:
            continue
        seen.add(key)
        s = sfx(name, dur)
        i = int(at * SR)
        if i >= len(mix):
            continue
        s = s[: len(mix) - i]
        mix[i:i + len(s)] += s
    # gentle fade in/out + soft limiter
    fade = int(0.5 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.tanh(mix * 2.2) * 0.9
    pcm = (mix * 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
