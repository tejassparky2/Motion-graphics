"""The leather cast and props for builder A's parts of the long video videos/six_stories.py (the intro, story 1 Kacha,
story 6 Yayati and the outro), in the Togalu Gombeyaata style of the reels (puppet_cast, kaikeyi_cast, lrekha_cast,
mandhata_cast, jayadratha_cast, arjuna_cast, ruru_cast): profile figures with big almond eyes, perforated garments and
jointed limbs. Traditional leather puppets, modelled on no actor and no film.

Cast (one look each, kept the same through the video):
  SHUKRA      Shukracharya, the asuras' guru: pale skin, long white hair, a long white beard and moustache, white matted
              hair piled high and tied with a saffron band, three ash lines and a red dot, a deep-saffron robe over a
              saffron dhoti with a dark-red border, a rudraksha mala; his wooden staff (ravana_cast rv_staff). Faces:
              calm, call (calling out, mouth open), angry (the curse), shock, shut (fallen, eyes closed), smile.
  KACHA       Brihaspati's son, a young Brahmin student: warm skin, no moustache, a top-knot (shikha), a white sandal
              mark, a simple white dhoti with a saffron border, the sacred thread and a rudraksha mala. Faces: calm,
              smile, angry, shock, shut.
  DEVAYANI    Shukra's daughter, proud: a turmeric-yellow sari with a deep-red pallu and border, a red blouse, jasmine
              round her bun and a jasmine string down her back, a small gold forehead band, a nose ring. The SAME puppet
              in story 1 and story 6. Faces: open, smile, proud, weep (eyes shut, tears), angry, shut.
  SHARMISHTHA the asura princess: darker skin, a violet sari with a deep-violet pallu, an emerald blouse, a small gold
              crown with points, gold flowers. Faces: open, angry, smile.
  YAYATI      the king: wheat skin, a black moustache, long hair, a gold kirita with a blue flare, a teal dhoti with a
              gold border, a red sash. The same king OLD: white hair and brows, a white beard and moustache, lines at
              the eye, the same crown and clothes (the scenes bend him forward and give him a stick).
  PURU        the youngest son: light skin, no moustache, long hair, a gold prince's band with a small crest, a saffron
              dhoti with a red border, a blue sash. OLD (while his father is young): white hair and beard. KING: a
              gold kirita. The other sons are shown as silhouettes of this puppet.
  ASURA       a Danava: dark violet skin, wild hair, two curved horns, small tusks (always shown as silhouettes).
  BRIHASPATI  the gods' guru: pale-gold skin, a small ring of gold rays, white beard and matted hair with a gold band,
              a gold robe and dhoti (shown small).
Props: a wolf (profile, punched eye), the well (back half: the dark opening, posts, crossbar, pulley, rope, bucket;
front half: the stone wall and rim, drawn over a figure falling in), a brass wine goblet (upright / overturned), a
small brass ghee pot (lota), a red pin, a leather medallion (family-tree nodes, number badges), a carved door frame and
its door leaf, two sea-wave strips. The palm-leaf books, the big leaf, the speech cloud, plaque, garland, crown,
altar, flames, ground, trees and the balance come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import jayadratha_cast as J  # noqa: F401  (registers Arjuna for the family tree)
import kaikeyi_cast as K  # noqa: F401  (registers the balance, plaque, leaf, garland, crown)
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf books, big leaf, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BLUE, BROWN, DRED, GOLD, GREEN, INK, PALE, PARCH, RED, SAFFRON, band, cut, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, spath)

ASH = (0.90, 0.89, 0.86)              # white hair and beards
ASH2 = (0.60, 0.58, 0.56)
SH_SKIN = (0.97, 0.82, 0.64)          # Shukra
SH_ROBE = (0.96, 0.44, 0.10)          # deep saffron
SH_DHOTI = (1.0, 0.62, 0.20)
KA_SKIN = (0.98, 0.74, 0.50)          # Kacha
KA_WHITE = (1.0, 0.96, 0.88)
DV_SKIN = (0.99, 0.79, 0.60)          # Devayani
DV_SARI = (1.0, 0.80, 0.26)           # turmeric yellow
DV_RED = (0.84, 0.17, 0.12)
SM_SKIN = (0.74, 0.52, 0.48)          # Sharmishtha
SM_SARI = (0.50, 0.24, 0.64)          # violet
SM_PALLU = (0.32, 0.13, 0.44)
SM_CHOLI = (0.10, 0.50, 0.38)         # emerald
YY_SKIN = (0.98, 0.73, 0.47)          # Yayati
YY_DHOTI = (0.14, 0.54, 0.50)         # teal
PU_SKIN = (1.0, 0.79, 0.56)           # Puru
PU_SASH = (0.30, 0.52, 0.90)
AS_SKIN = (0.42, 0.30, 0.46)          # an asura
BR_SKIN = (1.0, 0.88, 0.62)           # Brihaspati
WOLF = (0.46, 0.42, 0.40)
WOLF2 = (0.62, 0.58, 0.54)
STONE = (0.80, 0.70, 0.56)
STONE2 = (0.66, 0.56, 0.44)
WOOD = (0.58, 0.34, 0.16)
BRASS = (0.98, 0.76, 0.30)
WINE = (0.55, 0.06, 0.12)
SEA = (0.24, 0.52, 0.86)
SEA2 = (0.12, 0.34, 0.68)

WELL_RX, WELL_RY, WELL_H = 280.0, 56.0, 300.0     # the well: rim half-width, rim ellipse half-height, wall height


# ------------------------------------------------------------------ shared face bits


def _old_hair(cr):
    """Long white hair falling down the back (behind the face)."""
    hp = [(-30, -176), (-64, -146), (-92, -70), (-98, 40), (-74, 110), (-48, 64), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-76 - 6 * k, -20), (-68 - 4 * k, 80)], 2.5, col=ASH2)


def _white_beard(cr, long_=1.0):
    bp = [(64, -54), (70, -26), (66, 16), (54, 60 * long_), (34, 112 * long_), (16, 150 * long_), (4, 108 * long_),
          (-8, 56 * long_), (-12, 4), (-4, -40), (18, -58), (42, -60)]
    _shape(cr, bp, ASH, 4)
    for k in range(4):
        ink(cr, [(52 - 12 * k, -44), (46 - 13 * k, 30 * long_), (36 - 10 * k, 96 * long_)], 2.5, col=ASH2)


def _white_moustache(cr, dy=0.0):
    m = [(74, -76 + dy), (52, -86 + dy), (26, -90 + dy), (6, -76 + dy), (28, -80 + dy), (52, -76 + dy),
         (76, -71 + dy)]
    _shape(cr, m, ASH, 3)


def _age_lines(cr):
    ink(cr, [(52, -104), (60, -96)], 2.5)
    ink(cr, [(8, -92), (20, -80)], 2.5)
    ink(cr, [(10, -160), (40, -164)], 2.2)


def _open_mouth(cr, x=66, y=-64, rx=9, ry=13):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    leather(cr, (0.36, 0.05, 0.06), 3)


def _jata(cr, col, band_col=None, n=5, rud=True):
    """Matted hair piled up on the crown of the head, optionally tied with a coloured band."""
    for k in range(n):
        cr.new_path()
        ell(cr, -4 - 3 * k, -194 - 26 * k, 52 - 6 * k, 22)
        leather(cr, col, 4)
        ink(cr, [(-40 + 6 * k, -194 - 26 * k), (-4, -184 - 26 * k), (32 - 6 * k, -196 - 26 * k)], 2.5, col=ASH2)
    if band_col is not None:
        band(cr, [(-52, -232), (-6, -242), (44, -234)], 16, band_col, spacing=11, hole_r=2.4)
    if rud:
        for i in range(7):
            cr.new_path()
            cr.arc(-44 + 14 * i, -178, 6, 0, 2 * math.pi)
            leather(cr, BROWN, 2)


def _ash_lines(cr, dot=True):
    for k in range(3):
        ink(cr, [(4, -172 + 9 * k), (46, -174 + 9 * k)], 3, col=(1.0, 0.97, 0.9))
    if dot:
        cr.new_path()
        cr.arc(48, -160, 5, 0, 2 * math.pi)
        cr.set_source_rgb(*RED)
        cr.fill()


def _face(cr, skin, mood, hair=False, moustache=False):
    """ruru_cast.rface (arjuna_cast.face + weep / sleep / shock / teach) with a 'call' (mouth open) and 'shut'."""
    base = {"call": "calm", "shut": "sleep"}.get(mood, mood)
    RU.rface(cr, dict(skin=skin, hair=hair, moustache=moustache, tilak=False, earring=False), base)


# ------------------------------------------------------------------ Shukracharya


def shukra_head(cr, mood="calm"):
    _old_hair(cr)
    _face(cr, SH_SKIN, mood)
    if mood not in ("shut",):
        ink(cr, [(12, -142), (34, -152), (60, -142)] if mood != "angry" else [(6, -154), (34, -144), (62, -128)], 8,
            col=ASH)                                                              # white brows
    _age_lines(cr)
    _white_beard(cr, 1.15)
    _white_moustache(cr, -4 if mood in ("call", "angry") else 0)
    if mood in ("call", "angry", "shock"):
        _open_mouth(cr, 70, -62, 8, 11 if mood != "shock" else 13)
    _jata(cr, ASH, SAFFRON)
    _ash_lines(cr)


SHUKRA = man("sx_shukra", skin=SH_SKIN, bulk=1.0, dhoti=SH_DHOTI, border=DRED, pleat=(1.0, 0.74, 0.36), sash=DRED,
             neck=BROWN, crown="tiara", halo=False, robe=SH_ROBE, beads=True, hair=False, earring=False, tilak=False,
             hands=("open", "open"))
SHUKRA.points["belly"] = ("sx_shukra_body", (26, -118))
SHUKRA.points["mouth"] = ("sx_shukra_head", (70, -62))
for _m in ("calm", "call", "angry", "shock", "shut", "smile"):
    register("sx_shukra_head" + ("" if _m == "calm" else "_" + _m), (-190, -370, 120, 200),
             (lambda m: lambda cr: shukra_head(cr, m))(_m))


# ------------------------------------------------------------------ Kacha


def kacha_head(cr, mood="calm"):
    _face(cr, KA_SKIN, mood)
    if mood == "call":
        _open_mouth(cr, 68, -66, 7, 9)
    _shape(cr, [(-48, -146), (-44, -190), (0, -208), (40, -192), (48, -160), (0, -174)], HAIR, 4)   # the hair cap
    holes_line(cr, [(-40, -150), (-34, -186), (0, -198)], 14, 2.2)
    cr.new_path()
    cr.arc(-36, -210, 25, 0, 2 * math.pi)                                         # the shikha knot
    leather(cr, HAIR, 4)
    holes_line(cr, [(-52, -210), (-36, -228), (-20, -210)], 9, 2.2)
    for x in (40, 50):                                                            # the white sandal mark
        ink(cr, [(x, -146), (x + 2, -176)], 3.5, col=(1.0, 0.97, 0.9))
    cr.new_path()
    cr.arc(46, -150, 4.5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()
    cr.arc(-14, -80, 7, 0, 2 * math.pi)
    leather(cr, BROWN, 2)


KACHA = man("sx_kacha", skin=KA_SKIN, bulk=0.92, dhoti=KA_WHITE, border=SAFFRON, pleat=(1.0, 0.86, 0.62),
            sash=SAFFRON, neck=BROWN, crown="tiara", halo=False, thread=True, beads=True, hair=False, earring=False,
            tilak=False, hands=("open", "open"))
for _m in ("calm", "smile", "angry", "shock", "shut", "call"):
    register("sx_kacha_head" + ("" if _m == "calm" else "_" + _m), (-130, -260, 120, 60),
             (lambda m: lambda cr: kacha_head(cr, m))(_m))


# ------------------------------------------------------------------ Devayani


def _woman_face(cr, skin):
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, skin, 6)


def _woman_eyes(cr, skin, mood):
    if mood in ("shut", "weep"):
        cr.new_path()
        ell(cr, 30, -112, 19, 13)
        cr.set_source_rgb(*skin)
        cr.fill()
        ink(cr, [(14, -112), (30, -104), (46, -112)], 4)
        for x in (22, 30, 38):
            ink(cr, [(x, -107), (x - 2, -100)], 2.2)
        ink(cr, [(14, -128), (30, -132), (46, -126)] if mood == "shut" else [(14, -124), (30, -132), (48, -140)], 3.5)
        if mood == "weep":
            for k, (x0, y0) in enumerate(((32, -100), (40, -98))):
                ink(cr, [(x0, y0), (x0 + 4, y0 + 22), (x0 + 2, y0 + 42)], 5 - k, col=M.TEAR)
    elif mood == "smile":
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5)
    elif mood == "proud":                                                         # chin up, lids half down
        from puppet_core import almond_eye
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        _shape(cr, [(13, -114), (30, -124), (47, -114), (30, -118)], skin, 2.5)
        ink(cr, [(13, -114), (30, -121), (47, -114)], 4)
        ink(cr, [(12, -134), (30, -142), (48, -136)], 3.5)
    elif mood == "angry":
        from puppet_core import almond_eye
        almond_eye(cr, 30, -112, 34, 12, col=PALE)
        ink(cr, [(10, -140), (30, -132), (52, -122)], 6)
    else:
        from puppet_core import almond_eye
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
    if mood == "smile":
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    elif mood == "proud":
        ink(cr, [(56, -72), (62, -70)], 3, col=RED)
    elif mood == "angry":
        ink(cr, [(64, -70), (55, -72)], 3.5, col=RED)
    elif mood == "weep":
        ink(cr, [(62, -70), (56, -74)], 3, col=RED)
    else:
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)


def deva_head(cr, mood="open"):
    """Devayani: jasmine round the bun and a jasmine string down her back, a small gold forehead band with a red
    drop, a bindi, gold studs, a nose ring."""
    veni = [(-70, -104), (-80, -50), (-80, 10), (-74, 70), (-66, 120)]           # the jasmine string down her back
    band(cr, veni, 22, PALE, spacing=12, hole_r=3.0)
    for x, y in veni[1:]:
        _flower(cr, x, y, 12, PALE, 5)
    _woman_face(cr, DV_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 22 * math.cos(a), -128 + 22 * math.sin(a))], 3.2)
    for i in range(13):                                                           # jasmine round the bun
        a = math.pi * (0.2 + 1.6 * i / 12)
        _flower(cr, -62 + 42 * math.cos(a), -128 + 42 * math.sin(a), 9, PALE, 5)
    _flower(cr, -62, -128, 13, DV_RED, 6)
    band(cr, [(-30, -176), (6, -190), (40, -178)], 10, GOLD, spacing=10, hole_r=2.0)   # the forehead band
    _jewel(cr, 42, -168, 7, DV_RED)
    cr.new_path()
    cr.arc(47, -146, 5, 0, 2 * math.pi)                                           # bindi
    cr.set_source_rgb(*RED)
    cr.fill()
    _woman_eyes(cr, DV_SKIN, mood)
    cr.new_path()
    cr.arc(66, -88, 8, 0, 2 * math.pi)                                            # nose ring
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3.2)
    cr.stroke()
    _jewel(cr, -10, -70, 9, GOLD)


def _deva_extra(cr):
    for i in range(9):
        u = i / 8
        cr.new_path()
        cr.arc(-12 + 58 * u, -276 + 76 * u + 26 * u * u, 6, 0, 2 * math.pi)
        leather(cr, GOLD, 2.2)
    _jewel(cr, 50, -176, 9, GREEN)


DEVA = woman("sx_deva", skin=DV_SKIN, skirt=DV_SARI, choli=DV_RED, border=DV_RED, pallu_col=DV_RED, gem=GREEN,
             flower=PALE, ornaments_extra=_deva_extra, hands=("open", "open"))
for _m in ("open", "smile", "proud", "weep", "angry", "shut"):
    register("sx_deva_head" + ("" if _m == "open" else "_" + _m), (-140, -250, 100, 190),
             (lambda m: lambda cr: deva_head(cr, m))(_m))


# ------------------------------------------------------------------ Sharmishtha


def sharm_head(cr, mood="open"):
    """Sharmishtha: dark hair in a bun with gold flowers, a small gold crown with points, a red bindi, gold hoops."""
    _woman_face(cr, SM_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 38, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 24 * math.cos(a), -128 + 24 * math.sin(a))], 3.4)
    for x, y in ((-86, -150), (-40, -158), (-92, -106)):
        _flower(cr, x, y, 13, GOLD, 6)
    tp = [(-36, -170), (-28, -218), (-14, -196), (0, -236), (14, -198), (30, -228), (44, -172)]
    _shape(cr, tp, GOLD, 4, smooth=False, holes=(7, 11, 2.2))
    _jewel(cr, 2, -194, 8, RED)
    _jewel(cr, -24, -192, 5, SM_CHOLI)
    _jewel(cr, 28, -192, 5, SM_CHOLI)
    cr.new_path()
    cr.arc(46, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _woman_eyes(cr, SM_SKIN, mood)
    cr.new_path()
    cr.arc(-10, -58, 14, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(4)
    cr.stroke()


def _sharm_extra(cr):
    for i in range(7):
        u = i / 6
        _jewel(cr, -10 + 56 * u, -272 + 70 * u + 22 * u * u, 7, GOLD if i % 2 else RED)


SHARM = woman("sx_sharm", skin=SM_SKIN, skirt=SM_SARI, choli=SM_CHOLI, border=GOLD, pallu_col=SM_PALLU, gem=RED,
              flower=GOLD, ornaments_extra=_sharm_extra, hands=("open", "open"))
for _m in ("open", "angry", "smile"):
    register("sx_sharm_head" + ("" if _m == "open" else "_" + _m), (-140, -260, 100, 40),
             (lambda m: lambda cr: sharm_head(cr, m))(_m))


# ------------------------------------------------------------------ Yayati


def yay_head(cr, mood="calm", old=False):
    if old:
        _old_hair(cr)
        _face(cr, YY_SKIN, mood)
        ink(cr, [(12, -142), (34, -152), (60, -142)], 8, col=ASH)
        _age_lines(cr)
        _white_beard(cr, 0.8)
        _white_moustache(cr)
        if mood == "shock":
            _open_mouth(cr, 70, -62, 8, 12)
    else:
        _face(cr, YY_SKIN, mood, hair=True, moustache=True)
        if mood == "shock":
            _open_mouth(cr, 68, -64, 7, 10)
    R.kirita(cr, GOLD, None, tall=1.0, flare=BLUE)
    _jewel(cr, 2, -282, 9, (0.16, 0.66, 0.40))
    _jewel(cr, -12, -72, 13, GOLD)


YAY = man("sx_yay", skin=YY_SKIN, bulk=1.06, dhoti=YY_DHOTI, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
          crown="tiara", halo=False, hair=False, thread=True, hands=("open", "open"))
for _m in ("calm", "smile", "shock", "shame", "proud"):
    register("sx_yay_head" + ("" if _m == "calm" else "_" + _m), (-190, -460, 120, 120),
             (lambda m: lambda cr: yay_head(cr, m))(_m))
for _m in ("calm", "shock", "shame", "smile"):
    register("sx_yay_old_head" + ("" if _m == "calm" else "_" + _m), (-190, -460, 120, 170),
             (lambda m: lambda cr: yay_head(cr, m, True))(_m))


# ------------------------------------------------------------------ Puru


def _diadem(cr):
    band(cr, [(-46, -168), (0, -184), (48, -170)], 14, GOLD, spacing=10, hole_r=2.2)
    _shape(cr, [(-6, -180), (2, -222), (12, -180)], GOLD, 3.5, smooth=False)
    _jewel(cr, 3, -186, 7, RED)


def puru_head(cr, mood="calm", old=False, king=False):
    if old:
        _old_hair(cr)
        _face(cr, PU_SKIN, mood)
        ink(cr, [(12, -142), (34, -152), (60, -142)], 8, col=ASH)
        _age_lines(cr)
        _white_beard(cr, 0.75)
        _white_moustache(cr)
    else:
        _face(cr, PU_SKIN, mood, hair=True)
    if king:
        R.kirita(cr, GOLD, None, tall=0.9, flare=RED)
    else:
        _diadem(cr)
    _jewel(cr, -12, -72, 11, GOLD)


PURU = man("sx_puru", skin=PU_SKIN, bulk=0.94, dhoti=SAFFRON, border=RED, pleat=RED, sash=PU_SASH, neck=GOLD,
           crown="tiara", halo=False, hair=False, thread=True, hands=("open", "open"))
for _m in ("calm", "smile", "shame"):
    register("sx_puru_head" + ("" if _m == "calm" else "_" + _m), (-130, -260, 120, 100),
             (lambda m: lambda cr: puru_head(cr, m))(_m))
    register("sx_puru_old_head" + ("" if _m == "calm" else "_" + _m), (-140, -260, 120, 170),
             (lambda m: lambda cr: puru_head(cr, m, True))(_m))
register("sx_puru_king_head", (-130, -440, 120, 100), lambda cr: puru_head(cr, "smile", king=True))


# ------------------------------------------------------------------ an asura (silhouettes)


def asura_head(cr):
    """A Danava: wild hair, two horns curving up and back, small tusks, a heavy brow."""
    mass = [(-30 + 112 * math.cos(math.radians(a)) * (1 + 0.16 * math.sin(a * 0.31)),
             -120 - 112 * math.sin(math.radians(a)) * (1 + 0.16 * math.cos(a * 0.27))) for a in range(60, 320, 20)]
    _shape(cr, mass, HAIR, 5)
    _face(cr, AS_SKIN, "angry", moustache=True)
    for x0, y0 in ((-60, -184), (16, -176)):                                     # the far horn, then the near one
        horn = [(x0 - 14, y0 + 6), (x0 - 30, y0 - 50), (x0 - 20, y0 - 110), (x0 + 6, y0 - 150), (x0 + 30, y0 - 166),
                (x0 + 14, y0 - 130), (x0 + 4, y0 - 90), (x0 + 10, y0 - 40), (x0 + 16, y0 + 2)]
        _shape(cr, horn, PALE, 4)
        for k in range(3):
            ink(cr, [(x0 - 22 + 4 * k, y0 - 30 - 30 * k), (x0 - 2 + 4 * k, y0 - 36 - 30 * k)], 2.5)
    for tx in (50, 62):
        _shape(cr, [(tx - 8, -58), (tx + 2, -60), (tx + 14, -90), (tx + 10, -98), (tx - 2, -76)], PALE, 3,
               smooth=False)


ASURA = man("sx_asura", skin=AS_SKIN, bulk=1.2, dhoti=DRED, border=GOLD, pleat=GOLD, sash=DRED, neck=GOLD,
            crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("fist", "fist"))
register("sx_asura_head", (-190, -380, 120, 60), asura_head)


# ------------------------------------------------------------------ Brihaspati


def brih_head(cr):
    M._ray_halo(cr, -20, -200, 120, 176, 14, (GOLD, PALE))
    _old_hair(cr)
    _face(cr, BR_SKIN, "smile")
    ink(cr, [(12, -142), (34, -152), (60, -142)], 8, col=ASH)
    _white_beard(cr, 0.95)
    _white_moustache(cr)
    _jata(cr, ASH, GOLD, n=4)
    _ash_lines(cr)


BRIH = man("sx_brih", skin=BR_SKIN, bulk=0.9, dhoti=GOLD, border=SAFFRON, pleat=SAFFRON, sash=(1.0, 0.95, 0.72),
           neck=GOLD, crown="tiara", halo=False, robe=(1.0, 0.80, 0.24), beads=True, hair=False, earring=False,
           tilak=False, hands=("open", "open"))
register("sx_brih_head", (-200, -390, 120, 170), brih_head)


# ------------------------------------------------------------------ the wolf


def _wolf(cr, pose=0):
    """A wolf in profile facing +x (pivot on the ground under its middle): a lean body, a bushy tail, pricked ears,
    a long muzzle, a punched eye. pose 1 = head low (sniffing)."""
    hy = 0 if pose == 0 else 60
    for lx, ph in ((-170, 0.1), (150, -0.1)):                                      # the far legs
        _shape(cr, [(lx - 16, -170), (lx + 18, -170), (lx + 14 + 30 * ph, -10), (lx + 30 + 30 * ph, 0),
                    (lx - 6 + 30 * ph, 0), (lx - 14 + 30 * ph, -12)], WOLF2, 3.5, smooth=False)
    tail = [(-230, -250), (-320, -250), (-400, -200), (-430, -140), (-400, -150), (-350, -190), (-290, -212),
            (-236, -210)]
    _shape(cr, tail, WOLF, 4)
    body = [(-250, -250), (-200, -280), (-60, -276), (100, -290), (200, -300 + hy * 0.4), (250, -330 + hy),
            (300, -350 + hy), (330, -330 + hy), (390, -300 + hy), (400, -286 + hy), (370, -276 + hy),
            (300, -262 + hy), (250, -220 + hy * 0.6), (220, -170), (160, -150), (0, -160), (-150, -150), (-240, -170),
            (-270, -210)]
    _shape(cr, body, WOLF, 5)
    dots_in(cr, lambda: spath(cr, body), 26, 3.2, shape="d")
    for (x0, y0), (x1, y1) in (((262, -336 + hy), (282, -392 + hy)), ((290, -344 + hy), (316, -398 + hy))):
        _shape(cr, [(x0 - 12, y0), (x1, y1), (x0 + 16, y0 + 4)], WOLF, 3.5, smooth=False)   # ears
    punch(cr, [(328, -318 + hy)], 7)                                               # the eye
    ink(cr, [(320, -324 + hy), (342, -320 + hy)], 2.5)
    ink(cr, [(370, -280 + hy), (396, -286 + hy)], 3)                              # the mouth line
    for lx, ph in ((-200, -0.1), (190, 0.15)):                                     # the near legs
        _shape(cr, [(lx - 20, -180), (lx + 22, -176), (lx + 16 + 30 * ph, -12), (lx + 36 + 30 * ph, 0),
                    (lx - 8 + 30 * ph, 0), (lx - 16 + 30 * ph, -14)], WOLF, 4, smooth=False)
    holes_line(cr, [(-200, -240), (0, -250), (180, -270)], 18, 3)


register("sx_wolf", (-450, -420, 420, 10), lambda cr: _wolf(cr, 0))
register("sx_wolf_low", (-450, -420, 420, 10), lambda cr: _wolf(cr, 1))


# ------------------------------------------------------------------ the well


def _rim_pts(cy, rx, ry, a0, a1, n=48):
    return [(rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _well_back(cr):
    """Behind a figure: the posts, crossbar, pulley, rope and bucket, the far rim and the dark opening (pivot: the
    ground at the well's front centre)."""
    top = -WELL_H
    for sx in (-1, 1):                                                            # posts
        x = sx * (WELL_RX - 30)
        _shape(cr, [(x - 16, top + 10), (x + 16, top + 10), (x + 12, top - 470), (x - 12, top - 470)], WOOD, 4,
               smooth=False)
        holes_line(cr, [(x, top - 20), (x, top - 450)], 30, 3, smooth=False)
    band(cr, [(-WELL_RX, top - 460), (WELL_RX, top - 460)], 26, WOOD, spacing=20, hole_r=3)       # crossbar
    cr.new_path()
    cr.arc(0, top - 430, 38, 0, 2 * math.pi)                                      # pulley
    leather(cr, (0.80, 0.56, 0.26), 4)
    punch(cr, [(0, top - 430)], 9)
    ink(cr, [(38, top - 430), (38, top - 230)], 3.5, smooth=False, col=(0.50, 0.36, 0.20))       # rope
    _shape(cr, [(10, top - 236), (66, top - 236), (60, top - 180), (16, top - 180)], (0.70, 0.46, 0.22), 4,
           smooth=False)                                                           # bucket
    ink(cr, [(10, top - 236), (38, top - 262), (66, top - 236)], 3)
    far = _rim_pts(top, WELL_RX, WELL_RY, math.pi, 2 * math.pi)                  # the far rim (upper arc)
    outer = [(x, y - 26) for x, y in far]
    _shape(cr, outer + list(reversed(far)), STONE, 4, smooth=False)
    cr.new_path()                                                                 # the dark opening
    ell(cr, 0, top, WELL_RX - 18, WELL_RY - 8)
    cr.set_source_rgb(0.10, 0.06, 0.05)
    cr.fill()


def _well_front(cr):
    """In front of a figure: the near rim and the stone wall down to the ground."""
    top = -WELL_H
    near = _rim_pts(top, WELL_RX, WELL_RY, 0, math.pi)                           # the near rim (lower arc), R to L
    base = _rim_pts(0, WELL_RX, WELL_RY * 0.9, math.pi, 0)                        # the ground line, L to R
    wall = [(WELL_RX, top)] + near[1:] + [(-WELL_RX, 0)] + base[1:]
    _shape(cr, wall, STONE2, 5, smooth=False)
    for row in range(1, 6):                                                       # courses of stone
        y = top + WELL_RY + row * 50
        pts = [(x, y + WELL_RY * 0.0 + 0.9 * WELL_RY * math.sqrt(max(0, 1 - (x / WELL_RX) ** 2)) - WELL_RY)
               for x in range(-int(WELL_RX) + 4, int(WELL_RX) - 3, 14)]
        ink(cr, pts, 3, smooth=False, col=(0.42, 0.32, 0.22))
        off = 35 if row % 2 else 0
        for x in range(-int(WELL_RX) + 40 + off, int(WELL_RX) - 30, 80):
            yy = y + 0.9 * WELL_RY * math.sqrt(max(0, 1 - (x / WELL_RX) ** 2)) - WELL_RY
            ink(cr, [(x, yy), (x + 2, yy - 46)], 3, smooth=False, col=(0.42, 0.32, 0.22))
    rim = [(x, y) for x, y in near] + [(x, y + 30) for x, y in reversed(near)]
    _shape(cr, rim, STONE, 4, smooth=False, holes=(9, 18, 2.6))


register("sx_well_back", (-WELL_RX - 10, -WELL_H - 520, WELL_RX + 10, -WELL_H + WELL_RY + 4), _well_back)
register("sx_well_front", (-WELL_RX - 10, -WELL_H - 10, WELL_RX + 10, WELL_RY + 10), _well_front)


def well_mouth_front(x, ground, s):
    """The near rim's lower arc on screen (for clipping a figure that drops in), left to right."""
    return [(x + s * px, ground + s * py) for px, py in _rim_pts(-WELL_H, WELL_RX, WELL_RY, math.pi, 0)]


# ------------------------------------------------------------------ small props


def _cup(cr, wine=True):
    """A brass goblet (pivot at the foot's centre on the ground): a wide bowl with a red band, a knotted stem."""
    _shape(cr, [(-70, -18), (70, -18), (52, 0), (-52, 0)], BRASS, 4, smooth=False)
    _shape(cr, [(-16, -120), (16, -120), (12, -70), (22, -56), (12, -40), (14, -18), (-14, -18), (-12, -40),
                (-22, -56), (-12, -70)], BRASS, 4, smooth=False)
    bowl = [(-86, -250), (86, -250), (78, -190), (52, -140), (20, -120), (-20, -120), (-52, -140), (-78, -190)]
    _shape(cr, bowl, BRASS, 5)
    band(cr, [(-80, -214), (0, -210), (80, -214)], 14, RED, spacing=11, hole_r=2.2)
    dots_in(cr, lambda: poly(cr, [(-70, -196), (70, -196), (40, -140), (-40, -140)]), 18, 2.6, shape="d")
    if wine:
        cr.new_path()
        ell(cr, 0, -250, 84, 16)
        leather(cr, WINE, 3)
    else:
        cr.new_path()
        ell(cr, 0, -250, 84, 16)
        leather(cr, (0.66, 0.46, 0.18), 3)


register("sx_cup", (-95, -275, 95, 6), lambda cr: _cup(cr, True))
register("sx_cup_empty", (-95, -275, 95, 6), lambda cr: _cup(cr, False))


def _lota(cr):
    """A small brass pot of ghee with a spout (pivot at its centre)."""
    cr.new_path()
    ell(cr, 0, 0, 90, 80)
    leather(cr, BRASS, 5)
    _shape(cr, [(-46, -64), (46, -64), (52, -100), (-52, -100)], BRASS, 4, smooth=False)
    band(cr, [(-80, -20), (0, -12), (80, -20)], 12, RED, spacing=10, hole_r=2.0)
    _shape(cr, [(70, -30), (150, -86), (162, -78), (86, -6)], BRASS, 4, smooth=False)
    dots_in(cr, lambda: ell(cr, 0, 30, 60, 30), 16, 2.6)


register("sx_lota", (-100, -110, 170, 90), _lota)


def _pin(cr):
    """A red push pin, seen from the side, its needle tip at (0, 0)."""
    ink(cr, [(0, 0), (-34, -96)], 7, smooth=False, col=(0.75, 0.75, 0.78))
    ink(cr, [(0, 0), (-34, -96)], 3, smooth=False, col=(0.95, 0.95, 0.98))
    _shape(cr, [(-26, -96), (-62, -84), (-58, -110), (-30, -122)], (0.80, 0.08, 0.06), 4, smooth=False)
    cr.new_path()
    ell(cr, -60, -116, 38, 34, -0.35)
    leather(cr, (0.90, 0.12, 0.08), 4)
    punch(cr, [(-70, -130)], 7)


register("sx_pin", (-110, -160, 10, 10), _pin)


def _medal(cr, col):
    """A round leather medallion (centre pivot) with a perforated border."""
    pts = [(100 * math.cos(2 * math.pi * i / 48), 100 * math.sin(2 * math.pi * i / 48)) for i in range(48)]
    _shape(cr, pts, col, 6, smooth=False, holes=(12, 15, 3.0))
    cr.new_path()
    cr.arc(0, 0, 74, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()


register("sx_medal", (-106, -106, 106, 106), lambda cr: _medal(cr, PARCH))
register("sx_medal_red", (-106, -106, 106, 106), lambda cr: _medal(cr, (0.86, 0.20, 0.12)))
register("sx_medal_gold", (-106, -106, 106, 106), lambda cr: _medal(cr, GOLD))


def _door_frame(cr):
    """A carved doorway (pivot at the bottom centre): the opening is cut through, the light shows inside."""
    outer = [(-260, 0), (-260, -640), (-200, -760), (0, -830), (200, -760), (260, -640), (260, 0)]
    _shape(cr, outer, (0.62, 0.38, 0.18), 6, smooth=False, holes=(14, 18, 3))
    dots_in(cr, lambda: poly(cr, outer), 30, 3.2, shape="d")
    cut(cr, lambda: poly(cr, [(-190, 0), (-190, -610), (-140, -690), (0, -740), (140, -690), (190, -610),
                              (190, 0)]))
    ink(cr, [(-190, 0), (-190, -610), (-140, -690), (0, -740), (140, -690), (190, -610), (190, 0)], 6, smooth=False)
    _jewel(cr, 0, -786, 14, RED)


def _door_leaf(cr):
    """One door leaf (pivot at the hinge, bottom): planks, iron studs, a ring handle."""
    pts = [(0, 0), (0, -610), (190, -610), (190, 0)]
    _shape(cr, pts, WOOD, 5, smooth=False)
    for x in (48, 96, 144):
        ink(cr, [(x, -600), (x, -10)], 3, smooth=False)
    for y in (-520, -320, -120):
        band(cr, [(6, y), (184, y)], 16, (0.30, 0.22, 0.16), holes=False)
        for x in (20, 70, 120, 170):
            cr.new_path()
            cr.arc(x, y, 6, 0, 2 * math.pi)
            leather(cr, GOLD, 2)
    cr.new_path()
    cr.arc(160, -300, 18, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(6)
    cr.stroke()


register("sx_door_frame", (-270, -840, 270, 6), _door_frame)
register("sx_door_leaf", (-6, -620, 196, 6), _door_leaf)


def _wave(cr, col, ph):
    """A long strip of sea (pivot at the middle of its crest line): rolling crests with curls, punched foam."""
    crest = []
    for i in range(0, 121):
        x = -1200 + 20 * i
        u = (x / 240.0 + ph) % 1.0
        y = -26 * math.sin(2 * math.pi * u) - 14 * math.sin(4 * math.pi * u + 0.6)
        crest.append((x, y))
    pts = crest + [(1200, 420), (-1200, 420)]
    _shape(cr, pts, col, 5, smooth=False)
    for k in range(10):
        cx = -1200 + 240 * k + 240 * ((0.75 - ph) % 1.0)
        ink(cr, [(cx - 50, -6), (cx - 10, -40), (cx + 26, -30), (cx + 14, -8)], 4, col=(0.90, 0.96, 1.0))
    holes_line(cr, [(-1180, 60), (1180, 60)], 22, 3.2)
    holes_line(cr, [(-1180, 150), (1180, 150)], 34, 2.6)


register("sx_wave", (-1210, -60, 1210, 430), lambda cr: _wave(cr, SEA, 0.0))
register("sx_wave2", (-1210, -60, 1210, 430), lambda cr: _wave(cr, SEA2, 0.5))


def _horn(cr):
    """A small horn (for the boy of story 4 in the intro panel): pivot at its base."""
    _shape(cr, [(-12, 0), (-8, -40), (6, -72), (14, -68), (8, -38), (12, 0)], PALE, 3)


register("sx_horn", (-20, -80, 20, 6), _horn)

# the puppets the family tree borrows: arjuna_cast YUDH, jayadratha_cast ARJUNA, puppet_cast BHIMA / KRISHNA / KING
YUDH = A.YUDH
