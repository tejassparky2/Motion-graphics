"""Sound design for "Cute Things Kill Here": effects and music beds, all synthesized with numpy/scipy (no samples).

Every function returns a mono float32 array at 44.1 kHz and is deterministic (each sound seeds its own RNG), so a
shot sounds the same on every session. Nothing here quotes a franchise jingle or creature cry: the melodies are
generic pentatonic figures and the creature voices are formant-filtered pulse waves.
Owner rule: no heartbeats and no risers anywhere (beds keep a steady level and pitch; whoosh/bond are short swells).

Importing the module also registers the effects and beds with motion.audio (EXTRA_SFX / EXTRA_BEDS, prefixed "m_").
Run it directly to write a demo of every sound: python channels/monsters/sfx.py [out.wav]
"""
import zlib

import numpy as np
from scipy import signal

SR = 44100


# ---------------------------------------------------------------- helpers

def _rng(name, seed=0):
    return np.random.default_rng(zlib.crc32(f"{name}:{seed}".encode()))


def _t(n):
    return np.arange(n) / SR


def _n(sec):
    return max(1, int(round(sec * SR)))


def _sos(kind, f):
    return signal.butter(2 if kind == "bandpass" else 4, f, btype=kind, fs=SR, output="sos")


def _lp(x, f):
    return signal.sosfilt(_sos("lowpass", min(f, SR / 2 - 100)), x)


def _hp(x, f):
    return signal.sosfilt(_sos("highpass", f), x)


def _bp(x, lo, hi):
    return signal.sosfilt(_sos("bandpass", (lo, min(hi, SR / 2 - 100))), x)


def _exp(n, tau, attack=0.002):
    t = _t(n)
    return np.minimum(1, t / attack) * np.exp(-t / tau) if attack else np.exp(-t / tau)


def _fade(x, a=0.05, b=0.3):
    x = x.copy()
    ia, ib = min(len(x), _n(a)), min(len(x), _n(b))
    x[:ia] *= np.linspace(0, 1, ia)
    x[-ib:] *= np.linspace(1, 0, ib)
    return x


def _sweep(f, phase=0.0):
    """A sine whose frequency follows the array f (Hz per sample)."""
    return np.sin(2 * np.pi * np.cumsum(f) / SR + phase)


def _bell(f, dur, decay=0.6):
    """An inharmonic struck-bell tone (glockenspiel-like partials)."""
    n = _n(dur)
    t = _t(n)
    out = np.zeros(n)
    for ratio, amp, dk in ((1, 1, 1), (2.76, 0.35, 2.2), (5.40, 0.15, 3.5), (8.93, 0.06, 5)):
        if f * ratio < SR / 2 - 500:
            out += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dk / decay)
    return out * np.minimum(1, t / 0.002)


def _pluck(f, dur, damp=0.996, seed=0):
    """Karplus-Strong string, run as an IIR filter (fast and seeded)."""
    p = max(2, int(SR / f))
    n = _n(dur)
    x = np.zeros(n)
    x[:p] = _rng("pluck", seed * 1000 + p).uniform(-1, 1, p)
    a = np.zeros(p + 2)
    a[0], a[p], a[p + 1] = 1, -damp / 2, -damp / 2
    return _lp(signal.lfilter([1.0], a, x), 6000)


def _verb(x, mix=0.25, size=1.0, seed=0):
    """A small Schroeder reverb (four combs and two all-passes) for space around the dry sounds."""
    pad = np.concatenate([x, np.zeros(_n(1.2 * size))])
    wet = np.zeros_like(pad)
    for d, g in ((1557, 0.80), (1617, 0.79), (1491, 0.78), (1422, 0.77)):
        d = int(d * size)
        a = np.zeros(d + 1)
        a[0], a[d] = 1, -g
        wet += signal.lfilter([1.0], a, pad)
    for d, g in ((225, 0.5), (556, 0.5)):
        b = np.zeros(d + 1)
        b[0], b[d] = -g, 1
        a = np.zeros(d + 1)
        a[0], a[d] = 1, -g
        wet = signal.lfilter(b, a, wet)
    wet = _lp(wet, 7000) * 0.12
    return pad * (1 - mix) + wet * mix


def _norm(x, peak=0.8):
    m = np.max(np.abs(x))
    return (x / m * peak if m > 0 else x).astype(np.float32)


def _place(out, x, at):
    i = int(at * SR)
    if i >= len(out):
        return
    m = min(len(x), len(out) - i)
    out[i:i + m] += x[:m]


def _midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- effects

def snap(seed=0):
    """The pistol-shrimp snap: a hard crack, then the cavitation bubble collapsing with a hollow pop and fizz."""
    r = _rng("snap", seed)
    n = _n(0.6)
    out = np.zeros(n)
    m = _n(0.012)
    crack = _hp(r.uniform(-1, 1, m), 1800) * _exp(m, 0.0025, 0.0003) * 2.2
    _place(out, crack, 0)
    click = np.zeros(_n(0.003))
    click[0], click[1] = 1.0, -0.8
    _place(out, click * 1.5, 0)
    m = _n(0.07)                                                 # the bubble collapses: a fast falling "pok"
    f = 1600 * np.exp(-_t(m) * 45) + 180
    _place(out, _sweep(f) * _exp(m, 0.022, 0.001) * 0.9, 0.018)
    m = _n(0.18)                                                 # a low body thump under it
    _place(out, _sweep(np.linspace(140, 55, m)) * _exp(m, 0.05) * 0.8, 0.018)
    m = _n(0.35)                                                 # fizz of tiny bubbles
    fizz = _bp(r.uniform(-1, 1, m), 2500, 9000) * (r.random(m) > 0.97) * 2.5
    _place(out, _lp(fizz, 9000) * _exp(m, 0.09, 0.01), 0.05)
    return _norm(_verb(out, 0.15, 0.5), 0.9)


def shockwave(seed=0):
    """A deep whoomp that you feel more than hear, with a rush of displaced air rolling past."""
    r = _rng("shockwave", seed)
    n = _n(2.4)
    t = _t(n)
    boom = _sweep(95 * np.exp(-t * 2.2) + 32) * np.minimum(1, t / 0.006) * np.exp(-t / 0.45)
    boom = np.tanh(boom * 1.8)
    noise = r.uniform(-1, 1, n)
    rush_env = np.minimum(1, t / 0.08) * np.exp(-t / 0.7)
    rush = (_bp(noise, 200, 900) * 1.5 + _bp(noise, 900, 4000) * np.exp(-t * 3) * 0.8) * rush_env
    crack = _hp(noise, 2500) * _exp(n, 0.015, 0.0005) * 0.8
    return _norm(_lp(boom, 300) * 1.4 + rush * 0.9 + crack, 0.9)


def erase(seed=0):
    """Something turns to dust: a soft dry burst, then grains crumbling and pattering down, thinning out."""
    r = _rng("erase", seed)
    n = _n(2.2)
    t = _t(n)
    noise = r.uniform(-1, 1, n)
    burst = (_bp(noise, 600, 5000) + 0.6 * _lp(noise, 400)) * np.minimum(1, t / 0.02) * np.exp(-t / 0.18)
    out = burst * 0.9
    k = 0
    at = 0.05
    while at < 2.0:                                              # grains: dense at first, sparse at the end
        m = _n(r.uniform(0.004, 0.02))
        g = _bp(r.uniform(-1, 1, m), r.uniform(800, 2500), r.uniform(3000, 8000)) * _exp(m, m / SR / 3, 0.0005)
        _place(out, g * r.uniform(0.2, 0.7) * np.exp(-at * 1.2), at)
        at += r.exponential(0.006 + 0.05 * at * at)
        k += 1
    hiss = _hp(noise, 4000) * np.exp(-t / 0.9) * 0.08            # fine dust settling
    return _norm(_verb(out + hiss, 0.2, 0.8), 0.8)


def rain(dur, seed=0):
    """Steady rain: a wash of fine drops with a few fat ones hitting something close."""
    r = _rng("rain", seed)
    n = _n(max(0.5, dur))
    noise = r.uniform(-1, 1, n)
    wash = _bp(noise, 400, 6000) * 0.5 + _lp(noise, 300) * 0.25
    flutter = 1 + 0.15 * _lp(r.uniform(-1, 1, n), 3) * 30         # gusts
    wash *= np.clip(flutter, 0.6, 1.4)
    drops = np.zeros(n)
    for at in np.sort(r.uniform(0, n / SR, int(dur * 9))):
        m = _n(0.03)
        f0 = r.uniform(1800, 3500)
        _place(drops, _sweep(np.linspace(f0, f0 * 1.4, m)) * _exp(m, 0.006, 0.0003) * r.uniform(0.2, 0.6), at)
    return _norm(_fade(wash + drops, 0.4, 0.6), 0.5)


def thunder(seed=0):
    """A close strike: a ripping crack, then a long rumble that rolls in uneven waves."""
    r = _rng("thunder", seed)
    n = _n(5.0)
    t = _t(n)
    noise = r.uniform(-1, 1, n)
    rip = _hp(noise, 1500) * np.minimum(1, t / 0.004) * np.exp(-t / 0.12)
    rip *= 0.6 + 0.4 * (r.random(n) > 0.6)                        # ragged, crackly
    waves = np.ones(n) * 0.5
    for at in (0.25, 0.9, 1.6, 2.6):
        waves += r.uniform(0.4, 1.0) * np.exp(-((t - at) / r.uniform(0.25, 0.5)) ** 2)
    roll = _lp(noise, 160) * 5 * waves * np.exp(-t / 1.6) * np.minimum(1, t / 0.15)
    return _norm(rip * 0.7 + roll, 0.9)


def spark(seed=0):
    """An electrical short: a few hard arcing crackles over a harsh mains buzz, then it dies."""
    r = _rng("spark", seed)
    n = _n(0.9)
    t = _t(n)
    buzz = signal.sawtooth(2 * np.pi * 100 * t) * 0.25 * np.exp(-t / 0.3) * (t < 0.6)
    out = _lp(buzz, 3000)
    at = 0.0
    while at < 0.55:
        m = _n(r.uniform(0.005, 0.03))
        arc = _hp(r.uniform(-1, 1, m), 2000) * (r.random(m) > 0.5) * r.uniform(0.5, 1.2)
        _place(out, arc * _exp(m, m / SR / 2, 0.0002), at)
        at += r.exponential(0.035)
    return _norm(out, 0.8)


def lab_hum(dur, seed=0):
    """Room tone of a night lab: mains hum, an air-handler fan, and a faint high whine from the equipment."""
    r = _rng("lab_hum", seed)
    n = _n(max(0.5, dur))
    t = _t(n)
    hum = 0.5 * np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 100 * t) + 0.1 * np.sin(2 * np.pi * 150 * t)
    fan = _bp(r.uniform(-1, 1, n), 120, 900) * (1 + 0.1 * np.sin(2 * np.pi * 0.4 * t))
    whine = np.sin(2 * np.pi * 7400 * t) * 0.012
    return _norm(_fade(hum * 0.4 + fan * 0.6 + whine, 0.5, 0.8), 0.25)


def aquarium_bubbles(dur, seed=0):
    """A fish tank: the air pump's low drone and streams of little bubbles popping at the surface."""
    r = _rng("aquarium", seed)
    n = _n(max(0.5, dur))
    t = _t(n)
    pump = _lp(signal.square(2 * np.pi * 50 * t) * 0.3, 160) + _bp(r.uniform(-1, 1, n), 60, 300) * 0.4
    out = pump * 0.12
    at = 0.0
    while at < n / SR:
        f0 = r.uniform(500, 1600)                                # small bubbles ring higher (Minnaert)
        m = _n(0.05)
        b = _sweep(f0 * (1 + 2.5 * _t(m))) * _exp(m, r.uniform(0.008, 0.02), 0.001)
        _place(out, b * r.uniform(0.15, 0.5), at)
        at += r.exponential(0.07) if r.random() > 0.15 else r.uniform(0.2, 0.5)
    return _norm(_fade(_verb(out, 0.2, 0.4)[:n], 0.3, 0.5), 0.4)


def birds(dur, seed=0):
    """Soft birdsong somewhere in the trees: a few short whistled phrases from two or three different birds."""
    r = _rng("birds", seed)
    n = _n(max(0.5, dur))
    out = np.zeros(n)
    voices = [dict(f=r.uniform(2500, 4200), rate=r.uniform(7, 14), amp=r.uniform(0.4, 1.0)) for _ in range(3)]
    at = r.uniform(0.1, 0.5)
    while at < n / SR - 0.4:
        v = voices[int(r.integers(len(voices)))]
        notes = int(r.integers(2, 6))
        for k in range(notes):
            m = _n(r.uniform(0.05, 0.12))
            f0 = v["f"] * r.uniform(0.85, 1.2)
            shape = r.choice(["up", "down", "trill"])
            p = np.linspace(0, 1, m)
            f = (f0 * (1 + 0.35 * p) if shape == "up" else f0 * (1.3 - 0.35 * p) if shape == "down"
                 else f0 * (1 + 0.08 * np.sin(2 * np.pi * 40 * p * m / SR)))
            _place(out, _sweep(f) * np.sin(np.pi * p) ** 2 * v["amp"], at)
            at += m / SR + 1 / v["rate"]
        at += r.uniform(0.25, 1.0)
    return _norm(_fade(_verb(out, 0.35, 1.0)[:n], 0.2, 0.5), 0.3)


def chime_hud(seed=0):
    """The game HUD boots: a soft click, a quick bright four-note bell figure up a fifth-and-octave, a glassy
    shimmer, all on one warm chord (an original figure: root, fifth, octave, ninth)."""
    out = np.zeros(_n(2.0))
    _place(out, ui_blip(seed) * 0.5, 0)
    for k, semi in enumerate((0, 7, 12, 14)):
        _place(out, _bell(_midi(74 + semi), 1.2, 0.5) * (0.6 + 0.1 * k), 0.06 + 0.07 * k)
    n = _n(1.6)
    t = _t(n)
    pad = sum(np.sin(2 * np.pi * _midi(m) * t) for m in (62, 69, 74)) * np.sin(np.pi * np.clip(t / 1.6, 0, 1)) ** 2
    _place(out, pad * 0.12, 0.06)
    return _norm(_verb(out, 0.3, 0.7), 0.7)


def ui_blip(seed=0):
    """A menu cursor move: a tiny soft square blip."""
    m = _n(0.05)
    t = _t(m)
    x = _lp(signal.square(2 * np.pi * (1760 - 300 * t / 0.05) * t), 5000) * _exp(m, 0.012, 0.001)
    return _norm(x, 0.5)


def ui_select(seed=0):
    """A menu confirm: two quick rising blips with a little ring."""
    out = np.zeros(_n(0.35))
    for k, f in enumerate((_midi(88), _midi(95))):
        m = _n(0.07)
        t = _t(m)
        b = _lp(signal.square(2 * np.pi * f * t) * 0.6 + np.sin(2 * np.pi * f * t), 6000) * _exp(m, 0.03, 0.001)
        _place(out, b, 0.065 * k)
    return _norm(_verb(out, 0.2, 0.4), 0.55)


def bond(seed=0):
    """A magical bond forming: a scatter of tiny high bells over a warm major chord that swells in and fades
    (steady pitch and no build-up, so it never reads as a riser)."""
    r = _rng("bond", seed)
    n = _n(2.6)
    t = _t(n)
    env = np.sin(np.pi * np.clip(t / 2.2, 0, 1)) ** 2
    pad = sum(np.sin(2 * np.pi * _midi(m) * t + r.uniform(0, 6)) + 0.5 * np.sin(2 * np.pi * _midi(m) * 1.003 * t)
              for m in (60, 64, 67, 72)) * env * 0.1
    out = pad
    scale = [72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96]          # C major pentatonic, two octaves up
    for at in np.sort(r.uniform(0.05, 1.9, 26)):
        _place(out, _bell(_midi(int(r.choice(scale))), 0.7, 0.35) * r.uniform(0.1, 0.3), at)
    shimmer = _hp(r.uniform(-1, 1, n), 7000) * env * 0.03
    return _norm(_verb(out + shimmer, 0.35, 1.0), 0.7)


def hit(seed=0):
    """An HP-drop hit: a punchy thump and slap, then a short falling square tone (the bar draining)."""
    r = _rng("hit", seed)
    out = np.zeros(_n(0.7))
    m = _n(0.25)
    t = _t(m)
    _place(out, np.tanh(_sweep(160 * np.exp(-t * 18) + 50) * 2) * np.exp(-t / 0.07), 0)
    m2 = _n(0.04)
    _place(out, _bp(r.uniform(-1, 1, m2), 800, 6000) * _exp(m2, 0.008, 0.0005) * 1.2, 0)
    m3 = _n(0.32)
    t3 = _t(m3)
    drain = _lp(signal.square(2 * np.pi * np.cumsum(880 * np.exp(-t3 * 4.5)) / SR), 4000)
    _place(out, drain * np.exp(-t3 / 0.2) * 0.3, 0.09)
    return _norm(out, 0.85)


def cute_chirp(pitch=1.0, seed=0):
    """A creature's call: a bright "pi-yu!" with a fast vibrato (cute), shadowed by a quieter voice a semitone
    below that lags behind and a little stutter at the end (slightly wrong). pitch scales it (1.0 ~ 750 Hz;
    0.6 = bigger creature, 1.6 = tiny one); seed varies the contour."""
    r = _rng("chirp", seed)
    n = _n(0.42 / max(0.5, pitch) ** 0.3)
    p = np.linspace(0, 1, n)
    t = _t(n)
    base = 750 * pitch
    rise = r.uniform(1.25, 1.6)
    contour = base * (1 + (rise - 1) * np.sin(np.pi * np.clip(p / 0.35, 0, 1) / 2) - 0.45 * np.clip((p - 0.35) / 0.65, 0, 1))
    contour *= 1 + 0.025 * np.sin(2 * np.pi * r.uniform(9, 13) * t)

    def voice(f):
        ph = 2 * np.pi * np.cumsum(f) / SR
        src = sum(np.sin(k * ph) / k for k in range(1, 9))         # a soft pulse wave
        return _bp(src, 900 * pitch, 3200 * pitch ** 0.5) + 0.4 * np.sin(ph)

    env = np.minimum(1, p / 0.06) * np.clip((1 - p) / 0.25, 0, 1)
    main = voice(contour) * env
    lag = _n(0.025)
    ghost = np.zeros(n)
    ghost[lag:] = (voice(contour * 2 ** (-1 / 12)) * env)[: n - lag]
    out = np.concatenate([main + 0.28 * ghost, np.zeros(_n(0.25))])
    grain = main[int(n * 0.55): int(n * 0.55) + _n(0.03)] * np.hanning(_n(0.03))[: len(main[int(n * 0.55): int(n * 0.55) + _n(0.03)])]
    for k in range(3):                                           # the stutter: three fading repeats of a fragment
        _place(out, grain * (0.35 - 0.1 * k), n / SR + 0.02 + 0.045 * k)
    return _norm(_verb(out, 0.2, 0.5), 0.7)


def glitch(dur=1.7, seed=0):
    """A digital rewind glitch for `dur` seconds: a tape-rewind whirr (band-passed noise and a tone warbling around
    one pitch, so it never climbs like a riser) under stuttering digital grains (bit-crushed buzzes and square chirps
    with hard gaps)."""
    r = _rng("glitch", seed)
    n = _n(max(0.3, dur))
    t = _t(n)
    noise = r.uniform(-1, 1, n)
    whirr = _bp(noise, 1500, 5000) * 0.35 * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * t))
    tone = _sweep(900 + 260 * np.sin(2 * np.pi * 3.1 * t) + 60 * np.sin(2 * np.pi * 17 * t)) * 0.12
    out = whirr + tone
    at = 0.0
    while at < dur - 0.03:                                       # the stutter grains
        m = _n(r.uniform(0.02, 0.09))
        tt = _t(m)
        if r.random() < 0.5:
            g = signal.square(2 * np.pi * r.uniform(180, 2400) * tt)
        else:
            g = np.round(_bp(r.uniform(-1, 1, m), 300, 6000) * 4) / 4   # crushed noise
        _place(out, g * r.uniform(0.25, 0.6) * np.minimum(1, tt / 0.002), at)
        at += m / SR + (r.uniform(0.0, 0.05) if r.random() < 0.7 else r.uniform(0.08, 0.16))
    return _norm(_fade(out, 0.01, 0.06), 0.75)


def whoosh(seed=0):
    """A fast pass-by: filtered air that sweeps up and back down through the band (short; not a riser)."""
    r = _rng("whoosh", seed)
    n = _n(0.65)
    p = np.linspace(0, 1, n)
    noise = r.uniform(-1, 1, n)
    centre = np.sin(np.pi * p) ** 1.5                             # 0 -> 1 -> 0
    bands = [(200, 600), (500, 1500), (1200, 3500), (3000, 8000)]
    pos = centre * (len(bands) - 1)
    out = np.zeros(n)
    for k, (lo, hi) in enumerate(bands):
        w = np.clip(1 - np.abs(pos - k), 0, 1)
        out += _bp(noise, lo, hi) * w
    env = np.sin(np.pi * p) ** 2
    return _norm(out * env, 0.7)


# ---------------------------------------------------------------- music beds

def _pad(t, notes, detune=0.004, bright=0.3):
    x = np.zeros(len(t))
    for m in notes:
        f = _midi(m)
        x += np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * (1 + detune) * t) + bright * np.sin(2 * np.pi * 2 * f * t)
    return x / max(1, len(notes))


def _bed_lab(dur, r):
    """Calm, slightly tense: slow minor pad chords, a soft low drone, sparse high plinks, a cold added second."""
    n = _n(dur)
    t = _t(n)
    chords = [(45, 52, 57, 60, 64), (41, 48, 53, 57, 64), (43, 50, 55, 59, 62), (45, 52, 57, 60, 71)]  # Am Fmaj7 G Am(add9)
    bar = 60 / 66 * 4
    out = np.zeros(n)
    for i in range(int(dur / bar) + 1):
        s, e = int(i * bar * SR), min(n, int((i + 1.15) * bar * SR))
        if s >= n:
            break
        tt = t[s:e]
        seg = _pad(tt, chords[i % 4], 0.003, 0.15)
        w = np.sin(np.pi * np.clip((tt - tt[0]) / (bar * 1.15), 0, 1))
        out[s:e] += seg * w * 0.5
    out = _lp(out, 1800)
    out += np.sin(2 * np.pi * _midi(33) * t) * 0.12                # A1 drone
    for at in np.arange(r.uniform(0.5, 2), dur - 1, bar / 2):
        if r.random() < 0.55:
            _place(out, _bell(_midi(int(r.choice([81, 84, 88, 83]))), 1.6, 0.9) * 0.06, at)
    return out


def _bed_wonder(dur, r):
    """Bright and light: plucked pentatonic arpeggios over I-V-vi-IV, a few bells, a soft pad."""
    n = _n(dur)
    t = _t(n)
    key = 65                                                      # F
    prog = [(0, 4, 7), (7, 11, 14), (9, 12, 16), (5, 9, 12)]
    beat = 60 / 104
    out = np.zeros(n)
    cache = {}
    bar = 0
    s = 0.0
    while s < dur:
        ch = [key + x for x in prog[bar % 4]]
        notes = [ch[0], ch[1], ch[2], ch[0] + 12, ch[2], ch[1] + 12, ch[2], ch[1]]
        for k, m in enumerate(notes):
            if m not in cache:
                cache[m] = _pluck(_midi(m), 1.0, 0.994, m)
            _place(out, cache[m] * (0.5 if k % 2 else 0.7), s + k * beat / 2)
        tt = t[int(s * SR): int((s + 4 * beat) * SR)]
        _place(out, _pad(tt - tt[0], [ch[0] - 12, ch[0] - 24], 0.002, 0.1) * np.exp(-(tt - tt[0]) / 1.2) * 0.25, s)
        if r.random() < 0.6:
            _place(out, _bell(_midi(int(r.choice([84, 86, 89, 91, 93]))), 1.2, 0.6) * 0.15, s + 2 * beat)
        s += 4 * beat
        bar += 1
    return out[:n]


def _bed_danger(dur, r):
    """A low, even pulse (steady eighth notes, never a lub-dub), a dark minor drone with a cold tritone above it,
    and a dry tick: tense but flat, no build."""
    n = _n(dur)
    t = _t(n)
    beat = 60 / 132
    out = np.zeros(n)
    root = 38                                                     # D2
    pattern = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1]    # D D D D D D Eb D ... F Eb
    m = _n(beat / 2 * 0.95)
    tt = _t(m)
    i = 0
    s = 0.0
    while s < dur:
        f = _midi(root + pattern[i % 16])
        note = _lp(signal.sawtooth(2 * np.pi * f * tt) + 0.6 * np.sin(2 * np.pi * f / 2 * tt), 420)
        _place(out, note * _exp(m, 0.12, 0.004) * 0.5, s)
        if i % 2 == 1:
            k = _n(0.02)
            _place(out, _hp(r.uniform(-1, 1, k), 6000) * _exp(k, 0.004, 0.0003) * 0.15, s)
        s += beat / 2
        i += 1
    drone = _pad(t, [root + 12, root + 15], 0.005, 0.2) * 0.25 + np.sin(2 * np.pi * _midi(root + 18) * t) * 0.03
    return out + _lp(drone, 900)


_BEDS = {"lab": _bed_lab, "wonder": _bed_wonder, "danger": _bed_danger}


def music_bed(dur, mood="lab", seed=0):
    """A music bed for `dur` seconds in one of three moods: "lab", "wonder", "danger". Steady level from start to
    end (no riser, no heartbeat), RMS about -30 dBFS so it sits well under narration and ducks cleanly."""
    if mood not in _BEDS:
        raise ValueError(f"mood must be one of {sorted(_BEDS)}")
    x = _BEDS[mood](dur, _rng("bed_" + mood, seed))
    x = _verb(x, 0.25, 1.2)[: _n(dur)]
    x = _hp(x, 35)
    rms = np.sqrt(np.mean(x ** 2)) or 1
    x = x / rms * 10 ** (-30 / 20)
    return _fade(x, 1.0, 1.5).astype(np.float32)


# ---------------------------------------------------------------- registry and demo

def _register():
    try:
        from motion import audio
    except ImportError:
        return
    one_shots = dict(snap=snap, shockwave=shockwave, erase=erase, thunder=thunder, spark=spark, chime_hud=chime_hud,
                     ui_blip=ui_blip, ui_select=ui_select, bond=bond, hit=hit, whoosh=whoosh)
    for k, f in one_shots.items():
        audio.EXTRA_SFX["m_" + k] = lambda dur, f=f: f().astype(np.float64)
    for k, f in dict(rain=rain, lab_hum=lab_hum, aquarium_bubbles=aquarium_bubbles, birds=birds).items():
        audio.EXTRA_SFX["m_" + k] = lambda dur, f=f: f(dur).astype(np.float64)
    audio.EXTRA_SFX["m_chirp"] = lambda dur: cute_chirp().astype(np.float64)
    audio.EXTRA_SFX["m_glitch"] = lambda dur: glitch(dur if dur and dur > 0.2 else 1.7).astype(np.float64)
    for mood in _BEDS:
        audio.EXTRA_BEDS["m_" + mood] = lambda total, seed=None, mood=mood: music_bed(total, mood, zlib.crc32(str(seed).encode())).astype(np.float64)


_register()


def demo():
    """Every sound in a row with short gaps (beds are 5 s excerpts, normalised up so they can be heard)."""
    parts = [("snap", snap()), ("shockwave", shockwave()), ("erase", erase()), ("rain", rain(3)),
             ("thunder", thunder()), ("spark", spark()), ("lab_hum", lab_hum(3)),
             ("aquarium_bubbles", aquarium_bubbles(3)), ("birds", birds(4)), ("chime_hud", chime_hud()),
             ("ui_blip", ui_blip()), ("ui_select", ui_select()), ("bond", bond()), ("hit", hit()),
             ("cute_chirp 0.6/1.0/1.6", np.concatenate([np.concatenate([cute_chirp(p, s), np.zeros(_n(0.15))])
                                                         for s, p in enumerate((0.6, 1.0, 1.6))])),
             ("whoosh", whoosh()), ("glitch", glitch(1.7))]
    for mood in _BEDS:
        parts.append((f"music_bed {mood}", _norm(music_bed(5, mood), 0.5)))
    gap = np.zeros(_n(0.45), np.float32)
    out, marks, at = [], [], 0.0
    for name, x in parts:
        loud = np.nonzero(np.abs(x) > 0.002)[0]                   # drop reverb tails below -54 dB
        x = x[: loud[-1] + 1] if len(loud) else x
        marks.append((round(at, 2), name))
        out += [x.astype(np.float32), gap]
        at += (len(x) + len(gap)) / SR
    return np.concatenate(out), marks


if __name__ == "__main__":
    import sys
    from pathlib import Path

    import soundfile as sf

    path = Path(sys.argv[1] if len(sys.argv) > 1 else "out/monsters/tests/sfx_demo.wav")
    path.parent.mkdir(parents=True, exist_ok=True)
    x, marks = demo()
    sf.write(path, x, SR, subtype="PCM_16")
    for at, name in marks:
        print(f"{at:6.2f}s  {name}")
    print(f"wrote {path} ({len(x) / SR:.1f} s)")
