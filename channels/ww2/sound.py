"""WW2 channel sound palette: a documentary score toolkit, the effects library and the mixer. Everything is original
and synthesized here with numpy/scipy: no samples, no recordings, no quoted melodies.

Every generator is deterministic (each one seeds its own RNG from its name and `seed`) and returns float64 audio at
SR = 48 kHz, peak-normalised to 0.9: mono as shape (n,), stereo as shape (n, 2). Levels are set in the mix.

Music (any length; the patterns loop by bars and the cue fades on its last 0.8 s):
    tension(dur)      low string drone, a ticking pulse, timpani swells into each 4-bar phrase
    march(dur)        military snare, bass drum, low brass ostinato and chords (Blitzkrieg, D-Day)
    somber(dur)       solo piano over a soft pad (the aftermath; with pad=False, piano alone)
    low_tone(dur)     the single low tone for the Holocaust chapter (script: "the music drops to a single low tone")
    triumph(dur)      a slow brass-and-strings chorale with bells, bittersweet (a borrowed minor chord): V-E Day
    drum_hit()        the stinger for "the biggest shock": timpani, bass drum, crash and a low brass stab
    (the hard cut to silence is Mix.cut)

Effects (MUSIC and SFX map the names to the functions, so a scene's engine.cue("tank", ...) names one of them):
    gun_boom, artillery, artillery_barrage, tank, plane_drone, dive_whine, explosion, rifle_crack, sea_waves, blizzard,
    radio_static, voice_crackle, morse, typewriter, stamp, page_whoosh, crowd_cheer, clock_tick, train, door_slam

The mix (as the Shorts): music ducks ~10 dB and ambience ~8 dB under the narration (20 ms attack, 300 ms release);
effects are not ducked. Master: a true-peak look-ahead limiter, then ffmpeg loudnorm in two passes to -14 LUFS with
peaks at or under -1 dBTP; 48 kHz 16-bit stereo, no metadata.

    m = Mix(total)
    m.music(tension(12), 0.0, -16)                    # x, at, dB (fade_in/fade_out optional)
    m.sfx(gun_boom(), 11.2, -4, pan=-0.2)
    m.cut(11.8, 12.6)                                 # hard cut to silence (music, effects, ambience)
    m.amb(sea_waves(8), 12.6, -20, fade_in=1)
    m.master("out/ww2/ep01/mix.wav", voice=v)         # v: the mono narration track at SR, same length or shorter

    python channels/ww2/sound.py          # writes out/ww2/style/sound_demo.wav (~40 s) and sfx_reel.wav
"""
import json
import os
import re
import subprocess
import sys
import wave
import zlib

import numpy as np
from scipy import signal
from scipy.ndimage import minimum_filter1d

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SR = 48000
STYLE_OUT = os.path.join(ROOT, "out", "ww2", "style")


# ---------------------------------------------------------------- helpers

def _rng(name, seed=0):
    return np.random.default_rng(zlib.crc32(f"ww2:{name}:{seed}".encode()))


def _n(sec):
    return max(1, int(round(sec * SR)))


def _t(n):
    return np.arange(n) / SR


def _sos(kind, f, order=4):
    return signal.butter(order, f, btype=kind, fs=SR, output="sos")


def _lp(x, f, order=4):
    return signal.sosfilt(_sos("lowpass", min(f, SR / 2 - 200), order), x, axis=0)


def _hp(x, f, order=4):
    return signal.sosfilt(_sos("highpass", f, order), x, axis=0)


def _bp(x, lo, hi, order=2):
    return signal.sosfilt(_sos("bandpass", (lo, min(hi, SR / 2 - 200)), order), x, axis=0)


def _reso(x, f, q):
    """A two-pole resonator (a formant, a body mode)."""
    w = 2 * np.pi * f / SR
    r = np.exp(-np.pi * f / q / SR)
    return signal.lfilter([1 - r], [1, -2 * r * np.cos(w), r * r], x, axis=0)


def _dec(n, tau, attack=0.002):
    t = _t(n)
    return np.minimum(1, t / attack) * np.exp(-t / tau) if attack else np.exp(-t / tau)


def _ramp(n, a, b):
    """1 inside, with linear ramps of a and b seconds at the ends."""
    e = np.ones(n)
    ia, ib = min(n, _n(a)) if a else 0, min(n, _n(b)) if b else 0
    if ia:
        e[:ia] = np.linspace(0, 1, ia)
    if ib:
        e[n - ib:] *= np.linspace(1, 0, ib)
    return e


def _place(out, x, at, gain=1.0):
    i = int(round(at * SR))
    if i < 0:
        x, i = x[-i:], 0
    if i >= len(out) or len(x) == 0:
        return
    m = min(len(x), len(out) - i)
    if out.ndim == 2 and x.ndim == 1:
        out[i:i + m] += x[:m, None] * gain
    else:
        out[i:i + m] += x[:m] * gain


def _midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _saw(f, n, phase=0.0):
    """A naive sawtooth (the music filters it well below where its aliasing would show). f: Hz or Hz per sample."""
    ph = (np.cumsum(np.broadcast_to(f, (n,))) / SR + phase) % 1.0
    return 2 * ph - 1


def _sweep(f, phase=0.0):
    return np.sin(2 * np.pi * np.cumsum(f) / SR + phase)


def _lfo(n, rate, depth, r):
    """A slow random wobble (smoothed noise), for vibrato and gusts."""
    k = max(4, int(n / SR * rate) + 4)
    pts = r.uniform(-1, 1, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts) * depth


def _pan(x, p):
    """Mono -> stereo, constant power; p -1 (left) .. +1 (right)."""
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1) * np.sqrt(2)


def _norm(x, peak=0.9):
    m = np.max(np.abs(x))
    return x / m * peak if m > 0 else x


def _verb(x, mix=0.25, size=1.0, damp=6000, seed=0):
    """A Schroeder reverb (four combs, two all-passes) with a tail; stereo in -> decorrelated stereo out."""
    st = x if x.ndim == 2 else np.stack([x, x], 1)
    pad = np.concatenate([st, np.zeros((_n(1.8 * size), 2))])
    out = np.empty_like(pad)
    for ch in range(2):
        wet = np.zeros(len(pad))
        for d, g in ((1687, 0.82), (1753, 0.81), (1615, 0.80), (1541, 0.79)):
            d = int(d * size) + 23 * ch + seed % 7
            a = np.zeros(d + 1)
            a[0], a[d] = 1, -g
            wet += signal.lfilter([1.0], a, pad[:, ch])
        for d, g in ((245, 0.5), (603, 0.5)):
            d += 11 * ch
            b = np.zeros(d + 1)
            b[0], b[d] = -g, 1
            a = np.zeros(d + 1)
            a[0], a[d] = 1, -g
            wet = signal.lfilter(b, a, wet)
        out[:, ch] = pad[:, ch] * (1 - mix) + _lp(wet, damp, 2) * 0.1 * mix
    return out


def _bars(dur, bpm, beats=4):
    """How many whole bars cover `dur` (at least one)."""
    return max(1, int(np.ceil(dur / (60.0 / bpm * beats))))


def _finish(x, dur, fade_in=0.0, fade_out=0.8):
    x = x[: _n(dur)]
    x = np.pad(x, ((0, _n(dur) - len(x)),) + ((0, 0),) * (x.ndim - 1))
    e = _ramp(len(x), fade_in, fade_out)
    return _norm(x * (e[:, None] if x.ndim == 2 else e))


# ---------------------------------------------------------------- instruments

def strings(midis, dur, seed=0, bright=1100, attack=1.5, vib=0.004, voices=5):
    """A string section on sustained notes: detuned saws, slow vibrato, a soft bow attack. Stereo."""
    n = _n(dur)
    r = _rng("strings", seed)
    out = np.zeros((n, 2))
    for m in midis:
        f = _midi(m)
        for v in range(voices):
            det = 1 + r.uniform(-1, 1) * 0.004
            fm = f * det * (1 + _lfo(n, 5.5, vib, r) * np.sin(2 * np.pi * r.uniform(4.6, 5.6) * _t(n)))
            out += _pan(_saw(fm, n, r.uniform()), r.uniform(-0.7, 0.7)) / voices
    out = _lp(_hp(out, 50), bright)
    out = out + _bp(_rng("bow", seed).uniform(-1, 1, (n, 2)), 1500, 4000) * 0.01      # bow hair
    return out * _ramp(n, attack, min(1.0, dur / 3))[:, None]


def pad(midis, dur, seed=0, bright=900, attack=2.0):
    """A soft pad: sines plus a little filtered saw, slowly breathing. Stereo."""
    n = _n(dur)
    r = _rng("pad", seed)
    t = _t(n)
    out = np.zeros((n, 2))
    for m in midis:
        f = _midi(m)
        for ch, det in ((0, 0.998), (1, 1.002)):
            out[:, ch] += np.sin(2 * np.pi * f * det * t + r.uniform(0, 6)) + 0.3 * _lp(_saw(f * det, n), bright)
    out *= (1 + 0.15 * np.sin(2 * np.pi * 0.07 * t + r.uniform(0, 6)))[:, None]
    return out * _ramp(n, attack, min(1.5, dur / 3))[:, None]


def timpani(midi=38, vel=1.0, seed=0, dur=2.5):
    """A timpano: membrane modes (1, 1.5, 1.99, 2.44) with a small pitch drop and a felt thump."""
    n = _n(dur)
    t = _t(n)
    f = _midi(midi)
    out = np.zeros(n)
    for ratio, amp, tau in ((1, 1.0, 1.1), (1.5, 0.5, 0.6), (1.99, 0.35, 0.45), (2.44, 0.2, 0.3)):
        fr = f * ratio * (1 + 0.03 * np.exp(-t / 0.04))
        out += amp * _sweep(fr) * np.exp(-t / (tau * (0.6 + 0.4 * vel)))
    thump = _lp(_rng("timp", seed).uniform(-1, 1, n), 300 + 900 * vel) * _dec(n, 0.03, 0.001) * 1.5
    return (out + thump) * vel


def timpani_roll(midi, dur, seed=0, start_vel=0.15, end_vel=0.9):
    """A crescendo roll: alternating sticks about 14 strokes a second."""
    out = np.zeros(_n(dur + 2.5))
    r = _rng("roll", seed)
    k, t = 0, 0.0
    while t < dur:
        vel = start_vel + (end_vel - start_vel) * (t / dur) ** 1.6
        _place(out, timpani(midi, vel * r.uniform(0.85, 1.0), seed + k, 1.2), t)
        t += 1 / 14 * r.uniform(0.9, 1.1)
        k += 1
    return out


def snare(vel=1.0, seed=0):
    """A field snare: the shell tone, the wires (band-passed noise) and a stick click."""
    n = _n(0.35)
    t = _t(n)
    r = _rng("snare", seed)
    shell = (np.sin(2 * np.pi * 185 * t) + 0.5 * np.sin(2 * np.pi * 330 * t)) * np.exp(-t / 0.05)
    wires = _bp(r.uniform(-1, 1, n), 1800, 9000) * np.exp(-t / (0.08 + 0.06 * vel))
    click = _hp(r.uniform(-1, 1, n), 3000) * np.exp(-t / 0.004)
    return (shell * 0.6 + wires * 1.2 + click * 0.5) * vel * np.minimum(1, t / 0.0007)


def bass_drum(vel=1.0, seed=0):
    n = _n(0.9)
    t = _t(n)
    body = _sweep(58 + 70 * np.exp(-t / 0.03)) * np.exp(-t / 0.3)
    beater = _lp(_rng("bd", seed).uniform(-1, 1, n), 1500) * np.exp(-t / 0.012) * 0.6
    return (body + beater) * vel


def crash(vel=1.0, seed=0, dur=3.0):
    """A suspended cymbal crash: dense inharmonic partials and bright noise, long decay. Stereo."""
    n = _n(dur)
    t = _t(n)
    r = _rng("crash", seed)
    out = np.zeros((n, 2))
    for ch in range(2):
        noise = _hp(r.uniform(-1, 1, n), 3500) * np.exp(-t / 1.1)
        ring = sum(np.sin(2 * np.pi * r.uniform(3000, 9000) * t + r.uniform(0, 6)) for _ in range(12)) / 12
        out[:, ch] = noise + ring * np.exp(-t / 0.8) * 0.3
    return out * vel * np.minimum(1, t / 0.003)[:, None]


def brass(midi, dur, vel=1.0, seed=0, warm=False):
    """A brass-like synth: three detuned saws through a filter that opens on the attack ("blat") and settles."""
    n = _n(dur + 0.25)
    t = _t(n)
    r = _rng("brass", seed + midi)
    f = _midi(midi) * (1 + 0.003 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.4))
    s = sum(_saw(f * d, n, r.uniform()) for d in (0.997, 1.0, 1.003)) / 3
    lo, hi = (500, 1600) if warm else (700, 2600 + 1200 * vel)
    bright = np.exp(-t / 0.12) * 0.7 + 0.3 * vel
    out = _lp(s, lo) * (1 - bright) + _lp(s, hi) * bright
    gate = np.minimum(1, t / 0.03) * np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.08))
    return out * gate * vel


def piano(midi, dur, vel=0.7, seed=0):
    """A piano note: inharmonic partials on two slightly detuned strings, a hammer knock, the damper at note-off."""
    f = _midi(midi)
    tau0 = float(np.clip(4.0 * np.sqrt(220 / f), 0.8, 7.0))
    n = _n(dur + 0.3)
    t = _t(n)
    out = np.zeros(n)
    for k in range(1, 13):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)
        if fk > 12000:
            break
        amp = 1 / k ** (1.7 - 0.8 * vel)
        tau = tau0 / (1 + 0.5 * (k - 1))
        for det in (-0.0004, 0.0004):
            out += amp * np.sin(2 * np.pi * fk * (1 + det) * t + k) * np.exp(-t / tau) * 0.5
    hammer = _lp(_rng("hammer", seed + midi).uniform(-1, 1, n), 1500 + 3000 * vel) * np.exp(-t / 0.006) * 0.15
    damper = np.where(t < dur, 1.0, np.exp(-(t - dur) / 0.07))
    return (out + hammer) * damper * vel * np.minimum(1, t / 0.0015)


def bell(midi, dur=4.0, vel=1.0):
    """A tubular bell (partials of a struck tube)."""
    n = _n(dur)
    t = _t(n)
    f = _midi(midi)
    out = np.zeros(n)
    for ratio, amp, tau in ((1, 1, 2.5), (2.0, 0.6, 1.8), (2.76, 0.5, 1.2), (5.4, 0.25, 0.6), (8.9, 0.1, 0.3)):
        out += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    return out * vel * np.minimum(1, t / 0.002)


def tick(f=3200, seed=0, vel=1.0):
    """A dry wooden tick (the clock and the tension pulse)."""
    n = _n(0.08)
    x = _reso(_rng("tick", seed).uniform(-1, 1, n) * _dec(n, 0.002, 0.0003), f, 18)
    return _norm(x) * vel


# ---------------------------------------------------------------- music cues

D = 38            # the score's home: D (D2 = midi 38). Minor for the war, major for V-E Day.


def tension(dur, seed=0, bpm=100, tick_on=True):
    """Low strings on D and A, a dissonant high harmonic creeping in, a ticking pulse on every beat, a low pizzicato
    on each downbeat, and a timpani swell rolling into the start of every 4-bar phrase (and into the cue's end)."""
    beat = 60 / bpm
    bars = _bars(dur, bpm)
    total = bars * 4 * beat
    n = _n(total + 3)
    out = np.zeros((n, 2))
    _place(out, strings([D, D + 7, D + 12], total + 1, seed, bright=1300, attack=2.5), 0, 0.55)
    _place(out, strings([D + 25], total * 0.6 + 1, seed + 1, bright=3000, attack=total * 0.5, voices=3),
           total * 0.4, 0.06)                                                            # E-flat harmonic: unease
    for b in range(bars * 4):
        at = b * beat
        if tick_on:
            _place(out, _pan(tick(3400 if b % 4 else 2600, b, 0.9 if b % 4 == 0 else 0.6), 0.25), at, 0.10)
        if b % 4 == 0:
            p = _lp(_hp(strings([D + (7 if (b // 4) % 4 == 3 else 0)], 0.5, seed + b, 700, 0.005, 0, 3), 40), 600)
            _place(out, p * np.exp(-_t(len(p)) / 0.18)[:, None], at, 0.5)              # pizzicato
    for ph in range(4, bars + 1, 4):                                                     # swells into phrases
        end = ph * 4 * beat
        _place(out, _pan(timpani_roll(D, 2 * 4 * beat * 0.5, seed + ph), -0.15), end - 4 * beat, 0.25)
        _place(out, _pan(timpani(D, 1.0, seed + ph), -0.15), end, 0.3)
    if bars % 4:
        _place(out, _pan(timpani_roll(D, min(dur, 2.5), seed + 99), -0.15), dur - min(dur, 2.5), 0.22)
    return _finish(_verb(out, 0.3, 1.1, seed=seed), dur)


# a field-drum cadence on a 16th grid: velocity per 16th (0 = rest)
_SNARE = [1.0, 0, .45, .5, .9, 0, .45, 0, 1.0, 0, .45, .5, .9, .4, .45, .5]
_SNARE_ROLL = [1.0, .5, .55, .6, .65, .7, .75, .8, .85, .9, .92, .95, .97, 1.0, 1.0, 0]
_MARCH_CHORDS = [(D, D + 3, D + 7), (D - 4, D, D + 3), (D - 7, D - 4, D), (D - 5, D - 1, D + 2)]   # Dm Bb Gm A
_MARCH_BASS = [[0, 0, 0, 3, 0, 0, -2, -5], [-4, -4, -4, -1, -4, -4, -2, -5],
               [-7, -7, -7, -4, -7, -7, -5, -4], [-5, -5, -5, -1, -5, -5, -3, -1]]


def march(dur, seed=0, bpm=112):
    """The drive: field snare (a roll every 4th bar), bass drum on 1 and 3, a low brass ostinato in eighths and brass
    chords on Dm - Bb - Gm - A, a crash every 8 bars. It builds: drums alone for 2 bars, then the bass, then the
    chords."""
    beat = 60 / bpm
    s16 = beat / 4
    bars = _bars(dur, bpm)
    total = bars * 4 * beat
    out = np.zeros((_n(total + 3), 2))
    sn = [snare(v, k) for k, v in enumerate((1.0, 0.8, 0.6, 0.45))]
    r = _rng("march", seed)
    for b in range(bars):
        bar0 = b * 4 * beat
        pat = _SNARE_ROLL if b % 4 == 3 else _SNARE
        for i, v in enumerate(pat):
            if v:
                hit = sn[min(3, int((1 - v) * 4))] * v * r.uniform(0.9, 1.05)
                _place(out, _pan(hit, 0.2), bar0 + i * s16 + r.normal(0, 0.003), 0.22)
                if i in (0, 8) and pat is _SNARE:                                          # flams on 1 and 3
                    _place(out, _pan(sn[3] * 0.4, 0.2), bar0 + i * s16 - 0.025, 0.22)
        for i in (0, 2):
            _place(out, _pan(bass_drum(1.0 if i == 0 else 0.8, b), 0.0), bar0 + i * beat, 0.22)
        if b % 8 == 0 and b:
            _place(out, crash(0.8, b), bar0, 0.10)
        if b >= 2:
            for i, step in enumerate(_MARCH_BASS[b % 4]):
                _place(out, _pan(brass(D + step, s16 * 1.6, 0.9, b * 8 + i), -0.1), bar0 + i * 2 * s16, 0.42)
        if b >= 4:
            for k, m in enumerate(_MARCH_CHORDS[b % 4]):
                x = brass(m + 12, 4 * beat * 0.92, 0.7, b * 3 + k)
                _place(out, _pan(x, (-0.4, 0.0, 0.4)[k]), bar0, 0.24)
    return _finish(_verb(out, 0.18, 0.9, seed=seed), dur, fade_out=0.6)


_SOMBER = [(D, (D + 12, D + 15, D + 19), 74), (D - 4, (D + 8, D + 12, D + 15), 72),
           (D - 7, (D + 5, D + 8, D + 12), 70), (D - 5, (D + 7, D + 11, D + 14), 69)]           # Dm Bb Gm A


def somber(dur, seed=0, bpm=60, with_pad=True):
    """Solo piano, slow, in D minor (Dm - Bb - Gm - A, one chord a bar): a low octave in the left hand, a broken
    chord in the right, and a falling melody note on beat 3 of every other bar; a soft pad underneath."""
    beat = 60 / bpm
    bars = _bars(dur, bpm)
    total = bars * 4 * beat
    out = np.zeros((_n(total + 4), 2))
    r = _rng("somber", seed)
    for b in range(bars):
        root, chord, mel = _SOMBER[b % 4]
        bar0 = b * 4 * beat
        _place(out, _pan(piano(root, 4 * beat, 0.4, b) + piano(root + 12, 4 * beat, 0.4, b), -0.3), bar0)
        for i, m in enumerate((chord + chord[1:2])[:4]):
            _place(out, _pan(piano(m, beat * 1.8, r.uniform(0.32, 0.42), b * 4 + i), 0.15),
                   bar0 + i * beat + r.normal(0, 0.008))
        if b % 2 == 1:
            _place(out, _pan(piano(mel, beat * 2, 0.55, b), 0.25), bar0 + 2 * beat + 0.02)
    if with_pad:
        p = pad([D + 12, D + 19, D + 24], total + 1, seed, bright=600, attack=3)
        _place(out, p, 0, 0.12)
    return _finish(_verb(out, 0.38, 1.4, damp=5000, seed=seed), dur, fade_in=0.05, fade_out=1.2)


def low_tone(dur, seed=0):
    """The Holocaust chapter's music: a single low D, barely moving (a slow swell, no rhythm, no melody)."""
    n = _n(dur)
    t = _t(n)
    r = _rng("low_tone", seed)
    f = _midi(D - 12) * (1 + _lfo(n, 0.2, 0.0015, r))
    x = _sweep(f) + 0.35 * _sweep(2 * f) + 0.08 * _lp(_saw(f, n), 300)
    swell = 0.8 + 0.2 * np.sin(2 * np.pi * t / 9.0 - np.pi / 2)
    st = _verb(_pan(x * swell, 0.0), 0.3, 1.5, damp=2000, seed=seed)
    return _finish(st, dur, fade_in=min(3.0, dur / 3), fade_out=min(3.0, dur / 3))


_TRIUMPH = [(D, (D + 12, D + 16, D + 19)), (D - 3, (D + 9, D + 12, D + 16)),               # D, A/C#
            (D - 3 - 2, (D + 7, D + 11, D + 14)), (D - 7, (D + 7, D + 11, D + 14)),        # Bm, G
            (D - 5, (D + 12, D + 16, D + 19)), (D - 7, (D + 7, D + 10, D + 14)),           # D/A, Gm (borrowed: sad)
            (D - 5, (D + 7, D + 9, D + 13)), (D, (D + 12, D + 16, D + 21))]                # A, D


def triumph(dur, seed=0, bpm=66):
    """V-E Day: a slow chorale (one chord a bar) for warm brass over strings, D major with a borrowed G minor in
    each 8-bar phrase so the victory sounds earned and sad; a tubular bell on every other bar, timpani on phrase
    starts and a soft snare roll into them."""
    beat = 60 / bpm
    bars = _bars(dur, bpm)
    total = bars * 4 * beat
    out = np.zeros((_n(total + 5), 2))
    for b in range(bars):
        root, chord = _TRIUMPH[b % 8]
        bar0 = b * 4 * beat
        _place(out, strings([root - 12, root] + list(chord), 4 * beat + 0.4, seed + b, bright=1800, attack=0.5,
                            voices=3), bar0, 0.35)
        for k, m in enumerate(chord):
            _place(out, _pan(brass(m, 4 * beat * 0.95, 0.65, b * 3 + k, warm=True), (-0.35, 0.05, 0.35)[k]),
                   bar0 + 0.03 * k, 0.22)
        if b % 2 == 0:
            _place(out, _pan(bell(chord[-1] + 12, 4.0, 0.8), 0.3), bar0, 0.12)
        if b % 8 == 0:
            _place(out, _pan(timpani(D, 0.9, b), -0.2), bar0, 0.35)
        if b % 8 == 7:
            sr = np.zeros(_n(4 * beat))
            for i in range(int(4 * beat * 16)):
                _place(sr, snare(0.15 + 0.35 * i / (4 * beat * 16), i), i / 16)
            _place(out, _pan(sr, 0.2), bar0, 0.12)
    return _finish(_verb(out, 0.32, 1.3, seed=seed), dur, fade_in=0.3, fade_out=1.5)


def drum_hit(seed=0):
    """The stinger for "the biggest shock": timpani and bass drum together, a crash, a short low brass stab on a
    D minor cluster (D, E-flat, A), ringing out about 3 s."""
    out = np.zeros((_n(4.0), 2))
    _place(out, _pan(timpani(D, 1.0, seed) + timpani(D - 5, 0.8, seed + 1), -0.1), 0, 0.7)
    _place(out, _pan(bass_drum(1.0, seed) * 1.2, 0), 0, 0.6)
    _place(out, crash(1.0, seed), 0.005, 0.25)
    for k, m in enumerate((D, D + 1, D + 7, D + 12)):
        _place(out, _pan(brass(m, 0.45, 1.0, seed + k), (-0.3, 0.3, -0.1, 0.1)[k]), 0, 0.22)
    return _norm(_verb(out, 0.35, 1.3, seed=seed)[: _n(4.0)] * _ramp(_n(4.0), 0, 0.6)[:, None])


# ---------------------------------------------------------------- effects

def gun_boom(seed=0):
    """A battleship's main gun: a muzzle crack, a huge low boom, a rolling harbour echo off the walls."""
    n = _n(4.5)
    t = _t(n)
    r = _rng("gun_boom", seed)
    crack = _hp(r.uniform(-1, 1, n), 900) * _dec(n, 0.012, 0.0005)
    boom = np.tanh(2.5 * _sweep(28 + 70 * np.exp(-t / 0.07)) * np.exp(-t / 0.7))
    body = _lp(r.uniform(-1, 1, n), 500) * _dec(n, 0.35, 0.002) * 1.6
    rumble = _lp(r.uniform(-1, 1, n), 140) * _dec(n, 1.4, 0.05) * 2.0
    x = crack * 0.5 + boom * 0.9 + body + rumble
    echo = np.zeros(n)
    for d, g in ((0.32, 0.35), (0.85, 0.22), (1.6, 0.12)):
        _place(echo, _lp(x, 900 / (1 + d)), d, g)
    return _norm(x + echo)


def artillery(seed=0, distance=1.0):
    """One distant gun or shell: a muffled thump with a rolling tail (distance 0.5 near .. 2 far)."""
    n = _n(3.0)
    t = _t(n)
    r = _rng("artillery", seed)
    thump = _sweep(35 + 40 * np.exp(-t / 0.05)) * np.exp(-t / 0.4)
    roll = _lp(r.uniform(-1, 1, n), 200) * _dec(n, 0.9, 0.03) * 1.5
    x = _lp(thump + roll + _lp(r.uniform(-1, 1, n), 1200) * _dec(n, 0.08, 0.002) * 0.6, 900 / distance)
    return _norm(x)


def artillery_barrage(dur, seed=0, rate=0.9):
    """Distant guns over a span: thumps at random, near and far, left and right. Stereo."""
    r = _rng("barrage", seed)
    out = np.zeros((_n(dur + 3), 2))
    t = r.uniform(0, 0.4)
    k = 0
    while t < dur:
        dist = r.uniform(0.8, 2.2)
        _place(out, _pan(artillery(seed * 100 + k, dist), r.uniform(-0.8, 0.8)), t, 1 / dist)
        t += r.exponential(1 / rate) + 0.15
        k += 1
    return _finish(out, dur, 0.05, 0.6)


def tank(dur, seed=0, speed=1.0):
    """A tank on the move: a lumpy diesel rumble, track links clanking at the sprocket, the odd squeal."""
    n = _n(dur)
    t = _t(n)
    r = _rng("tank", seed)
    f0 = 38 * speed * (1 + _lfo(n, 0.5, 0.05, r))
    eng = _saw(f0, n) + 0.6 * _saw(2 * f0 * 1.003, n) + 0.3 * np.sign(_sweep(f0 / 2))
    eng = _lp(eng, 260) + _lp(r.uniform(-1, 1, n), 400) * 0.3
    eng *= 1 + 0.25 * np.sin(2 * np.pi * f0 / 4 * t)
    clank = np.zeros(n)
    rate = 9 * speed
    k, tt = 0, 0.0
    while tt < dur:
        m = _n(0.06)
        tm = _t(m)
        c = sum(np.sin(2 * np.pi * r.uniform(900, 4200) * tm) for _ in range(3)) * np.exp(-tm / 0.02)
        c += _hp(r.uniform(-1, 1, m), 2000) * np.exp(-tm / 0.006)
        _place(clank, c * r.uniform(0.5, 1.0), tt)
        tt += 1 / rate * r.uniform(0.8, 1.2)
        k += 1
    squeal = np.sin(2 * np.pi * (2600 + 200 * np.sin(2 * np.pi * 0.7 * t)) * t) * np.clip(_lfo(n, 0.6, 3, r) - 2.2,
                                                                                            0, 1) * 0.15
    return _finish(_hp(eng, 45) + _bp(clank, 600, 6000) * 0.35 + squeal, dur, 0.4, 0.6)


def plane_drone(dur, seed=0, count=1, pass_by=True):
    """Piston aircraft: engine firing harmonics and the propeller beat; a pass-by bends the pitch (Doppler) and
    swells. count > 1 is a formation, each plane a little detuned and offset. Stereo."""
    n = _n(dur)
    t = _t(n)
    out = np.zeros((n, 2))
    r = _rng("plane", seed)
    for p in range(count):
        mid = dur * (0.5 + (r.uniform(-0.25, 0.25) if count > 1 else 0))
        u = (t - mid) / (dur * 0.35)
        dopp = 1 + 0.06 * -np.tanh(u * 2) if pass_by else np.ones(n)
        f = 85 * r.uniform(0.94, 1.06) * dopp * (1 + _lfo(n, 0.3, 0.004, r))
        x = sum(_sweep(f * h, r.uniform(0, 6)) / h ** 0.8 for h in range(1, 14))
        x *= 1 + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 0.5) / SR)                   # the prop beat
        x = _lp(x + _bp(r.uniform(-1, 1, n), 300, 2500) * 0.6, 1800)
        amp = 1 / (1 + u ** 2) if pass_by else np.ones(n)
        out += _pan(x * amp, np.clip(np.tanh(u) * 0.8, -0.9, 0.9) if pass_by else r.uniform(-0.5, 0.5))
    return _finish(out, dur, 0.3, 0.5)


def dive_whine(dur=2.6, seed=0):
    """A dive bomber going down: a siren-like whine climbing as the plane speeds up, under a rising engine roar.
    It stays loud to the end (follow it with explosion())."""
    n = _n(dur)
    t = _t(n)
    r = _rng("dive", seed)
    u = t / dur
    f = 380 * (1100 / 380) ** (u ** 1.3)
    whine = _sweep(f * (1 + 0.006 * np.sin(2 * np.pi * 7 * t))) + 0.4 * _sweep(2.01 * f)
    whine = _bp(whine + 0.3 * np.sign(_sweep(f)), 300, 4000)
    roar = _bp(r.uniform(-1, 1, n), 150, 1500) * (0.3 + u)
    eng = sum(_sweep(90 * (1 + 0.5 * u) * h) / h for h in range(1, 8)) * 0.4
    return _norm((whine * (0.3 + 0.7 * u ** 1.5) + roar * 0.6 + eng * 0.5) * _ramp(n, 0.25, 0.01))


def explosion(seed=0, size=1.0, distance=1.0):
    """An explosion: a sharp crack, a low boom, a noise blast and a crackling tail (size 0.5 small .. 2 huge;
    distance > 1 muffles it and softens the attack, for a far-off blast)."""
    dur = 2.5 + 1.5 * size
    n = _n(dur)
    t = _t(n)
    r = _rng("explosion", seed)
    crack = _hp(r.uniform(-1, 1, n), 1200) * _dec(n, 0.01, 0.0005)
    boom = np.tanh(2 * _sweep(30 + 60 * np.exp(-t / (0.06 * size))) * np.exp(-t / (0.5 * size)))
    blast = _lp(r.uniform(-1, 1, n), 2500) * _dec(n, 0.25 * size, 0.003) * 1.3
    rumble = _lp(r.uniform(-1, 1, n), 160) * _dec(n, 0.9 * size, 0.04) * 2.2
    crackle = np.zeros(n)
    for _ in range(int(60 * size)):
        at = r.exponential(0.5) + 0.1
        m = _n(0.01)
        _place(crackle, _hp(r.uniform(-1, 1, m), 2500) * np.exp(-_t(m) / 0.002) * r.uniform(0.1, 0.5) *
               np.exp(-at / 1.2), at)
    x = crack * 0.5 + boom + blast + rumble + crackle
    if distance > 1:
        x = _lp(x, 2500 / distance)
    return _norm(_verb(_pan(x, 0), 0.2, 1.2, seed=seed)[:n].mean(1) * _ramp(n, 0.001 * distance, 0.5))


def rifle_crack(seed=0):
    """A rifle shot heard from a little way off: a muffled crack and a short echo."""
    n = _n(1.2)
    t = _t(n)
    r = _rng("rifle", seed)
    crack = _lp(_hp(r.uniform(-1, 1, n), 400) * _dec(n, 0.006, 0.0003), 2200)
    thump = np.sin(2 * np.pi * 120 * t) * np.exp(-t / 0.03) * 0.5
    x = crack + thump
    echo = np.zeros(n)
    _place(echo, _lp(x, 1200), 0.18 + r.uniform(0, 0.08), 0.35)
    _place(echo, _lp(x, 800), 0.45 + r.uniform(0, 0.1), 0.15)
    return _norm(x + echo)


def sea_waves(dur, seed=0):
    """Waves on a beach: each swell rises, breaks and hisses back out (one every 5-9 s), over a steady wash. Stereo."""
    n = _n(dur)
    r = _rng("sea", seed)
    out = np.zeros((n, 2))
    for ch in range(2):
        env = np.zeros(n)
        tt = -r.uniform(0, 5)
        while tt < dur:
            per = r.uniform(5, 9)
            m = _n(per)
            u = np.linspace(0, 1, m)
            w = np.where(u < 0.55, (u / 0.55) ** 2, np.exp(-(u - 0.55) / 0.12))
            _place(env, w * r.uniform(0.6, 1.0), tt)
            tt += per * r.uniform(0.7, 0.95)
        rumble = _lp(r.uniform(-1, 1, n), 500) * (0.3 + env)
        hiss = _bp(r.uniform(-1, 1, n), 1500, 8000) * np.roll(env, _n(0.6)) ** 1.5 * 0.7
        out[:, ch] = rumble + hiss + _lp(r.uniform(-1, 1, n), 2000) * 0.08
    return _finish(out, dur, 1.0, 1.0)


def blizzard(dur, seed=0):
    """A winter storm: howling wind (narrow resonances that swap as it gusts), gust swells and blowing snow. Stereo."""
    n = _n(dur)
    r = _rng("blizzard", seed)
    out = np.zeros((n, 2))
    for ch in range(2):
        gust = 0.5 + 0.5 * np.clip(_lfo(n, 0.35, 1.4, r), -1, 1)
        howl = sum(_reso(r.uniform(-1, 1, n), f, 40) * np.clip(_lfo(n, 0.25, 1.5, r), 0, 1)
                   for f in (380, 470, 560, 690, 820))
        body = _bp(r.uniform(-1, 1, n), 150, 1200)
        snow = _hp(r.uniform(-1, 1, n), 3500) * 0.25
        out[:, ch] = (_norm(howl) * 0.6 + _norm(body) * 0.5) * gust + snow * gust ** 2
    return _finish(out, dur, 1.5, 1.5)


def radio_static(dur, seed=0):
    """A shortwave radio: band-limited hiss that fades in and out, crackle, and a tuning whistle now and then."""
    n = _n(dur)
    t = _t(n)
    r = _rng("static", seed)
    hiss = _bp(r.uniform(-1, 1, n), 300, 3500) * (0.6 + 0.4 * np.clip(_lfo(n, 0.4, 1.2, r), -1, 1))
    crackle = np.zeros(n)
    for _ in range(int(dur * 25)):
        m = _n(0.004)
        _place(crackle, r.uniform(-1, 1, m) * np.exp(-_t(m) / 0.001) * r.uniform(0.3, 1.5), r.uniform(0, dur))
    whistle = _sweep(1200 + 600 * np.sin(2 * np.pi * 0.13 * t + r.uniform(0, 6))) * \
        np.clip(_lfo(n, 0.3, 2.0, r) - 1.3, 0, 1) * 0.25
    return _finish(hiss * 0.6 + _bp(crackle, 200, 5000) + whistle, dur, 0.05, 0.1)


_VOWELS = [(730, 1090, 2440), (530, 1840, 2480), (270, 2290, 3010), (570, 840, 2410), (300, 870, 2240),
           (660, 1720, 2410), (490, 1350, 1690)]


def voice_crackle(dur, seed=0, f0=120):
    """A voice on a bad radio: a glottal buzz through changing vowel formants in syllables, with consonant hiss and
    phrase pauses, squeezed into a telephone band under static. It sounds like speech but says nothing."""
    n = _n(dur)
    t = _t(n)
    r = _rng("voice", seed)
    pitch = f0 * (1 + _lfo(n, 1.5, 0.08, r)) * (1 - 0.06 * (t % 2.2) / 2.2)       # falls through each phrase
    buzz = _saw(pitch, n)
    syl = np.zeros(n)
    vowel_track = [np.zeros(n) for _ in _VOWELS]
    tt = 0.05
    while tt < dur:
        if r.uniform() < 0.12:
            tt += r.uniform(0.25, 0.5)                                                   # a pause
            continue
        L = r.uniform(0.12, 0.26)
        m = _n(L)
        e = np.sin(np.pi * np.linspace(0, 1, m)) ** 0.7
        _place(syl, e, tt)
        _place(vowel_track[r.integers(len(_VOWELS))], e, tt)
        tt += L + r.uniform(0.01, 0.06)
    out = np.zeros(n)
    for (f1, f2, f3), env in zip(_VOWELS, vowel_track):
        if env.any():
            src = buzz * env
            out += _reso(src, f1, 8) + 0.6 * _reso(src, f2, 12) + 0.3 * _reso(src, f3, 14)
    cons = _hp(r.uniform(-1, 1, n), 3000) * np.clip(np.diff(syl, prepend=0) * SR / 12, 0, 1) * 0.6
    x = np.tanh(3 * _norm(_bp(out + cons, 400, 2800)))
    return _norm(x + radio_static(dur, seed + 7) * 0.35)


_MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
          "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
          "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
          "Y": "-.--", "Z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
          "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"}


def morse(text="CQ CQ DE G", wpm=20, f=680, seed=0):
    """Morse code keyed on a radio tone (dot = 1.2 / wpm s), with soft key clicks and a little static under it."""
    dot = 1.2 / wpm
    events, tt = [], 0.0
    for word in text.upper().split():
        for ch in word:
            for sym in _MORSE.get(ch, ""):
                ln = dot if sym == "." else 3 * dot
                events.append((tt, ln))
                tt += ln + dot
            tt += 2 * dot
        tt += 4 * dot
    n = _n(tt + 0.2)
    gate = np.zeros(n)
    edge = _n(0.005)
    for at, ln in events:
        m = _n(ln)
        g = np.ones(m)
        g[:edge] = np.sin(np.linspace(0, np.pi / 2, edge)) ** 2
        g[-edge:] = g[:edge][::-1]
        _place(gate, g, at)
    tone = np.sin(2 * np.pi * f * _t(n)) * gate
    return _norm(tone + radio_static(tt + 0.2, seed) * 0.12)


def typewriter(dur, seed=0, cps=7, bell=True):
    """A typewriter: key strikes at a typing rhythm (type bar slap on the platen), a spacebar now and then, and at
    the end the margin bell and the carriage return."""
    n = _n(dur)
    r = _rng("typewriter", seed)
    out = np.zeros(n)
    end = dur - (0.7 if bell else 0)
    tt, k = 0.05, 0
    while tt < end:
        m = _n(0.08)
        tm = _t(m)
        space = r.uniform() < 0.16
        click = _hp(r.uniform(-1, 1, m), 2500) * np.exp(-tm / 0.0025)
        slap = _bp(r.uniform(-1, 1, m), 900, 3500) * np.exp(-tm / 0.012)
        thunk = _lp(r.uniform(-1, 1, m), 350) * np.exp(-tm / 0.025)
        x = (click * 0.8 + slap + thunk * (1.6 if space else 0.8)) * (0.6 if space else r.uniform(0.75, 1.0))
        _place(out, x, tt)
        tt += max(0.06, r.gamma(4, 1 / cps / 4)) + (0.25 if r.uniform() < 0.05 else 0)
        k += 1
    if bell:
        _place(out, _norm(sum(np.sin(2 * np.pi * f * _t(_n(1.0))) * np.exp(-_t(_n(1.0)) / tau)
                              for f, tau in ((2350, 0.5), (6100, 0.15)))) * 0.5, end)
        for i in range(14):                                                               # the return ratchet
            m = _n(0.02)
            _place(out, _hp(r.uniform(-1, 1, m), 1500) * np.exp(-_t(m) / 0.003) * 0.5, end + 0.15 + i * 0.022)
        m = _n(0.1)
        _place(out, _lp(r.uniform(-1, 1, m), 600) * np.exp(-_t(m) / 0.03) * 1.2, end + 0.47)
    return _norm(out)


def stamp(seed=0):
    """A rubber stamp slammed on paper on a wooden desk: the wood thud, the rubber-and-paper slap, a small rattle."""
    n = _n(0.7)
    t = _t(n)
    r = _rng("stamp", seed)
    wood = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
               for f, a, tau in ((118, 1.0, 0.09), (196, 0.7, 0.06), (312, 0.5, 0.04), (505, 0.3, 0.025)))
    slap = _bp(r.uniform(-1, 1, n), 400, 3500) * np.exp(-t / 0.012) * 1.2
    rattle = _bp(r.uniform(-1, 1, n), 2000, 6000) * np.exp(-t / 0.03) * 0.15
    return _norm((np.tanh(1.5 * wood) + slap + rattle) * np.minimum(1, t / 0.0008))


def page_whoosh(seed=0, dur=0.45):
    """A page or a map swept across: an airy swish rising in pitch, paper flutter, and a soft landing."""
    n = _n(dur)
    u = np.linspace(0, 1, n)
    r = _rng("page", seed)
    noise = r.uniform(-1, 1, n)
    swish = sum(_bp(noise, lo, lo * 2.2) * np.exp(-((u - c) / 0.18) ** 2)
                for lo, c in ((500, 0.2), (900, 0.4), (1500, 0.55), (2400, 0.7)))
    flutter = _bp(noise, 1500, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * _t(n))) * np.sin(np.pi * u) * 0.25
    land = np.zeros(n)
    m = _n(0.05)
    _place(land, _bp(r.uniform(-1, 1, m), 300, 2000) * np.exp(-_t(m) / 0.01) * 0.4, dur * 0.82)
    return _norm((swish + flutter + land) * _ramp(n, 0.04, 0.05))


def crowd_cheer(dur, seed=0, size=60):
    """A crowd cheering: many voices shouting open vowels with rising pitch glides, applause and a few whistles,
    swelling in and dying away. Stereo (each side its own half of the crowd)."""
    n = _n(dur)
    r = _rng("crowd", seed)
    out = np.zeros((n, 2))
    vowels = [(800, 1200, 2500), (650, 1700, 2500), (500, 900, 2400)]                     # ah, ay, oh
    for ch in range(2):
        src = [np.zeros(n) for _ in vowels]
        for _ in range(size // 2):
            f0 = r.uniform(110, 300)
            at, ln = r.uniform(0, dur * 0.3), r.uniform(dur * 0.4, dur)
            m = min(_n(ln), n - _n(at))
            if m <= 0:
                continue
            tm = _t(m)
            glide = f0 * (1 + 0.25 * np.minimum(1, tm / 0.4)) * (1 + _lfo(m, 2, 0.04, r))
            e = np.minimum(1, tm / 0.3) * np.exp(-np.maximum(0, tm - ln * 0.6) / (ln * 0.25)) * \
                (0.7 + 0.3 * np.clip(_lfo(m, 1.5, 1.5, r), -1, 1))
            _place(src[r.integers(3)], _saw(glide, m, r.uniform()) * e, at)
        voices = sum(_reso(s, f1, 6) + 0.6 * _reso(s, f2, 9) + 0.25 * _reso(s, f3, 12)
                     for s, (f1, f2, f3) in zip(src, vowels))
        claps = np.zeros(n)
        for _ in range(int(dur * size * 1.5)):
            m = _n(0.012)
            _place(claps, _bp(r.uniform(-1, 1, m), 900, 5000) * np.exp(-_t(m) / 0.003) * r.uniform(0.3, 1),
                   r.uniform(0.2, dur * 0.95))
        whistles = np.zeros(n)
        for _ in range(max(1, int(dur / 3))):
            m = _n(r.uniform(0.4, 0.9))
            tm = _t(m)
            whistles_f = r.uniform(1800, 2600) * (1 + 0.15 * np.sin(np.pi * tm / tm[-1]))
            _place(whistles, _sweep(whistles_f) * np.sin(np.pi * tm / tm[-1]) * 0.3, r.uniform(0.3, dur * 0.7))
        out[:, ch] = _norm(_hp(voices, 120)) + _norm(claps) * 0.45 + whistles
    return _finish(_verb(out, 0.25, 1.4, seed=seed)[:n], dur, 0.4, min(2.0, dur / 3))


def clock_tick(dur, seed=0, bpm=60):
    """A mantel clock: tick and tock alternating, with a faint escapement rattle."""
    n = _n(dur)
    out = np.zeros(n)
    beat = 60 / bpm
    for k in range(int(dur / beat) + 1):
        _place(out, tick(4200 if k % 2 == 0 else 2900, k, 1.0 if k % 2 == 0 else 0.8), k * beat)
        _place(out, tick(6000, k + 99, 0.15), k * beat + 0.012)
    return _norm(_verb(_pan(out, 0), 0.12, 0.5, seed=seed)[:n].mean(1))


def train(dur, seed=0, speed=1.0, whistle=True, distance=1.0):
    """A steam train: chuffs from the stack (4 a wheel turn), rail-joint clicks in pairs (clickety-clack), the low
    roll, and a three-note whistle at the start. distance > 1 muffles it."""
    n = _n(dur)
    r = _rng("train", seed)
    out = np.zeros(n)
    rate = 3.2 * speed
    k, tt = 0, 0.0
    while tt < dur:
        m = _n(0.25)
        tm = _t(m)
        ch = _lp(r.uniform(-1, 1, m), 1800) * np.minimum(1, tm / 0.012) * np.exp(-tm / 0.09)
        _place(out, ch * (1.0 if k % 4 == 0 else 0.65), tt)
        tt += 1 / rate
        k += 1
    tt = 0.3
    while tt < dur:
        for off in (0.0, 0.11 / speed):
            m = _n(0.05)
            c = _bp(r.uniform(-1, 1, m), 800, 4000) * np.exp(-_t(m) / 0.008) + \
                np.sin(2 * np.pi * 210 * _t(m)) * np.exp(-_t(m) / 0.02) * 0.6
            _place(out, c * 0.5, tt + off)
        tt += 1.05 / speed
    out += _lp(r.uniform(-1, 1, n), 120) * 0.5
    if whistle:
        m = _n(1.6)
        tm = _t(m)
        bend = 1 - 0.03 * np.exp(-tm / 0.08)
        w = sum(np.sin(2 * np.pi * f * bend * tm) for f in (415, 523, 622)) / 3
        w = (w + _bp(r.uniform(-1, 1, m), 400, 2000) * 0.15) * _ramp(m, 0.08, 0.35)
        _place(out, w * 1.2, 0.2)
    if distance > 1:
        out = _lp(out, 3000 / distance)
    return _finish(out, dur, 0.5, 0.8)


def door_slam(seed=0):
    """A heavy steel door slammed shut in a concrete room (the bunker): a low boom, a metal ring, the latch."""
    n = _n(2.0)
    t = _t(n)
    r = _rng("door", seed)
    boom = np.tanh(2 * _sweep(45 + 40 * np.exp(-t / 0.04)) * np.exp(-t / 0.25))
    ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
               for f, a, tau in ((138, 0.5, 0.5), (302, 0.4, 0.4), (517, 0.3, 0.3), (811, 0.2, 0.25),
                                 (1290, 0.1, 0.15)))
    latch = np.zeros(n)
    m = _n(0.03)
    _place(latch, _hp(r.uniform(-1, 1, m), 2500) * np.exp(-_t(m) / 0.004), 0.06)
    x = boom + ring * 0.6 + latch * 0.4 + _lp(r.uniform(-1, 1, n), 800) * _dec(n, 0.03, 0.001)
    return _norm(_verb(_pan(x, 0), 0.3, 0.6, damp=3000, seed=seed)[:n].mean(1))


MUSIC = dict(tension=tension, march=march, somber=somber, low_tone=low_tone, triumph=triumph, drum_hit=drum_hit)
SFX = dict(gun_boom=gun_boom, artillery=artillery, artillery_barrage=artillery_barrage, tank=tank,
           plane_drone=plane_drone, dive_whine=dive_whine, explosion=explosion, rifle_crack=rifle_crack,
           sea_waves=sea_waves, blizzard=blizzard, radio_static=radio_static, voice_crackle=voice_crackle,
           morse=morse, typewriter=typewriter, stamp=stamp, page_whoosh=page_whoosh, crowd_cheer=crowd_cheer,
           clock_tick=clock_tick, train=train, door_slam=door_slam)


# ---------------------------------------------------------------- the mix

def _db(x):
    return 10 ** (x / 20)


def duck_env(v):
    """The sidechain envelope from the narration: 20 ms attack, 300 ms release (as the Shorts)."""
    gate = (np.abs(v) > 0.01).astype(np.float64)
    hop = SR // 1000
    g = gate[: len(gate) // hop * hop].reshape(-1, hop).max(axis=1)
    env = np.empty_like(g)
    a_up, a_dn = 1 - np.exp(-1 / 20), 1 - np.exp(-1 / 300)
    val = 0.0
    for i, x in enumerate(g):
        val += (a_up if x > val else a_dn) * (x - val)
        env[i] = val
    env = np.repeat(env, hop)
    return np.clip(np.concatenate([env, np.full(len(gate) - len(env), env[-1] if len(env) else 0.0)]), 0, 1)


def limit(x, ceiling_db=-1.5, release=0.08):
    """A look-ahead peak limiter on a 4x oversampled detector, so the true peak stays under the ceiling.
    Vectorised: the release is a peak-hold with exponential decay, computed as a running max in the log domain."""
    ceil = _db(ceiling_db)
    det = np.max(np.abs(signal.resample_poly(x, 4, 1, axis=0)), axis=1)
    det = det[: len(x) * 4].reshape(-1, 4).max(axis=1)[: len(x)]
    det = np.pad(det, (0, len(x) - len(det)), mode="edge")
    need = np.minimum(1.0, ceil / np.maximum(det, 1e-12))
    g = minimum_filter1d(need, 2 * int(0.004 * SR) + 1, mode="nearest")               # 4 ms look-ahead and hold
    red = -np.log(g)                                                                     # >= 0, 0 = no reduction
    la = 1 / (release * SR)                                                              # decay per sample (log)
    k = np.arange(len(red))
    held = np.maximum.accumulate(np.where(red > 0, red + k * la, -np.inf)) - k * la
    gain = np.exp(-np.maximum(held, 0.0))
    return x * gain[:, None]


def write_wav(path, x):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).round().astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def loudnorm(src, dst, target=-14.0, tp=-1.0):
    """ffmpeg loudnorm, two passes (measure, then a linear correction). Returns the pass-2 measurement."""
    flt = f"loudnorm=I={target}:TP={tp}:LRA=20"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", flt + ":print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    flt2 = (f"{flt}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", src, "-af", flt2, "-ar", str(SR),
                        "-c:a", "pcm_s16le", "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
                        dst], capture_output=True, text=True)
    return json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])


def measure(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        "loudnorm=I=-14:TP=-1:LRA=20:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    return {"I": float(m["input_i"]), "TP": float(m["input_tp"]), "LRA": float(m["input_lra"])}


class Mix:
    """Three stereo buses (music, effects, ambience) on one timeline, the narration ducking music and ambience,
    hard cuts to silence, and the master."""

    def __init__(self, total):
        self.total = total
        n = _n(total)
        self.bus = {k: np.zeros((n, 2)) for k in ("music", "fx", "amb")}
        self.cuts = []

    def _add(self, bus, x, at, db, pan, fade_in, fade_out):
        x = np.asarray(x, np.float64)
        if fade_in or fade_out:
            e = _ramp(len(x), fade_in, fade_out)
            x = x * (e[:, None] if x.ndim == 2 else e)
        if x.ndim == 1:
            x = _pan(x, pan) / np.sqrt(2)
        _place(self.bus[bus], x, at, _db(db))

    def music(self, x, at, db=-16, fade_in=0.0, fade_out=0.0):
        self._add("music", x, at, db, 0.0, fade_in, fade_out)

    def sfx(self, x, at, db=-10, pan=0.0, fade_in=0.0, fade_out=0.0):
        self._add("fx", x, at, db, pan, fade_in, fade_out)

    def amb(self, x, at, db=-22, pan=0.0, fade_in=0.5, fade_out=0.5):
        self._add("amb", x, at, db, pan, fade_in, fade_out)

    def cut(self, t0, t1):
        """A hard cut to silence from t0 to t1 on music, effects and ambience (5 ms edges, so no click)."""
        self.cuts.append((t0, t1))

    def render(self, voice=None, music_duck_db=-10.0, amb_duck_db=-8.0):
        n = _n(self.total)
        music, fx, amb = (self.bus[k].copy() for k in ("music", "fx", "amb"))
        v = np.zeros(n)
        if voice is not None:
            v[: min(n, len(voice))] = np.asarray(voice, np.float64)[:n]
            env = duck_env(v)[:, None]
            music *= 1 - (1 - _db(music_duck_db)) * env
            amb *= 1 - (1 - _db(amb_duck_db)) * env
        gate = np.ones(n)
        e = _n(0.005)
        for t0, t1 in self.cuts:
            i0, i1 = int(t0 * SR), min(n, int(t1 * SR))
            gate[max(0, i0 - e):i0] *= np.linspace(1, 0, min(e, i0))
            gate[i0:i1] = 0
            gate[i1:i1 + e] *= np.linspace(0, 1, len(gate[i1:i1 + e]))
        bed = _hp(music + fx + amb, 30, 2)                    # nothing useful lives under 30 Hz: keep the headroom
        return bed * gate[:, None] + v[:, None]

    def master(self, path, voice=None, target=-14.0):
        """Render, bring to the target loudness through the limiter, then ffmpeg loudnorm (two passes) to the file.
        Returns the measured {"I", "TP", "LRA"} of the written file."""
        import pyloudnorm
        mix = self.render(voice)
        meter = pyloudnorm.Meter(SR)
        g = _db(target - meter.integrated_loudness(mix))
        for _ in range(3):                                   # the limiter costs loudness: make it up and re-limit
            lim = limit(mix * g, -1.5)
            g *= _db(target - meter.integrated_loudness(lim))
        mix = limit(mix * g, -1.5)
        pre = path[:-4] + "_pre.wav"
        write_wav(pre, mix)
        loudnorm(pre, path, target)
        os.remove(pre)
        return measure(path)


# ---------------------------------------------------------------- the demo

def demo(path=None):
    """~40 s: the four moods with effects laid in, as the episode would use them.
    0-9 tension (clock, radio voice, morse, typewriter and stamp) -> the drum-hit stinger (9.0) -> map whoosh ->
    the battleship gun (11.2) and a hard cut to silence -> march (12.4-22.4: sea, tanks, planes, guns, a dive and its
    explosion) -> somber (22.4-30.2: piano; a blizzard, a distant train) -> the bunker door and silence -> triumph
    (31.2-40: the crowd cheers V-E Day)."""
    path = path or os.path.join(STYLE_OUT, "sound_demo.wav")
    total = 40.0
    m = Mix(total)
    # tension
    m.music(tension(9.0), 0.0, -14, fade_in=0.4)
    m.amb(clock_tick(4.5), 0.0, -22, fade_in=0.05, fade_out=0.3)
    m.sfx(voice_crackle(3.2, 1), 1.2, -24, pan=-0.3, fade_in=0.1, fade_out=0.2)
    m.sfx(morse("SOS DE SP"), 4.4, -26, pan=0.3)
    m.sfx(typewriter(2.4, 2), 6.0, -20, pan=0.2)
    m.sfx(stamp(), 8.55, -12)
    m.music(drum_hit(), 9.0, -6)
    m.sfx(page_whoosh(), 10.5, -16, pan=-0.2)
    m.sfx(gun_boom(), 11.2, -3)
    m.cut(11.75, 12.4)
    # march
    m.music(march(10.4), 12.4, -15, fade_out=1.5)
    m.amb(sea_waves(5.0), 12.4, -22, fade_in=0.05, fade_out=1.5)
    m.sfx(tank(5.5, 1), 15.5, -17, pan=-0.3, fade_in=0.5, fade_out=1.0)
    m.sfx(plane_drone(6.0, 2, count=3), 14.0, -17)
    m.sfx(artillery_barrage(5.5, 3), 16.0, -18)
    for k, at in enumerate((16.9, 17.3, 18.6)):
        m.sfx(rifle_crack(k), at, -20, pan=0.4)
    m.sfx(dive_whine(2.4), 18.2, -14, pan=0.2)
    m.sfx(explosion(1, 1.2), 20.6, -6, pan=0.1)
    # somber
    m.music(somber(8.6), 22.4, -13, fade_in=0.3)
    m.amb(blizzard(4.6), 22.4, -24, fade_in=1.0, fade_out=1.5)
    m.amb(train(4.4, 1, distance=2.5), 26.0, -24, fade_in=0.8, fade_out=1.0)
    m.sfx(door_slam(), 30.2, -8)
    m.cut(30.75, 31.2)
    # triumph
    m.music(triumph(8.8), 31.2, -13)
    m.amb(crowd_cheer(6.8, 2), 32.6, -19, fade_in=0.6, fade_out=1.5)
    meas = m.master(path)
    return path, meas


def reel(path=None):
    """Every effect and the stinger one after another (1 s apart), for review. Prints the start times."""
    path = path or os.path.join(STYLE_OUT, "sfx_reel.wav")
    items = [("drum_hit", drum_hit()), ("gun_boom", gun_boom()), ("artillery", artillery()),
             ("artillery_barrage", artillery_barrage(5)), ("tank", tank(5)), ("plane_drone", plane_drone(6)),
             ("plane_drone x4", plane_drone(7, 1, count=4)), ("dive_whine", dive_whine()),
             ("explosion", explosion()), ("explosion far", explosion(2, 1.5, 3)), ("rifle_crack", rifle_crack()),
             ("sea_waves", sea_waves(10)), ("blizzard", blizzard(8)), ("radio_static", radio_static(4)),
             ("voice_crackle", voice_crackle(5)), ("morse", morse()), ("typewriter", typewriter(4)),
             ("stamp", stamp()), ("page_whoosh", page_whoosh()), ("crowd_cheer", crowd_cheer(7)),
             ("clock_tick", clock_tick(5)), ("train", train(8)), ("door_slam", door_slam())]
    at, plan = 0.5, []
    for name, x in items:
        plan.append((round(at, 2), name))
        at += len(x) / SR + 1.0
    m = Mix(at)
    for (t0, name), (_, x) in zip(plan, items):
        m.sfx(x, t0, -8)
    meas = m.master(path)
    return path, meas, plan


if __name__ == "__main__":
    p, meas = demo(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"{os.path.relpath(p, ROOT)}: I {meas['I']:.2f} LUFS, TP {meas['TP']:.2f} dBTP, LRA {meas['LRA']:.1f}")
    p, meas, plan = reel()
    print(f"{os.path.relpath(p, ROOT)}: I {meas['I']:.2f} LUFS, TP {meas['TP']:.2f} dBTP")
    print("  " + ", ".join(f"{t:.1f} {nm}" for t, nm in plan))
