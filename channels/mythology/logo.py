"""Logo for the Kannada channel "Namma Purana" (owner, 7 Nov 2026: "Give me logo and bio for kannada channel name is
namma purana words in English"). Karnataka flag colours (yellow and red) on deep maroon, the golden petal halo of our
videos, and a lit diya; the name in English letters. Everything sits inside the circle that Instagram and YouTube
crop profile pictures to.

Usage: python -I -X utf8 channels/mythology/logo.py <out_dir>
Writes namma_purana_logo_1080.png (profile picture), namma_purana_logo_800.png (YouTube) and a 110 px preview."""
import math
import os
import sys

import cairo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
from poster import HEAD_FONT, MONO_FONT, draw_text  # noqa: E402

S = 1080
YELLOW = (1.0, 0.82, 0.18)
RED = (0.86, 0.13, 0.13)
GOLD = (0.95, 0.74, 0.28)
CREAMY = (0.98, 0.93, 0.80)


def text(cr, s, cx, cy, size, color, font=HEAD_FONT, tracking=0):
    draw_text(cr, s, cx, cy, size, color, 1.0, font, "cm", tracking=tracking)


def petals(cr, cx, cy, r, n, length, width, color, alpha=1.0):
    for k in range(n):
        a = k * 2 * math.pi / n
        cr.save()
        cr.translate(cx + math.cos(a) * r, cy + math.sin(a) * r)
        cr.rotate(a)
        cr.scale(length, width)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*color, alpha)
        cr.fill()


def diya(cr, cx, cy, w):
    """A clay lamp with a tall flame and a soft glow; (cx, cy) is the lamp's rim centre."""
    g = cairo.RadialGradient(cx, cy - w * 0.55, 5, cx, cy - w * 0.45, w * 1.25)
    g.add_color_stop_rgba(0, 1.0, 0.85, 0.4, 0.75)
    g.add_color_stop_rgba(0.45, 1.0, 0.6, 0.15, 0.25)
    g.add_color_stop_rgba(1, 1.0, 0.6, 0.15, 0)
    cr.set_source(g)
    cr.arc(cx, cy - w * 0.45, w * 1.25, 0, 2 * math.pi)
    cr.fill()
    # lamp body: a shallow bowl with a pinched spout on the right
    cr.move_to(cx - w * 0.62, cy)
    cr.curve_to(cx - w * 0.58, cy + w * 0.38, cx + w * 0.3, cy + w * 0.42, cx + w * 0.5, cy + w * 0.08)
    cr.curve_to(cx + w * 0.62, cy - w * 0.02, cx + w * 0.72, cy - w * 0.08, cx + w * 0.78, cy - w * 0.12)
    cr.curve_to(cx + w * 0.6, cy - w * 0.04, cx + w * 0.3, cy - w * 0.02, cx - w * 0.62, cy)
    cr.close_path()
    lg = cairo.LinearGradient(cx, cy - w * 0.1, cx, cy + w * 0.4)
    lg.add_color_stop_rgb(0, 0.86, 0.48, 0.22)
    lg.add_color_stop_rgb(1, 0.55, 0.24, 0.10)
    cr.set_source(lg)
    cr.fill_preserve()
    cr.set_source_rgb(*YELLOW)
    cr.set_line_width(w * 0.035)
    cr.stroke()
    for k in range(5):                                  # a row of painted dots on the lamp
        cr.arc(cx - w * 0.36 + k * w * 0.16, cy + w * 0.16, w * 0.025, 0, 2 * math.pi)
        cr.set_source_rgb(*YELLOW)
        cr.fill()
    # flame
    fx, fy = cx + w * 0.62, cy - w * 0.14
    for scale, col in ((1.0, (1.0, 0.55, 0.12)), (0.72, (1.0, 0.82, 0.25)), (0.42, (1.0, 0.98, 0.85))):
        h = w * 0.95 * scale
        cr.move_to(fx, fy)
        cr.curve_to(fx - h * 0.42, fy - h * 0.25, fx - h * 0.12, fy - h * 0.7, fx + h * 0.02, fy - h)
        cr.curve_to(fx + h * 0.2, fy - h * 0.68, fx + h * 0.4, fy - h * 0.25, fx, fy)
        cr.close_path()
        cr.set_source_rgb(*col)
        cr.fill()


def logo(size):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    cr = cairo.Context(surf)
    cr.scale(size / S, size / S)
    c = S / 2
    bg = cairo.RadialGradient(c, c * 0.9, 60, c, c, S * 0.72)
    bg.add_color_stop_rgb(0, 0.55, 0.08, 0.08)
    bg.add_color_stop_rgb(1, 0.22, 0.03, 0.04)
    cr.set_source(bg)
    cr.paint()
    # the golden halo of our videos: petals, two rings in the Karnataka yellow and red
    petals(cr, c, c, 470, 36, 34, 14, GOLD, 0.95)
    cr.arc(c, c, 440, 0, 2 * math.pi)
    cr.set_source_rgb(*YELLOW)
    cr.set_line_width(16)
    cr.stroke()
    cr.arc(c, c, 418, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.set_line_width(12)
    cr.stroke()
    for k in range(48):                                 # soft rays behind the lamp
        a = k * 2 * math.pi / 48
        cr.move_to(c + math.cos(a) * 120, 430 + math.sin(a) * 120)
        cr.line_to(c + math.cos(a) * 330, 430 + math.sin(a) * 330)
    cr.set_source_rgba(1, 0.85, 0.45, 0.10)
    cr.set_line_width(10)
    cr.stroke()
    diya(cr, c - 40, 470, 250)
    text(cr, "NAMMA", c, 630, 104, CREAMY, HEAD_FONT, tracking=14)
    text(cr, "PURANA", c, 760, 190, YELLOW)
    cr.move_to(c - 230, 875)
    cr.line_to(c + 230, 875)
    cr.set_source_rgb(*RED)
    cr.set_line_width(10)
    cr.stroke()
    return surf


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    logo(1080).write_to_png(os.path.join(out, "namma_purana_logo_1080.png"))
    logo(800).write_to_png(os.path.join(out, "namma_purana_logo_800.png"))
    # what it looks like as a 110 px round profile picture
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, 330, 130)
    sc = cairo.Context(small)
    sc.set_source_rgb(1, 1, 1)
    sc.paint()
    for i, d in enumerate((110, 56)):
        img = logo(d)
        x, y = 10 + i * 150, 10
        sc.save()
        sc.arc(x + d / 2, y + d / 2, d / 2, 0, 2 * math.pi)
        sc.clip()
        sc.set_source_surface(img, x, y)
        sc.paint()
        sc.restore()
    small.write_to_png(os.path.join(out, "namma_purana_logo_preview_small.png"))
    print("wrote logos to", out)


main()
