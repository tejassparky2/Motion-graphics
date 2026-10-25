"""Horror sound design for the 3D horror channel: room tones and effects, all synthesized with numpy (no samples).
Importing this module registers them with motion.audio (EXTRA_SFX) under the names the episodes cue."""
import numpy as np

from motion import audio
from motion.audio import SR, _env, _lowpass, _thud

_rng = np.random.default_rng(13)


def _noise(n):
    return _rng.uniform(-1, 1, n)


def _band(x, lo, hi):
    """Crude band-pass: difference of two moving averages (lo/hi are window lengths in samples, lo < hi)."""
    return _lowpass(x, lo) - _lowpass(x, hi)


def _fade(x, a=0.3, b=0.6):
    n = len(x)
    e = np.ones(n)
    ia, ib = min(n, int(a * SR)), min(n, int(b * SR))
    e[:ia] = np.linspace(0, 1, ia)
    if ib:
        e[-ib:] *= np.linspace(1, 0, ib)
    return x * e


def hum(dur):
    """Elevator: mains hum and a fluorescent buzz."""
    n = int(max(1, dur) * SR)
    t = np.arange(n) / SR
    x = 0.5 * np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 100 * t) + 0.08 * np.sign(np.sin(2 * np.pi * 100 * t))
    return _fade(x * (0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t)) * 0.12)


def chime(dur):
    """The floor chime: two soft bell tones, the second lower (something arrived)."""
    out = np.zeros(int(1.8 * SR))
    for k, f in enumerate((659.3, 523.3)):
        m = int(1.3 * SR)
        t = np.arange(m) / SR
        tone = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 6)) * np.exp(-t * 2.2)
        i = int(k * 0.45 * SR)
        out[i:i + m] += tone
    return out * 0.35


def doors(dur):
    """Sliding/folding doors: a motor whine over a rumble, ending in a thunk."""
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    whine = np.sin(2 * np.pi * np.cumsum(260 + 60 * np.sin(np.pi * t / 1.4)) / SR) * 0.08
    rum = _lowpass(_noise(n), 30) * 0.6
    x = (whine + rum) * np.sin(np.pi * np.clip(t / 1.2, 0, 1))
    end = _thud(0.3, 120, 60, 0.05, 0.5) * 0.5
    i = int(1.1 * SR)
    x[i:i + len(end)] += end[: n - i]
    return x


def power_down(dur):
    """The lights die: a falling whine, a relay clunk, then the emergency relay clicks on."""
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 2.5) + 40
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.8) * 0.25
    clunk = _thud(0.4, 90, 40, 0.08, 0.9)
    x[: len(clunk)] += clunk * 0.9
    click = _band(_noise(int(0.02 * SR)), 1, 4) * 0.8
    i = int(0.6 * SR)
    x[i:i + len(click)] += click
    return x


def drip(dur):
    """Water dripping somewhere in the dark (wet footprints)."""
    n = int(max(2, dur if dur else 4) * SR)
    out = np.zeros(n)
    for at in (0.0, 1.3, 2.1, 3.4):
        i = int(at * SR)
        m = int(0.15 * SR)
        if i + m > n:
            break
        t = np.arange(m) / SR
        out[i:i + m] += np.sin(2 * np.pi * np.cumsum(np.linspace(1400, 2200, m)) / SR) * np.exp(-t * 40) * 0.3
    return out


def cable(dur):
    """A steel cable slips: a groan, a bang, the car swinging and creaking."""
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    groan = np.sin(2 * np.pi * np.cumsum(70 + 30 * np.sin(2 * np.pi * 1.3 * t)) / SR)
    groan = np.sign(groan) * np.abs(groan) ** 0.5 * np.exp(-t * 1.2) * 0.25
    bang = _thud(1.2, 70, 25, 0.25, 1.0)
    out = groan
    out[: len(bang)] += bang * 1.1
    squeal = np.sin(2 * np.pi * np.cumsum(2200 + 300 * np.sin(2 * np.pi * 5 * t)) / SR) * np.exp(-t * 3) * 0.05
    return out + squeal


def click(dur):
    """A counter clicking up: a dry mechanical tick."""
    m = int(0.05 * SR)
    return _band(_noise(m), 1, 6) * np.exp(-np.arange(m) / (0.006 * SR)) * 0.6


def engine_idle(dur):
    """A diesel bus: a low uneven rumble with a rattle (the bed under the whole episode)."""
    n = int(max(1, dur) * SR)
    t = np.arange(n) / SR
    f = 31 + 2 * np.sin(2 * np.pi * 0.2 * t)
    putt = np.sin(2 * np.pi * np.cumsum(f) / SR)
    putt = np.sign(putt) * np.abs(putt) ** 0.3
    x = _lowpass(putt, 60) * 0.8 + _lowpass(_noise(n), 90) * 0.5
    rattle = _band(_noise(n), 3, 12) * (0.5 + 0.5 * np.sin(2 * np.pi * f * 2 * t)) * 0.05
    return _fade((x + rattle) * 0.16, 0.5, 1.0)


def dip(dur):
    """The bus suspension sinking under a weight: a heavy creak and a thud."""
    out = audio.thriller_sfx("creak", 0.8) * 0.8
    th = _thud(0.6, 60, 30, 0.12, 0.8)
    out[: len(th)] += th * 1.2
    return out


def breath(dur):
    """A slow, close exhale behind your ear."""
    n = int(1.4 * SR)
    p = np.linspace(0, 1, n)
    return _band(_noise(n), 3, 25) * np.sin(np.pi * p) ** 1.5 * 1.4


def brakes(dur):
    """Air brakes: a squeal and a long hiss."""
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    squeal = np.sin(2 * np.pi * np.cumsum(1800 - 300 * t / 2.2) / SR) * np.exp(-t * 2) * 0.08
    hiss = _band(_noise(n), 1, 3) * np.clip((t - 0.8) * 4, 0, 1) * np.exp(-(t - 0.8).clip(0) * 1.4) * 0.5
    return squeal + hiss


def rain(dur):
    """Rain on a roof and in the trees, with a few heavier drops."""
    n = int(max(1, dur) * SR)
    x = _lowpass(_noise(n), 3) * 0.5 + _lowpass(_noise(n), 14) * 0.6
    drops = (_rng.random(n) > 0.9993) * _rng.uniform(0.3, 1, n)
    x += _band(drops, 1, 8) * 2
    return _fade(x * 0.2, 1.0, 1.0)


def generator(dur):
    """A small generator chugging below the cabin."""
    n = int(max(1, dur) * SR)
    t = np.arange(n) / SR
    f = 22 + 0.6 * np.sin(2 * np.pi * 0.13 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = _lowpass(np.sign(x) * np.abs(x) ** 0.4, 40)
    return _fade(x * 0.12, 0.5, 1.0)


def static(dur):
    """A radio squelch: a burst of crackling static."""
    n = int(max(0.2, dur) * SR)
    x = _band(_noise(n), 1, 5) * (0.6 + 0.4 * (_rng.random(n) > 0.995))
    crackle = (_rng.random(n) > 0.997) * _rng.uniform(-1, 1, n) * 2
    return _fade((x + crackle) * 0.35, 0.01, 0.08)


def thunder(dur):
    """A close lightning strike: a crack, then a long rolling rumble."""
    n = int(4.5 * SR)
    t = np.arange(n) / SR
    crack = _band(_noise(n), 1, 4) * np.exp(-t * 18) * 1.2
    roll = _lowpass(_noise(n), 120) * 6 * np.exp(-t * 0.8) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.9 * t + 1))
    return (crack + roll) * 0.7


def ladder_step(dur):
    """A slow step on a steel ladder rung: a dull clank."""
    m = int(0.5 * SR)
    t = np.arange(m) / SR
    ring = (np.sin(2 * np.pi * 410 * t) + 0.6 * np.sin(2 * np.pi * 1130 * t)) * np.exp(-t * 14) * 0.25
    return ring + _thud(0.5, 110, 50, 0.05, 0.6)[:m] * 0.6


def horror_bed(total, seed=None):
    """The horror bed, different for every episode (YouTube's spam policy names "the exact same background music"
    across many videos as a sign of mass production): a low drone in an episode-specific key whose two voices beat
    at an episode-specific rate, a slow pulse, a cold high tone that comes and goes, and air; it tightens toward
    the end. Key, beat rate, pulse tempo, high interval and air colour all come from the episode name."""
    import zlib
    r = np.random.default_rng(zlib.crc32(str(seed).encode()))
    n = int(total * SR) + SR
    t = np.arange(n) / SR
    root = 41.2 * 2 ** (int(r.integers(0, 9)) / 12)            # E1 .. C2
    beat = float(r.uniform(0.35, 1.2))
    rise = 0.55 + 0.45 * np.clip(t / max(total, 1), 0, 1) ** 1.5
    low = (np.sin(2 * np.pi * root * t) + np.sin(2 * np.pi * (root + beat) * t)
           + 0.45 * np.sin(2 * np.pi * root * float(r.choice([1.5, 1.498, 1.414])) * t)) * 0.45
    bpm = float(r.uniform(48, 64))                             # a slow pulse, like a heartbeat far away
    ph = (t * bpm / 60) % 1
    pulse = np.sin(2 * np.pi * root * 2 * t) * np.exp(-ph * 9) * 0.35
    hi_f = root * 2 ** (float(r.choice([35, 36, 37, 41, 42])) / 12)
    hi = np.sin(2 * np.pi * (hi_f + 4 * np.sin(2 * np.pi * 0.09 * t)) * t) * 0.05 * (0.5 + 0.5 * np.sin(2 * np.pi * float(r.uniform(0.04, 0.09)) * t))
    air = _lowpass(_noise(n), int(r.integers(40, 90))) * 0.35 * (0.6 + 0.4 * np.sin(2 * np.pi * float(r.uniform(0.07, 0.15)) * t))
    return ((low + pulse + air) * rise + hi)[: int(total * SR)] * 0.16


audio.EXTRA_BEDS["horror"] = horror_bed
audio.EXTRA_SFX.update(hum=hum, chime=chime, doors=doors, power_down=power_down, drip=drip, cable=cable, click=click,
                       engine_idle=engine_idle, dip=dip, breath=breath, brakes=brakes, rain=rain, generator=generator,
                       static=static, thunder=thunder, ladder_step=ladder_step)
# beds sit low under the narration (in Tower 9 the rain masked "voice" as "point")
audio.GAINS.update(hum=0.4, chime=0.6, rain=0.3, engine_idle=0.45, generator=0.3, static=0.5, thunder=0.7, sting=0.8,
                   heartbeat=0.7, riser=0.6, click=0.6, drip=0.5)
