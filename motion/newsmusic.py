"""Background music for the news channel: a simple pulse bed that follows the story (synthesized, no samples).

Why it is built this way (sources in research_notes/news_music.md):
- A simple beat under spoken news made it more memorable and more enjoyable; complex music hurt both
  (Dillman Carpentier 2010, Journal of Radio & Audio Media). So: a steady pulse, short chords, no busy melody.
- No vocals or lyric-like melody: music with lyrics hurt verbal memory and reading
  (Souza & Barbosa 2023, Journal of Cognition). Nothing melodic sits in the speech band (about 1-4 kHz) under a line.
- Music that fits the story's emotion raised memory and perceived credibility of non-fiction video
  (Herget & Albrecht 2022, Psychology of Music). Each video picks a mood: "urgent", "money" or "tech".
- Tempo drives arousal and mode drives mood (Husain, Thompson & Schellenberg 2002). All moods stay brisk
  (108-128 BPM); "tech" is major, "urgent" and "money" are minor.
- Music onsets and sound changes cause orienting responses that pull attention back (Lang, LC4MP; Potter, Lang &
  Bolls 2008), and the response fades when the same cue repeats. The bed changes groove and plays a short sting at
  each scene cut, and stays steady inside a scene so it doesn't compete with the words.
- A sudden drop to silence is itself a change the brain flags. `drops` cuts the music in the pause before a
  reveal line ("But there is a catch.") and brings it back with a hit on the first word.
- Shorts count every replay as a view (YouTube, 31 Mar 2025). The last scene ends on the dominant (V) chord,
  which resolves into the tonic of bar one when the video loops.
- YouTube's spam policy names "the exact same background music" across many videos as mass-produced content,
  so key, tempo, chords, grooves and tone are picked per video from its name.
- Phone speakers barely reproduce below ~150 Hz, so the bass carries harmonics (heard via the missing
  fundamental) and the clock-like ticks sit high (6-10 kHz), above the voice.
"""
import zlib

import numpy as np

SR = 44100

MOODS = {
    # chord progressions as (semitones above the key root, quality); "m" minor, "" major, "s" sus2
    "urgent": dict(minor=True, bpm=(112, 124), progs=[
        [(0, "m"), (8, ""), (3, ""), (10, "")],      # i  VI  III VII
        [(0, "m"), (5, "m"), (8, ""), (7, "")],      # i  iv  VI  V
        [(0, "m"), (0, "m"), (8, ""), (10, "")],     # i  i   VI  VII
        [(0, "m"), (10, ""), (8, ""), (7, "")],      # i  VII VI  V (descending)
    ]),
    "money": dict(minor=True, bpm=(108, 120), progs=[
        [(0, "m"), (10, ""), (8, ""), (10, "")],     # i  VII VI VII
        [(0, "m"), (3, ""), (10, ""), (5, "m")],     # i  III VII iv
        [(0, "m"), (5, "m"), (10, ""), (3, "")],     # i  iv VII III
    ]),
    "tech": dict(minor=False, bpm=(116, 128), progs=[
        [(0, "s"), (7, ""), (9, "m"), (5, "s")],     # I  V  vi IV (sus2 colour)
        [(0, "s"), (2, ""), (5, "s"), (0, "s")],     # I  II IV I (lydian lift)
        [(5, "s"), (0, "s"), (7, ""), (9, "m")],     # IV I  V  vi
    ]),
}

# 16-step grooves for the bass pulse (1 = hit, 2 = accent); each scene gets the next one
GROOVES = [
    [2, 0, 1, 0, 1, 0, 1, 0, 2, 0, 1, 0, 1, 0, 1, 0],
    [2, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0, 0, 1, 0],
    [2, 0, 1, 1, 0, 1, 1, 0, 2, 0, 1, 1, 0, 1, 1, 0],
    [2, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0, 1, 0, 1, 1],
    [2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1],
]
TICKS = [
    [2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],   # straight 16ths, like a clock
    [2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 1],
    [2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 1, 1],
]


def _rng(seed):
    return np.random.default_rng(zlib.crc32((seed or "news").encode()))


def style(seed, mood):
    m = MOODS[mood]
    r = _rng(seed)
    return dict(minor=m["minor"], key=int(r.integers(-4, 5)), bpm=int(r.integers(m["bpm"][0], m["bpm"][1] + 1)),
                prog=m["progs"][int(r.integers(len(m["progs"])))], groove0=int(r.integers(len(GROOVES))),
                ticks=TICKS[int(r.integers(len(TICKS)))], bright=float(r.uniform(0.45, 0.75)),
                decay=float(r.uniform(0.12, 0.22)), sting=int(r.choice([7, 12, 4 if not m["minor"] else 3])),
                kick4=bool(r.integers(2)) if mood == "tech" else False)


def _hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def _triad(root, quality):
    third = {"m": 3, "": 4, "s": 2}[quality]
    return [root, root + third, root + 7]


def _bass(f, n, bright, decay):
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * f * t) + bright * np.sin(4 * np.pi * f * t) + 0.6 * bright * np.sin(6 * np.pi * f * t) \
        + 0.3 * bright * np.sin(8 * np.pi * f * t)
    return w * np.minimum(1, t / 0.004) * np.exp(-t / decay)


def _tick(n, rng):
    x = rng.uniform(-1, 1, n)
    x = np.diff(np.diff(x, prepend=0), prepend=0)   # crude high-pass: leaves the 6-10 kHz hiss
    t = np.arange(n) / SR
    return x * np.exp(-t / 0.012)


def _kick(n):
    t = np.arange(n) / SR
    f = 45 + 75 * np.exp(-t / 0.04)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    click = np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.006) * 0.3   # gives phones something to play
    return body + click


def _pad(freqs, n):
    t = np.arange(n) / SR
    w = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t) for f in freqs) / len(freqs)
    env = np.minimum(1, t / 0.25) * np.minimum(1, (t[-1] - t) / 0.2 + 1e-9)
    return w * env


def _bell(f, n):
    t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * f * 1.41 * t) * 1.2 * np.exp(-t / 0.15)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t / 0.35)


def _riser(n, rng):
    """Filtered noise that swells into a cut."""
    x = rng.uniform(-1, 1, n)
    x = np.diff(x, prepend=0)
    return x * np.linspace(0, 1, n) ** 2.5


def _impact(n, rng):
    t = np.arange(n) / SR
    f = 40 + 50 * np.exp(-t / 0.05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.3)
    m = int(0.03 * SR)
    boom[:m] += rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / (0.006 * SR)) * 0.4
    return boom


def _add(out, i, x, g=1.0):
    if i >= len(out) or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: len(out) - i]
    out[i:i + len(x)] += g * x


def _carve(x):
    """Dip the band the voice lives in (about 1-4 kHz) by ~8 dB so words stay clear."""
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    dip = 1 - 0.6 * np.exp(-0.5 * ((np.log2(np.maximum(f, 1) / 2000)) / 0.7) ** 2)
    return np.fft.irfft(spec * dip, len(x))


def news_music(total, seed=None, mood="urgent", scenes=None, drop_times=()):
    """The bed for one video. `scenes` = [(name, start, end)], `drop_times` = times of reveal lines."""
    st = style(seed, mood)
    rng = _rng((seed or "") + "fx")
    n = int(total * SR) + SR
    bass, tick, kick, pad, fx = (np.zeros(n) for _ in range(5))
    beat = 60 / st["bpm"]
    step = beat / 4
    root = 33 + st["key"] + (12 if st["key"] < 0 else 0)   # bass around A1-E2, pitched up for phones below
    scenes = scenes or [("all", 0.0, total)]
    last = len(scenes) - 1

    def scene_at(t):
        for k, (_, s, e) in enumerate(scenes):
            if t < e:
                return k
        return last

    cadence = [(5, "m" if st["minor"] else ""), (7, "")]   # iv-V / IV-V: ends on V, resolves into bar one on loop
    tick_snd = [_tick(int(0.05 * SR), rng) for _ in range(4)]
    kick_snd = _kick(int(0.35 * SR))
    t, bar = 0.0, 0
    while t < total:
        k = scene_at(t)
        prog = cadence if k == last and last > 0 else st["prog"]
        chord_root, quality = prog[bar % len(prog)]
        groove = GROOVES[(st["groove0"] + k) % len(GROOVES)]
        # bass pulse (octave up on accents for movement)
        f = _hz(root + chord_root + 12)
        for i, v in enumerate(groove):
            if v:
                tone = _bass(f * (2 if v == 2 and i == 8 else 1), int(0.4 * SR), st["bright"], st["decay"])
                _add(bass, int((t + i * step) * SR), tone, 0.9 if v == 2 else 0.6)
        # clock-like ticks
        for i, v in enumerate(st["ticks"]):
            if v:
                _add(tick, int((t + i * step) * SR), tick_snd[i % 4], 1.0 if v == 2 else 0.45)
        # kick: none in the hook's first half-bar and in the last scene (lets the question breathe)
        if k != last or last == 0:
            hits = range(4) if st["kick4"] else (0, 2)
            for b in hits:
                _add(kick, int((t + b * beat) * SR), kick_snd, 1.0)
        # low pad (kept under ~500 Hz, below the voice)
        freqs = [_hz(root + 24 + x) for x in _triad(chord_root, quality)]
        _add(pad, int(t * SR), _pad(freqs, int(4 * beat * SR)), 1.0)
        t += 4 * beat
        bar += 1

    # scene cuts: a riser into the cut, an impact and a short two-note sting on it
    for k, (_, s, _) in enumerate(scenes):
        if k == 0:
            _add(fx, 0, _impact(int(0.8 * SR), rng), 0.9)   # the hook starts at full energy, no fade-in
            continue
        r = _riser(int(0.5 * SR), rng)
        _add(fx, int(s * SR) - len(r), r, 0.05)
        _add(fx, int(s * SR), _impact(int(0.8 * SR), rng), 0.7)
        top = root + 48 + (3 if st["minor"] else 4)
        _add(fx, int(s * SR), _bell(_hz(top), int(0.6 * SR)), 0.10)
        _add(fx, int((s + step * 2) * SR), _bell(_hz(top + st["sting"]), int(0.6 * SR)), 0.08)

    bed = 0.55 * bass + 0.30 * tick + 0.35 * kick + 0.22 * pad
    bed = _carve(bed)
    # drops: silence in the pause before a reveal line, back in with a hit on its first word
    for d in drop_times:
        a, b = int((d - 0.5) * SR), int(d * SR)
        if a > 0:
            ramp = int(0.03 * SR)
            bed[a:a + ramp] *= np.linspace(1, 0, ramp)
            bed[a + ramp:b] = 0
            _add(fx, b, _impact(int(0.8 * SR), rng), 0.8)
    out = bed + fx
    return out[: int(total * SR)] / (np.max(np.abs(out)) + 1e-9) * 0.5
