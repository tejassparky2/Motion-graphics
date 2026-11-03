"""Demo (3 Nov 2026, owner: "Create 2.5d or 2d mascot yourself which you can animate yourself"): the opening of Vex
episode 1 played by the fully code-drawn Vex (motion/vex2d.py) in the reference's style: one close bright floor shot,
no music, no overlays, plain comic captions, Vex's lines as red handwriting, lip sync from the loudness of his voice."""
import math

import numpy as np

from motion import voice
from motion.engine import ease_out, lerp, seg
from motion.vex2d import vex
from videos import vex_kit as K

NARRATOR = dict(turbo=True)
TAIL = 0.6
MUSIC = "none"
voice.SPEAKERS.update({"vex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+5")})

SCRIPT = [
    dict(id="v1", scene="floor", text="Vex, try and bite this pufferfish."),
    dict(id="v2", scene="floor", text="Easy. I'm a vampire.", speaker="vex"),
    dict(id="v3", scene="floor", text="When a pufferfish gets scared, it gulps water and blows up into a spiky ball."),
    dict(id="v4", scene="floor", text="Ow! It poked me!", speaker="vex"),
]

VX, VY, S = 235, 740, 0.33
BX, BY, BR = 510, 742, 92
_env = {}


def talk(tl, t, who="vex"):
    """Mouth opening 0..1 from the loudness of `who`'s voice right now (30 ms windows), 0 when silent."""
    if not _env:
        for b in tl.beats:
            if b.speaker != who or b.audio is None:
                continue
            a = np.abs(np.asarray(b.audio, dtype=np.float32))
            win = int(44100 * 0.03)
            rms = np.sqrt(np.convolve(a * a, np.ones(win) / win, mode="same"))
            _env[b.id] = (b.start, rms / max(1e-6, np.percentile(rms, 95)))
    for bid, (st, env) in _env.items():
        i = int((t - st) * 44100)
        if 0 <= i < len(env):
            return float(min(1.0, env[i] * 1.1))
    return None


def draw(cr, t, tl):
    A = tl.at
    K.photo(cr, t, "close_living", 0.0, push=0.03, dur=12, focus=(380, 700))
    g0, g1 = A("v3", "gulps"), A("v3", "ball", end=True)
    u = max(0.0, min(1.0, (t - g0) / (g1 - g0))) * 3
    k = int(u)
    puff = min(1.0, (k + ease_out(u - k)) / 3)
    poke = A("v4")
    shake = 5 * math.sin(t * 60) if poke <= t < poke + 0.3 else 0
    K.floor_shadow(cr, BX, BY + 2, BR * 0.95)
    K.bowl_back(cr, BX, BY, BR)
    K.pufferfish(cr, t, BX + shake, BY - BR * 1.02, 0.5 + 0.08 * puff, puff=puff, facing=-1,
                 eyes="angry" if puff > 0.5 else "open")
    K.bowl_front(cr, BX, BY, BR)

    blink = K.auto_blink(t)
    tk = talk(tl, t)
    v2, lunge0 = A("v2"), A("v3", "scared")
    if t < v2:                                        # listening, then perks up at "bite"
        perk = seg(t, A("v1", "bite"), A("v1", "bite") + 0.3)
        vex(cr, t, VX, VY, S, turn=0.35 * perk, look=(0.7 * perk, 0), eyes="sparkle" if perk > 0.5 else "open",
            brows="angry", mouth="smirk", blink=blink, squash=0.2 * math.sin(perk * math.pi))
    elif t < lunge0:                                  # "Easy." hands on hips ... "I'm a vampire" cape spread
        big = seg(t, A("v2", "vampire") - 0.15, A("v2", "vampire") + 0.15)
        arms = ("out", "out") if big > 0.5 else ("hips", "hips")
        vex(cr, t, VX, VY, S, turn=-0.15, eyes="angry", brows="angry", mouth="smirk", talk=tk, arms=arms,
            cape=big, blink=blink, squash=0.25 * math.sin(seg(t, v2, v2 + 0.3) * math.pi), tilt=-0.06)
    elif t < poke:                                    # leaps at the bowl, mouth wide; then sees it puff up
        l = seg(t, lunge0, lunge0 + 0.4)
        x = lerp(VX, 395, ease_out(l))
        lift = 90 * math.sin(l * math.pi) if l < 1 else 0
        scared = t > A("v3", "blows")
        vex(cr, t, x, VY, S, turn=0.6, lean=0.22 * l, eyes="shocked" if scared else "angry",
            brows="up" if scared else "angry", mouth="o" if scared else "wide", arms=("reach", "reach"),
            legs="jump" if 0 < l < 1 else "stand", lift=lift, blink=0 if scared else blink, cape=0.6 * (l < 1))
    else:                                             # "Ow!": knocked back in a spin, lands sitting, dizzy
        v = seg(t, poke, poke + 0.5)
        x = lerp(395, 205, ease_out(v))
        land = t - (poke + 0.5)
        sq = 0.9 * math.exp(-9 * land) * math.cos(16 * land) if land > 0 else 0
        vex(cr, t, x, VY, S, rot=-2 * math.pi * ease_out(v), pivot="center",
            lift=130 * math.sin(v * math.pi) if v < 1 else 0, legs="sit" if v >= 1 else "jump",
            eyes="dizzy" if v >= 1 else "cry", mouth="wobble" if tk is None else None, talk=tk,
            arms=("up", "up") if v < 1 else ("out", "out"), squash=sq, cape=0.5, tears=v >= 1)
        K.dizzy(cr, t, x, VY - 1000 * S + 20, poke + 0.5, r=80)
    K.grain(cr)
    K.reply(cr, t, v2, A("v2", end=True) + 0.4, VX, VY - 1080 * S - 20, "easy. i'm a vampire", size=52,
            font="Comic Neue")
    K.reply(cr, t, poke, A("v4", end=True) + 0.5, 230, VY - 1080 * S - 20, "OW! it poked me!", size=54,
            font="Comic Neue")
    K.comic_captions(cr, t, tl, skip="vex", y=860, size=56, line_chars=20)
