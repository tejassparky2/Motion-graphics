"""The leather cast and props for the Shani and Ganesha reel (videos/shani_ganesha.py), in the Togalu Gombeyaata style
of the Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha, Arjuna, Ruru and Dharmavyadha reels (puppet_cast,
kaikeyi_cast, lrekha_cast, mandhata_cast, jayadratha_cast, arjuna_cast, ruru_cast, dharmavyadha_cast): profile figures
with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no
film. Every sprite name starts with "sg_".

Cast (one look each, kept the same through the video; every deity with dignity and beauty):
  SHANI DEV   deep indigo-blue skin, a tall gold kirita with a blue flare and a blue sapphire (neelam, his stone) in
              front of a blue flame halo, long black hair, a gold tilak, a dark-blue dhoti whose punched dots let the
              lamp through like stars, a gold border, an iron-grey sash; his iron staff with gold bands (a cane to
              his chest), his crow beside him. His eyes are always lowered: faces down (lids lowered, calm), sad
              (lowered, a sad brow), shut (meditating), glance (the lid half down, the eye turned to its front corner),
              speak. Pale lines (brow, lid) so his features read on the dark leather. Sits cross-legged to meditate.
  HIS WIFE    the Gandharva princess, daughter of King Chitraratha: fair skin, a peacock-blue sari with a gold border
              and a magenta pallu and blouse, a low gold tiara of five small peaks hung with pearls, pearls in her bun,
              long gold jhumkas, a nose ring with a pearl chain, layered necklaces. Faces: open, smile, angry, curse
              (angry, the mouth open).
  PARVATI     radiant and motherly: warm fair skin, a red sari with a gold border and a deep-red pallu, a green blouse,
              a tall tiered gold crown (karanda mukuta) in front of a ring of golden rays, a red bindi and a line of
              sindoor, gold jewellery. Faces: open, smile, laugh (joy, pride), speak, faint (eyes shut), angry.
  GANESHA     the baby (mandhata_cast's frontal baby shapes and limbs, its golden skin), a small gold crown and a red
              tilak dot; afterwards the same baby with a gentle elephant head: big ears with rose-pink insides and gold
              studs, a domed forehead with a gold band and a red tilak, kind eyes, two small tusks, the trunk curling
              to one side, the same gold crown. No wound is ever drawn: the body is never shown without a head (the
              cradle cloth covers the cradle instead).
  SHIVA       only small, as the popular version's silhouette: piled jata and his trident (sg_trishul).
  VISHNU      blue skin, a tall gold kirita in front of a ring of golden rays, the Vaishnava tilak, a yellow
              pitambara with a red border, four arms (the extra pair raised: the Sudarshana chakra and the conch);
              seated (sg_vishnu_seat) on Garuda.
  GARUDA      a large eagle-man bird in flight: a golden feathered body, a pale face with a hooked orange beak, a
              crest of red and gold feathers, a small gold crown, gold anklets and talons, great red-gold-green wings.
  ELEPHANT    a grey elephant asleep, lying with its legs folded, eye shut, trunk curled on the ground; nothing more.
  DEVAS       one repeated figure drawn as a dark silhouette with a halo: a small kirita, a sash.
Sets and props: Mount Kailash (snow peaks), the Kailash court (two carved pillars, a scalloped arch, a mango-leaf
toran, marigold strings, bells), the cradle (back and front) and its cloth, the crow (perched / flying), Shani's
staff, the Sudarshana chakra, the conch, Shiva's trident. The palm-leaf book, plaque cards, speech cloud, thought
bubble, garland, moon, stars and sun come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import dharmavyadha_cast as DV
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
from puppet_cast import HAIR, _flower, _jewel, _shape, fore_arm, man, upper_arm, woman
from puppet_core import (DGREEN, DRED, GOLD, GREEN, INK, PALE, RED, almond_eye, band, dots_in, ell, holes_line, ink,
                         leather, poly, punch, register, rivet, spath)

SH_SKIN = (0.25, 0.30, 0.54)          # Shani: deep indigo-blue
SH_DHOTI = (0.15, 0.19, 0.42)
SH_SASH = (0.62, 0.66, 0.82)          # iron grey-blue
SH_HALO = (0.30, 0.42, 0.86)
SH_LINE = (0.90, 0.84, 0.66)          # pale lines on his dark face
SAPPHIRE = (0.22, 0.40, 0.98)
IRON = (0.40, 0.42, 0.50)
CROW = (0.18, 0.18, 0.23)
CROW2 = (0.40, 0.44, 0.56)
WF_SKIN = (0.99, 0.80, 0.62)          # the Gandharva princess
WF_SARI = (0.10, 0.52, 0.62)          # peacock blue
WF_PALLU = (0.80, 0.16, 0.46)         # magenta
PV_SKIN = (1.0, 0.80, 0.60)           # Parvati
PV_SARI = (0.90, 0.14, 0.10)          # red
PV_PALLU = (0.68, 0.06, 0.08)
PV_CHOLI = (0.16, 0.56, 0.30)
RAY = (1.0, 0.88, 0.46)
BABY = M.BABY_SKIN                    # Ganesha (the same golden skin before and after)
EAR_IN = (1.0, 0.64, 0.58)
IVORY = (1.0, 0.96, 0.84)
VI_SKIN = (0.22, 0.44, 0.96)          # Vishnu
VI_DHOTI = (1.0, 0.84, 0.20)          # pitambara
GA_BODY = (1.0, 0.70, 0.22)           # Garuda
GA_FACE = (1.0, 0.90, 0.76)
GA_BEAK = (0.98, 0.50, 0.12)
GA_RED = (0.88, 0.20, 0.10)
GA_GREEN = (0.18, 0.56, 0.32)
EL = (0.64, 0.64, 0.74)               # the elephant
EL2 = (0.52, 0.52, 0.62)
DV_SKIN = (0.98, 0.84, 0.58)          # the devas (drawn as silhouettes)
SNOW = (0.90, 0.94, 1.0)
SNOW2 = (0.66, 0.76, 0.92)
WOOD = K.WOOD
CLOTH = (0.92, 0.22, 0.18)
CLOTH2 = (1.0, 0.76, 0.26)

STAFF_TOP = (0.0, -470.0)             # where the crow perches on the staff (staff units)
CRADLE_RIM = -330.0                   # the cradle's front rim above the ground (cradle units)
GA_SEAT = (30.0, -180.0)              # Vishnu's hip on Garuda's back (Garuda units)
GA_SHOULDER = (-150.0, -120.0)        # where Garuda's wings join (behind Vishnu)
EL_HEAD = (470.0, -330.0)             # the sleeping elephant's head (elephant units)


def _cover(cr, col, x, y, rx, ry):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    cr.set_source_rgb(*col)
    cr.fill()


# ------------------------------------------------------------------ Shani Dev


_SH_O = dict(skin=SH_SKIN, hair=True, moustache=False, tilak=False, earring=True)


def shani_eyes(cr, mood="down"):
    """His eye and brow, drawn in pale lines so they read on the dark leather. mood: down | sad | shut | glance |
    speak (down, the mouth a little open)."""
    _cover(cr, SH_SKIN, 34, -118, 28, 19)
    _cover(cr, SH_SKIN, 34, -142, 28, 9)
    if mood == "shut":
        ink(cr, [(14, -116), (34, -106), (54, -116)], 4.5, col=SH_LINE)
        for x in (24, 34, 44):
            ink(cr, [(x, -109), (x - 2, -100)], 2.4, col=SH_LINE)
    else:
        glance = mood == "glance"
        lid = -127 if glance else -121                                           # the lid's edge (its middle)
        almond_eye(cr, 34, -116, 44, 15, col=PALE, pupil=False, lw=3.5)
        px, py = (50, -115) if glance else (36, -110)
        cr.new_path()
        cr.arc(px, py, 8.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(px + 2.5, py - 2.5)], 2.2)
        cr.new_path()                                                            # the lowered lid
        cr.move_to(9, -117)
        cr.curve_to(22, -142, 46, -142, 59, -115)
        cr.curve_to(46, lid, 22, lid, 9, -117)
        cr.close_path()
        cr.set_source_rgb(*SH_SKIN)
        cr.fill()
        ink(cr, [(9, -117), (34, lid + 5), (59, -115)], 4.0, col=SH_LINE)
        for x in (20, 30, 40):
            ink(cr, [(x, lid + 6), (x - 2, lid - 1)], 2.0, col=SH_LINE)
    if mood == "sad":
        ink(cr, [(12, -136), (34, -144), (58, -158)], 4.5, col=SH_LINE)
    elif mood == "glance":
        ink(cr, [(12, -142), (34, -146), (58, -140)], 4.5, col=SH_LINE)
        ink(cr, [(8, -150), (2, -138)], 2.4, col=SH_LINE)
    else:
        ink(cr, [(12, -138), (34, -146), (58, -140)], 4.5, col=SH_LINE)
    if mood == "speak":
        cr.new_path()
        ell(cr, 64, -68, 6, 8)
        leather(cr, (0.36, 0.06, 0.08), 2.5)
    else:
        ink(cr, [(68, -70), (58, -68)], 3.2, col=(0.80, 0.46, 0.50))


def shani_head(cr, mood="down"):
    """Shani Dev: a blue flame halo, long black hair, a tall gold kirita with a blue flare and a sapphire, a gold
    tilak; his eyes per mood (shani_eyes)."""
    K._halo(cr, SH_HALO)
    A.face(cr, _SH_O, "calm")
    shani_eyes(cr, mood)
    ink(cr, [(52, -150), (54, -174)], 5, col=GOLD)
    R.kirita(cr, GOLD, None, tall=1.06, flare=SH_HALO)
    _jewel(cr, 4, -150 + (-222 + 150) * 1.06, 14, SAPPHIRE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.06, 9, SAPPHIRE)


_SH = dict(skin=SH_SKIN, bulk=1.06, dhoti=SH_DHOTI, border=GOLD, pleat=GOLD, sash=SH_SASH, neck=GOLD, thread=True)
SHANI = man("sg_shani", crown="tiara", halo=False, hair=False, moustache=False, earring=False, tilak=False,
            hands=("open", "fist"), **_SH)
SH_MOODS = ("down", "sad", "shut", "glance", "speak")
for _m in SH_MOODS:
    register("sg_shani_head" + ("" if _m == "down" else "_" + _m), (-230, -490, 140, 110),
             (lambda m: lambda cr: shani_head(cr, m))(_m))
register("sg_shani_body_sit", (-200, -330, 140, 80), DV._sit_body(_SH))
register("sg_shani_seat", (-110, -60, 280, 110), lambda cr: DV._cross_seat(cr, SH_DHOTI, GOLD, SH_SKIN))


def _staff(cr):
    """Shani's staff (grip at 0, 0): a long iron rod with gold bands, a gold knob and a flat perch on top."""
    band(cr, [(0, 420), (0, -420)], 20, IRON, spacing=24, hole_r=2.6)
    for y in (-330, -170, 0, 170, 330):
        band(cr, [(-13, y), (13, y)], 12, GOLD, holes=False)
    cr.new_path()
    ell(cr, 0, -436, 30, 26)
    leather(cr, GOLD, 4)
    _jewel(cr, 0, -436, 9, SAPPHIRE)
    _shape(cr, [(-44, -462), (44, -462), (36, -476), (-36, -476)], GOLD, 4, smooth=False)


def _crow(cr, fly=False):
    """Shani's crow in profile facing +x, feet at (0, 0): black with blue-grey feather lines, a pale eye ring."""
    if not fly:
        for dx in (-10, 14):
            ink(cr, [(dx, -96), (dx + 2, -40), (dx, 0)], 7, smooth=False, col=INK)
            for tx in (-22, 0, 24):
                ink(cr, [(dx, 0), (dx + tx, 3)], 5, smooth=False, col=INK)
    tail = [(-150, -120), (-250, -70), (-262, -50), (-236, -46), (-140, -92)]
    _shape(cr, tail, CROW, 5)
    for k in range(3):
        ink(cr, [(-150, -104 + 6 * k), (-244, -62 + 6 * k)], 2.2, col=CROW2)
    body = [(-160, -110), (-90, -170), (0, -200), (70, -210), (110, -190), (120, -150), (90, -100), (20, -80),
            (-80, -82)]
    _shape(cr, body, CROW, 6)
    if fly:                                                                      # wings up
        for k, (dx, col) in enumerate(((-30, CROW2), (0, CROW))):
            w = [(dx + 40, -170), (dx - 20, -260), (dx - 90, -340), (dx - 170, -390), (dx - 150, -330),
                 (dx - 200, -330), (dx - 150, -270), (dx - 180, -250), (dx - 100, -200), (dx - 20, -150)]
            _shape(cr, w, col if k else (0.26, 0.28, 0.34), 5)
            holes_line(cr, [(dx - 10, -190), (dx - 90, -290), (dx - 150, -350)], 16, 2.4)
    else:
        wing = [(-150, -112), (-60, -160), (40, -170), (90, -140), (40, -110), (-60, -96)]
        _shape(cr, wing, (0.24, 0.25, 0.31), 5)
        for k in range(4):
            ink(cr, [(-20 + 28 * k, -150), (-100 + 22 * k, -108)], 2.4, col=CROW2)
        holes_line(cr, [(-120, -116), (-30, -146), (60, -150)], 16, 2.4)
    head = [(70, -200), (90, -244), (130, -262), (170, -248), (186, -220), (170, -192), (126, -180)]
    _shape(cr, head, CROW, 5)
    beak = [(176, -238), (250, -222), (178, -208)]
    _shape(cr, beak, (0.34, 0.34, 0.40), 4, smooth=False)
    ink(cr, [(180, -223), (240, -222)], 2.2, smooth=False, col=CROW2)
    cr.new_path()
    cr.arc(144, -230, 10, 0, 2 * math.pi)
    leather(cr, SH_LINE, 2.5)
    cr.new_path()
    cr.arc(146, -230, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(148, -232)], 1.6)


register("sg_staff", (-60, -500, 60, 440), _staff)
register("sg_crow", (-275, -280, 260, 14), lambda cr: _crow(cr))
register("sg_crow_fly", (-275, -410, 260, 14), lambda cr: _crow(cr, True))


# ------------------------------------------------------------------ the Gandharva princess


def _face_w(cr, skin):
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, skin, 6)


def _w_eyes(cr, skin, mood):
    """A woman's eye, brow and mouth: open | smile | laugh | speak | faint (shut) | angry | curse."""
    if mood in ("smile", "laugh"):
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5)
    elif mood == "faint":
        RU._cover(cr, skin, 30, -112, 19, 13)
        ink(cr, [(14, -112), (30, -104), (46, -112)], 4)
        for x in (22, 30, 38):
            ink(cr, [(x, -107), (x - 2, -100)], 2.2)
        ink(cr, [(12, -128), (30, -132), (48, -140)], 3.5)
    elif mood in ("angry", "curse"):
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(8, -136), (30, -130), (52, -118)], 6)
    else:
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
    if mood == "smile":
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    elif mood in ("laugh", "speak", "curse"):
        cr.new_path()
        ell(cr, 59, -71, 6, 7 if mood != "laugh" else 6)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
        if mood == "laugh":
            ink(cr, [(52, -78), (60, -70), (66, -76)], 2.5, col=RED)
    elif mood == "angry":
        ink(cr, [(64, -70), (54, -72)], 3.5, col=RED)
    else:
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)


def wife_head(cr, mood="open"):
    """The Gandharva princess: pearls in her bun, a low gold tiara of five small peaks with pearl drops, long gold
    jhumkas, a nose ring with a pearl chain, a bindi."""
    _face_w(cr, WF_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(10):                                                          # pearls round the bun
        a = math.pi * (0.3 + 1.5 * i / 9)
        cr.new_path()
        cr.arc(-62 + 40 * math.cos(a), -128 + 40 * math.sin(a), 6, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _flower(cr, -62, -128, 15, WF_PALLU)
    pts = [(-36, -168), (-30, -196), (-18, -180), (-6, -208), (6, -184), (18, -214), (28, -186), (38, -204),
           (44, -172)]
    _shape(cr, pts, GOLD, 4, smooth=False, holes=(6, 10, 2.0))
    for x, y in ((-30, -190), (-6, -200), (18, -206), (38, -196)):
        cr.new_path()
        cr.arc(x, y + 22, 4.5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _jewel(cr, 18, -186, 7, WF_PALLU)
    _w_eyes(cr, WF_SKIN, mood)
    cr.new_path()
    cr.arc(46, -148, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()                                                                # nose ring and its pearl chain
    cr.arc(64, -90, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    for i in range(7):
        u = i / 6
        cr.new_path()
        cr.arc(60 - 70 * u, -86 + 4 * math.sin(math.pi * u) * 6, 3, 0, 2 * math.pi)
        leather(cr, PALE, 1.5)
    _jewel(cr, -10, -70, 9, GOLD)                                                # the jhumka: a dome and pearls
    _shape(cr, [(-26, -58), (-10, -66), (6, -58), (10, -34), (-30, -34)], GOLD, 3, smooth=False)
    for x in (-24, -10, 4):
        cr.new_path()
        cr.arc(x, -26, 4, 0, 2 * math.pi)
        leather(cr, PALE, 1.5)


def _wife_extra(cr):
    """Layered gold necklaces with pearls and a magenta pendant."""
    band(cr, [(-20, -282), (14, -226), (42, -184)], 8, GOLD, spacing=10, hole_r=1.8)
    for i in range(9):
        u = i / 8
        cr.new_path()
        cr.arc(-26 + 60 * u, -274 + 120 * u + 20 * u * u, 5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _jewel(cr, 36, -134, 11, WF_PALLU)


WIFE = woman("sg_wife", skin=WF_SKIN, skirt=WF_SARI, choli=WF_PALLU, border=GOLD, pallu_col=WF_PALLU, gem=WF_PALLU,
             ornaments_extra=_wife_extra, hands=("open", "open"))
for _e in ("open", "smile", "angry", "curse"):
    register("sg_wife_head" + ("" if _e == "open" else "_" + _e), (-150, -250, 100, 40),
             (lambda e: lambda cr: wife_head(cr, e))(_e))


# ------------------------------------------------------------------ Parvati


def parvati_crown(cr):
    """A tall tiered gold crown (karanda mukuta) with jewels, pearl strings behind."""
    for k in range(3):
        x = -52 - 9 * k
        for j in range(6):
            cr.new_path()
            cr.arc(x - 2 * j, -150 + 15 * j, 4.5, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    tiers = [(-50, 54, -150, -196), (-42, 46, -196, -238), (-32, 36, -238, -276), (-22, 26, -276, -310)]
    for x0, x1, y0, y1 in tiers:
        _shape(cr, [(x0, y0), (x0 + 6, y1), (x1 - 6, y1), (x1, y0)], GOLD, 5, smooth=False, holes=(7, 11, 2.2))
        band(cr, [(x0 + 4, y0 - 6), (x1 - 4, y0 - 6)], 8, RED, holes=False)
    _shape(cr, [(-14, -310), (0, -352), (18, -310)], GOLD, 4, smooth=False)
    cr.new_path()
    cr.arc(2, -360, 9, 0, 2 * math.pi)
    leather(cr, GOLD, 3)
    for x, y, c in ((2, -222, RED), (2, -258, GREEN), (2, -292, RED), (-34, -176, GREEN), (38, -176, GREEN)):
        _jewel(cr, x, y, 8 if y < -200 else 7, c)


def parvati_head(cr, mood="open"):
    """Parvati: a ring of golden rays, her hair in a bun with jasmine, the tiered gold crown, sindoor in the parting,
    a red bindi, a nose ring and gold earrings."""
    M._ray_halo(cr, -20, -168, 112, 162, 18, (RAY, GOLD))
    _face_w(cr, PV_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    hp = [(-40, -150), (-70, -110), (-84, -40), (-80, 40), (-60, 80), (-44, 30), (-40, -40), (-30, -100)]
    _shape(cr, hp, HAIR, 4)                                                     # hair down her back
    for k in range(3):
        holes_line(cr, [(-50 - 6 * k, -120), (-66 - 4 * k, -40), (-60 - 2 * k, 40)], 15, 2.2)
    for i in range(7):
        _flower(cr, -58 - 8 * math.sin(i), -110 + 26 * i, 8, PALE, 5)
    ink(cr, [(8, -188), (28, -178)], 4, col=RED)
    parvati_crown(cr)
    _w_eyes(cr, PV_SKIN, mood)
    cr.new_path()
    cr.arc(46, -148, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()
    cr.arc(64, -90, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    _jewel(cr, -10, -70, 11, GOLD)
    poly(cr, [(-24, -58), (-10, -66), (4, -58), (8, -34), (-28, -34)])
    leather(cr, GOLD, 3)
    punch(cr, [(-18, -40), (-10, -40), (-2, -40)], 2.2)


def _pv_extra(cr):
    """Layered gold necklaces, a green pendant, a jewelled waist belt."""
    band(cr, [(-22, -282), (12, -220), (40, -176)], 9, GOLD, spacing=10, hole_r=1.8)
    band(cr, [(-28, -276), (4, -180), (30, -120)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 32, -110, 12, GREEN)
    for x in (-26, -2, 22):
        _jewel(cr, x, -22, 7, RED)


PARVATI = woman("sg_parvati", skin=PV_SKIN, skirt=PV_SARI, choli=PV_CHOLI, border=GOLD, pallu_col=PV_PALLU,
                gem=GREEN, ornaments_extra=_pv_extra, hands=("open", "open"))
PV_MOODS = ("open", "smile", "laugh", "speak", "faint", "angry")
for _e in PV_MOODS:
    register("sg_parvati_head" + ("" if _e == "open" else "_" + _e), (-240, -390, 190, 110),
             (lambda e: lambda cr: parvati_head(cr, e))(_e))


# ------------------------------------------------------------------ Ganesha


def _crown_small(cr, y0, w=70):
    """A small gold crown sitting at y0 (three peaks, a red jewel)."""
    pts = [(-w, y0), (-w + 6, y0 - 46), (-w * 0.5, y0 - 30), (-w * 0.25, y0 - 74), (0, y0 - 104), (w * 0.25, y0 - 74),
           (w * 0.5, y0 - 30), (w - 6, y0 - 46), (w, y0)]
    _shape(cr, pts, GOLD, 5, smooth=False, holes=(8, 12, 2.4))
    band(cr, [(-w, y0 - 8), (w, y0 - 8)], 14, RED, spacing=11, hole_r=2.2)
    _jewel(cr, 0, y0 - 46, 11, RED)
    for sx in (-1, 1):
        _jewel(cr, sx * w * 0.56, y0 - 26, 6, GREEN)


def _baby_torso(cr):
    col = BABY
    _shape(cr, M._sym((0, -248), [(-60, -242), (-118, -218), (-150, -176), (-154, -100), (-140, -36), (-118, 6),
                                  (-70, 24)], (0, 30)), col, 7)
    langot = [(-112, -12), (-96, 30), (-50, 56), (0, 66), (50, 56), (96, 30), (112, -12), (0, -14)]
    cr.new_path()
    poly(cr, langot)
    pl = leather(cr, GOLD, 5, keep=True)
    from puppet_core import perforate
    perforate(cr, pl, 9, 13, 2.6)
    band(cr, [(-116, -22), (-60, -18), (0, -18), (60, -18), (116, -22)], 16, RED, spacing=12)
    for sx in (-1, 1):
        ink(cr, [(sx * 60, -150), (sx * 110, -120)], 4)
    band(cr, [(-124, -196), (-70, -222), (0, -228), (70, -222), (124, -196)], 14, GOLD, spacing=11, hole_r=2.4)
    _jewel(cr, 0, -212, 10, RED)
    punch(cr, [(0, -96)], 5)


def baby_human(cr):
    """Baby Ganesha before (frontal, hip at 0, 0): mandhata_cast's sweet baby with a small gold crown and a red dot."""
    col = BABY
    _baby_torso(cr)
    for sx in (-1, 1):
        cr.new_path()
        ell(cr, sx * 172, -428, 24, 40)
        leather(cr, col, 5)
    _shape(cr, M._sym((0, -606), [(-70, -598), (-128, -566), (-166, -500), (-174, -424), (-160, -350), (-126, -292),
                                  (-72, -262)], (0, -252)), col, 7)
    for sx in (-1, 1):
        _jewel(cr, sx * 178, -378, 13, GOLD)
        ink(cr, [(sx * 150, -520), (sx * 110, -572), (sx * 50, -596)], 5, col=HAIR)
        ink(cr, [(sx * 108, -490), (sx * 74, -502), (sx * 36, -494)], 6)
        cr.new_path()
        cr.arc(sx * 112, -350, 22, 0, 2 * math.pi)
        cr.set_source_rgb(*DRED)
        cr.set_line_width(3)
        cr.stroke()
        punch(cr, [(sx * 112 + 12 * math.cos(a), -350 + 12 * math.sin(a)) for a in [i * 1.047 for i in range(6)]], 2.6)
    ink(cr, [(-14, -380), (0, -368), (14, -380)], 5)
    ink(cr, [(-40, -326), (-20, -314), (0, -311), (20, -314), (40, -326)], 6, col=DRED)
    cr.new_path()
    cr.arc(0, -540, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _crown_small(cr, -590)


def _trunk_pts(n=40):
    """The trunk's centre line (body coordinates) and width at each point: down from between the eyes, curling to the
    viewer's right at the tip."""
    out = []
    for i in range(n + 1):
        u = i / n
        if u < 0.6:
            v = u / 0.6
            x, y = 6 * v * v, -400 + 190 * v
        else:
            v = (u - 0.6) / 0.4
            a = math.pi * (1.0 - 1.25 * v)
            x, y = 6 + 44 + 44 * math.cos(a), -210 - 44 * math.sin(a) * 1.05
        out.append((x, y, 46 - 30 * u))
    return out


def baby_elephant(cr):
    """Ganesha alive again (frontal, hip at 0, 0): the same baby with a gentle elephant head: big ears with rose-pink
    insides and gold studs, a domed forehead with a gold band and a red tilak, kind eyes, two small tusks, the trunk
    curling to one side, the same gold crown."""
    col = BABY
    _baby_torso(cr)
    for sx in (-1, 1):                                                           # the ears, behind
        ear = [(sx * 100, -580), (sx * 200, -632), (sx * 300, -620), (sx * 350, -540), (sx * 336, -430),
               (sx * 290, -340), (sx * 216, -296), (sx * 146, -322), (sx * 110, -410)]
        _shape(cr, ear, col, 6, holes=(12, 16, 2.8))
        inner = [(sx * 140, -560), (sx * 214, -594), (sx * 286, -582), (sx * 318, -520), (sx * 306, -440),
                 (sx * 270, -370), (sx * 214, -340), (sx * 166, -370), (sx * 146, -440)]
        _shape(cr, inner, EAR_IN, 4)
        dots_in(cr, lambda sx=sx: spath(cr, [(sx * 170, -540), (sx * 260, -560), (sx * 290, -470),
                                              (sx * 240, -380), (sx * 180, -420)]), 22, 3.0)
        _jewel(cr, sx * 236, -326, 12, GOLD)
    face = M._sym((0, -650), [(-90, -642), (-150, -604), (-182, -530), (-176, -450), (-146, -388), (-98, -356),
                              (-60, -346)], (0, -344))
    _shape(cr, face, col, 7)
    for sx in (-1, 1):                                                           # cheeks
        cr.new_path()
        cr.arc(sx * 112, -400, 18, 0, 2 * math.pi)
        cr.set_source_rgb(*DRED)
        cr.set_line_width(3)
        cr.stroke()
    for sx in (-1, 1):                                                           # tusks
        tusk = [(sx * 44, -356), (sx * 66, -352), (sx * 84, -320), (sx * 92, -290), (sx * 74, -300), (sx * 52, -332)]
        _shape(cr, tusk, IVORY, 4)
    pts = _trunk_pts()
    left, right = [], []
    for i, (x, y, w) in enumerate(pts):
        x0, y0, _ = pts[max(0, i - 1)]
        x1, y1, _ = pts[min(len(pts) - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0
        L_ = math.hypot(dx, dy) or 1
        nx, ny = -dy / L_, dx / L_
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    tip = pts[-1]
    _shape(cr, left + [(tip[0], tip[1])] + right[::-1], col, 6)
    for i in range(3, len(pts) - 3, 3):                                          # trunk wrinkles
        x, y, w = pts[i]
        ink(cr, [left[i], (x, y + 4), right[i]], 2.6)
    band(cr, [(-150, -560), (-80, -586), (0, -592), (80, -586), (150, -560)], 16, GOLD, spacing=12, hole_r=2.4)
    _jewel(cr, 0, -592, 11, RED)
    cr.new_path()                                                                # red tilak
    ell(cr, 0, -536, 9, 22)
    cr.set_source_rgb(*RED)
    cr.fill()
    for sx in (-1, 1):                                                           # kind eyes, brows
        cr.save()
        cr.translate(sx * 80, -466)
        cr.new_path()
        cr.move_to(-26, 0)
        cr.curve_to(-12, -20, 12, -20, 26, 0)
        cr.curve_to(12, 16, -12, 16, -26, 0)
        cr.close_path()
        leather(cr, PALE, 4)
        cr.new_path()
        cr.arc(-sx * 2, 0, 11, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(-sx * 2 + 4, -4)], 3.4)
        ink(cr, [(-26, -32), (0, -40), (26, -32)], 5)
        cr.restore()
    _crown_small(cr, -636, 80)


register("sg_baby_hu", (-210, -720, 210, 80), baby_human)
register("sg_baby_el", (-370, -770, 370, 80), baby_elephant)


# ------------------------------------------------------------------ the cradle and its cloth


def _cradle_back(cr):
    """The cradle's inside (pivot at the bottom centre): the back rail, low, with a soft cream pillow along it."""
    back = [(-300, -330), (-300, -372), (-200, -390), (0, -398), (200, -390), (300, -372), (300, -330)]
    _shape(cr, back, (0.98, 0.86, 0.60), 5)
    band(cr, [(-296, -374), (-200, -392), (0, -400), (200, -392), (296, -374)], 10, GOLD, spacing=12, hole_r=2.0)
    dots_in(cr, lambda: spath(cr, back), 24, 2.6, shape="d")


def _cradle(cr):
    """The cradle's front (pivot at the bottom centre): a red and gold panel on two curved rockers, corner posts with
    gold knobs."""
    for sx in (-1, 1):
        rk = [(sx * 330, -60), (sx * 300, -20), (sx * 200, 0), (0, 0), (0, -26), (sx * 200, -30), (sx * 290, -50)]
        _shape(cr, rk, WOOD, 5)
    for sx in (-1, 1):
        _shape(cr, [(sx * 250, -30), (sx * 220, -100), (sx * 200, -100), (sx * 230, -30)], WOOD, 4, smooth=False)
    panel = [(-310, -100), (310, -100), (320, -330), (-320, -330)]
    _shape(cr, panel, (0.86, 0.20, 0.12), 6, smooth=False)
    band(cr, [(-312, -316), (312, -316)], 22, GOLD, spacing=13)
    band(cr, [(-306, -116), (306, -116)], 18, GOLD, spacing=13)
    for i in range(5):
        _flower(cr, -220 + 110 * i, -214, 30, GOLD, 8)
        _jewel(cr, -220 + 110 * i, -214, 8, GREEN)
    dots_in(cr, lambda: poly(cr, [(-300, -290), (300, -290), (300, -140), (-300, -140)]), 26, 2.6)
    for sx in (-1, 1):
        _shape(cr, [(sx * 300, -96), (sx * 340, -96), (sx * 340, -360), (sx * 300, -360)], WOOD, 5, smooth=False)
        cr.new_path()
        cr.arc(sx * 320, -384, 26, 0, 2 * math.pi)
        leather(cr, GOLD, 4)
        _jewel(cr, sx * 320, -384, 8, RED)


def _cloth(cr):
    """The cradle's cloth heaped up inside it (pivot at the rim's centre): soft red and gold folds."""
    heap = [(-296, 0), (-270, -60), (-180, -110), (-80, -126), (20, -140), (120, -118), (220, -96), (290, -40),
            (300, 0)]
    _shape(cr, heap, CLOTH, 6)
    dots_in(cr, lambda: spath(cr, heap), 22, 2.8, shape="d")
    for x0, x1 in ((-200, -120), (-40, 40), (130, 200)):
        ink(cr, [(x0, -10), ((x0 + x1) / 2, -90), (x1, -100)], 3)
    band(cr, [(-270, -52), (-180, -100), (-80, -116), (20, -130), (120, -110), (220, -88), (284, -36)], 16, CLOTH2,
         spacing=12, hole_r=2.4)


register("sg_cradle_back", (-310, -500, 310, -320), _cradle_back)
register("sg_cradle", (-350, -420, 350, 10), _cradle)
register("sg_cloth", (-310, -160, 310, 10), _cloth)


# ------------------------------------------------------------------ Shiva (the popular version, a small silhouette)


_SV_O = dict(skin=(0.80, 0.86, 0.96), bulk=1.0, dhoti=(0.92, 0.66, 0.30), border=INK, pleat=(0.92, 0.66, 0.30),
             sash=GREEN, neck=GOLD)
SHIVA = man("sg_shiva", crown="jata", hair=True, halo=False, earring=True, tilak=False, hands=("fist", "open"),
            **_SV_O)


def _trishul(cr):
    """Shiva's trident (grip at 0, 0): a long shaft, three prongs, a small damaru tied under them."""
    band(cr, [(0, 420), (0, -420)], 16, (0.70, 0.66, 0.62), spacing=22, hole_r=2.4)
    _shape(cr, [(-96, -440), (96, -440), (90, -420), (-90, -420)], GOLD, 4, smooth=False)
    _shape(cr, [(-10, -440), (0, -600), (10, -440)], (0.80, 0.80, 0.86), 4, smooth=False)
    for sx in (-1, 1):
        _shape(cr, [(sx * 70, -440), (sx * 96, -500), (sx * 86, -560), (sx * 70, -510), (sx * 54, -440)],
               (0.80, 0.80, 0.86), 4, smooth=False)
    _shape(cr, [(-30, -400), (30, -400), (0, -370)], DRED, 3, smooth=False)
    _shape(cr, [(-30, -340), (30, -340), (0, -370)], DRED, 3, smooth=False)


register("sg_trishul", (-110, -620, 110, 440), _trishul)


# ------------------------------------------------------------------ Vishnu (four arms) and his chakra, conch


_VI_O = dict(skin=VI_SKIN, hair=True, moustache=False, tilak=False)


def vishnu_head(cr):
    """Vishnu: a ring of golden rays, a tall gold kirita with a green flare, the Vaishnava tilak (a white U and a red
    line), gentle smile."""
    M._ray_halo(cr, -30, -250, 136, 220, 18, (RAY, GOLD))
    A.face(cr, _VI_O, "smile")
    ink(cr, [(42, -178), (46, -150), (58, -150), (62, -176)], 4, col=PALE)
    ink(cr, [(52, -152), (53, -176)], 4, col=RED)
    R.kirita(cr, GOLD, None, tall=1.45, flare=GREEN)
    _jewel(cr, 4, -150 + (-222 + 150) * 1.45, 14, RED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.45, 9, GREEN)


_VI = dict(skin=VI_SKIN, bulk=1.1, dhoti=VI_DHOTI, border=RED, pleat=RED, sash=RED, neck=GOLD, thread=True)
VISHNU = man("sg_vishnu", crown="tiara", halo=False, moustache=False, hands=("open", "open"), **_VI)
register("sg_vishnu_head", (-260, -560, 200, 130), vishnu_head)
register("sg_vishnu_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, VI_SKIN, VI_DHOTI, RED, 1.1))
register("sg_vishnu_armF2_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, _VI))
register("sg_vishnu_armF2_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, _VI, None, "open"))
register("sg_vishnu_armB2_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, _VI))
register("sg_vishnu_armB2_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, _VI, None, "open"))
_b = _VI["bulk"]
VISHNU.parts.insert(0, ("sg_vishnu_armB2_up", "sg_vishnu_body", (-14 * _b, -262), 0.30))
VISHNU.parts.insert(1, ("sg_vishnu_armB2_lo", "sg_vishnu_armB2_up", (0, 150), -0.25))
_i = [p[0] for p in VISHNU.parts].index("sg_vishnu_head")
VISHNU.parts.insert(_i, ("sg_vishnu_armF2_up", "sg_vishnu_body", (26 * _b, -262), -0.32))
VISHNU.parts.insert(_i + 1, ("sg_vishnu_armF2_lo", "sg_vishnu_armF2_up", (0, 150), -0.55))
VISHNU.points["handF2"] = ("sg_vishnu_armF2_lo", (6, 160))
VISHNU.points["handB2"] = ("sg_vishnu_armB2_lo", (6, 160))


def _chakra(cr):
    """The Sudarshana chakra (pivot at its hub): a gold wheel with a serrated rim of points, spokes, a red hub."""
    pts = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        r = 150 if i % 2 == 0 else 124
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, GOLD, 5, smooth=False)
    cr.new_path()
    cr.arc(0, 0, 104, 0, 2 * math.pi)
    leather(cr, (1.0, 0.70, 0.20), 4)
    for i in range(12):
        a = 2 * math.pi * i / 12
        band(cr, [(30 * math.cos(a), 30 * math.sin(a)), (96 * math.cos(a), 96 * math.sin(a))], 10, GOLD, holes=False,
             lw=3)
    for i in range(12):
        a = 2 * math.pi * (i + 0.5) / 12
        punch(cr, [(70 * math.cos(a), 70 * math.sin(a))], 9)
    cr.new_path()
    cr.arc(0, 0, 32, 0, 2 * math.pi)
    leather(cr, RED, 4)
    _jewel(cr, 0, 0, 12, GOLD)


def _conch(cr):
    """The conch (pivot at its middle): a white spiral shell with a gold cap."""
    shell = [(-90, 20), (-70, -40), (-20, -70), (50, -66), (100, -30), (110, 10), (80, 40), (20, 54), (-50, 46)]
    _shape(cr, shell, IVORY, 5)
    for k in range(3):
        ink(cr, [(-60 + 30 * k, -40 + 6 * k), (-30 + 30 * k, 30 - 4 * k)], 3, col=(0.70, 0.62, 0.50))
    _shape(cr, [(100, -30), (140, -16), (140, 6), (110, 10)], GOLD, 4, smooth=False)
    _shape(cr, [(-90, 20), (-120, 30), (-110, 4), (-80, 0)], IVORY, 4, smooth=False)


register("sg_chakra", (-160, -160, 160, 160), _chakra)
register("sg_conch", (-130, -80, 150, 64), _conch)


# ------------------------------------------------------------------ Garuda


def _garuda(cr):
    """Garuda in flight facing +x (pivot at his body centre): a fanned tail, a golden feathered body, gold anklets and
    talons trailing, a pale face with a hooked orange beak, a red and gold crest, a small gold crown."""
    for k, (col, ang) in enumerate(((GA_GREEN, 0.34), (GA_RED, 0.16), (GA_BODY, -0.02), (GA_RED, -0.2))):
        cr.save()                                                                # the tail feathers
        cr.translate(-300, -10)
        cr.rotate(math.pi + ang)
        fp = [(0, -30), (180, -44), (300, -26), (330, 0), (300, 26), (180, 44), (0, 30)]
        _shape(cr, fp, col, 4)
        ink(cr, [(20, 0), (300, 0)], 2.2, smooth=False, col=(0.50, 0.30, 0.10))
        cr.restore()
    for dx, k in ((-40, 0.85), (40, 1.0)):                                       # legs trailing back
        leg = [(dx - 10, 40), (dx + 40, 50), (dx - 30, 160), (dx - 110, 200), (dx - 120, 176), (dx - 60, 140)]
        _shape(cr, leg, tuple(c * k for c in GA_BODY), 4)
        band(cr, [(dx - 70, 160), (dx - 50, 186)], 12, GOLD, spacing=9, hole_r=2.0)
        for tx, ty in ((-160, 200), (-150, 220), (-130, 226)):
            ink(cr, [(dx - 110, 196), (dx + tx + 20, ty)], 6, col=INK)
    body = [(-330, -10), (-250, -100), (-100, -140), (60, -150), (190, -170), (250, -240), (300, -310), (390, -260),
            (400, -160), (340, -60), (230, 30), (100, 80), (-80, 86), (-250, 56)]
    _shape(cr, body, GA_BODY, 7)
    for row in range(3):                                                         # scale-like feather rows
        for i in range(9):
            x = -250 + 60 * i + 30 * (row % 2)
            y = -70 + 40 * row
            if -300 < x < 230:
                ink(cr, [(x - 20, y), (x, y + 16), (x + 20, y)], 2.4, col=(0.70, 0.40, 0.10))
    holes_line(cr, [(-280, 20), (-60, 56), (140, 40)], 18, 2.8)
    band(cr, [(236, -150), (290, -110), (318, -60)], 18, GOLD, spacing=11)
    _jewel(cr, 290, -110, 12, RED)
    cr.save()                                                                    # the head: an eagle's, noble
    cr.translate(330, -300)
    for k in range(6):                                                           # crest behind
        cr.save()
        cr.rotate(math.pi * (0.58 + 0.11 * k))
        ln = 190 - 14 * k
        _shape(cr, [(0, -20), (ln * 0.8, -16), (ln, 0), (ln * 0.8, 16), (0, 20)], GA_RED if k % 2 == 0 else GOLD,
               3.5)
        cr.restore()
    for k in range(7):                                                           # a ruff of pointed neck feathers
        a = math.pi * (0.35 + 0.1 * k)
        cr.save()
        cr.rotate(a)
        _shape(cr, [(60, -16), (150, 0), (60, 16)], GOLD if k % 2 else (1.0, 0.56, 0.16), 3, smooth=False)
        cr.restore()
    head = [(-100, 50), (-112, -20), (-80, -84), (0, -110), (70, -96), (118, -64), (134, -20), (128, 30), (90, 70),
            (20, 96), (-50, 90)]
    _shape(cr, head, GA_FACE, 7)
    for k in range(4):                                                           # feathered cheek lines
        ink(cr, [(-80 + 22 * k, 30 + 10 * k), (-30 + 22 * k, 62 + 4 * k), (20 + 18 * k, 60)], 2.4,
            col=(0.80, 0.60, 0.40))
    beak = [(112, -62), (176, -66), (236, -42), (268, 6), (258, 66), (234, 44), (222, 18), (190, 24), (128, 30)]
    _shape(cr, beak, GA_BEAK, 6)
    ink(cr, [(136, 6), (200, 4), (240, 22)], 3, col=(0.60, 0.24, 0.06))
    punch(cr, [(180, -40)], 5)
    _shape(cr, [(-20, -40), (40, -60), (100, -50), (70, -14), (10, -10)], (0.36, 0.22, 0.12), 3)   # eye stripe
    almond_eye(cr, 62, -34, 54, 19, col=(1.0, 0.86, 0.30))
    _shape(cr, [(14, -66), (66, -84), (118, -66), (110, -56), (64, -68), (20, -54)], (0.50, 0.30, 0.12), 3)
    pts = [(-50, -96), (-40, -140), (-16, -118), (4, -164), (24, -120), (46, -138), (54, -98)]
    _shape(cr, pts, GOLD, 5, smooth=False, holes=(7, 11, 2.2))
    _jewel(cr, 4, -120, 9, RED)
    band(cr, [(-54, -98), (58, -100)], 14, RED, spacing=11, hole_r=2.2)
    cr.restore()


def _gwing(cr, col, col2, tip):
    """Garuda's wing spread (pivot at the shoulder; reaching up and back): layered flight feathers in three colours,
    a perforated covert."""
    for i in reversed(range(9)):                                                 # flight feathers, tip first
        u = i / 8
        bx, by = -30 - 230 * u, -40 - 540 * u                                    # along the leading edge
        ang = math.pi - 0.25 + 1.15 * u                                          # back, fanning up toward the tip
        ln = 240 + 110 * math.sin(math.pi * (0.25 + 0.7 * u))
        cr.save()
        cr.translate(bx, by)
        cr.rotate(ang)
        fp = [(0, -28), (ln * 0.5, -38), (ln * 0.9, -22), (ln, 0), (ln * 0.9, 20), (ln * 0.5, 32), (0, 26)]
        _shape(cr, fp, (col, col2, tip)[i % 3], 3.5)
        ink(cr, [(10, 0), (ln * 0.86, 0)], 1.8, smooth=False, col=(0.50, 0.26, 0.10))
        cr.restore()
    cov = [(40, 30), (10, -120), (-70, -330), (-170, -540), (-260, -640), (-300, -600), (-250, -480), (-190, -330),
           (-150, -180), (-120, -40), (-60, 50)]
    _shape(cr, cov, col2, 4, holes=(11, 15, 2.6))
    for k in range(2):
        ink(cr, [(-40 - 34 * k, 0), (-90 - 30 * k, -260), (-200 - 10 * k, -520)], 2.4, col=(0.66, 0.36, 0.10))
    rivet(cr, 0, 0, 9)


register("sg_garuda", (-660, -500, 620, 260), _garuda)
register("sg_gwing", (-700, -960, 120, 140), lambda cr: _gwing(cr, GA_RED, GA_BODY, GA_GREEN))
register("sg_gwing_far", (-700, -960, 120, 140),
         lambda cr: _gwing(cr, (0.70, 0.16, 0.08), (0.86, 0.58, 0.18), (0.14, 0.44, 0.26)))


# ------------------------------------------------------------------ the sleeping elephant


def _elephant(cr):
    """A grey elephant asleep facing +x (pivot on the ground under its middle): lying with its legs folded, the big ear
    resting, the eye shut, the trunk curled on the ground, small tusks."""
    _shape(cr, [(-420, -120), (-470, -60), (-480, -10), (-460, -14), (-440, -70), (-400, -110)], EL2, 4)  # tail
    for x0, k in ((-330, 0.86), (180, 0.86)):                                    # far legs folded
        _shape(cr, [(x0, -40), (x0 + 150, -40), (x0 + 170, 0), (x0 - 10, 0)], tuple(c * k for c in EL), 5)
    body = [(-430, -60), (-440, -220), (-380, -380), (-240, -470), (-40, -500), (160, -470), (300, -420),
            (380, -330), (380, -150), (320, -40), (200, -10), (-300, -10)]
    _shape(cr, body, EL, 7)
    dots_in(cr, lambda: spath(cr, [(-360, -300), (-200, -420), (100, -430), (240, -340), (200, -160), (-300, -150)]),
            30, 3.0)
    for k in range(4):
        ink(cr, [(-300 + 120 * k, -420 + 10 * k), (-280 + 120 * k, -300), (-300 + 120 * k, -160)], 2.6, col=EL2)
    _shape(cr, [(-360, -40), (-160, -40), (-120, 0), (-380, 0)], EL, 5)          # near back leg, folded
    _shape(cr, [(150, -40), (440, -40), (470, 0), (140, 0)], EL, 5)              # near front leg, folded forward
    for x in (-360, -330, 440, 410):
        _shape(cr, [(x - 12, -18), (x + 12, -18), (x + 12, 0), (x - 12, 0)], PALE, 3, smooth=False)
    head = [(300, -420), (420, -470), (540, -440), (600, -360), (600, -260), (560, -180), (520, -130), (420, -110),
            (340, -160)]
    _shape(cr, head, EL, 7)
    trunk = [(560, -200), (620, -150), (660, -80), (690, -30), (740, -10), (770, -30), (760, -60), (730, -50),
             (700, -70), (640, -150), (580, -230)]
    _shape(cr, trunk, EL, 6)
    for k in range(6):
        ink(cr, [(590 + 18 * k, -190 + 30 * k), (612 + 18 * k, -200 + 32 * k)], 2.4, col=EL2)
    _shape(cr, [(560, -170), (610, -140), (640, -150), (600, -186)], IVORY, 4)
    ear = [(330, -420), (420, -440), (470, -380), (470, -260), (430, -180), (360, -170), (320, -230), (310, -340)]
    _shape(cr, ear, (0.70, 0.68, 0.78), 6, holes=(12, 16, 2.6))
    _shape(cr, [(350, -400), (430, -410), (450, -300), (410, -210), (360, -220), (340, -320)], (0.86, 0.68, 0.70), 3)
    ink(cr, [(500, -340), (520, -330), (540, -340)], 4.5)                        # the shut eye
    for x in (508, 520, 532):
        ink(cr, [(x, -334), (x - 2, -326)], 2.2)
    ink(cr, [(498, -366), (522, -372), (544, -364)], 3.5, col=EL2)


register("sg_elephant", (-500, -520, 790, 20), _elephant)


# ------------------------------------------------------------------ the devas (drawn as silhouettes)


DEVA = man("sg_deva", skin=DV_SKIN, bulk=0.95, dhoti=PALE, border=GOLD, pleat=GOLD, sash=RED, neck=GOLD,
           crown="kirita", halo=False, thread=True, hair=True, hands=("open", "open"))


# ------------------------------------------------------------------ Kailash


def _kailash(cr):
    """Mount Kailash (pivot at the foot of the middle peak): the great snow peak with its ridges between smaller
    peaks, pale ice shadows, a few punched stars of snow."""
    rock, rock2 = (0.62, 0.66, 0.80), (0.50, 0.54, 0.70)

    def peak(x0, w, h, k):
        top = (x0, -h)
        body = [(x0 - w, 0), (x0 - w * 0.55, -h * 0.5), (x0 - w * 0.18, -h * 0.9), top, (x0 + w * 0.2, -h * 0.88),
                (x0 + w * 0.6, -h * 0.45), (x0 + w, 0)]
        _shape(cr, body, tuple(c * k for c in rock), 5, smooth=False)
        _shape(cr, [top, (x0 + w * 0.2, -h * 0.88), (x0 + w * 0.6, -h * 0.45), (x0 + w, 0), (x0 + w * 0.1, 0)],
               tuple(c * k for c in rock2), 3, smooth=False)
        cap = [(x0 - w * 0.55, -h * 0.5), (x0 - w * 0.18, -h * 0.9), top, (x0 + w * 0.2, -h * 0.88),
               (x0 + w * 0.6, -h * 0.45), (x0 + w * 0.42, -h * 0.5), (x0 + w * 0.3, -h * 0.4),
               (x0 + w * 0.14, -h * 0.54), (x0, -h * 0.42), (x0 - w * 0.16, -h * 0.56), (x0 - w * 0.32, -h * 0.44),
               (x0 - w * 0.44, -h * 0.52)]
        _shape(cr, cap, SNOW, 4, smooth=False)
        _shape(cr, [top, (x0 + w * 0.2, -h * 0.88), (x0 + w * 0.6, -h * 0.45), (x0 + w * 0.42, -h * 0.5),
                    (x0 + w * 0.3, -h * 0.4), (x0 + w * 0.14, -h * 0.54), (x0 + w * 0.05, -h * 0.6)], SNOW2, 2.5,
               smooth=False)
        holes_line(cr, [(x0 - w * 0.4, -h * 0.55), (x0 - w * 0.12, -h * 0.86)], 18, 2.6)

    for x0, w, h, k in ((-600, 320, 520, 0.9), (600, 340, 580, 0.9), (-330, 300, 720, 0.96), (330, 300, 760, 0.96)):
        peak(x0, w, h, k)
    peak(0, 380, 1000, 1.0)


def _hall(cr):
    """The court of Kailash (pivot at the floor's centre): two carved pillars, a scalloped arch with bells, a
    mango-leaf toran and marigold strings."""
    for sx in (-1, 1):
        x = sx * 430
        _shape(cr, [(x - 50, 0), (x + 50, 0), (x + 40, -40), (x - 40, -40)], WOOD, 5, smooth=False)
        _shape(cr, [(x - 34, -40), (x + 34, -40), (x + 28, -760), (x - 28, -760)], (0.92, 0.62, 0.22), 5, smooth=False)
        for y in (-200, -400, -600):
            band(cr, [(x - 32, y), (x + 32, y)], 18, RED, spacing=11, hole_r=2.4)
        dots_in(cr, lambda x=x: poly(cr, [(x - 24, -60), (x + 24, -60), (x + 22, -740), (x - 22, -740)]), 18, 2.6)
        _shape(cr, [(x - 60, -760), (x + 60, -760), (x + 44, -800), (x - 44, -800)], GOLD, 5, smooth=False)
    arch = [(-500, -800), (500, -800), (500, -900), (-500, -900)]
    _shape(cr, arch, (0.86, 0.22, 0.14), 6, smooth=False)
    band(cr, [(-500, -890), (500, -890)], 18, GOLD, spacing=13)
    for i in range(9):                                                            # scallops under the beam
        x = -400 + 100 * i
        cr.new_path()
        cr.arc(x, -800, 50, 0, math.pi)
        leather(cr, (0.98, 0.70, 0.20), 4)
        _jewel(cr, x, -772, 7, RED)
    for i in range(10):                                                           # bells
        x = -450 + 100 * i
        ink(cr, [(x, -800), (x, -740)], 3)
        _shape(cr, [(x - 14, -742), (x + 14, -742), (x + 20, -712), (x - 20, -712)], GOLD, 3, smooth=False)
    for i in range(22):                                                           # mango-leaf toran
        x = -470 + 45 * i
        cr.save()
        cr.translate(x, -900)
        cr.rotate(0.12 * math.sin(i * 1.7))
        _shape(cr, [(0, 0), (16, 40), (0, 86), (-16, 40)], GREEN if i % 2 else DGREEN, 3)
        cr.restore()
    for sx in (-1, 1):                                                            # marigold strings down the pillars
        for j in range(12):
            _flower(cr, sx * 380, -720 + 30 * j, 14, (1.0, 0.62, 0.10) if j % 2 else GOLD, 7)
    ink(cr, [(-430, -880), (-200, -830), (0, -816), (200, -830), (430, -880)], 3, col=(0.40, 0.24, 0.08))
    for i in range(15):
        u = i / 14
        x = -430 + 860 * u
        y = -880 + 64 * math.sin(math.pi * u)
        _flower(cr, x, y, 13, (1.0, 0.62, 0.10) if i % 2 else GOLD, 7)


register("sg_kailash", (-900, -1040, 900, 10), _kailash)
register("sg_hall", (-520, -1000, 520, 10), _hall)
