"""Drawing kit for the Hinglish mini-documentary channel: photo cut-outs on creased poster paper, two-tier headlines
(small dark setup line + one big red word), hand-drawn red marks, specimen labels and flip counters.

Everything is a pure function of time, so any frame can be drawn on its own (parallel rendering, stills, sheets).
Text is rasterised with Pillow from the OFL fonts in fonts/ and cached as cairo surfaces.
"""
import functools
import math
import os

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
HEAD_FONT = os.path.join(FONTS, "Anton-Regular.ttf")
MONO_FONT = os.path.join(FONTS, "IBMPlexMono-Medium.ttf")

PAPER = (0.85, 0.79, 0.66)
INK = (0.16, 0.12, 0.09)
RED = (0.74, 0.13, 0.11)
FADED = (0.45, 0.39, 0.31)
MARGIN = 70


# ---------- timing ----------

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    """Cubic ease-out on 0..1."""
    x = clamp(x)
    return 1 - (1 - x) ** 3


def prog(t, t0, dur=0.35):
    return ease((t - t0) / dur) if dur > 0 else float(t >= t0)


def back(x, s=1.7):
    """Ease-out with a small overshoot (pops, drops)."""
    x = clamp(x) - 1
    return 1 + x * x * ((s + 1) * x + s)


def window(t, t0, t1, fade=0.25):
    """1 inside [t0, t1], fading in/out over `fade` seconds at both ends."""
    return clamp((t - t0) / fade) * clamp((t1 - t) / fade)


# ---------- PIL -> cairo ----------

def to_surface(img):
    """RGBA Pillow image -> cairo ARGB32 surface (premultiplied)."""
    a = np.asarray(img.convert("RGBA"), dtype=np.float32)
    alpha = a[..., 3:4] / 255.0
    bgra = np.empty_like(a)
    bgra[..., 0], bgra[..., 1], bgra[..., 2] = a[..., 2], a[..., 1], a[..., 0]
    bgra[..., :3] *= alpha
    bgra[..., 3] = a[..., 3]
    h, w = a.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = bytearray(stride * h)
    arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, stride)
    arr[:, : w * 4] = bgra.astype(np.uint8).reshape(h, w * 4)
    return cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_ARGB32, w, h, stride)


@functools.lru_cache(maxsize=512)
def text_surface(text, size, color=INK, font=HEAD_FONT, tracking=0):
    f = ImageFont.truetype(font, size)
    l, t_, r, b = f.getbbox(text)
    pad = max(4, size // 10)
    w = r - l + 2 * pad + tracking * max(0, len(text) - 1)
    h = b - t_ + 2 * pad
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rgb = tuple(int(c * 255) for c in color)
    if tracking:
        x = pad - l
        for ch in text:
            d.text((x, pad - t_), ch, font=f, fill=rgb + (255,))
            x += f.getlength(ch) + tracking
    else:
        d.text((pad - l, pad - t_), text, font=f, fill=rgb + (255,))
    return to_surface(img), pad


def text_size(text, size, font=HEAD_FONT, tracking=0):
    s, pad = text_surface(text, size, INK, font, tracking)
    return s.get_width() - 2 * pad, s.get_height() - 2 * pad


def draw_text(cr, text, x, y, size, color=INK, alpha=1.0, font=HEAD_FONT, anchor="lt", tracking=0):
    """anchor: l/c/r + t/m/b (e.g. "cm" = centred both ways)."""
    s, pad = text_surface(text, size, color, font, tracking)
    w, h = s.get_width() - 2 * pad, s.get_height() - 2 * pad
    dx = {"l": 0, "c": -w / 2, "r": -w}[anchor[0]]
    dy = {"t": 0, "m": -h / 2, "b": -h}[anchor[1]]
    cr.set_source_surface(s, x + dx - pad, y + dy - pad)
    cr.paint_with_alpha(alpha)
    return x + dx, y + dy, w, h


# ---------- paper ----------

@functools.lru_cache(maxsize=8)
def paper_surface(seed=1, tone=PAPER):
    rng = np.random.default_rng(seed)
    base = np.ones((H, W, 3), np.float32) * np.array(tone, np.float32)
    grain = rng.normal(0, 0.018, (H // 2, W // 2, 1)).astype(np.float32)
    grain = np.kron(grain, np.ones((2, 2, 1), np.float32))[:H, :W]
    blotch = np.asarray(Image.fromarray((rng.random((24, 14)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                        np.float32)[..., None] / 255.0
    img = base + grain + (blotch - 0.5) * 0.05
    yy, xx = np.mgrid[0:H, 0:W]
    vign = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2
    img *= (1 - 0.22 * vign)[..., None]
    for fx in (W * 0.34, W * 0.70):              # vertical folds: a dark crease with a lit edge beside it
        d = xx - fx
        img *= (1 - 0.07 * np.exp(-(d / 3.0) ** 2))[..., None]
        img *= (1 + 0.035 * np.exp(-((d - 7) / 9.0) ** 2))[..., None]
    for fy in (H * 0.52,):                        # one faint horizontal fold
        d = yy - fy
        img *= (1 - 0.035 * np.exp(-(d / 3.0) ** 2))[..., None]
    rgb = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    return to_surface(Image.fromarray(rgb, "RGB"))


def paper(cr, seed=1, tone=PAPER):
    cr.set_source_surface(paper_surface(seed, tone), 0, 0)
    cr.paint()


SLATE = (0.13, 0.15, 0.16)


@functools.lru_cache(maxsize=2)
def slate_surface(seed=5):
    """Dark slate ground for inside-the-body / microscope scenes, with a soft centre light and grain."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W]
    light = np.exp(-(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.5) / (H * 0.55)) ** 2))
    base = np.array(SLATE, np.float32)[None, None, :] * (0.75 + 0.55 * light[..., None])
    grain = rng.normal(0, 0.012, (H // 2, W // 2, 1)).astype(np.float32)
    img = base + np.kron(grain, np.ones((2, 2, 1), np.float32))[:H, :W]
    return to_surface(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), "RGB"))


def slate(cr):
    cr.set_source_surface(slate_surface(), 0, 0)
    cr.paint()


@functools.lru_cache(maxsize=1)
def print_texture():
    """The printed-poster finish laid over every finished frame (as in the reference style: halftone dot screen on
    photos and paper, speckled grain, faint ruled lines and a column of binder holes down the left edge)."""
    rng = np.random.default_rng(11)
    a = np.zeros((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    a += 0.055 * (((xx % 5) < 2) & ((yy % 5) < 2))                       # halftone screen
    a += np.clip(rng.normal(0, 0.035, (H, W)), 0, None).astype(np.float32)  # speckle
    for y in range(240, H, 58):                                          # ruled lines
        a[y:y + 1, :] += 0.05
    for y in range(300, H - 100, 175):                                   # binder holes
        a[(yy - y) ** 2 + (xx - 26) ** 2 < 49] = 0.32
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = 40
    rgba[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return to_surface(Image.fromarray(rgba, "RGBA"))


def finish(cr):
    """Lay the printed texture over the whole frame (call last)."""
    cr.set_source_surface(print_texture(), 0, 0)
    cr.paint()


def footnote(cr, text, alpha=1.0, y=H - 120, color=None):
    draw_text(cr, text.upper(), W / 2, y, 20, color or FADED, 0.85 * alpha, MONO_FONT, "cm", tracking=2)


# ---------- physical motion ----------

def drop(t, t0, y, dur=0.45, height=700):
    """y position of an object dropped in from above, landing at `y` with a small bounce."""
    p = clamp((t - t0) / dur)
    return y - height * (1 - back(p, 1.4))


def knock(t, t_hit, x, y, rot=0.0, dx=900, dy=380, spin=1.2, dur=0.5):
    """(x, y, rot, alpha) of an object knocked away from t_hit: flies off sideways and down while spinning."""
    p = clamp((t - t_hit) / dur)
    if p <= 0:
        return x, y, rot, 1.0
    q = p * p
    return x + dx * q, y + dy * q, rot + spin * q, 1.0 - clamp((p - 0.6) / 0.4)


def slide(t, t0, x0, x1, dur=0.5):
    return x0 + (x1 - x0) * ease((t - t0) / dur)


def magnifier(cr, t, t0, cx, cy, r, inner, rim=(0.78, 0.74, 0.66), dark=False):
    """A round lens that pops open at t0 and shows `inner(cr)` (drawn in frame coordinates, clipped to the lens)."""
    p = clamp((t - t0) / 0.35)
    if p <= 0:
        return
    rr = r * (0.2 + 0.8 * back(p, 1.5))
    cr.save()
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.arc(cx + 10, cy + 18, rr, 0, 2 * math.pi)
    cr.fill()
    cr.arc(cx, cy, rr, 0, 2 * math.pi)
    cr.clip()
    cr.set_source_rgb(*((0.09, 0.08, 0.07) if dark else (0.95, 0.90, 0.80)))
    cr.paint()
    inner(cr)
    cr.reset_clip()
    cr.restore()
    cr.set_source_rgba(*rim, 1)
    cr.set_line_width(18)
    cr.arc(cx, cy, rr, 0, 2 * math.pi)
    cr.stroke()
    cr.set_source_rgba(1, 1, 1, 0.25)
    cr.set_line_width(4)
    cr.arc(cx, cy, rr - 14, 3.6, 4.6)
    cr.stroke()


def icon_array(cr, t, t0, n, cols, x, y, size, red=(), red_at=None, gap=0.25, step=0.035, color=INK):
    """n person icons in a grid that pop in one by one from t0; indices in `red` turn red at red_at."""
    for i in range(n):
        p = clamp((t - t0 - step * i) / 0.18)
        if p <= 0:
            continue
        cx = x + (i % cols) * size * (1 + gap)
        cy = y + (i // cols) * size * 1.9
        c = RED if (i in red and red_at is not None and t >= red_at) else color
        person(cr, cx, cy + 20 * (1 - p), size * 1.7, c, p)


def calendar(cr, t, t0, x, y, pages, title, interval=0.4, w=340, h=360, circle_last=True):
    """Tear-off calendar: pages[0] shows first; each next page appears as the previous tears off and falls."""
    def page(label, alpha=1.0):
        cr.set_source_rgba(0.95, 0.92, 0.85, alpha)
        cr.rectangle(-w / 2, -h / 2, w, h)
        cr.fill()
        cr.set_source_rgba(*RED, alpha)
        cr.rectangle(-w / 2, -h / 2, w, 70)
        cr.fill()
        draw_text(cr, title.upper(), 0, -h / 2 + 35, 30, (0.97, 0.94, 0.88), alpha, MONO_FONT, "cm", tracking=3)
        draw_text(cr, label, 0, 25, 96 if len(label) < 8 else 70, INK, alpha, HEAD_FONT, "cm")
        cr.set_source_rgba(*INK, alpha)
        for dx in (-w / 4, w / 4):
            cr.arc(dx, -h / 2, 9, 0, 2 * math.pi)
            cr.fill()
    k = int(clamp((t - t0) / interval, 0, len(pages) - 1)) if t >= t0 else 0
    p_in = prog(t, t0 - 0.3, 0.3)
    cr.save()
    cr.translate(x, y)
    cr.set_source_rgba(0, 0, 0, 0.2 * p_in)
    cr.rectangle(-w / 2 + 8, -h / 2 + 14, w, h)
    cr.fill()
    page(pages[min(k + 1, len(pages) - 1)] if k + 1 < len(pages) and t >= t0 else pages[k], p_in)
    if t >= t0 and k + 1 < len(pages):
        f = clamp((t - t0 - k * interval) / interval)          # the current page tears off and falls
        cr.save()
        cr.translate(60 * f, 260 * f * f)
        cr.rotate(0.5 * f)
        page(pages[k], 1 - f * 0.7)
        cr.restore()
    cr.restore()
    if circle_last and k == len(pages) - 1 and t >= t0:
        ring(cr, x, y + 25, w * 0.42, 80, prog(t, t0 + interval * (len(pages) - 1) + 0.1, 0.4))


GREEN = (0.20, 0.55, 0.30)      # reassurance accent (the reference's HIV reel: IS NORMAL, LONG LIFE...)
GOLD = (0.85, 0.58, 0.16)       # big closing numbers


def rule(cr, alpha=1.0, y=162, color=INK):
    """The bare header rule (HIV / chickenpox style: no section label, no FIG number)."""
    cr.set_source_rgba(*color, 0.5 * alpha)
    cr.set_line_width(2)
    cr.move_to(MARGIN, y)
    cr.line_to(W - MARGIN, y)
    cr.stroke()


def parasite(cr, x, y, s, rot=0.0, color=(0.55, 0.30, 0.62), alpha=1.0, wobble=0.0):
    """Flat textbook Toxoplasma tachyzoite: a crescent/banana cell with a nucleus and an apical tip."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot + 0.12 * math.sin(wobble))
    cr.scale(s / 100, s / 100)
    cr.move_to(-50, 8)
    cr.curve_to(-40, -34, 30, -40, 52, -6)
    cr.curve_to(40, 4, 10, -14, -20, 2)
    cr.curve_to(-34, 10, -42, 16, -50, 8)
    cr.close_path()
    cr.set_source_rgba(*color, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(0.15, 0.08, 0.18, alpha)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_source_rgba(0.95, 0.85, 0.95, 0.9 * alpha)
    cr.arc(-6, -10, 9, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.15, 0.08, 0.18, alpha)
    cr.arc(46, -8, 4, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def cyst(cr, x, y, r, t=0.0, alpha=1.0, n=14):
    """Tissue cyst: a pale round wall packed with small crescents (sleeping parasites)."""
    cr.set_source_rgba(0.97, 0.92, 0.95, 0.95 * alpha)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill_preserve()
    cr.set_source_rgba(0.45, 0.20, 0.50, alpha)
    cr.set_line_width(max(3, r * 0.06))
    cr.stroke()
    rng = np.random.default_rng(int(x * 7 + y))
    for i in range(n):
        a, d = rng.uniform(0, 6.28), rng.uniform(0, r * 0.7)
        parasite(cr, x + d * math.cos(a), y + d * math.sin(a), r * 0.42, rng.uniform(0, 6.28), alpha=alpha,
                 wobble=t * 2 + i)


def strings(cr, t, t0, points, bar=(540, 360), alpha=1.0, sway=0.0):
    """Marionette control bar with strings drawn down to `points` (the puppeteer metaphor), dropping in at t0."""
    p = prog(t, t0, 0.4)
    if p <= 0:
        return
    bx, by = bar[0] + 30 * math.sin(sway), bar[1] - 200 * (1 - p)
    cr.set_source_rgba(0.42, 0.28, 0.16, alpha * p)
    cr.set_line_width(16)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(bx - 170, by)
    cr.line_to(bx + 170, by)
    cr.stroke()
    cr.move_to(bx, by - 60)
    cr.line_to(bx, by + 60)
    cr.stroke()
    q = prog(t, t0 + 0.25, 0.45)
    cr.set_line_width(2.5)
    cr.set_source_rgba(0.92, 0.90, 0.85, 0.9 * alpha * q)
    for i, (px, py) in enumerate(points):
        sx = bx - 150 + 300 * i / max(1, len(points) - 1)
        cr.move_to(sx, by)
        cr.line_to(sx + (px - sx) * q, by + (py - by) * q)
        cr.stroke()


def yes_no_card(cr, t, t0, x, y, w=620, h=300, question="TELL US IN THE COMMENTS"):
    """Kraft card with two boxes; a red circle switches between YES and NO (chickenpox-style ending)."""
    p = clamp((t - t0) / 0.35)
    if p <= 0:
        return
    yy = y + 160 * (1 - back(p))
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.02)
    cr.set_source_rgba(0, 0, 0, 0.22 * p)
    _round(cr, -w / 2 + 8, -h / 2 + 14, w, h, 18)
    cr.fill()
    cr.set_source_rgba(0.80, 0.68, 0.50, p)
    _round(cr, -w / 2, -h / 2, w, h, 18)
    cr.fill()
    for i, label in enumerate(("YES", "NO")):
        bx = -w / 4 + i * w / 2
        cr.set_source_rgba(*INK, p)
        cr.set_line_width(6)
        cr.rectangle(bx - 120, -70, 56, 56)
        cr.stroke()
        draw_text(cr, label, bx - 40, -42, 64, INK, p, anchor="lm")
    draw_text(cr, question, 0, 80, 30, INK, p, MONO_FONT, "cm", tracking=2)
    if t > t0 + 0.6:
        side = int((t - t0 - 0.6) / 0.9) % 2
        ring(cr, -w / 4 + side * w / 2 - 40, -42, 150, 70, prog(t, t0 + 0.6 + 0.9 * int((t - t0 - 0.6) / 0.9), 0.35))
    cr.restore()


def gauge(cr, t, t0, x, y, r, v0, v1, labels=("LOW", "HIGH"), alpha=1.0):
    """Half-dial risk gauge; the needle swings from v0 to v1 (0..1 = low..high) after t0."""
    v = v0 + (v1 - v0) * back(clamp((t - t0) / 0.8), 1.2)
    for i in range(30):
        a0 = math.pi + math.pi * i / 30
        f = i / 29
        cr.set_source_rgba(0.2 + 0.6 * f, 0.6 - 0.45 * f, 0.25, alpha)
        cr.set_line_width(r * 0.22)
        cr.arc(x, y, r, a0, a0 + math.pi / 30 + 0.01)
        cr.stroke()
    a = math.pi + math.pi * clamp(v, 0, 1)
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(10)
    cr.move_to(x, y)
    cr.line_to(x + r * 0.95 * math.cos(a), y + r * 0.95 * math.sin(a))
    cr.stroke()
    cr.arc(x, y, 18, 0, 2 * math.pi)
    cr.fill()
    draw_text(cr, labels[0], x - r, y + 30, 34, INK, alpha, MONO_FONT, "ct")
    draw_text(cr, labels[1], x + r, y + 30, 34, INK, alpha, MONO_FONT, "ct")


def header(cr, label, fig, alpha=1.0, y=150, color=INK):
    """Thin rule with a small mono section label (left) and FIG. number (right), like a printed plate."""
    cr.set_source_rgba(*color, 0.55 * alpha)
    cr.set_line_width(2)
    cr.move_to(MARGIN, y + 12)
    cr.line_to(W - MARGIN, y + 12)
    cr.stroke()
    draw_text(cr, label.upper(), MARGIN, y, 22, color, 0.7 * alpha, MONO_FONT, "lb", tracking=3)
    draw_text(cr, f"FIG. {fig}", W - MARGIN, y, 22, color, 0.7 * alpha, MONO_FONT, "rb", tracking=3)


# ---------- headlines ----------

CREAM = (0.93, 0.89, 0.80)      # small headline line on dark grounds
CORAL = (0.95, 0.42, 0.32)      # the "red" line on dark grounds (the reference turns coral/orange on dark)


def headline(cr, t, small, big, t_small, t_big, y=200, x=MARGIN, small_size=64, big_size=150, alpha=1.0,
             big_color=RED, strike_at=None, struck=False, small_color=INK, t_ghost=None):
    """Two-tier headline: small dark setup words revealed one by one from t_small, then the big red word at t_big.
    t_ghost: the big word shows as a faint grey ghost from then until t_big (the reference does this on most hooks).
    strike_at: time a red strike-through starts drawing across the big word. Returns the big word's box.
    A big word wider than the frame is shrunk to fit."""
    if big:
        big_size = min(big_size, int(big_size * (W - 2 * x) / max(1, text_size(big, big_size)[0])))
    if big and t_ghost is not None and t_ghost <= t < t_big:
        draw_text(cr, big, x, y + small_size * 1.18, big_size, FADED, 0.35 * alpha * prog(t, t_ghost, 0.25))
    words = small.split()
    cx = x
    gap = small_size * 0.28
    for k, word in enumerate(words):
        p = prog(t, t_small + 0.09 * k, 0.25)
        if p <= 0:
            break
        _, _, w, _ = draw_text(cr, word, cx, y + 18 * (1 - p), small_size, small_color, p * alpha)
        cx += w + gap
    by = y + small_size * 1.18
    p = prog(t, t_big, 0.3)
    box = None
    if p > 0:
        s = 1.12 - 0.12 * back(clamp((t - t_big) / 0.3))
        bw, bh = text_size(big, big_size)
        cr.save()
        cr.translate(x, by + bh / 2)
        cr.scale(s, s)
        color = FADED if struck and strike_at is not None and t >= strike_at else big_color
        draw_text(cr, big, 0, -bh / 2, big_size, color, p * alpha)
        cr.restore()
        box = (x, by, bw, bh)
        if strike_at is not None and t >= strike_at:
            strike(cr, x - 10, by + bh * 0.55, x + bw + 14, by + bh * 0.48, prog(t, strike_at, 0.35), alpha=alpha)
    return box


def stamp(cr, t, text, t0, x, y, size=46, color=RED, rot=-0.06, alpha=1.0):
    """Rubber-stamp word in a box that thumps in."""
    p = clamp((t - t0) / 0.22)
    if p <= 0:
        return
    s = 1.6 - 0.6 * back(p, 2.2)
    w, h = text_size(text, size, tracking=4)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*color, 0.85 * alpha * p)
    cr.set_line_width(5)
    cr.rectangle(-w / 2 - 22, -h / 2 - 16, w + 44, h + 32)
    cr.stroke()
    draw_text(cr, text, 0, 0, size, color, 0.9 * alpha * p, anchor="cm", tracking=4)
    cr.restore()


# ---------- red marks ----------

def _brush(cr, color, width, alpha):
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(width)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)


def strike(cr, x0, y0, x1, y1, p, width=14, color=RED, alpha=1.0):
    if p <= 0:
        return
    _brush(cr, color, width, 0.92 * alpha)
    cr.move_to(x0, y0)
    cr.line_to(x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)
    cr.stroke()


def tick(cr, x, y, size, p, color=RED, alpha=1.0):
    if p <= 0:
        return
    pts = [(x, y), (x + 0.35 * size, y + 0.4 * size), (x + size, y - 0.55 * size)]
    _brush(cr, color, size * 0.12, alpha)
    l1 = math.dist(pts[0], pts[1])
    l2 = math.dist(pts[1], pts[2])
    d = p * (l1 + l2)
    cr.move_to(*pts[0])
    if d <= l1:
        f = d / l1
        cr.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * f, pts[0][1] + (pts[1][1] - pts[0][1]) * f)
    else:
        cr.line_to(*pts[1])
        f = (d - l1) / l2
        cr.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * f, pts[1][1] + (pts[2][1] - pts[1][1]) * f)
    cr.stroke()


def cross(cr, x, y, size, p, color=RED, alpha=1.0):
    strike(cr, x - size / 2, y - size / 2, x + size / 2, y + size / 2, clamp(p * 2), size * 0.13, color, alpha)
    strike(cr, x + size / 2, y - size / 2, x - size / 2, y + size / 2, clamp(p * 2 - 1), size * 0.13, color, alpha)


def ring(cr, cx, cy, rx, ry, p, width=9, color=RED, alpha=1.0):
    """Hand-drawn ellipse that overshoots its start a little, drawn over time."""
    if p <= 0:
        return
    _brush(cr, color, width, 0.9 * alpha)
    a0, span = -2.2, 2 * math.pi + 0.5
    n = max(2, int(80 * p))
    for i in range(n + 1):
        a = a0 + span * p * i / n
        wob = 1 + 0.04 * math.sin(3 * a + 1.3)
        px, py = cx + rx * wob * math.cos(a), cy + ry * wob * math.sin(a)
        (cr.move_to if i == 0 else cr.line_to)(px, py)
    cr.stroke()


def path(cr, pts, p, width=6, color=INK, alpha=1.0, dash=None, arrow=False):
    """Polyline revealed along its length (p 0..1), optional arrowhead at the moving tip."""
    if p <= 0 or len(pts) < 2:
        return
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(lens)
    d = total * clamp(p)
    _brush(cr, color, width, alpha)
    if dash:
        cr.set_dash(dash)
    cr.move_to(*pts[0])
    tip, prev = pts[0], pts[0]
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        if d <= 0:
            break
        f = min(1.0, d / L) if L else 1.0
        tip = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        prev = a
        cr.line_to(*tip)
        d -= L
    cr.stroke()
    cr.set_dash([])
    if arrow:
        ang = math.atan2(tip[1] - prev[1], tip[0] - prev[0])
        s = width * 3.2
        cr.move_to(tip[0] + s * math.cos(ang), tip[1] + s * math.sin(ang))
        cr.line_to(tip[0] + s * math.cos(ang + 2.5), tip[1] + s * math.sin(ang + 2.5))
        cr.line_to(tip[0] + s * math.cos(ang - 2.5), tip[1] + s * math.sin(ang - 2.5))
        cr.close_path()
        cr.fill()


def _along(pts, p):
    """Point at fraction p of a polyline's length."""
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    d = sum(lens) * clamp(p)
    for (a, b), L in zip(zip(pts, pts[1:]), lens):
        if d <= L and L:
            return a[0] + (b[0] - a[0]) * d / L, a[1] + (b[1] - a[1]) * d / L
        d -= L
    return pts[-1]


def erase(cr, t, t0, text, x, y, size, color=INK, dur=0.9, eraser=None, ghost=0.12, anchor="lt"):
    """A word rubbed out by an eraser (the Toxoplasma metaphor, "dar mita deta hai"): zig-zag strokes clear it left to
    right, leaving a faint smudge and crumbs below. `eraser` = cut-out photo drawn at the stroke head (flat pink block
    if None)."""
    s, pad = text_surface(text, size, color)
    w, h = s.get_width() - 2 * pad, s.get_height() - 2 * pad
    x0 = x + {"l": 0, "c": -w / 2, "r": -w}[anchor[0]]
    y0 = y + {"t": 0, "m": -h / 2, "b": -h}[anchor[1]]
    p = clamp((t - t0) / dur)
    n = max(3, int(w / (h * 0.3)))
    pts = [(x0 - 12 + (w + 24) * i / n, y0 + (h + 14 if i % 2 else -14)) for i in range(n + 1)]
    cr.push_group()
    draw_text(cr, text, x0, y0, size, color)
    cr.set_operator(cairo.OPERATOR_DEST_OUT)
    if p >= 1:
        cr.set_source_rgba(0, 0, 0, 1 - ghost)
        cr.rectangle(x0 - pad, y0 - pad, w + 2 * pad, h + 2 * pad)
        cr.fill()
    else:
        path(cr, pts, p, width=h * 0.7, color=(0, 0, 0), alpha=1 - ghost)
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.pop_group_to_source()
    cr.paint()
    rng = np.random.default_rng(sum(map(ord, text)))
    for u, dy, r in zip(rng.random(22), rng.random(22), rng.random(22)):
        if u < p:                                          # crumbs where the eraser has passed
            cr.set_source_rgba(0.78, 0.55, 0.52, 0.75)
            cr.arc(x0 + w * u, y0 + h + 12 + 50 * dy, 3 + 4 * r, 0, 2 * math.pi)
            cr.fill()
    a = window(t, t0 - 0.2, t0 + dur + 0.3, 0.2)
    if a <= 0:
        return
    ex, ey = _along(pts, p)
    ey -= 80 * clamp((t - t0 - dur) / 0.3)                 # lifts off when done
    eh = h * 1.0
    if eraser:
        photo(cr, eraser, ex, ey - eh * 0.25, eh, alpha=a, rot=-0.45)
    else:
        cr.save()
        cr.translate(ex, ey - eh * 0.25)
        cr.rotate(-0.45)
        _round(cr, -eh * 0.3, -eh * 0.5, eh * 0.6, eh, eh * 0.12)
        cr.set_source_rgba(0.93, 0.60, 0.60, a)
        cr.fill()
        cr.rectangle(-eh * 0.3, -eh * 0.5, eh * 0.6, eh * 0.45)
        cr.set_source_rgba(0.22, 0.36, 0.62, a)
        cr.fill()
        cr.restore()


# ---------- photo cut-outs ----------

@functools.lru_cache(maxsize=64)
def _cutout(path_, max_side=1400, tint=None):
    img = Image.open(path_).convert("RGBA")
    img.thumbnail((max_side, max_side), Image.LANCZOS)
    if tint is not None:                                   # flat colour silhouette from the alpha
        r, g, b = (int(c * 255) for c in tint)
        flat = Image.new("RGBA", img.size, (r, g, b, 255))
        flat.putalpha(img.getchannel("A"))
        img = flat
    a = img.getchannel("A")
    pad = 60
    sh = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    blur = Image.new("L", sh.size, 0)
    blur.paste(a, (pad, pad))
    blur = blur.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.42))
    sh.putalpha(blur)
    return to_surface(img), to_surface(sh), pad


def photo(cr, path_, cx, cy, height, alpha=1.0, rot=0.0, shadow=True, flip=False, tint=None, shadow_dy=22):
    """Draw a cut-out centred at (cx, cy) scaled to `height` px, with a soft drop shadow on the paper."""
    if alpha <= 0:
        return
    surf, sh, pad = _cutout(path_, tint=tint)
    s = height / surf.get_height()
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.scale(-s if flip else s, s)
    if shadow:
        cr.set_source_surface(sh, -surf.get_width() / 2 - pad + 6, -surf.get_height() / 2 - pad + shadow_dy / s)
        cr.paint_with_alpha(alpha)
    cr.set_source_surface(surf, -surf.get_width() / 2, -surf.get_height() / 2)
    cr.paint_with_alpha(alpha)
    cr.restore()


def photo_width(path_, height):
    surf, _, _ = _cutout(path_)
    return surf.get_width() * height / surf.get_height()


def framed_photo(cr, path_, cx, cy, w, h, alpha=1.0, rot=0.0):
    """A rectangular plate (micrograph) with a thin dark frame and a shadow, cropped to cover w x h."""
    surf, _, _ = _cutout(path_, max_side=1200)
    s = max(w / surf.get_width(), h / surf.get_height())
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha)
    cr.rectangle(-w / 2 + 8, -h / 2 + 16, w, h)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.clip()
    cr.scale(s, s)
    cr.set_source_surface(surf, -surf.get_width() / 2, -surf.get_height() / 2)
    cr.paint_with_alpha(alpha)
    cr.reset_clip()
    cr.restore()
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.set_line_width(6)
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.stroke()
    cr.restore()


# ---------- cards, labels, counters ----------

def _torn_rect(cr, x, y, w, h, seed):
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(13):
        pts.append((x + w * i / 12, y + rng.uniform(-3, 3)))
    for i in range(1, 7):
        pts.append((x + w + rng.uniform(-3, 3), y + h * i / 6))
    for i in range(11, -1, -1):
        pts.append((x + w * i / 12, y + h + rng.uniform(-3, 3)))
    for i in range(5, 0, -1):
        pts.append((x + rng.uniform(-3, 3), y + h * i / 6))
    cr.move_to(*pts[0])
    for pt in pts[1:]:
        cr.line_to(*pt)
    cr.close_path()


def card(cr, t, t0, x, y, lines, w=None, size=34, seed=3, alpha=1.0, rot=-0.02, color=INK, pin_line=None):
    """Torn paper label. lines: [text, ...]; the first line is the main one, later lines smaller and faded.
    It drops in at t0. pin_line: (x, y) point on the subject that a thin leader line points to."""
    p = clamp((t - t0) / 0.3)
    if p <= 0:
        return
    sizes = [size] + [int(size * 0.62)] * (len(lines) - 1)
    widths = [text_size(s, z, MONO_FONT, 2)[0] for s, z in zip(lines, sizes)]
    w = w or max(widths) + 56
    h = sum(z * 1.35 for z in sizes) + 34
    if pin_line:
        path(cr, [(x + w / 2, y), pin_line], ease(p), 2, INK, 0.7 * alpha)
        cr.arc(*pin_line, 6, 0, 2 * math.pi)
        cr.fill()
    cr.save()
    cr.translate(x + w / 2, y + h / 2 + 30 * (1 - back(p)))
    cr.rotate(rot)
    cr.set_source_rgba(0, 0, 0, 0.18 * alpha * p)
    _torn_rect(cr, -w / 2 + 5, -h / 2 + 9, w, h, seed)
    cr.fill()
    cr.set_source_rgba(0.93, 0.89, 0.80, alpha * p)
    _torn_rect(cr, -w / 2, -h / 2, w, h, seed)
    cr.fill()
    yy = -h / 2 + 17
    for k, (s, z) in enumerate(zip(lines, sizes)):
        draw_text(cr, s, -w / 2 + 28, yy, z, color if k == 0 else FADED, alpha * p, MONO_FONT, tracking=2)
        yy += z * 1.35
    cr.restore()


def counter(cr, t, t0, x, y, text, size=120, alpha=1.0, color=INK, anchor="c"):
    """Flip-card counter: each character sits on its own dark card and flips in, left to right."""
    cw, ch = size * 0.66, size * 1.18
    gap = size * 0.08
    n = len(text)
    total = n * cw + (n - 1) * gap
    x0 = x - total / 2 if anchor == "c" else x
    for i, c in enumerate(text):
        p = clamp((t - t0 - 0.06 * i) / 0.22)
        if p <= 0:
            continue
        cx = x0 + i * (cw + gap)
        if c == " ":
            continue
        squash = abs(math.cos((1 - p) * math.pi / 2)) if p < 1 else 1
        cr.save()
        cr.translate(cx + cw / 2, y)
        cr.scale(1, max(0.05, squash))
        cr.set_source_rgba(*INK, 0.92 * alpha)
        cr.rectangle(-cw / 2, -ch / 2, cw, ch)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.12 * alpha)
        cr.set_line_width(2)
        cr.move_to(-cw / 2, 0)
        cr.line_to(cw / 2, 0)
        cr.stroke()
        draw_text(cr, c, 0, 0, size, (0.95, 0.91, 0.82), alpha, HEAD_FONT, "cm")
        cr.restore()


def push(cr, t, t0, t1, z0=1.0, z1=1.06, cx=W / 2, cy=H * 0.55):
    """Slow push-in for a scene: call inside cr.save()/restore() before drawing the scene's layers."""
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.01, t1 - t0))
    cr.translate(cx, cy)
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ---------- simple silhouettes ----------

def person(cr, x, y, h, color=INK, alpha=1.0):
    """Standing figure, feet at (x, y)."""
    cr.set_source_rgba(*color, alpha)
    head = h * 0.13
    cr.arc(x, y - h + head, head, 0, 2 * math.pi)
    cr.fill()
    bw = h * 0.30
    top = y - h + 2.25 * head
    cr.move_to(x - bw / 2, top + h * 0.06)
    cr.curve_to(x - bw / 2, top - h * 0.02, x + bw / 2, top - h * 0.02, x + bw / 2, top + h * 0.06)
    cr.line_to(x + bw * 0.42, y - h * 0.38)
    cr.line_to(x + bw * 0.30, y)
    cr.line_to(x + bw * 0.06, y)
    cr.line_to(x, y - h * 0.30)
    cr.line_to(x - bw * 0.06, y)
    cr.line_to(x - bw * 0.30, y)
    cr.line_to(x - bw * 0.42, y - h * 0.38)
    cr.close_path()
    cr.fill()


def head_profile(cr, cx, cy, s, color=INK, alpha=1.0, fill=False):
    """Side-view head outline facing right, centred near the brain; s = overall height."""
    cr.save()
    cr.translate(cx, cy)
    cr.scale(s / 100, s / 100)
    cr.move_to(-30, 50)
    cr.curve_to(-48, 30, -52, -25, -30, -42)
    cr.curve_to(-12, -56, 26, -54, 38, -30)
    cr.curve_to(44, -18, 42, -8, 44, 0)
    cr.line_to(52, 12)
    cr.line_to(44, 16)
    cr.curve_to(46, 24, 44, 30, 38, 32)
    cr.curve_to(36, 40, 26, 42, 16, 40)
    cr.line_to(14, 52)
    cr.restore()
    cr.set_source_rgba(*color, alpha)
    if fill:
        cr.fill()
    else:
        cr.set_line_width(7)
        cr.stroke()


def blob(cr, cx, cy, r, seed, color, alpha=1.0, fill=True, width=4):
    """Irregular round cell / cyst."""
    rng = np.random.default_rng(seed)
    k = rng.uniform(0.06, 0.14, 5)
    ph = rng.uniform(0, 6.28, 5)
    n = 48
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        rr = r * (1 + sum(k[j] * math.sin((j + 2) * a + ph[j]) for j in range(5)) * 0.5)
        (cr.move_to if i == 0 else cr.line_to)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    cr.close_path()
    cr.set_source_rgba(*color, alpha)
    if fill:
        cr.fill()
    else:
        cr.set_line_width(width)
        cr.stroke()


def phone_comments(cr, t, t0, cx, cy, h=760, alpha=1.0, reply="HAAN, MERE GHAR MEIN BHI!"):
    """A hand-less phone showing a comments sheet; a reply types itself in from t0 + 0.6."""
    p = prog(t, t0, 0.4)
    if p <= 0:
        return
    w = h * 0.5
    y = cy + 80 * (1 - p)
    cr.save()
    cr.translate(cx, y)
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha * p)
    _round(cr, -w / 2 + 10, -h / 2 + 22, w, h, 46)
    cr.fill()
    cr.set_source_rgba(0.1, 0.09, 0.08, alpha * p)
    _round(cr, -w / 2, -h / 2, w, h, 46)
    cr.fill()
    sw, sh_ = w - 36, h - 36
    cr.set_source_rgba(0.96, 0.94, 0.89, alpha * p)
    _round(cr, -sw / 2, -sh_ / 2, sw, sh_, 32)
    cr.fill()
    draw_text(cr, "Comments", -sw / 2 + 30, -sh_ / 2 + 34, 30, INK, alpha * p, MONO_FONT)
    cols = [(0.86, 0.33, 0.25), (0.25, 0.55, 0.75), (0.36, 0.65, 0.35), (0.90, 0.62, 0.20), (0.55, 0.40, 0.70)]
    for i in range(5):
        yy = -sh_ / 2 + 120 + i * 92
        cr.set_source_rgba(*cols[i], alpha * p)
        cr.arc(-sw / 2 + 52, yy + 16, 18, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(*INK, 0.55 * alpha * p)
        cr.rectangle(-sw / 2 + 88, yy, sw * (0.45 + 0.08 * (i % 3)), 12)
        cr.fill()
        cr.set_source_rgba(*INK, 0.25 * alpha * p)
        cr.rectangle(-sw / 2 + 88, yy + 24, sw * (0.30 + 0.1 * ((i + 1) % 3)), 10)
        cr.fill()
    n = int(clamp((t - t0 - 0.6) / 1.2) * len(reply))
    bx, by = -sw / 2 + 20, sh_ / 2 - 120
    cr.set_source_rgba(1, 1, 1, alpha * p)
    _round(cr, bx, by, sw - 40, 76, 38)
    cr.fill()
    draw_text(cr, reply[:n] + ("|" if n < len(reply) and int(t * 3) % 2 == 0 else ""), bx + 26, by + 38, 24, INK,
              alpha * p, MONO_FONT, "lm")
    cr.restore()


def _round(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()
