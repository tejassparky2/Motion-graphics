"""Cast, sets and props for the Kannada Yakshagana reel of videos/bhrigu.py (scenes_bhrigu_yk), built on yaksha_kit
(never edited: new looks are dicts made from the kit's looks, new face paints are added to Y.FACES under "bgy_" keys,
extra costume parts are added by drawing a figure with a temporarily extended parts list, as ky_yk_cast does).
Nothing here is shared with the Hindi shadow-puppet reel (scenes_bhrigu).

Cast (one look each, the same all through the reel):
  BHRIGU   the fiery young sage: the kit's SAGE with a black beard and black matted hair, a flame-red cloth with a
           yellow edge, vibhuti and rouge (the other sages are the kit's white-bearded SAGE / SAGE2 / a white-clad one)
  BRAHMA   ky_yk_cast's Brahma: golden face, long white beard, two more faces turned out at the sides, red jacket
  SHIVA    ash-grey face and arms with vibhuti, a slate-blue jacket, a crescent moon on his crown, a green cobra round
           his neck, his trident
  VISHNU   the kit's GOD (blue face, tall gold crown, yellow pitambara) with a flower garland (vanamala); his conch and
           his spinning discus are drawn in his hands when the shot wants them
  PARVATI  a queen in a green saree with a red border and a small gold crown
  LAKSHMI  a queen in a rose saree with a gold border and a small gold crown, a pink lotus in her hand
Extra drawing modes: kneel / sit on the floor (no legs; the kase or the saree rests on the floor), lying down (the
whole figure turned on its side, head to the left), and reach() (arm angles that put a hand on a point).
Sets (three visits = three painted theras a child can tell apart):
  brahma    a saffron-orange thera with a big painted lotus (Brahma's world)
  kailasa   a deep violet night thera with white snow peaks, a crescent moon and stars (Shiva's mountain)
  vaikuntha a sea-teal thera with rows of white milk-ocean waves and a gold discus-sun (Vishnu's home)
Props: Adishesha's coils and five-headed hood, the discus, the conch, an anger flame, little faces (angry / calm),
a scolding burst, a low seat, tears, hearts.
"""
import functools
import math

import cairo

import ky_yk_cast as KY
import sy_yk_cast as SY
import yaksha_kit as Y
from poster import H, W, back, clamp

INK, GOLD, GOLD_HI, GOLD_DK, RED, CRIMSON, MAROON = Y.INK, Y.GOLD, Y.GOLD_HI, Y.GOLD_DK, Y.RED, Y.CRIMSON, Y.MAROON
WHITE, CREAM, YEL, SAFF, GREEN, BLUE, MIRROR = Y.WHITE, Y.CREAM, Y.YEL, Y.SAFF, Y.GREEN, Y.BLUE, Y.MIRROR
shape, stroke, dot, oval, glow, sparkle = Y.shape, Y.stroke, Y.dot, Y.oval, Y.glow, Y.sparkle

# ------------------------------------------------------------------ colours

BEARD = (0.17, 0.13, 0.13)                 # Bhrigu's black beard and hair
FLAME = (0.88, 0.20, 0.05)                 # Bhrigu's cloth
ASH = (0.80, 0.83, 0.88)                   # Shiva's ash-grey skin
SLATE = (0.22, 0.29, 0.45)
VBLUE = (0.22, 0.42, 0.88)                 # Vishnu's blue
SNAKE = (0.20, 0.62, 0.30)
SNAKE_DK = (0.06, 0.34, 0.16)
ROSE = (0.86, 0.12, 0.34)
LOTUS, LOTUS_DK = KY.LOTUS, KY.LOTUS_DK
WOOD = (0.50, 0.26, 0.10)
MILK = (0.99, 0.97, 0.90)
TEAL = (0.02, 0.30, 0.38)
SHESHA = (0.30, 0.58, 0.62)                # the great serpent's coils
SHESHA_DK = (0.12, 0.34, 0.40)
TEAR = (0.75, 0.92, 1.0)

# ------------------------------------------------------------------ face paints (added to the kit's table)

Y.FACES.setdefault("bgy_bhrigu", dict(base=(0.97, 0.72, 0.52), mark="vibhuti", beard=BEARD, brow=BEARD, old=True,
                                      rouge=True))
Y.FACES.setdefault("bgy_shiva", dict(base=ASH, mark="vibhuti", rouge=False, jaw=True, lips=Y.LIPS))
Y.FACES.setdefault("bgy_vishnu", dict(base=VBLUE, mark="namam", rouge=False, jaw=True, lips=Y.LIPS))

# ------------------------------------------------------------------ looks

BHRIGU = dict(Y.SAGE, face="bgy_bhrigu", crown="bgy_jata", cloth=FLAME, cloth2=YEL, skin=(0.96, 0.72, 0.52),
              hand=(0.96, 0.72, 0.52))
SAGE_A = dict(Y.SAGE)
SAGE_B = dict(Y.SAGE2)
SAGE_C = dict(Y.SAGE, cloth=WHITE, cloth2=SAFF)
BRAHMA = KY.BRAHMA
SHIVA = dict(Y.GOD, face="bgy_shiva", hand=ASH, jacket=SLATE, sleeve=ASH, kase=(SAFF, (0.36, 0.20, 0.08), INK, YEL),
             hem=SLATE, hem_zig=WHITE, sash=WHITE, pads=SLATE, disc_cols=(GOLD, SLATE, WHITE), bgy_snake=True,
             bgy_moon=True)
VISHNU = dict(Y.GOD, face="bgy_vishnu", hand=VBLUE, jacket=YEL, sleeve=YEL, kase=(YEL, RED, INK, BLUE), hem=BLUE,
              hem_zig=YEL, sash=WHITE, pads=RED, disc_cols=(GOLD, RED, BLUE), bgy_garland=True)
VISHNU_LYING = dict(VISHNU, disc=False, halo=False)
VISHNU_KNEEL = dict(VISHNU, disc=False)               # bowing low at the sage's feet: no big back-disc
PARVATI = dict(Y.WOMAN, saree=GREEN, border=RED, blouse=(0.98, 0.62, 0.12), skin=(0.98, 0.76, 0.60),
               hand=(0.98, 0.76, 0.60), ky_goddess=True)
LAKSHMI = dict(Y.WOMAN, saree=ROSE, border=GOLD, blouse=GREEN, skin=(0.99, 0.80, 0.64), hand=(0.99, 0.80, 0.64),
               ky_goddess=True)

# ------------------------------------------------------------------ arm poses (upper, forearm, wrist), kit angles

REST = (0.16, 0.30, 0.0)
ANJALI = (0.30, 2.30, 0.0)            # palms joined at the chest
ANJALI_UP = (0.55, 2.75, 0.0)         # joined hands raised in front of the face
CROSS = (0.42, 2.05, 0.6)             # arms folded across the chest (stern)
PALM_OUT = (1.25, -0.75, 0.25)        # an open palm out to the side: stop / no
WAG = (0.95, -1.70, 0.0)              # a forearm up, wagging (scolding)
OPEN_WIDE = (1.30, 0.35, 0.0)         # arms open wide (a hug coming)
CHEST = (0.10, 2.35, 0.2)             # a hand on the chest
BLESS = (0.55, -2.30, 0.0)            # a hand raised, palm out, beside the face
HIGH = (2.65, 0.25, 0.0)              # the arm straight up (holding the trident high)
HIP_HAND = (0.45, 1.35, 0.3)


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    if isinstance(a, str) or a is None:
        return a if u < 0.5 else b
    return a + (b - a) * u


def U(c, p):
    return Y.to_user(c, p)


# ------------------------------------------------------------------ extra parts


def _bj_back(ctx):
    """Bhrigu's long black hair falling behind his shoulders."""
    if ctx.look.get("crown") != "bgy_jata":
        return
    cr = ctx.cr
    cr.translate(0, Y.FACE_C)
    shape(cr, [(-62, -84), (-92, -20), (-100, 70), (-96, 170), (-70, 210), (70, 210), (96, 170), (100, 70),
               (92, -20), (62, -84), (0, -100)], BEARD, 5.0)


def _bj_front(ctx):
    """The black hairline and the tall bun of matted hair wound with rudraksha beads (like the kit's jata)."""
    look = ctx.look
    if look.get("crown") != "bgy_jata":
        return
    cr = ctx.cr
    cr.translate(0, Y.FACE_C)
    line = (0.40, 0.33, 0.30)
    shape(cr, [(-70, -46), (-64, -84), (-30, -100), (0, -104), (30, -100), (64, -84), (70, -46), (52, -62),
               (24, -72), (0, -74), (-24, -72), (-52, -62)], BEARD, 4.5)
    shape(cr, [(-36, -98), (-52, -124), (-58, -160), (-46, -192), (-20, -208), (0, -211), (20, -208), (46, -192),
               (58, -160), (52, -124), (36, -98)], (0.22, 0.17, 0.16), 5.0)
    for k in range(-3, 4):
        stroke(cr, [(k * 10, -104), (k * 15 + 3, -156), (k * 8, -202)], 2.6, line)
    for x, y in Y.along([(-44, -110), (-20, -116), (0, -118), (20, -116), (44, -110)], 8):
        dot(cr, x, y, 6.5, (0.62, 0.22, 0.10), 2.2)
    dot(cr, 0, -214, 7, (0.62, 0.22, 0.10), 2.2)
    for sd in (-1, 1):                                  # ears with rudraksha earrings
        oval(cr, sd * 68, -6, 10, 20, look.get("skin"), 3.0)
        dot(cr, sd * 70, 22, 7, (0.62, 0.22, 0.10), 2.5)
    ctx.mark("crown", 0, -300)


def _moon(ctx):
    """Shiva's crescent moon on the side of his crown."""
    if not ctx.look.get("bgy_moon"):
        return
    cr = ctx.cr
    cr.translate(0, Y.FACE_C)
    SY.crescent(cr, -96, -200, 34)


def _snake(ctx):
    """A green cobra round Shiva's neck, its hood up at his shoulder."""
    if not ctx.look.get("bgy_snake"):
        return
    cr = ctx.cr
    body = [(-96, -318), (-60, -286), (0, -272), (60, -286), (92, -314)]
    Y.inked_line(cr, body, 22, SNAKE, 4.0)
    for x, y in Y.along(body, 9):
        dot(cr, x, y + 1, 3.0, YEL)
    Y.inked_line(cr, [(92, -314), (110, -348), (104, -384)], 20, SNAKE, 4.0)
    shape(cr, [(104, -384), (80, -402), (74, -436), (92, -462), (116, -466), (136, -440), (130, -404)], SNAKE, 4.0)
    shape(cr, [(104, -398), (92, -414), (98, -440), (112, -444), (122, -420), (116, -400)], (0.70, 0.86, 0.50), 2.0)
    dot(cr, 96, -446, 3.5, INK)
    dot(cr, 116, -448, 3.5, INK)


def _garland(ctx):
    """Vishnu's long garland of forest flowers (vanamala) from his shoulders down past his belt."""
    if not ctx.look.get("bgy_garland"):
        return
    cr = ctx.cr
    pts = [(-84, -334), (-92, -230), (-70, -120), (-30, -40), (0, -24), (30, -40), (70, -120), (92, -230),
           (84, -334)]
    stroke(cr, pts, 12, INK)
    for i, (x, y) in enumerate(Y.along(pts, 22)):
        dot(cr, x, y, 11.5, (RED, YEL, (0.99, 0.55, 0.70), WHITE)[i % 4], 3.0)
    dot(cr, 0, -26, 16, (0.10, 0.70, 0.75), 4.0)        # the Kaustubha jewel
    dot(cr, 4, -31, 4, WHITE)


def _kneel_saree(ctx):
    """The saree of a woman sitting on the floor: a wide low mound of cloth with the border along the floor."""
    cr, look = ctx.cr, ctx.look
    pts = [(-84, -8), (-118, 60), (-176, 140), (-214, 196), (-130, 212), (0, 206), (130, 212), (214, 196),
           (176, 140), (118, 60), (84, -8)]
    shape(cr, pts, look.get("saree", GREEN), 6.5)
    for k in range(-3, 4):
        stroke(cr, [(k * 9, 20), (k * 22, 120), (k * 34, 200)], 3.0, INK, alpha=0.5)
    stroke(cr, [(-206, 186), (-130, 200), (0, 194), (130, 200), (206, 186)], 16.0, look.get("border", RED))
    stroke(cr, [(-206, 177), (-130, 191), (0, 185), (130, 191), (206, 177)], 3.0, GOLD)
    stroke(cr, [(-84, -6), (0, -12), (84, -6)], 12.0, GOLD)


def _kneel_kase(ctx):
    """The kase of an actor sitting back on his heels: the puffed skirt pressed lower and wider on the floor."""
    ctx.cr.scale(1.08, 0.72)
    Y.kase(ctx)


LEGS = ("thighL", "thighR", "shinL", "shinR", "footL", "footR")
TORSOS = (Y.torso, KY._belly, Y.sage_torso, Y.woman_torso)


@functools.lru_cache(maxsize=16)
def _parts(kind, mode="stand"):
    out = []
    for part, fn in KY._parts(kind):
        if mode == "kneel" and (part in LEGS or fn is Y.tail):
            continue
        if fn is Y.saree and mode == "kneel":
            out.append(("root", _kneel_saree))
            continue
        if fn is Y.kase and mode == "kneel":
            out.append(("root", _kneel_kase))
            continue
        if fn is Y.crown_back:
            out.append(("head", _bj_back))
        out.append((part, fn))
        if part == "torso" and fn in TORSOS:
            out.append(("torso", _garland))
            out.append(("torso", _snake))
        if fn is Y.crown_front:
            out.append(("head", _bj_front))
            out.append(("head", _moon))
    return out


DROP = {"actor": 214.0, "woman": 200.0, "sage": 330.0}     # waist height above the floor when kneeling / sitting


def hip_h(pose):
    p = dict(Y.POSE)
    p.update(pose or {})
    return max(Y.leg_solve(p["bend"], p["liftL"])[3], Y.leg_solve(p["bend"], p["liftR"])[3])


def figure(cr, look, x, feet, s=1.0, t=0.0, pose=None, flip=False, alpha=1.0, mode="stand", lotus=False):
    """yaksha_kit.figure with this reel's extra parts. mode "kneel": no legs, the kase / saree rests on the floor at
    `feet`. lotus: a pink lotus held up in the (screen) right hand."""
    kind = look.get("kind", "actor")
    old = Y.KINDS[kind]
    Y.KINDS[kind] = _parts(kind, mode)
    try:
        if mode == "kneel":
            feet = feet - DROP[kind] * s + hip_h(pose) * s
        if alpha < 0.999:
            cr.push_group()
        pts = Y.figure(cr, look, x, feet, s, t, pose, flip, 1.0)
        if lotus:
            hx, hy = U(cr, pts["handR" if not flip else "handL"])
            KY.held_lotus(cr, hx, hy - 10 * s, s)
        if alpha < 0.999:
            cr.pop_group_to_source()
            cr.paint_with_alpha(alpha)
        return pts
    finally:
        Y.KINDS[kind] = old


def waist_at(look, x, feet, s, pose, mode="stand"):
    """Where the figure's waist will be (user space) for these arguments."""
    p = dict(Y.POSE)
    p.update(pose or {})
    if mode == "kneel":
        return x + p["shift"] * s, feet - DROP[look.get("kind", "actor")] * s
    return x + p["shift"] * s, feet - hip_h(p) * s


def reach(side, target, waist, s, lean=0.0, elbow=1.0, wrist=0.0, flip=False):
    """Arm angles (upper, forearm, wrist) in the kit's convention that put the hand of the arm on screen side `side`
    (-1 left, +1 right, of the unflipped figure) on `target` (user space); waist = waist_at(...). elbow +1 bends the
    elbow outward (away from the body), -1 inward."""
    fx = -1.0 if flip else 1.0
    tx, ty = (target[0] - waist[0]) / s * fx, (target[1] - waist[1]) / s
    sx0, sy0 = side * Y.SHOULDER[0], Y.SHOULDER[1]
    sx = sx0 * math.cos(lean) - sy0 * math.sin(lean)
    sy = sx0 * math.sin(lean) + sy0 * math.cos(lean)
    L1, L2 = Y.UARM, Y.FARM + 40.0
    vx, vy = tx - sx, ty - sy
    d = clamp(math.hypot(vx, vy), abs(L1 - L2) + 1.0, L1 + L2 - 1.0)
    pv = math.atan2(-vx, vy)
    al = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1.0, 1.0))
    best = None
    for sg in (1, -1):
        p1 = pv + sg * al
        ex, ey = sx - L1 * math.sin(p1), sy + L1 * math.cos(p1)
        score = (ex - sx) * side * elbow
        if best is None or score > best[0]:
            best = (score, p1, ex, ey)
    _, p1, ex, ey = best
    k = math.hypot(vx, vy)
    hx, hy = sx + vx * min(1.0, (L1 + L2 - 1) / max(1e-6, k)), sy + vy * min(1.0, (L1 + L2 - 1) / max(1e-6, k))
    p2 = math.atan2(-(hx - ex), hy - ey)
    if side < 0:
        return (p1 - lean, p1 - p2, wrist)
    return (lean - p1, p2 - p1, wrist)


def lying(c, look, wx, wy, s, t, pose, ang=-math.pi / 2):
    """An actor lying on his back across the stage: the waist at (wx, wy), the head to the left (ang = -pi/2), or
    any angle in between (ang = 0 is standing) for getting up."""
    c.save()
    c.translate(wx, wy)
    c.rotate(ang)
    pts = figure(c, look, 0, hip_h(pose) * s, s, t, pose)
    c.restore()
    return pts


# ------------------------------------------------------------------ sets: three painted theras

Y.CURTAINS.setdefault("bgy_brahma", ((0.74, 0.30, 0.03), YEL, RED, MAROON, (1.0, 0.88, 0.45)))
Y.CURTAINS.setdefault("bgy_kailasa", ((0.17, 0.10, 0.34), (0.86, 0.90, 0.97), BLUE, (0.42, 0.52, 0.74),
                                      (0.90, 0.94, 1.0)))
Y.CURTAINS.setdefault("bgy_vaikuntha", (TEAL, GOLD, RED, SAFF, (1.0, 0.86, 0.40)))
FIELD = (134, 664, 946, 1586)            # the painted field of the thera (inside its border)


def _motif_brahma(cr):
    """A big painted lotus in gold lines, ripples under it."""
    cx, cy = W / 2, 1230
    col = (1.0, 0.86, 0.42)
    cr.set_line_width(7)
    for ring, (n, r0, r1, wd, a) in enumerate(((12, 120, 420, 0.20, 0.30), (10, 100, 330, 0.24, 0.40),
                                               (8, 80, 240, 0.28, 0.55))):
        for i in range(n):
            ang = -math.pi / 2 + (i - (n - 1) / 2) * (math.pi * 1.05 / n)
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(ang + math.pi / 2)
            cr.move_to(0, -r0 * 0.3)
            cr.curve_to(-r1 * wd, -r0 - (r1 - r0) * 0.3, -r1 * wd * 0.6, -r1 * 0.85, 0, -r1)
            cr.curve_to(r1 * wd * 0.6, -r1 * 0.85, r1 * wd, -r0 - (r1 - r0) * 0.3, 0, -r0 * 0.3)
            cr.restore()
            cr.set_source_rgba(*col, a * 0.5)
            cr.fill_preserve()
            cr.set_source_rgba(*col, 0.6)
            cr.stroke()
    cr.set_source_rgba(*col, 0.6)
    cr.arc(cx, cy, 70, math.pi, 2 * math.pi)
    cr.close_path()
    cr.fill()
    for k in range(4):                                   # water ripples under the lotus
        y = cy + 60 + 70 * k
        cr.move_to(FIELD[0], y)
        for i in range(10):
            x0 = FIELD[0] + (FIELD[2] - FIELD[0]) * i / 10
            x1 = FIELD[0] + (FIELD[2] - FIELD[0]) * (i + 1) / 10
            cr.curve_to(x0 + (x1 - x0) * 0.3, y - 18, x0 + (x1 - x0) * 0.7, y + 18, x1, y)
        cr.set_source_rgba(*col, 0.35)
        cr.set_line_width(6)
        cr.stroke()
    for i in range(30):                                  # a ring of little dots high up (light)
        a = math.pi + math.pi * i / 29
        cr.arc(cx + 470 * math.cos(a), cy + 470 * math.sin(a), 5, 0, 2 * math.pi)
        cr.set_source_rgba(*col, 0.6)
        cr.fill()


def _motif_kailasa(cr):
    """White snow peaks against a violet night, a crescent moon and stars."""
    rng = [(190, 760), (300, 700), (420, 880), (640, 720), (760, 820), (880, 690), (240, 940), (900, 960),
           (560, 690), (330, 1010), (820, 1080), (180, 1120)]
    for k, (x, y) in enumerate(rng):
        sparkle(cr, x, y, 14 + 6 * (k % 3), 0.85)
    SY.crescent(cr, 265, 790, 58, 0.95)
    ice = (0.88, 0.92, 0.98)
    shade = (0.60, 0.68, 0.84)
    for (px, py, w, h) in ((300, 1080, 360, 1.0), (790, 1060, 380, 1.0), (545, 930, 460, 1.0)):
        base = FIELD[3] + 10
        pts = [(px - w, base), (px - w * 0.55, py + (base - py) * 0.45), (px - w * 0.22, py + 60), (px, py),
               (px + w * 0.25, py + 70), (px + w * 0.6, py + (base - py) * 0.5), (px + w, base)]
        cr.new_path()
        cr.move_to(*pts[0])
        for q in pts[1:]:
            cr.line_to(*q)
        cr.close_path()
        cr.set_source_rgb(*shade)
        cr.fill_preserve()
        cr.set_source_rgb(*INK)
        cr.set_line_width(6)
        cr.stroke()
        cap = [(px - w * 0.36, py + 150), (px - w * 0.22, py + 60), (px, py), (px + w * 0.25, py + 70),
               (px + w * 0.40, py + 160), (px + w * 0.22, py + 130), (px + w * 0.08, py + 175),
               (px - w * 0.08, py + 120),
               (px - w * 0.22, py + 170)]
        cr.new_path()
        cr.move_to(*cap[0])
        for q in cap[1:]:
            cr.line_to(*q)
        cr.close_path()
        cr.set_source_rgb(*ice)
        cr.fill_preserve()
        cr.set_source_rgb(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.move_to(px, py + 10)
        cr.line_to(px + w * 0.18, base - 40)
        cr.set_source_rgba(*INK, 0.35)
        cr.set_line_width(4)
        cr.stroke()


def _motif_vaikuntha(cr):
    """Rows of white milk-ocean waves along the bottom and a gold discus-sun painted high in the middle."""
    cx, cy = W / 2, 1000
    col = (1.0, 0.86, 0.40)
    cr.set_line_width(7)
    for r in (300, 270):
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.set_source_rgba(*col, 0.5)
        cr.stroke()
    for i in range(24):                                  # the discus teeth
        a = 2 * math.pi * i / 24
        cr.move_to(cx + 300 * math.cos(a - 0.08), cy + 300 * math.sin(a - 0.08))
        cr.line_to(cx + 380 * math.cos(a), cy + 380 * math.sin(a))
        cr.line_to(cx + 300 * math.cos(a + 0.08), cy + 300 * math.sin(a + 0.08))
        cr.close_path()
    cr.set_source_rgba(*col, 0.35)
    cr.fill()
    for i in range(12):
        a = 2 * math.pi * i / 12
        cr.move_to(cx + 60 * math.cos(a), cy + 60 * math.sin(a))
        cr.line_to(cx + 260 * math.cos(a), cy + 260 * math.sin(a))
    cr.set_source_rgba(*col, 0.4)
    cr.stroke()
    cr.arc(cx, cy, 60, 0, 2 * math.pi)
    cr.set_source_rgba(*col, 0.5)
    cr.fill()
    for k in range(5):                                   # the milk ocean: rows of white waves
        y = 1300 + 62 * k
        wl = 118
        off = (k % 2) * wl / 2
        cr.new_path()
        x = FIELD[0] - wl + off
        cr.move_to(x, y + 40)
        while x < FIELD[2] + wl:
            cr.curve_to(x + wl * 0.25, y - 26, x + wl * 0.75, y - 26, x + wl, y)
            x += wl
        cr.line_to(FIELD[2] + wl, FIELD[3] + 20)
        cr.line_to(FIELD[0] - wl, FIELD[3] + 20)
        cr.close_path()
        cr.set_source_rgba(*MILK, 0.55 + 0.1 * k)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, 0.7)
        cr.set_line_width(4)
        cr.stroke()


MOTIFS = {"bgy_brahma": _motif_brahma, "bgy_kailasa": _motif_kailasa, "bgy_vaikuntha": _motif_vaikuntha}


@functools.lru_cache(maxsize=4)
def stage_surface(style):
    """The whole set for one of the three visits (cached): the kit's night, floor, thera (in this reel's colours)
    and posts, with this reel's motif painted on the thera."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    Y._night(cr)
    Y._floor(cr)
    Y._curtain(cr, style, "none")
    cr.save()
    cr.rectangle(FIELD[0], FIELD[1], FIELD[2] - FIELD[0], FIELD[3] - FIELD[1])
    cr.clip()
    MOTIFS[style](cr)
    cr.restore()
    Y._post(cr, 22, 0, Y.FLOOR_Y + 40, -1)
    Y._post(cr, W - 22, 0, Y.FLOOR_Y + 40, 1)
    s.flush()
    return s


def stage(cr, t, style, garland=True):
    if style in MOTIFS:
        cr.set_source_surface(stage_surface(style), 0, 0)
        cr.paint()
        if garland:
            Y.thorana(cr, t)
    else:
        Y.stage(cr, t, style[0], style[1], True, garland)


def backlight(cr, t, a=1.0):
    """The thera lit from behind (the kick is played as a shadow): a hot gold glow over the backdrop."""
    if a <= 0.01:
        return
    cr.save()
    cr.rectangle(Y.CURT[0], Y.CURT[1] - 30, Y.CURT[2] - Y.CURT[0], Y.FLOOR_Y - Y.CURT[1] + 60)
    cr.clip()
    g = cairo.RadialGradient(W / 2, 1250, 60, W / 2, 1250, 900)
    g.add_color_stop_rgba(0, 1.0, 0.97, 0.82, 0.97 * a)
    g.add_color_stop_rgba(0.45, 1.0, 0.82, 0.45, 0.92 * a)
    g.add_color_stop_rgba(1, 0.95, 0.55, 0.20, 0.85 * a)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def silhouette(cr, surf, a=1.0, col=(0.07, 0.03, 0.05)):
    """Paint a layer's shapes as one dark shadow (a shadow-play moment on the lit thera)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_source_rgba(*col, a)
    cr.mask_surface(surf, 0, 0)
    cr.restore()


# ------------------------------------------------------------------ props


def chakra(cr, t, x, y, r, a=1.0, spin=1.0, glow_a=0.6):
    """Vishnu's discus, spinning: a gold wheel with flame teeth, red ring, spokes and a hub."""
    if a <= 0.01:
        return
    if glow_a > 0:
        glow(cr, x, y, r * 2.6, glow_a * a, (1.0, 0.80, 0.35))
    cr.save()
    cr.translate(x, y)
    cr.rotate(t * 4.0 * spin)
    cr.push_group()
    n = 14
    for i in range(n):
        ang = 2 * math.pi * i / n
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(r * 0.80 * math.cos(ang - 0.18), r * 0.80 * math.sin(ang - 0.18)),
               (r * 1.28 * ca - r * 0.2 * sa, r * 1.28 * sa + r * 0.2 * ca),
               (r * 0.80 * math.cos(ang + 0.2), r * 0.80 * math.sin(ang + 0.2))]
        shape(cr, pts, SAFF, 3.0)
    dot(cr, 0, 0, r, GOLD, 4.0)
    dot(cr, 0, 0, r * 0.78, RED, 3.0)
    dot(cr, 0, 0, r * 0.62, GOLD, 3.0)
    for i in range(8):
        ang = 2 * math.pi * i / 8
        stroke(cr, [(r * 0.18 * math.cos(ang), r * 0.18 * math.sin(ang)),
                    (r * 0.6 * math.cos(ang), r * 0.6 * math.sin(ang))], max(3.0, r * 0.08), RED)
    dot(cr, 0, 0, r * 0.2, GOLD_HI, 3.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def conch(cr, x, y, s=1.0, rot=0.0, a=1.0):
    """Vishnu's white conch (shankha) with a gold cap, its spiral end up."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(0, -70), (22, -58), (34, -26), (36, 14), (24, 52), (8, 74), (-8, 74), (-24, 52), (-36, 14),
               (-34, -26), (-22, -58)], MILK, 5.0)
    for k in range(4):
        stroke(cr, [(-30 + 4 * k, -30 + 22 * k), (0, -38 + 22 * k), (30 - 4 * k, -30 + 22 * k)], 3.0, INK, alpha=0.6)
    shape(cr, [(-14, -70), (0, -96), (14, -70)], MILK, 4.0, smooth=False)
    stroke(cr, [(-26, 46), (0, 54), (26, 46)], 8.0, GOLD)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def anger(cr, t, x, y, s=1.0, a=1.0):
    """A ball of anger: a flickering red-orange flame (what comes over an angry face in a cartoon)."""
    if a <= 0.01 or abs(s) < 1e-3:                   # a flame growing in from scale 0 is simply not drawn yet
        return
    glow(cr, x, y, 150 * s, 0.6 * a, (1.0, 0.35, 0.10))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    f = math.sin(t * 13)
    for k, (col, sc) in enumerate(((RED, 1.0), (SAFF, 0.72), (YEL, 0.44))):
        pts = [(0, 60), (-52, 30), (-58, -10), (-36, -54), (-28, -20), (-14, -96 - 8 * f), (8, -40), (24, -82 + 6 * f),
               (46, -30), (56, 10), (50, 34)]
        cr.save()
        cr.translate(0, 20 * (1 - sc))
        cr.scale(sc, sc)
        shape(cr, pts, col, 4.0 if k == 0 else 0)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


FACE_ICON = dict(kind="actor", face="hero", crown="none", head_s=1.0)


def face_icon(cr, t, x, y, r, mood, a=1.0, face="hero", ring_col=CREAM):
    """A little painted face in a round frame (angry / calm), for the rule card."""
    if a <= 0.01:
        return
    cr.save()
    cr.push_group()
    dot(cr, x, y, r, ring_col, 6.0)
    cr.translate(x, y + r * 0.08)
    k = r / 120.0
    cr.scale(k, k)
    look = dict(FACE_ICON, face=face)
    p = dict(Y.POSE, mood=mood)
    Y.head_paint(Y.Ctx(cr, look, p, t))
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def burst(cr, t, t0, x, y, w, h, tail_to=None, a=1.0, field=(0.95, 0.18, 0.10)):
    """A jagged red shouting burst with zig-zag scribbles in it (scolding, no words) popping in at t0."""
    q = clamp((t - t0) / 0.25)
    if q <= 0 or a <= 0.01:
        return
    k = 0.5 + 0.5 * back(q, 2.0)
    jit = 6 * math.sin(t * 30)
    cr.save()
    cr.push_group()
    if tail_to:
        stroke(cr, [(x - w * 0.2, y + h * 0.3), tail_to], 18, INK)
        stroke(cr, [(x - w * 0.2, y + h * 0.3), tail_to], 9, field)
    cr.translate(x, y)
    cr.scale(k, k)
    n = 18
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        rr = 1.0 if i % 2 == 0 else 0.72
        pts.append((w / 2 * rr * math.cos(ang) + (jit if i % 3 == 0 else 0), h / 2 * rr * math.sin(ang)))
    shape(cr, pts, field, 6.0, smooth=False)
    shape(cr, [(px * 0.78, py * 0.78) for px, py in pts], YEL, 0, smooth=False)
    for row in range(2):                                 # zig-zag scribbles
        zz = []
        for i in range(9):
            zz.append((-w * 0.30 + w * 0.6 * i / 8, (-h * 0.10 + h * 0.2 * row) + (14 if i % 2 else -14)))
        stroke(cr, zz, 9, INK, smooth=False)
    Y.kn_text(cr, "!", w * 0.36, -h * 0.05, 90, RED, INK, 6)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a * clamp(q * 3))
    cr.restore()


def high_seat(cr, x, top, floor, s=1.0):
    """A tall wooden seat (peetha) with gold trim and a red cushion, its top at `top`, its legs on the floor."""
    w = 170 * s
    for sd in (-1, 1):
        shape(cr, [(x + sd * w - 18 * s, top), (x + sd * w + 18 * s, top), (x + sd * w + 14 * s, floor),
                   (x + sd * w - 14 * s, floor)], WOOD, 5.0, smooth=False)
    shape(cr, [(x - w - 20 * s, top + 20 * s), (x + w + 20 * s, top + 20 * s), (x + w + 10 * s, top + 120 * s),
               (x - w - 10 * s, top + 120 * s)], WOOD, 6.0, smooth=False)
    stroke(cr, [(x - w, top + 60 * s), (x + w, top + 60 * s)], 10 * s, GOLD, smooth=False)
    Y.dot_row(cr, [(x - w + 10 * s, top + 92 * s), (x + w - 10 * s, top + 92 * s)], 11, 4.0 * s, GOLD_HI)
    shape(cr, [(x - w - 34 * s, top + 22 * s), (x - w - 14 * s, top - 14 * s), (x + w + 14 * s, top - 14 * s),
               (x + w + 34 * s, top + 22 * s)], RED, 5.0)


def footstool(cr, x, top, floor, w):
    """A low footstool with a red top (the sage's feet rest on it)."""
    shape(cr, [(x - w / 2, top + 14), (x + w / 2, top + 14), (x + w / 2 - 12, floor), (x - w / 2 + 12, floor)], WOOD,
          5.0, smooth=False)
    stroke(cr, [(x - w / 2 + 10, top + 50), (x + w / 2 - 10, top + 50)], 8, GOLD, smooth=False)
    shape(cr, [(x - w / 2 - 10, top + 16), (x - w / 2 + 6, top - 4), (x + w / 2 - 6, top - 4),
               (x + w / 2 + 10, top + 16)], RED, 4.0)


def seat(cr, x, floor, s=1.0):
    """A low wooden seat (peetha) with gold trim and a red cushion; its top at floor - 170 * s."""
    cr.save()
    cr.translate(x, floor)
    cr.scale(s, s)
    for sd in (-1, 1):
        shape(cr, [(sd * 150 - 18, -40), (sd * 150 + 18, -40), (sd * 150 + 14, 0), (sd * 150 - 14, 0)], WOOD, 5.0,
              smooth=False)
    shape(cr, [(-190, -150), (190, -150), (180, -40), (-180, -40)], WOOD, 6.0, smooth=False)
    stroke(cr, [(-180, -110), (180, -110)], 10, GOLD, smooth=False)
    Y.dot_row(cr, [(-170, -76), (170, -76)], 11, 4.0, GOLD_HI)
    shape(cr, [(-200, -150), (-180, -184), (180, -184), (200, -150)], RED, 5.0)
    cr.restore()


def tear(cr, x, y, s, a):
    SY.tear(cr, x, y, s, a)


def heart(cr, x, y, s, a=1.0, col=(0.98, 0.35, 0.50)):
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    cr.move_to(0, 22)
    cr.curve_to(-40, -6, -30, -40, 0, -22)
    cr.curve_to(30, -40, 40, -6, 0, 22)
    cr.close_path()
    cr.set_source_rgba(*col, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(4)
    cr.stroke()
    cr.restore()


def shesha(cr, t, x0, x1, y, s=1.0, hood=None):
    """Adishesha: the great serpent's coils as a long couch from x0 to x1 (top at y), and, if hood = (hx, hy, k), his
    five hooded heads fanned out above that point."""
    if hood:
        hx, hy, k = hood
        cr.save()
        cr.translate(hx, hy)
        cr.scale(k, k)
        Y.inked_line(cr, [(0, 330), (10, 200), (0, 60)], 70, SHESHA, 5.0)
        for i in range(5):
            ang = (i - 2) * 0.42
            cr.save()
            cr.rotate(ang)
            cr.translate(0, -120)
            shape(cr, [(0, 150), (-46, 100), (-64, 30), (-52, -30), (-24, -58), (0, -64), (24, -58), (52, -30),
                       (64, 30), (46, 100)], SHESHA, 5.0)
            shape(cr, [(0, 120), (-26, 80), (-32, 30), (-20, -10), (0, -18), (20, -10), (32, 30), (26, 80)],
                  (0.86, 0.90, 0.60), 3.0)
            for sd in (-1, 1):
                oval(cr, sd * 12, 30, 7, 9, INK, 0)
                dot(cr, sd * 12 + 2, 27, 2.2, WHITE)
            stroke(cr, [(0, -10), (0, 6)], 3, INK)
            cr.restore()
        cr.restore()
    cr.save()
    hgt = 120 * s
    cr.new_path()
    cr.move_to(x0, y + hgt * 0.5)
    cr.curve_to(x0, y - 10, x0 + 60, y, x0 + 120, y)
    cr.line_to(x1 - 80, y)
    cr.curve_to(x1 + 10, y, x1 + 30, y + hgt, x1 - 60, y + hgt)
    cr.line_to(x0 + 60, y + hgt)
    cr.curve_to(x0 + 10, y + hgt, x0, y + hgt * 0.8, x0, y + hgt * 0.5)
    cr.close_path()
    path = cr.copy_path()
    cr.set_source_rgb(*SHESHA)
    cr.fill_preserve()
    cr.save()
    cr.clip()
    for row in range(3):                                 # the coils, one above the other
        yy = y + hgt * (row + 0.5) / 3
        stroke(cr, [(x0, yy + hgt / 6), (x1, yy + hgt / 6)], 4.0, SHESHA_DK, smooth=False, alpha=0.8)
        for i in range(int((x1 - x0) / 46)):
            xx = x0 + 23 + 46 * i + (23 if row % 2 else 0)
            cr.new_path()
            cr.arc(xx, yy, 14 * s, math.pi * 0.1, math.pi * 0.9)
            cr.set_source_rgba(*SHESHA_DK, 0.7)
            cr.set_line_width(3.0)
            cr.stroke()
    stroke(cr, [(x0, y + 10), (x1, y + 10)], 10.0, (0.86, 0.90, 0.60), smooth=False, alpha=0.9)
    cr.restore()
    cr.new_path()
    cr.append_path(path)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    # the tail curling out at the right end
    Y.inked_line(cr, [(x1 - 40, y + hgt * 0.8), (x1 + 30, y + hgt * 0.55), (x1 + 34, y + hgt * 0.2),
                      (x1 + 10, y + hgt * 0.05)], 22 * s, SHESHA, 4.0)
    cr.restore()


def red_ring(cr, x, y, rx, ry, p, w=10.0, a=1.0):
    KY.red_ring(cr, x, y, rx, ry, p, w, a)


def flash(cr, t, t0, x, y, r=260, a=1.0):
    """A soft white-gold flash at (x, y) from t0 (a touch of light, not a blow): a bloom and one expanding ring."""
    u = (t - t0) / 0.7
    if u <= 0 or u >= 1 or a <= 0.01:
        return
    k = math.exp(-3.0 * u)
    glow(cr, x, y, r * (0.6 + 0.8 * u), 0.9 * k * a, (1.0, 0.95, 0.80))
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.new_path()
    cr.arc(x, y, r * (0.2 + 0.9 * u), 0, 2 * math.pi)
    cr.set_source_rgba(1.0, 0.92, 0.70, 0.6 * (1 - u) * a)
    cr.set_line_width(12 * (1 - u) + 2)
    cr.stroke()
    cr.restore()
    sparkle(cr, x, y, 60 * (1 - u) + 20, k * a)


def footprint(cr, x, y, s=1.0, rot=0.0, a=1.0):
    """A small glowing gold footprint (where the sage's foot touched Vishnu's chest)."""
    if a <= 0.01:
        return
    glow(cr, x, y, 120 * s, 0.7 * a, (1.0, 0.85, 0.45))
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(0, 46), (-20, 36), (-26, 6), (-22, -26), (-12, -44), (6, -46), (20, -34), (22, -4), (16, 24),
               (12, 42)], GOLD_HI, 3.5)
    for k, (dx, dy, r) in enumerate(((-16, -60, 7.5), (-3, -66, 7), (9, -63, 6.5), (19, -55, 6), (26, -44, 5))):
        dot(cr, dx, dy, r, GOLD_HI, 3.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def cushion(cr, x, y, s=1.0):
    """A small round red cushion with gold tassels, its top at y (a raised foot rests on it)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for sd in (-1, 1):
        dot(cr, sd * 70, 34, 9, GOLD, 3.0)
    oval(cr, 0, 34, 74, 36, RED, 5.0)
    stroke(cr, [(-66, 36), (0, 44), (66, 36)], 6.0, GOLD)
    cr.restore()


def kick_leg(cr, hip, foot, s=1.0, col=(0.07, 0.03, 0.05)):
    """A leg (thigh, shin, foot) from the hip to the foot point, bent a little at the knee: drawn flat and dark, only
    for the shadow moment of the kick."""
    L1, L2 = 190 * s, 190 * s
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    d = max(1.0, math.hypot(dx, dy))
    k = min(1.0, (L1 + L2 - 4) / d)
    fx, fy = hip[0] + dx * k, hip[1] + dy * k
    d = math.hypot(fx - hip[0], fy - hip[1])
    h = math.sqrt(max(0.0, L1 * L1 - (d / 2) ** 2))
    nx, ny = -(fy - hip[1]) / d, (fx - hip[0]) / d
    if ny > 0:
        nx, ny = -nx, -ny
    knee = ((hip[0] + fx) / 2 + nx * h, (hip[1] + fy) / 2 + ny * h)
    stroke(cr, [hip, knee], 64 * s, col, smooth=False)
    stroke(cr, [knee, (fx, fy)], 46 * s, col, smooth=False)
    ang = math.atan2(fy - knee[1], fx - knee[0])
    cr.save()
    cr.translate(fx, fy)
    cr.rotate(ang)
    oval(cr, 18 * s, 0, 44 * s, 20 * s, col, 0)
    cr.restore()
    return fx, fy


def namaste_icon(cr, x, y, r, a=1.0):
    """Two hands joined in namaskara, in a cream circle."""
    if a <= 0.01:
        return
    cr.save()
    cr.push_group()
    dot(cr, x, y, r, CREAM, 6.0)
    for sd in (-1, 1):
        cr.save()
        cr.translate(x + sd * r * 0.14, y + r * 0.62)
        cr.rotate(math.pi + sd * 0.12)
        cr.scale(r / 95.0, r / 95.0)
        Y._hand(cr, "open", sd, SAGE_SKIN_ICON, 0.0)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


SAGE_SKIN_ICON = (0.96, 0.72, 0.52)


def talk_icon(cr, x, y, r, a=1.0):
    """A speech bubble with three dots (talking), in a cream circle."""
    if a <= 0.01:
        return
    cr.save()
    cr.push_group()
    dot(cr, x, y, r, CREAM, 6.0)
    shape(cr, [(x - r * 0.62, y - r * 0.40), (x + r * 0.62, y - r * 0.40), (x + r * 0.62, y + r * 0.26),
               (x - r * 0.10, y + r * 0.26), (x - r * 0.40, y + r * 0.58), (x - r * 0.36, y + r * 0.26),
               (x - r * 0.62, y + r * 0.26)], WHITE, 5.0, smooth=False)
    for k in (-1, 0, 1):
        dot(cr, x + k * r * 0.32, y - r * 0.07, r * 0.09, INK)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def crown_icon(cr, x, y, s=1.0, a=1.0):
    """A small gold crown (the greatest)."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(-60, 30), (-66, -30), (-34, 0), (0, -46), (34, 0), (66, -30), (60, 30)], GOLD, 5.0, smooth=False)
    stroke(cr, [(-60, 30), (60, 30)], 12, RED, smooth=False)
    for xx, yy in ((-66, -34), (0, -52), (66, -34)):
        dot(cr, xx, yy, 9, RED, 3.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def anger_face(cr, t, x, y, r, a=1.0, ring_col=CREAM):
    """A red angry face (for 'he got angry')."""
    face_icon(cr, t, x, y, r, "angry", a, face="bgy_red", ring_col=ring_col)


def calm_face(cr, t, x, y, r, a=1.0, ring_col=CREAM):
    """A calm, smiling face (for 'no anger')."""
    face_icon(cr, t, x, y, r, "joy", a, face="hero", ring_col=ring_col)


Y.FACES.setdefault("bgy_red", dict(base=(0.95, 0.30, 0.20), mark="namam", rouge=False, jaw=False, stache=True))
