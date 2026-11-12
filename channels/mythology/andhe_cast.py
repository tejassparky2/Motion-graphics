"""The leather cast and props for the "andhe ka putra andha" myth-bust reel (videos/andhe_ka_putra.py), in the Togalu
Gombeyaata style of the earlier reels (puppet_cast, kaikeyi_cast, jayadratha_cast, arjuna_cast, shani_cast...): profile
figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor
and no film. Every sprite name starts with "ak_" (other builders' casts load in the same process).

Cast (one look each, kept the same through the video):
  DURYODHANA    the proud Kaurava prince: warm wheat skin, a black moustache, long hair, a tall gold kirita with a
                violet flare in front of a dark-red flame halo, a royal violet dhoti with a gold border, a red sash, a
                broad jewelled gold collar and a jewelled belt; his great gold mace (ak_gada). Faces: calm, proud,
                smile, angry, scold (complaining), shock (the fall: wide eyes, mouth open), shame (drenched, eyes
                down), envy (a narrowed, hard stare). Legs and dhoti hitched up to the knee for lifting his robe
                (ak_duryo_*_up).
  DRAUPADI      the queen, with dignity: dusky skin (she is Krishnaa), a deep rani-pink sari with a gold border and a
                darker pallu, a saffron-gold blouse, a small gold queen's crown, a long braid with jasmine, sindoor, a
                bindi, a nose ring, jhumkas, layered necklaces. Faces: open, smile, laugh.
  HER COMPANIONS puppet_cast's QUEEN1 / QUEEN2 with laughing faces (ak_lady*_head_laugh).
  BHIMA         puppet_cast.BHIMA's big body (bulk 1.38, cream dhoti, blue border) with a prince's gold kirita and a
                blue flare (ak_bhima_head, _laugh); his mace is puppet_cast's "mace".
  ARJUNA        jayadratha_cast.ARJUNA; laughing face ak_arjuna_head_laugh (arjuna_cast's face, his own kirita).
  NAKULA, SAHADEVA  the twins: fair skin, no moustache, small gold kiritas (green / saffron flares); Nakula a green
                dhoti and a saffron sash, Sahadeva a teal dhoti and a red sash. Faces: calm, laugh.
  SERVANTS      palace attendants: a cream cotton dhoti with a red border, a saffron sash, a wrapped turban (rust or
                teal), a moustache; one carries a chamara fly-whisk. Faces: calm, laugh.
  DHRITARASHTRA the old blind king: wheat skin, long white hair, a long white beard and moustache, his eyes always
                closed, a tall gold crown with a dark-red flare, a dark-red dhoti with a gold border; seated on the
                throne (mandhata_cast's md_throne) with ak_dhrita_seat legs.
Sets and props: Maya's crystal palace (crystal pillars, a cusped crystal arch with hanging drops, a crystal lattice
wall, a blue glass floor of tiles in perspective that shimmers like water, the pond's water, a splash), the quote card
(ak_qcard, big red quote marks), an old TV set (ak_tv, its screen at TV_SCREEN), a magnifying lens,
heaps of gold, an open chest of gems, a palace balcony (back and front rail),
green flames of envy. The palm-leaf book, plaque, speech cloud, thought bubble, throne, drops and the pot of gold
come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import jayadratha_cast as J  # noqa: F401  (registers Arjuna)
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import puppet_cast as C
import ravana_cast as R  # noqa: F401  (registers the drops)
import shani_cast as S
import six_cast_b as SB  # noqa: F401  (registers the coins and the pot of gold)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BLUE, BROWN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, SAFFRON, SKIN,
                         almond_eye, band, dots_in, ell, holes_line, ink, leather, perforate, poly, punch, register,
                         rivet, spath)

DU_SKIN = (0.93, 0.66, 0.42)          # Duryodhana
DU_DHOTI = (0.42, 0.15, 0.50)         # royal violet
DU_FLARE = (0.62, 0.30, 0.74)
DU_HALO = (0.46, 0.08, 0.10)
DR_SKIN = (0.82, 0.56, 0.38)          # Draupadi: dusky
DR_SARI = (0.80, 0.11, 0.34)          # deep rani pink
DR_PALLU = (0.54, 0.05, 0.22)
DR_CHOLI = (0.99, 0.66, 0.18)
BH_SKIN = (0.80, 0.52, 0.26)          # Bhima (puppet_cast.BHIMA)
TW_SKIN = (0.99, 0.80, 0.58)          # the twins
TEAL = (0.10, 0.50, 0.58)
SV_SKIN = (0.78, 0.50, 0.30)          # the servants
TURBAN_A = (0.86, 0.38, 0.12)
TURBAN_B = (0.16, 0.54, 0.60)
DH_SKIN = (0.94, 0.72, 0.52)          # Dhritarashtra
DH_DHOTI = (0.60, 0.12, 0.12)
WHITE = (0.95, 0.94, 0.90)
CRYSTAL = (0.80, 0.92, 1.0)           # Maya's palace
CRYSTAL2 = (0.56, 0.76, 0.96)
CRYSTAL3 = (0.40, 0.62, 0.90)
AQUA = (0.40, 0.70, 0.88)
AQUA2 = (0.22, 0.50, 0.74)
WOOD = K.WOOD
WOOD2 = (0.55, 0.32, 0.14)
LOTUS = (1.0, 0.62, 0.70)
LEAF = (0.30, 0.60, 0.32)
LIME = (0.72, 0.94, 0.34)

DU_B = 1.15                           # Duryodhana's bulk
DH_B = 1.2                            # Dhritarashtra's bulk
TV_SCREEN = (-232.0, -502.0, 344.0, 354.0)   # the TV's glass: x0, y0, w, h (TV units, pivot at the bottom centre)
FLOOR_W, FLOOR_D, FLOOR_VP = 780.0, 560.0, 1150.0   # the glass floor: half width at the back edge, depth, vanishing
FLOOR_ROWS, FLOOR_COLS = 7, 9                       # point above the back edge; tile rows and columns

# ------------------------------------------------------------------ faces

FACE = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152), (60, -128),
        (66, -116), (92, -92), (68, -82), (70, -72), (62, -64), (66, -56), (56, -44), (52, -30), (34, -22), (26, 6)]
FACE_OPEN = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
             (60, -128), (66, -116), (92, -92), (72, -84), (48, -74), (70, -52), (66, -40), (56, -28), (40, -16),
             (26, 6)]


def face2(cr, o, mood="calm"):
    """arjuna_cast.face, plus three more moods: shock (wide eyes, the mouth open), shut (eyes closed, calm), envy (a
    narrowed, hard stare and a tight mouth)."""
    if mood not in ("shock", "shut", "envy"):
        return A.face(cr, o, mood)
    skin = o["skin"]
    if o.get("hair", True):
        hp = [(-30, -176), (-62, -146), (-84, -80), (-88, 0), (-74, 64), (-50, 84), (-40, 30), (-36, -40), (-20, -90)]
        _shape(cr, hp, HAIR, 5)
        for k in range(4):
            holes_line(cr, [(-46 - 8 * k, -140 + 10 * k), (-70 - 4 * k, -40), (-62 - 2 * k, 50)], 16, 2.4)
    _shape(cr, FACE_OPEN if mood == "shock" else FACE, skin, 6)
    cr.new_path()
    ell(cr, -14, -108, 13, 21)
    leather(cr, skin, 4)
    if mood == "shock":
        _shape(cr, [(74, -84), (50, -76), (54, -60), (70, -54)], (0.42, 0.05, 0.06), 4)
        almond_eye(cr, 34, -120, 44, 17, col=PALE)
        ink(cr, [(10, -160), (34, -174), (60, -164)], 5)                         # brow shot up
        ink(cr, [(18, -184), (44, -186)], 2.5)
    elif mood == "shut":
        ink(cr, [(68, -70), (60, -68)], 3)
        ink(cr, [(16, -118), (34, -110), (52, -118)], 5)                         # the closed lid
        for k in range(3):
            ink(cr, [(24 + 10 * k, -112), (22 + 10 * k, -104)], 2.2)
        ink(cr, [(14, -140), (34, -148), (56, -140)], 4.5)
    else:                                                                         # envy
        ink(cr, [(72, -66), (58, -70), (52, -64)], 4)
        almond_eye(cr, 36, -116, 38, 11, col=PALE)
        ink(cr, [(14, -122), (36, -130), (58, -118)], 7)                         # the heavy lid
        ink(cr, [(6, -152), (34, -140), (64, -128)], 8)                          # brow pulled down hard
        ink(cr, [(4, -144), (-4, -128)], 3)
    if o.get("tilak", True):
        ink(cr, [(52, -150), (54, -170)], 5, col=RED)
    if o.get("moustache"):
        m = [(64, -74), (44, -82), (26, -86), (14, -102), (24, -94), (44, -86), (66, -79)]
        _shape(cr, m, o.get("tache_col", HAIR), 3)
    if o.get("earring", True):
        _jewel(cr, -12, -72, 16, GOLD)
        poly(cr, [(-20, -58), (-12, -36), (-4, -58)])
        leather(cr, RED, 3)


# ------------------------------------------------------------------ Duryodhana


_DU_O = dict(skin=DU_SKIN, hair=True, moustache=True, tilak=True)
DU_MOODS = ("calm", "proud", "smile", "angry", "scold", "hurt", "shock", "shame", "envy")


def duryo_crown(cr):
    """A tall gold kirita with a violet flare, an emerald and strings of pearls falling behind."""
    for k in range(2):
        for j in range(6):
            cr.new_path()
            cr.arc(-60 - 10 * k - 2 * j, -150 + 17 * j, 5, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    R.kirita(cr, GOLD, None, tall=1.3, flare=DU_FLARE)
    h = lambda y: -150 + (y + 150) * 1.3
    _jewel(cr, 2, h(-282), 10, (0.16, 0.66, 0.40))
    for sx in (-1, 1):                                                            # small side peaks
        _shape(cr, [(sx * 34, -170), (sx * 62, h(-226)), (sx * 48, h(-262)), (sx * 30, h(-224)), (sx * 16, -186)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))


def duryo_head(cr, mood="calm"):
    K._halo(cr, DU_HALO)
    face2(cr, _DU_O, mood)
    duryo_crown(cr)


def _du_jewels(cr, b=DU_B):
    """A broad jewelled gold collar and a gem belt over the body (body coordinates)."""
    band(cr, [(-34, -286), (8 * b, -238), (58 * b, -204)], 24, GOLD, spacing=12, hole_r=2.4)
    for i, u in enumerate((0.15, 0.4, 0.65, 0.9)):
        _jewel(cr, -34 + (92 * b) * u, -286 + 82 * u, 8, RED if i % 2 == 0 else (0.16, 0.66, 0.40))
    band(cr, [(-30, -276), (12 * b, -190), (52 * b, -142)], 9, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 54 * b, -130, 14, RED)
    band(cr, [(-62 * b, -40), (0, -52), (64 * b, -44)], 20, GOLD, spacing=12, hole_r=2.4)
    for x in (-34, 0, 34):
        _jewel(cr, x * b, -46, 8, RED)


_DU = dict(skin=DU_SKIN, bulk=DU_B, dhoti=DU_DHOTI, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD, crown="tiara",
           halo=False, moustache=True, hands=("fist", "fist"))
DURYO = man("ak_duryo", **_DU)


def _du_body(cr, up=False):
    if up:                                                    # the dhoti's front pleats held up to the knee
        cr.save()
        cr.rectangle(-400, -500, 800, 610)
        cr.clip()
        C.man_body(cr, _DU)
        cr.restore()
        b = DU_B
        pf = [(24 * b, 30), (62 * b, 26), (84 * b, 96), (76 * b, 112), (64 * b, 100), (52 * b, 114), (40 * b, 100),
              (28 * b, 112), (16 * b, 100)]
        _shape(cr, pf, GOLD, 5, smooth=False)
        for u in (0.3, 0.6):
            ink(cr, [(24 * b + 36 * b * u, 34), (22 * b + 50 * b * u, 100)], 3, smooth=False)
        rivet(cr, 16 * b, 6, 7)
    else:
        C.man_body(cr, _DU)
    _du_jewels(cr)


def _leg_up(cr, o):
    """puppet_cast.leg with the dhoti hitched up to the knee: the bare knee and shin show."""
    b = o.get("bulk", 1.0)
    _shape(cr, [(-28 * b, 70), (22 * b, 70), (20 * b, 204), (-26 * b, 204)], o["skin"], 5)
    shin = [(-24 * b, 196), (18 * b, 196), (16 * b, 300), (12 * b, 388), (-10 * b, 392), (-24 * b, 300)]
    _shape(cr, shin, o["skin"], 5)
    foot = [(-14, 382), (14, 380), (32, 396), (70, 410), (72, 424), (-16, 426)]
    _shape(cr, foot, o["skin"], 4)
    band(cr, [(-12 * b, 374), (14 * b, 374)], 9, GOLD, spacing=8, hole_r=2.0)
    dl = [(-42 * b, -10), (0, -26), (46 * b, -10), (56 * b, 50), (52 * b, 100), (30 * b, 116), (6, 106), (-22 * b, 120),
          (-44 * b, 104), (-52 * b, 50)]
    _shape(cr, dl, o["dhoti"], 5)
    dots_in(cr, lambda: spath(cr, dl), 19, 2.8)
    band(cr, [(-44 * b, 100), (0, 110), (50 * b, 100)], 14, o.get("border", GOLD), spacing=11, hole_r=2.4)
    for x in (-20, 4, 26):
        ink(cr, [(x * b, 10), (x * b + 4, 96)], 3)
    rivet(cr, 0, 0, 9)


register("ak_duryo_body", (-200, -330, 140, 300), lambda cr: _du_body(cr))
register("ak_duryo_body_up", (-200, -330, 140, 300), lambda cr: _du_body(cr, True))
register("ak_duryo_legF_up", (-70, -40, 90, 440), lambda cr: _leg_up(cr, _DU))
register("ak_duryo_legB_up", (-70, -40, 90, 440), lambda cr: _leg_up(cr, _DU))
for _m in DU_MOODS:
    register("ak_duryo_head" + ("" if _m == "calm" else "_" + _m), (-230, -500, 130, 110),
             (lambda m: lambda cr: duryo_head(cr, m))(_m))


def _gada(cr):
    """Duryodhana's great mace (grip at 0, 0, the head up): a ribbed gold head with violet bands and a spike, a red
    grip, a gold shaft with rings."""
    ink(cr, [(0, 70), (0, -250)], 22, smooth=False, col=INK)
    ink(cr, [(0, 70), (0, -250)], 13, smooth=False, col=GOLD)
    for y in (-30, -120, -210):
        band(cr, [(-14, y), (14, y)], 12, RED, holes=False)
    _shape(cr, [(-14, 30), (14, 30), (14, 80), (-14, 80)], RED, 4, smooth=False)
    cr.new_path()
    ell(cr, 0, 90, 22, 12)
    leather(cr, GOLD, 4)
    cr.new_path()
    ell(cr, 0, -340, 82, 100)
    pl = leather(cr, GOLD, 6, keep=True)
    for k in (-1, 0, 1):
        ink(cr, [(k * 56, -428), (k * 78, -340), (k * 56, -252)], 4)
    band(cr, [(-80, -340), (80, -340)], 18, DU_FLARE, spacing=12)
    band(cr, [(-62, -270), (62, -270)], 12, DU_FLARE, spacing=11, hole_r=2.2)
    for x, y in ((-40, -390), (40, -390), (0, -300)):
        _jewel(cr, x, y, 9, RED)
    _shape(cr, [(-12, -432), (0, -476), (12, -432)], GOLD, 4, smooth=False)
    _shape(cr, [(-60, -250), (60, -250), (36, -230), (-36, -230)], GOLD, 4, smooth=False)
    perforate(cr, pl, 10, 16, 2.6)


register("ak_gada", (-110, -490, 110, 110), _gada)

# ------------------------------------------------------------------ Draupadi and her companions


def draupadi_head(cr, mood="open"):
    """Draupadi: a long braid with jasmine, a bun, a small gold queen's crown, sindoor, a bindi, a nose ring and
    jhumkas."""
    for i in range(9):                                                            # the braid down her back
        u = i / 8
        x, y = -60 - 26 * u, -120 + 230 * u
        cr.new_path()
        ell(cr, x, y, 22 - 7 * u, 18 - 4 * u, 0.5 if i % 2 else -0.5)
        leather(cr, HAIR, 3.5)
        if i % 2 == 0:
            cr.new_path()
            cr.arc(x - 16 + 4 * u, y + 2, 5, 0, 2 * math.pi)
            leather(cr, PALE, 1.5)
    _shape(cr, [(-92, 106), (-76, 104), (-70, 136), (-84, 146), (-98, 134)], RED, 3)       # the tassel
    S._face_w(cr, DR_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -134, 34, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(10):                                                           # jasmine round the bun
        a = math.pi * (0.25 + 1.6 * i / 9)
        cr.new_path()
        cr.arc(-62 + 38 * math.cos(a), -134 + 38 * math.sin(a), 6, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    ink(cr, [(8, -188), (28, -178)], 4, col=RED)                                  # sindoor
    crown = [(-38, -168), (-34, -206), (-20, -194), (-10, -236), (0, -212), (10, -248), (20, -212), (30, -236),
             (40, -196), (46, -170)]
    _shape(cr, crown, GOLD, 4, smooth=False, holes=(6, 10, 2.0))
    _jewel(cr, 10, -206, 8, RED)
    for x in (-10, 30):
        _jewel(cr, x, -200, 5, (0.16, 0.66, 0.40))
    S._w_eyes(cr, DR_SKIN, mood)
    cr.new_path()
    cr.arc(46, -150, 5.5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()
    cr.arc(64, -90, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    _jewel(cr, -10, -70, 10, GOLD)
    _shape(cr, [(-26, -58), (-10, -66), (6, -58), (10, -34), (-30, -34)], GOLD, 3, smooth=False)
    for x in (-24, -10, 4):
        cr.new_path()
        cr.arc(x, -26, 4, 0, 2 * math.pi)
        leather(cr, PALE, 1.5)


def _dr_extra(cr):
    """Layered gold necklaces with a ruby pendant."""
    band(cr, [(-20, -282), (14, -226), (42, -184)], 9, GOLD, spacing=10, hole_r=1.8)
    band(cr, [(-28, -276), (6, -184), (32, -130)], 7, GOLD, spacing=10, hole_r=1.6)
    _jewel(cr, 34, -120, 11, RED)
    for x in (-26, -2, 22):
        _jewel(cr, x, -22, 6, GOLD)


DRAUPADI = woman("ak_draupadi", skin=DR_SKIN, skirt=DR_SARI, choli=DR_CHOLI, border=GOLD, pallu_col=DR_PALLU,
                 gem=GREEN, ornaments_extra=_dr_extra, hands=("open", "open"))
DR_MOODS = ("open", "smile", "laugh")
for _e in DR_MOODS:
    register("ak_draupadi_head" + ("" if _e == "open" else "_" + _e), (-160, -260, 100, 160),
             (lambda e: lambda cr: draupadi_head(cr, e))(_e))


def lady_head(cr, skin, flower, mood="laugh"):
    """A companion's head (puppet_cast.woman_head's look) with arjuna/shani-style moods."""
    S._face_w(cr, skin)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    _flower(cr, -62, -128, 14, flower)
    tp = [(-30, -172), (-20, -200), (-6, -184), (8, -212), (20, -184), (34, -204), (40, -170)]
    _shape(cr, tp, GOLD, 4, smooth=False)
    S._w_eyes(cr, skin, mood)
    cr.new_path()
    cr.arc(44, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _jewel(cr, -10, -70, 11, GOLD)
    poly(cr, [(-24, -58), (-10, -66), (4, -58), (8, -34), (-28, -34)])
    leather(cr, GOLD, 3)


register("ak_lady1_head_laugh", (-120, -240, 100, 30), lambda cr: lady_head(cr, SKIN, GOLD))
register("ak_lady2_head_laugh", (-120, -240, 100, 30), lambda cr: lady_head(cr, (0.99, 0.76, 0.56), PALE))

# ------------------------------------------------------------------ the Pandavas


_BH_O = dict(skin=BH_SKIN, hair=True, moustache=True, tilak=True)


def bhima_head(cr, mood="calm"):
    """Bhima as a prince: arjuna_cast's face, side whiskers, a gold kirita with a blue flare."""
    A.face(cr, _BH_O, mood)
    ink(cr, [(20, -70), (8, -60), (14, -46)], 5, col=HAIR)
    R.kirita(cr, GOLD, None, tall=1.05, flare=BLUE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.05, 9, RED)


for _m in ("calm", "laugh"):
    register("ak_bhima_head" + ("" if _m == "calm" else "_" + _m), (-200, -440, 120, 110),
             (lambda m: lambda cr: bhima_head(cr, m))(_m))
register("ak_arjuna_head_laugh", (-200, -440, 120, 110), lambda cr: A.arjuna_head(cr, "laugh"))

_TW_O = dict(skin=TW_SKIN, hair=True, moustache=False, tilak=True)


def twin_head(cr, mood, flare):
    A.face(cr, _TW_O, mood)
    R.kirita(cr, GOLD, None, tall=0.86, flare=flare)
    _jewel(cr, 2, -150 + (-282 + 150) * 0.86, 8, flare)


NAKULA = man("ak_nakula", skin=TW_SKIN, bulk=0.98, dhoti=GREEN, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
             crown="tiara", halo=False, thread=True, hands=("open", "fist"))
SAHADEVA = man("ak_sahadeva", skin=TW_SKIN, bulk=0.98, dhoti=TEAL, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
               crown="tiara", halo=False, thread=True, hands=("open", "fist"))
for _key, _fl in (("ak_nakula", GREEN), ("ak_sahadeva", SAFFRON)):
    for _m in ("calm", "laugh"):
        register(_key + "_head" + ("" if _m == "calm" else "_" + _m), (-200, -420, 120, 110),
                 (lambda m, f: lambda cr: twin_head(cr, m, f))(_m, _fl))

# ------------------------------------------------------------------ the servants


_SV_O = dict(skin=SV_SKIN, hair=False, moustache=True, tilak=False, earring=True)


def servant_head(cr, mood="calm", col=TURBAN_A):
    """A palace attendant: a wrapped turban with a gold band and a tail, a moustache."""
    A.face(cr, _SV_O, mood)
    _shape(cr, [(-56, -160), (-92, -146), (-104, -104), (-84, -112), (-62, -140)], col, 4)
    tb = [(-56, -134), (-62, -172), (-46, -206), (-8, -222), (32, -214), (54, -186), (58, -148), (30, -152), (0, -148),
          (-30, -142)]
    _shape(cr, tb, col, 5)
    for k, dy in enumerate((0, 24, 48)):
        ink(cr, [(-50, -156 - dy), (0, -170 - dy - 6 * k), (52, -162 - dy)], 3)
    band(cr, [(-58, -144), (58, -150)], 12, GOLD, spacing=11, hole_r=2.2)
    _jewel(cr, 28, -196, 8, RED)


SERVANT = man("ak_servant", skin=SV_SKIN, bulk=0.95, dhoti=PALE, border=RED, pleat=RED, sash=SAFFRON, neck=BROWN,
              crown="tiara", halo=False, hair=False, moustache=True, hands=("open", "fist"))
for _m in ("calm", "laugh"):
    register("ak_servant_head" + ("" if _m == "calm" else "_" + _m), (-130, -250, 110, 40),
             (lambda m: lambda cr: servant_head(cr, m, TURBAN_A))(_m))
    register("ak_servantB_head" + ("" if _m == "calm" else "_" + _m), (-130, -250, 110, 40),
             (lambda m: lambda cr: servant_head(cr, m, TURBAN_B))(_m))


def _chamara(cr):
    """A fly-whisk (grip at 0, 0): a gold handle and a white plume."""
    ink(cr, [(0, 60), (0, -160)], 16, smooth=False)
    ink(cr, [(0, 60), (0, -160)], 9, smooth=False, col=GOLD)
    plume = [(0, -150), (-40, -200), (-58, -280), (-40, -360), (0, -390), (40, -360), (58, -280), (40, -200)]
    _shape(cr, plume, WHITE, 4)
    for x in (-26, 0, 26):
        ink(cr, [(x * 0.4, -170), (x, -280), (x * 0.6, -370)], 2.5, col=(0.70, 0.66, 0.60))
    band(cr, [(-18, -156), (18, -156)], 14, RED, holes=False)


register("ak_chamara", (-70, -400, 70, 70), _chamara)

# ------------------------------------------------------------------ Dhritarashtra


_DH_O = dict(skin=DH_SKIN, hair=False, moustache=False, tilak=True, earring=True)


def dhrita_head(cr):
    """The old blind king: long white hair, a long white beard and moustache, his eyes closed, a tall gold crown."""
    hp = [(-30, -176), (-62, -146), (-84, -80), (-90, 10), (-78, 80), (-52, 96), (-40, 30), (-36, -40), (-20, -90)]
    _shape(cr, hp, WHITE, 5)
    for k in range(4):
        holes_line(cr, [(-46 - 8 * k, -140 + 10 * k), (-70 - 4 * k, -40), (-64 - 2 * k, 60)], 16, 2.4)
    face2(cr, _DH_O, "shut")
    ink(cr, [(6, -104), (-4, -94)], 2.5)                                          # lines of age
    ink(cr, [(14, -166), (42, -170)], 2.2)
    bp = [(60, -50), (64, -20), (58, 50), (42, 140), (22, 90), (2, 30), (6, -40), (28, -54)]
    _shape(cr, bp, WHITE, 4)
    for k in range(3):
        ink(cr, [(46 - 10 * k, -40), (40 - 12 * k, 30), (34 - 10 * k, 100)], 2.5, col=(0.62, 0.60, 0.56))
    m = [(66, -72), (44, -82), (26, -86), (14, -100), (24, -94), (44, -88), (70, -80)]
    _shape(cr, m, WHITE, 3)
    R.kirita(cr, GOLD, None, tall=1.15, flare=DRED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.15, 9, BLUE)


DHRITA = man("ak_dhrita", skin=DH_SKIN, bulk=DH_B, dhoti=DH_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
             crown="tiara", halo=False, thread=True, hands=("open", "open"))
register("ak_dhrita_head", (-200, -460, 120, 170), dhrita_head)
register("ak_dhrita_seat", (-100, -60, 340, 290), lambda cr: M.seat_legs(cr, DH_SKIN, DH_DHOTI, GOLD, DH_B))

# ------------------------------------------------------------------ the quote card, the TV, the lens


def _quote_mark(cr, x, y, s, col=RED):
    """A big quote mark: two commas (a round head and a curved tail)."""
    for dx in (0, 70 * s):
        cr.new_path()
        cr.arc(x + dx, y, 28 * s, 0, 2 * math.pi)
        leather(cr, col, 4)
        _shape(cr, [(x + dx + 26 * s, y + 2 * s), (x + dx + 20 * s, y + 46 * s), (x + dx - 12 * s, y + 78 * s),
                    (x + dx + 2 * s, y + 40 * s), (x + dx - 8 * s, y + 18 * s)], col, 4)
        punch(cr, [(x + dx - 8 * s, y - 8 * s)], 5 * s)


def _qcard(cr):
    """The quote card: a wide parchment board with a perforated border, a ruled inner frame, red flowers at the
    corners and big red quote marks (the quote itself is drawn over it per frame)."""
    pts = [(-470, -150), (-420, -190), (420, -190), (470, -150), (470, 150), (420, 190), (-420, 190), (-470, 150)]
    _shape(cr, pts, PARCH, 8, smooth=False, holes=(16, 17, 3.6))
    cr.new_path()
    poly(cr, [(-430, -150), (430, -150), (430, 150), (-430, 150)])
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    for sx in (-1, 1):
        for y in (-150, 150):
            _flower(cr, sx * 430, y, 24, RED, 8)
    cr.save()                                          # the opening marks (66) top left, the closing ones (99) below
    cr.translate(-346, -92)
    cr.rotate(math.pi)
    _quote_mark(cr, 0, 0, 0.8)
    cr.restore()
    _quote_mark(cr, 346, 84, 0.8)


register("ak_qcard", (-490, -210, 490, 210), _qcard)


def _rrect(cr, x0, y0, x1, y1, r):
    cr.new_path()
    cr.arc(x1 - r, y0 + r, r, -math.pi / 2, 0)
    cr.arc(x1 - r, y1 - r, r, 0, math.pi / 2)
    cr.arc(x0 + r, y1 - r, r, math.pi / 2, math.pi)
    cr.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def _tv(cr):
    """An old television set (pivot at the bottom centre): splayed wooden legs, a wooden cabinet, the rounded glass,
    two knobs and a speaker grille, rabbit-ear antennas."""
    for sx in (-1, 1):
        ink(cr, [(sx * 190, -100), (sx * 236, 0)], 26, smooth=False)
        ink(cr, [(sx * 190, -100), (sx * 236, 0)], 15, smooth=False, col=WOOD2)
    for ex, ey in ((-190, -790), (130, -800)):
        ink(cr, [(-30, -560), (ex, ey)], 9, smooth=False)
        ink(cr, [(-30, -560), (ex, ey)], 4, smooth=False, col=(0.78, 0.78, 0.84))
        cr.new_path()
        cr.arc(ex, ey, 14, 0, 2 * math.pi)
        leather(cr, (0.78, 0.78, 0.84), 3)
    cr.new_path()
    ell(cr, -30, -560, 44, 22)
    leather(cr, (0.40, 0.40, 0.46), 4)
    _rrect(cr, -300, -560, 300, -90, 46)
    pl = leather(cr, WOOD2, 8, keep=True)
    perforate(cr, pl, 14, 18, 3.2)
    _rrect(cr, -256, -526, 136, -124, 40)
    leather(cr, (0.20, 0.18, 0.18), 5)
    x0, y0, w, h = TV_SCREEN
    _rrect(cr, x0, y0, x0 + w, y0 + h, 34)
    leather(cr, (0.62, 0.70, 0.68), 3)
    for y, r in ((-450, 32), (-354, 26)):
        cr.new_path()
        cr.arc(212, y, r, 0, 2 * math.pi)
        leather(cr, GOLD, 4)
        ink(cr, [(212, y - r + 6), (212, y - 4)], 4, smooth=False)
    cr.save()
    _rrect(cr, 166, -296, 262, -142, 12)
    pl = leather(cr, (0.36, 0.22, 0.10), 4, keep=True)
    cr.restore()
    for i in range(6):
        for j in range(4):
            punch(cr, [(180 + 22 * j, -280 + 24 * i)], 4)
    band(cr, [(-280, -112), (280, -112)], 12, GOLD, spacing=14, hole_r=2.2)


register("ak_tv", (-320, -820, 320, 14), _tv)


def _lens(cr):
    """A magnifying lens (pivot at the glass centre): a gold rim, a pale glass with glints, a wooden handle."""
    cr.save()
    cr.rotate(-math.pi / 4)                            # the handle down to the lower right
    _shape(cr, [(-22, 118), (22, 118), (26, 330), (0, 350), (-26, 330)], WOOD2, 5)
    band(cr, [(-24, 136), (24, 136)], 22, GOLD, spacing=10, hole_r=2.2)
    cr.restore()
    cr.new_path()
    cr.arc(0, 0, 118, 0, 2 * math.pi)
    leather(cr, (0.90, 0.96, 1.0), 0)
    cr.new_path()
    cr.arc(0, 0, 118, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(34)
    cr.stroke()
    cr.new_path()
    cr.arc(0, 0, 118, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(22)
    cr.stroke()
    punch(cr, [(118 * math.cos(2 * math.pi * i / 24), 118 * math.sin(2 * math.pi * i / 24)) for i in range(24)], 3)
    cr.save()
    cr.set_operator(0)
    cr.set_line_width(12)
    cr.set_line_cap(1)
    cr.arc(0, 0, 80, math.pi * 1.1, math.pi * 1.45)
    cr.stroke()
    cr.restore()
    punch(cr, [(-30, -70)], 7)


register("ak_lens", (-160, -160, 280, 280), _lens)


# ------------------------------------------------------------------ Maya's crystal palace


def _pillar(cr):
    """A crystal pillar (pivot at the bottom centre): a gold base, a faceted pale-blue shaft with punched diamonds, gold
    bands, a lotus capital."""
    _shape(cr, [(-92, 0), (92, 0), (82, -30), (64, -62), (-64, -62), (-82, -30)], GOLD, 5, smooth=False,
           holes=(8, 13, 2.4))
    shaft = [(-54, -60), (54, -60), (48, -880), (-48, -880)]
    _shape(cr, shaft, CRYSTAL, 5, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-40, -80), (40, -80), (36, -860), (-36, -860)]), 30, 4.2, shape="d")
    for x in (-24, 0, 24):
        ink(cr, [(x, -70), (x * 0.9, -870)], 3, smooth=False, col=CRYSTAL3)
    for y in (-300, -600):
        band(cr, [(-54, y), (54, y)], 18, GOLD, spacing=11, hole_r=2.2)
    cap = [(-56, -878), (56, -878), (96, -930), (70, -962), (-70, -962), (-96, -930)]
    _shape(cr, cap, GOLD, 5, smooth=False, holes=(8, 12, 2.2))
    for k in range(-2, 3):
        _shape(cr, [(k * 34 - 16, -900), (k * 34, -950), (k * 34 + 16, -900)], CRYSTAL2, 3)
    _shape(cr, [(-104, -960), (104, -960), (104, -994), (-104, -994)], CRYSTAL2, 5, smooth=False)
    _jewel(cr, 0, -977, 10, BLUE)


register("ak_pillar", (-115, -1005, 115, 10), _pillar)


def _arch(cr):
    """A cusped crystal arch hung under a gold beam (pivot at the beam's middle), crystal drops hanging from it."""
    lobes = 7
    edge = []
    for i in range(lobes * 12 + 1):
        u = i / (lobes * 12)
        x = -500 + 1000 * u
        base = 60 + 150 * math.sin(math.pi * u)
        cusp = 22 * abs(math.sin(math.pi * lobes * u))
        edge.append((x, base - cusp))
    fill = [(-540, -40), (540, -40)] + list(reversed(edge))
    cr.new_path()
    poly(cr, fill)
    pl = leather(cr, CRYSTAL, 6, keep=True)
    perforate(cr, pl, 12, 16, 2.8)
    dots_in(cr, lambda: poly(cr, [(-420, 0), (420, 0)] + [(x, y - 40) for x, y in reversed(edge[12:-12])]), 34, 4,
            shape="d")
    _shape(cr, [(-570, -110), (570, -110), (570, -40), (-570, -40)], GOLD, 6, smooth=False, holes=(10, 16, 3))
    for k in range(-5, 6):
        _jewel(cr, k * 100, -75, 9 if k % 2 else 12, RED if k % 2 else BLUE)
        _shape(cr, [(k * 100 - 18, -110), (k * 100, -150), (k * 100 + 18, -110)], CRYSTAL2, 3)
    for i in range(1, lobes):
        x, y = edge[i * 12]
        ink(cr, [(x, y), (x, y + 50)], 2.5, smooth=False)
        _shape(cr, [(x, y + 46), (x + 12, y + 70), (x, y + 96), (x - 12, y + 70)], CRYSTAL2, 3, smooth=False)


register("ak_arch", (-590, -160, 590, 300), _arch)


def _jali(cr):
    """The palace's back wall: crystal lattice panels (pivot at the bottom centre)."""
    for k in range(-3, 3):
        x0 = k * 180 + 10
        pts = [(x0, 0), (x0 + 160, 0), (x0 + 160, -560), (x0 + 80, -640), (x0, -560)]
        _shape(cr, pts, CRYSTAL, 5, smooth=False)
        dots_in(cr, lambda x0=x0: poly(cr, [(x0 + 14, -14), (x0 + 146, -14), (x0 + 146, -550), (x0 + 80, -616),
                                             (x0 + 14, -550)]), 22, 5, shape="d")
        band(cr, [(x0 + 4, -300), (x0 + 156, -300)], 12, GOLD, spacing=12, hole_r=2.2)


register("ak_jali", (-560, -660, 560, 10), _jali)


def floor_xy(u, v):
    """A point on the glass floor (floor units: the back edge at y = 0): u in -1..1 across the back edge, v in 0..1
    from the back edge to the front."""
    y = FLOOR_D * v
    k = (FLOOR_VP + y) / FLOOR_VP
    return FLOOR_W * u * k, y


def floor_v(i):
    """Row line i of FLOOR_ROWS (0 = back edge): rows get deeper toward the front."""
    return (i / FLOOR_ROWS) ** 1.25


def _floor(cr):
    """The glass floor in perspective (pivot at the middle of its back edge): blue crystal tiles in two shades with
    gold seams, pale ripple lines in them (it looks like water), glints."""
    cols = FLOOR_COLS
    for i in range(FLOOR_ROWS):
        v0, v1 = floor_v(i), floor_v(i + 1)
        for j in range(-cols, cols):
            u0, u1 = j / cols, (j + 1) / cols
            pts = [floor_xy(u0 * 1.6, v0), floor_xy(u1 * 1.6, v0), floor_xy(u1 * 1.6, v1), floor_xy(u0 * 1.6, v1)]
            cr.new_path()
            poly(cr, pts)
            cr.set_source_rgb(*(CRYSTAL if (i + j) % 2 == 0 else CRYSTAL2))
            cr.fill()
            cx = sum(p[0] for p in pts) / 4
            cy = sum(p[1] for p in pts) / 4
            wd = abs(pts[1][0] - pts[0][0])
            hh = pts[2][1] - pts[0][1]
            for k in (-1, 1):                                                     # ripple lines
                yy = cy + k * hh * 0.22
                ink(cr, [(cx - wd * 0.32, yy), (cx - wd * 0.12, yy - hh * 0.06), (cx + wd * 0.08, yy),
                         (cx + wd * 0.28, yy - hh * 0.06)], 2.2, col=(0.92, 0.98, 1.0))
            if (i * 7 + j * 3) % 5 == 0:
                punch(cr, [(cx + wd * 0.18, cy - hh * 0.2)], 3.5)
    for i in range(FLOOR_ROWS + 1):
        v = floor_v(i)
        a, b = floor_xy(-1.6, v), floor_xy(1.6, v)
        ink(cr, [a, b], 5 if i == 0 else 3.5, smooth=False, col=GOLD)
        ink(cr, [a, b], 1.4, smooth=False, col=INK)
    for j in range(-cols, cols + 1):
        a, b = floor_xy(1.6 * j / cols, 0), floor_xy(1.6 * j / cols, 1)
        ink(cr, [a, b], 3.5, smooth=False, col=GOLD)
        ink(cr, [a, b], 1.4, smooth=False, col=INK)


register("ak_floor", (-1300, -10, 1300, FLOOR_D + 10), _floor, tex=0.6)


def _water(cr):
    """The pond's real water (pivot at its middle; the scene clips it to the pond): deep blue-green with ripple bands,
    punched glints and lotus leaves at the edge."""
    cr.new_path()
    poly(cr, [(-420, -150), (420, -150), (420, 150), (-420, 150)])
    cr.set_source_rgb(*AQUA)
    cr.fill()
    for k in range(-5, 6):
        y = k * 26
        pts = [(x, y + 7 * math.sin(x / 38.0 + k)) for x in range(-420, 421, 20)]
        ink(cr, pts, 3, col=AQUA2 if k % 2 else (0.80, 0.94, 1.0))
    for i in range(18):
        punch(cr, [(-380 + 45 * i, -120 + 230 * ((i * 0.618) % 1.0))], 3.2)
    for x, y, r in ((-300, 70, 48), (-230, 110, 34), (290, 80, 44), (330, -40, 30)):
        cr.new_path()
        ell(cr, x, y, r, r * 0.42)
        leather(cr, LEAF, 4)
        ink(cr, [(x, y), (x + r * 0.8, y - r * 0.2)], 3)
    _shape(cr, [(-270, 40), (-282, 6), (-266, -20), (-254, 6), (-240, -24), (-226, 6), (-238, 40)], LOTUS, 3)


register("ak_water", (-430, -160, 430, 160), _water, tex=0.6)


def _splash(cr):
    """A crown of water thrown up (pivot at the water line's middle)."""
    pts = [(-250, 0)]
    n = 9
    for i in range(n):
        x = -230 + 460 * (i + 0.5) / n
        h = 230 + 150 * math.sin(i * 2.1 + 0.7) ** 2
        pts += [(x - 22, -h * 0.4), (x - 4 + 10 * math.sin(i), -h), (x + 18, -h * 0.45)]
    pts += [(250, 0)]
    _shape(cr, pts, AQUA, 5)
    _shape(cr, [(x * 0.7, y * 0.7) for x, y in pts], (0.66, 0.86, 1.0), 0)
    _shape(cr, [(x * 0.4, y * 0.4) for x, y in pts], (0.92, 0.98, 1.0), 0)
    for i in range(10):
        punch(cr, [(-200 + 44 * i, -60 - 70 * ((i * 0.618) % 1.0))], 5)


register("ak_splash", (-270, -420, 270, 14), _splash, tex=0.5)

# ------------------------------------------------------------------ wealth and glory


def _heap(cr):
    """A heap of gold coins (pivot at the bottom centre) with gems scattered in it."""
    rows = 7
    for r in range(rows):
        n = 9 - r
        y = -26 - 38 * r
        for i in range(n):
            x = (i - (n - 1) / 2) * 62 + (18 if r % 2 else 0) * ((i % 3) - 1)
            cr.new_path()
            ell(cr, x, y, 36, 16)
            leather(cr, GOLD if (i + r) % 3 else OCHRE, 3.5)
            punch(cr, [(x, y)], 3)
    for x, y, col in ((-150, -60, RED), (90, -100, (0.16, 0.66, 0.40)), (-40, -150, BLUE), (120, -40, RED),
                      (10, -230, RED), (-110, -170, (0.16, 0.66, 0.40))):
        _jewel(cr, x, y, 14, col)


register("ak_heap", (-320, -300, 320, 20), _heap)


def _chest(cr):
    """An open treasure chest (pivot at the bottom centre): the lid thrown back, gems, pearls and necklaces heaped
    and spilling."""
    lid = [(-210, -170), (210, -170), (190, -330), (-190, -330)]
    _shape(cr, lid, WOOD2, 6, smooth=False)
    band(cr, [(-200, -250), (200, -250)], 16, GOLD, spacing=12)
    for x in (-120, 0, 120):
        _jewel(cr, x, -300, 9, RED)
    for i in range(14):
        x = -170 + 340 * ((i * 0.618) % 1.0)
        y = -180 - 50 * math.sin(math.pi * (x + 170) / 340) + 8 * (i % 3)
        _jewel(cr, x, y, 16 + 4 * (i % 2), (RED, (0.16, 0.66, 0.40), BLUE, GOLD)[i % 4])
    for k in range(2):
        pts = [(-120 + 240 * u, -150 + 70 * k + 40 * math.sin(math.pi * u)) for u in (i / 10 for i in range(11))]
        for x, y in pts:
            cr.new_path()
            cr.arc(x, y, 7, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    box = [(-220, 0), (220, 0), (230, -170), (-230, -170)]
    _shape(cr, box, WOOD2, 6, smooth=False, holes=(12, 16, 3))
    for x in (-150, 150):
        band(cr, [(x, -4), (x, -166)], 22, GOLD, spacing=12)
    band(cr, [(-226, -150), (226, -150)], 16, GOLD, spacing=12)
    _shape(cr, [(-26, -110), (26, -110), (26, -60), (-26, -60)], GOLD, 4, smooth=False)
    punch(cr, [(0, -86)], 6)
    for x, y in ((250, -10), (280, -24), (-260, -12)):
        cr.new_path()
        ell(cr, x, y, 26, 11)
        leather(cr, GOLD, 3)


register("ak_chest", (-300, -350, 300, 20), _chest)


def _gflame(cr, ph):
    """A green flame of envy (pivot at its base): soft curling tongues, the middle one tallest, three greens."""
    for layer, (col, sc) in enumerate((((0.10, 0.42, 0.16), 1.0), ((0.36, 0.74, 0.22), 0.74), (LIME, 0.48))):
        pts = [(-120 * sc, 0), (-128 * sc, -60 * sc)]
        n = 5
        for i in range(n):
            x = -110 * sc + 220 * sc * (i + 0.5) / n
            h = (190 + 70 * math.sin(i * 1.9 + ph * 2.3)) * sc * (1.25 - 0.3 * abs(i - 2))
            lean = 26 * sc * math.sin(i * 1.3 + ph)
            pts += [(x - 22 * sc, -h * 0.42), (x - 6 * sc + lean * 0.5, -h * 0.8), (x + lean, -h),
                    (x + 14 * sc, -h * 0.62), (x + 22 * sc, -h * 0.38)]
        pts += [(128 * sc, -60 * sc), (120 * sc, 0), (0, 24 * sc)]
        _shape(cr, pts, col, 4 if layer == 0 else 0)


for _i in range(3):
    register(f"ak_gflame{_i}", (-150, -400, 150, 8), (lambda ph: lambda cr: _gflame(cr, ph))(_i), tex=0.5)

# ------------------------------------------------------------------ the balcony


def _balc_back(cr):
    """A palace balcony's back (pivot at the balcony floor's middle): a curved bangla roof with a gold finial and
    scallops, slim pillars, a lattice wall behind."""
    _shape(cr, [(-250, 0), (250, 0), (250, -560), (-250, -560)], (0.96, 0.80, 0.56), 5, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-230, -20), (230, -20), (230, -540), (-230, -540)]), 30, 4.5, shape="d")
    for sx in (-1, 1):
        _shape(cr, [(sx * 300 - 22, 0), (sx * 300 + 22, 0), (sx * 300 + 18, -600), (sx * 300 - 18, -600)], OCHRE, 5,
               smooth=False, holes=(7, 13, 2.2))
        band(cr, [(sx * 300 - 20, -300), (sx * 300 + 20, -300)], 12, RED, holes=False)
    roof = [(-360, -600), (-300, -660), (-150, -700), (0, -712), (150, -700), (300, -660), (360, -600),
            (330, -580), (0, -620), (-330, -580)]
    _shape(cr, roof, RED, 6, holes=(10, 14, 2.6))
    band(cr, [(-350, -600), (0, -640), (350, -600)], 16, GOLD, spacing=12)
    for i in range(12):
        x = -330 + 660 * (i + 0.5) / 12
        y = -598 - 30 * math.sin(math.pi * (i + 0.5) / 12)
        cr.new_path()
        cr.arc(x, y + 8, 22, 0, math.pi)
        leather(cr, GOLD, 3)
    _shape(cr, [(-16, -708), (0, -770), (16, -708)], GOLD, 4, smooth=False)
    cr.new_path()
    cr.arc(0, -716, 14, 0, 2 * math.pi)
    leather(cr, GOLD, 3)


def _balc_rail(cr):
    """The balcony's front (pivot at the balcony floor's middle): a jali railing, a carved ledge, brackets below."""
    rail = [(-340, -230), (340, -230), (340, 30), (-340, 30)]
    _shape(cr, rail, OCHRE, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-320, -200), (320, -200), (320, -10), (-320, -10)]), 26, 6, shape="d")
    band(cr, [(-350, -232), (350, -232)], 22, GOLD, spacing=12)
    band(cr, [(-350, 28), (350, 28)], 18, RED, spacing=12)
    for x in range(-320, 321, 128):
        _shape(cr, [(x - 14, -224), (x + 14, -224), (x + 14, 24), (x - 14, 24)], GOLD, 4, smooth=False)
    for sx in (-1, 1):
        for x0 in (220, 60):
            _shape(cr, [(sx * x0 - 26, 36), (sx * x0 + 26, 36), (sx * x0 + 12, 170), (sx * x0 - 12, 170)], OCHRE, 5,
                   smooth=False)
            cr.new_path()
            cr.arc(sx * x0, 176, 14, 0, 2 * math.pi)
            leather(cr, GOLD, 3)


register("ak_balc_back", (-380, -790, 380, 10), _balc_back)
register("ak_balc_rail", (-360, -250, 360, 200), _balc_rail)
