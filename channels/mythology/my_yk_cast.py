"""Cast and props for the Kannada Yakshagana reel of video 19, andhe_ka_putra (scenes_andhe_ka_putra_yk): the looks
built from yaksha_kit's ready looks, a palace servant with a turban (a new figure kind registered under this module's
own name), and the props this story needs, all in the kit's flat paint with thick black outlines:

  the palace of illusions   a thera painted as Maya's crystal hall (pillars, arches, a shining tiled floor that ripples
                            like water), and a crystal-tile floor cloth over the stage boards
  the pond                  a blue water cloth on the stage floor (waves, lotus leaves), hidden under a skin of tiles
                            until Duryodhana steps in; a splash of drops; the water line and ripples round his waist
  the palm-leaf book        an ole-gari manuscript (Vyasa's Mahabharata) that opens; leaves with written lines
  the old TV                a wooden TV set drawn round the stage (bezel, knobs, antenna) for "what we saw on TV"
  gold and envy             heaps of gold coins and a chest of jewels; a green fire (hotte-kichchu, "stomach fire")
  marks                     red cross, red ring, tick, stamp, laugh marks, name tags, the question mark
"""
import functools
import math

import cairo
import numpy as np

import yaksha_kit as Y
from poster import H, W, back, clamp, ease

INK = Y.INK

# ------------------------------------------------------------------ looks

DKGOLD = (0.62, 0.43, 0.08)
DURYO = dict(Y.KING, jacket=DKGOLD, sleeve=DKGOLD, kase=((0.80, 0.58, 0.14), Y.MAROON, INK, Y.RED), hem=Y.MAROON,
             hem_zig=Y.GOLD, sash=Y.MAROON, pads=Y.MAROON, disc_cols=(Y.GOLD, Y.MAROON, (0.14, 0.10, 0.10)))
DRAUPADI = dict(Y.WOMAN, saree=(0.80, 0.06, 0.22), border=Y.GOLD, blouse=Y.GREEN)
BHIMA = dict(Y.HERO, jacket=(0.80, 0.10, 0.06), sleeve=(0.80, 0.10, 0.06))
ARJUNA = dict(Y.HERO, crown="kireeta", disc=True, jacket=Y.BLUE, sleeve=Y.BLUE, kase=(Y.YEL, Y.BLUE, INK, Y.RED),
              hem=Y.BLUE, disc_cols=(Y.GOLD, Y.BLUE, Y.RED))
NAKULA = dict(Y.HERO, crown="kireeta_small", jacket=Y.SAFF, sleeve=Y.SAFF, kase=(Y.YEL, Y.GREEN, INK, Y.RED),
              hem=Y.GREEN)
SAHADEVA = dict(NAKULA, jacket=(0.52, 0.16, 0.56), sleeve=(0.52, 0.16, 0.56), kase=(Y.YEL, (0.52, 0.16, 0.56), INK,
                                                                                    Y.GREEN))
YUDHI = dict(Y.KING)
VYASA = dict(Y.SAGE)
DHRITA = dict(Y.KING, jacket=(0.93, 0.88, 0.74), sleeve=(0.93, 0.88, 0.74), kase=(Y.WHITE, Y.RED, INK, Y.GOLD),
              hem=Y.RED, sash=Y.RED, pads=Y.RED, disc_cols=(Y.GOLD, Y.RED, Y.WHITE))

# --- the palace servant: bare chest and dhoti (the sage's body), the hero's painted face, a red turban

_HERO_BASE = Y.FACES["hero"]["base"]


def _turban(ctx):
    cr, look = ctx.cr, ctx.look
    cr.translate(0, Y.FACE_C)
    col = look.get("turban", Y.RED)
    Y.shape(cr, [(-72, -40), (-80, -84), (-60, -118), (-20, -134), (20, -134), (60, -118), (80, -84), (72, -40),
                 (40, -66), (0, -72), (-40, -66)], col, 5.5)
    for k in range(3):                                   # the wound folds
        y = -78 - 16 * k
        Y.stroke(cr, [(-70 + 6 * k, y + 8), (0, y - 6), (70 - 6 * k, y + 8)], 4.0, INK, alpha=0.7)
    Y.stroke(cr, [(-74, -66), (0, -80), (74, -66)], 9.0, Y.GOLD)
    Y.stroke(cr, [(-74, -66), (0, -80), (74, -66)], 2.0)
    Y.oval(cr, 0, -96, 12, 15, Y.GOLD, 3.0)
    Y.dot(cr, 0, -98, 5, Y.RED)
    Y.shape(cr, [(4, -120), (14, -164), (30, -176), (24, -150), (14, -124)], (0.97, 0.95, 0.90), 3.0)   # a plume
    for sd in (-1, 1):                                   # ears with gold rings
        Y.oval(cr, sd * 68, -6, 10, 20, look.get("skin", Y.SKIN), 3.0)
        Y.dot(cr, sd * 70, 22, 7, Y.GOLD, 2.5)
    ctx.mark("crown", 0, -176)


def _servant_parts():
    uL, lL = Y._arm(-1)
    uR, lR = Y._arm(1)
    return [("shinL", Y._shin(-1)), ("shinR", Y._shin(1)), ("footL", Y._foot(-1)), ("footR", Y._foot(1)),
            ("root", Y.dhoti), ("torso", Y.sage_torso),
            ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR), ("head", Y.head), ("head", _turban)]


Y.KINDS.setdefault("my_servant", _servant_parts())      # registered under this module's own name (kit untouched)
SERVANT = dict(kind="my_servant", face="hero", head_s=1.1, skin=_HERO_BASE, hand=_HERO_BASE, cloth=Y.WHITE,
               cloth2=Y.RED, turban=Y.RED)
SERVANT2 = dict(SERVANT, cloth=(0.99, 0.80, 0.30), cloth2=Y.GREEN, turban=Y.GREEN)


# ------------------------------------------------------------------ the palace of illusions (a painted thera)

CRYSTAL = (0.62, 0.88, 0.96)
CRYSTAL_DK = (0.20, 0.52, 0.70)
WATER = (0.10, 0.42, 0.78)
WATER_DK = (0.04, 0.22, 0.52)
WATER_HI = (0.70, 0.92, 1.0)


def _arch(cr, x0, x1, y_spring, rise, col, lw):
    """A cusped (scalloped) Indian arch between two pillars, as a gold line."""
    cx = (x0 + x1) / 2
    w = (x1 - x0) / 2
    pts = []
    n = 7
    for i in range(n + 1):
        a = math.pi * (1 - i / n)
        pts.append((cx + w * math.cos(a), y_spring - rise * math.sin(a)))
    cr.new_path()
    cr.move_to(*pts[0])
    for a_, b_ in zip(pts, pts[1:]):                     # a little cusp between each pair of points
        mx, my = (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2
        dx, dy = mx - cx, my - y_spring
        L = math.hypot(dx, dy) or 1
        cr.curve_to(mx - dx / L * 18, my - dy / L * 18, mx - dx / L * 18, my - dy / L * 18, b_[0], b_[1])
    cr.set_source_rgba(*col)
    cr.set_line_width(lw)
    cr.stroke()


def _tile_floor(cr, x0, x1, y0, y1, vx, vy, n=12, rows=7, base=CRYSTAL, line=CRYSTAL_DK, alpha=1.0):
    """A floor of square tiles seen in perspective (vanishing point vx, vy), filled flat."""
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_source_rgba(*base, alpha)
    cr.paint()
    cr.set_source_rgba(*line, 0.85 * alpha)
    cr.set_line_width(3.0)
    span = (x1 - x0) * 2.2
    for i in range(-n, n + 1):
        bx = (x0 + x1) / 2 + i * span / (2 * n)
        cr.move_to(vx + (bx - vx) * (y0 - vy) / (y1 - vy), y0)
        cr.line_to(bx, y1)
    for k in range(1, rows + 1):
        u = (k / rows) ** 1.7
        y = y0 + (y1 - y0) * u
        cr.move_to(x0, y)
        cr.line_to(x1, y)
    cr.stroke()
    cr.restore()


@functools.lru_cache(maxsize=2)
def palace_surface():
    """The thera of Maya's palace: the kit's indigo stage with the crystal hall painted on the cloth."""
    src = Y.stage_surface("indigo", "none", True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_source_surface(src, 0, 0)
    cr.paint()
    x0, y0, x1, y1 = Y.CURT
    bw = 64
    fx0, fy0, fx1, fy1 = x0 + bw, y0 + bw, x1 - bw, y1 - bw
    cr.save()
    cr.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    cr.clip()
    g = cairo.LinearGradient(0, fy0, 0, fy1)               # the hall: deep blue to teal
    g.add_color_stop_rgb(0, 0.05, 0.10, 0.30)
    g.add_color_stop_rgb(0.62, 0.06, 0.26, 0.44)
    g.add_color_stop_rgb(1, 0.08, 0.34, 0.50)
    cr.set_source(g)
    cr.paint()
    fl = 1260                                              # where the painted floor begins
    _tile_floor(cr, fx0, fx1, fl, fy1, W / 2, 900, 9, 6, (0.40, 0.74, 0.88), (0.14, 0.40, 0.60))
    for k in range(5):                                     # the shine on the floor: it looks like water
        y = fl + 40 + 62 * k
        pts = [(fx0 + 20 + 60 * i, y + 9 * math.sin(i * 1.3 + k)) for i in range(15)]
        Y.stroke(cr, pts, 6.0 - 0.6 * k, WATER_HI, alpha=0.75)
    gold = (*Y.GOLD, 0.95)
    cols = [fx0 + 40, 330, 540, 750, fx1 - 40]
    for x in cols:                                         # pillars, painted in gold lines over the blue
        cr.rectangle(x - 26, 840, 52, fl - 840)
        cr.set_source_rgba(0.10, 0.20, 0.42, 0.9)
        cr.fill_preserve()
        cr.set_source_rgba(*gold)
        cr.set_line_width(5)
        cr.stroke()
        for y in (880, 960, fl - 40):
            cr.rectangle(x - 34, y - 10, 68, 20)
            cr.set_source_rgba(*gold)
            cr.fill()
        for k in range(6):
            Y.dot(cr, x, 1000 + 40 * k, 5, Y.MIRROR)
    for a, b in zip(cols, cols[1:]):
        _arch(cr, a + 26, b - 26, 900, 150, gold, 6)
        _arch(cr, a + 44, b - 44, 912, 118, (*Y.MIRROR, 0.6), 3)
    for i in range(4):                                     # a crystal lamp hanging in each bay
        cx = (cols[i] + cols[i + 1]) / 2
        Y.stroke(cr, [(cx, fy0), (cx, 770)], 3.0, Y.GOLD)
        Y.shape(cr, [(cx, 770), (cx + 26, 806), (cx, 862), (cx - 26, 806)], Y.MIRROR, 4.0, smooth=False)
        Y.shape(cr, [(cx, 780), (cx + 12, 806), (cx, 838), (cx - 12, 806)], (1.0, 0.95, 0.75), 0, smooth=False)
        Y.glow(cr, cx, 812, 90, 0.35, (0.75, 0.92, 1.0))
    rng = np.random.default_rng(11)
    for _ in range(26):                                    # crystal glints
        x, y = rng.uniform(fx0 + 20, fx1 - 20), rng.uniform(fy0 + 20, fy1 - 40)
        Y.sparkle(cr, x, y, rng.uniform(8, 16), 0.7)
    for i in range(12):                                    # cloth folds over the painting
        x = fx0 + (fx1 - fx0) * (i + 0.5) / 12
        g = cairo.LinearGradient(x - 40, 0, x + 40, 0)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
        g.add_color_stop_rgba(0.5, 0, 0, 0, 0.14)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        cr.set_source(g)
        cr.rectangle(x - 40, fy0, 80, fy1 - fy0)
        cr.fill()
    cr.restore()
    floor_cloth(cr)
    s.flush()
    return s


def floor_cloth(cr):
    """The crystal-tile floor cloth spread over the stage boards in the palace scenes."""
    y0 = Y.FLOOR_Y
    _tile_floor(cr, 0, W, y0, H, W / 2, 1100, 9, 5, (0.52, 0.80, 0.90), (0.18, 0.44, 0.62))
    g = cairo.LinearGradient(0, y0, 0, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.45)
    g.add_color_stop_rgba(0.4, 0, 0, 0, 0.0)
    cr.set_source(g)
    cr.rectangle(0, y0, W, H - y0)
    cr.fill()
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.move_to(0, y0)
    cr.line_to(W, y0)
    cr.stroke()


def palace_stage(cr, t, garland=True):
    cr.set_source_surface(palace_surface(), 0, 0)
    cr.paint()
    if garland:
        Y.thorana(cr, t)


def floor_shine(cr, t, a=1.0, x0=0.0, x1=W, y0=Y.FLOOR_Y + 6, y1=H):
    """Moving ripples of light over the crystal floor: the floor that looks like water."""
    if a <= 0.01:
        return
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_operator(cairo.OPERATOR_ADD)
    for k in range(6):
        y = y0 + 30 + (y1 - y0 - 40) * ((k / 6 + 0.06 * t) % 1.0)
        amp = 6 + 0.04 * (y - y0)
        pts = [(x, y + amp * math.sin(x / 70 + t * 2.2 + k)) for x in np.linspace(x0 - 20, x1 + 20, 24)]
        Y.stroke(cr, pts, 5 + 0.02 * (y - y0), (0.55, 0.85, 1.0), alpha=0.35 * a)
    cr.restore()


# ------------------------------------------------------------------ the pond (a water cloth on the stage floor)


def pond_path(cr, cx, cy, rx, ry):
    cr.new_path()
    Y.ell(cr, cx, cy, rx, ry)


def pond(cr, t, cx, cy, rx, ry, skin=1.0, ripple=0.0, lotus=True, rim=1.0, hint=0.0):
    """The pond on the floor: blue water with wave lines and lotus leaves; `skin` 0..1 lays the crystal tiles over
    it (water that looks like floor), `hint` 0..1 lets the water show faintly through the tiles; `rim` the stone
    rim's opacity; `ripple` > 0 rings spreading out from the middle after a fall."""
    if rim > 0.01:
        pond_path(cr, cx, cy, rx + 10, ry + 6)
        Y.ink_fill(cr, (0.70, 0.60, 0.40), 6.0, alpha=clamp(rim))      # the stone rim
    cr.save()
    pond_path(cr, cx, cy, rx, ry)
    cr.clip()
    g = cairo.RadialGradient(cx, cy - ry * 0.3, 0, cx, cy, rx)
    g.add_color_stop_rgb(0, *WATER)
    g.add_color_stop_rgb(1, *WATER_DK)
    cr.set_source(g)
    cr.paint()
    for k in range(5):                                     # wave lines
        y = cy - ry + (2 * ry) * (k + 0.5) / 5
        pts = [(x, y + 6 * math.sin(x / 40 + t * 2.0 + k * 1.7)) for x in np.linspace(cx - rx, cx + rx, 18)]
        Y.stroke(cr, pts, 4.0, WATER_HI, alpha=0.75)
    if lotus:
        for (dx, dy, r) in ((-0.62, 0.15, 0.13), (0.55, -0.25, 0.11), (0.70, 0.35, 0.09)):
            x, y = cx + dx * rx, cy + dy * ry
            cr.save()
            cr.translate(x, y)
            cr.scale(1, 0.45)
            cr.new_path()
            cr.arc(0, 0, r * rx, 0.25, 2 * math.pi - 0.25)
            cr.line_to(0, 0)
            cr.close_path()
            cr.restore()
            Y.ink_fill(cr, Y.LEAF, 3.0)
        x, y = cx - 0.62 * rx, cy + 0.15 * ry - 10
        for k in range(5):
            a = math.pi * (0.15 + 0.7 * k / 4)
            Y.shape(cr, [(x, y), (x + 26 * math.cos(a) - 8, y - 30 * math.sin(a)), (x + 30 * math.cos(a),
                                                                                  y - 38 * math.sin(a)),
                         (x + 26 * math.cos(a) + 8, y - 30 * math.sin(a))], Y.PINK, 2.5)
    if ripple > 0:
        for k in range(3):
            u = (ripple * 0.8 + k * 0.33) % 1.0
            cr.save()
            cr.translate(cx, cy)
            cr.scale(1, ry / rx)
            cr.arc(0, 0, rx * (0.15 + 0.85 * u), 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(*WATER_HI, 0.8 * (1 - u))
            cr.set_line_width(5)
            cr.stroke()
    if skin > 0.01:                                        # the crystal tiles over the water
        _tile_floor(cr, cx - rx - 10, cx + rx + 10, cy - ry - 6, cy + ry + 6, W / 2, 1100, 9, 5,
                    (0.52, 0.80, 0.90), (0.18, 0.44, 0.62), alpha=skin * (1 - 0.5 * clamp(hint)))
    cr.restore()


def clip_above_water(cr, y, t, amp=6.0):
    """Clip to everything above a gently waving water line at y (a figure standing in the pond)."""
    cr.new_path()
    cr.move_to(-50, -50)
    cr.line_to(W + 50, -50)
    for x in np.linspace(W + 50, -50, 40):
        cr.line_to(x, y + amp * math.sin(x / 40 + t * 4.0))
    cr.close_path()
    cr.clip()


def waterline(cr, t, x, y, w, a=1.0, churn=0.0):
    """The water round a figure's waist in the pond: rings spreading on the surface and a collar of water across
    the front of the body (the front half of an ellipse), with bright wave lines."""
    if a <= 0.01:
        return
    for k in range(3):                                     # rings spreading out on the surface
        u = (t * 0.6 + k / 3) % 1.0
        rx = w * (0.55 + 0.9 * u)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.28)
        cr.arc(0, 0, rx, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*WATER_HI, 0.7 * (1 - u) * a)
        cr.set_line_width(4)
        cr.stroke()
    rx, ry = w * 0.62, w * 0.17
    amp = 4 + 8 * churn
    cr.new_path()
    for i, ang in enumerate(np.linspace(0, math.pi, 24)):  # the front half of the collar
        px = x + rx * math.cos(ang)
        py = y + ry * math.sin(ang) + amp * math.sin(ang * 6 + t * 5)
        (cr.move_to if i == 0 else cr.line_to)(px, py)
    for ang in np.linspace(math.pi, 0, 24):
        cr.line_to(x + rx * 0.98 * math.cos(ang), y - 6 + amp * 0.6 * math.sin(ang * 5 + t * 4))
    cr.close_path()
    cr.set_source_rgba(*WATER, 0.92 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(4)
    cr.stroke()
    pts = [(x + rx * 0.85 * math.cos(ang), y + ry * 0.55 * math.sin(ang) + 3 * math.sin(ang * 7 + t * 5))
           for ang in np.linspace(0.3, math.pi - 0.3, 14)]
    Y.stroke(cr, pts, 4.0, WATER_HI, alpha=0.9 * a)


def splash(cr, t, t_s, x, y, s=1.0):
    """Drops of water flying up and out from (x, y) after t_s, falling back (a comic, harmless splash)."""
    u = (t - t_s) / 1.1
    if u <= 0 or u >= 1:
        return
    rng = np.random.default_rng(5)
    for k in range(16):
        ang = math.pi * (0.08 + 0.84 * k / 15) + rng.uniform(-0.08, 0.08)
        sp = rng.uniform(380, 720) * s
        px = x - math.cos(ang) * sp * u
        py = y - math.sin(ang) * sp * u * 1.3 + 900 * s * u * u
        r = (14 + 10 * rng.random()) * s * (1 - 0.5 * u)
        cr.save()
        cr.translate(px, py)
        cr.rotate(-ang + math.pi / 2)
        Y.shape(cr, [(0, -r * 1.8), (r * 0.9, 0), (0, r), (-r * 0.9, 0)], WATER_HI, 3.0)
        cr.restore()
    hgt = 260 * s * math.sin(math.pi * clamp(u * 1.25))  # jets of water leaping up in a fan, round drops on top
    if hgt > 4:
        for i in range(7):
            a = (i - 3) * 0.26
            hh = hgt * (1.0 - 0.12 * abs(i - 3))
            bx = x + (i - 3) * 46 * s
            tx, ty = bx + math.sin(a) * hh * 0.9, y - math.cos(a) * hh
            w0 = 24 * s
            cr.new_path()
            cr.move_to(bx - w0, y + 6)
            cr.curve_to(bx - w0 * 0.6, y - hh * 0.4, tx - 8 * s, ty + 30 * s, tx, ty)
            cr.curve_to(tx + 8 * s, ty + 30 * s, bx + w0 * 0.6, y - hh * 0.4, bx + w0, y + 6)
            cr.close_path()
            Y.ink_fill(cr, (0.62, 0.86, 1.0) if i % 2 else (0.86, 0.96, 1.0), 4.0)
            Y.dot(cr, tx, ty - 14 * s, 13 * s, (0.86, 0.96, 1.0), 3.5)


def drips(cr, t, x, y, w, a=1.0, n=5):
    """Water dripping (from his crown and sleeves), a pure function of t."""
    for k in range(n):
        u = (t * 0.9 + k / n) % 1.0
        px = x - w / 2 + w * (k + 0.5) / n
        py = y + 120 * u * u
        Y.shape(cr, [(px, py - 14), (px + 7, py + 2), (px, py + 9), (px - 7, py + 2)], WATER_HI, 2.5)


# ------------------------------------------------------------------ the palm-leaf book (ole-gari)

LEAF_COL = (0.93, 0.80, 0.52)
LEAF_DK = (0.66, 0.48, 0.24)


def leaf(cr, x, y, w, h, alpha=1.0, lines=3, holes=True):
    """One palm leaf: a long rounded strip with written lines (scribbles) and two string holes."""
    cr.save()
    cr.push_group()
    cr.new_path()
    r = h / 2
    cr.arc(x - w / 2 + r, y, r, math.pi / 2, 3 * math.pi / 2)
    cr.arc(x + w / 2 - r, y, r, -math.pi / 2, math.pi / 2)
    cr.close_path()
    Y.ink_fill(cr, LEAF_COL, 5.0)
    if holes:
        for sd in (-1, 1):
            Y.dot(cr, x + sd * w * 0.33, y, 6, INK)
    for k in range(lines):
        yy = y - h * 0.28 + h * 0.56 * k / max(1, lines - 1)
        pts = [(xx, yy + 3 * math.sin(xx * 0.31 + k)) for xx in np.linspace(x - w * 0.42, x + w * 0.42, 30)]
        Y.stroke(cr, pts, 2.6, (0.35, 0.22, 0.10), alpha=0.75)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def book(cr, t, x, y, w, openp=1.0, alpha=1.0, glow_a=0.0):
    """The bundle of palm leaves between two painted wooden boards, tied with a string; openp 0..1 fans the top
    leaves up into a reading stack."""
    if alpha <= 0.01:
        return
    if glow_a > 0:
        Y.glow(cr, x, y - 40, w * 0.9, 0.5 * glow_a, (1.0, 0.85, 0.45))
    h = w * 0.16
    cr.save()
    cr.push_group()
    for sd in (1, -1):                                     # the two boards
        yy = y + sd * h * 0.42
        cr.rectangle(x - w / 2, yy - h * 0.14, w, h * 0.28)
        Y.ink_fill(cr, (0.55, 0.20, 0.08), 5.0)
        for k in range(5):
            Y.dot(cr, x - w * 0.4 + w * 0.2 * k, yy, h * 0.05, Y.GOLD, 2.0)
    for k in range(3):                                     # the bundle
        leaf(cr, x, y + h * (0.2 - 0.18 * k), w * 0.97, h * 0.34, lines=0)
    for k in range(4):                                     # leaves lifting up as it opens
        o = ease(clamp(openp * 1.6 - k * 0.2))
        if o <= 0:
            continue
        leaf(cr, x + 6 * k, y - h * 0.2 - o * (h * 0.55 + k * h * 0.42), w * 0.95, h * 0.36, lines=2)
    Y.stroke(cr, [(x - w * 0.33, y - h * 0.5), (x - w * 0.33, y + h * 0.5)], 4.0, Y.RED)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


# ------------------------------------------------------------------ the old TV round the stage


def tv_bezel(cr, t, rect, alpha=1.0, on=1.0):
    """A wooden TV set drawn round the screen rect (x0, y0, x1, y1): thick rounded frame, knobs, antenna; scan lines
    and a glass sheen over the picture inside."""
    x0, y0, x1, y1 = rect
    r = 60
    cr.save()
    cr.push_group()
    # the cabinet (everything outside the glass)
    cr.new_path()
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    _rrect(cr, x0 - 46, y0 - 46, x1 - x0 + 92, y1 - y0 + 170, r + 30)
    _rrect(cr, x0, y0, x1 - x0, y1 - y0, r)
    g = cairo.LinearGradient(0, y0 - 46, 0, y1 + 124)
    g.add_color_stop_rgb(0, 0.46, 0.25, 0.10)
    g.add_color_stop_rgb(1, 0.30, 0.15, 0.06)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(8)
    cr.stroke()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    _rrect(cr, x0 - 14, y0 - 14, x1 - x0 + 28, y1 - y0 + 28, r + 10)
    cr.set_source_rgb(0.14, 0.12, 0.12)
    cr.set_line_width(16)
    cr.stroke()
    _rrect(cr, x0 - 14, y0 - 14, x1 - x0 + 28, y1 - y0 + 28, r + 10)
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    for k, kx in enumerate((x0 + 70, x0 + 190)):           # knobs under the screen
        Y.dot(cr, kx, y1 + 66, 28, (0.85, 0.80, 0.70), 5.0)
        a = 0.8 + 1.4 * k
        Y.stroke(cr, [(kx, y1 + 66), (kx + 20 * math.cos(a), y1 + 66 + 20 * math.sin(a))], 6.0)
    for k in range(7):                                     # the speaker grille
        Y.stroke(cr, [(x1 - 330 + 44 * k, y1 + 44), (x1 - 330 + 44 * k, y1 + 92)], 8.0, (0.18, 0.09, 0.04))
    # the antenna
    ax, ay = (x0 + x1) / 2, y0 - 46
    Y.oval(cr, ax, ay - 6, 70, 34, (0.20, 0.17, 0.16), 5.0)
    for sd in (-1, 1):
        Y.stroke(cr, [(ax + sd * 20, ay - 30), (ax + sd * 230, ay - 150)], 7.0)
        Y.stroke(cr, [(ax + sd * 20, ay - 30), (ax + sd * 230, ay - 150)], 3.0, (0.75, 0.72, 0.68))
        Y.dot(cr, ax + sd * 230, ay - 150, 10, (0.75, 0.72, 0.68), 3.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    # scan lines and sheen on the glass
    cr.save()
    _rrect(cr, x0, y0, x1 - x0, y1 - y0, r)
    cr.clip()
    cr.set_source_rgba(0, 0, 0, 0.16 * alpha)
    for y in range(int(y0), int(y1), 6):
        cr.rectangle(x0, y, x1 - x0, 2)
    cr.fill()
    g = cairo.LinearGradient(x0, y0, x0 + 400, y0 + 500)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.20 * alpha)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    cr.set_source(g)
    cr.paint()
    if on < 1:
        cr.set_source_rgba(0.02, 0.02, 0.03, alpha * (1 - on))
        cr.paint()
        Y.glow(cr, (x0 + x1) / 2, (y0 + y1) / 2, 200 * on + 20, 0.8 * on * (1 - on) * 4)
    cr.restore()
    cr.restore()


def _rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def sepia(cr, a, rect=None):
    """An old-TV tint over a region (or the whole frame)."""
    if a <= 0.01:
        return
    cr.save()
    if rect:
        x0, y0, x1, y1 = rect
        cr.rectangle(x0, y0, x1 - x0, y1 - y0)
        cr.clip()
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.55 * a)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_SOFT_LIGHT)
    cr.set_source_rgba(0.85, 0.62, 0.30, 0.55 * a)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ gold, respect, envy


def coins(cr, t, x, y, s=1.0, alpha=1.0, n=26, seed=3):
    """A heap of gold coins (a pile of flat gold ovals), with a glint."""
    if alpha <= 0.01:
        return
    rng = np.random.default_rng(seed)
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-170, 0), (-120, -70), (-50, -120), (0, -134), (50, -120), (120, -70), (170, 0)], Y.GOLD_DK, 5.0)
    for k in range(n):
        u = rng.uniform(-1, 1)
        hy = -130 * (1 - abs(u) ** 1.5) * rng.uniform(0.3, 1.0)
        Y.oval(cr, 160 * u, hy, 30, 11, Y.GOLD, 3.5)
        Y.oval(cr, 160 * u, hy, 18, 6, Y.GOLD_HI, 0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()
    Y.sparkle(cr, x + 40 * s, y - 100 * s, 30 * s * (0.6 + 0.4 * math.sin(t * 5)), alpha)


def chest(cr, t, x, y, s=1.0, alpha=1.0):
    """An open chest of jewels."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-130, -150), (130, -150), (150, -230), (-150, -230)], (0.50, 0.20, 0.08), 6.0, smooth=False)  # lid
    for k, c in enumerate((Y.RED, Y.GREEN, Y.MIRROR, Y.RED, Y.BLUE, Y.GREEN)):
        Y.dot(cr, -100 + 40 * k, -150 - 14 * (k % 2), 16, c, 3.0)
    Y.oval(cr, 0, -150, 130, 30, Y.GOLD, 4.0)
    cr.rectangle(-140, -150, 280, 150)
    Y.ink_fill(cr, (0.55, 0.24, 0.10), 6.0)
    for xx in (-140, -40, 40, 140):
        Y.stroke(cr, [(xx, -150), (xx, 0)], 12.0, Y.GOLD, smooth=False)
    Y.oval(cr, 0, -80, 22, 26, Y.GOLD, 4.0)
    Y.dot(cr, 0, -76, 7, INK)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


ENVY = (0.30, 0.90, 0.30)


def green_fire(cr, t, x, y, s=1.0, a=1.0):
    """Hotte-kichchu, "stomach fire": a small flickering green fire (envy) with a glow."""
    if a <= 0.01:
        return
    Y.glow(cr, x, y - 30 * s, 220 * s, 0.55 * a, (0.30, 0.95, 0.30))
    for k, (dx, hh, w) in enumerate(((0, 1.0, 1.0), (-34, 0.7, 0.7), (34, 0.75, 0.7))):
        f = Y.noise1(t * 2.3, k * 1.7)
        hgt = (120 + 18 * f) * hh * s
        ww = 44 * w * s
        fx = x + dx * s
        sw = 10 * s * math.sin(t * 6 + k)
        for (kw, kh, col) in ((1.0, 1.0, (0.06, 0.45, 0.12)), (0.7, 0.78, (0.30, 0.86, 0.26)),
                              (0.38, 0.5, (0.85, 1.0, 0.70))):
            cr.new_path()
            cr.move_to(fx - ww * kw, y)
            cr.curve_to(fx - ww * kw, y - hgt * kh * 0.5, fx + sw, y - hgt * kh * 0.8, fx + sw * 1.5, y - hgt * kh)
            cr.curve_to(fx + sw, y - hgt * kh * 0.8, fx + ww * kw, y - hgt * kh * 0.5, fx + ww * kw, y)
            cr.curve_to(fx + ww * kw, y + 14 * s, fx - ww * kw, y + 14 * s, fx - ww * kw, y)
            cr.set_source_rgba(*col, a)
            if kw == 1.0:
                cr.fill_preserve()
                cr.set_source_rgba(*INK, a)
                cr.set_line_width(4 * s)
                cr.stroke()
            else:
                cr.fill()


def roots(cr, t, x, y, p, s=1.0, a=1.0, col=(0.45, 0.28, 0.12), spread=0.42):
    """Roots growing down and out from (x, y) as p goes 0..1 (the real root of the story)."""
    if p <= 0.01 or a <= 0.01:
        return
    rng = np.random.default_rng(9)
    for k in range(5):
        ang = math.pi / 2 + (k - 2) * spread + rng.uniform(-0.06, 0.06)
        L = (300 + 120 * rng.random()) * s * ease(clamp(p * 1.3 - 0.08 * abs(k - 2)))
        if L <= 2:
            continue
        pts = []
        for i in range(9):
            u = i / 8
            wob = 26 * s * math.sin(u * 6 + k * 1.7)
            pts.append((x + math.cos(ang) * L * u + wob * math.sin(ang), y + math.sin(ang) * L * u))
        w0 = (11 - 1.5 * abs(k - 2)) * s
        for i in range(len(pts) - 1):                      # tapering: thick at the heart, thin at the tip
            ww = w0 * (1 - 0.8 * i / (len(pts) - 1)) + 1.5
            Y.stroke(cr, pts[i:i + 2], ww + 6, INK, smooth=False, alpha=a)
        for i in range(len(pts) - 1):
            ww = w0 * (1 - 0.8 * i / (len(pts) - 1)) + 1.5
            Y.stroke(cr, pts[i:i + 2], ww, col, smooth=False, alpha=a)
        for j in (3, 5, 7):                                # little rootlets
            if j < len(pts):
                bx, by = pts[j]
                sd = 1 if (j + k) % 2 else -1
                tip = (bx + sd * 46 * s, by + 34 * s)
                Y.stroke(cr, [(bx, by), tip], 4.0 * s + 4, INK, smooth=False, alpha=a)
                Y.stroke(cr, [(bx, by), tip], 4.0 * s, col, smooth=False, alpha=a)


# ------------------------------------------------------------------ marks: cross, ring, tick, stamp, tags, laughs


def red_cross(cr, x, y, w, h, p, lw=26, alpha=1.0):
    """A painted red X over a box, the two strokes drawn one after the other."""
    if p <= 0.01:
        return
    for k, (a, b) in enumerate((((x - w / 2, y - h / 2), (x + w / 2, y + h / 2)),
                                ((x + w / 2, y - h / 2), (x - w / 2, y + h / 2)))):
        q = clamp(p * 2 - k)
        if q <= 0:
            continue
        e = (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)
        Y.stroke(cr, [a, e], lw + 12, INK, smooth=False, alpha=alpha)
        Y.stroke(cr, [a, e], lw, Y.RED, smooth=False, alpha=alpha)


def strike(cr, x0, x1, y, p, lw=18, alpha=1.0):
    if p <= 0.01:
        return
    xe = x0 + (x1 - x0) * clamp(p)
    pts = [(x0, y + 6), (xe, y - 6)]
    Y.stroke(cr, pts, lw + 10, INK, smooth=False, alpha=alpha)
    Y.stroke(cr, pts, lw, Y.RED, smooth=False, alpha=alpha)


def red_ring(cr, x, y, rx, ry, p, lw=12, alpha=1.0, rot=-0.05):
    if p <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(rx, ry)
    cr.new_path()
    a0 = -math.pi * 0.6
    cr.arc(0, 0, 1, a0, a0 + 2.15 * math.pi * clamp(p))
    cr.restore()
    path = cr.copy_path()
    cr.new_path()
    cr.append_path(path)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(lw + 8)
    cr.stroke()
    cr.append_path(path)
    cr.set_source_rgba(*Y.RED, alpha)
    cr.set_line_width(lw)
    cr.stroke()


def tick(cr, x, y, size, p, col=(0.15, 0.62, 0.20), alpha=1.0):
    if p <= 0.01:
        return
    a, b, c = (x - size * 0.45, y), (x - size * 0.1, y + size * 0.38), (x + size * 0.5, y - size * 0.42)
    q1, q2 = clamp(p * 2), clamp(p * 2 - 1)
    pts = [a, (a[0] + (b[0] - a[0]) * q1, a[1] + (b[1] - a[1]) * q1)]
    if q2 > 0:
        pts.append((b[0] + (c[0] - b[0]) * q2, b[1] + (c[1] - b[1]) * q2))
    Y.stroke(cr, pts, size * 0.2 + 10, INK, smooth=False, alpha=alpha)
    Y.stroke(cr, pts, size * 0.2, col, smooth=False, alpha=alpha)


def stamp(cr, t, t0, lines, x, y, rot=-0.08, col=Y.RED, max_w=760):
    """A rubber stamp slamming on: a red double frame with Kannada lines [(text, size), ...], big then settling."""
    q = clamp((t - t0) / 0.28)
    if q <= 0:
        return None
    k = 1.0 + 0.6 * (1 - ease(q))
    surfs = [Y.kn_surface(tx, int(sz), tuple(col), tuple(Y.WHITE), 6.0, tuple(INK), 4.0) for tx, sz in lines]
    tw = max(s.get_width() for s in surfs)
    th = sum(s.get_height() for s in surfs) + 6 * (len(surfs) - 1)
    w, h = tw + 70, th + 50
    fit = min(1.0, max_w / w)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k * fit, k * fit)
    cr.push_group()
    for lw, c in ((22, INK), (12, col)):
        _rrect(cr, -w / 2, -h / 2, w, h, 18)
        cr.set_source_rgb(*c)
        cr.set_line_width(lw)
        cr.stroke()
    _rrect(cr, -w / 2 + 3, -h / 2 + 3, w - 6, h - 6, 16)
    cr.set_source_rgba(*Y.WHITE, 0.92)
    cr.fill()
    _rrect(cr, -w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 10)
    cr.set_source_rgb(*col)
    cr.set_line_width(4)
    cr.stroke()
    yy = -th / 2
    for s in surfs:
        cr.set_source_surface(s, -s.get_width() / 2, yy)
        cr.paint()
        yy += s.get_height() + 6
    cr.pop_group_to_source()
    cr.paint_with_alpha(clamp(q * 3))
    cr.restore()
    return x - w * fit / 2, y - h * fit / 2, w * fit, h * fit


def tag(cr, t, t0, text, x, y, size=58, col=Y.CREAM, field=Y.MAROON, alpha=1.0, max_w=420):
    """A small painted name plate (dark cloth, gold rim, cream Kannada) popping in at t0, centred on (x, y)."""
    q = clamp((t - t0) / 0.3)
    if q <= 0 or alpha <= 0.01:
        return
    s = Y.kn_surface(text, int(size), tuple(col), tuple(INK), 5.0, None, 0.0)
    fit = min(1.0, max_w / (s.get_width() + 40))
    w, h = (s.get_width() + 40) * fit, (s.get_height() + 18) * fit
    x = min(max(x, 60 + w / 2), W - 60 - w / 2)          # inside the safe margins
    k = 0.6 + 0.4 * back(q, 2.0)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.push_group()
    _rrect(cr, -w / 2, -h / 2, w, h, 14)
    Y.ink_fill(cr, field, 5.0)
    _rrect(cr, -w / 2 + 7, -h / 2 + 7, w - 14, h - 14, 9)
    cr.set_source_rgb(*Y.GOLD)
    cr.set_line_width(3)
    cr.stroke()
    cr.scale(fit, fit)
    cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha * clamp(q * 3))
    cr.restore()


def laugh(cr, t, t0, x, y, size=54, side=1, alpha=1.0):
    """'ಹ ಹ ಹ!' bursting out beside a laughing face, bobbing."""
    q = clamp((t - t0) / 0.3)
    if q <= 0 or alpha <= 0.01:
        return
    bob = 8 * math.sin((t - t0) * 14)
    k = 0.5 + 0.5 * back(q, 2.4)
    cr.save()
    cr.translate(x, y + bob)
    cr.rotate(side * 0.10)
    cr.scale(k, k)
    for i in range(3):                                     # little burst lines
        a = -math.pi / 2 + side * (0.5 + 0.35 * i)
        Y.stroke(cr, [(-side * 70 + 40 * math.cos(a), 40 * math.sin(a)),
                      (-side * 70 + 64 * math.cos(a), 64 * math.sin(a))], 5.0, Y.YEL, alpha=alpha * clamp(q * 3))
    Y.kn_text(cr, "ಹ ಹ ಹ!", 0, 0, size, Y.YEL, INK, 6, alpha=alpha * clamp(q * 3))
    cr.restore()


def big_q(cr, t, t0, x, y, size=300, alpha=1.0):
    """A big red question mark with a cream outline, popping in and rocking."""
    q = clamp((t - t0) / 0.4)
    if q <= 0:
        return
    k = 0.4 + 0.6 * back(q, 2.2)
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.06 * math.sin((t - t0) * 2.5))
    cr.scale(k, k)
    Y.kn_text(cr, "?", 0, 0, size, Y.RED, Y.CREAM, 12, INK, 9, alpha=alpha * clamp(q * 3))
    cr.restore()


def bubble(cr, t, t0, x, y, w, h, tail_to, alpha=1.0, field=Y.WHITE):
    """A thought cloud (puffy outline) with three little puffs trailing to tail_to; returns nothing."""
    q = clamp((t - t0) / 0.35)
    if q <= 0 or alpha <= 0.01:
        return
    k = 0.4 + 0.6 * back(q, 1.8)
    cr.save()
    cr.push_group()
    tx, ty = tail_to
    for i in range(3):
        u = (i + 1) / 4
        Y.dot(cr, tx + (x - tx) * u * 0.7, ty + (y + h / 2 - ty) * u * 0.7, 10 + 6 * i, field, 4.0)
    cr.translate(x, y)
    cr.scale(k, k)
    n = 12
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append(((w / 2) * math.cos(a), (h / 2) * math.sin(a)))
    cr.new_path()
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        p0 = ((w / 2) * math.cos(a0), (h / 2) * math.sin(a0))
        p1 = ((w / 2) * math.cos(a1), (h / 2) * math.sin(a1))
        am = (a0 + a1) / 2
        c = ((w / 2 + 34) * math.cos(am), (h / 2 + 34) * math.sin(am))
        if i == 0:
            cr.move_to(*p0)
        cr.curve_to(c[0], c[1], c[0], c[1], *p1)
    cr.close_path()
    Y.ink_fill(cr, field, 6.0)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha * clamp(q * 3))
    cr.restore()


def card(cr, t, t0, lines, x, y, w, h, field=Y.CRIMSON, rot=0.0, alpha=1.0, ring=0.0):
    """A painted choice card (gold frame, crimson field) with Kannada lines [(text, size, colour), ...] centred; a red
    ring round it when ring > 0."""
    q = clamp((t - t0) / 0.4)
    if q <= 0 or alpha <= 0.01:
        return
    k = 0.6 + 0.4 * back(q, 1.8)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    cr.push_group()
    _rrect(cr, -w / 2 + 10, -h / 2 + 14, w, h, 22)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    _rrect(cr, -w / 2, -h / 2, w, h, 22)
    Y.ink_fill(cr, Y.GOLD, 7.0)
    _rrect(cr, -w / 2 + 18, -h / 2 + 18, w - 36, h - 36, 14)
    Y.ink_fill(cr, field, 5.0)
    surfs = [Y.kn_surface(tx, int(sz), tuple(col), tuple(INK), 6.0, None, 0.0) for tx, sz, col in lines]
    th = sum(s.get_height() for s in surfs) + 8 * (len(surfs) - 1)
    yy = -th / 2
    for s in surfs:
        f = min(1.0, (w - 70) / s.get_width())
        cr.save()
        cr.translate(0, yy + s.get_height() * f / 2)
        cr.scale(f, f)
        cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
        cr.paint()
        cr.restore()
        yy += s.get_height() * f + 8
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha * clamp(q * 3))
    cr.restore()
    if ring > 0.01:
        red_ring(cr, x, y, w * 0.62, h * 0.66, 1.0, 14, ring, rot - 0.04)
