"""The leather cast, props and the landscape stage for stories 3 and 4 of the long video (videos/six_stories.py,
1920x1080): Agastya who drank the ocean (lines g1-g11) and Rishyashringa, the boy who had never seen a woman (s1-s13).
Togalu Gombeyaata leather shadow puppets in the style of the reels (puppet_cast, ruru_cast, mandhata_cast,
kaikeyi_cast ...): profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather
puppets, modelled on no actor and no film.

The stage: puppet_core's cloth screen is lit for the 1080x1920 reels (its lamp sits low on the left of a landscape
frame), so this module paints the wide cloth and lamp of scenes_six_b (same recipe and numbers: the lamp low in the
middle, a second small lamp over the headline, weave, panel seams, creases, oil stains), so all six stories match.

Cast (one look each, kept the same through both stories):
  AGASTYA       short, stout and strong: dark warm skin, a huge white beard and moustache, long white hair, white
                matted hair piled up with rudraksha, ash lines, a round belly, a saffron dhoti; his kamandalu (a brass
                water pot with a spout and a looped handle). Faces: calm, smile, drink (eyes shut, mouth open).
  INDRA         mandhata_cast's Indra (pale gold, a ring of rays, the vajra). DEVA1 / DEVA2: two gods with gold kirita
                crowns and flame halos (blue and green dhotis); they carry small hand lamps.
  KALAKEYAS     asuras, always shown as dark shadows (scenes draw them through a silhouette): heavy bodies, clawed hands,
                three kinds of horns (bull, swept-back spikes, curled ram), eyes and tusks cut through the leather so
                the lamp shines out of them.
  BRAHMA        three faces showing (the fourth is behind): a frontal face and two profiles, white beards, one wide crown,
                a ring of golden rays; golden skin, a red dhoti; seated cross-legged on a lotus; a palm-leaf Veda.
  BHAGIRATHA    a king in white with a saffron border and sash, a gold kirita with a saffron halo; eyes shut in prayer.
  GANGA         the river goddess: pale skin, a white blouse, a queen's crown, a ring of pale-blue rays; from the waist
                down she is a ribbon of river water (drawn per frame in the scenes).
  RISHYASHRINGA a forest boy: bark-brown clothes, long untidy hair with a top-knot tied by a green vine, a rudraksha
                mala and, on his forehead, a small ivory horn. Faces: calm, puzzled, smile, wonder.
  VIBHANDAKA    his father, a lean sage: grey beard and hair, grey matted hair piled up, a deer-skin across the chest.
  DOE           a spotted doe (spots punched through), her head on its own pivot so she can nod and nuzzle.
  CITY WOMEN    three women in bright saris (pink, orange, violet), jasmine and flowers in their hair, a nose ring,
                a plate of sweets shaped like fruits.
  LOMAPADA      the king of Anga (green, a gold kirita, a moustache). SHANTA: the princess in a red sari, gold.
  BRAHMINS      two priests (white, saffron, top-knots, the sacred thread; the elder has a white beard).
  VILLAGERS     a farmer with a red turban and a village woman (sad, and dancing in the rain).
  DASHARATHA    kaikeyi_cast's Dasharatha, kneeling at the fire (his kneeling legs are registered here).
  BABY RAMA     a small blue baby asleep in a decorated cradle (a prop).
Props: ocean wave strips that scroll, the sandy sea floor, stranded fish, shells and a starfish, a shore rock, the
rim of Patala's hole, a hand lamp, the boat-hermitage (hut + hull), cracked and wet earth,
dead and green crops, a wide grass strip, the plate of sweets, the fruit-shaped sweet and its two halves (a laddu
inside), a small Veda bundle. The tree, hut, clouds, sun, moon, lotus, throne, garland, altar, flames and the
palm-leaf book come from the earlier casts.
"""
import functools
import math
import random

import cairo
import numpy as np
from scipy.ndimage import gaussian_filter

import arjuna_cast as A  # noqa: F401
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (palm-leaf book boards and leaves, speech cloud, leaf hut)
import mandhata_cast as M
import puppet_core as pc
import ravana_cast as R
import ruru_cast as RU
from puppet_cast import HAIR, _flower, _jewel, _shape, man, man_body, man_head, woman, woman_body, woman_head
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, RED, ROSE, SAFFRON,
                         almond_eye, band, cut, dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet,
                         spath)

W, H = pc.W, pc.H

# ------------------------------------------------------------------ colours

AG_SKIN = (0.82, 0.54, 0.32)          # Agastya
AG_WHITE = (0.96, 0.95, 0.91)         # his hair and beard
AG_STRAND = (0.66, 0.64, 0.62)
AG_DHOTI = (0.97, 0.58, 0.16)
AG_DHOTI2 = (1.0, 0.78, 0.38)
BRASS = (0.92, 0.66, 0.24)
KALA = (0.26, 0.18, 0.28)             # the asuras' dye (they are drawn as silhouettes)
SIL = (0.09, 0.05, 0.10)              # their shadow colour
BR_SKIN = (1.0, 0.76, 0.42)           # Brahma
BH_SKIN = (0.97, 0.72, 0.48)          # Bhagiratha
GA_SKIN = (1.0, 0.90, 0.80)           # Ganga
GA_BLUE = (0.66, 0.84, 1.0)
WATER = (0.50, 0.75, 1.0)
WATER2 = (0.30, 0.56, 0.95)
FOAM = (0.93, 0.97, 1.0)
WAVES = ((0.66, 0.85, 1.0), (0.48, 0.72, 1.0), (0.32, 0.57, 0.95), (0.22, 0.43, 0.86))
RS_SKIN = (0.96, 0.74, 0.50)          # Rishyashringa
HORN = (1.0, 0.94, 0.80)
BARK = (0.66, 0.45, 0.24)
BARK2 = (0.48, 0.31, 0.15)
VINE = (0.36, 0.64, 0.26)
VB_SKIN = (0.80, 0.56, 0.36)          # Vibhandaka
GREY = (0.62, 0.60, 0.58)
GREY2 = (0.40, 0.38, 0.38)
DEERSKIN = (0.88, 0.68, 0.42)
DOE = (0.88, 0.60, 0.32)
DOE2 = (0.99, 0.90, 0.74)
LP_SKIN = (0.96, 0.70, 0.46)          # Lomapada
LP_GREEN = (0.20, 0.56, 0.36)
SH_SKIN = (0.99, 0.80, 0.62)          # Shanta
BRM_SKIN = (0.96, 0.76, 0.54)         # the Brahmins
FM_SKIN = (0.80, 0.52, 0.30)          # the farmer
SAND = (0.97, 0.85, 0.58)
SAND2 = (0.86, 0.68, 0.40)
EARTH = (0.88, 0.66, 0.40)
EARTH2 = (0.70, 0.48, 0.26)
WET = (0.56, 0.42, 0.26)
LEAF = (0.98, 0.86, 0.56)
LEAF2 = (0.86, 0.66, 0.34)
WOOD = K.WOOD
RAMA_SKIN = (0.36, 0.56, 0.92)
WAVE_P = 200.0                         # wave strip period (design units): they scroll seamlessly
SEAT_H = 96.0                          # seated cross-legged: hip above the ground


# ------------------------------------------------------------------ the landscape cloth screen and lamp
# The same wide cloth and lamp as scenes_six_b (stage_surface / lamp / title_lift), copied here so the sibling modules
# stay independent: all six stories are lit the same.

LAMP = (960.0, 1000.0)                 # the oil lamp behind the cloth (wide frame)


@functools.lru_cache(maxsize=1)
def screen_surface():
    """puppet_core.screen_surface's backlit cloth, laid out for the wide frame: the oil lamp low in the middle, a second
    small lamp lighting the headline, two stitched panel seams, gentle creases and a few oil stains."""
    rng = np.random.default_rng(1729)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - LAMP[0]) / 1150.0
    dy = (yy - LAMP[1]) / 1250.0
    d2 = dx * dx + dy * dy
    lum = np.exp(-1.55 * d2 ** 1.15)
    hx, hy = (xx - 960) / 900.0, (yy - 150) / 330.0
    lum = lum + 0.30 * np.exp(-(hx * hx + hy * hy) ** 1.1) * (1 - 0.6 * lum)
    lum *= 1 + 0.025 * pc._smooth_noise(rng, (H // 8 + 1, W // 8 + 1), 9).repeat(8, 0).repeat(8, 1)[:H, :W]
    fib = pc._smooth_noise(rng, (H, W), 0.8) * 0.010
    slub = gaussian_filter(rng.normal(0, 1, (H, W // 16 + 1)).astype(np.float32), (0.6, 2.0)).repeat(16, 1)[:, :W]
    slub = slub / (slub.std() + 1e-6) * 0.012
    tex = 1 + fib + slub
    for sx in (330.0, 1590.0):
        d = xx - sx - 6 * np.sin(yy / 260.0)
        tex *= 1 - 0.07 * np.exp(-(d / 2.2) ** 2)
        tex *= 1 + 0.03 * np.exp(-((d - 5) / 5.0) ** 2)
        st = (np.abs(d) < 2.5) & ((yy.astype(np.int32) // 9) % 2 == 0)
        tex *= np.where(st, 0.93, 1.0)
    for (x0, y0, ang, wdt, k) in ((560, 340, 1.35, 30, 0.03), (1400, 760, 1.75, 40, 0.03), (980, 160, 1.5, 24, 0.02)):
        nx, ny = math.cos(ang), math.sin(ang)
        d = (xx - x0) * ny - (yy - y0) * nx
        along = np.exp(-(((xx - x0) * nx + (yy - y0) * ny) / 700.0) ** 2)
        tex *= 1 - k * along * np.exp(-(d / wdt) ** 2) + 0.6 * k * along * np.exp(-((d - wdt) / wdt) ** 2)
    stain = np.zeros((H, W), np.float32)
    for (sx, sy, r, k) in ((150, 930, 120, 0.10), (1760, 230, 90, 0.07), (1660, 990, 70, 0.08), (90, 420, 60, 0.05)):
        stain += k * np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (r * r)) ** 1.5)
    stops = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    cols = np.array([(0.03, 0.012, 0.006), (0.24, 0.10, 0.04), (0.62, 0.36, 0.15), (0.90, 0.68, 0.40),
                     (0.98, 0.88, 0.66), (1.0, 0.96, 0.84)])
    lc = np.clip(lum, 0, 1.05)
    img = np.stack([np.interp(lc, stops, cols[:, c]) for c in range(3)], -1).astype(np.float32)
    img *= tex[..., None]
    img *= (1 - stain[..., None] * np.array([0.45, 0.65, 0.95], np.float32))
    a = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    return pc.surface_from_rgba(a)


def screen(cr):
    cr.set_source_surface(screen_surface(), 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint()


def lamp(cr, t, night=0.0, flash=0.0):
    """puppet_core.lamp for the wide frame: flicker, a drifting warm hot spot, a night tint, a flash of lamp light."""
    f = pc.flicker(t)
    lx = LAMP[0] + 20 * math.sin(t * 1.3) + 8 * math.sin(t * 3.1)
    ly = LAMP[1] - 60 + 10 * math.sin(t * 0.9 + 1)
    hs, n = pc._hotspot()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(lx, ly)
    cr.scale(1400 / n, 1000 / n)
    cr.set_source_surface(hs, -n, -n)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(pc.clamp(0.10 + 0.05 * f))
    cr.restore()
    if night > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_rgba(0.40, 0.48, 0.78, pc.clamp(night))
        cr.paint()
        cr.restore()
    dark = 0.05 + 0.035 * f
    if dark > 0:
        cr.set_source_rgba(0.02, 0.01, 0.0, pc.clamp(dark))
        cr.paint()
    if flash > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.translate(960, 760)
        cr.scale(2300 / n, 1500 / n)
        cr.set_source_surface(hs, -n, -n)
        cr.get_source().set_filter(cairo.FILTER_BILINEAR)
        cr.paint_with_alpha(pc.clamp(flash) * 0.5)
        cr.restore()


def title_lift(cr, a):
    """In the dark shots the small lamp over the headline stays lit, so the words read."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(960, 150)
    cr.scale(1.0, 0.24)
    g = cairo.RadialGradient(0, 0, 60, 0, 0, 1050)
    g.add_color_stop_rgba(0, 1.0, 0.93, 0.76, 0.55 * a)
    g.add_color_stop_rgba(0.6, 1.0, 0.90, 0.70, 0.3 * a)
    g.add_color_stop_rgba(1, 1.0, 0.88, 0.66, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ small shared pieces


def _mala(cr, b=1.0, n=12):
    for i in range(n):
        u = i / (n - 1)
        x, y = -24 + (70 * b) * u, -276 + 150 * u * u + 40 * u
        cr.new_path()
        cr.arc(x, y, 7, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()


def _jata(cr, col, n=5, dy=30, x0=-6, y0=-196, w0=52, line=INK):
    """Matted hair piled up in rolls on top of the head, tied with a row of rudraksha beads."""
    for k in range(n):
        cr.new_path()
        ell(cr, x0 - 3 * k, y0 - dy * k, w0 - 5 * k, 22)
        leather(cr, col, 4)
        ink(cr, [(x0 - 34 + 6 * k, y0 - dy * k), (x0, y0 + 10 - dy * k), (x0 + 36 - 6 * k, y0 - 2 - dy * k)], 2.5,
            col=line)
    for i in range(7):
        cr.new_path()
        cr.arc(-44 + 14 * i, -178, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)


def _ash_lines(cr, x0=6, x1=46, y=-172):
    for k in range(3):
        ink(cr, [(x0, y + 9 * k), (x1, y + 2 + 9 * k)], 3.2, col=(1.0, 0.97, 0.9))


def _cover(cr, skin, x, y, rx, ry):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    cr.set_source_rgb(*skin)
    cr.fill()


def seat_legs(cr, skin, cloth, border):
    """Cross-legged in profile (hip at 0, 0; the ground at y = +SEAT_H), as ruru_cast._khag_seat."""
    th = [(-80, -30), (40, -44), (160, -32), (250, -10), (266, 40), (250, 86), (120, 96), (-40, 96), (-92, 70),
          (-96, 14)]
    _shape(cr, th, cloth, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(246, -8), (266, 40), (250, 86)], 14, border, spacing=11, hole_r=2.4)
    band(cr, [(-84, 88), (240, 90)], 10, border, holes=False)
    foot = [(104, 8), (150, -6), (204, 0), (222, 22), (196, 38), (118, 40)]
    _shape(cr, foot, skin, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 4), (x + 4, 18)], 2.2)
    rivet(cr, 0, 0, 9)


def body_sit(o):
    """A man() body with the front pleats tucked away (they would hang into the ground when he sits)."""
    def fn(cr):
        cr.save()
        cr.rectangle(-400, -600, 800, 664)
        cr.clip()
        man_body(cr, o)
        cr.restore()
    return fn


# ------------------------------------------------------------------ Agastya


_AG_O = dict(skin=AG_SKIN, hair=False, moustache=False, tilak=False, earring=False)
_AG = dict(skin=AG_SKIN, bulk=1.22, dhoti=AG_DHOTI, border=DRED, pleat=AG_DHOTI2, sash=OCHRE, neck=BROWN, beads=True)


def agastya_head(cr, mood="calm"):
    """A huge white beard and moustache, long white hair, white matted hair piled up with rudraksha, bushy white brows,
    ash lines. mood: calm | smile | drink (eyes shut, the mouth open as the ocean pours in)."""
    hp = [(-26, -178), (-70, -156), (-104, -80), (-114, 20), (-100, 110), (-70, 136), (-50, 64), (-42, -30),
          (-24, -100)]
    _shape(cr, hp, AG_WHITE, 5)
    for k in range(4):
        ink(cr, [(-50 - 12 * k, -146 + 6 * k), (-80 - 8 * k, -30), (-74 - 6 * k, 96)], 2.4, col=AG_STRAND)
    RU.rface(cr, _AG_O, {"drink": "sleep"}.get(mood, mood))
    bp = [(60, -56), (76, -40), (86, -4), (88, 44), (80, 96), (64, 146), (46, 190), (30, 222), (14, 192), (0, 228),
          (-14, 188), (-28, 200), (-36, 150), (-42, 96), (-40, 40), (-30, -10), (-16, -44), (6, -40), (30, -52)]
    _shape(cr, bp, AG_WHITE, 4.5)
    for k in range(5):
        x0 = 60 - 17 * k
        ink(cr, [(x0, -26), (x0 + 6, 40), (x0 - 4, 110), (x0 + 2, 176 - 12 * abs(k - 2))], 2.4, col=AG_STRAND)
    if mood == "drink":
        cr.new_path()
        ell(cr, 76, -60, 13, 17)
        leather(cr, (0.30, 0.05, 0.06), 3)
    m = [(74, -76), (50, -86), (26, -92), (6, -80), (-8, -54), (8, -62), (28, -70), (52, -68), (76, -68)]
    _shape(cr, m, AG_WHITE, 3.5)
    if mood == "smile":
        ink(cr, [(10, -152), (34, -166), (60, -154)], 9, col=AG_WHITE)
    else:
        ink(cr, [(8, -144), (34, -156), (62, -146)], 10, col=AG_WHITE)
    _jata(cr, AG_WHITE, 5, 30, line=AG_STRAND)
    _ash_lines(cr, 8, 46, -178)
    cr.new_path()
    cr.arc(-14, -82, 7, 0, 2 * math.pi)
    leather(cr, BROWN, 2)


def agastya_body(cr):
    """man_body with a round belly in front (a short, stout, strong sage), the mala over it."""
    b = _AG["bulk"]
    man_body(cr, _AG)
    belly = [(20 * b, -200), (76 * b, -186), (118 * b, -146), (134 * b, -94), (124 * b, -50), (80 * b, -30),
             (20 * b, -50)]
    _shape(cr, belly, AG_SKIN, 5)
    ink(cr, [(74 * b, -180), (100 * b, -160)], 3)
    holes_line(cr, [(84 * b, -130), (110 * b, -96), (104 * b, -60)], 13, 2.2)
    punch(cr, [(112 * b, -86)], 5.5)
    band(cr, [(-64 * b, -32), (0, -40), (70 * b, -34), (122 * b, -44)], 14, DRED, spacing=12)
    _mala(cr, b)
    _jewel(cr, 66 * b, -118, 11, RED)


AGASTYA = man("c6_agastya", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
              **_AG)
register("c6_agastya_body", (-240, -340, 220, 300), agastya_body)
for _m in ("calm", "smile", "drink"):
    register("c6_agastya_head" + ("" if _m == "calm" else "_" + _m), (-150, -380, 120, 250),
             (lambda m: lambda cr: agastya_head(cr, m))(_m))


def _kamandalu(cr):
    """Agastya's water pot (grip at 0, 0, the top of its handle): a round brass pot, a spout, a looped handle."""
    band(cr, [(-58, 100), (-54, 30), (-26, 2), (26, 2), (54, 30), (58, 100)], 16, BROWN, spacing=12, hole_r=2.2)
    _shape(cr, [(62, 150), (118, 100), (150, 78), (160, 90), (104, 176)], BRASS, 4)
    cr.new_path()
    ell(cr, 0, 178, 100, 86)
    pl = leather(cr, BRASS, 6, keep=True)
    from puppet_core import perforate
    perforate(cr, pl, 12, 16, 3)
    _shape(cr, [(-46, 104), (46, 104), (38, 84), (-38, 84)], BRASS, 5, smooth=False)
    band(cr, [(-50, 92), (50, 92)], 12, DRED, spacing=10, hole_r=2.0)
    band(cr, [(-96, 172), (0, 186), (96, 172)], 14, DRED, spacing=12, hole_r=2.2)
    _flower(cr, 0, 214, 18, RED, 8)


register("c6_kamandalu", (-110, -20, 170, 270), _kamandalu)


# ------------------------------------------------------------------ the gods


DEVA1 = man("c6_deva1", skin=(1.0, 0.86, 0.64), bulk=1.0, dhoti=(0.30, 0.55, 0.95), border=GOLD, pleat=GOLD,
            sash=GREEN, neck=GOLD, crown="kirita", crown_col=GOLD, halo_col=SAFFRON, thread=True,
            hands=("open", "open"))
DEVA2 = man("c6_deva2", skin=(0.98, 0.76, 0.52), bulk=1.05, dhoti=GREEN, border=GOLD, pleat=GOLD, sash=RED,
            neck=GOLD, crown="kirita", crown_col=GOLD, halo_col=(0.30, 0.55, 0.95), thread=True, moustache=True,
            hands=("open", "open"))


def _handlamp(cr):
    """A small clay oil lamp held on the palm (pivot at its foot), its flame lit."""
    _shape(cr, [(-26, 0), (26, 0), (16, -26), (-16, -26)], BRASS, 4, smooth=False)
    cup = [(-70, -40), (-60, -22), (-20, -12), (30, -14), (70, -30), (96, -52), (60, -52), (-60, -52)]
    _shape(cr, cup, (0.84, 0.46, 0.22), 5)
    holes_line(cr, [(-50, -32), (50, -32)], 14, 2.4)
    _shape(cr, [(84, -50), (92, -86), (100, -120), (108, -86), (106, -52)], GOLD, 3)
    _shape(cr, [(92, -56), (98, -82), (104, -56)], PALE, 0)


register("c6_handlamp", (-80, -130, 120, 10), _handlamp, tex=0.6)


# ------------------------------------------------------------------ the Kalakeyas (drawn as silhouettes)


def kala_head(cr, kind=0):
    """An asura's head facing +x: a wild mane, a heavy jaw, horns of three kinds (0 bull, 1 swept-back spikes, 2 a
    curled ram's horn); the eye, the brow slit and two tusks are cut through so the light shows."""
    mane = []
    for i in range(13):
        a = math.radians(100 + 170 * i / 12)
        r = 118 if i % 2 == 0 else 88
        mane.append((-34 + r * math.cos(a), -100 - r * math.sin(a) * 1.05))
    mane += [(-40, 30), (0, -40)]
    _shape(cr, mane, KALA, 5, smooth=False)
    face = [(-30, 10), (-44, -40), (-58, -100), (-52, -160), (-22, -198), (30, -194), (66, -166), (80, -132),
            (106, -110), (100, -86), (116, -60), (100, -34), (74, -18), (40, 2), (20, 16)]
    _shape(cr, face, KALA, 6)

    def crescent(base, tip, bulge, w):
        """A tapered horn from base to tip, bowed out by `bulge` (perpendicular), w = width at the base."""
        (bx, by), (tx, ty) = base, tip
        dx, dy = tx - bx, ty - by
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        outer, inner = [], []
        for i in range(17):
            u = i / 16
            bow = 4 * u * (1 - u) * bulge
            cx, cy = bx + dx * u + nx * bow, by + dy * u + ny * bow
            hw = w * (1 - u) ** 0.9 / 2
            outer.append((cx + nx * hw, cy + ny * hw))
            inner.append((cx - nx * hw, cy - ny * hw))
        _shape(cr, outer + inner[::-1], KALA, 5)
    if kind == 0:                                     # bull horns sweeping out and up, front and back
        crescent((44, -186), (190, -330), 70, 46)
        crescent((-4, -190), (-150, -340), -70, 46)
    elif kind == 1:                                   # two long spikes swept back
        crescent((30, -192), (-120, -390), -40, 38)
        crescent((2, -186), (-170, -320), -30, 34)
    else:                                             # a curled ram's horn round the ear, a short spike in front
        pts, inner = [], []
        for i in range(31):
            u = i / 30
            a = -1.9 - 4.6 * u
            r = 120 * (1 - 0.62 * u)
            w = 46 * (1 - 0.75 * u)
            pts.append((-20 + r * math.cos(a), -200 + r * math.sin(a) * 0.95))
            inner.append((-20 + (r - w) * math.cos(a), -200 + (r - w) * math.sin(a) * 0.95))
        _shape(cr, pts + inner[::-1], KALA, 5)
        crescent((40, -190), (80, -280), 20, 30)
    cut(cr, lambda: ell(cr, 54, -126, 15, 11))                        # the eye
    cut(cr, lambda: poly(cr, [(28, -150), (80, -146), (78, -140), (30, -142)]))   # the brow slit
    for tx in (78, 96):                                               # tusks
        cut(cr, lambda tx=tx: poly(cr, [(tx - 8, -40), (tx + 4, -42), (tx + 14, -76), (tx + 8, -82), (tx - 2, -60)]))
    cut(cr, lambda: poly(cr, [(60, -44), (104, -52), (104, -48), (62, -40)]))      # the mouth line


KALAS = []
for _k, _b in enumerate((1.36, 1.15, 1.5)):
    KALAS.append(man(f"c6_kala{_k}", skin=KALA, bulk=_b, dhoti=KALA, border=KALA, pleat=KALA, sash=KALA, neck=KALA,
                     crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("claw", "claw")))
    register(f"c6_kala{_k}_head", (-260, -430, 260, 60), (lambda k: lambda cr: kala_head(cr, k))(_k))


# ------------------------------------------------------------------ Brahma


_BR_O = dict(skin=BR_SKIN, hair=False, moustache=False, tilak=True, earring=False)


def _white_beard(cr):
    bp = [(62, -50), (64, -22), (58, 40), (42, 120), (22, 70), (2, 20), (8, -40), (30, -54)]
    _shape(cr, bp, AG_WHITE, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -40), (42 - 12 * k, 20), (36 - 10 * k, 80)], 2.5, col=AG_STRAND)
    m = [(66, -76), (46, -84), (24, -88), (12, -74), (30, -78), (52, -76), (68, -72)]
    _shape(cr, m, AG_WHITE, 3)


def _crown_front(cr, cx, by, w, h):
    """A symmetric gold crown (seen from the front) with three peaks over a jewelled band."""
    pts = [(cx - w, by), (cx - w * 1.04, by - h * 0.35), (cx - w * 0.7, by - h * 0.62), (cx - w * 0.42, by - h * 0.5),
           (cx - w * 0.2, by - h * 0.9), (cx, by - h), (cx + w * 0.2, by - h * 0.9), (cx + w * 0.42, by - h * 0.5),
           (cx + w * 0.7, by - h * 0.62), (cx + w * 1.04, by - h * 0.35), (cx + w, by)]
    _shape(cr, pts, GOLD, 6, smooth=False, holes=(11, 14, 2.8))
    band(cr, [(cx - w, by - 10), (cx + w, by - 10)], 18, RED, spacing=12, hole_r=2.4)
    _jewel(cr, cx, by - h * 0.55, 15, RED)
    _jewel(cr, cx - w * 0.62, by - h * 0.36, 9, GREEN)
    _jewel(cr, cx + w * 0.62, by - h * 0.36, 9, GREEN)
    cr.new_path()
    cr.arc(cx, by - h - 14, 13, 0, 2 * math.pi)
    leather(cr, GOLD, 4)


def brahma_head(cr):
    """Three of Brahma's four faces: a profile to each side and a frontal face in the middle, white beards, one wide
    gold crown, a ring of golden rays behind."""
    M._ray_halo(cr, 0, -170, 190, 270, 20, (GOLD, SAFFRON))
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 70, 10)
        cr.scale(sx * 0.82, 0.82)
        A.face(cr, _BR_O, "calm")
        _white_beard(cr)
        R.kirita(cr, GOLD, None, tall=0.7, flare=RED)
        cr.restore()
    cx, cy = 0, -104
    cr.new_path()
    ell(cr, cx - 64, cy, 12, 20)
    leather(cr, BR_SKIN, 4)
    cr.new_path()
    ell(cr, cx + 64, cy, 12, 20)
    leather(cr, BR_SKIN, 4)
    cr.new_path()
    ell(cr, cx, cy, 62, 80)
    leather(cr, BR_SKIN, 6)
    for sx in (-1, 1):
        cr.save()
        cr.translate(cx + sx * 26, cy - 16)
        cr.scale(sx, 1)
        almond_eye(cr, 0, 0, 34, 11, look=0, col=PALE)
        cr.restore()
        ink(cr, [(cx + sx * 10, cy - 38), (cx + sx * 28, cy - 46), (cx + sx * 46, cy - 38)], 4)
    ink(cr, [(cx + 2, cy - 18), (cx - 4, cy + 16), (cx + 6, cy + 20)], 3.5)
    ink(cr, [(cx, cy - 74), (cx, cy - 52)], 5, col=RED)
    bp = [(cx - 54, cy + 14), (cx - 60, cy + 70), (cx - 36, cy + 130), (cx, cy + 160), (cx + 36, cy + 130),
          (cx + 60, cy + 70), (cx + 54, cy + 14), (cx + 30, cy + 46), (cx, cy + 52), (cx - 30, cy + 46)]
    _shape(cr, bp, AG_WHITE, 4)
    for k in (-2, -1, 0, 1, 2):
        ink(cr, [(cx + 14 * k, cy + 60), (cx + 18 * k, cy + 110), (cx + 12 * k, cy + 140 - 8 * abs(k))], 2.4,
            col=AG_STRAND)
    ms = [(cx - 44, cy + 40), (cx - 20, cy + 26), (cx, cy + 32), (cx + 20, cy + 26), (cx + 44, cy + 40),
          (cx + 20, cy + 40), (cx, cy + 38), (cx - 20, cy + 40)]
    _shape(cr, ms, AG_WHITE, 3)
    _crown_front(cr, cx, cy - 62, 78, 200)


_BRB = dict(skin=BR_SKIN, bulk=1.12, dhoti=RED, border=GOLD, pleat=GOLD, sash=GOLD, neck=GOLD, thread=True, beads=True)
BRAHMA = man("c6_brahma", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_BRB)
register("c6_brahma_head", (-300, -500, 300, 120), brahma_head)
register("c6_brahma_body_sit", (-220, -330, 160, 80), body_sit(_BRB))
register("c6_brahma_seat", (-110, -60, 280, 110), lambda cr: seat_legs(cr, BR_SKIN, RED, GOLD))


def _veda(cr):
    """A small palm-leaf book (the Vedas) between two boards, tied with a red string (pivot at its centre)."""
    for y in (-14, -4, 6):
        _shape(cr, [(-96, y), (96, y - 1), (98, y + 9), (-98, y + 10)], LEAF, 2.5, smooth=False)
    for y in (-30, 16):
        _shape(cr, [(-104, y), (104, y), (106, y + 14), (-106, y + 14)], WOOD, 4, smooth=False)
    ink(cr, [(-50, -34), (-46, 34)], 4, col=RED)
    ink(cr, [(50, -34), (46, 34)], 4, col=RED)


register("c6_veda", (-110, -40, 110, 40), _veda)


# ------------------------------------------------------------------ Bhagiratha and Ganga


_BH = dict(skin=BH_SKIN, bulk=1.05, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=SAFFRON, neck=GOLD,
           crown="kirita", crown_col=GOLD, halo_col=SAFFRON, moustache=True, thread=True)
BHAGI = man("c6_bhagi", hands=("open", "open"), **_BH)


def bhagi_pray_head(cr):
    man_head(cr, _BH)
    M._sleep_eye(cr, BH_SKIN)


register("c6_bhagi_head_pray", (-190, -420, 110, 100), bhagi_pray_head)


def ganga_head(cr):
    M._ray_halo(cr, -10, -120, 130, 190, 18, (PALE, GA_BLUE))
    woman_head(cr, dict(skin=GA_SKIN, flower=PALE))
    K.queen_crown(cr)
    _jewel(cr, -10, -60, 9, (0.30, 0.60, 1.0))


_GA = dict(skin=GA_SKIN, skirt=GA_BLUE, choli=(0.97, 0.98, 1.0), border=GOLD, pallu_col=(0.40, 0.66, 1.0), gem=BLUE,
           flower=PALE)
GANGA = woman("c6_ganga", hands=("open", "open"), **_GA)
register("c6_ganga_head", (-200, -330, 140, 70), ganga_head)


def ganga_body(cr):
    """Her body from the waist up (below the waist she is the river, drawn per frame)."""
    cr.save()
    cr.rectangle(-400, -600, 800, 640)
    cr.clip()
    woman_body(cr, _GA)
    cr.restore()
    band(cr, [(-60, 36), (0, 30), (66, 34)], 16, GOLD, spacing=11, hole_r=2.2)


register("c6_ganga_body", (-160, -310, 170, 60), ganga_body)


# ------------------------------------------------------------------ Rishyashringa, Vibhandaka and the doe


_RS_O = dict(skin=RS_SKIN, hair=False, moustache=False, tilak=False, earring=False)
_RS = dict(skin=RS_SKIN, bulk=0.88, dhoti=BARK, border=BARK2, pleat=BARK2, sash=VINE, neck=BROWN, beads=True)


def horn(cr):
    """His small ivory horn, growing up from the forehead and curving forward, with ridges."""
    hp = [(22, -184), (34, -192), (48, -184), (60, -206), (70, -236), (70, -262), (60, -270), (52, -246),
          (40, -220), (28, -200)]
    _shape(cr, hp, HORN, 4)
    for k, y in enumerate((-200, -216, -232, -248)):
        ink(cr, [(32 + 5 * k, y + 4), (44 + 6 * k, y - 2), (58 + 4 * k, y + 2)], 2.4, col=(0.66, 0.56, 0.40))


def rishya_head(cr, mood="calm"):
    """The forest boy: long untidy hair, a top-knot tied with a green vine, the small horn. mood: calm | puzzled |
    smile | wonder."""
    hp = [(-28, -178), (-68, -150), (-94, -80), (-104, 10), (-92, 96), (-70, 118), (-56, 60), (-46, -20), (-24, -100)]
    _shape(cr, hp, HAIR, 5)
    for k in range(4):
        holes_line(cr, [(-48 - 8 * k, -140 + 10 * k), (-74 - 4 * k, -40), (-70 - 2 * k, 60)], 16, 2.4)
    RU.rface(cr, _RS_O, {"puzzled": "calm", "wonder": "shock"}.get(mood, mood))
    if mood == "puzzled":                              # one brow raised high, a small round mouth
        _cover(cr, RS_SKIN, 34, -146, 30, 9)
        ink(cr, [(10, -152), (32, -170), (58, -160)], 5)
        _cover(cr, RS_SKIN, 64, -70, 6, 5)
        cr.new_path()
        ell(cr, 66, -68, 6, 7)
        leather(cr, (0.40, 0.06, 0.06), 2.2)
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (40, -202), (52, -188), (22, -190), (-8, -184),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, HAIR, 4)
    cr.new_path()
    ell(cr, -18, -232, 40, 32, -0.2)
    leather(cr, HAIR, 4)
    holes_line(cr, [(-46, -234), (-18, -252), (12, -238)], 11, 2.2)
    band(cr, [(-50, -212), (-18, -206), (16, -214)], 10, VINE, spacing=10, hole_r=1.8)
    _shape(cr, [(14, -218), (40, -236), (52, -222), (30, -212)], VINE, 3)
    horn(cr)
    cr.new_path()
    cr.arc(-14, -80, 7, 0, 2 * math.pi)
    leather(cr, BROWN, 2)


RISHYA = man("c6_rishya", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_RS)
for _m in ("calm", "puzzled", "smile", "wonder"):
    register("c6_rishya_head" + ("" if _m == "calm" else "_" + _m), (-130, -300, 120, 140),
             (lambda m: lambda cr: rishya_head(cr, m))(_m))
register("c6_rishya_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, RS_SKIN, BARK, BARK2, 0.88))


_VB_O = dict(skin=VB_SKIN, hair=False, moustache=False, tilak=False, earring=False)
_VB = dict(skin=VB_SKIN, bulk=0.9, dhoti=BARK2, border=BARK, pleat=BARK, sash=BARK, neck=BROWN, beads=True,
           robe=DEERSKIN)


def vibha_head(cr):
    """The father: long grey hair, a long grey beard, grey matted hair piled high, a stern brow, ash lines."""
    hp = [(-30, -176), (-66, -146), (-92, -70), (-98, 40), (-74, 120), (-48, 70), (-40, -30), (-24, -100)]
    _shape(cr, hp, GREY, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-74 - 6 * k, -20), (-66 - 4 * k, 90)], 2.5, col=GREY2)
    RU.rface(cr, _VB_O, "calm")
    bp = [(62, -50), (66, -20), (60, 50), (46, 140), (26, 96), (4, 30), (8, -40), (30, -54)]
    _shape(cr, bp, GREY, 4)
    for k in range(3):
        ink(cr, [(50 - 12 * k, -36), (44 - 12 * k, 30), (38 - 10 * k, 100)], 2.5, col=GREY2)
    m = [(66, -76), (46, -84), (24, -88), (12, -74), (30, -78), (52, -76), (68, -72)]
    _shape(cr, m, GREY, 3)
    ink(cr, [(10, -138), (34, -144), (60, -132)], 8, col=GREY2)
    _jata(cr, GREY2, 6, 30, line=INK)
    _ash_lines(cr, 4, 44, -176)


VIBHA = man("c6_vibha", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "fist"),
            **_VB)
register("c6_vibha_head", (-150, -400, 120, 160), vibha_head)


DOE_NECK = (120.0, -400.0)            # where the doe's neck joins her body (body units)


def _doe_leg(cr, x0, col, hind=False):
    """A slender leg from the body down to a dark hoof on the ground (y = 0); hind legs bend back at the hock."""
    if hind:
        lg = [(x0 - 30, -330), (x0 + 26, -330), (x0 + 22, -230), (x0 - 4, -150), (x0 + 6, -14), (x0 - 8, -14),
              (x0 - 22, -150), (x0 - 10, -230)]
    else:
        lg = [(x0 - 18, -320), (x0 + 18, -320), (x0 + 12, -200), (x0 + 8, -14), (x0 - 6, -14), (x0 - 10, -200)]
    _shape(cr, lg, col, 4, smooth=False)
    hx = x0 - (1 if hind else 0)
    _shape(cr, [(hx - 10, -16), (hx + 12, -16), (hx + 16, 2), (hx - 10, 2)], INK, 0, smooth=False)


def _doe_body(cr):
    """A spotted doe in profile facing +x (pivot on the ground under her middle; her neck joins at DOE_NECK): long
    slender legs, a short deep body, white spots punched through, a short upturned tail."""
    dark = tuple(c * 0.82 for c in DOE)
    _doe_leg(cr, -112, dark, True)
    _doe_leg(cr, 118, dark)
    body = [(-190, -380), (-150, -432), (-40, -436), (80, -432), (150, -444), (196, -406), (200, -350), (168, -318),
            (80, -306), (-60, -306), (-160, -314), (-196, -340)]
    _shape(cr, body, DOE, 5)
    cr.save()
    cr.new_path()
    spath(cr, body)
    cr.clip()
    cr.new_path()
    ell(cr, 0, -300, 190, 34)
    cr.set_source_rgb(*DOE2)
    cr.fill()
    cr.restore()
    cr.new_path()
    spath(cr, body)
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    rng = random.Random(4)
    spots = [(-160 + 30 * i + rng.uniform(-6, 6), -408 + 22 * (i % 2) + rng.uniform(-5, 5)) for i in range(11)]
    spots += [(-140 + 36 * i + rng.uniform(-6, 6), -368 + rng.uniform(-5, 5)) for i in range(8)]
    punch(cr, spots, 6.5)
    _shape(cr, [(-186, -396), (-222, -440), (-214, -452), (-178, -420)], DOE, 3)
    _doe_leg(cr, -140, DOE, True)
    _doe_leg(cr, 146, DOE)
    rivet(cr, *DOE_NECK, 9)


def _doe_head(cr):
    """The doe's neck and head (pivot at the base of the neck): big ears, a big soft eye, a dark nose."""
    neck = [(-46, 16), (40, 6), (100, -130), (120, -200), (74, -236), (16, -170), (-36, -60)]
    _shape(cr, neck, DOE, 5)
    holes_line(cr, [(6, -6), (46, -100), (80, -180)], 14, 2.6)
    for k, (ex, rot) in enumerate(((60, -1.0), (84, -0.62))):
        cr.save()
        cr.translate(ex, -246)
        cr.rotate(rot)
        _shape(cr, [(0, 0), (-22, -50), (-8, -120), (18, -126), (30, -50), (16, 0)], DOE if k else DOE2, 4)
        ink(cr, [(4, -16), (6, -100)], 2.2)
        cr.restore()
    head = [(56, -250), (110, -276), (180, -262), (238, -232), (248, -210), (230, -190), (170, -178), (110, -182),
            (68, -206)]
    _shape(cr, head, DOE, 5)
    cr.save()
    cr.new_path()
    spath(cr, head)
    cr.clip()
    cr.new_path()
    ell(cr, 170, -176, 84, 22)
    cr.set_source_rgb(*DOE2)
    cr.fill()
    cr.restore()
    almond_eye(cr, 142, -240, 44, 15, look=1, col=PALE)
    cr.new_path()
    ell(cr, 242, -214, 14, 12)
    cr.set_source_rgb(*INK)
    cr.fill()
    ink(cr, [(228, -190), (204, -188)], 3)


register("c6_doe_body", (-240, -470, 230, 12), _doe_body)
register("c6_doe_head", (-60, -400, 270, 30), _doe_head)


# ------------------------------------------------------------------ the city women, the villagers, Shanta


def cw_head(cr, skin, flowers=(RED, ROSE, GOLD), eyes="open", plain=False):
    """A woman's head with no crown: hair bun with jasmine and flowers, a maang-tikka, a bindi, a nose ring, jhumkas.
    eyes: open | smile | down (sad). plain: a village woman (one flower, no nose ring)."""
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, skin, 6)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 22 * math.cos(a), -128 + 22 * math.sin(a))], 3.2)
    if not plain:
        for i in range(12):
            a = math.pi * (0.25 + 1.5 * i / 11)
            _flower(cr, -62 + 42 * math.cos(a), -128 + 42 * math.sin(a), 9, PALE, 5)
        for (x, y, r), col in zip(((-72, -176, 15), (-44, -170, 12), (-98, -156, 12), (-100, -110, 11)),
                                  flowers + flowers[:1]):
            _flower(cr, x, y, r, col, 6)
        ink(cr, [(-2, -188), (18, -184), (34, -176)], 3.5, col=GOLD)
        _jewel(cr, 38, -170, 7, RED)
    else:
        _flower(cr, -80, -160, 14, flowers[0], 6)
    cr.new_path()
    cr.arc(46, -146, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    if eyes == "smile":
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5)
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    elif eyes == "down":
        _cover(cr, skin, 30, -112, 19, 13)
        ink(cr, [(14, -110), (30, -102), (46, -110)], 4)
        ink(cr, [(14, -126), (30, -132), (48, -140)], 3.5)
        ink(cr, [(62, -72), (54, -70)], 3, col=RED)
    else:
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)
    if not plain:
        cr.new_path()
        cr.arc(68, -90, 9, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(3)
        cr.stroke()
    _jewel(cr, -10, -70, 9, GOLD)
    for k in range(3):
        cr.new_path()
        cr.arc(-10, -52 + 12 * k, 5 - k, 0, 2 * math.pi)
        leather(cr, GOLD, 2)


_WOMEN = (dict(skin=(0.99, 0.78, 0.60), skirt=(0.98, 0.44, 0.62), choli=(0.20, 0.60, 0.90), border=GOLD,
               pallu_col=(0.90, 0.22, 0.48), gem=GOLD, fl=(RED, GOLD, PALE)),
          dict(skin=(0.97, 0.72, 0.52), skirt=(1.0, 0.62, 0.14), choli=(0.56, 0.26, 0.72), border=RED,
               pallu_col=(0.90, 0.34, 0.10), gem=GREEN, fl=(ROSE, RED, GOLD)),
          dict(skin=(1.0, 0.82, 0.66), skirt=(0.56, 0.36, 0.86), choli=(1.0, 0.76, 0.22), border=GOLD,
               pallu_col=(0.36, 0.20, 0.70), gem=RED, fl=(GOLD, ROSE, RED)))
WOMEN = []
for _k, _o in enumerate(_WOMEN):
    _oo = {k: v for k, v in _o.items() if k != "fl"}
    WOMEN.append(woman(f"c6_wom{_k}", hands=("open", "open"), **_oo))
    for _e in ("open", "smile"):
        register(f"c6_wom{_k}_head" + ("" if _e == "open" else "_" + _e), (-140, -250, 100, 30),
                 (lambda o, e: lambda cr: cw_head(cr, o["skin"], o["fl"], e))(_o, _e))

VWOMAN = woman("c6_vwom", skin=(0.90, 0.62, 0.40), skirt=(0.86, 0.56, 0.22), choli=(0.30, 0.46, 0.76), border=DRED,
               pallu_col=(0.70, 0.34, 0.12), gem=RED, hands=("open", "open"))
for _e in ("down", "smile"):
    register("c6_vwom_head" + ("" if _e == "down" else "_" + _e), (-140, -250, 100, 30),
             (lambda e: lambda cr: cw_head(cr, (0.90, 0.62, 0.40), (GOLD,), e, plain=True))(_e))

_FM_O = dict(skin=FM_SKIN, hair=False, moustache=True, tilak=False, earring=False)
_FM = dict(skin=FM_SKIN, bulk=0.92, dhoti=(0.97, 0.92, 0.78), border=BROWN, pleat=(0.97, 0.92, 0.78),
           sash=(0.86, 0.32, 0.16), neck=BROWN)


def farmer_head(cr, mood="sad"):
    """A farmer with a red turban and a moustache. mood: sad (eyes cast down) | happy (laughing)."""
    RU.rface(cr, _FM_O, {"sad": "shame", "happy": "laugh"}[mood])
    tail = [(-50, -150), (-90, -120), (-110, -40), (-96, -30), (-76, -100), (-44, -126)]
    _shape(cr, tail, (0.86, 0.22, 0.14), 4)
    tb = [(-60, -118), (-66, -160), (-48, -200), (-6, -222), (40, -214), (60, -190), (62, -158), (40, -166),
          (10, -158), (-24, -146), (-44, -122)]
    _shape(cr, tb, (0.92, 0.26, 0.14), 5)
    for k in range(3):
        ink(cr, [(-54 + 4 * k, -132 - 22 * k), (0, -160 - 22 * k), (52 - 4 * k, -170 - 14 * k)], 3, col=GOLD)


FARMER = man("c6_farmer", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_FM)
for _m in ("sad", "happy"):
    register("c6_farmer_head" + ("" if _m == "sad" else "_" + _m), (-130, -250, 110, 60),
             (lambda m: lambda cr: farmer_head(cr, m))(_m))

SHANTA = woman("c6_shanta", skin=SH_SKIN, skirt=(0.86, 0.12, 0.12), choli=(0.98, 0.72, 0.20), border=GOLD,
               pallu_col=(0.66, 0.05, 0.10), gem=GREEN, flower=PALE, hands=("open", "open"))
for _e in ("open", "smile"):
    register("c6_shanta_head" + ("" if _e == "open" else "_" + _e), (-140, -300, 110, 40),
             (lambda e: lambda cr: (cw_head(cr, SH_SKIN, (RED, GOLD, PALE), e), K.queen_crown(cr)))(_e))

LOMA = man("c6_loma", skin=LP_SKIN, bulk=1.12, dhoti=LP_GREEN, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
           crown="kirita", crown_col=GOLD, halo_col=LP_GREEN, moustache=True, thread=True, hands=("open", "open"))

BRAHMIN_A = man("c6_brahA", skin=BRM_SKIN, bulk=0.95, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=SAFFRON,
                neck=BROWN, crown="shikha", thread=True, beard=True, moustache=True, hair=False, beads=True,
                hands=("open", "open"))
BRAHMIN_B = man("c6_brahB", skin=(0.90, 0.66, 0.44), bulk=0.92, dhoti=(1.0, 0.86, 0.56), border=DRED, pleat=DRED,
                sash=DRED, neck=BROWN, crown="shikha", thread=True, moustache=True, hair=False, beads=True,
                hands=("open", "open"))

register("c6_dasha_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, K.DS_SKIN, RED, GOLD, 1.12))


# ------------------------------------------------------------------ the sea


def _wave(cr, col, k):
    """A long sea strip (2800 units, repeating every WAVE_P): rolling crests with a curl of foam, perforated."""
    ph = 0.37 * k
    top = []
    for i in range(-1400, 1401, 6):
        u = (i / WAVE_P + ph) % 1.0                       # a slow rise to a crest at u = 1, a steep fall after it
        y = -34 + 30 * (1 - u ** 1.6) if u > 0.08 else -34 + 30 * (u / 0.08) ** 0.5 * (1 - 0.08 ** 1.6)
        top.append((i, y))
    cr.new_path()
    poly(cr, top + [(1400, 170), (-1400, 170)])
    leather(cr, col, 5)
    for j in range(-8, 9):                                # a curl of foam breaking over each crest
        x = (j - ph) * WAVE_P
        _shape(cr, [(x - 60, -26), (x - 26, -40), (x + 4, -42), (x + 22, -30), (x + 18, -14), (x + 6, -24),
                    (x - 14, -30), (x - 40, -22)], FOAM, 3)
        punch(cr, [(x - 70, -8), (x - 50, 4), (x + 30, 2)], 3.2)
    holes_line(cr, [(-1390, 64), (1390, 64)], 22, 3.0, smooth=False)


for _k, _c in enumerate(WAVES):
    register(f"c6_wave{_k}", (-1410, -60, 1410, 180), (lambda c, k: lambda cr: _wave(cr, c, k))(_c, _k))


def _seabed(cr, wet=False):
    """The sandy sea floor (top edge at y ~ 0, 2400 units wide): ripples, pebbles, punched sparkles."""
    rng = random.Random(21)
    top = [(x, 6 * math.sin(x / 90.0) + 4 * math.sin(x / 37.0)) for x in range(-1200, 1201, 20)]
    cr.new_path()
    poly(cr, top + [(1200, 300), (-1200, 300)])
    leather(cr, (0.80, 0.70, 0.50) if wet else SAND, 6)
    for row in range(5):
        y = 40 + 50 * row
        pts = [(x, y + 8 * math.sin(x / 60.0 + row)) for x in range(-1180, 1181, 30)]
        ink(cr, pts, 2.5, col=SAND2)
    for _ in range(40):
        x, y = rng.uniform(-1150, 1150), rng.uniform(30, 280)
        cr.new_path()
        ell(cr, x, y, rng.uniform(8, 18), rng.uniform(5, 10))
        leather(cr, SAND2, 2)
    punch(cr, [(rng.uniform(-1180, 1180), rng.uniform(20, 290)) for _ in range(70)], 2.6)


register("c6_seabed", (-1210, -20, 1210, 310), _seabed)


def _fish(cr, col, col2):
    """A fish lying on its side (pivot at its middle), facing +x: scales punched, a round eye, a forked tail."""
    body = [(-110, 0), (-60, -46), (20, -56), (90, -30), (120, 0), (90, 26), (20, 46), (-60, 40)]
    pl = _shape(cr, body, col, 5)
    cr.save()
    cr.new_path()
    spath(cr, body)
    cr.clip()
    cr.new_path()
    ell(cr, 10, 40, 120, 26)
    cr.set_source_rgb(*col2)
    cr.fill()
    cr.restore()
    cr.new_path()
    spath(cr, body)
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    _shape(cr, [(-104, 0), (-170, -50), (-150, 0), (-170, 50)], col, 4, smooth=False)
    _shape(cr, [(-50, -42), (-30, -76), (30, -80), (40, -54)], col, 3, smooth=False)
    for x in (-30, -6, 16):
        ink(cr, [(x, -50), (x + 4, -74)], 2, smooth=False)
    ink(cr, [(64, -36), (56, 0), (64, 30)], 3)
    cr.new_path()
    cr.arc(84, -10, 13, 0, 2 * math.pi)
    leather(cr, PALE, 3)
    cr.new_path()
    cr.arc(87, -10, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    pts = [(-60 + 24 * i, -20 + 22 * j + (11 if i % 2 else 0)) for i in range(5) for j in range(2)]
    punch(cr, pts, 4)


register("c6_fish0", (-180, -95, 130, 60), lambda cr: _fish(cr, (0.62, 0.78, 0.92), (0.90, 0.94, 0.98)))
register("c6_fish1", (-180, -95, 130, 60), lambda cr: _fish(cr, (1.0, 0.58, 0.20), (1.0, 0.84, 0.50)))
register("c6_fish2", (-180, -95, 130, 60), lambda cr: _fish(cr, (0.56, 0.80, 0.40), (0.92, 0.94, 0.62)))


def _shell(cr):
    """A conch shell lying on the sand (pivot at its base)."""
    sh = [(-80, 0), (-60, -40), (-10, -70), (50, -66), (90, -40), (100, -10), (70, 0)]
    _shape(cr, sh, (1.0, 0.92, 0.84), 5)
    for k in range(4):
        ink(cr, [(-50 + 30 * k, -4), (-30 + 30 * k, -50 + 4 * k)], 3, col=(0.80, 0.56, 0.48))
    _shape(cr, [(70, -10), (110, -26), (126, -10), (100, 2)], (1.0, 0.70, 0.62), 3)


def _star(cr):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + math.pi * i / 5
        r = 64 if i % 2 == 0 else 26
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, (1.0, 0.56, 0.30), 4)
    punch(cr, [(30 * math.cos(-math.pi / 2 + 2 * math.pi * i / 5), 30 * math.sin(-math.pi / 2 + 2 * math.pi * i / 5))
               for i in range(5)], 4)


register("c6_shell", (-90, -80, 135, 10), _shell)
register("c6_star", (-70, -70, 70, 70), _star)


def _rock(cr):
    """A big shore rock (pivot at the middle of its foot), layered, with a few cracks and holes."""
    rk = [(-300, 0), (-290, -80), (-240, -180), (-150, -250), (-30, -280), (100, -268), (210, -220), (280, -140),
          (300, -60), (310, 0)]
    _shape(cr, rk, (0.64, 0.60, 0.62), 6, holes=(14, 18, 3))
    for pts in (((-220, -120), (-100, -150), (40, -140), (180, -110)), ((-160, -200), (-40, -220), (90, -210)),
                ((-260, -50), (-120, -70), (60, -60), (250, -50))):
        ink(cr, list(pts), 3.5, col=(0.40, 0.38, 0.42))
    ink(cr, [(60, -268), (40, -200), (70, -150)], 3)


register("c6_rock", (-320, -300, 330, 12), _rock)


def _hole_rim(cr):
    """The near lip of Patala's hole (pivot at its centre; the hole is an ellipse 520 x 130): a crescent of broken
    rock with a jagged outer edge, cracks and holes."""
    rng = random.Random(7)
    outer, inner = [], []
    for i in range(41):
        a = math.pi * i / 40
        j = 1.0 + (rng.uniform(-0.06, 0.08) if 0 < i < 40 else 0)
        outer.append((300 * math.cos(a) * j, 96 * math.sin(a) * j + 6))
        inner.append((262 * math.cos(a), 64 * math.sin(a)))
    _shape(cr, outer + inner[::-1], (0.58, 0.50, 0.46), 5, smooth=False, holes=(9, 15, 2.6))
    for a in (0.5, 1.2, 1.9, 2.6):
        ink(cr, [(262 * math.cos(a), 64 * math.sin(a)), (286 * math.cos(a + 0.05), 90 * math.sin(a + 0.05))], 3)


register("c6_hole_rim", (-320, -20, 320, 120), _hole_rim)


# ------------------------------------------------------------------ cards, leaves, earth, crops, ground


def _earth(cr, wet=False):
    """The fields of Anga (2400 units wide, top at y = 0): dry and cracked, or (wet) dark, with puddles."""
    rng = random.Random(33)
    top = [(x, 4 * math.sin(x / 70.0)) for x in range(-1200, 1201, 20)]
    cr.new_path()
    poly(cr, top + [(1200, 320), (-1200, 320)])
    leather(cr, WET if wet else EARTH, 6)
    if wet:
        for _ in range(9):
            x, y = rng.uniform(-1100, 1100), rng.uniform(60, 260)
            cr.new_path()
            ell(cr, x, y, rng.uniform(70, 140), rng.uniform(12, 22))
            leather(cr, (0.56, 0.74, 0.96), 3)
        punch(cr, [(rng.uniform(-1180, 1180), rng.uniform(20, 300)) for _ in range(60)], 2.6)
        return
    for _ in range(46):                                   # cracks: branching zig-zags
        x, y = rng.uniform(-1180, 1180), rng.uniform(20, 300)
        pts = [(x, y)]
        a = rng.uniform(0, 2 * math.pi)
        for _k in range(5):
            a += rng.uniform(-0.9, 0.9)
            x += 40 * math.cos(a)
            y = min(310, max(10, y + 20 * math.sin(a)))
            pts.append((x, y))
        ink(cr, pts, rng.uniform(4, 7), smooth=False, col=(0.36, 0.22, 0.12))
    holes_line(cr, [(-1190, 14), (1190, 14)], 26, 3, smooth=False)


register("c6_earth", (-1210, -20, 1210, 330), _earth)
register("c6_earth_wet", (-1210, -20, 1210, 330), lambda cr: _earth(cr, True))


def _crop(cr, green=False):
    """A clump of crop stalks (pivot at the base): drooping and dry, or green and standing with grain heads."""
    rng = random.Random(5 if green else 6)
    for i in range(7):
        x0 = -60 + 20 * i + rng.uniform(-6, 6)
        hgt = rng.uniform(220, 300)
        if green:
            tip = (x0 + rng.uniform(-30, 30), -hgt)
            ink(cr, [(x0, 0), ((x0 + tip[0]) / 2, -hgt * 0.5), tip], 6, col=DGREEN)
            cr.new_path()
            ell(cr, tip[0], tip[1] - 26, 10, 30, rng.uniform(-0.2, 0.2))
            leather(cr, (0.86, 0.80, 0.30), 3)
            for s in (-1, 1):
                _shape(cr, [(x0, -60), (x0 + s * 60, -130), (x0 + s * 20, -90)], GREEN, 3)
        else:
            bend = 1 if i % 2 else -1
            pts = [(x0, 0), (x0 + bend * 10, -hgt * 0.55), (x0 + bend * 60, -hgt * 0.75), (x0 + bend * 100,
                                                                                           -hgt * 0.55)]
            ink(cr, pts, 6, col=(0.72, 0.56, 0.28))
            _shape(cr, [(x0 + bend * 100 - 8, -hgt * 0.55), (x0 + bend * 112, -hgt * 0.42),
                        (x0 + bend * 96, -hgt * 0.40)], (0.62, 0.46, 0.22), 3)
            _shape(cr, [(x0, -40), (x0 + bend * 50, -60), (x0 + bend * 80, -20)], (0.80, 0.64, 0.34), 3)


register("c6_crop_dry", (-200, -320, 200, 10), _crop)
register("c6_crop_green", (-160, -360, 160, 10), lambda cr: _crop(cr, True))


def _ground_w(cr):
    """puppet_cast's ground strip, wide enough for the landscape frame (2400 units)."""
    _shape(cr, [(-1200, 0), (1200, 0), (1200, 140), (-1200, 140)], (0.45, 0.30, 0.14), 6, smooth=False)
    rng = random.Random(9)
    for i in range(42):
        x = -1180 + 57 * i + rng.uniform(-10, 10)
        for k in (-1, 0, 1):
            poly(cr, [(x + 8 * k - 5, 4), (x + 22 * k, -36 - 12 * abs(k - 0.3)), (x + 8 * k + 5, 4)])
            leather(cr, GREEN, 3)
    holes_line(cr, [(-1190, 70), (1190, 70)], 22, 4, smooth=False)


register("c6_ground", (-1210, -60, 1210, 150), _ground_w)


# ------------------------------------------------------------------ sweets


SWEET_Y = (1.0, 0.80, 0.26)
SWEET_O = (1.0, 0.56, 0.18)
LADDU = (1.0, 0.68, 0.20)


def _fruit_outline():
    return [(0, -78), (36, -70), (62, -30), (64, 20), (44, 62), (6, 80), (-34, 66), (-56, 26), (-56, -24), (-34, -64)]


def _fruit(cr):
    """A sweet shaped like a mango (pivot at its middle): golden with an orange blush, a green leaf."""
    pts = _fruit_outline()
    _shape(cr, pts, SWEET_Y, 6)
    cr.save()
    cr.new_path()
    spath(cr, pts)
    cr.clip()
    cr.new_path()
    ell(cr, 30, -30, 46, 52)
    cr.set_source_rgb(*SWEET_O)
    cr.fill()
    cr.restore()
    cr.new_path()
    spath(cr, pts)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    punch(cr, [(-20, 10), (-6, 30), (10, 44), (-28, -16), (16, 2)], 3)
    ink(cr, [(0, -78), (6, -100)], 6, col=BROWN)
    _shape(cr, [(6, -96), (40, -120), (86, -112), (50, -92)], GREEN, 4)
    ink(cr, [(10, -98), (80, -110)], 2.5)


def _fruit_half(cr, s):
    """Half of the 'fruit', cut down the middle (s = -1 the left half): inside it is a laddu, golden boondi."""
    pts = [(0, -78), (s * 36, -70), (s * 62, -30), (s * 64, 20), (s * 44, 62), (s * 6, 80), (0, 80)]
    cr.new_path()
    poly(cr, pts)
    leather(cr, SWEET_Y, 6)
    cr.new_path()
    ell(cr, s * 14, 2, 26, 70)
    pl = leather(cr, LADDU, 4, keep=True)
    rng = random.Random(3 if s < 0 else 4)
    cr.save()
    cr.new_path()
    ell(cr, s * 14, 2, 22, 66)
    cr.clip()
    for _ in range(26):
        x, y = s * 14 + rng.uniform(-22, 22), rng.uniform(-62, 66)
        cr.new_path()
        cr.arc(x, y, rng.uniform(5, 8), 0, 2 * math.pi)
        cr.set_source_rgb(*SWEET_O)
        cr.fill()
    cr.restore()
    punch(cr, [(s * 14 + rng.uniform(-16, 16), rng.uniform(-56, 56)) for _ in range(14)], 2.6)
    _shape(cr, [(s * 8, -20), (s * 22, -24), (s * 18, -14)], GREEN, 2)
    if s < 0:
        ink(cr, [(0, -78), (4, -100)], 6, col=BROWN)
        _shape(cr, [(4, -96), (38, -120), (84, -112), (48, -92)], GREEN, 4)


register("c6_fruit", (-70, -130, 100, 90), _fruit)
register("c6_fruitL", (-75, -130, 95, 90), lambda cr: _fruit_half(cr, -1))
register("c6_fruitR", (-10, -90, 75, 90), lambda cr: _fruit_half(cr, 1))


def _plate(cr):
    """A brass plate of sweets shaped like fruits (pivot at the plate's middle, where a palm holds it)."""
    def mini_fruit(x, y, s, col, col2):
        cr.save()
        cr.translate(x, y)
        cr.scale(s, s)
        pts = _fruit_outline()
        _shape(cr, pts, col, 7)
        cr.save()
        cr.new_path()
        spath(cr, pts)
        cr.clip()
        cr.new_path()
        ell(cr, 30, -30, 46, 52)
        cr.set_source_rgb(*col2)
        cr.fill()
        cr.restore()
        cr.new_path()
        spath(cr, pts)
        cr.set_source_rgb(*INK)
        cr.set_line_width(7)
        cr.stroke()
        _shape(cr, [(6, -76), (40, -104), (80, -96), (46, -76)], GREEN, 5)
        cr.restore()

    def laddu(x, y, r):
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        leather(cr, LADDU, 4)
        punch(cr, [(x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a)) for a in (0.5, 1.9, 3.3, 4.6)], 2.6)
    _shape(cr, [(-150, -22), (-60, -46), (60, -46), (150, -22), (60, -6), (-60, -6)], GREEN, 4)
    mini_fruit(-70, -62, 0.42, SWEET_Y, SWEET_O)
    mini_fruit(64, -62, 0.42, (0.98, 0.42, 0.36), (0.88, 0.20, 0.20))
    mini_fruit(0, -104, 0.44, SWEET_Y, (0.60, 0.80, 0.30))
    for x, y in ((-112, -40), (-20, -44), (110, -40)):
        laddu(x, y, 22)
    cr.new_path()
    ell(cr, 0, -10, 164, 22)
    leather(cr, BRASS, 5)
    holes_line(cr, [(-140, -10), (140, -10)], 14, 2.4)
    _shape(cr, [(-40, 8), (40, 8), (30, 24), (-30, 24)], BRASS, 4, smooth=False)


register("c6_plate", (-175, -160, 175, 30), _plate)


# ------------------------------------------------------------------ the boat-hermitage


def _boat_hull(cr):
    """The hull of the boat-hermitage (pivot at the middle of the deck): a long painted hull, a swan's neck at the
    prow (+x), a curled stern."""
    hull = [(-600, -40), (-560, 0), (560, 0), (612, -40), (600, 30), (520, 110), (-480, 110), (-580, 40)]
    _shape(cr, hull, WOOD, 7, holes=(14, 18, 3.2))
    band(cr, [(-560, 16), (560, 16)], 22, GOLD, spacing=14)
    band(cr, [(-470, 92), (500, 92)], 14, RED, spacing=12, hole_r=2.2)
    for x in range(-420, 461, 110):
        _flower(cr, x, 54, 22, RED if (x // 110) % 2 else GOLD, 8)
    neck = [(560, 0), (612, -40), (640, -120), (636, -190), (668, -232), (720, -230), (744, -212), (700, -204),
            (676, -186), (672, -120), (650, -40), (600, 30)]
    _shape(cr, neck, (1.0, 0.95, 0.86), 6)
    holes_line(cr, [(600, -10), (640, -90), (650, -170)], 16, 2.6)
    _shape(cr, [(744, -212), (790, -204), (744, -196)], SAFFRON, 3)
    cr.new_path()
    cr.arc(696, -218, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    stern = [(-600, -40), (-660, -110), (-650, -170), (-610, -180), (-600, -150), (-630, -130), (-614, -90),
             (-570, -40)]
    _shape(cr, stern, GOLD, 5, holes=(9, 13, 2.4))


def _boat_hut(cr):
    """The hut on the deck (pivot at the middle of the deck): leaf walls, a thatched roof with garlands, flowers."""
    wall = [(-260, 0), (260, 0), (260, -260), (-260, -260)]
    _shape(cr, wall, (0.86, 0.74, 0.40), 6, smooth=False)
    for x in range(-240, 251, 40):
        ink(cr, [(x, -250), (x, -6)], 3, smooth=False, col=(0.62, 0.48, 0.22))
    door = [(-70, 0), (-70, -170), (-40, -210), (40, -210), (70, -170), (70, 0)]
    _shape(cr, door, (0.30, 0.18, 0.10), 5, smooth=False)
    roof = [(-330, -240), (-260, -300), (-120, -420), (0, -470), (120, -420), (260, -300), (330, -240)]
    _shape(cr, roof, (0.94, 0.76, 0.36), 7, smooth=False)
    for k in range(9):
        x = -280 + 70 * k
        ink(cr, [(x, -248), (x * 0.3, -440)], 2.5, smooth=False, col=(0.70, 0.52, 0.22))
    for k in range(13):                                   # a marigold string along the eaves
        x = -300 + 50 * k
        _flower(cr, x, -236 + 14 * math.sin(k * 1.3), 16, SAFFRON if k % 2 else GOLD, 8)
    for x in (-180, 180):
        _flower(cr, x, -130, 24, RED, 8)
    cr.new_path()
    cr.arc(0, -480, 16, 0, 2 * math.pi)
    leather(cr, GOLD, 4)


register("c6_boat_hull", (-680, -250, 800, 120), _boat_hull)
register("c6_boat_hut", (-340, -500, 340, 10), _boat_hut)


# ------------------------------------------------------------------ baby Rama


def _rama_cradle(cr):
    """A decorated wooden cradle on rockers (pivot at the bottom middle) with baby Rama asleep in it: blue skin, dark
    curls with a small gold ornament, a tilak, a peaceful smile; a yellow blanket."""
    _shape(cr, [(-236, -200), (-200, -236), (-120, -232), (-110, -196)], (1.0, 0.97, 0.90), 4)   # pillow
    _shape(cr, [(-90, -196), (-20, -250), (120, -262), (200, -236), (214, -196)], (1.0, 0.84, 0.30), 5)  # blanket
    dots_in(cr, lambda: spath(cr, [(-80, -204), (-14, -244), (118, -254), (194, -232), (204, -204)]), 18, 2.6)
    _flower(cr, 90, -230, 16, RED, 8)
    cx, cy = -150, -268                                   # his face, sleeping, propped on the pillow
    for k in range(7):
        a = math.pi * (1.05 + 0.9 * k / 6)
        cr.new_path()
        cr.arc(cx + 70 * math.cos(a), cy + 66 * math.sin(a) - 6, 22, 0, 2 * math.pi)
        leather(cr, HAIR, 3)
    cr.new_path()
    ell(cr, cx, cy, 70, 64)
    leather(cr, RAMA_SKIN, 5)
    for k in range(5):
        cr.new_path()
        cr.arc(cx - 44 + 22 * k, cy - 58 + 4 * abs(k - 2), 16, 0, 2 * math.pi)
        leather(cr, HAIR, 3)
    _jewel(cr, cx, cy - 66, 10, GOLD)
    for sx in (-1, 1):
        ink(cr, [(cx + sx * 34 - 14, cy - 2), (cx + sx * 34, cy + 6), (cx + sx * 34 + 14, cy - 2)], 4.5)
        cr.new_path()
        cr.arc(cx + sx * 46, cy + 22, 9, 0, 2 * math.pi)
        cr.set_source_rgb(0.56, 0.62, 0.98)
        cr.fill()
    ink(cr, [(cx - 12, cy + 30), (cx, cy + 38), (cx + 12, cy + 30)], 3.5, col=(0.62, 0.12, 0.16))
    ink(cr, [(cx, cy - 46), (cx, cy - 28)], 4, col=RED)
    _shape(cr, [(-60, -238), (-50, -300), (-34, -316), (-18, -306), (-30, -244)], RAMA_SKIN, 4)   # a little hand
    basket = [(-240, -220), (240, -220), (210, -90), (-210, -90)]
    _shape(cr, basket, RED, 6, holes=(11, 15, 3))
    dots_in(cr, lambda: poly(cr, [(-190, -200), (190, -200), (170, -110), (-170, -110)]), 24, 4, shape="d")
    band(cr, [(-246, -220), (246, -220)], 20, GOLD, spacing=12)
    for x in (-120, 0, 120):
        _flower(cr, x, -150, 22, GOLD, 8)
    for s in (-1, 1):
        _shape(cr, [(s * 150, -96), (s * 170, -96), (s * 180, -30), (s * 160, -30)], WOOD, 4, smooth=False)
    rocker = [(-300, -40), (-200, -14), (0, -4), (200, -14), (300, -40), (300, -20), (200, 6), (0, 16), (-200, 6),
              (-300, -20)]
    _shape(cr, rocker, WOOD, 5)


register("c6_rama_cradle", (-320, -370, 320, 30), _rama_cradle)


# ------------------------------------------------------------------ rig helpers for the scenes


def kala_rig(k):
    return KALAS[k % len(KALAS)]
