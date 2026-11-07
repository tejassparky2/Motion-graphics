"""The leather cast and props for the Kaikeyi debate reel (videos/kaikeyi.py), in the Togalu Gombeyaata style of the
Jarasandha and Ravana reels (puppet_cast, ravana_cast): profile figures with big almond eyes, perforated garments and
jointed limbs. Traditional leather puppets, modelled on no actor and no film.

Cast (one look each, kept the same through the video):
  KAIKEYI    queen of Ayodhya, princess of Kekaya: violet sari with a plum pallu and gold border, a three-peaked gold
             queen's crown, long necklace. Dignified: calm face, no villain features.
  DASHARATHA the old king: white hair and a long white beard, a tall gold kirita with a deep-red halo, red dhoti, green
             sash.
  KEKAYA     Kaikeyi's father, the Kekaya king: a saffron turban-crown with a plume (no kirita), a short dark beard,
             green dhoti with a saffron sash.
  RAMA       blue skin, gold kirita with a green halo, yellow dhoti, a bow and a quiver; calm.
  BHARATA    the young prince: warm tan skin, no beard, a smaller crown with a blue flare, cream dhoti with blue
             border and sash. Also kneels (bharata_kneel).
Props: the leather balance scale (post, beam, two pans with their strings), the crown, palm-leaf evidence tags, the
invitation scroll and a quill, garlands, the promise scroll, a coronation drum, the throne, Rama's padukas, a cloth map
of Ayodhya and Kekaya with city icons, pointing hands.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math
import random

import puppet_cast as C
import ravana_cast as R
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, SAFFRON, band, cut,
                         dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet, spath)

KK_SKIN = (0.99, 0.78, 0.58)          # Kaikeyi
KK_SARI = (0.66, 0.40, 0.80)          # violet sari
KK_PLUM = (0.44, 0.18, 0.52)          # plum pallu
DS_SKIN = (0.98, 0.76, 0.56)          # Dasharatha
ASH = (0.86, 0.86, 0.92)              # white hair and beard (a cool grey reads as white on the warm cloth)
ASH2 = (0.56, 0.55, 0.60)
KEK_SKIN = (0.90, 0.60, 0.38)         # the Kekaya king
RAMA_SKIN = (0.26, 0.48, 0.95)        # Rama: blue
BH_SKIN = (0.97, 0.68, 0.42)          # Bharata
LEAF = (0.98, 0.86, 0.56)             # palm leaf
LEAF2 = (0.86, 0.66, 0.34)
WOOD = (0.58, 0.34, 0.16)

POST_H = 720.0                        # the scale: pivot height above the base
BEAM_L = 330.0                        # beam half length (pivot to hook)
PAN_DROP = 300.0                      # hook to pan rim


# ------------------------------------------------------------------ shared head pieces


def _halo(cr, col):
    pts = []
    for i in range(19):
        a = math.pi * (0.62 + 0.9 * i / 18)
        r = 160 if i % 2 == 0 else 128
        pts.append((-30 + r * math.cos(a) * 1.05, -190 + r * math.sin(a) * 1.1))
    pts += [(-40, -150), (0, -160)]
    _shape(cr, pts, col, 5, smooth=False, holes=(14, 15, 3))


# ------------------------------------------------------------------ Kaikeyi


def queen_crown(cr):
    """A queen's crown: three gold peaks over a jewelled band, pearl strings at the back."""
    for k in range(3):                                                            # pearls hanging behind
        x = -52 - 9 * k
        for j in range(5):
            cr.new_path()
            cr.arc(x - 2 * j, -150 + 15 * j, 4.5, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    pts = [(-48, -154), (-52, -196), (-40, -236), (-26, -206), (-8, -244), (2, -272), (12, -244), (28, -206),
           (42, -236), (54, -196), (52, -154)]
    _shape(cr, pts, GOLD, 5, smooth=False, holes=(10, 13, 2.6))
    for x, y in ((-40, -222), (2, -246), (42, -222)):
        _jewel(cr, x, y, 8, RED)
    _jewel(cr, 2, -200, 12, GREEN)
    band(cr, [(-50, -164), (54, -164)], 15, RED, spacing=11, hole_r=2.3)
    cr.new_path()
    cr.arc(2, -282, 9, 0, 2 * math.pi)
    leather(cr, GOLD, 3)


def kaikeyi_head(cr):
    C.woman_head(cr, dict(skin=KK_SKIN, flower=PALE))
    queen_crown(cr)
    for k in range(3):                                                            # long jhumka earring
        cr.new_path()
        cr.arc(-10, -44 + 12 * k, 5 - k, 0, 2 * math.pi)
        leather(cr, GOLD, 2)


def _kaikeyi_extra(cr):
    """A long gold necklace with a pendant and a jewelled waist belt."""
    band(cr, [(-22, -282), (10, -206), (34, -150)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 36, -140, 11, RED)
    for x in (-24, 4, 30):
        _jewel(cr, x, -24, 7, RED)


KAIKEYI = woman("kaikeyi", skin=KK_SKIN, skirt=KK_SARI, choli=GOLD, border=GOLD, pallu_col=KK_PLUM, gem=RED,
                flower=PALE, ornaments_extra=_kaikeyi_extra, hands=("open", "open"))
register("kaikeyi_head", (-130, -300, 110, 40), kaikeyi_head)


# ------------------------------------------------------------------ Dasharatha


_DS_O = dict(skin=DS_SKIN, crown="tiara", hair=False, halo=False, beard=False, moustache=False, tilak=True)


def ds_crown(cr):
    """Dasharatha's tall crown alone (head coordinates), so it can slip and fall in the death scene."""
    R.kirita(cr, GOLD, None, tall=1.3, flare=DRED)
    _jewel(cr, 4, -150 + (-282 + 150) * 1.3, 10, GREEN)


def dasharatha_head(cr, crown=True):
    """The old king: deep-red halo, white hair down the back, a long white beard, a tall gold crown."""
    if crown:
        _halo(cr, DRED)
    hp = [(-30, -176), (-64, -146), (-92, -70), (-98, 40), (-74, 110), (-48, 64), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-76 - 6 * k, -20), (-68 - 4 * k, 80)], 2.5, col=ASH2)
    C.man_head(cr, _DS_O)
    ink(cr, [(12, -140), (34, -150), (60, -140)], 8, col=ASH)                     # white brows
    ink(cr, [(52, -104), (60, -96)], 2.5)                                          # age lines at the eye
    ink(cr, [(8, -92), (20, -80)], 2.5)
    bp = [(66, -60), (72, -30), (68, 16), (56, 66), (36, 118), (18, 150), (6, 112), (-8, 60), (-12, 4), (-4, -40),
          (18, -58), (42, -62)]
    _shape(cr, bp, ASH, 4)
    for k in range(4):
        ink(cr, [(52 - 12 * k, -44), (46 - 13 * k, 30), (36 - 10 * k, 100)], 2.5, col=ASH2)
    m = [(74, -76), (52, -86), (26, -90), (6, -76), (28, -80), (52, -76), (76, -71)]
    _shape(cr, m, ASH, 3)
    if crown:
        ds_crown(cr)
    else:                                                                         # bare head: white hair on top
        _shape(cr, [(-40, -168), (-30, -192), (0, -204), (34, -196), (52, -170), (10, -176)], ASH, 4)


DASHARATHA = man("dasharatha", skin=DS_SKIN, bulk=1.12, dhoti=RED, border=GOLD, pleat=GOLD, sash=DGREEN, neck=GOLD,
                 crown="tiara", halo=False, hair=False, hands=("open", "open"))
register("dasharatha_head", (-200, -490, 120, 170), dasharatha_head)
register("dasharatha_head_bare", (-200, -260, 120, 170), lambda cr: dasharatha_head(cr, crown=False))
register("ds_crown", (-130, -490, 80, -120), ds_crown)


# ------------------------------------------------------------------ the Kekaya king


_KEK_O = dict(skin=KEK_SKIN, crown="tiara", hair=True, halo=False, beard=False, moustache=True, tilak=True)


def kekaya_head(cr):
    """Kaikeyi's father: a saffron turban-crown with a gold band, a red jewel and a plume; short dark beard."""
    pl = [(-40, -230), (-80, -300), (-128, -330), (-150, -318), (-112, -290), (-80, -250), (-56, -214)]   # plume
    _shape(cr, pl, PALE, 4)
    holes_line(cr, [(-50, -232), (-90, -290), (-130, -318)], 13, 2.4)
    ink(cr, [(-44, -228), (-130, -322)], 2.5, col=RED)
    C.man_head(cr, _KEK_O)
    bp = [(60, -50), (64, -26), (54, 8), (34, 26), (14, 14), (4, -24), (24, -48)]
    _shape(cr, bp, HAIR, 4)
    tb = [(-62, -136), (-70, -184), (-48, -228), (-6, -248), (40, -240), (66, -206), (64, -156), (24, -166),
          (-22, -154)]
    _shape(cr, tb, SAFFRON, 6, holes=(10, 14, 2.6))
    for k in range(3):                                                            # the wraps of the turban
        ink(cr, [(-58, -170 - 20 * k), (-10, -196 - 14 * k), (50, -200 - 8 * k)], 3)
    band(cr, [(-62, -150), (-10, -162), (62, -164)], 15, GOLD, spacing=11, hole_r=2.3)
    _jewel(cr, 44, -194, 15, RED)
    _shape(cr, [(-46, -226), (-34, -246), (-20, -232)], GOLD, 3)                 # plume holder


KEKAYA = man("kekaya", skin=KEK_SKIN, bulk=1.15, dhoti=DGREEN, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
             crown="tiara", halo=False, moustache=True, hands=("open", "open"))
register("kekaya_head", (-200, -380, 120, 100), kekaya_head)


# ------------------------------------------------------------------ Rama and Bharata


def _quiver(cr):
    """Rama's quiver of arrows on his back (pivot at the strap, hanging down-left)."""
    q = [(-26, 0), (26, 0), (30, 230), (-22, 236)]
    _shape(cr, q, DRED, 5, smooth=False, holes=(9, 13, 2.4))
    band(cr, [(-28, 30), (28, 30)], 12, GOLD, spacing=10, hole_r=2)
    band(cr, [(-26, 200), (30, 200)], 12, GOLD, spacing=10, hole_r=2)
    for k in range(4):                                                            # fletched arrow ends
        x = -16 + 11 * k
        ink(cr, [(x, 0), (x - 4, -60)], 4)
        _shape(cr, [(x - 4, -60), (x - 14, -90), (x - 4, -82), (x + 6, -90)], RED if k % 2 else GOLD, 2.5,
               smooth=False)


RAMA = man("rama", skin=RAMA_SKIN, bulk=1.05, dhoti=GOLD, border=DRED, pleat=DRED, sash=RED, neck=GOLD,
           crown_col=GOLD, halo_col=GREEN, thread=True, hands=("open", "fist"))
register("rama_quiver", (-50, -110, 50, 250), _quiver)
RAMA.parts.insert(0, ("rama_quiver", "rama_body", (-30, -250), 0.55))

_BH_O = dict(skin=BH_SKIN, crown="tiara", hair=True, halo=False, tilak=True)


def bharata_head(cr):
    C.man_head(cr, _BH_O)
    R.kirita(cr, GOLD, None, tall=0.72, flare=BLUE)


BHARATA = man("bharata", skin=BH_SKIN, bulk=0.95, dhoti=PALE, border=BLUE, pleat=BLUE, sash=BLUE, neck=GOLD,
              crown="tiara", halo=False, hands=("open", "open"))
register("bharata_head", (-190, -400, 110, 100), bharata_head)


def kneel_legs(cr, skin, dhoti, border, b=1.0):
    """Legs kneeling on one knee (hip at 0, 0; ground at y=+250), as ravana_cast.ravana_kneel."""
    _shape(cr, [(-40, 196), (-36, 242), (-190, 250), (-200, 232), (-180, 212)], skin, 5)
    _shape(cr, [(-186, 214), (-232, 200), (-240, 246), (-194, 250)], skin, 4)
    th = [(-54 * b, -20), (44 * b, -24), (44, 40), (14, 226), (-48, 236), (-72, 100)]
    _shape(cr, th, dhoti, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(-46, 214), (16, 214)], 14, border, spacing=11, hole_r=2.4)
    _shape(cr, [(120, 40), (170, 40), (168, 222), (126, 226)], skin, 5)
    _shape(cr, [(118, 214), (170, 212), (226, 230), (228, 250), (116, 252)], skin, 4)
    band(cr, [(124, 204), (168, 204)], 9, GOLD, spacing=8, hole_r=2.0)
    fth = [(-40, -34), (60, -40), (176, 8), (182, 70), (120, 82), (-30, 60)]
    _shape(cr, fth, dhoti, 5)
    dots_in(cr, lambda: spath(cr, fth), 19, 2.8)
    band(cr, [(120, 76), (186, 64)], 14, border, spacing=11, hole_r=2.4)
    rivet(cr, 0, 0, 9)


register("bharata_kneel", (-250, -60, 240, 260), lambda cr: kneel_legs(cr, BH_SKIN, PALE, BLUE, 0.95))


# ------------------------------------------------------------------ the balance scale


def _post(cr):
    """The scale's stand: stepped base, a turned column, a fork holding the pivot (pivot at y=-POST_H)."""
    for y0, w, col in ((0, 170, WOOD), (-46, 130, OCHRE), (-84, 90, WOOD)):
        _shape(cr, [(-w, y0), (w, y0), (w - 14, y0 - 40), (-w + 14, y0 - 40)], col, 6, smooth=False,
               holes=(9, 14, 2.8) if w > 100 else None)
    band(cr, [(-150, -26), (150, -26)], 14, GOLD, spacing=13)
    col = [(-24, -120), (24, -120), (20, -POST_H + 70), (-20, -POST_H + 70)]
    _shape(cr, col, WOOD, 6, smooth=False)
    holes_line(cr, [(0, -140), (0, -POST_H + 90)], 26, 3.2, smooth=False)
    for y in (-260, -470):                                                        # turned knobs
        cr.new_path()
        ell(cr, 0, y, 46, 26)
        leather(cr, GOLD, 5)
        punch(cr, [(-24, y), (0, y), (24, y)], 4)
    fork = [(-60, -POST_H + 90), (60, -POST_H + 90), (54, -POST_H - 40), (34, -POST_H - 40), (30, -POST_H + 50),
            (-30, -POST_H + 50), (-34, -POST_H - 40), (-54, -POST_H - 40)]
    _shape(cr, fork, GOLD, 5, smooth=False, holes=(8, 12, 2.2))
    cr.new_path()                                                                 # finial: a gold knob
    ell(cr, 0, -POST_H - 66, 30, 26)
    leather(cr, GOLD, 4)
    _jewel(cr, 0, -POST_H - 66, 10, RED)
    poly(cr, [(-6, -POST_H - 90), (0, -POST_H - 122), (6, -POST_H - 90)])
    leather(cr, GOLD, 3)


def _beam(cr):
    """The beam (pivot at 0, 0): tapered gold bar, rings at the hooks (x = +-BEAM_L), a pointer needle up."""
    L = BEAM_L
    pts = [(-L - 10, -8), (-L + 30, -14), (-60, -20), (0, -26), (60, -20), (L - 30, -14), (L + 10, -8), (L + 10, 10),
           (L - 30, 14), (60, 22), (0, 28), (-60, 22), (-L + 30, 14), (-L - 10, 10)]
    _shape(cr, pts, GOLD, 6, smooth=False)
    holes_line(cr, [(-L + 30, 1), (L - 30, 1)], 20, 3.2, smooth=False)
    for sx in (-1, 1):
        band(cr, [(sx * 100, -22), (sx * 100, 24)], 12, RED, spacing=10, hole_r=2)
        cr.new_path()
        cr.arc(sx * L, 0, 22, 0, 2 * math.pi)
        leather(cr, GOLD, 5)
        punch(cr, [(sx * L, 0)], 8)
    _shape(cr, [(-12, -20), (0, -150), (12, -20)], GOLD, 4, smooth=False)       # the pointer
    _jewel(cr, 0, -30, 12, RED)
    rivet(cr, 0, 0, 12)


def _pan(cr):
    """A pan with its two strings, hanging from the hook (0, 0); the rim is at y = PAN_DROP."""
    D = PAN_DROP
    for sx in (-1, 1):
        ink(cr, [(0, 0), (sx * 128, D)], 5, smooth=False)
        holes_line(cr, [(0, 10), (sx * 122, D - 8)], 34, 1.8, smooth=False)
    cr.new_path()
    cr.arc(0, 0, 14, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    bowl = [(-142, D - 6), (142, D - 6), (136, D + 14), (100, D + 40), (40, D + 54), (-40, D + 54), (-100, D + 40),
            (-136, D + 14)]
    _shape(cr, bowl, GOLD, 6)
    band(cr, [(-136, D + 8), (136, D + 8)], 13, RED, spacing=11, hole_r=2.3)
    dots_in(cr, lambda: poly(cr, [(-96, D + 24), (96, D + 24), (40, D + 46), (-40, D + 46)]), 16, 2.6)


register("kk_post", (-180, -POST_H - 120, 180, 10), _post)
register("kk_beam", (-BEAM_L - 30, -160, BEAM_L + 30, 40), _beam)
register("kk_pan", (-150, -20, 150, PAN_DROP + 64), _pan)


# ------------------------------------------------------------------ props


def _crown(cr):
    """The crown of Ayodhya, frontal (pivot at the bottom centre), ~200 units tall."""
    pts = [(-96, 0), (96, 0), (100, -46), (118, -120), (78, -82), (58, -150), (28, -96), (0, -196), (-28, -96),
           (-58, -150), (-78, -82), (-118, -120), (-100, -46)]
    _shape(cr, pts, GOLD, 6, smooth=False, holes=(11, 14, 2.6))
    band(cr, [(-98, -22), (98, -22)], 22, RED, spacing=13, hole_r=2.6)
    for x in (-60, -20, 20, 60):
        _jewel(cr, x, -22, 8, GOLD)
    _jewel(cr, 0, -100, 17, GREEN)
    for x, y in ((-58, -118), (58, -118), (-104, -96), (104, -96)):
        _jewel(cr, x, y, 8, RED)
    cr.new_path()
    cr.arc(0, -206, 13, 0, 2 * math.pi)
    leather(cr, GOLD, 4)


def _leaf(cr):
    """A palm-leaf strip (centre pivot), string holes and a red thread; text is drawn over it per frame."""
    pts = [(-270, 0), (-250, -34), (-200, -44), (200, -44), (250, -34), (270, 0), (250, 34), (200, 44), (-200, 44),
           (-250, 34)]
    _shape(cr, pts, LEAF, 5)
    ink(cr, [(-236, -30), (236, -30)], 2, smooth=False, col=LEAF2)
    ink(cr, [(-236, 30), (236, 30)], 2, smooth=False, col=LEAF2)
    punch(cr, [(-226, 0), (226, 0)], 6)
    ink(cr, [(-226, 8), (-236, 40), (-226, 66)], 3.5, col=RED)


def _scroll(cr):
    """The invitation list: a tall paper sheet between two wooden rollers (centre pivot)."""
    rng = random.Random(5)
    w, h = 330, 380
    pts = [(-w, -h)]
    for i in range(1, 16):
        pts.append((w * (-1 + 2 * i / 15), -h + rng.uniform(-3, 3)))
    pts += [(w, h)]
    for i in range(1, 16):
        pts.append((w * (1 - 2 * i / 15), h + rng.uniform(-3, 3)))
    _shape(cr, pts, PARCH, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-w + 24, -h + 30), (w - 24, -h + 30), (w - 24, h - 30), (-w + 24, h - 30)]), 64,
            1.4)
    for y in (-h, h):
        _shape(cr, [(-w - 30, y - 24), (w + 30, y - 24), (w + 30, y + 24), (-w - 30, y + 24)], WOOD, 5, smooth=False)
        for sx in (-1, 1):
            cr.new_path()
            ell(cr, sx * (w + 40), y, 18, 30)
            leather(cr, GOLD, 4)
    band(cr, [(-w + 20, -h + 110), (w - 20, -h + 110)], 6, RED, holes=False)


def _quill(cr):
    """A feather pen; the nib tip is the pivot (0, 0), the feather rises up and to the right."""
    vane = [(10, -20), (40, -110), (90, -220), (140, -290), (128, -230), (96, -150), (56, -70), (24, -18)]
    _shape(cr, vane, PALE, 4)
    for k in range(6):
        y = -60 - 36 * k
        ink(cr, [(20 + 20 * k, y + 20), (46 + 22 * k, y - 4)], 2, col=OCHRE)
    ink(cr, [(0, 0), (130, -280)], 3.5)
    _shape(cr, [(0, 0), (6, -26), (16, -22)], INK, 2, smooth=False)


def _garland(cr):
    """A marigold garland hanging in a U (pivot at the top centre), a red tassel at the bottom."""
    pts = []
    for i in range(23):
        u = i / 22
        a = math.pi * u
        pts.append((-78 * math.cos(a), 190 * math.sin(a) ** 1.2))
    for i, (x, y) in enumerate(pts):
        r = 17 if i % 2 == 0 else 14
        star = []
        for k in range(16):
            aa = 2 * math.pi * k / 16
            rr = r if k % 2 == 0 else r * 0.74
            star.append((x + rr * math.cos(aa), y + rr * math.sin(aa)))
        _shape(cr, star, GOLD if i % 3 else SAFFRON, 2.5, smooth=False)
        punch(cr, [(x, y)], 3)
    _shape(cr, [(-12, 196), (12, 196), (18, 250), (0, 240), (-18, 250)], RED, 3, smooth=False)


def _vow(cr):
    """The promise: a rolled palm-leaf bundle tied with red thread, a seal (centre pivot)."""
    _shape(cr, [(-110, -26), (110, -26), (118, 0), (110, 26), (-110, 26), (-118, 0)], LEAF, 5)
    for x in (-90, 90):
        cr.new_path()
        ell(cr, x, 0, 12, 26)
        leather(cr, LEAF2, 3)
    band(cr, [(-14, -30), (-14, 30)], 10, RED, holes=False)
    band(cr, [(14, -30), (14, 30)], 10, RED, holes=False)
    cr.new_path()
    cr.arc(0, 30, 20, 0, 2 * math.pi)
    leather(cr, DRED, 4)
    _flower(cr, 0, 30, 12, GOLD, 6)


def _drum(cr):
    """A nagara kettle drum (pivot at the bottom centre)."""
    bowl = [(-130, -150), (130, -150), (120, -90), (90, -30), (40, 0), (-40, 0), (-90, -30), (-120, -90)]
    _shape(cr, bowl, (0.56, 0.20, 0.10), 6)
    for k in range(9):                                                            # lacing
        x0 = -112 + 28 * k
        ink(cr, [(x0, -146), (x0 * 0.4 + 14, -10)], 3, smooth=False, col=GOLD)
    cr.new_path()
    ell(cr, 0, -150, 138, 26)
    leather(cr, PALE, 6)
    band(cr, [(-134, -136), (134, -136)], 12, GOLD, spacing=12, hole_r=2.2)


def _throne(cr):
    """The throne of Ayodhya (pivot at the bottom centre): steps, seat, cushion, a tall arched back, lion arms."""
    for y0, w, col in ((0, 290, WOOD), (-40, 250, OCHRE)):
        _shape(cr, [(-w, y0), (w, y0), (w - 10, y0 - 40), (-w + 10, y0 - 40)], col, 6, smooth=False,
               holes=(9, 15, 3))
    back = [(-200, -200), (-210, -420), (-180, -540), (-110, -620), (0, -660), (110, -620), (180, -540),
            (210, -420), (200, -200)]
    _shape(cr, back, RED, 7, holes=(14, 17, 3.2))
    dots_in(cr, lambda: spath(cr, [(-150, -260), (-160, -420), (-90, -560), (0, -600), (90, -560), (160, -420),
                                   (150, -260)]), 24, 3.6, shape="d")
    _flower(cr, 0, -470, 54, GOLD, 8)
    seat = [(-230, -80), (230, -80), (236, -200), (-236, -200)]
    _shape(cr, seat, GOLD, 7, smooth=False, holes=(11, 15, 3))
    cush = [(-200, -200), (200, -200), (210, -232), (190, -250), (-190, -250), (-210, -232)]
    _shape(cr, cush, (0.34, 0.46, 0.86), 5)
    band(cr, [(-196, -214), (196, -214)], 10, GOLD, spacing=12, hole_r=2)
    for sx in (-1, 1):                                                            # lion arm rests
        x = sx * 250
        _shape(cr, [(x - 40, -80), (x + 40, -80), (x + 44, -280), (x - 44, -280)], OCHRE, 6, smooth=False)
        cr.new_path()
        cr.arc(x, -320, 58, 0, 2 * math.pi)
        leather(cr, SAFFRON, 6)
        for k in range(10):
            a = 2 * math.pi * k / 10
            punch(cr, [(x + 44 * math.cos(a), -320 + 44 * math.sin(a))], 4)
        _flower(cr, x, -320, 30, GOLD, 8)


def _paduka(cr):
    """Rama's wooden sandals, a pair standing side by side, frontal (pivot at the bottom centre)."""
    for sx in (-1, 1):
        x = sx * 54
        sole = [(x - 30, 0), (x + 30, 0), (x + 40, -60), (x + 42, -130), (x + 30, -176), (x, -192), (x - 30, -176),
                (x - 42, -130), (x - 40, -60)]
        _shape(cr, sole, WOOD, 5)
        band(cr, [(x - 34, -24), (x + 34, -24)], 10, GOLD, spacing=10, hole_r=2)
        holes_line(cr, [(x - 30, -60), (x - 32, -140), (x, -176), (x + 32, -140), (x + 30, -60)], 14, 2.4)
        cr.new_path()
        cr.arc(x, -136, 16, 0, 2 * math.pi)
        leather(cr, GOLD, 4)
        punch(cr, [(x, -136)], 5)
        _flower(cr, x, -76, 14, RED, 6)


def _map(cr):
    """A cloth map: Kekaya's hills in the north-west, Ayodhya in the plains to the south-east, rivers between."""
    cloth = [(-460, -330), (460, -330), (468, 320)]
    for i in range(12):
        x = 468 - 936 * (i + 0.5) / 12
        cloth.append((x, 346 if i % 2 == 0 else 322))
    cloth += [(-468, 320)]
    _shape(cr, cloth, PARCH, 7, smooth=False, holes=(14, 17, 3.2))
    land = [(-410, -270), (-150, -300), (120, -280), (400, -230), (420, 0), (390, 230), (160, 280), (-80, 250),
            (-300, 280), (-420, 160), (-430, -60)]
    _shape(cr, land, R.LAND, 5, holes=(10, 15, 2.6))
    for x, y, s in ((-360, -200, 1.0), (-290, -230, 1.3), (-220, -190, 0.9), (-380, -110, 0.8), (-140, -230, 0.8),
                    (60, -240, 0.7)):
        _shape(cr, [(x - 44 * s, y + 34 * s), (x, y - 44 * s), (x + 44 * s, y + 34 * s)], OCHRE, 3.5, smooth=False)
        _shape(cr, [(x - 14 * s, y - 22 * s), (x, y - 44 * s), (x + 14 * s, y - 22 * s), (x, y - 30 * s)],
               (1, 1, 1), 2, smooth=False)
    for pts in (((-330, -60), (-200, 10), (-60, 0), (80, 60), (220, 40), (330, 120), (400, 200)),
                ((-180, -170), (-120, -80), (-60, 0)), ((40, -170), (60, -60), (80, 60))):
        ink(cr, pts, 9, col=INK)
        ink(cr, pts, 5, col=BLUE)
    for x, y in ((150, 160), (190, 200), (-40, 140), (300, -100), (-300, 120), (0, -100)):
        cr.new_path()
        cr.arc(x, y, 15, 0, 2 * math.pi)
        leather(cr, DGREEN, 3)
    band(cr, [(-500, -344), (500, -344)], 24, BROWN, spacing=16)
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 510, -344, 18, 0, 2 * math.pi)
        leather(cr, GOLD, 4)


def _city(cr, col, dome):
    """A small city on the map: a wall with towers and a dome (pivot at the bottom centre)."""
    _shape(cr, [(-70, 0), (70, 0), (70, -50), (-70, -50)], col, 4, smooth=False)
    for x in (-50, -20, 10, 40):
        cut(cr, lambda x=x: poly(cr, [(x, -30), (x + 12, -30), (x + 12, -12), (x, -12)]))
    for x in (-62, 62):
        _shape(cr, [(x - 14, 0), (x + 14, 0), (x + 14, -86), (x - 14, -86)], col, 4, smooth=False)
        _shape(cr, [(x - 16, -86), (x, -110), (x + 16, -86)], RED, 3, smooth=False)
    _shape(cr, [(-34, -50), (-30, -86), (0, -112), (30, -86), (34, -50)], dome, 4)
    poly(cr, [(-3, -112), (0, -134), (3, -112)])
    leather(cr, GOLD, 2.5)


def _point(cr, skin):
    """A pointing arm (elbow at 0, 0, pointing along +x): sleeve band, hand, extended index finger."""
    arm = [(0, -26), (200, -22), (230, -20), (230, 22), (200, 22), (0, 26)]
    _shape(cr, arm, skin, 5, smooth=False)
    band(cr, [(186, -24), (186, 26)], 14, GOLD, spacing=10, hole_r=2)
    hand = [(226, -24), (270, -30), (300, -22), (378, -18), (384, -8), (300, -4), (306, 14), (296, 34), (262, 38),
            (230, 28)]
    _shape(cr, hand, skin, 4)
    ink(cr, [(272, 10), (294, 12)], 2.5)
    ink(cr, [(270, 24), (290, 26)], 2.5)


register("kk_crown", (-130, -230, 130, 10), _crown)
register("kk_leaf", (-280, -52, 280, 74), _leaf)
register("kk_scroll", (-390, -420, 390, 420), _scroll)
register("kk_quill", (-10, -300, 150, 10), _quill)
register("kk_garland", (-100, -24, 100, 260), _garland)
register("kk_vow", (-130, -40, 130, 60), _vow)
register("kk_drum", (-150, -186, 150, 10), _drum)
register("kk_throne", (-300, -670, 300, 10), _throne)
register("kk_paduka", (-110, -200, 110, 10), _paduka)
register("kk_map", (-530, -370, 530, 360), _map)
register("kk_cityA", (-90, -140, 90, 10), lambda cr: _city(cr, OCHRE, GOLD))
register("kk_cityK", (-90, -140, 90, 10), lambda cr: _city(cr, (0.70, 0.58, 0.46), SAFFRON))
for _i, _c in enumerate(((0.99, 0.72, 0.48), (0.86, 0.56, 0.34), (0.95, 0.64, 0.42))):
    register(f"kk_point{_i}", (-10, -50, 390, 50), (lambda c: lambda cr: _point(cr, c))(_c))
