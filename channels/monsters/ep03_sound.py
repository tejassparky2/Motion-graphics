"""Cute Things Kill Here, Episode 3 ("They Rang Every Bell. The Moths Didn't Care") sound mix -> out/monsters/ep03/mix.wav
(48 kHz stereo).

    tar xf assets/voice_cache/monsters_ep03_takes.tar
    python channels/monsters/ep03_sound.py [--check] [--roughcut]

ep02_sound.py's way: ep01v2_sound.py with EPISODE = "ep03" and the cue sheet below. The voice layout comes from the
cached takes (it refuses to synthesise), then the sidechain duck (20/300 ms), the two-pass ffmpeg loudnorm to -14 LUFS
/ -1 dBTP, the stems and the Whisper medium.en check per line. Every cue is (shot, frame) or (line, word) from
channels/monsters/ep03/timing.json, so a re-timed cut moves the sound with it. Frames are 0-based in the cut. The
picture beats are constants at the top: word anchors and placeholders until each shot lands.

The cues (DIORAMA_EP03.md "The other passes", the coordinator 7 Nov 2026): the mark's flare and hum; Wren's stumble;
villagers' steps, doors and shutters slamming; the dusk (birds settling, crickets) and the night; the swarm's soft
fluffy wing flutter, growing; the wing-dust glitter; a scratch; every bell ringing, still ringing as the moths pass;
the orbit whoosh; Kai dropping into the grass; THE FLIP (TWIST = l14: the music drops a tick before; a held hush, then
soft comic plop-plop-plops and tiny dazed trills); Wren's last bell clink; her whisper on l18 (quieter and closer:
Turbo has no real whisper); the lake lapping; the lighthouse glow chime; the A/B stingers. Owner rules kept: every
sound original and synthesised, no heartbeat, no riser.
"""
import os
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters import ep02_sound as e2                           # noqa: E402  (its effects; it sets base)
from channels.monsters import ep01v2_sound as base                       # noqa: E402
from channels.monsters import ep01v3_sound as v3                         # noqa: E402
from channels.monsters import sfx                                        # noqa: E402
from channels.monsters.sfx import SR, _bp, _lp, _midi, _n, _place, _rng, _t, _verb  # noqa: E402

base.EPISODE = "ep03"
base.OUT = os.path.join(base.ROOT, "out", "monsters", "ep03")
WHISPER = "l18"            # Wren leans in: quieter and closer

# ---------------------------------------------------------------- picture beats (0-based frames in the cut)
# None = that shot hasn't landed: the cue sits on its word (or a time into the shot) instead.
S01_FLARE = 0              # the mark blazes from frame 0 (the hook)
S14_HUSH = 0.9             # seconds of held hush at the top of S14 before the first moth plops (placeholder)
S14_PLOPS = 1.5            # seconds the tumble lasts (placeholder)


# ---------------------------------------------------------------- the voice: l18 whispered, close

def _close_whisper(x):
    """Quieter and closer: ~4.5 dB down, the rumble off, presence and air up, a breath that follows the words."""
    sos = lambda kind, f: signal.butter(2, f, kind, fs=SR, output="sos")  # noqa: E731
    x = signal.sosfilt(sos("highpass", 110), x)
    presence = signal.sosfilt(signal.butter(2, (2000, 6000), "bandpass", fs=SR, output="sos"), x)
    air = signal.sosfilt(sos("highpass", 7000), x)
    env = signal.sosfilt(sos("lowpass", 25), np.abs(x))
    breath = _bp(np.random.default_rng(18).uniform(-1, 1, len(x)), 1500, 8000) * env * 0.35
    return (x + 0.35 * presence + 0.5 * air + breath) * 10 ** (-4.5 / 20)


def voice_track(tl, n):
    out = np.zeros(n)
    for b in tl.beats:
        if b.audio is None or not len(b.audio):
            continue
        x = np.asarray(b.audio, np.float64)
        _place(out, _close_whisper(x) if b.id == WHISPER else x, b.start)
    return out


base.voice_track = voice_track


# ---------------------------------------------------------------- effects (original, seeded)

def mark_hum(dur, seed=0):
    """The mark glowing: a warm low hum (two soft tones a fifth apart) with a slow shimmer on top."""
    r = _rng("markhum", seed)
    n = _n(dur)
    t = _t(n)
    hum = np.sin(2 * np.pi * 98 * t) + 0.6 * np.sin(2 * np.pi * 147 * t + 0.4) + 0.25 * np.sin(2 * np.pi * 196 * t)
    hum *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.6 * t + seed)
    shimmer = _bp(r.uniform(-1, 1, n), 3000, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 1.3 * t)) * 0.05
    return (hum * 0.4 + shimmer) * np.minimum(1, t / 0.2) * np.minimum(1, (dur - t) / 0.4)


def flare(seed=0):
    """The mark blazing up: a bright bloom of shimmer over a soft low swell."""
    out = e2.glow_chime(seed) * 0.8
    n = _n(1.2)
    t = _t(n)
    swell = np.sin(2 * np.pi * 98 * t) * np.minimum(1, t / 0.05) * np.exp(-t / 0.5) * 0.5
    _place(out, swell, 0)
    return out


def stumble(seed=0):
    """Wren stumbling back: two quick scuffs on the lane and her bell knocked."""
    r = _rng("stumble", seed)
    out = np.zeros(_n(1.2))
    for k, at in enumerate((0.0, 0.17)):
        m = _n(0.2)
        _place(out, _bp(r.uniform(-1, 1, m), 500, 4000) * np.exp(-_t(m) / 0.05) * (1 - 0.3 * k), at)
        _place(out, e2.footstep(40 + k, 1.1), at + 0.01)
    _place(out, e2.bell_clank(seed) * 0.8, 0.06)
    return out


def door_slam(seed=0, shutter=False):
    """A wooden door (or a pair of shutters) banging shut: a low wooden thud, a latch click and a short rattle."""
    r = _rng("door", seed)
    n = _n(0.7)
    t = _t(n)
    f = 95 if not shutter else 170
    body = np.sin(2 * np.pi * f * t) * np.exp(-t / (0.09 if not shutter else 0.05))
    knock = _lp(r.uniform(-1, 1, n), 1800 if not shutter else 3000) * np.exp(-t / 0.025)
    out = (body * 0.8 + knock) * np.minimum(1, t / 0.002)
    for k in range(2 if shutter else 1):                                 # the latch, or the second shutter leaf
        m = _n(0.03)
        _place(out, _bp(r.uniform(-1, 1, m), 2500, 7000) * np.exp(-_t(m) / 0.005) * 0.5, 0.05 + 0.07 * k)
    return _verb(out, 0.15, 0.7)


def crickets(dur, seed=0):
    """Night crickets: a few insects chirping pulse trains at slightly different pitches and rates."""
    r = _rng("crickets", seed)
    n = _n(dur)
    out = np.zeros(n)
    for k in range(4):
        f = r.uniform(4200, 5200)
        rate = r.uniform(1.4, 2.6)                                       # chirps a second
        pulses = int(r.integers(3, 5))
        at = r.uniform(0, 1 / rate)
        amp = r.uniform(0.25, 1.0)
        while at < dur:
            for p in range(pulses):
                m = _n(0.012)
                tt = _t(m)
                _place(out, np.sin(2 * np.pi * f * tt) * np.sin(np.pi * tt / tt[-1]) * amp, at + p * 0.022)
            at += 1 / rate * r.uniform(0.9, 1.1)
    return _verb(out, 0.2, 0.8)


def night(dur, seed=0):
    """The night island: crickets, a soft low wind, now and then a far frog."""
    r = _rng("night", seed)
    n = _n(dur)
    out = crickets(dur, seed)[:n] * 0.7 + base.meadow_wind(dur, 300 + seed)[:n] * 0.35
    at = r.uniform(0.5, 1.5)
    while at < dur - 0.3:
        m = _n(0.18)
        tt = _t(m)
        croak = np.sign(np.sin(2 * np.pi * 180 * tt)) * np.sin(np.pi * tt / tt[-1]) * 0.08
        _place(out, _lp(croak, 900), at)
        at += r.uniform(1.5, 3.5)
    return out


def dusk(dur, seed=0):
    """The dusk: birdsong thinning out (they settle), crickets coming in."""
    n = _n(dur)
    t = _t(n)
    fade = np.clip(1 - t / dur, 0, 1) ** 1.5
    birdsong = sfx.birds(dur, 50 + seed).astype(np.float64)[:n]
    return birdsong * fade * 1.2 + crickets(dur, seed)[:n] * (1 - fade) * 0.6 + base.meadow_wind(dur, seed)[:n] * 0.3


def swarm(dur, grow=(0.2, 1.0), seed=0):
    """The fluffmoths: many soft, fluffy wing flutters (felt more than heard), swelling from grow[0] to grow[1]."""
    r = _rng("swarm", seed)
    n = _n(dur)
    t = _t(n)
    out = np.zeros(n)
    for k in range(9):
        rate = r.uniform(11, 19)                                          # wing beats a second (big soft wings)
        ph = 2 * np.pi * np.cumsum(rate * (1 + 0.05 * np.sin(2 * np.pi * r.uniform(0.2, 0.6) * t))) / SR
        pulses = np.maximum(0, np.sin(ph + r.uniform(0, 6))) ** 2
        out += _bp(r.uniform(-1, 1, n), 150, 1400) * pulses * r.uniform(0.5, 1.0)
    out = _lp(out, 1600)
    level = grow[0] + (grow[1] - grow[0]) * t / dur
    return out * level * np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.3)


def glitter(dur, seed=0):
    """Wing dust drifting down: sparse tiny high glints, airy."""
    r = _rng("glitter", seed)
    out = np.zeros(_n(dur + 0.5))
    at = r.uniform(0, 0.1)
    while at < dur:
        m = _n(0.08)
        tt = _t(m)
        _place(out, np.sin(2 * np.pi * r.uniform(6000, 9500) * tt) * np.exp(-tt / 0.02) * r.uniform(0.3, 1.0), at)
        at += r.exponential(0.07)
    return _verb(out, 0.5, 1.2)


def scratch(strokes=4, seed=0):
    """A villager scratching an itchy arm: quick rough strokes of nails on skin and sleeve."""
    r = _rng("scratch", seed)
    out = np.zeros(_n(0.16 * strokes + 0.3))
    for k in range(strokes):
        m = _n(0.11)
        env = np.sin(np.pi * np.linspace(0, 1, m)) ** 0.7
        grain = (r.uniform(0, 1, m) > 0.6) * 1.0
        _place(out, _bp(r.uniform(-1, 1, m) * (0.5 + grain), 1800, 7000) * env * (1 if k % 2 else 0.8), 0.15 * k)
    return out


def all_bells(dur, seed=0):
    """Every bell in the village ringing: Wren's close and loud, the porch bells round about, far ones roomier."""
    out = e2.bell_peal(dur, seed) * 0.7
    at = 0.0
    k = 0
    while at < dur:
        _place(out, e2.hand_bell(86 + (k % 2) * 2, seed + k), at)           # Wren, both hands, hard
        at += 0.24
        k += 1
    return out


def orbit_whoosh(dur, turns=2, seed=0):
    """The swarm circling: a soft air whoosh that swings round left-right-left. Returns (left, right)."""
    r = _rng("orbit", seed)
    n = _n(dur)
    t = _t(n)
    air = _bp(r.uniform(-1, 1, n), 300, 2500)
    ang = 2 * np.pi * turns * t / dur
    loud = 0.55 + 0.45 * np.cos(ang)                                     # nearer at the front of the circle
    pan = np.sin(ang)
    x = air * loud * np.sin(np.pi * t / dur) ** 0.6
    return x * np.clip(1 - pan, 0, 1), x * np.clip(1 + pan, 0, 1)


def drop_to_grass(seed=0):
    """Kai dropping flat on his back in the grass: a soft heavy thud and a long swish of grass."""
    r = _rng("grass", seed)
    out = np.zeros(_n(0.9))
    m = _n(0.35)
    t = _t(m)
    _place(out, np.tanh(np.sin(2 * np.pi * (100 * np.exp(-t * 9) + 45) * t) * 1.5) * np.exp(-t / 0.1), 0.05)
    k = _n(0.5)
    _place(out, _bp(r.uniform(-1, 1, k), 1200, 6000) * np.sin(np.pi * np.linspace(0, 1, k)) * 0.4, 0.0)
    return out


def plop(seed=0):
    """One moth landing on its back in the grass: a soft comic plop with a tiny puff."""
    r = _rng("plop", seed)
    n = _n(0.25)
    t = _t(n)
    f = r.uniform(260, 420)
    body = np.sin(2 * np.pi * (f * np.exp(-t / 0.04) + 0.45 * f) * t) * np.minimum(1, t / 0.003) * np.exp(-t / 0.05)
    puff = _lp(r.uniform(-1, 1, n), 1500) * np.exp(-t / 0.03) * 0.25
    return body + puff


def plops(dur, count=16, seed=0):
    """The swarm tumbling into the grass: plop, plop, plop, thick in the middle, one late straggler."""
    r = _rng("plops", seed)
    out = np.zeros(_n(dur + 0.5))
    times = np.sort(r.beta(2.0, 2.4, count - 1) * dur * 0.9)
    for k, at in enumerate(list(times) + [dur * 0.97]):
        _place(out, plop(seed * 100 + k) * r.uniform(0.5, 1.0), at)
    return out


def dazed_trills(dur, seed=0):
    """Tiny dazed trills from the upside-down moths: soft wobbly little chirps, scattered."""
    r = _rng("trills", seed)
    out = np.zeros(_n(dur + 0.4))
    at = r.uniform(0, 0.2)
    while at < dur:
        m = _n(r.uniform(0.18, 0.3))
        tt = _t(m)
        f = r.uniform(1700, 2600) * (1 - 0.2 * tt / tt[-1]) * (1 + 0.06 * np.sin(2 * np.pi * 22 * tt))
        _place(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) * r.uniform(0.4, 1.0), at)
        at += r.uniform(0.15, 0.45)
    return _verb(out, 0.25)


def last_clink(seed=0):
    """Wren's bell lowered: one small soft clink, damped by her hand."""
    n = _n(0.6)
    t = _t(n)
    return sfx._bell(_midi(86), 0.6, 0.25)[:n] * np.exp(-t / 0.12)


def lighthouse_chime(seed=0):
    """The faint coral glow in the lighthouse, far across the lake: a low soft chime, distant and roomy."""
    out = np.zeros(_n(2.6))
    for k, m in enumerate((74, 81, 86)):
        _place(out, sfx._bell(_midi(m), 2.0, 0.9) * (0.8 - 0.2 * k), 0.12 * k)
    return _verb(_lp(out, 4000), 0.55, 1.4)


# ---------------------------------------------------------------- the cue sheet

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

    def bed(x, t0, d, pan=0.0):
        """A long effect (a swarm, the bells) set by its RMS, not its peak."""
        x = np.asarray(x, np.float64)
        x = x / base._rms(x) * v_rms * db(d)
        _place(fx[0], x * min(1.0, 1 - pan), t0)
        _place(fx[1], x * min(1.0, 1 + pan), t0)

    words = {l["id"]: v3.timing_words(timing, l["id"]) for l in timing["lines"]}

    def w(line, word, edge="start"):
        return c.word(line, word, edge)

    s = c.t
    twist = s("S14")

    # --- the ambience: evening village S01-S03, the dusk S04, night from S05 (crickets; the hush in S14)
    amb(lambda d, k: base.meadow_wind(d, k), 0.0, s("S04"), -27, 0.02, 0.4)
    amb(lambda d, k: dusk(d, k), s("S04"), s("S05") + 0.3, -24, 0.3, 0.4)
    amb(lambda d, k: night(d, k), s("S05"), twist - 0.05, -25, 0.4, 0.25)
    amb(lambda d, k: night(d, 10 + k), twist + S14_HUSH + 0.4, s("S18") + 1.0, -27, 1.2, 0.6)
    amb(lambda d, k: e2.lake(d, k), s("S18"), total, -22, 0.6, 0.02)        # the lake lapping, to the end

    # --- the mark: it blazes on frame 0 and hums under the whole night
    hit(flare(), c.f("S01", S01_FLARE), -12, -0.2)
    music_at(mark_hum(total, 1), 0.0, total, -30, 0.02, 0.3)              # under everything, quietly
    hit(stumble(), c.f("S01", 0) + 0.25, -17, 0.3)                        # Wren stumbles back, bell knocked
    for k in range(6):                                                    # villagers scattering, nets dropped
        hit(e2.footstep(60 + k, 0.7), 0.35 + 0.22 * k, -27, 0.5 - 0.15 * k)

    # --- music: tense S01-S03, a dusk pad S04-S05, the swarm's danger bed S06-S09, the orbit S10-S13,
    #     the TWIST drop a tick before S14, a soft comic pad from the laugh, Wren's tender pad, the A/B sting
    music_at(base.tense_tone(s("S04") + 0.3, 1), 0.0, s("S04"), -21, 0.02, 0.5)
    music_at(base.soft_pad(s("S06") - s("S04") + 0.6, (52, 59, 64, 67), 0.08, 2), s("S04"), s("S06"), -20, 0.5, 0.4)
    music_at(base.bed("danger", s("S10") - s("S06") + 0.6, 7), s("S06"), s("S10"), -19, 0.4, 0.3)
    music_at(base.tense_tone(twist - s("S10") + 0.3, 6), s("S10"), twist - 0.1, -19, 0.3, 0.06)
    music_at(base.soft_pad(s("S17") - s("S15") + 0.6, (60, 64, 67, 72), 0.15, 8), s("S15") + 0.3, s("S17"),
             -22, 0.8, 0.4)
    music_at(base.soft_pad(s("S19") - s("S17") + 0.6, (57, 64, 69, 72), 0.08, 9), s("S17"), s("S19"), -21, 0.5, 0.4)
    opt_a = w("l19", "Option")
    music_at(base.sting(total - opt_a), opt_a, total, -15, 0.25, 0.01)

    # --- S02: Wren: "Marked." The sky crack
    hit(e2.rift_hum(s("S03") - w("l2", "sky") + 0.3, 2), w("l2", "sky"), -24, 0.0)
    hit(base.eerie_sting(3), w("l2", "cracked"), -21, 0.0)

    # --- S03: the village backs away: steps, doors and shutters banging shut
    for k in range(8):
        hit(e2.footstep(80 + k, 0.8), s("S03") + 0.1 + 0.2 * k, -25, 0.6 - 0.15 * k)
    bangs = [(0.5, False, -0.5), (0.9, True, 0.6), (1.3, False, 0.3), (1.65, True, -0.4), (2.1, True, 0.1)]
    for k, (at, sh, pan) in enumerate(bangs):
        if s("S03") + at < s("S04") - 0.1:
            hit(door_slam(k, sh), s("S03") + at, -16 - 2 * (k % 2), pan)

    # --- S04-S05: the sun goes down (the mark brightens), the only light for miles
    hit(e2.glow_chime(4), w("l4", "down"), -20, -0.1)
    hit(e2.glow_chime(5), w("l5", "light"), -22, 0.0)

    # --- S06-S09: the swarm comes down the hill, growing; wing dust; the scratch; every bell rings
    bed(swarm(s("S10") - s("S06") + 0.5, (0.15, 0.7), 1), s("S06"), -20, 0.1)
    hit(base.flutter(0.5, 6), w("l6", "fluffmoths"), -20, 0.2)           # close on one: its eye-spots open
    bed(glitter(s("S08") - s("S07"), 2), s("S07"), -28, 0.0)
    hit(scratch(4, 1), w("l7", "stings"), -20, 0.4)
    hit(e2.cloth_swish(0.4, 7), w("l7", "nettles"), -22, -0.3)           # Wren pulls her cape over her face
    bells_from = w("l8", "Ring")
    bed(all_bells(s("S10") - bells_from + 0.6, 3), bells_from, -17, 0.15)  # still ringing as the moths pass
    hit(base.ring_out(2.0), s("S10") - 0.1, -26, 0.15)

    # --- S10-S13: the orbit; the backs to the light; Kai drops into the grass
    orb_t0, orb_t1 = s("S10"), s("S13")
    ol, orr = orbit_whoosh(orb_t1 - orb_t0, 4, 1)
    for ch, x in enumerate((ol, orr)):
        y = x / base._rms(x) * v_rms * db(-24)
        _place(fx[ch], y, orb_t0)
    bed(swarm(orb_t1 - orb_t0 + 0.6, (0.7, 1.0), 2), orb_t0, -21, 0.0)
    hit(base.flutter(0.4, 11), w("l11", "backs"), -24, 0.2)
    bed(swarm(twist - orb_t1 + 0.2, (1.0, 1.1), 3), orb_t1, -21, 0.0)
    hit(drop_to_grass(), w("l13", "put"), -14, 0.0)

    # --- S14: THE FLIP (TWIST): a held hush, then plop-plop-plop, then tiny dazed trills
    plops_at = twist + S14_HUSH
    hit(sfx.whoosh(1) * 0.6, plops_at - 0.25, -24, 0.0)                   # the whole swarm rolling over
    bed(plops(S14_PLOPS, 18, 1), plops_at, -15, 0.0)
    bed(dazed_trills(s("S16") - plops_at - S14_PLOPS + 0.5, 1), plops_at + S14_PLOPS * 0.7, -26, 0.1)

    # --- S16-S18: the bell lowered (a last clink), Wren kneels, whispers; the lighthouse
    hit(last_clink(), w("l16", "bell", "end") + 0.1, -21, 0.2)
    hit(lighthouse_chime(), w("l18", "lighthouse"), -19, 0.2)

    # --- S19: the A and B stingers on the letters; "Comment" blip
    wl = words["l19"]
    a_t = next(x["start"] for x in wl if x["w"].strip(".,:?!").upper() == "A")
    b_t = next(x["start"] for x in wl if x["w"].strip(".,:?!").upper() == "B")
    comment = next(x["start"] for x in wl if x["w"].lower().startswith("comment"))
    hit(sfx.whoosh(), s("S19") + 0.02, -12)
    hit(v3.option_sting("A"), a_t, -12, -0.15)
    hit(v3.option_sting("B"), b_t, -12, 0.15)
    hit(sfx.ui_select(5), comment, -20)

    # --- the whisper (l18): the world draws back 5 dB more so she sounds close
    l = c.line[WHISPER]
    for tr in (music, *fx, *ambience):
        i0, i1, r = int((l["start"] - 0.15) * SR), int((l["end"] + 0.1) * SR), _n(0.12)
        g = np.ones(len(tr))
        g[i0:i1] = db(-5)
        g[i0 - r:i0] = np.linspace(1, db(-5), r)
        g[i1:i1 + r] = np.linspace(db(-5), 1, r)
        tr *= g
    return music, fx, ambience


base.build = build

if __name__ == "__main__":
    base.main()
    if "--check" in sys.argv:
        base.check()
    if "--roughcut" in sys.argv:
        base.roughcut()
