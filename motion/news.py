"""Pieces for the news & tech channel: the talking globe (painted in each story's flag colours), a date stamp,
a source tag, price tags, pop-in panels and simple drawn props (crowd, passport, phone, dinner plate). Everything is drawn by us: no logos, photos or footage.

Panels and tags are drawn in screen space (call after the world is drawn); `globe` is drawn in world space."""
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


# ---------------------------------------------------------------- the talking globe
# The channel's recurring character: a desk globe with a face. For each story it is painted in that country's flag
# colours (sea, land, stand ring), so viewers see whose story it is without us drawing anyone's flag as a character.
# For a company story it wears that company's brand colours plus a badge with our own simple drawing of the
# company's mark (owner's request, 5 Oct 2026), never a copied logo file.
PALETTES = {
    "jp": dict(sea=hexc("#fbf8ef"), land=hexc("#bc002d"), ring=hexc("#bc002d"), lines=hexc("#e9b8c0")),
    # companies: the globe in the company's brand colours (never its logo). Apple: silver and graphite.
    # Apple: the whole globe in the mark's graphite, the apple big and white on one side, the name on the base.
    "apple": dict(sea=hexc("#2b2d33"), land=hexc("#3b3e46"), ring=hexc("#c9ccd2"), lines=hexc("#44474f"),
                  emblem="apple", emblem_col=hexc("#f5f5f7"), name="APPLE"),
    "world": dict(sea=hexc("#5fa8d8"), land=hexc("#5cb85c"), ring=hexc("#c9a227"), lines=hexc("#9fd0ee")),
}
_LAND = [(-0.45, -0.28, 0.48, 0.34, 1), (0.02, 0.4, 0.3, 0.4, 2), (0.55, -0.22, 0.4, 0.46, 3),
         (-0.9, 0.48, 0.22, 0.2, 4), (0.95, 0.5, 0.2, 0.14, 5)]


def _continent(cx, cy, rx, ry, k, n=18):
    """A lumpy landmass outline (fixed shape per k)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        f = 1 + 0.22 * math.sin(3 * a + k * 1.7) + 0.14 * math.sin(5 * a + k * 2.9) + 0.08 * math.sin(7 * a + k)
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return pts


def _apple_mark(cr, x, y, s, seed, col=None):
    """Our own hand-drawn apple with a bite and a leaf (a simple shape that says "Apple", not the official logo)."""
    body = [(0, -17), (8, -21), (17, -22), (24, -18), (27, -12),
            (24, -8), (21, -4), (20, 0), (21, 4), (24, 8),            # the bite
            (27, 13), (24, 20), (18, 27), (11, 30), (5, 29), (0, 27), (-5, 29), (-11, 30), (-18, 27),
            (-24, 20), (-28, 10), (-29, 0), (-28, -10), (-24, -18), (-17, -22), (-8, -21)]
    leaf = [(1, -24), (3, -33), (12, -39), (10, -30)]
    with at(cr, x, y, s):
        col = col or hexc("#1d1d1f")
        shape(cr, body, col, seed=seed, amp=0.25, lw=0, stroke=None)
        shape(cr, leaf, col, seed=seed + 1, amp=0.15, lw=0, stroke=None)


EMBLEMS = {"apple": _apple_mark}


def globe(cr, code, x, ground_y, t, s=1.0, eyes="dot", mouth="smile", look=-1, bounce=0.0, spin=0.12, seed=7000):
    """A talking desk globe standing on the floor at (x, ground_y), coloured for `code` (see PALETTES)."""
    p = PALETTES[code]
    r = 128
    cy = -r - 120
    with at(cr, x, ground_y - bounce, s):
        # stand: base, post and the half-ring meridian
        blob(cr, 0, -10, 70, 16, hexc("#8e5a2e"), seed, amp=0.4, lw=4)
        line(cr, [(0, -14), (0, cy + r + 14)], 12, INK, seed + 1, amp=0.2)
        line(cr, [(0, -14), (0, cy + r + 14)], 6, hexc("#b07a45"), seed + 1, amp=0.2)
        if p.get("name"):   # a name plate on the base
            shape(cr, rrect_pts(-92, -54, 184, 46, 12, 14), p["ring"], seed=seed + 60, amp=0.4, lw=4)
            write(cr, [(p["name"], INK)], 0, -20, 34, align="center", bold=True)
        # sphere, tilted a little like a real desk globe
        with at(cr, 0, cy, 1.0, rot=-0.18):
            blob(cr, 0, 0, r, r, p["sea"], seed + 2, amp=0.6, lw=5)
            cr.save()
            cr.arc(0, 0, r - 3, 0, 2 * math.pi)
            cr.clip()
            off = (t * spin) % 2.4 - 1.2
            for lx, ly, rx, ry, k in _LAND:
                for wrap in (0.0, -2.4, 2.4):
                    u = lx + off + wrap
                    if -1.6 < u < 1.6:
                        sq = max(0.3, math.cos(min(1.5, abs(u)) * math.pi / 3.2))   # land squashes near the edge
                        shape(cr, _continent(u * r, ly * r, rx * r * sq, ry * r, k), p["land"], seed=seed + 10 + k,
                              amp=0.8, lw=3, stroke=hexc("#2a2230", 0.55))
            for k in (-2, -1, 0, 1, 2):
                line(cr, [(-r, k * r * 0.36), (r, k * r * 0.36)], 2.5, p["lines"], seed + 30 + k, amp=0.3)
            if p.get("emblem_col"):   # the company's mark, big, on one side of the globe (our own drawing)
                EMBLEMS[p["emblem"]](cr, -look * 58, 4, 1.6, seed + 51, p["emblem_col"])
            cr.restore()
            blob(cr, 0, 0, r, r, None, seed + 2, amp=0.6, lw=5)
        # meridian ring in the flag's second colour
        cr.save()
        cr.new_path()
        cr.arc(0, cy, r + 18, math.pi * 0.62, math.pi * 1.38)
        cr.set_line_width(15)
        cr.set_source_rgba(*INK)
        cr.stroke()
        cr.arc(0, cy, r + 18, math.pi * 0.62, math.pi * 1.38)
        cr.set_line_width(8)
        cr.set_source_rgba(*p["ring"])
        cr.stroke()
        cr.restore()
        if p.get("emblem") and not p.get("emblem_col"):   # or as a small badge, hand-drawn by us
            with at(cr, -look * 56, cy - 76, 1.0):
                blob(cr, 0, 0, 46, 46, WHITE, seed + 50, amp=0.4, lw=4)
                EMBLEMS[p["emblem"]](cr, 0, 4, 1.15, seed + 51)
        with at(cr, look * (46 if p.get("emblem_col") else 10), cy + 6, 1.7):   # the face
            for sx in (-1, 1):
                if eyes in ("dot", "wide", "sly"):
                    blob(cr, sx * 15, -8, 11, 12, WHITE, seed + 20 + sx, amp=0.4, lw=2.5)
            _eyes(cr, eyes, 0, -8, t, seed + 9)
            blob(cr, 0, 18, 17, 11, hexc("#fffdf7", 0.85), seed + 41, amp=0.4, lw=0, stroke=None)
            _mouth(cr, mouth, 0, 16, seed + 10, t)
    return x, ground_y + cy * s


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
