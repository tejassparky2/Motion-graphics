"""WW2 kit: poster effects from SHOTLIST.md (flat shapes, key lines, halftone; no gradients, no gore).

All functions draw in the current coordinates and are pure functions of time, so frames render in any order.
`age` = seconds since the event started (negative or None = not yet).

    starburst(cr, x, y, age, size=1, seed=0)        flat layered star burst with a key line + short speed lines
    puff(cr, x, y, age, size=1, seed=0)             one rolling halftone smoke puff (rises, grows, shrinks away)
    cloud(cr, x, y, w, seed=0, color="cream")       a flat poster cloud silhouette (SKY layers)
    flash(cr, t, start, hold=0.08, fade=0.7)        full-frame white flash that fades back to the picture
    mud(cr, t, x0, x1, y, depth=120)                a churned mud band with ruts and puddles (vehicles sink into it)
    mud_splash(cr, x, y, age, size=1, seed=0)       flat clods thrown up by wheels or shells
    radar_rings(cr, x, y, t, period=1.1, reach=700) rings pulsing out of a mast top; blips(cr, pts, t, start)
    firework(cr, x, y, t, start, color, size=1)     rocket trail then a burst of sparks that fall and fade
    fireworks(cr, t, x0, x1, y0, y1, n=8, start=0)  a show of them over a skyline
    mushroom(cr, x, y, t, start, size=1)            the distant mushroom-cloud SILHOUETTE: far away, flat, non-graphic
Also re-exported from props.py: explosion, smoke, fire, snowfall/Snow, beam, signal_flash, muzzle_flash, glow,
and the Candle prop.
"""
import math
import random

from channels.ww2.kit.core import H, W, back_out, clamp01, ease_in, ease_out, lerp, seg, smooth
from channels.ww2.kit.props import (TAU, Candle, Snow, beam, dots, explosion, fill, fill_ink, fire, glow, ink,  # noqa: F401
                                    line, muzzle_flash, poly, rgba, rng, shade, signal_flash, smoke, snowfall)


def _klw(cr, px=3.0):
    return abs(cr.device_to_user_distance(px, 0)[0]) or px


def blob(cr, puffs, color, line_px=3.0, dense=2):
    """Draw a cloud made of circles [(x, y, r)] as one poster shape: key line round the union, a dotted shadow tone,
    then the lit tone nudged up-left (hard-edged shadow crescents)."""
    puffs = [p for p in puffs if p[2] > 0.3]
    if not puffs:
        return
    k = _klw(cr, line_px)
    for x, y, r in puffs:
        cr.new_sub_path()
        cr.arc(x, y, r, 0, TAU)
    ink(cr, k * 2)
    for x, y, r in puffs:
        cr.new_sub_path()
        cr.arc(x, y, r, 0, TAU)
    fill(cr, shade(color, -0.22), keep=True)
    if dense:
        dots(cr, shade(color, -0.5), dense, 1.0)
    cr.new_path()
    for x, y, r in puffs:
        cr.new_sub_path()
        cr.arc(x - r * 0.1, y - r * 0.14, r * 0.88, 0, TAU)
    fill(cr, color)


def starburst(cr, x, y, age, size=1.0, seed=0, life=0.55, lines=True, colors=("alert", "fire", "gold", "cream")):
    """A flat poster star burst (about 240*size across at its peak): pops with overshoot, holds, then collapses.
    Short ink/cream speed lines flick outward (never full-frame rays)."""
    if age is None or age < 0 or age > life:
        return
    u = age / life
    k = back_out(clamp01(age / 0.07), 2.4) * (1 - ease_in(seg(u, 0.55, 1.0)))
    s = 120.0 * size * k
    if s <= 0.5:
        return
    lw = _klw(cr, 3.5)
    if lines and u < 0.7:
        for i in range(12):
            r = rng(seed, "l", i)
            a = TAU * i / 12 + r.uniform(-0.12, 0.12)
            r0 = s * (1.15 + 0.6 * u)
            r1 = r0 + s * (0.35 + 0.3 * r.random()) * (1 - u)
            line(cr, x + math.cos(a) * r0, y + math.sin(a) * r0, x + math.cos(a) * r1, y + math.sin(a) * r1,
                 lw * (1.6 if i % 2 else 1.0), "ink" if i % 2 else "cream")
    for j, c in enumerate(colors):
        f = 1.0 - j * 0.22
        n = 9 + j
        pts = []
        for i in range(n * 2):
            r = rng(seed, j, i)
            a = TAU * i / (n * 2) + j * 0.3 + seed
            rr = s * f * ((1.0 if i % 2 == 0 else 0.5) + 0.18 * r.random())
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        poly(cr, pts)
        if j == 0:
            fill_ink(cr, c, lw * 1.4, tone=False)
        else:
            fill(cr, c)


def puff(cr, x, y, age, size=1.0, seed=0, life=2.4, color="#8a8170", rise=160.0):
    """One rolling halftone smoke puff (~150*size across): billows up from (x, y), grows, then shrinks away."""
    if age is None or age < 0 or age > life:
        return
    u = age / life
    g = ease_out(clamp01(u * 1.6)) * (1 - smooth(seg(u, 0.6, 1.0)))
    s = 75.0 * size
    puffs = []
    for i in range(6):
        r = rng(seed, "p", i)
        a = TAU * i / 6 + r.random()
        d = s * 0.55 * (0.6 + 0.6 * r.random())
        puffs.append((x + math.cos(a) * d, y - rise * size * ease_out(u) + math.sin(a) * d * 0.6,
                      s * (0.5 + 0.35 * r.random()) * g))
    puffs.append((x, y - rise * size * ease_out(u) - s * 0.3, s * 0.75 * g))
    blob(cr, puffs, color)


def cloud(cr, x, y, w=420.0, seed=0, color="cream", dense=1):
    """A flat poster cloud silhouette, w wide, sitting on y (flat underside)."""
    r = random.Random(seed)
    n = max(3, int(w / 90))
    puffs = []
    for i in range(n):
        u = (i + 0.5) / n
        rad = w * (0.12 + 0.1 * math.sin(u * math.pi)) * r.uniform(0.8, 1.2)
        puffs.append((x - w / 2 + u * w, y - rad * 0.6, rad))
    cr.save()
    cr.rectangle(x - w, y - w, w * 2, w)                                    # flat underside
    cr.clip()
    blob(cr, puffs, color, line_px=2.5, dense=dense)
    cr.restore()
    line(cr, x - w / 2 - w * 0.05, y, x + w / 2 + w * 0.05, y, _klw(cr, 5), "ink")


def flash(cr, t, start, hold=0.08, fade=0.7, color="white"):
    """A full-frame flash: snaps to `color` at `start`, holds, then fades back (screen space)."""
    if t < start:
        return
    a = 1.0 if t < start + hold else 1 - ease_out(seg(t, start + hold, start + hold + fade))
    if a <= 0:
        return
    cr.save()
    cr.identity_matrix()
    cr.rectangle(0, 0, W, H)
    fill(cr, color, a)
    cr.restore()


def mud(cr, t, x0, x1, y, depth=120.0, color="#5e4a33", seed=2):
    """A churned mud band from y down `depth`: a wavy dark surface, ruts, puddles with a sky glint."""
    r = random.Random(seed)
    n = 40
    top = []
    for i in range(n + 1):
        x = lerp(x0, x1, i / n)
        top.append((x, y + math.sin(x * 0.02 + seed) * 6 + r.uniform(-3, 3)))
    poly(cr, top + [(x1, y + depth), (x0, y + depth)])
    fill(cr, color, keep=True)
    dots(cr, shade(color, -0.35), 2, 1.0)
    cr.new_path()
    poly(cr, top, close=False)
    ink(cr, _klw(cr, 4))
    for i in range(6):                                                        # ruts
        yy = y + depth * (0.2 + 0.12 * i)
        xa = lerp(x0, x1, r.random() * 0.3)
        line(cr, xa, yy, xa + (x1 - x0) * r.uniform(0.4, 0.7), yy + r.uniform(-6, 6), _klw(cr, 3),
             shade(color, -0.4))
    for i in range(5):                                                        # puddles with a glint
        px = lerp(x0, x1, r.random())
        py = y + depth * r.uniform(0.25, 0.85)
        w = r.uniform(40, 110)
        cr.save()
        cr.translate(px, py)
        cr.scale(1, 0.22)
        cr.arc(0, 0, w, 0, TAU)
        cr.restore()
        fill_ink(cr, "#8d9488", _klw(cr, 2.5), tone=False)
        line(cr, px - w * 0.4, py - 2, px - w * 0.4 + w * 0.3 * (0.6 + 0.4 * math.sin(t * 2 + i)), py - 2,
             _klw(cr, 2.5), "cream")


def mud_splash(cr, x, y, age, size=1.0, seed=0, life=0.9, color="#5e4a33"):
    """Flat clods of mud thrown up from (x, y) and falling back (wheels spinning, a shell landing nearby)."""
    if age is None or age < 0 or age > life:
        return
    for i in range(9):
        r = rng(seed, "m", i)
        a = -math.pi / 2 + r.uniform(-0.9, 0.9)
        v = 420 * size * r.uniform(0.6, 1.1)
        px = x + math.cos(a) * v * age
        py = y + math.sin(a) * v * age + 0.5 * 1400 * size * age * age
        s = 14 * size * r.uniform(0.6, 1.3) * (1 - 0.5 * age / life)
        poly(cr, [(px - s, py), (px - s * 0.3, py - s * 0.9), (px + s * 0.8, py - s * 0.4), (px + s * 0.6, py + s * 0.6)])
        fill_ink(cr, color, _klw(cr, 2), tone=False)


def radar_rings(cr, x, y, t, period=1.1, reach=700.0, color="allies", n=4, a0=-math.pi * 0.95, a1=-math.pi * 0.05):
    """Rings pulsing out of a mast top at (x, y) (upper half by default), thinning and fading as they spread."""
    for k in range(n):
        u = ((t / period) + k / n) % 1.0
        cr.new_path()
        cr.arc(x, y, 30 + u * reach, a0, a1)
        ink(cr, _klw(cr, 6) * (1.2 - u * 0.8), color, 0.8 * (1 - u) ** 1.2)


def blips(cr, pts, t, start=0.0, step=0.25, color="alert", size=10.0):
    """Radar blips appearing one by one at pts (from `start`, every `step` s), each pinging once then holding."""
    for i, (x, y) in enumerate(pts):
        a = t - start - i * step
        if a < 0:
            continue
        p = back_out(clamp01(a / 0.2))
        cr.new_path()
        cr.arc(x, y, size * p, 0, TAU)
        fill_ink(cr, color, _klw(cr, 2), tone=False)
        if a < 0.6:
            cr.new_path()
            cr.arc(x, y, size * (1 + a * 6), 0, TAU)
            ink(cr, _klw(cr, 2), color, 1 - a / 0.6)


def firework(cr, x, y, t, start, color="gold", size=1.0, seed=0, rise=0.6, life=1.8):
    """A rocket climbs to (x, y) over `rise` s, then bursts into spark streaks that droop and fade."""
    a = t - start
    if a < 0 or a > rise + life:
        return
    lw = _klw(cr, 3)
    if a < rise:
        u = ease_out(a / rise)
        yy = lerp(y + 500 * size, y, u)
        line(cr, x, yy, x, yy + 60 * size * (1 - u * 0.5), lw, "cream", 0.9)
        return
    b = (a - rise) / life
    R = 170 * size * ease_out(clamp01(b * 2.2))
    drop = 120 * size * b * b
    fade = 1 - ease_in(b)
    if b < 0.12:
        cr.new_path()
        cr.arc(x, y, 30 * size * (1 - b / 0.12) + 1, 0, TAU)
        fill(cr, "cream")
    for i in range(16):
        r = rng(seed, "fw", i)
        ang = TAU * i / 16 + r.uniform(-0.1, 0.1)
        rr = R * r.uniform(0.8, 1.05)
        ex, ey = x + math.cos(ang) * rr, y + math.sin(ang) * rr + drop
        sx, sy = x + math.cos(ang) * rr * 0.55, y + math.sin(ang) * rr * 0.55 + drop * 0.6
        line(cr, sx, sy, ex, ey, lw * 1.2, color, fade)
        cr.new_path()
        cr.arc(ex, ey, lw * 1.6, 0, TAU)
        fill(cr, "cream", fade)


def fireworks(cr, t, x0, x1, y0, y1, n=8, start=0.0, every=0.45, seed=5,
              colors=("gold", "alert", "cream", "allies")):
    """A looping show: n rockets over the box, staggered `every` s from `start`."""
    r = random.Random(seed)
    for i in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        s = start + i * every
        period = n * every + 1.0
        sz = r.uniform(0.7, 1.2)
        if t < s:
            continue
        firework(cr, x, y, s + (t - s) % period, s, colors[i % len(colors)], sz, seed=seed + i)


def mushroom(cr, x, y, t, start, size=1.0, seed=7, color="#b3a88c", grow=4.0):
    """The DISTANT mushroom-cloud silhouette rising from the horizon point (x, y): a billowing column, a wide cap and
    a low base cloud, about 520*size tall when grown, all one flat poster shape. Kept small, pale and far away:
    no fire, no city detail."""
    a = t - start
    if a < 0:
        return
    u = ease_out(clamp01(a / grow))
    s = size
    top = 520 * s * u
    capr = 150 * s * (0.35 + 0.65 * u)
    puffs = []
    for i in range(7):                                                       # low base cloud
        r = rng(seed, "b", i)
        puffs.append((x + (i - 3) * 40 * s * (0.5 + 0.5 * u), y - 18 * s, 38 * s * (0.6 + 0.5 * u) * r.uniform(0.8, 1.2)))
    n = 16
    for i in range(n):                                                       # the column, widening as it climbs
        f = (i + 1) / (n + 1)
        r = rng(seed, "s", i)
        puffs.append((x + math.sin(i * 1.7 + t * 0.6) * 5 * s, y - top * f * 0.9,
                      40 * s * (0.8 + 0.25 * r.random()) * (0.75 + 0.5 * f)))
    for i in range(9):                                                       # the cap
        r = rng(seed, "c", i)
        ang = math.pi + math.pi * i / 8
        puffs.append((x + math.cos(ang) * capr * 0.8, y - top + math.sin(ang) * capr * 0.4 + capr * 0.2,
                      capr * (0.34 + 0.12 * r.random()) * (1 + 0.04 * math.sin(t * 1.3 + i))))
    puffs.append((x, y - top, capr * 0.62))
    blob(cr, puffs, color, line_px=3, dense=2)


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "random")]


def _sheet(t=1.3, out=None):
    """Contact sheet: out/ww2/style/props_sheet_3_fx.png."""
    import os
    from channels.ww2.kit.core import ROOT, paper, print_finish, render_clip
    from channels.ww2.kit.props import RadarTower

    def draw(cr, tt):
        paper(cr)
        starburst(cr, 200, 220, 0.12, 1.0)
        starburst(cr, 470, 220, 0.3, 0.7, seed=3)
        puff(cr, 720, 320, 0.9, 1.0)
        explosion(cr, 980, 300, 0.25, 0.9)
        cloud(cr, 1300, 300, 420, seed=1)
        cloud(cr, 1680, 260, 300, seed=4, color="sky")
        mud(cr, tt, 60, 760, 560, 140)
        mud_splash(cr, 400, 580, 0.25, 1.0)
        RadarTower(x=950, y=760, scale=0.4, side="britain", pulse=False).draw(cr, tt)
        radar_rings(cr, 950, 760 - 0.4 * 560, tt, reach=320)
        blips(cr, [(1180, 480), (1230, 520), (1150, 560)], tt, start=0.4)
        fireworks(cr, tt, 1350, 1850, 420, 600, n=5, start=0.0, every=0.25)
        mushroom(cr, 300, 1040, tt, start=tt - 3.0, size=0.6)
        smoke(cr, 640, 1040, tt, height=300, width=50, dark=True)
        fire(cr, 860, 1040, tt, 50)
        Candle().draw(cr, tt, x=1040, y=1050, scale=0.5)
        snowfall(cr, tt, density=60, w=600, h=400)
        flash(cr, tt, tt - 0.4, fade=0.7)
        cr.save()
        cr.rectangle(1200, 760, 680, 300)
        cr.clip()
        beam(cr, 1300, 1060, -1.1, 600, 120)
        signal_flash(cr, 1700, 900, tt, pattern="-", size=20)
        cr.restore()
        print_finish(cr, tt)

    out = out or os.path.join(ROOT, "out", "ww2", "style", "props_sheet_3_fx.png")
    return render_clip(draw, 1, out, still=t)


if __name__ == "__main__":
    print(_sheet())
