"""Yakshagana cast and props for the Kannada Mrityu reel (scenes_mrityu_yk), built on yaksha_kit (never edited: new
looks are dicts made from the kit's looks, a new body kind and new face paints are registered under "mry_" names).
Nothing here is shared with the Hindi shadow-puppet reel (scenes_mrityu).

Cast (one look each, kept the same through the reel; colours a child can follow):
  BRAHMA   the creator: the Kumbhakarna reel's Brahma (ky_yk_cast: a golden face with a long white beard and three of
           his four faces showing, each under a crown), in his red jacket. His palms (big, in close-up) catch her tears.
  SHIVA    ash-grey face with the three white lines of vibhuti, a white jacket, a tiger-coloured kase, a trident, a
           crescent moon by his crown, cool blue-white light.
  MRITYU   Death, a dignified young woman in a deep RED dancer's saree (draped round each leg to the calf, a pleated fan
           between the knees, so she can stand on one leg), a dark blouse, tawny skin, bright glowing earrings; sad
           and gentle, her tears are drops of blue-white light. Never a skull or a monster.
  BHOOMI   Mother Earth, a goddess in a GREEN saree with a small gold crown; she carries the crowded world.
Props: the world (a painted globe) with little Channapatna-toy people and animals standing round it, the palm-leaf
Mahabharata, glowing tears, Brahma's cupped palms in close-up, the diseases as small dark clouds, an hourglass, the
fire as light only (glow, rays, sparks; nobody burns), a small warm light for a life taken gently.
"""
import functools
import math

import cairo
import numpy as np

import ky_yk_cast as K
import sy_yk_cast as S
import yaksha_kit as Y
from poster import back, clamp, ease

INK = Y.INK

# ------------------------------------------------------------------ face paints (added to the kit's table)

ASH = (0.80, 0.82, 0.86)
TAWNY = (0.90, 0.62, 0.44)
Y.FACES.setdefault("mry_shiva", dict(base=ASH, mark="vibhuti", rouge=False, jaw=True, lips=Y.LIPS))
Y.FACES.setdefault("mry_death", dict(base=(0.94, 0.68, 0.50), mark="bindi", rouge=True, nosering=True, lips=Y.LIPS,
                                     lashes=True))

# ------------------------------------------------------------------ colours

DEATH_RED = (0.68, 0.04, 0.10)
DEATH_DK = (0.22, 0.04, 0.07)
EARTH_GREEN = (0.10, 0.52, 0.22)
TEAR = (0.72, 0.92, 1.0)             # her tears: blue-white light
TEAR_HI = (0.95, 1.0, 1.0)
FIRE = (1.0, 0.45, 0.10)             # Brahma's anger: orange light only
FIRE_HI = (1.0, 0.78, 0.30)
COOL = (0.70, 0.84, 1.0)             # Shiva's light
CLOUD = (0.33, 0.27, 0.40)           # the diseases: small dark clouds
CLOUD_DK = (0.17, 0.12, 0.22)
SOUL = (1.0, 0.92, 0.70)             # a life taken gently: a small warm light rising
BRAHMA_HAND = K.BRAHMA["hand"]
BRAHMA_SLEEVE = K.BRAHMA["sleeve"]

# ------------------------------------------------------------------ the dancer's body (Mrityu): each leg wrapped


def _as_woman(fn):
    """Run one of the kit's woman parts (arms with blouse sleeves and bangles, head, hair) for the dancer kind."""
    def g(ctx):
        lk = ctx.look
        ctx.look = dict(lk, kind="woman")
        try:
            fn(ctx)
        finally:
            ctx.look = lk
    return g


def _d_thigh(side):
    def fn(ctx):
        cr, look = ctx.cr, ctx.look
        Y.capsule(cr, 46, 38, Y.THIGH)
        Y.ink_fill(cr, look["saree"], 5.0)
        Y.stroke(cr, [(side * 30, 30), (side * 27, Y.THIGH - 14)], 6.0, Y.GOLD, alpha=0.9)
    return fn


def _d_shin(side):
    def fn(ctx):
        cr, look = ctx.cr, ctx.look
        Y.capsule(cr, 24, 17, Y.SHIN)
        Y.ink_fill(cr, look["skin"], 5.0)
        Y.shape(cr, [(-40, -18), (40, -18), (34, 98), (-34, 98)], look["saree"], 5.0, smooth=False)
        Y.stroke(cr, [(-34, 92), (34, 92)], 13.0, look.get("border", Y.GOLD), cap=cairo.LINE_CAP_BUTT)
        Y.stroke(cr, [(-34, 85), (34, 85)], 2.0)
        Y.stroke(cr, [(-34, 99), (34, 99)], 2.0)
        for k in range(5):                               # gejje: the ankle bells
            Y.dot(cr, -16 + 8 * k, 146, 5.0, Y.GOLD, 2.0)
        Y.stroke(cr, [(-19, 139), (19, 139)], 3.0, Y.RED)
    return fn


def _d_skirt(ctx):
    """The pleated fan between the knees and the cloth round the hips, with a gold belt."""
    cr, look = ctx.cr, ctx.look
    sar, bor = look["saree"], look.get("border", Y.GOLD)
    fan = [(-30, 40), (30, 40), (78, 300), (40, 314), (0, 318), (-40, 314), (-78, 300)]
    Y.shape(cr, fan, sar, 5.0, smooth=False)
    for k in range(-3, 4):
        Y.stroke(cr, [(k * 8, 46), (k * 22, 312)], 2.6, INK, alpha=0.55)
    Y.stroke(cr, [(-74, 296), (0, 310), (74, 296)], 14.0, bor)
    Y.stroke(cr, [(-74, 288), (0, 302), (74, 288)], 2.0)
    Y.shape(cr, [(-86, -10), (86, -10), (98, 64), (60, 88), (0, 96), (-60, 88), (-98, 64)], sar, 5.5)
    Y.stroke(cr, [(-96, 58), (-60, 80), (0, 88), (60, 80), (96, 58)], 10.0, bor)
    Y.shape(cr, [(-88, -18), (0, -24), (88, -18), (90, 8), (0, 2), (-90, 8)], Y.GOLD, 4.5)    # the oddiyana belt
    Y.dot_row(cr, [(-80, -7), (0, -12), (80, -7)], 11, 3.0, Y.RED)
    Y.oval(cr, 0, -8, 18, 14, Y.RED, 3.0)


def _dancer_parts():
    uL, lL = Y._arm(-1)
    uR, lR = Y._arm(1)
    w = _as_woman
    return [("head", w(Y.crown_back)), ("thighL", _d_thigh(-1)), ("thighR", _d_thigh(1)),
            ("shinL", _d_shin(-1)), ("shinR", _d_shin(1)), ("footL", w(Y._foot(-1))), ("footR", w(Y._foot(1))),
            ("root", _d_skirt), ("torso", w(Y.woman_torso)),
            ("uarmL", w(uL)), ("farmL", w(lL)), ("uarmR", w(uR)), ("farmR", w(lR)),
            ("head", w(Y.head)), ("head", w(Y.crown_front))]


Y.KINDS.setdefault("mry_dancer", _dancer_parts())     # registered under this module's own name (kit untouched)

# ------------------------------------------------------------------ looks

BRAHMA = dict(K.BRAHMA)
SHIVA = dict(S.SHIVA, face="mry_shiva", hand=(0.74, 0.76, 0.82), sleeve=(0.74, 0.76, 0.82),
             kase=(Y.SAFF, Y.INK, Y.INK, Y.YEL), disc_cols=(Y.GOLD, (0.30, 0.42, 0.70), Y.WHITE))
MRITYU = dict(Y.WOMAN, kind="mry_dancer", face="mry_death", saree=DEATH_RED, border=Y.GOLD, blouse=DEATH_DK,
              skin=TAWNY, hand=TAWNY)
BHOOMI = dict(Y.WOMAN, saree=EARTH_GREEN, border=Y.GOLD, blouse=Y.YEL, skin=(0.96, 0.72, 0.54),
              hand=(0.96, 0.72, 0.54), ky_goddess=True)

# ------------------------------------------------------------------ arm poses (upper, forearm, hand) in kit angles

REST = (0.16, 0.30, 0.0)
REST_DN = (0.12, 0.10, 0.0)
AKIMBO = (0.45, 1.35, 0.3)
ANJALI = (0.30, 2.30, 0.0)           # palms joined at the chest
FACE_HANDS = (0.25, 2.75, -0.3)      # both hands to the face (crying)
FACE_ONE = (0.30, 2.65, -0.3)
PALM_OUT = (1.25, -0.75, 0.25)       # an open palm raised to the side: stop / no
PALM_UP = (0.70, -2.44, 0.0)         # an open palm raised beside the face (stop, a blessing)
POINT = (1.45, 0.10, 0.0)            # the arm straight out to the side (an order: go!)
FIST_UP = (2.75, 0.15, 0.0)
HOLD_UP = (2.25, -0.85, 0.0)         # both arms up and out, the palms pushing up a load on her shoulders
CUP = (0.10, 1.95, 0.0)              # forearms forward, the hands together in front of the belly
PLEAD = (0.62, -0.55, 0.0)           # open hands held out low at the sides: helpless, pleading
HANDS_UP = (2.42, -1.50, 0.0)        # both arms up, the palms meeting over the head


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
    """Draw an actor (with the Kumbhakarna reel's extra parts: Brahma's side faces, the goddess crown) and a soft
    shadow on the boards under the feet."""
    if shadow:
        Y.floor_shadow(c, x + p.get("shift", 0.0) * s, feet, 300 * s, shadow * alpha)
    return K.figure(c, look, x, feet, s, t, p, flip, alpha)


def U(c, p):
    """Device point -> the context's user space."""
    return Y.to_user(c, p)


# ------------------------------------------------------------------ tears (drops of blue-white light)


def tear(cr, x, y, s, a=1.0, col=TEAR, glow=True):
    """One glowing tear drop, its point up, centred at (x, y)."""
    if a <= 0.01:
        return
    if glow:
        Y.glow(cr, x, y, 46 * s, 0.55 * a, col)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    cr.move_to(0, -18)
    cr.curve_to(7, -6, 12, 4, 12, 10)
    cr.curve_to(12, 19, -12, 19, -12, 10)
    cr.curve_to(-12, 4, -7, -6, 0, -18)
    cr.close_path()
    cr.set_source_rgba(*col, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(2.6)
    cr.stroke()
    Y.dot(cr, -4, 6, 3.2, (1, 1, 1))
    cr.restore()


def tears_from(cr, t, face, s, a=1.0, rate=1.0, fall=170.0, n=2, seed=0.0):
    """Tears running down from both eyes of a woman's face (face = its centre in user space, s = figure scale)."""
    if a <= 0.01:
        return
    fx, fy = face
    for sd in (-1, 1):
        Y.glow(cr, fx + sd * 36 * s, fy + 8 * s, 30 * s, 0.14 * a, TEAR)
        for k in range(n):
            u = ((t - seed) * 0.9 * rate + k / n + (0.25 if sd > 0 else 0.0)) % 1.0
            x = fx + sd * 40 * s + sd * 8 * s * u
            y = fy + 22 * s + fall * s * u
            tear(cr, x, y, 0.95 * s, a * clamp((1 - u) * 2.5) * clamp(u * 6))


def earrings_glow(cr, t, face, s, a=1.0):
    """Her bright earrings (the source: "with bright earrings"): two small warm glints."""
    if a <= 0.01:
        return
    fx, fy = face
    for sd in (-1, 1):
        x, y = fx + sd * 72 * s * 1.1, fy + 52 * s * 1.1
        Y.glow(cr, x, y, 24 * s, 0.22 * a, (1.0, 0.82, 0.40))
        Y.sparkle(cr, x, y, (10 + 4 * math.sin(t * 4 + sd)) * s, 0.6 * a)


# ------------------------------------------------------------------ Brahma's cupped palms (close-up)


def _shade(c, k):
    return tuple(max(0.0, min(1.0, v * k)) for v in c)


def palms(cr, t, x, y, s, pool=1.0, glow_a=1.0, dark=0.0, drops=3, sleeve=BRAHMA_SLEEVE, hand=BRAHMA_HAND):
    """Brahma's two palms held together like a bowl (palms up, fingers rising at the far rim, the wrists coming up
    from below in red sleeves with gold cuffs), centred at (x, y) = the middle of the bowl; s = 1.0 is about 600 px
    wide. pool 0..1 = how much of her light lies in it; dark 0..1 turns that light dark (the diseases).
    Returns the pool's centre (user space)."""
    back_col = _shade(hand, 0.86)
    palm_col = _shade(hand, 1.06)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for sd in (-1, 1):                                    # sleeves and cuffs coming up from below
        Y.shape(cr, [(sd * 40, 330), (sd * 250, 330), (sd * 280, 900), (sd * 20, 900)], sleeve, 7.0, smooth=False)
        Y.shape(cr, [(sd * 70, 150), (sd * 215, 150), (sd * 225, 340), (sd * 60, 340)], back_col, 6.0, smooth=False)
        Y.shape(cr, [(sd * 50, 300), (sd * 240, 300), (sd * 246, 372), (sd * 44, 372)], Y.GOLD, 6.0, smooth=False)
        Y.stroke(cr, [(sd * 48, 336), (sd * 243, 336)], 12.0, Y.RED, cap=cairo.LINE_CAP_BUTT)
        Y.dot_row(cr, [(sd * 56, 314), (sd * 236, 314)], 7, 4.0, Y.WHITE)
    rx, ry = 270.0, 104.0

    def rim_y(px):
        return -ry * math.sqrt(max(0.0, 1 - (px / rx) ** 2))
    lens = (118, 150, 166, 150)                           # little, ring, middle, index (from the middle outward)
    for sd in (-1, 1):                                    # the fingers, rising from the far rim
        for j, (bx, L) in enumerate(zip((38, 100, 162, 220), lens)):
            px = sd * bx
            cr.save()
            cr.translate(px, rim_y(px) + 18)
            cr.rotate(math.pi + sd * (0.04 + 0.11 * j))
            Y.capsule(cr, 30, 25, L)
            Y.ink_fill(cr, hand, 6.0)
            Y.oval(cr, 0, L - 6, 13, 16, _shade(hand, 1.12), 2.5)
            Y.stroke(cr, [(-14, L * 0.45), (14, L * 0.45)], 2.5, alpha=0.5)
            cr.restore()
    outer = [(-292, -14), (-282, 70), (-232, 150), (-128, 206), (0, 222), (128, 206), (232, 150), (282, 70),
             (292, -14), (0, -14)]
    Y.shape(cr, outer[:-1] + [(240, -40), (-240, -40)], back_col, 7.0)
    cr.new_path()
    Y.ell(cr, 0, 0, rx, ry, 0.0)
    Y.ink_fill(cr, palm_col, 6.0)
    cr.save()
    cr.new_path()
    Y.ell(cr, 0, 0, rx, ry, 0.0)
    cr.clip()
    for sd in (-1, 1):                                    # palm lines and the seam where the hands meet
        Y.stroke(cr, [(sd * 40, -60), (sd * 110, -10), (sd * 210, -30)], 3.0, _shade(hand, 0.62), alpha=0.7)
        Y.stroke(cr, [(sd * 60, 40), (sd * 150, 20), (sd * 230, 30)], 3.0, _shade(hand, 0.62), alpha=0.7)
    Y.stroke(cr, [(0, -104), (-4, 0), (0, 104)], 5.0, _shade(hand, 0.5), alpha=0.8)
    pc = (0.0, 26.0)
    if pool > 0.01:
        k = math.sqrt(clamp(pool))
        col = mix(TEAR, CLOUD, dark)
        cr.new_path()
        Y.ell(cr, pc[0], pc[1], 205 * k, 66 * k, 0.0)
        cr.set_source_rgba(*col, 0.95)
        cr.fill_preserve()
        cr.set_source_rgba(*mix((0.30, 0.55, 0.80), CLOUD_DK, dark), 1.0)
        cr.set_line_width(4)
        cr.stroke()
        cr.new_path()
        Y.ell(cr, pc[0] - 30 * k, pc[1] - 16 * k, 110 * k, 22 * k, 0.0)
        cr.set_source_rgba(*mix(TEAR_HI, CLOUD, dark), 0.8)
        cr.fill()
        for i in range(drops):                            # single tears resting in the pool
            ang = i * 2.1 + 0.4
            tear(cr, pc[0] + 120 * k * math.cos(ang), pc[1] + 30 * k * math.sin(ang) - 6, 1.5,
                 1.0 - dark, mix(TEAR, CLOUD, dark), glow=False)
    cr.restore()
    Y.stroke(cr, [(-rx, 4), (-200, 72), (0, 106), (200, 72), (rx, 4)], 6.0, _shade(hand, 1.12), alpha=0.8)
    for sd in (-1, 1):                                    # the thumbs on the outer sides
        cr.save()
        cr.translate(sd * 268, 40)
        cr.rotate(math.pi + sd * 0.55)
        Y.capsule(cr, 30, 26, 120)
        Y.ink_fill(cr, hand, 6.0)
        Y.oval(cr, 0, 112, 13, 16, _shade(hand, 1.12), 2.5)
        cr.restore()
    cr.restore()
    if pool > 0.01:
        Y.glow(cr, x + pc[0] * s, y + pc[1] * s, 330 * s * math.sqrt(pool), 0.75 * glow_a * (1 - dark), TEAR)
        Y.sparks(cr, t, x, y + pc[1] * s, 200 * s, 6, glow_a * (1 - dark) * clamp(pool), 0.35, seed=11)
    return x + pc[0] * s, y + pc[1] * s


# ------------------------------------------------------------------ the diseases: small dark clouds

_PUFFS = ((-42, 6, 32), (-12, -20, 40), (28, -10, 36), (50, 12, 26), (10, 18, 32), (-26, 22, 26))


def cloud(cr, t, x, y, s, a=1.0, seed=0.0, col=CLOUD):
    """A small dark cloud (a disease): soft puffs with one outline, a darker underside, a few dark specks; it bobs."""
    if a <= 0.01 or s <= 0.01:
        return
    bob = 6 * math.sin(t * 2.6 + seed * 1.7)
    cr.save()
    cr.translate(x, y + bob * s)
    cr.scale(s, s)
    cr.rotate(0.06 * math.sin(t * 1.9 + seed))
    cr.push_group()
    cr.new_path()
    for px, py, r in _PUFFS:
        cr.new_sub_path()
        cr.arc(px, py, r, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(14)
    cr.stroke_preserve()
    cr.set_source_rgb(*col)
    cr.fill()
    cr.save()
    cr.new_path()
    for px, py, r in _PUFFS:
        cr.new_sub_path()
        cr.arc(px, py, r - 1, 0, 2 * math.pi)
    cr.clip()
    cr.rectangle(-90, 14, 180, 60)
    cr.set_source_rgba(*CLOUD_DK, 0.75)
    cr.fill()
    for i, (px, py) in enumerate(((-30, -4), (6, -18), (30, 2), (-6, 10))):      # specks (germs)
        Y.dot(cr, px + 3 * math.sin(t * 3 + i + seed), py, 5.5, CLOUD_DK)
    Y.dot(cr, -18, -24, 7, (0.55, 0.50, 0.62))
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def soul(cr, t, x, y, a=1.0, r=16.0):
    """A small warm light (a life taken gently, without pain)."""
    if a <= 0.01:
        return
    Y.glow(cr, x, y, r * 6, 0.5 * a, SOUL)
    Y.glow(cr, x, y, r * 2.2, 0.9 * a, (1.0, 0.98, 0.88))
    Y.sparkle(cr, x, y, r * 2.4, 0.8 * a)


# ------------------------------------------------------------------ little Channapatna-toy people and animals

PEOPLE = ("man", "woman", "child")
ANIMALS = ("cow", "elephant", "deer")
DOLL_COLS = (Y.RED, Y.GREEN, (0.98, 0.70, 0.08), Y.BLUE, (0.92, 0.40, 0.08), (0.56, 0.16, 0.58), (0.06, 0.56, 0.62))
_TOY_SKIN = (0.98, 0.80, 0.58)


def _doll_person(cr, kind, col):
    k = 0.78 if kind == "child" else 1.0
    cr.save()
    cr.scale(k, k)
    Y.oval(cr, 0, -5, 24, 7, (0.70, 0.46, 0.20), 3.0)
    if kind == "woman":
        body = [(-27, -6), (27, -6), (18, -40), (13, -60), (-13, -60), (-18, -40)]
    else:
        body = [(-21, -6), (21, -6), (18, -38), (15, -60), (-15, -60), (-18, -38)]
    Y.shape(cr, body, col, 3.5, smooth=False)
    cr.save()
    cr.new_path()
    Y.poly(cr, body)
    cr.clip()
    for yy, c2 in ((-20, Y.GOLD), (-44, INK)):
        Y.stroke(cr, [(-30, yy), (30, yy)], 5.0 if c2 == Y.GOLD else 2.5, c2, cap=cairo.LINE_CAP_BUTT)
    cr.restore()
    Y.dot(cr, 0, -76, 17, _TOY_SKIN, 3.0)
    cr.new_path()
    cr.arc(0, -78, 17, math.pi * 1.05, math.pi * 1.95)
    cr.close_path()
    Y.ink_fill(cr, INK, 0)
    if kind == "woman":
        Y.dot(cr, 0, -96, 8, INK)
        Y.dot(cr, 0, -72, 2.2, Y.RED)
    elif kind == "man":
        Y.shape(cr, [(-18, -86), (18, -86), (14, -98), (-14, -98)], (0.98, 0.95, 0.88), 2.5, smooth=False)
    else:
        Y.dot(cr, 0, -97, 6, INK)
    for sd in (-1, 1):
        Y.dot(cr, sd * 6, -76, 2.4, INK)
    Y.stroke(cr, [(-5, -68), (0, -66), (5, -68)], 2.0, Y.RED)
    cr.restore()


def _doll_animal(cr, kind, col):
    if kind == "cow":
        for lx in (-26, -12, 14, 28):
            Y.shape(cr, [(lx - 4, -30), (lx + 4, -30), (lx + 4, -2), (lx - 4, -2)], (0.90, 0.88, 0.82), 2.5,
                    smooth=False)
        Y.oval(cr, 0, -36, 40, 18, (0.97, 0.95, 0.90), 3.5)
        Y.dot(cr, 16, -50, 9, (0.97, 0.95, 0.90), 3.0)
        Y.dot(cr, -12, -36, 6, (0.40, 0.30, 0.25))
        Y.stroke(cr, [(-40, -36), (-50, -22)], 3.0)
        Y.oval(cr, 44, -48, 13, 10, (0.97, 0.95, 0.90), 3.0, rot=0.4)
        for sd in (-1, 1):
            Y.stroke(cr, [(44 + sd * 6, -56), (44 + sd * 12, -68), (44 + sd * 8, -74)], 3.0, (0.60, 0.40, 0.20))
        Y.dot(cr, 48, -48, 2.0, INK)
        Y.shape(cr, [(-14, -54), (14, -54), (12, -40), (-12, -40)], col, 2.5, smooth=False)
    elif kind == "elephant":
        grey = (0.60, 0.58, 0.64)
        for lx in (-24, -8, 12, 26):
            Y.shape(cr, [(lx - 7, -34), (lx + 7, -34), (lx + 7, -2), (lx - 7, -2)], grey, 2.5, smooth=False)
        Y.oval(cr, 0, -44, 42, 26, grey, 3.5)
        Y.dot(cr, 40, -54, 18, grey, 3.0)
        Y.stroke(cr, [(52, -48), (60, -28), (56, -10)], 9.0, INK)
        Y.stroke(cr, [(52, -48), (60, -28), (56, -10)], 4.5, grey)
        Y.oval(cr, 30, -52, 9, 13, (0.52, 0.50, 0.56), 2.5)
        Y.dot(cr, 46, -60, 2.2, INK)
        Y.shape(cr, [(-26, -70), (22, -70), (26, -40), (-30, -40)], col, 3.0, smooth=False)
        Y.stroke(cr, [(-30, -44), (26, -44)], 4.0, Y.GOLD)
    else:                                                 # deer
        brown = (0.80, 0.50, 0.22)
        for lx in (-20, -10, 12, 22):
            Y.stroke(cr, [(lx, -28), (lx, -2)], 5.0, INK)
            Y.stroke(cr, [(lx, -28), (lx, -2)], 2.5, brown)
        Y.oval(cr, 0, -34, 30, 13, brown, 3.0)
        Y.stroke(cr, [(24, -40), (32, -58)], 8.0, INK)
        Y.stroke(cr, [(24, -40), (32, -58)], 5.0, brown)
        Y.oval(cr, 38, -60, 11, 7, brown, 2.5, rot=0.3)
        for sd in (-6, 2):
            Y.stroke(cr, [(32 + sd, -66), (28 + sd, -80), (22 + sd, -86)], 2.5, (0.50, 0.30, 0.12))
        for px, py in ((-12, -36), (0, -40), (10, -34)):
            Y.dot(cr, px, py, 2.6, (1, 0.95, 0.85))
        Y.dot(cr, 42, -61, 1.8, INK)


@functools.lru_cache(maxsize=64)
def doll_surface(kind, ci):
    """(surface, feet x, feet y, px per unit): a toy person or animal drawn once (about 100 units tall)."""
    k = 2.0
    w, h = int(150 * k), int(130 * k)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.translate(w / 2, h - 8 * k)
    c.scale(k, k)
    col = DOLL_COLS[ci % len(DOLL_COLS)]
    if kind in PEOPLE:
        _doll_person(c, kind, col)
    else:
        _doll_animal(c, kind, col)
    s.flush()
    return s, w / 2, h - 8 * k, k


def doll(cr, kind, ci, x, y, size, rot=0.0, a=1.0, pop=1.0):
    """A toy standing with its feet at (x, y), about `size` px tall, rotated by rot about its feet."""
    if a <= 0.01 or pop <= 0.01:
        return
    s, fx, fy, k = doll_surface(kind, ci)
    sc = size / 100.0 / k * back(clamp(pop), 2.2)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(sc, sc)
    cr.set_source_surface(s, -fx, -fy)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(a * clamp(pop * 3))
    cr.restore()


def _spots():
    """Places for the crowd on the world: rim spots (standing out from the top of the ball, radially) and face spots
    (standing upright on its lands), in the order they appear; people and animals mixed."""
    rng = np.random.default_rng(5)
    rim = [-1.62 + 3.24 * (i + 0.5) / 26 for i in range(26)]
    rim = [rim[i] for i in rng.permutation(26)]
    face = []
    for row, (v, n) in enumerate(((-0.42, 4), (-0.15, 6), (0.12, 7), (0.40, 6), (0.64, 4))):
        for j in range(n):
            u = (j + 0.5) / n * 2 - 1
            face.append((u * math.sqrt(max(0.0, 1 - v * v)) * 0.80, v + rng.uniform(-0.04, 0.04)))
    face = [face[i] for i in rng.permutation(len(face))]
    out = []
    while rim or face:                                    # mostly one rim spot, one face spot, in turn
        if rim:
            out.append(("rim", rim.pop(0)))
        if face:
            out.append(("face", face.pop(0)))
    kinds = []
    for i in range(len(out)):
        kinds.append(ANIMALS[(i // 3) % 3] if i % 3 == 2 else PEOPLE[(i * 7) % 3])
    return [(m, p, kd, (i * 3) % len(DOLL_COLS)) for i, ((m, p), kd) in enumerate(zip(out, kinds))]


SPOTS = _spots()
N_PEOPLE = sum(1 for s_ in SPOTS if s_[2] in PEOPLE)
N_ANIMALS = len(SPOTS) - N_PEOPLE


def spot_xy(i, x, y, r):
    """(feet x, feet y, rotation) of crowd spot i on a world drawn at (x, y) with radius r."""
    m, p, _, _ = SPOTS[i]
    if m == "rim":
        return x + r * math.sin(p), y - r * math.cos(p) + 4, p
    u, v = p
    return x + r * u, y + r * v + 0.07 * r, 0.0


def earth(cr, t, x, y, r, people=0.0, animals=0.0, a=1.0, heat=0.0, gone=None, spin=0.0, size=None, sick=None):
    """The world: the painted globe with the toy crowd on it. people / animals = how many have appeared (fractions pop
    in); heat 0..1 = Brahma's fire as an orange light over it; gone = {spot: 0..1} lives taken gently (the toy fades
    to a small warm light that rises); sick = {spot: 0..1} a dark tint on that toy."""
    if a <= 0.01:
        return
    gone = gone or {}
    sick = sick or {}
    if heat > 0.01:
        Y.glow(cr, x, y, r * 2.2, 0.55 * heat, FIRE)
    K.globe(cr, t, x, y, r, a, spin)
    if heat > 0.01:
        cr.save()
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.clip()
        g = cairo.RadialGradient(x, y + r * 0.5, 0, x, y, r * 1.2)        # the world washed orange-red
        hw = 0.92 * clamp(heat * 1.5)
        g.add_color_stop_rgba(0, 1.0, 0.52, 0.06, hw)
        g.add_color_stop_rgba(1, 0.80, 0.14, 0.02, hw)
        cr.set_source(g)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_ADD)
        g = cairo.RadialGradient(x, y + r * 0.9, 0, x, y + r * 0.9, r * 1.1)
        g.add_color_stop_rgba(0, 1.0, 0.70, 0.25, 0.22 * heat * (0.85 + 0.15 * math.sin(t * 9)))
        g.add_color_stop_rgba(1, 1.0, 0.40, 0.10, 0.0)
        cr.set_source(g)
        cr.paint()
        cr.restore()
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(7)
        cr.stroke()
    sz = size or r * 0.24
    ip = ia = 0
    for i, (m, p, kind, ci) in enumerate(SPOTS):
        if kind in PEOPLE:
            pop = clamp(people - ip)
            ip += 1
        else:
            pop = clamp(animals - ia)
            ia += 1
        if pop <= 0.01:
            continue
        fx, fy, rot = spot_xy(i, x, y, r)
        g_ = gone.get(i, 0.0)
        if g_ < 0.999:
            doll(cr, kind, ci, fx, fy, sz * (0.85 if m == "face" else 1.0), rot, a * (1 - g_), pop)
            sk = sick.get(i, 0.0)
            if sk > 0.01:
                cr.save()
                cr.translate(fx, fy)
                cr.rotate(rot)
                cr.new_path()
                cr.arc(0, -sz * 0.45, sz * 0.55, 0, 2 * math.pi)
                cr.set_source_rgba(*CLOUD_DK, 0.60 * sk * a)
                cr.fill()
                cr.restore()
        if g_ > 0.01:
            up = ease(g_)
            soul(cr, t, fx + math.sin(rot) * sz * (0.6 + 1.6 * up), fy - math.cos(rot) * sz * (0.6 + 1.6 * up),
                 a * clamp(g_ * 3) * clamp((1 - g_) * 4 + 0.25), 16 + 6 * up)
    if heat > 0.01:                                       # heat shimmering up off the world (light only)
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        for k in range(4):
            u = (t * 0.7 + k / 4) % 1.0
            yy = y - r * 0.9 - 30 - 200 * u
            w_ = r * (0.7 - 0.3 * u)
            pts = [(x - w_ + 2 * w_ * j / 12, yy + 12 * math.sin(j * 1.3 + t * 5 + k)) for j in range(13)]
            Y.stroke(cr, pts, 7, (1.0, 0.70, 0.30), alpha=0.75 * heat * math.sin(math.pi * u))
        cr.restore()
        Y.sparks(cr, t, x, y - r * 0.6, r * 1.1, 10, heat, 0.6, seed=3)


def hover_doll(cr, t, x, y, size, a=1.0, ci=2):
    """One more toy person bobbing just above the crowd: there is no room to put a foot down."""
    bob = abs(math.sin(t * 4.2)) * size * 0.35
    doll(cr, "man", ci, x, y - bob, size, 0.08 * math.sin(t * 4.2), a)
    return x, y - bob


def weight_arrows(cr, t, x, y, w, a=1.0, n=3):
    """Thick red arrows pushing down (a heavy load)."""
    if a <= 0.01:
        return
    for k in range(n):
        xx = x + (k - (n - 1) / 2) * w
        yy = y + 14 * math.sin(t * 5 + k)
        pts = [(xx - 16, yy - 70), (xx + 16, yy - 70), (xx + 16, yy - 10), (xx + 34, yy - 10), (xx, yy + 30),
               (xx - 34, yy - 10), (xx - 16, yy - 10)]
        cr.save()
        cr.push_group()
        Y.shape(cr, pts, (0.90, 0.10, 0.08), 6.0, smooth=False)
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
        cr.restore()


def sweat(cr, t, face, s, a=1.0):
    """Drops of sweat flicking off a tired face."""
    if a <= 0.01:
        return
    fx, fy = face
    for k, sd in enumerate((-1, 1, -1)):
        u = (t * 1.1 + k * 0.37) % 1.0
        x = fx + sd * (90 + 60 * u) * s
        y = fy - (60 - 120 * u * u) * s
        tear(cr, x, y, 0.9 * s / 0.7, a * (1 - u), (0.80, 0.94, 1.0), glow=False)


# ------------------------------------------------------------------ fire as light only, Shiva's cool light


def fire_light(cr, t, x, y, r, a=1.0):
    """Brahma's anger as a fire of LIGHT behind him: an orange glow, turning rays and rising sparks (no flames on
    anyone)."""
    if a <= 0.01:
        return
    f = 0.85 + 0.15 * math.sin(t * 9) * math.sin(t * 5.3)
    Y.glow(cr, x, y, r * 1.9, 0.55 * a * f, FIRE)
    Y.glow(cr, x, y, r * 1.0, 0.65 * a * f, FIRE_HI)
    Y.rays(cr, t, x, y, r * 0.25, r * 2.6, 0.9 * a, 26, (1.0, 0.50, 0.12), 0.35)
    Y.sparks(cr, t, x, y + r * 0.5, r * 1.3, 14, a, 0.7, seed=2)


def tint(cr, col, a, rect=None):
    """A flat wash of colour (over the backdrop, or a rectangle of it)."""
    if a <= 0.01:
        return
    cr.save()
    if rect:
        cr.rectangle(*rect)
        cr.clip()
    cr.set_source_rgba(*col, a)
    cr.paint()
    cr.restore()


def streams_in(cr, t, x, y, r, u, a=1.0, col=FIRE_HI, n=26):
    """Streaks of orange light pulled in from all round into (x, y): u 0..1 how far the pull has gone."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        ang = i * 2.399
        ph = (u * 1.8 + i / n) % 1.0
        d1 = r * (1 - ph) * (1.0 - 0.5 * u) + 30
        d0 = d1 + 120 * (1 - ph) + 30
        p0 = (x + d0 * math.cos(ang), y + d0 * math.sin(ang))
        p1 = (x + d1 * math.cos(ang), y + d1 * math.sin(ang))
        al = a * clamp(ph * 5) * (0.4 + 0.6 * (1 - ph))
        for lw, k in ((22, 0.25), (9, 0.6), (3.5, 1.0)):
            g = cairo.LinearGradient(p0[0], p0[1], p1[0], p1[1])
            g.add_color_stop_rgba(0, *FIRE, 0.0)
            g.add_color_stop_rgba(1, *col, al * k)
            cr.set_source(g)
            cr.set_line_width(lw)
            cr.move_to(*p0)
            cr.line_to(*p1)
            cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ small props


def hourglass(cr, t, x, y, s, u, a=1.0):
    """An hourglass standing with its foot at (x, y); u 0..1 = how much sand has run down."""
    if a <= 0.01:
        return
    u = clamp(u)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    wood = (0.50, 0.24, 0.10)
    for py in (-30, -330):
        Y.shape(cr, [(-110, py), (110, py), (100, py + 30), (-100, py + 30)], wood, 6.0, smooth=False)
        Y.stroke(cr, [(-100, py + 15), (100, py + 15)], 5.0, Y.GOLD)
    top = [(-80, -300), (80, -300), (70, -230), (12, -180), (-12, -180), (-70, -230)]
    bot = [(-12, -180), (12, -180), (70, -130), (80, -30), (-80, -30), (-70, -130)]
    glass = (0.80, 0.92, 1.0)
    Y.shape(cr, top, glass, 5.0, smooth=True)
    Y.shape(cr, bot, glass, 5.0, smooth=True)
    sand = (0.98, 0.78, 0.30)
    cr.save()
    cr.new_path()
    Y.spath(cr, top)
    cr.clip()
    ht = 110 * (1 - u)
    cr.rectangle(-90, -180 - ht, 180, ht)
    cr.set_source_rgb(*sand)
    cr.fill()
    cr.restore()
    cr.save()
    cr.new_path()
    Y.spath(cr, bot)
    cr.clip()
    hb = 120 * u
    cr.new_path()
    cr.move_to(-90, -30)
    cr.line_to(-90, -30 - hb * 0.6)
    cr.line_to(0, -30 - hb)
    cr.line_to(90, -30 - hb * 0.6)
    cr.line_to(90, -30)
    cr.close_path()
    cr.set_source_rgb(*sand)
    cr.fill()
    cr.restore()
    if 0.0 < u < 1.0:
        Y.stroke(cr, [(0, -182), (0, -32 - 120 * u)], 5.0, sand)
    for sd in (-1, 1):
        Y.shape(cr, [(sd * 96, -300), (sd * 104, -300), (sd * 104, -30), (sd * 96, -30)], wood, 4.0, smooth=False)
    Y.stroke(cr, [(-50, -280), (-30, -240)], 5.0, (1, 1, 1), alpha=0.7)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def book_stand(cr, x, top, floor, w=520.0):
    """A carved wooden book-rest (two crossed boards) holding a book whose bottom is at `top`, standing on `floor`."""
    wood, hi = (0.50, 0.24, 0.10), (0.72, 0.42, 0.16)
    for sd in (-1, 1):
        Y.shape(cr, [(x + sd * w * 0.48, top + 10), (x + sd * w * 0.36, top + 10), (x - sd * w * 0.30, floor),
                     (x - sd * w * 0.42, floor)], wood, 6.0, smooth=False)
    Y.shape(cr, [(x - w * 0.52, top - 6), (x + w * 0.52, top - 6), (x + w * 0.48, top + 26), (x - w * 0.48, top + 26)],
            hi, 6.0, smooth=False)
    Y.dot_row(cr, [(x - w * 0.44, top + 10), (x + w * 0.44, top + 10)], 9, 5.0, Y.GOLD, lw=2.0)
    Y.oval(cr, x, top + (floor - top) * 0.52, 26, 26, Y.GOLD, 5.0)
    Y.dot(cr, x, top + (floor - top) * 0.52, 9, Y.RED, 2.5)


def red_x(cr, x, y, r, p, a=1.0, w=24.0):
    """A big red X drawn stroke by stroke as p goes 0 -> 1."""
    if p <= 0.01 or a <= 0.01:
        return
    for k, (p0, p1) in enumerate((((-r, -r), (r, r)), ((r, -r), (-r, r)))):
        u = clamp(p * 2 - k)
        if u <= 0:
            continue
        e = (p0[0] + (p1[0] - p0[0]) * ease(u), p0[1] + (p1[1] - p0[1]) * ease(u))
        Y.stroke(cr, [(x + p0[0], y + p0[1]), (x + e[0], y + e[1])], w + 10, INK, smooth=False, alpha=a)
        Y.stroke(cr, [(x + p0[0], y + p0[1]), (x + e[0], y + e[1])], w, (0.90, 0.08, 0.06), smooth=False, alpha=a)


def tick(cr, x, y, r, p, a=1.0, w=26.0, col=(0.15, 0.68, 0.25)):
    if p <= 0.01 or a <= 0.01:
        return
    pts = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    u = clamp(p) * 2
    if u <= 1:
        seg = [pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * u, pts[0][1] + (pts[1][1] - pts[0][1]) * u)]
    else:
        v = u - 1
        seg = [pts[0], pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * v, pts[1][1] + (pts[2][1] - pts[1][1]) * v)]
    Y.stroke(cr, seg, w + 10, INK, smooth=False, alpha=a)
    Y.stroke(cr, seg, w, col, smooth=False, alpha=a)


def lotus_seat(cr, x, y, w):
    K.lotus_seat(cr, x, y, w)


def globe(cr, t, x, y, r, a=1.0, spin=0.0):
    K.globe(cr, t, x, y, r, a, spin)


def trishula(cr, x, y, s, rot=0.0, alpha=1.0):
    S.trishula(cr, x, y, s, rot, alpha)


def crescent(cr, x, y, r, alpha=1.0):
    S.crescent(cr, x, y, r, alpha)
