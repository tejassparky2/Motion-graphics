"""Shots for videos/superbugs.py: our own drawings (bacteria, petri dish, plasmid, pills, viruses, props)."""
import math

import numpy as np

from motion import paper as P
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg, smooth
from motion.paper import (INK, RED, Shot, appear, circle_mark, curve, fill, flip_counter, place, poly, rrect, shade,
                          slide, stamp, stroke, text, tick, red_x, with_shadow)
from videos.snakebite_shots import arrow

GERM = hexc("#6fa64a")
MUTANT = hexc("#8a5fb8")
GOLD = hexc("#e2b23c")
SKIN = hexc("#e7b98f")


# ================================================================ drawings
def bacterium(cr, x, y, s=1.0, rot=0.0, col=None, shield=0.0, burst=0.0, t=0.0, a=1.0):
    """A rod-shaped bacterium; `shield` 0..1 adds a gold shield badge; `burst` 0..1 pops it."""
    col = col or GERM
    if burst >= 1 or a <= 0:
        return
    k = s * (1 + 0.25 * burst)
    with place(cr, x, y, k, rot):
        al = a * (1 - burst)
        for j in range(3):   # flagella
            cr.move_to(-40, -8 + 8 * j)
            for i in range(1, 7):
                cr.line_to(-40 - i * 7, -8 + 8 * j + 4 * math.sin(i * 1.4 + t * 8 + j))
            stroke(cr, shade(col, 0.6), 1.6, al)
        rrect(cr, -40, -17, 80, 34, 17)
        cr.set_source(P.lin_grad(0, -17, 0, 17, [(0, (*shade(col, 1.25)[:3], al)), (0.5, (*col[:3], al)),
                                                 (1, (*shade(col, 0.7)[:3], al))]))
        cr.fill()
        rrect(cr, -40, -17, 80, 34, 17)
        stroke(cr, shade(col, 0.55), 2, al)
        for dx, dy in ((-18, -3), (4, 5), (20, -4)):
            cr.arc(dx, dy, 3.2, 0, 6.3)
            fill(cr, shade(col, 0.6), al)
        if shield > 0:
            with place(cr, 24, -20, shield):
                shield_icon(cr, 0, 0, 0.55, al)
    if 0 < burst < 1:
        for i in range(8):
            ang = i * math.pi / 4 + 0.3
            r0, r1 = 40 * s * (0.6 + burst), 40 * s * (0.9 + burst * 1.2)
            cr.move_to(x + r0 * math.cos(ang), y + r0 * math.sin(ang))
            cr.line_to(x + r1 * math.cos(ang), y + r1 * math.sin(ang))
            stroke(cr, shade(col, 0.7), 3, 1 - burst)


def coccus(cr, x, y, r=26, col=None, shield=0.0):
    col = col or hexc("#d9a03a")
    for dx in (-r * 0.9, r * 0.9):   # a pair, like diplococci
        cr.arc(x + dx, y, r, 0, 6.3)
        cr.set_source(P.rad_grad(x + dx - r * 0.3, y - r * 0.3, r * 0.1, r, [(0, shade(col, 1.25)), (1, shade(col, 0.8))]))
        cr.fill()
        cr.arc(x + dx, y, r, 0, 6.3)
        stroke(cr, shade(col, 0.55), 2)
    if shield > 0:
        with place(cr, x + r * 1.4, y - r, shield):
            shield_icon(cr, 0, 0, 0.55)


def shield_icon(cr, x, y, s=1.0, a=1.0):
    with place(cr, x, y, s):
        curve(cr, [(0, -34), (28, -24), (26, 6), (0, 32), (-26, 6), (-28, -24)], close=True)
        cr.set_source(P.lin_grad(-28, 0, 28, 0, [(0, shade(GOLD, 1.2)), (1, shade(GOLD, 0.8))]))
        cr.fill()
        curve(cr, [(0, -34), (28, -24), (26, 6), (0, 32), (-26, 6), (-28, -24)], close=True)
        stroke(cr, hexc("#7a5a18"), 3, a)
        cr.move_to(0, -24)
        cr.line_to(0, 22)
        stroke(cr, hexc("#7a5a18"), 2, a * 0.7)


def plasmid(cr, x, y, r=34, s=1.0, rot=0.0):
    with place(cr, x, y, s, rot):
        cr.arc(0, 0, r, 0, 6.3)
        stroke(cr, hexc("#3a6fb0"), 7)
        cr.arc(0, 0, r, 0, 6.3)
        stroke(cr, hexc("#9cc3ea"), 2.5)
        cr.arc(0, 0, r, -0.6, 0.6)
        stroke(cr, GOLD, 8)


def petri(cr, x, y, r, t, colonies=1.0, clear=0.0, mould=0.0, regrow=0.0):
    """A petri dish: bacterial colonies on agar; a mould spot with a clear ring where the bacteria died."""
    def d(c):
        c.arc(x, y, r + 12, 0, 6.3)
        fill(c, (0.92, 0.94, 0.94), 0.9)
        c.arc(x, y, r, 0, 6.3)
        c.set_source(P.rad_grad(x, y, 10, r, [(0, hexc("#f1dc98")), (1, hexc("#d9bf72"))]))
        c.fill()
    with_shadow(cr, d, 6, 9, 0.3)
    r_ = np.random.default_rng(1)
    cx, cy = x + r * 0.05, y - r * 0.05
    for i in range(110):
        ang, d = r_.uniform(0, 6.3), r_.uniform(0, 1) ** 0.5 * r * 0.9
        px, py = x + d * math.cos(ang), y + d * math.sin(ang)
        dist = math.hypot(px - cx, py - cy)
        dead = clear > 0 and dist < r * 0.55 * clear
        back = regrow > 0 and dist < r * 0.55 and (i % 4 == 0 or regrow > 0.5)
        if (dead and not back) or i / 110 > colonies:
            continue
        rr = r_.uniform(4, 9)
        cr.arc(px, py, rr, 0, 6.3)
        fill(cr, MUTANT if back else hexc("#f4f0e4"), 0.95)
        cr.arc(px, py, rr, 0, 6.3)
        stroke(cr, hexc("#b8a878"), 1)
    if mould > 0:
        for k in range(14):
            ang = k * 0.45
            rr = r * 0.16 * mould * (1 + 0.15 * math.sin(k * 2.3))
            cr.arc(cx + rr * 0.5 * math.cos(ang), cy + rr * 0.5 * math.sin(ang), rr * 0.7, 0, 6.3)
            fill(cr, hexc("#5f9a8a"), 0.7)
        cr.arc(cx, cy, r * 0.12 * mould, 0, 6.3)
        fill(cr, hexc("#f2f4ee"))
    cr.arc(x - r * 0.35, y - r * 0.4, r * 0.5, 0, 6.3)   # glass glint
    cr.set_source(P.rad_grad(x - r * 0.35, y - r * 0.4, 0, r * 0.5, [(0, (1, 1, 1, 0.25)), (1, (1, 1, 1, 0))]))
    cr.fill()


def finger(cr, x, y, s, spread):
    """A hand-drawn finger (pointing right) with a small cut; red streaks spread as `spread` goes 0 -> 1."""
    with place(cr, x, y, s):
        def d(c):
            curve(c, [(-360, -70), (60, -72), (180, -66), (250, -46), (276, 0), (250, 46), (180, 66), (60, 72),
                      (-360, 70)], close=True)
            c.set_source(P.lin_grad(0, -72, 0, 72, [(0, hexc("#efc39b")), (0.6, SKIN), (1, hexc("#c08b63"))]))
            c.fill()
            for kx in (-120, 40):   # knuckle creases
                c.move_to(kx, -50)
                c.curve_to(kx + 8, -20, kx + 8, 20, kx, 50)
                stroke(c, hexc("#b9805c"), 2, 0.6)
            curve(c, [(170, -40), (232, -34), (254, 0), (232, 34), (170, 40)], close=False)
            stroke(c, hexc("#d9a585"), 3)
        with_shadow(cr, d, 6, 10, 0.3)
        cr.move_to(90, -14)
        cr.line_to(128, 10)
        stroke(cr, hexc("#8e1f1a"), 5)
        if spread > 0:
            r = np.random.default_rng(3)
            for k in range(7):
                ang = math.pi + r.uniform(-0.6, 0.6)
                L = 60 + 300 * spread * r.uniform(0.6, 1)
                pts = [(110, 0)]
                for j in range(1, 8):
                    px = 110 + L * j / 7 * math.cos(ang)
                    py = L * j / 7 * math.sin(ang) * 0.35 + r.uniform(-6, 6)
                    pts.append((px, max(-60, min(60, py))))
                curve(cr, pts)
                stroke(cr, hexc("#c4302b"), 4, 0.55)
            cr.arc(110, 0, 50 + 40 * spread, 0, 6.3)
            cr.set_source(P.rad_grad(110, 0, 0, 50 + 40 * spread, [(0, (0.85, 0.2, 0.15, 0.45)), (1, (0.85, 0.2, 0.15, 0))]))
            cr.fill()


def capsule(cr, x, y, s=1.0, rot=0.0):
    with place(cr, x, y, s, rot):
        def d(c):
            rrect(c, -60, -24, 120, 48, 24)
            fill(c, hexc("#f4efe4"))
            c.save()
            rrect(c, -60, -24, 120, 48, 24)
            c.clip()
            c.rectangle(-60, -24, 60, 48)
            fill(c, RED)
            c.restore()
            rrect(c, -50, -16, 100, 10, 5)
            fill(c, (1, 1, 1), 0.35)
        with_shadow(cr, d, 4, 7, 0.3)


def virus(cr, x, y, r=50, col=None, rot=0.0):
    col = col or hexc("#7d8fc4")
    with place(cr, x, y, 1, rot):
        for k in range(14):
            ang = 2 * math.pi * k / 14
            cr.move_to(r * 0.9 * math.cos(ang), r * 0.9 * math.sin(ang))
            cr.line_to(r * 1.3 * math.cos(ang), r * 1.3 * math.sin(ang))
            stroke(cr, shade(col, 0.7), 4)
            cr.arc(r * 1.33 * math.cos(ang), r * 1.33 * math.sin(ang), 6, 0, 6.3)
            fill(cr, hexc("#e2b23c"))
        cr.arc(0, 0, r, 0, 6.3)
        cr.set_source(P.rad_grad(-r * 0.3, -r * 0.3, r * 0.1, r, [(0, shade(col, 1.3)), (1, shade(col, 0.8))]))
        cr.fill()


def tissue_box(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-110, -60), (110, -60), (110, 70), (-110, 70)])
            fill(c, hexc("#7fb2c9"))
            for k in range(5):
                c.arc(-80 + k * 40, 5, 12, 0, 6.3)
                fill(c, hexc("#f2e6c9"), 0.8)
            curve(c, [(-40, -60), (-20, -120), (20, -110), (40, -60)], close=True)
            fill(c, hexc("#fbf8f0"))
        with_shadow(cr, d, 5, 8, 0.3)


def thermometer(cr, x, y, s=1.0, level=0.7):
    with place(cr, x, y, s):
        rrect(cr, -12, -180, 24, 200, 12)
        fill(cr, hexc("#f4f4f2"))
        rrect(cr, -12, -180, 24, 200, 12)
        stroke(cr, hexc("#a8a8a8"), 2)
        rrect(cr, -5, -170 + 170 * (1 - level), 10, 170 * level + 10, 5)
        fill(cr, RED)
        cr.arc(0, 30, 22, 0, 6.3)
        fill(cr, RED)
        for k in range(8):
            cr.move_to(12, -150 + k * 20)
            cr.line_to(22, -150 + k * 20)
            stroke(cr, INK, 1.5, 0.6)


def paper_person(cr, x, y, s=1.0, col=None):
    """A gingerbread-style paper cut-out person (x, y = feet)."""
    col = col or hexc("#efe3c6")
    with place(cr, x, y, s):
        def d(c):
            c.arc(0, -300, 52, 0, 6.3)
            fill(c, col)
            curve(c, [(-60, -240), (60, -240), (130, -160), (120, -130), (60, -170), (64, -80), (84, 0), (30, 0),
                      (0, -70), (-30, 0), (-84, 0), (-64, -80), (-60, -170), (-120, -130), (-130, -160)], close=True)
            fill(c, col)
        with_shadow(cr, d, 6, 9, 0.3)


def dumbbell(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        cr.move_to(-40, 0)
        cr.line_to(40, 0)
        stroke(cr, hexc("#5a5a5a"), 6)
        for sx in (-40, 40):
            rrect(cr, sx - 8, -18, 16, 36, 4)
            fill(cr, hexc("#3a3a3a"))


def prescription(cr, x, y, t, t_tick):
    def d(c):
        P.card(c, x, y, 420, 520, hexc("#f7f3ea"))
        c.rectangle(x, y, 420, 70)
        fill(c, hexc("#3a6fb0"))
        text(c, "CLINIC", x + 30, y + 46, 30, hexc("#ffffff"), P.FONT_MONO, spacing=3)
        text(c, "Rx", x + 30, y + 180, 90, INK)
        for k in range(5):
            c.move_to(x + 30, y + 240 + k * 46)
            c.line_to(x + 390, y + 240 + k * 46)
            stroke(c, INK, 1.5, 0.35)
        text(c, "Take exactly as prescribed", x + 30, y + 228, 22, INK, P.FONT_MONO, alpha=0.85)
        c.move_to(x + 220, y + 470)
        c.curve_to(x + 260, y + 430, x + 300, y + 500, x + 380, y + 450)
        stroke(c, INK, 2.5)
    with_shadow(cr, d, 6, 10, 0.3)
    tick(cr, t, t_tick, x + 330, y + 160, 50, lw=12)


def pill_strip(cr, x, y, s=1.0, used=4):
    with place(cr, x, y, s):
        def d(c):
            rrect(c, -170, -70, 340, 140, 12)
            c.set_source(P.lin_grad(0, -70, 0, 70, [(0, hexc("#e6e8ea")), (1, hexc("#b9bec2"))]))
            c.fill()
            for k in range(10):
                px, py = -132 + (k % 5) * 66, -30 + (k // 5) * 60
                rrect(c, px - 24, py - 14, 48, 28, 14)
                if k < used:
                    stroke(c, hexc("#8a8f93"), 2)
                else:
                    fill(c, hexc("#f4efe4"))
                    rrect(c, px - 24, py - 14, 48, 28, 14)
                    stroke(c, hexc("#a8a8a8"), 1.5)
        with_shadow(cr, d, 5, 8, 0.3)


def medal(cr, x, y, s=1.0, year="1945"):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-40, -170), (-6, -170), (-6, -60), (-40, -80)])
            fill(c, hexc("#3a6fb0"))
            poly(c, [(40, -170), (6, -170), (6, -60), (40, -80)])
            fill(c, RED)
            c.arc(0, 0, 80, 0, 6.3)
            c.set_source(P.rad_grad(-20, -20, 10, 80, [(0, hexc("#f6dc8a")), (0.7, hexc("#d4a83a")),
                                                       (1, hexc("#9c7a22"))]))
            c.fill()
            c.arc(0, 0, 64, 0, 6.3)
            stroke(c, hexc("#9c7a22"), 3)
            text(c, year, 0, 14, 40, hexc("#6a5010"), align="center")
        with_shadow(cr, d, 5, 8, 0.3)


def year_card(cr, x, y, year, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            P.card(c, -140, -100, 280, 200, hexc("#f4eedc"))
            c.rectangle(-140, -100, 280, 50)
            fill(c, RED)
            for hx in (-90, -30, 30, 90):
                c.arc(hx, -100, 7, 0, 6.3)
                fill(c, hexc("#3a3a3a"))
            text(c, "YEAR", 0, -64, 22, hexc("#ffffff"), P.FONT_MONO, align="center", spacing=3)
            text(c, year, 0, 70, 96, INK, align="center")
        with_shadow(cr, d, 5, 8, 0.3)


# ================================================================ the population (b7 - b11)
_R = np.random.default_rng(21)
POP = []
for _ in range(4000):          # random packing of rod-shaped bacteria inside the microscope circle
    ang, d = _R.uniform(0, 6.3), _R.uniform(0, 1) ** 0.6 * 215
    x, y = d * math.cos(ang), d * math.sin(ang)
    if all(math.hypot(x - a, y - b) > 50 for a, b, _ in POP):
        POP.append((x, y, _R.uniform(0, 6.3)))
    if len(POP) == 40:
        break
MUTANTS = {5, 17, 31}


def population(c, t, tl, phase):
    """The infection in the microscope. phase: 'all', 'mark', 'hit', 'kill', 'regrow'."""
    A = tl.at
    for i, (x, y, rot) in enumerate(POP):
        mut = i in MUTANTS
        col = MUTANT if mut and phase != "all" else GERM
        burst = 0.0
        if phase in ("kill", "regrow") and not mut:
            t0 = A("b10", "kills") + 0.04 * (i % 12) if phase == "kill" else -1
            burst = 1.0 if phase == "regrow" else seg(t, t0, t0 + 0.35)
        shield = 1.0 if (mut and phase in ("regrow",)) else 0.0
        bacterium(c, x, y, 0.62, rot, col, shield=shield, burst=burst, t=t + i)
    if phase == "regrow":
        t0 = A("b11", "multiply")
        for i, (x, y, rot) in enumerate(POP):
            if i in MUTANTS:
                continue
            a = appear(t, t0 + 0.06 * i)
            if a > 0:
                bacterium(c, x, y, 0.62 * a, rot + 1, MUTANT, shield=seg(t, A("b11", "shield"), A("b11", "shield") + 0.3),
                          t=t + i)


# ================================================================ shots
def B1(cr, t, tl, bid):
    A = tl.at
    finger(cr, 330, 720, 1.05, ease_out(seg(t, A(bid, "kill") - 0.6, A(bid, "kill") + 1.2)))
    circle_mark(cr, t, A(bid, "cut") + 0.1, 440, 720, 90, 70)


def B2(cr, t, tl, bid):
    A = tl.at
    tm = A(bid, "mould")
    petri(cr, 360, 760, 250, t, 1.0, clear=ease_out(seg(t, A(bid, "kills") - 0.2, A(bid, "kills") + 1.0)),
          mould=ease_out(seg(t, tm - 0.2, tm + 0.6)))
    a = appear(t, A(bid, "1928") - 0.1)
    if a > 0:
        with place(cr, 560, 1080, a, 0.06):
            P.card(cr, -110, -46, 220, 84, hexc("#efe6d2"), torn=True, seed=8)
            text(cr, "1928", 0, 22, 62, RED, align="center")
    if t > A(bid, "kills"):
        text(cr, "MOULD", 360, 1060, 22, INK, P.FONT_MONO, align="center", spacing=3)


def B3(cr, t, tl, bid):
    A = tl.at
    petri(cr, 360, 760, 250, t, 1.0, clear=1.0, mould=1.0, regrow=ease_out(seg(t, A(bid, "fighting") - 0.3,
                                                                             A(bid, "fighting") + 0.9)))
    if t > A(bid, "back"):
        stamp(cr, t, A(bid, "back"), "RESISTANT", 360, 1080, -0.08, size=56)


def B4(cr, t, tl, bid):
    A = tl.at
    def mp(c):
        P.world(c, 360, 560, 660, hexc("#d9ccaa"), edge=hexc("#8d7b58"), lw=1)
    with_shadow(cr, mp, 3, 6, 0.2)
    r = np.random.default_rng(6)
    t0 = A(bid, "killed")
    for i in range(60):
        u = seg(t, t0 + i * 0.02, t0 + i * 0.02 + 0.3)
        if u > 0:
            px, py = 360 + r.uniform(-300, 300), 560 + r.uniform(-120, 140)
            cr.arc(px, py, 6 * u, 0, 6.3)
            fill(cr, RED, 0.8)
    flip_counter(cr, t, A(bid, "million") - 0.6, "1,140,000", 360, 930, 92, 1.2, unit="DEATHS IN 2021 · DIRECTLY")


def B5(cr, t, tl, bid):
    A = tl.at
    t0 = A(bid, "five")
    flip_counter(cr, t, -10, "1,140,000", 360, 560, 80, 0.01, unit="DIRECTLY")
    a = appear(t, t0 - 0.3)
    if a > 0:
        with place(cr, 360, 900, a):
            flip_counter(cr, t, t0 - 0.3, "4,710,000", 0, 0, 92, 1.0, unit="LINKED DEATHS · 2021")
    arrow(cr, 360, 700, 360, 790, seg(t, t0 - 0.6, t0 - 0.3))


def B6(cr, t, tl, bid):
    A = tl.at
    ts = A(bid, "superbugs")
    a = appear(t, tl.by_id[bid].start)
    bacterium(cr, 360, 760, 3.0 * a, -0.15, MUTANT, shield=appear(t, ts), t=t)
    if t > A(bid, "medicine") - 0.3:
        capsule(cr, 560, 520, appear(t, A(bid, "medicine") - 0.3), -0.5)
        text(cr, "?", 600, 450, 80, RED, alpha=appear(t, A(bid, "medicine")))


def B7(cr, t, tl, bid):
    P.microscope(cr, 360, 760, 260, lambda c: population(c, t, tl, "all"), tint=hexc("#eef0dc"))
    text(cr, "ONE INFECTION, UP CLOSE", 360, 1100, 18, P.TONES["teal"][1], P.FONT_MONO, align="center", spacing=2,
         alpha=0.75)


def B8(cr, t, tl, bid):
    A = tl.at
    td = A(bid, "different")
    P.microscope(cr, 360, 760, 260, lambda c: population(c, t, tl, "mark" if t > td - 0.4 else "all"),
                 tint=hexc("#eef0dc"))
    for k, i in enumerate(sorted(MUTANTS)):
        x, y, _ = POP[i]
        circle_mark(cr, t, td + 0.1 * k, 360 + x, 760 + y, 44, 34, lw=5)


def B9(cr, t, tl, bid):
    A = tl.at
    th = A(bid, "hits")
    P.microscope(cr, 360, 760, 260, lambda c: population(c, t, tl, "mark"), tint=hexc("#eef0dc"))
    u = seg(t, tl.by_id[bid].start, th)
    if u < 1:
        capsule(cr, 360, lerp(380, 700, ease_out(u)), 1.2, 0.5)
    if t > th:
        w = seg(t, th, th + 0.8)
        cr.arc(360, 760, 260 * w, 0, 6.3)
        stroke(cr, hexc("#f2f2f2"), 14, 1 - w)
        cue("hit", t, th)


def B10(cr, t, tl, bid):
    P.microscope(cr, 360, 760, 260, lambda c: population(c, t, tl, "kill"), tint=hexc("#eef0dc"))


def B11(cr, t, tl, bid):
    P.microscope(cr, 360, 760, 260, lambda c: population(c, t, tl, "regrow"), tint=hexc("#eef0dc"))


def B12(cr, t, tl, bid):
    A = tl.at
    tl_ = A(bid, "loops")
    bacterium(cr, 200, 760, 2.4, 0.1, MUTANT, shield=1.0, t=t)
    th = A(bid, "other")
    bacterium(cr, 530, 820, 2.4, -0.1, GERM, shield=seg(t, th + 1.6, th + 1.9), t=t + 3)
    u = ease_out(seg(t, th, th + 1.6))
    if t > tl_ - 0.6 or u > 0:
        px, py = lerp(220, 520, u), lerp(760, 820, u) - 120 * math.sin(math.pi * u)
        plasmid(cr, px, py, 34, appear(t, min(th, tl_) - 0.2), t * 2)
    if t > tl_:
        a = appear(t, tl_)
        with place(cr, 360, 1050, a, -0.04):
            P.card(cr, -170, -40, 340, 72, hexc("#efe6d2"), torn=True, seed=5)
            text(cr, "PLASMID (DNA LOOP)", 0, 12, 30, INK, align="center")


def B13(cr, t, tl, bid):
    A = tl.at
    tk = A(bid, "kinds")
    bacterium(cr, 200, 700, 2.0, 0.1, MUTANT, shield=1.0, t=t)
    coccus(cr, 520, 760, 56, shield=seg(t, tk + 0.6, tk + 0.9))
    u = ease_out(seg(t, tk - 0.6, tk + 0.6))
    plasmid(cr, lerp(220, 520, u), lerp(700, 760, u) - 100 * math.sin(math.pi * u), 30, 1, t * 2)
    text(cr, "ROD-SHAPED", 200, 840, 22, INK, P.FONT_MONO, align="center", spacing=2)
    text(cr, "ROUND", 520, 860, 22, INK, P.FONT_MONO, align="center", spacing=2)


def B14(cr, t, tl, bid):
    A = tl.at
    def frame_(c):
        P.card(c, 150, 400, 300, 380, hexc("#e9e0c9"))
        c.rectangle(170, 420, 260, 300)
        fill(c, hexc("#b7a98a"))
        c.arc(300, 530, 62, 0, 6.3)        # an anonymous paper silhouette, not a likeness
        fill(c, hexc("#5a4c3a"))
        curve(c, [(200, 720), (220, 630), (300, 600), (380, 630), (400, 720)], close=True)
        fill(c, hexc("#5a4c3a"))
        text(c, "THE DISCOVERER", 300, 760, 18, INK, P.FONT_MONO, align="center", spacing=2)
    with_shadow(cr, frame_, 6, 10, 0.3)
    a = appear(t, A(bid, "penicillin") - 0.2)
    if a > 0:
        medal(cr, 520, 820, a)
    if t > A(bid, "coming"):
        stamp(cr, t, A(bid, "coming"), "WARNING", 360, 1060, -0.08, size=56)


def B15(cr, t, tl, bid):
    A = tl.at
    tt = A(bid, "little")
    def card_(c):
        P.card(c, 70, 420, 580, 420, hexc("#f4eedc"))
        text(c, "NOBEL LECTURE · 1945", 110, 480, 20, INK, P.FONT_MONO, spacing=2, alpha=0.8)
        lines = ["Too little of the drug", "can make the microbes", "resistant."]
        for k, s in enumerate(lines):
            text(c, s, 110, 580 + k * 70, 34, INK, P.FONT_MONO, alpha=seg(t, tt - 0.6 + 0.4 * k, tt - 0.2 + 0.4 * k))
        text(c, "(his warning, in short)", 110, 800, 18, INK, P.FONT_MONO, alpha=0.6)
    with_shadow(cr, card_, 6, 10, 0.3)
    if t > A(bid, "resist"):
        c0 = A(bid, "resist")
        cr.move_to(110, 590 + 2 * 70 + 10)
        cr.line_to(lerp(110, 330, seg(t, c0, c0 + 0.3)), 590 + 2 * 70 + 10)
        stroke(cr, RED, 6)
    medal(cr, 560, 1000, 0.8)


def B16(cr, t, tl, bid):
    A = tl.at
    tb, tba = A(bid, "body"), A(bid, "bacteria", nth=1)
    a = appear(t, tb - 0.3)
    if a > 0:
        paper_person(cr, 210, 1000, 1.2 * a)
        red_x(cr, t, A(bid, "resistant"), 210, 720, 110, 14)
    a2 = appear(t, tba - 0.2)
    if a2 > 0:
        bacterium(cr, 520, 720, 2.0 * a2, -0.2, MUTANT, shield=1.0, t=t)
        tick(cr, t, tba + 0.3, 520, 880, 50, lw=12)


def B17(cr, t, tl, bid):
    A = tl.at
    tissue_box(cr, 200, 560, 1.0)
    thermometer(cr, 480, 600, 1.0, 0.75)
    tv = A(bid, "viruses")
    a = appear(t, tv - 0.3)
    if a > 0:
        virus(cr, 360, 900, 80 * a, rot=t * 0.4)
    tc = A(bid, "nothing")
    u = seg(t, tc - 0.3, tc + 1.2)
    if 0 < u < 1:
        cx = lerp(80, 300, min(1, u * 1.6))
        cy = 900 - 160 * math.sin(math.pi * u)
        capsule(cr, cx - (u > 0.62) * (u - 0.62) * 400, cy, 0.8, u * 6)
    text(cr, "VIRUS", 360, 1060, 24, INK, P.FONT_MONO, align="center", spacing=3, alpha=a)


def B18(cr, t, tl, bid):
    for k, (x, y) in enumerate(((200, 620), (520, 640), (360, 920))):
        lift = 18 * math.sin(t * 5 + k)
        bacterium(cr, x, y, 1.6, 0, MUTANT, t=t + k)
        dumbbell(cr, x, y - 60 - lift, 1.2)
        for sx in (-30, 30):
            cr.move_to(x + sx, y - 20)
            cr.line_to(x + sx * 1.2, y - 60 - lift)
            stroke(cr, shade(MUTANT, 0.6), 4)
    A = tl.at
    if t > A(bid, "free"):
        stamp(cr, t, A(bid, "free"), "FREE TRAINING", 360, 1100, -0.07, size=50)


def B19(cr, t, tl, bid):
    A = tl.at
    prescription(cr, 150, 420, t, A(bid, "prescribed", nth=1))
    a = appear(t, A(bid, "exactly"))
    if a > 0:
        capsule(cr, 560, 1040, a, -0.3)


def B20(cr, t, tl, bid):
    A = tl.at
    ts, tl_ = A(bid, "share"), A(bid, "leftovers")
    paper_person(cr, 160, 760, 0.8)
    paper_person(cr, 560, 760, 0.8, hexc("#e7d7b4"))
    a = appear(t, ts - 0.3)
    if a > 0:
        capsule(cr, lerp(240, 470, ease_out(seg(t, ts - 0.3, ts + 0.5))), 560, 0.8)
        red_x(cr, t, ts + 0.2, 360, 560, 80, 12)
    a2 = appear(t, tl_ - 0.3)
    if a2 > 0:
        pill_strip(cr, 360, 940, a2, used=6)
        red_x(cr, t, tl_ + 0.2, 360, 940, 90, 12)


def B21(cr, t, tl, bid):
    A = tl.at
    tn = A(bid, "2050")
    u = seg(t, A(bid, "between"), tn)
    year = int(round(lerp(2025, 2050, u)))
    year_card(cr, 360, 560, str(year))
    flip_counter(cr, t, A(bid, "thirty-nine") - 0.3, "39,000,000", 360, 900, 80, 1.3, unit="DEATHS · 2025-2050 · FORECAST", tone="dark")


def B22(cr, t, tl, bid):
    A = tl.at
    tissue_box(cr, 200, 960, 0.9)
    capsule(cr, 480, 960, 1.0, -0.4)
    a = appear(t, A(bid, "honest") - 0.2)
    if a > 0:
        with place(cr, 360, 560, a):
            P.comment_bubble(cr, -280, -80, 560, 150, "FOR A COLD? BE HONEST")


SHOTS = {
    "b1": Shot(B1, "HOOK", 1, "cream", "A TINY CUT", "COULD KILL", "kill"),
    "b2": Shot(B2, "1928", 2, "khaki", "THEN CAME", "PENICILLIN", "mould"),
    "b3": Shot(B3, "HOOK", 3, "khaki", "THEY'RE", "FIGHTING BACK", "fighting"),
    "b4": Shot(B4, "THE WORLD", 1, "cream", "2021", "1,140,000", "million"),
    "b5": Shot(B5, "THE WORLD", 2, "cream", "NEARLY", "5 MILLION", "five"),
    "b6": Shot(B6, "SUPERBUGS", 1, "mint", "HOW DO GERMS", "BEAT MEDICINE?", "medicine"),
    "b7": Shot(B7, "INSIDE", 1, "teal", "BILLIONS", "OF THEM", "billions"),
    "b8": Shot(B8, "INSIDE", 2, "teal", "A FEW ARE", "DIFFERENT", "different"),
    "b9": Shot(B9, "THE DRUG", 1, "teal", "THE DRUG", "HITS", "hits"),
    "b10": Shot(B10, "THE DRUG", 2, "teal", "ALMOST", "ALL", "all"),
    "b11": Shot(B11, "SURVIVORS", 1, "teal", "THE SURVIVORS", "TAKE OVER", "whole"),
    "b12": Shot(B12, "SURVIVORS", 2, "mint", "THEY", "SHARE IT", "pass"),
    "b13": Shot(B13, "SURVIVORS", 3, "mint", "EVEN TO", "STRANGERS", "different"),
    "b14": Shot(B14, "1945", 1, "khaki", "HE", "WARNED US", "coming"),
    "b15": Shot(B15, "1945", 2, "khaki", "TOO LITTLE", "TEACHES THEM", "teach"),
    "b16": Shot(B16, "MYTHS", 1, "cream", "NOT YOU.", "THE BACTERIA.", "bacteria"),
    "b17": Shot(B17, "MYTHS", 2, "mint", "COLD? FLU?", "VIRUSES.", "viruses"),
    "b18": Shot(B18, "MYTHS", 3, "khaki", "FREE", "TRAINING", "training"),
    "b19": Shot(B19, "WHAT TO DO", 1, "mint", "ONLY WHEN", "PRESCRIBED", "prescribes"),
    "b20": Shot(B20, "WHAT TO DO", 2, "mint", "NO SHARING", "NO LEFTOVERS", "leftovers"),
    "b21": Shot(B21, "2050", 1, "dark", "BY 2050", "39 MILLION", "thirty-nine"),
    "b22": Shot(B22, "END", 1, "cream", "BE", "HONEST", "honest"),
}
