"""Brand for "Interestingly Strange": the mascot and the wordmark.

The mascot is a one-eyed creature whose curled antenna and round body together read as a question mark
(the hook on top, the body as the dot). One raised eyebrow gives it the "hm, that's odd" expression.
Everything is drawn with the same hand-drawn helpers as the videos, so the mascot can be animated too.
"""
import math

from .engine import INK, at, blob, cairo, dot, hexc, line, shape, write

PURPLE = hexc("#8a63d2")
PURPLE_D = hexc("#6a45b5")
YELLOW = hexc("#ffd23f")
ORANGE = hexc("#ff8a3d")
PINK = hexc("#ff7a8a", 0.55)
WHITE = hexc("#fffdf7")
CREAM = hexc("#f6ecd2")


def mascot(cr, x, y, s=1.0, t=0.0, look=(0.35, -0.3), blink=False):
    """Mascot centred on its body at (x, y); body radius ~95*s. `look` shifts the pupil (-1..1)."""
    with at(cr, x, y, s):
        # antenna: a question-mark hook rising from the head
        hook = [(4, -80), (2, -112), (8, -138), (30, -160), (34, -188), (14, -210), (-14, -208), (-32, -190)]
        wob = math.sin(t * 3) * 3
        hook = [(px + wob * (i / len(hook)), py) for i, (px, py) in enumerate(hook)]
        line(cr, hook, 26, INK, seed=1, amp=0.5)
        line(cr, hook, 14, PURPLE, seed=1, amp=0.5)
        blob(cr, hook[-1][0] - 4, hook[-1][1] + 6, 13, 13, ORANGE, seed=2, amp=0.4, lw=6)
        # feet
        for fx in (-42, 42):
            blob(cr, fx, 92, 26, 14, PURPLE_D, seed=3 + fx, amp=0.5, lw=7)
        # body
        blob(cr, 0, 6, 98, 94, PURPLE, seed=5, amp=0.8, lw=9, n=28)
        blob(cr, 0, 42, 58, 34, hexc("#a585e6"), seed=6, amp=0.6, lw=0, stroke=None)  # belly highlight
        # little arms
        line(cr, [(-92, 20), (-112, 40), (-110, 58)], 14, INK, seed=7, amp=0.3)
        line(cr, [(-92, 20), (-112, 40), (-110, 58)], 6, PURPLE, seed=7, amp=0.3)
        line(cr, [(92, 18), (114, 2), (122, -18)], 14, INK, seed=8, amp=0.3)
        line(cr, [(92, 18), (114, 2), (122, -18)], 6, PURPLE, seed=8, amp=0.3)
        # the big eye
        ex, ey = 0, 4
        if blink:
            line(cr, [(ex - 38, ey + 4), (ex, ey + 14), (ex + 38, ey + 4)], 8, INK, seed=9, amp=0.3)
        else:
            blob(cr, ex, ey, 42, 42, WHITE, seed=9, amp=0.5, lw=8)
            px, py = ex + look[0] * 18, ey + look[1] * 18
            dot(cr, px, py, 21, INK)
            dot(cr, px + 7, py - 8, 7, WHITE)
        # one raised eyebrow = "hm, interesting..."
        line(cr, [(ex - 30, ey - 54), (ex + 4, ey - 70), (ex + 36, ey - 62)], 9, INK, seed=10, amp=0.3)
        # cheeks + small curious mouth
        dot(cr, -60, 42, 12, PINK)
        dot(cr, 60, 42, 12, PINK)
        line(cr, [(-12, 64), (2, 70), (16, 62)], 7, INK, seed=11, amp=0.3)


def sparkle(cr, x, y, r, color=WHITE, seed=0):
    pts = []
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.32
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    shape(cr, pts, color, seed=seed, amp=0.3, lw=5, closed=True)


def _letters(cr, text, x, y, size, fill, stroke, lw, rot=0.0, bounce=0.0, spacing=0.0, bold=True, seed=0):
    """Draw text letter by letter (outlined), with optional hand-made wobble in angle and baseline."""
    import random
    r = random.Random(seed)
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    widths = [cr.text_extents(ch).x_advance for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    cx = x - total / 2
    for ch, w in zip(text, widths):
        cr.save()
        cr.translate(cx + w / 2, y + r.uniform(-bounce, bounce))
        cr.rotate(r.uniform(-rot, rot))
        cr.move_to(-w / 2, 0)
        cr.text_path(ch)
        if stroke is not None:
            cr.set_source_rgba(*stroke)
            cr.set_line_width(lw)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke_preserve()
        cr.set_source_rgba(*fill)
        cr.fill()
        cr.restore()
        cx += w + spacing
    return total


def wordmark(cr, x, y, scale=1.0, dark=False):
    """Stacked wordmark centred at x; y is the baseline of STRANGE."""
    top = CREAM if dark else INK
    with at(cr, x, y, scale):
        _letters(cr, "INTERESTINGLY", 0, -150, 64, top, None, 0, spacing=7, seed=1)
        _letters(cr, "STRANGE", 0, 0, 170, PURPLE, INK if not dark else hexc("#120f18"), 18, rot=0.09, bounce=9,
                 spacing=4, seed=7)
