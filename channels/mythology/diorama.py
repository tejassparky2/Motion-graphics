"""The "painted diorama" look from the owner's reference reel (7 Nov 2026, "make it like this": the Diwali-series reel
"Lakshmi has an elder sister"): painted cut-out characters on painted stage sets, with a thin top label row
("THE DOORSTEP · DIWALI NIGHT" ... "FIG. 1"), a torn white tag ("DIWALI · DAY 3/5"), torn paper notes, a calendar
card, a checklist card with red ticks, progress bars, red target rings, glowing dotted paths, flat paper clouds and
faint poster fold lines. Everything is a pure function of t.

Text uses poster.draw_text (Anton for headlines, IBM Plex Mono for labels)."""
import functools
import math
import os

import cairo
import numpy as np

from poster import (CORAL, CREAM, FPS, H, MONO_FONT, RED, W, back, clamp, draw_text, prog, text_size, to_surface)

INK = (0.12, 0.10, 0.09)
PAPER_W = (0.96, 0.94, 0.88)
GOLDC = (0.93, 0.72, 0.25)
GREEN = (0.45, 0.78, 0.45)


# ---------------------------------------------------------------- images
@functools.lru_cache(maxsize=64)
def _img(path, max_h=2400):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    if im.height > max_h:
        im = im.resize((int(im.width * max_h / im.height), max_h), Image.LANCZOS)
    return to_surface(im)


@functools.lru_cache(maxsize=64)
def _shadow(path, max_h=2400, blur=14):
    """A soft dark silhouette of a cut-out, for the paper drop shadow."""
    from PIL import Image, ImageFilter
    im = Image.open(path).convert("RGBA")
    if im.height > max_h:
        im = im.resize((int(im.width * max_h / im.height), max_h), Image.LANCZOS)
    a = im.getchannel("A")
    sh = Image.new("RGBA", im.size, (10, 6, 4, 0))
    sh.putalpha(a.point(lambda v: int(v * 0.55)))
    pad = blur * 3
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.paste(sh, (pad, pad))
    return to_surface(big.filter(ImageFilter.GaussianBlur(blur))), pad


def stage(cr, t, path, t0=0.0, drift=(0.0, -24.0), zoom=1.0, dim=0.0):
    """A painted set filling the frame (scaled to cover), drifting slowly. A missing set paints a dusk gradient."""
    if not os.path.exists(path):
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.12, 0.12, 0.28)
        g.add_color_stop_rgb(1, 0.35, 0.22, 0.18)
        cr.set_source(g)
        cr.paint()
        return
    s = _img(path)
    k = max(W / s.get_width(), H / s.get_height()) * 1.06 * zoom
    p = clamp((t - t0) / 8.0)
    cr.save()
    cr.translate(W / 2 + drift[0] * p, H / 2 + drift[1] * p)
    cr.scale(k, k)
    cr.set_source_surface(s, -s.get_width() / 2, -s.get_height() / 2)
    cr.paint()
    cr.restore()
    if dim:
        cr.set_source_rgba(0.03, 0.02, 0.06, dim)
        cr.paint()


def cutout(cr, t, path, x, y, h, alpha=1.0, flip=False, rot=0.0, bob=1.0, seed=0, shadow=True, anchor="feet",
           glow=0.0):
    """A painted cut-out character, feet at (x, y) and h px tall, with a soft paper drop shadow (down-right), a slow
    breathing bob and an optional golden glow behind it."""
    if alpha <= 0 or h <= 2:
        return
    s = _img(path)
    k = h / s.get_height()
    w = s.get_width() * k
    by = 4 * math.sin(t * 1.6 + seed) * bob
    if glow > 0:
        g = cairo.RadialGradient(x, y - h * 0.55, 10, x, y - h * 0.55, h * 0.75)
        g.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.55 * glow * alpha)
        g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        cr.set_source(g)
        cr.arc(x, y - h * 0.55, h * 0.75, 0, 2 * math.pi)
        cr.fill()
    cr.save()
    cr.translate(x, y + by)
    cr.rotate(rot)
    if flip:
        cr.scale(-1, 1)
    oy = -h if anchor == "feet" else -h / 2
    if shadow:
        sh, pad = _shadow(path)
        cr.save()
        cr.translate(10, 14)
        cr.scale(k, k)
        cr.set_source_surface(sh, -s.get_width() / 2 - pad, oy / k - pad)
        cr.paint_with_alpha(0.8 * alpha)
        cr.restore()
    cr.scale(k, k)
    cr.set_source_surface(s, -s.get_width() / 2, oy / k)
    cr.paint_with_alpha(alpha)
    cr.restore()
    return w


def slide(t, t0, x0, x1, dur=0.55):
    p = back(clamp((t - t0) / dur)) if t >= t0 else 0.0
    return x0 + (x1 - x0) * p


# ---------------------------------------------------------------- the reference's paper devices
def label_row(cr, left, right, alpha=1.0, y=78, color=CREAM):
    """The thin top row: a place label on the left, "FIG. n" on the right, a hairline under it."""
    draw_text(cr, left, 60, y, 22, color, 0.85 * alpha, MONO_FONT, "lm", tracking=3)
    draw_text(cr, right, W - 60, y, 22, color, 0.85 * alpha, MONO_FONT, "rm", tracking=3)
    cr.set_source_rgba(*color, 0.35 * alpha)
    cr.set_line_width(2)
    cr.move_to(60, y + 26)
    cr.line_to(W - 60, y + 26)
    cr.stroke()


def _torn_path(cr, x, y, w, h, seed, jag=6):
    rng = np.random.default_rng(seed)
    cr.move_to(x, y)
    n = max(4, int(w / 18))
    for i in range(1, n + 1):
        cr.line_to(x + w * i / n, y + rng.uniform(-jag, jag) * 0.6)
    m = max(3, int(h / 14))
    for i in range(1, m + 1):
        cr.line_to(x + w + rng.uniform(-jag, jag), y + h * i / m)
    for i in range(n - 1, -1, -1):
        cr.line_to(x + w * i / n, y + h + rng.uniform(-jag, jag) * 0.6)
    for i in range(m - 1, 0, -1):
        cr.line_to(x + rng.uniform(-jag, jag), y + h * i / m)
    cr.close_path()


def torn_tag(cr, t, t0, left, right, x, y, size=26, seed=3, rot=-0.02):
    """The white torn tag ("DIWALI · DAY 3/5"): dark mono text with the last part in red."""
    p = prog(t, t0, 0.3)
    if p <= 0:
        return
    w1 = text_size(left, size, MONO_FONT, 2)[0]
    w2 = text_size(right, size, MONO_FONT, 2)[0]
    w, h = w1 + w2 + 50, size * 1.8
    cr.save()
    cr.translate(x, y - 20 * (1 - p))
    cr.rotate(rot)
    cr.set_source_rgba(0, 0, 0, 0.25 * p)
    _torn_path(cr, -w / 2 + 5, -h / 2 + 6, w, h, seed)
    cr.fill()
    cr.set_source_rgba(*PAPER_W, p)
    _torn_path(cr, -w / 2, -h / 2, w, h, seed)
    cr.fill()
    draw_text(cr, left, -w / 2 + 22, 0, size, INK, p, MONO_FONT, "lm", tracking=2)
    draw_text(cr, right, -w / 2 + 28 + w1, 0, size, RED, p, MONO_FONT, "lm", tracking=2)
    cr.restore()


def torn_note(cr, t, t0, text, x, y, size=44, seed=7, rot=-0.03, lines=None):
    """A torn cream paper strip with dark headline text ("FOUND OUT AFTER THE WEDDING")."""
    p = prog(t, t0, 0.3)
    if p <= 0:
        return
    rows = lines or [text]
    w = max(text_size(r, size)[0] for r in rows) + 60
    h = size * 1.25 * len(rows) + 30
    s = 1.15 - 0.15 * back(clamp((t - t0) / 0.3))
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(0, 0, 0, 0.3 * p)
    _torn_path(cr, -w / 2 + 6, -h / 2 + 8, w, h, seed, jag=8)
    cr.fill()
    cr.set_source_rgba(0.95, 0.91, 0.80, p)
    _torn_path(cr, -w / 2, -h / 2, w, h, seed, jag=8)
    cr.fill()
    for i, r in enumerate(rows):
        draw_text(cr, r, 0, -h / 2 + 15 + size * 0.62 + i * size * 1.25, size, INK, p, anchor="cm")
    cr.restore()


def checklist(cr, t, x, y, w, title, items, alpha=1.0):
    """A cream card with a mono title and rows that tick in: items = [(text, t_show)]."""
    p = prog(t, items[0][1] - 0.3, 0.3) * alpha
    if p <= 0:
        return
    h = 90 + 72 * len(items)
    cr.set_source_rgba(0, 0, 0, 0.3 * p)
    cr.rectangle(x + 8, y + 10, w, h)
    cr.fill()
    cr.set_source_rgba(0.96, 0.93, 0.84, p)
    cr.rectangle(x, y, w, h)
    cr.fill()
    draw_text(cr, title, x + 28, y + 38, 24, INK, p, MONO_FONT, "lm", tracking=3)
    for i, (label, ts) in enumerate(items):
        q = prog(t, ts, 0.25) * alpha
        if q <= 0:
            continue
        ry = y + 100 + 72 * i
        cr.set_source_rgba(*INK, 0.8 * q)
        cr.set_line_width(4)
        cr.rectangle(x + 28, ry - 20, 40, 40)
        cr.stroke()
        k = prog(t, ts + 0.15, 0.25)
        if k > 0:                                          # red tick
            cr.set_source_rgba(*RED, q)
            cr.set_line_width(8)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(x + 32, ry)
            cr.line_to(x + 32 + 12 * min(1, k * 2), ry + 12 * min(1, k * 2))
            if k > 0.5:
                cr.line_to(x + 44 + 26 * (k - 0.5) * 2, ry + 12 - 30 * (k - 0.5) * 2)
            cr.stroke()
        draw_text(cr, label, x + 90, ry, 44, INK, q, anchor="lm")


def calendar(cr, t, t0, x, y, month, year, first_weekday, days, marks, highlight, w=560):
    """A wall calendar card: red header, a grid of days, red ticks on `marks`, a gold box on `highlight`."""
    p = prog(t, t0, 0.35)
    if p <= 0:
        return
    cw = w / 7
    h = 150 + cw * 6
    cr.save()
    cr.translate(x, y + 60 * (1 - back(p)))
    cr.rotate(-0.02)
    cr.set_source_rgba(0, 0, 0, 0.3 * p)
    cr.rectangle(-w / 2 + 10, 12, w, h)
    cr.fill()
    cr.set_source_rgba(0.97, 0.95, 0.88, p)
    cr.rectangle(-w / 2, 0, w, h)
    cr.fill()
    cr.set_source_rgba(0.75, 0.16, 0.13, p)
    cr.rectangle(-w / 2, 0, w, 100)
    cr.fill()
    draw_text(cr, month, -w / 2 + 28, 50, 56, CREAM, p, anchor="lm")
    draw_text(cr, str(year), w / 2 - 24, 50, 26, CREAM, p, MONO_FONT, "rm")
    for d in range(1, days + 1):
        i = first_weekday + d - 1
        cx, cy = -w / 2 + cw * (i % 7) + cw / 2, 130 + cw * (i // 7) + cw / 2
        if d == highlight:
            cr.set_source_rgba(*GOLDC, p)
            cr.rectangle(cx - cw * 0.42, cy - cw * 0.42, cw * 0.84, cw * 0.84)
            cr.fill()
        draw_text(cr, str(d), cx, cy, 30, INK, p, MONO_FONT, "cm")
        if d in marks:
            cr.set_source_rgba(*RED, p)
            cr.set_line_width(6)
            cr.move_to(cx - 18, cy)
            cr.line_to(cx - 6, cy + 14)
            cr.line_to(cx + 20, cy - 18)
            cr.stroke()
    cr.restore()


def progress(cr, t, t0, x, y, w, label, value, color=CREAM):
    p = prog(t, t0, 0.3)
    if p <= 0:
        return
    draw_text(cr, label, x, y - 30, 22, color, p, MONO_FONT, "lm", tracking=3)
    cr.set_source_rgba(1, 1, 1, 0.2 * p)
    cr.rectangle(x, y, w, 16)
    cr.fill()
    cr.set_source_rgba(*color, p)
    cr.rectangle(x, y, w * clamp(value), 16)
    cr.fill()
    draw_text(cr, f"{int(round(value * 100))}%", x + w + 20, y + 8, 34, CORAL if value < 0.5 else color, p,
              MONO_FONT, "lm")


def target(cr, t, t0, x, y, r, color=RED):
    """The red target ring the reference puts on a spot ("dark corner")."""
    p = prog(t, t0, 0.35)
    if p <= 0:
        return
    rr = r * (1.6 - 0.6 * back(clamp((t - t0) / 0.35)))
    cr.set_source_rgba(*color, p)
    cr.set_line_width(5)
    cr.arc(x, y, rr, 0, 2 * math.pi)
    cr.stroke()
    cr.arc(x, y, rr * 0.45, 0, 2 * math.pi)
    cr.stroke()
    for a in range(4):
        ang = a * math.pi / 2
        cr.move_to(x + math.cos(ang) * rr * 0.7, y + math.sin(ang) * rr * 0.7)
        cr.line_to(x + math.cos(ang) * rr * 1.25, y + math.sin(ang) * rr * 1.25)
    cr.stroke()


def dotted_path(cr, t, t0, pts, color=GOLDC, dur=1.0, r=5):
    """Glowing dots running along a polyline (lamp to lamp)."""
    p = clamp((t - t0) / dur)
    if p <= 0:
        return
    segs = list(zip(pts, pts[1:]))
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    step, d = 26, 0.0
    for a, b in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(L / step)
        for i in range(n):
            if d + i * step > total * p:
                return
            f = i / max(1, n)
            x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            cr.arc(x, y, r * 2.4, 0, 2 * math.pi)
            cr.set_source_rgba(*color, 0.25)
            cr.fill()
            cr.arc(x, y, r, 0, 2 * math.pi)
            cr.set_source_rgba(1, 0.95, 0.75, 0.95)
            cr.fill()
        d += L


def paper_clouds(cr, t, y0=120, n=6, seed=2, color=(0.86, 0.87, 0.93), alpha=0.9):
    """Flat cut-paper clouds drifting slowly across the top."""
    rng = np.random.default_rng(seed)
    for k in range(n):
        x = (rng.uniform(-200, W) + t * rng.uniform(6, 16)) % (W + 400) - 200
        y = y0 + rng.uniform(0, 260)
        s = rng.uniform(0.7, 1.4)
        cr.save()
        cr.translate(x, y)
        cr.scale(s, s)
        cr.set_source_rgba(0, 0, 0, 0.12 * alpha)
        for dx, dy, r in ((0, 8, 46), (50, -12, 56), (104, 8, 44), (52, 20, 50)):
            cr.arc(dx + 6, dy + 8, r, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(*color, alpha)
        for dx, dy, r in ((0, 8, 46), (50, -12, 56), (104, 8, 44), (52, 20, 50)):
            cr.arc(dx, dy, r, 0, 2 * math.pi)
            cr.fill()
        cr.restore()


@functools.lru_cache(maxsize=4)
def _grain(k):
    from PIL import Image
    rng = np.random.default_rng(200 + k)
    n = rng.normal(128, 38, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(n, "L").convert("RGBA")
    im.putalpha(12)
    return to_surface(im.resize((W, H)))


def finish(cr, t):
    """The reference's poster feel: two faint vertical fold lines, a soft vignette and per-frame grain."""
    for fx in (W / 3, 2 * W / 3):
        cr.set_source_rgba(1, 1, 1, 0.06)
        cr.rectangle(fx - 1, 0, 2, H)
        cr.fill()
        cr.set_source_rgba(0, 0, 0, 0.05)
        cr.rectangle(fx + 1, 0, 2, H)
        cr.fill()
    g = cairo.RadialGradient(W / 2, H * 0.48, H * 0.36, W / 2, H * 0.5, H * 0.8)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.01, 0.01, 0.03, 0.5)
    cr.set_source(g)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVERLAY)
    cr.set_source_surface(_grain(int(t * FPS) % 4), 0, 0)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
