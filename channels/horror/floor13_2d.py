"""Floor 13, Part 1, in the illustrated 2D style (channels/horror/toon2d.py): the full episode.

Owner, 25 Oct 2026: "Not liking the animation" -> picked "Illustrated 2D, drawn in code"; after the 15 s look test:
"Yeah 2d better". Same script and narration takes as the 3D episode (floor13.py), redrawn shot by shot.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py floor13_2d   -> out/horror/floor13_2d.mp4
"""
import math

from motion import voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import floor13 as ep3d
from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
voice.SPEAKERS.update({"gray": dict(voice="bf_emma", turbo_ref="bf_emma-1.5")})
SCRIPT = [dict(d) for d in ep3d.SCRIPT]
for _d in SCRIPT:
    if _d["id"] == "f18":
        _d["gap"] = 1.0          # the drop happens in this silence; the line then names it (the snap on a word hid it)
METADATA = ep3d.METADATA
KEY = ep3d.KEY
STEEL, STEEL_D = hexa("#8a939c"), hexa("#4c535b")
RED_RIM = (1, 0.2, 0.12, 0.9)
COLD_RIM = (0.75, 0.88, 1, 0.6)
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


def hallway(cr, t, doors=1.0, spill=1.0, red=0.0, eyes=0.0, prints=1.0, figure=None, raise_=0.0):
    """One-point perspective down the dark hallway beyond the elevator doors (vanishing point at 360, 610)."""
    vx, vy = 360, 610
    x0, x1, y0, y1 = 140, 580, 250, 1180          # the doorway
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_source_rgba(0.03, 0.03, 0.04, 1)
    cr.paint()
    cr.save()
    cr.translate(0, -raise_)                      # after the drop the whole hallway sits higher than the car
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
    if figure:
        figure(cr)
    cr.restore()
    if raise_ > 0:                                # the shaft wall below the hallway's floor edge
        top = y1 - raise_
        g = cairo.LinearGradient(0, top, 0, y1)
        g.add_color_stop_rgba(0, 0.16, 0.15, 0.15, 1)
        g.add_color_stop_rgba(1, 0.05, 0.05, 0.06, 1)
        cr.rectangle(x0, top, x1 - x0, raise_)
        cr.set_source(g)
        cr.fill()
        cr.set_source_rgba(0.55, 0.5, 0.42, 1)
        cr.rectangle(x0, top - 6, x1 - x0, 12)
        cr.fill()
        cr.set_source_rgba(0, 0, 0, 0.5)
        for k in range(6):
            cr.rectangle(x0, top + 30 + k * 52, x1 - x0, 3)
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


# ------------------------------------------------------------------ extra sets
def panel_scene(cr, t, gap_focus=0.0, red=0.0):
    """The button panel close: rows of buttons, 12 then 14, no 13; the sign taped above."""
    tex = _brushed(720, 1280, 31, hexa("#8f979f"), hexa("#555c64"))
    cr.set_source_surface(tex, 0, 0)
    cr.paint()
    toon(cr, lambda c: tk.tk_rrect(c, 170, 220, 380, 900, 26), hexa("#a4acb4"), hexa("#6c747c"), (-10, -8), None, lw=5)
    labels = ["B", "G", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", None, "14"]   # no 13: a blank
    for k, lab in enumerate(labels):
        if lab is None:
            continue
        col, row = k % 3, k // 3
        bx, by = 255 + col * 105, 1040 - row * 150 if k < 15 else 290
        toon(cr, lambda c, bx=bx, by=by: c.arc(bx, by, 38, 0, 2 * math.pi), hexa("#d9dde1"), hexa("#9aa1a8"), (-6, -5),
             None, lw=4)
        cr.set_source_rgba(*INK)
        tw = hud.text_width(cr, lab, 30, "Liberation Sans")
        hud._plain(cr, lab, bx - tw / 2, by + 11, 30, "Liberation Sans", "left", INK)
    gx, gy = 465, 440                                   # where 13 should be: a blank plate
    if gap_focus > 0:
        glow(cr, gx, gy, 90, (1, 0.2, 0.1), 0.35 * gap_focus)
        cr.set_source_rgba(1, 0.25, 0.15, 0.9 * gap_focus)
        cr.set_line_width(4)
        cr.set_dash([10, 8])
        cr.arc(gx, gy, 40, 0, 2 * math.pi)
        cr.stroke()
        cr.set_dash([])


def sign_scene(cr, t):
    """The sign above the buttons: printed, taped, yellowed."""
    tex = _brushed(720, 1280, 41, hexa("#8f979f"), hexa("#555c64"))
    cr.set_source_surface(tex, 0, 0)
    cr.paint()
    cr.save()
    cr.translate(360, 640)
    cr.rotate(-0.03)
    cr.set_source_rgba(0, 0, 0, 0.35)
    tk.tk_rrect(cr, -262, -322, 540, 660, 6)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, -270, -330, 540, 660, 6), hexa("#eae2c8"), hexa("#cfc4a2"), (-12, -10), None, lw=4)
    for (x, y, r) in ((-250, -320, -0.5), (250, -320, 0.5)):
        cr.save()
        cr.translate(x, y)
        cr.rotate(r)
        cr.set_source_rgba(0.95, 0.92, 0.75, 0.75)
        cr.rectangle(-40, -14, 80, 28)
        cr.fill()
        cr.restore()
    rows = [("NOTICE", 64, INK, "Liberation Sans"), ("IF THE DOORS OPEN ON", 34, INK, "Liberation Sans"),
            ("A FLOOR THAT ISN'T THERE:", 34, INK, "Liberation Sans"), ("", 20, INK, "Liberation Sans"),
            ("DO NOT STEP OUT.", 46, hexa("#a3150f"), "Liberation Sans"),
            ("DO NOT ANSWER.", 46, hexa("#a3150f"), "Liberation Sans"), ("", 20, INK, "Liberation Sans"),
            ("- Management", 26, INK, "Liberation Sans")]
    y = -240
    for txt, size, col, font in rows:
        if txt:
            w_ = hud.text_width(cr, txt, size, font)
            hud._plain(cr, txt, -w_ / 2, y, size, font, "left", col)
        y += size * 1.45
    cr.restore()


def flashback(cr, t, k, x_mark):
    """A memory, as an old photo: Mrs. Gray in daylight with her cane, beside the stairs she can't climb."""
    cr.set_source_rgba(0.05, 0.04, 0.05, 1)
    cr.paint()
    cr.save()
    cr.translate(360, 600 + 40 * (1 - k))
    cr.rotate(-0.04)
    cr.set_source_rgba(0.96, 0.94, 0.88, 1)
    cr.rectangle(-270, -380, 540, 700)
    cr.fill()
    cr.rectangle(-240, -350, 480, 520)
    cr.clip()
    g = cairo.LinearGradient(0, -350, 0, 170)
    g.add_color_stop_rgba(0, *hexa("#e8cf9c"))
    g.add_color_stop_rgba(1, *hexa("#b48d5c"))
    cr.set_source(g)
    cr.paint()
    for k2 in range(7):                                   # the stairs behind her
        toon(cr, lambda c, k2=k2: c.rectangle(40 + k2 * 30, 170 - (k2 + 1) * 40, 200, 40), hexa("#a07548"),
             hexa("#7c5634"), (-6, -4), None, lw=3)
    tk.gray_full(cr, -90, 165, 0.82, t, smile=0.0)
    cr.restore()
    cr.save()
    cr.translate(360, 600 + 40 * (1 - k))
    cr.rotate(-0.04)
    hud._plain(cr, "Mrs. Gray, 1402", -150, 262, 40, "Permanent Marker", "left", INK)   # on the photo's white border
    cr.restore()
    if x_mark > 0:                                        # she can't do stairs
        cr.save()
        cr.translate(470, 560)
        cr.set_source_rgba(0.9, 0.08, 0.06, 0.95)
        cr.set_line_width(18)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        u = clamp01(x_mark)
        cr.move_to(-90, -90)
        cr.line_to(-90 + 180 * min(1, u * 2), -90 + 180 * min(1, u * 2))
        if u > 0.5:
            cr.move_to(90, -90)
            cr.line_to(90 - 180 * (u - 0.5) * 2, -90 + 180 * (u - 0.5) * 2)
        cr.stroke()
        cr.restore()


def mirror_scene(cr, t, red=1.0):
    """You face the mirror on the back wall; in it, the open doorway behind you is empty."""
    elevator_wall(cr, t, lit=0)
    mx0, my0, mx1, my1 = 90, 180, 630, 900
    toon(cr, lambda c: tk.tk_rrect(c, mx0 - 18, my0 - 18, mx1 - mx0 + 36, my1 - my0 + 36, 10), hexa("#5d656d"),
         hexa("#3a4047"), (-8, -6), None, lw=5)
    cr.save()
    cr.rectangle(mx0, my0, mx1 - mx0, my1 - my0)
    cr.clip()
    cr.set_source_rgba(0.12, 0.05, 0.06, 1)
    cr.paint()
    cr.save()                                             # the reflection: the car behind you and the doorway
    cr.translate(360, 560)
    cr.scale(0.5, 0.5)
    cr.translate(-360, -560)
    hallway(cr, t, doors=0, spill=0.5, red=1.0, prints=0.6)
    cr.restore()
    tk.you_bust(cr, 360, 960, 1.15, tk.face_mix("terror", "terror", 0), t, look=(0.0, 0.0), rim=RED_RIM,
                skin=mix(tk.SKIN, (0.9, 0.25, 0.2, 1), 0.5), sweat=1, tremble=0.5)
    g = cairo.LinearGradient(mx0, my0, mx1, my1)          # glass sheen
    g.add_color_stop_rgba(0, 1, 1, 1, 0.12)
    g.add_color_stop_rgba(0.5, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.08)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    tk.you_back(cr, 420, 1330, 1.25, t, rim=RED_RIM, rim_from=(-10, 0))


def shaft_scene(cr, t, slip=0.0):
    """Outside the car: the dark shaft, the car roof hanging on its cables, one cable fraying."""
    cr.set_source_rgba(0.04, 0.04, 0.05, 1)
    cr.paint()
    for x in (80, 640):
        g = cairo.LinearGradient(x - 60, 0, x + 60, 0)
        g.add_color_stop_rgba(0, 0.1, 0.1, 0.11, 1)
        g.add_color_stop_rgba(1, 0.06, 0.06, 0.07, 1)
        cr.set_source(g)
        cr.rectangle(x - 80, 0, 160, H)
        cr.fill()
    for cx in (320, 360, 400):
        cr.set_source_rgba(0.55, 0.55, 0.52, 1)
        cr.set_line_width(7)
        cr.move_to(cx, 0)
        cr.line_to(cx, 780)
        cr.stroke()
    cr.set_source_rgba(0.75, 0.7, 0.6, 1)                 # the frayed one
    cr.set_line_width(2)
    for k in range(7):
        a = (k - 3) * 0.2
        cr.move_to(360, 520)
        cr.line_to(360 + 40 * math.sin(a), 520 - 40 * math.cos(a) * 0.4)
        cr.stroke()
    glow(cr, 360, 520, 80, (1, 0.7, 0.3), 0.4 * (noise(t * 20, 3) > 0.4))
    toon(cr, lambda c: c.rectangle(110, 780 + 18 * slip, 500, 70), hexa("#4f565e"), hexa("#30353b"), (-8, -6), None, lw=5)
    glow(cr, 360, 980, 400, (1, 0.15, 0.08), 0.35)


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "face_hook"), (A("f1", "13.", end=True) + 0.25, "display"),
        (B["f2"].start - 0.2, "doors"), (A("f2", "Wet") - 0.1, "prints"),
        (B["f3"].start - 0.2, "panel"), (B["f4"].start - 0.2, "sign"),
        (B["f5"].start - 0.2, "lights_out"), (A("f5", "Battery,") - 0.15, "hall_red"),
        (B["f6"].start - 0.2, "hall_eyes"), (B["f7"].start - 0.2, "hall_gray_far"),
        (B["f8"].start - 0.2, "hall_gray_mid"), (B["f9"].start - 0.2, "face_listen"),
        (A("f9", "cane.", end=True) + 0.1, "flashback"),
        (B["f10"].start - 0.2, "phone"), (B["f12"].start - 0.2, "panel_gap"), (B["f13"].start - 0.2, "phone"),
        (B["f15"].start - 0.2, "hall_empty"), (B["f16"].start - 0.2, "mirror"), (B["f17"].start - 0.2, "turn"),
        (A("f17", "isn't.") - 0.03, "reveal"), (B["f18"].start - 0.95, "drop"), (B["f19"].start - 0.2, "gray_close"),
        (B["f20"].start - 0.2, "face_2pct"), (B["f20b"].start - 0.2, "gray_door"), (B["f20c"].start - 0.2, "shaft"),
        (B["f21"].start - 0.2, "choice"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_die = A("f5", "die.", end=True) + 0.05
    t_red = A("f5", "emergency") - 0.1
    t_drop = B["f18"].start - 0.9                    # in the silence before the line (on a word the snap hid it)
    red_on = t > t_red
    red = (0.75 + 0.25 * (noise(t * 13, 2) > -0.6)) * (1 - 0.4 * seg(t, B["f19"].start, tl.total)) if red_on else 0
    raise_ = 330 * min(1.0, ((t - t_drop) / 0.18) ** 2) if t > t_drop else 0.0
    shake = 1.0 + (6 * max(0.0, 1 - (t - t_drop) / 1.2) if t > t_drop else 0)
    red_skin = mix(tk.SKIN, (0.9, 0.25, 0.2, 1), 0.55)

    def gray_at(x, y, sc, smile, glow_e, reach=0.0, dark=0.0):
        def fig(c):
            tk.gray_full(c, x, y, sc, t, smile=smile, glow_eyes=glow_e, reach=reach, rim=RED_RIM if red_on else COLD_RIM)
            if dark > 0:
                c.set_source_rgba(0.02, 0.0, 0.0, dark)
                c.paint()
                for sx in (-1, 1):
                    glow(c, x + sx * 24 * sc, y - 572 * sc, 40 * sc + 10, (1, 0.95, 0.8), 0.6 * glow_e)
                    c.set_source_rgba(1, 0.97, 0.88, glow_e)
                    c.arc(x + sx * 24 * sc, y - 572 * sc, 6.5 * sc + 1.5, 0, 2 * math.pi)
                    c.fill()
        return fig

    cr.save()
    if name == "face_hook":
        camera(cr, t, s0, s1, 1.0, 1.07)
        hud2d.blurred(cr, lambda c: elevator_wall(c, t))
        f = tk.face_mix("uneasy", "alarmed", seg(t, A("f1", "stopped") - 0.2, A("f1", "stopped") + 0.3))
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.15, -0.9), tilt=-0.05, rim=COLD_RIM, rim_from=(-10, -4),
                    sweat=seg(t, 2.5, 3.5))
        glow(cr, 360, -80, 520, (1, 0.12, 0.08), 0.35)
    elif name == "display":
        camera(cr, t, s0, s1, 1.0, 1.12)
        display(cr, t, "12" if (t - s0) < 0.18 else "13", 0.35 if noise(t * 17, 5) > 0.75 else 1.0)
    elif name == "doors":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600)
        hallway(cr, t, doors=1 - seg(t, B["f2"].start, B["f2"].start + 1.4), spill=seg(t, B["f2"].start + 0.2, B["f2"].start + 1.4))
        tk.you_back(cr, 150, 1230, 1.5, t, rim=COLD_RIM)
    elif name == "prints":
        camera(cr, t, s0, s1, 1.25, 1.75, cy=900, shake=1.4, pan=(0, -120))
        hallway(cr, t, doors=0, spill=1.0)
    elif name == "panel":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=700)
        panel_scene(cr, t)
        tk.hand_point(cr, 560 - 60 * seg(t, s0, s1), 1230 - 140 * seg(t, s0, s0 + 1.5), 1.3, t, tremble=0.5)
    elif name == "sign":
        camera(cr, t, s0, s1, 1.0, 1.15)
        sign_scene(cr, t)
    elif name == "lights_out":
        camera(cr, t, s0, s1, 1.02, 1.1)
        hud2d.blurred(cr, lambda c: elevator_wall(c, t, lit=0 if t > t_die else 1))
        f = tk.face_mix("alarmed", "terror", seg(t, t_red, t_red + 0.5))
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.6 * math.sin(t * 2.2), -0.2), tilt=0.03,
                    rim=RED_RIM if red_on else COLD_RIM, rim_from=(10, -6), sweat=1.0, tremble=0.6 if red_on else 0.0,
                    skin=red_skin if t > t_die else None)
        if t > t_die:
            grade(cr, (0.95, 0.25, 0.2), (0.35, 0.05, 0.08))
            glow(cr, 620, 120, 380, (1, 0.15, 0.08), 0.55 * red)
    elif name in ("hall_red", "hall_eyes", "hall_gray_far", "hall_gray_mid", "hall_empty"):
        camera(cr, t, s0, s1, 1.0, 1.16 if name != "hall_empty" else 1.25, cy=640)
        eyes = 0.0
        if name == "hall_red":
            eyes = seg(t, A("f5", "percent.") - 0.2, A("f5", "percent.") + 0.25)
        elif name == "hall_eyes":
            eyes = 1.0
        fig = None
        if name == "hall_gray_far":
            fig = gray_at(360, 690, 0.22, 0.2, 1.0, dark=0.7)
        elif name == "hall_gray_mid":
            fig = gray_at(360, 860, 0.62, 0.35, 1.0, dark=0.55)
        hallway(cr, t, doors=0, spill=0.8, red=1.0, eyes=eyes, figure=fig)
        grade(cr, (0.9, 0.3, 0.28), (0.5, 0.1, 0.12))
    elif name == "face_listen":
        camera(cr, t, s0, s1, 1.05, 1.12)
        hud2d.blurred(cr, lambda c: elevator_wall(c, t, lit=0))
        tk.you_bust(cr, 360, 930, 1.42, tk.face_mix("terror", "terror", 0), t, look=(0.9, 0.1), turn=0.35, rim=RED_RIM,
                    rim_from=(10, -6), sweat=1, tremble=0.7, skin=red_skin)
        grade(cr, (0.95, 0.25, 0.2), (0.35, 0.05, 0.08))
    elif name == "flashback":
        flashback(cr, t, seg(t, s0, s0 + 0.4), seg(t, A("f9", "can't") - 0.1, A("f9", "stairs.", end=True)))
        grade(cr, (1, 0.93, 0.8), (0.8, 0.7, 0.6))
    elif name == "phone":
        camera(cr, t, s0, s1, 1.0, 1.04, shake=0.6)
        hud2d.blurred(cr, lambda c: (elevator_wall(c, t, lit=0), grade(c, (0.9, 0.3, 0.28), (0.3, 0.06, 0.08))), sigma=10)
        first = t < B["f13"].start - 0.2
        notes = ([(A("f10", "building") - 0.3, "MESSAGES", "Tower B Residents", "Elevator broken since 6 PM. Nobody use it.")]
                 if first else
                 [(B["f13"].start + 0.1, "MESSAGES", "Mrs. Gray (1402)", "Are you in the elevator??"),
                  (A("f14", "Don't") - 0.3, "MESSAGES", "Mrs. Gray (1402)", "Don't come out. I'm at home on 14.")])
        hud2d.phone_pov(cr, t, s0, "11:52", "Friday", notes, skin=mix(tk.SKIN, (0.55, 0.7, 1.0, 1), 0.3))
    elif name == "panel_gap":
        camera(cr, t, s0, s1, 1.0, 1.35, cx=465, cy=440)
        panel_scene(cr, t, gap_focus=seg(t, s0, s0 + 0.6))
        grade(cr, (0.95, 0.3, 0.25), (0.45, 0.08, 0.1))
    elif name == "mirror":
        camera(cr, t, s0, s1, 1.0, 1.08)
        mirror_scene(cr, t)
        grade(cr, (0.95, 0.3, 0.25), (0.45, 0.08, 0.1))
    elif name == "turn":
        camera(cr, t, s0, s1, 1.05, 1.1, shake=2.0)
        hud2d.blurred(cr, lambda c: elevator_wall(c, t, lit=0))
        tk.you_bust(cr, 360, 930, 1.42, tk.face_mix("terror", "terror", 0), t, look=(1.0, 0), turn=-0.9 * seg(t, s0, s0 + 0.6),
                    rim=RED_RIM, rim_from=(10, -6), sweat=1, tremble=1.0, skin=red_skin)
        grade(cr, (0.95, 0.25, 0.2), (0.35, 0.05, 0.08))
    elif name in ("reveal", "drop", "gray_door"):
        cyy = 640 if name != "drop" else 700
        camera(cr, t, s0, s1, 1.0, 1.1 if name != "gray_door" else 1.05, cy=cyy, shake=shake)
        smile = 1.0
        fig = gray_at(360, 1170, 1.45, smile, 1.0, reach=0.6 if name == "gray_door" else 0.0)
        hallway(cr, t, doors=0, spill=0.9, red=1.0, figure=fig, raise_=raise_)
        if name == "gray_door":
            tk.you_back(cr, 170, 1360, 1.2, t, rim=RED_RIM, rim_from=(-10, 0))
        grade(cr, (0.95, 0.3, 0.25), (0.45, 0.08, 0.1))
    elif name == "gray_close":
        camera(cr, t, s0, s1, 1.0, 1.12, shake=1.5)
        hallway(cr, t, doors=0, spill=0.9, red=1.0, raise_=330)
        cr.save()
        cr.translate(380, 520)
        cr.rotate(0.35 + 0.05 * math.sin(t * 0.8))
        cr.scale(3.6, 3.6)
        talk = 0.5 + 0.5 * math.sin(t * 14)
        tk.gray_head(cr, t, 1.0, 1.0, rim=RED_RIM, mouth_open=talk if A("f19", "Come") <= t <= B["f19"].end else 0)
        cr.restore()
        grade(cr, (0.95, 0.3, 0.25), (0.45, 0.08, 0.1))
    elif name == "face_2pct":
        camera(cr, t, s0, s1, 1.08, 1.16)
        hud2d.blurred(cr, lambda c: elevator_wall(c, t, lit=0))
        tk.you_bust(cr, 360, 930, 1.42, tk.face_mix("terror", "terror", 0), t, look=(0.2, -0.5), rim=RED_RIM,
                    rim_from=(10, -6), sweat=1, tremble=1.0, skin=mix(red_skin, (0, 0, 0, 1), 0.3))
        grade(cr, (0.75, 0.15, 0.12), (0.25, 0.03, 0.05))
    elif name == "shaft":
        camera(cr, t, s0, s1, 1.0, 1.08)
        shaft_scene(cr, t, slip=seg(t, s0 + 0.6, s0 + 0.9))
    elif name == "choice":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=0.6)
        fig = gray_at(360, 1170, 1.45, 1.0, 1.0, reach=1.0)
        hallway(cr, t, doors=0, spill=0.7, red=1.0, figure=fig, raise_=330)
        tk.you_back(cr, 170, 1360, 1.2, t, rim=RED_RIM, rim_from=(-10, 0))
        grade(cr, (0.95, 0.3, 0.25), (0.45, 0.08, 0.1))
    cr.restore()
    if t_die <= t < t_red:                                        # the dead moment: black
        cr.set_source_rgba(0, 0, 0, 1 if t < t_red - 0.25 else 0.6)
        cr.paint()
    hud.blackout(cr, t, A("f17", "around.", end=True) + 0.05, A("f17", "isn't.") - 0.03)
    hud.finish(cr, t, flash_at=[A("f17", "isn't."), t_drop], vig=0.55, grain=0.06)
    if t < A("f5", "Battery,"):
        batt = ("BATTERY", "--", None)
    else:
        v = round(12 - 10 * seg(t, A("f5", "Battery,"), B["f20"].start + 0.3))
        batt = ("BATTERY", f"{v}%", "bad" if v <= 4 else "warn", A("f5", "Battery,"))
    sig = ("SIGNAL", "1 BAR", "warn", B["f10"].start) if t >= B["f10"].start else ("SIGNAL", "NONE", "bad")
    floor = ("FLOOR", "13 -0.5M", "bad", t_drop) if t >= t_drop else ("FLOOR", "13 ?", "bad")
    hud2d.stats(cr, t, [floor, batt, sig])
    hud2d.hook(cr, t, [("FLOOR 13?", True), ("YOUR BUILDING", False), ("DOESN'T HAVE ONE", False)],
               end=A("f1", "13.", end=True) + 0.25, y=270)
    hud2d.rule_tag(cr, t, A("f4", "don't", nth=1), B["f4"].end + 0.6, "RULE: DON'T STEP OUT. DON'T ANSWER.", y=200)
    hud2d.stamp(cr, t, A("f12", "13?"), B["f12"].end + 0.3, ["WHO PRESSED 13?"], y=250)
    hud2d.stamp(cr, t, t_drop + 0.05, t_drop + 1.0, ["-0.5 M"], y=330)
    hud2d.bubble(cr, t, B["f7"].start, B["f7"].end, "Sweetheart? It's me. Mrs. Gray, from your floor.", 360, 330,
                 (372, 470), creepy=True)
    hud2d.bubble(cr, t, B["f8"].start, B["f8"].end, "The elevator is broken. Come out, quickly. I'll take you to the stairs.",
                 360, 330, (372, 520), creepy=True)
    hud2d.bubble(cr, t, B["f19"].start, B["f19"].end, "Come out now. Or you'll fall.", 360, 1010, (380, 820), creepy=True)
    if name == "shaft":
        hud.blueprint(cr, t, B["f20c"].start + 0.3, B["f20c"].end + 0.3, "THE SHAFT", ep3d.shaft)
    hud2d.ab_card(cr, t, A("f22", "step"), "STEP OUT", "STAY", kicker="FLOOR 13 · PART 1 · YOUR CHOICE")
    hud2d.captions(cr, t, tl, KEY, skip=("f7", "f8", "f19"))
    cue("hum", t, 0.0, t_die)
    cue("chime", t, A("f1", "stopped", end=True) + 0.05)
    cue("doors", t, B["f2"].start + 0.05)
    cue("power_down", t, t_die)
    cue("drip", t, B["f6"].start - 0.3)
    cue("sting", t, A("f17", "isn't."))
    cue("cable", t, t_drop)
    cue("heartbeat", t, B["f19"].start, B["f20c"].end - B["f19"].start)
    cue("riser", t, B["f21"].start, B["f22"].start - B["f21"].start)
