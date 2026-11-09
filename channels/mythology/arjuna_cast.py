"""The leather cast and props for the Arjuna reel (videos/arjuna.py), in the Togalu Gombeyaata style of the Jarasandha,
Kaikeyi, Lakshman Rekha, Mandhata and Jayadratha reels (puppet_cast, kaikeyi_cast, lrekha_cast, mandhata_cast,
jayadratha_cast): profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather
puppets, modelled on no actor and no film.

Cast (one look each, kept the same through the video):
  ARJUNA        jayadratha_cast.ARJUNA unchanged (warm skin, black moustache, gold kirita with a red flare, cream dhoti
                with a red border and sash, a quiver, the bow Gandiva), plus a sword (a curved talwar in a red-and-gold
                scabbard at his hip) and three more faces: fierce (the vow), ashamed (eyes cast down), proud (chin up,
                smiling); kneeling legs for the end.
  YUDHISHTHIRA  the eldest Pandava, a crowned king: a deeper wheat skin, a short dark beard and moustache, a tall gold
                crown with a blue flare and a dark-green flame halo (Arjuna has none), an indigo dhoti with a gold
                border and a saffron sash. Faces: calm, smiling, angry, hurt; seated legs (on the camp cot); white
                bandages for his wounds (chest wrap, arm wrap), only cloth, never blood.
  KRISHNA       puppet_cast.KRISHNA, as in the Jarasandha and Jayadratha reels: blue skin, peacock feather; calm.
  KARNA         the Kaurava champion: golden-tan skin, a saffron-and-gold sun-ray halo (the son of the Sun), big gold
                kundala earrings, a gold kirita with a saffron flare, a gold armour plate (kavacha) with a sun on the
                chest, a red dhoti with a gold border; a big dark-red bow. Faces: calm and laughing.
Props: the camp tent (a striped canopy with an open front, flaps tied back), the tent's inside wall, a camp cot, a
standing oil lamp, dice (square ivory faces with punched pips), a wax seal, a thought bubble, Karna's bow (strung and
unstrung), Yudhishthira's plain bow, the sword and its scabbard (empty / with the hilt showing). The palm-leaf book,
speech cloud, torn note, plaque, scale, sun and flames come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man().
"""
import math

import jayadratha_cast as J
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import puppet_cast as C
import ravana_cast as R
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BLUE, DGREEN, DRED, GOLD, INK, OCHRE, PALE, PARCH, RED, ROSE, SAFFRON, almond_eye, band,
                         dots_in, ell, holes_line, ink, leather, poly, punch, register, spath)

AR_SKIN = J.AR_SKIN                   # Arjuna
YU_SKIN = (0.90, 0.64, 0.42)          # Yudhishthira: a deeper wheat
YU_DHOTI = (0.36, 0.30, 0.74)         # indigo
KA_SKIN = (0.97, 0.72, 0.40)          # Karna: golden tan
KA_DHOTI = (0.86, 0.16, 0.10)         # deep red
CLOTH = (1.0, 0.98, 0.94)             # bandage cloth
CLOTH2 = (0.84, 0.80, 0.74)
STEEL = J.STEEL
STEEL2 = J.STEEL2
WOOD = K.WOOD
TENT_A = (0.96, 0.62, 0.20)           # the tent's saffron stripes
TENT_B = (1.0, 0.93, 0.76)            # cream stripes
TENT_C = (0.74, 0.16, 0.10)           # red border
IVORY = (1.0, 0.95, 0.82)
WAX = (0.78, 0.10, 0.08)

SEAT_H = 268.0                        # seated: hip above the floor (design units; mandhata_cast.seat_legs)
COT_TOP = 206.0                       # the cot's seat above the floor
SWORD_L = 560.0                       # grip to blade tip (design units)

# ------------------------------------------------------------------ faces


def face(cr, o, mood="calm"):
    """puppet_cast.man_head's bare head ("tiara": hair, face, ear, eye, brow, tilak, moustache, earring) drawn the same
    way, with a mood: calm | smile | laugh | angry | scold | shame | hurt | proud. o: skin, hair, moustache,
    beard (a short dark beard), earring ('ring' = big kundala rings)."""
    skin = o["skin"]
    if o.get("hair", True):
        hp = [(-30, -176), (-62, -146), (-84, -80), (-88, 0), (-74, 64), (-50, 84), (-40, 30), (-36, -40), (-20, -90)]
        _shape(cr, hp, HAIR, 5)
        for k in range(4):
            holes_line(cr, [(-46 - 8 * k, -140 + 10 * k), (-70 - 4 * k, -40), (-62 - 2 * k, 50)], 16, 2.4)
    fc = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152), (60, -128),
          (66, -116), (92, -92), (68, -82), (70, -72), (62, -64), (66, -56), (56, -44), (52, -30), (34, -22), (26, 6)]
    if mood in ("laugh", "scold"):                     # the jaw drops open
        drop = 26 if mood == "laugh" else 14
        fc = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
              (60, -128), (66, -116), (92, -92), (72, -84), (48, -74), (70, -52 + drop - 26), (66, -40 + drop - 26),
              (56, -28 + drop - 26), (40, -16 + drop - 26), (26, 6)]
    _shape(cr, fc, skin, 6)
    cr.new_path()
    ell(cr, -14, -108, 13, 21)
    leather(cr, skin, 4)
    if o.get("beard"):                                 # a short, neat dark beard along the jaw
        bp = [(58, -46), (62, -26), (52, 4), (34, 22), (12, 18), (-4, -6), (-14, -40), (6, -30), (28, -34), (44, -48)]
        _shape(cr, bp, HAIR, 4)
        holes_line(cr, [(46, -30), (30, 0), (8, 6)], 13, 2.2)
    # mouth
    if mood in ("laugh", "scold"):
        d = 26 if mood == "laugh" else 14
        _shape(cr, [(74, -84), (48, -74), (70, -52 + d - 26)], (0.42, 0.05, 0.06), 4, smooth=False)
        _shape(cr, [(72, -83), (52, -76), (56, -70), (72, -78)], PALE, 2.5, smooth=False)
        if mood == "laugh":
            _shape(cr, [(64, -58), (58, -64), (52, -68), (66, -54)], ROSE, 2, smooth=False)
    elif mood in ("smile", "proud"):
        ink(cr, [(56, -70), (62, -64), (70, -68)], 3.5)
    elif mood == "angry":
        ink(cr, [(70, -66), (60, -70)], 4)
    else:
        ink(cr, [(68, -70), (60, -68)], 3)
    # eye and brow
    if mood == "laugh":
        ink(cr, [(16, -112), (34, -128), (54, -114)], 7)               # squeezed shut with laughing
        ink(cr, [(20, -104), (34, -98), (48, -104)], 3)
        ink(cr, [(12, -150), (34, -160), (58, -150)], 5)
    elif mood in ("smile", "proud"):
        ink(cr, [(16, -112), (34, -126), (52, -114)], 6)               # a happy, curved eye
        ink(cr, [(12, -142), (34, -154), (56, -144)], 5)
        if mood == "proud":
            ink(cr, [(8, -110), (-2, -118)], 3)
    elif mood in ("angry", "scold"):
        almond_eye(cr, 34, -116, 40, 14, col=PALE)
        ink(cr, [(6, -152), (34, -142), (62, -124)], 9)                # brow pulled down
        ink(cr, [(2, -146), (-4, -130)], 3)
    elif mood == "shame":
        ink(cr, [(16, -116), (34, -106), (52, -114)], 6)               # eyes cast down, shut
        for k in range(3):
            ink(cr, [(22 + 12 * k, -108), (20 + 12 * k, -98)], 2.5)
        ink(cr, [(12, -132), (34, -140), (58, -154)], 5)               # sad brow, raised at the front
    elif mood == "hurt":
        almond_eye(cr, 34, -116, 38, 12, col=PALE)
        ink(cr, [(14, -124), (34, -130), (54, -124)], 5)               # a heavy, tired lid
        ink(cr, [(12, -138), (34, -144), (58, -156)], 5)
        ink(cr, [(40, -96), (52, -88)], 2.5)
    else:
        almond_eye(cr, 34, -118, 38, 13, col=PALE)
        ink(cr, [(14, -136), (34, -144), (56, -136)], 4.5)
    if o.get("tilak", True):
        ink(cr, [(52, -150), (54, -170)], 5, col=RED)
    if o.get("moustache"):
        dy = -6 if mood == "laugh" else 0
        m = [(64, -74 + dy), (44, -82 + dy), (26, -86 + dy), (14, -102 + dy), (24, -94 + dy), (44, -86 + dy),
             (66, -79 + dy)]
        _shape(cr, m, HAIR, 3)
    if o.get("earring") == "ring":                     # Karna's kundalas: big gold rings with a red stone
        for r, col in ((30, GOLD), (19, (1.0, 0.6, 0.2))):
            cr.new_path()
            cr.arc(-14, -62, r, 0, 2 * math.pi)
            leather(cr, col, 4)
        _jewel(cr, -14, -62, 9, RED)
        punch(cr, [(-14 + 24 * math.cos(a), -62 + 24 * math.sin(a)) for a in (0.4, 1.6, 2.8, 4.0, 5.2)], 2.6)
    elif o.get("earring", True):
        _jewel(cr, -12, -72, 16, GOLD)
        poly(cr, [(-20, -58), (-12, -36), (-4, -58)])
        leather(cr, RED, 3)


# ------------------------------------------------------------------ Arjuna: more faces, sword, kneeling legs


_AR_O = dict(skin=AR_SKIN, hair=True, moustache=True, tilak=True)


def arjuna_head(cr, mood):
    face(cr, _AR_O, mood)
    R.kirita(cr, GOLD, None, tall=1.08, flare=RED)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.08, 9, BLUE)


for _m in ("angry", "scold", "shame", "proud"):
    register(f"ar_arjuna_head_{_m}", (-200, -440, 120, 110), (lambda m: lambda cr: arjuna_head(cr, m))(_m))
register("ar_arjuna_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, AR_SKIN, PALE, RED, 1.05))


def _sword(cr):
    """A curved talwar (grip at 0, 0, the blade up to y = -SWORD_L): a steel blade with a fuller, a gold cross-guard
    and knuckle bow, a red grip, a disc pommel."""
    blade = [(-14, -40), (-16, -200), (-10, -360), (6, -480), (34, -556), (40, -566), (26, -520), (14, -440),
             (14, -300), (16, -160), (14, -40)]
    _shape(cr, blade, STEEL2, 5)
    ink(cr, [(-2, -60), (-2, -220), (6, -380), (20, -480)], 3, col=STEEL)
    holes_line(cr, [(-6, -90), (-6, -260)], 30, 2.2, smooth=False)
    _shape(cr, [(-64, -46), (60, -46), (66, -30), (-70, -30)], GOLD, 4, smooth=False)       # cross-guard
    for sx in (-1, 1):
        _jewel(cr, sx * 60, -38, 7, RED)
    ink(cr, [(52, -36), (64, 10), (40, 52), (12, 60)], 9, col=INK)                         # knuckle bow
    ink(cr, [(52, -36), (64, 10), (40, 52), (12, 60)], 5, col=GOLD)
    _shape(cr, [(-14, -32), (14, -32), (16, 44), (-16, 44)], RED, 4, smooth=False)           # grip
    for y in (-14, 6, 26):
        ink(cr, [(-14, y), (14, y + 8)], 2.5, smooth=False)
    cr.new_path()
    ell(cr, 0, 60, 30, 14)
    leather(cr, GOLD, 4)
    _jewel(cr, 0, 60, 7, RED)


def _scabbard(cr, hilt):
    """The scabbard on Arjuna's hip (body coordinates, hip at 0, 0): it hangs from the sash down and back behind the
    legs; hilt = the sword still in it (its gold hilt showing at the mouth, pointing forward)."""
    sc = [(40, -30), (-6, 30), (-80, 150), (-170, 280), (-220, 352), (-246, 360), (-236, 330), (-196, 262),
          (-110, 128), (-36, 8), (14, -44)]
    _shape(cr, sc, DRED, 5, holes=(9, 12, 2.2))
    for (x, y) in ((16, -20), (-120, 168)):                                                 # gold lockets
        cr.save()
        cr.translate(x, y)
        cr.rotate(-0.95)
        _shape(cr, [(-28, -12), (28, -12), (30, 12), (-30, 12)], GOLD, 3.5, smooth=False)
        cr.restore()
    _shape(cr, [(-226, 340), (-252, 372), (-238, 340)], GOLD, 3, smooth=False)               # chape
    if hilt:                                            # the sword's hilt out of the mouth, along the scabbard
        cr.save()
        cr.translate(48, -68)
        cr.rotate(-2.544)
        _shape(cr, [(-64, -46), (60, -46), (66, -30), (-70, -30)], GOLD, 4, smooth=False)
        ink(cr, [(52, -36), (64, 10), (40, 52), (12, 60)], 9, col=INK)
        ink(cr, [(52, -36), (64, 10), (40, 52), (12, 60)], 5, col=GOLD)
        _shape(cr, [(-14, -32), (14, -32), (16, 44), (-16, 44)], RED, 4, smooth=False)
        cr.new_path()
        ell(cr, 0, 60, 30, 14)
        leather(cr, GOLD, 4)
        _jewel(cr, 0, 60, 7, RED)
        cr.restore()


register("ar_sword", (-80, -580, 80, 80), _sword)
register("ar_scabbard", (-270, -110, 80, 390), lambda cr: _scabbard(cr, False))
register("ar_scabbard_full", (-270, -170, 140, 390), lambda cr: _scabbard(cr, True))

# ------------------------------------------------------------------ Yudhishthira


_YU_O = dict(skin=YU_SKIN, hair=True, moustache=True, beard=True, tilak=True)


def yudh_head(cr, mood="calm"):
    """The eldest: a dark-green flame halo, a tall gold crown with a blue flare, a short dark beard."""
    K._halo(cr, DGREEN)
    face(cr, _YU_O, mood)
    R.kirita(cr, GOLD, None, tall=1.32, flare=BLUE)
    h = lambda y: -150 + (y + 150) * 1.32
    for sx in (-1, 1):                                                          # side peaks
        _shape(cr, [(sx * 30, -170), (sx * 64, h(-240)), (sx * 50, h(-286)), (sx * 38, h(-238)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 48, h(-252), 7, BLUE)
    _jewel(cr, 2, h(-292), 10, (0.16, 0.66, 0.40))


YUDH = man("ar_yudh", skin=YU_SKIN, bulk=1.08, dhoti=YU_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
           crown="tiara", halo=False, moustache=True, thread=True, hands=("open", "open"))
for _m in ("calm", "smile", "angry", "hurt"):
    register("ar_yudh_head" + ("" if _m == "calm" else "_" + _m), (-230, -520, 130, 110),
             (lambda m: lambda cr: yudh_head(cr, m))(_m))
register("ar_yudh_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, YU_SKIN, YU_DHOTI, GOLD, 1.08))


def _band_chest(cr):
    """A white cloth bandage wrapped across his chest (body coordinates of a bulk-1.08 man), knotted at the shoulder."""
    b = 1.08
    for dy in (0, 44):
        pts = [(-58 * b, -252 + dy), (-10, -214 + dy), (40 * b, -170 + dy), (86 * b, -140 + dy)]
        band(cr, pts, 30, CLOTH, holes=False, lw=4)
        ink(cr, [(-50 * b, -246 + dy), (40 * b, -168 + dy)], 2, col=CLOTH2)
    _shape(cr, [(-62, -262), (-86, -244), (-80, -218), (-56, -232)], CLOTH, 3.5)            # the knot
    _shape(cr, [(-80, -236), (-112, -196), (-96, -190), (-72, -226)], CLOTH, 3)
    _shape(cr, [(-76, -228), (-100, -170), (-86, -168), (-66, -222)], CLOTH, 3)


def _band_arm(cr):
    """A white bandage round an upper arm (upper-arm coordinates)."""
    for y in (78, 102, 124):
        band(cr, [(-31, y - 4), (31, y + 4)], 20, CLOTH, holes=False, lw=3.5)
    _shape(cr, [(24, 92), (52, 110), (44, 124), (22, 108)], CLOTH, 3)


register("ar_band_chest", (-130, -290, 110, -70), _band_chest)
register("ar_band_arm", (-50, 50, 70, 150), _band_arm)


def _ybow(cr):
    """Yudhishthira's plain bow (grip at 0, 0, the string at x = -60): ochre limbs, gold tips, a blue grip."""
    cr.new_path()
    cr.move_to(-60, -280)
    cr.curve_to(40, -170, 40, 170, -60, 280)
    cr.set_line_cap(1)
    cr.set_source_rgb(*INK)
    cr.set_line_width(24)
    cr.stroke_preserve()
    cr.set_source_rgb(*OCHRE)
    cr.set_line_width(14)
    cr.stroke()
    holes_line(cr, [(-46, -240), (0, -140), (14, -60)], 24, 2.4)
    holes_line(cr, [(-46, 240), (0, 140), (14, 60)], 24, 2.4)
    for s in (-1, 1):
        cr.new_path()
        cr.arc(-60, s * 282, 10, 0, 2 * math.pi)
        leather(cr, GOLD, 3)
    band(cr, [(14, -36), (14, 36)], 22, BLUE, spacing=10, hole_r=1.8)
    ink(cr, [(-60, -280), (-60, 280)], 2.5, smooth=False)


register("ar_ybow", (-80, -300, 40, 300), _ybow)

# ------------------------------------------------------------------ Karna


_KA_O = dict(skin=KA_SKIN, hair=True, moustache=True, tilak=True, earring="ring")


def karna_head(cr, mood="calm"):
    """Karna: a sun-ray halo (saffron and gold), big gold kundala rings, a gold kirita with a saffron flare."""
    M._ray_halo(cr, -36, -236, 132, 206, 16, (SAFFRON, GOLD))
    face(cr, _KA_O, mood)
    R.kirita(cr, GOLD, None, tall=1.12, flare=SAFFRON)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.12, 10, RED)


_KA = dict(skin=KA_SKIN, bulk=1.18, dhoti=KA_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD)
KARNA = man("ar_karna", crown="tiara", halo=False, moustache=True, hands=("fist", "fist"), **_KA)


def karna_body(cr):
    """His body with the golden armour (kavacha) he was born with: gold scales over the chest, a sun on it."""
    C.man_body(cr, _KA)
    b = _KA["bulk"]
    plate = [(-50 * b, -70), (-58 * b, -170), (-50 * b, -240), (-24, -278), (20, -284), (54 * b, -254), (80 * b, -206),
             (76 * b, -160), (60 * b, -110), (52 * b, -70)]
    _shape(cr, plate, GOLD, 5)
    for row in range(6):                                                     # rows of scales
        y = -250 + 30 * row
        for k in range(6):
            x = -44 * b + 22 * k + (11 if row % 2 else 0)
            if x > 70 * b - 8 * row:
                continue
            ink(cr, [(x - 9, y), (x, y + 10), (x + 9, y)], 2.4, col=(0.70, 0.46, 0.10))
    pts = []                                                                 # the sun on his chest
    for i in range(24):
        a = 2 * math.pi * i / 24
        r = 46 if i % 2 == 0 else 30
        pts.append((22 + r * math.cos(a), -176 + r * math.sin(a)))
    _shape(cr, pts, SAFFRON, 3.5, smooth=False)
    cr.new_path()
    cr.arc(22, -176, 24, 0, 2 * math.pi)
    leather(cr, RED, 3.5)
    _flower(cr, 22, -176, 13, GOLD, 8)
    band(cr, [(-52 * b, -74), (54 * b, -74)], 14, RED, spacing=11, hole_r=2.2)


register("ar_karna_body", (-200, -330, 140, 300), karna_body)
register("ar_karna_head", (-260, -470, 190, 110), lambda cr: karna_head(cr, "calm"))
register("ar_karna_head_laugh", (-260, -470, 190, 110), lambda cr: karna_head(cr, "laugh"))


def _kbow(cr, string=True):
    """Karna's great bow (grip at 0, 0; the belly bulges to +x, the string at x = -100): dark-red limbs with gold
    bands and sun discs, gold tips."""
    cr.new_path()
    cr.move_to(-100, -380)
    cr.curve_to(46, -250, 46, 250, -100, 380)
    cr.set_line_cap(1)
    cr.set_source_rgb(*INK)
    cr.set_line_width(32)
    cr.stroke_preserve()
    cr.set_source_rgb(*DRED)
    cr.set_line_width(21)
    cr.stroke()
    for s in (-1, 1):
        for y in (110, 200, 290):
            u = y / 380
            x = -100 + 146 * 0.75 * (1 - u * u) * 1.0 - 4
            band(cr, [(x - 14, s * y), (x + 14, s * (y + 6))], 10, GOLD, holes=False)
        for w, col in ((16, INK), (8, GOLD)):
            cr.new_path()
            spath(cr, [(-100, s * 378), (-82, s * 418), (-48, s * 428)], closed=False)
            cr.set_source_rgb(*col)
            cr.set_line_width(w)
            cr.stroke()
        _flower(cr, -30, s * 150, 14, GOLD, 8)
    band(cr, [(10, -50), (10, 50)], 30, GOLD, spacing=10, hole_r=2.0)
    _jewel(cr, 12, 0, 9, RED)
    if string:
        ink(cr, [(-98, -378), (-98, 378)], 3.0, smooth=False)


register("ar_kbow", (-125, -445, 70, 445), lambda cr: _kbow(cr, True))
register("ar_kbow_bare", (-125, -445, 70, 445), lambda cr: _kbow(cr, False))

# ------------------------------------------------------------------ the camp: tent, inside wall, cot, lamp


def _stripes(cr, x0, x1, top, bottom, w=70):
    """Vertical saffron and cream stripes filling the current clip."""
    i = 0
    x = x0
    while x < x1:
        cr.new_path()
        poly(cr, [(x, top), (x + w, top), (x + w, bottom), (x, bottom)])
        cr.set_source_rgb(*(TENT_A if i % 2 == 0 else TENT_B))
        cr.fill()
        x += w
        i += 1


def _scallops(cr, x0, x1, y, w=64, depth=34, col=TENT_C):
    """A scalloped valance hanging from y."""
    pts = [(x0, y - 30)]
    n = int((x1 - x0) / w)
    for i in range(n + 1):
        x = x0 + i * w
        pts += [(x, y), (x + w / 2, y + depth)]
    pts += [(x1, y), (x1, y - 30)]
    _shape(cr, pts, col, 5, smooth=False)
    for i in range(n):
        punch(cr, [(x0 + i * w + w / 2, y + depth * 0.45)], 4.5)


def _tent(cr):
    """The camp tent (pivot at the bottom centre): a peaked striped canopy on poles, a red border, the back wall seen
    through the open front (the figures stand inside it), a pennant on top."""
    wall = [(-560, 0), (560, 0), (560, -640), (-560, -640)]
    cr.save()
    cr.new_path()
    poly(cr, wall)
    cr.clip()
    _stripes(cr, -560, 560, -660, 10, 80)
    cr.restore()
    cr.new_path()
    poly(cr, wall)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    dots_in(cr, lambda: poly(cr, [(-540, -40), (540, -40), (540, -600), (-540, -600)]), 34, 3.0, shape="d")
    band(cr, [(-560, -26), (560, -26)], 26, TENT_C, spacing=15)
    roof = [(-680, -600), (-420, -820), (0, -1010), (420, -820), (680, -600)]
    cr.new_path()
    poly(cr, roof)
    pl = leather(cr, TENT_A, 7, keep=True)
    cr.save()
    cr.new_path()
    poly(cr, roof)
    cr.clip()
    for k in range(-9, 10):                                                  # canopy seams
        ink(cr, [(0, -1010), (k * 80, -600)], 3, smooth=False, col=(0.72, 0.38, 0.10))
    cr.restore()
    holes_line(cr, [(-640, -630), (0, -985), (640, -630)], 22, 3.0, smooth=False)
    _scallops(cr, -690, 690, -606, 69)
    for x in (-560, 560):                                                    # corner poles
        _shape(cr, [(x - 16, 0), (x + 16, 0), (x + 13, -620), (x - 13, -620)], WOOD, 5, smooth=False)
    _shape(cr, [(-12, -1000), (12, -1000), (10, -1150), (-10, -1150)], WOOD, 4, smooth=False)   # the top pole
    _shape(cr, [(8, -1146), (150, -1112), (96, -1094), (150, -1072), (8, -1050)], SAFFRON, 4, smooth=False,
           holes=(8, 12, 2.2))
    cr.new_path()
    cr.arc(0, -1160, 14, 0, 2 * math.pi)
    leather(cr, GOLD, 3.5)


def _tent_front(cr):
    """The tent's front flaps, tied back to the sides (pivot at the bottom centre); drawn in front of the figures."""
    for sx in (-1, 1):
        flap = [(sx * 566, -640), (sx * 380, -640), (sx * 440, -420), (sx * 520, -300), (sx * 470, -150),
                (sx * 500, 0), (sx * 566, 0)]
        _shape(cr, flap, TENT_B, 6, holes=(12, 16, 2.8))
        for k in range(3):
            ink(cr, [(sx * (420 + 40 * k), -620), (sx * (480 + 20 * k), -340)], 3, col=(0.80, 0.62, 0.36))
        band(cr, [(sx * 450, -330), (sx * 520, -310), (sx * 580, -320)], 18, TENT_C, spacing=11)   # the tie
        _jewel(cr, sx * 520, -316, 10, GOLD)
    _scallops(cr, -580, 580, -648, 58, 40)


def _wall(cr):
    """Inside the tent: the striped back wall (pivot at the bottom centre, 1400 wide, 900 high), a scalloped red
    valance at the top, two poles."""
    wall = [(-700, 0), (700, 0), (700, -900), (-700, -900)]
    cr.save()
    cr.new_path()
    poly(cr, wall)
    cr.clip()
    _stripes(cr, -700, 700, -920, 10, 90)
    cr.restore()
    cr.new_path()
    poly(cr, wall)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    dots_in(cr, lambda: poly(cr, [(-690, -60), (690, -60), (690, -820), (-690, -820)]), 40, 3.2, shape="d")
    band(cr, [(-700, -30), (700, -30)], 30, TENT_C, spacing=16)
    _scallops(cr, -710, 710, -884, 71, 44)
    for x in (-520, 520):
        _shape(cr, [(x - 18, 0), (x + 18, 0), (x + 14, -900), (x - 14, -900)], WOOD, 5, smooth=False)
        holes_line(cr, [(x, -40), (x, -860)], 40, 3, smooth=False)


def _cot(cr):
    """A low camp cot (pivot at the bottom centre; the seat top at y = -COT_TOP): turned wooden legs, a woven seat,
    a red cushion with a gold border."""
    for x in (-250, 230):
        _shape(cr, [(x - 18, 0), (x + 18, 0), (x + 14, -60), (x + 22, -90), (x + 14, -130), (x + 14, -170),
                    (x - 14, -170), (x - 14, -130), (x - 22, -90), (x - 14, -60)], WOOD, 4, smooth=False)
    frame = [(-280, -166), (270, -166), (270, -196), (-280, -196)]
    _shape(cr, frame, WOOD, 5, smooth=False, holes=(8, 13, 2.2))
    cush = [(-266, -192), (256, -192), (262, -214), (240, -226), (-246, -226), (-272, -214)]
    _shape(cr, cush, RED, 5)
    band(cr, [(-262, -198), (258, -198)], 8, GOLD, holes=False)
    dots_in(cr, lambda: poly(cr, [(-240, -220), (230, -220), (230, -202), (-240, -202)]), 18, 2.4)


def _diya(cr):
    """A standing brass oil lamp (pivot at the bottom centre; the wick at y = -420)."""
    _shape(cr, [(-70, 0), (70, 0), (50, -30), (14, -50), (14, -330), (40, -350), (-40, -350), (-14, -330),
                (-14, -50), (-50, -30)], GOLD, 5, smooth=False, holes=(7, 11, 2.2))
    for y in (-150, -250):
        cr.new_path()
        ell(cr, 0, y, 30, 14)
        leather(cr, GOLD, 4)
    _shape(cr, [(-70, -350), (70, -350), (60, -380), (30, -396), (-30, -396), (-60, -380)], GOLD, 5)
    _shape(cr, [(46, -390), (86, -404), (60, -378)], GOLD, 3.5, smooth=False)


register("ar_tent", (-700, -1180, 700, 10), _tent)
register("ar_tent_front", (-600, -700, 600, 10), _tent_front)
register("ar_wall", (-720, -940, 720, 10), _wall)
register("ar_cot", (-300, -240, 290, 10), _cot)
register("ar_diya", (-80, -420, 100, 10), _diya)

# ------------------------------------------------------------------ dice, seal, thought bubble


def _die(cr, n):
    """One face of a die, flat (centre pivot): an ivory square with rounded corners, the pips punched through (the
    lamp shines through them) with ink rings."""
    r = 66
    pts = []
    for cx, cy, a0 in ((r, -r, -math.pi / 2), (r, r, 0), (-r, r, math.pi / 2), (-r, -r, math.pi)):
        for k in range(5):
            a = a0 + (math.pi / 2) * k / 4
            pts.append((cx * 0.8 + 14 * math.cos(a), cy * 0.8 + 14 * math.sin(a)))
    _shape(cr, pts, IVORY, 6, smooth=False)
    ink(cr, [(-60, -54), (54, -60)], 2, smooth=False, col=(0.86, 0.76, 0.56))
    g = 30
    spots = {1: [(0, 0)], 2: [(-g, -g), (g, g)], 3: [(-g, -g), (0, 0), (g, g)], 4: [(-g, -g), (g, -g), (-g, g), (g, g)],
             5: [(-g, -g), (g, -g), (0, 0), (-g, g), (g, g)],
             6: [(-g, -g), (g, -g), (-g, 0), (g, 0), (-g, g), (g, g)]}[n]
    for x, y in spots:
        cr.new_path()
        cr.arc(x, y, 14, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(x, y)], 9)


def _seal(cr):
    """A red wax seal (centre pivot): a wavy disc, a lotus pressed into it, two ribbon tails below."""
    for sx in (-1, 1):
        _shape(cr, [(sx * 10, 30), (sx * 40, 150), (sx * 24, 140), (sx * 14, 160), (sx * -4, 40)], DRED, 4,
               smooth=False)
    pts = []
    for i in range(36):
        a = 2 * math.pi * i / 36
        r = 92 + 7 * math.sin(7 * a + 0.4) + (4 if i % 2 else 0)
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, WAX, 6)
    cr.new_path()
    cr.arc(0, 0, 64, 0, 2 * math.pi)
    cr.set_source_rgb(0.58, 0.06, 0.05)
    cr.set_line_width(5)
    cr.stroke()
    for i in range(8):                                                       # the pressed lotus
        a = 2 * math.pi * i / 8
        cr.save()
        cr.translate(0, 0)
        cr.rotate(a)
        _shape(cr, [(0, -8), (12, -26), (0, -50), (-12, -26)], (0.94, 0.30, 0.22), 2.5)
        cr.restore()
    punch(cr, [(0, 0)], 6)


def _think(cr):
    """A thought bubble (centre pivot), bumpy parchment, a trail of small puffs to the lower right (the thinker)."""
    for i, (x, y, r) in enumerate(((300, 250, 30), (356, 312, 20), (396, 360, 13))):
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        leather(cr, PARCH, 5)
    rx, ry = 290, 200
    bumps = [(rx * math.cos(2 * math.pi * i / 20), ry * math.sin(2 * math.pi * i / 20)) for i in range(20)]
    for col, lw in ((INK, 12), (PARCH, 0)):
        for x, y in bumps:
            cr.new_path()
            cr.arc(x, y, 74, 0, 2 * math.pi)
            cr.set_source_rgb(*col)
            if lw:
                cr.set_line_width(lw)
                cr.stroke()
            else:
                cr.fill()
    cr.new_path()
    ell(cr, 0, 0, rx + 8, ry + 8)
    cr.fill()
    for i in range(20):
        a = 2 * math.pi * (i + 0.5) / 20
        punch(cr, [((rx + 44) * math.cos(a), (ry + 44) * math.sin(a))], 3.4)


for _n in (2, 3, 5, 6):
    register(f"ar_die{_n}", (-100, -100, 100, 100), (lambda n: lambda cr: _die(cr, n))(_n))
register("ar_seal", (-110, -110, 110, 170), _seal)
register("ar_think", (-390, -300, 420, 390), _think)
