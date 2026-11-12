"""Cast, props and light effects for the Kannada Yakshagana Shikhandi reel (scenes_shikhandi_yk), built on yaksha_kit
(never edited: new looks are dicts made from the kit's looks, new face paints are added to Y.FACES under "sy_" keys).

Colour rule a child can follow: Amba wears PINK with gold and saffron; in her next life Shikhandi, the warrior, wears
the same pink and saffron, and her soul is a pink-gold light. Bhishma is the old warrior in white with a white beard;
Arjuna is the archer in green with the fan headdress.

No wounds anywhere: arrows are streaks of golden light, the bed of arrows is a row of light, the fire is a glow.
"""
import functools
import math

import cairo
import numpy as np
from scipy.ndimage import gaussian_filter

import yaksha_kit as Y
from poster import back, clamp, ease
from puppet_core import surface_from_rgba

# ------------------------------------------------------------------ colours

PINK = (0.93, 0.25, 0.56)            # Amba's colour, and Shikhandi's
PINK_DK = (0.60, 0.07, 0.33)
PINK_LT = (1.0, 0.66, 0.82)
SOUL = (1.0, 0.70, 0.84)             # her soul's light
GOLDL = (1.0, 0.84, 0.45)            # arrows of light, Bhishma's light
GREENL = (0.55, 1.0, 0.50)           # the yaksha's light
WHITE_CLOTH = (0.97, 0.96, 0.92)

# ------------------------------------------------------------------ face paints (added to the kit's table)

Y.FACES.setdefault("sy_bhishma", dict(base=(0.99, 0.72, 0.46), mark="namam", beard=(0.99, 0.98, 0.95),
                                      brow=(0.99, 0.98, 0.95), old=True, rouge=True))
Y.FACES.setdefault("sy_yaksha", dict(base=(0.46, 0.80, 0.44), mark="namam", stache=True, jaw=True, rouge=False))
Y.FACES.setdefault("sy_shiva", dict(base=(0.52, 0.66, 0.92), mark="vibhuti", rouge=False, jaw=True, lips=Y.LIPS))

# ------------------------------------------------------------------ looks

AMBA = dict(Y.WOMAN, saree=PINK, border=Y.GOLD, blouse=Y.SAFF)
QUEEN = dict(Y.WOMAN, saree=Y.GREEN, border=Y.RED, blouse=Y.RED)
SHIKHANDI = dict(Y.HERO, crown="kireeta_small", disc=False, head_s=1.12, jacket=PINK, sleeve=PINK,
                 kase=(PINK, Y.SAFF, Y.INK, Y.YEL), hem=Y.SAFF, hem_zig=Y.YEL, sash=Y.SAFF, pads=PINK)
BHISHMA = dict(Y.KING, face="sy_bhishma", jacket=WHITE_CLOTH, sleeve=WHITE_CLOTH,
               kase=(WHITE_CLOTH, Y.GOLD, Y.INK, Y.RED), hem=Y.GOLD, hem_zig=Y.RED, sash=Y.RED,
               pads=(0.93, 0.90, 0.82), disc_cols=(Y.GOLD, Y.RED, WHITE_CLOTH))
ARJUNA = dict(Y.HERO, jacket=Y.GREEN, sleeve=Y.GREEN, kase=(Y.YEL, Y.GREEN, Y.INK, Y.RED), hem=Y.RED,
              hem_zig=Y.YEL, sash=Y.YEL, pads=Y.GREEN)
SALVA = dict(Y.KING, jacket=Y.BLUE, sleeve=Y.BLUE, kase=(Y.YEL, Y.BLUE, Y.INK, Y.RED), hem=Y.BLUE, pads=Y.BLUE,
             disc_cols=(Y.GOLD, Y.BLUE, Y.RED))
DRUPADA = dict(Y.KING, jacket=Y.CRIMSON, sleeve=Y.CRIMSON, kase=(Y.YEL, Y.CRIMSON, Y.INK, Y.GREEN), hem=Y.CRIMSON,
               pads=Y.CRIMSON)
BROTHER = dict(Y.HERO, crown="kireeta_small", jacket=Y.YEL, sleeve=Y.YEL, kase=(Y.RED, Y.YEL, Y.INK, Y.GREEN),
               hem=Y.RED, pads=Y.RED, edehara="small", bhuja=False, head_s=1.2)
YAKSHA = dict(Y.HERO, face="sy_yaksha", crown="kireeta", disc=True, disc_cols=(Y.GOLD, Y.GREEN, Y.YEL),
              jacket=Y.DGREEN, sleeve=Y.DGREEN, hand=(0.40, 0.72, 0.38), kase=(Y.GREEN, Y.YEL, Y.INK, Y.DGREEN),
              hem=Y.DGREEN, hem_zig=Y.YEL, sash=Y.YEL, pads=Y.DGREEN)
SHIVA = dict(Y.GOD, face="sy_shiva", hand=(0.52, 0.66, 0.92), jacket=(0.90, 0.88, 0.84), sleeve=(0.52, 0.66, 0.92),
             kase=(Y.SAFF, Y.INK, Y.INK, Y.YEL), hem=Y.BLUE, hem_zig=Y.WHITE, sash=Y.WHITE, pads=Y.BLUE,
             disc_cols=(Y.GOLD, Y.BLUE, Y.WHITE))

# ------------------------------------------------------------------ arm poses (upper, forearm, hand) in kit angles

REST = (0.16, 0.30, 0.0)
AKIMBO = (0.45, 1.35, 0.3)
ANJALI = (0.30, 2.30, 0.0)            # palms joined at the chest (woman / actor)
BOW_HOLD = (1.52, 0.02, 0.0)          # the arm out to the side holding the bow upright
BOW_DRAW = (1.45, 3.0, 0.0)           # the other hand pulled back to the shoulder
BOW_REST = (1.05, 0.55, 0.0)          # the bow held out lower, ready
FIST_UP = (2.75, 0.15, 0.0)
PALM_OUT = (1.25, -0.75, 0.25)        # a raised open palm to the side: stop / no
PALM_UP = (0.70, -2.44, 0.0)          # an open palm raised beside the face (no / a blessing), close to the body
PALM_DOWN = (0.55, 0.25, 0.0)
FACE_HANDS = (0.25, 2.75, -0.3)       # both hands to the face (crying)
REACH = (1.30, 0.20, 0.0)             # an arm reaching out to the side


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def pose(t, amp=1.0, freq=0.5, ph=0.0, **kw):
    """A pose with the Yakshagana idle sway mixed in (lean/head/shift given in kw are added to the sway)."""
    sh, ln, hd = Y.sway(t, amp, freq, ph)
    p = dict(shift=sh + kw.pop("shift", 0.0), lean=ln + kw.pop("lean", 0.0), head=hd + kw.pop("head", 0.0),
             sash=-ln * 3, breathe=math.sin(t * 2.2 + ph))
    p.update(kw)
    return p


def fig(c, look, x, feet, s, t, p, flip=False, alpha=1.0, shadow=0.5):
    if shadow:
        Y.floor_shadow(c, x + p.get("shift", 0.0) * s, feet, 300 * s, shadow * alpha)
    return Y.figure(c, look, x, feet, s, t, p, flip, alpha)


def U(c, p):
    """Device point -> the context's user space."""
    return Y.to_user(c, p)


# ------------------------------------------------------------------ props


def bow(cr, gx, gy, h, out=-1, pull=None, rot=0.0, alpha=1.0, arrow=False, lw=1.0):
    """An upright bow gripped at (gx, gy): its back bulges toward `out` (-1 = screen left), the tips curl back; the
    string runs tip to tip, or through `pull` (the drawing hand) when drawn. arrow=True lays a golden arrow on it."""
    tipx = -out * 0.20 * h
    top = (gx + tipx, gy - h / 2)
    bot = (gx + tipx, gy + h / 2)

    def limb(sgn):
        return [(gx, gy), (gx + out * 0.02 * h, gy + sgn * 0.18 * h), (gx + tipx * 0.45, gy + sgn * 0.38 * h),
                (gx + tipx, gy + sgn * 0.5 * h), (gx + tipx * 1.25, gy + sgn * 0.54 * h)]
    cr.save()
    if rot:
        cr.translate(gx, gy)
        cr.rotate(rot)
        cr.translate(-gx, -gy)
    sp = pull if pull else (gx + tipx, gy)
    cr.push_group()
    Y.stroke(cr, [top, sp, bot], 3.5 * lw, (0.95, 0.92, 0.80), smooth=False)
    if arrow:
        ax0 = sp[0]
        ax1 = gx + out * 0.62 * h
        Y.stroke(cr, [(ax0, sp[1]), (ax1, sp[1])], 9 * lw, Y.INK, smooth=False)
        Y.stroke(cr, [(ax0, sp[1]), (ax1, sp[1])], 5 * lw, Y.GOLD, smooth=False)
        Y.shape(cr, [(ax1 + out * 34 * lw, sp[1]), (ax1, sp[1] - 12 * lw), (ax1 + out * 6 * lw, sp[1]),
                     (ax1, sp[1] + 12 * lw)], Y.GOLD_HI, 3.0 * lw, smooth=False)
        for sg in (-1, 1):
            Y.shape(cr, [(ax0 - out * 4, sp[1]), (ax0 - out * 30 * lw, sp[1] + sg * 16 * lw),
                         (ax0 + out * 10 * lw, sp[1] + sg * 3)], Y.RED, 2.5 * lw, smooth=False)
    for sgn in (-1, 1):
        Y.inked_line(cr, limb(sgn), 13 * lw, (0.62, 0.34, 0.12), 3.5 * lw)
        pts = limb(sgn)
        Y.stroke(cr, pts[1:4], 3.0 * lw, Y.GOLD_HI, alpha=0.8)
    Y.shape(cr, [(gx - 11 * lw, gy - 30 * lw), (gx + 11 * lw, gy - 30 * lw), (gx + 11 * lw, gy + 30 * lw),
                 (gx - 11 * lw, gy + 30 * lw)], Y.RED, 3.5 * lw, smooth=False)
    for k in (-1, 1):
        Y.stroke(cr, [(gx - 12 * lw, gy + k * 20 * lw), (gx + 12 * lw, gy + k * 20 * lw)], 4 * lw, Y.GOLD)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def streak(cr, p0, p1, u, a=1.0, L=260.0, w=1.0, col=GOLDL):
    """An arrow of light flying from p0 to p1: at progress u its point is at lerp(p0, p1, u) with a fading tail."""
    if a <= 0.01 or u <= 0.0 or u > 1.25:
        return
    uu = min(u, 1.0)
    hx, hy = p0[0] + (p1[0] - p0[0]) * uu, p0[1] + (p1[1] - p0[1]) * uu
    d = math.dist(p0, p1) or 1.0
    ux, uy = (p1[0] - p0[0]) / d, (p1[1] - p0[1]) / d
    LL = min(L, d * uu)
    tx, ty = hx - ux * LL, hy - uy * LL
    fade = 1.0 if u <= 1.0 else clamp(1 - (u - 1.0) / 0.25)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, al in ((34 * w, 0.18), (14 * w, 0.45), (5 * w, 1.0)):
        g = cairo.LinearGradient(tx, ty, hx, hy)
        g.add_color_stop_rgba(0, *col, 0.0)
        g.add_color_stop_rgba(1, *col, al * a * fade)
        cr.set_source(g)
        cr.set_line_width(lw)
        cr.move_to(tx, ty)
        cr.line_to(hx, hy)
        cr.stroke()
    cr.restore()
    if u <= 1.0:
        cr.save()
        cr.translate(hx, hy)
        cr.rotate(math.atan2(uy, ux))
        cr.new_path()
        cr.move_to(26 * w, 0)
        cr.line_to(-6 * w, -11 * w)
        cr.line_to(0, 0)
        cr.line_to(-6 * w, 11 * w)
        cr.close_path()
        cr.set_source_rgba(1.0, 0.97, 0.80, a)
        cr.fill()
        cr.restore()
        Y.glow(cr, hx, hy, 70 * w, 0.5 * a, col)


def garland(cr, x, y, r, alpha=1.0, droop=1.0, rot=0.0):
    """A marigold garland hanging from (x, y): a loop of orange and yellow flowers."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.push_group()
    n = 18
    for i in range(n):
        a = math.pi * 2 * i / n
        px, py = r * 0.62 * math.sin(a), r * droop * (1 - math.cos(a)) * 0.5
        Y.dot(cr, px, py, r * 0.13, (0.99, 0.55, 0.05) if i % 2 else Y.YEL, 2.5)
        Y.dot(cr, px, py, r * 0.04, (0.75, 0.30, 0.0))
    Y.shape(cr, [(-r * 0.05, r * droop), (r * 0.05, r * droop), (0, r * droop + r * 0.3)], Y.RED, 2.5, smooth=False)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def heart(cr, x, y, s, alpha=1.0, crack=0.0, t=0.0):
    """A glowing red heart (love); crack 0..1 splits it in two halves that fall apart."""
    if alpha <= 0.01:
        return
    Y.glow(cr, x, y, 140 * s, 0.35 * alpha * (1 - crack), (1.0, 0.45, 0.55))
    pts = [(0, 34), (-36, 4), (-46, -20), (-36, -40), (-16, -44), (0, -28), (16, -44), (36, -40), (46, -20), (36, 4)]
    for sd in ((0,) if crack <= 0.0 else (-1, 1)):
        cr.save()
        cr.translate(x + sd * 30 * s * crack, y + 60 * s * crack * crack)
        cr.rotate(sd * 0.5 * crack)
        cr.scale(s * (1 + 0.04 * math.sin(t * 6)), s * (1 + 0.04 * math.sin(t * 6)))
        if sd:
            cr.new_path()
            cr.rectangle(-60 if sd < 0 else 0, -60, 60, 120)
            cr.clip()
        cr.push_group()
        Y.shape(cr, pts, (0.92, 0.12, 0.22), 5.0)
        Y.shape(cr, [(-26, -22), (-18, -34), (-8, -30)], (1.0, 0.75, 0.75), 0, smooth=True)
        if sd:
            Y.stroke(cr, [(0, -28), (-8, -12), (6, 2), (-4, 16), (0, 34)], 5.0, Y.INK, smooth=False)
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
        cr.restore()


def tear(cr, x, y, s, alpha):
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    cr.move_to(0, -14)
    cr.curve_to(6, -4, 10, 4, 10, 9)
    cr.curve_to(10, 16, -10, 16, -10, 9)
    cr.curve_to(-10, 4, -6, -4, 0, -14)
    cr.close_path()
    cr.set_source_rgba(0.75, 0.92, 1.0, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*Y.INK, alpha)
    cr.set_line_width(2.5)
    cr.stroke()
    cr.restore()


def linga(cr, x, y, s, t=0.0, glow_a=0.0):
    """A small Shiva linga on its base with flowers (what Amba prays to)."""
    Y.glow(cr, x, y - 60 * s, 260 * s, glow_a, (1.0, 0.85, 0.5))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-110, 0), (110, 0), (96, -40), (-96, -40)], (0.55, 0.52, 0.50), 6.0, smooth=False)
    Y.shape(cr, [(-130, -40), (150, -40), (190, -58), (150, -76), (-130, -76), (-150, -58)], (0.62, 0.60, 0.58), 6.0,
            smooth=False)
    Y.shape(cr, [(-46, -76), (-50, -150), (-36, -196), (0, -212), (36, -196), (50, -150), (46, -76)],
            (0.26, 0.25, 0.27), 6.0)
    for yy in (-150, -140, -130):
        Y.stroke(cr, [(-40, yy), (0, yy - 4), (40, yy)], 5, Y.WHITE)
    Y.dot(cr, 0, -140, 7, Y.RED, 2.0)
    for i, xx in enumerate((-100, -60, 60, 100, 140)):
        Y.dot(cr, xx, -82, 15, (0.99, 0.55, 0.05) if i % 2 else Y.YEL, 3.0)
    Y.dot(cr, 0, -222, 12, (0.99, 0.95, 0.85), 3.0)
    cr.restore()


def trishula(cr, x, y, s, rot=0.0, alpha=1.0):
    """Shiva's trident standing at (x, y) = its foot."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    Y.shape(cr, [(-8, 0), (8, 0), (8, -560), (-8, -560)], Y.GOLD_DK, 4.5, smooth=False)
    Y.shape(cr, [(-40, -560), (40, -560), (34, -585), (-34, -585)], Y.GOLD, 4.5, smooth=False)
    Y.shape(cr, [(-10, -585), (10, -585), (12, -690), (0, -730), (-12, -690)], Y.GOLD, 4.5, smooth=False)
    for sd in (-1, 1):
        Y.shape(cr, [(sd * 20, -580), (sd * 62, -600), (sd * 74, -650), (sd * 64, -700), (sd * 58, -650),
                     (sd * 46, -615), (sd * 16, -600)], Y.GOLD, 4.5)
    Y.dot(cr, 0, -572, 9, Y.RED, 2.5)
    # the little damaru tied below the prongs
    Y.shape(cr, [(-22, -500), (22, -500), (6, -520), (22, -540), (-22, -540), (-6, -520)], (0.70, 0.35, 0.15), 3.5,
            smooth=False)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def crescent(cr, x, y, r, alpha=1.0):
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.new_sub_path()
    cr.arc_negative(x + r * 0.45, y - r * 0.25, r * 0.85, 2 * math.pi, 0)
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.set_source_rgb(0.99, 0.97, 0.85)
    cr.fill_preserve()
    cr.set_source_rgb(*Y.INK)
    cr.set_line_width(3)
    cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def spin(t, t0, dur=0.8):
    """0..1 through one full turn from t0, eased in and out (smooth, no jumps)."""
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return 0.0
    return 0.5 - 0.5 * math.cos(math.pi * u)


def cradle(cr, x, y, s, t=0.0, swing=1.0, rope_top=600):
    """A wooden cradle (thottilu) hanging from a ring on a rope, with a pink bundle in it."""
    a = 0.06 * swing * math.sin(t * 2.0)
    Y.stroke(cr, [(x, rope_top), (x, y - 420 * s)], 11, Y.INK)
    Y.stroke(cr, [(x, rope_top), (x, y - 420 * s)], 5, (0.80, 0.62, 0.35))
    cr.save()
    cr.translate(x, y - 420 * s)
    cr.rotate(a)
    cr.scale(s, s)
    for sd in (-1, 1):
        Y.stroke(cr, [(0, 0), (sd * 150, 330)], 9, Y.INK)
        Y.stroke(cr, [(0, 0), (sd * 150, 330)], 4, Y.GOLD)
    Y.dot(cr, 0, 0, 16, Y.GOLD, 4.0)
    Y.shape(cr, [(-200, 330), (200, 330), (180, 420), (120, 450), (-120, 450), (-180, 420)], (0.62, 0.34, 0.13), 6.0)
    Y.stroke(cr, [(-190, 360), (190, 360)], 10, Y.RED)
    Y.dot_row(cr, [(-180, 395), (180, 395)], 12, 5, Y.GOLD_HI)
    for sd in (-1, 1):
        Y.dot(cr, sd * 200, 330, 16, Y.GOLD, 4.0)
    # the baby: a pink bundle with a little face
    Y.shape(cr, [(-110, 330), (-90, 290), (60, 284), (110, 304), (120, 332)], PINK, 5.0)
    Y.dot(cr, -70, 300, 30, (0.99, 0.80, 0.62), 4.0)
    Y.stroke(cr, [(-80, 300), (-74, 304)], 3)
    Y.stroke(cr, [(-64, 300), (-58, 304)], 3)
    Y.dot(cr, -69, 284, 4, Y.RED)
    cr.restore()
    m = cairo.Matrix()
    m.translate(x, y - 420 * s)
    m.rotate(a)
    return m.transform_point(-70 * s, 300 * s)


def palm_book(cr, x, y, s, t=0.0, open_=0.0):
    """An old palm-leaf book seen from the front: the top leaf (rows of writing, two string holes) lying on the
    bundle, wooden covers under it, a red string with a gold coin; open_ (0..1) lights it up. (x, y) = its centre."""
    wood, leaf, leaf2 = (0.48, 0.22, 0.08), (0.95, 0.84, 0.58), (0.84, 0.70, 0.42)
    Y.glow(cr, x, y, 620 * s, 0.25 + 0.45 * open_, (1.0, 0.85, 0.5))
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.04)
    cr.scale(s, s)

    def leafpath(w, h):
        return [(-w, -h), (w, -h), (w + h * 0.8, 0), (w, h), (-w, h), (-w - h * 0.8, 0)]
    Y.shape(cr, [(px, py + 46) for px, py in leafpath(450, 70)], wood, 6.0)            # the bottom cover
    Y.stroke(cr, [(-430, 46), (430, 46)], 5, Y.GOLD)
    for k in (3, 2, 1):                                                                 # the bundle's edges
        Y.shape(cr, [(px + 4 * k, py + 12 * k) for px, py in leafpath(430, 80)], leaf2, 3.5)
    Y.shape(cr, leafpath(430, 80), leaf, 5.0)                                           # the top leaf
    for row in range(3):                                                                # rows of old writing
        yy = -44 + 44 * row
        xs = -360
        k = 0
        while xs < 360:
            wv = 26 + 14 * ((row * 7 + k * 3) % 4)
            pts = [(xs + i * wv / 6, yy + 7 * math.sin(i * 1.7 + k)) for i in range(7)]
            Y.stroke(cr, pts, 4.0, (0.30, 0.16, 0.06))
            xs += wv + 16
            k += 1
    for hx in (-150, 150):                                                              # string holes, string
        Y.dot(cr, hx, 0, 12, (0.30, 0.16, 0.06), 2.5)
    sw = 6 * math.sin(t * 2.0)
    Y.stroke(cr, [(-150, 0), (-190 + sw, 110), (-176 + sw, 170)], 6, Y.RED)
    Y.dot(cr, -176 + sw, 182, 18, Y.GOLD, 4.0)
    Y.dot(cr, -176 + sw, 182, 6, Y.GOLD_DK)
    cr.restore()
    if open_ > 0.05:
        for k in range(7):
            u = ((t * 0.5 + k / 7.0) % 1.0)
            Y.sparkle(cr, x + (k - 3) * 110 * s + 20 * math.sin(t + k), y - 120 * s - 380 * s * u, 26 * (1 - u) + 4,
                      open_ * (1 - u))


def chariot(cr, x, y, s, t=0.0, roll=0.0):
    """A stage chariot facing right: a tall painted front panel (covering the riders' legs), a big wheel, a flag
    pole at the back. (x, y) = the middle of the panel's bottom edge."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    # the flag pole at the back (left), the flag above the riders' crowns
    Y.shape(cr, [(-330, -40), (-314, -40), (-314, -1250), (-330, -1250)], (0.55, 0.32, 0.14), 4.0, smooth=False)
    wv = 12 * math.sin(t * 3.0)
    Y.shape(cr, [(-314, -1245), (-150, -1205 + wv), (-180, -1165 + wv * 0.6), (-314, -1130)], Y.SAFF, 5.0)
    Y.stroke(cr, [(-300, -1200), (-200, -1185 + wv * 0.8)], 6, Y.RED)
    Y.dot(cr, -322, -1260, 14, Y.GOLD, 4.0)
    # the wheel
    cr.save()
    cr.translate(-40, 10)
    cr.rotate(roll)
    Y.dot(cr, 0, 0, 175, (0.50, 0.28, 0.10), 7.0)
    Y.dot(cr, 0, 0, 148, (0.30, 0.16, 0.06), 5.0)
    cr.set_source_rgb(*Y.GOLD)
    cr.set_line_width(14)
    for i in range(8):
        a = math.pi * i / 4
        cr.move_to(0, 0)
        cr.line_to(150 * math.cos(a), 150 * math.sin(a))
    cr.stroke()
    Y.dot(cr, 0, 0, 34, Y.GOLD, 5.0)
    Y.dot(cr, 0, 0, 12, Y.RED, 3.0)
    for i in range(16):
        a = math.pi * i / 8
        Y.dot(cr, 162 * math.cos(a), 162 * math.sin(a), 5, Y.GOLD_HI)
    cr.restore()
    # the panel
    panel = [(-380, -270), (380, -270), (440, -350), (492, -350), (462, -190), (400, -40), (-380, -40)]
    Y.shape(cr, panel, Y.RED, 7.0, smooth=False)
    Y.shape(cr, [(-360, -254), (368, -254), (398, -214), (-360, -214)], Y.GOLD, 4.0, smooth=False)
    Y.dot_row(cr, [(-350, -234), (372, -234)], 22, 5, Y.RED)
    Y.shape(cr, [(-360, -86), (408, -86), (392, -56), (-360, -56)], Y.GOLD, 4.0, smooth=False)
    Y.dot_row(cr, [(-350, -71), (386, -71)], 22, 4, Y.RED)
    for k, mx in enumerate((-220, 0, 220)):             # three painted lotus medallions
        Y.dot(cr, mx, -150, 44, Y.GOLD, 5.0)
        Y.dot(cr, mx, -150, 30, (Y.GREEN, Y.BLUE, Y.GREEN)[k], 3.5)
        Y.dot(cr, mx, -150, 11, Y.WHITE, 2.5)
    Y.dot(cr, 470, -352, 18, Y.GOLD, 4.0)
    cr.restore()


def light_bed(cr, t, x0, x1, ytop, yfloor, a=1.0, n=17):
    """The bed of arrows, as a soft row of light: thin golden shafts standing up from the floor."""
    if a <= 0.01:
        return
    Y.glow(cr, (x0 + x1) / 2, (ytop + yfloor) / 2, (x1 - x0) * 0.7, 0.30 * a, GOLDL)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        u = (i + 0.5) / n
        x = x0 + (x1 - x0) * u
        lean = 0.10 * math.sin(i * 2.3)
        top = ytop + 18 * math.sin(i * 1.7)
        bx = x + lean * (yfloor - top)
        sh = 0.75 + 0.25 * math.sin(t * 2.5 + i)
        for lw, al in ((16, 0.16), (6, 0.5), (2.5, 1.0)):
            cr.set_source_rgba(*GOLDL, al * a * sh)
            cr.set_line_width(lw)
            cr.move_to(bx, yfloor)
            cr.line_to(x, top)
            cr.stroke()
        for sg in (-1, 1):                              # the fletching near the floor
            cr.set_source_rgba(*GOLDL, 0.6 * a * sh)
            cr.set_line_width(3)
            fy = yfloor - 24
            fx = bx - lean * 24
            cr.move_to(fx, fy)
            cr.line_to(fx + sg * 12, fy + 18)
            cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ figures of light (the soul, the fallen Bhishma)

GHOSTS = {}


def ghost_def(key, look, p, s=1.0):
    GHOSTS[key] = (look, p, s)


@functools.lru_cache(maxsize=16)
def ghost_surfaces(key, col):
    """(figure-of-light surface, its glow surface, the feet point in the surface): the figure drawn once, its paint
    turned into tones of one colour of light (outlines stay a little darker so the face still reads), and a soft
    glow round it."""
    look, p, s = GHOSTS[key]
    gw, gh = int(1000 * s), int(1560 * s)
    fx, fy = gw / 2, gh - 60 * s
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, gw, gh)
    c = cairo.Context(surf)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    Y.figure(c, look, fx, fy, s, 0.0, p)
    surf.flush()
    a = np.ndarray((gh, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :gw].astype(np.float32) / 255.0
    al = a[..., 3]
    rgb = a[..., 2::-1] / np.maximum(al[..., None], 1e-4)          # un-premultiplied RGB (cairo stores BGRA)
    lum = 0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
    tone = 0.62 + 0.38 * np.clip(lum * 1.4, 0, 1)
    out = np.zeros((gh, gw, 4), np.float32)
    for i in range(3):
        out[..., i] = np.clip(col[i] * tone + 0.25 * (tone - 0.6), 0, 1) * al
    out[..., 3] = al
    k = 4
    small = gaussian_filter(al[::k, ::k], 7.0)
    small = np.clip(small * 1.6, 0, 1)
    gl = np.zeros(small.shape + (4,), np.float32)
    for i in range(3):
        gl[..., i] = col[i] * small
    gl[..., 3] = small
    return surface_from_rgba(out), surface_from_rgba(gl), (fx, fy), k


def ghost(cr, key, x, feet, s, alpha, col=SOUL, rot=0.0, glow=1.0, t=0.0):
    """Paint a figure of light (ghost_def'd as `key`) standing with its feet at (x, feet), scale s (relative to the
    scale it was made at), rotated by rot about its feet."""
    if alpha <= 0.01:
        return
    fs, gs, (fx, fy), k = ghost_surfaces(key, col)
    cr.save()
    cr.translate(x, feet)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.translate(-fx, -fy)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.scale(k, k)
    cr.set_source_surface(gs, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(alpha * glow * (0.85 + 0.15 * math.sin(t * 3.0)))
    cr.restore()
    cr.set_source_surface(fs, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(alpha * 0.92)
    cr.restore()


# ------------------------------------------------------------------ on-screen text pieces


def tag(cr, t, t_in, text, x, y, target=None, size=56, alpha=1.0, col=Y.YEL, field=Y.MAROON):
    """A small painted name tag (Kannada) centred at (x, y), with a short pointer to `target`."""
    q = clamp((t - t_in) / 0.3)
    if q <= 0 or alpha <= 0.01:
        return
    k = 0.6 + 0.4 * back(q, 2.0)
    s = Y.kn_surface(text, int(size), tuple(col), tuple(Y.INK), 5.0, None, 0.0)
    w, h = s.get_width() + 44, s.get_height() + 22
    a = clamp(q * 2) * alpha
    cr.save()
    if target is not None:
        tx, ty = target
        dy = (h / 2 + 4) * (1 if ty > y else -1)
        Y.stroke(cr, [(x, y + dy), (tx, ty)], 9, Y.INK, smooth=False, alpha=a)
        Y.stroke(cr, [(x, y + dy), (tx, ty)], 4, Y.GOLD, smooth=False, alpha=a)
        Y.dot(cr, tx, ty, 9 * a, Y.GOLD, 3.0)
    cr.translate(x, y)
    cr.scale(k, k)
    cr.push_group()
    cr.new_path()
    r = 14
    cr.move_to(-w / 2 + r, -h / 2)
    cr.arc(w / 2 - r, -h / 2 + r, r, -math.pi / 2, 0)
    cr.arc(w / 2 - r, h / 2 - r, r, 0, math.pi / 2)
    cr.arc(-w / 2 + r, h / 2 - r, r, math.pi / 2, math.pi)
    cr.arc(-w / 2 + r, -h / 2 + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()
    cr.set_source_rgb(*field)
    cr.fill_preserve()
    cr.set_source_rgb(*Y.GOLD)
    cr.set_line_width(5)
    cr.stroke()
    cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def red_ring(cr, x, y, rx, ry, p, alpha=1.0, w=10.0):
    """A hand-drawn red ring drawn round (x, y) as p goes 0 -> 1."""
    if p <= 0.01 or alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(rx, ry)
    cr.new_path()
    a0 = -2.2
    cr.arc(0, 0, 1.0, a0, a0 + 2 * math.pi * 1.08 * ease(p))
    cr.restore()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*Y.INK, alpha)
    cr.set_line_width(w + 6)
    cr.stroke_preserve()
    cr.set_source_rgba(0.90, 0.08, 0.08, alpha)
    cr.set_line_width(w)
    cr.stroke()


def underline(cr, x0, x1, y, p, alpha=1.0, w=12.0):
    if p <= 0.01:
        return
    xe = x0 + (x1 - x0) * ease(p)
    pts = [(x0, y), ((x0 + xe) / 2, y + 6), (xe, y - 2)]
    Y.stroke(cr, pts, w + 6, Y.INK, alpha=alpha)
    Y.stroke(cr, pts, w, (0.90, 0.08, 0.08), alpha=alpha)


def big_q(cr, t, t_in, x, y, size, alpha=1.0):
    """A big red "?" that pops in and wobbles."""
    q = back(clamp((t - t_in) / 0.35), 1.8)
    if q <= 0.01 or alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.10 + 0.05 * math.sin(t * 3))
    cr.scale(q, q)
    Y.kn_text(cr, "?", 0, 0, size, (0.90, 0.08, 0.08), Y.CREAM, 10, Y.INK, 8, alpha=clamp(q) * alpha)
    cr.restore()


def card(cr, t, t_in, x, y, w, h, lines, alpha=1.0, field=(0.20, 0.06, 0.06), rot=0.0, lit=0.0):
    """A painted cloth card (gold frame, dark field) with Kannada lines [(text, size, colour)], popping in at t_in.
    lit 0..1 brightens the frame (the red ring is drawn by the caller). Returns its box."""
    q = clamp((t - t_in) / 0.35)
    if q <= 0 or alpha <= 0.01:
        return None
    k = 0.5 + 0.5 * back(q, 1.8)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    cr.push_group()
    cr.rectangle(-w / 2 + 10, -h / 2 + 14, w, h)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    Y.ink_fill(cr, Y.GOLD, 7.0)
    cr.rectangle(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32)
    Y.ink_fill(cr, field, 5.0)
    for x_, y_ in Y.along([(-w / 2 + 28, -h / 2 + 28), (w / 2 - 28, -h / 2 + 28), (w / 2 - 28, h / 2 - 28),
                           (-w / 2 + 28, h / 2 - 28)], int((w + h) / 14), closed=True):
        Y.dot(cr, x_, y_, 2.6, Y.GOLD_HI)
    if lit > 0:
        Y.glow(cr, 0, 0, max(w, h) * 0.7, 0.25 * lit, (1.0, 0.8, 0.4))
    surfs = [Y.kn_surface(tx, int(sz), tuple(col), tuple(Y.INK), 6.0, None, 0.0) for tx, sz, col in lines]
    th = sum(s.get_height() for s in surfs) + 8 * (len(surfs) - 1)
    yy = -th / 2
    for s in surfs:
        sc = min(1.0, (w - 70) / s.get_width())
        cr.save()
        cr.translate(0, yy + s.get_height() * sc / 2)
        cr.scale(sc, sc)
        cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
        cr.paint()
        cr.restore()
        yy += s.get_height() * sc + 8
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha * clamp(q * 3))
    cr.restore()
    return x - w / 2, y - h / 2, w, h


def dust(cr, x, y, stamp, n=7, spread=1.0):
    """Dust and a jingle of light where a foot stamped (stamp 1 -> 0 after the stamp)."""
    if stamp <= 0.01:
        return
    for k in range(n):
        a = math.pi * (0.08 + 0.84 * k / (n - 1))
        d = (40 + 150 * (1 - stamp)) * spread
        Y.sparkle(cr, x - d * math.cos(a), y - 10 - d * 0.45 * math.sin(a), 20 * stamp, stamp)
    cr.save()
    cr.translate(x, y)
    cr.scale(1.0, 0.28)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 220 * spread)
    g.add_color_stop_rgba(0, 0.75, 0.55, 0.35, 0.45 * stamp)
    g.add_color_stop_rgba(1, 0.75, 0.55, 0.35, 0.0)
    cr.set_source(g)
    cr.arc(0, 0, 220 * spread, 0, 2 * math.pi)
    cr.fill()
    cr.restore()
