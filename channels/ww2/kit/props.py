"""WW2 channel kit: vehicles, ships, planes, effects and small props (pure pycairo, all animated).

Style rules: channels/ww2/STYLE.md ("animated 1940s posters"). Every shape is a poster print: a flat side-colour
fill, slightly misregistered on big shapes (MISREG), a halftone underside (TONE, screen-sized dots), an ink key line
6 px at scale 1. No gradients: glows are halftone halos, smoke is flat two-tone puffs with a key line round the cloud,
explosions are flat star bursts, wakes are flat cream streaks. silhouette="ink" draws any prop as one flat
silhouette (crowded or distant shots). Generic marks only:
a plain roundel (Britain, France), a plain white star (US), a plain red star (Soviet). German, Italian and
Japanese machines stay plain charcoal: no crosses, no symbols of any kind.

API
---
Every prop is a class built once and drawn every frame:

    from channels.ww2.kit.props import *
    tank = Tank(x=900, y=820, scale=0.8, facing=-1, side="germany")
    tank.draw(cr, t, speed=120, turret=20, fire=[2.0])        # any keyword overrides the constructor for one frame

Common arguments (constructor or draw()):
    x, y      where the prop stands: its ground point (land), its waterline centre (ships), its centre (planes)
    scale     1.0 = drawn at the sizes below (a stick figure is 300 px tall at scale 1)
    facing    1 faces right, -1 faces left (mirrors the prop)
    side      "germany" "italy" "japan" "britain" "france" "usa" "allies" "soviet" "china" "neutral" (fill + marks)
    mark      override the insignia: "roundel", "roundel_fr", "star_us", "star_su" or None
    alpha     fade the whole prop (0..1)
    silhouette  a colour: the whole prop as one flat poster silhouette (ships keep their cream wake and bow wave)
    seed      varies bobbing, flicker and smoke between copies

Motion is a function of t, so frames render in any order. Moving props take `speed` (px/s in the prop's own units):
tracks, wheels, propellers and wakes follow it; move x yourself (e.g. x = lerp(x0, x1, u)). Guns take `fire=[t, ...]`
(recoil, muzzle flash, smoke). Turrets take `turret` in degrees: 0 points forward, 90 points at the camera,
180 points back, and `elev` in degrees.

Land:   Tank (~400 long), Artillery, Truck, Sandbags(length, rows), Trench(width, depth), BarbedWire(length),
        RadarTower (pulse rings), Searchlight(aim, sweep)
Air:    Fighter(bank, pitch, gear), Bomber(engines, bay, drop=[t]), DiveBomber(dive 0..1, release=t),
        Parachute(open_at, load="man"|"crate")
Sea:    Battleship(turrets, fire), Carrier(burn 0..1, planes), Destroyer, FishingBoat, Yacht(sail), PaddleFerry,
        Submarine(depth 0..1, periscope), Periscope. Ships bob, roll and leave a wake and bow wave from `speed`;
        small boats take `crowd=n` (rescued soldiers on deck). `water=None` skips the waterline strip.
Effects (functions in the current coordinates, plus classes):
        muzzle_flash(cr, x, y, age, size, angle), Explosion(start, size), smoke(cr, x, y, t, ...),
        fire(cr, x, y, t, size), Snow(density, wind), beam(cr, x, y, angle, length, width), signal_flash(...)
Small:  Telegram, SigningTable(signed 0..1), RailwayCarriage, Locomotive, Radio(on), Enigma(auto, lit),
        Candle(burn), Calendar(date, prev, flip_at)
Marks:  roundel(cr, x, y, r, french=False), star(cr, x, y, r, fill, disc=None), mark_for(side)

`python -m channels.ww2.kit.props` writes a contact sheet of everything to out/ww2/style/props_sheet.png.
"""
import math
import random

from channels.ww2.kit.core import (H, LABEL, SIDE, TITLE, W, _dot_tile, back_out, cairo, clamp01, col,
                                   ease_in, ease_out, lerp, seg, smooth, text)

HAND = LABEL        # small lettering on props (Oswald since the poster look)
MISREG = (2.5, 2.0)  # device-px offset of big fills from their key line (print misregistration)
TONE = 0.62          # halftone shading covers each big shape below this fraction of its height
DOT_CELL = 9         # halftone screen in device px

TAU = math.tau
INK = 6.0           # outline width at scale 1 (STYLE: 5-7 px)
MIN_PX = 1.4        # outlines never get thinner than this on screen, however small the prop


# ================================================================ colour and path helpers
def rgba(c, a=1.0):
    """A palette/side name, a #hex or an (r, g, b[, a]) tuple, as (r, g, b, a) with alpha multiplied by a."""
    if isinstance(c, tuple):
        return (c[0], c[1], c[2], (c[3] if len(c) > 3 else 1.0) * a)
    return col(c, a)


def shade(c, k):
    """k < 0 darkens toward black, k > 0 lightens toward white."""
    r, g, b, a = rgba(c)
    if k < 0:
        f = 1 + k
        return (r * f, g * f, b * f, a)
    return (r + (1 - r) * k, g + (1 - g) * k, b + (1 - b) * k, a)


def mix(c1, c2, u):
    a, b = rgba(c1), rgba(c2)
    return tuple(lerp(a[i], b[i], u) for i in range(4))


def poly(cr, pts, close=True):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    if close:
        cr.close_path()


def rrect(cr, x, y, w, h, r):
    r = max(0.0, min(r, w / 2, h / 2))
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def ellipse(cr, cx, cy, rx, ry):
    cr.save()
    cr.translate(cx, cy)
    cr.scale(max(rx, 1e-3), max(ry, 1e-3))
    cr.new_sub_path()
    cr.arc(0, 0, 1, 0, TAU)
    cr.restore()


def ink(cr, lw, color="ink", a=1.0, keep=False):
    cr.set_source_rgba(*rgba(color, a))
    cr.set_line_width(lw)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke_preserve() if keep else cr.stroke()


def fill(cr, color, a=1.0, keep=False):
    cr.set_source_rgba(*rgba(color, a))
    cr.fill_preserve() if keep else cr.fill()


def dots(cr, color, density=3, alpha=1.0, below=None, cell=DOT_CELL):
    """Halftone the current path (kept) in `color`; below = only under that user-space y. Dots are screen-sized."""
    path = cr.copy_path()
    cr.save()
    cr.clip()
    if below is not None:
        cr.rectangle(-1e5, below, 2e5, 2e5)
        cr.clip()
    cr.identity_matrix()
    cr.set_source_rgba(*rgba(color, alpha))
    cr.mask(_dot_tile(max(1, min(5, int(density))), cell))
    cr.restore()
    cr.new_path()
    cr.append_path(path)


def fill_ink(cr, color, lw, a=1.0, line="ink", tone="auto"):
    """Poster fill of the current path: a flat fill (big shapes slightly misregistered), a halftone underside on
    big shapes (tone="auto"; False for none), then the ink key line."""
    path = cr.copy_path()
    x0, y0, x1, y1 = cr.fill_extents()
    dw, dh = cr.user_to_device_distance(x1 - x0, y1 - y0)
    big = max(abs(dw), abs(dh)) > 70
    if big and MISREG:
        ox, oy = cr.device_to_user_distance(*MISREG)
        cr.save()
        cr.new_path()
        cr.translate(ox, oy)
        cr.append_path(path)
        fill(cr, color, a)
        cr.restore()
    else:
        fill(cr, color, a)
    cr.new_path()
    cr.append_path(path)
    if tone and abs(dh) > 26:
        r, g, b_, _ = rgba(color)
        light = 0.3 * r + 0.59 * g + 0.11 * b_ > 0.78       # paper-light shapes stay clean
        if not light:
            dots(cr, shade(color, -0.42), 3, a, below=y0 + TONE * (y1 - y0))
    ink(cr, lw, line, a)


def line(cr, x0, y0, x1, y1, lw, color="ink", a=1.0):
    cr.move_to(x0, y0)
    cr.line_to(x1, y1)
    ink(cr, lw, color, a)


def glow(cr, x, y, r, color, a=0.6):
    """A printed glow (no gradients in the poster look): a halftone halo around a flat inner disc."""
    if r <= 1:
        return
    cr.new_path()
    cr.arc(x, y, r * 0.72, 0, TAU)
    dots(cr, color, 2, a)
    cr.new_path()
    cr.arc(x, y, r * 0.38, 0, TAU)
    fill(cr, color, a * 0.55)


def rng(*key):
    return random.Random(hash(key) & 0xFFFFFFFF)


def noise(t, seed=0, f=1.0):
    """Smooth pseudo-noise in about -1..1 (sum of incommensurate sines)."""
    s = seed * 1.618
    return (math.sin(t * f * 2.1 + s) * 0.5 + math.sin(t * f * 3.7 + s * 2.3) * 0.3
            + math.sin(t * f * 7.3 + s * 0.7) * 0.2)


def since(t, times):
    """Seconds since the latest time in `times` that is <= t (None if none yet)."""
    best = None
    for s in times or ():
        if s <= t and (best is None or s > best):
            best = s
    return None if best is None else t - best


def recoil(age):
    """0 -> 1 kick in 0.05 s, then a spring back over about 0.6 s."""
    if age is None or age < 0:
        return 0.0
    if age < 0.05:
        return age / 0.05
    return math.exp(-(age - 0.05) * 7.0)


# ================================================================ insignia (generic only)
def roundel(cr, x, y, r, french=False, lw=None):
    """A plain three-ring roundel. British: blue outside, red centre. French: blue centre, red outside."""
    rings = (("alert", "cream", "allies") if french else ("allies", "cream", "alert"))
    for c, f in zip(rings, (1.0, 0.66, 0.33)):
        cr.arc(x, y, r * f, 0, TAU)
        fill(cr, c)
    cr.arc(x, y, r, 0, TAU)
    ink(cr, lw or max(1.0, r * 0.12))


def star(cr, x, y, r, color="cream", disc=None, lw=None, rot=0.0):
    """A plain five-pointed star; disc puts it on a coloured circle (the US mark is a white star on blue)."""
    lw = lw or max(1.0, r * 0.1)
    if disc:
        cr.arc(x, y, r * 1.12, 0, TAU)
        fill_ink(cr, disc, lw, tone=False)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    poly(cr, pts)
    fill_ink(cr, color, lw * 0.8, tone=False)


MARKS = {"britain": "roundel", "allies": "roundel", "france": "roundel_fr", "usa": "star_us", "soviet": "star_su",
         "china": "star_cn"}


def mark_for(side):
    """The generic mark for a side (None for Germany, Italy, Japan and neutral)."""
    return MARKS.get(side)


def draw_mark(cr, kind, x, y, r, lw=None):
    if not kind:
        return
    if kind == "roundel":
        roundel(cr, x, y, r, lw=lw)
    elif kind == "roundel_fr":
        roundel(cr, x, y, r, french=True, lw=lw)
    elif kind == "star_us":
        star(cr, x, y, r * 0.92, "cream", disc="allies", lw=lw)
    elif kind == "star_su":
        star(cr, x, y, r, "soviet", lw=lw)
    elif kind == "star_cn":
        star(cr, x, y, r * 0.8, "cream", disc="allies", lw=lw)


# ================================================================ effects (current coordinates)
def muzzle_flash(cr, x, y, age, size=60.0, angle=0.0, smoke_puff=True, seed=0):
    """A gun flash at (x, y) pointing along `angle` (radians); age = seconds since the shot. Flash 0.12 s, smoke 1 s."""
    if age is None or age < 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    if smoke_puff and age < 1.2:
        u = age / 1.2
        for i in range(3):
            r = rng(seed, i)
            px = size * (0.5 + i * 0.45 + u * 0.6)
            py = -size * u * (0.4 + 0.3 * r.random())
            cr.arc(px, py, size * (0.28 + 0.4 * u) * (0.8 + 0.4 * r.random()), 0, TAU)
            fill(cr, "#8d877d", 0.55 * (1 - u) ** 1.5)
    if age < 0.13:
        k = 1 - age / 0.13
        glow(cr, size * 0.4, 0, size * 1.6 * k + 1, "fire", 0.55 * k)
        for c, f in (("alert", 1.0), ("fire", 0.72), ("white", 0.4)):
            pts = []
            n = 7
            for i in range(n * 2):
                a = -0.9 + 1.8 * i / (n * 2 - 1)
                rr = size * f * k * (1.25 if i % 2 == 0 else 0.5) * (1.4 if abs(a) < 0.2 else 1.0)
                pts.append((rr * math.cos(a), rr * math.sin(a) * 0.8))
            poly(cr, [(0, -size * 0.18 * f)] + pts + [(0, size * 0.18 * f)])
            fill(cr, c)
    cr.restore()


def smoke(cr, x, y, t, height=420.0, width=90.0, color="#a59c84", alpha=0.95, wind=0.35, rate=5.0, life=4.0,
          seed=0, dark=False, soft=False, line=True):
    """A drifting column of flat poster smoke puffs rising from (x, y): one flat tone with a key line round the
    whole cloud and halftone undersides; loops forever, deterministic in t. Puffs grow, then shrink away (no fades).
    wind = sideways drift per unit of rise (+ is right). dark=True for black oil smoke. (soft is ignored.)"""
    if dark:
        color = "#3b3633"
    n = max(1, int(rate * life))
    puffs = []
    for k in range(n):
        r = rng(seed, k)
        age = (t + k / rate + r.random() * 0.2) % life
        u = age / life
        rise = height * (u ** 0.8)
        px = x + wind * rise + noise(t * 0.6 + k, seed + k) * width * 0.15 * u
        py = y - rise
        env = min(1.0, u * 8) * (1 - smooth(seg(u, 0.72, 1.0)))
        rad = width * (0.5 + 0.9 * u) * (0.75 + 0.5 * r.random()) * env
        if rad > 0.5:
            puffs.append((py, px, rad))
    if not puffs:
        return
    puffs.sort()
    klw = abs(cr.device_to_user_distance(3.0, 0)[0]) or 3.0
    cr.push_group()
    if line:
        for py, px, rad in puffs:
            cr.new_sub_path()
            cr.arc(px, py, rad, 0, TAU)
        ink(cr, klw * 2, "ink")
    for py, px, rad in puffs:                               # the shadow tone over the whole cloud, dotted
        cr.new_sub_path()
        cr.arc(px, py, rad, 0, TAU)
    fill(cr, shade(color, -0.22), keep=True)
    dots(cr, shade(color, -0.5), 2, 1.0)
    cr.new_path()
    for py, px, rad in puffs:                               # the lit tone, nudged up-wind: hard shadow crescents
        cr.new_sub_path()
        cr.arc(px - rad * 0.1, py - rad * 0.14, rad * 0.9, 0, TAU)
    fill(cr, color)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)


def fire(cr, x, y, t, size=60.0, seed=0, alpha=1.0):
    """Flickering flames standing on (x, y), about 2*size tall, with a glow and rising embers."""
    glow(cr, x, y - size * 0.6, size * 2.2, "fire", 0.35 * alpha)
    for layer, (c, f) in enumerate((("alert", 1.0), ("fire", 0.72), ("gold", 0.42))):
        for i in range(5):
            r = rng(seed, layer, i)
            off = (i - 2) * size * 0.32 * f
            h = size * f * (1.3 + 0.7 * r.random()) * (1 + 0.28 * noise(t * 3.2, seed * 7 + i + layer))
            w = size * 0.32 * f
            sway = noise(t * 2.5, seed + i * 3) * size * 0.18
            cr.move_to(x + off - w, y)
            cr.curve_to(x + off - w, y - h * 0.5, x + off + sway - w * 0.3, y - h * 0.7, x + off + sway, y - h)
            cr.curve_to(x + off + sway + w * 0.3, y - h * 0.7, x + off + w, y - h * 0.5, x + off + w, y)
            cr.close_path()
            fill(cr, c, alpha)
    for i in range(6):
        r = rng(seed, "ember", i)
        u = (t * 0.8 + r.random()) % 1.0
        ex = x + (r.random() - 0.5) * size + noise(t + i, seed) * size * 0.3
        ey = y - size * (0.6 + 2.6 * u)
        cr.arc(ex, ey, max(1.0, size * 0.04), 0, TAU)
        fill(cr, "gold", alpha * (1 - u))


def beam(cr, x, y, angle, length=1600.0, width=110.0, color="cream", alpha=0.45):
    """A searchlight beam from (x, y) along `angle` (radians, 0 = right, -pi/2 = straight up): two flat
    translucent wedges (a wide one and a bright core), poster style."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    poly(cr, [(0, -width * 0.12), (length, -width / 2), (length, width / 2), (0, width * 0.12)])
    fill(cr, color, alpha * 0.55)
    poly(cr, [(0, -width * 0.06), (length, -width * 0.2), (length, width * 0.2), (0, width * 0.06)])
    fill(cr, color, alpha * 0.6)
    cr.restore()


def signal_flash(cr, x, y, t, start=0.0, pattern="... --- ...", unit=0.12, size=26.0, color="#fff4c8"):
    """A signal lamp blinking Morse at (x, y) from `start` (dot = 1 unit, dash = 3, gaps of 1 and 3), looping."""
    seq = []
    for ch in pattern:
        if ch == ".":
            seq += [(1, True), (1, False)]
        elif ch == "-":
            seq += [(3, True), (1, False)]
        else:
            seq += [(2, False)]
    total = sum(d for d, _ in seq) * unit
    if t < start or total <= 0:
        return False
    p = (t - start) % (total + 6 * unit)
    acc = 0.0
    on = False
    for d, state in seq:
        if acc <= p < acc + d * unit:
            on = state
            break
        acc += d * unit
    if on:
        glow(cr, x, y, size * 3.2, color, 0.7)
        cr.arc(x, y, size * 0.5, 0, TAU)
        fill(cr, "white")
    return on


def explosion(cr, x, y, age, size=1.0, seed=0, smoke_life=2.6):
    """Flash, fireball, shock ring and a smoke puff (no debris, no gore). age = seconds since the blast."""
    if age is None or age < 0 or age > smoke_life + 0.5:
        return
    s = 120.0 * size
    u = clamp01((age - 0.05) / smoke_life)
    if 0 < u < 1:                                        # flat smoke cloud: rises, grows, then shrinks away
        puffs = []
        for i in range(7):
            r = rng(seed, "s", i)
            a = TAU * i / 7 + r.random()
            d = s * (0.3 + 0.5 * ease_out(u)) * (0.6 + 0.6 * r.random())
            rad = s * (0.35 + 0.55 * ease_out(u)) * (0.7 + 0.5 * r.random()) * (1 - smooth(seg(u, 0.6, 1.0)))
            puffs.append((x + math.cos(a) * d, y - s * 0.3 - s * 1.1 * ease_out(u) + math.sin(a) * d * 0.5, rad))
        klw = abs(cr.device_to_user_distance(3.0, 0)[0]) or 3.0
        for pass_ in ("line", "fill"):
            for px, py, rad in puffs:
                cr.new_sub_path()
                cr.arc(px, py, max(rad, 0.1), 0, TAU)
            ink(cr, klw * 2, "ink") if pass_ == "line" else fill(cr, "#8a8170")
        for px, py, rad in puffs:
            cr.new_path()
            cr.arc(px, py, max(rad, 0.1), 0, TAU)
            dots(cr, "#4f4740", 2, 1.0, below=py)
        cr.new_path()
    if age < 0.55:                                       # shock ring
        u = age / 0.55
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.45)
        cr.arc(0, 0, s * (0.3 + 2.0 * ease_out(u)), 0, TAU)
        cr.restore()
        ink(cr, s * 0.07 * (1 - u) + 0.5, "ink_soft", 0.7 * (1 - u))
    if age < 0.4:                                        # fireball
        u = age / 0.4
        k = back_out(clamp01(age / 0.08)) * (1 - ease_in(u) * 0.6)
        glow(cr, x, y - s * 0.25, s * 2.4 * k + 1, "fire", 0.55 * (1 - u))
        klw = abs(cr.device_to_user_distance(3.0, 0)[0]) or 3.0
        for c, f in (("alert", 1.0), ("fire", 0.74), ("gold", 0.48)):
            pts = []
            for i in range(14):
                r = rng(seed, "f", i)
                a = TAU * i / 14
                rr = s * f * k * ((1.0 if i % 2 == 0 else 0.62) + 0.2 * r.random())
                pts.append((x + rr * math.cos(a), y - s * 0.25 + rr * math.sin(a) * 0.85))
            poly(cr, pts)
            if c == "alert":
                fill_ink(cr, c, klw * 1.6, tone=False)
            else:
                fill(cr, c)
    if age < 0.09:                                       # white flash
        glow(cr, x, y - s * 0.2, s * 3.2, "white", 0.9 * (1 - age / 0.09))


def snowfall(cr, t, density=180, wind=40.0, seed=3, w=W, h=H, size=4.0, alpha=0.9):
    """Flakes falling over the whole frame (screen coordinates), looping seamlessly."""
    for i in range(density):
        r = rng(seed, i)
        depth = 0.4 + 0.6 * r.random()
        v = 60 + 90 * depth
        x0, y0 = r.random() * (w + 200) - 100, r.random() * (h + 40)
        y = (y0 + v * t) % (h + 40) - 20
        x = (x0 + wind * depth * t + math.sin(t * (0.8 + r.random()) + i) * 12) % (w + 200) - 100
        cr.arc(x, y, size * depth, 0, TAU)
        fill(cr, "snow", alpha * depth)


# ================================================================ base class
def _flatten(cr, o):
    """Close the group pushed by draw(): as a one-tone silhouette (o["silhouette"] = colour) or faded by alpha."""
    pat = cr.pop_group()
    if o.get("silhouette"):
        cr.set_source_rgba(*rgba(o["silhouette"], o["alpha"]))
        cr.mask(pat)
    else:
        cr.set_source(pat)
        cr.paint_with_alpha(o["alpha"])


class Prop:
    """Base: stores placement + options; draw() applies x, y, scale, facing and alpha, then calls _draw().
    silhouette="ink" (any colour) draws the whole prop as one flat poster silhouette."""
    defaults = {}

    def __init__(self, x=0.0, y=0.0, scale=1.0, facing=1, side=None, alpha=1.0, seed=0, **kw):
        self.o = dict(self.defaults)
        self.o.update(x=x, y=y, scale=scale, facing=facing, alpha=alpha, seed=seed)
        self.o["side"] = side or self.defaults.get("side", "allies")     # an explicit side beats the class default
        self.o.update(kw)

    def opts(self, kw):
        o = dict(self.o)
        o.update(kw)
        if "mark" not in kw and "mark" not in self.o:
            o["mark"] = mark_for(o["side"])
        o["body"] = o.get("color") or SIDE.get(o["side"], o["side"])
        return o

    def draw(self, cr, t, **kw):
        o = self.opts(kw)
        if o["alpha"] <= 0:
            return
        cr.save()
        cr.translate(o["x"], o["y"])
        cr.scale(o["scale"] * (1 if o["facing"] >= 0 else -1), o["scale"])
        self.lw = max(INK, MIN_PX / max(o["scale"], 1e-3))
        group = o["alpha"] < 1 or o.get("silhouette")
        if group:
            cr.push_group()
        self._draw(cr, t, o)
        if group:
            _flatten(cr, o)
        cr.restore()

    def _draw(self, cr, t, o):
        raise NotImplementedError


# ---------------------------------------------------------------- shared vehicle parts
def wheel(cr, x, y, r, spin, lw, tire="#3b3631", hub="#8a8478", spokes=5):
    cr.arc(x, y, r, 0, TAU)
    fill_ink(cr, tire, lw)
    cr.arc(x, y, r * 0.62, 0, TAU)
    fill_ink(cr, hub, lw * 0.6)
    for i in range(spokes):
        a = spin + TAU * i / spokes
        line(cr, x, y, x + math.cos(a) * r * 0.58, y + math.sin(a) * r * 0.58, lw * 0.45)
    cr.arc(x, y, r * 0.16, 0, TAU)
    fill(cr, "ink")


def propeller(cr, x, y, r, spin, lw, blades=3, color="ink"):
    """A spinning propeller seen from the side: a faint disc plus blades foreshortened by their angle."""
    ellipse(cr, x, y, r * 0.12, r)
    fill(cr, "white", 0.22, keep=True)
    ink(cr, lw * 0.35, "ink", 0.35)
    for i in range(blades):
        a = spin + TAU * i / blades
        ey = -r * math.cos(a)
        ex = r * 0.1 * math.sin(a)
        line(cr, x, y, x + ex, y + ey, lw * 0.9, color, 0.85)
    ellipse(cr, x + r * 0.04, y, r * 0.16, r * 0.2)
    fill_ink(cr, "ink_soft", lw * 0.5)


def barrels(cr, px, py, ang, elev, length, thick, n, kick, fill_c, lw, spacing=None):
    """Gun barrels from pivot (px, py), turret angle `ang` (deg; 0 forward, +90 at the camera), elevation `elev` (deg).
    Returns the muzzle points and whether they point at the camera."""
    a, e = math.radians(ang), math.radians(elev)
    vx, vy = math.cos(e) * math.cos(a), -math.sin(e)
    lat = -math.sin(a)
    spacing = spacing if spacing is not None else thick * 1.7
    tips = []
    L = length * (1 - 0.18 * kick)
    for i in range(n):
        off = (i - (n - 1) / 2) * spacing * lat
        x0, y0 = px + off, py
        x1, y1 = x0 + vx * L, y0 + vy * L
        line(cr, x0, y0, x1, y1, thick + lw * 1.4)
        line(cr, x0, y0, x1, y1, thick, fill_c)
        cr.arc(x1, y1, thick * 0.55, 0, TAU)
        fill_ink(cr, shade(fill_c, -0.35), lw * 0.5)
        tips.append((x0 + vx * length, y0 + vy * length))
    return tips, (vx, vy)


# ================================================================ LAND
class Tank(Prop):
    """Side-view tank, ~400 long, ~200 tall. draw(t, speed=0 px/s, turret=0 deg, elev=4 deg, fire=[...],
    snow=False, exhaust=True)."""
    defaults = dict(speed=0.0, turret=0.0, elev=4.0, fire=(), snow=False, exhaust=True, dist=None)

    def _draw(self, cr, t, o):
        lw = self.lw
        body = o["body"]
        moving = abs(o["speed"]) > 1
        dist = o["dist"] if o["dist"] is not None else o["speed"] * t
        age = since(t, o["fire"])
        kick = recoil(age)
        cr.translate(-6 * kick, 0)
        bob = math.sin(t * 24 + o["seed"]) * 1.4 if moving else math.sin(t * 2 + o["seed"]) * 0.4
        if o["exhaust"] and moving:
            smoke(cr, -200, -110, t, height=120, width=18, alpha=0.4, wind=-1.2, rate=6, life=1.2, seed=o["seed"])
        # tracks
        rrect(cr, -195, -74, 390, 74, 36)
        fill_ink(cr, "#3b3631", lw)
        for i, wx in enumerate((-150, -90, -30, 30, 90, 150)):
            wheel(cr, wx, -30, 25, dist / 25 + i, lw * 0.7, tire="#55504a", hub="#8a8478")
        wheel(cr, 172, -44, 20, dist / 20, lw * 0.6, tire="#55504a")
        wheel(cr, -172, -44, 20, dist / 20, lw * 0.6, tire="#55504a")
        rrect(cr, -195, -74, 390, 74, 36)
        cr.set_dash([10, 9], -dist)
        ink(cr, lw * 1.3, "#8a8478")
        cr.set_dash([])
        cr.translate(0, bob)
        # hull
        poly(cr, [(-190, -72), (-200, -112), (-150, -126), (150, -126), (206, -100), (190, -72)])
        fill_ink(cr, body, lw)
        line(cr, -186, -84, 192, -84, lw * 0.5, shade(body, -0.35))
        poly(cr, [(-150, -126), (150, -126), (160, -120), (-160, -120)])
        fill(cr, shade(body, 0.18))
        if o["snow"]:
            rrect(cr, -150, -134, 300, 12, 6)
            fill_ink(cr, "snow", lw * 0.6)
        # turret (pivot at its front-centre)
        a = math.radians(o["turret"])
        ca, sa = math.cos(a), math.sin(a)
        tw = 70 * abs(ca) + 52 * abs(sa)
        fx = 1 if ca >= 0 else -1
        ty = -126
        tur = [(-tw, ty), (-tw + 8, ty - 58), (tw - 22 * fx * 0.5 - 6, ty - 62), (tw + 14 * fx * 0.3, ty - 30), (tw, ty)]
        if fx < 0:
            tur = [(-x, y) for x, y in tur]
        behind = sa < -0.05
        pivot = (tw * 0.55 * ca, ty - 34)
        tips = vec = None
        if behind:
            tips, vec = barrels(cr, pivot[0], pivot[1], o["turret"], o["elev"], 175, 15, 1, kick, body, lw)
        poly(cr, tur)
        fill_ink(cr, body, lw)
        poly(cr, [(-tw + 8, ty - 58), (tw - 10, ty - 62), (tw - 4, ty - 54), (-tw + 10, ty - 50)])
        fill(cr, shade(body, 0.18))
        rrect(cr, -28, ty - 80, 46, 22, 8)                       # cupola
        fill_ink(cr, body, lw * 0.8)
        if o["snow"]:
            rrect(cr, -tw + 6, ty - 68, tw * 2 - 20, 10, 5)
            fill_ink(cr, "snow", lw * 0.5)
        draw_mark(cr, o["mark"], -tw * 0.25, ty - 28, 17, lw * 0.5)
        if not behind:
            tips, vec = barrels(cr, pivot[0], pivot[1], o["turret"], o["elev"], 175, 15, 1, kick, body, lw)
        if age is not None and age < 1.2:
            ang = math.atan2(vec[1], vec[0]) if abs(vec[0]) > 0.15 else (-math.pi / 2 if vec[1] < 0 else 0.0)
            muzzle_flash(cr, tips[0][0], tips[0][1], age, 60, ang, seed=o["seed"])


class Artillery(Prop):
    """A field gun: spoked wheels, shield, trail on the ground. draw(t, elev=24, fire=[...], speed=0)."""
    defaults = dict(elev=24.0, fire=(), speed=0.0)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        age = since(t, o["fire"])
        kick = recoil(age)
        poly(cr, [(-10, -60), (-210, -6), (-200, 4), (0, -44)])          # trail
        fill_ink(cr, shade(body, -0.15), lw)
        cr.save()
        cr.translate(-14 * kick, 4 * kick)
        tips, vec = barrels(cr, 6, -78, 0, o["elev"], 220, 16, 1, kick, body, lw)
        rrect(cr, -30, -96, 70, 36, 10)                                  # breech/cradle
        fill_ink(cr, body, lw)
        cr.restore()
        poly(cr, [(10, -150), (34, -150), (40, -40), (14, -40)])         # shield
        fill_ink(cr, body, lw)
        wheel(cr, 0, -55, 55, o["speed"] * t / 55, lw * 0.8, tire="#55504a", hub=shade(body, 0.1), spokes=10)
        if age is not None and age < 1.2:
            muzzle_flash(cr, tips[0][0], tips[0][1], age, 80, math.atan2(vec[1], vec[0]), seed=o["seed"])


class Truck(Prop):
    """An army truck with a canvas-covered bed, ~360 long. draw(t, speed=0, cover=True)."""
    defaults = dict(speed=0.0, cover=True)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        moving = abs(o["speed"]) > 1
        if moving:
            smoke(cr, -185, -40, t, height=80, width=12, alpha=0.35, wind=-1.5, rate=6, life=1.0, seed=o["seed"])
        dist = o["speed"] * t
        bob = math.sin(t * 20 + o["seed"]) * 1.6 if moving else 0
        cr.save()
        cr.translate(0, bob)
        poly(cr, [(-180, -50), (180, -50), (180, -70), (-180, -70)])      # chassis
        fill_ink(cr, shade(body, -0.25), lw)
        poly(cr, [(70, -70), (70, -168), (135, -168), (160, -120), (182, -116), (184, -70)])   # cab
        fill_ink(cr, body, lw)
        poly(cr, [(84, -150), (128, -150), (146, -118), (84, -118)])
        fill_ink(cr, "#c9d6d6", lw * 0.6)
        cr.arc(176, -96, 7, 0, TAU)
        fill_ink(cr, "gold", lw * 0.4)
        if o["cover"]:
            cr.move_to(-182, -70)
            cr.line_to(-182, -160)
            cr.curve_to(-182, -192, -150, -196, -120, -196)
            cr.line_to(30, -196)
            cr.curve_to(58, -196, 62, -180, 62, -160)
            cr.line_to(62, -70)
            cr.close_path()
            fill_ink(cr, shade(body, 0.22), lw)
            for rx in (-130, -70, -10):
                line(cr, rx, -190, rx, -74, lw * 0.4, shade(body, -0.1))
        else:
            rrect(cr, -182, -110, 244, 40, 4)
            fill_ink(cr, shade(body, 0.1), lw)
        draw_mark(cr, o["mark"], 104, -95, 13, lw * 0.4)
        cr.restore()
        for wx in (-120, -60, 120):
            wheel(cr, wx, -30, 30, dist / 30, lw * 0.7, tire="#3b3631", hub="#8a8478", spokes=6)


class Sandbags(Prop):
    """A wall of sandbags standing on y, `length` long, `rows` high. Static (bags vary a little)."""
    defaults = dict(length=300.0, rows=3, color="#cdb98f")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.8
        bw, bh = 62.0, 30.0
        n = max(1, int(o["length"] // (bw * 0.86)))
        for row in range(o["rows"]):
            cols = n - row
            x0 = -(cols - 1) * bw * 0.86 / 2
            for i in range(cols):
                r = rng(o["seed"], row, i)
                x = x0 + i * bw * 0.86 + r.uniform(-3, 3)
                y = -bh / 2 - row * bh * 0.82 + r.uniform(-1.5, 1.5)
                rrect(cr, x - bw / 2, y - bh / 2, bw, bh, bh * 0.45)
                fill_ink(cr, shade(o["color"], r.uniform(-0.08, 0.06)), lw)
                line(cr, x - bw * 0.25, y - 2, x + bw * 0.2, y - 4, lw * 0.4, "ink_soft", 0.6)


class Trench(Prop):
    """A trench cut-away: the ground line at y, a dug channel `width` wide and `depth` deep with plank walls,
    duckboards and sandbags on the parapet. Figures stand at y + depth - 14 inside it."""
    defaults = dict(width=420.0, depth=170.0, extent=900.0, earth="#9a8466", ground="#b5a27e")

    def _draw(self, cr, t, o):
        lw, w, d, e = self.lw, o["width"], o["depth"], o["extent"]
        poly(cr, [(-e, 0), (-w / 2, 0), (-w / 2 + 12, d), (w / 2 - 12, d), (w / 2, 0), (e, 0), (e, d + 140), (-e, d + 140)])
        fill(cr, o["earth"])
        poly(cr, [(-e, 0), (-w / 2, 0), (-w / 2 + 12, d), (w / 2 - 12, d), (w / 2, 0), (e, 0)], close=False)
        ink(cr, lw)
        rrect(cr, -e, -6, e - w / 2, 12, 6)
        fill(cr, o["ground"])
        rrect(cr, w / 2, -6, e - w / 2, 12, 6)
        fill(cr, o["ground"])
        for side in (-1, 1):                                             # plank revetment and posts
            x = side * (w / 2 - 6)
            for k in range(5):
                yy = 14 + k * (d - 20) / 5
                line(cr, x - side * (k * 2.4), yy, x - side * (k * 2.4 + 2.4), yy + (d - 20) / 5 - 6, lw * 1.6,
                     "#7a5f45")
            line(cr, x, 0, x - side * 12, d, lw * 0.7)
        for i in range(int(w // 46)):                                    # duckboards
            x = -w / 2 + 26 + i * 46
            rrect(cr, x - 18, d - 12, 36, 10, 2)
            fill_ink(cr, "#a07f5a", lw * 0.5)
        sb = Sandbags(length=min(260, e - w / 2 - 10), rows=2, seed=o["seed"])
        sb.draw(cr, t, x=-w / 2 - 130, y=-4, scale=0.8)
        sb.draw(cr, t, x=w / 2 + 130, y=-4, scale=0.8, seed=o["seed"] + 1)


class BarbedWire(Prop):
    """Barbed-wire coil on X stakes along `length`, swaying a little in the wind."""
    defaults = dict(length=500.0, height=90.0, wind=1.0)

    def _draw(self, cr, t, o):
        lw = self.lw
        L, hgt = o["length"], o["height"]
        n = max(2, int(L // 160) + 1)
        for i in range(n):
            x = -L / 2 + i * L / (n - 1)
            line(cr, x - 22, 0, x + 18, -hgt - 10, lw * 0.9, "#6b5440")
            line(cr, x + 22, 0, x - 18, -hgt - 10, lw * 0.9, "#6b5440")
        loops = int(L // 38)
        pts = []
        for i in range(loops * 16 + 1):
            u = i / 16
            a = u * TAU
            sway = math.sin(t * 1.6 * o["wind"] + u * 0.6 + o["seed"]) * 3
            pts.append((-L / 2 + u * 38 + math.sin(a) * 16, -hgt / 2 - math.cos(a) * hgt / 2 + sway))
        poly(cr, pts, close=False)
        ink(cr, lw * 0.45, "ink_soft")
        for i in range(0, len(pts), 6):
            x, y = pts[i]
            line(cr, x - 5, y - 5, x + 5, y + 5, lw * 0.35, "ink_soft")


class RadarTower(Prop):
    """A tall lattice radar mast (~560) with a hut; rings pulse out from the top. draw(t, pulse=True, period=1.1,
    ring="allies", reach=700)."""
    defaults = dict(pulse=True, period=1.1, ring=None, reach=700.0, height=560.0)

    def _draw(self, cr, t, o):
        lw, h = self.lw, o["height"]
        ring = o["ring"] or o["body"]
        if o["pulse"]:
            for k in range(4):
                u = ((t / o["period"]) + k / 4) % 1.0
                r = 30 + u * o["reach"]
                cr.arc(0, -h, r, -math.pi * 0.95, -math.pi * 0.05)
                ink(cr, lw * (1.2 - u * 0.7), ring, 0.75 * (1 - u) ** 1.3)
        base = 70
        for s in (-1, 1):
            line(cr, s * base, 0, s * 14, -h, lw)
        k = 0
        y = 0.0
        while y > -h + 30:                                               # lattice
            y1 = y - 60
            w0 = lerp(base, 14, -y / h)
            w1 = lerp(base, 14, -y1 / h)
            line(cr, -w0, y, w1, y1, lw * 0.5)
            line(cr, w0, y, -w1, y1, lw * 0.5)
            line(cr, -w1, y1, w1, y1, lw * 0.6)
            y = y1
            k += 1
        rrect(cr, -60, -h - 14, 120, 14, 4)                              # aerial bar
        fill_ink(cr, o["body"], lw * 0.7)
        cr.arc(0, -h - 7, 7 + 3 * (0.5 + 0.5 * math.sin(t * TAU / o["period"])), 0, TAU)
        fill(cr, "alert")
        rrect(cr, base + 20, -70, 140, 70, 4)                            # hut
        fill_ink(cr, "#a89a80", lw)
        poly(cr, [(base + 10, -70), (base + 90, -102), (base + 170, -70)])
        fill_ink(cr, "#7a6a55", lw)
        rrect(cr, base + 110, -46, 30, 26, 2)
        fill_ink(cr, "#e8d79a", lw * 0.5)


class Searchlight(Prop):
    """A searchlight drum on a stand with its beam. draw(t, aim=60 deg up from horizontal, sweep=0 deg,
    sweep_speed=0.4, on=True, length=1800)."""
    defaults = dict(aim=60.0, sweep=0.0, sweep_speed=0.4, on=True, length=1800.0, beam_w=130.0, beam_alpha=0.42)

    def _draw(self, cr, t, o):
        lw = self.lw
        aim = math.radians(o["aim"] + o["sweep"] * math.sin(t * o["sweep_speed"] * TAU + o["seed"]))
        ang = -aim
        if o["on"]:
            beam(cr, 0, -70, ang, o["length"], o["beam_w"], alpha=o["beam_alpha"])
        poly(cr, [(-50, 0), (-20, -60), (20, -60), (50, 0)])
        fill_ink(cr, "#6b665e", lw)
        cr.save()
        cr.translate(0, -70)
        cr.rotate(ang)
        rrect(cr, -40, -32, 70, 64, 10)
        fill_ink(cr, o["body"], lw)
        ellipse(cr, 32, 0, 10, 32)
        fill_ink(cr, "#fff4c8" if o["on"] else "#b9b4a6", lw * 0.7)
        cr.restore()
        if o["on"]:
            glow(cr, math.cos(ang) * 32, -70 + math.sin(ang) * 32, 60, "#fff4c8", 0.6)


# ================================================================ AIR
class Fighter(Prop):
    """A single-engine fighter, side view, ~260 long, centred on (x, y). draw(t, rpm=18 rev/s, bank=0 deg
    (shows the wing planform), pitch=0 deg (+ nose up), gear=False, trail=False (damage smoke))."""
    defaults = dict(rpm=18.0, bank=0.0, pitch=0.0, gear=False, trail=False)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        cr.rotate(-math.radians(o["pitch"]) + math.radians(o["bank"]) * 0.12)
        if o["trail"]:
            smoke(cr, -120, 0, t, height=260, width=22, alpha=0.5, wind=-4.0, rate=10, life=1.0, seed=o["seed"])
        span = abs(math.sin(math.radians(o["bank"])))
        self._wing(cr, 10, -4, -span, body, lw, o)                       # far wing (above), behind the fuselage
        line(cr, -122, -6, -40, -10, lw * 0.4)
        poly(cr, [(-140, -18), (-150, -62), (-118, -60), (-96, -16)])    # fin
        fill_ink(cr, body, lw)
        cr.move_to(118, -14)                                             # fuselage
        cr.curve_to(110, -36, 40, -40, 0, -36)
        cr.curve_to(-60, -30, -110, -24, -142, -16)
        cr.line_to(-142, -4)
        cr.curve_to(-100, 6, -40, 16, 0, 16)
        cr.curve_to(60, 16, 110, 12, 118, 4)
        cr.close_path()
        fill_ink(cr, body, lw)
        cr.move_to(110, -18)
        cr.curve_to(60, -32, 0, -30, -140, -14)
        ink(cr, lw * 0.5, shade(body, 0.35))
        cr.move_to(40, -36)                                              # canopy
        cr.curve_to(30, -62, -20, -62, -34, -34)
        cr.close_path()
        fill_ink(cr, "#c9d6d6", lw * 0.8)
        line(cr, 4, -58, 4, -36, lw * 0.4)
        poly(cr, [(-150, -16), (-96, -14), (-90, -6), (-150, -8)])       # tailplane
        fill_ink(cr, body, lw * 0.8)
        draw_mark(cr, o["mark"], -50, -10, 14, lw * 0.4)
        if o["gear"]:
            for gx in (30,):
                line(cr, gx, 10, gx + 8, 48, lw * 0.8)
                wheel(cr, gx + 8, 52, 12, 0, lw * 0.5)
        self._wing(cr, 10, 2, span, body, lw, o, mark=True)            # near wing (below), in front
        propeller(cr, 124, -6, 58, t * o["rpm"] * TAU, lw)
        rrect(cr, 112, -16, 18, 20, 8)
        fill_ink(cr, shade(body, -0.2), lw * 0.6)

    def _wing(self, cr, x, y, span, body, lw, o, mark=False):
        """One wing half: edge-on when level, its planform foreshortened by the bank (span < 0 = upward half)."""
        h = 130 * span
        if abs(h) < 10:
            if mark:
                rrect(cr, x - 56, y - 3, 112, 10, 5)
                fill_ink(cr, body, lw * 0.8)
            return
        poly(cr, [(x + 46, y), (x + 14, y + h), (x - 26, y + h), (x - 56, y)])
        fill_ink(cr, shade(body, 0.08 if span > 0 else -0.12), lw * 0.8)
        if mark:
            draw_mark(cr, o["mark"], x - 6, y + h * 0.62, 15 * min(1.0, abs(span) * 1.6 + 0.2), lw * 0.4)


class Bomber(Prop):
    """A multi-engine bomber, side view, ~480 long. draw(t, engines=2|4, rpm=14, bay=0..1 doors open,
    drop=[t...] bomb releases, bomb_drift=140 px/s backward, pitch=0)."""
    defaults = dict(engines=2, rpm=14.0, bay=0.0, drop=(), bomb_drift=140.0, pitch=0.0, trail=False)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        cr.rotate(-math.radians(o["pitch"]))
        for s in o["drop"] or ():                                        # bombs fall behind and under
            age = t - s
            for k in range(4):
                a = age - k * 0.12
                if 0 <= a < 3.0:
                    bx = -10 - o["bomb_drift"] * a - k * 4
                    by = 34 + 0.5 * 700 * a * a
                    ang = math.atan2(700 * a, o["bomb_drift"] + 60) if a > 0 else 0
                    cr.save()
                    cr.translate(bx, by)
                    cr.rotate(ang)
                    ellipse(cr, 0, 0, 16, 6)
                    fill_ink(cr, "#55504a", lw * 0.5)
                    line(cr, -16, -7, -16, 7, lw * 0.5)
                    cr.restore()
        if o["trail"]:
            smoke(cr, -40, 10, t, height=300, width=26, alpha=0.5, wind=-4.0, rate=10, life=1.0, seed=o["seed"])
        if o["engines"] >= 4:                                            # far engines first
            self._engine(cr, t, 70, -26, 0.85, body, lw, o)
        poly(cr, [(-226, -18), (-244, -112), (-196, -110), (-160, -14)])   # fin
        fill_ink(cr, body, lw)
        cr.move_to(232, -6)
        cr.curve_to(228, -40, 170, -46, 100, -44)
        cr.line_to(-180, -30)
        cr.curve_to(-220, -26, -236, -18, -246, -10)
        cr.line_to(-246, 2)
        cr.curve_to(-220, 8, -180, 14, -120, 20)
        cr.line_to(150, 26)
        cr.curve_to(200, 26, 228, 18, 232, -6)
        cr.close_path()
        fill_ink(cr, body, lw)
        cr.move_to(232, -6)                                              # glazed nose
        cr.curve_to(228, -34, 196, -40, 176, -40)
        cr.line_to(176, 18)
        cr.curve_to(206, 20, 228, 12, 232, -6)
        cr.close_path()
        fill_ink(cr, "#c9d6d6", lw * 0.7)
        for gx in (190, 210):
            line(cr, gx, -36, gx, 18, lw * 0.35)
        cr.move_to(150, -45)
        cr.curve_to(140, -66, 100, -66, 92, -44)
        fill_ink(cr, "#c9d6d6", lw * 0.7)
        for wx in (-40, 0, 40):
            cr.arc(wx, -18, 6, 0, TAU)
            fill_ink(cr, "#c9d6d6", lw * 0.4)
        poly(cr, [(-250, -14), (-180, -12), (-174, -2), (-250, -4)])
        fill_ink(cr, body, lw * 0.8)
        draw_mark(cr, o["mark"], -110, -2, 16, lw * 0.4)
        if o["bay"] > 0:                                                 # bomb-bay doors swing down
            for hx, sgn in ((-60, 1), (40, -1)):
                ang = sgn * o["bay"] * 1.2
                cr.save()
                cr.translate(hx, 24)
                cr.rotate(ang)
                rrect(cr, 0 if sgn > 0 else -50, -3, 50, 6, 3)
                fill_ink(cr, shade(body, -0.2), lw * 0.5)
                cr.restore()
        rrect(cr, -40, 6, 140, 14, 7)                                   # wing root (edge on)
        fill_ink(cr, body, lw * 0.8)
        self._engine(cr, t, 110, 6, 1.0, body, lw, o)
        if o["engines"] >= 4:
            self._engine(cr, t, 150, 10, 1.0, body, lw, o)

    def _engine(self, cr, t, x, y, k, body, lw, o):
        rrect(cr, x - 70 * k, y - 18 * k, 90 * k, 34 * k, 16 * k)
        fill_ink(cr, shade(body, -0.12 if k < 1 else 0.0), lw * 0.7)
        propeller(cr, x + 26 * k, y - 1, 52 * k, t * o["rpm"] * TAU + x, lw * 0.9)


class DiveBomber(Prop):
    """A dive bomber, side view, ~280 long, with gull wings and spatted gear (axis) or retracted gear (allies).
    draw(t, dive=0..1 (0 level, 1 = 70 deg nose-down with dive brakes out), release=None (bomb drops at t),
    rpm=18, pull_out=False)."""
    defaults = dict(dive=0.0, release=None, rpm=18.0, spats=None)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        dive = clamp01(o["dive"])
        cr.rotate(math.radians(70) * smooth(dive))
        spats = o["spats"] if o["spats"] is not None else o["side"] in ("germany", "italy", "axis", "japan")
        rel = o["release"]
        held = rel is None or t < rel
        poly(cr, [(-130, -16), (-140, -66), (-110, -64), (-88, -14)])
        fill_ink(cr, body, lw)
        cr.move_to(120, -12)
        cr.curve_to(112, -34, 40, -38, 0, -34)
        cr.curve_to(-60, -28, -110, -22, -136, -14)
        cr.line_to(-136, -2)
        cr.curve_to(-100, 6, -40, 16, 0, 16)
        cr.curve_to(60, 16, 112, 12, 120, 4)
        cr.close_path()
        fill_ink(cr, body, lw)
        cr.move_to(60, -34)                                              # long greenhouse canopy
        cr.curve_to(50, -60, -60, -60, -70, -30)
        cr.close_path()
        fill_ink(cr, "#c9d6d6", lw * 0.8)
        for gx in (30, 0, -30):
            line(cr, gx, -56, gx, -34, lw * 0.35)
        poly(cr, [(-142, -14), (-90, -12), (-84, -4), (-142, -6)])
        fill_ink(cr, body, lw * 0.8)
        draw_mark(cr, o["mark"], -60, -8, 13, lw * 0.4)
        if spats:
            for gx in (40,):
                line(cr, gx, 12, gx + 6, 46, lw * 1.6)
                line(cr, gx, 12, gx + 6, 46, lw * 0.8, body)
                ellipse(cr, gx + 8, 52, 20, 13)
                fill_ink(cr, body, lw * 0.7)
        cr.move_to(-30, 4)                                               # gull wing (cranked)
        cr.line_to(20, 22)
        cr.line_to(70, 8)
        ink(cr, lw * 2.6)
        cr.move_to(-30, 4)
        cr.line_to(20, 22)
        cr.line_to(70, 8)
        ink(cr, lw * 1.3, body)
        if dive > 0.3:                                                   # dive brakes out under the wing
            k = smooth(seg(dive, 0.3, 0.7))
            for bx in (-10, 30):
                rrect(cr, bx, 22, 26, 6 + 10 * k, 2)
                fill_ink(cr, shade(body, -0.25), lw * 0.4)
        if held:
            ellipse(cr, 10, 28, 30, 9)
            fill_ink(cr, "#55504a", lw * 0.6)
        else:
            a = t - rel
            if a < 3:
                bx, by = 10 + 60 * a, 30 + 0.5 * 500 * a * a
                cr.save()
                cr.translate(bx, by)
                cr.rotate(0.2 * a)
                ellipse(cr, 0, 0, 30, 9)
                fill_ink(cr, "#55504a", lw * 0.6)
                cr.restore()
        propeller(cr, 126, -4, 54, t * o["rpm"] * TAU, lw)
        rrect(cr, 114, -14, 18, 20, 8)
        fill_ink(cr, shade(body, -0.2), lw * 0.6)


class Parachute(Prop):
    """A parachute (canopy ~180 wide) with a soldier or a crate hanging under it; sways. (x, y) = the load.
    draw(t, open_at=None (canopy blooms from a streamer), load="man"|"crate", helmet=side colour)."""
    defaults = dict(open_at=None, load="man", canopy="#efe9da", sway=1.0)

    def _draw(self, cr, t, o):
        lw = self.lw
        u = 1.0 if o["open_at"] is None else back_out(seg(t, o["open_at"], o["open_at"] + 0.5))
        ang = math.sin(t * 1.3 + o["seed"]) * 0.12 * o["sway"]
        cr.rotate(ang)
        top = -260
        wdt = 180 * max(0.08, u) * (1 + 0.03 * math.sin(t * 3 + o["seed"]))
        hgt = 90 * max(0.3, u)
        for s in (-1, -0.45, 0.45, 1):                                   # shroud lines
            line(cr, 0, -40, s * wdt / 2, top + hgt * 0.15, lw * 0.3, "ink_soft")
        cr.move_to(-wdt / 2, top + hgt * 0.15)
        cr.curve_to(-wdt / 2, top - hgt, wdt / 2, top - hgt, wdt / 2, top + hgt * 0.15)
        n = 6
        for i in range(n, -1, -1):                                       # scalloped hem
            x0 = -wdt / 2 + wdt * i / n
            cr.line_to(x0, top + hgt * 0.15 - (8 if i % 2 else 0))
        cr.close_path()
        fill_ink(cr, o["canopy"], lw * 0.8)
        for i in range(1, n):
            x0 = -wdt / 2 + wdt * i / n
            cr.move_to(x0, top + hgt * 0.15)
            cr.curve_to(x0 * 0.9, top - hgt * 0.4, x0 * 0.4, top - hgt * 0.75, 0, top - hgt * 0.75)
            ink(cr, lw * 0.3, "ink_soft", 0.6)
        if o["load"] == "crate":
            rrect(cr, -30, -40, 60, 50, 4)
            fill_ink(cr, "#a07f5a", lw * 0.8)
            line(cr, -30, -15, 30, -15, lw * 0.4)
        else:                                                            # a little stand-in figure
            line(cr, 0, -26, 0, 20, lw * 1.2)
            line(cr, 0, -14, -18, -40, lw * 1.1)
            line(cr, 0, -14, 18, -40, lw * 1.1)
            line(cr, 0, 20, -10, 52 + 4 * math.sin(t * 2), lw * 1.1)
            line(cr, 0, 20, 12, 50 - 4 * math.sin(t * 2), lw * 1.1)
            cr.arc(0, -44, 15, 0, TAU)
            fill_ink(cr, "paper", lw * 0.8)
            cr.arc(0, -48, 16, math.pi, TAU)
            cr.close_path()
            fill_ink(cr, o["body"], lw * 0.7)


# ================================================================ SEA
class Ship(Prop):
    """Base for ships: bob and roll, wake and bow wave from speed, and a waterline strip over the hull bottom."""
    defaults = dict(speed=0.0, water="sea", bob=1.0, length=600.0, list_=0.0, crowd=0)

    def draw(self, cr, t, **kw):
        o = self.opts(kw)
        if o["alpha"] <= 0:
            return
        cr.save()
        cr.translate(o["x"], o["y"])
        sc = o["scale"]
        cr.scale(sc * (1 if o["facing"] >= 0 else -1), sc)
        self.lw = max(INK, MIN_PX / max(sc, 1e-3))
        L = o["length"]
        per = 2.2 + L / 900
        dy = math.sin(t * TAU / per + o["seed"]) * (3 + L / 200) * o["bob"]
        roll = math.sin(t * TAU / (per * 1.3) + o["seed"] * 1.7) * 0.012 * o["bob"] * 600 / max(L, 150)
        if o["alpha"] < 1:
            cr.push_group()
        self._wake(cr, t, o, L)
        if o.get("silhouette"):
            cr.push_group()
        cr.save()
        cr.translate(0, dy)
        cr.rotate(roll + o["list_"])
        self._draw(cr, t, o)
        cr.restore()
        if o.get("silhouette"):
            _flatten(cr, dict(o, alpha=1.0))
        if o["water"]:
            self._waterline(cr, t, o, L)
        self._bow(cr, t, o, L)
        if o["alpha"] < 1:
            cr.pop_group_to_source()
            cr.paint_with_alpha(o["alpha"])
        cr.restore()

    def _waterline(self, cr, t, o, L):
        x0, x1 = -L / 2 - 12, L / 2 + 12
        pts = []
        n = 24
        for i in range(n + 1):
            x = lerp(x0, x1, i / n)
            pts.append((x, 6 + math.sin(x * 0.05 + t * 3 + o["seed"]) * 3))
        poly(cr, pts + [(x1, 22), (x0, 22)])
        fill(cr, o["water"])
        poly(cr, pts, close=False)
        ink(cr, self.lw * 0.5, "white", 0.8)

    def _wake(self, cr, t, o, L):
        sp = o["speed"]
        if sp <= 1:
            return
        k = min(1.0, sp / 200)
        stern = -L / 2
        tail = (L * 0.9 + 220) * k
        poly(cr, [(stern + 10, 3), (stern - tail, 9), (stern - tail * 0.7, 13), (stern + 10, 16)])
        fill(cr, "cream", 0.9)
        for j in range(5):                                   # flat foam dashes sliding back along the wake
            u = ((t * sp / 160) + j / 5) % 1.0
            x = stern - 30 - u * tail
            w = 50 * k * (1 - u * 0.6)
            poly(cr, [(x - w, 18 + 6 * u), (x + w * 0.6, 17 + 6 * u), (x + w, 20 + 6 * u), (x - w * 0.6, 21 + 6 * u)])
            fill(cr, "cream", 0.85)

    def _bow(self, cr, t, o, L):
        sp = o["speed"]
        if sp <= 1:
            return
        k = min(1.0, sp / 200)
        bow = L / 2
        h = (16 + 10 * math.sin(t * 9 + o["seed"])) * k
        poly(cr, [(bow - 50, 8), (bow + 6, 6 - h), (bow + 34 * k, 10), (bow - 10, 14)])
        fill_ink(cr, "cream", self.lw * 0.5, tone=False)

    def _crowd(self, cr, n, x0, x1, y, color, lw, t, seed):
        """A row of helmeted heads on deck (rescued soldiers)."""
        for i in range(n):
            x = lerp(x0, x1, (i + 0.5) / n)
            r = rng(seed, "c", i)
            yy = y + math.sin(t * 2 + i) * 0.8 - r.random() * 4
            cr.arc(x, yy, 10, 0, TAU)
            fill_ink(cr, "paper", lw * 0.5)
            cr.arc(x, yy - 3, 13, math.pi, TAU)
            cr.close_path()
            fill_ink(cr, color, lw * 0.5)


def _hull(cr, L, h_bow, h_stern, body, lw, sheer=0.0, deck="#b9b0a0", bow_rake=40):
    b, s = L / 2, -L / 2
    cr.move_to(s, -h_stern)
    cr.curve_to(s + L * 0.3, -h_stern + sheer, b - L * 0.3, -h_bow + sheer, b + bow_rake, -h_bow - 6)
    cr.line_to(b, 14)
    cr.line_to(s + 20, 14)
    cr.curve_to(s, 10, s - 6, -h_stern * 0.5, s, -h_stern)
    cr.close_path()
    fill_ink(cr, body, lw)
    line(cr, s + 10, 0, b - 6, 0, lw * 0.5, shade(body, -0.35))


class Battleship(Ship):
    """A battleship, ~760 long. draw(t, speed=0, turrets=(0, 0, 180) deg per turret (fore, fore, aft),
    elev=8, fire=[t...] all turrets fire, smoke=True)."""
    defaults = dict(Ship.defaults, length=760.0, turrets=(0.0, 0.0, 180.0), elev=8.0, fire=(), smoke=True)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        L = o["length"]
        if o["smoke"]:
            smoke(cr, -10, -260, t, height=260, width=36, alpha=0.5, wind=-1.6, rate=9, life=3.0, seed=o["seed"])
        _hull(cr, L, 62, 50, body, lw, sheer=8)
        age = since(t, o["fire"])
        kick = recoil(age)
        poly(cr, [(-150, -50), (-140, -110), (120, -112), (140, -56)])   # superstructure
        fill_ink(cr, shade(body, 0.12), lw)
        poly(cr, [(40, -112), (46, -190), (110, -186), (116, -112)])     # bridge tower
        fill_ink(cr, shade(body, 0.12), lw)
        rrect(cr, 44, -200, 70, 18, 4)
        fill_ink(cr, "#c9d6d6", lw * 0.6)
        line(cr, 80, -200, 80, -300, lw * 0.8)                           # mast
        line(cr, 60, -270, 100, -270, lw * 0.6)
        poly(cr, [(-40, -112), (-34, -250), (20, -250), (24, -112)])     # funnel
        fill_ink(cr, shade(body, -0.05), lw)
        rrect(cr, -38, -262, 60, 14, 4)
        fill_ink(cr, "#3b3631", lw * 0.6)
        draw_mark(cr, o["mark"], -80, -80, 15, lw * 0.4)
        spots = [(250, -64, 1.0), (170, -112, 1.05), (-240, -54, 1.0)]
        angs = list(o["turrets"]) + [180.0] * 3
        for i, (tx, ty, k) in enumerate(spots):
            if i >= len(o["turrets"]):
                break
            self._turret(cr, t, tx, ty, k, angs[i], o, age, kick, lw, body)

    def _turret(self, cr, t, tx, ty, k, ang, o, age, kick, lw, body):
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        tw = 54 * abs(ca) + 40 * abs(sa)
        behind = sa < -0.05
        draw_b = lambda: barrels(cr, tx + tw * 0.4 * ca, ty - 22 * k, ang, o["elev"], 130 * k, 11 * k, 2, kick,
                                 body, lw * 0.8, spacing=22 * k)
        res = draw_b() if behind else None
        poly(cr, [(tx - tw, ty), (tx - tw + 6, ty - 42 * k), (tx + tw - 6, ty - 42 * k), (tx + tw, ty)])
        fill_ink(cr, shade(body, 0.08), lw)
        if not behind:
            res = draw_b()
        tips, vec = res
        if age is not None and age < 1.2:
            angf = math.atan2(vec[1], vec[0]) if abs(vec[0]) > 0.15 else -math.pi / 2
            for (x, y) in tips:
                muzzle_flash(cr, x, y, age, 90 * k, angf, seed=o["seed"] + int(tx))


class Carrier(Ship):
    """An aircraft carrier, ~820 long: flat flight deck, island, parked planes. draw(t, speed=0, burn=0..1 (deck
    fires, smoke column, slight list), planes=4)."""
    defaults = dict(Ship.defaults, length=820.0, burn=0.0, planes=4)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        L = o["length"]
        burn = clamp01(o["burn"])
        b, s = L / 2, -L / 2
        cr.move_to(s + 40, -70)                                          # hull
        cr.line_to(b - 30, -70)
        cr.curve_to(b, -70, b + 20, -60, b + 30, -50)
        cr.line_to(b, 14)
        cr.line_to(s + 30, 14)
        cr.curve_to(s + 10, 10, s, -30, s + 40, -70)
        cr.close_path()
        fill_ink(cr, body, lw)
        line(cr, s + 30, 0, b - 6, 0, lw * 0.5, shade(body, -0.35))
        for i in range(10):
            rrect(cr, s + 80 + i * (L - 160) / 10, -56, 26, 12, 3)
            fill_ink(cr, shade(body, -0.3), lw * 0.4)
        rrect(cr, s - 20, -92, L + 70, 22, 4)                            # flight deck
        fill_ink(cr, "#9c8f7a", lw)
        cr.set_dash([28, 22])
        line(cr, s, -81, b + 30, -81, lw * 0.45, "white", 0.8)
        cr.set_dash([])
        poly(cr, [(60, -92), (66, -170), (150, -170), (160, -92)])      # island
        fill_ink(cr, shade(body, 0.12), lw)
        rrect(cr, 70, -184, 76, 16, 4)
        fill_ink(cr, "#c9d6d6", lw * 0.6)
        poly(cr, [(90, -170), (94, -220), (134, -220), (140, -170)])
        fill_ink(cr, shade(body, -0.05), lw)
        line(cr, 110, -220, 110, -280, lw * 0.7)
        line(cr, 92, -258, 128, -258, lw * 0.6)
        for i in range(int(o["planes"])):                                # parked planes (tiny side views)
            px = s + 70 + i * 90
            if px > 20:
                break
            Fighter(side=o["side"], mark=o.get("mark")).draw(cr, t, x=px, y=-112, scale=0.26, rpm=0)
        if burn > 0:
            for i, fx in enumerate((-260, -80, 220)):
                fire(cr, fx, -92, t, 60 * burn, seed=o["seed"] * 3 + i)
            smoke(cr, -80, -150, t, height=700 * burn, width=110 * burn, dark=True, alpha=0.8, wind=-0.6, rate=5,
                  life=3.5, seed=o["seed"])
            smoke(cr, 200, -150, t, height=500 * burn, width=80 * burn, dark=True, alpha=0.7, wind=-0.7, rate=4,
                  life=3.0, seed=o["seed"] + 9)
        draw_mark(cr, o["mark"], 110, -130, 14, lw * 0.4)


class Destroyer(Ship):
    """A destroyer, ~520 long, sleek, two funnels and small turrets. draw(t, speed=180, fire=[...], turrets=(0, 180))."""
    defaults = dict(Ship.defaults, length=520.0, speed=180.0, fire=(), turrets=(0.0, 180.0), elev=6.0, smoke=True)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        L = o["length"]
        if o["smoke"]:
            smoke(cr, -20, -150, t, height=200, width=26, alpha=0.45, wind=-2.2, rate=11, life=2.2, seed=o["seed"])
        _hull(cr, L, 48, 30, body, lw, sheer=10, bow_rake=50)
        poly(cr, [(-80, -36), (-70, -80), (100, -80), (110, -40)])
        fill_ink(cr, shade(body, 0.12), lw)
        poly(cr, [(60, -80), (64, -128), (110, -124), (114, -80)])
        fill_ink(cr, shade(body, 0.12), lw)
        rrect(cr, 62, -136, 50, 12, 3)
        fill_ink(cr, "#c9d6d6", lw * 0.5)
        line(cr, 86, -136, 86, -200, lw * 0.7)
        for fx in (-50, 0):
            poly(cr, [(fx - 14, -80), (fx - 10, -150), (fx + 16, -150), (fx + 20, -80)])
            fill_ink(cr, shade(body, -0.05), lw)
        draw_mark(cr, o["mark"], -120, -18, 11, lw * 0.4)
        age = since(t, o["fire"])
        kick = recoil(age)
        for (tx, ty), ang in zip(((180, -42), (-190, -32)), o["turrets"]):
            a = math.radians(ang)
            tips, vec = barrels(cr, tx + 20 * math.cos(a), ty - 16, ang, o["elev"], 70, 8, 1, kick, body, lw * 0.7)
            rrect(cr, tx - 26, ty - 30, 52, 30, 8)
            fill_ink(cr, shade(body, 0.08), lw * 0.8)
            if age is not None and age < 1.2:
                muzzle_flash(cr, tips[0][0], tips[0][1], age, 50, math.atan2(vec[1], vec[0]), seed=o["seed"] + tx)


class FishingBoat(Ship):
    """A small fishing boat, ~200 long: wheelhouse, mast, nets. draw(t, speed=60, crowd=0)."""
    defaults = dict(Ship.defaults, length=200.0, speed=60.0, color="#8b5e3c", trim="#d8c9a3")

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["color"]
        cr.move_to(-100, -40)
        cr.curve_to(-40, -34, 40, -40, 110, -58)
        cr.line_to(84, 12)
        cr.line_to(-86, 12)
        cr.curve_to(-100, 0, -104, -20, -100, -40)
        cr.close_path()
        fill_ink(cr, body, lw)
        line(cr, -98, -30, 104, -46, lw * 0.6, o["trim"])
        line(cr, 30, -44, 30, -200, lw * 0.8)                            # mast + furled sail
        poly(cr, [(30, -190), (-40, -60), (30, -64)])
        fill_ink(cr, "#c9a77a", lw * 0.6)
        rrect(cr, -70, -96, 60, 56, 4)                                   # wheelhouse
        fill_ink(cr, "#e8dcc0", lw * 0.8)
        rrect(cr, -60, -86, 22, 18, 2)
        fill_ink(cr, "#c9d6d6", lw * 0.4)
        line(cr, -70, -98, -6, -98, lw * 1.2, "#7a2f25")
        if o["crowd"]:
            self._crowd(cr, int(o["crowd"]), -4, 96, -56, SIDE["britain"], lw, t, o["seed"])


class Yacht(Ship):
    """A small pleasure motor yacht (~180 long) with a cabin; sail=True gives a sailing yacht. draw(t, speed=70, crowd=0)."""
    defaults = dict(Ship.defaults, length=180.0, speed=70.0, sail=False, color="#f1ece0", trim="#3f6fb5")

    def _draw(self, cr, t, o):
        lw = self.lw
        cr.move_to(-90, -30)
        cr.line_to(70, -34)
        cr.curve_to(90, -36, 100, -40, 108, -46)
        cr.line_to(76, 12)
        cr.line_to(-80, 12)
        cr.curve_to(-92, 4, -94, -14, -90, -30)
        cr.close_path()
        fill_ink(cr, o["color"], lw)
        line(cr, -88, -20, 96, -30, lw * 0.6, o["trim"])
        if o["sail"]:
            line(cr, 0, -34, 0, -230, lw * 0.7)
            poly(cr, [(4, -226), (4, -40), (80, -44)])
            fill_ink(cr, "white", lw * 0.6)
            poly(cr, [(-4, -210), (-4, -40), (-70, -40)])
            fill_ink(cr, "white", lw * 0.6)
        else:
            cr.move_to(-60, -32)
            cr.line_to(-56, -70)
            cr.line_to(30, -70)
            cr.line_to(50, -34)
            cr.close_path()
            fill_ink(cr, "#e2d6bb", lw * 0.8)
            for wx in (-40, -10, 18):
                rrect(cr, wx, -62, 20, 16, 4)
                fill_ink(cr, "#c9d6d6", lw * 0.4)
            line(cr, -70, -32, -70, -60, lw * 0.5)
            poly(cr, [(-70, -60), (-100, -54), (-70, -48)])
            fill(cr, "allies")
        if o["crowd"]:
            self._crowd(cr, int(o["crowd"]), -80 if o["sail"] else 54, 90 if o["sail"] else 96, -46, SIDE["britain"],
                        lw, t, o["seed"])


class PaddleFerry(Ship):
    """A paddle steamer ferry, ~380 long: paddle box with turning paddles, a tall funnel. draw(t, speed=70, crowd=0)."""
    defaults = dict(Ship.defaults, length=380.0, speed=70.0, color="#2f2b28", upper="#f1ece0", funnel="#c4892f")

    def _draw(self, cr, t, o):
        lw = self.lw
        smoke(cr, -10, -190, t, height=180, width=28, alpha=0.5, wind=-1.8, rate=10, life=2.2, seed=o["seed"])
        _hull(cr, 380, 44, 40, o["color"], lw, sheer=4, bow_rake=24)
        rrect(cr, -150, -80, 270, 38, 4)                                 # saloon deck
        fill_ink(cr, o["upper"], lw)
        for i in range(9):
            rrect(cr, -140 + i * 29, -72, 16, 16, 3)
            fill_ink(cr, "#c9d6d6", lw * 0.35)
        line(cr, -150, -98, 120, -98, lw * 0.5)                          # rail
        for i in range(10):
            line(cr, -150 + i * 30, -98, -150 + i * 30, -80, lw * 0.35)
        poly(cr, [(-26, -80), (-22, -176), (14, -176), (18, -80)])       # funnel
        fill_ink(cr, o["funnel"], lw)
        rrect(cr, -24, -188, 40, 14, 3)
        fill_ink(cr, "#2f2b28", lw * 0.5)
        spin = o["speed"] * t / 40
        cr.arc(-10, -6, 62, math.pi, TAU)                                # paddle box
        cr.close_path()
        fill_ink(cr, o["upper"], lw)
        for i in range(8):
            a = math.pi + math.pi * i / 7
            line(cr, -10, -6, -10 + math.cos(a) * 58, -6 + math.sin(a) * 58, lw * 0.3, "ink_soft")
        for i in range(6):
            a = spin + TAU * i / 6
            if math.sin(a) > 0.1:
                line(cr, -10 + math.cos(a) * 30, -6 + math.sin(a) * 30, -10 + math.cos(a) * 64,
                     -6 + math.sin(a) * 64, lw * 1.2, "#6b5440")
        if o["crowd"]:
            self._crowd(cr, int(o["crowd"]), -140, 120, -110, SIDE["britain"], lw, t, o["seed"])


class Submarine(Ship):
    """A U-boat-style submarine, ~460 long. depth 0 = surfaced, 1 = submerged with only the periscope showing.
    draw(t, depth=0, periscope=True, scope_turn=0 (0..1 turns the head round), speed=60)."""
    defaults = dict(Ship.defaults, length=460.0, depth=0.0, periscope=True, scope_turn=0.0, speed=60.0, bob=0.6)

    def _draw(self, cr, t, o):
        lw, body = self.lw, o["body"]
        d = clamp01(o["depth"])
        cr.save()
        cr.rectangle(-2000, -2000, 4000, 2000 + 4)                       # only what is above the waterline
        cr.clip()
        cr.translate(0, d * 150)
        cr.move_to(-230, -6)
        cr.curve_to(-120, -30, 120, -34, 220, -16)
        cr.curve_to(240, -12, 240, 4, 220, 8)
        cr.curve_to(100, 18, -120, 16, -230, 6)
        cr.close_path()
        fill_ink(cr, body, lw)
        poly(cr, [(-60, -30), (-50, -96), (40, -96), (60, -30)])         # conning tower
        fill_ink(cr, body, lw)
        line(cr, -50, -80, 40, -80, lw * 0.4, shade(body, 0.3))
        if o["periscope"]:
            ph = 110 + 60 * d
            line(cr, 0, -96, 0, -96 - ph, lw * 1.2)
            sgn = 1 if math.cos(o["scope_turn"] * math.pi) >= 0 else -1
            rrect(cr, -6 if sgn > 0 else -20, -96 - ph - 10, 26, 14, 4)
            fill_ink(cr, shade(body, -0.1), lw * 0.6)
            cr.arc(14 * sgn, -96 - ph - 3, 3, 0, TAU)
            fill(cr, "#c9d6d6")
        line(cr, 120, -26, 150, -40, lw * 1.0)                           # deck gun
        rrect(cr, 104, -36, 24, 12, 3)
        fill_ink(cr, body, lw * 0.6)
        draw_mark(cr, o["mark"], -100, -12, 12, lw * 0.4)
        cr.restore()
        if d > 0.6 and o["periscope"]:                                   # feather of foam at the scope
            k = (d - 0.6) / 0.4
            ph = 110 + 60 * d
            if -96 - ph + d * 150 < 0:
                for j in range(4):
                    u = (t * 1.5 + j / 4) % 1.0
                    ellipse(cr, -10 - u * 70, 2, 10 + 30 * u, 4 + 3 * u)
                    ink(cr, lw * 0.5, "white", 0.8 * (1 - u) * k)


class Periscope(Submarine):
    """Just the periscope breaking the surface (a submerged Submarine)."""
    defaults = dict(Submarine.defaults, depth=1.0, bob=0.2)


# ================================================================ SMALL PROPS
class Telegram(Prop):
    """A telegram form (~240 x 170), centred on (x, y), fluttering. draw(t, lines=("WAR DECLARED", ...),
    flutter=1.0, header="TELEGRAM")."""
    defaults = dict(lines=(), flutter=1.0, header="TELEGRAM")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.7
        f = o["flutter"]
        cr.rotate(math.sin(t * 5 + o["seed"]) * 0.05 * f)
        cr.scale(1, 1 - 0.06 * f * (0.5 + 0.5 * math.sin(t * 7 + o["seed"])))
        rrect(cr, -120, -85, 240, 170, 4)
        fill_ink(cr, "#f4ecd2", lw)
        rrect(cr, -120, -85, 240, 34, 4)
        fill(cr, "#e6c76a")
        text(cr, o["header"], 0, -58, 24, font=TITLE, color="ink", bold=False, spacing=3)
        if o["lines"]:
            for i, s in enumerate(o["lines"][:4]):
                text(cr, s, -104, -16 + i * 30, 20, font=HAND, color="ink", align="left")
        else:
            for i in range(4):
                r = rng(o["seed"], i)
                line(cr, -100, -14 + i * 26, -100 + 120 + r.random() * 80, -14 + i * 26, lw * 0.9, "ink_soft")


class SigningTable(Prop):
    """A table with a cloth, a document, an inkwell and a pen; `signed` 0..1 writes the signature with the pen.
    (x, y) = floor point under the table centre. Table ~420 wide, ~150 tall."""
    defaults = dict(signed=0.0, cloth="#5f7a5a")

    def _draw(self, cr, t, o):
        lw = self.lw
        for lx in (-180, 180):
            line(cr, lx, -150, lx, 0, lw * 1.4, "#6b4e3a")
        poly(cr, [(-215, -150), (215, -150), (230, -70), (-230, -70)])
        fill_ink(cr, o["cloth"], lw)
        poly(cr, [(-210, -150), (210, -150), (204, -166), (-204, -166)])
        fill_ink(cr, shade(o["cloth"], 0.15), lw)
        poly(cr, [(-70, -152), (80, -152), (70, -166), (-62, -166)])     # paper (top, foreshortened)
        fill_ink(cr, "#fbf8ef", lw * 0.6)
        for i in range(3):
            line(cr, -50 + i * 4, -155 - i * 3.5, 40 - i * 4, -155 - i * 3.5, lw * 0.3, "ink_soft")
        rrect(cr, 120, -186, 30, 22, 5)                                  # inkwell
        fill_ink(cr, "#2f2b28", lw * 0.6)
        u = clamp01(o["signed"])
        pts = []
        n = 40
        for i in range(int(n * u) + 1):
            s = i / n
            pts.append((-40 + 90 * s, -158 + math.sin(s * 22) * 3 - s * 2))
        if len(pts) > 1:
            poly(cr, pts, close=False)
            ink(cr, lw * 0.35, "#1f3c7a")
        px, py = pts[-1] if u > 0 else (135, -186)
        line(cr, px, py, px + 26, py - 46, lw * 0.9, "#2f2b28")


class RailwayCarriage(Prop):
    """A dark-wood railway carriage (~620 long) on two bogies; (x, y) = rail level under its centre.
    draw(t, speed=0 (wheels turn), lit=False (warm windows), age="1918"|"1940" (slightly paler in 1918))."""
    defaults = dict(speed=0.0, lit=False, wood="#6b4e3a", era="1940")

    def _draw(self, cr, t, o):
        lw = self.lw
        wood = o["wood"] if o["era"] != "1918" else shade(o["wood"], 0.18)
        line(cr, -380, 2, 380, 2, lw * 0.9, "ink_soft")
        dist = o["speed"] * t
        for bx in (-210, 210):
            rrect(cr, bx - 80, -48, 160, 20, 6)
            fill_ink(cr, "#3b3631", lw * 0.8)
            for wx in (-46, 46):
                wheel(cr, bx + wx, -20, 22, dist / 22, lw * 0.6, tire="#3b3631", hub="#8a8478", spokes=6)
        rrect(cr, -310, -230, 620, 180, 10)
        fill_ink(cr, wood, lw)
        cr.move_to(-318, -226)
        cr.curve_to(-300, -262, 300, -262, 318, -226)
        cr.close_path()
        fill_ink(cr, shade(wood, -0.3), lw)
        for i in range(8):
            x = -270 + i * 70
            rrect(cr, x, -204, 48, 58, 6)
            fill_ink(cr, "#f2d38a" if o["lit"] else "#c9d6d6", lw * 0.5)
            if o["lit"]:
                glow(cr, x + 24, -175, 50, "#f2d38a", 0.3)
        line(cr, -300, -120, 300, -120, lw * 0.5, shade(wood, 0.25))
        line(cr, -300, -86, 300, -86, lw * 0.5, shade(wood, 0.25))
        for dx in (-318, 300):
            rrect(cr, dx, -200, 18, 150, 3)
            fill_ink(cr, shade(wood, -0.15), lw * 0.6)


class Locomotive(Prop):
    """A steam locomotive, ~460 long, facing right; (x, y) = rail level. draw(t, speed=0, steam=True)."""
    defaults = dict(speed=0.0, steam=True, color="#2f2b28", trim="#b8382e")

    def _draw(self, cr, t, o):
        lw = self.lw
        dist = o["speed"] * t
        if o["steam"]:
            smoke(cr, 150, -250, t, height=240, width=36, color="#d9d3c6", alpha=0.75,
                  wind=-2.0 if o["speed"] > 1 else 0.1, rate=6, life=2.0, seed=o["seed"])
        line(cr, -260, 2, 260, 2, lw * 0.9, "ink_soft")
        rrect(cr, -220, -70, 430, 26, 4)
        fill_ink(cr, o["trim"], lw * 0.8)
        rrect(cr, -60, -180, 250, 110, 50)                               # boiler
        fill_ink(cr, o["color"], lw)
        rrect(cr, -220, -230, 150, 160, 6)                               # cab
        fill_ink(cr, o["color"], lw)
        rrect(cr, -196, -206, 50, 50, 6)
        fill_ink(cr, "#c9d6d6", lw * 0.5)
        rrect(cr, -232, -244, 174, 18, 6)
        fill_ink(cr, shade(o["color"], 0.2), lw * 0.7)
        poly(cr, [(136, -180), (130, -244), (170, -244), (164, -180)])   # chimney
        fill_ink(cr, o["color"], lw)
        cr.arc(40, -184, 22, math.pi, TAU)
        fill_ink(cr, "gold", lw * 0.6)
        poly(cr, [(210, -44), (250, 0), (190, 0)])                       # cow-catcher
        fill_ink(cr, o["trim"], lw * 0.7)
        for wx in (-150, -40, 70):
            wheel(cr, wx, -40, 40 if wx > -150 else 30, dist / 40, lw * 0.7, tire="#3b3631", hub=o["trim"], spokes=8)
        a = dist / 40
        line(cr, -40 + math.cos(a) * 22, -40 + math.sin(a) * 22, 70 + math.cos(a) * 22, -40 + math.sin(a) * 22,
             lw * 1.0, "#8a8478")


class Radio(Prop):
    """A 1940s arched cabinet radio (~220 x 260); (x, y) = its base centre. draw(t, on=True (dial glows, sound rings))."""
    defaults = dict(on=True, wood="#7a5236")

    def _draw(self, cr, t, o):
        lw = self.lw
        if o["on"]:
            for k in range(3):
                u = (t * 0.9 + k / 3) % 1.0
                for s in (-1, 1):
                    a0 = 0.0 if s > 0 else math.pi
                    cr.new_sub_path()
                    cr.arc(0, -150, 140 + 160 * u, a0 - 0.35, a0 + 0.35)
                    ink(cr, lw * 0.6, "ink_soft", 0.6 * (1 - u))
        cr.move_to(-110, 0)
        cr.line_to(-110, -170)
        cr.curve_to(-110, -270, 110, -270, 110, -170)
        cr.line_to(110, 0)
        cr.close_path()
        fill_ink(cr, o["wood"], lw)
        cr.move_to(-80, -110)
        cr.line_to(-80, -170)
        cr.curve_to(-80, -235, 80, -235, 80, -170)
        cr.line_to(80, -110)
        cr.close_path()
        fill_ink(cr, "#c8b48a", lw * 0.7)
        for i in range(7):
            x = -66 + i * 22
            line(cr, x, -116, x, -170 - 40 * (1 - abs(x) / 90), lw * 0.4, shade("#c8b48a", -0.3))
        rrect(cr, -60, -90, 120, 30, 6)
        fill_ink(cr, "#f2d38a" if o["on"] else "#d8cfb6", lw * 0.6)
        if o["on"]:
            glow(cr, 0, -75, 70, "#f2d38a", 0.45)
        nx = -40 + 80 * (0.5 + 0.1 * math.sin(t * 0.7))
        line(cr, nx, -88, nx, -62, lw * 0.4, "alert")
        for kx in (-60, 0, 60):
            cr.arc(kx, -30, 13, 0, TAU)
            fill_ink(cr, "#3b3631", lw * 0.5)


class Enigma(Prop):
    """An Enigma-style cipher machine in an open wooden box (~420 x 300, seen from the front/above); (x, y) = the
    box's front-bottom centre. draw(t, auto=True presses keys every `beat` s and lights a scrambled lamp,
    lit="Q" lights one lamp, step=0 rotor step)."""
    defaults = dict(auto=True, lit=None, step=0, beat=0.32, wood="#6b4e3a")
    ROWS = ("QWERTZUIO", "ASDFGHJK", "PYXCVBNML")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.8
        poly(cr, [(-210, 0), (210, 0), (190, -300), (-190, -300)])
        fill_ink(cr, o["wood"], lw * 1.2)
        poly(cr, [(-186, -14), (186, -14), (170, -286), (-170, -286)])
        fill_ink(cr, "#2f2b28", lw)
        k = int(t / o["beat"]) if o["auto"] else 0
        u = (t / o["beat"]) % 1.0 if o["auto"] else 1.0
        r = rng(o["seed"], k)
        letters = "".join(self.ROWS)
        press = r.choice(letters) if o["auto"] else None
        lit = o["lit"] or (r.choice([c for c in letters if c != press]) if o["auto"] and u < 0.75 else None)
        step = o["step"] + k
        for i in range(3):                                               # rotors with letter windows
            x = -60 + i * 60
            rrect(cr, x - 20, -282, 40, 34, 4)
            fill_ink(cr, "#d8cfb6", lw * 0.6)
            ch = chr(65 + (step // (26 ** (2 - i)) + i * 7) % 26)
            text(cr, ch, x, -258, 22, font=TITLE, color="ink", bold=False)
            for j in range(5):
                line(cr, x + 22, -282 + j * 7, x + 30, -282 + j * 7, lw * 0.4, "#8a8478")
        for row, keys in enumerate(self.ROWS):                           # lampboard
            y = -224 + row * 30
            for j, ch in enumerate(keys):
                x = (j - (len(keys) - 1) / 2) * 34
                on = ch == lit
                if on:
                    glow(cr, x, y, 34, "#f6d36a", 0.85)
                cr.arc(x, y, 12, 0, TAU)
                fill_ink(cr, "#f6d36a" if on else "#5b544c", lw * 0.4)
                text(cr, ch, x, y + 5, 13, font=TITLE, color="ink" if on else "#cfc6b0", bold=False)
        for row, keys in enumerate(self.ROWS):                           # keyboard
            y = -120 + row * 36
            for j, ch in enumerate(keys):
                x = (j - (len(keys) - 1) / 2) * 38
                down = ch == press and u < 0.4
                dy = 4 if down else 0
                line(cr, x, y + dy, x, y + 14, lw * 0.6, "#8a8478")
                cr.arc(x, y + dy, 15, 0, TAU)
                fill_ink(cr, "#f1ece0", lw * 0.5)
                text(cr, ch, x, y + dy + 6, 15, font=TITLE, color="ink", bold=False)


class Candle(Prop):
    """A single candle in a holder with a flickering flame and glow; (x, y) = holder base. draw(t, burn=0..1
    (melts down), lit=True)."""
    defaults = dict(burn=0.0, lit=True, wax="#f1ece0")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.8
        h = 220 * (1 - 0.7 * clamp01(o["burn"]))
        if o["lit"]:
            fl = 1 + 0.08 * noise(t * 4, o["seed"])
            glow(cr, 0, -h - 60, 260 * fl, "#f6d36a", 0.35)
        ellipse(cr, 0, -8, 90, 18)
        fill_ink(cr, "#b08d4a", lw)
        rrect(cr, -36, -h - 30, 72, h, 8)
        fill_ink(cr, o["wax"], lw)
        cr.move_to(-36, -h - 22)
        cr.curve_to(-30, -h - 4, -20, -h - 6, -18, -h + 20)
        cr.curve_to(-14, -h + 26, -10, -h - 10, 0, -h - 22)
        ink(cr, lw * 0.5, "ink_soft", 0.6)
        line(cr, 0, -h - 30, 0, -h - 46, lw * 0.6)
        if o["lit"]:
            sway = noise(t * 3, o["seed"]) * 4
            fh = 58 * (1 + 0.12 * noise(t * 6, o["seed"] + 3))
            for c, k in (("fire", 1.0), ("gold", 0.7), ("white", 0.35)):
                cr.move_to(-12 * k, -h - 40)
                cr.curve_to(-14 * k, -h - 40 - fh * k * 0.5, sway, -h - 40 - fh * k * 0.8, sway, -h - 40 - fh * k)
                cr.curve_to(sway, -h - 40 - fh * k * 0.8, 14 * k, -h - 40 - fh * k * 0.5, 12 * k, -h - 40)
                cr.curve_to(8 * k, -h - 32, -8 * k, -h - 32, -12 * k, -h - 40)
                cr.close_path()
                fill(cr, c)


class Calendar(Prop):
    """A tear-off date calendar (~200 x 240); (x, y) = its centre. draw(t, date=("JUNE", "4", "1940"),
    prev=None (the page flipping away), flip_at=None, flip_dur=0.28)."""
    defaults = dict(date=("SEPT", "1", "1939"), prev=None, flip_at=None, flip_dur=0.28)

    def _page(self, cr, date, lw):
        rrect(cr, -100, -110, 200, 230, 6)
        fill_ink(cr, "#fbf8ef", lw)
        rrect(cr, -100, -110, 200, 56, 6)
        fill(cr, "alert")
        rrect(cr, -100, -110, 200, 230, 6)
        ink(cr, lw)
        text(cr, date[0], 0, -68, 36, font=TITLE, color="white", bold=False, spacing=2)
        text(cr, str(date[1]), 0, 64, 110, font=TITLE, color="ink", bold=False)
        if len(date) > 2:
            text(cr, str(date[2]), 0, 104, 28, font=TITLE, color="ink_soft", bold=False, spacing=2)

    def _draw(self, cr, t, o):
        lw = self.lw * 0.8
        rrect(cr, -112, -132, 224, 262, 8)
        fill_ink(cr, "#6b4e3a", lw)
        self._page(cr, o["date"], lw)
        for rx in (-60, 0, 60):
            cr.arc(rx, -118, 8, 0, TAU)
            fill_ink(cr, "#8a8478", lw * 0.5)
        if o["prev"] and o["flip_at"] is not None:
            u = seg(t, o["flip_at"], o["flip_at"] + o["flip_dur"])
            if u < 1:
                cr.save()
                cr.translate(0, -110)
                k = math.cos(ease_in(u) * math.pi)                       # page swings up over the top
                cr.scale(1, k if abs(k) > 0.02 else 0.02)
                cr.translate(0, 110)
                if k > 0:
                    self._page(cr, o["prev"], lw)
                else:
                    rrect(cr, -100, -110, 200, 230, 6)
                    fill_ink(cr, "#e9e2cf", lw)
                cr.restore()


# ================================================================ effect classes (same API as props)
class Explosion(Prop):
    """explosion() as a prop: Explosion(x, y, start=2.0, size=1.0).draw(cr, t)."""
    defaults = dict(start=0.0, size=1.0)

    def _draw(self, cr, t, o):
        explosion(cr, 0, 0, t - o["start"], o["size"], o["seed"])


class Smoke(Prop):
    """smoke() as a prop: Smoke(x, y, height=420, width=90, dark=False, wind=0.35).draw(cr, t)."""
    defaults = dict(height=420.0, width=90.0, dark=False, wind=0.35, smoke_alpha=0.75, rate=5.0, life=4.0)

    def _draw(self, cr, t, o):
        smoke(cr, 0, 0, t, o["height"], o["width"], alpha=o["smoke_alpha"], wind=o["wind"], rate=o["rate"],
              life=o["life"], seed=o["seed"], dark=o["dark"])


class Fire(Prop):
    """fire() as a prop: Fire(x, y, size=60).draw(cr, t)."""
    defaults = dict(size=60.0)

    def _draw(self, cr, t, o):
        fire(cr, 0, 0, t, o["size"], o["seed"])


class Snow:
    """Full-frame snowfall in screen coordinates: Snow(density=180, wind=40).draw(cr, t)."""

    def __init__(self, density=180, wind=40.0, seed=3, size=4.0, alpha=0.9):
        self.k = dict(density=density, wind=wind, seed=seed, size=size, alpha=alpha)

    def draw(self, cr, t, **kw):
        k = dict(self.k)
        k.update(kw)
        snowfall(cr, t, **k)


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "random")]


def _extend():
    """Re-export the SHOTLIST extras (things.py, fx.py, sets.py) so `from channels.ww2.kit.props import *` has all.
    (Import props first for that; importing fx or sets first still works, they just are not re-exported then.)"""
    import importlib
    for mod in ("things", "fx", "sets"):
        try:
            m = importlib.import_module("channels.ww2.kit." + mod)
        except ModuleNotFoundError as e:
            if e.name != "channels.ww2.kit." + mod:
                raise
            continue
        except ImportError:          # circular: that module is being imported first; it imports us, not vice versa
            continue
        for n in getattr(m, "__all__", ()):
            if n not in globals():
                globals()[n] = getattr(m, n)
                __all__.append(n)


_extend()


# ================================================================ contact sheet
def _sheet(t=1.3, out=None):
    import os
    from channels.ww2.kit.core import ROOT, paper, print_finish, render_clip

    def draw(cr, tt):
        paper(cr)
        cr.rectangle(0, 600, W, 480)
        fill(cr, "sea", 0.55)
        items = [
            (Tank(x=230, y=250, scale=0.55, side="germany"), dict(speed=120, turret=0, fire=[tt - 0.05])),
            (Tank(x=560, y=250, scale=0.55, side="soviet"), dict(turret=70, snow=True)),
            (Tank(x=880, y=250, scale=0.55, side="usa", facing=-1), dict(turret=150)),
            (Artillery(x=1180, y=250, scale=0.6, side="britain"), dict(fire=[tt - 0.06])),
            (Truck(x=1500, y=250, scale=0.55, side="usa"), dict(speed=100)),
            (Sandbags(x=1780, y=250, scale=0.6), {}),
            (Fighter(x=170, y=380, scale=0.6, side="britain"), dict(bank=35)),
            (Fighter(x=420, y=380, scale=0.6, side="germany", facing=-1), dict(bank=-25)),
            (Bomber(x=760, y=380, scale=0.5, side="usa"), dict(engines=4, bay=1, drop=[tt - 0.4])),
            (DiveBomber(x=1100, y=370, scale=0.55, side="germany"), dict(dive=0.6)),
            (Fighter(x=1340, y=380, scale=0.5, side="soviet"), {}),
            (Parachute(x=1560, y=520, scale=0.6, side="usa"), {}),
            (RadarTower(x=1780, y=560, scale=0.42, side="britain"), {}),
            (Trench(x=380, y=520, scale=0.5, extent=330), {}),
            (BarbedWire(x=860, y=560, scale=0.6), {}),
            (Searchlight(x=1130, y=575, scale=0.55, side="britain"), dict(length=500)),
            (Battleship(x=330, y=720, scale=0.45, side="germany"), dict(turrets=(40, 0, 180), fire=[tt - 0.04])),
            (Carrier(x=820, y=720, scale=0.42, side="japan"), dict(burn=0.8)),
            (Destroyer(x=1340, y=720, scale=0.5, side="britain"), {}),
            (Submarine(x=1720, y=720, scale=0.45, side="germany"), {}),
            (FishingBoat(x=120, y=860, scale=0.6), dict(crowd=5)),
            (Yacht(x=330, y=860, scale=0.6), dict(crowd=3)),
            (Yacht(x=520, y=860, scale=0.6), dict(sail=True)),
            (PaddleFerry(x=800, y=860, scale=0.5), dict(crowd=12)),
            (Periscope(x=1100, y=860, scale=0.5, side="germany"), {}),
            (RailwayCarriage(x=1500, y=880, scale=0.45), dict(lit=True)),
            (Telegram(x=140, y=990, scale=0.5), dict(lines=("BRITAIN AND", "FRANCE AT WAR"))),
            (SigningTable(x=400, y=1060, scale=0.45), dict(signed=0.7)),
            (Radio(x=600, y=1060, scale=0.4), {}),
            (Enigma(x=820, y=1060, scale=0.42), {}),
            (Candle(x=1000, y=1060, scale=0.42), {}),
            (Calendar(x=1160, y=990, scale=0.42), dict(date=("JUNE", "4", "1940"))),
            (Locomotive(x=1420, y=1060, scale=0.36), dict(speed=60)),
            (Explosion(x=1700, y=1000, scale=0.6), dict(start=tt - 0.15)),
        ]
        for p, kw in items:
            p.draw(cr, tt, **kw)
        roundel(cr, 1860, 980, 24)
        star(cr, 1860, 1040, 22, disc="#2f5596")
        signal_flash(cr, 1600, 600, tt, pattern="-")
        print_finish(cr, tt)

    out = out or os.path.join(ROOT, "out", "ww2", "style", "props_sheet.png")
    return render_clip(draw, 1, out, still=t)


if __name__ == "__main__":
    print(_sheet())
