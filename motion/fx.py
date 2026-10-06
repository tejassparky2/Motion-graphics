"""More animation and more looks for the news Shorts (owner, 6 Oct 2026: "increase the quantity of animation and
styles"). Everything here works in screen space (720x1280); keep the main action between y 280 and 860 so the
headline band (top) and the captions (y ~915) stay clear.

- Transitions: transition(cr, t, start, kind) with kind in whip / zoom / slide / iris / flash.
- Camera feel: shake(), push() (slow zoom on a held shot), bob() (idle motion).
- Backgrounds: bg(cr, style, t) with sunburst / comic / blueprint / night / sky.
- Comic language: burst() starburst, speed_lines(), panel() that slides in with its own clip.
- Particles: swarm(), heat_waves(), mist(), sparkles(), sweat().
- Numbers: big_number() that counts up and lands with a pop.
"""
import math

from .engine import INK, RED, WHITE, W, H, at, blob, cue, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write

YELLOW = hexc("#ffd23f")
ORANGE = hexc("#ff8a3d")
NAVY = hexc("#1d2a55")
CREAM = hexc("#fbf3e1")


# ---------------------------------------------------------------- transitions
def transition(cr, t, start, kind="whip", dur=0.22):
    """Call at the top of a scene (after cr.save()). Each scene can use a different kind so cuts don't repeat."""
    if start <= 0 or t - start >= dur:
        return
    u = ease_out((t - start) / dur)
    if kind == "whip":
        cr.set_source_rgba(*INK)
        cr.paint()
        cr.translate(W * (1 - u), 0)
        cue("whoosh", t, start, 0.25)
    elif kind == "slide":   # the new scene slides up from below
        cr.set_source_rgba(*INK)
        cr.paint()
        cr.translate(0, H * (1 - u))
        cue("whoosh", t, start, 0.25)
    elif kind == "zoom":    # punch in from 1.35x
        z = 1.35 - 0.35 * u
        cr.translate(W / 2, H / 2)
        cr.scale(z, z)
        cr.translate(-W / 2, -H / 2)
        cue("hit", t, start)
    elif kind == "iris":    # circle opens from the centre
        cr.set_source_rgba(*INK)
        cr.paint()
        cr.arc(W / 2, H * 0.45, 40 + 900 * u, 0, 2 * math.pi)
        cr.clip()
        cue("pop", t, start)
    elif kind == "flash":   # white flash that fades (drawn after the scene by flash_over)
        pass


def flash_over(cr, t, start, dur=0.25):
    """White flash on top of a scene; call after drawing it."""
    if 0 < start <= t < start + dur:
        cr.save()
        cr.identity_matrix()
        cr.set_source_rgba(1, 1, 1, 0.85 * (1 - (t - start) / dur))
        cr.paint()
        cr.restore()


# ---------------------------------------------------------------- camera feel
def shake(cr, t, start, dur=0.35, amp=14):
    """Short decaying screen shake for an impact (call before drawing)."""
    if start <= t < start + dur:
        k = 1 - (t - start) / dur
        cr.translate(amp * k * math.sin(t * 90), amp * k * math.cos(t * 70))


def push(cr, t, start, rate=0.02, cx=W / 2, cy=H * 0.45):
    """Slow zoom-in on a held shot so nothing is ever frozen."""
    z = 1 + rate * max(0.0, t - start)
    cr.translate(cx, cy)
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def bob(t, speed=3.0, amp=6.0, phase=0.0):
    return amp * math.sin(t * speed + phase)


# ---------------------------------------------------------------- backgrounds
def bg(cr, style, t, c1=None, c2=None):
    if style == "sunburst":   # rotating rays: loud, good for hooks and the ending
        c1, c2 = c1 or hexc("#ff5a4e"), c2 or hexc("#ff8a6e")
        cr.set_source_rgba(*c1)
        cr.paint()
        cx, cy, n = W / 2, H * 0.42, 18
        for k in range(n):
            a0 = 2 * math.pi * k / n + t * 0.25
            cr.move_to(cx, cy)
            cr.arc(cx, cy, 1600, a0, a0 + math.pi / n)
            cr.close_path()
        cr.set_source_rgba(*c2)
        cr.fill()
    elif style == "comic":    # yellow with halftone dots
        cr.set_source_rgba(*(c1 or YELLOW))
        cr.paint()
        col = c2 or hexc("#f2b632")
        for r in range(0, H, 34):
            for c in range(0, W + 34, 34):
                x = c + (17 if (r // 34) % 2 else 0)
                rad = 3 + 5 * (r / H)
                dot(cr, x, r, rad, col)
    elif style == "blueprint":
        cr.set_source_rgba(*(c1 or NAVY))
        cr.paint()
        cr.set_source_rgba(1, 1, 1, 0.08)
        cr.set_line_width(2)
        off = (t * 12) % 48
        for x in range(-48, W + 48, 48):
            cr.move_to(x + off, 0)
            cr.line_to(x + off, H)
        for y in range(-48, H + 48, 48):
            cr.move_to(0, y + off)
            cr.line_to(W, y + off)
        cr.stroke()
    elif style == "night":
        cr.set_source_rgba(*(c1 or hexc("#2a2f5a")))
        cr.paint()
        for k in range(40):
            x = (k * 151) % W
            y = 120 + (k * 97) % 520
            dot(cr, x, y, 2 + (k % 3), hexc("#fbf3e1", 0.4 + 0.4 * abs(math.sin(t * 2 + k))))
    else:                     # plain sky
        cr.set_source_rgba(*(c1 or hexc("#a9dcf5")))
        cr.paint()


# ---------------------------------------------------------------- comic language
def burst(cr, x, y, r, t, start, col=YELLOW, spikes=14, seed=40000):
    """Comic starburst that pops in behind a number or word."""
    if t < start:
        return
    s = pop(t, start, 0.3) or 0.01
    wob = 1 + 0.03 * math.sin(t * 8)
    pts = []
    for k in range(spikes * 2):
        a = math.pi * k / spikes + t * 0.3
        rr = r * (1.0 if k % 2 == 0 else 0.68) * s * wob
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    shape(cr, pts, col, seed=seed, amp=0.4, lw=5)


def speed_lines(cr, cx, cy, t, col=WHITE, n=22, r0=260, r1=900, alpha=0.6):
    """Radial comic speed lines around a focus point (flicker every frame)."""
    cr.set_source_rgba(*col[:3], alpha)
    for k in range(n):
        a = 2 * math.pi * k / n + 0.13 * math.sin(t * 13 + k)
        w = 0.025 + 0.02 * ((k * 7) % 3)
        cr.move_to(cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        cr.line_to(cx + r1 * math.cos(a - w), cy + r1 * math.sin(a - w))
        cr.line_to(cx + r1 * math.cos(a + w), cy + r1 * math.sin(a + w))
        cr.close_path()
    cr.fill()


def panel(cr, t, start, x, y, w, h, draw_fn, frm="left", fill=CREAM, seed=40100, tilt=0.0):
    """A comic panel that slides in from `frm` at `start`; draw_fn(cr) draws inside its clip, origin at the centre."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.3))
    dx = {"left": -W, "right": W}.get(frm, 0) * (1 - u)
    dy = {"top": -H / 2, "bottom": H / 2}.get(frm, 0) * (1 - u)
    with at(cr, x + w / 2 + dx, y + h / 2 + dy, 1.0, rot=tilt):
        shape(cr, rrect_pts(-w / 2 - 6, -h / 2 + 6, w, h, 10, 16), INK, seed=seed + 1, amp=0.3, lw=0, stroke=None)
        shape(cr, rrect_pts(-w / 2, -h / 2, w, h, 10, 16), fill, seed=seed, amp=0.3, lw=6)
        cr.save()
        cr.rectangle(-w / 2 + 4, -h / 2 + 4, w - 8, h - 8)
        cr.clip()
        draw_fn(cr)
        cr.restore()
    cue("whoosh", t, start, 0.2)


# ---------------------------------------------------------------- particles
def swarm(cr, cx, cy, t, n=6, r=150, draw_one=None, s=0.35):
    """Small things orbiting a point on wobbly loops (e.g. mosquitoes)."""
    for k in range(n):
        a = t * (1.4 + 0.2 * k) + k * 2 * math.pi / n
        x = cx + r * math.cos(a) * (1 + 0.2 * math.sin(t * 2 + k))
        y = cy + 0.55 * r * math.sin(a * 1.3)
        if draw_one:
            draw_one(cr, x, y, t + k, s, 1 if math.cos(a) < 0 else -1, 40200 + k * 40)
        else:
            dot(cr, x, y, 5, INK)


def heat_waves(cr, x, y, t, n=3, col=RED):
    for k in range(n):
        pts = [(x - 40 + k * 40 + 8 * math.sin(t * 6 + j + k), y - j * 18) for j in range(6)]
        line(cr, pts, 5, col, 40300 + k, amp=0.2)


def mist(cr, x, y, t, start, col=hexc("#7fc8e8"), n=14):
    if t < start:
        return
    for k in range(n):
        d = ((t - start) * 160 + k * 23) % 180
        a = -0.5 + 0.08 * (k % 7)
        dot(cr, x + d * math.cos(a), y + d * math.sin(a), 6 - d / 45, col)


def sparkles(cr, x, y, t, r=80, n=6, col=YELLOW):
    for k in range(n):
        a = k * 2 * math.pi / n + t
        rr = r * (0.8 + 0.2 * math.sin(t * 4 + k))
        sx, sy = x + rr * math.cos(a), y + rr * math.sin(a)
        sz = 6 + 4 * abs(math.sin(t * 5 + k))
        line(cr, [(sx - sz, sy), (sx + sz, sy)], 3, col, 40400 + k, amp=0)
        line(cr, [(sx, sy - sz), (sx, sy + sz)], 3, col, 40420 + k, amp=0)


def sweat(cr, x, y, t, n=3):
    for k in range(n):
        d = ((t * 60 + k * 30) % 60)
        blob(cr, x + k * 14, y + d, 5, 8, hexc("#7fc8e8"), 40500 + k, amp=0.1, lw=2)


# ---------------------------------------------------------------- numbers
def big_number(cr, t, start, value, x, y, size=150, col=RED, prefix="", suffix="", dur=0.8, burst_col=None):
    """A big number that counts up to `value` and lands with a starburst."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + dur))
    if burst_col:
        burst(cr, x, y - size * 0.3, size * 1.1, t, start + dur * 0.8, burst_col)
    s = 1 + 0.15 * max(0.0, 1 - abs((t - start - dur) / 0.12)) if t >= start + dur - 0.12 else 1.0
    with at(cr, x, y, s):
        write(cr, [(f"{prefix}{int(round(value * u))}{suffix}", col)], 0, 0, size, align="center", bold=True,
              halo=CREAM)
    cue("hit", t, start + dur)
