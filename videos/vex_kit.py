"""The Vex series kit (from 3 Nov 2026): Vex the baby vampire as a 2D sprite (the owner's ChatGPT art) on photos of
the owner's home, grounded with real floor shadows, plus his props. Poses are PNGs in assets/mascot/vex/; add new ones
to POSES (feet and eye centres are measured from the image, see experiments/mascot_test/README.md).

  vex(cr, t, x, y, s, ...)     Vex with his feet at (x, y): squash, jelly wobble, lean/spin, lift (jumps), auto blinks
  reply(cr, t, start, end, x, y, text)   his line as small red handwriting over his head (the reference's look)
  photo(cr, t, name, start)    one of the owner's photos (assets/mascot/photos/crops) with a slow push-in
  pufferfish(cr, t, x, y, s, puff)       a flat-style pufferfish that inflates (puff 0..1) into a spiky ball
  bowl_back / bowl_front       a fishbowl around it; dizzy, carrot, skull, pan, bacteria, worm, chef_hat props
"""
import math
import os

import cairo
import numpy as np

from motion.engine import W, H, hexc, lerp, seg
from motion.polish import appear, bold_text, ellipse, paint, rad, rrect, stroke_line

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = (0.1, 0.06, 0.08, 1)
RED = (0.92, 0.12, 0.15, 1)

POSES = {   # name -> png, eye centres (image px), lid colour (flat skin)
    "front": dict(png="assets/mascot/vex/vex_flat_front.png", eyes=((397, 570), (705, 590)), eye_r=(110, 98),
                  lid=(0.867, 0.796, 0.925)),
}
_cache = {}


def _pose(name):
    if name in _cache:
        return _cache[name]
    p = POSES[name]
    img = cairo.ImageSurface.create_from_png(os.path.join(ROOT, p["png"]))
    w, h = img.get_width(), img.get_height()
    a = np.ndarray((h, w, 4), np.uint8, img.get_data(), strides=(img.get_stride(), 4, 1))[..., 3]
    sole = max(y for y in range(h) if (a[y] > 40).any())
    rows = a[sole - 60:sole - 4] > 40
    cols = np.where(rows.any(0))[0]
    gaps = np.where(np.diff(cols) > 6)[0]
    boots = [(cols[0], cols[gaps[0]]), (cols[gaps[0] + 1], cols[-1])] if len(gaps) else [(cols[0], cols[-1])]
    sil = cairo.ImageSurface(cairo.FORMAT_ARGB32, w // 10 + 2, h // 10 + 2)
    c = cairo.Context(sil)
    c.scale(0.1, 0.1)
    c.set_source_rgba(0, 0, 0, 1)
    c.mask_surface(img, 0, 0)
    d = dict(img=img, w=w, h=h, foot=((cols[0] + cols[-1]) / 2, sole), boots=boots, sil=sil, **p)
    _cache[name] = d
    return d


def _lids(c, P, k):
    if k <= 0:
        return
    rx, ry = P["eye_r"]
    for ex, ey in P["eyes"]:
        c.save()
        c.translate(ex, ey)
        c.scale(rx, ry)
        c.arc(0, 0, 1, 0, 2 * math.pi)
        c.restore()
        c.save()
        c.clip()
        c.rectangle(ex - rx - 6, ey - ry - 4, 2 * rx + 12, (2 * ry + 8) * k)
        c.set_source_rgba(*P["lid"], 1)
        c.fill()
        c.restore()
        if k > 0.85:
            c.move_to(ex - rx * 0.8, ey + 8)
            c.curve_to(ex - rx * 0.36, ey + 44, ex + rx * 0.36, ey + 44, ex + rx * 0.8, ey + 8)
            c.set_source_rgba(*INK)
            c.set_line_width(14)
            c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.stroke()


def _sprite(P, name, blink, wobble):
    """The pose with lids and jelly wobble, softened ~0.6 px (cached for the common still case)."""
    key = (name, round(blink, 2), round(wobble))
    if key in _cache:
        return _cache[key]
    w, h, pad = P["w"], P["h"], 40
    base = cairo.ImageSurface(cairo.FORMAT_ARGB32, w + 2 * pad, h)
    c = cairo.Context(base)
    if abs(wobble) < 0.5:
        c.set_source_surface(P["img"], pad, 0)
        c.paint()
    else:
        for y0 in range(0, h, 4):       # the top lags behind, the boots stay planted
            c.save()
            c.rectangle(0, y0, w + 2 * pad, 4)
            c.clip()
            c.set_source_surface(P["img"], pad + round(wobble * (1 - y0 / h) ** 1.6), 0)
            c.paint()
            c.restore()
    c.save()
    c.translate(pad + wobble * 0.62, 0)
    _lids(c, P, blink)
    c.restore()
    c.set_operator(cairo.OPERATOR_ATOP)  # a faint wash of the room's light
    c.set_source_rgba(0.55, 0.55, 0.56, 0.06)
    c.paint()
    soft = cairo.ImageSurface(cairo.FORMAT_ARGB32, w + 2 * pad + 8, h + 8)
    c = cairo.Context(soft)
    c.set_operator(cairo.OPERATOR_ADD)
    for ox, oy in ((-3.5, 0), (3.5, 0), (0, -3.5), (0, 3.5)):
        c.set_source_surface(base, 4 + ox, 4 + oy)
        c.paint_with_alpha(0.25)
    if blink == 0 and abs(wobble) < 0.5:
        _cache[key] = (soft, pad)
    return soft, pad


def auto_blink(t, seed=0.0):
    u = (t + 1.3 + seed) % 2.9
    return max(0.0, 1 - abs(u - 0.08) / 0.08) if u < 0.16 else 0.0


def shadows(cr, P, x, y, s, lift=0.0, alpha=1.0):
    """Floor shadows: his silhouette laid flat behind him, an occlusion pool, a contact shadow under each boot."""
    fade = alpha / (1 + lift / 60)
    cr.save()
    cr.translate(x, y)
    cr.transform(cairo.Matrix(1, 0, 0.12, 0.2, 0, 0))
    cr.scale(s * 10, s * 10)
    cr.translate(-P["foot"][0] / 10, -P["foot"][1] / 10)
    cr.set_source_surface(P["sil"], 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(0.16 * fade)
    cr.restore()
    b0, b1 = P["boots"][0][0], P["boots"][-1][1]
    w = (b1 - b0) * s
    grow = 1 + lift / 200
    for rx, ry, a in ((w * 0.75, w * 0.13, 0.22), (w * 0.5, w * 0.08, 0.3)):
        cr.save()
        cr.translate(x, y - 2)
        cr.scale(rx * grow, ry * grow)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y - 2, rx * grow, [(0, (0.08, 0.06, 0.05, a * fade)), (1, (0.08, 0.06, 0.05, 0))]))
        cr.fill()
    if lift < 4:
        for c0, c1 in P["boots"]:
            bx = x + ((c0 + c1) / 2 - P["foot"][0]) * s
            bw = (c1 - c0) * s * 0.55
            cr.save()
            cr.translate(bx, y - 1)
            cr.scale(bw, bw * 0.22)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.set_source(rad(bx, y - 1, bw, [(0, (0.05, 0.03, 0.03, 0.55 * alpha)), (1, (0.05, 0.03, 0.03, 0))]))
            cr.fill()


def vex(cr, t, x, y, s=0.19, pose="front", squash=0.0, wobble=0.0, blink=None, rot=0.0, pivot="feet", lift=0.0,
        flip=False, alpha=1.0, ground=True):
    """Vex with his feet at (x, y) on the floor. lift = px above the floor (jumps); rot leans (pivot "feet") or spins
    (pivot "center"); squash > 0 = wide and short; wobble = sideways jelly at the top (px in image space)."""
    P = _pose(pose)
    if blink is None:
        blink = auto_blink(t)
    if ground:
        shadows(cr, P, x, y, s, lift, alpha)
    spr, pad = _sprite(P, pose, min(1.0, blink * 1.6), wobble)
    fx, fy = P["foot"]
    cr.save()
    cr.translate(x, y - lift)
    if pivot == "center":
        cr.translate(0, -fy * s * 0.5)
        cr.rotate(rot)
        cr.translate(0, fy * s * 0.5)
    else:
        cr.rotate(rot)
    cr.scale(s * (1 + 0.14 * squash) * (-1 if flip else 1), s * (1 - 0.16 * squash))
    cr.translate(-fx - pad - 4, -fy - 4)
    cr.set_source_surface(spr, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(alpha)
    cr.restore()


def head_top(y, s, pose="front"):
    return y - _pose(pose)["foot"][1] * s


def reply(cr, t, start, end, x, y, text, size=42):
    """Vex's line in small red handwriting (Kalam) over his head, popping in at `start`, gone after `end`."""
    if t < start or t > end + 0.25:
        return
    k = appear(t, start, 0.3) * (1 - seg(t, end, end + 0.25))
    if k <= 0.01:
        return
    from motion.polish import text_width
    half = text_width(cr, text, size, "Kalam") / 2 + size * 0.2
    x = min(max(x, half + 16), W - half - 16)          # keep the whole line on screen
    cr.save()
    cr.translate(x, y + 3 * math.sin(t * 5))
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, RED, font="Kalam", outline=(1, 1, 1, 1), ow=size * 0.17, shadow=0)
    cr.restore()


# ---------------------------------------------------------------- the owner's photos
_photos = {}


def photo(cr, t, name, start=0.0, push=0.05, dur=6.0, focus=(360, 640)):
    """A photo from assets/mascot/photos/crops, with a slow push-in toward `focus` (no shot is ever static)."""
    if name not in _photos:
        _photos[name] = cairo.ImageSurface.create_from_png(os.path.join(ROOT, "assets/mascot/photos/crops",
                                                                         name + ".png"))
    z = 1 + push * min(1.0, max(0.0, (t - start) / dur))
    cr.save()
    cr.translate(focus[0], focus[1])
    cr.scale(z, z)
    cr.translate(-focus[0], -focus[1])
    cr.set_source_surface(_photos[name], 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()
    return z


def zoom_at(cr, z, focus=(360, 640)):
    """Apply the same push-in to things standing on the photo, so they stay put on the floor."""
    cr.translate(focus[0], focus[1])
    cr.scale(z, z)
    cr.translate(-focus[0], -focus[1])


_rng = np.random.default_rng(11)


def grain(cr, sigma=2.2):
    """Phone-video grain over everything drawn so far (photo + sprites), so the cartoon sits in the footage."""
    sf = cr.get_target()
    sf.flush()
    a = np.ndarray((sf.get_height(), sf.get_width(), 4), np.uint8, sf.get_data(), strides=(sf.get_stride(), 4, 1))
    n = _rng.normal(0, sigma, (a.shape[0], a.shape[1], 1)).astype(np.float32)
    a[..., :3] = (a[..., :3].astype(np.float32) + n).clip(0, 255).astype(np.uint8)
    sf.mark_dirty()


# ---------------------------------------------------------------- props (flat 2D, thick outline, like Vex)
FISH = hexc("#f2c94c")
FISH_BELLY = hexc("#fff4dc")
FIN = hexc("#f0a040")


def pufferfish(cr, t, x, y, s=1.0, puff=0.0, facing=1, eyes="open", flap=True):
    """A cute pufferfish, centre (x, y), facing right; puff 0..1 blows it up into an angry spiky ball."""
    if s <= 0.01:
        return
    p = max(0.0, min(1.0, puff))
    rx, ry = 70 + 44 * p, 48 + 62 * p
    cr.save()
    cr.translate(x, y + (4 * math.sin(t * 3) if flap else 0))
    cr.scale(s * facing, s)
    # tail fin
    ft = 0.25 * math.sin(t * 9) if flap else 0
    cr.save()
    cr.translate(-rx + 6, 0)
    cr.rotate(ft)
    cr.move_to(0, 0)
    cr.curve_to(-30, -40, -46, -34, -44, -4)
    cr.curve_to(-46, 26, -30, 40, 0, 0)
    paint(cr, FIN, INK, 5)
    cr.restore()
    # spikes
    if p > 0.03:
        n = 20
        for k in range(n):
            a = 2 * math.pi * k / n + 0.1
            bx, by = rx * math.cos(a), ry * math.sin(a)
            ln = (10 + 24 * p)
            nx, ny = math.cos(a), math.sin(a)
            tx, ty = -ny * 9, nx * 9
            cr.move_to(bx * 0.92 + tx, by * 0.92 + ty)
            cr.line_to(bx + nx * ln, by + ny * ln)
            cr.line_to(bx * 0.92 - tx, by * 0.92 - ty)
            cr.close_path()
            paint(cr, FISH_BELLY, INK, 4)
    # body: yellow back, cream belly
    ellipse(cr, 0, 0, rx, ry)
    paint(cr, FISH, None, 0)
    cr.save()
    ellipse(cr, 0, 0, rx, ry)
    cr.clip()
    ellipse(cr, 0, ry * 0.55, rx * 1.05, ry * 0.75)
    paint(cr, FISH_BELLY, None, 0)
    for sx, sy, r in ((-30, -22, 7), (-5, -32, 6), (20, -24, 5), (-45, -5, 5), (-15, -10, 4)):
        ellipse(cr, sx * rx / 70, sy * ry / 48, r, r)
        paint(cr, hexc("#b8862a"), None, 0)
    cr.restore()
    ellipse(cr, 0, 0, rx, ry)
    paint(cr, None, INK, 5)
    # side fin
    cr.save()
    cr.translate(rx * 0.05, ry * 0.25)
    cr.rotate(0.3 * math.sin(t * 7) if flap else 0)
    cr.move_to(0, 0)
    cr.curve_to(-18, 10, -26, 28, -8, 30)
    cr.curve_to(4, 26, 6, 12, 0, 0)
    paint(cr, FIN, INK, 4)
    cr.restore()
    # face
    ex, ey, er = rx * 0.48, -ry * 0.22, 15 + 3 * p
    if eyes == "dizzy":
        for k in range(14):
            a = k * 0.7
            cr.line_to(ex + math.cos(a) * k * 0.9, ey + math.sin(a) * k * 0.9)
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.stroke()
    else:
        ellipse(cr, ex, ey, er, er)
        paint(cr, (1, 1, 1, 1), INK, 4)
        ellipse(cr, ex + 4, ey + 1, er * 0.52, er * 0.6)
        paint(cr, INK, None, 0)
        ellipse(cr, ex + 1, ey - 4, er * 0.2, er * 0.2)
        paint(cr, (1, 1, 1, 1), None, 0)
        if eyes == "angry" or p > 0.6:
            stroke_line(cr, [(ex - er * 1.1, ey - er * 1.3), (ex + er * 1.0, ey - er * 0.8)], 6, INK, curve=False)
    if p > 0.5:                          # angry red cheek
        ellipse(cr, ex - 6, ey + er * 1.6, 11, 6)
        paint(cr, (1, 0.45, 0.45, 0.8), None, 0)
    # mouth: pursed lips at the front
    ellipse(cr, rx * 0.96, ry * 0.12, 9 - 3 * p, 8 - 2 * p)
    paint(cr, hexc("#ff8fa0"), INK, 4)
    cr.restore()


def bowl_back(cr, x, y, r):
    """The back half of a round fishbowl standing at (x, y): glass tint and water (draw the fish after this)."""
    cx, cy = x, y - r
    cr.save()
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.clip()
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.85, 0.95, 1.0, 0.25)
    cr.fill()
    cr.rectangle(cx - r, cy - r * 0.45, 2 * r, 2 * r)
    cr.set_source(rad(cx - r * 0.3, cy - r * 0.2, r * 1.5, [(0, (0.6, 0.85, 0.98, 0.55)), (1, (0.35, 0.65, 0.9, 0.6))]))
    cr.fill()
    cr.restore()


def bowl_front(cr, x, y, r):
    """The glass, rim and shine over the fish."""
    cx, cy = x, y - r
    cr.save()
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.clip()
    ellipse(cr, cx, cy - r * 0.45, r * 0.95, r * 0.12)
    cr.set_source_rgba(1, 1, 1, 0.45)
    cr.set_line_width(4)
    cr.stroke()
    cr.restore()
    cr.arc(cx, cy, r, -0.9 * math.pi / 2 - 1.25, -0.9 * math.pi / 2 + 1.25 + math.pi)   # glass outline (open top)
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.stroke()
    ellipse(cr, cx, cy - r * 0.84, r * 0.56, r * 0.1)                                     # rim
    paint(cr, (1, 1, 1, 0.35), INK, 5)
    cr.arc(cx, cy, r * 0.78, math.pi * 1.1, math.pi * 1.45)                               # shine
    cr.set_source_rgba(1, 1, 1, 0.75)
    cr.set_line_width(9)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()


def floor_shadow(cr, x, y, w, a=0.35):
    for rx, ry, aa in ((w, w * 0.16, a * 0.6), (w * 0.7, w * 0.1, a)):
        cr.save()
        cr.translate(x, y)
        cr.scale(rx, ry)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y, rx, [(0, (0.06, 0.05, 0.05, aa)), (1, (0.06, 0.05, 0.05, 0))]))
        cr.fill()


def star(cr, x, y, r, col=(1, 0.85, 0.2, 1)):
    if r <= 0.01:
        return
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        (cr.move_to if k == 0 else cr.line_to)(x + rr * math.cos(a), y + rr * math.sin(a))
    cr.close_path()
    paint(cr, col, INK, 3)


def dizzy(cr, t, x, y, start, end=None, r=60):
    """Little stars circling over a dazed head."""
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.3)
    for j in range(3):
        a = t * 5 + j * 2 * math.pi / 3
        star(cr, x + math.cos(a) * r * k, y + math.sin(a) * r * 0.3 * k, 13 * k)


def skull(cr, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, 0, -6, 40, 36)
    paint(cr, (1, 1, 1, 1), INK, 5)
    rrect(cr, -22, 20, 44, 22, 8)
    paint(cr, (1, 1, 1, 1), INK, 5)
    for ex in (-15, 15):
        ellipse(cr, ex, -6, 11, 12)
        paint(cr, INK, None, 0)
    cr.move_to(0, 6)
    cr.line_to(-5, 16)
    cr.line_to(5, 16)
    cr.close_path()
    paint(cr, INK, None, 0)
    for tx in (-10, 0, 10):
        stroke_line(cr, [(tx, 24), (tx, 40)], 3, INK, curve=False)
    cr.restore()


def pan(cr, t, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for k in range(3):                    # flames under it
        fx = -36 + k * 36
        h = 34 + 8 * math.sin(t * 12 + k)
        cr.move_to(fx - 14, 40)
        cr.curve_to(fx - 16, 40 - h * 0.6, fx - 2, 40 - h, fx, 40 - h)
        cr.curve_to(fx + 4, 40 - h * 0.6, fx + 16, 40 - h * 0.4, fx + 14, 40)
        cr.close_path()
        paint(cr, (1, 0.55, 0.15, 1), INK, 3)
    rrect(cr, 60, -8, 90, 16, 8)
    paint(cr, hexc("#5a3a24"), INK, 4)
    ellipse(cr, 0, 0, 66, 22)
    paint(cr, hexc("#3a3a44"), INK, 5)
    ellipse(cr, 0, -3, 50, 13)
    paint(cr, hexc("#55555f"), None, 0)
    cr.restore()


def carrot(cr, x, y, s=1.0, rot=0.3):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    for a in (-0.5, 0, 0.5):
        cr.save()
        cr.rotate(a)
        ellipse(cr, 0, -40, 8, 20)
        paint(cr, hexc("#4caf50"), INK, 3)
        cr.restore()
    cr.move_to(-16, -22)
    cr.curve_to(-14, 10, -4, 40, 0, 50)
    cr.curve_to(4, 40, 14, 10, 16, -22)
    cr.close_path()
    paint(cr, hexc("#ff8a2a"), INK, 4)
    for ly in (-6, 10, 26):
        stroke_line(cr, [(-9, ly), (-2, ly + 3)], 3, INK, curve=False)
    cr.restore()


def bacteria(cr, t, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for j, (bx, by, r) in enumerate(((-22, 6, 20), (14, -10, 17), (20, 18, 14))):
        for k in range(4):
            a = t * 3 + k * 1.6 + j
            stroke_line(cr, [(bx + r * math.cos(a), by + r * math.sin(a)),
                             (bx + (r + 12) * math.cos(a + 0.3), by + (r + 12) * math.sin(a + 0.3))], 3, INK)
        ellipse(cr, bx, by, r * 1.15, r)
        paint(cr, hexc("#7bd36a"), INK, 4)
        ellipse(cr, bx - r * 0.3, by - r * 0.1, 3.5, 3.5)
        paint(cr, INK, None, 0)
        ellipse(cr, bx + r * 0.3, by - r * 0.1, 3.5, 3.5)
        paint(cr, INK, None, 0)
    cr.restore()


def worm(cr, t, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for k in range(6, -1, -1):
        wx, wy = -50 + k * 16, 8 * math.sin(t * 6 + k * 0.9)
        ellipse(cr, wx, wy, 14, 12)
        paint(cr, hexc("#f28fb0"), INK, 4)
    ellipse(cr, 50, 8 * math.sin(t * 6 + 6.3) - 4, 3.5, 3.5)
    paint(cr, INK, None, 0)
    cr.restore()


def chef_hat(cr, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for bx, by, r in ((-24, -20, 24), (0, -32, 28), (24, -20, 24)):
        ellipse(cr, bx, by, r, r)
        paint(cr, (1, 1, 1, 1), INK, 5)
    rrect(cr, -36, -16, 72, 40, 6)
    paint(cr, (1, 1, 1, 1), INK, 5)
    for k in range(3):
        stroke_line(cr, [(-18 + k * 18, -10), (-18 + k * 18, 18)], 3, (0.75, 0.75, 0.8, 1), curve=False)
    cr.restore()
