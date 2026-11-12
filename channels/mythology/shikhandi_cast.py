"""The leather cast and props for the Shikhandi reel (videos/shikhandi.py), in the Togalu Gombeyaata style of the
Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha, Arjuna, Ruru, Dharmavyadha and Shani reels: profile figures
with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no
film. Every sprite name starts with "sk_".

Cast (one look each, kept the same through the video; every god, king and woman with dignity):
  AMBA         the eldest Kashi princess: fair skin, a rose-pink sari with a gold border and a deep-magenta pallu, a
               gold choli, a small gold princess tiara with pearl drops, jasmine in her bun. Faces: open (proud), smile,
               sad (eyes lowered), angry, shock.
  AMBA (TAPAS) the same woman after years of penance: the same face, a little darker from the sun, a high bun of
               matted hair (jata) wound with rudraksha beads and long matted locks down her back, three ash lines and a
               red dot on her forehead, an ochre bark-cloth sari, a rudraksha mala. Faces: fierce, shut (meditating),
               open.
  HER SISTERS  Ambika and Ambalika (only small, on the chariot): the same princess look in green and in saffron.
  BHISHMA      the grand-sire, old and upright: white hair down his back, a long white beard and white brows, a tall
               gold crown with a blue flare in front of a deep-blue flame halo, steel armour over his chest with a gold
               rim and his palm-tree emblem, a white dhoti with a gold border, a blue sash; a steel bow with dark-red
               bands. Faces: calm, speak, stern, rest (eyes shut).
  SALVA        king of Saubha: tan skin, a black moustache, a gold kirita with a green flare in front of a purple flame
               halo, a purple dhoti, a green sash. Faces: calm, proud (turning away), angry.
  SHIVA        blue-grey skin, piled matted hair with the crescent moon and rudraksha, the third eye, three lines of
               ash, a serpent round his neck, a tiger-skin dhoti, his trident (shani_cast's sg_trishul). Calm, kind.
  DRUPADA      king of Panchala: wheat skin, a short dark beard and moustache, a tall gold crown with a red flare and a
               dark-red flame halo, a deep-green dhoti, a red sash. Faces: calm, smile, worry.
  THE QUEEN    his queen: a saffron-gold sari, a green choli, a red pallu, a queen's crown. Faces: open, smile, sad.
  SHIKHANDINI  raised as a boy: the SAME soft face in every shot (female face shape, the same eye, the same small
               gold earring), a saffron turban with red wraps, a gold jewel and a white plume, a teal knee-length tunic
               with a gold border over a cream dhoti. Faces: open, sad, shock. As the grown princess (GIRL, before
               the exchange): the same skin, a teal sari and a saffron pallu (his tunic and turban colours), a small
               gold tiara; faces open, sad, smile, shock. As SHIKHANDI after the exchange: the
               same face with a thin moustache (man), and on the battlefield (war) a gold crest on the turban and gold
               armour instead of the tunic.
  THE BRIDE    the Dasarna princess: a crimson bridal sari with a gold border, a red veil over her hair, a maang tikka.
               Faces: open, smile, shock, sad.
  HER FATHER   King Hiranyavarman of Dasarna: darker tan skin, a curled moustache and a full dark beard, a gold kirita
               with a saffron flare in front of a slate-dark halo, a navy dhoti, a saffron sash. Faces: calm, angry,
               shout.
  THE YAKSHA   Sthunakarna, a forest spirit: leaf-green skin, a crown of standing leaves with small white flowers,
               dark vine-hair, a garland of leaves across his chest, a dark-green dhoti and a lime sash. Faces: calm,
               speak, sad. After Kubera's curse the same spirit as a woman (yakshi): the same skin and leaf crown, a
               dark-green sari with a lime pallu. Faces: open, sad.
  KUBERA       king of the Yakshas: golden skin, a big round belly, a tall gold crown with a red flare and side peaks in
               front of a ring of golden rays, big gold earrings, a red dhoti with a gold border, a green sash; his
               money bag (red, tied with gold, coins spilling). Faces: calm, angry, shout.
Props: Bhishma's bow (strung), the money bag. The Kashi/Drupada palace arch, trees, altar fire, flames, palm-leaf
book, plaque cards, speech cloud, garland, cradle, the chariot, horses, arrows, Arjuna, Yudhishthira, Krishna, the
Kaurava soldiers, the tent and the cot come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import jayadratha_cast as J  # noqa: F401  (registers the chariot, horses, arrows, soldiers, Arjuna)
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import puppet_cast as C
import ravana_cast as R
import shani_cast as S  # noqa: F401  (registers the trident, the cradle)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, PALE, RED, SAFFRON, almond_eye, band, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, spath)

AM_SKIN = (0.99, 0.79, 0.60)          # Amba
AM_SARI = (0.92, 0.38, 0.52)          # rose pink
AM_PALLU = (0.62, 0.10, 0.34)         # deep magenta
TP_SKIN = (0.95, 0.71, 0.50)          # Amba after years of penance (the same face, a little sun-darkened)
TP_CLOTH = (0.86, 0.50, 0.18)         # ochre bark cloth
TP_CLOTH2 = (0.66, 0.36, 0.14)
JATA = (0.36, 0.22, 0.12)             # matted hair
RUDRA = (0.46, 0.20, 0.10)            # rudraksha beads
ASH = K.ASH                           # white hair (a cool grey reads as white on the warm cloth)
ASH2 = K.ASH2
BH_SKIN = (0.97, 0.74, 0.54)          # Bhishma
BH_BLUE = (0.20, 0.38, 0.82)
BH_HALO = (0.14, 0.26, 0.62)
STEEL = (0.70, 0.72, 0.80)
STEEL2 = (0.52, 0.54, 0.64)
SV_SKIN = (0.88, 0.60, 0.38)          # Salva
SV_DHOTI = (0.46, 0.22, 0.58)         # purple
SV_SASH = (0.14, 0.56, 0.40)          # green
SI_SKIN = (0.56, 0.68, 0.88)          # Shiva: blue-grey
TIGER = (0.98, 0.62, 0.18)
SNAKE = (0.40, 0.58, 0.46)
DR_SKIN = (0.90, 0.63, 0.42)          # Drupada
DR_DHOTI = (0.12, 0.46, 0.34)         # deep green
QN_SKIN = (0.99, 0.80, 0.62)          # the queen
QN_SARI = (0.98, 0.66, 0.18)          # saffron gold
SK_SKIN = (0.96, 0.73, 0.52)          # Shikhandini / Shikhandi
TURBAN = (0.98, 0.56, 0.12)           # saffron
TUNIC = (0.12, 0.52, 0.62)            # teal
TUNIC2 = (0.08, 0.36, 0.44)
CREAM = (1.0, 0.94, 0.80)
BR_SKIN = (1.0, 0.82, 0.64)           # the bride
BR_SARI = (0.82, 0.08, 0.18)          # crimson
BR_VEIL = (0.94, 0.20, 0.16)
DS_SKIN = (0.80, 0.52, 0.32)          # the Dasarna king
DS_DHOTI = (0.14, 0.26, 0.54)         # navy
DS_HALO = (0.24, 0.24, 0.34)
YK_SKIN = (0.50, 0.78, 0.54)          # the Yaksha
YK_DHOTI = (0.14, 0.42, 0.24)
YK_LIME = (0.66, 0.86, 0.32)
YK_LEAF = (0.26, 0.62, 0.30)
KB_SKIN = (1.0, 0.82, 0.48)           # Kubera
KB_DHOTI = (0.88, 0.20, 0.12)
RAY = (1.0, 0.88, 0.46)
SIS1 = ((0.20, 0.60, 0.36), (0.10, 0.40, 0.24))   # Ambika: green
SIS2 = ((0.99, 0.62, 0.16), (0.80, 0.30, 0.08))   # Ambalika: saffron

# ------------------------------------------------------------------ women's faces


def _w_eyes(cr, skin, mood):
    """A woman's eye, brow and mouth (puppet_cast's woman head, eye at 30, -112): open | smile | sad | angry |
    shock | shut (meditating, calm) | fierce (the ascetic: wide, hard, the brow pulled down)."""
    if mood == "sad":
        almond_eye(cr, 30, -110, 32, 11, col=PALE)
        cr.new_path()                                                            # the lid lowered over the eye
        cr.move_to(12, -112)
        cr.curve_to(22, -128, 40, -128, 48, -110)
        cr.curve_to(40, -114, 22, -114, 12, -112)
        cr.close_path()
        leather(cr, skin, 2.5)
        ink(cr, [(12, -112), (30, -116), (48, -110)], 4)
        ink(cr, [(12, -126), (30, -132), (50, -144)], 3.5)                       # brow raised at the front
        ink(cr, [(52, -72), (60, -74), (66, -70)], 3, col=RED)
    elif mood == "shock":
        almond_eye(cr, 30, -114, 36, 15, col=PALE)
        ink(cr, [(10, -140), (30, -152), (50, -144)], 3.5)
        cr.new_path()
        ell(cr, 60, -70, 7, 9)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
    elif mood == "shut":
        cr.new_path()
        ell(cr, 30, -112, 19, 13)
        cr.set_source_rgb(*skin)
        cr.fill()
        ink(cr, [(14, -112), (30, -104), (46, -112)], 4)
        for x in (22, 30, 38):
            ink(cr, [(x, -107), (x - 2, -100)], 2.2)
        ink(cr, [(14, -130), (30, -136), (46, -130)], 3.5)
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)
    elif mood == "fierce":
        almond_eye(cr, 30, -112, 34, 13, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(8, -138), (30, -130), (54, -120)], 6.5)
        ink(cr, [(64, -70), (54, -72)], 3.5, col=RED)
    else:
        S._w_eyes(cr, skin, mood)


def lady_head(cr, skin, mood="open", bun=True, flower=PALE, bindi=True, nosering=True, jhumka=True):
    """A woman's profile head without a crown (puppet_cast.woman_head's face, hair and bun), eyes per mood."""
    S._face_w(cr, skin)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    if bun:
        cr.new_path()
        cr.arc(-62, -128, 36, 0, 2 * math.pi)
        leather(cr, HAIR, 4)
        for i in range(8):
            a = 2 * math.pi * i / 8
            punch(cr, [(-62 + 24 * math.cos(a), -128 + 24 * math.sin(a))], 3.5)
        _flower(cr, -62, -128, 14, flower)
    _w_eyes(cr, skin, mood)
    if bindi:
        cr.new_path()
        cr.arc(44, -150, 5, 0, 2 * math.pi)
        cr.set_source_rgb(*RED)
        cr.fill()
    if nosering:
        cr.new_path()
        cr.arc(64, -90, 8, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(3)
        cr.stroke()
    if jhumka:
        _jewel(cr, -10, -70, 11, GOLD)
        poly(cr, [(-24, -58), (-10, -66), (4, -58), (8, -34), (-28, -34)])
        leather(cr, GOLD, 3)
        punch(cr, [(-18, -40), (-10, -40), (-2, -40)], 2.2)


def princess_tiara(cr, gem=RED):
    """A small gold princess tiara: five low peaks over a jewelled band, pearl drops."""
    pts = [(-40, -168), (-36, -198), (-22, -184), (-8, -214), (4, -230), (16, -214), (30, -186), (42, -200),
           (48, -166)]
    _shape(cr, pts, GOLD, 4, smooth=False, holes=(6, 10, 2.0))
    for x, y in ((-36, -186), (-8, -200), (16, -202), (42, -188)):
        cr.new_path()
        cr.arc(x, y + 22, 4.5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _jewel(cr, 4, -200, 8, gem)
    band(cr, [(-42, -170), (50, -168)], 11, gem, spacing=10, hole_r=2.0)


# ------------------------------------------------------------------ Amba, the princess


AM_MOODS = ("open", "smile", "sad", "angry", "shock")


def amba_head(cr, mood="open"):
    lady_head(cr, AM_SKIN, mood)
    princess_tiara(cr, RED)


def _amba_extra(cr):
    """A gold necklace with a magenta pendant and a jewelled belt."""
    band(cr, [(-20, -282), (12, -220), (40, -178)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 40, -168, 10, AM_PALLU)
    for x in (-24, 4, 30):
        _jewel(cr, x, -24, 6, GREEN)


AMBA = woman("sk_amba", skin=AM_SKIN, skirt=AM_SARI, choli=GOLD, border=GOLD, pallu_col=AM_PALLU, gem=AM_PALLU,
             ornaments_extra=_amba_extra, hands=("open", "open"))
for _m in AM_MOODS:
    register("sk_amba_head" + ("" if _m == "open" else "_" + _m), (-150, -270, 100, 40),
             (lambda m: lambda cr: amba_head(cr, m))(_m))


def _sis_head(cr, gem):
    lady_head(cr, AM_SKIN, "open")
    princess_tiara(cr, gem)


SIS_A = woman("sk_sisa", skin=AM_SKIN, skirt=SIS1[0], choli=GOLD, border=GOLD, pallu_col=SIS1[1], gem=RED,
              hands=("open", "open"))
SIS_B = woman("sk_sisb", skin=AM_SKIN, skirt=SIS2[0], choli=GOLD, border=DRED, pallu_col=SIS2[1], gem=GREEN,
              hands=("open", "open"))
register("sk_sisa_head", (-150, -270, 100, 40), lambda cr: _sis_head(cr, GREEN))
register("sk_sisb_head", (-150, -270, 100, 40), lambda cr: _sis_head(cr, RED))

# ------------------------------------------------------------------ Amba, the ascetic


TP_MOODS = ("fierce", "shut", "open")


def tapas_head(cr, mood="fierce"):
    """Amba after years of penance: long matted locks down her back, a high bun of matted hair wound with rudraksha,
    three ash lines and a red dot on her forehead, rudraksha earrings."""
    for k, (x0, ln) in enumerate(((-40, 1.0), (-56, 0.86), (-24, 0.74))):         # matted locks down her back
        lock = [(x0 + 10, -150), (x0 - 24, -90), (x0 - 40 - 6 * k, 0), (x0 - 44 - 4 * k, 90 * ln),
                (x0 - 26 - 4 * k, 96 * ln), (x0 - 20, 0), (x0 - 4, -90), (x0 + 24, -140)]
        _shape(cr, lock, JATA if k != 1 else (0.30, 0.18, 0.10), 4)
        for j in range(4):
            y = -100 + 46 * j
            ink(cr, [(x0 - 26 - 4 * j, y), (x0 - 12 - 4 * j, y + 10)], 2.4, col=(0.56, 0.38, 0.22))
    S._face_w(cr, TP_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, JATA, 4)
    for k in range(5):                                                            # the high bun of matted coils
        cr.new_path()
        ell(cr, -14 + 3 * k, -196 - 26 * k, 46 - 6 * k, 20)
        leather(cr, JATA, 4)
        ink(cr, [(-50 + 8 * k, -196 - 26 * k), (-14, -186 - 26 * k), (24 - 6 * k, -198 - 26 * k)], 2.4,
            col=(0.56, 0.38, 0.22))
    for i in range(7):                                                            # rudraksha wound round it
        a = -0.4 + 0.5 * i
        cr.new_path()
        cr.arc(-14 + 40 * math.cos(a) * 0.9, -232 + 12 * math.sin(a) - 8 * i, 5.5, 0, 2 * math.pi)
        leather(cr, RUDRA, 2)
    _w_eyes(cr, TP_SKIN, mood)
    for k in range(3):                                                            # ash lines
        ink(cr, [(6, -160 + 8 * k), (48, -162 + 8 * k)], 3.2, col=(1.0, 0.97, 0.9))
    cr.new_path()
    cr.arc(30, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    for k in range(3):                                                            # rudraksha earring
        cr.new_path()
        cr.arc(-10, -70 + 13 * k, 6 - k, 0, 2 * math.pi)
        leather(cr, RUDRA, 2)


def _tapas_extra(cr):
    """A long rudraksha mala."""
    for i in range(14):
        u = i / 13
        cr.new_path()
        cr.arc(-24 + 64 * u, -278 + 160 * u + 30 * u * u, 7, 0, 2 * math.pi)
        leather(cr, RUDRA, 2)


TAPAS = woman("sk_tapas", skin=TP_SKIN, skirt=TP_CLOTH, choli=TP_CLOTH2, border=TP_CLOTH2, pallu_col=TP_CLOTH2,
              gem=RUDRA, ornaments_extra=_tapas_extra, hands=("open", "open"))
for _m in TP_MOODS:
    register("sk_tapas_head" + ("" if _m == "fierce" else "_" + _m), (-170, -340, 100, 120),
             (lambda m: lambda cr: tapas_head(cr, m))(_m))

# ------------------------------------------------------------------ Bhishma


BH_MOODS = ("calm", "speak", "stern", "rest")


def bhishma_head(cr, mood="calm"):
    """Bhishma: a deep-blue flame halo, white hair down his back, white brows, a long white beard and moustache, a
    tall gold crown with a blue flare. mood: calm | speak (the mouth open over the beard) | stern | rest (eyes shut)."""
    K._halo(cr, BH_HALO)
    hp = [(-30, -176), (-64, -146), (-92, -70), (-98, 40), (-74, 110), (-48, 64), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-76 - 6 * k, -20), (-68 - 4 * k, 80)], 2.5, col=ASH2)
    fm = {"calm": "calm", "speak": "calm", "stern": "angry", "rest": "shame"}[mood]
    A.face(cr, dict(skin=BH_SKIN, hair=False, moustache=False, tilak=True), fm)
    if mood == "stern":
        ink(cr, [(6, -152), (34, -144), (62, -128)], 9, col=ASH)
    elif mood == "rest":
        ink(cr, [(12, -134), (34, -142), (58, -152)], 8, col=ASH)
    else:
        ink(cr, [(12, -140), (34, -150), (60, -140)], 8, col=ASH)
    ink(cr, [(52, -104), (60, -96)], 2.5)                                          # age lines
    ink(cr, [(8, -92), (20, -80)], 2.5)
    ink(cr, [(20, -170), (40, -172)], 2.2)
    bp = [(66, -60), (72, -30), (70, 20), (60, 80), (44, 140), (26, 176), (12, 132), (-4, 70), (-12, 4), (-4, -40),
          (18, -58), (42, -62)]
    _shape(cr, bp, ASH, 4)
    for k in range(4):
        ink(cr, [(54 - 12 * k, -44), (48 - 13 * k, 40), (38 - 10 * k, 120)], 2.5, col=ASH2)
    m = [(76, -76), (52, -86), (26, -90), (6, -76), (28, -80), (52, -76), (78, -71)]
    _shape(cr, m, ASH, 3)
    if mood == "speak":
        cr.new_path()
        ell(cr, 62, -62, 9, 7)
        leather(cr, (0.40, 0.08, 0.06), 2.5)
    R.kirita(cr, GOLD, None, tall=1.22, flare=BH_BLUE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.22, 10, BH_BLUE)


_BH = dict(skin=BH_SKIN, bulk=1.1, dhoti=PALE, border=GOLD, pleat=GOLD, sash=BH_BLUE, neck=GOLD)
BHISHMA = man("sk_bhishma", crown="tiara", halo=False, hair=False, moustache=False, hands=("fist", "fist"), **_BH)


def _palm(cr, x, y, s):
    """Bhishma's emblem, the palm tree (tala), small."""
    ink(cr, [(x, y + 34 * s), (x + 2 * s, y - 10 * s)], 5 * s, col=BROWN)
    for a in (-2.6, -2.1, -1.57, -1.05, -0.55):
        ink(cr, [(x + 2 * s, y - 10 * s), (x + 2 * s + 30 * s * math.cos(a), y - 10 * s + 24 * s * math.sin(a))],
            4 * s, col=DGREEN)


def bhishma_body(cr):
    """His body with steel armour over the chest: a gold rim, rows of scales, the palm-tree emblem on a gold disc."""
    C.man_body(cr, _BH)
    b = _BH["bulk"]
    plate = [(-50 * b, -64), (-58 * b, -170), (-50 * b, -240), (-24, -280), (20, -286), (54 * b, -256), (80 * b, -206),
             (76 * b, -160), (60 * b, -106), (52 * b, -64)]
    _shape(cr, plate, STEEL, 5)
    for row in range(6):
        y = -246 + 30 * row
        for k in range(6):
            x = -44 * b + 22 * k + (11 if row % 2 else 0)
            if x > 70 * b - 8 * row:
                continue
            ink(cr, [(x - 9, y), (x, y + 10), (x + 9, y)], 2.4, col=STEEL2)
    band(cr, [(-52 * b, -240), (-20, -276), (22, -282), (56 * b, -252)], 12, GOLD, spacing=11, hole_r=2.2)
    cr.new_path()
    cr.arc(24, -170, 34, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    _palm(cr, 24, -168, 0.85)
    band(cr, [(-52 * b, -70), (54 * b, -70)], 14, DRED, spacing=11, hole_r=2.2)


register("sk_bhishma_body", (-200, -330, 140, 300), bhishma_body)
for _m in BH_MOODS:
    register("sk_bhishma_head" + ("" if _m == "calm" else "_" + _m), (-230, -500, 120, 190),
             (lambda m: lambda cr: bhishma_head(cr, m))(_m))
register("sk_bhishma_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, BH_SKIN, PALE, GOLD, 1.1))


def _bow(cr, string=True):
    """Bhishma's bow (grip at 0, 0; the belly bulges to +x, the string at x = -88, its tips at y = -/+338): steel limbs
    with dark-red bands and gold tips."""
    cr.new_path()
    cr.move_to(-90, -340)
    cr.curve_to(40, -220, 40, 220, -90, 340)
    cr.set_line_cap(1)
    cr.set_source_rgb(*INK)
    cr.set_line_width(28)
    cr.stroke_preserve()
    cr.set_source_rgb(*STEEL)
    cr.set_line_width(17)
    cr.stroke()
    for s in (-1, 1):
        for y in (90, 170, 250):
            u = y / 340
            x = -90 + 130 * 0.75 * (1 - u * u) - 6
            band(cr, [(x - 12, s * y), (x + 12, s * (y + 6))], 9, DRED, holes=False)
        for w, col in ((16, INK), (8, GOLD)):
            cr.new_path()
            spath(cr, [(-90, s * 338), (-70, s * 376), (-36, s * 384)], closed=False)
            cr.set_source_rgb(*col)
            cr.set_line_width(w)
            cr.stroke()
    band(cr, [(8, -46), (8, 46)], 28, DRED, spacing=10, hole_r=2.0)
    _jewel(cr, 10, 0, 8, GOLD)
    if string:
        ink(cr, [(-88, -338), (-88, 338)], 3.0, smooth=False)


register("sk_bow", (-110, -400, 60, 400), _bow)

# ------------------------------------------------------------------ Salva


SV_MOODS = ("calm", "proud", "angry")


def salva_head(cr, mood="calm"):
    K._halo(cr, SV_DHOTI)
    A.face(cr, dict(skin=SV_SKIN, hair=True, moustache=True, tilak=True), mood)
    R.kirita(cr, GOLD, None, tall=1.05, flare=SV_SASH)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.05, 9, SV_SASH)


SALVA = man("sk_salva", skin=SV_SKIN, bulk=1.06, dhoti=SV_DHOTI, border=GOLD, pleat=GOLD, sash=SV_SASH, neck=GOLD,
            crown="tiara", halo=False, moustache=True, hands=("open", "open"))
for _m in SV_MOODS:
    register("sk_salva_head" + ("" if _m == "calm" else "_" + _m), (-220, -460, 120, 110),
             (lambda m: lambda cr: salva_head(cr, m))(_m))

# ------------------------------------------------------------------ Shiva


def shiva_head(cr, mood="calm"):
    """Shiva: piled matted hair with the crescent moon and rudraksha, matted locks down his back, the third eye,
    three lines of ash, big gold earrings; calm (eyes half shut, kind) or speak."""
    for k, x0 in enumerate((-36, -58)):                                           # locks down his back
        lock = [(x0 + 10, -160), (x0 - 26, -90), (x0 - 40, 10), (x0 - 46 + 6 * k, 100), (x0 - 26, 104),
                (x0 - 18, 10), (x0 - 2, -90), (x0 + 26, -150)]
        _shape(cr, lock, JATA, 4)
        holes_line(cr, [(x0 - 6, -120), (x0 - 28, 0), (x0 - 34, 80)], 16, 2.4)
    o = dict(skin=SI_SKIN, hair=False, moustache=False, tilak=False, earring=False)
    A.face(cr, o, "calm")
    if mood != "speak":                                                           # the eyes half shut: calm, inward
        cr.new_path()
        cr.move_to(14, -120)
        cr.curve_to(24, -138, 44, -138, 54, -118)
        cr.curve_to(44, -124, 24, -124, 14, -120)
        cr.close_path()
        leather(cr, SI_SKIN, 2.5)
        ink(cr, [(14, -120), (34, -126), (54, -118)], 4)
    else:
        cr.new_path()
        ell(cr, 62, -68, 6, 7)
        leather(cr, (0.36, 0.08, 0.10), 2.5)
    for k in range(3):                                                            # ash lines
        ink(cr, [(0, -156 + 9 * k), (52, -158 + 9 * k)], 3.4, col=(1.0, 0.98, 0.92))
    cr.new_path()                                                                 # the third eye
    ell(cr, 34, -168, 5, 10)
    leather(cr, RED, 2)
    for k in range(5):                                                            # the piled jata
        cr.new_path()
        ell(cr, -10 - 2 * k, -196 - 30 * k, 54 - 7 * k, 22)
        leather(cr, JATA, 4)
        ink(cr, [(-50 + 7 * k, -196 - 30 * k), (-10, -186 - 30 * k), (32 - 7 * k, -198 - 30 * k)], 2.5,
            col=(0.58, 0.40, 0.22))
    for i in range(6):
        cr.new_path()
        cr.arc(-40 + 13 * i, -212 + 3 * math.sin(i), 6, 0, 2 * math.pi)
        leather(cr, RUDRA, 2)
    cr.save()                                                                     # the crescent moon
    cr.translate(34, -300)
    cr.rotate(-0.5)
    outer = [(36 * math.cos(a), 36 * math.sin(a)) for a in (math.pi * (-0.62 + 1.24 * i / 16) for i in range(17))]
    inner = [(-14 + 30 * math.cos(a), 30 * math.sin(a)) for a in (math.pi * (0.52 - 1.04 * i / 16)
                                                                  for i in range(17))]
    _shape(cr, outer + inner, (1.0, 0.98, 0.86), 3.5, smooth=False)
    cr.restore()
    for r, col in ((24, GOLD), (14, (1.0, 0.7, 0.3))):                           # earring
        cr.new_path()
        cr.arc(-12, -62, r, 0, 2 * math.pi)
        leather(cr, col, 3.5)
    punch(cr, [(-12, -62)], 4)


_SI = dict(skin=SI_SKIN, bulk=1.08, dhoti=TIGER, border=INK, pleat=TIGER, sash=(0.80, 0.30, 0.14), neck=RUDRA,
           beads=True)
SHIVA = man("sk_shiva", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
            **_SI)


def _stripes(cr, path_fn, x0, x1, y0, y1, step=34):
    cr.save()
    cr.new_path()
    path_fn()
    cr.clip()
    k = 0
    x = x0
    while x < x1:
        ink(cr, [(x, y0), (x + 14, (y0 + y1) / 2), (x - 4, y1)], 6, col=INK)
        x += step + 6 * (k % 2)
        k += 1
    cr.restore()


def shiva_body(cr):
    """His body: rudraksha beads, a serpent coiled round his neck with its hood at his chest, a tiger-skin wrap."""
    C.man_body(cr, _SI)
    b = _SI["bulk"]
    wrap = [(-62 * b, -40), (0, -50), (64 * b, -42), (74 * b, 10), (70 * b, 48), (0, 56), (-70 * b, 48), (-74 * b, 10)]
    _stripes(cr, lambda: spath(cr, wrap), -80, 90, -50, 60)
    band(cr, [(-30, -286), (0, -270), (30 * b, -250), (62 * b, -224)], 18, SNAKE, spacing=12, hole_r=2.4)
    body = [(62 * b, -224), (74 * b, -196), (70 * b, -160), (54 * b, -150)]
    band(cr, body, 16, SNAKE, spacing=12, hole_r=2.4)
    hood = [(40 * b, -150), (54 * b, -178), (72 * b, -186), (88 * b, -170), (86 * b, -140), (70 * b, -126),
            (52 * b, -128)]
    _shape(cr, hood, SNAKE, 4)
    ink(cr, [(58 * b, -164), (70 * b, -150), (80 * b, -162)], 2.4, col=(0.86, 0.92, 0.70))
    punch(cr, [(76 * b, -168)], 3)


def _tiger_leg(o, side=None):
    def fn(cr):
        C.leg(cr, o, side)
        b = o["bulk"]
        dl = [(-42 * b, -10), (0, -26), (46 * b, -10), (54 * b, 80), (46 * b, 170), (32 * b, 214), (-26 * b, 214),
              (-38 * b, 170), (-48 * b, 80)]
        _stripes(cr, lambda: spath(cr, dl), -60, 70, -20, 220, 40)
    return fn


register("sk_shiva_body", (-200, -330, 140, 300), shiva_body)
register("sk_shiva_legF", (-70, -40, 90, 440), _tiger_leg(_SI))
register("sk_shiva_legB", (-70, -40, 90, 440), _tiger_leg(_SI))
for _m in ("calm", "speak"):
    register("sk_shiva_head" + ("" if _m == "calm" else "_" + _m), (-200, -470, 120, 130),
             (lambda m: lambda cr: shiva_head(cr, m))(_m))

# ------------------------------------------------------------------ Drupada and his queen


DR_MOODS = ("calm", "smile", "worry")


def drupada_head(cr, mood="calm"):
    K._halo(cr, DRED)
    A.face(cr, dict(skin=DR_SKIN, hair=True, moustache=True, beard=True, tilak=True),
           {"calm": "calm", "smile": "smile", "worry": "hurt"}[mood])
    R.kirita(cr, GOLD, None, tall=1.18, flare=RED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.18, 10, GREEN)


DRUPADA = man("sk_drupada", skin=DR_SKIN, bulk=1.1, dhoti=DR_DHOTI, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
              crown="tiara", halo=False, moustache=True, hands=("open", "open"))
for _m in DR_MOODS:
    register("sk_drupada_head" + ("" if _m == "calm" else "_" + _m), (-220, -490, 120, 110),
             (lambda m: lambda cr: drupada_head(cr, m))(_m))


def queen_head(cr, mood="open"):
    lady_head(cr, QN_SKIN, mood, flower=GOLD)
    K.queen_crown(cr)


def _queen_extra(cr):
    band(cr, [(-22, -282), (10, -206), (34, -150)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 36, -140, 11, GREEN)


QUEEN = woman("sk_queen", skin=QN_SKIN, skirt=QN_SARI, choli=GREEN, border=RED, pallu_col=RED, gem=RED,
              ornaments_extra=_queen_extra, hands=("open", "open"))
for _m in ("open", "smile", "sad"):
    register("sk_queen_head" + ("" if _m == "open" else "_" + _m), (-150, -310, 100, 40),
             (lambda m: lambda cr: queen_head(cr, m))(_m))

# ------------------------------------------------------------------ Shikhandini / Shikhandi


SK_MOODS = ("open", "sad", "shock", "man", "war")


def turban(cr, war=False):
    """A saffron turban wrapped round the head (head coordinates), red wraps, a gold jewel (sarpech) and a white plume;
    war = a gold crest plate and a red plume instead."""
    tail = [(-48, -150), (-78, -110), (-92, -40), (-84, 6), (-68, -34), (-58, -100)]
    _shape(cr, tail, TURBAN, 4)
    holes_line(cr, [(-62, -128), (-78, -70), (-80, -20)], 14, 2.2)
    dome = [(-58, -116), (-64, -164), (-48, -220), (-6, -254), (40, -244), (62, -206), (60, -160), (44, -148),
            (6, -160), (-30, -142)]
    _shape(cr, dome, TURBAN, 5)
    for k in range(4):                                                            # the wraps
        y0 = -132 - 26 * k
        ink(cr, [(-58 + 4 * k, y0 + 10), (-10, y0 - 22), (56 - 6 * k, y0 - 44)], 7, col=RED if k % 2 else DRED)
    holes_line(cr, [(-40, -150), (0, -186), (44, -214)], 14, 2.2)
    if war:
        crest = [(-30, -236), (-20, -290), (0, -318), (24, -300), (40, -250), (10, -246)]
        _shape(cr, crest, GOLD, 4, holes=(7, 10, 2.0))
        _jewel(cr, 8, -282, 9, RED)
        plume = [(4, -312), (-6, -344), (-30, -372), (-58, -380), (-40, -362), (-22, -338), (-10, -312)]
        _shape(cr, plume, RED, 3.5)
        for k in range(5):
            ink(cr, [(-4 - 10 * k, -318 - 12 * k), (-14 - 10 * k, -330 - 6 * k)], 2.0, col=(1.0, 0.7, 0.5))
    else:
        plume = [(28, -228), (22, -262), (6, -294), (-16, -314), (-6, -288), (8, -258), (18, -226)]
        _shape(cr, plume, PALE, 3.5)
        ink(cr, [(22, -236), (10, -270), (-8, -300)], 2.0, col=(0.7, 0.62, 0.5))
    _jewel(cr, 34, -214, 11, GREEN)
    _shape(cr, [(30, -228), (40, -228), (36, -200)], GOLD, 2.5, smooth=False)


def shk_head(cr, mood="open"):
    """Shikhandini's face (the same in every shot: a woman's face shape, the same eye, the same small gold earring)
    under the saffron turban. mood: open | sad | shock | man (Shikhandi: a thin moustache) | war (and the crest)."""
    S._face_w(cr, SK_SKIN)
    hair = [(-40, -150), (-10, -166), (-30, -110), (-44, -90), (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    eyes = {"man": "open", "war": "fierce"}.get(mood, mood)
    _w_eyes(cr, SK_SKIN, eyes)
    if mood in ("man", "war"):
        m = [(64, -76), (50, -82), (36, -84), (26, -96), (36, -90), (50, -82), (66, -79)]
        _shape(cr, m, HAIR, 2.5)
        ink(cr, [(20, -40), (36, -28)], 2.5)                                      # a firmer jaw line
    cr.new_path()
    cr.arc(-10, -66, 9, 0, 2 * math.pi)
    leather(cr, GOLD, 3)
    poly(cr, [(-16, -56), (-10, -40), (-4, -56)])
    leather(cr, GOLD, 2.5)
    ink(cr, [(46, -160), (48, -176)], 4.5, col=RED)                               # a small red tilak
    turban(cr, war=mood == "war")


_SK = dict(skin=SK_SKIN, bulk=0.95, dhoti=CREAM, border=TUNIC, pleat=TUNIC, sash=RED, neck=GOLD)
SHK = man("sk_shk", crown="tiara", halo=False, hair=False, moustache=False, earring=False, hands=("open", "open"),
          **_SK)


def shk_body(cr):
    """Raised as a son: a teal knee-length tunic (angarkha) with a gold border over the cream dhoti, a red sash."""
    C.man_body(cr, _SK)
    b = _SK["bulk"]
    tunic = [(-56 * b, -250), (-30, -288), (24, -298), (40 * b, -282), (70 * b, -250), (88 * b, -206), (84 * b, -160),
             (66 * b, -104), (62 * b, -40), (76 * b, 30), (96 * b, 150), (40 * b, 160), (-40 * b, 156), (-84 * b, 146),
             (-70 * b, 30), (-60 * b, -60), (-66 * b, -180)]
    _shape(cr, tunic, TUNIC, 6)
    dots_in(cr, lambda: spath(cr, tunic), 22, 3.0, shape="d")
    band(cr, [(-80 * b, 144), (0, 154), (94 * b, 148)], 16, GOLD, spacing=11, hole_r=2.2)
    band(cr, [(24, -292), (40 * b, -230), (52 * b, -150), (60 * b, -60), (74 * b, 40), (92 * b, 140)], 12, GOLD,
         spacing=11, hole_r=2.0)
    band(cr, [(-66 * b, -30), (0, -40), (66 * b, -34)], 20, RED, spacing=11, hole_r=2.4)
    _shape(cr, [(-60 * b, -30), (-96 * b, 30), (-108 * b, 96), (-84 * b, 90), (-74 * b, 20)], RED, 4)
    band(cr, [(-12, -290), (26 * b, -256), (60 * b, -228)], 11, GOLD, spacing=11, hole_r=2.0)


def shk_war_body(cr):
    """Shikhandi on the battlefield: gold armour over the chest with a teal rim, the red sash."""
    C.man_body(cr, dict(_SK, dhoti=CREAM))
    b = _SK["bulk"]
    plate = [(-50 * b, -64), (-58 * b, -170), (-50 * b, -240), (-24, -280), (20, -286), (54 * b, -256), (80 * b, -206),
             (76 * b, -160), (60 * b, -106), (52 * b, -64)]
    _shape(cr, plate, GOLD, 5)
    for row in range(6):
        y = -246 + 30 * row
        for k in range(6):
            x = -44 * b + 22 * k + (11 if row % 2 else 0)
            if x > 70 * b - 8 * row:
                continue
            ink(cr, [(x - 9, y), (x, y + 10), (x + 9, y)], 2.4, col=(0.70, 0.46, 0.10))
    band(cr, [(-52 * b, -240), (-20, -276), (22, -282), (56 * b, -252)], 12, TUNIC, spacing=11, hole_r=2.2)
    _jewel(cr, 22, -176, 16, TUNIC)
    band(cr, [(-52 * b, -70), (54 * b, -70)], 14, RED, spacing=11, hole_r=2.2)


register("sk_shk_body", (-200, -330, 140, 300), shk_body)
register("sk_shk_body_war", (-200, -330, 140, 300), shk_war_body)
for _m in SK_MOODS:
    register("sk_shk_head" + ("" if _m == "open" else "_" + _m), (-150, -420, 110, 40),
             (lambda m: lambda cr: shk_head(cr, m))(_m))

def girl_head(cr, mood="open"):
    """Shikhandi as the grown king's daughter (before the exchange): the same skin, a small gold tiara with a green
    jewel, jasmine in her bun."""
    lady_head(cr, SK_SKIN, mood, flower=PALE)
    princess_tiara(cr, GREEN)


# the same colours as the man she becomes: a teal sari (his tunic), a saffron pallu (his turban)
GIRL = woman("sk_girl", skin=SK_SKIN, skirt=TUNIC, choli=GOLD, border=GOLD, pallu_col=TURBAN, gem=RED,
             hands=("open", "open"))
for _m in ("open", "sad", "smile", "shock"):
    register("sk_girl_head" + ("" if _m == "open" else "_" + _m), (-150, -270, 100, 40),
             (lambda m: lambda cr: girl_head(cr, m))(_m))

# ------------------------------------------------------------------ the Dasarna princess and her father


BR_MOODS = ("open", "smile", "shock", "sad")


def bride_head(cr, mood="open"):
    """The bride: a red veil over her hair (gold border), a maang tikka, a nose ring, jhumkas."""
    lady_head(cr, BR_SKIN, mood, bun=True, flower=GOLD)
    veil = [(-30, -176), (8, -196), (40, -184), (48, -168), (10, -176), (-30, -158), (-74, -120), (-104, -40),
            (-120, 60), (-90, 70), (-80, -20), (-96, -120), (-70, -160)]
    _shape(cr, veil, BR_VEIL, 4)
    dots_in(cr, lambda: spath(cr, veil), 18, 2.4)
    band(cr, [(46, -170), (8, -188), (-30, -168), (-76, -126), (-106, -40), (-118, 56)], 10, GOLD, spacing=10,
         hole_r=1.8)
    ink(cr, [(20, -186), (34, -164)], 2.5, col=GOLD)                              # maang tikka
    _jewel(cr, 36, -160, 7, RED)


BRIDE = woman("sk_bride", skin=BR_SKIN, skirt=BR_SARI, choli=GOLD, border=GOLD, pallu_col=BR_VEIL, gem=GREEN,
              ornaments_extra=_queen_extra, hands=("open", "open"))
for _m in BR_MOODS:
    register("sk_bride_head" + ("" if _m == "open" else "_" + _m), (-170, -260, 100, 100),
             (lambda m: lambda cr: bride_head(cr, m))(_m))

DS_MOODS = ("calm", "angry", "shout")


def dasarna_head(cr, mood="calm"):
    K._halo(cr, DS_HALO)
    A.face(cr, dict(skin=DS_SKIN, hair=True, moustache=True, beard=True, tilak=True),
           {"calm": "calm", "angry": "angry", "shout": "scold"}[mood])
    _shape(cr, [(60, -52), (66, -24), (60, 10), (44, 40), (22, 40), (6, 10), (-6, -30), (14, -36), (34, -44)], HAIR, 4)
    ink(cr, [(28, -88), (8, -86), (0, -100), (12, -110)], 4.5, col=HAIR)            # the curled moustache's end
    if mood == "shout":
        _shape(cr, [(74, -84), (48, -74), (70, -52 + 14 - 26)], (0.42, 0.05, 0.06), 3, smooth=False)
    dasarna_crown(cr)


def dasarna_crown(cr):
    """A domed gold crown (a rounded mitre) with saffron bands, side flaps and a spike: unlike the kiritas."""
    for sx in (-1, 1):
        _shape(cr, [(sx * 50, -150), (sx * 74, -136), (sx * 70, -96), (sx * 52, -110)], GOLD, 4, smooth=False)
    dome = [(-54, -150), (-60, -200), (-46, -256), (-14, -290), (16, -292), (46, -262), (60, -206), (58, -150)]
    _shape(cr, dome, GOLD, 6, holes=(10, 14, 2.6))
    for y, w in ((-196, 56), (-246, 44)):
        band(cr, [(-w, y), (w + 2, y - 2)], 12, SAFFRON, spacing=11, hole_r=2.2)
    _jewel(cr, 4, -222, 12, (0.10, 0.54, 0.58))
    poly(cr, [(-6, -290), (0, -336), (6, -290)])
    leather(cr, GOLD, 3)
    band(cr, [(-58, -156), (62, -150)], 16, (0.10, 0.54, 0.58), spacing=12)


DASARNA = man("sk_dasarna", skin=DS_SKIN, bulk=1.14, dhoti=DS_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
              crown="tiara", halo=False, moustache=True, hands=("fist", "open"))
for _m in DS_MOODS:
    register("sk_dasarna_head" + ("" if _m == "calm" else "_" + _m), (-220, -460, 120, 110),
             (lambda m: lambda cr: dasarna_head(cr, m))(_m))

# ------------------------------------------------------------------ the Yaksha Sthunakarna (and as a yakshi)


def leaf_crown(cr, y0=-160):
    """A crown of standing leaves with small white flowers (head coordinates; its band at y0)."""
    for k, (x, a, ln) in enumerate(((-52, -0.62, 90), (-36, -0.36, 120), (-16, -0.14, 150), (6, 0.06, 160),
                                    (26, 0.26, 140), (44, 0.5, 110), (56, 0.8, 80))):
        cr.save()
        cr.translate(x, y0)
        cr.rotate(a)
        leaf = [(0, 0), (-ln * 0.2, -ln * 0.4), (-ln * 0.08, -ln * 0.8), (0, -ln), (ln * 0.08, -ln * 0.8),
                (ln * 0.2, -ln * 0.4)]
        _shape(cr, leaf, YK_LEAF if k % 2 else DGREEN, 3.5)
        ink(cr, [(0, -6), (0, -ln * 0.9)], 2.2, col=YK_LIME)
        cr.restore()
    band(cr, [(-56, y0), (0, y0 - 8), (60, y0 + 2)], 16, YK_LIME, spacing=11, hole_r=2.2)
    for x in (-40, -6, 30):
        _flower(cr, x, y0 - 6, 11, PALE, 6)


YK_MOODS = ("calm", "speak", "sad")


def yaksha_head(cr, mood="calm"):
    o = dict(skin=YK_SKIN, hair=True, moustache=False, tilak=False, earring=False)
    A.face(cr, o, {"calm": "calm", "speak": "calm", "sad": "shame"}[mood])
    if mood == "speak":
        cr.new_path()
        ell(cr, 62, -68, 6, 7)
        leather(cr, (0.24, 0.10, 0.08), 2.5)
    ink(cr, [(48, -150), (52, -176)], 4.5, col=YK_LIME)
    for k in range(3):                                                            # vine earring
        cr.new_path()
        cr.arc(-12 - 4 * k, -70 + 14 * k, 7, 0, 2 * math.pi)
        leather(cr, YK_LIME, 2)
    leaf_crown(cr)


def yaksha_body(cr):
    """A garland of leaves (vanamala) across his chest over a plain leafy body."""
    C.man_body(cr, _YK)
    for i in range(11):
        u = i / 10
        x, y = -40 + 110 * u, -276 + 230 * u + 40 * u * u
        cr.save()
        cr.translate(x, y)
        cr.rotate(0.6 + 0.4 * math.sin(i))
        _shape(cr, [(0, -16), (12, 0), (0, 16), (-12, 0)], YK_LEAF if i % 2 else YK_LIME, 2.5)
        cr.restore()


_YK = dict(skin=YK_SKIN, bulk=1.0, dhoti=YK_DHOTI, border=YK_LIME, pleat=YK_LIME, sash=YK_LIME, neck=YK_LIME)
YAKSHA = man("sk_yaksha", crown="tiara", halo=False, hair=True, earring=False, tilak=False, hands=("open", "open"),
             **_YK)
register("sk_yaksha_body", (-200, -330, 140, 300), yaksha_body)
for _m in YK_MOODS:
    register("sk_yaksha_head" + ("" if _m == "calm" else "_" + _m), (-170, -340, 110, 110),
             (lambda m: lambda cr: yaksha_head(cr, m))(_m))


def yakshi_head(cr, mood="open"):
    lady_head(cr, YK_SKIN, mood, flower=PALE, nosering=False)
    leaf_crown(cr, -168)


YAKSHI = woman("sk_yakshi", skin=YK_SKIN, skirt=YK_DHOTI, choli=YK_LIME, border=YK_LIME, pallu_col=YK_LIME, gem=PALE,
               hands=("open", "open"))
for _m in ("open", "sad"):
    register("sk_yakshi_head" + ("" if _m == "open" else "_" + _m), (-160, -340, 100, 40),
             (lambda m: lambda cr: yakshi_head(cr, m))(_m))

# ------------------------------------------------------------------ Kubera


KB_MOODS = ("calm", "angry", "shout")


def kubera_head(cr, mood="calm"):
    """Kubera: a ring of golden rays, a tall gold crown with side peaks and a red flare, big gold earrings, a round
    full face with a moustache."""
    M._ray_halo(cr, -26, -262, 100, 156, 16, (RAY, GOLD))
    A.face(cr, dict(skin=KB_SKIN, hair=True, moustache=True, tilak=True, earring=False),
           {"calm": "smile", "angry": "angry", "shout": "scold"}[mood])
    ink(cr, [(30, -20), (50, -26)], 2.6)                                          # a double chin
    R.kirita(cr, GOLD, None, tall=1.36, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.36
    for sx in (-1, 1):
        _shape(cr, [(sx * 30, -170), (sx * 66, h(-240)), (sx * 52, h(-290)), (sx * 38, h(-238)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 50, h(-254), 7, GREEN)
    _jewel(cr, 2, h(-292), 11, GREEN)
    for r, col in ((26, GOLD), (15, RED)):
        cr.new_path()
        cr.arc(-14, -60, r, 0, 2 * math.pi)
        leather(cr, col, 4)
    punch(cr, [(-14, -60)], 4)


_KB = dict(skin=KB_SKIN, bulk=1.2, dhoti=KB_DHOTI, border=GOLD, pleat=GOLD, sash=GREEN, neck=GOLD)
KUBERA = man("sk_kubera", crown="tiara", halo=False, moustache=True, hands=("open", "open"), **_KB)


def kubera_body(cr):
    """His big round belly (puppet_cast.man_body with the belly drawn over the lower torso), gold necklaces, a jewelled
    belt."""
    C.man_body(cr, _KB)
    b = _KB["bulk"]
    belly = [(-40 * b, -170), (20, -196), (80 * b, -190), (124 * b, -140), (136 * b, -80), (120 * b, -20), (70 * b, 10),
             (0, 14), (-60 * b, 0), (-62 * b, -90)]
    _shape(cr, belly, KB_SKIN, 6)
    ink(cr, [(60 * b, -170), (100 * b, -150)], 3)
    punch(cr, [(96 * b, -92)], 6)
    ink(cr, [(84 * b, -110), (100 * b, -112)], 2.4)
    band(cr, [(-64 * b, -6), (40, 12), (118 * b, -4)], 20, GOLD, spacing=11, hole_r=2.4)
    for x in (-30, 30, 90):
        _jewel(cr, x * b, 4 + (x == 90) * -6, 8, RED)
    band(cr, [(-16, -290), (24 * b, -246), (72 * b, -200)], 12, GOLD, spacing=10, hole_r=2.0)
    band(cr, [(-26, -282), (20 * b, -196), (80 * b, -150)], 10, GOLD, spacing=10, hole_r=2.0)
    _jewel(cr, 82 * b, -146, 13, GREEN)


register("sk_kubera_body", (-220, -330, 190, 300), kubera_body)
for _m in KB_MOODS:
    register("sk_kubera_head" + ("" if _m == "calm" else "_" + _m), (-270, -520, 190, 110),
             (lambda m: lambda cr: kubera_head(cr, m))(_m))


def _bag(cr):
    """Kubera's money bag (grip at the knot, 0, 0): a round red bag tied with gold, gold coins on it."""
    body = [(-20, 10), (-70, 50), (-96, 120), (-80, 190), (0, 222), (80, 190), (96, 120), (70, 50), (20, 10)]
    _shape(cr, body, RED, 5)
    dots_in(cr, lambda: spath(cr, body), 22, 3.0, shape="d")
    band(cr, [(-26, 14), (26, 14)], 16, GOLD, spacing=10, hole_r=2.0)
    _shape(cr, [(-14, 10), (-30, -24), (0, -12), (30, -24), (14, 10)], RED, 4)
    for x, y in ((-50, 120), (0, 150), (50, 120), (-20, 90), (26, 92)):
        _jewel(cr, x, y, 12, GOLD)


register("sk_bag", (-110, -40, 110, 236), _bag)
