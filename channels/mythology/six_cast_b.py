"""The leather cast and props for builder B's parts of long video 1 (videos/six_stories.py, scenes_six_b): story 2, the
sage Mandavya, and story 5, Nachiketa. Togalu Gombeyaata style as in the reels (puppet_cast, ruru_cast, jayadratha_cast,
mandhata_cast...): profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather
puppets, modelled on no actor and no film. Every sprite name starts with "sb_" (the other builders' casts load in the
same process).

Cast (one look each, kept the same through the video):
  MANDAVYA     the silent sage: tan skin, dark matted hair piled high (jata) with rudraksha, a long dark-grey beard, ash
               lines, a saffron dhoti with a dark-red border, beads and the sacred thread on a bare chest. Faces: calm,
               sleep (meditating, eyes shut), angry, teach. Sits cross-legged (sb_mand_seat) or stands; a forearm with
               the index finger raised (sb_mand_armF_lo_hush) for the "silence" sign at the lips.
  THIEVES      masked silhouettes: near-black indigo cloth, a dark head wrap and a mask band with punched eye holes (the
               lamp light shows through them); each carries a lumpy loot sack (sb_sack, gold coins at its mouth).
  THE KING     warm skin, a curled moustache, a gold kirita with a red flare in front of a dark-red halo, a violet dhoti
               with a gold border, a saffron sash. Faces: calm, angry, shame. Kneels (sb_king_kneel).
  YAMA         ruru_cast.YAMA (dark blue-grey skin, gold crown, the danda), the same puppet in both stories; extra faces
               here (smile, shame) drawn the same way as rr_yama_head. His book of deeds: sb_ledger (closed, in his
               hand) and sb_ledger_open (open on a carved stand).
  THE CHILD    little Mandavya in the flashback: a boy with a big head, a small top-knot, a short dhoti; kneels on one
               knee (sb_kid_kneel). The insect: sb_bug.
  VIDURA       a calm, wise minister: warm skin, a short neat black beard, a low gold diadem, a cream dhoti and a blue
               sash. Calm, gentle smile.
  NACHIKETA    a boy of about ten: fair warm skin, a short hair cap and a top-knot, a cream dhoti with a saffron border and
               a saffron sash, the sacred thread. Faces: calm, smile, shock, shame. Sits cross-legged (sb_nachi_seat).
  VAJASHRAVAS  his father, a priest: grey hair with a top-knot, a grey beard, ash lines, a white dhoti with a red border, an
               ochre shawl and beads. Faces: calm, angry.
Props: the hermitage is lrekha_cast's leaf hut; a tall pointed wooden stake (an object only), Yama's hall (dark stone
pillars, gold bands, a buffalo-horn crest), Yama's great door, thin old cows, gold in a pot, an elephant, a plot of
land, an hourglass, a "silence" badge, coins.
"""
import math

import arjuna_cast as A
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (leaf hut, palm-leaf book, big leaf, speech cloud, palace)
import mandhata_cast as M  # noqa: F401  (straw mat, kalasha, world strip)
import ravana_cast as R
import ruru_cast as RU  # noqa: F401  (Yama, his danda, the mat, flowers)
import jayadratha_cast as J  # noqa: F401  (chariot, horses, Krishna and Arjuna, soldiers, spear, shield)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, man_body
from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, SAFFRON, SKIN,
                         VIOLET, almond_eye, band, cut, dots_in, ell, holes_line, ink, leather, poly, punch, register,
                         rivet, spath)

MD_SKIN = (0.88, 0.60, 0.38)          # Mandavya
MD_JATA = (0.36, 0.22, 0.12)
MD_BEARD = (0.40, 0.38, 0.40)
TH_SKIN = (0.40, 0.31, 0.30)          # the thieves
TH_CLOTH = (0.20, 0.18, 0.25)
TH_CLOTH2 = (0.34, 0.30, 0.40)
KG_SKIN = (0.98, 0.74, 0.50)          # the king
KG_DHOTI = VIOLET
SACK = (0.74, 0.55, 0.30)
SACK2 = (0.56, 0.38, 0.18)
WOOD = K.WOOD
STEEL = (0.62, 0.62, 0.70)
STONE = (0.42, 0.44, 0.54)            # Yama's hall and door
STONE2 = (0.30, 0.32, 0.42)
KID_SKIN = (1.0, 0.80, 0.58)
VD_SKIN = (0.93, 0.66, 0.42)          # Vidura
NC_SKIN = (1.0, 0.80, 0.58)           # Nachiketa
VJ_SKIN = (0.90, 0.62, 0.40)          # Vajashravas
GREY = (0.70, 0.70, 0.74)
COW = (0.93, 0.88, 0.76)
COW2 = (0.74, 0.66, 0.54)
ELE = (0.52, 0.52, 0.62)
ELE2 = (0.40, 0.40, 0.50)
SAND = (0.98, 0.80, 0.40)
LEDGER = (0.58, 0.12, 0.10)
PAGE = (0.99, 0.92, 0.72)
ASH_W = (1.0, 0.97, 0.9)
SEAT_H = 96.0                         # cross-legged: hip above the ground (as ruru_cast.SEAT_H)

# where the open ledger's pages are (design units, sb_ledger_open's pivot at the stand's foot)
LEDGER_PAGES = ((-150, -440), (150, -440))     # centres of the left / right page
LEDGER_PAGE_WH = (270, 330)


# ------------------------------------------------------------------ shared bits


def _ash(cr, x0=6, y0=-174, n=3, w=40):
    for k in range(n):
        ink(cr, [(x0, y0 + 9 * k), (x0 + w, y0 + 2 + 9 * k)], 3.2, col=ASH_W)


def _rudraksha(cr, x0, y0, n=7, step=14):
    for i in range(n):
        cr.new_path()
        cr.arc(x0 + step * i, y0, 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)


def _jata(cr, col, n=6, top=-196, step=29):
    """Matted hair piled up in rolls."""
    for k in range(n):
        cr.new_path()
        ell(cr, -8 - 3 * k, top - step * k, 54 - 5 * k, 23)
        leather(cr, col, 4)
        ink(cr, [(-44 + 6 * k, top - step * k), (-8, top + 10 - step * k), (30 - 6 * k, top - 2 - step * k)], 2.5)


def _seat(cr, cloth, border, skin):
    """Cross-legged in profile (hip at 0, 0; the ground at y = +SEAT_H), as ruru_cast._khag_seat."""
    th = [(-80, -30), (40, -44), (160, -32), (250, -10), (266, 40), (250, 86), (120, 96), (-40, 96), (-92, 70),
          (-96, 14)]
    _shape(cr, th, cloth, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(246, -8), (266, 40), (250, 86)], 14, border, spacing=11, hole_r=2.4)
    band(cr, [(-84, 88), (240, 90)], 10, border, holes=False)
    foot = [(104, 8), (150, -6), (204, 0), (222, 22), (196, 38), (118, 40)]
    _shape(cr, foot, skin, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 4), (x + 4, 18)], 2.2)
    rivet(cr, 0, 0, 9)


def _body_sit(o):
    def fn(cr):
        cr.save()
        cr.rectangle(-400, -600, 800, 664)
        cr.clip()
        man_body(cr, o)
        cr.restore()
    return fn


# ------------------------------------------------------------------ Mandavya


_MD_O = dict(skin=MD_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def mand_head(cr, mood="calm"):
    """Mandavya: dark hair down the back, a long dark-grey beard and moustache, dark matted hair piled high with
    rudraksha, ash lines."""
    hp = [(-30, -176), (-64, -146), (-90, -70), (-94, 30), (-72, 100), (-48, 60), (-40, -30), (-24, -100)]
    _shape(cr, hp, MD_JATA, 5)
    for k in range(3):
        holes_line(cr, [(-50 - 10 * k, -140), (-74 - 6 * k, -20), (-66 - 4 * k, 80)], 15, 2.3)
    RU.rface(cr, _MD_O, mood)
    bp = [(62, -50), (64, -22), (60, 30), (48, 110), (34, 150), (18, 96), (2, 30), (8, -40), (30, -54)]
    _shape(cr, bp, MD_BEARD, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -40), (44 - 12 * k, 30), (36 - 10 * k, 110)], 2.5, col=(0.62, 0.6, 0.62))
    m = [(66, -76), (46, -84), (24, -88), (12, -74), (30, -78), (52, -76), (68, -72)]
    _shape(cr, m, MD_BEARD, 3)
    _jata(cr, MD_JATA)
    _rudraksha(cr, -44, -178)
    if mood not in ("angry",):
        _ash(cr, 2, -174, 3, 44)


MAND = man("sb_mand", skin=MD_SKIN, bulk=0.92, dhoti=SAFFRON, border=DRED, pleat=DRED, sash=OCHRE, neck=BROWN,
           crown="tiara", halo=False, beads=True, thread=True, hair=False, earring=False, tilak=False,
           hands=("open", "open"))
for _m in ("calm", "sleep", "angry", "teach"):
    register("sb_mand_head" + ("" if _m == "calm" else "_" + _m), (-190, -400, 120, 190),
             (lambda m: lambda cr: mand_head(cr, m))(_m))
_MD_BODY = dict(skin=MD_SKIN, bulk=0.92, dhoti=SAFFRON, border=DRED, pleat=DRED, sash=OCHRE, neck=BROWN, beads=True,
                thread=True)
register("sb_mand_body_sit", (-200, -330, 140, 80), _body_sit(_MD_BODY))
register("sb_mand_seat", (-110, -60, 280, 110), lambda cr: _seat(cr, SAFFRON, DRED, MD_SKIN))


def _hush_forearm(cr, skin, b=0.92):
    """A forearm whose hand is a fist with the index finger raised straight on along the arm (the "silence" sign)."""
    pts = [(-19 * b, -6), (0, -22 * b), (19 * b, -6), (16 * b, 90), (13 * b, 128), (-13 * b, 128), (-16 * b, 90)]
    _shape(cr, pts, skin, 5)
    fing = [(-2, 140), (12, 140), (14, 200), (10, 216), (2, 216), (-2, 200)]
    _shape(cr, fing, skin, 3.5)
    cr.new_path()
    ell(cr, 2, 148, 22, 25)
    leather(cr, skin, 4)
    ink(cr, [(-12, 142), (12, 142)], 2.5)
    ink(cr, [(-12, 154), (12, 154)], 2.5)
    for y in (106, 118):
        band(cr, [(-15 * b, y), (15 * b, y + 2)], 8, BROWN, spacing=9, hole_r=2.0)
    rivet(cr, 0, 0, 6)


register("sb_mand_armF_lo_hush", (-45, -30, 45, 230), lambda cr: _hush_forearm(cr, MD_SKIN))


# ------------------------------------------------------------------ the thieves


_TH_O = dict(skin=TH_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def thief_head(cr):
    """A masked thief: a dark head wrap tied at the back (its ends flying), a mask band across the eyes with a punched
    eye hole (the lamp light shines through it)."""
    tails = [(-40, -130), (-120, -150), (-176, -120), (-120, -126), (-170, -86), (-104, -104), (-44, -100)]
    _shape(cr, tails, TH_CLOTH2, 4)
    A.face(cr, _TH_O, "angry")
    wrap = [(-58, -100), (-62, -150), (-44, -196), (0, -214), (44, -198), (60, -168), (62, -146), (20, -150),
            (-20, -146), (-40, -110)]
    _shape(cr, wrap, TH_CLOTH, 5)
    holes_line(cr, [(-46, -150), (-20, -190), (24, -196)], 14, 2.4)
    band(cr, [(-56, -150), (66, -142)], 12, TH_CLOTH2, spacing=12, hole_r=2.2)
    mask = [(-60, -134), (70, -136), (98, -122), (70, -96), (-60, -98)]
    _shape(cr, mask, (0.12, 0.10, 0.14), 4, smooth=False)
    punch(cr, [(36, -117)], 10)
    punch(cr, [(38, -119)], 7)
    cr.new_path()
    ell(cr, -60, -116, 16, 20)
    leather(cr, TH_CLOTH, 3)


THIEF = man("sb_thief", skin=TH_SKIN, bulk=0.98, dhoti=TH_CLOTH, border=TH_CLOTH2, pleat=TH_CLOTH2, sash=TH_CLOTH2,
            neck=TH_CLOTH2, crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=False,
            hands=("open", "open"))
register("sb_thief_head", (-200, -250, 120, 40), thief_head)


def _sack(cr):
    """A lumpy loot sack (pivot at its bottom centre): burlap with a patch, tied at the neck, gold coins at its mouth."""
    for x, y in ((-30, -300), (8, -312), (40, -296), (-6, -290)):
        cr.new_path()
        ell(cr, x, y, 26, 12)
        leather(cr, GOLD, 3.5)
        punch(cr, [(x, y)], 3.5)
    body = [(-40, -270), (-100, -230), (-140, -150), (-150, -60), (-120, -6), (0, 6), (120, -6), (150, -60),
            (140, -150), (100, -230), (40, -270)]
    _shape(cr, body, SACK, 6, holes=(12, 16, 2.6))
    for pts in (((-90, -200), (-60, -120), (-70, -30)), ((60, -210), (80, -120), (64, -30))):
        ink(cr, pts, 3, col=SACK2)
    patch = [(10, -140), (80, -150), (86, -80), (16, -70)]
    _shape(cr, patch, SACK2, 3.5, smooth=False)
    for k in range(4):
        ink(cr, [(14 + 18 * k, -146), (20 + 18 * k, -76)], 2, smooth=False, col=INK)
    neck = [(-46, -266), (46, -266), (34, -240), (-34, -240)]
    _shape(cr, neck, SACK2, 4, smooth=False)
    band(cr, [(-40, -252), (40, -252)], 12, BROWN, holes=False)
    _shape(cr, [(30, -256), (70, -280), (76, -262), (40, -246)], BROWN, 3)


register("sb_sack", (-160, -340, 160, 20), _sack)


def _coin(cr):
    cr.new_path()
    ell(cr, 0, 0, 26, 26)
    leather(cr, GOLD, 4)
    cr.new_path()
    ell(cr, 0, 0, 16, 16)
    cr.set_source_rgb(*INK)
    cr.set_line_width(2.5)
    cr.stroke()
    punch(cr, [(0, 0)], 4)


register("sb_coin", (-32, -32, 32, 32), _coin)


# ------------------------------------------------------------------ the king


_KG_O = dict(skin=KG_SKIN, hair=True, moustache=True, tilak=True, earring=True)


def king_head(cr, mood="calm"):
    K._halo(cr, DRED)
    A.face(cr, _KG_O, mood)
    ink(cr, [(20, -88), (8, -78), (14, -66)], 5, col=HAIR)                      # the moustache's curl
    R.kirita(cr, GOLD, None, tall=1.12, flare=RED)
    _jewel(cr, -12, -72, 15, GOLD)


KING = man("sb_king", skin=KG_SKIN, bulk=1.1, dhoti=KG_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
           crown="tiara", halo=False, moustache=True, hands=("open", "open"))
for _m in ("calm", "angry", "shame"):
    register("sb_king_head" + ("" if _m == "calm" else "_" + _m), (-200, -430, 120, 110),
             (lambda m: lambda cr: king_head(cr, m))(_m))
register("sb_king_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, KG_SKIN, KG_DHOTI, GOLD, 1.1))


# ------------------------------------------------------------------ the stake (an object only)


def _stake(cr):
    """A tall wooden stake (pivot at the bottom centre): a stone block for a base, a rough pole bound with rope, an
    iron point at the top. Only ever shown as an object."""
    base = [(-150, 0), (150, 0), (130, -90), (-130, -90)]
    _shape(cr, base, (0.56, 0.54, 0.58), 6, smooth=False, holes=(10, 18, 3))
    pole = [(-34, -86), (34, -86), (28, -900), (22, -1000), (-22, -1000), (-28, -900)]
    _shape(cr, pole, WOOD, 6, smooth=False)
    for k in range(4):
        ink(cr, [(-14 + 9 * k, -110), (-12 + 8 * k, -500), (-10 + 7 * k, -960)], 2.5, col=(0.36, 0.20, 0.08))
    for y in (-300, -620):
        band(cr, [(-34, y), (34, y - 10)], 16, (0.86, 0.70, 0.40), holes=False, lw=3)
        band(cr, [(-34, y + 18), (34, y + 8)], 16, (0.86, 0.70, 0.40), holes=False, lw=3)
    tip = [(-24, -996), (24, -996), (0, -1150)]
    _shape(cr, tip, STEEL, 5, smooth=False)
    band(cr, [(-26, -1000), (26, -1000)], 14, (0.40, 0.40, 0.48), holes=False)


register("sb_stake", (-160, -1170, 160, 10), _stake)


# ------------------------------------------------------------------ Yama: more faces, the book of deeds


_YM_O = dict(skin=RU.YM_SKIN, hair=True, moustache=True, tilak=True)


def yama_head(cr, mood="calm"):
    """ruru_cast.yama_head with a mood (smile | shame | teach); the crown, halo and moustache exactly as there."""
    K._halo(cr, DRED)
    RU.rface(cr, _YM_O, mood)
    ink(cr, [(20, -88), (8, -78), (14, -66)], 5, col=HAIR)
    R.kirita(cr, GOLD, None, tall=1.36, flare=RED)
    h = lambda y: -150 + (y + 150) * 1.36
    for sx in (-1, 1):
        _shape(cr, [(sx * 30, -170), (sx * 66, h(-240)), (sx * 52, h(-290)), (sx * 40, h(-240)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
        _jewel(cr, sx * 50, h(-254), 7, RED)
    _jewel(cr, 2, h(-292), 10, (0.16, 0.66, 0.40))


for _m in ("smile", "shame", "teach"):
    register("sb_yama_head_" + _m, (-230, -530, 140, 120), (lambda m: lambda cr: yama_head(cr, m))(_m))


def _scales_emblem(cr, x, y, s=1.0):
    """A small balance (the emblem on the book of deeds)."""
    ink(cr, [(x, y - 40 * s), (x, y + 40 * s)], 5 * s, smooth=False, col=INK)
    ink(cr, [(x - 50 * s, y - 30 * s), (x + 50 * s, y - 30 * s)], 5 * s, smooth=False, col=INK)
    for sx in (-1, 1):
        cx = x + sx * 50 * s
        ink(cr, [(cx, y - 30 * s), (cx - 18 * s, y + 6 * s)], 2.5 * s, smooth=False, col=INK)
        ink(cr, [(cx, y - 30 * s), (cx + 18 * s, y + 6 * s)], 2.5 * s, smooth=False, col=INK)
        cr.new_path()
        cr.move_to(cx - 24 * s, y + 6 * s)
        cr.curve_to(cx - 18 * s, y + 24 * s, cx + 18 * s, y + 24 * s, cx + 24 * s, y + 6 * s)
        cr.close_path()
        leather(cr, GOLD, 3 * s)
    cr.new_path()
    ell(cr, x, y + 44 * s, 24 * s, 8 * s)
    leather(cr, GOLD, 3 * s)


def _ledger(cr):
    """Yama's book of deeds, closed (centre pivot): a thick dark-red cover, gold corners and spine bands, a gold
    balance on the front."""
    w, h = 130, 170
    _shape(cr, [(-w + 10, -h + 10), (w + 18, -h + 10), (w + 18, h + 12), (-w + 10, h + 12)], PAGE, 5, smooth=False)
    for y in range(-h + 24, h, 14):
        ink(cr, [(w + 2, y), (w + 16, y)], 1.8, smooth=False, col=(0.7, 0.6, 0.45))
    cover = [(-w, -h), (w, -h), (w, h), (-w, h)]
    _shape(cr, cover, LEDGER, 6, smooth=False, holes=(12, 15, 2.6))
    for sx in (-1, 1):
        for sy in (-1, 1):
            _shape(cr, [(sx * w, sy * h), (sx * (w - 50), sy * h), (sx * w, sy * (h - 50))], GOLD, 3.5, smooth=False)
    band(cr, [(-w + 26, -h), (-w + 26, h)], 14, GOLD, spacing=12, hole_r=2.2)
    cr.new_path()
    ell(cr, 10, 0, 70, 82)
    leather(cr, (0.80, 0.30, 0.16), 4)
    _scales_emblem(cr, 10, -6, 0.9)


register("sb_ledger", (-150, -190, 160, 200), _ledger)


def _ledger_open(cr):
    """The book of deeds lying open on a carved wooden stand (pivot at the stand's foot): two pale pages with faint
    ruled lines (the scenes write on them), a dark-red cover showing round the pages."""
    for sg in (1, -1):                                                            # a carved X-shaped stand
        _shape(cr, [(-sg * 214, -246), (-sg * 182, -262), (sg * 164, 0), (sg * 120, 0)],
               WOOD if sg > 0 else (0.48, 0.28, 0.12), 5, smooth=False, holes=(9, 22, 2.6))
    pw, ph = LEDGER_PAGE_WH
    cx = LEDGER_PAGES[0][1]
    cover = [(-pw - 34, cx - ph / 2 - 20), (pw + 34, cx - ph / 2 - 20), (pw + 40, cx + ph / 2 + 26),
             (-pw - 40, cx + ph / 2 + 26)]
    _shape(cr, cover, LEDGER, 6, smooth=False, holes=(11, 16, 2.6))
    for (px, py) in LEDGER_PAGES:
        sgn = -1 if px < 0 else 1
        pts = [(px - pw / 2 - 8, py - ph / 2), (px + pw / 2 + 8, py - ph / 2), (px + pw / 2 + 12, py + ph / 2),
               (px - pw / 2 - 12, py + ph / 2)]
        if sgn < 0:
            pts[1] = (px + pw / 2 + 8, py - ph / 2 + 10)
            pts[2] = (px + pw / 2 + 12, py + ph / 2 + 6)
        else:
            pts[0] = (px - pw / 2 - 8, py - ph / 2 + 10)
            pts[3] = (px - pw / 2 - 12, py + ph / 2 + 6)
        _shape(cr, pts, PAGE, 4, smooth=False)
        for k in range(10):
            y = py - ph / 2 + 60 + 26 * k
            ink(cr, [(px - pw / 2 + 14, y), (px + pw / 2 - 14, y)], 1.6, smooth=False, col=(0.80, 0.68, 0.48))
    ink(cr, [(0, cx - ph / 2 + 6), (0, cx + ph / 2 + 4)], 4, smooth=False)
    _shape(cr, [(-14, cx + ph / 2 + 20), (14, cx + ph / 2 + 20), (8, cx + ph / 2 + 110), (0, cx + ph / 2 + 96),
                (-8, cx + ph / 2 + 110)], RED, 3, smooth=False)                 # a ribbon marker


register("sb_ledger_open", (-330, -660, 330, 10), _ledger_open)


# ------------------------------------------------------------------ Yama's hall


def _horns(cr, x, y, s=1.0, col=GOLD):
    """A buffalo-horn crest (Yama's mount) around a round boss."""
    for sx in (-1, 1):
        hp = [(x + sx * 40 * s, y + 10 * s), (x + sx * 130 * s, y - 20 * s), (x + sx * 190 * s, y - 90 * s),
              (x + sx * 200 * s, y - 150 * s), (x + sx * 170 * s, y - 100 * s), (x + sx * 120 * s, y - 52 * s),
              (x + sx * 40 * s, y - 30 * s)]
        _shape(cr, hp, col, 5 * s)
        holes_line(cr, [(x + sx * 60 * s, y - 6 * s), (x + sx * 140 * s, y - 40 * s), (x + sx * 182 * s, y - 104 * s)],
                   18 * s, 2.6 * s)
    cr.new_path()
    ell(cr, x, y - 14 * s, 54 * s, 50 * s)
    leather(cr, (0.80, 0.30, 0.16), 5 * s)
    _jewel(cr, x, y - 14 * s, 22 * s, GOLD)


def _pillar(cr, x, h, w=70):
    _shape(cr, [(x - w, 0), (x + w, 0), (x + w - 14, -60), (x - w + 14, -60)], STONE2, 5, smooth=False)
    _shape(cr, [(x - w + 22, -60), (x + w - 22, -60), (x + w - 30, -h + 80), (x - w + 30, -h + 80)], STONE, 5,
           smooth=False, holes=(12, 22, 3))
    for k in range(4):
        y = -160 - (h - 300) * k / 3
        band(cr, [(x - w + 26, y), (x + w - 26, y)], 18, GOLD, spacing=13, hole_r=2.4)
    _shape(cr, [(x - w, -h + 80), (x + w, -h + 80), (x + w + 16, -h + 20), (x - w - 16, -h + 20)], STONE2, 5,
           smooth=False)
    _shape(cr, [(x - w - 26, -h + 20), (x + w + 26, -h + 20), (x + w + 26, -h - 10), (x - w - 26, -h - 10)], GOLD, 4,
           smooth=False)


def _yhall(cr):
    """Yama's hall (pivot at the bottom centre, 2300 wide): four dark stone pillars with gold bands, a wide cusped arch
    between the middle pair, a buffalo-horn crest, two hanging lamps, a low stepped dais."""
    H_ = 1040
    for x in (-1050, -620, 620, 1050):
        _pillar(cr, x, H_, 62 if abs(x) > 900 else 74)
    beam = [(-1120, -H_ - 10), (1120, -H_ - 10), (1120, -H_ - 90), (-1120, -H_ - 90)]
    _shape(cr, beam, STONE2, 6, smooth=False, holes=(12, 20, 3.2))
    band(cr, [(-1120, -H_ - 50), (1120, -H_ - 50)], 16, GOLD, spacing=14)
    # the cusped arch between the inner pillars
    arch = [(-560, -H_ - 10)]
    n = 9
    for i in range(n + 1):
        a = math.pi * i / n
        r = 560
        x = -r * math.cos(a)
        y = -H_ + 300 - 340 * math.sin(a)
        arch.append((x, y + (24 if i % 2 else 0)))
    arch += [(560, -H_ - 10)]
    _shape(cr, arch, STONE2, 6, smooth=False, holes=(10, 18, 3))
    ink(cr, [(-520, -H_ + 290), (-300, -H_ + 30), (0, -H_ - 40), (300, -H_ + 30), (520, -H_ + 290)], 6, col=GOLD)
    _horns(cr, 0, -H_ - 120, 1.2)
    for x in (-330, 330):                                                         # hanging lamps
        ink(cr, [(x, -H_ + 60), (x, -H_ + 330)], 3, smooth=False)
        _shape(cr, [(x - 40, -H_ + 330), (x + 40, -H_ + 330), (x + 22, -H_ + 360), (x - 22, -H_ + 360)], GOLD, 4,
               smooth=False)
        _shape(cr, [(x - 10, -H_ + 330), (x, -H_ + 290), (x + 10, -H_ + 330)], (1.0, 0.70, 0.20), 2.5)
    dais = [(-900, 0), (900, 0), (860, -40), (-860, -40)]
    _shape(cr, dais, STONE2, 5, smooth=False, holes=(10, 20, 3))


register("sb_yhall", (-1160, -1360, 1160, 10), _yhall)


# ------------------------------------------------------------------ the child in the flashback, the insect


_KID_O = dict(skin=KID_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def kid_head(cr):
    """Little Mandavya: a round young face, a small top-knot, a short hair cap."""
    RU.rface(cr, _KID_O, "calm")
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -186), (24, -188), (-8, -182),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, HAIR, 4)
    cr.new_path()
    ell(cr, -16, -222, 26, 20, -0.2)
    leather(cr, HAIR, 4)
    holes_line(cr, [(-48, -130), (-40, -176), (0, -200)], 15, 2.4)


KID = man("sb_kid", skin=KID_SKIN, bulk=0.85, dhoti=(0.96, 0.82, 0.50), border=RED, pleat=(0.96, 0.82, 0.50),
          sash=RED, neck=GOLD, crown="tiara", halo=False, hair=False, earring=False, tilak=False,
          hands=("fist", "open"))
register("sb_kid_head", (-130, -250, 110, 30), kid_head)
register("sb_kid_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, KID_SKIN, (0.96, 0.82, 0.50), RED, 0.85))


def _bug(cr):
    """A little insect (a grasshopper-like bug, facing +x, pivot under its belly)."""
    for k, (x0, x1) in enumerate(((-40, -70), (0, -10), (30, 50))):
        ink(cr, [(x0, -20), (x0 - 20 + 10 * k, -4), (x1, 18)], 4)
    ink(cr, [(-60, -34), (-110, -70), (-130, 4)], 5)                              # the big hind leg
    body = [(-90, -30), (-40, -52), (30, -50), (70, -36), (64, -14), (-20, -10), (-84, -14)]
    _shape(cr, body, GREEN, 4)
    holes_line(cr, [(-70, -28), (0, -34), (50, -32)], 12, 2.2)
    cr.new_path()
    ell(cr, 82, -38, 24, 20)
    leather(cr, (0.50, 0.74, 0.30), 4)
    cr.new_path()
    cr.arc(90, -42, 7, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    ink(cr, [(92, -56), (120, -100), (150, -110)], 2.5)
    ink(cr, [(86, -56), (100, -104), (124, -126)], 2.5)


register("sb_bug", (-140, -130, 160, 30), _bug)


# ------------------------------------------------------------------ Vidura


_VD_O = dict(skin=VD_SKIN, hair=True, moustache=True, beard=True, tilak=True, earring=True)


def vidura_head(cr, mood="calm"):
    """Vidura: a short neat black beard, a low gold diadem with three small points, a calm look."""
    A.face(cr, _VD_O, mood)
    dia = [(-50, -150), (-46, -176), (-20, -186), (0, -212), (20, -188), (44, -180), (54, -152)]
    _shape(cr, dia, GOLD, 4, smooth=False, holes=(8, 12, 2.2))
    band(cr, [(-52, -156), (58, -150)], 15, GOLD, spacing=11)
    _jewel(cr, 2, -184, 9, BLUE)
    _jewel(cr, -12, -72, 12, GOLD)


VIDURA = man("sb_vidura", skin=VD_SKIN, bulk=1.0, dhoti=PALE, border=BLUE, pleat=BLUE, sash=BLUE, neck=GOLD,
             crown="tiara", halo=False, thread=True, hands=("open", "open"))
for _m in ("calm", "smile"):
    register("sb_vidura_head" + ("" if _m == "calm" else "_" + _m), (-190, -300, 120, 110),
             (lambda m: lambda cr: vidura_head(cr, m))(_m))


# ------------------------------------------------------------------ Nachiketa and his father


_NC_O = dict(skin=NC_SKIN, hair=False, moustache=False, tilak=True, earring=False)


def nachi_head(cr, mood="calm"):
    """Nachiketa: a young face, a short hair cap and a top-knot, a small tilak."""
    RU.rface(cr, _NC_O, mood)
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -186), (24, -188), (-8, -182),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, HAIR, 4)
    holes_line(cr, [(-50, -130), (-40, -176), (0, -200)], 15, 2.4)
    cr.new_path()
    ell(cr, -14, -230, 32, 24, -0.15)
    leather(cr, HAIR, 4)
    band(cr, [(-36, -212), (10, -210)], 9, SAFFRON, spacing=9, hole_r=2.0)


NACHI = man("sb_nachi", skin=NC_SKIN, bulk=0.84, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=SAFFRON, neck=GOLD,
            crown="tiara", halo=False, thread=True, hair=False, earring=False, tilak=False, hands=("open", "open"))
for _m in ("calm", "smile", "shock", "shame"):
    register("sb_nachi_head" + ("" if _m == "calm" else "_" + _m), (-130, -270, 120, 40),
             (lambda m: lambda cr: nachi_head(cr, m))(_m))
_NC_BODY = dict(skin=NC_SKIN, bulk=0.84, dhoti=PALE, border=SAFFRON, pleat=SAFFRON, sash=SAFFRON, neck=GOLD,
                thread=True)
register("sb_nachi_body_sit", (-200, -330, 140, 80), _body_sit(_NC_BODY))
register("sb_nachi_seat", (-110, -60, 280, 110), lambda cr: _seat(cr, PALE, SAFFRON, NC_SKIN))

_VJ_O = dict(skin=VJ_SKIN, hair=False, moustache=False, tilak=False, earring=False)


def vaja_head(cr, mood="calm"):
    """Vajashravas, the priest: grey hair down the back and a grey top-knot, a grey beard and moustache, ash lines."""
    hp = [(-30, -176), (-62, -146), (-86, -80), (-90, 0), (-74, 50), (-50, 40), (-40, -30), (-24, -100)]
    _shape(cr, hp, GREY, 5)
    RU.rface(cr, _VJ_O, mood)
    bp = [(60, -50), (64, -24), (58, 20), (44, 70), (24, 50), (4, 10), (8, -40), (30, -52)]
    _shape(cr, bp, GREY, 4)
    for k in range(3):
        ink(cr, [(46 - 10 * k, -40), (42 - 12 * k, 0), (36 - 10 * k, 50)], 2.4, col=(0.5, 0.5, 0.54))
    dy = 4 if mood == "angry" else 0
    m = [(66, -76 + dy), (46, -84 + dy), (24, -88 + dy), (12, -74 + dy), (30, -78 + dy), (52, -76 + dy), (68, -72 + dy)]
    _shape(cr, m, GREY, 3)
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -210), (42, -198), (54, -184), (24, -186), (-8, -180),
           (-34, -158), (-42, -116)]
    _shape(cr, cap, GREY, 4)
    cr.new_path()
    ell(cr, -18, -226, 30, 22, -0.2)
    leather(cr, GREY, 4)
    _rudraksha(cr, -44, -204, 6, 13)
    _ash(cr, 4, -172, 3, 42)
    cr.new_path()
    cr.arc(30, -150, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


VAJA = man("sb_vaja", skin=VJ_SKIN, bulk=1.04, dhoti=PALE, border=DRED, pleat=DRED, sash=OCHRE, neck=BROWN,
           crown="tiara", halo=False, thread=True, beads=True, robe=(1.0, 0.80, 0.46), hair=False, earring=False,
           tilak=False, hands=("open", "open"))
for _m in ("calm", "angry", "smile"):
    register("sb_vaja_head" + ("" if _m == "calm" else "_" + _m), (-130, -270, 120, 90),
             (lambda m: lambda cr: vaja_head(cr, m))(_m))


# ------------------------------------------------------------------ thin old cows


def _cow(cr, head_down=0.0):
    """A thin old cow facing +x (pivot on the ground under its middle), an Indian cow with a hump: a bony back and
    hips, ribs showing, thin legs with knobbly knees, a dewlap, a drooping head with curved horns and a tired eye."""
    bone = (0.55, 0.46, 0.36)
    for x0, x1 in ((-236, -250), (150, 158)):                                     # far legs, darker
        leg = [(x0 - 15, -350), (x0 + 15, -350), (x0 + 10, -180), (x1 + 8, -20), (x1 + 12, 0), (x1 - 14, 0),
               (x1 - 8, -20), (x0 - 11, -180)]
        _shape(cr, leg, COW2, 4, smooth=False)
    tail = [(-336, -500), (-360, -380), (-362, -250), (-350, -244), (-346, -380), (-324, -490)]
    _shape(cr, tail, COW, 3.5)
    _shape(cr, [(-372, -262), (-344, -262), (-340, -196), (-356, -180), (-376, -200)], (0.46, 0.38, 0.30), 3)
    body = [(-340, -500), (-300, -592), (-240, -574), (-140, -548), (0, -552), (100, -572), (160, -640), (222, -632),
            (262, -578), (282, -500), (272, -420), (232, -372), (120, -350), (-20, -336), (-160, -352), (-262, -384),
            (-330, -432)]
    _shape(cr, body, COW, 6)
    for k in range(5):                                                            # the ribs
        x = -90 + 46 * k
        ink(cr, [(x - 4, -540), (x + 10, -480), (x + 2, -410), (x - 14, -360)], 3.5, col=bone)
    ink(cr, [(-306, -588), (-270, -520), (-300, -452)], 4, col=bone)              # the hip bone
    ink(cr, [(-240, -572), (-210, -540)], 3, col=bone)
    ink(cr, [(208, -626), (196, -540), (220, -470)], 3.5, col=bone)                # shoulder
    for (x, y, rx, ry) in ((-170, -470, 46, 30), (60, -470, 34, 24)):              # pale patches
        cr.new_path()
        ell(cr, x, y, rx, ry, 0.3)
        cr.set_source_rgb(*COW2)
        cr.fill()
    holes_line(cr, [(-280, -572), (-120, -540), (60, -556), (170, -620)], 22, 3.0)
    for x0, x1 in ((-276, -290), (196, 206)):                                     # near legs
        leg = [(x0 - 17, -380), (x0 + 17, -380), (x0 + 11, -186), (x1 + 9, -20), (x1 + 13, 0), (x1 - 13, 0),
               (x1 - 9, -20), (x0 - 11, -186)]
        _shape(cr, leg, COW, 4.5, smooth=False)
        cr.new_path()
        ell(cr, (x0 + x1) / 2 - 2, -184, 16, 14)                                   # knobbly knee
        leather(cr, COW, 3)
        _shape(cr, [(x1 - 15, -2), (x1 + 15, -2), (x1 + 17, 10), (x1 - 17, 10)], (0.30, 0.24, 0.20), 3, smooth=False)
    cr.save()                                                                     # neck and head, drooping
    cr.translate(258, -560)
    cr.rotate(0.42 * head_down)
    dew = [(-10, 40), (20, 120), (60, 160), (100, 130), (130, 50)]
    _shape(cr, dew, COW, 4)
    ink(cr, [(20, 70), (50, 120), (70, 140)], 2.6, col=bone)
    neck = [(-30, -40), (60, -52), (130, -16), (156, 40), (110, 72), (30, 80), (-30, 60)]
    _shape(cr, neck, COW, 5)
    for hx, col in ((118, COW2), (138, PALE)):                                     # curved horns
        _shape(cr, [(hx - 10, -40), (hx + 10, -44), (hx + 16, -90), (hx - 2, -128), (hx - 10, -118), (hx, -88)],
               col, 3)
    ear = [(110, -10), (50, -30), (20, -12), (54, 6), (110, 8)]
    _shape(cr, ear, COW2, 3.5)
    head = [(100, -40), (156, -52), (192, -14), (240, 64), (264, 108), (252, 140), (210, 142), (168, 104),
            (120, 40), (96, 0)]
    _shape(cr, head, COW, 5)
    cr.new_path()
    ell(cr, 244, 124, 24, 20, 0.5)
    leather(cr, (0.80, 0.62, 0.58), 4)
    punch(cr, [(252, 118)], 4)
    ink(cr, [(150, 12), (168, 22), (186, 16)], 4)                                 # a tired, half-shut eye
    ink(cr, [(150, 2), (170, 4), (188, 0)], 2.5)
    ink(cr, [(140, 40), (160, 60)], 2.2, col=bone)
    cr.restore()


register("sb_cow", (-400, -720, 560, 20), lambda cr: _cow(cr, 0.0))
register("sb_cow_low", (-400, -720, 560, 140), lambda cr: _cow(cr, 1.0))


# ------------------------------------------------------------------ Yama's gifts


def _gold(cr):
    """Gold: a round pot heaped with coins (pivot at the bottom centre), coins spilling."""
    pot = [(-150, -200), (150, -200), (190, -120), (170, -30), (100, 0), (-100, 0), (-170, -30), (-190, -120)]
    for i in range(16):
        x = -130 + 260 * ((i * 0.618) % 1.0)
        y = -220 - 70 * math.sin(math.pi * (x + 130) / 260) + 10 * (i % 3)
        cr.new_path()
        ell(cr, x, y, 32, 14)
        leather(cr, GOLD, 3.5)
        punch(cr, [(x, y)], 3)
    _shape(cr, pot, (0.76, 0.42, 0.18), 6, holes=(12, 17, 3))
    band(cr, [(-160, -190), (160, -190)], 22, GOLD, spacing=13)
    for k, x in enumerate((-60, 0, 60)):
        _flower(cr, x, -100, 20, GOLD if k % 2 == 0 else RED, 8)
    for x, y in ((210, -14), (250, -6), (-220, -10)):
        cr.new_path()
        ell(cr, x, y, 28, 12)
        leather(cr, GOLD, 3)


register("sb_gold", (-280, -320, 280, 20), _gold)


def _elephant(cr):
    """An elephant facing +x (pivot on the ground under its middle) in a red and gold caparison, a gold headpiece."""
    for x in (-210, 170):                                                         # far legs
        _shape(cr, [(x - 50, -330), (x + 50, -330), (x + 46, 0), (x - 46, 0)], ELE2, 5, smooth=False)
    body = [(-330, -380), (-300, -560), (-150, -660), (60, -670), (220, -620), (300, -520), (300, -360), (220, -280),
            (-260, -280)]
    _shape(cr, body, ELE, 7)
    _shape(cr, [(-336, -420), (-380, -300), (-372, -250), (-356, -300), (-330, -380)], ELE, 4)   # tail
    cap = [(-200, -640), (120, -650), (160, -400), (60, -320), (-200, -320), (-250, -420)]
    _shape(cr, cap, RED, 6, holes=(12, 16, 3))
    dots_in(cr, lambda: spath(cr, cap), 30, 4, shape="d")
    band(cr, [(-246, -400), (-200, -330), (60, -326), (156, -396)], 22, GOLD, spacing=13)
    for x in (-250, 130):                                                         # near legs
        _shape(cr, [(x - 56, -320), (x + 56, -320), (x + 52, 0), (x - 52, 0)], ELE, 6, smooth=False)
        for k in range(3):
            ink(cr, [(x - 40, -40 - 12 * k), (x + 40, -40 - 12 * k)], 2.5, smooth=False)
        band(cr, [(x - 54, -70), (x + 54, -70)], 12, GOLD, spacing=10, hole_r=2.2)
    head = [(220, -620), (330, -690), (420, -650), (450, -540), (440, -420), (380, -360), (300, -380)]
    _shape(cr, head, ELE, 7)
    trunk = [(420, -470), (450, -380), (470, -250), (500, -150), (530, -110), (510, -90), (470, -140), (436, -240),
             (400, -380), (380, -440)]
    _shape(cr, trunk, ELE, 6)
    for k in range(6):
        y = -400 + 50 * k
        ink(cr, [(404 + 10 * k, y), (444 + 12 * k, y + 8)], 2.5, smooth=False)
    _shape(cr, [(380, -410), (440, -400), (500, -370), (540, -380), (520, -350), (430, -370), (370, -380)], PALE, 4)
    ear = [(250, -640), (180, -600), (160, -480), (200, -400), (270, -420), (300, -520)]
    _shape(cr, ear, ELE2, 5, holes=(10, 15, 2.6))
    _shape(cr, [(260, -690), (340, -720), (420, -680), (400, -640), (300, -640)], GOLD, 4, holes=(8, 12, 2.4))
    _jewel(cr, 350, -680, 12, RED)
    cr.new_path()
    cr.arc(370, -560, 10, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(373, -563)], 3)


register("sb_elephant", (-400, -740, 560, 20), _elephant)


def _land(cr):
    """A plot of land (pivot at the bottom centre): a green field in rows, boundary stones, a small tree."""
    field = [(-300, 0), (300, 0), (240, -150), (-240, -150)]
    _shape(cr, field, (0.46, 0.66, 0.26), 6, smooth=False, holes=(10, 18, 3))
    for k in range(6):
        u = (k + 0.5) / 6
        ink(cr, [(-300 + 600 * u, 0), (-240 + 480 * u, -150)], 3, smooth=False, col=DGREEN)
        for j in range(4):
            v = (j + 0.5) / 4
            x = (-300 + 600 * u) * (1 - v) + (-240 + 480 * u) * v
            y = -150 * v
            _shape(cr, [(x - 8, y), (x, y - 26), (x + 8, y)], (0.80, 0.80, 0.30), 2, smooth=False)
    for x in (-300, -100, 100, 300):
        cr.new_path()
        ell(cr, x, -2, 20, 14)
        leather(cr, (0.70, 0.68, 0.66), 3)
    _shape(cr, [(206, -150), (226, -150), (222, -260), (210, -260)], BROWN, 3, smooth=False)
    cr.new_path()
    ell(cr, 216, -300, 60, 52)
    leather(cr, DGREEN, 4)
    punch(cr, [(200, -310), (230, -290), (214, -320)], 4)


register("sb_land", (-320, -370, 320, 20), _land)


def _hourglass(cr):
    """An hourglass (pivot at the bottom centre): carved wooden ends, glass bulbs, gold sand."""
    for y in (0, -360):
        _shape(cr, [(-120, y), (120, y), (110, y - 30), (-110, y - 30)], WOOD, 5, smooth=False)
    for x in (-96, 96):
        _shape(cr, [(x - 9, -30), (x + 9, -30), (x + 9, -330), (x - 9, -330)], WOOD, 3, smooth=False)
    glass = [(-76, -330), (76, -330), (70, -250), (12, -186), (12, -174), (70, -110), (76, -30), (-76, -30),
             (-70, -110), (-12, -174), (-12, -186), (-70, -250)]
    _shape(cr, glass, (0.88, 0.94, 0.98), 4, smooth=False)
    _shape(cr, [(-50, -300), (50, -300), (12, -200), (-12, -200)], SAND, 2.5, smooth=False)
    _shape(cr, [(-70, -34), (70, -34), (36, -90), (0, -104), (-36, -90)], SAND, 2.5, smooth=False)
    ink(cr, [(0, -186), (0, -100)], 3, smooth=False, col=(0.86, 0.62, 0.20))


register("sb_hourglass", (-130, -400, 130, 10), _hourglass)


# ------------------------------------------------------------------ Yama's door


def _door(cr):
    """Yama's great door (pivot at the bottom centre): a tall stone arch with gold trim, two closed doors of dark wood
    studded with iron, big ring handles, a buffalo-horn crest, two steps."""
    _shape(cr, [(-520, 0), (520, 0), (490, -50), (-490, -50)], STONE2, 6, smooth=False, holes=(10, 20, 3))
    _shape(cr, [(-470, -50), (470, -50), (450, -96), (-450, -96)], STONE, 5, smooth=False)
    frame = [(-430, -96), (-430, -900), (-380, -1080), (-220, -1220), (0, -1280), (220, -1220), (380, -1080),
             (430, -900), (430, -96)]
    _shape(cr, frame, STONE, 7, smooth=False, holes=(14, 22, 3.4))
    ink(cr, [(-400, -110), (-400, -900), (-356, -1060), (-210, -1190), (0, -1246), (210, -1190), (356, -1060),
             (400, -900), (400, -110)], 6, smooth=False, col=GOLD)
    opening = [(-330, -96), (-330, -880), (-280, -1010), (-160, -1110), (0, -1150), (160, -1110), (280, -1010),
               (330, -880), (330, -96)]
    _shape(cr, opening, (0.30, 0.18, 0.12), 6, smooth=False)
    for sx in (-1, 1):                                                            # the two leaves
        x0, x1 = (sx * 6, sx * 326)
        lo, hi = min(x0, x1), max(x0, x1)
        for k in range(5):
            xx = lo + (hi - lo) * (k + 0.5) / 5
            ink(cr, [(xx, -110), (xx, -990 + 120 * abs(xx) / 330)], 2.5, smooth=False, col=(0.20, 0.10, 0.06))
        for y in (-260, -560, -860):
            band(cr, [(lo + 10, y), (hi - 10, y)], 20, (0.36, 0.36, 0.44), holes=False)
            for k in range(6):
                cr.new_path()
                cr.arc(lo + 30 + (hi - lo - 60) * k / 5, y, 7, 0, 2 * math.pi)
                leather(cr, (0.70, 0.70, 0.78), 2)
        cr.new_path()
        cr.arc(sx * 70, -520, 46, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.set_line_width(20)
        cr.stroke()
        cr.arc(sx * 70, -520, 46, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(11)
        cr.stroke()
        _jewel(cr, sx * 70, -566, 14, GOLD)
    ink(cr, [(0, -100), (0, -1146)], 6, smooth=False)
    _horns(cr, 0, -1300, 1.25)


register("sb_door", (-540, -1500, 540, 10), _door)


# ------------------------------------------------------------------ small badges


def _hush(cr):
    """The "silence" badge (centre pivot): lips seen from the front with an index finger held across them."""
    cr.new_path()
    ell(cr, 0, 0, 120, 120)
    leather(cr, PARCH, 6)
    holes_line(cr, [(-104, -40), (-60, -96), (0, -110), (60, -96), (104, -40)], 16, 2.8)
    lip = [(-70, 0), (-40, -24), (-14, -18), (0, -26), (14, -18), (40, -24), (70, 0), (40, 26), (0, 32), (-40, 26)]
    _shape(cr, lip, RED, 5)
    ink(cr, [(-66, 0), (66, 0)], 4)
    fing = [(-14, 90), (14, 90), (16, -60), (8, -84), (-8, -84), (-16, -60)]
    _shape(cr, fing, SKIN, 5)
    cr.new_path()
    ell(cr, 0, -66, 9, 12)
    leather(cr, (1.0, 0.86, 0.74), 2.5)
    ink(cr, [(-12, 30), (12, 30)], 2.5)


register("sb_hush", (-130, -130, 130, 130), _hush)
