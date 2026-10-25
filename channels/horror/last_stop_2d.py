"""Last Stop, Night 1, in the illustrated 2D style (channels/horror/toon2d.py): the full episode.

Same script and narration takes as the 3D episode (last_stop.py), redrawn shot by shot after the owner's "Yeah 2d
better" and their 2D reference (stats bar, blurred backgrounds, speech bubbles, the phone in your hands, A/B ending).
Rewatch detail: one of the three faces in the window wears the old man's flat cap and scarf, and he is asleep at the
front of the bus.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py last_stop_2d   -> out/horror/last_stop_2d.mp4
"""
import math

from motion import voice  # noqa: F401  (last_stop registers the driver's and the old man's voices)
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import last_stop as ep3d
from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
SCRIPT = [dict(d) for d in ep3d.SCRIPT]
for _d in SCRIPT:
    if _d["id"] == "b15":
        _d["gap"] = 1.3          # the breath on your neck plays in this silence (on "breathes" it was heard as "bruised")
METADATA = hud2d.meta_2d(ep3d.METADATA)
KEY = ep3d.KEY
COLD_RIM = (0.75, 0.95, 0.85, 0.55)        # the bus's fluorescent tubes
ORANGE = (1.0, 0.62, 0.28)                 # sodium streetlights
MOQ, MOQ_D = hexa("#2d3f78"), hexa("#1b2750")     # seat fabric
WALL, WALL_D = hexa("#3b444c"), hexa("#262c32")
POLE = hexa("#e0b43a")
TEAL, TEAL_D = hexa("#1f6a63"), hexa("#124340")
CREAM = hexa("#e8dcbc")
_cache = {}

# ------------------------------------------------------------------ the aisle, from the front of the bus looking back
VX, VY, F = 360, 600, 430
HW, YC, YF, YT, YS = 1.25, -0.75, 1.5, 0.48, 1.05       # half width, ceiling, floor, seat top, cushion (metres)
Z0, ZB = 0.35, 6.4
ROWS = [1.55 + r * 0.78 for r in range(6)]


def P(x, y, z):
    return VX + x * F / z, VY + y * F / z


def quad(cr, pts):
    poly(cr, [P(*p) for p in pts])


def _sweeps(t, speed=7.5, length=12.0, n=2):
    """Depths of the streetlights passing outside (they slide from the front of the bus to the back)."""
    return [Z0 + ((t * speed + k * length / n) % length) for k in range(n)]


def _seat(cr, x_in, x_out, zb, top=YT, seed=0, lit=1.0):
    """One seat block seen from the front: top edge, back face (moquette), cushion."""
    lo, hi = min(x_in, x_out), max(x_in, x_out)
    quad(cr, [(lo, top, zb), (hi, top, zb), (hi, top, zb + 0.1), (lo, top, zb + 0.1)])
    cr.set_source_rgba(*MOQ_D)
    cr.fill()
    (ax, ay), (bx, by) = P(lo, top, zb), P(hi, YS, zb)
    r = 0.08 * F / zb
    toon(cr, lambda c: tk.tk_rrect(c, ax, ay, bx - ax, by - ay, r), MOQ, MOQ_D, (-4, -3), None, lw=max(1.5, 9 / zb))
    cr.save()                                                   # the moquette's squiggles
    tk.tk_rrect(cr, ax, ay, bx - ax, by - ay, r)
    cr.clip()
    cols = [(0.95, 0.75, 0.2), (0.85, 0.25, 0.25), (0.3, 0.75, 0.75)]
    cr.set_line_width(max(1.0, 5 / zb))
    for k in range(14):
        u, v = ((k * 0.618 + seed * 0.37) % 1), ((k * 0.382 + seed * 0.21) % 1)
        px, py = ax + u * (bx - ax), ay + v * (by - ay)
        sz = 0.05 * F / zb
        cr.set_source_rgba(*cols[k % 3], 0.6)
        cr.move_to(px, py)
        cr.curve_to(px + sz * 0.4, py - sz * 0.5, px + sz * 0.8, py + sz * 0.5, px + sz * 1.2, py)
        cr.stroke()
    cr.restore()
    quad(cr, [(lo, YS, zb), (hi, YS, zb), (hi, YS, zb - 0.45), (lo, YS, zb - 0.45)])
    cr.set_source_rgba(*mix(MOQ, (1, 1, 1, 1), 0.08))
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(max(1.5, 7 / zb))
    cr.stroke()
    quad(cr, [(lo, YS, zb - 0.45), (hi, YS, zb - 0.45), (hi, YS + 0.12, zb - 0.45), (lo, YS + 0.12, zb - 0.45)])
    cr.set_source_rgba(*MOQ_D)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.stroke()
    quad(cr, [(lo + 0.05, YS + 0.12, zb - 0.4), (hi - 0.05, YS + 0.12, zb - 0.4), (hi - 0.05, YF, zb - 0.2),
              (lo + 0.05, YF, zb - 0.2)])
    cr.set_source_rgba(0.05, 0.05, 0.06, 0.8)
    cr.fill()
    gx, gy = P(x_in, top, zb)                                   # chrome grab handle on the aisle corner
    cr.set_source_rgba(0.85, 0.87, 0.9, 1)
    cr.set_line_width(max(2.0, 0.035 * F / zb))
    cr.arc(gx, gy, 0.07 * F / zb, math.pi, 2 * math.pi)
    cr.stroke()


def _pole(cr, x, z, y0=YC, y1=YF):
    (ax, ay), (bx, by) = P(x, y0, z), P(x, y1, z)
    w = 0.045 * F / z
    for col, lw in ((INK, w + 3), (POLE, w)):
        cr.set_source_rgba(*col)
        cr.set_line_width(lw)
        cr.move_to(ax, ay)
        cr.line_to(bx, by)
        cr.stroke()
    cr.set_source_rgba(1, 1, 1, 0.35)
    cr.set_line_width(w * 0.25)
    cr.move_to(ax - w * 0.2, ay)
    cr.line_to(bx - w * 0.2, by)
    cr.stroke()


def _sitter_lap(cr, x, z, zb, s, col, col_d):
    """Thighs from the hips to the front of the cushion, so a seated bust doesn't end in a straight cut."""
    nx, ny = P(x, 0.45, z)
    fx, fy = P(x, YS, zb - 0.45)
    top = ny + 360 * s
    w0, w1 = 175 * s, 175 * s * z / (zb - 0.45)
    toon(cr, lambda c: tk.curve(c, [(nx - w0, top), (nx + w0, top), (fx + w1, fy), (fx + w1 * 0.9, fy + 12 * s),
                                    (fx - w1 * 0.9, fy + 12 * s), (fx - w1, fy)]), col, col_d, (-6, -4), None, lw=3)


def aisle(cr, t, *, sweep=1.0, back_dark=0.75, crowd=0.0, swing=0.0, you=None, old=None, lights=1.0, people=True):
    """The bus interior from the front, looking down the aisle to the back seats.
    you = face dict for the lead (row 2, left window seat); old = (eyes, tilt) for the old man (row 1, right window);
    crowd = 0..1: the shapes on the back seats and the last rows (eyes shining through the dark)."""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    sw = _sweeps(t)
    # back wall and its window
    quad(cr, [(-HW, YC, ZB), (HW, YC, ZB), (HW, YF, ZB), (-HW, YF, ZB)])
    cr.set_source_rgba(*WALL_D)
    cr.fill()
    quad(cr, [(-1.05, -0.42, ZB), (1.05, -0.42, ZB), (1.05, 0.25, ZB), (-1.05, 0.25, ZB)])
    cr.set_source_rgba(0.03, 0.04, 0.07, 1)
    cr.fill()
    bx, by = P(0, 0.2, ZB)
    glow(cr, bx, by, 60, (1, 0.1, 0.05), 0.25)
    # ceiling and floor
    quad(cr, [(-HW, YC, Z0), (HW, YC, Z0), (HW, YC, ZB), (-HW, YC, ZB)])
    cr.set_source_rgba(*hexa("#30353b"))
    cr.fill()
    quad(cr, [(-HW, YF, Z0), (HW, YF, Z0), (HW, YF, ZB), (-HW, YF, ZB)])
    cr.set_source_rgba(*hexa("#222427"))
    cr.fill()
    quad(cr, [(-0.3, YF, Z0), (0.3, YF, Z0), (0.3, YF, ZB), (-0.3, YF, ZB)])
    cr.set_source_rgba(*hexa("#2f3236"))
    cr.fill()
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.set_line_width(1.5)
    for k in range(7):
        x = -0.27 + k * 0.09
        cr.move_to(*P(x, YF, Z0 + 0.3))
        cr.line_to(*P(x, YF, ZB))
        cr.stroke()
    # ceiling lights: tubes along the middle; the last one, over the back seats, is dead
    for k in range(6):
        z0, z1 = 0.9 + k * 0.95, 0.9 + k * 0.95 + 0.55
        on = lights * (0 if k == 5 else 1) * (0.35 if k == 4 and noise(t * 11, 4) > 0.7 else 1)
        quad(cr, [(-0.18, YC, z0), (0.18, YC, z0), (0.18, YC, z1), (-0.18, YC, z1)])
        cr.set_source_rgba(*mix((0.16, 0.17, 0.18, 1), (0.88, 0.97, 0.9, 1), on))
        cr.fill()
        if on > 0:
            gx, gy = P(0, YC + 0.05, (z0 + z1) / 2)
            glow(cr, gx, gy, 0.9 * F / z0, (0.75, 0.95, 0.85), 0.16 * on)
    # side walls, windows, pillars, streetlights sliding past on the left (kerb) side
    for sx in (-1, 1):
        quad(cr, [(sx * HW, YC, Z0), (sx * HW, YC, ZB), (sx * HW, YF, ZB), (sx * HW, YF, Z0)])
        cr.set_source_rgba(*WALL)
        cr.fill()
        quad(cr, [(sx * HW, YT, Z0), (sx * HW, YT, ZB), (sx * HW, YF, ZB), (sx * HW, YF, Z0)])
        cr.set_source_rgba(*WALL_D)
        cr.fill()
        quad(cr, [(sx * HW, -0.42, 0.9), (sx * HW, -0.42, ZB - 0.25), (sx * HW, 0.42, ZB - 0.25), (sx * HW, 0.42, 0.9)])
        cr.set_source_rgba(0.03, 0.04, 0.07, 1)
        cr.fill()
        if sx < 0:
            for zs in sw:
                if 0.9 < zs < ZB - 0.25:
                    za, zb_ = max(0.9, zs - 0.35), min(ZB - 0.25, zs + 0.35)
                    quad(cr, [(-HW, -0.42, za), (-HW, -0.42, zb_), (-HW, 0.42, zb_), (-HW, 0.42, za)])
                    cr.set_source_rgba(*ORANGE, 0.55 * sweep)
                    cr.fill()
        for k in range(5):
            z = 1.0 + k * 1.3
            quad(cr, [(sx * HW, -0.42, z), (sx * HW, -0.42, z + 0.12), (sx * HW, 0.42, z + 0.12), (sx * HW, 0.42, z)])
            cr.set_source_rgba(*WALL)
            cr.fill()
    # hand rails along the ceiling, with straps
    for sx in (-1, 1):
        for k in range(12):
            za, zb_ = Z0 + 0.1 + k * 0.5, Z0 + 0.1 + (k + 1) * 0.5
            if za > ZB:
                break
            (ax, ay), (bx2, by2) = P(sx * 0.72, -0.62, za), P(sx * 0.72, -0.62, min(zb_, ZB))
            w = 0.035 * F / za
            for col, lw in ((INK, w + 2), (POLE, w)):
                cr.set_source_rgba(*col)
                cr.set_line_width(lw)
                cr.move_to(ax, ay)
                cr.line_to(bx2, by2)
                cr.stroke()
        for k in range(5):
            z = 1.2 + k * 0.8
            ax, ay = P(sx * 0.72, -0.62, z)
            L = 0.36 * F / z
            a = swing * 0.45 * math.sin(t * 7 + k * 0.9 + sx) * math.exp(-0.0 * t) + 0.04 * math.sin(t * 1.3 + k)
            ex, ey = ax + L * math.sin(a), ay + L * math.cos(a)
            cr.set_source_rgba(0.12, 0.12, 0.13, 1)
            cr.set_line_width(0.03 * F / z)
            cr.move_to(ax, ay)
            cr.line_to(ex, ey)
            cr.stroke()
            hs = 0.06 * F / z
            poly(cr, [(ex - hs, ey), (ex + hs, ey), (ex, ey + hs * 1.6)])
            cr.set_source_rgba(0.85, 0.85, 0.82, 1)
            cr.set_line_width(0.018 * F / z + 1)
            cr.stroke()
    # the back bench, then the rows from the back to the front
    _seat(cr, -1.2, 1.2, ZB - 0.05, top=0.25, seed=9)
    if crowd > 0:
        for k, (x, cap) in enumerate(((-0.8, False), (-0.25, False), (0.35, False), (0.85, False))):
            nx, ny = P(x, 0.4, ZB - 0.35)
            tk.pale_face(cr, nx, ny, 0.11, t, crowd, cap, seed=k)
    for r in range(5, -1, -1):
        zb = ROWS[r]
        for sx in (-1, 1):
            _seat(cr, sx * 0.3, sx * 1.2, zb, seed=r * 2 + (sx > 0))
        if r % 2 == 0:                                   # poles stand at the seat backs, behind the sitters
            for sx in (-1, 1):
                _pole(cr, sx * 0.3, zb - 0.02, y1=YT)
        if people and r == 1 and you is not None:
            z = zb - 0.28
            s = F / z / 1000 * 1.4
            nx, ny = P(-0.72, 0.45, z)
            _sitter_lap(cr, -0.72, z, zb, s, tk.HOOD, tk.HOOD_D)
            tk.you_bust(cr, nx, ny, s, you, t, look=(0.2, 0.1), rim=COLD_RIM, rim_from=(0, -10))
        if people and r == 0 and old is not None:
            z = zb - 0.28
            s = F / z / 1000 * 1.2
            nx, ny = P(0.72, 0.45, z)
            _sitter_lap(cr, 0.72, z, zb, s, tk.OM_COAT, tk.OM_COAT_D)
            tk.oldman_bust(cr, nx, ny, s, t, eyes=old[0], tilt=old[1], rim=COLD_RIM, rim_from=(0, -10))
        if crowd > 0 and r >= 4:
            for k, x in enumerate((-0.9, -0.55, 0.6, 0.95)):
                if (k + r) % 2:
                    continue
                nx, ny = P(x, 0.45, zb - 0.28)
                tk.pale_face(cr, nx, ny, F / (zb - 0.28) / 1000 * 1.1, t, crowd, seed=r * 4 + k)
    # light from the streetlights crossing the bus, and the dark at the back
    for zs in sw:
        if Z0 < zs < ZB:
            gx, gy = P(0.4, 0.4, zs + 0.3)
            glow(cr, gx, gy, 0.9 * F / zs, ORANGE, 0.16 * sweep)
    g = cairo.RadialGradient(VX, VY, 10, VX, VY, 300)
    g.add_color_stop_rgba(0, 0, 0, 0, back_dark)
    g.add_color_stop_rgba(0.6, 0, 0, 0, back_dark * 0.5)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    if crowd > 0:                                    # their eyes shine through the dark
        pts = [(x, ZB - 0.35, 0.11) for x in (-0.8, -0.25, 0.35, 0.85)]
        pts += [(x, ROWS[r] - 0.28, F / (ROWS[r] - 0.28) / 1000 * 1.1) for r in (4, 5)
                for k, x in enumerate((-0.9, -0.55, 0.6, 0.95)) if not (k + r) % 2]
        for x, z, s in pts:
            nx, ny = P(x, 0.4 if z > ZB - 1 else 0.45, z)
            for ex in (-30, 30):
                glow(cr, nx + ex * s, ny - 154 * s, 70 * s + 4, (1, 0.95, 0.8), 0.6 * crowd)


# ------------------------------------------------------------------ other sets
def window_glass(cr, t, x0, y0, x1, y1, speed=900):
    """A night bus window: black glass, trees and streetlights streaking past, raindrops."""
    cr.save()
    tk.tk_rrect(cr, x0, y0, x1 - x0, y1 - y0, 40)
    cr.clip()
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, 0.03, 0.04, 0.08, 1)
    g.add_color_stop_rgba(1, 0.06, 0.07, 0.1, 1)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.01, 0.015, 0.02, 1)                # tree line rushing past
    off = (t * speed) % 260
    for k in range(-1, 6):
        x = x0 + k * 260 - off
        tk.curve(cr, [(x, y1), (x + 30, y0 + 420), (x + 80, y0 + 300), (x + 130, y0 + 380), (x + 190, y0 + 330),
                      (x + 260, y1)], closed=True)
        cr.fill()
    for zs in _sweeps(t, speed=4, length=6):                # a streetlight flashing by
        u = (zs - Z0) / 6
        glow(cr, x1 + 200 - u * (x1 - x0 + 500), y0 + 220, 260, ORANGE, 0.45 * math.sin(math.pi * u) ** 2)
    cr.restore()


def raindrops(cr, t, x0, y0, x1, y1, n=40, seed=3):
    for k in range(n):
        u, v = (k * 0.618 + seed * 0.1) % 1, (k * 0.7548 + seed * 0.3) % 1
        x = x0 + 20 + u * (x1 - x0 - 40)
        y = y0 + 20 + ((v + t * (0.02 + 0.05 * (k % 3 == 0))) % 1) * (y1 - y0 - 40)
        r = 3 + 4 * ((k * 0.37) % 1)
        cr.set_source_rgba(0.75, 0.85, 1, 0.22)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.45)
        cr.arc(x - r * 0.3, y - r * 0.3, r * 0.3, 0, 2 * math.pi)
        cr.fill()


def window_scene(cr, t, faces=0.0, face=None):
    """Close on your window: in the black glass, your reflection; at `faces`, three pale faces behind you."""
    cr.set_source_rgba(*WALL)
    cr.paint()
    x0, y0, x1, y1 = 50, 150, 670, 1060
    window_glass(cr, t, x0, y0, x1, y1)
    cr.save()
    tk.tk_rrect(cr, x0, y0, x1 - x0, y1 - y0, 40)
    cr.clip()
    cr.push_group()                                          # the reflection: the lit bus behind you, mirrored
    for k in range(3):
        glow(cr, 160 + k * 200, y0 + 40, 120, (0.75, 0.95, 0.85), 0.4)
    if faces > 0:
        tk.pale_face(cr, 170, 760, 0.62, t, faces, tilt=-0.08, seed=1)
        tk.pale_face(cr, 560, 740, 0.56, t, faces, cap=True, tilt=0.06, seed=2)       # the old man's cap: rewatch detail
        tk.pale_face(cr, 365, 560, 0.48, t, faces, seed=3)
    tk.you_bust(cr, 360, 1110, 1.25, face or tk.face_mix("uneasy", "uneasy", 0), t, look=(0, 0.1), blink=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(0.55)
    if faces > 0:                                             # their eyes are not faint like a reflection
        for (x, y, s) in ((170, 760, 0.62), (560, 740, 0.56), (365, 560, 0.48)):
            for ex in (-30, 30):
                glow(cr, x + ex * s, y - 154 * s, 40 * s + 8, (1, 0.95, 0.8), 0.7 * faces)
    raindrops(cr, t, x0, y0, x1, y1)
    g = cairo.LinearGradient(x0, y0, x1, y1)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.1)
    g.add_color_stop_rgba(0.45, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.06)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    for col, lw in ((INK, 30), (hexa("#15171a"), 24)):        # rubber seal
        tk.tk_rrect(cr, x0, y0, x1 - x0, y1 - y0, 40)
        cr.set_source_rgba(*col)
        cr.set_line_width(lw)
        cr.stroke()
    toon(cr, lambda c: c.rectangle(-10, y1 + 30, W + 20, 40), hexa("#5a636b"), hexa("#3b434a"), (0, -5), None, lw=4)


def road_view(cr, t, speed=1.0):
    """Through the windshield: a dark road in the headlights, trees, the centre line rushing at you."""
    g = cairo.LinearGradient(0, 0, 0, 560)
    g.add_color_stop_rgba(0, 0.02, 0.03, 0.07, 1)
    g.add_color_stop_rgba(1, 0.06, 0.08, 0.14, 1)
    cr.set_source(g)
    cr.paint()
    hy = 560
    cr.set_source_rgba(0.02, 0.03, 0.03, 1)
    for k in range(-2, 12):
        x = k * 70 + 20 * math.sin(k * 2.1)
        tk.curve(cr, [(x - 40, hy), (x - 10, hy - 140 - 40 * ((k * 0.37) % 1)), (x + 30, hy - 120), (x + 40, hy)])
        cr.fill()
    poly(cr, [(330, hy), (390, hy), (W + 300, H), (-300, H)])
    g = cairo.LinearGradient(0, hy, 0, H)
    g.add_color_stop_rgba(0, 0.12, 0.11, 0.1, 1)
    g.add_color_stop_rgba(1, 0.42, 0.36, 0.28, 1)
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(0.95, 0.85, 0.4, 0.9)
    for k in range(8):
        u = ((k / 8) + t * 0.9 * speed) % 1
        z = 1 / (0.05 + u * 0.95)
        ya, yb = hy + (H - hy) * (1 / z), hy + (H - hy) * min(1.2, 1 / z * 1.35)
        wa, wb = 2 + 22 / z, 2 + 30 / z
        poly(cr, [(360 - wa, ya), (360 + wa, ya), (360 + wb, yb), (360 - wb, yb)])
        cr.fill()
    glow(cr, 360, hy + 60, 360, (1, 0.85, 0.6), 0.25)


def mirror_scene(cr, t, glint=0.0, behind=0.0):
    """The driver's rear-view mirror: his eyes on you. behind = shapes standing in the aisle behind you."""
    hud2d.blurred(cr, lambda c: road_view(c, t), sigma=9)
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.paint()
    mx, my, mw, mh = 360, 500, 620, 250
    cr.set_source_rgba(0.12, 0.12, 0.14, 1)
    cr.rectangle(mx - 14, 0, 28, my - mh / 2)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, mx - mw / 2 - 18, my - mh / 2 - 18, mw + 36, mh + 36, 30), hexa("#2a2d33"),
         hexa("#16181c"), (-6, -5), (0.8, 0.85, 0.9, 0.5), (0, -6), lw=6)
    cr.save()
    tk.tk_rrect(cr, mx - mw / 2, my - mh / 2, mw, mh, 20)
    cr.clip()
    cr.save()                                                 # in the mirror: the bus behind you, small and dark
    cr.translate(mx, my + 60)
    cr.scale(0.55, 0.55)
    cr.translate(-VX, -VY)
    aisle(cr, t, sweep=0.6, back_dark=0.9, crowd=behind, people=False)
    cr.restore()
    cr.save()
    cr.translate(mx - 70, my - 10)
    cr.push_group()
    tk.driver_eyes(cr, t, w=470, h=170, look=(0.15, 0.1), glint=glint)
    cr.pop_group_to_source()
    m = cairo.LinearGradient(-235, 0, 235, 0)                 # his face fades into the dark of the mirror
    m.add_color_stop_rgba(0, 0, 0, 0, 1)
    m.add_color_stop_rgba(0.75, 0, 0, 0, 1)
    m.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.mask(m)
    cr.restore()
    g = cairo.LinearGradient(mx - mw / 2, my - mh / 2, mx + mw / 2, my + mh / 2)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.14)
    g.add_color_stop_rgba(0.4, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.05)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def route_card(cr, t, k):
    """The route map on the bus wall: six stops to yours; the forest between Pine Gate and Lake Road has none."""
    hud2d.blurred(cr, lambda c: aisle(c, t, old=(0, 0.2)), sigma=10)
    cr.set_source_rgba(0, 0, 0, 0.4)
    cr.paint()
    cr.save()
    cr.translate(360, 515)
    cr.rotate(-0.02)
    toon(cr, lambda c: tk.tk_rrect(c, -280, -345, 560, 690, 22), hexa("#f1ead6"), hexa("#d8cdb0"), (-10, -8), None, lw=5)
    cr.set_source_rgba(*TEAL)
    tk.tk_rrect(cr, -280, -345, 560, 100, 22)
    cr.fill()
    hud2d._text(cr, "ROUTE 9", -250, -278, 54, CREAM, hud2d.ROUND)
    hud2d._text(cr, "NIGHT SERVICE", 250, -280, 24, CREAM, hud2d.MONO, "right")
    stops = ["TOWN SQUARE", "MILL ROAD", "PINE GATE", "LAKE ROAD", "HILLCREST", "ELM STREET", "HOME"]
    ys = [-190, -120, -50, 120, 190, 250, 300]
    x = -170
    cr.set_source_rgba(*hud2d.RED)
    cr.set_line_width(12)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x, ys[0])
    cr.line_to(x, ys[0] + (ys[-1] - ys[0]) * clamp01(k * 1.4))
    cr.stroke()
    for i, (y, name) in enumerate(zip(ys, stops)):
        if k * 1.4 < (y - ys[0]) / (ys[-1] - ys[0]):
            break
        home = name == "HOME"
        cr.arc(x, y, 20 if home else 15, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*(hud2d.RED if home else INK))
        cr.set_line_width(6)
        cr.stroke()
        hud2d._text(cr, name, x + 45, y + 12, 36 if home else 32, hud2d.RED if home else INK, hud2d.ROUND)
    if k * 1.4 > 0.5:                                        # the forest: trees, and no stop
        for j in range(5):
            tx, ty = x + 60 + j * 52, 40 + 14 * (j % 2)
            toon(cr, lambda c, tx=tx, ty=ty: poly(c, [(tx, ty - 46), (tx + 22, ty + 8), (tx - 22, ty + 8)]),
                 hexa("#2e6b45"), hexa("#1d4a2f"), (-4, -3), None, lw=3)
        hud2d._text(cr, "FOREST · NO STOPS", x + 40, 90, 22, hexa("#2e6b45"), hud2d.MONO)
    if t % 0.8 < 0.55:                                       # YOU ARE HERE
        glow(cr, x, ys[0], 50, (1, 0.3, 0.2), 0.5)
    hud2d._text(cr, "YOU", x - 110, ys[0] + 12, 30, hud2d.RED, hud2d.ROUND)
    if k > 0.75:
        cr.set_source_rgba(*hud2d.RED)
        cr.set_line_width(5)
        cr.move_to(225, ys[1])
        cr.line_to(245, ys[1])
        cr.line_to(245, ys[-1])
        cr.line_to(225, ys[-1])
        cr.stroke()
        hud2d._text(cr, "6", 262, (ys[1] + ys[-1]) / 2 + 18, 56, hud2d.RED, hud2d.ROUND)
    cr.restore()


def shelter(cr, t, x0, y0, x1, y1):
    """Outside the door at Mill Road: wet pavement, an empty shelter, one lamp, rain. Nobody."""
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, 0.03, 0.04, 0.07, 1)
    g.add_color_stop_rgba(1, 0.08, 0.08, 0.1, 1)
    cr.set_source(g)
    cr.paint()
    gy = y0 + (y1 - y0) * 0.72
    cr.set_source_rgba(0.12, 0.12, 0.14, 1)
    cr.rectangle(x0, gy, x1 - x0, y1 - gy)
    cr.fill()
    flick = 0.55 if noise(t * 9, 2) > 0.75 else 1.0
    lx = x0 + 70
    cr.set_source_rgba(0.1, 0.1, 0.11, 1)
    cr.rectangle(lx - 6, y0 + 60, 12, gy - y0 - 60)
    cr.fill()
    poly(cr, [(lx - 8, y0 + 70), (lx + 30, y0 + 70), (lx + 260, gy + 40), (lx - 120, gy + 40)])
    g = cairo.LinearGradient(0, y0 + 70, 0, gy + 40)
    g.add_color_stop_rgba(0, *ORANGE, 0.35 * flick)
    g.add_color_stop_rgba(1, *ORANGE, 0.05 * flick)
    cr.set_source(g)
    cr.fill()
    glow(cr, lx + 10, y0 + 70, 80, ORANGE, 0.8 * flick)
    sx0, sx1, st = x0 + 150, x1 - 30, gy - 330                 # the shelter: glass panels, a bench, a sign
    for k in range(3):
        cr.rectangle(sx0 + k * (sx1 - sx0) / 3 + 6, st + 20, (sx1 - sx0) / 3 - 12, 300)
    cr.set_source_rgba(0.55, 0.7, 0.8, 0.12)
    cr.fill()
    cr.set_source_rgba(0.35, 0.37, 0.4, 1)
    cr.set_line_width(8)
    cr.rectangle(sx0, st, sx1 - sx0, 330)
    cr.stroke()
    cr.rectangle(sx0 - 14, st - 22, sx1 - sx0 + 28, 26)
    cr.fill()
    toon(cr, lambda c: c.rectangle(sx0 + 40, gy - 110, sx1 - sx0 - 80, 18), hexa("#6b5a45"), hexa("#4a3d2f"), (0, -4),
         None, lw=3)
    toon(cr, lambda c: c.rectangle(sx0 + 50, gy - 92, 10, 92), hexa("#2d2f33"), None, (0, 0), None, lw=2)
    toon(cr, lambda c: c.rectangle(sx1 - 60, gy - 92, 10, 92), hexa("#2d2f33"), None, (0, 0), None, lw=2)
    toon(cr, lambda c: tk.tk_rrect(c, sx1 - 150, st + 40, 110, 46, 6), hexa("#1f6a63"), None, (0, 0), None, lw=3)
    hud2d._text(cr, "MILL RD", sx1 - 95, st + 72, 22, CREAM, hud2d.ROUND, "center")
    for k in range(6):                                        # reflections in the wet ground
        cr.set_source_rgba(*ORANGE, 0.12)
        cr.rectangle(lx - 20 + k * 8, gy + 20 + k * 22, 30, 6)
        cr.fill()
    cr.set_source_rgba(0.7, 0.8, 0.95, 0.25)                 # rain
    cr.set_line_width(2)
    for k in range(40):
        x = x0 + (k * 53.7) % (x1 - x0)
        y = y0 + ((k * 91.3 + t * 900) % (y1 - y0 + 80)) - 40
        cr.move_to(x, y)
        cr.line_to(x - 6, y + 34)
        cr.stroke()


def forest(cr, t, x0, y0, x1, y1, door_light=1.0, fog=1.0):
    """The forest at the stop that isn't a stop: no streetlight, no shelter; just the light from the bus door."""
    cr.set_source_rgba(0.015, 0.02, 0.03, 1)
    cr.paint()
    gy = y0 + (y1 - y0) * 0.7
    for layer, (col, n, wmin) in enumerate((((0.05, 0.07, 0.08), 9, 14), ((0.03, 0.045, 0.05), 6, 30),
                                            ((0.01, 0.015, 0.02), 4, 60))):
        cr.set_source_rgba(*col, 1)
        for k in range(n):
            x = x0 + ((k * 0.618 + layer * 0.3) % 1) * (x1 - x0)
            w = wmin + 10 * ((k * 0.37) % 1)
            cr.rectangle(x - w / 2, y0, w, gy - y0 + 40 * layer)
            cr.fill()
        if fog:
            g = cairo.LinearGradient(0, gy - 200, 0, gy + 60)
            g.add_color_stop_rgba(0, 0.5, 0.6, 0.65, 0)
            g.add_color_stop_rgba(1, 0.5, 0.6, 0.65, 0.07 * fog)
            cr.set_source(g)
            cr.rectangle(x0, gy - 200, x1 - x0, 260)
            cr.fill()
    cr.set_source_rgba(0.06, 0.06, 0.06, 1)
    cr.rectangle(x0, gy, x1 - x0, y1 - gy)
    cr.fill()
    poly(cr, [(x0 + 40, y1), (x0 + 150, gy), (x1 - 150, gy), (x1 - 40, y1)])     # the door's light on the gravel
    g = cairo.LinearGradient(0, y1, 0, gy)
    g.add_color_stop_rgba(0, 0.8, 0.95, 0.85, 0.45 * door_light)
    g.add_color_stop_rgba(1, 0.8, 0.95, 0.85, 0.05 * door_light)
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(0.3, 0.3, 0.28, 0.5)
    for k in range(60):
        x = x0 + 60 + ((k * 0.618) % 1) * (x1 - x0 - 120)
        y = gy + 10 + ((k * 0.382) % 1) * (y1 - gy - 10)
        cr.arc(x, y, 1.5 + 2.5 * (y - gy) / (y1 - gy), 0, 2 * math.pi)
        cr.fill()


def door_scene(cr, t, open_k, outside="shelter", fig=None):
    """Looking at the front door from inside: steps down, yellow poles, folding glass leaves; outside beyond."""
    x0, y0, x1, y1 = 150, 170, 570, 1130
    cr.set_source_rgba(*WALL)
    cr.paint()
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    if outside == "shelter":
        shelter(cr, t, x0, y0, x1, y1)
    else:
        forest(cr, t, x0, y0, x1, y1, door_light=open_k)
        if fig:
            fig(cr)
    cr.restore()
    for k, (yy, dy) in enumerate(((y1 - 160, 80), (y1 - 80, 80))):        # the steps, edged in yellow
        cr.set_source_rgba(0.13, 0.13, 0.14, 1)
        cr.rectangle(x0, yy, x1 - x0, dy)
        cr.fill()
        cr.set_source_rgba(*POLE)
        cr.rectangle(x0, yy, x1 - x0, 10)
        cr.fill()
    half = (x1 - x0) / 2
    for side in (-1, 1):                                       # two folding leaves each side
        w = half * (1 - 0.82 * open_k)
        ex = x0 if side < 0 else x1 - w
        for j in range(2):
            lx = ex + j * w / 2
            cr.save()
            cr.rectangle(lx, y0, w / 2, y1 - 160 - y0)
            cr.set_source_rgba(0.1, 0.12, 0.14, 0.92)
            cr.fill_preserve()
            cr.set_source_rgba(*INK)
            cr.set_line_width(5)
            cr.stroke()
            cr.rectangle(lx + 8, y0 + 10, w / 2 - 16, y1 - 180 - y0)
            cr.set_source_rgba(0.5, 0.65, 0.75, 0.12)
            cr.fill()
            cr.restore()
    for col, lw in ((INK, 34), (WALL_D, 26)):                 # the door frame
        cr.rectangle(x0, y0, x1 - x0, y1 - y0)
        cr.set_source_rgba(*col)
        cr.set_line_width(lw)
        cr.stroke()
    for x in (x0 - 40, x1 + 40):                               # grab poles beside the door
        for col, lw in ((INK, 30), (POLE, 24)):
            cr.set_source_rgba(*col)
            cr.set_line_width(lw)
            cr.move_to(x, 0)
            cr.line_to(x, H)
            cr.stroke()
        cr.set_source_rgba(1, 1, 1, 0.35)
        cr.set_line_width(5)
        cr.move_to(x - 6, 0)
        cr.line_to(x - 6, H)
        cr.stroke()
    g = cairo.LinearGradient(0, 0, 0, H)                       # fluorescent wash from above
    g.add_color_stop_rgba(0, 0.75, 0.95, 0.85, 0.22)
    g.add_color_stop_rgba(0.6, 0.75, 0.95, 0.85, 0.0)
    cr.set_source(g)
    cr.paint()


# ------------------------------------------------------------------ outside the bus
def sign_text(cr, txt, x, y, w, h, col=(1, 0.62, 0.15), a=1.0):
    """Amber dot-matrix destination text in a black box."""
    cr.save()
    tk.tk_rrect(cr, x - w / 2, y - h / 2, w, h, 6)
    cr.set_source_rgba(0.02, 0.02, 0.02, 1)
    cr.fill()
    glow(cr, x, y, w * 0.6, col, 0.12 * a)
    sz = h * 0.62
    tw = hud.text_width(cr, txt, sz, "Liberation Mono")
    sz *= min(1, (w - 24) / tw)
    hud2d._text(cr, txt, x, y + sz * 0.36, sz, (*col, a), "Liberation Mono", "center")
    cr.set_source_rgba(0, 0, 0, 0.55)                        # the dot grid
    for gx in range(int(x - w / 2), int(x + w / 2), 5):
        cr.rectangle(gx, y - h / 2, 1.5, h)
    for gy in range(int(y - h / 2), int(y + h / 2), 5):
        cr.rectangle(x - w / 2, gy, w, 1.5)
    cr.fill()
    cr.restore()


def bus_front(cr, x, y, s, t, sign="9  HOME", sign_flick=0.0, lights=1.0):
    """Route 9 head-on: wheels at (x, y), ~540 x 620 px at s = 1."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_source_rgba(0, 0, 0, 0.5)
    cr.save()
    cr.scale(1, 0.12)
    cr.arc(0, 0, 320, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: tk.tk_rrect(c, sx * 205 - 40, -70, 80, 80, 14), hexa("#121315"), None, (0, 0), None,
             lw=4)
    toon(cr, lambda c: tk.tk_rrect(c, -265, -620, 530, 590, 34), TEAL, TEAL_D, (-14, -10), None, lw=6)
    toon(cr, lambda c: c.rectangle(-265, -205, 530, 40), CREAM, mix(CREAM, INK, 0.25), (0, -6), None, lw=4)
    for sx in (-1, 1):                                       # windshield panes
        toon(cr, lambda c, sx=sx: tk.tk_rrect(c, (0 if sx > 0 else -238) + 4 * sx, -480, 234, 262, 14),
             hexa("#0d1219"), None, (0, 0), None, lw=5)
    cr.save()
    tk.tk_rrect(cr, -238, -480, 476, 262, 14)
    cr.clip()
    g = cairo.LinearGradient(0, -480, 0, -218)
    g.add_color_stop_rgba(0, 0.25, 0.35, 0.3, 0.6 * lights)
    g.add_color_stop_rgba(1, 0.05, 0.08, 0.08, 0.3 * lights)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.02, 0.02, 0.03, 0.95)               # the driver behind the glass: a cap and shoulders
    tk.curve(cr, [(-200, -218), (-190, -300), (-150, -330), (-110, -300), (-100, -218)])
    cr.fill()
    cr.arc(-150, -360, 34, 0, 2 * math.pi)
    cr.fill()
    cr.rectangle(-196, -392, 92, 16)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.12)
    poly(cr, [(40, -480), (110, -480), (-20, -218), (-90, -218)])
    cr.fill()
    cr.restore()
    cr.set_source_rgba(*INK)
    cr.set_line_width(10)
    cr.move_to(0, -480)
    cr.line_to(0, -218)
    cr.stroke()
    on = 0.4 if sign_flick and noise(t * 23, 1) > 0.2 else 1.0
    sign_text(cr, sign, 0, -553, 420, 72, a=on)
    for sx in (-1, 1):                                       # wipers, mirrors on their arms, headlights
        cr.set_source_rgba(*INK)
        cr.set_line_width(6)
        cr.move_to(sx * 40, -222)
        cr.line_to(sx * 170, -262)
        cr.stroke()
        cr.set_line_width(10)
        cr.move_to(sx * 262, -560)
        cr.curve_to(sx * 330, -560, sx * 340, -520, sx * 322, -470)
        cr.stroke()
        toon(cr, lambda c, sx=sx: tk.tk_rrect(c, sx * 322 - 22, -500, 44, 90, 10), hexa("#16181c"), None, (0, 0), None,
             lw=4)
        for k in range(2):
            hx = sx * (190 - k * 60)
            toon(cr, lambda c, hx=hx: c.arc(hx, -105, 26, 0, 2 * math.pi), (1, 0.97, 0.85, 1), None, (0, 0), None, lw=4)
            glow(cr, hx, -105, 150, (1, 0.95, 0.8), 0.5 * lights)
    toon(cr, lambda c: tk.tk_rrect(c, -90, -150, 180, 80, 10), hexa("#16191c"), None, (0, 0), None, lw=4)
    cr.set_source_rgba(0.3, 0.32, 0.35, 1)
    cr.set_line_width(3)
    for k in range(5):
        cr.move_to(-80, -140 + k * 15)
        cr.line_to(80, -140 + k * 15)
        cr.stroke()
    toon(cr, lambda c: tk.tk_rrect(c, -275, -62, 550, 46, 16), hexa("#1a1c1f"), None, (0, 0), None, lw=5)
    cr.restore()
    for sx in (-1, 1):                                       # flare
        glow(cr, x + sx * 160 * s, y - 105 * s, 420 * s, (1, 0.95, 0.85), 0.18 * lights)


def night_road(cr, t, town=1.0):
    """A two-lane road out of town at night: hills, the town's glow behind, streetlights that end."""
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgba(0, 0.02, 0.03, 0.08, 1)
    g.add_color_stop_rgba(1, 0.1, 0.1, 0.18, 1)
    cr.set_source(g)
    cr.paint()
    hy = 720
    glow(cr, 360, hy, 520, (1, 0.6, 0.3), 0.3 * town)
    for k in range(30):
        x = 80 + (k * 47.3) % 560
        cr.set_source_rgba(1, 0.75, 0.4, 0.7 * town)
        cr.arc(x, hy - 6 - (k * 7) % 22, 2.2, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(0.03, 0.04, 0.06, 1)
    tk.curve(cr, [(-100, hy + 30), (120, hy - 40), (300, hy + 10), (500, hy - 60), (820, hy + 20), (820, H), (-100, H)])
    cr.fill()
    poly(cr, [(345, hy), (375, hy), (W + 220, H), (-220, H)])
    cr.set_source_rgba(0.12, 0.12, 0.13, 1)
    cr.fill()
    for k in range(5):                                       # streetlights stepping toward you
        z = 1 + k * 1.6
        sx_ = 360 + 260 * 1.8 / z
        lyt = hy - 300 / z
        cr.set_source_rgba(0.08, 0.08, 0.09, 1)
        cr.set_line_width(max(2, 12 / z))
        cr.move_to(sx_, hy + 420 / z)
        cr.line_to(sx_, lyt)
        cr.line_to(sx_ - 60 / z, lyt)
        cr.stroke()
        glow(cr, sx_ - 60 / z, lyt + 6 / z, 140 / z + 20, ORANGE, 0.55)
        glow(cr, sx_ - 80 / z, hy + 300 / z, 260 / z + 30, ORANGE, 0.18)


def bus_side(cr, t, door=1.0):
    """Stopped in the forest, seen from the side: front half of the bus, its door open and spilling light. In the
    back windows, shapes."""
    forest(cr, t, 0, 0, W, H, door_light=0, fog=1.0)
    glow(cr, -60, 800, 520, (1, 0.95, 0.8), 0.35)           # headlights into the trees
    poly(cr, [(60, 760), (-200, 560), (-200, 1020)])
    cr.set_source_rgba(1, 0.95, 0.8, 0.12)
    cr.fill()
    gy = 1000
    poly(cr, [(150, gy), (290, gy), (520, H), (-60, H)])     # the door's light on the gravel
    g = cairo.LinearGradient(0, gy, 0, H)
    g.add_color_stop_rgba(0, 0.8, 0.95, 0.85, 0.55 * door)
    g.add_color_stop_rgba(1, 0.8, 0.95, 0.85, 0.08 * door)
    cr.set_source(g)
    cr.fill()
    body = lambda c: tk.curve(c, [(60, 470), (110, 400), (900, 400), (900, 990), (70, 990), (50, 900)])
    toon(cr, body, TEAL, TEAL_D, (-10, -8), None, lw=6)
    toon(cr, lambda c: c.rectangle(55, 800, 860, 34), CREAM, mix(CREAM, INK, 0.25), (0, -5), None, lw=4)
    toon(cr, lambda c: poly(c, [(66, 470), (110, 420), (140, 420), (140, 780), (58, 780)]), hexa("#0d1219"), None,
         (0, 0), None, lw=5)
    sign_text(cr, "9  HOME", 520, 435, 300, 44)
    cr.save()                                                # the open door: the lit stairwell inside
    cr.rectangle(160, 460, 130, 520)
    cr.clip()
    g = cairo.LinearGradient(0, 460, 0, 980)
    g.add_color_stop_rgba(0, 0.85, 0.97, 0.9, 1)
    g.add_color_stop_rgba(1, 0.45, 0.55, 0.5, 1)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(*WALL)
    cr.rectangle(160, 460, 130, 120)
    cr.fill()
    for k in range(2):                                       # steps up into the bus
        cr.set_source_rgba(0.2, 0.22, 0.24, 1)
        cr.rectangle(160, 880 + k * 50, 130, 50)
        cr.fill()
        cr.set_source_rgba(*POLE)
        cr.rectangle(160, 880 + k * 50, 130, 8)
        cr.fill()
    _pole_flat = lambda x: (cr.set_source_rgba(*INK), cr.rectangle(x - 9, 460, 18, 520), cr.fill(),
                            cr.set_source_rgba(*POLE), cr.rectangle(x - 6, 460, 12, 520), cr.fill())
    _pole_flat(270)
    for side in (0, 1):                                      # the door leaves, folded back
        cr.set_source_rgba(0.1, 0.12, 0.14, 0.9)
        cr.rectangle(160 + side * (130 - 22 * door - 4), 460, 4 + 22 * (1 - door) * 3 + 22 * door, 520)
        cr.fill()
    cr.restore()
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.rectangle(160, 460, 130, 520)
    cr.stroke()
    for k in range(4):                                       # side windows: you, empty, shapes at the back
        wx = 320 + k * 150
        toon(cr, lambda c, wx=wx: tk.tk_rrect(c, wx, 480, 130, 220, 14), hexa("#2f4a42"), None, (0, 0), None, lw=5)
        cr.save()
        tk.tk_rrect(cr, wx, 480, 130, 220, 14)
        cr.clip()
        g = cairo.LinearGradient(0, 480, 0, 700)
        g.add_color_stop_rgba(0, 0.75, 0.95, 0.85, 0.55)
        g.add_color_stop_rgba(1, 0.3, 0.45, 0.4, 0.4)
        cr.set_source(g)
        cr.paint()
        if k == 1:                                           # your seat: your silhouette
            cr.set_source_rgba(0.05, 0.08, 0.1, 0.95)
            cr.arc(wx + 65, 600, 30, 0, 2 * math.pi)
            cr.fill()
            tk.curve(cr, [(wx + 15, 700), (wx + 35, 640), (wx + 95, 640), (wx + 115, 700)])
            cr.fill()
        if k >= 2:                                           # the back: shapes with eyes
            for j in range(2):
                hx = wx + 35 + j * 60
                cr.set_source_rgba(0.03, 0.04, 0.05, 0.95)
                cr.arc(hx, 612 - 8 * j, 26, 0, 2 * math.pi)
                cr.fill()
                tk.curve(cr, [(hx - 40, 700), (hx - 30, 650), (hx + 30, 650), (hx + 40, 700)])
                cr.fill()
                for ex in (-9, 9):
                    glow(cr, hx + ex, 608 - 8 * j, 12, (1, 0.95, 0.8), 0.8)
        cr.restore()
    for wx in (300, 860):                                     # wheels
        toon(cr, lambda c, wx=wx: c.arc(wx, 990, 72, 0, 2 * math.pi), hexa("#141518"), None, (0, 0), None, lw=5)
        toon(cr, lambda c, wx=wx: c.arc(wx, 990, 34, 0, 2 * math.pi), hexa("#6d7075"), hexa("#45474b"), (-4, -3), None,
             lw=4)
    toon(cr, lambda c: c.arc(70, 930, 18, 0, 2 * math.pi), (1, 0.97, 0.85, 1), None, (0, 0), None, lw=4)
    glow(cr, 70, 930, 140, (1, 0.95, 0.8), 0.6)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0, pan=(0, 0)):
    """A slow push-in with handheld drift, plus the bus's own sway."""
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1) + pan[0] * k, cy + 3 * shake * noise(t * 0.6, 4) + pan[1] * k
                 + 2.5 * math.sin(t * 5.3))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7) + 0.003 * math.sin(t * 1.1))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "face_hook"), (B["b2"].start - 0.2, "road"), (A("b2", "Just") - 0.15, "aisle"),
        (B["b3"].start - 0.2, "route"), (B["b4"].start - 0.2, "stop"), (B["b5"].start - 0.2, "dip"),
        (B["b6"].start - 0.2, "face_creak"), (B["b7"].start - 0.2, "mirror"), (B["b8"].start - 0.2, "window"),
        (B["b9"].start - 0.2, "phone"), (B["b11"].start - 0.2, "bus_front"), (B["b12"].start - 0.2, "oldman"),
        (B["b13"].start - 0.2, "oldman_close"), (B["b14"].start - 0.2, "neck"), (B["b15"].start - 0.2, "forest"),
        (B["b16"].start - 0.2, "mirror2"), (B["b17"].start - 0.2, "out"), (B["b17c"].start - 0.2, "convex"),
        (B["b18"].start - 0.2, "choice"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_dip = A("b5", "dips.", end=True) + 0.2
    t_faces = A("b8", "faces", end=True)
    cold = ((0.92, 1.0, 0.96), (0.55, 0.62, 0.66))

    cr.save()
    if name == "face_hook":
        camera(cr, t, s0, s1, 1.0, 1.07)
        hud2d.blurred(cr, lambda c: aisle(c, t, old=(0, 0.2)))
        f = tk.face_mix("calm", "uneasy", seg(t, A("b1", "Whatever") - 0.2, A("b1", "Whatever") + 0.4))
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.1, -0.1), rim=COLD_RIM, rim_from=(-10, -4))
        grade(cr, *cold)
    elif name == "road":
        camera(cr, t, s0, s1, 1.0, 1.12, cy=720)
        night_road(cr, t)
        k2 = seg(t, s0, s1)
        bus_front(cr, 360, 760 + 180 * k2, 0.42 + 0.3 * k2, t, sign="9  LAST BUS")
    elif name == "aisle":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=640)
        aisle(cr, t, you=tk.face_mix("calm", "calm", 0), old=(0, 0.22))
        grade(cr, *cold)
    elif name == "route":
        camera(cr, t, s0, s1, 1.0, 1.05)
        route_card(cr, t, seg(t, s0 + 0.05, s0 + 0.75))
    elif name == "stop":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=640)
        door_scene(cr, t, seg(t, B["b4"].start + 0.1, B["b4"].start + 1.0), "shelter")    # with the doors sound
    elif name == "dip":
        drop = 26 * math.exp(-max(0.0, t - t_dip) * 3.5) * math.sin(max(0.0, t - t_dip) * 14) if t > t_dip else 0
        cr.translate(0, drop)
        cr.rotate(-0.012 * (drop / 26))
        camera(cr, t, s0, s1, 1.04, 1.1, cy=640, shake=1.0 + (2.5 if t > t_dip else 0) * math.exp(-max(0, t - t_dip) * 2))
        aisle(cr, t, you=tk.face_mix("uneasy", "alarmed", seg(t, t_dip, t_dip + 0.3)), old=(0, 0.22),
              swing=1.0 if t > t_dip else 0.15)
        grade(cr, *cold)
    elif name in ("face_creak", "neck"):
        neck = name == "neck"
        camera(cr, t, s0, s1, 1.04, 1.12, shake=1.0 + 1.5 * neck)
        hud2d.blurred(cr, lambda c: aisle(c, t, old=(0, 0.2), back_dark=0.9, crowd=0.0, lights=0.85))
        if neck:                                              # something right behind you, out of focus
            hud2d.blurred(cr, lambda c: tk.pale_face(c, 170, 860, 1.6, t, 0.9, seed=5), sigma=14)
        f = (tk.face_mix("alarmed", "terror", seg(t, A("b14", "breathes") - 0.1, A("b14", "breathes") + 0.3)) if neck
             else tk.face_mix("uneasy", "alarmed", seg(t, A("b6", "creaks.") - 0.1, A("b6", "creaks.") + 0.3)))
        look = (-1.0, 0.1) if neck or t > A("b6", "creaks.") else (-0.3, 0)
        tk.you_bust(cr, 380, 930, 1.42, f, t, look=look, turn=-0.12, rim=COLD_RIM, rim_from=(-10, -4),
                    sweat=1.0 if neck else 0.5, tremble=0.6 if neck else 0.0)
        if neck:                                              # cold breath curling past your neck
            for j in range(3):
                ph = (t * 0.6 + j * 0.33) % 1
                glow(cr, 170 + 120 * ph, 720 - 40 * j + 30 * math.sin(t * 2 + j), 70 + 40 * ph, (0.8, 0.9, 1),
                     0.25 * math.sin(math.pi * ph))
        grade(cr, *cold)
    elif name in ("mirror", "mirror2"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=500)
        two = name == "mirror2"
        mirror_scene(cr, t, glint=0.8 if two else 0.0, behind=0.9 if two else 0.0)
    elif name == "window":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=700)
        f = tk.face_mix("uneasy", "terror", seg(t, t_faces - 0.1, t_faces + 0.3))
        window_scene(cr, t, faces=seg(t, t_faces - 0.35, t_faces), face=f)
    elif name == "phone":
        camera(cr, t, s0, s1, 1.0, 1.04, shake=0.6)
        hud2d.blurred(cr, lambda c: (aisle(c, t, old=(0, 0.2)), grade(c, *cold)), sigma=10)
        notes = [(B["b9"].start + 0.25, "CITYBUS LIVE", "Route 9 · Live tracker", "Where is your bus? Tap to see."),
                 (A("b10", "Out") - 0.25, "CITYBUS LIVE", "Route 9: OUT OF SERVICE", "In the depot since 10:40 PM.",
                  False)]                     # silent: its buzz under "out of service" was heard as "out of Cervith"
        hud2d.phone_pov(cr, t, s0, "11:58", "Saturday", notes, skin=mix(tk.SKIN, (0.55, 0.7, 1.0, 1), 0.25))
    elif name == "bus_front":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=760)
        night_road(cr, t, town=0.0)
        bus_front(cr, 360, 1130, 1.18, t, sign="NOT IN SERVICE" if t > B["b11"].start + 0.25 else "9  HOME",
                  sign_flick=1.0 if t < B["b11"].start + 0.6 else 0.0)
        grade(cr, (0.85, 0.9, 1.0), (0.5, 0.5, 0.6))
    elif name in ("oldman", "oldman_close"):
        close = name == "oldman_close"
        camera(cr, t, s0, s1, 1.0, 1.1 if close else 1.06, shake=0.8)

        def bg(c):
            c.set_source_rgba(*WALL)
            c.paint()
            window_glass(c, t, 380, 100, 760, 900)
        hud2d.blurred(cr, bg, sigma=8)
        sweep = max(0.0, math.sin(t * 2.2)) ** 6
        if close:
            talk = 0.4 + 0.4 * math.sin(t * 13) if B["b13"].start <= t <= B["b13"].end else 0.0
            tk.oldman_bust(cr, 380, 1240, 1.95, t, eyes=1.0, look=(-0.1, 0.1), mouth=talk, tilt=-0.05,
                           rim=COLD_RIM, rim_from=(10, -4))
        else:
            eyes = seg(t, A("b12", "opens") - 0.1, A("b12", "eyes.", end=True))
            lean = seg(t, A("b12", "leans") - 0.1, A("b12", "leans") + 0.6)
            sc = 1.3 + 0.35 * lean
            tk.oldman_bust(cr, 420 - 40 * lean, 1060 + 120 * lean, sc, t, eyes=eyes, look=(-0.6 * lean, 0.1),
                           tilt=0.22 * (1 - lean) - 0.05 * lean, rim=COLD_RIM, rim_from=(10, -4))
        glow(cr, 600, 500, 380, ORANGE, 0.22 * sweep)
        grade(cr, *cold)
    elif name == "forest":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=760)
        bus_side(cr, t, door=seg(t, B["b15"].start + 0.6, B["b15"].start + 1.4))
    elif name in ("out", "choice"):
        camera(cr, t, s0, s1, 1.0, 1.06, cy=700)
        back = seg(t, B["b17"].start, A("b17", "dark.", end=True))          # he steps out backwards, facing you
        hand = seg(t, A("b17", "holds") - 0.1, A("b17", "hand.", end=True))
        if name == "choice":
            back, hand = 1.0, 1.0

        def fig(c):
            tk.oldman_full(c, 360 + 30 * back, 1150 - 120 * back, 1.25 - 0.45 * back, t, eyes=1.0, hand=hand,
                           look=(0, 0.2), rim=COLD_RIM, rim_from=(0, -10))
        door_scene(cr, t, 1.0, "forest", fig)
        if name == "choice":
            tk.you_back(cr, 150, 1330, 1.2, t, rim=COLD_RIM, rim_from=(-10, 0))
        grade(cr, *cold)
    elif name == "convex":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=600)
        hud2d.blurred(cr, lambda c: door_scene(c, t, 1.0, "forest"), sigma=10)
        cr.set_source_rgba(0, 0, 0, 0.45)
        cr.paint()
        cx, cy, r = 360, 600, 300
        toon(cr, lambda c: c.arc(cx, cy, r + 22, 0, 2 * math.pi), hexa("#2a2d33"), hexa("#16181c"), (-6, -5),
             (0.85, 0.9, 0.95, 0.5), (0, -6), lw=6)
        cr.save()
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.clip()
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1.9, 1.9)                                    # the mirror shows the back of the bus, big
        cr.translate(-VX, -VY - 20)
        aisle(cr, t, crowd=seg(t, s0 + 0.2, s0 + 0.9), back_dark=0.8, people=False, lights=0.7)
        cr.restore()
        g = cairo.RadialGradient(cx, cy, r * 0.5, cx, cy, r)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.7)
        cr.set_source(g)
        cr.paint()
        glow(cr, cx - 120, cy - 140, 160, (1, 1, 1), 0.12)
        cr.restore()
        grade(cr, *cold)
    cr.restore()
    hud.finish(cr, t, flash_at=[t_faces], vig=0.55, grain=0.06)
    stops = ("STOPS LEFT", "6", None) if t < B["b4"].start else ("STOPS LEFT", "5", None, B["b4"].start)
    if t >= B["b15"].start:
        stops = ("STOPS LEFT", "?", "bad", B["b15"].start)
    bumps = [(t_dip, 4), (A("b6", "creaks.", end=True), 5), (A("b6", "another.", end=True), 6), (A("b14", "breathes"), 7)]
    n, bumped = 3, None
    for at, v in bumps:
        if t >= at:
            n, bumped = v, at
    for at in (t_dip + 0.35, A("b6", "creaks.", end=True) + 0.35, A("b6", "another.", end=True) + 0.35):
        cue("click", t, at)          # the counter's click comes after the words (on "creaks" it ate the "s")
    pas = ("PASSENGERS", str(n), "bad" if n >= 6 else "warn" if n > 3 else None, bumped) if bumped else \
        ("PASSENGERS", "3", None)
    route = ("ROUTE 9", "DEPOT", "bad", A("b10", "Out")) if t >= A("b10", "Out") else ("ROUTE 9", "ON TIME", None)
    hud2d.stats(cr, t, [stops, pas, route])
    hud2d.hook(cr, t, [("ONE RULE:", False), ("DON'T LOOK AT", False), ("THE BACK SEATS", True)],
               end=B["b1"].end + 0.15, y=270)
    hud2d.rule_tag(cr, t, B["b6"].start, B["b6"].end + 0.4, "RULE: DON'T LOOK BACK", y=200)
    hud2d.rule_tag(cr, t, A("b14", "breathes"), B["b14"].end + 0.4, "RULE: DON'T LOOK BACK", y=200)
    hud2d.stamp(cr, t, t_faces, B["b8"].end + 0.4, ["3 FACES"], y=330)
    hud2d.stamp(cr, t, A("b10", "Out"), B["b10"].end + 0.3, ["OUT OF SERVICE"], y=1010, rot=-0.08)
    hud2d.bubble(cr, t, B["b7"].start, B["b7"].end, "Eyes front. Don't turn around.", 360, 860, (300, 600))
    hud2d.bubble(cr, t, B["b13"].start, B["b13"].end, "The driver isn't taking us home. Get off at the next stop. "
                 "With me.", 360, 300, (400, 560))
    hud2d.bubble(cr, t, B["b16"].start, B["b16"].end, "This isn't your stop. Sit down.", 360, 860, (300, 600))
    hud2d.ab_card(cr, t, A("b19", "get"), "GET OFF", "RIDE ON", kicker="LAST STOP · NIGHT 1 · YOUR CHOICE",
                  decides="Night 2")
    hud2d.captions(cr, t, tl, KEY, skip=("b7", "b13", "b16"))
    cue("engine_idle", t, 0.0, tl.total)
    cue("doors", t, B["b4"].start + 0.1)
    cue("dip", t, t_dip)                                       # after the words: on "the bus" it was heard as "the best"
    cue("creak", t, A("b6", "creaks.", end=True) + 0.2, 0.7)   # after the word: on it "creaks" was heard as "crease"
    cue("creak", t, A("b6", "another.", end=True) + 0.2, 0.7)
    cue("sting", t, t_faces)                                   # after "three faces": on it, "three" was lost
    cue("breath", t, B["b14"].end + 0.05)
    cue("brakes", t, B["b15"].start)
    cue("doors", t, B["b17"].start)
    cue("heartbeat", t, B["b16"].start, B["b18"].end - B["b16"].start)
    cue("riser", t, B["b18"].start, B["b19"].start - B["b18"].start)
