"""Polished insect characters for the polished look (motion/polish.py): bees, a wasp, larvae, honeycomb cells.

bee(cr, t, x, y, s, kind=...) draws an upright cartoon bee whose body centre is at (x, y). kind: "worker",
"drone" (bigger, rounder, huge eyes, no stinger, as real drones), "queen" (long abdomen, crown, lashes).
Faces: eyes in open/happy/wide/half/closed/x/angry/sad/shades, mouth in smile/grin/o/flat/sad/smug/open/talk.
"""
import math

from .engine import cairo, hexc
from .polish import OUTLINE, WHITE, alpha, ellipse, ground_shadow, lin, paint, rad, rrect, shade, smooth, \
    stroke_line

YELLOW = hexc("#ffc93c")
STRIPE = hexc("#3b2a20")
LIMB = hexc("#3b2a20")
BLUSH = hexc("#ff7d8a")
WING = hexc("#dff3ff")
GOLD = hexc("#ffcf3f")

KINDS = {
    #        head r, body rx, body ry, body y, stinger, body colour
    "worker": dict(hr=50, brx=48, bry=56, by=44, sting=True, col=YELLOW),
    "drone": dict(hr=56, brx=62, bry=64, by=50, sting=False, col=hexc("#f2b233")),
    "queen": dict(hr=50, brx=46, bry=80, by=62, sting=True, col=hexc("#ffbe2e")),
}

ARMS = {   # hand position relative to the shoulder (x toward the facing side)
    "down": (10, 52), "hips": (30, 30), "wave": (30, -58), "up": (16, -66), "point": (62, -10),
    "hold": (46, 20), "out": (58, 10), "chin": (-6, -30), "face": (-12, -50), "push": (64, 6),
}


def _wing(cr, sx, sy, ang, length, width, a, worn):
    cr.save()
    cr.translate(sx, sy)
    cr.rotate(ang)
    if worn:
        cr.push_group()
    ellipse(cr, 0, -length * 0.5, width, length * 0.5)
    cr.set_source(lin(0, -length, 0, 0, [(0, alpha(WHITE, 0.85 * a)), (1, alpha(WING, 0.45 * a))]))
    cr.fill_preserve()
    cr.set_source_rgba(*alpha(hexc("#6f93b8"), 0.85 * a))
    cr.set_line_width(3)
    cr.stroke()
    stroke_line(cr, [(0, -4), (width * 0.15, -length * 0.45), (0, -length * 0.85)], 1.6,
                alpha(hexc("#6f93b8"), 0.6 * a))
    if worn:      # frayed tips and a couple of holes, cut out of the wing only (it's drawn in its own group)
        cr.set_operator(cairo.OPERATOR_DEST_OUT)
        for px, py, r in ((width * 0.6, -length * 0.92, 11), (-width * 0.5, -length * 0.8, 9),
                          (width * 0.1, -length * 0.62, 6), (width * 0.85, -length * 0.55, 8)):
            cr.arc(px, py, r, 0, 2 * math.pi)
            cr.set_source_rgba(0, 0, 0, 1)
            cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.pop_group_to_source()
        cr.paint()
    cr.restore()


def _eye(cr, ex, ey, rx, ry, look, mood, drone=False):
    if mood in ("happy", "closed", "x"):
        if mood == "happy":
            cr.arc(ex, ey + ry * 0.35, rx * 0.8, math.pi * 1.1, math.pi * 1.9)
            paint(cr, None, OUTLINE, 5)
        elif mood == "closed":
            stroke_line(cr, [(ex - rx * 0.8, ey + 2), (ex, ey + 6), (ex + rx * 0.8, ey + 2)], 5, OUTLINE)
        else:
            for d in (-1, 1):
                stroke_line(cr, [(ex - rx * 0.6, ey - ry * 0.5 * d), (ex + rx * 0.6, ey + ry * 0.5 * d)], 5,
                            OUTLINE, curve=False)
        return
    if drone:     # big dark compound eyes, the way real drones look
        ellipse(cr, ex, ey, rx, ry)
        paint(cr, rad(ex - rx * 0.3, ey - ry * 0.4, ry * 1.3,
                      [(0, hexc("#6b4e3a")), (0.5, hexc("#2b1d16")), (1, hexc("#120a06"))]), OUTLINE, 4)
        ellipse(cr, ex - rx * 0.35 + look[0] * 4, ey - ry * 0.4, rx * 0.34, ry * 0.24, -0.4)
        paint(cr, alpha(WHITE, 0.9), None, 0)
        ellipse(cr, ex + rx * 0.3, ey + ry * 0.35, rx * 0.12, ry * 0.1)
        paint(cr, alpha(WHITE, 0.7), None, 0)
        return
    k = 1.18 if mood == "wide" else 1.0
    ellipse(cr, ex, ey, rx * k, ry * k)
    paint(cr, rad(ex - rx * 0.2, ey - ry * 0.3, ry * 1.2, [(0, WHITE), (1, hexc("#e7ecf2"))]), OUTLINE, 4)
    pr = 0.55 if mood == "wide" else 0.68
    px, py = ex + look[0] * rx * 0.28, ey + look[1] * ry * 0.22 + ry * 0.08
    ellipse(cr, px, py, rx * pr, ry * pr)
    paint(cr, rad(px, py - ry * 0.2, ry * pr, [(0, hexc("#5a3b28")), (0.7, hexc("#2b1d16")), (1, hexc("#160d08"))]),
          None, 0)
    ellipse(cr, px + rx * 0.22, py - ry * 0.28, rx * 0.2, ry * 0.18)
    paint(cr, WHITE, None, 0)
    ellipse(cr, px - rx * 0.2, py + ry * 0.25, rx * 0.09, ry * 0.08)
    paint(cr, alpha(WHITE, 0.85), None, 0)


def _lid(cr, ex, ey, rx, ry, frac, head_col, slope=0.0):
    """Eyelid covering the top `frac` of the eye (half-asleep, smug, sad)."""
    cr.save()
    ellipse(cr, ex, ey, rx + 1, ry + 1)
    cr.clip()
    top = ey - ry - 2
    cut = top + (2 * ry + 4) * frac
    cr.move_to(ex - rx - 4, top)
    cr.line_to(ex + rx + 4, top)
    cr.line_to(ex + rx + 4, cut - slope * rx)
    cr.line_to(ex - rx - 4, cut + slope * rx)
    cr.close_path()
    cr.set_source_rgba(*head_col)
    cr.fill()
    stroke_line(cr, [(ex - rx - 4, cut + slope * rx), (ex + rx + 4, cut - slope * rx)], 4.5, OUTLINE, curve=False)
    cr.restore()


def _mouth(cr, mx, my, mood, t):
    if mood == "smile":
        cr.arc(mx, my - 8, 13, math.pi * 0.2, math.pi * 0.8)
        paint(cr, None, OUTLINE, 4.5)
    elif mood in ("grin", "open", "talk"):
        h = {"grin": 14, "open": 24}.get(mood, 8 + 9 * abs(math.sin(t * 17)))
        cr.move_to(mx - 16, my - 4)
        cr.curve_to(mx - 14, my + h, mx + 14, my + h, mx + 16, my - 4)
        cr.close_path()
        paint(cr, hexc("#7a2b35"), OUTLINE, 4)
        if h > 10:
            ellipse(cr, mx, my + h * 0.55, 8, 4)
            paint(cr, hexc("#ff8a95"), None, 0)
    elif mood == "o":
        ellipse(cr, mx, my + 2, 8, 10)
        paint(cr, hexc("#7a2b35"), OUTLINE, 4)
    elif mood == "flat":
        stroke_line(cr, [(mx - 12, my), (mx + 12, my)], 4.5, OUTLINE, curve=False)
    elif mood == "sad":
        cr.arc(mx, my + 12, 12, math.pi * 1.2, math.pi * 1.8)
        paint(cr, None, OUTLINE, 4.5)
    elif mood == "smug":
        stroke_line(cr, [(mx - 12, my + 2), (mx + 2, my + 3), (mx + 14, my - 6)], 4.5, OUTLINE)


def _arm(cr, sx, sy, pose, facing, side):
    hx, hy = ARMS.get(pose, ARMS["down"]) if isinstance(pose, str) else pose
    hx *= facing if side > 0 else -facing
    ex, ey = sx + hx, sy + hy
    mx, my = (sx + ex) / 2 + side * 6, (sy + ey) / 2 + 6
    stroke_line(cr, [(sx, sy), (mx, my), (ex, ey)], 9, LIMB)
    cr.arc(ex, ey, 8, 0, 2 * math.pi)
    paint(cr, LIMB, None, 0)
    return ex, ey


def bee(cr, t, x, y, s=1.0, kind="worker", facing=1, eyes="open", mouth="smile", look=(0.0, 0.0),
        arms=("down", "down"), fly=False, flap=1.0, wings_worn=False, bob=True, shadow=True, crown=None,
        shades=False, tilt=0.0, hold=None, squash=0.0, lid=0.0, brows=None, blush=True, seed=0):
    """An upright cartoon bee. `hold(cr, hand_x, hand_y)` draws a prop in the front hand (local coordinates)."""
    k = KINDS[kind]
    hr, brx, bry, by = k["hr"], k["brx"], k["bry"], k["by"]
    by += 10
    col = k["col"]
    ph = seed * 1.7
    dy = (math.sin(t * (6.0 if fly else 2.2) + ph) * (7 if fly else 2.5)) if bob else 0.0
    if shadow:
        ground_shadow(cr, x, y + (by + bry + 26) * s + (0 if not fly else 40 * s), brx * 1.2 * s,
                      0.25 if not fly else 0.14)
    cr.save()
    cr.translate(x, y + dy * s)
    cr.rotate(tilt)
    cr.scale(s * (1 + squash * 0.12), s * (1 - squash * 0.12))
    # ---- wings (behind the body)
    rate = 9.0 if fly else 1.6
    amp = (0.42 if fly else 0.12) * flap
    for side in (-1, 1):
        base = side * 0.62
        if fly:   # motion-blurred flap: ghost copies either side of the current angle
            a0 = math.sin(t * rate * 2 * math.pi + ph) * amp
            for g, ga in ((-0.22, 0.28), (0.0, 0.75), (0.22, 0.28)):
                _wing(cr, side * 22, by - bry * 0.55, base + side * (a0 + g), 92, 34, ga, wings_worn)
        else:
            a0 = math.sin(t * rate * 2 * math.pi + ph) * amp
            _wing(cr, side * 22, by - bry * 0.55, base + side * a0, 88, 32, 1.0, wings_worn)
    # ---- legs
    for side in (-1, 1):
        stroke_line(cr, [(side * brx * 0.35, by + bry * 0.8), (side * brx * 0.42, by + bry + 18)], 9, LIMB,
                    curve=False)
        ellipse(cr, side * brx * 0.42 + side * 4, by + bry + 22, 12, 7)
        paint(cr, LIMB, None, 0)
    # ---- stinger
    if k["sting"]:
        cr.move_to(-8, by + bry - 6)
        cr.line_to(8, by + bry - 6)
        cr.line_to(0, by + bry + 14)
        cr.close_path()
        paint(cr, STRIPE, OUTLINE, 3)
    # ---- body with stripes
    ellipse(cr, 0, by, brx, bry)
    paint(cr, rad(-brx * 0.3, by - bry * 0.35, max(brx, bry) * 1.25,
                  [(0, shade(col, 0.55)), (0.45, col), (1, shade(col, -0.22))]), None, 0)
    cr.save()
    ellipse(cr, 0, by, brx, bry)
    cr.clip()
    n = 3 if kind == "queen" else 2
    for j in range(n):
        yy = by - bry * 0.15 + j * bry * (0.62 if n == 2 else 0.46)
        cr.move_to(-brx - 5, yy - 9)
        cr.curve_to(-brx * 0.4, yy - 1, brx * 0.4, yy - 1, brx + 5, yy - 9)
        cr.line_to(brx + 5, yy + 9)
        cr.curve_to(brx * 0.4, yy + 17, -brx * 0.4, yy + 17, -brx - 5, yy + 9)
        cr.close_path()
        cr.set_source_rgba(*STRIPE)
        cr.fill()
    ellipse(cr, -brx * 0.38, by - bry * 0.42, brx * 0.22, bry * 0.16, -0.5)
    cr.set_source_rgba(1, 1, 1, 0.45)
    cr.fill()
    cr.restore()
    ellipse(cr, 0, by, brx, bry)
    paint(cr, None, OUTLINE, 5)
    # ---- back arm, then fuzzy collar
    shoulder_y = by - bry * 0.55
    _arm(cr, -facing * brx * 0.62, shoulder_y + 6, arms[1], facing, -1)
    ellipse(cr, 0, by - bry * 0.78, brx * 0.62, 16)
    paint(cr, rad(0, by - bry * 0.82, brx * 0.7, [(0, hexc("#fff3c4")), (1, hexc("#f2c96a"))]), OUTLINE, 4)
    # ---- head
    hy = by - bry - hr * 0.62
    for side in (-1, 1):   # antennae
        w = math.sin(t * 3.1 + ph + side) * 4
        stroke_line(cr, [(side * hr * 0.3, hy - hr * 0.82), (side * hr * 0.48 + w, hy - hr * 1.22),
                         (side * hr * 0.62 + w * 1.5, hy - hr * 1.42)], 5, LIMB)
        cr.arc(side * hr * 0.62 + w * 1.5, hy - hr * 1.42, 7.5, 0, 2 * math.pi)
        paint(cr, rad(side * hr * 0.6 + w * 1.5, hy - hr * 1.46, 9, [(0, hexc("#7a5a44")), (1, LIMB)]), OUTLINE, 2.5)
    head_col = shade(col, 0.12)
    ellipse(cr, 0, hy, hr, hr * 0.95)
    paint(cr, rad(-hr * 0.3, hy - hr * 0.4, hr * 1.3, [(0, shade(col, 0.6)), (0.5, head_col), (1, shade(col, -0.15))]),
          OUTLINE, 5)
    ellipse(cr, -hr * 0.42, hy - hr * 0.5, hr * 0.22, hr * 0.12, -0.6)
    cr.set_source_rgba(1, 1, 1, 0.5)
    cr.fill()
    fx = facing * hr * 0.12
    drone = kind == "drone"
    erx, ery = (hr * 0.38, hr * 0.48) if drone else (hr * 0.27, hr * 0.34)
    eyx = hy - hr * (0.16 if drone else 0.1)
    for side in (-1, 1):
        ex = fx + side * hr * (0.42 if drone else 0.38)
        if eyes == "shades" or shades:
            continue
        _eye(cr, ex, eyx, erx, ery, look, eyes, drone and eyes not in ("happy", "closed", "x"))
        if lid or eyes in ("half", "sad", "angry"):
            frac = lid or {"half": 0.5, "sad": 0.32, "angry": 0.3}[eyes]
            slope = {"sad": -0.25 * side, "angry": 0.3 * side}.get(eyes, 0.0)
            if eyes not in ("happy", "closed", "x"):
                _lid(cr, ex, eyx, erx * (1.18 if eyes == "wide" else 1), ery, frac, head_col, slope)
        if kind == "queen" and eyes not in ("happy", "closed", "x"):
            for j in range(3):
                a = -math.pi / 2 + side * (0.4 + j * 0.28)
                stroke_line(cr, [(ex + side * erx * 0.6 * math.cos(a) * side, eyx - ery * 0.92),
                                 (ex + side * (erx * 0.5 + j * 7), eyx - ery * 1.25 - (2 - j) * 2)], 3, OUTLINE,
                            curve=False)
    if shades or eyes == "shades":
        cr.move_to(fx - hr * 0.78, eyx - 14)
        cr.line_to(fx + hr * 0.78, eyx - 14)
        cr.line_to(fx + hr * 0.7, eyx + 10)
        cr.curve_to(fx + hr * 0.45, eyx + 24, fx + hr * 0.12, eyx + 18, fx + 4, eyx - 2)
        cr.curve_to(fx - hr * 0.12, eyx + 18, fx - hr * 0.45, eyx + 24, fx - hr * 0.7, eyx + 10)
        cr.close_path()
        paint(cr, lin(0, eyx - 14, 0, eyx + 24, [(0, hexc("#3a3f52")), (1, hexc("#0f1118"))]), OUTLINE, 4)
        stroke_line(cr, [(fx - hr * 0.55, eyx - 6), (fx - hr * 0.3, eyx + 6)], 4, alpha(WHITE, 0.5), curve=False)
    if brows:
        for side in (-1, 1):
            ex = fx + side * hr * 0.38
            tilt_b = {"angry": 0.35, "worried": -0.35, "up": -0.1}[brows] * side
            stroke_line(cr, [(ex - 14, eyx - ery - 12 - tilt_b * 14), (ex + 14, eyx - ery - 12 + tilt_b * 14)], 6,
                        OUTLINE, curve=False)
    if blush:
        for side in (-1, 1):
            ellipse(cr, fx + side * hr * 0.6, hy + hr * 0.3, 11, 7)
            cr.set_source_rgba(*alpha(BLUSH, 0.45))
            cr.fill()
    _mouth(cr, fx, hy + hr * 0.42, mouth, t)
    if crown or kind == "queen":
        cy = hy - hr * 0.9
        cr.move_to(-30, cy + 10)
        for j, (px, py) in enumerate(((-30, cy - 22), (-15, cy - 4), (0, cy - 28), (15, cy - 4), (30, cy - 22))):
            cr.line_to(px, py)
        cr.line_to(30, cy + 10)
        cr.close_path()
        paint(cr, lin(0, cy - 28, 0, cy + 10, [(0, hexc("#fff0a0")), (0.5, GOLD), (1, hexc("#d99a12"))]), OUTLINE, 4)
        for px in (-15, 0, 15):
            cr.arc(px, cy + 2, 4, 0, 2 * math.pi)
            paint(cr, hexc("#e8473f"), None, 0)
    # ---- front arm (+ prop)
    hx, hy2 = _arm(cr, facing * brx * 0.62, shoulder_y + 6, arms[0], facing, 1)
    if hold:
        hold(cr, hx, hy2)
    cr.restore()


def larva(cr, t, x, y, s=1.0, mouth="open", seed=0):
    """A baby bee: a curled white grub with a tiny face, mouth open for food."""
    cr.save()
    cr.translate(x, y + math.sin(t * 3 + seed) * 2)
    cr.scale(s, s)
    for j in range(5, -1, -1):
        a = math.pi * (0.15 + j * 0.24)
        ellipse(cr, 34 * math.cos(a), 18 * math.sin(a) + 8, 22 - j, 20 - j)
        paint(cr, rad(34 * math.cos(a) - 6, 18 * math.sin(a), 26, [(0, WHITE), (1, hexc("#f0e6d6"))]), OUTLINE, 3.5)
    ellipse(cr, 30, -8, 26, 23)
    paint(cr, rad(24, -16, 30, [(0, WHITE), (1, hexc("#f2e9da"))]), OUTLINE, 4)
    for side in (-1, 1):
        cr.arc(30 + side * 9, -12, 3.5, 0, 2 * math.pi)
        paint(cr, OUTLINE, None, 0)
    _mouth(cr, 30, 2, mouth, t)
    ellipse(cr, 18, -4, 5, 3)
    cr.set_source_rgba(*alpha(BLUSH, 0.5))
    cr.fill()
    cr.restore()


def wasp(cr, t, x, y, s=1.0, facing=-1, eyes="angry", mouth="flat", fly=True, seed=3):
    """The intruder: sharper, yellow-black, narrow waist, angry brows."""
    cr.save()
    cr.translate(x, y + math.sin(t * 7 + seed) * 5)
    cr.scale(s * facing, s)
    for side in (-1, 1):
        a0 = math.sin(t * 9 * 2 * math.pi) * 0.4
        for g, ga in ((-0.2, 0.3), (0, 0.75), (0.2, 0.3)):
            _wing(cr, side * 10, -20, side * (0.7 + a0 + g), 80, 22, ga, False)
    smooth(cr, [(-26, 10), (0, -2), (26, 10), (30, 60), (0, 104), (-30, 60)])
    paint(cr, lin(0, 0, 0, 100, [(0, hexc("#ffe14a")), (1, hexc("#e0a800"))]), OUTLINE, 5)
    cr.set_source_rgba(*STRIPE)
    cr.save()
    smooth(cr, [(-26, 10), (0, -2), (26, 10), (30, 60), (0, 104), (-30, 60)])
    cr.clip()
    cr.rectangle(-40, 26, 80, 11)
    cr.rectangle(-40, 50, 80, 11)
    cr.rectangle(-40, 74, 80, 11)
    cr.fill()
    cr.restore()
    cr.move_to(-6, 100)
    cr.line_to(6, 100)
    cr.line_to(0, 126)
    cr.close_path()
    paint(cr, STRIPE, OUTLINE, 3)
    ellipse(cr, 0, -12, 20, 16)
    paint(cr, hexc("#3b2a20"), OUTLINE, 4)
    ellipse(cr, 0, -66, 40, 36)
    paint(cr, rad(-10, -78, 46, [(0, hexc("#fff07a")), (1, hexc("#e8b400"))]), OUTLINE, 5)
    for side in (-1, 1):
        stroke_line(cr, [(side * 14, -98), (side * 26, -126), (side * 40, -134)], 4, LIMB)
        _eye(cr, 6 + side * 15, -70, 11, 13, (0.6, 0), "open")
        stroke_line(cr, [(6 + side * 15 - 13, -88 - side * 5), (6 + side * 15 + 13, -88 + side * 5)], 6, OUTLINE,
                    curve=False)
    _mouth(cr, 8, -46, mouth, t)
    cr.restore()


def comb_cell(cr, cx, cy, r, fill="honey", t=0.0):
    """One honeycomb cell seen head-on: rim, deep inside, and contents (honey / empty / capped)."""
    from .polish import hexagon
    hexagon(cr, cx, cy, r, math.pi / 6)
    paint(cr, lin(cx, cy - r, cx, cy + r, [(0, hexc("#ffd767")), (1, hexc("#e09a1c"))]), hexc("#b8730f"), 3)
    hexagon(cr, cx, cy, r * 0.78, math.pi / 6)
    if fill == "honey":
        paint(cr, rad(cx - r * 0.2, cy - r * 0.3, r, [(0, hexc("#ffe28a")), (0.6, hexc("#f2a81d")),
                                                      (1, hexc("#c96f05"))]), None, 0)
        ellipse(cr, cx - r * 0.25, cy - r * 0.3, r * 0.22, r * 0.12, -0.5)
        cr.set_source_rgba(1, 1, 1, 0.55)
        cr.fill()
    elif fill == "capped":
        paint(cr, rad(cx, cy - r * 0.2, r, [(0, hexc("#fff6d8")), (1, hexc("#ead29a"))]), None, 0)
    else:
        paint(cr, rad(cx, cy, r * 0.8, [(0, hexc("#7a4a12")), (1, hexc("#b8730f"))]), None, 0)
