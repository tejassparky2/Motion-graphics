"""Two anime effects that channels/monsters/fx2d.py doesn't have yet: a glowing beam (white core, coloured body,
wide glow, white streaks racing along it) and soft round bokeh glows (pink, blue, white) with twinkling 4-point
sparkles. Same calling style as fx2d: fn(cr, t, start, ...), nothing drawn outside the time window, jitter on 2s.

    fx2d_extra.beam(cr, t, 1.0, 1.8, 215, 300, 760, 120)      # from the claw to the top-right corner
    fx2d_extra.bokeh(cr, t, 0.0, 3.0, 335, 650)               # dreamy glows around the creature

Demo still: FPS=24 python -m channels.monsters.fx2d_extra  -> out/monsters/tests/fx2d_extra_beam_bokeh.png
"""
import math

import numpy as np

from motion.engine import FPS, cairo, clamp01, cue, ease_out
from motion.polish import rrect
from channels.monsters import sfx as _sfx  # noqa: F401  (registers the m_* sounds the cues name)

WHITE = (1, 1, 1)
PINK = (1.00, 0.55, 0.78)
BLUE = (0.45, 0.70, 1.00)


def _twos(t):
    return int(math.floor(t * FPS / 2 + 1e-6))


def _rng(*key):
    return np.random.default_rng([abs(int(k)) for k in key])


def _glow(cr, x, y, r, col, a=1.0):
    if r <= 0 or a <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col[:3], a)
    g.add_color_stop_rgba(0.3, *col[:3], a * 0.4)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def _star4(cr, x, y, r, rot=0.0, waist=0.16):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    pts = [(math.cos(k * math.pi / 2) * r, math.sin(k * math.pi / 2) * r) for k in range(4)]
    cr.move_to(*pts[0])
    for k in range(4):
        mid = (k + 0.5) * math.pi / 2
        cx, cy = math.cos(mid) * r * waist, math.sin(mid) * r * waist
        cr.curve_to(cx, cy, cx, cy, *pts[(k + 1) % 4])
    cr.close_path()
    cr.restore()


def _sparkle(cr, x, y, r, col=WHITE, a=1.0, rot=0.0):
    if r <= 0.5 or a <= 0:
        return
    _glow(cr, x, y, r * 2.2, col, 0.55 * a)
    _star4(cr, x, y, r, rot)
    cr.set_source_rgba(*col[:3], 0.9 * a)
    cr.fill()
    _star4(cr, x, y, r * 0.62, rot)
    cr.set_source_rgba(1, 1, 1, a)
    cr.fill()


def _disc(cr, x, y, r, col, a):
    """One bokeh disc: flat, soft-edged, with a slightly brighter rim like a lens highlight."""
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col[:3], a * 0.75)
    g.add_color_stop_rgba(0.75, *col[:3], a * 0.6)
    g.add_color_stop_rgba(0.9, *col[:3], a * 0.85)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def beam(cr, t, start, end, x0, y0, x1, y1, width=56, col=(0.45, 0.85, 1.0), seed=0, sound=True):
    """A glowing beam from (x0, y0) to (x1, y1): it shoots out in 0.12 s, flickers on 2s and thins out over 0.2 s
    after `end`. Layers: wide coloured glow, coloured body, white core, white streaks racing along it, a flare at
    the source and a hot spot where it lands."""
    if t < start or t > end + 0.2:
        return
    if sound:
        cue("m_shockwave", t, start)
    grow = ease_out((t - start) / 0.12)
    thin = 1 - clamp01((t - end) / 0.2)
    r = _rng(seed, _twos(t))
    wd = width * thin * (0.92 + 0.12 * r.random())
    L = math.hypot(x1 - x0, y1 - y0) * grow
    if L < 1 or wd < 0.5:
        return
    cr.save()
    cr.translate(x0, y0)
    cr.rotate(math.atan2(y1 - y0, x1 - x0))

    def band(w, stops):
        g = cairo.LinearGradient(0, -w / 2, 0, w / 2)
        for o, c in stops:
            g.add_color_stop_rgba(o, *c)
        cr.set_source(g)
        rrect(cr, -w / 4, -w / 2, L + w / 2, w, w / 2)
        cr.fill()

    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    band(wd * 3.2, [(0, (*col, 0)), (0.5, (*col, 0.45)), (1, (*col, 0))])
    cr.restore()
    band(wd, [(0, (*col, 0)), (0.2, (*col, 0.95)), (0.5, (*col, 1)), (0.8, (*col, 0.95)), (1, (*col, 0))])
    band(wd * 0.45, [(0, (1, 1, 1, 0)), (0.3, (1, 1, 1, 1)), (0.7, (1, 1, 1, 1)), (1, (1, 1, 1, 0))])
    rs = _rng(seed, 3)
    for _ in range(26):
        off = rs.uniform(-0.45, 0.45) * wd
        ln = rs.uniform(0.08, 0.3) * L
        sp = rs.uniform(900, 1600)
        xs = ((rs.uniform(0, L + ln) + (t - start) * sp) % (L + ln)) - ln
        cr.move_to(max(0, xs), off)
        cr.line_to(min(L, xs + ln), off)
        cr.set_line_width(rs.uniform(1.2, 3.5))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_source_rgba(1, 1, 1, rs.uniform(0.35, 0.8))
        cr.stroke()
    cr.restore()
    _glow(cr, x0, y0, wd * 1.8, col, 0.8 * thin)
    _sparkle(cr, x0, y0, wd * 0.9, col, thin, rot=0.785 if _twos(t) % 2 else 0)
    tx, ty = x0 + (x1 - x0) * grow, y0 + (y1 - y0) * grow
    _glow(cr, tx, ty, wd * 2.2, col, 0.9 * thin)
    _glow(cr, tx, ty, wd * 0.9, WHITE, 0.8 * thin)


def bokeh(cr, t, start, end, x, y, spread=200, n=10, stars=12, cols=(WHITE, PINK, BLUE), seed=0):
    """Soft round bokeh glows drifting slowly upward in a ring around (x, y) (kept off the middle, so they don't
    sit on a face), with twinkling 4-point sparkles in between. Fades in over 0.15 s and out 0.3 s after `end`."""
    if t < start or t > end + 0.3:
        return
    a = clamp01((t - start) / 0.15) * (1 - clamp01((t - end) / 0.3))
    r = _rng(seed, 11)
    el = t - start
    for i in range(n):
        ang, d = r.uniform(0, 2 * math.pi), spread * math.sqrt(r.uniform(0.45, 1.4))
        bx, by = x + math.cos(ang) * d, y + math.sin(ang) * d * 0.8 - el * r.uniform(8, 25)
        _disc(cr, bx, by, r.uniform(14, 40), cols[i % len(cols)],
              a * r.uniform(0.35, 0.6) * (0.75 + 0.25 * math.sin(el * r.uniform(1.5, 3) + i)))
    for i in range(stars):
        ang, d = r.uniform(0, 2 * math.pi), spread * math.sqrt(r.uniform(0.0, 1.0))
        rate, ph = r.uniform(0.9, 1.8), r.uniform(0, 1)
        u = (el * rate + ph) % 1.0
        _sparkle(cr, x + math.cos(ang) * d, y + math.sin(ang) * d * 0.8, r.uniform(16, 36) * math.sin(math.pi * u) ** 1.5,
                 cols[i % len(cols)], a, rot=r.uniform(-0.2, 0.2) + el * 0.4)


if __name__ == "__main__":
    import os
    import sys

    from motion.engine import H, W
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bg = cairo.ImageSurface.create_from_png(os.path.join(root, "out/monsters/style_frame_anime_v2.png"))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    cr.set_source_surface(bg, 0, 0)
    cr.paint()
    bokeh(cr, 1.0, 0.0, 3.0, 335, 650, spread=230)
    beam(cr, 0.5, 0.0, 1.0, 215, 300, 760, 120, 60)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "out/monsters/tests/fx2d_extra_beam_bokeh.png")
    surf.write_to_png(out)
    print("wrote", out)
