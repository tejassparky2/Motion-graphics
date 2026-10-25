"""Channel art for the horror channel ("Midnight with Manya", the owner's pick, 25 Oct 2026): the profile picture and the banner,
drawn in the same 2D style as the episodes. Manya is a fictional storyteller (toon2d.manya_bust).

    /home/user/.venv-main/bin/python channels/horror/brand.py   -> out/horror/channel/avatar.png, banner.png
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(ROOT, "build", "fonts.conf"))
from motion.engine import cairo   # noqa: E402
from motion.polish import text_width   # noqa: E402

from channels.horror import hud2d   # noqa: E402
from channels.horror import toon2d as tk   # noqa: E402
from channels.horror.toon2d import INK, glow, hexa, poly   # noqa: E402

NAME = "MIDNIGHT WITH MANYA"
OUT = os.path.join(ROOT, "out", "horror", "channel")
AMBER = hexa("#ffb347")


def sky(cr, w, h, seed=1):
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgba(0, *hexa("#0a0e22"))
    g.add_color_stop_rgba(1, *hexa("#1d1433"))
    cr.set_source(g)
    cr.paint()
    for k in range(int(w * h / 9000)):                       # stars
        x = (k * 0.618034 * w + seed * 131) % w
        y = (k * 0.7548777 * h * 1.3) % (h * 0.8)
        r = 0.8 + 1.6 * ((k * 0.37) % 1)
        cr.set_source_rgba(1, 1, 1, 0.25 + 0.5 * ((k * 0.53) % 1))
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.fill()


def moon(cr, x, y, r):
    glow(cr, x, y, r * 3.2, (0.75, 0.82, 1.0), 0.35)
    cr.set_source_rgba(*hexa("#eef0f7"))
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.75, 0.78, 0.88, 0.6)                # craters
    for dx, dy, rr in ((-0.3, -0.2, 0.18), (0.25, 0.1, 0.12), (-0.05, 0.4, 0.1), (0.35, -0.35, 0.08)):
        cr.arc(x + dx * r, y + dy * r, rr * r, 0, 2 * math.pi)
        cr.fill()


def avatar(path, size=800):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
    cr = cairo.Context(s)
    sky(cr, size, size, seed=3)
    moon(cr, 590, 230, 120)
    glow(cr, 400, 900, 520, (1, 0.6, 0.3), 0.45)             # her lantern, below the frame
    tk.manya_bust(cr, 400, 640, 1.55, 0.0)
    g = cairo.RadialGradient(400, 400, 300, 400, 400, 420)     # keep the edge of the circle dark
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.45)
    cr.set_source(g)
    cr.paint()
    s.write_to_png(path)


def skyline(cr, w, h, ground):
    """Silhouettes from the three stories: Floor 13's building, the night bus, Tower 9 above the forest."""
    cr.set_source_rgba(*hexa("#07080f"))
    pts = [(-20, h)]
    for x in range(-20, w + 60, 38):
        pts.append((x, ground - 40 - 46 * abs(math.sin(x * 0.021)) - 22 * ((x // 38) % 2)))
    pts.append((w + 20, h))
    poly(cr, pts)
    cr.fill()
    bx, by, bw, bh = 120, ground - 520, 260, 560              # the apartment block; one red window: 13
    cr.set_source_rgba(*hexa("#0c0d16"))
    cr.rectangle(bx, by, bw, bh)
    cr.fill()
    for r in range(11):
        for c in range(4):
            lit = (r * 7 + c * 3) % 5 == 0
            red = (r, c) == (3, 2)
            col = (1, 0.15, 0.1, 0.95) if red else (1, 0.8, 0.45, 0.85) if lit else (0.12, 0.13, 0.2, 1)
            cr.set_source_rgba(*col)
            cr.rectangle(bx + 22 + c * 60, by + 24 + r * 46, 36, 26)
            cr.fill()
            if red:
                glow(cr, bx + 40 + c * 60, by + 37 + r * 46, 70, (1, 0.15, 0.1), 0.5)
    tx, top = w - 330, ground - 560                           # the fire tower
    cr.set_source_rgba(*hexa("#090a12"))
    cr.set_line_width(9)
    for sx in (-1, 1):
        cr.move_to(tx + sx * 34, top)
        cr.line_to(tx + sx * 120, ground)
    cr.stroke()
    cr.set_line_width(4)
    for k in range(5):
        y0, y1 = top + k * (ground - top) / 5, top + (k + 1) * (ground - top) / 5
        w0, w1 = 34 + 86 * (y0 - top) / (ground - top), 34 + 86 * (y1 - top) / (ground - top)
        cr.move_to(tx - w0, y0)
        cr.line_to(tx + w1, y1)
        cr.move_to(tx + w0, y0)
        cr.line_to(tx - w1, y1)
    cr.stroke()
    cr.rectangle(tx - 60, top - 70, 120, 70)
    cr.fill()
    poly(cr, [(tx - 78, top - 68), (tx, top - 112), (tx + 78, top - 68)])
    cr.fill()
    cr.set_source_rgba(1, 0.78, 0.42, 1)
    for k in range(3):
        cr.rectangle(tx - 50 + k * 36, top - 56, 28, 32)
    cr.fill()
    glow(cr, tx, top - 40, 120, (1, 0.72, 0.38), 0.45)
    for k in range(7):                                        # torches circling its foot
        a = k * 2 * math.pi / 7
        glow(cr, tx + 150 * math.cos(a), ground - 20 + 18 * math.sin(a), 26, (1, 0.55, 0.18), 0.8)


def bus(cr, x, y, s):
    """The night bus, side-on, lit inside."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    tk.toon(cr, lambda c: tk.tk_rrect(c, 0, -230, 640, 200, 26), hexa("#12302d"), None, (0, 0), None, lw=5)
    for k in range(5):
        cr.set_source_rgba(0.75, 0.95, 0.85, 0.9)
        tk.tk_rrect(cr, 90 + k * 104, -205, 86, 90, 10)
        cr.fill()
    cr.set_source_rgba(0.04, 0.05, 0.06, 1)                  # a head in one window, shapes at the back
    cr.arc(305, -150, 18, 0, 2 * math.pi)
    cr.fill()
    for hx in (510, 545):
        cr.arc(hx, -150, 16, 0, 2 * math.pi)
        cr.fill()
        for ex in (-6, 6):
            glow(cr, hx + ex, -153, 9, (1, 0.95, 0.8), 0.9)
    hud2d._text(cr, "9", 40, -150, 54, (1, 0.62, 0.15, 1), "Liberation Mono")
    for wx in (120, 520):
        cr.set_source_rgba(0.03, 0.03, 0.04, 1)
        cr.arc(wx, -30, 44, 0, 2 * math.pi)
        cr.fill()
    glow(cr, -10, -70, 160, (1, 0.95, 0.8), 0.5)
    cr.restore()


def banner(path, w=2560, h=1440):
    """2560 x 1440. Everything that matters sits in the centre 1546 x 423 that every device shows."""
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    cr = cairo.Context(s)
    sky(cr, w, h)
    moon(cr, 2150, 610, 95)
    ground = 990
    skyline(cr, w, h, ground)
    bus(cr, 175, 975, 0.46)
    sx0, sy0, sx1, sy1 = 507, 508, 2053, 931                 # the safe area
    tk.manya_bust(cr, 760, sy1 - 430 * 0.52 + 60, 0.52, 0.0)
    g = cairo.LinearGradient(0, sy1 - 30, 0, sy1 + 40)       # she sits behind the dark of the ground
    g.add_color_stop_rgba(0, *hexa("#07080f", 0))
    g.add_color_stop_rgba(1, *hexa("#07080f"))
    cr.set_source(g)
    cr.rectangle(560, sy1 - 30, 420, h - sy1 + 30)
    cr.fill()
    tx = 1000
    size = 128
    size *= min(1.0, (sx1 - tx - 20) / text_width(cr, NAME, size, hud2d.ROUND))
    hud2d._text(cr, "MIDNIGHT WITH ", tx, 690, size, (1, 1, 1, 1), hud2d.ROUND, outline=INK, ow=10, shadow=0.5)
    mx = tx + text_width(cr, "MIDNIGHT WITH ", size, hud2d.ROUND)
    glow(cr, mx + 120, 650, 240, AMBER, 0.18)
    hud2d._text(cr, "MANYA", mx, 690, size, AMBER, hud2d.ROUND, outline=INK, ow=10, shadow=0.5)
    sub = "Horror stories where YOU choose what happens next"
    ss = min(46.0, 46 * (sx1 - tx - 20) / text_width(cr, sub, 46, hud2d.ROUND))
    hud2d._text(cr, sub, tx + 4, 772, ss, (1, 1, 1, 0.92), hud2d.ROUND, shadow=0.5)
    pill = "COMMENT A OR B"
    pw = text_width(cr, pill, 40, hud2d.ROUND) + 60
    cr.set_source_rgba(*hud2d.YELLOW)
    tk.tk_rrect(cr, tx, 815, pw, 70, 35)
    cr.fill()
    hud2d._text(cr, pill, tx + 30, 864, 40, (0.08, 0.06, 0.04, 1), hud2d.ROUND)
    rest = "the top answer decides the next part"
    rs = min(36.0, 36 * (sx1 - tx - pw - 44) / text_width(cr, rest, 36, hud2d.ROUND))
    hud2d._text(cr, rest, tx + pw + 24, 862, rs, (1, 1, 1, 0.8), hud2d.ROUND)
    s.write_to_png(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    avatar(os.path.join(OUT, "avatar.png"))
    banner(os.path.join(OUT, "banner.png"))
    print("wrote", OUT)
