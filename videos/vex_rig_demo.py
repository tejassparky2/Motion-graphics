"""Demo for the owner (3 Nov 2026, "You can't animate it??"): the first four lines of Vex episode 1 redone in the
reference's style with the cut-out puppet (videos/vex_rig.py): one close, bright floor shot, no overlays, plain comic
captions under the characters, Vex's lines as red handwriting with lip sync, no music. Same voice takes as episode 1."""
import math

from motion import voice
from motion.engine import ease_out, lerp, seg
from videos import vex_kit as K
from videos import vex_rig as R

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

VX, VY, VS = 245, 735, 0.24          # Vex's spot and size
BX, BY, BR = 505, 740, 92            # the fishbowl


def draw(cr, t, tl):
    A = tl.at
    K.photo(cr, t, "close_living", 0.0, push=0.03, dur=12, focus=(380, 700))
    # the fish puffs up in three gulps on the keeper's line, stays angry after
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

    mouth = R.talk_mouth(tl, "vex", t)
    lunge0 = A("v3", "scared")
    if t < A("v2"):                                   # listening; leans toward the fish on "pufferfish"
        lean = 22 * seg(t, A("v1", "pufferfish"), A("v1", "pufferfish") + 0.4)
        R.puppet(cr, t, VX, VY, VS, mouth="closed", lean=lean, arms=("rest", "rest"))
    elif t < lunge0:                                  # "Easy. I'm a vampire.": fist pump, cocky lean
        up = seg(t, A("v2"), A("v2") + 0.25)
        down = seg(t, A("v2", end=True) + 0.1, A("v2", end=True) + 0.4)
        arm = ("rest", "up", up * (1 - down))
        R.puppet(cr, t, VX, VY, VS, mouth=mouth, arms=(arm, "rest"), lean=-18 * up * (1 - down),
                 shake=4 if up >= 1 and down <= 0 else 0, squash=0.15 * math.sin(seg(t, A("v2"), A("v2") + 0.3) * math.pi))
    elif t < poke:                                    # lunges at the bowl, mouth wide, arms out
        l = seg(t, lunge0, lunge0 + 0.35)
        x = lerp(VX, 380, ease_out(l))
        R.puppet(cr, t, x, VY, VS, mouth="open", arms=(("rest", "front", l), ("rest", "out", l)),
                 rot=0.28 * ease_out(l), lean=30 * l)
    else:                                             # "Ow!": knocked back in a spin, lands on his bottom, dazed
        v = seg(t, poke, poke + 0.5)
        x = lerp(380, 215, ease_out(v))
        land = t - (poke + 0.5)
        sq = (0.9 * math.exp(-9 * land) * math.cos(16 * land) if land > 0 else 0) + (0.22 if v >= 1 else 0)
        R.puppet(cr, t, x, VY + 5, VS, mouth=mouth, arms=("up", "up"), rot=-2 * math.pi * ease_out(v), pivot="center",
                 lift=120 * math.sin(v * math.pi) if v < 1 else 0, squash=sq, shake=3)
        K.dizzy(cr, t, x, K.head_top(VY, VS) + 20, poke + 0.5)
    K.grain(cr)
    K.reply(cr, t, A("v2"), A("v2", end=True) + 0.4, VX, K.head_top(VY, VS) - 30, "easy. i'm a vampire",
            size=52, font="Comic Neue")
    K.reply(cr, t, poke, A("v4", end=True) + 0.5, 230, K.head_top(VY, VS) - 30, "OW! it poked me!", size=54,
            font="Comic Neue")
    K.comic_captions(cr, t, tl, skip="vex", y=860, size=56, line_chars=20)
