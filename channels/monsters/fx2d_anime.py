"""The 2D anime kit for "Cute Things Kill Here" that the 3D models can't do themselves, after
reports/Pokémon episodes story and animation.md:

- comic faces drawn over a face (TP7): sweat_drop, dot_eyes, tear_streams, swirl_eyes, terror_eyes, anger_mark,
  blush_lines;
- full-frame emotion backgrounds (SU16, IM6) to put behind a subject pass with comp.backdrop:
  emotion_bg(mood=) with "realisation", "dread", "love", "gloom", "rage", "victory";
- the split screen for face-offs and the A/B ending (SG7, AB13): split() with jagged white dividers, 2 to 5 panels;
- the observer shake on 2s (IM5): shake() moves the picture drawn so far, shake_offset() gives the bare offsets.

Every function follows the fx2d convention fn(cr, t, start, ...) and draws nothing outside its window. Comic faces
cut in and out hard (the anime swaps them on a cut); the backgrounds and the split are hard cuts too (SG12).
Effects that jitter do it on 2s (IM4). No HUD and no text in the picture.

Face placement: (x, y) is the point between the eyes and `size` the face width in pixels; `tilt` turns the face
(radians). For a three-quarter view pass `eyes=((x1, y1), (x2, y2))` and, if needed, the eye radius `er`.
"""
import math
import random

from channels.monsters.fx2d import INK, WHITE, _glow, _star4, _twos, _wedge, hexa
from motion.engine import FPS, H, W, back_out, cairo, clamp01, cue, ease_out

SKIN = hexa("#fbe3d6")               # the hero's skin under the comic eyes (mk/hero.py restyle)
TEAR = hexa("#9fd8ff")
TEAR_LINE = hexa("#2f6fae")
RED = hexa("#e8303a")
PINK = hexa("#ff8fb1")


# ---------------------------------------------------------------- helpers
def _on(t, start, end, dur):
    """True inside the window: start..end, or start..start+dur when end is None."""
    stop = start + dur if end is None else end
    return start <= t <= stop


def _rot(x, y, dx, dy, tilt):
    c, s = math.cos(tilt), math.sin(tilt)
    return x + dx * c - dy * s, y + dx * s + dy * c


def _eyes(x, y, size, tilt, eyes, er):
    if eyes is None:
        eyes = (_rot(x, y, -0.23 * size, 0, tilt), _rot(x, y, 0.23 * size, 0, tilt))
    return eyes, (0.1 * size if er is None else er)


def _frame(t, start):
    return int(math.floor((t - start) * FPS + 1e-6))


# ================================================================ comic faces (TP7)
def _drop(cr, h):
    """A teardrop with its point up, h tall, its round end centred at (0, 0)."""
    r = h * 0.36
    cr.move_to(0, -h + r)
    cr.curve_to(r * 0.35, -h * 0.55, r, -r * 0.6, r, 0)
    cr.arc(0, 0, r, 0, math.pi)
    cr.curve_to(-r, -r * 0.6, -r * 0.35, -h * 0.55, 0, -h + r)
    cr.close_path()


def sweat_drop(cr, t, start, x, y, size=200, end=None, side=1, bead=False, tilt=0.0):
    """The anime sweat drop beside the head (side=1 right, -1 left): pops in and slides a little. bead=True gives
    the small bead that runs slowly down the temple (a tense, quiet hold)."""
    if not _on(t, start, end, 1.5):
        return
    u = t - start
    if bead:
        h = 0.13 * size
        px, py = _rot(x, y, side * 0.36 * size, -0.3 * size + 0.35 * size * ease_out(u / 2.5), tilt)
        s = 1.0
    else:
        h = 0.36 * size
        px, py = _rot(x, y, side * 0.5 * size, -0.22 * size + 0.06 * size * ease_out(u / 0.6), tilt)
        s = max(0.01, back_out(u / 0.12, 2.0))
    cr.save()
    cr.translate(px, py)
    cr.rotate(tilt - side * 0.15)
    cr.scale(s, s)
    _drop(cr, h)
    cr.set_source_rgba(*TEAR)
    cr.fill_preserve()
    cr.set_source_rgba(*TEAR_LINE)
    cr.set_line_width(max(2.0, h * 0.06))
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
    cr.arc(-h * 0.13, -h * 0.05, h * 0.07, 0, 2 * math.pi)        # white highlights
    cr.set_source_rgba(1, 1, 1, 0.95)
    cr.fill()
    cr.move_to(-h * 0.06, -h * 0.5)
    cr.curve_to(-h * 0.15, -h * 0.35, -h * 0.2, -h * 0.25, -h * 0.2, -h * 0.18)
    cr.set_line_width(max(1.5, h * 0.04))
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()
    cr.restore()


def _cover_eye(cr, ex, ey, rx, ry, tilt, col):
    """Paint over the model's eye with a soft-edged patch (skin or white)."""
    cr.save()
    cr.translate(ex, ey)
    cr.rotate(tilt)
    cr.scale(rx, ry)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, *col[:3], 1)
    g.add_color_stop_rgba(0.82, *col[:3], 1)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.set_source(g)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def dot_eyes(cr, t, start, x, y, size=200, end=None, eyes=None, er=None, skin=SKIN, tilt=0.0):
    """Blank dot eyes (deadpan, disbelief): the eyes are painted over in skin and replaced by two small black dots."""
    if not _on(t, start, end, 1.5):
        return
    eyes, er = _eyes(x, y, size, tilt, eyes, er)
    for ex, ey in eyes:
        _cover_eye(cr, ex, ey, er * 1.8, er * 1.5, tilt, skin)
        cr.arc(ex, ey, er * 0.24, 0, 2 * math.pi)
        cr.set_source_rgba(*INK)
        cr.fill()


def tear_streams(cr, t, start, x, y, size=200, end=None, eyes=None, er=None, tilt=0.0):
    """Comic crying: two wobbling streams that pour from the lower outer corner of each eye, arc outward over the
    cheeks and widen as they fall, with highlights running down them."""
    if not _on(t, start, end, 2.0):
        return
    u = t - start
    eyes, er = _eyes(x, y, size, tilt, eyes, er)
    ln = 0.62 * size * ease_out(u / 0.2)
    w = 0.11 * size
    if ln < 2:
        return
    for k, (ex, ey) in enumerate(eyes):
        sx = -1 if k == 0 else 1

        def centre(v):
            wob = math.sin(v * 7 + u * 16 + k * 2) * w * 0.22 * v
            return sx * (0.1 * size * v + 0.16 * size * v * v) + wob, v * ln

        cr.save()
        cr.translate(*_rot(ex, ey, sx * er * 0.55, er * 0.75, tilt))
        cr.rotate(tilt)
        left, right = [], []
        for i in range(17):
            v = i / 16
            cx, cy = centre(v)
            half = w * (0.18 + 0.82 * math.sqrt(v)) / 2
            left.append((cx - half, cy))
            right.append((cx + half, cy))
        cr.move_to(*left[0])
        for p in left[1:]:
            cr.line_to(*p)
        bx, by = centre(1.0)
        cr.arc_negative(bx, by, w / 2, math.pi, 0)              # the rounded end
        for p in reversed(right):
            cr.line_to(*p)
        cr.close_path()
        g = cairo.LinearGradient(0, 0, 0, ln)
        g.add_color_stop_rgba(0, *TEAR[:3], 0.95)
        g.add_color_stop_rgba(1, *TEAR[:3], 0.75)
        cr.set_source(g)
        cr.fill_preserve()
        cr.set_source_rgba(*TEAR_LINE[:3], 0.9)
        cr.set_line_width(max(1.5, w * 0.1))
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
        cr.set_source_rgba(1, 1, 1, 0.9)                         # highlight dashes running down the stream
        cr.set_line_width(max(1.5, w * 0.14))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for j in range(3):
            v0 = (u * 1.8 + j / 3) % 1.0
            v1 = min(1.0, v0 + 0.12)
            p0, p1 = centre(v0), centre(v1)
            cr.move_to(p0[0] - w * 0.18 * math.sqrt(v0), p0[1])
            cr.line_to(p1[0] - w * 0.18 * math.sqrt(v1), p1[1])
        cr.stroke()
        cr.restore()


def swirl_eyes(cr, t, start, x, y, size=200, end=None, eyes=None, er=None, tilt=0.0):
    """Dizzy swirl eyes: white discs with black spirals turning (on 2s)."""
    if not _on(t, start, end, 1.5):
        return
    eyes, er = _eyes(x, y, size, tilt, eyes, er)
    turn = _twos(t - start) * 2 / FPS * 2 * math.pi * 1.5             # 1.5 turns a second, stepped on 2s
    r = er * 1.35
    for k, (ex, ey) in enumerate(eyes):
        cr.save()
        cr.translate(ex, ey)
        cr.arc(0, 0, r, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(max(2.0, r * 0.1))
        cr.stroke()
        direction = 1 if k == 0 else -1
        for i in range(61):
            v = i / 60
            a = direction * (v * 3 * 2 * math.pi + turn)
            px, py = math.cos(a) * r * 0.88 * v, math.sin(a) * r * 0.88 * v
            (cr.move_to if i == 0 else cr.line_to)(px, py)
        cr.set_line_width(max(2.0, r * 0.11))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
        cr.restore()


def terror_eyes(cr, t, start, x, y, size=200, end=None, eyes=None, er=None, shade=True, tilt=0.0, seed=0):
    """Pin-prick terror eyes: white eyes with tiny trembling pupils; shade=True adds the blue vertical lines of
    shock over the upper face."""
    if not _on(t, start, end, 1.5):
        return
    eyes, er = _eyes(x, y, size, tilt, eyes, er)
    if shade:
        cr.save()
        cr.translate(x, y)
        cr.rotate(tilt)
        top, bot = -0.45 * size, -0.05 * size
        g = cairo.LinearGradient(0, top, 0, bot)
        g.add_color_stop_rgba(0, 0.12, 0.2, 0.55, 0.7)
        g.add_color_stop_rgba(1, 0.12, 0.2, 0.55, 0)
        cr.set_source(g)
        for i in range(11):
            xx = (-0.42 + 0.084 * i) * size
            cr.rectangle(xx, top, max(2.0, 0.018 * size), (bot - top) * (0.75 + 0.25 * ((i * 7) % 3) / 2))
        cr.fill()
        cr.restore()
    rnd = random.Random(seed * 131 + _frame(t, start))                 # pupils tremble every frame
    for ex, ey in eyes:
        cr.save()
        cr.translate(ex, ey)
        cr.rotate(tilt)
        cr.save()
        cr.scale(er * 1.3, er * 1.45)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(max(2.0, er * 0.14))
        cr.stroke()
        j = er * 0.09
        cr.arc(rnd.uniform(-j, j), rnd.uniform(-j, j), max(2.0, er * 0.14), 0, 2 * math.pi)
        cr.set_source_rgba(*INK)
        cr.fill()
        cr.restore()


def anger_mark(cr, t, start, x, y, size=200, end=None, side=1, tilt=0.0):
    """The red cross-shaped anger vein on the temple, throbbing."""
    if not _on(t, start, end, 1.5):
        return
    u = t - start
    px, py = _rot(x, y, side * 0.38 * size, -0.42 * size, tilt)
    s = max(0.01, back_out(u / 0.1, 3.0)) * (1 + 0.14 * max(0.0, math.sin(u * 2 * math.pi * 3.5)))
    r = 0.11 * size * s
    cr.save()
    cr.translate(px, py)
    cr.rotate(tilt + 0.25)
    for q in range(4):                                         # four brackets, their backs to the centre
        cr.save()
        cr.rotate(q * math.pi / 2 + math.pi / 4)
        cr.move_to(r * 0.28, -r * 0.62)
        cr.curve_to(r * 0.28, -r * 0.2, r * 0.2, -r * 0.18, r * 0.62, -r * 0.18)
        cr.restore()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_source_rgba(1, 1, 1, 0.9)
    cr.set_line_width(r * 0.5)
    cr.stroke_preserve()
    cr.set_source_rgba(*RED)
    cr.set_line_width(r * 0.3)
    cr.stroke()
    cr.restore()


def blush_lines(cr, t, start, x, y, size=200, end=None, eyes=None, er=None, tilt=0.0):
    """Embarrassment: soft pink cheeks with short diagonal hatch lines under each eye."""
    if not _on(t, start, end, 1.5):
        return
    eyes, er = _eyes(x, y, size, tilt, eyes, er)
    for ex, ey in eyes:
        cx, cy = _rot(ex, ey, 0, 0.22 * size, tilt)
        cr.save()
        cr.translate(cx, cy)
        cr.rotate(tilt)
        cr.save()
        cr.scale(0.15 * size, 0.07 * size)
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
        g.add_color_stop_rgba(0, *PINK[:3], 0.7)
        g.add_color_stop_rgba(1, *PINK[:3], 0)
        cr.set_source(g)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.fill()
        cr.restore()
        for i in range(4):
            xx = (-0.09 + 0.06 * i) * size
            cr.move_to(xx + 0.022 * size, -0.035 * size)
            cr.line_to(xx - 0.022 * size, 0.035 * size)
        cr.set_source_rgba(0.85, 0.25, 0.35, 0.9)
        cr.set_line_width(max(2.0, 0.014 * size))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
        cr.restore()


# ================================================================ emotion backgrounds (SU16, IM6)
def _radial(cr, cx, cy, stops, r=None):
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, r or math.hypot(W, H) * 0.6)
    for at, col in stops:
        g.add_color_stop_rgb(at, *col[:3])
    cr.set_source(g)
    cr.paint()


def _vertical(cr, stops):
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, col in stops:
        g.add_color_stop_rgb(at, *col[:3])
    cr.set_source(g)
    cr.paint()


def _realisation(cr, t, start, cx, cy, seed):
    """Electric blue with sharp white radial lines and a white flash on the first frames."""
    _radial(cr, cx, cy, [(0, hexa("#bfe9ff")), (0.18, hexa("#2f8dff")), (0.6, hexa("#1638a8")),
                         (1, hexa("#0a1240"))])
    rnd = random.Random(seed * 991 + _twos(t - start))
    cr.set_source_rgba(1, 1, 1, 0.9)
    for _ in range(90):
        _wedge(cr, cx, cy, rnd.uniform(0, 2 * math.pi), 170 * rnd.uniform(0.9, 2.2), 1600, rnd.uniform(2, 11))
    cr.fill()
    flash = 1 - clamp01((t - start) / 0.12)
    if flash > 0:
        cr.set_source_rgba(1, 1, 1, flash)
        cr.paint()


def _dread(cr, t, start, cx, cy, seed):
    """Near-black violet with dark wavy lines creeping down and a slow vignette breath."""
    _vertical(cr, [(0, hexa("#07040f")), (0.55, hexa("#1d1033")), (1, hexa("#0b0716"))])
    rnd = random.Random(seed * 17 + 3)
    u = t - start
    for i in range(13):
        x0 = (i + 0.5) * W / 13 + rnd.uniform(-18, 18)
        amp, freq, ph = rnd.uniform(14, 34), rnd.uniform(0.008, 0.016), rnd.uniform(0, 6)
        for k in range(0, H + 21, 20):
            xx = x0 + amp * math.sin(k * freq + ph - u * 2.2)
            (cr.move_to if k == 0 else cr.line_to)(xx, k)
        cr.set_source_rgba(0.42, 0.22, 0.62, rnd.uniform(0.35, 0.6))
        cr.set_line_width(rnd.uniform(5, 13))
        cr.stroke()
    breath = 0.55 + 0.15 * math.sin(u * 2.6)
    g = cairo.RadialGradient(cx, cy, H * 0.2, cx, cy, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, breath)
    cr.set_source(g)
    cr.paint()


def _heart(cr, x, y, s):
    cr.move_to(x, y + s * 0.35)
    cr.curve_to(x - s * 1.1, y - s * 0.35, x - s * 0.45, y - s * 1.05, x, y - s * 0.45)
    cr.curve_to(x + s * 0.45, y - s * 1.05, x + s * 1.1, y - s * 0.35, x, y + s * 0.35)
    cr.close_path()


def _love(cr, t, start, cx, cy, seed):
    """Soft pink with bokeh, rising hearts and twinkles."""
    _radial(cr, cx, cy, [(0, hexa("#fff0f6")), (0.35, hexa("#ffb3cf")), (1, hexa("#e2588f"))])
    u = t - start
    rnd = random.Random(seed * 53 + 1)
    for _ in range(12):
        bx, by, br = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(30, 90)
        _glow(cr, bx, (by - u * 30) % (H + 200) - 100, br, (1, 1, 1), rnd.uniform(0.15, 0.35))
    for _ in range(14):
        hx, hy, hs = rnd.uniform(40, W - 40), rnd.uniform(0, H), rnd.uniform(18, 46)
        sp, ph = rnd.uniform(60, 140), rnd.uniform(0, 6)
        yy = (hy - u * sp) % (H + 120) - 60
        xx = hx + 16 * math.sin(u * 2 + ph)
        _heart(cr, xx, yy, hs)
        cr.set_source_rgba(1, 1, 1, 0.75)
        cr.set_line_width(hs * 0.18)
        cr.stroke_preserve()
        cr.set_source_rgba(*hexa("#ff4f8b")[:3], 0.85)
        cr.fill()
    for _ in range(9):
        sx, sy, ss = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(10, 24)
        k = 0.5 + 0.5 * math.sin(u * 7 + sx)
        _star4(cr, sx, sy, ss * (0.6 + 0.4 * k))
        cr.set_source_rgba(1, 1, 1, 0.5 + 0.5 * k)
        cr.fill()


def _gloom(cr, t, start, cx, cy, seed):
    """Grey-blue, darkest at the top, with the vertical lines of gloom hanging down from the top edge."""
    _vertical(cr, [(0, hexa("#141a2a")), (0.5, hexa("#3a4660")), (1, hexa("#5d6a82"))])
    rnd = random.Random(seed * 29 + 5)
    u = t - start
    for i in range(30):
        x = (i + 0.5) * W / 30 + rnd.uniform(-6, 6)
        ln = H * rnd.uniform(0.3, 0.75) * (0.92 + 0.08 * math.sin(u * 1.5 + i))
        g = cairo.LinearGradient(0, 0, 0, ln)
        g.add_color_stop_rgba(0, 0.03, 0.05, 0.12, 0.9)
        g.add_color_stop_rgba(1, 0.03, 0.05, 0.12, 0)
        cr.set_source(g)
        cr.rectangle(x, 0, rnd.uniform(3, 9), ln)
        cr.fill()


def _rage(cr, t, start, cx, cy, seed):
    """Deep red with turning dark rays and flames licking up from the bottom, redrawn on 2s."""
    _radial(cr, cx, cy, [(0, hexa("#ffb02e")), (0.25, hexa("#ff4a1c")), (0.65, hexa("#b0101e")),
                         (1, hexa("#4a0510"))])
    u = t - start
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(u * 0.5)
    cr.set_source_rgba(0.35, 0.0, 0.05, 0.35)
    for i in range(16):
        a = i * 2 * math.pi / 16
        _wedge(cr, 0, 0, a, 0, 1600, 220)
    cr.fill()
    cr.restore()
    step = _twos(u)
    for layer, (col, top, a) in enumerate(((hexa("#7a0612"), 0.45, 1.0), (hexa("#ff4a1c"), 0.6, 0.95),
                                           (hexa("#ffcf3a"), 0.77, 0.9))):
        rnd = random.Random(seed * 7 + layer * 1000 + step)
        n = 9
        tw = W / n
        cr.move_to(-tw, H)
        for i in range(-1, n + 1):                              # one curling tongue of flame per slot
            x0 = i * tw + rnd.uniform(-10, 10)
            base = H * (top + 0.12)
            tip_y = H * (top + rnd.uniform(-0.08, 0.04))
            lean = rnd.uniform(-0.5, 0.5) * tw
            tip_x = x0 + tw / 2 + lean
            cr.line_to(x0, base)
            cr.curve_to(x0 + tw * 0.1, base - (base - tip_y) * 0.5, tip_x - lean * 0.2 - tw * 0.15, tip_y + 40,
                        tip_x, tip_y)
            cr.curve_to(tip_x + tw * 0.05, tip_y + 50, x0 + tw * 0.95, base - (base - tip_y) * 0.4, x0 + tw, base)
        cr.line_to(W + tw, H)
        cr.close_path()
        cr.set_source_rgba(*col[:3], a)
        cr.fill()


def _victory(cr, t, start, cx, cy, seed):
    """A golden sunburst turning slowly, a bright core and twinkling sparkles."""
    _radial(cr, cx, cy, [(0, hexa("#fffbe0")), (0.2, hexa("#ffd84a")), (1, hexa("#ff9a1f"))])
    u = t - start
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(u * 0.35)
    cr.set_source_rgba(1, 0.97, 0.75, 0.45)
    for i in range(20):
        _wedge(cr, 0, 0, i * 2 * math.pi / 20, 0, 1600, 300)
    cr.fill()
    cr.restore()
    _glow(cr, cx, cy, 300, (1, 1, 0.9), 0.9)
    rnd = random.Random(seed * 61 + 2)
    for _ in range(16):
        sx, sy, ss = rnd.uniform(20, W - 20), rnd.uniform(20, H - 20), rnd.uniform(14, 34)
        k = 0.5 + 0.5 * math.sin(u * 8 + sx * 0.1)
        _glow(cr, sx, sy, ss * 1.6, (1, 1, 0.85), 0.4 * k)
        _star4(cr, sx, sy, ss * (0.5 + 0.5 * k), u * 0.8)
        cr.set_source_rgba(1, 1, 1, 0.6 + 0.4 * k)
        cr.fill()


MOODS = {"realisation": _realisation, "dread": _dread, "love": _love, "gloom": _gloom, "rage": _rage,
         "victory": _victory}
_SOUNDS = {"realisation": "m_whoosh", "rage": "m_hit", "love": "m_bond", "victory": "m_bond"}


def emotion_bg(cr, t, start, end, mood="realisation", cx=W / 2, cy=H * 0.42, seed=0, sound=True):
    """A full-frame emotion background from start to end (hard cuts), to draw behind a frozen subject pass:
    comp.backdrop(start=, end=, fn=fx2d_anime.emotion_bg, args=dict(mood="dread")). Moods: realisation (blue,
    sharp radial lines and a flash), dread (dark wavy lines), love (pink, hearts, bokeh), gloom (vertical lines
    hanging from the top), rage (red burst, flames on 2s), victory (golden sunburst, sparkles). (cx, cy) is where
    the subject's head sits: the radial ones centre there."""
    if t < start or t > end:
        return
    if sound and mood in _SOUNDS:
        cue(_SOUNDS[mood], t, start)
    cr.save()
    MOODS[mood](cr, t, start, cx, cy, seed)
    cr.restore()


# ================================================================ split screen (SG7, AB13)
def _divider_pts(y, tilt, seed, jag=22, n=9):
    """A jagged line across the frame at height y, sloping by `tilt` (fraction of the width)."""
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        x = -20 + i * (W + 40) / n
        off = (jag if i % 2 else -jag) * rnd.uniform(0.5, 1.0) if 0 < i < n else 0
        pts.append((x, y + tilt * W * (0.5 - i / n) + off))
    return pts


def split(cr, t, start, end, panels, focus=None, zoom=None, tilt=0.06, slide=0.12, seed=0, sound=True):
    """A split screen of 2-5 horizontal panels (top to bottom) cut by jagged white dividers: the vertical face-off
    and the A/B ending (A above, B below). panels: full-frame pictures, each a cairo ImageSurface or a callable
    draw(cr) painting a 720x1280 frame. focus: one (x, y) per panel, the point of its picture to centre in its
    band (None or omitted = the frame centre); the picture slides vertically to bring it in, as far as it can
    while still covering the band. zoom: one scale per panel (default 1); above 1 the panel is enlarged around its
    focus point, which is then centred in both directions. The panels slide in from alternate sides over `slide` seconds (0 = hard
    cut) and the dividers flash white."""
    if t < start or t > end:
        return
    if sound:
        cue("m_whoosh", t, start)
    n = len(panels)
    focus = [f or (W / 2, H / 2) for f in (focus or [None] * n)]
    zoom = list(zoom or [1.0] * n)
    u = t - start
    bands = [H * (i + 1) / n for i in range(n - 1)]
    divs = [_divider_pts(y, tilt * (1 if i % 2 == 0 else -1), seed * 13 + i) for i, y in enumerate(bands)]
    cr.save()
    cr.set_source_rgba(*INK)
    cr.paint()
    for i, pic in enumerate(panels):
        cr.save()
        top = [(-20, -20), (W + 20, -20)] if i == 0 else divs[i - 1]
        bot = [(W + 20, H + 20), (-20, H + 20)] if i == n - 1 else list(reversed(divs[i]))
        cr.move_to(*top[0])
        for p in top[1:] + bot:
            cr.line_to(*p)
        cr.close_path()
        cr.clip()
        mid = H * (i + 0.5) / n
        lo, hi = H * i / n - 60, H * (i + 1) / n + 60             # the band, with room for the jagged edge
        tx = 0.0                                                  # the picture always covers its band
        ty = min(max(mid - focus[i][1], hi - H), lo) if hi - lo < H else 0.0
        if zoom[i] != 1:
            cr.translate(focus[i][0], focus[i][1])
            tx, ty = W / 2 - focus[i][0], mid - focus[i][1]
        dx = (1 - ease_out(u / slide)) * W * (-1 if i % 2 == 0 else 1) if slide > 0 else 0.0
        cr.translate(tx + dx, ty)
        if zoom[i] != 1:
            cr.scale(zoom[i], zoom[i])
            cr.translate(-focus[i][0], -focus[i][1])
        if isinstance(pic, cairo.ImageSurface):
            cr.scale(W / pic.get_width(), H / pic.get_height())
            cr.set_source_surface(pic, 0, 0)
            cr.paint()
        else:
            pic(cr)
        cr.restore()
    flash = 1 - clamp01((u - slide) / 0.2)
    for pts in divs:
        for lw, col in ((22, INK), (11, WHITE)):
            cr.move_to(*pts[0])
            for p in pts[1:]:
                cr.line_to(*p)
            cr.set_source_rgba(*col)
            cr.set_line_width(lw)
            cr.set_line_join(cairo.LINE_JOIN_MITER)
            cr.stroke()
        if flash > 0:
            for p in pts[1:-1:2]:
                _glow(cr, p[0], p[1], 120, (1, 1, 1), 0.6 * flash)
    cr.restore()


# ================================================================ the observer shake (IM5)
def shake_offset(t, start, dur=0.6, amp=0.30, floor=0.01, seed=0):
    """(dx, dy) in pixels for an observer shake on 2s: about amp x frame width at first, decaying exponentially to
    floor x width by `dur`, then still. Each held pair of frames jumps to the opposite side (mostly up and down,
    with some sideways), as measured in E43 9:36.04-9:36.58."""
    u = t - start
    if u < 0 or u >= dur:
        return 0.0, 0.0
    step = _frame(t, start) // 2
    k = min(1.0, step * 2 / FPS / dur)
    a = amp * (floor / amp) ** k * W
    rnd = random.Random(seed * 7349 + step)
    ang = math.pi / 2 + rnd.uniform(-0.6, 0.6) + (math.pi if step % 2 else 0)
    return a * math.cos(ang), a * math.sin(ang)


def shake(cr, t, start, dur=0.6, amp=0.30, floor=0.01, seed=0):
    """Shake the picture drawn so far (the observer's shot, after the hit): the frame moves by shake_offset and
    the edges it uncovers are filled by stretching the border pixels (they are only on screen for 2 frames).
    Draw it in the "fx" layer before any HUD or captions; lock the camera on reveals and on the final hit."""
    dx, dy = shake_offset(t, start, dur, amp, floor, seed)
    if dx == 0 and dy == 0:
        return
    surf = cr.get_target()
    if not isinstance(surf, cairo.ImageSurface):
        return
    surf.flush()
    copy = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
    c = cairo.Context(copy)
    c.set_source_surface(surf, 0, 0)
    c.paint()
    pat = cairo.SurfacePattern(copy)
    pat.set_extend(cairo.EXTEND_PAD)
    m = cairo.Matrix()
    m.translate(-dx, -dy)
    pat.set_matrix(m)
    cr.save()
    cr.identity_matrix()
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source(pat)
    cr.paint()
    cr.restore()
