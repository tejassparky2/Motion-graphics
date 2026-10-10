"""Polished cartoon people and animals for the polished look (motion/polish.py), in the style of motion/bees.py.

person(cr, t, x, y, s, who=...) draws a big-headed (chibi) character standing with its feet at (x, y).
`who` picks a preset from CAST (hair, skin, clothes, accessories); any field can be overridden by keyword.
Faces share the bee faces: eyes in open/happy/wide/half/closed/x/angry/sad, mouth in
smile/grin/o/flat/sad/smug/open/talk. Brows: None/up/angry/sad/flat/raise.
Arms: (front, back) poses from ARMS or (dx, dy) tuples relative to the shoulder.

Animals: tortoise (side view), jellyfish, polyp, jelly_blob, fish.
"""
import math

from .bees import _eye, _lid, _mouth
from .engine import hexc
from .polish import OUTLINE, WHITE, alpha, ellipse, ground_shadow, lin, paint, rad, rrect, shade, smooth, \
    soft_disc, stroke_line

SKIN = {"light": hexc("#f8cfa8"), "tan": hexc("#e0a77a"), "brown": hexc("#b5764c"), "olive": hexc("#d9ab7e")}
BLUSH = hexc("#ff8a8a")

ARMS = {   # hand position relative to the shoulder at s=1 (x toward the body's outside for each arm)
    "down": (18, 150), "hips": (62, 88), "wave": (78, -118), "up": (26, -170), "point": (158, -18),
    "hold": (96, 46), "out": (140, 34), "chin": (-56, -58), "face": (-44, -112), "push": (150, 18),
    "cross": (-70, 52), "front": (40, 66), "shrug": (92, -30), "fist": (60, -150), "think": (-40, -72),
    "write": (70, 20), "pocket": (30, 120),
}

CAST = {
    "kid": dict(skin="tan", hair="spiky", hair_col=hexc("#2b1a12"), shirt=hexc("#f4f6fb"), pants=hexc("#3b5b9a"),
                shoes=hexc("#2b2b33"), tie=hexc("#d8453c"), build="kid"),
    "teacher": dict(skin="light", hair="bun", hair_col=hexc("#6b3a22"), shirt=hexc("#7a5bd0"),
                    pants=hexc("#2f3550"), skirt=True, shoes=hexc("#5a2a3a"), glasses=True, build="adult",
                    collar=hexc("#ffffff")),
    "student1": dict(skin="light", hair="pony", hair_col=hexc("#e0a33a"), shirt=hexc("#f4f6fb"),
                     pants=hexc("#3b5b9a"), tie=hexc("#d8453c"), build="kid"),
    "student2": dict(skin="brown", hair="curly", hair_col=hexc("#1e130d"), shirt=hexc("#f4f6fb"),
                     pants=hexc("#3b5b9a"), tie=hexc("#d8453c"), build="kid"),
    "student3": dict(skin="olive", hair="short", hair_col=hexc("#4a2c1c"), shirt=hexc("#f4f6fb"),
                     pants=hexc("#3b5b9a"), tie=hexc("#d8453c"), glasses=True, build="kid"),
    "achilles": dict(skin="tan", hair="short", hair_col=hexc("#5a3418"), shirt=hexc("#d8453c"), tunic=True,
                     belt=hexc("#c99a2e"), helmet=True, shoes=hexc("#8a5a2b"), sandals=True, build="adult"),
    "zeno": dict(skin="light", hair="bald", hair_col=hexc("#d9d9e0"), beard=hexc("#e8e8ee"), shirt=hexc("#f3efe4"),
                 toga=hexc("#4f7fc9"), shoes=hexc("#8a5a2b"), sandals=True, build="adult", brows_col=hexc("#b8b8c4")),
    "twain": dict(skin="light", hair="twain", hair_col=hexc("#f2f2f5"), stache=hexc("#f2f2f5"),
                  shirt=hexc("#ffffff"), suit=hexc("#f1ede4"), pants=hexc("#e9e4d8"), tie=hexc("#2b2b33"),
                  shoes=hexc("#ece6da"), build="adult", brows_col=hexc("#e8e8ee"), bowtie=True),
    "reporter": dict(skin="olive", hair="short", hair_col=hexc("#2b1a12"), shirt=hexc("#f4f0e6"),
                     suit=hexc("#7a5a3c"), pants=hexc("#6a4c32"), tie=hexc("#b33a2e"), shoes=hexc("#2b1d16"),
                     fedora=hexc("#5c4632"), build="adult"),
    "protagoras": dict(skin="olive", hair="short", hair_col=hexc("#3a2418"), beard=hexc("#5a3a24"),
                       shirt=hexc("#f3efe4"), toga=hexc("#8a4fc9"), shoes=hexc("#8a5a2b"), sandals=True, build="adult"),
    "student_gr": dict(skin="tan", hair="curly", hair_col=hexc("#4a2c1c"), shirt=hexc("#3fae6a"), tunic=True,
                       belt=hexc("#8a5a2b"), shoes=hexc("#8a5a2b"), sandals=True, build="adult"),
    "judge": dict(skin="light", hair="bald", hair_col=hexc("#d9d9e0"), beard=hexc("#e8e8ee"), shirt=hexc("#f3efe4"),
                  toga=hexc("#c8402e"), shoes=hexc("#8a5a2b"), sandals=True, build="adult",
                  brows_col=hexc("#b8b8c4")),
    "mother": dict(skin="brown", hair="bun", hair_col=hexc("#1e130d"), shirt=hexc("#2fa59a"), pants=hexc("#e8a33a"),
                   skirt=True, shoes=hexc("#5a2a3a"), build="adult"),
    "barber": dict(skin="olive", hair="short", hair_col=hexc("#1e130d"), stache=hexc("#1e130d"), shirt=WHITE,
                   pants=hexc("#2b2b33"), apron=hexc("#e8473f"), tie=hexc("#2b2b33"), bowtie=True, build="adult"),
    "villager": dict(skin="tan", hair="short", hair_col=hexc("#5a3418"), beard=hexc("#5a3418"),
                     shirt=hexc("#c9a46a"), pants=hexc("#5a6478"), build="adult"),
    "russell": dict(skin="light", hair="twain", hair_col=hexc("#e8e8ee"), shirt=WHITE, suit=hexc("#4a4f5c"),
                    pants=hexc("#3a3e48"), tie=hexc("#2b2b33"), build="adult", brows_col=hexc("#c8c8d0")),
    "seller": dict(skin="light", hair="topknot", hair_col=hexc("#1e130d"), stache=hexc("#1e130d"),
                   shirt=hexc("#f4d35e"), toga=hexc("#c8302a"), shoes=hexc("#2b1d16"), build="adult"),
    "crowdkid": dict(skin="light", hair="topknot", hair_col=hexc("#1e130d"), shirt=hexc("#4a8ad0"), tunic=True,
                     belt=hexc("#2b2b33"), shoes=hexc("#2b1d16"), build="kid"),
    "aquinas": dict(skin="light", hair="tonsure", hair_col=hexc("#5a3a24"), shirt=WHITE, toga=hexc("#2b2b33"),
                    shoes=hexc("#2b1d16"), build="adult"),
    "fermi": dict(skin="olive", hair="short", hair_col=hexc("#2b1a12"), shirt=WHITE, suit=hexc("#6a7080"),
                  pants=hexc("#5a606e"), tie=hexc("#8a2a2a"), shoes=hexc("#2b1d16"), build="adult"),
    "doctor": dict(skin="brown", hair="short", hair_col=hexc("#1e130d"), shirt=hexc("#2fa59a"), suit=WHITE,
                   pants=hexc("#2f7f78"), shoes=hexc("#2b2b33"), stethoscope=True, build="adult"),
    "doctor2": dict(skin="light", hair="bun", hair_col=hexc("#6b3a22"), shirt=hexc("#4a8ad0"), suit=WHITE,
                    pants=hexc("#3a6aa8"), shoes=hexc("#2b2b33"), stethoscope=True, glasses=True, build="adult"),
    "patient": dict(skin="tan", hair="short", hair_col=hexc("#3a2418"), shirt=hexc("#9fd0f0"),
                    pants=hexc("#9fd0f0"), shoes=hexc("#e8e8ee"), build="adult"),
    "cousin": dict(skin="light", hair="short", hair_col=hexc("#8a6a4a"), shirt=hexc("#e8f0ff"), build="adult",
                   stache=hexc("#8a6a4a")),
}

BUILDS = {   # head r, head centre y, shoulder y, hip y, shoulder half-width, hip half-width, leg width, arm width
    "kid": dict(hr=94, hy=-392, sy=-292, py=-128, sw=66, pw=60, lw=34, aw=28),
    "adult": dict(hr=86, hy=-468, sy=-372, py=-168, sw=78, pw=66, lw=38, aw=30),
}


def _limb(cr, pts, w, col, curve=True):
    stroke_line(cr, pts, w + 9, OUTLINE, curve=curve)
    stroke_line(cr, pts, w, col, curve=curve)


def _hand(cr, x, y, r, skin):
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, rad(x - r * 0.3, y - r * 0.4, r * 1.3, [(0, shade(skin, 0.25)), (1, shade(skin, -0.08))]), OUTLINE, 4.5)


# ---------------------------------------------------------------- hair (drawn around a head of radius r at 0, 0)
def _hair_back(cr, style, r, col):
    if style == "bun":
        ellipse(cr, 0, 0.05 * r, 1.13 * r, 1.08 * r)          # a bob behind the head
        paint(cr, lin(0, -r, 0, r, [(0, shade(col, 0.15)), (1, shade(col, -0.2))]), OUTLINE, 5)
        cr.arc(0, -1.02 * r, 0.42 * r, 0, 2 * math.pi)        # the bun
        paint(cr, rad(-0.1 * r, -1.12 * r, 0.5 * r, [(0, shade(col, 0.3)), (1, shade(col, -0.1))]), OUTLINE, 5)
        stroke_line(cr, [(-0.25 * r, -1.0 * r), (0, -0.88 * r), (0.25 * r, -1.0 * r)], 3, alpha(OUTLINE, 0.5))
    elif style == "topknot":
        cr.arc(0, -1.12 * r, 0.28 * r, 0, 2 * math.pi)
        paint(cr, rad(-0.08 * r, -1.2 * r, 0.35 * r, [(0, shade(col, 0.35)), (1, col)]), OUTLINE, 5)
        rrect(cr, -0.2 * r, -0.92 * r, 0.4 * r, 0.12 * r, 0.05 * r)
        paint(cr, hexc("#e8473f"), OUTLINE, 3)
    elif style == "pony":
        smooth(cr, [(0.7 * r, -0.6 * r), (1.35 * r, -0.4 * r), (1.45 * r, 0.3 * r), (1.15 * r, 0.75 * r),
                    (1.0 * r, 0.1 * r), (0.85 * r, -0.3 * r)])
        paint(cr, lin(0, -r, 0, r, [(0, shade(col, 0.25)), (1, shade(col, -0.15))]), OUTLINE, 5)
    elif style == "twain":
        pts = []
        for k in range(15):   # a bushy white mane, wider than the head
            a = math.pi * (0.92 + 1.16 * k / 14)
            rr = r * (1.22 + 0.1 * math.sin(k * 2.3))
            pts.append((math.cos(a) * rr * 1.05, math.sin(a) * rr * 0.95 + 0.12 * r))
        pts += [(1.1 * r, 0.35 * r), (0.9 * r, 0.55 * r), (-0.9 * r, 0.55 * r), (-1.1 * r, 0.35 * r)]
        smooth(cr, pts)
        paint(cr, rad(-0.3 * r, -0.6 * r, 1.6 * r, [(0, WHITE), (1, shade(col, -0.12))]), OUTLINE, 5)
    elif style == "curly":
        for k in range(11):
            a = math.pi * (0.95 + 1.1 * k / 10)
            cr.arc(math.cos(a) * r * 0.98, math.sin(a) * r * 0.98 - 0.02 * r, 0.3 * r, 0, 2 * math.pi)
            paint(cr, rad(0, -r, 1.4 * r, [(0, shade(col, 0.3)), (1, col)]), OUTLINE, 4.5)


def _hair_front(cr, style, r, col):
    g = lin(0, -r, 0, 0, [(0, shade(col, 0.28)), (1, shade(col, -0.05))])
    if style == "spiky":
        pts = [(-1.02 * r, 0.05 * r)]
        for k in range(9):
            a = math.pi * (1.0 + k / 8)
            rr = r * (1.08 if k % 2 == 0 else 1.3)
            pts.append((math.cos(a) * rr, math.sin(a) * rr - 0.05 * r))
        pts += [(1.02 * r, 0.05 * r), (0.8 * r, -0.32 * r), (0.45 * r, -0.42 * r), (0.2 * r, -0.3 * r),
                (-0.15 * r, -0.44 * r), (-0.5 * r, -0.35 * r), (-0.82 * r, -0.3 * r)]
        smooth(cr, pts)
        paint(cr, g, OUTLINE, 5)
    elif style in ("bun", "short", "pony", "topknot"):
        part = 0.25 if style == "bun" else -0.2
        pts = [(-1.03 * r, 0.1 * r if style == "bun" else -0.15 * r)]
        for k in range(9):
            a = math.pi * (1.0 + k / 8)
            pts.append((math.cos(a) * 1.07 * r, math.sin(a) * 1.07 * r))
        pts += [(1.03 * r, 0.1 * r if style == "bun" else -0.15 * r), (0.8 * r, -0.45 * r),
                (part * r, -0.62 * r), (-0.6 * r, -0.4 * r), (-0.9 * r, -0.2 * r)]
        smooth(cr, pts)
        paint(cr, g, OUTLINE, 5)
        stroke_line(cr, [(part * r, -0.62 * r), (part * r + 0.15 * r, -0.95 * r)], 3, alpha(OUTLINE, 0.45))
    elif style == "curly":
        for k in range(7):
            a = math.pi * (1.12 + 0.76 * k / 6)
            cr.arc(math.cos(a) * r * 0.82, math.sin(a) * r * 0.82, 0.28 * r, 0, 2 * math.pi)
            paint(cr, rad(0, -r, 1.4 * r, [(0, shade(col, 0.35)), (1, col)]), OUTLINE, 4.5)
    elif style == "twain":
        pts = [(-1.05 * r, -0.05 * r)]       # one big swept-back cloud of white hair, a low wavy hairline
        for k in range(11):
            a = math.pi * (1.0 + k / 10)
            rr = r * (1.16 if k % 2 == 0 else 1.26)
            pts.append((math.cos(a) * rr * 1.04, math.sin(a) * rr - 0.04 * r))
        pts += [(1.05 * r, -0.05 * r), (0.8 * r, -0.42 * r), (0.4 * r, -0.55 * r), (0.0, -0.5 * r),
                (-0.4 * r, -0.58 * r), (-0.8 * r, -0.42 * r)]
        smooth(cr, pts)
        paint(cr, rad(-0.3 * r, -0.9 * r, 1.4 * r, [(0, WHITE), (0.6, col), (1, shade(col, -0.16))]), OUTLINE, 5)
        for k in range(4):
            x = (-0.55 + 0.36 * k) * r
            stroke_line(cr, [(x, -0.62 * r), (x + 0.12 * r, -0.9 * r), (x + 0.3 * r, -1.02 * r)], 3,
                        alpha(OUTLINE, 0.22))
    elif style == "tonsure":
        cr.new_path()
        cr.arc(0, -0.05 * r, 1.07 * r, math.pi * 0.95, math.pi * 2.05)
        cr.arc_negative(0, -0.1 * r, 0.8 * r, math.pi * 2.0, math.pi * 1.0)
        cr.close_path()
        paint(cr, lin(0, -r, 0, 0, [(0, shade(col, 0.25)), (1, shade(col, -0.05))]), OUTLINE, 5)
        ellipse(cr, -0.25 * r, -0.62 * r, 0.25 * r, 0.12 * r, -0.4)
        paint(cr, alpha(WHITE, 0.45), None, 0)
    elif style == "bald":
        for side in (-1, 1):   # grey tufts over the ears
            smooth(cr, [(side * 0.78 * r, -0.45 * r), (side * 1.12 * r, -0.3 * r), (side * 1.12 * r, 0.25 * r),
                        (side * 0.86 * r, 0.3 * r)])
            paint(cr, rad(side * r, 0, 0.6 * r, [(0, WHITE), (1, shade(col, -0.15))]), OUTLINE, 4)
        ellipse(cr, -0.3 * r, -0.62 * r, 0.25 * r, 0.12 * r, -0.4)   # shine on the bald top
        paint(cr, alpha(WHITE, 0.45), None, 0)


def _helmet(cr, r, t):
    gold = hexc("#e2b23a")
    # horsehair crest, front to back over the top
    smooth(cr, [(-0.9 * r, -0.75 * r), (-0.5 * r, -1.55 * r), (0.4 * r, -1.62 * r), (1.05 * r, -1.1 * r),
                (1.25 * r, -0.55 * r), (0.85 * r, -0.95 * r), (0.2 * r, -1.2 * r), (-0.5 * r, -1.0 * r)])
    paint(cr, lin(0, -1.6 * r, 0, -0.6 * r, [(0, hexc("#ff5a4a")), (1, hexc("#b8262a"))]), OUTLINE, 5)
    for k in range(6):
        x = (-0.5 + 0.28 * k) * r
        stroke_line(cr, [(x, -1.05 * r - 0.1 * r * math.sin(k)), (x + 0.12 * r, -1.45 * r)], 2.5,
                    alpha(hexc("#7a1418"), 0.55))
    # dome + cheek guards, with the face opening cut out
    cr.new_path()
    cr.arc(0, -0.05 * r, 1.08 * r, math.pi * 1.0, math.pi * 2.0)
    cr.line_to(1.08 * r, 0.55 * r)
    cr.line_to(0.62 * r, 0.62 * r)
    cr.line_to(0.6 * r, -0.12 * r)
    cr.line_to(0.28 * r, -0.3 * r)
    cr.line_to(0.12 * r, 0.2 * r)          # nose guard
    cr.line_to(-0.12 * r, 0.2 * r)
    cr.line_to(-0.28 * r, -0.3 * r)
    cr.line_to(-0.6 * r, -0.12 * r)
    cr.line_to(-0.62 * r, 0.62 * r)
    cr.line_to(-1.08 * r, 0.55 * r)
    cr.close_path()
    paint(cr, lin(-r, -r, r, r, [(0, hexc("#fff0a8")), (0.35, gold), (1, hexc("#9a6a14"))]), OUTLINE, 5)
    ellipse(cr, -0.45 * r, -0.72 * r, 0.3 * r, 0.12 * r, -0.5)
    paint(cr, alpha(WHITE, 0.6), None, 0)


def _fedora(cr, r, col):
    ellipse(cr, 0, -0.68 * r, 1.45 * r, 0.3 * r)
    paint(cr, lin(0, -r, 0, -0.4 * r, [(0, shade(col, 0.2)), (1, shade(col, -0.25))]), OUTLINE, 5)
    smooth(cr, [(-0.85 * r, -0.7 * r), (-0.8 * r, -1.35 * r), (-0.2 * r, -1.5 * r), (0.15 * r, -1.36 * r),
                (0.5 * r, -1.5 * r), (0.85 * r, -1.32 * r), (0.85 * r, -0.7 * r)])
    paint(cr, lin(0, -1.5 * r, 0, -0.7 * r, [(0, shade(col, 0.25)), (1, col)]), OUTLINE, 5)
    rrect(cr, -0.86 * r, -0.98 * r, 1.72 * r, 0.24 * r, 4)
    paint(cr, hexc("#2b1d16"), None, 0)
    rrect(cr, 0.2 * r, -1.12 * r, 0.5 * r, 0.3 * r, 4)
    paint(cr, hexc("#fff8e6"), OUTLINE, 3)
    cr.select_font_face("Fredoka")
    cr.set_font_size(0.16 * r)
    cr.move_to(0.24 * r, -0.92 * r)
    cr.set_source_rgba(*OUTLINE)
    cr.show_text("PRESS")


def head(cr, t, x, y, r, who="kid", eyes="open", mouth="smile", look=(0.0, 0.0), brows=None, turn=0.0, lid=0.0,
         blush=True, sweat=False, **kw):
    """Just the head (for heads peeking out of beds, windows, crowds). (x, y) is the head centre."""
    c = dict(CAST.get(who, CAST["kid"]))
    c.update(kw)
    skin = SKIN.get(c.get("skin"), c.get("skin")) if isinstance(c.get("skin"), str) else c.get("skin")
    hair, hcol = c.get("hair"), c.get("hair_col", OUTLINE)
    cr.save()
    cr.translate(x, y)
    if not c.get("helmet"):
        _hair_back(cr, hair, r, hcol)
    for side in (-1, 1):    # ears
        ellipse(cr, side * 0.98 * r, 0.08 * r, 0.2 * r, 0.24 * r)
        paint(cr, shade(skin, -0.05), OUTLINE, 4.5)
        ellipse(cr, side * 0.98 * r, 0.08 * r, 0.09 * r, 0.12 * r)
        paint(cr, shade(skin, -0.2), None, 0)
    ellipse(cr, 0, 0, r, r * 0.97)
    paint(cr, rad(-0.3 * r, -0.35 * r, 1.35 * r, [(0, shade(skin, 0.3)), (0.6, skin), (1, shade(skin, -0.12))]),
          OUTLINE, 5.5)
    if c.get("beard") is not None:
        bc = c["beard"]
        smooth(cr, [(-0.92 * r, 0.05 * r), (-0.8 * r, 0.8 * r), (-0.4 * r, 1.55 * r), (0, 1.85 * r),
                    (0.4 * r, 1.55 * r), (0.8 * r, 0.8 * r), (0.92 * r, 0.05 * r), (0.5 * r, 0.42 * r),
                    (0, 0.3 * r), (-0.5 * r, 0.42 * r)])
        paint(cr, rad(0, 0.4 * r, 1.6 * r, [(0, WHITE), (1, shade(bc, -0.18))]), OUTLINE, 5)
        for k in range(5):
            xx = (-0.5 + 0.25 * k) * r
            stroke_line(cr, [(xx, 0.7 * r), (xx * 0.8, 1.2 * r), (xx * 0.5, 1.55 * r)], 2.5, alpha(OUTLINE, 0.25))
    if not c.get("helmet"):
        _hair_front(cr, hair, r, hcol)
    fx = turn * 0.22 * r
    ey = -0.02 * r
    erx, ery = 0.19 * r, 0.25 * r
    for side in (-1, 1):
        ex = fx + side * 0.36 * r
        _eye(cr, ex, ey, erx, ery, look, eyes)
        if lid or eyes in ("half",):
            _lid(cr, ex, ey, erx, ery, lid or 0.5, skin, slope=0.0)
        elif eyes == "sad":
            _lid(cr, ex, ey, erx, ery, 0.35, skin, slope=-0.35 * side)
        elif eyes == "angry":
            _lid(cr, ex, ey, erx, ery, 0.35, skin, slope=0.4 * side)
    bcol = c.get("brows_col", shade(hcol, -0.1))
    if brows is not None or c.get("hair") == "twain":
        for side in (-1, 1):
            ex = fx + side * 0.36 * r
            by = ey - ery - 0.14 * r
            inner, outer = (ex - side * 0.16 * r), (ex + side * 0.18 * r)
            d = {"up": (-0.12, -0.12), "angry": (0.1, -0.08), "sad": (-0.12, 0.06), "flat": (0, 0),
                 "raise": (-0.16 if side > 0 else 0.0, -0.16 if side > 0 else 0.0)}.get(brows, (0, 0))
            w = 9 if c.get("hair") == "twain" else 6
            stroke_line(cr, [(inner, by + d[0] * r), (outer, by + d[1] * r)], w, bcol if w == 9 else OUTLINE,
                        curve=False)
    if blush:
        for side in (-1, 1):
            ellipse(cr, fx + side * 0.58 * r, 0.3 * r, 0.16 * r, 0.09 * r)
            paint(cr, alpha(BLUSH, 0.45), None, 0)
    ellipse(cr, fx, 0.2 * r, 0.09 * r, 0.07 * r)     # nose
    paint(cr, shade(skin, -0.15), None, 0)
    cr.save()
    cr.translate(fx, 0.46 * r)
    cr.scale(r / 70, r / 70)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    if c.get("stache") is not None:
        sc = c["stache"]
        big = c.get("hair") == "twain"
        for side in (-1, 1):
            smooth(cr, [(fx, 0.3 * r), (fx + side * 0.25 * r, 0.27 * r), (fx + side * (0.62 if big else 0.36) * r,
                        (0.52 if big else 0.4) * r), (fx + side * 0.45 * r, 0.5 * r),
                        (fx + side * 0.2 * r, 0.44 * r), (fx, 0.4 * r)])
            paint(cr, rad(fx, 0.3 * r, 0.6 * r, [(0, shade(sc, 0.2)), (1, shade(sc, -0.15))]), OUTLINE, 4)
    if c.get("glasses"):
        for side in (-1, 1):
            cr.arc(fx + side * 0.36 * r, ey, 0.27 * r, 0, 2 * math.pi)
            cr.set_source_rgba(1, 1, 1, 0.12)
            cr.fill_preserve()
            cr.set_source_rgba(*OUTLINE)
            cr.set_line_width(5)
            cr.stroke()
            stroke_line(cr, [(fx + side * 0.36 * r - 0.12 * r, ey - 0.12 * r),
                             (fx + side * 0.36 * r - 0.02 * r, ey - 0.2 * r)], 3, alpha(WHITE, 0.8))
        stroke_line(cr, [(fx - 0.1 * r, ey - 0.03 * r), (fx + 0.1 * r, ey - 0.03 * r)], 5, OUTLINE, curve=False)
    if c.get("helmet"):
        _helmet(cr, r, t)
    if c.get("fedora") is not None:
        _fedora(cr, r, c["fedora"])
    if sweat:
        k = (t * 1.3) % 1.0
        sx, sy = 0.95 * r, -0.4 * r + k * 0.5 * r
        cr.move_to(sx, sy - 0.16 * r)
        cr.curve_to(sx + 0.1 * r, sy, sx + 0.08 * r, sy + 0.1 * r, sx, sy + 0.1 * r)
        cr.curve_to(sx - 0.08 * r, sy + 0.1 * r, sx - 0.1 * r, sy, sx, sy - 0.16 * r)
        paint(cr, alpha(hexc("#8fd3ff"), 1 - k * 0.6), OUTLINE, 3)
    cr.restore()


def person(cr, t, x, y, s=1.0, who="kid", facing=1, eyes="open", mouth="smile", look=(0.0, 0.0), brows=None,
           arms=("down", "down"), turn=0.0, walk=None, run=False, bob=True, shadow=True, tilt=0.0, squash=0.0,
           hold=None, hold_back=None, lid=0.0, blush=True, sweat=False, seed=0, **kw):
    """A standing character with its feet at (x, y). `walk` is a phase (radians) for stepping legs/arms;
    `run` makes the stride big. `hold(cr, hx, hy)` draws a prop at the front hand (local coordinates)."""
    c = dict(CAST.get(who, CAST["kid"]))
    c.update(kw)
    b = BUILDS[c.get("build", "kid")]
    skin = SKIN.get(c.get("skin"), hexc("#f8cfa8"))
    hr, hy, sy, py, sw, pw, lw, aw = (b[k] for k in ("hr", "hy", "sy", "py", "sw", "pw", "lw", "aw"))
    ph = seed * 1.3
    breathe = math.sin(t * 2.2 + ph) if bob else 0.0
    stride = 0.0 if walk is None else math.sin(walk)
    hop = abs(math.sin(walk)) * (14 if run else 5) if walk is not None else 0.0
    if shadow:
        ground_shadow(cr, x, y + 4 * s, (sw + 30) * s, 0.26)
    cr.save()
    cr.translate(x, y - hop * s)
    cr.rotate(tilt)
    cr.scale(s * facing * (1 + squash * 0.1), s * (1 - squash * 0.1))
    shirt, pants = c.get("shirt", WHITE), c.get("pants", hexc("#3b5b9a"))
    shoes = c.get("shoes", hexc("#2b2b33"))
    sleeve = c.get("suit") or shirt
    bare_arms = bool(c.get("tunic"))
    # ---- legs
    amp = (60 if run else 26) * stride
    for side in (-1, 1):
        hx = side * pw * 0.45
        fx = side * pw * 0.48 + (amp if side > 0 else -amp)
        fy = -14 - (max(0.0, (stride if side > 0 else -stride)) * (40 if run else 12) if walk is not None else 0)
        leg_col = skin if (c.get("tunic") or c.get("toga") or c.get("skirt")) else pants
        _limb(cr, [(hx, py + 10), (fx * 0.9, (py + fy) / 2 + 6), (fx, fy - 6)], lw, leg_col)
        if c.get("sandals"):
            stroke_line(cr, [(fx - lw * 0.45, fy - 30), (fx + lw * 0.45, fy - 22)], 4, hexc("#8a5a2b"), curve=False)
        ellipse(cr, fx + 10, fy + 2, 30, 15)
        paint(cr, lin(0, fy - 14, 0, fy + 16, [(0, shade(shoes, 0.35)), (1, shade(shoes, -0.2))]), OUTLINE, 4.5)
    # ---- back arm (behind the body)
    shoulder_y = sy + 26 + breathe * 1.5

    def arm(side, pose, prop=None):
        hxy = ARMS.get(pose, ARMS["down"]) if isinstance(pose, str) else pose
        swing = (stride * 30 * (-side)) if walk is not None and pose == "down" else 0.0
        sx = side * (sw - 8)
        ex, ey = sx + side * hxy[0] + swing, shoulder_y + hxy[1]
        mx = (sx + ex) / 2 + side * 16
        my = (shoulder_y + ey) / 2 + 12
        if bare_arms:
            _limb(cr, [(sx, shoulder_y), (mx, my), (ex, ey)], aw, skin)
            _limb(cr, [(sx, shoulder_y), (sx + (mx - sx) * 0.5, shoulder_y + (my - shoulder_y) * 0.5)], aw + 6, shirt)
        else:
            _limb(cr, [(sx, shoulder_y), (mx, my), (ex, ey)], aw, sleeve)
            cr.arc(ex - (ex - mx) * 0.12, ey - (ey - my) * 0.12, aw * 0.42, 0, 2 * math.pi)
            paint(cr, shade(shirt, -0.05), OUTLINE, 3.5)
        _hand(cr, ex, ey, 19, skin)
        if prop:
            prop(cr, ex, ey)

    arm(-1, arms[1], hold_back)
    # ---- torso
    top, bot = sy + breathe, py + 14
    pts = [(-sw, top + 30), (-sw + 18, top + 4), (0, top - 4), (sw - 18, top + 4), (sw, top + 30),
           (pw + 6, bot - 20), (pw - 4, bot), (-pw + 4, bot), (-pw - 6, bot - 20)]
    if c.get("toga") is not None:
        smooth(cr, [(-sw, top + 30), (-sw + 18, top + 4), (0, top - 4), (sw - 18, top + 4), (sw, top + 30),
                    (pw + 30, -60), (pw + 20, -24), (-pw - 20, -24), (-pw - 30, -60)])
        paint(cr, lin(0, top, 0, 0, [(0, shade(shirt, 0.2)), (1, shade(shirt, -0.12))]), OUTLINE, 5)
        smooth(cr, [(-sw + 4, top + 20), (-sw + 30, top + 6), (sw - 10, bot - 60), (pw + 26, -40), (pw - 10, -26),
                    (-sw + 30, top + 90)])     # the blue sash draped across
        paint(cr, lin(-sw, top, sw, 0, [(0, shade(c["toga"], 0.25)), (1, shade(c["toga"], -0.2))]), OUTLINE, 5)
        for k in range(3):
            stroke_line(cr, [(-sw + 40 + k * 30, top + 40 + k * 20), (sw - 30 - k * 10, bot - 50 + k * 30)], 3,
                        alpha(OUTLINE, 0.25))
    elif c.get("tunic"):
        smooth(cr, [(-sw, top + 30), (-sw + 18, top + 4), (0, top - 4), (sw - 18, top + 4), (sw, top + 30),
                    (pw + 18, py + 60), (pw + 10, py + 80), (-pw - 10, py + 80), (-pw - 18, py + 60)])
        paint(cr, lin(0, top, 0, py + 80, [(0, shade(shirt, 0.3)), (1, shade(shirt, -0.2))]), OUTLINE, 5)
        rrect(cr, -pw - 8, py - 26, 2 * pw + 16, 24, 8)
        paint(cr, lin(0, py - 26, 0, py, [(0, shade(c["belt"], 0.3)), (1, shade(c["belt"], -0.2))]), OUTLINE, 4)
        for k in range(5):
            xx = -pw + k * pw * 0.5
            stroke_line(cr, [(xx, py + 6), (xx * 1.08, py + 74)], 3, alpha(OUTLINE, 0.3), curve=False)
    else:
        if c.get("skirt"):
            smooth(cr, [(-pw - 4, py - 30), (pw + 4, py - 30), (pw + 34, py + 70), (-pw - 34, py + 70)])
            paint(cr, lin(0, py - 30, 0, py + 70, [(0, shade(pants, 0.25)), (1, shade(pants, -0.2))]), OUTLINE, 5)
        smooth(cr, pts)
        body_col = c.get("suit") or shirt
        paint(cr, lin(-sw, top, sw, bot, [(0, shade(body_col, 0.3)), (0.5, body_col), (1, shade(body_col, -0.15))]),
              OUTLINE, 5)
        if c.get("suit") is not None:   # open jacket: shirt V and lapels
            cr.move_to(-26, top + 2)
            cr.line_to(26, top + 2)
            cr.line_to(0, top + 120)
            cr.close_path()
            paint(cr, shirt, OUTLINE, 4)
            for side in (-1, 1):
                cr.move_to(side * 26, top + 2)
                cr.line_to(side * 46, top + 60)
                cr.line_to(side * 6, top + 128)
                paint(cr, None, alpha(OUTLINE, 0.7), 4)
        if c.get("apron") is not None:
            ap = c["apron"]
            cr.save()
            smooth(cr, [(-sw + 22, top + 70), (sw - 22, top + 70), (pw + 16, bot + 40), (-pw - 16, bot + 40)])
            cr.clip_preserve()
            paint(cr, WHITE, None, 0)
            for k in range(-4, 5):
                cr.rectangle(k * 28 - 7, top + 60, 14, bot - top + 60)
            cr.set_source_rgba(*ap)
            cr.fill()
            cr.restore()
            smooth(cr, [(-sw + 22, top + 70), (sw - 22, top + 70), (pw + 16, bot + 40), (-pw - 16, bot + 40)])
            paint(cr, None, OUTLINE, 4.5)
        if c.get("collar") is not None:
            for side in (-1, 1):
                cr.move_to(0, top + 4)
                cr.line_to(side * 40, top - 2)
                cr.line_to(side * 30, top + 34)
                cr.close_path()
                paint(cr, c["collar"], OUTLINE, 4)
        if c.get("tie") is not None:
            if c.get("bowtie"):
                for side in (-1, 1):
                    cr.move_to(0, top + 18)
                    cr.line_to(side * 26, top + 6)
                    cr.line_to(side * 26, top + 32)
                    cr.close_path()
                    paint(cr, c["tie"], OUTLINE, 3.5)
                cr.arc(0, top + 19, 7, 0, 2 * math.pi)
                paint(cr, c["tie"], OUTLINE, 3)
            else:
                cr.move_to(-10, top + 8)
                cr.line_to(10, top + 8)
                cr.line_to(14, top + 92)
                cr.line_to(0, top + 108)
                cr.line_to(-14, top + 92)
                cr.close_path()
                paint(cr, lin(0, top, 0, top + 108, [(0, shade(c["tie"], 0.25)), (1, shade(c["tie"], -0.15))]),
                      OUTLINE, 4)
        if c.get("stethoscope"):    # tubing around the neck, chest piece on the front
            stroke_line(cr, [(-34, top + 4), (-40, top + 70), (-12, top + 120), (14, top + 112)], 9, OUTLINE)
            stroke_line(cr, [(-34, top + 4), (-40, top + 70), (-12, top + 120), (14, top + 112)], 5,
                        hexc("#3a3e48"))
            stroke_line(cr, [(34, top + 4), (40, top + 60)], 9, OUTLINE)
            stroke_line(cr, [(34, top + 4), (40, top + 60)], 5, hexc("#3a3e48"))
            cr.arc(20, top + 112, 14, 0, 2 * math.pi)
            paint(cr, rad(16, top + 106, 18, [(0, WHITE), (1, hexc("#9aa4b4"))]), OUTLINE, 4)
        if c.get("build") == "kid" and c.get("tie") is not None and c.get("suit") is None:
            for side in (-1, 1):   # school-shirt collar points
                cr.move_to(0, top + 4)
                cr.line_to(side * 34, top)
                cr.line_to(side * 24, top + 26)
                cr.close_path()
                paint(cr, WHITE, OUTLINE, 3.5)
    # ---- head
    cr.save()
    cr.translate(0, hy + breathe * 2)
    cr.rotate(math.sin(t * 1.7 + ph) * 0.02 if bob else 0.0)
    head(cr, t, 0, 0, hr, who, eyes, mouth, (look[0] * facing, look[1]), brows, turn, lid, blush, sweat, **kw)
    cr.restore()
    # ---- front arm
    arm(1, arms[0], hold)
    cr.restore()


# ---------------------------------------------------------------- animals
def tortoise(cr, t, x, y, s=1.0, facing=1, eyes="open", mouth="smile", look=(0.3, 0.0), walk=None, headband=False,
             shadow=True, tilt=0.0, seed=0):
    """Side-view tortoise, feet on the ground at (x, y), facing right (facing=-1 for left). Shell ~250 px long."""
    if shadow:
        ground_shadow(cr, x, y + 4 * s, 140 * s, 0.26)
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s * facing, s)
    st = math.sin(walk) if walk is not None else 0.0
    skin = hexc("#9fcf6a")
    # legs
    for k, lx in enumerate((-70, -30, 40, 80)):
        sw = st * 16 * (1 if k % 2 else -1)
        rrect(cr, lx - 22 + sw, -70, 44, 70, 18)
        paint(cr, lin(0, -70, 0, 0, [(0, skin), (1, shade(skin, -0.25))]), OUTLINE, 4.5)
        for j in range(3):
            cr.arc(lx - 12 + j * 12 + sw, -6, 4, 0, 2 * math.pi)
            paint(cr, hexc("#f4f0dc"), None, 0)
    # tail
    smooth(cr, [(-118, -62), (-150, -50), (-118, -42)])
    paint(cr, skin, OUTLINE, 4)
    # neck + head
    hb = math.sin(t * 3 + seed) * 4
    smooth(cr, [(80, -110), (130, -150 + hb), (165, -140 + hb), (150, -90), (100, -70)])
    paint(cr, lin(0, -150, 0, -70, [(0, shade(skin, 0.2)), (1, shade(skin, -0.15))]), OUTLINE, 4.5)
    hx, hy = 170, -165 + hb
    ellipse(cr, hx, hy, 58, 50)
    paint(cr, rad(hx - 15, hy - 20, 70, [(0, shade(skin, 0.35)), (1, shade(skin, -0.12))]), OUTLINE, 5)
    for ex, rx in ((hx + 4, 17), (hx + 34, 15)):
        _eye(cr, ex, hy - 10, rx, rx * 1.25, look, eyes)
        if eyes == "half":
            _lid(cr, ex, hy - 10, rx, rx * 1.25, 0.5, shade(skin, 0.2))
    ellipse(cr, hx + 26, hy + 18, 9, 5)
    paint(cr, alpha(BLUSH, 0.5), None, 0)
    cr.save()
    cr.translate(hx + 26, hy + 22)
    cr.scale(0.8, 0.8)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    if headband:
        rrect(cr, hx - 52, hy - 46, 100, 18, 8)
        paint(cr, hexc("#e8473f"), OUTLINE, 4)
        smooth(cr, [(hx - 50, hy - 40), (hx - 84, hy - 30 + math.sin(t * 8) * 6), (hx - 80, hy - 20),
                    (hx - 50, hy - 32)])
        paint(cr, hexc("#e8473f"), OUTLINE, 3.5)
    # shell
    cr.new_path()
    cr.move_to(-130, -60)
    cr.curve_to(-130, -210, 130, -210, 130, -60)
    cr.close_path()
    shell = hexc("#5f9e45")
    paint(cr, rad(-30, -170, 200, [(0, shade(shell, 0.4)), (0.6, shell), (1, shade(shell, -0.3))]), OUTLINE, 5.5)
    cr.save()
    cr.move_to(-130, -60)
    cr.curve_to(-130, -210, 130, -210, 130, -60)
    cr.close_path()
    cr.clip()
    for cx, cy, r in ((0, -150, 40), (-78, -112, 36), (78, -112, 36), (-40, -88, 26), (40, -88, 26)):
        pts = [(cx + r * math.cos(a), cy + r * 0.8 * math.sin(a)) for a in [math.pi / 3 * k + math.pi / 6
                                                                             for k in range(6)]]
        smooth(cr, pts)
        paint(cr, alpha(shade(shell, 0.25), 0.8), alpha(hexc("#2f5a24"), 0.8), 4)
    cr.restore()
    rrect(cr, -138, -72, 276, 22, 11)
    paint(cr, lin(0, -72, 0, -50, [(0, hexc("#e8d38a")), (1, hexc("#b89a4a"))]), OUTLINE, 4.5)
    ellipse(cr, -50, -168, 40, 12, -0.25)
    paint(cr, alpha(WHITE, 0.35), None, 0)
    cr.restore()


JELLY = hexc("#ffb3c7")
JELLY_IN = hexc("#e8333f")


def _tentacles(cr, t, s, n, r, length, col, seed=0):
    for k in range(n):
        x0 = -r * 0.85 + 1.7 * r * k / (n - 1)
        pts = []
        for j in range(7):
            u = j / 6
            pts.append((x0 * (1 - 0.2 * u) + math.sin(t * 2.5 + k * 1.3 + u * 4 + seed) * 10 * u,
                        u * length))
        stroke_line(cr, pts, 3.2, alpha(col, 0.85))


def jellyfish(cr, t, x, y, s=1.0, eyes="open", mouth="smile", look=(0.0, 0.0), glow=1.0, pulse=True, age=0.0,
              tilt=0.0, seed=0, tentacles=True, blush=True):
    """The immortal jellyfish: a see-through bell with its bright red stomach, a fringe of tentacles and a face.
    (x, y) is the bell centre. `age` 0..1 greys and droops it."""
    p = math.sin(t * 3.0 + seed) if pulse else 0.0
    cr.save()
    cr.translate(x, y + p * 6 * s)
    cr.rotate(tilt)
    cr.scale(s * (1 + 0.05 * p), s * (1 - 0.05 * p))
    if glow:
        soft_disc(cr, 0, 10, 190, alpha(hexc("#ffd6e4"), 0.35 * glow))
    col = tuple(a + (b - a) * age for a, b in zip(JELLY, hexc("#b9aab4")))
    if tentacles:
        _tentacles(cr, t, s, 14, 92, 170 - 50 * age, shade(col, -0.1), seed)
        for k in range(4):     # frilly mouth arms in the middle
            xx = -30 + k * 20
            stroke_line(cr, [(xx, 20), (xx + math.sin(t * 2 + k) * 8, 70), (xx - 4, 110)], 7, alpha(shade(col, 0.1),
                                                                                                    0.8))
    cr.new_path()
    cr.move_to(-100, 26)
    cr.curve_to(-110, -110, 110, -110, 100, 26)
    for k in range(8):      # scalloped rim
        x0 = 100 - k * 25
        cr.curve_to(x0 - 6, 40, x0 - 19, 40, x0 - 25, 26)
    cr.close_path()
    cr.set_source(rad(-20, -60, 150, [(0, (1, 1, 1, 0.95)), (0.35, alpha(col, 0.85)), (1, alpha(shade(col, -0.2),
                                                                                                0.8))]))
    cr.fill_preserve()
    cr.set_source_rgba(*alpha(shade(col, -0.45), 0.9))
    cr.set_line_width(4.5)
    cr.stroke()
    # the bright red stomach (as in the real animal), seen through the bell
    smooth(cr, [(-18, -60), (0, -74), (18, -60), (14, -38), (0, -32), (-14, -38)])
    paint(cr, alpha(tuple(a + (b - a) * age for a, b in zip(JELLY_IN, hexc("#8a6a74"))), 0.6), None, 0)
    for k in range(4):      # radial canals
        a = math.pi * (1.15 + 0.7 * k / 3)
        stroke_line(cr, [(0, -50), (math.cos(a) * 92, -50 + math.sin(a) * 40)], 3, alpha(JELLY_IN, 0.25))
    ellipse(cr, -40, -62, 26, 12, -0.5)
    paint(cr, alpha(WHITE, 0.8), None, 0)
    for side in (-1, 1):
        _eye(cr, side * 32, -12, 15, 19, look, eyes)
        if eyes == "half":
            _lid(cr, side * 32, -12, 15, 19, 0.5, col)
    if blush:
        for side in (-1, 1):
            ellipse(cr, side * 56, 8, 12, 7)
            paint(cr, alpha(hexc("#ff6f91"), 0.55), None, 0)
    cr.save()
    cr.translate(0, 14)
    cr.scale(0.85, 0.85)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    cr.restore()


def polyp(cr, t, x, y, s=1.0, eyes="happy", mouth="smile", look=(0.0, 0.0), sway=1.0, bonnet=False, seed=0):
    """A baby polyp: a little stalk on a rock with a crown of tiny tentacles. (x, y) = where it stands."""
    sw = math.sin(t * 1.8 + seed) * 0.08 * sway
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(sw)
    stem = hexc("#ffc2d1")
    smooth(cr, [(-14, 0), (-10, -80), (-22, -120), (22, -120), (10, -80), (14, 0)])
    paint(cr, lin(-20, 0, 20, 0, [(0, shade(stem, -0.1)), (0.5, shade(stem, 0.3)), (1, shade(stem, -0.15))]),
          OUTLINE, 4)
    for k in range(9):
        a = math.pi * (1.05 + 0.9 * k / 8)
        ln = 46 + 6 * math.sin(t * 3 + k)
        stroke_line(cr, [(math.cos(a) * 22, -140 + math.sin(a) * 10),
                         (math.cos(a) * ln, -150 + math.sin(a) * ln * 0.9)], 6, alpha(shade(stem, -0.05), 0.95))
    ellipse(cr, 0, -142, 40, 34)
    paint(cr, rad(-10, -155, 50, [(0, WHITE), (0.5, stem), (1, shade(stem, -0.15))]), OUTLINE, 4.5)
    for side in (-1, 1):
        _eye(cr, side * 14, -146, 8, 10, look, eyes)
    cr.save()
    cr.translate(0, -128)
    cr.scale(0.5, 0.5)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    if bonnet:
        cr.new_path()
        cr.arc(0, -160, 40, math.pi * 1.0, math.pi * 2.0)
        cr.close_path()
        paint(cr, lin(0, -200, 0, -160, [(0, hexc("#bfe6ff")), (1, hexc("#86c6f0"))]), OUTLINE, 4)
        cr.arc(0, -203, 8, 0, 2 * math.pi)
        paint(cr, hexc("#ffffff"), OUTLINE, 3)
    cr.restore()


def jelly_blob(cr, t, x, y, s=1.0, eyes="closed", mouth="flat", seed=0):
    """The shrunken blob the old jellyfish turns into on the sea floor."""
    k = 1 + 0.04 * math.sin(t * 2 + seed)
    cr.save()
    cr.translate(x, y)
    cr.scale(s * k, s / k)
    smooth(cr, [(-60, 0), (-56, -40), (-20, -62), (24, -60), (58, -36), (62, 0)])
    paint(cr, rad(-15, -40, 80, [(0, WHITE), (0.4, JELLY), (1, shade(JELLY, -0.25))]), alpha(shade(JELLY, -0.5), 0.9),
          4.5)
    ellipse(cr, 0, -26, 16, 12)
    paint(cr, alpha(JELLY_IN, 0.6), None, 0)
    for side in (-1, 1):
        _eye(cr, side * 22, -34, 9, 11, (0, 0), eyes)
    cr.save()
    cr.translate(0, -16)
    cr.scale(0.5, 0.5)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    cr.restore()


def fish(cr, t, x, y, s=1.0, facing=1, mouth_open=0.0, eyes="open", col=hexc("#ff9a3c"), seed=0):
    """A chunky cartoon fish centred at (x, y), facing right."""
    cr.save()
    cr.translate(x, y + math.sin(t * 3 + seed) * 6 * s)
    cr.scale(s * facing, s)
    wag = math.sin(t * 9 + seed) * 0.25
    cr.save()
    cr.translate(-90, 0)
    cr.rotate(wag)
    smooth(cr, [(10, 0), (-60, -50), (-46, 0), (-60, 50)])
    paint(cr, lin(-60, 0, 10, 0, [(0, shade(col, -0.2)), (1, col)]), OUTLINE, 5)
    cr.restore()
    m = 0.15 + 0.5 * mouth_open
    cr.new_path()
    cr.move_to(110, -26 * m)
    cr.curve_to(60, -110, -110, -90, -100, 0)
    cr.curve_to(-110, 90, 60, 110, 110, 26 * m)
    cr.line_to(70, 0)
    cr.close_path()
    paint(cr, rad(10, -40, 140, [(0, shade(col, 0.45)), (0.6, col), (1, shade(col, -0.25))]), OUTLINE, 5.5)
    smooth(cr, [(-10, -64), (20, -110), (50, -66)])
    paint(cr, shade(col, -0.1), OUTLINE, 4.5)
    for k in range(3):
        cr.arc(-30 + k * 26, 10, 22, -0.9, 0.9)
        paint(cr, None, alpha(OUTLINE, 0.3), 3)
    _eye(cr, 50, -22, 18, 22, (0.5, 0), eyes)
    cr.restore()


def portrait(cr, t, start, x, y, r, who, eyes="open", mouth="smile", brows=None, look=(0.0, 0.0), sweat=False,
             bg=hexc("#ffd84d"), end=None, **kw):
    """A round 'reaction' bubble with a character's head and shoulders, popping in at `start`."""
    from .polish import appear, soft_disc
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start, 0.35)
    if end is not None and t > end:
        k *= 1 - min(1.0, (t - end) / 0.2)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    soft_disc(cr, 0, 10, r * 1.08, (0, 0, 0, 0.35))
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source(rad(-r * 0.3, -r * 0.4, r * 1.4, [(0, shade(bg, 0.45)), (1, shade(bg, -0.15))]))
    cr.fill()
    cr.save()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.clip()
    c = dict(CAST.get(who, CAST["kid"]))
    c.update(kw)
    body = c.get("suit") or c.get("shirt", WHITE)
    ellipse(cr, 0, r * 1.05, r * 0.95, r * 0.6)
    paint(cr, lin(0, r * 0.5, 0, r * 1.6, [(0, shade(body, 0.2)), (1, shade(body, -0.2))]), OUTLINE, 5)
    head(cr, t, 0, -r * 0.08, r * 0.6, who, eyes, mouth, look, brows, 0.0, 0.0, True, sweat, **kw)
    cr.restore()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    paint(cr, None, OUTLINE, 7)
    cr.restore()



CROC = hexc("#5fae4a")


def crocodile(cr, t, x, y, s=1.0, facing=1, eyes="half", jaw=0.15, arms=("hips", "down"), brows=None, bob=True,
              hold=None, shadow=True, seed=0):
    """A big upright cartoon crocodile standing with its feet at (x, y), snout pointing toward `facing`.
    `jaw` 0..1 opens the mouth (teeth showing). `hold(cr, hx, hy)` draws a prop in the front hand."""
    if shadow:
        ground_shadow(cr, x, y + 4 * s, 120 * s, 0.26)
    b = math.sin(t * 2.0 + seed) * 3 if bob else 0.0
    cr.save()
    cr.translate(x, y + b * s)
    cr.scale(s * facing, s)
    sk = CROC
    belly = hexc("#e8e0a8")
    # tail
    smooth(cr, [(-60, -120), (-150, -90), (-230, -40 + 10 * math.sin(t * 2 + seed)), (-250, -20), (-150, -40),
                (-60, -60)])
    paint(cr, lin(-250, 0, -60, 0, [(0, shade(sk, -0.2)), (1, sk)]), OUTLINE, 5)
    for k in range(5):
        xx = -80 - k * 34
        cr.move_to(xx - 10, -96 + k * 12)
        cr.line_to(xx, -116 + k * 14)
        cr.line_to(xx + 10, -96 + k * 12)
        paint(cr, shade(sk, -0.25), OUTLINE, 3)
    # legs
    for side in (-1, 1):
        lx = side * 44
        rrect(cr, lx - 26, -110, 52, 104, 22)
        paint(cr, lin(0, -110, 0, 0, [(0, sk), (1, shade(sk, -0.25))]), OUTLINE, 5)
        ellipse(cr, lx + 14, -8, 40, 16)
        paint(cr, shade(sk, -0.1), OUTLINE, 4.5)
    # back arm
    def arm(side, pose, prop=None):
        hxy = {"down": (20, 120), "hips": (60, 70), "wave": (70, -110), "up": (20, -150), "point": (150, -10),
               "hold": (90, 40), "out": (130, 20), "chin": (-40, -40), "shrug": (90, -30), "face": (-30, -90),
               "fist": (60, -130)}.get(pose, (20, 120)) if isinstance(pose, str) else pose
        sx, sy = side * 66, -330
        ex, ey = sx + side * hxy[0], sy + hxy[1]
        mx, my = (sx + ex) / 2 + side * 14, (sy + ey) / 2 + 12
        stroke_line(cr, [(sx, sy), (mx, my), (ex, ey)], 38, OUTLINE)
        stroke_line(cr, [(sx, sy), (mx, my), (ex, ey)], 29, sk)
        for k in range(3):
            a = -0.6 + 0.6 * k
            stroke_line(cr, [(ex, ey), (ex + side * math.cos(a) * 22, ey + math.sin(a) * 22)], 11, OUTLINE)
            stroke_line(cr, [(ex, ey), (ex + side * math.cos(a) * 22, ey + math.sin(a) * 22)], 6, sk)
        if prop:
            prop(cr, ex, ey)
    arm(-1, arms[1])
    # body
    smooth(cr, [(-80, -360), (0, -380), (80, -360), (96, -200), (80, -90), (0, -70), (-80, -90), (-96, -200)])
    paint(cr, rad(-30, -300, 300, [(0, shade(sk, 0.35)), (0.6, sk), (1, shade(sk, -0.2))]), OUTLINE, 5.5)
    smooth(cr, [(-46, -340), (46, -340), (58, -200), (40, -100), (-40, -100), (-58, -200)])
    paint(cr, lin(0, -340, 0, -100, [(0, shade(belly, 0.2)), (1, shade(belly, -0.1))]), OUTLINE, 4)
    for k in range(5):
        yy = -310 + k * 44
        stroke_line(cr, [(-50 + abs(k - 2) * 4, yy), (50 - abs(k - 2) * 4, yy)], 3, alpha(OUTLINE, 0.35),
                    curve=False)
    # head: skull + long snout; the lower jaw hinges open
    hy = -420
    ja = jaw * 0.55
    cr.save()
    cr.translate(30, hy + 30)
    cr.rotate(ja)
    smooth(cr, [(-60, -10), (200, -10), (214, 6), (200, 22), (-50, 30)])
    paint(cr, lin(0, -10, 0, 30, [(0, belly), (1, shade(sk, -0.15))]), OUTLINE, 5)
    for k in range(7):
        xx = 10 + k * 28
        cr.move_to(xx - 8, -10)
        cr.line_to(xx, -26)
        cr.line_to(xx + 8, -10)
        paint(cr, WHITE, OUTLINE, 2.5)
    cr.restore()
    if jaw > 0.1:
        cr.move_to(-20, hy + 30)
        cr.line_to(230, hy + 30)
        cr.line_to(230 * math.cos(ja), hy + 30 + 230 * math.sin(ja))
        cr.close_path()
        paint(cr, hexc("#b8384a"), None, 0)
    smooth(cr, [(-70, hy + 30), (-60, hy - 60), (10, hy - 80), (70, hy - 50), (230, hy - 10), (246, hy + 14),
                (230, hy + 34), (-40, hy + 44)])
    paint(cr, rad(0, hy - 60, 220, [(0, shade(sk, 0.4)), (0.6, sk), (1, shade(sk, -0.2))]), OUTLINE, 5.5)
    for k in range(7):
        xx = 50 + k * 26
        cr.move_to(xx - 7, hy + 32)
        cr.line_to(xx, hy + 48)
        cr.line_to(xx + 7, hy + 32)
        paint(cr, WHITE, OUTLINE, 2.5)
    for nx in (226, 236):
        cr.arc(nx, hy - 4, 4, 0, 2 * math.pi)
        paint(cr, OUTLINE, None, 0)
    for k, ex in enumerate((-18, 40)):     # eyes on top of the head
        cr.arc(ex, hy - 70, 34, 0, 2 * math.pi)
        paint(cr, rad(ex, hy - 80, 40, [(0, shade(sk, 0.4)), (1, sk)]), OUTLINE, 5)
        _eye(cr, ex, hy - 72, 22, 24, (0.6, 0.1), eyes)
        if eyes == "half":
            _lid(cr, ex, hy - 72, 22, 24, 0.5, shade(sk, 0.3))
        elif eyes == "angry":
            _lid(cr, ex, hy - 72, 22, 24, 0.4, shade(sk, 0.3), slope=0.4 * (1 if k else -1))
        if brows:
            d = {"up": -14, "angry": 8, "sad": -6}.get(brows, 0)
            stroke_line(cr, [(ex - 22, hy - 104 + (d if k else -d) * 0.5), (ex + 22, hy - 104 - (d if k else -d) * 0.5)],
                        7, OUTLINE, curve=False)
    ellipse(cr, 150, hy + 14, 22, 10)
    paint(cr, alpha(hexc("#ff8a8a"), 0.4), None, 0)
    arm(1, arms[0], hold)
    cr.restore()


def baby_basket(cr, t, x, y, s=1.0, eyes="open", mouth="smile", seed=0):
    """A woven basket with a baby in it; (x, y) is the basket's bottom centre."""
    cr.save()
    cr.translate(x, y + math.sin(t * 2 + seed) * 2)
    cr.scale(s, s)
    head(cr, t, 0, -150, 58, "kid", eyes, mouth, hair=None, blush=True)
    for side in (-1, 1):
        cr.arc(side * 66, -112 + math.sin(t * 6 + side) * 8, 16, 0, 2 * math.pi)
        paint(cr, SKIN["tan"], OUTLINE, 4)
    cr.move_to(-110, -90)
    cr.curve_to(-100, 10, 100, 10, 110, -90)
    cr.close_path()
    paint(cr, lin(0, -90, 0, 0, [(0, hexc("#e0b070")), (1, hexc("#a8763a"))]), OUTLINE, 5)
    cr.save()
    cr.move_to(-110, -90)
    cr.curve_to(-100, 10, 100, 10, 110, -90)
    cr.close_path()
    cr.clip()
    for k in range(-6, 7):
        stroke_line(cr, [(k * 20, -90), (k * 20 + 10, 10)], 3, alpha(OUTLINE, 0.3), curve=False)
    for k in range(4):
        stroke_line(cr, [(-110, -70 + k * 22), (110, -70 + k * 22)], 3, alpha(OUTLINE, 0.3), curve=False)
    cr.restore()
    rrect(cr, -116, -100, 232, 20, 10)
    paint(cr, hexc("#ffd6e4"), OUTLINE, 4)
    cr.restore()



def alien(cr, t, x, y, s=1.0, eyes="open", mouth="smile", wave=False, seed=0, col=hexc("#8fe07a")):
    """A small cute green alien standing with its feet at (x, y)."""
    b = math.sin(t * 3 + seed) * 4
    ground_shadow(cr, x, y + 4 * s, 60 * s, 0.25)
    cr.save()
    cr.translate(x, y + b * s)
    cr.scale(s, s)
    for side in (-1, 1):
        stroke_line(cr, [(side * 20, -60), (side * 26, -4)], 18, OUTLINE, curve=False)
        stroke_line(cr, [(side * 20, -60), (side * 26, -4)], 11, col, curve=False)
    ellipse(cr, 0, -100, 46, 56)
    paint(cr, rad(-14, -120, 70, [(0, shade(col, 0.4)), (1, shade(col, -0.15))]), OUTLINE, 5)
    for side in (-1, 1):
        hy = -180 if (wave and side > 0) else -70
        stroke_line(cr, [(side * 40, -120), (side * 70, hy + 10 * math.sin(t * 8) * (1 if wave and side > 0 else 0))],
                    16, OUTLINE)
        stroke_line(cr, [(side * 40, -120), (side * 70, hy + 10 * math.sin(t * 8) * (1 if wave and side > 0 else 0))],
                    9, col)
    for side in (-1, 1):       # antennae
        stroke_line(cr, [(side * 22, -250), (side * 40, -300)], 6, OUTLINE)
        cr.arc(side * 40, -304, 11, 0, 2 * math.pi)
        paint(cr, hexc("#ffd84d"), OUTLINE, 3.5)
    ellipse(cr, 0, -210, 78, 66)
    paint(cr, rad(-20, -235, 100, [(0, shade(col, 0.45)), (1, shade(col, -0.12))]), OUTLINE, 5.5)
    for side in (-1, 1):
        ellipse(cr, side * 32, -215, 24, 30, side * 0.35)
        paint(cr, rad(side * 26, -228, 34, [(0, hexc("#3a3a58")), (1, hexc("#0e0e1a"))]), OUTLINE, 4)
        ellipse(cr, side * 26, -228, 7, 9)
        paint(cr, alpha(WHITE, 0.9), None, 0)
    cr.save()
    cr.translate(0, -170)
    cr.scale(0.7, 0.7)
    _mouth(cr, 0, 0, mouth, t)
    cr.restore()
    cr.restore()
