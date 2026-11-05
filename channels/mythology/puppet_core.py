"""Togalu Gombeyaata (Karnataka leather shadow-puppet theatre), drawn in code: the lamp-lit cloth screen, translucent
punched-leather sprites, jointed rod puppets, rods, flicker and the camera.

How a frame is built (every step a pure function of t):
  screen(cr)                    the cached backlit cloth (warm centre, dark edges, weave, creases, oil stains)
  puppet / prop sprites         painted with OPERATOR_MULTIPLY: the leather is a coloured filter on the lamp light, so
                                puppets glow in the centre and sink into the dark at the edges, punched holes let the
                                light straight through, black ink outlines stay black
  rods                          thin dark shadows of the control sticks, sharp at the puppet, soft lower down
  lamp(cr, t)                   oil-lamp flicker and a drifting hot spot over everything
A puppet pulled away from the cloth is drawn from a blurred copy of its sprite, a little larger and paler.

Sprites are drawn once per process in "design units" (a standing figure is ~1000 units tall) at a resolution chosen
from a small ladder to suit the on-screen size, then cached with a leather texture (fibre mottling) baked in.
"""
import functools
import math
import zlib

import cairo
import numpy as np
from scipy.ndimage import gaussian_filter

from poster import FPS, H, W, back, clamp, ease

INK = (0.07, 0.04, 0.025)
# leather dyes (the light through them is multiplied by the lamp colour)
PARCH = (0.98, 0.86, 0.60)
PALE = (1.0, 0.95, 0.84)
RED = (0.93, 0.24, 0.12)
DRED = (0.66, 0.11, 0.08)
OCHRE = (0.99, 0.66, 0.16)
GOLD = (1.0, 0.82, 0.30)
GREEN = (0.36, 0.66, 0.26)
DGREEN = (0.13, 0.42, 0.22)
BLUE = (0.16, 0.42, 0.96)
SKIN = (0.99, 0.72, 0.48)
ROSE = (0.98, 0.50, 0.36)
BROWN = (0.62, 0.36, 0.16)
DARK = (0.30, 0.27, 0.32)
SAFFRON = (1.0, 0.55, 0.10)
VIOLET = (0.55, 0.30, 0.62)
LAMP_XY = (540.0, 1010.0)

# ------------------------------------------------------------------ numpy <-> cairo


def surface_from_rgba(a):
    """float RGBA (premultiplied, 0..1) -> cairo ARGB32 surface."""
    h, w = a.shape[:2]
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    buf = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())
    q = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    buf[:, :w, 0], buf[:, :w, 1], buf[:, :w, 2], buf[:, :w, 3] = q[..., 2], q[..., 1], q[..., 0], q[..., 3]
    s.mark_dirty()
    return s


def rgba_from_surface(s):
    s.flush()
    h, w = s.get_height(), s.get_width()
    b = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :w].astype(np.float32) / 255
    return np.stack([b[..., 2], b[..., 1], b[..., 0], b[..., 3]], -1)


# ------------------------------------------------------------------ the screen


def _smooth_noise(rng, shape, sigma):
    n = gaussian_filter(rng.normal(0, 1, shape).astype(np.float32), sigma)
    return n / (n.std() + 1e-6)


@functools.lru_cache(maxsize=1)
def screen_surface():
    """The backlit cloth: an oil lamp behind it at LAMP_XY (warm off-white centre, falling off to dark brown edges),
    a soft weave, two stitched panel seams, gentle creases and a few oil stains."""
    rng = np.random.default_rng(1729)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - LAMP_XY[0]) / 610.0
    dy = (yy - LAMP_XY[1]) / 1260.0
    d2 = dx * dx + dy * dy
    L = np.exp(-1.55 * d2 ** 1.15)
    hx, hy = (xx - 540) / 560.0, (yy - 440) / 420.0          # a second, smaller lamp lights the title area
    L = L + 0.30 * np.exp(-(hx * hx + hy * hy) ** 1.1) * (1 - 0.6 * L)
    L *= 1 + 0.025 * _smooth_noise(rng, (H // 8 + 1, W // 8 + 1), 9).repeat(8, 0).repeat(8, 1)[:H, :W]
    # cloth: fine fibre noise, horizontal slubs, two vertical panel seams, a few creases
    fib = _smooth_noise(rng, (H, W), 0.8) * 0.010
    slub = gaussian_filter(rng.normal(0, 1, (H, W // 16 + 1)).astype(np.float32), (0.6, 2.0)).repeat(16, 1)[:, :W]
    slub = slub / (slub.std() + 1e-6) * 0.012
    tex = 1 + fib + slub
    for sx in (178.0, 902.0):
        d = xx - sx - 6 * np.sin(yy / 260.0)
        tex *= 1 - 0.07 * np.exp(-(d / 2.2) ** 2)
        tex *= 1 + 0.03 * np.exp(-((d - 5) / 5.0) ** 2)
        st = (np.abs(d) < 2.5) & ((yy.astype(np.int32) // 9) % 2 == 0)
        tex *= np.where(st, 0.93, 1.0)
    for (x0, y0, ang, wdt, k) in ((300, 600, 1.35, 30, 0.035), (760, 1300, 1.75, 40, 0.03), (520, 300, 1.5, 24, 0.02)):
        nx, ny = math.cos(ang), math.sin(ang)
        d = (xx - x0) * ny - (yy - y0) * nx
        along = np.exp(-(((xx - x0) * nx + (yy - y0) * ny) / 700.0) ** 2)
        tex *= 1 - k * along * np.exp(-(d / wdt) ** 2) + 0.6 * k * along * np.exp(-((d - wdt) / wdt) ** 2)
    stain = np.zeros((H, W), np.float32)
    for (sx, sy, r, k) in ((130, 1650, 120, 0.10), (980, 420, 90, 0.07), (860, 1720, 70, 0.08), (90, 700, 60, 0.05)):
        stain += k * np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (r * r)) ** 1.5)
    # colour ramp: lamp light through cotton
    stops = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    cols = np.array([(0.03, 0.012, 0.006), (0.24, 0.10, 0.04), (0.62, 0.36, 0.15), (0.90, 0.68, 0.40),
                     (0.98, 0.88, 0.66), (1.0, 0.96, 0.84)])
    Lc = np.clip(L, 0, 1.05)
    img = np.stack([np.interp(Lc, stops, cols[:, c]) for c in range(3)], -1).astype(np.float32)
    img *= tex[..., None]
    img *= (1 - stain[..., None] * np.array([0.45, 0.65, 0.95], np.float32))
    a = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    return surface_from_rgba(a)


@functools.lru_cache(maxsize=4)
def grain_surface(k):
    rng = np.random.default_rng(100 + k)
    n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    n = np.kron(n, np.ones((2, 2), np.float32))
    a = np.zeros((H, W, 4), np.float32)
    lum = np.clip(n, 0, None) * 0.035
    dk = np.clip(-n, 0, None) * 0.045
    a[..., 0] = a[..., 1] = a[..., 2] = lum
    a[..., 0] += 0
    a[..., 3] = lum + dk
    return surface_from_rgba(a)


def screen(cr):
    cr.set_source_surface(screen_surface(), 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint()


def flicker(t):
    """Oil-lamp brightness wobble, -1..1-ish, a pure function of t."""
    f = int(t * FPS)
    h = (zlib.crc32(f.to_bytes(4, "little")) % 1000) / 1000.0 - 0.5
    return (0.55 * math.sin(2 * math.pi * 0.9 * t) + 0.35 * math.sin(2 * math.pi * 2.3 * t + 1.1)
            + 0.25 * math.sin(2 * math.pi * 5.3 * t + 2.0) + 0.35 * h)


@functools.lru_cache(maxsize=1)
def _hotspot():
    n = 205
    yy, xx = np.mgrid[0:2 * n, 0:2 * n].astype(np.float32)
    d = np.sqrt((xx - n) ** 2 + (yy - n) ** 2) / n
    v = np.clip(np.exp(-3.2 * d * d) - np.exp(-3.2), 0, None)
    a = np.zeros((2 * n, 2 * n, 4), np.float32)
    a[..., 0], a[..., 1], a[..., 2], a[..., 3] = v * 1.0, v * 0.74, v * 0.40, v
    return surface_from_rgba(a), n


def lamp(cr, t, strength=1.0, night=0.0, flash=0.0):
    """Lamp over the composed frame: flicker, a drifting warm hot spot, an optional night tint (moonlit scenes) and a
    flash of lamp light (joins, the roar, the split)."""
    f = flicker(t) * strength
    lx = LAMP_XY[0] + 14 * math.sin(t * 1.3) + 6 * math.sin(t * 3.1)
    ly = LAMP_XY[1] - 40 + 10 * math.sin(t * 0.9 + 1)
    hs, n = _hotspot()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(lx, ly)
    cr.scale(820 / n, 1100 / n)
    cr.set_source_surface(hs, -n, -n)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(clamp(0.10 + 0.05 * f))
    cr.restore()
    if night > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_rgba(0.40, 0.48, 0.78, night)
        cr.paint()
        cr.restore()
    dark = 0.05 + 0.035 * f
    if dark > 0:
        cr.set_source_rgba(0.02, 0.01, 0.0, clamp(dark))
        cr.paint()
    if flash > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.translate(LAMP_XY[0], LAMP_XY[1] - 200)
        cr.scale(1500 / n, 1700 / n)
        cr.set_source_surface(hs, -n, -n)
        cr.get_source().set_filter(cairo.FILTER_BILINEAR)
        cr.paint_with_alpha(clamp(flash) * 0.5)
        cr.restore()


def finish(cr, t):
    cr.set_source_surface(grain_surface(int(t * FPS) % 4), 0, 0)
    cr.paint()


# ------------------------------------------------------------------ path helpers (design units)


def spath(cr, pts, closed=True, cont=False):
    """Smooth Catmull-Rom path through pts (cont=True continues the current sub-path instead of starting one)."""
    n = len(pts)
    if closed:
        P = [pts[-1]] + list(pts) + [pts[0], pts[1]]
        rng_ = range(1, n + 1)
    else:
        P = [pts[0]] + list(pts) + [pts[-1]]
        rng_ = range(1, n)
    (cr.line_to if cont else cr.move_to)(*P[1])
    for i in rng_:
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if closed:
        cr.close_path()


def poly(cr, pts, closed=True):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    if closed:
        cr.close_path()


def ell(cr, cx, cy, rx, ry, rot=0.0):
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.scale(max(rx, 0.01), max(ry, 0.01))
    cr.new_sub_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()


def flat_pts(cr):
    """Current path flattened to a list of polylines."""
    out, cur = [], []
    for kind, pts in cr.copy_path_flat():
        if kind == cairo.PATH_MOVE_TO:
            if len(cur) > 1:
                out.append(cur)
            cur = [pts]
        elif kind == cairo.PATH_LINE_TO:
            cur.append(pts)
    if len(cur) > 1:
        out.append(cur)
    return out


def resample(pl, spacing, closed=True, start=0.5):
    pts = list(pl) + ([pl[0]] if closed else [])
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    if total < spacing:
        return []
    n = int(total / spacing)
    sp = total / n if closed else spacing
    out, d, i, acc = [], sp * start, 0, 0.0
    while d < total - (0 if closed else 1e-6) and len(out) < 5000:
        while i < len(seg) and acc + seg[i] < d:
            acc += seg[i]
            i += 1
        if i >= len(seg):
            break
        f = (d - acc) / seg[i] if seg[i] else 0
        a, b = pts[i], pts[i + 1]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, math.atan2(b[1] - a[1], b[0] - a[0])))
        d += sp
    return out


def inset(pl, d):
    """Offset a closed polyline inwards by d."""
    n = len(pl)
    if n < 3:
        return pl
    area = sum(pl[i][0] * pl[(i + 1) % n][1] - pl[(i + 1) % n][0] * pl[i][1] for i in range(n))
    sgn = 1 if area > 0 else -1
    out = []
    for i in range(n):
        a, b, c = pl[i - 1], pl[i], pl[(i + 1) % n]
        n1 = (-(b[1] - a[1]), b[0] - a[0])
        n2 = (-(c[1] - b[1]), c[0] - b[0])
        l1, l2 = math.hypot(*n1) or 1, math.hypot(*n2) or 1
        nx, ny = n1[0] / l1 + n2[0] / l2, n1[1] / l1 + n2[1] / l2
        ln = math.hypot(nx, ny) or 1
        out.append((b[0] + sgn * d * nx / ln, b[1] + sgn * d * ny / ln))
    return out


# ------------------------------------------------------------------ leather painting (inside sprite draw functions)


def leather(cr, col, lw=6.0, keep=False):
    """Fill the current path with a leather dye and ink its outline. keep=True leaves the path for perforate()."""
    pts = flat_pts(cr) if keep else None
    cr.set_source_rgb(*col)
    cr.fill_preserve()
    if lw:
        cr.set_source_rgb(*INK)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    cr.new_path()
    return pts


def punch(cr, pts, r):
    """Punch round holes (the light comes straight through)."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    for p in pts:
        cr.new_sub_path()
        cr.arc(p[0], p[1], r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def perforate(cr, polylines, d=11.0, spacing=15.0, r=3.0, closed=True):
    """A row of punched holes running just inside an outline (the classic perforated border)."""
    for pl in polylines:
        src = inset(pl, d) if (closed and d) else pl
        punch(cr, [(x, y) for x, y, _ in resample(src, spacing, closed)], r)


def holes_line(cr, pts, spacing=14.0, r=3.0, smooth=True):
    """Holes along an open line."""
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=False)
    pl = flat_pts(cr)
    cr.new_path()
    for p in pl:
        punch(cr, [(x, y) for x, y, _ in resample(p, spacing, closed=False, start=0.0)], r)


def cut(cr, fn):
    """Cut a shape out of the leather (fn draws the path)."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.new_path()
    fn()
    cr.fill()
    cr.restore()


def ink(cr, pts, w=5.0, smooth=True, closed=False, col=INK):
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=closed)
    cr.set_source_rgb(*col)
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def dots_in(cr, path_fn, spacing=22.0, r=3.4, stagger=True, bbox=(-600, -1200, 600, 600), shape="o"):
    """Punch a grid of holes (or tiny diamonds) inside a region (path_fn draws it)."""
    cr.save()
    cr.new_path()
    path_fn()
    cr.clip()
    x0, y0, x1, y1 = cr.clip_extents()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    j = 0
    y = y0 + spacing / 2
    while y < y1:
        x = x0 + spacing / 2 + (spacing / 2 if (stagger and j % 2) else 0)
        while x < x1:
            if shape == "o":
                cr.new_sub_path()
                cr.arc(x, y, r, 0, 2 * math.pi)
            else:
                poly(cr, [(x, y - r * 1.6), (x + r, y), (x, y + r * 1.6), (x - r, y)])
            x += spacing
        y += spacing * (0.87 if stagger else 1)
        j += 1
    cr.fill()
    cr.restore()


def band(cr, pts, width, col, holes=True, lw=4.0, hole_r=2.6, spacing=13.0):
    """A decorated strip (armlet, border, sash) along an open line: dyed, inked, with a row of holes."""
    cr.new_path()
    spath(cr, pts, closed=False)
    cr.set_line_cap(cairo.LINE_CAP_BUTT)
    cr.set_line_width(width + lw * 2)
    cr.set_source_rgb(*INK)
    cr.stroke_preserve()
    cr.set_line_width(width)
    cr.set_source_rgb(*col)
    cr.stroke()
    if holes:
        holes_line(cr, pts, spacing, hole_r)


def rivet(cr, x=0.0, y=0.0, r=9.0):
    """The knotted pivot of a joint: a dark knot with a light pin-hole."""
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    cr.arc(x, y, r * 0.55, 0, 2 * math.pi)
    cr.set_source_rgb(0.85, 0.62, 0.30)
    cr.fill()
    punch(cr, [(x, y)], r * 0.25)


def almond_eye(cr, x, y, L, Hh, look=1, col=PALE, pupil=True, lw=4.0):
    """A big almond eye in profile (facing +x when look=1)."""
    cr.new_path()
    cr.move_to(x - L / 2, y)
    cr.curve_to(x - L / 4, y - Hh, x + L / 4, y - Hh, x + L / 2, y + Hh * 0.1)
    cr.curve_to(x + L / 4, y + Hh * 0.8, x - L / 4, y + Hh * 0.8, x - L / 2, y)
    cr.close_path()
    leather(cr, col, lw)
    if pupil:
        cr.arc(x + look * L * 0.12, y, Hh * 0.62, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(x + look * L * 0.12 + Hh * 0.18, y - Hh * 0.22)], Hh * 0.16)
    ink(cr, [(x - L / 2 - 4, y - Hh * 0.2), (x - L / 2 - 14, y - Hh * 0.6)], 3.5)


# ------------------------------------------------------------------ sprite registry

_DEFS = {}
RES = (0.3, 0.5, 0.75, 1.0, 1.4)


def part(name, bbox, seed=None, tex=1.0):
    """Register a sprite: fn(cr) draws it in design units with the pivot at (0, 0); bbox = (x0, y0, x1, y1)."""
    def deco(fn):
        _DEFS[name] = (fn, bbox, seed if seed is not None else zlib.crc32(name.encode()) % 100000, tex)
        return fn
    return deco


def register(name, bbox, fn, tex=1.0):
    _DEFS[name] = (fn, bbox, zlib.crc32(name.encode()) % 100000, tex)


TEX_N = 1600


@functools.lru_cache(maxsize=1)
def _big_tex():
    rng = np.random.default_rng(77)
    N = TEX_N
    n = (0.055 * _smooth_noise(rng, (N, N), 7.0) + 0.035 * _smooth_noise(rng, (N, N), 1.6)
         + 0.04 * _smooth_noise(rng, (N // 4, N // 4), 6.0).repeat(4, 0).repeat(4, 1))
    streak = gaussian_filter(rng.normal(0, 1, (N, N)).astype(np.float32), (9.0, 1.2))
    n += 0.03 * streak / (streak.std() + 1e-6)
    return (1 + n).astype(np.float32)


def _leather_tex(h, w, seed):
    big = _big_tex()
    r = (np.arange(h) + seed * 211) % TEX_N
    c = (np.arange(w) + seed * 97) % TEX_N
    return big[np.ix_(r, c)]


@functools.lru_cache(maxsize=None)
def sprite(name, res, blur=0):
    """(surface, x0, y0) for a part at `res` px per design unit; blur = sigma in sprite pixels (0 = pressed flat)."""
    fn, (x0, y0, x1, y1), seed, tex = _DEFS[name]
    pad = 6 + int(3.2 * blur)
    if blur:
        base, _, _ = sprite(name, res, 0)
        a = rgba_from_surface(base)
        p0 = 6
        big = np.zeros((a.shape[0] - 2 * p0 + 2 * pad, a.shape[1] - 2 * p0 + 2 * pad, 4), np.float32)
        big[pad - p0:pad - p0 + a.shape[0], pad - p0:pad - p0 + a.shape[1]] = a
        big = gaussian_filter(big, (blur, blur, 0))
        return surface_from_rgba(big), x0 - pad / res, y0 - pad / res
    w = int(math.ceil((x1 - x0) * res)) + 2 * pad
    h = int(math.ceil((y1 - y0) * res)) + 2 * pad
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cr = cairo.Context(s)
    cr.translate(pad, pad)
    cr.scale(res, res)
    cr.translate(-x0, -y0)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    fn(cr)
    if tex:
        a = rgba_from_surface(s)
        f = _leather_tex(h, w, seed % 7)
        edge = np.clip((1 - gaussian_filter(a[..., 3], 2.5 * res + 0.8)) * 2.4, 0, 1)
        f = f * (1 - 0.30 * edge)
        a[..., :3] = np.minimum(a[..., :3] * (1 + (f[..., None] - 1) * tex), a[..., 3:4])
        s = surface_from_rgba(a)
    return s, x0 - pad / res, y0 - pad / res


def _pick_res(scale):
    for r in RES:
        if r >= scale * 0.92:
            return r
    return RES[-1]


BLUR_LEVELS = (0.0, 1.5, 3.0, 5.0, 8.0, 12.0, 17.0, 23.0)


def paint_part(cr, name, alpha=1.0, blur=0.0, op=cairo.OPERATOR_MULTIPLY):
    """Paint a registered sprite at the current transform (design units). blur = screen pixels of defocus (a puppet
    pulled away from the cloth): drawn from a cached blurred copy made at a lower resolution."""
    if alpha <= 0.003:
        return
    m = cr.get_matrix()
    scale = math.sqrt(abs(m.xx * m.yy - m.xy * m.yx))
    b = min(BLUR_LEVELS, key=lambda v: abs(v - blur)) if blur > 0.7 else 0.0
    res = _pick_res(scale / (1 + b / 4.0))
    sig = round(b * res / max(scale, 1e-3) * 2) / 2 if b else 0
    surf, ox, oy = sprite(name, res, sig)
    cr.save()
    cr.set_operator(op)
    cr.translate(ox, oy)
    cr.scale(1 / res, 1 / res)
    cr.set_source_surface(surf, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.rectangle(0, 0, surf.get_width(), surf.get_height())
    cr.clip()
    cr.paint_with_alpha(alpha)
    cr.restore()


def prop(cr, name, x, y, s=1.0, rot=0.0, alpha=1.0, blur=0.0, flip=False):
    """A single-piece leather prop with its pivot at (x, y)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(-s if flip else s, s)
    paint_part(cr, name, alpha, blur)
    cr.restore()


# ------------------------------------------------------------------ jointed puppets


class Rig:
    """parts: [(name, parent, anchor_xy_in_parent, rest_angle)], listed back to front. The root has parent None.
    Each part's own drawing has its pivot at (0, 0). points: named attachment points {name: (part, (x, y))}."""

    def __init__(self, parts, points=None, rods=()):
        self.parts = parts
        self.points = points or {}
        self.rods = rods          # [(point name, bottom dx, bottom spread)]


def rig_mats(cr, rig, angles, scales=None):
    base = cr.get_matrix()
    spec = {name: (parent, anchor, rest) for name, parent, anchor, rest in rig.parts}
    mats = {}

    def get(name):
        if name in mats:
            return mats[name]
        parent, anchor, rest = spec[name]
        m = base if parent is None else get(parent)
        cr.set_matrix(m)
        if parent is not None:
            cr.translate(*anchor)
        cr.rotate(rest + angles.get(name, 0.0))
        if scales and name in scales:
            cr.scale(max(1e-3, scales[name]), max(1e-3, scales[name]))
        mats[name] = cr.get_matrix()
        return mats[name]
    for name in spec:
        get(name)
    cr.set_matrix(base)
    return mats


def point_of(cr, mats, rig, pname):
    pn, (px, py) = rig.points[pname]
    cr.save()
    cr.set_matrix(mats[pn])
    x, y = cr.user_to_device(px, py)
    cr.restore()
    return x, y


def puppet(cr, rig, x, y, s=1.0, rot=0.0, flip=False, angles=None, alpha=1.0, blur=0.0, hide=(), swap=None,
           rods=True, rod_alpha=1.0, extra=None, only=None, scales=None):
    """Draw a jointed puppet with its root pivot at (x, y). angles: {part: radians}; swap: {part: other sprite};
    blur: screen px of defocus (pulled away from the cloth). Returns {point name: device xy}."""
    angles = angles or {}
    swap = swap or {}
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(-s if flip else s, s)
    mats = rig_mats(cr, rig, angles, scales)
    for name, parent, anchor, rest in rig.parts:
        if name in hide or (only is not None and name not in only):
            continue
        cr.set_matrix(mats[name])
        far = 1.2 if ("_armB" in name or "_legB" in name) else 0.0
        paint_part(cr, swap.get(name, name), alpha, blur + far)
        if extra and name in extra:
            extra[name](cr)
    pts = {k: point_of(cr, mats, rig, k) for k in rig.points}
    cr.restore()
    if rods and rig.rods:
        for pname, dx, lean in rig.rods:
            if pname in pts and rig.points[pname][0] not in hide:
                px, py = pts[pname]
                rod(cr, px, py, px + (dx * s * (-1 if flip else 1)), H + 60, alpha=rod_alpha * alpha, blur=blur)
    return pts


def rod(cr, x0, y0, x1, y1, alpha=1.0, blur=0.0, w=3.2):
    """The shadow of a control stick: crisp where it touches the puppet, softer and wider further down."""
    if alpha <= 0.01:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1:
        return
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    for k, (wm, am) in enumerate(((4.0, 0.06), (2.2, 0.14), (1.0, 0.55))):
        w0, w1 = (w + blur * 0.6) * wm * 0.5, (w * 2.2 + blur) * wm * 0.5
        g = cairo.LinearGradient(x0, y0, x1, y1)
        g.add_color_stop_rgba(0, 0.05, 0.025, 0.01, alpha * am * (0.55 if blur > 3 else 1.0))
        g.add_color_stop_rgba(1, 0.05, 0.025, 0.01, alpha * am * 0.45)
        cr.set_source(g)
        poly(cr, [(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1),
                  (x0 - nx * w0, y0 - ny * w0)])
        cr.fill()


def split_draw(cr, draw_fn, offA, offB, root_xy, root_rot=0.0, root_s=1.0, flip=False, seam_x=0.0, zig=12.0):
    """Draw a figure twice, clipped either side of a zig-zag seam (root-local x = seam_x), each half moved rigidly by
    its own (dx, dy, drot about the root): the figure coming apart in two halves, or (run backwards) joining.
    draw_fn(cr) draws the whole figure in scene coordinates."""
    for side, (dx, dy, dr) in ((-1, offA), (1, offB)):
        cr.save()
        cr.translate(dx, dy)
        cr.translate(*root_xy)
        cr.rotate(dr)
        cr.translate(-root_xy[0], -root_xy[1])
        m = cr.get_matrix()
        cr.translate(*root_xy)
        cr.rotate(root_rot)
        cr.scale(-root_s if flip else root_s, root_s)
        sx = seam_x
        pts = [(sx + (zig if i % 2 else -zig) * 0.5, -1500 + i * 30) for i in range(0, 91)]
        far = sx + side * 3000
        cr.new_path()
        cr.move_to(far, -1500)
        for p in pts:
            cr.line_to(*p)
        cr.line_to(far, pts[-1][1])
        cr.close_path()
        cr.set_matrix(m)
        cr.clip()
        draw_fn(cr)
        cr.restore()


# ------------------------------------------------------------------ motion


def keyed(t, keys, dur=0.28, overshoot=1.6):
    """Rod-puppet keyframes: [(time, value), ...]; each move is quick with a small overshoot, then holds still.
    Values may be numbers or tuples."""
    if t <= keys[0][0]:
        return keys[0][1]
    v = keys[0][1]
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        if t < tb:
            return va
        p = (t - tb) / dur
        if p >= 1:
            v = vb
            continue
        q = back(clamp(p), overshoot)
        if isinstance(va, tuple):
            return tuple(a + (b - a) * q for a, b in zip(va, vb))
        return va + (vb - va) * q
    return v


def dangle(t, hits, amp=0.25, freq=1.7, decay=2.6):
    """Damped swing of a loose limb after each hit time (the arm swings about its pivot and settles)."""
    s = 0.0
    for th, a in hits:
        dt = t - th
        if dt > 0:
            s += a * amp * math.exp(-decay * dt) * math.sin(2 * math.pi * freq * dt)
    return s


def sway(t, amp=0.02, freq=0.6, ph=0.0):
    return amp * math.sin(2 * math.pi * freq * t + ph) + amp * 0.4 * math.sin(2 * math.pi * freq * 2.3 * t + ph * 1.7)


def hop_walk(t, t0, t1, x0, x1, step=0.42):
    """A rod puppet walking: x advances in jerky steps, the body bobs and rocks with each step.
    Returns (x, bob_y, rock, leg_phase)."""
    if t <= t0:
        return x0, 0.0, 0.0, 0.0
    if t >= t1:
        return x1, 0.0, 0.0, 0.0
    n = max(1, round((t1 - t0) / step))
    st = (t1 - t0) / n
    k = int((t - t0) / st)
    f = (t - t0 - k * st) / st
    e = ease(f / 0.7)
    x = x0 + (x1 - x0) * (k + e) / n
    bob = -abs(math.sin(math.pi * f)) * 16
    rock = 0.05 * math.sin(math.pi * f) * (1 if k % 2 else -1)
    return x, bob, rock, (1 if k % 2 else -1) * math.sin(math.pi * f)


def depth(t, t_in, dur=0.45, t_out=None, out_dur=0.35, far=22.0):
    """Blur/scale/alpha of a puppet brought from away (blurred, big, pale) onto the cloth, and taken away again.
    Returns (blur px, scale factor, alpha)."""
    p = ease((t - t_in) / dur) if dur > 0 else float(t >= t_in)
    if t_out is not None and t > t_out:
        p = min(p, 1 - ease((t - t_out) / out_dur))
    d = 1 - p
    return far * d, 1 + 0.22 * d, clamp(0.25 + 0.75 * p * 1.3) * clamp(p * 4)
