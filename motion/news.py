"""Pieces for the news & tech channel: talking country flags, a date stamp, a source tag, price tags, pop-in panels
and simple drawn props (crowd, passport, phone, dinner plate). Everything is drawn by us; flags are plain geometric
national flags, no logos, photos or footage.

Panels and tags are drawn in screen space (call after the world is drawn); `country` is drawn in world space."""
import math

from .characters import _eyes, _mouth
from .engine import INK, WHITE, at, blob, cairo, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write

PAPER = hexc("#f3ead6")
SKY = hexc("#cfe6f2")
NAVY = hexc("#2b2d3a")
JP_RED = hexc("#bc002d")
GREEN = hexc("#2e9e52")
GOLD = hexc("#f2b632")
TEAL = hexc("#2e9e8f")


# ---------------------------------------------------------------- flags
def _wave_pts(x0, y0, w, h, t, amp=7.0, n=14):
    """Outline of a flag waving from its pole edge (x0): the free end moves most."""
    def dy(u):
        return amp * u * math.sin(t * 5.0 - u * 5.5)
    top = [(x0 + w * k / n, y0 + dy(k / n)) for k in range(n + 1)]
    bot = [(x0 + w * k / n, y0 + h + dy(k / n)) for k in range(n, -1, -1)]
    return top + bot, dy


def _flag_jp(cr, x0, y0, w, h, t, seed):
    pts, dy = _wave_pts(x0, y0, w, h, t)
    shape(cr, pts, WHITE, seed=seed, amp=0.5, lw=4.5)
    cx, cy = x0 + w / 2, y0 + h / 2 + dy(0.5)
    blob(cr, cx, cy, h * 0.3, h * 0.3, JP_RED, seed=seed + 1, amp=0.5, lw=0, stroke=None)
    return cx, cy


FLAGS = {"jp": _flag_jp}


def country(cr, code, pole_x, ground_y, t, s=1.0, eyes="dot", mouth="smile", look=-1, bounce=0.0, seed=7000):
    """A national flag on a pole that talks: face on the flag's centre. `look` = -1 faces left, 1 right."""
    w, h = 250, 160
    with at(cr, pole_x, ground_y - bounce, s):
        line(cr, [(0, 0), (0, -370)], 9, INK, seed, amp=0.2)
        line(cr, [(0, 0), (0, -370)], 4, hexc("#a9a2ae"), seed, amp=0.2)
        blob(cr, 0, -376, 9, 9, GOLD, seed + 1, amp=0.3, lw=3)
        blob(cr, 0, -4, 34, 10, hexc("#8e8a80"), seed + 2, amp=0.4, lw=3.5)
        cx, cy = FLAGS[code](cr, 0, -360, w, h, t, seed + 3)
        with at(cr, cx + look * 8, cy, 1.55):   # a big, readable face on the flag's centre
            if eyes in ("dot", "wide", "sly"):
                for sx in (-1, 1):
                    blob(cr, sx * 15, -8, 11, 12, WHITE, seed + 20 + sx, amp=0.4, lw=2.5)
            _eyes(cr, eyes, 0, -8, t, seed + 9)
            _mouth(cr, mouth, 0, 16, seed + 10, t)
    return pole_x + cx * s, ground_y + cy * s


# ---------------------------------------------------------------- screen-space overlays
def _screen(cr):
    cr.save()
    cr.identity_matrix()


def panel(cr, t, start, end, x, y, w, h, draw_fn, seed=7100, fill=PAPER):
    """A pop-in card centred on (x, y) in screen space; `draw_fn(cr)` draws its content around (0, 0)."""
    if not (start <= t < end):
        return
    sc = pop(t, start, 0.22) * (1 - 0.2 * seg(t, end - 0.12, end))
    if sc <= 0:
        return
    _screen(cr)
    with at(cr, x, y, sc):
        shape(cr, rrect_pts(-w / 2, -h / 2, w, h, 24, 18), fill, seed=seed, amp=0.7, lw=5)
        draw_fn(cr)
    cr.restore()


def date_stamp(cr, t, start, text, x=150, y=150):
    """A red rubber stamp with the date the facts are true for."""
    if t < start:
        return
    _screen(cr)
    with at(cr, x, y, max(0.7, pop(t, start, 0.25)), rot=-0.08):
        shape(cr, rrect_pts(-108, -34, 216, 68, 10, 14), hexc("#fbf3e1", 0.9), seed=7200, amp=0.4, lw=4.5,
              stroke=RED_STAMP)
        write(cr, [(text, RED_STAMP)], 0, 14, 36, align="center", bold=True)
    cr.restore()


RED_STAMP = hexc("#c8303a")


def source_tag(cr, t, start, text, end=None, y=268):
    """Small dark pill under the headline: where the number comes from."""
    if t < start or (end is not None and t >= end):
        return
    _screen(cr)
    a = ease_out(seg(t, start, start + 0.25))
    cr.push_group()
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(24)
    label = "Source: " + text
    half = cr.text_extents(label).x_advance / 2 + 22
    shape(cr, rrect_pts(360 - half, y - 24, half * 2, 46, 22, 12), hexc("#2b2d3a", 0.88), seed=7300, amp=0.2, lw=0,
          stroke=None)
    write(cr, [(label, hexc("#fbf3e1"))], 360, y + 8, 24, align="center", bold=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def price_tag(cr, x, y, top, bottom, col=INK, s=1.0, crossed=0.0, seed=7400, rot=-0.05):
    """A hanging price tag (draw inside a panel or in screen space). `crossed` 0..1 strikes it through."""
    with at(cr, x, y, s, rot=rot):
        pts = [(-120, -60), (90, -60), (130, 0), (90, 60), (-120, 60)]
        shape(cr, pts, WHITE, seed=seed, amp=0.6, lw=4.5)
        blob(cr, 96, 0, 8, 8, PAPER, seed + 1, amp=0.2, lw=3)
        write(cr, [(top, col)], -14, 6, 50, align="center", bold=True)
        write(cr, [(bottom, INK)], -14, 46, 26, align="center")
        if crossed > 0:
            line(cr, [(-130, 30), (-130 + 260 * crossed, -30 + 0 * crossed)], 8, RED_STAMP, seed + 2, amp=0.4)


# ---------------------------------------------------------------- props (draw around (0, 0))
def crowd(cr, x, y, t, n, cols=10, gap=22, progress=1.0, seed=7500):
    """Little round people filling in row by row."""
    palette = [hexc(c) for c in ("#e0487a", "#3f6fb5", "#2e9e52", "#f2b632", "#8a63d2", "#e8743b", "#2e9e8f")]
    shown = int(n * progress)
    rows = (n + cols - 1) // cols
    for k in range(shown):
        r, c = divmod(k, cols)
        px = x + (c - (cols - 1) / 2) * gap
        py = y + (r - (rows - 1) / 2) * gap * 1.25 + math.sin(t * 6 + k) * 1.2
        dot(cr, px, py - 7, 6.5, INK)
        dot(cr, px, py - 7, 4.5, hexc("#f0c29c"))
        blob(cr, px, py + 5, 7.5, 6, palette[(k * 5 + seed) % len(palette)], seed + k, amp=0.3, lw=2)


def passport(cr, x, y, s=1.0, cover=hexc("#8e1b2e"), seed=7600):
    """A generic passport: no real national design."""
    with at(cr, x, y, s, rot=0.06):
        shape(cr, rrect_pts(-62, -86, 124, 172, 10, 14), cover, seed=seed, amp=0.4, lw=4)
        blob(cr, 0, -6, 30, 30, None, seed + 1, amp=0.3, lw=3, stroke=GOLD)
        line(cr, [(-30, -6), (30, -6)], 2.5, GOLD, seed + 2, amp=0.2)
        line(cr, [(0, -36), (0, 24)], 2.5, GOLD, seed + 3, amp=0.2)
        write(cr, [("PASSPORT", GOLD)], 0, 62, 22, align="center", bold=True)


def phone(cr, x, y, s=1.0, seed=7700):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-46, -86, 92, 172, 16, 14), NAVY, seed=seed, amp=0.4, lw=4)
        shape(cr, rrect_pts(-38, -72, 76, 140, 8, 14), hexc("#7fc8e8"), seed=seed + 1, amp=0.3, lw=0, stroke=None)
        dot(cr, 0, -79, 3.5, hexc("#a9a2ae"))


def dinner(cr, x, y, s=1.0, seed=7800):
    """A bowl of ramen-style noodles (any nice meal)."""
    with at(cr, x, y, s):
        blob(cr, 0, 6, 80, 16, hexc("#e9e2d0"), seed, amp=0.4, lw=4)
        shape(cr, [(-70, -8), (70, -8), (52, 46), (-52, 46)], hexc("#d8363a"), seed=seed + 1, amp=0.5, lw=4)
        blob(cr, 0, -8, 70, 14, hexc("#f2d38b"), seed + 2, amp=0.6, lw=3.5)
        for k in (-30, -6, 18):
            line(cr, [(k, -14), (k + 8, -6), (k + 2, 2)], 3, hexc("#c99a3a"), seed + 3 + k, amp=0.4)
        line(cr, [(20, -18), (84, -84)], 5, hexc("#8e5a2e"), seed + 4, amp=0.2)
        line(cr, [(32, -14), (96, -76)], 5, hexc("#8e5a2e"), seed + 5, amp=0.2)


def big_x(cr, x, y, r, progress=1.0, seed=7900):
    u = ease_out(progress)
    line(cr, [(x - r, y - r), (x - r + 2 * r * u, y - r + 2 * r * u)], 14, RED_STAMP, seed, amp=0.4)
    if u > 0.5:
        v = (u - 0.5) * 2
        line(cr, [(x + r, y - r), (x + r - 2 * r * v, y - r + 2 * r * v)], 14, RED_STAMP, seed + 1, amp=0.4)


def tick(cr, x, y, r, col=GREEN, seed=7950):
    line(cr, [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)], 10, col, seed, amp=0.3)
