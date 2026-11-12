"""Yakshagana (Karnataka's night theatre of the coast and Malnad) drawn in code: the art style for the Kannada
mythology reels, so they no longer share the Togalu Gombeyaata shadow-puppet pictures of the Hindi reels.

The look (every frame a pure function of t):
  stage(cr, t)            a night stage: dark sky, a mango-leaf and marigold thorana across the top, two posts wrapped
                          in red and white cloth with banana leaves, a painted thera (backdrop cloth) with bold
                          borders, wooden boards; optional small silhouettes of the bhagavata and the chende drummer
  figure(cr, look, ...)   jointed costumed actors, flat bold colours and thick black outlines, facing the audience:
                          kireeta / kedige mundale / demon / small crowns, mukhavarna face paint (white dot rows, long
                          black eye lines, namam or vibhuti), edehara chest plate, bhujakeerthi shoulder wings, a puffed
                          checked kase skirt with sashes and tassels, leg pads covered in bells. A `turn` parameter
                          shifts the features for a three-quarter look; moods: calm, wonder, angry, joy, sad, fierce
  lamps(cr, t)            a row of brass oil lamps along the front edge (flickering flames)
  light(cr, t)            warm light from the lamps below, darker sky above, a flicker
  finish(cr, t)           a canvas / paper texture over everything
  kn_headline / kn_banner Kannada text, shaped correctly (matplotlib's libraqm layout with Nirmala UI Bold), with
                          bold outlines so it reads at phone size

No translucent leather, no punched holes, no rods: flat painted shapes, nothing like the shadow-puppet reels.
Figures are drawn in "design units": a standing actor is about 1230 units from the feet to the tip of a kireeta (the
waist is the root at (0, 0), the soles 440 units below it when standing straight).
"""
import functools
import math
import os

import cairo
import numpy as np
from scipy.ndimage import gaussian_filter

from poster import H, W, back, clamp, ease, prog
from puppet_core import ell, flicker, poly, spath, surface_from_rgba

# ------------------------------------------------------------------ palette (saturated, Yakshagana stage colours)

INK = (0.055, 0.035, 0.035)
RED = (0.82, 0.07, 0.07)
CRIMSON = (0.56, 0.03, 0.07)
MAROON = (0.32, 0.02, 0.05)
VERM = (0.92, 0.30, 0.10)
SAFF = (0.98, 0.55, 0.10)
YEL = (0.99, 0.80, 0.12)
GOLD = (0.97, 0.72, 0.16)
GOLD_HI = (1.0, 0.92, 0.55)
GOLD_DK = (0.70, 0.42, 0.06)
GREEN = (0.03, 0.50, 0.24)
DGREEN = (0.02, 0.30, 0.15)
LEAF = (0.32, 0.66, 0.16)
DLEAF = (0.06, 0.38, 0.13)
BLUE = (0.10, 0.26, 0.68)
WHITE = (0.99, 0.97, 0.91)
CREAM = (1.0, 0.94, 0.76)
MIRROR = (0.84, 0.97, 1.0)
PINK = (0.99, 0.62, 0.58)
BLACK = (0.10, 0.07, 0.08)
SKIN = (0.93, 0.64, 0.40)
SAGE_SKIN = (0.96, 0.76, 0.56)
LIPS = (0.86, 0.06, 0.10)
ORB = (1.0, 0.80, 0.30)
LW = 7.0                                   # the main black outline, in design units

# ------------------------------------------------------------------ small drawing helpers (design units)


def ink_fill(cr, col, lw=LW, alpha=1.0):
    """Fill the current path flat and stroke it with the thick black outline."""
    cr.set_source_rgba(*col, alpha)
    if lw:
        cr.fill_preserve()
        cr.set_source_rgba(*INK, alpha)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    else:
        cr.fill()


def shape(cr, pts, col, lw=LW, smooth=True):
    cr.new_path()
    (spath if smooth else poly)(cr, pts)
    ink_fill(cr, col, lw)


def mirror(pts):
    return [(-x, y) for x, y in pts]


def stroke(cr, pts, w, col=INK, smooth=True, closed=False, cap=cairo.LINE_CAP_ROUND, alpha=1.0):
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=closed)
    cr.set_source_rgba(*col, alpha)
    cr.set_line_width(w)
    cr.set_line_cap(cap)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def inked_line(cr, pts, w, col, edge=3.0, smooth=True, closed=False):
    """A coloured line with a black edge on both sides (painted trim, the tail, sashes)."""
    stroke(cr, pts, w + 2 * edge, INK, smooth, closed)
    stroke(cr, pts, w, col, smooth, closed)


def dot(cr, x, y, r, col, lw=0.0):
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    ink_fill(cr, col, lw)


def oval(cr, x, y, rx, ry, col, lw=LW, rot=0.0):
    cr.new_path()
    ell(cr, x, y, rx, ry, rot)
    ink_fill(cr, col, lw)


def capsule(cr, w0, w1, L):
    """Path of a limb from (0, 0) to (0, L), half-widths w0 -> w1, round ends."""
    cr.new_path()
    cr.arc(0, 0, w0, math.pi, 2 * math.pi)
    cr.line_to(w1, L)
    cr.arc(0, L, w1, 0, math.pi)
    cr.close_path()


def along(pts, n, closed=False):
    """n points spread evenly along a polyline (by length)."""
    P = list(pts) + ([pts[0]] if closed else [])
    seg = [math.dist(a, b) for a, b in zip(P, P[1:])]
    tot = sum(seg) or 1.0
    out = []
    for k in range(n):
        d = tot * (k + 0.5) / n
        for (a, b), L in zip(zip(P, P[1:]), seg):
            if d <= L and L:
                f = d / L
                out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
                break
            d -= L
    return out


def flat(cr, pts, closed=True):
    """The Catmull-Rom curve through pts as a dense polyline (for dots along it)."""
    cr.save()
    cr.identity_matrix()
    cr.new_path()
    spath(cr, pts, closed=closed)
    out = []
    for kind, p in cr.copy_path_flat():
        if kind in (cairo.PATH_MOVE_TO, cairo.PATH_LINE_TO):
            out.append(p)
    cr.new_path()
    cr.restore()
    return out


def dot_row(cr, pts, n, r, col=WHITE, closed=False, lw=0.0):
    for x, y in along(pts, n, closed):
        dot(cr, x, y, r, col, lw)


def mirror_bits(cr, pts, n, r=4.0):
    """Little mirror pieces (bright with a dark rim), the glitter of Yakshagana ornaments."""
    for x, y in along(pts, n):
        dot(cr, x, y, r + 1.4, INK)
        dot(cr, x, y, r, MIRROR)


def glow(cr, x, y, r, a, col=ORB):
    """Additive soft light."""
    if a <= 0.005 or r <= 1:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(0.35, *col, a * 0.45)
    g.add_color_stop_rgba(1, *col, 0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def sparkle(cr, x, y, r, a, col=(1.0, 0.95, 0.75)):
    """A four-pointed star of light."""
    if a <= 0.01 or r <= 0.5:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source_rgba(*col, a)
    cr.new_path()
    k = 0.16 * r
    cr.move_to(x, y - r)
    cr.curve_to(x + k, y - k, x + k, y - k, x + r, y)
    cr.curve_to(x + k, y + k, x + k, y + k, x, y + r)
    cr.curve_to(x - k, y + k, x - k, y + k, x - r, y)
    cr.curve_to(x - k, y - k, x - k, y - k, x, y - r)
    cr.fill()
    cr.restore()


def noise1(t, seed=0.0):
    """Smooth pseudo-random wobble in about -1..1 (pure function of t)."""
    return (0.5 * math.sin(2.1 * t + seed) + 0.3 * math.sin(3.7 * t + 1.3 * seed + 0.7)
            + 0.2 * math.sin(7.3 * t + 2.1 * seed + 1.9))


# ------------------------------------------------------------------ fabric patterns


@functools.lru_cache(maxsize=32)
def check_pattern(base, band, line, accent, cell=44.0, bw=11.0, k=2):
    """A madras-style check (the kase cloth): base colour, crossing bands, thin dark lines, a square where they meet.
    Mapped in design units (k pattern pixels per unit)."""
    n = int(cell * k)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, n, n)
    c = cairo.Context(s)
    c.scale(k, k)
    c.set_source_rgb(*base)
    c.paint()
    m = cell / 2
    c.set_source_rgb(*band)
    c.rectangle(m - bw / 2, 0, bw, cell)
    c.fill()
    c.rectangle(0, m - bw / 2, cell, bw)
    c.fill()
    c.set_source_rgb(*accent)
    c.rectangle(m - bw / 2, m - bw / 2, bw, bw)
    c.fill()
    c.set_source_rgb(*line)
    c.set_line_width(1.8)
    for v in (m - bw / 2 - 3, m + bw / 2 + 3):
        c.move_to(v, 0)
        c.line_to(v, cell)
        c.move_to(0, v)
        c.line_to(cell, v)
    c.stroke()
    c.set_line_width(1.2)
    c.move_to(0.6, 0)
    c.line_to(0.6, cell)
    c.move_to(0, 0.6)
    c.line_to(cell, 0.6)
    c.stroke()
    pat = cairo.SurfacePattern(s)
    pat.set_extend(cairo.EXTEND_REPEAT)
    pat.set_filter(cairo.FILTER_GOOD)
    pat.set_matrix(cairo.Matrix(xx=k, yy=k))
    return pat


@functools.lru_cache(maxsize=16)
def stripe_pattern(a, b, w=10.0, k=2):
    """Diagonal stripes (the cloth wrapped round the stage posts, sashes)."""
    n = int(2 * w * k)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, n, n)
    c = cairo.Context(s)
    c.scale(k, k)
    c.set_source_rgb(*a)
    c.paint()
    c.set_source_rgb(*b)
    for o in (-2 * w, 0, 2 * w):
        c.move_to(o, 0)
        c.line_to(o + w, 0)
        c.line_to(o + w + 2 * w, 2 * w)
        c.line_to(o + 2 * w, 2 * w)
        c.close_path()
    c.fill()
    pat = cairo.SurfacePattern(s)
    pat.set_extend(cairo.EXTEND_REPEAT)
    pat.set_filter(cairo.FILTER_GOOD)
    pat.set_matrix(cairo.Matrix(xx=k, yy=k))
    return pat


def fill_pattern(cr, pat, lw=LW):
    cr.set_source(pat)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(lw)
    cr.stroke()


# ------------------------------------------------------------------ looks (who wears what)

FACES = {
    # base paint, forehead mark, extras
    "hero": dict(base=(0.99, 0.72, 0.30), mark="namam", stache=True, rouge=True, jaw=True),
    "king": dict(base=(0.99, 0.66, 0.36), mark="namam", stache=True, rouge=True, jaw=True),
    "god": dict(base=(0.30, 0.48, 0.86), mark="namam", rouge=False, jaw=True, lips=LIPS),
    "hanuman": dict(base=(0.91, 0.30, 0.11), mark="namam", muzzle=WHITE, ruff=(1.0, 0.85, 0.48), patch=WHITE),
    "child": dict(base=(0.93, 0.36, 0.14), mark="namam", muzzle=WHITE, ruff=(1.0, 0.86, 0.50), patch=WHITE,
                  big_eyes=True),
    "jambavan": dict(base=(0.24, 0.16, 0.13), mark="namam", muzzle=(0.80, 0.58, 0.36), ruff=(0.97, 0.95, 0.90),
                     patch=(0.99, 0.88, 0.62), brow=WHITE, old=True, ruff_beard=True),
    "sage": dict(base=SAGE_SKIN, mark="vibhuti", beard=(0.97, 0.96, 0.93), brow=(0.97, 0.96, 0.93), old=True,
                 rouge=False),
    "woman": dict(base=(0.99, 0.78, 0.64), mark="bindi", rouge=True, nosering=True, lips=LIPS, lashes=True),
    "demon": dict(base=(0.13, 0.12, 0.17), mark="demon", rouge=True, jaw=True, tusks=True, stache=True,
                  red_eyes=True),
}

HANUMAN = dict(kind="actor", face="hanuman", crown="kireeta", disc=True, head_s=1.1, jacket=GREEN, sleeve=GREEN,
               hand=(0.90, 0.44, 0.22), kase=(YEL, RED, INK, GREEN), hem=GREEN, hem_zig=YEL, sash=WHITE,
               pads=RED, tail=(0.90, 0.32, 0.12), disc_cols=(GOLD, RED, GREEN))
CHILD_HANUMAN = dict(HANUMAN, face="child", crown="kireeta_small", disc=False, head_s=1.32, jacket=RED, sleeve=RED,
                     kase=(YEL, GREEN, INK, RED), hem=RED, edehara="small", bhuja=False)
JAMBAVAN = dict(kind="actor", face="jambavan", crown="kireeta", disc=True, head_s=1.1, ears="bear", disc_r=160.0,
                jacket=(0.12, 0.09, 0.09),
                sleeve=(0.12, 0.09, 0.09), fur=(0.30, 0.22, 0.19), hand=(0.30, 0.21, 0.17),
                kase=(GREEN, YEL, INK, RED), hem=RED, hem_zig=YEL, sash=YEL, pads=RED,
                disc_cols=(GOLD, GREEN, RED))
HERO = dict(kind="actor", face="hero", crown="kedige", disc=False, head_s=1.1, jacket=RED, sleeve=RED, hand=SKIN,
            kase=(RED, YEL, INK, GREEN), hem=GREEN, hem_zig=YEL, sash=WHITE, pads=RED)
KING = dict(HERO, face="king", crown="kireeta", disc=True, jacket=GREEN, sleeve=GREEN, kase=(YEL, RED, INK, GREEN))
GOD = dict(HERO, face="god", crown="kireeta", disc=True, jacket=YEL, sleeve=YEL, kase=(YEL, RED, INK, BLUE),
           hand=(0.36, 0.54, 0.90), halo=True)
DEMON = dict(kind="actor", face="demon", crown="demon", disc=False, head_s=1.1, jacket=BLACK, sleeve=BLACK, hand=(0.30, 0.24, 0.30),
             kase=(RED, BLACK, YEL, GREEN), hem=BLACK, hem_zig=RED, sash=RED, pads=BLACK)
SAGE = dict(kind="sage", face="sage", crown="jata", head_s=1.1, skin=SAGE_SKIN, hand=SAGE_SKIN, cloth=SAFF,
            cloth2=WHITE)
SAGE2 = dict(SAGE, cloth=(0.99, 0.70, 0.18), cloth2=(0.95, 0.40, 0.10))
WOMAN = dict(kind="woman", face="woman", crown="woman", head_s=1.1, skin=(0.96, 0.70, 0.52), hand=(0.96, 0.70, 0.52),
             saree=GREEN, border=RED, blouse=RED)

POSE = dict(mood="calm", gaze=(0.0, 0.0), lid=0.0, turn=0.0, head=0.0, lean=0.0, shift=0.0,
            armL=(0.16, 0.30, 0.0), armR=(0.16, 0.30, 0.0), handL="open", handR="open", holdL=None, holdR=None,
            bend=0.15, liftL=0.0, liftR=0.0, spin=0.0, sash=0.0, tail=0.0, breathe=0.0)

# rig dimensions (design units)
HIP = (55.0, 60.0)           # hip joints (x = ±55) below the waist
THIGH, SHIN, FOOT_H = 190.0, 165.0, 25.0
SHOULDER = (120.0, -300.0)
UARM, FARM = 150.0, 135.0
NECK = -335.0                 # the base of the neck on the torso
FACE_C = -118.0               # the face centre above the neck base


# ------------------------------------------------------------------ the rig


class Ctx:
    """What a part's draw function gets: the look, the pose, the time, and a place to record named points."""

    def __init__(self, cr, look, pose, t):
        self.cr, self.look, self.p, self.t = cr, look, pose, t
        self.pts = {}

    def mark(self, name, x, y):
        self.pts[name] = self.cr.user_to_device(x, y)


def _solve(cr, spec):
    base = cr.get_matrix()
    mats = {}

    def get(name):
        if name in mats:
            return mats[name]
        parent, anchor, ang, sc = spec[name]
        m = base if parent is None else get(parent)
        cr.set_matrix(m)
        if parent is not None:
            cr.translate(*anchor)
        cr.rotate(ang)
        if sc != 1.0:
            cr.scale(sc, sc)
        mats[name] = cr.get_matrix()
        return mats[name]
    for n in spec:
        get(n)
    cr.set_matrix(base)
    return mats


def leg_solve(bend, lift):
    """(thigh angle, shin angle relative, foot angle relative, hip-to-sole height) for one leg; angles for the
    screen-left leg (the right leg mirrors them). bend 0..1 = the Yakshagana half-sit with knees out; lift 0..1
    raises this leg's knee out to the side."""
    a = 0.05 + 0.80 * bend
    th = a + 1.05 * lift
    sh = -1.25 * a - 0.75 * lift
    ft = -(th + sh)
    h = HIP[1] + THIGH * math.cos(th) + SHIN * math.cos(th + sh) + FOOT_H
    return th, sh, ft, h


def figure(cr, look, x, feet, s=1.0, t=0.0, pose=None, flip=False, alpha=1.0):
    """Draw a costumed actor standing on the stage line `feet` at x, scale s. Returns named points (device
    coordinates): handL, handR, face, chest, crown, waist, footL, footR (L / R = screen left / right before flip)."""
    p = dict(POSE)
    p.update(pose or {})
    kind = look.get("kind", "actor")
    thL, shL, ftL, hL = leg_solve(p["bend"], p["liftL"])
    thR, shR, ftR, hR = leg_solve(p["bend"], p["liftR"])
    hip_h = max(hL, hR) if kind == "actor" else max(hL, hR)
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x + p["shift"] * s, feet - hip_h * s)
    sx = math.cos(math.pi * 2 * p["spin"]) if p["spin"] else 1.0
    if abs(sx) < 0.06:
        sx = 0.06 if sx >= 0 else -0.06
    cr.scale(s * sx * (-1 if flip else 1), s)
    ctx = Ctx(cr, look, p, t)
    uL, lL, _ = p["armL"]
    uR, lR, _ = p["armR"]
    br = p["breathe"]
    spec = {
        "root": (None, (0, 0), 0.0, 1.0),
        "thighL": ("root", (-HIP[0], HIP[1]), thL, 1.0),
        "shinL": ("thighL", (0, THIGH), shL, 1.0),
        "footL": ("shinL", (0, SHIN), ftL, 1.0),
        "thighR": ("root", (HIP[0], HIP[1]), -thR, 1.0),
        "shinR": ("thighR", (0, THIGH), -shR, 1.0),
        "footR": ("shinR", (0, SHIN), -ftR, 1.0),
        "torso": ("root", (0, 0), p["lean"], 1.0),
        "uarmL": ("torso", (-SHOULDER[0], SHOULDER[1] - 3 * br), uL, 1.0),
        "farmL": ("uarmL", (0, UARM), -lL, 1.0),
        "uarmR": ("torso", (SHOULDER[0], SHOULDER[1] - 3 * br), -uR, 1.0),
        "farmR": ("uarmR", (0, UARM), lR, 1.0),
        "head": ("torso", (0, NECK - 2 * br), p["head"], look.get("head_s", 1.0)),
    }
    mats = _solve(cr, spec)
    draw = KINDS[kind]
    for part, fn in draw:
        cr.set_matrix(mats[part])
        cr.save()
        fn(ctx)
        cr.restore()
    cr.set_matrix(mats["root"])
    ctx.mark("waist", 0, 0)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    return ctx.pts


# ------------------------------------------------------------------ face paint (mukhavarna)

FACE_PTS = [(0, 96), (32, 89), (55, 64), (66, 26), (69, -14), (67, -50), (58, -80), (30, -91), (0, -93),
            (-30, -91), (-58, -80), (-67, -50), (-69, -14), (-66, 26), (-55, 64), (-32, 89)]

MOODS = {
    #           brow inner dy, outer dy, lift, eye height, mouth
    "calm": dict(bi=0, bo=0, lift=0, eh=15, mouth="smile", pupil=0.44),
    "wonder": dict(bi=-5, bo=-1, lift=-7, eh=19, mouth="o", pupil=0.36),
    "angry": dict(bi=10, bo=-7, lift=2, eh=17, mouth="open", pupil=0.34),
    "fierce": dict(bi=12, bo=-9, lift=2, eh=20, mouth="roar", pupil=0.32),
    "joy": dict(bi=-3, bo=0, lift=-4, eh=15, mouth="grin", pupil=0.44, closed=True),
    "sad": dict(bi=-9, bo=5, lift=-2, eh=12, mouth="frown", pupil=0.46),
    "smile": dict(bi=-2, bo=0, lift=-2, eh=15, mouth="grin", pupil=0.44),
}


def _eye(cr, ctx, cx, cy, side, f, m):
    """One eye of the painted face, outer corner toward `side` (-1 screen left, +1 screen right), with the long black
    Yakshagana eye line swept out to the temple, the brow, and a row of white dots above the brow."""
    p = ctx.p
    big = 1.12 if f.get("big_eyes") else 1.0
    eh = m["eh"] * big
    gx, gy = p["gaze"]
    lid = p["lid"]
    base = f["base"]
    cr.save()
    cr.translate(cx, cy)
    cr.scale(side * big, big)
    gx *= side
    if f.get("patch"):                                  # a white ground round the eye (monkey / bear faces)
        cr.new_path()
        cr.move_to(-25, 6)
        cr.curve_to(-14, -eh - 12, 16, -eh - 13, 33, -5)
        cr.curve_to(22, eh * 0.7 + 10, -10, eh * 0.7 + 10, -25, 6)
        cr.close_path()
        ink_fill(cr, f["patch"], 3.0)
        base = f["patch"]
    if f.get("red_eyes"):
        oval(cr, 4, 0, 34, eh + 10, (0.85, 0.10, 0.08), 0)
        base = (0.85, 0.10, 0.08)
    if m.get("closed"):                                 # a smiling, closed eye
        stroke(cr, [(-19, 3), (0, -eh * 0.55), (20, 1)], 6.0)
        stroke(cr, [(18, 0), (44, -13)], 5.0)
    else:
        cr.new_path()
        cr.move_to(-19, 2)
        cr.curve_to(-9, -eh, 9, -eh * 1.05, 20, -2)
        cr.curve_to(9, eh * 0.66, -9, eh * 0.6, -19, 2)
        cr.close_path()
        cr.set_source_rgb(*WHITE)
        cr.fill_preserve()
        cr.save()
        cr.clip()
        ix, iy = gx * 7.0, -1 + gy * 4.0
        r = eh * m["pupil"] + 1.0
        if f.get("red_eyes") or p["mood"] in ("angry", "fierce"):
            dot(cr, ix, iy, r + 3.0, (0.80, 0.10, 0.06))
        dot(cr, ix, iy, r, INK)
        dot(cr, ix + r * 0.35, iy - r * 0.4, r * 0.28, WHITE)
        if lid > 0.01:                                  # the upper lid comes down (looking down, sleepy, sad)
            cr.rectangle(-30, -eh - 10, 60, (eh + 10) * 0.25 + lid * eh * 1.1)
            cr.set_source_rgb(*base)
            cr.fill()
        cr.restore()
        ly = -eh * 0.95 + lid * eh * 1.0
        stroke(cr, [(-20, 2), (-8, ly), (9, ly - 0.5), (21, -2)], 6.5)
        stroke(cr, [(-18, 3), (-6, eh * 0.62), (10, eh * 0.6), (20, 0)], 3.2)
        cr.new_path()                                   # the wing out to the temple
        cr.move_to(17, -5)
        cr.curve_to(28, -8, 36, -10, 46, -15 - 0.2 * ly)
        cr.curve_to(38, -6, 30, 2, 14, 4)
        cr.close_path()
        cr.set_source_rgb(*INK)
        cr.fill()
    bi, bo, lift = m["bi"], m["bo"], m["lift"]
    bcol = f.get("brow", INK)
    top = [(-21, -22 + bi), (0, -33 + lift), (22, -32 + lift + bo * 0.5), (40, -24 + bo)]
    bot = [(40, -24 + bo), (22, -26 + lift + bo * 0.5), (2, -26 + lift), (-19, -14 + bi)]
    cr.new_path()
    spath(cr, top, closed=False)
    spath(cr, bot, closed=False, cont=True)
    cr.close_path()
    ink_fill(cr, bcol, 2.5 if bcol != INK else 0)
    if f.get("old"):                                    # bushy old brows: a few hairs
        for i in range(4):
            stroke(cr, [(-12 + 13 * i, -26 + lift + 0.3 * bi), (-6 + 13 * i, -36 + lift + 0.2 * bi)], 3.0, bcol)
    if not f.get("old"):
        dot_row(cr, [(-17, -33 + bi), (0, -44 + lift), (22, -43 + lift), (42, -34 + bo)], 5, 2.8, WHITE)
        dot_row(cr, [(-4, 15), (12, 14), (28, 9), (44, 1)], 4, 2.6, WHITE)
    cr.restore()


def _mouth(cr, f, m, y=46.0, w=1.0, col=LIPS):
    kind = m["mouth"]
    cr.save()
    cr.translate(0, y)
    cr.scale(w, 1.0)
    if kind == "smile":
        shape(cr, [(-21, -1), (-10, -6), (0, -4), (10, -6), (21, -1), (10, 7), (0, 9), (-10, 7)], col, 2.5)
        stroke(cr, [(-21, -1), (0, 2), (21, -1)], 2.5)
    elif kind == "grin":
        cr.new_path()
        cr.move_to(-24, -4)
        cr.curve_to(-8, 2, 8, 2, 24, -4)
        cr.curve_to(14, 16, -14, 16, -24, -4)
        cr.close_path()
        ink_fill(cr, (0.35, 0.03, 0.04), 2.5)
        cr.new_path()
        cr.move_to(-20, -2)
        cr.curve_to(-8, 3, 8, 3, 20, -2)
        cr.line_to(16, 4)
        cr.curve_to(6, 7, -6, 7, -16, 4)
        cr.close_path()
        ink_fill(cr, WHITE, 0)
        stroke(cr, [(-26, -6), (-22, -2)], 2.5)
        stroke(cr, [(26, -6), (22, -2)], 2.5)
    elif kind == "o":
        oval(cr, 0, 2, 9, 11, col, 2.5)
        oval(cr, 0, 3, 5, 7, (0.30, 0.02, 0.03), 0)
    elif kind in ("open", "roar"):
        k = 1.35 if kind == "roar" else 1.0
        cr.new_path()
        cr.move_to(-24 * k, -3)
        cr.curve_to(-8, -9, 8, -9, 24 * k, -3)
        cr.curve_to(16 * k, 18 * k, -16 * k, 18 * k, -24 * k, -3)
        cr.close_path()
        ink_fill(cr, (0.32, 0.02, 0.03), 3.0)
        cr.new_path()
        cr.move_to(-20 * k, -3)
        cr.curve_to(-8, -7, 8, -7, 20 * k, -3)
        cr.line_to(18 * k, 2)
        cr.curve_to(6, -1, -6, -1, -18 * k, 2)
        cr.close_path()
        ink_fill(cr, WHITE, 0)
        stroke(cr, [(-24 * k, -3), (-8, -10), (8, -10), (24 * k, -3)], 4.0, col)
    elif kind == "frown":
        shape(cr, [(-19, 5), (-9, -2), (0, -1), (9, -2), (19, 5), (9, 7), (0, 6), (-9, 7)], col, 2.5)
    cr.restore()


def _ruff(cr, col, beard=False, lw=5.0):
    """The fur round a vanara's (or the bear king's) face: a spiky ring from temple to temple under the chin."""
    pts = []
    n = 30
    a0, a1 = -0.42, math.pi + 0.42
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        down = max(0.0, math.sin(a))
        rx, ry = 92 + 6 * down, 100 + (40 if beard else 14) * down ** 2
        k = 1.0 if i % 2 == 0 else 0.86
        pts.append((rx * k * math.cos(a), 6 + ry * k * math.sin(a)))
    pts += [(-60, -70), (0, -80), (60, -70)]
    shape(cr, pts, col, lw, smooth=False)
    for i in range(1, n, 2):                            # a little shading line in each tuft
        a = a0 + (a1 - a0) * i / n
        down = max(0.0, math.sin(a))
        rx, ry = 92 + 6 * down, 100 + (40 if beard else 14) * down ** 2
        stroke(cr, [(rx * 0.80 * math.cos(a), 6 + ry * 0.80 * math.sin(a)),
                    (rx * 0.93 * math.cos(a), 6 + ry * 0.93 * math.sin(a))], 2.5, INK, alpha=0.6)


def _forehead_mark(cr, f, X):
    mk = f.get("mark")
    if mk == "namam":
        stroke(cr, [(X(-9), -72), (X(-9), -50), (X(0), -38), (X(9), -50), (X(9), -72)], 10.0)
        stroke(cr, [(X(-9), -72), (X(-9), -50), (X(0), -38), (X(9), -50), (X(9), -72)], 5.5, WHITE)
        stroke(cr, [(X(0), -72), (X(0), -47)], 4.5, RED)
    elif mk == "vibhuti":
        for y in (-70, -61, -52):
            stroke(cr, [(X(-40), y + 2), (X(0), y), (X(40), y + 2)], 7.0)
            stroke(cr, [(X(-40), y + 2), (X(0), y), (X(40), y + 2)], 4.0, WHITE)
        dot(cr, X(0), -60, 5.5, RED, 2.0)
    elif mk == "bindi":
        dot(cr, X(0), -50, 6.5, RED, 2.0)
        dot(cr, X(0), -62, 2.8, GOLD)
    elif mk == "demon":
        shape(cr, [(X(0), -36), (X(-16), -58), (X(-10), -80), (X(0), -66), (X(10), -80), (X(16), -58)], WHITE, 3.0)
        shape(cr, [(X(0), -44), (X(-7), -58), (X(0), -66), (X(7), -58)], RED, 0)


def head_paint(ctx):
    """The face (origin = face centre): fur ruff, face shape, paint, eyes, nose, mouth, moustache, beard."""
    cr, look, p = ctx.cr, ctx.look, ctx.p
    f = FACES[look["face"]]
    m = MOODS[p["mood"]]
    turn = p["turn"]

    def X(x):
        return x + turn * 15.0 * (1 - min(1.0, (x / 72.0) ** 2))
    if f.get("ruff"):
        cr.save()
        cr.translate(turn * 5, 0)
        _ruff(cr, f["ruff"], beard=f.get("ruff_beard", False))
        cr.restore()
    cr.save()
    cr.translate(turn * 4, 0)
    cr.scale(1 - 0.05 * abs(turn), 1)
    shape(cr, FACE_PTS, f["base"])
    cr.restore()
    cr.save()                                           # everything painted stays inside the face
    cr.save()
    cr.new_path()
    cr.translate(turn * 4, 0)
    cr.scale(1 - 0.05 * abs(turn), 1)
    spath(cr, FACE_PTS)
    cr.restore()
    cr.clip()
    if f.get("rouge"):
        for sd in (-1, 1):
            oval(cr, X(sd * 44), 30, 17, 11, (0.98, 0.36, 0.20) if look["face"] != "demon" else RED, 0)
    if f.get("jaw"):                                    # the white jaw line with red dots (chutti-like)
        jaw = [(X(-62), 18), (X(-52), 58), (X(-28), 82), (X(0), 88), (X(28), 82), (X(52), 58), (X(62), 18)]
        stroke(cr, jaw, 13.0)
        stroke(cr, jaw, 7.0, WHITE)
        dot_row(cr, jaw, 9, 2.4, RED)
    if look["face"] == "demon":
        for sd in (-1, 1):
            shape(cr, [(X(sd * 20), 10), (X(sd * 60), -8), (X(sd * 66), 36), (X(sd * 34), 56)], RED, 3.0)
            dot_row(cr, [(X(sd * 24), 14), (X(sd * 58), -2), (X(sd * 62), 34)], 5, 2.6, WHITE)
    cr.restore()
    _forehead_mark(cr, f, X)
    for sd in (-1, 1):
        _eye(cr, ctx, X(sd * 31), -12, sd, f, m)
    if f.get("muzzle"):
        mz = [(X(-28), 12), (X(-50), 30), (X(-54), 58), (X(-38), 86), (X(0), 99), (X(38), 86), (X(54), 58),
              (X(50), 30), (X(28), 12), (X(0), 20)]
        shape(cr, mz, f["muzzle"], 5.0)
        shape(cr, [(X(-15), 12), (X(15), 12), (X(11), 25), (X(0), 29), (X(-11), 25)], INK, 0)
        dot(cr, X(-5), 16, 2.2, (0.5, 0.5, 0.55))
        for sd in (-1, 1):
            for k in range(3):
                dot(cr, X(sd * (22 + 7 * k)), 44 - 3 * k, 2.2, INK)
        mm = dict(m)
        _mouth(cr, f, mm, 66, 1.05)
    else:
        stroke(cr, [(X(1), -12), (X(-3), 8), (X(-1), 16)], 3.2, (0.42, 0.14, 0.08))
        stroke(cr, [(X(-10), 20), (X(0), 25), (X(10), 20)], 3.2, (0.42, 0.14, 0.08))
        if f.get("beard"):
            _sage_beard(cr, f, m, X)
        else:
            _mouth(cr, f, m, 47, 1.0 - 0.1 * abs(turn), f.get("lips", LIPS))
            if f.get("stache"):
                for sd in (-1, 1):
                    pts = [(sd * 2, 33), (sd * 22, 30), (sd * 40, 29), (sd * 53, 19), (sd * 55, 6), (sd * 49, 9),
                           (sd * 45, 21), (sd * 27, 38), (sd * 4, 40)]
                    shape(cr, [(X(x), y) for x, y in pts], INK, 0)
    if f.get("nosering"):
        cr.new_path()
        cr.arc(X(-9), 24, 7.5, -0.3, 4.6)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(2.5)
        cr.stroke()
        dot(cr, X(-15), 29, 3.0, WHITE, 1.2)
    if f.get("tusks"):
        for sd in (-1, 1):
            shape(cr, [(X(sd * 18), 50), (X(sd * 30), 46), (X(sd * 34), 18), (X(sd * 28), 28)], WHITE, 3.0)
    ctx.mark("face", 0, 0)


def _sage_beard(cr, f, m, X):
    col = f["beard"]
    angry = m["mouth"] in ("open", "roar")
    pts = [(-58, 14), (-66, 56), (-60, 110), (-44, 168), (-22, 212), (0, 236), (22, 212), (44, 168), (60, 110),
           (66, 56), (58, 14), (40, 30), (22, 46), (0, 50), (-22, 46), (-40, 30)]
    shape(cr, [(X(x), y) for x, y in pts], col, 5.0)
    for k in range(-3, 4):                               # strands
        x0 = k * 15
        stroke(cr, [(X(x0 * 0.9), 70), (X(x0 * 1.1), 130), (X(x0 * 0.6), 200)], 2.4, (0.70, 0.68, 0.66))
    if angry:
        oval(cr, X(0), 50, 16, 11, (0.32, 0.02, 0.03), 3.0)
        stroke(cr, [(X(-12), 45), (X(12), 45)], 4.0, WHITE)
    else:
        stroke(cr, [(X(-12), 49), (X(0), 51), (X(12), 49)], 3.0, (0.55, 0.12, 0.10))
    for sd in (-1, 1):                                   # the moustache, drooping
        pts = [(sd * 2, 33), (sd * 20, 30), (sd * 38, 36), (sd * 50, 58), (sd * 44, 60), (sd * 30, 45),
               (sd * 4, 42)]
        shape(cr, [(X(x), y) for x, y in pts], col, 3.0)


# ------------------------------------------------------------------ crowns and headgear


def _band(cr, look):
    """The gold forehead band with a row of red stones and mirror dots, and a jewel at the centre."""
    shape(cr, [(-78, -58), (-82, -84), (-78, -104), (-40, -110), (0, -112), (40, -110), (78, -104), (82, -84),
               (78, -58), (40, -66), (0, -68), (-40, -66)], GOLD, 6.0)
    stroke(cr, [(-78, -80), (-40, -86), (0, -88), (40, -86), (78, -80)], 13.0, RED)
    stroke(cr, [(-78, -73), (0, -80), (78, -73)], 2.5)
    stroke(cr, [(-78, -87), (0, -96), (78, -87)], 2.5)
    dot_row(cr, [(-74, -80), (-40, -86), (0, -88), (40, -86), (74, -80)], 11, 3.0, MIRROR, lw=1.5)
    oval(cr, 0, -86, 11, 14, RED, 3.0)
    dot(cr, 3, -91, 3.0, WHITE)


def _ear_flaps(cr, look, t, s=1.0):
    """Kivi: the gold ear ornaments hanging from the crown over the ears, each with a pendant."""
    for sd in (-1, 1):
        pts = [(sd * 66, -84), (sd * 94, -66), (sd * 106, -18), (sd * 98, 26), (sd * 82, 44), (sd * 66, 22),
               (sd * 62, -36)]
        cr.save()
        cr.translate(0, -20)
        cr.scale(1, s)
        cr.translate(0, 20)
        shape(cr, pts, GOLD, 5.5)
        shape(cr, [(sd * 72, -54), (sd * 92, -40), (sd * 96, -6), (sd * 86, 20), (sd * 74, 4)], RED, 3.0)
        dot(cr, sd * 84, -14, 9, GREEN, 3.0)
        dot(cr, sd * 86, -17, 2.8, WHITE)
        mirror_bits(cr, [(sd * 70, -80), (sd * 96, -62), (sd * 106, -18), (sd * 98, 24)], 6, 3.0)
        sw = 4 * math.sin(t * 2.3 + sd)
        for k in range(3):
            dot(cr, sd * 82 + sw * k * 0.4, 52 + 12 * k, 5.0, GOLD_HI, 2.5)
        shape(cr, [(sd * 82 + sw, 86), (sd * 92 + sw, 100), (sd * 82 + sw * 1.2, 118), (sd * 72 + sw, 100)], RED, 3.0)
        cr.restore()


def _tier(cr, y0, y1, w0, w1, col=GOLD, band=None, stones=RED, n=5):
    shape(cr, [(-w0, y0), (-w1, y1), (w1, y1), (w0, y0)], col, 6.0, smooth=False)
    if band:
        stroke(cr, [(-w0 + 6, y0 - 9), (w0 - 6, y0 - 9)], 9.0, band, cap=cairo.LINE_CAP_BUTT)
    for i in range(n):
        u = (i + 0.5) / n
        yy = (y0 + y1) / 2 - 2
        ww = (w0 + w1) / 2
        xx = -ww * 0.82 + 2 * ww * 0.82 * u
        shape(cr, [(xx, yy - 10), (xx + 7, yy), (xx, yy + 10), (xx - 7, yy)], stones if i % 2 == 0 else GREEN, 2.5,
              smooth=False)
    mirror_bits(cr, [(-w1 + 6, y1 + 6), (w1 - 6, y1 + 6)], max(2, int(w1 / 12)), 2.6)


def _petals(cr, y, w, n, col=RED, h=22.0):
    for i in range(n):
        x = -w + 2 * w * (i + 0.5) / n
        pw = w / n
        shape(cr, [(x - pw * 0.9, y), (x - pw * 0.5, y - h * 0.6), (x, y - h), (x + pw * 0.5, y - h * 0.6),
                   (x + pw * 0.9, y)], col, 3.0)


def _kireeta(cr, look, t, small=False):
    """The tall tiered gold crown of kings, heroes and gods (and Hanuman), with flame wings at its sides."""
    if small:
        _tier(cr, -104, -150, 70, 54, n=4)
        _petals(cr, -150, 52, 5, RED, 18)
        shape(cr, [(-24, -150), (-30, -178), (-16, -196), (0, -232), (16, -196), (30, -178), (24, -150)], GOLD, 5.0)
        oval(cr, 0, -180, 8, 10, RED, 2.5)
        return
    for sd in (-1, 1):                                  # flame plumes at the sides
        pts = [(64, -104), (94, -110), (122, -132), (112, -142), (136, -166), (120, -174), (132, -210),
               (104, -188), (86, -166), (66, -150)]
        shape(cr, [(sd * x, y) for x, y in pts], GOLD, 5.5, smooth=False)
        shape(cr, [(sd * x, y) for x, y in [(74, -118), (100, -126), (112, -158), (96, -150), (78, -140)]], RED,
              2.5)
        dot(cr, sd * 84, -128, 4.0, MIRROR, 1.5)
    _tier(cr, -104, -166, 76, 62, band=None, n=5)
    _petals(cr, -166, 62, 7, RED, 24)
    _tier(cr, -170, -226, 56, 44, n=4, stones=GREEN)
    _petals(cr, -226, 44, 5, GREEN, 20)
    _tier(cr, -230, -278, 40, 30, n=3)
    # the kalasha spire
    shape(cr, [(-28, -278), (-34, -300), (-22, -320), (-10, -326), (0, -372), (10, -326), (22, -320), (34, -300),
               (28, -278)], GOLD, 5.5)
    stroke(cr, [(-30, -300), (30, -300)], 3.0)
    oval(cr, 0, -312, 9, 11, RED, 2.5)
    dot(cr, 0, -380, 6, GOLD_HI, 3.0)


def _disc(cr, look, t, r=178.0, cy=-150.0):
    """The big round back-piece (prabhavali) of a kireeta: scalloped gold rim, red ring, mirror ring, green ring,
    red spokes."""
    c1, c2, c3 = look.get("disc_cols", (GOLD, RED, GREEN))
    cr.save()
    cr.translate(0, cy)
    n = 26
    for i in range(n):
        a = 2 * math.pi * i / n + 0.5 * math.sin(t * 0.0)
        dot(cr, (r - 6) * math.cos(a), (r - 6) * math.sin(a), 22, c1, 5.0)
    for i in range(n):
        a = 2 * math.pi * i / n
        dot(cr, (r + 4) * math.cos(a), (r + 4) * math.sin(a), 3.2, WHITE)
    dot(cr, 0, 0, r - 12, c1, 6.0)
    dot(cr, 0, 0, r - 26, c2, 4.0)
    for i in range(36):
        a = 2 * math.pi * (i + 0.5) / 36
        rr = r - 40
        dot(cr, rr * math.cos(a), rr * math.sin(a), 5.0, MIRROR, 2.0)
    dot(cr, 0, 0, r - 54, c3, 4.0)
    dot(cr, 0, 0, r - 74, c1, 4.0)
    cr.set_source_rgb(*c2)
    cr.set_line_width(5)
    for i in range(16):
        a = 2 * math.pi * i / 16
        cr.move_to(30 * math.cos(a), 30 * math.sin(a))
        cr.line_to((r - 80) * math.cos(a), (r - 80) * math.sin(a))
    cr.stroke()
    cr.restore()


def _kedige(cr, look, t):
    """Kedige mundale: the great fan-shaped headdress of Yakshagana heroes, red cloth pleated under gold strips,
    edged with gold and mirrors."""
    outer = [(0, -96), (-96, -110), (-178, -170), (-214, -250), (-200, -330), (-140, -394), (-60, -424), (0, -432),
             (60, -424), (140, -394), (200, -330), (214, -250), (178, -170), (96, -110)]
    shape(cr, outer, GOLD, 7.0)
    inner = [(0, -112), (-86, -126), (-158, -180), (-188, -252), (-176, -320), (-124, -374), (-56, -400), (0, -406),
             (56, -400), (124, -374), (176, -320), (188, -252), (158, -180), (86, -126)]
    shape(cr, inner, RED, 4.0)
    cr.save()
    cr.new_path()
    spath(cr, inner)
    cr.clip()
    for i in range(15):                                 # pleats and gold strips radiating from the brow
        a = -math.pi * (0.06 + 0.88 * i / 14)
        x1, y1 = 440 * math.cos(a), -110 + 440 * math.sin(a)
        stroke(cr, [(0, -110), (x1, y1)], 9.0 if i % 2 else 4.0, GOLD if i % 2 else MAROON)
    cr.restore()
    mirror_bits(cr, outer[1:], 26, 4.0)
    for k, rr in enumerate((330, 250)):                 # two arcs of jewels
        pts = [(rr * 0.56 * math.cos(-math.pi * u), -110 + rr * math.sin(-math.pi * u) * 0.86)
               for u in np.linspace(0.12, 0.88, 7)]
        for i, (x, y) in enumerate(pts):
            dot(cr, x, y, 9 - 2 * k, GREEN if (i + k) % 2 else WHITE, 2.5)
    shape(cr, [(0, -404), (-16, -440), (0, -470), (16, -440)], GOLD, 4.0)
    dot(cr, 0, -442, 6, RED, 2.0)


def _demon_crown_back(cr, look, t):
    """The huge flaming round crown of a demon role."""
    cr.save()
    cr.translate(0, -170)
    n = 22
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n
        rr = 262 if i % 2 == 0 else 214
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    shape(cr, pts, RED, 6.0, smooth=False)
    pts2 = [(p[0] * 0.86, p[1] * 0.86) for p in pts]
    shape(cr, pts2, GOLD, 4.0, smooth=False)
    dot(cr, 0, 0, 170, BLACK, 5.0)
    dot_row(cr, [(170 * math.cos(a) * 0.9, 170 * math.sin(a) * 0.9) for a in np.linspace(0, 2 * math.pi, 40)], 34,
            4.0, WHITE)
    dot(cr, 0, 0, 130, RED, 4.0)
    dot(cr, 0, 0, 96, GOLD, 4.0)
    cr.restore()


def _demon_crown(cr, look, t):
    for sd in (-1, 1):                                  # horns
        shape(cr, [(sd * 50, -100), (sd * 96, -150), (sd * 120, -232), (sd * 104, -246), (sd * 86, -170),
                   (sd * 40, -132)], WHITE, 5.0)
    _tier(cr, -104, -176, 84, 70, n=5)
    _petals(cr, -176, 70, 7, RED, 30)
    shape(cr, [(-40, -180), (0, -260), (40, -180)], GOLD, 5.0)
    dot(cr, 0, -206, 10, RED, 3.0)


def _jata_back(cr, look, t):
    """A sage's long grey hair falling behind his shoulders."""
    shape(cr, [(-62, -84), (-92, -20), (-100, 70), (-96, 170), (-70, 210), (70, 210), (96, 170), (100, 70),
               (92, -20), (62, -84), (0, -100)], (0.86, 0.85, 0.83), 5.0)


def _jata(cr, look, t):
    """The hairline, and the tall bun of matted hair wound with rudraksha beads."""
    shape(cr, [(-70, -46), (-64, -84), (-30, -100), (0, -104), (30, -100), (64, -84), (70, -46), (52, -62),
               (24, -72), (0, -74), (-24, -72), (-52, -62)], (0.90, 0.89, 0.87), 4.5)
    for k in range(-3, 4):
        stroke(cr, [(k * 18, -74 + abs(k) * 2), (k * 21, -96 + abs(k) * 2)], 2.2, (0.60, 0.58, 0.56))
    hair = (0.62, 0.56, 0.50)
    line = (0.84, 0.80, 0.74)
    shape(cr, [(-36, -98), (-52, -124), (-58, -160), (-46, -192), (-20, -208), (0, -211), (20, -208), (46, -192),
               (58, -160), (52, -124), (36, -98)], hair, 5.0)       # the matted hair piled up in a bun
    for k in range(-3, 4):
        stroke(cr, [(k * 10, -104), (k * 15 + 3, -156), (k * 8, -202)], 2.6, line)
    for x, y in along([(-44, -110), (-20, -116), (0, -118), (20, -116), (44, -110)], 8):   # a rudraksha string
        dot(cr, x, y, 6.5, (0.55, 0.20, 0.10), 2.2)
    dot(cr, 0, -214, 7, (0.55, 0.20, 0.10), 2.2)


def _woman_back(cr, look, t):
    shape(cr, [(-66, -80), (-88, -10), (-86, 70), (-62, 110), (62, 110), (86, 70), (88, -10), (66, -80),
               (0, -100)], BLACK, 5.0)
    for sd in (-1, 1):                                  # jasmine strings round the hair
        pts = [(sd * 80, -70), (sd * 96, 0), (sd * 90, 70), (sd * 70, 104)]
        for x, y in along(pts, 10):
            dot(cr, x, y, 6.0, WHITE, 2.0)


def _woman_crown(cr, look, t):
    shape(cr, [(-70, -40), (-66, -84), (-30, -100), (0, -104), (30, -100), (66, -84), (70, -40), (54, -64),
               (24, -78), (0, -70), (-24, -78), (-54, -64)], BLACK, 4.5)
    stroke(cr, [(-64, -78), (-30, -94), (0, -97), (30, -94), (64, -78)], 9.0, GOLD)
    stroke(cr, [(-64, -78), (-30, -94), (0, -97), (30, -94), (64, -78)], 2.0)
    stroke(cr, [(0, -97), (0, -70)], 3.0, GOLD)
    oval(cr, 0, -64, 7, 9, RED, 2.5)
    shape(cr, [(-26, -96), (-30, -126), (-14, -136), (0, -160), (14, -136), (30, -126), (26, -96)], GOLD, 4.5)
    dot(cr, 0, -124, 8, RED, 2.5)
    dot(cr, 0, -127, 2.5, WHITE)
    for sd in (-1, 1):                                  # ears with jhumkas
        oval(cr, sd * 68, -6, 10, 20, look.get("skin", SKIN), 3.0)
        shape(cr, [(sd * 62, 22), (sd * 74, 22), (sd * 84, 46), (sd * 52, 46)], GOLD, 3.0)
        for k in range(3):
            dot(cr, sd * (58 + 10 * k), 50, 3.0, GOLD_HI, 1.5)


def crown_back(ctx):
    cr, look, t = ctx.cr, ctx.look, ctx.t
    cr.translate(0, FACE_C)
    if look.get("halo"):
        glow(cr, 0, -150, 300, 0.35, (1.0, 0.85, 0.45))
    c = look.get("crown")
    if look.get("disc"):
        _disc(cr, look, t, look.get("disc_r", 178.0))
    if look.get("ears") == "bear":                       # the bear king's round ears beside his crown
        for sd in (-1, 1):
            dot(cr, sd * 104, -112, 34, FACES["jambavan"]["base"], 5.0)
            dot(cr, sd * 106, -110, 18, FACES["jambavan"]["muzzle"], 3.0)
    if c == "kedige":
        _kedige(cr, look, t)
    elif c == "demon":
        _demon_crown_back(cr, look, t)
    elif c == "jata":
        _jata_back(cr, look, t)
    elif c == "woman":
        _woman_back(cr, look, t)


def crown_front(ctx):
    cr, look, t = ctx.cr, ctx.look, ctx.t
    cr.translate(0, FACE_C)
    c = look.get("crown")
    if c in ("kireeta", "kireeta_small", "kedige", "demon"):
        _ear_flaps(cr, look, t, 0.85 if c == "kireeta_small" else 1.0)
        if c == "kireeta":
            _kireeta(cr, look, t)
        elif c == "kireeta_small":
            _kireeta(cr, look, t, small=True)
        elif c == "demon":
            _demon_crown(cr, look, t)
        _band(cr, look)
        if c == "kedige":                               # the gold forehead crest of the kedige
            shape(cr, [(-30, -104), (-20, -136), (0, -150), (20, -136), (30, -104)], GOLD, 5.0)
            oval(cr, 0, -126, 8, 10, GREEN, 2.5)
    elif c == "jata":
        _jata(cr, look, t)
        for sd in (-1, 1):                              # ears with rudraksha earrings
            oval(cr, sd * 68, -6, 10, 20, look.get("skin", SKIN), 3.0)
            dot(cr, sd * 70, 22, 7, (0.55, 0.20, 0.10), 2.5)
    elif c == "woman":
        _woman_crown(cr, look, t)
    ctx.mark("crown", 0, -380)


def head(ctx):
    cr, look = ctx.cr, ctx.look
    skin = FACES[look["face"]]["base"] if look.get("kind") == "actor" else look.get("skin", SKIN)
    shape(cr, [(-30, 6), (-30, -40), (30, -40), (30, 6)], skin, 5.0, smooth=False)
    cr.translate(0, FACE_C)
    head_paint(ctx)


# ------------------------------------------------------------------ the costumed body (veshabhusha)


TORSO = [(-92, 4), (-98, -80), (-108, -190), (-124, -282), (-112, -320), (-70, -340), (-30, -346), (30, -346),
         (70, -340), (112, -320), (124, -282), (108, -190), (98, -80), (92, 4)]
EDEHARA = [(0, -102), (-46, -140), (-90, -205), (-108, -262), (-98, -306), (-60, -324), (0, -314), (60, -324),
           (98, -306), (108, -262), (90, -205), (46, -140)]
KASE = [(-96, -6), (-150, 30), (-204, 100), (-228, 170), (-216, 232), (-150, 258), (-60, 268), (0, 270), (60, 268),
        (150, 258), (216, 232), (228, 170), (204, 100), (150, 30), (96, -6), (0, -12)]
HEM = [(-226, 214), (-150, 252), (-60, 263), (0, 265), (60, 263), (150, 252), (226, 214)]


def _scale_pts(pts, k, c=(0, 0)):
    return [(c[0] + (x - c[0]) * k, c[1] + (y - c[1]) * k) for x, y in pts]


def torso(ctx):
    cr, look, p = ctx.cr, ctx.look, ctx.p
    jac = look.get("jacket", GREEN)
    shape(cr, TORSO, jac)
    if look.get("fur"):                                 # the bear king's shaggy fur
        for i in range(9):
            for sd in (-1, 1):
                y = -300 + 32 * i
                x = sd * (100 - 8 * math.sin(i))
                stroke(cr, [(x, y), (x + sd * 14, y + 14)], 4.0, look["fur"])
    # gold buttons down the front, under the chest plate
    for i in range(3):
        dot(cr, 0, -110 + 28 * i, 6.0, GOLD, 2.5)
    # the gold collar
    shape(cr, [(-66, -338), (-40, -306), (0, -294), (40, -306), (66, -338), (40, -330), (0, -318), (-40, -330)], GOLD,
          5.0)
    dot_row(cr, [(-54, -326), (0, -306), (54, -326)], 7, 3.2, RED)
    e = look.get("edehara", True)
    if e:
        k = 0.72 if e == "small" else 1.0
        cen = (0, -300)
        outer = _scale_pts(EDEHARA, k, cen)
        shape(cr, outer, GOLD, 6.0)
        shape(cr, _scale_pts(EDEHARA, 0.80 * k, (0, -320)), RED, 3.5)
        inner = _scale_pts(EDEHARA, 0.58 * k, (0, -330))
        shape(cr, inner, GREEN, 3.0)
        cr.save()
        cr.new_path()
        spath(cr, inner)
        cr.clip()
        for row in range(6):
            for col in range(-3, 4):
                x, y = col * 26 + (13 if row % 2 else 0), -300 + 24 * row
                shape(cr, [(x, y - 10), (x + 8, y), (x, y + 10), (x - 8, y)], MIRROR, 2.0, smooth=False)
        cr.restore()
        oval(cr, 0, -236 + (1 - k) * 20, 21 * k, 27 * k, RED, 4.0)
        dot(cr, 6 * k, -246 + (1 - k) * 20, 5 * k, WHITE)
        dot_row(cr, _scale_pts(EDEHARA, 0.93 * k, cen), 22, 3.4, WHITE, closed=True)
        tip = outer[0]
        sw = 5 * math.sin(ctx.t * 2.0)
        for j, dx in enumerate((-22, 0, 22)):            # hanging beads under the plate
            x0, y0 = tip[0] + dx, tip[1] - (14 if dx else 0)
            for q in range(3):
                dot(cr, x0 + sw * q * 0.3, y0 + 10 + 12 * q, 4.5, GOLD_HI, 2.0)
            shape(cr, [(x0 + sw, y0 + 46), (x0 + 7 + sw, y0 + 56), (x0 + sw, y0 + 68), (x0 - 7 + sw, y0 + 56)], RED, 2.5)
    # the waist belt (dabu) with its big buckle
    shape(cr, [(-104, -36), (-40, -42), (0, -43), (40, -42), (104, -36), (108, 10), (40, 4), (0, 3), (-40, 4),
               (-108, 10)], GOLD, 6.0)
    stroke(cr, [(-104, -16), (0, -20), (104, -16)], 10.0, RED, cap=cairo.LINE_CAP_BUTT)
    dot_row(cr, [(-100, -16), (0, -20), (100, -16)], 13, 2.8, WHITE)
    oval(cr, 0, -18, 34, 27, GOLD, 5.0)
    oval(cr, 0, -18, 20, 15, RED, 3.0)
    dot(cr, 5, -23, 4, WHITE)
    ctx.mark("chest", 0, -230)


def bhujakeerthi(ctx):
    """Bhujakeerthi: the gilded shoulder wings with red and green leaves and mirror bits."""
    cr, look = ctx.cr, ctx.look
    if look.get("bhuja", True) is False:
        return
    for sd in (-1, 1):
        cr.save()
        cr.translate(sd * (SHOULDER[0] + 6), SHOULDER[1] - 10)
        cr.scale(sd, 1)
        pts = [(-24, 14), (-30, -24), (-20, -70), (0, -110), (24, -134), (34, -118), (48, -86), (56, -46), (52, -8),
               (36, 20), (6, 28)]
        shape(cr, pts, GOLD, 6.0)
        shape(cr, [(-14, 6), (-18, -28), (-6, -66), (14, -100), (28, -84), (38, -46), (34, -4), (14, 12)], RED, 3.5)
        shape(cr, [(0, -4), (-2, -30), (8, -58), (20, -76), (26, -48), (22, -14)], GREEN, 3.0)
        mirror_bits(cr, [(-28, -10), (-22, -64), (2, -108), (26, -130), (48, -88), (54, -30)], 9, 3.2)
        dot(cr, 12, 6, 10, MIRROR, 3.0)
        cr.restore()


def _hand(cr, kind, side, col, t=0.0):
    """A hand at the wrist (0, 0) pointing down +y. side: -1 / +1 screen side of the figure (thumb toward the body's
    middle). kinds: open, point, fist, cup, grip, bless."""
    cr.save()
    cr.scale(-side, 1)                                  # drawn with the thumb on +x
    lw = 4.5
    if kind in ("open", "bless"):
        for i, (x, L) in enumerate(((-13, 74), (-4, 84), (5, 82), (13, 72))):
            cr.save()
            cr.translate(x, 36)
            cr.rotate(-0.06 * (i - 1.5))
            capsule(cr, 5.4, 4.8, L - 40)
            ink_fill(cr, col, 3.5)
            cr.restore()
        cr.new_path()
        spath(cr, [(-18, 0), (-20, 26), (-15, 46), (0, 50), (15, 44), (19, 24), (16, 0)])
        ink_fill(cr, col, lw)
        cr.save()
        cr.translate(16, 16)
        cr.rotate(-0.75)
        capsule(cr, 6, 5, 28)
        ink_fill(cr, col, 3.5)
        cr.restore()
    elif kind == "point":
        cr.save()
        cr.translate(-2, 40)
        capsule(cr, 5.5, 4.8, 52)
        ink_fill(cr, col, 3.5)
        cr.restore()
        cr.new_path()
        spath(cr, [(-18, 0), (-20, 28), (-14, 52), (2, 56), (16, 46), (19, 24), (16, 0)])
        ink_fill(cr, col, lw)
        for k in range(2):
            stroke(cr, [(6 + 5 * k, 44), (10 + 5 * k, 54)], 2.5)
        cr.save()
        cr.translate(16, 18)
        cr.rotate(-0.4)
        capsule(cr, 6, 5, 22)
        ink_fill(cr, col, 3.5)
        cr.restore()
    elif kind in ("fist", "grip"):
        cr.new_path()
        spath(cr, [(-19, 0), (-21, 26), (-16, 50), (0, 56), (16, 50), (20, 26), (17, 0)])
        ink_fill(cr, col, lw)
        for k in range(3):
            stroke(cr, [(-12 + 9 * k, 40), (-12 + 9 * k, 52)], 2.5)
        cr.save()
        cr.translate(17, 18)
        cr.rotate(0.5)
        capsule(cr, 6, 5, 18)
        ink_fill(cr, col, 3.5)
        cr.restore()
    elif kind == "cup":                                 # palm up, the fingertips curling up toward +x
        cr.new_path()
        spath(cr, [(-17, 0), (-21, 26), (-18, 54), (-6, 72), (12, 76), (28, 68), (32, 54), (20, 50), (16, 26),
                   (16, 0)])
        ink_fill(cr, col, lw)
        for k in range(3):
            stroke(cr, [(14 + 5 * k, 72 - 3 * k), (12 + 4 * k, 60 - 2 * k)], 2.5)
        cr.save()
        cr.translate(14, 14)
        cr.rotate(-1.1)
        capsule(cr, 6, 5, 22)
        ink_fill(cr, col, 3.5)
        cr.restore()
    cr.restore()


def _held(cr, what, side, t):
    """A prop held in the hand (drawn in the hand's frame before the fingers close over it)."""
    if what == "staff":                                 # Jambavan's long staff, kept upright on the screen
        cr.save()
        cr.translate(0, 34)
        m = cr.get_matrix()
        m.invert()
        dx, dy = m.transform_distance(0, 1)
        cr.rotate(math.atan2(-dx, dy))
        shape(cr, [(-9, -360), (9, -360), (9, 440), (-9, 440)], (0.55, 0.32, 0.14), 5.0, smooth=False)
        for y in (-300, -150, 100, 300):
            stroke(cr, [(-9, y), (9, y)], 7.0, GOLD, cap=cairo.LINE_CAP_BUTT)
        oval(cr, 0, -372, 18, 22, GOLD, 5.0)
        dot(cr, 0, -374, 7, RED, 2.0)
        cr.restore()
    elif what == "gada":
        cr.save()
        cr.translate(0, 34)
        shape(cr, [(-8, -40), (8, -40), (8, 260), (-8, 260)], GOLD_DK, 4.0, smooth=False)
        oval(cr, 0, 300, 52, 62, GOLD, 6.0)
        for k in range(-2, 3):
            stroke(cr, [(k * 18, 248), (k * 22, 300), (k * 18, 352)], 3.0)
        dot(cr, 0, 368, 9, GOLD, 3.0)
        cr.restore()
    elif what == "kamandalu":                           # a sage's water pot hanging from the hand
        cr.save()
        cr.translate(0, 50)
        stroke(cr, [(-26, 10), (0, -14), (26, 10)], 6.0, (0.45, 0.25, 0.10))
        shape(cr, [(-30, 14), (30, 14), (44, 50), (36, 86), (0, 98), (-36, 86), (-44, 50)], (0.62, 0.36, 0.14), 5.0)
        stroke(cr, [(-40, 46), (40, 46)], 4.0, GOLD)
        stroke(cr, [(38, 40), (66, 22), (74, 12)], 6.0, (0.62, 0.36, 0.14))
        cr.restore()


def _arm(side):
    def upper(ctx):
        cr, look = ctx.cr, ctx.look
        kind = look.get("kind")
        col = look.get("sleeve", look.get("skin", SKIN)) if kind == "actor" else look.get("skin", SKIN)
        if kind == "woman":
            col = look.get("skin")
        capsule(cr, 31 if kind == "actor" else 26, 25 if kind == "actor" else 21, UARM)
        ink_fill(cr, col, 6.0)
        if kind == "woman":                             # the blouse sleeve
            cr.save()
            cr.new_path()
            cr.rectangle(-40, -40, 80, 80)
            cr.clip()
            capsule(cr, 27, 24, UARM)
            ink_fill(cr, look.get("blouse", RED), 5.0)
            cr.restore()
            stroke(cr, [(-24, 38), (24, 38)], 6.0, GOLD)
        if kind == "actor":                             # the armlet
            shape(cr, [(-33, 36), (33, 36), (31, 58), (-31, 58)], GOLD, 4.5, smooth=False)
            shape(cr, [(-12, 36), (0, 14), (12, 36)], GOLD, 4.0, smooth=False)
            dot(cr, 0, 46, 6, RED, 2.0)
        elif kind == "sage":
            for x, y in along([(-24, 40), (24, 40)], 5):
                dot(cr, x, y, 5, (0.55, 0.20, 0.10), 2.0)

    def lower(ctx):
        cr, look, t = ctx.cr, ctx.look, ctx.t
        kind = look.get("kind")
        p = ctx.p
        hk = p["handL" if side < 0 else "handR"]
        hold = p["holdL" if side < 0 else "holdR"]
        col = look.get("sleeve", GREEN) if kind == "actor" else look.get("skin", SKIN)
        uw0, uw1 = (31, 25) if kind == "actor" else (26, 21)
        fw0, fw1 = (25, 20) if kind == "actor" else (21, 17)
        capsule(cr, fw0, fw1, FARM)
        ink_fill(cr, col, 6.0 if kind == "actor" else 5.5)
        # one smooth arm, not two pieces: refill both segments (inset by half the outline) round the elbow
        bend = p["armL"][1] if side < 0 else p["armR"][1]
        cr.save()
        cr.new_path()
        cr.arc(0, 0, uw1 + 16, 0, 2 * math.pi)
        cr.clip()
        cr.save()
        cr.rotate(bend if side < 0 else -bend)
        cr.translate(0, -UARM)
        capsule(cr, uw0 - 3.2, uw1 - 3.2, UARM)
        cr.set_source_rgb(*col)
        cr.fill()
        cr.restore()
        capsule(cr, fw0 - 3.2, fw1 - 3.2, FARM)
        cr.set_source_rgb(*col)
        cr.fill()
        cr.restore()
        cr.save()
        cr.translate(0, FARM)
        cr.rotate(-ctx.p["armL"][2] if side < 0 else ctx.p["armR"][2])
        if hold:
            _held(cr, hold, side, t)
        _hand(cr, "grip" if hold in ("staff", "gada") else hk, side, look.get("hand", SKIN), t)
        ctx.mark("handL" if side < 0 else "handR", 0, 40)
        cr.restore()
        if kind == "actor":                             # the big gold wrist cuff
            shape(cr, [(-23, 92), (23, 92), (28, 134), (-28, 134)], GOLD, 5.0, smooth=False)
            stroke(cr, [(-26, 113), (26, 113)], 7.0, RED, cap=cairo.LINE_CAP_BUTT)
            dot_row(cr, [(-24, 100), (24, 100)], 5, 2.6, WHITE)
        elif kind == "woman":
            for k in range(4):
                stroke(cr, [(-19, 104 + 7 * k), (19, 104 + 7 * k)], 4.0, (GOLD, RED, GREEN, GOLD)[k])
    return upper, lower


def _thigh(side):
    def fn(ctx):
        cr, look = ctx.cr, ctx.look
        capsule(cr, 42, 32, THIGH)
        ink_fill(cr, look.get("tights", WHITE), 5.0)
    return fn


def _shin(side):
    def fn(ctx):
        cr, look, t = ctx.cr, ctx.look, ctx.t
        kind = look.get("kind")
        skin = look.get("hand", SKIN) if kind == "actor" else look.get("skin", SKIN)
        capsule(cr, 26, 17, SHIN)
        ink_fill(cr, skin, 5.0)
        if kind == "actor":                             # the leg pad covered with bells (gejje)
            pad = [(-36, 10), (36, 10), (31, 140), (-31, 140)]
            shape(cr, pad, look.get("pads", RED), 5.0, smooth=False)
            for y, c in ((10, GOLD), (140, GOLD)):
                stroke(cr, [(-36 + (y - 10) * 0.04, y), (36 - (y - 10) * 0.04, y)], 9.0, c, cap=cairo.LINE_CAP_BUTT)
                stroke(cr, [(-36 + (y - 10) * 0.04, y - 5), (36 - (y - 10) * 0.04, y - 5)], 2.0)
                stroke(cr, [(-36 + (y - 10) * 0.04, y + 5), (36 - (y - 10) * 0.04, y + 5)], 2.0)
            for r_, y in enumerate((30, 54, 78, 102, 124)):
                w = 30 - (y - 10) * 0.04
                n = 4
                for i in range(n):
                    x = -w + 2 * w * (i + 0.5 + (0.25 if r_ % 2 else -0.25)) / n
                    if abs(x) > w - 4:
                        continue
                    dot(cr, x, y, 7.0, GOLD, 2.2)
                    stroke(cr, [(x - 3, y + 2), (x + 3, y + 2)], 1.8)
                    dot(cr, x - 2, y - 3, 1.8, GOLD_HI)
            stroke(cr, [(-17, 153), (17, 153)], 5.0, GOLD)
        elif kind == "sage":
            for x, y in along([(-17, 150), (17, 150)], 4):
                dot(cr, x, y, 4.5, (0.55, 0.20, 0.10), 1.8)
        else:
            for k in range(2):
                stroke(cr, [(-18, 146 + 6 * k), (18, 146 + 6 * k)], 3.5, GOLD)
    return fn


def _foot(side):
    def fn(ctx):
        cr, look = ctx.cr, ctx.look
        kind = look.get("kind")
        skin = look.get("hand", SKIN) if kind == "actor" else look.get("skin", SKIN)
        pts = [(-14, -2), (14, -2), (26, 12), (46, 20), (58, 28), (56, 38), (12, 40), (-16, 38), (-21, 22)]
        if side < 0:
            pts = mirror(pts)
        shape(cr, pts, skin, 5.0)
        for k in range(3):
            x = side * (40 + 6 * k)
            stroke(cr, [(x, 30), (x, 38)], 2.0)
        ctx.mark("footL" if side < 0 else "footR", side * 20, 40)
    return fn


def kase(ctx):
    """The puffed checked skirt with its hem band, pom-pom tassels and the hanging front sashes."""
    cr, look, p, t = ctx.cr, ctx.look, ctx.p, ctx.t
    spread = 1 + 0.16 * p["bend"]
    cr.save()
    cr.scale(spread, 1 - 0.05 * p["bend"])
    base, band, line, acc = look.get("kase", (YEL, RED, INK, GREEN))
    pat = check_pattern(base, band, line, acc)
    # pom-pom tassels round the hem (behind the skirt)
    for i, (x, y) in enumerate(along(HEM, 9)):
        sw = 4 * math.sin(t * 3 + i)
        stroke(cr, [(x, y), (x + sw, y + 22)], 2.5)
        dot(cr, x + sw, y + 26, 9, (RED, YEL, GREEN)[i % 3], 3.0)
    cr.new_path()
    spath(cr, KASE)
    fill_pattern(cr, pat, 7.0)
    cr.save()
    cr.new_path()
    spath(cr, KASE)
    cr.clip()
    g = cairo.LinearGradient(-230, 0, 230, 0)          # roundness: darker toward the sides
    for u, a in ((0, 0.42), (0.28, 0.0), (0.72, 0.0), (1, 0.42)):
        g.add_color_stop_rgba(u, 0.12, 0.02, 0.02, a)
    cr.set_source(g)
    cr.paint()
    g = cairo.LinearGradient(0, -10, 0, 270)
    g.add_color_stop_rgba(0, 0.1, 0.02, 0.02, 0.35)
    g.add_color_stop_rgba(0.25, 0.1, 0.02, 0.02, 0.0)
    cr.set_source(g)
    cr.paint()
    for k in (-3, -2, -1, 1, 2, 3):                     # gathers
        stroke(cr, [(k * 26, 0), (k * 62, 120), (k * 66, 262)], 3.2, INK, alpha=0.55)
    hem_up = [(x, y - 12) for x, y in HEM]
    stroke(cr, hem_up, 44.0, look.get("hem", GREEN), cap=cairo.LINE_CAP_BUTT)
    zz = []
    hp = along(flat(cr, hem_up, closed=False), 40)
    for i, (x, y) in enumerate(hp):
        zz.append((x, y + (-8 if i % 2 else 8)))
    stroke(cr, zz, 5.0, look.get("hem_zig", YEL), smooth=False)
    stroke(cr, [(x, y - 23) for x, y in HEM], 3.0)
    cr.restore()
    cr.new_path()
    spath(cr, KASE)
    cr.set_source_rgb(*INK)
    cr.set_line_width(7.0)
    cr.stroke()
    cr.restore()
    # the hanging front sashes
    sw = p["sash"] + 0.03 * math.sin(t * 1.7)
    for sd in (-1, 1):
        cr.save()
        cr.translate(sd * 66, 0)
        cr.rotate(sw * 0.8 + sd * 0.04)
        shape(cr, [(-11, 0), (11, 0), (12, 270), (-12, 270)], RED, 4.0, smooth=False)
        for y in range(30, 260, 40):
            stroke(cr, [(-11, y), (11, y)], 6.0, GOLD, cap=cairo.LINE_CAP_BUTT)
        shape(cr, [(-16, 270), (16, 270), (22, 300), (0, 318), (-22, 300)], GOLD, 4.0)
        cr.restore()
    cr.save()
    cr.rotate(sw)
    shape(cr, [(-28, -4), (28, -4), (34, 292), (0, 316), (-34, 292)], look.get("sash", WHITE), 5.0, smooth=False)
    stroke(cr, [(-21, 6), (-25, 288)], 5.0, RED)
    stroke(cr, [(21, 6), (25, 288)], 5.0, RED)
    stroke(cr, [(-30, 250), (30, 250)], 5.0, GREEN)
    shape(cr, [(-26, 14), (26, 14), (22, 62), (0, 78), (-22, 62)], GOLD, 4.0)
    dot(cr, 0, 40, 9, RED, 2.5)
    cr.restore()


def tail(ctx):
    """Hanuman's tail rising behind him in a big curve with a curled tip."""
    cr, look, p, t = ctx.cr, ctx.look, ctx.p, ctx.t
    if not look.get("tail"):
        return
    w = p["tail"] + 0.10 * math.sin(t * 1.3)
    base = [(60, 70), (170, 190), (280, 280), (370, 250), (400, 140), (370, 40), (380, -50), (420, -80),
            (452, -58), (446, -22)]
    pts = []
    for i, (x, y) in enumerate(base):
        k = (i / (len(base) - 1)) ** 1.5
        a = w * k
        cx, cy = 60, 70
        dx, dy = x - cx, y - cy
        pts.append((cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)))
    stroke(cr, pts, 48.0, INK)
    stroke(cr, pts, 34.0, look["tail"])
    stroke(cr, pts[:-1], 7.0, (1.0, 0.62, 0.30), alpha=0.85)
    for x, y in along(flat(cr, pts, closed=False), 12)[1:-1]:      # rings of fur
        dot(cr, x, y, 3.2, (1.0, 0.86, 0.50))
    tx, ty = pts[-1]
    tuft = [(tx + 40 * math.cos(a) * (1.0 if i % 2 == 0 else 0.62), ty + 40 * math.sin(a) * (1.0 if i % 2 == 0 else 0.62))
            for i, a in enumerate(np.linspace(0, 2 * math.pi, 18, endpoint=False))]
    shape(cr, tuft, (1.0, 0.86, 0.50), 4.5, smooth=False)
    dot(cr, tx, ty, 10, (1.0, 0.94, 0.75))


# --- the sage's body: bare chest, saffron cloth, rudraksha, sacred thread, a dhoti to the shins

SAGE_TORSO = [(-84, 4), (-90, -80), (-100, -190), (-116, -282), (-106, -318), (-66, -336), (-28, -342), (28, -342),
              (66, -336), (106, -318), (116, -282), (100, -190), (90, -80), (84, 4)]


def sage_torso(ctx):
    cr, look = ctx.cr, ctx.look
    shape(cr, SAGE_TORSO, look.get("skin", SAGE_SKIN))
    stroke(cr, [(-50, -250), (-20, -236), (0, -240)], 3.0, (0.55, 0.30, 0.15), alpha=0.6)
    stroke(cr, [(50, -250), (20, -236), (0, -240)], 3.0, (0.55, 0.30, 0.15), alpha=0.6)
    stroke(cr, [(-74, -320), (-20, -200), (40, -80), (80, -10)], 4.0, WHITE)          # sacred thread
    shape(cr, [(40, -342), (104, -322), (114, -270), (96, -150), (70, -60), (40, -10), (-30, 0), (-60, -40),
               (-20, -120), (20, -220), (24, -300)], look.get("cloth", SAFF), 6.0)    # the upper cloth
    stroke(cr, [(26, -300), (20, -220), (-20, -120), (-60, -40)], 6.0, look.get("cloth2", WHITE))
    for x, y in along([(-62, -330), (-40, -250), (0, -212), (40, -250), (62, -330)], 15):   # rudraksha mala
        dot(cr, x, y, 7.0, (0.55, 0.20, 0.10), 2.2)
    shape(cr, [(-96, -32), (96, -32), (100, 10), (-100, 10)], look.get("cloth2", WHITE), 5.0, smooth=False)
    ctx.mark("chest", 0, -230)


def dhoti(ctx):
    cr, look, p = ctx.cr, ctx.look, ctx.p
    spread = 1 + 0.10 * p["bend"]
    cr.save()
    cr.scale(spread, 1)
    pts = [(-94, -6), (-120, 80), (-138, 200), (-142, 330), (-60, 342), (0, 334), (60, 342), (142, 330), (138, 200),
           (120, 80), (94, -6)]
    shape(cr, pts, look.get("cloth", SAFF), 6.5)
    for k in (-2, -1, 1, 2):
        stroke(cr, [(k * 18, 10), (k * 34, 180), (k * 40, 334)], 3.0, INK, alpha=0.5)
    stroke(cr, [(-140, 316), (-60, 328), (0, 320), (60, 328), (140, 316)], 12.0, look.get("cloth2", WHITE))
    shape(cr, [(-22, 0), (22, 0), (26, 300), (0, 320), (-26, 300)], look.get("cloth2", WHITE), 4.0, smooth=False)
    cr.restore()


# --- the woman: blouse, saree with pleats and pallu, jewellery

def woman_torso(ctx):
    cr, look = ctx.cr, ctx.look
    shape(cr, [(-74, 4), (-80, -80), (-92, -190), (-104, -282), (-96, -314), (-60, -334), (-26, -340), (26, -340),
               (60, -334), (96, -314), (104, -282), (92, -190), (80, -80), (74, 4)], look.get("skin"))
    shape(cr, [(-92, -180), (-100, -282), (-60, -326), (0, -300), (60, -326), (100, -282), (92, -180), (0, -170)],
          look.get("blouse", RED), 5.0)
    shape(cr, [(60, -334), (100, -300), (80, -200), (30, -100), (-40, -20), (-76, -10), (-70, -60), (-10, -140),
               (40, -240)], look.get("saree", GREEN), 6.0)                                # the pallu
    stroke(cr, [(64, -330), (44, -240), (-6, -140), (-66, -60)], 10.0, look.get("border", RED))
    stroke(cr, [(64, -330), (44, -240), (-6, -140), (-66, -60)], 2.5, GOLD)
    for k, (w, y) in enumerate(((52, -300), (66, -270))):    # necklaces
        stroke(cr, [(-w, y - 30), (0, y), (w, y - 30)], 7.0, GOLD)
        dot_row(cr, [(-w, y - 30), (0, y), (w, y - 30)], 7, 2.6, RED)
    dot(cr, 0, -262, 9, RED, 2.5)
    ctx.mark("chest", 0, -230)


def saree(ctx):
    cr, look = ctx.cr, ctx.look
    pts = [(-84, -8), (-110, 100), (-128, 240), (-136, 410), (-60, 424), (0, 418), (60, 424), (136, 410), (128, 240),
           (110, 100), (84, -8)]
    shape(cr, pts, look.get("saree", GREEN), 6.5)
    for k in range(-3, 4):                                # the pleats at the front
        stroke(cr, [(k * 9, 20), (k * 16, 200), (k * 22, 416)], 3.0, INK, alpha=0.55)
    stroke(cr, [(-132, 396), (-60, 410), (0, 404), (60, 410), (132, 396)], 18.0, look.get("border", RED))
    stroke(cr, [(-132, 386), (-60, 400), (0, 394), (60, 400), (132, 386)], 3.0, GOLD)
    stroke(cr, [(-84, -6), (0, -12), (84, -6)], 12.0, GOLD)


def _actor_parts():
    uL, lL = _arm(-1)
    uR, lR = _arm(1)
    return [("root", tail), ("head", crown_back),
            ("thighL", _thigh(-1)), ("thighR", _thigh(1)), ("shinL", _shin(-1)), ("shinR", _shin(1)),
            ("footL", _foot(-1)), ("footR", _foot(1)),
            ("root", kase), ("torso", torso),
            ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR),
            ("torso", bhujakeerthi), ("head", head), ("head", crown_front)]


def _sage_parts():
    uL, lL = _arm(-1)
    uR, lR = _arm(1)
    return [("head", crown_back), ("shinL", _shin(-1)), ("shinR", _shin(1)), ("footL", _foot(-1)),
            ("footR", _foot(1)), ("root", dhoti), ("torso", sage_torso),
            ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR), ("head", head), ("head", crown_front)]


def _woman_parts():
    uL, lL = _arm(-1)
    uR, lR = _arm(1)
    return [("head", crown_back), ("shinL", _shin(-1)), ("shinR", _shin(1)), ("footL", _foot(-1)),
            ("footR", _foot(1)), ("root", saree), ("torso", woman_torso),
            ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR), ("head", head), ("head", crown_front)]


KINDS = {"actor": _actor_parts(), "sage": _sage_parts(), "woman": _woman_parts()}


# ------------------------------------------------------------------ dance motion


def sway(t, amp=1.0, freq=0.55, ph=0.0):
    """The slow side-to-side sway of a Yakshagana actor waiting on the beat: (shift, lean, head)."""
    s = math.sin(2 * math.pi * freq * t + ph)
    return 14 * amp * s, -0.035 * amp * s, 0.05 * amp * math.sin(2 * math.pi * freq * t + ph + 0.6)


def step(t, t0, dur=0.9, side="R"):
    """One stamped step: the knee rises out to the side and the foot stamps down at t0 + dur * 0.62.
    Returns (lift, bend boost, stamp 0..1 flash just after the stamp)."""
    u = (t - t0) / dur
    if u <= 0 or u >= 1.4:
        return 0.0, 0.0, 0.0
    lift = math.sin(math.pi * clamp(u / 0.62)) if u < 0.62 else 0.0
    bend = 0.35 * math.sin(math.pi * clamp(u))
    stamp = math.exp(-9 * (u - 0.62) * dur) if u >= 0.62 else 0.0
    return lift, bend, stamp


def spin_phase(t, t0, dur=0.7):
    """0..1 through a full spin from t0 (0 outside it)."""
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return 0.0
    return ease(u) if u < 0.5 else 0.5 + 0.5 * (1 - (1 - (u - 0.5) * 2) ** 2)


# ------------------------------------------------------------------ the stage

CURTAINS = {
    # field, border, border teeth, inner band, motif colour
    "crimson": ((0.50, 0.03, 0.07), YEL, RED, GREEN, (0.98, 0.70, 0.20)),
    "green": ((0.04, 0.33, 0.17), YEL, RED, RED, (0.98, 0.78, 0.28)),
    "indigo": ((0.11, 0.09, 0.34), GOLD, RED, (0.90, 0.25, 0.10), (0.98, 0.72, 0.25)),
}
CURT = (70, 600, 1010, 1650)          # the thera: x0, y0, x1, y1
FLOOR_Y = 1650


def _night(cr):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.020, 0.015, 0.035)
    g.add_color_stop_rgb(0.35, 0.045, 0.025, 0.040)
    g.add_color_stop_rgb(1, 0.10, 0.04, 0.03)
    cr.set_source(g)
    cr.paint()
    rng = np.random.default_rng(7)
    for _ in range(60):                                 # a few faint stars over the open-air stage
        x, y = rng.uniform(0, W), rng.uniform(0, 560)
        cr.set_source_rgba(1, 0.95, 0.85, rng.uniform(0.15, 0.5))
        cr.arc(x, y, rng.uniform(0.8, 2.0), 0, 2 * math.pi)
        cr.fill()


def _floor(cr):
    cr.save()
    cr.rectangle(0, FLOOR_Y, W, H - FLOOR_Y)
    cr.clip()
    cr.set_source_rgb(0.36, 0.20, 0.09)
    cr.paint()
    vx, vy = W / 2, 1100
    cr.set_source_rgba(0.14, 0.07, 0.03, 0.9)
    cr.set_line_width(4)
    for i in range(-8, 9):
        bx = W / 2 + i * 150
        cr.move_to(vx + (bx - vx) * (FLOOR_Y - vy) / (H + 200 - vy), FLOOR_Y)
        cr.line_to(bx, H + 200)
    cr.stroke()
    for y in (1700, 1770, 1860):
        cr.move_to(0, y)
        cr.line_to(W, y)
    cr.set_line_width(2.5)
    cr.stroke()
    g = cairo.LinearGradient(0, FLOOR_Y, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55)
    g.add_color_stop_rgba(0.4, 0, 0, 0, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def _border_teeth(cr, x0, y0, x1, y1, n, col, inward=1):
    """A row of triangles along the line (x0, y0)-(x1, y1)."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * inward, ux * inward
    step_ = L / n
    hgt = step_ * 0.8
    cr.new_path()
    for i in range(n):
        ax, ay = x0 + ux * step_ * i, y0 + uy * step_ * i
        bx, by = ax + ux * step_, ay + uy * step_
        mx, my = (ax + bx) / 2 + nx * hgt, (ay + by) / 2 + ny * hgt
        cr.move_to(ax, ay)
        cr.line_to(mx, my)
        cr.line_to(bx, by)
        cr.close_path()
    ink_fill(cr, col, 2.5)


def _curtain(cr, style="crimson", motif="sun"):
    field, border, teeth, inner, mcol = CURTAINS[style]
    x0, y0, x1, y1 = CURT
    # the cloth hangs from a pole in loops between rings: a gently scalloped top edge
    cr.new_path()
    cr.move_to(x0, y0)
    nr = 9
    for i in range(nr):
        a = x0 + (x1 - x0) * i / nr
        b = x0 + (x1 - x0) * (i + 1) / nr
        cr.curve_to(a + (b - a) * 0.3, y0 + 18, a + (b - a) * 0.7, y0 + 18, b, y0)
    cr.line_to(x1, y1)
    cr.line_to(x0, y1)
    cr.close_path()
    cr.set_source_rgb(*border)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(7)
    cr.stroke()
    bw = 64
    fx0, fy0, fx1, fy1 = x0 + bw, y0 + bw, x1 - bw, y1 - bw
    for (ax, ay, bx, by, n, inw) in ((x0 + 6, y0 + 16, x1 - 6, y0 + 16, 24, 1), (x1 - 8, y0 + 10, x1 - 8, y1 - 6, 28, 1),
                                     (x1 - 6, y1 - 8, x0 + 6, y1 - 8, 24, 1), (x0 + 8, y1 - 6, x0 + 8, y0 + 10, 28, 1)):
        _border_teeth(cr, ax, ay, bx, by, n, teeth, inw)
    cr.rectangle(fx0 - 14, fy0 - 14, fx1 - fx0 + 28, fy1 - fy0 + 28)
    ink_fill(cr, inner, 5)
    cr.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    ink_fill(cr, field, 5)
    for (ax, ay, bx, by, n) in ((fx0, fy0, fx1, fy0, 30), (fx1, fy0, fx1, fy1, 34), (fx1, fy1, fx0, fy1, 30),
                                (fx0, fy1, fx0, fy0, 34)):
        for x, y in along([(ax, ay), (bx, by)], n):
            dot(cr, x, y, 3.5, GOLD_HI)
    cr.save()
    cr.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    cr.clip()
    if motif == "sun":                                  # a big painted sun-lotus, in thin gold lines
        cx, cy = W / 2, 1120
        cr.set_source_rgba(*mcol, 0.55)
        cr.set_line_width(6)
        for r in (360, 330):
            cr.arc(cx, cy, r, 0, 2 * math.pi)
            cr.stroke()
        for i in range(16):
            a = 2 * math.pi * i / 16
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(a)
            cr.move_to(0, -170)
            cr.curve_to(-60, -220, -40, -290, 0, -320)
            cr.curve_to(40, -290, 60, -220, 0, -170)
            cr.restore()
        cr.stroke()
        cr.arc(cx, cy, 160, 0, 2 * math.pi)
        cr.stroke()
        for i in range(48):
            a = 2 * math.pi * i / 48
            cr.arc(cx + 345 * math.cos(a), cy + 345 * math.sin(a), 4, 0, 2 * math.pi)
            cr.fill()
    elif motif == "tree":                               # a painted tree of life
        cx, cy = W / 2, 1260
        cr.set_source_rgba(*mcol, 0.5)
        cr.set_line_width(8)
        cr.move_to(cx, fy1)
        cr.curve_to(cx - 10, cy, cx + 10, cy - 200, cx, cy - 420)
        cr.stroke()
        for i in range(9):
            a = -math.pi / 2 + (i - 4) * 0.33
            r = 260 + 40 * math.sin(i)
            px, py = cx + r * math.cos(a) * 1.2, cy - 180 + r * math.sin(a)
            cr.move_to(cx, cy - 120 - 30 * abs(i - 4))
            cr.curve_to(cx + (px - cx) * 0.4, py + 60, px, py + 20, px, py)
            cr.stroke()
            cr.save()
            cr.translate(px, py)
            cr.rotate(a + math.pi / 2)
            cr.move_to(0, 0)
            cr.curve_to(-34, -30, -20, -80, 0, -96)
            cr.curve_to(20, -80, 34, -30, 0, 0)
            cr.restore()
            cr.stroke()
    elif motif == "rays":                               # rays of light painted from the centre
        cx, cy = W / 2, 1000
        for i in range(24):
            a = 2 * math.pi * i / 24
            cr.move_to(cx, cy)
            cr.line_to(cx + 1400 * math.cos(a - 0.06), cy + 1400 * math.sin(a - 0.06))
            cr.line_to(cx + 1400 * math.cos(a + 0.06), cy + 1400 * math.sin(a + 0.06))
            cr.close_path()
        cr.set_source_rgba(*mcol, 0.30)
        cr.fill()
    for i in range(12):                                 # cloth folds
        x = fx0 + (fx1 - fx0) * (i + 0.5) / 12
        g = cairo.LinearGradient(x - 40, 0, x + 40, 0)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
        g.add_color_stop_rgba(0.5, 0, 0, 0, 0.16)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        cr.set_source(g)
        cr.rectangle(x - 40, fy0, 80, fy1 - fy0)
        cr.fill()
    cr.restore()
    # the pole and its rings
    cr.rectangle(30, y0 - 22, W - 60, 18)
    ink_fill(cr, (0.40, 0.22, 0.10), 5)
    for i in range(nr + 1):
        x = x0 + (x1 - x0) * i / nr
        cr.new_path()
        cr.arc(x, y0 - 6, 12, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.set_line_width(9)
        cr.stroke_preserve()
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(4)
        cr.stroke()
    for x in (30, W - 30):
        dot(cr, x, y0 - 13, 20, GOLD, 5)
    # a fringe of tassels along the bottom
    for i in range(30):
        x = x0 + (x1 - x0) * (i + 0.5) / 30
        shape(cr, [(x - 10, y1), (x + 10, y1), (x, y1 + 26)], (GOLD, RED)[i % 2], 2.5, smooth=False)


def _post(cr, x, top=0, bottom=FLOOR_Y + 20, side=-1):
    """A stage post wrapped in red and white cloth, banana leaves tied at its top."""
    w = 30
    cr.save()
    cr.rectangle(x - w, top - 10, 2 * w, bottom - top + 10)
    fill_pattern(cr, stripe_pattern(RED, WHITE, 16.0), 6)
    cr.restore()
    for (ly, ang, L) in ((150, 1.05, 230), (190, 0.55, 190), (560, 1.15, 210)):
        cr.save()
        cr.translate(x, ly)
        cr.scale(-side * 0.8, 0.8)
        cr.rotate(ang)
        shape(cr, [(0, 0), (60, -40), (160, -60), (L, -30), (L - 40, 0), (160, 30), (60, 28)], LEAF, 5.0)
        stroke(cr, [(0, 0), (160, -14), (L - 20, -22)], 4.0, DLEAF)
        for k in range(5):
            u = 40 + k * (L - 80) / 5
            stroke(cr, [(u, -6 - k), (u + 26, -44 + k * 3)], 2.0, DLEAF)
        cr.restore()


def thorana(cr, t=0.0, y=18, sag=42, n=30):
    """The festive string of mango leaves and marigolds across the top of the stage."""
    def rope_y(x):
        u = x / W
        return y + sag * 4 * u * (1 - u)
    pts = [(x, rope_y(x)) for x in np.linspace(-20, W + 20, 30)]
    stroke(cr, pts, 6.0, (0.40, 0.25, 0.12), smooth=False)
    for i in range(n):
        x = W * (i + 0.5) / n
        yy = rope_y(x)
        sw = 0.08 * math.sin(t * 1.4 + i * 0.7)
        cr.save()
        cr.translate(x, yy)
        cr.rotate(sw)
        if i % 4 == 2:
            for k in range(3):                          # a short string of marigolds
                dot(cr, 0, 18 + 24 * k, 13, (0.99, 0.55, 0.05) if k % 2 == 0 else YEL, 3.0)
                for q in range(6):
                    a = q * math.pi / 3
                    stroke(cr, [(0, 18 + 24 * k), (8 * math.cos(a), 18 + 24 * k + 8 * math.sin(a))], 1.5,
                           (0.75, 0.30, 0.0))
        else:
            col = LEAF if i % 2 else DLEAF
            shape(cr, [(0, 0), (-14, 22), (-12, 58), (0, 84), (12, 58), (14, 22)], col, 3.5)
            stroke(cr, [(0, 4), (0, 78)], 2.0, (0.75, 0.85, 0.35) if i % 2 else (0.25, 0.55, 0.20))
        cr.restore()


@functools.lru_cache(maxsize=8)
def stage_surface(style="crimson", motif="sun", posts=True):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    _night(cr)
    _floor(cr)
    _curtain(cr, style, motif)
    if posts:
        _post(cr, 22, 0, FLOOR_Y + 40, -1)
        _post(cr, W - 22, 0, FLOOR_Y + 40, 1)
    s.flush()
    return s


def stage(cr, t, style="crimson", motif="sun", posts=True, garland=True):
    """The whole set behind the actors (cached), with the thorana swaying a little."""
    cr.set_source_surface(stage_surface(style, motif, posts), 0, 0)
    cr.paint()
    if garland:
        thorana(cr, t)


def musicians(cr, t, x, floor=FLOOR_Y + 30, s=1.0, flip=False, alpha=0.95):
    """The himmela, small and dark at the edge of the stage: the bhagavata (singer) with his cymbals and the chende
    drummer with his tall drum and two curved sticks."""
    dk = (0.30, 0.17, 0.10)                             # skin in the half-dark at the back of the stage
    cloth = (0.66, 0.60, 0.50)
    rim = (0.70, 0.48, 0.16)
    cr.save()
    cr.translate(x, floor)
    cr.scale(-s if flip else s, s)
    cr.push_group()
    # the bhagavata, seated, in white with a red shawl and a red turban, beating his cymbals
    shape(cr, [(-90, 0), (-70, -60), (-40, -140), (0, -160), (40, -140), (64, -60), (90, 0)], cloth, 4.0)
    shape(cr, [(-40, -140), (0, -160), (24, -150), (40, -60), (10, -40), (-20, -110)], (0.62, 0.12, 0.10), 3.0)
    dot(cr, 0, -190, 30, dk, 4.0)
    shape(cr, [(-34, -200), (-30, -230), (0, -242), (30, -230), (34, -200), (0, -210)], (0.70, 0.12, 0.10), 3.0)
    stroke(cr, [(-30, -206), (0, -214), (30, -206)], 4, GOLD)
    beat = abs(math.sin(t * math.pi * 2.2))
    for sd in (-1, 1):
        cx, cy = 50 * sd * (0.5 + 0.3 * beat), -110 - 10 * beat
        stroke(cr, [(sd * 30, -130), (cx, cy)], 18, INK)
        stroke(cr, [(sd * 30, -130), (cx, cy)], 11, dk)
        oval(cr, cx, cy, 16, 6, GOLD, 2.5, rot=sd * 0.4)
    # the chende drummer, standing, the tall drum hung at his side
    cr.translate(170, 0)
    shape(cr, [(-42, 0), (-46, -120), (46, -120), (42, 0)], cloth, 4.0, smooth=False)
    shape(cr, [(-46, -120), (-50, -260), (-30, -300), (30, -300), (50, -260), (46, -120)], dk, 4.0)
    dot(cr, 0, -330, 28, dk, 4.0)
    stroke(cr, [(-26, -350), (26, -350)], 8, (0.85, 0.80, 0.70))
    cr.save()
    cr.translate(30, -170)
    cr.rotate(-0.25)
    shape(cr, [(-38, -60), (38, -60), (38, 120), (-38, 120)], (0.20, 0.10, 0.06), 4.0, smooth=False)
    oval(cr, 0, -60, 38, 10, (0.85, 0.75, 0.55), 3.0)
    for y in (-40, 100):
        stroke(cr, [(-38, y), (38, y)], 6, rim, cap=cairo.LINE_CAP_BUTT)
    cr.restore()
    for k, sd in enumerate((-1, 1)):
        up = abs(math.sin(t * math.pi * 4.4 + k * 1.6))
        hx, hy = 10 + sd * 40, -230 - 40 * up
        stroke(cr, [(sd * 34, -280), (hx, hy)], 14, dk)
        stroke(cr, [(hx, hy), (hx + 30 + sd * 10, hy + 30 + 50 * (1 - up)), (30, -235)], 4, (0.50, 0.32, 0.14))
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def lamp(cr, t, x, y, s=1.0, k=0):
    """A brass oil lamp with a flickering flame."""
    f = flicker(t + k * 0.37)
    hgt = (54 + 7 * f) * s
    sway_ = (3 + 2 * f) * math.sin(t * 5.3 + k) * s
    glow(cr, x, y - 30 * s, 210 * s, 0.30 + 0.05 * f, (1.0, 0.55, 0.18))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    oval(cr, 0, 46, 40, 11, (0.78, 0.52, 0.16), 4.0)
    shape(cr, [(-9, 8), (9, 8), (12, 44), (-12, 44)], (0.80, 0.55, 0.18), 4.0, smooth=False)
    shape(cr, [(-38, -6), (38, -6), (26, 12), (0, 16), (-26, 12)], (0.86, 0.60, 0.20), 4.0)
    oval(cr, 0, -6, 38, 8, (0.30, 0.16, 0.05), 3.5)
    stroke(cr, [(-30, 0), (30, 0)], 2.5, GOLD_HI, alpha=0.8)
    cr.restore()
    fx, fy = x, y - 8 * s
    for (w, hh, col) in ((15, 1.0, (1.0, 0.42, 0.05)), (10, 0.78, (1.0, 0.76, 0.18)), (5.5, 0.5, (1.0, 0.97, 0.85))):
        cr.new_path()
        cr.move_to(fx - w * s, fy)
        cr.curve_to(fx - w * s, fy - hgt * hh * 0.5, fx + sway_ * hh, fy - hgt * hh * 0.8, fx + sway_ * 1.4 * hh,
                    fy - hgt * hh)
        cr.curve_to(fx + sway_ * hh, fy - hgt * hh * 0.8, fx + w * s, fy - hgt * hh * 0.5, fx + w * s, fy)
        cr.curve_to(fx + w * s, fy + 8 * s, fx - w * s, fy + 8 * s, fx - w * s, fy)
        cr.set_source_rgb(*col)
        cr.fill()
    glow(cr, fx, fy - hgt * 0.5, 70 * s, 0.55, (1.0, 0.75, 0.35))


def lamps(cr, t, y=1872, xs=(120, 330, 540, 750, 960), s=1.0):
    for k, x in enumerate(xs):
        lamp(cr, t, x, y, s, k)


@functools.lru_cache(maxsize=2)
def _vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - W / 2) / (W * 0.62)
    dy = (yy - H * 0.62) / (H * 0.62)
    v = np.clip((dx * dx + dy * dy) ** 1.3 * 0.75, 0, 0.85)
    top = np.clip((560 - yy) / 560.0, 0, 1) * 0.0
    a = np.zeros((H, W, 4), np.float32)
    a[..., 3] = np.clip(v + top, 0, 0.9)
    a[..., 0] = 0.01 * a[..., 3]
    return surface_from_rgba(a)


def light(cr, t, strength=1.0, flash=0.0):
    """The lamp light over the composed frame: warm uplight from the lamps at the front edge (flickering), a dark
    vignette, and an optional flash."""
    f = flicker(t)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(W / 2, H + 80)
    cr.scale(1.0, 1.55)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 900)
    a = (0.20 + 0.025 * f) * strength
    g.add_color_stop_rgba(0, 1.0, 0.55, 0.18, a)
    g.add_color_stop_rgba(0.5, 1.0, 0.45, 0.12, a * 0.45)
    g.add_color_stop_rgba(1, 1.0, 0.40, 0.10, 0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    cr.set_source_surface(_vignette(), 0, 0)
    cr.paint_with_alpha(0.9 + 0.08 * f)
    if flash > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_source_rgba(1.0, 0.78, 0.45, 0.35 * clamp(flash))
        cr.paint()
        cr.restore()


@functools.lru_cache(maxsize=1)
def _canvas():
    rng = np.random.default_rng(23)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = 0.018 * np.sin(xx * 2 * np.pi / 4.0) * np.sin(yy * 2 * np.pi / 4.0)
    fib = gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), (0.6, 3.0))
    fib /= fib.std() + 1e-6
    blot = gaussian_filter(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), 6)
    blot = np.kron(blot / (blot.std() + 1e-6), np.ones((8, 8), np.float32))[:H, :W]
    v = 0.955 + weave + 0.016 * fib + 0.018 * blot
    v = np.clip(v, 0.82, 1.0)
    a = np.ones((H, W, 4), np.float32)
    a[..., 0] = v
    a[..., 1] = v * 0.995
    a[..., 2] = v * 0.98
    return surface_from_rgba(a)


def finish(cr, t=0.0):
    """Canvas texture over the finished frame (multiplied), so the flat paint feels painted on cloth."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_surface(_canvas(), 0, 0)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ actors on the stage: shadow on the thera


def layer(draw_fn):
    """Draw into a transparent full-frame layer and return it (to cast a shadow from it)."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    out = draw_fn(c)
    s.flush()
    return s, out


def cast_shadow(cr, surf, dx=36.0, dy=-60.0, grow=1.09, about=(W / 2, 1800), blur=8.0, alpha=0.6):
    """The actor's soft shadow thrown up on the backdrop by the lamps in front (from a layer's alpha)."""
    k = 4
    a = np.ndarray((H, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :W, 3]
    small = a[::k, ::k].astype(np.float32) / 255.0
    small = gaussian_filter(small, blur / k * 2)
    rgba = np.zeros(small.shape + (4,), np.float32)
    rgba[..., 3] = small
    rgba[..., 0] = 0.05 * small
    rgba[..., 1] = 0.01 * small
    sh = surface_from_rgba(rgba)
    cr.save()
    cr.rectangle(CURT[0], 0, CURT[2] - CURT[0], FLOOR_Y + 10)
    cr.clip()
    cr.translate(about[0] + dx, about[1] + dy)
    cr.scale(grow, grow)
    cr.translate(-about[0], -about[1])
    cr.scale(k, k)
    cr.set_source_surface(sh, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(alpha)
    cr.restore()


def paint_layer(cr, surf, alpha=1.0):
    cr.set_source_surface(surf, 0, 0)
    cr.paint_with_alpha(alpha)


def floor_shadow(cr, x, feet, w, alpha=0.5):
    cr.save()
    cr.translate(x, feet + 8)
    cr.scale(w, w * 0.12)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, 0, 0, 0, alpha)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ light effects


def orb(cr, t, x, y, r, a=1.0):
    """A ball of golden light (power): soft glow, turning rays, a bright core with a black rim."""
    if a <= 0.01:
        return
    glow(cr, x, y, r * 7, 0.55 * a, (1.0, 0.62, 0.20))
    glow(cr, x, y, r * 3.2, 0.8 * a, (1.0, 0.85, 0.45))
    cr.save()
    cr.translate(x, y)
    cr.rotate(t * 0.6)
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(12):
        cr.rotate(2 * math.pi / 12)
        L = r * (2.4 + 0.5 * math.sin(t * 3 + i * 1.7))
        cr.move_to(r * 0.9, -r * 0.12)
        cr.line_to(L, 0)
        cr.line_to(r * 0.9, r * 0.12)
        cr.close_path()
    cr.set_source_rgba(1.0, 0.85, 0.40, 0.55 * a)
    cr.fill()
    cr.restore()
    g = cairo.RadialGradient(x - r * 0.25, y - r * 0.25, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.92, a)
    g.add_color_stop_rgba(0.55, 1.0, 0.86, 0.35, a)
    g.add_color_stop_rgba(1, 1.0, 0.55, 0.10, a)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.9 * a)
    cr.set_line_width(max(2.5, r * 0.09))
    cr.stroke()
    sparkle(cr, x, y, r * 1.9, 0.9 * a)


def sparks(cr, t, x, y, r, n=10, a=1.0, speed=0.6, seed=0):
    """Specks of light rising around a point."""
    for i in range(n):
        u = (t * speed + i / n + seed * 0.13) % 1.0
        ang = i * 2.399 + seed
        px = x + r * 0.6 * math.cos(ang) + 14 * math.sin(t * 2 + i)
        py = y + r * 0.3 * math.sin(ang) - r * 1.4 * u
        sparkle(cr, px, py, (10 + 8 * math.sin(i)) * (1 - u) + 3, a * (1 - u))


def crackle(cr, t, p0, p1, a=1.0, col=(1.0, 0.55, 0.15), seed=0, w=1.0):
    """A jagged bolt of light (a curse leaving a sage's hand), re-jagged a few times a second."""
    if a <= 0.01:
        return
    k = int(t * 12) + seed * 7
    rng = np.random.default_rng(k)
    n = 9
    pts = []
    L = math.dist(p0, p1)
    nx, ny = -(p1[1] - p0[1]) / L, (p1[0] - p0[0]) / L
    for i in range(n + 1):
        u = i / n
        off = 0 if i in (0, n) else rng.uniform(-1, 1) * L * 0.06
        pts.append((p0[0] + (p1[0] - p0[0]) * u + nx * off, p0[1] + (p1[1] - p0[1]) * u + ny * off))
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, c, al in ((26 * w, col, 0.25), (11 * w, col, 0.6), (4 * w, (1, 1, 0.9), 1.0)):
        stroke(cr, pts, lw, c, smooth=False, alpha=al * a)
    cr.restore()


def rays(cr, t, x, y, r0, r1, a=1.0, n=20, col=(1.0, 0.80, 0.35), spin=0.05):
    """Sun-rays of light around a point (power, a revelation)."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(t * spin)
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(n):
        ang = 2 * math.pi * i / n
        w = 0.05 + 0.02 * math.sin(i * 1.3)
        cr.move_to(r0 * math.cos(ang), r0 * math.sin(ang))
        cr.line_to(r1 * math.cos(ang - w), r1 * math.sin(ang - w))
        cr.line_to(r1 * math.cos(ang + w), r1 * math.sin(ang + w))
        cr.close_path()
    g = cairo.RadialGradient(0, 0, r0, 0, 0, r1)
    g.add_color_stop_rgba(0, *col, 0.55 * a)
    g.add_color_stop_rgba(1, *col, 0.0)
    cr.set_source(g)
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ Kannada text (shaped by libraqm in matplotlib)

KN_FAMILY = "Nirmala UI"           # Windows' Nirmala UI Bold carries Kannada; matplotlib >= 3.11 shapes it with libraqm


@functools.lru_cache(maxsize=256)
def kn_surface(text, size, fill=CREAM, stroke_col=INK, stroke_w=0.0, outer=None, outer_w=0.0):
    """Kannada (or any Indic) text as a cairo surface cropped to the ink: bold Nirmala UI, shaped (conjuncts, vowel
    signs, ottaksharas), with an optional inner outline (stroke_w px) and outer outline (outer_w px)."""
    from matplotlib import font_manager, patheffects
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    from PIL import Image
    from poster import to_surface
    fp = font_manager.FontProperties(family=KN_FAMILY, weight="bold", size=size)
    pad = stroke_w + outer_w + size * 0.6
    fig = Figure(figsize=((size * 0.95 * len(text) + 2 * pad) / 72.0, (size * 2.3 + 2 * pad) / 72.0), dpi=72)
    fig.patch.set_alpha(0.0)
    canvas = FigureCanvasAgg(fig)
    fx = []
    if outer is not None and outer_w > 0:
        fx.append(patheffects.Stroke(linewidth=2 * (stroke_w + outer_w), foreground=outer, joinstyle="round"))
    if stroke_w > 0:
        fx.append(patheffects.Stroke(linewidth=2 * stroke_w, foreground=stroke_col, joinstyle="round"))
    fx.append(patheffects.Normal())
    fig.text(0.5, 0.5, text, fontproperties=fp, color=fill, ha="center", va="center", path_effects=fx)
    canvas.draw()
    a = np.asarray(canvas.buffer_rgba()).copy()
    ys, xs = np.nonzero(a[..., 3] > 6)
    a = a[max(0, ys.min() - 3):ys.max() + 4, max(0, xs.min() - 3):xs.max() + 4]
    return to_surface(Image.fromarray(np.ascontiguousarray(a), "RGBA"))


def kn_text(cr, text, x, y, size, fill=CREAM, stroke_col=INK, stroke_w=0.0, outer=None, outer_w=0.0, alpha=1.0,
            anchor="cm", scale=1.0, max_w=None):
    """Paint Kannada text anchored at (x, y) (anchor l/c/r + t/m/b); returns its box (x, y, w, h)."""
    s = kn_surface(text, int(size), tuple(fill), tuple(stroke_col), float(stroke_w),
                   tuple(outer) if outer else None, float(outer_w))
    w, h = s.get_width(), s.get_height()
    k = scale
    if max_w and w * k > max_w:
        k = max_w / w
    dx = {"l": 0, "c": -w * k / 2, "r": -w * k}[anchor[0]]
    dy = {"t": 0, "m": -h * k / 2, "b": -h * k}[anchor[1]]
    if alpha > 0.005:
        cr.save()
        cr.translate(x + dx, y + dy)
        cr.scale(k, k)
        cr.set_source_surface(s, 0, 0)
        cr.get_source().set_filter(cairo.FILTER_GOOD)
        cr.paint_with_alpha(alpha)
        cr.restore()
    return x + dx, y + dy, w * k, h * k


def divider(cr, x, y, w, p=1.0, alpha=1.0):
    """A gold ornament line with a diamond at its centre, drawn out from the middle."""
    if p <= 0.01:
        return
    hw = w / 2 * ease(p)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col in ((10, INK), (5, GOLD)):
        cr.set_source_rgba(*col, alpha)
        cr.set_line_width(lw)
        cr.move_to(x - hw, y)
        cr.line_to(x + hw, y)
        cr.stroke()
    cr.restore()
    for sd in (-1, 1):
        dot(cr, x + sd * hw, y, 6, GOLD_HI, 3.0)
    cr.save()
    cr.translate(x, y)
    k = back(clamp(p * 1.4), 2.0)
    cr.scale(k, k)
    shape(cr, [(0, -18), (16, 0), (0, 18), (-16, 0)], RED, 4.0, smooth=False)
    dot(cr, 0, 0, 4, GOLD_HI)
    cr.restore()


def kn_headline(cr, t, small, big, t_small=0.0, t_big=0.4, y=150, small_size=70, big_size=150, max_w=980,
                small_col=YEL, big_col=RED, alpha=1.0, ornament=True, cx=W / 2):
    """Two-tier Kannada headline: a small turmeric-yellow setup line, then the big red key line popping in with an
    overshoot, a gold divider under it. Returns the big line's box."""
    yy = y
    if small:
        p = prog(t, t_small, 0.3)
        if p > 0:
            _, _, _, h = kn_text(cr, small, cx, yy + 22 * (1 - p), small_size, small_col, INK, 7, alpha=p * alpha,
                                 anchor="ct", max_w=max_w)
        s = kn_surface(small, int(small_size), tuple(small_col), tuple(INK), 7.0, None, 0.0)
        yy += min(s.get_height(), s.get_height() * max_w / max(1, s.get_width())) + 8
    box = None
    q = clamp((t - t_big) / 0.38)
    if q > 0:
        k = 0.55 + 0.45 * back(q, 2.2)
        s = kn_surface(big, int(big_size), tuple(big_col), tuple(CREAM), 9.0, tuple(INK), 7.0)
        fit = min(1.0, max_w / s.get_width())
        bh = s.get_height() * fit
        box = kn_text(cr, big, cx, yy + bh / 2, big_size, big_col, CREAM, 9, INK, 7, alpha=clamp(q * 2.5) * alpha,
                      anchor="cm", scale=fit * k)
        if ornament:
            divider(cr, cx, yy + bh + 22, min(max_w, s.get_width() * fit) * 0.8, prog(t, t_big + 0.2, 0.45), alpha)
    return box


def kn_banner(cr, t, t_in, lines, x, y, rot=-0.02, field=CRIMSON, alpha=1.0, quote=True, pad=(80, 40),
              max_w=900):
    """A painted cloth banner (like a small thera) with Kannada lines on it: lines = [(text, size, colour), ...].
    Unfurls from the middle at t_in; shrunk to fit max_w (the ribbon ends stick out ~50 px more each side).
    Returns its box."""
    q = clamp((t - t_in) / 0.45)
    if q <= 0:
        return None
    surfs = [kn_surface(tx, int(sz), tuple(col), tuple(INK), 6.0, None, 0.0) for tx, sz, col in lines]
    tw = max(s.get_width() for s in surfs)
    th = sum(s.get_height() for s in surfs) + 10 * (len(surfs) - 1)
    w, h = tw + 2 * pad[0], th + 2 * pad[1]
    fit = min(1.0, max_w / w)
    sx = 0.15 + 0.85 * back(q, 1.6)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(fit, fit)
    cr.push_group()
    cr.save()
    cr.scale(sx, 1.0)
    for sd in (-1, 1):                                  # the notched ribbon ends behind
        ex = sd * (w / 2 + 50)
        shape(cr, [(sd * (w / 2 - 20), -h / 2 + 24), (ex, -h / 2 + 24), (ex - sd * 36, 24), (ex, h / 2 + 24),
                   (sd * (w / 2 - 20), h / 2 + 24)], MAROON, 6.0, smooth=False)
    cr.rectangle(-w / 2 + 10, -h / 2 + 14, w, h)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    ink_fill(cr, GOLD, 7.0)
    _border_teeth(cr, -w / 2 + 4, -h / 2 + 8, w / 2 - 4, -h / 2 + 8, max(6, int(w / 34)), RED, 1)
    _border_teeth(cr, w / 2 - 4, h / 2 - 8, -w / 2 + 4, h / 2 - 8, max(6, int(w / 34)), RED, 1)
    cr.rectangle(-w / 2 + 16, -h / 2 + 30, w - 32, h - 60)
    ink_fill(cr, field, 5.0)
    for x_, y_ in along([(-w / 2 + 30, -h / 2 + 42), (w / 2 - 30, -h / 2 + 42)], int(w / 26)):
        dot(cr, x_, y_, 2.6, GOLD_HI)
    for x_, y_ in along([(-w / 2 + 30, h / 2 - 42), (w / 2 - 30, h / 2 - 42)], int(w / 26)):
        dot(cr, x_, y_, 2.6, GOLD_HI)
    cr.restore()
    if q > 0.5:
        a = clamp((q - 0.5) * 3)
        yy = -th / 2
        for s in surfs:
            cr.set_source_surface(s, -s.get_width() / 2, yy)
            cr.paint_with_alpha(a)
            yy += s.get_height() + 10
        if quote:
            kn_text(cr, "\u201c", -w / 2 + 34, -h / 2 + 52, 96, GOLD, INK, 5, alpha=a)
            kn_text(cr, "\u201d", w / 2 - 34, h / 2 - 22, 96, GOLD, INK, 5, alpha=a)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha * clamp(q * 3))
    cr.restore()
    return x - w * fit / 2, y - h * fit / 2, w * fit, h * fit


# ------------------------------------------------------------------ a whole frame, the usual way


def compose(cr, t, actors, style="crimson", motif="sun", band=True, shadow=True, flash=0.0, extra=None, ui=None,
            posts=True, lamps_on=True, musicians_at=None, light_strength=1.0, zoom=(1.0, W / 2, H * 0.6),
            behind=None):
    """Stage, actors (each a function(cr) drawing into a shared layer; they cast one shadow on the thera), lamps,
    light, UI text and the canvas finish. behind(cr): effects on the backdrop under the actors (rays of light);
    extra(cr, pts): effects drawn over the actors before the light (glows, orbs); ui(cr, pts): text on top."""
    z, zx, zy = zoom
    cr.save()
    if z != 1.0:
        cr.translate(zx, zy)
        cr.scale(z, z)
        cr.translate(-zx, -zy)
    stage(cr, t, style, motif, posts, band)
    if behind:
        behind(cr)
    if musicians_at is not None:
        mx, ms, mflip = musicians_at
        musicians(cr, t, mx, FLOOR_Y + 40, ms, mflip)
    m = cr.get_matrix()

    def draw_all(c):
        c.set_matrix(m)
        out = []
        for fn in actors:
            out.append(fn(c))
        return out
    surf, pts = layer(draw_all)
    cr.restore()
    if shadow:
        cast_shadow(cr, surf)
    paint_layer(cr, surf)
    cr.save()
    if z != 1.0:
        cr.translate(zx, zy)
        cr.scale(z, z)
        cr.translate(-zx, -zy)
    if extra:
        extra(cr, pts)
    if lamps_on:
        lamps(cr, t)
    cr.restore()
    light(cr, t, light_strength, flash)
    if ui:
        ui(cr, pts)
    finish(cr, t)
    return pts


def to_user(cr, p):
    m = cr.get_matrix()
    m.invert()
    return m.transform_point(*p)


HAS_KN = os.path.exists(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "Nirmala.ttc"))
