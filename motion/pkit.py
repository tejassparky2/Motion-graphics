"""Shared on-screen pieces for the polished paradox videos: logic path cards, buttons, bubbles, marks and backdrops.

Everything bounces in at a `start` time (keyed to a spoken word) and is drawn in screen space unless noted.
"""
import math
import random

from .engine import W, H, cairo, clamp01, cue, ease_out, hexc, seg
from .polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, lin, paint, rad, rrect, shade, smooth,
                     soft_disc, soft_rrect, stroke_line, text_width)

RED = hexc("#e8473f")
GOLD = hexc("#ffcf3f")
BLUE = hexc("#4aa3f0")
GREEN = hexc("#3fbf6a")
PURPLE = hexc("#7a5bd0")
PINK = hexc("#ff6fa5")
INKC = hexc("#2b1d16")


def studio(cr, t, top, bottom, seed=1, n=14):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, top), (1, bottom)]))
    cr.fill()
    bokeh(cr, t, seed, n, [WHITE, hexc("#ffe7a8")], rmin=20, rmax=70)


def _pop(t, start, end=None, dur=0.35):
    if t < start or (end is not None and t > end + 0.2):
        return 0.0
    k = appear(t, start, dur)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    return k


def red_x(cr, t, start, x, y, r=40):
    if t < start:
        return
    k = appear(t, start, 0.25)
    cue("hit", t, start)
    for d in (-1, 1):
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 17, OUTLINE, curve=False)
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 10, RED, curve=False)


def check(cr, t, start, x, y, r=36):
    if t < start:
        return
    k = appear(t, start, 0.3)
    cue("pop", t, start)
    pts = [(x - r * k, y), (x - r * 0.3 * k, y + r * 0.7 * k), (x + r * k, y - r * 0.8 * k)]
    stroke_line(cr, pts, 17, OUTLINE, curve=False)
    stroke_line(cr, pts, 10, GREEN, curve=False)


def sparkles(cr, t, start, x, y, n=6, seed=2, col=WHITE, spread=90):
    if t < start or t > start + 1.2:
        return
    u = seg(t, start, start + 1.2)
    rng = random.Random(seed)
    for k in range(n):
        a = rng.random() * 6.28
        d = spread * ease_out(u) * (0.6 + 0.4 * rng.random())
        sx, sy = x + math.cos(a) * d, y + math.sin(a) * d
        r = 14 * (1 - u)
        cr.move_to(sx, sy - r)
        for j in range(1, 8):
            rr = r if j % 2 == 0 else r * 0.35
            aa = j * math.pi / 4 - math.pi / 2
            cr.line_to(sx + math.cos(aa) * rr, sy + math.sin(aa) * rr)
        cr.close_path()
        paint(cr, col, OUTLINE, 2.5)


def tag(cr, t, start, x, y, text, col=GOLD, size=40, end=None):
    k = _pop(t, start, end, 0.3)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 4) * 4)
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, col)
    cr.move_to(-12, 12)
    cr.line_to(12, 12)
    cr.line_to(0, 30)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    cr.restore()


def bubble(cr, t, start, x, y, text, col=WHITE, size=40, tail=-1, end=None, tcol=INKC, maxw=600):
    """A speech bubble that pops in at `start`; `tail` -1/1 points the tail left/right, 0 for none."""
    k = _pop(t, start, end)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    w = text_width(cr, text, size) + 56
    if w > maxw:
        size *= maxw / w
        w = maxw
    h = size * 1.7
    soft_rrect(cr, -w / 2, -h / 2 + 8, w, h, h / 2, (0, 0, 0, 0.3), sigma=8)
    if tail:
        cr.move_to(tail * w * 0.12, h / 2 - 4)
        cr.line_to(tail * w * 0.32, h / 2 + 36)
        cr.line_to(tail * w * 0.0, h / 2 - 4)
        cr.close_path()
        paint(cr, col, OUTLINE, 5)
    rrect(cr, -w / 2, -h / 2, w, h, h / 2)
    paint(cr, col, OUTLINE, 5)
    bold_text(cr, text, 0, size * 0.36, size, tcol, outline=None, shadow=0)
    cr.restore()


def card(cr, t, start, x, y, w, h, title, lines=(), col=BLUE, end=None, rot=0.0, title_size=40, line_size=40,
         mark=None, mark_at=None):
    """A white card with a coloured header (title) and up to a few text lines; optional ✔/✘ `mark` at `mark_at`."""
    k = _pop(t, start, end, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    soft_rrect(cr, -w / 2, -h / 2 + 12, w, h, 26, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -w / 2, -h / 2, w, h, 26)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    cr.save()
    rrect(cr, -w / 2, -h / 2, w, h, 26)
    cr.clip()
    cr.rectangle(-w / 2, -h / 2, w, title_size * 1.7)
    cr.set_source(lin(0, -h / 2, 0, -h / 2 + title_size * 1.7, [(0, shade(col, 0.3)), (1, col)]))
    cr.fill()
    cr.restore()
    bold_text(cr, title, 0, -h / 2 + title_size * 1.22, title_size, WHITE, ow=6)
    y0 = -h / 2 + title_size * 1.7 + line_size * 1.3
    for ln in lines:
        tw = text_width(cr, ln, line_size, "Fredoka")
        sz = line_size * min(1.0, (w - 40) / max(tw, 1))
        bold_text(cr, ln, 0, y0, sz, INKC, font="Fredoka", outline=None, shadow=0)
        y0 += line_size * 1.25
    cr.restore()
    if mark and mark_at is not None:
        mx, my = x + w / 2 - 20, y - h / 2 + 10
        (check if mark == "ok" else red_x)(cr, t, mark_at, mx, my, 34)


def buttons(cr, t, start, labels, y=380, size=44, w=260):
    """Answer buttons [(label, colour, start_offset_key_time or None)] spread across the width."""
    n = len(labels)
    for k, (lab, col) in enumerate(labels):
        x = W * (2 * k + 1) / (2 * n)
        kk = appear(t, start + k * 0.12) if t >= start + k * 0.12 else 0
        if kk <= 0.01:
            continue
        bw = min(w, W / n - 24)
        cr.save()
        cr.translate(x, y)
        cr.scale(kk, kk)
        soft_rrect(cr, -bw / 2, -42, bw, 92, 46, (0, 0, 0, 0.3), sigma=10)
        rrect(cr, -bw / 2, -50, bw, 92, 46)
        paint(cr, lin(0, -50, 0, 42, [(0, shade(col, 0.3)), (1, shade(col, -0.15))]), OUTLINE, 6)
        tw = text_width(cr, lab, size)
        bold_text(cr, lab, 0, 14, size * min(1.0, (bw - 30) / max(tw, 1)), WHITE)
        cr.restore()
    cue("pop", t, start)


def knot(cr, t, start, x, y, r=110, col=RED, label=None):
    """Two arrows chasing each other in a circle: 'this loops forever'."""
    k = _pop(t, start)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.rotate(t * 2.2)
    for j in range(2):
        a0 = j * math.pi
        for lw, c in ((22, OUTLINE), (13, col)):
            cr.new_path()
            cr.arc(0, 0, r, a0 + 0.25, a0 + math.pi - 0.35)
            cr.set_line_width(lw)
            cr.set_source_rgba(*c)
            cr.stroke()
        a = a0 + math.pi - 0.35
        hx, hy = math.cos(a) * r, math.sin(a) * r
        tx, ty = -math.sin(a), math.cos(a)
        nx, ny = math.cos(a), math.sin(a)
        cr.move_to(hx + tx * 34, hy + ty * 34)
        cr.line_to(hx + nx * 28, hy + ny * 28)
        cr.line_to(hx - nx * 28, hy - ny * 28)
        cr.close_path()
        paint(cr, col, OUTLINE, 4)
    cr.restore()
    if label:
        bold_text(cr, label, x, y + 16, 46, WHITE)


def calendar(cr, t, start, x, y, top, big, col=RED, s=1.0, end=None):
    k = _pop(t, start, end, 0.4)
    if k <= 0.01:
        return
    cue("pop", t, start)
    cr.save()
    cr.translate(x, y + math.sin(t * 2) * 3)
    cr.rotate(0.04 * math.sin(t * 1.6))
    cr.scale(k * s, k * s)
    soft_rrect(cr, -120, -76, 240, 200, 22, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -120, -86, 240, 200, 22)
    paint(cr, lin(0, -86, 0, 114, [(0, WHITE), (1, hexc("#e9e2d6"))]), OUTLINE, 6)
    cr.save()
    rrect(cr, -120, -86, 240, 200, 22)
    cr.clip()
    cr.rectangle(-120, -86, 240, 58)
    cr.set_source(lin(0, -86, 0, -28, [(0, shade(col, 0.2)), (1, col)]))
    cr.fill()
    cr.restore()
    bold_text(cr, top, 0, -42, 30, WHITE)
    tw = text_width(cr, big, 80)
    bold_text(cr, big, 0, 72, 80 * min(1.0, 210 / max(tw, 1)), INKC, outline=None, shadow=0)
    cr.restore()


def hanzi(cr, t, start, x, y, ch, size=170, col=RED, sub=None, end=None):
    """A big Chinese character on a square tile (WenQuanYi Zen Hei), with an optional pinyin label."""
    k = _pop(t, start, end, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    soft_rrect(cr, -size * 0.62, -size * 0.6, size * 1.24, size * 1.24, 24, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -size * 0.62, -size * 0.66, size * 1.24, size * 1.24, 24)
    paint(cr, lin(0, -size * 0.66, 0, size * 0.6, [(0, WHITE), (1, hexc("#f1e6d2"))]), OUTLINE, 6)
    cr.select_font_face("WenQuanYi Zen Hei", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    e = cr.text_extents(ch)
    cr.move_to(-e.x_advance / 2, size * 0.36)
    cr.text_path(ch)
    cr.set_source_rgba(*col)
    cr.fill()
    cr.restore()
    if sub:
        bold_text(cr, sub, x, y + size * 0.85, 44 * k, WHITE, font="Fredoka")


def shake(t, start, dur=0.4, amp=10):
    """A camera-shake offset (dx, dy) for `dur` seconds after `start`."""
    if not (start <= t < start + dur):
        return 0.0, 0.0
    u = 1 - (t - start) / dur
    return math.sin(t * 90) * amp * u, math.cos(t * 77) * amp * u
