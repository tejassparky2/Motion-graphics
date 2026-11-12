"""Builder C's extra leather cast and props for long video 2 (videos/yamlok_yatra.py, scenes_yy_c: Yama's court, the
eastern gate, the ending), in the Togalu Gombeyaata style of the reels (puppet_cast, ruru_cast, garuda_cast...):
profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on
no actor and no film. Every sprite name starts with "yc_". Dhaniram, his soul and Bhola come from yy_cast (builder A).

Cast and props here:
  YAMA'S BUFFALO  his mount for the terrible form: a huge dark slate-blue water buffalo facing +x, a red-and-gold saddle
                  cloth, gold anklets, a gold bell on a red cord; the head (with its great back-swept horns and a
                  fierce, heavy-browed eye) is its own sprite so it can toss and snort. Fierce, never monstrous.
  YAMA            ruru_cast's Yama Dharmaraja; here a fierce face (frowning brow) under a taller, two-layer flame halo
                  for the terrible form (yc_yama_head_fierce), and his kneeling legs (yc_yama_kneel) for the foot
                  washing. His smile comes from six_cast_b (sb_yama_head_smile).
  SHRAVANAS       the sons of Brahma who hear and see everything: pale silver-blue figures with gold ornaments, an
                  oversized ear with a gold ring and one big wide-open eye; a small gold crown with a pale-blue flare.
  THE MUNIM       Dhaniram's accountant (in Dhaniram's thought): a round black cap, round spectacles, a pen behind the
                  ear, a moustache, a cream kurta-like shawl; faces calm and sly (a wink); sits behind a low desk.
Props: four city gates (dark iron for the south with a buffalo-horn crest, gold with a sunburst for the east, pale stone
for north and west; yc_gate_<S|E|P>), a celestial chariot with a domed canopy and a door that opens (yc_ratha,
yc_ratha_door), a Parijata tree (white flowers with orange hearts) and one flower, a leather heart, a mountain range,
the munim's desk and ledger, a roti. Dhaniram's safe and Bhola's water pot are yy_cast's.
"""
import math

import arjuna_cast as A
import kaikeyi_cast as K
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
import garuda_cast as GC  # noqa: F401  (messengers, Chitragupta, the noose, rice-balls, the cow)
import six_cast_b as SB    # noqa: F401  (Yama's smile and shame faces, his hall, the horn crest)
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BROWN, DRED, GOLD, INK, PALE, RED, SAFFRON, almond_eye, band, dots_in, ell, holes_line, ink,
                         leather, poly, punch, register, rivet, spath)

BUF = (0.30, 0.31, 0.40)               # the buffalo: dark slate blue
BUF2 = (0.22, 0.22, 0.30)              # its far legs
BUF3 = (0.42, 0.42, 0.52)              # the muzzle
HORN = (0.70, 0.64, 0.54)
HORN2 = (0.52, 0.47, 0.40)
HOOF = (0.16, 0.14, 0.16)
SHR_SKIN = (0.62, 0.76, 0.98)          # the Shravanas: silver-blue
SHR_CLOTH = (0.92, 0.94, 1.0)
SHR_SASH = (0.42, 0.60, 0.96)
MN_SKIN = (0.92, 0.66, 0.44)           # the munim
MN_KURTA = (0.98, 0.93, 0.80)
CAP = (0.14, 0.12, 0.14)
LEDGER = (0.72, 0.12, 0.10)            # a red bahi-khata
PAGE = (0.99, 0.93, 0.74)
WOOD = (0.56, 0.33, 0.15)
WOOD2 = (0.72, 0.46, 0.22)
DSTONE = (0.36, 0.34, 0.42)            # the south gate
DSTONE2 = (0.24, 0.23, 0.30)
IRON = (0.30, 0.30, 0.36)
PSTONE = (0.86, 0.72, 0.52)            # north / west gates
PSTONE2 = (0.70, 0.54, 0.36)
GOLD2 = (0.96, 0.66, 0.16)
LEAFG = (0.20, 0.50, 0.24)
LEAFG2 = (0.30, 0.62, 0.30)
FLOWER = (1.0, 0.99, 0.95)
HEART = (0.86, 0.16, 0.14)
ROCK = (0.62, 0.54, 0.48)
ROCK2 = (0.48, 0.40, 0.36)
SNOW = (0.98, 0.98, 1.0)
ROTI = (0.94, 0.76, 0.44)

BUF_NECK = (330.0, -640.0)             # the buffalo: the head's pivot on the body
BUF_SEAT = (-70.0, -712.0)             # where Yama's hip sits on its back
RATHA_DECK = 330.0                     # the chariot: the floor of the car above the ground
RATHA_DOOR = (-40.0, -330.0)           # the door's hinge (its top-left corner) on the car
RATHA_DOOR_W, RATHA_DOOR_H = 200.0, 400.0
GATE_DOOR = (110.0, 330.0)             # a city gate's doorway: half width, height


def _tube(cr, p0, p1, w0, w1, col, lw=5.0):
    """A tapered limb from p0 to p1 (half widths w0, w1)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    _shape(cr, [(p0[0] + nx * w0, p0[1] + ny * w0), (p1[0] + nx * w1, p1[1] + ny * w1),
                (p1[0] - nx * w1, p1[1] - ny * w1), (p0[0] - nx * w0, p0[1] - ny * w0)], col, lw)


# ------------------------------------------------------------------ Yama's buffalo


def _buf_leg(cr, x, top, col, near=True):
    w = 66 if near else 58
    leg = [(x - w, top), (x + w, top), (x + w * 0.72, -260), (x + w * 0.55, -90), (x + w * 0.62, -30),
           (x - w * 0.62, -30), (x - w * 0.55, -90), (x - w * 0.8, -260)]
    _shape(cr, leg, col, 5)
    _shape(cr, [(x - w * 0.66, -34), (x + w * 0.66, -34), (x + w * 0.74, 0), (x - w * 0.74, 0)], HOOF, 4,
           smooth=False)
    ink(cr, [(x, -30), (x, -2)], 3, col=(0.4, 0.4, 0.45))
    if near:
        band(cr, [(x - w * 0.6, -70), (x + w * 0.6, -70)], 16, GOLD, spacing=11, hole_r=2.2)


def _buf_body(cr):
    """The buffalo's body facing +x (pivot on the ground under its middle; the neck joint at BUF_NECK)."""
    for x in (-250, 170):                                                          # far legs
        _buf_leg(cr, x, -420, BUF2, near=False)
    tail = [(-436, -600), (-480, -470), (-490, -300), (-470, -296), (-458, -470), (-418, -590)]
    _shape(cr, tail, BUF, 4)
    _shape(cr, [(-506, -320), (-460, -320), (-454, -230), (-480, -206), (-510, -236)], HOOF, 3)
    body = [(-450, -520), (-430, -620), (-340, -676), (-160, -690), (40, -708), (160, -768), (260, -780),
            (350, -730), (392, -630), (380, -500), (318, -404), (190, -350), (0, -336), (-200, -344), (-350, -384),
            (-440, -450)]
    _shape(cr, body, BUF, 7, holes=(16, 24, 3.2))
    for k in range(3):                                                              # the ribs, faintly
        ink(cr, [(-60 + 60 * k, -600), (-70 + 60 * k, -470), (-50 + 60 * k, -400)], 3, col=(0.18, 0.18, 0.24))
    ink(cr, [(-330, -600), (-380, -500), (-360, -420)], 4, col=(0.18, 0.18, 0.24))   # the haunch
    cloth = [(-250, -688), (40, -712), (150, -760), (160, -520), (-40, -488), (-240, -496)]
    _shape(cr, cloth, RED, 5)
    dots_in(cr, lambda: spath(cr, cloth), 24, 3.2, shape="d")
    band(cr, [(-240, -508), (-40, -500), (156, -532)], 26, GOLD, spacing=13, hole_r=2.4)
    for k in range(11):                                                             # the fringe
        x = -232 + 38 * k
        y = -496 + 2 * k - (14 * max(0, k - 5))
        ink(cr, [(x, y), (x, y + 34)], 4, col=GOLD)
    _flower(cr, -50, -610, 34, GOLD, 8)
    _jewel(cr, -50, -610, 12, RED)
    for x in (-320, 230):                                                           # near legs
        _buf_leg(cr, x, -440, BUF, near=True)
    rivet(cr, 230, -440, 10)
    rivet(cr, -320, -440, 10)


def _horn(cr, dx, dy, col, s=1.0):
    """A water buffalo's horn in profile: broad at the base on top of the head, arching up and back over the neck in
    a wide crescent, the tip turning down and back; growth rings across it."""
    outer = [(200, -50), (218, -140), (186, -222), (118, -274), (24, -292), (-60, -276), (-114, -238), (-128, -196),
             (-112, -160)]
    inner = [(-112, -160), (-86, -192), (-34, -214), (38, -218), (98, -192), (128, -140), (128, -60)]
    pts = [(dx + x * s, dy + y * s) for x, y in outer + inner]
    _shape(cr, pts, col, 5)
    for k in range(7):                                                              # growth rings
        i = k + 1
        ox, oy = outer[i]
        ix, iy = inner[len(inner) - 1 - min(i, len(inner) - 1)]
        ink(cr, [(dx + (0.75 * ox + 0.25 * ix) * s, dy + (0.75 * oy + 0.25 * iy) * s),
                 (dx + (0.3 * ox + 0.7 * ix) * s, dy + (0.3 * oy + 0.7 * iy) * s)], 3, smooth=False, col=HORN2)


def _buf_head(cr):
    """The buffalo's neck and head (pivot at the neck joint): a long, low head with a broad muzzle, the great
    crescent horns arching back over the neck (the far one behind), a small drooping ear, a heavy brow over a fierce
    pale eye, a gold forehead jewel, a gold bell on a red cord."""
    _horn(cr, 30, -24, HORN2, 0.94)                                                 # the far horn
    neck = [(-80, -96), (60, -126), (160, -96), (210, -20), (196, 70), (80, 110), (-60, 100)]
    _shape(cr, neck, BUF, 6)
    for k in range(4):                                                              # neck folds
        ink(cr, [(30 + 30 * k, 60), (44 + 30 * k, 96)], 3, col=(0.18, 0.18, 0.24))
    head = [(110, -90), (200, -112), (270, -72), (330, 8), (372, 98), (368, 160), (320, 192), (250, 172),
            (180, 112), (120, 40), (100, -30)]
    _shape(cr, head, BUF, 6)
    cr.new_path()
    ell(cr, 330, 152, 46, 36, 0.5)
    leather(cr, BUF3, 4)
    punch(cr, [(348, 144)], 7)
    ink(cr, [(296, 182), (330, 190)], 3)
    ear = [(126, -30), (64, -48), (30, -30), (64, -10), (126, -12)]
    _shape(cr, ear, BUF2, 4)
    almond_eye(cr, 222, -32, 42, 15, col=(1.0, 0.86, 0.66))
    ink(cr, [(188, -64), (222, -72), (258, -54)], 11)                               # the heavy brow
    _jewel(cr, 270, -78, 13, GOLD)
    _horn(cr, 0, 0, HORN, 1.0)                                                      # the near horn
    band(cr, [(40, 96), (100, 124), (170, 100)], 16, RED, holes=False, lw=3)        # the bell on its cord
    _shape(cr, [(86, 124), (118, 124), (128, 170), (76, 170)], GOLD, 3.5, smooth=False)
    punch(cr, [(102, 162)], 4)


register("yc_buf_body", (-530, -800, 420, 20), _buf_body)
register("yc_buf_head", (-310, -360, 380, 200), _buf_head)


# ------------------------------------------------------------------ Yama: the fierce face, kneeling legs


_YM_O = dict(skin=RU.YM_SKIN, hair=True, moustache=True, tilak=True)


def _fire_halo(cr):
    """A taller, wilder flame halo: dark red flames behind orange ones."""
    for col, r0, r1, n in ((DRED, 230, 150, 23), ((0.95, 0.42, 0.10), 178, 128, 19)):
        pts = []
        for i in range(n):
            a = math.pi * (0.55 + 1.0 * i / (n - 1))
            r = r0 if i % 2 == 0 else r1
            r *= 1 + 0.08 * math.sin(i * 2.3)
            pts.append((-30 + r * math.cos(a) * 1.05, -190 + r * math.sin(a) * 1.12))
        pts += [(-40, -150), (0, -160)]
        _shape(cr, pts, col, 5, smooth=False, holes=(14, 15, 3))


def yama_fierce(cr):
    """ruru_cast.yama_head for the terrible form: the angry face, the same crown, a fire halo."""
    _fire_halo(cr)
    RU.rface(cr, _YM_O, "angry")
    ink(cr, [(20, -88), (8, -78), (14, -66)], 5, col=HAIR)
    R.kirita(cr, GOLD, None, tall=1.36, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.36
    for sx in (-1, 1):
        _shape(cr, [(sx * 30, -170), (sx * 66, h(-240)), (sx * 52, h(-290)), (sx * 40, h(-240)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 50, h(-254), 7, RED)
    _jewel(cr, 2, h(-292), 10, (0.16, 0.66, 0.40))


register("yc_yama_head_fierce", (-260, -560, 140, 120), yama_fierce)
register("yc_yama_kneel", (-260, -60, 250, 260), lambda cr: K.kneel_legs(cr, RU.YM_SKIN, RU.YM_DHOTI, GOLD, 1.18))


# ------------------------------------------------------------------ the Shravanas


_SHR_O = dict(skin=SHR_SKIN, hair=True, moustache=False, tilak=True, earring=False)


def shr_head(cr, mood="calm"):
    """A Shravana: an oversized ear with a gold ring, one big wide-open eye, a small gold crown with a pale-blue
    flare."""
    A.face(cr, _SHR_O, "smile" if mood == "smile" else "calm")
    if mood != "smile":
        cr.new_path()                                                               # the big eye over the small one
        ell(cr, 34, -118, 30, 16)
        cr.set_source_rgb(*SHR_SKIN)
        cr.fill()
        almond_eye(cr, 36, -118, 58, 22, col=PALE)
        ink(cr, [(8, -150), (36, -160), (66, -148)], 4.5)
    ear = [(-4, -150), (-34, -176), (-72, -166), (-92, -118), (-86, -62), (-58, -32), (-26, -42), (-30, -70),
           (-12, -96)]
    _shape(cr, ear, SHR_SKIN, 5, holes=(10, 14, 2.4))
    ink(cr, [(-26, -138), (-56, -142), (-70, -110), (-62, -76), (-44, -66)], 4)
    ink(cr, [(-40, -118), (-52, -102), (-44, -88)], 3)
    for r, col in ((20, GOLD), (11, (0.42, 0.60, 0.96))):
        cr.new_path()
        cr.arc(-66, -40, r, 0, 2 * math.pi)
        leather(cr, col, 3.5)
    R.kirita(cr, GOLD, None, tall=0.7, flare=(0.55, 0.78, 1.0))
    _jewel(cr, 2, -150 + (-282 + 150) * 0.7, 9, (0.42, 0.60, 0.96))


SHR = man("yc_shr", skin=SHR_SKIN, bulk=0.92, dhoti=SHR_CLOTH, border=GOLD, pleat=GOLD, sash=SHR_SASH, neck=GOLD,
          crown="tiara", halo=False, hair=False, earring=False, tilak=False, thread=True, hands=("open", "open"))
register("yc_shr_head", (-200, -400, 120, 100), shr_head)
register("yc_shr_head_smile", (-200, -400, 120, 100), lambda cr: shr_head(cr, "smile"))


# ------------------------------------------------------------------ the munim (in Dhaniram's thought)


_MN_O = dict(skin=MN_SKIN, hair=False, moustache=True, tilak=True, earring=False)


def munim_head(cr, mood="calm"):
    """The munim: a round black cap, round spectacles, a pen behind his ear, a moustache; mood calm | sly (a wink and
    a smile)."""
    A.face(cr, _MN_O, "smile" if mood == "sly" else "calm")
    cap = [(-58, -128), (-60, -176), (-36, -206), (10, -214), (48, -200), (60, -170), (58, -134)]
    _shape(cr, cap, CAP, 4)
    band(cr, [(-58, -140), (0, -146), (58, -140)], 14, (0.40, 0.08, 0.10), holes=False, lw=3)
    holes_line(cr, [(-40, -184), (0, -200), (40, -186)], 14, 2.2)
    cr.new_path()                                                                   # the spectacles
    cr.arc(36, -116, 24, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    ink(cr, [(12, -118), (-12, -114)], 4)
    if mood == "sly":
        ink(cr, [(20, -112), (52, -112)], 5)                                        # the winking eye, shut
    _shape(cr, [(-30, -150), (-6, -150), (-4, -140), (-60, -86), (-70, -92)], (0.62, 0.36, 0.14), 3)  # the pen
    _shape(cr, [(-70, -92), (-60, -86), (-76, -76)], INK, 2, smooth=False)


MUNIM = man("yc_munim", skin=MN_SKIN, bulk=1.0, dhoti=MN_KURTA, border=DRED, pleat=MN_KURTA, sash=(0.80, 0.30, 0.14),
            neck=BROWN, crown="tiara", halo=False, hair=False, earring=False, tilak=False, robe=MN_KURTA,
            hands=("open", "open"))
register("yc_munim_head", (-130, -260, 110, 40), munim_head)
register("yc_munim_head_sly", (-130, -260, 110, 40), lambda cr: munim_head(cr, "sly"))


def _desk(cr):
    """A low slanted writing desk (pivot at its bottom centre; the ledger lies on its top, centred at (0, -200))."""
    _shape(cr, [(-230, -190), (230, -230), (240, -200), (-220, -160)], WOOD2, 5, smooth=False)
    _shape(cr, [(-220, -164), (236, -204), (220, 0), (-200, 0)], WOOD, 6, smooth=False, holes=(12, 18, 2.6))
    for x in (-120, 0, 120):
        band(cr, [(x, -170 - x * 0.08), (x, -10)], 10, GOLD, holes=False, lw=3)
    _flower(cr, 0, -90, 28, GOLD, 8)


def _ledger(cr):
    """The munim's open red ledger (bahi-khata) seen from above-front (pivot at its centre): two cream pages in a red
    cloth binding (the scenes write on the right page)."""
    _shape(cr, [(-250, -110), (250, -110), (262, 110), (-262, 110)], LEDGER, 6, smooth=False, holes=(10, 18, 2.6))
    for sx in (-1, 1):
        _shape(cr, [(sx * 6, -96), (sx * 236, -96), (sx * 244, 96), (sx * 6, 96)], PAGE, 4, smooth=False)
        for k in range(5):
            ink(cr, [(sx * 26, -60 + 34 * k), (sx * 220, -60 + 34 * k)], 2, smooth=False, col=(0.80, 0.60, 0.40))
    ink(cr, [(0, -100), (0, 100)], 4)
    ink(cr, [(-130, -82), (-130, 92)], 2, smooth=False, col=(0.86, 0.30, 0.20))


register("yc_desk", (-250, -250, 250, 10), _desk)
register("yc_ledger", (-280, -125, 280, 125), _ledger)
register("yc_munim_seat", (-130, -80, 300, 300), lambda cr: M.seat_legs(cr, MN_SKIN, MN_KURTA, DRED, 1.0))


# ------------------------------------------------------------------ city gates


def _tower(cr, x, stone, stone2, flag, dome):
    _shape(cr, [(x - 90, 0), (x - 90, -460), (x + 90, -460), (x + 90, 0)], stone, 5, smooth=False,
           holes=(12, 18, 2.4))
    for y in (-150, -300):
        band(cr, [(x - 86, y), (x + 86, y)], 14, GOLD if stone != DSTONE else IRON, spacing=12, hole_r=2.2)
    cr.new_path()
    cr.move_to(x - 100, -460)
    cr.curve_to(x - 100, -560, x - 30, -600, x, -640)
    cr.curve_to(x + 30, -600, x + 100, -560, x + 100, -460)
    cr.close_path()
    leather(cr, dome, 5)
    punch(cr, [(x - 40, -520), (x, -560), (x + 40, -520)], 6)
    ink(cr, [(x, -640), (x, -720)], 4)
    _shape(cr, [(x, -720), (x + 70, -700), (x, -676)], flag, 3, smooth=False)
    punch(cr, [(x, -380), (x, -240)], 10)


def _gate(cr, kind):
    """A city gate facing the viewer (pivot at the bottom centre): two domed towers with flags, a wall between with
    battlements and a tall arched doorway (half width GATE_DOOR[0], height GATE_DOOR[1]).
    kind S: dark stone, iron doors studded and shut, a buffalo-horn crest, red flags.
    kind E: gold and saffron, the doorway left open (cut through, so the light shows), a sunburst over it.
    kind P: pale sandstone, wooden doors shut, gold bands."""
    stone, stone2, flag, dome = {"S": (DSTONE, DSTONE2, DRED, DSTONE2),
                                 "E": (GOLD, GOLD2, SAFFRON, GOLD2),
                                 "P": (PSTONE, PSTONE2, RED, PSTONE2)}[kind]
    for sx in (-1, 1):
        _tower(cr, sx * 250, stone, stone2, flag, dome)
    wall = [(-160, 0), (-160, -420), (160, -420), (160, 0)]
    _shape(cr, wall, stone2, 5, smooth=False, holes=(12, 20, 2.4))
    for k in range(6):
        x = -154 + 54 * k
        _shape(cr, [(x, -420), (x, -460), (x + 36, -460), (x + 36, -420)], stone2, 4, smooth=False)
    dw, dh = GATE_DOOR
    cr.new_path()
    cr.move_to(-dw, 0)
    cr.line_to(-dw, -dh + dw)
    cr.arc(0, -dh + dw, dw, math.pi, 2 * math.pi)
    cr.line_to(dw, 0)
    cr.close_path()
    if kind == "E":
        cr.set_source_rgb(*INK)
        cr.set_line_width(9)
        cr.stroke_preserve()
        cr.save()
        cr.set_operator(0)
        cr.fill()
        cr.restore()
    else:
        leather(cr, IRON if kind == "S" else WOOD, 6)
        ink(cr, [(0, -dh), (0, 0)], 4)
        for row in range(5):
            for sx in (-1, 1):
                for c in range(2):
                    x = sx * (28 + 44 * c)
                    y = -40 - 60 * row
                    cr.new_path()
                    cr.arc(x, y, 9 if kind == "S" else 6, 0, 2 * math.pi)
                    leather(cr, (0.62, 0.62, 0.68) if kind == "S" else GOLD, 2.5)
        for sx in (-1, 1):
            cr.new_path()
            cr.arc(sx * 30, -170, 18, 0, 2 * math.pi)
            cr.set_source_rgb(*INK)
            cr.set_line_width(5)
            cr.stroke()
    band(cr, [(-dw - 20, -dh + dw), (-dw - 20, 0)], 14, GOLD if kind != "S" else IRON, holes=False, lw=3)
    band(cr, [(dw + 20, -dh + dw), (dw + 20, 0)], 14, GOLD if kind != "S" else IRON, holes=False, lw=3)
    if kind == "S":
        SB._horns(cr, 0, -dh - 30, 0.62, col=(0.70, 0.66, 0.58))
    elif kind == "E":
        for i in range(16):                                                         # a sunburst over the arch
            a = math.pi * (1.0 + i / 15)
            ink(cr, [(60 * math.cos(a), -dh - 10 + 60 * math.sin(a)),
                     (110 * math.cos(a), -dh - 10 + 110 * math.sin(a))], 7, col=SAFFRON)
        cr.new_path()
        cr.arc(0, -dh - 10, 46, 0, 2 * math.pi)
        leather(cr, (1.0, 0.86, 0.36), 4)
        _jewel(cr, 0, -dh - 10, 16, RED)
    else:
        _flower(cr, 0, -dh - 10, 30, GOLD, 8)


for _k in ("S", "E", "P"):
    register("yc_gate_" + _k, (-370, -740, 370, 10), (lambda k: lambda cr: _gate(cr, k))(_k))


# ------------------------------------------------------------------ the celestial chariot


def _ratha(cr):
    """A celestial chariot facing +x (pivot on the ground under the axle; the wheel is jayadratha_cast's jd_wheel at
    (0, -250)): a gold car with a painted side panel, a door opening (filled by yc_ratha_door), four slim pillars, a
    domed canopy with a kalasha finial and pennants, a curved pole forward to the horses."""
    deck = -RATHA_DECK
    band(cr, [(160, deck + 60), (420, deck + 10), (640, deck - 40)], 22, WOOD, spacing=20, hole_r=2.4)  # the pole
    _shape(cr, [(-330, deck), (260, deck), (290, deck + 50), (-300, deck + 50)], WOOD, 5, smooth=False)
    for x in (-300, -120, 80, 240):                                                 # pillars
        band(cr, [(x, deck), (x, deck - 520)], 22, GOLD, spacing=14, hole_r=2.4)
    roof = [(-360, deck - 500), (300, deck - 500), (250, deck - 600), (120, deck - 700), (-30, deck - 760),
            (-180, deck - 700), (-310, deck - 600)]
    _shape(cr, roof, GOLD2, 6, holes=(14, 20, 2.8))
    band(cr, [(-350, deck - 510), (290, deck - 510)], 20, RED, spacing=14, hole_r=2.4)
    for i in range(8):                                                              # hanging bells along the eave
        x = -320 + 84 * i
        ink(cr, [(x, deck - 500), (x, deck - 470)], 3)
        cr.new_path()
        cr.arc(x, deck - 462, 9, 0, 2 * math.pi)
        leather(cr, GOLD, 2.5)
    for k in range(3):
        ink(cr, [(-240 + 40 * k, deck - 560), (-40 + 30 * k, deck - 720 + 30 * k)], 3, col=(0.70, 0.40, 0.10))
    kal = [(-56, deck - 760), (-34, deck - 800), (-50, deck - 840), (-30, deck - 870), (-10, deck - 840),
           (-26, deck - 800), (-4, deck - 760)]
    _shape(cr, kal, GOLD, 4)
    for x, dirn in ((-310, -1), (250, 1)):                                          # pennants
        ink(cr, [(x, deck - 600), (x, deck - 700)], 4)
        _shape(cr, [(x, deck - 700), (x + dirn * 70, deck - 680), (x, deck - 660)], SAFFRON, 3, smooth=False)
    panel = [(-340, deck + 6), (270, deck + 6), (300, deck - 60), (300, deck - 200), (250, deck - 240),
             (-300, deck - 240), (-340, deck - 200)]
    cr.new_path()
    spath(cr, panel)
    dx, dy = RATHA_DOOR
    cr.new_sub_path()
    cr.rectangle(dx, deck - 4, RATHA_DOOR_W, -(RATHA_DOOR_H - 4))
    cr.set_fill_rule(1)
    leather(cr, GOLD, 6)
    cr.set_fill_rule(0)
    dots_in(cr, lambda: poly(cr, [(-300, deck - 20), (dx - 20, deck - 20), (dx - 20, deck - 220),
                                  (-300, deck - 220)]), 22, 3.0, shape="d")
    _flower(cr, -190, deck - 120, 46, RED, 8)
    _jewel(cr, -190, deck - 120, 16, GOLD)
    band(cr, [(-330, deck - 236), (dx - 6, deck - 236)], 16, RED, spacing=12, hole_r=2.2)
    band(cr, [(dx + RATHA_DOOR_W + 6, deck - 236), (296, deck - 236)], 16, RED, spacing=12, hole_r=2.2)
    cr.new_path()                                                                   # the doorway's frame
    cr.rectangle(dx, deck, RATHA_DOOR_W, -RATHA_DOOR_H)
    cr.set_source_rgb(*INK)
    cr.set_line_width(7)
    cr.stroke()


def _ratha_door(cr):
    """The chariot's door leaf (pivot at its hinge = its left edge, middle height): carved gold with a lotus."""
    w, h = RATHA_DOOR_W, RATHA_DOOR_H
    _shape(cr, [(0, -h / 2), (w, -h / 2), (w, h / 2), (0, h / 2)], GOLD2, 5, smooth=False, holes=(12, 18, 2.6))
    _flower(cr, w / 2, -40, 44, RED, 8)
    _jewel(cr, w / 2, -40, 14, GOLD)
    cr.new_path()
    cr.arc(w - 30, 40, 12, 0, 2 * math.pi)
    leather(cr, GOLD, 3)


register("yc_ratha", (-380, -1230, 680, 20), _ratha)
register("yc_ratha_door", (-10, -210, 210, 210), _ratha_door)


# ------------------------------------------------------------------ Parijata tree, mountains, heart


def _parijata(cr):
    """A Parijata tree (pivot at the trunk's foot): a gnarled trunk, a round crown of leaf clusters and white
    flowers with orange hearts."""
    _tube(cr, (0, 0), (-10, -420), 54, 36, (0.50, 0.34, 0.22), 5)
    _tube(cr, (-10, -420), (-170, -640), 30, 16, (0.50, 0.34, 0.22), 4)
    _tube(cr, (-10, -420), (150, -660), 30, 16, (0.50, 0.34, 0.22), 4)
    _tube(cr, (-10, -420), (10, -720), 28, 14, (0.50, 0.34, 0.22), 4)
    for y in (-120, -260):
        ink(cr, [(-20, y), (6, y - 34), (-10, y - 70)], 3)
    blobs = ((-240, -640, 160), (-60, -760, 190), (170, -700, 170), (60, -560, 150), (-170, -520, 130),
             (240, -540, 120), (-30, -900, 140))
    for i, (x, y, r) in enumerate(blobs):
        pts = [(x + r * math.cos(2 * math.pi * k / 14) * (1 + 0.12 * math.sin(k * 2.7 + i)),
                y + 0.86 * r * math.sin(2 * math.pi * k / 14) * (1 + 0.12 * math.cos(k * 1.9 + i)))
               for k in range(14)]
        _shape(cr, pts, LEAFG if i % 2 else LEAFG2, 5, holes=(14, 26, 3.0))
    flowers = ((-280, -680), (-180, -580), (-90, -820), (0, -700), (110, -780), (220, -640), (160, -520),
               (-60, -560), (-260, -500), (40, -930), (-150, -900), (260, -560), (70, -620))
    for x, y in flowers:
        _flower(cr, x, y, 26, FLOWER, 6)
        cr.new_path()
        cr.arc(x, y, 8, 0, 2 * math.pi)
        leather(cr, SAFFRON, 2)


def _flowerp(cr):
    """A single Parijata flower (pivot at its centre), for falling petals."""
    _flower(cr, 0, 0, 30, FLOWER, 6)
    cr.new_path()
    cr.arc(0, 0, 9, 0, 2 * math.pi)
    leather(cr, SAFFRON, 2)


def _hills(cr):
    """A mountain range (pivot at the bottom centre): three rocky peaks with snow caps."""
    for x, h, w, col in ((-420, 520, 360, ROCK2), (380, 600, 400, ROCK2), (0, 820, 460, ROCK)):
        pts = [(x - w, 0), (x - w * 0.5, -h * 0.55), (x - w * 0.2, -h * 0.82), (x, -h), (x + w * 0.25, -h * 0.78),
               (x + w * 0.55, -h * 0.5), (x + w, 0)]
        _shape(cr, pts, col, 5, smooth=False, holes=(14, 26, 3))
        snow = [(x - w * 0.2, -h * 0.82), (x, -h), (x + w * 0.25, -h * 0.78), (x + w * 0.12, -h * 0.74),
                (x + w * 0.02, -h * 0.8), (x - w * 0.1, -h * 0.72)]
        _shape(cr, snow, SNOW, 3, smooth=False)
        ink(cr, [(x, -h), (x - w * 0.1, -h * 0.55), (x - w * 0.3, -h * 0.2)], 3, col=(0.3, 0.24, 0.2))


def _heart(cr):
    """A leather heart (pivot at its centre): red, a gold rim band, a pale highlight."""
    pts = []
    for i in range(48):
        q = 2 * math.pi * i / 48
        hx = 16 * math.sin(q) ** 3
        hy = -(13 * math.cos(q) - 5 * math.cos(2 * q) - 2 * math.cos(3 * q) - math.cos(4 * q))
        pts.append((hx * 12, hy * 12 - 10))
    _shape(cr, pts, HEART, 7, smooth=False, holes=(18, 20, 3.2))
    cr.new_path()
    ell(cr, -70, -80, 34, 20, -0.6)
    cr.set_source_rgb(1.0, 0.70, 0.62)
    cr.fill()
    _flower(cr, 20, 10, 40, GOLD, 8)


register("yc_parijata", (-430, -1060, 430, 20), _parijata)
register("yc_flower", (-36, -36, 36, 36), _flowerp)
register("yc_hills", (-800, -840, 800, 10), _hills)
register("yc_heart", (-210, -230, 210, 210), _heart)


# ------------------------------------------------------------------ a roti


def _roti(cr):
    cr.new_path()
    ell(cr, 0, 0, 70, 66)
    leather(cr, ROTI, 4)
    for x, y in ((-20, -18), (24, 6), (-6, 26), (30, -30), (-36, 12)):
        cr.new_path()
        ell(cr, x, y, 10, 7)
        cr.set_source_rgb(0.62, 0.40, 0.18)
        cr.fill()


register("yc_roti", (-80, -76, 80, 76), _roti)
