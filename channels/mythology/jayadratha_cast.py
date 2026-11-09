"""The leather cast and props for the Jayadratha reel (videos/jayadratha.py), in the Togalu Gombeyaata style of the
Jarasandha, Kaikeyi, Lakshman Rekha and Mandhata reels (puppet_cast, kaikeyi_cast, lrekha_cast, mandhata_cast): profile
figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor
and no film.

Cast (one look each, kept the same through the video):
  KRISHNA        puppet_cast.KRISHNA, as in the Jarasandha reel: blue skin, a peacock feather in his hair knot, a gold
                 dhoti with a red border, a green sash. Here he is Arjuna's charioteer (a whip, the reins); calm.
  ARJUNA         the warrior: warm skin, a black moustache, a gold kirita with a red flare (he is "Kiriti", the crowned
                 one), a cream dhoti with a red border and sash (his colours in the Jarasandha reel), a quiver on his
                 back and the bow Gandiva (a big gold recurved bow with a red grip).
  JAYADRATHA     king of Sindhu: darker tan skin, a curled moustache and a short pointed beard, a gold FAN crown of five
                 peaks with teal jewels and a teal plume, a dark teal flame halo, a maroon dhoti with a gold border and
                 a teal sash. Distinct from every other king in the channel.
  VRIDDHAKSHATRA his old father, now an ascetic: white hair and a long white beard, a white top-knot with a rudraksha
                 string, ash lines on the forehead, a saffron dhoti and ochre robe with beads. Sits cross-legged in
                 prayer (eyes closed, jd_vk_seat legs, pleats tucked under) or stands.
  ABHIMANYU      the young warrior (only small, in the chakravyuha): no moustache, a small gold kirita with a green
                 flare, a green dhoti and a red sash.
  SOLDIERS       the Kaurava army: one repeated figure, an iron helmet with a spike and a neck guard, a brown dhoti
                 with a dark-red border, a spear and a round shield.
Props: the chariot (a gold car on a big spoked wheel, a yoke pole, a flagstaff with a saffron pennant), two white
horses (near and far), the bow Gandiva (strung / unstrung for the pulled string), an arrow, a whip, a spear, a round
shield, the funeral pyre (stacked logs), the dark disc of yoga-maya (a dark leather disc with a spiral of punched
holes), Jayadratha's fan crown and a small kirita on their own (the two crowns that fall in the hook). The sun, moon,
trees, altar fire, palm-leaf book, torn note, speech cloud, leaf hut and straw mat come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man().
"""
import math
import random

import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the leaf hut, palm-leaf book, speech cloud)
import mandhata_cast as M
import puppet_cast as C
import ravana_cast as R
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, RED, SAFFRON, band, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, rivet, spath)

AR_SKIN = (0.98, 0.76, 0.50)          # Arjuna
JD_SKIN = (0.86, 0.58, 0.36)          # Jayadratha
JD_DHOTI = (0.56, 0.14, 0.30)         # maroon
JD_TEAL = (0.10, 0.54, 0.58)
JD_HALO = (0.08, 0.36, 0.40)
AB_SKIN = (1.0, 0.82, 0.60)           # Abhimanyu
SD_SKIN = (0.78, 0.50, 0.30)          # the Kaurava soldiers
SD_DHOTI = (0.62, 0.40, 0.20)
STEEL = (0.50, 0.50, 0.58)
STEEL2 = (0.72, 0.72, 0.80)
VK_SKIN = K.DS_SKIN                   # Vriddhakshatra
ASH = K.ASH
ASH2 = K.ASH2
HORSE = (1.0, 0.92, 0.76)
HORSE2 = (0.86, 0.76, 0.60)
MANE = (0.95, 0.66, 0.20)
MAYA = (0.19, 0.16, 0.26)             # the dark disc of yoga-maya
MAYA2 = (0.33, 0.27, 0.44)
WOOD = K.WOOD
LOG = (0.50, 0.30, 0.13)
LOG2 = (0.74, 0.50, 0.24)

DECK = 300.0                          # the chariot: deck (the riders' soles) above the ground, design units
WHEEL_R = 250.0
WHEEL_XY = (-20.0, -250.0)
HORSE_DX = 760.0                      # chariot pivot to the near horse's pivot
LAP = (128.0, -40.0)                  # Vriddhakshatra seated: his lap, in hip coordinates
SEAT_H = 96.0                         # seated: hip above the ground (design units)

# ------------------------------------------------------------------ Arjuna


_AR_O = dict(skin=AR_SKIN, crown="tiara", hair=True, halo=False, moustache=True, tilak=True)


def arjuna_head(cr):
    """Arjuna: long hair, a black moustache, a gold kirita with a red flare and a blue jewel."""
    C.man_head(cr, _AR_O)
    R.kirita(cr, GOLD, None, tall=1.08, flare=RED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.08, 9, (0.16, 0.42, 0.96))


ARJUNA = man("jd_arjuna", skin=AR_SKIN, bulk=1.05, dhoti=PALE, border=RED, pleat=RED, sash=RED, neck=GOLD,
             crown="tiara", halo=False, thread=True, moustache=True, hands=("fist", "fist"))
register("jd_arjuna_head", (-200, -440, 120, 110), arjuna_head)
register("jd_arjuna_quiver", (-50, -110, 50, 250), K._quiver)
ARJUNA.parts.insert(0, ("jd_arjuna_quiver", "jd_arjuna_body", (-30, -250), 0.55))


def _gandiva(cr, string=True):
    """The bow Gandiva (grip at 0, 0; the belly bulges to +x, the string at x = -90): gold limbs with holes, recurved
    tips, a red grip, small jewels."""
    cr.new_path()
    cr.move_to(-90, -340)
    cr.curve_to(40, -220, 40, 220, -90, 340)
    cr.set_line_cap(1)
    cr.set_source_rgb(*INK)
    cr.set_line_width(30)
    cr.stroke_preserve()
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(19)
    cr.stroke()
    holes_line(cr, [(-74, -300), (-20, -200), (2, -90)], 22, 2.6)
    holes_line(cr, [(-74, 300), (-20, 200), (2, 90)], 22, 2.6)
    for s in (-1, 1):                                                            # recurved tips
        for w, col in ((16, INK), (8, GOLD)):
            cr.new_path()
            spath(cr, [(-90, s * 338), (-70, s * 376), (-36, s * 384)], closed=False)
            cr.set_source_rgb(*col)
            cr.set_line_width(w)
            cr.stroke()
        _jewel(cr, -40, s * 150, 9, RED)
    band(cr, [(8, -46), (8, 46)], 28, RED, spacing=10, hole_r=2.0)
    _jewel(cr, 10, 0, 8, GOLD)
    if string:
        ink(cr, [(-88, -338), (-88, 338)], 3.0, smooth=False)


register("jd_gandiva", (-110, -400, 60, 400), lambda cr: _gandiva(cr, True))
register("jd_gandiva_bare", (-110, -400, 60, 400), lambda cr: _gandiva(cr, False))


def _arrow(cr):
    """An arrow pointing +x (pivot at the nock, the tip at x = 350)."""
    ink(cr, [(6, 0), (300, 0)], 12, smooth=False)
    ink(cr, [(6, 0), (300, 0)], 6, smooth=False, col=GOLD)
    _shape(cr, [(292, -18), (356, 0), (292, 18), (304, 0)], STEEL2, 4, smooth=False)
    for s in (-1, 1):
        _shape(cr, [(4, 0), (20, s * 22), (74, s * 22), (60, 0)], RED, 3, smooth=False)
    band(cr, [(80, 0), (100, 0)], 8, GOLD, holes=False)


register("jd_arrow", (-10, -32, 366, 32), _arrow)

# ------------------------------------------------------------------ Krishna's whip


def _whip(cr):
    """A charioteer's whip (grip at 0, 0): a thin stick and a curling cord."""
    ink(cr, [(0, 40), (2, -250)], 11, smooth=False)
    ink(cr, [(0, 40), (2, -250)], 6, smooth=False, col=BROWN)
    band(cr, [(0, 30), (0, -30)], 14, RED, spacing=9, hole_r=1.8)
    ink(cr, [(2, -250), (40, -300), (100, -296), (122, -240), (96, -196), (64, -214), (70, -250)], 4)
    _flower(cr, 2, -256, 12, GOLD, 6)


register("jd_whip", (-30, -330, 140, 60), _whip)

# ------------------------------------------------------------------ Jayadratha


def _petal(cr, x0, y0, length, w, a, col, holes=None):
    ux, uy = math.sin(a), -math.cos(a)
    px, py = math.cos(a), math.sin(a)
    P = lambda s_, t_: (x0 + ux * t_ + px * s_, y0 + uy * t_ + py * s_)
    _shape(cr, [P(0, 0), P(w, length * 0.38), P(w * 0.62, length * 0.82), P(0, length), P(-w * 0.62, length * 0.82),
                P(-w, length * 0.38)], col, 4, holes=holes)
    return P(0, length * 0.7)


def jaya_crown(cr, plume=True):
    """Jayadratha's fan crown (head coordinates): five gold peaks spreading like a fan from a jewelled band, teal
    jewels, a teal plume sweeping back."""
    if plume:
        pl = [(-40, -196), (-92, -276), (-150, -330), (-182, -322), (-136, -268), (-84, -214), (-56, -184)]
        _shape(cr, pl, JD_TEAL, 4)
        holes_line(cr, [(-54, -206), (-104, -270), (-152, -314)], 13, 2.4)
    for x0, a, ln in ((-34, -0.78, 112), (34, 0.78, 112), (-18, -0.40, 146), (18, 0.40, 146), (0, 0.0, 178)):
        tip = _petal(cr, x0 + 3, -160, ln, 30 if ln < 170 else 34, a, GOLD, holes=(8, 11, 2.2))
        _jewel(cr, tip[0], tip[1], 8 if ln < 170 else 11, JD_TEAL)
    band(cr, [(-54, -160), (0, -168), (60, -158)], 22, GOLD, spacing=11, hole_r=2.4)
    _jewel(cr, 4, -164, 10, RED)
    for x in (-34, 40):
        _jewel(cr, x, -163, 6, JD_TEAL)


_JD_O = dict(skin=JD_SKIN, crown="tiara", hair=True, halo=False, moustache=True, tilak=True)


def jaya_head(cr):
    """Jayadratha: a dark teal flame halo, long hair, a curled moustache, a short pointed beard, the fan crown."""
    K._halo(cr, JD_HALO)
    C.man_head(cr, _JD_O)
    _shape(cr, [(60, -52), (64, -28), (56, 2), (40, 36), (28, 14), (18, -20), (32, -48)], HAIR, 4)
    ink(cr, [(28, -88), (10, -86), (2, -98), (12, -108)], 4.5, col=HAIR)
    jaya_crown(cr)


JAYA = man("jd_jaya", skin=JD_SKIN, bulk=1.12, dhoti=JD_DHOTI, border=GOLD, pleat=GOLD, sash=JD_TEAL, neck=GOLD,
           crown="tiara", halo=False, moustache=True, hands=("open", "open"))
register("jd_jaya_head", (-230, -400, 130, 110), jaya_head)


def _crown_a(cr):
    cr.translate(0, 248)
    jaya_crown(cr, plume=False)


def _crown_b(cr):
    cr.translate(0, 270)
    R.kirita(cr, GOLD, None, tall=0.9, flare=DRED)


register("jd_crown_a", (-150, -110, 150, 110), _crown_a)
register("jd_crown_b", (-120, -110, 80, 140), _crown_b)

# ------------------------------------------------------------------ Abhimanyu


_AB_O = dict(skin=AB_SKIN, crown="tiara", hair=True, halo=False, tilak=True)


def abhi_head(cr):
    C.man_head(cr, _AB_O)
    R.kirita(cr, GOLD, None, tall=0.78, flare=GREEN)


ABHI = man("jd_abhi", skin=AB_SKIN, bulk=0.9, dhoti=GREEN, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
           crown="tiara", halo=False, thread=True, hands=("fist", "fist"))
register("jd_abhi_head", (-200, -400, 120, 110), abhi_head)

# ------------------------------------------------------------------ the Kaurava soldiers


def helmet(cr):
    """An iron helmet (head coordinates): a dome with a gold band and spike, a short neck guard."""
    guard = [(-50, -140), (-70, -128), (-74, -96), (-52, -92), (-44, -118)]
    _shape(cr, guard, STEEL, 4)
    dome = [(-58, -132), (-58, -172), (-38, -206), (0, -222), (38, -208), (58, -178), (64, -136)]
    _shape(cr, dome, STEEL, 5, holes=(10, 13, 2.4))
    band(cr, [(-62, -140), (66, -138)], 14, GOLD, spacing=11, hole_r=2.2)
    poly(cr, [(-7, -218), (0, -270), (7, -218)])
    leather(cr, GOLD, 3)
    _jewel(cr, 2, -176, 8, RED)


_SD_O = dict(skin=SD_SKIN, crown="tiara", hair=False, halo=False, moustache=True, tilak=False, earring=False)


def soldier_head(cr):
    C.man_head(cr, _SD_O)
    helmet(cr)


SOLDIER = man("jd_soldier", skin=SD_SKIN, bulk=1.0, dhoti=SD_DHOTI, border=DRED, pleat=DRED, sash=DRED, neck=BROWN,
              crown="tiara", halo=False, moustache=True, hands=("fist", "fist"))
register("jd_soldier_head", (-120, -290, 110, 30), soldier_head)


def _spear(cr):
    """A spear (grip at 0, 0): a wooden shaft, a leaf-shaped iron blade, a red tassel."""
    ink(cr, [(0, 230), (0, -400)], 13, smooth=False)
    ink(cr, [(0, 230), (0, -400)], 7, smooth=False, col=WOOD)
    _shape(cr, [(0, -520), (20, -456), (15, -414), (0, -400), (-15, -414), (-20, -456)], STEEL2, 4, smooth=False)
    ink(cr, [(0, -506), (0, -412)], 2.2, smooth=False)
    for k in (-1, 0, 1):
        ink(cr, [(0, -396), (k * 12, -344)], 4.5, col=RED)
    band(cr, [(0, -400), (0, -380)], 14, GOLD, holes=False)


def _shield(cr):
    """A round shield (centre pivot): leather with a gold boss and studs."""
    cr.new_path()
    cr.arc(0, 0, 78, 0, 2 * math.pi)
    leather(cr, OCHRE, 5)
    cr.new_path()
    cr.arc(0, 0, 60, 0, 2 * math.pi)
    leather(cr, BROWN, 3)
    for i in range(8):
        a = 2 * math.pi * i / 8
        _jewel(cr, 44 * math.cos(a), 44 * math.sin(a), 6, GOLD)
    cr.new_path()
    cr.arc(0, 0, 20, 0, 2 * math.pi)
    leather(cr, GOLD, 3)
    punch(cr, [(0, 0)], 5)


register("jd_spear", (-30, -530, 30, 240), _spear)
register("jd_shield", (-86, -86, 86, 86), _shield)

# ------------------------------------------------------------------ Vriddhakshatra


def vk_head(cr, shut=False):
    """The old father: Dasharatha's white hair and beard (no crown), a white top-knot tied with rudraksha beads, three
    ash lines on the forehead; shut = eyes closed in prayer."""
    K.dasharatha_head(cr, crown=False)
    cr.new_path()
    ell(cr, -20, -214, 40, 26, -0.2)
    leather(cr, ASH, 4)
    ink(cr, [(-50, -214), (-20, -226), (10, -218)], 2.5, col=ASH2)
    for i in range(6):
        cr.new_path()
        cr.arc(-48 + 14 * i, -192 + 2 * math.sin(i), 5.5, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    for k in range(3):
        ink(cr, [(4, -168 + 9 * k), (46, -170 + 9 * k)], 3, col=(1.0, 0.97, 0.9))
    if shut:
        M._sleep_eye(cr, VK_SKIN)


_VK = dict(skin=VK_SKIN, bulk=0.92, dhoti=SAFFRON, border=DRED, pleat=DRED, sash=OCHRE, neck=BROWN, robe=OCHRE,
           beads=True)
VK = man("jd_vk", crown="tiara", hair=False, halo=False, earring=False, hands=("open", "open"), tilak=False, **_VK)
register("jd_vk_head", (-200, -270, 120, 170), vk_head)
register("jd_vk_head_pray", (-200, -270, 120, 170), lambda cr: vk_head(cr, True))


def _vk_body_sit(cr):
    """His body with the front pleats tucked away (they would hang into the ground when he sits)."""
    cr.save()
    cr.rectangle(-400, -600, 800, 664)
    cr.clip()
    C.man_body(cr, _VK)
    cr.restore()


def _vk_seat(cr):
    """Cross-legged in profile (hip at 0, 0; the ground at y = +SEAT_H): the folded thighs in front, the near foot
    tucked sole-up on top."""
    th = [(-80, -30), (40, -44), (160, -32), (250, -10), (266, 40), (250, 86), (120, 96), (-40, 96), (-92, 70),
          (-96, 14)]
    _shape(cr, th, SAFFRON, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(246, -8), (266, 40), (250, 86)], 14, DRED, spacing=11, hole_r=2.4)
    band(cr, [(-84, 88), (240, 90)], 10, DRED, holes=False)
    foot = [(104, 8), (150, -6), (204, 0), (222, 22), (196, 38), (118, 40)]
    _shape(cr, foot, VK_SKIN, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 4), (x + 4, 18)], 2.2)
    band(cr, [(112, 14), (112, 38)], 8, GOLD, holes=False)
    rivet(cr, 0, 0, 9)


register("jd_vk_body_sit", (-200, -330, 140, 80), _vk_body_sit)
register("jd_vk_seat", (-110, -60, 280, 110), _vk_seat)

# ------------------------------------------------------------------ the chariot and its horses


def _wheel(cr):
    """A big spoked chariot wheel (centre pivot)."""
    for i in range(10):
        a = 2 * math.pi * i / 10
        band(cr, [(46 * math.cos(a), 46 * math.sin(a)), (224 * math.cos(a), 224 * math.sin(a))], 16, WOOD,
             spacing=30, hole_r=2.2)
    cr.new_path()
    cr.arc(0, 0, WHEEL_R - 14, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(38)
    cr.stroke()
    cr.arc(0, 0, WHEEL_R - 14, 0, 2 * math.pi)
    cr.set_source_rgb(*OCHRE)
    cr.set_line_width(28)
    cr.stroke()
    for i in range(36):
        a = 2 * math.pi * (i + 0.5) / 36
        punch(cr, [((WHEEL_R - 14) * math.cos(a), (WHEEL_R - 14) * math.sin(a))], 3.4)
    for i in range(10):
        a = 2 * math.pi * i / 10
        _jewel(cr, (WHEEL_R - 14) * math.cos(a), (WHEEL_R - 14) * math.sin(a), 7, GOLD)
    cr.new_path()
    cr.arc(0, 0, 54, 0, 2 * math.pi)
    leather(cr, GOLD, 5)
    _flower(cr, 0, 0, 30, RED, 8)
    rivet(cr, 0, 0, 10)


def _chariot_back(cr):
    """The flagstaff at the back of the car (pivot on the ground under the axle) with Arjuna's saffron pennant."""
    band(cr, [(-300, -290), (-300, -1490)], 18, GOLD, spacing=24, hole_r=2.4)
    flag = [(-292, -1484), (-30, -1420), (-110, -1376), (-30, -1330), (-292, -1268)]
    _shape(cr, flag, SAFFRON, 5, smooth=False, holes=(10, 14, 2.6))
    cr.new_path()
    cr.arc(-170, -1376, 34, 0, 2 * math.pi)
    leather(cr, RED, 4)
    _flower(cr, -170, -1376, 22, GOLD, 8)
    cr.new_path()
    cr.arc(-300, -1506, 18, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    poly(cr, [(-306, -1520), (-300, -1560), (-294, -1520)])
    leather(cr, GOLD, 3)


PANEL = [(-330, -300), (246, -300), (304, -362), (334, -470), (326, -598), (288, -644), (254, -604), (244, -526),
         (176, -500), (-224, -500), (-290, -540), (-330, -524)]     # the car's side panel (the riders stand behind it)


def _chariot(cr):
    """The car in front of the riders (pivot on the ground under the axle): the yoke pole to the horses, the deck, a
    gold side panel with a curved prow, a red rail and a lotus medallion."""
    band(cr, [(240, -340), (480, -430), (760, -560)], 24, WOOD, spacing=28, hole_r=2.6)
    _shape(cr, [(730, -600), (790, -600), (796, -540), (724, -540)], GOLD, 4, smooth=False)
    deck = [(-350, -300), (276, -300), (290, -262), (-350, -262)]
    _shape(cr, deck, WOOD, 6, smooth=False, holes=(8, 14, 2.4))
    _shape(cr, PANEL, GOLD, 6, holes=(12, 15, 3))
    dots_in(cr, lambda: poly(cr, [(-300, -330), (220, -330), (230, -470), (-300, -470)]), 24, 3.6, shape="d")
    band(cr, [(-318, -512), (-224, -508), (176, -508), (244, -530)], 18, RED, spacing=13)
    band(cr, [(-340, -310), (270, -310)], 14, RED, holes=False)
    cr.new_path()
    cr.arc(-20, -404, 62, 0, 2 * math.pi)
    leather(cr, RED, 5)
    _flower(cr, -20, -404, 46, GOLD, 8)
    _jewel(cr, -20, -404, 12, (0.16, 0.42, 0.96))
    _flower(cr, 300, -560, 26, RED, 8)


def _horse(cr, col, far=False):
    """A horse in profile facing +x (pivot on the ground under the middle of its body): white leather, a gold mane,
    a red saddle-cloth, a gold breast collar and a red plume."""
    dk = 0.86 if far else 1.0
    c2 = tuple(c * 0.86 for c in col)
    tail = [(-290, -612), (-352, -584), (-404, -484), (-414, -344), (-386, -262), (-362, -330), (-352, -452),
            (-300, -540)]
    _shape(cr, tail, tuple(c * dk for c in MANE), 4)
    holes_line(cr, [(-320, -590), (-380, -480), (-392, -340)], 16, 2.4)

    def fore(x, c):
        p = [(x - 36, -500), (x + 36, -500), (x + 28, -330), (x + 18, -150), (x + 22, -70), (x + 34, -24), (x + 40, 0),
             (x - 16, 0), (x - 14, -30), (x - 18, -90), (x - 22, -160), (x - 30, -330)]
        _shape(cr, p, c, 5)
        band(cr, [(x - 16, -16), (x + 38, -16)], 14, INK, holes=False)
        band(cr, [(x - 22, -150), (x + 20, -150)], 9, GOLD, spacing=8, hole_r=1.8)

    def hind(x, c):
        p = [(x - 64, -530), (x + 52, -530), (x + 40, -400), (x + 12, -300), (x + 30, -200), (x + 24, -80),
             (x + 34, -24), (x + 40, 0), (x - 16, 0), (x - 14, -30), (x - 10, -90), (x - 14, -200), (x - 36, -290),
             (x - 54, -400)]
        _shape(cr, p, c, 5)
        band(cr, [(x - 16, -16), (x + 38, -16)], 14, INK, holes=False)

    hind(-236, c2)
    fore(150, c2)
    body = [(-300, -560), (-288, -622), (-220, -664), (-60, -664), (100, -654), (222, -642), (292, -600), (304, -530),
            (272, -452), (160, -424), (0, -432), (-160, -424), (-262, -452), (-302, -502)]
    _shape(cr, body, col, 6)
    neck = [(170, -626), (232, -726), (302, -826), (362, -884), (420, -904), (452, -872), (432, -802), (384, -722),
            (334, -604), (284, -524)]
    _shape(cr, neck, col, 6)
    head = [(382, -902), (432, -934), (474, -922), (524, -862), (584, -792), (594, -762), (564, -742), (512, -752),
            (462, -792), (412, -830)]
    _shape(cr, head, col, 6)
    _shape(cr, [(402, -912), (412, -976), (434, -918)], col, 4, smooth=False)
    almond_eye_x, almond_eye_y = 456, -872
    cr.new_path()
    ell(cr, almond_eye_x, almond_eye_y, 16, 10, 0.5)
    leather(cr, PALE, 3)
    cr.new_path()
    cr.arc(almond_eye_x + 4, almond_eye_y + 2, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(572, -770)], 5)
    ink(cr, [(560, -752), (536, -748)], 3)
    band(cr, [(448, -900), (500, -800), (560, -760)], 10, RED, spacing=10, hole_r=1.8)          # bridle
    band(cr, [(430, -820), (500, -800)], 8, GOLD, holes=False)
    mane = [(178, -660), (238, -758), (306, -858), (372, -918), (402, -930)]
    band(cr, mane, 30, tuple(c * dk for c in MANE), spacing=12, hole_r=2.6)
    for i in range(7):                                                                       # mane tufts
        u = i / 6
        x = 190 + (390 - 190) * u
        y = -680 - (928 - 680) * u
        _shape(cr, [(x - 12, y), (x - 42, y + 8), (x - 10, y + 24)], tuple(c * dk for c in MANE), 2.5,
               smooth=False)
    _shape(cr, [(410, -930), (392, -1010), (420, -1060), (434, -1000), (428, -930)], RED, 3)  # plume
    cloth = [(-140, -664), (70, -660), (84, -548), (-150, -552)]
    _shape(cr, cloth, RED, 5, smooth=False, holes=(9, 12, 2.4))
    dots_in(cr, lambda: poly(cr, [(-120, -640), (60, -640), (66, -572), (-128, -572)]), 20, 3.0, shape="d")
    band(cr, [(-150, -556), (86, -552)], 14, GOLD, spacing=11, hole_r=2.2)
    band(cr, [(250, -650), (300, -570), (290, -486)], 18, GOLD, spacing=11, hole_r=2.4)       # breast collar
    for y in (-600, -540):
        _jewel(cr, 298, y, 7, RED)
    fore(214, col)
    hind(-196, col)
    holes_line(cr, [(-240, -600), (0, -620), (200, -600)], 26, 3)


register("jd_wheel", (-WHEEL_R - 14, -WHEEL_R - 14, WHEEL_R + 14, WHEEL_R + 14), _wheel)
register("jd_chariot_back", (-330, -1580, -10, -270), _chariot_back)
register("jd_chariot", (-360, -660, 810, -250), _chariot)
register("jd_horse", (-430, -1080, 610, 10), lambda cr: _horse(cr, HORSE))
register("jd_horse_far", (-430, -1080, 610, 10), lambda cr: _horse(cr, HORSE2, True))

# ------------------------------------------------------------------ props


def _maya(cr):
    """The dark disc of yoga-maya (centre pivot): dark leather with a slow spiral of punched holes and a perforated
    rim; it hides the sun but lets a few points of light through."""
    cr.new_path()
    cr.arc(0, 0, 226, 0, 2 * math.pi)
    leather(cr, MAYA, 7)
    cr.new_path()
    cr.arc(0, 0, 186, 0, 2 * math.pi)
    cr.set_source_rgb(*MAYA2)
    cr.set_line_width(14)
    cr.stroke()
    for i in range(40):
        a = 0.46 * i
        r = 24 + 4.0 * i
        punch(cr, [(r * math.cos(a), r * math.sin(a))], 2.4 + 0.04 * i)
    for i in range(30):
        a = 2 * math.pi * (i + 0.5) / 30
        punch(cr, [(208 * math.cos(a), 208 * math.sin(a))], 3.6)


def _pyre(cr):
    """A funeral pyre (pivot at the bottom centre): long logs stacked in rows, crossing rows showing their ends."""
    rng = random.Random(5)
    rows = ((0, 560), (1, 500), (2, 430), (3, 350), (4, 260))
    for row, w in rows:
        y = -row * 54
        if row % 2 == 0:
            for k, dy in enumerate((0, -27)):
                lg = [(-w / 2, y + dy - 2), (w / 2, y + dy - 2), (w / 2 + 6, y + dy - 26), (-w / 2 - 6, y + dy - 26)]
                _shape(cr, lg, LOG if k == 0 else tuple(c * 1.12 for c in LOG), 4, smooth=False)
                ink(cr, [(-w / 2 + 30, y + dy - 14), (w / 2 - 40, y + dy - 12)], 2.2, col=LOG2)
            for x in (-w / 2, w / 2):
                cr.new_path()
                ell(cr, x, y - 26, 13, 26)
                leather(cr, LOG2, 3)
        else:
            n = int(w / 56)
            for i in range(n):
                x = -w / 2 + 28 + i * (w - 56) / max(1, n - 1)
                cr.new_path()
                cr.arc(x + rng.uniform(-4, 4), y - 27, 25, 0, 2 * math.pi)
                leather(cr, LOG2, 4)
                for r in (14, 6):
                    cr.new_path()
                    cr.arc(x, y - 27, r, 0, 2 * math.pi)
                    cr.set_source_rgb(*LOG)
                    cr.set_line_width(2.5)
                    cr.stroke()


register("jd_maya", (-240, -240, 240, 240), _maya)
register("jd_pyre", (-300, -290, 300, 10), _pyre)
