"""The explainer look (owner's reference reels, 24 Oct 2026): every shot sits on aged paper with fold creases, grain
and punch holes; a thin header rule with a small section label and "FIG. N"; a two-line headline (small dark line,
big red condensed word) that fills in as it's said; flat cut-out props with soft shadows. No subtitles.

A video lists its shots in SHOTS = {scene: Shot(...)} and calls frame() from draw(). All art is our own vector
drawing (Natural Earth outlines for maps are public domain).
"""
import json
import math
import os
from dataclasses import dataclass, field

import numpy as np

from .engine import FPS, H, ROOT, W, cairo, clamp01, cue, ease_out, hexc, lerp, seg, smooth, back_out

# ---------------------------------------------------------------- palette
TONES = {   # paper colour, ink, headline red, is it dark?
    "khaki": (hexc("#d8ccab"), hexc("#2b2420"), hexc("#c3332b"), False),
    "cream": (hexc("#e6dcc2"), hexc("#2b2420"), hexc("#c3332b"), False),
    "mint": (hexc("#bcd2bd"), hexc("#23302a"), hexc("#c3332b"), False),
    "teal": (hexc("#2e5a51"), hexc("#efe6d2"), hexc("#ef5a45"), True),
    "dark": (hexc("#2a2724"), hexc("#efe6d2"), hexc("#e8483a"), True),
    "night": (hexc("#1f2633"), hexc("#efe6d2"), hexc("#e8483a"), True),
    "blood": (hexc("#a4302c"), hexc("#f6ead6"), hexc("#ffd9a8"), True),
}
INK = hexc("#2b2420")
RED = hexc("#c3332b")
PAPER_HI = hexc("#efe6d2")
SHADOW = (0.12, 0.08, 0.05)

FONT_HEAD = "Anton"
FONT_MONO = "Space Mono"


# ---------------------------------------------------------------- paper background (cached per tone)
_PAPER = {}


def _paper_surface(tone):
    if tone in _PAPER:
        return _PAPER[tone]
    from scipy.ndimage import gaussian_filter, zoom
    base, _, _, dark = TONES[tone]
    rng = np.random.default_rng(11)
    mott = zoom(rng.normal(0, 1, (34, 20)), (H / 34, W / 20), order=3)[:H, :W]
    mott = gaussian_filter(mott, 18) * (0.03 if dark else 0.018)
    grain = rng.normal(0, 1, (H, W)) * (0.022 if dark else 0.018)
    fibre = gaussian_filter(rng.normal(0, 1, (H, W)), (0.6, 3)) * 0.03
    lum = 1 + mott + grain + fibre
    # fold creases: two vertical folds and one faint horizontal one (a highlight edge with a soft shadow beside it)
    xs, ys = np.arange(W)[None, :], np.arange(H)[:, None]
    for cx, k in ((W * 0.31, 1.0), (W * 0.64, 0.8)):
        d = xs - cx
        lum = lum + k * (0.055 * np.exp(-(d / 1.3) ** 2) - 0.05 * np.exp(-np.maximum(d - 1.5, 0) / 9) * (d > 1.5))
    d = ys - H * 0.53
    lum = lum + 0.4 * (0.05 * np.exp(-(d / 1.3) ** 2) - 0.045 * np.exp(-np.maximum(d - 1.5, 0) / 8) * (d > 1.5))
    # vignette
    u, v = (xs - W / 2) / (W / 2), (ys - H / 2) / (H / 2)
    lum = lum * (1 - 0.16 * np.clip(u ** 2 * 0.8 + v ** 2 * 0.6, 0, 1.4))
    rgb = np.clip(np.stack([lum * base[0], lum * base[1], lum * base[2]], -1), 0, 1)
    if not dark:   # faint ruled lines, like a notebook page
        rule = ((ys % 38) == 0) & (ys > 200)
        rgb = rgb * (1 - 0.035 * rule[..., None])
    arr = np.empty((H, W, 4), np.uint8)
    arr[..., 0] = (rgb[..., 2] * 255).astype(np.uint8)   # cairo ARGB32 is BGRA in memory
    arr[..., 1] = (rgb[..., 1] * 255).astype(np.uint8)
    arr[..., 2] = (rgb[..., 0] * 255).astype(np.uint8)
    arr[..., 3] = 255
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    np.frombuffer(s.get_data(), np.uint8).reshape(H, s.get_stride() // 4, 4)[:, :W] = arr
    s.mark_dirty()
    _PAPER[tone] = s
    return s


def paper(cr, tone):
    cr.set_source_surface(_paper_surface(tone), 0, 0)
    cr.paint()
    # punch holes down the left edge
    _, ink, _, dark = TONES[tone]
    for y in range(205, H - 60, 150):
        cr.arc(30, y, 6.5, 0, 2 * math.pi)
        cr.set_source_rgba(0, 0, 0, 0.32 if dark else 0.22)
        cr.fill()
        cr.arc(30.8, y + 1.2, 5.2, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.05 if dark else 0.16)
        cr.fill()


# ---------------------------------------------------------------- text
def font(cr, name, size):
    cr.select_font_face(name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def text(cr, s, x, y, size, col=INK, face=FONT_HEAD, align="left", spacing=0.0, alpha=1.0):
    """One line of text, baseline at y. Returns its width."""
    font(cr, face, size)
    widths = [cr.text_extents(ch).x_advance + spacing for ch in s] if spacing else None
    wd = sum(widths) - spacing if spacing else cr.text_extents(s).x_advance
    x0 = x - wd / 2 if align == "center" else x - wd if align == "right" else x
    cr.set_source_rgba(col[0], col[1], col[2], col[3] * alpha if len(col) > 3 else alpha)
    if spacing:
        cx = x0
        for ch, w in zip(s, widths):
            cr.move_to(cx, y)
            cr.show_text(ch)
            cx += w
    else:
        cr.move_to(x0, y)
        cr.show_text(s)
    return wd


def text_w(cr, s, size, face=FONT_HEAD):
    font(cr, face, size)
    return cr.text_extents(s).x_advance


def fit(cr, s, size, maxw, face=FONT_HEAD):
    """Largest size <= `size` at which `s` fits in `maxw`."""
    w = text_w(cr, s, size, face)
    return size if w <= maxw else size * maxw / w


# ---------------------------------------------------------------- header + headline
HEAD_Y = 168          # header rule
SMALL_Y = 228         # small headline baseline
BIG_Y = 330           # big headline baseline
LEFT = 64


def header(cr, tone, label, fig):
    _, ink, _, dark = TONES[tone]
    cr.set_source_rgba(ink[0], ink[1], ink[2], 0.55)
    cr.set_line_width(1.6)
    cr.move_to(LEFT, HEAD_Y)
    cr.line_to(W - LEFT, HEAD_Y)
    cr.stroke()
    text(cr, label.upper(), LEFT, HEAD_Y - 12, 15, ink, FONT_MONO, spacing=1.5, alpha=0.75)
    text(cr, f"FIG. {fig}", W - LEFT, HEAD_Y - 12, 15, ink, FONT_MONO, align="right", spacing=1.5, alpha=0.75)


def headline(cr, t, tone, small, big, t0, t_big, out=None):
    """Small line from t0; the big red line sits faded until t_big (when its word is said), then fills in."""
    _, ink, red, _ = TONES[tone]
    a = smooth(seg(t, t0, t0 + 0.2))
    if out is not None:
        a *= 1 - seg(t, out, out + 0.12)
    if a <= 0:
        return
    maxw = W - 2 * LEFT
    if small:
        sz = fit(cr, small, 54, maxw)
        text(cr, small, LEFT, SMALL_Y + 8 * (1 - a), sz, ink, alpha=a)
    if big:
        sz = fit(cr, big, 112, maxw)
        fill = seg(t, t_big, t_big + 0.16)
        s = lerp(1.06, 1.0, ease_out(fill)) if fill > 0 else 1.0
        y = BIG_Y if small else SMALL_Y + 60
        cr.save()
        cr.translate(LEFT, y)
        cr.scale(s, s)
        text(cr, big, 0, 0, sz, red, alpha=a * lerp(0.22, 1.0, fill))
        cr.restore()


# ---------------------------------------------------------------- shadows and groups
def with_shadow(cr, draw, dx=7, dy=11, alpha=0.30, soft=4):
    """Draw something with a soft drop shadow underneath, like a paper cut-out lying on the page."""
    cr.push_group()
    draw(cr)
    pat = cr.pop_group()
    taps = ((0, 0), (soft, 0), (-soft, 0), (0, soft), (0, -soft))
    for ox, oy in taps:
        cr.save()
        cr.translate(dx + ox, dy + oy)
        cr.set_source_rgba(*SHADOW, alpha / len(taps) * 1.6)
        cr.mask(pat)
        cr.restore()
    cr.set_source(pat)
    cr.paint()


def faded(cr, a, draw):
    if a <= 0:
        return
    if a >= 1:
        draw(cr)
        return
    cr.push_group()
    draw(cr)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)


class place:
    """Translate / scale / rotate around a point (context manager)."""

    def __init__(self, cr, x, y, s=1.0, rot=0.0):
        self.cr, self.x, self.y, self.s, self.rot = cr, x, y, max(abs(s), 1e-4), rot

    def __enter__(self):
        self.cr.save()
        self.cr.translate(self.x, self.y)
        if self.rot:
            self.cr.rotate(self.rot)
        self.cr.scale(self.s, self.s)
        return self.cr

    def __exit__(self, *a):
        self.cr.restore()


def appear(t, start, dur=0.3):
    """0 -> 1 pop (with a small overshoot) from `start`."""
    return back_out(seg(t, start, start + dur), 1.4) if t >= start else 0.0


def slide(t, start, dur=0.35):
    return ease_out(seg(t, start, start + dur))


# ---------------------------------------------------------------- basic shapes
def rrect(cr, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def fill(cr, col, alpha=1.0):
    cr.set_source_rgba(col[0], col[1], col[2], (col[3] if len(col) > 3 else 1) * alpha)
    cr.fill()


def stroke(cr, col, lw, alpha=1.0):
    cr.set_source_rgba(col[0], col[1], col[2], (col[3] if len(col) > 3 else 1) * alpha)
    cr.set_line_width(lw)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def poly(cr, pts, close=True):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    if close:
        cr.close_path()


def curve(cr, pts, close=False):
    """Smooth Catmull-Rom curve through points."""
    n = len(pts)
    cr.move_to(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if close or i > 0 else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if close or i + 2 < n else p2
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if close:
        cr.close_path()


def lin_grad(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        g.add_color_stop_rgba(o, *c[:3], c[3] if len(c) > 3 else 1)
    return g


def rad_grad(x, y, r0, r1, stops):
    g = cairo.RadialGradient(x, y, r0, x, y, r1)
    for o, c in stops:
        g.add_color_stop_rgba(o, *c[:3], c[3] if len(c) > 3 else 1)
    return g


def shade(c, k):
    """Darker (k < 1) or lighter (k > 1) version of a colour."""
    if k <= 1:
        return (c[0] * k, c[1] * k, c[2] * k, c[3] if len(c) > 3 else 1)
    return (c[0] + (1 - c[0]) * (k - 1), c[1] + (1 - c[1]) * (k - 1), c[2] + (1 - c[2]) * (k - 1),
            c[3] if len(c) > 3 else 1)


# ---------------------------------------------------------------- props
def card(cr, x, y, w, h, col=None, torn=False, seed=0):
    """A paper card (optionally with torn top and bottom edges)."""
    col = col or hexc("#e9dfc6")
    if torn:
        r = np.random.default_rng(seed)
        top = [(x + w * i / 18, y + r.uniform(-4, 4)) for i in range(19)]
        bot = [(x + w - w * i / 18, y + h + r.uniform(-4, 4)) for i in range(19)]
        poly(cr, top + bot)
    else:
        cr.rectangle(x, y, w, h)
    fill(cr, col)


def stamp(cr, t, start, s, x, y, rot=-0.12, col=None, size=64, box=True):
    """A red rubber stamp that slams down at `start`."""
    if t < start:
        return
    col = col or RED
    cue("thud", t, start)
    u = seg(t, start, start + 0.16)
    k = lerp(1.7, 1.0, ease_out(u))
    a = lerp(0.0, 0.92, min(1, u * 2))
    with place(cr, x, y, k, rot):
        font(cr, FONT_HEAD, size)
        w = cr.text_extents(s).x_advance
        cr.push_group()
        text(cr, s, -w / 2, size * 0.36, size, col)
        if box:
            rrect(cr, -w / 2 - 22, -size * 0.62, w + 44, size * 1.24, 8)
            stroke(cr, col, 6)
            rrect(cr, -w / 2 - 13, -size * 0.52, w + 26, size * 1.04, 5)
            stroke(cr, col, 2)
        pat = cr.pop_group()
        # worn ink: knock out a fixed speckle pattern
        cr.push_group()
        cr.set_source(pat)
        cr.paint_with_alpha(a)
        r = np.random.default_rng(hash(s) & 0xFFFF)
        cr.set_operator(cairo.OPERATOR_DEST_OUT)
        for _ in range(70):
            cr.arc(r.uniform(-w / 2 - 20, w / 2 + 20), r.uniform(-size * 0.6, size * 0.6), r.uniform(1, 3.5), 0, 6.3)
            cr.set_source_rgba(0, 0, 0, 0.75)
            cr.fill()
        cr.pop_group_to_source()
        cr.paint()


def red_x(cr, t, start, x, y, s=60, lw=10):
    """A hand-drawn red X that strokes on."""
    if t < start:
        return
    cue("scribble", t, start, 0.25)
    u1, u2 = seg(t, start, start + 0.14), seg(t, start + 0.12, start + 0.26)
    for (ax, ay, bx, by), u in (((-s, -s, s, s), u1), ((s, -s, -s, s), u2)):
        if u > 0:
            cr.move_to(x + ax, y + ay)
            cr.line_to(x + lerp(ax, bx, u), y + lerp(ay, by, u))
            stroke(cr, RED, lw)


def tick(cr, t, start, x, y, s=40, col=None, lw=9):
    if t < start:
        return
    col = col or hexc("#2f8f4e")
    u = seg(t, start, start + 0.22)
    pts = [(x - s * 0.8, y), (x - s * 0.2, y + s * 0.6), (x + s, y - s * 0.7)]
    cr.move_to(*pts[0])
    if u < 0.4:
        p = u / 0.4
        cr.line_to(lerp(pts[0][0], pts[1][0], p), lerp(pts[0][1], pts[1][1], p))
    else:
        p = (u - 0.4) / 0.6
        cr.line_to(*pts[1])
        cr.line_to(lerp(pts[1][0], pts[2][0], p), lerp(pts[1][1], pts[2][1], p))
    stroke(cr, col, lw)


def circle_mark(cr, t, start, x, y, rx, ry, col=None, lw=6):
    """A red pen circle drawn around something."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.4))
    a0 = -2.2
    cr.new_path()
    n = 40
    for i in range(int(n * u * 1.08) + 1):
        a = a0 + 2 * math.pi * 1.08 * i / n
        rr = 1 + 0.04 * math.sin(i * 0.7)
        p = (x + rx * rr * math.cos(a), y + ry * rr * math.sin(a))
        (cr.move_to if i == 0 else cr.line_to)(*p)
    stroke(cr, col or RED, lw)


def flip_counter(cr, t, start, value, x, y, digit_h=110, roll=0.9, plate=True, unit=None, tone="khaki"):
    """A mechanical flip counter on a brass plate; digits roll up to `value` (a string like "58,000")."""
    font(cr, FONT_HEAD, digit_h * 0.78)
    dw = digit_h * 0.62
    gap = 6
    cells = [(ch, ch.isdigit()) for ch in value]
    widths = [dw if d else dw * 0.32 for ch, d in cells]
    total = sum(widths) + gap * (len(cells) - 1)
    x0 = x - total / 2
    if plate:
        pad = 22
        rrect(cr, x0 - pad, y - digit_h / 2 - pad, total + 2 * pad, digit_h + 2 * pad, 8)
        cr.set_source(lin_grad(0, y - digit_h, 0, y + digit_h, [(0, hexc("#b39150")), (0.5, hexc("#8a6a32")),
                                                                 (1, hexc("#6d5126"))]))
        cr.fill()
        rrect(cr, x0 - pad + 5, y - digit_h / 2 - pad + 5, total + 2 * pad - 10, digit_h + 2 * pad - 10, 5)
        stroke(cr, hexc("#d9bd7c"), 1.5, 0.7)
        for sx in (x0 - pad + 11, x0 + total + pad - 11):
            for sy in (y - digit_h / 2 - pad + 11, y + digit_h / 2 + pad - 11):
                cr.arc(sx, sy, 3, 0, 6.3)
                fill(cr, hexc("#4a3818"))
    u = ease_out(seg(t, start, start + roll))
    if start <= t < start + roll:
        if int(t * 14) != int((t - 1 / FPS) * 14):
            cue("tick", t, t)
    digits = [int(ch) for ch, d in cells if d]
    target = int("".join(str(d) for d in digits) or 0)
    shown = int(round(target * u))
    s = str(shown).rjust(len(digits), "0")
    k = 0
    cx = x0
    for (ch, d), w in zip(cells, widths):
        if d:
            rrect(cr, cx, y - digit_h / 2, w, digit_h, 5)
            cr.set_source(lin_grad(0, y - digit_h / 2, 0, y + digit_h / 2,
                                   [(0, hexc("#f1e8d4")), (0.48, hexc("#e2d6bb")), (0.52, hexc("#cdbf9f")),
                                    (1, hexc("#e8dec8"))]))
            cr.fill()
            frac = (target * u) % 1 if k == len(digits) - 1 and u < 1 else 0
            cr.save()
            cr.rectangle(cx, y - digit_h / 2, w, digit_h)
            cr.clip()
            font(cr, FONT_HEAD, digit_h * 0.78)
            for off, dd in ((0, int(s[k])), (1, (int(s[k]) + 1) % 10)):
                gw = cr.text_extents(str(dd)).x_advance
                cr.move_to(cx + (w - gw) / 2, y + digit_h * 0.29 + (off - frac) * digit_h)
                cr.set_source_rgba(*hexc("#1f1a16"))
                cr.show_text(str(dd))
            cr.restore()
            cr.move_to(cx, y)
            cr.line_to(cx + w, y)
            stroke(cr, hexc("#000000"), 1.2, 0.35)
            k += 1
        else:
            font(cr, FONT_HEAD, digit_h * 0.6)
            cr.move_to(cx + w * 0.05, y + digit_h * 0.42)
            cr.set_source_rgba(*hexc("#2b2015"))
            cr.show_text(ch)
        cx += w + gap
    if unit:
        _, ink, _, _ = TONES[tone]
        text(cr, unit, x, y + digit_h / 2 + 64, 30, ink, FONT_MONO, align="center", spacing=2, alpha=0.85)


def stopwatch(cr, x, y, r, frac=0.0, hand=None, red=None):
    """A chrome stopwatch; `frac` of the dial shaded red (from 12 o'clock), hand at `hand` (0..1 turns)."""
    red = red or RED
    # crown + ring
    rrect(cr, x - r * 0.12, y - r * 1.32, r * 0.24, r * 0.2, 3)
    cr.set_source(lin_grad(x - r * 0.12, 0, x + r * 0.12, 0, [(0, hexc("#9a9a9a")), (0.5, hexc("#eeeeee")),
                                                              (1, hexc("#8a8a8a"))]))
    cr.fill()
    cr.arc(x, y - r * 1.2, r * 0.13, math.pi, 2 * math.pi)
    stroke(cr, hexc("#9a9a9a"), r * 0.05)
    cr.arc(x, y, r * 1.1, 0, 2 * math.pi)
    cr.set_source(lin_grad(x - r, y - r, x + r, y + r, [(0, hexc("#f4f4f4")), (0.45, hexc("#a8a8a8")),
                                                        (0.7, hexc("#e2e2e2")), (1, hexc("#7c7c7c"))]))
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    fill(cr, hexc("#f3efe6"))
    if frac > 0:
        cr.move_to(x, y)
        cr.arc(x, y, r * 0.86, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
        cr.close_path()
        fill(cr, red, 0.9)
    for i in range(60):
        a = 2 * math.pi * i / 60 - math.pi / 2
        l = 0.12 if i % 5 == 0 else 0.06
        cr.move_to(x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a))
        cr.line_to(x + r * (0.92 - l) * math.cos(a), y + r * (0.92 - l) * math.sin(a))
        stroke(cr, INK, 2.2 if i % 5 == 0 else 1.1)
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        n = str((i * 5) or 60)
        font(cr, FONT_HEAD, r * 0.15)
        tw = cr.text_extents(n).x_advance
        cr.move_to(x + r * 0.66 * math.cos(a) - tw / 2, y + r * 0.66 * math.sin(a) + r * 0.055)
        cr.set_source_rgba(*INK)
        cr.show_text(n)
    hand = frac if hand is None else hand
    a = 2 * math.pi * hand - math.pi / 2
    cr.move_to(x - r * 0.15 * math.cos(a), y - r * 0.15 * math.sin(a))
    cr.line_to(x + r * 0.84 * math.cos(a), y + r * 0.84 * math.sin(a))
    stroke(cr, INK, r * 0.035)
    cr.arc(x, y, r * 0.06, 0, 6.3)
    fill(cr, INK)
    cr.arc(x - r * 0.3, y - r * 0.35, r * 0.7, 0, 6.3)   # glass glint
    cr.set_source(rad_grad(x - r * 0.3, y - r * 0.35, 0, r * 0.7, [(0, (1, 1, 1, 0.22)), (1, (1, 1, 1, 0))]))
    cr.fill()


def vial(cr, x, y, s=1.0, label="ANTIVENOM", sub="FOR INJECTION", liquid=None, glow=0.0):
    """A small glass vial with a metal cap and a paper label (x, y = bottom centre)."""
    liquid = liquid or hexc("#f2ead2")
    with place(cr, x, y, s):
        w, h = 120, 230
        if glow > 0:
            cr.arc(0, -h / 2, 190, 0, 6.3)
            cr.set_source(rad_grad(0, -h / 2, 10, 190, [(0, (1, 0.95, 0.75, 0.55 * glow)), (1, (1, 0.95, 0.75, 0))]))
            cr.fill()
        # glass body
        rrect(cr, -w / 2, -h + 50, w, h - 50, 16)
        cr.set_source(lin_grad(-w / 2, 0, w / 2, 0, [(0, (0.86, 0.88, 0.88, 0.95)), (0.2, (1, 1, 1, 0.9)),
                                                     (0.55, (0.84, 0.86, 0.86, 0.9)), (1, (0.7, 0.72, 0.72, 0.95))]))
        cr.fill()
        rrect(cr, -w / 2 + 6, -h * 0.55, w - 12, h * 0.55 - 6, 12)
        fill(cr, liquid, 0.9)
        # neck + cap
        cr.rectangle(-w * 0.3, -h + 30, w * 0.6, 24)
        fill(cr, hexc("#c9cccc"))
        rrect(cr, -w * 0.42, -h, w * 0.84, 40, 6)
        cr.set_source(lin_grad(-w / 2, 0, w / 2, 0, [(0, hexc("#7d8285")), (0.3, hexc("#e8eaea")),
                                                     (0.6, hexc("#9aa0a3")), (1, hexc("#6a6f72"))]))
        cr.fill()
        # label
        cr.rectangle(-w / 2 + 2, -h * 0.62, w - 4, h * 0.36)
        fill(cr, hexc("#f7f2e6"))
        cr.rectangle(-w / 2 + 2, -h * 0.62 + 8, w - 4, 26)
        fill(cr, RED)
        text(cr, "Rx", 0, -h * 0.62 + 29, 20, hexc("#ffffff"), align="center")
        sz = fit(cr, label, 26, w - 14)
        text(cr, label, 0, -h * 0.62 + 66, sz, INK, align="center")
        text(cr, sub, 0, -h * 0.62 + 84, 9, INK, FONT_MONO, align="center", alpha=0.8)
        cr.rectangle(-w / 2 + 14, -h + 56, 10, h - 80)
        fill(cr, (1, 1, 1), 0.35)


def polaroid(cr, x, y, w, h, draw, rot=0.0, caption=None):
    """A photo print with a white border; `draw(cr, w, h)` paints the picture area (origin at its top-left)."""
    with place(cr, x, y, 1.0, rot):
        def body(c):
            c.rectangle(-w / 2, -h / 2, w, h)
            fill(c, hexc("#f7f3ea"))
            m = w * 0.07
            c.save()
            c.rectangle(-w / 2 + m, -h / 2 + m, w - 2 * m, h - m * 4.2)
            c.clip()
            c.translate(-w / 2 + m, -h / 2 + m)
            draw(c, w - 2 * m, h - m * 4.2)
            c.restore()
            if caption:
                text(c, caption, 0, h / 2 - m * 1.2, w * 0.09, INK, FONT_MONO, align="center")
        with_shadow(cr, body, 5, 8, 0.35)


def clothes_pin(cr, x, y):
    rrect(cr, x - 9, y - 22, 18, 44, 4)
    fill(cr, hexc("#b8925e"))
    cr.move_to(x, y - 22)
    cr.line_to(x, y + 22)
    stroke(cr, hexc("#7a5a32"), 1.5)


def microscope(cr, x, y, r, draw, tint=None):
    """A circular microscope view: `draw(cr)` paints the slide in a coordinate frame centred on (0, 0)."""
    tint = tint or hexc("#efe2b8")
    cr.arc(x, y, r + 26, 0, 6.3)
    cr.set_source(lin_grad(x - r, y - r, x + r, y + r, [(0, hexc("#3a3632")), (0.5, hexc("#1d1b19")),
                                                        (1, hexc("#4a4540"))]))
    cr.fill()
    cr.arc(x, y, r + 8, 0, 6.3)
    fill(cr, hexc("#0d0c0b"))
    cr.save()
    cr.arc(x, y, r, 0, 6.3)
    cr.clip()
    cr.set_source(rad_grad(x, y, r * 0.2, r, [(0, shade(tint, 1.08)), (1, shade(tint, 0.8))]))
    cr.paint()
    cr.translate(x, y)
    draw(cr)
    cr.restore()
    cr.arc(x, y, r, 0, 6.3)   # lens vignette
    cr.set_source(rad_grad(x, y, r * 0.65, r, [(0, (0, 0, 0, 0)), (1, (0, 0, 0, 0.45))]))
    cr.fill()


def pie(cr, x, y, r, frac, col=None, back=None, ink=INK):
    back = back or hexc("#e9dfc6")
    cr.arc(x, y, r, 0, 6.3)
    fill(cr, back)
    if frac > 0:
        cr.move_to(x, y)
        cr.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
        cr.close_path()
        fill(cr, col or RED)
    cr.arc(x, y, r, 0, 6.3)
    stroke(cr, ink, 3)


def checklist(cr, t, x, y, w, items, starts, title="WHAT TO DO", tone="khaki"):
    """A card with a list; each item's box gets a tick at its start time."""
    h = 120 + 92 * len(items)

    def body(c):
        card(c, x, y, w, h, hexc("#ece3cb"))
        text(c, title, x + 34, y + 58, 20, INK, FONT_MONO, spacing=2.5, alpha=0.8)
        for i, (s, st) in enumerate(zip(items, starts)):
            yy = y + 130 + 92 * i
            c.rectangle(x + 34, yy - 40, 46, 46)
            stroke(c, INK, 3.5)
            text(c, s, x + 108, yy, fit(c, s, 50, w - 140), INK, alpha=0.35 + 0.65 * seg(t, st, st + 0.2))
            tick(c, t, st, x + 57, yy - 17, 24, lw=7)
    with_shadow(cr, body, 6, 10, 0.3)


def comment_bubble(cr, x, y, w, h, s, t=None, start=0):
    def body(c):
        rrect(c, x, y, w, h, 34)
        fill(c, hexc("#fbf8f0"))
        poly(c, [(x + 70, y + h - 4), (x + 50, y + h + 40), (x + 120, y + h - 4)])
        fill(c, hexc("#fbf8f0"))
        text(c, s, x + w / 2, y + h / 2 + 18, fit(c, s, 50, w - 60), INK, align="center")
    with_shadow(cr, body, 6, 10, 0.3)


# ---------------------------------------------------------------- maps (Natural Earth, public domain)
_MAPS = {}


def _map(name):
    if name not in _MAPS:
        _MAPS[name] = json.load(open(os.path.join(ROOT, "assets", "maps", f"{name}.json")))
    return _MAPS[name]


def india(cr, cx, cy, height, col, edge=None, lw=3):
    """India's outline (India point-of-view boundary), centred at (cx, cy). Returns a lon/lat -> x, y function."""
    rings = _map("india")["india"]
    lat0, lat1, lon0, lon1 = 6.5, 37.2, 68.0, 97.5
    k = height / (lat1 - lat0)
    kx = k * math.cos(math.radians(22))
    def P(lon, lat):
        return cx + (lon - (lon0 + lon1) / 2) * kx, cy - (lat - (lat0 + lat1) / 2) * k
    for ring in rings:
        poly(cr, [P(*p) for p in ring])
        if edge:
            cr.set_source_rgba(*col)
            cr.fill_preserve()
            stroke(cr, edge, lw)
        else:
            fill(cr, col)
    return P


def world(cr, cx, cy, width, col, edge=None, lw=1.2):
    """Equirectangular world map (no Antarctica), centred at (cx, cy)."""
    k = width / 360
    def P(lon, lat):
        return cx + lon * k, cy - (lat - 12) * k
    for ring in _map("world"):
        poly(cr, [P(*p) for p in ring])
        if edge:
            cr.set_source_rgba(*col)
            cr.fill_preserve()
            stroke(cr, edge, lw)
        else:
            fill(cr, col)
    return P


# ---------------------------------------------------------------- shots and the frame loop
@dataclass
class Shot:
    draw: object                 # draw(cr, t, tl, beat_id) paints the content
    label: str = ""
    fig: int = 1
    tone: str = "khaki"
    small: str = ""
    big: str = ""
    big_at: str = None           # word in the line that fills the big headline (default: shortly after the start)
    zoom: float = 0.035          # slow push-in over the shot
    focus: tuple = (W / 2, 760)
    extra: dict = field(default_factory=dict)


XFADE = 0.14


def _shot(cr, t, tl, shots, name, start, end, beat_id):
    sh = shots[name]
    paper(cr, sh.tone)
    cr.save()
    u = seg(t, start, end)
    z = 1 + sh.zoom * smooth(u)
    fx, fy = sh.focus
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    sh.draw(cr, t, tl, beat_id)
    cr.restore()
    header(cr, sh.tone, sh.label, sh.fig)
    b = tl.by_id[beat_id]
    small, big, big_at, t0 = sh.small, sh.big, sh.big_at, start
    for word, sm, bg, bat in sh.extra.get("phases", ()):   # a line can change headline part-way through
        tw = tl.at(beat_id, word)
        if t >= tw - 0.05:
            small, big, big_at, t0 = sm, bg, bat, tw - 0.05
    t_big = tl.at(beat_id, big_at) if big_at else b.start + 0.35
    headline(cr, t, sh.tone, small, big, t0, t_big)


def frame(cr, t, tl, shots):
    name, start, end = tl.scene_at(t)
    beat_id = next(b.id for b in tl.beats if b.scene == name)
    k = [s[0] for s in tl.scenes].index(name)
    _shot(cr, t, tl, shots, name, start, end, beat_id)
    if k > 0 and t < start + XFADE:   # quick cross-fade from the previous shot (held at its last frame)
        pname, pstart, pend = tl.scenes[k - 1]
        pid = next(b.id for b in tl.beats if b.scene == pname)
        cr.push_group()
        _shot(cr, pend - 1e-3, tl, shots, pname, pstart, pend, pid)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - smooth(seg(t, start, start + XFADE)))
    if k > 0 and start <= t < start + 1 / FPS:
        cue("whoosh", t, start, 0.25)
    brand(cr)


def brand(cr):
    """Channel logo (owner's, top-left, scaled to sit above the header) and the name faint across the page."""
    from .doc_brand import CHANNEL, _badge_surface
    cr.save()
    cr.identity_matrix()
    for x, y in ((200, 520), (520, 900)):
        with place(cr, x, y, 1.0, 0.38):
            font(cr, FONT_HEAD, 28)
            wd = cr.text_extents(CHANNEL).x_advance
            cr.move_to(-wd / 2, 0)
            cr.set_source_rgba(0.5, 0.45, 0.4, 0.10)
            cr.show_text(CHANNEL)
    cr.translate(24, 40)
    cr.scale(0.66, 0.66)
    cr.set_source_surface(_badge_surface(), 0, 0)
    cr.paint_with_alpha(0.95)
    cr.restore()
