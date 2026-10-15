"""Thriller kit for the Milo series: film-like still shots brought to life.

Shots are made locally and free (tools/shots.py) and kept in assets/milo/shots/. Here they get a film grade
(crushed blacks, teal shadows, warm highlights), slow camera creep with a little handheld drift, shake and flashes on
the shocks, flicker, grain and a heavy vignette. Text the image model can't draw (phone texts, notes, choice cards,
the hook line, captions) is drawn crisp on top.

Pacing taken from the owner's reference ("That's Not My Dad"): a new shot about every 2 s and the camera never still.
"""
import math
import os

import numpy as np

from .engine import ROOT, W, H, cairo, clamp01, cue, hexc, seg
from .polish import rrect, text_path, text_width

SHOTS = os.path.join(ROOT, "assets", "milo", "shots")
HOOK = "Anton"
MARKER = "Permanent Marker"
UI = "Liberation Sans"
RED = hexc("#ff2b2b")
WHITE = (1, 1, 1, 1)
_img = {}


def _grade(a):
    """Film grade on an RGB float image (0..1): crush blacks, a little contrast, teal shadows, warm highlights."""
    a = np.clip((a - 0.025) / 0.975, 0, 1) ** 1.08
    lum = a @ np.array([0.299, 0.587, 0.114])
    a = lum[..., None] + (a - lum[..., None]) * 0.88                 # slightly less colour
    sh = (1 - lum)[..., None] ** 2
    hi = lum[..., None] ** 2
    a = a + sh * np.array([-0.025, 0.012, 0.035]) + hi * np.array([0.03, 0.012, -0.02])
    return np.clip(a, 0, 1)


def image(name):
    """The graded shot as a cairo surface, 2x the generated size (cached per process)."""
    s = _img.get(name)
    if s is None:
        from PIL import Image, ImageFilter
        path = next(os.path.join(SHOTS, name + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(SHOTS, name + e)))
        im = Image.open(path).convert("RGB")
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
        a = _grade(np.asarray(im, np.float32) / 255)
        h, w = a.shape[:2]
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        buf = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())
        buf[:, :w, 2::-1] = (a * 255 + 0.5).astype(np.uint8)          # BGRA in memory
        buf[:, :w, 3] = 255
        s.mark_dirty()
        _img[name] = s
    return s


def _noise(t, seed, freqs=(0.31, 0.53, 0.97)):
    return sum(math.sin(t * f * 2 * math.pi + seed * (k + 1) * 1.7) / (k + 1) for k, f in enumerate(freqs)) / 1.8


def shot(cr, name, t, t0, t1, move="push", focus=(0.5, 0.45), zoom=(1.04, 1.16), shake=0.0, bright=1.0, lift=0.0):
    """Draw a shot filling the frame. `move`: push (creep in), pull (creep out), left/right/up/down (drift), hold.
    `focus`: where the push heads, as fractions of the image. `shake`: handheld shake strength (shocks)."""
    surf = image(name)
    iw, ih = surf.get_width(), surf.get_height()
    p = clamp01((t - t0) / max(0.1, t1 - t0))
    p = p * p * (3 - 2 * p) * 0.6 + p * 0.4                             # mostly steady creep, soft start and end
    z0, z1 = zoom
    z = {"push": z0 + (z1 - z0) * p, "pull": z1 - (z1 - z0) * p}.get(move, (z0 + z1) / 2)
    base = max(W / iw, H / ih)
    sc = base * z
    fx, fy = focus
    dx = {"left": 0.5 - 0.06 * p, "right": 0.5 + 0.06 * p}.get(move, 0.5 + (fx - 0.5) * p * 0.5)
    dy = {"up": 0.5 - 0.05 * p, "down": 0.5 + 0.05 * p}.get(move, 0.5 + (fy - 0.5) * p * 0.5)
    jx = 3.0 * _noise(t, 1) + shake * 18 * _noise(t * 9, 3)
    jy = 3.0 * _noise(t, 2) + shake * 18 * _noise(t * 9, 4)
    rot = 0.004 * _noise(t, 5) + shake * 0.012 * _noise(t * 7, 6)
    cr.save()
    cr.translate(W / 2 + jx, H / 2 + jy)
    cr.rotate(rot)
    cr.scale(sc, sc)
    vw, vh = W / sc, H / sc                                             # visible part of the image, in image px
    cx = min(max(dx * iw, vw / 2 + 6 / sc), iw - vw / 2 - 6 / sc)
    cy = min(max(dy * ih, vh / 2 + 6 / sc), ih - vh / 2 - 6 / sc)
    cr.translate(-cx, -cy)
    cr.set_source_surface(surf, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    if lift:                                                            # brighten a very dark shot
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_source_surface(surf, 0, 0)
        cr.paint_with_alpha(lift)
    cr.restore()
    if bright < 1:
        cr.set_source_rgba(0, 0, 0, 1 - bright)
        cr.paint()


class Plan:
    """The edit: [(start time, shot name, options)], each shot running until the next one starts."""

    def __init__(self, cuts, total):
        self.cuts = sorted(cuts, key=lambda c: c[0])
        self.total = total

    def draw(self, cr, t):
        for i, (t0, name, opt) in enumerate(self.cuts):
            t1 = self.cuts[i + 1][0] if i + 1 < len(self.cuts) else self.total
            if t0 <= t < t1 or (i == 0 and t < t0):
                shot(cr, name, t, t0, t1, **opt)
                if opt.get("shake") and t - t0 < 0.5:
                    pass
                return t0, name


def finish(cr, t, flicker=0.0, vig=0.62):
    """Whole-frame film finish: flicker, vignette, grain."""
    if flicker:
        f = clamp01(0.5 + 0.5 * math.sin(t * 37) * math.sin(t * 13.3 + 1) + 0.3 * math.sin(t * 71))
        cr.set_source_rgba(0, 0, 0, flicker * f)
        cr.paint()
    g = cairo.RadialGradient(W / 2, H * 0.45, H * 0.18, W / 2, H * 0.48, H * 0.78)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, vig)
    cr.set_source(g)
    cr.paint()
    grain(cr, t)


_grain = []


def grain(cr, t, a=0.075):
    if not _grain:
        rng = np.random.default_rng(3)
        for _ in range(6):
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2)
            buf = np.ndarray((H // 2, s.get_stride() // 4, 4), np.uint8, s.get_data())
            v = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
            buf[:, :W // 2, 0] = buf[:, :W // 2, 1] = buf[:, :W // 2, 2] = v
            buf[:, :W // 2, 3] = 255
            s.mark_dirty()
            _grain.append(s)
    cr.save()
    cr.scale(2, 2)
    cr.set_source_surface(_grain[int(t * 24) % len(_grain)], 0, 0)
    cr.set_operator(cairo.OPERATOR_OVERLAY)
    cr.paint_with_alpha(a)
    cr.restore()


def flash(cr, t, at, col=(1, 1, 1), dur=0.18, a=0.85):
    """A hard flash on a shock or a cut (white = shock, black = dread)."""
    if at <= t < at + dur:
        cr.set_source_rgba(*col, a * (1 - (t - at) / dur))
        cr.paint()


def glow(cr, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col[:3], a)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()


# ---------------------------------------------------------------- text on top
def _text(cr, s, x, y, size, col, font, align="center", ow=None, shadow=0.6):
    ow = size * 0.12 if ow is None else ow
    text_path(cr, s, x + size * 0.03, y + size * 0.06, size, font, align)
    cr.set_source_rgba(0, 0, 0, shadow)
    cr.set_line_width(ow * 1.4)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke_preserve()
    cr.fill()
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(0, 0, 0, 1)
    cr.set_line_width(ow)
    cr.stroke()
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(*col)
    cr.fill()


def hook(cr, t, lines, end, y=250, size=86):
    """The hook in big type from frame 0 (no fade in): `lines` = [(text, red?)], one per line. Shudders a little."""
    if t >= end + 0.25:
        return
    a = 1.0 if t < end else 1 - (t - end) / 0.25
    cr.save()
    cr.push_group()
    for k, (s, red) in enumerate(lines):
        sz = size
        wd = text_width(cr, s, sz, HOOK)
        if wd > W - 70:
            sz *= (W - 70) / wd
        jx = 1.5 * math.sin(t * 41 + k) if red else 0
        _text(cr, s, W / 2 + jx, y + k * size * 1.08, sz, RED if red else WHITE, HOOK)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def captions(cr, t, tl, y=930, size=64, max_w=600):
    """Thriller captions: 1-3 words in Anton, white, the word being spoken in red."""
    from .captions import _chunks
    chunks = _caps.get(id(tl))
    if chunks is None:
        chunks = _caps[id(tl)] = _chunks(tl)
    for i, ch in enumerate(chunks):
        start = ch[0].start
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else tl.total
        stop = nxt if nxt - ch[-1].end < 0.5 else ch[-1].end + 0.25
        if start - 0.02 <= t < stop:
            words = [u.shown.rstrip(",;:").upper() for u in ch]
            space = text_width(cr, " ", size, HOOK)
            widths = [text_width(cr, w, size, HOOK) for w in words]
            total = sum(widths) + space * (len(words) - 1)
            sz = size * min(1, max_w / total)
            k = 0.9 + 0.1 * clamp01((t - start) / 0.1)
            cr.save()
            cr.translate(W / 2, y)
            cr.scale(k, k)
            x = -total * sz / size / 2
            for wd, w, u in zip(widths, words, ch):
                col = RED if u.start - 0.03 <= t < u.end + 0.05 else WHITE
                _text(cr, w, x, 0, sz, col, HOOK, align="left", ow=sz * 0.14)
                x += (wd + space) * sz / size
            cr.restore()
            return


_caps = {}


def phone(cr, t, start, sender, msg, y=330, typing=0.7, end=None):
    """A phone screen sliding up with a text arriving: '...' typing, then the message."""
    if t < start or (end is not None and t > end + 0.3):
        return
    a = clamp01((t - start) / 0.25) * (1 if end is None or t < end else 1 - (t - end) / 0.3)
    up = (1 - clamp01((t - start) / 0.3)) ** 2 * 260
    cr.save()
    cr.translate(0, up)
    cr.push_group()
    x0, w, h = 110, W - 220, 480
    glow(cr, W / 2, y + h / 2, 420, (0.5, 0.7, 1.0), 0.18)
    rrect(cr, x0, y, w, h, 56)
    cr.set_source_rgba(0.04, 0.05, 0.07, 0.96)
    cr.fill_preserve()
    cr.set_source_rgba(0.25, 0.27, 0.32, 1)
    cr.set_line_width(6)
    cr.stroke()
    cr.set_source_rgba(1, 1, 1, 0.9)
    _plain(cr, sender, W / 2, y + 86, 34, UI)
    cr.set_source_rgba(1, 1, 1, 0.35)
    cr.rectangle(x0 + 30, y + 112, w - 60, 2)
    cr.fill()
    bx, by = x0 + 34, y + 150
    if t < start + typing:
        rrect(cr, bx, by, 130, 70, 34)
        cr.set_source_rgba(0.2, 0.21, 0.24, 1)
        cr.fill()
        for k in range(3):
            on = 0.4 + 0.6 * clamp01(math.sin((t - start) * 9 - k * 0.9))
            cr.arc(bx + 36 + k * 30, by + 35, 9, 0, 2 * math.pi)
            cr.set_source_rgba(1, 1, 1, on)
            cr.fill()
    else:
        cue("buzz", t, start + typing)
        lines = _wrap(cr, msg, 40, UI, w - 120)
        bh = 40 + 50 * len(lines)
        rrect(cr, bx, by, w - 68, bh, 30)
        cr.set_source_rgba(0.2, 0.21, 0.24, 1)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 1)
        for k, line in enumerate(lines):
            _plain(cr, line, bx + 28, by + 60 + 50 * k, 40, UI, "left")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def _plain(cr, s, x, y, size, font, align="center"):
    text_path(cr, s, x, y, size, font, align)
    cr.fill()


def _wrap(cr, s, size, font, max_w):
    lines, cur = [], ""
    for w in s.split():
        nxt = (cur + " " + w).strip()
        if cur and text_width(cr, nxt, size, font) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = nxt
    return lines + [cur] if cur else lines


def note(cr, t, words, y=470, size=96, rot=-0.04):
    """A handwritten note pressed to glass: `words` = [(text, time it appears)]."""
    shown = [w for w, at in words if t >= at]
    if not shown:
        return
    cr.save()
    cr.translate(W / 2, y)
    cr.rotate(rot)
    rrect(cr, -250, -190, 500, 380, 8)
    cr.set_source_rgba(0.93, 0.91, 0.84, 0.96)
    cr.fill()
    for k, w in enumerate(shown):
        cr.set_source_rgba(0.08, 0.05, 0.05, 1)
        _plain(cr, w, 0, -70 + k * 110, size, MARKER)
    cr.restore()


def choice(cr, t, start, a_text, b_text, count_from=None, y=520):
    """The ending: two options and (optionally) a 3-2-1 countdown."""
    if t < start:
        return
    for k, s in enumerate((a_text, b_text)):
        p = clamp01((t - start - 0.15 * k) / 0.25)
        if p <= 0:
            continue
        cy = y + k * 190
        cr.save()
        cr.translate(W / 2, cy)
        cr.scale(0.85 + 0.15 * p, 0.85 + 0.15 * p)
        rrect(cr, -250, -75, 500, 150, 22)
        cr.set_source_rgba(0.05, 0.05, 0.06, 0.85 * p)
        cr.fill_preserve()
        cr.set_source_rgba(*(RED[:3] if k == 0 else (1, 1, 1)), p)
        cr.set_line_width(6)
        cr.stroke()
        cr.set_source_rgba(1, 1, 1, p)
        _plain(cr, s, 0, 30, 84, HOOK)
        cr.restore()
    if count_from is not None and t >= count_from:
        n = 3 - int(t - count_from)
        if n >= 1:
            cue("heartbeat", t, count_from + (3 - n), 0.4)
            ph = (t - count_from) % 1
            cr.save()
            cr.translate(W / 2, y - 200)
            cr.scale(1.3 - 0.3 * min(1, ph * 4), 1.3 - 0.3 * min(1, ph * 4))
            _text(cr, str(n), 0, 40, 130, RED, HOOK)
            cr.restore()
