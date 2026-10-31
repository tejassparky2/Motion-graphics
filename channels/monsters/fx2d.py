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


# ================================================================ v3 effects (Episode 1 v3, Q5: helper 7)
# Added beside the v2 functions (not replacing them) so shots already built on impact_frame / speed_lines don't move.

def _two_tone(cr, invert):
    """Turn what is already drawn into pure black/white (Otsu split, as impact_frame does)."""
    surf = cr.get_target()
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    a = np.ndarray((h, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :w]
    lum = gaussian_filter((0.114 * a[..., 0] + 0.587 * a[..., 1] + 0.299 * a[..., 2]).astype(np.float32), 1.5)
    v = np.clip((lum - _otsu(lum[::3, ::3])) * 0.25 + 0.5, 0, 1)
    if invert:
        v = 1 - v
    a[..., :3] = (v * 255).astype(np.uint8)[..., None]
    a[..., 3] = 255
    surf.mark_dirty()


def _taper(cr, cx, cy, ang, r0, r1, w0, w1, bend=0.0):
    """A tapered stroke from radius r0 (width w0) out to r1 (width w1), optionally bent sideways: a manga focus line."""
    ca, sa = math.cos(ang), math.sin(ang)
    nx, ny = -sa, ca
    mx, my = cx + ca * (r0 + r1) / 2 + nx * bend, cy + sa * (r0 + r1) / 2 + ny * bend
    cr.move_to(cx + ca * r0 + nx * w0 / 2, cy + sa * r0 + ny * w0 / 2)
    cr.curve_to(mx + nx * (w0 + w1) / 4, my + ny * (w0 + w1) / 4, mx + nx * (w0 + w1) / 4, my + ny * (w0 + w1) / 4,
                cx + ca * r1 + nx * w1 / 2, cy + sa * r1 + ny * w1 / 2)
    cr.line_to(cx + ca * r1 - nx * w1 / 2, cy + sa * r1 - ny * w1 / 2)
    cr.curve_to(mx - nx * (w0 + w1) / 4, my - ny * (w0 + w1) / 4, mx - nx * (w0 + w1) / 4, my - ny * (w0 + w1) / 4,
                cx + ca * r0 - nx * w0 / 2, cy + sa * r0 - ny * w0 / 2)
    cr.close_path()


def impact_frame_v3(cr, t, start, cx=W / 2, cy=H * 0.5, frames=4, accent="#ff3b30", subject=None, clear=200,
                    seed=0, sound=False):
    """A fuller anime impact on 1s, 4 frames from `start` (draw on the frame's own context, after the render, before
    the HUD and captions):
      0  white-out flash, the subject as a black silhouette;
      1  inverted two-tone (white subject on black) with tapered focus lines bursting out of (cx, cy);
      2  the accent frame: the background flooded with `accent`, the subject solid black, white lines;
      3  normal two-tone (black on white) with the lines thinning out.
    subject: the shot's character-only RGBA pass for this frame (a cairo ImageSurface), which keeps the subject a
    clean silhouette; without it frames 0 and 2 use the two-tone of the whole frame. Lines change every frame."""
    k = int(math.floor((t - start) * FPS + 1e-6))
    if not 0 <= k < frames:
        return
    if sound:
        cue("m_hit", t, start)
    rnd = random.Random(seed * 7919 + k)

    def silhouette(col):
        if subject is None:
            return False
        cr.save()
        cr.set_source_rgba(*col[:3], 1)
        cr.mask_surface(subject, 0, 0)
        cr.restore()
        return True

    def lines(col, n, w_out, keep=1.0):
        cr.save()
        cr.set_source_rgba(*col)
        for i in range(n):
            if rnd.random() > keep:
                continue
            ang = (i + rnd.uniform(-0.45, 0.45)) * 2 * math.pi / n
            r0 = clear * rnd.uniform(0.9, 1.7)
            _taper(cr, cx, cy, ang, r0, 1700, 0.5, w_out * rnd.uniform(0.5, 1.5), rnd.uniform(-18, 18))
        cr.fill()
        cr.restore()

    phase = k % 4
    if phase == 0:
        if subject is None:                                      # a white-out with the subject's shape still showing
            _two_tone(cr, False)
        cr.save()
        cr.set_source_rgba(1, 1, 1, 1.0 if subject is not None else 0.6)
        cr.paint()
        cr.restore()
        silhouette(INK)
        lines(INK, 40, 16, 0.6)
    elif phase == 1:
        _two_tone(cr, True)
        lines(WHITE, 64, 30)
    elif phase == 2:
        if subject is None:                                      # two-tone, then the white turns accent, black stays
            _two_tone(cr, False)
            cr.save()
            cr.set_operator(cairo.OPERATOR_MULTIPLY)
            cr.set_source_rgba(*hexa(accent))
            cr.paint()
            cr.restore()
        else:
            cr.save()
            cr.set_source_rgba(*hexa(accent))
            cr.paint()
            cr.restore()
            silhouette(INK)
        lines(WHITE, 56, 24, 0.85)
    else:
        _two_tone(cr, False)
        lines(INK, 48, 12, 0.7)


def speed_lines_v3(cr, t, start, end=None, mode="radial", cx=W / 2, cy=H * 0.45, col=WHITE, bg=None, n=90,
                   clear=0.24, speed=1.0, seed=0):
    """Speed lines that move: tapered strokes (hair-thin at the inner tip, thick at the edge) that keep streaming
    while they are re-dealt on 2s, with a feathered open zone round the focus.
      mode "radial"     focus lines rushing in towards (cx, cy) (a reaction, a lock-on);
      mode "horizontal" streaks racing right to left (a dash);
      mode "vertical"   streaks falling past (a fall, a dive): they run downwards.
    bg: None draws only the lines over the render; a pair of hex colours paints a gradient behind them first
    (centre colour, edge colour). clear = open radius as a fraction of the frame height (radial)."""
    a = _fade(t, start, end, 0.04, 0.15)
    if a <= 0:
        return
    u = t - start
    cr.save()
    cr.push_group()
    if bg:
        c0, c1 = hexa(bg[0]), hexa(bg[1])
        g = (cairo.RadialGradient(cx, cy, 0, cx, cy, H * 0.85) if mode == "radial"
             else cairo.LinearGradient(0, 0, W, 0) if mode == "vertical" else cairo.LinearGradient(0, 0, 0, H))
        if mode == "radial":
            g.add_color_stop_rgba(0, *c0)
        else:
            g.add_color_stop_rgba(0, *c1)
            g.add_color_stop_rgba(0.5, *c0)
        g.add_color_stop_rgba(1, *c1)
        cr.set_source(g)
        cr.paint()
    rnd = random.Random(seed * 104729 + _twos(u))
    if mode == "radial":
        flow = (u * 2.2 * speed) % 1.0                           # the lines creep inwards between re-deals
        for i in range(n):
            ang = rnd.uniform(0, 2 * math.pi)
            r0 = H * clear * rnd.uniform(0.9, 1.7) * (1 - 0.12 * flow)
            cr.set_source_rgba(*col[:3], col[3] * rnd.uniform(0.5, 0.95))
            _taper(cr, cx, cy, ang, r0, 1600, 0.4, rnd.uniform(5, 22))
            cr.fill()
    else:
        horizontal = mode == "horizontal"
        span, across = (W, H) if horizontal else (H, W)
        for i in range(n):
            pos = rnd.uniform(0, across)
            ln = rnd.uniform(140, 640)
            th = rnd.uniform(2, 10)
            go = (rnd.uniform(0, span + ln) + u * 2600 * speed * rnd.uniform(0.7, 1.3)) % (span + 2 * ln) - ln
            head = span - go if horizontal else go                # horizontal runs right to left, vertical falls
            tail = head + ln if horizontal else head - ln
            cr.set_source_rgba(*col[:3], col[3] * rnd.uniform(0.45, 0.9))
            if horizontal:
                cr.move_to(head, pos)
                cr.curve_to(head + ln * 0.4, pos - th, tail - ln * 0.2, pos - th * 0.4, tail, pos)
                cr.curve_to(tail - ln * 0.2, pos + th * 0.4, head + ln * 0.4, pos + th, head, pos)
            else:
                cr.move_to(pos, head)
                cr.curve_to(pos - th, head - ln * 0.4, pos - th * 0.4, tail + ln * 0.2, pos, tail)
                cr.curve_to(pos + th * 0.4, tail + ln * 0.2, pos + th, head - ln * 0.4, pos, head)
            cr.fill()
    cr.pop_group_to_source()
    if mode == "radial":                                         # feather the open zone so lines fade in, not stop
        m = cairo.RadialGradient(cx, cy, H * clear * 0.7, cx, cy, H * clear * 1.35)
        m.add_color_stop_rgba(0, 0, 0, 0, 0)
        m.add_color_stop_rgba(1, 0, 0, 0, a)
        cr.mask(m) if not bg else cr.paint_with_alpha(a)
    else:
        cr.paint_with_alpha(a)


# ================================================================ v3 effects (Q5): electricity, x-ray, soul spark
ELECTRIC = hexa("#7fd8ff")           # the blue of the lab zap
SOUL = hexa("#ffe7a3")               # Kai's soul spark: warm white-gold


def _bolt(rnd, p0, p1, rough=0.25, depth=5):
    """A jagged polyline from p0 to p1 (midpoint displacement): every level kicks each midpoint sideways by up to
    `rough` times that segment's length, so the zigzag is the same at every scale."""
    pts = [p0, p1]
    for _ in range(depth):
        nxt = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1.0
            off = rnd.uniform(-rough, rough) * ln
            nxt += [((a[0] + b[0]) / 2 - dy / ln * off, (a[1] + b[1]) / 2 + dx / ln * off), b]
        pts = nxt
    return pts


def _cut_path(path, frac):
    """The first `frac` (0-1, by length) of a polyline, and the point where it stops."""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])]
    goal = sum(segs) * clamp01(frac)
    out = [path[0]]
    for (a, b), s in zip(zip(path, path[1:]), segs):
        if goal <= s:
            k = goal / s if s else 1.0
            p = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
            out.append(p)
            return out, p
        out.append(b)
        goal -= s
    return out, path[-1]


def _stroke_bolt(cr, pts, width, col, a):
    """Three passes: a wide soft glow (added), the coloured body, a white-hot core."""
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for w, c, alpha, op in ((width * 5.0, col, 0.16 * a, cairo.OPERATOR_ADD),
                            (width * 2.4, col, 0.35 * a, cairo.OPERATOR_ADD),
                            (width * 1.25, col, 0.95 * a, cairo.OPERATOR_OVER),
                            (width * 0.5, WHITE, a, cairo.OPERATOR_OVER)):
        cr.set_operator(op)
        cr.set_source_rgba(*c[:3], alpha)
        cr.set_line_width(w)
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.stroke()
    cr.restore()


def electric_arcs(cr, t, start, end=None, path=((200, 900), (520, 500)), n=3, width=5.0, col=ELECTRIC, rough=0.25,
                  branches=3, travel=0.0, ones=True, flicker=0.25, glow=True, sound=True, seed=0):
    """Crackling electric arcs along `path` (pixel points: the strip, the water, his feet, his chest...).

    n jagged bolts follow the path, redrawn every frame (ones=True: electricity on 1s reads as live current; False
    keeps them on 2s like the characters), with `branches` short forks and glows where they start and end.
    travel > 0: the current RUNS along the path over that many seconds (a bright head leads, the bolts grow behind
    it), then keeps crackling until `end`. flicker: the chance that a frame stutters dim (never the first)."""
    a = _fade(t, start, end, 0.0, 0.08)
    if a <= 0:
        return
    if sound:
        cue("m_spark", t, start)
    k = int(math.floor(t * FPS + 1e-6)) if ones else _twos(t)
    rnd = random.Random(seed * 7919 + k)
    if k != int(math.floor(start * FPS + 1e-6)) and rnd.random() < flicker:
        a *= 0.35
    path = [tuple(p) for p in path]
    head = path[-1]
    if travel > 0 and t - start < travel:
        path, head = _cut_path(path, ease_out((t - start) / travel))
        if len(path) < 2 or math.hypot(head[0] - path[0][0], head[1] - path[0][1]) < 2:
            path = [path[0], (path[0][0] + 1, path[0][1])]
    span = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(path, path[1:]))
    cr.save()
    for i in range(n):
        pts = [path[0]]
        for p, q in zip(path, path[1:]):
            pts += _bolt(rnd, p, q, rough * rnd.uniform(0.7, 1.2), 5)[1:]
        _stroke_bolt(cr, pts, width * (1.0 if i == 0 else rnd.uniform(0.45, 0.75)), col, a * (1 if i == 0 else 0.8))
        if i == 0:                                              # forks off the main bolt
            for _ in range(branches):
                j = rnd.randrange(1, max(2, len(pts) - 1))
                p, q = pts[j - 1], pts[j]
                ang = math.atan2(q[1] - p[1], q[0] - p[0]) + rnd.choice((-1, 1)) * rnd.uniform(0.4, 1.0)
                ln = span * rnd.uniform(0.12, 0.3)
                tip = (q[0] + math.cos(ang) * ln, q[1] + math.sin(ang) * ln)
                _stroke_bolt(cr, _bolt(rnd, q, tip, rough, 4), width * 0.45, col, a * 0.85)
    if glow:
        _glow(cr, path[0][0], path[0][1], width * 14, col, 0.8 * a)
        _glow(cr, head[0], head[1], width * (18 if travel and t - start < travel else 12), col, 0.9 * a)
        _glow(cr, head[0], head[1], width * 4, WHITE, a)
    cr.restore()


# ---- the x-ray skeleton flash
JOINTS = ("head", "neck", "chest", "pelvis", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_hand", "r_hand",
          "l_hip", "r_hip", "l_knee", "r_knee", "l_foot", "r_foot")


def joints_from_box(x, y, w, h, head=0.22, arms_out=0.0):
    """Standing-pose joint positions (pixels) for a figure filling the box (x, y, w, h), facing the camera. head is
    the head's share of the height (Kai's anime proportions ~0.2); arms_out 0 = arms down, 1 = straight out (the
    stiff electrocution pose)."""
    cx = x + w / 2

    def p(fx, fy):
        return (cx + fx * w, y + fy * h)
    hr = head / 2
    out = dict(head=p(0, hr), neck=p(0, head + 0.02), chest=p(0, head + 0.12), pelvis=p(0, head + 0.33),
               l_shoulder=p(-0.2, head + 0.05), r_shoulder=p(0.2, head + 0.05),
               l_hip=p(-0.1, head + 0.36), r_hip=p(0.1, head + 0.36),
               l_knee=p(-0.11, head + 0.58), r_knee=p(0.11, head + 0.58),
               l_foot=p(-0.12, 0.97), r_foot=p(0.12, 0.97))
    for s, sg in (("l", -1), ("r", 1)):
        sh = out[s + "_shoulder"]
        ang = math.radians(90 - 80 * arms_out) if sg > 0 else math.radians(90 + 80 * arms_out)
        up = h * 0.15
        el = (sh[0] + math.cos(ang) * up + sg * w * 0.03, sh[1] + math.sin(ang) * up)
        out[s + "_elbow"] = el
        out[s + "_hand"] = (el[0] + math.cos(ang) * up, el[1] + math.sin(ang) * up)
    return out


def _bone_seg(cr, p, q, w):
    """A cartoon long bone: a shaft with two round knobs at each end."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(w)
    cr.move_to(*p)
    cr.line_to(*q)
    cr.stroke()
    for c, sgn in ((p, 1), (q, -1)):
        for side in (-1, 1):
            cr.arc(c[0] + nx * side * w * 0.45 + dx / ln * sgn * w * 0.15,
                   c[1] + ny * side * w * 0.45 + dy / ln * sgn * w * 0.15, w * 0.62, 0, 2 * math.pi)
            cr.fill()


def _skeleton(cr, j, col, hole, head_r=None):
    """Skull, spine, ribs, pelvis and limb bones from joint positions (pixels)."""
    torso = math.hypot(j["pelvis"][0] - j["neck"][0], j["pelvis"][1] - j["neck"][1])
    hr = head_r or 0.42 * torso
    w = max(4.0, hr * 0.22)
    cr.save()
    cr.set_source_rgba(*col)
    # limbs
    for a, b in (("l_shoulder", "l_elbow"), ("l_elbow", "l_hand"), ("r_shoulder", "r_elbow"), ("r_elbow", "r_hand"),
                 ("l_hip", "l_knee"), ("l_knee", "l_foot"), ("r_hip", "r_knee"), ("r_knee", "r_foot"),
                 ("l_shoulder", "r_shoulder")):
        _bone_seg(cr, j[a], j[b], w * (1.15 if "knee" in a + b or "hip" in a else 0.9))
    for s in ("l_hand", "r_hand"):                              # little finger fans
        e = j[s.replace("hand", "elbow")]
        h = j[s]
        ang = math.atan2(h[1] - e[1], h[0] - e[0])
        for f in (-0.5, -0.17, 0.17, 0.5):
            cr.set_line_width(w * 0.4)
            cr.move_to(*h)
            cr.line_to(h[0] + math.cos(ang + f) * w * 2.2, h[1] + math.sin(ang + f) * w * 2.2)
            cr.stroke()
    # spine: vertebrae from neck to pelvis
    n = 9
    for i in range(n):
        k = i / (n - 1)
        x = j["neck"][0] + (j["pelvis"][0] - j["neck"][0]) * k
        y = j["neck"][1] + (j["pelvis"][1] - j["neck"][1]) * k
        cr.save()
        cr.translate(x, y)
        cr.scale(w * 0.75, w * 0.45)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    # ribs: curved pairs hanging off the upper spine
    cr.set_line_width(w * 0.55)
    sw = math.hypot(j["r_shoulder"][0] - j["l_shoulder"][0], j["r_shoulder"][1] - j["l_shoulder"][1])
    for i in range(4):
        k = 0.12 + i * 0.13
        x = j["neck"][0] + (j["pelvis"][0] - j["neck"][0]) * k
        y = j["neck"][1] + (j["pelvis"][1] - j["neck"][1]) * k
        half = sw * (0.42 - i * 0.04)
        for sg in (-1, 1):
            cr.move_to(x, y)
            cr.curve_to(x + sg * half * 0.8, y - w * 0.6, x + sg * half * 1.1, y + w * 1.2, x + sg * half * 0.7,
                        y + w * 2.0)
            cr.stroke()
    # pelvis: a butterfly between the hips
    px, py = j["pelvis"]
    hw = abs(j["r_hip"][0] - j["l_hip"][0]) * 0.75 + w
    cr.move_to(px, py - w)
    cr.curve_to(px - hw, py - w * 3, px - hw * 1.2, py + w * 1.5, px - hw * 0.3, py + w * 1.6)
    cr.line_to(px + hw * 0.3, py + w * 1.6)
    cr.curve_to(px + hw * 1.2, py + w * 1.5, px + hw, py - w * 3, px, py - w)
    cr.close_path()
    cr.fill()
    # skull: cranium + jaw, dark eye sockets and nose, a row of teeth
    hx, hy = j["head"]
    cr.arc(hx, hy - hr * 0.08, hr * 0.78, 0, 2 * math.pi)
    cr.fill()
    rrect(cr, hx - hr * 0.45, hy + hr * 0.25, hr * 0.9, hr * 0.55, hr * 0.2)
    cr.fill()
    cr.set_source_rgba(*hole)
    for sg in (-1, 1):
        cr.save()
        cr.translate(hx + sg * hr * 0.3, hy + hr * 0.02)
        cr.scale(hr * 0.2, hr * 0.24)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    cr.move_to(hx, hy + hr * 0.2)
    cr.line_to(hx - hr * 0.08, hy + hr * 0.36)
    cr.line_to(hx + hr * 0.08, hy + hr * 0.36)
    cr.close_path()
    cr.fill()
    cr.set_line_width(max(1.5, hr * 0.04))
    for i in range(5):
        x = hx - hr * 0.3 + i * hr * 0.15
        cr.move_to(x, hy + hr * 0.5)
        cr.line_to(x, hy + hr * 0.72)
    cr.move_to(hx - hr * 0.38, hy + hr * 0.6)
    cr.line_to(hx + hr * 0.38, hy + hr * 0.6)
    cr.stroke()
    cr.restore()


def _alpha_of(surf):
    surf.flush()
    a = np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :surf.get_width()]
    return a[..., 3].astype(np.float32) / 255.0


def xray_flash(cr, t, start, frames=6, beat=2, joints=None, box=None, mask=None, ctx=None, head_r=None,
               dark=hexa("#08113a"), body=hexa("#2f9bff"), rim=hexa("#bff4ff"), bone=WHITE, sound=False, seed=0):
    """The cartoon electrocution x-ray: for `frames` frames, alternating every `beat` frames, the picture goes deep
    navy, the body becomes a glowing blue silhouette and his white skeleton shows through (the other beats show
    the normal render, so it strobes).

    Silhouette: `mask` (a cairo surface whose alpha is the body; a comp.py overlay gets the subject pass through
    ctx automatically), else a glow drawn along the bones. Skeleton: `joints` (a dict of JOINTS -> pixel (x, y),
    or a function t -> dict, e.g. mk/joints.py's per-frame export from the rig), else joints_from_box(*box), else
    the mask's bounding box."""
    k = int(math.floor((t - start) * FPS + 1e-6))
    if not 0 <= k < frames or (k // beat) % 2 == 1:
        return
    if sound:
        cue("m_spark", t, start)
    if mask is None and ctx is not None:
        mask = getattr(ctx, "subject", None)
    alpha = _alpha_of(mask) if mask is not None else None
    if callable(joints):
        joints = joints(t)
    if joints is None:
        if box is None and alpha is not None:
            ys, xs = np.nonzero(alpha[::2, ::2] > 0.5)
            if len(xs):
                box = (xs.min() * 2, ys.min() * 2, (xs.max() - xs.min()) * 2, (ys.max() - ys.min()) * 2)
        if box is None:
            return
        joints = joints_from_box(*box)
    cr.save()
    cr.set_source_rgba(*dark)
    cr.paint()
    if alpha is not None and alpha.shape == (H, W):             # the body: blue fill, a bright rim, an outer glow
        halo = gaussian_filter(alpha, 14)
        edge = np.clip((alpha - gaussian_filter(alpha, 3)) * 3.0, 0, 1)
        out = np.zeros((H, W, 4), np.float32)
        cov = np.clip(alpha * 0.82 + halo * (1 - alpha) * 0.7, 0, 1)
        for c in range(3):                                      # BGRA, premultiplied
            col = body[2 - c] * (1 - edge) + rim[2 - c] * edge
            out[..., c] = col * cov * 255
        out[..., 3] = cov * 255
        arr = np.ascontiguousarray(out.astype(np.uint8))
        surf = cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, W, H, W * 4)
        cr.set_source_surface(surf, 0, 0)
        cr.paint()
        del surf
    else:                                                       # no mask: a fat glow along the limbs
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        tor = math.hypot(joints["pelvis"][0] - joints["neck"][0], joints["pelvis"][1] - joints["neck"][1])
        for w, a in ((tor * 0.75, 0.25), (tor * 0.5, 0.85)):
            cr.set_source_rgba(*body[:3], a)
            cr.set_line_width(w)
            for chain in (("l_hand", "l_elbow", "l_shoulder", "r_shoulder", "r_elbow", "r_hand"),
                          ("l_foot", "l_knee", "l_hip", "r_hip", "r_knee", "r_foot"), ("neck", "pelvis")):
                cr.move_to(*joints[chain[0]])
                for c in chain[1:]:
                    cr.line_to(*joints[c])
                cr.stroke()
            hx, hy = joints["head"]
            cr.arc(hx, hy, (head_r or 0.42 * tor) * (1.25 if a < 0.5 else 1.05), 0, 2 * math.pi)
            cr.fill()
    _skeleton(cr, joints, bone, (*dark[:3], 1.0), head_r)
    rnd = random.Random(seed * 31 + k)                         # a few crackles around the outline
    hx, hy = joints["head"]
    for _ in range(3):
        a0 = rnd.uniform(0, 2 * math.pi)
        r0 = math.hypot(joints["head"][0] - joints["l_foot"][0], joints["head"][1] - joints["l_foot"][1]) * 0.5
        mx, my = (joints["head"][0] + joints["pelvis"][0]) / 2, (joints["head"][1] + joints["l_foot"][1]) / 2
        p = (mx + math.cos(a0) * r0 * 0.6, my + math.sin(a0) * r0 * 0.9)
        q = (p[0] + math.cos(a0) * r0 * 0.3, p[1] + math.sin(a0) * r0 * 0.3)
        _stroke_bolt(cr, _bolt(rnd, p, q, 0.3, 4), 3.0, ELECTRIC, 0.9)
    cr.restore()


# ---- the soul spark
def _soul_pos(path, u, wobble, phase):
    """Point on the spark's fall at u (0-1): a smooth (Catmull-Rom) curve through `path`, swaying sideways."""
    pts = [tuple(p) for p in path]
    if len(pts) == 2:
        p = (pts[0][0] + (pts[1][0] - pts[0][0]) * u, pts[0][1] + (pts[1][1] - pts[0][1]) * u)
    else:
        segs = len(pts) - 1
        s = min(segs - 1, int(u * segs))
        f = u * segs - s
        p0, p1, p2 = pts[max(0, s - 1)], pts[s], pts[s + 1]
        p3 = pts[min(segs, s + 2)]
        p = tuple(0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * f + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * f * f
                         + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * f ** 3) for i in range(2))
    sway = wobble * math.sin(u * math.pi * 3 + phase) * math.sin(u * math.pi)   # no sway at the two ends
    return p[0] + sway, p[1]


def soul_spark(cr, t, start, end=None, path=((360, 160), (330, 520), (380, 820)), dur=1.6, size=22, col=SOUL,
               trail=0.5, wobble=26, land=True, sound=False, seed=0):
    """A tiny glowing spark (Kai's soul) drifting down along `path` over `dur` seconds with a comet trail and
    twinkles left behind it. land=True: it lands with a soft flash, a ring and a sparkle pop at the last point.
    end (None = gone right after the landing): hold it there, pulsing, until then. Drawn on 1s (it is light, not a
    character); the twinkles are on 2s."""
    if t < start:
        return
    stop = start + dur + (0.45 if land else 0.0)
    hold_to = max(stop, end) if end is not None else stop
    if t > hold_to + 0.15:
        return
    a = 1.0 - (clamp01((t - hold_to) / 0.15) if t > hold_to else 0.0)
    if sound:
        cue("m_chime_hud", t, start)
    phase = seed * 1.7

    def at(tt):
        u = clamp01((tt - start) / dur)
        u = u * u * (3 - 2 * u) * 0.35 + u * 0.65          # eases in and out, but never stalls
        return _soul_pos(path, u, wobble, phase)
    cr.save()
    flying = t - start < dur
    if flying:                                               # the trail: overlapping additive dots, tapering
        steps = 22
        for i in range(steps, 0, -1):
            tt = t - trail * i / steps
            if tt < start:
                continue
            x, y = at(tt)
            k = 1 - i / steps
            _glow(cr, x, y, size * (0.6 + 1.6 * k), col, 0.22 * k * a)
            cr.set_source_rgba(1, 1, 1, 0.5 * k * k * a)
            cr.arc(x, y, size * 0.32 * k, 0, 2 * math.pi)
            cr.fill()
        rnd = random.Random(seed * 101 + _twos(t))           # twinkles shed behind it
        for i in range(4):
            tt = t - rnd.uniform(0.05, trail * 1.4)
            if tt < start:
                continue
            x, y = at(tt)
            life = 1 - (t - tt) / (trail * 1.4)
            cr.set_source_rgba(*col[:3], 0.9 * life * a)
            _star4(cr, x + rnd.uniform(-18, 18), y + rnd.uniform(-10, 10), size * 0.5 * life + 3,
                   rnd.uniform(0, 0.8))
            cr.fill()
    x, y = at(min(t, start + dur))
    pulse = 1 + 0.12 * math.sin((t - start) * 2 * math.pi * 2.2)
    _glow(cr, x, y, size * 4.5 * pulse, col, 0.5 * a)
    _glow(cr, x, y, size * 1.8 * pulse, WHITE, 0.9 * a)
    cr.set_source_rgba(1, 1, 1, a)
    _star4(cr, x, y, size * 1.4 * pulse, (t - start) * 0.8, 0.14)
    cr.fill()
    cr.arc(x, y, size * 0.38, 0, 2 * math.pi)
    cr.fill()
    if land and not flying:                                  # landing: flash, ring, sparkle pop
        u = clamp01((t - start - dur) / 0.45)
        _glow(cr, x, y, size * (5 + 6 * u), WHITE, (1 - u) * 0.9 * a)
        cr.set_source_rgba(*col[:3], (1 - u) * a)
        cr.set_line_width(4 * (1 - u) + 1)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.35)                                    # a ring lying on the ground
        cr.arc(0, 0, size * (1.5 + 7 * ease_out(u)), 0, 2 * math.pi)
        cr.restore()
        cr.stroke()
        rnd = random.Random(seed * 7 + 3)
        for i in range(6):
            ang = i * math.pi / 3 + rnd.uniform(-0.3, 0.3)
            r = size * (1.2 + 4.5 * ease_out(u))
            cr.set_source_rgba(1, 1, 1, (1 - u) * a)
            _star4(cr, x + math.cos(ang) * r, y + math.sin(ang) * r * 0.6, size * 0.5 * (1 - u) + 2, 0.3)
            cr.fill()
    cr.restore()
