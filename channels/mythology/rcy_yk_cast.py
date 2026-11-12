"""Cast and props for the Kannada Yakshagana reel of video 21, ranchhod (scenes_ranchhod_yk): looks built from
yaksha_kit's ready looks (the kit file is never edited), new face paints, moods and figure kinds registered under
"rcy_" names, and the props this story needs, all in the kit's flat paint with thick black outlines:

  KRISHNA      the kit's GOD made Krishna: a blue painted face, a small gold kireeta with a PEACOCK FEATHER rising
               behind it, a small round back-piece, yellow silk (pitambara) jacket and sash, a yellow-and-blue check
               kase; unarmed all through (at most his flute)
  KALAYAVANA   the cruel king in the banna style: the huge flaming round crown, a near-black face with red cheek
               patterns and rows of white dots (chukki), red eyes and a heavy moustache (no tusks: he is a king, not a
               rakshasa), black and crimson costume, a mace he throws away
  MUCHUKUNDA   the old king asleep: the kit's KING with a white beard and bushy white brows, purple and gold; he
               lies on a stone bed in the cave (drawn rotated, in the scenes) and can rise and glare
  the gods     three crowned actors with halos (rc10)

  rig()        yaksha_kit.figure with one more freedom: a leg can be set by its own thigh / shin angles (the kick)

Props: sword / bow icons (crossed out = no weapon), the flute, Krishna's town (a fort gate whose doors open), rows of
marching soldiers, flying arrows, the hill thera of the chase, a rock cave mouth (a dark inside the actors vanish
into, and its rock rim drawn over them), the cave thera inside (rock walls, a hole in the roof where the sun and the
moon race past), the stone bed, creepers and cobwebs growing over the sleeper (years), a painted eye opening with
rays, eye beams, a white flash, a heap of ash with grey flakes drifting up (never a burning body), an impact star,
footprints and the route map of the chase, a lamp of buddhi, dust.
"""
import functools
import math

import cairo
import numpy as np

import yaksha_kit as Y
from poster import H, W, clamp, ease
from puppet_core import spath

INK, GOLD, GOLD_HI, GOLD_DK, RED, CRIMSON, MAROON = Y.INK, Y.GOLD, Y.GOLD_HI, Y.GOLD_DK, Y.RED, Y.CRIMSON, Y.MAROON
WHITE, CREAM, YEL, SAFF, GREEN, BLUE, MIRROR = Y.WHITE, Y.CREAM, Y.YEL, Y.SAFF, Y.GREEN, Y.BLUE, Y.MIRROR
shape, stroke, dot, oval, glow, sparkle = Y.shape, Y.stroke, Y.dot, Y.oval, Y.glow, Y.sparkle

KR_BLUE = (0.27, 0.47, 0.88)
KR_HAND = (0.31, 0.51, 0.90)
PURPLE = (0.42, 0.13, 0.50)
ROCK = (0.40, 0.33, 0.28)
ROCK_HI = (0.58, 0.49, 0.40)
ROCK_DK = (0.20, 0.15, 0.13)
ASH = (0.62, 0.61, 0.60)
ASH_DK = (0.38, 0.37, 0.37)
STEEL = (0.84, 0.88, 0.92)
SAND = (0.86, 0.66, 0.40)
SAND_DK = (0.62, 0.42, 0.22)
PEA_GREEN = (0.10, 0.55, 0.42)
PEA_BLUE = (0.06, 0.20, 0.62)
PEA_TEAL = (0.12, 0.62, 0.70)

# ------------------------------------------------------------------ faces and moods (registered under rcy_ names)

Y.FACES.setdefault("rcy_krishna", dict(Y.FACES["god"], base=KR_BLUE))
Y.FACES.setdefault("rcy_banna", dict(Y.FACES["demon"], base=(0.11, 0.09, 0.12), tusks=False))
Y.FACES.setdefault("rcy_old", dict(Y.FACES["king"], base=(0.97, 0.70, 0.47), beard=(0.97, 0.96, 0.93),
                                   brow=(0.97, 0.96, 0.93), old=True))
Y.MOODS.setdefault("rcy_sleep", dict(bi=-2, bo=3, lift=0, eh=15, mouth="smile", pupil=0.44))


# ------------------------------------------------------------------ extra parts


def feather(cr, x, y, s=1.0, rot=0.0, sway=0.0):
    """A peacock feather standing on (x, y) (the quill end), leaning by rot: a quill, green barbs, the eye."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot + sway)
    cr.scale(s, s)
    stroke(cr, [(0, 0), (2, -120), (0, -250)], 9.0, INK)
    stroke(cr, [(0, 0), (2, -120), (0, -250)], 4.5, (0.86, 0.80, 0.55))
    for k in range(16):                                  # the fine green barbs along the quill
        yy = -60 - 12 * k
        for sd in (-1, 1):
            stroke(cr, [(1, yy), (sd * (16 + 2.2 * k), yy - 26)], 3.4, PEA_GREEN)
    eye = [(0, -196), (-46, -232), (-60, -292), (-44, -346), (0, -372), (44, -346), (60, -292), (46, -232)]
    shape(cr, eye, (0.20, 0.62, 0.30), 5.0)
    shape(cr, [(0, -222), (-36, -250), (-44, -296), (-30, -334), (0, -348), (30, -334), (44, -296), (36, -250)],
          GOLD, 3.5)
    shape(cr, [(0, -244), (-26, -264), (-30, -298), (-20, -324), (0, -332), (20, -324), (30, -298), (26, -264)],
          PEA_TEAL, 3.0)
    oval(cr, 0, -292, 16, 22, PEA_BLUE, 3.0)
    dot(cr, -4, -298, 4.0, (0.55, 0.80, 1.0))
    cr.restore()


def _crown_feather(ctx):
    cr, t = ctx.cr, ctx.t
    cr.translate(0, Y.FACE_C)
    feather(cr, 18, -150, 0.92, 0.30, 0.04 * math.sin(t * 1.8))


def _banna_paint(ctx):
    """The banna face paint over the kit's face: red cheek wings edged with white dot rows, a red chin mark."""
    cr, p = ctx.cr, ctx.p
    turn = p["turn"]

    def X(x):
        return x + turn * 15.0 * (1 - min(1.0, (x / 72.0) ** 2))
    cr.translate(turn * 4, Y.FACE_C)
    for sd in (-1, 1):
        pts = [(sd * 22, 12), (sd * 58, -4), (sd * 64, 34), (sd * 36, 54)]
        shape(cr, [(X(x), y) for x, y in pts], RED, 3.0)
        Y.dot_row(cr, [(X(sd * 26), 16), (X(sd * 56), 2), (X(sd * 60), 32)], 5, 2.6, WHITE)
        stroke(cr, [(X(sd * 64), -38), (X(sd * 52), -60), (X(sd * 30), -66)], 4.0, WHITE)
    shape(cr, [(X(-12), 70), (X(0), 62), (X(12), 70), (X(0), 86)], RED, 2.5)


def _parts_with(base, after, extra):
    i = base.index(after) + 1
    return base[:i] + [extra] + base[i:]


Y.KINDS.setdefault("rcy_krishna", _parts_with(Y._actor_parts(), ("head", Y.crown_back), ("head", _crown_feather)))
Y.KINDS.setdefault("rcy_banna", _parts_with(Y._actor_parts(), ("head", Y.head), ("head", _banna_paint)))

# ------------------------------------------------------------------ looks

KRISHNA = dict(Y.GOD, kind="rcy_krishna", face="rcy_krishna", crown="kireeta_small", disc=True, disc_r=128.0,
               halo=True, jacket=YEL, sleeve=YEL, hand=KR_HAND, kase=(YEL, BLUE, INK, RED), hem=BLUE, hem_zig=YEL,
               sash=(1.0, 0.86, 0.25), pads=RED, disc_cols=(GOLD, BLUE, GREEN))
KALA = dict(Y.DEMON, kind="rcy_banna", face="rcy_banna", jacket=(0.12, 0.08, 0.09), sleeve=(0.56, 0.03, 0.07),
            hand=(0.24, 0.19, 0.22), kase=(RED, Y.BLACK, YEL, GREEN), hem=Y.BLACK, hem_zig=RED, sash=RED,
            pads=Y.BLACK)
MUCHU = dict(Y.KING, face="rcy_old", jacket=PURPLE, sleeve=PURPLE, kase=(GOLD, PURPLE, INK, GREEN), hem=PURPLE,
             hem_zig=GOLD, sash=GOLD_HI, pads=PURPLE, disc_cols=(GOLD, PURPLE, GREEN))
GODS = (dict(Y.KING, halo=True, jacket=BLUE, sleeve=BLUE, kase=(YEL, BLUE, INK, RED), hem=BLUE,
             disc_cols=(GOLD, BLUE, RED)),
        dict(Y.KING, halo=True, face="hero", jacket=SAFF, sleeve=SAFF, kase=(YEL, SAFF, INK, GREEN), hem=GREEN,
             disc_cols=(GOLD, SAFF, GREEN)),
        dict(Y.KING, halo=True, face="hero", jacket=GREEN, sleeve=GREEN, kase=(YEL, GREEN, INK, RED), hem=RED,
             disc_cols=(GOLD, GREEN, RED)))

# arm poses (upper angle, elbow bend, wrist)
REST = (0.16, 0.30, 0.0)
OPEN_OUT = (0.95, 0.35, 0.0)          # arm out to the side, palm open: "see, nothing in my hands"
FIST_UP = (2.75, 0.15, 0.0)
CLAW = (1.25, 0.55, 0.0)              # reaching forward-out to grab
AKIMBO = (0.45, 1.35, 0.3)
PALM_UP = (0.70, -2.44, 0.0)          # a raised open palm beside the face (blessing / stop)
FLUTE_L = (0.62, 2.30, 0.0)           # both forearms up to the mouth (the flute)
FLUTE_R = (0.95, 2.25, 0.0)


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def pose(t, amp=1.0, freq=0.5, ph=0.0, **kw):
    """A pose with the Yakshagana idle sway mixed in (lean / head / shift in kw are added to the sway)."""
    sh, ln, hd = Y.sway(t, amp, freq, ph)
    p = dict(shift=sh + kw.pop("shift", 0.0), lean=ln + kw.pop("lean", 0.0), head=hd * 0.6 + kw.pop("head", 0.0),
             sash=-ln * 3 + kw.pop("sash", 0.0), breathe=math.sin(t * 2.2 + ph), bend=0.3)
    p.update(kw)
    return p


def U(c, p):
    """Device point -> the context's user space."""
    return Y.to_user(c, p)


def spin(t, t0, dur=0.8):
    """0..1 through one full turn from t0, eased in and out (smooth, no jumps)."""
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return 0.0
    return 0.5 - 0.5 * math.cos(math.pi * u)


def run(t, t0, t1, x0, x1, period=0.36, amp=0.85):
    """Running across the stage from x0 to x1 between t0 and t1 (knees high, Yakshagana style):
    (x, liftL, liftR, bob 0..1, stamp 0..1 just after each foot lands)."""
    u = clamp((t - t0) / max(0.01, t1 - t0))
    x = x0 + (x1 - x0) * u
    if t <= t0 or t >= t1:
        return x, 0.0, 0.0, 0.0, 0.0
    ph = (t - t0) / period
    f = ph % 1.0
    lift = amp * math.sin(math.pi * clamp(f / 0.7)) if f < 0.7 else 0.0
    side = int(ph) % 2
    stamp = math.exp(-14 * (f - 0.7) * period) if f >= 0.7 else 0.0
    return x, lift if side == 0 else 0.0, lift if side == 1 else 0.0, abs(math.sin(math.pi * f)), stamp


def run_in_place(t, t0, period=0.42, amp=0.9):
    """The run on the spot: (liftL, liftR, stamp, which foot 0/1)."""
    if t < t0:
        return 0.0, 0.0, 0.0, 0
    ph = (t - t0) / period
    f = ph % 1.0
    lift = amp * math.sin(math.pi * clamp(f / 0.68)) if f < 0.68 else 0.0
    side = int(ph) % 2
    stamp = math.exp(-12 * (f - 0.68) * period) if f >= 0.68 else 0.0
    return (lift if side == 0 else 0.0), (lift if side == 1 else 0.0), stamp, side


# ------------------------------------------------------------------ the rig (figure + a leg set by angles)


def rig(cr, look, x, feet, s=1.0, t=0.0, pose_=None, flip=False, alpha=1.0, legL=None, legR=None):
    """yaksha_kit.figure, except a leg can be given as (thigh angle, shin angle) (the kick: knee out, shin
    straightened). The standing leg keeps the feet on `feet`. Returns the kit's named points."""
    p = dict(Y.POSE)
    p.update(pose_ or {})
    thL, shL, ftL, hL = Y.leg_solve(p["bend"], p["liftL"])
    thR, shR, ftR, hR = Y.leg_solve(p["bend"], p["liftR"])
    if legL:
        thL, shL = legL
        ftL = -(thL + shL) * 0.6
    if legR:
        thR, shR = legR
        ftR = -(thR + shR) * 0.6
    hip_h = hR if legL else (hL if legR else max(hL, hR))
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x + p["shift"] * s, feet - hip_h * s)
    sx = math.cos(math.pi * 2 * p["spin"]) if p["spin"] else 1.0
    if abs(sx) < 0.06:
        sx = 0.06 if sx >= 0 else -0.06
    cr.scale(s * sx * (-1 if flip else 1), s)
    ctx = Y.Ctx(cr, look, p, t)
    uL, lL, _ = p["armL"]
    uR, lR, _ = p["armR"]
    br = p["breathe"]
    spec = {
        "root": (None, (0, 0), 0.0, 1.0),
        "thighL": ("root", (-Y.HIP[0], Y.HIP[1]), thL, 1.0),
        "shinL": ("thighL", (0, Y.THIGH), shL, 1.0),
        "footL": ("shinL", (0, Y.SHIN), ftL, 1.0),
        "thighR": ("root", (Y.HIP[0], Y.HIP[1]), -thR, 1.0),
        "shinR": ("thighR", (0, Y.THIGH), -shR, 1.0),
        "footR": ("shinR", (0, Y.SHIN), -ftR, 1.0),
        "torso": ("root", (0, 0), p["lean"], 1.0),
        "uarmL": ("torso", (-Y.SHOULDER[0], Y.SHOULDER[1] - 3 * br), uL, 1.0),
        "farmL": ("uarmL", (0, Y.UARM), -lL, 1.0),
        "uarmR": ("torso", (Y.SHOULDER[0], Y.SHOULDER[1] - 3 * br), -uR, 1.0),
        "farmR": ("uarmR", (0, Y.UARM), lR, 1.0),
        "head": ("torso", (0, Y.NECK - 2 * br), p["head"], look.get("head_s", 1.0)),
    }
    mats = Y._solve(cr, spec)
    for part, fn in Y.KINDS[look.get("kind", "actor")]:
        cr.set_matrix(mats[part])
        cr.save()
        fn(ctx)
        cr.restore()
    for name, part, pt in (("ankleL", "footL", (0, 0)), ("ankleR", "footR", (0, 0)), ("kneeL", "shinL", (0, 0)),
                           ("kneeR", "shinR", (0, 0)), ("soleL", "footL", (0, Y.FOOT_H)),
                           ("soleR", "footR", (0, Y.FOOT_H))):
        cr.set_matrix(mats[part])
        ctx.mark(name, *pt)
    cr.set_matrix(mats["root"])
    ctx.mark("waist", 0, 0)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    return ctx.pts


def fig(c, look, x, feet, s, t, p, flip=False, alpha=1.0, shadow=0.5, **kw):
    if shadow:
        Y.floor_shadow(c, x + p.get("shift", 0.0) * s, feet, 300 * s, shadow * alpha)
    return rig(c, look, x, feet, s, t, p, flip, alpha, **kw)


# ------------------------------------------------------------------ weapons and the flute


def sword(cr, x, y, s=1.0, rot=0.0, alpha=1.0):
    """A straight sword, hilt at (x, y), blade up (before rot)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(-14, -40), (-12, -330), (0, -372), (12, -330), (14, -40)], STEEL, 5.0, smooth=False)
    stroke(cr, [(0, -50), (0, -330)], 3.0, (0.55, 0.60, 0.66))
    shape(cr, [(-62, -46), (62, -46), (54, -26), (-54, -26)], GOLD, 5.0, smooth=False)
    shape(cr, [(-11, -26), (11, -26), (11, 46), (-11, 46)], RED, 4.0, smooth=False)
    for k in range(4):
        stroke(cr, [(-11, -14 + 16 * k), (11, -6 + 16 * k)], 3.0, GOLD_DK)
    dot(cr, 0, 58, 16, GOLD, 4.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def bow_icon(cr, x, y, s=1.0, rot=0.0, alpha=1.0):
    """A bow with its string (and an arrow), centred at (x, y)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    pts = [(-20, -220), (40, -150), (64, 0), (40, 150), (-20, 220)]
    stroke(cr, pts, 28, INK)
    stroke(cr, pts, 16, (0.62, 0.34, 0.12))
    stroke(cr, [(-20, -220), (-20, 220)], 4.0, CREAM, smooth=False)
    stroke(cr, [(-60, 0), (150, 0)], 7.0, INK, smooth=False)
    stroke(cr, [(-60, 0), (150, 0)], 3.5, GOLD, smooth=False)
    shape(cr, [(150, -14), (186, 0), (150, 14)], STEEL, 3.5, smooth=False)
    for sd in (-1, 1):
        shape(cr, [(-60, 0), (-80, sd * 18), (-30, sd * 6)], RED, 2.5, smooth=False)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def flute(cr, x0, y0, x1, y1, w=1.0, alpha=1.0):
    """Krishna's flute from (x0, y0) to (x1, y1): a bamboo tube with gold bands, holes and a red tassel."""
    a = math.atan2(y1 - y0, x1 - x0)
    L = math.dist((x0, y0), (x1, y1))
    cr.save()
    cr.translate(x0, y0)
    cr.rotate(a)
    cr.push_group()
    shape(cr, [(0, -11 * w), (L, -11 * w), (L, 11 * w), (0, 11 * w)], (0.86, 0.62, 0.28), 4.0, smooth=False)
    for u in (0.06, 0.94):
        stroke(cr, [(L * u, -11 * w), (L * u, 11 * w)], 7.0 * w, GOLD, smooth=False, cap=cairo.LINE_CAP_BUTT)
    for k in range(6):
        dot(cr, L * (0.30 + 0.09 * k), 0, 4.0 * w, INK)
    stroke(cr, [(L * 0.94, 8 * w), (L * 0.97, 40 * w), (L * 0.92, 70 * w)], 4.0 * w, RED)
    dot(cr, L * 0.92, 74 * w, 9 * w, RED, 2.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def mace(cr, x, y, s=1.0, rot=0.0, alpha=1.0):
    """The kit's gada drawn loose (thrown down): handle end at (x, y), head toward +y before rot."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(-8, -40), (8, -40), (8, 260), (-8, 260)], GOLD_DK, 4.0, smooth=False)
    oval(cr, 0, 300, 52, 62, GOLD, 6.0)
    for k in range(-2, 3):
        stroke(cr, [(k * 18, 248), (k * 22, 300), (k * 18, 352)], 3.0)
    dot(cr, 0, 368, 9, GOLD, 3.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def crossed_swords(cr, t, x, y, s=1.0, alpha=1.0, spark=1.0):
    """Two swords crossed (war), sparks where they meet."""
    if alpha <= 0.01:
        return
    sword(cr, x - 110 * s, y + 150 * s, s * 0.8, 0.62, alpha)
    sword(cr, x + 110 * s, y + 150 * s, s * 0.8, -0.62, alpha)
    if spark > 0.01:
        glow(cr, x, y - 20 * s, 150 * s, 0.45 * spark * alpha, (1.0, 0.75, 0.30))
        for i in range(6):
            u = (t * 1.8 + i / 6) % 1.0
            a = i * 1.05 + 0.3
            sparkle(cr, x + 120 * s * u * math.cos(a), y - 20 * s + 120 * s * u * math.sin(a),
                    (14 + 8 * math.sin(i)) * s * (1 - u) + 2, spark * alpha * (1 - u))


def red_x(cr, x, y, r, p, lw=18, alpha=1.0):
    """A painted red X, the two strokes one after the other."""
    if p <= 0.01:
        return
    for k, (a, b) in enumerate((((x - r, y - r), (x + r, y + r)), ((x + r, y - r), (x - r, y + r)))):
        q = clamp(p * 2 - k)
        if q <= 0:
            continue
        e = (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)
        stroke(cr, [a, e], lw + 12, INK, smooth=False, alpha=alpha)
        stroke(cr, [a, e], lw, RED, smooth=False, alpha=alpha)


# ------------------------------------------------------------------ Krishna's town and the army


def town(cr, t, x0, x1, floor, open_=0.0, alpha=1.0, flags=True):
    """Krishna's town on the stage: a sandstone fort wall with battlements, two towers with domes and saffron flags,
    and an arched gate in the middle whose wooden doors swing open (open_ 0..1). Returns the gate's centre x."""
    if alpha <= 0.01:
        return (x0 + x1) / 2
    cr.save()
    cr.push_group()
    top = floor - 470
    gx = (x0 + x1) / 2
    gw, gh = 190, 330
    cr.rectangle(x0, top, x1 - x0, floor - top)
    Y.ink_fill(cr, SAND, 6.0)
    for k in range(int((x1 - x0) / 56)):                  # battlements
        bx = x0 + 10 + 56 * k
        cr.rectangle(bx, top - 44, 34, 46)
        Y.ink_fill(cr, SAND, 5.0)
    for row in range(1, 7):                               # stone courses
        y = top + 66 * row
        stroke(cr, [(x0 + 4, y), (x1 - 4, y)], 2.5, SAND_DK, smooth=False)
        for k in range(int((x1 - x0) / 90) + 1):
            bx = x0 + 90 * k + (45 if row % 2 else 0)
            stroke(cr, [(bx, y), (bx, y + 66)], 2.5, SAND_DK, smooth=False)
    for tx in (x0 + 40, x1 - 40):                         # two towers with domes and flags
        cr.rectangle(tx - 56, top - 150, 112, floor - top + 150)
        Y.ink_fill(cr, (0.90, 0.72, 0.46), 6.0)
        shape(cr, [(tx - 66, top - 150), (tx - 56, top - 196), (tx - 30, top - 232), (tx, top - 244),
                   (tx + 30, top - 232), (tx + 56, top - 196), (tx + 66, top - 150)], GOLD, 6.0)
        dot(cr, tx, top - 258, 12, RED, 4.0)
        cr.rectangle(tx - 18, top - 100, 36, 60)
        Y.ink_fill(cr, (0.22, 0.10, 0.06), 4.0)
        if flags:
            stroke(cr, [(tx, top - 262), (tx, top - 380)], 6.0, INK, smooth=False)
            wv = 10 * math.sin(t * 4 + tx)
            shape(cr, [(tx + 3, top - 378), (tx + 96, top - 362 + wv), (tx + 70, top - 340), (tx + 98, top - 318 + wv),
                       (tx + 3, top - 324)], SAFF, 4.0, smooth=False)
    # the gate: a dark arch, the doors opening outward
    def arch(dx=0.0):
        cr.new_path()
        cr.move_to(gx - gw / 2 + dx, floor)
        cr.line_to(gx - gw / 2 + dx, floor - gh + gw / 2)
        cr.arc(gx + dx, floor - gh + gw / 2, gw / 2, math.pi, 2 * math.pi)
        cr.line_to(gx + gw / 2 + dx, floor)
        cr.close_path()
    arch()
    Y.ink_fill(cr, (0.06, 0.03, 0.02), 6.0)
    g = cairo.RadialGradient(gx, floor - 80, 10, gx, floor - 80, 260)      # warm light from inside the town
    g.add_color_stop_rgba(0, 1.0, 0.75, 0.35, 0.55 * ease(open_))
    g.add_color_stop_rgba(1, 1.0, 0.55, 0.20, 0.0)
    arch()
    cr.set_source(g)
    cr.fill()
    o = ease(open_)
    for sd in (-1, 1):                                    # the two doors (they swing open: narrower)
        w = gw / 2 * (1 - 0.82 * o)
        xa = gx + sd * gw / 2
        xb = xa - sd * w
        cr.save()
        arch()
        cr.clip()
        cr.rectangle(min(xa, xb), floor - gh - 10, abs(xa - xb), gh + 10)
        Y.ink_fill(cr, (0.48, 0.24, 0.08), 5.0)
        for k in range(4):
            yy = floor - gh + 70 + 70 * k
            stroke(cr, [(xa, yy), (xb, yy)], 6.0, GOLD_DK, smooth=False)
            dot(cr, (xa + xb) / 2, yy, 5, GOLD, 2.0)
        cr.restore()
    arch()
    cr.set_source_rgb(*INK)
    cr.set_line_width(8)
    cr.stroke()
    arch(0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()
    return gx


def soldier(cr, x, y, s, t, ph, col=(0.16, 0.10, 0.10), shield=RED):
    """One small marching soldier (a cut-out: helmet, body, a round shield, a spear), feet at (x, y)."""
    bob = 6 * abs(math.sin(t * 5 + ph)) * s
    cr.save()
    cr.translate(x, y - bob)
    cr.scale(s, s)
    stroke(cr, [(-14, 0), (-10, -70)], 14, INK)
    stroke(cr, [(14, 0), (10, -70)], 14, INK)
    shape(cr, [(-30, -70), (-28, -150), (28, -150), (30, -70)], col, 4.0, smooth=False)
    dot(cr, 0, -176, 26, (0.55, 0.36, 0.24), 4.0)
    shape(cr, [(-28, -178), (0, -214), (28, -178)], STEEL, 4.0, smooth=False)
    stroke(cr, [(38, 10), (46, -250)], 6.0, (0.45, 0.28, 0.12), smooth=False)
    shape(cr, [(40, -248), (46, -290), (54, -248)], STEEL, 3.0, smooth=False)
    dot(cr, -26, -110, 34, shield, 4.0)
    dot(cr, -26, -110, 10, GOLD, 2.0)
    cr.restore()


def army(cr, t, x0, x1, floor, rows=3, rise=1.0, march=1.0, alpha=1.0, split=None, left_alpha=1.0):
    """Rows of marching soldiers filling the stage between x0 and x1 (crores of them): the back rows small and dark,
    the front rows bigger; they rise up into view (rise 0..1) and march on the spot; soldiers left of `split` are
    drawn at left_alpha (they melt away)."""
    if alpha <= 0.01 or rise <= 0.01:
        return
    cr.save()
    cr.push_group()
    for r in range(rows):
        k = r / max(1, rows - 1)
        s = 0.62 + 0.43 * k
        yy = floor - 420 * (1 - k) - 20
        lift = (1 - ease(clamp(rise * 1.6 - k * 0.6))) * 500
        step = 70 * s
        n = int((W + 400) / step) + 2
        shade = 0.06 + 0.10 * k
        for i in range(n):
            x = -200 + i * step + (r % 2) * step * 0.5
            if x < x0 or x > x1:
                continue
            a = left_alpha if split is not None and x < split else 1.0
            if a <= 0.01:
                continue
            if a < 0.99:
                cr.push_group()
            soldier(cr, x, yy + lift, s, t * march, i * 0.7 + r, (shade, shade * 0.7, shade * 0.7),
                    (RED, CRIMSON, (0.70, 0.30, 0.06))[(i + r) % 3])
            if a < 0.99:
                cr.pop_group_to_source()
                cr.paint_with_alpha(a)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def arrows_over(cr, t, x0, x1, y, a=1.0, n=6, seed=0):
    """Arrows arcing from right to left over the stage."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * 0.9 + i / n + seed * 0.17) % 1.0
        x = x1 + (x0 - x1) * u
        yy = y - 260 * math.sin(math.pi * u) + 30 * i % 90
        ang = math.atan2(-260 * math.pi * math.cos(math.pi * u), (x0 - x1))
        cr.save()
        cr.translate(x, yy)
        cr.rotate(ang)
        al = a * clamp(u * 6) * clamp((1 - u) * 6)
        stroke(cr, [(-70, 0), (40, 0)], 9, INK, smooth=False, alpha=al)
        stroke(cr, [(-70, 0), (40, 0)], 4, GOLD, smooth=False, alpha=al)
        cr.new_path()
        cr.move_to(58, 0)
        cr.line_to(36, -10)
        cr.line_to(36, 10)
        cr.close_path()
        cr.set_source_rgba(*STEEL, al)
        cr.fill()
        cr.restore()


# ------------------------------------------------------------------ the theras (painted backdrops) of this story


def _field(cr):
    x0, y0, x1, y1 = Y.CURT
    bw = 64
    return x0 + bw, y0 + bw, x1 - bw, y1 - bw


def _folds(cr, fx0, fy0, fx1, fy1, a=0.14):
    for i in range(12):
        x = fx0 + (fx1 - fx0) * (i + 0.5) / 12
        g = cairo.LinearGradient(x - 40, 0, x + 40, 0)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
        g.add_color_stop_rgba(0.5, 0, 0, 0, a)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        cr.set_source(g)
        cr.rectangle(x - 40, fy0, 80, fy1 - fy0)
        cr.fill()


def _rock_blob(cr, cx, cy, rx, ry, col=ROCK, hi=ROCK_HI, seed=0, lw=6.0):
    rng = np.random.default_rng(seed)
    pts = []
    n = 11
    for i in range(n):
        a = 2 * math.pi * i / n
        k = rng.uniform(0.82, 1.1)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    shape(cr, pts, col, lw)
    stroke(cr, [(cx - rx * 0.6, cy - ry * 0.55), (cx - rx * 0.1, cy - ry * 0.8), (cx + rx * 0.4, cy - ry * 0.62)],
           5.0, hi)


@functools.lru_cache(maxsize=2)
def hills_surface():
    """The thera of the chase: a dusk sky painted on the cloth, rolling hills in flat bands, a rocky mountain."""
    src = Y.stage_surface("green", "none", True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_source_surface(src, 0, 0)
    cr.paint()
    fx0, fy0, fx1, fy1 = _field(cr)
    cr.save()
    cr.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    cr.clip()
    g = cairo.LinearGradient(0, fy0, 0, fy1)
    g.add_color_stop_rgb(0, 0.10, 0.08, 0.26)
    g.add_color_stop_rgb(0.55, 0.62, 0.22, 0.20)
    g.add_color_stop_rgb(1, 0.92, 0.52, 0.22)
    cr.set_source(g)
    cr.paint()
    dot(cr, 760, 900, 70, (1.0, 0.86, 0.45), 5.0)            # a low painted sun
    for k, (col, base, amp) in enumerate((((0.30, 0.20, 0.30), 1130, 90), ((0.22, 0.30, 0.18), 1290, 70),
                                          ((0.14, 0.24, 0.12), 1450, 60))):
        pts = [(fx0 - 20, fy1 + 10)]
        for i in range(13):
            x = fx0 - 20 + (fx1 - fx0 + 40) * i / 12
            pts.append((x, base - amp * (0.5 + 0.5 * math.sin(i * 1.3 + k * 2.1))))
        pts.append((fx1 + 20, fy1 + 10))
        shape(cr, pts, col, 5.0)
    shape(cr, [(700, 1330), (760, 1210), (820, 1150), (880, 1170), (fx1 + 20, 1220), (fx1 + 20, 1330)],
          (0.30, 0.22, 0.24), 5.0)                         # a far rocky hill with a small dark cave in it
    cr.new_path()
    cr.move_to(836, 1300)
    cr.line_to(836, 1262)
    cr.arc(856, 1262, 20, math.pi, 2 * math.pi)
    cr.line_to(876, 1300)
    cr.close_path()
    Y.ink_fill(cr, (0.03, 0.02, 0.03), 3.0)
    for k in range(4):                                     # a few painted trees on the hills
        x = fx0 + 90 + 210 * k
        y = 1330 + 60 * (k % 2)
        shape(cr, [(x - 8, y + 50), (x + 8, y + 50), (x + 6, y), (x - 6, y)], (0.35, 0.20, 0.10), 3.0, smooth=False)
        dot(cr, x, y - 16, 34, (0.10, 0.36, 0.16), 4.0)
    _folds(cr, fx0, fy0, fx1, fy1)
    cr.restore()
    s.flush()
    return s


@functools.lru_cache(maxsize=2)
def cave_surface():
    """The thera of the cave inside: the cloth painted dark with rock walls in flat bands, hanging rocks, a hole in
    the roof (the sky behind it is drawn live: sun and moon racing past)."""
    src = Y.stage_surface("indigo", "none", True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_source_surface(src, 0, 0)
    cr.paint()
    fx0, fy0, fx1, fy1 = _field(cr)
    cr.save()
    cr.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    cr.clip()
    g = cairo.RadialGradient(W / 2, 1300, 50, W / 2, 1200, 700)
    g.add_color_stop_rgb(0, 0.20, 0.14, 0.13)
    g.add_color_stop_rgb(1, 0.06, 0.04, 0.06)
    cr.set_source(g)
    cr.paint()
    # the hole in the roof (left of centre), cut out as transparent: the sky is drawn behind the thera later
    for k, (cx, cy, rx, ry) in enumerate(((fx0 + 40, 900, 150, 260), (fx1 - 40, 940, 150, 300),
                                          (fx0 + 60, 1340, 120, 220), (fx1 - 50, 1360, 130, 240),
                                          (380, fy0 + 20, 220, 90), (760, fy0 + 30, 240, 110))):
        _rock_blob(cr, cx, cy, rx, ry, (ROCK, (0.34, 0.27, 0.24), (0.44, 0.36, 0.30))[k % 3], ROCK_HI, seed=k)
    for i, x in enumerate((230, 300, 520, 640, 880)):       # hanging rocks
        L = (120, 70, 150, 90, 110)[i]
        shape(cr, [(x - 30, fy0 + 60), (x + 30, fy0 + 60), (x + 6, fy0 + 60 + L), (x, fy0 + 70 + L)],
              (0.36, 0.29, 0.25), 5.0, smooth=False)
    for k in range(5):                                      # cracks
        x = fx0 + 120 + 170 * k
        stroke(cr, [(x, 1050 + 30 * k), (x + 30, 1120 + 20 * k), (x + 10, 1200 + 30 * k)], 3.0, (0.03, 0.02, 0.02),
               alpha=0.6)
    _folds(cr, fx0, fy0, fx1, fy1, 0.18)
    cr.restore()
    # the roof hole: punch it out of the cloth
    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    Y.ell(cr, *HOLE)
    cr.fill()
    cr.restore()
    hx, hy, rx, ry = HOLE                                   # a rough rock lip round the hole
    cr.new_path()
    Y.ell(cr, hx, hy, rx + 16, ry + 14)
    Y.ell(cr, hx, hy, rx, ry)
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    Y.ink_fill(cr, (0.46, 0.38, 0.32), 6.0)
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    stroke(cr, [(hx - rx * 0.7, hy - ry - 4), (hx, hy - ry - 10), (hx + rx * 0.7, hy - ry - 4)], 5.0, ROCK_HI)
    s.flush()
    return s


HOLE = (300, 860, 120, 90)        # the roof hole: centre x, y, rx, ry (sky shows through)


def cave_sky(cr, t, speed=0.0, base=0.0):
    """The sky in the cave's roof hole: day and night racing past (speed in days per second), sun and moon."""
    hx, hy, rx, ry = HOLE
    cr.save()
    cr.new_path()
    Y.ell(cr, hx, hy, rx, ry)
    cr.clip()
    ph = (base + t * speed) % 1.0
    day = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
    cr.set_source_rgb(*mix((0.04, 0.05, 0.16), (0.45, 0.72, 0.95), day))
    cr.paint()
    a = 2 * math.pi * ph
    sx, sy = hx - 200 * math.cos(a), hy + 40 - 150 * math.sin(a)
    dot(cr, sx, sy, 34, (1.0, 0.85, 0.30), 4.0)
    mx, my = hx + 200 * math.cos(a), hy + 40 + 150 * math.sin(a)
    dot(cr, mx, my, 28, (0.95, 0.95, 0.85), 4.0)
    dot(cr, mx + 12, my - 8, 24, mix((0.04, 0.05, 0.16), (0.45, 0.72, 0.95), day), 0)
    cr.restore()


def cave_light(cr, a=1.0, x=300, y=860):
    """The shaft of daylight falling from the roof hole to the floor."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    g = cairo.LinearGradient(0, y, 0, Y.FLOOR_Y + 80)
    g.add_color_stop_rgba(0, 1.0, 0.90, 0.60, 0.22 * a)
    g.add_color_stop_rgba(1, 1.0, 0.85, 0.50, 0.04 * a)
    cr.move_to(x - 100, y + 30)
    cr.line_to(x + 100, y + 30)
    cr.line_to(x + 340, Y.FLOOR_Y + 80)
    cr.line_to(x - 60, Y.FLOOR_Y + 80)
    cr.close_path()
    cr.set_source(g)
    cr.fill()
    cr.restore()


def cave_stage(cr, t, sky_speed=0.0, sky_base=0.15, garland=True):
    cave_sky(cr, t, sky_speed, sky_base)
    cr.set_source_surface(cave_surface(), 0, 0)
    cr.paint()
    if garland:
        Y.thorana(cr, t)


def hills_stage(cr, t, garland=True):
    cr.set_source_surface(hills_surface(), 0, 0)
    cr.paint()
    if garland:
        Y.thorana(cr, t)


# ------------------------------------------------------------------ the cave mouth (a stage piece) and the stone bed


def _arch_path(cr, cx, floor, w, h):
    cr.new_path()
    cr.move_to(cx - w / 2, floor)
    cr.line_to(cx - w / 2, floor - h + w / 2)
    cr.arc(cx, floor - h + w / 2, w / 2, math.pi, 2 * math.pi)
    cr.line_to(cx + w / 2, floor)
    cr.close_path()


def cave_back(cr, cx, floor, s=1.0, alpha=1.0):
    """The dark inside of the cave mouth (drawn behind the actors)."""
    if alpha <= 0.01:
        return
    cr.save()
    _arch_path(cr, cx, floor, 360 * s, 620 * s)
    g = cairo.RadialGradient(cx, floor - 220 * s, 20, cx, floor - 220 * s, 380 * s)
    g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, alpha)
    g.add_color_stop_rgba(1, 0.10, 0.06, 0.06, alpha)
    cr.set_source(g)
    cr.fill()
    cr.restore()


def cave_swallow(cr, cx, floor, s=1.0, alpha=1.0):
    """Darkness over whatever is inside the mouth (actors going in fade into it); drawn over the actors."""
    if alpha <= 0.01:
        return
    cr.save()
    _arch_path(cr, cx, floor, 360 * s, 620 * s)
    cr.clip()
    g = cairo.RadialGradient(cx, floor - 200 * s, 30 * s, cx, floor - 200 * s, 300 * s)
    g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92 * alpha)
    g.add_color_stop_rgba(0.75, 0.02, 0.01, 0.01, 0.55 * alpha)
    g.add_color_stop_rgba(1, 0.05, 0.03, 0.03, 0.15 * alpha)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def cave_rim(cr, t, cx, floor, s=1.0, alpha=1.0):
    """The rock rim of the cave mouth: a heap of painted boulders round the dark arch (drawn over the actors)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    w, h = 360 * s, 620 * s
    ow, oh = w + 300 * s, h + 170 * s
    cr.new_path()                                          # a thick painted rock arch round the dark mouth
    rng = np.random.default_rng(31)
    pts = []
    for i in range(23):
        a = math.pi * i / 22
        k = 1.0 + 0.05 * rng.uniform(-1, 1)
        pts.append((cx - ow / 2 * math.cos(a) * k, floor - (oh - ow / 2) - ow / 2 * math.sin(a) * k * 0.9))
    pts = [(cx - ow / 2, floor)] + pts + [(cx + ow / 2, floor)]
    spath(cr, pts, closed=False)
    cr.line_to(cx + w / 2, floor)
    cr.line_to(cx + w / 2, floor - h + w / 2)
    cr.arc_negative(cx, floor - h + w / 2, w / 2, 0, math.pi)
    cr.line_to(cx - w / 2, floor)
    cr.close_path()
    Y.ink_fill(cr, ROCK, 7.0)
    for i in range(7):                                     # rock layers: cracks and lit edges
        a = math.pi * (0.08 + 0.84 * i / 6)
        r0, r1 = w / 2 + 14 * s, ow / 2 - 30 * s
        x0, y0 = cx - r0 * math.cos(a), floor - h + w / 2 - r0 * math.sin(a)
        x1, y1 = cx - r1 * math.cos(a + 0.05), floor - (oh - ow / 2) - r1 * math.sin(a + 0.05) * 0.9
        stroke(cr, [(x0, y0), ((x0 + x1) / 2 + 10 * s, (y0 + y1) / 2), (x1, y1)], 4.0, ROCK_DK)
    stroke(cr, [(cx - ow * 0.36, floor - oh * 0.72), (cx - ow * 0.1, floor - oh * 0.92), (cx + ow * 0.2,
                                                                                          floor - oh * 0.88)],
           7.0, ROCK_HI)
    for i, (u, rx) in enumerate(((-0.55, 0.16), (0.52, 0.14), (-0.30, 0.10))):      # boulders at its foot
        _rock_blob(cr, cx + u * ow, floor - 30 * s, rx * ow, 0.08 * oh, (0.46, 0.38, 0.32), ROCK_HI, seed=40 + i)
    for i in range(5):                                     # creepers hanging over the mouth
        x = cx - w * 0.35 + w * 0.18 * i
        L = (80, 130, 60, 110, 90)[i] * s
        pts = [(x, floor - h + 20 * s), (x + 8 * math.sin(t + i), floor - h + 20 * s + L * 0.5),
               (x - 4, floor - h + 20 * s + L)]
        stroke(cr, pts, 6.0, Y.DLEAF)
        for k in range(3):
            px, py = pts[min(2, k)]
            shape(cr, [(px, py), (px + 14, py + 8), (px + 4, py + 22)], Y.LEAF, 2.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def stone_bed(cr, x0, x1, top, floor):
    """A long stone slab on the floor of the cave (the sleeper's bed)."""
    shape(cr, [(x0, top + 20), (x0 + 30, top), (x1 - 30, top), (x1, top + 20), (x1 - 10, floor), (x0 + 10, floor)],
          (0.42, 0.36, 0.32), 6.0, smooth=False)
    stroke(cr, [(x0 + 30, top + 4), (x1 - 30, top + 4)], 5.0, ROCK_HI, smooth=False)
    for k in range(4):
        x = x0 + 80 + (x1 - x0 - 160) * k / 3
        stroke(cr, [(x, top + 30), (x + 20, top + 70), (x + 6, floor - 10)], 3.0, ROCK_DK, alpha=0.7)


def creepers(cr, t, x0, x1, y, p, seed=3):
    """Green creepers growing along a line (over the sleeper) as p goes 0..1 (years passing)."""
    if p <= 0.01:
        return
    rng = np.random.default_rng(seed)
    n = 5
    for i in range(n):
        ax = x0 + (x1 - x0) * (i + 0.3 * rng.uniform()) / n
        L = (0.4 + 0.6 * rng.uniform()) * 260 * p
        pts = []
        for k in range(8):
            u = k / 7
            pts.append((ax + L * u, y - 30 * math.sin(u * 5 + i) - 40 * u * rng.uniform()))
        stroke(cr, pts, 6.0, Y.DLEAF)
        for k in range(1, 8, 2):
            if k / 7 > p * 1.4:
                break
            px, py = pts[k]
            shape(cr, [(px, py), (px + 22, py - 18), (px + 30, py - 4), (px + 10, py + 8)], Y.LEAF, 3.0)


def cobweb(cr, x, y, r, p, corner=(1, 1), alpha=0.85):
    """A cobweb in a corner (x, y), spreading out to r (p 0..1)."""
    if p <= 0.01:
        return
    sx, sy = corner
    rr = r * ease(p)
    cr.save()
    cr.set_source_rgba(0.92, 0.92, 0.92, alpha)
    cr.set_line_width(2.4)
    for i in range(6):
        a = (math.pi / 2) * i / 5
        cr.move_to(x, y)
        cr.line_to(x + sx * rr * math.cos(a), y + sy * rr * math.sin(a))
    for k in range(1, 5):
        q = rr * k / 4
        cr.move_to(x + sx * q, y)
        for i in range(1, 6):
            a = (math.pi / 2) * i / 5
            cr.line_to(x + sx * q * 0.92 * math.cos(a), y + sy * q * 0.92 * math.sin(a))
    cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ the boon's power: the eye, beams, flash, ash


def big_eye(cr, t, x, y, s, open_=1.0, glow_a=0.0, alpha=1.0):
    """A big painted Yakshagana eye (the long black wing out to the temple) opening (open_ 0..1), rays when lit."""
    if alpha <= 0.01:
        return
    if glow_a > 0.01:
        Y.rays(cr, t, x, y, 60 * s, 330 * s, glow_a * alpha, 18, (1.0, 0.90, 0.55))
        glow(cr, x, y, 200 * s, 0.5 * glow_a * alpha, (1.0, 0.85, 0.45))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    eh = 60 * max(0.04, open_)
    cr.new_path()
    cr.move_to(-120, 0)
    cr.curve_to(-60, -eh * 1.4, 60, -eh * 1.4, 120, 0)
    cr.curve_to(60, eh * 1.0, -60, eh * 1.0, -120, 0)
    cr.close_path()
    Y.ink_fill(cr, WHITE, 0)
    cr.save()
    cr.new_path()
    cr.move_to(-120, 0)
    cr.curve_to(-60, -eh * 1.4, 60, -eh * 1.4, 120, 0)
    cr.curve_to(60, eh * 1.0, -60, eh * 1.0, -120, 0)
    cr.close_path()
    cr.clip()
    dot(cr, 0, -4, 44, (0.80, 0.10, 0.06) if glow_a > 0.3 else INK)
    dot(cr, 0, -4, 28, INK)
    dot(cr, 10, -16, 9, WHITE)
    cr.restore()
    stroke(cr, [(-124, 2), (-60, -eh * 1.36), (60, -eh * 1.36), (124, 2)], 14.0)
    stroke(cr, [(-118, 4), (-60, eh * 0.95), (60, eh * 0.95), (118, 4)], 7.0)
    cr.new_path()                                           # the long wing out to the temple
    cr.move_to(110, -6)
    cr.curve_to(160, -16, 200, -26, 250, -50)
    cr.curve_to(210, -14, 170, 8, 100, 10)
    cr.close_path()
    cr.set_source_rgb(*INK)
    cr.fill()
    shape(cr, [(-130, -70), (-40, -118), (60, -120), (150, -90), (60, -100), (-40, -98)], INK, 0)   # the brow
    Y.dot_row(cr, [(-120, -96), (-40, -134), (60, -136), (150, -110)], 9, 5.0, WHITE)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def beams(cr, srcs, dst, a=1.0, w=1.0):
    """Two beams of white-gold light from the eyes (srcs) to a target point."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for sx, sy in srcs:
        for lw, col, al in ((60 * w, (1.0, 0.70, 0.30), 0.25), (26 * w, (1.0, 0.88, 0.55), 0.55),
                            (9 * w, (1.0, 1.0, 0.92), 1.0)):
            stroke(cr, [(sx, sy), dst], lw, col, smooth=False, alpha=al * a)
    cr.restore()
    for sx, sy in srcs:
        glow(cr, sx, sy, 70 * w, 0.8 * a, (1.0, 0.92, 0.70))


def white_flash(cr, a):
    if a <= 0.01:
        return
    cr.save()
    cr.set_source_rgba(1.0, 0.99, 0.95, clamp(a))
    cr.paint()
    cr.restore()


def ash_heap(cr, x, floor, s=1.0, alpha=1.0):
    """A small grey heap of ash on the floor."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    shape(cr, [(x - 150 * s, floor + 6), (x - 110 * s, floor - 30 * s), (x - 40 * s, floor - 58 * s),
               (x + 20 * s, floor - 64 * s), (x + 90 * s, floor - 40 * s), (x + 150 * s, floor + 6)], ASH, 5.0)
    for k in range(9):
        dot(cr, x - 100 * s + 25 * k * s, floor - 20 * s - 18 * s * math.sin(k * 1.7) ** 2, 4 * s, ASH_DK)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def ash_flakes(cr, t, t0, x, y, w=300, h=900, n=40, alpha=1.0, seed=5, size=1.0):
    """Grey and white flakes of ash drifting up and sideways from a body-sized area, slowly thinning (from t0)."""
    if t < t0 or alpha <= 0.01:
        return
    rng = np.random.default_rng(seed)
    age = t - t0
    for i in range(n):
        bx = x + rng.uniform(-w / 2, w / 2)
        by = y - rng.uniform(0, h)
        sp = rng.uniform(40, 110)
        ph = rng.uniform(0, 6.28)
        life = rng.uniform(2.0, 4.5)
        u = age / life
        if u >= 1:
            continue
        px = bx + 60 * math.sin(age * 1.3 + ph) + 30 * age
        py = by - sp * age
        r = rng.uniform(4, 10) * (1 - 0.5 * u) * size
        col = ASH if i % 3 else (0.92, 0.91, 0.88)
        cr.save()
        cr.translate(px, py)
        cr.rotate(age * 2 + ph)
        cr.scale(1.0, 0.6)
        cr.new_path()
        cr.arc(0, 0, r, 0, 2 * math.pi)
        a = alpha * (1 - u) * clamp(age * 4)
        cr.set_source_rgba(*col, a)
        cr.fill_preserve()
        cr.set_source_rgba(*ASH_DK, 0.6 * a)
        cr.set_line_width(1.5)
        cr.stroke()
        cr.restore()


def impact(cr, t, t0, x, y, s=1.0, dur=0.5):
    """A star-burst where a kick lands."""
    u = (t - t0) / dur
    if not 0 <= u < 1:
        return
    k = (0.5 + 0.7 * ease(min(1.0, u * 3))) * s
    a = 1 - clamp((u - 0.4) / 0.6)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    pts = []
    for i in range(20):
        ang = math.pi * i / 10
        r = 120 if i % 2 == 0 else 52
        pts.append((r * math.cos(ang), r * math.sin(ang)))
    cr.push_group()
    shape(cr, pts, YEL, 7.0, smooth=False)
    shape(cr, [(p[0] * 0.55, p[1] * 0.55) for p in pts], WHITE, 0, smooth=False)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def dust(cr, t, t0, x, y, s=1.0, dur=0.8):
    """A puff of dust where a foot stamps."""
    u = (t - t0) / dur
    if not 0 < u < 1:
        return
    for k in range(7):
        a = math.pi * (0.05 + 0.9 * k / 6)
        d = (40 + 150 * ease(u)) * s
        px, py = x - d * math.cos(a), y - 6 - d * 0.35 * math.sin(a)
        r = (18 + 26 * u) * s
        cr.new_path()
        cr.arc(px, py, r, 0, 2 * math.pi)
        cr.set_source_rgba(0.80, 0.62, 0.42, 0.55 * (1 - u))
        cr.fill()


def dust_trail(cr, t, x, y, direction=1, a=1.0, s=1.0):
    """Little clouds kicked up behind a runner (direction = +1 running right)."""
    if a <= 0.01:
        return
    for i in range(5):
        u = (t * 2.4 + i / 5) % 1.0
        px = x - direction * (40 + 240 * u) * s
        py = y - 10 - 50 * u * s
        cr.new_path()
        cr.arc(px, py, (14 + 30 * u) * s, 0, 2 * math.pi)
        cr.set_source_rgba(0.80, 0.62, 0.42, 0.5 * a * (1 - u))
        cr.fill()


def speed_lines(cr, x, y, h, direction=1, a=1.0):
    """Painted speed strokes behind a runner."""
    if a <= 0.01:
        return
    for k in range(4):
        yy = y - h * (0.2 + 0.2 * k)
        L = 140 + 40 * (k % 2)
        stroke(cr, [(x - direction * 60, yy), (x - direction * (60 + L), yy)], 8.0, CREAM, smooth=False,
               alpha=0.7 * a)


# ------------------------------------------------------------------ the route map (the twist), footprints


def footprint(cr, x, y, s, ang, col, alpha=1.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(s, s)
    cr.new_path()
    Y.ell(cr, 0, 0, 9, 16)
    cr.set_source_rgba(*col, alpha)
    cr.fill()
    for k in range(4):
        cr.new_path()
        cr.arc(-6 + 4 * k, -20 + abs(k - 1.5), 3.2, 0, 2 * math.pi)
        cr.fill()
    cr.restore()


def route_path(x, y, w, h):
    """The chase route on the map, from the town (left) over the hills to the cave (right)."""
    return [(x - w * 0.36, y + h * 0.18), (x - w * 0.18, y + h * 0.26), (x - w * 0.04, y + h * 0.02),
            (x + w * 0.10, y - h * 0.14), (x + w * 0.22, y + h * 0.04), (x + w * 0.33, y + h * 0.12)]


def route_map(cr, t, x, y, w, h, p_cloth=1.0, p_path=0.0, ring=0.0, alpha=1.0):
    """A painted map cloth: the town at the left, the hills, the cave at the right with the sleeping king's crown
    in its dark; footprints run along the route (p_path 0..1), Krishna's small blue ones ahead of Kalayavana's big
    black ones; a red ring round the cave (ring 0..1)."""
    q = ease(clamp(p_cloth))
    if q <= 0.01 or alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(0.2 + 0.8 * q, 1.0)
    cr.translate(-x, -y)
    cr.push_group()
    shape(cr, [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)],
          GOLD, 7.0, smooth=False)
    shape(cr, [(x - w / 2 + 18, y - h / 2 + 18), (x + w / 2 - 18, y - h / 2 + 18), (x + w / 2 - 18, y + h / 2 - 18),
               (x - w / 2 + 18, y + h / 2 - 18)], (0.95, 0.86, 0.62), 4.0, smooth=False)
    # hills
    for k in range(3):
        cx = x - w * 0.08 + k * w * 0.14
        shape(cr, [(cx - 90, y + h * 0.20), (cx, y - h * 0.22 + 20 * k), (cx + 90, y + h * 0.20)], (0.55, 0.70, 0.36),
              4.0)
    # the town (a little fort) at the left
    tx, ty = x - w * 0.40, y + h * 0.10
    shape(cr, [(tx - 60, ty + 50), (tx - 60, ty - 40), (tx + 60, ty - 40), (tx + 60, ty + 50)], SAND, 4.0, smooth=False)
    for sd in (-1, 1):
        shape(cr, [(tx + sd * 60 - 18, ty - 40), (tx + sd * 60 - 18, ty - 90), (tx + sd * 60 + 18, ty - 90),
                   (tx + sd * 60 + 18, ty - 40)], SAND, 4.0, smooth=False)
        dot(cr, tx + sd * 60, ty - 98, 14, GOLD, 3.0)
    cr.new_path()
    cr.move_to(tx - 20, ty + 50)
    cr.line_to(tx - 20, ty + 10)
    cr.arc(tx, ty + 10, 20, math.pi, 2 * math.pi)
    cr.line_to(tx + 20, ty + 50)
    cr.close_path()
    Y.ink_fill(cr, (0.20, 0.08, 0.04), 3.0)
    # the cave at the right: a rock with a black mouth and the sleeper's crown glinting inside
    cx, cy = x + w * 0.38, y + h * 0.06
    shape(cr, [(cx - 110, cy + 80), (cx - 90, cy - 40), (cx - 30, cy - 100), (cx + 50, cy - 96), (cx + 110, cy - 30),
               (cx + 110, cy + 80)], ROCK, 5.0)
    cr.new_path()
    cr.move_to(cx - 44, cy + 80)
    cr.line_to(cx - 44, cy + 10)
    cr.arc(cx, cy + 10, 44, math.pi, 2 * math.pi)
    cr.line_to(cx + 44, cy + 80)
    cr.close_path()
    Y.ink_fill(cr, (0.03, 0.02, 0.02), 4.0)
    shape(cr, [(cx - 12, cy + 54), (cx - 14, cy + 34), (cx, cy + 22), (cx + 14, cy + 34), (cx + 12, cy + 54)], GOLD,
          2.5)
    # the route: a red dashed line drawn along, two rows of footprints on it (Krishna's blue ones ahead)
    path = route_path(x, y, w, h)
    pts = Y.along(path, 60)
    m = int(len(pts) * clamp(p_path))
    for i in range(0, m - 1, 2):
        stroke(cr, [pts[i], pts[i + 1]], 9.0, RED, smooth=False)
    for i in range(3, m, 5):
        px, py = pts[i]
        nx, ny = pts[min(i + 1, len(pts) - 1)]
        ang = math.atan2(ny - py, nx - px) + math.pi / 2
        nxx, nyy = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)      # unit normal of the route
        footprint(cr, px - 24 * nxx, py - 24 * nyy, 0.75, ang, (0.14, 0.09, 0.09))
        if i + 2 < m:
            qx, qy = pts[i + 2]
            footprint(cr, qx + 22 * nxx, qy + 22 * nyy, 0.6, ang, KR_BLUE)
    if m > 2:                                             # the red arrow head at the front of the route
        hx, hy = pts[m - 1]
        bx, by = pts[max(0, m - 3)]
        a = math.atan2(hy - by, hx - bx)
        cr.save()
        cr.translate(hx, hy)
        cr.rotate(a)
        shape(cr, [(34, 0), (-12, -26), (-2, 0), (-12, 26)], RED, 4.0, smooth=False)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()
    if ring > 0.01:
        from my_yk_cast import red_ring
        red_ring(cr, cx, cy + 10, 150, 130, ring, 12, alpha)
    return (tx, ty), (cx, cy)


# ------------------------------------------------------------------ a lamp of buddhi, a bubble with a picture


def lamp_of_mind(cr, t, x, y, s=1.0, alpha=1.0):
    """A brass oil lamp with a bright flame and rays: buddhi (wisdom)."""
    if alpha <= 0.01:
        return
    Y.rays(cr, t, x, y - 70 * s, 30 * s, 190 * s, 0.7 * alpha, 16, (1.0, 0.85, 0.45))
    glow(cr, x, y - 70 * s, 120 * s, 0.6 * alpha, (1.0, 0.80, 0.40))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    shape(cr, [(-70, -20), (70, -20), (40, 20), (-40, 20)], GOLD, 5.0)
    shape(cr, [(-20, 20), (20, 20), (30, 70), (-30, 70)], GOLD_DK, 4.0, smooth=False)
    shape(cr, [(-50, 70), (50, 70), (40, 86), (-40, 86)], GOLD, 4.0, smooth=False)
    f = 1 + 0.08 * math.sin(t * 9)
    shape(cr, [(0, -20), (-18, -50), (0, -110 * f), (18, -50)], (1.0, 0.70, 0.15), 4.0)
    shape(cr, [(0, -26), (-8, -50), (0, -80 * f), (8, -50)], (1.0, 0.95, 0.70), 0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def shake(t, t0, amp=14.0, dur=0.45):
    """(dx, dy) of a short shake after t0."""
    u = (t - t0) / dur
    if not 0 <= u < 1:
        return 0.0, 0.0
    d = amp * (1 - u)
    return d * math.sin(t * 90), d * 0.6 * math.cos(t * 77)
