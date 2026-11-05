"""Scenes for mythology video 2, "Brahma hides the cowherd boys and calves" (videos/brahma_calves.py).

Approach B, a living manuscript: CC0 Indian miniature paintings from the Cleveland Museum of Art, cut into layers
(bc_prep.py: rembg cut-outs, LaMa hole fills) and moved as a multiplane camera, with drawn light, glow, gold dust and
petals, one warm manuscript grade and a gold folio border. Deities are never warped: they only move as whole layers
(drift, parallax, a bow), glow and light.

Every frame is a pure function of t; decoded paintings, scaled copies, glows and textures are cached per process.
"""
import functools
import json
import math
import os

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from channel import ASSETS_ROOT
from poster import (CORAL, CREAM, FPS, HEAD_FONT, MONO_FONT, H, W, _round, back, clamp, draw_text, prog, ring, stamp,
                    strike, text_size, tick, to_surface, yes_no_card)
from shots import T

ART = os.path.join(ASSETS_ROOT, "brahma_calves")
LAYERS = os.path.join(ART, "layers")
CREDITS_FILES = [os.path.join(ART, "credits.json")]

PAINT = dict(
    brahma="cma_162498_brahma_kalighat.jpg", hides="cma_141755_brahma_hides.jpg",
    braj="cma_146117_krishna_returns_braj.jpg", graze="cma_154758_cattle_to_graze.jpg",
    forest="cma_154759_krishna_summons_cows.jpg", malwa="cma_153198_flute_episodes_malwa.jpg",
    friends="cma_145241_friends_of_krishna.jpg", flute="cma_314462_krishna_fluting.jpg",
    yasoda="cma_162465_yasoda_holding.jpg", vishnu="cma_155590_vishnu_garuda.jpg",
    dive="cma_314425_cowherds_dive.jpg", govardhan="cma_162094_govardhan.jpg", nanda="cma_314498_nanda_elders.jpg",
)
USED_ASSETS = sorted(PAINT.values())
P = {k: os.path.join(ART, v) for k, v in PAINT.items()}

GOLD_L = (1.0, 0.84, 0.47)
GOLD = (0.88, 0.66, 0.28)
GOLD_D = (0.62, 0.43, 0.15)


# ---------------------------------------------------------------- timing helpers

def sm(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, u):
    return a + (b - a) * u


def C(tl, bid, hi=None, kn=None, frac=0.5):
    """Cue time: the word (per language) if given and found, otherwise a fraction of the line."""
    word = {"hi": hi, "kn": kn}.get(getattr(tl, "lang", "hi"))
    if word:
        try:
            return T(tl, bid, word)
        except KeyError:
            pass
    return T(tl, bid, frac)


def F(tl, bid, frac):
    return T(tl, bid, frac)


# ---------------------------------------------------------------- images, mip levels

@functools.lru_cache(maxsize=1)
def _index():
    return json.load(open(os.path.join(LAYERS, "index.json"), encoding="utf-8"))


def _path(name):
    p = os.path.join(LAYERS, name + ".png")
    return p if os.path.exists(p) else os.path.join(ART, name)


@functools.lru_cache(maxsize=None)
def _pil(name):
    return Image.open(_path(name)).convert("RGBA")


def dims(name):
    im = _pil(name)
    return im.width, im.height


LEVELS = (1.0, 0.71, 0.5, 0.35, 0.25, 0.18, 0.125, 0.09)


def _level(z):
    for L in reversed(LEVELS):
        if L >= z * 0.97:
            return L
    return 1.0


@functools.lru_cache(maxsize=None)
def surf(name, L):
    im = _pil(name)
    if L != 1.0:
        im = im.resize((max(1, round(im.width * L)), max(1, round(im.height * L))), Image.LANCZOS)
    return to_surface(im)


def _paint_surface(cr, s, L, x, y, alpha=1.0, op=None, filt=cairo.FILTER_GOOD):
    cr.save()
    cr.translate(x, y)
    cr.scale(1 / L, 1 / L)
    cr.set_source_surface(s, 0, 0)
    cr.get_source().set_filter(filt)
    if op is not None:
        cr.set_operator(op)
    if alpha >= 0.999:
        cr.paint()
    elif alpha > 0.002:
        cr.paint_with_alpha(alpha)
    cr.restore()


def blit(cr, name, x, y, z, alpha=1.0, op=None):
    """Draw `name` with its top-left at (x, y) in user space, where one source pixel is about z device pixels."""
    if alpha <= 0.002:
        return
    L = _level(z)
    _paint_surface(cr, surf(name, L), L, x, y, alpha, op)


@functools.lru_cache(maxsize=None)
def silhouette(name, color, L=0.25):
    im = _pil(name)
    a = im.getchannel("A").resize((max(1, round(im.width * L)), max(1, round(im.height * L))), Image.LANCZOS)
    flat = Image.new("RGBA", a.size, tuple(int(c * 255) for c in color) + (255,))
    flat.putalpha(a)
    return to_surface(flat)


@functools.lru_cache(maxsize=None)
def aura(name, color=GOLD_L, L=0.12, spread=0.06):
    """Soft glow from a cut-out's alpha: padded, blurred, tinted. Returns (surface, pad in source px, L)."""
    im = _pil(name)
    a = im.getchannel("A").resize((max(1, round(im.width * L)), max(1, round(im.height * L))), Image.LANCZOS)
    r = max(2, int(max(a.size) * spread))
    pad = 3 * r
    big = Image.new("L", (a.width + 2 * pad, a.height + 2 * pad), 0)
    big.paste(a, (pad, pad))
    big = big.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(r))
    flat = Image.new("RGBA", big.size, tuple(int(c * 255) for c in color) + (255,))
    flat.putalpha(big)
    return to_surface(flat), pad / L, L


@functools.lru_cache(maxsize=None)
def blurred(name, L=0.18, radius=6):
    im = _pil(name)
    im = im.resize((max(1, round(im.width * L)), max(1, round(im.height * L))), Image.LANCZOS)
    pad = radius * 3
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.paste(im, (pad, pad))
    arr = np.asarray(big, np.float32)
    a = arr[..., 3:4] / 255.0
    pre = Image.fromarray(np.clip(np.concatenate([arr[..., :3] * a, arr[..., 3:4]], -1), 0, 255).astype(np.uint8))
    pre = np.asarray(pre.filter(ImageFilter.GaussianBlur(radius)), np.float32)
    al = pre[..., 3:4] / 255.0
    rgb = np.where(al > 0.004, pre[..., :3] / np.maximum(al, 1e-3), 0)
    out = Image.fromarray(np.clip(np.concatenate([rgb, pre[..., 3:4]], -1), 0, 255).astype(np.uint8), "RGBA")
    return to_surface(out), pad / L, L


@functools.lru_cache(maxsize=None)
def mask_points(name, n=260, seed=1):
    """Deterministic points inside a cut-out (source px) with their colours, for dust dissolves."""
    im = _pil(name)
    small = im.resize((max(1, im.width // 8), max(1, im.height // 8)))
    arr = np.asarray(small, np.float32)
    ys, xs = np.nonzero(arr[..., 3] > 160)
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(xs), size=min(n, len(xs)), replace=False)
    pts = np.stack([xs[pick] * 8 + rng.uniform(0, 8, len(pick)), ys[pick] * 8 + rng.uniform(0, 8, len(pick))], 1)
    cols = arr[ys[pick], xs[pick], :3] / 255.0
    return pts, cols, rng.random((len(pick), 4))


def fig(cr, name, cx, by, hgt, alpha=1.0, rot=0.0, flip=False, kind=None, color=GOLD_L, anchor="b", op=None):
    """A cut-out with its bottom centre (anchor "b") or centre ("c") at (cx, by), `hgt` px tall.
    kind: None = the painting, "gold" = flat silhouette, "aura" = soft glow behind it, "blur" = soft copy."""
    if alpha <= 0.002:
        return
    sw, sh = dims(name)
    z = hgt / sh
    cr.save()
    cr.translate(cx, by)
    if rot:
        cr.rotate(rot)
    cr.scale(-z if flip else z, z)
    y0 = -sh if anchor == "b" else -sh / 2
    if kind is None:
        blit(cr, name, -sw / 2, y0, z, alpha, op)
    elif kind == "gold":
        _paint_surface(cr, silhouette(name, color), 0.25, -sw / 2, y0, alpha, op, cairo.FILTER_BILINEAR)
    elif kind == "aura":
        s, pad, L = aura(name, color)
        _paint_surface(cr, s, L, -sw / 2 - pad, y0 - pad, alpha, op if op is not None else cairo.OPERATOR_ADD,
                       cairo.FILTER_BILINEAR)
    elif kind == "blur":
        s, pad, L = blurred(name)
        _paint_surface(cr, s, L, -sw / 2 - pad, y0 - pad, alpha, op, cairo.FILTER_BILINEAR)
    cr.restore()


# ---------------------------------------------------------------- camera / multiplane

def camera(cr, cx, cy, z):
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def clamp_cam(cx, cy, z, box):
    """Keep the view inside box = (x0, y0, x1, y1) in source px."""
    x0, y0, x1, y1 = box
    hw, hh = W / 2 / z, H / 2 / z
    cx = clamp(cx, x0 + hw, x1 - hw) if x1 - x0 > 2 * hw else (x0 + x1) / 2
    cy = clamp(cy, y0 + hh, y1 - hh) if y1 - y0 > 2 * hh else (y0 + y1) / 2
    return cx, cy, z


def layer_at(cr, name, cam, ref, k=1.0, alpha=1.0, dx=0.0, dy=0.0, zref=None):
    """A cut-out over its own plate: aligned when the camera is at `ref`; nearer layers (k > 1) slide and grow more."""
    e = _index()[name]
    cx, cy, z = cam
    ox, oy = (cx - ref[0]) * (1 - k), (cy - ref[1]) * (1 - k)
    cr.save()
    if zref and k != 1.0:
        s = (z / zref) ** ((k - 1) * 1.6)
        ax, ay = e["x"] + e["w"] / 2, e["y"] + e["h"]
        cr.translate(ax + ox, ay + oy)
        cr.scale(s, s)
        cr.translate(-ax - ox, -ay - oy)
    blit(cr, name, e["x"] + ox + dx, e["y"] + oy + dy, z, alpha)
    cr.restore()


def panel(cr, rect, fn, border=True, alpha=1.0):
    """Draw fn(cr) clipped to rect = (x, y, w, h), with a gold rule round it."""
    x, y, w, h = rect
    if alpha <= 0:
        return
    cr.save()
    cr.rectangle(x, y, w, h)
    cr.clip()
    if alpha < 1:
        cr.push_group()
    fn(cr)
    if alpha < 1:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    cr.restore()
    if border:
        cr.set_source_rgba(*GOLD, 0.95 * alpha)
        cr.set_line_width(5)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        cr.set_source_rgba(*GOLD_L, 0.5 * alpha)
        cr.set_line_width(1.5)
        cr.rectangle(x + 9, y + 9, w - 18, h - 18)
        cr.stroke()


# ---------------------------------------------------------------- grounds, light, particles

@functools.lru_cache(maxsize=4)
def _ground(kind):
    rng = np.random.default_rng({"indigo": 3, "saffron": 4, "rose": 5, "night": 6}[kind])
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.47) / (H * 0.62)) ** 2)
    blot = np.asarray(Image.fromarray((rng.random((20, 12)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                      np.float32)[..., None] / 255.0
    fib = np.asarray(Image.fromarray((rng.random((H // 3, 60)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                     np.float32)[..., None] / 255.0
    if kind == "indigo":
        c0, c1 = np.array([0.20, 0.18, 0.42]), np.array([0.035, 0.03, 0.09])
    elif kind == "night":
        c0, c1 = np.array([0.33, 0.22, 0.30]), np.array([0.05, 0.03, 0.07])
    elif kind == "rose":
        c0, c1 = np.array([0.78, 0.36, 0.25]), np.array([0.22, 0.06, 0.05])
    else:
        c0, c1 = np.array([0.97, 0.74, 0.30]), np.array([0.70, 0.40, 0.10])
    f = np.clip(d / 0.75, 0, 1)[..., None] ** 1.2
    img = c0 * (1 - f) + c1 * f
    img = img * (0.93 + 0.12 * blot) + (fib - 0.5) * 0.025
    img += rng.normal(0, 0.008, img.shape)
    return to_surface(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), "RGB"))


def ground(cr, kind):
    cr.set_source_surface(_ground(kind), 0, 0)
    cr.paint()


@functools.lru_cache(maxsize=2)
def _rays(seed=3, n=22, size=900):
    rng = np.random.default_rng(seed)
    yy, xx = (np.mgrid[0:size, 0:size].astype(np.float32) - size / 2)
    ang = np.arctan2(yy, xx)
    r = np.hypot(xx, yy) / (size / 2)
    v = np.zeros_like(r)
    for _ in range(n):
        a0, wd, amp = rng.uniform(-np.pi, np.pi), rng.uniform(0.025, 0.10), rng.uniform(0.35, 1.0)
        d = np.angle(np.exp(1j * (ang - a0)))
        v += amp * np.exp(-(d / wd) ** 2)
    v = np.clip(v, 0, 1.4) / 1.4 * np.clip(1 - r, 0, 1) ** 1.6
    a = (np.clip(v, 0, 1) * 255).astype(np.uint8)
    img = Image.new("RGBA", (size, size), (255, 226, 160, 255))
    img.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(3)))
    return to_surface(img)


def rays(cr, cx, cy, radius, t, alpha=0.4, speed=0.03, seed=3):
    if alpha <= 0:
        return
    s = _rays(seed)
    sz = s.get_width()
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(t * speed)
    k = 2 * radius / sz
    cr.scale(k, k)
    cr.set_source_surface(s, -sz / 2, -sz / 2)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.paint_with_alpha(alpha)
    cr.restore()


def glow(cr, cx, cy, r, color=GOLD_L, alpha=0.5, op=cairo.OPERATOR_ADD):
    if alpha <= 0:
        return
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, r)
    g.add_color_stop_rgba(0, *color, alpha)
    g.add_color_stop_rgba(0.35, *color, alpha * 0.45)
    g.add_color_stop_rgba(1, *color, 0)
    cr.save()
    cr.set_operator(op)
    cr.set_source(g)
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def mandala(cr, cx, cy, r, t, alpha=1.0):
    """Rotating rings of gold dots and hairlines behind a deity (a painted prabhamandala)."""
    if alpha <= 0:
        return
    cr.save()
    for rr, n, dot, spd in ((r, 56, 5.5, 0.05), (r * 0.80, 40, 4.0, -0.07), (r * 1.17, 72, 3.2, 0.035)):
        cr.set_source_rgba(*GOLD_L, 0.75 * alpha)
        for i in range(n):
            a = 2 * math.pi * i / n + spd * t
            cr.new_sub_path()
            cr.arc(cx + rr * math.cos(a), cy + rr * math.sin(a), dot, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(*GOLD, 0.45 * alpha)
        cr.set_line_width(2)
        cr.arc(cx, cy, rr + 14, 0, 2 * math.pi)
        cr.stroke()
    cr.set_line_width(1.5)
    cr.set_source_rgba(*GOLD, 0.35 * alpha)
    for i in range(24):                          # petal arcs between the rings
        a = 2 * math.pi * i / 24 + 0.02 * t
        cr.arc(cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a), r * 0.13, a + 1.9, a + 4.4)
        cr.new_sub_path()
    cr.stroke()
    cr.restore()


@functools.lru_cache(maxsize=1)
def _sprite():
    n = 64
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32) - n / 2 + 0.5
    r = np.hypot(xx, yy) / (n / 2)
    a = np.clip(np.exp(-(r / 0.28) ** 2) + 0.25 * np.exp(-(r / 0.7) ** 2), 0, 1)
    img = Image.new("RGBA", (n, n), (255, 236, 190, 255))
    img.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return to_surface(img)


_DUST = np.random.default_rng(5).random((140, 7))


def dust(cr, t, alpha=0.8, n=70, box=(0, 0, W, H), size=1.0, rise=18.0, seed_off=0, color=None):
    """Floating motes catching the light: deterministic in t."""
    if alpha <= 0:
        return
    s = _sprite()
    x0, y0, w, h = box
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(n):
        a, b, c, d, e, f, g = _DUST[(i + seed_off) % len(_DUST)]
        x = x0 + (a * w + 40 * math.sin(t * (0.2 + 0.3 * c) + 6 * d)) % w
        y = y0 + (b * h - rise * (0.5 + e) * t) % h
        tw = 0.45 + 0.55 * math.sin(t * (1.2 + 2 * f) + 9 * g) ** 2
        sz = (6 + 22 * e ** 2) * size
        k = sz / 64
        cr.save()
        cr.translate(x, y)
        cr.scale(k, k)
        cr.set_source_surface(s, -32, -32)
        cr.paint_with_alpha(alpha * tw * (0.35 + 0.65 * c))
        cr.restore()
    cr.restore()


_PET = np.random.default_rng(9).random((60, 8))
PETAL_COLS = [(0.98, 0.62, 0.12), (0.99, 0.75, 0.20), (0.93, 0.36, 0.30), (0.98, 0.92, 0.82), (0.96, 0.50, 0.55)]


def petals(cr, t, t0, alpha=1.0, n=26, speed=1.0, box=(0, 0, W, H), leaves=False, seed_off=0):
    """Marigold, rose and jasmine petals (or leaves) drifting down from t0; deterministic in t."""
    if alpha <= 0 or t < t0:
        return
    x0, y0, w, h = box
    u = t - t0
    for i in range(n):
        a, b, c, d, e, f, g, k = _PET[(i + seed_off) % len(_PET)]
        delay = b * 1.5
        if u < delay:
            continue
        uu = u - delay
        fall = (110 + 120 * c) * speed
        y = y0 - 60 + (uu * fall + a * 300 * (seed_off % 3)) % (h + 160)
        x = x0 + a * w + 70 * math.sin(uu * (0.8 + c) + 7 * d) + 30 * uu * (e - 0.5)
        rot = uu * (1.5 + 2 * f) * (1 if g > 0.5 else -1) + 6 * d
        sz = 14 + 16 * e
        col = (0.36 + 0.2 * k, 0.52 + 0.2 * k, 0.18) if leaves else PETAL_COLS[int(k * len(PETAL_COLS)) % len(PETAL_COLS)]
        flipw = abs(math.cos(uu * (2 + 2 * g) + d * 5))
        cr.save()
        cr.translate(x, y)
        cr.rotate(rot)
        cr.scale(max(0.15, flipw), 1)
        cr.move_to(0, -sz)
        cr.curve_to(sz * 0.62, -sz * 0.6, sz * 0.5, sz * 0.55, 0, sz)
        cr.curve_to(-sz * 0.5, sz * 0.55, -sz * 0.62, -sz * 0.6, 0, -sz)
        cr.set_source_rgba(*col, 0.92 * alpha * min(1.0, uu / 0.3))
        cr.fill_preserve()
        cr.set_source_rgba(col[0] * 0.6, col[1] * 0.5, col[2] * 0.4, 0.5 * alpha)
        cr.set_line_width(1.2)
        cr.stroke()
        cr.restore()


def sparkle(cr, x, y, r, alpha):
    """Four-point glint."""
    if alpha <= 0:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source_rgba(1, 0.95, 0.8, alpha)
    cr.move_to(x - r, y)
    cr.curve_to(x - r * 0.15, y - r * 0.15, x - r * 0.15, y - r * 0.15, x, y - r)
    cr.curve_to(x + r * 0.15, y - r * 0.15, x + r * 0.15, y - r * 0.15, x + r, y)
    cr.curve_to(x + r * 0.15, y + r * 0.15, x + r * 0.15, y + r * 0.15, x, y + r)
    cr.curve_to(x - r * 0.15, y + r * 0.15, x - r * 0.15, y + r * 0.15, x - r, y)
    cr.fill()
    cr.restore()
    glow(cr, x, y, r * 1.4, (1, 0.9, 0.7), alpha * 0.5)


def gold_dust_from(cr, name, ox, oy, z, t, t0, dur, target=None, alpha=1.0, n=220):
    """Gold dust leaving a cut-out (placed at source origin ox, oy under the current transform) from t0."""
    u = (t - t0) / dur
    if u <= 0 or u > 1.6:
        return
    pts, cols, rnd = mask_points(name, n)
    s = _sprite()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for (px, py), r in zip(pts, rnd):
        start = r[0] * 0.55
        q = clamp((u - start) / 0.9)
        if q <= 0 or q >= 1:
            continue
        x, y = ox + px, oy + py
        if target:
            e = q * q
            x = lerp(x, target[0], e) + 60 * math.sin(q * 6 + r[1] * 9) * (1 - e)
            y = lerp(y, target[1], e) - 140 * math.sin(q * math.pi) * r[2]
        else:
            x += 80 * (r[1] - 0.5) * q
            y -= (180 + 260 * r[2]) * q
        a = alpha * math.sin(math.pi * q) * (0.6 + 0.4 * r[3])
        sz = (10 + 18 * r[3]) / z
        cr.save()
        cr.translate(x, y)
        cr.scale(sz / 64, sz / 64)
        cr.set_source_surface(s, -32, -32)
        cr.paint_with_alpha(a)
        cr.restore()
    cr.restore()


def flash(cr, a, color=(1.0, 0.86, 0.55)):
    if a <= 0:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source_rgba(*color, clamp(a))
    cr.paint()
    cr.restore()


def sun_wash(cr, alpha, color=(1.0, 0.58, 0.22), top=True):
    """Evening/morning light: a warm gradient laid over the painting (soft light) plus a little lift."""
    if alpha <= 0:
        return
    g = cairo.LinearGradient(0, 0, 0, H)
    if top:
        g.add_color_stop_rgba(0, *color, 0.55 * alpha)
        g.add_color_stop_rgba(0.55, *color, 0.18 * alpha)
        g.add_color_stop_rgba(1, 0.25, 0.08, 0.10, 0.35 * alpha)
    else:
        g.add_color_stop_rgba(0, 0.25, 0.08, 0.10, 0.3 * alpha)
        g.add_color_stop_rgba(1, *color, 0.5 * alpha)
    cr.save()
    cr.set_operator(cairo.OPERATOR_SOFT_LIGHT)
    cr.set_source(g)
    cr.paint()
    cr.restore()


# ---------------------------------------------------------------- the manuscript finish

@functools.lru_cache(maxsize=1)
def _overlay():
    rng = np.random.default_rng(21)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = ((xx - W / 2) / (W * 0.66)) ** 2 + ((yy - H * 0.48) / (H * 0.62)) ** 2
    vig = np.clip((d - 0.30) / 1.1, 0, 1) ** 1.25 * 0.70
    blot = np.asarray(Image.fromarray((rng.random((34, 20)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                      np.float32) / 255.0
    fib = np.asarray(Image.fromarray((rng.random((H // 2, 90)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                     np.float32) / 255.0
    speck = (rng.random((H, W)) > 0.9993).astype(np.float32) * 0.35
    a = np.clip(vig + 0.07 * np.clip(blot - 0.45, 0, 1) + 0.03 * fib + speck, 0, 1)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 26, 12, 6
    rgba[..., 3] = (a * 255).astype(np.uint8)
    s = to_surface(Image.fromarray(rgba, "RGBA"))
    cr = cairo.Context(s)
    # gold folio border: a dark margin, a gold rule, a hairline and small corner rosettes
    m = 16
    cr.set_source_rgba(0.09, 0.05, 0.03, 0.9)
    cr.rectangle(0, 0, W, H)
    cr.rectangle(m, m, W - 2 * m, H - 2 * m)
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.fill()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    for inset, wd, col in ((m + 3, 5, GOLD), (m + 3, 1.6, GOLD_L), (m + 16, 1.4, GOLD)):
        g = cairo.LinearGradient(0, 0, W, H)
        for k in range(9):
            c = col if k % 2 == 0 else tuple(min(1, v * 1.18) for v in col)
            g.add_color_stop_rgba(k / 8, *c, 0.95)
        cr.set_source(g)
        cr.set_line_width(wd)
        cr.rectangle(inset, inset, W - 2 * inset, H - 2 * inset)
        cr.stroke()
    for cx, cy in ((m + 16, m + 16), (W - m - 16, m + 16), (m + 16, H - m - 16), (W - m - 16, H - m - 16)):
        cr.set_source_rgba(*GOLD_L, 0.95)
        for i in range(8):
            a = i * math.pi / 4
            cr.new_sub_path()
            cr.arc(cx + 9 * math.cos(a), cy + 9 * math.sin(a), 3.2, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.62, 0.12, 0.10, 1)
        cr.arc(cx, cy, 5, 0, 2 * math.pi)
        cr.fill()
    for i in range(1, 12):                       # tiny gold dots along the rule
        y = H * i / 12
        for x in (m + 16, W - m - 16):
            cr.set_source_rgba(*GOLD_L, 0.85)
            cr.arc(x, y, 3, 0, 2 * math.pi)
            cr.fill()
    s.flush()
    return s


@functools.lru_cache(maxsize=6)
def _grain(k):
    rng = np.random.default_rng(100 + k)
    n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    n = np.repeat(np.repeat(n, 2, 0), 2, 1)
    a = np.clip(np.abs(n) * 0.032, 0, 0.11)
    rgba = np.zeros((H, W, 4), np.uint8)
    lum = np.where(n > 0, 255, 0).astype(np.uint8)
    rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = lum
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return to_surface(Image.fromarray(rgba, "RGBA"))


def finish(cr, t):
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgb(1.0, 0.95, 0.86)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_surface(_overlay(), 0, 0)
    cr.paint()
    cr.set_source_surface(_grain(int(round(t * FPS)) % 6), 0, 0)
    cr.paint()
    cr.restore()


# ---------------------------------------------------------------- text

def _anchor(anchor, w, h):
    return {"l": 0, "c": -w / 2, "r": -w}[anchor[0]], {"t": 0, "m": -h / 2, "b": -h}[anchor[1]]


@functools.lru_cache(maxsize=256)
def _shadow(text, size, font, tracking):
    f = ImageFont.truetype(font, size)
    l, t_, r, b = f.getbbox(text)
    pad = max(4, size // 10)
    blur = max(3, size // 9)
    P = pad + 3 * blur
    w = r - l + 2 * pad + tracking * max(0, len(text) - 1)
    h = b - t_ + 2 * pad
    img = Image.new("L", (int(w + 6 * blur), int(h + 6 * blur)), 0)
    d = ImageDraw.Draw(img)
    if tracking:
        x = P - l
        for ch in text:
            d.text((x, P - t_), ch, font=f, fill=255)
            x += f.getlength(ch) + tracking
    else:
        d.text((P - l, P - t_), text, font=f, fill=255)
    img = img.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(blur))
    rgba = Image.new("RGBA", img.size, (12, 6, 4, 255))
    rgba.putalpha(img)
    return to_surface(rgba), P


def stext(cr, text, x, y, size, color=CREAM, alpha=1.0, font=HEAD_FONT, anchor="lt", tracking=0, shadow=0.85):
    """Text with a soft dark shadow so it reads on a painting."""
    if alpha <= 0:
        return x, y, 0, 0
    w, h = text_size(text, size, font, tracking)
    dx, dy = _anchor(anchor, w, h)
    if shadow:
        s, P = _shadow(text, size, font, tracking)
        cr.set_source_surface(s, x + dx - P, y + dy - P + size * 0.05)
        cr.paint_with_alpha(min(1.0, alpha * shadow))
    draw_text(cr, text, x, y, size, color, alpha, font, anchor, tracking)
    return x + dx, y + dy, w, h


def head2(cr, t, small, big, t_small, t_big, y=250, x=80, small_size=62, big_size=170, alpha=1.0,
          small_color=CREAM, big_color=CORAL, center=False, t_ghost=None):
    """Two-tier headline (small setup words one by one, then one big word) with shadows. Returns the big word box."""
    if alpha <= 0:
        return None
    if big:
        big_size = min(big_size, int(big_size * (W - 2 * x) / max(1, text_size(big, big_size)[0])))
    words = small.split() if small else []
    widths = [text_size(wd, small_size)[0] for wd in words]
    gap = small_size * 0.28
    total = sum(widths) + gap * max(0, len(words) - 1)
    cx = (W - total) / 2 if center else x
    for k, wd in enumerate(words):
        p = prog(t, t_small + 0.08 * k, 0.25)
        if p <= 0:
            break
        stext(cr, wd, cx, y + 16 * (1 - p), small_size, small_color, p * alpha)
        cx += widths[k] + gap
    if not big:
        return None
    by = y + (small_size * 1.2 if words else 0)
    bw, bh = text_size(big, big_size)
    bx = (W - bw) / 2 if center else x
    if t_ghost is not None and t_ghost <= t < t_big + 0.3:
        stext(cr, big, bx, by, big_size, (0.6, 0.55, 0.5), 0.3 * alpha * prog(t, t_ghost, 0.25) * (1 - prog(t, t_big, 0.3)),
              shadow=0)
    p = prog(t, t_big, 0.3)
    if p > 0:
        s = 1.14 - 0.14 * back(clamp((t - t_big) / 0.32))
        cr.save()
        cr.translate(bx + bw / 2, by + bh / 2)
        cr.scale(s, s)
        stext(cr, big, -bw / 2, -bh / 2, big_size, big_color, p * alpha)
        cr.restore()
    return bx, by, bw, bh


def label(cr, t, t0, text, x, y, size=30, t1=None, alpha=1.0, anchor="c", color=CREAM, fill=(0.10, 0.07, 0.16),
          tracking=3):
    """Cartouche label: dark lacquer pill with a gold rule, mono caps. Pops in at t0, out at t1."""
    p = prog(t, t0, 0.28) * (1 - prog(t, t1, 0.3) if t1 is not None else 1.0) * alpha
    if p <= 0.003:
        return None
    w, h = text_size(text, size, MONO_FONT, tracking)
    bw, bh = w + 54, h + 30
    bx = {"l": 0, "c": -bw / 2, "r": -bw}[anchor[0]]
    s = 0.9 + 0.1 * back(clamp((t - t0) / 0.3))
    cr.save()
    cr.translate(x, y + 10 * (1 - p))
    cr.scale(s, s)
    cr.set_source_rgba(0, 0, 0, 0.35 * p)
    _round(cr, bx + 5, -bh / 2 + 8, bw, bh, bh / 2)
    cr.fill()
    cr.set_source_rgba(*fill, 0.88 * p)
    _round(cr, bx, -bh / 2, bw, bh, bh / 2)
    cr.fill()
    cr.set_source_rgba(*GOLD, 0.95 * p)
    cr.set_line_width(2.5)
    _round(cr, bx + 5, -bh / 2 + 5, bw - 10, bh - 10, (bh - 10) / 2)
    cr.stroke()
    draw_text(cr, text, bx + bw / 2, 0, size, color, p, MONO_FONT, "cm", tracking)
    cr.restore()
    return x + bx, y - bh / 2, bw, bh


def credit(cr, alpha=1.0, y=1612):
    if alpha > 0:
        stext(cr, "PAINTINGS: CLEVELAND MUSEUM OF ART, CC0", W / 2, y, 21, (0.95, 0.90, 0.80), 0.8 * alpha, MONO_FONT,
              "cm", tracking=2, shadow=0.9)


def bubble(cr, t, t0, text, x, y, size=46, tail=(0, 1), alpha=1.0, t1=None):
    """A speech scroll: cream rounded card with a gold edge and a small tail pointing at the speaker."""
    p = prog(t, t0, 0.3) * (1 - prog(t, t1, 0.3) if t1 is not None else 1.0) * alpha
    if p <= 0.003:
        return
    lines = text.split("\n")
    ws = [text_size(s, size)[0] for s in lines]
    lh = size * 1.12
    bw, bh = max(ws) + 70, lh * len(lines) + 46
    s = 0.8 + 0.2 * back(clamp((t - t0) / 0.3))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_source_rgba(0, 0, 0, 0.3 * p)
    _round(cr, -bw / 2 + 6, -bh / 2 + 10, bw, bh, 26)
    cr.fill()
    cr.set_source_rgba(0.98, 0.93, 0.82, p)
    _round(cr, -bw / 2, -bh / 2, bw, bh, 26)
    cr.fill()
    tx, ty = tail
    cr.move_to(-30 + 60 * (tx > 0), bh / 2 - 2)
    cr.line_to(tx * 90, bh / 2 + 70 * ty)
    cr.line_to(30 + 60 * (tx > 0) - 40, bh / 2 - 2)
    cr.close_path()
    cr.fill()
    cr.set_source_rgba(*GOLD_D, p)
    cr.set_line_width(4)
    _round(cr, -bw / 2 + 7, -bh / 2 + 7, bw - 14, bh - 14, 20)
    cr.stroke()
    for i, s_ in enumerate(lines):
        draw_text(cr, s_, 0, -bh / 2 + 23 + lh * i + lh / 2, size, (0.30, 0.10, 0.06), p, HEAD_FONT, "cm")
    cr.restore()


def plate_stamp(cr, t, text, t0, x, y, size=80, color=GOLD_L, rot=-0.05, backing=(0.06, 0.04, 0.08)):
    """A stamp on a soft backing plate so it reads on a busy painting."""
    p = clamp((t - t0) / 0.22)
    if p <= 0:
        return
    w, h = text_size(text, size, tracking=4)
    s = 1.6 - 0.6 * back(p, 2.2)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*backing, 0.72 * p)
    _round(cr, -w / 2 - 40, -h / 2 - 30, w + 80, h + 60, 14)
    cr.fill()
    cr.restore()
    stamp(cr, t, text, t0, x, y, size=size, color=color, rot=rot)


# ---------------------------------------------------------------- shared compositions

def brahma_hero(cr, t, cx=540, by=1700, hgt=1150, alpha=1.0, glow_a=1.0, t0=0.0):
    """The Kalighat Brahma with his mandala, rays and aura."""
    head_y = by - hgt * 0.80
    rays(cr, cx, head_y, 780, t, 0.30 * glow_a)
    mandala(cr, cx, head_y + 10, 330, t, 0.9 * glow_a * alpha)
    glow(cr, cx, head_y, 520, (1.0, 0.70, 0.35), 0.22 * glow_a * alpha)
    fig(cr, "brahma_k", cx, by, hgt, 0.55 * glow_a * alpha, kind="aura")
    fig(cr, "brahma_k", cx, by, hgt, alpha)


def crowd_slots():
    """The boys and calves Krishna becomes (c7), and that turn into Vishnu (c13): back row to front."""
    out = []
    for i, x in enumerate((70, 215, 365, 715, 865, 1010)):            # back row
        out.append(("boy_grey" if i % 2 else "boy_red", x, 1270, 330, 0.30 + 0.05 * abs(i - 2.5), i % 3 == 0, 0.8))
    for i, x in enumerate((120, 300, 780, 960)):                       # front row
        out.append(("boy_red" if i % 2 else "boy_grey", x, 1440, 470, 0.05 * abs(i - 1.5), i >= 2, 1.0))
    return out


CALF_SLOTS = [("cows_145", 250, 1700, 310, 0.0, False), ("cows_145", 830, 1700, 310, 0.08, True),
              ("calf_row", 540, 1585, 170, 0.16, False)]


# ---------------------------------------------------------------- shots
# each: fn(cr, t, tl, t0, t1); t0/t1 = the shot's start/end

def s_brahma(cr, t, tl, t0, t1):
    """c1 + c2: Brahma alone on indigo (frame 0), the hook, then a push into his four faces."""
    ground(cr, "indigo")
    c2 = T(tl, "c2")
    u2 = sm((t - c2) / max(0.5, tl["c2"].end - c2))
    z = lerp(1.0 + 0.03 * clamp(t / 6), 1.85, u2 * u2 * 0.9 + u2 * 0.1)
    cr.save()
    fx, fy = 540, 820
    cr.translate(fx, fy + 260 * u2)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pulse = 0.5 + 0.5 * math.sin(t * 2.2)
    brahma_hero(cr, t, glow_a=0.75 + 0.25 * pulse + 0.4 * prog(t, 2.3, 0.6) * (1 - prog(t, 3.4, 0.8)))
    cr.restore()
    dust(cr, t, 0.75, 60)
    # the boys he hid, as gold ghosts "playing here"
    tp = C(tl, "c1", "खेल", "ಆಟ", 0.7)
    a = prog(t, tp - 0.15, 0.5) * (1 - prog(t, c2 + 0.3, 0.5))
    if a > 0:
        for name, x, ph, flip in (("boy_red", 140, 0.0, False), ("boy_grey", 950, 1.3, True)):
            hop = abs(math.sin((t - tp) * 3.4 + ph)) * 30
            q = prog(t, tp - 0.15, 0.5)
            fig(cr, name, x, 1680 - hop + 40 * (1 - q), 360, 0.9 * a, kind="aura", flip=flip)
            fig(cr, name, x, 1680 - hop + 40 * (1 - q), 360, a, flip=flip)
        stext(cr, "?", 225, 1250 - 10 * math.sin(t * 3), 110, GOLD_L, a * 0.95)
        stext(cr, "?", 800, 1230 - 10 * math.sin(t * 3 + 1), 96, GOLD_L, a * 0.9)
    # hook headline, fully on by ~1.5 s, ringed as "how" is spoken
    ha = 1 - prog(t, c2 + 0.05, 0.35)
    if ha > 0:
        cr.save()
        cr.translate(0, -60 * prog(t, c2 + 0.05, 0.35))
        box = head2(cr, t, "I HID THEM MYSELF.", "SO HOW?", -0.3, 0.9, y=245, small_size=64, big_size=200,
                    alpha=ha, t_ghost=-0.3)
        th = C(tl, "c1", "कैसे", "ಹೇಗೆ", 0.85)
        if box:
            bx, by_, bw, bh = box
            ring(cr, bx + bw / 2, by_ + bh * 0.56, bw * 0.60, bh * 0.62, prog(t, th - 0.05, 0.45), 10, CORAL, ha)
        cr.restore()
    # c2: Brahma's own question; the answer is a year old
    label(cr, t, c2 + 0.1, "THE QUESTION AROSE IN BRAHMA'S MIND", W / 2, 300, 27, t1=C(tl, "c2", "जवाब", "ಉತ್ತರ", 0.62) - 0.1)
    label(cr, t, F(tl, "c2", 0.25), "BRAHMA, THE CREATOR", W / 2, 1180, 30, t1=C(tl, "c2", "जवाब", "ಉತ್ತರ", 0.62) - 0.2,
          fill=(0.35, 0.08, 0.10))
    ta = C(tl, "c2", "जवाब", "ಉತ್ತರ", 0.62)
    ty = C(tl, "c2", "साल", "ವರ್ಷ", 0.85)
    if t >= ta - 0.1:
        head2(cr, t, "AND THE ANSWER WAS", "1 YEAR OLD", ta - 0.05, ty - 0.1, y=1250, small_size=60, big_size=170,
              big_color=GOLD_L, center=True)
    flash(cr, 0.85 * sm((t - (t1 - 0.25)) / 0.25))


def s_lunch(cr, t, tl, t0, t1):
    """c3: Bhagavata Purana, canto 10. The lunch on the river bank (146117), tilting down from the hills."""
    u = sm((t - t0) / max(0.5, F(tl, "c3", 0.8) - t0))
    cam = (lerp(1180, 650, u), lerp(960, 1290, u), lerp(1.04, 1.12, sm((t - t0) / max(0.5, t1 - t0))))
    cam = clamp_cam(*cam, (40, 45, 3385, 2330))
    ref = (650, 1290)
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_146117", 0, 0, cam[2])
    tk = C(tl, "c3", "कृष्ण", "ಕೃಷ್ಣ", 0.55)
    ox = (cam[0] - ref[0]) * (1 - 1.10)
    oy = (cam[1] - ref[1]) * (1 - 1.10)
    ka = prog(t, tk - 0.1, 0.6)
    glow(cr, 640 + ox, 1180 + oy, 260, GOLD_L, 0.55 * ka * (0.8 + 0.2 * math.sin(t * 3)))
    layer_at(cr, "boys_lunch", cam, ref, 1.10)
    for i in range(14):                                     # sunlight glints on the river
        x = 80 + (i * 233.7) % 1300
        y = 2180 + (i * 61.3) % 120
        sparkle(cr, x + 20 * math.sin(t + i), y, 16, 0.75 * max(0, math.sin(t * 2.4 + i * 1.7)) ** 3)
    cr.restore()
    dust(cr, t, 0.45, 40, seed_off=20)
    flash(cr, 0.7 * (1 - sm((t - t0) / 0.35)))
    label(cr, t, t0 + 0.05, "ONE YEAR EARLIER", W / 2, 1520, 32, t1=t0 + 1.6, fill=(0.35, 0.08, 0.10))
    head2(cr, t, "BHAGAVATA PURANA", "", t0 + 0.15, t0 + 10, y=250, small_size=70, center=True)
    tv = C(tl, "c3", "वृंदावन", "ವೃಂದಾವನ", 0.4)
    label(cr, t, t0 + 0.55, "CANTO 10 · CHAPTER 13", W / 2, 375, 30, t1=tv - 0.15)
    label(cr, t, tv, "VRINDAVAN, ON THE YAMUNA", W / 2, 375, 30, fill=(0.06, 0.20, 0.14))
    if ka > 0:
        sx = W / 2 + (640 + ox - cam[0]) * cam[2]
        sy = H / 2 + (1120 + oy - cam[1]) * cam[2]
        label(cr, t, tk, "KRISHNA", sx, max(500, sy - 120), 34, fill=(0.06, 0.12, 0.30))
    tn = C(tl, "c3", "नदी", "ನದಿ", 0.75)
    label(cr, t, tn, "LUNCH ON THE RIVERBANK", W / 2, 1440, 32, fill=(0.35, 0.08, 0.10))
    credit(cr, prog(t, t0 + 0.4, 0.4))


def s_forest(cr, t, tl, t0, t1):
    """c4: the calves wander deep into the forest; Krishna goes to find them (154759, multiplane)."""
    u = sm((t - t0) / max(0.5, t1 - t0))
    cam = clamp_cam(lerp(2500, 1650, u), 1330, lerp(0.80, 0.86, u), (100, 90, 3300, 2510))
    ref = (2075, 1330)
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_154759", 0, 0, cam[2])
    layer_at(cr, "krishna_forest", cam, ref, 1.14, zref=0.83)
    cr.restore()
    sun_wash(cr, 0.55, (0.55, 0.75, 0.55))
    rays(cr, 120, -100, 1500, t, 0.22, 0.01, seed=4)
    petals(cr, t, t0 - 2, 0.9, 18, 0.7, leaves=True, seed_off=7)
    dust(cr, t, 0.4, 30, seed_off=50)
    head2(cr, t, "THE CALVES WANDERED", "DEEP INTO THE FOREST", t0 + 0.1, F(tl, "c4", 0.3), y=250, small_size=58,
          big_size=120, big_color=GOLD_L)
    tk = C(tl, "c4", "ढूँढ", "ಹುಡುಕೋಕೆ", 0.75)
    label(cr, t, tk - 0.1, "KRISHNA GOES TO FIND THEM", W / 2, 1520, 32, fill=(0.06, 0.12, 0.30))


def s_hide(cr, t, tl, t0, t1):
    """c5: Brahma flies in and the boys vanish into gold dust (146117 again: same bank, now empty)."""
    u = sm((t - t0) / max(0.5, t1 - t0))
    cam = clamp_cam(700, 1188, lerp(0.84, 0.90, u), (40, 45, 3385, 2330))
    ref = (650, 1545)
    td = C(tl, "c5", "ग्वाल", "ಗೋಪಾಲಕ", 0.6) - 0.2
    dd = 1.5
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_146117", 0, 0, cam[2])
    # Brahma glides in from the top left to where the painter put him, then hovers
    ts = t0 + 0.15
    p = sm((t - ts) / 1.8)
    e = _index()["swan_146"]
    sx = lerp(-520, e["x"] + 40, p) + 18 * math.sin(t * 1.3)
    sy = lerp(-380, e["y"] + 70, p) + 10 * math.sin(t * 1.9)
    fig_c = (sx + e["w"] / 2, sy + e["h"] / 2)
    sw_glow = 0.35 + 0.65 * prog(t, td - 0.3, 0.6)
    s_, pad, L = aura("swan_146")
    _paint_surface(cr, s_, L, sx - pad, sy - pad, 0.7 * sw_glow, cairo.OPERATOR_ADD)
    blit(cr, "swan_146", sx, sy, cam[2])
    # the boys: fade + blur away from td, dust flies up to Brahma
    q = clamp((t - td) / dd)
    ox, oy = (cam[0] - ref[0]) * (1 - 1.10), (cam[1] - ref[1]) * (1 - 1.10)
    eb = _index()["boys_lunch"]
    if q < 1:
        layer_at(cr, "boys_lunch", cam, ref, 1.10, alpha=(1 - q) ** 1.5)
        if q > 0:
            s_, pad, L = blurred("boys_lunch")
            _paint_surface(cr, s_, L, eb["x"] + ox - pad, eb["y"] + oy - pad, math.sin(math.pi * q) * 0.6)
    gold_dust_from(cr, "boys_lunch", eb["x"] + ox, eb["y"] + oy, cam[2], t, td, dd, target=fig_c, n=260)
    cr.restore()
    dust(cr, t, 0.5, 40, seed_off=30)
    head2(cr, t, "BRAHMA HID", "EVERY BOY", t0 + 0.2, td + 0.1, y=250, small_size=62, big_size=170)
    label(cr, t, td + 0.5, "AND EVERY CALF", W / 2, 640, 34, fill=(0.35, 0.08, 0.10))
    th = C(tl, "c5", "छुपा", "ಬಚ್ಚಿಟ್ಟು", 0.9)
    stamp(cr, t, "HIDDEN", th, 700, 1420, size=96, color=GOLD_L, rot=-0.08)


def s_cave(cr, t, tl, t0, t1):
    """c6: the hidden boys in the cave; pan across to Brahma, watching (141755)."""
    u = sm((t - t0 - 0.35) / max(0.5, (t1 - t0) * 0.6))
    cam = clamp_cam(lerp(2600, 1180, u), 1215, lerp(1.08, 1.12, u), (300, 268, 3115, 2160))
    ref = (1180, 1215)
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_141755", 0, 0, cam[2])
    glow(cr, 2620, 1830, 300, (0.75, 0.80, 1.0), 0.25 * (0.6 + 0.4 * math.sin(t * 2)))
    e = _index()["swan_141"]
    bob = 160 + 14 * math.sin(t * 1.6)          # flown a little lower than painted, so his crowns stay in frame
    ox, oy = (cam[0] - ref[0]) * (1 - 1.22), (cam[1] - ref[1]) * (1 - 1.22)
    s_, pad, L = aura("swan_141")
    _paint_surface(cr, s_, L, e["x"] + ox - pad, e["y"] + oy + bob - pad, 0.5, cairo.OPERATOR_ADD)
    layer_at(cr, "swan_141", cam, ref, 1.22, dy=bob)
    cr.restore()
    dust(cr, t, 0.45, 40, seed_off=60)
    label(cr, t, t0 + 0.1, "HIDDEN AWAY, ASLEEP", W / 2, 1480, 32, t1=t0 + 0.35 + (t1 - t0) * 0.35)
    head2(cr, t, "NOW, WHAT WILL", "KRISHNA DO?", F(tl, "c6", 0.3), F(tl, "c6", 0.55), y=1230, small_size=64,
          big_size=170, big_color=GOLD_L)


def _krishna_crowd(cr, t, tl, t0, t_boys, t_calves, alpha=1.0, vishnu_at=None, krishna=True):
    """Krishna at the centre; copies of the boys fly out of him as gold and settle in colour; calves in front."""
    cx0, cy0 = 540, 1050
    slots = crowd_slots()
    order = sorted(range(len(slots)), key=lambda i: slots[i][2])
    for i in order:
        name, x, by, h, delay, flip, depth = slots[i]
        tb = t_boys + delay
        p = sm((t - tb) / 0.7)
        if p <= 0:
            continue
        xx, yy = lerp(cx0, x, p), lerp(cy0 + h * 0.5, by, p)
        hh = lerp(h * 0.4, h, p)
        col = prog(t, tb + 0.55, 0.6)
        v = prog(t, vishnu_at + delay * 0.6, 0.35) if vishnu_at is not None else 0
        a = alpha * depth
        fig(cr, name, xx, yy, hh, a * (0.55 * (1 - col) + 0.25) * (1 - v), kind="aura", flip=flip)
        if col < 1:
            fig(cr, name, xx, yy, hh, a * p * (1 - col) * (1 - v), kind="gold", color=(1.0, 0.82, 0.45), flip=flip,
                op=cairo.OPERATOR_ADD)
        fig(cr, name, xx, yy, hh, a * col * (1 - v), flip=flip)
        if v > 0:
            vw = h * (0.50 if depth < 1 else 0.58)
            vh = vw / 1.38
            cyv = yy - h * 0.45
            ring_halo(cr, xx, cyv, vw * 0.36, v * a, t, glow_a=0.6)
            fig(cr, "vishnu_garuda", xx, cyv, vh, v * a, anchor="c")
    if krishna:
        ka = alpha * (1 - (prog(t, vishnu_at - 0.1, 0.4) if vishnu_at is not None else 0))
        fig(cr, "krishna_145", cx0, 1500, 900, 0.55 * ka, kind="aura")
        fig(cr, "krishna_145", cx0, 1500, 900, ka)
    for k, (name, x, by, h, delay, flip) in enumerate(CALF_SLOTS):
        tb = t_calves + delay
        p = sm((t - tb) / 0.6)
        if p <= 0:
            continue
        col = prog(t, tb + 0.45, 0.5)
        v = prog(t, vishnu_at + 0.2 + 0.1 * k, 0.35) if vishnu_at is not None else 0
        yy = lerp(by + 60, by, p)
        fig(cr, name, x, yy, h, 0.8 * alpha * p * (1 - 0.6 * col) * (1 - v), kind="aura", flip=flip)
        fig(cr, name, x, yy, h, alpha * p * (1 - col) * (1 - v), kind="gold", color=(1.0, 0.82, 0.45), flip=flip,
            op=cairo.OPERATOR_ADD)
        fig(cr, name, x, yy, h, alpha * col * (1 - v), flip=flip)
        if v > 0:
            vh = h * 0.62
            ring_halo(cr, x, yy - h * 0.45, vh * 0.55, v * alpha, t, glow_a=0.6)
            fig(cr, "vishnu_garuda", x, yy - h * 0.45, vh, v * alpha, anchor="c")


def ring_halo(cr, cx, cy, r, a, t, glow_a=1.0):
    if a <= 0:
        return
    glow(cr, cx, cy, r * 1.3, (1.0, 0.78, 0.40), 0.35 * a * glow_a)
    cr.set_source_rgba(*GOLD_L, 0.9 * a)
    cr.set_line_width(max(2, r * 0.04))
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.stroke()
    cr.set_line_width(max(1, r * 0.015))
    cr.set_source_rgba(*GOLD, 0.7 * a)
    n = 24
    for i in range(n):
        ang = 2 * math.pi * i / n + t * 0.4
        cr.move_to(cx + r * 1.05 * math.cos(ang), cy + r * 1.05 * math.sin(ang))
        cr.line_to(cx + r * 1.22 * math.cos(ang), cy + r * 1.22 * math.sin(ang))
    cr.stroke()


def s_multiply(cr, t, tl, t0, t1):
    """c7: Krishna himself becomes every boy and every calf (gold copies streaming out, settling in colour)."""
    ground(cr, "indigo")
    tb = C(tl, "c7", "हर एक बच्चा", "ಪ್ರತಿಯೊಬ್ಬ", 0.55) - 0.15
    tc = C(tl, "c7", "बछड़ा", "ಕರುವೂ", 0.85) - 0.15
    z = lerp(1.0, 1.06, sm((t - t0) / max(0.5, t1 - t0)))
    cr.save()
    cr.translate(540, 1100)
    cr.scale(z, z)
    cr.translate(-540, -1100)
    rays(cr, 540, 760, 1100, t, 0.28 + 0.35 * prog(t, tb - 0.2, 0.5) * (1 - prog(t, tb + 1.2, 1.0)))
    mandala(cr, 540, 760, 260, t, 0.65)
    glow(cr, 540, 900, 600, (1.0, 0.72, 0.35), 0.18 + 0.25 * prog(t, tb - 0.3, 0.4))
    _krishna_crowd(cr, t, tl, t0, tb, tc)
    cr.restore()
    flash(cr, 0.45 * (1 - sm((t - tb) / 0.5)) * float(t >= tb))
    dust(cr, t, 0.8, 70, seed_off=10)
    head2(cr, t, "KRISHNA BECAME", "", t0 + 0.15, t0 + 99, y=250, small_size=66)
    big = "EVERY CALF" if t >= tc else "EVERY BOY"
    tbig = tc if t >= tc else tb
    head2(cr, t, "", big, 0, tbig, y=250 + 66 * 1.2, big_size=170, big_color=GOLD_L)
    if t < tb:
        label(cr, t, F(tl, "c7", 0.12), "WHAT NOBODY COULD IMAGINE", W / 2, 520, 30, t1=tb - 0.1)


def s_same(cr, t, tl, t0, t1):
    """c8: same face, same clothes, same flute, same habits: a boy and Krishna-as-the-boy, side by side."""
    ground(cr, "saffron")
    cr.set_source_rgba(0.55, 0.12, 0.08, 0.85)                       # painted red inner margin, like the folio
    cr.set_line_width(10)
    cr.rectangle(52, 52, W - 104, H - 104)
    cr.stroke()
    cr.set_source_rgba(0.15, 0.08, 0.05, 0.7)
    cr.set_line_width(2.5)
    cr.rectangle(66, 66, W - 132, H - 132)
    cr.stroke()
    z = lerp(1.0, 1.05, sm((t - t0) / max(0.5, t1 - t0)))
    cr.save()
    cr.translate(540, 1200)
    cr.scale(z, z)
    cr.translate(-540, -1200)
    hgt = 770
    lx, rx, by = 300, 780, 1600
    for x in (lx, rx):
        cr.set_source_rgba(0.35, 0.18, 0.05, 0.22)
        cr.save()
        cr.translate(x, by - 4)
        cr.scale(1, 0.18)
        cr.arc(0, 0, 150, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    shine = 0.5 + 0.5 * math.sin(t * 2.6)
    fig(cr, "boy_red", rx, by, hgt, 0.35 + 0.2 * shine, kind="aura")
    fig(cr, "boy_red", lx, by, hgt)
    fig(cr, "boy_red", rx, by, hgt)
    for i in range(5):                                                # a faint golden shimmer only on Krishna
        a = (t * 0.7 + i * 0.2) % 1
        sparkle(cr, rx - 120 + 240 * ((i * 0.37 + 0.2) % 1), by - hgt * (0.15 + 0.7 * a), 12, 0.6 * math.sin(math.pi * a))
    cr.restore()
    label(cr, t, t0 + 0.05, "THE REAL BOY", lx, 770, 30, fill=(0.35, 0.08, 0.10))
    label(cr, t, t0 + 0.25, "KRISHNA AS HIM", rx, 770, 30, fill=(0.06, 0.12, 0.30))
    items = [("FACE", C(tl, "c8", "शक्ल", "ಮುಖ", 0.08)), ("CLOTHES", C(tl, "c8", "कपड़े", "ಡ್ರೆಸ್", 0.25)),
             ("FLUTE", C(tl, "c8", "बांसुरी", "ಕೊಳಲು", 0.43)), ("HABITS", C(tl, "c8", "आदतें", "ಹ್ಯಾಬಿಟ್ಸ್", 0.6))]
    for i, (word, tw) in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 110 + col * 460, 270 + row * 120
        p = prog(t, tw - 0.1, 0.25)
        if p <= 0:
            continue
        stext(cr, "SAME " + word, x + 80, y + 12 * (1 - p), 60, (0.25, 0.07, 0.04), p, shadow=0)
        cr.set_source_rgba(0.25, 0.07, 0.04, p)
        cr.set_line_width(5)
        cr.rectangle(x, y + 10, 56, 56)
        cr.stroke()
        tick(cr, x + 8, y + 40, 60, prog(t, tw + 0.15, 0.3), color=(0.62, 0.10, 0.08))
    # matching marks on both figures as each item is said
    face_y, cloth_y = by - hgt * 0.86, by - hgt * 0.35
    for x in (lx, rx):
        dxf = 25 if x == lx else 25
        ring(cr, x + dxf, face_y, 95, 95, prog(t, items[0][1] + 0.1, 0.4), 7, (0.62, 0.10, 0.08))
        ring(cr, x - 10, cloth_y, 150, 230, prog(t, items[1][1] + 0.1, 0.45), 6, (0.62, 0.10, 0.08))
    tn = C(tl, "c8", "फ़र्क़", "ಎಕ್ಸಾಕ್ಟ್", 0.85)
    stamp(cr, t, "NO DIFFERENCE", tn - 0.05, W / 2, 600, size=78, color=(0.62, 0.10, 0.08), rot=-0.05)


def s_evening(cr, t, tl, t0, t1):
    """c9, first half: evening; the herd comes home and the mothers wait at the door (154758, warm light)."""
    u = sm((t - t0) / max(0.5, t1 - t0))
    cam = clamp_cam(lerp(2000, 2780, u), 1110, lerp(0.92, 0.98, u), (55, 70, 3345, 2105))
    ref = (2700, 1110)
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_154758", 0, 0, cam[2])
    for x, y in ((3010, 820), (2860, 1130)):
        glow(cr, x, y, 260, (1.0, 0.62, 0.25), 0.28 * (0.8 + 0.2 * math.sin(t * 5 + x)))
    layer_at(cr, "mothers", cam, ref, 1.08, zref=0.97)
    cr.restore()
    sun_wash(cr, 1.0)
    glow(cr, 900, 260, 900, (1.0, 0.55, 0.20), 0.30)
    dust(cr, t, 0.6, 50, seed_off=80, rise=10)
    head2(cr, t, "EVENING.", "", t0 + 0.1, t0 + 99, y=250, small_size=70)
    label(cr, t, t0 + 0.6, "EVERYONE COMES HOME", 330, 390, 30, anchor="l", fill=(0.35, 0.08, 0.10))


def s_hug(cr, t, tl, t0, t1):
    """c9, second half: the mothers hug their sons, and the love overflows (Kalighat Yasoda, warm glow, petals)."""
    ground(cr, "rose")
    z = lerp(1.0, 1.07, sm((t - t0) / max(0.5, t1 - t0)))
    to = C(tl, "c9", "उमड़", "ಜಾಸ್ತಿ", 0.88) - 0.2
    th = C(tl, "c9", "गले", "ತಬ್ಕೊಂಡ್ರು", 0.45) - 0.1
    ti = C(tl, "c9", "इस बार", "ಈ ಸಲ", 0.65) - 0.1
    cr.save()
    cr.translate(540, 1150)
    cr.scale(z, z)
    cr.translate(-540, -1150)
    beat = 0.5 + 0.5 * math.sin(t * 2.4)
    for k in range(4):                                    # waves of warmth going out from the hug
        ph = ((t - t0) * 0.45 + k / 4) % 1
        a = (0.25 + 0.45 * prog(t, to, 0.6)) * math.sin(math.pi * ph)
        cr.set_source_rgba(1.0, 0.80, 0.55, 0.35 * a)
        cr.set_line_width(6 + 30 * ph)
        cr.arc(560, 1000, 150 + 650 * ph, 0, 2 * math.pi)
        cr.stroke()
    glow(cr, 560, 1000, 700, (1.0, 0.75, 0.45), 0.25 + 0.3 * prog(t, to, 0.6) + 0.08 * beat)
    burst = sm((t - th) / 0.25) * (1 - sm((t - th - 0.25) / 0.9))          # the hug: one warm pulse
    glow(cr, 560, 1050, 900, (1.0, 0.85, 0.6), 0.45 * burst)
    fig(cr, "yasoda_hug", 540, 1720, 1240, 0.55 + 0.4 * prog(t, to, 0.6), kind="aura", color=(1.0, 0.78, 0.5))
    fig(cr, "yasoda_hug", 540, 1720, 1240)
    cr.restore()
    petals(cr, t, t0 + 0.2, 1.0, 30, 0.8 + 0.6 * prog(t, to, 0.5))
    dust(cr, t, 0.6, 40, seed_off=90)
    head2(cr, t, "EVERY MOTHER HUGS HER SON", "", t0 + 0.1, t0 + 99, y=250, small_size=54,
          alpha=1 - prog(t, ti - 0.1, 0.3))
    head2(cr, t, "THIS TIME, THE LOVE", "OVERFLOWED", ti, to, y=250, small_size=60, big_size=170,
          big_color=(1.0, 0.86, 0.62))


SEASONS = [((0.65, 1.0, 0.70), 0.10, "SPRING"), ((1.0, 0.78, 0.35), 0.16, "SUMMER"),
           ((0.40, 0.48, 0.66), 0.30, "MONSOON"), ((0.80, 0.88, 1.0), 0.24, "WINTER")]


def s_year(cr, t, tl, t0, t1):
    """c10: a whole year passes and nobody notices: seasons wash over the Braj landscape, days fly by."""
    tn = C(tl, "c10", "पता", "ಗೊತ್ತಾಗ್ಲಿಲ್ಲ", 0.75)
    te = max(t0 + 1.5, tn - 0.15)
    u = clamp((t - t0) / (te - t0))
    cam = clamp_cam(lerp(1150, 2150, sm((t - t0) / max(0.5, t1 - t0))), 1330, 1.08, (240, 270, 3160, 2310))
    cr.save()
    camera(cr, *cam)
    blit(cr, PAINT["nanda"], 0, 0, cam[2])
    cr.restore()
    s = u * len(SEASONS)
    k = min(len(SEASONS) - 1, int(s))
    f = s - k
    for j, (col, a, _) in enumerate(SEASONS):
        w = (1 - f) if j == k else (f if j == (k + 1) % len(SEASONS) and k + 1 < len(SEASONS) else 0)
        if w > 0.01:
            cr.set_source_rgba(*col, a * 1.1 * w)
            cr.paint()
            if j == 2:                                    # monsoon rain
                cr.set_source_rgba(0.88, 0.92, 1.0, 0.55 * w)
                cr.set_line_width(2.5)
                for i in range(90):
                    x = (i * 137.3 + t * 260) % (W + 200) - 100
                    y = (i * 91.7 + t * 1500) % (H + 200) - 100
                    cr.move_to(x, y)
                    cr.line_to(x - 14, y + 46)
                cr.stroke()
            if j == 3:
                glow(cr, W / 2, 1300, 900, (0.9, 0.93, 1.0), 0.18 * w, cairo.OPERATOR_OVER)
            if j == 0:
                petals(cr, t, t0 - 3, 0.7 * w, 14, 0.6, seed_off=13)
    g = cairo.RadialGradient(W / 2, 520, 40, W / 2, 520, 620)
    g.add_color_stop_rgba(0, 0.05, 0.03, 0.02, 0.62)
    g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
    cr.set_source(g)
    cr.paint()
    # the sun races across the sky: days flying past
    days = int(lerp(1, 365, u ** 1.6))
    ph = (u * 7.0) % 1
    sx = lerp(-80, W + 80, ph)
    sy = 760 - 360 * math.sin(math.pi * ph)
    glow(cr, sx, sy, 220, (1.0, 0.85, 0.5), 0.6)
    cr.set_source_rgba(1.0, 0.93, 0.75, 0.9)
    cr.arc(sx, sy, 34, 0, 2 * math.pi)
    cr.fill()
    stext(cr, "DAY", W / 2, 470, 44, CREAM, prog(t, t0 + 0.1, 0.3), MONO_FONT, "cm", tracking=8)
    stext(cr, f"{days}", W / 2, 600, 190, GOLD_L, prog(t, t0 + 0.1, 0.3), HEAD_FONT, "cm")
    lab = SEASONS[k][2] if u < 1 else "1 FULL YEAR"
    stext(cr, lab, W / 2, 760, 46, CREAM, prog(t, t0 + 0.2, 0.3), MONO_FONT, "cm", tracking=6)
    head2(cr, t, "A WHOLE YEAR PASSED", "", t0 + 0.1, t0 + 99, y=250, small_size=64, center=True)
    plate_stamp(cr, t, "NOBODY KNEW", tn, W / 2, 1260, size=104, color=(0.70, 0.10, 0.07), rot=-0.06,
                backing=(0.98, 0.94, 0.84))


def s_moment(cr, t, tl, t0, t1):
    """c11, the re-hook: but for Brahma, only a moment had passed. Back to Brahma on indigo."""
    ground(cr, "indigo")
    z = lerp(1.0, 1.06, sm((t - t0) / max(0.5, t1 - t0)))
    cr.save()
    cr.translate(540, 1300)
    cr.scale(z, z)
    cr.translate(-540, -1300)
    brahma_hero(cr, t, 540, 1720, 980, glow_a=0.9)
    cr.restore()
    dust(cr, t, 0.6, 50)
    tm = C(tl, "c11", "पल", "ಕ್ಷಣ", 0.85)
    p = prog(t, t0 + 0.1, 0.3)
    stext(cr, "FOR VRAJ:", 80, 250, 56, CREAM, p)
    _, _, w1, _ = stext(cr, "1 YEAR", 80, 320, 120, CREAM, p)
    if t > t0 + 0.6:
        strike(cr, 70, 395, 90 + w1, 380, prog(t, F(tl, "c11", 0.35), 0.35), 12, CORAL)
    head2(cr, t, "FOR BRAHMA:", "1 MOMENT", F(tl, "c11", 0.3), tm - 0.1, y=500, small_size=56, big_size=190)
    box = (80, 500 + 56 * 1.2, text_size("1 MOMENT", 190)[0], text_size("1 MOMENT", 190)[1])
    ring(cr, box[0] + box[2] / 2, box[1] + box[3] / 2, box[2] * 0.6, box[3] * 0.75, prog(t, tm + 0.25, 0.45), 10, CORAL)


def s_split(cr, t, tl, t0, t1):
    """c12: the same boys in two places: asleep in Brahma's cave AND playing with Krishna (callback to the hook)."""
    ground(cr, "night")
    tsl = C(tl, "c12", "सो रहे", "ಮಲಗಿದ್ದಾರೆ", 0.4) - 0.3
    tpl = C(tl, "c12", "कृष्ण", "ಕೃಷ್ಣನ", 0.62) - 0.2
    u = sm((t - t0) / max(0.5, t1 - t0))
    sh_ = sm((t - (tpl - 0.25)) / 0.6)
    top = (70, lerp(420, 300, sh_), 940, lerp(980, 620, sh_))
    bot = (70, 990, 940, 620)

    def cave(c):
        cam = (lerp(2560, 2620, u), lerp(1760, 1800, u), lerp(1.15, 1.25, u))
        c.translate(top[0] + top[2] / 2, top[1] + top[3] / 2)
        c.scale(cam[2], cam[2])
        c.translate(-cam[0], -cam[1])
        blit(c, "plate_141755", 0, 0, cam[2])
        glow(c, 2620, 1850, 300, (0.7, 0.75, 1.0), 0.2)

    def play(c):
        cam = (lerp(2050, 2150, u), lerp(1850, 1800, u), lerp(0.66, 0.72, u))
        c.translate(bot[0] + bot[2] / 2, bot[1] + bot[3] / 2)
        c.scale(cam[2], cam[2])
        c.translate(-cam[0], -cam[1])
        blit(c, PAINT["dive"], 0, 0, cam[2])
        glow(c, 2240, 1650, 300, GOLD_L, 0.25 * prog(t, tpl, 0.5))

    a1 = prog(t, t0, 0.35)
    a2 = prog(t, tpl - 0.2, 0.35)
    panel(cr, top, cave, alpha=a1)
    panel(cr, bot, play, alpha=a2)
    label(cr, t, tsl, "ASLEEP IN BRAHMA'S CAVE", W / 2, top[1] + 52, 28, fill=(0.10, 0.10, 0.25))
    if t < tpl:
        stext(cr, "?", W / 2, 1560, 110, GOLD_L, 0.6 * prog(t, tsl + 0.4, 0.4), anchor="cm")
    label(cr, t, tpl + 0.1, "PLAYING WITH KRISHNA", W / 2, bot[1] + bot[3] - 52, 28, fill=(0.06, 0.12, 0.30))
    head2(cr, t, "HE CAME BACK AND SAW", "", t0 + 0.1, t0 + 99, y=180, small_size=56, center=True)
    tq = F(tl, "c12", 0.86)
    if t > tq - 0.2:
        ba = prog(t, tq - 0.1, 0.3)
        g = cairo.LinearGradient(0, 820, 0, 1060)
        g.add_color_stop_rgba(0, 0.04, 0.02, 0.05, 0)
        g.add_color_stop_rgba(0.3, 0.04, 0.02, 0.05, 0.75 * ba)
        g.add_color_stop_rgba(0.7, 0.04, 0.02, 0.05, 0.75 * ba)
        g.add_color_stop_rgba(1, 0.04, 0.02, 0.05, 0)
        cr.set_source(g)
        cr.rectangle(0, 820, W, 240)
        cr.fill()
        box = head2(cr, t, "", "SO HOW?", 0, tq, y=862, big_size=150, center=True)
        if box:
            bx, by_, bw, bh = box
            ring(cr, bx + bw / 2, by_ + bh / 2, bw * 0.62, bh * 0.75, prog(t, tq + 0.3, 0.45), 9, CORAL)


def s_vishnu(cr, t, tl, t0, t1):
    """c13: suddenly every boy and every calf appears as four-armed Vishnu."""
    ground(cr, "indigo")
    tv = C(tl, "c13", "विष्णु", "ವಿಷ್ಣುವಿನ", 0.75) - 0.6
    ta = C(tl, "c13", "अचानक", "ಇದ್ದಕ್ಕಿದ್ದಂತೆ", 0.12)
    z = lerp(1.0, 1.08, sm((t - t0) / max(0.5, t1 - t0)))
    cr.save()
    cr.translate(540, 1100)
    cr.scale(z, z)
    cr.translate(-540, -1100)
    rays(cr, 540, 900, 1300, t, 0.25 + 0.45 * prog(t, tv, 0.5))
    glow(cr, 540, 1000, 700, (0.55, 0.65, 1.0), 0.15 + 0.25 * prog(t, tv, 0.5))
    wave = sm((t - ta) / 0.8) * (1 - sm((t - ta - 0.8) / 0.5))
    _krishna_crowd(cr, t, tl, t0 - 5, t0 - 5, t0 - 5, vishnu_at=tv, krishna=True)
    if wave > 0:
        flash(cr, 0.25 * wave, (0.8, 0.85, 1.0))
    vb = prog(t, tv + 0.6, 0.6)
    if vb > 0:
        glow(cr, 540, 880, 520, GOLD_L, 0.4 * vb)
        ring_halo(cr, 540, 820, 330, vb, t)
        fig(cr, "vishnu_garuda", 540, 870, lerp(500, 640, vb), 0.6 * vb, kind="aura", anchor="c")
        fig(cr, "vishnu_garuda", 540, 870, lerp(500, 640, vb), vb, anchor="c")
    cr.restore()
    flash(cr, 0.6 * (1 - sm((t - tv) / 0.5)) * float(t >= tv), (0.95, 0.9, 1.0))
    dust(cr, t, 0.9, 80, seed_off=5)
    head2(cr, t, "EVERY BOY, EVERY CALF", "", t0 + 0.1, t0 + 99, y=250, small_size=60, center=True)
    if t >= tv + 0.3:
        head2(cr, t, "", "VISHNU", 0, tv + 0.5, y=250 + 72, big_size=180, big_color=GOLD_L, center=True)
        label(cr, t, tv + 0.9, "FOUR-ARMED: CONCH, DISC, MACE, LOTUS", W / 2, 1180, 26, fill=(0.06, 0.12, 0.30))


def s_feet(cr, t, tl, t0, t1):
    """c14: Brahma falls at Krishna's feet (both as whole painted figures; a bow, petals, light)."""
    ground(cr, "indigo")
    tf = C(tl, "c14", "चरणों", "ಕಾಲಿಗೆ", 0.55) - 0.4
    z = lerp(1.0, 1.05, sm((t - t0) / max(0.5, t1 - t0)))
    cr.save()
    cr.translate(540, 1000)
    cr.scale(z, z)
    cr.translate(-540, -1000)
    rays(cr, 540, 520, 1100, t, 0.4)
    mandala(cr, 540, 520, 230, t, 0.8)
    glow(cr, 540, 700, 600, GOLD_L, 0.3)
    fig(cr, "krishna_flute", 560, 1420, 940, 0.6, kind="aura")
    fig(cr, "krishna_flute", 560, 1420, 940)
    q = sm((t - (t0 + 0.1)) / max(0.6, tf + 0.6 - t0))
    by = lerp(2150, 1800, q)
    rot = lerp(0.0, -0.20, sm((t - tf) / 0.8))
    fig(cr, "brahma_k", 540, by, 580, 0.5, kind="aura", rot=rot)
    fig(cr, "brahma_k", 540, by, 580, 1.0, rot=rot)
    cr.restore()
    petals(cr, t, t0 - 1.5, 1.0, 34, 1.0, seed_off=21)
    dust(cr, t, 0.7, 60, seed_off=15)
    head2(cr, t, "BRAHMA FELL", "AT KRISHNA'S FEET", t0 + 0.1, tf + 0.2, y=230, small_size=62, big_size=120,
          big_color=GOLD_L, center=True)


def s_wake(cr, t, tl, t0, t1):
    """c15: the boys wake: "Krishna, back so soon? We haven't eaten a bite!" (the lunch painting, morning light)."""
    u = sm((t - t0) / max(0.5, t1 - t0))
    cam = clamp_cam(lerp(600, 700, u), lerp(1480, 1560, u), lerp(1.30, 1.42, u), (40, 45, 3385, 2330))
    ref = (650, 1545)
    cr.save()
    camera(cr, *cam)
    blit(cr, "plate_146117", 0, 0, cam[2])
    layer_at(cr, "boys_lunch", cam, ref, 1.10)
    for i in range(10):
        x = 120 + (i * 233.7) % 1200
        y = 2190 + (i * 61.3) % 110
        sparkle(cr, x, y, 14, 0.7 * max(0, math.sin(t * 2.4 + i * 1.7)) ** 3)
    cr.restore()
    sun_wash(cr, 0.55, (1.0, 0.85, 0.55))
    rays(cr, 1100, -150, 1700, t, 0.25, 0.01, seed=5)
    dust(cr, t, 0.5, 40, seed_off=25)
    tw = C(tl, "c15", "जागे", "ಎದ್ದಾಗ", 0.15)
    tq = C(tl, "c15", "जल्दी", "ಬೇಗ", 0.45) - 0.4
    tb = C(tl, "c15", "निवाला", "ತುತ್ತೂ", 0.85) - 0.6
    label(cr, t, tw - 0.1, "THE BOYS WAKE UP", W / 2, 300, 32, t1=tq + 0.6)
    bubble(cr, t, tq, "KRISHNA,\nBACK SO SOON?", 560, 520, 62, tail=(-0.6, 1))
    bubble(cr, t, tb, "WE HAVEN'T EATEN\nA SINGLE BITE!", 520, 1580, 58, tail=(0.2, -1.6))


def s_village(cr, t, tl, t0, t1):
    """c16: a whole village fed God for a year, and nobody knew (the Braj crowd and their cows, 162094)."""
    u = sm((t - t0) / max(0.5, t1 - t0))
    cam = clamp_cam(lerp(1000, 1400, u), lerp(2150, 2080, u), lerp(0.86, 0.92, u), (150, 1000, 2330, 3245))
    cr.save()
    camera(cr, *cam)
    blit(cr, PAINT["govardhan"], 0, 0, cam[2])
    glow(cr, 1050, 1350, 420, GOLD_L, 0.35 * (0.8 + 0.2 * math.sin(t * 2)))
    cr.restore()
    sun_wash(cr, 0.6, (1.0, 0.72, 0.35))
    dust(cr, t, 0.7, 60, seed_off=35)
    petals(cr, t, t0 + 0.3, 0.8, 18, 0.7, seed_off=40)
    tg = C(tl, "c16", "भगवान", "ದೇವರಿಗೇ", 0.35) - 0.2
    tn = C(tl, "c16", "पता", "ಗೊತ್ತೇ", 0.85) - 0.1
    g = cairo.LinearGradient(0, 1060, 0, 1800)          # text sits low here: Krishna's face stays clear at the top
    g.add_color_stop_rgba(0, 0.05, 0.03, 0.02, 0)
    g.add_color_stop_rgba(0.28, 0.05, 0.03, 0.02, 0.62)
    g.add_color_stop_rgba(0.75, 0.05, 0.03, 0.02, 0.62)
    g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
    cr.set_source(g)
    cr.rectangle(0, 1060, W, 740)
    cr.fill()
    head2(cr, t, "A WHOLE VILLAGE", "FED GOD", t0 + 0.1, tg, y=1150, small_size=64, big_size=200, big_color=GOLD_L)
    label(cr, t, tg + 0.5, "FOR A WHOLE YEAR", 80, 1560, 32, anchor="l", fill=(0.35, 0.08, 0.10))
    plate_stamp(cr, t, "AND NOBODY KNEW", tn, W / 2 + 40, 960, size=80, color=GOLD_L, rot=-0.05)


def s_end(cr, t, tl, t0, t1):
    """c17: closing YES / NO card over Krishna among the boys he became."""
    ground(cr, "indigo")
    cr.save()
    z = lerp(1.04, 1.0, sm((t - t0) / max(0.5, t1 - t0)))
    cr.translate(540, 1200)
    cr.scale(z, z)
    cr.translate(-540, -1200)
    glow(cr, 540, 900, 650, (1.0, 0.72, 0.35), 0.22)
    rays(cr, 540, 760, 1000, t, 0.2)
    _krishna_crowd(cr, t, tl, t0 - 5, t0 - 5, t0 - 5, alpha=0.85)
    cr.restore()
    cr.set_source_rgba(0.03, 0.02, 0.06, 0.30)
    cr.paint()
    dust(cr, t, 0.7, 50, seed_off=45)
    head2(cr, t, "IF YOU LIVED IN THAT VILLAGE,", "", t0 + 0.1, t0 + 99, y=250, small_size=56, center=True)
    head2(cr, t, "", "WOULD YOU KNOW?", 0, t0 + 0.6, y=330, big_size=150, big_color=GOLD_L, center=True)
    ty = C(tl, "c17", "यस", "ಎಸ್", 0.6) - 0.3
    cr.save()
    cr.translate(W / 2, 1180)
    cr.scale(1.35, 1.35)
    yes_no_card(cr, t, ty, 0, 0, question="COMMENT: YES OR NO")
    cr.restore()
    credit(cr, prog(t, t0 + 0.5, 0.4), y=1470)


SHOTS = [  # (line id, cue fraction or None, function, cross-fade seconds in)
    ("c1", None, s_brahma, 0.0),
    ("c3", None, s_lunch, 0.0),
    ("c4", None, s_forest, 0.25),
    ("c5", None, s_hide, 0.25),
    ("c6", None, s_cave, 0.25),
    ("c7", None, s_multiply, 0.2),
    ("c8", None, s_same, 0.2),
    ("c9", None, s_evening, 0.25),
    ("c9", 0.33, s_hug, 0.35),
    ("c10", None, s_year, 0.3),
    ("c11", None, s_moment, 0.2),
    ("c12", None, s_split, 0.2),
    ("c13", None, s_vishnu, 0.25),
    ("c14", None, s_feet, 0.25),
    ("c15", None, s_wake, 0.3),
    ("c16", None, s_village, 0.3),
    ("c17", None, s_end, 0.35),
]
LEAD = 0.12


def shot_starts(tl):
    cached = getattr(tl, "_bc_starts", None)
    if cached is None:
        out = []
        for k, (bid, cue, _, _) in enumerate(SHOTS):
            if k == 0:
                out.append(0.0)
                continue
            s = (T(tl, bid, cue) if cue is not None else tl[bid].start) - LEAD
            out.append(max(s, out[-1] + 0.6))
        cached = tl._bc_starts = out
    return cached


def draw(cr, t, tl):
    st = shot_starts(tl)
    k = max(i for i, s in enumerate(st) if t >= s) if t >= 0 else 0
    t0 = st[k]
    t1 = st[k + 1] if k + 1 < len(st) else tl.total
    cr.set_source_rgb(0, 0, 0)
    cr.paint()
    fn, xf = SHOTS[k][2], SHOTS[k][3]
    if k > 0 and xf > 0 and t < t0 + xf:
        SHOTS[k - 1][2](cr, t, tl, st[k - 1], t0)
        cr.push_group()
        fn(cr, t, tl, t0, t1)
        cr.pop_group_to_source()
        cr.paint_with_alpha(sm((t - t0) / xf))
    else:
        fn(cr, t, tl, t0, t1)
    finish(cr, t)


# ---------------------------------------------------------------- sound

_HAVE = {}


def _have(name):
    """True if motion.audio can make this sound (the mythology sounds were added on 6 Nov 2026)."""
    if name not in _HAVE:
        try:
            from motion import audio
            _HAVE[name] = audio.sfx(name, 0.5) is not None or audio.thriller_sfx(name, 0.5) is not None
        except Exception:
            _HAVE[name] = False
    return _HAVE[name]


FALLBACK = {"bell": "ding", "conch": "riser", "shimmer": "ding", "damaru": "knock"}


def sfx(tl):
    """(time, name, duration): a shimmer on frame 0, a temple bell as the story starts, whooshes on cuts, shimmer on
    every divine moment, a conch when Vishnu appears, ticks and music dips before the reveals."""
    st = shot_starts(tl)
    ev = [(s, "whoosh", 0.25) for s in st[1:]]
    ev += [(0.0, "shimmer", 1.2), (1.0, "thud", 0.0),
           (C(tl, "c1", "कैसे", "ಹೇಗೆ", 0.85), "scribble", 0.4),
           (C(tl, "c2", "साल", "ವರ್ಷ", 0.85) - 0.1, "hit", 0.0),
           (T(tl, "c3") - 0.1, "bell", 2.5),
           (C(tl, "c5", "ग्वाल", "ಗೋಪಾಲಕ", 0.6) - 0.2, "shimmer", 1.5),
           (C(tl, "c5", "छुपा", "ಬಚ್ಚಿಟ್ಟು", 0.9), "thud", 0.0),
           (C(tl, "c7", "हर एक बच्चा", "ಪ್ರತಿಯೊಬ್ಬ", 0.55) - 0.15, "shimmer", 1.6),
           (C(tl, "c7", "बछड़ा", "ಕರುವೂ", 0.85) - 0.15, "shimmer", 1.0),
           (C(tl, "c8", "फ़र्क़", "ಎಕ್ಸಾಕ್ಟ್", 0.85) - 0.05, "thud", 0.0),
           (C(tl, "c9", "उमड़", "ಜಾಸ್ತಿ", 0.88) - 0.2, "shimmer", 1.2),
           (C(tl, "c10", "पता", "ಗೊತ್ತಾಗ್ಲಿಲ್ಲ", 0.75), "thud", 0.0),
           (C(tl, "c11", "पल", "ಕ್ಷಣ", 0.85) + 0.2, "scribble", 0.4),
           (F(tl, "c12", 0.86), "hit", 0.0),
           (C(tl, "c13", "विष्णु", "ವಿಷ್ಣುವಿನ", 0.75) - 0.6, "conch", 2.5),
           (C(tl, "c13", "विष्णु", "ವಿಷ್ಣುವಿನ", 0.75) - 0.6, "shimmer", 2.0),
           (T(tl, "c14") - 0.05, "bell", 2.5),
           (C(tl, "c16", "पता", "ಗೊತ್ತೇ", 0.85) - 0.1, "thud", 0.0)]
    for bid in ("c3", "c15"):
        ev.append((tl[bid].start + 0.6, "pop", 0.0))
    ev += [(C(tl, "c15", "जल्दी", "ಬೇಗ", 0.45) - 0.4, "pop", 0.0),
           (C(tl, "c15", "निवाला", "ತುತ್ತೂ", 0.85) - 0.6, "pop", 0.0)]
    for i, (w_hi, w_kn, fr) in enumerate((("शक्ल", "ಮುಖ", 0.08), ("कपड़े", "ಡ್ರೆಸ್", 0.25), ("बांसुरी", "ಕೊಳಲು", 0.43),
                                          ("आदतें", "ಹ್ಯಾಬಿಟ್ಸ್", 0.6))):
        ev.append((C(tl, "c8", w_hi, w_kn, fr) + 0.15, "tick", 0.0))
    for bid in ("c7", "c11", "c14", "c17"):
        ev.append((tl[bid].start - 0.35, "tick", 0.0))
        ev.append((tl[bid].start - 0.35, "dip", 0.5))
    out = []
    for at, name, dur in ev:
        if name not in ("dip", "hush") and not _have(name):
            name = FALLBACK.get(name, name)
        out.append((max(0.0, at), name, dur))
    return sorted(out, key=lambda e: e[0])
