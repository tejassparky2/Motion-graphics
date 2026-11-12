"""The leather cast and props for the Mrityu reel (videos/mrityu.py): "Death herself wept", in the Togalu Gombeyaata
style of the earlier reels (puppet_cast, shani_cast, kumbhakarna_cast, shikhandi_cast...): profile figures with big
almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film.
Every sprite name starts with "mr_" (other builders' casts load in the same process).

Cast (one look each, kept the same through the video; gods and women with dignity):
  MRITYU (DEATH)  a dignified young woman, gentle and sad, never a skull or a monster: dusky skin (the text calls her
                  dark), a deep-red sari with a gold border and a dark-maroon pallu, a maroon blouse, long loose black
                  hair down her back with red flowers, a thin gold headband with a red tikka on her forehead, big
                  bright gold kundala earrings (the text: "bright earrings"), a nose ring, gold necklaces. Faces: open,
                  sad, cry (eyes squeezed shut, a sob), speak (pleading), bow (eyes lowered: she agrees), shut
                  (standing in penance), gentle (a kind, sad half-smile). Her glowing tears are light drawn by the
                  scenes from the rig point "eye". A second body (mr_death_body_leg) stands on ONE leg, the other foot
                  lifted behind under the sari (her penance).
  MOTHER EARTH    Bhudevi: warm brown skin, a leaf-green sari with a gold border and a deep-green pallu, a gold blouse,
                  shani_cast's tall tiered gold crown, her bun with flowers, gold jewellery. Faces: open, tired
                  (heavy lids, a sad brow, the mouth a little open), plead (brow raised, the mouth open).
  BRAHMA          six_cast_c.BRAHMA (three of his four faces showing, white beards, on his lotus), plus two pieces made
                  here: mr_brahma_head_angry (all three faces frowning) and mr_brahma_lo_cup (his forearm ending in a
                  cupped palm, to catch her tears).
  SHIVA           shikhandi_cast.SHIVA (blue-grey skin, matted hair with the moon, the trident), unchanged.
  THE CROWD       little dark silhouettes (the world's people and animals) that stand on the round world: a man, a
                  woman, a child, a man and a woman with their arms up, an old man with a stick, a cow, an elephant, a
                  deer, a goat, a dog; and a person lying down (asleep, for the shot where people die of illness: no
                  harm is drawn).
Props: mr_disease (a small dark smoky cloud with sickly specks: what her tears became), mr_hourglass (a wooden frame
and two pale glass bulbs; the sand is drawn by the scenes inside hourglass_bulb()). A soul is light drawn by the
scenes. The round world (kb_world), the lotus, the plaques, the speech cloud, the palm-leaf book, flames, sun and moon
come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.woman().
"""
import math

import arjuna_cast as A
import kumbhakarna_cast as KB  # noqa: F401  (registers the world disc, kb_world)
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import shani_cast as S
import shikhandi_cast as SK  # noqa: F401  (registers Shiva)
import six_cast_c as C6
from puppet_cast import HAIR, _flower, _jewel, _shape, fore_arm, woman, woman_body
from puppet_core import (GOLD, GREEN, PALE, RED, almond_eye, band, dots_in, ell, holes_line, ink, leather, poly,
                         punch, register, spath)

DT_SKIN = (0.80, 0.54, 0.37)          # Mrityu: dusky
DT_SARI = (0.86, 0.13, 0.10)          # deep red
DT_PALLU = (0.50, 0.05, 0.09)         # dark maroon
DT_CHOLI = (0.62, 0.08, 0.10)
DT_FLOWER = (0.95, 0.24, 0.20)
ER_SKIN = (0.90, 0.64, 0.42)          # Mother Earth
ER_SARI = (0.36, 0.66, 0.28)          # leaf green
ER_PALLU = (0.12, 0.42, 0.22)         # deep green
SIL = (0.20, 0.15, 0.16)              # the little silhouettes
SIL_LINE = (0.07, 0.04, 0.03)
SMOKE = (0.36, 0.30, 0.42)            # the disease cloud
SMOKE2 = (0.24, 0.20, 0.30)
SPECK = (0.58, 0.66, 0.36)
WOOD = (0.62, 0.36, 0.16)
WOOD2 = (0.82, 0.54, 0.24)
GLASS = (0.96, 0.97, 1.0)
TEAR = (0.82, 0.94, 1.0)              # her tears' light

EYE = (34.0, -100.0)                  # where her tears start (head units, just under the eye)
DT_MOODS = ("open", "sad", "cry", "speak", "bow", "shut", "gentle")
ER_MOODS = ("open", "tired", "plead")

# ------------------------------------------------------------------ Mrityu's face


def _death_eyes(cr, mood):
    """Her eye, brow and mouth (eye at 30, -112, as puppet_cast's woman head)."""
    sk = DT_SKIN
    if mood in ("open", "speak", "gentle"):
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        if mood == "gentle":                                                     # the lid a little lowered
            cr.new_path()
            cr.move_to(12, -113)
            cr.curve_to(22, -128, 40, -128, 48, -111)
            cr.curve_to(40, -117, 22, -117, 12, -113)
            cr.close_path()
            leather(cr, sk, 2.5)
            ink(cr, [(12, -113), (30, -118), (48, -111)], 4)
        if mood == "open":
            ink(cr, [(14, -128), (30, -134), (48, -132)], 3.5)
        else:                                                                    # a sad brow, raised at the front
            ink(cr, [(12, -126), (30, -133), (50, -145)], 3.5)
    elif mood == "sad":
        almond_eye(cr, 30, -110, 32, 11, col=PALE)
        cr.new_path()
        cr.move_to(12, -112)
        cr.curve_to(22, -128, 40, -128, 48, -110)
        cr.curve_to(40, -114, 22, -114, 12, -112)
        cr.close_path()
        leather(cr, sk, 2.5)
        ink(cr, [(12, -112), (30, -116), (48, -110)], 4)
        ink(cr, [(12, -126), (30, -132), (50, -146)], 3.5)
    elif mood == "cry":                                                          # squeezed shut, the brow up
        cr.new_path()
        ell(cr, 30, -112, 20, 13)
        cr.set_source_rgb(*sk)
        cr.fill()
        ink(cr, [(12, -114), (24, -106), (38, -105), (50, -112)], 5)
        for x, dx in ((20, -3), (30, -1), (40, 1)):
            ink(cr, [(x, -107), (x + dx, -99)], 2.4)
        ink(cr, [(50, -112), (58, -118)], 2.5)
        ink(cr, [(8, -122), (28, -132), (52, -152)], 4)
        ink(cr, [(52, -152), (48, -160)], 2.5)
    elif mood == "bow":                                                          # eyes lowered
        cr.new_path()
        ell(cr, 30, -112, 19, 13)
        cr.set_source_rgb(*sk)
        cr.fill()
        ink(cr, [(14, -112), (30, -104), (46, -110)], 4.5)
        for x in (20, 28, 36, 44):
            ink(cr, [(x, -106), (x + 2, -98)], 2.2)
        ink(cr, [(14, -130), (30, -136), (48, -136)], 3.5)
    elif mood == "shut":
        cr.new_path()
        ell(cr, 30, -112, 19, 13)
        cr.set_source_rgb(*sk)
        cr.fill()
        ink(cr, [(14, -112), (30, -104), (46, -112)], 4)
        for x in (22, 30, 38):
            ink(cr, [(x, -107), (x - 2, -100)], 2.2)
        ink(cr, [(14, -130), (30, -136), (46, -130)], 3.5)
    # the mouth
    if mood == "cry":
        cr.new_path()
        ell(cr, 59, -69, 6, 5)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
        ink(cr, [(50, -64), (59, -74), (66, -66)], 2.5, col=RED)
    elif mood == "speak":
        cr.new_path()
        ell(cr, 59, -71, 6, 7)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
    elif mood == "gentle":
        ink(cr, [(54, -74), (60, -69), (65, -72)], 3, col=RED)
    elif mood == "sad":
        ink(cr, [(52, -70), (59, -74), (65, -69)], 3, col=RED)
    else:
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)


def death_head(cr, mood="open"):
    """Mrityu: long loose black hair down her back with red flowers, a thin gold headband with a red tikka, big bright
    gold kundala earrings, a nose ring."""
    hp = [(-30, -176), (-62, -150), (-82, -96), (-90, -20), (-102, 60), (-96, 140), (-108, 220), (-90, 284),
          (-66, 250), (-70, 180), (-56, 110), (-48, 40), (-36, -30), (-26, -80)]
    _shape(cr, hp, HAIR, 5)                                                      # hair down her back
    for k in range(4):
        holes_line(cr, [(-44 - 8 * k, -140 + 8 * k), (-56 - 9 * k, -20), (-62 - 8 * k, 120), (-74 - 3 * k, 220)],
                   17, 2.3)
    for i, (x, y) in enumerate(((-58, -122), (-70, -60), (-76, 4))):
        _flower(cr, x, y, 12 if i == 0 else 9, DT_FLOWER, 6)
    S._face_w(cr, DT_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    band(cr, [(-36, -170), (0, -186), (34, -176)], 9, GOLD, spacing=9, hole_r=1.8)  # the headband
    ink(cr, [(30, -176), (42, -158)], 2.5, col=GOLD)                              # its tikka on her forehead
    cr.new_path()
    ell(cr, 44, -150, 6, 8)
    leather(cr, RED, 2.5)
    _death_eyes(cr, mood)
    cr.new_path()
    cr.arc(64, -90, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    for r, col in ((24, GOLD), (14, (1.0, 0.62, 0.22))):                          # the bright kundala earring
        cr.new_path()
        cr.arc(-12, -50, r, 0, 2 * math.pi)
        leather(cr, col, 3.5)
    punch(cr, [(-12 + 19 * math.cos(a * math.pi / 4), -50 + 19 * math.sin(a * math.pi / 4)) for a in range(8)], 2.4)
    _jewel(cr, -12, -50, 6, RED)
    _jewel(cr, -12, -80, 7, GOLD)


def _death_extra(cr):
    """Two gold necklaces with a red pendant, a jewelled belt."""
    band(cr, [(-20, -282), (12, -222), (40, -180)], 8, GOLD, spacing=10, hole_r=1.8)
    band(cr, [(-26, -276), (2, -190), (28, -132)], 7, GOLD, spacing=10, hole_r=1.6)
    _jewel(cr, 30, -122, 10, RED)
    for x in (-24, 4, 30):
        _jewel(cr, x, -24, 6, GOLD)


DEATH = woman("mr_death", skin=DT_SKIN, skirt=DT_SARI, choli=DT_CHOLI, border=GOLD, pallu_col=DT_PALLU, gem=RED,
              ornaments_extra=_death_extra, hands=("open", "open"))
DEATH.points["eye"] = ("mr_death_head", EYE)
for _m in DT_MOODS:
    register("mr_death_head" + ("" if _m == "open" else "_" + _m), (-150, -270, 100, 300),
             (lambda m: lambda cr: death_head(cr, m))(_m))


def death_body_leg(cr):
    """Her body standing on ONE leg (the front one, straight down), the back leg bent up behind her: the sari hangs
    round the standing leg and its hem lifts behind with the raised foot showing."""
    o = dict(skin=DT_SKIN, skirt=DT_SARI, choli=DT_CHOLI, border=GOLD, pallu_col=DT_PALLU, gem=RED,
             ornaments_extra=_death_extra)
    # the raised leg behind: the sari over the bent knee, the foot lifted up behind
    back = [(-40, 40), (10, 60), (30, 200), (20, 260), (-40, 300), (-150, 250), (-196, 214), (-190, 190),
            (-120, 200), (-50, 210)]
    _shape(cr, back, DT_PALLU, 5)
    dots_in(cr, lambda: spath(cr, back), 22, 2.8, shape="d")
    band(cr, [(-150, 238), (-90, 262), (-36, 282)], 22, GOLD, spacing=11, hole_r=2.2)
    foot = [(-196, 170), (-176, 156), (-150, 176), (-150, 214), (-184, 222), (-206, 204)]
    _shape(cr, foot, DT_SKIN, 4)                                                 # sole up
    band(cr, [(-150, 182), (-148, 214)], 8, GOLD, spacing=8, hole_r=1.8)
    # the standing leg's sari: narrow, down to the ankle
    skirt = [(-40, -30), (40, -34), (62, 120), (70, 300), (76, 430), (64, 446), (-44, 446), (-54, 430), (-56, 300),
             (-60, 120)]
    _shape(cr, skirt, DT_SARI, 6)
    dots_in(cr, lambda: spath(cr, skirt), 24, 3.2, shape="d")
    for x0, x1 in ((-10, -24), (10, 10), (30, 44)):
        ink(cr, [(x0, 0), (x1, 420)], 3, smooth=False)
    band(cr, [(-50, 420), (10, 424), (72, 420)], 26, GOLD, spacing=13)
    _shape(cr, [(-10, 438), (40, 440), (96, 456), (98, 472), (-12, 472)], DT_SKIN, 4)   # her one foot, flat
    band(cr, [(-8, 432), (36, 434)], 8, GOLD, spacing=8, hole_r=1.8)
    # the upper body: woman_body's torso, blouse, belt, pallu and jewels (its skirt is covered by the parts above)
    cr.save()
    cr.rectangle(-400, -400, 800, 400)
    cr.clip()
    woman_body(cr, o)
    cr.restore()


register("mr_death_body_leg", (-230, -310, 170, 490), death_body_leg)

# ------------------------------------------------------------------ Mother Earth


def _earth_eyes(cr, mood):
    sk = ER_SKIN
    if mood == "tired":
        almond_eye(cr, 30, -110, 32, 11, col=PALE)
        cr.new_path()
        cr.move_to(12, -111)
        cr.curve_to(22, -124, 40, -124, 48, -109)
        cr.curve_to(40, -108, 22, -108, 12, -111)
        cr.close_path()
        leather(cr, sk, 2.5)
        ink(cr, [(12, -111), (30, -110), (48, -109)], 4.5)
        ink(cr, [(12, -126), (30, -132), (50, -144)], 3.5)
        ink(cr, [(20, -96), (34, -92), (46, -96)], 2)                            # tired lines under the eye
        cr.new_path()
        ell(cr, 59, -70, 5, 4)
        leather(cr, (0.42, 0.06, 0.06), 2.2)
    elif mood == "plead":
        almond_eye(cr, 30, -114, 34, 13, col=PALE)
        ink(cr, [(46, -114), (60, -122)], 3)
        ink(cr, [(10, -130), (30, -138), (52, -152)], 3.5)
        cr.new_path()
        ell(cr, 59, -70, 6, 8)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
    else:
        S._w_eyes(cr, sk, "open")
        return


def earth_head(cr, mood="open"):
    """Mother Earth: her bun with green-and-gold flowers, the tall tiered gold crown, a bindi, a nose ring, gold
    jhumkas."""
    S._face_w(cr, ER_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-66, -126, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        _flower(cr, -66 + 26 * math.cos(a), -126 + 26 * math.sin(a), 7, GREEN if i % 2 else GOLD, 5)
    S.parvati_crown(cr)
    _earth_eyes(cr, mood)
    if mood == "open":
        S._w_eyes(cr, ER_SKIN, "open")
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


def _earth_extra(cr):
    band(cr, [(-22, -282), (12, -220), (40, -176)], 9, GOLD, spacing=10, hole_r=1.8)
    _jewel(cr, 40, -166, 11, GREEN)
    for x in (-26, -2, 22):
        _jewel(cr, x, -22, 7, GREEN)


EARTH = woman("mr_earth", skin=ER_SKIN, skirt=ER_SARI, choli=GOLD, border=GOLD, pallu_col=ER_PALLU, gem=GREEN,
              ornaments_extra=_earth_extra, hands=("open", "open"))
for _m in ER_MOODS:
    register("mr_earth_head" + ("" if _m == "open" else "_" + _m), (-150, -390, 120, 40),
             (lambda m: lambda cr: earth_head(cr, m))(_m))

# ------------------------------------------------------------------ Brahma: an angry head, cupped palms


def brahma_head_angry(cr):
    """six_cast_c.brahma_head with all three faces frowning (profiles: arjuna_cast's angry face)."""
    M._ray_halo(cr, 0, -170, 190, 270, 20, (GOLD, (1.0, 0.55, 0.10)))
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 70, 10)
        cr.scale(sx * 0.82, 0.82)
        A.face(cr, C6._BR_O, "angry")
        C6._white_beard(cr)
        R.kirita(cr, GOLD, None, tall=0.7, flare=RED)
        cr.restore()
    cx, cy = 0, -104
    for sx in (-1, 1):
        cr.new_path()
        ell(cr, cx + sx * 64, cy, 12, 20)
        leather(cr, C6.BR_SKIN, 4)
    cr.new_path()
    ell(cr, cx, cy, 62, 80)
    leather(cr, C6.BR_SKIN, 6)
    for sx in (-1, 1):
        cr.save()
        cr.translate(cx + sx * 26, cy - 14)
        cr.scale(sx, 1)
        almond_eye(cr, 0, 0, 34, 10, look=0, col=PALE)
        cr.restore()
        ink(cr, [(cx + sx * 6, cy - 30), (cx + sx * 28, cy - 38), (cx + sx * 50, cy - 50)], 7)   # brows pulled down
    ink(cr, [(cx - 4, cy - 34), (cx - 2, cy - 22)], 3)
    ink(cr, [(cx + 6, cy - 34), (cx + 4, cy - 22)], 3)
    ink(cr, [(cx + 2, cy - 14), (cx - 4, cy + 16), (cx + 6, cy + 20)], 3.5)
    ink(cr, [(cx, cy - 74), (cx, cy - 52)], 5, col=RED)
    bp = [(cx - 54, cy + 14), (cx - 60, cy + 70), (cx - 36, cy + 130), (cx, cy + 160), (cx + 36, cy + 130),
          (cx + 60, cy + 70), (cx + 54, cy + 14), (cx + 30, cy + 46), (cx, cy + 52), (cx - 30, cy + 46)]
    _shape(cr, bp, C6.AG_WHITE, 4)
    for k in (-2, -1, 0, 1, 2):
        ink(cr, [(cx + 14 * k, cy + 60), (cx + 18 * k, cy + 110), (cx + 12 * k, cy + 140 - 8 * abs(k))], 2.4,
            col=C6.AG_STRAND)
    ms = [(cx - 44, cy + 44), (cx - 20, cy + 26), (cx, cy + 32), (cx + 20, cy + 26), (cx + 44, cy + 44),
          (cx + 20, cy + 38), (cx, cy + 38), (cx - 20, cy + 38)]
    _shape(cr, ms, C6.AG_WHITE, 3)
    C6._crown_front(cr, cx, cy - 62, 78, 200)


register("mr_brahma_head_angry", (-300, -500, 300, 120), brahma_head_angry)


def brahma_lo_cup(cr):
    """Brahma's forearm ending in a cupped palm (it opens toward the arm's +x side: up, when the arm points
    forward)."""
    o = dict(C6._BRB)
    fore_arm(cr, o, None, "cup")
    hp = [(-16, 120), (-24, 150), (-22, 180), (-8, 202), (12, 210), (30, 204), (36, 192), (24, 190), (12, 180),
          (8, 156), (16, 140), (32, 134), (30, 122), (14, 118)]
    _shape(cr, hp, C6.BR_SKIN, 4)
    ink(cr, [(-14, 186), (2, 198)], 2.2)
    ink(cr, [(-10, 172), (4, 186)], 2.2)


register("mr_brahma_lo_cup", (-45, -30, 50, 220), brahma_lo_cup)
CUP = (14.0, 168.0)                   # the bowl of the cupped palm (forearm units)

# ------------------------------------------------------------------ the crowd: little dark silhouettes


def _sil(cr, pts, lw=3.0, smooth=True):
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=True)
    cr.set_source_rgb(*SIL)
    cr.fill_preserve()
    cr.set_source_rgb(*SIL_LINE)
    cr.set_line_width(lw)
    cr.set_line_join(1)
    cr.stroke()


def _sil_head(cr, x, y, r, knot=True, bun=False):
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*SIL)
    cr.fill_preserve()
    cr.set_source_rgb(*SIL_LINE)
    cr.set_line_width(2.5)
    cr.stroke()
    if knot:
        cr.new_path()
        cr.arc(x + 2, y - r - 4, r * 0.42, 0, 2 * math.pi)
        cr.set_source_rgb(*SIL)
        cr.fill()
    if bun:
        cr.new_path()
        cr.arc(x - r * 0.9, y - r * 0.2, r * 0.55, 0, 2 * math.pi)
        cr.set_source_rgb(*SIL)
        cr.fill()


def _person(cr, kind):
    """A little frontal person (feet at y = 0, ~100 units tall): man | woman | child | man_up | woman_up | old."""
    k = 0.72 if kind == "child" else 1.0
    cr.save()
    cr.scale(k, k)
    up = kind.endswith("_up")
    if kind.startswith("woman"):
        _sil(cr, [(-12, -76), (12, -76), (16, -46), (24, -2), (-24, -2), (-16, -46)])
        _sil_head(cr, 0, -88, 12, knot=False, bun=True)
    else:
        _sil(cr, [(-14, -76), (14, -76), (12, -44), (16, -22), (-16, -22), (-12, -44)])
        for sx in (-1, 1):
            _sil(cr, [(sx * 4, -26), (sx * 14, -26), (sx * 12, 0), (sx * 2, 0)], 2.5, smooth=False)
        _sil_head(cr, 0, -90, 12, knot=kind != "child")
    for sx in (-1, 1):
        if up:
            _sil(cr, [(sx * 10, -74), (sx * 18, -78), (sx * 30, -112), (sx * 22, -116)], 2.5, smooth=False)
        else:
            _sil(cr, [(sx * 12, -74), (sx * 19, -72), (sx * 21, -36), (sx * 14, -36)], 2.5, smooth=False)
    if kind == "old":
        ink(cr, [(26, -44), (30, 0)], 4, col=SIL_LINE)
    cr.restore()
    punch(cr, [(-4 * k, -90 * k), (4 * k, -90 * k)], 1.6)


def _cow(cr):
    _sil(cr, [(-46, -60), (-10, -66), (30, -62), (46, -54), (48, -30), (36, -24), (-40, -24), (-50, -38)])
    for x in (-38, -24, 26, 38):
        _sil(cr, [(x - 4, -30), (x + 4, -30), (x + 4, 0), (x - 4, 0)], 2.2, smooth=False)
    _sil(cr, [(42, -64), (62, -78), (76, -70), (78, -56), (62, -48), (48, -50)])
    ink(cr, [(60, -78), (56, -94)], 3.5, col=SIL)
    ink(cr, [(68, -78), (74, -92)], 3.5, col=SIL)
    ink(cr, [(-48, -54), (-60, -30)], 3, col=SIL)
    punch(cr, [(66, -66)], 1.8)


def _elephant(cr):
    _sil(cr, [(-60, -70), (-20, -92), (30, -90), (60, -70), (62, -36), (-62, -36)])
    for x in (-48, -28, 28, 46):
        _sil(cr, [(x - 8, -40), (x + 8, -40), (x + 8, 0), (x - 8, 0)], 2.2, smooth=False)
    _sil(cr, [(50, -86), (80, -84), (92, -60), (90, -20), (98, -6), (84, -4), (78, -44), (62, -50)])
    _sil(cr, [(48, -82), (66, -76), (64, -54), (46, -56)], 2.2)
    punch(cr, [(80, -72)], 2.0)


def _deer(cr):
    _sil(cr, [(-34, -50), (20, -54), (34, -46), (32, -30), (-34, -30)])
    for x in (-28, -18, 18, 28):
        _sil(cr, [(x - 3, -34), (x + 3, -34), (x + 2, 0), (x - 2, 0)], 2.0, smooth=False)
    _sil(cr, [(26, -52), (34, -76), (48, -78), (52, -70), (38, -66), (34, -48)])
    for d in (0, 6):
        ink(cr, [(36 + d, -76), (32 + d, -96), (24 + d, -104)], 2.6, col=SIL)
        ink(cr, [(33 + d, -90), (42 + d, -100)], 2.2, col=SIL)
    punch(cr, [(44, -72)], 1.6)


def _goat(cr):
    _sil(cr, [(-28, -40), (18, -44), (30, -36), (28, -22), (-28, -22)])
    for x in (-22, -12, 14, 22):
        _sil(cr, [(x - 3, -26), (x + 3, -26), (x + 2, 0), (x - 2, 0)], 2.0, smooth=False)
    _sil(cr, [(22, -42), (30, -60), (42, -58), (44, -48), (32, -40)])
    ink(cr, [(30, -60), (22, -72)], 3, col=SIL)
    ink(cr, [(40, -48), (40, -38)], 2.5, col=SIL)
    punch(cr, [(36, -54)], 1.5)


def _dog(cr):
    _sil(cr, [(-26, -34), (16, -36), (24, -28), (22, -18), (-26, -18)])
    for x in (-20, -12, 12, 20):
        _sil(cr, [(x - 3, -22), (x + 3, -22), (x + 2, 0), (x - 2, 0)], 2.0, smooth=False)
    _sil(cr, [(16, -34), (24, -50), (32, -50), (42, -42), (30, -34)])
    ink(cr, [(-26, -32), (-36, -46)], 3, col=SIL)
    punch(cr, [(30, -45)], 1.4)


def _lying(cr):
    """A person lying down asleep (feet to the left, head on the right; pivot at the middle of the ground line)."""
    _sil(cr, [(-48, -8), (-40, -20), (20, -22), (30, -16), (30, -2), (-48, -2)])
    _sil_head(cr, 42, -12, 11, knot=False)


CROWD = ("man", "woman", "child", "old", "man_up", "woman_up")
for _k in CROWD:
    register("mr_p_" + _k, (-40, -125, 40, 6), (lambda k: lambda cr: _person(cr, k))(_k), tex=0.4)
register("mr_a_cow", (-66, -100, 84, 6), _cow, tex=0.4)
register("mr_a_elephant", (-70, -100, 104, 6), _elephant, tex=0.4)
register("mr_a_deer", (-42, -110, 58, 6), _deer, tex=0.4)
register("mr_a_goat", (-34, -78, 50, 6), _goat, tex=0.4)
register("mr_a_dog", (-44, -56, 48, 6), _dog, tex=0.4)
register("mr_p_lying", (-56, -30, 58, 6), _lying, tex=0.4)
WIDTH = {"mr_p_man": 34, "mr_p_woman": 50, "mr_p_child": 26, "mr_p_old": 40, "mr_p_man_up": 64,
         "mr_p_woman_up": 64, "mr_a_cow": 130, "mr_a_elephant": 170, "mr_a_deer": 90, "mr_a_goat": 70,
         "mr_a_dog": 70}

# ------------------------------------------------------------------ props


def _disease(cr):
    """A small dark smoky cloud with sickly green-grey specks (what her tears became)."""
    lobes = [(-56, 4, 40), (-20, -26, 46), (26, -22, 44), (60, 4, 38), (14, 20, 44), (-28, 22, 40)]
    for x, y, r in lobes:
        cr.new_sub_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*SIL_LINE)
    cr.set_line_width(10)
    cr.stroke_preserve()
    cr.set_source_rgb(*SMOKE)
    cr.fill()
    for x, y, r in ((-14, -8, 24), (30, 2, 18)):
        ink(cr, [(x - r, y), (x - r * 0.4, y - r * 0.8), (x + r * 0.5, y - r * 0.4), (x + r * 0.2, y + r * 0.3),
                 (x - r * 0.3, y + r * 0.1)], 4, col=SMOKE2)
    for x, y in ((-44, 6), (-6, -36), (40, -10), (8, 26), (58, 14)):
        cr.new_path()
        cr.arc(x, y, 7, 0, 2 * math.pi)
        leather(cr, SPECK, 2.5)
        for k in range(6):
            a = k * math.pi / 3
            ink(cr, [(x + 7 * math.cos(a), y + 7 * math.sin(a)), (x + 12 * math.cos(a), y + 12 * math.sin(a))], 2,
                col=SIL_LINE)
    punch(cr, [(-60, -10), (22, -40), (64, -14), (-30, 34)], 3)


register("mr_disease", (-110, -84, 110, 76), _disease)

HG_H = 190.0                          # the hourglass: the bulbs reach from -HG_H to +HG_H (pivot at the neck)


def hourglass_bulb(cr, upper=True, inset=0.0):
    """The path of one glass bulb (hourglass units, the neck at 0, 0)."""
    s = -1 if upper else 1
    w = 104 - inset
    cr.new_path()
    cr.move_to(-8 + inset * 0.2, 0)
    cr.curve_to(-30, s * 30, -w, s * 60, -w, s * 120)
    cr.line_to(-w, s * (HG_H - 14 + inset * 0.3))
    cr.line_to(w, s * (HG_H - 14 + inset * 0.3))
    cr.line_to(w, s * 120)
    cr.curve_to(w, s * 60, 30, s * 30, 8 - inset * 0.2, 0)
    cr.close_path()


def _hourglass(cr):
    for upper in (True, False):
        hourglass_bulb(cr, upper)
        leather(cr, GLASS, 5)
    for y in (-HG_H - 22, HG_H - 4):                                              # the wooden plates
        _shape(cr, [(-140, y), (140, y), (148, y + 26), (-148, y + 26)], WOOD, 5, smooth=False)
        band(cr, [(-132, y + 13), (132, y + 13)], 8, WOOD2, spacing=12, hole_r=2.2)
    for x in (-126, 126):                                                         # the turned posts
        pts = [(x - 9, -HG_H + 4), (x + 9, -HG_H + 4), (x + 12, -100), (x + 7, 0), (x + 12, 100),
               (x + 9, HG_H - 4), (x - 9, HG_H - 4), (x - 12, 100), (x - 7, 0), (x - 12, -100)]
        _shape(cr, pts, WOOD2, 4)
    ink(cr, [(-70, -150), (-80, -80)], 3, col=(0.80, 0.86, 0.96))
    ink(cr, [(-70, 80), (-80, 150)], 3, col=(0.80, 0.86, 0.96))


register("mr_hourglass", (-160, -230, 160, 230), _hourglass)
