"""Episode 1 v2 sound mix: voice + original music + effects -> out/monsters/ep01v2/mix.wav (48 kHz stereo, 62.48 s).

    tar xf assets/voice_cache/monsters_ep01v2_takes.tar
    python channels/monsters/ep01v2_sound.py            # mix.wav + stems voice.wav, music.wav, sfx.wav
    python channels/monsters/ep01v2_sound.py --check    # also Whisper medium.en on every line of mix.wav
    python channels/monsters/ep01v2_sound.py --roughcut # also mux picture.mp4 + mix.wav -> roughcut.mp4

Needs numpy, scipy, pyloudnorm, pycairo and imageio-ffmpeg (motion/), ffmpeg on PATH, openai-whisper for --check.

The voice is the cached Turbo am_liam takes laid out exactly as ep01v2_timing.py lays them out (same pauses, same
NARRATOR); it refuses to synthesise. Times come from ep01v2/timing.json; every cue below is (shot, seconds into the
shot) so a re-timed cut moves the sound with it.

Sound plan (reports/Pokémon episodes story and animation.md, SS1-SS10):
  S01-S02   meadow wind + smoke crackle from frame 0 (SS1), a low uneasy pad; S02 the tape-rewind glitch.
  S03a-S08  the lab opens quiet (SS7): rain, lab hum, tank bubbles, the "lab" bed low. S04/S05a the slowed snap,
            the bubble's hiss and collapse; S06 thunder; S07 snap + glass crack; S08 water trickle, the spark, then
            dead silence through the black.
  S09-S14   the white bloom opens on a soft pad, then light bright plucks ("wonder" bed); birds, creature squeaks.
  S15       near-silence for ~1 s (two drips off the claw), then the burst on STRIKE_FRAME: snap + shockwave + erase,
            a ring-out, then quiet under S16-S18. S19 a tense held tone (steady pitch and level: no riser).
  S20       a tiny pathetic "pff", then silence for the deadpan. S21 little stomps, plucks back.
  S22-S24   a low uneasy pad, a wing flutter; the bed dips ~0.5 s before the A/B line (SS3), a whoosh as the split
            opens, then a sting that climbs in steps under the question and cuts with the picture.
Music is sidechain-ducked under the voice (20 ms attack, 300 ms release; SS10). All music is original (sfx.py beds
and the figures here: no franchise jingles or melodies, SS9). Loudness: -14 LUFS integrated, true peak <= -1 dBTP,
measured and corrected with ffmpeg loudnorm in two passes; no metadata in the WAVs.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import wave
import zlib

import numpy as np
from scipy import signal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault("CLONE_RATE", "5.0")

STRIKE_FRAME = 41        # S15 frame, 0-based in the cut: the claw snaps shut (helper10.py re-stage, Blender frame 42)
FLASH_FRAME = 43         # the 2-frame white flash (Blender 44-45): the shockwave boom
DUST_FRAME = 49          # the forest wall pops into dust (Blender 50 on): the erase
BLOWN_FRAME = 79         # Kai is blown back (Blender 80)
OUT_SR = 48000
OUT = os.path.join(ROOT, "out", "monsters", "ep01v2")

from channels.monsters import sfx                 # noqa: E402
from channels.monsters.sfx import SR, _bp, _exp, _hp, _lp, _midi, _n, _place, _pluck, _rng, _sweep, _t, _verb  # noqa: E402
from motion import timeline, voice                # noqa: E402

timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4   # as ep01v2_timing.py


# ---------------------------------------------------------------- the voice (cached takes only)

def _no_synth(*a, **k):
    raise SystemExit(f"missing voice take (would synthesise): {a[:1]}")


def load_voice():
    """The episode's Timeline built from the cached takes, exactly as ep01v2_timing.py builds it."""
    voice._clone_generate = _no_synth if hasattr(voice, "_clone_generate") else None
    spec = importlib.util.spec_from_file_location("ep01v2_episode", os.path.join(ROOT, "channels", "monsters",
                                                                                  "ep01v2", "episode.py"))
    ep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ep)
    voice.configure(**ep.NARRATOR)
    real_run = voice.subprocess.run

    def guarded(cmd, *a, **k):
        if any("clone_tts.py" in str(c) for c in cmd):
            raise SystemExit("missing voice take: clone_tts.py would run. Unpack the takes tar first.")
        return real_run(cmd, *a, **k)

    voice.subprocess.run = guarded
    try:
        return ep, timeline.Timeline(ep.SCRIPT, tail=ep.TAIL)
    finally:
        voice.subprocess.run = real_run


def _whisper_line(x):
    """Line 1 is whispered inside the scene: ~4 dB down, a little high-pass and some air on top."""
    x = signal.sosfilt(signal.butter(2, 140, "highpass", fs=SR, output="sos"), x)
    air = signal.sosfilt(signal.butter(2, 5500, "highpass", fs=SR, output="sos"), x)
    return (x + 0.6 * air) * 10 ** (-4 / 20)


def voice_track(tl, n):
    out = np.zeros(n)
    for b in tl.beats:
        if b.audio is None or not len(b.audio):
            continue
        x = np.asarray(b.audio, np.float64)
        if b.id == "l1":
            x = _whisper_line(x)
        _place(out, x, b.start)
    return out


def duck_env(v):
    """Sidechain envelope from the voice: 20 ms attack, 300 ms release (as motion.voice.narration_track)."""
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


# ---------------------------------------------------------------- extra effects (original, seeded)

def meadow_wind(dur, seed=0):
    """Soft open-air wind: low rumble and a breathy band that swell in slow, uneven gusts."""
    r = _rng("meadow_wind", seed)
    n = _n(dur)
    t = _t(n)
    noise = r.uniform(-1, 1, n)
    gust = 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t + r.uniform(0, 6)) * np.sin(2 * np.pi * 0.31 * t + r.uniform(0, 6))
    body = _lp(noise, 350) * 1.2 + _bp(noise, 500, 2200) * 0.35
    return body * gust


def crackle(dur, seed=0):
    """Smouldering wood: sparse dry pops and ticks."""
    r = _rng("crackle", seed)
    out = np.zeros(_n(dur))
    at = r.uniform(0, 0.1)
    while at < dur:
        m = _n(r.uniform(0.002, 0.012))
        _place(out, _hp(r.uniform(-1, 1, m), 1500) * _exp(m, m / SR / 3, 0.0002) * r.uniform(0.2, 1.0), at)
        at += r.exponential(0.09)
    return out


def slow_snap(factor=2.5, seed=0):
    """The snap stretched in time (pitch falls with it): the slow-motion close-up of S04."""
    x = sfx.snap(seed).astype(np.float64)
    return signal.resample_poly(x, int(factor * 10), 10)


def bubble_hiss(dur, seed=0):
    """The cavitation bubble swelling: a hot fizz that thickens and brightens a little, at a steady level."""
    r = _rng("bubble_hiss", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    noise = r.uniform(-1, 1, n)
    fizz = _bp(noise, 1800, 9000) * (r.random(n) > 0.9) * 2.0 + _bp(noise, 300, 1500) * 0.3
    return fizz * np.minimum(1, p / 0.15) * np.minimum(1, (1 - p) / 0.05)


def bubble_collapse(seed=0):
    """The bubble collapses: a hollow falling pop, then a fizz of micro-bubbles thinning out."""
    r = _rng("bubble_collapse", seed)
    out = np.zeros(_n(1.0))
    m = _n(0.12)
    _place(out, _sweep(900 * np.exp(-_t(m) * 30) + 120) * _exp(m, 0.04, 0.002), 0)
    at = 0.04
    while at < 0.9:
        k = _n(0.03)
        f0 = r.uniform(1500, 4000)
        _place(out, _sweep(f0 * (1 + 2 * _t(k))) * _exp(k, 0.006, 0.0005) * r.uniform(0.1, 0.4) * (1 - at), at)
        at += r.exponential(0.025)
    return _verb(out, 0.2, 0.4)


def glass_crack(seed=0):
    """Tank glass cracking: a hard tick, then a quick run of brittle splintering ticks climbing away."""
    r = _rng("glass_crack", seed)
    out = np.zeros(_n(0.6))
    m = _n(0.01)
    _place(out, _hp(r.uniform(-1, 1, m), 3000) * _exp(m, 0.002, 0.0002) * 1.5, 0)
    at = 0.01
    while at < 0.22:
        k = _n(r.uniform(0.002, 0.006))
        f0 = r.uniform(3000, 8000)
        tick = _bp(r.uniform(-1, 1, k), f0 * 0.7, min(f0 * 1.4, SR / 2 - 200)) * _exp(k, k / SR / 3, 0.0002)
        _place(out, tick * r.uniform(0.3, 0.9), at)
        at += r.exponential(0.012)
    m = _n(0.4)                                                  # a faint glassy ring under it
    _place(out, sum(np.sin(2 * np.pi * f * _t(m)) for f in (2630, 4170, 5890)) * _exp(m, 0.12) * 0.05, 0)
    return _verb(out, 0.15, 0.4)


def trickle(dur, seed=0):
    """Water running across a floor: a soft wash with little bubbling plinks."""
    r = _rng("trickle", seed)
    n = _n(dur)
    out = _bp(r.uniform(-1, 1, n), 800, 4000) * 0.15
    at = 0.0
    while at < dur:
        k = _n(0.04)
        f0 = r.uniform(700, 1800)
        _place(out, _sweep(f0 * (1 + 1.5 * _t(k))) * _exp(k, 0.01, 0.001) * r.uniform(0.2, 0.6), at)
        at += r.exponential(0.05)
    return out


def drip(seed=0):
    """One drop falling off the claw: a small bright plink."""
    k = _n(0.15)
    f0 = 1300 + 300 * (seed % 3)
    return _sweep(f0 * (1 + 2.0 * _t(k))) * _exp(k, 0.025, 0.001)


def ring_out(dur=3.0):
    """After the blast: a thin high ear-ring that fades, over a hollow low sine."""
    n = _n(dur)
    t = _t(n)
    ring = np.sin(2 * np.pi * 3150 * t) * 0.25 + np.sin(2 * np.pi * 3163 * t) * 0.15
    low = np.sin(2 * np.pi * 55 * t) * 0.3
    return (ring + low) * np.exp(-t / (dur / 3)) * np.minimum(1, t / 0.05)


def pff(seed=0):
    """The failed snap: a tiny dry click and a weak little puff of dust."""
    r = _rng("pff", seed)
    out = np.zeros(_n(0.4))
    c = np.zeros(_n(0.002))
    c[0], c[1] = 0.6, -0.4
    _place(out, c, 0)
    m = _n(0.3)
    _place(out, _bp(r.uniform(-1, 1, m), 300, 2500) * np.sin(np.pi * np.clip(_t(m) / 0.3, 0, 1)) ** 2 * 0.5, 0.01)
    return out


def stomp(seed=0):
    """A tiny angry footstep: a small soft thump with a grass rustle."""
    r = _rng("stomp", seed)
    m = _n(0.12)
    t = _t(m)
    thump = _sweep(220 * np.exp(-t * 25) + 90) * np.exp(-t / 0.03)
    rustle = _bp(r.uniform(-1, 1, m), 1500, 6000) * _exp(m, 0.015, 0.001) * 0.4
    return thump + rustle


def flutter(dur=0.6, seed=0):
    """Small wings beating as a bird lands: fast soft air pulses that slow down."""
    r = _rng("flutter", seed)
    n = _n(dur)
    t = _t(n)
    rate = 22 - 10 * t / dur
    pulses = np.maximum(0, np.sin(2 * np.pi * np.cumsum(rate) / SR)) ** 3
    air = _bp(r.uniform(-1, 1, n), 400, 3500)
    return air * pulses * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.5


def lap(seed=0):
    """A small creature lapping at water: a soft wet tick."""
    k = _n(0.06)
    return _bp(_rng("lap", seed).uniform(-1, 1, k), 500, 3000) * _exp(k, 0.012, 0.001)


def eerie_sting(seed=0):
    """A small wrong-feeling glint: two high glassy bells a semitone apart, beating, with a soft breathy swell."""
    out = np.zeros(_n(1.4))
    _place(out, sfx._bell(_midi(88), 1.3, 0.7) + sfx._bell(_midi(89), 1.3, 0.7) * 0.8, 0)
    m = _n(0.9)
    _place(out, _bp(_rng("eerie", seed).uniform(-1, 1, m), 2500, 7000) * np.sin(np.pi * np.linspace(0, 1, m)) ** 2
           * 0.15, 0.02)
    return _verb(out, 0.3, 0.8)


# ---------------------------------------------------------------- music cues (original)

def soft_pad(dur, notes=(57, 64, 69, 72), bright=0.15, seed=0):
    """A held, even pad (steady pitch and level) that fades in and out."""
    n = _n(dur)
    t = _t(n)
    r = _rng("soft_pad", seed)
    x = sum(np.sin(2 * np.pi * _midi(m) * t + r.uniform(0, 6)) + np.sin(2 * np.pi * _midi(m) * 1.003 * t)
            + bright * np.sin(2 * np.pi * 2 * _midi(m) * t) for m in notes) / len(notes)
    x = _lp(x, 2500)
    fade = np.minimum(1, t / min(0.6, dur / 3)) * np.minimum(1, (dur - t) / min(0.8, dur / 3))
    return x * fade


def tense_tone(dur, seed=0):
    """S19: one held tense chord (a low fifth with a cold minor second on top), even level, no rise."""
    n = _n(dur)
    t = _t(n)
    x = (np.sin(2 * np.pi * _midi(38) * t) * 0.6 + np.sin(2 * np.pi * _midi(45) * t) * 0.4
         + np.sin(2 * np.pi * _midi(62) * t) * 0.18 + np.sin(2 * np.pi * _midi(63) * t) * 0.14)
    x *= 1 + 0.04 * np.sin(2 * np.pi * 0.25 * t)
    return _lp(x, 1500) * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.3)


def sting(dur, seed=0):
    """Under the A/B question: a held minor chord and a plucked figure that climbs in steps (an original
    pentatonic line, not a noise riser); it is cut hard by the picture."""
    n = _n(dur)
    t = _t(n)
    base = soft_pad(dur + 0.5, (50, 57, 62, 65), 0.25, seed)[:n] * 0.8
    steps = [62, 65, 67, 69, 72, 74, 77]
    out = base.copy()
    for k, m in enumerate(steps):
        at = k * dur / len(steps)
        _place(out, _pluck(_midi(m), 0.9, 0.994, k) * (0.5 + 0.08 * k), at)
        _place(out, _pluck(_midi(m - 12), 0.9, 0.994, k + 9) * 0.3, at)
    return out[:n]


def bed(mood, dur, seed=0):
    return sfx.music_bed(dur, mood, seed).astype(np.float64)


# ---------------------------------------------------------------- the mix

class Cue:
    def __init__(self, timing):
        self.shot = {s["shot"]: s for s in timing["shots"]}
        self.line = {l["id"]: l for l in timing["lines"]}

    def t(self, shot, sec=0.0):
        return self.shot[shot]["start"] + sec

    def f(self, shot, frame):
        return self.shot[shot]["start"] + frame / 24

    def end(self, shot):
        return self.shot[shot]["start"] + self.shot[shot]["seconds"]

    def word(self, line, word, edge="start"):
        for w in self.line[line]["words"]:
            if w["w"].strip(".,?!\"'").lower() == word.lower():
                return w[edge]
        raise KeyError((line, word))


def _span(track, x, t0, t1, fade_in=0.05, fade_out=0.1):
    """Place x (trimmed to t1 - t0) with short fades at both ends."""
    x = x[: _n(t1 - t0)].copy()
    a, b = min(len(x), _n(fade_in)), min(len(x), _n(fade_out))
    if a:
        x[:a] *= np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)
    _place(track, x, t0)


def _rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def _db(x):
    return 10 ** (x / 20)


def build(timing, n, v):
    """Returns (music, fx, amb): music is mono; the one-shot effects and the ambience are stereo (the ambience
    decorrelated per side, and ducked under the voice later so its ticks never blur a consonant)."""
    c = Cue(timing)
    total = n / SR
    music = np.zeros(n)
    fx = [np.zeros(n), np.zeros(n)]
    ambience = [np.zeros(n), np.zeros(n)]
    v_rms = _rms(v[np.abs(v) > 0.01])
    strike = c.f("S15", STRIKE_FRAME)

    def music_at(x, t0, t1, db, fi=0.3, fo=0.4):
        _span(music, x / _rms(x) * v_rms * _db(db), t0, t1, fi, fo)

    def amb(gen, t0, t1, db, fi=0.3, fo=0.3):
        for side in (0, 1):
            x = gen(t1 - t0 + 0.1, side)
            _span(ambience[side], x / _rms(x) * v_rms * _db(db), t0, t1, fi, fo)

    def hit(x, at, db, pan=0.0):
        x = np.asarray(x, np.float64)
        x = x / (np.max(np.abs(x)) + 1e-12) * v_rms * _db(db) * 4   # db relative to ~voice peak level
        _place(fx[0], x * min(1.0, 1 - pan), at)                 # pan: -1 left .. +1 right
        _place(fx[1], x * min(1.0, 1 + pan), at)

    # --- S01-S02: frame 0 already has sound (SS1)
    amb(lambda d, s: meadow_wind(d, s), 0.0, c.t("S02"), -20, 0.02, 0.15)
    amb(lambda d, s: crackle(d, 10 + s), 0.0, c.t("S02"), -24, 0.02, 0.15)
    music_at(bed("danger", c.t("S02") + 0.5, 1), 0.0, c.t("S02"), -18, 0.02, 0.15)
    hit(sfx.glitch(c.end("S02") - c.t("S02"), 0), c.t("S02"), -14)

    # --- the lab, quiet (SS7): rain, hum, bubbles under a low bed; it stops dead after the spark
    lab0, spark_t = c.t("S03a"), c.word("l8", "Me", "end") + 0.02    # the spark answers "Me." (never masks it)
    silence0 = spark_t + 0.3                                     # the power dies with the spark: rain and hum cut
    amb(lambda d, s: sfx.rain(d, s), lab0, silence0, -24, 0.4, 0.05)
    amb(lambda d, s: sfx.lab_hum(d, s), lab0, silence0, -28, 0.4, 0.05)
    amb(lambda d, s: sfx.aquarium_bubbles(d, s), lab0, c.t("S06"), -27, 0.4, 0.5)
    music_at(bed("lab", silence0 - lab0 + 0.5, 0), lab0, spark_t, -17, 0.5, 0.2)
    hit(slow_snap(), c.word("l4", "snaps"), -6)
    hiss0 = c.word("l4", "snaps") + 0.35
    collapse_t = c.t("S05a", 1.65)
    amb(lambda d, s: bubble_hiss(d, 20 + s), hiss0, collapse_t, -22, 0.4, 0.05)
    hit(bubble_collapse(), collapse_t, -10)
    hit(sfx.thunder(), c.f("S06", 14), -3)                        # the crack lands on the bolt and flash (S06 f14, on "storm")
    hit(sfx.snap(1), c.f("S07", 9), -2)                          # the snap and its flash (S07 f8-9)
    hit(glass_crack(), c.f("S07", 10), -8, 0.2)
    amb(lambda d, s: trickle(d, 30 + s), c.t("S08"), spark_t + 0.1, -22, 0.2, 0.1)
    hit(sfx.spark(), spark_t, -6)
    i0, i1, f = int((spark_t + 0.4) * SR), int(c.t("S09") * SR), _n(0.08)
    for tr in (music, *fx, *ambience):                             # dead silence through the black
        tr[i0:i0 + f] *= np.linspace(1, 0, f)
        tr[i0 + f:i1] = 0

    # --- dead silence through the black, then the white bloom on a soft pad
    w0 = c.t("S09")
    music_at(soft_pad(1.8, (60, 67, 72, 76), 0.1), w0, w0 + 1.8, -16, 0.5, 0.6)
    music_at(bed("wonder", c.t("S15") - w0 + 1.0, 2), c.f("S09", 30), c.t("S15"), -15, 0.4, 0.12)   # lifts as the crack lands
    amb(lambda d, s: meadow_wind(d, 40 + s), w0 + 0.3, strike - 1.0, -27, 0.6, 0.25)
    amb(lambda d, s: sfx.birds(d, 50 + s), w0 + 0.5, c.t("S12"), -24, 0.5, 0.6)
    for k, (at, pitch) in enumerate([(c.t("S10a", 1.58), 1.6), (c.t("S10b", 0.74), 1.8)]):
        hit(sfx.cute_chirp(pitch, k), at, -16, (-0.3, 0.3)[k])
    hit(eerie_sting(), c.f("S11b", 6), -18)                      # the moth's eye-spots open on "wrong" (f6-10)
    for k in range(4):                                           # S13: something lapping at the puddle
        hit(lap(k), c.t("S13", 0.12 + 0.22 * k), -24)

    # --- S15: near-silence ~1 s (SS2), two drips, then the burst
    amb(lambda d, s: meadow_wind(d, 60 + s), strike - 1.0, strike, -40, 0.1, 0.0)
    for k, d in enumerate((0.75, 0.35)):
        hit(drip(k), strike - d, -22)
    hit(sfx.snap(2), strike, 0)
    hit(sfx.shockwave(), c.f("S15", FLASH_FRAME), 0)
    hit(sfx.erase(), c.f("S15", DUST_FRAME), -4)
    hit(ring_out(3.2), c.f("S15", FLASH_FRAME) + 0.3, -16)
    hit(sfx.whoosh(1), c.f("S15", BLOWN_FRAME) - 0.15, -14)

    # --- after the snap: quiet under S16-S18, a held tense tone under S19
    amb(lambda d, s: meadow_wind(d, 70 + s), strike + 1.5, c.t("S20"), -29, 1.0, 0.3)
    music_at(soft_pad(c.t("S19") - c.t("S16") + 0.4, (45, 52, 57, 60), 0.05, 1), c.t("S16"), c.t("S19") + 0.3, -21,
             1.0, 0.4)
    music_at(tense_tone(c.end("S19") - c.t("S19")), c.t("S19"), c.end("S19"), -19, 0.5, 0.25)

    # --- S20: a tiny "pff", then silence for the deadpan (only the faintest air)
    pff_t = c.word("l20", "anyway") + 0.85
    hit(pff(), pff_t, -14)
    amb(lambda d, s: meadow_wind(d, 80 + s), c.t("S20"), c.t("S21"), -38, 0.3, 0.3)

    # --- S21-S23: plucks back with the stomps, then the thorn tree and the bird
    amb(lambda d, s: meadow_wind(d, 90 + s), c.t("S21"), total, -28, 0.4, 0.02)
    for k in range(6):
        hit(stomp(k), c.t("S21", 0.35 + 0.19 * k), -15, (-0.25 + 0.1 * k))
    music_at(bed("wonder", c.t("S22") - c.t("S21") + 1.0, 3), c.t("S21"), c.t("S22"), -16, 0.4, 0.3)
    dip = c.word("l24", "Save") - 0.5                            # SS3: the bed dips ~0.5 s before the A/B line
    music_at(soft_pad(dip - c.t("S22") + 0.3, (50, 57, 62, 63), 0.1, 2), c.t("S22"), dip, -19, 0.4, 0.2)
    hit(flutter(0.6), c.t("S23", 0.2), -14, 0.15)
    hit(sfx._bell(_midi(96), 0.8, 0.4) + sfx._bell(_midi(103), 0.8, 0.3) * 0.5, c.f("S23", 62), -22, 0.2)   # the glint
    hit(sfx.whoosh(), c.t("S24") + 0.02, -10)
    music_at(sting(total - c.word("l24", "Save")), c.word("l24", "Save"), total, -14, 0.25, 0.01)
    return music, fx, ambience


def true_peak(x, os_=4):
    up = signal.resample_poly(x, os_, 1, axis=0)
    return float(np.max(np.abs(up)) + 1e-12)


def limit(x, ceiling_db=-1.5, release=0.08, sr=OUT_SR):
    """A look-ahead peak limiter on an oversampled detector so the true peak stays under the ceiling."""
    ceil = _db(ceiling_db)
    det = np.max(np.abs(signal.resample_poly(x, 4, 1, axis=0)), axis=1).reshape(-1, 4).max(axis=1)[: len(x)]
    need = np.minimum(1.0, ceil / np.maximum(det, 1e-12))
    from scipy.ndimage import minimum_filter1d
    g = minimum_filter1d(need, 2 * int(0.004 * sr) + 1, mode="nearest")   # 4 ms look-ahead (and hold)
    # release: the gain recovers smoothly (one-pole), attack is the look-ahead minimum above
    out = np.empty_like(g)
    a = np.exp(-1 / (release * sr))
    val = 1.0
    for i, gi in enumerate(g):
        val = gi if gi < val else gi + (val - gi) * a
        out[i] = val
    return x * out[:, None]


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).round().astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(OUT_SR)
        w.writeframes(pcm.tobytes())


def loudnorm(src, dst, target=-14.0, tp=-1.0):
    """ffmpeg loudnorm, two passes (measure, then linear correction). Returns the pass-1 and output measurements."""
    flt = f"loudnorm=I={target}:TP={tp}:LRA=11"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", flt + ":print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    flt2 = (f"{flt}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", src, "-af", flt2, "-ar", str(OUT_SR),
                        "-c:a", "pcm_s16le", "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
                        dst], capture_output=True, text=True)
    m2 = json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])
    return m, m2


def measure(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.findall(r"\{[^{}]*\}", r.stderr)[-1])


def to_out(x):
    return signal.resample_poly(x, 160, 147, axis=0)


def main():
    import pyloudnorm
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")) as f:
        timing = json.load(f)
    ep, tl = load_voice()
    if abs(tl.total - timing["total"]) > 0.01:
        raise SystemExit(f"voice layout {tl.total:.3f} s != timing.json {timing['total']} s: re-run ep01v2_timing.py")
    total = timing["total"]
    n = int(round(total * SR))
    v = voice_track(tl, n)
    music, fx, ambience = build(timing, n, v)
    env = duck_env(v)
    music *= 1 - (1 - _db(-10)) * env                           # ~10 dB of sidechain duck while a word is heard
    fx = [f + a * (1 - (1 - _db(-8)) * env) for f, a in zip(fx, ambience)]   # ambience ~8 dB down under words
    stems = dict(voice=np.stack([v, v], 1), music=np.stack([music, signal.lfilter([0.6, 1], [1, 0.6], music)], 1),
                 sfx=np.stack(fx, 1))
    out_n = int(round(total * OUT_SR))
    stems = {k: to_out(x)[:out_n] for k, x in stems.items()}
    stems = {k: np.pad(x, ((0, out_n - len(x)), (0, 0))) for k, x in stems.items()}
    mix = sum(stems.values())
    a, b = int(0.01 * OUT_SR), int(0.02 * OUT_SR)               # click-free edges; the cut stays hard
    mix[:a] *= np.linspace(0, 1, a)[:, None]
    mix[-b:] *= np.linspace(1, 0, b)[:, None]
    meter = pyloudnorm.Meter(OUT_SR)
    g = _db(-14.0 - meter.integrated_loudness(mix))
    for _ in range(3):                                           # the limiter costs loudness: make it up and re-limit
        lim = limit(mix * g, -1.4)
        g *= _db(-14.0 - meter.integrated_loudness(lim))
    mix = limit(mix * g, -1.4)
    for k in stems:
        stems[k] = stems[k] * g
    pre = os.path.join(OUT, "mix_pre.wav")
    write_wav(pre, mix)
    m1, _ = loudnorm(pre, os.path.join(OUT, "mix.wav"))
    os.remove(pre)
    m = measure(os.path.join(OUT, "mix.wav"))
    for k, x in stems.items():
        write_wav(os.path.join(OUT, f"{k}.wav"), x)
    with wave.open(os.path.join(OUT, "mix.wav")) as w:
        dur = w.getnframes() / w.getframerate()
        info = (w.getframerate(), w.getnchannels(), dur)
    print(f"mix.wav: {info[0]} Hz, {info[1]} ch, {info[2]:.3f} s")
    print(f"pass 1: I {m1['input_i']} LUFS, TP {m1['input_tp']} dBTP, LRA {m1['input_lra']}")
    print(f"output: I {m['input_i']} LUFS, TP {m['input_tp']} dBTP, LRA {m['input_lra']}")
    return m


# ---------------------------------------------------------------- Whisper check

NUMBERS = {"10": "ten"}                                         # Whisper writes some numbers as digits


def _norm_words(s):
    s = s.lower().replace("’", "'")
    return [NUMBERS.get(w, w) for w in re.sub(r"[^a-z0-9' ]+", " ", s).split()]


def check(model_name="medium.en"):
    """Whisper every line out of mix.wav (its own window, the mix as heard) and compare with the script."""
    import whisper
    with open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")) as f:
        timing = json.load(f)
    model = whisper.load_model(model_name, device="cpu")
    audio = whisper.load_audio(os.path.join(OUT, "mix.wav"))     # 16 kHz mono
    bad = []
    for l in timing["lines"]:
        if not l["text"]:
            continue
        clip = audio[int(max(0, l["start"] - 0.15) * 16000): int((l["end"] + 0.25) * 16000)]
        r = model.transcribe(clip, language="en", temperature=0.0, condition_on_previous_text=False, fp16=False)
        heard, want = _norm_words(r["text"]), _norm_words(l["text"])
        ok = heard == want
        print(f"{l['id']:>4} {'OK ' if ok else 'BAD'} | {l['text']} | heard: {r['text'].strip()}")
        if not ok:
            bad.append((l["id"], l["text"], r["text"].strip()))
    print(f"{len(bad)} line(s) not heard as written")
    return bad


def roughcut():
    """Mux helper 8's picture.mp4 with mix.wav -> out/monsters/ep01v2/roughcut.mp4 (no re-encode of the picture)."""
    out = os.path.join(OUT, "roughcut.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(OUT, "picture.mp4"), "-i", os.path.join(OUT, "mix.wav"),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-map_metadata", "-1", "-fflags", "+bitexact", out], check=True)
    print(f"{os.path.relpath(out, ROOT)}: {os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
    if "--check" in sys.argv:
        check()
    if "--roughcut" in sys.argv:
        roughcut()
