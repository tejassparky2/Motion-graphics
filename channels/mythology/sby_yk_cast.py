"""Yakshagana cast and props for the Kannada Shabari reel (scenes_shabari_yk), built on yaksha_kit (never edited: new
looks are dicts made from the kit's looks, new face paints and the new "sby_old" body are registered under sby_ names).
Nothing here is shared with the Hindi shadow-puppet reel (scenes_shabari).

Cast (one look each, kept the same through the reel):
  SHABARI      a simple, gentle old forest woman: no crown, no gold; white hair parted in the middle and tied in a low
               bun, white brows, a few kind wrinkles, a small red bindi, a plain ochre saree with a dark red border, a
               wooden-bead mala. SHABARI_YOUNG is the same woman with dark hair (the years turn it white in sb6).
  RAMA         the Yakshagana hero (the kedige fan headdress) with a blue face and hands, a red jacket, a yellow kase,
               his bow in his hand.
  GURUS        the three old sages of the hermitage (saffron, orange and bark-brown cloth); their clothes on the tree
               later have the same three colours.
  VALMIKI      the poet sage in white (as in the Kannada Hanuman reel), with his palm-leaf Ramayana.
  TULSIDAS     the poet sage in yellow with a namam, with his bound Ramacharitamanasa in red cloth.
  SITA         a small figure in a yellow saree (only in Rama's thought cloud).
Props: berries (one with a bite: the "tasted" fruit), a woven basket, the forest fruits, a leaf plate, a brass water
pot, the two books, the stone altar with fresh flowers, a tree with the sages' wet clothes dripping, tally marks,
the sun and moon racing across the thera, music notes, hearts, light.
"""
import functools
import math

import cairo
import numpy as np

import yaksha_kit as Y
from poster import back, clamp, ease

INK = Y.INK

# ------------------------------------------------------------------ colours

OLD_SKIN = (0.86, 0.62, 0.44)
OCHRE = (0.80, 0.50, 0.17)
OCHRE_DK = (0.58, 0.32, 0.09)
BORDER = (0.50, 0.08, 0.08)
BLOUSE = (0.42, 0.13, 0.10)
HAIR_OLD = (0.94, 0.93, 0.90)
HAIR_OLD_LN = (0.66, 0.64, 0.62)
HAIR_YOUNG = (0.14, 0.10, 0.10)
HAIR_YOUNG_LN = (0.36, 0.28, 0.25)
WRINKLE = (0.52, 0.30, 0.18)
BEAD = (0.48, 0.24, 0.10)
RAMA_BLUE = (0.42, 0.60, 0.93)
BERRY = (0.90, 0.30, 0.10)
BERRY_DK = (0.62, 0.14, 0.05)
FLESH = (0.99, 0.90, 0.62)
WEAVE = (0.86, 0.66, 0.34)
WEAVE_DK = (0.58, 0.40, 0.16)
BARK = (0.66, 0.42, 0.20)
LEAFG = (0.20, 0.62, 0.22)
LEAFG_DK = (0.08, 0.38, 0.12)
STONE = (0.72, 0.42, 0.30)
STONE_DK = (0.50, 0.26, 0.18)
WATER = (0.40, 0.70, 1.0)
LIGHT = (1.0, 0.86, 0.55)

# ------------------------------------------------------------------ face paints (added to the kit's table)

Y.FACES.setdefault("sby_old", dict(base=(0.90, 0.67, 0.50), mark=None, rouge=False, old=True, brow=HAIR_OLD,
                                   lips=(0.70, 0.26, 0.22)))
Y.FACES.setdefault("sby_young", dict(base=(0.90, 0.67, 0.50), mark=None, rouge=False, old=True, brow=HAIR_YOUNG,
                                     lips=(0.74, 0.22, 0.20)))
Y.FACES.setdefault("sby_rama", dict(base=RAMA_BLUE, mark="namam", rouge=False, jaw=True, lips=Y.LIPS))
Y.FACES.setdefault("sby_tulsi", dict(base=Y.SAGE_SKIN, mark="namam", beard=(0.90, 0.89, 0.86), brow=(0.90, 0.89, 0.86),
                                     old=True, rouge=False))


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


# ------------------------------------------------------------------ Shabari's body (kind "sby_old")


def _X(turn):
    def X(x):
        return x + turn * 15.0 * (1 - min(1.0, (x / 72.0) ** 2))
    return X


def _hair_cols(look):
    age = look.get("sby_age", 1.0)
    return mix(HAIR_YOUNG, HAIR_OLD, age), mix(HAIR_YOUNG_LN, HAIR_OLD_LN, age)


def hair_back(ctx):
    """Her hair behind the face, down to the jaw, and a low bun showing at the side of the neck."""
    cr, look = ctx.cr, ctx.look
    col, ln = _hair_cols(look)
    cr.translate(ctx.p["turn"] * 5, Y.FACE_C)
    Y.shape(cr, [(-66, -84), (-86, -30), (-88, 30), (-74, 76), (74, 76), (88, 30), (86, -30), (66, -84), (0, -102)],
            col, 5.0)
    bx = 70 - 30 * ctx.p["turn"]
    Y.dot(cr, bx + 6, 96, 30, mix(col, ln, 0.25), 5.0)       # the bun at the nape
    for k in range(3):
        a = 0.6 + 0.9 * k
        Y.stroke(cr, [(bx + 6 + 10 * math.cos(a), 96 + 10 * math.sin(a)),
                      (bx + 6 + 24 * math.cos(a + 0.9), 96 + 24 * math.sin(a + 0.9))], 2.4, ln)
    for x, y in Y.along([(bx - 14, 78), (bx - 2, 68), (bx + 16, 66)], 4):     # a small string of jasmine buds
        Y.dot(cr, x, y, 4.0, Y.WHITE, 1.6)


def hair_front(ctx):
    """The hairline: parted in the middle and pulled back, with strands; plain ears with small brass studs."""
    cr, look, p = ctx.cr, ctx.look, ctx.p
    col, ln = _hair_cols(look)
    X = _X(p["turn"])
    cr.translate(0, Y.FACE_C)
    for sd in (-1, 1):                                      # ears first, the hair over their tops
        Y.oval(cr, X(sd * 68), -4, 10, 20, look.get("skin", OLD_SKIN), 3.0)
        Y.dot(cr, X(sd * 69), 18, 5.0, Y.GOLD_DK, 2.0)
    pts = [(-72, -30), (-70, -72), (-46, -96), (-16, -104), (0, -100), (16, -104), (46, -96), (70, -72), (72, -30),
           (60, -50), (40, -66), (14, -74), (0, -70), (-14, -74), (-40, -66), (-60, -50)]
    Y.shape(cr, [(X(x), y) for x, y in pts], col, 4.5)
    for sd in (-1, 1):                                      # strands combed back from the parting
        for k in range(4):
            x0 = sd * (8 + 14 * k)
            Y.stroke(cr, [(X(x0), -72 + 2 * k), (X(x0 * 1.5), -86 + 4 * k), (X(sd * (30 + 14 * k)), -98 + 6 * k)],
                     2.4, ln)
    Y.stroke(cr, [(X(0), -100), (X(0), -72)], 2.6, ln)         # the parting
    Y.dot(cr, X(0), -42, 6.0, Y.RED, 2.0)                    # a small kumkum bindi
    ctx.mark("crown", 0, -120)


def wrinkles(ctx):
    """A few kind lines: the forehead, the corners of the eyes, round the mouth."""
    cr, look, p = ctx.cr, ctx.look, ctx.p
    age = look.get("sby_age", 1.0)
    if age < 0.3:
        return
    a = 0.75 * min(1.0, (age - 0.3) / 0.5)
    X = _X(p["turn"])
    cr.translate(0, Y.FACE_C)
    for y, w in ((-60, 30), (-52, 22)):
        Y.stroke(cr, [(X(-w), y + 2), (X(-w * 0.4), y - 1), (X(w * 0.4), y - 1), (X(w), y + 2)], 2.4, WRINKLE,
                 alpha=a)
    for sd in (-1, 1):
        for k in range(2):                                  # crow's feet
            Y.stroke(cr, [(X(sd * 56), -8 + 8 * k), (X(sd * 64), -12 + 12 * k)], 2.2, WRINKLE, alpha=a)
        Y.stroke(cr, [(X(sd * 16), 16), (X(sd * 26), 34), (X(sd * 28), 52)], 2.6, WRINKLE, alpha=a)   # smile lines
        Y.stroke(cr, [(X(sd * 20), 4), (X(sd * 31), 8), (X(sd * 42), 4)], 2.0, WRINKLE, alpha=0.7 * a)  # under the eyes


def plain_torso(ctx):
    cr, look = ctx.cr, ctx.look
    skin = look.get("skin", OLD_SKIN)
    Y.shape(cr, [(-74, 4), (-80, -80), (-92, -190), (-104, -282), (-96, -314), (-60, -334), (-26, -340), (26, -340),
                 (60, -334), (96, -314), (104, -282), (92, -190), (80, -80), (74, 4)], skin)
    Y.shape(cr, [(-92, -180), (-100, -282), (-60, -326), (0, -304), (60, -326), (100, -282), (92, -180), (0, -172)],
            look.get("blouse", BLOUSE), 5.0)
    sar = look.get("saree", OCHRE)
    Y.shape(cr, [(-90, -186), (-84, -80), (-76, 4), (76, 4), (84, -80), (90, -186), (40, -178), (0, -174),
                 (-40, -178)], mix(sar, INK, 0.12), 5.0)     # the saree wrapped over the waist (no bare midriff)
    Y.shape(cr, [(60, -334), (100, -300), (88, -200), (60, -100), (10, -10), (-60, 4), (-80, -20), (-70, -70),
                 (-10, -150), (40, -240)], sar, 6.0)          # the pallu over the shoulder, across the front
    for k in range(3):                                       # its folds
        Y.stroke(cr, [(70 - 8 * k, -300 + 30 * k), (30 - 10 * k, -200 + 20 * k), (-30 - 8 * k, -80 + 10 * k)], 2.8,
                 INK, alpha=0.4)
    Y.stroke(cr, [(64, -330), (44, -240), (-6, -140), (-66, -60)], 9.0, look.get("border", BORDER))
    for x, y in Y.along([(-50, -318), (-30, -270), (0, -252), (30, -270), (50, -318)], 15):   # the bead mala
        Y.dot(cr, x, y, 6.0, BEAD, 2.0)
    ctx.mark("chest", 0, -230)


def plain_saree(ctx):
    cr, look = ctx.cr, ctx.look
    col = look.get("saree", OCHRE)
    pts = [(-84, -8), (-110, 100), (-128, 240), (-136, 410), (-60, 424), (0, 418), (60, 424), (136, 410), (128, 240),
           (110, 100), (84, -8)]
    Y.shape(cr, pts, col, 6.5)
    for k in range(-3, 4):                                   # the pleats at the front
        Y.stroke(cr, [(k * 9, 20), (k * 16, 200), (k * 22, 416)], 3.0, INK, alpha=0.5)
    Y.stroke(cr, [(-132, 398), (-60, 412), (0, 406), (60, 412), (132, 398)], 16.0, look.get("border", BORDER))
    Y.stroke(cr, [(-84, -6), (0, -12), (84, -6)], 10.0, mix(col, INK, 0.25))


def _arms():
    out = []
    for side in (-1, 1):
        up, lo = Y._arm(side)

        def upper(ctx, up=up):
            up(ctx)
            cr, look = ctx.cr, ctx.look
            cr.save()
            cr.new_path()
            cr.rectangle(-40, -40, 80, 78)
            cr.clip()
            Y.capsule(cr, 27, 24, Y.UARM)
            Y.ink_fill(cr, look.get("blouse", BLOUSE), 5.0)
            cr.restore()
            Y.stroke(cr, [(-25, 37), (25, 37)], 5.0, look.get("border", BORDER))

        def lower(ctx, lo=lo):
            lo(ctx)
            Y.stroke(ctx.cr, [(-20, 108), (20, 108)], 6.0, BEAD)      # one plain wooden bangle
        out.append((upper, lower))
    return out


def _old_parts():
    """Her arms come after her head, so a hand can go over the brow (shading the eyes) or to the lips (tasting)."""
    (uL, lL), (uR, lR) = _arms()
    return [("head", hair_back), ("shinL", Y._shin(-1)), ("shinR", Y._shin(1)), ("footL", Y._foot(-1)),
            ("footR", Y._foot(1)), ("root", plain_saree), ("torso", plain_torso), ("head", Y.head),
            ("head", wrinkles), ("head", hair_front), ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR)]


def kneel_saree(ctx):
    """The saree of a kneeling woman: a wide mound from the waist down to the floor (236 units), her toes behind."""
    cr, look = ctx.cr, ctx.look
    col = look.get("saree", OCHRE)
    for sd in (-1, 1):                                       # the soles of her feet showing behind
        Y.oval(cr, sd * 150, 222, 30, 14, look.get("skin", OLD_SKIN), 4.0)
    pts = [(-84, -8), (-118, 70), (-164, 160), (-196, 214), (-120, 238), (0, 232), (120, 238), (196, 214),
           (164, 160), (118, 70), (84, -8)]
    Y.shape(cr, pts, col, 6.5)
    for k in range(-3, 4):
        Y.stroke(cr, [(k * 9, 20), (k * 22, 130), (k * 34, 228)], 3.0, INK, alpha=0.5)
    Y.stroke(cr, [(-190, 212), (-120, 230), (0, 225), (120, 230), (190, 212)], 14.0, look.get("border", BORDER))
    Y.stroke(cr, [(-84, -6), (0, -12), (84, -6)], 10.0, mix(col, INK, 0.25))


def _kneel_parts():
    (uL, lL), (uR, lR) = _arms()
    return [("head", hair_back), ("root", kneel_saree), ("torso", plain_torso), ("head", Y.head),
            ("head", wrinkles), ("head", hair_front), ("uarmL", uL), ("farmL", lL), ("uarmR", uR), ("farmR", lR)]


Y.KINDS.setdefault("sby_old", _old_parts())             # registered under this module's own name (kit untouched)
Y.KINDS.setdefault("sby_kneel", _kneel_parts())

# ------------------------------------------------------------------ looks

SHABARI = dict(kind="sby_old", face="sby_old", head_s=1.1, skin=OLD_SKIN, hand=OLD_SKIN, saree=OCHRE, border=BORDER,
               blouse=BLOUSE, sby_age=1.0)
SHABARI_YOUNG = dict(SHABARI, face="sby_young", sby_age=0.0)


def shabari_aged(age):
    """Shabari as the years pass: the hair and brows go from dark to white (age 0..1)."""
    if age >= 0.999:
        return SHABARI
    return dict(SHABARI, face="sby_young" if age < 0.5 else "sby_old", sby_age=age)


RAMA = dict(Y.HERO, face="sby_rama", hand=RAMA_BLUE, jacket=Y.RED, sleeve=Y.RED, kase=(Y.YEL, Y.RED, INK, Y.GREEN),
            hem=Y.GREEN, hem_zig=Y.YEL, sash=Y.WHITE, pads=Y.RED)
GURU1 = dict(Y.SAGE)                                                       # saffron and white
GURU2 = dict(Y.SAGE, cloth=(0.99, 0.70, 0.18), cloth2=(0.95, 0.40, 0.10))  # orange
GURU3 = dict(Y.SAGE, cloth=BARK, cloth2=(0.92, 0.80, 0.56))                # bark-brown
GURUS = (GURU1, GURU2, GURU3)
CLOTH_COLS = ((Y.SAFF, Y.WHITE), ((0.99, 0.70, 0.18), (0.95, 0.40, 0.10)), (BARK, (0.92, 0.80, 0.56)))
VALMIKI = dict(Y.SAGE, cloth=Y.WHITE, cloth2=Y.SAFF)
TULSIDAS = dict(Y.SAGE, face="sby_tulsi", cloth=(0.99, 0.84, 0.22), cloth2=Y.RED)
SITA = dict(Y.WOMAN, saree=(0.99, 0.74, 0.12), border=Y.RED, blouse=Y.GREEN)

# ------------------------------------------------------------------ arm poses (upper, forearm, hand) in kit angles

REST = (0.16, 0.30, 0.0)
ANJALI = (0.30, 2.30, 0.0)            # palms joined at the chest
OFFER = (0.70, -0.90, 0.0)            # an arm held out level to the side, palm up (giving)
TO_MOUTH = (0.42, -3.73, -0.2)        # the hand lifted to the mouth (tasting; the same as (0.42, 2.55), wound the
#                                       other way so it blends smoothly from SHOW and to OFFER)
SHOW = (0.90, -2.30, 0.0)             # a hand raised beside the face, showing what it holds
EAT = (0.60, 2.85, -0.3)              # an actor's hand lifted to his mouth (eating)
BASKET = (0.32, 1.45, 0.25)           # the forearm crooked across the waist, carrying the basket
SHADE = (2.70, -1.40, -0.5)           # a hand flat over the brow, shading the eyes (looking far)
BLESS = (0.85, -2.2, 0.0)             # a palm raised beside the face (a blessing)
POINT = (1.30, 0.40, 0.0)             # an arm pointing out to the side
HOLD_UP = (0.55, 1.75, 0.3)           # both hands up in front of the chest (holding a book)


def pose(t, amp=1.0, freq=0.45, ph=0.0, **kw):
    """A pose with the Yakshagana idle sway mixed in (lean/head/shift given in kw are added to the sway)."""
    sh, ln, hd = Y.sway(t, amp, freq, ph)
    p = dict(shift=sh + kw.pop("shift", 0.0), lean=ln + kw.pop("lean", 0.0), head=hd * 0.6 + kw.pop("head", 0.0),
             sash=-ln * 3, breathe=math.sin(t * 2.2 + ph), bend=kw.pop("bend", 0.28))
    p.update(kw)
    return p


@functools.lru_cache(maxsize=4)
def _front_arm_parts(kind):
    """The kit's parts for `kind` with the screen-right arm moved to the very end (drawn over the face and crown)."""
    base = list(Y.KINDS[kind])
    arm = [pp for pp in base if pp[0] in ("uarmR", "farmR")]
    return [pp for pp in base if pp[0] not in ("uarmR", "farmR")] + arm


def fig(c, look, x, feet, s, t, p, flip=False, alpha=1.0, shadow=0.5, front=False):
    """Draw a figure with a soft floor shadow; front=True draws the right arm over the face (a hand at the brow)."""
    if shadow:
        Y.floor_shadow(c, x + p.get("shift", 0.0) * s, feet, 280 * s, shadow * alpha)
    if not front:
        return Y.figure(c, look, x, feet, s, t, p, flip, alpha)
    kind = look.get("kind", "actor")
    old = Y.KINDS[kind]
    Y.KINDS[kind] = _front_arm_parts(kind)
    try:
        return Y.figure(c, look, x, feet, s, t, p, flip, alpha)
    finally:
        Y.KINDS[kind] = old


def U(c, p):
    """Device point -> the context's user space."""
    return Y.to_user(c, p)


def kneel(c, look, x, floor, s, t, p, alpha=1.0, shadow=0.5):
    """Shabari kneeling on the floor line (her waist 236 units above it), her saree spread round her knees."""
    hip_h = Y.leg_solve(p.get("bend", 0.15), 0.0)[3]
    if shadow:
        Y.floor_shadow(c, x + p.get("shift", 0.0) * s, floor, 320 * s, shadow * alpha)
    return Y.figure(c, dict(look, kind="sby_kneel"), x, floor + (hip_h - 236.0) * s, s, t, p, False, alpha)


# ------------------------------------------------------------------ fruit


def berry(cr, x, y, r, bite=0.0, alpha=1.0, col=BERRY, rot=0.0):
    """A round forest berry (ber) with a shine and a little stem; bite 0..1 takes a bite out of its upper right."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.push_group()
    lw = max(2.0, r * 0.12)
    cr.new_path()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    Y.ink_fill(cr, col, lw)
    if bite > 0.01:                                          # a bite out of the upper right, with teeth marks
        bx, by = r * (1.15 - 0.35 * bite), -r * (0.62 - 0.12 * bite)
        rb = r * 0.58

        def bite_path(grow):
            cr.new_path()
            for i in range(73):
                a = 2 * math.pi * i / 72
                rr = rb * (1 - 0.07 * (1 + math.cos(14 * a))) + grow
                (cr.move_to if i == 0 else cr.line_to)(bx + rr * math.cos(a), by + rr * math.sin(a))
            cr.close_path()
        cr.save()
        cr.new_path()
        cr.arc(0, 0, r - lw * 0.5, 0, 2 * math.pi)
        cr.clip()
        bite_path(r * 0.12)                                  # the pale flesh round the bite
        cr.set_source_rgb(*FLESH)
        cr.fill()
        bite_path(0.0)
        cr.set_source_rgb(*INK)
        cr.set_line_width(max(2.0, r * 0.09))
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
        cr.restore()
        cr.save()                                            # then cut the bite itself away
        cr.set_operator(cairo.OPERATOR_CLEAR)
        bite_path(-r * 0.04)
        cr.fill()
        cr.restore()
    Y.oval(cr, -r * 0.35, -r * 0.38, r * 0.22, r * 0.14, (1.0, 0.80, 0.62), 0, rot=-0.6)   # the shine
    Y.stroke(cr, [(-r * 0.1, -r * 0.92), (-r * 0.2, -r * 1.25)], max(2.0, r * 0.12), (0.36, 0.22, 0.08))
    cr.save()
    cr.translate(-r * 0.2, -r * 1.2)
    cr.rotate(-0.9)
    Y.shape(cr, [(0, 0), (r * 0.25, -r * 0.16), (r * 0.6, -r * 0.08), (r * 0.30, r * 0.10)], LEAFG, max(1.5, r * 0.08))
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def fruit(cr, kind, x, y, s=1.0, rot=0.0):
    """One forest fruit, centred, about 60*s across: ber, mango, banana, jamun, guava."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    if kind == "ber":
        berry(cr, 0, 0, 24)
    elif kind == "mango":
        Y.shape(cr, [(-30, 10), (-26, -18), (-4, -32), (22, -26), (34, -4), (28, 20), (6, 32), (-18, 28)],
                (0.99, 0.66, 0.12), 4.0)
        Y.oval(cr, -10, -14, 12, 7, (1.0, 0.86, 0.45), 0, rot=-0.5)
        Y.shape(cr, [(18, -26), (26, -42), (40, -46), (32, -30)], LEAFG, 3.0)
    elif kind == "banana":
        for k in range(3):
            cr.save()
            cr.rotate(-0.25 + 0.25 * k)
            Y.shape(cr, [(-8, -36), (6, -34), (14, -6), (10, 26), (-2, 36), (-6, 20), (0, -4)], (0.99, 0.86, 0.20), 3.5)
            Y.dot(cr, 0, -36, 4, (0.40, 0.26, 0.10))
            cr.restore()
    elif kind == "jamun":
        for k, (dx, dy) in enumerate(((-12, 4), (10, 6), (0, -12), (-2, 18))):
            Y.oval(cr, dx, dy, 12, 14, (0.36, 0.12, 0.42), 3.0)
            Y.dot(cr, dx - 4, dy - 5, 3.0, (0.80, 0.62, 0.86))
    elif kind == "guava":
        Y.dot(cr, 0, 0, 27, (0.62, 0.82, 0.30), 4.0)
        Y.dot(cr, -8, -9, 6, (0.86, 0.96, 0.60))
        Y.stroke(cr, [(0, -27), (2, -36)], 4.0, (0.36, 0.22, 0.08))
    cr.restore()


MIXED = ("mango", "ber", "banana", "jamun", "guava", "ber", "mango", "jamun", "ber")


def basket(cr, x, y, s=1.0, fill=1.0, kinds=None, alpha=1.0, bite_top=0.0):
    """A woven bamboo basket (about 200*s wide), its rim at y, heaped with fruit (fill 0..1). kinds: the fruits
    (None = all berries). bite_top > 0 gives the berry on top a bite."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    n = int(round(9 * clamp(fill)))
    spots = ((-60, -8), (0, -12), (60, -8), (-30, -34), (30, -34), (-80, 6), (80, 6), (0, -54), (-48, -50))
    for k in range(n):                                       # the heap, behind the front of the basket
        sx, sy = spots[k]
        if kinds:
            fruit(cr, kinds[k % len(kinds)], sx, sy, 0.95, rot=0.4 * math.sin(k * 2.1))
        else:
            berry(cr, sx, sy, 24, bite=bite_top if k == n - 1 else 0.0, rot=0.3 * math.sin(k * 1.7))
    body = [(-104, 0), (104, 0), (88, 74), (60, 96), (-60, 96), (-88, 74)]
    Y.shape(cr, body, WEAVE, 5.0, smooth=False)
    for k in range(1, 4):                                    # the weave
        yy = 24 * k
        w = 104 - 16 * k * (k > 2) - 5 * k
        Y.stroke(cr, [(-w + 4, yy), (w - 4, yy)], 3.0, WEAVE_DK, smooth=False)
    for k in range(-4, 5):
        Y.stroke(cr, [(k * 22, 4), (k * 17, 92)], 2.4, WEAVE_DK, smooth=False)
    Y.shape(cr, [(-112, -8), (112, -8), (108, 8), (-108, 8)], WEAVE_DK, 4.5, smooth=False)   # the rim
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def leaf_plate(cr, x, y, w, alpha=1.0):
    """A banana leaf laid on the ground (centred at x, y, w wide)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    h = w * 0.22
    Y.shape(cr, [(-w / 2, 0), (-w * 0.3, -h * 0.55), (0, -h * 0.62), (w * 0.3, -h * 0.55), (w / 2, -h * 0.05),
                 (w * 0.3, h * 0.45), (0, h * 0.5), (-w * 0.3, h * 0.45)], LEAFG, 5.0)
    Y.stroke(cr, [(-w * 0.48, 0), (w * 0.48, -h * 0.04)], 4.0, LEAFG_DK)
    for k in range(-5, 6):
        Y.stroke(cr, [(k * w * 0.08, -2), (k * w * 0.08 + w * 0.04, -h * 0.5)], 2.0, LEAFG_DK, alpha=0.7)
        Y.stroke(cr, [(k * w * 0.08, 2), (k * w * 0.08 + w * 0.04, h * 0.42)], 2.0, LEAFG_DK, alpha=0.7)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def fruit_pile(cr, x, y, n, s=1.0, alpha=1.0):
    """n fruits heaped on a leaf (they appear one by one as n grows), the bottom of the heap at y."""
    if alpha <= 0.01:
        return
    spots = []
    rows = ((0, 7), (1, 6), (2, 5), (3, 3), (4, 1))
    for r, m in rows:
        for i in range(m):
            spots.append(((i - (m - 1) / 2) * 52, -10 - 40 * r))
    k = int(min(len(spots), max(0, n)))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for i in range(k):
        sx, sy = spots[i]
        fruit(cr, MIXED[i % len(MIXED)], sx, sy, 0.85, rot=0.5 * math.sin(i * 1.9))
    cr.restore()


def lota(cr, x, y, s=1.0, tilt=0.0, pour=0.0, t=0.0, fall=200.0):
    """A brass water pot held at (x, y) (its neck), tilted by tilt (radians, + = spout to the right); pour 0..1 runs
    a stream of water from its mouth down fall px."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s, s)
    brass = (0.86, 0.62, 0.18)
    Y.shape(cr, [(-24, -20), (24, -20), (20, -4), (46, 22), (54, 56), (40, 88), (0, 100), (-40, 88), (-54, 56),
                 (-46, 22), (-20, -4)], brass, 5.0)
    Y.oval(cr, 0, -20, 30, 9, (0.62, 0.40, 0.10), 4.0)
    Y.stroke(cr, [(-48, 50), (48, 50)], 4.0, (1.0, 0.86, 0.45))
    Y.oval(cr, -18, 36, 9, 18, (1.0, 0.90, 0.60), 0, rot=0.3)
    cr.restore()
    if pour > 0.01:
        mx = x + math.cos(tilt) * 30 * s
        my = y - 18 * s + math.sin(tilt) * 30 * s
        L = fall * clamp(pour * 1.5)
        pts = [(mx + 6 * math.sin(t * 9 + i), my + L * i / 6) for i in range(7)]
        Y.stroke(cr, pts, 16 * s, (0.20, 0.42, 0.78), alpha=0.9)
        Y.stroke(cr, pts, 8 * s, WATER, alpha=0.95)
        for i in range(4):
            u = (t * 2.2 + i / 4) % 1.0
            Y.dot(cr, mx + 22 * math.sin(i * 2.3) * u, my + L + 10 - 30 * u, 6 * (1 - u) + 1, (0.75, 0.90, 1.0))


# ------------------------------------------------------------------ books


@functools.lru_cache(maxsize=16)
def _title(text, size, col=(0.30, 0.12, 0.05)):
    return Y.kn_surface(text, size, col, col, 0.0, None, 0.0)


def palm_book(cr, t, x, y, s, open_=1.0, title="ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣ", alpha=1.0, glow_a=0.0):
    """Valmiki's palm-leaf book (ole gari), held flat: a stack of long leaves between two wooden covers, a red string
    through them; open_ lifts the top cover away and shows the title written on the top leaf (about 520*s wide)."""
    if alpha <= 0.01:
        return
    if glow_a > 0.01:
        Y.glow(cr, x, y - 40 * s, 460 * s, 0.5 * glow_a, (1.0, 0.82, 0.42))
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    leaf = (0.93, 0.80, 0.52)
    wood = (0.50, 0.20, 0.08)
    for k in range(4):
        yy = 34 - 9 * k
        Y.shape(cr, [(-250, yy - 22), (250, yy - 22), (262, yy), (250, yy + 22), (-250, yy + 22), (-262, yy)],
                wood if k == 0 else leaf, 5.0, smooth=False)
    Y.shape(cr, [(-250, -40), (250, -40), (262, -12), (250, 16), (-250, 16), (-262, -12)], leaf, 5.0, smooth=False)
    for xx in (-215, 215):
        Y.dot(cr, xx, -12, 9, (0.30, 0.14, 0.06), 2.5)
    if open_ > 0.3:
        tx = _title(title, 64)
        a = clamp((open_ - 0.3) / 0.4)
        sc = min(1.0, 370 / tx.get_width(), 46 / tx.get_height())
        cr.save()
        cr.translate(-tx.get_width() * sc / 2, -12 - tx.get_height() * sc / 2)
        cr.scale(sc, sc)
        cr.set_source_surface(tx, 0, 0)
        cr.paint_with_alpha(a)
        cr.restore()
    Y.stroke(cr, [(-215, -12), (-240, 30), (-256, 70), (-242, 104)], 4.0, Y.RED)
    Y.dot(cr, -242, 108, 10, Y.GOLD, 3.0)
    lift = ease(open_)
    if lift < 0.98:
        cr.save()
        cr.translate(250, -40)
        cr.rotate(-1.9 * lift)
        cr.translate(-250, 40)
        Y.shape(cr, [(-250, -62), (250, -62), (262, -40), (250, -18), (-250, -18), (-262, -40)], wood, 5.0,
                smooth=False)
        for xx in (-120, 0, 120):
            Y.dot(cr, xx, -40, 7, Y.GOLD, 2.5)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def manas_book(cr, t, x, y, s, open_=1.0, title="ರಾಮಚರಿತಮಾನಸ", alpha=1.0, glow_a=0.0):
    """Tulsidas's book: a bound book in a red cloth cover with a gold border (about 420*s wide when open); open_ 0..1
    swings the cover open onto two cream pages with lines and the title."""
    if alpha <= 0.01:
        return
    if glow_a > 0.01:
        Y.glow(cr, x, y, 440 * s, 0.5 * glow_a, (1.0, 0.82, 0.42))
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    o = ease(open_)
    w, h = 200, 270
    cr.rectangle(-w - 8, -h / 2 - 8, 2 * w + 16, h + 16)     # the back cover under both pages
    Y.ink_fill(cr, (0.62, 0.06, 0.08), 5.0)
    if o > 0.02:
        cr.rectangle(-w * o, -h / 2, w * o, h)              # the left page (opening out)
        Y.ink_fill(cr, (0.99, 0.95, 0.84), 4.0)
    cr.rectangle(0, -h / 2, w, h)
    Y.ink_fill(cr, (0.99, 0.95, 0.84), 4.0)
    for k in range(7):                                       # lines of writing on the right page
        yy = -h / 2 + 100 + 22 * k
        Y.stroke(cr, [(24, yy), (w - 24, yy)], 3.0, (0.40, 0.26, 0.14), alpha=0.6)
    if o > 0.5:
        for k in range(8):
            yy = -h / 2 + 40 + 26 * k
            Y.stroke(cr, [(-w * o + 24, yy), (-24, yy)], 3.0, (0.40, 0.26, 0.14), alpha=0.6 * clamp((o - 0.5) * 3))
        tx = _title(title, 60, (0.60, 0.06, 0.06))
        sc = min(1.0, (w - 40) / tx.get_width())
        cr.save()
        cr.translate(w / 2 - tx.get_width() * sc / 2, -h / 2 + 50 - tx.get_height() * sc / 2)
        cr.scale(sc, sc)
        cr.set_source_surface(tx, 0, 0)
        cr.paint_with_alpha(clamp((o - 0.5) * 3))
        cr.restore()
    Y.stroke(cr, [(0, -h / 2), (0, h / 2)], 4.0, INK)
    if o < 0.98:                                             # the front cover swinging open (to the left)
        cw = w * (1 - 2 * o)
        cr.rectangle(min(0, cw), -h / 2 - 6, abs(cw), h + 12)
        Y.ink_fill(cr, (0.80, 0.08, 0.10), 5.0)
        if o < 0.5:
            cr.save()
            cr.translate(cw / 2, 0)
            cr.scale(max(0.05, 1 - 2 * o), 1)
            cr.rectangle(-w / 2 + 18, -h / 2 + 18, w - 36, h - 36)
            cr.set_source_rgb(*Y.GOLD)
            cr.set_line_width(6)
            cr.stroke()
            Y.dot(cr, 0, 0, 34, Y.GOLD, 4.0)
            Y.dot(cr, 0, 0, 16, Y.RED, 3.0)
            cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


# ------------------------------------------------------------------ the hermitage: altar, flowers, tree, clothes


def flower(cr, x, y, r, col=(0.99, 0.45, 0.62), wilt=0.0, rot=0.0, centre=Y.YEL):
    """A simple six-petalled flower; wilt 0..1 droops the petals and turns them brown."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    c = mix(col, (0.52, 0.34, 0.18), wilt)
    for i in range(6):
        a = 2 * math.pi * i / 6 - math.pi / 2
        down = wilt * 0.9 * (0.5 + 0.5 * math.sin(a))
        cr.save()
        cr.rotate(a + down * 0.6)
        cr.translate(0, -r * 0.1)
        L = r * (1 - 0.25 * wilt)
        Y.shape(cr, [(0, 0), (-r * 0.36, -L * 0.45), (0, -L), (r * 0.36, -L * 0.45)], c, max(2.0, r * 0.1))
        cr.restore()
    Y.dot(cr, 0, 0, r * 0.32, mix(centre, (0.42, 0.28, 0.12), wilt), max(2.0, r * 0.09))
    cr.restore()


def lotus(cr, x, y, r, wilt=0.0, col=(0.98, 0.52, 0.68)):
    """A pink lotus seen from the side."""
    c = mix(col, (0.55, 0.36, 0.20), wilt)
    cr.save()
    cr.translate(x, y)
    for i, (a, k) in enumerate(((-0.9, 0.8), (0.9, 0.8), (-0.45, 0.95), (0.45, 0.95), (0.0, 1.05))):
        cr.save()
        cr.rotate(a * (1 + 0.6 * wilt))
        L = r * k * (1 - 0.3 * wilt)
        Y.shape(cr, [(0, 0), (-r * 0.30, -L * 0.5), (0, -L), (r * 0.30, -L * 0.5)], c, max(2.0, r * 0.08))
        cr.restore()
    cr.restore()


ALTAR_FLOWERS = ((-120, (0.99, 0.45, 0.62)), (-60, Y.WHITE), (0, (0.99, 0.62, 0.10)), (60, (0.99, 0.45, 0.62)),
                 (120, Y.WHITE))


def altar(cr, t, x, y, s=1.0, fresh=1.0, wilt=0.0, alpha=1.0):
    """The sages' stone altar (vedi) standing on y: three steps of red laterite, a lotus garland draped over it and
    flowers on the top (fresh 0..1 = how bright; wilt 0..1 = drooped and brown)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    for k, (w, h) in enumerate(((300, 70), (240, 70), (180, 60))):
        y0 = -70 * k
        cr.rectangle(-w / 2, y0 - h, w, h)
        Y.ink_fill(cr, STONE if k % 2 == 0 else mix(STONE, STONE_DK, 0.35), 5.0)
        for i in range(int(w / 40)):                         # the laterite's pores
            Y.dot(cr, -w / 2 + 20 + 40 * i + (10 if k % 2 else 0), y0 - h / 2 + 8 * math.sin(i * 1.3), 4.0,
                  STONE_DK)
    Y.stroke(cr, [(-100, -205), (-60, -175), (0, -165), (60, -175), (100, -205)], 3.0, (0.30, 0.50, 0.15))
    for i, (gx, gy) in enumerate(Y.along([(-110, -200), (-60, -170), (0, -160), (60, -170), (110, -200)], 9)):
        lotus(cr, gx, gy + 18, 22, wilt, (0.98, 0.52, 0.68) if i % 2 else (0.99, 0.95, 0.88))
    for i, (fx, col) in enumerate(ALTAR_FLOWERS):
        fy = -212 - 18 * (1 - abs(fx) / 120)
        flower(cr, fx * 0.62, fy, 30, col, wilt, rot=0.2 * math.sin(i * 2.0))
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()
    if fresh > 0.01 and wilt < 0.5:
        for k in range(5):
            u = (t * 0.5 + k / 5) % 1.0
            Y.sparkle(cr, x + (-110 + 55 * k) * s, y - (230 + 120 * u) * s, 16 * s * math.sin(math.pi * u),
                      0.9 * fresh)


def tree(cr, x, y, s=1.0, alpha=1.0):
    """A forest tree standing on y (trunk, a long side branch to the right where clothes hang, a round canopy)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    trunk = (0.45, 0.26, 0.12)
    Y.shape(cr, [(-46, 0), (-34, -300), (-30, -520), (-60, -640), (-20, -620), (0, -560), (30, -640), (60, -630),
                 (34, -520), (40, -300), (60, 0)], trunk, 6.0)
    Y.shape(cr, [(20, -470), (200, -500), (420, -520), (424, -496), (200, -470), (30, -440)], trunk, 5.0)   # branch
    for k in range(4):
        Y.stroke(cr, [(-20 + 12 * k, -40), (-14 + 10 * k, -280)], 3.0, (0.30, 0.16, 0.06), alpha=0.7)
    for (cx, cy, r, col) in ((-150, -690, 150, LEAFG_DK), (130, -720, 160, LEAFG_DK), (0, -800, 190, LEAFG),
                             (-120, -620, 120, LEAFG), (140, -630, 120, LEAFG), (360, -560, 90, LEAFG)):
        Y.dot(cr, cx, cy, r, col, 6.0)
    for k in range(14):                                      # leaves painted on the canopy
        a = k * 2.4
        rr = 60 + 110 * ((k * 0.37) % 1)
        lx, ly = 0 + rr * math.cos(a) * 1.4, -720 + rr * math.sin(a) * 0.8
        cr.save()
        cr.translate(lx, ly)
        cr.rotate(a)
        Y.shape(cr, [(0, -16), (9, 0), (0, 16), (-9, 0)], (0.45, 0.80, 0.30), 2.5)
        cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


CLOTH_XS = (150, 255, 360)         # where the three clothes hang on the branch (tree units, from the trunk)


def clothes(cr, t, x, y, s=1.0, wet=1.0, alpha=1.0, drip_t0=0.0, n_drips=3, show=(1.0, 1.0, 1.0)):
    """The three sages' clothes hanging over the tree's branch (tree at x, y, scale s): long strips in their colours,
    dark and shiny when wet, dripping (wet 0..1). show: each cloth's own opacity (they can be hung one by one)."""
    if alpha <= 0.01:
        return
    bottoms = []
    for k, cx in enumerate(CLOTH_XS):
        if show[k] <= 0.01:
            bottoms.append(None)
            continue
        cr.save()
        cr.push_group()
        cr.translate(x, y)
        cr.scale(s, s)
        drop_in = 30 * (1 - ease(show[k]))
        cr.translate(0, -drop_in)
        c1, c2 = CLOTH_COLS[k]
        top = -490 - 10 * (cx / 420)
        L = 250 + 30 * k
        sw = 6 * math.sin(t * 1.3 + k)
        col = mix(c1, mix(c1, INK, 0.14), wet)
        pts = [(cx - 44, top), (cx + 44, top), (cx + 48 + sw, top + L), (cx + 20 + sw, top + L + 12),
               (cx - 10 + sw, top + L), (cx - 46 + sw, top + L + 8)]
        Y.shape(cr, pts, col, 5.0, smooth=False)
        Y.stroke(cr, [(cx - 44, top + L * 0.7 + 4), (cx + 48 + sw, top + L * 0.7)], 10.0, mix(c2, INK, 0.3 * wet),
                 smooth=False)
        for j in range(3):                                   # folds
            Y.stroke(cr, [(cx - 24 + 24 * j, top + 10), (cx - 24 + 24 * j + sw, top + L - 10)], 2.6, INK, alpha=0.45)
        if wet > 0.1:                                        # wet shine
            Y.stroke(cr, [(cx - 30, top + 30), (cx - 26 + sw * 0.5, top + L * 0.55)], 6.0, (1.0, 1.0, 1.0),
                     alpha=0.35 * wet)
        Y.shape(cr, [(cx - 50, top - 14), (cx + 50, top - 14), (cx + 50, top + 10), (cx - 50, top + 10)], col, 4.0,
                smooth=False)                                # folded over the branch
        bottoms.append((cx + 4 + sw, top + L + 10))
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha * clamp(show[k] * 2))
        cr.restore()
    if wet > 0.1:                                            # drops falling from each hem
        for k, bt in enumerate(bottoms):
            if bt is None:
                continue
            bx, by = bt
            fall = max(40.0, -by - 34)                       # down to the ground under the tree
            for j in range(n_drips):
                u = ((t - drip_t0) * 0.9 + j / n_drips + k * 0.31) % 1.0
                dx, dy = x + bx * s, y + (by + 20 + fall * u * u) * s
                a = wet * alpha * (1 - u * 0.6)
                drop(cr, dx, dy, 13 * s, a)


def drop(cr, x, y, r, a=1.0):
    """A water drop (pointed top)."""
    if a <= 0.01:
        return
    cr.save()
    cr.push_group()
    cr.new_path()
    cr.move_to(x, y - r * 1.8)
    cr.curve_to(x + r * 0.5, y - r * 0.8, x + r, y - r * 0.2, x + r, y + r * 0.2)
    cr.arc(x, y + r * 0.2, r, 0, math.pi)
    cr.curve_to(x - r, y - r * 0.2, x - r * 0.5, y - r * 0.8, x, y - r * 1.8)
    cr.close_path()
    Y.ink_fill(cr, WATER, max(2.0, r * 0.25))
    Y.dot(cr, x - r * 0.35, y, r * 0.25, Y.WHITE)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def puddle(cr, t, x, y, w, a=1.0):
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(w, w * 0.16)
    cr.new_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(0.25, 0.50, 0.90, 0.75 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.8 * a)
    cr.set_line_width(4)
    cr.stroke()
    for k in range(2):                                       # rings from the drops
        u = (t * 0.9 + k * 0.5) % 1.0
        cr.save()
        cr.translate(x + (k - 0.5) * w * 0.5, y)
        cr.scale(w * 0.4 * u + 8, (w * 0.4 * u + 8) * 0.25)
        cr.new_path()
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.80, 0.92, 1.0, 0.8 * a * (1 - u))
        cr.set_line_width(3)
        cr.stroke()


# ------------------------------------------------------------------ waiting: the path, the hut wall, sun and moon


def path(cr, x0, x1, y, top_x, top_y, alpha=1.0, swing=120.0):
    """A winding forest path painted on the thera: wide at the front (between x0 and x1 on line y), snaking back and
    narrowing to a point at the horizon (top_x, top_y), with low green hills along the horizon."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.push_group()
    hills = [(top_x - 520, top_y + 30), (top_x - 300, top_y - 40), (top_x - 60, top_y + 10), (top_x + 200, top_y - 50),
             (top_x + 480, top_y + 20), (top_x + 700, top_y - 20), (top_x + 700, top_y + 140),
             (top_x - 520, top_y + 140)]
    Y.shape(cr, hills, (0.26, 0.58, 0.26), 5.0)
    n = 24
    cx0 = (x0 + x1) / 2
    left, right = [], []
    for i in range(n + 1):
        u = i / n                                            # 0 at the front, 1 at the horizon
        cy = mix(y, top_y, 1 - (1 - u) ** 1.6)
        cx = mix(cx0, top_x, u) + swing * math.sin(u * math.pi * 1.6) * (1 - u)
        w = mix((x1 - x0) / 2, 6.0, u ** 0.8)
        left.append((cx - w, cy))
        right.append((cx + w, cy))
    Y.shape(cr, left + right[::-1], (0.74, 0.52, 0.28), 5.0)
    for k in range(12):                                      # pebbles, bigger near the front
        u = (k + 0.5) / 12
        cy = mix(y, top_y, 1 - (1 - u) ** 1.6)
        cx = mix(cx0, top_x, u) + swing * math.sin(u * math.pi * 1.6) * (1 - u)
        w = mix((x1 - x0) / 2, 6.0, u ** 0.8)
        Y.dot(cr, cx + w * 0.5 * math.sin(k * 2.7), cy, 2 + 7 * (1 - u), (0.60, 0.42, 0.22))
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def tally(cr, x, y, n, s=1.0, alpha=1.0):
    """Tally marks scratched in white on a wall (groups of five), n of them, rows of four groups."""
    if alpha <= 0.01 or n <= 0:
        return
    for i in range(int(n)):
        g, k = divmod(i, 5)
        row, col = divmod(g, 4)
        gx, gy = x + col * 78 * s, y + row * 74 * s
        if k < 4:
            Y.stroke(cr, [(gx + k * 14 * s, gy), (gx + k * 14 * s + 3 * s, gy + 52 * s)], 5.5 * s, Y.WHITE,
                     alpha=alpha)
        else:
            Y.stroke(cr, [(gx - 8 * s, gy + 44 * s), (gx + 58 * s, gy + 6 * s)], 5.5 * s, Y.WHITE, alpha=alpha)


def sun_moon(cr, t, u, cx, cy, rx, ry, alpha=1.0):
    """The sun by day and the crescent moon by night racing over an arc (u counts days: 0..1 one day, 1..2 a night,
    ...). Returns how dark it is (0..1)."""
    k = int(u)
    f = u - k
    x = cx - rx + 2 * rx * f
    y = cy - ry * math.sin(math.pi * f)
    if k % 2 == 0:
        Y.glow(cr, x, y, 160, 0.5 * alpha, (1.0, 0.80, 0.35))
        Y.dot(cr, x, y, 54, (1.0, 0.78, 0.20), 5.0)
        for i in range(12):
            a = 2 * math.pi * i / 12 + t
            Y.stroke(cr, [(x + 64 * math.cos(a), y + 64 * math.sin(a)), (x + 84 * math.cos(a), y + 84 * math.sin(a))],
                     6.0, (1.0, 0.78, 0.20), alpha=alpha)
        return 0.0
    Y.glow(cr, x, y, 160, 0.35 * alpha, (0.70, 0.80, 1.0))
    cr.push_group()
    Y.dot(cr, x, y, 50, (0.98, 0.95, 0.80), 5.0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.arc(x + 24, y - 14, 44, 0, 2 * math.pi)
    cr.fill()
    cr.restore()
    cr.save()                                                # the inner edge of the crescent, inked
    cr.arc(x, y, 50, 0, 2 * math.pi)
    cr.clip()
    cr.arc(x + 24, y - 14, 44, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    return math.sin(math.pi * f)


# ------------------------------------------------------------------ little signs


def heart(cr, x, y, s, alpha=1.0, col=(0.92, 0.12, 0.22)):
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    cr.move_to(0, 30)
    cr.curve_to(-60, -10, -36, -56, 0, -26)
    cr.curve_to(36, -56, 60, -10, 0, 30)
    cr.close_path()
    Y.ink_fill(cr, col, 5.0, alpha)
    Y.dot(cr, -18, -22, 6, (1.0, 0.70, 0.75))
    cr.restore()


def note(cr, x, y, s, alpha=1.0, col=Y.YEL):
    """A music note (two joined quavers)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    for dx in (0, 46):
        Y.oval(cr, dx, 0, 16, 12, col, 4.0, rot=-0.4)
        Y.stroke(cr, [(dx + 13, -4), (dx + 13, -70)], 9.0, INK)
        Y.stroke(cr, [(dx + 13, -4), (dx + 13, -70)], 4.0, col)
    Y.shape(cr, [(9, -76), (63, -86), (63, -70), (9, -60)], col, 4.0, smooth=False)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.restore()


def light_pillar(cr, t, x, y_top, y_bot, w, a=1.0):
    """A soft column of warm light from the sky down to the stage (no fire)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    g = cairo.LinearGradient(x - w, 0, x + w, 0)
    g.add_color_stop_rgba(0, *LIGHT, 0.0)
    g.add_color_stop_rgba(0.5, *LIGHT, 0.45 * a)
    g.add_color_stop_rgba(1, *LIGHT, 0.0)
    cr.set_source(g)
    cr.rectangle(x - w, y_top, 2 * w, y_bot - y_top)
    cr.fill()
    cr.restore()
    for k in range(10):
        u = (t * 0.35 + k / 10) % 1.0
        Y.sparkle(cr, x + w * 0.5 * math.sin(k * 2.3 + t), y_bot - (y_bot - y_top) * u, 14 * (1 - u) + 4,
                  a * (1 - u * 0.7))


@functools.lru_cache(maxsize=12)
def _light_figure(key, look_items, pose_items, s):
    """A figure turned into warm light (drawn once): its shape in tones of gold, a soft glow round it."""
    from puppet_core import surface_from_rgba
    from scipy.ndimage import gaussian_filter
    look, p = dict(look_items), dict(pose_items)
    gw, gh = int(900 * s), int(1500 * s)
    fx, fy = gw / 2, gh - 60 * s
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, gw, gh)
    c = cairo.Context(surf)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    Y.figure(c, look, fx, fy, s, 0.0, p)
    surf.flush()
    a = np.ndarray((gh, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :gw].astype(np.float32) / 255.0
    al = a[..., 3]
    rgb = a[..., 2::-1] / np.maximum(al[..., None], 1e-4)
    lum = 0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
    tone = 0.66 + 0.34 * np.clip(lum * 1.4, 0, 1)
    out = np.zeros((gh, gw, 4), np.float32)
    for i in range(3):
        out[..., i] = np.clip(LIGHT[i] * tone + 0.2 * (tone - 0.6), 0, 1) * al
    out[..., 3] = al
    k = 4
    small = np.clip(gaussian_filter(al[::k, ::k], 7.0) * 1.6, 0, 1)
    gl = np.zeros(small.shape + (4,), np.float32)
    for i in range(3):
        gl[..., i] = LIGHT[i] * small
    gl[..., 3] = small
    return surface_from_rgba(out), surface_from_rgba(gl), (fx, fy), k


def _freeze(d):
    return tuple(sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items()))


def light_figure(cr, key, look, p, x, feet, s, alpha, t=0.0, made_at=0.6):
    """Paint `look` in pose p as a figure of warm light standing at (x, feet), scale s."""
    if alpha <= 0.01:
        return
    fs, gs, (fx, fy), k = _light_figure(key, _freeze(look), _freeze(p), made_at)
    sc = s / made_at
    cr.save()
    cr.translate(x, feet)
    cr.scale(sc, sc)
    cr.translate(-fx, -fy)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.scale(k, k)
    cr.set_source_surface(gs, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(alpha * (0.85 + 0.15 * math.sin(t * 3.0)))
    cr.restore()
    cr.set_source_surface(fs, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(alpha * 0.9)
    cr.restore()


def medallion(cr, x, y, r, p=1.0, field=(0.99, 0.94, 0.80)):
    """A round gold-framed plate (for a close-up picture), popping in with p 0..1; returns the scale applied."""
    if p <= 0.01:
        return 0.0
    k = 0.5 + 0.5 * back(clamp(p), 2.0)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.new_path()
    cr.arc(8, 12, r, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    Y.dot(cr, 0, 0, r, Y.GOLD, 7.0)
    Y.dot(cr, 0, 0, r - 16, field, 5.0)
    for i in range(24):
        a = 2 * math.pi * i / 24
        Y.dot(cr, (r - 8) * math.cos(a), (r - 8) * math.sin(a), 3.0, Y.GOLD_HI)
    cr.restore()
    return k


def feet_closeup(cr, t, x, y, r, p=1.0, touch=1.0):
    """A round close-up plate: Rama's blue feet (red leg pads with gold bells) on the boards, and Shabari's two hands
    coming in from the left to touch them (touch 0..1), a few sparkles. Pops in with p 0..1."""
    if p <= 0.01:
        return
    k = medallion(cr, x, y, r, p, field=(0.36, 0.20, 0.09))
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.new_path()
    cr.arc(0, 0, r - 18, 0, 2 * math.pi)
    cr.clip()
    cr.rectangle(-r, -r, 2 * r, r * 0.95)                  # dark curtain above, boards below
    cr.set_source_rgb(0.20, 0.06, 0.08)
    cr.fill()
    for i in range(-3, 4):
        Y.stroke(cr, [(i * r * 0.32, r * 0.0), (i * r * 0.45, r)], 3.0, (0.18, 0.09, 0.03), alpha=0.8)
    u = r / 170.0
    for sd in (-1, 1):                                     # his two feet and shins
        fx = 50 * u + sd * 52 * u
        cr.save()
        cr.translate(fx, -30 * u)
        Y.shape(cr, [(-26 * u, -150 * u), (26 * u, -150 * u), (22 * u, 30 * u), (-22 * u, 30 * u)], Y.RED, 4.0,
                smooth=False)
        for row in range(4):
            for col in range(3):
                Y.dot(cr, (-14 + 14 * col) * u, (-125 + 38 * row) * u, 7 * u, Y.GOLD, 2.0)
        Y.stroke(cr, [(-24 * u, 26 * u), (24 * u, 26 * u)], 9 * u, Y.GOLD)
        foot = [(-20 * u, 30 * u), (20 * u, 30 * u), (24 * u, 54 * u), (sd * 60 * u, 74 * u), (sd * 62 * u, 90 * u),
                (-22 * u * sd, 92 * u), (-24 * u, 60 * u)]
        Y.shape(cr, foot, RAMA_BLUE, 4.0)
        cr.restore()
    q = ease(clamp(touch))
    for j, (hx, hy) in enumerate(((-150, 40), (-120, 90))):  # her hands, reaching in from the left
        ex, ey = mix(hx - 120, hx + 120, q) * u, hy * u
        Y.inked_line(cr, [(ex - 260 * u, ey + 40 * u), (ex, ey)], 40 * u, OLD_SKIN, 4.0)   # the forearm
        cr.save()                                          # the hand: palm and fingers resting on the foot
        cr.translate(ex, ey)
        cr.rotate(-0.25)
        Y.shape(cr, [(-14 * u, -18 * u), (34 * u, -14 * u), (60 * u, -4 * u), (62 * u, 8 * u), (30 * u, 16 * u),
                     (-14 * u, 18 * u)], OLD_SKIN, 3.5)
        for f in range(3):
            Y.stroke(cr, [(36 * u, (-8 + 7 * f) * u), (58 * u, (-4 + 5 * f) * u)], 2.0)
        Y.stroke(cr, [(-12 * u, -14 * u), (-12 * u, 14 * u)], 6 * u, BEAD)
        cr.restore()
    cr.restore()
    if touch > 0.6:
        for k2 in range(5):
            uu = (t * 0.9 + k2 / 5) % 1.0
            Y.sparkle(cr, x + (-60 + 40 * k2) * k, y + (20 - 120 * uu) * k, 14 * (1 - uu) * k, touch)
