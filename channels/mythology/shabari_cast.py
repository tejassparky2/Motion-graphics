"""The leather cast and props for the Shabari reel (videos/shabari.py), in the Togalu Gombeyaata style of the earlier
reels (puppet_cast, lrekha_cast, dharmavyadha_cast, six_cast_a, hanuman_cast): profile figures with big almond eyes,
perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every sprite
name starts with "sb_" followed by a word six_cast_b's own "sb_" sprites never use (sha, sg, sing, ber, bask, cov,
vedi, bloom, bark, path, note, stick, broom), so the two casts can never overwrite each other.

Cast (one look each, kept the same through the video; Shabari, Rama and the sages with dignity):
  SHABARI      a simple, gentle, old forest woman (sb_sha, her own rig, a little stooped): warm brown skin, grey-white
               hair under the end of her sari drawn over her head, a coarse bark-brown cotton sari with a dark border,
               a leaf-green blouse, a string of wooden beads, wooden bangles, no gold. Faces: calm, smile, look
               (looking out down the path, hopeful), joy (eyes shut with joy, a tear), shut (eyes peacefully shut).
               Kneels (sb_sha_kneel + sb_sha_torso) to touch Rama's feet. Props: her knotted stick (sb_stick), a
               twig broom (sb_broom), a round bamboo basket with a handle (sb_bask_back / sb_bask) that fills with
               berries (sb_ber red, sb_ber_y yellow, sb_ber_bit a bitten one).
  RAMA         kaikeyi_cast.RAMA (the Lakshman Rekha reel's Rama: blue skin, gold kirita, green halo, his bow).
  THE SAGES    of Matanga's hermitage: six_cast_a.SHUKRA's puppet and ruru_cast.RISHI's puppet (white hair and long
               white beards), seated cross-legged here (sb_sgA_* / sb_sgB_*: their bodies with the pleats tucked, a
               crossed-legs seat).
  THE SINGER   a bhajan singer (sb_sing, puppet_cast.man): dark hair, a saffron head-cloth, a moustache, a sandal
               tilak, a cream dhoti and a saffron shawl. Faces: calm, sing (eyes shut, mouth open), sing2 (half
               open). He holds six_cast_c's clay hand lamp.
Props: two book covers (sb_cov_v: the Valmiki Ramayana, saffron; sb_cov_t: the Ramcharitmanas, deep red; the titles are
drawn over them per frame), the sages' brick fire altar (sb_vedi) with its offered flowers fresh (sb_bloom) or, as the
viewer would expect after years, wilted (sb_bloom_dry), bark cloth hanging dripping on a branch (sb_bark), the path
to the hermitage (sb_path), a music note (sb_note).

Every sprite is drawn once in design units and cached by puppet_core.
"""
import math
import random

import dharmavyadha_cast as DV
import kaikeyi_cast as K
import ruru_cast as RU
import six_cast_a as SA
from puppet_cast import _flower, _shape, fore_arm, man
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, SAFFRON, Rig, almond_eye,
                         band, dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet, spath)

SKIN = (0.86, 0.60, 0.40)             # Shabari: warm brown
SARI = (0.80, 0.53, 0.27)             # coarse bark-brown cotton
VEIL = (0.92, 0.70, 0.42)             # the sari's end over her head (sun-faded)
BORDER = (0.48, 0.22, 0.10)           # its plain dark border
BLOUSE = (0.34, 0.54, 0.28)           # leaf green
ASH = (0.90, 0.89, 0.86)              # grey-white hair
ASH2 = (0.62, 0.60, 0.58)
BEAD = (0.56, 0.34, 0.16)             # wooden beads and bangles
TEAR = (0.62, 0.84, 1.0)
WOOD = (0.62, 0.40, 0.20)
WOOD2 = (0.46, 0.28, 0.13)
BAMBOO = (0.90, 0.72, 0.40)
BAMBOO2 = (0.70, 0.50, 0.24)
BER_R = (0.86, 0.20, 0.10)            # ripe ber (Indian jujube): red
BER_Y = (0.98, 0.70, 0.16)            # half-ripe: yellow-orange
FLESH = (1.0, 0.94, 0.74)
BRICK = (0.80, 0.42, 0.24)
BRICK2 = (0.92, 0.58, 0.34)
LOTUS = (1.0, 0.56, 0.62)
LOTUS2 = (0.94, 0.36, 0.46)
MARI = (1.0, 0.62, 0.12)              # marigold
DRY = (0.58, 0.42, 0.26)              # wilted flowers
DRY2 = (0.44, 0.32, 0.20)
BARK = (0.58, 0.36, 0.18)
BARK2 = (0.76, 0.52, 0.28)
EARTH = (0.94, 0.78, 0.52)
EARTH2 = (0.80, 0.60, 0.34)
SG_SKIN = (0.93, 0.68, 0.46)          # the singer
SG_SHAWL = (1.0, 0.56, 0.14)
SG_CLOTH = (1.0, 0.94, 0.80)

KNEEL_H = 196.0                       # Shabari kneeling: hip above the ground
BASK_RIM = 130.0                      # basket: the rim's centre below the handle's top (basket units)
BASK_RX, BASK_RY = 150.0, 34.0        # the rim ellipse
# where the berries sit in the basket (basket units, the rim at y = BASK_RIM): filled in this order
HEAP = [(-96, 118), (-48, 122), (0, 124), (48, 122), (96, 118), (-72, 96), (-24, 98), (24, 98), (72, 96),
        (-48, 74), (0, 74), (48, 74), (-24, 52), (24, 52), (0, 32)]


# ------------------------------------------------------------------ Shabari


def sha_head(cr, mood="calm"):
    """Shabari's head (neck at 0, 0, facing +x): the end of her sari drawn over the back of her head and falling
    behind, grey-white hair at the temple, an old, kind face with wrinkles, a sandal mark. mood: calm | smile | look |
    joy | shut."""
    vp = [(-28, -188), (6, -210), (42, -200), (60, -176), (42, -168), (8, -178), (-24, -162), (-44, -124),
          (-48, -60), (-40, 0), (-36, 50), (-62, 84), (-84, 52), (-80, -20), (-74, -104), (-60, -164)]
    _shape(cr, vp, VEIL, 5)
    dots_in(cr, lambda: spath(cr, vp), 21, 2.6)
    ink(cr, [(-58, -150), (-66, -70), (-66, 30)], 2.6, col=SARI)                     # its folds
    band(cr, [(-50, -20), (-44, 30), (-50, 70)], 10, BORDER, spacing=11, hole_r=2.0)
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148),
            (54, -126), (58, -116), (74, -98), (60, -88), (62, -80), (55, -73), (58, -64), (50, -50), (42, -38),
            (30, -28), (22, 6)]
    _shape(cr, face, SKIN, 6)
    hair = [(-36, -170), (4, -188), (40, -178), (48, -162), (20, -162), (-8, -150), (-26, -120), (-38, -100),
            (-46, -130)]
    _shape(cr, hair, ASH, 4)
    for k in range(3):
        ink(cr, [(-28 + 10 * k, -168 + 4 * k), (-14 + 12 * k, -158), (6 + 10 * k, -164 + 2 * k)], 2.2, col=ASH2)
    band(cr, [(-32, -180), (6, -200), (46, -184), (56, -168)], 14, BORDER, spacing=12, hole_r=2.2)
    # eye and brow
    if mood in ("smile", "joy"):
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        if mood == "joy":
            for x in (22, 30, 38):
                ink(cr, [(x, -114), (x - 1, -106)], 2.2)
            for k, (x0, y0) in enumerate(((40, -100), (46, -96))):                # a tear of joy
                ink(cr, [(x0, y0), (x0 + 4, y0 + 22), (x0 + 2, y0 + 40)], 5 - k, col=TEAR)
        ink(cr, [(12, -136), (30, -142), (48, -136)], 5, col=ASH)
    elif mood == "shut":
        ink(cr, [(14, -114), (30, -106), (46, -114)], 4.5)
        for x in (22, 30, 38):
            ink(cr, [(x, -109), (x - 2, -101)], 2.2)
        ink(cr, [(12, -132), (30, -138), (48, -134)], 5, col=ASH)
    elif mood == "look":
        almond_eye(cr, 31, -114, 32, 12, col=PALE)
        ink(cr, [(12, -142), (32, -150), (52, -142)], 5, col=ASH)                 # brows raised: hopeful
    else:
        almond_eye(cr, 30, -112, 30, 10, col=PALE)
        ink(cr, [(15, -121), (30, -125), (45, -120)], 3)                          # a heavy, old lid
        ink(cr, [(12, -136), (30, -142), (48, -136)], 5, col=ASH)
    # wrinkles: crow's feet, the forehead, the cheek
    ink(cr, [(48, -110), (58, -104)], 2.2)
    ink(cr, [(49, -116), (59, -116)], 2.0)
    ink(cr, [(16, -154), (40, -158)], 2.0)
    ink(cr, [(20, -147), (38, -150)], 1.8)
    ink(cr, [(40, -96), (46, -82), (44, -72)], 2.2)
    ink(cr, [(10, -92), (6, -76)], 2.0)
    # mouth
    if mood in ("smile", "joy"):
        ink(cr, [(48, -72), (55, -66), (62, -70)], 3.5, col=(0.50, 0.16, 0.12))
    else:
        ink(cr, [(60, -71), (52, -69)], 3, col=(0.50, 0.16, 0.12))
    ink(cr, [(52, -56), (46, -50)], 2.0)                                          # a soft chin line
    ink(cr, [(46, -160), (46, -146)], 4.5, col=PALE)                             # a sandal-paste mark


SHA_MOODS = ("calm", "smile", "look", "joy", "shut")


def _sha_torso(cr):
    """Her torso (hip at 0, 0): a gentle stoop, the green blouse's sleeve, the sari's end across her chest and over
    her shoulder, hanging down her back; a string of wooden beads; the waist."""
    pal_back = [(-14, -284), (14, -286), (-8, -200), (-44, -60), (-84, 110), (-122, 96), (-92, -50), (-62, -200)]
    _shape(cr, pal_back, VEIL, 5)
    dots_in(cr, lambda: spath(cr, pal_back), 21, 2.6)
    band(cr, [(-118, 92), (-86, 104)], 12, BORDER, spacing=10, hole_r=2.0)
    torso = [(-38, -10), (-46, -120), (-50, -196), (-38, -252), (-12, -284), (24, -290), (44, -268), (64, -230),
             (68, -206), (56, -180), (46, -120), (40, -10)]
    _shape(cr, torso, SKIN, 6)
    blouse = [(-48, -244), (-20, -282), (22, -288), (42, -266), (64, -230), (68, -206), (54, -180), (-48, -178)]
    _shape(cr, blouse, BLOUSE, 5, holes=(9, 12, 2.4))
    # the sari's end, across the chest from the waist (front) up over the back shoulder
    pal = [(46, -26), (60, -120), (70, -196), (52, -244), (20, -282), (-14, -290), (-34, -270), (-6, -216),
           (16, -150), (14, -60), (6, -24)]
    _shape(cr, pal, VEIL, 5)
    dots_in(cr, lambda: spath(cr, pal), 21, 2.6)
    for x0, x1 in ((10, 40), (24, 56), (40, 62)):
        ink(cr, [(x0, -40), (x1, -190)], 2.4, col=SARI)
    band(cr, [(48, -30), (62, -120), (72, -196), (54, -246)], 12, BORDER, spacing=12, hole_r=2.0)
    for i in range(9):                                                            # wooden beads
        u = i / 8
        cr.new_path()
        cr.arc(-16 + 60 * u, -276 + 60 * u + 34 * u * u, 6.5, 0, 2 * math.pi)
        leather(cr, BEAD, 2.5)
    band(cr, [(-40, -22), (0, -28), (44, -24)], 16, BORDER, spacing=11, hole_r=2.2)
    rivet(cr, 0, 0, 8)


def _sha_body(cr):
    """Standing: the sari straight to her ankles (a little flare, pleats, a plain border), her toes, then the torso."""
    skirt = [(-42, -30), (42, -34), (64, 120), (84, 300), (104, 446), (94, 466), (-92, 466), (-100, 446),
             (-78, 300), (-60, 120)]
    _shape(cr, skirt, SARI, 6)
    dots_in(cr, lambda: spath(cr, skirt), 24, 3.0, shape="d")
    for x0, x1 in ((-8, -30), (12, 24), (30, 62), (46, 90)):
        ink(cr, [(x0, 0), (x1, 440)], 2.6, smooth=False, col=BORDER)
    band(cr, [(-98, 440), (0, 444), (102, 440)], 24, BORDER, spacing=13, hole_r=2.4)
    _shape(cr, [(84, 456), (126, 460), (132, 474), (80, 476)], SKIN, 4)          # toes
    for x in (110, 120):
        ink(cr, [(x, 462), (x + 2, 472)], 2.0)
    _sha_torso(cr)


def _sha_kneel(cr):
    """Kneeling (hip at 0, 0; the ground at y = +KNEEL_H): the sari folded over her thighs and shins, her toes
    tucked behind."""
    _shape(cr, [(-118, 176), (-84, 168), (-80, 196), (-122, 198)], SKIN, 4)       # toes behind
    leg = [(-50, -30), (46, -36), (120, 40), (178, 128), (182, 186), (150, 198), (-90, 198), (-100, 150), (-78, 40)]
    _shape(cr, leg, SARI, 6)
    dots_in(cr, lambda: spath(cr, leg), 24, 3.0, shape="d")
    ink(cr, [(-60, 120), (40, 110), (150, 150)], 2.6, col=BORDER)
    ink(cr, [(-20, 20), (80, 60), (150, 120)], 2.6, col=BORDER)
    band(cr, [(-92, 188), (40, 192), (160, 190)], 20, BORDER, spacing=13, hole_r=2.4)
    rivet(cr, 0, 0, 8)


def _sha_upper(cr):
    """An upper arm in the blouse's short sleeve (thin, old)."""
    pts = [(-22, -8), (-14, -28), (0, -32), (16, -28), (24, -8), (20, 80), (14, 150), (0, 162), (-14, 150), (-20, 80)]
    _shape(cr, pts, SKIN, 5)
    sl = [(-24, -10), (-14, -32), (0, -36), (16, -32), (26, -10), (24, 62), (-22, 62)]
    _shape(cr, sl, BLOUSE, 5)
    band(cr, [(-23, 56), (24, 58)], 10, BORDER, spacing=10, hole_r=2.0)
    rivet(cr, 0, 0, 6)


_ARM = dict(skin=SKIN, bulk=0.8, neck=BEAD)


def _sha_fore(cr, hand):
    fore_arm(cr, _ARM, None, hand)


register("sb_sha_body", (-140, -310, 150, 490), _sha_body)
register("sb_sha_torso", (-140, -310, 150, 130), _sha_torso)
register("sb_sha_kneel", (-140, -60, 200, 210), _sha_kneel)
for _m in SHA_MOODS:
    register("sb_sha_head" + ("" if _m == "calm" else "_" + _m), (-140, -220, 90, 90),
             (lambda m: lambda cr: sha_head(cr, m))(_m))
register("sb_sha_armF_up", (-35, -45, 35, 175), _sha_upper)
register("sb_sha_armB_up", (-35, -45, 35, 175), _sha_upper)
register("sb_sha_armF_lo", (-45, -30, 45, 210), lambda cr: _sha_fore(cr, "open"))
register("sb_sha_armB_lo", (-45, -30, 45, 210), lambda cr: _sha_fore(cr, "fist"))
register("sb_sha_armF_lo_fist", (-45, -30, 45, 210), lambda cr: _sha_fore(cr, "fist"))
register("sb_sha_armB_lo_open", (-45, -30, 45, 210), lambda cr: _sha_fore(cr, "open"))

SHABARI = Rig([("sb_sha_armB_up", "sb_sha_body", (-4, -258), 0.15),
               ("sb_sha_armB_lo", "sb_sha_armB_up", (0, 150), -0.2),
               ("sb_sha_body", None, (0, 0), 0.0),
               ("sb_sha_head", "sb_sha_body", (12, -288), 0.0),
               ("sb_sha_armF_up", "sb_sha_body", (30, -258), -0.08),
               ("sb_sha_armF_lo", "sb_sha_armF_up", (0, 150), -0.35)],
              {"handF": ("sb_sha_armF_lo", (6, 160)), "handB": ("sb_sha_armB_lo", (4, 150)),
               "chest": ("sb_sha_body", (10, -200)), "head": ("sb_sha_head", (10, -110)),
               "top": ("sb_sha_head", (0, -205)), "mouth": ("sb_sha_head", (58, -70)),
               "hip": ("sb_sha_body", (0, 0))},
              [("chest", 30, 0), ("handF", 140, 0)])
SHA_SHOULDER_F = (30.0, -258.0)       # shoulders in her root coordinates (for reach_arm-style aiming)
SHA_SHOULDER_B = (-4.0, -258.0)


# ------------------------------------------------------------------ her things


def _berry(cr, col, bit=False, leaf=True):
    """A ber (Indian jujube; centre pivot, ~50 x 56 units): a glossy oval, a stem and a small leaf; bit = a bite taken
    out of its front, the pale flesh showing."""
    _shape(cr, [(-6, -26), (0, -40), (6, -26)], WOOD2, 2.5, smooth=False)
    if leaf:
        _shape(cr, [(2, -36), (22, -50), (34, -44), (18, -34)], GREEN, 2.5)
    body = [(0, -28), (20, -22), (27, 0), (20, 24), (0, 30), (-20, 24), (-27, 0), (-20, -22)]
    _shape(cr, body, col, 4)
    if bit:
        bite = [(14, -24), (6, -12), (10, -2), (4, 8), (10, 18), (24, 22), (32, 0), (28, -20)]
        cr.save()
        cr.new_path()
        spath(cr, body)
        cr.clip()
        _shape(cr, bite, FLESH, 3)
        cr.restore()
        for y in (-8, 6):
            ink(cr, [(12, y - 4), (16, y), (12, y + 4)], 2.2, col=(0.80, 0.62, 0.36))
    punch(cr, [(-10, -10)], 4.5)
    punch(cr, [(-14, -2)], 2.2)


register("sb_ber", (-34, -56, 40, 36), lambda cr: _berry(cr, BER_R))
register("sb_ber_y", (-34, -56, 40, 36), lambda cr: _berry(cr, BER_Y))
register("sb_ber_bit", (-34, -56, 40, 36), lambda cr: _berry(cr, BER_R, True))


def _bunch(cr, bit=False):
    """A small bunch of ber on a twig (centre pivot, ~150 units): three berries, two leaves; bit = the front one
    has a bite taken out of it (the picture people know)."""
    ink(cr, [(-70, -86), (-30, -60), (0, -40)], 7, col=WOOD2)
    ink(cr, [(-30, -60), (-40, -20)], 5, col=WOOD2)
    ink(cr, [(-12, -50), (34, -24)], 5, col=WOOD2)
    for x, y, a in ((-60, -100, -0.6), (-6, -76, 0.5)):
        cr.save()
        cr.translate(x, y)
        cr.rotate(a)
        _shape(cr, [(-12, 0), (-24, -30), (0, -58), (24, -30), (12, 0)], GREEN, 3)
        ink(cr, [(0, -4), (0, -46)], 2, col=DGREEN)
        cr.restore()
    for x, y, col, s, b in ((-44, 8, BER_Y, 1.0, False), (38, 16, BER_R, 1.0, False), (-2, 38, BER_R, 1.25, bit)):
        cr.save()
        cr.translate(x, y)
        cr.scale(s, s)
        _berry(cr, col, b, leaf=False)
        cr.restore()


register("sb_ber3", (-90, -170, 90, 90), lambda cr: _bunch(cr, False))
register("sb_ber3_bit", (-90, -170, 90, 90), lambda cr: _bunch(cr, True))


def _bask_back(cr):
    """The basket's inside back wall (pivot at the handle's top, the rim's centre at (0, BASK_RIM)): dark weave."""
    cr.new_path()
    ell(cr, 0, BASK_RIM, BASK_RX - 6, BASK_RY - 4)
    leather(cr, BAMBOO2, 4)
    for k in range(7):
        x = -120 + 40 * k
        ink(cr, [(x, BASK_RIM - 26 + abs(x) * 0.05), (x + 8, BASK_RIM - 2)], 2.4, col=WOOD2)


def _bask_front(cr):
    """The basket's front (pivot at the handle's top): a round woven bowl, its rim, a bent-cane handle."""
    rim_y = BASK_RIM
    bowl = [(-BASK_RX, rim_y), (-140, rim_y + 60), (-112, rim_y + 116), (-80, rim_y + 144), (0, rim_y + 152),
            (80, rim_y + 144), (112, rim_y + 116), (140, rim_y + 60), (BASK_RX, rim_y), (100, rim_y + 22),
            (0, rim_y + 34), (-100, rim_y + 22)]
    _shape(cr, bowl, BAMBOO, 6)
    cr.save()
    cr.new_path()
    spath(cr, bowl)
    cr.clip()
    for k in range(-6, 7):                                                        # the weave: crossing strips
        ink(cr, [(k * 34 - 60, rim_y + 20), (k * 34 + 60, rim_y + 160)], 3, smooth=False, col=BAMBOO2)
        ink(cr, [(k * 34 + 60, rim_y + 20), (k * 34 - 60, rim_y + 160)], 3, smooth=False, col=BAMBOO2)
    cr.restore()
    dots_in(cr, lambda: spath(cr, bowl), 34, 3.0, shape="d")
    band(cr, [(-146, rim_y + 6), (-90, rim_y + 26), (0, rim_y + 36), (90, rim_y + 26), (146, rim_y + 6)], 16,
         WOOD, spacing=13, hole_r=2.4)
    band(cr, [(-104, rim_y + 120), (0, rim_y + 140), (104, rim_y + 120)], 10, WOOD, spacing=12, hole_r=2.0)
    band(cr, [(-136, rim_y + 4), (-120, rim_y - 70), (-60, rim_y - 124), (0, -4), (60, rim_y - 124),
              (120, rim_y - 70), (136, rim_y + 4)], 14, WOOD, spacing=14, hole_r=2.2)   # the cane handle
    for x in (-136, 136):
        band(cr, [(x - 10, rim_y - 6), (x + 10, rim_y + 14)], 8, WOOD2, holes=False)


register("sb_bask_back", (-160, 90, 160, 170), _bask_back)
register("sb_bask", (-165, -20, 165, 300), _bask_front)


def _stick(cr):
    """Her walking stick (pivot at the grip, near the top): a knotted forest branch, a little crooked."""
    pts = [(-12, -60), (10, -64), (14, 0), (8, 160), (16, 320), (10, 500), (-10, 504), (-6, 320), (-12, 160), (-8, 0)]
    _shape(cr, pts, WOOD, 5)
    for y in (90, 250, 410):
        ink(cr, [(-12, y), (2, y - 8), (14, y + 2)], 3, col=WOOD2)
    _shape(cr, [(-8, -60), (-30, -84), (-24, -92), (6, -66)], WOOD, 4)            # a knob of the old branch
    holes_line(cr, [(0, 30), (2, 470)], 32, 2.4)


register("sb_stick", (-40, -100, 30, 512), _stick)


def _broom(cr):
    """A twig broom (pivot at the grip): a bound handle of twigs fanning out into a brush."""
    for k in range(-5, 6):
        ink(cr, [(k * 2, -40), (k * 4, 160), (k * 13, 330)], 4, col=WOOD2)
        ink(cr, [(k * 2, -40), (k * 4, 160), (k * 13, 330)], 2, col=BAMBOO)
    for y in (-30, 30, 90):
        band(cr, [(-14, y), (14, y + 2)], 12, RED, holes=False)


register("sb_broom", (-80, -60, 80, 345), _broom)


# ------------------------------------------------------------------ the books


def _cover(cr, col, col2, trim):
    """A bound book's cloth cover (centre pivot, 440 x 600): a trim border with punched holes, a pale title panel
    at the top, a pale round medallion lower down (its picture is drawn per frame), corner lotuses."""
    w, h = 220, 300
    pts = [(-w, -h + 20), (-w + 20, -h), (w - 20, -h), (w, -h + 20), (w, h - 20), (w - 20, h), (-w + 20, h),
           (-w, h - 20)]
    _shape(cr, pts, col, 7, smooth=False, holes=(14, 18, 3.2))
    for d in (34, 50):
        poly(cr, [(-w + d, -h + d), (w - d, -h + d), (w - d, h - d), (-w + d, h - d)])
        cr.set_source_rgb(*trim)
        cr.set_line_width(5 if d == 34 else 3)
        cr.stroke()
    _shape(cr, [(-170, -250), (170, -250), (178, -236), (178, -110), (170, -96), (-170, -96), (-178, -110),
                (-178, -236)], PARCH, 5, smooth=False)
    cr.new_path()
    cr.arc(0, 110, 118, 0, 2 * math.pi)
    leather(cr, trim, 5)
    cr.new_path()
    cr.arc(0, 110, 100, 0, 2 * math.pi)
    leather(cr, PARCH, 4)
    for i in range(24):
        a = 2 * math.pi * i / 24
        punch(cr, [(109 * math.cos(a), 110 + 109 * math.sin(a))], 2.6)
    for x, y in ((-w + 42, -h + 42), (w - 42, -h + 42), (-w + 42, h - 42), (w - 42, h - 42)):
        _flower(cr, x, y, 16, trim, 6)
    band(cr, [(-150, -60), (150, -60)], 10, col2, holes=False)
    band(cr, [(-150, 266), (150, 266)], 10, col2, holes=False)
    for x in (-w - 6, ):
        for y in (-240, -120, 0, 120, 240):                                     # the binding stitches
            ink(cr, [(x, y - 14), (x + 22, y), (x, y + 14)], 4, smooth=False, col=INK)


register("sb_cov_v", (-232, -312, 232, 312), lambda cr: _cover(cr, (1.0, 0.60, 0.16), DRED, GOLD))
register("sb_cov_t", (-232, -312, 232, 312), lambda cr: _cover(cr, (0.74, 0.12, 0.10), GOLD, GOLD))


# ------------------------------------------------------------------ the hermitage


def _vedi(cr):
    """The sages' brick fire altar (pivot at the bottom centre): three steps of brick, a sacred-ash band, a hollow
    on top where the flowers were laid."""
    steps = ((0, 200, 70), (-70, 160, 60), (-130, 120, 50))
    for y0, w, hh in steps:
        pts = [(-w, y0), (w, y0), (w - 8, y0 - hh), (-w + 8, y0 - hh)]
        _shape(cr, pts, BRICK, 6, smooth=False)
        cr.save()
        cr.new_path()
        poly(cr, pts)
        cr.clip()
        for r in range(3):                                                        # brick courses
            yy = y0 - hh * (r + 1) / 3
            ink(cr, [(-w, yy), (w, yy)], 2.4, smooth=False, col=(0.56, 0.24, 0.12))
            off = 0 if r % 2 else 30
            for x in range(int(-w) + off, int(w), 60):
                ink(cr, [(x, yy), (x, yy + hh / 3)], 2.4, smooth=False, col=(0.56, 0.24, 0.12))
        cr.restore()
    for k in range(3):                                                            # three ash lines on the front
        ink(cr, [(-60, -40 - 10 * k), (60, -40 - 10 * k)], 4, smooth=False, col=PALE)
    cr.new_path()
    cr.arc(0, -50, 7, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


register("sb_vedi", (-210, -190, 210, 10), _vedi)


def _lotus_bloom(cr, x, y, s, col, col2, dry):
    """One lotus seen from the side (pivot at its base)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if dry:                                                                       # drooping, shrivelled petals
        for a, L in ((-1.9, 60), (-1.2, 70), (1.2, 70), (1.9, 60), (0.0, 52)):
            cr.save()
            cr.rotate(a * 0.55 + 0.5)
            _shape(cr, [(-12, 0), (-8, L * 0.6), (0, L), (8, L * 0.6), (12, 0)], col, 3)
            cr.restore()
        cr.new_path()
        ell(cr, 0, -6, 20, 14)
        leather(cr, col2, 3)
    else:
        for a, L, c in ((-1.0, 74, col2), (1.0, 74, col2), (-0.5, 86, col), (0.5, 86, col), (0.0, 92, col)):
            cr.save()
            cr.rotate(a)
            _shape(cr, [(-16, 0), (-18, -L * 0.55), (0, -L), (18, -L * 0.55), (16, 0)], c, 3)
            ink(cr, [(0, -8), (0, -L * 0.7)], 2, col=col2)
            cr.restore()
        cr.new_path()
        ell(cr, 0, 2, 26, 12)
        leather(cr, GOLD, 3)
    cr.restore()


def _bloom(cr, dry=False):
    """The flowers the sages offered on the altar (pivot at the bottom centre, sitting on the altar's top): lotuses,
    a marigold garland draped over the edge, a few leaves; dry = the same flowers wilted, brown and drooping."""
    lc, lc2 = (DRY, DRY2) if dry else (LOTUS, LOTUS2)
    mc = DRY2 if dry else MARI
    leaf = (0.60, 0.52, 0.30) if dry else GREEN
    for x, a in ((-110, -0.5), (100, 0.6), (-30, -0.1), (40, 0.2)):              # leaves
        cr.save()
        cr.translate(x, -6)
        cr.rotate(a + (0.9 if dry else 0.0) * (1 if a > 0 else -1))
        _shape(cr, [(-14, 0), (-30, -50), (0, -96), (30, -50), (14, 0)], leaf, 3)
        ink(cr, [(0, -6), (0, -80)], 2, col=DGREEN if not dry else DRY2)
        cr.restore()
    for x, y, s in ((-70, -10, 0.9), (70, -10, 0.95), (0, -24, 1.15)):
        _lotus_bloom(cr, x, y, s, lc, lc2, dry)
    for i in range(14):                                                            # the garland along the edge
        u = i / 13
        x = -150 + 300 * u
        y = 4 + 36 * math.sin(math.pi * u) * (1.4 if dry else 1.0)
        _flower(cr, x, y, 13 if not dry else 10, mc, 8)


register("sb_bloom", (-170, -140, 170, 60), lambda cr: _bloom(cr, False))
register("sb_bloom_dry", (-170, -110, 170, 70), lambda cr: _bloom(cr, True))


def _bark(cr):
    """A bark-cloth garment hung over a branch to dry (pivot at the branch, seen from the front): a wide cloth draped
    over it, the back half peeking out at one side, soft folds, a wavy fringed hem, dark wet streaks."""
    rng = random.Random(7)
    back = [(-60, -14), (96, -14), (104, 120), (98, 226), (60, 236), (40, 120)]
    _shape(cr, back, BARK, 5)
    front = [(-96, -16), (-60, -26), (0, -30), (60, -26), (90, -16), (98, 80), (94, 190), (100, 270), (70, 282),
             (40, 270), (10, 286), (-20, 272), (-50, 288), (-80, 274), (-100, 280), (-98, 180), (-104, 80)]
    _shape(cr, front, BARK2, 6)
    for k in range(7):                                                            # the fibre and the folds
        x = -78 + 26 * k + rng.uniform(-3, 3)
        ink(cr, [(x, -14), (x + rng.uniform(-6, 6), 130), (x + rng.uniform(-4, 4), 262)], 2.4,
            col=(0.46, 0.28, 0.14))
    for x in (-50, 18, 62):                                                       # wet, darker streaks
        _shape(cr, [(x - 9, 30), (x + 9, 30), (x + 11, 230), (x, 250), (x - 11, 230)], BARK, 0)
    for k in range(17):                                                           # the fringe
        x = -96 + 12 * k
        y0 = 276 + 8 * math.sin(k * 1.3)
        ink(cr, [(x, y0), (x + rng.uniform(-4, 4), y0 + 20 + rng.uniform(0, 10))], 3.2, col=BARK2)
    holes_line(cr, [(-80, 10), (80, 10)], 18, 2.4)
    holes_line(cr, [(-84, 250), (84, 250)], 18, 2.2)


register("sb_bark", (-120, -50, 120, 330), _bark)


def _path(cr):
    """The path to the hermitage, seen from the side as the puppets stand on it (pivot at the centre of its top
    edge): a long strip of pale trodden earth with pebbles, footprints and grass tufts along its top edge."""
    rng = random.Random(3)
    top = [(-760 + 1520 * i / 30, 6 * math.sin(i * 1.7)) for i in range(31)]
    _shape(cr, top + [(760, 60), (-760, 64)], EARTH, 6, smooth=False)
    for _ in range(46):
        cr.new_path()
        ell(cr, rng.uniform(-730, 730), rng.uniform(16, 50), rng.uniform(5, 11), rng.uniform(3, 5))
        leather(cr, EARTH2, 2)
    for i in range(12):                                                           # bare footprints along it
        x = -700 + 125 * i
        cr.new_path()
        ell(cr, x, 30 + (6 if i % 2 else -4), 14, 6)
        leather(cr, EARTH2, 0)
    for i in range(0, 31, 3):                                                     # grass tufts on the top edge
        px, py = top[i]
        px += rng.uniform(-14, 14)
        for j in (-1, 0, 1):
            poly(cr, [(px + 9 * j - 4, py + 2), (px + 13 * j, py - 30 - 6 * (j == 0)), (px + 9 * j + 4, py + 2)])
            leather(cr, GREEN, 2.5)


register("sb_path", (-770, -50, 770, 72), _path)


def _note(cr):
    """A music note (pivot at its head): a round head, a stem, a flag."""
    cr.new_path()
    ell(cr, 0, 0, 22, 16, -0.4)
    leather(cr, INK, 2)
    band(cr, [(18, -4), (18, -110)], 9, INK, holes=False, lw=0)
    _shape(cr, [(18, -112), (52, -84), (58, -50), (44, -64), (22, -82)], INK, 2)


register("sb_note", (-30, -125, 70, 25), _note)


# ------------------------------------------------------------------ the sages, seated


_SG_A = dict(skin=SA.SH_SKIN, bulk=1.0, dhoti=SA.SH_DHOTI, border=DRED, pleat=(1.0, 0.74, 0.36), sash=DRED,
             neck=BROWN, robe=SA.SH_ROBE, beads=True)
_SG_B = dict(skin=RU.RS_SKIN, bulk=0.9, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=OCHRE, neck=BROWN,
             robe=(1.0, 0.70, 0.36), beads=True)
register("sb_sgA_body_sit", (-200, -330, 140, 80), DV._sit_body(_SG_A))
register("sb_sgA_seat", (-110, -60, 280, 110), lambda cr: DV._cross_seat(cr, SA.SH_DHOTI, DRED, SA.SH_SKIN))
register("sb_sgB_body_sit", (-200, -330, 140, 80), DV._sit_body(_SG_B))
register("sb_sgB_seat", (-110, -60, 280, 110), lambda cr: DV._cross_seat(cr, PALE, SAFFRON, RU.RS_SKIN))
SAGE_A, SAGE_B = SA.SHUKRA, RU.RISHI


# ------------------------------------------------------------------ the bhajan singer


_SG_O = dict(skin=SG_SKIN, hair=True, moustache=True, tilak=False, earring=False)


def sing_head(cr, mood="calm"):
    """The bhajan singer: a saffron head-cloth, a moustache, a sandal tilak; sing = eyes shut in devotion and mouth
    open, sing2 = mouth half open. mood: calm | sing | sing2."""
    import arjuna_cast as A
    A.face(cr, _SG_O, "smile" if mood != "calm" else "calm")
    if mood in ("sing", "sing2"):
        cr.new_path()
        ell(cr, 64, -66, 8, 11 if mood == "sing" else 6)
        leather(cr, (0.40, 0.06, 0.06), 2.5)
    tb = [(-56, -118), (-62, -168), (-44, -210), (0, -228), (42, -216), (60, -184), (54, -150), (24, -162),
          (-20, -150), (-42, -112)]
    _shape(cr, tb, SG_SHAWL, 5)
    for k in range(3):
        ink(cr, [(-54, -130 - 22 * k), (0, -164 - 16 * k), (52, -158 - 14 * k)], 3, col=(0.70, 0.30, 0.04))
    holes_line(cr, [(-48, -120), (0, -150), (50, -144)], 14, 2.4)
    for x in (46, 54):                                                            # sandal tilak, a red dot
        ink(cr, [(x, -146), (x + 2, -134)], 3.5, col=PALE)
    cr.new_path()
    cr.arc(51, -128, 4, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


_SG = dict(skin=SG_SKIN, bulk=0.98, dhoti=SG_CLOTH, border=SG_SHAWL, pleat=SG_CLOTH, sash=SG_SHAWL, neck=BROWN,
           robe=SG_SHAWL, beads=True)
SINGER = man("sb_sing", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
             hands=("open", "open"), **_SG)
for _m in ("calm", "sing", "sing2"):
    register("sb_sing_head" + ("" if _m == "calm" else "_" + _m), (-130, -250, 110, 30),
             (lambda m: lambda cr: sing_head(cr, m))(_m))

RAMA = K.RAMA
_RAMA_O = dict(skin=K.RAMA_SKIN, bulk=1.05, dhoti=GOLD, border=DRED, pleat=DRED, sash=RED, neck=GOLD, crown_col=GOLD,
               halo_col=GREEN, thread=True, seam_dx=-6)


def rama_head(cr, mood="smile"):
    """kaikeyi_cast's Rama head (puppet_cast.man_head) with a warm, happy eye and a smile; eat = his mouth a little
    open, a berry on its way in."""
    from puppet_cast import man_head
    man_head(cr, _RAMA_O)
    RU._cover(cr, K.RAMA_SKIN, 34, -118, 24, 16)
    ink(cr, [(16, -113), (34, -127), (52, -115)], 6)                              # a happy, curved eye
    ink(cr, [(20, -106), (34, -101), (48, -106)], 2.6)
    if mood == "eat":
        cr.new_path()
        ell(cr, 63, -67, 6, 8)
        leather(cr, (0.36, 0.05, 0.06), 2.5)
    else:
        ink(cr, [(61, -69), (55, -75)], 3)                                        # the corner of a smile


for _m in ("smile", "eat"):
    register("sb_rama_head_" + _m, (-190, -420, 110, 100), (lambda m: lambda cr: rama_head(cr, m))(_m))
