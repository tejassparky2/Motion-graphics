"""The leather cast and props for the Hanuman reel (videos/hanuman_curse.py), in the Togalu Gombeyaata style of the
earlier reels (puppet_cast, ravana_cast, mandhata_cast, ruru_cast, shani_cast): profile figures with big almond eyes,
perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every sprite name
starts with "hn_".

Cast (one look each, kept the same through the video; gods, sages and Hanuman with dignity):
  BABY HANUMAN  a playful vanara child (hn_baby, its own small rig): golden-orange fur, a big round head with a tuft,
                a pale muzzle, a big bright eye, a curling tail, a red langot with a gold band, a gold necklace and
                anklets. Faces: calm, happy, wonder (looking up, mouth round), cheeky (a grin), daze (eyes shut after
                the fall; no injury is ever drawn, only a little star on the chin).
  HANUMAN       grown and mighty (hn_hanu, puppet_cast.man): sindoor-orange fur as ravana_cast's Hanuman, a tall gold
                kirita, a red dhoti with a gold border, a saffron sash, his tail; his gold gada (hn_gada). The halo is
                light drawn by the scenes (it comes back when he remembers). Faces: calm, puzzled, sad, joy, smile.
  VAYU          the wind god (hn_vayu): sky-blue skin, long hair streaming back in the wind, a gold kirita with a blue
                flare, a pale-blue dhoti, a deep-blue sash. Faces: calm, angry, hurt.
  JAMBAVAN      the old bear-king (hn_jamb): white fur, a long pale muzzle with a dark nose, bushy white brows, a
                white beard of fur, a small gold crown, a maroon dhoti, rudraksha; his staff. Faces: calm, speak, smile.
  AIRAVATA      Indra's white elephant (hn_airavata) with four tusks, a red and gold caparison and a gold headpiece;
                Indra himself is mandhata_cast's INDRA, seen only in the thunderbolt's flash.
Sets and props: the rising sun (hn_sun: a red-orange disc with a shine, like a ripe fruit; hn_sun_rays turning behind
it; hn_stem: a stem and leaf that turn it into a fruit), the mountain (hn_hill), the hermitage's sruva ladle
(hn_ladle) and heap of bark cloth (hn_bark), the seashore (hn_sand, hn_palm), the gada. The sages, devas, vanaras,
Indra, Lanka, the waves, pots, fire, hut, thought bubble and plaques come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; the grown figures' rigs come from
puppet_cast.man(), the baby's is built here.
"""
import math

import arjuna_cast as A
import ravana_cast as R
from puppet_cast import _jewel, _shape, man
from puppet_core import (BROWN, DGREEN, GOLD, INK, OCHRE, PALE, RED, SAFFRON, Rig, almond_eye, band,
                         dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet, spath)

FUR = (1.0, 0.62, 0.24)               # baby Hanuman: golden orange
FUR2 = (0.84, 0.36, 0.10)
BELLY = (1.0, 0.86, 0.62)
MUZ = (1.0, 0.90, 0.72)
HANU_FUR = R.HANU_FUR                 # grown Hanuman: sindoor orange (as ravana_cast)
HANU_FUR2 = R.HANU_FUR2
VY_SKIN = (0.60, 0.80, 1.0)           # Vayu
VY_DHOTI = (0.86, 0.94, 1.0)
VY_BLUE = (0.20, 0.46, 0.92)
VY_SASH = (0.12, 0.32, 0.78)
VY_HAIR = (0.20, 0.26, 0.46)
JB_FUR = (0.88, 0.87, 0.85)           # Jambavan: white fur (a little grey on the body so it reads on the cloth)
JB_HEAD = (0.95, 0.94, 0.91)
JB_FUR2 = (0.58, 0.56, 0.56)
JB_MUZ = (1.0, 0.93, 0.80)
JB_DHOTI = (0.58, 0.16, 0.14)
EL_W = (0.97, 0.96, 0.93)             # Airavata
EL_W2 = (0.80, 0.80, 0.84)
SUN_R = (0.93, 0.22, 0.08)
SUN_O = (1.0, 0.50, 0.12)
STONE = (0.66, 0.54, 0.42)
STONE2 = (0.52, 0.40, 0.30)
SAND = (0.98, 0.84, 0.56)
WOOD = (0.70, 0.44, 0.20)
BARK = (0.66, 0.42, 0.22)
BARK2 = (0.84, 0.60, 0.32)
ROSE_IN = (1.0, 0.66, 0.58)

SUN_RAD = 210.0                       # the sun disc's radius (sun units)


# ------------------------------------------------------------------ baby Hanuman (his own rig)


def _ruff(cr, cx, cy, r0, r1, a0, a1, n, col):
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        r = r0 if i % 2 == 0 else r1
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    _shape(cr, pts + [(cx + 10, cy)], col, 4, smooth=False)


def baby_head(cr, mood="calm"):
    """Baby Hanuman's head in profile facing +x (neck at 0, 0): a fluffy ruff, a big round cranium with a tuft, a pale
    muzzle, a big eye. mood: calm | happy | wonder | cheeky | daze."""
    _ruff(cr, -14, -132, 128, 102, 80, 280, 18, FUR2)
    for k, (x, a) in enumerate(((-6, -0.5), (16, -0.15), (36, 0.25))):        # the tuft on top
        cr.save()
        cr.translate(x, -236)
        cr.rotate(a)
        _shape(cr, [(-12, 6), (-6, -30), (0, -52), (8, -28), (12, 6)], FUR2, 3.5)
        cr.restore()
    cran = [(-26, 4), (-56, -40), (-74, -100), (-70, -170), (-36, -224), (14, -244), (62, -228), (94, -190),
            (104, -152), (100, -122), (70, -104), (60, -60), (46, -24), (24, 4)]
    _shape(cr, cran, FUR, 6)
    face = [(28, -214), (70, -206), (98, -176), (104, -146), (96, -118), (60, -108), (30, -130), (20, -176)]
    _shape(cr, face, MUZ, 3.5)                                                   # the pale face mask
    mz = [(62, -124), (98, -120), (124, -104), (136, -80), (128, -56), (104, -42), (72, -40), (52, -58), (52, -96)]
    _shape(cr, mz, MUZ, 4.5)
    cr.new_path()                                                                 # the ear
    ell(cr, -30, -122, 24, 32)
    leather(cr, FUR, 4)
    cr.new_path()
    ell(cr, -28, -122, 12, 18)
    leather(cr, ROSE_IN, 2.5)
    _jewel(cr, -34, -84, 11, GOLD)
    punch(cr, [(128, -94)], 4.0)                                                   # nostril
    for k in range(3):                                                            # cheek fur
        ink(cr, [(-2 + 9 * k, -70 + 4 * k), (8 + 9 * k, -52 + 4 * k)], 2.4, col=FUR2)
    cr.new_path()                                                                 # a sindoor dot
    cr.arc(40, -206, 7, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    # eye, brow, mouth
    ex, ey = 62, -158
    if mood == "daze":
        ink(cr, [(ex - 22, ey + 2), (ex, ey + 12), (ex + 22, ey + 2)], 5)
        for x in (ex - 12, ex, ex + 12):
            ink(cr, [(x, ey + 10), (x - 2, ey + 18)], 2.4)
        ink(cr, [(ex - 24, ey - 24), (ex, ey - 30), (ex + 24, ey - 22)], 4)
    elif mood == "cheeky":
        almond_eye(cr, ex, ey, 44, 15, look=1, col=PALE, lw=4)
        ink(cr, [(ex - 26, ey - 30), (ex, ey - 22), (ex + 26, ey - 32)], 5.5)
    else:
        big = mood in ("wonder", "happy")
        h_ = 21 if big else 18
        cr.new_path()
        cr.move_to(ex - 24, ey)
        cr.curve_to(ex - 12, ey - h_ * 1.1, ex + 12, ey - h_ * 1.1, ex + 24, ey + 1)
        cr.curve_to(ex + 12, ey + h_ * 0.9, ex - 12, ey + h_ * 0.9, ex - 24, ey)
        cr.close_path()
        leather(cr, PALE, 4)
        px, py = (ex + 6, ey - 7) if mood == "wonder" else (ex + 6, ey)
        cr.new_path()
        cr.arc(px, py, 10.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(px + 3.5, py - 3.5)], 3.2)
        bdy = -6 if mood == "wonder" else 0
        ink(cr, [(ex - 26, ey - 28 + bdy), (ex, ey - 36 + bdy), (ex + 26, ey - 28 + bdy)], 5)
    if mood == "wonder":
        cr.new_path()
        ell(cr, 112, -58, 10, 12)
        leather(cr, (0.40, 0.06, 0.06), 3)
    elif mood in ("happy", "cheeky"):
        _shape(cr, [(126, -66), (112, -56), (92, -56), (78, -66), (96, -50), (114, -50)], (0.42, 0.06, 0.06), 3)
        if mood == "cheeky":
            _shape(cr, [(122, -64), (96, -60), (100, -55), (118, -58)], PALE, 2, smooth=False)
        ink(cr, [(76, -70), (70, -76)], 2.5)
    elif mood == "daze":
        ink(cr, [(122, -62), (106, -56), (92, -60)], 3.5)
    else:
        ink(cr, [(124, -64), (106, -58), (86, -62)], 3.5)


def _baby_body(cr):
    """The torso (hip at 0, 0): a round belly with a pale patch, a red langot with a gold band, a gold necklace."""
    torso = [(-44, 6), (-56, -60), (-58, -128), (-46, -178), (-18, -204), (20, -206), (46, -190), (60, -150),
             (72, -100), (68, -48), (52, -4)]
    _shape(cr, torso, FUR, 6)
    patch = [(16, -176), (50, -156), (66, -104), (60, -46), (32, -30), (18, -90)]
    _shape(cr, patch, BELLY, 3.5)
    punch(cr, [(50, -70)], 4.0)
    ink(cr, [(30, -156), (52, -136)], 3)
    holes_line(cr, [(-40, -150), (-46, -90), (-38, -40)], 13, 2.2)
    lang = [(-50, -34), (56, -30), (60, 8), (42, 34), (10, 46), (-22, 40), (-50, 22)]
    _shape(cr, lang, RED, 5)
    dots_in(cr, lambda: spath(cr, lang), 18, 2.6, shape="d")
    band(cr, [(-52, -28), (58, -24)], 14, GOLD, spacing=11, hole_r=2.4)
    band(cr, [(-18, -200), (14, -186), (46, -170)], 11, GOLD, spacing=11, hole_r=2.2)
    _jewel(cr, 40, -160, 10, RED)


def _baby_arm(cr, col=FUR):
    pts = [(-22, -8), (0, -24), (22, -8), (20, 70), (16, 132), (-14, 132), (-20, 70)]
    _shape(cr, pts, col, 5)
    hp = [(-14, 126), (14, 126), (24, 150), (20, 176), (10, 190), (2, 180), (-4, 160), (-14, 148)]
    _shape(cr, hp, col, 4)
    _shape(cr, [(14, 138), (30, 146), (28, 158), (16, 154)], col, 3)
    band(cr, [(-14, 116), (16, 118)], 9, GOLD, spacing=9, hole_r=2.0)
    rivet(cr, 0, 0, 6)


def _baby_leg(cr):
    pts = [(-34, -10), (0, -30), (36, -10), (34, 80), (24, 156), (-20, 158), (-32, 80)]
    _shape(cr, pts, FUR, 5)
    foot = [(-20, 150), (18, 150), (40, 168), (66, 180), (64, 196), (-22, 198)]
    _shape(cr, foot, FUR, 4)
    band(cr, [(-18, 146), (22, 146)], 9, GOLD, spacing=8, hole_r=2.0)
    ink(cr, [(-6, 40), (2, 120)], 2.5, col=FUR2)
    rivet(cr, 0, 0, 7)


def _baby_tail(cr):
    pts = [(0, 0), (-56, 12), (-120, -6), (-160, -70), (-162, -158), (-126, -214), (-86, -212), (-92, -176)]
    band(cr, pts, 24, FUR, spacing=12, hole_r=2.4)
    tip = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        r = 22 if i % 2 == 0 else 15
        tip.append((-94 + r * math.cos(a), -180 + r * 1.2 * math.sin(a)))
    _shape(cr, tip, FUR2, 3)


BABY_MOODS = ("calm", "happy", "wonder", "cheeky", "daze")
for _m in BABY_MOODS:
    register("hn_baby_head" + ("" if _m == "calm" else "_" + _m), (-150, -300, 145, 20),
             (lambda m: lambda cr: baby_head(cr, m))(_m))
register("hn_baby_body", (-70, -215, 85, 55), _baby_body)
register("hn_baby_armB", (-30, -30, 40, 200), lambda cr: _baby_arm(cr, FUR2))
register("hn_baby_tail", (-180, -235, 10, 25), _baby_tail)

BABY = Rig([
    ("hn_baby_tail", "hn_baby_body", (-44, -24), 0.0),
    ("hn_baby_armB", "hn_baby_body", (-18, -176), 0.25),
    ("hn_baby_legB", "hn_baby_body", (-14, 8), 0.06),
    ("hn_baby_legF", "hn_baby_body", (16, 8), -0.06),
    ("hn_baby_body", None, (0, 0), 0.0),
    ("hn_baby_head", "hn_baby_body", (10, -196), 0.0),
    ("hn_baby_armF", "hn_baby_body", (28, -176), -0.25),
], {"handF": ("hn_baby_armF", (4, 176)), "handB": ("hn_baby_armB", (4, 176)),
    "head": ("hn_baby_head", (20, -130)), "top": ("hn_baby_head", (10, -270)), "chin": ("hn_baby_head", (112, -40)),
    "eye": ("hn_baby_head", (62, -158)), "chest": ("hn_baby_body", (10, -130)), "hip": ("hn_baby_body", (0, 0)),
    "tail": ("hn_baby_tail", (-94, -180))},
    [("chest", 30, 0), ("handF", 110, 0)])
register("hn_baby_armF", (-30, -30, 40, 200), lambda cr: _baby_arm(cr))
register("hn_baby_legF", (-42, -36, 72, 205), _baby_leg)
register("hn_baby_legB", (-42, -36, 72, 205), _baby_leg)
BABY_LEG = 205.0                      # the baby's hip above its soles (baby units)


# ------------------------------------------------------------------ grown Hanuman


def hanu_head(cr, mood="calm"):
    """ravana_cast.vanara_head for Hanuman (sindoor fur, a pale muzzle, the tall kirita), with a mood: calm | puzzled
    (brows up, the eye looking down) | sad (the lid low, a sad brow) | joy (eye wide, mouth open) | smile."""
    fur, fur2, muz = HANU_FUR, HANU_FUR2, (1.0, 0.88, 0.70)
    pts = []
    for i in range(17):
        a = math.radians(92 + 176 * i / 16)
        r = 100 if i % 2 == 0 else 76
        pts.append((-16 + r * math.cos(a), -98 - r * math.sin(a)))
    _shape(cr, pts + [(-4, -98)], fur2, 4, smooth=False)
    cran = [(-24, 6), (-34, -40), (-52, -86), (-54, -134), (-38, -176), (0, -198), (40, -188), (60, -162),
            (70, -138), (80, -126), (74, -110), (82, -100), (102, -92), (114, -76), (112, -58), (100, -44),
            (78, -36), (56, -30), (36, -18), (26, 6)]
    if mood == "joy":                                          # the jaw drops open
        cran = cran[:13] + [(108, -74), (84, -66), (102, -50), (96, -34), (76, -24), (52, -20), (34, -10), (26, 6)]
    _shape(cr, cran, fur, 6)
    if mood == "joy":
        mz = [(64, -104), (84, -100), (104, -92), (112, -78), (86, -70), (62, -62), (50, -80)]
        _shape(cr, mz, muz, 4)
        _shape(cr, [(108, -74), (84, -68), (98, -52)], (0.42, 0.05, 0.06), 3.5, smooth=False)
        _shape(cr, [(104, -72), (88, -68), (92, -64), (104, -68)], PALE, 2, smooth=False)
        jaw = [(84, -64), (100, -50), (94, -36), (74, -28), (56, -36), (60, -54)]
        _shape(cr, jaw, muz, 3.5)
    else:
        mz = [(64, -104), (84, -100), (104, -92), (114, -76), (112, -58), (100, -44), (78, -36), (56, -36), (46, -56),
              (50, -86)]
        _shape(cr, mz, muz, 4)
    cr.new_path()
    ell(cr, -26, -110, 19, 26)
    leather(cr, fur, 4)
    cr.new_path()
    ell(cr, -24, -110, 9, 14)
    leather(cr, (1.0, 0.76, 0.62), 3)
    # brow, eye
    if mood == "puzzled":
        band(cr, [(14, -146), (44, -158), (78, -146)], 15, fur2, spacing=11, hole_r=2.2)
        almond_eye(cr, 44, -116, 30, 12, col=PALE, pupil=False)
        cr.new_path()
        cr.arc(48, -111, 7, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(50, -113)], 2)
        ink(cr, [(4, -150), (0, -164)], 3)
    elif mood == "sad":
        band(cr, [(14, -128), (44, -138), (76, -142)], 15, fur2, spacing=11, hole_r=2.2)
        almond_eye(cr, 44, -114, 30, 10, col=PALE, pupil=False)
        cr.new_path()
        cr.arc(46, -110, 6.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        cr.new_path()                                          # the heavy lid
        cr.move_to(28, -116)
        cr.curve_to(36, -128, 52, -128, 60, -114)
        cr.curve_to(52, -118, 36, -118, 28, -116)
        cr.close_path()
        leather(cr, fur, 2.5)
    elif mood in ("smile",):
        band(cr, [(14, -140), (46, -148), (78, -134)], 15, fur2, spacing=11, hole_r=2.2)
        ink(cr, [(30, -112), (44, -124), (60, -114)], 5.5)
    else:                                                      # calm, joy
        up = 10 if mood == "joy" else 0
        band(cr, [(14, -136 - up), (46, -142 - up), (78, -128 - up)], 15, fur2, spacing=11, hole_r=2.2)
        almond_eye(cr, 44, -116, 32 if mood == "joy" else 30, 13 if mood == "joy" else 11, col=PALE)
    punch(cr, [(106, -80)], 4.0)
    ink(cr, [(98, -86), (108, -88)], 3)
    if mood == "sad":
        ink(cr, [(108, -56), (92, -60), (70, -56)], 3.5)
    elif mood == "smile":
        ink(cr, [(110, -62), (92, -54), (70, -58)], 3.5)
    elif mood != "joy":
        ink(cr, [(110, -60), (92, -58), (70, -56)], 3.5)
    if mood != "joy":
        ink(cr, [(60, -44), (70, -40), (84, -42)], 2.5)
    for k in range(4):
        ink(cr, [(-6 + 8 * k, -78 + 6 * k), (6 + 8 * k, -60 + 6 * k)], 2.5, col=fur2)
    _jewel(cr, -24, -74, 14, GOLD)
    R.kirita(cr, GOLD, None, tall=0.95)


HANU = man("hn_hanu", skin=HANU_FUR, bulk=1.2, dhoti=RED, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
           halo=False, hands=("open", "fist"))
HANU_MOODS = ("calm", "puzzled", "sad", "joy", "smile")
for _m in HANU_MOODS:
    register("hn_hanu_head" + ("" if _m == "calm" else "_" + _m), (-200, -450, 135, 100),
             (lambda m: lambda cr: hanu_head(cr, m))(_m))
register("hn_hanu_tail", (-250, -320, 20, 50), lambda cr: R.vali_tail(cr, HANU_FUR, HANU_FUR2))
HANU.parts.insert(0, ("hn_hanu_tail", "hn_hanu_body", (-56, -10), 0.0))
HANU.points["tail"] = ("hn_hanu_tail", (-94, -224))
HANU.points["eye"] = ("hn_hanu_head", (44, -116))


def _hanu_sit(cr):
    """Hanuman seated on a rock, his legs folded in front (hip at 0, 0; soles at +250)."""
    thigh = [(-60, -30), (40, -40), (150, -20), (180, 20), (170, 60), (40, 66), (-66, 50)]
    _shape(cr, thigh, RED, 6)
    dots_in(cr, lambda: spath(cr, thigh), 19, 2.8)
    band(cr, [(120, -26), (176, 30)], 14, GOLD, spacing=11, hole_r=2.4)
    shin = [(150, 30), (190, 40), (200, 140), (196, 220), (160, 222), (150, 140)]
    _shape(cr, shin, HANU_FUR, 5)
    foot = [(156, 214), (196, 212), (226, 230), (250, 240), (248, 254), (156, 256)]
    _shape(cr, foot, HANU_FUR, 4)
    band(cr, [(158, 204), (198, 204)], 9, GOLD, spacing=8, hole_r=2.0)
    rivet(cr, 0, 0, 9)


register("hn_hanu_sit", (-90, -60, 270, 270), _hanu_sit)
HANU_SIT_H = 250.0                    # seated: soles below the hip (hanu units)


def _gada(cr):
    """Hanuman's gada (grip at 0, 0, the head up): a long gold handle, a round ribbed gold head, a red band."""
    band(cr, [(0, 120), (0, -230)], 22, GOLD, spacing=20, hole_r=2.6)
    for y in (90, -40, -200):
        band(cr, [(-16, y), (16, y)], 12, RED, holes=False)
    cr.new_path()
    ell(cr, 0, -330, 96, 106)
    leather(cr, GOLD, 6)
    for k in (-2, -1, 0, 1, 2):
        ink(cr, [(k * 34, -428 + 6 * abs(k)), (k * 44, -330), (k * 34, -232 - 6 * abs(k))], 3.5)
    holes_line(cr, [(-80, -320), (0, -300), (80, -320)], 16, 3)
    band(cr, [(-92, -350), (92, -350)], 16, RED, spacing=12, hole_r=2.6)
    poly(cr, [(-14, -432), (0, -480), (14, -432)])
    leather(cr, GOLD, 4)
    cr.new_path()
    ell(cr, 0, -222, 30, 16)
    leather(cr, GOLD, 4)


register("hn_gada", (-110, -500, 110, 140), _gada)


# ------------------------------------------------------------------ Vayu


def vayu_head(cr, mood="calm"):
    """Vayu: long hair streaming back in the wind, a gold kirita with a blue flare, a pale-blue ring halo."""
    for k, (dy, ln) in enumerate(((-150, 1.0), (-110, 1.15), (-70, 1.05), (-30, 0.9))):
        L = 230 * ln
        pts = [(-30, dy), (-30 - L * 0.3, dy - 18), (-30 - L * 0.6, dy + 14), (-30 - L * 0.85, dy - 10),
               (-30 - L, dy + 8)]
        band(cr, pts, 26 - 3 * k, VY_HAIR, spacing=14, hole_r=2.2)
    A.face(cr, dict(skin=VY_SKIN, hair=False, moustache=True, tilak=True, earring=True), mood)
    R.kirita(cr, GOLD, None, tall=0.95, flare=VY_BLUE)


VAYU = man("hn_vayu", skin=VY_SKIN, bulk=1.05, dhoti=VY_DHOTI, border=GOLD, pleat=VY_BLUE, sash=VY_SASH, neck=GOLD,
           halo=False, thread=True, hands=("open", "open"))
for _m in ("calm", "angry", "hurt"):
    register("hn_vayu_head" + ("" if _m == "calm" else "_" + _m), (-300, -460, 130, 100),
             (lambda m: lambda cr: vayu_head(cr, m))(_m))


# ------------------------------------------------------------------ Jambavan


def jamb_head(cr, mood="calm"):
    """The old bear-king in profile facing +x (neck at 0, 0): a ruff of white fur, a round ear, a long pale muzzle
    with a dark nose, bushy white brows, a white fur beard, a small gold crown. mood: calm | speak | smile."""
    _ruff(cr, -10, -100, 118, 92, 70, 290, 20, (0.84, 0.83, 0.82))
    for k in range(5):
        a = math.radians(110 + 30 * k)
        ink(cr, [(-10 + 70 * math.cos(a), -100 - 70 * math.sin(a)), (-10 + 100 * math.cos(a),
                                                                       -100 - 100 * math.sin(a))], 2.4, col=JB_FUR2)
    cr.new_path()                                                                  # the ear
    ell(cr, -14, -178, 30, 28)
    leather(cr, JB_FUR, 4)
    cr.new_path()
    ell(cr, -12, -176, 15, 14)
    leather(cr, (0.80, 0.56, 0.52), 2.5)
    open_ = 14 if mood == "speak" else 0
    head = [(-26, 6), (-46, -40), (-56, -100), (-44, -156), (-8, -192), (40, -194), (80, -172), (106, -146),
            (138, -128), (170, -118), (184, -100), (182, -82), (166, -72), (136, -66 + open_ * 0.3), (106, -48),
            (72, -24), (40, -6), (20, 8)]
    _shape(cr, head, JB_HEAD, 6)
    mz = [(100, -140), (138, -128), (170, -118), (184, -100), (182, -82), (166, -72), (134, -66), (104, -66),
          (94, -100)]
    _shape(cr, mz, JB_MUZ, 4)
    cr.new_path()                                                                  # the nose
    ell(cr, 178, -104, 15, 12, -0.2)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(182, -108)], 3.5)
    if mood == "speak":
        _shape(cr, [(176, -78), (136, -66), (150, -52), (172, -60)], (0.36, 0.06, 0.06), 3, smooth=False)
    elif mood == "smile":
        ink(cr, [(176, -80), (150, -72), (128, -76)], 3.5)
    else:
        ink(cr, [(176, -78), (150, -72), (130, -70)], 3.5)
    beard = [(16, 8), (40, -6), (72, -24), (106, -48), (130, -60), (124, -34), (104, -6), (80, 22), (56, 44),
             (30, 46), (6, 28)]
    _shape(cr, beard, JB_FUR, 4)
    for k in range(4):
        ink(cr, [(40 + 20 * k, -6 - 10 * k), (36 + 18 * k, 30 - 8 * k)], 2.4, col=JB_FUR2)
    # eye and brow
    if mood == "smile":
        ink(cr, [(58, -128), (72, -138), (88, -128)], 5)
    else:
        almond_eye(cr, 72, -130, 34, 12, col=PALE)
    brow = [(44, -150), (64, -164), (92, -160), (110, -146), (88, -146), (66, -144)]
    _shape(cr, brow, (1.0, 0.99, 0.96), 3.5)
    for k in range(3):
        ink(cr, [(54 + 16 * k, -156 + 2 * k), (60 + 16 * k, -148)], 2, col=JB_FUR2)
    ink(cr, [(46, -118), (40, -104)], 2.4, col=JB_FUR2)                           # wrinkles
    ink(cr, [(90, -116), (100, -106)], 2.4, col=JB_FUR2)
    # a small gold crown
    band(cr, [(-36, -178), (6, -198), (60, -192)], 18, GOLD, spacing=12, hole_r=2.4)
    for x, h_ in ((-24, 40), (12, 56), (48, 40)):
        _shape(cr, [(x - 16, -188 - (x + 36) * 0.2), (x, -188 - h_ - (x + 36) * 0.2), (x + 16, -188 - (x + 36) * 0.2)],
               GOLD, 3.5, smooth=False)
    _jewel(cr, 12, -204, 9, RED)


JAMB = man("hn_jamb", skin=JB_FUR, bulk=1.3, dhoti=JB_DHOTI, border=GOLD, pleat=GOLD, sash=OCHRE, neck=GOLD,
           halo=False, beads=True, hands=("open", "fist"))
for _m in ("calm", "speak", "smile"):
    register("hn_jamb_head" + ("" if _m == "calm" else "_" + _m), (-150, -320, 205, 60),
             (lambda m: lambda cr: jamb_head(cr, m))(_m))


def _jstaff(cr):
    """Jambavan's staff (grip at 0, 0): a knotted wooden staff with a curled top and a gold ring."""
    band(cr, [(0, 420), (2, 100), (-4, -200), (0, -430)], 22, WOOD, spacing=24, hole_r=2.6)
    for y in (300, 40, -260):
        ink(cr, [(-12, y), (12, y - 8)], 3)
    band(cr, [(-14, -380), (14, -380)], 12, GOLD, holes=False)
    band(cr, [(0, -430), (-20, -470), (-60, -480), (-76, -450), (-56, -428), (-36, -444)], 20, WOOD, spacing=14,
         hole_r=2.2)


register("hn_jstaff", (-100, -500, 40, 440), _jstaff)


# ------------------------------------------------------------------ Airavata


def _airavata(cr):
    """Indra's white elephant facing +x (pivot on the ground under its middle): four tusks, a red and gold
    caparison, a gold headpiece, a howdah cloth on its back."""
    for x in (-210, 170):                                                         # far legs
        _shape(cr, [(x - 50, -330), (x + 50, -330), (x + 46, 0), (x - 46, 0)], EL_W2, 5, smooth=False)
    for x in (-250, 130):                                                         # near legs
        _shape(cr, [(x - 56, -340), (x + 56, -340), (x + 52, 0), (x - 52, 0)], EL_W, 6, smooth=False)
        for k in range(3):
            ink(cr, [(x - 40, -40 - 12 * k), (x + 40, -40 - 12 * k)], 2.5, smooth=False, col=EL_W2)
        band(cr, [(x - 54, -70), (x + 54, -70)], 12, GOLD, spacing=10, hole_r=2.2)
    body = [(-330, -380), (-300, -560), (-150, -660), (60, -670), (220, -620), (300, -520), (300, -360), (220, -280),
            (-260, -280)]
    _shape(cr, body, EL_W, 7)
    _shape(cr, [(-336, -420), (-380, -300), (-372, -250), (-356, -300), (-330, -380)], EL_W, 4)
    cap = [(-200, -650), (120, -660), (160, -400), (60, -320), (-200, -320), (-250, -420)]
    _shape(cr, cap, RED, 6, holes=(12, 16, 3))
    dots_in(cr, lambda: spath(cr, cap), 30, 4, shape="d")
    band(cr, [(-246, -400), (-200, -330), (60, -326), (156, -396)], 22, GOLD, spacing=13)
    band(cr, [(-190, -650), (120, -660)], 18, GOLD, spacing=12)
    head = [(220, -620), (330, -690), (420, -650), (450, -540), (440, -420), (380, -360), (300, -380)]
    _shape(cr, head, EL_W, 7)
    for dy in (0, 26):                                                            # the far tusks (behind the trunk)
        _shape(cr, [(372, -404 + dy), (436, -396 + dy), (500, -360 + dy), (540, -370 + dy), (522, -342 + dy),
                    (430, -364 + dy), (366, -378 + dy)], (0.92, 0.88, 0.76), 3.5)
    trunk = [(420, -470), (450, -380), (470, -250), (500, -150), (530, -110), (510, -90), (470, -140), (436, -240),
             (400, -380), (380, -440)]
    _shape(cr, trunk, EL_W, 6)
    for k in range(6):
        y = -400 + 50 * k
        ink(cr, [(404 + 10 * k, y), (444 + 12 * k, y + 8)], 2.5, smooth=False, col=EL_W2)
    for dy in (0, 30):
        _shape(cr, [(380, -410 + dy), (440, -400 + dy), (500, -370 + dy), (552, -386 + dy), (530, -352 + dy),
                    (430, -370 + dy), (370, -380 + dy)], PALE, 4)
    ear = [(250, -640), (180, -600), (160, -480), (200, -400), (270, -420), (300, -520)]
    _shape(cr, ear, EL_W2, 5, holes=(10, 15, 2.6))
    _shape(cr, [(250, -690), (340, -730), (430, -686), (410, -640), (300, -640)], GOLD, 4, holes=(8, 12, 2.4))
    _jewel(cr, 350, -688, 13, RED)
    cr.new_path()
    cr.arc(370, -560, 10, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(373, -563)], 3)


register("hn_airavata", (-400, -760, 580, 20), _airavata)
AIR_SEAT = (-30.0, -690.0)            # Indra's hip on Airavata's back (elephant units)


# ------------------------------------------------------------------ the sun


def _sun(cr):
    """The rising sun as a ripe fruit (centre pivot): a red-orange disc, a darker rim, a shine, a dimple on top."""
    cr.new_path()
    cr.arc(0, 0, SUN_RAD, 0, 2 * math.pi)
    leather(cr, SUN_O, 7)
    cr.new_path()
    cr.arc(6, 8, SUN_RAD - 34, 0, 2 * math.pi)
    leather(cr, SUN_R, 0)
    for k in range(3):
        r = 60 + 40 * k
        holes_line(cr, [(r * math.cos(a), r * math.sin(a)) for a in (i * 0.3 for i in range(22))], 18, 3.0)
    cr.new_path()                                                                 # the shine
    ell(cr, -80, -86, 56, 32, -0.7)
    cr.set_source_rgb(1.0, 0.80, 0.56)
    cr.fill()
    cr.new_path()
    ell(cr, -112, -36, 14, 10, -0.6)
    cr.set_source_rgb(1.0, 0.86, 0.66)
    cr.fill()
    ink(cr, [(-30, -SUN_RAD + 6), (0, -SUN_RAD + 24), (30, -SUN_RAD + 6)], 5)    # the dimple


def _sun_rays(cr):
    pts = []
    n = 28
    for i in range(2 * n):
        a = math.pi * i / n
        r = 330 if i % 4 == 0 else (290 if i % 2 == 0 else 236)
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, (1.0, 0.70, 0.18), 5, smooth=False, holes=(14, 22, 3.2))


def _stem(cr):
    """A stem with two leaves (pivot at the stem's foot, which sits in the sun's dimple)."""
    band(cr, [(0, 8), (4, -40), (18, -80)], 18, BROWN, spacing=12, hole_r=2.2)
    for sg, rot in ((1, 0.0), (-1, 0.35)):
        cr.save()
        cr.translate(12, -64)
        cr.rotate(rot)
        cr.scale(sg, 1)
        lf = [(0, 0), (40, -40), (110, -56), (160, -30), (110, -6), (50, 6)]
        _shape(cr, lf, (0.30, 0.62, 0.22), 4)
        ink(cr, [(6, -2), (80, -26), (150, -30)], 2.5, col=DGREEN)
        cr.restore()


register("hn_sun", (-SUN_RAD - 10, -SUN_RAD - 10, SUN_RAD + 10, SUN_RAD + 10), _sun)
register("hn_sun_rays", (-340, -340, 340, 340), _sun_rays)
register("hn_stem", (-170, -150, 180, 20), _stem)


# ------------------------------------------------------------------ the mountain, the hermitage, the shore


def _hill(cr):
    """A rocky mountain (pivot at the bottom centre): stone facets, green patches at its foot."""
    body = [(-560, 0), (-470, -180), (-380, -300), (-250, -470), (-130, -560), (-40, -640), (40, -610),
            (150, -520), (260, -400), (380, -300), (480, -160), (580, 0)]
    _shape(cr, body, STONE, 7, smooth=False)
    for pts in (((-40, -640), (-60, -420), (-160, -260), (-200, 0)), ((40, -610), (90, -380), (60, -200), (120, 0)),
                ((-250, -470), (-300, -260), (-420, -90))):
        ink(cr, list(pts), 4, smooth=False, col=STONE2)
    face = [(40, -610), (150, -520), (260, -400), (110, -300), (60, -460)]
    _shape(cr, face, (0.76, 0.64, 0.50), 4, smooth=False)
    dots_in(cr, lambda: poly(cr, body), 34, 3.4, shape="d")
    for x, w in ((-420, 150), (-150, 200), (250, 180), (470, 120)):
        g = [(x - w / 2, 4), (x - w / 3, -40), (x, -60), (x + w / 3, -44), (x + w / 2, 4)]
        _shape(cr, g, (0.40, 0.62, 0.26), 4)
    for x, y, s in ((-300, -330, 1.0), (300, -300, 0.8), (-120, -520, 0.7)):     # a few shrubs on its slopes
        cr.new_path()
        ell(cr, x, y, 46 * s, 30 * s)
        leather(cr, (0.36, 0.58, 0.24), 3.5)


register("hn_hill", (-600, -680, 620, 20), _hill)


def _ladle(cr):
    """The sruva, the sacrificial ladle (pivot at its middle): a long wooden handle, a small round bowl."""
    band(cr, [(-200, 0), (120, 0)], 18, WOOD, spacing=16, hole_r=2.4)
    for x in (-160, 60):
        band(cr, [(x, -12), (x, 12)], 8, GOLD, holes=False)
    cr.new_path()
    ell(cr, 160, 0, 46, 32)
    leather(cr, WOOD, 5)
    cr.new_path()
    ell(cr, 162, -2, 30, 18)
    leather(cr, (0.46, 0.26, 0.10), 3)


register("hn_ladle", (-215, -40, 215, 40), _ladle)


def _bark(cr):
    """A heap of bark cloth (valkala) and bark strips, tied with grass (pivot at the bottom centre)."""
    for k, (y, w, col) in enumerate(((0, 300, BARK), (-46, 260, BARK2), (-90, 220, BARK), (-130, 170, BARK2))):
        strip = [(-w / 2, y), (-w / 2 + 16, y - 50), (w / 2 - 10, y - 54), (w / 2 + 6, y - 4)]
        _shape(cr, strip, col, 4.5)
        for j in range(4):
            x = -w / 2 + 40 + j * (w - 70) / 3
            ink(cr, [(x, y - 8), (x + 12, y - 44)], 2.2, col=(0.40, 0.22, 0.08))
    for x in (-80, 70):
        band(cr, [(x, -170), (x + 6, 2)], 9, (0.80, 0.74, 0.36), spacing=10, hole_r=2.0)


register("hn_bark", (-170, -200, 170, 12), _bark)


def _sand(cr):
    """The seashore: a strip of sand (pivot at the top centre of its front edge), shells and pebbles."""
    pts = [(-760, -40), (-400, -60), (0, -48), (400, -64), (760, -40), (760, 160), (-760, 160)]
    _shape(cr, pts, SAND, 6)
    dots_in(cr, lambda: spath(cr, pts), 28, 3.0)
    for x, y in ((-560, 20), (-220, 60), (140, 30), (480, 70), (640, 10)):
        cr.new_path()
        ell(cr, x, y, 18, 11)
        leather(cr, (0.98, 0.92, 0.84), 3)
    for x, y in ((-380, 90), (300, 100), (40, 110)):
        cr.new_path()
        ell(cr, x, y, 22, 14)
        leather(cr, (0.70, 0.66, 0.64), 3)


register("hn_sand", (-770, -80, 770, 170), _sand)


def _beach(cr):
    """The wide beach in front of the sea (pivot at the middle of the shoreline): a wavy line of foam, then sand
    down to the bottom of the screen, shells and pebbles."""
    edge = [(-780 + 40 * i, 10 * math.sin(i * 0.9) + 6 * math.sin(i * 2.3)) for i in range(40)]
    pts = edge + [(780, 1000), (-780, 1000)]
    _shape(cr, pts, SAND, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, pts), 30, 3.0)
    band(cr, [(x, y + 16) for x, y in edge], 18, (0.92, 0.97, 1.0), spacing=16, hole_r=2.6)
    for x, y in ((-600, 160), (-260, 260), (120, 140), (420, 300), (650, 120), (-80, 420), (300, 520), (-480, 560)):
        cr.new_path()
        ell(cr, x, y, 20, 12)
        leather(cr, (0.98, 0.92, 0.84), 3)
    for x, y in ((-400, 330), (230, 380), (560, 450), (-660, 420)):
        cr.new_path()
        ell(cr, x, y, 26, 16)
        leather(cr, (0.70, 0.66, 0.64), 3)


register("hn_beach", (-790, -30, 790, 1010), _beach)


def _palm(cr):
    """A coconut palm (pivot at the foot of its trunk), leaning a little."""
    trunk = [(-30, 0), (30, 0), (40, -300), (70, -600), (110, -840), (80, -846), (34, -600), (4, -300)]
    _shape(cr, trunk, (0.74, 0.54, 0.32), 5)
    for k in range(12):
        y = -60 - 66 * k
        x = 4 + 0.012 * k * k * 60
        ink(cr, [(x - 22, y), (x + 26, y - 10)], 3, col=(0.48, 0.32, 0.16))
    cx, cy = 96, -850
    for a in (-2.9, -2.4, -1.9, -1.2, -0.6, -0.1, 0.4):
        L = 300
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a) + 120 * abs(math.cos(a))
        mx, my = cx + L * 0.5 * math.cos(a), cy + L * 0.5 * math.sin(a) - 40
        lf = [(cx, cy), (mx - 20, my - 30), (ex, ey), (mx + 20, my + 24)]
        _shape(cr, lf, (0.30, 0.58, 0.24), 4)
        ink(cr, [(cx, cy), (mx, my - 4), (ex, ey)], 2.5, col=DGREEN)
    for dx in (-20, 10, 36):
        cr.new_path()
        cr.arc(cx + dx, cy + 34, 20, 0, 2 * math.pi)
        leather(cr, (0.56, 0.40, 0.18), 3)


register("hn_palm", (-260, -1100, 420, 20), _palm)

