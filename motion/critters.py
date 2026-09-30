"""Original animal characters and props for fact episodes: a cartoon carpenter ant (with a 'zombie' state),
an emu with a running cycle, fungus spores, and a period machine gun on a tripod.

All drawn with the same hand-drawn helpers as the human cast; (x, y) is where the feet touch the ground.
"""
import math

from .engine import INK, WHITE, at, blob, dot, hexc, line, rrect_pts, shape, sharp_shape

ANT = hexc("#5a3326")
ANT_D = hexc("#3a1f18")
FUNGUS = hexc("#e9e1c8")
FUNGUS_D = hexc("#b7a67a")
EMU = hexc("#7a6552")
EMU_D = hexc("#54443a")
EMU_FACE = hexc("#6f8fb0")


def ant(cr, x, y, t, s=1.0, facing=1, walk=None, zombie=0.0, grip=False, eye="normal", seed=0, tilt=0.0):
    """Side-view ant, ~220 units long at s=1. zombie 0..1 adds fungus fuzz and a spiral eye.
    grip=True points the head up with jaws clamped (the 'death grip')."""
    body = ANT if zombie < 0.5 else hexc("#6a4a3e")
    with at(cr, x, y, s, rot=tilt, flip=facing < 0):
        ph = walk * 2 * math.pi if walk is not None else 0.0
        bob = abs(math.sin(ph)) * 3 if walk is not None else math.sin(t * 3 + seed) * 1.2
        if zombie > 0.3 and walk is None and not grip:
            cr.translate(math.sin(t * 40) * 2.5 * zombie, 0)   # convulsions
        # legs (three pairs, alternating tripod gait)
        for i, lx in enumerate((-18, 8, 32)):
            for side in (0, 1):
                off = ph + (math.pi if (i + side) % 2 else 0)
                sw = math.sin(off) * 14 if walk is not None else 0
                lift = max(0.0, math.sin(off)) * 8 if walk is not None else 0
                knee = (lx + 10 + sw * 0.5, -58 - bob)
                foot = (lx + 22 + sw, -4 - lift)
                col = ANT_D if side == 0 else ANT
                line(cr, [(lx, -40 - bob), knee, foot], 6, col, seed=seed + i * 2 + side, amp=0.4)
        cr.translate(0, -bob)
        # abdomen, waist, thorax
        blob(cr, -70, -52, 50, 36, body, seed=seed + 10, amp=0.8, lw=4)
        for k in range(3):
            line(cr, [(-88 + k * 16, -84), (-94 + k * 16, -20)], 2.5, ANT_D, seed=seed + 11 + k, amp=0.5)
        blob(cr, -20, -50, 12, 10, body, seed=seed + 14, amp=0.5, lw=3.5)
        blob(cr, 12, -52, 30, 20, body, seed=seed + 15, amp=0.7, lw=4)
        # head (tilted up in the death grip)
        with at(cr, 50, -60, 1.0, rot=-0.9 if grip else 0.0):
            blob(cr, 22, -6, 32, 28, body, seed=seed + 16, amp=0.7, lw=4)
            # antennae
            for k, a in enumerate((-0.4, -0.15)):
                tip = (22 + 60 * math.cos(a - 1.2) + math.sin(t * 4 + k) * 3, -30 + 60 * math.sin(a - 1.2))
                line(cr, [(24, -30), (30 + k * 6, -58), tip], 4, ANT_D, seed=seed + 17 + k, amp=0.4)
            # jaws
            open_ = 0 if grip else 8 + 4 * math.sin(t * 5)
            line(cr, [(46, 4), (60, 6 - open_ * 0.3), (64, 14)], 5, ANT_D, seed=seed + 19, amp=0.3)
            line(cr, [(46, 12), (60, 16 + open_ * 0.3), (62, 22)], 5, ANT_D, seed=seed + 20, amp=0.3)
            # the eye
            blob(cr, 28, -10, 13, 13, WHITE, seed=seed + 21, amp=0.4, lw=3)
            if zombie > 0.5 or eye == "spiral":
                cr.set_source_rgba(*hexc("#8a63d2"))
                cr.set_line_width(2.5)
                for k in range(22):
                    a = k * 0.6 + t * 6
                    r = 1 + k * 0.45
                    px, py = 28 + r * math.cos(a), -10 + r * math.sin(a)
                    cr.line_to(px, py) if k else cr.move_to(px, py)
                cr.stroke()
            elif eye == "wide":
                dot(cr, 31, -10, 5, INK)
            elif eye == "happy":
                line(cr, [(21, -8), (28, -15), (35, -8)], 3, INK, seed=seed + 22, amp=0.2)
            else:
                dot(cr, 32, -9, 6, INK)
                dot(cr, 34, -12, 2, WHITE)
        # fungus fuzz
        if zombie > 0:
            for i, (fx, fy, r) in enumerate([(-80, -80, 10), (-50, -86, 8), (-96, -50, 9), (8, -70, 8), (-60, -20, 7)]):
                if i / 5 < zombie:
                    blob(cr, fx, fy, r, r * 0.8, FUNGUS, seed=seed + 30 + i, amp=1.2, lw=2.5)


def stalk(cr, x, y, h, t, seed=0):
    """Fungal stalk growing up from (x, y), height h; spore capsule near the tip once tall."""
    if h <= 1:
        return
    sway = math.sin(t * 1.5) * h * 0.05
    pts = [(x, y), (x + 6 + sway * 0.3, y - h * 0.35), (x - 4 + sway * 0.7, y - h * 0.7), (x + sway, y - h)]
    line(cr, pts, 14, INK, seed=seed, amp=0.6)
    line(cr, pts, 8, FUNGUS_D, seed=seed, amp=0.6)
    if h > 60:
        blob(cr, pts[-1][0] + 2, pts[-1][1] + 14, 14, 18, hexc("#c98b5a"), seed=seed + 1, amp=0.8, lw=3)


def spores(cr, x, y, t, start, spread=260, n=34, seed=5):
    """Spores drifting down from (x, y) after `start`."""
    if t < start:
        return
    import random
    r = random.Random(seed)
    for i in range(n):
        k = ((t - start) * r.uniform(0.3, 0.6) + r.uniform(0, 1)) % 1
        px = x + r.uniform(-0.25, 0.25) * spread + (k * r.uniform(-1, 1)) * spread * 0.6
        py = y + k * r.uniform(300, 520)
        dot(cr, px, py, r.uniform(2.5, 5), hexc("#f3ead0", 1 - k * 0.6))


def emu(cr, x, y, t, s=1.0, facing=1, run=None, eye="normal", peck=0.0, seed=0):
    """Side-view emu, ~330 units tall at s=1. run = gait phase in cycles (None = standing)."""
    with at(cr, x, y, s, flip=facing < 0):
        ph = run * 2 * math.pi if run is not None else 0.0
        bob = abs(math.sin(ph)) * 10 if run is not None else math.sin(t * 2 + seed) * 2
        # legs
        for side, off in ((0, 0.0), (1, math.pi)):
            sw = math.sin(ph + off) * 40 if run is not None else (8 if side else -8)
            lift = max(0.0, math.sin(ph + off)) * 24 if run is not None else 0
            hip = (0 + side * 10, -140 - bob)
            knee = (hip[0] - 14 + sw * 0.4, -80 - lift * 0.5)
            foot = (hip[0] + sw, -6 - lift)
            col = hexc("#3b3431") if side == 0 else hexc("#4a423e")
            line(cr, [hip, knee, foot], 9, col, seed=seed + side, amp=0.3)
            for d in (-12, 0, 12):   # toes
                line(cr, [foot, (foot[0] + 16 + d * 0.4, foot[1] + 2 + abs(d) * 0.2)], 4, col, seed=seed + 5 + d,
                     amp=0.2)
        cr.translate(0, -bob)
        # shaggy body
        blob(cr, -10, -190, 92, 66, EMU, seed=seed + 10, amp=2.2, lw=4, n=30)
        for i in range(9):
            fx = -80 + i * 18
            line(cr, [(fx, -170 + (i % 3) * 8), (fx - 10, -140 + (i % 2) * 10)], 3, EMU_D, seed=seed + 11 + i, amp=0.8)
        # neck + head
        lean = 0.45 if run is not None else 0.0
        hx, hy = 70 + lean * 60, -300 + lean * 50 + peck * 70
        line(cr, [(50, -220), (62 + lean * 30, -260 + lean * 20), (hx - 6, hy + 16)], 26, INK, seed=seed + 20, amp=0.4)
        line(cr, [(50, -220), (62 + lean * 30, -260 + lean * 20), (hx - 6, hy + 16)], 18, EMU_FACE, seed=seed + 20,
             amp=0.4)
        blob(cr, hx, hy, 22, 18, EMU_D, seed=seed + 21, amp=0.8, lw=3.5)
        shape(cr, [(hx + 16, hy - 4), (hx + 46, hy + 2), (hx + 16, hy + 8)], hexc("#3b3431"), seed=seed + 22, amp=0.3,
              lw=3)   # beak
        blob(cr, hx + 4, hy - 4, 8, 8, hexc("#f2b632"), seed=seed + 23, amp=0.3, lw=2.5)
        if eye == "angry":
            dot(cr, hx + 6, hy - 3, 4, INK)
            line(cr, [(hx - 6, hy - 16), (hx + 14, hy - 10)], 3.5, INK, seed=seed + 24, amp=0.2)
        elif eye == "smug":
            line(cr, [(hx - 2, hy - 4), (hx + 10, hy - 4)], 3.5, INK, seed=seed + 24, amp=0.2)
        else:
            dot(cr, hx + 6, hy - 4, 4, INK)


def lewis_gun(cr, x, y, s=1.0, facing=1, recoil=0.0, seed=0):
    """Tripod machine gun with the characteristic round drum magazine."""
    with at(cr, x - recoil * 6, y, s, flip=facing < 0):
        for dx in (-40, 0, 40):   # tripod
            line(cr, [(0, -70), (dx, 0)], 6, INK, seed=seed + dx, amp=0.3)
        shape(cr, rrect_pts(-60, -96, 150, 26, 10, 18), hexc("#4a4f55"), seed=seed + 1, amp=0.6, lw=3.5)
        shape(cr, rrect_pts(90, -90, 70, 14, 5, 14), hexc("#3a3f45"), seed=seed + 2, amp=0.4, lw=3)   # barrel
        blob(cr, 10, -110, 34, 10, hexc("#6b7178"), seed=seed + 3, amp=0.4, lw=3.5)   # drum magazine
        sharp_shape(cr, [(-60, -92), (-96, -80), (-96, -64), (-60, -74)], hexc("#8e4a1e"), seed=seed + 4, amp=0.4,
                    lw=3)   # stock


def goat(cr, x, y, t, s=1.0, facing=1, bleat=False, seed=0):
    """Cartoon goat standing at (x, y), ~200 units tall at s=1."""
    with at(cr, x, y, s, flip=facing < 0):
        for lx in (-50, -24, 28, 52):   # legs
            line(cr, [(lx, -60), (lx + 2, -6)], 9, INK, seed=seed + lx, amp=0.3)
            line(cr, [(lx, -60), (lx + 2, -6)], 5, hexc("#f4efe1"), seed=seed + lx, amp=0.3)
        blob(cr, 0, -90, 78, 42, hexc("#f4efe1"), seed=seed + 1, amp=1.6, lw=4)   # body
        line(cr, [(-74, -100), (-92, -118)], 5, INK, seed=seed + 2, amp=0.3)     # tail
        with at(cr, 70, -130, 1.0, rot=-0.25 + (0.12 * math.sin(t * 14) if bleat else 0)):
            blob(cr, 0, 0, 30, 24, hexc("#f4efe1"), seed=seed + 3, amp=0.8, lw=4)   # head
            line(cr, [(-10, -18), (-26, -48), (-14, -58)], 6, hexc("#8e7a5a"), seed=seed + 4, amp=0.3)   # horns
            line(cr, [(6, -20), (2, -52), (16, -60)], 6, hexc("#8e7a5a"), seed=seed + 5, amp=0.3)
            shape(cr, [(-26, -6), (-50, -2), (-30, 8)], hexc("#e3dccb"), seed=seed + 6, amp=0.3, lw=3)   # ear
            dot(cr, 10, -4, 4.5, INK)
            line(cr, [(18, 18), (14, 38), (22, 36)], 4, hexc("#d9d0bb"), seed=seed + 7, amp=0.4)   # beard
            if bleat:
                blob(cr, 26, 10, 7, 8 + 3 * abs(math.sin(t * 14)), hexc("#7a2b35"), seed=seed + 8, amp=0.4, lw=2.5)


def car(cr, x, y, t, s=1.0, facing=1, color=None, seed=0):
    """Shiny cartoon sports car, ground at (x, y), ~380 units long at s=1."""
    body = color or hexc("#e0483f")
    with at(cr, x, y, s, flip=facing < 0):
        shape(cr, [(-190, -40), (-180, -90), (-80, -100), (-30, -150), (80, -150), (130, -100), (190, -90),
                   (196, -40)], body, seed=seed, amp=0.8, lw=4.5)
        shape(cr, [(-20, -140), (70, -140), (110, -100), (-60, -100)], hexc("#bfe6ef"), seed=seed + 1, amp=0.5, lw=3.5)
        line(cr, [(30, -140), (30, -100)], 4, INK, seed=seed + 2, amp=0.2)
        line(cr, [(0, -132), (-20, -108)], 5, WHITE, seed=seed + 3, amp=0.2)
        for wx in (-110, 120):
            blob(cr, wx, -36, 36, 36, hexc("#2b2530"), seed=seed + wx, amp=0.5, lw=4)
            blob(cr, wx, -36, 16, 16, hexc("#c7c2cc"), seed=seed + wx + 1, amp=0.3, lw=3)
        blob(cr, 180, -74, 10, 7, hexc("#ffe28a"), seed=seed + 4, amp=0.3, lw=2.5)
        sparkle_n = int(t * 3) % 3
        for k, (sx, sy) in enumerate([(-120, -170), (60, -190), (170, -140)]):
            if k == sparkle_n:
                line(cr, [(sx - 10, sy), (sx + 10, sy)], 4, hexc("#ffd23f"), seed=seed + 20 + k, amp=0.1)
                line(cr, [(sx, sy - 10), (sx, sy + 10)], 4, hexc("#ffd23f"), seed=seed + 30 + k, amp=0.1)
