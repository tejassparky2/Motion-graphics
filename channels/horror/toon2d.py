"""Illustrated 2D look for the horror channel, drawn in code with pycairo (owner, 25 Oct 2026: not liking the 3D look;
picked "Illustrated 2D, drawn in code" to test). Clean ink outlines, two-tone cel shading with a rim light, painted
light (glows, spills, colour grades), and an original lead character ("you": hoodie, messy hair, big readable eyes).

Shapes are built by path functions so the same outline can be filled, shaded (the part not reached by the key light),
rim-lit (a crescent on the side of a second light) and inked.
"""
import math

import numpy as np

from motion.engine import W, H, cairo, clamp01
from motion.polish import rad

INK = (0.09, 0.07, 0.11, 1)


def mix(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(len(a)))


def hexa(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def curve(cr, pts, closed=True):
    """A smooth Catmull-Rom curve through pts (adds a sub-path; never clears the current path)."""
    n = len(pts)
    cr.move_to(*pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if closed:
        cr.close_path()


def poly(cr, pts):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()


def toon(cr, shape, base, shade=None, light=(-16, -12), rim=None, rim_from=(9, 0), lw=4.5, ink=INK):
    """Fill `shape` (a function adding the outline to the path) with `base`; paint `shade` where the shape moved
    toward the key light no longer covers it; paint `rim` on the side the rim light comes from; ink the outline."""
    cr.save()
    cr.new_path()
    shape(cr)
    cr.clip()
    cr.set_source_rgba(*base)
    cr.paint()
    for col, off in ((shade, light), (rim, (-rim_from[0], -rim_from[1]))):
        if col is None:
            continue
        cr.new_path()
        shape(cr)
        cr.save()
        cr.translate(*off)
        shape(cr)
        cr.restore()
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.set_source_rgba(*col)
        cr.fill()
        cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.restore()
    if lw:
        cr.new_path()
        shape(cr)
        cr.set_source_rgba(*ink)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()


def glow(cr, x, y, r, col, a=1.0, op=cairo.OPERATOR_ADD):
    cr.save()
    cr.set_operator(op)
    cr.set_source(rad(x, y, r, [(0, (*col[:3], a)), (0.35, (*col[:3], a * 0.35)), (1, (*col[:3], 0))]))
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def grade(cr, top, bottom, op=cairo.OPERATOR_MULTIPLY, a=1.0):
    """A full-frame colour grade: a vertical gradient blended over everything (multiply darkens/tints)."""
    cr.save()
    cr.set_operator(op)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *top[:3], a)
    g.add_color_stop_rgba(1, *bottom[:3], a)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def noise(t, s=0.0):
    return math.sin(t * 1.7 + s) * 0.5 + math.sin(t * 3.1 + s * 2.3) * 0.3 + math.sin(t * 7.3 + s * 1.1) * 0.2


# ------------------------------------------------------------------ the lead: "you"
SKIN, SKIN_D = hexa("#c98d62"), hexa("#9c6644")
HAIR, HAIR_D = hexa("#2b1c17"), hexa("#160e0b")
HOOD, HOOD_D, HOOD_L = hexa("#35565e"), hexa("#203840"), hexa("#4d7680")
LIP = hexa("#7a3a34")

FACES = {   # eye opening, iris size, brow raise, brow worry (inner ends up), mouth, mouth open
    "calm":    dict(eye=1.0, iris=1.0, raise_=0.1, worry=0.3, mouth="flat", open=0.0),
    "uneasy":  dict(eye=1.05, iris=0.95, raise_=0.25, worry=0.55, mouth="flat", open=0.0),
    "alarmed": dict(eye=1.3, iris=0.72, raise_=0.6, worry=0.75, mouth="o", open=0.45),
    "terror":  dict(eye=1.45, iris=0.6, raise_=0.85, worry=1.0, mouth="grim", open=0.7),
}


def face_mix(a, b, k):
    A, B = FACES[a], FACES[b]
    out = {key: A[key] + (B[key] - A[key]) * k for key in ("eye", "iris", "raise_", "worry", "open")}
    out["mouth"] = B["mouth"] if k > 0.5 else A["mouth"]
    return out


def you_bust(cr, x, y, s, f, t, look=(0.0, 0.0), turn=0.0, tilt=0.0, breath=1.0, light=(-18, -14), rim=None,
             rim_from=(10, 0), sweat=0.0, tremble=0.0, skin=None, blink=True):
    """The lead from the chest up, facing the camera. (x, y) = the base of the neck; s = scale; f = face dict
    (face_mix); look = where the eyes point (-1..1); turn = head turned left/right (-1..1)."""
    sk = skin or SKIN
    sk_d = mix(sk, SKIN_D, 1.0) if skin is None else mix(sk, (0, 0, 0, 1), 0.3)
    jx = tremble * 2.2 * math.sin(t * 41)
    cr.save()
    cr.translate(x + jx, y)
    cr.scale(s, s)
    up = -4 * breath * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 0.28))     # breathing lifts the shoulders
    # hoodie body
    toon(cr, lambda c: curve(c, [(-62, -12 + up), (-150, 28 + up), (-182, 118), (-196, 430), (196, 430),
                                 (182, 118), (150, 28 + up), (62, -12 + up)]),
         HOOD, HOOD_D, light, rim, rim_from)
    # pocket seam and zip line
    cr.set_source_rgba(*INK[:3], 0.55)
    cr.set_line_width(3)
    curve(cr, [(-110, 300), (-60, 270), (60, 270), (110, 300)], closed=False)
    cr.stroke()
    # neck
    toon(cr, lambda c: poly(c, [(-36, -82), (36, -82), (40, 0), (-40, 0)]), sk, sk_d, (10, 0), None, lw=4)
    # hood roll around the neck, with drawstrings
    toon(cr, lambda c: curve(c, [(-118, -2 + up), (-80, -44 + up), (0, -54 + up), (80, -44 + up), (118, -2 + up),
                                 (86, 36 + up), (0, 18 + up), (-86, 36 + up)]),
         HOOD_L, HOOD_D, light, rim, rim_from)
    for sx in (-1, 1):
        cr.set_source_rgba(*INK)
        cr.set_line_width(5)
        sway = 3 * math.sin(t * 1.4 + sx)
        cr.move_to(sx * 26, 22 + up)
        cr.curve_to(sx * 28, 70 + up, sx * 22 + sway, 110, sx * 24 + sway, 150)
        cr.stroke()
        cr.set_source_rgba(0.82, 0.82, 0.86, 1)
        cr.rectangle(sx * 24 + sway - 5, 148, 10, 18)
        cr.fill()
    # head
    cr.save()
    cr.translate(0, -175)
    cr.rotate(tilt + 0.012 * noise(t * 0.6, 3))
    tx = turn * 16
    head = lambda c: curve(c, [(-100, -10), (-96, -82), (-52, -128), (0, -138), (52, -128), (96, -82), (100, -10),
                               (90, 46), (60, 88), (tx * 0.3, 108), (-60, 88), (-90, 46)])
    for sx in (-1, 1):                                                   # ears
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 96, -22), (sx * 118, -30), (sx * 122, 6), (sx * 104, 22)]),
             sk, sk_d, light, rim, rim_from, lw=4)
    toon(cr, head, sk, sk_d, light, rim, rim_from)
    # cheek shade under the hair line and blush of fear (cold)
    cr.save()
    cr.new_path()
    head(cr)
    cr.clip()
    cr.set_source(rad(tx, 60, 120, [(0, (0, 0, 0, 0)), (1, (0.25, 0.1, 0.12, 0.18))]))
    cr.paint()
    cr.restore()
    cr.save()                                                 # the fringe casts a soft shadow on the forehead
    cr.new_path()
    head(cr)
    cr.clip()
    g = cairo.LinearGradient(0, -80, 0, -25)
    g.add_color_stop_rgba(0, 0.18, 0.08, 0.06, 0.45)
    g.add_color_stop_rgba(1, 0.18, 0.08, 0.06, 0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    # eyes
    blink_k = 0.0
    if blink:
        ph = (t + 0.7) % (4.4 if f["eye"] > 1.2 else 3.2)
        blink_k = math.sin(ph / 0.14 * math.pi) if ph < 0.14 else 0.0
    open_ = f["eye"] * (1 - 0.95 * blink_k)
    for sx in (-1, 1):
        ex, ey = sx * 42 + tx, -8
        rx, ry = 28, 21 * open_
        cr.save()
        cr.translate(ex, ey)
        eye = lambda c: (c.save(), c.scale(1, max(0.05, ry / rx)), c.arc(0, 0, rx, 0, 2 * math.pi), c.restore())
        cr.new_path()
        eye(cr)
        cr.set_source_rgba(0.97, 0.95, 0.92, 1)
        cr.fill_preserve()
        cr.save()
        cr.clip()
        ir = 14 * f["iris"]
        px, py = look[0] * 11, look[1] * 8
        cr.set_source_rgba(*hexa("#4a2c1c"))
        cr.arc(px, py, ir, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.04, 0.03, 0.03, 1)
        cr.arc(px, py, ir * 0.5, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.95)
        cr.arc(px + ir * 0.35, py - ir * 0.4, 3.6, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.25, 0.15, 0.12, 0.35)          # upper-lid shadow on the eyeball
        cr.rectangle(-rx, -ry, 2 * rx, ry * 0.45)
        cr.fill()
        cr.restore()
        cr.new_path()
        eye(cr)
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.set_line_width(6)                                 # upper lash line, heavier
        cr.save()
        cr.scale(1, max(0.05, ry / rx))
        cr.arc(0, 0, rx, math.pi * 1.08, math.pi * 1.92)
        cr.restore()
        cr.stroke()
        cr.restore()
    # nose: a small hook on the shadow side and a soft shadow under it
    nx = tx * 1.2
    cr.new_path()
    cr.move_to(6 + nx, 4)
    cr.curve_to(10 + nx, 18, 18 + nx, 28, 8 + nx, 34)
    cr.set_source_rgba(*INK[:3], 0.85)
    cr.set_line_width(3.5)
    cr.stroke()
    cr.set_source_rgba(*sk_d[:3], 0.7)
    cr.save()
    cr.translate(nx, 37)
    cr.scale(1, 0.4)
    cr.arc(0, 0, 13, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    # mouth
    my, mx = 66, tx * 0.8
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    if f["mouth"] == "flat" or f["open"] < 0.12:
        cr.move_to(mx - 22, my + 2)
        cr.curve_to(mx - 8, my - 2 + 6 * f["worry"], mx + 8, my - 2 + 6 * f["worry"], mx + 22, my + 4)
        cr.set_source_rgba(*INK)
        cr.set_line_width(4.5)
        cr.stroke()
    else:
        o = f["open"]
        w_, h_ = (16 + 6 * o, 10 + 26 * o) if f["mouth"] == "o" else (30, 8 + 16 * o)
        cr.save()
        cr.translate(mx, my + 6)
        cr.new_path()
        if f["mouth"] == "o":
            cr.scale(1, h_ / w_)
            cr.arc(0, 0, w_, 0, 2 * math.pi)
            cr.restore()
            cr.save()
            cr.translate(mx, my + 6)
        else:
            w_, h_ = 30, 14 + 22 * o
            curve(cr, [(-w_, -h_ * 0.35), (0, -h_ * 0.5), (w_, -h_ * 0.35), (w_ * 0.85, h_ * 0.45), (0, h_ * 0.6),
                       (-w_ * 0.85, h_ * 0.45)])
        cr.set_source_rgba(*mix(LIP, (0.1, 0.02, 0.03, 1), 0.6))
        cr.fill_preserve()
        cr.save()
        cr.clip()
        cr.set_source_rgba(0.95, 0.93, 0.88, 1)               # top teeth (and bottom teeth in a grimace)
        cr.rectangle(-w_, -h_ * 0.8, 2 * w_, h_ * 0.42)
        cr.fill()
        if f["mouth"] == "grim":
            cr.rectangle(-w_, h_ * 0.32, 2 * w_, h_ * 0.4)
            cr.fill()
        cr.restore()
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.restore()
    # hair: volume on top, a messy fringe
    hair = lambda c: curve(c, [(-110, -12), (-114, -76), (-84, -128), (-24, -154), (38, -150), (92, -122), (116, -74),
                               (112, -6), (98, -46), (78, -40), (64, -70), (40, -44), (18, -72), (-6, -46),
                               (-30, -74), (-54, -48), (-74, -74), (-92, -40)])
    toon(cr, hair, HAIR, HAIR_D, light, rim, rim_from)
    cr.set_source_rgba(1, 1, 1, 0.18)                         # a few highlight strands
    cr.set_line_width(3)
    for k in range(4):
        cr.move_to(-60 + k * 34, -132 + 4 * k)
        cr.curve_to(-50 + k * 34, -120, -44 + k * 34, -104, -46 + k * 34, -92)
        cr.stroke()
    # brows over the hair (cartoon convention): the inner end rises with worry, both rise with alarm
    for sx in (-1, 1):
        by = -40 - 18 * f["raise_"]
        inner, outer = (sx * 14 + tx, by - 15 * f["worry"]), (sx * 68 + tx, by + 7 * f["worry"])
        cr.new_path()
        cr.move_to(inner[0], inner[1] + 5)
        cr.curve_to(inner[0] + sx * 18, inner[1] - 7, outer[0] - sx * 18, outer[1] - 9, outer[0], outer[1])
        cr.curve_to(outer[0] - sx * 18, outer[1] - 1, inner[0] + sx * 18, inner[1] + 3, inner[0], inner[1] + 13)
        cr.close_path()
        cr.set_source_rgba(*HAIR_D)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(2)
        cr.stroke()
    if sweat > 0:
        cr.save()
        cr.translate(92 + tx, -44 + 30 * ((t * 0.35) % 1) * sweat)
        cr.new_path()
        cr.move_to(0, -14)
        cr.curve_to(9, 0, 9, 10, 0, 12)
        cr.curve_to(-9, 10, -9, 0, 0, -14)
        cr.set_source_rgba(0.75, 0.9, 1, 0.85 * sweat)
        cr.fill_preserve()
        cr.set_source_rgba(*INK[:3], 0.8 * sweat)
        cr.set_line_width(2.5)
        cr.stroke()
        cr.restore()
    cr.restore()   # head
    cr.restore()


def you_back(cr, x, y, s, t, light=(8, -6), rim=None, rim_from=(-9, 0)):
    """The lead from behind (over-the-shoulder shots): hair, ears, hood and shoulders."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    up = -3 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 0.28))
    toon(cr, lambda c: curve(c, [(-62, -12 + up), (-150, 28 + up), (-182, 118), (-196, 430), (196, 430), (182, 118),
                                 (150, 28 + up), (62, -12 + up)]), HOOD, HOOD_D, light, rim, rim_from)
    toon(cr, lambda c: curve(c, [(-112, 0 + up), (-70, -60 + up), (0, -76 + up), (70, -60 + up), (112, 0 + up),
                                 (60, 40 + up), (0, 48 + up), (-60, 40 + up)]), HOOD_L, HOOD_D, light, rim, rim_from)
    cr.translate(0, -175)
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 96, -22), (sx * 120, -30), (sx * 122, 6), (sx * 104, 22)]),
             SKIN, SKIN_D, light, rim, rim_from, lw=4)
    toon(cr, lambda c: curve(c, [(-108, 10), (-114, -70), (-84, -128), (-20, -152), (40, -148), (92, -122),
                                 (116, -70), (110, 10), (70, 70), (30, 92), (0, 84), (-34, 94), (-72, 66)]),
         HAIR, HAIR_D, light, rim, rim_from)
    cr.restore()


# ------------------------------------------------------------------ seven-segment LED digits
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc",
       "8": "abcdefg", "9": "abcdfg"}


def led_digit(cr, ch, x, y, h, col, a=1.0):
    w = h * 0.55
    th = h * 0.12
    segs = {"a": (0, 0, w, 0), "b": (w, 0, w, h / 2), "c": (w, h / 2, w, h), "d": (0, h, w, h),
            "e": (0, h / 2, 0, h), "f": (0, 0, 0, h / 2), "g": (0, h / 2, w, h / 2)}
    cr.save()
    cr.translate(x, y)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, (x0, y0, x1, y1) in segs.items():
        on = k in SEG.get(ch, "")
        cr.set_source_rgba(*col[:3], a if on else 0.07)
        cr.set_line_width(th)
        cr.move_to(x0, y0)
        cr.line_to(x1, y1)
        cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ Mrs. Gray (the thing that says it is her)
G_SKIN, G_SKIN_D = hexa("#d9b8a0"), hexa("#a88370")
G_HAIR, G_HAIR_D = hexa("#c9c6c2"), hexa("#8e8a86")
G_GOWN, G_GOWN_D = hexa("#4b3652"), hexa("#2c1f31")
G_SHAWL, G_SHAWL_D = hexa("#8a7f8c"), hexa("#5a525c")
SLIPPER = hexa("#b06a72")


def gray_head(cr, t, smile=0.0, glow_eyes=0.0, light=(-14, -10), rim=None, rim_from=(9, 0), skin=None, look=(0, 0),
              mouth_open=0.0):
    """Her head, centred at (0, 0), radius ~62. smile: 0 = a kind old lady, 1 = the grin that is too wide."""
    sk = skin or G_SKIN
    sk_d = G_SKIN_D if skin is None else mix(sk, (0, 0, 0, 1), 0.3)
    toon(cr, lambda c: curve(c, [(-56, -70), (0, -96), (56, -70), (78, -20), (66, 40), (26, 66), (-26, 66),
                                 (-66, 40), (-78, -20)]), G_HAIR, G_HAIR_D, light, rim, rim_from)       # hair behind
    toon(cr, lambda c: (c.arc(0, -98, 30, 0, 2 * math.pi)), G_HAIR, G_HAIR_D, light, rim, rim_from)     # the bun
    head = lambda c: curve(c, [(-58, -36), (-50, -70), (0, -84), (50, -70), (58, -36), (56, 20), (36, 58), (0, 70),
                               (-36, 58), (-56, 20)])
    toon(cr, head, sk, sk_d, light, rim, rim_from)
    cr.set_source_rgba(*INK[:3], 0.35)                       # wrinkles
    cr.set_line_width(2)
    for sx in (-1, 1):
        cr.move_to(sx * 50, 4)
        cr.curve_to(sx * 44, 18, sx * 46, 30, sx * 40, 40)
        cr.stroke()
        cr.move_to(sx * 18, -50)
        cr.line_to(sx * 36, -52)
        cr.stroke()
    toon(cr, lambda c: curve(c, [(-58, -40), (-46, -76), (0, -88), (46, -76), (58, -40), (36, -58), (0, -62),
                                 (-36, -58)]), G_HAIR, G_HAIR_D, light, rim, rim_from, lw=3.5)       # hairline
    for sx in (-1, 1):                                        # eyes behind round glasses
        ex = sx * 24 + look[0] * 3
        if glow_eyes > 0.05:
            glow(cr, ex, -12, 28, (1, 0.96, 0.82), 0.55 * glow_eyes)
            cr.set_source_rgba(1, 0.98, 0.88, glow_eyes)
            cr.arc(ex, -12, 6.5, 0, 2 * math.pi)
            cr.fill()
        else:
            cr.set_source_rgba(*INK)
            cr.arc(ex, -12 + look[1] * 2, 4.5, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(*INK)
        cr.set_line_width(3.5)
        cr.arc(sx * 24, -12, 17, 0, 2 * math.pi)
        cr.stroke()
        cr.set_source_rgba(1, 1, 1, 0.25)
        cr.arc(sx * 24 - 5, -18, 6, 0, 2 * math.pi)
        cr.fill()
    cr.move_to(-7, -12)
    cr.curve_to(-3, -16, 3, -16, 7, -12)
    cr.set_source_rgba(*INK)
    cr.set_line_width(3)
    cr.stroke()
    cr.move_to(2, 2)                                          # nose
    cr.curve_to(8, 14, 6, 20, -2, 20)
    cr.set_line_width(3)
    cr.stroke()
    w = 14 + 34 * smile                                        # the smile widens until it reaches the cheeks
    lift = 6 + 10 * smile
    h = 4 + (14 + 10 * mouth_open) * smile
    cr.save()
    cr.translate(0, 38)
    cr.new_path()
    cr.move_to(-w, -lift)
    cr.curve_to(-w * 0.5, h, w * 0.5, h, w, -lift)
    if smile > 0.3:
        cr.curve_to(w * 0.5, h * 0.25, -w * 0.5, h * 0.25, -w, -lift)
        cr.close_path()
        cr.set_source_rgba(0.12, 0.03, 0.04, 1)
        cr.fill_preserve()
        cr.save()
        cr.clip()
        n = int(6 + 10 * smile)
        for k in range(n):                                    # too many teeth, top and bottom
            xx = -w + k * 2 * w / n
            for y0_, hh in ((-lift, lift + h * 0.42), (h * 0.55, h)):
                cr.rectangle(xx + 1, y0_, 2 * w / n - 2, hh)
        cr.set_source_rgba(0.93, 0.9, 0.78, 1)
        cr.fill()
        cr.restore()
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.stroke()
    else:
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.stroke()
    cr.restore()


def gray_full(cr, x, y, s, t, smile=0.0, glow_eyes=0.0, reach=0.0, lean=0.0, light=(-14, -10), rim=None,
              rim_from=(9, 0), backwards=True, dark=0.0):
    """Mrs. Gray standing, feet at (x, y), ~600 px tall at s = 1, with her cane. Her slippers face backwards (the
    hidden detail): the toes point back, so the long side of each slipper runs up behind the ankle. dark: 0..1
    sinks her into the dark (only the eyes stay bright)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    sway = 3 * math.sin(t * 0.9)
    for sx in (-1, 1):                                        # slippers (backwards) and ankles
        cr.save()
        cr.translate(sx * 30, 0)
        toon(cr, lambda c: curve(c, [(-16, 0), (-20, -30), (-10, -62), (10, -62), (20, -30), (16, 0)]) if backwards
             else curve(c, [(-18, -20), (-24, 10), (0, 24), (24, 10), (18, -20)]), SLIPPER, mix(SLIPPER, INK, 0.4),
             light, rim, rim_from, lw=3.5)
        toon(cr, lambda c: c.rectangle(-9, -84, 18, 74), G_SKIN, G_SKIN_D, light, None, lw=3)
        if backwards:                                        # the heel cup faces us
            cr.set_source_rgba(*mix(SLIPPER, INK, 0.55))
            cr.arc(0, -6, 12, math.pi, 2 * math.pi)
            cr.fill()
        cr.restore()
    cr.translate(sway, 0)
    cr.rotate(lean)
    toon(cr, lambda c: curve(c, [(-70, -300), (70, -300), (118, -80), (100, -70), (-100, -70), (-118, -80)]),
         G_GOWN, G_GOWN_D, light, rim, rim_from)
    cr.set_source_rgba(*INK[:3], 0.4)                        # folds
    cr.set_line_width(2.5)
    for fx in (-50, -12, 30, 70):
        cr.move_to(fx * 0.6, -290)
        cr.curve_to(fx * 0.8, -220, fx, -150, fx * 1.1, -76)
        cr.stroke()
    toon(cr, lambda c: curve(c, [(-62, -470), (62, -470), (92, -400), (84, -296), (-84, -296), (-92, -400)]),
         G_GOWN, G_GOWN_D, light, rim, rim_from)
    # the arm with the cane (her left = screen right)
    toon(cr, lambda c: curve(c, [(70, -455), (100, -400), (108, -320), (90, -316), (76, -390), (58, -440)]),
         G_GOWN, G_GOWN_D, light, rim, rim_from)
    cr.set_source_rgba(*hexa("#4a2e1c"))
    cr.set_line_width(9)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(112, -318)
    cr.line_to(124 + 0 * reach, 0)
    cr.stroke()
    cr.move_to(92, -330)
    cr.curve_to(96, -352, 124, -352, 120, -318)
    cr.stroke()
    toon(cr, lambda c: c.arc(102, -318, 14, 0, 2 * math.pi), G_SKIN, G_SKIN_D, light, None, lw=3)
    # the other arm hangs, or reaches toward you (foreshortened: the hand grows as it comes closer)
    hx, hy = -96 + 60 * reach, -330 - 60 * reach
    hr = 15 + 22 * reach
    toon(cr, lambda c: curve(c, [(-66, -455), (-96, -410), (hx - hr * 0.6, hy - hr), (hx + hr * 0.8, hy - hr * 0.4),
                                 (-74, -400), (-56, -440)]), G_GOWN, G_GOWN_D, light, rim, rim_from)
    toon(cr, lambda c: curve(c, [(hx - hr, hy), (hx - hr * 0.6, hy - hr * 0.9), (hx + hr * 0.5, hy - hr),
                                 (hx + hr, hy - hr * 0.2), (hx + hr * 0.4, hy + hr * 1.2), (hx - hr * 0.8, hy + hr)]),
         G_SKIN, G_SKIN_D, light, rim, rim_from, lw=3.5)
    if reach > 0.3:                                           # long fingers
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        for k in range(4):
            fx = hx - hr * 0.6 + k * hr * 0.42
            cr.move_to(fx, hy + hr * 0.9)
            cr.line_to(fx + 4, hy + hr * 1.9)
            cr.stroke()
    # the shawl over her shoulders
    toon(cr, lambda c: curve(c, [(-84, -470), (0, -486), (84, -470), (98, -420), (30, -360), (0, -340), (-30, -360),
                                 (-98, -420)]), G_SHAWL, G_SHAWL_D, light, rim, rim_from)
    toon(cr, lambda c: c.rectangle(-16, -500, 32, 34), G_SKIN, G_SKIN_D, light, None, lw=3)
    cr.save()
    cr.translate(0, -560)
    cr.rotate(0.18 * smile * math.sin(t * 0.7) + 0.08 * smile)     # the head tilts as the smile widens
    gray_head(cr, t, smile, glow_eyes, light, rim, rim_from)
    cr.restore()
    if dark > 0:
        cr.restore()
        return
    cr.restore()


# ------------------------------------------------------------------ hands and the phone
def hand_point(cr, x, y, s, t, tremble=0.0, skin=None):
    """Your hand reaching up from the bottom of the frame, index finger out."""
    sk = skin or SKIN
    cr.save()
    cr.translate(x + tremble * 2.5 * math.sin(t * 37), y + tremble * 2 * math.sin(t * 29))
    cr.scale(s, s)
    toon(cr, lambda c: curve(c, [(-60, 400), (-50, 120), (40, 110), (70, 400)]), HOOD, HOOD_D, (-14, -10), None)
    toon(cr, lambda c: curve(c, [(-46, 130), (-40, 60), (-18, 30), (8, -60), (20, -66), (26, -50), (22, 30), (40, 40),
                                 (54, 70), (46, 130)]), sk, SKIN_D, (-12, -8), None)
    cr.set_source_rgba(*INK[:3], 0.6)
    cr.set_line_width(2.5)
    for k in range(3):
        cr.move_to(-30 + k * 14, 60)
        cr.curve_to(-34 + k * 14, 80, -28 + k * 14, 96, -24 + k * 14, 104)
        cr.stroke()
    cr.restore()


def phone_in_hands(cr, x, y, s, t, glow_a=1.0):
    """Two hands holding a glowing phone at chest height."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    glow(cr, 0, -40, 260, (0.55, 0.75, 1), 0.35 * glow_a)
    toon(cr, lambda c: tk_rrect(c, -46, -84, 92, 168, 14), hexa("#16181c"), None, (0, 0), None, lw=4)
    cr.set_source_rgba(0.75, 0.88, 1, 0.95 * glow_a)
    tk_rrect(cr, -38, -74, 76, 148, 9)
    cr.fill()
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 40, 70), (sx * 66, 20), (sx * 70, -30), (sx * 52, -40),
                                             (sx * 40, 0), (sx * 30, 40)]), SKIN, SKIN_D, (-10, -8), None, lw=3.5)
    cr.restore()


def tk_rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


# ------------------------------------------------------------------ Last Stop: the old man
OM_SKIN, OM_SKIN_D = hexa("#d6a487"), hexa("#a5735a")
OM_COAT, OM_COAT_D, OM_COAT_L = hexa("#3e4a3c"), hexa("#262f25"), hexa("#56654f")
OM_SCARF, OM_SCARF_D = hexa("#b8862f"), hexa("#7f5a1c")
OM_CAP, OM_CAP_D = hexa("#6e6052"), hexa("#463c33")
OM_HAIR, OM_HAIR_D = hexa("#e6e2dc"), hexa("#aaa49b")
OM_PANTS = hexa("#3a3940")


def oldman_cap(cr, light=(-16, -12), rim=None, rim_from=(9, 0)):
    """His tweed flat cap (also worn by one of the faces in the window: the rewatch detail)."""
    toon(cr, lambda c: curve(c, [(-110, -58), (-106, -112), (-62, -150), (0, -160), (64, -150), (112, -110), (114, -60),
                                 (60, -70), (0, -72), (-60, -70)]), OM_CAP, OM_CAP_D, light, rim, rim_from)
    cr.set_source_rgba(0.95, 0.88, 0.75, 0.12)                # tweed flecks
    cr.set_line_width(2)
    for k in range(26):
        x, y = -90 + (k * 37) % 180, -140 + (k * 23) % 70
        cr.move_to(x, y)
        cr.line_to(x + 7, y + 3)
        cr.stroke()
    toon(cr, lambda c: curve(c, [(-100, -66), (0, -84), (100, -66), (88, -40), (0, -50), (-88, -40)]), OM_CAP_D,
         mix(OM_CAP_D, INK, 0.4), (0, -6), rim, rim_from, lw=4)


def oldman_head(cr, t, eyes=0.0, look=(0.0, 0.0), mouth=0.0, light=(-16, -12), rim=None, rim_from=(9, 0), skin=None,
                blink=True):
    """His head centred at (0, 0), about the lead's size: flat cap, white tufts, bushy brows, big nose, stubble.
    eyes: 0 = shut (asleep), 1 = open. mouth: 0 = shut, 1 = open (whispering)."""
    sk = skin or OM_SKIN
    sk_d = OM_SKIN_D if skin is None else mix(sk, (0, 0, 0, 1), 0.3)
    for sx in (-1, 1):                                                    # big ears
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 92, -34), (sx * 126, -48), (sx * 132, 8), (sx * 110, 38)]),
             sk, sk_d, light, rim, rim_from, lw=4)
    head = lambda c: curve(c, [(-96, -40), (-92, -96), (-50, -130), (0, -138), (50, -130), (92, -96), (96, -40),
                               (94, 20), (80, 64), (46, 100), (0, 112), (-46, 100), (-80, 64), (-94, 20)])
    toon(cr, head, sk, sk_d, light, rim, rim_from)
    cr.save()
    cr.new_path()
    head(cr)
    cr.clip()
    g = cairo.LinearGradient(0, -70, 0, 0)                              # the cap's brim shadows the eyes
    g.add_color_stop_rgba(0, 0.15, 0.07, 0.05, 0.55)
    g.add_color_stop_rgba(1, 0.15, 0.07, 0.05, 0)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.35, 0.32, 0.3, 0.55)                           # grey stubble on the jaw
    for k in range(70):
        a = (k * 0.618 * 2 * math.pi) % (2 * math.pi)
        rr = 0.55 + 0.45 * ((k * 0.382) % 1)
        px, py = 86 * rr * math.cos(a), 30 + 74 * rr * abs(math.sin(a))
        if py > 62 and abs(px) < 80 and not (abs(px) < 30 and 66 < py < 90):
            cr.arc(px, py, 1.6, 0, 2 * math.pi)
            cr.fill()
    cr.restore()
    for sx in (-1, 1):                                                    # white tufts under the cap
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 88, -78), (sx * 108, -50), (sx * 104, -4), (sx * 92, -20),
                                             (sx * 84, -50)]), OM_HAIR, OM_HAIR_D, light, rim, rim_from, lw=3)
    # eyes: heavy lids, bags under them; shut = two downward arcs
    open_ = eyes
    if blink and eyes > 0.5:
        ph = (t + 1.3) % 3.8
        open_ *= 1 - 0.95 * (math.sin(ph / 0.16 * math.pi) if ph < 0.16 else 0.0)
    for sx in (-1, 1):
        ex, ey = sx * 38, -10
        cr.save()
        cr.translate(ex, ey)
        if open_ > 0.08:
            rx, ry = 22, 13 * open_
            eye = lambda c: (c.save(), c.scale(1, max(0.05, ry / rx)), c.arc(0, 0, rx, 0, 2 * math.pi), c.restore())
            cr.new_path()
            eye(cr)
            cr.set_source_rgba(0.93, 0.9, 0.84, 1)
            cr.fill_preserve()
            cr.save()
            cr.clip()
            px, py = look[0] * 8, look[1] * 5
            cr.set_source_rgba(*hexa("#4d5a52"))
            cr.arc(px, py, 9, 0, 2 * math.pi)
            cr.fill()
            cr.set_source_rgba(0.03, 0.03, 0.03, 1)
            cr.arc(px, py, 4.5, 0, 2 * math.pi)
            cr.fill()
            cr.set_source_rgba(1, 1, 1, 0.9)
            cr.arc(px + 3, py - 3, 2.4, 0, 2 * math.pi)
            cr.fill()
            cr.set_source_rgba(0.3, 0.15, 0.1, 0.4)                     # heavy upper lid
            cr.rectangle(-rx, -ry, 2 * rx, ry * 0.6)
            cr.fill()
            cr.restore()
            cr.new_path()
            eye(cr)
            cr.set_source_rgba(*INK)
            cr.set_line_width(3.5)
            cr.stroke()
        else:
            cr.new_path()
            cr.move_to(-20, -2)
            cr.curve_to(-8, 7, 8, 7, 20, -2)
            cr.set_source_rgba(*INK)
            cr.set_line_width(4)
            cr.stroke()
        cr.set_source_rgba(*INK[:3], 0.45)                               # bags and crow's feet
        cr.set_line_width(2.5)
        cr.new_path()
        cr.move_to(-16, 18)
        cr.curve_to(-6, 24, 8, 24, 18, 16)
        cr.stroke()
        for k in range(3):
            cr.move_to(sx * 28, -6 + k * 8)
            cr.line_to(sx * 40, -10 + k * 11)
            cr.stroke()
        cr.restore()
    for sx in (-1, 1):                                                    # bushy white brows
        cr.save()
        cr.translate(sx * 40, -30)
        cr.scale(sx, 1)
        toon(cr, lambda c: curve(c, [(-30, 4), (-20, -10), (6, -14), (32, -6), (36, 6), (14, 2), (-10, 6)]),
             OM_HAIR, OM_HAIR_D, (0, -4), None, lw=3)
        cr.restore()
    toon(cr, lambda c: curve(c, [(-6, -10), (-12, 26), (-26, 44), (-14, 58), (0, 52), (14, 58), (26, 44), (12, 26),
                                 (6, -10)]), sk, sk_d, light, rim, rim_from, lw=3.5)     # a big nose
    cr.set_source_rgba(*INK[:3], 0.7)
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 9, 52)
        cr.scale(1, 0.5)
        cr.arc(0, 0, 4.5, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    cr.set_source_rgba(*INK[:3], 0.4)                                   # the folds beside the mouth
    cr.set_line_width(2.5)
    for sx in (-1, 1):
        cr.move_to(sx * 30, 50)
        cr.curve_to(sx * 40, 62, sx * 42, 76, sx * 38, 90)
        cr.stroke()
    if mouth > 0.05:
        cr.save()
        cr.translate(0, 80)
        cr.scale(1, 0.35 + 0.4 * mouth)
        cr.arc(0, 0, 18, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.18, 0.05, 0.05, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.stroke()
    else:
        cr.move_to(-26, 82)
        cr.curve_to(-10, 76, 10, 76, 26, 82)
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
    oldman_cap(cr, light, rim, rim_from)


def oldman_bust(cr, x, y, s, t, eyes=0.0, look=(0.0, 0.0), mouth=0.0, tilt=0.0, lean=0.0, light=(-16, -12), rim=None,
                rim_from=(9, 0), skin=None):
    """The old man from the chest up (x, y = the base of the neck): wool coat, mustard scarf."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(lean)
    up = -3 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 0.2))
    toon(cr, lambda c: curve(c, [(-60, -10 + up), (-156, 30 + up), (-190, 120), (-200, 430), (200, 430), (190, 120),
                                 (156, 30 + up), (60, -10 + up)]), OM_COAT, OM_COAT_D, light, rim, rim_from)
    for sx in (-1, 1):                                                    # lapels
        toon(cr, lambda c, sx=sx: poly(c, [(sx * 40, 20), (sx * 120, 40 + up), (sx * 70, 200), (sx * 14, 260)]),
             OM_COAT_L, OM_COAT_D, light, rim, rim_from, lw=3.5)
    for k in range(2):                                                    # buttons
        toon(cr, lambda c, k=k: c.arc(-26, 300 + k * 70, 9, 0, 2 * math.pi), hexa("#2b2018"), None, (0, 0), None, lw=2.5)
    toon(cr, lambda c: poly(c, [(-34, -82), (34, -82), (38, 0), (-38, 0)]), OM_SKIN, OM_SKIN_D, (10, 0), None, lw=4)
    scarf = lambda c: curve(c, [(-104, 4 + up), (-70, -40 + up), (0, -50 + up), (70, -40 + up), (104, 4 + up),
                                (70, 40 + up), (0, 28 + up), (-70, 40 + up)])
    toon(cr, scarf, OM_SCARF, OM_SCARF_D, light, rim, rim_from)
    toon(cr, lambda c: curve(c, [(30, 30 + up), (74, 34 + up), (82, 200), (40, 206)]), OM_SCARF, OM_SCARF_D, light,
         rim, rim_from, lw=4)                                             # the tail of the scarf
    cr.set_source_rgba(0.55, 0.12, 0.08, 0.7)                           # its stripes
    cr.set_line_width(5)
    for yy in (90, 130, 170):
        cr.move_to(36 + yy * 0.05, yy)
        cr.line_to(78 + yy * 0.02, yy - 4)
        cr.stroke()
    cr.translate(0, -175)
    cr.rotate(tilt + 0.01 * noise(t * 0.5, 9))
    oldman_head(cr, t, eyes, look, mouth, light, rim, rim_from, skin)
    cr.restore()


def oldman_full(cr, x, y, s, t, eyes=1.0, hand=0.0, look=(0.0, 0.0), light=(-16, -12), rim=None, rim_from=(9, 0),
                skin=None):
    """Standing, feet at (x, y), ~620 px tall at s = 1. hand: 0 = arm down, 1 = holding his hand out to you
    (foreshortened: it grows as it comes toward the camera)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: c.rectangle(sx * 30 - 20, -190, 40, 182), OM_PANTS, mix(OM_PANTS, INK, 0.4), light,
             rim, rim_from, lw=3.5)
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 30 - 26, -6), (sx * 30 - 20, -22), (sx * 30 + 22, -22),
                                             (sx * 30 + 30, -4), (sx * 30 + 20, 6), (sx * 30 - 20, 6)]),
             hexa("#2a1d15"), None, (0, 0), rim, rim_from, lw=3)
    toon(cr, lambda c: curve(c, [(-70, -470), (70, -470), (104, -300), (118, -170), (-118, -170), (-104, -300)]),
         OM_COAT, OM_COAT_D, light, rim, rim_from)
    cr.set_source_rgba(*INK[:3], 0.5)
    cr.set_line_width(3)
    cr.move_to(4, -440)
    cr.line_to(8, -172)
    cr.stroke()
    for k in range(3):
        toon(cr, lambda c, k=k: c.arc(-8, -400 + k * 70, 6, 0, 2 * math.pi), hexa("#2b2018"), None, (0, 0), None, lw=2)
    # right arm (screen right) hangs
    toon(cr, lambda c: curve(c, [(62, -466), (98, -420), (112, -300), (104, -250), (84, -252), (82, -330), (60, -420)]),
         OM_COAT, OM_COAT_D, light, rim, rim_from)
    toon(cr, lambda c: c.arc(96, -236, 17, 0, 2 * math.pi), OM_SKIN, OM_SKIN_D, light, None, lw=3)
    # left arm (screen left): hangs, or reaches out to you, palm up
    ex, ey = -100 - 40 * hand, -360 + 10 * hand
    wx, wy = -104 - 92 * hand, -256 - 84 * hand
    for col, lw in ((INK, 54), (OM_COAT, 45)):
        cr.new_path()
        cr.move_to(-64, -452)
        cr.curve_to(ex + 10, ey - 50, ex, ey, wx, wy)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_source_rgba(*col)
        cr.set_line_width(lw)
        cr.stroke()
    cr.save()
    cr.translate(wx, wy)
    cr.rotate(0.25 * hand)
    cr.scale(-(1 + 0.35 * hand), 1 + 0.35 * hand)                      # fingers point away from him, toward the door
    if hand > 0.3:                                                       # an open hand, palm up, fingers toward you
        toon(cr, lambda c: curve(c, [(-14, -10), (8, -16), (34, -14), (52, -6), (54, 6), (30, 10), (4, 14), (-14, 10)]),
             OM_SKIN, OM_SKIN_D, light, rim, rim_from, lw=3.5)
        toon(cr, lambda c: curve(c, [(0, -12), (10, -30), (20, -28), (16, -12)]), OM_SKIN, OM_SKIN_D, light, None, lw=3)
        cr.set_source_rgba(*INK[:3], 0.7)
        cr.set_line_width(2.2)
        for k in range(3):
            cr.move_to(30 + k * 6, -12 + k * 2)
            cr.line_to(46 + k * 2, -4 + k * 4)
            cr.stroke()
    else:
        toon(cr, lambda c: c.arc(0, 12, 17, 0, 2 * math.pi), OM_SKIN, OM_SKIN_D, light, None, lw=3)
    cr.restore()
    toon(cr, lambda c: curve(c, [(-84, -472), (0, -488), (84, -472), (70, -440), (0, -450), (-70, -440)]), OM_SCARF,
         OM_SCARF_D, light, rim, rim_from, lw=4)
    toon(cr, lambda c: curve(c, [(24, -460), (56, -458), (60, -330), (30, -326)]), OM_SCARF, OM_SCARF_D, light, rim,
         rim_from, lw=3.5)
    cr.translate(0, -560)
    cr.scale(0.62, 0.62)
    oldman_head(cr, t, eyes, look, 0.0, light, rim, rim_from, skin)
    cr.restore()


# ------------------------------------------------------------------ Last Stop: the driver (only ever seen in his mirror)
DR_SKIN, DR_SKIN_D = hexa("#c7a088"), hexa("#8f6a56")
DR_CAP = hexa("#1d2433")


def driver_eyes(cr, t, w=420, h=150, look=(0.0, 0.0), glint=0.0):
    """The band of the driver's face a rear-view mirror shows: cap brim, heavy brows, eyes looking straight at you.
    Centred at (0, 0); w x h. glint: a pale shine in the irises (Night 1 ends with him less human)."""
    cr.save()
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    g.add_color_stop_rgba(0, *mix(DR_SKIN_D, INK, 0.3))
    g.add_color_stop_rgba(0.35, *DR_SKIN)
    g.add_color_stop_rgba(0.7, *DR_SKIN)
    g.add_color_stop_rgba(1, *mix(DR_SKIN_D, INK, 0.5))
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(*DR_CAP)                                          # the cap's brim and its shadow
    cr.rectangle(-w / 2, -h / 2, w, h * 0.22)
    cr.fill()
    cr.set_source_rgba(0.85, 0.68, 0.25, 1)
    cr.rectangle(-w / 2, -h / 2 + h * 0.2, w, 4)
    cr.fill()
    g = cairo.LinearGradient(0, -h / 2 + h * 0.22, 0, -h / 2 + h * 0.5)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.rectangle(-w / 2, -h / 2 + h * 0.22, w, h * 0.3)
    cr.set_source(g)
    cr.fill()
    for sx in (-1, 1):
        ex, ey = sx * w * 0.19, h * 0.12
        cr.save()
        cr.translate(ex, ey)
        rx, ry = w * 0.075, w * 0.032
        eye = lambda c: (c.save(), c.scale(1, ry / rx), c.arc(0, 0, rx, 0, 2 * math.pi), c.restore())
        cr.new_path()
        eye(cr)
        cr.set_source_rgba(0.9, 0.86, 0.8, 1)
        cr.fill_preserve()
        cr.save()
        cr.clip()
        px, py = look[0] * rx * 0.3, look[1] * ry * 0.3
        ir = ry * 1.05
        cr.set_source_rgba(*mix(hexa("#3b2a20"), (0.95, 0.95, 0.85, 1), glint))
        cr.arc(px, py, ir, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.02, 0.02, 0.02, 1)
        cr.arc(px, py, ir * (0.5 - 0.25 * glint), 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.arc(px + ir * 0.35, py - ir * 0.35, ir * 0.22, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.2, 0.1, 0.08, 0.45)
        cr.rectangle(-rx, -ry, 2 * rx, ry * 0.7)
        cr.fill()
        cr.restore()
        cr.new_path()
        eye(cr)
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.restore()
        if glint > 0:
            glow(cr, ex, ey, rx * 1.4, (1, 0.97, 0.85), 0.35 * glint)
        cr.save()                                                        # heavy brows, pulled down at the middle
        cr.translate(ex, ey - h * 0.2)
        cr.scale(sx, 1)
        toon(cr, lambda c: poly(c, [(-w * 0.1, h * 0.05), (-w * 0.08, -h * 0.04), (w * 0.09, -h * 0.06),
                                    (w * 0.1, h * 0.0)]), hexa("#2a1e18"), None, (0, 0), None, lw=2.5)
        cr.restore()
        cr.set_source_rgba(*INK[:3], 0.4)                               # bags
        cr.set_line_width(2.5)
        cr.move_to(ex - rx * 0.8, ey + ry * 1.7)
        cr.curve_to(ex - rx * 0.3, ey + ry * 2.3, ex + rx * 0.3, ey + ry * 2.3, ex + rx * 0.8, ey + ry * 1.6)
        cr.stroke()
    cr.set_source_rgba(*INK[:3], 0.55)                                   # the bridge of the nose
    cr.set_line_width(3)
    cr.move_to(-w * 0.03, h * 0.2)
    cr.curve_to(-w * 0.04, h * 0.35, -w * 0.02, h * 0.45, -w * 0.04, h * 0.5)
    cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ Last Stop: the passengers nobody saw get on
def pale_face(cr, x, y, s, t, a=1.0, cap=False, tilt=0.0, seed=0):
    """A passenger in the dark: shoulders, a pale blank face, hollow eyes with pin-point lights. cap=True gives it the
    old man's flat cap and scarf (the detail for rewatchers)."""
    if a <= 0:
        return
    cr.save()
    cr.translate(x + 1.5 * math.sin(t * 1.3 + seed), y)
    cr.scale(s, s)
    cr.push_group()
    cr.set_source_rgba(0.04, 0.05, 0.07, 1)
    curve(cr, [(-60, -10), (-150, 30), (-180, 200), (180, 200), (150, 30), (60, -10)])
    cr.fill()
    if cap:
        cr.set_source_rgba(*OM_SCARF[:3], 0.55)
        curve(cr, [(-90, 4), (0, -30), (90, 4), (0, 26)])
        cr.fill()
    cr.rotate(tilt)
    cr.translate(0, -140)
    face = lambda c: curve(c, [(-78, -30), (-70, -90), (0, -118), (70, -90), (78, -30), (66, 50), (0, 96), (-66, 50)])
    cr.new_path()
    face(cr)
    cr.set_source(rad(0, -20, 120, [(0, (0.86, 0.9, 0.95, 1)), (0.7, (0.62, 0.68, 0.76, 1)), (1, (0.3, 0.34, 0.42, 1))]))
    cr.fill()
    for sx in (-1, 1):                                                    # hollow eyes, a point of light in each
        cr.save()
        cr.translate(sx * 30, -16)
        cr.scale(1, 1.25)
        cr.arc(0, 0, 18, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.05, 0.04, 0.06, 0.95)
        cr.fill()
        cr.set_source_rgba(1, 0.97, 0.88, 1)
        cr.arc(sx * 30, -14, 3.8, 0, 2 * math.pi)
        cr.fill()
    cr.save()
    cr.translate(0, 46)
    cr.scale(1, 0.6)
    cr.arc(0, 0, 11, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(0.08, 0.06, 0.08, 0.85)
    cr.fill()
    if cap:
        cr.save()
        cr.translate(0, 12)
        cr.scale(0.74, 0.74)
        oldman_cap(cr)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()
