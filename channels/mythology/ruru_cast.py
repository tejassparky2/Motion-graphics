"""The leather cast and props for the Ruru reel (videos/ruru.py), in the Togalu Gombeyaata style of the Jarasandha,
Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha and Arjuna reels (puppet_cast, kaikeyi_cast, lrekha_cast, mandhata_cast,
jayadratha_cast, arjuna_cast): profile figures with big almond eyes, perforated garments and jointed limbs. Traditional
leather puppets, modelled on no actor and no film.

Cast (one look each, kept the same through the video):
  RURU        the young son of the sage Pramati: warm skin, no moustache, his hair in a top-knot tied with rudraksha
              beads, three ash lines on the forehead, a rudraksha mala and the sacred thread on a bare chest, a simple
              ochre dhoti with a thin dark-red border. Faces: calm, smile, weep (eyes shut, a tear streak), angry,
              shock. Kneels (rr_ruru_kneel). His wooden staff is ravana_cast's rv_staff.
  PRAMADVARA  the young bride: a rose-pink sari with a deep-pink pallu and a teal blouse (Sita in lrekha_cast wears leaf
              green), jasmine round her hair bun with red, pink and gold flowers in it, a small gold maang-tikka, a
              bindi, gold studs. Faces: open, shut (lying still / asleep), smile.
  MESSENGER   a messenger of the gods: pale gold skin, a ring of pale rays behind a small gold crown, two feathered
              wings, a sky-blue dhoti and a cream scarf; floats on a small cloud of light.
  YAMA        Yama Dharmaraja: dark blue-grey skin, a tall gold crown with side peaks and a red flare in front of a
              dark-red flame halo, a curled moustache, a red dhoti with a gold border; his danda (a tall staff with gold
              bands and a gold head). Calm and dignified, nothing frightening.
  OLD SNAKE   the harmless old Dundubha: big, plain grey-green with a pale belly, a round friendly eye, white brows,
              wrinkles at the neck, a gentle smile; mouth closed or open (speaking). Its body is drawn per frame in the
              scenes (a tapered leather strip along a spine); only the heads are sprites.
  BITE SNAKE  the snake in the grass: dark brown with cream bands, a small yellow eye with a slit pupil; closed or
              open (the strike: pink mouth, a forked tongue; no wound is ever shown).
  RISHI       the sage the old snake turns back into: pale skin, long white hair and a long white beard, white matted
              hair piled up with rudraksha, ash lines, a cream dhoti and a light-orange robe. Faces: calm, laugh,
              smile.
  KHAGAMA     his friend: darker tan skin, dark matted hair piled up (jata), a short dark beard, ash lines, a saffron
              dhoti, bare chest with a rudraksha mala; sits cross-legged by a small fire. Faces: sleep (eyes shut in
              meditation), shock, angry.
Props: the LIFE BAR (a leather cartouche with a red heart and ten punched windows the lamp light glows through; the
scenes light or darken each window), the bride's foot in close-up (sari hem, silver anklet with bells, alta-red sole,
a toe ring), tall grass clumps, the wedding mandap (posts, a red-and-gold canopy, banana plants, marigold strings, a
mango-leaf toran), a cloud of light, the messenger's wings, Yama's danda, the grass toy snake, a tear, small flowers.
The palm-leaf book, speech cloud, torn note, plaque, card, mat, garland, altar, flames and trees come from the earlier
casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math
import random

import arjuna_cast as A
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book boards and leaves, the speech cloud)
import mandhata_cast as M
import ravana_cast as R
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, ROSE, SAFFRON, band, cut,
                         dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet, spath)

RU_SKIN = (0.95, 0.70, 0.46)          # Ruru
RU_CLOTH = (0.93, 0.60, 0.22)         # his ochre dhoti
RU_CLOTH2 = (0.99, 0.78, 0.42)        # its lighter pleats
RU_SASH = (0.86, 0.48, 0.16)
PR_SKIN = (0.99, 0.78, 0.60)          # Pramadvara
PR_SARI = (0.96, 0.47, 0.60)          # rose pink
PR_PALLU = (0.84, 0.22, 0.42)         # deep pink
PR_CHOLI = (0.18, 0.56, 0.62)         # teal
DU_SKIN = (1.0, 0.91, 0.74)           # the messenger: pale gold
DU_CLOTH = (0.62, 0.82, 1.0)          # sky blue
DU_SCARF = (1.0, 0.97, 0.88)
DU_RAY = (1.0, 0.95, 0.78)
WING = (1.0, 0.97, 0.86)
WING2 = (1.0, 0.86, 0.56)
YM_SKIN = (0.30, 0.40, 0.54)          # Yama: dark blue-grey
YM_DHOTI = (0.82, 0.15, 0.10)
RS_SKIN = R.SAGE_SKIN                 # the rishi
ASH = R.ASH
KG_SKIN = (0.82, 0.54, 0.32)          # Khagama
JATA = (0.45, 0.28, 0.14)
SN_OLD = (0.55, 0.66, 0.48)           # the old snake: grey-green
SN_OLD_B = (0.88, 0.90, 0.70)         # its belly
SN_BITE = (0.38, 0.27, 0.14)          # the snake in the grass: dark brown
SN_BITE_B = (0.94, 0.82, 0.50)        # its belly and bands
TEAR = M.TEAR
SILVER = (0.90, 0.93, 1.0)
ALTA = (0.86, 0.12, 0.10)
STRAW = (0.88, 0.74, 0.38)
STRAW2 = (0.66, 0.50, 0.20)
BANANA = (0.42, 0.72, 0.28)
WOOD = K.WOOD

BAR_CELL0, BAR_STEP, BAR_CW, BAR_CH = -267.0, 72.0, 66.0, 80.0   # life-bar windows: first centre, step, size
BAR_SEAM = BAR_CELL0 + 4.5 * BAR_STEP                             # between window 5 and 6 (design x)
SEAT_H = 96.0                         # Khagama cross-legged: hip above the ground (as jayadratha_cast.SEAT_H)
HEAD_W = 100.0                        # a snake head's neck width (design units), the body's width there


# ------------------------------------------------------------------ faces


def _cover(cr, skin, x, y, rx, ry):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    cr.set_source_rgb(*skin)
    cr.fill()


def rface(cr, o, mood="calm"):
    """arjuna_cast.face with a few more moods: weep (eyes shut and cast down, a tear streak), sleep (eyes shut,
    peaceful), shock (a wide eye, raised brow, an open mouth), teach (a calm, warm look)."""
    base = {"weep": "shame", "sleep": "calm", "shock": "calm", "teach": "smile"}.get(mood, mood)
    A.face(cr, o, base)
    skin = o["skin"]
    if mood == "sleep":
        M._sleep_eye(cr, skin)
    elif mood == "weep":
        for k, (x0, y0) in enumerate(((36, -100), (44, -96))):
            ink(cr, [(x0, y0), (x0 + 4, y0 + 24), (x0 + 2, y0 + 44)], 5 - k, col=TEAR)
    elif mood == "shock":
        _cover(cr, skin, 34, -118, 27, 16)
        _cover(cr, skin, 34, -141, 25, 8)
        almond_eye_big(cr)
        ink(cr, [(10, -160), (34, -172), (58, -162)], 5)
        cr.new_path()
        ell(cr, 64, -68, 7, 10)
        leather(cr, (0.35, 0.05, 0.06), 2.5)


def almond_eye_big(cr):
    from puppet_core import almond_eye
    almond_eye(cr, 34, -118, 44, 19, col=PALE)


# ------------------------------------------------------------------ Ruru


_RU_O = dict(skin=RU_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def ruru_head(cr, mood="calm"):
    """Ruru: a hair cap and a top-knot tied with rudraksha beads, three ash lines, a rudraksha stud."""
    rface(cr, _RU_O, mood)
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -186), (24, -188), (-8, -182),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, HAIR, 4)
    holes_line(cr, [(-50, -130), (-40, -176), (0, -200)], 15, 2.4)
    cr.new_path()
    ell(cr, -12, -228, 38, 28, -0.15)
    leather(cr, HAIR, 4)
    holes_line(cr, [(-40, -230), (-12, -246), (16, -232)], 11, 2.2)
    for i in range(6):                                                           # rudraksha round the knot
        cr.new_path()
        cr.arc(-40 + 12 * i, -204 + 2 * math.sin(i * 1.7), 5.5, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    for k in range(3):                                                           # ash lines on the forehead
        ink(cr, [(10, -176 + 9 * k), (48, -172 + 9 * k)], 3.2, col=(1.0, 0.97, 0.9))
    cr.new_path()
    cr.arc(-14, -80, 7, 0, 2 * math.pi)
    leather(cr, BROWN, 2)


RURU = man("rr_ruru", skin=RU_SKIN, bulk=0.94, dhoti=RU_CLOTH, border=DRED, pleat=RU_CLOTH2, sash=RU_SASH, neck=BROWN,
           crown="tiara", halo=False, thread=True, beads=True, hair=False, earring=False, tilak=False,
           hands=("open", "open"))
for _m in ("calm", "smile", "weep", "angry", "shock"):
    register("rr_ruru_head" + ("" if _m == "calm" else "_" + _m), (-130, -290, 120, 60),
             (lambda m: lambda cr: ruru_head(cr, m))(_m))
register("rr_ruru_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, RU_SKIN, RU_CLOTH, DRED, 0.94))


# ------------------------------------------------------------------ Pramadvara


def pram_head(cr, eyes="open"):
    """Pramadvara: woman_head's face without a crown; jasmine round the bun with red, pink and gold flowers in it, a
    small gold maang-tikka on the hairline, a bindi, gold studs. eyes: open | shut | smile."""
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, PR_SKIN, 6)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 22 * math.cos(a), -128 + 22 * math.sin(a))], 3.2)
    for i in range(12):                                                           # jasmine round the bun
        a = math.pi * (0.25 + 1.5 * i / 11)
        _flower(cr, -62 + 42 * math.cos(a), -128 + 42 * math.sin(a), 9, PALE, 5)
    for x, y, r, col in ((-72, -176, 15, RED), (-44, -170, 12, ROSE), (-98, -156, 12, GOLD), (-100, -110, 11, RED)):
        _flower(cr, x, y, r, col, 6)
    ink(cr, [(-2, -188), (18, -184), (34, -176)], 3.5, col=GOLD)                 # maang-tikka chain
    _jewel(cr, 38, -170, 7, RED)
    cr.new_path()
    cr.arc(46, -146, 5, 0, 2 * math.pi)                                           # bindi
    cr.set_source_rgb(*RED)
    cr.fill()
    if eyes == "shut":
        _cover(cr, PR_SKIN, 30, -112, 19, 13)
        ink(cr, [(14, -112), (30, -104), (46, -112)], 4)
        for x in (22, 30, 38):
            ink(cr, [(x, -107), (x - 2, -100)], 2.2)
        ink(cr, [(14, -128), (30, -132), (46, -126)], 3.5)
    elif eyes == "smile":
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5)
    else:
        from puppet_core import almond_eye
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
    if eyes == "smile":
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    else:
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)
    _jewel(cr, -10, -70, 9, GOLD)


def _pram_extra(cr):
    """A thin gold necklace of beads and a small pendant."""
    for i in range(9):
        u = i / 8
        cr.new_path()
        cr.arc(-12 + 58 * u, -276 + 76 * u + 26 * u * u, 6, 0, 2 * math.pi)
        leather(cr, GOLD, 2.2)
    _jewel(cr, 50, -176, 9, RED)


PRAM = woman("rr_pram", skin=PR_SKIN, skirt=PR_SARI, choli=PR_CHOLI, border=GOLD, pallu_col=PR_PALLU, gem=RED,
             flower=PALE, ornaments_extra=_pram_extra, hands=("open", "open"))
for _e in ("open", "shut", "smile"):
    register("rr_pram_head" + ("" if _e == "open" else "_" + _e), (-140, -250, 100, 30),
             (lambda e: lambda cr: pram_head(cr, e))(_e))


# ------------------------------------------------------------------ the messenger of the gods


_DU_O = dict(skin=DU_SKIN, hair=True, moustache=False, tilak=True)


def duta_head(cr):
    """A ring of pale rays, long hair, a small gold crown with a saffron flare, a lotus over the ear."""
    M._ray_halo(cr, -30, -230, 128, 200, 16, (DU_RAY, GOLD))
    rface(cr, _DU_O, "teach")
    R.kirita(cr, GOLD, None, tall=0.86, flare=SAFFRON)
    _jewel(cr, 2, -150 + (-282 + 150) * 0.86, 9, (0.30, 0.60, 1.0))


def _wing(cr, col, col2):
    """A feathered wing (pivot at the root, on the upper back): long feathers fanning back and down, a covert patch."""
    for i in reversed(range(7)):                                                 # flight feathers, tip first
        u = i / 6
        bx, by = -50 - 330 * u, -30 - 210 * math.sin(math.pi * 0.5 * u)
        ang = 1.95 + 1.3 * u                                                     # down-back near the root, back at the tip
        ln = 250 + 90 * math.sin(math.pi * u * 0.8)
        cr.save()
        cr.translate(bx, by)
        cr.rotate(ang)
        fp = [(0, -30), (ln * 0.5, -40), (ln * 0.88, -22), (ln, 0), (ln * 0.88, 20), (ln * 0.5, 34), (0, 28)]
        _shape(cr, fp, col if i % 2 == 0 else col2, 3.5)
        ink(cr, [(14, 0), (ln * 0.86, 0)], 1.8, smooth=False, col=(0.66, 0.54, 0.34))
        cr.restore()
    cov = [(16, 14), (-30, -70), (-140, -180), (-290, -250), (-400, -250), (-360, -170), (-240, -90), (-120, -20),
           (-30, 34)]
    _shape(cr, cov, col, 4, holes=(11, 15, 2.6))
    for k in range(2):
        ink(cr, [(-50 - 40 * k, -30 - 14 * k), (-190 - 30 * k, -130 - 20 * k), (-320, -210 + 22 * k)], 2.2,
            col=(0.74, 0.62, 0.40))
    rivet(cr, 0, 0, 8)


DUTA = man("rr_duta", skin=DU_SKIN, bulk=0.95, dhoti=DU_CLOTH, border=GOLD, pleat=GOLD, sash=DU_SCARF, neck=GOLD,
           crown="tiara", halo=False, thread=True, hands=("open", "open"))
register("rr_duta_head", (-190, -470, 120, 120), duta_head)
register("rr_wingF", (-600, -340, 60, 280), lambda cr: _wing(cr, WING, WING2))
register("rr_wingB", (-600, -340, 60, 280), lambda cr: _wing(cr, (0.94, 0.84, 0.64), (0.92, 0.72, 0.42)))
DUTA.parts.insert(0, ("rr_wingB", "rr_duta_body", (-30, -250), -0.25))
DUTA.parts.insert(5, ("rr_wingF", "rr_duta_body", (-40, -236), 0.0))


def _lcloud(cr):
    """A small cloud of light (pivot at its centre top) for the messenger to float on."""
    blobs = [(0, 20, 180, 62), (-150, 40, 100, 50), (150, 40, 110, 52), (-70, -6, 90, 52), (80, -10, 96, 54)]
    for x, y, rx, ry in blobs:
        cr.new_path()
        ell(cr, x, y, rx, ry)
        leather(cr, (1.0, 0.97, 0.88), 5)
    for x, y, rx, ry in blobs:
        cr.new_path()
        ell(cr, x, y + 6, rx - 14, ry - 14)
        cr.set_source_rgb(1.0, 0.97, 0.88)
        cr.fill()
    holes_line(cr, [(-220, 50), (-80, 30), (80, 30), (230, 50)], 20, 3.6)
    for x in (-120, 0, 120):
        ink(cr, [(x - 40, 66), (x, 74), (x + 40, 66)], 2.5, col=(0.80, 0.80, 0.86))


register("rr_lcloud", (-280, -70, 280, 110), _lcloud)


# ------------------------------------------------------------------ Yama


_YM_O = dict(skin=YM_SKIN, hair=True, moustache=True, tilak=True)


def yama_head(cr):
    """Yama Dharmaraja: a dark-red flame halo, long black hair, a curled moustache, a tall gold crown with side peaks
    and a red flare."""
    K._halo(cr, DRED)
    rface(cr, _YM_O, "calm")
    ink(cr, [(20, -88), (8, -78), (14, -66)], 5, col=HAIR)                      # the moustache's curl
    R.kirita(cr, GOLD, None, tall=1.36, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.36
    for sx in (-1, 1):
        _shape(cr, [(sx * 30, -170), (sx * 66, h(-240)), (sx * 52, h(-290)), (sx * 40, h(-240)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 50, h(-254), 7, RED)
    _jewel(cr, 2, h(-292), 10, (0.16, 0.66, 0.40))


YAMA = man("rr_yama", skin=YM_SKIN, bulk=1.18, dhoti=YM_DHOTI, border=GOLD, pleat=GOLD, sash=GOLD, neck=GOLD,
           crown="tiara", halo=False, moustache=True, thread=True, hands=("open", "fist"))
register("rr_yama_head", (-230, -530, 140, 120), yama_head)


def _danda(cr):
    """Yama's danda (grip at 0, 0): a tall dark staff with gold bands, a gold head with a lotus bud on top."""
    band(cr, [(0, 420), (0, -380)], 22, DRED, spacing=22, hole_r=2.6)
    for y in (-300, -150, 0, 150, 300):
        band(cr, [(-14, y), (14, y)], 14, GOLD, holes=False)
    cr.new_path()
    ell(cr, 0, -440, 48, 62)
    leather(cr, GOLD, 5)
    for k in (-1, 0, 1):
        ink(cr, [(k * 34, -494), (k * 46, -440), (k * 34, -386)], 3.5)
    band(cr, [(-46, -440), (46, -440)], 12, RED, spacing=10, hole_r=2.0)
    _shape(cr, [(-16, -500), (0, -560), (16, -500)], GOLD, 4, smooth=False)
    _jewel(cr, 0, -440, 10, RED)


register("rr_danda", (-60, -580, 60, 440), _danda)


# ------------------------------------------------------------------ the rishi and his friend


_RS_O = dict(skin=RS_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def rishi_head(cr, mood="calm"):
    """The sage: long white hair behind, a long white beard and moustache, white matted hair piled up with rudraksha,
    white brows, ash lines."""
    hp = [(-30, -176), (-64, -146), (-90, -70), (-96, 40), (-70, 120), (-46, 70), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-74 - 6 * k, -20), (-66 - 4 * k, 90)], 2.5, col=(0.6, 0.58, 0.55))
    rface(cr, _RS_O, mood)
    bp = [(62, -50), (64, -22), (58, 40), (42, 120), (22, 70), (2, 20), (8, -40), (30, -54)]
    _shape(cr, bp, ASH, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -40), (42 - 12 * k, 20), (36 - 10 * k, 80)], 2.5, col=(0.62, 0.6, 0.6))
    dy = -6 if mood == "laugh" else 0
    m = [(66, -76 + dy), (46, -84 + dy), (24, -88 + dy), (12, -74 + dy), (30, -78 + dy), (52, -76 + dy),
         (68, -72 + dy)]
    _shape(cr, m, ASH, 3)
    for k in range(5):
        cr.new_path()
        ell(cr, -4 - 3 * k, -194 - 26 * k, 52 - 6 * k, 22)
        leather(cr, ASH, 4)
        ink(cr, [(-40 + 6 * k, -194 - 26 * k), (-4, -184 - 26 * k), (32 - 6 * k, -196 - 26 * k)], 2.5)
    for i in range(7):
        cr.new_path()
        cr.arc(-44 + 14 * i, -178, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    if mood not in ("laugh",):
        ink(cr, [(12, -142), (34, -150), (58, -142)], 7, col=ASH)
    for k in range(3):
        ink(cr, [(2, -172 + 9 * k), (44, -174 + 9 * k)], 3, col=(1.0, 0.97, 0.9))


RISHI = man("rr_rishi", skin=RS_SKIN, bulk=0.9, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=OCHRE, neck=BROWN,
            crown="tiara", halo=False, robe=(1.0, 0.70, 0.36), beads=True, hair=False, earring=False, tilak=False,
            hands=("open", "fist"))
for _m in ("calm", "laugh", "teach", "shock"):
    register("rr_rishi_head" + ("" if _m == "calm" else "_" + _m), (-190, -360, 120, 160),
             (lambda m: lambda cr: rishi_head(cr, m))(_m))

_KG_O = dict(skin=KG_SKIN, hair=True, moustache=True, beard=True, tilak=False, earring=False)


def khag_head(cr, mood="sleep"):
    """Khagama: dark matted hair piled up (jata) with rudraksha, a short dark beard, ash lines."""
    rface(cr, _KG_O, mood)
    for k in range(5):
        cr.new_path()
        ell(cr, -8 - 3 * k, -196 - 28 * k, 50 - 5 * k, 22)
        leather(cr, JATA, 4)
        ink(cr, [(-40 + 6 * k, -196 - 28 * k), (-6, -186 - 28 * k), (30 - 6 * k, -198 - 28 * k)], 2.5)
    for i in range(7):
        cr.new_path()
        cr.arc(-46 + 14 * i, -178, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    if mood != "shock":
        for k in range(3):
            ink(cr, [(4, -172 + 9 * k), (44, -174 + 9 * k)], 3, col=(1.0, 0.97, 0.9))


_KG = dict(skin=KG_SKIN, bulk=0.95, dhoti=SAFFRON, border=DRED, pleat=DRED, sash=OCHRE, neck=BROWN, beads=True)
KHAG = man("rr_khag", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
           moustache=True, **_KG)
for _m in ("sleep", "shock", "angry"):
    register("rr_khag_head" + ("" if _m == "sleep" else "_" + _m), (-190, -360, 120, 110),
             (lambda m: lambda cr: khag_head(cr, m))(_m))


def _khag_body_sit(cr):
    """His body with the front pleats tucked away (they would hang into the ground when he sits)."""
    from puppet_cast import man_body
    cr.save()
    cr.rectangle(-400, -600, 800, 664)
    cr.clip()
    man_body(cr, _KG)
    cr.restore()


def _khag_seat(cr):
    """Cross-legged in profile (hip at 0, 0; the ground at y = +SEAT_H), as jayadratha_cast._vk_seat."""
    th = [(-80, -30), (40, -44), (160, -32), (250, -10), (266, 40), (250, 86), (120, 96), (-40, 96), (-92, 70),
          (-96, 14)]
    _shape(cr, th, SAFFRON, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(246, -8), (266, 40), (250, 86)], 14, DRED, spacing=11, hole_r=2.4)
    band(cr, [(-84, 88), (240, 90)], 10, DRED, holes=False)
    foot = [(104, 8), (150, -6), (204, 0), (222, 22), (196, 38), (118, 40)]
    _shape(cr, foot, KG_SKIN, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 4), (x + 4, 18)], 2.2)
    rivet(cr, 0, 0, 9)


register("rr_khag_body_sit", (-200, -330, 140, 80), _khag_body_sit)
register("rr_khag_seat", (-110, -60, 280, 110), _khag_seat)


# ------------------------------------------------------------------ snakes (heads; the bodies are drawn per frame)


def snake_head(cr, kind="old", open_=0.0):
    """A snake's head in profile facing +x, the neck at x = 0 (HEAD_W wide). kind: old (grey-green, a round friendly
    eye, white brows, wrinkles, a gentle smile) | bite (dark brown, cream lips, a small slit eye, a forked tongue when
    open). open_ 0..1 opens the lower jaw about its hinge."""
    old = kind == "old"
    col, belly = (SN_OLD, SN_OLD_B) if old else (SN_BITE, SN_BITE_B)
    hinge = (70, 20)
    jaw_a = (0.34 if old else 0.62) * open_
    if open_ > 0:                                                                # the inside of the mouth
        tip_lo = _rot((196, 14), hinge, jaw_a)
        _shape(cr, [hinge, (196, 6), tip_lo], (0.42, 0.07, 0.08), 3, smooth=False)
        if not old:                                                              # a forked tongue
            ink(cr, [(150, 16), (214, 18), (244, 6)], 6, col=INK)
            ink(cr, [(150, 16), (214, 18), (244, 6)], 3, col=RED)
            ink(cr, [(214, 18), (246, 30)], 6, col=INK)
            ink(cr, [(214, 18), (246, 30)], 3, col=RED)
        else:
            _shape(cr, [(110, 16), (150, 18), (168, 26), (140, 30)], ROSE, 2, smooth=True)
    jaw = [(-12, 24), (40, 22), (90, 18), (130, 14), (172, 12), (194, 14), (186, 30), (150, 42), (100, 50), (50, 52),
           (-12, 50)]
    cr.save()
    cr.translate(*hinge)
    cr.rotate(jaw_a)
    cr.translate(-hinge[0], -hinge[1])
    _shape(cr, jaw, belly, 5)
    if not old:
        holes_line(cr, [(20, 38), (100, 36), (160, 26)], 14, 2.2)
    cr.restore()
    if old:
        top = [(-12, -50), (30, -60), (80, -68), (130, -64), (168, -46), (192, -20), (200, 4), (170, 12), (130, 16),
               (90, 20), (40, 26), (-12, 28)]
    else:
        top = [(-12, -48), (40, -56), (110, -60), (168, -44), (204, -16), (212, 4), (176, 10), (130, 14), (80, 18),
               (30, 24), (-12, 26)]
    _shape(cr, top, col, 5)
    if old:
        cr.new_path()                                                            # the big, friendly eye
        ell(cr, 116, -26, 24, 24)
        leather(cr, PALE, 4)
        cr.new_path()
        cr.arc(122, -24, 13, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(127, -30)], 4.8)
        ink(cr, [(98, -6), (116, 0), (136, -6)], 2.5)                            # a soft lower lid
        _shape(cr, [(90, -50), (108, -62), (134, -62), (152, -50), (134, -52), (110, -50)], ASH, 3)   # white brow
        for k in range(3):
            ink(cr, [(100 + 14 * k, -56), (96 + 14 * k, -66)], 2, col=(0.62, 0.6, 0.6))
        for k in range(3):                                                       # wrinkles at the neck
            ink(cr, [(8 + 16 * k, -32), (14 + 16 * k, -10), (8 + 16 * k, 12)], 2.6)
        if open_ <= 0:
            ink(cr, [(198, 8), (170, 14), (146, 12), (134, 4)], 3.5)            # a gentle smile
        punch(cr, [(186, -12)], 3.2)
        holes_line(cr, [(0, -38), (60, -50)], 15, 2.4)
    else:
        ink(cr, [(60, -36), (110, -40), (150, -32)], 7, col=(0.22, 0.14, 0.08))  # the dark eye stripe
        cr.new_path()
        ell(cr, 126, -26, 14, 12)
        leather(cr, (1.0, 0.84, 0.20), 3.5)
        cr.new_path()
        ell(cr, 127, -26, 3, 10)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(196, -8)], 3)
        if open_ <= 0:
            ink(cr, [(208, 6), (176, 12), (140, 14)], 3, col=SN_BITE_B)
        holes_line(cr, [(0, -34), (70, -46), (130, -48)], 15, 2.4)


def _rot(p, c, a):
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


register("rr_snake_old", (-30, -90, 230, 120), lambda cr: snake_head(cr, "old", 0.0))
register("rr_snake_old_talk", (-30, -90, 230, 130), lambda cr: snake_head(cr, "old", 1.0))
register("rr_snake_bite", (-30, -80, 260, 80), lambda cr: snake_head(cr, "bite", 0.0))
register("rr_snake_bite_open", (-30, -80, 260, 200), lambda cr: snake_head(cr, "bite", 1.0))


def _gsnake(cr):
    """The toy snake of grass (pivot at its tail end, where it is held; it hangs down): a braided straw rope with
    green blades, a knot for a head with two punched eyes and a straw tongue."""
    pts = [(0, 0), (20, 80), (-30, 170), (30, 260), (-20, 350), (16, 430), (0, 500)]
    for w, col in ((34, STRAW),):
        cr.new_path()
        spath(cr, pts, closed=False)
        cr.set_line_cap(1)
        cr.set_source_rgb(*INK)
        cr.set_line_width(w + 9)
        cr.stroke_preserve()
        cr.set_source_rgb(*col)
        cr.set_line_width(w)
        cr.stroke()
    for i in range(1, 30):                                                       # the braid
        u = i / 30
        k = min(int(u * 6), 5)
        f = u * 6 - k
        x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f
        y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
        ink(cr, [(x - 12, y - 8), (x + 12, y + 6)], 2.4, smooth=False, col=STRAW2)
    for y, sx in ((60, 1), (150, -1), (240, 1), (330, -1), (410, 1)):
        x = 0
        for i in range(len(pts) - 1):
            if pts[i][1] <= y <= pts[i + 1][1]:
                f = (y - pts[i][1]) / (pts[i + 1][1] - pts[i][1])
                x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
        _shape(cr, [(x, y), (x + sx * 44, y - 30), (x + sx * 70, y - 26), (x + sx * 38, y - 14)], GREEN, 2.5)
    cr.new_path()
    ell(cr, 2, 520, 34, 42)
    leather(cr, STRAW, 5)
    punch(cr, [(-12, 512), (14, 512)], 5)
    ink(cr, [(0, 560), (0, 590), (-10, 606)], 3, col=STRAW2)
    ink(cr, [(0, 590), (10, 606)], 3, col=STRAW2)
    band(cr, [(-18, 470), (20, 474)], 10, GREEN, holes=False)


register("rr_gsnake", (-70, -20, 110, 620), _gsnake)


# ------------------------------------------------------------------ the life bar


def _bar(cr):
    """The LIFE BAR: a leather cartouche (centre pivot, 900 x 150) with a red heart at the left and ten windows
    punched through it (the lamp light glows through each one; the scenes light or darken them)."""
    pts = [(-450, -60), (-420, -80), (440, -80), (470, -60), (470, 60), (440, 80), (-420, 80), (-450, 60)]
    _shape(cr, pts, PARCH, 7, smooth=False, holes=(13, 16, 3.0))
    hx, hy = -378, 2                                                             # the heart
    heart = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        heart.append((hx + 3.1 * x, hy + 3.1 * y))
    _shape(cr, heart, RED, 5, smooth=False)
    punch(cr, [(hx - 18, hy - 16)], 6)
    for i in range(10):                                                          # the windows
        cx = BAR_CELL0 + BAR_STEP * i
        x0, x1 = cx - BAR_CW / 2, cx + BAR_CW / 2
        y0, y1 = -BAR_CH / 2, BAR_CH / 2
        cr.new_path()
        poly(cr, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
        cr.set_source_rgb(*INK)
        cr.set_line_width(12)
        cr.stroke()
        cut(cr, lambda x0=x0, x1=x1, y0=y0, y1=y1: poly(cr, [(x0 + 3, y0 + 3), (x1 - 3, y0 + 3), (x1 - 3, y1 - 3),
                                                             (x0 + 3, y1 - 3)]))


register("rr_bar", (-470, -100, 490, 100), _bar)


# ------------------------------------------------------------------ the bride's foot, grass


def _foot(cr):
    """Pramadvara's foot in close-up (facing +x, pivot at the heel on the ground): the sari hem with a gold border,
    a silver anklet with little bells, the sole edged in red alta, red dots, a toe ring."""
    foot = [(46, -300), (40, -200), (32, -130), (12, -84), (2, -44), (12, -8), (50, 0), (110, -7), (165, -11),
            (215, -5), (262, 0), (318, 0), (346, -4), (358, -18), (350, -34), (318, -40), (276, -46), (226, -62),
            (176, -88), (144, -122), (130, -180), (128, -300)]
    _shape(cr, foot, PR_SKIN, 5)
    ink(cr, [(52, -130), (64, -116), (54, -104)], 2.6)                           # the ankle bone
    for x, y, rx in ((330, -40, 16), (306, -44, 14), (284, -48, 12)):           # the smaller toes behind
        cr.new_path()
        ell(cr, x, y, rx, 11, -0.15)
        leather(cr, PR_SKIN, 3)
        cr.new_path()
        ell(cr, x + rx * 0.4, y - 2, 4.5, 3.5)
        cr.set_source_rgb(*ALTA)
        cr.fill()
    cr.new_path()                                                                 # the big toe's nail, painted red
    ell(cr, 344, -28, 9, 6, -0.3)
    leather(cr, ALTA, 2)
    ink(cr, [(312, -38), (318, -12)], 2.4)
    band(cr, [(14, -6), (60, 2), (112, -4), (166, -8), (216, -2), (262, 2), (320, 2), (350, -4)], 10, ALTA, holes=False,
         lw=2.5)                                                                  # alta along the sole
    for x, y in ((200, -54), (232, -44), (170, -70)):
        cr.new_path()
        cr.arc(x, y, 5, 0, 2 * math.pi)
        cr.set_source_rgb(*ALTA)
        cr.fill()
    _flower(cr, 196, -36, 11, ALTA, 6)
    cr.new_path()                                                                 # a silver toe ring
    ell(cr, 306, -44, 9, 6)
    cr.set_source_rgb(*SILVER)
    cr.set_line_width(4)
    cr.stroke()
    band(cr, [(34, -168), (84, -174), (134, -166)], 16, SILVER, spacing=10, hole_r=2.0)   # the anklet
    for i in range(5):
        x = 44 + 20 * i
        cr.new_path()
        cr.arc(x, -148 + 2 * math.sin(i), 7, 0, 2 * math.pi)
        leather(cr, SILVER, 2.2)
    hem = [(-90, -700), (290, -700), (318, -420), (362, -268), (-130, -268), (-112, -420)]
    _shape(cr, hem, PR_SARI, 6)
    dots_in(cr, lambda: poly(cr, hem), 26, 3.4, shape="d")
    for x0, x1 in ((-20, -70), (70, 40), (160, 150), (240, 260)):               # pleats, flaring a little
        ink(cr, [(x0, -700), (x1, -290)], 3, smooth=False)
    band(cr, [(-136, -292), (110, -288), (360, -292)], 38, GOLD, spacing=14)
    holes_line(cr, [(-130, -276), (356, -276)], 14, 2.6)


register("rr_foot", (-170, -720, 380, 20), _foot)


def _grass(cr, seed):
    """A clump of tall grass (pivot at its base): blades curving up, punched along the middle."""
    rng = random.Random(seed)
    blades = []
    for i in range(15):
        bx = rng.uniform(-110, 110)
        h = rng.uniform(360, 600)
        lean = rng.uniform(-190, 190)
        blades.append((h, bx, lean, i))
    for h, bx, lean, i in sorted(blades, reverse=True):
        w = rng.uniform(8, 13)
        tip = (bx + lean, -h)
        mid = (bx + lean * 0.3, -h * 0.55)
        pts = [(bx - w, 0), (mid[0] - w * 0.7, mid[1]), tip, (mid[0] + w * 0.7, mid[1]), (bx + w, 0)]
        _shape(cr, pts, (GREEN, (0.50, 0.74, 0.30), DGREEN)[i % 3], 3)


for _g in range(3):
    register(f"rr_grass{_g}", (-280, -600, 280, 10), (lambda g: lambda cr: _grass(cr, 40 + g))(_g))


# ------------------------------------------------------------------ the wedding mandap


def _marigolds(cr, pts, r=13):
    for i, (x, y) in enumerate(pts):
        star = []
        for k in range(14):
            aa = 2 * math.pi * k / 14
            rr = r if k % 2 == 0 else r * 0.74
            star.append((x + rr * math.cos(aa), y + rr * math.sin(aa)))
        _shape(cr, star, GOLD if i % 3 else SAFFRON, 2.2, smooth=False)
        punch(cr, [(x, y)], 2.6)


def _mandap(cr):
    """The wedding mandap (pivot at the bottom centre): four posts wrapped in red and gold, a red canopy with a
    scalloped gold valance and a kalasha on top, banana plants tied to the front posts, marigold strings, a toran."""
    for x in (-330, 330):                                                        # the back posts, thinner
        _shape(cr, [(x - 14, -40), (x + 14, -40), (x + 12, -960), (x - 12, -960)], (0.50, 0.28, 0.14), 4, smooth=False)
    for x in (-470, 470):                                                        # banana plants
        sx = -1 if x < 0 else 1
        _shape(cr, [(x - 22, 0), (x + 22, 0), (x + 16, -520), (x - 16, -520)], (0.56, 0.68, 0.30), 4, smooth=False)
        for k, (ln, a) in enumerate(((420, -0.5), (380, -0.95), (360, 0.05), (330, -1.35))):
            cr.save()
            cr.translate(x, -500 + 70 * k)
            cr.rotate(sx * (math.pi / 2 + a) - math.pi / 2)
            leaf = [(0, -10), (ln * 0.3, -60), (ln * 0.75, -52), (ln, -10), (ln * 0.7, 30), (ln * 0.3, 34), (0, 10)]
            _shape(cr, leaf, BANANA if k % 2 == 0 else DGREEN, 4)
            ink(cr, [(0, 0), (ln * 0.95, -12)], 2.6)
            for j in range(5):
                ink(cr, [(ln * (0.15 + 0.15 * j), -2), (ln * (0.22 + 0.15 * j), -40)], 1.8, col=(0.24, 0.42, 0.14))
            cr.restore()
    for x in (-470, 470):                                                        # the front posts
        _shape(cr, [(x - 24, 0), (x + 24, 0), (x + 20, -980), (x - 20, -980)], RED, 5, smooth=False)
        for k in range(14):
            y = -40 - 66 * k
            band(cr, [(x - 22, y), (x + 22, y - 22)], 12, GOLD, holes=False, lw=3)
        _shape(cr, [(x - 40, 0), (x + 40, 0), (x + 30, -40), (x - 30, -40)], GOLD, 4, smooth=False)
        _shape(cr, [(x - 38, -970), (x + 38, -970), (x + 30, -1000), (x - 30, -1000)], GOLD, 4, smooth=False)
        _marigolds(cr, [(x + 30 * math.sin(i * 0.9), -930 + 34 * i) for i in range(12)], 12)
    roof = [(-560, -990), (560, -990), (520, -1080), (0, -1200), (-520, -1080)]
    _shape(cr, roof, RED, 7, smooth=False, holes=(12, 16, 3.0))
    dots_in(cr, lambda: poly(cr, [(-480, -1000), (480, -1000), (440, -1070), (0, -1170), (-440, -1070)]), 30, 3.6,
            shape="d")
    band(cr, [(-560, -996), (560, -996)], 26, GOLD, spacing=14)
    A._scallops(cr, -560, 560, -986, 56, 36, GOLD)
    cr.new_path()                                                                 # the kalasha on top
    ell(cr, 0, -1236, 36, 30)
    leather(cr, GOLD, 4)
    _shape(cr, [(-26, -1262), (26, -1262), (16, -1292), (-16, -1292)], GOLD, 3, smooth=False)
    for k in (-1, 0, 1):
        _shape(cr, [(k * 16, -1290), (k * 34, -1330), (k * 8, -1300)], GREEN, 2.5)
    for i in range(3):                                                            # marigold swags under the canopy
        x0, x1 = -470 + 313 * i, -470 + 313 * (i + 1)
        pts = [(x0 + (x1 - x0) * u, -930 + 90 * math.sin(math.pi * u)) for u in (j / 13 for j in range(14))]
        _marigolds(cr, pts, 12)
    for i in range(15):                                                           # a mango-leaf toran
        x = -420 + 60 * i
        _shape(cr, [(x - 10, -968), (x + 10, -968), (x + 7, -922), (x, -900), (x - 7, -922)], GREEN, 2.6)


register("rr_mandap", (-720, -1350, 720, 10), _mandap)


# ------------------------------------------------------------------ small things


def _tear(cr):
    cr.new_path()
    cr.move_to(0, -26)
    cr.curve_to(14, -4, 14, 14, 0, 16)
    cr.curve_to(-14, 14, -14, -4, 0, -26)
    leather(cr, TEAR, 3)
    punch(cr, [(-3, 2)], 3)


register("rr_tear", (-20, -32, 20, 22), _tear)
for _n, _c in (("rr_fl_red", RED), ("rr_fl_pink", ROSE), ("rr_fl_gold", GOLD), ("rr_fl_white", PALE)):
    register(_n, (-26, -26, 26, 26), (lambda c: lambda cr: _flower(cr, 0, 0, 20, c, 6))(_c))
