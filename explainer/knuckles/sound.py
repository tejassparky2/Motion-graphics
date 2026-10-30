"""Sound design + music bed for the knuckle short, mixed under the narration.

PY=blender/4.5/python/bin/python3.11   (numpy + scipy)
$PY explainer/knuckles/sound.py voice.wav out.wav
"""
import os
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots  # noqa: E402

SR = 48000
DUR = shots.DURATION
N = int(DUR * SR)
rng = np.random.default_rng(42)


def t_(n):
    return np.arange(n) / SR


def env(n, attack, decay):
    t = t_(n)
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / decay)


def band(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def hp(x, f):
    return signal.sosfilt(signal.butter(2, f, 'highpass', fs=SR, output='sos'), x)


def lp(x, f):
    return signal.sosfilt(signal.butter(2, f, 'lowpass', fs=SR, output='sos'), x)


class Track:
    def __init__(self):
        self.L = np.zeros(N)
        self.R = np.zeros(N)

    def add(self, x, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= N:
            return
        x = x[: N - i] * gain
        g_l = np.cos((pan + 1) * np.pi / 4)
        g_r = np.sin((pan + 1) * np.pi / 4)
        self.L[i:i + len(x)] += x * g_l * 1.414
        self.R[i:i + len(x)] += x * g_r * 1.414


def reverb(x, seconds=0.8, wet=0.25):
    n = int(seconds * SR)
    ir = rng.normal(0, 1, n) * np.exp(-t_(n) / (seconds / 5))
    ir = lp(ir, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    y = signal.fftconvolve(x, ir)[: len(x) + n // 2]
    out = np.zeros(len(y))
    out[: len(x)] += x * (1 - wet)
    return out + y * wet


# ---------------------------------------------------------------- sound effects

def knuckle_crack():
    n = int(0.09 * SR)
    click = hp(rng.normal(0, 1, n), 2500) * env(n, 0.0002, 0.0018)
    body = band(rng.normal(0, 1, n), 700, 2600) * env(n, 0.0005, 0.012)
    thud = np.sin(2 * np.pi * 95 * t_(n)) * env(n, 0.001, 0.025)
    return click * 0.9 + body * 1.4 + thud * 0.5


def whoosh(dur, f0, f1, gain=1.0):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    out = np.zeros(n)
    hop = 512
    fc = np.geomspace(f0, f1, n // hop + 1)
    zi = None
    for k in range(0, n, hop):
        f = fc[k // hop]
        sos = signal.butter(2, [f * 0.6, f * 1.6], 'bandpass', fs=SR, output='sos')
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        seg, zi = signal.sosfilt(sos, x[k:k + hop], zi=zi)
        out[k:k + hop] = seg
    e = np.sin(np.pi * np.clip(t_(n) / dur, 0, 1)) ** 1.5
    return out * e * gain * 2.5


def shimmer(dur):
    n = int(dur * SR)
    t = t_(n)
    x = sum(np.sin(2 * np.pi * f * t + p) for f, p in ((2400, 0), (3100, 1), (3720, 2), (4650, 0.5)))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)
    hum = 0.5 * np.sin(2 * np.pi * 120 * t) + 0.25 * np.sin(2 * np.pi * 240 * t)
    e = np.sin(np.pi * t / dur) ** 0.7
    return (x * trem * 0.12 + hum * 0.25) * e


def chime(f=880.0, dur=1.6):
    n = int(dur * SR)
    t = t_(n)
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.2) + \
        0.3 * np.sin(2 * np.pi * f * 1.5 * t)
    return x * env(n, 0.003, 0.45) * 0.5


def stretch(dur):
    n = int(dur * SR)
    t = t_(n)
    rumble = band(rng.normal(0, 1, n), 50, 220) * 2.5
    f = 300 + 140 * t / dur + 12 * np.sin(2 * np.pi * 7 * t)
    squeak = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.12
    e = np.clip(t / 0.15, 0, 1) * np.clip((dur - t) / 0.2, 0, 1)
    return (rumble + squeak) * e


def pressure_drop(dur):
    n = int(dur * SR)
    t = t_(n)
    f = 420 * (110 / 420) ** (t / dur)
    tone = np.tanh(2.0 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25
    e = np.clip(t / 0.3, 0, 1)
    return tone * e


def fizz(dur, density0=8, density1=90):
    n = int(dur * SR)
    out = np.zeros(n)
    t = 0.0
    while t < dur:
        dens = density0 + (density1 - density0) * (t / dur) ** 2
        t += rng.exponential(1 / dens)
        i = int(t * SR)
        m = int(0.004 * SR)
        if i + m >= n:
            break
        f = rng.uniform(1800, 5200)
        out[i:i + m] += np.sin(2 * np.pi * f * t_(m)) * env(m, 0.0003, 0.0012) * rng.uniform(0.2, 0.6)
    return out


def bubble_pop():
    n = int(1.2 * SR)
    t = t_(n)
    f = 55 + 160 * np.exp(-t / 0.035)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.28)
    click = hp(rng.normal(0, 1, n), 1500) * env(n, 0.0002, 0.004)
    bloop_f = 600 * np.exp(-t / 0.06) + 250
    bloop = np.sin(2 * np.pi * np.cumsum(bloop_f) / SR) * env(n, 0.001, 0.05) * 0.4
    return reverb(boom * 1.3 + click * 0.8 + bloop, 0.9, 0.3)


def tick(high=True):
    n = int(0.03 * SR)
    f = 3200 if high else 2500
    return (np.sin(2 * np.pi * f * t_(n)) * 0.6 + hp(rng.normal(0, 1, n), 3000) * 0.4) * env(n, 0.0003, 0.005)


def rub(dur):
    n = int(dur * SR)
    return band(rng.normal(0, 1, n), 1500, 6000) * np.sin(np.pi * t_(n) / dur) * 0.15


def thunk():
    n = int(0.12 * SR)
    return lp(rng.normal(0, 1, n), 400) * env(n, 0.002, 0.03) * 1.5 + \
        np.sin(2 * np.pi * 70 * t_(n)) * env(n, 0.002, 0.05) * 0.4


# ---------------------------------------------------------------- music bed

def pluck(f, dur=0.8, bright=0.5):
    n = int(dur * SR)
    p = int(SR / f)
    buf = rng.uniform(-1, 1, p)
    buf = lp(buf, 1500 + 6000 * bright)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * env(n, 0.002, 0.35)


def music():
    bpm = 112
    beat = 60 / bpm
    trk = Track()
    # A minor-ish curious riff (A C E G / F A C E), plucked eighths
    notes = {'A3': 220.0, 'C4': 261.63, 'E4': 329.63, 'G4': 392.0, 'F3': 174.61, 'A4': 440.0,
             'D4': 293.66, 'B3': 246.94, 'E3': 164.81}
    riff = ['A3', 'E4', 'C4', 'E4', 'G4', 'E4', 'C4', 'E4', 'F3', 'C4', 'A3', 'C4', 'E4', 'C4', 'A3', 'C4']
    cache = {}
    t = 0.0
    k = 0
    while t < DUR:
        tension = shots.PRESSURE_T[0] <= t < shots.BUBBLE_T
        silent = shots.BUBBLE_T - 0.2 <= t < shots.BUBBLE_T + 0.6
        if not silent:
            name = riff[k % len(riff)]
            f = notes[name] * (2 ** (1 / 12) if tension and k % 2 else 1)
            key = (round(f, 2))
            if key not in cache:
                cache[key] = pluck(f)
            g = 0.32 if k % 2 == 0 else 0.22
            trk.add(cache[key], t, gain=g, pan=-0.3 if k % 2 else 0.3)
        t += beat / 2
        k += 1
    # soft bass on the beat
    for i, t in enumerate(np.arange(0, DUR, beat * 2)):
        if shots.BUBBLE_T - 0.2 <= t < shots.BUBBLE_T + 0.6:
            continue
        f = 55.0 if (i // 2) % 2 == 0 else 43.65
        n = int(beat * 2 * SR)
        x = np.sin(2 * np.pi * f * t_(n)) * env(n, 0.01, 0.5) * 0.35
        trk.add(x, t)
    # tension riser before the pop
    d = shots.BUBBLE_T - shots.PRESSURE_T[0]
    n = int(d * SR)
    riser = band(rng.normal(0, 1, n), 800, 5000) * (t_(n) / d) ** 3 * 0.35
    trk.add(riser, shots.PRESSURE_T[0])
    return trk


def main():
    voice_path, out = sys.argv[1], sys.argv[2]
    sr_v, v = wavfile.read(voice_path)
    v = v.astype(np.float64)
    if v.ndim > 1:
        v = v.mean(1)
    v /= max(1e-9, np.abs(v).max())
    v = signal.resample_poly(v, SR, sr_v)
    fx = Track()
    T = shots
    for dt, g in ((0.0, 1.0), (0.035, 0.8), (0.08, 0.9)):
        fx.add(knuckle_crack(), T.CRACK_T + dt, gain=g, pan=-0.15 + dt)
    fx.add(rub(0.4), 0.35, pan=-0.1)
    fx.add(whoosh(0.5, 300, 3500, 0.8), 3.32, pan=0.2)
    fx.add(shimmer(T.XRAY_T[1] - T.XRAY_T[0] + 0.6), T.XRAY_T[0] - 0.1, gain=0.7)
    fx.add(chime(988.0), T.FLUID_T, gain=0.45)
    fx.add(whoosh(0.55, 150, 1500, 1.0), 5.5, pan=-0.2)
    fx.add(stretch(T.PULL_T[1] - T.PULL_T[0] + 0.2), T.PULL_T[0], gain=0.7)
    fx.add(pressure_drop(T.PRESSURE_T[1] - T.PRESSURE_T[0] + 0.4), T.PRESSURE_T[0], gain=0.55)
    fx.add(fizz(T.BUBBLE_T - 7.8), 7.8, gain=0.5)
    fx.add(bubble_pop(), T.BUBBLE_T, gain=1.1)
    fx.add(whoosh(0.4, 600, 4000, 0.6), 10.35, pan=0.3)
    fx.add(rub(0.4), 12.45, pan=0.1)
    fx.add(thunk(), 13.4, gain=0.5)
    for i, t in enumerate(np.arange(T.TIMER_T, DUR - 0.1, 0.5)):
        fx.add(tick(i % 2 == 0), t, gain=0.35)
    fx.add(chime(1318.5, 1.2), T.TIMER_T, gain=0.3)
    mus = music()
    # duck the music under speech
    ve = np.abs(signal.resample_poly(v, 1, 1))
    ve = lp(ve, 8)
    ve = np.pad(ve, (0, max(0, N - len(ve))))[:N]
    duck = 1.0 - 0.55 * np.clip(ve / (ve.max() * 0.3), 0, 1)
    voice = np.pad(v, (int(0.0 * SR), 0))[:N]
    voice = np.pad(voice, (0, N - len(voice)))
    L = voice * 0.85 + fx.L * 0.55 + mus.L * duck * 0.22
    R = voice * 0.85 + fx.R * 0.55 + mus.R * duck * 0.22
    st = np.stack([L, R], 1)
    st = np.tanh(st * 1.1) / np.tanh(1.1)
    st /= np.abs(st).max() / 0.89
    fade = int(0.25 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wavfile.write(out, SR, (st * 32767).astype(np.int16))
    print("wrote", out, f"{len(st) / SR:.2f}s")


if __name__ == '__main__':
    main()
