"""Shots for videos/snakebite.py: every drawing here is our own (horse, the Big Four snakes, venom, antibodies,
the body's nerves, props). Layout: header + headline at the top (motion.paper), content between y = 380 and 1080."""
import math

import numpy as np

from motion import paper as P
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg, smooth
from motion.paper import (INK, RED, Shot, appear, circle_mark, curve, fill, flip_counter, place, poly, polaroid,
                          rrect, shade, slide, stamp, stopwatch, stroke, text, tick, red_x, vial, with_shadow)

BROWN = hexc("#8b5a34")
MANE = hexc("#3a2417")
VENOM = hexc("#e2a23a")
ANTI = hexc("#e9eef2")
CELL = hexc("#c8322d")
CREAM = hexc("#efe6d2")
BONE = hexc("#f2ead8")


# ================================================================ the horse
def horse(cr, x, y, s=1.0, flip=False, badge=0.0, look=0.0):
    """A standing horse, side view, facing right (x, y = between the hooves on the ground)."""
    def legs(c, col, xs):
        for x0, hind in xs:
            if hind:
                pts = [(x0 - 14, -170), (x0 + 16, -170), (x0 + 6, -92), (x0 + 2, -70), (x0 + 6, -14), (x0 - 10, -14),
                       (x0 - 12, -66), (x0 - 20, -96)]
            else:
                pts = [(x0 - 14, -160), (x0 + 13, -160), (x0 + 9, -84), (x0 + 7, -14), (x0 - 8, -14), (x0 - 10, -84)]
            curve(c, pts, close=True)
            fill(c, col)
            rrect(c, x0 - 11 + (2 if hind else 0), -18, 21, 18, 4)
            fill(c, hexc("#2a2420"))

    def body(c):
        legs(c, shade(BROWN, 0.72), [(-108, True), (100, False)])     # far legs
        # tail
        curve(c, [(-148, -246), (-178, -230), (-196, -180), (-192, -120), (-176, -96), (-170, -140), (-166, -190),
                  (-150, -226)], close=True)
        fill(c, MANE)
        sil = [(95, -140), (124, -168), (140, -214), (162, -262), (188, -283), (226, -279), (242, -298),
               (234, -320), (202, -350), (186, -366), (166, -364), (138, -340), (104, -290), (70, -262), (10, -252),
               (-60, -255), (-112, -262), (-142, -246), (-156, -214), (-152, -178), (-134, -150), (-110, -138),
               (-60, -130), (20, -128), (70, -133)]
        curve(c, sil, close=True)
        c.set_source(P.lin_grad(0, -360, 0, -120, [(0, shade(BROWN, 1.12)), (0.6, BROWN), (1, shade(BROWN, 0.78))]))
        c.fill()
        # ears
        poly(c, [(182, -362), (178, -398), (166, -366)])
        fill(c, shade(BROWN, 0.85))
        # mane
        curve(c, [(170, -368), (150, -352), (120, -322), (90, -286), (66, -262), (80, -282), (108, -316), (140, -350),
                  (164, -372)], close=True)
        fill(c, MANE)
        for k in range(7):
            u = k / 6
            mx, my = lerp(162, 72, u), lerp(-366, -266, u)
            c.move_to(mx, my)
            c.line_to(mx - 16, my + 22)
            stroke(c, MANE, 5)
        # muzzle shade, eye, nostril, mouth
        c.arc(222, -294, 22, 0, 6.3)
        fill(c, shade(BROWN, 0.75), 0.5)
        c.arc(196, -330, 5.5, 0, 6.3)
        fill(c, hexc("#1a1210"))
        c.arc(197.5, -331.5, 1.8, 0, 6.3)
        fill(c, (1, 1, 1), 0.8)
        c.arc(234, -300, 4, 0, 6.3)
        fill(c, hexc("#2a1810"))
        c.move_to(222, -282)
        c.line_to(236, -284)
        stroke(c, hexc("#2a1810"), 2)
        legs(c, BROWN, [(-126, True), (82, False)])                    # near legs
        # muscle lines
        c.move_to(-120, -238)
        c.curve_to(-100, -200, -110, -170, -118, -150)
        stroke(c, shade(BROWN, 0.7), 2, 0.6)
        c.move_to(96, -236)
        c.curve_to(110, -200, 104, -170, 92, -150)
        stroke(c, shade(BROWN, 0.7), 2, 0.6)
        if badge > 0:
            with place(c, -10, -200, badge):
                c.arc(0, 0, 34, 0, 6.3)
                fill(c, hexc("#f7f2e6"))
                c.arc(0, 0, 34, 0, 6.3)
                stroke(c, RED, 4)
                c.rectangle(-8, -22, 16, 44)
                c.rectangle(-22, -8, 44, 16)
                fill(c, RED)

    with place(cr, x, y, s):
        if flip:
            cr.scale(-1, 1)
        with_shadow(cr, body, 10, 6, 0.28)


# ================================================================ snakes
def _tube(spine, w0, w1):
    """Left/right outline points of a tube along `spine`, width tapering from w0 (head end) to w1 (tail)."""
    n = len(spine)
    L, R, N = [], [], []
    for i, (x, y) in enumerate(spine):
        a = spine[max(0, i - 1)]
        b = spine[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = lerp(w0, w1, (i / (n - 1)) ** 1.6) / 2
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
        N.append((nx, ny, w))
    return L, R, N


def _spine(fn, n=60):
    return [fn(i / (n - 1)) for i in range(n)]


def snake(cr, spine, w0=34, w1=4, body=None, belly=None, pattern="plain", head=True, tongue=0.0, pat_col=None):
    """A snake along `spine` (head first). Patterns: plain, bands (krait), chain (Russell's viper),
    saw (saw-scaled viper)."""
    body = body or hexc("#5a4632")
    L, R, N = _tube(spine, w0, w1)
    pat_col = pat_col or hexc("#f3efe4")

    def draw(c):
        poly(c, L + R[::-1])
        fill(c, body)
        poly(c, L + R[::-1])
        c.save()
        c.clip()
        n = len(spine)
        # belly shade along the right edge
        for i in range(n - 1):
            nx, ny, w = N[i]
            x, y = spine[i]
            c.move_to(x - nx * w * 0.7, y - ny * w * 0.7)
            x2, y2 = spine[i + 1]
            c.line_to(x2 - nx * w * 0.7, y2 - ny * w * 0.7)
            stroke(c, shade(body, 0.6), w * 0.7, 0.6)
        if pattern == "bands":
            for i in range(4, n - 2, 4):
                q = [L[i], L[i + 1], R[i + 1], R[i]]
                poly(c, q)
                fill(c, pat_col)
        elif pattern == "chain":
            for i in range(5, n - 3, 5):
                x, y = spine[i]
                nx, ny, w = N[i]
                ang = math.atan2(nx, -ny)
                for off in (0, 0.62, -0.62):
                    cx, cy = x + nx * w * off, y + ny * w * off
                    rr = w * (0.55 if off == 0 else 0.32)
                    with place(c, cx, cy, 1, ang):
                        c.save()
                        c.scale(1.25, 1)
                        c.arc(0, 0, rr * 1.18, 0, 6.3)
                        fill(c, hexc("#efe2c0"))
                        c.arc(0, 0, rr, 0, 6.3)
                        fill(c, hexc("#4a2a18"))
                        c.restore()
        elif pattern == "saw":
            pts = []
            for i in range(2, n - 2, 2):
                x, y = spine[i]
                nx, ny, w = N[i]
                k = 0.55 if (i // 2) % 2 else -0.55
                pts.append((x + nx * w * k, y + ny * w * k))
            c.move_to(*pts[0])
            for p in pts[1:]:
                c.line_to(*p)
            stroke(c, hexc("#f1e8d2"), 3.5)
            for i in range(4, n - 3, 6):
                x, y = spine[i]
                c.arc(x, y, N[i][2] * 0.35, 0, 6.3)
                fill(c, hexc("#3a2a1c"))
        # sheen
        for i in range(n - 1):
            nx, ny, w = N[i]
            x, y = spine[i]
            x2, y2 = spine[i + 1]
            c.move_to(x + nx * w * 0.45, y + ny * w * 0.45)
            c.line_to(x2 + nx * w * 0.45, y2 + ny * w * 0.45)
            stroke(c, (1, 1, 1), max(1.0, w * 0.18), 0.12)
        c.restore()
        if head:
            (x, y), (x2, y2) = spine[0], spine[3]
            ang = math.atan2(y - y2, x - x2)
            with place(c, x, y, w0 / 34, ang):
                curve(c, [(-14, -17), (14, -16), (34, -9), (40, 0), (34, 9), (14, 16), (-14, 17)], close=True)
                fill(c, shade(body, 1.05))
                c.arc(22, -9, 4.2, 0, 6.3)
                fill(c, hexc("#120d0a"))
                c.arc(23, -10, 1.4, 0, 6.3)
                fill(c, (1, 1, 1), 0.8)
                if tongue > 0:
                    c.move_to(40, 0)
                    c.line_to(40 + 22 * tongue, 0)
                    c.line_to(40 + 30 * tongue, -6 * tongue)
                    c.move_to(40 + 22 * tongue, 0)
                    c.line_to(40 + 30 * tongue, 6 * tongue)
                    stroke(c, hexc("#c4302b"), 2.4)
    with_shadow(cr, draw, 6, 9, 0.3)


def wavy(x0, y0, length, amp, waves, phase=0.0, n=70):
    """A horizontal S-curve spine, head at the right end (x0 + length)."""
    return _spine(lambda u: (x0 + length * (1 - u), y0 + amp * math.sin(2 * math.pi * waves * u + phase) *
                             (0.4 + 0.6 * u)), n)


def cobra(cr, x, y, s=1.0, t=0.0, hood=1.0):
    """A cobra reared up with its hood spread, facing the viewer (x, y = where the coils sit)."""
    body = hexc("#3b2f26")
    with place(cr, x, y, s):
        # coils on the ground
        coil = _spine(lambda u: (math.cos(u * 4.2 * math.pi) * lerp(30, 150, u),
                                 30 + math.sin(u * 4.2 * math.pi) * lerp(12, 46, u)), 90)
        snake(cr, coil, 52, 6, body, head=False)
        # raised neck
        sway = 8 * math.sin(t * 2.2)
        neck = [(sway * 0.6, -330), (sway * 0.5, -260), (sway * 0.3, -180), (8, -100), (12, -30), (0, 20)]
        neck = _spine(lambda u: _bez(neck, u), 30)
        def draw(c):
            L, R, _ = _tube(neck, 66, 72)
            poly(c, L + R[::-1])
            fill(c, body)
            # hood
            hw = 92 * hood + 30
            curve(c, [(sway * 0.6, -400), (sway * 0.6 + hw * 0.62, -372), (sway * 0.5 + hw, -300),
                      (sway * 0.4 + hw * 0.78, -220), (sway * 0.3 + 30, -170), (sway * 0.3 - 30, -170),
                      (sway * 0.4 - hw * 0.78, -220), (sway * 0.5 - hw, -300), (sway * 0.6 - hw * 0.62, -372)],
                  close=True)
            c.set_source(P.rad_grad(sway * 0.5, -300, 10, hw, [(0, hexc("#7a6246")), (0.7, hexc("#4a3a2a")),
                                                               (1, hexc("#2e241c"))]))
            c.fill()
            curve(c, [(sway * 0.6 - 26, -380), (sway * 0.6 + 26, -380), (sway * 0.45 + 30, -240),
                      (sway * 0.35 + 24, -170), (sway * 0.35 - 24, -170), (sway * 0.45 - 30, -240)], close=True)
            fill(c, hexc("#b39a74"))
            # throat bands (front view)
            for k, yy in enumerate((-250, -228)):
                rrect(c, sway * 0.45 - 28, yy, 56, 10, 5)
                fill(c, hexc("#1a1410"), 0.8)
            # ventral scales
            for yy in range(-300, -170, 12):
                c.move_to(sway * 0.45 - 22, yy)
                c.line_to(sway * 0.45 + 22, yy)
                stroke(c, hexc("#c9b48c"), 1.6, 0.45)
            # head
            hx, hy = sway * 0.62, -410
            curve(c, [(hx - 30, hy + 10), (hx - 26, hy - 18), (hx, hy - 30), (hx + 26, hy - 18), (hx + 30, hy + 10),
                      (hx + 14, hy + 30), (hx - 14, hy + 30)], close=True)
            fill(c, shade(body, 1.15))
            for ex in (-14, 14):
                c.arc(hx + ex, hy - 4, 5, 0, 6.3)
                fill(c, hexc("#0e0a08"))
                c.arc(hx + ex + 1, hy - 5, 1.6, 0, 6.3)
                fill(c, (1, 1, 1), 0.85)
            tl_ = 0.5 + 0.5 * math.sin(t * 9)
            if tl_ > 0.3:
                c.move_to(hx, hy + 28)
                c.line_to(hx, hy + 28 + 22 * tl_)
                c.line_to(hx - 6, hy + 36 + 22 * tl_)
                c.move_to(hx, hy + 28 + 22 * tl_)
                c.line_to(hx + 6, hy + 36 + 22 * tl_)
                stroke(c, hexc("#c4302b"), 2.6)
        with_shadow(cr, draw, 8, 10, 0.3)


def _bez(pts, u):
    """Point on a Catmull-Rom chain through pts at parameter u in [0, 1]."""
    n = len(pts) - 1
    f = u * n
    i = min(int(f), n - 1)
    s = f - i
    p0, p1, p2 = pts[max(0, i - 1)], pts[i], pts[i + 1]
    p3 = pts[min(n, i + 2)]
    return tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * s + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * s * s +
                        (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * s ** 3) for k in range(2))


BIG_FOUR = [   # name, body colour, pattern, pattern colour
    ("COBRA", hexc("#4a3a2c"), "plain", None),
    ("COMMON KRAIT", hexc("#1f1d22"), "bands", hexc("#eeeae0")),
    ("RUSSELL'S VIPER", hexc("#9a7448"), "chain", None),
    ("SAW-SCALED VIPER", hexc("#a98b62"), "saw", None),
]


def snake_card(cr, x, y, k, t=0.0, rot=0.0, s=1.0):
    name, body, pattern, pc = BIG_FOUR[k]
    with place(cr, x, y, s, rot):
        def c_(c):
            P.card(c, -150, -110, 300, 220, hexc("#ece3cb"))
            c.rectangle(-150, -110, 300, 220)
            stroke(c, hexc("#b9ab88"), 2)
        with_shadow(cr, c_, 5, 8, 0.3)
        sp = wavy(-118, -10, 236, 26, 1.3, phase=t * 1.5 + k)
        snake(cr, sp, 26 if k != 3 else 22, 3, body, pattern=pattern, pat_col=pc)
        sz = P.fit(cr, name, 30, 270)
        text(cr, name, 0, 92, sz, INK, align="center")
        P.clothes_pin(cr, 0, -112)


# ================================================================ small props
def torn_hole(cr, x, y, rx, ry, seed=3):
    """A hole torn through the page (dark inside, curled paper flaps around the edge)."""
    r = np.random.default_rng(seed)
    n = 26
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = r.uniform(0.82, 1.08)
        pts.append((x + rx * k * math.cos(a), y + ry * k * math.sin(a)))
    poly(cr, pts)
    fill(cr, hexc("#16120f"))
    for i in range(0, n, 2):
        a = 2 * math.pi * i / n
        p, q = pts[i], pts[(i + 1) % n]
        tip = (x + rx * r.uniform(0.8, 0.9) * math.cos(a + 0.12), y + ry * r.uniform(0.8, 0.9) * math.sin(a + 0.12))
        poly(cr, [p, q, tip])
        fill(cr, hexc("#e4dbc3"))
        poly(cr, [p, q, tip])
        stroke(cr, hexc("#a89a7a"), 1.2, 0.8)


def flask(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-22, -120), (22, -120), (22, -60), (80, 40), (-80, 40), (-22, -60)])
            c.set_source(P.lin_grad(-80, 0, 80, 0, [(0, (0.82, 0.86, 0.86, 0.95)), (0.5, (0.97, 0.98, 0.98, 0.95)),
                                                    (1, (0.72, 0.76, 0.76, 0.95))]))
            c.fill()
            poly(c, [(-52, -10), (52, -10), (80, 40), (-80, 40)])
            fill(c, hexc("#5fae8e"), 0.85)
            rrect(c, -28, -132, 56, 16, 4)
            fill(c, hexc("#b9b2a2"))
        with_shadow(cr, d, 5, 8, 0.3)


def factory(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-110, 40), (-110, -40), (-60, -10), (-60, -40), (-10, -10), (-10, -40), (40, -10), (40, -120),
                     (70, -120), (70, -10), (110, -10), (110, 40)])
            fill(c, hexc("#8b8378"))
            for wx in (-90, -45, 0, 55):
                c.rectangle(wx, 0, 24, 18)
                fill(c, hexc("#f2d27a"))
            for k in range(3):
                c.arc(60 + k * 18, -140 - k * 26, 16 + k * 6, 0, 6.3)
                fill(c, hexc("#cfc8bb"), 0.8)
        with_shadow(cr, d, 5, 8, 0.3)


def syringe(cr, x, y, s=1.0, rot=0.0, push=0.0, liquid=None):
    """A syringe pointing left; `push` 0..1 empties it."""
    liquid = liquid or VENOM
    with place(cr, x, y, s, rot):
        def d(c):
            c.move_to(-180, 0)
            c.line_to(-96, 0)
            stroke(c, hexc("#9aa0a3"), 3)
            rrect(c, -100, -8, 14, 16, 2)
            fill(c, hexc("#c9cccc"))
            rrect(c, -86, -24, 190, 48, 6)
            c.set_source(P.lin_grad(0, -24, 0, 24, [(0, (0.95, 0.97, 0.97, 0.9)), (0.5, (1, 1, 1, 0.75)),
                                                    (1, (0.8, 0.83, 0.83, 0.9))]))
            c.fill()
            lw_ = 180 * (1 - push)
            if lw_ > 1:
                c.rectangle(-82, -20, lw_, 40)
                fill(c, liquid, 0.85)
            for k in range(8):
                c.move_to(-60 + k * 20, -24)
                c.line_to(-60 + k * 20, -12)
                stroke(c, INK, 1.4, 0.6)
            px = -82 + lw_
            c.rectangle(px, -22, 8, 44)
            fill(c, hexc("#3a3a3a"))
            c.rectangle(px + 8, -6, 150, 12)
            fill(c, hexc("#d8d8d8"))
            rrect(c, px + 150, -30, 14, 60, 4)
            fill(c, hexc("#bdbdbd"))
            rrect(c, 104, -36, 12, 72, 3)
            fill(c, hexc("#bdbdbd"))
        with_shadow(cr, d, 5, 8, 0.3)


def gauge(cr, x, y, r, val, label="DOSE"):
    """A dial with a green SAFE zone at the low end; needle at `val` (0..1)."""
    def d(c):
        c.arc(x, y, r + 18, math.pi, 2 * math.pi)
        c.line_to(x + r + 18, y + 26)
        c.line_to(x - r - 18, y + 26)
        c.close_path()
        fill(c, hexc("#efe7d3"))
        for a0, a1, col in ((math.pi, math.pi * 1.33, hexc("#3f9a5c")), (math.pi * 1.33, math.pi * 1.66,
                                                                          hexc("#e2b23c")),
                            (math.pi * 1.66, 2 * math.pi, RED)):
            c.arc(x, y, r, a0, a1)
            stroke(c, col, 26)
        text(c, "SAFE", x - r * 0.62, y - r * 0.32, 24, hexc("#2f7a48"), align="center")
        text(c, label, x, y + 18, 18, INK, P.FONT_MONO, align="center", spacing=2)
        a = math.pi + math.pi * val
        c.move_to(x, y)
        c.line_to(x + r * 0.86 * math.cos(a), y + r * 0.86 * math.sin(a))
        stroke(c, INK, 6)
        c.arc(x, y, 12, 0, 6.3)
        fill(c, INK)
    with_shadow(cr, d, 5, 8, 0.25)


def venom_blob(cr, x, y, r=14, a=1.0, grey=0.0):
    col = tuple(lerp(VENOM[k], 0.55, grey) for k in range(3))
    for k in range(6):
        ang = k * math.pi / 3
        cr.arc(x + r * 0.55 * math.cos(ang), y + r * 0.55 * math.sin(ang), r * 0.5, 0, 6.3)
        fill(cr, col, a)
    cr.arc(x, y, r * 0.55, 0, 6.3)
    fill(cr, shade(col, 0.8), a)


def antibody(cr, x, y, s=1.0, rot=0.0, a=1.0, col=None):
    """A Y-shaped antibody."""
    col = col or ANTI
    with place(cr, x, y, s, rot):
        for pts in (((0, 26), (0, 0)), ((0, 0), (-17, -20)), ((0, 0), (17, -20))):
            cr.move_to(*pts[0])
            cr.line_to(*pts[1])
            stroke(cr, shade(col, 0.6), 12, a)
            cr.move_to(*pts[0])
            cr.line_to(*pts[1])
            stroke(cr, col, 8, a)
        for ex in (-17, 17):
            cr.arc(ex, -20, 5, 0, 6.3)
            fill(cr, hexc("#7fb6e0"), a)


def red_cell(cr, x, y, r=26, rot=0.0, a=1.0):
    with place(cr, x, y, 1, rot):
        cr.save()
        cr.scale(1, 0.82)
        cr.arc(0, 0, r, 0, 6.3)
        cr.set_source(P.rad_grad(0, 0, r * 0.2, r, [(0, shade(CELL, 0.72)), (0.55, shade(CELL, 1.0)),
                                                     (1, shade(CELL, 0.85))]))
        cr.fill()
        cr.restore()


def blood_drop(cr, x, y, r, col=None):
    col = col or CELL
    cr.move_to(x, y - r * 1.9)
    cr.curve_to(x + r * 0.4, y - r * 1.1, x + r, y - r * 0.6, x + r, y)
    cr.arc(x, y, r, 0, math.pi)
    cr.curve_to(x - r, y - r * 0.6, x - r * 0.4, y - r * 1.1, x, y - r * 1.9)
    fill(cr, col)
    cr.arc(x - r * 0.35, y - r * 0.15, r * 0.22, 0, 6.3)
    fill(cr, (1, 1, 1), 0.35)


def paper_person_head(cr, x, y, r, lid=0.0, t=0.0):
    """A paper cut-out head (cream card) with eyes; `lid` 0..1 droops the eyelids."""
    def d(c):
        c.arc(x, y, r, 0, 6.3)
        fill(c, hexc("#f1e6cc"))
        c.rectangle(x - r * 0.35, y + r * 0.85, r * 0.7, r * 0.5)
        fill(c, hexc("#f1e6cc"))
        for ex in (-0.38, 0.38):
            ox, oy = x + ex * r, y - r * 0.05
            c.save()
            c.scale(1, 1)
            c.arc(ox, oy, r * 0.17, 0, 6.3)
            fill(c, hexc("#ffffff"))
            c.arc(ox, oy + r * 0.02, r * 0.08, 0, 6.3)
            fill(c, hexc("#2b2420"))
            if lid > 0:   # eyelid comes down over the top of the eye
                c.save()
                c.arc(ox, oy, r * 0.175, 0, 6.3)
                c.clip()
                c.rectangle(ox - r * 0.2, oy - r * 0.2, r * 0.4, r * 0.4 * lid * 0.85)
                fill(c, hexc("#e2c9a2"))
                c.move_to(ox - r * 0.2, oy - r * 0.2 + r * 0.4 * lid * 0.85)
                c.line_to(ox + r * 0.2, oy - r * 0.2 + r * 0.4 * lid * 0.85)
                stroke(c, hexc("#8a6a4a"), 3)
                c.restore()
            c.arc(ox, oy, r * 0.17, 0, 6.3)
            stroke(c, hexc("#8a6a4a"), 2.5)
            c.restore()
        c.move_to(x - r * 0.18, y + r * 0.45)
        c.curve_to(x - r * 0.05, y + r * 0.5 - 8 * lid, x + r * 0.05, y + r * 0.5 - 8 * lid, x + r * 0.18, y + r * 0.45)
        stroke(c, hexc("#8a6a4a"), 3)
    with_shadow(cr, d, 6, 9, 0.3)


def lungs(cr, x, y, s=1.0, breath=0.0, col=None, dead=0.0):
    """Lungs + windpipe + diaphragm in white engraving lines (for a dark board)."""
    col = col or BONE
    k = 1 + 0.06 * breath
    with place(cr, x, y, s):
        cr.move_to(0, -220)
        cr.line_to(0, -120)
        stroke(cr, col, 10)
        for i in range(-200, -125, 14):
            cr.move_to(-9, i)
            cr.line_to(9, i)
            stroke(cr, hexc("#2a2724"), 2)
        for sd in (-1, 1):
            cr.move_to(0, -120)
            cr.line_to(sd * 50, -80)
            stroke(cr, col, 7)
            with place(cr, sd * 92, -40, k):
                curve(cr, [(sd * -30, -120), (sd * 20, -125), (sd * 70, -60), (sd * 82, 40), (sd * 60, 110),
                           (sd * -20, 100), (sd * -48, 40), (sd * -42, -40)], close=True)
                cr.set_source_rgba(*col[:3], 0.12 + 0.08 * breath)
                cr.fill_preserve()
                stroke(cr, col, 3)
                for j in range(9):   # hatching
                    yy = -90 + j * 22
                    cr.move_to(sd * -30, yy)
                    cr.line_to(sd * 60, yy + 14)
                    stroke(cr, col, 1, 0.35)
        dy = 6 * breath
        cr.move_to(-200, 120 + dy)
        cr.curve_to(-120, 40 + dy, 120, 40 + dy, 200, 120 + dy)
        stroke(cr, hexc("#d8806a") if dead < 0.5 else hexc("#8a7a70"), 6)
        text(cr, "DIAPHRAGM", 0, 160, 18, col, P.FONT_MONO, align="center", spacing=2, alpha=0.8)


# ================================================================ the body's wiring (dark board, white engraving)
BODY_R = [(0, -470), (40, -462), (58, -430), (60, -392), (46, -360), (30, -344), (30, -322), (80, -306),
          (118, -292), (134, -260), (142, -180), (154, -100), (170, -20), (178, 30), (164, 36), (148, -16),
          (128, -96), (114, -170), (106, -220), (102, -130), (98, -40), (96, 30), (88, 130), (84, 240),
          (82, 330), (92, 380), (60, 384), (50, 330), (40, 240), (28, 130), (12, 40), (0, 30)]


def body_outline(cr, x, y, s=1.0, col=None, lw=3):
    col = col or BONE
    pts = BODY_R + [(-px, py) for px, py in BODY_R[::-1]]
    with place(cr, x, y, s):
        curve(cr, pts, close=True)
        cr.set_source_rgba(*col[:3], 0.05)
        cr.fill_preserve()
        stroke(cr, col, lw / s)


NERVES = {   # polylines in body coordinates
    "spine": [(0, -360), (0, -250), (0, -150), (0, -60), (0, 20)],
    "arm": [(0, -300), (60, -290), (110, -250), (124, -170), (138, -90), (156, -10), (166, 26)],
    "arm_l": [(0, -300), (-60, -290), (-110, -250), (-124, -170), (-138, -90), (-156, -10), (-166, 26)],
    "dia": [(0, -320), (20, -290), (34, -240), (40, -190), (60, -150), (90, -140)],
    "dia_l": [(0, -320), (-20, -290), (-34, -240), (-40, -190), (-60, -150), (-90, -140)],
    "leg": [(0, 20), (34, 60), (56, 140), (64, 240), (70, 340)],
    "leg_l": [(0, 20), (-34, 60), (-56, 140), (-64, 240), (-70, 340)],
}


def nervous_system(cr, x, y, s, t, sparks=(), dim=0.0, col=None):
    """Brain, spinal cord and nerves (white), with travelling sparks: [(nerve, t_start, dur)]."""
    col = col or BONE
    with place(cr, x, y, s):
        cr.save()
        cr.translate(0, -410)
        cr.scale(1, 0.82)
        cr.arc(0, 0, 44, 0, 6.3)
        cr.restore()
        cr.set_source_rgba(*hexc("#e8a090")[:3], 0.55)
        cr.fill_preserve()
        stroke(cr, col, 2.5 / s)
        for k in range(5):   # brain folds
            cr.move_to(-34 + k * 16, -440)
            cr.curve_to(-40 + k * 16, -420, -26 + k * 16, -400, -32 + k * 16, -380)
            stroke(cr, col, 1.4 / s, 0.6)
        for name, pts in NERVES.items():
            curve(cr, pts)
            stroke(cr, hexc("#f2c75c"), (6 if name == "spine" else 3.2) / s, 0.85 - 0.5 * dim)
        for name, t0, dur in sparks:
            if t0 <= t < t0 + dur + 0.25:
                u = seg(t, t0, t0 + dur)
                pts = NERVES[name]
                px, py = _bez(pts, min(u, 1))
                a = 1 - seg(t, t0 + dur, t0 + dur + 0.25)
                cr.arc(px, py, 26 / s, 0, 6.3)
                cr.set_source(P.rad_grad(px, py, 0, 26 / s, [(0, (1, 0.97, 0.7, 0.95 * a)), (1, (1, 0.8, 0.3, 0))]))
                cr.fill()
                cr.arc(px, py, 6 / s, 0, 6.3)
                fill(cr, (1, 1, 1), a)


# ================================================================ shots
def S1(cr, t, tl, bid):
    A = tl.at
    t_med = A(bid, "medicine")
    t_horse = A(bid, "made")
    # phase 1: the cobra bursts out of a hole in the page
    if t < t_med + 0.4:
        a = 1 - seg(t, t_med, t_med + 0.4)
        def ph1(c):
            torn_hole(c, 360, 700, 250, 230)
            c.save()
            c.arc(360, 700, 240, 0, 6.3)
            c.rectangle(0, 0, W, 700)
            c.clip()
            k = ease_out(seg(t, tl.by_id[bid].start, tl.by_id[bid].start + 0.5))
            cobra(c, 360, 860 + 80 * (1 - k), 1.05, t, hood=k)
            c.restore()
        P.faded(cr, a, ph1)
    if t >= t_med:
        u = slide(t, t_med, 0.4)
        vial(cr, 150, 1010 + 300 * (1 - u), 0.95, glow=seg(t, t_horse, t_horse + 0.4))
    if t >= t_horse - 0.2:
        u = slide(t, t_horse - 0.2, 0.45)
        horse(cr, lerp(900, 400, u), 1000, 1.0)
    cue("hit", t, tl.by_id[bid].start + 0.05)


def S2(cr, t, tl, bid):
    A = tl.at
    flask(cr, 190, 560, 1.15)
    factory(cr, 520, 600, 1.15)
    red_x(cr, t, A(bid, "lab"), 190, 540, 85)
    red_x(cr, t, A(bid, "factory"), 520, 560, 95)
    th = A(bid, "factory", end=True) + 0.15
    if t >= th - 0.15:
        u = slide(t, th - 0.15, 0.35)
        horse(cr, lerp(-300, 330, u), 1060, 0.95)
        tick(cr, t, th + 0.25, 600, 820, 46)


def S3(cr, t, tl, bid):
    A = tl.at
    b = tl.by_id[bid]
    def mp(c):
        Pf = P.india(c, 360, 640, 520, hexc("#e8dcbc"), edge=hexc("#7d6a4a"), lw=2.5)
        r = np.random.default_rng(5)
        pts = []
        for ring in P._map("india")["india"]:
            P.poly(c, [Pf(*q) for q in ring])
        while len(pts) < 70:   # illustrative spread of dots over the country
            px, py = r.uniform(140, 580), r.uniform(390, 900)
            if c.in_fill(px, py):
                pts.append((px, py))
        c.new_path()
        t0 = A(bid, "snakebites")
        for i, (px, py) in enumerate(pts):
            u = seg(t, t0 + i * 0.03, t0 + i * 0.03 + 0.3)
            if u > 0:
                c.arc(px, py, 9 * u + 3 * math.sin(t * 5 + i) * u, 0, 6.3)
                c.set_source(P.rad_grad(px, py, 0, 12, [(0, (0.9, 0.2, 0.15, 0.9)), (1, (0.9, 0.2, 0.15, 0.1))]))
                c.fill()
    with_shadow(cr, mp, 4, 7, 0.25)
    flip_counter(cr, t, A(bid, "fifty-eight"), "58,000", 360, 1010, 104, 1.2, unit="DEATHS A YEAR · 2000-2019")


def S4(cr, t, tl, bid):
    A = tl.at
    def mp(c):
        Pf = P.world(c, 360, 560, 660, hexc("#d9ccaa"), edge=hexc("#8d7b58"), lw=1)
    with_shadow(cr, mp, 3, 6, 0.2)
    # India in red on the world map
    k = 660 / 360
    cx, cy = 360 + 82 * k, 560 - (22 - 12) * k
    P.india(cr, cx, cy, 30.7 * k, RED)
    t0 = A(bid, "half")
    u = ease_out(seg(t, t0 - 0.3, t0 + 0.6))
    P.pie(cr, 360, 900, 135, 0.47 * u)
    text(cr, "INDIA", 470, 830, 34, RED)
    text(cr, "REST OF THE WORLD", 250, 1080, 26, INK, P.FONT_MONO, align="center", alpha=0.85 * u)


def S5(cr, t, tl, bid):
    A = tl.at
    tf = A(bid, "first")
    if t < tf + 0.3:
        def q(c):
            horse(c, 330, 1000, 1.0)
            text(c, "?", 560, 640, 220, RED, alpha=appear(t, tl.by_id[bid].start + 0.3))
        P.faded(cr, 1 - seg(t, tf, tf + 0.3), q)
        if t < tf:
            return
    t0 = tf + 0.5
    def slide_(c):
        u = seg(t, t0 + 0.25, t0 + 1.4)
        r = np.random.default_rng(2)
        for i in range(40):
            ang, d = r.uniform(0, 6.3), r.uniform(0, 1) ** 0.5 * 210 * ease_out(u)
            venom_blob(c, d * math.cos(ang), d * math.sin(ang), r.uniform(9, 16), min(1, u * 3))
        if t > t0 + 0.25:
            w = seg(t, t0 + 0.25, t0 + 0.7)
            c.arc(0, 0, 230 * w, 0, 6.3)
            stroke(c, VENOM, 6, 1 - w)
    with place(cr, 360, 760, appear(t, tf)):
        P.microscope(cr, 0, 0, 255, slide_, tint=hexc("#f0e6c2"))
    # the drop falls
    if t0 - 0.4 <= t < t0 + 0.3:
        u = seg(t, t0 - 0.4, t0 + 0.25)
        blood_drop(cr, 360, lerp(330, 760, ease_in(u)), 26, VENOM)
    text(cr, "VENOM UNDER THE MICROSCOPE", 360, 1090, 18, P.TONES["teal"][1], P.FONT_MONO, align="center", spacing=2,
         alpha=0.75)


def ease_in(u):
    return u ** 2


def S6(cr, t, tl, bid):
    b = tl.by_id[bid]
    body_outline(cr, 360, 720, 0.78)
    sp = [(n, b.start + 0.25 + 0.3 * k, 0.7) for k, n in enumerate(["spine", "arm", "arm_l", "leg", "leg_l"])]
    sp += [(n, b.start + 1.1 + 0.25 * k, 0.7) for k, n in enumerate(["arm", "dia", "leg_l"])]
    nervous_system(cr, 360, 720, 0.78, t, sp)
    text(cr, "THE NERVOUS SYSTEM", 360, 1100, 18, BONE, P.FONT_MONO, align="center", spacing=2, alpha=0.7)


def S7(cr, t, tl, bid):
    A = tl.at
    tm, tb = A(bid, "move"), A(bid, "breathe")
    body_outline(cr, 360, 720, 0.78)
    sp = [("arm", tm - 0.5, 0.6), ("arm_l", tm - 0.5, 0.6), ("dia", tb - 0.5, 0.6), ("dia_l", tb - 0.5, 0.6),
          ("spine", A(bid) + 0.1, 0.5)]
    nervous_system(cr, 360, 720, 0.78, t, sp)
    for tt, lbl, x, y in ((tm, "MOVE", 560, 760), (tb, "BREATHE", 560, 560)):
        a = appear(t, tt)
        if a > 0:
            with place(cr, x, y, a, -0.05):
                P.card(cr, -90, -34, 180, 60, hexc("#efe6d2"), torn=True, seed=len(lbl))
                text(cr, lbl, 0, 16, 40, INK, align="center")


def S8(cr, t, tl, bid):
    A = tl.at
    tj = A(bid, "jams")
    b = tl.by_id[bid]
    # nerve coming down onto a muscle fibre
    cr.move_to(360, 380)
    cr.curve_to(360, 480, 330, 560, 360, 640)
    stroke(cr, hexc("#f2c75c"), 16)
    curve(cr, [(300, 640), (420, 640), (440, 690), (280, 690)], close=True)
    fill(cr, hexc("#f2c75c"))
    rrect(cr, 120, 700, 480, 200, 40)
    cr.set_source(P.lin_grad(0, 700, 0, 900, [(0, hexc("#c4544a")), (1, hexc("#8f2f2a"))]))
    cr.fill()
    for k in range(14):
        cr.move_to(140 + k * 33, 712)
        cr.line_to(140 + k * 33, 888)
        stroke(cr, hexc("#7a2320"), 3, 0.6)
    text(cr, "NERVE", 470, 470, 24, BONE, P.FONT_MONO, spacing=2)
    text(cr, "MUSCLE", 360, 950, 24, BONE, P.FONT_MONO, align="center", spacing=2)
    a = appear(t, A(bid, "cobra"))
    if a > 0:
        with place(cr, 190, 520, a, -0.05):
            P.card(cr, -130, -36, 260, 64, hexc("#efe6d2"), torn=True, seed=11)
            text(cr, "COBRA VENOM", 0, 14, 34, INK, align="center")
    # signals: they get through until the venom arrives
    period = 0.9
    for k in range(6):
        t0 = b.start + k * period
        if t0 > tj - 0.3 and k > 0:
            blocked = True
        else:
            blocked = False
        u = seg(t, t0, t0 + 0.6)
        if 0 < u < 1:
            yy = lerp(380, 670 if blocked else 700, u)
            cr.arc(360, yy, 20, 0, 6.3)
            cr.set_source(P.rad_grad(360, yy, 0, 20, [(0, (1, 0.97, 0.7, 1)), (1, (1, 0.8, 0.3, 0))]))
            cr.fill()
        if not blocked and seg(t, t0 + 0.6, t0 + 0.9) > 0 and t < t0 + 0.9:
            cr.rectangle(120, 700, 480, 200)
            fill(cr, (1, 0.9, 0.5), 0.25 * (1 - seg(t, t0 + 0.6, t0 + 0.9)))
    # venom blobs pile onto the junction
    r = np.random.default_rng(4)
    for i in range(16):
        tt = tj - 0.2 + i * 0.05
        u = ease_out(seg(t, tt, tt + 0.4))
        if u > 0:
            gx, gy = 360 + r.uniform(-90, 90), 690 + r.uniform(-30, 20)
            sx, sy = gx + r.uniform(-300, 300), 380
            venom_blob(cr, lerp(sx, gx, u), lerp(sy, gy, u), r.uniform(12, 18))
    if t > tj + 0.9:
        red_x(cr, t, tj + 0.9, 360, 560, 40, 8)


def S9(cr, t, tl, bid):
    A = tl.at
    te, tb = A(bid, "eyelids"), A(bid, "breathing")
    lid = ease_out(seg(t, te, te + 1.2)) * 0.75
    paper_person_head(cr, 220, 560, 140, lid, t)
    # lungs on a small dark board
    def board(c):
        rrect(c, 300, 720, 380, 380, 14)
        fill(c, hexc("#2a2724"))
    with_shadow(cr, board, 6, 9, 0.3)
    slow = seg(t, tb, tb + 1.8)
    ph = t * lerp(5.5, 1.5, slow)
    br = (0.5 + 0.5 * math.sin(ph)) * (1 - slow)
    cr.save()
    rrect(cr, 300, 720, 380, 380, 14)
    cr.clip()
    lungs(cr, 490, 920, 0.72, br, dead=slow)
    cr.restore()
    stopwatch(cr, 560, 470, 70, frac=0.6 * seg(t, tb, tb + 2.5), hand=0.6 * seg(t, tb, tb + 2.5))


def clot_slide(c, t, t_v):
    """Red cells with fibrin threads that start to knit, then melt away once the viper venom arrives."""
    r = np.random.default_rng(9)
    melt = seg(t, t_v + 0.2, t_v + 1.2)
    for i in range(22):
        ang, d = r.uniform(0, 6.3), r.uniform(0, 1) ** 0.5 * 200
        x, y = d * math.cos(ang), d * math.sin(ang)
        drift = 20 * melt * (1 if i % 2 else -1)
        red_cell(c, x + drift, y + 0.5 * drift, r.uniform(20, 28), r.uniform(0, 3))
    knit = min(seg(t, t_v - 1.6, t_v - 0.2), 1 - melt)
    for i in range(14):
        x0, y0 = r.uniform(-200, 200), r.uniform(-200, 200)
        x1, y1 = x0 + r.uniform(-160, 160), y0 + r.uniform(-160, 160)
        if knit > 0:
            c.move_to(x0, y0)
            c.line_to(lerp(x0, x1, knit), lerp(y0, y1, knit))
            stroke(c, hexc("#f4e9c8"), 3, 0.9)
    if t > t_v:
        u = seg(t, t_v, t_v + 0.8)
        for i in range(10):
            ang, d = r.uniform(0, 6.3), r.uniform(0, 1) ** 0.5 * 190 * u
            venom_blob(c, d * math.cos(ang), d * math.sin(ang), 13, u)


def S10(cr, t, tl, bid):
    A = tl.at
    tv = A(bid, "viper")
    tc = A(bid, "clots")
    P.microscope(cr, 360, 820, 240, lambda c: clot_slide(c, t, tc - 0.4), tint=hexc("#f3d9cf"))
    sp = wavy(130, 470, 300, 22, 1.4, phase=t * 1.4)
    if t >= tv - 0.1:
        u = slide(t, tv - 0.1, 0.4)
        with place(cr, lerp(-400, 0, u), 0, 1):
            snake(cr, sp, 30, 3, BIG_FOUR[2][1], pattern="chain", tongue=0.6 + 0.4 * math.sin(t * 9))
            text(cr, "RUSSELL'S VIPER", 290, 535, 24, INK, P.FONT_MONO, align="center", spacing=1)
    if t > tc + 0.5:
        stamp(cr, t, tc + 0.5, "NO CLOT", 520, 1030, -0.1, size=52)


def S11(cr, t, tl, bid):
    b = tl.by_id[bid]
    u = slide(t, b.start, 0.5)
    horse(cr, lerp(-260, 300, u), 1000, 1.2)


def S12(cr, t, tl, bid):
    A = tl.at
    b = tl.by_id[bid]
    t0 = b.start + 0.25
    pos = [(200, 560, -0.05), (520, 560, 0.04), (200, 880, 0.04), (520, 880, -0.04)]
    for k, (x, y, rot) in enumerate(pos):
        tk = t0 + k * 0.45
        a = appear(t, tk)
        if a > 0:
            cue("pop", t, tk)
            snake_card(cr, x, y, k, t, rot, 0.98 * a)


def S13(cr, t, tl, bid):
    A = tl.at
    tt, tsm = A(bid, "tiny"), A(bid, "small")
    horse(cr, 330, 1080, 1.0)
    u = slide(t, tl.by_id[bid].start, 0.45)
    push = seg(t, tt, tt + 1.0)
    syringe(cr, lerp(60, 300, u), lerp(610, 790, u), 0.85, rot=math.pi + 0.64, push=push * 0.25)
    gauge(cr, 360, 520, 150, lerp(0.02, 0.14, seg(t, tt, tt + 0.6)))
    if t > tsm:
        stamp(cr, t, tsm + 0.1, "SAFE DOSE", 500, 640, -0.08, col=hexc("#2f7a48"), size=40)


def anti_slide(c, t, t0, t1, scale=1.0):
    """Venom blobs; antibodies appear (from t0) and latch on (from t1)."""
    r = np.random.default_rng(12)
    blobs = [(r.uniform(-170, 170), r.uniform(-170, 170)) for _ in range(9)]
    for i, (x, y) in enumerate(blobs):
        grab = seg(t, t1 + i * 0.08, t1 + i * 0.08 + 0.5)
        venom_blob(c, x, y, 16 * scale, 1, grey=0.6 * grab)
        for j in range(3):
            ang = j * 2.1 + i
            a = appear(t, t0 + 0.08 * (i * 3 + j) * 0.5)
            if a <= 0:
                continue
            far = 120 + 30 * j
            d = lerp(far, 30 * scale, ease_out(grab))
            ax, ay = x + d * math.cos(ang), y + d * math.sin(ang)
            antibody(c, ax, ay, 0.9 * scale * a, ang - math.pi / 2 + math.pi, 1)


def S14(cr, t, tl, bid):
    A = tl.at
    ta, tb = A(bid, "army"), A(bid, "antibodies")
    P.microscope(cr, 360, 760, 260, lambda c: anti_slide(c, t, ta, tb + 0.3), tint=hexc("#e9e0c6"))
    if t > tb:
        with place(cr, 560, 1060, appear(t, tb), -0.06):
            P.card(cr, -130, -36, 260, 64, hexc("#efe6d2"), torn=True, seed=3)
            antibody(cr, -95, 0, 0.9)
            text(cr, "ANTIBODY", 20, 16, 36, INK, align="center")


def blood_bag(cr, x, y, s=1.0, level=1.0):
    with place(cr, x, y, s):
        def d(c):
            rrect(c, -80, -120, 160, 230, 30)
            fill(c, hexc("#f4f1ea"), 0.95)
            rrect(c, -70, -110 + 210 * (1 - level), 140, 210 * level, 24)
            fill(c, CELL)
            c.rectangle(-60, -60, 120, 60)
            fill(c, hexc("#ffffff"), 0.9)
            text(c, "HORSE", 0, -38, 18, INK, P.FONT_MONO, align="center", spacing=2)
            text(c, "PLASMA", 0, -14, 18, INK, P.FONT_MONO, align="center", spacing=2)
            c.move_to(0, 110)
            c.line_to(0, 160)
            stroke(c, hexc("#d9d4c8"), 8)
        with_shadow(cr, d, 5, 8, 0.3)


def arrow(cr, x0, y0, x1, y1, u, col=INK):
    if u <= 0:
        return
    xe, ye = lerp(x0, x1, u), lerp(y0, y1, u)
    cr.move_to(x0, y0)
    cr.line_to(xe, ye)
    stroke(cr, col, 6)
    a = math.atan2(y1 - y0, x1 - x0)
    poly(cr, [(xe + 16 * math.cos(a), ye + 16 * math.sin(a)), (xe + 14 * math.cos(a + 2.4), ye + 14 * math.sin(a + 2.4)),
              (xe + 14 * math.cos(a - 2.4), ye + 14 * math.sin(a - 2.4))])
    fill(cr, col)


def filter_funnel(cr, x, y, s=1.0, drip=0.0):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-90, -90), (90, -90), (14, 20), (14, 90), (-14, 90), (-14, 20)])
            c.set_source(P.lin_grad(-90, 0, 90, 0, [(0, (0.85, 0.88, 0.88, 0.9)), (0.5, (1, 1, 1, 0.85)),
                                                    (1, (0.75, 0.78, 0.78, 0.9))]))
            c.fill()
            poly(c, [(-70, -80), (70, -80), (0, 0)])
            fill(c, hexc("#f6f0de"))
            text(c, "PURIFY", 0, -100, 20, INK, P.FONT_MONO, align="center", spacing=2)
        with_shadow(cr, d, 5, 8, 0.3)
        if drip > 0:
            yy = 100 + 60 * (drip % 1)
            cr.arc(0, yy, 6, 0, 6.3)
            fill(cr, hexc("#f2e7c4"))


def S15(cr, t, tl, bid):
    A = tl.at
    tb, tp, ta = A(bid, "blood"), A(bid, "purify"), A(bid, "antibodies")
    a = appear(t, tl.by_id[bid].start + 0.1)
    if a > 0:
        blood_bag(cr, 150, 640, a, 1 - 0.4 * seg(t, tp, tp + 1.2))
    arrow(cr, 245, 640, 290, 640, seg(t, tp - 0.3, tp))
    a2 = appear(t, tp - 0.1)
    if a2 > 0:
        filter_funnel(cr, 380, 640, a2, drip=(t - tp) * 1.5 if t > tp else 0)
    arrow(cr, 470, 640, 515, 640, seg(t, ta - 0.4, ta - 0.1))
    a3 = appear(t, ta - 0.1)
    if a3 > 0:
        vial(cr, 600, 760, 0.85 * a3, glow=seg(t, ta, ta + 0.5))
    if t > ta:
        with place(cr, 360, 950, appear(t, ta + 0.2)):
            for k in range(5):
                antibody(cr, -140 + 70 * k, 0, 1.1, 0.2 * math.sin(t * 2 + k))


def S16(cr, t, tl, bid):
    A = tl.at
    tg = A(bid, "grab")
    P.microscope(cr, 360, 720, 260, lambda c: anti_slide(c, t, tl.by_id[bid].start - 0.2, tg - 0.3, 1.1),
                 tint=hexc("#f3d0c4"))
    vial(cr, 590, 1100, 0.7)


def S17(cr, t, tl, bid):
    A = tl.at
    ts, td = A(bid, "snake"), A(bid, "delay")
    sp = wavy(90, 560, 280, 20, 1.3, phase=t * 1.4)
    snake(cr, sp, 28, 3, BIG_FOUR[0][1])
    if t > ts:
        red_x(cr, t, ts + 0.1, 230, 560, 70)
    if t > td - 0.3:
        a = appear(t, td - 0.3)
        with place(cr, 470, 860, a):
            fr = seg(t, td, td + 3.0) * 0.8
            stopwatch(cr, 0, 0, 170, fr, fr)


def night_room(cr, t):
    # window with the moon
    def win(c):
        rrect(c, 380, 380, 230, 270, 6)
        fill(c, hexc("#4a3a2c"))
        c.rectangle(396, 396, 198, 238)
        fill(c, hexc("#141a2a"))
        c.arc(520, 470, 34, 0, 6.3)
        fill(c, hexc("#f1e9c8"))
        c.arc(506, 462, 30, 0, 6.3)
        fill(c, hexc("#141a2a"))
        for sx, sy in ((430, 430), (560, 560), (450, 600), (580, 420)):
            c.arc(sx, sy, 2.4, 0, 6.3)
            fill(c, hexc("#f1e9c8"))
        c.move_to(495, 396)
        c.line_to(495, 634)
        c.move_to(396, 515)
        c.line_to(594, 515)
        stroke(c, hexc("#4a3a2c"), 8)
    with_shadow(cr, win, 6, 9, 0.35)
    # floor
    cr.rectangle(0, 900, W, H - 900)
    fill(cr, hexc("#6a5a4c"))
    cr.move_to(0, 900)
    cr.line_to(W, 900)
    stroke(cr, hexc("#3d3a42"), 3)
    # mat with stripes and a sleeper under a blanket
    def mat(c):
        poly(c, [(80, 960), (560, 960), (600, 1030), (40, 1030)])
        fill(c, hexc("#8a5a3a"))
        for k in range(7):
            x = 100 + k * 70
            poly(c, [(x, 960), (x + 26, 960), (x + 30, 1030), (x + 4, 1030)])
            fill(c, hexc("#c99a5a"), 0.7)
        c.arc(130, 945, 30, 0, 6.3)
        fill(c, hexc("#e9dcc0"))
        curve(c, [(160, 960), (220, 920), (400, 915), (520, 940), (540, 975), (160, 985)], close=True)
        fill(c, hexc("#5b6b8a"))
    with_shadow(cr, mat, 4, 6, 0.3)
    breathe = 4 * math.sin(t * 2.0)
    cr.arc(130, 945, 30, 0, 6.3)
    stroke(cr, hexc("#b9a888"), 2)
    text(cr, "z", 175, 890 - breathe, 30, hexc("#f1e9c8"), alpha=0.7)
    text(cr, "z", 200, 860 - breathe, 22, hexc("#f1e9c8"), alpha=0.5)


def S18(cr, t, tl, bid):
    A = tl.at
    night_room(cr, t)
    tk = A(bid, "krait")
    u = ease_out(seg(t, tk - 0.3, tk + 3.5))
    xh = lerp(760, 470, u)
    sp = _spine(lambda v: (xh + 330 * v, 1062 + 14 * math.sin(2 * math.pi * 1.6 * v + t * 4) * (0.4 + 0.6 * v)), 70)
    snake(cr, sp, 22, 3, BIG_FOUR[1][1], pattern="bands", pat_col=BIG_FOUR[1][3])


def arm(cr, x, y, s=1.0):
    """A forearm and hand, paper cut-out, lying across the page (hand to the right)."""
    with place(cr, x, y, s):
        def d(c):
            curve(c, [(-330, -46), (60, -54), (140, -60), (200, -52), (250, -40), (296, -30), (300, -8),
                      (262, 0), (300, 14), (296, 34), (250, 46), (150, 54), (60, 50), (-330, 46)], close=True)
            c.set_source(P.lin_grad(0, -60, 0, 60, [(0, hexc("#e7b98f")), (0.6, hexc("#d6a079")),
                                                    (1, hexc("#b9805c"))]))
            c.fill()
        with_shadow(cr, d, 6, 10, 0.3)


def S19(cr, t, tl, bid):
    A = tl.at
    arm(cr, 300, 600, 1.0)
    tb = A(bid, "bite")
    for k, dx in enumerate((0, 26)):
        a = appear(t, tb + 0.1 * k)
        if a > 0:
            cr.arc(240 + dx, 596, 5.5 * a, 0, 6.3)
            fill(cr, hexc("#7a1a16"))
    circle_mark(cr, t, tb + 0.3, 253, 596, 60, 46)
    # pain meter barely moves
    tp = A(bid, "painless")
    def meter(c):
        rrect(c, 160, 760, 400, 260, 16)
        fill(c, hexc("#efe6d2"))
        text(c, "PAIN", 360, 810, 24, INK, P.FONT_MONO, align="center", spacing=3)
        for k in range(10):
            c.rectangle(190 + k * 34, 840, 28, 120)
            fill(c, (0.25 + 0.07 * k, 0.6 - 0.05 * k, 0.3 - 0.02 * k), 0.25)
        lvl = 1 + int(seg(t, tp - 0.5, tp) * 0.99)
        for k in range(lvl):
            c.rectangle(190 + k * 34, 840, 28, 120)
            fill(c, (0.25 + 0.07 * k, 0.6 - 0.05 * k, 0.3 - 0.02 * k))
    with_shadow(cr, meter, 6, 9, 0.3)
    if t > A(bid, "sleep"):
        text(cr, "z z z", 470, 680, 40, P.TONES["night"][1], alpha=appear(t, A(bid, "sleep")))


ICONS = ["CUTTING", "SUCKING", "TIGHT ROPE", "HERBS"]


def icon(c, k, w, h):
    c.rectangle(0, 0, w, h)
    fill(c, hexc("#d9cfb6"))
    cx, cy = w / 2, h / 2
    if k == 0:   # knife
        poly(c, [(cx - 70, cy + 30), (cx + 60, cy - 40), (cx + 70, cy - 30), (cx - 50, cy + 40)])
        fill(c, hexc("#c9cdd0"))
        rrect(c, cx - 100, cy + 22, 50, 26, 6)
        fill(c, hexc("#6a4a2c"))
    elif k == 1:   # lips
        curve(c, [(cx - 60, cy), (cx - 30, cy - 26), (cx, cy - 16), (cx + 30, cy - 26), (cx + 60, cy), (cx + 30, cy + 28),
                  (cx - 30, cy + 28)], close=True)
        fill(c, hexc("#c4544a"))
        c.move_to(cx - 56, cy)
        c.curve_to(cx - 20, cy + 6, cx + 20, cy + 6, cx + 56, cy)
        stroke(c, hexc("#7a2320"), 3)
    elif k == 2:   # rope tied round an arm
        c.rectangle(0, cy - 26, w, 52)
        fill(c, hexc("#d6a079"))
        for j in range(5):
            c.move_to(cx - 30 + j * 12, cy - 34)
            c.line_to(cx - 40 + j * 12, cy + 34)
            stroke(c, hexc("#a8844e"), 7)
    else:   # leaves
        for j, (dx, rot) in enumerate(((-30, -0.6), (10, 0.2), (40, 0.9))):
            with place(c, cx + dx, cy + 10, 1, rot):
                curve(c, [(0, 40), (-22, 0), (0, -46), (22, 0)], close=True)
                fill(c, hexc("#4f8a4a"))
                c.move_to(0, 40)
                c.line_to(0, -40)
                stroke(c, hexc("#2f5a2c"), 2)


def S20(cr, t, tl, bid, all_x=False):
    A = tl.at
    cr.move_to(40, 470)
    cr.curve_to(250, 520, 470, 520, 680, 470)
    stroke(cr, hexc("#7a6a52"), 3)
    words = ["cutting", "sucking", "ropes", "herbs"]
    pos = [(170, 640, -0.06), (420, 660, 0.05), (170, 960, 0.04), (420, 980, -0.05)]
    for k, (x, y, rot) in enumerate(pos):
        tk = tl.by_id[bid].start if all_x else (A(bid, words[k]) if k else tl.by_id[bid].start + 0.3)
        a = appear(t, tk - 0.25) if not all_x else 1
        if a > 0:
            with place(cr, x + 50, y, a):
                polaroid(cr, 0, 0, 230, 270, lambda c, w, h, k=k: icon(c, k, w, h), rot, ICONS[k])
                P.clothes_pin(cr, 0, -130)
            red_x(cr, t, (tk + 0.15) if not all_x else tk - 1, x + 50, y - 20, 70, 11)


def S21(cr, t, tl, bid):
    S20(cr, t, tl, bid, all_x=True)
    stamp(cr, t, tl.at(bid, "none") + 0.05, "DOESN'T WORK", 360, 800, -0.14, size=70)


def S22(cr, t, tl, bid):
    A = tl.at
    P.checklist(cr, t, 70, 420, 580, ["STAY CALM", "KEEP THE LIMB STILL", "HOSPITAL, FAST"],
                [A(bid, "calm"), A(bid, "still"), A(bid, "hospital")])
    a = appear(t, A(bid, "fast"))
    if a > 0:
        with place(cr, 520, 1020, a):
            stopwatch(cr, 0, 0, 80, 0.08, 0.08)


def S23(cr, t, tl, bid):
    A = tl.at
    b = tl.by_id[bid]
    horse(cr, 330, 1060, 1.0, badge=appear(t, A(bid, "horse")))
    a = appear(t, A(bid, "comments") - 0.2)
    if a > 0:
        with place(cr, 360, 520, a):
            P.comment_bubble(cr, -280, -80, 560, 150, "A HORSE SAVED YOU?")


SHOTS = {
    "s1": Shot(S1, "HOOK", 1, "khaki", "MADE INSIDE", "A HORSE", "horse"),
    "s2": Shot(S2, "HOOK", 2, "khaki", "NOT A LAB.", "A HORSE.", "horse"),
    "s3": Shot(S3, "INDIA", 3, "cream", "EVERY YEAR", "58,000", "fifty-eight"),
    "s4": Shot(S4, "THE WORLD", 4, "khaki", "CLOSE TO", "HALF", "half"),
    "s5": Shot(S5, "THE VENOM", 1, "teal", "HOW DOES A HORSE", "FIX IT?", "fix",
               extra=dict(phases=[("first", "FIRST,", "THE VENOM", "venom")])),
    "s6": Shot(S6, "THE VENOM", 2, "dark", "YOUR BODY", "RUNS ON MESSAGES", "messages"),
    "s7": Shot(S7, "THE VENOM", 3, "dark", "MOVE.", "BREATHE.", "breathe"),
    "s8": Shot(S8, "THE VENOM", 4, "dark", "IT JAMS", "THE SIGNAL", "jams"),
    "s9": Shot(S9, "THE VENOM", 5, "mint", "EYELIDS DROOP", "THEN BREATHING", "breathing"),
    "s10": Shot(S10, "THE VENOM", 6, "khaki", "BLOOD", "WON'T CLOT", "clots"),
    "s11": Shot(S11, "THE HORSE", 1, "cream", "NOW,", "THE HORSE", "horse"),
    "s12": Shot(S12, "THE HORSE", 2, "khaki", "THE", "BIG FOUR", "four"),
    "s13": Shot(S13, "THE HORSE", 3, "cream", "TINY", "DOSES", "tiny"),
    "s14": Shot(S14, "THE HORSE", 4, "teal", "ITS ARMY", "LEARNS", "learns"),
    "s15": Shot(S15, "THE HORSE", 5, "cream", "PURIFIED", "ANTIBODIES", "purify"),
    "s16": Shot(S16, "THE CURE", 1, "blood", "BORROWED", "BODYGUARDS", "bodyguards"),
    "s17": Shot(S17, "THE DELAY", 1, "khaki", "NOT THE SNAKE", "THE DELAY", "delay"),
    "s18": Shot(S18, "THE DELAY", 2, "night", "AT NIGHT", "ON THE FLOOR", "floor", zoom=0.02),
    "s19": Shot(S19, "THE DELAY", 3, "night", "ALMOST", "PAINLESS", "painless"),
    "s20": Shot(S20, "MYTHS", 1, "khaki", "HOURS", "WASTED", "hours"),
    "s21": Shot(S21, "MYTHS", 2, "khaki", "NONE", "WORK", "none"),
    "s22": Shot(S22, "WHAT TO DO", 1, "mint", "STAY CALM", "GET TO HOSPITAL", "hospital"),
    "s23": Shot(S23, "END", 1, "cream", "A HORSE", "SAVED YOU?", "horse"),
}
