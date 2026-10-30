"""Anime effects that channels/monsters/fx2d.py doesn't have, in the same calling style (fn(cr, t, start, ...),
nothing drawn outside the time window, jitter on 2s, VFX moving on 1s):

- beam: a glowing beam (white core, coloured body, wide glow, white streaks racing along it);
- bokeh: soft round glows (pink, blue, white) with twinkling 4-point sparkles around one spot;
- ambient: the anime's ambient layer over a whole shot, slow drifting bokeh and bubbles plus 4-point twinkles;
- burst_bg: full-frame "big moment" backgrounds to put behind a frozen character: "lines" (one-colour radial speed
  lines), "red" (a comic red burst with halftone dots) and "sparkle" (a pastel sparkle field);
- wipe: a shape-wipe transition (iris or organic blob) driven by progress 0..1, revealing the next scene.

    fx2d_extra.beam(cr, t, 1.0, 1.8, 215, 300, 760, 120)      # from the claw to the top-right corner
    fx2d_extra.bokeh(cr, t, 0.0, 3.0, 335, 650)               # dreamy glows around the creature
    fx2d_extra.ambient(cr, t, 0.0)                            # over the whole shot, after the render
    fx2d_extra.burst_bg(cr, t, 4.0, 5.5, "red")               # then draw the frozen character on top
    fx2d_extra.wipe(cr, u, "blob", nxt=next_frame_surface)    # u = 0..1 across the transition

Demo stills: FPS=24 python -m channels.monsters.fx2d_extra  -> out/monsters/tests/fx2d_extra_*.png
"""
import math

import numpy as np

from motion.engine import FPS, H, W, cairo, clamp01, cue, ease_out
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


def _bubble(cr, x, y, r, a):
    """A clear soap/water bubble: a faint tinted body, a thin bright rim and a curved highlight."""
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.05 * a)
    g.add_color_stop_rgba(0.85, 0.75, 0.9, 1, 0.12 * a)
    g.add_color_stop_rgba(1, 0.85, 0.95, 1, 0.5 * a)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, 0.55 * a)
    cr.set_line_width(max(1.0, r * 0.07))
    cr.stroke()
    cr.arc(x, y, r * 0.7, math.pi * 1.1, math.pi * 1.45)
    cr.set_source_rgba(1, 1, 1, 0.85 * a)
    cr.set_line_width(max(1.2, r * 0.13))
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()


def ambient(cr, t, start, end=None, strength=1.0, n_bokeh=9, n_bubbles=6, n_twinkles=7, y_max=0.72 * H,
            keep_clear=None, cols=(WHITE, PINK, BLUE), seed=0):
    """The anime's ambient layer for a whole shot: soft bokeh glows and a few clear bubbles drifting slowly up and
    swaying, with 4-point twinkles that blink on and off in new places. Kept subtle (strength scales it) and above
    y_max so it stays off the captions; keep_clear=(x, y, radius) fades anything that drifts over a face. Positions
    depend only on t, so any frame renders the same on its own."""
    if t < start or (end is not None and t > end + 0.3):
        return
    a = strength * clamp01((t - start) / 0.3) * (1 - clamp01((t - end) / 0.3) if end is not None else 1)
    if a <= 0:
        return
    el = t - start
    r = _rng(seed, 41)
    span = y_max + 160

    def clear(x, y):
        if not keep_clear:
            return 1.0
        kx, ky, kr = keep_clear
        return clamp01((math.hypot(x - kx, y - ky) - kr) / 60)

    def drift(k):
        x0, y0 = r.uniform(-20, W + 20), r.uniform(0, span)
        rise, sway, ph = r.uniform(12, 32), r.uniform(8, 22), r.uniform(0, 6.3)
        y = (y0 - el * rise) % span - 80
        return x0 + sway * math.sin(el * 0.7 + ph), y

    for i in range(n_bokeh):
        x, y = drift(i)
        rad, base = r.uniform(12, 42), r.uniform(0.18, 0.4)
        fade = clamp01((y_max - y) / 120) * clear(x, y)           # dissolve before the caption band
        _disc(cr, x, y, rad, cols[i % len(cols)], a * base * fade * (0.8 + 0.2 * math.sin(el * 1.3 + i)))
    for i in range(n_bubbles):
        x, y = drift(i)
        rad = r.uniform(7, 20)
        _bubble(cr, x, y, rad, a * clamp01((y_max - y) / 120) * clear(x, y))
    for i in range(n_twinkles):
        period, ph = r.uniform(1.3, 2.6), r.uniform(0, 1)
        cyc = el / period + ph
        k = int(math.floor(cyc))
        u = cyc - k
        rr = _rng(seed, 43, i, k)                                 # a new spot every cycle
        x, y = rr.uniform(30, W - 30), rr.uniform(40, y_max - 40)
        size = rr.uniform(9, 22) * max(0.0, math.sin(math.pi * clamp01(u / 0.45))) ** 1.5
        _sparkle(cr, x, y, size, cols[i % len(cols)], a * clear(x, y), rot=rr.uniform(-0.3, 0.3))


def _halftone(cr, cx, cy, col, a, step=26, r_in=0.45, r_out=1.05):
    """Comic halftone dots, growing from nothing near the centre to big at the frame edges."""
    rmax = math.hypot(W, H) / 2
    cr.set_source_rgba(*col[:3], a)
    for j, y in enumerate(range(0, H + step, step)):
        off = step / 2 if j % 2 else 0
        for x in np.arange(off, W + step, step):
            d = math.hypot(x - cx, y - cy) / rmax
            rad = step * 0.48 * clamp01((d - r_in) / (r_out - r_in))
            if rad > 0.6:
                cr.arc(x, y, rad, 0, 2 * math.pi)
                cr.new_sub_path()
    cr.fill()


def _spiky(cr, cx, cy, r_in, r_out, n, rot, seed):
    """Path of a jagged comic starburst."""
    rr = _rng(seed, 51)
    for k in range(2 * n):
        ang = rot + k * math.pi / n
        rad = (r_out * rr.uniform(0.85, 1.15)) if k % 2 == 0 else r_in * rr.uniform(0.9, 1.05)
        (cr.move_to if k == 0 else cr.line_to)(cx + math.cos(ang) * rad, cy + math.sin(ang) * rad)
    cr.close_path()


def burst_bg(cr, t, start, end, style="lines", cx=W / 2, cy=H * 0.45, col=(0.16, 0.36, 0.95), seed=0, sound=True):
    """A full-frame "big moment" background for start..end (hard cuts in and out, like the anime), to draw BEFORE a
    frozen character pose: the character holds still while this keeps moving.
    style "lines": one colour, a bright centre and radial speed lines in a lighter tint, redrawn on 2s;
    style "red": a comic red burst, slowly turning sunburst wedges, a pulsing jagged starburst and halftone dots;
    style "sparkle": a pastel sparkle field with soft light rays, twinkles and bokeh (delight, a win)."""
    if t < start or t > end:
        return
    if sound:
        cue("m_whoosh" if style == "lines" else "m_hit" if style == "red" else "m_bond", t, start)
    el = t - start
    rmax = math.hypot(W, H)
    cr.save()
    if style == "lines":
        g = cairo.RadialGradient(cx, cy, 0, cx, cy, rmax * 0.6)
        light = tuple(c + (1 - c) * 0.55 for c in col)
        g.add_color_stop_rgb(0, *light)
        g.add_color_stop_rgb(0.35, *col)
        g.add_color_stop_rgb(1, *(c * 0.55 for c in col))
        cr.set_source(g)
        cr.paint()
        r = _rng(seed, 61, _twos(t))
        clear = 150
        for _ in range(110):
            ang = r.uniform(0, 2 * math.pi)
            wid = r.uniform(0.003, 0.02)
            r0 = clear * r.uniform(1.0, 2.4)
            cr.move_to(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0)
            cr.line_to(cx + math.cos(ang - wid) * rmax, cy + math.sin(ang - wid) * rmax)
            cr.line_to(cx + math.cos(ang + wid) * rmax, cy + math.sin(ang + wid) * rmax)
            cr.close_path()
            cr.set_source_rgba(*light, r.uniform(0.35, 0.9))
            cr.fill()
        _glow(cr, cx, cy, 260, WHITE, 0.35)
    elif style == "red":
        g = cairo.RadialGradient(cx, cy, 0, cx, cy, rmax * 0.6)
        g.add_color_stop_rgb(0, 1.0, 0.42, 0.25)
        g.add_color_stop_rgb(0.4, 0.92, 0.12, 0.16)
        g.add_color_stop_rgb(1, 0.5, 0.03, 0.08)
        cr.set_source(g)
        cr.paint()
        n, rot = 18, el * 0.25
        for k in range(n):                                        # sunburst wedges
            a0 = rot + k * 2 * math.pi / n
            cr.move_to(cx, cy)
            cr.arc(cx, cy, rmax, a0, a0 + math.pi / n)
            cr.close_path()
        cr.set_source_rgba(1, 0.55, 0.45, 0.22)
        cr.fill()
        _halftone(cr, cx, cy, (0.35, 0.0, 0.05), 0.55)
        pulse = 1 + 0.05 * math.sin(el * 2 * math.pi * 3)
        _spiky(cr, cx, cy, 190 * pulse, 330 * pulse, 14, -el * 0.15, seed)
        cr.set_source_rgba(1, 0.86, 0.3, 1)
        cr.fill_preserve()
        cr.set_source_rgba(0.25, 0.02, 0.05, 1)
        cr.set_line_width(8)
        cr.set_line_join(cairo.LINE_JOIN_MITER)
        cr.stroke()
        _spiky(cr, cx, cy, 120 * pulse, 220 * pulse, 14, -el * 0.15 + 0.11, seed + 1)
        cr.set_source_rgba(1, 1, 0.9, 1)
        cr.fill()
    else:                                                         # "sparkle"
        g = cairo.LinearGradient(0, 0, W * 0.4, H)
        g.add_color_stop_rgb(0, 1.0, 0.78, 0.9)
        g.add_color_stop_rgb(0.5, 0.86, 0.78, 1.0)
        g.add_color_stop_rgb(1, 0.66, 0.84, 1.0)
        cr.set_source(g)
        cr.paint()
        for k in range(12):                                       # soft light rays turning slowly
            a0 = el * 0.12 + k * 2 * math.pi / 12
            cr.move_to(cx, cy)
            cr.arc(cx, cy, rmax, a0, a0 + 0.12)
            cr.close_path()
        cr.set_source_rgba(1, 1, 1, 0.22)
        cr.fill()
        _glow(cr, cx, cy, 340, WHITE, 0.6)
        r = _rng(seed, 71)
        for i in range(26):
            x, y = r.uniform(0, W), r.uniform(0, H)
            period, ph = r.uniform(0.8, 1.6), r.uniform(0, 1)
            u = (el / period + ph) % 1.0
            _sparkle(cr, x, y, r.uniform(12, 34) * math.sin(math.pi * u) ** 1.5, (WHITE, PINK, BLUE)[i % 3], 1.0,
                     rot=el * 0.5)
        for i in range(14):
            x, y = r.uniform(0, W), (r.uniform(0, H) - el * r.uniform(20, 50)) % H
            _disc(cr, x, y, r.uniform(14, 46), (WHITE, PINK, BLUE)[i % 3], r.uniform(0.3, 0.55))
    cr.restore()


def _blob(cr, cx, cy, R, wob, seed):
    """Path of an organic blob of mean radius R (three wobbling lobes)."""
    rr = _rng(seed, 81)
    terms = [(k, rr.uniform(0.06, 0.12), rr.uniform(0, 6.3)) for k in (3, 5, 7)]
    n = 96
    for j in range(n + 1):
        th = 2 * math.pi * j / n
        f = 1 + sum(amp * math.sin(k * th + ph + wob * (0.6 + 0.2 * k)) for k, amp, ph in terms)
        (cr.move_to if j == 0 else cr.line_to)(cx + R * f * math.cos(th), cy + R * f * math.sin(th))
    cr.close_path()


def wipe(cr, u, shape="iris", nxt=None, fill=WHITE, cx=W / 2, cy=H * 0.45, edge=(1.0, 0.84, 0.35), mode="open",
         seed=0):
    """A shape-wipe transition at progress u (0..1, eased here): the shape grows from (cx, cy) and shows the next
    scene inside it (mode "open"), or shrinks and leaves the next scene outside (mode "close", an iris-out). nxt is
    an ImageSurface or a function nxt(cr) that draws the next scene; None fills with `fill` (e.g. white for the
    Earth -> white cut). shape: "iris" (a circle) or "blob" (an organic three-lobed blob that wobbles as it grows).
    A bright edge ring rides the boundary. Draw it after the outgoing frame."""
    if u <= 0:
        return
    k = clamp01(u)
    e = k * k * (3 - 2 * k)                                       # smoothstep
    far = max(math.hypot(px - cx, py - cy) for px in (0, W) for py in (0, H))
    reach = far * (1.6 if shape == "blob" else 1.02)              # blob dips (up to 36%) need extra reach
    R = reach * (e if mode == "open" else 1 - e)

    def path():
        if shape == "blob":
            _blob(cr, cx, cy, max(R, 0.1), k * 3.0, seed)
        else:
            cr.arc(cx, cy, max(R, 0.1), 0, 2 * math.pi)

    cr.save()
    if mode == "open" and e >= 1:
        pass                                                       # fully open: the next scene everywhere
    elif mode == "open":
        path()
    else:                                                          # everything outside the shape
        cr.rectangle(0, 0, W, H)
        path()
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    if not (mode == "open" and e >= 1):
        cr.clip()
    if isinstance(nxt, cairo.ImageSurface):
        cr.set_source_surface(nxt, 0, 0)
        cr.paint()
    elif callable(nxt):
        nxt(cr)
    else:
        cr.set_source_rgba(*fill[:3], 1)
        cr.paint()
    cr.restore()
    if 0 < R < reach and edge is not None:
        path()
        cr.set_source_rgba(0.08, 0.06, 0.12, 0.9)
        cr.set_line_width(14)
        cr.stroke()
        path()
        cr.set_source_rgba(*edge[:3], 1)
        cr.set_line_width(8)
        cr.stroke()


def wipe_at(cr, t, start, dur=0.5, **kw):
    """wipe() timed in seconds: progress runs 0..1 over [start, start + dur]; after that the next scene is shown in
    full (mode "open") until the caller stops calling it."""
    if t < start:
        return
    cue("m_whoosh", t, start)
    wipe(cr, (t - start) / dur, **kw)


if __name__ == "__main__":
    import os

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = os.path.join(root, "out/monsters/tests")
    v3 = cairo.ImageSurface.create_from_png(os.path.join(root, "out/monsters/style_frame_anime_v3.png"))
    v2 = cairo.ImageSurface.create_from_png(os.path.join(root, "out/monsters/style_frame_anime_v2.png"))

    def still(name, draw, base=v3):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        cr = cairo.Context(surf)
        cr.set_source_surface(base, 0, 0)
        cr.paint()
        draw(cr)
        path = os.path.join(out, f"fx2d_extra_{name}.png")
        surf.write_to_png(path)
        print(f"wrote {path} ({os.path.getsize(path) / 1e6:.2f} MB)")

    still("beam_bokeh", lambda cr: (bokeh(cr, 1.0, 0.0, 3.0, 335, 650, spread=230),
                                    beam(cr, 0.5, 0.0, 1.0, 215, 300, 760, 120, 60)), v2)
    still("ambient", lambda cr: ambient(cr, 2.0, 0.0, keep_clear=(335, 640, 150)))
    still("burst_lines", lambda cr: burst_bg(cr, 0.3, 0.0, 2.0, "lines"))
    still("burst_red", lambda cr: burst_bg(cr, 0.3, 0.0, 2.0, "red"))
    still("burst_sparkle", lambda cr: burst_bg(cr, 0.6, 0.0, 2.0, "sparkle"))
    still("wipe_iris", lambda cr: wipe(cr, 0.45, "iris", nxt=None))
    still("wipe_blob", lambda cr: wipe(cr, 0.45, "blob", nxt=lambda c: burst_bg(c, 0.3, 0.0, 2.0, "sparkle", sound=False)))
