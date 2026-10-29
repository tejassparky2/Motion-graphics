"""Synthesised soundtrack, sample-accurately synced to the animation.

Run with any Python that has numpy + scipy (Blender's bundled Python works):
    python synth.py scene_motion.npz out.wav

Layers
  * sea: filtered noise swells + lapping under the pier
  * gulls: formant-shaped glissando calls, panned around
  * bicycle: tyre thumps on every plank seam (from the real wheel position),
    chain whir with cadence, freewheel pawl ticks while coasting, saddle creaks
  * pelican: bill clacks when the jaw keys open/close
  * music: a small plucked-string (Karplus-Strong) waltz with a glockenspiel line
"""
import sys

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
RNG = np.random.default_rng(5)


def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1.0) * np.exp(-np.maximum(t - a, 0) / max(d, 1e-4))


def butter(x, lo=None, hi=None, order=2):
    if lo and hi:
        sos = signal.butter(order, [lo, hi], btype='band', fs=SR, output='sos')
    elif lo:
        sos = signal.butter(order, lo, btype='high', fs=SR, output='sos')
    else:
        sos = signal.butter(order, hi, btype='low', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def pan(mono, p):
    """p in [-1, 1] (scalar or per-sample) -> stereo with constant power."""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([mono * np.cos(a), mono * np.sin(a)], 1)


def place(buf, clip, t0):
    i0 = int(t0 * SR)
    if i0 >= len(buf):
        return
    n = min(len(clip), len(buf) - i0)
    if i0 < 0:
        clip = clip[-i0:]
        n = min(len(clip), len(buf))
        i0 = 0
    buf[i0:i0 + n] += clip[:n]


def reverb(x, decay=1.6, mix=0.25, pre=0.02):
    """Cheap stereo reverb: decaying filtered noise convolution."""
    n = int(decay * SR)
    t = np.arange(n) / SR
    out = np.zeros_like(x)
    for ch in range(x.shape[1]):
        ir = RNG.normal(0, 1, n) * np.exp(-t * 6.9 / decay)
        ir = butter(ir, hi=6000)
        ir[:int(pre * SR)] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        out[:, ch] = signal.fftconvolve(x[:, ch], ir)[:len(x)]
    return x * (1 - mix) + out * mix


# ---------------------------------------------------------------------------
def sea(T):
    n = int(T * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for ch in range(2):
        w = RNG.normal(0, 1, n)
        brown = np.cumsum(w)
        brown -= signal.savgol_filter(brown, 4001, 1) if n > 4001 else brown.mean()
        brown /= np.abs(brown).max() + 1e-9
        surf = butter(RNG.normal(0, 1, n), 200, 1800)
        swell = 0.55 + 0.45 * np.sin(2 * np.pi * t / (6.5 + ch * 0.8) + ch * 1.7) ** 2
        lap = np.zeros(n)
        k = 0.3
        while k < T:
            dur = RNG.uniform(0.25, 0.7)
            clip = butter(RNG.normal(0, 1, int(dur * SR)), 400, 3500) * env_ad(int(dur * SR), 0.03, dur / 3)
            place(lap, clip * RNG.uniform(0.2, 0.5), k)
            k += RNG.uniform(0.6, 1.8)
        out[:, ch] = 0.35 * brown + 0.22 * surf * swell + 0.35 * lap
    return out


def gull_call(dur=0.32, f0=None):
    f0 = f0 or RNG.uniform(1300, 1700)
    n = int(dur * SR)
    t = np.arange(n) / SR
    glide = f0 * (1.0 + 0.25 * np.exp(-t * 18) - 0.18 * t / dur)
    ph = 2 * np.pi * np.cumsum(glide) / SR
    tone = sum(np.sin(k * ph) / k ** 1.2 for k in range(1, 9))
    noise = RNG.normal(0, 0.3, n)
    x = (tone + noise) * env_ad(n, 0.015, dur * 0.45)
    x = butter(x, 900, 5200)
    return x / (np.abs(x).max() + 1e-9)


def gulls(T, events):
    n = int(T * SR)
    out = np.zeros((n, 2))
    for t0, count, p, vol in events:
        f0 = RNG.uniform(1250, 1700)
        k = t0
        for i in range(count):
            c = gull_call(RNG.uniform(0.22, 0.38), f0 * RNG.uniform(0.95, 1.05))
            place(out, pan(c * vol, p), k)
            k += RNG.uniform(0.28, 0.42)
    return reverb(out, decay=1.2, mix=0.35)


def bicycle(T, m, gains):
    n = int(T * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    # tyre thumps over plank seams for both wheels (front leads by the wheelbase)
    x = np.interp(t, m['t'], m['x'])
    pitch = 0.152
    thump = np.zeros(n)
    for off in (0.84, 0.0):
        idx = np.nonzero(np.diff(np.floor((x + off) / pitch)) > 0)[0]
        for i in idx:
            dur = 0.035
            clip = butter(RNG.normal(0, 1, int(dur * SR)), 60, 900) * env_ad(int(dur * SR), 0.001, 0.008)
            clip += 0.6 * np.sin(2 * np.pi * 95 * np.arange(len(clip)) / SR) * env_ad(len(clip), 0.001, 0.012)
            place(thump, clip * RNG.uniform(0.5, 1.0), i / SR)
    # chain whir follows cadence; freewheel ticks while coasting
    cad = np.interp(t, m['t'], np.gradient(m['crank'], m['t']) / (2 * np.pi))
    whir = butter(RNG.normal(0, 1, n), 1200, 4500) * np.clip(cad, 0, 2) * 0.10
    whir *= 0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(cad * 44) / SR) ** 2
    wheel = np.interp(t, m['t'], m['wheel'])
    cog = np.interp(t, m['t'], m['cog'])
    slip = (wheel - cog) / (2 * np.pi) * 24          # 24 pawl notches per revolution
    ticks = np.zeros(n)
    idx = np.nonzero(np.diff(np.floor(slip)) > 0)[0]
    for i in idx:
        clip = butter(RNG.normal(0, 1, 300), 2500, 9000) * env_ad(300, 0.0003, 0.0015)
        clip += 0.5 * np.sin(2 * np.pi * 3200 * np.arange(300) / SR) * env_ad(300, 0.0002, 0.002)
        place(ticks, clip * 0.55, i / SR)
    # saddle spring creaks on each power stroke
    crank = np.interp(t, m['t'], m['crank'])
    creak = np.zeros(n)
    idx = np.nonzero(np.diff(np.floor(crank / np.pi)) > 0)[0]
    for i in idx:
        dur = 0.12
        k = int(dur * SR)
        f = RNG.uniform(380, 520)
        ph = 2 * np.pi * np.cumsum(f * (1 + 0.15 * np.sin(np.arange(k) / SR * 60))) / SR
        clip = np.sign(np.sin(ph)) * 0.3 * env_ad(k, 0.02, 0.04)
        creak[i:i + k] += butter(clip, 300, 2500)[:max(0, min(k, n - i))] * 0.12
    mono = thump * 0.9 + whir + ticks + creak
    g = np.interp(t, gains[0], gains[1])
    out = pan(mono * g, 0.0)
    return out


def bill_clacks(T, jaw_keys):
    n = int(T * SR)
    out = np.zeros(n)
    jk = np.asarray(jaw_keys)
    for i in range(1, len(jk)):
        if jk[i, 1] < jk[i - 1, 1] - 0.03:        # jaw closing
            clip = butter(RNG.normal(0, 1, 2400), 500, 4000) * env_ad(2400, 0.0005, 0.01)
            clip += 0.8 * np.sin(2 * np.pi * 720 * np.arange(2400) / SR) * env_ad(2400, 0.0005, 0.02)
            place(out, clip * 0.5, jk[i, 0] - 0.02)
    return pan(out, 0.1)


# ---------------------------------------------------------------------------
NOTE = {n: i for i, n in enumerate(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])}


def freq(name):
    note, octv = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[note] + 12 * (octv + 1) - 69) / 12)


def pluck(f, dur, bright=0.5):
    """Karplus-Strong plucked string."""
    n = int(dur * SR)
    period = int(SR / f)
    buf = RNG.uniform(-1, 1, period)
    buf = butter(buf, hi=2000 + 6000 * bright) if period > 30 else buf
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = 0.4985 * (buf[i % period] + buf[(i + 1) % period])
    return out * env_ad(n, 0.002, dur * 0.6)


def bell(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
         + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12))
    return x * env_ad(n, 0.002, dur * 0.35)


def music(T, bpm=84):
    """A gentle seaside waltz in D major (3/4)."""
    n = int(T * SR)
    out = np.zeros((n, 2))
    beat = 60.0 / bpm
    chords = [['D3', 'A3', 'D4', 'F#4'], ['A2', 'E3', 'A3', 'C#4'], ['B2', 'F#3', 'B3', 'D4'],
              ['G2', 'D3', 'G3', 'B3'], ['D3', 'A3', 'D4', 'F#4'], ['G2', 'D3', 'G3', 'B3'],
              ['E3', 'B3', 'E4', 'G4'], ['A2', 'E3', 'A3', 'C#4']]
    melody = [('F#5', 0, 1.5), ('E5', 1.5, 0.5), ('D5', 2, 1), ('C#5', 3, 2), ('A4', 5, 1),
              ('B4', 6, 1.5), ('C#5', 7.5, 0.5), ('D5', 8, 1), ('B4', 9, 3),
              ('A4', 12, 1.5), ('B4', 13.5, 0.5), ('A4', 14, 1), ('G4', 15, 2), ('B4', 17, 1),
              ('E5', 18, 1.5), ('D5', 19.5, 0.5), ('C#5', 20, 1), ('A4', 21, 3)]
    bar = 3 * beat
    nbars = int(T / bar) + 1
    for b in range(nbars):
        ch = chords[b % len(chords)]
        t0 = b * bar + 0.25
        # bass on 1, strum-arpeggio on 2 and 3
        place_st(out, pluck(freq(ch[0]), 2.2, 0.3) * 0.55, t0, -0.2)
        for k, nt in enumerate(ch[1:]):
            place_st(out, pluck(freq(nt), 1.4, 0.6) * 0.30, t0 + beat + k * 0.035, 0.15)
            place_st(out, pluck(freq(nt), 1.2, 0.6) * 0.24, t0 + 2 * beat + k * 0.035, 0.2)
    loop = 24 * beat
    for rep in range(int(T / loop) + 1):
        for nt, st, ln in melody:
            t0 = 0.25 + rep * loop + st * beat
            place_st(out, bell(freq(nt), ln * beat + 1.2) * 0.16, t0, -0.1)
    return reverb(out, decay=2.4, mix=0.3)


def place_st(buf, mono, t0, p):
    place(buf, pan(mono, p), t0)


def main(npz, out_wav):
    m = dict(np.load(npz))
    T = float(m['t'][-1]) + 1.0 / 24
    shots = m['shots']
    # per-shot mix: (bike gain) - close shots hear the bike, wide shots hear the sea
    bike_g = {0: 0.35, 1: 1.0, 2: 0.8, 3: 0.75, 4: 0.30}
    gt, gv = [], []
    for i, (a, b) in enumerate(shots):
        gt += [a + 0.01, b - 0.01]
        gv += [bike_g.get(i, 0.6)] * 2
    gains = (np.array(gt), np.array(gv))
    layers = {
        'sea': sea(T),
        'bike': bicycle(T, m, gains),
        'clacks': bill_clacks(T, m['jaw']),
        'gulls': gulls(T, [(1.2, 3, -0.6, 0.18), (6.4, 2, 0.7, 0.10), (11.8, 4, -0.3, 0.14),
                           (16.6, 3, 0.5, 0.22), (18.7, 2, -0.7, 0.12)]),
        'music': music(T),
    }
    # target loudness of each layer relative to the music (RMS, dB)
    target_db = {'music': 0.0, 'sea': -9.0, 'bike': -10.0, 'gulls': -12.0, 'clacks': -14.0}
    ref = None
    mix = 0
    for k in ('music', 'sea', 'bike', 'gulls', 'clacks'):
        x = layers[k]
        rms = np.sqrt(np.mean(x ** 2)) + 1e-12
        if k == 'clacks':
            rms = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) * 0.25 + 1e-12
        if ref is None:
            ref = rms
        g = ref / rms * 10 ** (target_db[k] / 20)
        mix = mix + x * g
        print(f"  layer {k:7s} rms {20 * np.log10(rms):6.1f} dB gain {20 * np.log10(g):6.1f} dB")
    # fade in / out
    n = len(mix)
    fade = np.ones(n)
    fi = int(1.2 * SR)
    fo = int(2.0 * SR)
    fade[:fi] = np.linspace(0, 1, fi) ** 2
    fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    mix *= fade[:, None]
    mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.3) * 0.89
    wavfile.write(out_wav, SR, (mix * 32767).astype(np.int16))
    print("WROTE", out_wav, f"{T:.2f}s")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
