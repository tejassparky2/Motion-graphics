"""The news channel's own cast ("newsfolk"), drawn in a style of its own so it never looks like the Interestingly
Strange characters (motion/characters.py): bean-shaped bodies, big round heads, big oval eyes with a shine and
eyebrows, a nose, mitten hands, short legs. Every story character comes from FOLK below.

    folk(cr, "trucker", x, y, t, facing=1, arms=("wave", "down"), eyes="open", mouth="smile")

(x, y) is between the feet. Arms: down, hip, wave, cheer, point, hold, face, chin, thumb. Eyes: open, wide, happy,
sad, sly, closed. Mouth: smile, grin, o, flat, sad, talk (opens and closes)."""
import math

from .engine import INK, WHITE, at, blink, blob, dot, hexc, line, rrect_pts, shape

SKINS = [hexc(c) for c in ("#ffd9b8", "#f2bf94", "#d79a6b", "#b07848", "#8a5a36", "#6b4429")]
BLUSH = hexc("#ff8a8a", 0.45)

FOLK = {
    # recurring
    "anchor": dict(skin=SKINS[2], body=hexc("#ff7a59"), legs=hexc("#2b2d3a"), hair="quiff", hair_col=hexc("#1e1a2a"),
                   glasses=True, seed=201),
    # diesel story
    "trucker": dict(skin=SKINS[3], body=hexc("#d9534f"), legs=hexc("#2f5d9a"), hair="cap", hair_col=hexc("#2f5d9a"),
                    beard=hexc("#3a2418"), plaid=True, seed=203),
    "shopper": dict(skin=SKINS[0], body=hexc("#7bc96f"), legs=hexc("#3b3f4a"), hair="bun", hair_col=hexc("#8a4b2a"),
                    lashes=True, seed=205),
    "captain": dict(skin=SKINS[1], body=hexc("#f4f1ea"), legs=hexc("#23346b"), hair="captain",
                    hair_col=hexc("#23346b"), beard=hexc("#e8e2d4"), seed=207),
    "expert_a": dict(skin=SKINS[4], body=hexc("#5b8def"), legs=hexc("#2b2d3a"), hair="curls", hair_col=hexc("#1e1a2a"),
                     glasses=True, tie=hexc("#ffd23f"), seed=209),
    "expert_b": dict(skin=SKINS[0], body=hexc("#b388eb"), legs=hexc("#2b2d3a"), hair="bob", hair_col=hexc("#d9b26a"),
                     glasses=True, lashes=True, seed=211),
    # more story people
    "jobseeker": dict(skin=SKINS[2], body=hexc("#ffb347"), legs=hexc("#3f6fb5"), hair="short", hair_col=hexc("#2b2018"),
                      seed=241),
    "firefighter": dict(skin=SKINS[1], body=hexc("#3b3f4a"), legs=hexc("#3b3f4a"), hair="helmet",
                        hair_col=hexc("#d9302c"), beard=hexc("#6b4a2e"), stripes=True, seed=243),
    "inspector": dict(skin=SKINS[4], body=hexc("#4a6fa5"), legs=hexc("#2b2d3a"), hair="short", hair_col=hexc("#111111"),
                      glasses=True, tie=hexc("#e8e2d4"), seed=245),
    "rider": dict(skin=SKINS[0], body=hexc("#ff6fa5"), legs=hexc("#2b2d3a"), hair="bob", hair_col=hexc("#2b2018"),
                  lashes=True, seed=247),
    "mac_user": dict(skin=SKINS[3], body=hexc("#9ad1f5"), legs=hexc("#2b2d3a"), hair="curls", hair_col=hexc("#2b2018"),
                     seed=249),
    "doctor": dict(skin=SKINS[2], body=hexc("#f7f7f2"), legs=hexc("#5b8def"), hair="bun", hair_col=hexc("#1e1a2a"),
                   glasses=True, lashes=True, stethoscope=True, seed=251),
    "health_official": dict(skin=SKINS[1], body=hexc("#5a5f73"), legs=hexc("#23263a"), hair="gray",
                            hair_col=hexc("#d8d4cc"), tie=hexc("#2e6b5e"), seed=253),
    "builder": dict(skin=SKINS[3], body=hexc("#ff8a3d"), legs=hexc("#3f6fb5"), hair="hardhat",
                    hair_col=hexc("#f2c12e"), stripes=True, seed=255),
    "worker": dict(skin=SKINS[5], body=hexc("#4f86c6"), legs=hexc("#2b2d3a"), hair="cap", hair_col=hexc("#2b2d3a"),
                   seed=257),
    # generic officials (never portraits of real people)
    "official_1": dict(skin=SKINS[1], body=hexc("#3b4f7a"), legs=hexc("#23263a"), hair="side", hair_col=hexc("#4a3424"),
                       tie=hexc("#e0483d"), seed=221),
    "official_2": dict(skin=SKINS[3], body=hexc("#4a4f63"), legs=hexc("#23263a"), hair="bald", hair_col=hexc("#2b2018"),
                       tie=hexc("#2e9e8f"), seed=223),
    "official_3": dict(skin=SKINS[0], body=hexc("#8e2f4c"), legs=hexc("#23263a"), hair="bob", hair_col=hexc("#e8c46a"),
                       lashes=True, seed=225),
    "official_4": dict(skin=SKINS[5], body=hexc("#2b2d3a"), legs=hexc("#23263a"), hair="short", hair_col=hexc("#111111"),
                       tie=hexc("#ffd23f"), seed=227),
    "official_5": dict(skin=SKINS[2], body=hexc("#2e6b5e"), legs=hexc("#23263a"), hair="bun", hair_col=hexc("#2b2018"),
                       lashes=True, seed=229),
    "official_6": dict(skin=SKINS[1], body=hexc("#5a5f73"), legs=hexc("#23263a"), hair="gray", hair_col=hexc("#d8d4cc"),
                       glasses=True, tie=hexc("#5b8def"), seed=231),
    "official_7": dict(skin=SKINS[4], body=hexc("#6a3d8f"), legs=hexc("#23263a"), hair="curls", hair_col=hexc("#1e1a2a"),
                       seed=233),
}

# hand positions relative to the shoulder (front arm, facing right)
HANDS = {"down": (8, 70), "hip": (30, 40), "wave": (34, -70), "cheer": (14, -84), "point": (78, -10),
         "hold": (50, 30), "face": (-6, -54), "chin": (-12, -34), "thumb": (56, 4)}


def _arm(cr, sx, sy, pose, col, skin, seed, flip=False):
    hx, hy = HANDS.get(pose, HANDS["down"])
    if flip:
        hx = -hx * 0.6
    mx, my = sx + hx * 0.5 + (8 if hy < 0 else -6), sy + hy * 0.5
    for w, c in ((17, INK), (10, col)):
        cr.move_to(sx, sy)
        cr.curve_to(mx, my, mx, my, sx + hx, sy + hy)
        cr.set_line_width(w)
        cr.set_source_rgba(*c)
        cr.set_line_cap(1)
        cr.stroke()
    blob(cr, sx + hx, sy + hy, 11, 11, skin, seed, amp=0.3, lw=3.5)   # mitten hand


def _eyes(cr, kind, t, seed, lashes=False):
    shut = blink(t, seed) and kind in ("open", "wide", "sly")
    for sx in (-1, 1):
        x = sx * 17
        if shut or kind == "closed":
            line(cr, [(x - 9, 0), (x, 4), (x + 9, 0)], 3.5, INK, seed + sx, amp=0.2)
            continue
        if kind == "happy":
            line(cr, [(x - 9, 4), (x, -6), (x + 9, 4)], 4, INK, seed + sx, amp=0.2)
            continue
        ry = 15 if kind == "wide" else 12
        blob(cr, x, 0, 10 if kind != "wide" else 12, ry, WHITE, seed + 10 + sx, amp=0.3, lw=3)
        py = 3 if kind == "sad" else 2
        dot(cr, x + 2, py, 5.5 if kind != "wide" else 4.5, INK)
        dot(cr, x + 4, py - 3, 1.8, WHITE)   # the shine
        if kind == "sly":
            shape(cr, [(x - 11, -12), (x + 11, -12), (x + 11, -2), (x - 11, -4)], None, seed=seed + 20 + sx, amp=0.1,
                  lw=0, stroke=None)
            line(cr, [(x - 11, -3), (x + 11, -1)], 3.5, INK, seed + 22 + sx, amp=0.1)
        if lashes:
            line(cr, [(x + sx * 7, -9), (x + sx * 12, -15)], 2.5, INK, seed + 30 + sx, amp=0.1)
    # eyebrows
    tilt = {"sad": 5, "wide": -4, "sly": 3}.get(kind, 0)
    for sx in (-1, 1):
        x = sx * 17
        line(cr, [(x - 9, -19 - tilt * sx * 0.5), (x + 9, -19 + tilt * sx * 0.5)], 3.5, INK, seed + 40 + sx, amp=0.2)


def _mouth(cr, kind, t, seed):
    if kind == "talk":
        kind = "o" if int(t * 12) % 2 else "smile"
    if kind == "smile":
        line(cr, [(-12, 0), (0, 8), (12, 0)], 3.5, INK, seed, amp=0.2)
    elif kind == "grin":
        shape(cr, [(-15, -2), (15, -2), (8, 13), (-8, 13)], hexc("#7a2b35"), seed=seed, amp=0.3, lw=3)
        shape(cr, [(-12, -1), (12, -1), (10, 3), (-10, 3)], WHITE, seed=seed + 1, amp=0.1, lw=0, stroke=None)
    elif kind == "o":
        blob(cr, 0, 4, 7, 9, hexc("#7a2b35"), seed, amp=0.3, lw=3)
    elif kind == "flat":
        line(cr, [(-9, 3), (9, 3)], 3.5, INK, seed, amp=0.2)
    elif kind == "sad":
        line(cr, [(-11, 8), (0, 1), (11, 8)], 3.5, INK, seed, amp=0.2)


def _hair(cr, kind, col, hr, seed):
    if kind == "quiff":
        shape(cr, [(-hr, -6), (-hr + 4, -hr + 4), (-10, -hr - 6), (20, -hr - 18), (hr, -hr + 2), (hr + 2, -8),
                   (hr - 10, -hr + 18), (-hr + 14, -hr + 22)], col, seed=seed, amp=0.6, lw=3)
    elif kind == "cap":
        shape(cr, [(-hr - 2, -8), (-hr + 2, -hr + 2), (0, -hr - 10), (hr - 2, -hr + 2), (hr + 2, -8)], col, seed=seed,
              amp=0.5, lw=3.5)
        shape(cr, rrect_pts(hr - 14, -16, 46, 12, 6, 10), col, seed=seed + 1, amp=0.3, lw=3.5)
        blob(cr, 0, -hr + 10, 10, 9, WHITE, seed + 2, amp=0.2, lw=2.5)
    elif kind == "captain":
        shape(cr, [(-hr - 4, -12), (-hr + 4, -hr - 2), (hr - 4, -hr - 2), (hr + 4, -12)], WHITE, seed=seed, amp=0.4,
              lw=3.5)
        shape(cr, rrect_pts(-hr - 6, -20, 2 * hr + 12, 14, 6, 12), col, seed=seed + 1, amp=0.3, lw=3.5)
        blob(cr, 0, -hr + 10, 9, 8, hexc("#f2b632"), seed + 2, amp=0.2, lw=2.5)
    elif kind == "bun":
        blob(cr, 0, -hr - 14, 20, 18, col, seed + 1, amp=0.4, lw=3)
        shape(cr, [(-hr - 2, 6), (-hr, -hr + 10), (0, -hr - 4), (hr, -hr + 10), (hr + 2, 6), (hr - 8, -hr + 24),
                   (-hr + 8, -hr + 24)], col, seed=seed, amp=0.5, lw=3)
    elif kind == "bob":
        shape(cr, [(-hr - 6, 26), (-hr - 4, -hr + 6), (0, -hr - 8), (hr + 4, -hr + 6), (hr + 6, 26), (hr - 6, 20),
                   (hr - 10, -hr + 22), (-hr + 10, -hr + 22), (-hr + 6, 20)], col, seed=seed, amp=0.5, lw=3)
    elif kind == "curls":
        for k in range(7):
            a = math.pi + k * math.pi / 6
            blob(cr, (hr - 2) * math.cos(a), -6 + (hr - 2) * math.sin(a), 14, 14, col, seed + k, amp=0.4, lw=2.5)
    elif kind == "side":
        shape(cr, [(-hr, -4), (-hr + 2, -hr + 6), (10, -hr - 6), (hr, -hr + 8), (hr + 2, -6), (hr - 8, -hr + 20),
                   (-hr + 20, -hr + 14)], col, seed=seed, amp=0.5, lw=3)
    elif kind == "short":
        shape(cr, [(-hr, -10), (-hr + 4, -hr + 4), (0, -hr - 4), (hr - 4, -hr + 4), (hr, -10), (hr - 6, -hr + 16),
                   (-hr + 6, -hr + 16)], col, seed=seed, amp=0.4, lw=3)
    elif kind == "helmet":   # fire helmet with a wide brim
        shape(cr, [(-hr - 4, -6), (-hr + 4, -hr - 2), (0, -hr - 16), (hr - 4, -hr - 2), (hr + 4, -6)], col, seed=seed,
              amp=0.4, lw=3.5)
        shape(cr, rrect_pts(-hr - 18, -14, 2 * hr + 36, 14, 7, 12), col, seed=seed + 1, amp=0.3, lw=3.5)
        blob(cr, 0, -hr + 6, 11, 10, hexc("#f2b632"), seed + 2, amp=0.2, lw=2.5)
    elif kind == "hardhat":
        shape(cr, [(-hr - 2, -8), (-hr + 4, -hr), (0, -hr - 12), (hr - 4, -hr), (hr + 2, -8)], col, seed=seed, amp=0.4,
              lw=3.5)
        shape(cr, rrect_pts(-hr - 8, -14, 2 * hr + 16, 10, 5, 12), col, seed=seed + 1, amp=0.3, lw=3.5)
    elif kind in ("bald", "gray"):
        for sx in (-1, 1):
            blob(cr, sx * (hr - 4), -4, 10, 16, col, seed + sx, amp=0.4, lw=2.5)


def folk(cr, who, x, y, t, facing=1, arms=("down", "down"), eyes="open", mouth="smile", scale=1.0, walk=None,
         jump=0.0, sweat=False, shake=0.0, talking=False):
    c = FOLK[who]
    seed = c["seed"]
    hr, bw, bh = 46, 92, 104
    with at(cr, x, y - jump, scale, flip=facing < 0):
        if shake:
            cr.translate(math.sin(t * 60) * shake, 0)
        ph = walk * 2 * math.pi if walk is not None else 0.0
        bob = abs(math.sin(ph)) * 4 if walk is not None else math.sin(t * 2.4 + seed) * 1.5
        # legs and shoes
        for side, off in ((-1, 0.0), (1, math.pi)):
            fx = side * 20 + (math.sin(ph + off) * 14 if walk is not None else 0)
            lift = max(0.0, math.sin(ph + off)) * 10 if walk is not None else 0
            line(cr, [(side * 18, -40), (fx, -12 - lift)], 15, INK, seed + side, amp=0.2)
            line(cr, [(side * 18, -40), (fx, -12 - lift)], 8, c["legs"], seed + side, amp=0.2)
            blob(cr, fx + 8, -9 - lift, 17, 9, INK, seed + 3 + side, amp=0.3, lw=0, stroke=None)
        cr.translate(0, -bob)
        top = -40 - bh
        _arm(cr, -bw * 0.38, top + 30, arms[1], c["body"], c["skin"], seed + 5, flip=True)   # back arm
        # bean body
        shape(cr, rrect_pts(-bw / 2, top, bw, bh, 40, 18), c["body"], seed=seed + 6, amp=0.6, lw=4.5)
        if c.get("plaid"):
            for k in range(3):
                line(cr, [(-bw / 2 + 10, top + 26 + k * 26), (bw / 2 - 10, top + 26 + k * 26)], 3,
                     hexc("#ffffff", 0.35), seed + 7 + k, amp=0.3)
                line(cr, [(-26 + k * 26, top + 10), (-26 + k * 26, top + bh - 10)], 3, hexc("#ffffff", 0.35),
                     seed + 10 + k, amp=0.3)
        if c.get("stripes"):   # reflective bands on a firefighter's coat
            for yy in (top + 50, top + 80):
                line(cr, [(-bw / 2 + 6, yy), (bw / 2 - 6, yy)], 7, hexc("#f2e05a"), seed + 12, amp=0.2)
        if c.get("stethoscope"):
            cr.save()
            cr.new_path()
            cr.arc(0, top + 6, 26, 0.3, math.pi - 0.3)
            cr.set_line_width(4)
            cr.set_source_rgba(*INK)
            cr.stroke()
            cr.restore()
            blob(cr, 18, top + 40, 7, 7, hexc("#a9adb5"), seed + 13, amp=0.2, lw=2.5)
        if c.get("tie"):
            shape(cr, [(-7, top + 6), (7, top + 6), (10, top + 54), (0, top + 64), (-10, top + 54)], c["tie"],
                  seed=seed + 14, amp=0.2, lw=3)
        # head
        hy = top - hr + 10
        with at(cr, 0, hy):
            blob(cr, 0, 0, hr, hr * 0.96, c["skin"], seed + 15, amp=0.5, lw=4.5)
            if c.get("beard"):
                shape(cr, [(-hr + 6, 6), (-hr + 14, 30), (0, hr - 2), (hr - 14, 30), (hr - 6, 6), (12, 22),
                           (-12, 22)], c["beard"], seed=seed + 16, amp=0.4, lw=3)
            _hair(cr, c.get("hair"), c["hair_col"], hr, seed + 17)
            with at(cr, 8, -4):
                _eyes(cr, eyes, t, seed + 20, c.get("lashes"))
                if c.get("glasses"):
                    for sx in (-1, 1):
                        blob(cr, sx * 17, 1, 16, 15, None, seed + 50 + sx, amp=0.2, lw=3)
                    line(cr, [(-2, 0), (2, 0)], 3, INK, seed + 53, amp=0.1)
            blob(cr, 12, 14, 6, 5, hexc("#000000", 0.12), seed + 54, amp=0.1, lw=0, stroke=None)   # nose
            for sx in (-1, 1):
                dot(cr, 8 + sx * 26, 18, 6, BLUSH)
            with at(cr, 10, 30):
                _mouth(cr, "talk" if talking else mouth, t, seed + 60)
        if sweat:
            k = (t * 0.8) % 1
            blob(cr, -hr + 6, hy - 16 + k * 22, 6, 9, hexc("#6cc4f0"), seed + 61, amp=0.2, lw=2.5)
        _arm(cr, bw * 0.38, top + 30, arms[0], c["body"], c["skin"], seed + 70)   # front arm
