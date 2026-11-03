"""Quality test: an original chibi mascot (a tiny alien scientist) drawn with soft shading, glossy eyes, rim light
and a contact shadow, placed on a photo floor. Not the reference creator's character: our own design."""
import math
import sys

import cairo

sys.path.insert(0, "/home/user/Motion-graphics")
from motion.polish import bold_text, ellipse, lin, rad, stroke_line  # noqa: E402

INK = (0.13, 0.09, 0.16, 1)
SKIN_L, SKIN, SKIN_D = (0.80, 0.98, 0.86, 1), (0.52, 0.88, 0.66, 1), (0.25, 0.62, 0.47, 1)
COAT_L, COAT, COAT_D = (1, 1, 1, 1), (0.93, 0.95, 0.98, 1), (0.70, 0.75, 0.85, 1)
EYE_TOP, EYE_BOT = (0.10, 0.08, 0.22, 1), (0.14, 0.52, 0.66, 1)
BULB = (1.0, 0.80, 0.25, 1)


def blob(cr, pts):
    """Closed smooth path through points (Catmull-Rom -> Bezier)."""
    n = len(pts)
    cr.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        cr.curve_to(*c1, *c2, *p2)
    cr.close_path()


def shaded(cr, path, light, mid, dark, lx, ly, bbox, rim=True, lw=7):
    """Fill a path with soft 3-tone lighting from (lx, ly) (unit dir), a core shadow and a rim light, then ink it."""
    x0, y0, x1, y1 = bbox
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 0.62
    path(cr)
    cr.set_source(rad(cx + lx * r * 0.45, cy + ly * r * 0.45, r * 1.25,
                      [(0, light), (0.45, mid), (1, dark)], r0=r * 0.05))
    cr.fill_preserve()
    cr.save()
    cr.clip_preserve()
    cr.new_path()
    # occlusion along the far edge
    cr.set_source(rad(cx - lx * r * 0.9, cy - ly * r * 0.9, r * 1.1,
                      [(0, (dark[0], dark[1], dark[2], 0.35)), (1, (dark[0], dark[1], dark[2], 0))]))
    cr.paint()
    if rim:   # a thin cool rim light just inside the shadow-side edge, as if bounced off the floor/walls
        cr.save()
        cr.translate(lx * lw * 1.7, ly * lw * 1.7)
        path(cr)
        cr.restore()
        cr.set_source_rgba(0.85, 0.97, 1.0, 0.5)
        cr.set_line_width(lw * 1.1)
        cr.stroke()
    cr.restore()
    path(cr)
    cr.set_source_rgba(*INK)
    cr.set_line_width(lw)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def contact_shadow(cr, x, y, w, k=1.0):
    for rx, ry, a in ((w * 1.25, w * 0.22, 0.24), (w * 0.9, w * 0.15, 0.3), (w * 0.55, w * 0.09, 0.42)):
        cr.save()
        cr.translate(x, y)
        cr.scale(rx * k, ry * k)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y, rx * k, [(0, (0.12, 0.08, 0.05, a)), (1, (0.12, 0.08, 0.05, 0))]))
        cr.fill()


def eye(cr, x, y, rx, ry, look=(0, 0), lid=0.0, mood="open"):
    if mood == "happy":     # ^ ^ closed happy eyes
        stroke_line(cr, [(x - rx * 0.7, y + 6), (x, y - ry * 0.45), (x + rx * 0.7, y + 6)], 9, INK)
        return
    if mood == "shut":
        stroke_line(cr, [(x - rx * 0.7, y), (x, y + ry * 0.22), (x + rx * 0.7, y)], 9, INK)
        return
    ellipse(cr, x, y, rx, ry)
    cr.set_source(lin(0, y - ry, 0, y + ry, [(0, EYE_TOP), (0.55, (0.10, 0.20, 0.40, 1)), (1, EYE_BOT)]))
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(6)
    cr.stroke()
    lx, ly = look
    # pupil glow ring and reflections
    ellipse(cr, x + lx * 6, y + ry * 0.35 + ly * 6, rx * 0.62, ry * 0.32)
    cr.set_source(rad(x + lx * 6, y + ry * 0.4, rx * 0.7, [(0, (0.45, 0.95, 1.0, 0.55)), (1, (0.45, 0.95, 1.0, 0))]))
    cr.fill()
    ellipse(cr, x - rx * 0.32 + lx * 8, y - ry * 0.38 + ly * 8, rx * 0.36, ry * 0.30, -0.4)
    cr.set_source_rgba(1, 1, 1, 0.96)
    cr.fill()
    ellipse(cr, x + rx * 0.36 + lx * 8, y + ry * 0.05 + ly * 8, rx * 0.13, ry * 0.11)
    cr.set_source_rgba(1, 1, 1, 0.85)
    cr.fill()
    if mood == "cry":       # a wobbling tear pool on the lower lid
        ellipse(cr, x, y + ry * 0.62, rx * 0.85, ry * 0.28)
        cr.set_source_rgba(0.6, 0.9, 1.0, 0.75)
        cr.fill()
    if lid > 0:             # eyelid closes from the top (blink)
        cr.save()
        ellipse(cr, x, y, rx + 3, ry + 3)
        cr.clip()
        cr.rectangle(x - rx - 4, y - ry - 4, 2 * rx + 8, (2 * ry + 8) * lid)
        cr.set_source_rgba(*SKIN)
        cr.fill()
        cr.restore()
        stroke_line(cr, [(x - rx, y - ry + 2 * ry * lid), (x + rx, y - ry + 2 * ry * lid)], 6, INK, curve=False)


def zib(cr, t, x, y, s=1.0, mood="open", look=(0, 0), blink=0.0, squash=0.0, tilt=0.0, arms=("down", "down"),
        mouth="smile", light=(0.55, -0.75), ant_lag=(0.0, 0.0)):
    """The mascot, feet at (x, y). squash > 0 squashes (landing), < 0 stretches (jump)."""
    lx, ly = light
    contact_shadow(cr, x, y + 2, 92 * s, 1 - 0.25 * max(0, -squash))
    cr.save()
    cr.translate(x, y)
    cr.scale(s * (1 + 0.12 * squash), s * (1 - 0.12 * squash))
    cr.rotate(tilt)
    # feet
    for fx in (-34, 34):
        shaded(cr, lambda c, fx=fx: ellipse(c, fx, -10, 30, 16), SKIN_L, SKIN, SKIN_D, lx, ly,
               (fx - 30, -26, fx + 30, 6), rim=False, lw=6)
    # body = lab coat
    coat = lambda c: blob(c, [(-62, -20), (-66, -70), (-48, -118), (0, -132), (48, -118), (66, -70), (62, -20),
                              (0, -8)])
    shaded(cr, coat, COAT_L, COAT, COAT_D, lx, ly, (-66, -132, 66, -8))
    stroke_line(cr, [(0, -128), (0, -14)], 4, (0.55, 0.6, 0.72, 1), curve=False)            # coat opening
    stroke_line(cr, [(-26, -122), (0, -88), (26, -122)], 5, (0.55, 0.6, 0.72, 1))            # lapels
    for by in (-82, -56, -32):
        ellipse(cr, 8, by, 5, 5)
        cr.set_source_rgba(0.55, 0.6, 0.72, 1)
        cr.fill()
    cr.rectangle(-46, -70, 26, 20)                                                              # pocket + pen
    cr.set_source_rgba(0.55, 0.6, 0.72, 1)
    cr.set_line_width(3.5)
    cr.stroke()
    stroke_line(cr, [(-38, -70), (-38, -90)], 7, (0.25, 0.45, 0.95, 1), curve=False)
    # arms: little sleeves with mitten hands
    poses = {"down": (1.25, 46), "up": (-1.35, 52), "wave": (-1.0, 54), "hip": (0.55, 38), "point": (-0.15, 60)}
    for side, pose in ((-1, arms[1]), (1, arms[0])):
        ang, ln = poses[pose]
        if pose == "wave":
            ang += 0.35 * math.sin(t * 9)
        sx, sy = side * 54, -104
        hx, hy = sx + side * math.cos(ang) * ln, sy + math.sin(ang) * ln
        stroke_line(cr, [(sx, sy), (hx, hy)], 30, INK, curve=False)
        stroke_line(cr, [(sx, sy), (hx, hy)], 19, COAT, curve=False)
        shaded(cr, lambda c, hx=hx, hy=hy: ellipse(c, hx, hy, 15, 14), SKIN_L, SKIN, SKIN_D, lx, ly,
               (hx - 15, hy - 14, hx + 15, hy + 14), rim=False, lw=5)
    # head
    hy0 = -232
    head = lambda c: blob(c, [(-128, hy0 + 10), (-118, hy0 - 62), (-62, hy0 - 104), (0, hy0 - 112), (62, hy0 - 104),
                              (118, hy0 - 62), (128, hy0 + 10), (96, hy0 + 78), (0, hy0 + 98), (-96, hy0 + 78)])
    # antennae (behind the head outline, in front of the back)
    for sx_, lag in ((-1, ant_lag[0]), (1, ant_lag[1])):
        bx, by = sx_ * 46, hy0 - 104
        tx, ty = sx_ * (76 + 10 * lag) + 14 * lag, hy0 - 178 + 6 * abs(lag)
        mx, my = sx_ * 52 + 10 * lag, hy0 - 150
        stroke_line(cr, [(bx, by), (mx, my), (tx, ty)], 14, INK)
        stroke_line(cr, [(bx, by), (mx, my), (tx, ty)], 6, SKIN_D)
        cr.arc(tx, ty, 46, 0, 2 * math.pi)
        cr.set_source(rad(tx, ty, 46, [(0, (1, 0.85, 0.35, 0.55)), (1, (1, 0.85, 0.35, 0))]))
        cr.fill()
        shaded(cr, lambda c, tx=tx, ty=ty: ellipse(c, tx, ty, 17, 17), (1, 0.97, 0.75, 1), BULB, (0.9, 0.5, 0.1, 1),
               lx, ly, (tx - 17, ty - 17, tx + 17, ty + 17), rim=False, lw=5)
    shaded(cr, head, SKIN_L, SKIN, SKIN_D, lx, ly, (-128, hy0 - 112, 128, hy0 + 98))
    # cheeks
    for cx_ in (-84, 84):
        cr.arc(cx_, hy0 + 40, 26, 0, 2 * math.pi)
        cr.set_source(rad(cx_, hy0 + 40, 26, [(0, (1, 0.55, 0.6, 0.55)), (1, (1, 0.55, 0.6, 0))]))
        cr.fill()
    # eyes
    for ex in (-50, 50):
        eye(cr, ex, hy0 - 4, 38, 46, look, blink, mood)
    if mood == "angry":
        for ex in (-50, 50):
            stroke_line(cr, [(ex - 34 * (1 if ex < 0 else -1), hy0 - 62), (ex + 30 * (1 if ex < 0 else -1), hy0 - 44)],
                        10, INK, curve=False)
    # mouth
    my_ = hy0 + 58
    if mouth == "smile":
        stroke_line(cr, [(-16, my_ - 4), (-8, my_ + 4), (0, my_ - 1), (8, my_ + 4), (16, my_ - 4)], 6, INK)
    elif mouth == "o":
        ellipse(cr, 0, my_ + 4, 13, 16)
        cr.set_source_rgba(0.35, 0.08, 0.18, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(5)
        cr.stroke()
    elif mouth == "sad":
        stroke_line(cr, [(-16, my_ + 6), (0, my_ - 4), (16, my_ + 6)], 6, INK)
    elif mouth == "grin":
        cr.move_to(-26, my_ - 6)
        cr.curve_to(-16, my_ + 22, 16, my_ + 22, 26, my_ - 6)
        cr.close_path()
        cr.set_source_rgba(0.35, 0.08, 0.18, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(5)
        cr.stroke()
    cr.restore()


def reply(cr, x, y, text, size=40):
    """The mascot's tiny red line above its head (the reference's convention), handwritten."""
    bold_text(cr, text, x, y, size, (0.92, 0.15, 0.15, 1), font="Kalam", outline=(1, 1, 1, 1), ow=7, shadow=0.0)
