"""Synthesized soundtrack: a light plucked-string loop plus cartoon sound effects.

No samples are used — everything is generated with numpy.
"""
import wave
import zlib

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
    if name == "typing":                       # fast mechanical-keyboard clatter for `dur` seconds
        n = int(max(0.2, dur) * SR)
        out = np.zeros(n)
        i = 0
        while i < n:
            m = int(0.012 * SR)
            click = _rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / (0.0018 * SR))
            thock = np.sin(2 * np.pi * _rng.uniform(180, 260) * np.arange(m) / SR) * np.exp(-np.arange(m) / (0.004 * SR))
            out[i:i + m] += (np.diff(click, prepend=0) * 0.8 + thock * 0.35)[: n - i] * _rng.uniform(0.5, 1)
            i += int(_rng.uniform(0.055, 0.13) * SR)
        return out * _env(n, 0.01, 0.05) * 0.5
    if name == "rain":                         # soft rain on a window for `dur` seconds: filtered hiss + random drips
        n = int(max(1.0, dur) * SR)
        hiss = _lowpass(_rng.uniform(-1, 1, n), 6) - _lowpass(_rng.uniform(-1, 1, n), 60) * 0.5
        drips = np.zeros(n)
        for at in _rng.integers(0, n - 2000, int(dur * 9)):
            m = int(0.02 * SR)
            drips[at:at + m] += np.sin(2 * np.pi * _rng.uniform(1800, 3200) * np.arange(m) / SR) * np.exp(-np.arange(m) / (0.003 * SR)) * _rng.uniform(.2, .6)
        return (hiss * 0.5 + drips * 0.4) * _env(n, 0.8, 0.8) * 0.5
    if name == "ding":                         # a soft UI notification chime (counter ticks up)
        n = int(0.5 * SR)
        tt = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318 * tt) + 0.4 * np.sin(2 * np.pi * 1976 * tt)) * np.exp(-tt / 0.12) * 0.35
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


def _lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def _thud(n_sec, f0, f1, decay, noise=0.3):
    n = int(n_sec * SR)
    f = np.linspace(f0, f1, n)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (tone + noise * _lowpass(_rng.uniform(-1, 1, n), 8)) * _env(n, 0.002, decay)


def thriller_sfx(name, dur):
    """Suspense-thriller effects (the Milo series): all synthesized, no samples."""
    if name == "heartbeat":            # lub-dub, speeding up over `dur`
        n = int(max(1.0, dur) * SR)
        out, t, gap = np.zeros(n + SR), 0.0, 0.9
        while t < dur:
            for off, g in ((0.0, 1.0), (0.18, 0.7)):
                b = _thud(0.25, 70, 40, 0.07, 0.15) * g
                i = int((t + off) * SR)
                out[i:i + len(b)] += b[: max(0, len(out) - i)]
            t += gap
            gap = max(0.5, gap * 0.93)
        return out[:n] * 0.9
    if name == "sting":                # the shock: low hit + dissonant cluster that rings out
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n)
        for f in (311.1, 329.6, 466.2, 493.9, 622.3):
            out += np.sin(2 * np.pi * f * t + 2 * np.sin(2 * np.pi * 5.5 * t)) * np.exp(-t / 0.9) * 0.12
        out += _thud(2.2, 90, 30, 0.35, 0.5) * 0.9
        return out
    if name == "riser":                # tension swell that ends exactly at the cue time + dur
        n = int(max(0.6, dur) * SR)
        t = np.arange(n) / SR
        f = np.linspace(180, 900, n)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15 + _lowpass(_rng.uniform(-1, 1, n), 6) * 0.5
        return tone * (t / t[-1]) ** 2.2 * 0.8
    if name == "creak":                # old wood under weight
        n = int(max(0.5, dur) * SR)
        t = np.arange(n) / SR
        f = 110 + 60 * np.sin(2 * np.pi * 0.9 * t) + 25 * _lowpass(_rng.uniform(-1, 1, n), 2000) * 40
        saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
        grit = (np.sin(2 * np.pi * 37 * t) > 0.6)
        return _lowpass(saw * (0.4 + 0.6 * grit), 6) * np.sin(np.linspace(0, np.pi, n)) * 0.35
    if name == "knock":                # three knocks on a door
        out = np.zeros(int(1.2 * SR))
        for k in range(3):
            b = _thud(0.2, 220, 120, 0.04, 0.6)
            i = int(k * 0.32 * SR)
            out[i:i + len(b)] += b
        return out * 0.8
    if name == "buzz":                 # a phone vibrating on a table
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        gate = ((t % 0.45) < 0.32).astype(float)
        return np.sign(np.sin(2 * np.pi * 160 * t)) * _lowpass(gate, 300) * 0.12
    if name == "ring":                 # a ringtone heard through a mattress: muffled marimba
        n = int(max(1.5, dur) * SR)
        out = np.zeros(n)
        for k, m in enumerate([76, 79, 83, 81, 76, 79, 83, 86] * 4):
            i = int(k * 0.18 * SR)
            if i >= n:
                break
            nn = int(0.3 * SR)
            tt = np.arange(nn) / SR
            note = np.sin(2 * np.pi * 440 * 2 ** ((m - 69) / 12) * tt) * np.exp(-tt / 0.12)
            out[i:i + nn] += note[: n - i]
        return _lowpass(out, 14) * 0.5
    if name == "step":
        return _thud(0.3, 120, 50, 0.06, 0.8) * 0.6
    if name == "lock":
        out = np.zeros(int(0.35 * SR))
        for i0 in (0, int(0.12 * SR)):
            m = int(0.03 * SR)
            out[i0:i0 + m] += np.diff(_rng.uniform(-1, 1, m + 1)) * np.exp(-np.arange(m) / (0.004 * SR))
        return out * 0.5
    if name == "slam":
        return _thud(0.9, 80, 35, 0.2, 0.9) * 1.0
    if name == "musicbox":             # the "song" someone hums downstairs, played back as an old music box
        n = int(max(1.0, dur) * SR)
        out = np.zeros(n)
        mel = [72, 76, 79, 77, 76, 72, 74, 71, 72, 76, 79, 84, 83, 79, 77, 76]
        for k, m in enumerate(mel * 4):
            i = int(k * 0.36 * SR)
            if i >= n:
                break
            nn = int(1.2 * SR)
            tt = np.arange(nn) / SR
            f = 440 * 2 ** ((m - 69) / 12) * (1 + 0.004 * np.sin(2 * np.pi * 0.7 * tt))   # slightly detuned
            note = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt / 0.5)
            out[i:i + nn] += note[: n - i]
        return out * np.minimum(1, np.arange(n) / (0.3 * SR)) * 0.1
    if name in ("sniff", "gasp_in", "sigh"):    # breath reactions (scared, crying), reliable where voice tags aren't
        def breath(dur_s, lo, hi, shape):
            n = int(dur_s * SR)
            x = _rng.uniform(-1, 1, n)
            band = _lowpass(x, lo) - _lowpass(x, hi)                  # crude band-pass: airy, no tone
            return band * shape(np.linspace(0, 1, n))
        if name == "sniff":                    # two quick wet inhales through the nose
            one = breath(0.11, 3, 18, lambda p: np.sin(np.pi * p) ** 0.6)
            gap = np.zeros(int(0.07 * SR))
            return np.concatenate([one, gap, one * 0.8]) * 1.6
        if name == "gasp_in":                  # a sharp frightened inhale
            return breath(0.32, 2, 10, lambda p: np.minimum(1, p * 6) * np.exp(-p * 2.2)) * 1.8
        return breath(0.75, 4, 30, lambda p: np.sin(np.pi * p) ** 1.5 * (1 - 0.4 * p)) * 1.2   # shaky exhale
    if name == "whisper_air":          # breathy noise under a whisper
        n = int(max(0.5, dur) * SR)
        return np.diff(_rng.uniform(-1, 1, n + 1)) * np.sin(np.linspace(0, np.pi, n)) * 0.05
    if name == "police":               # distant siren wail
        n = int(max(1.0, dur) * SR)
        t = np.arange(n) / SR
        f = 700 + 250 * np.sin(2 * np.pi * 0.5 * t)
        return _lowpass(np.sin(2 * np.pi * np.cumsum(f) / SR), 10) * np.minimum(1, t / 0.5) * 0.12
    return None


def drone(total, seed=None):
    """The thriller bed: a low detuned drone that beats against itself, a cold high tone and air, getting slowly
    more intense toward the end."""
    n = int(total * SR) + SR
    t = np.arange(n) / SR
    rise = 0.6 + 0.4 * np.clip(t / max(total, 1), 0, 1)
    low = (np.sin(2 * np.pi * 55 * t) + np.sin(2 * np.pi * 55.7 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t)) * 0.5
    high = np.sin(2 * np.pi * (987.8 + 6 * np.sin(2 * np.pi * 0.13 * t)) * t) * 0.04 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t))
    air = _lowpass(_rng.uniform(-1, 1, n), 60) * 0.35 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t))
    return ((low + air) * rise + high)[: int(total * SR)] * 0.16


def room_tone(total, seed=None):
    """Quiet room sound under the pad (the references always keep a soft ambience, even when the music stops):
    a low, slowly breathing rumble and a faint computer-fan hiss."""
    rng = np.random.default_rng(zlib.crc32(("room" + str(seed)).encode()))
    n = int(total * SR)
    t = np.arange(n) / SR
    rumble = _lowpass(np.cumsum(rng.normal(0, 1, n)) * 0.002, 200)
    rumble -= _lowpass(rumble, 4000)
    hiss = _lowpass(rng.uniform(-1, 1, n), 12) * 0.25
    return (rumble * 3 + hiss) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * t))


def pad(total, seed=None):
    """Soft ambient bed (low-poly skits, after the owner's reference videos): slow pad chords and a mellow electric
    piano arpeggio in D minor, washed in a room reverb, very quiet; it swells a little toward the end."""
    rng = np.random.default_rng(zlib.crc32(str(seed).encode()))      # stable per episode (hash() is salted per run)
    n = int(total * SR) + 2 * SR
    t = np.arange(n) / SR
    # chords as semitones above A440 (D minor family), voiced low to high; each episode gets its own progression and
    # key (YouTube's reused-content policy: no two videos share a bed)
    progs = [[(-19, -16, -12, -9, -5), (-23, -19, -16, -12, -7), (-28, -24, -21, -17, -12), (-21, -17, -14, -7, -2)],
             [(-19, -16, -12, -9, -5), (-21, -17, -14, -7, -2), (-23, -19, -16, -12, -7), (-26, -21, -17, -14, -9)],
             [(-23, -19, -16, -12, -7), (-28, -24, -21, -17, -12), (-19, -16, -12, -9, -5), (-21, -17, -14, -7, -2)]]
    shift = int(rng.integers(-3, 4))
    chords = [tuple(440.0 * 2 ** ((x + shift) / 12) for x in c) for c in progs[int(rng.integers(0, len(progs)))]]
    span = float(rng.choice([4.8, 5.2, 5.6]))                         # long, slow chords like the references
    out = np.zeros(n)
    for k in range(int(np.ceil((total + 2) / span))):
        notes = chords[k % len(chords)]
        i0, i1 = int(k * span * SR), min(n, int((k + 1) * span * SR + 1.5 * SR))
        tt = t[i0:i1] - k * span
        env = np.clip(tt / 1.2, 0, 1) * np.clip((span + 1.5 - tt) / 1.5, 0, 1)
        for f in notes:
            for det in (-0.12, 0.0, 0.13):                          # three slightly detuned voices per note
                out[i0:i1] += env * np.sin(2 * np.pi * f * (1 + det / 100) * tt + rng.uniform(0, 6.3)) * 0.06
        for j, f0 in enumerate((notes[2], notes[3], notes[4], notes[3])):   # electric piano: one note per beat
            j0 = i0 + int(j * span / 4 * SR)
            if j0 >= n:
                break
            m = min(n - j0, int(2.5 * SR))
            tn = np.arange(m) / SR
            f = f0 * 2
            ep = (np.sin(2 * np.pi * f * tn + 0.6 * np.sin(2 * np.pi * f * tn)) * np.exp(-tn * 2.2)
                  + 0.25 * np.sin(4 * np.pi * f * tn) * np.exp(-tn * 5))
            out[j0:j0 + m] += ep * 0.05 * (0.7 + 0.3 * rng.random())
    out = _lowpass(out, 6)
    ir_n = int(1.8 * SR)                                              # small-room reverb: decaying noise
    ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 3.2)
    ir[0] = 6
    m = 1 << int(np.ceil(np.log2(n + ir_n)))
    wet = np.fft.irfft(np.fft.rfft(out, m) * np.fft.rfft(ir / np.abs(ir).sum() * 8, m), m)[:n]
    mix = 0.55 * out + 0.45 * wet
    mix += _lowpass(rng.uniform(-1, 1, n), 30) * 0.004                # a little air / tape hiss
    swell = 0.8 + 0.2 * np.clip((t - total * 0.6) / max(total * 0.4, 1), 0, 1)
    return (mix * swell)[: int(total * SR)]


def _piano(freq, dur, vel, rng):
    """A soft felt-piano note: inharmonic partials that die away faster the higher they are, a little hammer
    thump, and a damper that stops the note `dur` seconds in (with a short release)."""
    n = int((dur + 0.6) * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 7):
        fk = k * freq * np.sqrt(1 + 0.0003 * k * k)
        if fk > 9000:
            break
        out += (0.6 / k ** 1.4) * np.exp(-t * (0.9 + 0.8 * k) * (freq / 262) ** 0.35) * np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.3))
    out *= np.minimum(1, t / 0.006)
    hammer = _lowpass(rng.normal(0, 1, n), 18) * np.exp(-t / 0.012) * 0.15
    damper = np.clip(1 - (t - dur) / 0.45, 0, 1)
    return (out + hammer) * damper * vel


def score(total, seed=None, cues=None):
    """An emotional piano score that follows the story (low-poly skits; acting/sound research, 21 Oct 2026: state a
    short motif early and bring it back at the payoff; drop the music out before the key line).
    `cues`: [(time, section)], sections "light" (sparse chords), "tender" (arpeggios + the motif), "swell" (motif an
    octave up over strings), "out" (silence, the room tone carries on) and "end" (one last chord left to ring).
    Key, progression, tempo and the motif's rhythm are picked from the episode name, so no two episodes share music."""
    rng = np.random.default_rng(zlib.crc32(("score" + str(seed)).encode()))
    cues = sorted(cues or [(0.0, "tender")])
    n = int(total * SR) + 3 * SR
    out = np.zeros(n)
    strings = np.zeros(n)
    key = 48 + int(rng.choice([0, 2, 3, 5, 7]))                  # C, D, Eb, F or G major (MIDI root, octave 3)
    prog = PROGRESSIONS[int(rng.choice([0, 1, 2, 4]))]
    bpm = float(rng.choice([66, 69, 72]))
    beat = 60 / bpm
    bar = 4 * beat
    shapes = [[(0, 2, 1.5), (1.5, 1, .5), (2, 0, 2)], [(0, 1, 1), (1, 2, 1), (2, 3, 1.5), (3.5, 2, .5)],
              [(0, 3, 2), (2, 2, 1), (3, 1, 1)], [(.5, 1, .5), (1, 2, 1), (2, 1, 1), (3, 0, 1)]]
    shape = shapes[int(rng.integers(len(shapes)))]                # the motif: the same contour on every chord
    arp = [0, 2, 3, 1, 2, 3, 1, 2]
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

    def section(t):
        cur = cues[0][1]
        for at, name in cues:
            if t >= at - 1e-6:
                cur = name
        return cur

    def add(buf, t0, wave):
        i = int(t0 * SR)
        if 0 <= i < n:
            m = min(len(wave), n - i)
            buf[i:i + m] += wave[:m]
    end_at = next((at for at, name in cues if name == "end"), None)
    for b in range(int(np.ceil((total + 2) / bar))):
        t0 = b * bar
        root, q = prog[b % len(prog)]
        r = key + root
        third = r + (3 if q == "m" else 4)
        tones = [r + 12, third + 12, r + 19, r + 24]              # chord tones for the arpeggio and the motif
        sec = section(t0)
        if end_at is not None and t0 >= end_at + bar:
            break
        if end_at is not None and t0 >= end_at - 1e-6:            # the last chord, left to ring out
            for m in (r, r + 12, third + 12, r + 19):
                add(out, end_at, _piano(hz(m), 6.0, 0.32, rng))
            break
        if sec == "out":
            continue
        add(out, t0, _piano(hz(r), bar * 0.98, 0.34, rng))         # bass
        if sec == "light":
            for m in (third + 12, r + 19):
                add(out, t0, _piano(hz(m), bar * 0.5, 0.14, rng))
            add(out, t0 + 2 * beat, _piano(hz(r + 24), beat * 1.5, 0.12, rng))
            continue
        for j, k in enumerate(arp):                                # eighth-note arpeggio
            add(out, t0 + j * beat / 2, _piano(hz(tones[k]), beat * 0.9, 0.12 + 0.03 * (j == 0), rng))
        if sec == "swell" or b % 2 == 0:                          # the motif (every bar, doubled, once it swells)
            for at, idx, d in shape:
                add(out, t0 + at * beat, _piano(hz(tones[idx] + 12), d * beat, 0.32 if sec == "swell" else 0.24, rng))
                if sec == "swell":
                    add(out, t0 + at * beat, _piano(hz(tones[idx]), d * beat, 0.16, rng))
        if sec == "swell":
            tt = np.arange(int(bar * SR) + SR) / SR
            env = np.clip(tt / 1.0, 0, 1) * np.clip((bar + 1 - tt) / 1.0, 0, 1)
            w = np.zeros(len(tt))
            for m in (r + 12, third + 12, r + 19, third + 24):
                for det in (-0.15, 0.0, 0.16):
                    w += np.sin(2 * np.pi * hz(m) * (1 + det / 100) * tt + 0.004 * np.sin(2 * np.pi * 5.2 * tt) * 60) * 0.05
            add(strings, t0, w * env)
    gain = np.ones(n)                                             # "out" fades over 0.8 s and comes back over 0.4 s
    for at, name in cues:
        if name == "out":
            nxt = next((a for a, nm in cues if a > at), total + 3)
            i0, i1 = int(at * SR), int(nxt * SR)
            f0, f1 = int(0.8 * SR), int(0.4 * SR)
            gain[i0:i1] = 0
            seg_in = gain[max(0, i0 - f0):i0]
            gain[max(0, i0 - f0):i0] = np.minimum(seg_in, np.linspace(1, 0, len(seg_in)))
    level = np.array([{"light": 0.7, "tender": 0.85, "swell": 1.0}.get(section(i / SR), 1.0) for i in range(0, n, SR // 10)])
    level = np.repeat(level, SR // 10)[:n]
    level = np.convolve(level, np.ones(SR) / SR, mode="same")    # sections fade into each other over about a second
    mix = (out + 0.6 * _lowpass(strings, 4)) * gain * level
    ir_n = int(2.4 * SR)                                          # a soft hall
    ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 2.4)
    ir[0] = 8
    m = 1 << int(np.ceil(np.log2(n + ir_n)))
    wet = np.fft.irfft(np.fft.rfft(mix, m) * np.fft.rfft(ir / np.abs(ir).sum() * 8, m), m)[:n]
    mix = 0.6 * mix + 0.4 * wet
    mix += _lowpass(rng.uniform(-1, 1, n), 30) * 0.003
    return mix[: int(total * SR)]


GAINS = {"sniff": 0.45, "gasp_in": 0.5, "sigh": 0.4, "pop": 0.35, "scribble": 0.4, "thud": 0.6, "typing": 0.5, "ding": 0.45, "rain": 0.22, "whoosh": 0.6, "engine": 0.7, "kaching": 0.8, "hit": 1.0,
         "fall": 0.8, "laugh": 0.0}


def build_soundtrack(events, total, path, clips=None, seed=None, bed="plucks", cues=None):
    """Mix music + sound effects (+ voice clips [(start, samples)]) into a -14 LUFS stereo WAV.
    bed="thriller": the suspense drone instead of the plucked loop; bed="pad": the soft ambient bed; a "hush" cue silences bed and effects for its
    duration (the sudden silence before a shock)."""
    import pyloudnorm
    n = int(total * SR)
    style = bed
    bed = (drone(total, seed) if bed == "thriller" else pad(total, seed) if bed == "pad"
           else score(total, seed, cues) if bed == "score" else music(total, seed))[:n]
    hush = np.ones(n)
    fx = np.zeros(n)
    seen = set()
    for at, name, dur in events:
        key = (round(at, 2), name)
        if key in seen or GAINS.get(name, 1.0) == 0:
            continue
        seen.add(key)
        if name == "hush":
            i0, i1 = int(at * SR), int((at + dur) * SR)
            f = int(0.05 * SR)
            hush[max(0, i0):max(0, i1)] = 0
            hush[max(0, i1):max(0, i1 + f)] = np.linspace(0, 1, len(hush[max(0, i1):max(0, i1 + f)]))
            continue
        th = thriller_sfx(name, dur)
        s = (th if th is not None else sfx(name, dur)) * GAINS.get(name, 1.0)
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
        if not loud.any():       # a silent meme: no voice at all, so music + effects only
            clips = None
    bed *= _lowpass(hush, 400)
    room = room_tone(total, seed)[:n] if style in ("pad", "score") else None
    if clips:
        v_rms = rms(voice[loud])
        # music sits ~22 dB under the voice while speaking (ducked 12 dB), ~10 dB under it in the tiny gaps
        bed *= (v_rms * 10 ** ({"pad": -15, "score": -13}.get(style, -10) / 20)) / rms(bed)   # the pad sits softer
        mix = voice + bed * (1 - 0.75 * speaking) + fx * (1 - 0.3 * speaking)
        if room is not None:                                      # ~32 dB under the voice, never ducked
            mix += room * (v_rms * 10 ** (-32 / 20)) / rms(room)
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
