"""Look test: the opening of "Floor 13" (lines f1, f2, f5) in the illustrated 2D style (channels/horror/toon2d.py).

Owner, 25 Oct 2026: "Not liking the animation" -> picked "Illustrated 2D, drawn in code" as the direction to test.
Same narration takes as the 3D episode (cached), so the two looks can be compared directly.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py floor13_2d   -> out/horror/floor13_2d.mp4
"""
import math

from motion import voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import hud, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.6
MUSIC = "horror"
voice.SPEAKERS.update({"gray": dict(voice="bf_emma", turbo_ref="bf_emma-1.5")})

SCRIPT = [
    dict(id="f1", scene="a", text="The elevator just stopped at floor [thirteen.|13.] "
                                  "Your building doesn't have a floor [thirteen.|13.]"),
    dict(id="f2", scene="c", text="The doors slide open. A dark hallway. Wet footprints, right up to the doors."),
    dict(id="f5", scene="e", text="The lights die. The emergency light kicks in. Battery, twelve percent."),
]

KEY = {"dark", "doesn't", "wet", "die", "emergency"}
STEEL, STEEL_D = hexa("#8a939c"), hexa("#4c535b")
_cache = {}


def _brushed(w, h, seed, base, dark):
    """A cached brushed-steel panel texture."""
    key = ("brushed", w, h, seed)
    if key not in _cache:
        import numpy as np
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        c = cairo.Context(s)
        g = cairo.LinearGradient(0, 0, w, 0)
        g.add_color_stop_rgba(0, *dark)
        g.add_color_stop_rgba(0.5, *base)
        g.add_color_stop_rgba(1, *dark)
        c.set_source(g)
        c.paint()
        rng = np.random.default_rng(seed)
        for _ in range(int(w * 1.5)):
            x = float(rng.uniform(0, w))
            c.set_source_rgba(1, 1, 1, float(rng.uniform(0.01, 0.05)) if rng.random() < 0.5 else 0)
            c.set_source_rgba(*((1, 1, 1) if rng.random() < 0.5 else (0, 0, 0)), float(rng.uniform(0.01, 0.05)))
            c.rectangle(x, 0, 1, h)
            c.fill()
        _cache[key] = s
    return _cache[key]


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0, pan=(0, 0)):
    """A slow push-in over the shot with a little handheld drift."""
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1) + pan[0] * k, cy + 3 * shake * noise(t * 0.6, 4) + pan[1] * k)
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ sets
def elevator_wall(cr, t, lit=1.0):
    cr.set_source_rgba(0.1, 0.11, 0.13, 1)
    cr.paint()
    tex = _brushed(160, 1400, 3, STEEL, STEEL_D)
    for i in range(-1, 6):
        cr.set_source_surface(tex, i * 160 - 40, -60)
        cr.paint()
        cr.set_source_rgba(*INK[:3], 0.6)
        cr.rectangle(i * 160 - 41, -60, 3, 1400)
        cr.fill()
    toon(cr, lambda c: c.rectangle(-20, 1010, 760, 26), hexa("#c3cad1"), hexa("#6d757d"), (0, -6), None, lw=4)
    # the ceiling light panel's cold wash from above
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0.85, 0.92, 1, 0.55 * lit)
    g.add_color_stop_rgba(0.55, 0.85, 0.92, 1, 0.08 * lit)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.35)
    cr.set_source(g)
    cr.paint()


def hallway(cr, t, doors=1.0, spill=1.0, red=0.0, eyes=0.0, prints=1.0):
    """One-point perspective down the dark hallway beyond the elevator doors (vanishing point at 360, 610)."""
    vx, vy = 360, 610
    x0, x1, y0, y1 = 140, 580, 250, 1180          # the doorway
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_source_rgba(0.03, 0.03, 0.04, 1)
    cr.paint()
    fx0, fx1, fy0, fy1 = vx - 70, vx + 70, vy - 90, vy + 70   # the far end of the hall
    wall, floor_c, ceil_c = hexa("#4a4234"), hexa("#2c2620"), hexa("#1e1b18")
    for pts, col in (([(x0, y0), (fx0, fy0), (fx0, fy1), (x0, y1)], wall), ([(x1, y0), (fx1, fy0), (fx1, fy1), (x1, y1)], wall),
                     ([(x0, y1), (fx0, fy1), (fx1, fy1), (x1, y1)], floor_c), ([(x0, y0), (fx0, fy0), (fx1, fy0), (x1, y0)], ceil_c)):
        poly(cr, pts)
        cr.set_source_rgba(*col)
        cr.fill()
    # wallpaper stripes, a baseboard and dead ceiling lights, all in perspective
    def at(xa, xe, ya, ye, u):
        return xa + (xe - xa) * u, ya + (ye - ya) * u
    for side, xa, xe in ((-1, x0, fx0), (1, x1, fx1)):
        for k in range(14):
            u = 1 - (1 - k / 14) ** 1.8
            xt, yt = at(xa, xe, y0, fy0, u)
            xb, yb = at(xa, xe, y1, fy1, u)
            cr.move_to(xt, yt)
            cr.line_to(xb, yb)
            cr.set_source_rgba(0.75, 0.62, 0.38, 0.13)
            cr.set_line_width(5 * (1 - u) + 1)
            cr.stroke()
        # baseboard
        poly(cr, [(xa, y1 - 60), (xe, fy1 - 8), (xe, fy1), (xa, y1)])
        cr.set_source_rgba(*hexa("#1c1611"))
        cr.fill()
        # three doors with frames and number plates
        for u0 in (0.08, 0.34, 0.56):
            u1 = u0 + 0.13 * (1 - u0 * 0.8)
            (xt0, yt0), (xt1, yt1) = at(xa, xe, y1, fy1, u0), at(xa, xe, y1, fy1, u1)
            h0, h1 = (y1 - y0) * (1 - u0) * 0.72, (y1 - y0) * (1 - u1) * 0.72
            door = [(xt0, yt0 - h0), (xt1, yt1 - h1), (xt1, yt1), (xt0, yt0)]
            poly(cr, door)
            cr.set_source_rgba(*hexa("#5a4632"))
            cr.set_line_width(10 * (1 - u0))
            cr.stroke_preserve()
            cr.set_source_rgba(*hexa("#2b1c13"))
            cr.fill()
            cx, cy = (xt0 + xt1) / 2, (yt0 - h0 * 0.82 + yt1 - h1 * 0.82) / 2
            cr.set_source_rgba(0.75, 0.66, 0.42, 0.8)
            cr.rectangle(cx - 9 * (1 - u0), cy, 18 * (1 - u0), 8 * (1 - u0))
            cr.fill()
    for k in range(4):                                    # dead fixtures on the ceiling
        u = 0.1 + k * 0.22
        (lx0, ly0), (lx1, ly1) = at(x0 + 120, fx0 + 20, y0, fy0, u), at(x1 - 120, fx1 - 20, y0, fy0, u)
        dy = 26 * (1 - u)
        poly(cr, [(lx0, ly0), (lx1, ly1), (lx1, ly1 + dy), (lx0, ly0 + dy)])
        cr.set_source_rgba(0.55, 0.55, 0.5, 0.35 if k else 0.35 + 0.4 * (noise(t * 9, 1) > 0.85))
        cr.fill()
    # carpet stripes converging
    cr.set_source_rgba(0.5, 0.15, 0.12, 0.25)
    cr.set_line_width(3)
    for k in range(-4, 5):
        cr.move_to(vx + k * 18, fy1)
        cr.line_to(vx + k * 150, y1)
        cr.stroke()
    # the exit sign at the far end
    glow(cr, vx, fy0 + 26, 90, (1, 0.15, 0.1), 0.35 + 0.15 * red)
    cr.set_source_rgba(0.9, 0.1, 0.08, 1)
    cr.rectangle(vx - 22, fy0 + 18, 44, 16)
    cr.fill()
    # darkness swallowing the far half
    g = cairo.RadialGradient(vx, vy, 10, vx, vy, 520)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(0.45, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.1)
    cr.set_source(g)
    cr.paint()
    # light from the car spilling onto the hall floor (cold, or red after the lights die)
    lc = mix((0.85, 0.92, 1.0, 1), (1.0, 0.18, 0.1, 1), red)
    poly(cr, [(x0 + 20, y1), (vx - 120, 860), (vx + 120, 860), (x1 - 20, y1)])
    g = cairo.LinearGradient(0, y1, 0, 860)
    g.add_color_stop_rgba(0, *lc[:3], 0.45 * spill)
    g.add_color_stop_rgba(1, *lc[:3], 0)
    cr.set_source(g)
    cr.fill()
    # wet footprints coming up the hall to the doors, shining in the spill
    if prints:
        for k in range(9):
            u = k / 8
            yy = 700 + (1120 - 700) * u ** 1.6
            sz = 5 + 26 * u ** 1.6
            xx = vx + (-1 if k % 2 else 1) * (6 + 34 * u ** 1.6)
            cr.save()
            cr.translate(xx, yy)
            cr.scale(1, 0.42)
            cr.arc(0, 0, sz, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(0.04, 0.04, 0.05, 0.9 * prints)
            cr.fill()
            cr.save()
            cr.translate(xx - sz * 0.3, yy - sz * 0.12)
            cr.scale(1, 0.25)
            cr.arc(0, 0, sz * 0.45, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(*lc[:3], (0.25 + 0.5 * u) * spill * prints)
            cr.fill()
    if eyes > 0:                                   # two eyes in the dark at the far end
        for sx in (-1, 1):
            ex, ey = vx + sx * 16, vy + 4
            glow(cr, ex, ey, 44, (1, 0.95, 0.8), 0.6 * eyes)
            cr.save()
            cr.translate(ex, ey)
            cr.scale(1, max(0.05, eyes))
            cr.arc(0, 0, 6, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(1, 0.97, 0.85, eyes)
            cr.fill()
    # the sliding doors
    if doors > 0:
        half = (x1 - x0) / 2
        for side in (-1, 1):
            off = (1 - doors) * half * 1.02
            dx0 = x0 + (0 if side < 0 else half) + side * off
            tex = _brushed(int(half) + 2, y1 - y0, 11 + side, hexa("#9aa3ab"), hexa("#5d656d"))
            cr.set_source_surface(tex, dx0, y0)
            cr.rectangle(dx0, y0, half, y1 - y0)
            cr.fill()
            cr.set_source_rgba(*INK)
            cr.set_line_width(3)
            cr.rectangle(dx0, y0, half, y1 - y0)
            cr.stroke()
    cr.restore()
    # the car's door frame and side walls around the opening
    frame = hexa("#5b636b")
    for pts in ([(0, 0), (x0, y0), (x0, y1), (0, H)], [(W, 0), (x1, y0), (x1, y1), (W, H)]):
        poly(cr, pts)
        cr.set_source_rgba(*frame)
        cr.fill()
    poly(cr, [(0, 0), (W, 0), (x1, y0), (x0, y0)])
    cr.set_source_rgba(*hexa("#3d434a"))
    cr.fill()
    poly(cr, [(0, H), (W, H), (x1, y1), (x0, y1)])
    cr.set_source_rgba(*hexa("#26292d"))
    cr.fill()
    cr.set_source_rgba(*INK)
    cr.set_line_width(6)
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.stroke()


def display(cr, t, num, flick=1.0):
    """The floor indicator above the doors, close: a steel plate, a black window, red segment digits."""
    tex = _brushed(720, 1280, 21, hexa("#8f979f"), hexa("#565e66"))
    cr.set_source_surface(tex, 0, 0)
    cr.paint()
    for (x, y) in ((120, 330), (600, 330), (120, 830), (600, 830)):
        cr.set_source_rgba(0.3, 0.32, 0.35, 1)
        cr.arc(x, y, 9, 0, 2 * math.pi)
        cr.fill()
    toon(cr, lambda c: tk.curve(c, [(150, 400), (570, 400), (570, 760), (150, 760)]), hexa("#0c0707"), None, (0, 0),
         None, lw=7)
    col = (1, 0.13, 0.08, 1)
    glow(cr, 360, 580, 300, col, 0.28 * flick)
    for k, ch in enumerate(num):
        tk.led_digit(cr, ch, 215 + k * 165, 455, 230, col, 0.95 * flick)
    cr.set_source_rgba(*col[:3], 0.8 * flick)
    poly(cr, [(360, 790), (330, 830), (390, 830)])
    cr.fill()


# ------------------------------------------------------------------ the film
def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    t13 = A("f1", "13.", end=True) + 0.25
    t_c, t_d, t_e = B["f2"].start - 0.2, A("f2", "Wet") - 0.1, B["f5"].start - 0.2
    t_die = A("f5", "die.", end=True) + 0.05
    t_red = A("f5", "emergency") - 0.1
    t_e2 = A("f5", "Battery,") - 0.15
    red = clamp01((t - t_red) / 0.25) * (0.75 + 0.25 * (noise(t * 13, 2) > -0.6))
    cr.save()
    if t < t13:                                                    # A: your face, the car has stopped
        camera(cr, t, 0, t13, 1.0, 1.07)
        elevator_wall(cr, t)
        f = tk.face_mix("uneasy", "alarmed", seg(t, A("f1", "stopped") - 0.2, A("f1", "stopped") + 0.3))
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.15, -0.9), tilt=-0.05, rim=(0.75, 0.88, 1, 0.6), rim_from=(-10, -4),
                    sweat=seg(t, 2.5, 3.5))
        glow(cr, 360, -80, 520, (1, 0.12, 0.08), 0.35)               # the red "13" above, out of frame
    elif t < t_c:                                                  # B: the indicator says 13
        camera(cr, t, t13, t_c, 1.0, 1.12)
        roll = (t - t13) / 0.18
        num = "12" if roll < 1 else "13"
        flick = 0.35 if (noise(t * 17, 5) > 0.75) else 1.0
        display(cr, t, num, flick)
    elif t < t_d:                                                  # C: over your shoulder, the doors open
        camera(cr, t, t_c, t_d, 1.0, 1.08, cy=600)
        hallway(cr, t, doors=1 - seg(t, B["f2"].start, B["f2"].start + 1.4), spill=seg(t, B["f2"].start + 0.2, B["f2"].start + 1.4))
        tk.you_back(cr, 150, 1230, 1.5, t, rim=(0.8, 0.9, 1, 0.55))
    elif t < t_e:                                                  # D: the footprints, the camera follows them in
        camera(cr, t, t_d, t_e, 1.25, 1.75, cy=900, shake=1.4, pan=(0, -120))
        hallway(cr, t, doors=0, spill=1.0)
    elif t < t_e2:                                                 # E1: the lights die, the red light comes on
        camera(cr, t, t_e, t_e2, 1.02, 1.1)
        elevator_wall(cr, t, lit=0 if t > t_die else 1)
        f = tk.face_mix("alarmed", "terror", seg(t, t_red, t_red + 0.5))
        skin = mix(tk.SKIN, (0.9, 0.25, 0.2, 1), 0.55 * red) if t > t_die else None
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.6 * math.sin(t * 2.2), -0.2), tilt=0.03,
                    rim=(1, 0.2, 0.12, 0.9) if t > t_red else (0.75, 0.88, 1, 0.6), rim_from=(10, -6),
                    sweat=1.0, tremble=0.6 if t > t_red else 0.0, skin=skin)
        if t > t_die:
            grade(cr, (0.95, 0.25, 0.2), (0.35, 0.05, 0.08), a=1.0)
            glow(cr, 620, 120, 380, (1, 0.15, 0.08), 0.55 * red)
    else:                                                          # E2: the dark hall, and something in it
        camera(cr, t, t_e2, tl.total, 1.0, 1.16, cy=640)
        hallway(cr, t, doors=0, spill=0.8, red=1.0, eyes=seg(t, A("f5", "percent.") - 0.2, A("f5", "percent.") + 0.25))
        grade(cr, (0.9, 0.3, 0.28), (0.5, 0.1, 0.12), a=1.0)
    cr.restore()
    if t_die <= t < t_red:                                        # the dead moment: black
        cr.set_source_rgba(0, 0, 0, 1 if t < t_red - 0.25 else 0.6)
        cr.paint()
    hud.finish(cr, t, flash_at=[], vig=0.55, grain=0.07)
    if t >= A("f5", "Battery,"):
        hud.meter(cr, t, "EMERGENCY LIGHT", 0.12, warn=0.15)
    hud.tag(cr, t, "FLOOR 13", "PART 1")
    hud.chips(cr, t, [("FLOOR 13", None, True), ("SIGNAL X", None, True)])
    hud.hook(cr, t, [("FLOOR 13?", True), ("YOUR BUILDING", False), ("DOESN'T HAVE ONE", False)],
             end=t13, y=230, size=82)
    hud.captions(cr, t, tl, KEY)
    cue("hum", t, 0.0, t_die)
    cue("chime", t, A("f1", "stopped", end=True) + 0.05)
    cue("doors", t, B["f2"].start + 0.05)
    cue("drip", t, t_d)
    cue("power_down", t, t_die)
    cue("heartbeat", t, t_red, tl.total - t_red)
