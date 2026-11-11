"""The leather cast and props for the Garuda Purana reel (videos/garuda_purana.py), in the Togalu Gombeyaata style of
the earlier reels (puppet_cast, kaikeyi_cast, mandhata_cast, ruru_cast, dharmavyadha_cast, six_cast_b): profile figures
with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no
film. Every sprite name starts with "gp_".

Cast (one look each, kept the same through the video):
  THE OLD MAN   white hair and a white beard (dharmavyadha_cast.old_man_head), a cream dhoti with a brown border and a
                beige shawl; lies on a rope cot. Faces: calm (eyes open), shut (eyes closed). His empty body afterwards
                is a dotted outline (drawn in the scenes); the soul is a small figure of light (drawn in the scenes).
  YAMADUTAS     Yama's two messengers (one puppet, drawn twice): tall, dark blue-black skin, wild black hair standing
                up like flames, an iron headband with a red stone, a scowl, big pale eyes, a curled moustache, iron
                rings in the ears, a dark maroon dhoti; an iron-banded staff and a rope noose. Fierce, never monstrous:
                no fangs, no horns, no blood.
  YAMA          ruru_cast's Yama Dharmaraja (dark blue-grey skin, tall gold crown, red dhoti, the danda), seated on
                mandhata_cast's throne: his seated legs here (gp_yama_seat).
  THE SON       a young man in mourning: a plain white dhoti, bare chest with the sacred thread, a shaven head with a
                tuft (shikha), sandal-paste lines on the brow; eyes lowered. Kneels to offer the rice-balls.
  CHITRAGUPTA   Yama's record-keeper: warm skin, a small gold crown with a green flare, a yellow dhoti with a dark-red
                border, a green sash; holds the long scroll of deeds (drawn in the scenes).
  THE BOATMAN   dharmavyadha_cast's husband puppet (white head-cloth, moustache, short cream dhoti) with a bamboo pole.
Props: a big thumbs-up hand (the thumb's base at y = -THUMB_BASE, its tip at y = -THUMB_TIP), a rice-ball (pinda), a
banana leaf, a small clay lamp, the noose, the messengers' staff, a small city gate, the ferry boat, the bamboo pole, a
gift cow (decorated: painted horns, a red-and-gold cloth, a bell), dark-red river strips (the Vaitarani: dark water,
never gore), a wooden doorway, a dead tree. The room, rope cot, house, hall, door, throne, palm-leaf book, plaque,
speech cloud, flames, water pot and bowl come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man().
"""
import math

import arjuna_cast as A
import dharmavyadha_cast as DV
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
import six_cast_b as SB  # noqa: F401  (registers Yama's hall and door)
from puppet_cast import HAIR, _jewel, _shape, man
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, PALE, RED, SAFFRON, band, dots_in, ell, ink, leather,
                         poly, punch, register, rivet, spath)

OLD_SKIN = (0.86, 0.63, 0.44)         # the old man
OLD_DHOTI = (0.98, 0.94, 0.84)
OLD_BORDER = (0.55, 0.34, 0.16)
OLD_SHAWL = (0.84, 0.70, 0.48)
DU_SKIN = (0.22, 0.24, 0.33)          # the messengers: dark blue-black
DU_HAIR = (0.08, 0.06, 0.08)
DU_DHOTI = (0.36, 0.12, 0.14)         # dark maroon
DU_DARK = (0.20, 0.17, 0.20)
IRON = (0.42, 0.42, 0.48)
SON_SKIN = (0.93, 0.67, 0.45)         # the son
SON_SCALP = (0.84, 0.58, 0.38)
CG_SKIN = (0.96, 0.74, 0.50)          # Chitragupta
CG_DHOTI = (0.99, 0.80, 0.26)
THUMB_SKIN = (0.97, 0.73, 0.50)
NAIL = (1.0, 0.86, 0.80)
RICE = DV.RICE
LEAF = (0.42, 0.72, 0.28)
CLAY = (0.80, 0.40, 0.18)
ROPE = (0.82, 0.64, 0.32)
STONE = (0.74, 0.58, 0.42)
STONE2 = (0.58, 0.42, 0.30)
WOOD = (0.56, 0.33, 0.15)
WOOD2 = (0.72, 0.46, 0.22)
BAMBOO = (0.84, 0.72, 0.40)
COWC = (0.97, 0.94, 0.86)
COWC2 = (0.80, 0.74, 0.64)
RIVER = (0.50, 0.09, 0.10)            # the Vaitarani: dark red water
RIVER2 = (0.36, 0.05, 0.08)
BARK = (0.46, 0.36, 0.28)

THUMB_BASE, THUMB_TIP = 452.0, 772.0  # the thumb (design units above the wrist pivot)
DIYA_WICK = (112.0, -66.0)            # the clay lamp's wick


# ------------------------------------------------------------------ the old man


_OLD = dict(skin=OLD_SKIN, bulk=0.9, dhoti=OLD_DHOTI, border=OLD_BORDER, pleat=OLD_DHOTI, sash=OLD_SHAWL, neck=BROWN,
            robe=OLD_SHAWL, beads=True)
OLD = man("gp_old", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_OLD)
for _m in ("calm", "shut"):
    register("gp_old_head" + ("" if _m == "calm" else "_" + _m), (-130, -250, 110, 80),
             (lambda m: lambda cr: DV.old_man_head(cr, OLD_SKIN, m))(_m))


# ------------------------------------------------------------------ Yama's messengers


def duta_head(cr):
    """A Yamaduta: wild black hair standing up behind the head like dark flames, an iron headband with a red stone,
    a scowl, a big pale eye, a curled moustache, an earring."""
    locks = []
    cx, cy = -30, -130
    n = 15
    for i in range(n + 1):
        a = math.radians(-100 - 170 * i / n)                  # from the brow, over the top, down the back
        r = 150 if i % 2 == 0 else 96
        r += 30 * math.sin(i * 1.7)
        locks.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    locks += [(-60, -10), (-20, -60), (10, -150)]
    _shape(cr, locks, DU_HAIR, 5)
    for i in range(0, n, 2):                                                      # a few lighter strands
        a = math.radians(-100 - 170 * i / n)
        ink(cr, [(cx + 50 * math.cos(a), cy + 50 * math.sin(a)), (cx + 120 * math.cos(a), cy + 120 * math.sin(a))],
            2.6, col=(0.32, 0.30, 0.38))
    A.face(cr, dict(skin=DU_SKIN, hair=False, moustache=True, tilak=False, earring=True), "angry")
    ink(cr, [(22, -88), (6, -76), (12, -62), (24, -64)], 6, col=DU_HAIR)          # the moustache curls
    ink(cr, [(10, -160), (34, -150), (60, -164)], 9, col=DU_HAIR)                 # a heavy brow
    band(cr, [(-52, -168), (0, -192), (46, -186)], 22, IRON, spacing=12, hole_r=2.4)
    _jewel(cr, 18, -190, 10, RED)


_DU = dict(skin=DU_SKIN, bulk=1.12, dhoti=DU_DHOTI, border=DU_DARK, pleat=DU_DARK, sash=DRED, neck=IRON, beads=False)
DUTA = man("gp_duta", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
           hands=("fist", "fist"), **_DU)
register("gp_duta_head", (-220, -330, 120, 100), duta_head)


def rope(cr, pts, w=16.0, col=ROPE, smooth=True):
    """A twisted rope along pts: an ink edge, the dyed rope, small twist marks."""
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=False)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    cr.set_source_rgb(*INK)
    cr.set_line_width(w + 8)
    cr.stroke_preserve()
    cr.set_source_rgb(*col)
    cr.set_line_width(w)
    cr.stroke()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0)
        for k in range(int(L_ // 18)):
            u = (k + 0.5) * 18 / L_
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            nx, ny = -(y1 - y0) / L_, (x1 - x0) / L_
            ink(cr, [(x - nx * w * 0.4 - 4, y - ny * w * 0.4), (x + nx * w * 0.4 + 4, y + ny * w * 0.4)], 2,
                smooth=False, col=(0.55, 0.40, 0.18))


def _noose(cr):
    """The pasha (noose), held at its coil (pivot 0, 0): three loops of rope, the end hanging down into a running
    loop."""
    for k in range(3):
        pts = [(-46 + 4 * k, -20 + 18 * k), (0, -60 + 18 * k), (50 - 4 * k, -20 + 18 * k), (0, 22 + 18 * k),
               (-46 + 4 * k, -18 + 18 * k)]
        rope(cr, pts, 13)
    rope(cr, [(30, 50), (40, 130), (34, 220), (20, 280)], 13)
    loop = [(20, 280)] + [(20 + 70 * math.sin(a), 360 - 80 * math.cos(a)) for a in
                          (2 * math.pi * i / 18 for i in range(1, 19))]
    rope(cr, loop, 12)
    band(cr, [(10, 270), (34, 290)], 16, DRED, holes=False, lw=3)


register("gp_noose", (-80, -90, 110, 460), _noose)


def _dstaff(cr):
    """The messengers' staff (grip at 0, 0): dark wood with iron bands, an iron knob with three short points."""
    band(cr, [(0, 430), (0, -440)], 24, (0.28, 0.20, 0.16), spacing=22, hole_r=2.6)
    for y in (-330, -150, 30, 210, 380):
        band(cr, [(-15, y), (15, y)], 16, IRON, holes=False)
    cr.new_path()
    ell(cr, 0, -486, 46, 50)
    leather(cr, IRON, 5)
    for a in (-0.7, 0.0, 0.7):
        x0, y0 = 40 * math.sin(a), -486 - 44 * math.cos(a)
        _shape(cr, [(x0 - 12 * math.cos(a), y0 - 12 * math.sin(a)), (x0 + 40 * math.sin(a), y0 - 40 * math.cos(a)),
                    (x0 + 12 * math.cos(a), y0 + 12 * math.sin(a))], IRON, 3.5, smooth=False)
    punch(cr, [(-14, -496), (12, -478)], 5)


register("gp_dstaff", (-70, -580, 70, 450), _dstaff)


# ------------------------------------------------------------------ Yama seated


register("gp_yama_seat", (-130, -80, 380, 330), lambda cr: M.seat_legs(cr, RU.YM_SKIN, RU.YM_DHOTI, GOLD, 1.18))


# ------------------------------------------------------------------ the son


def son_head(cr, mood="sad"):
    """The son in mourning: a shaven head with a tuft at the crown, sandal-paste lines; eyes lowered (sad) or calm."""
    A.face(cr, dict(skin=SON_SKIN, hair=False, moustache=True, tilak=False, earring=False),
           "shame" if mood == "sad" else "calm")
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -186), (24, -188), (-8, -182),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, SON_SCALP, 4)
    dots_in(cr, lambda: spath(cr, cap), 16, 1.6)
    tuft = [(-30, -204), (-10, -230), (-30, -262), (-62, -268), (-80, -244), (-56, -226)]
    _shape(cr, tuft, HAIR, 3.5)
    for k in range(3):
        ink(cr, [(12, -176 + 9 * k), (50, -172 + 9 * k)], 3.2, col=(1.0, 0.97, 0.9))
    cr.new_path()
    cr.arc(50, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


_SON = dict(skin=SON_SKIN, bulk=0.95, dhoti=PALE, border=(0.80, 0.66, 0.36), pleat=PALE, sash=PALE, neck=BROWN,
            thread=True, beads=False)
SON = man("gp_son", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_SON)
for _m in ("sad", "calm"):
    register("gp_son_head" + ("" if _m == "sad" else "_" + _m), (-130, -290, 110, 30),
             (lambda m: lambda cr: son_head(cr, m))(_m))
register("gp_son_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, SON_SKIN, PALE, (0.80, 0.66, 0.36), 0.95))


# ------------------------------------------------------------------ Chitragupta


def chitra_head(cr):
    """Chitragupta: long dark hair, a moustache, a tilak, a small gold crown with a green flare and a green stone."""
    A.face(cr, dict(skin=CG_SKIN, hair=True, moustache=True, tilak=True, earring=True), "calm")
    R.kirita(cr, GOLD, None, tall=0.82, flare=GREEN)
    _jewel(cr, 2, -150 + (-282 + 150) * 0.82, 9, DGREEN)


CHITRA = man("gp_chitra", skin=CG_SKIN, bulk=1.0, dhoti=CG_DHOTI, border=DRED, pleat=GOLD, sash=GREEN, neck=GOLD,
             crown="tiara", halo=False, thread=True, hands=("open", "open"))
register("gp_chitra_head", (-200, -470, 120, 100), chitra_head)


# ------------------------------------------------------------------ the thumb, rice-balls, leaf, lamp


def _thumb(cr):
    """A big thumbs-up hand in leather (pivot at the wrist's bottom centre): the four curled fingers stacked on the
    right, the thumb straight up on the left (its base at -THUMB_BASE, its tip at -THUMB_TIP), a gold bangle."""
    sk = THUMB_SKIN
    _shape(cr, [(-118, 10), (-126, -190), (122, -190), (114, 10)], sk, 6, smooth=False, holes=(12, 18, 2.6))
    band(cr, [(-128, -64), (0, -70), (128, -64)], 40, GOLD, spacing=14)
    band(cr, [(-128, -112), (0, -118), (128, -112)], 14, RED, holes=False, lw=3)
    palm = [(-156, -170), (-170, -300), (-160, -440), (-110, -470), (20, -476), (90, -456), (110, -300), (96, -170)]
    _shape(cr, palm, sk, 6, holes=(14, 18, 2.6))
    thumb = [(-160, -430), (-164, -560), (-160, -680), (-140, -752), (-96, -776), (-50, -760), (-30, -700),
             (-26, -560), (-30, -452)]
    _shape(cr, thumb, sk, 6, holes=(14, 18, 2.6))
    cr.new_path()                                                                 # the nail
    ell(cr, -62, -718, 26, 40, 0.12)
    leather(cr, NAIL, 4)
    ink(cr, [(-80, -690), (-46, -688)], 2.4)
    for y in (-560, -585):
        ink(cr, [(-150, y), (-110, y - 6)], 3)
    for k, cy in enumerate((-418, -340, -262, -186)):                            # the curled fingers
        fx0, fx1, h = -40, 176 - 6 * k, 74
        fp = [(fx0, cy - h / 2), (fx1 - 30, cy - h / 2), (fx1, cy - h / 4), (fx1, cy + h / 4), (fx1 - 30, cy + h / 2),
              (fx0, cy + h / 2)]
        _shape(cr, fp, sk, 5)
        ink(cr, [(fx1 - 70, cy - h / 2 + 10), (fx1 - 64, cy + h / 2 - 10)], 3)   # the knuckle crease
        punch(cr, [(fx0 + 40, cy)], 4)
    rivet(cr, -60, -300, 9)


register("gp_thumb", (-200, -800, 200, 20), _thumb)


def _pinda(cr):
    """A rice-ball (pinda): a white ball, a pale highlight, a few grains, punched holes the light comes through."""
    cr.new_path()
    cr.arc(0, 0, 46, 0, 2 * math.pi)
    leather(cr, RICE, 5)
    cr.new_path()
    ell(cr, -14, -16, 16, 10, -0.5)
    cr.set_source_rgb(1.0, 1.0, 0.98)
    cr.fill()
    for x, y in ((14, 10), (-10, 18), (22, -12), (0, 30), (-26, 4)):
        ink(cr, [(x - 4, y - 2), (x + 4, y + 2)], 2.2, smooth=False, col=(0.78, 0.74, 0.62))
    punch(cr, [(10, -20), (-20, 22), (26, 18)], 3.4)


register("gp_pinda", (-54, -54, 54, 54), _pinda)


def _leaf(cr):
    """A banana leaf lying flat (pivot at its middle): a wide green leaf, the midrib, side veins."""
    pts = [(-300, 6), (-250, -42), (-120, -62), (60, -64), (230, -48), (300, -8), (250, 34), (80, 50), (-120, 50),
           (-260, 40)]
    _shape(cr, pts, LEAF, 5, holes=(12, 20, 2.6))
    ink(cr, [(-290, 4), (0, -4), (292, -8)], 4, col=DGREEN)
    for k in range(-6, 7):
        x = 42 * k
        ink(cr, [(x, -4), (x + 26, -46)], 2, smooth=False, col=DGREEN)
        ink(cr, [(x, -2), (x + 22, 36)], 2, smooth=False, col=DGREEN)


register("gp_leaf", (-310, -75, 310, 60), _leaf)


def _diya(cr):
    """A small clay lamp (pivot at the bottom centre; the wick at DIYA_WICK): a shallow terracotta bowl with a spout,
    painted dots and a band."""
    bowl = [(-110, -54), (-96, -20), (-60, 0), (60, 0), (96, -22), (118, -52), (140, -70), (104, -72), (60, -60),
            (0, -58), (-60, -60)]
    _shape(cr, bowl, CLAY, 5)
    band(cr, [(-100, -46), (0, -50), (98, -46)], 12, SAFFRON, holes=False, lw=3)
    punch(cr, [(-60, -24), (-20, -18), (20, -18), (60, -24)], 4)
    cr.new_path()
    ell(cr, 0, -60, 100, 12)
    leather(cr, (0.45, 0.22, 0.08), 3)
    ink(cr, [(96, -64), (114, -66)], 4, col=(0.25, 0.15, 0.08))


register("gp_diya", (-130, -90, 160, 10), _diya)


# ------------------------------------------------------------------ sets: gate, doorway, dead tree, river


def _gate(cr):
    """A small city gate (pivot at the bottom centre): two towers with domes and flags, a crenellated wall, an arched
    doorway cut through so the light shows."""
    for sx in (-1, 1):
        x = sx * 200
        _shape(cr, [(x - 80, 0), (x - 80, -420), (x + 80, -420), (x + 80, 0)], STONE, 5, smooth=False,
               holes=(12, 18, 2.4))
        cr.new_path()
        cr.arc(x, -420, 80, math.pi, 2 * math.pi)
        cr.close_path()
        leather(cr, STONE2, 5)
        ink(cr, [(x, -500), (x, -580)], 4)
        _shape(cr, [(x, -580), (x + 60 * sx, -560), (x, -540)], RED, 3, smooth=False)
        punch(cr, [(x, -300), (x, -200)], 9)
    wall = [(-130, 0), (-130, -330), (130, -330), (130, 0)]
    _shape(cr, wall, STONE2, 5, smooth=False)
    for k in range(5):
        x = -120 + 60 * k
        _shape(cr, [(x, -330), (x, -370), (x + 36, -370), (x + 36, -330)], STONE2, 4, smooth=False)
    cr.new_path()
    cr.move_to(-70, 0)
    cr.line_to(-70, -170)
    cr.arc(0, -170, 70, math.pi, 2 * math.pi)
    cr.line_to(70, 0)
    cr.close_path()
    cr.set_source_rgb(*INK)
    cr.set_line_width(8)
    cr.stroke_preserve()
    cr.save()
    cr.set_operator(0)
    cr.fill()
    cr.restore()
    band(cr, [(-140, -250), (140, -250)], 16, GOLD, spacing=12, hole_r=2.0)


register("gp_gate", (-300, -600, 300, 10), _gate)


def _doorway(cr):
    """A wooden doorway seen from inside the room (pivot at the bottom centre): two posts, a carved lintel with a
    mango-leaf toran, a raised threshold. The opening is left empty (the scene paints the night in it)."""
    for sx in (-1, 1):
        x = sx * 210
        _shape(cr, [(x - 34, 0), (x - 34, -940), (x + 34, -940), (x + 34, 0)], WOOD, 6, smooth=False,
               holes=(10, 18, 2.6))
        for k in range(5):
            band(cr, [(x - 30, -120 - 180 * k), (x + 30, -120 - 180 * k)], 12, GOLD, holes=False, lw=3)
    _shape(cr, [(-280, -930), (280, -930), (300, -1010), (-300, -1010)], WOOD2, 6, smooth=False, holes=(10, 18, 2.6))
    for i in range(9):
        x = -200 + 50 * i
        _shape(cr, [(x - 10, -930), (x + 10, -930), (x + 7, -880), (x, -858), (x - 7, -880)], GREEN, 2.6)
    _shape(cr, [(-260, 0), (260, 0), (250, -26), (-250, -26)], WOOD2, 5, smooth=False)


register("gp_doorway", (-310, -1020, 310, 10), _doorway)


def _limb(cr, p0, p1, w0, w1, col):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    _shape(cr, [(p0[0] + nx * w0, p0[1] + ny * w0), (p1[0] + nx * w1, p1[1] + ny * w1),
                (p1[0] - nx * w1, p1[1] - ny * w1), (p0[0] - nx * w0, p0[1] - ny * w0)], col, 4, smooth=False)


def _deadtree(cr):
    """A dead, leafless tree (pivot at the trunk's foot): a bent trunk, bare branches, a few cracks."""
    _limb(cr, (0, 0), (-20, -380), 46, 30, BARK)
    _limb(cr, (-20, -380), (40, -640), 30, 16, BARK)
    for p0, p1, w in (((-16, -300), (-200, -470), 18), ((-200, -470), (-260, -600), 10),
                      ((-150, -420), (-120, -560), 9),
                      ((10, -480), (190, -600), 16), ((190, -600), (250, -720), 8), ((120, -560), (110, -700), 7),
                      ((40, -640), (20, -760), 9)):
        _limb(cr, p0, p1, w, w * 0.45, BARK)
    for y in (-90, -200, -320):
        ink(cr, [(-14, y), (4, y - 30), (-8, y - 60)], 2.6)
    _shape(cr, [(-80, 6), (80, 6), (50, -16), (-50, -16)], BARK, 4, smooth=False)


register("gp_deadtree", (-300, -780, 290, 20), _deadtree)
register("gp_rwaveA", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, RIVER))
register("gp_rwaveB", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, RIVER2))


# ------------------------------------------------------------------ the ferry, the pole, the gift cow


def _boat(cr):
    """The ferry boat seen from the side (pivot at the middle of the waterline): a long wooden hull with curled-up
    ends, plank lines, a gold rim, punched holes."""
    hull = [(-520, -150), (-470, -40), (-380, 40), (-200, 70), (200, 70), (380, 40), (470, -40), (520, -150),
            (490, -150), (430, -80), (300, -60), (-300, -60), (-430, -80), (-490, -150)]
    _shape(cr, hull, WOOD, 6, holes=(12, 18, 2.8))
    for k in range(2):
        ink(cr, [(-430 + 30 * k, -40 + 30 * k), (-200, -10 + 30 * k), (200, -10 + 30 * k),
                 (430 - 30 * k, -40 + 30 * k)], 3, col=(0.32, 0.18, 0.08))
    band(cr, [(-470, -86), (-300, -66), (300, -66), (470, -86)], 18, GOLD, spacing=14, hole_r=2.4)
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 500, -168, 22, 0, 2 * math.pi)
        leather(cr, GOLD, 4)


register("gp_boat", (-560, -200, 560, 90), _boat)


def _pole(cr):
    """A long bamboo pole (grip at 0, 0)."""
    band(cr, [(0, 560), (0, -640)], 20, BAMBOO, spacing=24, hole_r=2.2)
    for y in range(-600, 560, 150):
        band(cr, [(-12, y), (12, y)], 8, (0.62, 0.50, 0.24), holes=False, lw=2.5)


register("gp_pole", (-40, -660, 40, 580), _pole)


def _cow(cr):
    """A healthy gift cow facing +x (pivot on the ground under its middle): a full body with a hump, a red-and-gold
    cloth on the back, painted horns, a bell at the neck, a calm eye."""
    for x0, x1 in ((-236, -244), (150, 156)):                                     # far legs, darker
        leg = [(x0 - 20, -350), (x0 + 20, -350), (x0 + 14, -180), (x1 + 10, -20), (x1 + 14, 0), (x1 - 16, 0),
               (x1 - 10, -20), (x0 - 14, -180)]
        _shape(cr, leg, COWC2, 4, smooth=False)
    tail = [(-336, -500), (-370, -380), (-372, -250), (-356, -244), (-350, -380), (-324, -490)]
    _shape(cr, tail, COWC, 3.5)
    _shape(cr, [(-384, -262), (-346, -262), (-342, -190), (-362, -172), (-386, -196)], (0.46, 0.38, 0.30), 3)
    body = [(-342, -500), (-310, -600), (-240, -606), (-120, -590), (20, -590), (110, -610), (160, -676), (226, -668),
            (270, -600), (292, -500), (280, -400), (230, -340), (100, -318), (-40, -312), (-180, -326), (-280, -360),
            (-336, -420)]
    _shape(cr, body, COWC, 6, holes=(14, 22, 2.8))
    cloth = [(-200, -598), (110, -606), (120, -470), (-190, -460)]
    _shape(cr, cloth, RED, 5, smooth=False)
    dots_in(cr, lambda: poly(cr, cloth), 24, 3.2, shape="d")
    band(cr, [(-196, -470), (118, -476)], 22, GOLD, spacing=12, hole_r=2.2)
    for k in range(9):                                                            # the fringe
        x = -186 + 36 * k
        ink(cr, [(x, -456), (x, -430)], 3.5, col=GOLD)
    for x0, x1 in ((-276, -284), (196, 204)):                                     # near legs
        leg = [(x0 - 22, -380), (x0 + 22, -380), (x0 + 15, -186), (x1 + 11, -20), (x1 + 15, 0), (x1 - 15, 0),
               (x1 - 11, -20), (x0 - 15, -186)]
        _shape(cr, leg, COWC, 4.5, smooth=False)
        _shape(cr, [(x1 - 17, -2), (x1 + 17, -2), (x1 + 19, 10), (x1 - 19, 10)], (0.30, 0.24, 0.20), 3, smooth=False)
    cr.save()                                                                     # neck and head, held up
    cr.translate(262, -600)
    cr.rotate(-0.18)
    dew = [(-10, 40), (20, 130), (70, 170), (110, 130), (140, 50)]
    _shape(cr, dew, COWC, 4)
    neck = [(-30, -40), (70, -56), (140, -16), (166, 40), (120, 76), (30, 84), (-30, 60)]
    _shape(cr, neck, COWC, 5)
    band(cr, [(20, 70), (70, 90), (126, 70)], 16, RED, holes=False, lw=3)        # the bell on its red band
    _shape(cr, [(58, 92), (86, 92), (94, 132), (50, 132)], GOLD, 3.5, smooth=False)
    punch(cr, [(72, 124)], 4)
    for hx, col in ((122, SAFFRON), (144, RED)):                                  # painted horns
        _shape(cr, [(hx - 12, -40), (hx + 12, -44), (hx + 22, -96), (hx + 4, -140), (hx - 8, -128), (hx, -94)],
               col, 3)
    ear = [(116, -10), (52, -34), (18, -12), (56, 8), (116, 8)]
    _shape(cr, ear, COWC2, 3.5)
    head = [(104, -42), (162, -54), (200, -14), (248, 64), (270, 108), (258, 142), (214, 144), (172, 106), (124, 40),
            (100, 0)]
    _shape(cr, head, COWC, 5)
    cr.new_path()
    ell(cr, 250, 126, 24, 20, 0.5)
    leather(cr, (0.86, 0.66, 0.60), 4)
    punch(cr, [(258, 120)], 4)
    from puppet_core import almond_eye
    almond_eye(cr, 166, 8, 30, 12, col=PALE)
    cr.new_path()
    cr.arc(150, -30, 9, 0, 2 * math.pi)                                           # a red dot on the brow
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.restore()


register("gp_cow", (-400, -820, 560, 20), _cow)
