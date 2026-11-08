"""The leather cast and props for the Mandhata reel (videos/mandhata.py), in the Togalu Gombeyaata style of the
Jarasandha, Ravana, Kaikeyi and Lakshman Rekha reels (puppet_cast, ravana_cast, kaikeyi_cast, lrekha_cast): profile
figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor
and no film.

Cast (one look each, kept the same through the video):
  YUVANASHVA the king: warm skin, a black moustache, a gold kirita with a blue flare and a violet halo, a teal dhoti
             with a saffron sash. From m9 his belly is gently rounded (yuva_body_b1..b7, swapped in step by step);
             shown with dignity, the same proud figure.
  SAGES      PULASTYA (ravana_cast: white hair and beard, cream dhoti, saffron robe) and a second sage in the same
             style with a saffron dhoti and an ochre robe (mdsage). Both can sleep (closed-eye heads).
  BABY       a whole baby (the Jarasandha baby's frontal design, not cut): warm golden skin, a top-knot, a gold
             langot; eyes open, shut (content) or crying (with tears and an open mouth).
  INDRA      king of the gods: pale gold skin, a very tall gold crown with a red flare in front of a ring of golden
             rays, gold dhoti with blue border and sash, the vajra in his hand; kneels (indra_kneel).
  ASHVINS    the twin physicians of the gods: two identical young figures, small gold crowns with a green flare, green
             dhoti with saffron border, a herb pouch at the hip; one holds a herb sprig, the other a medicine pot.
  MANDHATA   the grown emperor: golden skin like the baby's, a grand three-peaked crown in front of a saffron sun-ray
             halo, red dhoti, green sash, a chakra sceptre; sits on his throne (mandhata_seat legs).
Props: the clay kalasha of blessed water (a red kalava thread, a painted lotus), a lotus pedestal, the vajra, a herb
sprig, a medicine pot, the herb pouch, a chakra sceptre, straw sleeping mats, the emperor's throne (an open arched back,
so he stays clear in front of it), the world strip (land, hills and small cities along a horizon). The yajna fire,
moon, stars, sun, palace arch, trees, cradle, the queen's shadow and palm-leaf books come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book boards and leaves)
import puppet_cast as C
import ravana_cast as R
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, RED, ROSE, SAFFRON, VIOLET, Rig,
                         almond_eye, band, dots_in, ell, holes_line, ink, leather, poly, punch, register, rivet, spath)

YV_SKIN = (0.98, 0.74, 0.52)          # Yuvanashva
YV_DHOTI = (0.16, 0.58, 0.64)         # teal
BABY_SKIN = (1.0, 0.80, 0.50)         # the baby, and Mandhata grown up
MD_SKIN = (0.99, 0.77, 0.48)
IN_SKIN = (1.0, 0.88, 0.66)           # Indra: pale gold
AS_SKIN = (0.93, 0.64, 0.40)          # the Ashvins
CLAY = (0.84, 0.46, 0.22)
CLAY2 = (0.64, 0.30, 0.14)
LOTUS = (1.0, 0.62, 0.58)
LOTUS2 = (0.96, 0.40, 0.42)
TEAR = (0.46, 0.70, 1.0)
BELLY_LEVELS = 7                      # yuva_body_b1 .. b7: the belly growing in steps

# ------------------------------------------------------------------ Yuvanashva


def yv_body(cr, o, k):
    """puppet_cast.man_body with the belly rounded by k (0 = flat .. 1 = full), the waist wrap tucked under it."""
    b = o.get("bulk", 1.0)
    sc = o.get("sash", RED)
    for dy, ln in ((0, 1.0), (22, 0.75)):
        pts = [(-50 * b, -26 + dy), (-92 * b, -6 + dy), (-118 * b * ln, 40 + dy), (-128 * b * ln, 92 + dy)]
        band(cr, pts, 14, sc, holes=True, spacing=12, hole_r=2.2)
    torso = [(-46 * b, -6), (-54 * b, -100), (-62 * b, -190), (-56 * b, -246), (-30, -284), (-10, -300), (24, -300),
             (36 * b + 4, -282), (68 * b, -252), (86 * b, -208), (84 * b, -172), ((72 + 30 * k) * b, -140),
             ((64 + 66 * k) * b, -104), ((57 + 80 * k) * b, -66), ((52 + 58 * k) * b, -30), ((50 + 16 * k) * b, -6)]
    _shape(cr, torso, o["skin"])
    ink(cr, [(36 * b, -222), (62 * b, -192), (80 * b, -176)], 4)                 # chest
    holes_line(cr, [(30 * b, -206), (54 * b, -176), (70 * b, -160)], 11, 2.4)
    holes_line(cr, [(-46 * b, -230), (-50 * b, -150), (-42 * b, -70)], 13, 2.4)
    if k < 0.3:
        holes_line(cr, [(20 * b, -150), (40 * b, -120), (44 * b, -60)], 13, 2.2)
        ink(cr, [(40 * b, -132), (60 * b, -122)], 3.5)
    else:                                                                       # a soft line following the belly
        ink(cr, [((40 + 20 * k) * b, -150), ((70 + 50 * k) * b, -110), ((80 + 50 * k) * b, -64)], 3.0)
    punch(cr, [((46 + 70 * k) * b, -76)], 4.5)                                  # navel
    nk = o.get("neck", GOLD)
    band(cr, [(-12, -290), (26 * b, -252), (64 * b, -222)], 13, nk, spacing=12)
    band(cr, [(-26, -282), (14 * b, -200), (56 * b, -150)], 9, nk, spacing=11, hole_r=2.2)
    _jewel(cr, 60 * b, -136, 12, RED)
    wrap = [(-62 * b, -40), (0, -50), ((64 + 50 * k) * b, -40 + 8 * k), ((74 + 30 * k) * b, 10), ((70 + 10 * k) * b, 48),
            (0, 56), (-70 * b, 48), (-74 * b, 10)]
    _shape(cr, wrap, o["dhoti"], 6)
    dots_in(cr, lambda: spath(cr, wrap), 20, 3.0)
    band(cr, [(-64 * b, -32), (0, -42), ((66 + 48 * k) * b, -32 + 8 * k)], 14, o.get("border", GOLD), spacing=12)
    pf = [(24 * b, 30), (60 * b, 26), (100 * b, 246), (88 * b, 262), (76 * b, 248), (64 * b, 264), (50 * b, 248),
          (38 * b, 262), (26 * b, 246), (16 * b, 258)]
    _shape(cr, pf, o.get("pleat", o.get("border", GOLD)), 5, smooth=False)
    for u in (0.3, 0.55, 0.8):
        ink(cr, [(24 * b + 36 * b * u, 34), (20 * b + 80 * b * u, 250)], 3, smooth=False)
    holes_line(cr, [(28 * b, 236), (94 * b, 232)], 12, 2.6)
    rivet(cr, 16 * b, 6, 7)


def belly_xy(k, bulk=1.06):
    """The belly's centre (body coordinates) and its front, for the glow and the hand resting on it."""
    return ((34 + 52 * k) * bulk, -96), ((66 + 78 * k) * bulk, -100)


_YV_O = dict(skin=YV_SKIN, crown="tiara", hair=True, halo=False, moustache=True, tilak=True)


def yuva_head(cr):
    """Yuvanashva: a violet flame halo, long black hair, a black moustache, a gold kirita with a blue flare."""
    K._halo(cr, VIOLET)
    C.man_head(cr, _YV_O)
    R.kirita(cr, GOLD, None, tall=1.12, flare=BLUE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.12, 10, BLUE)


_YV = dict(skin=YV_SKIN, bulk=1.06, dhoti=YV_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD)
YUVA = man("yuva", crown="tiara", halo=False, moustache=True, hands=("open", "open"), **_YV)
register("yuva_head", (-220, -460, 130, 130), yuva_head)
register("yuva_body", (-200, -330, 200, 300), lambda cr: yv_body(cr, _YV, 0.0))
for _k in range(1, BELLY_LEVELS + 1):
    register(f"yuva_body_b{_k}", (-200, -330, 200, 300), (lambda k: lambda cr: yv_body(cr, _YV, k))(_k / BELLY_LEVELS))


# ------------------------------------------------------------------ the sages


PULASTYA = R.PULASTYA


def _sleep_eye(cr, skin):
    """Close the almond eye of a man_head (at 34, -118): skin over it, a calm closed lid with lashes."""
    cr.new_path()
    ell(cr, 34, -117, 24, 16)
    cr.set_source_rgb(*skin)
    cr.fill()
    ink(cr, [(14, -118), (34, -110), (54, -118)], 4.5)
    for x in (24, 34, 44):
        ink(cr, [(x, -112), (x - 2, -104)], 2.5)


def sage_sleep_head(cr):
    R.pulastya_head(cr)
    _sleep_eye(cr, R.SAGE_SKIN)


MDSAGE = man("mdsage", skin=R.SAGE_SKIN, bulk=0.9, dhoti=SAFFRON, border=DRED, pleat=DRED, sash=OCHRE, crown="tiara",
             beard=True, hair=False, robe=OCHRE, beads=True, halo=False, earring=False, neck=BROWN,
             hands=("open", "fist"), tilak=False)
register("mdsage_head", (-190, -360, 110, 140), R.pulastya_head)
register("md_sage_sleep", (-190, -360, 110, 140), sage_sleep_head)


# ------------------------------------------------------------------ the baby (whole, frontal)


def _sym(top, half, bottom):
    """A closed outline symmetric about x = 0: top point, the left half (top to bottom), bottom point, the mirror."""
    return [top] + list(half) + [bottom] + [(-x, y) for x, y in reversed(half)]


def baby_body(cr):
    """The whole baby (frontal; hip pivot at 0, 0): the Jarasandha baby's shapes, both sides, no cut."""
    col = BABY_SKIN
    _shape(cr, _sym((0, -248), [(-60, -242), (-118, -218), (-150, -176), (-154, -100), (-140, -36), (-118, 6),
                                (-70, 24)], (0, 30)), col, 7)
    langot = [(-112, -12), (-96, 30), (-50, 56), (0, 66), (50, 56), (96, 30), (112, -12), (0, -14)]
    cr.new_path()
    poly(cr, langot)
    pl = leather(cr, GOLD, 5, keep=True)
    from puppet_core import perforate
    perforate(cr, pl, 9, 13, 2.6)
    band(cr, [(-116, -22), (-60, -18), (0, -18), (60, -18), (116, -22)], 16, RED, spacing=12)
    for sx in (-1, 1):                                                          # ears, earrings
        cr.new_path()
        ell(cr, sx * 172, -428, 24, 40)
        leather(cr, col, 5)
    _shape(cr, _sym((0, -606), [(-70, -598), (-128, -566), (-166, -500), (-174, -424), (-160, -350), (-126, -292),
                                (-72, -262)], (0, -252)), col, 7)
    for sx in (-1, 1):
        _jewel(cr, sx * 178, -378, 13, GOLD)
    cr.new_path()                                                               # top-knot
    ell(cr, 0, -632, 42, 28)
    leather(cr, HAIR, 5)
    band(cr, [(-30, -610), (30, -610)], 10, GOLD, spacing=9, hole_r=2.0)
    for sx in (-1, 1):
        ink(cr, [(sx * 150, -520), (sx * 110, -572), (sx * 50, -596)], 5, col=HAIR)
        ink(cr, [(sx * 108, -490), (sx * 74, -502), (sx * 36, -494)], 6)        # brows
        cr.new_path()
        cr.arc(sx * 112, -350, 22, 0, 2 * math.pi)                              # painted cheeks
        cr.set_source_rgb(*DRED)
        cr.set_line_width(3)
        cr.stroke()
        punch(cr, [(sx * 112 + 12 * math.cos(a), -350 + 12 * math.sin(a)) for a in [i * 1.047 for i in range(6)]], 2.6)
        ink(cr, [(sx * 60, -150), (sx * 110, -120)], 4)
    ink(cr, [(-14, -380), (0, -368), (14, -380)], 5)                            # nose
    ink(cr, [(-40, -326), (-20, -314), (0, -311), (20, -314), (40, -326)], 6, col=DRED)   # a small smile
    band(cr, [(-124, -196), (-70, -222), (0, -228), (70, -222), (124, -196)], 14, GOLD, spacing=11, hole_r=2.4)
    _jewel(cr, 0, -212, 10, RED)
    punch(cr, [(0, -96)], 5)


def baby_eyes(cr, mode="open"):
    """Both eyes (centres at -70 and 70): open and looking out, shut (content), or crying (squeezed, tears)."""
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 70, 0)
        if mode == "open":
            C.baby_eye(cr, 0)
        elif mode == "shut":
            C.baby_eye(cr, 0, shut=True)
        else:
            ink(cr, [(-44, -4), (-4, 10), (40, -6)], 9)
            ink(cr, [(-40, -46), (0, -40), (sx * 44, -60 + 30 * (sx > 0))], 7)  # worried brows
            for k, (tx, ty) in enumerate(((sx * 10, 36), (sx * 22, 70))):
                cr.new_path()
                cr.move_to(tx, ty - 16)
                cr.curve_to(tx + 10, ty, tx + 9, ty + 12, tx, ty + 12)
                cr.curve_to(tx - 9, ty + 12, tx - 10, ty, tx, ty - 16)
                leather(cr, TEAR, 2.5)
        cr.restore()


def baby_mouth_cry(cr):
    """A wide open crying mouth (body coordinates), drawn over the smile."""
    cr.new_path()
    ell(cr, 0, -316, 44, 34)
    leather(cr, (0.35, 0.05, 0.06), 5)
    cr.new_path()
    ell(cr, 0, -298, 24, 12)
    cr.set_source_rgb(*ROSE)
    cr.fill()


register("mb_body", (-210, -680, 210, 80), baby_body)
register("mb_eyes", (-150, -70, 150, 50), lambda cr: baby_eyes(cr, "open"))
register("mb_eyes_shut", (-150, -70, 150, 50), lambda cr: baby_eyes(cr, "shut"))
register("mb_eyes_cry", (-150, -80, 150, 100), lambda cr: baby_eyes(cr, "cry"))
register("mb_mouth", (-60, -360, 60, -270), baby_mouth_cry)
register("mb_armL", (-50, -50, 50, 240), lambda cr: C.baby_arm(cr, -1, BABY_SKIN))
register("mb_armR", (-50, -50, 50, 240), lambda cr: C.baby_arm(cr, 1, BABY_SKIN))
register("mb_legL", (-80, -45, 80, 250), lambda cr: C.baby_leg(cr, -1, BABY_SKIN))
register("mb_legR", (-80, -45, 80, 250), lambda cr: C.baby_leg(cr, 1, BABY_SKIN))
BABY = Rig([("mb_legL", "mb_body", (-72, 14), 0.12),
            ("mb_legR", "mb_body", (72, 14), -0.12),
            ("mb_body", None, (0, 0), 0.0),
            ("mb_armL", "mb_body", (-128, -196), 0.42),
            ("mb_armR", "mb_body", (128, -196), -0.42),
            ("mb_eyes", "mb_body", (0, -420), 0.0)],
           {"chest": ("mb_body", (0, -150)), "handL": ("mb_armL", (0, 196)), "handR": ("mb_armR", (0, 196)),
            "head": ("mb_body", (0, -430)), "mouth": ("mb_body", (0, -316)), "top": ("mb_body", (0, -650)),
            "belly": ("mb_body", (0, -90))},
           [("chest", 60, 0), ("handR", 160, 0)])
BABY_FEET = 236.0                     # hip pivot to the soles (design units)


# ------------------------------------------------------------------ Indra


def _ray_halo(cr, cx, cy, r0, r1, n, cols):
    """A ring of pointed rays behind a head (light), perforated."""
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n
        r = r1 if i % 2 == 0 else r0
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    _shape(cr, pts, cols[0], 5, smooth=False, holes=(12, 15, 3))
    cr.new_path()
    cr.arc(cx, cy, r0 * 0.86, 0, 2 * math.pi)
    leather(cr, cols[1], 4)
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        punch(cr, [(cx + r0 * 0.66 * math.cos(a), cy + r0 * 0.66 * math.sin(a))], 4.5)


_IN_O = dict(skin=IN_SKIN, crown="tiara", hair=True, halo=False, tilak=True)


def indra_head(cr):
    """Indra: a ring of golden rays, long hair, a very tall jewelled gold crown with a red flare."""
    _ray_halo(cr, -30, -250, 150, 232, 16, (GOLD, PALE))
    C.man_head(cr, _IN_O)
    R.kirita(cr, GOLD, None, tall=1.55, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.55
    for y, c in ((-300, GREEN), (-330, BLUE)):
        _jewel(cr, 2, h(y), 9, c)
    for sx in (-1, 1):                                                          # crown wings
        _shape(cr, [(sx * 46, -180), (sx * 84, -236), (sx * 76, -276), (sx * 56, -232)], GOLD, 4, holes=(8, 11, 2.2))


INDRA = man("indra", skin=IN_SKIN, bulk=1.1, dhoti=GOLD, border=BLUE, pleat=BLUE, sash=BLUE, neck=GOLD, crown="tiara",
            halo=False, thread=True, hands=("open", "fist"))
register("indra_head", (-280, -560, 230, 130), indra_head)
register("indra_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, IN_SKIN, GOLD, BLUE, 1.1))


def _vajra(cr):
    """Indra's vajra (grip at 0, 0): a central prong and two curved side prongs at each end, a blue jewel."""
    for s in (-1, 1):
        for sx in (-1, 1):
            _shape(cr, [(sx * 8, s * 46), (sx * 66, s * 104), (sx * 62, s * 170), (sx * 10, s * 222), (sx * 36, s * 166),
                        (sx * 40, s * 112), (sx * 4, s * 70)], GOLD, 4)
        _shape(cr, [(-13, s * 40), (13, s * 40), (10, s * 186), (0, s * 230), (-10, s * 186)], GOLD, 4, smooth=False)
        cr.new_path()
        ell(cr, 0, s * 48, 30, 13)
        leather(cr, GOLD, 4)
    band(cr, [(0, -38), (0, 38)], 26, GOLD, spacing=10, hole_r=2.2)
    _jewel(cr, 0, 0, 13, BLUE)


register("md_vajra", (-80, -250, 80, 250), _vajra)


# ------------------------------------------------------------------ the Ashvins


_AS_O = dict(skin=AS_SKIN, crown="tiara", hair=True, halo=False, tilak=True)


def ashvin_head(cr):
    C.man_head(cr, _AS_O)
    R.kirita(cr, GOLD, None, tall=0.72, flare=GREEN)
    _flower(cr, 4, -205, 16, PALE, 8)


def _pouch(cr):
    """A healer's leather pouch hanging from the belt (pivot at the strap), herbs showing."""
    for x, a in ((-20, -0.4), (0, 0.0), (22, 0.35)):
        cr.save()
        cr.translate(x, 10)
        cr.rotate(a)
        ink(cr, [(0, 0), (0, -70)], 4, col=DGREEN)
        for y in (-30, -56):
            _shape(cr, [(0, y), (-22, y - 14), (-4, y - 8)], GREEN, 2.5)
            _shape(cr, [(0, y - 4), (22, y - 18), (4, y - 12)], GREEN, 2.5)
        cr.restore()
    bag = [(-50, 0), (50, 0), (58, 70), (40, 112), (0, 122), (-40, 112), (-58, 70)]
    _shape(cr, bag, OCHRE, 5, holes=(9, 12, 2.4))
    _shape(cr, [(-52, 0), (52, 0), (40, 40), (0, 52), (-40, 40)], BROWN, 4)
    _jewel(cr, 0, 42, 9, RED)


def _herb(cr):
    """A sprig of healing herbs (grip at 0, 0)."""
    ink(cr, [(0, 30), (2, -120), (-6, -230)], 6, col=DGREEN)
    for i, y in enumerate((-60, -110, -160, -205)):
        for sx in (-1, 1):
            L_ = 52 - 6 * i
            _shape(cr, [(0, y), (sx * L_ * 0.5, y - 26), (sx * L_, y - 18), (sx * L_ * 0.55, y + 2)], GREEN, 3)
            ink(cr, [(0, y), (sx * L_ * 0.8, y - 16)], 1.8, col=DGREEN)
    for x, y in ((-6, -238), (16, -196), (-22, -150)):
        _flower(cr, x, y, 13, PALE, 5)


def _medpot(cr):
    """A small round medicine pot with a knobbed lid, hanging from the hand by its cord (cord at 0, 0)."""
    ink(cr, [(0, 0), (0, 30)], 3)
    _shape(cr, [(-30, 30), (30, 30), (24, 50), (-24, 50)], GOLD, 3, smooth=False)
    cr.new_path()
    ell(cr, 0, 54, 10, 8)
    leather(cr, GOLD, 2.5)
    body = [(-24, 54), (24, 54), (56, 84), (64, 120), (50, 152), (0, 166), (-50, 152), (-64, 120), (-56, 84)]
    _shape(cr, body, CLAY, 5)
    band(cr, [(-60, 104), (60, 104)], 10, GOLD, spacing=10, hole_r=2.0)
    _flower(cr, 0, 132, 14, GREEN, 6)


ASHVIN = man("ashvin", skin=AS_SKIN, bulk=0.95, dhoti=GREEN, border=SAFFRON, pleat=SAFFRON, sash=PALE, neck=GOLD,
             crown="tiara", halo=False, thread=True, hands=("open", "fist"))
register("ashvin_head", (-200, -380, 120, 110), ashvin_head)
register("ashvin_pouch", (-70, -100, 70, 130), _pouch)
ASHVIN.parts.insert(4, ("ashvin_pouch", "ashvin_body", (-104, -14), 0.12))     # behind the body, at the back hip
register("md_herb", (-60, -260, 60, 40), _herb)
register("md_medpot", (-70, -10, 70, 175), _medpot)


# ------------------------------------------------------------------ Mandhata


_MD_O = dict(skin=MD_SKIN, crown="tiara", hair=True, halo=False, moustache=True, tilak=True)


def mandhata_head(cr):
    """The emperor: a saffron sun-ray halo, a grand three-peaked gold crown with jewels and a red flare."""
    _ray_halo(cr, -30, -230, 140, 214, 14, (SAFFRON, GOLD))
    C.man_head(cr, _MD_O)
    R.kirita(cr, GOLD, None, tall=1.3, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.3
    for sx in (-1, 1):                                                          # side peaks
        _shape(cr, [(sx * 30, -170), (sx * 66, h(-250)), (sx * 52, h(-296)), (sx * 40, h(-246)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 50, h(-262), 8, GREEN)
    _jewel(cr, 2, h(-300), 10, BLUE)


def seat_legs(cr, skin, dhoti, border, b=1.0):
    """Legs of a seated figure (hip at 0, 0; the soles at y = +268): thighs forward, shins down; the far leg first."""
    for dx, dy, dk in ((-30, -8, 0.8), (0, 0, 1.0)):
        cr.save()
        cr.translate(dx, dy)
        dcol = tuple(c * dk for c in dhoti)
        shin = [(150 * b, 30), (196 * b, 30), (192 * b, 150), (186 * b, 236), (156 * b, 240), (150 * b, 150)]
        _shape(cr, shin, skin, 5)
        foot = [(150 * b, 228), (190 * b, 226), (214 * b, 242), (252 * b, 254), (254 * b, 268), (148 * b, 268)]
        _shape(cr, foot, skin, 4)
        band(cr, [(152 * b, 214), (190 * b, 214)], 9, GOLD, spacing=8, hole_r=2.0)
        th = [(-48, -24), (60, -36), (190 * b, -22), (216 * b, 26), (198 * b, 66), (60, 64), (-40, 56)]
        _shape(cr, th, dcol, 5)
        dots_in(cr, lambda: spath(cr, th), 19, 2.8)
        band(cr, [(196 * b, -18), (216 * b, 26), (200 * b, 62)], 14, border, spacing=11, hole_r=2.4)
        cr.restore()
    rivet(cr, 0, 0, 9)


def _sceptre(cr):
    """A gold sceptre topped by a wheel (the chakravarti's chakra); grip at 0, 0."""
    band(cr, [(0, 300), (0, -300)], 16, GOLD, spacing=22, hole_r=2.4)
    cr.new_path()
    cr.arc(0, -370, 64, 0, 2 * math.pi)
    leather(cr, GOLD, 5)
    cr.new_path()
    cr.arc(0, -370, 46, 0, 2 * math.pi)
    leather(cr, RED, 4)
    for i in range(8):
        a = math.pi * i / 4
        ink(cr, [(0, -370), (46 * math.cos(a), -370 + 46 * math.sin(a))], 5, smooth=False, col=GOLD)
    _jewel(cr, 0, -370, 12, BLUE)
    for i in range(12):
        a = 2 * math.pi * i / 12
        punch(cr, [(56 * math.cos(a), -370 + 56 * math.sin(a))], 3)


MANDHATA = man("mandhata", skin=MD_SKIN, bulk=1.15, dhoti=RED, border=GOLD, pleat=GOLD, sash=GREEN, neck=GOLD,
               crown="tiara", halo=False, thread=True, hands=("open", "fist"))
register("mandhata_head", (-270, -500, 210, 130), mandhata_head)
register("mandhata_seat", (-100, -60, 300, 290), lambda cr: seat_legs(cr, MD_SKIN, RED, GOLD, 1.0))
register("md_sceptre", (-80, -450, 80, 320), _sceptre)


# ------------------------------------------------------------------ props


def _kalasha(cr):
    """The clay kalasha of blessed water (pivot at the bottom centre, mouth at y = -318): a round belly with painted
    bands and a lotus, a red kalava thread at the neck, a flared rim."""
    body = [(-56, 0), (56, 0), (108, -40), (140, -110), (134, -184), (98, -234), (52, -258), (46, -284), (72, -300),
            (80, -318), (-80, -318), (-72, -300), (-46, -284), (-52, -258), (-98, -234), (-134, -184), (-140, -110),
            (-108, -40)]
    _shape(cr, body, CLAY, 6)
    for y, w, col in ((-176, 132, RED), (-60, 112, OCHRE)):
        band(cr, [(-w, y), (-w * 0.5, y + 6), (0, y + 8), (w * 0.5, y + 6), (w, y)], 14, col, spacing=12)
    for i in range(9):                                                           # a row of white dots
        x = -104 + 26 * i
        cr.new_path()
        cr.arc(x, -150 + 4 * math.sin(i), 5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _flower(cr, 0, -112, 30, GOLD, 8)
    for sx in (-1, 1):
        _flower(cr, sx * 76, -112, 16, PALE, 6)
    band(cr, [(-50, -266), (0, -262), (50, -266)], 12, RED, spacing=10, hole_r=2.0)      # kalava thread
    for sx in (-1, 1):
        ink(cr, [(sx * 20, -262), (sx * 30, -226), (sx * 22, -200)], 4, col=RED)
    cr.new_path()
    ell(cr, 0, -316, 74, 12)
    leather(cr, CLAY2, 4)
    ink(cr, [(-118, -150), (-126, -110), (-112, -62)], 3, col=CLAY2)
    rivet(cr, 0, -20, 6)


def _petal(cr, x0, y0, length, w, a, col, holes=None):
    """An almond-shaped petal from its base (x0, y0), pointing at angle a from straight up."""
    ux, uy = math.sin(a), -math.cos(a)
    px, py = math.cos(a), math.sin(a)
    P = lambda s_, t_: (x0 + ux * t_ + px * s_, y0 + uy * t_ + py * s_)
    _shape(cr, [P(0, 0), P(w, length * 0.42), P(w * 0.5, length * 0.8), P(0, length), P(-w * 0.5, length * 0.8),
                P(-w, length * 0.42)], col, 4, holes=holes)
    ink(cr, [P(0, length * 0.12), P(0, length * 0.8)], 2.5, col=LOTUS2)


def _lotus(cr):
    """A lotus pedestal (the baby stands at 0, 0, inside the cup): a fan of back petals, a row of front petals, a
    green pad under it."""
    _shape(cr, [(-230, 96), (-120, 72), (120, 72), (230, 96), (0, 130)], GREEN, 5)
    for i in range(5):                                                           # back petals
        a = -1.0 + 2.0 * i / 4
        _petal(cr, 0, 80, 190, 52, a, LOTUS2)
    for i in range(4):                                                           # front petals
        a = -1.25 + 2.5 * i / 3
        _petal(cr, 0, 96, 150, 60, a, LOTUS, holes=(9, 12, 2.2))
    _petal(cr, 0, 100, 120, 54, 0.0, LOTUS, holes=(9, 12, 2.2))
    band(cr, [(-120, 92), (0, 100), (120, 92)], 12, GOLD, spacing=11, hole_r=2.0)


def _throne(cr):
    """Mandhata's throne (pivot at the bottom centre; the cushion top at y = -246): a gold seat, an open arched back
    frame (so the emperor in front of it stays clear), lion-head arm rests."""
    _shape(cr, [(-270, 0), (270, 0), (256, -40), (-256, -40)], K.WOOD, 6, smooth=False, holes=(9, 15, 3))
    arch = [(-176, -230), (-186, -400), (-126, -520), (0, -570), (126, -520), (186, -400), (176, -230)]
    band(cr, arch, 34, GOLD, spacing=16, hole_r=3.2)
    band(cr, arch, 10, RED, holes=False)
    _flower(cr, 0, -584, 44, RED, 8)
    _jewel(cr, 0, -584, 14, GOLD)
    seat = [(-236, -40), (236, -40), (242, -204), (-242, -204)]
    _shape(cr, seat, GOLD, 7, smooth=False, holes=(11, 15, 3))
    dots_in(cr, lambda: poly(cr, [(-200, -70), (200, -70), (204, -180), (-204, -180)]), 24, 3.6, shape="d")
    _flower(cr, 0, -122, 40, RED, 8)
    cush = [(-214, -204), (214, -204), (224, -230), (204, -248), (-204, -248), (-224, -230)]
    _shape(cr, cush, PALE, 5)
    band(cr, [(-206, -218), (206, -218)], 10, GOLD, spacing=12, hole_r=2)
    for sx in (-1, 1):                                                           # lion-head arm rests
        x = sx * 254
        _shape(cr, [(x - 30, -40), (x + 30, -40), (x + 34, -270), (x - 34, -270)], OCHRE, 6, smooth=False)
        cr.new_path()
        cr.arc(x, -304, 50, 0, 2 * math.pi)
        leather(cr, SAFFRON, 6)
        for k in range(10):
            a = 2 * math.pi * k / 10
            punch(cr, [(x + 38 * math.cos(a), -304 + 38 * math.sin(a))], 3.6)
        _flower(cr, x, -304, 26, GOLD, 8)


def _world(cr):
    """The world strip (pivot at the middle of the horizon, y = 0): land with hills, small cities, a river."""
    land = [(-660, 30)]
    for i in range(23):
        x = -660 + 1320 * i / 22
        land.append((x, 10 - 14 * math.sin(i * 1.7) - 8 * math.sin(i * 0.6)))
    land += [(660, 30), (660, 240), (-660, 240)]
    _shape(cr, land, R.LAND, 6, smooth=False, holes=(12, 16, 3))
    for x, s in ((-520, 1.0), (-430, 1.3), (-200, 0.9), (60, 1.2), (150, 0.8), (380, 1.1), (500, 0.9)):
        _shape(cr, [(x - 50 * s, 10), (x, -46 * s), (x + 50 * s, 10)], OCHRE, 3.5, smooth=False)
        _shape(cr, [(x - 14 * s, -22 * s), (x, -46 * s), (x + 14 * s, -22 * s), (x, -30 * s)], PALE, 2,
               smooth=False)
    for pts in (((-600, 150), (-380, 120), (-120, 170), (120, 130), (360, 180), (620, 140)),):
        ink(cr, pts, 11, col=INK)
        ink(cr, pts, 6, col=BLUE)
    for x, col, dome, s in ((-320, OCHRE, GOLD, 0.8), (-60, (0.70, 0.58, 0.46), SAFFRON, 0.7), (250, OCHRE, RED, 0.8),
                            (560, (0.70, 0.58, 0.46), GOLD, 0.65)):
        cr.save()
        cr.translate(x, 96)
        cr.scale(s, s)
        K._city(cr, col, dome)
        cr.restore()
    for x, y in ((-560, 200), (-240, 210), (20, 214), (300, 222), (480, 206)):
        cr.new_path()
        cr.arc(x, y, 14, 0, 2 * math.pi)
        leather(cr, DGREEN, 3)


def _mat(cr):
    """A woven straw sleeping mat seen from the side (pivot at the middle of its top surface), rolled at one end."""
    _shape(cr, [(-460, 0), (430, 0), (440, 34), (-460, 34)], (0.93, 0.74, 0.40), 5, smooth=False)
    for i in range(46):
        x = -450 + 19.5 * i
        ink(cr, [(x, 2), (x + 12, 32)], 2.2, smooth=False, col=OCHRE)
    band(cr, [(-456, 30), (436, 30)], 8, RED, holes=False)
    cr.new_path()
    ell(cr, 452, 4, 40, 34)
    leather(cr, (0.93, 0.74, 0.40), 5)
    for r in (24, 12):
        cr.new_path()
        cr.arc(452, 4, r, 0, 2 * math.pi)
        cr.set_source_rgb(*OCHRE)
        cr.set_line_width(3)
        cr.stroke()


register("md_mat", (-470, -40, 500, 50), _mat)
register("md_kalasha", (-150, -330, 150, 10), _kalasha)
register("md_lotus", (-250, -120, 250, 140), _lotus)
register("md_throne", (-290, -640, 290, 10), _throne)
register("md_world", (-670, -80, 670, 250), _world)
