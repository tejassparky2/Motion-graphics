"""The leather cast and props for the Ranchhod reel (videos/ranchhod.py), in the Togalu Gombeyaata style of the earlier
reels (puppet_cast, jayadratha_cast, hanuman_cast, kumbhakarna_cast): profile figures with big almond eyes,
perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every sprite
name starts with "rc_".

Cast (one look each, kept the same through the video; Krishna and Muchukunda with dignity):
  KRISHNA      puppet_cast.KRISHNA, as in the Jarasandha and Jayadratha reels (blue skin, a peacock feather in his hair
               knot, a gold dhoti with a red border, a green sash), with extra pieces for this story: two bent running
               legs (rc_kr_leg_fwd: the knee lifted forward; rc_kr_leg_back: pushing off behind) so he clearly RUNS,
               his head turned back over his shoulder (rc_kr_head_back, and smiling: rc_kr_head_back_smile), a calm
               smile (rc_kr_head_smile) and eyes shut with a smile (rc_kr_head_sleep: "pretending to sleep", only in
               Kalayavana's thought bubble).
  KALAYAVANA   a huge, cruel king (rc_kala, bulk 1.38, drawn bigger than everyone): dark iron armour (a breastplate
               with gold rivets and a sun boss, pauldrons, bracers and greaves), a dark-crimson cape, a maroon dhoti,
               a spiked iron crown-helmet with a red plume and a mail neck guard, a hooked nose, a black pointed beard
               and a thick curled moustache, a fierce red-rimmed eye under a heavy brow. Faces: fierce, laugh, shout,
               sly, shock. His big dark sword (rc_sword) and bent running legs (rc_kala_leg_fwd / _back).
  MUCHUKUNDA   the old king asleep in the cave (rc_mk): long white hair and a long white beard, bushy white brows, a
               short gold kirita, a violet dhoti with a gold border, a saffron sash, rudraksha beads. Faces: calm,
               sleep (eyes shut, peaceful), wake (eyes wide, a pale-gold fire in them, brows down: the scenes add the
               glow), fight (fierce, for the flashback).
  THE GODS     shani_cast.DEVA (silhouettes with halos). The demons of the flashback: rc_asura (one dark horned
               silhouette with a club). The army: rc_army (one leather piece, a marching row of soldiers in
               silhouette with helmets, shields and spears, as crowds are cut in the old puppet sets).
Sets and props: Mathura's gate (rc_gate: two tall towers with domes and saffron flags, a crenellated wall, a big arch;
rc_door: one wooden door leaf on its hinge), the cave on the hillside (rc_cave: the rock with the mouth cut out;
rc_cave_back: the darkness inside the mouth), the cave inside (rc_cave_in: rock walls, a ceiling of stalactites and a
rocky floor framing the screen), the stone bed with its stone pillow (rc_bed), a cobweb (rc_web), the heap of ash
(rc_ash), a big eye open and shut (rc_eye, rc_eye_shut: the rule card) and two crossed swords (rc_battle: the word
card). Hills, rocks, the thought bubble, speech cloud, plaques, palm leaves and the ground come from the earlier
casts; dust and drifting ash are drawn by the scenes.

Every sprite is drawn once in design units and cached by puppet_core; the rigs come from puppet_cast.man().
"""
import math
import random

import arjuna_cast  # noqa: F401  (the thought bubble ar_think)
import hanuman_cast  # noqa: F401  (the hill hn_hill)
import jayadratha_cast  # noqa: F401  (the soldiers, the palm-leaf book via lrekha_cast)
import kaikeyi_cast  # noqa: F401  (the palm leaf kk_leaf)
import lrekha_cast  # noqa: F401  (the speech cloud lr_scloud)
import puppet_cast as C
import ravana_cast as R
import shani_cast  # noqa: F401  (the devas)
import six_cast_c  # noqa: F401  (the rock c6_rock)
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BLUE, GOLD, GREEN, INK, PALE, RED, SAFFRON, almond_eye, band, cut, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, rivet, spath)

KR_O = dict(skin=BLUE, dhoti=GOLD, border=RED, pleat=RED, sash=GREEN, crown="feather", thread=True, hair=True,
            halo=False)                                    # puppet_cast.KRISHNA's options

KL_SKIN = (0.88, 0.62, 0.42)          # Kalayavana
KL_STEEL = (0.27, 0.27, 0.33)
KL_STEEL2 = (0.46, 0.46, 0.54)
KL_DHOTI = (0.44, 0.08, 0.12)
KL_CAPE = (0.56, 0.07, 0.08)
KL_B = 1.38
MK_SKIN = (0.93, 0.70, 0.48)          # Muchukunda
MK_DHOTI = (0.50, 0.26, 0.60)
WHITE = (0.97, 0.96, 0.92)
WHITE2 = (0.70, 0.68, 0.66)
STONE = (0.62, 0.55, 0.50)
STONE2 = (0.46, 0.40, 0.36)
ROCK = (0.56, 0.47, 0.40)
ROCK2 = (0.38, 0.31, 0.27)
CAVE_D = (0.10, 0.07, 0.07)
WOOD = (0.64, 0.40, 0.18)
WOOD2 = (0.46, 0.27, 0.11)
SIL = (0.12, 0.08, 0.07)
ASH = (0.84, 0.82, 0.80)
ASH2 = (0.50, 0.48, 0.49)

BED_H = 230.0                         # the stone bed: its top above the ground (bed units)
BED_W = 900.0
PILLOW = (-360.0, -BED_H - 40.0)      # the stone pillow's top centre (bed units)
GATE_ARCH = (300.0, 470.0)            # Mathura's gate: the arch's width and height (gate units)
CAVE_MOUTH = (-120.0, 400.0, 330.0)   # the cave on the hill: the mouth's centre x, height and width (cave units)
HIP_RUN = 352.0                       # a running figure: the hip above the ground at the bottom of a stride (units)


# ------------------------------------------------------------------ running legs (for Krishna and Kalayavana)


def _quad(p0, p1, w0, w1):
    """A tapered strip from p0 (width w0) to p1 (width w1) as a closed polygon."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return [(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
            (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)]


def run_leg(cr, o, mode="fwd"):
    """A leg bent at the knee (hip pivot at 0, 0; facing +x): mode 'fwd' = the knee lifted forward, the shin hanging
    under it; 'back' = pushing off behind, the foot up behind. The dhoti covers the thigh (as puppet_cast.leg), the
    shin and foot are skin (or a greave when o has 'greave')."""
    b = o.get("bulk", 1.0)
    if mode == "fwd":
        knee, ankle, foot_rot = (176, 132), (150, 322), -0.10
    else:
        knee, ankle, foot_rot = (-92, 196), (-250, 286), 0.95
    shin = _quad(knee, ankle, 44 * b, 30 * b)
    _shape(cr, shin, o["skin"], 5, smooth=False)
    if o.get("greave"):
        g = _quad((knee[0] + (ankle[0] - knee[0]) * 0.18, knee[1] + (ankle[1] - knee[1]) * 0.18),
                  (knee[0] + (ankle[0] - knee[0]) * 0.86, knee[1] + (ankle[1] - knee[1]) * 0.86), 50 * b, 36 * b)
        _shape(cr, g, o["greave"], 4.5, smooth=False, holes=(7, 12, 2.2))
    cr.save()                                                   # the foot (the standard puppet foot, turned)
    cr.translate(*ankle)
    cr.rotate(foot_rot)
    _shape(cr, [(-14, -2), (14, -4), (32, 12), (70, 26), (72, 40), (-16, 42)], o["skin"], 4)
    band(cr, [(-12 * b, -8), (14 * b, -8)], 9, GOLD, spacing=8, hole_r=2.0)
    cr.restore()
    th = _quad((0, -6), knee, 96 * b, 70 * b)                  # the thigh in the dhoti
    th = [th[3], th[0], (th[0][0] * 0.5 + th[1][0] * 0.5, th[0][1] * 0.5 + th[1][1] * 0.5), th[1],
          (knee[0] + (knee[0]) * 0.02 + 10, knee[1] + 26), th[2]]
    _shape(cr, th, o["dhoti"], 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    kx, ky = knee
    L = math.hypot(kx, ky)
    ux, uy = kx / L, ky / L
    p = (kx - ux * 22, ky - uy * 22)
    band(cr, [(p[0] - uy * 36 * b, p[1] + ux * 36 * b), (p[0] + uy * 36 * b, p[1] - ux * 36 * b)], 14,
         o.get("border", GOLD), spacing=11, hole_r=2.4)
    ink(cr, [(ux * 30 - uy * 8, uy * 30 + ux * 8), (kx * 0.7 - uy * 6, ky * 0.7 + ux * 6)], 3)
    rivet(cr, 0, 0, 9)


RUN_BOX = (-330, -70, 280, 400)


# ------------------------------------------------------------------ Krishna's extra pieces


def kr_head(cr, mood="calm", back=False):
    """Krishna's head (puppet_cast.man_head with his options); back = turned to look back over his shoulder (the
    profile mirrored on the neck); mood: calm | smile | sleep (eyes shut, a little smile: pretending)."""
    if back:
        cr.scale(-1, 1)
    C.man_head(cr, KR_O)
    if mood in ("smile", "sleep"):
        ink(cr, [(71, -72), (63, -66), (54, -70)], 3.6)                       # the smile
        ink(cr, [(50, -80), (47, -74)], 2.4)
    if mood == "sleep":
        cr.new_path()
        ell(cr, 34, -117, 24, 16)
        cr.set_source_rgb(*BLUE)
        cr.fill()
        ink(cr, [(14, -118), (34, -110), (54, -118)], 4.5)
        for x in (24, 34, 44):
            ink(cr, [(x, -112), (x - 2, -104)], 2.5)


register("rc_kr_head_smile", (-190, -420, 110, 100), lambda cr: kr_head(cr, "smile"))
register("rc_kr_head_sleep", (-190, -420, 110, 100), lambda cr: kr_head(cr, "sleep"))
register("rc_kr_head_back", (-110, -420, 190, 100), lambda cr: kr_head(cr, "calm", True))
register("rc_kr_head_back_smile", (-110, -420, 190, 100), lambda cr: kr_head(cr, "smile", True))
register("rc_kr_leg_fwd", RUN_BOX, lambda cr: run_leg(cr, KR_O, "fwd"))
register("rc_kr_leg_back", RUN_BOX, lambda cr: run_leg(cr, KR_O, "back"))
KRISHNA = C.KRISHNA                   # the shared rig (never changed here: other reels use it)


# ------------------------------------------------------------------ Kalayavana


KL_O = dict(skin=KL_SKIN, bulk=KL_B, dhoti=KL_DHOTI, border=GOLD, pleat=KL_STEEL, sash=KL_CAPE, neck=KL_STEEL2,
            crown="tiara", halo=False, hair=False, tilak=False, earring=False, hands=("fist", "fist"),
            greave=KL_STEEL)


def kala_head(cr, mood="fierce"):
    """Kalayavana in profile facing +x (neck at 0, 0). mood: fierce | laugh | shout | sly | shock."""
    guard = [(-40, -150), (-74, -132), (-86, -70), (-80, 4), (-40, 20), (-30, -40), (-26, -100)]   # mail neck guard
    _shape(cr, guard, KL_STEEL, 5)
    dots_in(cr, lambda: spath(cr, guard), 13, 2.6)
    openm = mood in ("laugh", "shout", "shock")
    face = [(-26, 8), (-34, -40), (-52, -84), (-58, -132), (-44, -176), (0, -196), (42, -186), (58, -156),
            (62, -132), (72, -118), (100, -94), (96, -84), (74, -82), (76, -74), (64, -66), (70, -56), (62, -42),
            (56, -26), (38, -16), (28, 8)]
    if openm:                                                  # the jaw drops open
        drop = 10 if mood == "shock" else 26
        face = face[:13] + [(52, -72), (84, -46 + drop * 0.4), (74, -24 + drop * 0.5), (46, -10 + drop * 0.3),
                            (30, 8)]
    _shape(cr, face, KL_SKIN, 6)
    if openm:                                                  # the open mouth, teeth along the top
        mo = [(76, -80), (52, -72), (84, -46 + drop * 0.4)]
        _shape(cr, mo, (0.36, 0.05, 0.05), 3.5, smooth=False)
        if mood != "shock":
            _shape(cr, [(74, -79), (56, -73), (60, -68), (74, -72)], PALE, 2, smooth=False)
            _shape(cr, [(80, -52), (70, -58), (72, -52), (82, -48)], PALE, 2, smooth=False)
    cr.new_path()                                              # the ear
    ell(cr, -16, -108, 13, 21)
    leather(cr, KL_SKIN, 4)
    _jewel(cr, -14, -76, 10, GOLD)
    beard = [(64, -48), (62, -22), (56, 10), (60, 44), (36, 30), (14, 6), (2, -34), (14, -52), (40, -56)]
    if openm:
        d2 = drop * 0.5
        beard = [(84, -40 + d2), (74, -14 + d2), (62, 20 + d2), (64, 56 + d2), (36, 38 + d2), (14, 8), (2, -32),
                 (16, -50), (44, -46)]
    _shape(cr, beard, HAIR, 4)
    for k in range(3):
        ink(cr, [(30 + 9 * k, -40), (30 + 8 * k, 0), (36 + 6 * k, 30)], 2.2, col=(0.42, 0.30, 0.24))
    must = [(74, -78), (52, -86), (28, -88), (8, -98), (-6, -116), (2, -96), (22, -82), (50, -76)]
    _shape(cr, must, HAIR, 3)
    ink(cr, [(-6, -116), (-14, -104), (-6, -96)], 4, col=HAIR)
    ex, ey = 34, -120
    if mood == "laugh":                                        # eyes squeezed shut with laughing
        ink(cr, [(ex - 18, ey + 4), (ex, ey - 8), (ex + 18, ey + 4)], 5.5)
        band(cr, [(ex - 26, ey - 26), (ex, ey - 34), (ex + 26, ey - 26)], 13, HAIR, holes=False)
    elif mood == "sly":                                        # a narrowed, scheming eye
        cr.new_path()
        ell(cr, ex, ey, 20, 8)
        leather(cr, PALE, 3.5)
        cr.arc(ex + 6, ey + 1, 6, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        band(cr, [(ex - 26, ey - 14), (ex, ey - 12), (ex + 26, ey - 18)], 13, HAIR, holes=False)
        ink(cr, [(72, -68), (64, -64), (58, -70)], 3)
    else:
        big = mood in ("shout", "shock")
        r_ = 15 if big else 12
        cr.new_path()                                          # a red rim round a fierce eye
        ell(cr, ex, ey, 26 if big else 23, r_ + 5)
        leather(cr, (0.86, 0.22, 0.14), 0)
        cr.new_path()
        cr.move_to(ex - 20, ey)
        cr.curve_to(ex - 10, ey - r_ * 1.2, ex + 10, ey - r_ * 1.2, ex + 22, ey)
        cr.curve_to(ex + 10, ey + r_ * 0.9, ex - 10, ey + r_ * 0.9, ex - 20, ey)
        cr.close_path()
        leather(cr, PALE, 4)
        cr.arc(ex + 6, ey, 7 if mood == "shock" else 9, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(ex + 9, ey - 3)], 2.6)
        if mood == "shock":
            band(cr, [(ex - 24, ey - 30), (ex, ey - 40), (ex + 26, ey - 32)], 13, HAIR, holes=False)
        else:                                                  # the heavy brow, slanting down to the nose
            band(cr, [(ex - 26, ey - 34), (ex, ey - 26), (ex + 28, ey - 14)], 15, HAIR, holes=False)
    ink(cr, [(84, -98), (90, -90)], 3)                         # the nostril
    # the spiked iron crown-helmet with a red plume
    plume = [(0, -282), (-40, -312), (-110, -300), (-170, -246), (-196, -170), (-150, -220), (-96, -262),
             (-46, -272)]
    _shape(cr, plume, RED, 4)
    holes_line(cr, [(-20, -290), (-90, -286), (-150, -236)], 14, 2.4)
    dome = [(-60, -142), (-62, -180), (-44, -216), (0, -236), (44, -222), (62, -192), (66, -142)]
    _shape(cr, dome, KL_STEEL, 6, holes=(11, 13, 2.4))
    ink(cr, [(0, -232), (4, -180), (2, -150)], 3, col=KL_STEEL2)
    poly(cr, [(-10, -230), (0, -300), (10, -230)])
    leather(cr, GOLD, 3.5)
    band(cr, [(-64, -146), (2, -152), (68, -146)], 22, GOLD, spacing=11, hole_r=2.4)
    for x in (-40, 0, 40):                                     # crown points on the band
        _shape(cr, [(x - 14, -156), (x, -186), (x + 14, -156)], GOLD, 3, smooth=False)
    _jewel(cr, 2, -150, 10, RED)


KL_MOODS = ("fierce", "laugh", "shout", "sly", "shock")


def kala_body(cr):
    """His body: a dark-crimson cape behind, then puppet_cast.man_body, then an iron breastplate over the torso."""
    b = KL_B
    cape = [(-20, -296), (-80, -284), (-140, -170), (-190, 20), (-224, 220), (-176, 262), (-130, 210), (-80, 60),
            (-40, -120)]
    _shape(cr, cape, KL_CAPE, 5, holes=(12, 15, 2.8))
    ink(cr, [(-70, -250), (-130, -40), (-170, 200)], 3, col=(0.30, 0.03, 0.04))
    C.man_body(cr, KL_O)
    plate = [(-46 * b, -44), (-56 * b, -150), (-50 * b, -238), (-22, -276), (30, -276), (58 * b, -244), (80 * b, -204),
             (76 * b, -152), (60 * b, -96), (52 * b, -44)]
    _shape(cr, plate, KL_STEEL, 6, holes=(12, 16, 2.6))
    for y in (-110, -80):                                      # the belly lames
        ink(cr, [(-50 * b, y), (10, y + 6), (58 * b, y)], 3.5, col=KL_STEEL2)
    for x, y in ((-40 * b, -230), (40 * b, -236), (-44 * b, -60), (48 * b, -60)):
        _jewel(cr, x, y, 7, GOLD)
    _flower(cr, 30 * b, -176, 30, GOLD, 8)                     # a gold sun boss on the chest
    _jewel(cr, 30 * b, -176, 9, RED)
    band(cr, [(-50 * b, -40), (54 * b, -40)], 14, GOLD, spacing=11, hole_r=2.2)


def kala_upper(cr):
    C.upper_arm(cr, KL_O)
    b = KL_B
    pd = [(-36 * b, 10), (-30 * b, -26), (0, -40 * b), (32 * b, -24), (36 * b, 14), (26 * b, 56), (-26 * b, 56)]
    _shape(cr, pd, KL_STEEL, 5, holes=(8, 12, 2.2))
    band(cr, [(-30 * b, 50), (30 * b, 52)], 10, GOLD, holes=False)
    rivet(cr, 0, 0, 7)


def kala_fore(cr):
    C.fore_arm(cr, KL_O, None, "fist")
    b = KL_B
    br = [(-20 * b, 30), (20 * b, 30), (18 * b, 112), (-18 * b, 112)]
    _shape(cr, br, KL_STEEL, 4, smooth=False, holes=(6, 11, 2.0))
    band(cr, [(-20 * b, 36), (20 * b, 36)], 8, GOLD, holes=False)
    rivet(cr, 0, 0, 6)


def kala_leg(cr):
    C.leg(cr, KL_O)
    b = KL_B
    g = [(-26 * b, 240), (20 * b, 240), (17 * b, 360), (-12 * b, 366), (-26 * b, 300)]
    _shape(cr, g, KL_STEEL, 4.5, holes=(7, 12, 2.2))


KALA = man("rc_kala", **KL_O)
register("rc_kala_body", (-260, -340, 160, 300), kala_body)
for _m in KL_MOODS:
    register("rc_kala_head" + ("" if _m == "fierce" else "_" + _m), (-220, -330, 120, 70),
             (lambda m: lambda cr: kala_head(cr, m))(_m))
register("rc_kala_armF_up", (-60, -70, 60, 175), kala_upper)
register("rc_kala_armB_up", (-60, -70, 60, 175), kala_upper)
register("rc_kala_armF_lo", (-45, -30, 45, 210), kala_fore)
register("rc_kala_armB_lo", (-45, -30, 45, 210), kala_fore)
register("rc_kala_legF", (-70, -40, 90, 440), kala_leg)
register("rc_kala_legB", (-70, -40, 90, 440), kala_leg)
register("rc_kala_leg_fwd", RUN_BOX, lambda cr: run_leg(cr, KL_O, "fwd"))
register("rc_kala_leg_back", RUN_BOX, lambda cr: run_leg(cr, KL_O, "back"))
KALA.points["eye"] = ("rc_kala_head", (34, -120))
KALA.points["mouth"] = ("rc_kala_head", (74, -64))


def _sword(cr):
    """Kalayavana's big sword (grip at 0, 0, the blade up): a broad curved dark-steel blade with a pale edge, a gold
    cross-guard, a red grip and a gold pommel."""
    blade = [(-28, -40), (-36, -220), (-26, -400), (-4, -540), (30, -640), (58, -680), (54, -610), (46, -530),
             (44, -400), (38, -220), (30, -40)]
    _shape(cr, blade, KL_STEEL2, 5)
    ink(cr, [(-6, -60), (-8, -260), (2, -470), (24, -600)], 4, col=(0.86, 0.86, 0.92))
    holes_line(cr, [(10, -80), (12, -300), (18, -480)], 26, 2.6)
    band(cr, [(-64, -36), (64, -36)], 18, GOLD, spacing=12, hole_r=2.2)
    for s_ in (-1, 1):
        _jewel(cr, s_ * 66, -36, 9, RED)
    band(cr, [(0, -24), (0, 64)], 26, RED, spacing=10, hole_r=2.0)
    cr.new_path()
    cr.arc(0, 82, 18, 0, 2 * math.pi)
    leather(cr, GOLD, 4)


register("rc_sword", (-90, -700, 90, 110), _sword)


# ------------------------------------------------------------------ Muchukunda


MK_O = dict(skin=MK_SKIN, bulk=1.1, dhoti=MK_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD, crown="tiara",
            halo=False, hair=False, beads=True, thread=True, hands=("open", "fist"))


def mk_head(cr, mood="calm"):
    """The old king in profile facing +x (neck at 0, 0): long white hair, a long white beard, bushy white brows, a
    short gold kirita. mood: calm | sleep | wake (eyes wide, a pale fire in them) | fight."""
    hp = [(-30, -176), (-64, -146), (-90, -80), (-96, 10), (-84, 90), (-56, 116), (-44, 40), (-38, -40), (-20, -90)]
    _shape(cr, hp, WHITE, 5)
    for k in range(4):
        holes_line(cr, [(-46 - 8 * k, -140 + 10 * k), (-74 - 4 * k, -40), (-66 - 2 * k, 60)], 16, 2.4)
        ink(cr, [(-50 - 8 * k, -120), (-76 - 4 * k, -20), (-70 - 2 * k, 70)], 2, col=WHITE2)
    face = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
            (60, -128), (66, -116), (92, -92), (68, -82), (70, -72), (62, -64), (66, -56), (56, -44), (52, -30),
            (34, -22), (26, 6)]
    _shape(cr, face, MK_SKIN, 6)
    cr.new_path()
    ell(cr, -14, -108, 13, 21)
    leather(cr, MK_SKIN, 4)
    _jewel(cr, -12, -74, 12, GOLD)
    beard = [(64, -58), (68, -30), (64, 30), (52, 110), (36, 176), (14, 140), (0, 60), (-6, -10), (8, -50),
             (30, -60)]
    _shape(cr, beard, WHITE, 4)
    for k in range(4):
        ink(cr, [(52 - 10 * k, -40), (46 - 11 * k, 40), (40 - 10 * k, 120)], 2.2, col=WHITE2)
    must = [(70, -76), (48, -84), (26, -86), (10, -98), (20, -90), (44, -80), (68, -70)]
    _shape(cr, must, WHITE, 3)
    ink(cr, [(10, -160), (30, -164)], 2.2, col=(0.66, 0.42, 0.26))                 # wrinkles
    ink(cr, [(6, -148), (28, -150)], 2.2, col=(0.66, 0.42, 0.26))
    ex, ey = 34, -118
    if mood == "sleep":
        cr.new_path()
        ell(cr, ex, ey + 1, 24, 16)
        cr.set_source_rgb(*MK_SKIN)
        cr.fill()
        ink(cr, [(ex - 20, ey), (ex, ey + 8), (ex + 20, ey)], 4.5)
        for x in (ex - 10, ex, ex + 10):
            ink(cr, [(x, ey + 6), (x - 2, ey + 14)], 2.5)
        brow = [(ex - 26, ey - 22), (ex, ey - 30), (ex + 28, ey - 22), (ex + 4, ey - 20)]
    elif mood == "wake":
        cr.new_path()
        cr.move_to(ex - 22, ey)
        cr.curve_to(ex - 10, ey - 20, ex + 12, ey - 20, ex + 24, ey)
        cr.curve_to(ex + 12, ey + 16, ex - 10, ey + 16, ex - 22, ey)
        cr.close_path()
        leather(cr, (1.0, 0.92, 0.56), 4.5)
        punch(cr, [(ex + 2, ey)], 8.0)                          # the light comes straight through
        brow = [(ex - 28, ey - 30), (ex, ey - 24), (ex + 30, ey - 10), (ex + 4, ey - 14)]
    else:
        almond_eye(cr, ex, ey, 38, 13, col=PALE)
        brow = ([(ex - 28, ey - 32), (ex, ey - 26), (ex + 30, ey - 14), (ex + 4, ey - 16)] if mood == "fight" else
                [(ex - 26, ey - 26), (ex, ey - 34), (ex + 28, ey - 24), (ex + 4, ey - 22)])
    _shape(cr, brow, WHITE, 3)
    if mood == "wake":
        ink(cr, [(70, -66), (60, -68)], 3)
    R.kirita(cr, GOLD, None, tall=0.72, flare=SAFFRON)


MK_MOODS = ("calm", "sleep", "wake", "fight")
MUCHU = man("rc_mk", **MK_O)
for _m in MK_MOODS:
    register("rc_mk_head" + ("" if _m == "calm" else "_" + _m), (-200, -400, 120, 190),
             (lambda m: lambda cr: mk_head(cr, m))(_m))
MUCHU.points["eye"] = ("rc_mk_head", (34, -118))


def _bed(cr):
    """The stone bed (pivot on the ground under its middle; its top at -BED_H): a rough slab on two stone blocks, a
    stone pillow at the head (left) end, cracks and a perforated edge."""
    for x in (-300, 300):
        blk = [(x - 110, 0), (x - 100, -BED_H + 50), (x + 100, -BED_H + 54), (x + 112, 0)]
        _shape(cr, blk, STONE2, 5, smooth=False, holes=(10, 16, 2.6))
        ink(cr, [(x - 60, -40), (x - 20, -110), (x + 30, -150)], 3, col=(0.30, 0.26, 0.24))
    slab = [(-BED_W / 2, -BED_H + 60), (-BED_W / 2 + 8, -BED_H), (-200, -BED_H - 6), (150, -BED_H - 2),
            (BED_W / 2 - 6, -BED_H - 6), (BED_W / 2, -BED_H + 58), (0, -BED_H + 66)]
    _shape(cr, slab, STONE, 6, smooth=False, holes=(12, 17, 2.8))
    for pts in (((-300, -BED_H + 20), (-220, -BED_H + 36), (-120, -BED_H + 24)), ((80, -BED_H + 30),
                                                                                 (200, -BED_H + 18))):
        ink(cr, list(pts), 3, col=STONE2)
    px, py = PILLOW
    pil = [(px - 110, -BED_H + 6), (px - 104, py + 16), (px - 60, py), (px + 70, py + 4), (px + 104, py + 20),
           (px + 110, -BED_H + 6)]
    _shape(cr, pil, STONE, 5, holes=(9, 14, 2.4))
    ink(cr, [(px - 60, py + 20), (px + 40, py + 22)], 2.5, col=STONE2)


register("rc_bed", (-BED_W / 2 - 20, -BED_H - 90, BED_W / 2 + 20, 12), _bed)


# ------------------------------------------------------------------ the army, the demons


def _soldier_sil(cr, x, k):
    """One marching soldier in silhouette (feet at x, 0, facing +x): helmet with a spike, a round shield in front,
    a spear slanting forward; k varies the stride."""
    st = (k % 3 - 1) * 26
    for sx, sp in ((-1, 0.30), (1, 0.26)):                      # legs: one striding forward, one back
        cr.save()
        cr.translate(x + sx * 10, -250)
        cr.rotate(-sx * (sp + 0.05 * (k % 2)))
        poly(cr, [(-17, 0), (17, 0), (13, 236), (-13, 236)])
        cr.restore()
        cr.fill()
        fx = x + sx * 10 + 240 * math.sin(sx * (sp + 0.05 * (k % 2)))
        poly(cr, [(fx - 14, -24), (fx + 34, -12), (fx + 36, 0), (fx - 16, 0)])
        cr.fill()
    poly(cr, [(x - 40, -360), (x + 44, -360), (x + 64, -236), (x - 60, -236)])   # the kilt
    cr.fill()
    spath(cr, [(x - 40, -350), (x - 58, -430), (x - 50, -486), (x + 4, -506), (x + 54, -484), (x + 50, -420),
               (x + 40, -350)])                                 # the torso
    cr.fill()
    poly(cr, [(x - 12, -500), (x + 14, -500), (x + 14, -530), (x - 12, -530)])
    cr.fill()
    ell(cr, x + 6, -560, 40, 44)                                # head
    cr.fill()
    poly(cr, [(x + 36, -566), (x + 58, -552), (x + 38, -544)])  # nose
    cr.fill()
    spath(cr, [(x - 44, -566), (x - 38, -612), (x + 6, -636), (x + 48, -614), (x + 54, -566)])   # helmet
    cr.fill()
    poly(cr, [(x - 2, -626), (x + 8, -690), (x + 16, -626)])
    cr.fill()
    cr.set_line_width(26)                                       # the spear arm
    cr.set_line_cap(1)
    cr.move_to(x + 20, -470)
    cr.line_to(x + 76, -400)
    cr.line_to(x + 100, -470)
    cr.stroke()
    cr.set_line_width(12)                                       # the spear, slanting forward
    cr.move_to(x + 40 + st * 0.2, -120)
    cr.line_to(x + 190 + st * 0.3, -820)
    cr.stroke()
    poly(cr, [(x + 180 + st * 0.3, -810), (x + 214 + st * 0.3, -900), (x + 208 + st * 0.3, -798)])
    cr.fill()
    ell(cr, x + 66, -370, 64, 72)                               # shield
    cr.fill()


def _army(cr):
    """A marching row of seven soldiers in silhouette, one leather piece (pivot at the bottom centre); shield bosses,
    eyes and spear blades punched so the light comes through."""
    cr.set_source_rgb(*SIL)
    xs = [-560 + 186 * i for i in range(7)]
    for k, x in enumerate(xs):
        cr.new_path()
        _soldier_sil(cr, x, k)
    cr.set_source_rgb(*SIL)
    band(cr, [(-660, -40), (660, -40)], 20, (0.30, 0.20, 0.16), holes=False)
    for k, x in enumerate(xs):
        punch(cr, [(x + 66, -370)], 9)
        punch(cr, [(x + 66 + 42 * math.cos(a), -370 + 48 * math.sin(a)) for a in (0, 1.6, 3.1, 4.7)], 4)
        punch(cr, [(x + 26, -566)], 5)
        holes_line(cr, [(x - 36, -580), (x + 46, -580)], 11, 2.4, smooth=False)
        holes_line(cr, [(x - 30, -320), (x + 40, -320)], 13, 2.4, smooth=False)
        st = (k % 3 - 1) * 26
        punch(cr, [(x + 200 + st * 0.3, -850)], 4)


register("rc_army", (-700, -900, 720, 20), _army, tex=0.6)


def _asura(cr):
    """A demon of the gods' war in silhouette (feet at 0, 0, facing +x): horns, wild hair, a raised club."""
    cr.set_source_rgb(*SIL)
    cr.new_path()
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 30, -320)
        cr.rotate(-sx * 0.3)
        poly(cr, [(-28, 0), (28, 0), (22, 320), (-22, 320)])
        cr.restore()
        cr.fill()
    poly(cr, [(-80, -420), (84, -420), (110, -300), (-104, -300)])          # a loincloth
    cr.fill()
    spath(cr, [(-74, -400), (-110, -520), (-86, -640), (10, -666), (100, -630), (110, -520), (74, -400)])
    cr.fill()
    ell(cr, 10, -720, 66, 74)
    cr.fill()
    for sx in (-1, 1):                                          # horns
        spath(cr, [(sx * 30 + 10, -770), (sx * 80 + 10, -830), (sx * 96 + 10, -900), (sx * 60 + 10, -820),
                   (sx * 10 + 10, -790)])
        cr.fill()
    rng = random.Random(3)
    pts = []
    for i in range(14):                                         # wild hair
        a = math.pi * (0.55 + 0.9 * i / 13)
        r = 96 if i % 2 == 0 else 70 + rng.uniform(-6, 6)
        pts.append((10 + r * math.cos(a) * 1.1, -720 + r * math.sin(a)))
    poly(cr, pts + [(10, -700)])
    cr.fill()
    cr.set_line_width(26)                                       # the arm and the club raised
    cr.move_to(40, -600)
    cr.line_to(140, -760)
    cr.stroke()
    spath(cr, [(120, -740), (150, -900), (200, -1010), (250, -990), (214, -880), (160, -730)])
    cr.fill()
    punch(cr, [(46, -730)], 9)                                  # the eye
    holes_line(cr, [(-60, -360), (70, -360)], 14, 3, smooth=False)
    for y in (-950, -880, -810):
        punch(cr, [(196 + (y + 950) * -0.3, y)], 5)


register("rc_asura", (-140, -1030, 280, 12), _asura, tex=0.6)


# ------------------------------------------------------------------ Mathura's gate


def _gate(cr):
    """Mathura's gate (pivot on the ground under the arch's middle): two tall towers with domes, kalasha tops and
    saffron flags, a crenellated wall over a big arch (cut out: the doors hang in it)."""
    aw, ah = GATE_ARCH
    wall = [(-300, 0), (-300, -720), (300, -720), (300, 0)]
    _shape(cr, wall, (0.86, 0.66, 0.36), 6, smooth=False, holes=(12, 16, 2.8))
    for i in range(6):                                          # crenellations
        x = -280 + i * 100
        _shape(cr, [(x, -720), (x, -790), (x + 60, -790), (x + 60, -720)], (0.86, 0.66, 0.36), 5, smooth=False)
    for y in (-200, -400, -600):
        ink(cr, [(-300, y), (300, y)], 2.5, smooth=False, col=(0.60, 0.42, 0.20))
    for tx in (-400, 400):
        tw = [(tx - 120, 0), (tx - 120, -940), (tx + 120, -940), (tx + 120, 0)]
        _shape(cr, tw, (0.92, 0.70, 0.36), 6, smooth=False, holes=(12, 16, 2.8))
        for y in (-260, -560):
            _shape(cr, [(tx - 30, y), (tx - 30, y - 90), (tx, y - 130), (tx + 30, y - 90), (tx + 30, y)],
                   (0.24, 0.14, 0.08), 4, smooth=False)
        dome = [(tx - 130, -940), (tx - 120, -1010), (tx - 70, -1080), (tx, -1110), (tx + 70, -1080),
                (tx + 120, -1010), (tx + 130, -940)]
        _shape(cr, dome, GOLD, 6, holes=(12, 15, 2.6))
        band(cr, [(tx - 130, -944), (tx + 130, -944)], 18, RED, spacing=12, hole_r=2.4)
        cr.new_path()
        cr.arc(tx, -1130, 20, 0, 2 * math.pi)
        leather(cr, GOLD, 4)
        ink(cr, [(tx, -1150), (tx, -1290)], 6, smooth=False)
        _shape(cr, [(tx, -1290), (tx + 120, -1262), (tx + 70, -1240), (tx + 116, -1214), (tx, -1206)], SAFFRON, 4,
               smooth=False, holes=(7, 11, 2.2))
    arch = [(-aw / 2 - 40, 0), (-aw / 2 - 40, -ah + 60), (-aw / 2 + 10, -ah - 20), (0, -ah - 60),
            (aw / 2 - 10, -ah - 20), (aw / 2 + 40, -ah + 60), (aw / 2 + 40, 0)]
    _shape(cr, arch, GOLD, 6, smooth=False, holes=(12, 15, 2.6))
    _flower(cr, 0, -ah - 110, 40, RED, 8)
    _jewel(cr, 0, -ah - 110, 12, GOLD)
    cut(cr, lambda: poly(cr, [(-aw / 2, 2), (-aw / 2, -ah + 60), (-aw / 2 + 40, -ah), (0, -ah - 30),
                              (aw / 2 - 40, -ah), (aw / 2, -ah + 60), (aw / 2, 2)]))


def _door(cr):
    """One wooden door leaf (pivot at the hinge on the ground; the leaf runs to +x): planks, gold studs, a ring."""
    aw, ah = GATE_ARCH
    w = aw / 2
    leaf = [(0, 0), (0, -ah + 60), (w * 0.45, -ah - 10), (w, -ah - 30), (w, 0)]
    _shape(cr, leaf, WOOD, 5, smooth=False)
    for k in range(1, 4):
        ink(cr, [(w * k / 4, -6), (w * k / 4, -ah + 30)], 2.5, smooth=False, col=WOOD2)
    for y in (-80, -220, -360):
        band(cr, [(4, y), (w - 4, y)], 14, (0.36, 0.30, 0.26), holes=False)
        for k in range(4):
            _jewel(cr, 16 + k * (w - 32) / 3, y, 6, GOLD)
    cr.new_path()
    cr.arc(w - 30, -240, 18, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()


register("rc_gate", (-540, -1320, 540, 12), _gate)
register("rc_door", (-8, -GATE_ARCH[1] - 40, GATE_ARCH[0] / 2 + 8, 8), _door)


# ------------------------------------------------------------------ the cave


def _cave(cr):
    """The rocky hill with the cave (pivot on the ground under the hill's middle); the mouth is cut out, so the
    darkness drawn behind it (rc_cave_back) shows, and a figure drawn between the two goes into the dark."""
    mx, mh, mw = CAVE_MOUTH
    rng = random.Random(11)
    body = [(-640, 0), (-600, -160), (-520, -330), (-420, -470), (-300, -590), (-160, -680), (-20, -720),
            (120, -700), (260, -620), (380, -500), (480, -360), (560, -200), (620, 0)]
    body = [(x + rng.uniform(-10, 10), y + rng.uniform(-8, 8)) if y < 0 else (x, y) for x, y in body]
    _shape(cr, body, ROCK, 7, smooth=False)
    for pts in (((-160, -680), (-200, -500), (-320, -330)), ((120, -700), (160, -520), (300, -360), (380, -200)),
                ((-420, -470), (-460, -260), (-560, -120)), ((-20, -720), (40, -560))):
        ink(cr, list(pts), 4, smooth=False, col=ROCK2)
    face = [(120, -700), (260, -620), (380, -500), (230, -420), (150, -560)]
    _shape(cr, face, (0.66, 0.57, 0.48), 4, smooth=False)
    dots_in(cr, lambda: poly(cr, body), 34, 3.4, shape="d")
    for x, w in ((-480, 150), (330, 190), (520, 120)):
        g = [(x - w / 2, 4), (x - w / 3, -40), (x, -62), (x + w / 3, -44), (x + w / 2, 4)]
        _shape(cr, g, (0.40, 0.58, 0.26), 4)
    rim = [(mx - mw / 2 - 50, 0), (mx - mw / 2 - 40, -mh * 0.7), (mx - mw * 0.3, -mh - 40), (mx, -mh - 70),
           (mx + mw * 0.3, -mh - 40), (mx + mw / 2 + 40, -mh * 0.7), (mx + mw / 2 + 50, 0)]
    _shape(cr, rim, (0.48, 0.40, 0.34), 6, smooth=True, holes=(12, 16, 2.8))
    for k in range(5):                                          # vines over the mouth
        x = mx - mw / 2 + 20 + k * (mw - 40) / 4
        ln = 70 + 50 * ((k * 7) % 3)
        band(cr, [(x, -mh - 30 + 10 * abs(k - 2)), (x + 6, -mh - 30 + ln * 0.5), (x - 4, -mh - 30 + ln)], 8,
             (0.32, 0.54, 0.22), spacing=10, hole_r=1.8)
    cut(cr, lambda: spath(cr, [(mx - mw / 2, 4), (mx - mw / 2 + 6, -mh * 0.6), (mx - mw * 0.32, -mh + 20),
                               (mx, -mh), (mx + mw * 0.32, -mh + 20), (mx + mw / 2 - 6, -mh * 0.6), (mx + mw / 2, 4)],
                         closed=True))


def _cave_back(cr):
    """The darkness inside the cave mouth (same pivot as rc_cave)."""
    mx, mh, mw = CAVE_MOUTH
    pts = [(mx - mw / 2 - 20, 6), (mx - mw / 2 - 14, -mh * 0.6), (mx - mw * 0.34, -mh + 6), (mx, -mh - 20),
           (mx + mw * 0.34, -mh + 6), (mx + mw / 2 + 14, -mh * 0.6), (mx + mw / 2 + 20, 6)]
    _shape(cr, pts, CAVE_D, 0)
    for k in range(4):
        ink(cr, [(mx - mw * 0.3 + k * mw * 0.2, -mh + 30), (mx - mw * 0.3 + k * mw * 0.2 + 8, -mh + 90)], 3,
            col=(0.20, 0.15, 0.14))


register("rc_cave", (-660, -760, 640, 12), _cave)
register("rc_cave_back", (CAVE_MOUTH[0] - CAVE_MOUTH[2], -CAVE_MOUTH[1] - 40, CAVE_MOUTH[0] + CAVE_MOUTH[2], 12),
         _cave_back, tex=0.4)


CAVE_FLOOR = 740.0                    # inside the cave: the floor's top below the pivot (1 unit = 1 px at scale 1)
CAVE_TOP = -880.0                     # and the ceiling (the headline sits under it, on the open cloth)


def _cave_in(cr):
    """Inside the cave (pivot at the screen's centre; 1 unit = 1 px at scale 1): rough rock walls down both sides, a
    vaulted ceiling hung with stalactites, a rocky floor (its top at CAVE_FLOOR); the middle is open (the lamp-lit
    cloth shows through)."""
    rng = random.Random(23)
    F = CAVE_FLOOR
    top, wx = CAVE_TOP, 470                                     # the open middle: straight rough walls, a low vault
    hole = [(-560, F + 40), (-wx + rng.uniform(-8, 8), 400), (-wx - 6, -100), (-wx + 8, -500)]
    for i in range(13):
        a = math.pi + 0.5 * math.pi * i / 12                     # the left corner rounds into the ceiling
        hole.append((-wx + 110 + 110 * math.cos(a), top + 110 + 110 * math.sin(a)))
    for i in range(1, 12):
        hole.append((-wx + 110 + (2 * wx - 220) * i / 12, top + rng.uniform(-14, 14)))
    for i in range(13):
        a = 1.5 * math.pi + 0.5 * math.pi * i / 12
        hole.append((wx - 110 + 110 * math.cos(a), top + 110 + 110 * math.sin(a)))
    hole += [(wx - 8, -500), (wx + 6, -100), (wx + rng.uniform(-8, 8), 400), (520, F + 40)]
    outer = [(-760, -1160), (760, -1160), (760, 1160), (-760, 1160)]
    cr.new_path()
    poly(cr, outer)
    spath(cr, hole)
    cr.set_fill_rule(1)
    cr.set_source_rgb(*ROCK2)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(7)
    cr.stroke()
    dots_in(cr, lambda: (poly(cr, outer), spath(cr, hole)), 40, 3.2, shape="d")    # even-odd: in the rock only
    cr.set_fill_rule(0)
    for k in range(9):                                          # strata in the rock
        y = -1000 + 250 * k
        for sx in (-1, 1):
            ink(cr, [(sx * 540, y), (sx * 620, y + 40 + 20 * (k % 2)), (sx * 720, y + 10)], 4, col=(0.24, 0.19, 0.16))
    stal = [(-wx + 4, -480, 150), (-wx + 6, -300, 90), (wx - 4, -470, 160), (wx - 6, -280, 80)]   # on the walls
    stal += [(-wx + 150 + k * (2 * wx - 300) / 8, top - 4, 50 + 40 * ((k * 5) % 3) / 2) for k in range(9)]
    for k, (x, y, ln) in enumerate(stal):                       # stalactites: short ones along the ceiling (clear
        w = 22 + 8 * (k % 3)                                    # of the headline), long ones down the walls
        _shape(cr, [(x - w, y - 20), (x + w, y - 20), (x + w * 0.4, y + ln * 0.6), (x, y + ln),
                    (x - w * 0.4, y + ln * 0.6)], ROCK2, 5, smooth=False)
        ink(cr, [(x - w * 0.3, y), (x - 2, y + ln * 0.7)], 2.5, col=(0.24, 0.19, 0.16))
    floor = [(-780, F + 30), (-500, F + 6), (-200, F - 4), (100, F + 4), (420, F - 6), (780, F + 24), (780, 1170),
             (-780, 1170)]
    _shape(cr, floor, (0.46, 0.38, 0.33), 6, smooth=False, holes=(12, 18, 2.8))
    for x, y, r in ((-380, F + 120, 70), (330, F + 150, 90), (-120, F + 260, 60), (560, F + 300, 70)):
        cr.new_path()
        ell(cr, x, y, r, r * 0.45)
        leather(cr, (0.38, 0.31, 0.27), 4)
    for x, h in ((-520, 120), (-430, 70), (500, 100)):          # stalagmites at the walls
        _shape(cr, [(x - 40, F + 10), (x - 10, F - h), (x + 6, F - h - 10), (x + 40, F + 10)], ROCK2, 5,
               smooth=False)


register("rc_cave_in", (-770, -1170, 770, 1170), _cave_in, tex=0.7)


def _web(cr):
    """A cobweb in a corner (pivot at the corner; it spreads to +x, +y): radial threads and a sagging spiral."""
    cr.set_line_cap(1)
    n = 7
    for i in range(n):
        a = (math.pi / 2) * i / (n - 1)
        ink(cr, [(0, 0), (300 * math.cos(a), 300 * math.sin(a))], 2.4, smooth=False)
    for r in (60, 110, 160, 210, 260):
        pts = []
        for i in range(n):
            a = (math.pi / 2) * i / (n - 1)
            pts.append((r * math.cos(a), r * math.sin(a)))
            if i < n - 1:
                am = (math.pi / 2) * (i + 0.5) / (n - 1)
                pts.append(((r - 12) * math.cos(am), (r - 12) * math.sin(am)))
        ink(cr, pts, 2.0)


register("rc_web", (-10, -10, 310, 310), _web, tex=0.2)


# ------------------------------------------------------------------ small props


def _ash(cr):
    """A heap of grey ash (pivot at the bottom centre) with dark flecks."""
    rng = random.Random(9)
    heap = [(-190, 0), (-150, -40), (-80, -76), (0, -96), (90, -74), (160, -36), (200, 0)]
    _shape(cr, heap, ASH, 5)
    for _ in range(26):
        x, y = rng.uniform(-150, 150), rng.uniform(-70, -8)
        if abs(x) < 170 + y:
            cr.new_path()
            cr.arc(x, y, rng.uniform(3, 6), 0, 2 * math.pi)
            cr.set_source_rgb(*ASH2)
            cr.fill()
    holes_line(cr, [(-120, -30), (0, -60), (130, -26)], 18, 2.6)


register("rc_ash", (-210, -110, 220, 12), _ash, tex=0.5)


def _eye(cr, shut=False):
    """A big eye seen from the front (centre pivot): almond, lashes; shut = the lid closed in a curve."""
    if shut:
        cr.new_path()
        cr.move_to(-160, -10)
        cr.curve_to(-80, 60, 80, 60, 160, -10)
        cr.set_source_rgb(*INK)
        cr.set_line_width(14)
        cr.set_line_cap(1)
        cr.stroke()
        for k in range(5):
            x = -100 + 50 * k
            ink(cr, [(x, 28 + 4 * (2 - abs(k - 2))), (x * 1.15, 70)], 7)
        return
    cr.new_path()
    cr.move_to(-170, 0)
    cr.curve_to(-90, -110, 90, -110, 170, 0)
    cr.curve_to(90, 100, -90, 100, -170, 0)
    cr.close_path()
    leather(cr, PALE, 9)
    cr.new_path()
    cr.arc(0, 0, 66, 0, 2 * math.pi)
    leather(cr, (0.86, 0.56, 0.18), 5)
    cr.new_path()
    cr.arc(0, 0, 32, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(16, -16)], 11)
    for k in range(5):
        x = -100 + 50 * k
        ink(cr, [(x, -78 - 4 * (2 - abs(k - 2))), (x * 1.15, -120)], 7)


register("rc_eye", (-185, -135, 185, 105), _eye)
register("rc_eye_shut", (-185, -40, 185, 90), lambda cr: _eye(cr, True))


def _battle(cr):
    """Two crossed swords over a round shield (centre pivot): the word card's picture of a battle."""
    cr.new_path()
    cr.arc(0, 30, 120, 0, 2 * math.pi)
    leather(cr, (0.86, 0.56, 0.22), 6)
    cr.new_path()
    cr.arc(0, 30, 92, 0, 2 * math.pi)
    leather(cr, (0.60, 0.30, 0.14), 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        _jewel(cr, 70 * math.cos(a), 30 + 70 * math.sin(a), 7, GOLD)
    for s_ in (-1, 1):
        cr.save()
        cr.translate(0, 40)
        cr.rotate(s_ * 0.72)
        cr.scale(0.42, 0.42)
        _sword(cr)
        cr.restore()


register("rc_battle", (-160, -290, 160, 170), _battle)
