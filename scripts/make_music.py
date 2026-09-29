#!/usr/bin/env python3
"""
Synthesises an original, royalty-free soundtrack for the ad (no samples, no licences needed).
120 BPM, I–V–vi–IV progression, with sound effects synced to src/timeline.json.

    python3 scripts/make_music.py        ->  public/music.wav

Needs numpy.  Re-run after changing scene timings or adding real photos.
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 44100
FPS = 30
BPM = 120
BEAT = 60 / BPM

timeline = json.loads((ROOT / "src/timeline.json").read_text())
cfg = (ROOT / "src/config.ts").read_text()
m = re.search(r"realPhotos:\s*string\[\]\s*=\s*\[(.*?)\]", cfg, re.S)
photo_count = len(re.findall(r"['\"][^'\"]+['\"]", m.group(1))) if m else 0

# scene start times (seconds), mirroring Root.tsx
starts, t = {}, 0
for s in timeline["scenes"]:
    starts[s["id"]] = t
    t += s["duration"]
    if s["id"] == "reveal" and photo_count:
        starts["proof"] = t
        t += timeline["proofSceneDuration"]
TOTAL_FRAMES = t
DUR = TOTAL_FRAMES / FPS
N = int(DUR * SR) + SR  # 1 s tail, trimmed later
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(7)


def sec(frame):
    return frame / FPS


def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i : i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i : i + len(sig)] += sig * gain * (1 + min(0, pan))


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a=0.005, d=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / d)
    return e


def pluck(freq, dur=0.6, bright=0.5):
    """Karplus–Strong plucked string."""
    n = int(dur * SR)
    p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * (0.994 + 0.004 * bright)
    return out * env(n, 0.002, dur * 0.6)


def sine(freq, dur, a=0.005, d=0.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * env(n, a, d)


def pad(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for nt in notes:
        f = midi(nt)
        for det in (-0.12, 0.0, 0.12):
            ph = 2 * np.pi * f * (1 + det / 100) * t
            s += np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    fade = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4)
    return s * fade / (len(notes) * 3)


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def noise_burst(dur, decay, hp=True):
    n = int(dur * SR)
    x = rng.uniform(-1, 1, n)
    if hp:
        x = np.diff(np.concatenate([[0], x]))
    return x * np.exp(-np.arange(n) / SR / decay)


def clap():
    s = np.zeros(int(0.25 * SR))
    for k, off in enumerate((0, 0.012, 0.024)):
        b = noise_burst(0.2, 0.05 if k == 2 else 0.01)
        i = int(off * SR)
        s[i : i + len(b)] += b[: len(s) - i]
    return s * 0.5


def whoosh(dur=0.5, up=True):
    n = int(dur * SR)
    x = rng.uniform(-1, 1, n)
    # simple one-pole low-pass with sweeping cutoff
    cut = np.linspace(0.02, 0.35, n) if up else np.linspace(0.35, 0.02, n)
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc += cut[i] * (x[i] - acc)
        y[i] = acc
    shape = np.sin(np.linspace(0, np.pi, n)) ** 2
    return y * shape * 2.5


def pop(f0=500, f1=1400):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)


def chime(root=84):
    s = np.zeros(int(1.2 * SR))
    for k, iv in enumerate((0, 4, 7, 12)):
        tone = sine(midi(root + iv), 1.0, 0.002, 0.35) + 0.3 * sine(midi(root + iv + 12), 1.0, 0.002, 0.2)
        i = int(k * 0.06 * SR)
        s[i : i + len(tone)] += tone[: len(s) - i]
    return s * 0.25


def tick():
    return noise_burst(0.03, 0.004) * 0.6 + sine(2200, 0.03, 0.0005, 0.006) * 0.3


# ---------- music ----------
# Key of C: C – G – Am – F  (I–V–vi–IV), one chord per bar (2 s)
CHORDS = [
    (48, [60, 64, 67]),
    (43, [59, 62, 67]),
    (45, [60, 64, 69]),
    (41, [60, 65, 69]),
]
bar = BEAT * 4
n_bars = int(np.ceil(DUR / bar))
drop = sec(starts["memories"])  # beat comes in after the hook
print_s, print_e = sec(starts["print"]), sec(starts["print"] + timeline["scenes"][3]["duration"])
end_s = sec(starts["cta"])

for b in range(n_bars):
    t0 = b * bar
    bass, tri = CHORDS[b % 4]
    add(pad(tri, bar + 0.2), t0, 0.16)
    # arpeggio in 8ths
    arp = tri + [tri[0] + 12, tri[1] + 12, tri[2] + 12, tri[1] + 12, tri[0] + 12]
    for k in range(8):
        tt = t0 + k * BEAT / 2
        if tt >= DUR:
            break
        note = arp[k % len(arp)] + 12
        add(pluck(midi(note), 0.5, 0.6), tt, 0.28, pan=(-0.3 if k % 2 else 0.3))
    for k in range(4):
        tt = t0 + k * BEAT
        if tt < drop or tt >= DUR - 0.3:
            continue
        add(kick(), tt, 0.55)
        add(sine(midi(bass - 12), BEAT * 0.9, 0.01, 0.35) * 0.9, tt, 0.35)
        if k in (1, 3):
            add(clap(), tt, 0.35)
        if print_s <= tt < print_e:
            add(noise_burst(0.05, 0.01), tt + BEAT / 2, 0.12, pan=0.4)

# riser into the drop

riser = whoosh(1.0, True)
add(riser, drop - 1.0, 0.35)

# ---------- sfx ----------
add(pop(300, 900), 0.08, 0.5)  # hook figure pops
add(chime(84), sec(14), 0.5)
for sid in ("steps", "print", "reveal", "gift", "cta") + (("proof",) if photo_count else ()):
    add(whoosh(0.45, False), sec(starts[sid]) - 0.12, 0.35)
# tool swaps during printing
p = timeline["print"]
for f in range(p["start"], p["end"], p["swapEvery"]):
    add(tick(), sec(starts["print"] + f), 0.35, pan=rng.uniform(-0.5, 0.5))
add(chime(88), sec(starts["print"] + p["end"]), 0.7)  # print finished
add(chime(84), sec(starts["reveal"]) + 0.05, 0.5)
for d in (26, 40, 54):
    add(pop(700, 1500), sec(starts["reveal"] + d + 6), 0.3)
for d in (18, 24, 30):
    add(pop(400, 1100), sec(starts["gift"] + d), 0.35)
add(chime(84), sec(starts["cta"]) + 0.1, 0.6)
add(pop(500, 1300), sec(starts["cta"] + 44), 0.45)

# final ring-out chord
add(pad([60, 64, 67, 72], 2.5), end_s + 2.2, 0.22)

# ---------- master ----------
n_out = int(DUR * SR)
mix = np.stack([L[:n_out], R[:n_out]], axis=1)
fade = np.ones(n_out)
fl = int(0.6 * SR)
fade[-fl:] = np.linspace(1, 0, fl)
mix *= fade[:, None]
mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89  # ~ -1 dBFS peak
pcm = (mix * 32767).astype(np.int16)
out = ROOT / "public/music.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {out}  ({DUR:.1f}s, photos={photo_count})")
