"""Shots for videos/malaria.py: our own drawings (mosquito, liver, parasites, red cells, props)."""
import math

import numpy as np

from motion import paper as P
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg, smooth
from motion.paper import (INK, RED, Shot, appear, circle_mark, curve, fill, flip_counter, place, poly, rrect, shade,
                          slide, stamp, stroke, text, tick, red_x, with_shadow)
from videos.snakebite_shots import _bez, arrow, body_outline, night_room
from videos.superbugs_shots import medal, paper_person, thermometer

PARA = hexc("#7a4fb0")
LIVER = hexc("#9a3f30")
SKIN = hexc("#e7b98f")
BONE = hexc("#f2ead8")


# ================================================================ drawings
def mosquito(cr, x, y, s=1.0, rot=0.0, t=0.0, fed=0.0, flap=True, female=True):
    """An Anopheles mosquito, side view, facing left (x, y = the tip of its proboscis)."""
    with place(cr, x, y, s, rot):
        def d(c):
            # legs
            for k, (lx, ly) in enumerate(((120, -40), (140, -36), (160, -34))):
                c.move_to(lx, ly)
                c.line_to(lx - 40 + k * 30, ly + 60)
                c.line_to(lx - 70 + k * 50, ly + 110)
                stroke(c, hexc("#3a2e26"), 2.2)
            # abdomen (raised, Anopheles rests tail-up)
            curve(c, [(160, -50), (220, -84), (290, -120), (300, -110), (230, -62), (170, -36)], close=True)
            col = hexc("#7a6050") if fed <= 0 else tuple(lerp(hexc("#7a6050")[k], hexc("#b8322a")[k], fed) for k in range(3))
            fill(c, col)
            for k in range(5):
                bx = 185 + k * 22
                c.move_to(bx, -52 - k * 13)
                c.line_to(bx + 6, -36 - k * 12)
                stroke(c, hexc("#3a2e26"), 1.5, 0.6)
            # thorax + head
            c.save()
            c.translate(140, -48)
            c.scale(1.2, 0.9)
            c.arc(0, 0, 22, 0, 6.3)
            c.restore()
            fill(c, hexc("#5a4638"))
            c.arc(106, -48, 13, 0, 6.3)
            fill(c, hexc("#3a2e26"))
            c.arc(101, -52, 4, 0, 6.3)
            fill(c, hexc("#120d0a"))
            # proboscis + palps + antennae
            c.move_to(94, -46)
            c.line_to(0, 0)
            stroke(c, hexc("#2a201a"), 2.4)
            c.move_to(96, -52)
            c.line_to(30, -30)
            stroke(c, hexc("#2a201a"), 1.6)
            for k in range(2):
                c.move_to(100, -58)
                c.line_to(70 - k * 8, -96 + k * 6)
                stroke(c, hexc("#2a201a"), 1.4)
        with_shadow(cr, d, 5, 9, 0.25)
        # wings
        ang = 0.25 * math.sin(t * 60) if flap else 0.1
        for k in (0, 1):
            with place(cr, 150, -64, 1, -0.5 + ang * (1 if k else -1)):
                cr.save()
                cr.scale(1, 0.32)
                cr.arc(70, 0, 72, 0, 6.3)
                cr.restore()
                cr.set_source_rgba(0.85, 0.9, 0.95, 0.45)
                cr.fill_preserve()
                stroke(cr, hexc("#6a7a86"), 1.4, 0.8)
                for j in range(3):
                    cr.arc(40 + j * 30, -2, 3, 0, 6.3)
                    fill(cr, hexc("#3a2e26"), 0.6)


def liver(cr, x, y, s=1.0, glow=0.0, col=None):
    """The liver, front view: a big right lobe and a smaller left lobe."""
    col = col or LIVER
    with place(cr, x, y, s):
        def d(c):
            curve(c, [(-190, -40), (-120, -96), (0, -100), (120, -84), (200, -50), (190, -20), (90, 10),
                      (20, 40), (-60, 90), (-150, 80), (-200, 20)], close=True)
            c.set_source(P.rad_grad(-60, -40, 20, 220, [(0, shade(col, 1.25)), (1, shade(col, 0.8))]))
            c.fill()
            c.move_to(10, -98)
            c.curve_to(0, -40, 10, 0, 20, 38)
            stroke(c, shade(col, 0.6), 3)
            curve(c, [(-40, 60), (-20, 30), (10, 40), (0, 80)], close=True)   # gall bladder
            fill(c, hexc("#5f8a4a"))
        with_shadow(cr, d, 6, 9, 0.3)
        if glow > 0:
            cr.arc(-60, -10, 230, 0, 6.3)
            cr.set_source(P.rad_grad(-60, -10, 30, 230, [(0, (1, 0.4, 0.3, 0.45 * glow)), (1, (1, 0.4, 0.3, 0))]))
            cr.fill()


def sporozoite(cr, x, y, s=1.0, rot=0.0, a=1.0, col=None):
    """A thin, curved, worm-like parasite."""
    col = col or PARA
    with place(cr, x, y, s, rot):
        cr.move_to(-26, 6)
        cr.curve_to(-10, -10, 10, -10, 26, 6)
        stroke(cr, shade(col, 0.6), 9, a)
        cr.move_to(-26, 6)
        cr.curve_to(-10, -10, 10, -10, 26, 6)
        stroke(cr, col, 6, a)
        cr.arc(0, -4, 3, 0, 6.3)
        fill(cr, hexc("#e9d6f5"), a)


def merozoite(cr, x, y, r=7, a=1.0):
    cr.arc(x, y, r, 0, 6.3)
    fill(cr, PARA, a)
    cr.arc(x - r * 0.3, y - r * 0.3, r * 0.35, 0, 6.3)
    fill(cr, hexc("#e9d6f5"), a)


def big_cell(cr, x, y, r, swell=0.0, n=0, t=0.0, burst=0.0, col=None, spread=2.5, drop=0.0):
    """A liver cell (or red cell) filling with `n` parasites; `burst` 0..1 splits it open."""
    col = col or hexc("#c98a6a")
    R = r * (1 + 0.25 * swell)
    r_ = np.random.default_rng(int(r))
    pts = [(r_.uniform(0, 6.3), r_.uniform(0, 1) ** 0.5) for _ in range(max(n, 1))]
    if burst < 1:
        a = 1 - burst
        cr.arc(x, y, R, 0, 6.3)
        cr.set_source(P.rad_grad(x - R * 0.3, y - R * 0.3, R * 0.1, R, [(0, (*shade(col, 1.2)[:3], a)),
                                                                        (1, (*shade(col, 0.85)[:3], a))]))
        cr.fill()
        cr.arc(x, y, R, 0, 6.3)
        stroke(cr, shade(col, 0.6), 3, a)
        if burst > 0:
            for k in range(7):
                ang = k * 0.9
                cr.move_to(x + R * math.cos(ang), y + R * math.sin(ang))
                cr.line_to(x + R * 0.6 * math.cos(ang + 0.2), y + R * 0.6 * math.sin(ang + 0.2))
                stroke(cr, hexc("#3a2018"), 3, a)
    for i, (ang, d) in enumerate(pts[:n]):
        dd = d * R * 0.8 * (1 + spread * ease_out(burst))
        merozoite(cr, x + dd * math.cos(ang + t * 0.1), y + dd * math.sin(ang + t * 0.1) + drop * ease_out(burst),
                  6 if n > 30 else 8)


def calendar(cr, x, y, day, s=1.0, flip=0.0):
    with place(cr, x, y, s):
        def d(c):
            P.card(c, -120, -110, 240, 230, hexc("#f4eedc"))
            c.rectangle(-120, -110, 240, 56)
            fill(c, RED)
            for hx in (-70, 0, 70):
                c.arc(hx, -110, 7, 0, 6.3)
                fill(c, hexc("#3a3a3a"))
            text(c, "DAY", 0, -70, 26, hexc("#ffffff"), P.FONT_MONO, align="center", spacing=4)
            text(c, str(day), 0, 80, 110, INK, align="center")
        with_shadow(cr, d, 5, 8, 0.3)
        if flip > 0:   # the old page lifting away
            with place(cr, 0, -110, 1, -1.2 * flip):
                P.card(cr, -120, 0, 240, 230 * (1 - flip), hexc("#efe7d2"))


def health_card(cr, x, y, t, starts):
    def d(c):
        P.card(c, x, y, 440, 400, hexc("#efe7d2"))
        c.rectangle(x, y, 440, 64)
        fill(c, hexc("#3f7a5a"))
        text(c, "HEALTH REPORT", x + 26, y + 44, 30, hexc("#ffffff"))
        text(c, "NAME: YOU", x + 26, y + 112, 20, INK, P.FONT_MONO)
        for k, s in enumerate(("FEVER", "ENERGY", "APPETITE")):
            text(c, s, x + 26, y + 190 + k * 70, 34, INK)
            c.move_to(x + 26, y + 206 + k * 70)
            c.line_to(x + 414, y + 206 + k * 70)
            stroke(c, INK, 1, 0.3)
    with_shadow(cr, d, 6, 10, 0.3)
    for k, st in enumerate(starts):
        stamp(cr, t, st, "NORMAL", x + 320, y + 178 + k * 70, -0.1, col=hexc("#2f7a48"), size=30)


def old_microscope(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            poly(c, [(-110, 0), (110, 0), (90, -30), (-90, -30)])
            fill(c, hexc("#3a3028"))
            c.move_to(40, -30)
            c.curve_to(110, -120, 100, -220, 40, -260)
            stroke(c, hexc("#4a3a2a"), 22)
            with place(c, -10, -200, 1, 0.45):
                rrect(c, -24, -110, 48, 200, 8)
                c.set_source(P.lin_grad(-24, 0, 24, 0, [(0, hexc("#9c7a3a")), (0.5, hexc("#e6c878")),
                                                        (1, hexc("#8a6a2a"))]))
                c.fill()
                rrect(c, -30, -130, 60, 30, 6)
                fill(c, hexc("#3a3028"))
            c.rectangle(-80, -110, 130, 14)
            fill(c, hexc("#5a4a3a"))
        with_shadow(cr, d, 6, 9, 0.3)


def notebook(cr, x, y, t, t_write):
    def d(c):
        P.card(c, x, y, 330, 400, hexc("#ece2c4"))
        for k in range(9):
            c.move_to(x + 20, y + 80 + k * 36)
            c.line_to(x + 310, y + 80 + k * 36)
            stroke(c, hexc("#8aa0b8"), 1, 0.5)
        text(c, "20 AUG 1897", x + 30, y + 58, 30, INK, P.FONT_MONO)
    with_shadow(cr, d, 6, 9, 0.3)
    u = seg(t, t_write, t_write + 1.2)
    for k in range(5):
        wl = 250 * min(1, max(0, u * 5 - k))
        if wl > 0:
            cr.move_to(x + 30, y + 108 + k * 36)
            for j in range(int(wl / 6)):
                cr.line_to(x + 30 + j * 6, y + 108 + k * 36 + 3 * math.sin(j * 1.7 + k))
            stroke(cr, hexc("#2a3a6a"), 1.8, 0.8)
    with place(cr, x + 250, y + 330, 0.5, -0.5):
        mosquito(cr, 0, 0, 1, 0, flap=False)


def bed_net(cr, x, y, w, h, u):
    """A mosquito net dropping over a bed (u 0..1)."""
    top = y - h
    yy = lerp(top - 300, top, ease_out(u))
    poly(cr, [(x - w / 2 + 30, yy), (x + w / 2 - 30, yy), (x + w / 2, yy + h), (x - w / 2, yy + h)])
    cr.set_source_rgba(0.95, 0.96, 0.98, 0.28)
    cr.fill()
    for k in range(0, int(w) + 1, 18):
        cr.move_to(x - w / 2 + 30 + (w - 60) * k / w, yy)
        cr.line_to(x - w / 2 + k, yy + h)
        stroke(cr, (1, 1, 1), 1, 0.35)
    for k in range(0, int(h) + 1, 18):
        f = k / h
        cr.move_to(lerp(x - w / 2 + 30, x - w / 2, f), yy + k)
        cr.line_to(lerp(x + w / 2 - 30, x + w / 2, f), yy + k)
        stroke(cr, (1, 1, 1), 1, 0.35)


def arm_skin(cr, x, y, s=1.0):
    with place(cr, x, y, s):
        def d(c):
            curve(c, [(-380, -80), (380, -90), (380, 90), (-380, 80)], close=True)
            c.set_source(P.lin_grad(0, -90, 0, 90, [(0, hexc("#efc39b")), (0.6, SKIN), (1, hexc("#c08b63"))]))
            c.fill()
        with_shadow(cr, d, 6, 10, 0.3)


def is_africa(ring):
    lon = sum(p[0] for p in ring) / len(ring)
    lat = sum(p[1] for p in ring) / len(ring)
    return -18 <= lon <= 51 and -36 <= lat <= 37.5 and not (lon > 34 and lat > 12) and not (lat > 30 and lon > 12)


# ================================================================ shots
def M1(cr, t, tl, bid):
    A = tl.at
    tb, tl_ = A(bid, "bite"), A(bid, "liver")
    arm_skin(cr, 360, 560, 1.0)
    u = ease_out(seg(t, tl.by_id[bid].start, tb))
    mosquito(cr, lerp(700, 380, u), lerp(380, 520, u), 0.95, 0.15 * (1 - u), t, fed=seg(t, tb, tb + 1.5),
             flap=u < 1)
    a = appear(t, tl_ - 0.3)
    if a > 0:
        liver(cr, 360, 940, 0.95 * a, glow=0.5 + 0.5 * math.sin(t * 6))
        text(cr, "YOUR LIVER", 360, 1100, 22, INK, P.FONT_MONO, align="center", spacing=3)


def M2(cr, t, tl, bid):
    A = tl.at
    b = tl.by_id[bid]
    k = int(seg(t, b.start, b.end) * 6.99)
    days = [1, 2, 3, 4, 5, 6, 7]
    calendar(cr, 200, 560, days[k], 0.9)
    health_card(cr, 220, 720, t, [A(bid, "fine") - 0.3 + 0.25 * j for j in range(3)])


def M3(cr, t, tl, bid):
    A = tl.at
    ta = A(bid, "again", nth=1)
    def slide_(c):
        r = np.random.default_rng(4)
        for i in range(16):
            ang, d = r.uniform(0, 6.3), r.uniform(0, 1) ** 0.5 * 190
            x, y = d * math.cos(ang), d * math.sin(ang)
            tb = ta - 0.8 + (i % 8) * 0.25 + (0.9 if i >= 8 else 0)
            burst = seg(t, tb, tb + 0.4)
            if burst < 1:
                big_cell(c, x, y, 30, swell=seg(t, tb - 0.6, tb), n=6, t=t, burst=burst, col=hexc("#c8322d"))
            else:
                for k in range(6):
                    merozoite(c, x + 40 * math.cos(k) * min(1, burst), y + 40 * math.sin(k), 6)
    P.microscope(cr, 360, 760, 260, slide_, tint=hexc("#f3d0c4"))


def M4(cr, t, tl, bid):
    A = tl.at
    def mp(c):
        P.world(c, 360, 560, 660, hexc("#5a5048"), edge=hexc("#8a7d6c"), lw=1)
    mp(cr)
    flip_counter(cr, t, A(bid, "two") - 0.3, "282,000,000", 360, 930, 76, 1.3, unit="MALARIA CASES · 2024", tone="dark")


def M5(cr, t, tl, bid):
    A = tl.at
    ta = A(bid, "africa")
    k = 660 / 360
    def P_(lon, lat):
        return 360 + lon * k, 560 - (lat - 12) * k
    for ring in P._map("world"):
        poly(cr, [P_(*p) for p in ring])
        af = is_africa(ring)
        fill(cr, RED if (af and t > ta - 0.2) else hexc("#5a5048"), 1.0)
    flip_counter(cr, t, A(bid, "six") - 0.3, "610,000", 360, 930, 90, 1.1, unit="DEATHS · 2024", tone="dark")
    a = appear(t, A(bid, "children"))
    if a > 0:
        with place(cr, 520, 760, a, -0.05):
            P.card(cr, -150, -36, 300, 64, hexc("#efe6d2"), torn=True, seed=4)
            text(cr, "MOSTLY UNDER 5", 0, 14, 34, INK, align="center")


def M6(cr, t, tl, bid):
    A = tl.at
    def slide_(c):
        for k in range(5):
            sporozoite(c, -140 + k * 70, -60 + 50 * math.sin(k * 1.7 + t), 2.0, 0.4 * math.sin(k + t * 0.8))
    P.microscope(cr, 360, 810, 230, slide_, tint=hexc("#eef0dc"))
    a = appear(t, A(bid, "parasite"))
    if a > 0:
        with place(cr, 470, 1060, a, -0.05):
            P.card(cr, -150, -36, 300, 64, hexc("#efe6d2"), torn=True, seed=9)
            text(cr, "PLASMODIUM", 0, 14, 36, INK, align="center")
    for k, w in enumerate(("virus", "bacterium")):
        a2 = appear(t, A(bid, w))
        if a2 > 0 and t < A(bid, "parasite"):
            with place(cr, 200 + 320 * k, 470, a2):
                P.card(cr, -110, -36, 220, 64, hexc("#efe6d2"), torn=True, seed=k)
                text(cr, w.upper(), 0, 14, 34, INK, align="center")
            red_x(cr, t, A(bid, w) + 0.3, 200 + 320 * k, 470, 50, 9)


def M7(cr, t, tl, bid):
    A = tl.at
    def card_(c, x, y, female):
        P.card(c, x - 150, y - 140, 300, 280, hexc("#ece3cb"))
    with_shadow(cr, lambda c: card_(c, 200, 620, False), 5, 8, 0.3)
    with_shadow(cr, lambda c: card_(c, 520, 620, True), 5, 8, 0.3)
    mosquito(cr, 120, 650, 0.6, 0, t, flap=False)
    mosquito(cr, 440, 650, 0.6, 0, t, flap=False, fed=seg(t, A(bid, "blood"), A(bid, "blood") + 1))
    text(cr, "MALE", 200, 740, 34, INK, align="center")
    text(cr, "FEMALE", 520, 740, 34, RED, align="center")
    red_x(cr, t, A(bid, "female") + 0.2, 200, 610, 80, 10)
    a = appear(t, A(bid, "eggs") - 0.2)
    if a > 0:
        with place(cr, 520, 940, a):
            for k in range(9):
                cr.save()
                cr.translate(-80 + k * 20, 0)
                cr.scale(0.6, 1)
                cr.arc(0, 0, 12, 0, 6.3)
                cr.restore()
                fill(cr, hexc("#3a3028"))
            text(cr, "EGGS", 0, 70, 30, INK, P.FONT_MONO, align="center", spacing=3)


def M8(cr, t, tl, bid):
    A = tl.at
    tb, tp = A(bid, "bites"), A(bid, "parasites")
    cr.rectangle(0, 760, W, 520)        # skin cross-section
    cr.set_source(P.lin_grad(0, 760, 0, 1280, [(0, SKIN), (0.25, hexc("#d99a7a")), (1, hexc("#c06a5a"))]))
    cr.fill()
    cr.move_to(0, 1000)
    cr.curve_to(240, 960, 480, 1040, 720, 990)
    cr.line_to(720, 1040)
    cr.curve_to(480, 1090, 240, 1010, 0, 1050)
    cr.close_path()
    fill(cr, hexc("#b8322a"))
    text(cr, "BLOOD VESSEL", 600, 1100, 18, hexc("#ffffff"), P.FONT_MONO, align="center", spacing=2)
    u = ease_out(seg(t, tl.by_id[bid].start, tb))
    mosquito(cr, lerp(560, 360, u), lerp(560, 770, u), 1.1, 0.35, t, flap=u < 1)
    for i in range(10):
        st = tp - 0.2 + i * 0.12
        v = seg(t, st, st + 1.0)
        if 0 < v:
            px = 360 + 40 * math.sin(i * 1.3) + v * 140 * math.cos(i)
            py = lerp(780, 1010, min(1, v * 1.3))
            sporozoite(cr, px, py, 0.9, 1.4 + 0.3 * math.sin(i + t * 3))


def M9(cr, t, tl, bid):
    A = tl.at
    th = A(bid, "hide")
    body_outline(cr, 360, 760, 0.78)
    with place(cr, 360, 760, 0.78):
        liver(cr, -40, -200, 0.32, glow=seg(t, A(bid, "liver"), A(bid, "liver") + 0.5))
        route = [(-125, -150), (-110, -230), (-80, -290), (-30, -280), (-40, -220)]
        u = seg(t, tl.by_id[bid].start, A(bid, "liver"))
        for k in range(30):
            v = k / 29
            if v <= u:
                px, py = _bez(route, v)
                cr.arc(px, py, 4, 0, 6.3)
                fill(cr, hexc("#e9d6f5"), 0.9)
    a = appear(t, th - 0.2)
    if a > 0:
        with place(cr, 530, 1010, a):
            def d(c):
                c.arc(0, 0, 120, 0, 6.3)
                fill(c, hexc("#efe6d2"))
            with_shadow(cr, d, 5, 8, 0.3)
            for k in range(3):
                big_cell(cr, -50 + k * 50, 10 * math.sin(k * 2), 36, n=1, t=t, col=hexc("#c98a6a"))
            text(cr, "LIVER CELLS", 0, 100, 18, INK, P.FONT_MONO, align="center", spacing=2)


def M10(cr, t, tl, bid):
    A = tl.at
    tm = A(bid, "multiplies")
    n = int(lerp(1, 60, ease_out(seg(t, tm - 0.4, tm + 1.6))))
    big_cell(cr, 360, 760, 220, swell=seg(t, tm, tm + 2.0) * 0.6, n=n, t=t)
    text(cr, "ONE LIVER CELL", 360, 1110, 20, INK, P.FONT_MONO, align="center", spacing=3)


def M11(cr, t, tl, bid):
    A = tl.at
    tb, tf = A(bid, "burst"), A(bid, "flood")
    big_cell(cr, 360, 640, 180, swell=0.6, n=60, t=t, burst=seg(t, tb, tb + 1.2), spread=0.5, drop=360)
    if t > tb:
        cue("hit", t, tb)
    a = seg(t, tf - 0.4, tf + 0.6)
    if a > 0:
        cr.rectangle(0, 1000 - 60 * a, W, 220)
        fill(cr, hexc("#b8322a"), a)
        for i in range(24):
            merozoite(cr, 40 + i * 28 + 10 * math.sin(t * 3 + i), 1060 - 40 * math.sin(i * 1.7), 7, a)


def M12(cr, t, tl, bid):
    A = tl.at
    tb, tm, to = A(bid, "breaks"), A(bid, "multiplies"), A(bid, "open")
    def slide_(c):
        u = ease_out(seg(t, tl.by_id[bid].start, tb))
        merozoite(c, lerp(-200, -10, u), lerp(-160, -10, u), 10)
        n = 1 + int(15 * seg(t, tm - 0.2, tm + 1.0))
        big_cell(c, 0, 0, 110, swell=seg(t, tm, to) * 0.4, n=n if t > tb else 0, t=t, burst=seg(t, to, to + 0.5),
                 col=hexc("#c8322d"))
    P.microscope(cr, 360, 760, 260, slide_, tint=hexc("#f3d0c4"))


def M13(cr, t, tl, bid):
    A = tl.at
    td = A(bid, "ten")
    calendar(cr, 190, 560, int(lerp(1, 12, seg(t, tl.by_id[bid].start, td + 0.8))), 0.85)
    thermometer(cr, 560, 640, 1.1, lerp(0.35, 0.9, seg(t, A(bid, "fever") - 0.4, A(bid, "fever") + 0.6)))
    shiver = 4 * math.sin(t * 40) * seg(t, A(bid, "chills") - 0.2, A(bid, "chills"))
    paper_person(cr, 300 + shiver, 1120, 0.85)
    for k, (w, x, y) in enumerate((("fever", 520, 920), ("chills", 520, 990), ("headache", 520, 1060))):
        a = appear(t, A(bid, w))
        if a > 0:
            with place(cr, x, y, a, -0.04):
                P.card(cr, -100, -28, 200, 50, hexc("#efe6d2"), torn=True, seed=k)
                text(cr, w.upper(), 0, 12, 30, RED, align="center")


def M14(cr, t, tl, bid):
    A = tl.at
    tv, tw = A(bid, "sleeping"), A(bid, "wake")
    liver(cr, 340, 700, 1.0)
    a = appear(t, tv - 0.2)
    if a > 0:
        sporozoite(cr, 280, 690, 2.2 * a, 0.1, col=hexc("#9a7ac8"))
        text(cr, "z", 340, 640 - 6 * math.sin(t * 2), 40, BONE)
        text(cr, "z", 365, 610 - 6 * math.sin(t * 2), 28, BONE, alpha=0.7)
    if t > tw - 0.3:
        for k, lbl in enumerate(("WEEKS", "MONTHS", "YEARS")):
            ak = appear(t, lerp(tw - 0.3, A(bid, "years"), k / 2))
            if ak > 0:
                with place(cr, 170 + 190 * k, 1000, ak, -0.05 + 0.05 * k):
                    P.card(cr, -85, -32, 170, 58, hexc("#efe6d2"), torn=True, seed=k + 3)
                    text(cr, lbl, 0, 13, 32, INK, align="center")
        cue("tick", t, A(bid, "wake"))


def M15(cr, t, tl, bid):
    A = tl.at
    Pf = P.india(cr, 360, 720, 600, hexc("#e8dcbc"), edge=hexc("#7d6a4a"), lw=2.5)
    ti = A(bid, "india")
    a = appear(t, ti)
    if a > 0:
        px, py = Pf(78.5, 17.44)
        with place(cr, px, py, a):
            curve(cr, [(0, 0), (-18, -34), (-18, -52), (0, -66), (18, -52), (18, -34)], close=True)
            fill(cr, RED)
            cr.arc(0, -46, 7, 0, 6.3)
            fill(cr, hexc("#ffffff"))
        text(cr, "SECUNDERABAD", px + 30, py + 8, 30, INK, alpha=a)


def M16(cr, t, tl, bid):
    A = tl.at
    old_microscope(cr, 200, 1000, 1.1)
    notebook(cr, 330, 450, t, A(bid, "found"))
    a = appear(t, A(bid, "ronald"))
    if a > 0:
        with place(cr, 250, 840, a, -0.05):
            P.card(cr, -150, -36, 300, 64, hexc("#efe6d2"), torn=True, seed=12)
            text(cr, "DR RONALD ROSS", 0, 14, 36, INK, align="center")
    tn = A(bid, "nobel")
    a = appear(t, tn - 0.2)
    if a > 0:
        medal(cr, 520, lerp(700, 960, ease_out(seg(t, tn - 0.2, tn + 0.3))), 0.9, year="1902")
        text(cr, "NOBEL PRIZE", 520, 1120, 26, INK, P.FONT_MONO, align="center", spacing=2, alpha=a)


def M17(cr, t, tl, bid):
    A = tl.at
    paper_person(cr, 170, 900, 0.85)
    paper_person(cr, 550, 900, 0.85, hexc("#e7d7b4"))
    arrow(cr, 260, 700, 460, 700, seg(t, A(bid, "person", nth=1), A(bid, "person", nth=2)))
    red_x(cr, t, A(bid, "person", nth=2) + 0.2, 360, 700, 60, 10)
    tm = A(bid, "mosquito")
    a = appear(t, tm - 0.3)
    if a > 0:
        mosquito(cr, 300, 1020, 0.7 * a, 0, t)
        circle_mark(cr, t, tm + 0.1, 400, 990, 150, 80)


def M18(cr, t, tl, bid):
    A = tl.at
    tt = A(bid, "treated")
    def slide_(c):
        rrect(c, 90, 460, 540, 150, 6)
        c.set_source_rgba(0.85, 0.92, 0.95, 0.8)
        c.fill()
        rrect(c, 90, 460, 540, 150, 6)
        stroke(c, hexc("#9ab0b8"), 2)
        c.save()
        c.translate(360, 535)
        c.scale(1.6, 0.6)
        c.arc(0, 0, 70, 0, 6.3)
        c.restore()
        fill(c, hexc("#c8526a"), 0.55)
        text(c, "BLOOD TEST", 140, 500, 18, INK, P.FONT_MONO, spacing=2)
    with_shadow(cr, slide_, 5, 8, 0.25)
    ta = A(bid, "doctor")
    a = appear(t, ta - 0.2)
    if a > 0:
        with place(cr, 360, 820, a, -0.03):
            def card_(c):
                P.card(c, -230, -80, 460, 160, hexc("#f7f3ea"))
                c.rectangle(-230, -80, 26, 160)
                fill(c, RED)
                text(c, "SEE A DOCTOR", 10, 22, 64, INK, align="center")
            with_shadow(cr, card_, 5, 8, 0.3)
    tb = A(bid, "test")
    if t > tb:
        stamp(cr, t, tb + 0.1, "TREATABLE", 360, 1060, -0.08, col=hexc("#2f7a48"), size=56)


def M19(cr, t, tl, bid):
    A = tl.at
    night_room(cr, t)
    bed_net(cr, 320, 1000, 560, 220, seg(t, tl.by_id[bid].start + 0.1, A(bid, "nets") + 0.3))
    tr = A(bid, "repellent")
    u = seg(t, tr - 0.5, tr + 1.2)
    bounce = 1 - abs(1 - 2 * u)
    mosquito(cr, lerp(680, 600, bounce), lerp(700, 820, bounce), 0.55, 0.2, t)


def M20(cr, t, tl, bid):
    A = tl.at
    mosquito(cr, 280, 1000, 0.9, 0.1, t)
    a = appear(t, A(bid, "comments") - 0.2)
    if a > 0:
        with place(cr, 360, 540, a):
            P.comment_bubble(cr, -280, -80, 560, 150, "HAVE YOU HAD IT?")


SHOTS = {
    "m1": Shot(M1, "HOOK", 1, "khaki", "ONE", "BITE", "bite"),
    "m2": Shot(M2, "HOOK", 2, "mint", "YOU FEEL", "FINE", "fine"),
    "m3": Shot(M3, "HOOK", 3, "blood", "AGAIN", "AND AGAIN", "again"),
    "m4": Shot(M4, "THE WORLD", 1, "dark", "2024", "282 MILLION", "million"),
    "m5": Shot(M5, "THE WORLD", 2, "dark", "610,000", "MOSTLY CHILDREN", "children"),
    "m6": Shot(M6, "THE PARASITE", 1, "teal", "IT'S A", "PARASITE", "parasite",
               extra=dict(phases=[("follow", "LET'S FOLLOW", "ITS JOURNEY", "journey")])),
    "m7": Shot(M7, "THE BITE", 1, "khaki", "ONLY", "FEMALES", "female"),
    "m8": Shot(M8, "THE BITE", 2, "cream", "INTO", "YOUR BLOOD", "blood"),
    "m9": Shot(M9, "THE LIVER", 1, "dark", "THEY", "HIDE", "hide"),
    "m10": Shot(M10, "THE LIVER", 2, "cream", "ONE BECOMES", "THOUSANDS", "thousands"),
    "m11": Shot(M11, "THE BLOOD", 1, "cream", "THEN", "THEY BURST", "burst"),
    "m12": Shot(M12, "THE BLOOD", 2, "blood", "INVADE", "AND BURST", "bursts"),
    "m13": Shot(M13, "THE BLOOD", 3, "mint", "DAY 10-15", "FEVER", "fever"),
    "m14": Shot(M14, "THE LIVER", 3, "dark", "IT CAN", "SLEEP", "sleeping"),
    "m15": Shot(M15, "INDIA", 1, "cream", "DISCOVERED", "IN INDIA", "india"),
    "m16": Shot(M16, "1897", 1, "khaki", "SECUNDERABAD", "1897", "1897"),
    "m17": Shot(M17, "MYTHS", 1, "mint", "NOT PERSON", "TO PERSON", "person"),
    "m18": Shot(M18, "WHAT TO DO", 1, "cream", "SEE A", "DOCTOR", "doctor"),
    "m19": Shot(M19, "WHAT TO DO", 2, "night", "STOP", "THE BITE", "nets"),
    "m20": Shot(M20, "END", 1, "khaki", "HAVE YOU", "HAD IT?", "comments"),
}
