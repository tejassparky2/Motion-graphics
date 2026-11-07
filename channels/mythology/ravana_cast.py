"""The leather cast and props for the Ravana reel (videos/ravana.py), in the same Togalu Gombeyaata style as the
Jarasandha reel (puppet_cast): profile figures with big almond eyes, perforated garments and jointed limbs.

Cast (consistent through the video):
  RAVANA     a traditional ten-headed leather puppet (teal-green skin, red dhoti, gold crowns), modelled on no actor:
             the main head in profile with nine smaller heads fanned out on a red perforated head-plate behind it.
             Heads are drawn per frame (ravana_heads) so they can jiggle, laugh, frown and be squashed.
  VALI       king of Kishkindha: a dignified vanara face, gold crown with a green flame halo, gold necklace, a long tail.
  NANDI      Shiva's attendant in the form the text gives him (a vanara-like face): ash marks (tripundra), rudraksha,
             a trident. Never comic.
  KARTA      King Kartavirya Arjuna of Mahishmati; his thousand arms are a fan of separate gold-tipped arms (ka_arm).
  PULASTYA   the old sage: white beard, white matted hair, rudraksha, a staff.
Sets: Shiva linga, marigolds, river strips, two cloth maps, Kailasa, small crowns, the curse note, the tally board,
Lanka's golden walls, a club, trident, staff, rope, droplet.
  HANUMAN    (Lanka) and VANARA (the warriors of the curse and of the army) are full puppets too.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man().
"""
import math
import random

import puppet_cast as C
import puppet_core as pc
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, INK, OCHRE, PALE, PARCH, RED, ROSE, SAFFRON, VIOLET,
                         almond_eye, band, cut, dots_in, ell, holes_line, ink, leather, perforate, poly, punch,
                         register, rivet, spath)

RV_SKIN = (0.34, 0.62, 0.58)        # Ravana: teal-green leather
VALI_FUR = (0.96, 0.68, 0.30)       # Vali: golden fur
VALI_FUR2 = (0.80, 0.46, 0.16)
NANDI_FUR = (0.76, 0.58, 0.40)      # Nandi: dark tawny ("krishna-pingala")
NANDI_FUR2 = (0.55, 0.36, 0.20)
KA_SKIN = (1.0, 0.77, 0.52)         # Kartavirya Arjuna
SAGE_SKIN = (0.96, 0.80, 0.60)
ASH = (0.90, 0.89, 0.86)            # the sage's white hair
STONE = (0.56, 0.55, 0.60)
STONE2 = (0.44, 0.43, 0.50)
STONE_D = (0.36, 0.36, 0.44)
WATER = (0.46, 0.70, 1.0)
WATER2 = (0.24, 0.48, 0.92)
SEA = (0.66, 0.82, 1.0)
ROPE = (0.88, 0.70, 0.40)
SNOW = (1.0, 1.0, 1.0)
ROCK = (0.56, 0.60, 0.78)
LAND = (0.76, 0.88, 0.50)

FAN_C = (-10.0, -168.0)             # centre of Ravana's fan of heads (head coordinates, neck at 0, 0)
FAN_R = 268.0                       # small heads' centres
PLATE_R = (168.0, 214.0)            # the head-plate band their necks sit on
FAN_A0, FAN_A1 = math.pi + 0.22, 2 * math.pi - 0.22
HEAD_C = (2.0, -128.0)              # visual centre of one head (for placing the small heads)
MINI = 0.52
WAVE_P = 160.0                      # river strip wavelength (design units)


# ------------------------------------------------------------------ crowns


def kirita(cr, col=GOLD, halo=None, tall=1.0, flare=RED):
    """A kirita crown on a profile head (as puppet_cast.man_head draws it), `tall` scales its height."""
    if halo:
        pts = []
        for i in range(19):
            a = math.pi * (0.62 + 0.9 * i / 18)
            r = 160 if i % 2 == 0 else 128
            pts.append((-30 + r * math.cos(a) * 1.05, -190 + r * math.sin(a) * 1.1))
        pts += [(-40, -150), (0, -160)]
        _shape(cr, pts, halo, 5, smooth=False, holes=(14, 15, 3))
    h = lambda y: -150 + (y + 150) * tall
    kp = [(-50, -150), (-48, h(-196)), (-34, h(-252)), (-18, h(-312)), (0, h(-350)), (18, h(-312)), (34, h(-252)),
          (50, h(-196)), (56, -150)]
    _shape(cr, kp, col, 6, smooth=False, holes=(11, 14, 2.8))
    for y, w in ((-196, 46), (-252, 32)):
        band(cr, [(-w - 2, h(y)), (w + 4, h(y) - 2)], 12, RED, spacing=11, hole_r=2.4)
    _jewel(cr, 4, h(-222), 13, RED)
    cr.new_path()
    cr.arc(0, h(-350) - 10, 12, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    poly(cr, [(-6, h(-350) - 20), (0, h(-350) - 50), (6, h(-350) - 20)])
    leather(cr, GOLD, 3)
    fl = [(-48, -168), (-96, -200), (-112, -170), (-96, -140), (-60, -140)]
    _shape(cr, fl, flare, 4, holes=(9, 12, 2.4))
    band(cr, [(-52, -156), (60, -150)], 16, GOLD, spacing=12)


# ------------------------------------------------------------------ Ravana


def ravana_head(cr, mood="calm"):
    """Ravana's head in profile (facing +x): heavy curled moustache, big eye, red tilak, a short kirita."""
    hp = [(-24, -178), (-62, -152), (-88, -100), (-92, -40), (-78, 14), (-52, 30), (-38, -28), (-30, -96)]
    _shape(cr, hp, HAIR, 5)
    for k in range(3):
        holes_line(cr, [(-46 - 10 * k, -146 + 8 * k), (-72 - 4 * k, -60), (-62 - 2 * k, 10)], 16, 2.4)
    face = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
            (60, -128), (66, -116), (94, -92), (70, -82), (72, -72), (64, -64), (68, -56), (58, -44), (54, -30),
            (34, -22), (26, 6)]
    if mood == "laugh":          # the jaw drops open
        face = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
                (60, -128), (66, -116), (94, -92), (74, -84), (46, -72), (72, -36), (66, -22), (54, -12),
                (34, -8), (26, 6)]
    _shape(cr, face, RV_SKIN, 6)
    cr.new_path()
    ell(cr, -14, -108, 13, 21)
    leather(cr, RV_SKIN, 4)
    if mood == "laugh":
        _shape(cr, [(76, -84), (44, -72), (72, -36)], (0.42, 0.05, 0.06), 4, smooth=False)
        _shape(cr, [(74, -83), (50, -74), (54, -68), (74, -77)], PALE, 2.5, smooth=False)
        _shape(cr, [(66, -46), (60, -54), (54, -58), (70, -40)], ROSE, 2, smooth=False)
        ink(cr, [(16, -112), (34, -128), (54, -114)], 7)                          # eye squeezed shut
        ink(cr, [(20, -104), (34, -98), (48, -104)], 3)
        ink(cr, [(12, -150), (34, -160), (58, -150)], 5)
    elif mood == "angry":
        almond_eye(cr, 34, -116, 40, 14, col=(1.0, 0.60, 0.48))
        ink(cr, [(6, -154), (34, -144), (62, -124)], 9)                           # brow pulled down
        ink(cr, [(2, -146), (-4, -130)], 3)
        ink(cr, [(72, -70), (58, -64)], 4)
        _shape(cr, [(62, -66), (66, -54), (70, -66)], PALE, 2.5, smooth=False)    # a bared tooth
    else:
        almond_eye(cr, 34, -118, 40, 14, col=PALE)
        ink(cr, [(14, -138), (34, -148), (58, -138)], 5)
        ink(cr, [(70, -70), (60, -68)], 3)
    dy = -6 if mood == "laugh" else 0
    m = [(74, -80 + dy), (58, -84 + dy), (42, -84 + dy), (30, -90 + dy), (24, -102 + dy), (30, -112 + dy),
         (38, -108 + dy), (34, -100 + dy), (44, -92 + dy), (60, -88 + dy), (74, -85 + dy)]
    _shape(cr, m, HAIR, 3)
    ink(cr, [(52, -150), (54, -172)], 6, col=RED)
    _jewel(cr, -12, -72, 17, GOLD)
    poly(cr, [(-20, -56), (-12, -32), (-4, -56)])
    leather(cr, RED, 3)
    kirita(cr, GOLD, None, tall=0.62)


def _rv_fan(cr):
    """The red perforated head-plate that carries the nine smaller heads (one leather piece, as real puppets do)."""
    cx, cy = FAN_C
    r0, r1 = PLATE_R
    a0, a1 = FAN_A0 - 0.16, FAN_A1 + 0.16
    cr.new_path()
    cr.arc(cx, cy, r1, a0, a1)
    cr.arc_negative(cx, cy, r0, a1, a0)
    cr.close_path()
    pl = leather(cr, GOLD, 6, keep=True)
    perforate(cr, pl, 9, 14, 2.6)
    for i in range(13):
        a = a0 + (a1 - a0) * (i + 0.5) / 13
        _jewel(cr, cx + (r0 + r1) / 2 * math.cos(a), cy + (r0 + r1) / 2 * math.sin(a), 8, RED)
    for a in (a0, a1):
        _flower(cr, cx + (r0 + r1) / 2 * math.cos(a), cy + (r0 + r1) / 2 * math.sin(a), 26, RED, 8)


def ravana_heads(t, mood="calm", jig=0.0, squash=0.0, head_rot=0.0, alpha=1.0, blur=0.0, look=0.0):
    """extra= callback for the body part: the head-plate and the nine small heads (behind the main head).
    jig 0..1 = how hard they shake (laughing), squash 0..1 = pressed flat (under Vali's arm), look = a turn of all
    heads (radians)."""
    name = {"calm": "ravana_head", "laugh": "ravana_head_laugh", "angry": "ravana_head_angry"}[mood]

    def fn(cr):
        cr.save()
        cr.translate(6, -300)
        cr.rotate(head_rot)
        cr.translate(*FAN_C)
        cr.scale(1 - 0.22 * squash, 1 - 0.42 * squash)
        cr.translate(-FAN_C[0], -FAN_C[1])
        base = cr.get_matrix()
        pc.paint_part(cr, "rv_fan", alpha, blur)
        for i in (0, 8, 1, 7, 2, 6, 3, 5, 4):             # outer heads first, the top one last
            a = FAN_A0 + (FAN_A1 - FAN_A0) * i / 8
            ph = i * 1.37
            px = FAN_C[0] + FAN_R * math.cos(a)
            py = FAN_C[1] + FAN_R * math.sin(a)
            r = (a - 1.5 * math.pi) * 0.5 + 0.03 * math.sin(t * 1.7 + ph) + look
            r += jig * 0.22 * math.sin(t * 17 + ph * 2.1)
            py += jig * 14 * math.sin(t * 19 + ph)
            if squash:
                r += squash * 0.5 * math.sin(ph * 3.1)
            cr.set_matrix(base)
            cr.translate(px, py)
            cr.rotate(r)
            cr.scale(MINI, MINI * (1 - 0.25 * squash))
            cr.translate(-HEAD_C[0], -HEAD_C[1])
            pc.paint_part(cr, name, alpha, blur)
        cr.restore()
    return fn


def ravana_kneel(cr):
    """Ravana's legs kneeling on one knee (hip at 0, 0; ground at y=+250)."""
    b = 1.18
    _shape(cr, [(-40, 196), (-36, 242), (-190, 250), (-200, 232), (-180, 212)], RV_SKIN, 5)          # back shin
    _shape(cr, [(-186, 214), (-232, 200), (-240, 246), (-194, 250)], RV_SKIN, 4)                      # back foot
    th = [(-54 * b, -20), (44 * b, -24), (44, 40), (14, 226), (-48, 236), (-72, 100)]
    _shape(cr, th, DRED, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(-46, 214), (16, 214)], 14, GOLD, spacing=11, hole_r=2.4)
    _shape(cr, [(120, 40), (170, 40), (168, 222), (126, 226)], RV_SKIN, 5)                           # front shin
    _shape(cr, [(118, 214), (170, 212), (226, 230), (228, 250), (116, 252)], RV_SKIN, 4)              # front foot
    band(cr, [(124, 204), (168, 204)], 9, GOLD, spacing=8, hole_r=2.0)
    fth = [(-40, -34), (60, -40), (176, 8), (182, 70), (120, 82), (-30, 60)]
    _shape(cr, fth, DRED, 5)
    dots_in(cr, lambda: spath(cr, fth), 19, 2.8)
    band(cr, [(120, 76), (186, 64)], 14, GOLD, spacing=11, hole_r=2.4)
    pf = [(30, 40), (70, 40), (92, 180), (78, 196), (64, 182), (50, 198), (36, 182), (22, 194)]
    _shape(cr, pf, GOLD, 4, smooth=False)
    rivet(cr, 0, 0, 9)


RAVANA = man("ravana", skin=RV_SKIN, bulk=1.18, dhoti=DRED, border=GOLD, pleat=GOLD, sash=VIOLET, neck=GOLD,
             halo=False, hands=("open", "fist"))
register("ravana_head", (-130, -345, 125, 40), lambda cr: ravana_head(cr, "calm"))
register("ravana_head_laugh", (-130, -345, 125, 40), lambda cr: ravana_head(cr, "laugh"))
register("ravana_head_angry", (-130, -345, 125, 40), lambda cr: ravana_head(cr, "angry"))
register("rv_fan", (-330, -480, 320, -96), _rv_fan)
register("ravana_kneel", (-250, -60, 240, 260), ravana_kneel)


# ------------------------------------------------------------------ vanara heads (Vali, Nandi)


def vanara_head(cr, o):
    """A dignified vanara face in profile: a ruff of fur, a rounded brow, a pale muzzle, calm almond eye."""
    fur, fur2, muz = o["fur"], o["fur2"], o.get("muzzle", (1.0, 0.88, 0.70))
    pts = []
    for i in range(17):
        a = math.radians(92 + 176 * i / 16)
        r = 100 if i % 2 == 0 else 76
        pts.append((-16 + r * math.cos(a), -98 - r * math.sin(a)))
    _shape(cr, pts + [(-4, -98)], fur2, 4, smooth=False)
    cran = [(-24, 6), (-34, -40), (-52, -86), (-54, -134), (-38, -176), (0, -198), (40, -188), (60, -162),
            (70, -138), (80, -126), (74, -110), (82, -100), (102, -92), (114, -76), (112, -58), (100, -44),
            (78, -36), (56, -30), (36, -18), (26, 6)]
    _shape(cr, cran, fur, 6)
    mz = [(64, -104), (84, -100), (104, -92), (114, -76), (112, -58), (100, -44), (78, -36), (56, -36), (46, -56),
          (50, -86)]
    _shape(cr, mz, muz, 4)
    cr.new_path()
    ell(cr, -26, -110, 19, 26)
    leather(cr, fur, 4)
    cr.new_path()
    ell(cr, -24, -110, 9, 14)
    leather(cr, (1.0, 0.76, 0.62), 3)
    band(cr, [(14, -136), (46, -142), (78, -128)], 15, fur2, spacing=11, hole_r=2.2)
    almond_eye(cr, 44, -116, 30, 11, col=PALE)
    punch(cr, [(106, -80)], 4.0)
    ink(cr, [(98, -86), (108, -88)], 3)
    ink(cr, [(110, -60), (92, -58), (70, -56)], 3.5)
    ink(cr, [(60, -44), (70, -40), (84, -42)], 2.5)
    for k in range(4):                                                            # cheek fur lines
        ink(cr, [(-6 + 8 * k, -78 + 6 * k), (6 + 8 * k, -60 + 6 * k)], 2.5, col=fur2)
    if o.get("tripundra"):                                                        # three lines of ash, red dot
        for k in range(3):
            y = -178 + 13 * k
            cut(cr, lambda y=y: ell(cr, 22, y, 40, 4.2, -0.06))
        cr.new_path()
        cr.arc(24, -165, 7.5, 0, 2 * math.pi)
        cr.set_source_rgb(*RED)
        cr.fill()
    if o.get("band"):                                                             # a warrior's headband
        band(cr, [(-50, -150), (10, -176), (64, -166)], 16, o["band"], spacing=11, hole_r=2.4)
    if o.get("earring", True):
        _jewel(cr, -24, -74, 14, o.get("ear_col", GOLD))
    if o.get("rudraksha"):
        for i in range(9):
            a = math.radians(200 + 18 * i)
            cr.new_path()
            cr.arc(-6 + 40 * math.cos(a) * 1.4, -6 + 40 * math.sin(a) * 0.5, 7, 0, 2 * math.pi)
            leather(cr, BROWN, 2.5)
    if o.get("crown"):
        kirita(cr, GOLD, o.get("halo"), tall=0.9)


def vali_tail(cr, fur=VALI_FUR, fur2=VALI_FUR2):
    pts = [(0, 0), (-70, 26), (-150, 16), (-206, -56), (-214, -170), (-176, -256), (-114, -290), (-76, -262),
           (-92, -226)]
    band(cr, pts, 30, fur, spacing=13, hole_r=2.6)
    tip = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        r = 26 if i % 2 == 0 else 19
        tip.append((-94 + r * math.cos(a), -224 + r * 1.2 * math.sin(a)))
    _shape(cr, tip, fur2, 3)


def vali_sit(cr):
    """Vali's crossed legs, seated for his twilight prayer (hip at 0, 0; ground at y=+112)."""
    lump = [(-84, -24), (70, -30), (160, -6), (214, 40), (208, 92), (150, 112), (-60, 112), (-104, 70)]
    _shape(cr, lump, RED, 6)
    dots_in(cr, lambda: spath(cr, lump), 20, 3.0)
    band(cr, [(-90, 96), (40, 104), (190, 94)], 14, GOLD, spacing=12)
    _shape(cr, [(110, 20), (164, 4), (200, 26), (176, 52), (120, 46)], VALI_FUR, 4)
    ink(cr, [(140, 22), (178, 30)], 2.5)
    band(cr, [(104, 34), (124, 50)], 9, GOLD, spacing=8, hole_r=2.0)
    rivet(cr, 0, 0, 9)


VALI = man("vali", skin=VALI_FUR, bulk=1.32, dhoti=RED, border=GOLD, pleat=GOLD, sash=DGREEN, neck=GOLD,
           hands=("open", "open"), halo=False)
_VALI_O = dict(fur=VALI_FUR, fur2=VALI_FUR2, crown=True, halo=DGREEN)
register("vali_head", (-200, -430, 130, 100), lambda cr: vanara_head(cr, _VALI_O))
register("vali_tail", (-250, -320, 20, 50), vali_tail)
register("vali_sit", (-120, -50, 230, 130), vali_sit)
VALI.parts.insert(0, ("vali_tail", "vali_body", (-56, -10), 0.0))
VALI.points["tail"] = ("vali_tail", (-96, -222))

NANDI = man("nandi", skin=NANDI_FUR, bulk=1.25, dhoti=OCHRE, border=DRED, pleat=OCHRE, sash=DRED, neck=BROWN,
            beads=True, halo=False, hands=("fist", "open"))
_NANDI_O = dict(fur=NANDI_FUR, fur2=NANDI_FUR2, tripundra=True, ear_col=BROWN)
register("nandi_head", (-130, -220, 130, 30), lambda cr: vanara_head(cr, _NANDI_O))

VAN_FUR = (0.66, 0.44, 0.26)        # the vanara warriors (the curse, the army at Lanka)
VAN_FUR2 = (0.46, 0.28, 0.14)
VANARA = man("vanara", skin=VAN_FUR, bulk=1.12, dhoti=OCHRE, border=DRED, pleat=OCHRE, sash=DGREEN, neck=BROWN,
             halo=False, hands=("fist", "fist"))
_VAN_O = dict(fur=VAN_FUR, fur2=VAN_FUR2, band=RED)
register("vanara_head", (-130, -220, 130, 30), lambda cr: vanara_head(cr, _VAN_O))
register("vanara_tail", (-250, -320, 20, 50), lambda cr: vali_tail(cr, VAN_FUR, VAN_FUR2))
VANARA.parts.insert(0, ("vanara_tail", "vanara_body", (-56, -10), 0.0))


def _club(cr):
    """A vanara's club: a tree branch with a knotted head (grip at 0, 0)."""
    band(cr, [(0, 60), (2, -200), (-6, -330)], 18, BROWN, spacing=22, hole_r=2.4)
    cr.new_path()
    ell(cr, -8, -380, 46, 64, -0.1)
    leather(cr, BROWN, 5)
    for x, y in ((-24, -400), (8, -360), (-10, -420)):
        punch(cr, [(x, y)], 5)
    band(cr, [(-26, -318), (22, -320)], 10, GOLD, spacing=9, hole_r=2)


register("rv_club", (-60, -450, 50, 80), _club)

HANU_FUR = (1.0, 0.56, 0.26)        # Hanuman: sindoor orange
HANU_FUR2 = (0.80, 0.30, 0.10)
HANUMAN = man("hanuman", skin=HANU_FUR, bulk=1.2, dhoti=RED, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
              halo=False, hands=("open", "fist"))
_HANU_O = dict(fur=HANU_FUR, fur2=HANU_FUR2, crown=True, halo=None)
register("hanuman_head", (-200, -430, 130, 100), lambda cr: vanara_head(cr, _HANU_O))
register("hanuman_tail", (-250, -320, 20, 50), lambda cr: vali_tail(cr, HANU_FUR, HANU_FUR2))
HANUMAN.parts.insert(0, ("hanuman_tail", "hanuman_body", (-56, -10), 0.0))
HANUMAN.points["tail"] = ("hanuman_tail", (-94, -224))


# ------------------------------------------------------------------ Kartavirya Arjuna and Pulastya

KARTA = man("karta", skin=KA_SKIN, bulk=1.15, dhoti=GOLD, border=RED, pleat=RED, sash=BLUE, moustache=True,
            crown_col=GOLD, halo_col=RED)


def ka_arm(cr):
    """One of the thousand arms: shoulder at (0, 0), pointing down (+y), a gold hand."""
    pts = [(-24, -8), (-14, -28), (0, -32), (14, -28), (24, -8), (22, 110), (16, 150), (18, 230), (14, 286),
           (-14, 286), (-18, 230), (-16, 150), (-22, 110)]
    _shape(cr, pts, KA_SKIN, 5)
    band(cr, [(-23, 56), (23, 58)], 13, GOLD, spacing=10, hole_r=2.3)
    for y in (258, 272):
        band(cr, [(-15, y), (15, y + 2)], 8, GOLD, spacing=8, hole_r=1.8)
    hp = [(-14, 282), (14, 282), (24, 310), (20, 344), (8, 334), (0, 352), (-8, 336), (-18, 324), (-20, 300)]
    _shape(cr, hp, GOLD, 4)
    ink(cr, [(0, 300), (0, 334)], 2.5)
    rivet(cr, 0, 0, 6)


register("ka_arm", (-40, -40, 40, 360), ka_arm)

PULASTYA = man("pulastya", skin=SAGE_SKIN, bulk=0.86, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=SAFFRON,
               crown="tiara", beard=True, hair=False, robe=SAFFRON, beads=True, halo=False, earring=False, neck=BROWN,
               hands=("fist", "open"), tilak=False)
_PUL_O = dict(skin=SAGE_SKIN, crown="tiara", beard=True, hair=False, earring=False, tilak=False)


def pulastya_head(cr):
    """The old sage: white hair falling behind, white matted hair piled up, white brows, ash marks."""
    hp = [(-30, -176), (-64, -146), (-90, -70), (-96, 40), (-70, 120), (-46, 70), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-50 - 10 * k, -140), (-74 - 6 * k, -20), (-66 - 4 * k, 90)], 2.5, col=(0.6, 0.58, 0.55))
    C.man_head(cr, _PUL_O)
    for k in range(5):
        cr.new_path()
        ell(cr, -4 - 3 * k, -194 - 26 * k, 52 - 6 * k, 22)
        leather(cr, ASH, 4)
        ink(cr, [(-40 + 6 * k, -194 - 26 * k), (-4, -184 - 26 * k), (32 - 6 * k, -196 - 26 * k)], 2.5)
    for i in range(7):                                                            # a rudraksha string round the bun
        cr.new_path()
        cr.arc(-44 + 14 * i, -178, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    ink(cr, [(12, -140), (34, -146), (58, -138)], 7, col=ASH)
    m = [(66, -76), (46, -84), (24, -88), (12, -74), (30, -78), (52, -76), (68, -72)]
    _shape(cr, m, ASH, 3)
    for k in range(3):
        ink(cr, [(2, -170 + 9 * k), (44, -172 + 9 * k)], 3, col=(1.0, 0.97, 0.9))


register("pulastya_head", (-190, -360, 110, 140), pulastya_head)


# ------------------------------------------------------------------ props


def _linga(cr):
    """A Shiva linga on its pedestal, in profile: dark stone, three lines of ash and a red dot."""
    base = [(-170, 0), (170, 0), (170, -26), (150, -34), (150, -62), (-150, -62), (-150, -34), (-170, -26)]
    _shape(cr, base, STONE2, 6, smooth=False, holes=(10, 14, 3))
    yoni = [(-150, -62), (150, -62), (248, -78), (262, -96), (248, -110), (150, -114), (-150, -114), (-164, -88)]
    _shape(cr, yoni, STONE, 6, smooth=False)
    holes_line(cr, [(-140, -88), (236, -94)], 16, 3, smooth=False)
    lp = [(-66, -110), (-68, -210), (-56, -262), (-28, -290), (0, -298), (28, -290), (56, -262), (68, -210),
          (66, -110)]
    _shape(cr, lp, STONE_D, 6)
    for k in range(3):
        y = -238 + 17 * k
        cut(cr, lambda y=y: ell(cr, 0, y, 48, 4.6))
    cr.new_path()
    cr.arc(0, -221, 9, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    holes_line(cr, [(-58, -130), (58, -130)], 13, 2.6, smooth=False)


def _marigold(cr, col):
    pts = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        r = 32 if i % 2 == 0 else 24
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, col, 3.5, smooth=False)
    cr.new_path()
    cr.arc(0, 0, 13, 0, 2 * math.pi)
    leather(cr, DRED if col == GOLD else GOLD, 3)
    punch(cr, [(20 * math.cos(a), 20 * math.sin(a)) for a in [i * 1.047 for i in range(6)]], 2.4)


def _wave(cr, col):
    """A long river / sea strip: wavy top, perforated, repeating every WAVE_P units (scrolls seamlessly)."""
    top = [(x, -22 + 14 * math.sin(2 * math.pi * x / WAVE_P)) for x in range(-1040, 1041, 10)]
    cr.new_path()
    poly(cr, top + [(1040, 48), (-1040, 48)])
    leather(cr, col, 5)
    holes_line(cr, [(-1030, 16), (1030, 16)], 20, 3.2, smooth=False)
    for k in range(-7, 8):
        x = WAVE_P * (k - 0.25)
        punch(cr, [(x + 14, -24), (x + 24, -18)], 3.6)


def _drop(cr):
    _shape(cr, [(0, -24), (10, -6), (12, 6), (0, 15), (-12, 6), (-10, -6)], WATER, 3)
    punch(cr, [(-3, 2)], 2.5)


def _map(cr):
    """The cloth map Ravana marches across: lands, hills, rivers, the sea, hung from a rod."""
    cloth = [(-460, -330), (460, -330), (468, 320)]
    for i in range(12):
        x = 468 - 936 * (i + 0.5) / 12
        cloth.append((x, 346 if i % 2 == 0 else 322))
    cloth += [(-468, 320)]
    _shape(cr, cloth, PARCH, 7, smooth=False, holes=(14, 17, 3.2))
    land = [(-400, -250), (-200, -290), (40, -260), (250, -280), (400, -200), (420, 0), (380, 210), (180, 270),
            (-40, 230), (-230, 280), (-410, 180), (-430, -40)]
    _shape(cr, land, LAND, 5, holes=(10, 15, 2.6))
    for x, y in ((-250, -150), (-200, -170), (60, -170), (110, -190), (300, 60), (250, 40)):
        _shape(cr, [(x - 40, y + 30), (x, y - 40), (x + 40, y + 30)], OCHRE, 3.5, smooth=False)
        ink(cr, [(x, y - 40), (x + 10, y + 20)], 2.5)
    for pts in (((-380, -60), (-250, 0), (-120, -40), (20, 30), (160, 0), (300, 130), (380, 180)),
                ((-100, 240), (-60, 120), (40, 90))):
        ink(cr, pts, 9, col=INK)
        ink(cr, pts, 5, col=BLUE)
    for x, y in ((-330, 120), (-300, 160), (150, -100), (190, -60), (-60, -200), (330, -140)):
        cr.new_path()
        cr.arc(x, y, 16, 0, 2 * math.pi)
        leather(cr, DGREEN, 3)
    for x, y in ((-440, 290), (440, -300), (430, 290), (-445, -300)):
        for k in range(3):
            ink(cr, [(x - 30 + 0, y + 8 * k), (x - 10, y - 6 + 8 * k), (x + 10, y + 8 * k)], 2.5, col=BLUE)
    band(cr, [(-500, -344), (500, -344)], 24, BROWN, spacing=16)
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 510, -344, 18, 0, 2 * math.pi)
        leather(cr, GOLD, 4)


def _omap(cr):
    """A round cloth map: the land in the middle, the ocean all round it (four oceans: S, W, N, E)."""
    cloth = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        r = 470 if i % 2 == 0 else 452
        cloth.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, cloth, PARCH, 7, smooth=False, holes=(14, 17, 3.2))
    cr.new_path()
    cr.arc(0, 0, 410, 0, 2 * math.pi)
    leather(cr, SEA, 6)
    rng = random.Random(3)
    for ring in (370, 300):
        for k in range(18):
            a = 2 * math.pi * (k + rng.uniform(0, 0.5)) / 18
            x, y = ring * math.cos(a), ring * math.sin(a)
            ink(cr, [(x - 22, y + 4), (x - 8, y - 8), (x + 6, y + 4), (x + 20, y - 8)], 3, col=WATER2)
    land = []
    for i in range(20):
        a = 2 * math.pi * i / 20
        r = 200 + 30 * math.sin(3 * a + 0.6) + 18 * math.cos(5 * a)
        land.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, land, LAND, 5, holes=(10, 15, 2.6))
    for x, y in ((-70, -60), (-20, -90), (40, -50), (90, 40), (-90, 70)):
        _shape(cr, [(x - 34, y + 26), (x, y - 34), (x + 34, y + 26)], OCHRE, 3.5, smooth=False)
    for x, y in ((-40, 110), (40, 120), (110, -100), (-120, -10)):
        cr.new_path()
        cr.arc(x, y, 14, 0, 2 * math.pi)
        leather(cr, DGREEN, 3)


def _kailasa(cr):
    """Mount Kailasa: a snow-capped dome over a blue range, with ledges of snow."""
    back = [(-700, 0), (-600, -260), (-520, -220), (-420, -380), (-330, -300), (-240, -420), (240, -420),
            (330, -300), (420, -380), (520, -220), (600, -260), (700, 0)]
    _shape(cr, back, (0.66, 0.70, 0.86), 6, smooth=False, holes=(12, 18, 3))
    main = [(-440, 0), (-330, -270), (-220, -500), (-150, -620), (-80, -690), (0, -716), (80, -690), (150, -620),
            (220, -500), (330, -270), (440, 0)]
    _shape(cr, main, ROCK, 7, smooth=False)
    snow = [(-200, -520), (-110, -660), (0, -716), (110, -660), (200, -520), (150, -480), (104, -530), (50, -470),
            (0, -520), (-50, -468), (-104, -530), (-150, -480)]
    _shape(cr, snow, SNOW, 5, smooth=False)
    for y, w in ((-400, 230), (-300, 300), (-190, 360)):
        _shape(cr, [(-w, y), (w, y - 6), (w - 20, y + 16), (-w + 20, y + 20)], SNOW, 4, smooth=False)
    for sx in (-1, 1):
        holes_line(cr, [(sx * 20, -690), (sx * 120, -500), (sx * 250, -260), (sx * 380, -40)], 22, 3.6)
    for sx in (-1, 1):
        _shape(cr, [(sx * 600, -260), (sx * 560, -236), (sx * 640, -150), (sx * 620, -210)], SNOW, 3,
               smooth=False)


def _crown_s(cr):
    pts = [(-32, 0), (32, 0), (36, -26), (22, -14), (14, -42), (0, -22), (-14, -42), (-22, -14), (-36, -26)]
    _shape(cr, pts, GOLD, 4, smooth=False)
    _jewel(cr, 0, -10, 6, RED)


def _note(cr):
    """A torn parchment note (the curse), pinned at the top."""
    rng = random.Random(7)
    w, h = 380, 250
    pts = []
    for i in range(20):
        pts.append((-w + 2 * w * i / 19, -h + rng.uniform(-8, 8)))
    for i in range(1, 12):
        pts.append((w + rng.uniform(-6, 6), -h + 2 * h * i / 12))
    for i in range(24):
        pts.append((w - 2 * w * i / 23, h + (rng.uniform(4, 22) if i % 2 else rng.uniform(-16, 0))))
    for i in range(1, 12):
        pts.append((-w + rng.uniform(-6, 6), h - 2 * h * i / 12))
    _shape(cr, pts, PARCH, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-w + 30, -h + 30), (w - 30, -h + 30), (w - 30, h - 30), (-w + 30, h - 30)]),
            60, 1.6)
    rivet(cr, 0, -h + 26, 12)


def _tally(cr):
    """The tally board (text and boxes are drawn over it per frame)."""
    pts = [(-400, -300), (-350, -340), (350, -340), (400, -300), (400, 300), (350, 340), (-350, 340), (-400, 300)]
    _shape(cr, pts, PARCH, 8, smooth=False, holes=(16, 17, 3.6))
    cr.new_path()
    poly(cr, [(-360, -300), (360, -300), (360, 300), (-360, 300)])
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    for sx in (-1, 1):
        for y in (-300, 300):
            _flower(cr, sx * 360, y, 24, RED, 8)


def _lanka(cr):
    """Lanka's golden walls: towers with domes, a great gate, crenellations."""
    wall = [(-560, 0), (560, 0), (560, -300)]
    for i in range(14, -1, -1):
        x = -560 + 80 * i
        if i > 0:
            wall += [(x, -300), (x, -340), (x - 40, -340), (x - 40, -300)]
    wall += [(-560, -300)]
    _shape(cr, wall, GOLD, 7, smooth=False)
    for row in range(4):
        holes_line(cr, [(-550, -50 - 70 * row), (550, -50 - 70 * row)], 34, 4, smooth=False)
    for x0 in (-430, 430):
        tw = [(x0 - 70, 0), (x0 + 70, 0), (x0 + 70, -470), (x0 - 70, -470)]
        _shape(cr, tw, OCHRE, 6, smooth=False, holes=(12, 16, 3))
        dome = [(x0 - 80, -470), (x0 - 70, -540), (x0 - 30, -590), (x0, -604), (x0 + 30, -590), (x0 + 70, -540),
                (x0 + 80, -470)]
        _shape(cr, dome, RED, 6, holes=(10, 14, 3))
        poly(cr, [(x0 - 5, -600), (x0, -660), (x0 + 5, -600)])
        leather(cr, GOLD, 3)
        for k in range(3):
            cut(cr, lambda k=k, x0=x0: ell(cr, x0, -140 - 110 * k, 14, 30))
    gop = [(-170, 0), (170, 0), (150, -420), (110, -470), (80, -560), (40, -610), (0, -640), (-40, -610),
           (-80, -560), (-110, -470), (-150, -420)]
    _shape(cr, gop, OCHRE, 7, smooth=False, holes=(12, 16, 3))
    for y, w in ((-420, 150), (-490, 104), (-570, 64)):
        band(cr, [(-w, y), (w, y)], 14, RED, spacing=12)
    gate = [(-100, 0), (100, 0), (100, -200), (60, -260), (0, -284), (-60, -260), (-100, -200)]
    _shape(cr, gate, (0.30, 0.16, 0.08), 6)
    for gx in (-60, -20, 20, 60):
        for gy in (-50, -110, -170):
            cr.new_path()
            cr.arc(gx, gy, 8, 0, 2 * math.pi)
            leather(cr, GOLD, 2.5)


def _trident(cr):
    """Nandi's trident (grip at 0, 0)."""
    band(cr, [(0, 400), (0, -400)], 14, BROWN, spacing=20, hole_r=2.4)
    _shape(cr, [(-10, -400), (10, -400), (8, -520), (0, -560), (-8, -520)], GOLD, 4, smooth=False)
    for s in (-1, 1):
        _shape(cr, [(0, -400), (s * 60, -420), (s * 84, -480), (s * 76, -530), (s * 62, -470), (s * 40, -440),
                    (0, -430)], GOLD, 4, smooth=False)
    band(cr, [(-40, -404), (40, -404)], 14, GOLD, spacing=10, hole_r=2.0)
    _shape(cr, [(4, -380), (40, -360), (60, -300), (34, -320), (6, -350)], RED, 3, smooth=False)


def _staff(cr):
    band(cr, [(0, 430), (4, 0), (0, -470)], 16, BROWN, spacing=24, hole_r=2.6)
    for y in (-300, -60, 200):
        ink(cr, [(-10, y), (10, y - 6)], 4)
    cr.new_path()
    ell(cr, 0, -480, 20, 16)
    leather(cr, BROWN, 4)


def _rope(cr):
    """Rope coils round a body (centre at 0, 0), with a loose end."""
    for dy in (-70, -10, 50):
        for w, col in ((20, INK), (13, ROPE)):
            cr.new_path()
            ell(cr, 0, dy, 118, 26, -0.08)
            cr.set_source_rgb(*col)
            cr.set_line_width(w)
            cr.stroke()
        for k in range(14):
            a = 2 * math.pi * k / 14
            x, y = 118 * math.cos(a), dy + 26 * math.sin(a)
            ink(cr, [(x - 4, y - 5), (x + 4, y + 5)], 2.2)
    for w, col in ((20, INK), (13, ROPE)):
        cr.new_path()
        spath(cr, [(100, 50), (140, 100), (130, 170)], closed=False)
        cr.set_source_rgb(*col)
        cr.set_line_width(w)
        cr.stroke()


for _c, _n in ((GOLD, "rv_mari0"), (SAFFRON, "rv_mari1")):
    register(_n, (-38, -38, 38, 38), (lambda c: lambda cr: _marigold(cr, c))(_c))
register("rv_linga", (-180, -310, 275, 8), _linga)
register("rv_waveA", (-1050, -46, 1050, 56), lambda cr: _wave(cr, WATER))
register("rv_waveB", (-1050, -46, 1050, 56), lambda cr: _wave(cr, WATER2))
register("rv_drop", (-16, -28, 16, 20), _drop)
register("rv_map", (-530, -370, 530, 360), _map)
register("rv_omap", (-480, -480, 480, 480), _omap)
register("rv_kailasa", (-710, -730, 710, 10), _kailasa)
register("rv_crown", (-42, -48, 42, 6), _crown_s)
register("rv_note", (-400, -275, 400, 280), _note)
register("rv_tally", (-410, -350, 410, 350), _tally)
register("rv_lanka", (-580, -670, 580, 10), _lanka)
register("rv_trident", (-100, -570, 100, 410), _trident)
register("rv_staff", (-30, -500, 30, 440), _staff)
register("rv_rope", (-150, -110, 160, 190), _rope)
