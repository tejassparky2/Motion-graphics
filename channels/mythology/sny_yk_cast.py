"""Cast and props for the Kannada Yakshagana reel of video 24, snake_tongue (scenes_snake_tongue_yk), built on
yaksha_kit without changing it (new parts are swapped into Y.KINDS only for the length of one figure() call, the way
ky_yk_cast does it). Everything is the kit's flat paint with thick black outlines; coordinates are frame pixels
(1080x1920) unless a function says "units".

  Garuda            the kit's actor with a red-gold hooked beak over a white painted face, a kireeta, and two huge
                    painted wings on his back (fans of red, green and gold boards with mirror bits) that spread, fold
                    and flap (pose keys sny_wing 0..1, sny_flap)
  the Nagas         snake actors: a green painted face, a cobra hood with three heads fanning behind the crown, a
                    long snake tail coiling on the floor round the feet, and a long red tongue that flicks out
                    (sny_tongue 0..1) and is single (before the story) or forked (sny_fork 0..1, the split)
  the two mothers   Vinata (Garuda's mother, saffron saree) and Kadru (the snakes' mother, dark green saree, a small
                    three-headed hood behind her hair)
  Indra             a king's look in white and blue with a halo; his vajra comes from hy_yk_cast
  props             the white stage horse (its long white tail can be wrapped by black snakes), small snakes that
                    slither on the floor, the golden pot of amrit, the sharp darbhe grass (glints, amrit drops, holy
                    glow), a broom, a puja plate, a heaven thera (gold sky, clouds, the gods' gateway)
"""
import functools
import math

import cairo
import numpy as np

import yaksha_kit as Y
from poster import H, W, back, clamp, ease

INK, RED, GOLD, CREAM, WHITE = Y.INK, Y.RED, Y.GOLD, Y.CREAM, Y.WHITE

# ------------------------------------------------------------------ colours

TONGUE = (0.88, 0.07, 0.16)
TONGUE_DK = (0.52, 0.02, 0.08)
NAGA = (0.10, 0.50, 0.26)              # snake green
NAGA_DK = (0.03, 0.26, 0.14)
NAGA_BELLY = (0.86, 0.88, 0.46)
SNAKE_BLACK = (0.10, 0.10, 0.12)
SNAKE_SHINE = (0.30, 0.34, 0.40)
EYE_Y = (1.0, 0.86, 0.10)
AMRIT = (1.0, 0.92, 0.55)
GRASS = (0.42, 0.70, 0.16)
GRASS_LT = (0.70, 0.82, 0.22)
GRASS_DK = (0.16, 0.42, 0.10)
SKY_BLUE = (0.12, 0.30, 0.72)
WOOD = (0.55, 0.30, 0.12)

# ------------------------------------------------------------------ faces and looks

Y.FACES.setdefault("sny_garuda", dict(base=(0.99, 0.92, 0.78), mark="namam", rouge=True, jaw=True))
Y.FACES.setdefault("sny_naga", dict(base=(0.46, 0.76, 0.34), mark="namam", rouge=False, jaw=True))

GARUDA = dict(Y.KING, face="sny_garuda", disc=False, jacket=Y.RED, sleeve=Y.RED, kase=(Y.YEL, Y.RED, INK, Y.GREEN),
              hem=Y.GREEN, hem_zig=Y.YEL, sash=Y.GOLD, pads=Y.RED, sny="garuda")
NAGA_A = dict(Y.HERO, face="sny_naga", crown="kireeta_small", disc=False, jacket=NAGA_DK, sleeve=NAGA_DK,
              kase=(Y.YEL, NAGA, INK, Y.RED), hem=NAGA, hem_zig=Y.YEL, sash=NAGA_BELLY, pads=NAGA_DK, sny="naga",
              edehara=False,
              hood=NAGA, tailc=NAGA)
NAGA_B = dict(NAGA_A, jacket=(0.08, 0.20, 0.36), sleeve=(0.08, 0.20, 0.36), kase=(Y.YEL, (0.08, 0.36, 0.52), INK,
                                                                                   Y.RED),
              hem=(0.08, 0.36, 0.52), pads=(0.08, 0.20, 0.36), hood=(0.10, 0.40, 0.55), tailc=(0.10, 0.40, 0.55))
NAGA_C = dict(NAGA_A, jacket=(0.40, 0.36, 0.06), sleeve=(0.40, 0.36, 0.06), kase=(Y.YEL, (0.62, 0.52, 0.06), INK,
                                                                                   NAGA),
              hem=(0.62, 0.52, 0.06), pads=(0.40, 0.36, 0.06), hood=(0.58, 0.54, 0.10), tailc=(0.58, 0.54, 0.10))
VINATA = dict(Y.WOMAN, saree=(0.98, 0.58, 0.10), border=Y.RED, blouse=(0.72, 0.06, 0.10))
KADRU = dict(Y.WOMAN, saree=(0.05, 0.32, 0.22), border=Y.GOLD, blouse=(0.10, 0.10, 0.12), sny="kadru", hood=NAGA)
INDRA = dict(Y.KING, jacket=(0.95, 0.93, 0.84), sleeve=(0.95, 0.93, 0.84), kase=(Y.YEL, SKY_BLUE, INK, Y.RED),
             hem=SKY_BLUE, hem_zig=Y.YEL, sash=SKY_BLUE, pads=SKY_BLUE, disc_cols=(Y.GOLD, SKY_BLUE, Y.WHITE),
             halo=True)
SAGE = dict(Y.SAGE)

# poses used often (upper, lower bend, wrist) -- the kit's arm convention
REST = (0.16, 0.30, 0.0)
PALM_UP = (0.70, -2.44, 0.0)          # an open palm raised beside the face
PALM_OUT = (1.25, -0.75, 0.25)        # a raised open palm to the side: stop
REACH = (1.30, 0.20, 0.0)             # an arm out to the side
FIST_UP = (2.75, 0.15, 0.0)
HOLD_UP = (2.55, 0.55, -0.2)          # both hands up holding something over the head
HOLD_CHEST = (0.55, 1.75, 0.3)        # both hands in front of the chest
HOOD_ARMS = (1.15, -1.95, 0.25)       # both forearms raised wide, palms open: the snake's spread hood
FACE_HANDS = (0.25, 2.75, -0.3)
AKIMBO = (0.45, 1.35, 0.3)
ANJALI = (0.30, 2.30, 0.0)


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def to_user(cr, p):
    m = cr.get_matrix()
    m.invert()
    return m.transform_point(*p)


# ------------------------------------------------------------------ Garuda: the wings and the beak


def _feather(cr, L, w, col, inner=None, quill=GOLD, lw=4.5, tip_dot=None):
    """A painted feather board along +x from the hub: a long leaf with an inner stripe and a quill."""
    pts = [(0, -w * 0.5), (L * 0.42, -w), (L * 0.86, -w * 0.82), (L, 0), (L * 0.86, w * 0.82), (L * 0.42, w),
           (0, w * 0.5)]
    Y.shape(cr, pts, col, lw)
    if inner:
        Y.shape(cr, [(L * 0.18, -w * 0.32), (L * 0.5, -w * 0.55), (L * 0.82, -w * 0.4), (L * 0.9, 0),
                     (L * 0.82, w * 0.4), (L * 0.5, w * 0.55), (L * 0.18, w * 0.32)], inner, 2.5)
    Y.stroke(cr, [(L * 0.06, 0), (L * 0.84, 0)], 3.0, quill)
    if tip_dot:
        Y.dot(cr, L * 0.74, 0, w * 0.22, tip_dot, 2.0)


def _wing(cr, t, spread, flap, k=1.0):
    """One wing in a frame whose +x points outward from the shoulder (units)."""
    a_top = mix(0.95, -1.42, spread) + 0.42 * flap
    a_bot = mix(1.55, 0.20, spread) + 0.30 * flap
    sc = k * mix(0.78, 1.0, spread)
    cr.save()
    cr.scale(sc, sc)
    Lmax = 560.0
    rows = ((9, 1.0, 46, Y.RED, Y.GOLD, Y.MIRROR), (8, 0.68, 42, Y.GREEN, Y.YEL, None),
            (7, 0.42, 38, Y.GOLD, Y.RED, None))
    for n, f, w, col, inner, tip in rows:
        for i in range(n):
            u = i / (n - 1)
            a = a_top + (a_bot - a_top) * (0.04 + 0.92 * u if f < 1 else u)
            L = Lmax * f * (0.80 + 0.20 * math.sin(math.pi * (0.15 + 0.7 * (1 - u))))
            cr.save()
            cr.rotate(a)
            _feather(cr, L, w, col, inner, tip_dot=tip)
            cr.restore()
    # the gold bar along the top edge, with mirror bits, and the jewelled hub
    cr.save()
    cr.rotate(a_top + 0.10)
    Y.inked_line(cr, [(0, 0), (Lmax * 0.30, -6), (Lmax * 0.52, 0)], 20, Y.GOLD, 3.5)
    Y.mirror_bits(cr, [(30, -2), (Lmax * 0.30, -6), (Lmax * 0.50, 0)], 6, 3.2)
    cr.restore()
    Y.dot(cr, 0, 0, 44, Y.GOLD, 5.0)
    Y.dot(cr, 0, 0, 26, Y.RED, 3.5)
    Y.dot(cr, 6, -7, 7, Y.WHITE)
    cr.restore()


def _garuda_wings(ctx):
    cr, p, t = ctx.cr, ctx.p, ctx.t
    spread = clamp(p.get("sny_wing", 1.0))
    flap = p.get("sny_flap", 0.0)
    for sd in (-1, 1):
        cr.save()
        cr.translate(sd * 96, -282)
        cr.scale(sd, 1)
        _wing(cr, t, spread, flap)
        cr.restore()


def _garuda_beak(ctx):
    """The hooked beak mask over the nose and mouth (face units, seen from the front): a vermilion beak with a gold
    ridge and edge, red nostrils; sny_beak opens the lower beak."""
    cr, p = ctx.cr, ctx.p
    cr.translate(0, Y.FACE_C)
    turn = p["turn"]
    cr.translate(turn * 12, 0)
    op = clamp(p.get("sny_beak", 0.0))
    if op > 0.01:                                       # the lower beak dropping open
        Y.shape(cr, [(-26, 52), (26, 52), (20, 90 + 30 * op), (0, 104 + 40 * op), (-20, 90 + 30 * op)],
                (0.60, 0.08, 0.06), 4.5)
        Y.shape(cr, [(-14, 62), (14, 62), (0, 92 + 30 * op)], (0.30, 0.02, 0.03), 0)
    up = [(0, -40), (20, -24), (33, 6), (35, 40), (28, 74), (16, 106), (4, 132), (-6, 140), (-10, 126), (-16, 104),
          (-28, 74), (-35, 40), (-33, 6), (-20, -24)]
    Y.shape(cr, up, (0.93, 0.24, 0.08), 6.0)
    Y.shape(cr, [(0, -30), (9, -10), (8, 60), (2, 118), (-4, 118), (-8, 60), (-9, -10)], Y.GOLD, 2.5)
    Y.stroke(cr, [(-31, 44), (-22, 82), (-8, 114)], 4.0, Y.GOLD)
    Y.stroke(cr, [(31, 44), (22, 82), (8, 114)], 4.0, Y.GOLD)
    for sd in (-1, 1):
        Y.oval(cr, sd * 19, 22, 5, 9, (0.40, 0.02, 0.03), 2.0, rot=sd * 0.3)
    for sd in (-1, 1):                                  # white feather marks from the eyes out to the temples
        for k in range(3):
            Y.stroke(cr, [(sd * (52 + 6 * k), 30 + 14 * k), (sd * (66 + 8 * k), 50 + 16 * k)], 4.5, Y.WHITE)


# ------------------------------------------------------------------ the Nagas: hood, tail, tongue


def cobra_head(cr, x, y, r, col, t=0.0, fork=1.0, flick=0.0, rot=0.0, belly=NAGA_BELLY):
    """A small cobra head seen from the front (r = half width), with its own little hood behind it."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    Y.shape(cr, [(0, -0.2 * r), (1.55 * r, 0.25 * r), (1.65 * r, 1.0 * r), (1.0 * r, 1.9 * r), (0, 2.1 * r),
                 (-1.0 * r, 1.9 * r), (-1.65 * r, 1.0 * r), (-1.55 * r, 0.25 * r)], col, 4.0)
    Y.shape(cr, [(0, 0.5 * r), (0.8 * r, 0.9 * r), (0.6 * r, 1.7 * r), (0, 1.9 * r), (-0.6 * r, 1.7 * r),
                 (-0.8 * r, 0.9 * r)], belly, 2.5)
    Y.shape(cr, [(0, -r), (0.75 * r, -0.75 * r), (1.0 * r, 0), (0.62 * r, 0.75 * r), (0, 0.95 * r),
                 (-0.62 * r, 0.75 * r), (-1.0 * r, 0), (-0.75 * r, -0.75 * r)], col, 4.0)
    for sd in (-1, 1):
        Y.oval(cr, sd * 0.42 * r, -0.12 * r, 0.24 * r, 0.22 * r, EYE_Y, 2.5)
        Y.oval(cr, sd * 0.42 * r, -0.12 * r, 0.06 * r, 0.17 * r, INK, 0)
        Y.dot(cr, sd * 0.16 * r, 0.55 * r, 0.06 * r, INK)
    if flick > 0.05:
        cr.save()
        cr.translate(0, 0.92 * r)
        tongue(cr, 0.9 * r * flick, fork, 0.0, w=0.16 * r, lw=2.0)
        cr.restore()
    cr.restore()


def tongue(cr, L, fork=1.0, wig=0.0, w=22.0, lw=4.5, col=TONGUE, glow=0.0):
    """A snake's tongue from (0, 0) downward (+y), L long: single and pointed at fork 0, split into two prongs at
    fork 1 (the split runs up from the tip). wig = side-to-side wiggle -1..1."""
    if L <= 1:
        return
    fs = 0.20 + 0.28 * clamp(fork)
    ys = L * (1 - fs)
    n = 10
    stem = [(wig * 0.14 * L * math.sin(math.pi * 0.9 * i / n) * (i / n), ys * i / n) for i in range(n + 1)]
    sx, sy = stem[-1]
    dx = stem[-1][0] - stem[-2][0]
    dy = stem[-1][1] - stem[-2][1]
    base_a = math.atan2(dx, dy)
    ang = 0.03 + 0.40 * clamp(fork)
    pl = fs * L * (1.0 + 0.12 * clamp(fork))
    prongs = []
    for sd in (-1, 1):
        a = base_a + sd * ang
        tx, ty = sx + pl * math.sin(a), sy + pl * math.cos(a)
        nx, ny = math.cos(a), -math.sin(a)
        hw = w * (0.5 if fork > 0.02 else 0.5)
        ox = sd * (w * 0.25 * min(1.0, fork * 4))       # the two halves of the stem's width
        prongs.append([(sx + ox - nx * hw * 0.55, sy - ny * hw * 0.55), (sx + ox + nx * hw * 0.55, sy + ny * hw * 0.55),
                       (tx, ty)])
    if glow > 0.01:
        Y.glow(cr, sx, sy, 2.2 * L, 0.35 * glow, (1.0, 0.6, 0.5))
    # the black edge first, then the red, so the joins have no inner lines
    Y.stroke(cr, stem, w + 2 * lw, INK)
    for pr in prongs:
        cr.new_path()
        Y.poly(cr, pr)
        cr.set_source_rgb(*INK)
        cr.set_line_width(2 * lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
        cr.fill()
    Y.stroke(cr, stem, w, col)
    for pr in prongs:
        cr.new_path()
        Y.poly(cr, pr)
        cr.set_source_rgb(*col)
        cr.fill()
    Y.stroke(cr, stem[1:-1], max(1.5, w * 0.16), TONGUE_DK)


def tongue_tips(L, fork, wig=0.0):
    """Where the tongue's split point and tips are (same frame as tongue())."""
    fs = 0.20 + 0.28 * clamp(fork)
    ys = L * (1 - fs)
    sx = wig * 0.14 * L * math.sin(math.pi * 0.9) * 1.0
    ang = 0.03 + 0.40 * clamp(fork)
    pl = fs * L * (1.0 + 0.12 * clamp(fork))
    return (sx, ys), [(sx + sd * pl * math.sin(ang), ys + pl * math.cos(ang)) for sd in (-1, 1)]


def _hood(cr, t, look, p, k=1.0, heads=3):
    """The cobra hood behind the head (face-centre units): a wide hood with a pale belly panel and a gold rim, and
    three cobra heads fanning over the crown."""
    col = look.get("hood", NAGA)
    dk = tuple(c * 0.55 for c in col)
    fork = p.get("sny_fork", 1.0)
    cr.save()
    cr.scale(k, k)
    out = [(-110, 150), (-178, 50), (-214, -80), (-208, -200), (-160, -300), (-86, -356), (0, -372), (86, -356),
           (160, -300), (208, -200), (214, -80), (178, 50), (110, 150)]
    Y.shape(cr, out, col, 7.0)
    Y.stroke(cr, out, 9.0, Y.GOLD)
    Y.stroke(cr, out, 2.0, INK)
    belly = [(-74, 130), (-128, 30), (-148, -90), (-120, -210), (-60, -270), (0, -282), (60, -270), (120, -210),
             (148, -90), (128, 30), (74, 130)]
    Y.shape(cr, belly, NAGA_BELLY, 4.0)
    cr.save()
    cr.new_path()
    Y.spath(cr, belly)
    cr.clip()
    for i in range(9):                                  # the belly scales
        y = -250 + 44 * i
        Y.stroke(cr, [(-160, y + 18), (0, y), (160, y + 18)], 4.0, dk, alpha=0.8)
    cr.restore()
    Y.mirror_bits(cr, out[1:-1], 16, 3.4)
    sw = 0.05 * math.sin(t * 1.6)
    spots = ((-150, -250, 38, -0.45), (150, -250, 38, 0.45), (0, -330, 50, 0.0))[:heads]
    for i, (x, y, r, a) in enumerate(spots):
        fl = max(0.0, math.sin(t * 5.0 + i * 2.1)) ** 3
        cobra_head(cr, x, y, r, col, t, fork, fl, a + sw)
    cr.restore()


def _naga_hood(ctx):
    cr, look, p, t = ctx.cr, ctx.look, ctx.p, ctx.t
    cr.translate(0, Y.FACE_C)
    if look.get("sny") == "kadru":
        cr.translate(0, -10)
        _hood(cr, t, look, p, 0.62, 3)
    else:
        _hood(cr, t, look, p, 1.0, 3)


def _naga_tail(ctx):
    """A long snake tail that comes out under the skirt and coils on the floor in front of the feet (root units)."""
    cr, look, p, t = ctx.cr, ctx.look, ctx.p, ctx.t
    sw = 12 * math.sin(t * 1.8) + p.get("sny_tailsw", 0.0)
    th, sh, ft, hh = Y.leg_solve(p["bend"], 0.0)
    fy = hh - 14                                         # the floor, just above the soles
    pts = [(150, 200), (215, 300), (220, fy - 50), (150, fy + 6), (0, fy + 18), (-170, fy + 8), (-280, fy - 30),
           (-310 + sw * 0.4, fy - 90), (-282 + sw, fy - 128)]
    col = look.get("tailc", NAGA)
    dk = tuple(c * 0.55 for c in col)
    fl = Y.flat(cr, pts, closed=False)
    n = len(fl)
    left, right = [], []
    for i in range(n):
        a = fl[max(0, i - 1)]
        b = fl[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        u = i / (n - 1)
        hw = 44 * (1 - u) ** 0.8 + 4
        x, y = fl[i]
        left.append((x + nx * hw, y + ny * hw))
        right.append((x - nx * hw, y - ny * hw))
    cr.new_path()
    Y.poly(cr, left + right[::-1])
    Y.ink_fill(cr, col, 6.0)
    cr.save()
    cr.new_path()
    Y.poly(cr, left + right[::-1])
    cr.clip()
    for i in range(4, n - 2, 7):                         # bands of scales across the tail
        x, y = fl[i]
        a, b = left[i], right[i]
        Y.stroke(cr, [a, ((a[0] + b[0]) / 2 + 4, (a[1] + b[1]) / 2 + 6), b], 7.0, dk, alpha=0.9)
    Y.stroke(cr, [((l[0] * 2 + r[0]) / 3, (l[1] * 2 + r[1]) / 3) for l, r in zip(left[2:-3], right[2:-3])][::3],
             8.0, NAGA_BELLY, alpha=0.85)
    cr.restore()


def _naga_tongue(ctx):
    cr, p = ctx.cr, ctx.p
    cr.translate(0, Y.FACE_C)
    L = p.get("sny_tongue", 0.0) * 240.0
    turn = p["turn"]
    cr.translate(turn * 15, 48)
    ctx.mark("mouth", 0, 0)
    if L > 1:
        wig = p.get("sny_wig", 0.0)
        fork = p.get("sny_fork", 1.0)
        tongue(cr, L, fork, wig, w=26.0, glow=p.get("sny_tglow", 0.0))
        sp, tips = tongue_tips(L, fork, wig)
        ctx.mark("fork", *sp)
        ctx.mark("tipL", *tips[0])
        ctx.mark("tipR", *tips[1])
        ctx.mark("ttip", (tips[0][0] + tips[1][0]) / 2, (tips[0][1] + tips[1][1]) / 2)
    else:
        ctx.mark("fork", 0, 0)
        ctx.mark("ttip", 0, 0)


def _naga_scales(ctx):
    """Rows of snake scales painted on the plain chest (no gold chest plate, so the red tongue reads)."""
    cr, look = ctx.cr, ctx.look
    col = look.get("hood", NAGA)
    cr.save()
    cr.new_path()
    Y.spath(cr, Y.TORSO)
    cr.clip()
    for row in range(8):
        y = -286 + 30 * row
        for k in range(-4, 5):
            x = k * 34 + (17 if row % 2 else 0)
            if abs(x) > 96:
                continue
            cr.new_path()
            cr.arc(x, y, 15, 0.15 * math.pi, 0.85 * math.pi)
            cr.set_source_rgba(*col, 0.85)
            cr.set_line_width(5)
            cr.stroke()
    cr.restore()


@functools.lru_cache(maxsize=8)
def _parts(kind, extra):
    out = []
    if extra == "garuda":
        out.append(("torso", _garuda_wings))
    for part, fn in Y.KINDS[kind]:
        if extra == "naga" and part == "root" and fn is Y.kase:
            out.append(("root", _naga_tail))
        out.append((part, fn))
        if extra == "naga" and part == "torso" and fn is Y.torso:
            out.append(("torso", _naga_scales))
        if extra in ("naga", "kadru") and part == "head" and fn is Y.crown_back:
            out.insert(len(out) - 1, ("head", _naga_hood))
        if part == "head" and fn is Y.head and extra == "garuda":
            out.append(("head", _garuda_beak))
    if extra == "naga":
        out.append(("head", _naga_tongue))
    return out


def figure(cr, look, x, feet, s=1.0, t=0.0, pose=None, flip=False, alpha=1.0):
    """yaksha_kit.figure with this reel's extra parts (Garuda's wings and beak; the Nagas' hood, tail and tongue;
    Kadru's hood) swapped in for the call."""
    kind = look.get("kind", "actor")
    extra = look.get("sny")
    if not extra:
        return Y.figure(cr, look, x, feet, s, t, pose, flip, alpha)
    old = Y.KINDS[kind]
    Y.KINDS[kind] = _parts(kind, extra)
    try:
        return Y.figure(cr, look, x, feet, s, t, pose, flip, alpha)
    finally:
        Y.KINDS[kind] = old


# ------------------------------------------------------------------ the white horse (a painted stage horse)

HORSE_TAIL = [(236, -402), (284, -368), (312, -296), (318, -206), (308, -116), (322, -26)]


def _tail_line(sw):
    return [(x + sw * (i / 5) ** 1.3 * 40, y) for i, (x, y) in enumerate(HORSE_TAIL)]


def horse(cr, t, x, feet, s=1.0, flip=False, black=0.0, coils=0.0, prance=0.0, alpha=1.0, step=0.0):
    """The white horse Uchchaihshravas as a flat painted stage horse seen from the side, facing left (flip: right),
    hooves on `feet`. black 0..1 darkens the tail; coils 0..1 wraps it in black snakes from the bottom up (their heads
    peek out); prance lifts a front leg; step walks the legs."""
    if alpha <= 0.01:
        return {}
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x, feet)
    cr.scale(-s if flip else s, s)
    body = WHITE
    far = (0.84, 0.83, 0.78)
    sw = 0.5 * math.sin(t * 1.7)
    tl = _tail_line(sw)
    # the tail (behind the body): long white hair, strands
    fl = Y.flat(cr, tl, closed=False)
    n = len(fl)
    left, right = [], []
    for i in range(n):
        a, b = fl[max(0, i - 1)], fl[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        u = i / (n - 1)
        hw = 26 + 30 * math.sin(math.pi * min(1.0, u * 1.25)) * (1 - 0.6 * u) + 4
        left.append((fl[i][0] + nx * hw, fl[i][1] + ny * hw))
        right.append((fl[i][0] - nx * hw, fl[i][1] - ny * hw))
    tail_col = mix(body, SNAKE_BLACK, black)
    cr.new_path()
    Y.poly(cr, left + right[::-1])
    Y.ink_fill(cr, tail_col, 6.0)
    for k in range(-2, 3):                              # hair strands
        pts = [(fl[i][0] + (left[i][0] - fl[i][0]) * k * 0.35, fl[i][1] + (left[i][1] - fl[i][1]) * k * 0.35)
               for i in range(2, n - 2, 3)]
        Y.stroke(cr, pts, 2.5, mix((0.70, 0.70, 0.72), SNAKE_SHINE, black), alpha=0.9)
    if coils > 0.01:
        _coils(cr, t, fl, left, right, coils)
    # legs on the far side
    walk = step

    def leg(x0, ph, col, lift=0.0):
        k = math.sin(walk * 2 * math.pi + ph) if walk else 0.0
        a = 0.18 * k - 0.55 * lift
        cr.save()
        cr.translate(x0, -262)
        cr.rotate(a)
        Y.capsule(cr, 26, 20, 130)
        Y.ink_fill(cr, col, 5.0)
        cr.translate(0, 130)
        cr.rotate(-a + 1.4 * lift + 0.1 * max(0.0, -k))
        Y.capsule(cr, 19, 15, 120)
        Y.ink_fill(cr, col, 5.0)
        cr.translate(0, 120)
        Y.shape(cr, [(-20, -6), (20, -6), (26, 18), (-24, 18)], Y.GOLD, 4.0, smooth=False)
        cr.restore()
    leg(-112, 0.0, far)
    leg(178, math.pi, far)
    # the body
    Y.shape(cr, [(-205, -300), (-232, -362), (-192, -424), (-80, -448), (60, -444), (172, -432), (238, -390),
                 (250, -322), (218, -268), (120, -250), (0, -246), (-120, -256), (-190, -272)], body, 7.0)
    # the near legs
    leg(-160, math.pi, body, prance)
    leg(132, 0.0, body)
    # the neck and the head
    Y.shape(cr, [(-178, -398), (-222, -500), (-262, -590), (-296, -646), (-238, -664), (-196, -596), (-148, -496),
                 (-104, -432)], body, 7.0)
    head = [(-252, -682), (-300, -672), (-352, -632), (-402, -586), (-420, -560), (-404, -538), (-362, -532),
            (-312, -552), (-270, -586), (-236, -626)]
    Y.shape(cr, head, body, 7.0)
    Y.shape(cr, [(-262, -676), (-270, -728), (-244, -684)], body, 5.0, smooth=False)        # the ear
    Y.oval(cr, -302, -630, 13, 11, INK, 0)
    Y.dot(cr, -298, -633, 3.5, WHITE)
    Y.stroke(cr, [(-318, -642), (-292, -646)], 3.0)
    Y.dot(cr, -402, -566, 5.5, (0.40, 0.25, 0.25))
    Y.stroke(cr, [(-410, -546), (-378, -542)], 3.0)
    # the mane (gold) along the neck
    mane = [(-250, -688), (-226, -640), (-196, -580), (-168, -520), (-140, -464), (-110, -430)]
    zz = []
    for i, (mx, my) in enumerate(Y.along(mane, 12)):
        zz.append((mx + (20 if i % 2 else 4), my - (6 if i % 2 else 0)))
    Y.inked_line(cr, mane, 22, (0.99, 0.86, 0.40), 3.0)
    Y.stroke(cr, zz, 4.0, Y.GOLD_DK, smooth=False)
    # the harness: a gold bridle with mirror bits, a red plume, a breast collar with bells, the saddle cloth
    Y.stroke(cr, [(-262, -664), (-330, -588), (-372, -552)], 9.0, Y.GOLD)
    Y.stroke(cr, [(-262, -664), (-330, -588), (-372, -552)], 2.0)
    Y.stroke(cr, [(-282, -612), (-262, -560), (-248, -540)], 8.0, Y.GOLD)
    Y.mirror_bits(cr, [(-262, -664), (-330, -588)], 4, 3.0)
    Y.shape(cr, [(-252, -690), (-262, -742), (-246, -790), (-226, -748), (-238, -690)], Y.RED, 4.0)
    Y.dot(cr, -246, -694, 9, Y.GOLD, 3.0)
    Y.stroke(cr, [(-200, -430), (-232, -360), (-206, -296)], 14.0, Y.RED)
    Y.dot_row(cr, [(-200, -430), (-232, -360), (-206, -296)], 6, 7.0, Y.GOLD, lw=2.0)
    Y.shape(cr, [(-96, -450), (126, -440), (148, -320), (40, -300), (-60, -300), (-118, -320)], Y.RED, 5.5)
    Y.shape(cr, [(-80, -440), (110, -432), (128, -334), (40, -318), (-56, -318), (-102, -334)], Y.GREEN, 3.5)
    Y.dot_row(cr, [(-104, -326), (-60, -306), (40, -306), (140, -326)], 10, 4.0, Y.MIRROR, lw=1.5)
    for i, (px, py) in enumerate(Y.along([(-110, -320), (-60, -302), (40, -302), (140, -322)], 7)):
        Y.stroke(cr, [(px, py), (px, py + 22)], 2.5)
        Y.dot(cr, px, py + 28, 8, (Y.YEL, Y.RED)[i % 2], 2.5)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    return {}


def _coils(cr, t, fl, left, right, p):
    """Black snakes wound round the horse's tail, the bands appearing from the bottom up as p goes 0 -> 1, with three
    snake heads peeking out."""
    n = len(fl)
    m = 7
    idx = [int(round(4 + (n - 9) * (j + 0.5) / m)) for j in range(m)][::-1]      # bottom first
    for j, i in enumerate(idx):
        q = clamp(p * m * 1.15 - j)
        if q <= 0:
            continue
        a, b = left[i], right[i]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        pts = [(a[0] - 10, a[1] - 8), (mx, my + 20), (b[0] + 10, b[1] - 8)]
        e = ease(q)
        part = [pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * min(1.0, 2 * e),
                         pts[0][1] + (pts[1][1] - pts[0][1]) * min(1.0, 2 * e))]
        if e > 0.5:
            f = 2 * e - 1
            part.append((pts[1][0] + (pts[2][0] - pts[1][0]) * f, pts[1][1] + (pts[2][1] - pts[1][1]) * f))
        Y.stroke(cr, part, 40, INK)
        Y.stroke(cr, part, 30, SNAKE_BLACK)
        Y.stroke(cr, [(x, y + 7) for x, y in part], 6, (0.62, 0.64, 0.58), alpha=0.9)        # the pale belly line
        Y.stroke(cr, [(x, y - 7) for x, y in part], 3, SNAKE_SHINE, alpha=0.9)
    heads = ((idx[0], 1, 0.2), (idx[3], -1, 0.55), (idx[6], 1, 0.9))
    for i, sd, at in heads:
        q = clamp((p - at + 0.15) / 0.2)
        if q <= 0:
            continue
        a = left[i] if sd < 0 else right[i]
        cr.save()
        cr.translate(a[0] + sd * 24, a[1] - 6)
        cr.rotate(sd * 1.35)
        k = back(q, 2.0)
        cr.scale(k, k)
        fl_ = max(0.0, math.sin(t * 6 + i)) ** 2
        cobra_head(cr, 0, 0, 30, SNAKE_BLACK, t, 0.0, fl_, 0.0, belly=(0.62, 0.64, 0.58))
        cr.restore()


# ------------------------------------------------------------------ a small snake on the floor


def snake(cr, t, pts, w=24.0, col=SNAKE_BLACK, belly=(0.32, 0.32, 0.36), flick=0.0, fork=0.0, hood=0.6,
          alpha=1.0, head_k=1.0):
    """A snake along pts (tail tip first, head last), tapering to the tail, with a small hood, yellow eyes and a
    tongue that flicks (flick 0..1; fork 0 = single tongue, 1 = split)."""
    if alpha <= 0.01 or len(pts) < 2:
        return
    if alpha < 0.999:
        cr.push_group()
    fl = Y.flat(cr, pts, closed=False)
    n = len(fl)
    left, right = [], []
    for i in range(n):
        a, b = fl[max(0, i - 1)], fl[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        u = i / (n - 1)
        hw = w * (0.15 + 0.85 * min(1.0, u * 2.2)) * (1 - 0.15 * max(0.0, u - 0.85) / 0.15) / 2
        left.append((fl[i][0] + nx * hw, fl[i][1] + ny * hw))
        right.append((fl[i][0] - nx * hw, fl[i][1] - ny * hw))
    cr.new_path()
    Y.poly(cr, left + right[::-1])
    Y.ink_fill(cr, col, 4.5)
    Y.stroke(cr, [((l[0] * 3 + r[0]) / 4, (l[1] * 3 + r[1]) / 4) for l, r in zip(left[3:-2], right[3:-2])][::2],
             max(2.0, w * 0.14), belly, alpha=0.9)
    hx, hy = fl[-1]
    px, py = fl[max(0, n - 4)]
    ang = math.atan2(hy - py, hx - px)
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(ang)
    k = head_k * w / 24.0
    cr.scale(k, k)
    if hood > 0.01:                                     # the hood flaring behind the head
        hw = 24 + 14 * hood
        Y.shape(cr, [(-46, 0), (-26, -hw), (4, -hw * 0.8), (14, 0), (4, hw * 0.8), (-26, hw)], col, 4.0)
    Y.shape(cr, [(-14, -15), (14, -13), (30, -6), (36, 0), (30, 6), (14, 13), (-14, 15)], col, 4.0)
    for sd in (-1, 1):
        Y.dot(cr, 14, sd * 8, 4.5, EYE_Y, 1.5)
        Y.oval(cr, 14, sd * 8, 1.6, 3.6, INK, 0)
    if flick > 0.05:
        cr.save()
        cr.translate(36, 0)
        cr.rotate(-math.pi / 2)
        tongue(cr, 34 * flick, fork, 0.0, w=6.0, lw=2.0)
        cr.restore()
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


def wave_path(x0, y0, x1, y1, t, amp=18.0, waves=2.0, n=18, speed=6.0):
    """A slithering S-curve from (x0, y0) (tail) to (x1, y1) (head)."""
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    out = []
    for i in range(n + 1):
        u = i / n
        o = amp * math.sin(2 * math.pi * waves * u - speed * t) * (0.4 + 0.6 * u) * (1 - 0.6 * u ** 4)
        out.append((x0 + ux * L * u + nx * o, y0 + uy * L * u + ny * o))
    return out


# ------------------------------------------------------------------ the pot of amrit


def pot(cr, t, x, y, s=1.0, glow=1.0, alpha=1.0, tilt=0.0, lid=1.0):
    """The golden pot of amrit (a kalasha with a domed lid), its bottom centre on (x, y); about 250 units tall."""
    if alpha <= 0.01:
        return
    if glow > 0.01:
        Y.glow(cr, x, y - 120 * s, 330 * s, 0.45 * glow * alpha, (1.0, 0.85, 0.45))
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s, s)
    Y.shape(cr, [(-48, -6), (48, -6), (56, 0), (-56, 0)], Y.GOLD_DK, 4.5, smooth=False)          # the foot
    body = [(-40, -10), (-84, -46), (-100, -96), (-88, -146), (-50, -176), (-30, -186), (30, -186), (50, -176),
            (88, -146), (100, -96), (84, -46), (40, -10)]
    Y.shape(cr, body, Y.GOLD, 6.5)
    cr.save()
    cr.new_path()
    Y.spath(cr, body)
    cr.clip()
    g = cairo.LinearGradient(-100, 0, 100, 0)
    for u, a in ((0, 0.35), (0.35, 0.0), (0.6, 0.0), (1, 0.4)):
        g.add_color_stop_rgba(u, 0.45, 0.22, 0.02, a)
    cr.set_source(g)
    cr.paint()
    Y.stroke(cr, [(-110, -100), (0, -88), (110, -100)], 22, Y.RED)
    Y.dot_row(cr, [(-96, -100), (0, -88), (96, -100)], 9, 4.2, WHITE)
    Y.stroke(cr, [(-110, -64), (0, -52), (110, -64)], 4.0, Y.GOLD_DK)
    Y.stroke(cr, [(-110, -136), (0, -126), (110, -136)], 4.0, Y.GOLD_DK)
    Y.oval(cr, -46, -150, 12, 22, Y.GOLD_HI, 0, rot=0.4)
    cr.restore()
    Y.shape(cr, [(-30, -184), (30, -184), (26, -204), (46, -218), (-46, -218), (-26, -204)], Y.GOLD, 5.0,
            smooth=False)                                                                           # neck and rim
    if lid > 0.01:
        Y.shape(cr, [(-44, -218), (-40, -238), (-24, -256), (0, -264), (24, -256), (40, -238), (44, -218)], Y.GOLD,
                5.0)
        Y.stroke(cr, [(-40, -232), (40, -232)], 3.0)
        Y.dot(cr, 0, -276, 13, Y.GOLD, 4.0)
        Y.dot(cr, 0, -276, 6, Y.RED, 0)
    cr.restore()
    if glow > 0.01:
        for i in range(5):                                # light rising from the nectar
            u = (t * 0.55 + i / 5) % 1.0
            Y.sparkle(cr, x + (34 * math.sin(i * 2.3 + t)) * s, y - (230 + 160 * u) * s, (16 * (1 - u) + 4) * s,
                      glow * alpha * (1 - u))
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


def pot_outline(cr, x, y, s=1.0, alpha=1.0):
    """A dotted outline where the pot stood (it is gone)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pts = [(-40, -10), (-84, -46), (-100, -96), (-88, -146), (-50, -176), (-30, -186), (-28, -204), (-46, -218),
           (-40, -238), (0, -264), (40, -238), (46, -218), (28, -204), (30, -186), (50, -176), (88, -146), (100, -96),
           (84, -46), (40, -10)]
    for px, py in Y.along(Y.flat(cr, pts, closed=False), 30):
        Y.dot(cr, px, py, 7, CREAM, 2.5)
    cr.restore()


def drop_icon(cr, x, y, r, col=AMRIT, alpha=1.0):
    """One drop of nectar."""
    cr.save()
    cr.translate(x, y)
    cr.push_group()
    Y.shape(cr, [(0, -1.6 * r), (0.55 * r, -0.4 * r), (r, 0.3 * r), (0.8 * r, 0.9 * r), (0, 1.15 * r),
                 (-0.8 * r, 0.9 * r), (-r, 0.3 * r), (-0.55 * r, -0.4 * r)], col, max(3.0, r * 0.12))
    Y.oval(cr, -0.35 * r, 0.25 * r, 0.16 * r, 0.3 * r, WHITE, 0, rot=0.4)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


# ------------------------------------------------------------------ the darbhe (kusha) grass


def _blades(n, seed):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        u = (i + 0.5) / n
        a = (u - 0.5) * 1.15 + rng.uniform(-0.06, 0.06)
        L = 300 + 110 * math.cos((u - 0.5) * 2.4) + rng.uniform(-25, 25)
        bx = (u - 0.5) * 150
        out.append((bx, a, L, i % 3))
    return out


def darbhe(cr, t, x, y, s=1.0, n=15, seed=4, glint=0.0, holy=0.0, drops=0.0, alpha=1.0, wind=1.0, drop_k=1.0):
    """A clump of long sharp darbhe blades rising from (x, y): pointed tips (glint: light running to the tips =
    sharp), drops of amrit shining on them (drops), and a golden holy light (holy). Returns the tips (frame px)."""
    if alpha <= 0.01:
        return []
    if holy > 0.01:
        Y.rays(cr, t, x, y - 220 * s, 60 * s, 620 * s, 0.75 * holy, 18, (1.0, 0.86, 0.40), 0.12)
        Y.glow(cr, x, y - 200 * s, 420 * s, 0.45 * holy, (1.0, 0.85, 0.45))
    if alpha < 0.999:
        cr.push_group()
    tips = []
    cols = (GRASS, GRASS_LT, GRASS_DK)
    order = sorted(_blades(n, seed), key=lambda b: (b[3] != 2, abs(b[1])), reverse=False)
    for bx, a, L, kind in order:
        sw = 0.04 * wind * math.sin(t * 1.6 + bx * 0.02)
        aa = a + sw
        tx, ty = x + (bx + L * math.sin(aa)) * s, y - L * math.cos(aa) * s
        mx, my = x + (bx + 0.5 * L * math.sin(aa * 0.8)) * s, y - 0.5 * L * math.cos(aa * 0.8) * s
        w0 = 15 * s
        nx, ny = math.cos(aa), math.sin(aa)
        pts = [(x + bx * s - w0, y), (mx - nx * w0 * 0.75, my - ny * w0 * 0.75), (tx, ty),
               (mx + nx * w0 * 0.75, my + ny * w0 * 0.75), (x + bx * s + w0, y)]
        col = cols[kind]
        if holy > 0.01:
            col = mix(col, (0.98, 0.84, 0.30), 0.55 * holy)
        cr.new_path()
        Y.spath(cr, pts, closed=True)
        Y.ink_fill(cr, col, 4.0 * max(0.6, s))
        Y.stroke(cr, [(x + bx * s, y), (mx, my), (tx, ty)], 2.0 * max(0.6, s), GRASS_DK, alpha=0.7)
        tips.append((tx, ty))
    for i, (tx, ty) in enumerate(tips):
        if glint > 0.01 and i % 3 == 1:
            ph = (t * 1.4 + i * 0.37) % 1.0
            Y.sparkle(cr, tx, ty, 26 * s * glint * (0.6 + 0.4 * math.sin(math.pi * ph)), glint)
        if drops > 0.01 and i % 2 == 0:
            Y.glow(cr, tx, ty + 30 * s * drop_k, 50 * s * drop_k, 0.6 * drops, (1.0, 0.85, 0.40))
            drop_icon(cr, tx + 4 * s, ty + 36 * s * drop_k, 11 * s * drop_k, AMRIT, min(1.0, drops))
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    return tips


def blade(cr, x0, y0, x1, y1, w, col=GRASS, glint=0.0, t=0.0):
    """One big sharp blade from (x0, y0) (root) to (x1, y1) (tip), w wide at the root."""
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    m = (x0 + ux * L * 0.5, y0 + uy * L * 0.5)
    pts = [(x0 - nx * w / 2, y0 - ny * w / 2), (m[0] - nx * w * 0.4, m[1] - ny * w * 0.4), (x1, y1),
           (m[0] + nx * w * 0.4, m[1] + ny * w * 0.4), (x0 + nx * w / 2, y0 + ny * w / 2)]
    cr.new_path()
    Y.spath(cr, pts, closed=True)
    Y.ink_fill(cr, col, 5.0)
    Y.stroke(cr, [(x0, y0), (x1 - ux * 20, y1 - uy * 20)], 3.0, GRASS_DK, alpha=0.75)
    if glint > 0.01:                                    # light running up the sharp edge to the tip
        u = (t * 0.9) % 1.0
        d, o = L * (0.3 + 0.7 * u), w * 0.3 * (1 - u)
        px, py = x0 + ux * d - nx * o, y0 + uy * d - ny * o
        Y.sparkle(cr, px, py, 30 * glint, glint)
        Y.sparkle(cr, x1, y1, 22 * glint, glint)


# ------------------------------------------------------------------ small props


def broom(cr, x, y, s=1.0, rot=0.0, alpha=1.0):
    """A coconut-leaf broom, held at (x, y), hanging along +y (about 360 units)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    Y.shape(cr, [(-14, -20), (14, -20), (16, 70), (-16, 70)], (0.62, 0.40, 0.16), 4.5, smooth=False)
    Y.stroke(cr, [(-16, 30), (16, 30)], 8.0, Y.RED, cap=cairo.LINE_CAP_BUTT)
    Y.shape(cr, [(-16, 66), (16, 66), (64, 330), (-64, 330)], (0.86, 0.70, 0.36), 4.5)
    for k in range(-5, 6):
        Y.stroke(cr, [(k * 2.5, 72), (k * 11, 326)], 2.2, (0.55, 0.40, 0.16))
    cr.restore()


def puja_plate(cr, t, x, y, s=1.0, alpha=1.0):
    """A brass puja plate: a lamp, flowers, kumkum, and a ring of darbhe (pavitra)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    Y.oval(cr, 0, 0, 170, 40, (0.86, 0.60, 0.20), 6.0)
    Y.oval(cr, 0, -4, 140, 28, (0.96, 0.72, 0.26), 3.0)
    for k, col in enumerate((Y.SAFF, Y.RED, Y.YEL, Y.SAFF, Y.RED)):
        Y.dot(cr, -110 + 26 * k, -10 + 4 * math.sin(k), 13, col, 3.0)
    Y.dot(cr, 70, -10, 16, Y.RED, 3.0)
    cr.new_path()
    cr.save()
    cr.translate(-10, -14)
    cr.scale(1, 0.45)
    cr.arc(0, 0, 44, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgb(*INK)
    cr.set_line_width(14)
    cr.stroke_preserve()
    cr.set_source_rgb(*GRASS)
    cr.set_line_width(8)
    cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()
    Y.lamp(cr, t, x + 120 * s, y - 30 * s, 0.8 * s, 3)


def gust(cr, t, x0, y0, x1, y1, a=1.0, n=4, seed=0):
    """Lines of wind blowing from (x0, y0) toward (x1, y1) (Garuda's wings)."""
    if a <= 0.01:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    for i in range(n):
        u = (t * 1.8 + i / n + seed * 0.21) % 1.0
        off = (i - (n - 1) / 2) * 70
        sx, sy = x0 + ux * L * u * 0.8 + nx * off, y0 + uy * L * u * 0.8 + ny * off
        pts = [(sx, sy), (sx + ux * 120 + nx * 14, sy + uy * 120 + ny * 14), (sx + ux * 220, sy + uy * 220)]
        Y.stroke(cr, pts, 7, WHITE, alpha=a * math.sin(math.pi * u) * 0.85)


# ------------------------------------------------------------------ heaven: a thera painted as svarga

FIELD = (134, 664, 946, 1586)


@functools.lru_cache(maxsize=2)
def heaven_surface():
    """The thera's field painted as svarga (cached): a gold sky, rows of cream clouds, the gods' gateway."""
    import hy_yk_cast as HC
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    x0, y0, x1, y1 = FIELD
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, 0.95, 0.62, 0.20)
    g.add_color_stop_rgb(0.5, 0.99, 0.82, 0.42)
    g.add_color_stop_rgb(1, 0.98, 0.90, 0.66)
    cr.set_source(g)
    cr.paint()
    cx = W / 2                                           # the gateway (a gopura of gold)
    for k, (w, h, y) in enumerate(((330, 90, 1120), (270, 80, 1040), (210, 74, 966), (150, 66, 900))):
        Y.shape(cr, [(cx - w, y), (cx - w + 26, y - h), (cx + w - 26, y - h), (cx + w, y)],
                (0.96, 0.70, 0.22) if k % 2 == 0 else (0.90, 0.56, 0.16), 5.0, smooth=False)
        Y.dot_row(cr, [(cx - w + 30, y - h / 2), (cx + w - 30, y - h / 2)], int(w / 30), 4.0, (1.0, 0.95, 0.75))
    Y.shape(cr, [(cx - 60, 834), (cx, 760), (cx + 60, 834)], (0.98, 0.78, 0.30), 5.0, smooth=False)
    Y.dot(cr, cx, 750, 14, Y.RED, 4.0)
    Y.shape(cr, [(cx - 330, 1120), (cx + 330, 1120), (cx + 330, 1400), (cx - 330, 1400)], (0.86, 0.50, 0.14), 5.0,
            smooth=False)
    cr.new_path()
    cr.move_to(cx - 110, 1400)
    cr.line_to(cx - 110, 1240)
    cr.curve_to(cx - 110, 1160, cx + 110, 1160, cx + 110, 1240)
    cr.line_to(cx + 110, 1400)
    cr.close_path()
    Y.ink_fill(cr, (1.0, 0.94, 0.70), 5.0)
    for (px, py, sc) in ((250, 760, 0.9), (830, 820, 0.8), (210, 1250, 1.1), (870, 1290, 1.05), (520, 1520, 1.6)):
        HC.cloud(cr, px, py, sc, (1.0, 0.97, 0.90))
    rng = np.random.default_rng(5)
    for _ in range(22):
        Y.sparkle(cr, rng.uniform(x0, x1), rng.uniform(y0, y1 - 200), rng.uniform(8, 16), 0.7)
    s.flush()
    return s


def heaven_field(cr):
    cr.set_source_surface(heaven_surface(), 0, 0)
    cr.paint()


def cloud_bank(cr, t, y, a=1.0, drift=0.0, col=(1.0, 0.97, 0.90)):
    """A row of painted clouds across the stage at height y (drifting)."""
    if a <= 0.01:
        return
    import hy_yk_cast as HC
    for k in range(5):
        x = ((k * 260 + drift) % 1300) - 110
        HC.cloud(cr, x, y + 30 * math.sin(k * 1.7), 1.2 + 0.25 * math.sin(k * 2.3), col, a)
