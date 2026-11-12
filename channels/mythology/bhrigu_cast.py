"""The leather cast and props for the Bhrigu reel (videos/bhrigu.py), in the Togalu Gombeyaata style of the earlier
shadow-puppet reels (puppet_cast, shani_cast, shikhandi_cast, six_cast_c, kumbhakarna_cast, hanuman_cast): profile
figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor
and no film. Every sprite name starts with "bg_".

Cast (one look each, kept the same through the video; every deity and sage with dignity):
  BHRIGU     the fiery sage, son of Brahma: warm brown skin, a tall dark top-knot of matted hair rising like a flame,
             tied with a red cloth and a ring of rudraksha, a long grey beard and moustache, three ash lines and a red
             dot on the brow, a deep saffron-red robe over a red dhoti, his bamboo staff (ashtavakra_cast's av_staff).
             Faces: calm, stern (a hard straight brow: no bow, no word), shout (the jaw open, the brow pulled down),
             shock, weep (eyes shut, tears), joy. Standing, kicking (only ever drawn as a silhouette), or seated with
             one leg stretched out (bg_bhrigu_seat_ext: his foot held in Vishnu's hands).
  VISHNU     shani_cast.VISHNU (four arms, conch and Sudarshana chakra, the tall kirita and ring of rays) with more
             faces here: kind (his smile), rest (eyes shut, peaceful), speak (a gentle open mouth), calm; a lying-down
             head with a low kirita and no rays (bg_vishnu_head_lie_rest / _calm) so it rests in Lakshmi's lap;
             kneeling legs (bg_vishnu_kneel) for pressing the sage's feet.
  LAKSHMI    graceful and calm: warm fair skin, a rose-red sari with a gold border and a deep-red pallu, a gold blouse,
             a gold crown topped with a pink lotus, a ring of pink and gold rays, jasmine in her bun, sindoor and a
             bindi. Faces: open, smile, speak (startled), down (eyes lowered). Seated (bg_lakshmi_body_sit) with
             Vishnu's head in her lap.
  BRAHMA     six_cast_c.BRAHMA on his lotus (three of four faces, white beards), plus bg_brahma_head_red: the same
             three faces flushed red with an angry brow (his anger, which he then swallows).
  SHIVA      shikhandi_cast.SHIVA (piled jata with the crescent moon, the serpent at his neck, a tiger-skin wrap) with
             faces here: smile (glad, open-armed), shock, angry (the brow pulled down, the third eye glowing); his
             trident is shani_cast's sg_trishul (only ever raised, never used).
  PARVATI    shani_cast.PARVATI (red sari, tiered gold crown) with a kneeling body (bg_parvati_body_kneel): she kneels
             at Shiva's feet, holds them and calms him.
  THE SAGES  the fire's other sages are the earlier casts' rishis (ruru_cast KHAG and RISHI, mandhata_cast MDSAGE,
             six_cast_a SHUKRA).
Sets and props: Adishesha (bg_shesha: a great coiled serpent bed with a five-headed hood), the ocean of milk
(bg_milkA / bg_milkB), a foot-sole print (bg_sole: the ghost of the kick, drawn translucent), a spiky shout cloud
(bg_shout), a parchment medallion rim (bg_medal_rim). Kailash, the lotus, the fire altar, plaques, clouds and the
palm-leaf book come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import ashtavakra_cast as AV  # noqa: F401  (registers the bamboo staff av_staff)
import dharmavyadha_cast as DV  # noqa: F401  (registers the bowl, cot)
import kaikeyi_cast as K
import lrekha_cast as LR  # noqa: F401  (palm-leaf book, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
import shani_cast as S
import shikhandi_cast as SK
import six_cast_a as SA  # noqa: F401  (Shukra, the medals, the sea)
import six_cast_c as C6
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman, woman_body
from puppet_core import (DRED, GOLD, GREEN, INK, OCHRE, PALE, RED, SAFFRON, almond_eye, band, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, rivet, spath)

BG_SKIN = (0.86, 0.56, 0.32)          # Bhrigu: warm brown
BG_DHOTI = (0.86, 0.20, 0.10)         # deep red
BG_ROBE = (1.0, 0.50, 0.14)           # saffron-red robe over it
BG_HAIR = (0.24, 0.18, 0.16)          # his top-knot: dark, greying
GREY = (0.86, 0.84, 0.80)             # his beard
GREY_D = (0.56, 0.52, 0.50)
ASHW = (1.0, 0.97, 0.90)              # ash lines
TEAR = (0.62, 0.84, 1.0)
LK_SKIN = (1.0, 0.82, 0.62)           # Lakshmi
LK_SARI = (0.94, 0.30, 0.42)          # rose red
LK_PALLU = (0.66, 0.08, 0.20)
LK_RAY = (1.0, 0.70, 0.74)            # pink rays
LOTUS = (1.0, 0.56, 0.66)
LOTUS2 = (0.92, 0.34, 0.48)
BR_RED = (1.0, 0.46, 0.30)            # Brahma, flushed with anger
NAGA = (0.30, 0.62, 0.62)             # Adishesha: sea-green
NAGA2 = (0.18, 0.44, 0.48)
NAGA_B = (0.98, 0.86, 0.50)           # his belly plates
MILK = (0.86, 0.93, 1.0)
MILK2 = (0.68, 0.82, 0.98)

# ------------------------------------------------------------------ Bhrigu

_BG_O = dict(skin=BG_SKIN, hair=False, moustache=False, tilak=False, earring=False)
BG_MOODS = ("calm", "stern", "shout", "shock", "weep", "joy")


def bhrigu_head(cr, mood="calm"):
    """Bhrigu: grey hair down his back, the face (ruru_cast.rface moods), a long grey beard and moustache, a tall dark
    top-knot rising like a flame (rudraksha round its base, a red cloth tie), ash lines and a red dot on his brow."""
    hp = [(-30, -176), (-62, -146), (-80, -70), (-82, 10), (-64, 52), (-44, 24), (-40, -30), (-24, -100)]
    _shape(cr, hp, GREY, 5)
    for k in range(3):
        ink(cr, [(-48 - 9 * k, -140), (-66 - 5 * k, -40), (-58 - 3 * k, 30)], 2.5, col=GREY_D)
    base = {"stern": "calm", "shout": "scold", "joy": "smile"}.get(mood, mood)
    RU.rface(cr, _BG_O, base)
    if mood == "stern":                                                          # a hard, straight brow
        ink(cr, [(6, -146), (34, -146), (62, -136)], 9)
        ink(cr, [(52, -100), (60, -96)], 3)
    elif mood == "shout":
        ink(cr, [(2, -132), (-6, -118)], 3)
    bp = [(62, -48), (64, -22), (58, 40), (44, 130), (24, 84), (4, 26), (8, -40), (30, -52)]
    _shape(cr, bp, GREY, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -38), (42 - 12 * k, 24), (36 - 10 * k, 90)], 2.5, col=GREY_D)
    dy = -8 if mood == "shout" else (-4 if mood == "joy" else 0)
    m = [(66, -76 + dy), (46, -84 + dy), (24, -88 + dy), (12, -74 + dy), (30, -78 + dy), (52, -76 + dy),
         (68, -72 + dy)]
    _shape(cr, m, GREY, 3)
    for k in range(4):                                                           # the piled top-knot
        cr.new_path()
        ell(cr, -8 - 3 * k, -194 - 28 * k, 52 - 7 * k, 22)
        leather(cr, BG_HAIR, 4)
        ink(cr, [(-42 + 6 * k, -194 - 28 * k), (-8, -184 - 28 * k), (28 - 6 * k, -196 - 28 * k)], 2.5, col=GREY_D)
    tuft = [(-30, -282), (-36, -312), (-24, -346), (-8, -384), (2, -352), (14, -322), (20, -300),
            (10, -280)]
    _shape(cr, tuft, BG_HAIR, 4)                                                 # its tip, curling up like a flame
    holes_line(cr, [(-22, -300), (-14, -340)], 12, 2.2)
    band(cr, [(-36, -280), (-8, -286), (22, -280)], 14, RED, spacing=10, hole_r=2.0)
    for i in range(7):                                                           # rudraksha round its base
        cr.new_path()
        cr.arc(-44 + 13 * i, -180, 6, 0, 2 * math.pi)
        leather(cr, (0.46, 0.20, 0.10), 2)
    if mood not in ("shock",):
        for k in range(3):
            ink(cr, [(4, -170 + 8 * k), (44, -172 + 8 * k)], 3, col=ASHW)
    cr.new_path()
    cr.arc(36, -160, 5.5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    if mood == "weep":                                                           # tears on his cheek
        for k, (x0, y0) in enumerate(((34, -100), (46, -96))):
            ink(cr, [(x0, y0), (x0 + 3, y0 + 26), (x0 + 1, y0 + 48)], 6 - k, col=TEAR)
        cr.new_path()
        ell(cr, 38, -46, 6, 9)
        leather(cr, TEAR, 2.5)
    cr.new_path()                                                                # a rudraksha stud
    cr.arc(-14, -72, 9, 0, 2 * math.pi)
    leather(cr, (0.46, 0.20, 0.10), 3)


_BG = dict(skin=BG_SKIN, bulk=0.94, dhoti=BG_DHOTI, border=GOLD, pleat=BG_ROBE, sash=OCHRE, neck=(0.46, 0.20, 0.10),
           beads=True, robe=BG_ROBE)
BHRIGU = man("bg_bhrigu", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_BG)
for _m in BG_MOODS:
    register("bg_bhrigu_head" + ("" if _m == "calm" else "_" + _m), (-200, -400, 120, 150),
             (lambda m: lambda cr: bhrigu_head(cr, m))(_m))


def _limb(p0, p1, w0, w1):
    """A tapered limb outline from p0 to p1 (half-widths w0, w1)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return [(p0[0] + nx * w0, p0[1] + ny * w0), (p1[0] + nx * w1, p1[1] + ny * w1),
            (p1[0] - nx * w1, p1[1] - ny * w1), (p0[0] - nx * w0, p0[1] - ny * w0)]


EXT_KNEE = (186.0, 22.0)              # the stretched leg (seat_ext units): knee and ankle
EXT_ANKLE = (336.0, 64.0)


def _ext_frame():
    """(u, v, heel): the shin's direction, the foot's direction (90 degrees up from the shin) and the heel."""
    ux, uy = EXT_ANKLE[0] - EXT_KNEE[0], EXT_ANKLE[1] - EXT_KNEE[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    return (ux, uy), (uy, -ux), (EXT_ANKLE[0] + ux * 22, EXT_ANKLE[1] + uy * 22)


_u, _v, _h = _ext_frame()
EXT_SOLE = (_h[0] + _u[0] * 14 + _v[0] * 52, _h[1] + _u[1] * 14 + _v[1] * 52)    # the middle of the sole
EXT_INSTEP = (_h[0] - _u[0] * 22 + _v[0] * 50, _h[1] - _u[1] * 22 + _v[1] * 50)  # the top of the foot
EXT_TOES = (_h[0] + _u[0] * 4 + _v[0] * 96, _h[1] + _u[1] * 4 + _v[1] * 96)      # the toes' tips
EXT_HEEL = (_h[0] + _u[0] * 10 - _v[0] * 4, _h[1] + _u[1] * 10 - _v[1] * 4)      # the heel's back


def _seat_ext(cr):
    """Bhrigu seated (hip at 0, 0; the far sole at +268): the far leg hanging down (M.seat_legs' far leg), the near
    leg stretched forward and up, the foot held out (sole facing forward): the foot Vishnu presses."""
    b = 0.94
    cr.save()
    cr.translate(-30, -8)
    dcol = tuple(c * 0.8 for c in BG_DHOTI)
    shin = [(150 * b, 30), (196 * b, 30), (192 * b, 150), (186 * b, 236), (156 * b, 240), (150 * b, 150)]
    _shape(cr, shin, BG_SKIN, 5)
    foot = [(150 * b, 228), (190 * b, 226), (214 * b, 242), (252 * b, 254), (254 * b, 268), (148 * b, 268)]
    _shape(cr, foot, BG_SKIN, 4)
    th = [(-48, -24), (60, -36), (190 * b, -22), (216 * b, 26), (198 * b, 66), (60, 64), (-40, 56)]
    _shape(cr, th, dcol, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(196 * b, -18), (216 * b, 26), (200 * b, 62)], 14, GOLD, spacing=11, hole_r=2.4)
    cr.restore()
    kx, ky = EXT_KNEE
    ax, ay = EXT_ANKLE
    _shape(cr, _limb((kx - 6, ky), (ax, ay), 26, 17), BG_SKIN, 5, smooth=False)
    (ux, uy), (vx, vy), heel = _ext_frame()                                      # the foot, toes up
    pts = [(ax - ux * 16 + vx * -10, ay - uy * 16 + vy * -10), (heel[0] + vx * -8, heel[1] + vy * -8),
           (heel[0] + ux * 12 + vx * 30, heel[1] + uy * 12 + vy * 30),
           (heel[0] + ux * 14 + vx * 80, heel[1] + uy * 14 + vy * 80),
           (heel[0] + ux * 6 + vx * 104, heel[1] + uy * 6 + vy * 104),
           (heel[0] - ux * 12 + vx * 104, heel[1] - uy * 12 + vy * 104),
           (heel[0] - ux * 22 + vx * 70, heel[1] - uy * 22 + vy * 70),
           (ax - ux * 22 + vx * 24, ay - uy * 22 + vy * 24)]
    _shape(cr, pts, BG_SKIN, 4)
    ink(cr, [(heel[0] - ux * 4 + vx * 60, heel[1] - uy * 4 + vy * 60),
             (heel[0] - ux * 10 + vx * 90, heel[1] - uy * 10 + vy * 90)], 2.4)
    band(cr, [(ax - ux * 6 - vx * 18, ay - uy * 6 - vy * 18), (ax - ux * 6 + vx * 18, ay - uy * 6 + vy * 18)], 9,
         (0.46, 0.20, 0.10), spacing=8, hole_r=2.0)
    th = [(-48, -24), (60, -36), (170, -22), (206, 14), (196, 62), (60, 64), (-40, 56)]
    _shape(cr, th, BG_DHOTI, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(184, -18), (208, 18), (196, 58)], 14, GOLD, spacing=11, hole_r=2.4)
    rivet(cr, 0, 0, 9)


register("bg_bhrigu_seat_ext", (-110, -70, 470, 300), _seat_ext)
register("bg_bhrigu_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, BG_SKIN, BG_DHOTI, GOLD, 0.94))

# ------------------------------------------------------------------ Vishnu: more faces, kneeling legs

_VI_O = dict(skin=S.VI_SKIN, hair=True, moustache=False, tilak=False)
VI_MOODS = ("kind", "rest", "speak", "calm")


def vishnu_head(cr, mood="kind"):
    """shani_cast.vishnu_head (rays, the tall kirita with a green flare, the Vaishnava tilak) with a mood: kind (his
    smile), rest (eyes shut, peaceful), speak (a gentle open mouth), calm."""
    M._ray_halo(cr, -30, -250, 136, 220, 18, (S.RAY, GOLD))
    if mood == "rest":
        RU.rface(cr, _VI_O, "sleep")
        ink(cr, [(56, -70), (62, -65), (70, -68)], 3.2)
    elif mood == "speak":
        A.face(cr, _VI_O, "calm")
        RU._cover(cr, S.VI_SKIN, 64, -68, 9, 6)
        cr.new_path()
        ell(cr, 62, -68, 6, 7)
        leather(cr, (0.36, 0.06, 0.10), 2.5)
    else:
        A.face(cr, _VI_O, "smile" if mood == "kind" else "calm")
    ink(cr, [(42, -178), (46, -150), (58, -150), (62, -176)], 4, col=PALE)
    ink(cr, [(52, -152), (53, -176)], 4, col=RED)
    R.kirita(cr, GOLD, None, tall=1.45, flare=GREEN)
    _jewel(cr, 4, -150 + (-222 + 150) * 1.45, 14, RED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.45, 9, GREEN)


for _m in VI_MOODS:
    register("bg_vishnu_head_" + _m, (-260, -560, 200, 130), (lambda m: lambda cr: vishnu_head(cr, m))(_m))


def vishnu_head_lie(cr, mood="rest"):
    """Vishnu's head for lying down on Adishesha: the same face and tilak, a low kirita, no ring of rays (so it rests
    in Lakshmi's lap without spearing her); rest (eyes shut) or calm (awake)."""
    if mood == "rest":
        RU.rface(cr, _VI_O, "sleep")
        ink(cr, [(56, -70), (62, -65), (70, -68)], 3.2)
    else:
        A.face(cr, _VI_O, "calm")
    ink(cr, [(42, -178), (46, -150), (58, -150), (62, -176)], 4, col=PALE)
    ink(cr, [(52, -152), (53, -176)], 4, col=RED)
    R.kirita(cr, GOLD, None, tall=0.62, flare=GREEN)
    _jewel(cr, 4, -150 + (-222 + 150) * 0.62, 12, RED)


for _m in ("rest", "calm"):
    register("bg_vishnu_head_lie_" + _m, (-200, -380, 130, 130), (lambda m: lambda cr: vishnu_head_lie(cr, m))(_m))
register("bg_vishnu_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, S.VI_SKIN, S.VI_DHOTI, RED, 1.1))

# ------------------------------------------------------------------ Lakshmi

LK_MOODS = ("open", "smile", "speak", "down")


def _lotus_crown(cr):
    """A gold crown of two tiers with jewels, a pink lotus on top, pearl strings behind."""
    for k in range(3):
        x = -52 - 9 * k
        for j in range(6):
            cr.new_path()
            cr.arc(x - 2 * j, -150 + 15 * j, 4.5, 0, 2 * math.pi)
            leather(cr, PALE, 2)
    for x0, x1, y0, y1 in ((-50, 54, -150, -200), (-40, 44, -200, -240)):
        _shape(cr, [(x0, y0), (x0 + 6, y1), (x1 - 6, y1), (x1, y0)], GOLD, 5, smooth=False, holes=(7, 11, 2.2))
        band(cr, [(x0 + 4, y0 - 6), (x1 - 4, y0 - 6)], 8, RED, holes=False)
    cx, cy = 2, -244
    for a, L, col in ((-1.05, 70, LOTUS2), (1.05, 70, LOTUS2), (-0.55, 84, LOTUS), (0.55, 84, LOTUS),
                      (0.0, 96, LOTUS)):
        tip = (cx + L * math.sin(a), cy - L * math.cos(a))
        side = (math.cos(a) * 22, math.sin(a) * 22)
        mx, my = (cx + tip[0]) / 2, (cy + tip[1]) / 2
        _shape(cr, [(cx - side[0], cy - side[1]), (mx - side[0] * 1.2, my - side[1] * 1.2), tip,
                    (mx + side[0] * 1.2, my + side[1] * 1.2), (cx + side[0], cy + side[1])], col, 4)
        ink(cr, [(cx, cy - 4), ((cx + tip[0]) / 2, (cy + tip[1]) / 2)], 2.2, col=(0.80, 0.26, 0.40))
    for x, y, c in ((2, -222, RED), (-30, -176, GREEN), (36, -176, GREEN), (2, -178, RED)):
        _jewel(cr, x, y, 8, c)


def lakshmi_head(cr, mood="open"):
    """Lakshmi: a ring of pink and gold rays, her hair in a bun with jasmine, the lotus crown, sindoor in the parting,
    a red bindi, a nose ring, gold earrings."""
    M._ray_halo(cr, -20, -168, 112, 162, 18, (LK_RAY, GOLD))
    S._face_w(cr, LK_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    hp = [(-40, -150), (-70, -110), (-84, -40), (-80, 40), (-60, 80), (-44, 30), (-40, -40), (-30, -100)]
    _shape(cr, hp, HAIR, 4)
    for k in range(3):
        holes_line(cr, [(-50 - 6 * k, -120), (-66 - 4 * k, -40), (-60 - 2 * k, 40)], 15, 2.2)
    for i in range(7):
        _flower(cr, -58 - 8 * math.sin(i), -110 + 26 * i, 8, PALE, 5)
    ink(cr, [(8, -188), (28, -178)], 4, col=RED)
    _lotus_crown(cr)
    if mood == "down":
        S._w_eyes(cr, LK_SKIN, "faint")
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    else:
        S._w_eyes(cr, LK_SKIN, mood)
    if mood == "speak":                                                          # startled: brow raised
        ink(cr, [(12, -138), (30, -146), (48, -140)], 3.5)
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


def _lk_extra(cr):
    """Layered gold necklaces, a lotus-pink pendant, a jewelled waist belt."""
    band(cr, [(-22, -282), (12, -220), (40, -176)], 9, GOLD, spacing=10, hole_r=1.8)
    band(cr, [(-28, -276), (4, -180), (30, -120)], 8, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 32, -110, 12, LOTUS2)
    for x in (-26, -2, 22):
        _jewel(cr, x, -22, 7, GREEN)


_LK = dict(skin=LK_SKIN, skirt=LK_SARI, choli=GOLD, border=GOLD, pallu_col=LK_PALLU, gem=GREEN,
           ornaments_extra=_lk_extra)
LAKSHMI = woman("bg_lakshmi", hands=("open", "open"), **_LK)
for _m in LK_MOODS:
    register("bg_lakshmi_head" + ("" if _m == "open" else "_" + _m), (-240, -390, 190, 110),
             (lambda m: lambda cr: lakshmi_head(cr, m))(_m))
register("bg_lakshmi_body_sit", (-150, -310, 290, 290), DV.wbody_sit(_LK))
SIT_H = DV.BENCH_H                    # seated: hip above the soles

# ------------------------------------------------------------------ Brahma, flushed with anger


def brahma_head_red(cr):
    """six_cast_c.brahma_head with the three faces flushed red and an angry brow."""
    o = dict(C6._BR_O, skin=BR_RED)
    M._ray_halo(cr, 0, -170, 190, 270, 20, (RED, SAFFRON))
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 70, 10)
        cr.scale(sx * 0.82, 0.82)
        A.face(cr, o, "angry")
        C6._white_beard(cr)
        R.kirita(cr, GOLD, None, tall=0.7, flare=RED)
        cr.restore()
    cx, cy = 0, -104
    for dx in (-64, 64):
        cr.new_path()
        ell(cr, cx + dx, cy, 12, 20)
        leather(cr, BR_RED, 4)
    cr.new_path()
    ell(cr, cx, cy, 62, 80)
    leather(cr, BR_RED, 6)
    for sx in (-1, 1):
        cr.save()
        cr.translate(cx + sx * 26, cy - 14)
        cr.scale(sx, 1)
        almond_eye(cr, 0, 0, 34, 11, look=0, col=PALE)
        cr.restore()
        ink(cr, [(cx + sx * 8, cy - 30), (cx + sx * 28, cy - 40), (cx + sx * 48, cy - 50)], 7)     # brows pulled down
    ink(cr, [(cx + 2, cy - 18), (cx - 4, cy + 16), (cx + 6, cy + 20)], 3.5)
    ink(cr, [(cx, cy - 74), (cx, cy - 52)], 5, col=DRED)
    bp = [(cx - 54, cy + 14), (cx - 60, cy + 70), (cx - 36, cy + 130), (cx, cy + 160), (cx + 36, cy + 130),
          (cx + 60, cy + 70), (cx + 54, cy + 14), (cx + 30, cy + 46), (cx, cy + 52), (cx - 30, cy + 46)]
    _shape(cr, bp, C6.AG_WHITE, 4)
    for k in (-2, -1, 0, 1, 2):
        ink(cr, [(cx + 14 * k, cy + 60), (cx + 18 * k, cy + 110), (cx + 12 * k, cy + 140 - 8 * abs(k))], 2.4,
            col=C6.AG_STRAND)
    ms = [(cx - 44, cy + 44), (cx - 20, cy + 28), (cx, cy + 32), (cx + 20, cy + 28), (cx + 44, cy + 44),
          (cx + 20, cy + 40), (cx, cy + 38), (cx - 20, cy + 40)]
    _shape(cr, ms, C6.AG_WHITE, 3)
    C6._crown_front(cr, cx, cy - 62, 78, 200)


register("bg_brahma_head_red", (-300, -500, 300, 120), brahma_head_red)

# ------------------------------------------------------------------ Shiva: more faces


def shiva_head(cr, mood="smile"):
    """shikhandi_cast.shiva_head (piled jata with the crescent moon and rudraksha, locks down his back, the third
    eye, ash lines, big gold earrings) with a mood: smile (glad), shock, angry (brow down, the third eye glowing)."""
    for k, x0 in enumerate((-36, -58)):
        lock = [(x0 + 10, -160), (x0 - 26, -90), (x0 - 40, 10), (x0 - 46 + 6 * k, 100), (x0 - 26, 104),
                (x0 - 18, 10), (x0 - 2, -90), (x0 + 26, -150)]
        _shape(cr, lock, SK.JATA, 4)
        holes_line(cr, [(x0 - 6, -120), (x0 - 28, 0), (x0 - 34, 80)], 16, 2.4)
    o = dict(skin=SK.SI_SKIN, hair=False, moustache=False, tilak=False, earring=False)
    RU.rface(cr, o, mood)
    for k in range(3):
        ink(cr, [(0, -156 + 9 * k), (52, -158 + 9 * k)], 3.4, col=ASHW)
    cr.new_path()                                                                 # the third eye
    if mood == "angry":
        ell(cr, 34, -170, 7, 13)
        leather(cr, (1.0, 0.40, 0.10), 2.5)
        cr.new_path()
        ell(cr, 34, -170, 3, 7)
        cr.set_source_rgb(*DRED)
        cr.fill()
    else:
        ell(cr, 34, -168, 5, 10)
        leather(cr, RED, 2)
    for k in range(5):
        cr.new_path()
        ell(cr, -10 - 2 * k, -196 - 30 * k, 54 - 7 * k, 22)
        leather(cr, SK.JATA, 4)
        ink(cr, [(-50 + 7 * k, -196 - 30 * k), (-10, -186 - 30 * k), (32 - 7 * k, -198 - 30 * k)], 2.5,
            col=(0.58, 0.40, 0.22))
    for i in range(6):
        cr.new_path()
        cr.arc(-40 + 13 * i, -212 + 3 * math.sin(i), 6, 0, 2 * math.pi)
        leather(cr, SK.RUDRA, 2)
    cr.save()                                                                     # the crescent moon
    cr.translate(34, -300)
    cr.rotate(-0.5)
    outer = [(36 * math.cos(a), 36 * math.sin(a)) for a in (math.pi * (-0.62 + 1.24 * i / 16) for i in range(17))]
    inner = [(-14 + 30 * math.cos(a), 30 * math.sin(a)) for a in (math.pi * (0.52 - 1.04 * i / 16)
                                                                  for i in range(17))]
    _shape(cr, outer + inner, (1.0, 0.98, 0.86), 3.5, smooth=False)
    cr.restore()
    for r, col in ((24, GOLD), (14, (1.0, 0.7, 0.3))):
        cr.new_path()
        cr.arc(-12, -62, r, 0, 2 * math.pi)
        leather(cr, col, 3.5)
    punch(cr, [(-12, -62)], 4)


for _m in ("smile", "shock", "angry"):
    register("bg_shiva_head_" + _m, (-200, -470, 120, 130), (lambda m: lambda cr: shiva_head(cr, m))(_m))

# ------------------------------------------------------------------ Parvati kneeling

KNEEL_H = 150.0                       # kneeling: hip above the ground


def wbody_kneel(o):
    """A woman kneeling (hip at 0, 0; the ground at +KNEEL_H): the sari folded over her knees and tucked feet, then
    woman_body's torso, blouse and pallu."""
    def fn(cr):
        fold = [(-110, -30), (40, -46), (150, -10), (206, 60), (214, 130), (196, 150), (-140, 152), (-156, 120),
                (-136, 40)]
        _shape(cr, fold, o["skirt"], 5)
        dots_in(cr, lambda: spath(cr, fold), 22, 3.0, shape="d")
        band(cr, [(-150, 140), (20, 144), (204, 140)], 18, o.get("border", GOLD), spacing=11, hole_r=2.2)
        _shape(cr, [(-150, 118), (-188, 130), (-190, 150), (-146, 152)], o["skin"], 4)        # her heels behind
        for x0, x1 in ((40, 190), (60, 200)):
            ink(cr, [(x0, -20 + (x0 - 40) * 0.2), (x1, 110)], 2.6, smooth=False)
        cr.save()
        cr.rectangle(-400, -600, 800, 610)
        cr.clip()
        woman_body(cr, o)
        cr.restore()
        band(cr, [(-40, -36), (0, -42), (40, -40)], 16, o.get("border", GOLD), spacing=11, hole_r=2.2)
        rivet(cr, 0, 0, 8)
    return fn


_PV = dict(skin=S.PV_SKIN, skirt=S.PV_SARI, choli=S.PV_CHOLI, border=GOLD, pallu_col=S.PV_PALLU, gem=GREEN,
           ornaments_extra=S._pv_extra)
register("bg_parvati_body_kneel", (-200, -320, 230, 170), wbody_kneel(_PV))

# ------------------------------------------------------------------ Adishesha, the ocean of milk


SH_TOP = -262.0                       # the top of Shesha's coils (bed units): Vishnu lies here
SH_HOOD = (-530.0, -910.0)            # the middle of his hood


def _coil(cr, x0, x1, y0, y1, col, col2):
    """One fat coil of the serpent seen side on: a long rounded tube with scale diamonds, a thin band of belly plates
    along its bottom."""
    r = (y1 - y0) / 2
    cy = (y0 + y1) / 2
    pts = [(x0 + r - r * math.sin(math.pi * i / 12), cy - r * math.cos(math.pi * i / 12)) for i in range(13)]
    pts += [(x1 - r + r * math.sin(math.pi * i / 12), cy + r * math.cos(math.pi * i / 12)) for i in range(13)]
    cr.new_path()
    poly(cr, pts)
    cr.set_source_rgb(*col)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.save()
    cr.new_path()
    poly(cr, pts)
    cr.clip()
    cr.new_path()
    cr.rectangle(x0 - 10, cy + r * 0.5, x1 - x0 + 20, r)
    cr.set_source_rgb(*col2)
    cr.fill()
    x = x0 + r * 0.5
    while x < x1 - r * 0.4:
        ink(cr, [(x, cy + r * 0.52), (x + 5, y1)], 2.4, smooth=False)
        x += 26
    cr.restore()
    ink(cr, [(x0 + r * 0.5, cy + r * 0.5), (x1 - r * 0.5, cy + r * 0.5)], 3.5)
    dots_in(cr, lambda: poly(cr, [(x0 + r, y0 + 10), (x1 - r, y0 + 10), (x1 - r, cy + r * 0.36),
                                    (x0 + r, cy + r * 0.36)]), 24, 3.6, shape="d")
    ink(cr, [(x0 + r * 0.7, y0 + 14), (x1 - r * 0.7, y0 + 14)], 2.4, col=NAGA2)


def _cobra(cr, x, y, rot, s=1.0):
    """One cobra hood seen from the front (pivot at its neck): the spread hood, the head on top with two eyes, the
    pale spectacle mark, a red forked tongue."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    hood = [(0, 30), (-26, 10), (-58, -40), (-66, -90), (-50, -130), (-30, -150), (-20, -176), (0, -186), (20, -176),
            (30, -150), (50, -130), (66, -90), (58, -40), (26, 10)]
    _shape(cr, hood, NAGA, 5)
    inner = [(0, 6), (-30, -36), (-40, -86), (-26, -124), (0, -134), (26, -124), (40, -86), (30, -36)]
    _shape(cr, inner, NAGA_B, 3.5)
    for i in range(5):
        ink(cr, [(-26 + 13 * i, -112), (-14 + 7 * i, -30)], 2.2, col=(0.80, 0.62, 0.30))
    for sx in (-1, 1):                                                           # the spectacle mark
        cr.new_path()
        ell(cr, sx * 18, -96, 11, 9)
        leather(cr, NAGA2, 2.5)
        punch(cr, [(sx * 18, -96)], 3.5)
    for sx in (-1, 1):                                                           # the eyes
        cr.new_path()
        ell(cr, sx * 12, -160, 6, 8)
        leather(cr, (1.0, 0.86, 0.30), 2.2)
        cr.new_path()
        ell(cr, sx * 12, -160, 2.2, 5)
        cr.set_source_rgb(*INK)
        cr.fill()
    _shape(cr, [(-3, -186), (0, -212), (-8, -224), (0, -218), (6, -226), (3, -212), (3, -186)], RED, 2, smooth=False)
    cr.restore()


def _shesha(cr):
    """Adishesha as a bed (pivot at the bottom centre; the top of his coils at SH_TOP): three great coils, his tail
    curling up at the right, his neck rising at the left into a fan of five cobra hoods leaning over the bed."""
    cx, cy = SH_HOOD
    inner = [(-520, -250), (-545, -440), (-540, -640), (-500, -800)]
    neck = [(-620, -250), (-650, -420), (-650, -620), (-620, -800), (-560, -880), (-470, -870)] + inner[::-1]
    _shape(cr, neck, NAGA, 5)
    for k in range(11):                                                           # belly plates up the neck
        y = -280 - 50 * k
        for (xa, ya), (xb, yb) in zip(inner, inner[1:]):
            if yb <= y <= ya:
                xr = xa + (xb - xa) * (y - ya) / (yb - ya)
                band(cr, [(xr - 8, y), (xr - 50, y + 6)], 12, NAGA_B, holes=False, lw=3)
    for a, s in ((-1.1, 1.3), (1.1, 1.3), (-0.55, 1.42), (0.55, 1.42), (0.0, 1.6)):   # back to front
        a2 = a + 0.12
        _cobra(cr, cx + 40 * math.sin(a2), cy + 60 - 40 * math.cos(a2), a2, s)
    _coil(cr, -540, 540, -90, 0, NAGA2, NAGA_B)
    _coil(cr, -520, 520, -178, -84, NAGA, NAGA_B)
    tail = [(470, -200), (540, -250), (600, -330), (590, -400), (556, -420), (570, -370), (556, -300), (480, -250)]
    _shape(cr, tail, NAGA, 4)
    _coil(cr, -500, 500, SH_TOP, -168, NAGA, NAGA_B)
    band(cr, [(-470, SH_TOP + 6), (0, SH_TOP + 2), (470, SH_TOP + 6)], 10, GOLD, spacing=14, hole_r=2.4)


register("bg_shesha", (-920, -1260, 660, 10), _shesha)
register("bg_milkA", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, MILK))
register("bg_milkB", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, MILK2))

# ------------------------------------------------------------------ small props


def _sole(cr):
    """A foot-sole print (pivot at its middle; toes up): the ghost of the kick, drawn translucent in the scenes."""
    sole = [(-34, 70), (-44, 20), (-46, -30), (-36, -76), (-10, -96), (20, -94), (40, -70), (44, -20), (36, 30),
            (26, 72), (0, 90)]
    cr.new_path()
    spath(cr, sole)
    cr.set_source_rgb(*INK)
    cr.fill()
    for i, (x, y, r) in enumerate(((-30, -116, 13), (-6, -128, 12), (16, -126, 11), (34, -114, 10),
                                   (46, -98, 8))):
        cr.new_path()
        ell(cr, x, y, r, r * 1.2)
        cr.set_source_rgb(*INK)
        cr.fill()


register("bg_sole", (-60, -150, 60, 100), _sole, tex=0.0)


def _shout(cr):
    """A spiky shout cloud (pivot at its centre, the tail at the lower left), red zig-zags inside: angry words."""
    pts = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        r = 1.0 if i % 2 == 0 else 0.78
        pts.append((300 * r * math.cos(a), 170 * r * math.sin(a)))
    _shape(cr, pts, (1.0, 0.94, 0.80), 6, smooth=False)
    _shape(cr, [(-150, 120), (-250, 230), (-90, 140)], (1.0, 0.94, 0.80), 5, smooth=False)
    for k, y in enumerate((-60, 0, 60)):
        zz = [(-170 + 28 * i, y + (18 if i % 2 else -18)) for i in range(13)]
        ink(cr, zz, 9, smooth=False, col=(0.78, 0.10, 0.06))


register("bg_shout", (-320, -190, 320, 250), _shout)


def _medal_rim(cr):
    """A parchment medallion rim (pivot at its centre): a gold ring with punched holes, a red inner line."""
    cr.new_path()
    cr.arc(0, 0, 176, 0, 2 * math.pi)
    cr.arc_negative(0, 0, 150, 2 * math.pi, 0)
    cr.set_source_rgb(*GOLD)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.new_path()
    cr.arc(0, 0, 150, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(4)
    cr.stroke()
    punch(cr, [(163 * math.cos(2 * math.pi * i / 36), 163 * math.sin(2 * math.pi * i / 36)) for i in range(36)], 3.2)
    cr.new_path()
    cr.arc(0, 0, 142, 0, 2 * math.pi)
    cr.set_source_rgb(*DRED)
    cr.set_line_width(3)
    cr.stroke()


def _medal_face(cr):
    cr.new_path()
    cr.arc(0, 0, 151, 0, 2 * math.pi)
    cr.set_source_rgb(1.0, 0.93, 0.76)
    cr.fill()


register("bg_medal_rim", (-185, -185, 185, 185), _medal_rim)
register("bg_medal_face", (-160, -160, 160, 160), _medal_face)
