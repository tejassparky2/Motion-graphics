"""The leather cast and props for the Jatayu reel (videos/jatayu.py), in the Togalu Gombeyaata style of the earlier
reels. Traditional leather puppets, modelled on no actor and no film. Every sprite name starts with "jt_".

  JATAYU   the old king of the vultures, a jointed leather bird in profile (facing +x): dark brown body with punched
           feather rows, a pale ruff at the neck, a long bare neck, a hooked pale-gold beak, a big almond eye under a
           white brow (he is old), a small gold crown (king of birds), a fan tail, two long wings with fingered
           tips (pivots at the shoulder: 0 = folded along the back, + raises the tip), two scaly legs with talons
           (- swings the foot forward). Heads: open eye (calm), shut (asleep), fierce (brow down, beak open), tired
           (eye half shut, beak open). A loose wing (jt_wing_loose) for the cut wings falling as pieces of leather.
Props: Ravana's flying chariot (gold box, wheel, parasol), its two broken halves, Ravana's bow and its two halves,
the pyre of logs, a burning torch, a compass card pointing south (drawn in the scenes), a single feather.
"""
import math

import puppet_cast as C
from puppet_cast import _jewel, _shape
from puppet_core import (BROWN, DRED, GOLD, GREEN, INK, PALE, RED, Rig, band, dots_in, holes_line, ink, leather,
                         poly, punch, register, spath)

FEATH = (0.46, 0.30, 0.18)            # dark brown feathers
FEATH2 = (0.62, 0.42, 0.24)           # lighter feather rows
RUFF = (0.97, 0.92, 0.82)
NECK = (0.94, 0.70, 0.56)
BEAK = (0.99, 0.86, 0.50)
LEGC = (0.90, 0.74, 0.50)
WOOD = (0.56, 0.33, 0.15)
CHAR = (0.99, 0.80, 0.30)


def _feather_rows(cr, pts, n, r=3.0):
    dots_in(cr, lambda: spath(cr, pts), n, r)


def jt_body(cr):
    tail = [(-200, -30), (-470, -110), (-500, -60), (-480, -10), (-500, 40), (-460, 80), (-200, 60)]
    _shape(cr, tail, FEATH, 5, smooth=False)
    for y in (-60, -10, 40):
        ink(cr, [(-220, y * 0.3), (-470, y)], 3)
    body = [(-240, -30), (-150, -118), (20, -146), (150, -106), (196, -30), (166, 58), (60, 112), (-120, 104),
            (-230, 50)]
    _shape(cr, body, FEATH, 6)
    _feather_rows(cr, body, 20, 3.4)
    for k in range(4):                                   # rows of scalloped feathers
        y = -76 + 46 * k
        pts = [(-180 + 60 * i, y + 18 * (i % 2)) for i in range(7)]
        ink(cr, pts, 3, col=(0.25, 0.14, 0.06))
    ruff = []
    for i in range(15):                                   # a fluffy collar round the neck's base
        a = math.pi * (0.95 + 1.1 * i / 14)
        r = 74 if i % 2 == 0 else 52
        ruff.append((150 + r * math.cos(a) * 1.1, -112 + r * math.sin(a) * 0.8))
    _shape(cr, ruff, RUFF, 4, smooth=False)
    holes_line(cr, [(100, -130), (190, -120)], 16, 3)


def jt_head(cr, mood="calm"):
    """Neck from the pivot (0, 0) up and forward to the head (~(120, -230)); beak to ~(250, -210)."""
    neck = [(-20, 10), (30, -60), (60, -150), (90, -210), (140, -250), (175, -230), (150, -170), (110, -110),
            (70, -40), (40, 20)]
    _shape(cr, neck, NECK, 5)
    for y in (-60, -120, -180):
        ink(cr, [(40 + 0.25 * -y, y), (70 + 0.25 * -y, y - 6)], 2.5, col=(0.55, 0.32, 0.22))
    skull = [(80, -230), (100, -282), (150, -300), (196, -284), (214, -250), (200, -214), (150, -200), (110, -206)]
    _shape(cr, skull, NECK, 5)
    open_ = mood in ("fierce", "tired")
    upper = [(196, -270), (240, -262), (276, -236), (282, -204), (266, -212), (246, -232), (204, -236)]
    _shape(cr, upper, BEAK, 4)
    _shape(cr, [(266, -212), (282, -204), (276, -190), (262, -200)], INK, 2)          # dark hooked tip
    lower = [(204, -232), (248, -222), (258, -208)] if not open_ else [(204, -232), (240, -206), (250, -186)]
    _shape(cr, lower + [(206, -220)], BEAK, 3)
    cr.new_path()
    cr.arc(214, -258, 5, 0, 2 * math.pi)                                                    # nostril
    cr.set_source_rgb(*INK)
    cr.fill()
    ex, ey = 168, -258
    if mood == "shut":
        ink(cr, [(ex - 18, ey), (ex, ey + 6), (ex + 18, ey)], 4)
    else:
        hh = 7 if mood == "tired" else 11
        cr.new_path()
        cr.move_to(ex - 20, ey)
        cr.curve_to(ex - 10, ey - hh, ex + 10, ey - hh, ex + 20, ey + 1)
        cr.curve_to(ex + 10, ey + hh * 0.8, ex - 10, ey + hh * 0.8, ex - 20, ey)
        cr.close_path()
        leather(cr, PALE, 3.5)
        cr.arc(ex + 4, ey, hh * 0.6, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(ex + 7, ey - 3)], 2.2)
    brow = [(ex - 34, ey - 22), (ex - 4, ey - 32), (ex + 26, ey - 24), (ex + 20, ey - 16), (ex - 6, ey - 20),
            (ex - 30, ey - 12)]
    if mood == "fierce":
        brow = [(ex - 34, ey - 30), (ex - 4, ey - 28), (ex + 28, ey - 14), (ex + 22, ey - 6), (ex - 6, ey - 16),
                (ex - 32, ey - 20)]
    _shape(cr, brow, RUFF, 3)                                                               # white old brow
    for i in range(4):                                                                       # tufts at the back
        a = math.radians(160 + 14 * i)
        _shape(cr, [(110, -260), (110 + 70 * math.cos(a), -270 + 50 * math.sin(a) - 10 * i), (104, -236)], RUFF, 3)
    crown = [(110, -294), (112, -342), (132, -318), (152, -364), (172, -318), (192, -342), (194, -290)]
    _shape(cr, crown, GOLD, 4, smooth=False)
    band(cr, [(112, -300), (192, -296)], 12, RED, spacing=10, hole_r=2.0)
    _jewel(cr, 152, -324, 9, RED)


def jt_wing(cr):
    """A wing, pivot at the shoulder, lying back along -x: coverts then long fingered primaries."""
    cov = [(20, -30), (-60, -70), (-220, -76), (-320, -56), (-336, 0), (-220, 30), (-80, 40), (20, 20)]
    _shape(cr, cov, FEATH2, 5)
    _feather_rows(cr, cov, 14, 3)
    for i in range(7):                                   # primaries
        y0 = -50 + 14 * i
        L = 200 - 12 * abs(i - 2)
        x0 = -250 - 10 * i
        f = [(x0, y0 - 14), (x0 - L, y0 - 30 + 10 * i), (x0 - L - 26, y0 - 18 + 10 * i), (x0 - L + 10, y0 - 4 + 10 * i),
             (x0, y0 + 16)]
        _shape(cr, f, FEATH, 3)
        ink(cr, [(x0, y0), (x0 - L, y0 - 18 + 10 * i)], 2, col=(0.25, 0.14, 0.06))
    band(cr, [(10, -10), (-120, -40), (-250, -40)], 12, RUFF, spacing=12, hole_r=2.0)


def jt_leg(cr):
    _shape(cr, [(-30, -20), (40, -20), (34, 80), (-24, 80)], FEATH, 4)                     # feathered thigh
    _shape(cr, [(-10, 70), (16, 70), (14, 200), (-8, 200)], LEGC, 3, smooth=False)
    for y in (100, 130, 160, 190):
        ink(cr, [(-8, y), (14, y)], 2)
    for ang in (-0.2, 0.25, 0.75, 2.9):                   # toes with dark talons
        ca, sa = math.cos(ang), math.sin(ang)
        x1, y1 = 4 + 60 * ca, 204 + 30 * sa
        _shape(cr, [(0, 196), (x1, y1 - 6), (x1, y1 + 6), (6, 210)], LEGC, 2.5)
        _shape(cr, [(x1, y1 - 6), (x1 + 22 * ca, y1 + 12), (x1 - 2, y1 + 8)], INK, 2)


register("jt_body", (-520, -210, 230, 160), jt_body)
JT_MOODS = ("calm", "shut", "fierce", "tired")
for _m in JT_MOODS:
    register("jt_head" + ("" if _m == "calm" else "_" + _m), (-40, -360, 300, 40), lambda cr, m=_m: jt_head(cr, m))
for _k in ("F", "B"):
    register("jt_wing" + _k, (-720, -120, 40, 140), jt_wing)
    register("jt_leg" + _k, (-90, -30, 100, 240), jt_leg)
register("jt_wing_loose", (-720, -120, 40, 140), jt_wing)

JATAYU = Rig([
    ("jt_wingB", "jt_body", (40, -110), 0.0),
    ("jt_legB", "jt_body", (0, 100), 0.0),
    ("jt_body", None, (0, 0), 0.0),
    ("jt_legF", "jt_body", (40, 100), 0.0),
    ("jt_head", "jt_body", (140, -96), 0.2),
    ("jt_wingF", "jt_body", (70, -100), 0.0),
], points={"beak": ("jt_head", (270, -210)), "eye": ("jt_head", (168, -258)), "top": ("jt_head", (150, -340)),
           "footF": ("jt_legF", (10, 215)), "footB": ("jt_legB", (10, 215)), "chest": ("jt_body", (120, -40)),
           "tipF": ("jt_wingF", (-520, -30)), "tipB": ("jt_wingB", (-520, -30)), "back": ("jt_body", (0, -130))},
    rods=[("back", 60, 0), ("tipF", 160, 0)])


# ------------------------------------------------------------------ props


def chariot(cr, half=None):
    """Ravana's flying chariot (pivot at the floor's middle): a gold box with punched panels, a big wheel, a tall
    pole with a parasol. half = "L" / "R" draws only that half (the chariot broken in two)."""
    cr.save()
    if half:
        cr.rectangle(-700 if half == "L" else 10, -1200, 690, 1500)
        cr.clip()
    box = [(-300, 0), (-320, -200), (-260, -230), (260, -230), (320, -200), (300, 0)]
    _shape(cr, box, CHAR, 6, smooth=False)
    for x in (-200, 0, 200):
        cr.new_path()
        cr.arc(x, -110, 48, 0, 2 * math.pi)
        leather(cr, RED, 3)
        dots_in(cr, lambda x=x: (cr.new_path(), cr.arc(x, -110, 36, 0, 2 * math.pi)), 8, 3)
    band(cr, [(-310, -200), (310, -200)], 16, RED, spacing=12, hole_r=2.4)
    cr.new_path()
    cr.arc(-60, 20, 120, 0, 2 * math.pi)
    leather(cr, (0.80, 0.52, 0.24), 6)
    for i in range(8):
        a = math.pi * i / 4
        ink(cr, [(-60, 20), (-60 + 110 * math.cos(a), 20 + 110 * math.sin(a))], 5)
    punch(cr, [(-60, 20)], 10)
    ink(cr, [(220, -230), (220, -620)], 8, col=WOOD)
    para = [(60, -600), (220, -700), (380, -600), (340, -590), (220, -650), (100, -590)]
    _shape(cr, para, RED, 5)
    holes_line(cr, [(80, -604), (360, -604)], 20, 3)
    for x in (70, 140, 220, 300, 370):
        cr.new_path()
        cr.arc(x, -580, 8, 0, 2 * math.pi)
        leather(cr, GOLD, 2)
    cr.restore()


register("jt_chariot", (-460, -720, 400, 160), chariot)
register("jt_chariotL", (-460, -720, 20, 160), lambda cr: chariot(cr, "L"))
register("jt_chariotR", (-20, -720, 400, 160), lambda cr: chariot(cr, "R"))


def bow(cr, half=None):
    """Ravana's big bow (pivot at the grip), drawn upright: a gold-tipped dark arc and its string."""
    cr.save()
    if half:
        cr.rectangle(-200, -600 if half == "T" else 0, 400, 600)
        cr.clip()
    pts = [(0, -440), (60, -300), (84, -120), (90, 0), (84, 120), (60, 300), (0, 440)]
    ink(cr, pts, 26, col=INK)
    ink(cr, pts, 16, col=(0.45, 0.16, 0.10))
    ink(cr, [(0, -440), (0, 440)], 2.5, col=INK)
    _shape(cr, [(70, -26), (110, -26), (110, 26), (70, 26)], GOLD, 3, smooth=False)
    cr.restore()


register("jt_bow", (-40, -470, 140, 470), bow)
register("jt_bowT", (-40, -470, 140, 10), lambda cr: bow(cr, "T"))
register("jt_bowB", (-40, -10, 140, 470), lambda cr: bow(cr, "B"))


def _pyre(cr):
    """A stack of logs (pivot at the bottom centre)."""
    for row in range(4):
        y = -40 - 56 * row
        w = 380 - 40 * row
        for k in (-1, 1):
            log = [(-w, y - 24), (w, y - 24 + 6 * k), (w, y + 24 + 6 * k), (-w, y + 24)]
            if (row + (k > 0)) % 2 == 0:
                _shape(cr, log, WOOD, 4, smooth=False)
                for x in (-w + 10, w - 10):
                    cr.new_path()
                    cr.arc(x, y, 20, 0, 2 * math.pi)
                    leather(cr, (0.80, 0.56, 0.30), 3)


register("jt_pyre", (-400, -260, 400, 10), _pyre)


def _torch(cr):
    ink(cr, [(0, 0), (0, -260)], 12, col=WOOD)
    _shape(cr, [(-26, -250), (26, -250), (20, -300), (-20, -300)], (0.70, 0.50, 0.30), 3, smooth=False)


register("jt_torch", (-40, -320, 40, 10), _torch)


def _feather(cr):
    f = [(0, 0), (30, -90), (24, -200), (0, -260), (-24, -200), (-30, -90)]
    _shape(cr, f, FEATH2, 4)
    ink(cr, [(0, 30), (0, -250)], 3, col=(0.25, 0.14, 0.06))
    for y in (-60, -110, -160, -210):
        ink(cr, [(0, y), (22, y - 20)], 2)
        ink(cr, [(0, y), (-22, y - 20)], 2)


register("jt_feather", (-40, -270, 40, 40), _feather)
