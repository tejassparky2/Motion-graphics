"""Episode 1 v3 (2.5D diorama) sound mix -> out/monsters/ep01v3/mix.wav (48 kHz stereo, the v3 length).

    tar xf assets/voice_cache/monsters_ep01v2_takes.tar          # + the v3 takes tar (the new lines)
    python channels/monsters/ep01v3_sound.py [--check] [--roughcut]

It is ep01v2_sound.py with EPISODE = "ep01v3" and the v3 cue sheet below: the voice layout, the sidechain duck
(20/300 ms), the two-pass ffmpeg loudnorm to -14 LUFS / -1 dBTP, the stems and the Whisper medium.en check all come
from there. Every cue is (shot, frame) or (line, word) from channels/monsters/ep01v3/timing.json, so a re-timed cut
moves the sound with it. Frame numbers are 0-based in the cut; the ones marked "picture" are read from the shot
renders and are constants at the top so the shot owners can move them.

What v3 adds (DIORAMA_EP01_V3.md): the tank crack and the jet of water (S07), the pour, the splash and the plugs
fizzing (S08), the puddle under Kai's sneakers (S08a), the zap with a falling hum, the lights dying and the flatline
(S08b, into the black), the soul chime as the spark falls through the crack (S09), the aim (S15a), the smoking stump
and dazed stars (S15b), the wind-up and startle on the failed snap (S20), the bird's lock-on sting (S23b), the shadow
whoosh (S23c), and the A and B stingers on "Option A" / "Option B" (S24). Owner rules kept: no heartbeat (the monitor
gives one beep, then the flat tone) and no riser (stings climb in plucked steps over a held chord).
"""
import os
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters import ep01v2_sound as base                       # noqa: E402
from channels.monsters import sfx                                        # noqa: E402
from channels.monsters.sfx import SR, _bp, _exp, _hp, _lp, _midi, _n, _place, _pluck, _rng, _sweep, _t, _verb  # noqa

base.EPISODE = "ep01v3"
base.OUT = os.path.join(base.ROOT, "out", "monsters", "ep01v3")

# picture beats (0-based frames in the cut); the shots keep v2's beats unless their owner says otherwise
S04_SHUT, S05A_FLASH, S05B_TAPS = 19, 51, (29, 33)
S07_SNAP, S07_CRACK = None, None   # None: on the word "snap" / just after it, until helper 2's v3 render gives frames
S15_STRIKE, S15_FLASH, S15_DUST, S15_BLOWN = 41, 43, 49, 79     # helper 10's v2 beats; confirm for the v3 staging
S18_REALISE, S21_LANDINGS, S21_HUFF, S21_DIP, S23_GLINT = 29, (13, 21, 29), 4, 42, 62
# the v3 staging pass (coordinator, 31 Oct 12:25; provisional until the shot owners confirm the frames)
S06_FLASH = 13            # the strong near-white flash, 0-based f13-14 (helper 9; the crack on f13)
S08A_SPARKS = 28          # small sparks start fizzing at the plugs (helper 1)
S08B_LAND, S08B_BLACK = 28, 30   # helper 4 plan: limp from 0-based f23, lands ~f28, black f30 (exact frames to come)
S23B_LOCK = 19            # the snap-zoom and lock-on pose start (XprL: 1-based f20; peak f21 0-based)


# ---------------------------------------------------------------- v3 effects (original, seeded)

def water_jet(dur=0.8, seed=0):
    """A jet of water spitting through a crack: a hissing spray that settles into a gush."""
    r = _rng("water_jet", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    noise = r.uniform(-1, 1, n)
    spray = _bp(noise, 2500, 9000) * (0.6 + 0.4 * r.random(n))
    gush = _bp(noise, 300, 1800) * 0.7
    return (spray * np.exp(-p * 2) + gush * np.minimum(1, p / 0.2)) * np.minimum(1, p / 0.01) * np.minimum(1, (1 - p) / 0.15)


def water_pour(dur, seed=0):
    """A small waterfall off the desk edge: a steady splashy rush with bubbling plinks on top."""
    r = _rng("water_pour", seed)
    n = _n(dur)
    noise = r.uniform(-1, 1, n)
    rush = _bp(noise, 400, 5000) * (0.8 + 0.2 * np.sin(2 * np.pi * 3.1 * _t(n)))
    out = rush * 0.5 + _lp(noise, 250) * 0.3
    at = 0.0
    while at < dur:
        k = _n(0.04)
        f0 = r.uniform(600, 2000)
        _place(out, _sweep(f0 * (1 + 1.6 * _t(k))) * _exp(k, 0.01, 0.001) * r.uniform(0.2, 0.5), at)
        at += r.exponential(0.03)
    return out


def splash(seed=0):
    """Water hitting the floor tiles: a wet slap and a scatter of droplets."""
    r = _rng("splash", seed)
    out = np.zeros(_n(0.7))
    m = _n(0.15)
    _place(out, _bp(r.uniform(-1, 1, m), 300, 4000) * _exp(m, 0.04, 0.002), 0)
    for at in np.sort(r.uniform(0.03, 0.5, 14)):
        k = _n(0.03)
        _place(out, _sweep(r.uniform(1500, 3500) * (1 + 1.2 * _t(k))) * _exp(k, 0.006, 0.0005) * r.uniform(0.1, 0.4), at)
    return out


def plug_fizz(dur=1.2, seed=0):
    """Water reaching live plugs: a wet frying fizz with sharp little arcing pops."""
    r = _rng("plug_fizz", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    fry = _bp(r.uniform(-1, 1, n), 3000, 10000) * (r.random(n) > 0.85) * 1.5
    out = fry * np.minimum(1, p / 0.1) * np.minimum(1, (1 - p) / 0.2)
    at = 0.05
    while at < dur - 0.05:
        k = _n(r.uniform(0.004, 0.015))
        _place(out, _hp(r.uniform(-1, 1, k), 2000) * _exp(k, k / SR / 3, 0.0002) * r.uniform(0.6, 1.4), at)
        at += r.exponential(0.07)
    return out


def puddle_creep(dur=1.0, seed=0):
    """The puddle sliding under his sneakers: a soft wet creep and a little squelch."""
    r = _rng("puddle", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    wash = _bp(r.uniform(-1, 1, n), 300, 2500) * np.sin(np.pi * p) * 0.5
    sq = np.zeros(n)
    k = _n(0.12)
    _place(sq, _bp(r.uniform(-1, 1, k), 500, 1800) * _exp(k, 0.03, 0.005), dur * 0.6)
    return wash + sq


def zap(dur=1.1, seed=0):
    """The current through him: a hard buzzing arc that crackles, then a whine falling away as the power dies."""
    r = _rng("zap", seed)
    n = _n(dur)
    t = _t(n)
    buzz = signal.sawtooth(2 * np.pi * 100 * t) + 0.5 * signal.square(2 * np.pi * 50 * t)
    arcs = _hp(r.uniform(-1, 1, n), 2500) * (r.random(n) > 0.55)
    env = np.minimum(1, t / 0.01) * np.where(t < 0.6, 1.0, np.exp(-(t - 0.6) / 0.12))
    out = (_lp(buzz, 3500) * 0.5 + arcs * 0.6) * env
    whine = _sweep(2400 * np.exp(-t * 2.4) + 60) * np.exp(-t / 0.6) * 0.35          # the falling hum
    return out + whine


def flatline(dur=2.0, seed=0):
    """A monitor: one short beep, then the flat tone (no heartbeat), fading at the end."""
    n = _n(dur)
    t = _t(n)
    f = 1000.0
    tone = np.sin(2 * np.pi * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t)
    beep = (t < 0.12).astype(float)
    flat = (t >= 0.45).astype(float) * np.minimum(1, (dur - t) / 0.6)
    gate = np.clip(beep + flat, 0, 1)
    gate = _lp(gate, 200)                                         # click-free edges
    return tone * gate * 0.5


def soul_chime(dur=1.4, seed=0):
    """The soul spark falling through the crack: a soft descending run of glassy bells with a shimmer trail."""
    r = _rng("soul", seed)
    out = np.zeros(_n(dur + 1.2))
    notes = [96, 93, 91, 88, 86, 84]
    for k, m in enumerate(notes):
        _place(out, sfx._bell(_midi(m), 1.2, 0.7) * (0.5 - 0.04 * k), k * dur / len(notes))
    m = _n(dur)
    _place(out, _hp(r.uniform(-1, 1, m), 7000) * np.sin(np.pi * np.linspace(0, 1, m)) * 0.06, 0)
    return _verb(out, 0.35, 1.0)


def body_fall(seed=0):
    """Kai crumpling onto the wet floor: a soft heavy thud, a cloth rustle and a small splash."""
    r = _rng("body_fall", seed)
    out = np.zeros(_n(0.8))
    m = _n(0.35)
    t = _t(m)
    _place(out, np.tanh(_sweep(110 * np.exp(-t * 9) + 45) * 1.5) * np.exp(-t / 0.09), 0)
    k = _n(0.25)
    _place(out, _bp(r.uniform(-1, 1, k), 800, 5000) * _exp(k, 0.06, 0.004) * 0.35, 0.0)
    _place(out, splash(seed + 3) * 0.3, 0.01)
    return out


def eyes_open(seed=0):
    """His eyes snap open: a tiny bright 'ting'."""
    return sfx._bell(_midi(100), 0.5, 0.3) * 0.8


def aim(dur=0.8, seed=0):
    """The claw rising and swinging to aim: a low creaking swell and a cold glint at the end."""
    r = _rng("aim", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    creak = _bp(r.uniform(-1, 1, n), 200, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * p)) * np.sin(np.pi * p) * 0.4
    out = np.concatenate([creak, np.zeros(_n(0.8))])
    _place(out, sfx._bell(_midi(95), 0.8, 0.4) * 0.5 + sfx._bell(_midi(96), 0.8, 0.4) * 0.4, dur * 0.9)
    return out


def dazed(dur=1.6, seed=0):
    """Knocked-out stars circling: little high twinkles going round."""
    r = _rng("dazed", seed)
    out = np.zeros(_n(dur + 0.6))
    at = 0.0
    k = 0
    while at < dur:
        _place(out, sfx._bell(_midi((96, 100, 103, 100)[k % 4]), 0.4, 0.2) * 0.3 * (1 - at / dur * 0.5), at)
        at += 0.14
        k += 1
    return out


def startle(seed=0):
    """The shrimp startles at its dry claw: a tiny squeak with a hop."""
    return sfx.cute_chirp(1.9, 7 + seed) * 0.6


def lock_on(seed=0):
    """The bird locks on: a low dark hit under a cold, thin high 'shing' that rings."""
    n = _n(1.6)
    t = _t(n)
    hit = _sweep(70 * np.exp(-t * 3) + 40) * np.exp(-t / 0.35) * np.minimum(1, t / 0.01)
    shing = (np.sin(2 * np.pi * 3520 * t) + 0.6 * np.sin(2 * np.pi * 3730 * t)) * np.exp(-t / 0.5) * 0.25
    noise = _hp(_rng("lock_on", seed).uniform(-1, 1, n), 5000) * np.exp(-t / 0.08) * 0.3
    return _lp(hit, 300) * 0.9 + shing + noise


def shadow_whoosh(dur=1.4, seed=0):
    """A big wing-shadow sliding over: a slow, low, airy pass (no pitch rise)."""
    r = _rng("shadow", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    noise = r.uniform(-1, 1, n)
    body = _bp(noise, 120, 700) * np.sin(np.pi * p) ** 2
    air = _bp(noise, 700, 2500) * np.sin(np.pi * p) ** 3 * 0.4
    return body + air


def option_sting(which="A", seed=0):
    """The A / B card pop: a soft pop and a short plucked chord (A bright major, B darker minor)."""
    out = np.zeros(_n(1.2))
    _place(out, sfx.ui_select(seed).astype(np.float64) * 0.6, 0)
    chord = (72, 76, 79) if which == "A" else (69, 72, 76)
    for k, m in enumerate(chord):
        _place(out, _pluck(_midi(m), 1.0, 0.995, k + (0 if which == "A" else 5)) * 0.5, 0.02 * k)
    return _verb(out, 0.2, 0.6)


# ---------------------------------------------------------------- the v3 cue sheet

def build(timing, n, v):
    c = base.Cue(timing)
    total = n / SR
    music = np.zeros(n)
    fx = [np.zeros(n), np.zeros(n)]
    ambience = [np.zeros(n), np.zeros(n)]
    v_rms = base._rms(v[np.abs(v) > 0.01])
    db = base._db

    def music_at(x, t0, t1, d, fi=0.3, fo=0.4):
        base._span(music, x / base._rms(x) * v_rms * db(d), t0, t1, fi, fo)

    def amb(gen, t0, t1, d, fi=0.3, fo=0.3):
        for side in (0, 1):
            x = gen(t1 - t0 + 0.1, side)
            base._span(ambience[side], x / base._rms(x) * v_rms * db(d), t0, t1, fi, fo)

    def hit(x, at, d, pan=0.0):
        x = np.asarray(x, np.float64)
        x = x / (np.max(np.abs(x)) + 1e-12) * v_rms * db(d) * 4
        _place(fx[0], x * min(1.0, 1 - pan), at)
        _place(fx[1], x * min(1.0, 1 + pan), at)

    def hush(t0, t1, fade=0.06):
        i0, i1, f = int(t0 * SR), int(t1 * SR), _n(fade)
        for tr in (music, *fx, *ambience):
            tr[i0:i0 + f] *= np.linspace(1, 0, f)
            tr[i0 + f:i1] = 0

    # --- S01-S02: as v2 (frame 0 has sound)
    amb(lambda d, s: base.meadow_wind(d, s), 0.0, c.t("S02"), -20, 0.02, 0.15)
    amb(lambda d, s: base.crackle(d, 10 + s), 0.0, c.t("S02"), -24, 0.02, 0.15)
    music_at(base.bed("danger", c.t("S02") + 0.5, 1), 0.0, c.t("S02"), -18, 0.02, 0.15)
    hit(sfx.glitch(c.end("S02") - c.t("S02"), 0), c.t("S02"), -14)

    # --- the lab (SS7): rain, hum, bubbles, the lab bed; it all stops when the power dies (S08b)
    lab0 = c.t("S03a")
    power_off = c.f("S08b", S08B_BLACK)                           # the lights die: the black
    amb(lambda d, s: sfx.rain(d, s), lab0, power_off, -24, 0.4, 0.05)
    amb(lambda d, s: sfx.lab_hum(d, s), lab0, power_off, -28, 0.4, 0.05)
    amb(lambda d, s: sfx.aquarium_bubbles(d, s), lab0, c.t("S07"), -27, 0.4, 0.3)
    music_at(base.bed("lab", c.t("S08a") - lab0 + 0.5, 0), lab0, c.t("S08a"), -17, 0.5, 0.4)
    hit(base.slow_snap(), c.f("S04", S04_SHUT), -6)
    hiss0, collapse_t = c.f("S04", S04_SHUT) + 0.35, c.f("S05a", S05A_FLASH)
    amb(lambda d, s: base.bubble_hiss(d, 20 + s), hiss0, collapse_t, -22, 0.4, 0.05)
    hit(base.bubble_collapse(), collapse_t, -10)
    for k, (f, d) in enumerate(zip(S05B_TAPS, (-14, -19))):
        hit(base.glass_tap(k), c.f("S05b", f), d, 0.4)
    hit(sfx.thunder(), c.f("S06", S06_FLASH), -3)

    # --- S07: the panicked snap cracks the tank, a jet of water
    snap_t = c.f("S07", S07_SNAP) if S07_SNAP is not None else c.word("l7", "snap")
    crack_t = c.f("S07", S07_CRACK) if S07_CRACK is not None else snap_t + 0.08
    hit(startle(3), c.t("S07", 0.05), -22, -0.2)                  # it jolts at the start of "The shrimp panicked."
    hit(sfx.snap(1), snap_t, -4)
    hit(base.glass_crack(), crack_t, -6, 0.2)
    hit(base.glass_crack(1), crack_t + 0.12, -12, 0.25)           # the crack runs on across the glass
    hit(water_jet(0.9), crack_t + 0.15, -16, 0.2)

    # --- S08: the pour off the desk, the splash, the plugs fizz on "cables"
    amb(lambda d, s: water_pour(d, 30 + s), c.t("S08"), c.end("S08"), -21, 0.15, 0.3)
    hit(splash(), c.word("l8", "desk"), -16, -0.1)
    hit(plug_fizz(1.3), c.word("l8", "cables"), -18, 0.15)

    # --- S08a: the puddle under his sneakers, his face drops; the bed thins to a held tense pad
    amb(lambda d, s: base.trickle(d, 40 + s), c.t("S08a"), c.end("S08a"), -24, 0.2, 0.2)
    hit(puddle_creep(1.0), c.t("S08a", 0.1), -18)
    sp0 = c.f("S08a", S08A_SPARKS)                               # the plugs fizz at the end of the shot, swelling
    sp1 = c.t("S08b", 0.05)                                      # into the zap
    fz = plug_fizz(sp1 - sp0 + 0.2, 9) * np.linspace(0.35, 1.0, _n(sp1 - sp0 + 0.2))
    hit(fz, sp0, -22, 0.2)
    music_at(base.tense_tone(c.end("S08a") - c.t("S08a")), c.t("S08a"), c.end("S08a"), -20, 0.3, 0.2)

    # --- S08b: the zap and the falling hum under "That's how I died.", the power dies, black, the flatline
    zap_t = c.t("S08b", 0.05)
    land = c.f("S08b", S08B_LAND)
    power_off = c.f("S08b", S08B_BLACK)                           # the black
    zx = zap(land - zap_t + 0.25)
    zx[-_n(0.25):] *= np.linspace(1, 0.25, _n(0.25))              # the buzz ducks under the fall
    hit(zx, zap_t, -10)
    hit(body_fall(), land, -12)
    hit(sfx.spark(), power_off - 0.1, -16)
    hush(power_off, c.t("S09"))
    flat_t = power_off + 0.15
    hit(flatline(c.word("l11", "Then") - flat_t - 0.1), flat_t, -20)

    # --- S09: black, the crack of light, the soul falls, his eyes snap open, then the world (wonder)
    w0 = c.t("S09")
    hit(soul_chime(1.4), w0 + 0.05, -16)
    music_at(base.soft_pad(2.4, (60, 67, 72, 76), 0.1), w0, w0 + 2.4, -16, 0.5, 0.6)
    another = c.word("l11", "In")
    hit(eyes_open(), another - 0.25, -22)
    music_at(base.bed("wonder", c.t("S15a") - another + 1.0, 2), another, c.t("S15a"), -15, 0.4, 0.15)
    amb(lambda d, s: base.meadow_wind(d, 50 + s), w0 + 0.6, c.t("S15a"), -27, 0.6, 0.25)
    amb(lambda d, s: sfx.birds(d, 60 + s), another, c.t("S12"), -24, 0.5, 0.6)
    for k, (at, pitch) in enumerate([(c.t("S10a", 1.58), 1.6), (c.t("S10b", 0.74), 1.8)]):
        hit(sfx.cute_chirp(pitch, k), at, -16, (-0.3, 0.3)[k])
    hit(base.eerie_sting(), c.f("S11b", 6), -18)
    for k in range(4):
        hit(base.lap(k), c.t("S13", 0.12 + 0.22 * k), -24)

    # --- S15a: it looks right at him and aims; near-silence (SS2) into the snap
    strike = c.f("S15", S15_STRIKE)
    amb(lambda d, s: base.meadow_wind(d, 70 + s), c.t("S15a"), strike, -34, 0.2, 0.0)
    hit(aim(0.9), c.word("l17", "looked"), -18)
    for k, d in enumerate((0.75, 0.35)):
        hit(base.drip(k), strike - d, -22)
    hit(sfx.snap(2), strike, 0)
    hit(sfx.shockwave(), c.f("S15", S15_FLASH), 0)
    hit(sfx.erase(), c.f("S15", S15_DUST), -4)
    hit(base.ring_out(3.2), c.f("S15", S15_FLASH) + 0.3, -16)
    hit(sfx.whoosh(1), c.f("S15", S15_BLOWN) - 0.15, -14)

    # --- S15b: "It missed me by an inch." the smoking stump, dazed stars
    amb(lambda d, s: base.crackle(d, 80 + s), c.t("S15b"), c.end("S15b"), -26, 0.3, 0.3)
    hit(dazed(1.4), c.t("S15b", 0.1), -24)

    # --- S16-S19: quiet; the realisation; the held tense tone under the drying sun
    amb(lambda d, s: base.meadow_wind(d, 90 + s), c.t("S16"), c.t("S20"), -29, 1.0, 0.3)
    music_at(base.soft_pad(c.t("S19") - c.t("S16") + 0.4, (45, 52, 57, 60), 0.05, 1), c.t("S16"), c.t("S19") + 0.3,
             -21, 1.0, 0.4)
    hit(sfx._bell(_midi(91), 1.2, 0.6) + sfx._bell(_midi(98), 1.2, 0.5) * 0.6, c.f("S18", S18_REALISE), -20)
    music_at(base.tense_tone(c.end("S19") - c.t("S19")), c.t("S19"), c.end("S19"), -19, 0.5, 0.25)

    # --- S20: "It tried to finish me anyway." the wind-up, a tiny pff, the startle, silence for the deadpan
    pff_t = c.word("l24", "anyway", "end") + 0.55
    hit(sfx.whoosh(3), pff_t - 0.35, -26)
    hit(base.pff(), pff_t, -14)
    hit(startle(), pff_t + 0.3, -20, 0.2)
    amb(lambda d, s: base.meadow_wind(d, 100 + s), c.t("S20"), c.t("S21"), -38, 0.3, 0.3)

    # --- S21-S23: the smug strut and stomps, plucks back; the thorn tree; the bird and the glint
    amb(lambda d, s: base.meadow_wind(d, 110 + s), c.t("S21"), total, -28, 0.4, 0.02)
    hit(base.huff(), c.f("S21", S21_HUFF), -18)
    for k, (f, d) in enumerate(zip(S21_LANDINGS, (-17, -14, -10))):
        hit(base.stomp(k), c.f("S21", f), d, -0.1 + 0.1 * k)
    hit(base.drip(1), c.f("S21", S21_DIP), -18)
    music_at(base.bed("wonder", c.t("S22") - c.t("S21") + 1.0, 3), c.t("S21"), c.t("S22"), -16, 0.4, 0.3)
    music_at(base.soft_pad(c.t("S23b") - c.t("S22") + 0.3, (50, 57, 62, 63), 0.1, 2), c.t("S22"), c.t("S23b"), -19,
             0.4, 0.2)
    hit(base.flutter(0.6), c.t("S23", 0.2), -14, 0.15)
    hit(sfx._bell(_midi(96), 0.8, 0.4) + sfx._bell(_midi(103), 0.8, 0.3) * 0.5, c.f("S23", S23_GLINT), -22, 0.2)

    # --- S23b/S23c: it locks on to the shrimp; the shadow slides over; the shrimp keeps drinking
    hit(lock_on(), c.f("S23b", S23B_LOCK), -12)                # on the 2D snap-zoom
    music_at(base.bed("danger", c.t("S24") - c.t("S23b") + 0.5, 4), c.t("S23b"), c.t("S24"), -20, 0.3, 0.3)
    hit(shadow_whoosh(1.4), c.t("S23c", 0.1), -14, -0.2)
    for k in range(3):
        hit(base.lap(10 + k), c.t("S23c", 0.25 + 0.3 * k), -26)

    # --- S24: the split opens; the bed dips ~0.5 s before "Option A" (SS3); the A and B stingers; cut on the picture
    opt_a = c.word("l30", "Option")
    hit(sfx.whoosh(), c.t("S24") + 0.02, -10)
    words = timing_words(timing, "l30")
    a_t = next(w["start"] for w in words if w["w"].strip(".,:?!").upper() == "A")
    b_t = [w["start"] for w in words if w["w"].strip(".,:?!").upper() == "B"][0]
    comment = next(w["start"] for w in words if w["w"].lower().startswith("comment"))
    hit(option_sting("A"), a_t, -12, -0.15)
    hit(option_sting("B"), b_t, -12, 0.15)
    hit(sfx.ui_select(5), comment, -20)
    music_at(base.sting(total - opt_a), opt_a, total, -15, 0.25, 0.01)
    return music, fx, ambience


def timing_words(timing, line):
    return next(l for l in timing["lines"] if l["id"] == line)["words"]


base.build = build

if __name__ == "__main__":
    base.main()
    if "--check" in sys.argv:
        base.check()
    if "--roughcut" in sys.argv:
        base.roughcut()
