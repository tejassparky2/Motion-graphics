"""Shared pieces for the "researchers found / clever words from history" videos: a close camera, title cards,
quote scrolls and the two answer buttons at the end. Coordinates are world units; the camera puts its focus point
at the centre of the 720x1280 frame, so screen y = 640 + zoom * (world y - focus y)."""
from .engine import INK, WHITE, at, blob, ease_out, hexc, pop, rrect_pts, seg, shape, write
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
