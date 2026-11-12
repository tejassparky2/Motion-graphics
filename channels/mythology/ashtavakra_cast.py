"""The leather cast and props for the Ashtavakra reel (videos/ashtavakra.py), in the Togalu Gombeyaata style of the
Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha, Arjuna, Ruru, Dharmavyadha and Shani reels: profile figures
with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no
film. Every sprite name starts with "av_" (the other builders' casts load in the same process).

Cast (one look each, kept the same through the video; everyone with dignity):
  KAHODA      the Vedic teacher: warm brown skin, a long black beard and moustache, a hair cap and a top-knot, three ash
              lines and a red dot, a white dhoti with a saffron border, a saffron shawl across the chest, a rudraksha
              mala and the sacred thread. Faces: calm, read (eyes shut, reciting), shock, shame (eyes down, a red flush
              on the cheek), angry, curse (angry, the jaw open), bow (eyes down, calm), smile. Sits cross-legged
              (av_kahoda_body_sit + av_kahoda_seat) with the palm leaf (dharmavyadha_cast dv_pleaf).
  SUJATA      his wife: fair warm skin, a leaf-green sari with a gold border, a saffron pallu, a red blouse, jasmine
              round her bun, a small gold maang-tikka, a bindi, a nose stud, gold earrings, a black-bead mangalsutra.
              Seated on a low carved stool (av_peeta): av_suj_body_sit (expecting: a gently rounded belly under the
              sari, its centre at the rig point "belly") and av_suj_body_sit0 (after the birth). Faces: open, smile,
              shock, shut.
  DISCIPLES   two young Brahmin students (av_dis1, av_dis2): top-knots, white dhotis, saffron or green sashes, the
              sacred thread. Faces: calm, shock (a gasp), smile. Seated cross-legged, or standing (as silhouettes, the
              Brahmins rising from the water).
  ASHTAVAKRA  the boy at twelve: warm skin, a big head, a hair cap with a top-knot tied in rudraksha, a white
              sandal-paste tilak, a cream dhoti with a saffron border and a saffron sash, the sacred thread. Two rigs
              on the same parts: BOY_BENT (his back rounded into a hump, the head carried forward but the chin up, one
              knee bent and its foot turned, the other leg bowed, one wrist turned in: crooked, never mocked) and BOY
              (straight, after the river). Faces (bright and confident): calm (a small smile), smile, speak, firm,
              shut, wonder. His bamboo staff: av_staff (pivot at its foot).
  BABY        the unborn child in the womb window: av_fetus (curled, eyes shut) / av_fetus_talk (eye open, mouth open),
              its pointing arm av_fetus_arm (pivot at the shoulder, FETUS_SHOULDER); the newborn wrapped in a cloth:
              av_swaddle.
  JANAKA      the philosopher-king: warm skin, a long white beard, a gold kirita with a green flare before a gold flame
              halo, a maroon dhoti with a gold border, a green sash. Faces: calm, smile, wonder. Seated on a throne
              (av_janaka_body_sit + av_janaka_seat; mandhata_cast md_throne, its open back keeps him clear).
  VANDIN      the court scholar, tall and proud: a tall gold-and-red turban with a jewel and a plume, a curled
              moustache, a short pointed beard, rich robes (deep violet dhoti, a maroon shawl with gold, gold beads).
              Faces: calm, smirk (half-shut eye, raised brow, a sly smile), speak, shock.
  GATEKEEPER  jayadratha_cast's soldier with his spear (jd_soldier, jd_spear).
Props and sets: av_peeta (a low carved stool), av_staff, av_lamp (a small clay oil lamp on a stand), av_rwaveA/B (the
river Samanga's water strips, a clear green-blue), av_altar_w (a small fire altar seen under water). The court is
shani_cast's sg_hall with md_throne, the gate six_cast_a's sx_door_frame, the lake ravana_cast's rv_waveA/B, the cradle
shani_cast's sg_cradle; the palm-leaf book, plaques, speech cloud, stars and moon come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast as A
import dharmavyadha_cast as DV
import jayadratha_cast as J  # noqa: F401  (registers the soldier and his spear)
import kaikeyi_cast as K  # noqa: F401  (registers the throne, plaque)
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
import shani_cast as S  # noqa: F401  (registers the court hall and the cradle)
import six_cast_a as SA  # noqa: F401  (registers the door frame)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman, woman_body
from puppet_core import (BROWN, DGREEN, GOLD, GREEN, INK, PALE, RED, SAFFRON, Rig, almond_eye, band, dots_in, ell,
                         holes_line, ink, leather, punch, register, rivet, spath)

ASHW = (1.0, 0.97, 0.90)              # ash lines, sandal paste
KH_SKIN = (0.88, 0.60, 0.38)          # Kahoda
KH_CLOTH = (0.98, 0.88, 0.64)         # unbleached cotton
KH_CLOTH2 = (1.0, 0.95, 0.80)
D_CLOTH = (1.0, 0.92, 0.72)           # the disciples' dhotis
D_CLOTH2 = (1.0, 0.84, 0.46)
KH_SHAWL = (0.98, 0.56, 0.14)
FLUSH = (0.96, 0.36, 0.30)
SJ_SKIN = (0.99, 0.79, 0.60)          # Sujata
SJ_SARI = (0.20, 0.58, 0.38)          # leaf green
SJ_PALLU = (0.99, 0.60, 0.16)         # saffron
SJ_CHOLI = (0.86, 0.20, 0.16)
D1_SKIN = (0.97, 0.72, 0.48)          # the disciples
D2_SKIN = (0.80, 0.54, 0.34)
AV_SKIN = (0.98, 0.75, 0.50)          # Ashtavakra
AV_CLOTH = (1.0, 0.93, 0.78)
AV_SASH = (0.98, 0.48, 0.10)
BABY = M.BABY_SKIN                    # the unborn child, the newborn
CHEEK = (1.0, 0.62, 0.52)
JN_SKIN = (0.95, 0.70, 0.46)          # Janaka
JN_DHOTI = (0.62, 0.12, 0.22)
JN_SASH = (0.20, 0.56, 0.32)
BEARD = (0.94, 0.93, 0.90)
VD_SKIN = (0.84, 0.58, 0.40)          # Vandin
VD_DHOTI = (0.34, 0.16, 0.46)
VD_ROBE = (0.62, 0.10, 0.28)
VD_TURBAN = (0.92, 0.20, 0.14)
BAMBOO = (0.90, 0.74, 0.40)
WOOD = (0.62, 0.38, 0.18)
CLAY = (0.80, 0.46, 0.24)
RIVER = (0.42, 0.80, 0.84)            # the Samanga
RIVER2 = (0.26, 0.62, 0.74)

BEND = 0.42                           # how far the boy's back is rounded (radians at the shoulders)
BOY_BULK = 0.84
FETUS_SHOULDER = (40.0, -70.0)        # where the unborn child's pointing arm joins (fetus units)
SUJ_BELLY = (84.0, -104.0)            # the centre of Sujata's rounded belly (body units)
PEETA_TOP = -208.0                    # the stool's seat above the ground (stool units = DV.BENCH_H - 60)


def _cover(cr, col, x, y, rx, ry):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    cr.set_source_rgb(*col)
    cr.fill()


def _ash(cr, x0=8, x1=48, y0=-176):
    for k in range(3):
        ink(cr, [(x0, y0 + 9 * k), (x1, y0 - 2 + 9 * k)], 3.2, col=ASHW)
    cr.new_path()
    cr.arc((x0 + x1) / 2, y0 + 30, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


def _cap_knot(cr, col=HAIR, beads=True):
    """A hair cap and a top-knot (a Brahmin's shikha), tied with rudraksha."""
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -186), (24, -188), (-8, -182),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, col, 4)
    holes_line(cr, [(-50, -130), (-40, -176), (0, -200)], 15, 2.4)
    cr.new_path()
    ell(cr, -14, -230, 38, 28, -0.15)
    leather(cr, col, 4)
    holes_line(cr, [(-42, -232), (-14, -248), (14, -234)], 11, 2.2)
    if beads:
        for i in range(6):
            cr.new_path()
            cr.arc(-42 + 12 * i, -206 + 2 * math.sin(i * 1.7), 5.5, 0, 2 * math.pi)
            leather(cr, BROWN, 2)


def _o_mouth(cr, skin, x=64, y=-68, rx=8, ry=11):
    _cover(cr, skin, 63, -70, 9, 6)
    cr.new_path()
    ell(cr, x, y, rx, ry)
    leather(cr, (0.36, 0.05, 0.06), 2.5)


# ------------------------------------------------------------------ Kahoda


_KH_O = dict(skin=KH_SKIN, hair=False, moustache=True, tilak=False, earring=False)
KH_MOODS = ("calm", "read", "shock", "shame", "angry", "curse", "bow", "smile")


def kahoda_head(cr, mood="calm"):
    """Kahoda: a long black beard, a hair cap and a top-knot, three ash lines and a red dot; mood as KH_MOODS."""
    base = {"read": "sleep", "curse": "scold", "bow": "shame"}.get(mood, mood)
    RU.rface(cr, _KH_O, base)
    if mood == "read":                                                           # reciting: the lips apart
        cr.new_path()
        ell(cr, 64, -70, 5, 5)
        leather(cr, (0.40, 0.08, 0.06), 2)
    drop = 14 if mood == "curse" else (10 if mood == "shock" else 0)
    beard = [(60, -50 + drop), (66, -30 + drop), (60, 10 + drop), (44, 60 + drop), (24, 110 + drop), (14, 60),
             (0, 14), (-8, -34), (14, -40), (36, -52 + drop * 0.5)]
    _shape(cr, beard, HAIR, 4)
    holes_line(cr, [(46, -30 + drop), (36, 20 + drop), (26, 76 + drop)], 14, 2.2)
    if mood == "shame":                                                          # the embarrassed flush
        cr.new_path()
        ell(cr, 22, -88, 26, 15, -0.2)
        cr.set_source_rgb(*FLUSH)
        cr.fill()
        for k in range(3):
            ink(cr, [(8 + 12 * k, -96), (14 + 12 * k, -80)], 2.6, col=(0.70, 0.12, 0.10))
    _cap_knot(cr)
    _ash(cr)


_KH = dict(skin=KH_SKIN, bulk=0.98, dhoti=KH_CLOTH, border=SAFFRON, pleat=KH_CLOTH2, sash=SAFFRON, neck=BROWN,
           robe=KH_SHAWL, beads=True, thread=True)
KAHODA = man("av_kahoda", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_KH)
for _m in KH_MOODS:
    register("av_kahoda_head" + ("" if _m == "calm" else "_" + _m), (-150, -290, 120, 160),
             (lambda m: lambda cr: kahoda_head(cr, m))(_m))
register("av_kahoda_body_sit", (-200, -330, 140, 80), DV._sit_body(_KH))
register("av_kahoda_seat", (-110, -60, 280, 110), lambda cr: DV._cross_seat(cr, KH_CLOTH, SAFFRON, KH_SKIN))


# ------------------------------------------------------------------ Sujata


SJ_MOODS = ("open", "smile", "shock", "shut")


def suj_head(cr, mood="open"):
    """Sujata: jasmine round her bun, a small gold maang-tikka, a bindi, a nose stud, gold earrings."""
    S._face_w(cr, SJ_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(11):                                                          # jasmine round the bun
        a = math.pi * (0.25 + 1.6 * i / 10)
        cr.new_path()
        cr.arc(-62 + 40 * math.cos(a), -128 + 40 * math.sin(a), 6.5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _flower(cr, -62, -128, 14, RED)
    ink(cr, [(10, -186), (24, -178)], 4, col=RED)                                # sindoor
    _jewel(cr, 30, -176, 7, GOLD)                                                # maang-tikka
    if mood == "shock":
        S._w_eyes(cr, SJ_SKIN, "open")
        RU._cover(cr, SJ_SKIN, 30, -132, 22, 6)
        ink(cr, [(12, -140), (30, -148), (48, -140)], 3.5)
        _o_mouth(cr, SJ_SKIN, 60, -70, 6, 8)
    elif mood == "shut":
        S._w_eyes(cr, SJ_SKIN, "faint")
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    else:
        S._w_eyes(cr, SJ_SKIN, mood)
    cr.new_path()
    cr.arc(46, -148, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _jewel(cr, 62, -92, 5, GOLD)                                                 # nose stud
    _jewel(cr, -10, -70, 10, GOLD)
    _shape(cr, [(-20, -60), (-10, -66), (0, -60), (2, -42), (-22, -42)], GOLD, 3, smooth=False)


def _suj_extra(cr):
    """A black-bead mangalsutra with a gold pendant."""
    for i in range(12):
        u = i / 11
        cr.new_path()
        cr.arc(-20 + 56 * u, -280 + 100 * u + 16 * u * u, 4, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
    _jewel(cr, 36, -164, 9, GOLD)


_SJ = dict(skin=SJ_SKIN, skirt=SJ_SARI, choli=SJ_CHOLI, border=GOLD, pallu_col=SJ_PALLU, gem=RED,
           ornaments_extra=_suj_extra)
SUJ = woman("av_suj", hands=("open", "open"), **_SJ)
SUJ.points["belly"] = ("av_suj_body", SUJ_BELLY)
for _m in SJ_MOODS:
    register("av_suj_head" + ("" if _m == "open" else "_" + _m), (-140, -250, 100, 30),
             (lambda m: lambda cr: suj_head(cr, m))(_m))


def suj_body_sit(o, belly=True):
    """Seated on a low stool (hip at 0, 0; soles at +BENCH_H), as dharmavyadha_cast.wbody_sit; belly = a gently rounded
    belly under the sari (the womb window is drawn over it in the scenes)."""
    def fn(cr):
        shin = [(140, 30), (226, 30), (240, 150), (252, 258), (126, 258), (132, 150)]
        _shape(cr, shin, o["skirt"], 5)
        dots_in(cr, lambda: spath(cr, shin), 22, 3.0, shape="d")
        band(cr, [(124, 248), (254, 248)], 18, o.get("border", GOLD), spacing=11, hole_r=2.2)
        _shape(cr, [(234, 254), (276, 258), (280, 270), (230, 272)], o["skin"], 4)
        cr.save()
        cr.rectangle(-400, -600, 800, 640)
        cr.clip()
        woman_body(cr, o)
        cr.restore()
        if belly:
            bx, by = SUJ_BELLY
            bp = [(30, -200), (70, -184), (110, -150), (126, by), (116, -54), (84, -26), (40, -20)]
            _shape(cr, bp, o["skirt"], 5)
            dots_in(cr, lambda: spath(cr, bp), 22, 3.0, shape="d")
            ink(cr, [(60, -186), (96, -150), (112, -100)], 2.6)
        lap = [(-100, -34), (40, -46), (200, -30), (230, 20), (214, 66), (60, 70), (-90, 60), (-112, 20)]
        _shape(cr, lap, o["skirt"], 5)
        dots_in(cr, lambda: spath(cr, lap), 22, 3.0, shape="d")
        for x0, x1 in ((40, 200), (60, 210)):
            ink(cr, [(x0, -20 + (x0 - 40) * 0.2), (x1, 10)], 2.6, smooth=False)
        band(cr, [(204, -26), (230, 20), (214, 62)], 14, o.get("border", GOLD), spacing=11, hole_r=2.2)
        band(cr, [(-40, -36), (0, -42), (40, -40)], 16, o.get("border", GOLD), spacing=11, hole_r=2.2)
        pal = [(-6, -280), (30, -282), (8, -200), (-30, -60), (-70, 60), (-108, 52), (-80, -40), (-52, -200)]
        _shape(cr, pal, o["pallu_col"], 5)                                       # the pallu down her back
        dots_in(cr, lambda: spath(cr, pal), 20, 2.8)
        rivet(cr, 0, 0, 8)
    return fn


register("av_suj_body_sit", (-150, -310, 290, 290), suj_body_sit(_SJ, True))
register("av_suj_body_sit0", (-150, -310, 290, 290), suj_body_sit(_SJ, False))


def _peeta(cr):
    """A low carved wooden stool (pivot at the bottom centre; its seat at y = PEETA_TOP): four turned legs."""
    top = -PEETA_TOP
    _shape(cr, [(-190, -top), (190, -top), (200, -top + 30), (-200, -top + 30)], WOOD, 6, smooth=False,
           holes=(8, 14, 2.6))
    band(cr, [(-180, -top + 16), (180, -top + 16)], 8, GOLD, holes=False)
    for x in (-160, -60, 60, 160):
        leg = [(x - 16, -top + 30), (x + 16, -top + 30), (x + 22, -top + 80), (x + 10, -100), (x + 18, -40),
               (x + 10, 0), (x - 10, 0), (x - 18, -40), (x - 10, -100), (x - 22, -top + 80)]
        _shape(cr, leg, WOOD if abs(x) > 100 else (0.50, 0.30, 0.14), 4)
        punch(cr, [(x, -120)], 4)


register("av_peeta", (-210, PEETA_TOP - 10, 210, 10), _peeta)


# ------------------------------------------------------------------ the disciples


def dis_head(o, mood):
    def fn(cr):
        RU.rface(cr, o, {"calm": "calm", "shock": "shock", "smile": "smile"}[mood])
        _cap_knot(cr, beads=False)
        ink(cr, [(20, -178), (40, -180)], 4, col=ASHW)
    return fn


_D1O = dict(skin=D1_SKIN, hair=False, moustache=False, tilak=False, earring=False)
_D2O = dict(skin=D2_SKIN, hair=False, moustache=False, tilak=False, earring=False)
_D1 = dict(skin=D1_SKIN, bulk=0.86, dhoti=D_CLOTH, border=SAFFRON, pleat=KH_CLOTH2, sash=SAFFRON, neck=BROWN,
           thread=True)
_D2 = dict(skin=D2_SKIN, bulk=0.86, dhoti=D_CLOTH2, border=DGREEN, pleat=KH_CLOTH2, sash=GREEN, neck=BROWN,
           thread=True)
DIS1 = man("av_dis1", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_D1)
DIS2 = man("av_dis2", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_D2)
for _key, _o, _ob in (("av_dis1", _D1O, _D1), ("av_dis2", _D2O, _D2)):
    for _m in ("calm", "shock", "smile"):
        register(_key + "_head" + ("" if _m == "calm" else "_" + _m), (-130, -290, 120, 60), dis_head(_o, _m))
    register(_key + "_body_sit", (-200, -330, 140, 80), DV._sit_body(_ob))
    register(_key + "_seat", (-110, -60, 280, 110),
             (lambda ob: lambda cr: DV._cross_seat(cr, ob["dhoti"], ob["border"], ob["skin"]))(_ob))


# ------------------------------------------------------------------ Ashtavakra


def bend_pt(x, y, th=BEND, y0=-60.0, span=240.0):
    """A torso point with the back rounded: rotated forward about (0, y0), more the higher it is (a curved spine)."""
    if y >= y0 or not th:
        return (x, y)
    u = min(1.0, (y0 - y) / span)
    a = th * u * u * (3 - 2 * u)
    dx, dy = x, y - y0
    return (dx * math.cos(a) - dy * math.sin(a), y0 + dx * math.sin(a) + dy * math.cos(a))


def boy_body(cr, o, th=0.0):
    """puppet_cast.man_body for the boy (slimmer), its torso bent by th (bend_pt): a rounded back with a hump."""
    b = o.get("bulk", 1.0)
    f = lambda pts: [bend_pt(x, y, th) for x, y in pts]                         # noqa: E731
    sc = o.get("sash", RED)
    for dy, ln in ((0, 1.0), (22, 0.75)):
        pts = [(-50 * b, -26 + dy), (-92 * b, -6 + dy), (-118 * b * ln, 40 + dy), (-128 * b * ln, 92 + dy)]
        band(cr, pts, 14, sc, holes=True, spacing=12, hole_r=2.2)
    if th:                                                                       # the hump between the shoulders
        hx, hy = bend_pt(-50 * b, -200, th)
        cr.new_path()
        ell(cr, hx - 8, hy + 6, 46, 62, th)
        leather(cr, o["skin"], 5)
    torso = [(-46 * b, -6), (-54 * b, -100), (-62 * b, -190), (-56 * b, -246), (-30, -284), (-10, -300), (24, -300),
             (36 * b + 4, -282), (68 * b, -252), (86 * b, -208), (82 * b, -160), (64 * b, -110), (55 * b, -50),
             (50 * b, -6)]
    _shape(cr, f(torso), o["skin"], 6)
    ink(cr, f([(36 * b, -222), (62 * b, -192), (80 * b, -176)]), 4)
    holes_line(cr, f([(30 * b, -206), (54 * b, -176), (70 * b, -160)]), 11, 2.4)
    holes_line(cr, f([(-46 * b, -230), (-50 * b, -150), (-42 * b, -70)]), 13, 2.4)
    punch(cr, [bend_pt(46 * b, -78, th)], 4.5)
    if o.get("thread"):
        cr.save()
        cr.set_operator(0)
        spath(cr, f([(-44 * b, -258), (0, -170), (34 * b, -90), (52 * b, -28)]), closed=False)
        cr.set_line_width(6)
        cr.stroke()
        cr.restore()
    band(cr, f([(-12, -290), (26 * b, -252), (64 * b, -222)]), 11, BROWN, spacing=12)
    for i in range(9):                                                           # a rudraksha mala
        u = i / 8
        x, y = bend_pt(-20 + 74 * b * u, -280 + 120 * u * u + 30 * u, th)
        cr.new_path()
        cr.arc(x, y, 7, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    wrap = [(-62 * b, -40), (0, -50), (64 * b, -42), (74 * b, 10), (70 * b, 48), (0, 56), (-70 * b, 48), (-74 * b, 10)]
    _shape(cr, wrap, o["dhoti"], 6)
    dots_in(cr, lambda: spath(cr, wrap), 20, 3.0)
    band(cr, [(-64 * b, -32), (0, -42), (66 * b, -34)], 14, o.get("border", GOLD), spacing=12)
    pf = [(24 * b, 30), (60 * b, 26), (100 * b, 246), (88 * b, 262), (76 * b, 248), (64 * b, 264), (50 * b, 248),
          (38 * b, 262), (26 * b, 246), (16 * b, 258)]
    _shape(cr, pf, o.get("pleat", o.get("border", GOLD)), 5, smooth=False)
    for u in (0.3, 0.55, 0.8):
        ink(cr, [(24 * b + 36 * b * u, 34), (20 * b + 80 * b * u, 250)], 3, smooth=False)
    rivet(cr, 16 * b, 6, 7)


def boy_leg(cr, o, knee=0.0, foot=0.0, side=None):
    """puppet_cast.leg with the shin turned at the knee (knee > 0 bends it back) and the foot turned down (foot > 0)."""
    b = o.get("bulk", 1.0)
    col = o["skin"]
    cr.save()
    cr.translate(0, 196)
    cr.rotate(knee)
    cr.translate(0, -196)
    shin = [(-24 * b, 196), (18 * b, 196), (16 * b, 300), (12 * b, 388), (-10 * b, 392), (-24 * b, 300)]
    _shape(cr, shin, col, 5)
    cr.save()
    cr.translate(0, 386)
    cr.rotate(foot)
    cr.translate(0, -386)
    fp = [(-14, 382), (14, 380), (32, 396), (70, 410), (72, 424), (-16, 426)]
    _shape(cr, fp, col, 4)
    cr.restore()
    band(cr, [(-12 * b, 374), (14 * b, 374)], 9, GOLD, spacing=8, hole_r=2.0)
    cr.restore()
    dl = [(-42 * b, -10), (0, -26), (46 * b, -10), (54 * b, 80), (46 * b, 170), (32 * b, 214), (-26 * b, 214),
          (-38 * b, 170), (-48 * b, 80)]
    _shape(cr, dl, o["dhoti"], 5)
    dots_in(cr, lambda: spath(cr, dl), 19, 2.8)
    band(cr, [(-30 * b, 204), (34 * b, 204)], 14, o.get("border", GOLD), spacing=11, hole_r=2.4)
    ink(cr, [(-10, 20), (-4, 120), (6, 196)], 3)
    rivet(cr, 0, 0, 9)


def boy_wrist(cr, o):
    """The back forearm with the wrist turned in (the hand bent back toward the body)."""
    b = o.get("bulk", 1.0)
    pts = [(-19 * b, -6), (0, -22 * b), (19 * b, -6), (16 * b, 90), (13 * b, 128), (-13 * b, 128), (-16 * b, 90)]
    _shape(cr, pts, o["skin"], 5)
    cr.save()
    cr.translate(0, 124)
    cr.rotate(1.1)
    cr.translate(0, -124)
    hp = [(-13, 122), (14, 122), (24, 148), (22, 176), (12, 196), (4, 186), (-2, 162), (-14, 146)]
    _shape(cr, hp, o["skin"], 4)
    _shape(cr, [(14, 136), (32, 146), (30, 158), (16, 154)], o["skin"], 3)
    cr.restore()
    for y in (106, 118):
        band(cr, [(-15 * b, y), (15 * b, y + 2)], 8, BROWN, spacing=9, hole_r=2.0)
    rivet(cr, 0, 0, 6)


_AV_O = dict(skin=AV_SKIN, hair=False, moustache=False, tilak=False, earring=False)
AV_MOODS = ("calm", "smile", "speak", "firm", "shut", "wonder")
HEAD_K = 1.2                          # the boy's head, larger than an adult's (a child's proportions)


def boy_head(cr, mood="calm"):
    """Ashtavakra at twelve: a hair cap with a top-knot tied in rudraksha, a white sandal-paste tilak, rudraksha studs;
    a bright, confident face."""
    cr.save()
    cr.scale(HEAD_K, HEAD_K)
    base = {"calm": "calm", "smile": "smile", "speak": "calm", "firm": "calm", "shut": "sleep", "wonder": "shock"}
    RU.rface(cr, _AV_O, base[mood])
    if mood in ("calm", "firm"):                                                 # a small, sure smile
        RU._cover(cr, AV_SKIN, 64, -70, 9, 6)
        ink(cr, [(56, -70), (62, -65), (70, -68)], 3.5)
    if mood == "firm":
        ink(cr, [(12, -142), (34, -148), (58, -146)], 6)
    if mood == "speak":
        RU._cover(cr, AV_SKIN, 64, -70, 9, 6)
        cr.new_path()
        ell(cr, 62, -68, 7, 8)
        leather(cr, (0.40, 0.06, 0.06), 2.5)
        ink(cr, [(12, -142), (34, -152), (58, -146)], 5)
    cr.new_path()                                                                # a soft cheek
    ell(cr, 20, -86, 14, 9)
    cr.set_source_rgb(*CHEEK)
    cr.fill()
    _cap_knot(cr)
    ink(cr, [(22, -186), (26, -158)], 4, col=ASHW)                               # sandal-paste tilak (a U)
    ink(cr, [(40, -186), (38, -158)], 4, col=ASHW)
    ink(cr, [(26, -158), (32, -152), (38, -158)], 4, col=ASHW)
    cr.new_path()
    cr.arc(32, -164, 4, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()
    cr.arc(-14, -80, 7, 0, 2 * math.pi)
    leather(cr, BROWN, 2)
    cr.restore()


_AV = dict(skin=AV_SKIN, bulk=BOY_BULK, dhoti=AV_CLOTH, border=SAFFRON, pleat=AV_CLOTH, sash=AV_SASH, neck=BROWN,
           thread=True)
BOY = man("av_boy", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_AV)
register("av_boy_body", (-200, -330, 140, 300), lambda cr: boy_body(cr, _AV, 0.0))
register("av_boy_body_bent", (-220, -340, 220, 300), lambda cr: boy_body(cr, _AV, BEND))
register("av_boy_legF_bent", (-150, -40, 160, 460), lambda cr: boy_leg(cr, _AV, 0.42, 0.45))
register("av_boy_legB_bent", (-150, -40, 160, 460), lambda cr: boy_leg(cr, _AV, -0.22, -0.2))
register("av_boy_armB_lo_bent", (-60, -30, 100, 210), lambda cr: boy_wrist(cr, _AV))
for _m in AV_MOODS:
    register("av_boy_head" + ("" if _m == "calm" else "_" + _m), (-190, -340, 160, 140),
             (lambda m: lambda cr: boy_head(cr, m))(_m))


def _bent_rig(rig, th=BEND):
    """BOY with the shoulders and the head carried forward by the rounded back (the same parts and angles)."""
    b = BOY_BULK
    moved = {"av_boy_head": (bend_pt(6, -300, th), -0.75 * th),
             "av_boy_armF_up": (bend_pt(26 * b, -262, th), 0.0),
             "av_boy_armB_up": (bend_pt(-14 * b, -262, th), 0.0),
             "av_boy_legF": ((16 * b, 8), -0.22),
             "av_boy_legB": ((-12 * b, 8), 0.16)}
    parts = []
    for name, parent, anchor, rest in rig.parts:
        if name in moved:
            anchor, dr = moved[name]
            rest = rest + dr if name in ("av_boy_head",) else (dr if name.startswith("av_boy_leg") else rest)
        parts.append((name, parent, anchor, rest))
    pts = dict(rig.points)
    pts["chest"] = ("av_boy_body", bend_pt(0, -200, th))
    return Rig(parts, pts, rig.rods)


BOY_BENT = _bent_rig(BOY)
BENT_SWAP = {"av_boy_body": "av_boy_body_bent", "av_boy_legF": "av_boy_legF_bent", "av_boy_legB": "av_boy_legB_bent",
             "av_boy_armB_lo": "av_boy_armB_lo_bent"}


def _staff(cr):
    """A plain bamboo staff (pivot at its foot, 700 units tall): nodes every 120 units, a cord wound at the grip."""
    band(cr, [(0, 0), (0, -700)], 18, BAMBOO, spacing=26, hole_r=2.2)
    for y in range(-110, -700, -120):
        band(cr, [(-11, y), (11, y)], 7, (0.62, 0.44, 0.18), holes=False)
    for k in range(5):
        ink(cr, [(-10, -430 - 9 * k), (10, -436 - 9 * k)], 3, col=RED)
    cr.new_path()
    ell(cr, 0, -704, 12, 9)
    leather(cr, BAMBOO, 3)


register("av_staff", (-30, -720, 30, 10), _staff)


# ------------------------------------------------------------------ the unborn child, the newborn


def _fetus(cr, talk=False):
    """The unborn child curled in the womb (facing +x, centre at 0, 0): a big round head bowed forward, the back
    curved, the knee drawn up to the chest and the little foot tucked under."""
    col, ink_c = BABY, (0.50, 0.26, 0.10)
    body = [(-56, -96), (-94, -36), (-102, 36), (-76, 92), (-14, 116), (48, 104), (80, 64), (74, 4), (44, -52)]
    _shape(cr, body, col, 5)
    holes_line(cr, [(-78, -30), (-86, 26), (-64, 80)], 15, 2.4)                  # the spine, punched
    shin = [(64, -6), (92, 12), (100, 70), (118, 88), (120, 104), (84, 108), (66, 84), (60, 24)]
    _shape(cr, shin, col, 4)
    thigh = [(-62, 84), (-24, 50), (36, -2), (78, -16), (96, 8), (74, 42), (14, 94), (-36, 110)]
    _shape(cr, thigh, col, 4)
    ink(cr, [(-10, 76), (50, 22)], 2.4, col=ink_c)
    head = [(-66, -150), (-40, -214), (10, -238), (62, -222), (92, -184), (100, -156), (112, -146), (100, -136),
            (102, -122), (90, -106), (60, -90), (16, -84), (-30, -96), (-58, -118)]
    _shape(cr, head, col, 5)
    ink(cr, [(-30, -222), (-6, -244), (22, -240)], 3, col=ink_c)                  # a wisp of hair
    ink(cr, [(-12, -232), (4, -252)], 2.4, col=ink_c)
    cr.new_path()
    ell(cr, 2, -146, 12, 16)                                                     # the ear
    leather(cr, col, 3)
    ink(cr, [(0, -154), (6, -146), (0, -138)], 2.2, col=ink_c)
    cr.new_path()
    ell(cr, 64, -124, 15, 9)
    cr.set_source_rgb(*CHEEK)
    cr.fill()
    if talk:
        almond_eye_small(cr, 64, -164, talk)
        ink(cr, [(48, -186), (64, -192), (82, -184)], 3.5, col=ink_c)
        cr.new_path()
        ell(cr, 96, -116, 7, 9)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
    else:
        ink(cr, [(50, -162), (64, -154), (78, -162)], 3.5, col=ink_c)
        for x in (56, 64, 72):
            ink(cr, [(x, -157), (x - 1, -150)], 1.8, col=ink_c)
        ink(cr, [(88, -116), (96, -112), (100, -116)], 2.6, col=(0.70, 0.30, 0.22))


def almond_eye_small(cr, x, y, _):
    cr.new_path()
    cr.move_to(x - 14, y)
    cr.curve_to(x - 7, y - 12, x + 7, y - 12, x + 14, y + 1)
    cr.curve_to(x + 7, y + 9, x - 7, y + 9, x - 14, y)
    cr.close_path()
    leather(cr, PALE, 2.5)
    cr.new_path()
    cr.arc(x + 3, y - 1, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(x + 5, y - 3)], 1.8)


def _fetus_arm(cr):
    """The unborn child's arm (pivot at the shoulder, hanging along +y) with the index finger pointing out."""
    col = BABY
    _shape(cr, [(-14, -6), (0, -16), (14, -6), (12, 70), (8, 96), (-8, 96), (-12, 70)], col, 4)
    _shape(cr, [(-12, 92), (12, 92), (18, 112), (8, 124), (-10, 120), (-16, 106)], col, 3.5)   # the fist
    _shape(cr, [(2, 116), (8, 118), (9, 158), (3, 162), (-3, 158), (-4, 120)], col, 3)        # the finger
    rivet(cr, 0, 0, 5)


def _swaddle(cr):
    """The newborn wrapped in a saffron cloth with a gold border (lying, head to +x; pivot at the bundle's centre)."""
    cl = [(-150, -10), (-130, -60), (-40, -86), (60, -80), (110, -60), (120, 10), (90, 56), (-40, 66), (-130, 50)]
    _shape(cr, cl, SJ_PALLU, 5)
    dots_in(cr, lambda: spath(cr, cl), 20, 2.8)
    band(cr, [(-60, -80), (-30, 0), (-50, 60)], 12, GOLD, spacing=10, hole_r=2.0)
    cr.new_path()
    ell(cr, 124, -26, 50, 46)                                                    # the face, turned up
    leather(cr, BABY, 5)
    hood = [(70, 14), (62, -40), (84, -78), (126, -92), (168, -76), (150, -66), (120, -72), (94, -60), (82, -30),
            (88, 8)]
    _shape(cr, hood, SJ_PALLU, 4)
    ink(cr, [(116, -40), (128, -32), (140, -40)], 3)
    for x in (120, 128, 136):
        ink(cr, [(x, -35), (x - 1, -29)], 1.8)
    ink(cr, [(148, -8), (156, -4), (162, -8)], 2.6, col=(0.70, 0.30, 0.22))
    ink(cr, [(168, -30), (174, -22), (168, -16)], 2.4)
    cr.new_path()
    ell(cr, 120, -12, 11, 7)
    cr.set_source_rgb(*CHEEK)
    cr.fill()


register("av_fetus", (-130, -260, 140, 120), lambda cr: _fetus(cr, False))
register("av_fetus_talk", (-130, -260, 140, 120), lambda cr: _fetus(cr, True))
register("av_fetus_arm", (-30, -30, 30, 175), _fetus_arm)
register("av_swaddle", (-170, -110, 190, 80), _swaddle)


# ------------------------------------------------------------------ Janaka


_JN_O = dict(skin=JN_SKIN, hair=True, moustache=True, tilak=True, earring=True)


def janaka_head(cr, mood="calm"):
    """King Janaka: a long white beard and moustache, a gold kirita with a green flare before a gold flame halo."""
    A.face(cr, dict(_JN_O, moustache=False), {"wonder": "calm"}.get(mood, mood))
    if mood == "wonder":
        RU._cover(cr, JN_SKIN, 34, -118, 27, 16)
        RU._cover(cr, JN_SKIN, 34, -141, 25, 8)
        RU.almond_eye_big(cr)
        ink(cr, [(10, -160), (34, -170), (58, -162)], 5)
    bp = [(60, -56), (68, -30), (62, 20), (46, 80), (26, 130), (12, 70), (-2, 20), (-10, -36), (14, -44), (38, -58)]
    _shape(cr, bp, BEARD, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -40), (40 - 12 * k, 30), (32 - 10 * k, 100)], 2.5, col=(0.60, 0.58, 0.56))
    m = [(66, -76), (44, -86), (24, -90), (8, -104), (22, -94), (44, -84), (68, -80)]
    _shape(cr, m, BEARD, 3)
    R.kirita(cr, GOLD, (0.98, 0.72, 0.20), 1.0, flare=GREEN)


_JN = dict(skin=JN_SKIN, bulk=1.06, dhoti=JN_DHOTI, border=GOLD, pleat=GOLD, sash=JN_SASH, neck=GOLD, thread=True)
JANAKA = man("av_janaka", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_JN)
for _m in ("calm", "smile", "wonder"):
    register("av_janaka_head" + ("" if _m == "calm" else "_" + _m), (-220, -470, 140, 170),
             (lambda m: lambda cr: janaka_head(cr, m))(_m))
register("av_janaka_body_sit", (-200, -330, 140, 80), DV._sit_body(_JN))
register("av_janaka_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, JN_SKIN, JN_DHOTI, GOLD, 1.06))


# ------------------------------------------------------------------ Vandin


_VD_O = dict(skin=VD_SKIN, hair=False, moustache=False, tilak=False, earring=False, beard=True)
VD_MOODS = ("calm", "smirk", "speak", "shock")


def turban(cr):
    """A tall court turban (a Mysore-peta-like pagdi): red and gold bands wound up high, a jewelled sarpech and a
    white plume."""
    back_ = [(-56, -120), (-70, -170), (-64, -230), (-40, -290), (0, -318), (44, -300), (62, -250), (60, -180),
             (50, -140)]
    _shape(cr, back_, VD_TURBAN, 5, holes=(10, 14, 2.6))
    for k, y in enumerate((-150, -190, -230, -268)):
        w0 = 58 - 4 * k
        band(cr, [(-w0 - 6, y + 8), (0, y - 6), (w0 + 2, y + 2)], 16, GOLD if k % 2 == 0 else (0.98, 0.84, 0.50),
             spacing=11, hole_r=2.2)
    _shape(cr, [(30, -300), (62, -280), (90, -300), (70, -318)], VD_TURBAN, 4)     # the folded tail at the front
    _jewel(cr, 34, -210, 14, GREEN)
    for i in range(5):
        a = -0.9 + 0.45 * i
        _jewel(cr, 34 + 26 * math.cos(a), -210 + 26 * math.sin(a), 5, PALE)
    plume = [(30, -300), (20, -350), (36, -400), (60, -430), (52, -390), (48, -350), (44, -304)]
    _shape(cr, plume, PALE, 4)
    holes_line(cr, [(30, -320), (40, -380), (54, -420)], 12, 2.0)


def vandin_head(cr, mood="calm"):
    """Vandin: the tall turban, a curled moustache, a short pointed beard; smirk: a half-shut eye under a raised brow
    and a sly smile."""
    base = {"smirk": "proud", "speak": "scold", "shock": "shock", "calm": "calm"}[mood]
    RU.rface(cr, _VD_O, base)
    if mood == "smirk":
        RU._cover(cr, VD_SKIN, 34, -122, 26, 18)
        almond_eye_lid(cr)
        ink(cr, [(10, -150), (32, -166), (58, -156)], 5)                         # the brow raised
        RU._cover(cr, VD_SKIN, 62, -70, 10, 7)
        ink(cr, [(52, -66), (64, -68), (72, -78)], 3.5)                           # the sly smile, up at one end
    m = [(68, -76), (48, -84), (28, -84), (6, -96), (-4, -116), (12, -104), (30, -94), (50, -88), (70, -82)]
    _shape(cr, m, HAIR, 3)
    pb = [(56, -48), (62, -28), (56, 6), (44, 40), (34, 8), (22, -20), (36, -40)]
    _shape(cr, pb, HAIR, 3)
    turban(cr)
    _jewel(cr, -12, -72, 12, GOLD)
    cr.new_path()
    cr.arc(-12, -50, 8, 0, 2 * math.pi)
    leather(cr, (0.98, 0.84, 0.50), 2)


def almond_eye_lid(cr):
    """A proud, half-shut eye: the lid low over the pupil."""
    almond_eye(cr, 34, -118, 38, 13, col=PALE)
    cr.new_path()
    cr.move_to(13, -118)
    cr.curve_to(24, -136, 44, -136, 55, -116)
    cr.curve_to(44, -120, 24, -120, 13, -118)
    cr.close_path()
    leather(cr, VD_SKIN, 3.5)


_VD = dict(skin=VD_SKIN, bulk=1.12, dhoti=VD_DHOTI, border=GOLD, pleat=GOLD, sash=GOLD, neck=GOLD, robe=VD_ROBE,
           thread=True)
VANDIN = man("av_vandin", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"),
             **_VD)
for _m in VD_MOODS:
    register("av_vandin_head" + ("" if _m == "calm" else "_" + _m), (-140, -450, 120, 70),
             (lambda m: lambda cr: vandin_head(cr, m))(_m))


# ------------------------------------------------------------------ props


def _lamp(cr):
    """A small clay oil lamp on a short brass stand (pivot at the foot; the wick at 0, -250)."""
    _shape(cr, [(-60, 0), (60, 0), (40, -24), (-40, -24)], (0.86, 0.66, 0.26), 4, smooth=False)
    band(cr, [(0, -24), (0, -180)], 16, (0.86, 0.66, 0.26), spacing=16, hole_r=2.0)
    cr.new_path()
    ell(cr, 0, -100, 22, 12)
    leather(cr, (0.86, 0.66, 0.26), 3)
    _shape(cr, [(-70, -200), (-40, -180), (40, -180), (74, -206), (90, -232), (40, -222), (-60, -222)], CLAY, 4)
    punch(cr, [(-30, -202), (0, -200), (30, -202)], 3)


def _altar_w(cr):
    """A small square fire altar (pivot at the bottom centre) for the yajna under the water."""
    _shape(cr, [(-130, 0), (130, 0), (120, -50), (-120, -50)], (0.70, 0.50, 0.30), 5, smooth=False, holes=(8, 13, 2.4))
    _shape(cr, [(-100, -50), (100, -50), (90, -100), (-90, -100)], (0.80, 0.58, 0.34), 5, smooth=False,
           holes=(8, 13, 2.4))
    for x in (-60, 0, 60):
        _flower(cr, x, -24, 12, RED, 6)


register("av_lamp", (-100, -250, 100, 10), _lamp)
register("av_altar_w", (-140, -110, 140, 10), _altar_w)
register("av_rwaveA", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, RIVER))
register("av_rwaveB", (-1050, -46, 1050, 56), lambda cr: R._wave(cr, RIVER2))
