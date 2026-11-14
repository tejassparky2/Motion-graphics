"""The leather cast and props for the Manthara reel (videos/manthara.py), in the Togalu Gombeyaata style of the earlier
reels: profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets,
modelled on no actor and no film. Every sprite name starts with "mt_".

Cast (one look each, kept the same through the video):
  MANTHARA   Kaikeyi's old maid: a hump on her back (the figure also leans forward), her mustard sari's end pulled over
             her head like a hood, grey hair, a hooked nose and narrow eyes under a heavy brow, a small nose ring, no
             crown. Faces: sly (default), angry, smile (a thin smile). Never a monster: a sharp old woman.
  KAUSALYA   "the elder queen" (named only as that): a cream sari with a red blouse and the same queen's crown as
             Kaikeyi.
  GANDHARVI  the heavenly singer Brahma sends down: pale gold skin, a sky-blue sari with a pink blouse, a flower in her
             hair, a veena.
Kaikeyi, Rama, Bharata and Dasharatha come from kaikeyi_cast; Ravana from ravana_cast; Brahma from six_cast_c.
Props: the gold necklace Kaikeyi gives (mt_haar), a single loose bead, a veena, the decorated city of Ayodhya
(mt_city: towers, a dome, flags and garlands strung between), the terrace railing (mt_rail), a festive flag, the
servant's fan (mt_fan), a travel bundle on a stick (mt_bundle), and a boon light (drawn in the scenes).
"""
import math

import kaikeyi_cast as K
import puppet_cast as C
from puppet_cast import HAIR, _jewel, _shape, woman
from puppet_core import (BROWN, DRED, GOLD, GREEN, INK, PALE, RED, SAFFRON, band, dots_in, holes_line, ink, leather,
                         poly, punch, register, spath)

MT_SKIN = (0.88, 0.62, 0.42)
MT_SARI = (0.80, 0.58, 0.26)          # mustard
MT_HOOD = (0.64, 0.42, 0.18)          # the sari's end over her head
MT_BORDER = (0.48, 0.13, 0.10)
MT_CHOLI = (0.30, 0.42, 0.24)
GREY = (0.80, 0.80, 0.84)
KS_SKIN = (0.98, 0.76, 0.56)
KS_SARI = (0.99, 0.93, 0.80)
GD_SKIN = (1.0, 0.86, 0.62)
GD_SARI = (0.58, 0.78, 1.0)
GD_CHOLI = (0.98, 0.56, 0.74)
WOOD = (0.58, 0.34, 0.16)
STONE = (0.92, 0.78, 0.56)


# ------------------------------------------------------------------ Manthara


def manthara_head(cr, mood="sly"):
    hood = [(-6, -196), (34, -190), (40, -176), (6, -170), (-30, -150), (-50, -100), (-56, -30), (-40, 14),
            (-96, 30), (-112, -40), (-108, -120), (-84, -172), (-50, -194)]
    _shape(cr, hood, MT_HOOD, 5)
    dots_in(cr, lambda: spath(cr, hood), 16, 2.8)
    band(cr, [(-4, -192), (-62, -180), (-100, -128), (-108, -40), (-98, 22)], 14, MT_BORDER, spacing=11, hole_r=2.2)
    face = [(-20, 6), (-26, -36), (-40, -80), (-44, -126), (-30, -166), (4, -178), (34, -166), (46, -142),
            (50, -126), (58, -112), (84, -84), (86, -72), (62, -76), (58, -66), (50, -58), (52, -46), (40, -30),
            (22, -26), (16, 6)]
    _shape(cr, face, MT_SKIN, 6)
    _shape(cr, [(-28, -150), (2, -172), (32, -164), (20, -156), (-6, -150)], GREY, 3)      # grey hair under the hood
    if mood == "angry":
        ink(cr, [(12, -134), (34, -126), (50, -128)], 5)                                    # brow down to the nose
        cr.new_path()
        cr.move_to(16, -116)
        cr.curve_to(24, -124, 38, -124, 46, -114)
        cr.curve_to(38, -110, 24, -110, 16, -116)
        cr.close_path()
        leather(cr, PALE, 3.5)
        cr.arc(34, -116, 4.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        ink(cr, [(46, -50), (54, -54), (58, -46)], 3.5, col=RED)                            # mouth turned down
    else:
        ink(cr, [(10, -140), (30, -144), (50, -136)], 5)                                    # heavy brow, raised end
        cr.new_path()
        cr.move_to(16, -118)
        cr.curve_to(26, -126, 38, -126, 48, -118)
        cr.curve_to(38, -112, 26, -112, 16, -118)
        cr.close_path()
        leather(cr, PALE, 3.5)
        cr.arc(38, -118, 4.5, 0, 2 * math.pi)                                               # looking sideways
        cr.set_source_rgb(*INK)
        cr.fill()
        if mood == "smile":
            ink(cr, [(44, -56), (54, -54), (62, -62)], 3.5, col=RED)
        else:
            ink(cr, [(46, -54), (58, -56)], 3.5, col=RED)
    ink(cr, [(12, -108), (6, -98)], 2.5)                                                    # wrinkles
    ink(cr, [(16, -92), (8, -84)], 2.5)
    ink(cr, [(38, -82), (30, -70)], 2.5)
    cr.new_path()
    cr.arc(70, -74, 6, 0.6, 2 * math.pi - 0.6)                                               # nose ring
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    cr.new_path()
    cr.arc(26, -60, 4, 0, 2 * math.pi)                                                      # a mole
    cr.set_source_rgb(*INK)
    cr.fill()
    _jewel(cr, -14, -60, 8, GOLD)                                                           # plain earring


def manthara_body(cr):
    hump = [(-30, -300), (-70, -300), (-118, -262), (-136, -200), (-120, -140), (-80, -112), (-40, -120)]
    _shape(cr, hump, MT_HOOD, 5)
    dots_in(cr, lambda: spath(cr, hump), 14, 2.6)
    band(cr, [(-122, -238), (-134, -190), (-118, -142)], 12, MT_BORDER, spacing=10, hole_r=2.0)
    C.woman_body(cr, dict(skin=MT_SKIN, skirt=MT_SARI, choli=MT_CHOLI, border=MT_BORDER, pallu_col=MT_HOOD,
                          gem=MT_BORDER, pallu=False))


MANTHARA = woman("mt_manthara", skin=MT_SKIN, skirt=MT_SARI, choli=MT_CHOLI, border=MT_BORDER, pallu_col=MT_HOOD,
                 gem=MT_BORDER, hands=("open", "open"))
register("mt_manthara_body", (-160, -320, 170, 490), manthara_body)
MT_MOODS = ("sly", "angry", "smile")
for _m in MT_MOODS:
    register("mt_manthara_head" + ("" if _m == "sly" else "_" + _m), (-130, -210, 100, 40),
             lambda cr, m=_m: manthara_head(cr, m))


# ------------------------------------------------------------------ the elder queen and the heavenly singer


def kausalya_head(cr):
    C.woman_head(cr, dict(skin=KS_SKIN, flower=RED))
    K.queen_crown(cr)


KAUSALYA = woman("mt_kausalya", skin=KS_SKIN, skirt=KS_SARI, choli=RED, border=GOLD, pallu_col=(0.96, 0.84, 0.62),
                 gem=RED, hands=("open", "open"))
register("mt_kausalya_head", (-130, -300, 110, 40), kausalya_head)

GANDHARVI = woman("mt_gandh", skin=GD_SKIN, skirt=GD_SARI, choli=GD_CHOLI, border=GOLD, pallu_col=(0.74, 0.88, 1.0),
                  gem=GD_CHOLI, flower=GD_CHOLI, hands=("open", "open"))


# ------------------------------------------------------------------ props


def _haar(cr):
    """The necklace: a loop of gold beads with a red pendant (pivot at the loop's top)."""
    for i in range(23):
        a = math.pi * (0.06 + 0.88 * i / 22)
        x, y = 110 * math.cos(a), 150 * math.sin(a)
        cr.new_path()
        cr.arc(-x, y, 11 if i % 4 else 14, 0, 2 * math.pi)
        leather(cr, GOLD if i % 4 else RED, 2.5)
        punch(cr, [(-x, y)], 3)
    _shape(cr, [(-26, 150), (26, 150), (0, 214)], RED, 4, smooth=False)
    _jewel(cr, 0, 172, 13, GREEN)


register("mt_haar", (-130, -20, 130, 230), _haar)


def _bead(cr):
    cr.new_path()
    cr.arc(0, 0, 13, 0, 2 * math.pi)
    leather(cr, GOLD, 2.5)
    punch(cr, [(0, 0)], 3.5)


register("mt_bead", (-16, -16, 16, 16), _bead)


def _veena(cr):
    """A veena held across the body (pivot at the neck's middle): a long neck, two round gourds, frets, strings."""
    _shape(cr, [(-260, -16), (250, -16), (250, 16), (-260, 16)], WOOD, 4, smooth=False)
    for gx, gr in ((-250, 70), (210, 90)):
        cr.new_path()
        cr.arc(gx, 40 if gx > 0 else 30, gr, 0, 2 * math.pi)
        leather(cr, (0.86, 0.52, 0.22), 4)
        dots_in(cr, lambda gx=gx, gr=gr: (cr.new_path(), cr.arc(gx, 40 if gx > 0 else 30, gr * 0.8, 0, 2 * math.pi)),
                10, 3)
    for i in range(12):
        x = -200 + 34 * i
        ink(cr, [(x, -16), (x, 16)], 3)
    ink(cr, [(-260, -4), (250, -4)], 1.5)
    ink(cr, [(-260, 6), (250, 6)], 1.5)
    _shape(cr, [(250, -20), (290, -60), (300, -40), (264, 0)], GOLD, 3)


register("mt_veena", (-330, -80, 310, 140), _veena)


def _city(cr):
    """Ayodhya decorated: towers and a gold dome behind a wall, flags on every top, garlands strung between
    (pivot at the wall's bottom centre; ~1100 units wide)."""
    wall = [(-560, 0), (-560, -170), (560, -170), (560, 0)]
    _shape(cr, wall, STONE, 5, smooth=False)
    for x in range(-540, 560, 60):
        _shape(cr, [(x, -170), (x + 34, -170), (x + 34, -200), (x, -200)], STONE, 3, smooth=False)
    holes_line(cr, [(-540, -90), (540, -90)], 30, 4)
    tops = []
    for x, w_, h_, dome in ((-430, 120, 420, False), (-230, 150, 520, True), (0, 220, 640, True),
                            (240, 150, 500, True), (440, 120, 400, False)):
        body = [(x - w_ / 2, -170), (x - w_ / 2, -h_), (x + w_ / 2, -h_), (x + w_ / 2, -170)]
        _shape(cr, body, STONE if dome else (0.96, 0.70, 0.42), 5, smooth=False)
        for j in range(2, int((h_ - 170) / 90) + 1):
            cr.new_path()
            cr.arc(x, -170 - 90 * j + 40, 14, math.pi, 0)
            cr.line_to(x + 14, -170 - 90 * j + 66)
            cr.line_to(x - 14, -170 - 90 * j + 66)
            cr.close_path()
            cr.set_source_rgb(*INK)
            cr.fill()
        if dome:
            cr.new_path()
            cr.arc(x, -h_, w_ * 0.48, math.pi, 0)
            cr.close_path()
            leather(cr, GOLD, 5)
            dots_in(cr, lambda x=x, w_=w_, h_=h_: (cr.new_path(), cr.arc(x, -h_, w_ * 0.4, math.pi, 0)), 12, 3)
            top = (x, -h_ - w_ * 0.48)
        else:
            _shape(cr, [(x - w_ / 2 - 10, -h_), (x, -h_ - 90), (x + w_ / 2 + 10, -h_)], RED, 4, smooth=False)
            top = (x, -h_ - 90)
        ink(cr, [top, (top[0], top[1] - 80)], 4)
        _shape(cr, [(top[0], top[1] - 80), (top[0] + 70, top[1] - 64), (top[0], top[1] - 46)],
               SAFFRON if dome else GREEN, 3, smooth=False)
        tops.append((x, -h_ + 30))
    for (xa, ya), (xb, yb) in zip(tops, tops[1:]):                      # garlands strung between the towers
        n = 9
        for i in range(n + 1):
            u = i / n
            gx = xa + (xb - xa) * u
            gy = ya + (yb - ya) * u + 90 * math.sin(math.pi * u)
            cr.new_path()
            cr.arc(gx, gy, 12, 0, 2 * math.pi)
            leather(cr, SAFFRON if i % 2 else (1.0, 0.86, 0.30), 2)


register("mt_city", (-600, -900, 600, 10), _city)


def _rail(cr):
    """A terrace railing (pivot at its top centre; 1200 wide)."""
    _shape(cr, [(-600, 0), (600, 0), (600, 34), (-600, 34)], STONE, 5, smooth=False)
    for x in range(-570, 600, 76):
        _shape(cr, [(x - 16, 34), (x + 16, 34), (x + 24, 120), (x + 10, 190), (x - 10, 190), (x - 24, 120)], STONE, 4)
    _shape(cr, [(-600, 190), (600, 190), (600, 240), (-600, 240)], STONE, 5, smooth=False)
    holes_line(cr, [(-580, 214), (580, 214)], 40, 4)


register("mt_rail", (-610, -10, 610, 250), _rail)


def _fan(cr):
    """A servant's hand fan (pivot at the handle's end)."""
    ink(cr, [(0, 0), (0, -170)], 7, col=WOOD)
    pts = [(0, -160)] + [(150 * math.cos(math.radians(a)), -160 + 150 * math.sin(math.radians(a)))
                         for a in range(-160, -15, 12)]
    _shape(cr, pts, (0.92, 0.74, 0.40), 4, smooth=False)
    for a in range(-150, -20, 18):
        ink(cr, [(0, -160), (140 * math.cos(math.radians(a)), -160 + 140 * math.sin(math.radians(a)))], 2)


register("mt_fan", (-160, -320, 160, 10), _fan)


def _bundle(cr):
    """A travel bundle tied to a stick (pivot at the stick's lower end)."""
    ink(cr, [(0, 0), (150, -200)], 8, col=WOOD)
    blob = [(150, -200), (210, -240), (250, -190), (230, -130), (170, -120), (130, -160)]
    _shape(cr, blob, (0.86, 0.72, 0.52), 4)
    dots_in(cr, lambda: spath(cr, blob), 12, 2.6)
    ink(cr, [(160, -200), (210, -210)], 3)


register("mt_bundle", (-10, -260, 270, 10), _bundle)


# ------------------------------------------------------------------ Saraswati (version 3: the Ramcharitmanas reveal)

SR_SKIN = (1.0, 0.86, 0.66)


def saraswati_head(cr):
    C.woman_head(cr, dict(skin=SR_SKIN, flower=PALE))
    K.queen_crown(cr)


SARAS = woman("mt_saras", skin=SR_SKIN, skirt=(0.99, 0.97, 0.92), choli=(0.99, 0.80, 0.30), border=GOLD,
              pallu_col=(0.97, 0.94, 0.86), gem=RED, flower=PALE, hands=("open", "open"))
register("mt_saras_head", (-130, -300, 110, 40), saraswati_head)
