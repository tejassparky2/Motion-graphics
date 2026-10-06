"""Shared pieces for the "researchers found / clever words from history" videos: a close camera, title cards,
quote scrolls and the two answer buttons at the end. Coordinates are world units; the camera puts its focus point
at the centre of the 720x1280 frame, so screen y = 640 + zoom * (world y - focus y)."""
from .engine import INK, WHITE, at, blob, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from .kit import camera

CLOSE = (1.5, 360, 800)        # people standing at world y 960 fill the frame and stay clear of the captions
PARCH = hexc("#f4e4bc")
CREAM = hexc("#fdf6e3")
GREEN = hexc("#2e9e52")
RED = hexc("#e0483d")
BLUE = hexc("#3f6fb5")
GOLD_D = hexc("#b9862a")


def bg(cr, t, keys, sky, ground=None, ground_y=960, dur=0.3):
    cr.set_source_rgba(*sky)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    if ground is not None:
        shape(cr, [(-600, ground_y), (1400, ground_y), (1400, 2400), (-600, 2400)], ground, seed=1, amp=0.5, lw=4)


def card(cr, t, start, x, y, s, top, bottom, top_col=INK, bottom_col=RED, seed=50, w=460):
    """A two-line title card that pops in at `start`."""
    if t < start:
        return
    with at(cr, x, y, max(0.6, pop(t, start, 0.3)) * s, rot=-0.03):
        shape(cr, rrect_pts(-w / 2, -90, w, 180, 18, 14), CREAM, seed=seed, amp=0.5, lw=5)
        write(cr, [(top, top_col)], 0, -14, 48, align="center", bold=True)
        write(cr, [(bottom, bottom_col)], 0, 56, 56, align="center", bold=True)


def scroll(cr, t, lines, x, y, s, size=40, gap=62, w=600, h=None, seed=90):
    """A parchment quote; `lines` = [(runs, start_time)], each line writes on at its time."""
    h = h or 80 + gap * len(lines)
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-w / 2, -h / 2, w, h, 14, 14), PARCH, seed=seed, amp=0.6, lw=5)
        for sx in (-1, 1):
            blob(cr, sx * w / 2, 0, 24, h / 2 + 6, hexc("#d9c08a"), seed=seed + 1 + sx, amp=0.5, lw=4)
        top = -h / 2 + 40 + size * 0.4
        for k, (runs, st) in enumerate(lines):
            if t >= st:
                write(cr, runs, 0, top + k * gap, size, align="center", bold=True,
                      progress=ease_out(seg(t, st, st + 0.4)))


def buttons(cr, t, start, labels, y=1060, s=0.7):
    """Two answer buttons for the comment question, e.g. (("LOVED", GREEN), ("FEARED", RED))."""
    if t < start:
        return
    for k, (lab, col) in enumerate(labels):
        x = 220 if k == 0 else 500
        with at(cr, x, y, max(0.6, pop(t, start + k * 0.12, 0.25)) * s):
            w = max(220, 30 * len(lab) + 60)
            shape(cr, rrect_pts(-w / 2, -46, w, 92, 46, 14), col, seed=900 + k, amp=0.3, lw=4)
            write(cr, [(lab, WHITE)], 0, 16, 44, align="center", bold=True)


def tag(cr, t, start, x, y, text, col, s=0.8, seed=60):
    """A small dark label (a year, a name, a number) that pops in at `start`."""
    if t < start:
        return
    with at(cr, x, y, max(0.6, pop(t, start, 0.25)) * s):
        w = 26 * len(text) + 60
        shape(cr, rrect_pts(-w / 2, -40, w, 80, 24, 12), hexc("#2b2d3a"), seed=seed, amp=0.3, lw=0, stroke=None)
        write(cr, [(text, col)], 0, 14, 44, align="center", bold=True)


def head_c(who, x, y, s=1.0):
    """Centre of a character's head, for hats and helmets drawn on top of `person`."""
    from .characters import CAST
    c = CAST[who]
    return x, y - (14 + c["bh"] + c["head"]) * s


def talk(tl, who, t, idle="smile"):
    """Mouth for `person`: flaps while `who` is speaking."""
    return ("o" if int(t * 12) % 2 else idle) if tl.speaking(who, t) else idle


def helmet(cr, who, x, y, s=1.0, crest=RED, facing=1, metal=hexc("#c9a04a")):
    """An ancient Greek bronze helmet with a horsehair crest, over a character's head (eyes and face stay visible)."""
    import math
    from .characters import CAST
    hr = CAST[who]["head"]
    hx, hy = head_c(who, x, y, s)
    brow = -hr * 0.42                # the helmet's rim sits just above the eyes
    with at(cr, hx, hy, s, flip=facing < 0):
        shape(cr, [(-hr * 1.1 + k * hr * 0.22, -hr - 24 - 10 * math.sin(k / 10 * math.pi)) for k in range(11)] +
              [(hr * 1.1, -hr + 4), (-hr * 1.1, -hr + 4)], crest, seed=700, amp=0.6, lw=3.5)
        dome = [((hr + 8) * math.cos(a), brow + (hr * 0.62 + 8) * math.sin(a)) for a in
                [math.pi + k * math.pi / 14 for k in range(15)]]
        shape(cr, dome + [(-hr * 0.7, brow), (-hr * 0.85, hr * 0.55), (-hr - 6, hr * 0.4)], metal, seed=701, amp=0.4,
              lw=4)
        line(cr, [(-hr - 6, brow), (hr + 8, brow)], 4, hexc("#8a6a2a"), seed=702, amp=0.2)
