"""Cute Things Kill Here, Episode 2 ("I Saved the Shrimp That Tried to Kill Me") sound mix -> out/monsters/ep02/mix.wav
(48 kHz stereo, 57.34 s).

    tar xf assets/voice_cache/monsters_ep02_takes.tar
    python channels/monsters/ep02_sound.py [--check] [--roughcut]

It is ep01v2_sound.py with EPISODE = "ep02" and the cue sheet below, as ep01v3_sound.py does it: the voice layout from
the cached takes (it refuses to synthesise), the sidechain duck (20/300 ms), the two-pass ffmpeg loudnorm to -14 LUFS
/ -1 dBTP, the stems and the Whisper medium.en check per line. Every cue is (shot, frame) or (line, word) from
channels/monsters/ep02/timing.json, so a re-timed cut moves the sound with it. Frames are 0-based in the cut. The
picture beats are constants at the top: word anchors and placeholders until each shot's owner gives the exact frame.

The cues (DIORAMA_EP02.md, the coordinator 1 Nov 2026): the bird's dive whoosh, the talon swipe and the sleeve tear;
the wet drip; the wind-up hush and THE SNAP with its shockwave (TWIST = l9: the music drops a tick before the shot);
the thorn-bush crash, dazed tweets and the fluff "poomf"; the nose-tap "tink" and the wrist-glow chime; the bells
(S16), Wren's steps (S17) and the lake (S19); the A and B stingers on "Option A" / "Option B". Owner rules kept: every
sound original and synthesised, no heartbeat, no riser (swells stay on one pitch band; stings climb in plucked steps).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters import ep01v2_sound as base                       # noqa: E402
from channels.monsters import ep01v3_sound as v3                         # noqa: E402  (its effects; it sets base)
from channels.monsters import sfx                                        # noqa: E402
from channels.monsters.sfx import SR, _bp, _hp, _lp, _midi, _n, _place, _rng, _t, _verb  # noqa: E402

base.EPISODE = "ep02"
base.OUT = os.path.join(base.ROOT, "out", "monsters", "ep02")
base._whisper_line = lambda x: x          # Episode 1's line 1 was whispered; Episode 2's is spoken in full

# ---------------------------------------------------------------- picture beats (0-based frames in the cut)
# Read from the final shots in out/monsters/diorama_ep02/shots/ (2 Nov); "placeholder" = that shot hasn't landed yet.
S03_SLIDE, S03_SCOOP = 8, 27      # bGqrs S03: the knees hit the grass and slide f8; the scoop splash shows from f27
S03_SHADOW = 44            # bGqrs S03: the bird's shadow sweeps over him from ~f44 (its strike is S04)
S04_SWIPE, S04_UP = 11, 16        # helper 1 S04: the talons cross his arm f11-12; the bird climbs away from f16
S05_DROP, S05_FACE = 31, 49       # helper 4 S05: the drop leaves the claw tip f31; the cut up to his terror face f49
S09_COCK, S09_SNAP, S09_RING = 14, 33, 36   # helper 10 S09: the cut to the wind-up f14; impact frames f33-35 (white,
                                            # black, red); the shockwave ring from f36
S10_CRASH = 0              # helper 10 S10: the bird is already upside down in the thorns on the cut
S11_DROP, S11_POOF = 18, 43       # helper 5 S11: it drops out of the bush f18 (lands f19-20); the puffball f43-44
S11_HUFF, S11_STOMP = 70, 74      # it glares, huffs and turns f70-72, then stomps off to the right f74-104
S12_RAISE = 14             # helper 5 S12: it turns in his palm f7, the claw comes up f14-17
S13_TAP = 15               # helper 5 S13: the claw touches his nose f15
S17_STEPS, S17_STOP = 0, 45       # XprL S17: Wren marches in from the cut and stops stern in front of Kai ~f45
S14_DRAW, S14_BURST = 24, 48      # helper 9 S14: the mark draws on and flickers from "wrist" ~f24; the burst f48 ("glow")
S15_CUT = 30               # helper 9 S15: the wrist mark's match cut to the sky crack, one glow frame f30, the sky f31-79
S19_CUT, S19_DRY = 48, 89         # helper 9 S19: the crane rises over the lake f0-47, cuts to the claw f48; drops leave
S19_DROPS = 8                      # the tip every 8 frames (meadow.drips every=8); sparkle + eyes go big on "dry" f89
S20_SPLIT = 0              # S20top/S20bot: both halves open on the cut, so the split whoosh sits on f0
S20_RAISE = 82                     # S20 bottom (B, 2 Nov re-voice): Kai raises his wrist on "show" ~f82 (placeholder)
S20_FLARE = 94                     # the mark flares on "glowing mark" f94-107 (coordinator)
S20_CLANK = 105                    # Wren steps back, startled, her bell clanks ~f105 (coordinator)


# ---------------------------------------------------------------- Episode 2 effects (original, seeded)

def talon_swipe(seed=0):
    """Talons raking past: a fast air swish with three scratchy rakes on top."""
    r = _rng("talon", seed)
    n = _n(0.35)
    p = np.linspace(0, 1, n)
    noise = r.uniform(-1, 1, n)
    swish = sum(_bp(noise, lo, lo * 2) * np.exp(-((p - c) / 0.12) ** 2) for lo, c in ((700, 0.3), (1400, 0.45)))
    out = swish * 0.8
    for k in range(3):
        m = _n(0.05)
        _place(out, _bp(r.uniform(-1, 1, m), 2500, 8000) * np.exp(-_t(m) / 0.012) * 0.7, 0.1 + 0.035 * k)
    return out


def cloth_tear(dur=0.28, seed=0):
    """A sleeve tearing: a quick run of tiny fibre snaps that bunch together, over a papery rip."""
    r = _rng("tear", seed)
    n = _n(dur)
    out = _bp(r.uniform(-1, 1, n), 1200, 6000) * np.sin(np.pi * np.linspace(0, 1, n)) * 0.3
    at = 0.0
    while at < dur * 0.9:
        m = _n(0.004)
        _place(out, r.uniform(-1, 1, m) * np.exp(-_t(m) / 0.0008) * r.uniform(0.4, 1.0), at)
        at += r.exponential(0.006 + 0.01 * (1 - at / dur))
    return _hp(out, 600)


def windup_hush(dur=1.0, seed=0):
    """The breath before the snap: an airy, steady hush that thins to nothing (one band, no pitch rise)."""
    r = _rng("hush", seed)
    n = _n(dur)
    p = np.linspace(0, 1, n)
    air = _bp(r.uniform(-1, 1, n), 900, 4000)
    return air * np.minimum(1, p / 0.25) * (1 - p) ** 0.6


def thorn_crash(seed=0):
    """Landing in a thorn bush: a soft thump, then a cascade of twig snaps and a leafy rustle settling."""
    r = _rng("thorn", seed)
    n = _n(1.1)
    t = _t(n)
    out = np.sin(2 * np.pi * (90 + 60 * np.exp(-t / 0.03)) * t) * np.exp(-t / 0.08) * 0.8
    out += _bp(r.uniform(-1, 1, n), 1500, 7000) * np.exp(-t / 0.35) * 0.35        # leaves
    for _ in range(26):
        at = r.exponential(0.12)
        m = _n(0.012)
        f = r.uniform(1800, 4500)
        twig = (np.sin(2 * np.pi * f * _t(m)) + r.uniform(-1, 1, m)) * np.exp(-_t(m) / 0.0025)
        _place(out, twig * r.uniform(0.3, 1.0) * np.exp(-at / 0.5), at)
    return out


def dazed_tweets(dur=2.0, seed=0):
    """Dazed little-bird tweets going round with the stars: chirps on a slow wobble, under the star twinkles."""
    out = np.zeros(_n(dur + 0.5))
    at, k = 0.0, 0
    while at < dur:
        _place(out, sfx.cute_chirp(2.2 + 0.25 * np.sin(k * 1.7), 40 + k) * 0.5 * (1 - 0.4 * at / dur), at)
        at += 0.32
        k += 1
    stars = v3.dazed(dur, seed + 3)[: len(out)]
    out[: len(stars)] += stars * 0.6
    return out


def poomf(seed=0):
    """A bird fluffing itself into a ball: a soft low puff with a feather flutter."""
    r = _rng("poomf", seed)
    n = _n(0.6)
    t = _t(n)
    puff = _lp(r.uniform(-1, 1, n), 700) * np.minimum(1, t / 0.015) * np.exp(-t / 0.12)
    thump = np.sin(2 * np.pi * (140 * np.exp(-t / 0.08) + 60) * t) * np.exp(-t / 0.1) * 0.6
    return puff + thump + np.pad(base.flutter(0.4, seed), (0, n))[:n] * 0.4


def nose_tink(seed=0):
    """The claw tapping his nose: a tiny bright glassy tink with a soft click."""
    n = _n(0.6)
    click = _hp(_rng("tink", seed).uniform(-1, 1, n), 3000) * np.exp(-_t(n) / 0.002) * 0.4
    return sfx._bell(_midi(100), 0.6, 0.25) + sfx._bell(_midi(107), 0.6, 0.15) * 0.4 + click


def glow_chime(seed=0):
    """The wrist mark lighting up: a soft rising arpeggio of bells (in plucked steps) over a shimmer."""
    out = np.zeros(_n(2.2))
    for k, m in enumerate((79, 83, 86, 91)):
        _place(out, sfx._bell(_midi(m), 1.6, 0.8) * (0.8 - 0.1 * k), 0.09 * k)
    r = _rng("glow", seed)
    shimmer = _bp(r.uniform(-1, 1, _n(1.6)), 5000, 11000) * np.sin(np.pi * np.linspace(0, 1, _n(1.6))) * 0.08
    _place(out, shimmer, 0.05)
    return _verb(out, 0.3)


def hand_bell(midi=86, seed=0):
    """One shake of a small brass hand bell: three quick strikes of the clapper, ringing on."""
    out = np.zeros(_n(1.6))
    for k in range(3):
        _place(out, sfx._bell(_midi(midi) * (1 + 0.002 * k), 1.2, 0.5) * (1.0, 0.7, 0.55)[k], 0.09 * k)
    return out


def bell_peal(dur=2.4, seed=0):
    """The village bells from over the hill: hand bells at five pitches rung unevenly, distant and roomy."""
    r = _rng("peal", seed)
    out = np.zeros(_n(dur + 1.6))
    at = 0.0
    while at < dur:
        _place(out, hand_bell(int(r.choice((81, 84, 86, 88, 91))), seed) * r.uniform(0.4, 1.0), at)
        at += r.uniform(0.12, 0.3)
    return _verb(_lp(out, 6000), 0.45, 1.3)


def footstep(seed=0, weight=1.0):
    """One step on grass: a soft heel thud and a crunch of blades."""
    r = _rng("step", seed)
    n = _n(0.18)
    t = _t(n)
    thud = _lp(r.uniform(-1, 1, n), 300) * np.exp(-t / 0.03) * weight
    crunch = _bp(r.uniform(-1, 1, n), 1500, 6000) * np.exp(-t / 0.05) * 0.35
    return thud + crunch


def cloth_swish(dur=0.35, seed=0):
    """A body turning or hands at a collar: a soft rise and fall of cloth rustle."""
    r = _rng("swish", seed)
    n = _n(dur)
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    grain = 0.7 + 0.3 * np.abs(_lp(r.uniform(-1, 1, n), 30)) * 4
    return _bp(r.uniform(-1, 1, n), 700, 5000) * env * np.minimum(grain, 1.3) * 0.5


def eyes_wide(seed=0):
    """Kai's eyes going wide: a tight, slightly sour double ping with a quick wobble."""
    n = _n(0.7)
    t = _t(n)
    wob = 1 + 0.012 * np.sin(2 * np.pi * 9 * t)
    ping = np.sin(2 * np.pi * 1568 * wob * t) + 0.7 * np.sin(2 * np.pi * 1661 * wob * t)
    return ping * np.minimum(1, t / 0.003) * np.exp(-t / 0.18) * 0.5


def mark_flicker(dur, seed=0):
    """The wrist mark drawing on: faint warm glints and ticks that come faster as it brightens."""
    r = _rng("flicker", seed)
    out = np.zeros(_n(dur + 0.4))
    at = 0.0
    while at < dur:
        x = at / dur
        f = r.uniform(2200, 3600) * (1 + 0.4 * x)
        m = _n(0.12)
        tt = _t(m)
        _place(out, np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.03) * (0.3 + 0.7 * x), at)
        at += r.uniform(0.06, 0.14) * (1.2 - 0.6 * x)
    return _verb(out, 0.3)


def rift_hum(dur, seed=0):
    """The crack in the sky: a low uneasy hum with a faint dry crackle at its edges."""
    r = _rng("rift", seed)
    n = _n(dur)
    t = _t(n)
    hum = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.7 * t + 0.3 * np.sin(2 * np.pi * 0.7 * t))) * 0.4
    out = hum * (0.8 + 0.2 * np.sin(2 * np.pi * 3.1 * t))
    at = 0.0
    while at < dur - 0.02:
        m = _n(0.006)
        _place(out, _hp(r.uniform(-1, 1, m), 3000) * np.exp(-_t(m) / 0.0015) * r.uniform(0.1, 0.35), at)
        at += r.exponential(0.07)
    return out * np.minimum(1, t / 0.15) * np.minimum(1, (dur - t) / 0.4)


def bell_clank(seed=0):
    """Wren's hand bell knocked as she starts back: one dull, choked strike and the clapper rattling."""
    r = _rng("clank", seed)
    n = _n(0.9)
    t = _t(n)
    out = np.zeros(n)
    for f, a, tau in ((1175, 1.0, 0.16), (1690, 0.6, 0.09), (2830, 0.45, 0.05), (3910, 0.3, 0.03)):
        out += np.sin(2 * np.pi * f * t) * a * np.exp(-t / tau)
    out *= np.minimum(1, t / 0.002)
    for k in range(4):                                                   # the clapper rattling, dying away
        m = _n(0.02)
        _place(out, _bp(r.uniform(-1, 1, m), 2000, 7000) * np.exp(-_t(m) / 0.004) * (0.5 - 0.1 * k),
               0.05 + 0.045 * k + r.uniform(0, 0.01))
    return _verb(out, 0.2)


def lake(dur, seed=0):
    """A big still lake: small waves lapping the shore, a deep soft water hush, a breeze."""
    r = _rng("lake", seed)
    n = _n(dur)
    hush = _lp(r.uniform(-1, 1, n), 500) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.15 * _t(n) + seed))
    out = hush * 0.6 + base.meadow_wind(dur, 200 + seed)[:n] * 0.5
    at = r.uniform(0, 0.4)
    k = 0
    while at < dur:
        _place(out, base.lap(30 + k + 10 * seed) * r.uniform(0.5, 1.0), at)
        at += r.uniform(0.6, 1.3)
        k += 1
    return out


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

    # the meadow under everything up to the lake (frame 0 has sound)
    amb(lambda d, s: base.meadow_wind(d, s), 0.0, c.t("S19"), -27, 0.02, 0.6)

    # --- S01-S04: the run, the dive, the slide, the talons (the action bed from frame 0)
    music_at(base.bed("danger", c.t("S05") + 0.6, 5), 0.0, c.t("S05") + 0.3, -17, 0.02, 0.6)
    for k in range(7):                                               # Kai sprinting
        hit(footstep(k, 1.2), 0.08 + 0.3 * k, -24, -0.2)
    gap = c.word("l1", "it", "end")                                  # S01: the bird dives head-on (between sentences)
    hit(v3.shadow_whoosh(0.45, 1), gap + 0.02, -18, 0.3)
    dive_from = c.word("l2", "first", "end") + 0.03                # after the line: under it "dived" read as "died"
    hit(v3.shadow_whoosh(0.6, 2), dive_from, -12, 0.2)              # peaks across the cut into S03
    hit(_lp(np.random.default_rng(5).uniform(-1, 1, _n(0.5)), 900) * np.exp(-_t(_n(0.5)) / 0.12),
        c.f("S03", S03_SLIDE), -18, -0.1)                            # the knee slide on grass
    hit(v3.splash(3), c.f("S03", S03_SCOOP), -14, 0.0)
    hit(v3.shadow_whoosh(0.7, 3), c.f("S03", S03_SHADOW), -18, -0.3)  # the shadow passes over (into the talons)
    swipe = c.f("S04", S04_SWIPE)
    hit(talon_swipe(), swipe, -9, 0.25)
    hit(cloth_tear(), swipe + 0.07, -12, 0.15)
    hit(v3.wing_mantle(2, 4), c.f("S04", S04_UP), -16, 0.4)

    # --- S05-S08: wet hands, the fact, the turn, the aim (a tense low bed); the music drops a tick before S09
    snap_shot = c.t("S09")
    music_at(base.tense_tone(snap_shot - c.t("S05") + 0.3, 2), c.t("S05"), snap_shot - 0.1, -19, 0.6, 0.06)
    hit(base.drip(3), c.f("S05", S05_DROP), -16, 0.1)
    hit(eyes_wide(), c.f("S05", S05_FACE), -21, 0.0)                    # his eyes go wide (before "In my")
    hit(v3.water_jet(0.5, 4), c.word("l6", "Straight"), -20, 0.3)   # the 2D jet straight ahead
    hit(v3.startle(4), c.word("l7", "around", "end") + 0.05, -24, 0.0)   # the shrimp lets him, confused

    # --- S09: THE SNAP. No music; the claw cocks, the hush, SNAP + shockwave, the bird blasted back
    cock, snap_t = c.f("S09", S09_COCK), c.f("S09", S09_SNAP)
    hit(base.glass_tap(2), cock, -22, 0.0)
    hit(windup_hush(snap_t - cock), cock, -22, 0.0)
    hit(sfx.snap(4), snap_t, 0)
    hit(sfx.shockwave(2), c.f("S09", S09_RING), -1)
    hit(sfx.whoosh(3), snap_t + 0.08, -10, 0.3)
    hit(base.ring_out(2.2), snap_t + 0.25, -18)
    hit(base.flutter(0.7, 5), snap_t + 0.3, -18, 0.5)

    # --- S10-S11: the thorn bush, the dazed tweets, the puffball and the offended exit (a light comic bed)
    music_at(base.bed("lab", c.t("S12") - c.t("S10") + 0.8, 6), c.t("S10") + 0.4, c.t("S12"), -21, 0.5, 0.5)
    crash = c.f("S10", S10_CRASH)
    hit(thorn_crash(), crash, -9, 0.2)
    hit(dazed_tweets(c.end("S10") - crash - 0.4), crash + 0.35, -18, 0.25)
    hit(footstep(30, 0.6), c.f("S11", S11_DROP + 1), -20, 0.15)      # it drops out of the bush onto the grass
    hit(poomf(), c.f("S11", S11_POOF), -10, 0.15)
    hit(base.huff(1), c.f("S11", S11_HUFF), -20, 0.2)
    stomp0 = c.f("S11", S11_STOMP)
    for k in range(5):
        hit(base.stomp(k), stomp0 + 0.25 * k, -22, 0.2 + 0.12 * k)

    # --- S12-S13: the shrimp looks at him, the claw comes up: a held tense second, then the nose tap
    music_at(base.tense_tone(c.t("S14") - c.t("S12") + 0.3, 3), c.t("S12") + 0.2, c.f("S13", S13_TAP), -22,
             0.6, 0.08)
    hit(v3.aim(0.7, 6), c.f("S12", S12_RAISE), -22, 0.0)
    hit(nose_tink(), c.f("S13", S13_TAP), -12, 0.0)

    # --- S14-S15: the wrist glows (a wonder pad), the match cut to the crack in the sky
    music_at(base.soft_pad(c.t("S16") - c.t("S14") + 0.6, (62, 69, 74, 78), 0.1, 3), c.t("S14"), c.t("S16") + 0.2,
             -18, 0.6, 0.4)
    hit(mark_flicker(c.f("S14", S14_BURST) - c.f("S14", S14_DRAW), 1), c.f("S14", S14_DRAW), -25, -0.1)
    hit(glow_chime(), c.f("S14", S14_BURST) - 0.02, -12, -0.1)
    # S15: the match cut from the wrist mark to the sky crack: a glint on the glow frame, the sting on the cut,
    # then the rift's hum under the sky
    hit(glow_chime(2), c.f("S15", S15_CUT) - 0.03, -19, 0.0)
    hit(base.eerie_sting(2), c.f("S15", S15_CUT), -19, 0.0)
    rift = c.end("S15") - c.f("S15", S15_CUT + 1)
    hit(rift_hum(rift + 0.2, 1), c.f("S15", S15_CUT + 1), -24, 0.0)

    # --- S16-S18: the bells over the hill, Wren's march, her stern line (a low tense bed under Wren)
    hit(bell_peal(2.6, 1), c.word("l16", "bells") - 0.05, -16, 0.2)
    steps0, stop = c.f("S17", S17_STEPS), c.f("S17", S17_STOP)
    k, at = 0, steps0 + 0.1
    while at < stop:
        hit(footstep(10 + k, 0.9), at, -21, -0.15 + 0.1 * (k % 2))
        at += 0.36
        k += 1
    hit(hand_bell(86, 2), stop + 0.05, -16, -0.1)
    music_at(base.tense_tone(c.t("S19") - c.t("S17") + 0.3, 4), c.t("S17"), c.t("S19") + 0.2, -21, 0.5, 0.4)

    # --- S19: the lake: water, depth and a breeze; after the cut the claw drips, a sparkle on "dry"
    amb(lambda d, s: lake(d, s), c.t("S19"), c.t("S20") + 0.4, -20, 0.5, 0.4)
    music_at(base.soft_pad(c.t("S20") - c.t("S19") + 0.6, (50, 57, 62, 65), 0.08, 5), c.t("S19"), c.t("S20"),
             -19, 0.6, 0.3)
    f, k = S19_CUT + 6, 0                     # small plinks on the drop schedule, under the voice
    while c.f("S19", f) < c.end("S19") - 0.1:
        if abs(f - S19_DRY) > 4:
            hit(base.drip(k), c.f("S19", f), -29 + 2 * (k % 2), 0.1)
        f, k = f + S19_DROPS, k + 1
    hit(nose_tink(3), c.f("S19", S19_DRY), -21, 0.1)                    # the sparkle; its eyes go big
    hit(base.drip(4), c.word("l19", "dry", "end") + 0.05, -16, 0.1)

    # --- S20: the split opens; the A and B stingers on the letters; "Comment" blip; cut on the picture
    words = v3.timing_words(timing, "l20")
    opt_a = c.word("l20", "Option")
    a_t = next(w["start"] for w in words if w["w"].strip(".,:?!").upper() == "A")
    b_t = [w["start"] for w in words if w["w"].strip(".,:?!").upper() == "B"][0]
    comment = next(w["start"] for w in words if w["w"].lower().startswith("comment"))
    hit(sfx.whoosh(), c.f("S20", S20_SPLIT) + 0.02, -10)
    # the bottom half (B): Kai raises his wrist, the mark flares on "glowing mark", Wren starts back, bell clanking
    hit(cloth_swish(0.3, 2), c.f("S20", S20_RAISE), -22, -0.3)
    flare = c.f("S20", S20_FLARE)
    hit(mark_flicker(flare - c.f("S20", S20_RAISE) - 0.05, 2), c.f("S20", S20_RAISE) + 0.05, -26, -0.2)
    hit(glow_chime(1), flare - 0.02, -14, -0.2)
    hit(bell_clank(), c.f("S20", S20_CLANK), -19, 0.3)
    hit(footstep(31, 0.8), c.f("S20", S20_CLANK) + 0.06, -22, 0.35)
    hit(v3.option_sting("A"), a_t, -12, -0.15)
    hit(v3.option_sting("B"), b_t, -12, 0.15)
    hit(sfx.ui_select(5), comment, -20)
    music_at(base.sting(total - opt_a), opt_a, total, -15, 0.25, 0.01)
    # l2 ("The bird struck first."): everything under the line another 6 dB down (the duck comes on top of it)
    l2 = c.line["l2"]
    for tr in (music, *fx, *ambience):
        i0, i1, r = int((l2["start"] - 0.08) * SR), int((l2["end"] + 0.05) * SR), _n(0.05)
        g = np.ones(len(tr))
        g[i0:i1] = base._db(-6)
        g[i0 - r:i0] = np.linspace(1, base._db(-6), r)
        g[i1:i1 + r] = np.linspace(base._db(-6), 1, r)
        tr *= g
    return music, fx, ambience


base.build = build

if __name__ == "__main__":
    base.main()
    if "--check" in sys.argv:
        base.check()
    if "--roughcut" in sys.argv:
        base.roughcut()
