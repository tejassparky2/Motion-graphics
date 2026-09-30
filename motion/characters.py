"""Original cast and props for "The Pumpkin Trick".

Characters are drawn with their feet at (x, y). `facing` = 1 looks right, -1 looks left.
"""
import math

from .engine import (INK, RED, WHITE, at, blink, blob, dot, hexc, line, poly_pts, rrect_pts, shape,
                     sharp_shape, write)

SKIN_LIGHT = hexc("#f3c9a2")
SKIN_MID = hexc("#d9975f")
SKIN_TAN = hexc("#b9794a")
PURPLE = hexc("#6a4c9c")
PURPLE_D = hexc("#4b3474")
GOLD = hexc("#f2b632")
GREEN = hexc("#79b061")
GREEN_D = hexc("#4e8a3e")
YELLOW = hexc("#f6cf4f")
DENIM = hexc("#3f6fb5")
CAP_RED = hexc("#e0483f")
TURBAN = hexc("#f39a2b")
DHOTI = hexc("#f4efe1")
PUMPKIN = hexc("#f2892a")
PUMPKIN_D = hexc("#d86a18")
STEM = hexc("#5b8a3a")
WOOD = hexc("#b8672b")
WOOD_D = hexc("#8e4a1e")
CASH = hexc("#5dbb63")
CASH_D = hexc("#3d8f45")
TEAL = hexc("#2e9aa6")
TEAL_D = hexc("#1f6f78")
TYRE = hexc("#3a3140")
SHOE = hexc("#3b2a26")
BLUSH = hexc("#f08a7a", 0.45)
TEAR = hexc("#6cc4f0")
GLASS = hexc("#241c2b")

CAST = {
    "seth": dict(skin=SKIN_LIGHT, shirt=PURPLE, pants=PURPLE_D, bw=118, bh=118, head=40, kind="belly"),
    "ramu": dict(skin=SKIN_TAN, shirt=GREEN, pants=DHOTI, bw=96, bh=104, head=40, kind="box"),
    "chotu": dict(skin=SKIN_MID, shirt=YELLOW, pants=DENIM, bw=74, bh=92, head=36, kind="slim"),
    # "The $5 Lucky Charm" cast
    "sam": dict(skin=SKIN_MID, shirt=hexc("#6f8fb0"), pants=DENIM, bw=92, bh=102, head=40, kind="hoodie",
                hair="messy", hair_col=hexc("#3a2a22"), blush=True, seed=51),
    "mia": dict(skin=hexc("#f0c29c"), shirt=hexc("#e0487a"), pants=hexc("#f0c29c"), bw=78, bh=112, head=38,
                kind="dress", hair="long", hair_col=hexc("#5a2e1c"), lashes=True, blush=True, seed=63),
    "beggar": dict(skin=SKIN_TAN, shirt=hexc("#9a7a52"), pants=hexc("#6b5a45"), bw=90, bh=98, head=40, kind="ragged",
                   hair="scruffy", hair_col=hexc("#6d6258"), beard=hexc("#8a7f74"), seed=77),
    # "The Great Emu War" cast
    "soldier": dict(skin=SKIN_LIGHT, shirt=hexc("#9a8a55"), pants=hexc("#7d6f44"), bw=92, bh=104, head=38,
                    kind="uniform", hair="slouch", hair_col=hexc("#6b5a3a"), moustache=True, seed=91),
    "farmer": dict(skin=hexc("#e8b48a"), shirt=hexc("#c0504d"), pants=DENIM, bw=96, bh=104, head=40,
                   kind="plaid", hair="strawhat", hair_col=hexc("#e8c46a"), seed=97),
    # "The 40-Year Lottery Ticket" cast
    "oldman": dict(skin=hexc("#e8b48a"), shirt=hexc("#8a6f4d"), pants=hexc("#6b6f78"), bw=94, bh=100, head=40,
                   kind="cardigan", hair="gray", hair_col=hexc("#d8d4cc"), glasses=True, seed=103),
    "owner": dict(skin=SKIN_MID, shirt=hexc("#5b7c99"), pants=hexc("#3b3f4a"), bw=100, bh=108, head=40,
                  kind="apron", hair="bald", hair_col=hexc("#d8d4cc"), glasses=True, moustache=True, seed=109),
    # game-show host (The Monty Hall Problem)
    "host": dict(skin=hexc("#e8b48a"), shirt=hexc("#c9a227"), pants=hexc("#2b2d3a"), bw=96, bh=108, head=40,
                 kind="suit", hair="slick", hair_col=hexc("#3a2a22"), seed=113),
    # The Shortest War / Hilbert's Hotel
    "claimant": dict(skin=SKIN_TAN, shirt=hexc("#f4efe1"), pants=hexc("#f4efe1"), bw=92, bh=112, head=40, kind="robe",
                     hair="kofia", hair_col=hexc("#2f6f5e"), moustache=True, seed=141),
    "successor": dict(skin=SKIN_MID, shirt=hexc("#e9dcc0"), pants=hexc("#e9dcc0"), bw=92, bh=112, head=40, kind="robe",
                      hair="kofia", hair_col=hexc("#8e2f2c"), beard=hexc("#3a3a3a"), seed=149),
    "hilbert": dict(skin=hexc("#f0c29c"), shirt=hexc("#4a4f63"), pants=hexc("#2b2d3a"), bw=92, bh=110, head=40,
                    kind="suit", hair="gray", hair_col=hexc("#d8d3c4"), glasses=True, beard=hexc("#b9b4a6"), seed=151),
    # batch 3: a 1970s garage band, and a 1920s con man
    "rocker_a": dict(skin=hexc("#f0c29c"), shirt=hexc("#6a45b5"), pants=DENIM, bw=86, bh=106, head=38, kind="slim",
                     hair="long", hair_col=hexc("#8e4a1e"), seed=161),
    "rocker_b": dict(skin=SKIN_MID, shirt=hexc("#e8a93b"), pants=hexc("#5a3e2b"), bw=90, bh=104, head=40, kind="slim",
                     hair="messy", hair_col=hexc("#1f1a18"), beard=hexc("#1f1a18"), seed=167),
    "lustig": dict(skin=hexc("#f0c29c"), shirt=hexc("#2b2d3a"), pants=hexc("#1f2029"), bw=90, bh=112, head=39,
                   kind="suit", hair="slick", hair_col=hexc("#1f1a18"), moustache=True, seed=173),
    # classroom cast (The Backbencher)
    "teacher": dict(skin=hexc("#f0c29c"), shirt=hexc("#f4efe1"), pants=hexc("#555a66"), bw=94, bh=110, head=40,
                    kind="shirt_tie", hair="slick", hair_col=hexc("#3a2a22"), glasses=True, moustache=True, seed=121),
    "kid_a": dict(skin=hexc("#f0c29c"), shirt=hexc("#e0487a"), pants=DENIM, bw=78, bh=90, head=36, kind="slim",
                  hair="long", hair_col=hexc("#3a2a22"), lashes=True, blush=True, seed=127),
    "kid_b": dict(skin=SKIN_TAN, shirt=hexc("#79b061"), pants=DENIM, bw=80, bh=90, head=36, kind="slim",
                  hair="messy", hair_col=hexc("#1f1a18"), blush=True, seed=131),
    "kid_c": dict(skin=SKIN_MID, shirt=hexc("#4fb3e8"), pants=DENIM, bw=80, bh=90, head=36, kind="slim",
                  hair="slick", hair_col=hexc("#5a2e1c"), blush=True, seed=137),
    "richbeggar": dict(skin=SKIN_TAN, shirt=hexc("#2b2d3a"), pants=hexc("#2b2d3a"), bw=96, bh=104, head=40,
                       kind="suit", hair="slick", hair_col=hexc("#6d6258"), beard=hexc("#8a7f74"), shades=True,
                       seed=77),
}

# hand targets relative to the shoulder, for the arm on the facing side ("front")
HAND = {
    "down": (6, 62),
    "hip": (24, 36),
    "wave": (26, -62),
    "cheer": (18, -72),
    "thumb": (46, 2),
    "point": (64, -8),
    "give": (60, 18),
    "hold": (38, 34),
    "chin": (-14, -26),
    "rub": (-28, 40),
    "face": (-18, -40),
}


def _arm(cr, sx, sy, hx, hy, color, skin, bend=1):
    mx, my = (sx + hx) / 2, (sy + hy) / 2
    dx, dy = hx - sx, hy - sy
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * 14 * bend, my + dx / L * 14 * bend
    for w, col in ((15, INK), (8, color)):
        cr.move_to(sx, sy)
        cr.curve_to(cx, cy, cx, cy, hx, hy)
        cr.set_line_width(w)
        cr.set_source_rgba(*col)
        cr.set_line_cap(1)
        cr.stroke()
    blob(cr, hx, hy, 9, 9, skin, seed=int(hx * 7 + hy), amp=0.6, lw=3)


def cash(cr, x, y, s=1.0, seed=3, rot=-0.15):
    with at(cr, x, y, s, rot):
        for i in range(3):
            sharp_shape(cr, [(-26, -14 - i * 5), (26, -14 - i * 5), (26, 14 - i * 5), (-26, 14 - i * 5)],
                        CASH, seed=seed + i, amp=0.8, lw=3)
        sharp_shape(cr, [(-6, -24), (6, -24), (6, 4), (-6, 4)], hexc("#f2e8c9"), seed=seed + 9, amp=0.5, lw=2.5)
        write(cr, [("₹", CASH_D)], 14, 2, 18, align="center", bold=True)


def briefcase(cr, x, y, seed=4):
    sharp_shape(cr, [(x - 24, y), (x + 24, y), (x + 24, y + 34), (x - 24, y + 34)], WOOD_D, seed=seed, amp=0.8, lw=3.5)
    line(cr, [(x - 9, y), (x - 9, y - 9), (x + 9, y - 9), (x + 9, y)], 3.5, INK, seed=seed + 1, amp=0.4)
    dot(cr, x, y + 12, 3.5, GOLD)


def _eyes(cr, kind, ex, ey, t, seed, sun=False):
    if sun:
        for sx in (-1, 1):
            shape(cr, rrect_pts(ex + sx * 17 - 14, ey - 10, 28, 20, 8, 12), GLASS, seed=seed + sx, amp=0.6, lw=3)
        line(cr, [(ex - 3, ey - 4), (ex + 3, ey - 4)], 3, INK, seed, amp=0.3)
        # glint
        line(cr, [(ex - 24, ey - 4), (ex - 18, ey - 7)], 2.5, hexc("#ffffff", 0.8), seed, amp=0)
        if kind == "rupee":
            for sx in (-1, 1):
                write(cr, [("₹", GOLD)], ex + sx * 17, ey + 8, 22, align="center", bold=True)
        return
    blinking = blink(t, seed) and kind in ("dot", "wide", "sly")
    for sx in (-1, 1):
        x = ex + sx * 15
        if blinking:
            line(cr, [(x - 6, ey), (x + 6, ey)], 3.5, INK, seed + sx, amp=0.3)
        elif kind == "dot":
            dot(cr, x, ey, 5)
        elif kind == "wide":
            blob(cr, x, ey, 10, 11, WHITE, seed + sx, amp=0.5, lw=3)
            dot(cr, x + 2, ey + 1, 4.5)
        elif kind == "happy":
            line(cr, [(x - 7, ey + 3), (x, ey - 5), (x + 7, ey + 3)], 3.5, INK, seed + sx, amp=0.4)
        elif kind in ("closed", "cry"):
            line(cr, [(x - 7, ey - 2), (x, ey + 4), (x + 7, ey - 2)], 3.5, INK, seed + sx, amp=0.4)
        elif kind == "sad":
            dot(cr, x, ey + 2, 4.5)
            line(cr, [(x - 8, ey - 10 - sx * 3), (x + 8, ey - 10 + sx * 3)], 3, INK, seed + sx, amp=0.3)
        elif kind == "sly":
            dot(cr, x + 2, ey + 1, 4.5)
            line(cr, [(x - 8, ey - 3), (x + 8, ey - 1)], 3.5, INK, seed + sx, amp=0.3)
        elif kind == "rupee":
            blob(cr, x, ey, 12, 13, WHITE, seed + sx, amp=0.5, lw=3)
            write(cr, [("₹", RED)], x, ey + 8, 22, align="center", bold=True)


def _mouth(cr, kind, mx, my, seed, t):
    if kind == "smile":
        line(cr, [(mx - 11, my - 2), (mx, my + 5), (mx + 11, my - 2)], 3.5, INK, seed, amp=0.4)
    elif kind == "flat":
        line(cr, [(mx - 8, my + 1), (mx + 8, my)], 3.5, INK, seed, amp=0.4)
    elif kind == "sad":
        line(cr, [(mx - 10, my + 5), (mx, my - 1), (mx + 10, my + 5)], 3.5, INK, seed, amp=0.4)
    elif kind == "o":
        blob(cr, mx, my + 2, 6, 8, hexc("#7a2b35"), seed, amp=0.5, lw=3)
    elif kind == "smirk":
        line(cr, [(mx - 10, my + 2), (mx + 2, my + 3), (mx + 12, my - 4)], 3.5, INK, seed, amp=0.4)
    elif kind in ("grin", "laugh"):
        h = 16 if kind == "grin" else 20 + 4 * abs(math.sin(t * 18))
        pts = [(mx - 16, my - 3), (mx + 16, my - 3), (mx + 10, my - 3 + h * 0.8), (mx, my - 3 + h), (mx - 10, my - 3 + h * 0.8)]
        shape(cr, pts, hexc("#7a2b35"), seed, amp=0.5, lw=3)
        sharp_shape(cr, [(mx - 13, my - 2), (mx + 13, my - 2), (mx + 11, my + 3), (mx - 11, my + 3)], WHITE,
                    seed, amp=0.3, lw=0, stroke=None)
    elif kind == "wobble":
        line(cr, [(mx - 12, my + 2), (mx - 6, my - 2), (mx, my + 2), (mx + 6, my - 2), (mx + 12, my + 2)], 3,
             INK, seed, amp=0.5)


def person(cr, who, x, y, t, facing=1, walk=None, arms=("down", "down"), eyes="dot", mouth="smile",
           item=None, bob=True, shake=0.0, tears=False, sweat=False, scale=1.0, jump=0.0, lean=0.0):
    """Draw a character. `walk` is a phase in cycles (None = standing). `arms` = (front, back)."""
    c = CAST[who]
    seed = c.get("seed") or {"seth": 11, "ramu": 23, "chotu": 37}[who]
    skin, bw, bh, hr = c["skin"], c["bw"], c["bh"], c["head"]
    legs = 26
    with at(cr, x, y - jump, scale, flip=facing < 0):
        ph = walk * 2 * math.pi if walk is not None else 0.0
        b = 0.0
        if walk is not None:
            b = abs(math.sin(ph)) * 5
        elif bob:
            b = math.sin(t * 2.6 + seed) * 1.6
        if shake:
            cr.translate(math.sin(t * 60) * shake, 0)
        # ---- feet / legs
        for side, off in ((-1, 0), (1, math.pi)):
            fx = side * bw * 0.22 + (math.sin(ph + off) * 12 if walk is not None else 0)
            lift = max(0.0, math.sin(ph + off)) * 9 if walk is not None else 0
            line(cr, [(side * bw * 0.2, -legs - 4), (fx, -8 - lift)], 9, INK, seed + side, amp=0.4)
            line(cr, [(side * bw * 0.2, -legs - 4), (fx, -8 - lift)], 4, c["pants"], seed + side, amp=0.4)
            blob(cr, fx + 7, -7 - lift, 15, 8, SHOE, seed + side * 3, amp=0.6, lw=3)
        cr.translate(0, -legs - b)
        if lean:
            cr.rotate(lean)
        top = -bh
        # back arm first (behind body)
        sxb, syb = -bw / 2 + 12, top + 26
        hb = HAND[arms[1]]
        hbx, hby = sxb - hb[0] * 0.8, syb + hb[1]
        if arms[1] == "wave":
            hbx += math.sin(t * 12) * 10
        _arm(cr, sxb, syb, hbx, hby, c["shirt"], skin, bend=-1)
        # ---- body
        kind = c["kind"]
        if kind == "belly":
            shape(cr, poly_pts([(-bw / 2 + 8, top + 8), (bw / 2 - 8, top + 8), (bw / 2 + 6, -40), (bw / 2 - 10, 0),
                                (-bw / 2 + 10, 0), (-bw / 2 - 6, -40)], 14), c["shirt"], seed, amp=1.2)
            # shirt V, tie, gold chain
            shape(cr, [(-18, top + 10), (18, top + 10), (0, top + 52)], WHITE, seed + 1, amp=0.6, lw=3)
            sharp_shape(cr, [(-5, top + 14), (5, top + 14), (8, top + 44), (0, top + 54), (-8, top + 44)], RED,
                        seed + 2, amp=0.5, lw=3)
            line(cr, [(-30, top + 18), (-22, top + 50), (0, top + 64), (22, top + 50), (30, top + 18)], 4.5, GOLD,
                 seed + 3, amp=0.6)
            dot(cr, 0, top + 66, 7, GOLD)
        elif kind == "box":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 30), c["shirt"], seed, amp=1.2)
            line(cr, [(6, top + 12), (6, top + 60)], 3, GREEN_D, seed + 1, amp=0.6)
            for k in range(3):
                dot(cr, 12, top + 22 + k * 14, 3, INK)
        elif kind == "hoodie":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 30), c["shirt"], seed, amp=1.2)
            shape(cr, [(-24, top + 4), (0, top + 20), (24, top + 4)], None, seed + 1, amp=0.4, lw=3, closed=False)
            line(cr, [(-6, top + 18), (-8, top + 44)], 2.5, INK, seed + 2, amp=0.3)   # drawstrings
            line(cr, [(6, top + 18), (8, top + 44)], 2.5, INK, seed + 3, amp=0.3)
            shape(cr, rrect_pts(-28, top + bh - 44, 56, 24, 8, 14), hexc("#5d7a98"), seed + 4, amp=0.5, lw=3)
        elif kind == "dress":
            shape(cr, poly_pts([(-bw / 2 + 12, top + 6), (bw / 2 - 12, top + 6), (bw / 2 + 16, 0), (-bw / 2 - 16, 0)], 14),
                  c["shirt"], seed, amp=1.0)
            line(cr, [(-bw / 2 + 4, top + 44), (0, top + 50), (bw / 2 - 4, top + 44)], 4, hexc("#b8325e"), seed + 1,
                 amp=0.4)
            dot(cr, 0, top + 16, 5, hexc("#fff3c4"))   # pendant
            line(cr, [(-14, top + 4), (0, top + 16), (14, top + 4)], 2, hexc("#f2b632"), seed + 2, amp=0.3)
        elif kind == "ragged":
            pts = rrect_pts(-bw / 2, top, bw, bh - 10, 22)
            pts += [(-bw / 2 + 8, -2), (-bw / 2 + 22, -14)]
            shape(cr, poly_pts([(-bw / 2, top + 10), (bw / 2, top + 10), (bw / 2 + 4, -6), (bw / 4, 4), (0, -8),
                                (-bw / 4, 4), (-bw / 2 - 4, -6)], 14), c["shirt"], seed, amp=1.6)
            shape(cr, rrect_pts(12, top + 40, 22, 20, 4, 10), hexc("#c49a5c"), seed + 1, amp=0.8, lw=2.5)   # patch
            line(cr, [(-26, top + 30), (-14, top + 38)], 2.5, INK, seed + 2, amp=0.6)
        elif kind == "robe":   # long robe down to the ankles, embroidered collar
            shape(cr, poly_pts([(-bw / 2 + 4, top), (bw / 2 - 4, top), (bw / 2 + 8, legs - 6), (-bw / 2 - 8, legs - 6)], 14),
                  c["shirt"], seed, amp=1.0)
            line(cr, [(-14, top + 4), (0, top + 18), (14, top + 4)], 3.5, GOLD, seed + 1, amp=0.4)
            line(cr, [(0, top + 18), (0, top + 60)], 3, GOLD, seed + 2, amp=0.4)
        elif kind == "shirt_tie":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 24), c["shirt"], seed, amp=1.0)
            shape(cr, [(-16, top + 2), (0, top + 16), (16, top + 2)], hexc("#e3dccb"), seed + 1, amp=0.3, lw=3)
            sharp_shape(cr, [(-5, top + 14), (5, top + 14), (9, top + 60), (0, top + 72), (-9, top + 60)], hexc("#c0504d"),
                        seed + 2, amp=0.4, lw=3)
            shape(cr, rrect_pts(bw / 2 - 30, top + 22, 18, 16, 3, 8), hexc("#e3dccb"), seed + 3, amp=0.3, lw=2.5)
        elif kind == "cardigan":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 26), c["shirt"], seed, amp=1.0)
            shape(cr, [(-14, top + 4), (14, top + 4), (0, top + 40)], hexc("#f4efe1"), seed + 1, amp=0.4, lw=3)
            line(cr, [(0, top + 40), (0, top + bh - 6)], 3, INK, seed + 2, amp=0.3)
            for k in range(3):
                dot(cr, 6, top + 52 + k * 16, 3.5, hexc("#f2b632"))
        elif kind == "apron":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 26), c["shirt"], seed, amp=1.0)
            shape(cr, rrect_pts(-bw / 2 + 14, top + 22, bw - 28, bh - 26, 12, 16), hexc("#f4efe1"), seed + 1, amp=0.6,
                  lw=3)
            shape(cr, rrect_pts(-16, top + 60, 32, 22, 4, 10), hexc("#e3dccb"), seed + 2, amp=0.4, lw=2.5)
        elif kind == "uniform":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 22), c["shirt"], seed, amp=1.0)
            line(cr, [(0, top + 6), (0, top + bh - 6)], 3, INK, seed + 1, amp=0.4)
            for k in range(3):
                dot(cr, 6, top + 22 + k * 22, 3.5, hexc("#c9a64a"))
            shape(cr, rrect_pts(-bw / 2 + 10, top + 30, 26, 20, 4, 10), hexc("#8a7a48"), seed + 2, amp=0.5, lw=2.5)
            line(cr, [(-bw / 2 + 2, top + bh - 22), (bw / 2 - 2, top + bh - 22)], 7, hexc("#5a4a2c"), seed + 3, amp=0.4)
        elif kind == "plaid":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 26), c["shirt"], seed, amp=1.0)
            for k in range(1, 4):
                line(cr, [(-bw / 2 + 4, top + k * bh / 4), (bw / 2 - 4, top + k * bh / 4)], 3, hexc("#8e2f2c"), seed + k,
                     amp=0.5)
                line(cr, [(-bw / 2 + k * bw / 4, top + 4), (-bw / 2 + k * bw / 4, top + bh - 4)], 3, hexc("#8e2f2c"),
                     seed + 10 + k, amp=0.5)
        elif kind == "suit":
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 26), c["shirt"], seed, amp=1.0)
            shape(cr, [(-16, top + 4), (16, top + 4), (0, top + 50)], WHITE, seed + 1, amp=0.5, lw=3)
            sharp_shape(cr, [(-4, top + 10), (4, top + 10), (7, top + 38), (0, top + 48), (-7, top + 38)], GOLD,
                        seed + 2, amp=0.4, lw=2.5)
            dot(cr, 24, top + 26, 4, GOLD)
        else:
            shape(cr, rrect_pts(-bw / 2, top, bw, bh, 24), c["shirt"], seed, amp=1.2)
            line(cr, [(-bw / 2 + 4, top + 50), (bw / 2 - 4, top + 50)], 5, hexc("#e8a93b"), seed + 1, amp=0.6)
        # ---- head
        hy = top - hr + 12
        hair = c.get("hair")
        hc = c.get("hair_col", INK)
        if hair == "long":   # hair behind the head, down to the shoulders
            shape(cr, [(-hr - 10, hy - 10), (-hr - 4, hy - hr), (0, hy - hr - 10), (hr + 4, hy - hr), (hr + 12, hy - 6),
                       (hr + 16, hy + 50), (hr - 4, hy + 62), (-hr + 4, hy + 62), (-hr - 14, hy + 50)], hc, seed + 12,
                  amp=0.8, lw=3.5)
        blob(cr, 0, hy, hr, hr * 0.95, skin, seed + 5, amp=0.9)
        fx = 7  # face shifted toward facing side
        if c.get("beard"):
            shape(cr, [(-hr + 8, hy + 14), (fx - 8, hy + 20), (fx + 10, hy + 20), (hr - 6, hy + 14), (hr - 10, hy + 32),
                       (fx, hy + hr + 6), (-hr + 14, hy + 32)], c["beard"], seed + 13, amp=1.2, lw=3)
        if hair == "messy":
            shape(cr, [(-hr - 2, hy - 4), (-hr, hy - hr + 4), (-hr + 10, hy - hr - 10), (-8, hy - hr - 4), (0, hy - hr - 16),
                       (12, hy - hr - 4), (26, hy - hr - 12), (hr + 2, hy - hr + 2), (hr + 4, hy - 8), (hr - 8, hy - 18),
                       (4, hy - 24), (-16, hy - 18)], hc, seed + 6, amp=0.9, lw=3)
        elif hair == "long":
            shape(cr, [(-hr - 2, hy - 2), (-hr + 2, hy - hr * 0.7), (-6, hy - hr - 6), (hr * 0.7, hy - hr + 2), (hr + 4, hy - 6),
                       (hr - 4, hy - 16), (8, hy - 22), (-hr + 14, hy - 16)], hc, seed + 6, amp=0.8, lw=3)
            dot(cr, fx - hr + 4, hy + 16, 4, GOLD)   # earring
        elif hair == "scruffy":
            shape(cr, [(-hr - 4, hy), (-hr - 2, hy - hr + 2), (-10, hy - hr - 10), (hr - 4, hy - hr - 6), (hr + 6, hy - 2),
                       (hr - 6, hy - 14), (-4, hy - 22), (-hr + 8, hy - 10)], hc, seed + 6, amp=1.8, lw=3)
        elif hair == "gray":   # tufts over the ears, bald on top
            for sx in (-1, 1):
                blob(cr, sx * (hr - 4), hy - 14, 14, 16, hc, seed + 6 + sx, amp=1.0, lw=3)
            line(cr, [(-10, hy - hr + 4), (0, hy - hr - 4), (8, hy - hr + 2)], 3, hc, seed + 8, amp=0.6)
        elif hair == "bald":
            for sx in (-1, 1):
                blob(cr, sx * (hr - 2), hy - 6, 10, 14, hc, seed + 6 + sx, amp=0.8, lw=3)
            blob(cr, -8, hy - hr + 12, 10, 5, hexc("#ffffff", 0.45), seed + 8, amp=0.3, lw=0, stroke=None)
        elif hair == "slouch":   # wide-brimmed army hat, one side pinned up
            shape(cr, [(-hr - 28, hy - 18), (hr + 24, hy - 22), (hr + 30, hy - 12), (-hr - 30, hy - 8)], hc, seed + 6,
                  amp=0.8, lw=3.5)
            shape(cr, [(-hr + 4, hy - 18), (-hr + 10, hy - hr - 8), (hr - 8, hy - hr - 6), (hr - 2, hy - 20)], hc, seed + 7,
                  amp=0.8, lw=3.5)
            line(cr, [(-hr + 8, hy - 24), (hr - 4, hy - 26)], 4, hexc("#3a2a1e"), seed + 8, amp=0.3)
            shape(cr, [(-hr - 28, hy - 18), (-hr - 20, hy - 46), (-hr - 4, hy - 30)], hc, seed + 9, amp=0.5, lw=3)
        elif hair == "kofia":   # round embroidered cap
            shape(cr, rrect_pts(-hr + 4, hy - hr - 12, 2 * hr - 8, 30, 8, 12), hc, seed + 6, amp=0.6, lw=3.5)
            for k in range(4):
                dot(cr, -hr + 16 + k * (2 * hr - 32) / 3, hy - hr + 2, 3, GOLD)
        elif hair == "strawhat":
            blob(cr, 0, hy - 20, hr + 30, 9, hc, seed + 6, amp=0.8, lw=3.5)
            shape(cr, [(-hr + 6, hy - 22), (-hr + 12, hy - hr - 10), (hr - 12, hy - hr - 10), (hr - 6, hy - 22)], hc,
                  seed + 7, amp=0.8, lw=3.5)
            line(cr, [(-hr + 8, hy - 30), (hr - 8, hy - 30)], 5, hexc("#c0504d"), seed + 8, amp=0.3)
        elif hair == "slick" or who == "seth":
            # slick hair + side part
            shape(cr, [(-hr, hy - 4), (-hr + 4, hy - hr * 0.7), (-10, hy - hr - 6), (hr * 0.6, hy - hr - 2),
                       (hr + 2, hy - 12), (hr - 6, hy - 18), (-6, hy - hr + 12), (-hr + 10, hy - 14)],
                  INK, seed + 6, amp=0.7, lw=3)
        elif hair == "turban" or who == "ramu":
            shape(cr, [(-hr - 4, hy - 8), (-hr + 2, hy - hr - 6), (0, hy - hr - 20), (hr - 2, hy - hr - 6),
                       (hr + 4, hy - 8), (0, hy - 14)], TURBAN, seed + 6, amp=0.9, lw=3.5)
            line(cr, [(-hr + 6, hy - 24), (-4, hy - hr - 6), (hr - 8, hy - 30)], 3, WOOD_D, seed + 7, amp=0.6)
            line(cr, [(-hr + 12, hy - 12), (6, hy - hr + 4), (hr - 2, hy - 16)], 3, WOOD_D, seed + 8, amp=0.6)
        elif hair is None:
            shape(cr, [(-hr - 2, hy - 6), (-hr + 4, hy - hr - 2), (hr - 6, hy - hr - 2), (hr + 2, hy - 8)],
                  CAP_RED, seed + 6, amp=0.8, lw=3.5)
            shape(cr, rrect_pts(-hr - 26, hy - 16, 34, 12, 6, 12), CAP_RED, seed + 7, amp=0.5, lw=3.5)
        _eyes(cr, eyes, fx, hy + 2, t, seed, sun=(who == "seth" or c.get("shades", False)))
        if c.get("glasses"):
            for sx in (-1, 1):
                blob(cr, fx + sx * 15, hy + 2, 13, 12, hexc("#ffffff", 0.0), seed + 40 + sx, amp=0.4, lw=3,
                     stroke=INK)
            line(cr, [(fx - 3, hy + 1), (fx + 3, hy + 1)], 3, INK, seed + 42, amp=0.2)
        if c.get("lashes") and eyes in ("dot", "wide", "sly", "happy"):
            for sx in (-1, 1):
                line(cr, [(fx + sx * 15 + 5 * sx, hy - 6), (fx + sx * 15 + 10 * sx, hy - 11)], 2.5, INK, seed + sx, amp=0.2)
        if c.get("moustache"):
            line(cr, [(fx - 18, hy + 14), (fx - 6, hy + 10), (fx, hy + 13), (fx + 6, hy + 10), (fx + 18, hy + 14)], 4.5,
                 hexc("#5a3a22"), seed + 9, amp=0.4)
        if who in ("seth", "ramu"):
            # moustache
            mw = 22 if who == "seth" else 15
            line(cr, [(fx - mw, hy + 14), (fx - 8, hy + 10), (fx, hy + 13), (fx + 8, hy + 10), (fx + mw, hy + 14)],
                 5 if who == "seth" else 4, INK, seed + 9, amp=0.5)
        if eyes not in ("rupee",) and who != "seth" and c.get("blush", who in ("ramu", "chotu")):
            dot(cr, fx - 26, hy + 12, 6, BLUSH)
            dot(cr, fx + 26, hy + 12, 6, BLUSH)
        _mouth(cr, mouth, fx, hy + 24, seed + 10, t)
        if tears:
            for sx in (-1, 1):
                k = (t * 1.6 + (sx + 1) * 0.3) % 1
                blob(cr, fx + sx * 16, hy + 12 + k * 40, 5, 7, TEAR, seed + sx, amp=0.3, lw=2)
                line(cr, [(fx + sx * 16, hy + 6), (fx + sx * 18, hy + 34)], 5, hexc("#6cc4f0", 0.7), seed, amp=0.5)
        if sweat:
            k = (t * 0.8) % 1
            blob(cr, hr - 2, hy - 20 + k * 20, 6, 9, TEAR, seed + 3, amp=0.3, lw=2.5)
        # front arm
        sxf, syf = bw / 2 - 12, top + 26
        hf = HAND[arms[0]]
        hfx, hfy = sxf + hf[0], syf + hf[1]
        if arms[0] == "wave":
            hfx += math.sin(t * 12) * 10
        if arms[0] == "rub":
            hfx += math.sin(t * 16) * 5
        _arm(cr, sxf, syf, hfx, hfy, c["shirt"], skin)
        if arms[0] == "thumb":
            line(cr, [(hfx - 2, hfy - 6), (hfx - 1, hfy - 20)], 7, INK, seed, amp=0.3)
            line(cr, [(hfx - 2, hfy - 6), (hfx - 1, hfy - 19)], 3.5, skin, seed, amp=0.3)
        if facing < 0 and item:
            # keep text on props readable when the character faces left: un-mirror around the hand
            cr.translate(2 * hfx, 0)
            cr.scale(-1, 1)
        if item == "cash":
            cash(cr, hfx + 8, hfy - 6, 0.8)
        elif item == "cash_big":
            cash(cr, hfx + 18, hfy - 10, 1.3)
        elif item == "briefcase":
            briefcase(cr, hfx, hfy + 8)
        elif item == "phone":
            phone(cr, hfx + 4, hfy - 30, 0.2)
        elif item == "note5":
            dollar(cr, hfx + 16, hfy - 6, 0.7)
        elif item == "ticket":
            ticket(cr, hfx + 14, hfy - 10, 0.6)
        elif item == "mic":
            line(cr, [(hfx + 2, hfy), (hfx + 6, hfy - 30)], 7, INK, 0, amp=0.2)
            blob(cr, hfx + 7, hfy - 38, 11, 12, hexc("#8a8f96"), 0, amp=0.4, lw=3)
        elif item == "binoculars":
            binoculars(cr, hfx + 6, hfy - 8, 0.9)
    return


# ---------------------------------------------------------------- props
def pumpkin(cr, x, y, r=22, seed=0):
    """Pumpkin resting on (x, y)."""
    cy = y - r * 0.8
    blob(cr, x, cy, r * 1.15, r * 0.82, PUMPKIN, seed, amp=0.8, lw=3.5)
    for k in (-0.45, 0.45):
        line(cr, [(x + k * r * 0.5, cy - r * 0.75), (x + k * r * 1.1, cy), (x + k * r * 0.5, cy + r * 0.78)],
             2.5, PUMPKIN_D, seed + 1, amp=0.4)
    line(cr, [(x, cy - r * 0.78), (x + 2, cy - r * 1.15), (x + 7, cy - r * 1.25)], 5, STEM, seed + 2, amp=0.3)


# fixed layout of pumpkins stacked on the stall counter (dx, dy, r)
_STALL_PUMPKINS = [(-110, 0, 24), (-60, 0, 26), (-8, 0, 24), (44, 0, 26), (96, 0, 24),
                   (-84, -34, 22), (-34, -36, 24), (18, -34, 23), (70, -34, 22),
                   (-58, -66, 21), (-6, -68, 22), (46, -66, 21), (-32, -96, 20), (20, -96, 20)]


def stall(cr, x, y, stock=1.0, sign="KADDU MANDI"):
    """Village pumpkin stall; feet line at y. stock 0..1 controls pumpkins on the counter."""
    w = 320
    # back posts + awning
    for px in (x - w / 2 + 14, x + w / 2 - 14):
        sharp_shape(cr, [(px - 8, y - 280), (px + 8, y - 280), (px + 8, y - 60), (px - 8, y - 60)], WOOD_D,
                    seed=int(px), amp=0.8, lw=3.5)
    aw_y = y - 300
    stripes = 7
    sw = (w + 40) / stripes
    for i in range(stripes):
        x0 = x - w / 2 - 20 + i * sw
        col = RED if i % 2 == 0 else WHITE
        sharp_shape(cr, [(x0 + 6, aw_y - 40), (x0 + sw + 6, aw_y - 40), (x0 + sw, aw_y + 20), (x0, aw_y + 20)],
                    col, seed=90 + i, amp=0.8, lw=3)
    for i in range(stripes):
        x0 = x - w / 2 - 20 + i * sw
        col = RED if i % 2 == 0 else WHITE
        blob(cr, x0 + sw / 2, aw_y + 20, sw / 2, 12, col, seed=100 + i, amp=0.6, lw=3)
    # sign
    shape(cr, rrect_pts(x - 120, aw_y - 100, 240, 54, 10, 14), hexc("#3d8f45"), seed=77, amp=0.9)
    write(cr, [(sign, WHITE)], x, aw_y - 60, 34, align="center", bold=True)
    # counter pumpkins (drawn before counter front so they sit on top)
    top = y - 150
    n = round(stock * len(_STALL_PUMPKINS))
    for i, (dx, dy, r) in enumerate(_STALL_PUMPKINS[:n]):
        pumpkin(cr, x + dx, top + dy + 4, r, seed=200 + i)
    # counter
    sharp_shape(cr, [(x - w / 2, top), (x + w / 2, top), (x + w / 2 - 6, y - 4), (x - w / 2 + 6, y - 4)], WOOD,
                seed=55, amp=1.0, lw=4)
    for k in range(1, 4):
        line(cr, [(x - w / 2 + 8, top + k * 36), (x + w / 2 - 8, top + k * 36 + 2)], 3, WOOD_D, 60 + k, amp=0.8)
    shape(cr, rrect_pts(x - w / 2 - 10, top - 12, w + 20, 18, 6, 16), WOOD_D, seed=66, amp=0.8, lw=3.5)
    # price board
    board = [(x + 60, top + 26), (x + 140, top + 26), (x + 140, top + 86), (x + 60, top + 86)]
    sharp_shape(cr, board, hexc("#2f2a35"), seed=67, amp=0.6, lw=3)


def price_board(cr, x, y, txt, progress=1.0):
    """Chalk price on the stall's board (x, y = stall anchor)."""
    write(cr, [(txt, WHITE)], x + 100, y - 150 + 66, 30, progress, align="center")


def crate(cr, x, y, w=86, h=58, seed=0, full=True):
    """Wooden crate with pumpkins, bottom-centre at (x, y)."""
    if full:
        for i, dx in enumerate((-22, 4, 28)):
            pumpkin(cr, x + dx - 3, y - h + 12, 17, seed=seed + i)
    sharp_shape(cr, [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y)], hexc("#d9a15a"),
                seed=seed + 5, amp=0.8, lw=3.5)
    for k in (1, 2):
        line(cr, [(x - w / 2 + 4, y - h + k * h / 3), (x + w / 2 - 4, y - h + k * h / 3)], 3, WOOD_D, seed + k,
             amp=0.5)
    line(cr, [(x - w / 2 + 6, y - h + 4), (x + w / 2 - 6, y - 4)], 3, WOOD_D, seed + 8, amp=0.5)


def truck(cr, x, y, t, crates=0, wheel=0.0, facing=-1, driver=None, color=None):
    """Delivery truck; (x, y) = ground under the middle. facing -1 = cab on the left. color = (body, dark)."""
    TEAL, TEAL_D = color or (globals()["TEAL"], globals()["TEAL_D"])
    with at(cr, x, y, 1.0, flip=facing > 0):
        # bed
        bed_x0, bed_x1 = -40, 200
        # crates on bed
        slots = [(-5, 0), (85, 0), (165, 0), (40, 1), (125, 1)]
        for i, (cx, row) in enumerate(slots[:crates]):
            crate(cr, cx + 20, -80 - row * 56, 80, 56, seed=300 + i)
        sharp_shape(cr, [(bed_x0, -84), (bed_x1, -84), (bed_x1, -44), (bed_x0, -44)], TEAL, seed=1, amp=0.8, lw=4)
        line(cr, [(bed_x0 + 6, -64), (bed_x1 - 6, -64)], 3, TEAL_D, 2, amp=0.6)
        # cab
        shape(cr, poly_pts([(-190, -44), (-190, -120), (-160, -170), (-50, -170), (-40, -160), (-40, -44)], 16),
              TEAL, seed=3, amp=1.0)
        shape(cr, poly_pts([(-172, -118), (-150, -156), (-104, -156), (-104, -118)], 12), hexc("#bfe6ef"), seed=4,
              amp=0.7, lw=3.5)
        line(cr, [(-150, -128), (-128, -150)], 5, WHITE, 5, amp=0.3)
        shape(cr, poly_pts([(-94, -156), (-54, -156), (-54, -118), (-94, -118)], 12), hexc("#bfe6ef"), seed=6,
              amp=0.7, lw=3.5)
        if driver:
            blob(cr, -74, -128, 14, 14, driver, seed=8, amp=0.5, lw=3)
        line(cr, [(-80, -100), (-64, -100)], 4, INK, 7, amp=0.3)
        sharp_shape(cr, [(-196, -72), (-184, -72), (-184, -50), (-196, -50)], hexc("#ffe28a"), seed=9, amp=0.4,
                    lw=3)
        sharp_shape(cr, [(-200, -48), (-36, -48), (-36, -32), (-200, -32)], hexc("#9aa3a8"), seed=10, amp=0.6,
                    lw=3.5)
        # wheels
        for wx in (-140, 130):
            blob(cr, wx, -26, 28, 28, TYRE, seed=wx, amp=0.6, lw=4)
            blob(cr, wx, -26, 12, 12, hexc("#a9a2ae"), seed=wx + 1, amp=0.4, lw=3)
            for k in range(3):
                a = wheel + k * 2 * math.pi / 3
                line(cr, [(wx, -26), (wx + 12 * math.cos(a), -26 + 12 * math.sin(a))], 3, INK, wx + k, amp=0)


def exhaust(cr, x, y, t, strength=1.0):
    for i in range(3):
        k = (t * 1.8 + i / 3) % 1
        r = 6 + k * 16
        a = (1 - k) * 0.7 * strength
        blob(cr, x + k * 60, y - k * 30, r, r * 0.8, hexc("#d8d3c4", a), seed=400 + i, amp=0.8, lw=2.5,
             stroke=hexc("#2a2230", a))


def bubble(cr, x, y, w, h, tail, runs, s=1.0, size=30, thought=False, progress=1.0, lines=None):
    """Speech bubble centred at (x, y); tail = point it aims at. s = pop scale."""
    if s <= 0:
        return
    with at(cr, x, y, s):
        tx, ty = (tail[0] - x) / s, (tail[1] - y) / s
        if thought:
            shape(cr, _cloud(w, h), WHITE, seed=500, amp=1.0, lw=3.5)
            for i, k in enumerate((0.55, 0.75, 0.9)):
                r = 12 - i * 3.5
                blob(cr, tx * k, ty * k, r, r, WHITE, seed=510 + i, amp=0.4, lw=3)
        else:
            pts = rrect_pts(-w / 2, -h / 2, w, h, 26, 18)
            # splice a tail in toward the target
            import math as _m
            best = min(range(len(pts)), key=lambda i: _m.hypot(pts[i][0] - tx, pts[i][1] - ty))
            ang = _m.atan2(ty, tx)
            base = pts[best]
            pa = (base[0] - 16 * _m.sin(ang), base[1] + 16 * _m.cos(ang))
            pb = (base[0] + 16 * _m.sin(ang), base[1] - 16 * _m.cos(ang))
            tip = (base[0] + (tx - base[0]) * 0.55, base[1] + (ty - base[1]) * 0.55)
            pts = pts[:best] + [pa, tip, pb] + pts[best + 1:]
            shape(cr, pts, WHITE, seed=520, amp=0.9, lw=3.5)
        ls = lines or [runs]
        lh = size * 1.15
        y0 = -(len(ls) - 1) * lh / 2 + size * 0.35
        per = 1 / len(ls)
        for i, r in enumerate(ls):
            p = (progress - i * per) / per
            write(cr, r, 0, y0 + i * lh, size, p, align="center")


def _cloud(w, h):
    pts = []
    n = 12
    for i in range(n * 3):
        a = 2 * math.pi * i / (n * 3)
        bump = abs(math.sin(a * n / 2)) * 10
        pts.append(((w / 2 + bump) * math.cos(a), (h / 2 + bump) * math.sin(a)))
    return pts


def money_pile(cr, x, y, s=1.0, seed=600):
    with at(cr, x, y, s):
        shape(cr, [(-150, 0), (-110, -60), (-60, -110), (0, -140), (60, -112), (115, -58), (150, 0)], CASH,
              seed=seed, amp=1.5, lw=4)
        for i in range(10):
            dx = ((i * 53) % 220) - 110
            dy = -((i * 37) % 100) - 12
            if abs(dx) < 140 - (-dy) * 0.9:
                write(cr, [("₹", CASH_D)], dx, dy, 24, bold=True, align="center")
        for i, dx in enumerate((-120, -60, 70, 128)):
            cash(cr, dx, -6, 0.7, seed=seed + i, rot=0.2 * (i % 2 * 2 - 1))


# ---------------------------------------------------------------- props for "The $5 Lucky Charm"
DOLLAR = hexc("#8cc084")
DOLLAR_D = hexc("#4f7d4a")


def dollar(cr, x, y, s=1.0, amount="$5", rot=-0.12, seed=5):
    with at(cr, x, y, s, rot):
        sharp_shape(cr, [(-44, -22), (44, -22), (44, 22), (-44, 22)], DOLLAR, seed=seed, amp=0.8, lw=3.5)
        blob(cr, 0, 0, 14, 16, hexc("#cfe6c6"), seed=seed + 1, amp=0.4, lw=2.5)
        write(cr, [(amount, DOLLAR_D)], -28, 10, 22, align="center", bold=True)
        write(cr, [(amount, DOLLAR_D)], 30, 10, 22, align="center", bold=True)


def phone(cr, x, y, s=1.0, screen=None, seed=8):
    """Phone centred at (x, y); `screen(cr)` draws into a 180x320 screen box centred on the origin."""
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-110, -190, 220, 380, 30, 20), INK, seed=seed, amp=0.6, lw=4)
        shape(cr, rrect_pts(-96, -168, 192, 336, 16, 20), hexc("#dfe9f2"), seed=seed + 1, amp=0.4, lw=0, stroke=None)
        if screen:
            cr.save()
            cr.rectangle(-96, -168, 192, 336)
            cr.clip()
            screen(cr)
            cr.restore()
        dot(cr, 0, -178, 4, hexc("#555555"))


def ticket(cr, x, y, s=1.0, nums="07 13 21 34 42", seed=9):
    with at(cr, x, y, s, rot=-0.08):
        sharp_shape(cr, [(-80, -44), (80, -44), (80, 44), (-80, 44)], hexc("#fff3c4"), seed=seed, amp=0.8, lw=3.5)
        sharp_shape(cr, [(-80, -44), (80, -44), (80, -18), (-80, -18)], hexc("#e0483f"), seed=seed + 1, amp=0.6, lw=3)
        write(cr, [("LOTTO", WHITE)], 0, -24, 24, align="center", bold=True)
        write(cr, [(nums, INK)], 0, 20, 22, align="center", bold=True)


def binoculars(cr, x, y, s=1.0, seed=10):
    with at(cr, x, y, s):
        for dx in (-17, 17):
            shape(cr, rrect_pts(dx - 14, -22, 28, 44, 10, 12), hexc("#3a3140"), seed=seed + dx, amp=0.5, lw=3.5)
            blob(cr, dx, -20, 11, 6, hexc("#9fd3f0"), seed=seed + dx + 1, amp=0.3, lw=2.5)
        sharp_shape(cr, [(-4, -8), (4, -8), (4, 8), (-4, 8)], hexc("#3a3140"), seed=seed, amp=0.3, lw=2.5)
