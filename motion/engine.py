"""Core helpers: timing/easing, hand-drawn ("boiling") shapes, handwritten text.

Everything is drawn with pycairo on a 720x1280 (9:16) canvas.
"""
import math
import os
import random

W, H = 720, 1280
FPS = 30

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")


def register_fonts():
    """Point fontconfig at assets/fonts so cairo can find Kalam. Call before importing cairo."""
    conf = os.path.join(ROOT, "build", "fonts.conf")
    os.makedirs(os.path.dirname(conf), exist_ok=True)
    with open(conf, "w") as f:
        f.write(
            '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
            "<fontconfig>\n"
            "  <include ignore_missing=\"yes\">/etc/fonts/fonts.conf</include>\n"
            f"  <dir>{FONT_DIR}</dir>\n"
            f"  <cachedir>{os.path.join(ROOT, 'build', 'fontcache')}</cachedir>\n"
            "</fontconfig>\n"
        )
    os.environ["FONTCONFIG_FILE"] = conf


register_fonts()
import cairo  # noqa: E402

FONT = "Kalam"

# ---------------------------------------------------------------- palette
def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


INK = hexc("#2a2230")
RED = hexc("#d8363a")
CREAM = hexc("#efe4c8")
GROUND = hexc("#c7c2a6")
WHITE = hexc("#fbf8ef")

# ---------------------------------------------------------------- timing
_state = {"frame": 0, "offset": 0.0}
EVENTS = []  # (abs_time, sound_name, duration) collected while rendering, used for the soundtrack


def set_frame(i, scene_offset=0.0):
    _state["frame"] = i
    _state["offset"] = scene_offset


def cue(name, t, start, dur=0.0):
    """Register a sound effect when scene time t first reaches `start`."""
    if start <= t < start + 1.0 / FPS:
        EVENTS.append((_state["offset"] + start, name, dur))


def boil():
    """Index that changes ~8 times a second, so outlines 'boil' like hand animation."""
    return _state["frame"] // 4


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def seg(t, a, b):
    """0..1 progress of t through the window [a, b]."""
    if b <= a:
        return 1.0 if t >= a else 0.0
    return clamp01((t - a) / (b - a))


def lerp(a, b, u):
    return a + (b - a) * u


def smooth(u):
    u = clamp01(u)
    return u * u * (3 - 2 * u)


def ease_out(u):
    u = clamp01(u)
    return 1 - (1 - u) ** 3


def ease_in(u):
    u = clamp01(u)
    return u ** 3


def back_out(u, s=1.9):
    u = clamp01(u)
    u -= 1
    return u * u * ((s + 1) * u + s) + 1


def pop(t, start, dur=0.35):
    """Scale 0 -> overshoot -> 1 starting at `start`."""
    return back_out(seg(t, start, start + dur)) if t >= start else 0.0


def blink(t, seed=0):
    """True for a couple of frames every few seconds."""
    period = 3.1 + (seed % 5) * 0.37
    return (t + seed * 0.71) % period < 0.09


# ---------------------------------------------------------------- noise / wobble
def _rng(seed):
    return random.Random(hash((seed, boil())) & 0xFFFFFFFF)


def wobble(pts, seed, amp=1.4):
    r = _rng(seed)
    return [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in pts]


def _catmull(cr, pts, closed):
    n = len(pts)
    if n < 2:
        return
    cr.move_to(*pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        cr.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        cr.close_path()


def ellipse_pts(cx, cy, rx, ry, n=22, start=0.0):
    return [
        (cx + rx * math.cos(start + 2 * math.pi * i / n), cy + ry * math.sin(start + 2 * math.pi * i / n))
        for i in range(n)
    ]


def rrect_pts(x, y, w, h, r, step=18):
    """Points around a rounded rectangle (x, y = top-left)."""
    r = min(r, w / 2, h / 2)
    pts = []
    corners = [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]
    for cx, cy, a0 in corners:
        for k in range(4):
            a = math.radians(a0 + 90 * k / 3)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    # add straight-edge midpoints so long edges also wobble
    out = []
    for i, p in enumerate(pts):
        out.append(p)
        q = pts[(i + 1) % len(pts)]
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        k = int(d // step)
        for j in range(1, k):
            out.append((lerp(p[0], q[0], j / k), lerp(p[1], q[1], j / k)))
    return out


def poly_pts(corners, step=16):
    """Densify a polygon so straight edges get a subtle hand-drawn wobble."""
    out = []
    n = len(corners)
    for i in range(n):
        p, q = corners[i], corners[(i + 1) % n]
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        k = max(1, int(d // step))
        for j in range(k):
            out.append((lerp(p[0], q[0], j / k), lerp(p[1], q[1], j / k)))
    return out


def shape(cr, pts, fill=None, seed=0, amp=1.3, lw=4.0, stroke=INK, closed=True):
    pts = wobble(pts, seed, amp) if amp else pts
    _catmull(cr, pts, closed)
    if fill is not None and closed:
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
    else:
        cr.new_path()


def sharp_shape(cr, corners, fill=None, seed=0, amp=1.2, lw=4.0, stroke=INK):
    """Polygon with straight-ish (jittered) edges and sharp corners."""
    pts = wobble(corners, seed, amp)
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    if fill is not None:
        cr.set_source_rgba(*fill)
        cr.fill_preserve()
    if stroke is not None and lw:
        cr.set_source_rgba(*stroke)
        cr.set_line_width(lw)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    cr.new_path()


def blob(cr, cx, cy, rx, ry, fill, seed=0, amp=1.3, lw=4.0, stroke=INK, n=22):
    shape(cr, ellipse_pts(cx, cy, rx, ry, n), fill, seed, amp, lw, stroke)


def line(cr, pts, lw=4.0, color=INK, seed=0, amp=1.0):
    shape(cr, pts, None, seed, amp, lw, color, closed=False)


def dot(cr, x, y, r, color=INK):
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*color)
    cr.fill()


# ---------------------------------------------------------------- text
def _font(cr, size, bold=False):
    cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def text_width(cr, runs, size, bold=False):
    _font(cr, size, bold)
    return sum(cr.text_extents(s).x_advance for s, _ in runs)


def write(cr, runs, x, y, size, progress=1.0, align="left", bold=False, underline=False, halo=None):
    """Handwritten text that 'writes on' left-to-right as progress goes 0 -> 1.

    runs: list of (text, color) or a plain string (drawn in INK).
    y is the baseline.
    """
    if isinstance(runs, str):
        runs = [(runs, INK)]
    if progress <= 0:
        return 0
    _font(cr, size, bold)
    total = sum(cr.text_extents(s).x_advance for s, _ in runs)
    if align == "center":
        x -= total / 2
    elif align == "right":
        x -= total
    cr.save()
    # slight per-boil jitter makes static text feel hand drawn
    r = _rng(hash((x, y, size)))
    cr.translate(r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6))
    cr.rectangle(x - 10, y - size * 1.4, (total + 20) * clamp01(progress), size * 2.0)
    cr.clip()
    if halo is not None:   # soft outline so text stays readable over busy backgrounds
        cx = x
        for s, _ in runs:
            cr.move_to(cx, y)
            cr.text_path(s)
            cx += cr.text_extents(s).x_advance
        cr.set_source_rgba(*halo)
        cr.set_line_width(size * 0.22)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    cx = x
    for s, col in runs:
        cr.set_source_rgba(*col)
        cr.move_to(cx, y)
        cr.show_text(s)
        cx += cr.text_extents(s).x_advance
    if underline:
        line(cr, [(x, y + size * 0.22), (x + total / 2, y + size * 0.26), (x + total, y + size * 0.2)], 3, INK, seed=7)
    cr.restore()
    return total


def write_t(cr, runs, x, y, size, t, start, dur=None, end=None, **kw):
    """write() driven by scene time; optional `end` erases (fades) the text."""
    if isinstance(runs, str):
        runs = [(runs, INK)]
    n = sum(len(s) for s, _ in runs)
    dur = dur if dur is not None else max(0.35, 0.045 * n)
    cue("scribble", t, start, dur)
    p = seg(t, start, start + dur)
    cr.save()
    cr.identity_matrix()  # captions are always screen-space, whatever camera the scene uses
    if end is not None and t > end:
        a = 1 - seg(t, end, end + 0.25)
        if a > 0:
            cr.push_group()
            write(cr, runs, x, y, size, p, **kw)
            cr.pop_group_to_source()
            cr.paint_with_alpha(a)
    else:
        write(cr, runs, x, y, size, p, **kw)
    cr.restore()


# ---------------------------------------------------------------- transforms
class at:
    """Context manager: translate/scale/rotate around a point."""

    def __init__(self, cr, x, y, s=1.0, rot=0.0, flip=False):
        self.cr, self.x, self.y, self.s, self.rot, self.flip = cr, x, y, s, rot, flip

    def __enter__(self):
        self.cr.save()
        self.cr.translate(self.x, self.y)
        if self.rot:
            self.cr.rotate(self.rot)
        self.cr.scale(-self.s if self.flip else self.s, self.s)
        return self.cr

    def __exit__(self, *a):
        self.cr.restore()
