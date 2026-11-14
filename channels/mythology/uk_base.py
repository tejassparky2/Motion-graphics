"""Shared pieces for the Uttara Kanda long video (videos/uttar_kand.py, landscape 1920x1080): figures with their feet on
the ground line, sets, a Hindi label for every sentence, and small effects. The shots live in uk_shots_a / uk_shots_b;
scenes_uttar_kand puts them together with the fast camera (camera_beats) and the sound.

Cast (reused, one look each all video): Rama, Sita, Lakshmana (lrekha_cast / kaikeyi_cast), Bharata, Valmiki (the
white-bearded sage Pulastya puppet), Lava and Kusha (the boy puppet, two of them, one with a green sash tint), Durvasa
(the fiery sage Bhrigu puppet), Vasishtha (the old sage puppet), Kaal (a dark ascetic, with Yama's shadow at the
reveal), the Earth goddess (mrityu_cast EARTH), Hanuman, Brahma, Janaka, and townspeople.
"""
import math

import cairo

import andhe_cast  # noqa: F401  (pillars, arch, water)
import arjuna_cast  # noqa: F401  (thought bubble)
import ashtavakra_cast as AV
import bhrigu_cast as BG
import dharmavyadha_cast as DV
import jatayu_cast  # noqa: F401  (chariot, pyre)
import kaikeyi_cast as K
import lrekha_cast as L
import manthara_cast  # noqa: F401  (city, veena, fan)
import mrityu_cast as MR
import puppet_cast as PC
import puppet_core as pc
import ravana_cast as R
import ruru_cast as RU
import six_cast_c  # noqa: F401  (cradle, book, Brahma)
from poster import clamp, draw_text, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet
from scenes_arjuna import HAS_INDIC, indic_surface
from scenes_ashtavakra2 import PARCH, hcard, red_spot
from scenes_hanuman_curse import arc_path, orb, qmark, trail
from scenes_jarasandha import INK, RED, bob_rot, glow, man_angles, red_ring, walk_legs, woman_angles
from scenes_kaikeyi import ANJALI, BOW, fig
from scenes_lakshman_rekha import LK_BOW
from scenes_lakshman_rekha import HEART, sparkle
from scenes_mandhata import burst, lights, warm
from scenes_manthara import puffs
from shots import T

GL = 1000                      # the ground line (feet)
S0 = 0.62                      # a grown-up figure's usual scale (about 600 px tall)
ANJ = dict(front=ANJALI["front"], backa=ANJALI["backa"])
TINT_LAVA = (0.70, 1.0, 0.75)


# ------------------------------------------------------------------ timing


def ls(tl, line):
    """Start of a script line."""
    return T(tl, line)


def lf(tl, line, f):
    """A fraction of the way through a line."""
    return T(tl, line, f)


def le(tl, line):
    return tl[line].end


# ------------------------------------------------------------------ figures (feet on GL unless given)


def man(cr, t, rig, key, x, s=S0, feet=GL, **kw):
    kw.setdefault("ph", x * 0.003)
    return fig(cr, rig, key, t, x, s, feet=feet, **kw)


def woman(cr, t, rig, key, x, s=S0, feet=GL, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False,
          alpha=1.0, blur=0.0, rot=0.0, rods=True, ph=None, y=None):
    ang = woman_angles(key, t, front, backa, head, hits, x * 0.003 if ph is None else ph)
    hy = feet - 470 * s if y is None else y
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, x * 0.003), flip, ang, alpha, blur, rods=rods)


def rama(cr, t, x, s=S0, **kw):
    kw.setdefault("extra", BOW)
    return man(cr, t, K.RAMA, "rama", x, s, **kw)


def lakshmana(cr, t, x, s=S0, **kw):
    kw.setdefault("extra", LK_BOW)
    return man(cr, t, L.LAKSHMANA, "lakshmana", x, s, **kw)


def bharata(cr, t, x, s=S0, **kw):
    return man(cr, t, K.BHARATA, "bharata", x, s, **kw)


def sita(cr, t, x, s=S0, **kw):
    return woman(cr, t, L.SITA, "sita", x, s, **kw)


def earth(cr, t, x, s=S0, **kw):
    return woman(cr, t, MR.EARTH, "mr_earth", x, s, **kw)


def valmiki(cr, t, x, s=S0, **kw):
    return man(cr, t, R.PULASTYA, "pulastya", x, s, **kw)


def durvasa(cr, t, x, s=S0, **kw):
    return man(cr, t, BG.BHRIGU, "bg_bhrigu", x, s, **kw)


def vasishtha(cr, t, x, s=S0, **kw):
    return man(cr, t, PC.SAGE, "sage", x, s, **kw)


def kaal(cr, t, x, s=S0, **kw):
    """Death as an ascetic: the old sage puppet, darkened."""
    return man(cr, t, PC.SAGE, "sage", x, s, **kw)


def yama(cr, t, x, s=S0, **kw):
    return man(cr, t, RU.YAMA, "rr_yama", x, s, **kw)


def hanuman(cr, t, x, s=S0, **kw):
    return man(cr, t, R.HANUMAN, "hanuman", x, s, **kw)


def janaka(cr, t, x, s=S0, **kw):
    return man(cr, t, AV.JANAKA, "av_janaka", x, s, **kw)


def boy(cr, t, x, s=0.42, **kw):
    return man(cr, t, AV.BOY, "av_boy", x, s, **kw)


TOWN = ((DV.HUS, "dv_hus"), (DV.KAU, "dv_kau"), (DV.VY, "dv_vy"), (DV.BFA, "dv_bfa"), (DV.KFA, "dv_kfa"))
TOWN_W = ((DV.WIFE, "dv_wife"), (DV.BMO, "dv_bmo"), (DV.KMO, "dv_kmo"))


def townsfolk(cr, t, xs, s=0.5, feet=GL, flip=False, alpha=1.0, blur=2.0, front=(-0.3, -0.5), hits=()):
    """A row of townspeople (men and women in turn)."""
    for i, x in enumerate(xs):
        if i % 3 == 2:
            rig, key = TOWN_W[i % len(TOWN_W)]
            woman(cr, t, rig, key, x, s * 0.95, feet=feet, flip=flip, alpha=alpha, blur=blur, rods=False, hits=hits)
        else:
            rig, key = TOWN[i % len(TOWN)]
            man(cr, t, rig, key, x, s, feet=feet, flip=flip, alpha=alpha, blur=blur, rods=False, front=front,
                hits=hits)


def walker(cr, t, fn, t0, t1, x0, x1, s=S0, feet=GL, step=0.42, **kw):
    """A man() figure walking in rod-puppet steps."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    return fn(cr, t, x, s, legs=walk_legs(ph), rot=rock, y=feet - 434 * s + bob, **kw), x


# ------------------------------------------------------------------ sets


def ground(cr, y=GL, col=(0.50, 0.32, 0.16), a=0.85):
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    pc.poly(cr, [(-300, y - 6), (W + 300, y + 6), (W + 300, H + 300), (-300, H + 300)])
    cr.set_source_rgba(*col, a)
    cr.fill()
    cr.restore()


def palace(cr, alpha=1.0):
    """Inside the palace: carved pillars and an arch."""
    for x in (120, 1800):
        prop(cr, "ak_pillar", x, GL, 0.85, alpha=0.8 * alpha, blur=3)
    prop(cr, "ak_arch", 960, 150, 1.1, alpha=0.55 * alpha, blur=5)
    ground(cr, col=(0.55, 0.30, 0.18), a=0.7 * alpha)


def forest(cr, t, trees=((140, 0.62, 6, 0.8, True), (1780, 0.66, 4, 0.85, False), (1500, 0.45, 12, 0.5, True)),
           hut=None):
    L_forest = __import__("scenes_lakshman_rekha").forest
    hx, hs = hut if hut else (1500, 0.6)
    L_forest(cr, t, feet=GL, hut_x=hx, hut_s=hs, trees=trees, hut_a=1.0 if hut else 0.0)


def river(cr, t, y=GL - 10, h=170, col=(0.30, 0.52, 0.85), a=0.7):
    """A river band with moving ripple lines (the Ganga, the Sarayu)."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(-300, y, W + 600, h)
    cr.set_source_rgba(*col, a)
    cr.fill()
    cr.restore()
    cr.save()
    for k in range(5):
        yy = y + 22 + k * h / 5
        cr.move_to(-300, yy)
        for i in range(0, W + 600, 40):
            cr.line_to(-300 + i, yy + 6 * math.sin(i * 0.02 + t * 2 + k))
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.35)
        cr.set_line_width(3)
        cr.stroke()
    cr.restore()


def sky(cr, t, glow_a=0.8):
    glow(cr, 960, 360, 900, glow_a)
    for x, y, s_ in ((260, 300, 0.9), (1660, 260, 0.8), (980, 160, 0.7)):
        puffs(cr, x + 30 * math.sin(t * 0.3 + x), y, s_, 0.5)


def bubble(cr, t, t_in, x, y, s=1.4, t_out=None):
    """A thought bubble fading in at t_in; returns its alpha."""
    q = prog(t, t_in, 0.35)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    if q > 0.01:
        prop(cr, "ar_think", x, y, s * (0.9 + 0.1 * ease(q)), alpha=q)
    return q


def notes(cr, t, x, y, a=1.0):
    """Music notes rising (the boys singing)."""
    for i in range(5):
        u = (t * 0.5 + i / 5) % 1.0
        draw_text(cr, "♪", x + 40 * math.sin(i * 2.1 + t), y - 220 * u, 64, INK, a * math.sin(math.pi * u),
                  anchor="cm")


def petals(cr, t, t0, x0, x1, a=1.0, n=26):
    """Flowers raining down from t0."""
    if t < t0:
        return
    for i in range(n):
        u = ((t - t0) * 0.35 + i / n) % 1.0
        x = x0 + (x1 - x0) * ((i * 0.37) % 1.0) + 30 * math.sin(t + i)
        y = -40 + 1100 * u
        cr.new_path()
        cr.arc(x, y, 9, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.55 + 0.3 * (i % 2), 0.2, 0.85 * a * prog(t, t0, 0.5))
        cr.fill()


def card(cr, t, t_in, x, y, big, small, a=1.0):
    hcard(cr, t, t_in, x, y, big, small, a)


def book(cr, t, t_in, x, y, s=1.4, glow_a=1.0):
    q = prog(t, t_in, 0.4)
    if q > 0.01:
        warm(cr, x, y, 260 * s, q * glow_a)
        lights(cr, t, x, y, 180 * s, 10, q * glow_a)
        prop(cr, "c6_veda", x, y, s * (0.85 + 0.15 * ease(q)), -0.05, alpha=q)


# ------------------------------------------------------------------ labels: one per sentence


PARCH_ = PARCH


def label(cr, t, t_in, text, t_out, x=960, y=110, size=72, col=INK, under=False):
    """A short Hindi label on a parchment strip (the idea of the sentence being said)."""
    if not HAS_INDIC or t < t_in:
        return
    q = prog(t, t_in, 0.25) * (1 - prog(t, t_out, 0.2))
    if q <= 0.01:
        return
    su = indic_surface(text, size, col)
    w_, h_ = su.get_width(), su.get_height()
    pad = 0.36 * size
    yy = y + 18 * (1 - ease(q))
    cr.save()
    cr.translate(x, yy)
    pts = [(-w_ / 2 - pad, -h_ / 2 - 14), (w_ / 2 + pad, -h_ / 2 - 14), (w_ / 2 + pad + 14, 0), (w_ / 2 + pad, h_ / 2 + 14),
           (-w_ / 2 - pad, h_ / 2 + 14), (-w_ / 2 - pad - 14, 0)]
    pc.poly(cr, pts)
    cr.set_source_rgba(*PARCH, 0.97 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, q)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_source_surface(su, -w_ / 2, -h_ / 2)
    cr.paint_with_alpha(q)
    if under:
        u = prog(t, t_in + 0.3, 0.3)
        cr.move_to(-w_ / 2, h_ / 2 + 4)
        cr.line_to(-w_ / 2 + w_ * u, h_ / 2 + 4)
        cr.set_source_rgba(*RED, q)
        cr.set_line_width(6)
        cr.stroke()
    cr.restore()


pc.register("uk_lk_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, L.LK_SKIN, L.LK_DHOTI, K.GOLD, 1.0))
pc.register("uk_rama_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, K.RAMA_SKIN, K.GOLD, K.DRED, 1.05))
pc.register("uk_hanu_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, R.HANU_FUR, K.RED, K.GOLD, 1.2))
