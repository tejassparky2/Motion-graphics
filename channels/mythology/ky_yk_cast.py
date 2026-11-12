"""Yakshagana cast and props for the Kannada Kumbhakarna reel (scenes_kumbhakarna_yk), built on yaksha_kit. Nothing
here is shared with the Hindi shadow-puppet reel (kumbhakarna_cast / scenes_kumbhakarna).

Cast (one look each, kept the same through the reel):
  KUMBHAKARNA  the demon (bannada vesha) look made huge: the big flaming round crown, the black face with red patches,
               white dots and tusks, a black jacket over a round pot belly, a red-and-black check kase. Friendly-scary:
               he can open his mouth wide (a dropped jaw, teeth, tusks, a pink tongue) and a tiny glowing Saraswati
               can sit on his tongue; he snores with a round mouth; he can lie asleep across the whole stage.
  BRAHMA       the god look with a golden face, a long white beard, three of his four faces showing (two smaller
               faces turned out at the sides of his head, each under a small crown), a pink lotus in his hand and a
               lotus pedestal under his feet.
  SARASWATI    a goddess in a white saree with a gold border and a gold blouse, a small gold crown over her hair, her
               veena held across her body.
  RAVANA       a demon king: dark face, a tall gold crown with its round back-piece and two more heads at each side.
  RAMA         a blue-faced hero in the tall crown, with his bow. The gods: three crowned actors with halos.
Props: the whole world (a painted globe), the palm-leaf Ramayana, a homa fire, dolu drums, a caparisoned elephant,
food (bananas, a pot, laddus, a jackfruit), a calendar, Kannada word cards, tags, red rings, Zzz, a big "?".

The kit's actors are drawn by yaksha_kit.figure from a per-kind list of parts; the extra parts here (the belly, the
open mouth with Saraswati on the tongue, the side faces, the goddess crown) are added by drawing the figure with a
temporarily extended list (with_parts), so the kit file is never changed. The new face paint ("ky_brahma") and the
sleeping mood ("ky_sleep") are added under ky_ names.
"""
import functools
import math

import cairo

import yaksha_kit as Y
from poster import back, clamp, ease
from puppet_core import spath

Y.FACES.setdefault("ky_brahma", dict(base=(0.99, 0.72, 0.38), mark="namam", beard=(0.98, 0.97, 0.94),
                                     brow=(0.98, 0.97, 0.94), old=True, rouge=False))
Y.MOODS.setdefault("ky_sleep", dict(bi=-2, bo=3, lift=0, eh=15, mouth="smile", pupil=0.44))

TONGUE = (0.97, 0.45, 0.48)
TONGUE_DK = (0.78, 0.22, 0.30)
CAVITY = (0.24, 0.02, 0.04)
SR_GLOW = (1.0, 0.93, 0.70)
WOOD = (0.55, 0.30, 0.12)
WOOD_HI = (0.78, 0.50, 0.20)
LOTUS = (0.98, 0.50, 0.66)
LOTUS_DK = (0.84, 0.20, 0.44)
ELE = (0.52, 0.52, 0.58)
ELE_DK = (0.36, 0.36, 0.42)
SEA = (0.16, 0.48, 0.86)
LAND = (0.30, 0.66, 0.22)

# ------------------------------------------------------------------ looks

KUMBHAKARNA = dict(Y.DEMON, jacket=(0.12, 0.09, 0.10), sleeve=(0.62, 0.05, 0.08), kase=(Y.RED, Y.BLACK, Y.YEL, Y.GREEN),
                   hem=Y.BLACK, hem_zig=Y.YEL, sash=Y.RED, pads=Y.RED, ky_belly=1.0)
BRAHMA = dict(Y.GOD, face="ky_brahma", jacket=(0.86, 0.20, 0.10), sleeve=(0.86, 0.20, 0.10), hand=(0.99, 0.72, 0.38),
              kase=(Y.YEL, Y.RED, Y.INK, Y.GREEN), hem=Y.GREEN, sash=Y.WHITE, pads=Y.RED,
              disc_cols=(Y.GOLD, Y.RED, Y.GREEN), ky_faces=1)
SARASWATI = dict(Y.WOMAN, saree=Y.WHITE, border=Y.GOLD, blouse=(0.98, 0.62, 0.12), skin=(0.99, 0.80, 0.66),
                 hand=(0.99, 0.80, 0.66), ky_goddess=True)
RAVANA = dict(Y.DEMON, crown="kireeta", disc=True, disc_r=168.0, jacket=Y.GREEN, sleeve=Y.GREEN,
              kase=(Y.YEL, Y.GREEN, Y.INK, Y.RED), hem=Y.GREEN, hem_zig=Y.YEL, sash=Y.YEL, pads=Y.GREEN,
              disc_cols=(Y.GOLD, Y.GREEN, Y.RED), ky_heads=2)
RAMA = dict(Y.GOD, halo=False, jacket=Y.GREEN, sleeve=Y.GREEN, kase=(Y.YEL, Y.GREEN, Y.INK, Y.RED), hem=Y.RED,
            disc_cols=(Y.GOLD, Y.GREEN, Y.RED))
GODS = (dict(Y.KING, halo=True, jacket=Y.BLUE, sleeve=Y.BLUE, kase=(Y.YEL, Y.BLUE, Y.INK, Y.RED), hem=Y.BLUE),
        dict(Y.GOD, jacket=(0.98, 0.55, 0.10), sleeve=(0.98, 0.55, 0.10)),
        dict(Y.KING, halo=True, face="hero", jacket=Y.GREEN, sleeve=Y.GREEN))
DRUMMER = dict(Y.HERO, jacket=Y.WHITE, sleeve=Y.WHITE, kase=(Y.WHITE, Y.RED, Y.INK, Y.YEL), hem=Y.RED, sash=Y.RED)


# ------------------------------------------------------------------ extra parts for the kit's rig


def _belly(ctx):
    """Kumbhakarna's pot belly, under the jacket front (drawn before the kit's torso, so it shows at the sides)."""
    cr, look, p = ctx.cr, ctx.look, ctx.p
    k = look.get("ky_belly", 0.0)
    if k:
        puff = 1.0 + 0.045 * p.get("ky_puff", 0.0)
        Y.oval(cr, 0, -104, 156 * k * puff, 132 * puff, look["jacket"], 7.0)
        Y.stroke(cr, [(-120 * puff, -150), (-138 * puff, -100), (-124 * puff, -40)], 3.0, (0.35, 0.30, 0.32),
                 alpha=0.8)
        Y.stroke(cr, [(120 * puff, -150), (138 * puff, -100), (124 * puff, -40)], 3.0, (0.35, 0.30, 0.32), alpha=0.8)
    Y.torso(ctx)


def _goddess_crown(ctx):
    """A small gold kireeta over the woman's hair (Saraswati), with a string of pearls across the brow."""
    cr, look = ctx.cr, ctx.look
    if not look.get("ky_goddess"):
        return
    cr.translate(0, Y.FACE_C)
    cr.save()
    cr.translate(0, 6)
    cr.scale(0.92, 0.92)
    Y._kireeta(cr, look, ctx.t, small=True)
    cr.restore()
    Y.dot_row(cr, [(-60, -76), (-30, -90), (0, -93), (30, -90), (60, -76)], 13, 3.6, Y.WHITE, lw=1.4)


def _side_faces(ctx):
    """Brahma's two other faces (or two of Ravana's other heads each side), turned out, behind the main face."""
    cr, look, p, t = ctx.cr, ctx.look, ctx.p, ctx.t
    n = look.get("ky_heads", 0) or look.get("ky_faces", 0)
    if not n:
        return
    cr.translate(0, Y.FACE_C)
    for i in reversed(range(n)):
        for sd in (-1, 1):
            k = 0.70 - 0.10 * i
            dx = 128 + 92 * i
            dy = 4 + 18 * i
            cr.save()
            cr.translate(sd * dx, dy)
            cr.scale(k, k)
            Y.head_paint(Y.Ctx(cr, look, dict(p, turn=sd * 0.9, gaze=(sd * 0.7, 0.0), head=0.0), t))
            cr.save()
            cr.translate(sd * 8, 0)
            Y._kireeta(cr, look, t, small=True)
            Y._band(cr, look)
            cr.restore()
            cr.restore()


def _open_mouth(cr, op, base, seat_fn=None):
    """Kumbhakarna's mouth opened wide (face units, origin = face centre): the jaw drops below the face, a dark
    cavity with a row of teeth, two tusks, a pink tongue; seat_fn(cr, (x, y)) draws whatever sits on the tongue
    before the tongue's front edge is drawn over it."""
    bot = 66 + 38 * op
    w = 40 + 10 * op
    chin = bot + 24
    jaw = [(-66, 6), (-68, 48), (-62, chin - 34), (-38, chin - 6), (0, chin + 2), (38, chin - 6), (62, chin - 34),
           (68, 48), (66, 6)]
    Y.shape(cr, jaw, base, 6.0)
    jl = [(-62, 34), (-56, chin - 30), (-32, chin - 10), (0, chin - 5), (32, chin - 10), (56, chin - 30), (62, 34)]
    Y.stroke(cr, jl, 12.0)
    Y.stroke(cr, jl, 6.5, Y.WHITE)
    Y.dot_row(cr, jl, 9, 2.4, Y.RED)
    for sd in (-1, 1):                                   # the red cheek patches carried down the jaw
        Y.shape(cr, [(sd * 50, 14), (sd * 64, 30), (sd * 60, 60), (sd * 50, 52)], Y.RED, 2.5)
    cav = [(-w, 34), (-w * 0.6, 27), (0, 25), (w * 0.6, 27), (w, 34), (w * 0.92, bot - 16), (w * 0.55, bot - 2),
           (0, bot + 2), (-w * 0.55, bot - 2), (-w * 0.92, bot - 16)]
    Y.shape(cr, cav, CAVITY, 5.0)
    cr.save()
    cr.new_path()
    spath(cr, cav)
    cr.clip()
    Y.oval(cr, 0, bot - 4, w * 0.82, 18 + 6 * op, TONGUE, 3.5)          # the tongue, its back
    Y.stroke(cr, [(0, bot - 18), (0, bot - 2)], 2.5, TONGUE_DK)
    for i in range(7):                                                  # the upper teeth
        x = -w * 0.75 + w * 1.5 * i / 6
        Y.shape(cr, [(x - 6, 27), (x + 6, 27), (x, 38)], Y.WHITE, 2.0, smooth=False)
    cr.restore()
    seat = (0, bot - 12)
    if seat_fn:
        cr.save()
        cr.new_path()
        spath(cr, cav)
        cr.clip()
        seat_fn(cr, seat)
        cr.restore()
    cr.save()                                                           # the tongue's front edge over her lap
    cr.new_path()
    spath(cr, cav)
    cr.clip()
    cr.new_path()
    cr.move_to(-w * 0.8, bot - 8)
    cr.curve_to(-w * 0.5, bot - 20, w * 0.5, bot - 20, w * 0.8, bot - 8)
    cr.curve_to(w * 0.6, bot + 6, -w * 0.6, bot + 6, -w * 0.8, bot - 8)
    cr.close_path()
    Y.ink_fill(cr, TONGUE, 3.0)
    cr.restore()
    Y.stroke(cr, cav[:5], 4.5, Y.LIPS)
    for sd in (-1, 1):                                                  # tusks from the lower jaw
        Y.shape(cr, [(sd * (w * 0.62), bot - 2), (sd * (w * 0.90), bot - 10), (sd * (w * 0.86), bot - 40),
                     (sd * (w * 0.70), bot - 22)], Y.WHITE, 3.0)
    for sd in (-1, 1):                                                  # the curled moustache over the mouth
        pts = [(sd * 2, 22), (sd * 24, 18), (sd * 46, 20), (sd * 62, 10), (sd * 64, -6), (sd * 56, -4), (sd * 52, 8),
               (sd * 30, 28), (sd * 4, 30)]
        Y.shape(cr, pts, Y.INK, 0)
    return seat, bot


def _snore_mouth(cr, op, base):
    Y.oval(cr, 0, 49, 27, 13, base, 0)                                  # paint over the kit's smile
    Y.oval(cr, 0, 52, 12 + 6 * op, 10 + 9 * op, CAVITY, 4.0)
    Y.oval(cr, 0, 58 + 4 * op, 7 + 3 * op, 3 + 2 * op, TONGUE, 0)
    for sd in (-1, 1):
        pts = [(sd * 2, 33), (sd * 22, 30), (sd * 40, 29), (sd * 53, 19), (sd * 55, 6), (sd * 49, 9), (sd * 45, 21),
               (sd * 27, 38), (sd * 4, 40)]
        Y.shape(cr, pts, Y.INK, 0)


SR_POSE = dict(mood="smile", armL=(0.42, 1.30, 0.3), armR=(0.55, 2.15, 0.0), handL="open", handR="open")


def tiny_saraswati(cr, t, x, y, k, a=1.0):
    """Saraswati made tiny, drawn in the current frame with her waist at (x, y), k = scale."""
    if a <= 0.01:
        return
    figure(cr, SARASWATI, x, y + 440 * k, k, t, SR_POSE, alpha=a, veena=True)


def _mouth_part(ctx):
    cr, p, look = ctx.cr, ctx.p, ctx.look
    mode = p.get("ky_mouth")
    if not mode:
        return
    cr.translate(0, Y.FACE_C)
    base = Y.FACES[look["face"]]["base"]
    if mode == "open":
        sr = p.get("ky_sr", 0.0)

        def seat_fn(c, seat):
            ctx.mark("tongue", seat[0], seat[1])
            if sr > 0.01:
                k = p.get("ky_sr_k", 0.085)
                tiny_saraswati(c, ctx.t, seat[0], seat[1], k, sr)
                ctx.mark("sr", seat[0], seat[1] - 300 * k)
        _open_mouth(cr, p.get("ky_open", 1.0), base, seat_fn)
    elif mode == "snore":
        _snore_mouth(cr, p.get("ky_open", 0.5), base)
        ctx.mark("mouth", 0, 52)


@functools.lru_cache(maxsize=8)
def _parts(kind):
    base = list(Y.KINDS[kind])
    out = []
    for part, fn in base:
        if part == "torso" and fn is Y.torso:
            out.append(("torso", _belly))
            continue
        if part == "head" and fn is Y.head:
            out.append(("head", _side_faces))
            out.append(("head", fn))
            out.append(("head", _mouth_part))
            continue
        out.append((part, fn))
        if part == "head" and fn is Y.crown_front:
            out.append(("head", _goddess_crown))
    return out


def figure(cr, look, x, feet, s=1.0, t=0.0, pose=None, flip=False, alpha=1.0, veena=False, lotus=False):
    """yaksha_kit.figure with this reel's extra parts; veena / lotus draw Saraswati's veena or Brahma's lotus in the
    hands after the figure."""
    kind = look.get("kind", "actor")
    old = Y.KINDS[kind]
    Y.KINDS[kind] = _parts(kind)
    try:
        if alpha < 0.999:
            cr.push_group()
        pts = Y.figure(cr, look, x, feet, s, t, pose, flip, 1.0)
        if veena:
            draw_veena(cr, pts, s, t)
        if lotus:
            hand = pts["handR" if not flip else "handL"]
            hx, hy = to_user(cr, hand)
            held_lotus(cr, hx, hy - 10 * s, s)
        if alpha < 0.999:
            cr.pop_group_to_source()
            cr.paint_with_alpha(alpha)
        return pts
    finally:
        Y.KINDS[kind] = old


def to_user(cr, p):
    m = cr.get_matrix()
    m.invert()
    return m.transform_point(*p)


# ------------------------------------------------------------------ props held


def draw_veena(cr, pts, s, t):
    """Saraswati's veena across her body: the big gourd by her lower hand, the neck up past her raised hand, a small
    gourd under the neck and a carved head at the top."""
    a = to_user(cr, pts["handL"])
    b = to_user(cr, pts["handR"])
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    g = (a[0] - ux * 95 * s, a[1] - uy * 95 * s + 14 * s)        # the big gourd, beyond the plucking hand
    top = (b[0] + ux * 220 * s, b[1] + uy * 220 * s)
    ang = math.atan2(uy, ux)
    cr.save()
    cr.translate(*g)
    cr.rotate(ang)
    cr.scale(s, s)
    Lr = math.hypot(top[0] - g[0], top[1] - g[1]) / s
    Y.shape(cr, [(0, -20), (Lr, -14), (Lr, 14), (0, 20)], WOOD, 5.0, smooth=False)              # the neck
    for i in range(9):                                                                     # frets
        u = 120 + (Lr - 200) * i / 8
        Y.stroke(cr, [(u, -12), (u, 12)], 3.0, Y.GOLD)
    for j in (-6, -2, 2, 6):                                                               # strings
        Y.stroke(cr, [(40, j), (Lr - 20, j * 0.8)], 1.2, (0.98, 0.95, 0.80))
    Y.oval(cr, Lr * 0.80, 40, 40, 40, WOOD, 5.0)                                          # the small gourd
    Y.oval(cr, Lr * 0.80, 40, 24, 24, WOOD_HI, 0)
    Y.shape(cr, [(Lr - 6, -14), (Lr + 30, -34), (Lr + 52, -22), (Lr + 40, 0), (Lr + 14, 12)], Y.GOLD, 4.5)  # head
    Y.dot(cr, Lr + 34, -22, 4, Y.RED)
    Y.oval(cr, 0, 0, 96, 86, WOOD, 6.5)                                                   # the big gourd
    Y.oval(cr, 0, 0, 72, 64, WOOD_HI, 3.5)
    Y.oval(cr, 0, 0, 38, 33, Y.GOLD, 3.5)
    Y.dot(cr, 0, 0, 12, Y.RED, 2.5)
    Y.dot_row(cr, [(-66, -40), (0, -62), (66, -40)], 9, 3.4, Y.GOLD_HI)
    cr.restore()


def held_lotus(cr, x, y, s):
    """A pink lotus on a short stem rising from a hand at (x, y)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.stroke(cr, [(0, 40), (4, -40), (0, -120)], 14.0, Y.INK)
    Y.stroke(cr, [(0, 40), (4, -40), (0, -120)], 8.0, Y.LEAF)
    lotus_flower(cr, 0, -130, 1.0)
    cr.restore()


def lotus_flower(cr, x, y, k):
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    for ang in (-1.1, 1.1, -0.6, 0.6):
        cr.save()
        cr.rotate(ang)
        Y.shape(cr, [(0, 8), (-20, -20), (0, -66), (20, -20)], LOTUS_DK, 3.5)
        cr.restore()
    for ang in (-0.3, 0.3, 0.0):
        cr.save()
        cr.rotate(ang)
        Y.shape(cr, [(0, 8), (-20, -24), (0, -74), (20, -24)], LOTUS, 3.5)
        Y.stroke(cr, [(0, 0), (0, -50)], 2.0, LOTUS_DK)
        cr.restore()
    Y.oval(cr, 0, 6, 30, 10, Y.YEL, 3.0)
    cr.restore()


def lotus_seat(cr, x, y, w):
    """A wide lotus pedestal whose top is at y (a god stands on it)."""
    cr.save()
    cr.translate(x, y)
    k = w / 300.0
    cr.scale(k, k)
    for row, (yy, n, col, h) in enumerate(((54, 9, LOTUS_DK, 70), (30, 8, LOTUS, 84))):
        for i in range(n):
            u = (i + 0.5) / n
            px = -300 + 600 * u
            Y.shape(cr, [(px - 46, yy + 20), (px - 30, yy - h * 0.5), (px, yy - h), (px + 30, yy - h * 0.5),
                         (px + 46, yy + 20)], col, 4.5)
            Y.stroke(cr, [(px, yy + 10), (px, yy - h * 0.7)], 2.5, LOTUS_DK if col == LOTUS else Y.INK, alpha=0.7)
    Y.shape(cr, [(-280, 64), (280, 64), (250, 96), (-250, 96)], Y.GOLD, 5.0, smooth=False)
    Y.dot_row(cr, [(-260, 80), (260, 80)], 16, 3.2, Y.RED)
    cr.restore()


def bow(cr, x, y, s, ang=0.0, draw=0.0):
    """Rama's bow standing upright at (x, y) (its grip), its string pulled back by `draw`."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(s, s)
    pts = [(0, -300), (40, -200), (56, 0), (40, 200), (0, 300)]
    Y.stroke(cr, pts, 22.0, Y.INK)
    Y.stroke(cr, pts, 13.0, WOOD_HI)
    Y.stroke(cr, [(0, -300), (-60 * draw, 0), (0, 300)], 2.5, Y.CREAM, smooth=False)
    Y.shape(cr, [(30, -30), (66, -30), (66, 30), (30, 30)], Y.RED, 4.0, smooth=False)
    cr.restore()


def arrow(cr, x, y, ang, s=1.0, a=1.0):
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(s, s)
    Y.stroke(cr, [(-90, 0), (60, 0)], 9.0, Y.INK)
    Y.stroke(cr, [(-90, 0), (60, 0)], 4.5, Y.CREAM)
    Y.shape(cr, [(54, -12), (86, 0), (54, 12)], Y.GOLD, 3.0, smooth=False)
    for sd in (-1, 1):
        Y.shape(cr, [(-92, 0), (-74, sd * 16), (-58, sd * 16), (-72, 0)], Y.RED, 2.5, smooth=False)
    cr.restore()


# ------------------------------------------------------------------ props on the stage


def globe(cr, t, x, y, r, a=1.0, spin=0.0):
    """The whole world as a painted ball: blue sea, green lands with little trees and houses, a black outline."""
    if a <= 0.01:
        return
    cr.push_group()
    Y.dot(cr, x, y, r, SEA, 0)
    cr.save()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.clip()
    off = (spin * 0.8) % 2.0 - 1.0
    lands = [(-0.45, -0.35, 0.42, 0.30), (0.35, 0.10, 0.36, 0.42), (-0.25, 0.45, 0.30, 0.20), (0.55, -0.55, 0.22, 0.16)]
    for lx, ly, rx, ry in lands:
        for wrap in (-2.0, 0.0, 2.0):
            cx = x + r * (lx + off + wrap)
            Y.oval(cr, cx, y + r * ly, r * rx, r * ry, LAND, 4.0)
            for k in range(3):                                          # little trees and a house on each land
                tx = cx + r * rx * (-0.5 + 0.5 * k)
                ty = y + r * ly - r * ry * 0.1
                if k == 1:
                    Y.shape(cr, [(tx - 9, ty + 8), (tx - 9, ty - 4), (tx, ty - 13), (tx + 9, ty - 4), (tx + 9, ty + 8)],
                            Y.CREAM, 2.0, smooth=False)
                else:
                    Y.dot(cr, tx, ty - 6, 8, Y.DLEAF, 2.0)
    cr.restore()
    g = cairo.RadialGradient(x - r * 0.4, y - r * 0.4, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.30)
    g.add_color_stop_rgba(0.5, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(1, 0, 0, 0.1, 0.35)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*Y.INK)
    cr.set_line_width(7)
    cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)


def palm_book(cr, x, y, s, op=1.0, a=1.0):
    """The palm-leaf Ramayana: two carved wooden boards and a stack of long leaves tied with a red string; `op`
    fans the leaves open."""
    if a <= 0.01:
        return
    cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-350, 0), (350, 0), (360, 40), (-360, 40)], WOOD, 6.0, smooth=False)        # the bottom board
    Y.dot_row(cr, [(-300, 20), (300, 20)], 7, 6.0, Y.GOLD, lw=2.0)
    leaf = [(-320, -36), (320, -36), (336, 0), (320, 36), (-320, 36), (-336, 0)]
    for i in range(4):                                                                       # the closed leaves
        cr.save()
        cr.translate(0, -30 - 16 * i)
        Y.shape(cr, leaf, (0.90, 0.78, 0.50) if i % 2 else (0.95, 0.85, 0.60), 3.5, smooth=False)
        cr.restore()
    for k in range(2):                                                                       # two leaves lifting open
        u = ease(clamp(op * 1.3 - 0.3 * k))
        cr.save()
        cr.translate(-330, -96 - 4 * k)
        cr.rotate(-0.42 * u * (1.0 - 0.45 * k))
        cr.translate(330, 0)
        Y.shape(cr, leaf, (0.97, 0.88, 0.64), 4.0, smooth=False)
        for r in range(3):                                                                  # lines of writing
            yy = -18 + 18 * r
            xs = -280
            while xs < 280:
                w = 22 + 18 * abs(math.sin(xs * 0.37 + r))
                Y.stroke(cr, [(xs, yy), (xs + w * 0.5, yy - 5), (xs + w, yy)], 3.0, (0.30, 0.18, 0.08))
                xs += w + 12
        for hx in (-150, 150):                                                              # the string holes
            Y.dot(cr, hx, 0, 7, (0.45, 0.30, 0.12), 2.0)
        cr.restore()
    Y.stroke(cr, [(-150, -100), (-150, 30), (-120, 60)], 5.0, Y.RED)
    Y.dot(cr, -116, 66, 10, Y.RED, 3.0)
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    return y - 140 * s



def homa(cr, t, x, y, s, a=1.0):
    """A sacred fire in a square brick pit (homa kunda): bricks, flames that flicker, a glow."""
    if a <= 0.01:
        return
    Y.glow(cr, x, y - 60 * s, 260 * s, 0.35 * a, (1.0, 0.55, 0.15))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for row in range(2):
        for i in range(5):
            bx = -150 + 60 * i + (30 if row else 0)
            if bx > 120:
                continue
            Y.shape(cr, [(bx, -row * 30), (bx + 58, -row * 30), (bx + 58, -row * 30 + 28), (bx, -row * 30 + 28)],
                    (0.72, 0.30, 0.16), 3.5, smooth=False)
    for k, (w, h, col) in enumerate(((70, 170, (1.0, 0.40, 0.06)), (48, 128, (1.0, 0.72, 0.16)),
                                     (24, 80, (1.0, 0.96, 0.75)))):
        sw = 10 * math.sin(t * 7 + k) + 6 * math.sin(t * 11.3 + k)
        hh = h * (1 + 0.08 * math.sin(t * 9 + k * 2))
        cr.new_path()
        cr.move_to(-w, -30)
        cr.curve_to(-w, -30 - hh * 0.5, sw, -30 - hh * 0.75, sw * 1.4, -30 - hh)
        cr.curve_to(sw, -30 - hh * 0.75, w, -30 - hh * 0.5, w, -30)
        cr.close_path()
        cr.set_source_rgba(*col, a)
        cr.fill()
    cr.restore()


def dolu(cr, x, y, s, hit=0.0):
    """A big dolu drum lying across a drummer's front: a red barrel with gold rings and pale heads."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    k = 1 + 0.04 * hit
    Y.shape(cr, [(-150, -70 * k), (150, -70 * k), (166, 0), (150, 70 * k), (-150, 70 * k), (-166, 0)], Y.RED, 6.0)
    for xx in (-100, 0, 100):
        Y.stroke(cr, [(xx, -72), (xx + 4, 0), (xx, 72)], 9.0, Y.GOLD)
    for zz in range(6):
        Y.stroke(cr, [(-140 + 56 * zz, -64), (-112 + 56 * zz, 64)], 2.5, Y.CREAM, alpha=0.8)
    for sd in (-1, 1):
        Y.oval(cr, sd * 160, 0, 22, 74 * k, (0.95, 0.88, 0.70), 5.0)
    cr.restore()


def drum_stick(cr, x0, y0, x1, y1, w=1.0):
    Y.stroke(cr, [(x0, y0), (x1, y1)], 12 * w, Y.INK, smooth=False)
    Y.stroke(cr, [(x0, y0), (x1, y1)], 6 * w, WOOD_HI, smooth=False)
    Y.dot(cr, x1, y1, 9 * w, WOOD, 3.0)


def elephant(cr, t, x, y, s, walk=0.0, flip=False):
    """A temple elephant in side view facing right (flip: left), feet on y: grey body, red caparison with gold
    borders and tassels, a gold headpiece, the trunk swinging, legs stepping with `walk` (a phase)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(-s if flip else s, s)
    ph = walk * 2 * math.pi
    legs = [(-120, 0.0), (-60, math.pi), (70, math.pi * 0.5), (130, math.pi * 1.5)]
    for i, (lx, lp) in enumerate(legs):                      # far legs first (darker)
        far = i % 2 == 1
        sw = 16 * math.sin(ph + lp)
        lift = max(0.0, math.sin(ph + lp)) * 18
        col = ELE_DK if far else ELE
        Y.shape(cr, [(lx - 26, -150), (lx + 26, -150), (lx + 24 + sw, -10 - lift), (lx + 30 + sw, 0 - lift),
                     (lx - 30 + sw, 0 - lift), (lx - 24 + sw, -10 - lift)], col, 5.0, smooth=False)
        for k in range(3):
            Y.dot(cr, lx - 16 + 16 * k + sw, -6 - lift, 4.5, Y.CREAM, 1.5)
    Y.shape(cr, [(-190, -150), (-196, -230), (-150, -300), (-40, -330), (80, -320), (170, -280), (210, -200),
                 (200, -140), (140, -110), (-130, -110)], ELE, 6.0)                        # the body
    Y.stroke(cr, [(-190, -200), (-226, -150), (-218, -120)], 7.0, Y.INK)                    # tail
    sw = 0.25 * math.sin(t * 2.2)                                                            # the trunk
    trunk = [(232, -250), (276, -200), (292 + 20 * sw, -130), (282 + 30 * sw, -60), (300 + 40 * sw, -30)]
    Y.stroke(cr, trunk, 50.0, Y.INK)
    Y.stroke(cr, trunk, 38.0, ELE)
    Y.oval(cr, 210, -260, 62, 72, ELE, 6.0)                                                  # the head
    Y.shape(cr, [(150, -300), (110, -250), (120, -170), (170, -150), (190, -230)], ELE_DK, 5.0)  # the ear
    Y.shape(cr, [(196, -224), (236, -218), (262, -196), (226, -194)], Y.WHITE, 3.0)           # tusk
    Y.dot(cr, 232, -276, 8, Y.WHITE, 2.5)
    Y.dot(cr, 234, -276, 4, Y.INK)
    Y.shape(cr, [(170, -330), (240, -330), (264, -300), (250, -250), (196, -240), (170, -290)], Y.GOLD, 4.5)  # crest
    Y.dot_row(cr, [(186, -312), (246, -300)], 4, 4.0, Y.RED, lw=1.5)
    cap = [(-140, -300), (100, -316), (120, -170), (-130, -160)]                             # the caparison
    Y.shape(cr, cap, Y.RED, 5.5, smooth=False)
    Y.stroke(cr, [(-138, -294), (102, -310)], 10.0, Y.GOLD, smooth=False)
    Y.stroke(cr, [(-128, -170), (118, -178)], 12.0, Y.GOLD, smooth=False)
    Y.dot_row(cr, [(-120, -240), (100, -250)], 7, 7.0, Y.GREEN, lw=2.0)
    for i in range(8):
        tx = -120 + 32 * i
        Y.stroke(cr, [(tx, -170), (tx, -146)], 2.5)
        Y.dot(cr, tx, -140, 8, (Y.YEL, Y.GREEN)[i % 2], 2.5)
    cr.restore()


def banana_bunch(cr, x, y, s, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    for i in range(4):
        cr.save()
        cr.rotate(-0.5 + 0.33 * i)
        Y.shape(cr, [(0, 0), (16, -30), (14, -90), (0, -116), (-8, -96), (-4, -30)], Y.YEL, 4.0)
        cr.restore()
    Y.shape(cr, [(-12, -4), (12, -4), (8, 22), (-8, 22)], (0.40, 0.30, 0.10), 3.5, smooth=False)
    cr.restore()


def pot(cr, x, y, s, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    Y.shape(cr, [(-40, -60), (40, -60), (34, -44), (66, -10), (62, 40), (0, 66), (-62, 40), (-66, -10), (-34, -44)],
            (0.80, 0.42, 0.16), 5.0)
    Y.stroke(cr, [(-60, 4), (0, 14), (60, 4)], 6.0, Y.CREAM)
    Y.oval(cr, 0, -60, 42, 10, (0.98, 0.95, 0.88), 4.0)
    for k in range(5):
        Y.dot(cr, -24 + 12 * k, -70 - 6 * (k % 2), 9, (0.98, 0.95, 0.88), 2.0)
    cr.restore()


def laddus(cr, x, y, s, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    Y.shape(cr, [(-80, 0), (80, 0), (60, 18), (-60, 18)], Y.GOLD, 4.0, smooth=False)
    for i, (lx, ly) in enumerate(((-44, -20), (0, -20), (44, -20), (-22, -52), (22, -52), (0, -82))):
        Y.dot(cr, lx, ly, 22, (0.99, 0.66, 0.16), 4.0)
        Y.dot(cr, lx - 6, ly - 6, 4, Y.GOLD_HI)
    cr.restore()


def jackfruit(cr, x, y, s, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    Y.oval(cr, 0, 0, 56, 74, (0.62, 0.70, 0.18), 5.0)
    for i in range(5):
        for j in range(4):
            Y.dot(cr, -36 + 18 * i, -46 + 30 * j + (9 if i % 2 else 0), 3.0, (0.32, 0.40, 0.08))
    Y.stroke(cr, [(0, -74), (6, -96)], 7.0, (0.40, 0.30, 0.10))
    cr.restore()


FOODS = (banana_bunch, pot, laddus, jackfruit)


def calendar(cr, t, x, y, s, n, flip=0.0, a=1.0):
    """A hanging wall calendar: a red top bar with two rings, the page showing "<n> / ವರ್ಷ" (years); `flip` 0..1 is
    the old page tearing away upward."""
    if a <= 0.01:
        return
    cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.stroke(cr, [(-60, -150), (0, -200), (60, -150)], 5.0)
    Y.dot(cr, 0, -200, 9, Y.GOLD, 3.0)
    page = [(-150, -140), (150, -140), (150, 150), (-150, 150)]
    Y.shape(cr, page, Y.CREAM, 6.0, smooth=False)
    _page_text(cr, n)
    if flip > 0.0:                                             # the old page flying up and away
        cr.save()
        cr.translate(0, -140)
        cr.rotate(-0.6 * flip)
        cr.translate(260 * flip, -200 * flip)
        cr.scale(1.0, 1.0 - 0.6 * flip)
        cr.translate(0, 140)
        cr.push_group()
        Y.shape(cr, page, Y.CREAM, 6.0, smooth=False)
        _page_text(cr, n - 1)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - flip)
        cr.restore()
    Y.shape(cr, [(-160, -170), (160, -170), (160, -116), (-160, -116)], Y.RED, 6.0, smooth=False)
    for sd in (-1, 1):
        Y.dot(cr, sd * 90, -144, 12, Y.GOLD, 3.0)
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)


def _page_text(cr, n):
    Y.kn_text(cr, str(n), 0, -10, 150, Y.RED, Y.INK, 6)
    Y.kn_text(cr, "ವರ್ಷ", 0, 104, 64, Y.INK)


# ------------------------------------------------------------------ cards, tags and marks (screen space)


def red_ring(cr, x, y, rx, ry, p, w=9.0, a=1.0):
    """A hand-drawn red ring drawn round (x, y) as p goes 0 -> 1."""
    if p <= 0.01 or a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(rx, ry)
    cr.new_path()
    a0 = -2.2
    cr.arc(0, 0, 1, a0, a0 + 2 * math.pi * 1.08 * ease(clamp(p)))
    cr.restore()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    path = cr.copy_path()
    cr.set_source_rgba(*Y.INK, a)
    cr.set_line_width(w + 7)
    cr.stroke()
    cr.append_path(path)
    cr.set_source_rgba(0.90, 0.08, 0.06, a)
    cr.set_line_width(w)
    cr.stroke()


def tag(cr, t, t_in, text, x, y, to=None, size=58, field=Y.CRIMSON, col=Y.YEL, a=1.0):
    """A small painted cloth name tag at (x, y) with an optional pointer line to `to`."""
    q = clamp((t - t_in) / 0.3)
    if q <= 0 or a <= 0.01:
        return
    k = 0.6 + 0.4 * back(q, 2.0)
    s = Y.kn_surface(text, int(size), tuple(col), tuple(Y.INK), 5.0, None, 0.0)
    w, h = s.get_width() + 44, s.get_height() + 22
    if to is not None:
        Y.stroke(cr, [(x, y), to], 9.0, Y.INK, smooth=False, alpha=a * clamp(q * 2))
        Y.stroke(cr, [(x, y), to], 4.0, Y.GOLD, smooth=False, alpha=a * clamp(q * 2))
        Y.dot(cr, to[0], to[1], 8 * k, Y.GOLD, 3.0)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.push_group()
    cr.rectangle(-w / 2, -h / 2, w, h)
    Y.ink_fill(cr, Y.GOLD, 6.0)
    cr.rectangle(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16)
    Y.ink_fill(cr, field, 3.0)
    cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a * clamp(q * 2.5))
    cr.restore()


def word_card(cr, t, t_in, text, x, y, size=170, field=Y.CREAM, col=Y.RED, rot=0.0, a=1.0, label=None,
              label_col=Y.INK, w_min=0):
    """A big Kannada word on a painted card (gold frame, red teeth), dropping in with an overshoot; label = a small
    line above the word. Returns the card's box."""
    q = clamp((t - t_in) / 0.4)
    if q <= 0 or a <= 0.01:
        return None
    s = Y.kn_surface(text, int(size), tuple(col), tuple(Y.CREAM if field != Y.CREAM else Y.WHITE), 8.0, tuple(Y.INK),
                     6.0)
    ls = Y.kn_surface(label, 54, tuple(label_col), tuple(Y.INK), 0.0, None, 0.0) if label else None
    w = max(w_min, s.get_width() + 90, (ls.get_width() + 80) if ls else 0)
    h = s.get_height() + 60 + ((ls.get_height() + 6) if ls else 0)
    fit = min(1.0, 940.0 / w)
    k = (0.5 + 0.5 * back(q, 2.0)) * fit
    cr.save()
    cr.translate(x, y + 40 * (1 - q))
    cr.rotate(rot)
    cr.scale(k, k)
    cr.push_group()
    cr.rectangle(-w / 2 + 10, -h / 2 + 14, w, h)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    Y.ink_fill(cr, Y.GOLD, 7.0)
    Y._border_teeth(cr, -w / 2 + 4, -h / 2 + 8, w / 2 - 4, -h / 2 + 8, max(6, int(w / 34)), Y.RED, 1)
    Y._border_teeth(cr, w / 2 - 4, h / 2 - 8, -w / 2 + 4, h / 2 - 8, max(6, int(w / 34)), Y.RED, 1)
    cr.rectangle(-w / 2 + 16, -h / 2 + 28, w - 32, h - 56)
    Y.ink_fill(cr, field, 5.0)
    yy = -h / 2 + 30
    if ls:
        cr.set_source_surface(ls, -ls.get_width() / 2, yy + 4)
        cr.paint()
        yy += ls.get_height() + 6
    cr.set_source_surface(s, -s.get_width() / 2, yy + (h - 60 - (yy + h / 2 - 30) - s.get_height()) / 2 + 2)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a * clamp(q * 2.5))
    cr.restore()
    return x - w * k / 2, y - h * k / 2, w * k, h * k


def qmark(cr, t, t_in, x, y, size, a=1.0):
    """A big red question mark swinging in."""
    q = clamp((t - t_in) / 0.5)
    if q <= 0 or a <= 0.01:
        return
    k = 0.3 + 0.7 * back(q, 2.4)
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.12 * math.sin(t * 2.4) * (1 - 0.3 * q))
    cr.scale(k, k)
    Y.kn_text(cr, "?", 0, 0, size, (0.90, 0.08, 0.06), Y.CREAM, 12, Y.INK, 9, alpha=a * clamp(q * 2))
    cr.restore()


def zzz(cr, t, x, y, s=1.0, a=1.0, n=3):
    """Z's rising and growing from (x, y), drifting right."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * 0.45 + i / n) % 1.0
        al = a * clamp(u * 4) * clamp((1 - u) * 3)
        size = (40 + 70 * u) * s
        Y.kn_text(cr, "Z", x + 90 * u * s + 10 * math.sin(t * 2 + i), y - 220 * u * s, size, Y.CREAM, Y.INK, 6,
                  alpha=al)


def sound_rings(cr, t, x, y, r, a=1.0, ang=0.0, spread=0.9, n=3, col=Y.YEL):
    """Booming arcs spreading from (x, y) toward `ang`."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * 1.6 + i / n) % 1.0
        rr = r * (0.3 + u)
        al = a * (1 - u)
        cr.new_path()
        cr.arc(x, y, rr, ang - spread / 2, ang + spread / 2)
        cr.set_source_rgba(*Y.INK, al)
        cr.set_line_width(16)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke_preserve()
        cr.set_source_rgba(*col, al)
        cr.set_line_width(8)
        cr.stroke()


def choice_card(cr, t, t_in, text, x, y, w, h, field, col=Y.CREAM, a=1.0):
    q = clamp((t - t_in) / 0.35)
    if q <= 0:
        return
    k = 0.6 + 0.4 * back(q, 2.0)
    cr.save()
    cr.translate(x, y + 30 * (1 - q))
    cr.scale(k, k)
    cr.push_group()
    cr.rectangle(-w / 2 + 10, -h / 2 + 14, w, h)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    Y.ink_fill(cr, Y.GOLD, 7.0)
    cr.rectangle(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32)
    Y.ink_fill(cr, field, 5.0)
    Y.kn_text(cr, text, 0, 0, 120, col, Y.INK, 7, max_w=w - 60)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a * clamp(q * 2.5))
    cr.restore()
