#!/usr/bin/env python3
"""Brand kit for the doctor channel ("Doc and the Organs"), in the videos' clean style.

  python make_doc_brand.py                 # name from NAME below
  python make_doc_brand.py --name "Another Name"

Writes out/doc_brand/:
  avatar.png     800x800 profile picture (YouTube crops it to a circle; everything sits inside it)
  banner.png     2560x1440 channel banner; the text sits inside the 1546x423 area every device shows
  lockup.png     mascot + name on transparent, 2000x700 (for thumbnails, end screens, watermark)
  watermark.png  150x150 video watermark (YouTube Studio > Customization > Branding)
  preview.png    how the avatar and banner look at real sizes
"""
import argparse
import math
import os

from motion import doc_brand as brand, engine
from motion.engine import INK, WHITE, at, blob, cairo, hexc, line, rrect_pts, shape

NAME = brand.CHANNEL
TAGLINE = brand.TAGLINE
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "doc_brand")
SKY = brand.SKY
cross, mascot, avatar = brand.cross, brand.mascot, brand.avatar


def name_text(cr, x, y, size, color=INK, halo=WHITE, max_w=None):
    """The name centred on x, DOC in red; shrinks to fit max_w. Returns the font size used."""
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    runs = [(t, color if col == INK else col) for t, col in brand.name_runs(NAME)]
    cr.set_font_size(size)
    total = sum(cr.text_extents(t).x_advance for t, _ in runs)
    if max_w and total > max_w:
        size *= max_w / total
        cr.set_font_size(size)
        total = max_w
    cx = x - total / 2
    for t, col in runs:
        cr.move_to(cx, y)
        cr.text_path(t)
        if halo[3] > 0:
            cr.set_source_rgba(*halo)
            cr.set_line_width(size * 0.24)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke_preserve()
        cr.set_source_rgba(*col)
        cr.fill()
        cx += cr.text_extents(t).x_advance
    return size


def cast_row(cr, y, scale, t=0.0):
    """The channel's characters in a row: brain, kidney, liver, tooth, eye, toe."""
    from motion.organs import big_lobe_pts, brain, lobe
    from videos.kidney_donor import kidney
    from videos.toe_thumb import toe_char
    from videos.tooth_eye import eyeball, tooth
    items = [
        (lambda x: brain(cr, t, x, y, 0.62 * scale, "happy")),
        (lambda x: kidney(cr, t, x, y + 10, 0.8 * scale, 1, "happy")),
        (lambda x: lobe(cr, t, big_lobe_pts(x + 30 * scale, y, 0.62 * scale), x - 10 * scale, y - 20 * scale, 0.7 * scale,
                        "happy")),
        (lambda x: tooth(cr, t, x, y + 20 * scale, 0.75 * scale, "happy")),
        (lambda x: eyeball(cr, t, x, y, 0.38 * scale, "happy", cloudy=0.0)),
        (lambda x: toe_char(cr, t, x, y, 0.95 * scale, mood="happy")),
    ]
    return items


def banner(cr):
    W, H = 2560, 1440
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(14):
        line(cr, [(-100, 110 * k), (900, 110 * k + 40), (1800, 110 * k - 20), (2700, 110 * k + 30)], 8, hexc("#7cc3d1"),
             seed=40 + k, amp=0)
    # safe area (1546x423, centred): mascot left, name and tagline right; characters along the bottom edge of it
    sx = (W - 1546) / 2
    cross(cr, sx + 190, H / 2, 190, hexc("#ffffff", 0.9))
    with at(cr, sx + 190, H / 2 + 30, 0.62):
        mascot(cr)
    name_text(cr, sx + 940, H / 2 + 20, 190, max_w=1000)
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(62)
    tw = cr.text_extents(TAGLINE).x_advance
    with at(cr, sx + 940, H / 2 + 120, 1.0):
        shape(cr, rrect_pts(-tw / 2 - 30, -56, tw + 60, 84, 16, 20), WHITE, seed=50, amp=0, lw=5)
        cr.move_to(-tw / 2, 6)
        cr.set_source_rgba(*INK)
        cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(62)
        cr.show_text(TAGLINE)
    # the cast, outside the text area (visible on TV/desktop; trimmed on phones, which is fine)
    items = cast_row(cr, 0, 1.0)
    xs = [300, 700, 1100, 1460, 1860, 2260]
    for x, draw in zip(xs, items):
        cr.save()
        cr.translate(0, H / 2 + 420)
        draw(x)
        cr.restore()


def lockup(cr):
    with at(cr, 330, 360, 0.95):
        mascot(cr)
    name_text(cr, 1240, 420, 300, halo=hexc("#ffffff", 0.0), max_w=1300)


def main():
    global NAME
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=NAME)
    NAME = brand.CHANNEL = ap.parse_args().name
    engine.set_style("clean")
    os.makedirs(OUT, exist_ok=True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    avatar(cairo.Context(s))
    s.write_to_png(os.path.join(OUT, "avatar.png"))
    w = cairo.ImageSurface(cairo.FORMAT_ARGB32, 150, 150)
    c = cairo.Context(w)
    c.arc(75, 75, 75, 0, 2 * math.pi)
    c.clip()
    avatar(c, 150)
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
