"""2D overlays for the monster series ("Cute Things Kill Here"): anime effects and the game HUD, drawn with pycairo
on top of rendered 720x1280 frames.

Every element is fn(cr, t, start, ...): t is the shot time in seconds and start is when the element begins, so a
shot composites them frame by frame after drawing its rendered PNG:

    img = cairo.ImageSurface.create_from_png(frame_png)
    cr = cairo.Context(img)
    fx2d.status_bar(cr, t, 0.0, hits=[(2.1, 0.55)])
    fx2d.sparkles(cr, t, 3.0, 360, 640)

Outside its time window an element draws nothing. Sound cues (motion.engine.cue) use the "m_" names that
channels/monsters/sfx.py registers. Effects that jitter do it on 2s (new random lines every second frame), like the
characters; set FPS=24 in the environment before importing (motion.engine reads it).

Layout: the HUD stays above CAPTION_BAND (captions sit at ~71% height, hud2d.captions y=905) and never reaches
SAFE_BOTTOM (the Shorts UI covers the bottom 25%); channels/monsters/test_fx2d.py checks every HUD element.
Effects go wherever the caller puts them. The impact frame and speed lines are full-frame backgrounds: draw them
before the HUD and the captions.

The HUD is our own design (indigo panels with cut corners, mint edges, a five-pip threat meter): no Pokedex look,
no ball icon, no copied fonts or icons. Fonts are the repo's OFL fonts (Fredoka, Luckiest Guy).
"""
import math
import random

import numpy as np
from scipy.ndimage import gaussian_filter

from motion.engine import FPS, H, W, back_out, cairo, clamp01, cue, ease_out
from motion.polish import rrect, text_path, text_width

ROUND = "Fredoka"
DISPLAY = "Luckiest Guy"

SAFE_BOTTOM = int(H * 0.75)          # 960: the Shorts UI covers everything below this
CAPTION_BAND = (845, 930)            # hud2d.captions (baseline 905, size 52) with its outline and shadow
HUD_TOP = 96                         # below the Shorts top bar (back arrow, search)


def hexa(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


WHITE = (1, 1, 1, 1)
INK = (0.06, 0.05, 0.10, 1)
RED = hexa("#ff3b30")                # the channel's highlight red (hud2d.RED)
GREEN = hexa("#3ee07a")
AMBER = hexa("#ffb02e")
YELLOW = hexa("#ffd23f")
MINT = hexa("#5ef2c2")
PANEL = (0.07, 0.08, 0.20, 0.88)
TRACK = (0.02, 0.02, 0.07, 0.9)


# ---------------------------------------------------------------- helpers
def _mix(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(4))


def _fade(t, start, end, fin=0.0, fout=0.2):
    """Alpha of an element shown from start to end (end None = until the shot ends); 0 outside."""
    if t < start or (end is not None and t > end + fout):
        return 0.0
    a = clamp01((t - start) / fin) if fin > 0 else 1.0
    if end is not None and t > end:
        a *= 1 - clamp01((t - end) / fout)
    return a


def _twos(t):
    """Changes every second frame (anime timing on 2s)."""
    return int(math.floor(t * FPS + 1e-6)) // 2


def _text(cr, s, x, y, size, col, font=ROUND, align="left", outline=None, ow=0.0, shadow=0.0):
    if shadow:
        text_path(cr, s, x + size * 0.03, y + size * 0.07, size, font, align)
        cr.set_source_rgba(0, 0, 0, shadow * col[3])
        if outline:
            cr.set_line_width(ow)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke_preserve()
        cr.fill()
    if outline:
        text_path(cr, s, x, y, size, font, align)
        cr.set_source_rgba(*outline[:3], outline[3] * col[3])
        cr.set_line_width(ow)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(*col)
    cr.fill()


def _fit(cr, s, size, max_w, font=ROUND):
    return min(size, size * max_w / max(1.0, text_width(cr, s, size, font)))


def _chamfer(cr, x, y, w, h, c, flip=False):
    """A panel with two cut corners (top-left and bottom-right, or the mirror image): the HUD's own shape."""
    cr.new_sub_path()
    if not flip:
        pts = [(x + c, y), (x + w, y), (x + w, y + h - c), (x + w - c, y + h), (x, y + h), (x, y + c)]
    else:
        pts = [(x, y), (x + w - c, y), (x + w, y + c), (x + w, y + h), (x + c, y + h), (x, y + h - c)]
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()


def _panel(cr, x, y, w, h, edge=MINT, c=14, flip=False, a=1.0):
    _chamfer(cr, x, y, w, h, c, flip)
    cr.set_source_rgba(*PANEL[:3], PANEL[3] * a)
    cr.fill_preserve()
    cr.set_source_rgba(*edge[:3], 0.95 * a)
    cr.set_line_width(3)
    cr.set_line_join(cairo.LINE_JOIN_MITER)
    cr.stroke()
    _chamfer(cr, x + 5, y + 5, w - 10, h - 10, max(2, c - 4), flip)     # a faint inner line, like a game frame
    cr.set_source_rgba(*edge[:3], 0.18 * a)
    cr.set_line_width(1.5)
    cr.stroke()


def _glow(cr, x, y, r, col, a=1.0):
    if r <= 0 or a <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col[:3], a)
    g.add_color_stop_rgba(0.35, *col[:3], a * 0.35)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def _star4(cr, x, y, r, rot=0.0, waist=0.2):
    """A 4-point sparkle star: long points joined by curves pulled in toward the centre."""
    cr.new_sub_path()
    for k in range(4):
        a0 = rot + k * math.pi / 2
        a1 = a0 + math.pi / 2
        p0 = (x + r * math.cos(a0), y + r * math.sin(a0))
        p1 = (x + r * math.cos(a1), y + r * math.sin(a1))
        m = (x + r * waist * math.cos(a0 + math.pi / 4), y + r * waist * math.sin(a0 + math.pi / 4))
        if k == 0:
            cr.move_to(*p0)
        cr.curve_to(m[0], m[1], m[0], m[1], *p1)
    cr.close_path()


def _wedge(cr, cx, cy, ang, r0, r1, w):
    """A thin spike from radius r0 (a point) out to radius r1 (width w): one speed or impact line."""
    ca, sa = math.cos(ang), math.sin(ang)
    cr.move_to(cx + ca * r0, cy + sa * r0)
    cr.line_to(cx + ca * r1 - sa * w / 2, cy + sa * r1 + ca * w / 2)
    cr.line_to(cx + ca * r1 + sa * w / 2, cy + sa * r1 - ca * w / 2)
    cr.close_path()


# ================================================================ anime effects
def _otsu(lum):
    """The grey level that best splits an image into two tones (Otsu's method)."""
    hist = np.bincount(np.clip(lum, 0, 255).astype(np.uint8).ravel(), minlength=256).astype(np.float64)
    p = hist / hist.sum()
    w0 = np.cumsum(p)
    m0 = np.cumsum(p * np.arange(256))
    between = (m0[-1] * w0 - m0) ** 2 / np.maximum(w0 * (1 - w0), 1e-9)
    return float(np.argmax(between))


def impact_frame(cr, t, start, cx=W / 2, cy=H * 0.5, frames=3, clear=230, seed=0):
    """2-3 frames of high-contrast black/white with radial lines (the anime impact flash).

    Frames alternate inverted / normal (white subject on black, then black on white). It reads the pixels already
    drawn on the context's target, so call it on the frame's own context after the render and before the HUD.
    `clear` is the radius around (cx, cy) the lines leave open."""
    k = int(math.floor((t - start) * FPS + 1e-6))
    if not 0 <= k < frames:
        return
    cue("m_hit", t, start)
    invert = k % 2 == 0
    surf = cr.get_target()
    if isinstance(surf, cairo.ImageSurface) and surf.get_format() in (cairo.FORMAT_ARGB32, cairo.FORMAT_RGB24):
        surf.flush()
        w, h = surf.get_width(), surf.get_height()
        a = np.ndarray((h, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :w]
        lum = gaussian_filter((0.114 * a[..., 0] + 0.587 * a[..., 1] + 0.299 * a[..., 2]).astype(np.float32), 1.5)
        mid = _otsu(lum[::3, ::3])                             # splits at the valley, so flat areas stay one tone
        v = np.clip((lum - mid) * 0.25 + 0.5, 0, 1)            # a steep curve: pure black and white
        if invert:
            v = 1 - v
        a[..., :3] = (v * 255).astype(np.uint8)[..., None]
        a[..., 3] = 255
        surf.mark_dirty()
    else:                                                      # not an image: plain inversion
        cr.save()
        cr.set_operator(cairo.OPERATOR_DIFFERENCE)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
        cr.restore()
    rnd = random.Random(seed * 7919 + k)
    line = (1, 1, 1) if invert else INK[:3]
    cr.save()
    cr.set_source_rgb(*line)
    for i in range(56):
        ang = (i + rnd.uniform(-0.4, 0.4)) * 2 * math.pi / 56
        _wedge(cr, cx, cy, ang, clear * rnd.uniform(0.85, 1.5), 1600, rnd.uniform(6, 26))
    cr.fill()
    cr.restore()


def speed_lines(cr, t, start, end=None, mode="radial", cx=W / 2, cy=H * 0.45, cols=("#ffe36e", "#ff7a2f"),
                bg=True, n=80, clear=0.22, seed=0):
    """Anime speed lines: mode "radial" (focus lines around cx, cy) or "horizontal" (streaks racing sideways).

    bg=True paints a colour gradient behind them (the action background: cols[0] in the middle, cols[1] at the
    edges); bg=False draws only the lines over the render. clear = open radius as a fraction of the frame height."""
    a = _fade(t, start, end, 0.05, 0.15)
    if a <= 0:
        return
    c0, c1 = hexa(cols[0]), hexa(cols[1])
    cr.save()
    cr.push_group()
    if bg:
        if mode == "radial":
            g = cairo.RadialGradient(cx, cy, 0, cx, cy, H * 0.8)
        else:
            g = cairo.LinearGradient(0, 0, 0, H)
            g.add_color_stop_rgba(0, *c1)
        g.add_color_stop_rgba(0 if mode == "radial" else 0.5, *c0)
        g.add_color_stop_rgba(1, *c1)
        cr.set_source(g)
        cr.paint()
    rnd = random.Random(seed * 104729 + _twos(t - start))
    if mode == "radial":
        for i in range(n):
            ang = rnd.uniform(0, 2 * math.pi)
            r0 = H * clear * rnd.uniform(0.85, 1.6)
            cr.set_source_rgba(1, 1, 1, rnd.uniform(0.55, 0.95))
            _wedge(cr, cx, cy, ang, r0, 1500, rnd.uniform(3, 14))
            cr.fill()
    else:
        speed = 2600.0
        for i in range(n):
            y = rnd.uniform(0, H)
            ln = rnd.uniform(160, 620)
            th = rnd.uniform(2, 9)
            x = (rnd.uniform(0, W + ln) - (t - start) * speed * rnd.uniform(0.7, 1.3)) % (W + ln * 2) - ln
            cr.move_to(x, y)
            cr.curve_to(x + ln * 0.3, y - th, x + ln * 0.7, y - th, x + ln, y)
            cr.curve_to(x + ln * 0.7, y + th, x + ln * 0.3, y + th, x, y)
            cr.set_source_rgba(1, 1, 1, rnd.uniform(0.5, 0.9))
            cr.fill()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def sparkle(cr, t, start, x, y, size=40, col=YELLOW, life=1.1, phase=0.0):
    """One 4-point sparkle star: pops in with an overshoot, twinkles (pulses and turns), then shrinks away."""
    u = t - start
    if u < 0 or u > life:
        return
    s = back_out(u / 0.18, 2.6) * (1 + 0.22 * math.sin(u * 18 + phase))
    s *= 1 - clamp01((u - life + 0.3) / 0.3) ** 2
    if s <= 0.01:
        return
    r = size * s
    rot = 0.25 * math.sin(u * 5 + phase)
    _glow(cr, x, y, r * 1.6, col, 0.55)
    _star4(cr, x, y, r, rot)
    cr.set_source_rgba(*col[:3], 1)
    cr.fill()
    _star4(cr, x, y, r * 0.62, rot, 0.16)
    cr.set_source_rgba(1, 1, 1, 1)
    cr.fill()
    _star4(cr, x, y, r * 0.55, rot + math.pi / 4, 0.12)      # a smaller cross-twinkle on the diagonals
    cr.set_source_rgba(1, 1, 1, 0.7 * (0.5 + 0.5 * math.sin(u * 22 + phase)))
    cr.fill()


def sparkles(cr, t, start, x, y, n=7, radius=130, size=34, cols=(YELLOW, WHITE, MINT), life=1.1, seed=0):
    """A spray of sparkle stars around (x, y), popping in one after another."""
    rnd = random.Random(seed)
    for i in range(n):
        ang = rnd.uniform(0, 2 * math.pi)
        d = radius * rnd.uniform(0.35, 1.0)
        delay = rnd.uniform(0, 0.35)
        out = ease_out((t - start - delay) / 0.4) * 0.25 * radius       # they drift outward a little
        sparkle(cr, t, start + delay, x + math.cos(ang) * (d + out), y + math.sin(ang) * (d + out),
                size * rnd.uniform(0.55, 1.15), cols[i % len(cols)], life * rnd.uniform(0.8, 1.1), rnd.uniform(0, 6))


def glow_burst(cr, t, start, x, y, r=260, col=YELLOW, dur=0.7, rays=14, seed=0):
    """A bright flash that blooms out from (x, y) with a ring of light rays, then fades."""
    u = (t - start) / dur
    if u < 0 or u > 1:
        return
    e = ease_out(u)
    f = (1 - u) ** 1.5
    _glow(cr, x, y, r * (0.45 + 0.75 * e), col, 0.9 * f)
    _glow(cr, x, y, r * 0.35 * (1 - u * 0.5), (1, 1, 1), f)
    rnd = random.Random(seed)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(rays):
        ang = i * 2 * math.pi / rays + rnd.uniform(-0.12, 0.12) + u * 0.4
        ln = r * (0.5 + 0.7 * e) * rnd.uniform(0.7, 1.2)
        g = cairo.RadialGradient(x, y, 0, x, y, ln)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.9 * f)
        g.add_color_stop_rgba(1, *col[:3], 0)
        cr.set_source(g)
        _wedge(cr, x, y, ang, 0, ln, r * 0.09)
        cr.fill()
    cr.restore()


def shockwave(cr, t, start, x, y, r=300, col=WHITE, rings=2, squash=1.0, dur=0.55, lw=16, sound=True):
    """Accent rings expanding from (x, y). squash < 1 lays them flat on the ground (0.3 reads as a floor ring)."""
    u0 = t - start
    if u0 < 0 or u0 > dur + 0.12 * rings:
        return
    if sound:
        cue("m_shockwave", t, start)
    for i in range(rings):
        u = (u0 - i * 0.12) / dur
        if not 0 <= u <= 1:
            continue
        rr = r * (0.15 + 0.85 * ease_out(u)) * (1 - 0.25 * i)
        f = 1 - u
        for width, c, a in ((lw * f * 2.2, col, 0.25), (lw * f, col, 0.95), (lw * f * 0.35, (1, 1, 1), 1.0)):
            cr.save()
            cr.translate(x, y)
            cr.scale(1, squash)
            cr.arc(0, 0, rr, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(*c[:3], a * f)
            cr.set_line_width(max(0.5, width))
            cr.stroke()


def _cloud(cr, x, y, r, seed):
    rnd = random.Random(seed)
    cr.new_sub_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    for k in range(4):
        ang = math.pi * (0.9 + 0.4 * k) + rnd.uniform(-0.2, 0.2)
        rr = r * rnd.uniform(0.55, 0.75)
        cr.new_sub_path()
        cr.arc(x + math.cos(ang) * r * 0.75, y + math.sin(ang) * r * 0.6, rr, 0, 2 * math.pi)


def dust_puffs(cr, t, start, x, y, n=6, spread=170, size=44, col=hexa("#f4ead6"), dur=0.9, seed=0):
    """Cel-shaded dust clouds kicked out sideways along the ground at (x, y) (a landing, a skid, a stomp)."""
    u = (t - start) / dur
    if u < 0 or u > 1:
        return
    rnd = random.Random(seed)
    shade = _mix(col, (0.55, 0.45, 0.42, 1), 0.38)
    line = _mix(col, (0.25, 0.18, 0.15, 1), 0.65)
    e = ease_out(u)
    fade = 1 - clamp01((u - 0.6) / 0.4)
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        ang = rnd.uniform(0.05, 0.6)
        d = spread * rnd.uniform(0.55, 1.1) * e
        px = x + side * math.cos(ang) * d
        py = y - math.sin(ang) * d * 0.45 - 30 * u
        r = size * rnd.uniform(0.7, 1.1) * (0.35 + 0.75 * e) * (1 - 0.5 * u ** 3)
        sd = seed * 31 + i
        cr.save()
        cr.push_group()
        _cloud(cr, px, py, r, sd)                              # outline first, so the fills hide the inner seams
        cr.set_source_rgba(*line)
        cr.set_line_width(6)
        cr.stroke_preserve()
        cr.set_source_rgba(*shade)
        cr.fill()
        _cloud(cr, px, py, r, sd)                              # the lit part: the same cloud nudged up and left
        cr.clip()
        _cloud(cr, px - r * 0.22, py - r * 0.3, r * 0.95, sd)
        cr.set_source_rgba(*col)
        cr.fill()
        cr.reset_clip()
        cr.pop_group_to_source()
        cr.paint_with_alpha(fade)
        cr.restore()


def surprise(cr, t, start, x, y, size=110, col=RED, end=None):
    """The "!" surprise mark above a head (x, y = bottom of the mark): jumps up, settles, with three tick lines."""
    if end is None:
        end = start + 1.0
    a = _fade(t, start, end, 0.0, 0.15)
    if a <= 0:
        return
    u = t - start
    s = max(0.01, back_out(u / 0.2, 3.0))
    hop = (1 - ease_out(u / 0.18)) * size * 0.35
    cr.save()
    cr.push_group()
    cr.translate(x, y + hop)
    cr.rotate(0.12 * math.sin(u * 14) * (1 - clamp01(u / 0.5)))
    cr.scale(s, s)
    bw0, bw1, bh = size * 0.36, size * 0.2, size * 0.62
    top = -size
    bar = [(-bw0 / 2, top), (bw0 / 2, top), (bw1 / 2, top + bh), (-bw1 / 2, top + bh)]
    for lw, c in ((size * 0.11, INK), (0, col)):
        cr.move_to(*bar[0])
        for p in bar[1:]:
            cr.line_to(*p)
        cr.close_path()
        cr.new_sub_path()
        cr.arc(0, -size * 0.13, size * 0.12, 0, 2 * math.pi)
        cr.set_source_rgba(*c)
        if lw:
            cr.set_line_width(lw)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke_preserve()
        cr.fill()
    cr.move_to(-bw0 * 0.22, top + size * 0.08)                 # a highlight stripe
    cr.line_to(-bw1 * 0.15, top + bh * 0.7)
    cr.set_source_rgba(1, 1, 1, 0.6)
    cr.set_line_width(size * 0.05)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()
    k = ease_out((u - 0.05) / 0.15)                            # tick lines fanning out from the top
    for ang in (-2.35, -1.95, -1.19, -0.79):
        r0, r1 = size * 0.55, size * (0.55 + 0.3 * k)
        cx, cy = 0, top + size * 0.15
        cr.move_to(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0)
        cr.line_to(cx + math.cos(ang) * r1, cy + math.sin(ang) * r1)
    cr.set_source_rgba(*INK)
    cr.set_line_width(size * 0.07)
    cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


# ================================================================ game HUD
def _hp_col(f):
    if f > 0.5:
        return _mix(AMBER, GREEN, clamp01((f - 0.5) / 0.15))
    return _mix(RED, AMBER, clamp01((f - 0.2) / 0.15))


def _hp_at(t, hp, hits):
    """Shown HP, the trailing damage ghost, how hard the bar shakes and how bright it flashes at time t."""
    cur = ghost = hp
    shake = flash = 0.0
    for at, new in sorted(hits):
        if t < at:
            break
        d = t - at
        cur = cur + (new - cur) * ease_out(d / 0.25)
        ghost = ghost + (new - ghost) * ease_out((d - 0.45) / 0.5)
        shake = max(shake, 1 - d / 0.35)
        flash = max(flash, 1 - d / 0.15)
        if d > 1.0:
            cur = ghost = new
    return clamp01(cur), clamp01(max(ghost, cur)), max(0.0, shake), max(0.0, flash)


def status_bar(cr, t, start, name="KAI", level=1, hp=1.0, hits=(), max_hp=20, end=None, x=24, y=HUD_TOP, w=330):
    """The hero's status: "KAI · LV 1" over an HP bar that runs green, amber, red.

    hits = [(time, new_hp_fraction)]: at each the bar drops with a shake and a white flash, a pale damage ghost
    drains after it, and the number ticks down. Below 20% the bar blinks."""
    a = _fade(t, start, end, 0.0, 0.25)
    if a <= 0:
        return
    slide = (1 - ease_out((t - start) / 0.3)) * -(w + x + 20)
    cur, ghost, shake, flash = _hp_at(t, hp, hits)
    jx = jy = 0.0
    if shake > 0:
        rnd = random.Random(_twos(t))
        jx, jy = rnd.uniform(-7, 7) * shake, rnd.uniform(-5, 5) * shake
    h = 84
    cr.save()
    cr.push_group()
    cr.translate(x + slide + jx, y + jy)
    _panel(cr, 0, 0, w, h, MINT if cur > 0.2 else RED)
    _text(cr, name, 18, 36, 30, WHITE, ROUND, shadow=0.4)
    nw = text_width(cr, name, 30, ROUND)
    _text(cr, f"·  LV {level}", 18 + nw + 12, 36, 22, MINT, ROUND)
    _text(cr, f"{round(cur * max_hp)}/{max_hp}", w - 18, 36, 22, (1, 1, 1, 0.85), ROUND, "right")
    bx, by, bw, bh = 56, 52, w - 74, 16
    _text(cr, "HP", 18, by + 15, 19, YELLOW, ROUND)
    rrect(cr, bx, by, bw, bh, bh / 2)
    cr.set_source_rgba(*TRACK)
    cr.fill()
    if ghost > cur:
        rrect(cr, bx, by, bw * ghost, bh, bh / 2)
        cr.set_source_rgba(1, 0.85, 0.85, 0.85)
        cr.fill()
    col = _hp_col(cur)
    if cur < 0.2 and (t % 0.6) > 0.4:
        col = (*col[:3], 0.35)
    if cur > 0:
        rrect(cr, bx, by, max(bh, bw * cur), bh, bh / 2)
        cr.set_source_rgba(*col)
        cr.fill()
        rrect(cr, bx + 4, by + 3, max(bh - 8, bw * cur - 8), 4, 2)    # glossy top line
        cr.set_source_rgba(1, 1, 1, 0.35 * col[3])
        cr.fill()
    for k in range(1, 10):                                     # segment ticks every 10%
        cr.rectangle(bx + bw * k / 10 - 1, by + 2, 2, bh - 4)
    cr.set_source_rgba(*TRACK[:3], 0.55)
    cr.fill()
    if flash > 0:
        _chamfer(cr, 0, 0, w, h, 14)
        cr.set_source_rgba(1, 1, 1, 0.7 * flash)
        cr.fill()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def creature_tag(cr, t, start, name="???", threat=3, changes=(), end=None, x=372, y=HUD_TOP, w=324):
    """The creature's tag: "WILD ???" and a five-pip THREAT meter. changes = [(time, new_threat)]; new pips pop
    in, and at 4+ the meter and the frame turn red and blink. An unknown name ("???") glitches on 2s."""
    a = _fade(t, start, end, 0.0, 0.25)
    if a <= 0:
        return
    level, changed = threat, start
    for at, lv in sorted(changes):
        if t >= at:
            level, changed = lv, at
            cue("m_ui_blip", t, at)
    slide = (1 - ease_out((t - start) / 0.3)) * (W - x + 20)
    danger = level >= 4
    edge = RED if danger else _mix(MINT, YELLOW, clamp01((level - 1) / 2))
    h = 84
    cr.save()
    cr.push_group()
    cr.translate(x + slide, y)
    _panel(cr, 0, 0, w, h, edge, flip=True)
    _text(cr, "WILD", 18, 36, 22, YELLOW, ROUND)
    nx = 18 + text_width(cr, "WILD", 22, ROUND) + 12
    if name.strip("?") == "":
        rnd = random.Random(_twos(t) * 13)
        for ch in name:
            _text(cr, ch, nx + rnd.uniform(-2, 2), 37 + rnd.uniform(-2, 2), 30, WHITE, ROUND, shadow=0.4)
            nx += text_width(cr, ch, 30, ROUND) + 1
    else:
        _text(cr, name, nx, 37, 30, WHITE, ROUND, shadow=0.4)
    _text(cr, "THREAT", 18, 68, 17, (1, 1, 1, 0.7), ROUND)
    px0 = 18 + text_width(cr, "THREAT", 17, ROUND) + 14
    pw = (w - px0 - 20) / 5
    blink = danger and (t % 0.5) > 0.32
    for k in range(5):
        cx, cy = px0 + pw * (k + 0.5), 62
        on = k < level
        pop = back_out((t - changed) / 0.25, 3.0) if on and k == level - 1 and changed > start else 1.0
        s = (pw * 0.36) * max(0.0, pop)
        cr.save()
        cr.translate(cx, cy)
        cr.rotate(math.pi / 4)                                 # diamond pips
        rrect(cr, -s, -s, 2 * s, 2 * s, s * 0.3)
        cr.restore()
        if on:
            pc = _mix(YELLOW, RED, k / 4)
            cr.set_source_rgba(*pc[:3], 0.45 if blink else 1)
            cr.fill()
        else:
            cr.set_source_rgba(1, 1, 1, 0.22)
            cr.set_line_width(2)
            cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def choice_menu(cr, t, start, a="RUN", b="STAY STILL", end=None, pick=None, pick_at=None, prompt=None, y=748):
    """Two big rounded buttons popping in side by side (held ~1 s by default). pick = 0 or 1 highlights that
    button at pick_at (it turns yellow and pulses, the other dims); prompt adds a small line above."""
    if end is None:
        end = start + 1.2
    if t < start or t > end + 0.2:
        return
    cue("m_ui_blip", t, start)
    if pick_at is None:
        pick_at = start + 0.6
    if pick is not None:
        cue("m_ui_select", t, pick_at)
    out = 1 - clamp01((t - end) / 0.2)
    bw, bh = 316, 96
    if prompt:
        pa = clamp01((t - start) / 0.15) * out
        _text(cr, prompt, W / 2, y - bh / 2 - 22, 26, (1, 1, 1, pa), ROUND, "center",
              outline=INK, ow=6, shadow=0.4)
    for i, label in enumerate((a, b)):
        cx = W / 2 + (i - 0.5) * (bw + 28)
        s = back_out((t - start - 0.08 * i) / 0.28, 2.4) * (0.85 + 0.15 * out)
        if s <= 0.01:
            continue
        chosen = pick == i and t >= pick_at
        dim = pick is not None and pick != i and t >= pick_at
        if chosen:
            s *= 1.06 + 0.03 * math.sin((t - pick_at) * 14)
        al = out * (0.45 if dim else 1)
        cr.save()
        cr.translate(cx, y)
        cr.scale(s, s)
        cr.push_group()
        if chosen:                                             # a soft yellow halo hugging the pill
            for gw, ga in ((34, 0.12), (20, 0.22), (10, 0.35)):
                rrect(cr, -bw / 2, -bh / 2, bw, bh, bh / 2)
                cr.set_source_rgba(*YELLOW[:3], ga)
                cr.set_line_width(gw)
                cr.stroke()
        rrect(cr, -bw / 2, -bh / 2 + 6, bw, bh, bh / 2)          # a hard drop shadow for a pressable look
        cr.set_source_rgba(0, 0, 0, 0.45)
        cr.fill()
        rrect(cr, -bw / 2, -bh / 2, bw, bh, bh / 2)
        cr.set_source_rgba(*(YELLOW if chosen else PANEL))
        cr.fill_preserve()
        cr.set_source_rgba(*(WHITE if chosen else MINT))
        cr.set_line_width(5)
        cr.stroke()
        size = _fit(cr, label, 40, bw - 70)
        _text(cr, label, 0, size * 0.36, size, INK if chosen else WHITE, ROUND, "center")
        if chosen:                                             # a pointer arrow on the picked button
            ax = -bw / 2 + 24
            cr.move_to(ax, -11)
            cr.line_to(ax + 16, 0)
            cr.line_to(ax, 11)
            cr.close_path()
            cr.set_source_rgba(*INK)
            cr.fill()
        cr.pop_group_to_source()
        cr.paint_with_alpha(al)
        cr.restore()


def _ring_icon(cr, x, y, r, t):
    """The bond icon: a glowing gold ring with a small four-point gem on top (our own symbol)."""
    _glow(cr, x, y, r * 2.4, YELLOW, 0.5 + 0.15 * math.sin(t * 9))
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*INK)
    cr.set_line_width(r * 0.5)
    cr.stroke()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*YELLOW)
    cr.set_line_width(r * 0.32)
    cr.stroke()
    cr.arc(x, y, r, math.pi * 1.1, math.pi * 1.6)
    cr.set_source_rgba(1, 1, 1, 0.85)
    cr.set_line_width(r * 0.1)
    cr.stroke()
    _star4(cr, x, y - r, r * 0.55, t * 1.5)
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.stroke_preserve()
    cr.set_source_rgba(*MINT)
    cr.fill()


def bond_popup(cr, t, start, text="BOND!", end=None, x=W / 2, y=440):
    """BOND! popping up with a glowing ring icon over it and a burst of sparkles."""
    if end is None:
        end = start + 1.6
    a = _fade(t, start, end, 0.0, 0.25)
    if a <= 0:
        return
    cue("m_bond", t, start)
    u = t - start
    glow_burst(cr, t, start, x, y - 40, 240, YELLOW, 0.8)
    sparkles(cr, t, start + 0.05, x, y - 40, n=12, radius=230, size=36, life=1.3, seed=7)
    s = max(0.01, back_out(u / 0.3, 2.8))
    cr.save()
    cr.push_group()
    cr.translate(x, y)
    cr.scale(s, s)
    _ring_icon(cr, 0, -112, 40, u)
    size = _fit(cr, text, 120, W - 80, DISPLAY)
    _text(cr, text, 0, size * 0.42, size, YELLOW, DISPLAY, "center", outline=INK, ow=size * 0.17, shadow=0.5)
    text_path(cr, text, 0, size * 0.42, size, DISPLAY, "center")       # a white shine across the top half
    cr.save()
    cr.clip()
    cr.rectangle(-W, -size * 0.6, 2 * W, size * 0.42)
    cr.set_source_rgba(1, 1, 1, 0.45)
    cr.fill()
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def rule_chip(cr, t, start, text="NEVER RUN FROM SMALL THINGS", num=1, end=None, y=300):
    """RULE 1 · NEVER RUN FROM SMALL THINGS: a two-part chip (mint RULE n block, dark text block) that slides in
    from the left with a small overshoot."""
    if end is None:
        end = start + 2.5
    a = _fade(t, start, end, 0.0, 0.2)
    if a <= 0:
        return
    cue("m_ui_blip", t, start)
    tag = f"RULE {num}"
    tsize = 26
    tw = text_width(cr, tag, tsize, ROUND) + 34
    size = _fit(cr, text, 30, W - 48 - tw - 40)
    bw = text_width(cr, text, size, ROUND) + 40
    total = tw + bw
    x0 = (W - total) / 2
    h = 64
    slide = (1 - back_out((t - start) / 0.35, 1.6)) * -(total + x0 + 40)
    cr.save()
    cr.push_group()
    cr.translate(x0 + slide, y - h / 2)
    _chamfer(cr, 0, 0, total, h, 14)
    cr.set_source_rgba(*PANEL)
    cr.fill_preserve()
    cr.set_source_rgba(*MINT)
    cr.set_line_width(3)
    cr.stroke()
    cr.move_to(14, 0)
    cr.line_to(tw, 0)
    cr.line_to(tw, h)
    cr.line_to(0, h)
    cr.line_to(0, 14)
    cr.close_path()
    cr.set_source_rgba(*MINT)
    cr.fill()
    _text(cr, tag, tw / 2, h / 2 + tsize * 0.36, tsize, INK, ROUND, "center")
    _text(cr, text, tw + 20, h / 2 + size * 0.36, size, WHITE, ROUND)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def fact_card(cr, t, start, text="BUBBLE: ~4,700 °C · ONLY IN WATER", pic=None, end=None, y=300):
    """A fact card: "HEAD: fact · fact" as a yellow head over one line per fact (numbers in yellow), with a
    picture slot on the left. pic is None (a "?" placeholder), a cairo ImageSurface (scaled to fit) or a
    callable pic(cr, x, y, w, h) that draws into the slot. The card flips open from its middle."""
    if end is None:
        end = start + 3.0
    a = _fade(t, start, end, 0.0, 0.2)
    if a <= 0:
        return
    cue("m_ui_blip", t, start)
    head, _, rest = text.partition(":")
    facts = [f.strip() for f in rest.split("·") if f.strip()] or [head]
    w, ps = 660, 176
    h = max(ps + 44, 96 + 52 * len(facts))
    x0 = (W - w) / 2
    open_ = back_out((t - start) / 0.3, 1.8)
    cr.save()
    cr.push_group()
    cr.translate(x0, y + h / 2)
    cr.scale(1, max(0.02, open_))
    cr.translate(0, -h / 2)
    _panel(cr, 0, 0, w, h, YELLOW, 18)
    sx, sy = 22, (h - ps) / 2                                  # the picture slot
    rrect(cr, sx, sy, ps, ps, 18)
    cr.set_source_rgba(0.02, 0.02, 0.07, 0.95)
    cr.fill()
    cr.save()
    rrect(cr, sx, sy, ps, ps, 18)
    cr.clip()
    if pic is None:
        _text(cr, "?", sx + ps / 2, sy + ps / 2 + 34, 96, (1, 1, 1, 0.25), DISPLAY, "center")
    elif isinstance(pic, cairo.ImageSurface):
        k = max(ps / pic.get_width(), ps / pic.get_height())
        cr.translate(sx + ps / 2, sy + ps / 2)
        cr.scale(k, k)
        cr.set_source_surface(pic, -pic.get_width() / 2, -pic.get_height() / 2)
        cr.paint()
    else:
        pic(cr, sx, sy, ps, ps)
    cr.restore()
    rrect(cr, sx, sy, ps, ps, 18)
    cr.set_source_rgba(*YELLOW[:3], 0.9)
    cr.set_line_width(3)
    cr.stroke()
    tx = sx + ps + 26
    tmax = w - tx - 22
    rrect(cr, tx, 22, text_width(cr, "FACT", 18, ROUND) + 22, 28, 6)
    cr.set_source_rgba(*YELLOW)
    cr.fill()
    _text(cr, "FACT", tx + 11, 42, 18, INK, ROUND)
    hs = _fit(cr, head.strip(), 44, tmax)
    _text(cr, head.strip(), tx, 92, hs, YELLOW, ROUND, shadow=0.4)
    yy = 92 + 50
    for k, f in enumerate(facts if rest else []):
        ap = clamp01((t - start - 0.25 - 0.18 * k) / 0.15)       # facts tick in one by one
        fs = _fit(cr, f, 36, tmax)
        hot = any(c.isdigit() for c in f)
        _text(cr, f, tx, yy, fs, (*(YELLOW if hot else WHITE)[:3], ap), ROUND)
        yy += 50
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


_ICONS = ("circle", "square", "triangle", "diamond", "star", "drop")


def _icon(cr, kind, x, y, r):
    cr.new_path()
    if kind == "circle":
        cr.arc(x, y, r, 0, 2 * math.pi)
    elif kind == "square":
        rrect(cr, x - r, y - r, 2 * r, 2 * r, r * 0.3)
    elif kind == "triangle":
        cr.move_to(x, y - r)
        cr.line_to(x + r * 1.05, y + r * 0.8)
        cr.line_to(x - r * 1.05, y + r * 0.8)
        cr.close_path()
    elif kind == "diamond":
        cr.move_to(x, y - r * 1.15)
        cr.line_to(x + r, y)
        cr.line_to(x, y + r * 1.15)
        cr.line_to(x - r, y)
        cr.close_path()
    elif kind == "star":
        _star4(cr, x, y, r * 1.2)
    else:
        cr.move_to(x, y - r * 1.2)
        cr.curve_to(x + r * 1.1, y, x + r, y + r, x, y + r)
        cr.curve_to(x - r, y + r, x - r * 1.1, y, x, y - r * 1.2)
        cr.close_path()


def hud_boot(cr, t, start, title="FIELD LOG", items=("CREATURES", "RULES", "MAP", "BONDS"), end=None, y=360,
             cursor=0):
    """The game menu booting up with a chime: a bright line opens into a panel with scanlines, the title types
    on, and the menu tiles pop in one by one (each with a blip); `cursor` marks one tile. Closes back to a line."""
    if end is None:
        end = start + 2.5
    if t < start or t > end + 0.3:
        return
    cue("m_chime_hud", t, start)
    u = t - start
    w = 600
    rows = (len(items) + 1) // 2
    h = 120 + rows * 110
    x0 = (W - w) / 2
    line = ease_out(u / 0.15)
    opn = ease_out((u - 0.12) / 0.25)
    if t > end:
        opn = 1 - ease_out((t - end) / 0.18)
        line = 1 - clamp01((t - end - 0.15) / 0.15)
    cr.save()
    if opn < 0.04:
        lw = w * line
        _glow(cr, W / 2, y + h / 2, lw * 0.6, MINT, 0.35 * line)
        cr.rectangle(W / 2 - lw / 2, y + h / 2 - 2, lw, 4)
        cr.set_source_rgba(1, 1, 1, line)
        cr.fill()
        cr.restore()
        return
    cr.translate(x0, y + h / 2)
    cr.scale(1, opn)
    cr.translate(0, -h / 2)
    _glow(cr, w / 2, h / 2, w * 0.6, MINT, 0.18)
    _panel(cr, 0, 0, w, h, MINT, 20)
    cr.save()                                                  # scanlines, rolling down
    _chamfer(cr, 0, 0, w, h, 20)
    cr.clip()
    off = (u * 40) % 6
    for yy in np.arange(-6 + off, h, 6):
        cr.rectangle(0, yy, w, 2)
    cr.set_source_rgba(1, 1, 1, 0.04)
    cr.fill()
    sweep = (u * 1.3 % 1.4) * h                                # a bright refresh band
    g = cairo.LinearGradient(0, sweep - 40, 0, sweep + 40)
    g.add_color_stop_rgba(0, *MINT[:3], 0)
    g.add_color_stop_rgba(0.5, *MINT[:3], 0.12)
    g.add_color_stop_rgba(1, *MINT[:3], 0)
    cr.set_source(g)
    cr.rectangle(0, sweep - 40, w, 80)
    cr.fill()
    cr.restore()
    for cx, cy, dx, dy in ((14, 14, 1, 1), (w - 14, 14, -1, 1), (14, h - 14, 1, -1), (w - 14, h - 14, -1, -1)):
        cr.move_to(cx, cy + dy * 22)                           # corner brackets
        cr.line_to(cx, cy)
        cr.line_to(cx + dx * 22, cy)
    cr.set_source_rgba(*MINT)
    cr.set_line_width(3)
    cr.stroke()
    n = int(len(title) * clamp01((u - 0.3) / 0.35))           # the title types on from where it will sit
    tx = w / 2 - text_width(cr, title, 40, ROUND) / 2
    _text(cr, title[:n], tx, 70, 40, WHITE, ROUND, shadow=0.4)
    if n < len(title) and u > 0.3 and (u * 3) % 1 < 0.6:
        cr.rectangle(tx + text_width(cr, title[:n], 40, ROUND) + 4, 40, 14, 34)
        cr.set_source_rgba(*MINT)
        cr.fill()
    cr.rectangle(40, 90, w - 80, 2)
    cr.set_source_rgba(*MINT[:3], 0.4)
    cr.fill()
    tw_, th_ = (w - 40 * 2 - 20) / 2, 90
    for k, label in enumerate(items):
        at = start + 0.6 + 0.12 * k
        cue("m_ui_blip", t, at)
        s = back_out((t - at) / 0.22, 2.4)
        if s <= 0.01:
            continue
        cx = 40 + (k % 2) * (tw_ + 20) + tw_ / 2
        cy = 112 + (k // 2) * 110 + th_ / 2
        sel = k == cursor and t >= at + 0.25
        cr.save()
        cr.translate(cx, cy)
        cr.scale(s, s)
        rrect(cr, -tw_ / 2, -th_ / 2, tw_, th_, 16)
        cr.set_source_rgba(*(MINT[:3] if sel else (1, 1, 1)), 0.22 if sel else 0.07)
        cr.fill_preserve()
        cr.set_source_rgba(*(MINT if sel else (1, 1, 1, 0.3)))
        cr.set_line_width(3 if sel else 2)
        cr.stroke()
        _icon(cr, _ICONS[k % len(_ICONS)], -tw_ / 2 + 38, 0, 15)
        cr.set_source_rgba(*(YELLOW if sel else MINT))
        cr.fill()
        size = _fit(cr, label, 28, tw_ - 110)
        _text(cr, label, -tw_ / 2 + 66, size * 0.36, size, WHITE, ROUND)
        if sel:
            bob = 4 * math.sin((t - at) * 10)
            cr.move_to(tw_ / 2 - 30 + bob, -10)
            cr.line_to(tw_ / 2 - 16 + bob, 0)
            cr.line_to(tw_ / 2 - 30 + bob, 10)
            cr.close_path()
            cr.set_source_rgba(*YELLOW)
            cr.fill()
        cr.restore()
    cr.restore()


def hook_text(cr, t, start, lines=("THE CUTE ONES", "KILL FIRST"), red=("KILL",), end=None, y=230, size=84):
    """The hook in big rounded type from frame 0: white words, the `red` words in the channel's red, a thick dark
    outline. Each word lands with a quick squash (it is fully visible on its first frame); fades out after end."""
    a = _fade(t, start, end, 0.0, 0.25)
    if a <= 0:
        return
    hot = {r.lower() for r in red}
    cr.save()
    cr.push_group()
    k = 0
    for j, ln in enumerate(lines):
        words = ln.split()
        gap = text_width(cr, " ", size, ROUND) + size * 0.2       # wide gaps: the thick outlines must not touch
        full = sum(text_width(cr, wd, size, ROUND) for wd in words) + gap * (len(words) - 1)
        sz = size * min(1.0, (W - 70) / full)
        space = gap * sz / size
        widths = [text_width(cr, wd, sz, ROUND) for wd in words]
        x = W / 2 - (sum(widths) + space * (len(words) - 1)) / 2
        base = y + j * size * 1.08
        for wd, ww in zip(words, widths):
            land = 1 - ease_out((t - start - 0.05 * k) / 0.14)   # 1 before the word lands, 0 once it has
            s = 1 + 0.08 * land
            col = RED if wd.strip(".,!?\"'").lower() in hot else WHITE
            cr.save()
            cr.translate(x + ww / 2, base - sz * 0.35 - sz * 0.22 * land)
            cr.scale(s, s)
            _text(cr, wd, 0, sz * 0.35, sz, col, ROUND, "center", outline=INK, ow=sz * 0.18, shadow=0.5)
            cr.restore()
            x += ww + space
            k += 1
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()
