"""Cast and props for the Kannada Yakshagana reel of videos/ashtavakra.py (scenes_ashtavakra_yk), built from
yaksha_kit (never edited here): the same flat painted actors with black outlines, now as

  MOTHER   the kit's WOMAN; the unborn child is a soft glowing child-shape curled inside a gold halo at her belly
           (drawn over her arms; her hands are painted again on its lower rim)
  FATHER   the kit's SAGE (saffron cloth, white beard): the big guru
  PANDIT   a different SAGE colouring: deep blue cloth with gold, a black beard, namam, a red and gold turban (proud)
  KING     the kit's KING (Janaka), on a gold throne
  BOY      Ashtavakra at twelve: a young brahmin boy (topknot, vibhuti, saffron dhoti, a staff) whose body is gently
           bent in eight places (head tilted, a rounded back, one shoulder up, a bent elbow, a turned wrist, a knee
           turned in, the other knee out, a turned foot); `crook` 0..1 straightens him (the river)
  STUDENT  the father's pupils (small boys in white, hands folded)
  GUARD    the palace door-keeper (an actor with a small crown and a spear)
  VARUNA   the water god (the kit's GOD in sea colours)

rig() is yaksha_kit.figure() with a few more joints (separate knee bends, a knee that turns in, both soles kept on the
floor, shoulder heights, a neck that leans, a turned foot) and its own parts list; it also returns the elbows, knees,
ankles, neck and back as named points (device coordinates). New faces are registered in yaksha_kit.FACES under
"ay_" names at import (the kit's head painter reads that table); nothing else in the kit is touched.
"""
import math

import cairo

import yaksha_kit as Y
from poster import H, W, back, clamp, ease
from puppet_core import spath

INK, GOLD, GOLD_HI, GOLD_DK, RED, CRIMSON, MAROON = Y.INK, Y.GOLD, Y.GOLD_HI, Y.GOLD_DK, Y.RED, Y.CRIMSON, Y.MAROON
WHITE, CREAM, YEL, SAFF, GREEN, BLUE, MIRROR = Y.WHITE, Y.CREAM, Y.YEL, Y.SAFF, Y.GREEN, Y.BLUE, Y.MIRROR
shape, stroke, dot, oval, glow, sparkle = Y.shape, Y.stroke, Y.dot, Y.oval, Y.glow, Y.sparkle

BOY_SKIN = (0.95, 0.72, 0.52)
HAIR = (0.10, 0.07, 0.08)
WATER = (0.16, 0.42, 0.78)
WATER_DK = (0.07, 0.20, 0.50)
WATER_HI = (0.70, 0.90, 1.0)
COOL = (0.45, 0.72, 1.0)

Y.FACES.setdefault("ay_boy", dict(base=BOY_SKIN, mark="vibhuti", rouge=True, big_eyes=True, lips=(0.82, 0.16, 0.16)))
Y.FACES.setdefault("ay_pandit", dict(Y.FACES["sage"], base=(0.95, 0.71, 0.50), beard=(0.16, 0.12, 0.13),
                                     brow=(0.16, 0.12, 0.13), mark="namam"))

MOTHER = dict(Y.WOMAN)
FATHER = dict(Y.SAGE)
PANDIT = dict(Y.SAGE, face="ay_pandit", crown="ay_turban", cloth=(0.12, 0.28, 0.66), cloth2=GOLD)
KING = dict(Y.KING)
BOY = dict(kind="sage", face="ay_boy", crown="ay_boy", head_s=1.36, skin=BOY_SKIN, hand=BOY_SKIN, cloth=SAFF,
           cloth2=WHITE)
STUDENT = dict(BOY, cloth=WHITE, cloth2=SAFF, head_s=1.32)
GUARD = dict(Y.HERO, crown="kireeta_small", disc=False, jacket=MAROON, sleeve=MAROON, kase=(RED, YEL, INK, GREEN),
             hem=YEL, hem_zig=RED, pads=MAROON)
VARUNA = dict(Y.GOD, jacket=(0.10, 0.48, 0.66), sleeve=(0.10, 0.48, 0.66), kase=(WHITE, WATER, INK, GREEN),
              hem=WATER, hem_zig=WHITE, sash=WHITE, disc_cols=(GOLD, WATER, (0.25, 0.75, 0.80)))

# ------------------------------------------------------------------ the rig (yaksha_kit.figure with more joints)

EXTRA = dict(bendL=None, bendR=None, thL=0.0, thR=0.0, plant=True, shL=0.0, shR=0.0, neck_x=0.0, fturnL=0.0,
             fturnR=0.0, hump=0.0, halo=None)


def _shin_to(th, h):
    """Shin and foot angles that put the sole at hip height h for thigh angle th (knee out if th > 0, in if < 0)."""
    v = clamp((h - Y.HIP[1] - Y.FOOT_H - Y.THIGH * math.cos(th)) / Y.SHIN, -1.0, 1.0)
    a = math.acos(v)
    sh = (a if th < 0 else -a) - th
    return sh, -(th + sh)


def rig(cr, look, x, feet, s=1.0, t=0.0, pose=None, flip=False, alpha=1.0, parts=None):
    """Draw an actor like yaksha_kit.figure (same parts, same pose keys) plus: bendL / bendR (each knee), thL / thR
    (extra thigh angle, negative turns that knee in), plant (both soles stay on the floor), shL / shR (shoulder
    heights), neck_x, fturnL / fturnR (a turned foot), hump (a rounded back, BOY), halo (the unborn child, MOTHER).
    Returns the kit's named points plus elbowL/R, kneeL/R, ankleL/R, neck, back (device coordinates)."""
    p = dict(Y.POSE)
    p.update(EXTRA)
    p.update(pose or {})
    bL = p["bend"] if p["bendL"] is None else p["bendL"]
    bR = p["bend"] if p["bendR"] is None else p["bendR"]
    thL, shL, ftL, hL = Y.leg_solve(bL, p["liftL"])
    thR, shR, ftR, hR = Y.leg_solve(bR, p["liftR"])
    thL += p["thL"]
    thR += p["thR"]
    hL = Y.HIP[1] + Y.THIGH * math.cos(thL) + Y.SHIN * math.cos(thL + shL) + Y.FOOT_H if p["thL"] else hL
    hR = Y.HIP[1] + Y.THIGH * math.cos(thR) + Y.SHIN * math.cos(thR + shR) + Y.FOOT_H if p["thR"] else hR
    hip_h = max(hL, hR)
    if p["plant"]:
        down = [h for h, lift in ((hL, p["liftL"]), (hR, p["liftR"])) if lift < 0.02]
        if down:
            hip_h = min(down)
            if p["liftL"] < 0.02:
                shL, ftL = _shin_to(thL, hip_h)
            if p["liftR"] < 0.02:
                shR, ftR = _shin_to(thR, hip_h)
    if alpha < 0.999:
        cr.push_group()
    cr.save()
    cr.translate(x + p["shift"] * s, feet - hip_h * s)
    sx = math.cos(math.pi * 2 * p["spin"]) if p["spin"] else 1.0
    if abs(sx) < 0.06:
        sx = 0.06 if sx >= 0 else -0.06
    cr.scale(s * sx * (-1 if flip else 1), s)
    ctx = Y.Ctx(cr, look, p, t)
    uL, lL, _ = p["armL"]
    uR, lR, _ = p["armR"]
    br = p["breathe"]
    spec = {
        "root": (None, (0, 0), 0.0, 1.0),
        "thighL": ("root", (-Y.HIP[0], Y.HIP[1]), thL, 1.0),
        "shinL": ("thighL", (0, Y.THIGH), shL, 1.0),
        "footL": ("shinL", (0, Y.SHIN), ftL - p["fturnL"], 1.0),
        "thighR": ("root", (Y.HIP[0], Y.HIP[1]), -thR, 1.0),
        "shinR": ("thighR", (0, Y.THIGH), -shR, 1.0),
        "footR": ("shinR", (0, Y.SHIN), -ftR + p["fturnR"], 1.0),
        "torso": ("root", (0, 0), p["lean"], 1.0),
        "uarmL": ("torso", (-Y.SHOULDER[0], Y.SHOULDER[1] - 3 * br + p["shL"]), uL, 1.0),
        "farmL": ("uarmL", (0, Y.UARM), -lL, 1.0),
        "uarmR": ("torso", (Y.SHOULDER[0], Y.SHOULDER[1] - 3 * br + p["shR"]), -uR, 1.0),
        "farmR": ("uarmR", (0, Y.UARM), lR, 1.0),
        "head": ("torso", (p["neck_x"], Y.NECK - 2 * br), p["head"], look.get("head_s", 1.0)),
    }
    mats = Y._solve(cr, spec)
    for part, fn in (parts if parts is not None else PARTS[look.get("crown")]):
        cr.set_matrix(mats[part])
        cr.save()
        fn(ctx)
        cr.restore()
    for name, part, pt in (("elbowL", "farmL", (0, 0)), ("elbowR", "farmR", (0, 0)), ("kneeL", "shinL", (0, 0)),
                           ("kneeR", "shinR", (0, 0)), ("ankleL", "footL", (0, 0)), ("ankleR", "footR", (0, 0)),
                           ("wristL", "farmL", (0, Y.FARM)), ("wristR", "farmR", (0, Y.FARM)),
                           ("neck", "head", (0, -10)), ("back", "torso", (70, -340)), ("belly", "torso", (0, -46))):
        cr.set_matrix(mats[part])
        ctx.mark(name, *pt)
    cr.set_matrix(mats["root"])
    ctx.mark("waist", 0, 0)
    cr.restore()
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    return ctx.pts


# ------------------------------------------------------------------ new parts


def _ears(cr, skin, ring=GOLD):
    for sd in (-1, 1):
        oval(cr, sd * 68, -6, 10, 20, skin, 3.0)
        dot(cr, sd * 70, 20, 6, ring, 2.2)


def boy_hair(ctx):
    """A young brahmin boy's hair: a black cap of hair and a small topknot tied with jasmine."""
    cr, look = ctx.cr, ctx.look
    cr.translate(0, Y.FACE_C)
    _ears(cr, look.get("skin", BOY_SKIN))
    oval(cr, 0, -128, 30, 26, HAIR, 4.5)                                # the topknot
    for k in range(5):
        a = math.pi * (1.05 + 0.9 * k / 4)
        dot(cr, 30 * math.cos(a), -122 + 22 * math.sin(a), 6.0, WHITE, 2.0)
    shape(cr, [(-70, -34), (-72, -70), (-56, -96), (-28, -110), (0, -113), (28, -110), (56, -96), (72, -70),
               (70, -34), (60, -52), (40, -72), (14, -80), (0, -76), (-20, -82), (-46, -70), (-62, -50)], HAIR, 4.5)
    stroke(cr, [(-40, -100), (-10, -106), (24, -104)], 3.0, (0.35, 0.30, 0.32))


def turban(ctx):
    """The proud pandit's red and gold turban (peta) with a jewel and a white plume."""
    cr, look = ctx.cr, ctx.look
    cr.translate(0, Y.FACE_C)
    _ears(cr, Y.FACES["ay_pandit"]["base"])
    stroke(cr, [(-64, -40), (-70, -72)], 10.0, HAIR)
    stroke(cr, [(64, -40), (70, -72)], 10.0, HAIR)
    shape(cr, [(30, -170), (52, -238), (70, -286), (60, -292), (38, -246), (18, -186)], WHITE, 4.0)   # the plume
    dome = [(-86, -56), (-102, -100), (-98, -150), (-70, -190), (-28, -206), (0, -208), (28, -206), (70, -190),
            (98, -150), (102, -100), (86, -56), (44, -72), (0, -78), (-44, -72)]
    shape(cr, dome, (0.80, 0.08, 0.10), 6.0)
    cr.save()
    cr.new_path()
    spath(cr, dome)
    cr.clip()
    for k in range(-4, 5):                                              # the wound folds, gold bands between
        x0 = k * 46
        stroke(cr, [(x0 - 70, -40), (x0 + 60, -220)], 12.0, GOLD)
        stroke(cr, [(x0 - 70, -40), (x0 + 60, -220)], 2.5)
    cr.restore()
    stroke(cr, [(-88, -66), (-44, -82), (0, -86), (44, -82), (88, -66)], 16.0, GOLD)
    stroke(cr, [(-88, -66), (-44, -82), (0, -86), (44, -82), (88, -66)], 2.5)
    Y.dot_row(cr, [(-84, -66), (0, -86), (84, -66)], 11, 3.0, RED)
    oval(cr, 0, -150, 22, 26, GOLD, 4.5)
    oval(cr, 0, -150, 12, 15, GREEN, 3.0)
    dot(cr, 4, -156, 3.5, WHITE)
    for k in range(3):
        dot(cr, 0, -112 + 12 * k, 4.0, GOLD_HI, 1.8)


def hump(ctx):
    """The boy's rounded back, a soft rise behind his right shoulder under his cloth (p['hump'] 0..1)."""
    k = ctx.p["hump"]
    if k <= 0.02:
        return
    cr, look = ctx.cr, ctx.look
    cr.save()
    cr.translate(66, -300)
    cr.scale(0.55 + 0.45 * k, 0.35 + 0.65 * k)
    pts = [(-64, 30), (-70, -30), (-48, -80), (-4, -100), (40, -88), (72, -48), (76, 30)]
    shape(cr, pts, look.get("cloth", SAFF), 6.0)
    stroke(cr, [(-40, -50), (-6, -74), (34, -66)], 3.5, INK, alpha=0.45)
    cr.restore()


def belly_halo(ctx):
    """The unborn child in a halo of light at the mother's belly (between the saree and her arms).
    p['halo'] = dict(a, wake, talk, point, side, red, pulse) (all optional)."""
    h = ctx.p.get("halo")
    if not h or h.get("a", 1.0) <= 0.01:
        return
    cr, p = ctx.cr, ctx.p
    hh = dict(h)
    hands = hh.pop("hands", True)
    baby_halo(cr, ctx.t, 0, HALO_Y, HALO_R, **hh)
    ctx.mark("halo", 0, HALO_Y)
    ctx.mark("halo_rim", 0, HALO_Y - HALO_R)
    if not hands:
        return
    col = ctx.look.get("hand", Y.SKIN)
    for sd, arm, hk in ((-1, p["armL"], p["handL"]), (1, p["armR"], p["handR"])):
        u, l_, w = arm                               # her hands again, on top of the halo's lower rim
        cr.save()
        cr.rotate(p["lean"])
        cr.translate(sd * Y.SHOULDER[0], Y.SHOULDER[1] - 3 * p["breathe"] + (p["shL"] if sd < 0 else p["shR"]))
        cr.rotate(u if sd < 0 else -u)
        cr.translate(0, Y.UARM)
        cr.rotate(-l_ if sd < 0 else l_)
        cr.translate(0, Y.FARM)
        cr.rotate(-w if sd < 0 else w)
        Y._hand(cr, hk, sd, col, ctx.t)
        stroke(cr, [(-19, -6), (19, -6)], 4.0, GOLD)
        cr.restore()


HALO_Y, HALO_R = -70.0, 128.0          # the halo on the mother's belly (root frame, design units)


def _parts(kind, crown_extra=None, insert=None):
    base = list(Y.KINDS[kind])
    if insert:                                          # after the arms (her hands rest under its rim)
        i = [k for k, (part, fn) in enumerate(base) if part == "farmR"][0] + 1
        base[i:i] = insert
    if crown_extra:
        base.append(("head", crown_extra))
    return base


_uL, _lL = Y._arm(-1)
_uR, _lR = Y._arm(1)
BOY_PARTS = [("shinL", Y._shin(-1)), ("shinR", Y._shin(1)), ("footL", Y._foot(-1)), ("footR", Y._foot(1)),
             ("torso", hump), ("root", Y.dhoti), ("torso", Y.sage_torso), ("uarmL", _uL), ("farmL", _lL),
             ("uarmR", _uR), ("farmR", _lR), ("head", Y.head), ("head", boy_hair), ("head", Y.crown_front)]
PARTS = {
    "woman": _parts("woman", insert=[("root", belly_halo)]),
    "jata": _parts("sage"),
    "ay_turban": _parts("sage", turban),
    "ay_boy": BOY_PARTS,
    "kireeta": _parts("actor"),
    "kireeta_small": _parts("actor"),
    "kedige": _parts("actor"),
}


# ------------------------------------------------------------------ poses

FOLD = dict(armL=(0.10, 2.10, 1.05), armR=(0.10, 2.10, 1.05), handL="open", handR="open")       # hands folded
CRADLE = dict(armL=(0.05, 0.20, 0.75), armR=(0.05, 0.20, 0.75), handL="open", handR="open")    # on the halo rim
# the boy's crooked body, kindly: head tilted, a rounded back, one shoulder up, a bent elbow and turned wrist, a knee
# turned in, the other knee out, a turned foot (crook 1); crook 0 = straight
CROOK = dict(lean=0.12, head=-0.30, neck_x=-16.0, shL=-22.0, shR=12.0, hump=1.0, bendL=0.30, bendR=0.55,
             thL=-0.55, fturnL=0.45, fturnR=-0.15, armL=(0.50, 1.95, 1.10), handL="open")
STRAIGHT = dict(lean=0.0, head=0.0, neck_x=0.0, shL=0.0, shR=0.0, hump=0.0, bendL=0.15, bendR=0.15, thL=0.0,
                fturnL=0.0, fturnR=0.0, armL=(0.16, 0.30, 0.0), handL="open")


def mix(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    if isinstance(a, str) or a is None:
        return a if u < 0.5 else b
    return a + (b - a) * u


def crook_pose(c, extra=None):
    """The boy's pose at crookedness c (1 bent, 0 straight), then `extra` on top."""
    p = {k: mix(STRAIGHT[k], CROOK[k], c) for k in CROOK}
    if extra:
        p.update(extra)
    return p


# ------------------------------------------------------------------ the unborn child in his halo


def baby_halo(cr, t, cx, cy, r, a=1.0, wake=0.0, talk=0.0, point=0.0, side=1, red=0.0, pulse=0.0, glow_a=1.0):
    """A gold halo with the unborn child curled inside, glowing softly. wake 0..1 opens his eyes, talk 0..1 opens his
    mouth, point 0..1 lifts his little arm to point toward `side` (+1 screen right), red 0..1 tints the light red
    for a moment (the curse reaching the rim, never inside)."""
    if a <= 0.01:
        return
    k = r / 100.0 * (1 + 0.04 * pulse)
    breath = 1 + 0.015 * math.sin(t * 2.4)
    warm = (1.0, 0.78, 0.40)
    hot = (1.0, 0.30, 0.20)
    gcol = mix(warm, hot, red)
    glow(cr, cx, cy, r * 2.6, (0.50 + 0.25 * pulse) * a * glow_a, gcol)
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    if a < 0.999:
        cr.push_group()
    g = cairo.RadialGradient(-10, -20, 4, 0, 0, 100)
    g.add_color_stop_rgb(0, 1.0, 0.98, 0.90)
    g.add_color_stop_rgb(0.65, *mix((1.0, 0.86, 0.64), (1.0, 0.62, 0.55), red))
    g.add_color_stop_rgb(1, *mix((0.98, 0.64, 0.42), (0.95, 0.30, 0.25), red))
    cr.new_path()
    cr.arc(0, 0, 100, 0, 2 * math.pi)
    cr.set_source(g)
    cr.fill()
    # the child, curled: head up-left, back round, knees drawn up, a little hand by the face
    sk = (1.0, 0.80, 0.60)
    ln = (0.62, 0.30, 0.14)
    cr.save()
    cr.scale(-side, 1)
    cr.rotate(0.06 * math.sin(t * 1.3))
    cr.scale(breath, breath)
    body = [(-6, -30), (26, -40), (54, -22), (66, 12), (56, 46), (24, 62), (-14, 58), (-30, 34), (-26, 2)]
    cr.new_path()
    spath(cr, body)
    cr.set_source_rgb(*sk)
    cr.fill_preserve()
    cr.set_source_rgb(*ln)
    cr.set_line_width(3.5)
    cr.stroke()
    # legs folded up (thigh and foot)
    for pts in ([(4, 52), (34, 30), (44, 4)], [(44, 4), (30, -6), (16, -6)]):
        stroke(cr, pts, 18.0, ln)
        stroke(cr, pts, 12.5, sk)
    dot(cr, 14, -6, 9.5, sk, 3.0)
    # the head
    hx0, hy0 = -22, -50
    dot(cr, hx0, hy0, 36, sk, 3.5)
    stroke(cr, [(hx0 - 22, hy0 - 26), (hx0 - 4, hy0 - 36), (hx0 + 14, hy0 - 32)], 3.0, ln, alpha=0.7)   # a curl
    oval(cr, hx0 + 26, hy0 + 6, 6, 9, sk, 3.0)                     # an ear
    w = clamp(wake)
    for ex_ in (hx0 - 18, hx0 + 6):
        if w < 0.5:
            stroke(cr, [(ex_ - 7, hy0 - 2), (ex_, hy0 + 3), (ex_ + 7, hy0 - 2)], 3.2, ln)
        else:
            oval(cr, ex_ + 1, hy0, 5.2, 6.8, INK, 0)
            dot(cr, ex_ + 2.6, hy0 - 2.4, 2.0, WHITE)
    oval(cr, hx0 - 22, hy0 + 14, 7, 4.5, (1.0, 0.55, 0.45), 0)
    oval(cr, hx0 + 10, hy0 + 14, 7, 4.5, (1.0, 0.55, 0.45), 0)
    tk = clamp(talk)
    if tk > 0.2:
        oval(cr, hx0 - 6, hy0 + 18, 5 + 2 * tk, 4 + 5 * tk, (0.55, 0.12, 0.12), 2.2)
    else:
        stroke(cr, [(hx0 - 12, hy0 + 15), (hx0 - 6, hy0 + 19), (hx0, hy0 + 15)], 2.8, ln)
    # the arm, over the chest: resting by the chin, or reaching out to point (toward the way he faces)
    u = ease(clamp(point))
    wig = 3 * math.sin(t * 5) * u
    sx, sy = -2, 4
    ex, ey = mix((-8, -2), (-36, 2), u)
    hx, hy = mix((-22, -12), (-64, -8 + wig), u)
    stroke(cr, [(sx, sy), (ex, ey), (hx, hy)], 15.0, ln, smooth=False)
    stroke(cr, [(sx, sy), (ex, ey), (hx, hy)], 10.0, sk, smooth=False)
    dot(cr, hx, hy, 8.5, sk, 3.0)
    if u > 0.3:                                       # the little pointing finger
        stroke(cr, [(hx - 4, hy - 1), (hx - 17, hy - 4)], 6.5, ln)
        stroke(cr, [(hx - 4, hy - 1), (hx - 16, hy - 4)], 3.5, sk)
    cr.restore()
    # the rim: a gold ring with mirror dots (like the crowns), and soft rays
    cr.new_path()
    cr.arc(0, 0, 100, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(9)
    cr.stroke()
    cr.arc(0, 0, 100, 0, 2 * math.pi)
    cr.set_source_rgb(*mix(GOLD, (1.0, 0.35, 0.25), red))
    cr.set_line_width(5)
    cr.stroke()
    for i in range(24):
        aa = 2 * math.pi * i / 24 + t * 0.15
        dot(cr, 100 * math.cos(aa), 100 * math.sin(aa), 2.6, GOLD_HI)
    if a < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    cr.restore()
    for i in range(6):                                   # specks of light drifting round it
        aa = t * 0.7 + i * 1.047
        sparkle(cr, cx + 1.25 * r * math.cos(aa), cy + 1.1 * r * math.sin(aa), 9 + 4 * math.sin(t * 3 + i),
                0.7 * a)


def sound_rings(cr, t, x, y, t0, r0=60, n=3, period=0.35, rmax=220, a=1.0, col=(1.0, 0.90, 0.60)):
    """Rings of sound spreading from (x, y) after t0 (a voice)."""
    for i in range(n):
        u = (t - t0 - i * period) / 1.0
        if 0 < u < 1:
            rr = r0 + rmax * ease(u)
            cr.save()
            cr.set_operator(cairo.OPERATOR_ADD)
            cr.new_path()
            cr.arc(x, y, rr, 0, 2 * math.pi)
            cr.set_source_rgba(*col, 0.75 * (1 - u) * a)
            cr.set_line_width(9 * (1 - u) + 2)
            cr.stroke()
            cr.restore()


# ------------------------------------------------------------------ props

WOOD = (0.48, 0.26, 0.10)
LEAFC = (0.93, 0.82, 0.55)


def _rrect(cr, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    cr.new_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def palm_book(cr, t, x, y, s=1.0, rot=0.0, cross=0.0, glow_a=0.0, title=None, alpha=1.0, lines=3):
    """A palm-leaf book (ole gari): long dried leaves with rows of writing between two wooden covers, a red string
    through the holes. title: a closed book with the title painted on its cover. cross 0..1: a red X over the writing
    (read wrong)."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    if glow_a > 0.01:
        glow(cr, 0, 0, 260, glow_a, (1.0, 0.82, 0.45))
    if alpha < 0.999:
        cr.push_group()
    L = 300
    _rrect(cr, -L / 2 - 10, 18, L + 20, 22, 8)
    Y.ink_fill(cr, WOOD, 5.0)
    for i in range(2):
        _rrect(cr, -L / 2, 8 - 10 * i, L, 12, 5)
        Y.ink_fill(cr, mix(LEAFC, (0.80, 0.66, 0.38), 0.3 * i), 3.0)
    if title:
        _rrect(cr, -L / 2 - 10, -56, L + 20, 52, 10)
        Y.ink_fill(cr, (0.60, 0.10, 0.08), 5.0)
        stroke(cr, [(-L / 2 + 2, -50), (L / 2 - 2, -50)], 3.0, GOLD)
        stroke(cr, [(-L / 2 + 2, -10), (L / 2 - 2, -10)], 3.0, GOLD)
        Y.kn_text(cr, title, 0, -31, 40, YEL, INK, 4, anchor="cm", max_w=L - 40)
    else:
        _rrect(cr, -L / 2, -58, L, 62, 10)
        Y.ink_fill(cr, LEAFC, 4.5)
        for r_ in range(lines):
            yy = -44 + r_ * 16
            xx = -L / 2 + 34
            k = 0
            while xx < L / 2 - 30:
                w = 18 + 14 * ((k * 7 + r_ * 3) % 4)
                stroke(cr, [(xx, yy), (min(xx + w, L / 2 - 30), yy)], 4.0, (0.30, 0.18, 0.10))
                xx += w + 10
                k += 1
    for sd in (-1, 1):                                  # the string through the holes
        dot(cr, sd * L * 0.30, -26 if not title else -30, 5.5, INK)
    stroke(cr, [(-L * 0.30, 30), (-L * 0.30 - 8, 58), (-L * 0.30 + 4, 78)], 4.0, RED)
    dot(cr, -L * 0.30 + 4, 82, 6, RED, 2.0)
    if cross > 0.01:
        c = ease(clamp(cross))
        for (ax, ay, bx, by) in ((-80, -70, 80, 20), (80, -70, -80, 20)):
            ex, ey = ax + (bx - ax) * c, ay + (by - ay) * c
            stroke(cr, [(ax, ay), (ex, ey)], 22.0, INK)
            stroke(cr, [(ax, ay), (ex, ey)], 13.0, RED)
    if alpha < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    cr.restore()


def water_cloth(cr, t, y_top, x0=-30, x1=W + 30, a=1.0, bottom=H + 60, speed=1.0, rows=3):
    """The water, Yakshagana-style: a blue cloth painted with white wave curls, held up across the stage."""
    if a <= 0.01:
        return
    if a < 0.999:
        cr.push_group()
    top = [(x, y_top + 16 * math.sin(x / 75.0 + t * 2.0 * speed) + 6 * math.sin(x / 31.0 - t * 3.1 * speed))
           for x in range(int(x0), int(x1) + 20, 20)]

    def outline():
        cr.new_path()
        cr.move_to(*top[0])
        for p_ in top[1:]:
            cr.line_to(*p_)
        cr.line_to(x1, bottom)
        cr.line_to(x0, bottom)
        cr.close_path()
    outline()
    g = cairo.LinearGradient(0, y_top, 0, y_top + 420)
    g.add_color_stop_rgb(0, *WATER)
    g.add_color_stop_rgb(1, *WATER_DK)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(7)
    cr.stroke()
    cr.save()
    outline()
    cr.clip()
    stroke(cr, [(x, y + 16) for x, y in top], 6.0, WATER_HI, smooth=False, alpha=0.8)
    for r_ in range(rows):
        yy = y_top + 70 + 78 * r_
        off = (t * 40 * speed * (1 if r_ % 2 else -1) + 60 * r_) % 160
        for k in range(-1, int((x1 - x0) / 160) + 2):
            cx = x0 + k * 160 + off
            cr.new_path()
            cr.arc(cx, yy, 30, math.pi, 2 * math.pi)
            cr.arc_negative(cx + 18, yy, 12, 0, math.pi)
            cr.set_source_rgba(*WHITE, 0.85)
            cr.set_line_width(5)
            cr.stroke()
            dot(cr, cx + 52, yy - 14, 4, WATER_HI)
    cr.restore()
    if a < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)


def bubbles(cr, t, x, y, w, n=8, a=1.0, speed=0.5, seed=0, rise=300):
    """Little rings of air rising through the water from about (x, y)."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * speed + i / n + seed * 0.17) % 1.0
        px = x + w * math.sin(i * 2.3 + seed) * 0.5 + 10 * math.sin(t * 2 + i)
        py = y - rise * u
        r = 6 + 6 * math.sin(i * 1.7) ** 2
        cr.new_path()
        cr.arc(px, py, r, 0, 2 * math.pi)
        cr.set_source_rgba(*WATER_HI, 0.9 * a * (1 - u))
        cr.set_line_width(3)
        cr.stroke()


def throne(cr, x, floor, s=1.0):
    """King Janaka's gold throne: a tall arched back with a red panel, gold knobs, on a dais."""
    cr.save()
    cr.translate(x, floor)
    cr.scale(s, s)
    shape(cr, [(-330, 0), (-300, -60), (300, -60), (330, 0)], (0.55, 0.30, 0.12), 6.0, smooth=False)   # the dais
    stroke(cr, [(-300, -30), (300, -30)], 6.0, GOLD)
    back_ = [(-200, -330), (-210, -620), (-170, -800), (-90, -900), (0, -930), (90, -900), (170, -800),
             (210, -620), (200, -330)]
    shape(cr, back_, GOLD, 7.0)
    shape(cr, Y._scale_pts(back_, 0.80, (0, -560)), (0.70, 0.06, 0.08), 5.0)
    Y.dot_row(cr, Y._scale_pts(back_, 0.90, (0, -560)), 22, 4.0, MIRROR)
    for sd in (-1, 1):
        shape(cr, [(sd * 200, -60), (sd * 230, -330), (sd * 250, -340), (sd * 250, -60)], GOLD_DK, 5.0, smooth=False)
        dot(cr, sd * 240, -362, 30, GOLD, 5.0)
        dot(cr, sd * 240, -362, 12, RED, 3.0)
    dot(cr, 0, -930, 24, GOLD, 5.0)
    dot(cr, 0, -930, 9, RED, 2.0)
    cr.restore()


def gate(cr, t, x, floor, s=1.0, open_=0.0, inside=None):
    """The palace door: two striped pillars, a gold arch with a mango-leaf thorana, carved wooden doors (open_ 0..1
    swings them open); inside(cr) draws what is seen through the doorway."""
    cr.save()
    cr.translate(x, floor)
    cr.scale(s, s)
    w, h = 400, 820
    cr.rectangle(-w / 2, -h, w, h)                       # the hall inside
    g = cairo.LinearGradient(0, -h, 0, 0)
    g.add_color_stop_rgb(0, 0.30, 0.10, 0.06)
    g.add_color_stop_rgb(1, 0.55, 0.28, 0.10)
    cr.set_source(g)
    cr.fill()
    glow(cr, 0, -h * 0.5, 300, 0.35 * open_, (1.0, 0.75, 0.40))
    if inside:
        cr.save()
        cr.rectangle(-w / 2, -h, w, h)
        cr.clip()
        inside(cr)
        cr.restore()
    for sd in (-1, 1):                                   # the doors
        cr.save()
        cr.translate(sd * w / 2, 0)
        cr.scale(1 - 0.85 * ease(open_), 1)
        pts = [(0, 0), (-sd * w / 2, 0), (-sd * w / 2, -h + 40), (0, -h + 40)]
        shape(cr, pts, WOOD, 6.0, smooth=False)
        for r_ in range(4):
            yy = -h + 120 + r_ * 180
            shape(cr, [(-sd * 30, yy), (-sd * (w / 2 - 30), yy), (-sd * (w / 2 - 30), yy + 140), (-sd * 30, yy + 140)],
                  (0.58, 0.32, 0.12), 4.0, smooth=False)
            for c_ in range(3):
                dot(cr, -sd * (60 + 50 * c_), yy + 70, 7, GOLD, 2.5)
        cr.restore()
    for sd in (-1, 1):                                   # pillars
        cr.save()
        cr.rectangle(sd * (w / 2 + 40) - 40, -h - 40, 80, h + 40)
        Y.fill_pattern(cr, Y.stripe_pattern(RED, GOLD, 14.0), 6)
        cr.restore()
        shape(cr, [(sd * (w / 2 + 40) - 56, 0), (sd * (w / 2 + 40) + 56, 0), (sd * (w / 2 + 40) + 48, -40),
                   (sd * (w / 2 + 40) - 48, -40)], GOLD, 5.0, smooth=False)
    arch = [(-w / 2 - 100, -h - 40), (-w / 2 - 60, -h - 160), (-140, -h - 250), (0, -h - 290), (140, -h - 250),
            (w / 2 + 60, -h - 160), (w / 2 + 100, -h - 40)]
    shape(cr, arch + [(w / 2 + 100, -h + 10), (-w / 2 - 100, -h + 10)], GOLD, 7.0)
    shape(cr, [(-w / 2, -h + 2), (-w / 2 + 10, -h - 120), (-120, -h - 190), (0, -h - 220), (120, -h - 190),
               (w / 2 - 10, -h - 120), (w / 2, -h + 2)], (0.70, 0.06, 0.08), 5.0)
    Y.dot_row(cr, arch, 26, 4.0, MIRROR)
    dot(cr, 0, -h - 300, 22, RED, 5.0)
    for i in range(9):                                   # thorana leaves
        xx = -w / 2 + w * (i + 0.5) / 9
        sw = 0.08 * math.sin(t * 1.6 + i)
        cr.save()
        cr.translate(xx, -h + 12)
        cr.rotate(sw)
        shape(cr, [(0, 0), (-12, 20), (-10, 52), (0, 74), (10, 52), (12, 20)], Y.LEAF if i % 2 else Y.DLEAF, 3.5)
        cr.restore()
    cr.restore()


def spear(cr, x0, y0, x1, y1, w=1.0):
    """A door-keeper's spear from (x0, y0) (butt) to (x1, y1) (tip)."""
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.atan2(y1 - y0, x1 - x0)
    cr.save()
    cr.translate(x0, y0)
    cr.rotate(a)
    cr.scale(w, w)
    L /= w
    shape(cr, [(0, -7), (L - 70, -7), (L - 70, 7), (0, 7)], (0.50, 0.30, 0.12), 4.5, smooth=False)
    for k in range(4):
        stroke(cr, [(L * (0.2 + 0.18 * k), -7), (L * (0.2 + 0.18 * k), 7)], 6.0, GOLD, cap=cairo.LINE_CAP_BUTT)
    shape(cr, [(L - 74, 0), (L - 50, -24), (L, 0), (L - 50, 24)], (0.86, 0.88, 0.92), 4.5, smooth=False)
    for sd in (-1, 1):
        stroke(cr, [(L - 78, 0), (L - 98, sd * 18), (L - 112, sd * 30)], 6.0, RED)
    cr.restore()


def moon(cr, x, y, r, a=1.0):
    if a <= 0.01:
        return
    glow(cr, x, y, r * 4, 0.35 * a, (0.85, 0.90, 1.0))
    cr.save()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.98, 0.96, 0.86, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(5)
    cr.stroke()
    for dx, dy, rr in ((-0.3, -0.2, 0.18), (0.25, 0.1, 0.14), (-0.05, 0.35, 0.1)):
        cr.new_path()
        cr.arc(x + dx * r, y + dy * r, rr * r, 0, 2 * math.pi)
        cr.set_source_rgba(0.82, 0.80, 0.70, a)
        cr.fill()
    cr.restore()


def medal(cr, x, y, r, text, a=1.0, col=GOLD, txt=RED, pop=1.0, size=None):
    """A gold disc with a scalloped rim and a number or word on it (counters, the eight bends)."""
    if a <= 0.01 or pop <= 0.01:
        return
    k = back(clamp(pop), 2.2)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    if a < 0.999:
        cr.push_group()
    n = 18
    for i in range(n):
        aa = 2 * math.pi * i / n
        dot(cr, r * 0.92 * math.cos(aa), r * 0.92 * math.sin(aa), r * 0.2, col, max(2.0, r * 0.05))
    dot(cr, 0, 0, r * 0.92, col, max(3.0, r * 0.07))
    dot(cr, 0, 0, r * 0.74, (1.0, 0.95, 0.80), max(2.0, r * 0.04))
    if text:
        Y.kn_text(cr, text, 0, 0, size or r * 1.0, txt, INK, max(2, r * 0.07), anchor="cm", max_w=r * 1.25)
    if a < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    cr.restore()


def board(cr, x, y, w, h, a=1.0, field=CRIMSON, rot=0.0, pop=1.0):
    """A painted board (like a small thera) for cards: gold frame with red teeth, a coloured field."""
    if a <= 0.01 or pop <= 0.01:
        return
    k = 0.6 + 0.4 * back(clamp(pop), 1.8)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    if a < 0.999:
        cr.push_group()
    cr.rectangle(-w / 2 + 12, -h / 2 + 16, w, h)
    cr.set_source_rgba(0, 0, 0, 0.45)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    Y.ink_fill(cr, GOLD, 7.0)
    for (ax, ay, bx, by) in ((-w / 2 + 4, -h / 2 + 8, w / 2 - 4, -h / 2 + 8),
                             (w / 2 - 4, h / 2 - 8, -w / 2 + 4, h / 2 - 8)):
        Y._border_teeth(cr, ax, ay, bx, by, max(6, int(w / 34)), RED, 1)
    cr.rectangle(-w / 2 + 16, -h / 2 + 30, w - 32, h - 60)
    Y.ink_fill(cr, field, 5.0)
    for yy in (-h / 2 + 42, h / 2 - 42):
        for x_, y_ in Y.along([(-w / 2 + 30, yy), (w / 2 - 30, yy)], int(w / 26)):
            dot(cr, x_, y_, 2.6, GOLD_HI)
    if a < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    cr.restore()


def tick(cr, x, y, r, p=1.0, col=(0.10, 0.65, 0.25)):
    """A green tick drawn on as p goes 0..1."""
    if p <= 0.01:
        return
    P = [(x - r * 0.75, y), (x - r * 0.2, y + r * 0.55), (x + r * 0.85, y - r * 0.65)]
    u = ease(clamp(p))
    if u < 0.5:
        q = u / 0.5
        pts = [P[0], (P[0][0] + (P[1][0] - P[0][0]) * q, P[0][1] + (P[1][1] - P[0][1]) * q)]
    else:
        q = (u - 0.5) / 0.5
        pts = [P[0], P[1], (P[1][0] + (P[2][0] - P[1][0]) * q, P[1][1] + (P[2][1] - P[1][1]) * q)]
    stroke(cr, pts, r * 0.42, INK, smooth=False)
    stroke(cr, pts, r * 0.26, col, smooth=False)


def cross(cr, x, y, r, p=1.0, col=RED):
    """A red cross drawn on as p goes 0..1."""
    if p <= 0.01:
        return
    u = ease(clamp(p))
    for k, (ax, ay, bx, by) in enumerate(((-1, -1, 1, 1), (1, -1, -1, 1))):
        q = clamp(u * 2 - k)
        if q <= 0:
            continue
        p0 = (x + ax * r * 0.7, y + ay * r * 0.7)
        p1 = (p0[0] + (bx - ax) * r * 0.7 * q, p0[1] + (by - ay) * r * 0.7 * q)
        stroke(cr, [p0, p1], r * 0.40, INK, smooth=False)
        stroke(cr, [p0, p1], r * 0.25, col, smooth=False)


def cloud_path(cr, x, y, rx, ry, n=14):
    pts = []
    for i in range(n):
        aa = 2 * math.pi * i / n
        rr = 1.0 if i % 2 == 0 else 0.88
        pts.append((x + rx * rr * math.cos(aa), y + ry * rr * math.sin(aa)))
    cr.new_path()
    spath(cr, pts)


def thought(cr, x, y, rx, ry, a, src):
    """A thought cloud centred at (x, y) with little puffs back toward src (the thinker's head)."""
    if a <= 0.01:
        return
    for k in range(3):
        u = (k + 1) / 4.0
        px, py = src[0] + (x - src[0]) * u * 0.8, src[1] + (y + ry * 0.7 - src[1]) * u * 0.8
        cr.new_path()
        cr.arc(px, py, 10 + 8 * k, 0, 2 * math.pi)
        cr.set_source_rgba(*CREAM, a)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(5)
        cr.stroke()
    cloud_path(cr, x, y, rx, ry)
    cr.set_source_rgba(*CREAM, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(7)
    cr.stroke()


def pot_pour(cr, t, x, y, s=1.0, tilt=0.0, flow=0.0, fall=300.0):
    """A sage's water pot held at (x, y), tipped by `tilt` (radians), pouring a stream of drops (flow 0..1)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(tilt)
    shape(cr, [(-34, -20), (34, -20), (50, 20), (40, 62), (0, 74), (-40, 62), (-50, 20)], (0.62, 0.36, 0.14), 5.0)
    stroke(cr, [(-46, 18), (46, 18)], 5.0, GOLD)
    stroke(cr, [(40, 10), (78, -12), (88, -24)], 9.0, INK)
    stroke(cr, [(40, 10), (78, -12), (88, -24)], 5.0, (0.62, 0.36, 0.14))
    m = cr.get_matrix()
    cr.restore()
    if flow > 0.01:
        sx, sy = cr.device_to_user(*m.transform_point(88, -24))
        for i in range(12):
            u = (t * 1.6 + i / 12) % 1.0
            px = sx - 30 * u + 4 * math.sin(i)
            py = sy + fall * u
            dot(cr, px, py, (8 - 3 * u) * s, WATER_HI, 2.0)


def newborn(cr, t, x, y, s=1.0, a=1.0):
    """The newborn in his mother's arms: wrapped in a saffron cloth, his face peeping out, one little arm (bent)
    waving."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(-0.15)
    if a < 0.999:
        cr.push_group()
    glow(cr, 0, 0, 260, 0.45, (1.0, 0.82, 0.50))
    shape(cr, [(-150, -10), (-120, -60), (-40, -78), (60, -70), (140, -30), (150, 30), (110, 64), (0, 80),
               (-110, 60), (-160, 30)], SAFF, 6.0)
    for k in range(3):
        stroke(cr, [(-60 + 50 * k, -66), (-40 + 50 * k, 70)], 3.0, INK, alpha=0.4)
    stroke(cr, [(-140, 20), (0, 50), (140, 10)], 8.0, WHITE)
    sk = (1.0, 0.80, 0.62)
    sw = 0.25 * math.sin(t * 3.0)
    cr.save()                                            # the little bent arm
    cr.translate(30, -50)
    cr.rotate(-0.9 + sw)
    stroke(cr, [(0, 0), (0, -44), (26, -64)], 22.0, INK, smooth=False)
    stroke(cr, [(0, 0), (0, -44), (26, -64)], 15.0, sk, smooth=False)
    dot(cr, 28, -68, 12, sk, 3.5)
    cr.restore()
    dot(cr, -95, -30, 54, sk, 4.5)                        # the head
    stroke(cr, [(-130, -66), (-110, -82), (-88, -84)], 4.0, (0.60, 0.30, 0.14))
    for ex in (-116, -84):
        stroke(cr, [(ex - 9, -36), (ex, -42), (ex + 9, -36)], 4.0, INK)
    oval(cr, -124, -18, 9, 6, (1.0, 0.55, 0.45), 0)
    oval(cr, -66, -18, 9, 6, (1.0, 0.55, 0.45), 0)
    stroke(cr, [(-108, -14), (-98, -8), (-88, -14)], 4.0, (0.60, 0.15, 0.12))
    dot(cr, -97, -64, 4, RED)
    if a < 0.999:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    cr.restore()
