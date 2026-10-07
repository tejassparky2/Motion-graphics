"""The polished look: smooth vector shapes with gradients, soft blurred shadows and glows, bokeh and depth of
field, chunky signs, ticking counters and bold rounded captions. Videos opt in by importing from here; the
hand-drawn style in engine.py/kit.py is unchanged for everything else.

Expensive things (blurred sprites, painted backgrounds) are drawn once per process and cached, so a frame is mostly
cheap vector work plus a few cached bitmaps.
"""
import math
import random

import numpy as np
from scipy.ndimage import gaussian_filter

from .engine import H, W, _catmull, back_out, cairo, clamp01, cue, ease_out, hexc, lerp, seg

OUTLINE = hexc("#2b1d16")
WHITE = hexc("#ffffff")
DISPLAY = "Luckiest Guy"     # signs and counters
ROUND = "Fredoka"            # captions and small labels
CAPTION_Y = 905              # baseline: below faces, above the bottom ~25% the Shorts UI covers


# ---------------------------------------------------------------- colour
def shade(c, k):
    """k > 0 lightens toward white, k < 0 darkens toward black."""
    r, g, b = c[:3]
    a = c[3] if len(c) > 3 else 1.0
    if k >= 0:
        return (r + (1 - r) * k, g + (1 - g) * k, b + (1 - b) * k, a)
    return (r * (1 + k), g * (1 + k), b * (1 + k), a)


def alpha(c, a):
    return (*c[:3], a)


# ---------------------------------------------------------------- paths and paint
def ellipse(cr, cx, cy, rx, ry, rot=0.0):
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.scale(max(rx, 0.01), max(ry, 0.01))
    cr.new_sub_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()


def rrect(cr, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def smooth(cr, pts, closed=True):
    _catmull(cr, pts, closed)


def hexagon(cr, cx, cy, r, rot=0.0):
    for k in range(6):
        a = rot + k * math.pi / 3
        (cr.move_to if k == 0 else cr.line_to)(cx + r * math.cos(a), cy + r * math.sin(a))
    cr.close_path()


def lin(x0, y0, x1, y1, stops):
    p = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        p.add_color_stop_rgba(o, *c)
    return p


def rad(cx, cy, r1, stops, fx=None, fy=None, r0=0.0):
    p = cairo.RadialGradient(cx if fx is None else fx, cy if fy is None else fy, r0, cx, cy, r1)
    for o, c in stops:
        p.add_color_stop_rgba(o, *c)
    return p


def paint(cr, fill=None, stroke=OUTLINE, lw=5.0):
    """Fill (a colour or a cairo pattern) and outline the current path, then clear it."""
    if fill is not None:
        if isinstance(fill, cairo.Pattern):
            cr.set_source(fill)
        else:
            cr.set_source_rgba(*fill)
        if stroke is not None and lw:
            cr.fill_preserve()
        else:
            cr.fill()
    if stroke is not None and lw:
        cr.set_source_rgba(*stroke)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
    cr.new_path()


def stroke_line(cr, pts, lw, col, curve=True):
    if curve and len(pts) > 2:
        smooth(cr, pts, closed=False)
    else:
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
    paint(cr, None, col, lw)


# ---------------------------------------------------------------- blur and cached sprites
_SPRITES = {}


def _blur(surf, sigma):
    surf.flush()
    w, h, stride = surf.get_width(), surf.get_height(), surf.get_stride()
    a = np.ndarray((h, stride // 4, 4), np.uint8, surf.get_data())[:, :w].astype(np.float32)
    for c in range(4):    # premultiplied ARGB: blurring every channel the same way is correct
        a[..., c] = gaussian_filter(a[..., c], sigma)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    o = np.ndarray((h, out.get_stride() // 4, 4), np.uint8, out.get_data())
    o[:, :w] = np.clip(a + 0.5, 0, 255).astype(np.uint8)
    out.mark_dirty()
    return out


def sprite(key, w, h, draw, sigma=0.0, scale=1.0):
    """A cached bitmap of `draw(cr)` over a w x h box (origin at the box's top-left), optionally blurred.
    Blurred sprites are drawn at reduced `scale` (blur hides the lower resolution) to keep them cheap."""
    s = _SPRITES.get(key)
    if s is None:
        pad = int(math.ceil(sigma * 3))
        sw, sh = int((w + 2 * pad) * scale) + 2, int((h + 2 * pad) * scale) + 2
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
        cr = cairo.Context(surf)
        cr.scale(scale, scale)
        cr.translate(pad, pad)
        draw(cr)
        if sigma:
            surf = _blur(surf, sigma * scale)
        s = _SPRITES[key] = (surf, scale, pad)
    return s


def put(cr, spr, x, y, a=1.0, size=1.0):
    """Draw a sprite with its box's top-left at (x, y) in user space."""
    surf, scale, pad = spr
    cr.save()
    cr.translate(x, y)
    cr.scale(size / scale, size / scale)
    cr.translate(-pad * scale, -pad * scale)
    cr.set_source_surface(surf, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(a)
    cr.restore()


def tint(cr, spr, x, y, col, size=1.0):
    """Use a (white) sprite as a mask: paints `col` through it."""
    surf, scale, pad = spr
    cr.save()
    cr.translate(x, y)
    cr.scale(size / scale, size / scale)
    cr.translate(-pad * scale, -pad * scale)
    cr.set_source_rgba(*col)
    cr.mask_surface(surf, 0, 0)
    cr.restore()


def _disc(cr):
    cr.arc(50, 50, 50, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, 1)
    cr.fill()


def soft_disc(cr, cx, cy, r, col, blur=0.35):
    """A blurred disc of radius r (blur as a fraction of r): bokeh, glows, soft ground shadows."""
    key = ("disc", round(blur, 2))
    spr = sprite(key, 100, 100, _disc, sigma=100 * blur, scale=0.5)
    tint(cr, spr, cx - r, cy - r, col, size=r / 50)


def soft_rrect(cr, x, y, w, h, r, col, sigma=12):
    """A blurred rounded rectangle (drop shadows under signs and cards)."""
    key = ("rrect", int(w), int(h), int(r), int(sigma))
    spr = sprite(key, w, h, lambda c: (rrect(c, 0, 0, w, h, r), c.set_source_rgba(1, 1, 1, 1), c.fill()),
                 sigma=sigma, scale=0.5)
    tint(cr, spr, x, y, col)


def ground_shadow(cr, cx, cy, rx, a=0.28):
    cr.save()
    cr.translate(cx, cy)
    cr.scale(1, 0.22)
    soft_disc(cr, 0, 0, rx, (0.12, 0.06, 0.02, a), blur=0.3)
    cr.restore()


# ---------------------------------------------------------------- whole-frame layers
def vignette(cr, strength=0.38):
    spr = sprite(("vignette", round(strength, 2)), W, H, lambda c: (
        c.rectangle(0, 0, W, H),
        c.set_source(rad(W / 2, H * 0.46, H * 0.78, [(0.0, (0, 0, 0, 0)), (0.55, (0, 0, 0, 0)),
                                                     (1.0, (0.05, 0.02, 0.0, strength))])),
        c.fill()))
    cr.save()
    cr.identity_matrix()
    put(cr, spr, 0, 0)
    cr.restore()


def bokeh(cr, t, seed, n, cols, rmin=14, rmax=60, speed=6.0, area=(0, 0, W, H), alpha_=(0.10, 0.28)):
    """Out-of-focus lights drifting slowly (seeded, so every frame agrees)."""
    rng = random.Random(seed)
    x0, y0, w, h = area
    for _ in range(n):
        x, y = x0 + rng.random() * w, y0 + rng.random() * h
        r = lerp(rmin, rmax, rng.random() ** 1.6)
        ph = rng.random() * 6.28
        col = cols[rng.randrange(len(cols))]
        a = lerp(*alpha_, rng.random()) * (0.75 + 0.25 * math.sin(t * 1.3 + ph))
        dy = (y - t * speed * (0.4 + r / rmax)) % (h + 2 * rmax) + y0 - rmax
        dx = x + math.sin(t * 0.5 + ph) * 8
        soft_disc(cr, dx, dy, r, alpha(col, a), blur=0.18)


def light_rays(cr, t, x, y, n=5, length=1500, col=(1, 0.95, 0.8), a=0.10, spread=0.9, base=1.9):
    for k in range(n):
        ang = base + (k - n / 2) * spread / n + 0.03 * math.sin(t * 0.4 + k)
        wdt = 0.035 + 0.02 * ((k * 7) % 3)
        cr.move_to(x, y)
        cr.line_to(x + length * math.cos(ang - wdt), y + length * math.sin(ang - wdt))
        cr.line_to(x + length * math.cos(ang + wdt), y + length * math.sin(ang + wdt))
        cr.close_path()
        cr.set_source(rad(x, y, length, [(0, (*col, a)), (1, (*col, 0))]))
        cr.fill()


def particles(cr, t, seed, n, col, area=(0, 0, W, H), r=(1.5, 4.0), speed=18):
    """Floating pollen/dust motes."""
    rng = random.Random(seed)
    x0, y0, w, h = area
    for _ in range(n):
        px, py, ph = x0 + rng.random() * w, y0 + rng.random() * h, rng.random() * 6.28
        rr = lerp(*r, rng.random())
        yy = y0 + (py - y0 - t * speed * (0.5 + rng.random())) % h
        xx = px + math.sin(t * 0.9 + ph) * 14
        cr.arc(xx, yy, rr, 0, 2 * math.pi)
        cr.set_source_rgba(*col[:3], (col[3] if len(col) > 3 else 1) * (0.6 + 0.4 * math.sin(t * 2 + ph)))
        cr.fill()


# ---------------------------------------------------------------- camera
def camera(t, keys, dur=0.45):
    """Ease (smoothstep) between keys [(time, (zoom, fx, fy))]; fx, fy is the world point at screen centre."""
    keys = sorted(keys, key=lambda k: k[0])
    active = [k for k in keys if k[0] <= t]
    if not active:
        return keys[0][1]
    kt, v = active[-1]
    before = active[-2][1] if len(active) > 1 else v
    u = seg(t, kt, kt + dur)
    u = u * u * (3 - 2 * u)
    return tuple(lerp(a, b, u) for a, b in zip(before, v))


def enter(cr, cam, drift=0.0, t=0.0):
    """World transform for camera (zoom, fx, fy) plus an optional slow push-in so no shot is ever static."""
    z, fx, fy = cam
    z *= 1 + drift * t
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


# ---------------------------------------------------------------- text
def text_path(cr, s, x, y, size, font=DISPLAY, align="center"):
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    ext = cr.text_extents(s)
    if align == "center":
        x -= ext.x_advance / 2
    elif align == "right":
        x -= ext.x_advance
    cr.move_to(x, y)
    cr.text_path(s)
    return ext.x_advance


def text_width(cr, s, size, font=DISPLAY):
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    return cr.text_extents(s).x_advance


def bold_text(cr, s, x, y, size, col=WHITE, font=DISPLAY, outline=OUTLINE, ow=None, shadow=0.35, align="center"):
    """Chunky text: drop shadow, thick outline, fill (the sticker look of the signs)."""
    ow = size * 0.16 if ow is None else ow
    if shadow:
        text_path(cr, s, x, y + size * 0.08, size, font, align)
        cr.set_source_rgba(0, 0, 0, shadow)
        cr.set_line_width(ow)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
        cr.fill()
    if outline is not None:
        text_path(cr, s, x, y, size, font, align)
        cr.set_source_rgba(*outline)
        cr.set_line_width(ow)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(*col)
    cr.fill()


# ---------------------------------------------------------------- signs, counters, stamps
def appear(t, start, dur=0.4):
    """0 before `start`, then a bouncy 0 -> 1."""
    return back_out(seg(t, start, start + dur), 2.2) if t >= start else 0.0


def sign(cr, t, start, x, y, text, col=hexc("#ffcf3f"), tcol=WHITE, size=62, sub=None, sub_col=None, rot=-0.03,
         end=None, s=1.0, sound="pop", pad=30):
    """A chunky plate with a title (and optional subtitle) that bounces in at `start` and pops out at `end`."""
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    if k <= 0.01:
        return
    cue(sound, t, start)
    cr.save()
    tw = text_width(cr, text, size)
    sw = text_width(cr, sub, size * 0.5, ROUND) if sub else 0
    w = max(tw, sw) + 2 * pad
    h = size * 1.12 + (size * 0.62 if sub else 0) + pad
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k * s, k * s)
    soft_rrect(cr, -w / 2, -h / 2 + 12, w, h, 26, (0, 0, 0, 0.32), sigma=10)
    rrect(cr, -w / 2, -h / 2, w, h, 26)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, shade(col, 0.35)), (0.55, col), (1, shade(col, -0.18))]), OUTLINE, 6)
    rrect(cr, -w / 2 + 8, -h / 2 + 7, w - 16, h * 0.42, 20)
    cr.set_source(lin(0, -h / 2, 0, 0, [(0, (1, 1, 1, 0.45)), (1, (1, 1, 1, 0.0))]))
    cr.fill()
    ty = -h / 2 + pad / 2 + size * 0.86
    bold_text(cr, text, 0, ty, size, tcol)
    if sub:
        bold_text(cr, sub, 0, ty + size * 0.62, size * 0.5, sub_col or shade(col, -0.62), font=ROUND, outline=None,
                  shadow=0)
    cr.restore()


def counter(cr, t, start, x, y, value, size=96, dur=1.0, col=WHITE, prefix="", suffix="", sub=None, s=1.0):
    """A number that ticks up from 0 (ease-out) and lands with a bounce."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + dur))
    v = int(round(value * u))
    k = appear(t, start, 0.3) * (1 + 0.08 * math.sin(seg(t, start + dur, start + dur + 0.25) * math.pi))
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k * s, k * s)
    bold_text(cr, f"{prefix}{v:,}{suffix}", 0, 0, size, col)
    if sub:
        bold_text(cr, sub, 0, size * 0.62, size * 0.36, WHITE, font=ROUND, ow=size * 0.07, shadow=0.25)
    cr.restore()
    cue("pop", t, start + dur)


def stamp(cr, t, start, x, y, text, col=hexc("#e8473f"), size=70, rot=-0.12, end=None):
    """A rubber stamp that slams down (scale 1.6 -> 1)."""
    if t < start or (end is not None and t > end):
        return
    u = seg(t, start, start + 0.18)
    k = lerp(1.7, 1.0, ease_out(u))
    a = clamp01(u * 3)
    cue("hit", t, start)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(k, k)
    tw = text_width(cr, text, size)
    rrect(cr, -tw / 2 - 24, -size * 0.92, tw + 48, size * 1.3, 14)
    cr.set_source_rgba(*alpha(col, 0.12 * a))
    cr.fill_preserve()
    cr.set_source_rgba(*alpha(col, a))
    cr.set_line_width(7)
    cr.stroke()
    text_path(cr, text, 0, 0, size)
    cr.set_source_rgba(*alpha(col, a))
    cr.fill()
    cr.restore()


# ---------------------------------------------------------------- captions
_cap = {}


def captions(cr, t, tl, y=CAPTION_Y, size=58, max_w=600):
    """Bold rounded captions (Fredoka): 1-3 words, white with a dark outline, the spoken word in yellow,
    each chunk pops in."""
    from .captions import _chunks
    chunks = _cap.get(id(tl))
    if chunks is None:
        chunks = _cap[id(tl)] = _chunks(tl)
    for i, ch in enumerate(chunks):
        start = ch[0].start
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else tl.total
        stop = nxt if nxt - ch[-1].end < 0.5 else ch[-1].end + 0.25
        if start - 0.02 <= t < stop:
            _cap_draw(cr, t, ch, start, y, size, max_w)
            return


def _cap_draw(cr, t, chunk, start, y, size, max_w):
    words = [u.shown.rstrip(",.;:") or u.shown for u in chunk]
    cr.save()
    cr.identity_matrix()
    space = text_width(cr, " ", size, ROUND)
    widths = [text_width(cr, w, size, ROUND) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    if total > max_w:
        size *= max_w / total
        widths = [w * max_w / total for w in widths]
        space *= max_w / total
        total = max_w
    k = 0.8 + 0.2 * back_out(seg(t, start, start + 0.16), 2.0)
    cr.translate(W / 2, y)
    cr.scale(k, k)
    x = -total / 2
    for w, word, u in zip(widths, words, chunk):
        live = u.start - 0.03 <= t
        col = hexc("#ffd23f") if u.start - 0.03 <= t < u.end + 0.05 else WHITE
        if live or True:
            bold_text(cr, word, x, 0, size, col, font=ROUND, ow=size * 0.2, shadow=0.4, align="left")
        x += w + space
    cr.restore()
