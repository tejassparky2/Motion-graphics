#!/usr/bin/env python3
"""Brand kit for the doctor channel ("Doc and the Organs"), built around the owner's logo (assets/brand/doc_logo.png).

  python make_doc_brand.py                 # name from NAME below
  python make_doc_brand.py --name "Another Name"

Writes out/doc_brand/:
  avatar.png     800x800 profile picture (YouTube crops it to a circle; everything sits inside it)
  banner.png     2560x1440 channel banner; the text sits inside the 1546x423 area every device shows
  lockup.png     logo + name on transparent, 2000x700 (for thumbnails, end screens, watermark)
  watermark.png  150x150 video watermark (YouTube Studio > Customization > Branding)
  preview.png    how the avatar and banner look at real sizes
"""
import argparse
import math
import os

from motion import doc_brand as brand, engine
from motion.engine import WHITE, cairo

NAME = brand.CHANNEL
TAGLINE = brand.TAGLINE
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "doc_brand")


def navy_bg(cr, W, H):
    g = cairo.RadialGradient(W * 0.5, H * 0.5, 0, W * 0.5, H * 0.5, max(W, H) * 0.7)
    g.add_color_stop_rgba(0, *brand.NAVY[:3], 1)
    g.add_color_stop_rgba(1, *brand.NAVY_D[:3], 1)
    cr.set_source(g)
    cr.paint()
    for k in range(9):   # faint glowing rings, like the logo's edge
        cr.arc(W * 0.5, H * 0.5, 260 + 170 * k, 0, 2 * math.pi)
        cr.set_source_rgba(*brand.GLOW[:3], 0.10)
        cr.set_line_width(6)
        cr.stroke()


def glow_disc(cr, x, y, d):
    """The owner's logo with a soft blue glow behind it; (x, y) is the centre."""
    for k in range(10, 0, -1):
        cr.arc(x, y, d / 2 + 4 * k, 0, 2 * math.pi)
        cr.set_source_rgba(*brand.GLOW[:3], 0.05)
        cr.fill()
    brand.logo_disc(cr, x - d / 2, y - d / 2, d)


def name_block(cr, x, y, size, max_w):
    """DOC / AND THE / ORGANS in the logo's colours, left-aligned at x, as one line."""
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    runs = brand.name_tag_runs() if NAME == brand.CHANNEL_DEFAULT else [(NAME.upper(), WHITE)]
    cr.set_font_size(size)
    total = sum(cr.text_extents(t).x_advance for t, _ in runs)
    if total > max_w:
        size *= max_w / total
        cr.set_font_size(size)
    cx = x
    for t, col in runs:
        cr.move_to(cx, y)
        cr.text_path(t)
        cr.set_source_rgba(*brand.NAVY_D[:3], 1)
        cr.set_line_width(size * 0.16)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
        cr.set_source_rgba(*col)
        cr.fill()
        cx += cr.text_extents(t).x_advance
    return size


def banner(cr):
    W, H = 2560, 1440
    navy_bg(cr, W, H)
    # everything inside the 1546x423 area every device shows: logo left, name and tagline right
    sx = (W - 1546) / 2
    glow_disc(cr, sx + 200, H / 2, 390)
    name_block(cr, sx + 440, H / 2 + 30, 150, 1060)
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(58)
    cr.move_to(sx + 444, H / 2 + 120)
    cr.set_source_rgba(*WHITE)
    cr.show_text(TAGLINE)


def lockup(cr):
    glow_disc(cr, 350, 350, 620)
    name_block(cr, 720, 400, 170, 1240)


def main():
    global NAME
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=NAME)
    NAME = brand.CHANNEL = ap.parse_args().name
    engine.set_style("clean")
    os.makedirs(OUT, exist_ok=True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    c = cairo.Context(s)
    c.set_source_rgba(1, 1, 1, 1)
    c.paint()
    brand.logo_disc(c, 0, 0, 800)
    s.write_to_png(os.path.join(OUT, "avatar.png"))
    w = cairo.ImageSurface(cairo.FORMAT_ARGB32, 150, 150)
    c = cairo.Context(w)
    c.arc(75, 75, 75, 0, 2 * math.pi)
    c.clip()
    brand.logo_disc(c, 0, 0, 150)
    w.write_to_png(os.path.join(OUT, "watermark.png"))
    b = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2560, 1440)
    banner(cairo.Context(b))
    b.write_to_png(os.path.join(OUT, "banner.png"))
    lk = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2000, 700)
    lockup(cairo.Context(lk))
    lk.write_to_png(os.path.join(OUT, "lockup.png"))
    # preview: banner as a phone sees it (safe area), and the avatar as a circle at 176 px and 48 px
    p = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1600, 700)
    c = cairo.Context(p)
    c.set_source_rgb(0.97, 0.97, 0.97)
    c.paint()
    c.save()
    c.translate(20, 20)
    c.scale(1546 / 2560 * 0.98, 1546 / 2560 * 0.98)
    c.set_source_surface(b, 0, 0)
    c.paint()
    c.restore()
    for (x, y, d) in ((80, 480, 176), (300, 540, 48)):
        c.save()
        c.arc(x + d / 2, y + d / 2, d / 2, 0, 2 * math.pi)
        c.clip()
        c.translate(x, y)
        c.scale(d / 800, d / 800)
        c.set_source_surface(s, 0, 0)
        c.paint()
        c.restore()
    c.set_source_rgb(0.1, 0.1, 0.1)
    c.select_font_face("Anton")
    c.set_font_size(40)
    c.move_to(380, 580)
    c.show_text(NAME)
    p.write_to_png(os.path.join(OUT, "preview.png"))
    print(f"wrote {OUT}/ (avatar, banner, lockup, watermark, preview) for {NAME!r}")


if __name__ == "__main__":
    main()
