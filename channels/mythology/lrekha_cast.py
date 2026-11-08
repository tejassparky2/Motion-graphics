"""The leather cast and props for the Lakshman Rekha reel (videos/lakshman_rekha.py), in the Togalu Gombeyaata style of
the Jarasandha, Ravana and Kaikeyi reels (puppet_cast, ravana_cast, kaikeyi_cast): profile figures with big almond
eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film.

Cast (one look each, kept the same through the video):
  SITA       in simple forest clothes: a leaf-green sari with a saffron pallu and a rust blouse, no crown, jasmine round
             her hair bun and sindoor in the parting. Calm, dignified face.
  RAMA       kaikeyi_cast.RAMA (blue skin, gold kirita with a green halo, yellow dhoti, bow and quiver).
  LAKSHMANA  fair skin, gold kirita with a saffron halo, red dhoti with a dark-green sash, a bow and a quiver.
  DEER       the golden deer of the Aranya Kanda: gold hide with silver spots, jewel-tipped antlers, a red collar;
             a jointed rod puppet (four legs) so it can prance.
  MANDODARI  queen of Lanka: crimson sari, gold pallu, a tall five-peaked crown, long earrings, layered necklaces.
  RAVANA     ravana_cast.RAVANA, the ten-headed puppet of the Ravana reel.
Props: the leaf hut (parnashala), a big earth slab (the ground the line is drawn on), palm-leaf manuscripts (wooden
boards and leaves), a large written leaf, the dark shards of harsh words, a speech cloud, the palace of Lanka.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math
import random

import kaikeyi_cast as K
import puppet_cast as C
import ravana_cast as R  # noqa: F401  (registers the Ravana puppet used by the scenes)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, SAFFRON, Rig,
                         almond_eye, band, dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet)

SITA_SKIN = (0.99, 0.79, 0.60)
SITA_SARI = (0.40, 0.64, 0.30)        # leaf green
SITA_PALLU = (0.98, 0.58, 0.18)       # saffron
SITA_CHOLI = (0.80, 0.30, 0.14)       # rust
LK_SKIN = (1.0, 0.83, 0.66)           # Lakshmana: fair
LK_DHOTI = (0.84, 0.24, 0.14)         # his red dhoti
MD_SKIN = (0.98, 0.74, 0.54)          # Mandodari
MD_SARI = (0.80, 0.14, 0.30)          # crimson
MD_PALLU = (0.98, 0.66, 0.16)
DEER = (1.0, 0.80, 0.26)              # the golden deer
DEER2 = (0.88, 0.60, 0.18)            # its far legs and ear
SILVER = (0.90, 0.93, 1.0)            # silver spots
THATCH = (0.95, 0.72, 0.32)
STRAW = (0.62, 0.40, 0.14)
BAMBOO = (0.88, 0.74, 0.44)
DOOR = (0.30, 0.18, 0.10)
EARTH = (0.52, 0.33, 0.15)
EARTH2 = (0.64, 0.44, 0.22)
SHARD = (0.27, 0.21, 0.30)            # harsh words: dark, jagged
WOOD = K.WOOD
LEAF, LEAF2 = K.LEAF, K.LEAF2

DEER_FEET = 372.0                     # body centre to hoof bottom, legs straight (design units)


# ------------------------------------------------------------------ Sita


def sita_head(cr):
    """Sita's head: woman_head's face without the gold tiara; a hair bun ringed with jasmine, sindoor in the parting,
    small gold studs."""
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, SITA_SKIN, 6)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 22 * math.cos(a), -128 + 22 * math.sin(a))], 3.2)
    for i in range(10):                                                           # jasmine round the bun
        a = math.pi * (0.35 + 1.3 * i / 9)
        _flower(cr, -62 + 42 * math.cos(a), -128 + 42 * math.sin(a), 9, PALE, 5)
    ink(cr, [(-4, -188), (18, -184), (36, -176)], 4, col=RED)                    # sindoor in the parting
    almond_eye(cr, 30, -112, 32, 11, col=PALE)
    ink(cr, [(46, -112), (60, -120)], 3)
    ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
    ink(cr, [(62, -74), (56, -70)], 3, col=RED)
    cr.new_path()
    cr.arc(44, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _jewel(cr, -10, -70, 8, GOLD)


def _sita_extra(cr):
    """Only a thin chain of wooden beads: forest clothes."""
    for i in range(7):
        u = i / 6
        cr.new_path()
        cr.arc(-10 + 52 * u, -270 + 70 * u + 30 * u * u, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2.5)


SITA = woman("sita", skin=SITA_SKIN, skirt=SITA_SARI, choli=SITA_CHOLI, border=SITA_PALLU, pallu_col=SITA_PALLU,
             gem=GREEN, flower=PALE, ornaments_extra=_sita_extra, hands=("open", "open"))
register("sita_head", (-120, -240, 100, 30), sita_head)


# ------------------------------------------------------------------ Lakshmana


LAKSHMANA = man("lakshmana", skin=LK_SKIN, bulk=1.0, dhoti=LK_DHOTI, border=GOLD, pleat=GOLD, sash=DGREEN, neck=GOLD,
                crown_col=GOLD, halo_col=SAFFRON, thread=True, hands=("open", "fist"))
register("lakshmana_quiver", (-50, -110, 50, 250), K._quiver)
LAKSHMANA.parts.insert(0, ("lakshmana_quiver", "lakshmana_body", (-30, -250), 0.55))

RAMA = K.RAMA


# ------------------------------------------------------------------ Mandodari


def md_crown(cr):
    """The queen of Lanka's crown: five tall gold peaks with jewels, a red band, pearl strings at the back."""
    for k in range(4):
        x = -54 - 8 * k
        for j in range(6):
            cr.new_path()
            cr.arc(x - 2 * j, -150 + 15 * j, 4.5, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    pts = [(-52, -156), (-62, -214), (-50, -262), (-34, -226), (-22, -286), (-4, -322), (12, -286), (26, -232),
           (42, -268), (58, -218), (56, -156)]
    _shape(cr, pts, GOLD, 5, smooth=False, holes=(10, 13, 2.6))
    for x, y, c in ((-50, -244, RED), (-4, -296, GREEN), (42, -248, RED), (-22, -262, BLUE), (26, -214, BLUE)):
        _jewel(cr, x, y, 8, c)
    _jewel(cr, 2, -204, 13, RED)
    band(cr, [(-54, -168), (58, -168)], 16, RED, spacing=11, hole_r=2.3)
    cr.new_path()
    cr.arc(-4, -334, 10, 0, 2 * math.pi)
    leather(cr, GOLD, 3)


def mandodari_head(cr):
    C.woman_head(cr, dict(skin=MD_SKIN, flower=GOLD))
    md_crown(cr)
    for k in range(4):                                                            # long jhumka earrings
        cr.new_path()
        cr.arc(-10, -46 + 13 * k, 6 - k, 0, 2 * math.pi)
        leather(cr, GOLD, 2)
    _shape(cr, [(-22, 4), (2, 4), (-4, 20), (-16, 20)], GOLD, 2.5, smooth=False)
    ink(cr, [(44, -146), (44, -134)], 3, col=GOLD)                                # forehead pendant chain
    _jewel(cr, 44, -128, 5, RED)


def _md_extra(cr):
    """Layered necklaces, a pendant, a jewelled waist belt."""
    band(cr, [(-22, -282), (12, -220), (40, -176)], 9, GOLD, spacing=10, hole_r=1.8)
    band(cr, [(-28, -276), (4, -180), (30, -120)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 32, -110, 12, GREEN)
    for x in (-26, -2, 22):
        _jewel(cr, x, -22, 7, GREEN)


MANDODARI = woman("mandodari", skin=MD_SKIN, skirt=MD_SARI, choli=GOLD, border=GOLD, pallu_col=MD_PALLU, gem=GREEN,
                  flower=GOLD, ornaments_extra=_md_extra, hands=("open", "open"))
register("mandodari_head", (-140, -350, 110, 40), mandodari_head)


# ------------------------------------------------------------------ the golden deer


def _antler(cr, dx, col):
    for w, c in ((17, INK), (9, col)):
        for pts in (((226, -306), (214, -370), (194, -428), (172, -470)), ((214, -370), (252, -402)),
                    ((198, -420), (224, -462)), ((190, -432), (156, -444))):
            ink(cr, [(x + dx, y) for x, y in pts], w, col=c)


HEAD_DX, HEAD_DY = -14, 70           # the head sits this much lower than first drawn (a shorter, deer-like neck)


def _deer_head(cr, back):
    """The head and antlers (back=True: only the far antler, drawn behind the neck)."""
    cr.save()
    cr.translate(HEAD_DX, HEAD_DY)
    if back:
        _antler(cr, -16, DEER2)
        cr.restore()
        return
    head = [(196, -268), (214, -300), (250, -314), (290, -294), (332, -264), (352, -246), (342, -230), (300, -228),
            (262, -220), (226, -228), (204, -246)]
    _shape(cr, head, DEER, 5)
    _shape(cr, [(206, -292), (158, -352), (148, -342), (188, -284)], DEER2, 4)                      # ear
    _antler(cr, 0, DEER)
    for x, y, c in ((172, -470, RED), (252, -402, BLUE), (224, -462, DGREEN), (156, -444, RED)):
        _jewel(cr, x, y, 9, c)
    almond_eye(cr, 274, -276, 30, 11, col=PALE)
    cr.new_path()
    ell(cr, 346, -244, 8, 6)
    cr.set_source_rgb(*INK)
    cr.fill()
    ink(cr, [(342, -232), (320, -232)], 3)
    cr.restore()


def _deer_body(cr):
    """The golden deer (facing +x, body centre at 0, 0): neck, head, jewelled antlers, silver spots, a red collar."""
    _deer_head(cr, True)
    _shape(cr, [(-178, -40), (-222, -86), (-238, -72), (-214, -30), (-186, -12)], DEER, 4)          # tail
    neck = [(92, -60), (136, -96), (176, -160), (196, -206), (246, -196), (240, -150), (206, -80), (176, -30)]
    _shape(cr, neck, DEER, 5)
    body = [(-196, -6), (-180, -56), (-120, -80), (-20, -74), (80, -84), (150, -74), (196, -40), (204, 6),
            (176, 46), (110, 62), (0, 58), (-110, 62), (-170, 44)]
    _shape(cr, body, DEER, 6, holes=(12, 16, 2.6))
    for x, y, rx, ry in ((-140, -30, 16, 11), (-92, -50, 13, 9), (-60, -10, 17, 12), (-10, -46, 14, 10),
                         (30, -2, 16, 11), (70, -50, 13, 9), (112, -14, 15, 10), (-110, 22, 12, 8), (150, -42, 11, 8),
                         (-30, 30, 12, 8), (70, 30, 12, 8), (176, -134, 9, 11), (210, -170, 8, 9)):
        cr.new_path()
        ell(cr, x, y, rx, ry)
        leather(cr, SILVER, 2.5)
    band(cr, [(140, -104), (180, -66), (204, -34)], 13, RED, spacing=10, hole_r=2.0)                # collar
    _jewel(cr, 210, -20, 10, GOLD)
    band(cr, [(-150, -64), (-40, -74), (70, -80)], 9, DEER2, spacing=11, hole_r=2.0)
    _deer_head(cr, False)


def _deer_leg(cr, col, hind):
    if hind:
        pts = [(-36, -28), (32, -28), (34, 60), (18, 130), (6, 172), (16, 300), (14, 322), (-6, 324), (-10, 300),
               (-16, 182), (-22, 140), (-38, 60)]
    else:
        pts = [(-26, -22), (26, -22), (22, 70), (10, 150), (12, 300), (12, 322), (-8, 324), (-10, 300), (-12, 150),
               (-22, 70)]
    _shape(cr, pts, col, 4)
    band(cr, [(-12, 292), (14, 292)], 8, RED, holes=False)
    _shape(cr, [(-12, 316), (16, 316), (20, 342), (-14, 342)], DOOR, 3, smooth=False)                  # hoof
    rivet(cr, 0, 0, 6)


register("deer_body", (-250, -420, 355, 75), _deer_body)
register("deer_legF", (-45, -40, 45, 350), lambda cr: _deer_leg(cr, DEER, False))
register("deer_legH", (-45, -40, 45, 350), lambda cr: _deer_leg(cr, DEER, True))
register("deer_legBf", (-45, -40, 45, 350), lambda cr: _deer_leg(cr, DEER2, False))
register("deer_legBh", (-45, -40, 45, 350), lambda cr: _deer_leg(cr, DEER2, True))
DEER_RIG = Rig([("deer_legBh", "deer_body", (-124, 22), 0.0),
                ("deer_legBf", "deer_body", (124, 26), 0.0),
                ("deer_body", None, (0, 0), 0.0),
                ("deer_legH", "deer_body", (-142, 28), 0.0),
                ("deer_legF", "deer_body", (142, 30), 0.0)],
               {"head": ("deer_body", (286, -192)), "top": ("deer_body", (176, -400)), "chest": ("deer_body", (0, -20)),
                "tail": ("deer_body", (-220, -60))},
               [("chest", 40, 0)])


# ------------------------------------------------------------------ sets


def _hut(cr):
    """The leaf hut (parnashala) of Panchavati (pivot at the bottom centre): woven bamboo walls, a dark doorway with
    a mango-leaf toran, a thatched roof."""
    wall = [(-300, 0), (300, 0), (290, -360), (-290, -360)]
    _shape(cr, wall, BAMBOO, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-280, -20), (280, -20), (272, -350), (-272, -350)]), 22, 3.2, shape="d")
    for y in (-110, -250):
        band(cr, [(-296, y), (296, y)], 12, OCHRE, spacing=12, hole_r=2.2)
    for x in (-300, -160, 160, 300):
        _shape(cr, [(x - 16, 0), (x + 16, 0), (x + 13, -374), (x - 13, -374)], BROWN, 5, smooth=False)
        holes_line(cr, [(x, -30), (x, -350)], 40, 3, smooth=False)
    door = [(-92, 0), (92, 0), (92, -210), (60, -262), (0, -282), (-60, -262), (-92, -210)]
    _shape(cr, door, DOOR, 6)
    band(cr, [(-104, -4), (-104, -214), (-66, -272), (0, -296), (66, -272), (104, -214), (104, -4)], 12, OCHRE,
         spacing=14, hole_r=2.2)
    for i in range(7):                                                           # mango-leaf toran
        x = -96 + 32 * i
        _shape(cr, [(x - 9, -312), (x + 9, -312), (x + 6, -270), (x, -252), (x - 6, -270)], GREEN, 3)
    ink(cr, [(-110, -314), (0, -306), (110, -314)], 4, col=INK)
    thatch = [(-392, -330), (-336, -430), (-206, -560), (-64, -640), (0, -656), (64, -640), (206, -560), (336, -430),
              (392, -330), (300, -348), (0, -380), (-300, -348)]
    _shape(cr, thatch, THATCH, 7, holes=(15, 19, 3))
    for k in range(-9, 10):
        ink(cr, [(k * 14, -640 + abs(k) * 6), (k * 40, -368 + abs(k) * 2)], 3, col=STRAW)
    for i in range(26):                                                          # ragged eave fringe
        x = -380 + 30 * i
        y = -338 - 22 * (1 - abs(x) / 380) ** 2
        ink(cr, [(x, y), (x + 6, y + 22)], 4, smooth=False, col=STRAW)
    band(cr, [(-70, -640), (0, -660), (70, -640)], 14, BROWN, spacing=12)
    cr.new_path()
    ell(cr, 0, -684, 22, 26)
    leather(cr, OCHRE, 4)
    for x, a in ((-150, -0.6), (-110, 0.3), (140, 0.5), (180, -0.2)):           # a few leafy twigs on the roof
        cr.save()
        cr.translate(x, -560 - (0 if abs(x) > 145 else 20))
        cr.rotate(a)
        _shape(cr, [(-10, 0), (0, -46), (10, 0)], GREEN, 3)
        cr.restore()


def _earth(cr):
    """A big leather slab of earth (pivot at the top centre): the ground in front of the hut, seen a little from
    above, plain in the middle so a line drawn on it reads."""
    rng = random.Random(11)
    top = [(-720 + 1440 * i / 35, rng.uniform(-6, 6)) for i in range(36)]
    _shape(cr, top + [(720, 980), (-720, 980)], EARTH, 7, smooth=False)
    band(cr, [(-712, 24), (712, 24)], 26, EARTH2, spacing=24, hole_r=3)
    for i in range(27):
        x = -700 + 54 * i + rng.uniform(-8, 8)
        for k in (-1, 0, 1):
            poly(cr, [(x + 8 * k - 5, 6), (x + 22 * k, -34 - 12 * abs(k - 0.3)), (x + 8 * k + 5, 6)])
            leather(cr, GREEN, 3)
    for _ in range(26):
        x, y = rng.uniform(-680, 680), rng.uniform(70, 700)
        if abs(x) < 420 and y < 420:
            continue
        cr.new_path()
        ell(cr, x, y, rng.uniform(8, 16), rng.uniform(5, 9), rng.uniform(-0.4, 0.4))
        leather(cr, EARTH2, 2.5)
    for y in (520, 640):
        holes_line(cr, [(-700, y), (700, y)], 28, 3.6, smooth=False)


def _board(cr):
    """A palm-leaf manuscript's wooden cover board (centre pivot), painted border, lotus, two string holes."""
    pts = [(-480, -46), (-440, -56), (440, -56), (480, -46), (490, 0), (480, 46), (440, 56), (-440, 56), (-480, 46),
           (-490, 0)]
    _shape(cr, pts, WOOD, 6, holes=(10, 15, 2.6))
    for y in (-30, 30):
        band(cr, [(-430, y), (430, y)], 8, RED, holes=False)
    _flower(cr, 0, 0, 30, GOLD, 8)
    for x in (-200, 200):
        _flower(cr, x, 0, 17, GOLD, 6)
    punch(cr, [(-400, 0), (400, 0)], 9)


def _pleaf(cr):
    """One palm leaf of a manuscript (centre pivot); its text is drawn over it per frame."""
    pts = [(-470, 0), (-452, -50), (-410, -62), (410, -62), (452, -50), (470, 0), (452, 50), (410, 62), (-410, 62),
           (-452, 50)]
    _shape(cr, pts, LEAF, 5)
    for y in (-44, 44):
        ink(cr, [(-440, y), (440, y)], 2, smooth=False, col=LEAF2)
    punch(cr, [(-420, 0), (420, 0)], 8)
    ink(cr, [(-420, 8), (-430, 40), (-420, 74)], 3.5, col=RED)


def _bigleaf(cr):
    """A palm leaf seen close (centre pivot): wide margins, string holes, room for six lines of writing."""
    w, h = 470, 200
    pts = [(-w, 0), (-w + 14, -h + 40), (-w + 50, -h), (w - 50, -h), (w - 14, -h + 40), (w, 0), (w - 14, h - 40),
           (w - 50, h), (-w + 50, h), (-w + 14, h - 40)]
    _shape(cr, pts, LEAF, 7)
    for x in (-w + 92, w - 92):
        ink(cr, [(x, -h + 22), (x, h - 22)], 2.5, smooth=False, col=LEAF2)
    for y in (-h + 18, h - 18):
        ink(cr, [(-w + 40, y), (w - 40, y)], 2, smooth=False, col=LEAF2)
    punch(cr, [(-w + 48, 0), (w - 48, 0)], 11)


def _shard(cr, k):
    """A dark jagged shard: harsh words, shown only as a shape."""
    rng = random.Random(30 + k)
    n = 7 + k
    pts = []
    for i in range(n * 2):
        a = 2 * math.pi * i / (2 * n)
        r = (92 if i % 2 == 0 else 34) * rng.uniform(0.7, 1.25)
        pts.append((1.35 * r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, SHARD, 5, smooth=False)
    ink(cr, [(-50, -6), (-12, 10), (18, -8), (52, 6)], 3.5, smooth=False, col=DRED)
    punch(cr, [(0, 0)], 5)


def _scloud(cr):
    """A speech cloud (centre pivot) with its tail at the lower left; text is drawn over it per frame."""
    _shape(cr, [(-170, 110), (-300, 262), (-60, 150)], PARCH, 6, smooth=False)
    rx, ry = 300, 140
    bumps = [(rx * math.cos(2 * math.pi * i / 22), ry * math.sin(2 * math.pi * i / 22)) for i in range(22)]
    for col, lw in ((INK, 12), (PARCH, 0)):            # stroke every bump twice as thick, then fill them all over:
        for x, y in bumps:                             # only the outer half of the union's outline stays
            cr.new_path()
            cr.arc(x, y, 66, 0, 2 * math.pi)
            cr.set_source_rgb(*col)
            if lw:
                cr.set_line_width(lw)
                cr.stroke()
            else:
                cr.fill()
    cr.new_path()
    ell(cr, 0, 0, rx + 8, ry + 8)
    cr.fill()
    cr.new_path()
    poly(cr, [(-168, 120), (-80, 150), (-150, 118)])
    cr.fill()
    for i in range(22):
        a = 2 * math.pi * (i + 0.5) / 22
        punch(cr, [((rx + 34) * math.cos(a), (ry + 34) * math.sin(a))], 3.4)


def _cusp_arch(cr, xa, xb, y0, y1, col):
    """A lintel from xa to xb between y0 (bottom of the lintel, springing line) and y1 (top), with a cusped
    opening cut out of it."""
    cx, half = (xa + xb) / 2, (xb - xa) / 2 - 6
    rise = (y0 - y1) * 0.62
    cr.new_path()
    poly(cr, [(xa, y0), (xb, y0), (xb, y1), (xa, y1)])
    pts = []
    for i in range(81):
        th = math.pi * i / 80
        r = 1 - 0.07 * abs(math.sin(5 * th))
        pts.append((cx - half * math.cos(th) * r, y0 - rise * math.sin(th) * r - 0.2 * rise * math.sin(th) ** 6))
    cr.move_to(cx - half, y0)
    for p in pts:
        cr.line_to(*p)
    cr.close_path()
    cr.set_fill_rule(1)
    cr.set_source_rgb(*col)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    cr.set_fill_rule(0)


def _palace(cr):
    """Ravana's hall in Lanka (pivot at the bottom centre): golden pillars, three cusped arches, hanging lamps, a
    crenellated cornice. Open between the pillars, so the puppets stand in the lamp light."""
    _shape(cr, [(-610, 0), (610, 0), (600, -54), (-600, -54)], OCHRE, 6, smooth=False, holes=(10, 15, 3))
    xs = (-480, -165, 165, 480)
    for (xa, xb) in zip(xs, xs[1:]):
        _cusp_arch(cr, xa, xb, -900, -1080, DRED)
        dots_in(cr, lambda xa=xa, xb=xb: poly(cr, [(xa + 10, -1072), (xb - 10, -1072), (xb - 10, -1040),
                                                   (xa + 10, -1040)]), 20, 3.4, shape="d")
    for x in xs:
        pil = [(x - 44, -54), (x + 44, -54), (x + 36, -96), (x + 30, -870), (x + 52, -906), (x - 52, -906),
               (x - 30, -870), (x - 36, -96)]
        _shape(cr, pil, GOLD, 6, smooth=False, holes=(11, 15, 3))
        dots_in(cr, lambda x=x: poly(cr, [(x - 16, -130), (x + 16, -130), (x + 14, -840), (x - 14, -840)]), 20, 3.6,
                shape="d")
        for y in (-110, -850):
            band(cr, [(x - 44, y), (x + 44, y)], 18, RED, spacing=13)
        _flower(cr, x, -940, 26, RED, 8)
    band(cr, [(-610, -1092), (610, -1092)], 26, GOLD, spacing=15)
    for i in range(16):                                                          # crenellations
        x = -600 + 80 * i
        _shape(cr, [(x, -1104), (x + 40, -1104), (x + 40, -1150), (x + 20, -1170), (x, -1150)], GOLD, 4,
               smooth=False)
    for x in (-322, 322):                                                        # hanging lamps
        ink(cr, [(x, -900), (x, -720)], 4, smooth=False)
        _shape(cr, [(x - 44, -720), (x + 44, -720), (x + 26, -690), (x - 26, -690)], GOLD, 4, smooth=False)
        _jewel(cr, x, -704, 7, RED)


register("lr_hut", (-410, -716, 410, 10), _hut)
register("lr_earth", (-730, -60, 730, 990), _earth)
register("lr_board", (-500, -66, 500, 66), _board)
register("lr_pleaf", (-480, -72, 480, 86), _pleaf)
register("lr_bigleaf", (-480, -210, 480, 210), _bigleaf)
for _k in range(3):
    register(f"lr_shard{_k}", (-160, -130, 160, 130), (lambda k: lambda cr: _shard(cr, k))(_k))
register("lr_scloud", (-400, -240, 400, 280), _scloud)
register("lr_palace", (-620, -1180, 620, 10), _palace)
