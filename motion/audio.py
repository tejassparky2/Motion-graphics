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


# Per-episode music: every video gets its own key, chord progression, tempo, arpeggio and string tone, picked
# deterministically from the episode name. YouTube's spam policy calls out channels that reuse "the exact same
# background music" across many videos, so no two episodes share a bed.
PROGRESSIONS = [   # chords as (root semitone, quality) in a major key; "m" = minor triad
    [(0, ""), (7, ""), (9, "m"), (5, "")],      # I  V  vi IV
    [(9, "m"), (5, ""), (0, ""), (7, "")],      # vi IV I  V
    [(0, ""), (9, "m"), (5, ""), (7, "")],      # I  vi IV V
    [(2, "m"), (7, ""), (0, ""), (9, "m")],     # ii V  I  vi
    [(0, ""), (5, ""), (9, "m"), (7, "")],      # I  IV vi V
    [(9, "m"), (7, ""), (5, ""), (7, "")],      # vi V  IV V
]
PATTERNS = [[0, 2, 1, 3, 2, 1, 3, 2], [0, 1, 2, 3, 2, 1, 2, 3], [0, 3, 2, 1, 3, 2, 1, 2], [0, 2, 3, 2, 1, 2, 3, 1]]


def _style(seed):
    import zlib
    r = np.random.default_rng(zlib.crc32(seed.encode()) if seed else 0)
    if not seed:   # the original channel bed
        return dict(key=0, prog=PROGRESSIONS[0], pattern=PATTERNS[0], bpm=124, decay=0.996)
    return dict(key=int(r.integers(-5, 7)), prog=PROGRESSIONS[int(r.integers(len(PROGRESSIONS)))],
                pattern=PATTERNS[int(r.integers(len(PATTERNS)))], bpm=int(r.choice([116, 120, 124, 128, 132])),
                decay=float(r.choice([0.990, 0.993, 0.996])))


def _voicing(root, quality, key):
    third = 3 if quality == "m" else 4
    base = 48 + key + root            # MIDI: C3 = 48
    return [base - 12 if root > 4 else base, base + 12 + third, base + 19, base + 24]


def music(total, seed=None):
    st = _style(seed)
    beat = 60 / st["bpm"]   # tempos stay >=116 BPM (fast beds tend to lift watch-through)
    out = np.zeros(int(total * SR) + SR)
    cache = {}
    t = 0.0
    bar = 0
    while t < total:
        ch = _voicing(*st["prog"][bar % 4], st["key"])
        for k, idx in enumerate(st["pattern"]):   # arpeggio over 8 eighth notes
            m = ch[idx] if k else ch[0]
            if m not in cache:
                cache[m] = pluck(440.0 * 2 ** ((m - 69) / 12), 1.2, st["decay"])
            s = int((t + k * beat / 2) * SR)
            seg = cache[m] * (0.9 if k == 0 else 0.5)
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
    if name == "hit":
        # full-weight impact for the big plot turns: low boom + noise burst
        n = int(0.45 * SR)
        f = np.linspace(110, 40, n)
        boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.18)
        m = int(0.08 * SR)
        boom[:m] += _rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / (0.015 * SR)) * 0.5
        return boom * 0.6
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


GAINS = {"pop": 0.35, "scribble": 0.4, "thud": 0.6, "whoosh": 0.6, "engine": 0.7, "kaching": 0.8, "hit": 1.0,
         "fall": 0.8, "laugh": 0.0}


def build_soundtrack(events, total, path, clips=None, seed=None):
    """Mix music + sound effects (+ voice clips [(start, samples)]) into a -14 LUFS stereo WAV."""
    import pyloudnorm
    n = int(total * SR)
    bed = music(total, seed)[:n]
    fx = np.zeros(n)
    seen = set()
    for at, name, dur in events:
        key = (round(at, 2), name)
        if key in seen or GAINS.get(name, 1.0) == 0:
            continue
        seen.add(key)
        s = sfx(name, dur) * GAINS.get(name, 1.0)
        i = int(at * SR)
        if 0 <= i < n:
            s = s[: n - i]
            fx[i:i + len(s)] += s
    rms = lambda x: np.sqrt(np.mean(x ** 2)) + 1e-9
    if clips:
        from .voice import narration_track
        voice, speaking = narration_track(clips, total)
        voice, speaking = voice[:n], speaking[:n]
        loud = speaking > 0.5
        v_rms = rms(voice[loud])
        # music sits ~22 dB under the voice while speaking (ducked 12 dB), ~10 dB under it in the tiny gaps
        bed *= (v_rms * 10 ** (-10 / 20)) / rms(bed)
        mix = voice + bed * (1 - 0.75 * speaking) + fx * (1 - 0.3 * speaking)
    else:
        mix = bed + fx
    # very short fades so the Short loops cleanly
    a, b = int(0.03 * SR), int(0.12 * SR)
    mix[:a] *= np.linspace(0, 1, a)
    mix[-b:] *= np.linspace(1, 0, b)
    # loudness-normalise to -14 LUFS, then keep peaks under -1 dBFS with a soft clip
    meter = pyloudnorm.Meter(SR)
    mix = pyloudnorm.normalize.loudness(mix, meter.integrated_loudness(mix), -14.0)
    ceiling = 10 ** (-1 / 20)
    mix = np.where(np.abs(mix) > 0.8 * ceiling,
                   np.sign(mix) * (0.8 * ceiling + 0.2 * ceiling * np.tanh((np.abs(mix) - 0.8 * ceiling) / (0.2 * ceiling))),
                   mix)
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    return meter.integrated_loudness(pcm.astype(np.float64) / 32767)
