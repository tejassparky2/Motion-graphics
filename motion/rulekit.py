"""Shared pieces for the genie-style stories (one character with ONE rule, a kid who turns it against itself):
the big quoted note, turning a character to stone, and the two "either way" logic cards.
"""
import math

from .engine import cue, hexc
from .pkit import GOLD, INKC, card, knot
from .polish import OUTLINE, alpha, appear, bold_text, lin, paint, rrect, sign


def note(cr, t, start, x, y, lines, hot=0, w=420, size=60, rot=0.04, col=hexc("#e8473f")):
    """A cream paper note with a quoted line (one string per row) that pops in at `start`; row `hot` is red."""
    k = appear(t, start, 0.4)
    if k <= 0.01:
        return
    h = size * 1.18 * len(lines) + 70
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    rrect(cr, -w / 2, -h / 2, w, h, 28)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, hexc("#fff8e6")), (1, hexc("#f4e4c4"))]), OUTLINE, 6)
    y0 = -h / 2 + 35 + size * 0.95
    for j, ln in enumerate(lines):
        bold_text(cr, ln, 0, y0 + j * size * 1.18, size, col if j == hot else INKC, outline=None, shadow=0)
    cr.restore()
    cue("pop", t, start)


def stone(cr, draw, g):
    """Draw with `draw(cr)` and turn it to grey stone by `g` (0..1)."""
    cr.push_group()
    draw(cr)
    pat = cr.pop_group()
    cr.set_source(pat)
    cr.paint()
    if g > 0:
        cr.set_source_rgba(0.62, 0.64, 0.68, 0.85 * g)
        cr.mask(pat)


def either_way(cr, t, tl, a, b, c, left, right, tag_text, col, left_mark, right_mark, figure=None):
    """Beats a / b: two cards (title, lines, colour) with a ✘ each; beat c: the knot and `tag_text`.
    `left_mark` / `right_mark` are (beat, word) keys for the ✘. `figure(cr, t, spinning)` draws the stuck character."""
    A = tl.at
    ta, tb, tc = A(a), A(b), A(c)
    if t < tc:
        card(cr, t, ta, 185, 330, 330, 300, left[0], left[1], col=left[2], mark="no", mark_at=A(*left_mark),
             line_size=36)
        card(cr, t, tb, 535, 330, 330, 300, right[0], right[1], col=right[2], mark="no", mark_at=A(*right_mark),
             line_size=36)
        if t >= tb:
            bold_text(cr, "OR", 360, 560, 60 * appear(t, tb, 0.3), GOLD)
        if figure:
            figure(cr, t, False)
    else:
        knot(cr, t, tc, 360, 380, 150, col)
        if figure:
            figure(cr, t, True)
        sign(cr, t, tc + 0.5, 360, 140, tag_text, col=hexc("#e8473f"), size=64)


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


def zzz(cr, t, x, y, s=1.0):
    """Floating Z's for someone asleep."""
    for k in range(3):
        u = ((t * 0.7 + k / 3) % 1.0)
        bold_text(cr, "Z", x + u * 60 * s + k * 6, y - u * 120 * s, (26 + 20 * k) * s, alpha((1, 1, 1, 1), 1 - u))
