"""Vex, the baby vampire, drawn entirely in code so every part can move (owner, 3 Nov 2026: "Create 2.5d or 2d
mascot yourself which you can animate yourself"). Same design as the owner's ChatGPT drawing: lavender skin, slicked
black hair with one curl, pointy ears, big red eyes, two fangs, black cape with red lining and a tall collar, red bat
bow tie with a gold brooch, white jabot, black jacket with gold buttons and a red zigzag hem, black boots.

Flat colours with one cel-shadow tone per shape and a thin rim light (the "2.5D" look), thick dark outlines.

  vex(cr, t, x, y, s=0.33, **pose)   feet at (x, y); about 1000 units tall at s=1
  pose keys: turn (-1..1, head/body turn), lean (rad), squash, tilt (head, rad), look (dx, dy),
             eyes: open | happy | closed | angry | sad | shocked | dizzy | cry | sparkle
             brows: None | angry | sad | up | flat
             mouth: smirk | closed | open | wide | grin | frown | o | wobble  (or talk=0..1 to blend lip sync)
             arms: (left, right) names from HANDS or (x, y) hand targets; hold=(fn_l, fn_r) props in the fists
             legs: stand | walk | sit | jump ; walk=phase ; cape: flare 0..1 ; blink 0..1 ; blush ; tears
             shadow (floor shadow on/off)
"""
import math

import cairo

from .polish import ellipse, rad, smooth

INK = (0.11, 0.06, 0.1, 1)
SKIN, SKIN_SH, SKIN_HI = (0.89, 0.8, 0.97, 1), (0.78, 0.68, 0.9, 1), (0.95, 0.9, 1.0, 1)
EAR_IN = (0.72, 0.6, 0.86, 1)
HAIR, HAIR_SH, HAIR_HI = (0.18, 0.15, 0.22, 1), (0.11, 0.09, 0.14, 1), (0.36, 0.32, 0.44, 1)
CLOTH, CLOTH_SH = (0.17, 0.15, 0.19, 1), (0.1, 0.09, 0.12, 1)
RED, RED_SH = (0.93, 0.16, 0.18, 1), (0.74, 0.08, 0.12, 1)
WHITE, WHITE_SH = (1, 1, 1, 1), (0.86, 0.85, 0.9, 1)
GOLD, GOLD_SH = (0.98, 0.76, 0.2, 1), (0.85, 0.58, 0.1, 1)
EYE_RED, EYE_DARK, EYE_LIGHT = (0.78, 0.06, 0.12, 1), (0.38, 0.02, 0.06, 1), (1.0, 0.36, 0.38, 1)
MOUTH_IN, TONGUE = (0.42, 0.06, 0.12, 1), (0.98, 0.5, 0.58, 1)
BLUSH = (1.0, 0.45, 0.55, 0.85)
TEAR = (0.55, 0.85, 1.0, 0.9)
LW = 10
SHADE = (13, 11)                  # cel-shadow offset: light from the top left

HEAD = (0, -640)                  # head centre (face ellipse 275 x 250)
SHOULDER = {-1: (-112, -362), 1: (112, -362)}
HANDS = {   # named hand targets for the right arm (side=+1); mirrored for the left
    "rest": (92, -292), "up": (170, -570), "point": (330, -350), "out": (270, -250), "hips": (150, -228),
    "chin": (50, -455), "front": (70, -262), "cheek": (165, -540), "eyes": (100, -610), "wave": (230, -560),
    "down": (150, -200), "reach": (300, -420),
}
OVER_HEAD = ("chin", "cheek", "eyes")           # these hands are drawn over the head


def _path_fill(cr, path, base, shade=None, ink=INK, lw=LW, rim=None):
    """Fill a path with a cel shadow crescent (bottom right) and an optional rim light, then outline it."""
    path(cr)
    cr.set_source_rgba(*base)
    cr.fill()
    if shade:
        cr.save()
        path(cr)
        cr.clip()
        path(cr)
        cr.set_source_rgba(*shade)
        cr.fill()
        cr.translate(-SHADE[0], -SHADE[1])
        path(cr)
        cr.set_source_rgba(*base)
        cr.fill()
        if rim:
            cr.translate(SHADE[0] * 2.2, SHADE[1] * 2.2)
            path(cr)
            cr.set_source_rgba(*rim)
            cr.set_line_width(5)
            cr.stroke()
        cr.restore()
    if ink:
        path(cr)
        cr.set_source_rgba(*ink)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()


def _ell(cx, cy, rx, ry, rot=0.0):
    return lambda c: ellipse(c, cx, cy, rx, ry, rot)


def _poly(pts, curve=True):
    def p(c):
        if curve:
            smooth(c, pts)
        else:
            c.move_to(*pts[0])
            for q in pts[1:]:
                c.line_to(*q)
            c.close_path()
    return p


def _line(cr, pts, w, col=INK, curve=True):
    cr.move_to(*pts[0])
    if curve and len(pts) == 3:
        cr.curve_to(pts[1][0], pts[1][1], pts[1][0], pts[1][1], *pts[2])
    else:
        for q in pts[1:]:
            cr.line_to(*q)
    cr.set_source_rgba(*col)
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


# ---------------------------------------------------------------- cape and collar (behind everything)
def _cape(cr, t, turn, flare, sway):
    k = 1 + 0.45 * flare
    def X(x):                                    # turning: the near side gets narrower
        return x * k * (1 - 0.18 * turn * (1 if x > 0 else -1))
    hem = -36
    pts = [(X(-108), -400), (X(-200), -260), (X(-300), -120)]
    for j in range(4):                           # bat-scalloped hem, swaying
        x0 = -330 + j * 165
        pts += [(X(x0) + sway * (1 if j < 2 else -1), hem + (0 if j % 2 == 0 else 26)),
                (X(x0 + 82) + sway * 0.6, hem - 40)]
    pts += [(X(330) - sway, hem), (X(300), -120), (X(200), -260), (X(108), -400)]
    outer = _poly(pts, curve=False)
    _path_fill(cr, outer, RED, RED_SH)
    for side in (-1, 1):                         # black outer folds of the cape
        sx = side
        fold = [(X(sx * 108), -400), (X(sx * 196), -262), (X(sx * 298), -122), (X(sx * 330) - sway * sx, hem),
                (X(sx * 248) - sway * sx * 0.6, hem - 40), (X(sx * 215), -120), (X(sx * 150), -270)]
        _path_fill(cr, _poly(fold, curve=False), CLOTH, CLOTH_SH)


def _collar(cr, turn, flare):
    for side in (-1, 1):
        k = 1 + 0.25 * flare
        tip = (side * 365 * k + turn * 30, -585)
        pts = [(side * 120 + turn * 20, -470), tip, (side * 270 * k + turn * 25, -420), (side * 160 + turn * 20, -392)]
        _path_fill(cr, _poly(pts, curve=False), RED, RED_SH)
        back = [(side * 120 + turn * 20, -470), tip, (side * 335 * k + turn * 28, -560), (side * 150 + turn * 20, -478)]
        _path_fill(cr, _poly(back, curve=False), CLOTH, None, lw=8)


# ---------------------------------------------------------------- legs and body
def _legs(cr, t, legs, walk):
    if legs == "sit":
        for side in (-1, 1):                     # legs stretched toward the camera, soles showing
            _path_fill(cr, _poly([(side * 30, -150), (side * 105, -150), (side * 120, -40), (side * 40, -40)]),
                       CLOTH, CLOTH_SH)
            _path_fill(cr, _ell(side * 92, -18, 62, 54), CLOTH, CLOTH_SH)
            _path_fill(cr, _ell(side * 92, -14, 40, 34), (0.3, 0.27, 0.33, 1), None, lw=6)
        return
    for side in (-1, 1):
        ph = (walk or 0) + (0 if side < 0 else math.pi)
        lift = 26 * max(0.0, math.sin(ph)) if legs == "walk" else (40 if legs == "jump" else 0)
        dx = 22 * math.cos(ph) if legs == "walk" else 0
        hx = side * 58
        fx, fy = hx + dx, -8 - lift
        _path_fill(cr, _poly([(hx - 38, -170), (hx + 38, -170), (fx + 32, fy - 60), (fx - 32, fy - 60)],
                             curve=False), CLOTH, CLOTH_SH)
        boot = [(fx - 46, fy - 72), (fx + 40, fy - 72), (fx + 56 + side * 8, fy - 22), (fx + 44, fy + 4),
                (fx - 44, fy + 4), (fx - 56 + side * 8, fy - 22)]
        _path_fill(cr, _poly(boot), CLOTH, CLOTH_SH, rim=HAIR_HI)


def _torso(cr, turn, breathe):
    tx = turn * 30
    body = [(-112, -400), (112, -400), (128, -250), (138, -150), (0, -138), (-138, -150), (-128, -250)]
    _path_fill(cr, _poly(body, curve=False), CLOTH, CLOTH_SH)
    zig = [(-138, -150)]                          # red zigzag hem
    for j in range(7):
        zig.append((-138 + (j + 0.5) * 39.4 + tx * 0.3, -150 + (24 if j % 2 == 0 else 0) - 26))
    zig += [(138, -150), (0, -138)]
    cr.save()
    _poly(body, curve=False)(cr)
    cr.clip()
    _path_fill(cr, _poly(zig + [(138, -120), (-138, -120)], curve=False), RED, RED_SH, lw=7)
    cr.restore()
    _poly(body, curve=False)(cr)
    cr.set_source_rgba(*INK)
    cr.set_line_width(LW)
    cr.stroke()
    for by in (-268, -212):                        # gold buttons
        _path_fill(cr, _ell(tx, by, 15, 15), GOLD, GOLD_SH, lw=6)
    jab = [(-62 + tx, -392), (62 + tx, -392), (70 + tx, -340), (40 + tx, -312), (14 + tx, -326), (tx, -300),
           (-14 + tx, -326), (-40 + tx, -312), (-70 + tx, -340)]
    _path_fill(cr, _poly(jab), WHITE, WHITE_SH, lw=8)
    for side in (-1, 1):                           # ruffle lines
        _line(cr, [(tx + side * 22, -380), (tx + side * 26, -350), (tx + side * 18, -326)], 4)
    for side in (-1, 1):                           # red bat bow tie
        wing = [(tx, -408), (tx + side * 48, -432), (tx + side * 96, -420), (tx + side * 80, -398),
                (tx + side * 86, -380), (tx + side * 56, -386), (tx + side * 40, -372), (tx, -394)]
        _path_fill(cr, _poly(wing, curve=False), RED, RED_SH, lw=7)
    _path_fill(cr, _ell(tx, -400, 26, 30), GOLD, GOLD_SH, lw=6)
    _path_fill(cr, _ell(tx, -400, 15, 19), RED, RED_SH, ink=None)
    ellipse(cr, tx - 5, -408, 5, 6)
    cr.set_source_rgba(1, 1, 1, 0.8)
    cr.fill()


# ---------------------------------------------------------------- arms
def _ik(sx, sy, tx, ty, l1, l2, bend):
    dx, dy = tx - sx, ty - sy
    d = max(1e-3, min(l1 + l2 - 1, math.hypot(dx, dy)))
    a = math.atan2(dy, dx)
    c = max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
    e = a + bend * math.acos(c)
    return sx + l1 * math.cos(e), sy + l1 * math.sin(e)


def hand_pos(side, arm, turn=0.0):
    """Hand target in body units for an arm spec (a HANDS name or an (x, y) for the right side)."""
    hx, hy = HANDS[arm] if isinstance(arm, str) else arm
    return side * hx + turn * 25, hy


def _arm(cr, t, side, arm, turn, hold=None, point=False):
    sx, sy = SHOULDER[side]
    sx += turn * 20
    hx, hy = hand_pos(side, arm, turn)
    ex, ey = _ik(sx, sy, hx, hy, 86, 86, -side if hy > sy - 60 else side)
    for col, w in ((INK, 68), (CLOTH, 50)):        # sleeve
        cr.move_to(sx, sy)
        cr.line_to(ex, ey)
        cr.line_to(hx, hy)
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    ang = math.atan2(hy - ey, hx - ex)
    wx, wy = hx - 26 * math.cos(ang), hy - 26 * math.sin(ang)
    cr.save()
    cr.translate(wx, wy)
    cr.rotate(ang)
    _path_fill(cr, _ell(0, 0, 15, 32), WHITE, WHITE_SH, lw=7)
    cr.restore()
    if hold:
        hold(cr, hx, hy, ang)
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(ang)
    _path_fill(cr, _ell(14, 0, 45, 40), SKIN, SKIN_SH, lw=9)
    if point == "claw":                              # three little grabbing fingers
        for k in (-1, 0, 1):
            _path_fill(cr, _poly([(40, k * 20 - 8), (74, k * 26 - 6), (78, k * 26 + 4), (40, k * 20 + 8)]),
                       SKIN, SKIN_SH, lw=7)
    elif point:
        _path_fill(cr, _poly([(36, -10), (82, -8), (84, 8), (36, 10)]), SKIN, SKIN_SH, lw=7)
    for k in (-1, 0, 1):
        _line(cr, [(36, k * 14 - 4), (48, k * 14), (38, k * 14 + 7)], 4)
    cr.restore()
    return hx, hy


# ---------------------------------------------------------------- head
def _eye(cr, cx, cy, rx, ry, eyes, look, blink, t, side):
    if eyes == "happy":
        _line(cr, [(cx - rx * 0.75, cy + 10), (cx, cy - ry * 0.55), (cx + rx * 0.75, cy + 10)], 13)
        return
    if eyes == "closed" or blink >= 0.95:
        _line(cr, [(cx - rx * 0.78, cy + 6), (cx, cy + ry * 0.3), (cx + rx * 0.78, cy + 6)], 12)
        return
    if eyes == "dizzy":
        cr.move_to(cx, cy)
        for k in range(40):
            a = k * 0.45 + t * 6 * side
            r = k * 1.9
            cr.line_to(cx + math.cos(a) * r, cy + math.sin(a) * r)
        cr.set_source_rgba(*INK)
        cr.set_line_width(7)
        cr.stroke()
        return
    _path_fill(cr, _ell(cx, cy, rx, ry), WHITE, None, lw=12)
    lash_lw = 18
    cr.save()
    ellipse(cr, cx, cy, rx - 4, ry - 4)
    cr.clip()
    lx, ly = look
    ir = 0.52 if eyes == "shocked" else 0.8
    ix, iy = cx + lx * rx * 0.25 + side * -6, cy + 6 + ly * ry * 0.2
    ellipse(cr, ix, iy, rx * ir, ry * ir * 1.04)
    cr.set_source(rad(ix, iy - ry * 0.3, ry * ir * 1.3, [(0, EYE_DARK), (0.55, EYE_RED), (1, EYE_LIGHT)]))
    cr.fill()
    ellipse(cr, ix, iy, rx * ir * 0.5, ry * ir * 0.52)
    cr.set_source_rgba(*EYE_DARK)
    cr.fill()
    if eyes == "angry":                            # the top of the eye cut flat by a heavy lid
        cr.move_to(cx - rx - 5, cy - ry * (0.15 if side < 0 else 0.55))
        cr.line_to(cx + rx + 5, cy - ry * (0.55 if side < 0 else 0.15))
        cr.line_to(cx + rx + 5, cy - ry - 5)
        cr.line_to(cx - rx - 5, cy - ry - 5)
        cr.close_path()
        cr.set_source_rgba(*SKIN)
        cr.fill()
    cr.restore()
    cr.arc(cx, cy, rx + 2, math.pi * 1.08, math.pi * 1.92)       # thick upper lash with a little wing
    cr.set_source_rgba(*INK)
    cr.set_line_width(lash_lw)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()
    wx0 = cx + side * rx * 0.92
    _line(cr, [(wx0, cy - ry * 0.4), (wx0 + side * 22, cy - ry * 0.62)], 12, curve=False)
    hl = 1.25 if eyes == "sparkle" else 1.0
    ellipse(cr, ix - rx * 0.28, iy - ry * 0.3, rx * 0.26 * hl, ry * 0.25 * hl)
    cr.set_source_rgba(1, 1, 1, 0.97)
    cr.fill()
    ellipse(cr, ix + rx * 0.22, iy + ry * 0.12, rx * 0.11 * hl, ry * 0.1 * hl)
    cr.fill()
    if eyes == "sparkle":
        for k, (dx, dy) in enumerate(((rx * 0.3, -ry * 0.5), (-rx * 0.1, ry * 0.4))):
            sx, sy, r = ix + dx, iy + dy, 10
            cr.move_to(sx, sy - r)
            cr.line_to(sx + 3, sy - 3)
            cr.line_to(sx + r, sy)
            cr.line_to(sx + 3, sy + 3)
            cr.line_to(sx, sy + r)
            cr.line_to(sx - 3, sy + 3)
            cr.line_to(sx - r, sy)
            cr.line_to(sx - 3, sy - 3)
            cr.close_path()
            cr.fill()
    if eyes == "cry":                              # a wobbling pool on the lower lid
        cr.save()
        ellipse(cr, cx, cy, rx - 4, ry - 4)
        cr.clip()
        ellipse(cr, cx, cy + ry * 0.62 + 3 * math.sin(t * 9), rx, ry * 0.32)
        cr.set_source_rgba(*TEAR)
        cr.fill()
        cr.restore()
    if 0 < blink < 0.95 and eyes not in ("angry",):
        cr.save()
        ellipse(cr, cx, cy, rx + 6, ry + 6)
        cr.clip()
        cr.rectangle(cx - rx - 8, cy - ry - 8, 2 * rx + 16, (2 * ry + 16) * blink)
        cr.set_source_rgba(*SKIN)
        cr.fill()
        cr.restore()
        _line(cr, [(cx - rx, cy - ry + 2 * ry * blink), (cx + rx, cy - ry + 2 * ry * blink)], 10, curve=False)


def _mouth(cr, mx, my, mouth, talk, t):
    w = 62
    if talk is not None:                            # lip sync: 0 closed .. 1 wide
        mouth = "closed" if talk < 0.15 else ("open" if talk < 0.6 else "wide")
    if mouth in ("smirk", "closed"):
        lift = 14 if mouth == "smirk" else 6
        _line(cr, [(mx - w, my - lift * 0.6), (mx, my + 10), (mx + w, my - lift)], 9)
        for fx in (mx - 26, mx + 26):
            cr.move_to(fx - 11, my + 4 - (abs(fx - mx) / w) * 4)
            cr.line_to(fx + 11, my + 4 - (abs(fx - mx) / w) * 4)
            cr.line_to(fx, my + 30)
            cr.close_path()
            cr.set_source_rgba(*WHITE)
            cr.fill_preserve()
            cr.set_source_rgba(*INK)
            cr.set_line_width(5)
            cr.stroke()
        return
    if mouth == "chomp":                           # jaws clamped shut on something, long fangs down, cheeks tight
        cr.move_to(mx - w * 0.9, my - 6)
        for k in range(7):
            cr.line_to(mx - w * 0.9 + (k + 1) * w * 0.257, my - 6 + (7 if k % 2 == 0 else -3))
        cr.set_source_rgba(*INK)
        cr.set_line_width(10)
        cr.stroke()
        for fx in (mx - 30, mx + 30):
            cr.move_to(fx - 13, my - 2)
            cr.line_to(fx + 13, my - 2)
            cr.line_to(fx, my + 44)
            cr.close_path()
            cr.set_source_rgba(*WHITE)
            cr.fill_preserve()
            cr.set_source_rgba(*INK)
            cr.set_line_width(6)
            cr.stroke()
        for side in (-1, 1):                       # squeeze lines at the corners
            _line(cr, [(mx + side * (w + 14), my - 22), (mx + side * (w + 26), my - 4)], 6, curve=False)
        return
    if mouth == "frown":
        _line(cr, [(mx - w * 0.8, my + 14), (mx, my - 8), (mx + w * 0.8, my + 14)], 9)
        return
    if mouth == "wobble":
        cr.move_to(mx - w * 0.8, my + 6)
        for k in range(9):
            cr.line_to(mx - w * 0.8 + k * w * 0.2, my + 6 + (6 if k % 2 else -6))
        cr.set_source_rgba(*INK)
        cr.set_line_width(8)
        cr.stroke()
        return
    if mouth == "o":
        _path_fill(cr, _ell(mx, my + 10, 26, 32), MOUTH_IN, None, lw=9)
        return
    h = {"open": 48, "wide": 86, "grin": 58, "bite": 118}.get(mouth, 48)
    ww = w * (1.4 if mouth == "bite" else 1.15 if mouth in ("grin", "wide") else 0.95)
    fang = 46 if mouth == "bite" else 26
    def shape(c):
        c.move_to(mx - ww, my - 4)
        c.curve_to(mx - ww * 0.4, my + 2, mx + ww * 0.4, my + 2, mx + ww, my - 4)
        c.curve_to(mx + ww * 0.85, my + h * 0.9, mx - ww * 0.85, my + h * 0.9, mx - ww, my - 4)
        c.close_path()
    shape(cr)
    cr.set_source_rgba(*MOUTH_IN)
    cr.fill()
    cr.save()
    shape(cr)
    cr.clip()
    ellipse(cr, mx, my + h * 0.82, ww * 0.62, h * 0.42)
    cr.set_source_rgba(*TONGUE)
    cr.fill()
    cr.restore()
    for fx in (mx - ww * 0.48, mx + ww * 0.48):    # fangs
        cr.move_to(fx - 11 - (4 if fang > 30 else 0), my - 2)
        cr.line_to(fx + 11 + (4 if fang > 30 else 0), my - 2)
        cr.line_to(fx, my + fang)
        cr.close_path()
        cr.set_source_rgba(*WHITE)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(5)
        cr.stroke()
    shape(cr)
    cr.set_source_rgba(*INK)
    cr.set_line_width(9)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def _head(cr, t, turn, tilt, eyes, brows, mouth, talk, look, blink, blush, tears):
    hx, hy = HEAD
    cr.save()
    cr.translate(hx, hy + 250)                     # tilt about the neck
    cr.rotate(tilt)
    cr.translate(-hx, -(hy + 250))
    fx = turn * 58                                 # features slide toward the turn
    # back hair mass: big swept-back volume with flame-like tips at the sides and back
    back = [(-268, -600), (-330, -640), (-302, -700), (-352, -760), (-300, -820), (-322, -900), (-250, -930),
            (-200, -1010), (-60, -1060), (110, -1062), (250, -1010), (300, -925), (352, -880), (318, -808),
            (360, -740), (310, -690), (338, -628), (270, -600)]
    _path_fill(cr, _poly([(x + turn * 12, y) for x, y in back], curve=False), HAIR, HAIR_SH)
    # ears: big, pointing out at eye level (the far one tucks in when turning)
    for side in (-1, 1):
        k = 1 - 0.35 * max(0.0, -turn * side)
        ex0 = side * 252 + turn * 30
        ear = [(ex0, -690), (ex0 + side * 150 * k, -770), (ex0 + side * 48 * k, -585), (ex0 - side * 12, -585)]
        _path_fill(cr, _poly(ear, curve=False), SKIN, SKIN_SH)
        _path_fill(cr, _poly([(ex0 + side * 14, -672), (ex0 + side * 112 * k, -742), (ex0 + side * 40 * k, -612)],
                             curve=False), EAR_IN, None, ink=None)
    # face
    _path_fill(cr, _ell(hx + turn * 14, hy, 275, 250), SKIN, SKIN_SH, rim=SKIN_HI)
    # front hair: the pompadour cap, a deep widow's peak, swept to the back right
    front = [(-292, -690), (-270, -775), (-180, -840), (-80, -830), (-22 + fx * 0.5, -742), (40 + fx * 0.4, -808),
             (150, -850), (260, -800), (296, -700), (330, -830), (290, -960), (180, -1040), (20, -1072),
             (-140, -1050), (-262, -975), (-318, -840)]
    def hair_front(c):
        c.move_to(front[0][0] + turn * 12, front[0][1])
        n = len(front)
        for i in range(n):
            p0, p1, p2, p3 = front[i - 1], front[i], front[(i + 1) % n], front[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            c.curve_to(c1[0] + turn * 12, c1[1], c2[0] + turn * 12, c2[1], p2[0] + turn * 12, p2[1])
        c.close_path()
    _path_fill(cr, hair_front, HAIR, HAIR_SH)
    for (x0, y0), (x1, y1), (x2, y2) in (((-240, -900), (-120, -1010), (60, -1030)),     # swoosh highlights
                                         ((-190, -850), (-60, -950), (140, -985)),
                                         ((60, -840), (180, -910), (270, -900)),
                                         ((-100, -830), (-20, -880), (60, -900))):
        _line(cr, [(x0 + turn * 12, y0), (x1 + turn * 12, y1), (x2 + turn * 12, y2)], 10, HAIR_HI)
    for side in (-1, 1):                           # sideburn tufts
        sx0 = side * 286 + turn * 14
        _path_fill(cr, _poly([(sx0 + side * 4, -720), (sx0 + side * 22, -620), (sx0 - side * 10, -576),
                              (sx0 - side * 26, -690)], curve=False), HAIR, None, lw=8)
    # the curl: a lock hanging from the widow's peak
    cx = -18 + fx * 0.55
    _line(cr, [(cx + 10, -760), (cx + 26, -720), (cx + 2, -690)], 24, HAIR)
    cr.arc(cx - 14, -690, 22, -0.3, math.pi * 1.55)
    cr.set_source_rgba(*HAIR)
    cr.set_line_width(16)
    cr.stroke()
    _line(cr, [(cx + 14, -750), (cx + 22, -722)], 5, HAIR_HI)
    # eyes
    for side in (-1, 1):
        k = 1 - 0.28 * max(0.0, -turn * side)
        _eye(cr, side * 112 + fx, -598, 82 * k, 92, eyes, look, blink, t, side)
    # brows
    if brows or eyes == "angry":
        b = brows or "angry"
        for side in (-1, 1):
            bx = side * 112 + fx
            inner, outer = {"angry": (-700 + 26, -712), "sad": (-718, -690), "up": (-728, -718),
                            "flat": (-706, -706)}[b]
            _line(cr, [(bx - side * 62, inner if b != "angry" else -676), (bx, (inner + outer) / 2 - 8),
                       (bx + side * 70, outer)], 15)
    # blush marks
    if blush:
        for side in (-1, 1):
            bx = side * 178 + fx * 0.8
            for k in range(3):
                _line(cr, [(bx - 22 + k * 15, -508), (bx - 30 + k * 15, -490)], 7, BLUSH, curve=False)
    # tears
    if tears:
        for side in (-1, 1):
            tx0 = side * 112 + fx + side * 40
            ph = (t * 1.6 + (0.5 if side > 0 else 0)) % 1.0
            for k in range(3):
                yy = -540 + ((ph + k / 3) % 1.0) * 170
                ellipse(cr, tx0 + side * 6, yy, 9, 14)
                cr.set_source_rgba(*TEAR)
                cr.fill()
            _line(cr, [(tx0, -548), (tx0 + side * 10, -470), (tx0 + side * 4, -380)], 14, (0.6, 0.88, 1.0, 0.75))
    _mouth(cr, fx * 0.9, -492, mouth, talk, t)
    cr.restore()


# ---------------------------------------------------------------- floor shadow
def floor_shadow(cr, x, y, s, lift=0.0, legs="stand"):
    w = 330 * s * (1.2 if legs == "sit" else 1.0)
    grow = 1 + lift / 300
    fade = 1 / (1 + lift / 80)
    for rx, ry, a in ((w, w * 0.16, 0.22), (w * 0.65, w * 0.1, 0.32)):
        cr.save()
        cr.translate(x, y)
        cr.scale(rx * grow, ry * grow)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y, rx * grow, [(0, (0.06, 0.04, 0.05, a * fade)), (1, (0.06, 0.04, 0.05, 0))]))
        cr.fill()
    if lift < 3 and legs != "sit":
        for side in (-1, 1):
            bx = x + side * 58 * s
            cr.save()
            cr.translate(bx, y - 1)
            cr.scale(52 * s, 12 * s)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.set_source(rad(bx, y - 1, 52 * s, [(0, (0.04, 0.02, 0.03, 0.5)), (1, (0.04, 0.02, 0.03, 0))]))
            cr.fill()


# ---------------------------------------------------------------- the whole character
def vex(cr, t, x, y, s=0.33, turn=0.0, lean=0.0, squash=0.0, tilt=0.0, look=(0.0, 0.0), eyes="open", brows=None,
        mouth="smirk", talk=None, arms=("rest", "rest"), hold=(None, None), point=(False, False), legs="stand",
        walk=None, cape=0.0, blink=0.0, blush=True, tears=False, lift=0.0, rot=0.0, pivot="feet", shadow=True,
        flip=False, held=None):
    """Draw Vex with his feet at (x, y). held(cr): draws something he holds in front of him (screen coordinates),
    between his face and his hands, so his fingers grip it."""
    if shadow:
        floor_shadow(cr, x, y, s, lift, legs)
    bob = 0.012 * math.sin(t * 3.1)
    sit = 110 if legs == "sit" else 0
    outer = cr.get_matrix()
    cr.save()
    cr.translate(x, y - lift)
    if pivot == "center":
        cr.translate(0, -500 * s)
        cr.rotate(rot)
        cr.translate(0, 500 * s)
    else:
        cr.rotate(rot)
    cr.scale(s * (1 + 0.12 * squash - bob * 0.3) * (-1 if flip else 1), s * (1 - 0.14 * squash + bob))
    cr.rotate(lean)
    cr.translate(0, sit)
    sway = 10 * math.sin(t * 2.4) + (24 * math.sin(t * 9) if legs == "walk" or lift > 5 else 0)
    _cape(cr, t, turn, cape, sway)
    _collar(cr, turn, cape)
    if legs == "sit":
        cr.save()
        cr.translate(0, -sit)
        _legs(cr, t, legs, walk)
        cr.restore()
    else:
        _legs(cr, t, legs, walk)
    _torso(cr, turn, bob)
    hands = {}
    late = []
    for side, arm, hd, pt in ((-1, arms[0], hold[0], point[0]), (1, arms[1], hold[1], point[1])):
        if held or (isinstance(arm, str) and arm in OVER_HEAD):
            late.append((side, arm, hd, pt))
        else:
            hands[side] = _arm(cr, t, side, arm, turn, hd, pt)
    _head(cr, t, turn, tilt, eyes, brows, mouth, talk, look, blink, blush, tears)
    if held:
        inner = cr.get_matrix()
        cr.set_matrix(outer)
        held(cr)
        cr.set_matrix(inner)
    for side, arm, hd, pt in late:
        hands[side] = _arm(cr, t, side, arm, turn, hd, pt)
    cr.restore()
    return hands
