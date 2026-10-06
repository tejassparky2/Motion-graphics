#!/usr/bin/env python3
"""Export the "Interestingly Strange" logo set to out/brand/.

  python make_logo.py

Files:
  avatar.png / avatar.svg      800x800 profile picture (YouTube crops it to a circle; everything sits inside it)
  mark.png                     mascot alone on transparent, 1024x1024
  lockup_light.png / .svg      mascot + wordmark on transparent, for light backgrounds (2000x760)
  lockup_dark.png              same for dark backgrounds
  preview.png                  how the avatar and lockups look at real sizes on light and dark UI
"""
import math
import os

from motion.engine import cairo, hexc
from motion.brand import CREAM, YELLOW, WHITE, ORANGE, mascot, sparkle, wordmark

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "brand")


def avatar(cr, size=800):
    s = size / 800
    cr.save()
    cr.scale(s, s)
    cr.set_source_rgba(*YELLOW)
    cr.paint()
    # soft rays behind the mascot
    cr.save()
    cr.translate(400, 430)
    for k in range(12):
        cr.rotate(math.pi / 6)
        cr.move_to(0, 0)
        cr.line_to(-60, -520)
        cr.line_to(60, -520)
        cr.close_path()
        cr.set_source_rgba(*hexc("#ffc21a"))
        cr.fill()
    cr.restore()
    for (x, y, r, c) in [(160, 250, 30, WHITE), (640, 230, 22, WHITE), (600, 620, 26, ORANGE), (125, 430, 18, ORANGE)]:
        sparkle(cr, x, y, r, c, seed=int(x))
    mascot(cr, 395, 492, 1.95)
    cr.restore()


def lockup(cr, dark=False):
    mascot(cr, 300, 420, 1.45)
    wordmark(cr, 1210, 540, 1.25, dark=dark)


def export():
    os.makedirs(OUT, exist_ok=True)
    # avatar
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    avatar(cairo.Context(surf))
    surf.write_to_png(f"{OUT}/avatar.png")
    svg = cairo.SVGSurface(f"{OUT}/avatar.svg", 800, 800)
    avatar(cairo.Context(svg))
    svg.finish()
    # mark
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1024)
    mascot(cairo.Context(surf), 505, 620, 2.45)
    surf.write_to_png(f"{OUT}/mark.png")
    # lockups
    for dark in (False, True):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2000, 760)
        lockup(cairo.Context(surf), dark)
        surf.write_to_png(f"{OUT}/lockup_{'dark' if dark else 'light'}.png")
    svg = cairo.SVGSurface(f"{OUT}/lockup_light.svg", 2000, 760)
    lockup(cairo.Context(svg))
    svg.finish()
    preview()


def preview():
    """Avatar at YouTube's real display sizes (176/88/40 px circles) + lockups, on light and dark UI."""
    W, H = 1400, 1000
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    big = cairo.ImageSurface.create_from_png(f"{OUT}/avatar.png")
    for row, (bg, fg) in enumerate([(hexc("#ffffff"), hexc("#0f0f0f")), (hexc("#0f0f0f"), hexc("#f1f1f1"))]):
        y0 = row * 500
        cr.rectangle(0, y0, W, 500)
        cr.set_source_rgba(*bg)
        cr.fill()
        x = 60
        for d in (176, 88, 40):
            cr.save()
            cr.arc(x + d / 2, y0 + 60 + d / 2, d / 2, 0, 2 * math.pi)
            cr.clip()
            cr.translate(x, y0 + 60)
            cr.scale(d / 800, d / 800)
            cr.set_source_surface(big)
            cr.get_source().set_filter(cairo.FILTER_BEST)
            cr.paint()
            cr.restore()
            cr.set_source_rgba(*fg)
            cr.select_font_face("sans-serif")
            cr.set_font_size(18)
            cr.move_to(x, y0 + 60 + 176 + 30)
            cr.show_text(f"{d}px")
            x += d + 50
        lk = cairo.ImageSurface.create_from_png(f"{OUT}/lockup_{'dark' if row else 'light'}.png")
        cr.save()
        cr.translate(560, y0 + 40)
        cr.scale(0.4, 0.4)
        cr.set_source_surface(lk)
        cr.get_source().set_filter(cairo.FILTER_BEST)
        cr.paint()
        cr.restore()
        cr.save()
        cr.translate(560, y0 + 380)
        cr.scale(0.15, 0.15)
        cr.set_source_surface(lk)
        cr.get_source().set_filter(cairo.FILTER_BEST)
        cr.paint()
        cr.restore()
    surf.write_to_png(f"{OUT}/preview.png")


if __name__ == "__main__":
    export()
    print("wrote", sorted(os.listdir(OUT)))
