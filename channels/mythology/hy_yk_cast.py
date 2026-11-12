"""Extra looks, props and text pieces for the Kannada (Yakshagana) hanuman_curse reel (scenes_hanuman_curse_yk), built
on yaksha_kit without changing it: the painted red-gold sun (that turns into a fruit), Indra's vajra, a palm-leaf
book, the sages' hut and the things the child throws, painted thera fields (a dawn sky, the ocean with Lanka), the
blue wave cloth across the front of the stage, small cloth tags, rings, arrows, dotted jump arcs, dust and splashes.

Everything is flat paint with thick black outlines, like the kit. Coordinates are frame pixels (1080x1920) unless a
function says "units".
"""
import functools
import math

import cairo
import numpy as np

import yaksha_kit as Y
from poster import H, W, back, clamp, ease

INK, RED, GOLD, CREAM, WHITE = Y.INK, Y.RED, Y.GOLD, Y.CREAM, Y.WHITE
FIELD = (134, 664, 946, 1586)            # the painted field of the thera (inside its border): x0, y0, x1, y1

# ------------------------------------------------------------------ extra looks (new dicts from the kit's looks)

Y.FACES.setdefault("hy_vanara_a", dict(base=(0.66, 0.40, 0.20), mark="namam", muzzle=WHITE, ruff=(0.95, 0.80, 0.52),
                                       patch=WHITE))
Y.FACES.setdefault("hy_vanara_b", dict(base=(0.80, 0.55, 0.16), mark="namam", muzzle=WHITE, ruff=(1.0, 0.92, 0.70),
                                       patch=WHITE))
INDRA = dict(Y.GOD)                                                     # the king of the gods
GOD2 = dict(Y.GOD, jacket=RED, sleeve=RED, kase=(RED, Y.YEL, INK, Y.GREEN), disc_cols=(GOLD, Y.GREEN, RED))
VANARA_A = dict(Y.HANUMAN, face="hy_vanara_a", crown="kireeta_small", disc=False, jacket=Y.BLUE, sleeve=Y.BLUE,
                kase=(Y.GREEN, Y.YEL, INK, RED), hem=RED, tail=(0.62, 0.36, 0.18), hand=(0.70, 0.46, 0.26))
VANARA_B = dict(Y.HANUMAN, face="hy_vanara_b", crown="kireeta_small", disc=False, jacket=(0.50, 0.12, 0.42),
                sleeve=(0.50, 0.12, 0.42), kase=(RED, Y.YEL, INK, Y.BLUE), hem=Y.BLUE, tail=(0.78, 0.52, 0.16),
                hand=(0.84, 0.60, 0.26))
VALMIKI = dict(Y.SAGE, cloth=WHITE, cloth2=Y.SAFF)
HANUMAN_PLAIN = dict(Y.HANUMAN, crown="kireeta_small", disc=False)     # the years he forgot: no big crown, no halo


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def pulse(t, t0, dur=0.35):
    """0 -> 1 -> 0 bump starting at t0."""
    u = (t - t0) / dur
    return math.sin(math.pi * u) if 0 < u < 1 else 0.0


def hop(t, t0, dur=0.5, h=1.0):
    """A little jump: 0 outside, up to h in the middle."""
    u = (t - t0) / dur
    return h * 4 * u * (1 - u) if 0 < u < 1 else 0.0


# ------------------------------------------------------------------ the painted sun (and the fruit it turns into)


def sun_disc(cr, t, x, y, r, fruit=0.0, alpha=1.0, glow_a=1.0, spin=0.12):
    """The sun painted like a Yakshagana prop: a ring of flame petals round a gold rim, red disc, a ring of gold dots,
    a saffron heart. fruit 0..1 turns it into a sweet red fruit: the petals and rings melt away, a stem and a green
    leaf grow on top, a white shine appears."""
    if alpha <= 0.01:
        return
    if alpha < 0.999:
        cr.push_group()
    Y.glow(cr, x, y, r * 3.4, 0.42 * glow_a * (1 - 0.5 * fruit), (1.0, 0.50, 0.12))
    Y.glow(cr, x, y, r * 1.8, 0.35 * glow_a * (1 - 0.6 * fruit), (1.0, 0.75, 0.30))
    cr.save()
    cr.translate(x, y)
    k = r / 100.0
    cr.scale(k, k)
    pk = 1 - fruit
    if pk > 0.03:                                       # flame petals
        cr.save()
        cr.rotate(t * spin)
        n = 18
        for i in range(n):
            a = 2 * math.pi * i / n
            L = (176 if i % 2 == 0 else 148) * pk + 96 * (1 - pk)
            cr.save()
            cr.rotate(a)
            Y.shape(cr, [(-24, -88), (-18, -112), (-7, -L + 18), (0, -L), (7, -L + 18), (18, -112), (24, -88)],
                    (GOLD if i % 2 == 0 else Y.SAFF), 5.0)
            cr.restore()
        cr.restore()
    # the body: round sun -> a fruit with a little dip at the top
    dip = 14 * fruit
    body = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        rr = 100 - dip * max(0.0, math.cos(a + math.pi / 2)) ** 6 * 1.6
        body.append((rr * math.cos(a) * (1 + 0.04 * fruit), rr * math.sin(a)))
    if pk > 0.03:
        Y.dot(cr, 0, 0, 100 + 4 * pk, GOLD, 6.0)         # the gold rim
    Y.shape(cr, body if fruit > 0.02 else [(86 * math.cos(2 * math.pi * i / 48), 86 * math.sin(2 * math.pi * i / 48))
                                          for i in range(48)], mix(RED, (0.88, 0.10, 0.10), fruit), 6.0)
    if pk > 0.03:
        cr.push_group()
        for i in range(30):                             # the ring of gold dots
            a = 2 * math.pi * i / 30
            Y.dot(cr, 72 * math.cos(a), 72 * math.sin(a), 4.5, Y.GOLD_HI, 1.6)
        Y.dot(cr, 0, 0, 56, Y.VERM, 4.5)
        Y.dot(cr, 0, 0, 36, Y.SAFF, 3.5)
        for i in range(12):                             # a lotus heart
            a = 2 * math.pi * i / 12
            cr.save()
            cr.rotate(a)
            Y.shape(cr, [(-7, -12), (0, -34), (7, -12)], Y.YEL, 2.2)
            cr.restore()
        Y.dot(cr, 0, 0, 13, Y.GOLD_HI, 2.5)
        cr.pop_group_to_source()
        cr.paint_with_alpha(pk)
    if fruit > 0.02:
        q = ease(clamp(fruit * 1.3))
        cr.save()                                       # the shine
        cr.new_path()
        cr.arc(-30, -34, 42, math.pi * 1.05, math.pi * 1.55)
        cr.set_source_rgba(1, 1, 1, 0.85 * q)
        cr.set_line_width(14)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
        Y.dot(cr, -56, -6, 6 * q, (1, 1, 1))
        cr.restore()
        g = back(clamp((fruit - 0.25) / 0.75), 2.0)     # the stem and the leaf grow
        if g > 0.01:
            cr.save()
            cr.translate(0, -92)
            cr.scale(g, g)
            Y.inked_line(cr, [(0, 0), (4, -30), (14, -56)], 11, (0.45, 0.25, 0.10))
            Y.shape(cr, [(8, -36), (40, -70), (90, -74), (118, -54), (84, -30), (40, -24)], Y.LEAF, 5.0)
            Y.stroke(cr, [(14, -38), (60, -52), (110, -56)], 3.5, Y.DLEAF)
            cr.restore()
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


# ------------------------------------------------------------------ Indra's vajra


def vajra(cr, x, y, s, rot=0.0, alpha=1.0, glow_a=0.0, t=0.0):
    """The thunderbolt weapon: a gold grip with a red gem, a bulb at each end and three prongs meeting in a point.
    About 320 units long along its own y axis."""
    if alpha <= 0.01:
        return
    if glow_a > 0.01:
        Y.glow(cr, x, y, 260 * s, 0.6 * glow_a, (1.0, 0.85, 0.45))
        Y.rays(cr, t, x, y, 40 * s, 300 * s, 0.6 * glow_a, 14, (1.0, 0.90, 0.55), 0.3)
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    for sd in (-1, 1):
        cr.save()
        cr.scale(1, sd)
        for px in (-1, 1):                              # the curved side prongs
            Y.inked_line(cr, [(px * 20, 72), (px * 46, 100), (px * 44, 132), (px * 16, 158), (0, 166)], 11, GOLD,
                         3.5)
        Y.shape(cr, [(-8, 80), (0, 172), (8, 80)], GOLD, 4.0, smooth=False)       # the middle prong
        Y.oval(cr, 0, 66, 30, 22, GOLD, 5.0)                                       # the bulb
        Y.stroke(cr, [(-26, 66), (26, 66)], 4.0, RED)
        Y.shape(cr, [(-14, 24), (14, 24), (18, 46), (-18, 46)], GOLD, 4.5, smooth=False)
        cr.restore()
    Y.shape(cr, [(-12, -26), (12, -26), (12, 26), (-12, 26)], Y.GOLD_DK, 4.5, smooth=False)   # the grip
    Y.dot(cr, 0, 0, 20, GOLD, 4.5)
    Y.oval(cr, 0, 0, 10, 12, RED, 2.5)
    Y.dot(cr, 3, -4, 3, WHITE)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


# ------------------------------------------------------------------ the palm-leaf book (Valmiki's Ramayana)


@functools.lru_cache(maxsize=4)
def _title(text, size):
    return Y.kn_surface(text, size, (0.30, 0.12, 0.05), (0.30, 0.12, 0.05), 0.0, None, 0.0)


def palm_book(cr, t, x, y, s, open_=1.0, title="ರಾಮಾಯಣ", alpha=1.0, glow_a=0.0):
    """A palm-leaf manuscript (ole gari) held flat: a stack of long leaves between two wooden covers, a string through
    them. open_ lifts the top cover away and shows the title written on the top leaf."""
    if alpha <= 0.01:
        return
    if glow_a > 0.01:
        Y.glow(cr, x, y - 40 * s, 420 * s, 0.45 * glow_a, (1.0, 0.80, 0.40))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    leaf = (0.93, 0.80, 0.52)
    wood = (0.50, 0.20, 0.08)
    for k in range(4):                                  # the bottom cover and the stack
        yy = 34 - 9 * k
        Y.shape(cr, [(-250, yy - 22), (250, yy - 22), (262, yy), (250, yy + 22), (-250, yy + 22), (-262, yy)],
                wood if k == 0 else leaf, 5.0, smooth=False)
    Y.shape(cr, [(-250, -36), (250, -36), (262, -10), (250, 16), (-250, 16), (-262, -10)], leaf, 5.0, smooth=False)
    for xx in (-200, 200):                              # the string holes
        Y.dot(cr, xx, -10, 9, (0.30, 0.14, 0.06), 2.5)
    if open_ > 0.3:
        tx = _title(title, 64)
        a = clamp((open_ - 0.3) / 0.4)
        sc = min(1.0, 330 / tx.get_width())
        cr.save()
        cr.translate(-tx.get_width() * sc / 2, -10 - tx.get_height() * sc / 2)
        cr.scale(sc, sc)
        cr.set_source_surface(tx, 0, 0)
        cr.paint_with_alpha(a)
        cr.restore()
    Y.stroke(cr, [(-200, -10), (-232, 30), (-250, 70), (-236, 104)], 4.0, RED)   # the string and a bead
    Y.dot(cr, -236, 108, 10, GOLD, 3.0)
    lift = ease(open_)                                  # the top cover lifts up and swings away to the back
    if lift < 0.98:
        cr.save()
        cr.translate(250, -36)
        cr.rotate(-1.9 * lift)
        cr.translate(-250, 36)
        Y.shape(cr, [(-250, -58), (250, -58), (262, -36), (250, -14), (-250, -14), (-262, -36)], wood, 5.0,
                smooth=False)
        for xx in (-120, 0, 120):
            Y.dot(cr, xx, -36, 7, GOLD, 2.5)
        cr.restore()
    cr.restore()


# ------------------------------------------------------------------ the hermitage hut and the things in it


def hut(cr, x, y, s, alpha=1.0, shake=0.0):
    """A sage's thatched hut standing on the stage line y (units: about 460 wide, 420 tall)."""
    if alpha <= 0.01:
        return
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(0.02 * shake)
    mud = (0.78, 0.48, 0.24)
    Y.shape(cr, [(-180, 0), (-180, -210), (180, -210), (180, 0)], mud, 6.0, smooth=False)
    for k in range(5):                                  # a painted band of white dots and red triangles (rangoli)
        xx = -150 + 75 * k
        Y.shape(cr, [(xx - 18, -30), (xx, -62), (xx + 18, -30)], RED, 3.0, smooth=False)
    Y.dot_row(cr, [(-170, -18), (170, -18)], 16, 4.0, WHITE)
    cr.new_path()                                       # the doorway
    cr.move_to(-58, 0)
    cr.line_to(-58, -120)
    cr.curve_to(-58, -176, 58, -176, 58, -120)
    cr.line_to(58, 0)
    cr.close_path()
    Y.ink_fill(cr, (0.20, 0.10, 0.05), 5.0)
    Y.stroke(cr, [(-58, -120), (-58, 0)], 5.0, Y.GOLD_DK)
    Y.stroke(cr, [(58, -120), (58, 0)], 5.0, Y.GOLD_DK)
    straw, straw_dk = (0.90, 0.70, 0.30), (0.62, 0.42, 0.14)
    roof = [(-250, -170), (-200, -238), (-110, -340), (0, -420), (110, -340), (200, -238), (250, -170), (120, -190),
            (0, -196), (-120, -190)]
    Y.shape(cr, roof, straw, 7.0)
    for k in range(-6, 7):                              # thatch lines
        Y.stroke(cr, [(k * 6, -400), (k * 34, -200 + abs(k) * 2)], 3.0, straw_dk)
    for k in range(3):                                  # tied bands
        yy = -230 - 60 * k
        w = 200 - 62 * k
        Y.stroke(cr, [(-w, yy + 18), (0, yy - 8), (w, yy + 18)], 7.0, straw_dk)
    Y.stroke(cr, [(0, -420), (0, -470)], 5.0, (0.40, 0.22, 0.10))                 # a little saffron flag
    Y.shape(cr, [(0, -470), (60, -452), (0, -434)], Y.SAFF, 3.5, smooth=False)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


def item(cr, kind, x, y, s, rot=0.0):
    """One of the sages' things (units, centred): pot, ladle, bundle (palm leaves), lamp, bowl."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    copper = (0.78, 0.38, 0.14)
    if kind == "pot":
        Y.shape(cr, [(-26, -60), (26, -60), (22, -44), (52, -14), (58, 20), (40, 52), (0, 62), (-40, 52), (-58, 20),
                     (-52, -14), (-22, -44)], copper, 5.0)
        Y.stroke(cr, [(-50, 0), (50, 0)], 5.0, GOLD)
        Y.oval(cr, 0, -60, 30, 8, (0.55, 0.25, 0.08), 4.0)
        Y.dot_row(cr, [(-44, 22), (44, 22)], 6, 3.0, WHITE)
    elif kind == "ladle":
        Y.inked_line(cr, [(0, -80), (0, 40)], 10, (0.62, 0.38, 0.16))
        Y.oval(cr, 0, 58, 26, 22, (0.62, 0.38, 0.16), 5.0)
        Y.oval(cr, 0, 54, 16, 12, (0.40, 0.22, 0.08), 0)
    elif kind == "bundle":
        for k in range(3):
            Y.shape(cr, [(-80, -14 + 8 * k), (80, -14 + 8 * k), (86, -4 + 8 * k), (80, 6 + 8 * k), (-80, 6 + 8 * k),
                         (-86, -4 + 8 * k)], (0.93, 0.80, 0.52) if k else (0.50, 0.20, 0.08), 4.0, smooth=False)
        Y.stroke(cr, [(-50, -20), (-50, 30)], 4.0, RED)
        Y.stroke(cr, [(50, -20), (50, 30)], 4.0, RED)
    elif kind == "bowl":
        Y.shape(cr, [(-56, -10), (56, -10), (42, 22), (0, 34), (-42, 22)], copper, 5.0)
        for k in range(4):
            Y.dot(cr, -30 + 20 * k, -16, 12, (Y.SAFF, RED, Y.YEL, Y.SAFF)[k], 3.0)   # flowers
    elif kind == "kamandalu":
        Y.stroke(cr, [(-26, -40), (0, -64), (26, -40)], 6.0, (0.45, 0.25, 0.10))
        Y.shape(cr, [(-30, -36), (30, -36), (44, 0), (36, 36), (0, 48), (-36, 36), (-44, 0)], (0.62, 0.36, 0.14), 5.0)
        Y.stroke(cr, [(-40, -4), (40, -4)], 4.0, GOLD)
        Y.stroke(cr, [(38, -10), (66, -28), (74, -38)], 6.0, (0.62, 0.36, 0.14))
    cr.restore()


# ------------------------------------------------------------------ painted thera fields


def field_clip(cr):
    x0, y0, x1, y1 = FIELD
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()


def cloud(cr, x, y, s, col=(1.0, 0.93, 0.80), alpha=1.0):
    """A painted folk-art cloud: round puffs with a curl, outlined."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if alpha < 0.999:
        cr.push_group()
    pts = [(-120, 20), (-128, -6), (-100, -30), (-70, -26), (-56, -56), (-16, -68), (18, -54), (40, -74),
           (84, -66), (100, -36), (128, -24), (134, 8), (110, 24)]
    Y.shape(cr, pts, col, 5.0)
    for cx, cy, r in ((-60, -4, 18), (20, -22, 22), (86, -8, 16)):
        cr.new_path()
        cr.arc(cx, cy, r, math.pi * 0.9, math.pi * 2.1)
        cr.set_source_rgba(*INK, 0.65)
        cr.set_line_width(3.5)
        cr.stroke()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    cr.restore()


@functools.lru_cache(maxsize=4)
def sky_surface(kind="dawn"):
    """The thera's field painted as a sky (cached): a deep blue top fading to saffron, painted stars, flat clouds."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    x0, y0, x1, y1 = FIELD
    field_clip(cr)
    g = cairo.LinearGradient(0, y0, 0, y1)
    if kind == "dawn":
        g.add_color_stop_rgb(0, 0.10, 0.12, 0.40)
        g.add_color_stop_rgb(0.45, 0.42, 0.20, 0.42)
        g.add_color_stop_rgb(0.80, 0.95, 0.48, 0.22)
        g.add_color_stop_rgb(1, 0.99, 0.70, 0.30)
    else:                                               # a plain day sky
        g.add_color_stop_rgb(0, 0.12, 0.30, 0.62)
        g.add_color_stop_rgb(1, 0.55, 0.78, 0.92)
    cr.set_source(g)
    cr.paint()
    rng = np.random.default_rng(3)
    for _ in range(40):                                 # painted stars, top only
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y0 + 300)
        Y.sparkle(cr, x, y, rng.uniform(5, 10), 0.5)
    for (cx, cy, sc) in ((260, 820, 0.8), (690, 1060, 0.55)):
        cloud(cr, cx, cy, sc, (1.0, 0.86, 0.72) if kind == "dawn" else WHITE)
    s.flush()
    return s


@functools.lru_cache(maxsize=2)
def hills_surface():
    """Two rows of painted green hills along the bottom of the thera's field (cached)."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    x0, y0, x1, y1 = FIELD
    field_clip(cr)
    for k, (col, base, amp) in enumerate((((0.10, 0.42, 0.20), 1420, 70), ((0.04, 0.30, 0.15), 1490, 50))):
        pts = [(x0 - 20, y1 + 20)]
        for i in range(13):
            xx = x0 - 20 + (x1 - x0 + 40) * i / 12
            pts.append((xx, base - amp * math.sin(i * 1.3 + k * 2.0) ** 2))
        pts.append((x1 + 20, y1 + 20))
        Y.shape(cr, pts, col, 5.0)
        for i in range(9):                              # little painted trees on the hills
            xx = x0 + 40 + (x1 - x0 - 80) * (i + 0.3 * k) / 8.5
            yy = base - amp * math.sin(((xx - x0 + 20) / (x1 - x0 + 40) * 12) * 1.3 + k * 2.0) ** 2 + 6
            Y.stroke(cr, [(xx, yy + 8), (xx, yy - 22)], 4.0, (0.30, 0.16, 0.06))
            Y.oval(cr, xx, yy - 34, 16, 20, Y.LEAF if k == 0 else (0.10, 0.50, 0.22), 3.5)
    s.flush()
    return s


def sky_field(cr, kind="dawn", hills=True):
    cr.set_source_surface(sky_surface(kind), 0, 0)
    cr.paint()
    if hills:
        hills_field(cr)


def hills_field(cr):
    cr.set_source_surface(hills_surface(), 0, 0)
    cr.paint()


def ocean_disc(cr, t, x, y, r, alpha=1.0):
    """A little round painting of the sea (waves in a gold ring), small enough to sit on a palm."""
    if alpha <= 0.01:
        return
    cr.push_group()
    Y.dot(cr, x, y, r + 8, GOLD, 4.0)
    cr.save()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.clip()
    cr.set_source_rgb(0.55, 0.70, 0.90)
    cr.paint()
    k = r / 100.0
    for j, (yy, amp, wl, col) in enumerate(((-20, 12, 60, (0.10, 0.36, 0.66)), (20, 16, 80, (0.06, 0.28, 0.58)),
                                            (60, 20, 100, (0.04, 0.22, 0.50)))):
        wave_row(cr, t, y + yy * k, amp * k, wl * k, col, WHITE, (12 + 6 * j) * k, x - r - 40, x + r + 40,
                 y + r + 10, 3.0)
    cr.restore()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)


def medallion(cr, t, x, y, r, p=1.0, inner=None):
    """A round painted picture (a memory) in a gold ring with mirror dots; it pops in as p goes 0 -> 1 and
    inner(cr) paints what is inside (already clipped)."""
    if p <= 0.01:
        return
    k = 0.3 + 0.7 * back(clamp(p), 1.8)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.translate(-x, -y)
    cr.push_group()
    Y.glow(cr, x, y, r * 1.8, 0.5, (1.0, 0.80, 0.40))
    n = 24
    for i in range(n):
        a = 2 * math.pi * i / n
        Y.dot(cr, x + (r + 18) * math.cos(a), y + (r + 18) * math.sin(a), 16, GOLD, 4.0)
    Y.dot(cr, x, y, r + 12, GOLD, 5.0)
    cr.save()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.clip()
    if inner:
        inner(cr)
    cr.restore()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    for i in range(36):
        a = 2 * math.pi * (i + 0.5) / 36
        Y.dot(cr, x + (r + 6) * math.cos(a), y + (r + 6) * math.sin(a), 3.2, Y.MIRROR, 1.4)
    cr.pop_group_to_source()
    cr.paint_with_alpha(clamp(p * 3))
    cr.restore()


def name_split(cr, t, t_in, parts, cx, y, size=168, max_w=960, alpha=1.0):
    """A big word painted in parts of different colours (e.g. HANU in red + MANTHA in yellow), in the headline's big
    style, popping in at t_in; top at y. Returns the box of each part."""
    q = clamp((t - t_in) / 0.38)
    if q <= 0:
        return []
    surfs = [Y.kn_surface(tx, int(size), tuple(col), tuple(CREAM), 9.0, tuple(INK), 7.0) for tx, col in parts]
    lap = 14.0
    tw = sum(s.get_width() for s in surfs) - lap * (len(surfs) - 1)
    hh = max(s.get_height() for s in surfs)
    fit = min(1.0, max_w / tw)
    k = fit * (0.55 + 0.45 * back(q, 2.2))
    cr.save()
    cr.translate(cx, y + hh * fit / 2)
    cr.scale(k, k)
    xx = -tw / 2
    boxes = []
    for s in surfs:
        cr.set_source_surface(s, xx, -hh / 2 + (hh - s.get_height()) / 2)
        cr.get_source().set_filter(cairo.FILTER_GOOD)
        cr.paint_with_alpha(clamp(q * 2.5) * alpha)
        boxes.append((cx + xx * k, y + hh * fit / 2 - hh / 2 * k, s.get_width() * k, hh * k))
        xx += s.get_width() - lap
    cr.restore()
    return boxes


def lanka(cr, t, x, y, s, glow_a=0.0):
    """Lanka far over the sea: a green island with a golden fort, flags, (optionally) a warm light where Sita is."""
    if glow_a > 0.01:
        Y.glow(cr, x, y - 60 * s, 260 * s, 0.55 * glow_a, (1.0, 0.85, 0.45))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-220, 10), (-160, -40), (-60, -66), (60, -70), (170, -44), (230, 10)], (0.10, 0.45, 0.22), 6.0)
    fort = (0.98, 0.76, 0.22)
    for (fx, fw, fh) in ((-110, 46, 150), (-40, 40, 200), (40, 48, 250), (120, 40, 170)):
        Y.shape(cr, [(fx - fw, -50), (fx - fw, -fh), (fx + fw, -fh), (fx + fw, -50)], fort, 5.0, smooth=False)
        Y.shape(cr, [(fx - fw - 6, -fh), (fx, -fh - 56), (fx + fw + 6, -fh)], (0.92, 0.42, 0.10), 5.0)
        Y.stroke(cr, [(fx, -fh - 56), (fx, -fh - 92)], 4.0, INK)
        Y.shape(cr, [(fx, -fh - 92), (fx + 34, -fh - 82), (fx, -fh - 72)], RED, 3.0, smooth=False)
        for wy in range(int(-fh + 40), -60, 46):
            Y.shape(cr, [(fx - 10, wy + 22), (fx - 10, wy), (fx, wy - 10), (fx + 10, wy), (fx + 10, wy + 22)],
                    (0.40, 0.14, 0.06), 2.5, smooth=False)
    cr.restore()


def wave_row(cr, t, y, amp, wl, col, foam=WHITE, speed=20.0, x0=-40, x1=W + 40, bottom=None, lw=5.0):
    """One row of painted waves: a band with scalloped crests and a white curl on each crest."""
    ph = (t * speed) % wl
    bottom = H + 40 if bottom is None else bottom
    pts = [(x0 - wl + ph, bottom)]
    n = int((x1 - x0) / wl) + 3
    crests = []
    for i in range(n * 8 + 1):
        u = i / 8.0
        xx = x0 - wl + u * wl + ph
        f = u % 1.0
        yy = y - amp * (math.sin(math.pi * f) ** 0.6)
        pts.append((xx, yy))
        if i % 8 == 4:
            crests.append((xx, yy))
    pts.append((x1 + wl, bottom))
    cr.new_path()
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    Y.ink_fill(cr, col, lw)
    for cx, cy in crests:                               # foam curls
        cr.new_path()
        cr.arc(cx + amp * 0.25, cy + amp * 0.55, amp * 0.42, math.pi * 1.0, math.pi * 2.05)
        cr.set_source_rgb(*foam)
        cr.set_line_width(max(3.0, amp * 0.16))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
        Y.dot(cr, cx - amp * 0.7, cy + amp * 0.9, max(2.0, amp * 0.07), foam)


SEA_TOP = 930                                           # the painted horizon on the ocean thera


def ocean_field(cr, t, lanka_a=1.0, lanka_glow=0.0, lanka_xy=(800, 935, 0.42)):
    """The thera's field painted as the sea: a sky over the horizon with clouds, Lanka on the far right, rows of
    waves getting bigger toward the front."""
    cr.save()
    field_clip(cr)
    x0, y0, x1, y1 = FIELD
    g = cairo.LinearGradient(0, y0, 0, SEA_TOP)
    g.add_color_stop_rgb(0, 0.10, 0.20, 0.50)
    g.add_color_stop_rgb(1, 0.55, 0.62, 0.80)
    cr.set_source(g)
    cr.rectangle(x0, y0, x1 - x0, SEA_TOP - y0)
    cr.fill()
    cloud(cr, 300, 760, 0.7, WHITE)
    cloud(cr, 640, 700, 0.5, WHITE)
    if lanka_a > 0.01:
        lx, ly, ls = lanka_xy
        lanka(cr, t, lx, ly, ls, lanka_glow)
    cr.rectangle(x0, SEA_TOP, x1 - x0, y1 - SEA_TOP)
    cr.set_source_rgb(0.04, 0.22, 0.48)
    cr.fill()
    rows = ((SEA_TOP + 18, 10, 60, (0.10, 0.36, 0.64)), (SEA_TOP + 80, 16, 90, (0.07, 0.30, 0.58)),
            (SEA_TOP + 170, 24, 130, (0.05, 0.26, 0.54)), (SEA_TOP + 300, 34, 170, (0.04, 0.22, 0.50)),
            (SEA_TOP + 460, 46, 220, (0.03, 0.18, 0.44)))
    for k, (yy, amp, wl, col) in enumerate(rows):
        wave_row(cr, t, yy, amp, wl, col, (0.85, 0.95, 1.0), 14 + 6 * k * (1 if k % 2 else -1), x0 - 40, x1 + 40,
                 y1 + 10, 4.0)
    cr.restore()


def wave_cloth(cr, t, y=1700, x0=-40, x1=W + 40, alpha=1.0):
    """The blue sea cloth across the front of the stage (two rows, held low, rippling)."""
    if alpha <= 0.01:
        return
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.rectangle(x0, 0, x1 - x0, H)
    cr.clip()
    wave_row(cr, t, y, 46, 210, (0.10, 0.42, 0.78), WHITE, -26, x0, x1)
    wave_row(cr, t + 1.3, y + 70, 54, 250, (0.05, 0.30, 0.66), WHITE, 32, x0, x1)
    cr.restore()
    if x0 > 0:                                          # the rolled-up end of the cloth, held upright
        bob = 6 * math.sin(t * 2.6)
        Y.shape(cr, [(x0 - 22, y - 70 + bob), (x0 + 22, y - 70 + bob), (x0 + 22, H + 20), (x0 - 22, H + 20)],
                (0.06, 0.32, 0.70), 6.0, smooth=False)
        for k in range(5):
            yy = y - 40 + bob + 60 * k
            Y.stroke(cr, [(x0 - 20, yy), (x0 + 20, yy + 10)], 4.0, (0.03, 0.18, 0.45))
        Y.oval(cr, x0, y - 70 + bob, 22, 9, (0.30, 0.55, 0.90), 5.0)
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)


# ------------------------------------------------------------------ marks, arrows, arcs, dust


def red_ring(cr, x, y, rx, ry, p, w=9.0, alpha=1.0):
    """A hand-drawn red ring drawn round (x, y) as p goes 0 -> 1."""
    if p <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(rx, ry)
    cr.new_path()
    a0 = -math.pi * 0.6
    cr.arc(0, 0, 1.0, a0, a0 + 2 * math.pi * 1.06 * ease(p))
    cr.restore()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    path = cr.copy_path()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(w + 7)
    cr.stroke()
    cr.append_path(path)
    cr.set_source_rgba(0.92, 0.10, 0.08, alpha)
    cr.set_line_width(w)
    cr.stroke()


def arrow(cr, p0, p1, p, bend=0.25, w=12.0, col=CREAM, alpha=1.0):
    """A curved painted arrow from p0 to p1, drawn as p goes 0 -> 1."""
    if p <= 0.01:
        return
    (ax, ay), (bx, by) = p0, p1
    mx, my = (ax + bx) / 2 - (by - ay) * bend, (ay + by) / 2 + (bx - ax) * bend
    n = 30
    m = max(2, int(n * ease(p)))
    pts = []
    for i in range(m + 1):
        u = i / n
        pts.append(((1 - u) ** 2 * ax + 2 * u * (1 - u) * mx + u * u * bx,
                    (1 - u) ** 2 * ay + 2 * u * (1 - u) * my + u * u * by))
    cr.push_group()
    Y.stroke(cr, pts, w + 9, INK, smooth=False)
    Y.stroke(cr, pts, w, col, smooth=False)
    (x2, y2), (x1_, y1_) = pts[-1], pts[-3]
    a = math.atan2(y2 - y1_, x2 - x1_)
    cr.save()
    cr.translate(x2, y2)
    cr.rotate(a)
    Y.shape(cr, [(18, 0), (-22, -22), (-12, 0), (-22, 22)], col, 5.0, smooth=False)
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)


def arc_pts(p0, p1, lift, n=60, u1=1.0):
    (ax, ay), (bx, by) = p0, p1
    out = []
    for i in range(n + 1):
        u = u1 * i / n
        out.append((ax + (bx - ax) * u, ay + (by - ay) * u - lift * 4 * u * (1 - u)))
    return out


def dotted_arc(cr, p0, p1, lift, p, r=7.0, col=CREAM, alpha=1.0, gap=34.0):
    """A dotted jump arc from p0 to p1, drawn out as p goes 0 -> 1."""
    if p <= 0.01:
        return
    pts = arc_pts(p0, p1, lift, 120, ease(p))
    L = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    nd = max(1, int(L / gap))
    for x, y in Y.along(pts, nd):
        cr.new_path()
        cr.arc(x, y, r + 3, 0, 2 * math.pi)
        cr.set_source_rgba(*INK, alpha)
        cr.fill()
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(*col, alpha)
        cr.fill()


def big_x(cr, x, y, r, p, alpha=1.0):
    """A big red X, its two strokes drawn one after the other."""
    for k, (a, b) in enumerate((((-1, -1), (1, 1)), ((1, -1), (-1, 1)))):
        q = ease(clamp(p * 2 - k))
        if q <= 0:
            continue
        p0 = (x + a[0] * r, y + a[1] * r)
        p1 = (p0[0] + (b[0] - a[0]) * r * q, p0[1] + (b[1] - a[1]) * r * q)
        Y.stroke(cr, [p0, p1], 46, INK, smooth=False, alpha=alpha)
        Y.stroke(cr, [p0, p1], 32, (0.92, 0.10, 0.08), smooth=False, alpha=alpha)


def dust(cr, t, t0, x, y, s=1.0, dur=0.9):
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


def splash(cr, t, t0, x, y, s=1.0, dur=0.8):
    """Water jumping up where something falls into the sea."""
    u = (t - t0) / dur
    if not 0 < u < 1:
        return
    for k in range(9):
        a = math.pi * (0.15 + 0.7 * k / 8)
        d = (30 + 170 * ease(u)) * s
        px, py = x + d * math.cos(a) * 0.9, y - d * math.sin(a) * 1.3 + 260 * u * u * s
        Y.oval(cr, px, py, 12 * s * (1 - 0.5 * u), 18 * s * (1 - 0.5 * u), (0.85, 0.95, 1.0), 3.0)
    Y.oval(cr, x, y, 90 * s * (0.5 + u), 18 * s, (0.85, 0.95, 1.0), 3.0)


def qmark(cr, t, t_in, x, y, size, alpha=1.0, wobble=True):
    """A big red question mark that pops in at t_in."""
    q = clamp((t - t_in) / 0.4)
    if q <= 0:
        return
    k = 0.4 + 0.6 * back(q, 2.4)
    cr.save()
    cr.translate(x, y)
    if wobble:
        cr.rotate(0.06 * math.sin(t * 3.0))
    Y.kn_text(cr, "?", 0, 0, size, (0.90, 0.08, 0.06), CREAM, 10, INK, 9, alpha=alpha * clamp(q * 3), scale=k)
    cr.restore()


def tag(cr, t, t_in, text, x, y, size=60, field=Y.MAROON, col=CREAM, alpha=1.0, max_w=520):
    """A small painted cloth label naming someone or something."""
    return Y.kn_banner(cr, t, t_in, [(text, size, col)], x, y, rot=-0.02, field=field, alpha=alpha, quote=False,
                       pad=(46, 36), max_w=max_w)


def burst_rays(cr, t, x, y, a, r1=1100, n=26, col=(1.0, 0.78, 0.30)):
    Y.rays(cr, t, x, y, 100, r1, a, n, col, 0.05)
    Y.glow(cr, x, y, r1 * 0.6, 0.35 * a, (1.0, 0.70, 0.30))
