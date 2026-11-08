"""A reusable 2D vector rig for code-drawn talking cartoon characters (pycairo), Nov 2026.

Everything is a pure function of t, so frames can be drawn in any order in worker processes.

  geometry     centripetal Catmull-Rom paths (no overshoot, optional sharp corners), tapered ink strokes, capsules
  Head25D      a 2.5D head: front-view points get a depth from a head-shaped surface and are turned (yaw) and nodded
               (pitch) in 3D before projecting, so features slide across the face and the far side squashes
  ink()        a layered "ink group": the silhouette outline is stroked under the fills (heavier on the shadow side),
               each part gets cel shading (shadow and highlight rims plus painted shapes), and occlusion lines are drawn
               only where a part overlaps the parts behind it; joint masks hide the seams at elbows, knuckles, wrists
  hand_parts   a small 3D hand (palm slab + capsule fingers + thumb) posed by joint angles and projected, so curls,
               twists and spreads interpolate smoothly between gestures
  Voice        lip-sync from wav files: loudness envelope + spectral cues -> visemes (rest, slight, aa, ee, oo, ss)
               held >= 2 frames -> smoothed mouth parameters; phrases (gesture changes) and stressed peaks
  Blinks/Gaze  random natural blinks (some doubles) and small eye darts from a seeded schedule
  Track        pose interpolation with a springy ease (slight overshoot) and per-parameter delays (follow-through)
"""
import contextlib
import math
import random
import struct
import zlib

import cairo
import numpy as np

INK = (0.065, 0.055, 0.12)
TAU = 2 * math.pi


# ------------------------------------------------------------------ small maths

def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c1, c2, k):
    return tuple(a + (b - a) * k for a, b in zip(c1, c2))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def smoother(x):
    x = clamp(x)
    return x * x * x * (x * (6 * x - 15) + 10)


def spring(x, zeta=0.74, omega=4.8):
    """Step response of a slightly under-damped spring: starts with zero speed, reaches the target near x=1 with a
    ~2-3% overshoot, settles by x~2. Used as the ease between poses (dur = time to arrive)."""
    if x <= 0:
        return 0.0
    if x >= 3:
        return 1.0
    r = math.sqrt(1 - zeta * zeta)
    wd = omega * r
    return 1 - math.exp(-zeta * omega * x) * (math.cos(wd * x) + zeta / r * math.sin(wd * x))


def bump(t, t0, dur):
    """0 -> 1 -> 0 over [t0, t0+dur] (sin^2 window)."""
    u = (t - t0) / dur
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def pulse(t, t0, rise=0.08, fall=0.35):
    """Rises smoothly to 1 at t0 (starting `rise` earlier) and decays exponentially after."""
    d = t - t0
    if d < -rise:
        return 0.0
    if d < 0:
        return smooth((d + rise) / rise)
    return math.exp(-d / fall)


def _hash(i, seed):
    return zlib.crc32(struct.pack("<qi", i, seed)) / 4294967295.0 * 2 - 1


def noise(t, seed=0, freq=1.0):
    """Smooth 1-D value noise in [-1, 1]."""
    x = t * freq
    i = math.floor(x)
    f = x - i
    u = f * f * (3 - 2 * f)
    return lerp(_hash(i, seed), _hash(i + 1, seed), u)


def fbm(t, seed=0, freq=1.0):
    return 0.64 * noise(t, seed, freq) + 0.36 * noise(t + 7.3, seed + 101, freq * 2.17)


def rgb(cr, c, a=1.0):
    if a >= 1.0:
        cr.set_source_rgb(c[0], c[1], c[2])
    else:
        cr.set_source_rgba(c[0], c[1], c[2], a)


# ------------------------------------------------------------------ geometry

def _corner(p):
    return len(p) > 2 and bool(p[2])


def _cr_ctrl(p0, p1, p2, p3, alpha=0.5):
    """Bezier control points of the centripetal Catmull-Rom segment p1->p2 (no cusps, no overshoot loops)."""
    d1 = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) ** alpha
    d2 = math.hypot(p2[0] - p1[0], p2[1] - p1[1]) ** alpha
    d3 = math.hypot(p3[0] - p2[0], p3[1] - p2[1]) ** alpha
    if d2 < 1e-9:
        return (p1[0], p1[1]), (p2[0], p2[1])
    if d1 < 1e-9:
        d1 = d2
    if d3 < 1e-9:
        d3 = d2
    a = 2 * d1 * d1 + 3 * d1 * d2 + d2 * d2
    n = 3 * d1 * (d1 + d2)
    b = 2 * d3 * d3 + 3 * d3 * d2 + d2 * d2
    m = 3 * d3 * (d3 + d2)
    c1 = ((d1 * d1 * p2[0] - d2 * d2 * p0[0] + a * p1[0]) / n, (d1 * d1 * p2[1] - d2 * d2 * p0[1] + a * p1[1]) / n)
    c2 = ((d3 * d3 * p1[0] - d2 * d2 * p3[0] + b * p2[0]) / m, (d3 * d3 * p1[1] - d2 * d2 * p3[1] + b * p2[1]) / m)
    return c1, c2


def segments(pts, closed=True):
    """Cubic segments (p1, c1, c2, p2) through pts. A point (x, y, 1) is a sharp corner."""
    n = len(pts)
    out = []
    if n < 2:
        return out
    for i in range(n if closed else n - 1):
        p1, p2 = pts[i], pts[(i + 1) % n]
        p0 = pts[(i - 1) % n] if (closed or i > 0) else None
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else None
        if p0 is None or _corner(p1):
            p0 = (2 * p1[0] - p2[0], 2 * p1[1] - p2[1])
        if p3 is None or _corner(p2):
            p3 = (2 * p2[0] - p1[0], 2 * p2[1] - p1[1])
        c1, c2 = _cr_ctrl(p0, p1, p2, p3)
        out.append(((p1[0], p1[1]), c1, c2, (p2[0], p2[1])))
    return out


def spath(cr, pts, closed=True, cont=False):
    """Add a smooth path through pts to cr (cont=True continues the current sub-path)."""
    segs = segments(pts, closed)
    if not segs:
        return
    if cont:
        cr.line_to(*segs[0][0])
    else:
        cr.move_to(*segs[0][0])
    for _, c1, c2, p2 in segs:
        cr.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        cr.close_path()


def poly(cr, pts, closed=True):
    cr.move_to(*pts[0][:2])
    for p in pts[1:]:
        cr.line_to(*p[:2])
    if closed:
        cr.close_path()


def _bez(p0, c1, c2, p3, u):
    v = 1 - u
    a, b, c, d = v * v * v, 3 * v * v * u, 3 * v * u * u, u * u * u
    return (a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1])


def sample(pts, closed=False, step=3.0):
    """Dense polyline along the spline through pts."""
    out = []
    segs = segments(pts, closed)
    for p0, c1, c2, p3 in segs:
        ln = math.dist(p0, c1) + math.dist(c1, c2) + math.dist(c2, p3)
        k = max(2, int(ln / step))
        out.extend(_bez(p0, c1, c2, p3, j / k) for j in range(k))
    if segs and not closed:
        out.append(segs[-1][3])
    return out


def ellipse(cr, cx, cy, rx, ry, rot=0.0):
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.scale(max(rx, 0.01), max(ry, 0.01))
    cr.new_sub_path()
    cr.arc(0, 0, 1, 0, TAU)
    cr.restore()


def _prof(prof, u):
    if callable(prof):
        return prof(u)
    if prof == "both":
        return math.sin(math.pi * clamp(u)) ** 0.65
    if prof == "start":     # heavy at the start, thin at the end
        return (1 - u) ** 0.85 * min(1.0, 0.45 + u / 0.08)
    if prof == "end":
        return u ** 0.85 * min(1.0, 0.45 + (1 - u) / 0.08)
    if prof == "flat":
        return min(1.0, 0.3 + u / 0.12, 0.3 + (1 - u) / 0.12)
    vals = prof                 # tuple of factors at evenly spaced u
    x = clamp(u) * (len(vals) - 1)
    i = min(int(x), len(vals) - 2)
    return lerp(vals[i], vals[i + 1], x - i)


def taper(cr, pts, w, prof="both", closed=False, wmin=0.0, step=2.5, caps=True):
    """Add a filled, variable-width ink stroke along the spline through pts (call cr.fill() after)."""
    P = sample(pts, closed, step)
    n = len(P)
    if n < 2:
        return
    s = [0.0]
    for i in range(1, n):
        s.append(s[-1] + math.dist(P[i - 1], P[i]))
    L = s[-1] or 1.0
    left, right, hw = [], [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        h = max(wmin, w * _prof(prof, s[i] / L)) / 2
        hw.append(h)
        left.append((P[i][0] + nx * h, P[i][1] + ny * h))
        right.append((P[i][0] - nx * h, P[i][1] - ny * h))
    cr.move_to(*left[0])
    for p in left[1:]:
        cr.line_to(*p)
    for p in reversed(right):
        cr.line_to(*p)
    cr.close_path()
    if caps:
        for i in (0, n - 1):
            if hw[i] > 0.9:
                cr.new_sub_path()
                cr.arc(P[i][0], P[i][1], hw[i], 0, TAU)


def stroke_taper(cr, pts, w, color=INK, alpha=1.0, **kw):
    cr.new_path()
    taper(cr, pts, w, **kw)
    rgb(cr, color, alpha)
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.fill()


def capsule(cr, a, ra, b, rb):
    """Convex hull of two circles (a finger bone) as a closed sub-path."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy)
    if d < 1e-6 or d + min(ra, rb) <= max(ra, rb):
        c, r = (a, ra) if ra >= rb else (b, rb)
        cr.new_sub_path()
        cr.arc(c[0], c[1], r, 0, TAU)
        return
    ang = math.atan2(dy, dx)
    phi = math.acos(clamp((ra - rb) / d, -1, 1))
    cr.new_sub_path()
    cr.arc(a[0], a[1], ra, ang + phi, ang - phi + TAU)
    cr.arc(b[0], b[1], rb, ang - phi, ang + phi)
    cr.close_path()


def offset_band(center, widths, step=3.0):
    """Closed outline of a band of varying width around a centre line (list of points, list of widths)."""
    P = sample(center, False, step)
    n = len(P)
    s = [0.0]
    for i in range(1, n):
        s.append(s[-1] + math.dist(P[i - 1], P[i]))
    L = s[-1] or 1.0
    left, right = [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        h = _prof(tuple(widths), s[i] / L) / 2
        left.append((P[i][0] + nx * h, P[i][1] + ny * h))
        right.append((P[i][0] - nx * h, P[i][1] - ny * h))
    return left, right


def lock_edge(span, n, amp, lean=0.6, side=1, seed=0, step=3.0, var=0.3, sharp=True):
    """Stylised hair-lock silhouette along an open span: n locks bulging to `side` (+1 = left of the walking
    direction in y-down coordinates), each ending in a sharp tip pushed along the span by `lean` (tips point
    with the flow). Returns (points with corner flags, strand lines inside each lock)."""
    P = sample(span, False, step)
    s = [0.0]
    for i in range(1, len(P)):
        s.append(s[-1] + math.dist(P[i - 1], P[i]))
    L = s[-1] or 1.0

    def at(u):
        d = clamp(u, 0, 1) * L
        j = 1
        while j < len(s) - 1 and s[j] < d:
            j += 1
        a, b = P[j - 1], P[j]
        f = (d - s[j - 1]) / ((s[j] - s[j - 1]) or 1)
        x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        tx, ty = b[0] - a[0], b[1] - a[1]
        tl = math.hypot(tx, ty) or 1
        tx, ty = tx / tl, ty / tl
        return x, y, tx, ty, ty * side, -tx * side      # point, tangent, outward normal

    rng = random.Random(seed)
    pts, strands = [], []
    for k in range(n):
        a = amp * rng.uniform(1 - var, 1 + var)
        lk = lean * rng.uniform(0.7, 1.3)
        u0, du = k / n, 1.0 / n
        x, y, tx, ty, nx, ny = at(u0)
        if k == 0:
            pts.append((x, y))
        else:
            pts.append((x - nx * a * 0.12, y - ny * a * 0.12))
        x, y, tx, ty, nx, ny = at(u0 + du * 0.38)
        m1 = (x + nx * a * 0.62, y + ny * a * 0.62)
        x, y, tx, ty, nx, ny = at(u0 + du * 0.8)
        tip = (x + nx * a + tx * lk * a, y + ny * a + ty * lk * a)
        x, y, tx, ty, nx, ny = at(u0 + du * 0.9)
        m2 = (x + nx * a * 0.3, y + ny * a * 0.3)
        pts += [m1, tip + (1,) if sharp else tip, m2]
        x, y, tx, ty, nx, ny = at(u0 + du * 0.3)
        root = (x - nx * a * 0.9, y - ny * a * 0.9)
        x, y, tx, ty, nx, ny = at(u0 + du * 0.62)
        strands.append([root, (x + nx * a * 0.25, y + ny * a * 0.25), (tip[0] - tx * a * 0.25 - nx * a * 0.12,
                                                                      tip[1] - ty * a * 0.25 - ny * a * 0.12)])
    x, y, *_ = at(1.0)
    pts.append((x, y))
    return pts, strands


@contextlib.contextmanager
def clip(cr, pathfn, rule=cairo.FILL_RULE_WINDING):
    cr.save()
    cr.new_path()
    pathfn(cr)
    cr.set_fill_rule(rule)
    cr.clip()
    cr.new_path()
    try:
        yield
    finally:
        cr.restore()


def shifted(cr, pathfn, dx, dy):
    cr.save()
    cr.translate(dx, dy)
    pathfn(cr)
    cr.restore()


def multiply(cr, pathfn, color, alpha=1.0):
    """Fill pathfn with a multiply-blended tint (a shadow layer that darkens whatever is underneath)."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.new_path()
    pathfn(cr)
    rgb(cr, color, alpha)
    cr.fill()
    cr.restore()


def screen(cr, pathfn, color, alpha=1.0):
    cr.save()
    cr.set_operator(cairo.OPERATOR_SCREEN)
    cr.new_path()
    pathfn(cr)
    rgb(cr, color, alpha)
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ raster helpers (soft backgrounds)

def blur_surface(s, sigma):
    """Gaussian-blurred copy of an ARGB32 surface (premultiplied channels blurred together)."""
    from scipy.ndimage import gaussian_filter
    s.flush()
    h, w = s.get_height(), s.get_width()
    a = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :w].astype(np.float32)
    a = gaussian_filter(a, (sigma, sigma, 0), mode="nearest")
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    b = np.ndarray((h, out.get_stride() // 4, 4), np.uint8, out.get_data())
    b[:, :w] = np.clip(a + 0.5, 0, 255).astype(np.uint8)
    out.mark_dirty()
    return out


# ------------------------------------------------------------------ ink groups (layered parts)

class Part:
    """One flat-filled shape in an ink group.

    path(cr)  adds the outline (several sub-paths are unioned)
    fill      base colour (None: outline only)
    tones     (shadow, highlight) colours; form = (sx, sy, hx, hy): the shadow rim is the part minus itself moved by
              (-sx, -sy), the highlight rim the lit part minus itself moved by (hx, hy) (light from the upper left)
    shade(cr) painted shapes, clipped to the part;  post(cr) drawn after, unclipped (jewellery)
    occ       draw an occlusion line where it overlaps earlier parts of the group; masks = [(x, y, r)] hide it
    cast      (dx, dy, colour, alpha): a cast shadow onto the earlier parts
    """
    __slots__ = ("path", "fill", "tones", "form", "shade", "post", "occ", "masks", "cast", "lw", "occ_w", "depth")

    def __init__(self, path, fill, tones=None, form=None, shade=None, post=None, occ=True, masks=(), cast=None,
                 lw=None, occ_w=None, depth=0.0):
        self.path, self.fill, self.tones, self.form = path, fill, tones, form
        self.shade, self.post, self.occ, self.masks, self.cast = shade, post, occ, masks, cast
        self.lw, self.occ_w, self.depth = lw, occ_w, depth


def _union(parts):
    def f(cr):
        for q in parts:
            q.path(cr)
    return f


def _fill_part(cr, p):
    if p.fill is None:
        return
    cr.new_path()
    if p.form and p.tones:
        sx, sy, hx, hy = p.form
        shadow, hl = p.tones
        p.path(cr)
        rgb(cr, shadow if shadow else p.fill)
        cr.fill()
        cr.save()
        p.path(cr)
        cr.clip()
        shifted(cr, p.path, -sx, -sy)
        if hl:
            rgb(cr, hl)
            cr.fill_preserve()
            cr.clip()
            shifted(cr, p.path, hx, hy)
        rgb(cr, p.fill)
        cr.fill()
        cr.restore()
    else:
        p.path(cr)
        rgb(cr, p.fill)
        cr.fill()


def ink(cr, parts, lw=4.6, drop=(1.5, 2.3), occ_w=2.8, color=INK):
    """Draw parts back to front as one inked group (see Part)."""
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    rgb(cr, color)
    for dx, dy in ((0.0, 0.0), drop):          # silhouette: the fills cover the inner half; the dropped copy makes
        for p in parts:                         # the lower-right (shadow-side) edges heavier, like a brush line
            w = p.lw if p.lw is not None else lw
            if w <= 0:
                continue
            cr.new_path()
            shifted(cr, p.path, dx, dy)
            cr.set_line_width(2 * w)
            cr.stroke()
    for i, p in enumerate(parts):
        if i and p.cast:
            dx, dy, col, a = p.cast
            with clip(cr, _union(parts[:i])):
                cr.save()
                cr.set_operator(cairo.OPERATOR_MULTIPLY)
                cr.new_path()
                shifted(cr, p.path, dx, dy)
                rgb(cr, col, a)
                cr.fill()
                cr.restore()
        ow = p.occ_w if p.occ_w is not None else occ_w
        if i and p.occ and ow > 0:
            cr.save()
            for (mx, my, mr) in p.masks:
                cr.new_path()
                cr.rectangle(-1e5, -1e5, 2e5, 2e5)
                cr.new_sub_path()
                cr.arc(mx, my, mr, 0, TAU)
                cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
                cr.clip()
            cr.set_fill_rule(cairo.FILL_RULE_WINDING)
            cr.new_path()
            _union(parts[:i])(cr)
            cr.clip()
            cr.new_path()
            p.path(cr)
            rgb(cr, color)
            cr.set_line_width(2 * ow)
            cr.stroke()
            cr.restore()
        _fill_part(cr, p)
        if p.shade:
            with clip(cr, p.path):
                p.shade(cr)
        if p.post:
            p.post(cr)
    cr.restore()


# ------------------------------------------------------------------ 2.5D head

class Head25D:
    """Front-view head points (x right, y down, origin between the eyes) get a depth z from a head-shaped surface
    (a vertical cylinder over the face that rounds off over the skull), are turned by yaw about the vertical axis and
    nodded by pitch, then projected straight on. Features (high z) slide further than the cheeks, the far side
    squashes, the chin follows the nose. dz adds a feature's own depth; surf=False uses dz alone (hair behind)."""

    def __init__(self, yaw=0.0, pitch=0.0, rx=168.0, rz=150.0, top=-70.0, ry_top=175.0, pivot_y=40.0):
        self.cy, self.sy = math.cos(yaw), math.sin(yaw)
        self.cp, self.sp = math.cos(pitch), math.sin(pitch)
        self.rx, self.rz, self.top, self.ry_top, self.py = rx, rz, top, ry_top, pivot_y

    def depth(self, x, y):
        f = 1 - (x / self.rx) ** 2
        if y < self.top:
            f -= ((self.top - y) / self.ry_top) ** 2
        return self.rz * math.sqrt(f) if f > 0 else 0.0

    def p(self, x, y, dz=0.0, surf=True):
        z = (self.depth(x, y) if surf else 0.0) + dz
        x1 = x * self.cy + z * self.sy
        z1 = -x * self.sy + z * self.cy
        y1 = self.py + (y - self.py) * self.cp + z1 * self.sp
        return x1, y1

    def pts(self, pts, dz=0.0, surf=True):
        out = []
        for q in pts:
            x, y = self.p(q[0], q[1], dz, surf)
            out.append((x, y, 1) if _corner(q) else (x, y))
        return out

    def sx(self, x, y, dz=0.0):
        """Local horizontal squash at (x, y): how much a small width there is scaled on screen."""
        a = self.p(x - 1, y, dz)
        b = self.p(x + 1, y, dz)
        return max(0.25, (b[0] - a[0]) / 2)


# ------------------------------------------------------------------ 3D hand

# hand-local: X from the wrist to the knuckles, Y across the palm (thumb side negative), Z out of the palm
PALM = [(-4, -23), (10, -34), (38, -39), (68, -35), (80, -20), (83, 2), (78, 23), (52, 33), (20, 32), (-4, 23)]
FINGERS = (  # root (x, y), bone lengths, radii (root .. tip), spread weight
    ((72, -24), (35, 22, 18), (11.2, 10.2, 9.4, 8.6), -1.0),
    ((76, -8), (39, 24, 19), (11.6, 10.6, 9.7, 8.8), -0.3),
    ((74, 8), (36, 22, 18), (11.0, 10.0, 9.2, 8.4), 0.4),
    ((67, 23), (28, 18, 15), (9.8, 9.0, 8.3, 7.6), 1.1),
)
THUMB = ((14, -16, 5.0), (26, 22, 19), (18.0, 13.0, 11.8, 10.6))


def _v_add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def _v_norm(a):
    n = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]) or 1.0
    return (a[0] / n, a[1] / n, a[2] / n)


def hand_parts(x, y, ang, side, pose, scale, fill, tones=None, form=None, post=None):
    """Parts (for ink()) of a hand whose wrist is at (x, y), pointing along screen angle ang (radians).

    side      +1 / -1 mirrors the hand (left / right)
    pose      tw (twist about the hand axis, deg; 0 = palm to the viewer), tip (deg, fingers tipped toward the
              viewer), ci cm cr cp (finger curls 0..1), sp (spread 0..1), to (thumb out, deg), tf (thumb fold
              toward the palm, deg), tc (thumb curl 0..1)
    """
    tw, tip = math.radians(pose["tw"]), math.radians(pose["tip"])
    ca, sa = math.cos(ang), math.sin(ang)
    cw, sw = math.cos(tw), math.sin(tw)
    ct, st = math.cos(tip), math.sin(tip)

    def P(v):
        hx, hy, hz = v
        hx, hz = hx * ct + hz * st, -hx * st + hz * ct
        hy, hz = hy * cw - hz * sw, hy * sw + hz * cw
        hy *= side
        return (x + scale * (hx * ca - hy * sa), y + scale * (hx * sa + hy * ca), hz * scale)

    parts = []
    # palm: two faces of a slab, unioned (edge-on it reads as a thick hand, flat-on as a palm)
    front = [P((px, py, 9.0)) for px, py in PALM]
    back = [P((px, py, -11.0)) for px, py in PALM]

    def palm_path(cr, a=front, b=back):
        spath(cr, [(q[0], q[1]) for q in a])
        spath(cr, [(q[0], q[1]) for q in b])
    pz = 0.0
    parts.append((pz, Part(palm_path, fill, tones, form, occ=True)))

    curls = (pose["ci"], pose["cm"], pose["cr"], pose["cp"])
    for k, ((bx, by), bones, radii, sw_) in enumerate(FINGERS):
        c = curls[k]
        sig = math.radians(9.0) * pose["sp"] * sw_ + math.radians(2.0) * sw_
        d0 = (math.cos(sig), math.sin(sig))
        bends = (c * 78.0, c * 98.0, c * 62.0)
        p = (bx, by, 0.0)
        joints = [p]
        th = 0.0
        for L, b in zip(bones, bends):
            th += math.radians(b)
            p = _v_add(p, (math.cos(th) * d0[0], math.cos(th) * d0[1], math.sin(th)), L)
            joints.append(p)
        J = [P(q) for q in joints]
        R = [r * scale for r in radii]

        def fpath(cr, J=J, R=R):
            for i in range(3):
                capsule(cr, J[i], R[i], J[i + 1], R[i + 1])
        z = sum(q[2] for q in J[1:]) / 3 + 0.5 * scale
        parts.append((z, Part(fpath, fill, tones, form, masks=[(J[0][0], J[0][1], R[0] * 1.35)])))

    # thumb
    (tx, ty, tz), bones, radii = THUMB
    a = math.radians(pose["to"])
    u0 = (math.cos(a), -math.sin(a), 0.0)
    f = math.radians(pose["tf"])
    u = _v_norm((u0[0] * math.cos(f), u0[1] * math.cos(f), math.sin(f)))
    zc = (0.0, 0.35, 1.0)
    dotp = zc[0] * u[0] + zc[1] * u[1] + zc[2] * u[2]
    w = _v_norm((zc[0] - dotp * u[0], zc[1] - dotp * u[1], zc[2] - dotp * u[2]))
    p = (tx, ty, tz)
    joints = [p]
    th = 0.0
    for L, b in zip(bones, (0.0, pose["tc"] * 40.0, pose["tc"] * 70.0)):
        th += math.radians(b)
        d = _v_norm(_v_add((u[0] * math.cos(th), u[1] * math.cos(th), u[2] * math.cos(th)), w, math.sin(th)))
        p = _v_add(p, d, L)
        joints.append(p)
    J = [P(q) for q in joints]
    R = [r * scale for r in radii]

    def tpath(cr, J=J, R=R):
        for i in range(3):
            capsule(cr, J[i], R[i], J[i + 1], R[i + 1])
    z = sum(q[2] for q in J[2:]) / 2 + 1.0 * scale
    mid = ((J[0][0] * 0.4 + J[1][0] * 0.6), (J[0][1] * 0.4 + J[1][1] * 0.6))
    parts.append((z, Part(tpath, fill, tones, form, masks=[(J[0][0], J[0][1], R[0] * 1.3), (mid[0], mid[1], R[0] * 1.1)])))
    parts.sort(key=lambda zp: zp[0])
    out = [p for _, p in parts]
    if post:
        out[-1].post = post
    return out


# ------------------------------------------------------------------ voice -> lip-sync

VISEMES = {          # open, wide, round, teeth
    "rest": (0.0, 0.0, 0.0, 0.0),
    "slight": (0.20, 0.05, 0.0, 0.35),
    "aa": (0.85, 0.12, 0.0, 0.55),
    "ee": (0.40, 0.85, 0.0, 1.0),
    "oo": (0.46, -0.35, 1.0, 0.0),
    "ss": (0.13, 0.60, 0.0, 1.0),
}


class Voice:
    """Voice clips placed on a timeline, analysed once at 30 fps.

    env[f]       loudness 0..1 (dB, normalised to the take's own range)
    vis[f]       viseme name per frame: silence -> rest; sibilant hiss -> ss; low-only spectrum -> oo;
                 strong 1.7-3.2 kHz over 0.25-1.1 kHz (front vowels) -> ee; loud -> aa; quiet -> slight
                 (each choice held at least 2 frames so the mouth never flickers)
    mouth(t)     dict(open, wide, round, teeth): the viseme presets scaled by loudness and smoothed
                 (fast attack, slower release), 1 frame ahead of the sound
    phrases      [(start, end)] voiced stretches split at pauses >= 0.16 s
    peaks        times of stressed syllables (loudness peaks)
    """

    def __init__(self, clips, total, fps=30, sr=44100, lead_frames=1.0):
        import soundfile as sf
        self.fps, self.sr, self.total = fps, sr, total
        y = np.zeros(int(total * sr) + sr, np.float32)
        for path, t0 in clips:
            a, r = sf.read(path, dtype="float32")
            if a.ndim > 1:
                a = a.mean(1)
            if r != sr:
                idx = np.arange(0, len(a), r / sr)
                a = np.interp(idx, np.arange(len(a)), a).astype(np.float32)
            i0 = int(round(t0 * sr))
            m = min(len(a), len(y) - i0)
            y[i0:i0 + m] += a[:m]
        self.y = y[:int(total * sr)]
        n = int(round(total * fps))
        self.n = n
        N = 2048
        win = np.hanning(N).astype(np.float32)
        freqs = np.fft.rfftfreq(N, 1 / sr)

        def band(P, lo, hi):
            return P[(freqs >= lo) & (freqs < hi)].sum() + 1e-12
        rms = np.zeros(n)
        r_ee = np.zeros(n)
        r_oo = np.zeros(n)
        sib = np.zeros(n)
        pad = np.concatenate([np.zeros(N, np.float32), self.y, np.zeros(2 * N, np.float32)])
        for f in range(n):
            c = int((f + lead_frames) / fps * sr) + N
            seg = pad[c - N // 2:c + N // 2]
            core = seg[N // 2 - 520:N // 2 + 520]          # ~24 ms: follows syllables
            rms[f] = math.sqrt(float(np.mean(core * core)))
            P = np.abs(np.fft.rfft(seg * win)) ** 2
            lo_v = band(P, 250, 1100)
            r_ee[f] = math.log(band(P, 1700, 3200) / lo_v)
            r_oo[f] = math.log(band(P, 120, 650) / (band(P, 650, 3200)))
            sib[f] = band(P, 4000, 11000) / band(P, 90, 11000)
        db = 20 * np.log10(rms + 1e-6)
        top = float(np.percentile(db, 97))
        env = np.clip((db - (top - 25.0)) / 23.0, 0, 1)
        self.env = env
        voiced = env > 0.10
        # phrases: voiced runs, gaps < 0.16 s bridged, blips < 0.1 s dropped
        runs, f = [], 0
        while f < n:
            if voiced[f]:
                g = f
                while g < n and voiced[g]:
                    g += 1
                runs.append([f, g])
                f = g
            else:
                f += 1
        merged = []
        for a, b in runs:
            if merged and a - merged[-1][1] < 0.16 * fps:
                merged[-1][1] = b
            else:
                merged.append([a, b])
        self.phrases = [(a / fps, b / fps) for a, b in merged if b - a >= 0.1 * fps]
        # stressed peaks
        sm = np.convolve(env, [0.25, 0.5, 0.25], mode="same")
        peaks = []
        for f in range(2, n - 2):
            lo, hi = max(0, f - 6), min(n, f + 7)
            if sm[f] >= 0.62 and sm[f] == sm[lo:hi].max():
                if not peaks or f - peaks[-1] >= 8:
                    peaks.append(f)
        self.peaks = [f / fps for f in peaks]
        # visemes
        vv = env > 0.4                       # thresholds from the take's own spread (rank-based, robust to skew)
        oo_hi = np.percentile(r_oo[vv], 62) if vv.any() else 1e9
        ee_lo = np.percentile(r_ee[vv], 45) if vv.any() else -1e9
        ee_hi = np.percentile(r_ee[vv], 80) if vv.any() else 1e9
        vis = []
        for f in range(n):
            e = env[f]
            if e < 0.12:
                v = "rest"
            elif sib[f] > 0.42 and e < 0.8:
                v = "ss"
            elif e < 0.5:
                v = "slight"
            elif r_oo[f] > oo_hi and r_ee[f] < ee_lo:
                v = "oo"
            elif r_ee[f] > ee_hi:
                v = "ee"
            else:
                v = "aa"
            vis.append(v)
        for f in range(1, n - 1):                       # 1-frame blips -> neighbour
            if vis[f] != vis[f - 1] and vis[f] != vis[f + 1]:
                vis[f] = vis[f - 1]
        self.vis = vis
        # parameters: preset scaled by loudness, then attack/release smoothing
        keys = ("open", "wide", "round", "teeth")
        tgt = np.zeros((n, 4))
        for f in range(n):
            o, w, r, th = VISEMES[vis[f]]
            k = 0.25 + 0.85 * smooth((env[f] - 0.3) / 0.65) if vis[f] != "rest" else 0.0
            tgt[f] = (o * k, w, r, th)
        out = np.zeros_like(tgt)
        cur = np.zeros(4)
        for f in range(n):
            for j in range(4):
                a = 0.62 if abs(tgt[f, j]) > abs(cur[j]) else 0.42
                cur[j] += (tgt[f, j] - cur[j]) * a
            out[f] = cur
        self.params = out
        self.keys = keys

    def _frame(self, t):
        x = clamp(t * self.fps, 0, self.n - 1)
        i = min(int(x), self.n - 2)
        return i, x - i

    def mouth(self, t):
        i, u = self._frame(t)
        v = self.params[i] * (1 - u) + self.params[i + 1] * u
        return dict(zip(self.keys, v))

    def level(self, t):
        i, u = self._frame(t)
        return float(self.env[i] * (1 - u) + self.env[i + 1] * u)

    def activity(self, t, span=0.35):
        """Smoothed 'is talking' 0..1 (for livelier head motion while speaking)."""
        a = max(0, int((t - span) * self.fps))
        b = min(self.n, int((t + span) * self.fps) + 1)
        return float(np.mean(self.env[a:b] > 0.12)) if b > a else 0.0

    def write_wav(self, path):
        import soundfile as sf
        sf.write(path, self.y, self.sr, subtype="PCM_16")


# ------------------------------------------------------------------ blinks and gaze

def _blink_curve(d):
    if d < 0 or d > 0.26:
        return 0.0
    if d < 0.065:
        return smooth(d / 0.065)
    if d < 0.10:
        return 1.0
    return 1 - smooth((d - 0.10) / 0.16)


class Blinks:
    """Natural blinks every lo..hi s (a double blink now and then), plus forced blinks (e.g. on big head turns)."""

    def __init__(self, total, seed=7, lo=2.5, hi=5.0, double=0.28, extra=()):
        rng = random.Random(seed)
        t = rng.uniform(0.9, 1.8)
        ev = []
        while t < total:
            ev.append(t)
            if rng.random() < double:
                ev.append(t + rng.uniform(0.27, 0.34))
            t += rng.uniform(lo, hi)
        self.events = sorted(ev + list(extra))

    def __call__(self, t):
        return max((_blink_curve(t - e) for e in self.events), default=0.0)


class Gaze:
    """Eye darts: small saccades (2-frame moves) around a base direction, held 0.5-1.8 s."""

    def __init__(self, total, seed=11, amp=(0.22, 0.12)):
        rng = random.Random(seed)
        t, self.ev = 0.0, [(0.0, 0.0, 0.0)]
        while t < total:
            t += rng.uniform(0.5, 1.8)
            if rng.random() < 0.45:
                self.ev.append((t, 0.0, 0.0))          # back to the viewer
            else:
                self.ev.append((t, rng.uniform(-1, 1) * amp[0], rng.uniform(-1, 0.6) * amp[1]))

    def __call__(self, t):
        gx = gy = 0.0
        for i, (te, x, y) in enumerate(self.ev):
            if t < te:
                break
            px, py = (self.ev[i - 1][1], self.ev[i - 1][2]) if i else (x, y)
            k = smooth((t - te) / 0.07)
            gx, gy = lerp(px, x, k), lerp(py, y, k)
        return gx, gy


# ------------------------------------------------------------------ pose tracks

class Track:
    """Keyed poses with smooth, springy transitions.

    poses   {name: {param: value}}  (a pose may leave params out: they keep the previous target)
    keys    [(t, name, dur)]        the first key is the starting pose
    delays  {param: seconds}        later start for some params (wrist/fingers trail the arm: follow-through)
    """

    def __init__(self, poses, keys, delays=None, ease=spring, defaults=None):
        self.poses, self.keys = poses, sorted(keys, key=lambda k: k[0])
        self.delays, self.ease = delays or {}, ease
        self.params = list(dict.fromkeys(p for v in poses.values() for p in v))
        self.defaults = defaults or {}
        first = self.poses[self.keys[0][1]]
        self.targets = []
        cur = {p: first.get(p, self.defaults.get(p, 0.0)) for p in self.params}
        for tk, name, dur in self.keys:
            cur = dict(cur)
            cur.update(self.poses[name])
            self.targets.append((tk, cur, dur))

    def value(self, param, t):
        tt = t - self.delays.get(param, 0.0)
        v0 = self.targets[0][1][param]
        cf, ct, c0, cd = v0, v0, -1e9, 1.0
        for tk, tgt, dur in self.targets[1:]:
            if tt < tk:
                break
            vk = cf + (ct - cf) * self.ease((tk - c0) / cd)
            cf, ct, c0, cd = vk, tgt[param], tk, dur
        return cf + (ct - cf) * self.ease((tt - c0) / cd)

    def at(self, t):
        return {p: self.value(p, t) for p in self.params}
